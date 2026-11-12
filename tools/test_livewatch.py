#!/usr/bin/env python3
"""Tests for livewatch.py: the standstill it finds, and the line it prints."""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import os
import unittest

import idledips
from livewatch import STANDSTILL_MMH, fmt, status, stop_start

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        os.pardir, "test", "fixtures")


def g(t, rpm, speed_mmh):
    return (t, int(rpm * 4), 0, speed_mmh)


class StopStart(unittest.TestCase):
    def test_moving_at_the_end_is_no_stop(self):
        self.assertIsNone(stop_start([g(0, 800, 0), g(1, 1500, 20000)]))

    def test_the_last_standstill_counts_not_the_first(self):
        gated = [g(0, 800, 0), g(1, 1500, 20000), g(2, 800, 5), g(3, 800, 5)]
        self.assertEqual(stop_start(gated), 2)

    def test_the_rest_reading_of_0x1A0_is_standing(self):
        self.assertLessEqual(5, STANDSTILL_MMH)
        self.assertEqual(stop_start([g(0, 800, 5)]), 0)

    def test_engine_off_is_no_stop(self):
        self.assertIsNone(stop_start([g(0, 800, 0), g(1, 0, 0)]))


class OnARealStop(unittest.TestCase):
    """47 ends on a warm stop in the everyday state, engine running."""

    def test_the_figures_are_idledips_own(self):
        path = os.path.join(FIXTURES, "47_relearn_drive_z1.txt")
        rpm, oil, clt, gated = idledips.series(path)
        s = status(rpm, oil, clt, gated)
        self.assertIsNotNone(s["stop_s"])
        self.assertGreater(s["stop_s"], 60)
        t0 = gated[-1][0] - s["stop_s"]
        mean, _, _, _ = idledips.roughness(gated, t_from=max(t0, gated[-1][0] - 60))
        self.assertAlmostEqual(s["idle_health"], mean * 50.0)
        _, total, _ = idledips.misfires(gated, t_from=t0)
        self.assertEqual(s["misf_total"], total)
        line = fmt(s, "12:00:00")
        self.assertIn("standing", line)
        self.assertIn("IdleHealth", line)


if __name__ == "__main__":
    unittest.main()
