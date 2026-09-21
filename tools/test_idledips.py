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

from idledips import (EWMA_SHIFT, FIXTURES, GATE_THROTTLE, IDLE_INDEX_MAX,
                      IDLE_ROUGH_100, REARM_RPM, ROUGH_DEADBAND_RPM,
                      ROUGH_OUT_SHIFT, ROUGH_SHIFT, SETTLE_S, TRIP_RPM,
                      depths, dips, dips_cheap, firing_interval_s,
                      idle_index, rough_bands, roughness, segments)
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


class Depths(unittest.TestCase):
    def test_depths_are_the_same_events_deepest_first(self):
        log = series(30.0, events=((5.0, 0.1, 40.0), (12.0, 0.1, 22.0)))
        got, span = depths(log, 20)
        self.assertEqual([round(d) for d in got], [40, 22])
        self.assertEqual(len(got), len(dips(log, 20)[0]))


class SegmentRate(unittest.TestCase):
    """0x280's engine-speed field is recomputed once per firing event.

    That is what makes a dip in it a per-cylinder quantity rather than a
    smoothed one, and it is the measurement docs/engine-health.md argues the
    energy budget of one lost power stroke from. It is asserted as a band
    rather than a figure: what has to survive is that the interval tracks the
    firing rate and not the 10 ms frame period.
    """

    @classmethod
    def setUpClass(cls):
        cls.rpm = read_log(os.path.join(FIXTURES,
                           "17_drive_property_z1.txt"))[0]

    def test_the_firing_interval_is_two_revolutions_over_four(self):
        self.assertAlmostEqual(firing_interval_s(800.0), 0.0375)
        self.assertAlmostEqual(firing_interval_s(1600.0), 0.01875)

    def test_the_update_interval_tracks_firing_and_not_the_frame_period(self):
        rows = segments(self.rpm)
        self.assertGreater(len(rows), 3)
        for lo, hi, n, gap, firing in rows:
            if firing < 0.010:
                continue        # below the frame period there is nothing to track
            self.assertLess(abs(gap - firing), 0.005,
                            f"{lo}-{hi} rpm: {gap*1000:.1f} ms update against "
                            f"{firing*1000:.1f} ms firing")

    def test_it_never_updates_faster_than_the_frames_arrive(self):
        for lo, hi, n, gap, firing in segments(self.rpm):
            self.assertGreaterEqual(gap, 0.009)


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


class Roughness(unittest.TestCase):
    """Grading the idle rather than counting events past a threshold."""

    def test_the_frozen_constants_are_the_frozen_constants(self):
        """The same tripwire as for the cheap detector, and a stronger one.

        The 100 point of the index IS the engine before the repair. That
        engine is gone, so nothing can re-anchor the scale -- moving any of
        these silently re-bases every reading ever taken against them.
        """
        self.assertEqual(
            (ROUGH_DEADBAND_RPM, ROUGH_SHIFT, ROUGH_OUT_SHIFT,
             IDLE_ROUGH_100, IDLE_INDEX_MAX),
            (3, 8, 5, 64, 200))

    def test_a_perfectly_steady_idle_grades_zero(self):
        mean_rpm, counts, n, idle_s = roughness(gated(30.0))
        self.assertEqual((mean_rpm, counts), (0.0, 0))
        self.assertGreater(idle_s, 20.0)

    def test_steps_under_the_deadband_contribute_nothing(self):
        """A 2 rpm wobble is the idle's own noise, not combustion."""
        wobble = [(t, int(round((800 + (2 if i % 2 else 0)) * 4)), 38, 5)
                  for i, (t, _) in enumerate(series(30.0))]
        mean_rpm, counts, n, _ = roughness(wobble)
        self.assertGreater(n, 100)          # it did see the steps
        self.assertEqual((mean_rpm, counts), (0.0, 0))   # and graded them zero

    def test_a_repeated_value_is_not_a_step(self):
        """0x280 holds its speed field for three or four frames at idle.

        Stepping per frame instead of per change would make the answer depend
        on idle speed through the hold ratio, which is an artefact. The two
        series below are the same engine sampled at two hold lengths and must
        grade the same.
        """
        def held(hold):
            out, v = [], 800.0
            for i, (t, _) in enumerate(series(60.0)):
                if i % hold == 0:
                    v = 800.0 + (10.0 if (i // hold) % 2 else 0.0)
                out.append((t, int(round(v * 4)), 38, 5))
            return out
        three = roughness(held(3))[0]
        five = roughness(held(5))[0]
        self.assertAlmostEqual(three, five, delta=0.01)

    def test_it_grades_a_ramp_at_zero_where_a_baseline_would_not(self):
        """The whole reason the step is used instead of a deviation.

        A lagging first-order baseline sits above a falling idle and reports a
        permanent one-sided deviation out of nothing. The step does not.
        """
        mean_rpm, counts, _, _ = roughness(gated(60.0, ramp=-2.0))
        self.assertEqual(counts, 0)
        self.assertLess(mean_rpm, 0.01)

    def test_deeper_events_grade_higher_with_no_threshold_to_cross(self):
        """The property the count cannot have: it degrades gracefully.

        Three series whose events are under, around and over TRIP_RPM. The
        count would read zero, zero and three; the grade must rise throughout.
        """
        def graded(depth):
            ev = [(5.0 + 4 * i, 0.1, depth) for i in range(6)]
            return roughness(gated(40.0, events=ev))[0]
        under, at, over = graded(8), graded(20), graded(40)
        self.assertLess(under, at)
        self.assertLess(at, over)
        self.assertGreater(under, 0.0)      # and the small one is NOT zero

    def test_the_index_puts_the_old_engine_at_a_hundred_and_clamps(self):
        self.assertEqual(idle_index(IDLE_ROUGH_100), 100)
        self.assertEqual(idle_index(0), 0)
        self.assertEqual(idle_index(255), IDLE_INDEX_MAX)
        self.assertLess(idle_index(IDLE_ROUGH_100 // 2), 100)


class RoughnessAgainstTheFixtures(unittest.TestCase):
    """The separation, and the scale's anchor, held against the real logs.

    ⚠ These are all BEFORE-repair recordings, so the separation below is
    between temperature states of one engine and not between a sick engine
    and a well one. That is the whole of what is available today, and
    docs/next-drive.md question 6 is what asks for the other half.
    """

    @classmethod
    def setUpClass(cls):
        cls.cache = {}

    def read(self, name, t_from=None, t_to=None):
        if name not in self.cache:
            self.cache[name] = read_log(os.path.join(FIXTURES, name))
        return roughness(self.cache[name][3], t_from, t_to)

    def test_the_gate_is_the_cheap_detectors_gate(self):
        """Not decoration: a grade over a different set of samples than the
        count would not be comparable with it, and the two are quoted side by
        side. Proved rather than asserted."""
        for name, lo, hi in (("09_idle_60s_z1.txt", None, None),
                             ("18_coldstart_z1.txt", 50.0, 360.0)):
            g = self.cache.setdefault(
                name, read_log(os.path.join(FIXTURES, name)))[3]
            self.assertAlmostEqual(roughness(g, lo, hi)[3],
                                   dips_cheap(g, lo, hi)[1], delta=1e-9)

    def test_the_rough_engine_is_the_anchor_of_the_scale(self):
        """Two independent recordings of it, agreeing -- which is what makes
        the 100 point worth pinning to them."""
        for name, lo, hi in (("09_idle_60s_z1.txt", None, None),
                             ("18_coldstart_z1.txt", 50.0, 360.0)):
            self.assertAlmostEqual(self.read(name, lo, hi)[0], 2.12, delta=0.10)

    def test_the_smooth_readings_sit_well_under_it(self):
        for name in ("11_idle_noac_z1.txt", "12_idle_ac_z1.txt"):
            self.assertLess(self.read(name)[0], 1.1)

    def test_the_smooth_readings_are_not_at_the_floor(self):
        """The reason the deadband is 3 and not 8. A grade that has already
        reached zero on the smoothest thing ever recorded has nothing left to
        say when the engine gets better."""
        for name in ("11_idle_noac_z1.txt", "12_idle_ac_z1.txt"):
            self.assertGreater(self.read(name)[1], 10)

    def test_the_band_the_count_throws_away_is_where_the_contrast_lives(self):
        """TRIP_RPM is 20 and sits just above the 10-20 rpm band. On the rough
        logs that band carries about a third of the deviation while everything
        at 20 rpm and over carries a few per cent; on the smooth ones the
        latter is exactly nothing."""
        g = self.cache.setdefault(
            "09_idle_60s_z1.txt",
            read_log(os.path.join(FIXTURES, "09_idle_60s_z1.txt")))[3]
        _, parts = rough_bands(g)
        self.assertGreater(parts[2], 20.0)      # 10-20 rpm
        self.assertLess(parts[3], 10.0)         # >= 20 rpm
        gs = self.cache.setdefault(
            "11_idle_noac_z1.txt",
            read_log(os.path.join(FIXTURES, "11_idle_noac_z1.txt")))[3]
        self.assertEqual(rough_bands(gs)[1][3], 0.0)

    def test_the_firmware_shaped_ewma_agrees_with_the_exact_mean(self):
        """The byte that would go on the bus against the number the tables
        quote, on a steady idle where the two have the same meaning."""
        mean_rpm, counts, _, _ = self.read("09_idle_60s_z1.txt")
        self.assertAlmostEqual(counts / 32.0, mean_rpm, delta=0.25)
