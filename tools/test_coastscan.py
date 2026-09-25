#!/usr/bin/env python3
"""Tests for coastscan.py.

Three facts about the corpus are asserted hard, because
docs/engine-health-refuted.md C1 argues from them:

* the ECU does shut the injectors on the overrun -- four times in the one
  fixture that contains real driving
* it shuts them about 1.2 s after the pedal comes up, not immediately
* fuel comes back near 1,700 rpm

The bands are asserted as bands rather than as the exact figures. They are
what the tool is for, so tightening them to the printed number would make
re-running this against a new capture a test change.
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import glob
import os
import unittest

from coastscan import (COAST_MIN_MMH, COAST_MIN_RPM, CUT_UL_PER_REV, FIXTURES,
                       IDLE_UL_PER_REV, THROTTLE_REST, charges, coasting,
                       coolant, cut, ratio_drift, samples, windows)


def row(t, rpm, speed_mmh, d_ul=0, throttle=THROTTLE_REST, coolant_c=90.0):
    return (t, rpm, throttle, speed_mmh, d_ul, coolant_c)


def ramp(n, rpm0, rpm1, ratio, ul_per_rev=0.0, t0=0.0, dt=0.05, coolant_c=90.0):
    """n samples sweeping rpm at a fixed rpm-per-km/h ratio and a fixed charge."""
    out = []
    for i in range(n):
        rpm = rpm0 + (rpm1 - rpm0) * i / max(n - 1, 1)
        d = ul_per_rev * (rpm / 60.0) * dt
        out.append(row(t0 + i * dt, rpm, int(rpm / ratio * 1000), d,
                       coolant_c=coolant_c))
    return out


class Gate(unittest.TestCase):
    def test_a_standing_car_is_not_coasting(self):
        self.assertFalse(coasting(row(0.0, 3000, 0)))

    def test_walking_pace_is_not_coasting(self):
        self.assertFalse(coasting(row(0.0, 3000, COAST_MIN_MMH - 1)))

    def test_a_pressed_pedal_is_not_coasting(self):
        self.assertFalse(coasting(row(0.0, 3000, 30000, throttle=100)))

    def test_an_engine_back_at_the_governor_is_not_coasting(self):
        self.assertFalse(coasting(row(0.0, COAST_MIN_RPM - 1, 30000)))

    def test_rolling_with_the_pedal_at_rest_is(self):
        self.assertTrue(coasting(row(0.0, 3000, 30000)))


class Windows(unittest.TestCase):
    def test_the_pedal_going_down_splits_a_window(self):
        rows = (ramp(40, 4000, 3000, 160)
                + [row(2.0, 3000, 30000, throttle=200)]
                + ramp(40, 4000, 3000, 160, t0=3.0))
        self.assertEqual(len(windows(rows)), 2)

    def test_a_window_too_short_to_hold_a_cut_is_dropped(self):
        self.assertEqual(windows(ramp(5, 4000, 3900, 160, dt=0.02)), [])


class Cut(unittest.TestCase):
    def test_a_window_that_never_stops_fuelling_has_no_cut(self):
        self.assertIsNone(cut(ramp(40, 4000, 3000, 160, ul_per_rev=11.0)))

    def test_a_dry_stretch_is_found_and_bounded(self):
        win = (ramp(20, 4000, 3500, 160, ul_per_rev=11.0)
               + ramp(20, 3500, 2500, 160, ul_per_rev=0.0, t0=1.0))
        c = cut(win)
        self.assertIsNotNone(c)
        self.assertAlmostEqual(c[0][1], 3500, delta=60)
        self.assertAlmostEqual(c[-1][1], 2500, delta=60)

    def test_a_dry_stretch_too_short_to_be_a_strategy_is_not_a_cut(self):
        win = (ramp(30, 4000, 3500, 160, ul_per_rev=11.0)
               + ramp(3, 3500, 3400, 160, ul_per_rev=0.0, t0=1.5)
               + ramp(30, 3400, 2500, 160, ul_per_rev=11.0, t0=1.7))
        self.assertIsNone(cut(win))


class PerRevolution(unittest.TestCase):
    def test_the_same_charge_at_twice_the_speed_reads_the_same(self):
        slow = charges(ramp(20, 2000, 2000, 160, ul_per_rev=8.0))[1:]
        fast = charges(ramp(20, 4000, 4000, 160, ul_per_rev=8.0))[1:]
        for a, b in zip(slow, fast):
            self.assertAlmostEqual(a, b, places=6)
            self.assertAlmostEqual(a, 8.0, places=6)

    def test_idle_is_well_clear_of_the_cut_threshold(self):
        self.assertGreater(IDLE_UL_PER_REV, CUT_UL_PER_REV * 10)


class Coolant(unittest.TestCase):
    def test_a_window_reports_the_coolant_it_started_at(self):
        self.assertEqual(coolant(ramp(20, 4000, 3000, 160, coolant_c=42.0)), 42.0)

    def test_a_capture_without_0x288_says_so_rather_than_guessing(self):
        win = [row(i * 0.05, 3000, 30000, coolant_c=None) for i in range(20)]
        self.assertIsNone(coolant(win))

    def test_the_fixture_coasts_are_all_on_a_fully_warm_engine(self):
        """Which is why the cold coasts had to be driven for, in 19 and 24."""
        rows = samples(os.path.join(FIXTURES, "17_drive_property_z1.txt"))
        temps = [coolant(w) for w in windows(rows) if cut(w) is not None]
        self.assertTrue(temps and min(temps) > 95.0)


class Ratio(unittest.TestCase):
    def test_a_held_ratio_reads_near_zero(self):
        self.assertLess(ratio_drift(ramp(40, 5000, 3000, 160)), 0.01)

    def test_a_clutch_coming_in_shows_up(self):
        win = ramp(20, 5000, 4000, 160) + ramp(20, 4000, 3000, 120, t0=1.0)
        self.assertGreater(ratio_drift(win), 0.2)


class AgainstTheFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cuts = []
        cls.per_log = {}
        for p in sorted(glob.glob(os.path.join(FIXTURES, "*.txt"))):
            for w in windows(samples(p)):
                c = cut(w)
                if c is not None:
                    cls.cuts.append((w, c))
                    name = os.path.basename(p)
                    cls.per_log[name] = cls.per_log.get(name, 0) + 1

    def test_a_log_without_timestamps_is_skipped_rather_than_guessed_at(self):
        self.assertEqual(samples(os.path.join(FIXTURES, "03_drive.txt")), [])

    def test_the_corpus_holds_109_overrun_fuel_cuts(self):
        """Four in 17_drive_property_z1, 72 in the hour of 19, 33 in 24.

        Counted per log, so a change to the detector shows where it moved
        rather than only that the total did.
        """
        self.assertEqual(len(self.cuts), 109)
        self.assertEqual(self.per_log, {"17_drive_property_z1.txt": 4,
                                        "19_postfix_drive_z1.txt": 72,
                                        "24_mafswap_drive_z1.txt": 33})

    def test_the_cut_does_not_engage_the_moment_the_pedal_comes_up(self):
        """0.77-4.27 s after the lift across the corpus, never at once.

        17's four sat at 1.2-1.3 s, which once read as a fixed delay; the
        drives show it is not one, and the shortest is still most of a second.
        That is why a one-second coast shows nothing.
        """
        delays = [c[0][0] - w[0][0] for w, c in self.cuts]
        self.assertGreater(min(delays), 0.7)
        self.assertLess(max(delays), 4.5)

    def test_fuel_comes_back_well_above_idle(self):
        """1,380-3,500 rpm across the corpus, and never near idle.

        There is no single resume speed: it moves with gear and road speed, so
        17's 1,700-1,754 in first gear was one corner of a range and not the
        rule. The floor is still far above the ~800 rpm idle.
        """
        back = [c[-1][1] for _, c in self.cuts]
        self.assertGreater(min(back), 1300)
        self.assertLess(max(back), 3600)

    def test_a_log_where_the_car_never_moves_has_no_coasts_at_all(self):
        cold = samples(os.path.join(FIXTURES, "18_coldstart_z1.txt"))
        self.assertEqual(windows(cold), [],
                         "the cold cut is the open question, not a fixture")


if __name__ == "__main__":
    unittest.main()
