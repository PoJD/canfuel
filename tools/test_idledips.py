#!/usr/bin/env python3
"""Tests for idledips.py -- the dip detector behind the idle tables.

Running them:
    python -m unittest discover -s tools -p 'test_*.py' -v
    python tools/test_idledips.py

These are properties of the detector rather than a copy of the published
counts. Pinning the counts here would put the same numbers in two places and
guarantee that one of them goes stale, which is the thing docs/engine-health.md
and CLAUDE.md both argue against; the counts have exactly one home and it is
the tool's own output.

What is worth holding, and what each test is really about:

- a dip is an EVENT, not a sample. A wide dip and a narrow one of the same
  depth are one event each, or logs of different length cannot be compared
- the baseline has to ride a ramp. Idle falls from about 930 to 800 rpm over a
  cold-start warm-up, and none of that is a dip
- the threshold is a floor, not a band. A 40 rpm excursion counts at 20 and at
  15, and the two numbers are therefore nested rather than independent
- an overshoot is not a dip. Only excursions BELOW the baseline count, because
  the symptom is the engine losing speed
"""

from __future__ import annotations

import unittest

from idledips import dips

RATE_HZ = 94.0  # what 0x280 actually arrives at; see docs/can-decoding.md
STEP = 1.0 / RATE_HZ


def series(seconds, baseline=800.0, events=(), ramp=0.0):
    """A synthetic engine-speed series.

    events is a sequence of (start_s, duration_s, depth_rpm); ramp is in rpm
    per second and is applied to the baseline.
    """
    out = []
    n = int(seconds * RATE_HZ)
    for i in range(n):
        t = i * STEP
        v = baseline + ramp * t
        for start, dur, depth in events:
            if start <= t < start + dur:
                v -= depth
        out.append((t, v))
    return out


class DipDetector(unittest.TestCase):
    def test_a_quiet_series_has_no_dips(self):
        events, span = dips(series(30.0), 20)
        self.assertEqual(events, [])
        self.assertAlmostEqual(span, 30.0, delta=0.05)

    def test_one_dip_is_one_event_however_long_it_lasts(self):
        for duration in (0.05, 0.2, 0.5):
            with self.subTest(duration=duration):
                found, _ = dips(series(30.0, events=[(10.0, duration, 40.0)]), 20)
                self.assertEqual(len(found), 1)
                self.assertAlmostEqual(found[0][0], 10.0, delta=duration + 0.05)
                self.assertAlmostEqual(found[0][1], 40.0, delta=1.0)

    def test_separate_dips_are_separate_events(self):
        found, _ = dips(
            series(30.0, events=[(8.0, 0.1, 40.0), (12.0, 0.1, 40.0),
                                 (16.0, 0.1, 40.0)]),
            20,
        )
        self.assertEqual(len(found), 3)

    def test_the_threshold_is_a_floor_so_the_counts_nest(self):
        rpm = series(30.0, events=[(10.0, 0.1, 40.0), (14.0, 0.1, 18.0)])
        at20, _ = dips(rpm, 20)
        at15, _ = dips(rpm, 15)
        self.assertEqual(len(at20), 1)
        self.assertEqual(len(at15), 2)

    def test_a_warm_up_ramp_is_not_a_dip(self):
        """Idle falls about 130 rpm over the cold-start run in 18_coldstart_z1.

        A baseline that could not ride that would report the whole warm-up as
        one long dip, and the cold-start row would be meaningless.
        """
        found, _ = dips(series(300.0, baseline=930.0, ramp=-0.43), 20)
        self.assertEqual(found, [])

    def test_an_overshoot_is_not_a_dip(self):
        found, _ = dips(series(30.0, events=[(10.0, 0.1, -40.0)]), 20)
        self.assertEqual(found, [])

    def test_a_window_can_be_restricted(self):
        rpm = series(30.0, events=[(5.0, 0.1, 40.0), (20.0, 0.1, 40.0)])
        found, span = dips(rpm, 20, 15.0, 25.0)
        self.assertEqual(len(found), 1)
        self.assertAlmostEqual(span, 10.0, delta=0.05)


if __name__ == "__main__":
    unittest.main()
