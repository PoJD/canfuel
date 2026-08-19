#!/usr/bin/env python3
"""tools/flash.py against IPECMD's real output.

Every string in here was printed by IPECMD driving a PICkit 3 against the
board, or -- for the two failures nobody wants to reproduce on purpose -- was
provoked deliberately and recorded in docs/flash-tool-notes.md. That is the
point of the file: the tool's whole verdict comes from parsing this text, so
the text is what it has to be tested against, and it needs no programmer to
run.

Nothing here touches a device.
"""

import re
import unittest
from pathlib import Path

import flash

# --- observed, on a powered board with the PICkit on J3 ---------------------

IDENTIFY_OK = """DFP Version Used : PIC18F-K_DFP,1.5.114,Microchip
*****************************************************
Connecting to MPLAB PICkit 3...
Currently loaded firmware on PICkit 3
Firmware Suite Version.....01.56.09
Firmware type..............PIC18F
Target voltage detected
Target device PIC18F25K80 found.
Device Revision ID = 6
Target device PIC18F25K80 found.
Device Revision ID = 6
Operation Succeeded
"""

BLANK_CHECK_BLANK = """Target voltage detected
Target device PIC18F25K80 found.
Device Revision ID = 6
Blank Checking...
Blank check complete, device is blank.
Operation Succeeded
"""

PROGRAM_OK = """Target voltage detected
Target device PIC18F25K80 found.
Device Revision ID = 6
Device Erased...
Programming...
The following memory area(s) will be programmed:
program memory: start address = 0x0, end address = 0x44ff
configuration memory
Programming/Verify complete
PICKIT3 Program Report
Device Type:PIC18F25K80
Program Succeeded.
Operation Succeeded
"""

# -Y on a board that was just programmed, released from reset, and has stored a
# persist record. It verifies EEData against a hex with no EEPROM section, so
# slot 0 is a mismatch. A perfect board fails this.
VERIFY_EEDATA_FAILS = """Target voltage detected
Target device PIC18F25K80 found.
Device Revision ID = 6
PK3 Verify Report
Device Type:PIC18F25K80
The following memory areas(s) will be verified:
program memory: start address = 0x0, end address = 0x7fff
configuration memory
EEData memory
User Id Memory
EEData memory
Address: 0 Expected Value: ff Received Value: 0
Verify failed
"""

# --- provoked deliberately, see flash-tool-notes.md ------------------------

UNPOWERED = """Connecting to MPLAB PICkit 3...
Target device was not found (could not detect target voltage VDD).
Operation Succeeded
"""

ICSP_SILENT = """Target voltage detected
Target Device ID (0x0) is an Invalid Device ID. Please check your connections to the Target Device.
Operation Failed
"""

NO_PROGRAMMER = """DFP Version Used : PIC18F-K_DFP,1.5.114,Microchip
Programmer not found.
"""


def ihex(records):
    """Build an Intel HEX file out of (type, address, bytes) triples."""
    out = []
    for rtype, addr, data in records:
        body = [len(data), (addr >> 8) & 0xFF, addr & 0xFF, rtype] + list(data)
        checksum = (-sum(body)) & 0xFF
        out.append(":" + "".join("%02X" % b for b in body + [checksum]))
    out.append(":00000001FF")
    return "\n".join(out) + "\n"


class TestIdentify(unittest.TestCase):
    def test_real_success(self):
        ok, detail = flash.parse_identify(IDENTIFY_OK)
        self.assertTrue(ok)
        self.assertIn("revision 6", detail)
        self.assertIn("powered from the board", detail)

    def test_unpowered_is_a_failure_despite_operation_succeeded(self):
        # The one case the exit code gets wrong: this run exits 0.
        self.assertIn("Operation Succeeded", UNPOWERED)
        ok, detail = flash.parse_identify(UNPOWERED)
        self.assertFalse(ok)
        self.assertIn("not powered", detail)

    def test_icsp_silent(self):
        ok, detail = flash.parse_identify(ICSP_SILENT)
        self.assertFalse(ok)
        self.assertIn("JP2", detail)

    def test_no_programmer(self):
        ok, detail = flash.parse_identify(NO_PROGRAMMER)
        self.assertFalse(ok)
        self.assertIn("no programmer", detail)

    def test_a_different_part_answering_is_not_a_pass(self):
        ok, _ = flash.parse_identify(IDENTIFY_OK.replace("25K80", "26K80"))
        self.assertFalse(ok)


class TestBlankCheck(unittest.TestCase):
    def test_blank(self):
        blank, detail = flash.parse_blank_check(BLANK_CHECK_BLANK)
        self.assertTrue(blank)
        self.assertEqual(detail, "blank")

    def test_unpowered(self):
        blank, detail = flash.parse_blank_check(UNPOWERED)
        self.assertFalse(blank)
        self.assertIn("not powered", detail)


class TestProgram(unittest.TestCase):
    def test_real_success(self):
        ok, detail = flash.parse_program(PROGRAM_OK)
        self.assertTrue(ok)
        self.assertIn("implicitly verified", detail)

    def test_verify_failed_is_a_failure(self):
        ok, detail = flash.parse_program(VERIFY_EEDATA_FAILS)
        self.assertFalse(ok)
        self.assertIn("Verify failed", detail)

    def test_unpowered(self):
        ok, detail = flash.parse_program(UNPOWERED)
        self.assertFalse(ok)
        self.assertIn("not powered", detail)


# --- a real -GE0-400 dump, off the board -------------------------------------
#
# tools/testdata/ipecmd-ge0-400.txt is the whole thing, verbatim: the 1,024
# bytes of EEData off a converter that had been driven, with 38 persist records
# in it. It lives in a file rather than in a string here because it is 64 rows
# of hex and this file is meant to be readable; it is the same kind of artefact
# as test/fixtures, and the same rule applies -- DO NOT EDIT IT.
#
# One row of it, so the format is in front of the reader:
#
#   000000  00  00  00  00  00  00  00  00  80  00  A1  FA  45  00  00  00   . . . . . . . . . . . . E . . .
#
# Six-digit address, sixteen bytes separated by two spaces, then an ASCII
# column. The ASCII column is the part a line-anchored regex dies on and the
# reason parse_eeprom_dump() stops at the first token that is not a hex pair.

GE_DUMP = (Path(__file__).resolve().parent / "testdata"
           / "ipecmd-ge0-400.txt").read_text(encoding="utf-8")


class TestEepromDump(unittest.TestCase):
    def test_the_real_dump_parses(self):
        image = flash.parse_eeprom_dump(GE_DUMP)
        self.assertIsNotNone(image)
        self.assertEqual(len(image), flash.EEPROM_BYTES)

    def test_the_first_record_is_the_one_in_the_dump(self):
        """Byte for byte against the row quoted above, so a parser that was
        off by one row or by one byte cannot pass."""
        image = flash.parse_eeprom_dump(GE_DUMP)
        self.assertEqual(image[:12],
                         bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x80, 0x00, 0xA1, 0xFA]))

    def test_the_ascii_column_is_not_read_as_data(self):
        """`. . . . E . . .` ends the row; row 0 would otherwise carry 32
        bytes and every address after it would be wrong."""
        image = flash.parse_eeprom_dump(GE_DUMP)
        self.assertEqual(image[16:20], bytes([0x00, 0x00, 0x00, 0x00]))
        self.assertEqual(image[0x1C0:0x1C4],
                         bytes([0x6F, 0x48, 0x02, 0x00]))

    def test_the_tail_is_erased(self):
        """The ring is 768 bytes and this part had 38 records in it."""
        image = flash.parse_eeprom_dump(GE_DUMP)
        self.assertTrue(all(b == 0xFF for b in image[0x1C8:]))

    def test_a_dump_that_stops_one_byte_short_is_refused(self):
        """WHICH IS NOT HYPOTHETICAL: -GE0-3FF returns 1,023 bytes and prints
        the last cell as `--`, because -G's end address is EXCLUSIVE. That is
        why EEPROM_DUMP_RANGE is 0-400. A parser that padded the short read
        would have reported a preserved ring off an image it never saw."""
        short = GE_DUMP.replace("0003F0  FF  FF  FF  FF  FF  FF  FF  FF  FF  "
                                "FF  FF  FF  FF  FF  FF  FF",
                                "0003F0  FF  FF  FF  FF  FF  FF  FF  FF  FF  "
                                "FF  FF  FF  FF  FF  FF  --")
        self.assertNotEqual(short, GE_DUMP)
        self.assertIsNone(flash.parse_eeprom_dump(short))

    def test_a_failed_read_is_refused_before_parsing(self):
        """An unpowered board prints Operation Succeeded and exits 0."""
        self.assertIsNone(flash.parse_eeprom_dump(UNPOWERED))

    def test_prose_alone_never_yields_an_image(self):
        self.assertIsNone(flash.parse_eeprom_dump(IDENTIFY_OK))


# --- synthetic, and labelled as such -----------------------------------------
#
# These are NOT IPECMD output. parse_eeprom_dump() deliberately assumes nothing
# about row width, address width or separator -- it checks the RESULT instead --
# and that property cannot be tested against the one layout the tool happens to
# print. So the layout is varied here on purpose, and the real capture above is
# what pins the format.

def _dump(values, per_line=16, sep="  ", addr_width=4):
    out = ["Target voltage detected", "Target device PIC18F25K80 found."]
    for base in range(0, len(values), per_line):
        row = values[base:base + per_line]
        out.append("%0*X%s%s" % (addr_width, base, sep,
                                 " ".join("%02X" % v for v in row)))
    out.append("Operation Succeeded")
    return "\n".join(out) + "\n"


BLANK_RING = [0xFF] * flash.EEPROM_BYTES
USED_RING = [0x2A] * 12 + [0xFF] * (flash.EEPROM_BYTES - 12)


class TestEepromDumpTolerance(unittest.TestCase):
    def test_the_layout_may_vary(self):
        for kwargs in ({"per_line": 8}, {"per_line": 32},
                       {"sep": ": "}, {"addr_width": 8},
                       {"per_line": 16, "sep": "\t", "addr_width": 6}):
            with self.subTest(**kwargs):
                self.assertEqual(
                    flash.parse_eeprom_dump(_dump(BLANK_RING, **kwargs)),
                    bytes(BLANK_RING))

    def test_a_short_image_is_refused_rather_than_padded(self):
        """The whole point: a half-read must not read as a preserved ring."""
        text = _dump(USED_RING)
        text = "\n".join(text.splitlines()[:20]) + "\n"
        self.assertIsNone(flash.parse_eeprom_dump(text))

    def test_a_repeated_address_is_refused(self):
        text = _dump(BLANK_RING)
        lines = text.splitlines()
        self.assertIsNone(flash.parse_eeprom_dump(
            "\n".join(lines + [lines[3]]) + "\n"))

    def test_a_format_it_cannot_read_is_refused(self):
        """No addresses at all -- None, never a scrambled image."""
        rows = [" ".join("FF" for _ in range(16))
                for _ in range(flash.EEPROM_BYTES // 16)]
        self.assertIsNone(flash.parse_eeprom_dump("\n".join(rows) + "\n"))


class TestDescribeEeprom(unittest.TestCase):
    def test_blank_says_so_and_is_not_an_error(self):
        self.assertIn("blank", flash.describe_eeprom(bytes(BLANK_RING)))

    def test_a_written_ring_counts_its_bytes(self):
        self.assertIn("12 of 1024", flash.describe_eeprom(bytes(USED_RING)))

    def test_the_real_dump_is_described_as_written(self):
        image = flash.parse_eeprom_dump(GE_DUMP)
        self.assertIn("455 of 1024", flash.describe_eeprom(image))


class TestEepromRange(unittest.TestCase):
    def test_the_dump_range_end_is_exclusive(self):
        """Measured, not read: -GE0-400 returns 1,024 bytes and -GE0-3FF
        returns 1,023. No readme says so."""
        lo, hi = flash.EEPROM_DUMP_RANGE.split("-")
        self.assertEqual(int(lo, 16), 0)
        self.assertEqual(int(hi, 16), flash.EEPROM_BYTES)

    def test_the_preserve_range_covers_the_ring_either_way(self):
        """-Z's end has NOT been established as exclusive, so it keeps the
        readme's form. Both readings still cover the whole ring."""
        lo, hi = flash.EEPROM_PRESERVE_RANGE.split("-")
        self.assertEqual(int(lo, 16), 0)
        self.assertGreaterEqual(int(hi, 16), _ring_bytes())

    def test_the_ring_fits_inside_the_array(self):
        self.assertLessEqual(_ring_bytes(), flash.EEPROM_BYTES)


def _ring_bytes() -> int:
    """PERSIST_SLOTS * PERSIST_RECORD_BYTES, out of src/config.h."""
    cfg = Path(__file__).resolve().parent.parent / "src" / "config.h"
    text = cfg.read_text(encoding="utf-8")
    slots = int(re.search(r"#define PERSIST_SLOTS\s+(\d+)", text).group(1))
    size = int(re.search(r"#define PERSIST_RECORD_BYTES\s+(\d+)",
                         text).group(1))
    return slots * size


class TestHex(unittest.TestCase):
    def test_config3h_needs_the_extended_address_record(self):
        # 300005h is only reachable through a type 04 record. A parser that
        # ignored those would read address 0x0005 of program memory instead,
        # which is a real instruction and would pass or fail at random.
        text = ihex([
            (0x00, 0x0000, [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC]),
            (0x04, 0x0000, [0x00, 0x30]),
            (0x00, 0x0000, [0xFF, 0xFF, 0xFF, 0xFF, 0x26, 0x89]),
        ])
        self.assertEqual(flash.hex_byte(text, flash.CONFIG3H_ADDR), 0x89)
        self.assertEqual(flash.hex_byte(text, 0x000005), 0xBC)

    def test_missing_config_is_not_silently_ok(self):
        text = ihex([(0x00, 0x0000, [0x00, 0x01])])
        self.assertIsNone(flash.hex_byte(text, flash.CONFIG3H_ADDR))


class TestCanmx(unittest.TestCase):
    def write(self, value):
        path = Path(self.tmp) / "canfuel.hex"
        path.write_text(ihex([
            (0x04, 0x0000, [0x00, 0x30]),
            (0x00, 0x0000, [0xFF, 0xFF, 0xFF, 0xFF, 0x26, value]),
        ]), encoding="ascii")
        return path

    def setUp(self):
        import tempfile
        self._dir = tempfile.TemporaryDirectory()
        self.tmp = self._dir.name

    def tearDown(self):
        self._dir.cleanup()

    def test_set_is_the_pass(self):
        ok, detail = flash.check_canmx(self.write(0x89))
        self.assertTrue(ok)
        self.assertIn("RB2/RB3", detail)

    def test_clear_is_refused(self):
        ok, detail = flash.check_canmx(self.write(0x88))
        self.assertFalse(ok)
        self.assertIn("RC6/RC7", detail)


class TestRealHex(unittest.TestCase):
    """The check against the artefact, when there is one to check."""

    def test_built_hex_has_canmx_set(self):
        hex_path = Path(flash.REPO) / "mplab" / "build" / "canfuel.hex"
        if not hex_path.exists():
            self.skipTest("no build; needs XC8")
        ok, detail = flash.check_canmx(hex_path)
        self.assertTrue(ok, detail)


class TestModes(unittest.TestCase):
    def test_normal_is_the_absence_of_the_flag(self):
        # config.h defaults CAN_START_MODE, so a normal build passes no -D.
        self.assertEqual(flash.MODES["normal"], "")

    def test_names_match_hal_can_h(self):
        self.assertEqual(flash.MODES["loopback"], "LOOPBACK")
        self.assertEqual(flash.MODES["listen-only"], "LISTEN_ONLY")


if __name__ == "__main__":
    unittest.main()
