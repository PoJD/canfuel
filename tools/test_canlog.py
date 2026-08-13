#!/usr/bin/env python3
"""Tests for canlog.py -- both log formats plus anchors against real fixtures.

Running them:
    python -m unittest discover -s tools -p 'test_*.py' -v
    python tools/test_canlog.py

There are two goals here. One is checking the parser itself. The other is
pinning down a handful of values read out of the real logs. If the fixtures
were ever re-encoded or swapped, these tests catch it before anyone tunes
firmware against them.

Every number below was measured from these specific files, not copied from
the specification. Where measurement and specification disagree it is noted
at the test and in docs/can-decoding.md.
"""

from __future__ import annotations

import statistics
import unittest
from pathlib import Path

import canlog
from canlog import Frame, LogFormatError, parse_file, parse_line, undouble

FIXTURES = Path(__file__).resolve().parent.parent / "test" / "fixtures"

# Period of frame 0x480. For logs without timestamps this is the only way to
# turn the counter into a rate, so every absolute value below hangs off it.
PERIOD_0X480_S = 0.0495


def u16le(data: bytes, i: int) -> int:
    return data[i] | data[i + 1] << 8


class TestParseLineSlcan(unittest.TestCase):
    """Format A -- raw slcan stream."""

    def test_standard_frame(self):
        f = parse_line("t1a0800400100fefe001d")
        self.assertEqual(f.can_id, 0x1A0)
        self.assertEqual(f.dlc, 8)
        self.assertEqual(f.data, bytes.fromhex("00400100fefe001d"))
        self.assertIsNone(f.ts_ms)

    def test_adapter_timestamp(self):
        """Opened with Z1 the USBtin appends four hex digits of milliseconds.

        The five oldest fixtures have none -- they were recorded with
        timestamping off -- but the `_z1` recordings that resolved questions 1
        and 9 do, and it is the adapter's own clock rather than the host's.
        """
        f = parse_line("t1a0800400100fefe001d2a3f")
        self.assertEqual(f.can_id, 0x1A0)
        self.assertEqual(f.data, bytes.fromhex("00400100fefe001d"))
        self.assertEqual(f.ts_ms, 0x2A3F)

    def test_adapter_timestamp_on_a_short_frame(self):
        f = parse_line("t5d060003490900321234")
        self.assertEqual(f.can_id, 0x5D0)
        self.assertEqual(f.dlc, 6)
        self.assertEqual(f.ts_ms, 0x1234)

    def test_a_truncated_timestamp_is_an_error(self):
        # Silently ignoring a partial tail would hand the caller a frame with
        # no time on a recording made specifically to have one.
        with self.assertRaises(LogFormatError):
            parse_line("t1a0800400100fefe001d2a3")

    def test_short_dlc(self):
        # 0x5D0 arrives with DLC 6, not 8 -- the classic trap for a parser
        # that assumes a fixed length.
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
    """Format B -- TSV export from USBtinViewer."""

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
        """The tab tells the formats apart; slcan never contains one."""
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
            self.assertTrue((FIXTURES / name).is_file(), f"missing fixture {name}")


class TestFixtureContent(unittest.TestCase):
    """Anchors against the real logs. Every value measured from these files."""

    @classmethod
    def setUpClass(cls):
        cls.frames = {p.name: parse_file(p) for p in FIXTURES.glob("*.txt")}

    # -- IDs on the bus -----------------------------------------------------

    REGULAR_IDS = {0x050, 0x0C2, 0x1A0, 0x280, 0x288, 0x320,
                   0x420, 0x480, 0x488, 0x4A0, 0x520, 0x5A0, 0x5D0, 0x5D8}

    def test_regular_id_set(self):
        """Exactly 14 IDs are broadcast periodically -- see docs/can-decoding.md.

        Exception: 0x520 is slow enough that it misses short logs.
        """
        for name, frames in self.frames.items():
            seen = {f.can_id for f in frames}
            unexpected = seen - self.REGULAR_IDS - {0x767}
            self.assertEqual(unexpected, set(), f"{name}: unknown IDs")
            self.assertTrue(seen >= self.REGULAR_IDS - {0x520},
                            f"{name}: missing IDs {self.REGULAR_IDS - seen}")

    def test_0x767_is_a_one_off(self):
        """0x767 appears exactly once, in 06, on the first timestamp, DLC 2.

        It is not a periodic bus frame but a one-shot diagnostic response
        captured as the USBtin connected. Firmware should ignore it, but the
        0x7xx range can no longer be called completely quiet because of it.
        """
        hits = [(n, f) for n, fr in self.frames.items() for f in fr if f.can_id == 0x767]
        self.assertEqual(len(hits), 1)
        name, frame = hits[0]
        self.assertEqual(name, "06_trip_reset.txt")
        self.assertEqual(frame.ts_ms, 2000)
        self.assertEqual(frame.data, bytes.fromhex("3cfe"))

    def test_target_ids_are_free(self):
        """0x600-0x602 must not be on the bus -- the converter wants them."""
        for name, frames in self.frames.items():
            collisions = {f.can_id for f in frames if 0x600 <= f.can_id <= 0x602}
            self.assertEqual(collisions, set(), f"{name}: IDs already taken")

    def test_dlc_is_stable_per_id(self):
        """Each ID keeps one length throughout; 0x050 has 4, 0x5D0 has 6."""
        for name, frames in self.frames.items():
            per_id: dict[int, set[int]] = {}
            for f in frames:
                per_id.setdefault(f.can_id, set()).add(f.dlc)
            for can_id, dlcs in per_id.items():
                self.assertEqual(len(dlcs), 1, f"{name}: 0x{can_id:03X} has DLC {dlcs}")
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
            self.assertEqual(ts, sorted(ts), f"{name}: timestamps are not monotonic")

    def test_frame_counts(self):
        counts = {name: len(fr) for name, fr in self.frames.items()}
        self.assertEqual(counts["01_ign_only.txt"], 3402)
        self.assertEqual(counts["02_idle_60s.txt"], 89882)
        self.assertEqual(counts["03_drive.txt"], 18018)
        self.assertEqual(counts["05_rev3000.txt"], 1522)
        self.assertEqual(counts["06_trip_reset.txt"], 99101)
        self.assertEqual(counts["07_accel.txt"], 11188)
        self.assertEqual(counts["idle.txt"], 1136)

    # -- decoded signals ----------------------------------------------------

    def rpm(self, name):
        return [u16le(f.data, 2) * 0.25 for f in self.frames[name] if f.can_id == 0x280]

    def counter(self, name):
        return [u16le(f.data, 2) & 0x7FFF for f in self.frames[name] if f.can_id == 0x480]

    def test_ign_only_engine_is_off(self):
        """01_ign_only: the engine is not running, so rpm and counter are hard zeros."""
        self.assertTrue(all(r == 0 for r in self.rpm("01_ign_only.txt")))
        self.assertEqual(set(self.counter("01_ign_only.txt")), {0})

    def test_idle_rpm(self):
        """02 is a warm idle at 797 rpm, exactly as the specification says."""
        self.assertAlmostEqual(statistics.median(self.rpm("02_idle_60s.txt")), 797, delta=1)

    def test_rev3000_rpm(self):
        """05 is 2940 rpm in neutral -- the second calibration point for drag torque."""
        self.assertAlmostEqual(statistics.median(self.rpm("05_rev3000.txt")), 2940, delta=2)

    def test_clt_warmup_curve(self):
        """Coolant temperature rises across the session: idle 68 -> 05 90 -> 03 99 -> 01 100.5."""
        def clt(name):
            vals = [f.data[1] * 0.75 - 48 for f in self.frames[name] if f.can_id == 0x288]
            return statistics.median(vals)
        self.assertAlmostEqual(clt("idle.txt"), 68.25, places=2)
        self.assertAlmostEqual(clt("05_rev3000.txt"), 90.00, places=2)
        self.assertAlmostEqual(clt("03_drive.txt"), 99.00, places=2)
        self.assertAlmostEqual(clt("01_ign_only.txt"), 100.50, places=2)

    def test_counter_bit15_is_a_sticky_wrap_flag(self):
        """Bit 15 is NOT constantly 1, contrary to what docs/sensors.md claims.

        Measured across every log: bit 15 stays zero from ignition on until the
        15-bit counter first wraps, and is then permanently one.
        - 01_ign_only: engine off, counter zero -> bit 15 is zero.
        - 06_trip_reset: starts at zero, flips when 32767 -> 15 wraps.
        - all other logs: engine has run a while, already wrapped -> one.

        It makes no difference to the arithmetic, the 0x7FFF mask drops it.
        It is usable as a "this ignition cycle is still young" flag.

        02_idle_60s is excluded because it is doubled (see below) and the
        second copy appears to reset the flag back to zero.
        """
        for name, frames in self.frames.items():
            if name == "02_idle_60s.txt":
                continue
            b15 = [(f.data[3] >> 7) & 1 for f in frames if f.can_id == 0x480]
            if 1 in b15:
                first = b15.index(1)
                self.assertTrue(all(b == 1 for b in b15[first:]), f"{name}: bit 15 is not sticky")

    def test_counter_masked_to_15_bits(self):
        for name, frames in self.frames.items():
            masked = [u16le(f.data, 2) & 0x7FFF for f in frames if f.can_id == 0x480]
            self.assertTrue(all(0 <= v < 32768 for v in masked), name)

    def test_counter_only_moves_forward(self):
        """The delta is (new - old) mod 32768 and must never come out negative."""
        for name in self.frames:
            vals = self.counter(name)
            deltas = [(b - a) % 32768 for a, b in zip(vals, vals[1:])]
            # A jump past half the range would mean we missed a wrap, or that
            # the counter reset after the ignition was switched off.
            big = [d for d in deltas if d > 16384]
            self.assertEqual(big, [], f"{name}: suspicious deltas {big[:5]}")

    def test_accel_counter_span(self):
        """07_accel is timestamped, so it is the only fixture from which an
        absolute flow rate follows without assuming a frame period.

        The specification (BOOTSTRAP section 3) quotes 13247 -> 22622 over
        15.9 s. The end matches, the start does not -- the first sample in the
        file is 12870. The difference of 377 ul is a handful of early frames.
        See docs/can-decoding.md, question 2 -- resolved, and confirmed exactly.
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
        """Byte 1 of frame 0x1A0 is a bit field, not a single value.

        The specification (BOOTSTRAP section 3) says "valid only when
        b1 == 0x40". That is too strict. States measured across the logs:

            0x40  base valid state
            0x48  also valid -- in 07_accel it is the majority (1301/1991)
                  and carries the full speed range including the 24.78 km/h peak
            0x50  also valid, 11-15 km/h
            0x43  post-ignition init ramp -> discard
            0x42  same thing, only 2 frames

        Testing for equality with 0x40 would throw away two thirds of the speed
        samples in 07_accel and distance would come out as 14 m instead of 27 m.
        That would directly corrupt FuelAvg and Range. The correct rule is
        (b1 & 0x40) && !(b1 & 0x03).
        """
        frames = [f for f in self.frames["07_accel.txt"] if f.can_id == 0x1A0]
        gates = {f.data[1] for f in frames}
        self.assertEqual(gates, {0x40, 0x48, 0x50})

        def speeds(gate):
            return [u16le(f.data, 2) * 0.005 for f in frames if f.data[1] == gate]

        # 0x48 is not a fringe state and carries the same speeds as 0x40
        self.assertGreater(len(speeds(0x48)), len(speeds(0x40)))
        self.assertAlmostEqual(max(speeds(0x48)), 24.70, places=2)
        self.assertAlmostEqual(max(speeds(0x40)), 24.78, places=2)

    def test_init_ramp_only_after_ignition_on(self):
        """0x43 appears only after ignition on. 0x42 also happens while driving.

        The original claim covered both values and 17_drive_property_z1.txt
        disproved half of it: 0x42 turns up 134 times mid-drive, at 26 km/h,
        with nothing resembling an ignition event anywhere near it. What it
        marks there is the speed value freezing -- the raw word stops updating
        and repeats the last one -- which the low-bit gate rejects exactly as
        it rejects the ramp. So the decoder was always right and only this
        test's story about *when* the state can occur was too narrow.

        0x43 does still look specific to the ignition ramp: it appears in the
        two logs that start with the key being turned and in no other, across
        seventeen recordings and some 112,000 frames of 0x1A0.
        """
        ignition_on = ("01_ign_only.txt", "06_trip_reset.txt")
        for name, frames in self.frames.items():
            gates = {f.data[1] for f in frames if f.can_id == 0x1A0}
            if name in ignition_on:
                self.assertEqual(gates & {0x42, 0x43}, {0x42, 0x43}, name)
            else:
                self.assertNotIn(0x43, gates, f"{name}: unexpected ramp 0x43")

    def test_the_gate_rejects_every_state_that_freezes_the_value(self):
        """Every b1 state with a low bit set is one the gate must throw away.

        This is trap 1 from the other side: rather than listing the states seen
        so far, it asserts the property they share, so a new one arriving in a
        future recording is caught rather than silently accepted.
        """
        for name, frames in self.frames.items():
            for f in (f for f in frames if f.can_id == 0x1A0):
                valid = (f.data[1] & 0x40) != 0 and (f.data[1] & 0x03) == 0
                self.assertEqual(valid, f.data[1] in (0x40, 0x48, 0x50),
                                 f"{name}: unhandled 0x1A0 state {f.data[1]:#04x}")

    def test_valid_speed_is_in_range(self):
        for name, frames in self.frames.items():
            valid = [u16le(f.data, 2) * 0.005 for f in frames
                     if f.can_id == 0x1A0 and (f.data[1] & 0x40) and not (f.data[1] & 0x03)]
            self.assertTrue(valid, name)
            self.assertLess(max(valid), 200.0, name)

    def test_tank_reserve_bit(self):
        """The tank reads 0 l with the reserve lamp on -- byte 2 of 0x320 is exactly 0x80."""
        for name in ("01_ign_only.txt", "03_drive.txt", "05_rev3000.txt"):
            vals = {f.data[2] for f in self.frames[name] if f.can_id == 0x320}
            self.assertEqual(vals, {0x80}, name)

    def test_no_lambda_on_0x488(self):
        """0x488 is constant, there is no lambda on the bus."""
        for name, frames in self.frames.items():
            payloads = {f.data for f in frames if f.can_id == 0x488}
            self.assertEqual(payloads, {bytes.fromhex("ffffff8dffffffff")}, name)


class TestDoubledFixture(unittest.TestCase):
    """02_idle_60s.txt contains the recording exactly twice.

    This is not a theory -- the two halves of the file match line for line.
    We keep it in the repo the way it came out of the USBtin and correct it at
    read time, so the original measurement is never rewritten. If the file were
    ever replaced with a cleaned version, this test would fail and say so.
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
            self.assertEqual(undouble(lines), lines, f"{path.name} is doubled as well")

    def test_undouble_is_idempotent(self):
        once = undouble(self.lines("02_idle_60s.txt"))
        self.assertEqual(len(once), 44941)
        self.assertEqual(undouble(once), once)

    def test_undouble_leaves_normal_input_alone(self):
        self.assertEqual(undouble(["a", "b", "c"]), ["a", "b", "c"])
        self.assertEqual(undouble([]), [])
        # Two identical lines in a row do not yet make a doubled file, but the
        # two cases cannot be told apart -- which is why undouble is only ever
        # applied to a whole log.
        self.assertEqual(undouble(["a", "a"]), ["a"])

    def test_parse_file_fix_doubled(self):
        raw = parse_file(FIXTURES / "02_idle_60s.txt")
        fixed = parse_file(FIXTURES / "02_idle_60s.txt", fix_doubled=True)
        self.assertEqual(len(fixed) * 2, len(raw))


class TestFuelRates(unittest.TestCase):
    """Absolute flow rates. Logs without timestamps rest on the 0x480 period."""

    def counter_total(self, name, *, fix_doubled=False):
        frames = parse_file(FIXTURES / name, fix_doubled=fix_doubled)
        vals = [u16le(f.data, 2) & 0x7FFF for f in frames if f.can_id == 0x480]
        total = sum((b - a) % 32768 for a, b in zip(vals, vals[1:]))
        return total, len(vals), frames

    def test_idle_flow_matches_specification(self):
        """Warm idle at 797 rpm -> 310 ul/s = 1.12 l/h.

        It lands on the decimal, but only for the de-duplicated file. Without
        the fix the rate doubles and the whole fuel calculation is off by 100 %.
        """
        total, n, _ = self.counter_total("02_idle_60s.txt", fix_doubled=True)
        self.assertEqual(n, 1216)
        self.assertEqual(total, 18652)
        span_s = (n - 1) * PERIOD_0X480_S
        self.assertAlmostEqual(span_s, 60.1, places=1)
        self.assertAlmostEqual(total / span_s, 310, delta=2)

    def test_rev3000_flow(self):
        """2940 rpm in neutral. The specification says 958 ul/s, the data gives 1005.

        The 5 % gap is not in the data but in the assumed 0x480 period -- at
        51.9 ms it would come out at exactly 958. The log has no timestamps, so
        only a measurement on the live bus can settle it. See docs/can-decoding.md.
        """
        total, n, _ = self.counter_total("05_rev3000.txt")
        self.assertEqual(total, 1940)
        rate = total / ((n - 1) * PERIOD_0X480_S)
        self.assertAlmostEqual(rate, 1005, delta=5)

    def test_ign_only_burns_nothing(self):
        total, _, _ = self.counter_total("01_ign_only.txt")
        self.assertEqual(total, 0)

    def test_timestamped_logs_need_no_period_assumption(self):
        """06 and 07 are stamped, so they are the only logs with a hard rate."""
        for name, expect_ul, expect_s in (("06_trip_reset.txt", 51992, 134.979),
                                          ("07_accel.txt", 9752, 15.915)):
            total, _, frames = self.counter_total(name)
            ts = [f.ts_ms for f in frames if f.can_id == 0x480]
            self.assertEqual(total, expect_ul, name)
            self.assertAlmostEqual((ts[-1] - ts[0]) / 1000, expect_s, places=3)


class TestTimestampWrap(unittest.TestCase):
    """The USBtin's Z1 counter restarts; the host's timestamps do not.

    The wrap value was measured off a real capture -- the
    counter reaches 60000 and the next frame reads 0. See TIMESTAMP_WRAP_MS.
    """

    def test_monotonic_input_is_untouched(self):
        values = [10, 20, 30, 59999, 60000]
        self.assertEqual(canlog.unwrap_timestamps(values), values)

    def test_host_timestamps_past_60000_do_not_trigger_a_wrap(self):
        """07_accel runs 48399 -> 64314 without wrapping. Format B counts on.

        This is the case that made unwrapping worth a function rather than a
        modulo: a blind `% 60001` would fold this recording in half.
        """
        values = [48399, 59000, 60000, 61000, 64314]
        self.assertEqual(canlog.unwrap_timestamps(values), values)

    def test_a_wrap_is_carried_forward(self):
        wrapped = [59996, 60000, 0, 1, 2]
        self.assertEqual(canlog.unwrap_timestamps(wrapped),
                         [59996, 60000, 60001, 60002, 60003])

    def test_two_wraps_accumulate(self):
        values = [60000, 0, 60000, 0]
        got = canlog.unwrap_timestamps(values)
        self.assertEqual(got, [60000, 60001, 120001, 120002])

    def test_gap_across_the_wrap_is_one_millisecond(self):
        """60000 -> 0 is one tick, not a 60-second jump backwards."""
        run = canlog.unwrap_timestamps([60000, 0])
        self.assertEqual(run[1] - run[0], 1)

    def test_real_capture_spans_the_right_wall_clock(self):
        """07_accel's own numbers, as an end-to-end check of the helper."""
        frames = canlog.parse_file(str(FIXTURES / "07_accel.txt"))
        stamped = [f.ts_ms for f in frames if f.ts_ms is not None]
        run = canlog.unwrap_timestamps(stamped)
        self.assertAlmostEqual((run[-1] - run[0]) / 1000, 15.915, places=3)


class TestCli(unittest.TestCase):
    def test_summary_runs(self):
        self.assertEqual(canlog.main([str(FIXTURES / "idle.txt")]), 0)

    def test_filtered_dump_runs(self):
        self.assertEqual(canlog.main(["--dump", "--id", "0x480", str(FIXTURES / "idle.txt")]), 0)

    def test_gaps_runs_on_a_timestamped_log(self):
        self.assertEqual(
            canlog.main(["--gaps", "--id", "0x480", str(FIXTURES / "07_accel.txt")]), 0)

    def test_gaps_on_an_unstamped_log_says_so_rather_than_inventing_times(self):
        self.assertEqual(canlog.main(["--gaps", str(FIXTURES / "idle.txt")]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
