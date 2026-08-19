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


# --- NOT observed: synthetic, and labelled as such --------------------------
#
# Everything above this line is text IPECMD really printed. These two are not.
# `-GE0-3FF` had never been run against a part when parse_eeprom_dump() was
# written, so there is no real capture to test it on, and inventing one and
# filing it with the others would make the file lie about the one thing it is
# for. What is tested here is therefore the parser's TOLERANCE and its refusal
# to answer when it does not understand -- not IPECMD's layout.
#
# ⚠ REPLACE THESE WITH A REAL DUMP the first time --preserve-eeprom or
# --read-eeprom runs. flash.py writes the raw output to mplab/build/ for
# exactly that, docs/flash-tool-notes.md is where the format belongs, and this
# comment stops being true the moment both are done.

def _dump(values, per_line=16, sep="  ", addr_width=4):
    """A plausible address-then-hex-bytes dump of `values`."""
    out = ["Target voltage detected", "Target device PIC18F25K80 found."]
    for base in range(0, len(values), per_line):
        row = values[base:base + per_line]
        out.append("%0*X%s%s" % (addr_width, base, sep,
                                 " ".join("%02X" % v for v in row)))
    out.append("Operation Succeeded")
    return "\n".join(out) + "\n"


BLANK_RING = [0xFF] * flash.EEPROM_BYTES
USED_RING = [0x2A] * 12 + [0xFF] * (flash.EEPROM_BYTES - 12)


class TestEepromDump(unittest.TestCase):
    def test_a_full_image_parses(self):
        got = flash.parse_eeprom_dump(_dump(USED_RING))
        self.assertEqual(got, bytes(USED_RING))

    def test_the_layout_may_vary(self):
        """Row width, separator and address width are all free."""
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

    def test_a_failed_read_is_refused_before_parsing(self):
        """An unpowered board prints Operation Succeeded and exits 0."""
        self.assertIsNone(flash.parse_eeprom_dump(UNPOWERED))

    def test_prose_alone_never_yields_an_image(self):
        self.assertIsNone(flash.parse_eeprom_dump(IDENTIFY_OK))


class TestDescribeEeprom(unittest.TestCase):
    def test_blank_says_so_and_is_not_an_error(self):
        self.assertIn("blank", flash.describe_eeprom(bytes(BLANK_RING)))

    def test_a_written_ring_counts_its_bytes(self):
        self.assertIn("12 of 1024", flash.describe_eeprom(bytes(USED_RING)))


class TestEepromRange(unittest.TestCase):
    def test_the_range_covers_the_whole_array(self):
        """DS39977C Table 1: 1,024 bytes of data EEPROM on this part."""
        lo, hi = flash.EEPROM_RANGE.split("-")
        self.assertEqual(int(lo, 16), 0)
        self.assertEqual(int(hi, 16), flash.EEPROM_BYTES - 1)

    def test_the_ring_fits_inside_it(self):
        cfg = (Path(__file__).resolve().parent.parent / "src" / "config.h")
        text = cfg.read_text(encoding="utf-8")
        slots = int(re.search(r"#define PERSIST_SLOTS\s+(\d+)", text).group(1))
        size = int(re.search(r"#define PERSIST_RECORD_BYTES\s+(\d+)",
                             text).group(1))
        self.assertLessEqual(slots * size, flash.EEPROM_BYTES)


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
