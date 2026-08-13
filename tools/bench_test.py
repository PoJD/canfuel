#!/usr/bin/env python3
"""One command that tests a converter on a bench and prints a verdict.

docs/install.md step 7. It replays a real recording from the vehicle onto a
short bench bus through a USBtin, listens to what the converter transmits back,
reads the converter's own diagnostic frame, and says PASS or FAIL.

    python tools/bench_test.py                       # 20 s, the warm idle log
    python tools/bench_test.py --seconds 60
    python tools/bench_test.py --log test/fixtures/03_drive.txt
    python tools/bench_test.py --dry-run             # no adapter, no board

**Why a replay and not a generator.** test/fixtures/ holds seventeen logs off
the vehicle. Replaying one means the firmware meets the identifiers, payloads
and -- for the three `_z1` files -- the arrival pattern it will meet in the
car. Invented traffic would exercise the parts we already understand.

**Why this beats watching the LED.** The LED encodes the CAN health in a blink
rate, which asks a human to tell 2.5 Hz from 5 Hz correctly, once, and to
believe what they saw. 0x603 carries the same information as numbers, plus the
things no LED could express: which reset started the part, how long it has been
up, the module's own COMSTAT error state, and how many transmissions the
firmware could not queue.

⚠ **The converter must be running a NORMAL build**, and the reason is CAN
itself: a transmitter needs a receiver to drive the acknowledge slot, and
DS39977C §27.3.4 says listen only sends nothing "including error flags or
Acknowledge signals". With a LISTEN_ONLY hex, this adapter is alone on the bus:
every frame goes unacknowledged, is retransmitted, and the adapter reaches the
bus-off limit within milliseconds. Testing a listen-only build on a bench needs
a second adapter to do the acknowledging. The verdict below says so when it
sees it rather than leaving it to be worked out.

⚠ **The DBG_EN jumper (JP1) must be fitted**, or there is no 0x603 at all: the
firmware only transmits it while somebody is looking. A run that sees 0x600 and
0x601 but no 0x603 is almost always a missing jumper, not a fault.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import canlog

try:
    import serial
except ImportError:  # pragma: no cover - depends on the machine
    sys.exit("pyserial is not installed:  python -m pip install pyserial")

from usbtin_capture import BEL, BITRATE_CMD, CR, find_port, read_flags

REPO = Path(__file__).resolve().parents[1]
DEFAULT_LOG = REPO / "test" / "fixtures" / "09_idle_60s_z1.txt"

# What the converter transmits, from src/config.h.
TX_FUEL, TX_ENGINE, TX_TRIP, TX_DIAG = 0x600, 0x601, 0x602, 0x603
EXPECTED_HZ = {TX_FUEL: 10.0, TX_ENGINE: 10.0, TX_TRIP: 1.0, TX_DIAG: 1.0}
FRAME_NAME = {
    TX_FUEL:   "0x600 fuel   (FuelNow, FuelAvg, FuelTank, Range)",
    TX_ENGINE: "0x601 engine (Power, Torque, Flow, VddConv)",
    TX_TRIP:   "0x602 trip   (litres, metres)",
    TX_DIAG:   "0x603 diag   (errors, reset cause, uptime)",
}

# src/config.h. Kept as literals rather than parsed out of the header: this
# script is checked against it by tools/checkdocs.py, which fails when the two
# disagree, so a copy here cannot drift quietly.
DIAG_LAYOUT_VERSION = 1
DIAG_VERSION_SHIFT = 5
DIAG_RESET_CAUSE_MASK = 0x1F

DIAG_FLAGS = [
    (0x01, "CAN_OK"),
    (0x02, "SILENT"),
    (0x04, "UNHEALTHY"),
    (0x08, "DATA_LIVE"),
    (0x10, "PERSIST_OK"),
]
RESET_CAUSES = [
    (0x01, "power-on"),
    (0x02, "brown-out"),
    (0x04, "WATCHDOG"),
    (0x08, "RESET instruction"),
    (0x10, "STACK"),
]
# DS39977C Register 27-4, COMSTAT bits 5-0.
COMSTAT_BITS = [
    (0x20, "TXBO bus-off"),
    (0x10, "TXBP transmit passive"),
    (0x08, "RXBP receive passive"),
    (0x04, "TXWARN"),
    (0x02, "RXWARN"),
    (0x01, "EWARN"),
]

# Only the six identifiers the converter accepts are replayed by default. The
# other eight on the bus are filtered out in hardware by the firmware anyway,
# and dropping them halves what has to cross a 115200-baud serial link while
# the converter's own frames are coming back the other way.
ACCEPTED_IDS = {0x1A0, 0x280, 0x288, 0x320, 0x420, 0x480}


def be16(b: bytes, off: int) -> int:
    return b[off] << 8 | b[off + 1]


def decode_diag(data: bytes) -> dict:
    """0x603, laid out in src/config.h and docs/frames.md."""
    if len(data) != 8:
        raise ValueError(f"0x603 should carry 8 bytes, not {len(data)}")
    return {
        "rx_err": data[0],
        "tx_err": data[1],
        "comstat": data[2],
        "flags": data[3],
        "reset_cause": data[4] & DIAG_RESET_CAUSE_MASK,
        "version": data[4] >> DIAG_VERSION_SHIFT,
        "tx_fail": data[5],
        "uptime_s": be16(data, 6),
    }


def names(value: int, table) -> str:
    hits = [name for bit, name in table if value & bit]
    return " ".join(hits) if hits else "none"


def replay_frames(log: Path, every_id: bool):
    frames = canlog.parse_file(log, fix_doubled=True)
    if not every_id:
        frames = [f for f in frames if f.can_id in ACCEPTED_IDS]
    if not frames:
        sys.exit(f"{log}: nothing to replay")

    stamped = [f.ts_ms for f in frames if f.ts_ms is not None]
    if len(stamped) == len(frames) and len(frames) > 1:
        first = frames[0].ts_ms
        return frames, [f.ts_ms - first for f in frames], True
    return frames, [i * 10 for i in range(len(frames))], False


def slcan_tx(can_id: int, data: bytes) -> bytes:
    """One frame as the adapter's transmit command: tIIILDD.."""
    if not 0 <= can_id <= 0x7FF:
        raise ValueError(f"not an 11-bit identifier: {can_id:#x}")
    if len(data) > 8:
        raise ValueError(f"a CAN frame carries at most 8 bytes, not {len(data)}")
    return f"t{can_id:03X}{len(data):X}{data.hex().upper()}".encode()


def parse_rx(line: bytes):
    """A received frame off the adapter, or None for anything else.

    The stream carries our own transmit acknowledgements (`z`) interleaved with
    incoming frames, so this has to sort them rather than assume.
    """
    frame = canlog.parse_line(line.decode(errors="replace").strip())
    return frame


def run(port: str, frames, offsets, seconds: float, speed: float):
    received = {}          # can_id -> list of host monotonic times
    last_payload = {}      # can_id -> bytes
    sent = 0
    rejected = 0

    with serial.Serial(port, baudrate=115200, timeout=0) as ser:
        ser.write(b"C" + CR)
        ser.flush()
        time.sleep(0.1)
        ser.reset_input_buffer()

        for cmd in (BITRATE_CMD, b"O"):
            ser.write(cmd + CR)
            ser.flush()
            time.sleep(0.05)
        ser.reset_input_buffer()

        pending = bytearray()
        started = time.monotonic()
        span = (offsets[-1] + 1) / 1000.0 / speed

        try:
            loop = 0
            while time.monotonic() - started < seconds:
                base = started + loop * span
                for frame, offset in zip(frames, offsets):
                    due = base + offset / 1000.0 / speed
                    while True:
                        now = time.monotonic()
                        if now - started >= seconds:
                            raise TimeoutError
                        chunk = ser.read(512)
                        if chunk:
                            pending += chunk
                            while CR in pending:
                                raw, _, pending = pending.partition(CR)
                                text = bytes(raw).strip(BEL).strip()
                                if not text or text[:1] in (b"z", b"Z"):
                                    continue
                                got = parse_rx(text)
                                if got is not None:
                                    received.setdefault(
                                        got.can_id, []).append(now)
                                    last_payload[got.can_id] = got.data
                        if now >= due:
                            break
                        time.sleep(0)
                    ser.write(slcan_tx(frame.can_id, frame.data) + CR)
                    sent += 1
                loop += 1
        except TimeoutError:
            pass
        except KeyboardInterrupt:
            print("\nInterrupted.")

        elapsed = time.monotonic() - started
        ser.flush()
        time.sleep(0.2)
        ser.timeout = 0.1
        flags = read_flags(ser)
        ser.write(b"C" + CR)
        ser.flush()

    return {
        "sent": sent,
        "rejected": rejected,
        "elapsed": elapsed,
        "received": received,
        "last": last_payload,
        "flags": flags,
    }


def verdict(result: dict) -> int:
    """Print the report and return a process exit code."""
    fails, warns = [], []
    elapsed = result["elapsed"]
    received = result["received"]

    print()
    print(f"Traffic sent            {result['sent']} frames "
          f"in {elapsed:.1f} s")
    if result["sent"] == 0:
        fails.append("nothing was transmitted at all")

    text = result["flags"].decode(errors="replace").strip()
    if text.startswith("F") and len(text) >= 3:
        value = int(text[1:3], 16)
        if value == 0:
            print(f"Adapter status          {value:#04x} clean")
        elif value & 0x02:
            print(f"Adapter status          {value:#04x} transmit FIFO full")
            warns.append("the adapter could not keep up -- try --speed 0.5; "
                         "this is the host, not the converter")
        else:
            print(f"Adapter status          {value:#04x}")
            fails.append(f"the adapter reported errors ({value:#04x}); "
                         "nothing acknowledged us, or the bus is miswired")
    else:
        warns.append("the adapter did not report its status flags")

    print()
    print("What the converter transmitted")
    for can_id in (TX_FUEL, TX_ENGINE, TX_TRIP, TX_DIAG):
        times = received.get(can_id, [])
        hz = len(times) / elapsed if elapsed > 0 else 0.0
        want = EXPECTED_HZ[can_id]
        mark = "ok"
        if not times:
            mark = "MISSING"
            if can_id == TX_DIAG:
                fails.append("no 0x603 -- is the DBG_EN jumper (JP1) fitted?")
            else:
                fails.append(f"the converter never transmitted {can_id:#05x}")
        elif hz < want * 0.5 or hz > want * 1.8:
            mark = "RATE"
            warns.append(f"{can_id:#05x} arrived at {hz:.1f} Hz, "
                         f"expected about {want:.0f} Hz")
        print(f"  {FRAME_NAME[can_id]:<48} {len(times):5d}  "
              f"{hz:5.1f} Hz  {mark}")

    diag = None
    if TX_DIAG in result["last"]:
        try:
            diag = decode_diag(result["last"][TX_DIAG])
        except ValueError as exc:
            fails.append(str(exc))

    if diag is not None:
        print()
        print("Converter diagnostics, out of 0x603")
        if diag["version"] != DIAG_LAYOUT_VERSION:
            fails.append(f"0x603 layout version {diag['version']}, "
                         f"this script speaks {DIAG_LAYOUT_VERSION}")
        print(f"  CAN error counters      rx {diag['rx_err']}, "
              f"tx {diag['tx_err']}")
        if diag["rx_err"] or diag["tx_err"]:
            fails.append(f"CAN error counters are not zero "
                         f"(rx {diag['rx_err']}, tx {diag['tx_err']})")

        print(f"  Module error state      {names(diag['comstat'], COMSTAT_BITS)}")
        if diag["comstat"]:
            fails.append("the ECAN module is reporting an error state "
                         f"({names(diag['comstat'], COMSTAT_BITS)})")

        print(f"  Flags                   {names(diag['flags'], DIAG_FLAGS)}")
        if not diag["flags"] & 0x01:
            fails.append("CAN_OK is clear: hal_can_init() never reached "
                         "its mode")
        if diag["flags"] & 0x04:
            fails.append("UNHEALTHY is latched: there was an error or a FIFO "
                         "overflow at some point since power-up")
        if not diag["flags"] & 0x08:
            fails.append("DATA_LIVE is clear: the converter is not seeing "
                         "our traffic")
        if diag["flags"] & 0x02:
            warns.append("SILENT is set, so this is a loopback build")

        print(f"  Send refusals           {diag['tx_fail']}")
        if diag["tx_fail"]:
            warns.append(f"{diag['tx_fail']} frames could not be queued; a "
                         "few is arbitration, many means nothing is getting out")

        print(f"  Reset cause             "
              f"{names(diag['reset_cause'], RESET_CAUSES)}")
        if diag["reset_cause"] & 0x04:
            fails.append("the last reset was the WATCHDOG -- the firmware "
                         "hung. This is a bug, not a bench problem")
        if diag["reset_cause"] & 0x02:
            fails.append("the last reset was a BROWN-OUT -- the supply sagged "
                         "below BORV. Check the bench supply before the code")
        if diag["reset_cause"] & 0x10:
            fails.append("the last reset was a STACK overflow or underflow")

        print(f"  Uptime                  {diag['uptime_s']} s")
        if diag["uptime_s"] < elapsed - 2:
            fails.append(f"uptime is {diag['uptime_s']} s but the test ran "
                         f"{elapsed:.0f} s -- the converter restarted mid-test")

    if TX_FUEL in result["last"] and TX_ENGINE in result["last"]:
        fuel = result["last"][TX_FUEL]
        eng = result["last"][TX_ENGINE]
        print()
        print("Last values the converter sent")
        print(f"  FuelNow {be16(fuel, 0) / 10:.1f}   "
              f"FuelAvg {be16(fuel, 2) / 10:.1f} l/100km   "
              f"FuelTank {be16(fuel, 4) / 10:.1f} l   "
              f"Range {be16(fuel, 6)} km")
        vdd = be16(eng, 6) / 100
        print(f"  Power {be16(eng, 0) / 10:.1f} kW   "
              f"Torque {be16(eng, 2) / 10:.1f} Nm   "
              f"Vdd {vdd:.2f} V")
        if not 4.5 <= vdd <= 5.5:
            warns.append(f"VddConv reads {vdd:.2f} V, outside 4.5-5.5 V")

    print()
    for w in warns:
        print(f"  warning: {w}")
    for f in fails:
        print(f"  FAILED:  {f}")

    print()
    if fails:
        print("FAIL -- see above.")
        return 1
    print("Synthetic bench test finished. Traffic sent, the converter "
          "answered on all four")
    print("frames, and its CAN error counters are zero. "
          + ("PASS with warnings." if warns else "PASS."))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG,
                    help="recording to replay (default: the warm idle log)")
    ap.add_argument("--seconds", type=float, default=20.0,
                    help="how long to run (default 20)")
    ap.add_argument("--speed", type=float, default=1.0,
                    help="replay rate multiplier; below 1 if the adapter's "
                         "transmit FIFO fills")
    ap.add_argument("--all-ids", action="store_true",
                    help="replay every identifier, not just the six the "
                         "converter accepts")
    ap.add_argument("--port", help="serial port; guessed if omitted")
    ap.add_argument("--dry-run", action="store_true",
                    help="show what would be replayed and touch no hardware")
    args = ap.parse_args(argv)

    frames, offsets, timed = replay_frames(args.log, args.all_ids)

    print(f"Bench test")
    print(f"  log                   {args.log.name}")
    print(f"  frames per pass       {len(frames)} "
          f"({'adapter timestamps' if timed else 'fixed 10 ms period'})")
    print(f"  pass length           {offsets[-1] / 1000.0 / args.speed:.1f} s")
    print(f"  test length           {args.seconds:.0f} s")

    if args.dry_run:
        print("\nDry run: no adapter opened. First ten frames:")
        for frame, offset in list(zip(frames, offsets))[:10]:
            print(f"  {offset:7d} ms  "
                  f"{slcan_tx(frame.can_id, frame.data).decode()}")
        return 0

    port = args.port or find_port()
    print(f"  adapter               {port}")
    return verdict(run(port, frames, offsets, args.seconds, args.speed))


if __name__ == "__main__":
    raise SystemExit(main())
