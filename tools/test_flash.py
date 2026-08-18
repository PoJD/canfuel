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

# -Y on a board that was just programmed and released from reset. It verifies
# EEData against a hex with no EEPROM section, and by then the firmware has
# written its first persist record. A perfect board fails this.
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
        self.assertIn("released from reset", detail)

    def test_verify_failed_is_a_failure(self):
        ok, detail = flash.parse_program(VERIFY_EEDATA_FAILS)
        self.assertFalse(ok)
        self.assertIn("Verify failed", detail)

    def test_unpowered(self):
        ok, detail = flash.parse_program(UNPOWERED)
        self.assertFalse(ok)
        self.assertIn("not powered", detail)


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
