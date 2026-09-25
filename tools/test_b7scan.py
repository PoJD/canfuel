#!/usr/bin/env python3
"""Tests for b7scan.py.

The fixture assertions are deliberately loose where the exact figure is the
thing the tool is for -- a band rather than a count, so that re-running this
against a new capture is not a test change. Three things are asserted hard,
because docs/firmware/frames.md argues from them:

* cranking is excluded from the driving maximum
* every wide-open-throttle burst in the fixtures ended with b7 still rising
* b7 moves in steps of two
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import os
import unittest

from b7scan import (FIXTURES, GATE_THROTTLE, bursts, driving, ladder, peak,
                    samples, steps, still_rising)


def row(t, rpm, throttle, b7, speed_mmh):
    return (t, rpm, throttle, 0, b7, speed_mmh)


class Gate(unittest.TestCase):
    def test_a_standing_engine_is_not_driving(self):
        rows = [row(0.0, 800, 100, 200, 0)]
        self.assertEqual(driving(rows), [])

    def test_a_closed_throttle_is_not_driving(self):
        rows = [row(0.0, 3000, GATE_THROTTLE, 200, 5000)]
        self.assertEqual(driving(rows), [])

    def test_the_peak_is_taken_over_driving_samples_only(self):
        rows = [row(0.0, 300, GATE_THROTTLE, 250, 0),      # cranking
                row(1.0, 3000, 200, 150, 5000)]            # a pull
        self.assertEqual(peak(rows)[4], 150)

    def test_a_log_with_no_driving_has_no_peak(self):
        self.assertIsNone(peak([row(0.0, 800, GATE_THROTTLE, 30, 0)]))


class Bursts(unittest.TestCase):
    def series(self, b7s, t0=0.0):
        return [row(t0 + i * 0.01, 4000, 200, v, 5000)
                for i, v in enumerate(b7s)]

    def test_a_gap_splits_a_burst(self):
        rows = self.series([100] * 20) + self.series([100] * 20, t0 = 10.0)
        self.assertEqual(len(bursts(rows)), 2)

    def test_a_pull_that_ends_at_its_maximum_is_still_rising(self):
        self.assertTrue(still_rising(self.series(list(range(100, 140)))))

    def test_a_pull_that_peaked_early_is_not(self):
        self.assertFalse(still_rising(self.series(
            list(range(100, 140)) + list(range(140, 100, -1)))))

    def test_too_few_samples_answers_nothing(self):
        self.assertIsNone(still_rising(self.series([100, 101, 102])))


class AgainstTheFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.drive = samples(os.path.join(FIXTURES, "17_drive_property_z1.txt"))

    def test_the_largest_b7_ever_recorded_is_during_cranking(self):
        """192 is in the logs and it is not a torque this engine made."""
        cold = samples(os.path.join(FIXTURES, "18_coldstart_z1.txt"))
        self.assertEqual(max(r[4] for r in cold), 192)
        self.assertIsNone(peak(cold), "cranking must not reach the maximum")

    def test_the_largest_b7_under_load_is_well_short_of_full_scale(self):
        top = peak(self.drive)
        self.assertGreater(top[4], 150)
        self.assertLess(top[4], 200, "b7 has never been seen near 255")

    def test_every_wide_open_burst_ended_before_b7_stopped_rising(self):
        bs = bursts(self.drive)
        self.assertGreaterEqual(len(bs), 3)
        for b in bs:
            self.assertTrue(still_rising(b),
                            "a pull that ran out gives a maximum of the gear, "
                            "not of the engine")

    def test_b7_moves_in_steps_of_two(self):
        gaps = steps(ladder([os.path.join(FIXTURES, "17_drive_property_z1.txt"),
                             os.path.join(FIXTURES, "18_coldstart_z1.txt")]))
        twos = gaps.get(2, 0)
        self.assertGreater(twos, sum(v for k, v in gaps.items() if k != 2) * 5,
                           "one step is ~0.8 %% of full scale, not 0.39 %%")


if __name__ == "__main__":
    unittest.main()
