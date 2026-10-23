#!/usr/bin/env python3
"""Tests for afterpull.py -- the warm idle after high revs.

What is held:

- a stretch is engine speed above 4000 rpm at any load, and two stretches
  a moment apart are one
- a standing idle is graded on idledips.roughness()'s scale: the same
  dead band, the same settle, the same gate
- on `37`, the one capture with a cleaner in the tank and high revs before
  a stop, the stop after them is found and starts calm -- the reading
  open.md S1 quotes
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import io
import os
import unittest

import afterpull
import idledips
from idledips import FIXTURES


def _drive(rows, dt=0.01):
    """Samples from (seconds, rpm, b7, speed_mmh, throttle) rows."""
    out, t = [], 0.0
    for secs, rpm, b7, spd, thr in rows:
        for _ in range(int(round(secs / dt))):
            out.append((t, int(rpm * 4), thr, spd, b7, 100.0))
            t += dt
    return out


class PullsTest(unittest.TestCase):
    def test_speed_with_a_light_foot_counts(self):
        smp = _drive([(2, 4300, 60, 80000, 80), (1, 800, 20, 0, 35)])
        self.assertEqual(len(afterpull.pulls(smp)), 1)

    def test_load_without_speed_is_not_one(self):
        smp = _drive([(2, 3000, 190, 80000, 200), (1, 800, 20, 0, 35)])
        self.assertEqual(afterpull.pulls(smp), [])

    def test_a_short_gap_is_one_pull(self):
        smp = _drive([(2, 5000, 190, 80000, 200), (0.5, 3500, 190, 80000, 200),
                      (3, 5200, 190, 80000, 200), (1, 800, 20, 0, 35)])
        p = afterpull.pulls(smp)
        self.assertEqual(len(p), 1)
        self.assertAlmostEqual(p[0][2], 5.0, delta=0.05)

    def test_a_long_gap_is_two(self):
        smp = _drive([(2, 5000, 190, 80000, 200), (5, 3500, 120, 80000, 200),
                      (2, 5000, 190, 80000, 200), (1, 800, 20, 0, 35)])
        self.assertEqual(len(afterpull.pulls(smp)), 2)


class IdleTest(unittest.TestCase):
    def test_grade_matches_roughness(self):
        # A sawtooth idle: steps of 8 rpm, i.e. 5 after the 3 rpm dead band.
        smp, t = [], 0.0
        for k in range(6000):
            r = 800 if k % 2 else 808
            smp.append((t, r * 4, 35, 0, 22, 100.0))
            t += 0.0106
        runs = afterpull.idle_runs(smp)
        self.assertEqual(len(runs), 1)
        g = afterpull.grade(runs[0]["steps"], 0)
        gated = [(a, b, c, d) for a, b, c, d, _, _ in smp]
        mean_rpm = idledips.roughness(gated)[0]
        self.assertAlmostEqual(g, mean_rpm * 50, places=6)
        self.assertAlmostEqual(g, 250.0, places=6)

    def test_moving_ends_an_idle(self):
        smp = _drive([(10, 800, 22, 0, 35), (5, 2000, 80, 30000, 120),
                      (10, 800, 22, 0, 35)])
        self.assertEqual(len(afterpull.idle_runs(smp)), 2)

    def test_too_few_steps_is_not_a_reading(self):
        self.assertIsNone(afterpull.grade([(0.1, 4)] * 10, 0, 15))


class CaptureTest(unittest.TestCase):
    def test_37_starts_calm_after_high_revs(self):
        out = io.StringIO()
        rows = afterpull.report(os.path.join(FIXTURES, "37_item5_drive3_z1.txt"),
                                out=out)
        self.assertGreaterEqual(rows, 2)
        first = out.getvalue().splitlines()[0].split("|")
        bins = first[2].split()
        self.assertLess(int(bins[1]), 50)                      # 15-30 s
        self.assertGreater(int(bins[2]), int(bins[1]))         # then up


if __name__ == "__main__":
    unittest.main()
