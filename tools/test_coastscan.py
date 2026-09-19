#!/usr/bin/env python3
"""Tests for coastscan.py.

The gear test is what the tool is for, so it is what is tested hardest: a
gearchange and a clutch-in coast look exactly like an in-gear overrun on every
other channel, and counting them as one would answer the question wrongly in
the reassuring direction.

Two facts about the corpus are asserted hard, because docs/engine-health.md
argues from them:

* eighteen recordings contain exactly ONE in-gear coast, and it lasts 1.3 s
* the ECU is still injecting through it
"""

from __future__ import annotations

import glob
import os
import unittest

from coastscan import (COAST_MIN_MMH, COAST_MIN_RPM, CUT_UL_PER_REV, FIXTURES,
                       IDLE_UL_PER_REV, THROTTLE_REST, coasting, in_gear,
                       ratio_drift, rate_ul_s, samples, ul_per_rev, windows)


def row(t, rpm, speed_mmh, d_ul=0, throttle=THROTTLE_REST):
    return (t, rpm, throttle, speed_mmh, d_ul)


def ramp(n, rpm0, rpm1, ratio, d_ul=0, t0=0.0, dt=0.01):
    """A window of n samples sweeping rpm at a FIXED rpm-per-km/h ratio."""
    out = []
    for i in range(n):
        rpm = rpm0 + (rpm1 - rpm0) * i / max(n - 1, 1)
        out.append(row(t0 + i * dt, rpm, int(rpm / ratio * 1000), d_ul))
    return out


class Gate(unittest.TestCase):
    def test_a_standing_car_is_not_coasting(self):
        self.assertFalse(coasting(row(0.0, 3000, 0)))

    def test_a_crawl_is_not_coasting(self):
        self.assertFalse(coasting(row(0.0, 3000, COAST_MIN_MMH - 1)))

    def test_a_pressed_pedal_is_not_coasting(self):
        self.assertFalse(coasting(row(0.0, 3000, 30000, throttle=100)))

    def test_an_engine_at_the_governor_is_not_coasting(self):
        self.assertFalse(coasting(row(0.0, COAST_MIN_RPM - 1, 30000)))

    def test_moving_with_the_pedal_at_rest_is(self):
        self.assertTrue(coasting(row(0.0, 3000, 30000)))


class Windows(unittest.TestCase):
    def test_a_break_in_the_pedal_splits_a_window(self):
        rows = (ramp(200, 4000, 3000, 160)
                + [row(2.0, 3000, 30000, throttle=200)]
                + ramp(200, 4000, 3000, 160, t0=3.0))
        self.assertEqual(len(windows(rows)), 2)

    def test_a_window_too_short_to_mean_anything_is_dropped(self):
        self.assertEqual(windows(ramp(20, 4000, 3900, 160, dt=0.01)), [])


class Gear(unittest.TestCase):
    def test_a_held_ratio_is_one_gear(self):
        win = ramp(200, 5000, 3000, 160)
        self.assertLess(ratio_drift(win), 0.01)
        self.assertTrue(in_gear(win))

    def test_a_ratio_that_moves_is_a_gearchange_or_a_clutch(self):
        win = ramp(100, 5000, 4000, 160) + ramp(100, 4000, 3000, 120, t0=1.0)
        self.assertGreater(ratio_drift(win), 0.2)
        self.assertFalse(in_gear(win))

    def test_the_fixtures_own_rejected_windows_are_rejected(self):
        """Three of 17's four coasts move the ratio 12-17 %. None is an overrun."""
        rows = samples(os.path.join(FIXTURES, "17_drive_property_z1.txt"))
        rejected = [w for w in windows(rows) if not in_gear(w)]
        self.assertEqual(len(rejected), 3)
        for w in rejected:
            self.assertGreater(ratio_drift(w), 0.1)


class PerRevolution(unittest.TestCase):
    def test_the_same_charge_at_twice_the_speed_reads_the_same(self):
        slow = ramp(200, 2000, 2000, 160, d_ul=10)
        fast = ramp(200, 4000, 4000, 160, d_ul=10)
        self.assertGreater(rate_ul_s(fast), rate_ul_s(slow) * 0.9)
        self.assertAlmostEqual(ul_per_rev(fast), ul_per_rev(slow) / 2, places=3)


class AgainstTheFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.geared = []
        for p in sorted(glob.glob(os.path.join(FIXTURES, "*.txt"))):
            cls.geared += [w for w in windows(samples(p)) if in_gear(w)]

    def test_a_log_without_timestamps_is_skipped_rather_than_guessed_at(self):
        self.assertEqual(samples(os.path.join(FIXTURES, "03_drive.txt")), [])

    def test_the_corpus_holds_exactly_one_in_gear_coast(self):
        """Eighteen recordings of idling, revving and pottering. One."""
        self.assertEqual(len(self.geared), 1)

    def test_and_it_is_over_in_under_two_seconds(self):
        win = self.geared[0]
        self.assertLess(win[-1][0] - win[0][0], 2.0)

    def test_the_ecu_is_still_injecting_through_it(self):
        charge = ul_per_rev(self.geared[0])
        self.assertGreater(charge, CUT_UL_PER_REV * 5,
                           "no fuel cut is visible in the one window there is")
        self.assertLess(charge, IDLE_UL_PER_REV,
                        "it is reduced, which is not the same as cut")


if __name__ == "__main__":
    unittest.main()
