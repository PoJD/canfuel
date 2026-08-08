#!/usr/bin/env python3
"""Testy canlog.py -- parsovani obou formatu a kotvy proti realnym fixtures.

Spousteni:
    python -m unittest discover -s tools -p 'test_*.py' -v
    python tools/test_canlog.py

Ucel je dvoji. Jednak zkontrolovat parser samotny, jednak zamknout nekolik
hodnot vyctenych z realnych logu. Kdyby se fixtures nekdy prekodovaly nebo
prohodily, tyhle testy to chyti driv, nez se podle nich zacne ladit firmware.

Cisla nize jsou zmerena z techto konkretnich souboru, ne opsana ze zadani.
Kde se merenim rozchazeji se zadanim, je to poznamenane u testu i
v docs/can-decoding.md.
"""

from __future__ import annotations

import statistics
import unittest
from pathlib import Path

import canlog
from canlog import Frame, LogFormatError, parse_file, parse_line, undouble

FIXTURES = Path(__file__).resolve().parent.parent / "test" / "fixtures"

# Perioda ramce 0x480. U logu bez casovych znacek je to jediny zpusob, jak
# z citace udelat prutok, takze na ni visi vsechny absolutni hodnoty nize.
PERIOD_0X480_S = 0.0495


def u16le(data: bytes, i: int) -> int:
    return data[i] | data[i + 1] << 8


class TestParseLineSlcan(unittest.TestCase):
    """Format A -- syrovy slcan proud."""

    def test_standard_frame(self):
        f = parse_line("t1a0800400100fefe001d")
        self.assertEqual(f.can_id, 0x1A0)
        self.assertEqual(f.dlc, 8)
        self.assertEqual(f.data, bytes.fromhex("00400100fefe001d"))
        self.assertIsNone(f.ts_ms)

    def test_short_dlc(self):
        # 0x5D0 chodi jako DLC 6, ne 8 -- klasicka past na parser s pevnou delkou.
        f = parse_line("t5d06000349090032")
        self.assertEqual(f.can_id, 0x5D0)
        self.assertEqual(f.dlc, 6)
        self.assertEqual(f.data, bytes.fromhex("000349090032"))

    def test_dlc_four(self):
        f = parse_line("t050400507020")
        self.assertEqual(f.can_id, 0x050)
        self.assertEqual(f.dlc, 4)
        self.assertEqual(f.data, bytes.fromhex("00507020"))

    def test_extended_id(self):
        f = parse_line("T1234567881122334455667788")
        self.assertEqual(f.can_id, 0x12345678)
        self.assertEqual(f.dlc, 8)

    def test_whitespace_and_blank(self):
        self.assertIsNone(parse_line(""))
        self.assertIsNone(parse_line("   \n"))
        self.assertEqual(parse_line("  t050400507020  \n").can_id, 0x050)

    def test_truncated_payload_raises(self):
        with self.assertRaises(LogFormatError):
            parse_line("t1a08004001")

    def test_dlc_over_eight_raises(self):
        with self.assertRaises(LogFormatError):
            parse_line("t1a09004001000000000000")

    def test_non_hex_raises(self):
        with self.assertRaises(LogFormatError):
            parse_line("t1a080040zz00fefe001d")


class TestParseLineViewer(unittest.TestCase):
    """Format B -- TSV export z USBtinVieweru."""

    ICON = "jar:file:/C:/x/USBtinViewer_v1.3.1.jar!/res/icons/receive.png"

    def line(self, ts, can_id, dlc, data):
        return f"{ts}\t{self.ICON}\t{can_id}\t{dlc}\t{data}"

    def test_receive_row(self):
        f = parse_line(self.line("2078", "320h", "8", "05 00 86 00 00 00 00 00"))
        self.assertEqual(f.ts_ms, 2078)
        self.assertEqual(f.can_id, 0x320)
        self.assertEqual(f.data, bytes.fromhex("0500860000000000"))

    def test_short_dlc_row(self):
        f = parse_line(self.line("2124", "5d0h", "6", "00 03 49 09 00 32"))
        self.assertEqual(f.can_id, 0x5D0)
        self.assertEqual(f.dlc, 6)

    def test_info_row_is_skipped(self):
        info = "jar:file:/C:/x/USBtinViewer_v1.3.1.jar!/res/icons/info.png"
        self.assertIsNone(parse_line(f"\t{info}\t\t\tConnected to USBtin (FW0105/HW0100, SN: FFFF)"))
        self.assertIsNone(parse_line(f"\t{info}\t\t\tDisconnected"))

    def test_dlc_mismatch_raises(self):
        with self.assertRaises(LogFormatError):
            parse_line(self.line("2078", "320h", "8", "05 00 86"))


class TestFormatDetection(unittest.TestCase):
    def test_tab_decides(self):
        """Format se pozna podle tabulatoru; slcan ho nikdy neobsahuje."""
        self.assertIsNone(parse_line("t1a0800400100fefe001d").ts_ms)
        self.assertIsNotNone(parse_line("2078\ticon\t1a0h\t8\t00 40 01 00 fe fe 00 1d").ts_ms)

    def test_frame_is_hashable_and_comparable(self):
        a = Frame(None, 0x480, b"\x01\x02")
        b = Frame(None, 0x480, b"\x01\x02")
        self.assertEqual(a, b)
        self.assertEqual(len({a, b}), 1)


class TestFixturesExist(unittest.TestCase):
    EXPECTED = [
        "01_ign_only.txt", "02_idle_60s.txt", "03_drive.txt", "05_rev3000.txt",
        "06_trip_reset.txt", "07_accel.txt", "idle.txt",
    ]

    def test_all_present(self):
        for name in self.EXPECTED:
            self.assertTrue((FIXTURES / name).is_file(), f"chybi fixture {name}")


class TestFixtureContent(unittest.TestCase):
    """Kotvy proti realnym logum. Vsechny hodnoty zmerene z techto souboru."""

    @classmethod
    def setUpClass(cls):
        cls.frames = {p.name: parse_file(p) for p in FIXTURES.glob("*.txt")}

    # -- ID na sbernici -----------------------------------------------------

    REGULAR_IDS = {0x050, 0x0C2, 0x1A0, 0x280, 0x288, 0x320,
                   0x420, 0x480, 0x488, 0x4A0, 0x520, 0x5A0, 0x5D0, 0x5D8}

    def test_regular_id_set(self):
        """Periodicky vysilanych ID je presne 14 -- viz docs/can-decoding.md.

        Vyjimka: 0x520 je tak pomale, ze se do kratkych logu nevejde vzdycky.
        """
        for name, frames in self.frames.items():
            seen = {f.can_id for f in frames}
            unexpected = seen - self.REGULAR_IDS - {0x767}
            self.assertEqual(unexpected, set(), f"{name}: neznama ID")
            self.assertTrue(seen >= self.REGULAR_IDS - {0x520}, f"{name}: chybi ID {self.REGULAR_IDS - seen}")

    def test_0x767_is_a_one_off(self):
        """0x767 je v 06 presne jednou, hned na prvni znacce, s DLC 2.

        Neni to periodicky ramec sbernice, ale jednorazova diagnosticka
        odpoved zachycena pri pripojeni USBtinu. Firmware ho ma ignorovat,
        ale rozsah 0x7xx uz kvuli nemu nelze povazovat za uplne tichy.
        """
        hits = [(n, f) for n, fr in self.frames.items() for f in fr if f.can_id == 0x767]
        self.assertEqual(len(hits), 1)
        name, frame = hits[0]
        self.assertEqual(name, "06_trip_reset.txt")
        self.assertEqual(frame.ts_ms, 2000)
        self.assertEqual(frame.data, bytes.fromhex("3cfe"))

    def test_target_ids_are_free(self):
        """0x600-0x602 nesmi na sbernici byt -- prevodnik je chce pro sebe."""
        for name, frames in self.frames.items():
            collisions = {f.can_id for f in frames if 0x600 <= f.can_id <= 0x602}
            self.assertEqual(collisions, set(), f"{name}: obsazene ID")

    def test_dlc_is_stable_per_id(self):
        """Kazde ID ma po celou dobu stejnou delku; 0x050 ma 4, 0x5D0 ma 6."""
        for name, frames in self.frames.items():
            per_id: dict[int, set[int]] = {}
            for f in frames:
                per_id.setdefault(f.can_id, set()).add(f.dlc)
            for can_id, dlcs in per_id.items():
                self.assertEqual(len(dlcs), 1, f"{name}: 0x{can_id:03X} ma DLC {dlcs}")
            self.assertEqual(per_id[0x050], {4})
            self.assertEqual(per_id[0x5D0], {6})
            self.assertEqual(per_id[0x480], {8})

    # -- format A vs B ------------------------------------------------------

    def test_slcan_fixtures_have_no_timestamps(self):
        for name in ("01_ign_only.txt", "02_idle_60s.txt", "03_drive.txt",
                     "05_rev3000.txt", "idle.txt"):
            self.assertTrue(all(f.ts_ms is None for f in self.frames[name]), name)

    def test_viewer_fixtures_have_monotonic_timestamps(self):
        for name in ("06_trip_reset.txt", "07_accel.txt"):
            ts = [f.ts_ms for f in self.frames[name]]
            self.assertTrue(all(t is not None for t in ts), name)
            self.assertEqual(ts, sorted(ts), f"{name}: casove znacky nejsou monotonni")

    def test_frame_counts(self):
        counts = {name: len(fr) for name, fr in self.frames.items()}
        self.assertEqual(counts["01_ign_only.txt"], 3402)
        self.assertEqual(counts["02_idle_60s.txt"], 89882)
        self.assertEqual(counts["03_drive.txt"], 18018)
        self.assertEqual(counts["05_rev3000.txt"], 1522)
        self.assertEqual(counts["06_trip_reset.txt"], 99101)
        self.assertEqual(counts["07_accel.txt"], 11188)
        self.assertEqual(counts["idle.txt"], 1136)

    # -- dekodovane signaly -------------------------------------------------

    def rpm(self, name):
        return [u16le(f.data, 2) * 0.25 for f in self.frames[name] if f.can_id == 0x280]

    def counter(self, name):
        return [u16le(f.data, 2) & 0x7FFF for f in self.frames[name] if f.can_id == 0x480]

    def test_ign_only_engine_is_off(self):
        """01_ign_only: motor stoji, takze otacky i citac jsou tvrde nuly."""
        self.assertTrue(all(r == 0 for r in self.rpm("01_ign_only.txt")))
        self.assertEqual(set(self.counter("01_ign_only.txt")), {0})

    def test_idle_rpm(self):
        """02 je zahraty volnobeh 797 ot/min, presne jak rika zadani."""
        self.assertAlmostEqual(statistics.median(self.rpm("02_idle_60s.txt")), 797, delta=1)

    def test_rev3000_rpm(self):
        """05 je 2940 ot/min v neutralu -- druhy kalibracni bod ztratoveho momentu."""
        self.assertAlmostEqual(statistics.median(self.rpm("05_rev3000.txt")), 2940, delta=2)

    def test_clt_warmup_curve(self):
        """Teplota kapaliny roste napric session: idle 68 -> 05 90 -> 03 99 -> 01 100,5."""
        def clt(name):
            vals = [f.data[1] * 0.75 - 48 for f in self.frames[name] if f.can_id == 0x288]
            return statistics.median(vals)
        self.assertAlmostEqual(clt("idle.txt"), 68.25, places=2)
        self.assertAlmostEqual(clt("05_rev3000.txt"), 90.00, places=2)
        self.assertAlmostEqual(clt("03_drive.txt"), 99.00, places=2)
        self.assertAlmostEqual(clt("01_ign_only.txt"), 100.50, places=2)

    def test_counter_bit15_is_a_sticky_wrap_flag(self):
        """Bit 15 NENI konstantne 1, jak tvrdi docs/sensors.md.

        Zmereno napric vsemi logy: bit 15 je nula od zapnuti zapalovani az do
        prvniho preteceni 15bitoveho citace, pak uz zustane trvale jedna.
        - 01_ign_only: motor stoji, citac je nula -> bit 15 je nula.
        - 06_trip_reset: zacina na nule, pri preteceni 32767 -> 15 se prehodi.
        - ostatni logy: motor bezi dlouho, citac uz pretekl -> jedna.

        Pro vypocet je to jedno, maska 0x7FFF ho zahodi. Pouzitelne je to ale
        jako priznak "tenhle cyklus zapalovani je jeste mlady".

        02_idle_60s je z tohoto testu vyjmuty, protoze je zdvojeny (viz nize)
        a druha kopie priznak zdanlive vrati zpatky na nulu.
        """
        for name, frames in self.frames.items():
            if name == "02_idle_60s.txt":
                continue
            b15 = [(f.data[3] >> 7) & 1 for f in frames if f.can_id == 0x480]
            if 1 in b15:
                first = b15.index(1)
                self.assertTrue(all(b == 1 for b in b15[first:]), f"{name}: bit 15 neni sticky")

    def test_counter_masked_to_15_bits(self):
        for name, frames in self.frames.items():
            masked = [u16le(f.data, 2) & 0x7FFF for f in frames if f.can_id == 0x480]
            self.assertTrue(all(0 <= v < 32768 for v in masked), name)

    def test_counter_only_moves_forward(self):
        """Delta se pocita (novy - stary) mod 32768 a nikdy nesmi byt zaporna."""
        for name in self.frames:
            vals = self.counter(name)
            deltas = [(b - a) % 32768 for a, b in zip(vals, vals[1:])]
            # Preskok pres pulku rozsahu by znamenal, ze jsme minuli pretečeni
            # nebo ze se citac resetoval po vypnuti zapalovani.
            big = [d for d in deltas if d > 16384]
            self.assertEqual(big, [], f"{name}: podezrele delty {big[:5]}")

    def test_accel_counter_span(self):
        """07_accel ma casove znacky, takze je to jediny fixture, ze ktereho
        jde absolutni prutok odvodit bez odhadu periody ramce.

        Zadani (BOOTSTRAP sekce 3) uvadi 13247 -> 22622 za 15,9 s. Konec sedi,
        zacatek ne -- v souboru je prvni vzorek 12870. Rozdil je 377 ul, tedy
        nekolik prvnich ramcu. Viz docs/can-decoding.md, otevrene otazky.
        """
        vals = self.counter("07_accel.txt")
        self.assertEqual(vals[0], 12870)
        self.assertEqual(vals[-1], 22622)

        stamped = [f.ts_ms for f in self.frames["07_accel.txt"] if f.can_id == 0x480]
        span_s = (stamped[-1] - stamped[0]) / 1000.0
        self.assertAlmostEqual(span_s, 15.915, places=3)

        total = sum((b - a) % 32768 for a, b in zip(vals, vals[1:]))
        self.assertEqual(total, 9752)

    def test_speed_gate_is_a_bitmask_not_an_equality(self):
        """Bajt 1 ramce 0x1A0 je bitove pole, ne jedna hodnota.

        Zadani (BOOTSTRAP sekce 3) rika "platne jen kdyz b1 == 0x40". To je
        prilis prisne. Namerene stavy napric logy:

            0x40  zakladni platny stav
            0x48  taky platny -- v 07_accel je dokonce vetsinovy (1301/1991)
                  a nese plny rozsah rychlosti vcetne maxima 24,78 km/h
            0x50  taky platny, 11-15 km/h
            0x43  inicializacni rampa po zapnuti zapalovani -> zahodit
            0x42  totez, jen 2 ramce

        Rovnost na 0x40 by v 07_accel zahodila dve tretiny vzorku rychlosti
        a ujeta draha by vysla 14 m misto 27 m. To by primo zkazilo FuelAvg
        i Range. Spravne pravidlo je (b1 & 0x40) && !(b1 & 0x03).
        """
        frames = [f for f in self.frames["07_accel.txt"] if f.can_id == 0x1A0]
        gates = {f.data[1] for f in frames}
        self.assertEqual(gates, {0x40, 0x48, 0x50})

        def speeds(gate):
            return [u16le(f.data, 2) * 0.005 for f in frames if f.data[1] == gate]

        # 0x48 neni okrajovy stav a nese stejne rychlosti jako 0x40
        self.assertGreater(len(speeds(0x48)), len(speeds(0x40)))
        self.assertAlmostEqual(max(speeds(0x48)), 24.70, places=2)
        self.assertAlmostEqual(max(speeds(0x40)), 24.78, places=2)

    def test_init_ramp_only_after_ignition_on(self):
        """0x43 a 0x42 jsou jen v logach, ktere zacinaji zapnutim zapalovani."""
        for name, frames in self.frames.items():
            gates = {f.data[1] for f in frames if f.can_id == 0x1A0}
            ramp = gates & {0x42, 0x43}
            if name in ("01_ign_only.txt", "06_trip_reset.txt"):
                self.assertEqual(ramp, {0x42, 0x43}, name)
            else:
                self.assertEqual(ramp, set(), f"{name}: necekana rampa {ramp}")

    def test_valid_speed_is_in_range(self):
        for name, frames in self.frames.items():
            valid = [u16le(f.data, 2) * 0.005 for f in frames
                     if f.can_id == 0x1A0 and (f.data[1] & 0x40) and not (f.data[1] & 0x03)]
            self.assertTrue(valid, name)
            self.assertLess(max(valid), 200.0, name)

    def test_tank_reserve_bit(self):
        """Nadrz hlasi 0 l a sviti rezerva -- bajt 2 rámce 0x320 je presne 0x80."""
        for name in ("01_ign_only.txt", "03_drive.txt", "05_rev3000.txt"):
            vals = {f.data[2] for f in self.frames[name] if f.can_id == 0x320}
            self.assertEqual(vals, {0x80}, name)

    def test_no_lambda_on_0x488(self):
        """0x488 je konstantni, lambda na sbernici neni."""
        for name, frames in self.frames.items():
            payloads = {f.data for f in frames if f.can_id == 0x488}
            self.assertEqual(payloads, {bytes.fromhex("ffffff8dffffffff")}, name)


class TestDoubledFixture(unittest.TestCase):
    """02_idle_60s.txt obsahuje zaznam presne dvakrat.

    Neni to teorie -- obe poloviny souboru jsou radek po radku shodne.
    Nechavame ho v repu tak, jak prisel z USBtinu, a opravujeme az pri cteni,
    aby se nemenila puvodni namerena data. Kdyby se soubor nekdy prepsal
    ocistenou verzi, tenhle test spadne a bude to videt.
    """

    def lines(self, name):
        return (FIXTURES / name).read_text(encoding="utf-8", errors="replace").splitlines()

    def test_02_is_doubled(self):
        lines = self.lines("02_idle_60s.txt")
        self.assertEqual(len(lines), 89882)
        half = len(lines) // 2
        self.assertEqual(lines[:half], lines[half:])

    def test_no_other_fixture_is_doubled(self):
        for path in FIXTURES.glob("*.txt"):
            if path.name == "02_idle_60s.txt":
                continue
            lines = self.lines(path.name)
            self.assertEqual(undouble(lines), lines, f"{path.name} je take zdvojeny")

    def test_undouble_is_idempotent(self):
        once = undouble(self.lines("02_idle_60s.txt"))
        self.assertEqual(len(once), 44941)
        self.assertEqual(undouble(once), once)

    def test_undouble_leaves_normal_input_alone(self):
        self.assertEqual(undouble(["a", "b", "c"]), ["a", "b", "c"])
        self.assertEqual(undouble([]), [])
        # dva stejne radky za sebou jeste neznamenaji zdvojeny soubor,
        # ale rozlisit to nejde -- proto se undouble pousti jen na cely log
        self.assertEqual(undouble(["a", "a"]), ["a"])

    def test_parse_file_fix_doubled(self):
        raw = parse_file(FIXTURES / "02_idle_60s.txt")
        fixed = parse_file(FIXTURES / "02_idle_60s.txt", fix_doubled=True)
        self.assertEqual(len(fixed) * 2, len(raw))


class TestFuelRates(unittest.TestCase):
    """Absolutni prutoky. Logy bez casovych znacek stoji na perioda 0x480."""

    def counter_total(self, name, *, fix_doubled=False):
        frames = parse_file(FIXTURES / name, fix_doubled=fix_doubled)
        vals = [u16le(f.data, 2) & 0x7FFF for f in frames if f.can_id == 0x480]
        total = sum((b - a) % 32768 for a, b in zip(vals, vals[1:]))
        return total, len(vals), frames

    def test_idle_flow_matches_specification(self):
        """Zahraty volnobeh 797 ot/min -> 310 ul/s = 1,12 l/h.

        Vychazi to na desetinu presne, ale jen ze souboru zbaveneho zdvojeni.
        Bez opravy by vysel dvojnasobek a cely vypocet spotreby by byl mimo.
        """
        total, n, _ = self.counter_total("02_idle_60s.txt", fix_doubled=True)
        self.assertEqual(n, 1216)
        self.assertEqual(total, 18652)
        span_s = (n - 1) * PERIOD_0X480_S
        self.assertAlmostEqual(span_s, 60.1, places=1)
        self.assertAlmostEqual(total / span_s, 310, delta=2)

    def test_rev3000_flow(self):
        """2940 ot/min v neutralu. Zadani uvadi 958 ul/s, z dat vychazi 1005.

        Rozdil 5 % nesedi na data, ale na predpokladanou periodu 0x480 --
        pri 51,9 ms by vyslo presne 958. Log casove znacky nema, takze to
        rozhodne az mereni na sbernici. Viz docs/can-decoding.md.
        """
        total, n, _ = self.counter_total("05_rev3000.txt")
        self.assertEqual(total, 1940)
        rate = total / ((n - 1) * PERIOD_0X480_S)
        self.assertAlmostEqual(rate, 1005, delta=5)

    def test_ign_only_burns_nothing(self):
        total, _, _ = self.counter_total("01_ign_only.txt")
        self.assertEqual(total, 0)

    def test_timestamped_logs_need_no_period_assumption(self):
        """06 a 07 maji znacky, takze jsou to jedine logy s tvrdym prutokem."""
        for name, expect_ul, expect_s in (("06_trip_reset.txt", 51992, 134.979),
                                          ("07_accel.txt", 9752, 15.915)):
            total, _, frames = self.counter_total(name)
            ts = [f.ts_ms for f in frames if f.can_id == 0x480]
            self.assertEqual(total, expect_ul, name)
            self.assertAlmostEqual((ts[-1] - ts[0]) / 1000, expect_s, places=3)


class TestCli(unittest.TestCase):
    def test_summary_runs(self):
        self.assertEqual(canlog.main([str(FIXTURES / "idle.txt")]), 0)

    def test_filtered_dump_runs(self):
        self.assertEqual(canlog.main(["--dump", "--id", "0x480", str(FIXTURES / "idle.txt")]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
