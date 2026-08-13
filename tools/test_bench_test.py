"""Tests for bench_test.py and bench_scenarios.py.

Nothing here touches a serial port. Three properties are worth pinning without
hardware, and the third is the one that matters.

**The wire format round trips.** What goes onto the bench bus has to parse back
through canlog.py into the frame it came from.

**The 0x603 decoder agrees with the firmware that fills it in.**
bench_test.decode_diag() and txframes_diag() in src/txframes.c are twins, the
way tools/test_replay.py and test/test_compute.c are: same layout, two
languages, and a change belongs in both.

**A patched frame says what it was patched to say** -- checked with
tools/replay.py's decoder, which is an independent implementation written
against the same recordings rather than against bench_scenarios. If a scenario
asks for 60 km/h and the converter is really being told 12 km/h, every
assertion downstream is meaningless and nothing else here would notice.
"""

import unittest
from pathlib import Path

import bench_scenarios as bs
import bench_test as bt
import canlog
import replay

FIXTURES = Path(__file__).resolve().parents[1] / "test" / "fixtures"
LOG = FIXTURES / "09_idle_60s_z1.txt"


class TestSlcanTx(unittest.TestCase):
    def test_matches_the_documented_wire_format(self):
        self.assertEqual(bt.slcan_tx(0x480, bytes.fromhex("8fffffff8dffffff")),
                         b"t4808" + b"8FFFFFFF8DFFFFFF")

    def test_short_and_empty_frames(self):
        self.assertEqual(bt.slcan_tx(0x1A0, b"\x01\x02"), b"t1A020102")
        self.assertEqual(bt.slcan_tx(0x000, b""), b"t0000")

    def test_rejects_an_extended_identifier(self):
        with self.assertRaises(ValueError):
            bt.slcan_tx(0x800, b"\x00")

    def test_rejects_more_than_eight_bytes(self):
        with self.assertRaises(ValueError):
            bt.slcan_tx(0x100, bytes(9))


class TestRoundTrip(unittest.TestCase):
    def _round_trip(self, path):
        frames = canlog.parse_file(path, fix_doubled=True)
        self.assertGreater(len(frames), 0)
        for frame in frames:
            line = bt.slcan_tx(frame.can_id, frame.data).decode()
            back = canlog.parse_line(line)
            self.assertIsNotNone(back, f"canlog could not read back {line!r}")
            self.assertEqual(back.can_id, frame.can_id)
            self.assertEqual(back.data, frame.data)

    def test_a_timestamped_fixture(self):
        self._round_trip(FIXTURES / "10_rev2600_z1.txt")

    def test_an_untimed_fixture(self):
        self._round_trip(FIXTURES / "01_ign_only.txt")


class TestDiagDecode(unittest.TestCase):
    def test_matches_the_layout_the_firmware_writes(self):
        # b0 rx, b1 tx, b2 COMSTAT, b3 flags, b4 cause|version<<5,
        # b5 refusals, b6-7 uptime. Version 1 with WATCHDOG (0x04) is 0x24.
        got = bt.decode_diag(bytes([0x11, 0x22, 0x33, 0x1F,
                                    0x24, 0x44, 0x55, 0x66]))
        self.assertEqual(got["rx_err"], 0x11)
        self.assertEqual(got["tx_err"], 0x22)
        self.assertEqual(got["comstat"], 0x33)
        self.assertEqual(got["flags"], 0x1F)
        self.assertEqual(got["reset_cause"], 0x04)
        self.assertEqual(got["version"], bt.DIAG_LAYOUT_VERSION)
        self.assertEqual(got["tx_fail"], 0x44)
        self.assertEqual(got["uptime_s"], 0x5566)

    def test_a_clean_converter(self):
        got = bt.decode_diag(bytes([0, 0, 0, 0x19, 0x20, 0, 0, 42]))
        self.assertEqual(got["comstat"], 0)
        self.assertEqual(got["reset_cause"], 0)      # an MCLR reset
        self.assertEqual(got["uptime_s"], 42)

    def test_every_reset_cause_survives_the_shared_byte(self):
        for bit, _name in bt.RESET_CAUSES:
            packed = bit | (bt.DIAG_LAYOUT_VERSION << bt.DIAG_VERSION_SHIFT)
            got = bt.decode_diag(bytes([0, 0, 0, 0, packed, 0, 0, 0]))
            self.assertEqual(got["reset_cause"], bit)
            self.assertEqual(got["version"], bt.DIAG_LAYOUT_VERSION)

    def test_a_short_frame_is_an_error_not_a_guess(self):
        with self.assertRaises(ValueError):
            bt.decode_diag(bytes(7))


class TestNames(unittest.TestCase):
    def test_no_bits_reads_as_none_rather_than_blank(self):
        self.assertEqual(bt.names(0, bt.RESET_CAUSES), "none")

    def test_several_bits_are_all_listed(self):
        got = bt.names(0x01 | 0x08, bt.DIAG_FLAGS)
        self.assertIn("CAN_OK", got)
        self.assertIn("DATA_LIVE", got)
        self.assertNotIn("SILENT", got)


class TestPatching(unittest.TestCase):
    """A patched frame must decode, independently, to what was asked for."""

    def setUp(self):
        self.tpl = bs.templates(LOG)

    def _decode(self, frames):
        st = replay.Decoded()
        for can_id, data in frames:
            replay.decode(canlog.Frame(None, can_id, data), st)
        return st

    def test_speed_arrives_as_the_speed_that_was_asked_for(self):
        for kmh in (0.005, 2, 5, 50, 60, 180):
            cond = bs.Condition(speed_kmh=kmh)
            st = self._decode(bs.frames_for(self.tpl, cond, 1000))
            self.assertTrue(st.speed_valid, f"{kmh} km/h decoded as invalid")
            # One raw bit is 0.005 km/h, so the round trip quantises to that.
            self.assertAlmostEqual(st.speed_kmh, cond.speed_kmh, delta=0.005)

    def test_an_invalid_speed_really_reads_invalid(self):
        st = self._decode(bs.frames_for(
            self.tpl, bs.Condition(speed_kmh=50, speed_valid=False), 1000))
        self.assertFalse(st.speed_valid)

    def test_the_gate_bits_are_set_the_way_decode_wants_them(self):
        frames = dict((i, d) for i, d in
                      bs.frames_for(self.tpl, bs.Condition(speed_kmh=50), 1))
        b1 = frames[bs.ID_SPEED][1]
        self.assertTrue(b1 & bs.SPEED_GATE_REQUIRED)
        self.assertFalse(b1 & bs.SPEED_GATE_FORBIDDEN)

    def test_rpm_throttle_and_torque_arrive_intact(self):
        cond = bs.Condition(rpm=2600, throttle=91, torque_b7=133)
        st = self._decode(bs.frames_for(self.tpl, cond, 1000))
        self.assertEqual(st.rpm, 2600)
        self.assertEqual(st.throttle, 91)
        # replay.py scales b7 by TORQUE_CNM_PER_BIT, so 133 comes back in Nm.
        self.assertAlmostEqual(st.torque_ind_nm, 133 * 0.74, delta=0.01)

    def test_the_tank_level_survives_the_reserve_lamp_bit(self):
        for litres in (0, 7, 40, 63):
            st = self._decode(bs.frames_for(
                self.tpl, bs.Condition(tank_l=litres), 1000))
            self.assertEqual(st.tank_l, litres)

    def test_the_counter_is_masked_to_fifteen_bits(self):
        st = self._decode(bs.frames_for(self.tpl, bs.Condition(), 0x9234))
        self.assertEqual(st.fuel_counter, 0x9234 & 0x7FFF)

    def test_every_patched_frame_is_still_eight_bytes(self):
        for _id, data in bs.frames_for(self.tpl, bs.Condition(), 1):
            self.assertEqual(len(data), 8)

    def test_only_accepted_identifiers_are_generated(self):
        ids = {i for i, _d in bs.frames_for(self.tpl, bs.Condition(), 1)}
        self.assertTrue(ids <= bt.ACCEPTED_IDS, ids - bt.ACCEPTED_IDS)


class TestStream(unittest.TestCase):
    def test_the_counter_advances_at_the_requested_flow(self):
        stream = bs.Stream(bs.templates(LOG),
                           bs.Condition(flow_ul_s=1000))
        start = stream.counter
        for _ in range(100):            # 100 ticks of 10 ms = one second
            stream.tick()
        self.assertAlmostEqual(stream.counter - start, 1000, delta=2)

    def test_a_slow_flow_still_accumulates_rather_than_truncating(self):
        # 30 ul/s is 0.3 per tick. Truncating each tick would give zero for
        # ever, which is exactly the fault DIST_TICK_MS exists to avoid on the
        # other side of the arithmetic.
        stream = bs.Stream(bs.templates(LOG), bs.Condition(flow_ul_s=30))
        start = stream.counter
        for _ in range(100):
            stream.tick()
        self.assertAlmostEqual(stream.counter - start, 30, delta=2)

    def test_restart_puts_the_counter_back_to_zero(self):
        stream = bs.Stream(bs.templates(LOG), bs.Condition())
        for _ in range(50):
            stream.tick()
        stream.restart()
        self.assertEqual(stream.counter, 0)


class TestExpectedFuelNow(unittest.TestCase):
    """The two identities the scenarios assert against."""

    def test_below_four_kmh_it_is_litres_per_hour(self):
        # 1000 ul/s is 3.6 l/h, and the field is tenths.
        self.assertEqual(
            bs.Condition(speed_kmh=2, flow_ul_s=1000).fuel_now_d(), 36)

    def test_above_four_kmh_it_is_litres_per_hundred_km(self):
        # One microlitre per metre is exactly 0.1 l/100 km. At 60 km/h,
        # 1000 ul/s is 60 ul/m, so 6.0 l/100 km.
        self.assertEqual(
            bs.Condition(speed_kmh=60, flow_ul_s=1000).fuel_now_d(), 60)

    def test_the_clamp_is_the_gauge_and_not_a_wrap(self):
        got = bs.Condition(speed_kmh=5, flow_ul_s=3000).fuel_now_d()
        self.assertEqual(got, 999)

    def test_the_unit_switches_at_four_kmh_and_not_elsewhere(self):
        slow = bs.Condition(speed_kmh=3.9, flow_ul_s=1000).fuel_now_d()
        fast = bs.Condition(speed_kmh=4.0, flow_ul_s=1000).fuel_now_d()
        self.assertEqual(slow, 36)                  # l/h
        self.assertEqual(fast, 900)                 # l/100 km


class TestReplaySelection(unittest.TestCase):
    def test_only_the_accepted_identifiers_are_replayed_by_default(self):
        frames, _off, _timed = bt.replay_frames(LOG, every_id=False)
        self.assertTrue(frames)
        self.assertTrue(all(f.can_id in bt.ACCEPTED_IDS for f in frames))

    def test_all_ids_keeps_more_than_the_six(self):
        few, _o, _t = bt.replay_frames(LOG, False)
        many, _o, _t = bt.replay_frames(LOG, True)
        self.assertGreater(len(many), len(few))

    def test_offsets_start_at_zero_and_never_go_back(self):
        for path in sorted(FIXTURES.glob("*.txt")):
            _frames, offsets, _timed = bt.replay_frames(path, every_id=True)
            self.assertEqual(offsets[0], 0, f"{path.name}")
            self.assertEqual(offsets, sorted(offsets), f"{path.name}")

    def test_the_flooded_identifier_is_one_we_do_not_accept(self):
        self.assertNotIn(bt.UNACCEPTED_ID, bt.ACCEPTED_IDS)


if __name__ == "__main__":
    unittest.main()
