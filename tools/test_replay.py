#!/usr/bin/env python3
"""Testy referencniho dekoderu replay.py.

Az bude hotove ceckove jadro, tenhle soubor je sablona pro test_compute.c --
stejne fixtures, stejna ocekavana cisla.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from canlog import Frame, parse_file
from replay import (AVG_MIN_M, Compute, Decoded, decode,
                    SPEED_GATE_FORBIDDEN, SPEED_GATE_REQUIRED)

FIXTURES = Path(__file__).resolve().parent.parent / "test" / "fixtures"


def frame(can_id: int, hexdata: str, ts=None) -> Frame:
    return Frame(ts, can_id, bytes.fromhex(hexdata))


class TestDecode(unittest.TestCase):
    def setUp(self):
        self.st = Decoded()

    def test_rpm(self):
        # b2-b3 = 90 0c -> 0x0C90 = 3216 -> 804 ot/min
        decode(frame(0x280, "0123900c25261725"), self.st)
        self.assertAlmostEqual(self.st.rpm, 804.0, places=1)

    def test_clt(self):
        decode(frame(0x288, "8fbe3000004e2900"), self.st)
        self.assertAlmostEqual(self.st.clt_c, 0xBE * 0.75 - 48, places=2)

    def test_clt_error_value(self):
        decode(frame(0x288, "8fff3000004e2900"), self.st)
        self.assertIsNone(self.st.clt_c)

    def test_oil_error_value(self):
        decode(frame(0x420, "030000ffb800ff00"), self.st)
        self.assertIsNone(self.st.oil_c)

    def test_tank_reserve_bit(self):
        decode(frame(0x320, "0400800000000000"), self.st)
        self.assertEqual(self.st.tank_l, 0)
        self.assertTrue(self.st.tank_reserve)

    def test_counter_masking(self):
        decode(frame(0x480, "f208ffff00000000"), self.st)
        self.assertEqual(self.st.fuel_counter, 0x7FFF)
        self.assertTrue(self.st.counter_wrapped)

    def test_counter_wrap_flag_clear(self):
        # b3 = 0x7C, takze bit 15 je nula -- citac jeste od zapalovani nepretekl
        decode(frame(0x480, "f2085c7c00000000"), self.st)
        self.assertEqual(self.st.fuel_counter, 0x7C5C)
        self.assertFalse(self.st.counter_wrapped)

    def test_counter_wrap_flag_set(self):
        decode(frame(0x480, "f2085cfc00000000"), self.st)
        self.assertEqual(self.st.fuel_counter, 0x7C5C)
        self.assertTrue(self.st.counter_wrapped)


class TestSpeedGate(unittest.TestCase):
    def gate(self, b1: int) -> bool:
        st = Decoded()
        decode(frame(0x1A0, f"00{b1:02x}5b13fefe0013"), st)
        return st.speed_valid

    def test_accepted_states(self):
        for b1 in (0x40, 0x48, 0x50, 0x58):
            self.assertTrue(self.gate(b1), f"0x{b1:02X} mel projit")

    def test_rejected_states(self):
        for b1 in (0x00, 0x42, 0x43, 0x03):
            self.assertFalse(self.gate(b1), f"0x{b1:02X} mel byt zahozen")

    def test_stale_speed_is_kept_but_flagged(self):
        """Pri neplatne brane se hodnota neaktualizuje a priznak spadne."""
        st = Decoded()
        decode(frame(0x1A0, "00405b13fefe0013"), st)
        self.assertTrue(st.speed_valid)
        self.assertAlmostEqual(st.speed_kmh, 24.775, places=3)
        decode(frame(0x1A0, "00430100fefe001d"), st)
        self.assertFalse(st.speed_valid)
        self.assertAlmostEqual(st.speed_kmh, 24.775, places=3)

    def test_constants_match_documented_rule(self):
        self.assertEqual(SPEED_GATE_REQUIRED, 0x40)
        self.assertEqual(SPEED_GATE_FORBIDDEN, 0x03)


class TestCounterRestart(unittest.TestCase):
    """Past cislo jedna: po vypnuti zapalovani se citac resetuje na nulu."""

    def running(self, counter: int, rpm: float = 800.0) -> Decoded:
        st = Decoded()
        st.rpm = rpm
        st.fuel_counter = counter
        return st

    def test_normal_delta(self):
        cp = Compute()
        cp.on_counter(self.running(1000), 0.0)
        cp.on_counter(self.running(1050), 49.5)
        self.assertEqual(cp.total_ul, 50)
        self.assertEqual(cp.restarts, 0)

    def test_wrap_at_32768(self):
        cp = Compute()
        cp.on_counter(self.running(32700), 0.0)
        cp.on_counter(self.running(9), 49.5)
        self.assertEqual(cp.total_ul, 77)

    def test_ignition_off_does_not_produce_a_jump(self):
        """Bez detekce restartu by tady pribylo 12 000 ul z niceho."""
        cp = Compute()
        cp.on_counter(self.running(12000), 0.0)
        cp.on_counter(self.running(12100), 49.5)
        self.assertEqual(cp.total_ul, 100)
        cp.on_counter(self.running(0, rpm=0.0), 99.0)   # zapalovani vypnuto
        cp.on_counter(self.running(30, rpm=800.0), 148.5)  # a zase zapnuto
        # Zapocita se jen 30 ul skutecne spotrebovanych po restartu.
        # Bez detekce by tady delta byla (0 - 12100) mod 32768 = 20 668.
        self.assertEqual(cp.total_ul, 130)
        self.assertEqual(cp.restarts, 1)

    def test_engine_stopped_resets_reference(self):
        cp = Compute()
        cp.on_counter(self.running(5000), 0.0)
        cp.on_counter(self.running(5000, rpm=0.0), 49.5)
        cp.on_counter(self.running(5100), 99.0)
        self.assertEqual(cp.total_ul, 100)


class TestFuelNow(unittest.TestCase):
    def now(self, speed: float, flow_ul_s: float, valid: bool = True):
        st = Decoded()
        st.speed_kmh = speed
        st.speed_valid = valid
        cp = Compute()
        cp.flow_ul_s = flow_ul_s
        return cp.fuel_now(st)

    def test_below_threshold_is_litres_per_hour(self):
        val, unit = self.now(3.9, 310)
        self.assertEqual(unit, "l/h")
        self.assertAlmostEqual(val, 1.116, places=3)

    def test_at_threshold_switches(self):
        _, unit = self.now(4.0, 310)
        self.assertEqual(unit, "l/100km")

    def test_no_hysteresis(self):
        """Jediny prah. Skok pri prepnuti je zamer, ne chyba."""
        self.assertEqual(self.now(3.999, 500)[1], "l/h")
        self.assertEqual(self.now(4.000, 500)[1], "l/100km")

    def test_clamped_to_999(self):
        val, unit = self.now(4.0, 100_000)
        self.assertEqual(unit, "l/100km")
        self.assertAlmostEqual(val, 99.9, places=1)

    def test_invalid_speed_falls_back_to_flow(self):
        _, unit = self.now(50.0, 310, valid=False)
        self.assertEqual(unit, "l/h")

    def test_zero_flow(self):
        val, _ = self.now(0.0, 0)
        self.assertEqual(val, 0.0)

    def test_documented_table(self):
        """Tabulka z implementacniho planu, sekce 3.1."""
        for speed, flow_lh, expect in ((4, 1.5, 37.5), (6, 1.5, 25.0), (10, 1.5, 15.0),
                                       (6, 3.0, 50.0), (20, 3.0, 15.0), (10, 6.0, 60.0)):
            val, unit = self.now(speed, flow_lh * 1000 / 3.6)
            self.assertEqual(unit, "l/100km")
            self.assertAlmostEqual(val, expect, places=1, msg=f"{speed} km/h, {flow_lh} l/h")


class TestAverage(unittest.TestCase):
    def test_below_minimum_distance_is_zero(self):
        """Deleni skoro nulovou drahou davalo na 06_trip_reset 21 395 l/100 km."""
        cp = Compute()
        cp.total_ul = 17544
        cp.total_mm = (AVG_MIN_M - 1) * 1000
        self.assertEqual(cp.avg_l100, 0.0)

    def test_ratio_of_accumulators(self):
        cp = Compute()
        cp.total_ul = 700_000           # 0,7 l
        cp.total_mm = 10_000_000        # 10 km
        self.assertAlmostEqual(cp.avg_l100, 7.0, places=3)

    def test_idling_does_not_ruin_the_average(self):
        """Prumer je podil akumulatoru, takze stani prida palivo, ne nekonecno."""
        cp = Compute()
        cp.total_ul = 700_000
        cp.total_mm = 10_000_000
        before = cp.avg_l100
        cp.total_ul += 18_652           # minuta volnobehu
        self.assertLess(cp.avg_l100 - before, 3.0)


class TestAgainstFixtures(unittest.TestCase):
    """Cisla, ktera musi po prepsani do C vyjit stejne."""

    def run_log(self, name, fix_doubled=True):
        frames = parse_file(FIXTURES / name, fix_doubled=fix_doubled)
        st, cp = Decoded(), Compute()
        synthetic = all(f.ts_ms is None for f in frames)
        n480 = 0
        prev_ms = None
        for f in frames:
            now_ms = None
            if f.can_id == 0x480:
                now_ms = n480 * 49.5 if synthetic else float(f.ts_ms)
                n480 += 1
            decode(f, st)
            if now_ms is None:
                continue
            if prev_ms is not None:
                cp.on_distance(st, (now_ms - prev_ms) / 1000.0)
            prev_ms = now_ms
            cp.on_counter(st, now_ms)
        return st, cp

    def test_idle_totals(self):
        _, cp = self.run_log("02_idle_60s.txt")
        self.assertEqual(cp.total_ul, 18652)
        self.assertEqual(cp.total_mm, 0)
        self.assertEqual(cp.restarts, 0)

    def test_ign_only_burns_nothing_and_moves_nothing(self):
        _, cp = self.run_log("01_ign_only.txt")
        self.assertEqual(cp.total_ul, 0)
        self.assertEqual(cp.total_mm, 0)

    def test_trip_reset_distance_matches_the_checklist(self):
        """Checklist rikal 'popojet aspon 0,1 km'. Vyslo 125 m."""
        _, cp = self.run_log("06_trip_reset.txt")
        self.assertEqual(cp.total_ul, 51992)
        self.assertGreater(cp.total_mm, 100_000)
        self.assertLess(cp.total_mm, 200_000)

    def test_accel_distance_needs_the_corrected_gate(self):
        """S rovnosti b1 == 0x40 by vyslo 14 m misto 27 m."""
        _, cp = self.run_log("07_accel.txt")
        self.assertEqual(cp.total_ul, 9752)
        self.assertGreater(cp.total_mm, 20_000)

    def test_restart_detection_covers_engine_off_prefix(self):
        """06 zacina zapalovanim bez motoru, takze restartu je hodne -- a je
        to spravne. Vsechny padnou do uvodniho useku, ne doprostred jizdy."""
        _, cp = self.run_log("06_trip_reset.txt")
        self.assertGreater(cp.restarts, 300)
        _, cp7 = self.run_log("07_accel.txt")
        self.assertEqual(cp7.restarts, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
