#!/usr/bin/env python3
"""Tests for idledips.py -- the dip detector behind the idle tables.

Running them:
    python -m unittest discover -s tools -p 'test_*.py' -v
    python tools/test_idledips.py

These are properties of the detector rather than a copy of the published
counts. Pinning the counts here would put the same numbers in two places and
guarantee that one of them goes stale, which is the thing docs/engine-health.md
and CLAUDE.md both argue against; the counts have exactly one home and it is
the tool's own output.

What is worth holding, and what each test is really about:

- a dip is an EVENT, not a sample. A wide dip and a narrow one of the same
  depth are one event each, or logs of different length cannot be compared
- the baseline has to ride a ramp. Idle falls from about 930 to 800 rpm over a
  cold-start warm-up, and none of that is a dip
- the threshold is a floor, not a band. A 40 rpm excursion counts at 20 and at
  15, and the two numbers are therefore nested rather than independent
- an overshoot is not a dip. Only excursions BELOW the baseline count, because
  the symptom is the engine losing speed
"""

from __future__ import annotations

import os
import unittest

from idledips import (EWMA_SHIFT, FIXTURES, GATE_THROTTLE, REARM_RPM,
                      SETTLE_S, TRIP_RPM, dips, dips_cheap)
from idledips import series as read_log   # the local series() below is synthetic

RATE_HZ = 94.0  # what 0x280 actually arrives at; see docs/can-decoding.md
STEP = 1.0 / RATE_HZ


def series(seconds, baseline=800.0, events=(), ramp=0.0):
    """A synthetic engine-speed series.

    events is a sequence of (start_s, duration_s, depth_rpm); ramp is in rpm
    per second and is applied to the baseline.
    """
    out = []
    n = int(seconds * RATE_HZ)
    for i in range(n):
        t = i * STEP
        v = baseline + ramp * t
        for start, dur, depth in events:
            if start <= t < start + dur:
                v -= depth
        out.append((t, v))
    return out


class DipDetector(unittest.TestCase):
    def test_a_quiet_series_has_no_dips(self):
        events, span = dips(series(30.0), 20)
        self.assertEqual(events, [])
        self.assertAlmostEqual(span, 30.0, delta=0.05)

    def test_one_dip_is_one_event_however_long_it_lasts(self):
        for duration in (0.05, 0.2, 0.5):
            with self.subTest(duration=duration):
                found, _ = dips(series(30.0, events=[(10.0, duration, 40.0)]), 20)
                self.assertEqual(len(found), 1)
                self.assertAlmostEqual(found[0][0], 10.0, delta=duration + 0.05)
                self.assertAlmostEqual(found[0][1], 40.0, delta=1.0)

    def test_separate_dips_are_separate_events(self):
        found, _ = dips(
            series(30.0, events=[(8.0, 0.1, 40.0), (12.0, 0.1, 40.0),
                                 (16.0, 0.1, 40.0)]),
            20,
        )
        self.assertEqual(len(found), 3)

    def test_the_threshold_is_a_floor_so_the_counts_nest(self):
        rpm = series(30.0, events=[(10.0, 0.1, 40.0), (14.0, 0.1, 18.0)])
        at20, _ = dips(rpm, 20)
        at15, _ = dips(rpm, 15)
        self.assertEqual(len(at20), 1)
        self.assertEqual(len(at15), 2)

    def test_a_warm_up_ramp_is_not_a_dip(self):
        """Idle falls about 130 rpm over the cold-start run in 18_coldstart_z1.

        A baseline that could not ride that would report the whole warm-up as
        one long dip, and the cold-start row would be meaningless.
        """
        found, _ = dips(series(300.0, baseline=930.0, ramp=-0.43), 20)
        self.assertEqual(found, [])

    def test_an_overshoot_is_not_a_dip(self):
        found, _ = dips(series(30.0, events=[(10.0, 0.1, -40.0)]), 20)
        self.assertEqual(found, [])

    def test_a_window_can_be_restricted(self):
        rpm = series(30.0, events=[(5.0, 0.1, 40.0), (20.0, 0.1, 40.0)])
        found, span = dips(rpm, 20, 15.0, 25.0)
        self.assertEqual(len(found), 1)
        self.assertAlmostEqual(span, 10.0, delta=0.05)


def gated(seconds, baseline=800.0, events=(), ramp=0.0, throttle=38,
          speed_mmh=5):
    """The same synthetic series in the shape dips_cheap() takes.

    speed_mmh defaults to 5 because that is what a standing car really sends:
    0x1A0 raw speed is 1, never 0. docs/can-decoding.md has the measurement.
    """
    return [(t, int(round(v * 4)), throttle, speed_mmh)
            for t, v in series(seconds, baseline, events, ramp)]


class CheapDetector(unittest.TestCase):
    """The firmware-shaped detector: a filter, a latch and an idle gate."""

    def test_the_frozen_constants_are_the_frozen_constants(self):
        """Not a tautology -- it is a tripwire.

        These were fitted against a rough engine that is about to be repaired,
        after which nothing can re-fit them and any value at all reads zero.
        If this test has to be edited, the prediction in engine-health.md is
        void and has to be rewritten rather than quietly re-based.
        """
        self.assertEqual((EWMA_SHIFT, TRIP_RPM, REARM_RPM, SETTLE_S),
                         (8, 20, 10, 3.0))

    def test_a_quiet_idle_counts_nothing(self):
        found, idle_s = dips_cheap(gated(30.0))
        self.assertEqual(found, [])
        self.assertAlmostEqual(idle_s, 30.0 - SETTLE_S, delta=0.1)

    def test_it_finds_a_dip_and_counts_it_once(self):
        found, _ = dips_cheap(gated(30.0, events=[(10.0, 0.1, 40.0)]))
        self.assertEqual(len(found), 1)
        self.assertAlmostEqual(found[0][0], 10.0, delta=0.2)

    def test_the_latch_stops_one_dip_counting_twice(self):
        """A first-order baseline sags into a long dip where a median does not.

        Without the re-arm rule the signal hovers around the threshold and the
        same excursion is counted several times, so the latch is what makes a
        filter usable here at all.
        """
        found, _ = dips_cheap(gated(30.0, events=[(10.0, 2.0, 40.0)]))
        self.assertEqual(len(found), 1)

    def test_a_moving_car_is_not_idle(self):
        found, idle_s = dips_cheap(
            gated(30.0, events=[(10.0, 0.1, 40.0)], speed_mmh=20000))
        self.assertEqual(found, [])
        self.assertEqual(idle_s, 0.0)

    def test_a_pressed_pedal_is_not_idle(self):
        found, idle_s = dips_cheap(
            gated(30.0, events=[(10.0, 0.1, 40.0)], throttle=GATE_THROTTLE + 6))
        self.assertEqual(found, [])
        self.assertEqual(idle_s, 0.0)

    def test_the_gate_opening_above_idle_books_nothing(self):
        """The measured worst case, and the one that caught a real fault.

        Across the 24 gate openings in 17_drive_property_z1, engine speed at
        the moment the gate opens runs 741 to 1054 rpm -- the clutch beats the
        car to a stop, so the descent is mostly over before road speed reaches
        zero. Mostly. Seeded at 1054 the baseline is still 130 rpm high when a
        fixed three-second delay expires, and books one event that never
        happened.

        17 hides this because its stops are too short to reach the delay at
        all, which is exactly the kind of blind spot a fixture set has and a
        synthetic case does not. The delay is therefore restarted by any
        excursion past the trip threshold before counting begins.

        The range is walked past the measured maximum on purpose: 1054 is what
        was seen in six minutes of one drive, not a bound anybody established.
        """
        for opens_at in (1054, 1200, 1450):
            with self.subTest(opens_at=opens_at):
                run_down = [
                    (t, int(round(max(800.0, opens_at
                                      - (opens_at - 800.0) * t) * 4)), 38, 5)
                    for t, _ in series(30.0)
                ]
                found, idle_s = dips_cheap(run_down)
                self.assertEqual(found, [])
                self.assertGreater(idle_s, 15.0)   # and it still counts as idle


class CheapDetectorAgainstTheFixtures(unittest.TestCase):
    """The separation the prediction rests on, held against the real logs.

    These are the before-repair readings. They are asserted loosely -- a band
    rather than a count -- because what has to survive is the separation, not
    the arithmetic: a warm engine reads zero and a rough one reads roughly ten
    a minute, and no change to this file may blur those into each other.
    """

    @classmethod
    def setUpClass(cls):
        cls.cache = {}

    def rate(self, name, t_from=None, t_to=None):
        if name not in self.cache:
            self.cache[name] = read_log(os.path.join(FIXTURES, name))
        _, _, _, g = self.cache[name]
        found, idle_s = dips_cheap(g, t_from, t_to)
        self.assertGreater(idle_s, 5.0, f"{name}: too little settled idle")
        return len(found) * 60 / idle_s

    def test_a_warm_idle_reads_zero(self):
        self.assertEqual(self.rate("11_idle_noac_z1.txt"), 0.0)
        self.assertEqual(self.rate("12_idle_ac_z1.txt"), 0.0)

    def test_a_rough_idle_reads_about_ten_a_minute(self):
        self.assertGreater(self.rate("09_idle_60s_z1.txt"), 5.0)
        self.assertGreater(self.rate("18_coldstart_z1.txt", 50.0, 360.0), 5.0)

    def test_a_drive_contributes_almost_no_idle_and_no_events(self):
        _, _, _, g = read_log(os.path.join(FIXTURES,
                              "17_drive_property_z1.txt"))
        found, idle_s = dips_cheap(g)
        self.assertLess(idle_s, 30.0)
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
