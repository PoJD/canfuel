#!/usr/bin/env python3
"""Tests for fuelratio.py -- the old MAF's morning, and nothing else moving.

What is held: the ratio sits in its usual band on August's old MAF and on
the new one, and falls well below it on the hot idle of 24/9 after the
pulls, on the old MAF (refuted.md C2).
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import os
import statistics
import unittest

import fuelratio


def _median(name):
    w = fuelratio.windows(os.path.join(fuelratio.FIXTURES, name))
    return statistics.median(r for _, r, _ in w)


class RatioTest(unittest.TestCase):

    def test_august_on_the_old_maf_is_in_the_usual_band(self):
        self.assertTrue(0.29 < _median("09_idle_60s_z1.txt") < 0.33)

    def test_the_new_maf_is_in_the_same_band(self):
        self.assertTrue(0.29 < _median("24_mafswap_drive_z1.txt") < 0.33)

    def test_the_hot_idle_of_24_9_on_the_old_maf_is_far_below(self):
        self.assertLess(_median("20_postfix_final_z1.txt"), 0.24)


if __name__ == "__main__":
    unittest.main()
