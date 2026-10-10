#!/usr/bin/env python3
"""Tests for dipcontext.py -- what comes before an idle dip.

What is held:

- the run reading puts a next dip at one engine cycle on the same cylinder,
  at one and a half on the partner, and anything else on neither
- on a real warm idle the control is flat and the dip itself is found where
  it was triggered on -- the two things that make the trigger reading mean
  anything at all
- the injector cuts of `31` are found and kept out, so that a dead cylinder
  is never read as a dip
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import os
import unittest

import dipcontext
from dipcontext import Capture, Series, runs, trigger
from idledips import FIXTURES


class _Stub:
    """Just enough of a Capture for runs()."""

    def __init__(self, dips, rpm=800.0):
        self._dips = dips
        self.rpm = Series([(0.0, rpm)])

    def dips(self):
        return self._dips


class RunsTest(unittest.TestCase):
    CYC = 120.0 / 800.0

    def test_whole_and_half_cycles(self):
        c = self.CYC
        n, whole, half = runs(_Stub([0.0, 1 * c, 10.0, 10.0 + 2.5 * c, 20.0, 20.0 + 0.25 * c]))
        self.assertEqual(n, 6)
        self.assertEqual(whole, 1)   # 0 -> 1 cycle
        self.assertEqual(half, 1)    # 10 -> 2.5 cycles
        # the quarter-cycle pair counts as neither

    def test_far_apart_is_neither(self):
        self.assertEqual(runs(_Stub([0.0, 5.0, 10.0]))[1:], (0, 0))


def _path(name):
    return os.path.join(FIXTURES, name)


class RealIdleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cap = Capture(_path("28_sessionA2_warm_z1.txt"))
        cls.out, cls.n = trigger([cls.cap])

    def test_there_are_dips(self):
        self.assertGreater(self.n, 20)

    def test_the_dip_is_where_it_was_triggered(self):
        speed = dict((o, m) for o, m, _, _ in self.out["speed"])
        self.assertLess(speed[0.0], -8.0)

    def test_the_control_is_flat(self):
        # Flat against the dip, not against zero: one capture drifts a rpm
        # or so a second as the idle settles, and that is the drift the
        # control is there to show.
        limit = {"speed": 2.0, "inj": 0.2, "b7": 0.2}
        for c in dipcontext.CHANNELS:
            for _, _, _, mc in self.out[c]:
                self.assertLess(abs(mc), limit[c], c)


class CutsTest(unittest.TestCase):

    def test_the_cuts_of_31_are_kept_out(self):
        cap = Capture(_path("31_step4_drive_z1.txt"))
        self.assertEqual(len(cap.cuts), 4)
        for a, b in cap.cuts:
            self.assertFalse(cap.idle((a + b) / 2.0))


if __name__ == "__main__":
    unittest.main()
