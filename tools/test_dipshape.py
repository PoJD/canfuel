#!/usr/bin/env python3
"""Tests for dipshape.py -- how many weak strokes make one dip.

Synthetic runs hold the counting rules; one real capture holds the two
things that decide which idle is read: the injector cut is left out, and
the oil gate keeps a cold idle out.
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import os
import unittest

import cutscan
import dipshape
from dipshape import dips, follow_on, idle_runs
from idledips import FIXTURES, series

STROKE_S = 60.0 / 800.0 / 2.0


def run_of(values):
    return [(k * STROKE_S, float(v)) for k, v in enumerate(values)]


def flat(n=40, rpm=800.0):
    return [rpm] * n


class Counting(unittest.TestCase):

    def test_one_weak_stroke_is_a_single(self):
        v = flat() + [775.0] * 3 + [785.0, 795.0] + flat(30)
        got = dips(run_of(v))
        self.assertEqual(len(got), 1)
        self.assertEqual(len(got[0]["weak"]), 1)
        self.assertAlmostEqual(got[0]["depth"], 25.0)

    def test_two_weak_strokes_in_a_row_are_one_cluster(self):
        v = flat() + [788.0, 776.0, 776.0, 790.0] + flat(30)
        got = dips(run_of(v))
        self.assertEqual(len(got), 1)
        self.assertEqual(len(got[0]["weak"]), 2)

    def test_one_shallow_stroke_is_no_dip(self):
        v = flat() + [788.0, 788.0, 795.0] + flat(30)
        self.assertEqual(dips(run_of(v)), [])

    def test_a_dip_is_counted_once_until_speed_comes_back(self):
        # down 25, half-way back, down again: one dip, as the firmware's rearm
        v = flat() + [775.0, 785.0, 774.0, 790.0, 795.0] + flat(30)
        self.assertEqual(len(dips(run_of(v))), 1)
        # down 25, all the way back, down again: two
        v = flat() + [775.0, 800.0, 800.0, 775.0, 800.0] + flat(30)
        self.assertEqual(len(dips(run_of(v))), 2)

    def test_a_slow_sag_is_a_dip_of_many_small_steps(self):
        v = flat() + [800.0 - 5.0 * k for k in range(1, 11)] + flat(30, 760.0)
        got = dips(run_of(v))
        self.assertEqual(len(got), 1)
        self.assertLess(got[0]["biggest"], 0.2)


class EachCylinderAgainstItself(unittest.TestCase):

    def test_a_steady_low_slot_makes_no_weak_strokes(self):
        # one slot loses 9 every cycle and the other three win it back
        v, x = [], 800.0
        for k in range(200):
            x += -9.0 if k % 4 == 0 else 3.0
            v.append(x)
        run = run_of(v)
        raw = [d for d in dips(run)]
        _, base_raw, _ = follow_on([run])
        self.assertGreater(base_raw, 0.2)           # raw: one step in four "loses"
        _, base, _ = follow_on([dipshape.slot_level(run)])
        self.assertEqual(base, 0.0)
        self.assertEqual(dips(dipshape.slot_level(run)), raw)  # no dips either way

    def test_a_real_weak_stroke_survives(self):
        v, x = [], 800.0
        for k in range(200):
            x += -9.0 if k % 4 == 0 else 3.0
            if k == 120:
                x -= 25.0
            if 121 <= k <= 128:
                x += 25.0 / 8
            v.append(x)
        got = dips(dipshape.slot_level(run_of(v)))
        self.assertEqual(len(got), 1)
        self.assertEqual(len(got[0]["weak"]), 1)


class TheChanceCheck(unittest.TestCase):

    def test_independent_weak_strokes_follow_at_the_base_rate(self):
        # a weak stroke every 10th, never two together
        v, x = [], 800.0
        for k in range(400):
            x += -10.0 if k % 10 == 0 else (10.0 if k % 10 == 1 else 0.0)
            v.append(x)
        n, base, after = follow_on([run_of(v)])
        self.assertAlmostEqual(base, 0.1, delta=0.01)
        self.assertEqual(after, 0.0)

    def test_paired_weak_strokes_follow_each_other(self):
        v, x = [], 800.0
        for k in range(400):
            x += -10.0 if k % 10 in (0, 1) else (10.0 if k % 10 in (2, 3) else 0.0)
            v.append(x)
        _, base, after = follow_on([run_of(v)])
        self.assertAlmostEqual(after, 0.5, delta=0.02)
        self.assertGreater(after, base)


class WhichIdle(unittest.TestCase):

    PATH = os.path.join(FIXTURES, "43_stockmap_drive2_z1.txt")

    def test_the_injector_cut_is_left_out(self):
        gated = series(self.PATH)[3]
        cuts = cutscan.find_cuts(cutscan.stroke_runs(gated))
        self.assertEqual(len(cuts), 1)
        a, b = cuts[0]
        runs = idle_runs(self.PATH)
        self.assertTrue(runs)
        for r in runs:
            for t, _ in r:
                self.assertFalse(a - dipshape.CUT_MARGIN_S <= t
                                 <= b + dipshape.CUT_MARGIN_S)

    def test_the_oil_gate_keeps_a_cold_idle_out(self):
        self.assertEqual(idle_runs(self.PATH, min_oil=200.0), [])
        self.assertGreater(sum(map(len, idle_runs(self.PATH, min_oil=0))),
                           sum(map(len, idle_runs(self.PATH))))


if __name__ == "__main__":
    unittest.main()
