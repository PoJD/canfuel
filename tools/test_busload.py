#!/usr/bin/env python3
"""Tests for busload.py: the bit counting by hand, then one real capture."""

from __future__ import annotations

import fixturecache  # noqa: F401 -- before any canlog import; see its docstring
import unittest
from pathlib import Path

import busload

FIXTURES = Path(__file__).resolve().parent.parent / "test" / "fixtures"


class TestBits(unittest.TestCase):
    def test_all_zero_frame_by_hand(self):
        # SOF, ID, RTR/IDE/r0, DLC and a CRC of zero are 34 dominant bits in a
        # row: a stuff bit after the 5th, 10th, ... 30th, so six.
        self.assertEqual(busload.crc15([0] * 19), 0)
        self.assertEqual(busload.stuff_bits(0x000, b""), 6)
        self.assertEqual(busload.frame_bits(0x000, b""), 47 + 6)

    def test_stuffing_never_beyond_the_bound(self):
        for can_id in (0x000, 0x1A0, 0x280, 0x7FF):
            for data in (b"\x00" * 8, b"\xff" * 8, b"\x55" * 8, b"\x0f\xf0" * 4):
                self.assertLessEqual(busload.stuff_bits(can_id, data),
                                     busload.worst_stuff(len(data)))

    def test_converter_schedule_from_config(self):
        rates = busload.converter_rates()
        self.assertEqual(rates["always"], 22)   # 2 x 10 Hz + 0x602 + 0x604
        self.assertEqual(rates["jp1"], 1)


class TestCapture(unittest.TestCase):
    def test_idle_capture(self):
        m = busload.measure(str(FIXTURES / "09_idle_60s_z1.txt"))
        self.assertTrue(15 < busload.pct(m["car_bps"]) < 18)
        self.assertTrue(0.4 < busload.pct(m["conv_bps"]) < 0.7)

    def test_bursts(self):
        b = busload.bursts(str(FIXTURES / "09_idle_60s_z1.txt"))
        self.assertLessEqual(b["longest_gap_ms"], 10)        # nothing is slower
        self.assertLess(b["peak_pct"][1], 100)
        self.assertLess(b["densest_plus_tx_pct"], 100)        # still fits the ms
        self.assertEqual(b["ms_over_80_pct"], 0)

    def test_filtered_capture_refused(self):
        with self.assertRaises(ValueError):
            busload.measure(str(FIXTURES / "24_mafswap_drive_z1.txt"))


if __name__ == "__main__":
    unittest.main()
