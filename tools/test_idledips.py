#!/usr/bin/env python3
"""Tests for idledips.py -- the dip detector behind the idle tables.

Running them:
    python -m unittest discover -s tools -p 'test_*.py' -v
    python tools/test_idledips.py

These are properties of the detector rather than a copy of the published
counts. Pinning the counts here would put the same numbers in two places and
guarantee that one of them goes stale, which is the thing CLAUDE.md argues
against; the counts have exactly one home and it is
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

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import os
import unittest

from idledips import (EWMA_SHIFT, FIXTURES, GATE_THROTTLE, IDLE_INDEX_MAX,
                      IDLE_ROUGH_100, REARM_RPM, ROUGH_DEADBAND_RPM,
                      ROUGH_OUT_SHIFT, ROUGH_SHIFT, SETTLE_S, TRIP_RPM,
                      depths, dips, dips_cheap, firing_interval_s,
                      cylinder_runs, idle_index, period_power, rough_bands,
                      roughness, segment_degrees, segments, slot_means,
                      step_hist)
from idledips import series as read_log   # the local series() below is synthetic
from idledips import (START_CRANK_SHIFT, START_DIP_MS, START_FIRED_RPM,
                      START_INVALID, START_SAT, EWMA_SHIFT as BASE_SHIFT,
                      SETTLE_S, TRIP_RPM, GATE_SPEED_MMH, health_summary,
                      start_fields)
from canlog import Frame

RATE_HZ = 94.0  # what 0x280 actually arrives at; see docs/firmware/can-decoding.md
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
    0x1A0 raw speed is 1, never 0. docs/firmware/can-decoding.md has the measurement.
    """
    return [(t, int(round(v * 4)), throttle, speed_mmh)
            for t, v in series(seconds, baseline, events, ramp)]


class CheapDetector(unittest.TestCase):
    """The firmware-shaped detector: a filter, a latch and an idle gate."""

    def test_the_frozen_constants_are_the_frozen_constants(self):
        """Not a tautology -- it is a tripwire.

        These were fitted against a rough engine that is about to be repaired,
        after which nothing can re-fit them and any value at all reads zero.
        If this test has to be edited, the before-repair prediction in
        idledips.py is void and has to be rewritten rather than quietly
        re-based.
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
    """0x280's engine-speed field is recomputed once per 180 deg of crank.

    That is what makes a dip in it a per-cylinder quantity rather than a
    smoothed one -- 180 deg is one power stroke -- and it is the measurement
    docs/engine-health/open.md (S1) argues the energy budget of one lost power
    stroke from. Asserted as a band rather than a figure: what has to survive is that
    the interval tracks the engine and not the 10 ms frame period.

    ⚠ The crank-angle form below is the stronger statement and the one
    docs/firmware/can-decoding.md trap 6 is written from. An interval that sits near the
    firing rate AT ONE SPEED is a coincidence; a constant angle across a
    fivefold change of speed is not.
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
    and a well one. That is still the whole of what is available: the
    post-repair idle was not healthy either.
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


class StepDistribution(unittest.TestCase):
    """The shape the grade is a summary of.

    This is what `--roughness --hist` prints and what docs/firmware/can-decoding.md shows,
    and it is the answer to "what is being measured" -- not an event and not a
    threshold, but how often each size of step between firing events happens.
    """

    def test_a_steady_idle_has_no_steps_at_all(self):
        hist, n = step_hist(gated(30.0))
        self.assertEqual(n, 0)

    def test_the_shares_are_shares(self):
        g = read_log(os.path.join(FIXTURES, "09_idle_60s_z1.txt"))[3]
        hist, n = step_hist(g)
        self.assertGreater(n, 1000)
        self.assertAlmostEqual(sum(hist), 100.0, delta=0.01)

    def test_it_walks_the_same_events_roughness_does(self):
        """Not decoration: the table and the grade are quoted side by side and
        would be incomparable if they were built from different samples."""
        for name, lo, hi in (("09_idle_60s_z1.txt", None, None),
                             ("11_idle_noac_z1.txt", None, None)):
            g = read_log(os.path.join(FIXTURES, name))[3]
            self.assertEqual(step_hist(g, lo, hi)[1], roughness(g, lo, hi)[2])

    def test_the_rough_engine_has_the_fatter_tail(self):
        """The whole claim, held as a property rather than as a copy of the
        published percentages: the pairs differ in the 6-15 rpm columns and
        the smooth one piles up under 4 rpm."""
        def hist(name, lo=None, hi=None):
            return step_hist(read_log(os.path.join(FIXTURES, name))[3], lo, hi)[0]
        rough = hist("09_idle_60s_z1.txt")
        smooth = hist("12_idle_ac_z1.txt")
        self.assertGreater(rough[3], 2 * smooth[3])      # 6-10 rpm
        self.assertGreater(rough[4], 4 * smooth[4])      # 10-15 rpm
        self.assertLess(rough[0] + rough[1], smooth[0] + smooth[1])   # 0-4 rpm


class SegmentDegrees(unittest.TestCase):
    """The gap as crank ANGLE, which is what makes it a mechanism and not a
    coincidence. A four-stroke four fires every 180 deg."""

    @classmethod
    def setUpClass(cls):
        cls.rpm = read_log(os.path.join(FIXTURES,
                           "17_drive_property_z1.txt"))[0]

    def test_the_angle_is_180_degrees_until_the_frame_period_stops_it(self):
        rows = segment_degrees(self.rpm)
        self.assertGreater(len(rows), 5)
        for lo, hi, n, gap, deg in rows:
            if firing_interval_s((lo + hi) / 2.0) < 0.0104:
                continue        # the bus cannot carry 180 deg this fast
            self.assertLess(abs(deg - 180.0), 25.0,
                            f"{lo}-{hi} rpm: {deg:.0f} deg")

    def test_above_three_thousand_it_inflates_rather_than_holding(self):
        """The confirmation, not an exception: a TIME-based mechanism would
        have carried on unchanged where this one cannot."""
        top = [r for r in segment_degrees(self.rpm) if r[0] >= 3200]
        self.assertTrue(top)
        self.assertGreater(top[-1][4], 205.0)

    def test_it_is_a_constant_angle_and_not_a_constant_time(self):
        """The whole argument in one assertion: across the bands the bus can
        carry, the TIME changes several-fold and the ANGLE does not."""
        rows = [r for r in segment_degrees(self.rpm)
                if firing_interval_s((r[0] + r[1]) / 2.0) >= 0.0104]
        gaps = [r[3] for r in rows]
        degs = [r[4] for r in rows]
        self.assertGreater(max(gaps) / min(gaps), 2.0)
        self.assertLess(max(degs) / min(degs), 1.3)


class PerCylinderStructure(unittest.TestCase):
    """A cylinder comes round every four windows, so one that differs from its
    neighbours is a period-4 component. What the tests hold is the METHOD --
    that it finds a planted period and does not invent one -- plus the single
    conclusion that matters, which is that the line is in the smooth recording
    too and is therefore not a fault signature."""

    @classmethod
    def setUpClass(cls):
        cls.cache = {}

    def runs(self, name, t_from=None, t_to=None):
        if name not in self.cache:
            self.cache[name] = read_log(os.path.join(FIXTURES, name))
        return cylinder_runs(self.cache[name][3], t_from, t_to)

    def test_a_planted_weak_cylinder_is_found(self):
        """Every fourth window 3 rpm low, on an otherwise steady idle."""
        g = []
        for i, (t, _) in enumerate(series(120.0)):
            v = 800.0 + (0.5 if (i // 4) % 2 else 0.0)     # something to move
            if (i // 4) % 4 == 0:
                v -= 3.0
            g.append((t, int(round(v * 4)), 38, 5))
        runs = cylinder_runs(g)
        self.assertTrue(runs)
        ratio, n = period_power(runs, 0.25)
        self.assertGreater(ratio, 5.0)

    def test_a_steady_idle_invents_no_cylinder(self):
        """The control the finding needs: no period where none was planted."""
        g = [(t, int(round((800.0 + (i % 7) * 0.25) * 4)), 38, 5)
             for i, (t, _) in enumerate(series(120.0))]
        runs = cylinder_runs(g)
        ratio, n = period_power(runs, 0.25)
        if ratio is not None:
            self.assertLess(ratio, 5.0)

    def test_the_line_is_in_the_smooth_log_too(self):
        """THE conclusion. If this ever fails one way, the line has become a
        fault signature and docs/engine-health/refuted.md A5 is wrong; if it fails the other,
        the method has stopped finding what it found."""
        rough = period_power(self.runs("09_idle_60s_z1.txt"), 0.25)[0]
        smooth = period_power(self.runs("11_idle_noac_z1.txt"), 0.25)[0]
        self.assertGreater(rough, 5.0)
        self.assertGreater(smooth, 5.0)
        self.assertLess(abs(rough - smooth) / max(rough, smooth), 0.5)

    def test_the_control_frequencies_carry_nothing(self):
        for name in ("09_idle_60s_z1.txt", "11_idle_noac_z1.txt"):
            for f in (0.20, 0.30):
                self.assertLess(period_power(self.runs(name), f)[0], 3.0,
                                f"{name} at f={f}")

    def test_no_slot_is_a_consistent_outlier(self):
        """A single failing cylinder would put one slot far below the other
        three. The spread stays a few rpm and no slot runs away."""
        for name in ("09_idle_60s_z1.txt", "11_idle_noac_z1.txt"):
            for r in cylinder_runs(self.cache.setdefault(
                    name, read_log(os.path.join(FIXTURES, name)))[3]):
                got = slot_means(r)
                if got is None or got[3] < 80:
                    continue
                means, spread, se, n, sd_true = got
                self.assertLess(spread, 12.0, name)
                self.assertLess(sd_true, spread, name)   # the bias is real

    def test_the_phase_is_lost_between_runs_so_runs_are_not_pooled(self):
        """Not decoration: pooling them would average four cylinders over a
        random relabelling and delete the effect being looked for."""
        runs = self.runs("18_coldstart_z1.txt", 50.0, 360.0)
        self.assertGreater(len(runs), 5)


class SlotSpreadIsBiased(unittest.TestCase):
    """The plain max-minus-min of four slot means is biased upward by noise.

    This is the trap that would turn a short healthy recording into an
    apparently worse engine than a long sick one, so it is held here rather
    than only warned about in a docstring.
    """

    @staticmethod
    def windowed(seconds, weak_slot=None, weak_rpm=0.0, sigma=3.0, seed=1,
                 hold=4):
        """A synthetic idle in the shape 0x280 really has.

        ⚠ EACH VALUE IS HELD FOR `hold` FRAMES, because that is what the ECU
        does (docs/firmware/can-decoding.md trap 6) and because the window index is what a
        planted per-cylinder effect has to be planted on. Drawing fresh noise
        every FRAME instead makes every frame its own window, which silently
        moves a planted period 4 to period 16 -- that is not hypothetical, it
        is how the first version of this test failed.
        """
        import random
        rnd = random.Random(seed)
        out, w, v = [], -1, 800.0
        for i, (t, _) in enumerate(series(seconds)):
            if i // hold != w:
                w = i // hold
                v = 800.0 + rnd.gauss(0, sigma)
                if weak_slot is not None and w % 4 == weak_slot:
                    v -= weak_rpm
            out.append((t, int(round(v * 4)), 38, 5))
        return out

    def longest(self, gated):
        best = None
        for r in cylinder_runs(gated):
            got = slot_means(r)
            if got is None or got[3] < 80:
                continue
            if best is None or got[3] > best[3]:
                best = got
        return best

    def test_identical_cylinders_still_show_a_spread(self):
        """An engine whose four cylinders are the same, with ordinary noise."""
        got = self.longest(self.windowed(120.0, seed=11))
        self.assertIsNotNone(got, "no run long enough to test")
        means, spread, se, n, sd_true = got
        self.assertGreater(spread, 0.3)      # noise alone makes a spread
        self.assertLess(sd_true, spread)     # and sd_true removes most of it
        self.assertLess(sd_true, 1.0)        # ...leaving nearly nothing

    def test_a_planted_difference_survives_the_correction(self):
        """The other direction: correcting must not delete a real effect."""
        got = self.longest(
            self.windowed(120.0, weak_slot=0, weak_rpm=4.0, seed=3))
        self.assertIsNotNone(got)
        means, spread, se, n, sd_true = got
        self.assertGreater(sd_true, 1.0)
        self.assertEqual(means.index(min(means)), 0)   # and it names the slot



# --- 0x604: what the firmware carries, and its twin in test/test_compute.c ----

CONFIG_H = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        os.pardir, "src", "config.h")


def _config_defines():
    out = {}
    with open(CONFIG_H, encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if len(parts) >= 3 and parts[0] == "#define":
                out[parts[1]] = parts[2].rstrip("uUlL")
    return out


class TheFirmwareCarriesTheseConstants(unittest.TestCase):
    """src/config.h must hold the frozen constants VERBATIM.

    The frozen-constants tests above stop this file moving; this stops the
    firmware drifting away from it, which would be the same re-basing of every
    reading done from the other side.
    """

    def test_the_grade(self):
        d = _config_defines()
        self.assertEqual(
            (int(d["ROUGH_DEADBAND_RPM"]), int(d["ROUGH_SHIFT"]),
             int(d["ROUGH_OUT_SHIFT"]), int(d["IDLE_ROUGH_100"]),
             int(d["IDLE_INDEX_MAX"])),
            (ROUGH_DEADBAND_RPM, ROUGH_SHIFT, ROUGH_OUT_SHIFT,
             IDLE_ROUGH_100, IDLE_INDEX_MAX))

    def test_the_gate_and_the_settle_rule(self):
        """Proved, not asserted: the gate is the torque rule's two constants."""
        d = _config_defines()
        self.assertEqual(int(d["IDLE_BASE_SHIFT"]), BASE_SHIFT)
        self.assertEqual(int(d["IDLE_TRIP_RPM"]), TRIP_RPM)
        self.assertEqual(int(d["IDLE_SETTLE_MS"]), round(SETTLE_S * 1000))
        self.assertEqual(int(d["STANDSTILL_MMH"]), GATE_SPEED_MMH)
        self.assertEqual(int(d["THROTTLE_REST"]), GATE_THROTTLE)

    def test_the_start(self):
        d = _config_defines()
        self.assertEqual(int(d["START_FIRED_RPM"]), START_FIRED_RPM)
        self.assertEqual(int(d["START_DIP_MS"]), START_DIP_MS)
        self.assertEqual(int(d["START_CRANK_SHIFT"]), START_CRANK_SHIFT)
        self.assertEqual(int(d["HEALTH_UNKNOWN"]), START_INVALID)
        self.assertEqual(int(d["HEALTH_SAT"]), START_SAT)


def _engine(t_ms, rpm):
    q4 = int(rpm * 4)
    return Frame(t_ms, 0x280, bytes([0, 0, q4 & 0xFF, q4 >> 8, 0, 38, 0, 0]))


def _coolant(t_ms, raw):
    return Frame(t_ms, 0x288, bytes([0, raw, 0, 0, 0, 0, 0, 0]))


class TheStart(unittest.TestCase):
    """start_fields(), the oracle for the start detector in src/compute.c."""

    def a_start(self, crank_ms, low, stopped_first=True, clt_raw=80):
        frames = [_coolant(0, clt_raw)]
        t = 10
        if stopped_first:
            frames.append(_engine(t, 0))
            t += 10
        t0 = t
        while t < t0 + crank_ms:
            frames.append(_engine(t, 250))
            t += 10
        frames += [_engine(t, 450), _engine(t + 10, low)]
        t += 20
        for k in range(300):
            frames.append(_engine(t + 10 * k, 900))
        return start_fields(frames)

    def test_a_start_seen_from_rest_is_measured(self):
        crank, dip, clt = self.a_start(832, 331)
        self.assertEqual(crank, 832 >> START_CRANK_SHIFT)
        self.assertEqual(dip, 450 - 331)
        self.assertEqual(clt, 12 + 50)          # raw 80 is 12.00 C

    def test_a_start_not_seen_from_rest_is_not_published(self):
        """The one wrong answer that would be believed: a late crank clock."""
        self.assertEqual(self.a_start(832, 331, stopped_first=False),
                         (START_INVALID, START_INVALID, START_INVALID))

    def test_a_coolant_fault_is_not_a_temperature(self):
        self.assertEqual(self.a_start(832, 331, clt_raw=0xFF)[2], START_INVALID)


class HealthAgainstTheFixtures(unittest.TestCase):
    """The twin of test_the_fixtures_grade_exactly_as_the_oracle in
    test/test_compute.c: the same logs, the same numbers. The grade is
    roughness() over the whole log, which is what the firmware computes;
    `replay.py --host-build` checks every other timestamped fixture."""

    WANT = {
        "09_idle_60s_z1.txt":       (72, 255, 255, 255),
        "11_idle_noac_z1.txt":      (31, 255, 255, 255),
        "12_idle_ac_z1.txt":        (19, 255, 255, 255),
        "17_drive_property_z1.txt": (21, 255, 255, 255),
        "18_coldstart_z1.txt":      (85, 38, 141, 66),
        "19_postfix_drive_z1.txt":  (94, 26, 118, 62),
        "24_mafswap_drive_z1.txt":  (54, 27, 0, 77),
    }

    def test_every_log_grades_as_the_firmware_does(self):
        for name, want in self.WANT.items():
            h = health_summary(os.path.join(FIXTURES, name))
            self.assertEqual((h["idle_rough"], h["start_crank"],
                              h["start_dip"], h["start_clt"]), want, name)

    def test_the_two_recorded_cold_starts_are_the_ones_in_the_docs(self):
        """1.24 s against 0.83 s of cranking, 140 against 118 rpm lost: the
        numbers docs/engine-health/open.md (S7) quotes, to the resolution of the byte."""
        cold = health_summary(os.path.join(FIXTURES, "18_coldstart_z1.txt"))
        fixed = health_summary(os.path.join(FIXTURES, "19_postfix_drive_z1.txt"))
        self.assertAlmostEqual(cold["start_crank"] * 0.032, 1.24, delta=0.032)
        self.assertAlmostEqual(fixed["start_crank"] * 0.032, 0.83, delta=0.032)
        self.assertAlmostEqual(cold["start_dip"], 140, delta=1)
        self.assertEqual(fixed["start_dip"], 118)
