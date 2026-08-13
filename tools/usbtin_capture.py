#!/usr/bin/env python3
"""Capture from a USBtin over its serial port, with hardware timestamps on.

This exists because **USBtinViewer must not be used for timing work**. It
stamps a frame when the Java GUI gets round to the line, not when the frame
arrived, and it says so of itself: "the timestamp is generated in the
application on the host, the hardware timestamping is currently not used"
(github.com/EmbedME/USBtinViewer). Open question 9 in docs/can-decoding.md is
the damage that did to two of the seven fixtures. This script talks to the
adapter directly and turns the adapter's own timestamping on with `Z1`.

The output is **the raw slcan stream, byte for byte as the adapter emits it**,
which is format A of tools/canlog.py with the four extra hex digits of
millisecond timestamp that Z1 appends:

    t480821e6330000000000  2a3f
    ^                      ^--- ms, stamped in the adapter
    +--- the frame, exactly as the older fixtures store it

So the file this writes is readable by canlog.py and replay.py with no
conversion, and is directly comparable with the existing fixtures.

Commands, from fischl.de/usbtin:

    C   close the channel (sent first, in case it was left open)
    S6  500 kbit/s
    Z1  timestamping on -- the whole point of this script
    L   open listen only; the adapter does not ACK and does not transmit
    O   open normally (--normal; not the default, deliberately)
    F   read and clear the status flags

Every command answers CR for OK and BEL for error, and both are checked.

Usage:

    python usbtin_capture.py --seconds 60 --out idle_z1.txt
    python usbtin_capture.py --port COM5 --seconds 120 --out drive_z1.txt
    python usbtin_capture.py --list                     # show serial ports
"""

from __future__ import annotations

import argparse
import sys
import time

# pyserial is this project's only third-party dependency and only the two
# adapter scripts need it, which is why CI installs nothing and there is no
# requirements.txt. So a missing import is recorded rather than fatal: the
# module must stay importable so its pure helpers can be unit tested on a
# machine -- or a CI runner -- with no pyserial and no hardware. The scripts
# that actually open a port call require_serial() first.
try:
    import serial
    from serial.tools import list_ports
except ImportError:  # pragma: no cover - depends on the machine
    serial = None
    list_ports = None


def require_serial() -> None:
    if serial is None:
        sys.exit("pyserial is not installed:  python -m pip install pyserial")


CR = b"\r"
BEL = b"\x07"

# 500 kbit/s. The powertrain bus, measured -- see docs/can-decoding.md.
BITRATE_CMD = b"S6"

# No acceptance filter is set, and that is a decision rather than an oversight.
#
# The USBtin takes `mxxxxxxxx` and `Mxxxxxxxx` for an acceptance mask and code,
# but which polarity means "don't care" is not stated in any document we have,
# and the two conventions in circulation are exact opposites: get it backwards
# and the adapter passes *nothing*, which looks identical to a dead bus. A
# capture that silently records zero frames is the one failure mode worth
# engineering out of a trip to the car.
#
# The cost of not filtering is throughput, and it is affordable: the bus runs
# about 700 frames/s, i.e. roughly 18 kB/s of slcan text, and the USBtin is a
# USB CDC device whose serial link is not really running at the baud rate
# configured on it. If frames are being dropped the status flags say so, which
# is why --seconds always ends with an `F`. Filter afterwards instead:
#
#     python canlog.py --dump --id 0x480 FILE
ACCEPTANCE_FILTER = None


def find_port() -> str:
    """Guess the USBtin's port. Raises if it is not obvious."""
    require_serial()
    named, generic = [], []
    for p in list_ports.comports():
        text = f"{p.description} {p.manufacturer or ''} {p.product or ''}".lower()
        if "usbtin" in text or "lpc" in text:
            named.append(p.device)
        elif "bluetooth" in text:
            # A Windows box has several of these and none of them is a CAN
            # adapter. Skipping them is what makes the fallback below useful.
            continue
        elif p.vid is not None:
            # A real USB device rather than a legacy or virtual COM port. On
            # this machine Windows describes the USBtin as nothing more than
            # "Serial USB device", so name matching alone finds nothing.
            generic.append(p.device)

    if len(named) == 1:
        return named[0]
    if not named and len(generic) == 1:
        return generic[0]

    ports = [p.device for p in list_ports.comports()]
    if not ports:
        raise SystemExit("No serial ports at all. Is the USBtin plugged in?")
    raise SystemExit(
        "Could not identify the USBtin. Pass --port explicitly.\n"
        "Ports seen: " + ", ".join(ports)
    )


def command(ser: "serial.Serial", cmd: bytes, *, expect_payload: bool = False) -> bytes:
    """Send one command and check the adapter's answer.

    Returns whatever came back before the terminating CR. A BEL is an error
    and is raised rather than warned about -- a misconfigured adapter that
    keeps running produces a file that looks fine and is not.
    """
    ser.reset_input_buffer()
    ser.write(cmd + CR)
    ser.flush()

    answer = bytearray()
    deadline = time.monotonic() + 1.0
    while time.monotonic() < deadline:
        ch = ser.read(1)
        if not ch:
            continue
        if ch == BEL:
            raise SystemExit(
                f"The USBtin rejected {cmd.decode()!r} (BEL). "
                "Is the channel already open, or the adapter in a bad state? "
                "Unplug it and try again."
            )
        if ch == CR:
            return bytes(answer)
        answer += ch

    if expect_payload:
        raise SystemExit(f"No answer to {cmd.decode()!r} within a second.")
    return bytes(answer)


def capture(port: str, seconds: float, out_path: str, *, normal: bool) -> int:
    require_serial()
    with serial.Serial(port, baudrate=115200, timeout=0.1) as ser:
        # The channel may have been left open by a previous run or by a viewer
        # that exited badly. Closing an already-closed channel answers BEL on
        # some firmware, so this one send is deliberately not checked.
        ser.write(b"C" + CR)
        ser.flush()
        time.sleep(0.1)
        ser.reset_input_buffer()

        version = command(ser, b"V", expect_payload=True)
        print(f"USBtin on {port}, firmware {version.decode(errors='replace')}")

        command(ser, BITRATE_CMD)
        command(ser, b"Z1")
        if ACCEPTANCE_FILTER is not None:  # pragma: no cover - disabled above
            for part in ACCEPTANCE_FILTER:
                command(ser, part)

        mode = b"O" if normal else b"L"
        command(ser, mode)
        print(
            "Channel open at 500 kbit/s, timestamps ON, "
            + ("NORMAL -- this node ACKs the bus" if normal
               else "LISTEN ONLY -- silent on the bus")
        )

        lines = 0
        pending = bytearray()
        started = time.monotonic()
        deadline = started + seconds

        try:
            with open(out_path, "w", newline="\n", encoding="ascii") as fh:
                while time.monotonic() < deadline:
                    chunk = ser.read(4096)
                    if not chunk:
                        continue
                    pending += chunk
                    while CR in pending:
                        raw, _, pending = pending.partition(CR)
                        line = raw.decode("ascii", errors="replace").strip()
                        if not line or line == "\x07":
                            continue
                        fh.write(line + "\n")
                        lines += 1
                    left = deadline - time.monotonic()
                    print(f"\r{lines} frames, {left:5.1f} s left ", end="",
                          flush=True)
        finally:
            print()
            elapsed = time.monotonic() - started
            # Close the channel *before* asking for the status flags. Sent
            # while the channel is open, `F` races the frames still arriving
            # and the first CR back is the end of somebody else's frame --
            # which is what the first version of this script did, and it
            # reported "unreadable answer" on a perfectly good capture.
            ser.write(b"C" + CR)
            ser.flush()
            time.sleep(0.1)
            flags = read_flags(ser)

        print(f"{lines} frames in {elapsed:.1f} s = {lines / elapsed:.0f}/s"
              f"  ->  {out_path}")
        report_flags(flags)
        return lines


def read_flags(ser: "serial.Serial") -> bytes:
    """Ask for the status flags and pick the answer out of the stream.

    Anything still in flight from before the channel closed is skipped: frames
    begin with t/T/r/R, and the answer we want begins with F. Returns b"" if
    no such line turns up, which is reported as "not available" rather than as
    a fault -- the capture itself is unaffected either way.
    """
    ser.reset_input_buffer()
    ser.write(b"F" + CR)
    ser.flush()

    pending = bytearray()
    deadline = time.monotonic() + 1.0
    while time.monotonic() < deadline:
        chunk = ser.read(64)
        if chunk:
            pending += chunk
        while CR in pending:
            raw, _, pending = pending.partition(CR)
            line = bytes(raw).strip(BEL).strip()
            if line.startswith(b"F"):
                return line
    return b""


def report_flags(flags: bytes) -> None:
    """Decode the answer to `F`, which is 'F' plus two hex digits.

    Bit meanings are the Lawicel status byte the USBtin inherits. The two that
    matter here both mean the capture has holes in it, which would otherwise be
    indistinguishable from a quiet bus.
    """
    text = flags.decode(errors="replace").strip()
    if not text.startswith("F") or len(text) < 3:
        print("Status flags: not available from this adapter "
              "(the capture itself is unaffected).")
        return

    value = int(text[1:3], 16)
    meanings = {
        0x01: "CAN receive FIFO queue full",
        0x02: "CAN transmit FIFO queue full",
        0x04: "error warning",
        0x08: "data overrun",
        0x20: "passive error",
        0x40: "arbitration lost",
        0x80: "bus error",
    }
    hits = [t for bit, t in meanings.items() if value & bit]
    if not hits:
        print(f"Status flags: {value:#04x}, clean.")
    else:
        print(f"Status flags: {value:#04x}  ** {', '.join(hits)} **")
        print("  Frames were lost, so the frame counts and any average rate "
              "computed from them are understated.")
        print("  A frame *period* survives this, and it is worth knowing why: "
              "a lost frame merges two")
        print("  intervals into one, so losses only ever add counts at "
              "integer multiples of the true")
        print("  period and never below it. Read the mode, not the mean:  "
              "canlog.py --gaps --id 0x480")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", help="serial port, e.g. COM5 (default: autodetect)")
    ap.add_argument("--seconds", type=float, default=60.0,
                    help="how long to record (default 60)")
    ap.add_argument("--out", default="capture_z1.txt", help="output file")
    ap.add_argument("--normal", action="store_true",
                    help="open the channel in NORMAL mode -- this node then "
                         "ACKs frames on the car's bus. The default is listen "
                         "only, which is silent.")
    ap.add_argument("--list", action="store_true",
                    help="list serial ports and exit")
    args = ap.parse_args(argv)

    if args.list:
        for p in list_ports.comports():
            print(f"{p.device:10s} {p.description}")
        return 0

    port = args.port or find_port()
    lines = capture(port, args.seconds, args.out, normal=args.normal)

    if lines == 0:
        print("\nNothing was captured. Either the bus is asleep (ignition off) "
              "or CANH/CANL are not connected.")
        return 1

    print(f"\nNext:  python canlog.py {args.out}")
    print(f"       python canlog.py --dump --id 0x480 {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
