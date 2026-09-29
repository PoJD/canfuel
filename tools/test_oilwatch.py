#!/usr/bin/env python3
"""Tests for oilwatch.py.

Most captures are synthesised, because a verdict wants one state held still.
Three are real: the cold idle of 18_coldstart_z1, and the two warm-up drives
of 24/9 walked through both stops -- 24 reaches the middle idle in its band,
19 stands through it too briefly and heats out of it at idle, which is the
thing a driver has to be warned about.
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import io
import os
import tempfile
import unittest

import canlog
from oilwatch import (BELL_DONE, BELL_ON, BELL_STOP, STANDSTILL_MMH, STOPS,
                      THROTTLE_REST, UNTIL, Tail, oil_c, verdict, wait_for)

MID, HOT = STOPS

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        os.pardir, "test", "fixtures")


def slcan(can_id, data, ms):
    return "t%03X%X%s%04X" % (can_id, len(data), bytes(data).hex().upper(),
                              ms % canlog.TIMESTAMP_WRAP_MS)


def capture(seconds, oil_at, moving=True, rate_hz=10, t0=0.0, pedal=False):
    """A synthetic slcan stream: oil, coolant, engine speed and road speed."""
    out = []
    speed = 3000 if moving else 1          # 0x1A0 raw; a standing car sends 1
    throttle = 90 if moving or pedal else THROTTLE_REST
    for i in range(int(seconds * rate_hz)):
        t = t0 + i / rate_hz
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


def drive(*legs):
    """Legs of (seconds, oil_at(t), moving), one continuous capture."""
    out, t0 = [], 0.0
    for secs, oil_at, moving in legs:
        out.append(capture(secs, oil_at, moving=moving, t0=t0))
        t0 += secs
    return "".join(out)


class Verdicts(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "grow.txt")
        self.addCleanup(self.dir.cleanup)

    def tail_for(self, text, stops=STOPS):
        with open(self.path, "w", encoding="ascii") as fh:
            fh.write(text)
        t = Tail(self.path, stops)
        t.poll()
        return t

    def test_a_climb_well_short_of_the_band_says_keep_driving(self):
        t = self.tail_for(capture(300, lambda s: 20.0 + s * 0.5 / 60))
        self.assertEqual(verdict(t)[0], "KEEP DRIVING")

    def test_a_climb_about_to_reach_the_band_gives_warning(self):
        # one minute short of the band at one degree a minute
        t = self.tail_for(capture(300, lambda s: MID.lo_c - 6.0 + s / 60))
        self.assertEqual(verdict(t, lead_s=90)[0], "STOP WITHIN A MINUTE")

    def test_inside_the_band_while_moving_says_stop(self):
        t = self.tail_for(capture(300, lambda s: MID.lo_c + 1.0 + s / 600))
        self.assertEqual(verdict(t)[0], "STOP NOW")
        self.assertIn("mid", verdict(t)[1])

    def test_a_long_enough_idle_in_the_band_is_done(self):
        t = self.tail_for(capture(MID.idle_s + 30, lambda s: 58.0, moving=False))
        self.assertEqual(verdict(t)[0], "IDLING, DONE")
        self.assertIn("drive on", verdict(t)[1])

    def test_a_short_idle_in_the_band_is_not_done_yet(self):
        t = self.tail_for(capture(60, lambda s: 58.0, moving=False))
        self.assertEqual(verdict(t)[0], "IDLING, IN BAND")

    def test_a_standing_car_is_recognised_as_standing(self):
        t = self.tail_for(capture(60, lambda s: 58.0, moving=False))
        self.assertTrue(t.stationary())
        self.assertFalse(t.moving())
        self.assertLessEqual(t.now["speed_mmh"], STANDSTILL_MMH)

    def test_nothing_is_predicted_from_a_flat_channel(self):
        t = self.tail_for(capture(300, lambda s: 30.0))
        self.assertIsNone(t.seconds_to(MID.lo_c))
        self.assertEqual(verdict(t)[0], "KEEP DRIVING")

    def test_after_the_middle_idle_it_watches_for_the_hot_one(self):
        t = self.tail_for(drive((MID.idle_s + 10, lambda s: 58.0, False),
                                (60, lambda s: 60.0, True)))
        self.assertEqual(t.stop(), HOT)
        self.assertEqual(t.log[0][:2], ("mid", "done"))
        self.assertEqual(verdict(t)[0], "KEEP DRIVING")

    def test_a_middle_band_driven_through_is_missed_and_the_hot_one_follows(self):
        t = self.tail_for(capture(300, lambda s: 50.0 + s / 20))
        self.assertEqual(t.log[0][:2], ("mid", "missed"))
        self.assertEqual(t.stop(), HOT)

    def test_an_idle_is_one_standing_not_a_sum_of_short_ones(self):
        half = MID.idle_s * 0.6
        t = self.tail_for(drive((half, lambda s: 58.0, False),
                                (20, lambda s: 58.0, True),
                                (half, lambda s: 58.0, False)))
        self.assertEqual(verdict(t)[0], "IDLING, IN BAND")

    def test_a_touch_of_the_pedal_while_standing_does_not_restart_the_idle(self):
        text = (capture(MID.idle_s * 0.6, lambda s: 58.0, moving=False)
                + capture(3, lambda s: 58.0, moving=False, pedal=True,
                          t0=MID.idle_s * 0.6)
                + capture(MID.idle_s * 0.6, lambda s: 58.0, moving=False,
                          t0=MID.idle_s * 0.6 + 3))
        t = self.tail_for(text)
        self.assertEqual(verdict(t)[0], "IDLING, DONE")

    def test_the_hot_stop_entered_too_warm_counts_once_it_cools_in(self):
        only_hot = [HOT]
        # a degree above the band, cooling half a degree a minute
        t = self.tail_for(capture(HOT.idle_s + 180,
                                  lambda s: HOT.hi_c + 1.0 - s / 120, moving=False),
                          only_hot)
        self.assertEqual(verdict(t)[0], "IDLING, DONE")
        t = self.tail_for(capture(60, lambda s: HOT.hi_c + 2.0, moving=False),
                          only_hot)
        self.assertEqual(verdict(t)[0], "IDLING")
        self.assertIn("cooling", verdict(t)[1])

    def test_above_the_last_band_on_the_move_still_says_stop(self):
        t = self.tail_for(capture(300, lambda s: HOT.hi_c + 3.0), [HOT])
        self.assertEqual(verdict(t)[0], "STOP NOW")

    def test_both_idles_done_and_driven_away_is_all_done(self):
        t = self.tail_for(drive((MID.idle_s + 5, lambda s: 58.0, False),
                                (30, lambda s: 65.0, True),
                                (HOT.idle_s + 5, lambda s: 70.0, False)))
        self.assertEqual(verdict(t)[0], "IDLING, DONE")
        self.assertIn("engine off", verdict(t)[1])
        t = self.tail_for(drive((MID.idle_s + 5, lambda s: 58.0, False),
                                (30, lambda s: 65.0, True),
                                (HOT.idle_s + 5, lambda s: 70.0, False),
                                (10, lambda s: 70.0, True)))
        self.assertEqual(verdict(t)[0], "ALL STOPS DONE")

    def test_a_restarted_watch_arrives_at_the_same_state(self):
        text = drive((MID.idle_s + 5, lambda s: 58.0, False),
                     (120, lambda s: 60.0 + s / 60, True))
        whole = self.tail_for(text)
        with open(self.path, "w", encoding="ascii") as fh:
            fh.write(text[: len(text) // 3])
        piecewise = Tail(self.path)
        piecewise.poll()
        with open(self.path, "w", encoding="ascii") as fh:
            fh.write(text)
        piecewise.poll()
        self.assertEqual((whole.index, whole.log), (piecewise.index, piecewise.log))
        self.assertEqual(verdict(whole), verdict(piecewise))


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
        self.write(capture(300, lambda s: MID.lo_c + 1.0 + s / 600))
        tail = Tail(self.path)
        out = io.StringIO()
        self.assertEqual(wait_for(tail, "stop", 5.0, 0.01, 90.0, out), 0)
        self.assertIn("STOP NOW", out.getvalue())

    def test_nothing_to_report_times_out_with_2_and_is_not_a_failure(self):
        self.write(capture(300, lambda s: 20.0 + s * 0.1 / 60))
        tail = Tail(self.path)
        out = io.StringIO()
        self.assertEqual(wait_for(tail, "stop", 0.2, 0.01, 90.0, out), 2)
        self.assertIn("KEEP DRIVING", out.getvalue())

    def test_it_sees_the_state_arrive_in_a_file_that_is_still_growing(self):
        cold = capture(300, lambda s: 20.0 + s / 60)
        warm = capture(60, lambda s: MID.lo_c + 1.0, t0=300)
        self.write(cold)
        tail = Tail(self.path)
        out = io.StringIO()
        self.assertEqual(wait_for(tail, "stop", 0.05, 0.01, 90.0, out), 2)
        self.write(cold + warm)
        self.assertEqual(wait_for(tail, "stop", 5.0, 0.01, 90.0, out), 0)

    def test_every_until_target_is_a_headline_verdict_can_produce(self):
        produced = set()
        for text in (capture(300, lambda s: MID.lo_c + 1.0),
                     capture(MID.idle_s + 30, lambda s: 58.0, moving=False),
                     drive((MID.idle_s + 5, lambda s: 58.0, False),
                           (30, lambda s: 65.0, True),
                           (HOT.idle_s + 5, lambda s: 70.0, False),
                           (10, lambda s: 70.0, True))):
            self.write(text)
            t = Tail(self.path)
            t.poll()
            produced.add(verdict(t)[0])
        for heads in UNTIL.values():
            self.assertTrue(produced & set(heads), f"no state produces {heads}")

    def test_the_bell_states_are_the_actionable_ones(self):
        self.assertEqual(BELL_ON & {"KEEP DRIVING", "WAITING", "IDLING",
                                    "IDLING, IN BAND", "ALL STOPS DONE"}, set())
        self.assertIn("STOP NOW", BELL_STOP)
        self.assertIn("IDLING, DONE", BELL_DONE)
        self.assertEqual(BELL_STOP & BELL_DONE, set())


class TheBands(unittest.TestCase):
    def test_the_stops_are_in_order_and_do_not_overlap(self):
        for a, b in zip(STOPS, STOPS[1:]):
            self.assertLess(a.hi_c, b.lo_c)

    def test_the_hot_band_holds_the_plans_reading(self):
        """plan.md has read 70-72 C of oil since before this tool."""
        self.assertLessEqual(HOT.lo_c, 70.0)
        self.assertGreaterEqual(HOT.hi_c, 72.0)


class AgainstTheRecordings(unittest.TestCase):
    def tail(self, name):
        t = Tail(os.path.join(FIXTURES, name))
        t.poll()
        return t

    def test_the_real_cold_idle_reads_as_a_cold_idle(self):
        tail = self.tail("18_coldstart_z1.txt")
        self.assertTrue(tail.stationary())
        self.assertLess(tail.now["oil"], MID.lo_c)
        self.assertGreater(tail.now["coolant"], 60.0,
                           "the coolant is hot while the oil is not -- "
                           "which is why the gauge is no use for this")
        self.assertEqual(verdict(tail)[0], "IDLING")

    def test_24_had_its_middle_idle_in_the_band(self):
        tail = self.tail("24_mafswap_drive_z1.txt")
        self.assertEqual(tail.log[0][:2], ("mid", "done"))

    def test_19_heated_out_of_the_band_while_standing(self):
        """Stood at 60 C of oil and left at 65: heat soak at idle after a drive.

        Which is why the warning aims at the band's LOWER edge.
        """
        tail = self.tail("19_postfix_drive_z1.txt")
        self.assertEqual(tail.log[0][:2], ("mid", "missed"))


if __name__ == "__main__":
    unittest.main()
