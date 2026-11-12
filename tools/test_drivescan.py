#!/usr/bin/env python3
"""Tests for drivescan.py -- every stroke of a whole drive put to its
cylinder.

Synthetic streams hold what the reading rests on: one stroke count carried
through engine speeds where a stroke is shorter than a frame, by the parity
of the crank wheel's alternation; the two differences the wheel does not
touch; the scale of a stroke off idle. One real capture holds the count
from idle to idle through 5,800 rpm, and what the corpus is read by: off
idle cylinder 3 gives next to what 2 does under load, and 4 less than 1.
"""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import io
import os
import unittest

import cylscan
import drivescan
from drivescan import (FRAME_S, Drive, stroke_rpm, track_drive, windows)
from idledips import FIXTURES

ORDER = (2, 1, 3, 4)                    # the cylinder of stroke k is ORDER[k % 4]
WHEEL = {1: -1.0, 3: 1.0, 4: -1.0, 2: 1.0}


def profile(k):
    """Engine speed of stroke k without the cylinders: an idle, a pull to
    5,200 rpm and back, an idle."""
    if k < 1200:
        return 800.0
    if k < 4200:
        return 800.0 + (k - 1200) * 4400.0 / 3000.0
    if k < 7200:
        return 5200.0 - (k - 4200) * 4400.0 / 3000.0
    return 800.0


def strokes(n=8400, weak3=4.0, wheel=cylscan.WHEEL_ALT):
    """Per-stroke speeds: the wheel's alternation in the steps (so half of
    it in the levels), cylinder 2 the strongest and 3 the weakest at idle."""
    out = []
    for k in range(n):
        base = profile(k)
        c = ORDER[k % 4]
        r = base * (1.0 + 0.5 * wheel * WHEEL[c])
        if base < 1000.0:
            r += {2: weak3, 3: -weak3, 1: 0.0, 4: 0.0}[c] / 2.0
        out.append(round(r * 4.0) / 4.0)
    return out


def stream(stroke_rpm_values, jitter=True):
    """0x280 samples (t, rpm, throttle, speed) on the frame grid: each
    stroke's value shown from its end on, the pedal at rest at idle."""
    edges, t = [], 0.0
    for r in stroke_rpm_values:
        t += 30.0 / r
        edges.append(t)
    out, k, n = [], 0, 0
    t = edges[0]
    while t < edges[-1]:
        while k + 1 < len(edges) and edges[k + 1] <= t:
            k += 1
        r = stroke_rpm_values[k]
        out.append((t, r, 35 if r < 1000.0 else 80, 0))
        n += 1
        # the adapter stamps a frame 2 ms early or late now and then
        t += FRAME_S + (((n * 7) % 5 - 2) * 0.001 if jitter else 0.0)
    return out


def slot_of_two(e, k, t0, t1):
    """The slot (k mod 4) whose steps are the largest between t0 and t1."""
    sums, cnt = [0.0] * 4, [0] * 4
    prev = None
    for x, kk in zip(e, k):
        if kk is None or not t0 <= x[0] <= t1:
            continue
        if prev is not None and kk == prev[0] + 1:
            sums[kk % 4] += x[1] - prev[1]
            cnt[kk % 4] += 1
        if prev is None or kk != prev[0]:
            prev = (kk, x[1])
    return max(range(4), key=lambda q: sums[q] / max(cnt[q], 1))


class Counting(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.e = stream(strokes())
        cls.end = cls.e[-1][0]

    def test_the_parity_carries_the_count_through_a_pull(self):
        k, seg = track_drive(self.e, sign=None)
        sign = drivescan.learn_sign(self.e, k, seg)
        self.assertIn(sign, (1, -1))
        k, seg = track_drive(self.e, sign)
        self.assertEqual(seg[-1], 0)
        first = slot_of_two(self.e, k, 5.0, 40.0)
        last = slot_of_two(self.e, k, self.end - 40.0, self.end - 5.0)
        self.assertEqual(first, last)
        # and the sign learned is the wheel's: 2's slot is one that reads high
        self.assertEqual(sign, 1 if first % 2 == 0 else -1)

    def test_without_the_parity_the_count_is_restarted_not_trusted(self):
        k, seg = track_drive(self.e, sign=None)
        self.assertGreater(seg[-1], 0)

    def test_every_stroke_index_is_seen_below_one_frame_a_stroke(self):
        k, _ = track_drive(self.e, sign=1)
        idle = [kk for x, kk in zip(self.e, k) if x[0] < 40.0 and kk is not None]
        self.assertEqual(sorted(set(idle)), list(range(idle[0], idle[-1] + 1)))

    def test_a_stopped_engine_restarts_the_count(self):
        e = stream([800.0 + (k % 4) for k in range(600)], jitter=False)
        stop = e[-1][0]
        e += [(stop + 0.01 * (m + 1), 0.0, 35, 0) for m in range(300)]
        again = stream([800.0 + (k % 4) for k in range(600)], jitter=False)
        e += [(t + stop + 3.1, r, th, v) for t, r, th, v in again]
        _, seg = track_drive(e, sign=None)
        self.assertEqual(seg[10], 0)
        self.assertEqual(seg[-1], 1)


class Reading(unittest.TestCase):

    def data(self, values):
        e = stream(values)
        return {"e": e, "b7": [26 if x[1] < 1000.0 else 120 for x in e],
                "fuel": [(x[0], i) for i, x in enumerate(e)],
                "oil": [(0.0, 95.0)], "ac": []}

    def test_the_idle_names_the_cylinders_through_the_pull(self):
        d = Drive(self.data(strokes()))
        self.assertEqual(len(d.idles), 2)
        self.assertEqual(d.idles[0][2], d.idles[1][2])
        self.assertNotIn(None, d.SLOT2[100:-100])
        # the generator's cylinder is the tool's, at 5,000 rpm too
        hi = [i for i, r in enumerate(d.R) if r > 4800.0]
        self.assertGreater(len(hi), 100)
        off = {True: [], False: []}
        for i in hi:
            off[d.cyl(i) in (2, 3)].append(d.R[i] - profile_at(d, i))
        self.assertGreater(sum(off[True]) / len(off[True]), 3.0)
        self.assertLess(sum(off[False]) / len(off[False]), -3.0)

    def test_three_less_two_and_one_less_four_carry_no_wheel(self):
        # a wheel twice cylscan's, as it is past 4,000 rpm, and equal
        # cylinders off idle: the two differences stay at nothing
        d = Drive(self.data(strokes(wheel=2.0 * cylscan.WHEEL_ALT)))
        ws = [w for w in windows(d) if 2000.0 < w.rpm < 5000.0]
        self.assertGreater(len(ws), 50)
        dev = [w.deviation() for w in ws]
        m32 = sum(x[3] - x[2] for x in dev) / len(dev)
        m14 = sum(x[1] - x[4] for x in dev) / len(dev)
        self.assertAlmostEqual(m32, 0.0, delta=0.3)
        self.assertAlmostEqual(m14, 0.0, delta=0.3)
        # while the pair 2 and 3 against 1 and 4 reads the extra wheel
        pair = sum(x[2] + x[3] - x[1] - x[4] for x in dev) / len(dev)
        self.assertGreater(pair, 2.0)

    def test_the_idle_reads_three_under_two(self):
        d = Drive(self.data(strokes()))
        ws = [w for w in windows(d) if w.rpm < 900.0]
        dev = [w.deviation() for w in ws]
        self.assertLess(sum(x[3] - x[2] for x in dev) / len(dev), -3.0)

    def test_a_stroke_is_worth_more_rpm_under_load_and_less_at_speed(self):
        self.assertAlmostEqual(stroke_rpm(800.0, 25.0), cylscan.STROKE_RPM)
        self.assertAlmostEqual(stroke_rpm(1600.0, 25.0), cylscan.STROKE_RPM / 2)
        self.assertAlmostEqual(stroke_rpm(800.0, 100.0), cylscan.STROKE_RPM * 4)


def profile_at(d, i):
    """The mean of the strokes seen round i: the level without the wheel."""
    seg = d.R[max(i - 8, 0):i + 9]
    return sum(seg) / len(seg)


class Corpus(unittest.TestCase):
    """`39`: 33 minutes home, with pulls to 5,797 rpm."""

    @classmethod
    def setUpClass(cls):
        path = os.path.join(FIXTURES, "39_drive_home_z1.txt")
        cls.data = drivescan.read(path)
        cls.drive = Drive(cls.data)
        cls.ws = windows(cls.drive)

    def test_one_count_from_the_first_idle_to_the_last(self):
        self.assertIsNotNone(self.drive.sign)
        self.assertGreaterEqual(len(self.drive.idles), 4)
        self.assertEqual(len({x[2] for x in self.drive.idles}), 1)
        self.assertGreater(max(self.drive.R), 5500.0)
        buf = io.StringIO()
        self.assertTrue(drivescan.report_count("39", self.drive, out=buf))

    def test_the_timing_alone_loses_it(self):
        # the reading this tool replaces: no parity, and no restart either
        saved = drivescan.UNAIDED_MAX_RPM
        drivescan.UNAIDED_MAX_RPM = 1e9
        try:
            d = Drive(self.data, parity=False)
        finally:
            drivescan.UNAIDED_MAX_RPM = saved
        self.assertGreater(len({x[2] for x in d.idles}), 1)

    def test_nothing_is_left_on_the_overrun(self):
        sel = [w for w in self.ws if w.cut > 0.95 and 1600 <= w.rpm < 3300]
        self.assertGreater(len(sel), 40)
        dev = [w.deviation() for w in sel]
        self.assertAlmostEqual(sum(x[3] - x[2] for x in dev) / len(dev), 0.0,
                               delta=0.6)
        self.assertAlmostEqual(sum(x[1] - x[4] for x in dev) / len(dev), 0.0,
                               delta=0.6)

    def test_three_is_weak_at_idle_and_hardly_under_load(self):
        got = drivescan.report_pattern(self.ws, out=io.StringIO())
        self.assertLess(got["standing idle"][1], -12.0)
        loaded = [v for k, v in got.items() if "b7 90-140" in k or "b7 140-256" in k]
        self.assertTrue(loaded)
        for v in loaded:
            self.assertGreater(v[1], -6.0)


if __name__ == "__main__":
    unittest.main()
