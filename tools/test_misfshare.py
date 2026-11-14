#!/usr/bin/env python3
"""Tests for misfshare.py -- 014 at a standing idle, log by log.

Synthetic samples hold the rules: what counts as idle, a rise as misfires,
an episode and its climb, a silence and what breaks it. One real log, the
warm stop of 12/11/2026 on the canister, holds what docs/engine-health/
open.md reads off it: one misfire and the longest silence on record.
"""

from __future__ import annotations

import math
import os
import unittest

import misfshare
from misfshare import share
from idledips import FIXTURES

VCDS = os.path.join(FIXTURES, "vcds")


def pts(counts, rpm=800.0, load=20.0, active=True, dt=1.0):
    return [(k * dt, rpm, load, float(c), active) for k, c in enumerate(counts)]


class Rules(unittest.TestCase):

    def test_a_rise_is_misfires_by_its_weight_and_a_fall_is_nothing(self):
        g = share(pts([0, 12, 12, 0, 24, 0]))
        self.assertAlmostEqual(g["misfires"], 3.0)
        self.assertEqual(g["episodes"], 2)
        self.assertAlmostEqual(g["idle_s"], 5.0)

    def test_the_share_is_per_hundred_combustions(self):
        # 800 rpm is 26.7 combustions a second; 60 s with one misfire
        g = share(pts([0] * 30 + [12] + [0] * 30))
        self.assertAlmostEqual(g["share"], 100.0 / (800.0 / 30.0 * 60.0), places=4)

    def test_an_episode_climbs_when_it_passes_one_misfire(self):
        self.assertEqual(share(pts([0, 12, 12, 0]))["climbed"], 0)
        self.assertEqual(share(pts([0, 12, 24, 36, 0]))["climbed"], 1)
        self.assertEqual(share(pts([0, 24, 0]))["climbed"], 1)
        g = share(pts([0, 12, 24, 0, 12, 0, 12, 36, 0]))
        self.assertEqual((g["episodes"], g["climbed"]), (3, 2))

    def test_off_idle_load_on_and_detection_off_are_not_read(self):
        self.assertEqual(share(pts([0, 12, 24], rpm=1500.0))["idle_s"], 0.0)
        self.assertEqual(share(pts([0, 12, 24], load=40.0))["idle_s"], 0.0)
        self.assertEqual(share(pts([0, 12, 24], active=False))["idle_s"], 0.0)
        self.assertEqual(share(pts([0, 12, 24], dt=5.0))["idle_s"], 0.0)
        self.assertTrue(math.isnan(share(pts([0, 0], rpm=1500.0))["share"]))

    def test_a_silence_is_unbroken_idle_at_zero(self):
        self.assertAlmostEqual(share(pts([0] * 11))["longest_s"], 10.0)
        self.assertAlmostEqual(share(pts([0] * 5 + [12] + [0] * 8))["longest_s"], 8.0)
        gap = pts([0] * 6) + [(t + 60.0, r, ld, c, a) for t, r, ld, c, a in pts([0] * 4)]
        self.assertAlmostEqual(share(gap)["longest_s"], 5.0)

    def test_a_row_that_does_not_parse_is_left_out(self):
        got = misfshare.samples([(0.0, ["800", "20.0", "0", "aktivováno"]),
                                 (1.0, ["", "", "", ""]),
                                 (2.0, ["810", "21.0", "12", "deaktiv."])])
        self.assertEqual(got, [(0.0, 800.0, 20.0, 0.0, True),
                               (2.0, 810.0, 21.0, 12.0, False)])


class TheWarmStopOfTwelveEleven(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.g = misfshare.read(os.path.join(VCDS, "vcds-step6w-stop-014-032-036.csv"))

    def test_the_log_is_dated_from_its_own_header(self):
        self.assertEqual(self.g["stamp"], "12/11 11:21")
        self.assertIsNone(self.g["coolant"])

    def test_one_misfire_and_twelve_minutes_of_silence(self):
        self.assertAlmostEqual(self.g["misfires"], 1.0)
        self.assertTrue(12.0 < self.g["longest_s"] / 60.0 < 12.5)
        self.assertLess(self.g["share"], 0.02)

    def test_a_log_without_014_is_none(self):
        self.assertIsNone(misfshare.read(
            os.path.join(VCDS, "vcds-step8a-end-adaptations-032-055.csv")))


if __name__ == "__main__":
    unittest.main()
