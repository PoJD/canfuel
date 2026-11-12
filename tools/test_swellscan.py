#!/usr/bin/env python3
"""Tests for swellscan.py -- cylinder 3's swell and the common part.

Synthetic rows hold the rules: what counts as a fall, how its length is
read, a correlation within a stop with each stop's mean taken out. One real
capture, `49` (12/11/2026), holds what docs/engine-health/open.md reads off
it: the swell after the hot drive, its one fall with no cut, the floor after
it, and a common part that is the same in both.
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import math
import os
import unittest

import swellscan
from swellscan import (FALL_FROM, corr, fall_seconds, find_falls, mean_in,
                       warm_off, within)
from idledips import FIXTURES


def row(d3, oil=100.0, ac=0.0):
    return {"d3": d3, "oil": oil, "ac": ac}


class Falls(unittest.TestCase):

    def test_a_swell_that_ends_is_one_fall_from_its_deepest_window(self):
        rows = [row(d) for d in (-13, -16, -19, -22, -23, -18, -8, -7, -8)]
        self.assertEqual(find_falls(rows), [(4, 6)])

    def test_a_shallow_deficit_or_a_small_rise_is_no_fall(self):
        self.assertEqual(find_falls([row(d) for d in (-12, -14, -5, -4)]), [])
        self.assertEqual(find_falls([row(d) for d in (-20, -19, -17, -15, -14)]), [])
        self.assertLess(-14, FALL_FROM + 8)

    def test_a_cut_or_the_air_conditioning_between_is_no_fall(self):
        self.assertEqual(find_falls([row(-22), None, row(-9), row(-9)]), [])
        self.assertEqual(find_falls([row(-22), row(-9, ac=1.0), row(-9, ac=1.0)]), [])
        self.assertEqual(find_falls([row(-22, oil=60.0), row(-9, oil=60.0)]), [])

    def test_two_swells_are_two_falls(self):
        rows = [row(d) for d in (-20, -22, -8, -7, -12, -17, -21, -9, -8)]
        self.assertEqual(find_falls(rows), [(1, 2), (6, 7)])

    def test_the_falls_length_runs_to_where_it_stays(self):
        # down in two stages: the relapse in the middle belongs to the fall
        d = [-22] * 10 + [-16, -10, -10, -13, -13, -9, -7] + [-6] * 10
        series = [(4.0 * k, v) for k, v in enumerate(d)]
        self.assertEqual(fall_seconds(series), 4.0 * (15 - 9))

    def test_a_level_series_has_no_length(self):
        self.assertIsNone(fall_seconds([(4.0 * k, -9.0) for k in range(20)]))
        self.assertIsNone(fall_seconds([(0.0, -20.0), (4.0, -8.0)]))


class Numbers(unittest.TestCase):

    def test_mean_in_takes_the_half_open_interval(self):
        pairs = [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0)]
        self.assertEqual(mean_in(pairs, 0.0, 2.0), 2.0)
        self.assertTrue(math.isnan(mean_in(pairs, 5.0, 6.0)))

    def test_corr_skips_what_is_not_a_number(self):
        x = list(range(10)) + [math.nan]
        y = [2 * v + 1 for v in range(10)] + [5.0]
        r, n = corr(x, y)
        self.assertAlmostEqual(r, 1.0)
        self.assertEqual(n, 10)
        self.assertTrue(math.isnan(corr([1, 2], [1, 2])[0]))

    def test_within_takes_each_stops_own_mean_out(self):
        # between the two stops x and y rise together; inside each they
        # run against each other
        a = [{"x": 1.0 + k, "y": 10.0 - k} for k in range(5)]
        b = [{"x": 101.0 + k, "y": 110.0 - k} for k in range(5)]
        flat = a + b
        self.assertGreater(corr([r["x"] for r in flat], [r["y"] for r in flat])[0], 0.9)
        r, _ = corr(within([a, b], "x"), within([a, b], "y"))
        self.assertAlmostEqual(r, -1.0)

    def test_a_window_with_no_oil_reading_is_not_warm(self):
        self.assertFalse(warm_off(None))
        self.assertFalse(warm_off(row(-9, oil=math.nan)))
        self.assertTrue(warm_off(row(-9)))


class TheStopOfTwelveEleven(unittest.TestCase):
    """`49`: 18 minutes standing after a hot drive, no cut, the A/C off."""

    @classmethod
    def setUpClass(cls):
        cls.cap = swellscan.Capture(os.path.join(FIXTURES, "49_warm_drive_z1.txt"))
        st = swellscan.stops(cls.cap)
        cls.idle, cls.rows = max(st, key=lambda x: len(x[1]))

    def test_the_stop_is_read_whole(self):
        self.assertGreaterEqual(len(self.rows), 34)
        self.assertTrue(all(warm_off(r) for r in self.rows))
        self.assertGreater(self.rows[0]["high"], 300.0)

    def test_one_fall_from_the_swell_to_the_floor(self):
        falls = find_falls(self.rows)
        self.assertEqual(len(falls), 1)
        i, j = falls[0]
        self.assertLess(self.rows[i]["d3"], -20.0)
        self.assertGreater(self.rows[j]["d3"], -10.0)
        self.assertLess(self.rows[i]["into"], 240.0)

    def test_the_fall_takes_tens_of_seconds(self):
        i, j = find_falls(self.rows)[0]
        series = swellscan.fine(self.cap, self.idle,
                                self.rows[i]["t"] - swellscan.FINE_BEFORE_S,
                                self.rows[j]["t"] + swellscan.FINE_AFTER_S)
        secs = fall_seconds(series)
        self.assertIsNotNone(secs)
        self.assertGreaterEqual(secs, 15.0)
        self.assertLessEqual(secs, 60.0)

    def test_the_floor_holds_and_the_common_part_does_not_follow(self):
        _, j = find_falls(self.rows)[0]
        swell, floor = self.rows[:j - 1], self.rows[j + 1:]
        self.assertTrue(all(-10.0 < r["d3"] < -3.0 for r in floor))
        mean = lambda rs: sum(r["common"] for r in rs) / len(rs)  # noqa: E731
        self.assertLess(abs(mean(swell) - mean(floor)), 0.4)
        self.assertTrue(2.5 < mean(floor) < 3.4)


if __name__ == "__main__":
    unittest.main()
