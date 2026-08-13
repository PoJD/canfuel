"""Tests for bench_test.py.

Two properties matter here and neither is about the serial port.

**The wire format must round trip.** What this script puts on the bus has to
parse back, through canlog.py, into the frame it came from. A transposed nibble
would put plausible traffic on the bench bus and the converter would decode
nonsense from it with nothing looking broken.

**The 0x603 decoder must agree with the firmware that fills it in.**
decode_diag() here and txframes_diag() in src/txframes.c are twins, the same
way tools/test_replay.py and test/test_compute.c are: same layout, two
languages, and a change belongs in both. The byte string in
test_matches_the_layout_the_firmware_writes is the same one
test/test_txframes.c builds from the other side.
"""

import unittest
from pathlib import Path

import bench_test as bt
import canlog

FIXTURES = Path(__file__).resolve().parents[1] / "test" / "fixtures"


class TestSlcanTx(unittest.TestCase):
    def test_matches_the_documented_wire_format(self):
        # t, three hex digits of identifier, one of DLC, then the bytes.
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
        # b5 refusals, b6-7 uptime. Version 1 with cause WATCHDOG (0x04)
        # packs to 0x24.
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
        self.assertEqual(got["rx_err"], 0)
        self.assertEqual(got["tx_err"], 0)
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


class TestReplaySelection(unittest.TestCase):
    def test_only_the_accepted_identifiers_are_replayed_by_default(self):
        frames, _off, _timed = bt.replay_frames(FIXTURES / "09_idle_60s_z1.txt",
                                                every_id=False)
        self.assertTrue(frames)
        self.assertTrue(all(f.can_id in bt.ACCEPTED_IDS for f in frames))

    def test_all_ids_keeps_more_than_the_six(self):
        few, _o, _t = bt.replay_frames(FIXTURES / "09_idle_60s_z1.txt", False)
        many, _o, _t = bt.replay_frames(FIXTURES / "09_idle_60s_z1.txt", True)
        self.assertGreater(len(many), len(few))

    def test_offsets_start_at_zero_and_never_go_back(self):
        for path in sorted(FIXTURES.glob("*.txt")):
            _frames, offsets, _timed = bt.replay_frames(path, every_id=True)
            self.assertEqual(offsets[0], 0, f"{path.name}")
            self.assertEqual(offsets, sorted(offsets), f"{path.name}")


if __name__ == "__main__":
    unittest.main()
