#!/usr/bin/env python3
"""Build the converter and flash it in one command, with a verdict.

`docs/install.md` step 5 is the procedure this automates;
`docs/flash-tool-notes.md` is the argument for every flag and the record of
what IPECMD actually prints. Read that file before changing anything here.

    python tools/flash.py                      # normal build, then flash it
    python tools/flash.py --mode loopback      # step 6
    python tools/flash.py --mode listen-only   # steps 7.4 and 8
    python tools/flash.py --identify           # asks, writes nothing, keeps it running
    python tools/flash.py --dry-run            # print the commands, run none

WHY THIS EXISTS, WHICH IS NOT "TO SAVE TYPING".

Three of the ways to get step 5 wrong are invisible at the time:

  * **The mode and the hex can disagree.** The three builds differ by one -D
    and are otherwise indistinguishable, so a hex flashed in the belief that it
    is a loopback build produces a correctly programmed board doing the wrong
    thing. Building and flashing in one invocation is what stops that, and
    build/can_mode is checked afterwards as the belt to that brace.
  * **CANMX is one bit and the most expensive one in the project.** Clear, and
    the CAN pins are on RC6/RC7 while this board is wired to RB2/RB3. It is
    checkable in the hex before anything is written, so it is checked.
  * **A read-only check is not a harmless one.** `-I` on its own leaves the
    part **held in reset**, because that is IPECMD's default and `-OL` is what
    releases it -- so asking a running converter what it is stops it dead, and
    it stays stopped until something programs it again. Measured both ways on
    a live board: with `-OL` it kept transmitting at its nominal 22 frames a
    second through the identify; without, it went to zero and stayed there.
    That cost an afternoon once, diagnosed as a wedged CAN module. Every
    invocation here passes `-OL`, including this one.
  * **IPECMD's exit code cannot carry the decision.** A target nobody powered
    prints `Operation Succeeded` and returns 0, while bad ICSP wiring returns
    1. Every verdict here comes from the printed text; the return code is
    reported and never branched on.

WHAT IS DELIBERATELY NOT HERE YET. Reading memory back off the part -- the
persist ring, for bring-up in the vehicle -- and `-Z0-3FF`, which preserves the
EEPROM through a reflash. Neither has ever been run against a part, and
guessing an undocumented switch on a live board is exactly what this repository
does not do. The gap list at the end of `flash-tool-notes.md` is what to close
first.

`-Y` is not run either, and that is a finding rather than an omission: it
verifies EEData against a hex with no EEPROM section, so on a perfectly
programmed board that has stored a persist record it reports
`Expected ff, Received 0` at address 0 and exits 7. Whether it does depends on
what the firmware has had to store since `-OL` released the part, which is not
a thing a verify should depend on. `-M` verifies implicitly, and that is the
verify that counts.

WARNING: **JP2 comes off before programming and goes back on afterwards**, and
no software can check that. IPECMD also drops an `MPLABXLog.xml` into whatever
directory it is run from.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

DEVICE = "18F25K80"
TOOL = "PPK3"

# make's CAN_MODE for each name this tool accepts. Empty is the normal build:
# config.h defaults CAN_START_MODE to HAL_CAN_MODE_NORMAL when nothing defines
# it, so the normal build is the absence of the flag rather than a value of it.
MODES = {
    "normal": "",
    "loopback": "LOOPBACK",
    "listen-only": "LISTEN_ONLY",
}

# CONFIG3H, byte address 300005h. Bit 0 is CANMX: 1 puts CANTX and CANRX on
# RB2 and RB3, which is what this board is wired to (DS39977C Register 28-5).
CONFIG3H_ADDR = 0x300005
CANMX_BIT = 0x01

# What a failed run says, and what it means. A table rather than a chain of
# ifs, because these strings are the whole diagnosis and belong where they can
# be read at a glance. The observed outputs are in flash-tool-notes.md.
FAILURES = [
    ("could not detect target voltage VDD",
     "the board is not powered. -W is deliberately not used, so it needs its "
     "own 5 V. That run still exits 0"),
    ("is an Invalid Device ID",
     "power is fine and ICSP is not: JP2 still fitted, the MCLR/PGC/PGD "
     "wiring, or a dead part"),
    ("Programmer not found",
     "no programmer: MPLAB X or IPE open and holding the tool, the firewall "
     "rule on IPECMD's localhost socket, or the USB cable"),
    ("Connection Failed.",
     "the programmer did not reach the target"),
]

IPECMD_MISSING = (
    "ipecmd was not found on PATH. It ships with MPLAB X, in\n"
    "mplab_platform/mplab_ipe under the install directory, and the installer\n"
    "does not put it on PATH for you. It is the one tool this repository\n"
    "needs on PATH without a fallback."
)


# ----------------------------------------------------------------- parsing


def diagnose(text: str) -> str | None:
    """The first known failure signature in text, as an explanation."""
    for needle, meaning in FAILURES:
        if needle in text:
            return meaning
    return None


def parse_identify(text: str, device: str = DEVICE) -> tuple[bool, str]:
    """Did -I find the right part? Never look at the return code."""
    bad = diagnose(text)
    if bad:
        return False, bad
    if "Target device PIC" + device + " found" not in text:
        return False, "no device line in the output"
    if "Operation Succeeded" not in text:
        return False, "the operation did not report success"

    detail = "PIC" + device
    for line in text.splitlines():
        if "Device Revision ID" in line:
            detail += ", revision " + line.split("=")[-1].strip()
            break
    if "Target voltage detected" in text:
        detail += ", powered from the board"
    return True, detail


def parse_blank_check(text: str) -> tuple[bool, str]:
    """True when the part is blank. A programmed part is not an error here."""
    bad = diagnose(text)
    if bad:
        return False, bad
    if "device is blank" in text:
        return True, "blank"
    if "not blank" in text.lower():
        return False, "already programmed, which is normal for a reflash"
    return False, "no blank check verdict in the output"


def parse_program(text: str) -> tuple[bool, str]:
    """Did -M -OL programme and implicitly verify?"""
    bad = diagnose(text)
    if bad:
        return False, bad
    for loud in ("Verify failed", "Programming failed", "Operation Failed"):
        if loud in text:
            return False, loud
    if "Program Succeeded" not in text:
        return False, "no 'Program Succeeded' in the output"
    if "Operation Succeeded" not in text:
        return False, "the operation did not report success"
    return True, "programmed and implicitly verified, released from reset"


# --------------------------------------------------------------- the hex


def hex_byte(hex_text: str, want: int) -> int | None:
    """One byte out of an Intel HEX file, by absolute address.

    Minimal on purpose: record type 00 for data and 04 for the upper sixteen
    address bits, which is all XC8 emits. The configuration words live at
    300000h and are reachable only through the type 04 records, so ignoring
    those would silently read the wrong part of the file.
    """
    upper = 0
    for line in hex_text.splitlines():
        line = line.strip()
        if not line.startswith(":") or len(line) < 11:
            continue
        count = int(line[1:3], 16)
        addr = int(line[3:7], 16)
        rtype = int(line[7:9], 16)
        data = line[9:9 + count * 2]
        if rtype == 0x04:
            upper = int(data, 16) << 16
        elif rtype == 0x00:
            base = upper + addr
            if base <= want < base + count:
                off = (want - base) * 2
                return int(data[off:off + 2], 16)
    return None


def check_canmx(hex_path: Path) -> tuple[bool, str]:
    """CANMX must be set, or the CAN pins are on the wrong side of the part."""
    value = hex_byte(hex_path.read_text(encoding="ascii", errors="replace"),
                     CONFIG3H_ADDR)
    if value is None:
        return False, "CONFIG3H is not in the hex at all"
    if not value & CANMX_BIT:
        return False, ("CONFIG3H = 0x%02X, CANMX clear -- that hex puts "
                       "CANTX/CANRX on RC6/RC7 and this board is wired "
                       "RB2/RB3" % value)
    return True, "CONFIG3H = 0x%02X, CANMX set (RB2/RB3)" % value


# --------------------------------------------------------------- running


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, bool, str]] = []

    def check(self, name: str, ok: bool, detail: str = "") -> bool:
        self.rows.append((name, ok, detail))
        print("  [%s] %s%s" % ("ok  " if ok else "FAIL", name,
                               " -- " + detail if detail else ""))
        return ok

    @property
    def failed(self) -> list[str]:
        return [n + ": " + d if d else n for n, ok, d in self.rows if not ok]


def fail(rep: Report, extra: str) -> int:
    print()
    print("FAIL")
    for line in rep.failed:
        print("  " + line)
    if extra:
        print("  " + extra)
    return 1


def run(cmd: list[str], dry: bool, timeout: float = 300.0) -> str:
    print("  $ " + " ".join(cmd))
    if dry:
        return ""
    try:
        done = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout, cwd=REPO)
    except FileNotFoundError:
        sys.exit(IPECMD_MISSING)
    out = (done.stdout or "") + (done.stderr or "")
    for line in out.splitlines():
        print("      " + line)
    print("      (exit %d, which decides nothing)" % done.returncode)
    return out


def ipecmd(args: list[str], dry: bool, device: str, tool: str) -> str:
    return run(["ipecmd", "-P" + device, "-T" + tool] + args, dry)


def build(mode: str, dry: bool) -> bool:
    cmd = ["make", "-C", "mplab"]
    if MODES[mode]:
        cmd.append("CAN_MODE=" + MODES[mode])
    print("  $ " + " ".join(cmd))
    if dry:
        return True
    done = subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)
    out = (done.stdout or "") + (done.stderr or "")
    for line in out.splitlines():
        print("      " + line)
    return done.returncode == 0


def stamped_mode(build_dir: Path) -> str:
    """What mplab/Makefile recorded the last build as -- see MODE_STAMP there."""
    stamp = build_dir / "can_mode"
    if not stamp.exists():
        return "<no stamp>"
    return stamp.read_text(encoding="ascii").strip()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", choices=sorted(MODES), default="normal",
                    help="which build to make and flash (default: normal)")
    ap.add_argument("--identify", action="store_true",
                    help="only ask what is on the header, and change nothing")
    ap.add_argument("--blank-check", action="store_true",
                    help="also run -C first; a programmed part is not an error")
    ap.add_argument("--no-build", action="store_true",
                    help="flash whatever is already in mplab/build")
    ap.add_argument("--device", default=DEVICE)
    ap.add_argument("--tool", default=TOOL)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    hex_path = REPO / "mplab" / "build" / "canfuel.hex"
    rep = Report()

    print()
    print("flash.py -- install.md step 5")

    if args.identify:
        print()
        print("identify -- writes nothing, and releases the part afterwards")
        out = ipecmd(["-I", "-OL"], args.dry_run, args.device, args.tool)
        if args.dry_run:
            return 0
        ok, detail = parse_identify(out, args.device)
        rep.check("device answers on the ICSP header", ok, detail)
        return fail(rep, "") if rep.failed else 0

    print()
    print("build -- " + args.mode)
    if args.no_build:
        print("  (skipped, --no-build)")
    elif not build(args.mode, args.dry_run):
        return fail(rep, "the build failed; nothing was flashed")

    if not args.dry_run:
        want = MODES[args.mode]
        got = stamped_mode(hex_path.parent)
        rep.check("the hex is the mode that was asked for", got == want,
                  "build/can_mode is %r, wanted %r" % (got, want))
        if not hex_path.exists():
            return fail(rep, str(hex_path) + " does not exist")
        ok, detail = check_canmx(hex_path)
        rep.check("CANMX in the hex", ok, detail)
        if rep.failed:
            return fail(rep, "nothing was written to the part")

    print()
    print("identify")
    out = ipecmd(["-I", "-OL"], args.dry_run, args.device, args.tool)
    if not args.dry_run:
        ok, detail = parse_identify(out, args.device)
        rep.check("device answers on the ICSP header", ok, detail)
        if rep.failed:
            return fail(rep, "nothing after this could have succeeded")

    if args.blank_check:
        print()
        print("blank check")
        out = ipecmd(["-C"], args.dry_run, args.device, args.tool)
        if not args.dry_run:
            _, detail = parse_blank_check(out)
            print("  [note] " + detail)
            if diagnose(out):
                rep.check("blank check ran", False, detail)

    print()
    print("program -- -M -OL, which erases the EEPROM with it")
    out = ipecmd(["-F" + str(hex_path), "-M", "-OL"],
                 args.dry_run, args.device, args.tool)
    if not args.dry_run:
        ok, detail = parse_program(out)
        rep.check("programmed", ok, detail)

    print()
    if args.dry_run:
        print("dry run -- nothing was built and nothing was written.")
        return 0
    if rep.failed:
        return fail(rep, "")
    print("PASS -- the %s build is in the part and running." % args.mode)
    print("Put JP2 back on. JP1 decides whether the LEDs light and whether")
    print("0x603 is transmitted; steps 6 and 7 both want it fitted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
