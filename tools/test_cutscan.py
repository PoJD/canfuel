#!/usr/bin/env python3
"""Tests for cutscan.py -- the reading of the injector cut test.

The test has not been run on the car yet, so most of this is synthetic: an
idle built stroke by stroke, a cylinder taken out on a schedule, dips planted
on chosen cylinders. What is held:

- **a real idle with every cylinder firing is never taken for a cut** -- the
  control, on real captures, and the one that matters most: a false cut
  would name a cylinder that was never touched
- the schedule is found, and found in the right order
- the dead stroke itself is never counted as a dip
- dips planted on one cylinder name that cylinder; dips spread over all four
  name nobody
- the p-value is the exact one (two cells: the binomial)
- the rules are plan.md 3.3's, including what "only 1 and 4" cannot say
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import os
import random
import unittest

import cutscan
from cutscan import (find_cuts, firing_dips, max_rate_p, min_rate_p,
                     named_dips, named_verdict, read_vcds, slot_deficit,
                     stroke_runs, verdict)
from idledips import FIXTURES, series

FIRING = (1, 3, 4, 2)        # the firing order: slot i % 4 is FIRING[i % 4]
RATE_HZ = 94.0               # 0x280's frame rate


def synthetic(cuts, dip_cyls=(), dip_p=0.0, seconds=None, rpm=800.0,
              sd=5.0, seed=7):
    """Gated 0x280 samples for an idle, stroke by stroke.

    cuts: [(start_s, end_s, cylinder)] -- that cylinder's strokes 30 rpm low.
    dip_cyls / dip_p: each firing stroke of those cylinders is a 30 rpm dip
    with probability dip_p.
    """
    rnd = random.Random(seed)
    if seconds is None:
        seconds = max(b for _, b, _ in cuts) + 30.0 if cuts else 120.0
    stroke_s = 60.0 / rpm / 2.0
    strokes = []
    t, i = 0.0, 0
    while t < seconds:
        cyl = FIRING[i % 4]
        v = rpm + rnd.gauss(0.0, sd)
        dead = any(a <= t < b and c == cyl for a, b, c in cuts)
        if dead:
            v -= 30.0
        elif isinstance(dip_p, dict):
            if rnd.random() < dip_p.get(cyl, 0.0):
                v -= 30.0
        elif cyl in dip_cyls and rnd.random() < dip_p:
            v -= 30.0
        strokes.append((t, int(round(v * 4))))
        t += stroke_s
        i += 1
    out, j = [], 0
    for k in range(int(seconds * RATE_HZ)):
        ft = k / RATE_HZ
        while j + 1 < len(strokes) and strokes[j + 1][0] <= ft:
            j += 1
        out.append((ft, strokes[j][1], 35, 5))
    return out


SCHEDULE = [(30 + 90 * k, 90 + 90 * k, c)
            for k, c in enumerate((1, 2, 3, 4, 4, 3, 2, 1))]
ORDER = [c for _, _, c in SCHEDULE]


class TheControl(unittest.TestCase):
    """Every cylinder firing must never read as a cut."""

    def test_real_idles_hold_no_cut(self):
        for name in ("30_step2b_z1.txt", "28_sessionA2_warm_z1.txt",
                     "29_sessionB_z1.txt", "24_mafswap_drive_z1.txt"):
            runs = stroke_runs(series(os.path.join(FIXTURES, name))[3])
            self.assertTrue(runs, name)
            self.assertEqual(find_cuts(runs), [], name)

    def test_the_tool_stops_rather_than_guessing(self):
        got = cutscan.main([os.path.join(FIXTURES, "30_step2b_z1.txt")])
        self.assertEqual(got, 1)


class FindingTheCuts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runs = stroke_runs(synthetic(SCHEDULE))

    def test_the_schedule_is_found_in_order(self):
        cuts = find_cuts(self.runs)
        self.assertEqual(len(cuts), len(SCHEDULE))
        # a cut is seen run by run, and a run lasts a few seconds, so an edge
        # can land up to one run late; CUT_SETTLE_S is skipped anyway
        for (a, b), (pa, pb, _) in zip(cuts, SCHEDULE):
            self.assertLess(abs(a - pa), 10.0)
            self.assertLess(abs(b - pb), 10.0)

    def test_the_dead_slot_is_far_below(self):
        inside = [r for r in self.runs if 35 <= r[0][0] < 85]
        self.assertTrue(inside)
        for r in inside:
            self.assertGreater(slot_deficit(r)[1], cutscan.CUT_DEFICIT_RPM)

    def test_the_dead_stroke_is_not_a_dip(self):
        a, b = find_cuts(self.runs)[0]
        events, exposure = firing_dips(self.runs, a + 5, b)
        self.assertGreater(exposure, 500)
        self.assertLessEqual(events, 2)


class NamingTheCylinder(unittest.TestCase):

    def read(self, gated, order=ORDER):
        runs = stroke_runs(gated)
        cuts = find_cuts(runs)
        self.assertEqual(len(cuts), len(order))
        counts, exp = [], []
        for a, b in cuts:
            e, x = firing_dips(runs, a + cutscan.CUT_SETTLE_S, b)
            counts.append(e)
            exp.append(x)
        return verdict(order, counts, exp)[1]

    def test_one_cylinder_carrying_the_dips_is_named(self):
        res = self.read(synthetic(SCHEDULE, dip_cyls=(3,), dip_p=0.012))
        self.assertTrue(res["dips_one"])
        self.assertEqual(res["low"], 3)

    def test_dips_on_all_four_name_nobody(self):
        res = self.read(synthetic(SCHEDULE, dip_cyls=(1, 2, 3, 4), dip_p=0.004))
        self.assertFalse(res["dips_one"])

    def test_only_the_outer_two(self):
        sched = [(30 + 90 * k, 90 + 90 * k, c) for k, c in enumerate((1, 4, 4, 1))]
        res = self.read(synthetic(sched, dip_cyls=(4,), dip_p=0.012),
                        order=[1, 4, 4, 1])
        self.assertTrue(res["dips_one"])
        self.assertEqual(res["low"], 4)


class ByName(unittest.TestCase):
    """While a cylinder is out, the other three have names. The design
    plan.md 3.3 settled on is 1 and 4 only, repeated on separate days."""

    @staticmethod
    def named(gated, order):
        runs = stroke_runs(gated)
        cuts = find_cuts(runs)
        return [named_dips(runs, a + cutscan.CUT_SETTLE_S, b, c)
                for c, (a, b) in zip(order, cuts)], len(cuts)

    def test_cutting_1_names_3_4_and_2(self):
        sched = [(30, 90, 1)]
        named, n = self.named(synthetic(sched, seconds=120), [1])
        self.assertEqual(n, 1)
        self.assertEqual(sorted(named[0]), [2, 3, 4])

    def test_a_dip_prone_middle_cylinder_is_named_by_the_outer_cuts(self):
        order = [1, 4, 4, 1, 1, 4, 4, 1]
        sched = [(30 + 90 * k, 90 + 90 * k, c) for k, c in enumerate(order)]
        named, n = self.named(synthetic(sched, dip_p={3: 0.02}), order)
        self.assertEqual(n, len(order))
        res = named_verdict(order, named)[1]
        self.assertTrue(res["one"])
        self.assertEqual(res["high"], 3)

    def test_an_outer_cylinder_is_named_by_the_other_cut(self):
        order = [1, 4, 4, 1, 1, 4, 4, 1]
        sched = [(30 + 90 * k, 90 + 90 * k, c) for k, c in enumerate(order)]
        named, n = self.named(synthetic(sched, dip_p={1: 0.02}), order)
        res = named_verdict(order, named)[1]
        self.assertTrue(res["one"])
        self.assertEqual(res["high"], 1)

    def test_dips_on_all_four_name_nobody(self):
        order = [1, 4, 4, 1]
        sched = [(30 + 90 * k, 90 + 90 * k, c) for k, c in enumerate(order)]
        named, _ = self.named(synthetic(sched, dip_cyls=(1, 2, 3, 4),
                                        dip_p=0.006, seed=11), order)
        self.assertFalse(named_verdict(order, named)[1]["one"])

    def test_the_max_statistic_mirrors_the_min(self):
        self.assertAlmostEqual(max_rate_p([8, 2], [100, 100]),
                               min_rate_p([8, 2], [100, 100]), places=9)
        self.assertGreater(max_rate_p([10, 10, 10], [100] * 3), 0.99)


class SameSlotPairs(unittest.TestCase):
    """The evidence from ordinary idles: do the dips keep to one slot?"""

    def test_dips_on_one_cylinder_keep_to_one_slot(self):
        m = cutscan.slot_pairs(synthetic([], dip_p={3: 0.02}, seconds=900, seed=4))
        self.assertGreater(m[0] / sum(m), 0.8)

    def test_dips_on_all_four_do_not(self):
        m = [0, 0, 0, 0]
        for seed in (1, 2, 3, 5):
            got = cutscan.slot_pairs(synthetic([], dip_cyls=(1, 2, 3, 4),
                                               dip_p=0.006, seconds=900,
                                               seed=seed))
            m = [x + y for x, y in zip(m, got)]
        self.assertLess(m[0] / sum(m), 0.35)

    def test_the_real_idles_keep_to_one_slot(self):
        """The finding of 9/10/2026 (docs/engine-health/open.md, *The dips
        keep to one slot*). If this fails, that section is wrong."""
        m = [0, 0, 0, 0]
        for name in ("19_postfix_drive_z1.txt", "24_mafswap_drive_z1.txt",
                     "28_sessionA2_warm_z1.txt", "30_step2b_z1.txt"):
            got = cutscan.slot_pairs(series(os.path.join(FIXTURES, name))[3])
            m = [x + y for x, y in zip(m, got)]
        self.assertLess(cutscan.binom_upper(m[0], sum(m), 0.25), 0.001)


class TheStatistics(unittest.TestCase):

    def test_equal_counts_are_unremarkable(self):
        self.assertGreater(min_rate_p([10, 10, 10, 10], [100] * 4), 0.99)

    def test_two_cells_are_the_two_sided_binomial(self):
        from math import comb
        exact = sum(comb(10, k) for k in (0, 1, 2, 8, 9, 10)) / 2 ** 10
        self.assertAlmostEqual(min_rate_p([2, 8], [100, 100]), exact, places=9)

    def test_exposure_is_respected(self):
        # half the strokes and half the dips is no evidence at all
        self.assertGreater(min_rate_p([5, 10, 10, 10], [50, 100, 100, 100]), 0.9)

    def test_nothing_at_all_is_nothing(self):
        self.assertEqual(min_rate_p([0, 0, 0, 0], [100] * 4), 1.0)


class TheRules(unittest.TestCase):
    """plan.md 3.3, rule by rule, on numbers rather than captures."""

    EVEN = ([10] * 8, [1000] * 8)

    def test_a_weak_cylinder_by_air(self):
        air = [4.2, 4.0, 4.2, 4.2, 4.2, 4.2, 4.0, 4.2]   # 2 needs 0.2 less
        lines, res = verdict(ORDER, *self.EVEN, air=air)
        self.assertEqual(res["air_weak"], 2)
        self.assertTrue(any("cylinder 2 is steadily weak" in x for x in lines))

    def test_weak_in_one_round_only_is_not_weak(self):
        air = [4.2, 4.0, 4.2, 4.2, 4.2, 4.2, 4.2, 4.2]
        self.assertIsNone(verdict(ORDER, *self.EVEN, air=air)[1]["air_weak"])

    def test_not_one_cylinder_needs_both_readings(self):
        air = [4.20, 4.22, 4.19, 4.21, 4.20, 4.18, 4.21, 4.20]
        lines, res = verdict(ORDER, *self.EVEN, air=air)
        self.assertTrue(res.get("none"))
        self.assertTrue(any("smaller share is NOT excluded" in x for x in lines))
        lines, res = verdict(ORDER, *self.EVEN, air=None)
        self.assertFalse(res.get("none"))
        self.assertTrue(any("undecided" in x for x in lines))

    def test_the_outer_two_cannot_say_not_one_cylinder(self):
        lines, res = verdict([1, 4, 4, 1], [10] * 4, [1000] * 4,
                             air=[4.2, 4.2, 4.2, 4.2])
        self.assertTrue(any("2 or 3 untested" in x for x in lines))
        self.assertFalse(any("not one cylinder" in x for x in lines))


class TheVcdsLog(unittest.TestCase):

    def test_a_real_log_reads_and_lines_up(self):
        vc = read_vcds(os.path.join(FIXTURES, "vcds",
                                    "vcds-step2b-a3-014-055-003.csv"))
        self.assertIn("003", vc)
        self.assertIn("014", vc)
        rpm = series(os.path.join(FIXTURES, "30_step2b_z1.txt"))[0]
        off = cutscan.align([(t, float(f[0])) for t, f in vc["003"]], rpm)
        # the stop A3 of 9/10 sits about 28 minutes into the capture
        self.assertGreater(off, 1500)
        self.assertLess(off, 1900)


if __name__ == "__main__":
    unittest.main()
