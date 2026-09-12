#!/usr/bin/env python3
"""Tests for oilwatch.py.

The capture is synthesised rather than taken from a fixture, because what has
to be exercised is a warm-up under driving -- and docs/next-drive.md says
plainly that no fixture holds one. That is the whole reason this tool exists.
The one fixture case that is real is the cold idle, and it is asserted below
against 18_coldstart_z1.
"""

from __future__ import annotations

import io
import os
import tempfile
import unittest

import canlog
from oilwatch import (BAND_HI_C, BAND_LO_C, BELL_ON, IDLE_S, STANDSTILL_MMH,
                      THROTTLE_REST, UNTIL, Tail, oil_c, verdict, wait_for)

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        os.pardir, "test", "fixtures")


def slcan(can_id, data, ms):
    return "t%03X%X%s%04X" % (can_id, len(data), bytes(data).hex().upper(),
                              ms % canlog.TIMESTAMP_WRAP_MS)


def capture(seconds, oil_at, moving=True, rate_hz=10):
    """A synthetic slcan stream: oil, coolant, engine speed and road speed."""
    out = []
    speed = 3000 if moving else 1          # 0x1A0 raw; a standing car sends 1
    throttle = 90 if moving else THROTTLE_REST
    for i in range(int(seconds * rate_hz)):
        t = i / rate_hz
        ms = int(t * 1000)
        oil_byte = int(round((oil_at(t) + 48.0) / 0.75))
        out.append(slcan(0x420, [0x01, 0, 0, oil_byte], ms))
        out.append(slcan(0x288, [0, 0xC4], ms))
        out.append(slcan(0x280, [0, 0, 0x80, 0x0C, 0, throttle, 20, 40], ms))
        out.append(slcan(0x1A0, [0, 0x40, speed & 0xFF, speed >> 8], ms))
    return "\n".join(out) + "\n"


class Decoding(unittest.TestCase):
    def test_the_oil_scale_is_the_documented_one(self):
        self.assertEqual(oil_c(0x51), 0x51 * 0.75 - 48.0)

    def test_the_key_off_value_is_not_a_temperature(self):
        self.assertIsNone(oil_c(0xFF))


class Tailing(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "grow.txt")
        self.addCleanup(self.dir.cleanup)

    def write(self, text, mode="a"):
        with open(self.path, mode, encoding="ascii") as fh:
            fh.write(text)

    def test_only_the_appended_part_is_read_again(self):
        self.write(capture(10, lambda t: 40.0), "w")
        tail = Tail(self.path)
        tail.poll()
        self.assertEqual(tail.poll(), 0, "nothing new must read nothing")
        self.write(capture(5, lambda t: 41.0))
        self.assertGreater(tail.poll(), 0)

    def test_a_half_written_line_is_not_lost(self):
        text = capture(6, lambda t: 40.0)
        cut = len(text) // 2
        self.write(text[:cut], "w")
        tail = Tail(self.path)
        tail.poll()
        self.write(text[cut:])
        tail.poll()
        # the channel quantises to 0.75 C a count
        self.assertLess(abs(tail.now["oil"] - 40.0), 0.75)

    def test_the_timestamp_wrap_does_not_go_backwards(self):
        """The adapter's counter wraps every 65.5 s; an hour wraps it 55 times."""
        self.write(capture(200, lambda t: 40.0), "w")
        tail = Tail(self.path)
        tail.poll()
        self.assertGreater(tail.t_s, 190.0)
        times = [t for t, _ in tail.oil]
        self.assertEqual(times, sorted(times))


class Verdicts(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "grow.txt")
        self.addCleanup(self.dir.cleanup)

    def tail_for(self, text):
        with open(self.path, "w", encoding="ascii") as fh:
            fh.write(text)
        t = Tail(self.path)
        t.poll()
        return t

    def test_a_climb_well_short_of_the_band_says_keep_driving(self):
        t = self.tail_for(capture(300, lambda s: 20.0 + s * 0.5 / 60))
        self.assertEqual(verdict(t)[0], "KEEP DRIVING")

    def test_a_climb_about_to_reach_the_band_gives_warning(self):
        # one minute short of the band at one degree a minute
        t = self.tail_for(capture(300, lambda s: BAND_LO_C - 6.0 + s / 60))
        self.assertEqual(verdict(t, lead_s=90)[0], "STOP WITHIN A MINUTE")

    def test_inside_the_band_while_moving_says_stop(self):
        t = self.tail_for(capture(300, lambda s: BAND_LO_C + 2.0 + s / 600))
        self.assertEqual(verdict(t)[0], "STOP NOW")

    def test_above_the_band_is_the_hot_idle_and_says_so(self):
        t = self.tail_for(capture(300, lambda s: BAND_HI_C + 3.0))
        self.assertEqual(verdict(t)[0], "PAST THE BAND")

    def test_a_long_enough_idle_in_the_band_is_done(self):
        t = self.tail_for(capture(IDLE_S + 30, lambda s: 61.5, moving=False))
        head, _ = verdict(t)
        self.assertEqual(head, "IDLING, DONE")

    def test_a_short_idle_in_the_band_is_not_done_yet(self):
        t = self.tail_for(capture(60, lambda s: 61.5, moving=False))
        self.assertEqual(verdict(t)[0], "IDLING, IN BAND")

    def test_a_standing_car_is_recognised_as_standing(self):
        t = self.tail_for(capture(60, lambda s: 61.5, moving=False))
        self.assertTrue(t.stationary())
        self.assertLessEqual(t.now["speed_mmh"], STANDSTILL_MMH)

    def test_nothing_is_predicted_from_a_flat_channel(self):
        t = self.tail_for(capture(300, lambda s: 30.0))
        self.assertIsNone(t.seconds_to(BAND_LO_C))
        self.assertEqual(verdict(t)[0], "KEEP DRIVING")


class Until(unittest.TestCase):
    """--until is the mode an assistant on the same laptop drives this with."""

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "grow.txt")
        self.addCleanup(self.dir.cleanup)

    def write(self, text, mode="w"):
        with open(self.path, mode, encoding="ascii") as fh:
            fh.write(text)

    def test_a_state_already_reached_returns_at_once(self):
        self.write(capture(300, lambda s: BAND_LO_C + 2.0 + s / 600))
        tail = Tail(self.path)
        out = io.StringIO()
        self.assertEqual(wait_for(tail, "band", 5.0, 0.01, 90.0, out), 0)
        self.assertIn("STOP NOW", out.getvalue())

    def test_nothing_to_report_times_out_with_2_and_is_not_a_failure(self):
        self.write(capture(300, lambda s: 20.0 + s * 0.1 / 60))
        tail = Tail(self.path)
        out = io.StringIO()
        self.assertEqual(wait_for(tail, "band", 0.2, 0.01, 90.0, out), 2)
        self.assertIn("KEEP DRIVING", out.getvalue())

    def test_it_sees_the_state_arrive_in_a_file_that_is_still_growing(self):
        cold = capture(300, lambda s: 20.0 + s / 60)
        hot = capture(60, lambda s: BAND_LO_C + 1.0)
        self.write(cold)
        tail = Tail(self.path)
        out = io.StringIO()
        self.assertEqual(wait_for(tail, "band", 0.05, 0.01, 90.0, out), 2)
        self.write(cold + hot)
        self.assertEqual(wait_for(tail, "band", 5.0, 0.01, 90.0, out), 0)

    def test_every_until_target_is_a_headline_verdict_can_produce(self):
        produced = set()
        for oil, moving in ((BAND_LO_C + 2, True), (BAND_HI_C + 3, True),
                            (61.5, False)):
            self.write(capture(IDLE_S + 60, lambda s, o=oil: o, moving=moving))
            t = Tail(self.path)
            t.poll()
            produced.add(verdict(t)[0])
        for heads in UNTIL.values():
            self.assertTrue(produced & set(heads),
                            f"no state produces {heads}")

    def test_the_bell_states_are_the_actionable_ones(self):
        self.assertEqual(BELL_ON & {"KEEP DRIVING", "WAITING"}, set())
        self.assertIn("STOP NOW", BELL_ON)


class AgainstTheColdStart(unittest.TestCase):
    def test_the_real_cold_idle_reads_as_a_cold_idle(self):
        tail = Tail(os.path.join(FIXTURES, "18_coldstart_z1.txt"))
        tail.poll()
        self.assertTrue(tail.stationary())
        self.assertLess(tail.now["oil"], BAND_LO_C)
        self.assertGreater(tail.now["coolant"], 60.0,
                           "the coolant is hot while the oil is not -- "
                           "which is why the gauge is no use for this")


if __name__ == "__main__":
    unittest.main()
