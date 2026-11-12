#!/usr/bin/env python3
"""Tests for cylscan.py -- every stroke of an idle put to its cylinder.

Synthetic streams hold the three rules the reading rests on: the stroke
count does not slip across held values and missing frames, the crank
wheel's alternation is taken out, and a stroke's loss is gathered back from
the slot before its own. Two real captures hold what the corpus is read by:
the injector cut names cylinder 4 where the strongest slot named cylinder 2,
group 014's rises fall on cylinder 3, and the overrun shows the wheel.
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import os
import unittest

import cylscan
from cylscan import (FIRING_ORDER, OWN_SHARE, STROKE_RPM, WHEEL_ALT, Run,
                     deviation, invert, track, weak)
from idledips import FIXTURES

FRAME_S = 0.01065


def stream(stroke_rpm, drop_every=0):
    """0x280 samples (t, rpm, throttle, speed) for a list of per-stroke
    speeds: each value is reported from the end of its stroke on, on the
    frame grid, some frames lost."""
    edges, t = [], 0.0
    for r in stroke_rpm:
        t += 30.0 / r
        edges.append(t)
    out, k, n = [], 0, 0
    t = edges[0]
    while t < edges[-1]:
        while k + 1 < len(edges) and edges[k + 1] <= t:
            k += 1
        n += 1
        if not (drop_every and n % drop_every == 0):
            out.append((t, stroke_rpm[k], 35, 0))
        t += FRAME_S
    return out


def pattern_run(p, strokes=2000, rpm=800.0):
    """A Run whose steps repeat p (in firing order from cylinder 2's slot:
    2, 1, 3, 4) around `rpm`."""
    level, ev = rpm, []
    for k in range(strokes):
        level += p[k % 4]
        if k % 4 == 3:
            level = rpm          # p sums to nothing; keep rounding out
        ev.append((k * 30.0 / rpm, level, k))
    return Run(ev)


class Counting(unittest.TestCase):

    def test_no_slip_across_held_values_and_lost_frames(self):
        # a period-4 pattern, two neighbours equal now and then (a held
        # value), one frame in 17 lost
        base = [800.0, 812.0, 790.0, 778.0]
        rpm = []
        for k in range(4000):
            v = base[k % 4] + (k * 7 % 5) * 0.25
            if k % 53 == 20:
                v = rpm[-1]
            rpm.append(v)
        ev = track(stream(rpm, drop_every=17), 0, None)
        self.assertGreater(len(ev), 3500)
        # the value of stroke k is base[k % 4] and a little: every event's
        # index has to sit on the slot its value came from
        first = ev[0][2]
        slot_of = {}
        for _, r, k in ev:
            q = min(range(4), key=lambda j: abs(base[j] + 0.5 - r))
            slot_of.setdefault((k - first) % 4, []).append(q)
        for q, seen in slot_of.items():
            top = max(set(seen), key=seen.count)
            self.assertGreater(seen.count(top) / len(seen), 0.97)
        self.assertEqual(len({max(set(s), key=s.count)
                              for s in slot_of.values()}), 4)

    def test_invert_undoes_the_spread(self):
        d = [3.0, -5.0, 0.5, 1.5]
        p = [OWN_SHARE * d[k] + (1 - OWN_SHARE) * d[(k + 1) % 4] for k in range(4)]
        for got, want in zip(invert(p), d):
            self.assertAlmostEqual(got, want, places=9)


class Deviation(unittest.TestCase):

    def steps(self, d, rpm=800.0):
        """Steps in slot order 2, 1, 3, 4 for deviations d by cylinder, the
        wheel's alternation added."""
        alt = WHEEL_ALT * rpm
        wheel = {1: -alt, 3: alt, 4: -alt, 2: alt}
        order = (2, 1, 3, 4)
        return [OWN_SHARE * d[c] + (1 - OWN_SHARE) * d[order[(i + 1) % 4]]
                + wheel[c] for i, c in enumerate(order)]

    def test_the_wheel_is_taken_out(self):
        # 1 and 4 level with the mean: the raw steps put both 1.7 rpm under
        d = {1: 0.0, 3: -2.0, 4: 0.0, 2: 2.0}
        run = pattern_run(self.steps(d))
        self.assertTrue(run.named)
        got = deviation(run)
        for c in FIRING_ORDER:
            self.assertAlmostEqual(got[c], 100.0 * d[c] / STROKE_RPM, delta=0.4)

    def test_the_wheel_alone_names_nothing(self):
        # four equal cylinders: slots 2 and 3 are both the strongest
        run = pattern_run(self.steps({1: 0.0, 3: 0.0, 4: 0.0, 2: 0.0}))
        self.assertFalse(run.named)

    def test_a_weak_three_is_not_read_as_a_weak_four(self):
        # `46`'s shape: 3 gives 10 % less, 4 hardly less, 2 and 1 more
        d = {1: 1.2, 3: -3.5, 4: -0.9, 2: 3.2}
        run = pattern_run(self.steps(d))
        got = deviation(run)
        self.assertAlmostEqual(got[3], -10.3, delta=0.5)
        self.assertAlmostEqual(got[4], -2.6, delta=0.5)
        # without the wheel taken out the same steps would put 4 below 3:
        # that is the reading this tool replaces
        raw = dict(zip((2, 1, 3, 4), self.steps(d)))
        self.assertLess(raw[4], raw[3])

    def test_a_weak_stroke_is_put_to_its_own_cylinder(self):
        d = {1: 0.0, 3: -1.0, 4: 0.0, 2: 1.0}
        p = self.steps(d)
        level, ev = 800.0, []
        for k in range(4000):
            level += p[k % 4]
            if k % 4 == 3:
                level = 800.0
            r = level
            if k % 400 == 202:              # cylinder 3's slot (2, 1, 3, 4)
                r = level - 20.0
            ev.append((k * 0.0375, r, k))
        run = Run(ev)
        w, n = weak(run)
        self.assertEqual(w[3], 10)
        self.assertEqual(w[1] + w[2] + w[4], 0)


class Corpus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cold = cylscan.read(os.path.join(FIXTURES, "41_item6d_cold_cut_z1.txt"))
        cls.runs = cylscan.idle_runs(cls.cold)

    def test_one_run_holds_the_whole_idle_and_the_cut_names_four(self):
        run = max(self.runs, key=len)
        self.assertGreater(run.T[-1] - run.T[1], 600.0)
        self.assertTrue(run.named)
        # named by its strongest slot being cylinder 2; the cut was on 4
        self.assertEqual(cylscan.cut_cylinder(run), 4)

    def test_cylinder_three_gives_the_least_and_has_the_weak_strokes(self):
        run = max(self.runs, key=len)
        d = deviation(run)
        self.assertLess(d[3], -10.0)
        self.assertEqual(min(d, key=d.get), 3)
        w, _ = weak(run)
        self.assertGreater(w[3], w[1] + w[2] + w[4] - 1)

    def test_what_014_counted_was_cylinder_three(self):
        got = cylscan.misfires_014(
            os.path.join(FIXTURES, "vcds", "vcds-step6d-cold-cut-014-001-003.csv"),
            self.cold, self.runs)
        self.assertGreater(len(got), 40)
        on3 = sum(1 for x in got if x[1] == 3)
        self.assertGreater(on3 / len(got), 0.65)

    def test_the_wheel_alternates_where_nothing_burns(self):
        data = cylscan.read(os.path.join(FIXTURES, "43_stockmap_drive2_z1.txt"))
        rows = cylscan.wheel_windows(data)
        self.assertGreaterEqual(len(rows), 10)
        rel = sorted(a / r for r, a in rows)
        self.assertAlmostEqual(rel[len(rel) // 2], WHEEL_ALT, delta=0.0002)

    def test_the_wheel_reads_two_and_three_high_and_nothing_else(self):
        data = cylscan.read(os.path.join(FIXTURES, "37_item5_drive3_z1.txt"))
        got, linked = cylscan.wheel_named(data)
        self.assertGreaterEqual(linked, 1)
        for c, sign in ((1, -1), (3, 1), (4, -1), (2, 1)):
            mean = sum(got[c]) / len(got[c])
            self.assertAlmostEqual(mean, sign * WHEEL_ALT, delta=0.0004)


if __name__ == "__main__":
    unittest.main()
