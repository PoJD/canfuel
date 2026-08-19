#!/usr/bin/env python3
"""Bench tests for a converter on a desk, with a verdict instead of a blink rate.

docs/install.md step 7, and the last chance to find a fault while the board is
still on a table. --traffic and --scenarios need one adapter and are the two
worth doing whatever else is skipped: loopback in step 6 cannot exercise the
receive path, the acceptance filters or decode, so without these the first run
of any of that is in the car.

    python tools/bench_test.py --list             # find the adapters
    python tools/bench_test.py --all-one-device   # traffic + scenarios
    python tools/bench_test.py --all              # all four, needs two
    python tools/bench_test.py --scenarios        # or one at a time
    python tools/bench_test.py --dry-run          # no hardware at all

The tests run in a fixed order, and it is a prefix: **traffic, scenarios**
(one adapter), then **fault, listen only** (two). So `--all-one-device` is the
front of `--all` rather than a different set of things.

Listen only runs last because it is the only part wanting a different hex.
Anywhere else in the sequence it would cost a third flash; at the end it leaves
the device holding exactly what step 8 asks for next.

**Nothing here prompts, and that is deliberate.** This is meant to be driven
from a session that cannot see the board -- an agent at a terminal, with a
person nearby who can be asked. A prompt would read EOF and answer itself, so
every question is a flag instead. The one thing no frame can report is what the
LEDs were doing in listen only, and that arrives as `--led-can` / `--led-pwr`
on a later invocation; unreported is treated as *unconfirmed*, never as a pass.

Because the LEDs only mean anything while traffic is flowing, 7a holds the bus
alive for `--observe` seconds after its machine checks and says so, rather than
asking once the run has finished and the state is gone.

**Why this beats watching the LED.** LED_CAN encodes the CAN health as a blink
rate, which asks a human to tell 2.5 Hz from 5 Hz correctly, once. The 0x603
diagnostic frame carries the same information as numbers, plus what no LED
could say: which reset started the part, how long it has been up, the module's
own COMSTAT error state, and how many transmissions could not be queued.

⚠ **JP1 must be fitted** or there is no 0x603 at all -- the firmware only
transmits it while somebody is looking. Frames but no 0x603 is a missing
jumper, not a fault.

⚠ **The EEPROM holds bench data afterwards.** These scenarios drive synthetic
tank levels and fuel totals into the persist ring, and in the car that would
read as a wrong trip and a wrong Range. The reflash at the start of step 8
clears it -- do not pass `-Z0-3FF` there -- and the next run's 0x603 proves it,
because PERSIST_OK comes back clear on a virgin ring.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import bench_scenarios as bs
import canlog

# Deferred, not fatal -- see usbtin_capture.require_serial(). Everything in
# this file that decodes a frame, builds a command or grades a result is pure
# Python, and tools/test_bench_test.py exercises exactly that on a runner with
# no pyserial and no adapter. Only Adapter needs the real thing.
try:
    import serial
except ImportError:  # pragma: no cover - depends on the machine
    serial = None

from usbtin_capture import (BEL, BITRATE_CMD, CR, find_port, read_flags,
                            require_serial)

REPO = Path(__file__).resolve().parents[1]
DEFAULT_LOG = REPO / "test" / "fixtures" / "09_idle_60s_z1.txt"

TX_FUEL, TX_ENGINE, TX_TRIP, TX_DIAG = 0x600, 0x601, 0x602, 0x603
TX_IDS = (TX_FUEL, TX_ENGINE, TX_TRIP, TX_DIAG)
# src/config.h TX_SLOT_MS: one frame per slot, and never two.
SLOT_MS = 25

EXPECTED_HZ = {TX_FUEL: 10.0, TX_ENGINE: 10.0, TX_TRIP: 1.0, TX_DIAG: 1.0}
FRAME_NAME = {
    TX_FUEL:   "0x600 fuel   (FuelNow, FuelAvg, FuelTank, Range)",
    TX_ENGINE: "0x601 engine (Power, Torque, Flow, VddConv)",
    TX_TRIP:   "0x602 trip   (litres, metres)",
    TX_DIAG:   "0x603 diag   (errors, reset cause, uptime)",
}

# src/config.h. Copied rather than parsed, and pinned from both sides:
# test/test_txframes.c builds this layout and tools/test_bench_test.py reads it.
DIAG_LAYOUT_VERSION = 1
DIAG_VERSION_SHIFT = 5
DIAG_RESET_CAUSE_MASK = 0x1F

# 0x04 is the latch and 0x20 is the same fault right now -- docs/frames.md.
# LED_CAN follows the second; the first is what says something happened while
# nobody was watching.
DIAG_FLAGS = [(0x01, "CAN_OK"), (0x02, "SILENT"), (0x04, "UNHEALTHY"),
              (0x08, "DATA_LIVE"), (0x10, "PERSIST_OK"),
              (0x20, "UNHEALTHY_NOW")]
RESET_CAUSES = [(0x01, "power-on"), (0x02, "brown-out"), (0x04, "WATCHDOG"),
                (0x08, "RESET instruction"), (0x10, "STACK")]
# DS39977C Register 27-4, COMSTAT bits 5-0.
COMSTAT_BITS = [(0x20, "TXBO bus-off"), (0x10, "TXBP transmit passive"),
                (0x08, "RXBP receive passive"), (0x04, "TXWARN"),
                (0x02, "RXWARN"), (0x01, "EWARN")]

# The USBtin status byte, from the `F` command. Only the top three bits are
# the CAN bus; the rest are the adapter's own queues, and reading a full queue
# as a bus fault is a mistake this file has already made once -- 0x08 is what
# an adapter gets for being handed 610 frames a second while its host is busy,
# and it says nothing whatever about the converter.
ADAPTER_FLAGS = [(0x01, "rx queue full"), (0x02, "tx queue full"),
                 (0x04, "error warning"), (0x08, "DATA OVERRUN"),
                 (0x20, "ERROR PASSIVE"), (0x40, "ARBITRATION LOST"),
                 (0x80, "BUS ERROR")]
ADAPTER_BUS_ERROR = 0x80 | 0x40 | 0x20

ACCEPTED_IDS = {0x1A0, 0x280, 0x288, 0x320, 0x420, 0x480}
# Broadcast by the car, deliberately not accepted by the firmware: nothing
# reads the acceleration and the display takes 0x5A0 off the bus itself.
UNACCEPTED_ID = 0x5A0


def be16(b: bytes, off: int) -> int:
    return b[off] << 8 | b[off + 1]


def slcan_tx(can_id: int, data: bytes) -> bytes:
    """One frame as the adapter's transmit command: tIIILDD.."""
    if not 0 <= can_id <= 0x7FF:
        raise ValueError(f"not an 11-bit identifier: {can_id:#x}")
    if len(data) > 8:
        raise ValueError(f"a CAN frame carries at most 8 bytes, not {len(data)}")
    return f"t{can_id:03X}{len(data):X}{data.hex().upper()}".encode()


def decode_diag(data: bytes) -> dict:
    """0x603, laid out in src/config.h and docs/frames.md."""
    if len(data) != 8:
        raise ValueError(f"0x603 should carry 8 bytes, not {len(data)}")
    return {
        "rx_err": data[0], "tx_err": data[1], "comstat": data[2],
        "flags": data[3],
        "reset_cause": data[4] & DIAG_RESET_CAUSE_MASK,
        "version": data[4] >> DIAG_VERSION_SHIFT,
        "tx_fail": data[5], "uptime_s": be16(data, 6),
    }


def names(value: int, table) -> str:
    hits = [name for bit, name in table if value & bit]
    return " ".join(hits) if hits else "none"


def replay_frames(log, every_id: bool):
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


# --------------------------------------------------------------------------
# the adapter
# --------------------------------------------------------------------------

class Adapter:
    """One USBtin, opened and driven directly.

    Deliberately not usbtin_capture.command(): that helper reads until CR and
    treats whatever arrives as the answer, which is right for a capture and
    wrong here, where our own transmit acknowledgements are interleaved with
    incoming frames and have to be sorted rather than assumed.
    """

    def __init__(self, port: str, label: str):
        require_serial()
        self.port = port
        self.label = label
        self.ser = serial.Serial(port, baudrate=115200, timeout=0)
        self._pending = bytearray()
        self.rx: dict[int, list[float]] = {}
        # THE ADAPTER'S OWN CLOCK, kept separately from the host's. rx above is
        # taken when pump() got round to reading the port, which is fine for a
        # rate over thirty seconds and useless below about fifty milliseconds:
        # while the host is replaying 357 frames a second it reads several
        # frames in one go and stamps them all alike. The USBtin's Z1
        # timestamp is applied when the frame arrived, so it is the only one
        # that can answer how far apart two frames really were. It wraps at
        # 60000 ms -- see adapter_gaps_ms().
        self.ts: dict[int, list[int]] = {}
        self.first: dict[int, bytes] = {}
        self.last: dict[int, bytes] = {}
        self._close_channel()

    def _cmd(self, cmd: bytes) -> None:
        self.ser.write(cmd + CR)
        self.ser.flush()
        time.sleep(0.05)

    def _close_channel(self) -> None:
        # A channel left open by a previous run answers BEL to `C`, which is
        # why this one is not checked.
        self._cmd(b"C")
        self.ser.reset_input_buffer()
        self._pending.clear()

    def firmware(self, timeout: float = 1.0) -> str | None:
        """The adapter's own version string, and proof it is answering at all.

        A USBtin can stop responding while its serial port stays enumerated and
        writable -- unplug and replug is the cure. Until this check existed, a
        run against a wedged adapter reported `sent 8931 frames` and then four
        rate failures, which reads exactly like a converter that has stopped
        transmitting. It cost an afternoon, and the converter was fine
        throughout: a second adapter heard every frame at its nominal rate.
        """
        self.ser.reset_input_buffer()
        self._pending.clear()
        self.ser.write(b"V" + CR)
        self.ser.flush()
        deadline = time.monotonic() + timeout
        buf = bytearray()
        while time.monotonic() < deadline:
            buf += self.ser.read(64)
            while CR in buf:
                raw, _, rest = bytes(buf).partition(CR)
                buf = bytearray(rest)
                text = raw.strip(BEL).strip()
                if text.startswith(b"V"):
                    return text.decode(errors="replace")
        return None

    def open(self, *, listen_only: bool = False, bitrate: bytes = BITRATE_CMD):
        self._close_channel()
        if self.firmware() is None:
            sys.exit(
                f"\n{self.label} on {self.port} is not answering.\n"
                "The port is open and writable, so this is the adapter itself "
                "rather than the cable or the converter:\n"
                "  unplug its USB, plug it back in, and run this again.\n"
                "Nothing was measured -- frames written to a wedged adapter go "
                "nowhere and would have read as a silent converter.")
        self._cmd(bitrate)
        self._cmd(b"Z1")        # timestamps, for check_frame_spacing()
        self._cmd(b"L" if listen_only else b"O")
        self.ser.reset_input_buffer()
        self._pending.clear()
        return self

    def close(self) -> None:
        self._cmd(b"C")

    def release(self) -> None:
        try:
            self.close()
        finally:
            self.ser.close()

    def send(self, can_id: int, data: bytes) -> None:
        self.ser.write(slcan_tx(can_id, data) + CR)

    def pump(self) -> None:
        """Read whatever has arrived and sort frames from acknowledgements."""
        chunk = self.ser.read(4096)
        if chunk:
            self._pending += chunk
        now = time.monotonic()
        while CR in self._pending:
            raw, _, rest = self._pending.partition(CR)
            self._pending = bytearray(rest)
            text = bytes(raw).strip(BEL).strip()
            if not text or text[:1] in (b"z", b"Z"):
                continue
            frame = canlog.parse_line(text.decode(errors="replace"))
            if frame is not None:
                self.rx.setdefault(frame.can_id, []).append(now)
                if frame.ts_ms is not None:
                    self.ts.setdefault(frame.can_id, []).append(frame.ts_ms)
                self.first.setdefault(frame.can_id, frame.data)
                self.last[frame.can_id] = frame.data

    def forget(self) -> None:
        self.rx.clear()
        self.ts.clear()
        self.first.clear()
        self.last.clear()

    def flags(self) -> int | None:
        self.ser.timeout = 0.1
        try:
            text = read_flags(self.ser).decode(errors="replace").strip()
        finally:
            self.ser.timeout = 0
        if text.startswith("F") and len(text) >= 3:
            return int(text[1:3], 16)
        return None

    def count(self, can_id: int) -> int:
        return len(self.rx.get(can_id, []))


class Report:
    def __init__(self):
        self.rows: list[tuple[str, bool, str]] = []

    def check(self, name: str, ok: bool, detail: str = "") -> bool:
        self.rows.append((name, ok, detail))
        print(f"    [{'ok  ' if ok else 'FAIL'}] {name}"
              + (f" -- {detail}" if detail else ""))
        return ok

    def note(self, text: str) -> None:
        print(f"           {text}")

    @property
    def failed(self) -> list[str]:
        return [f"{n}: {d}" if d else n for n, ok, d in self.rows if not ok]


def pump_until(deadline: float, adapters) -> None:
    while time.monotonic() < deadline:
        for a in adapters:
            a.pump()
        time.sleep(0.001)


def feed(stream: bs.Stream, sender: Adapter, listeners, seconds: float,
         *, flood: int = 0) -> float:
    """Drive one condition onto the bus for `seconds`, pumping throughout.

    Returns the fraction of the intended ticks that actually went out. Worth
    returning rather than assuming: six frames every 10 ms is 600 a second,
    and at 22 bytes of slcan text each that is 132 kbit/s against a link
    nominally running at 115200. The USBtin is a USB CDC device, so the
    configured baud rate is not the real limit -- but if the write buffer ever
    does back up, the schedule below slips, a scenario runs at less than the
    condition it claims, and nothing would say so. Hence the number.
    """
    started = time.monotonic()
    tick = 0
    while True:
        now = time.monotonic()
        if now - started >= seconds:
            break
        due = started + tick * bs.Stream.TICK_MS / 1000.0
        if now >= due:
            for can_id, data in stream.tick():
                sender.send(can_id, data)
            for _ in range(flood):
                sender.send(UNACCEPTED_ID, bytes(8))
            tick += 1
        for a in listeners:
            a.pump()
        time.sleep(0)
    intended = max(1, round(seconds * 1000 / bs.Stream.TICK_MS))
    return tick / intended


def listen(listeners, seconds: float) -> None:
    """Pump without transmitting anything at all."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        for a in listeners:
            a.pump()
        time.sleep(0.001)


def check_clock(rep: Report, listener: Adapter, elapsed: float) -> None:
    """Does the converter's own second agree with the host's?

    Everything the device reports is integrated against its millisecond clock:
    16 MHz / 4, prescale 4, PR2 = 249, postscale 4. Get any link in that chain
    wrong and it still runs, still transmits, and every distance, flow and
    average is scaled by the error -- with nothing on the display to suggest
    it, because a wrong clock produces plausible numbers.

    Nothing else in this project can catch that. The host tests feed the core a
    clock of their own, and the fixtures cannot check a clock they were
    recorded with. Two 0x603 frames and a wall clock can.
    """
    stamps = listener.rx.get(TX_DIAG, [])
    if len(stamps) < 2 or TX_DIAG not in listener.first:
        rep.note("too few 0x603 frames to check the clock")
        return

    first = decode_diag(listener.first[TX_DIAG])
    last = decode_diag(listener.last[TX_DIAG])
    device_s = last["uptime_s"] - first["uptime_s"]
    host_s = stamps[-1] - stamps[0]
    if device_s <= 0 or host_s <= 0:
        rep.note("the uptime did not advance; cannot check the clock")
        return

    error = (device_s - host_s) / host_s
    # The device counts whole seconds, so one count of quantisation over a
    # 20 s window is already 5 %. The tolerance has to sit outside that or it
    # measures the rounding rather than the crystal: at 20 s it allows 2 %
    # plus a second, which a real divider mistake (a factor, not a percent)
    # blows through immediately.
    allowed = 0.02 + 1.0 / host_s
    rep.check("the converter's clock agrees with the host's",
              abs(error) <= allowed,
              f"device counted {device_s} s while the host saw {host_s:.1f} s "
              f"({error:+.1%}); a divider mistake scales every distance and "
              f"flow by the same factor")


def latest_diag(listener: Adapter):
    raw = listener.last.get(TX_DIAG)
    return decode_diag(raw) if raw else None


def explain_unhealthy(diag: dict, rep: Report) -> None:
    """UNHEALTHY with clean counters is a bench artefact, and it looks awful.

    It cost most of a day once, so it is explained here rather than left to be
    rediscovered. Between a flash and the moment this script opens its adapter,
    nothing on the bench bus acknowledges anything -- the converter is the only
    node with its channel open. So every frame it transmits goes unacknowledged
    and is retransmitted for as long as that lasts, its transmit error counter
    climbs, all three transmit buffers stay busy and hal_can_send() starts
    refusing. The latch remembers all of it.

    Then the adapter opens, the very next frame is acknowledged, the module
    recovers on its own within a few bit times and both counters reset -- which
    is exactly what makes the latch worth having and exactly what makes it
    unreadable here. In the car this cannot happen: the bus is alive before the
    converter is.

    The signature is specific, so say so only when it fits: UNHEALTHY set, both
    error counters zero now, and refusals greater than zero.
    """
    unhealthy = diag["flags"] & 0x04
    if not unhealthy:
        return
    # The refusal count is the fingerprint, not the counters. Refusals happen
    # only when all three transmit buffers are busy at once, which is what
    # starvation looks like and nothing else here does; the counters may still
    # be walking down from it while this runs, one per frame acknowledged.
    if diag["tx_fail"] > 0 and (diag["comstat"] & 0x38) == 0:
        rep.note("UNHEALTHY is latched but both counters are zero and there "
                 f"are {diag['tx_fail']} refusals: that is the converter "
                 "having transmitted into a bus nobody was acknowledging, "
                 "between the flash and this run. Normal on the bench, "
                 "impossible in the car. Power-cycle the board with the bus "
                 "already alive to see it clear.")
    else:
        rep.note("UNHEALTHY is latched and the counters do NOT fit the "
                 "bench's own start-up storm -- this one is worth chasing.")


def show_diag(diag: dict, rep: Report, *, expect_clean: bool = True) -> None:
    rep.note(f"rx err {diag['rx_err']}, tx err {diag['tx_err']}, "
             f"COMSTAT {names(diag['comstat'], COMSTAT_BITS)}")
    rep.note(f"flags {names(diag['flags'], DIAG_FLAGS)}, "
             f"reset {names(diag['reset_cause'], RESET_CAUSES)}, "
             f"uptime {diag['uptime_s']} s, refusals {diag['tx_fail']}")
    if expect_clean:
        rep.check("CAN error counters are zero",
                  diag["rx_err"] == 0 and diag["tx_err"] == 0,
                  f"rx {diag['rx_err']}, tx {diag['tx_err']}")
        rep.check("the module reports no error state", diag["comstat"] == 0,
                  names(diag["comstat"], COMSTAT_BITS))
    rep.check("the last reset was not the watchdog",
              not diag["reset_cause"] & 0x04)
    # DS39977C 5.4.2: BOR resets to 0 on a power-on as well as on a brown-out,
    # so the pair is the reading and 0x02 alone is not. Every cold start of
    # this board reports both, which is the hardware working -- and this check
    # used to call it a fault in the one test whose whole method is pulling the
    # power.
    rep.check("the last reset was not a brown-out",
              not (diag["reset_cause"] & 0x02
                   and not diag["reset_cause"] & 0x01),
              "power-on sets BOR too; only BOR without POR is a sagging supply"
              if diag["reset_cause"] & 0x02 else "")
    rep.check("0x603 layout is the one this script speaks",
              diag["version"] == DIAG_LAYOUT_VERSION,
              f"frame says {diag['version']}")
    explain_unhealthy(diag, rep)


# --------------------------------------------------------------------------
# 7a -- listen only
# --------------------------------------------------------------------------

def mode_listen_only(sender: Adapter, acker: Adapter, log, seconds: float,
                     observe: float, led_can: str, led_pwr: str) -> Report:
    print("\n7a  LISTEN ONLY -- the converter must receive and stay silent")
    rep = Report()
    tpl = bs.templates(log)
    stream = bs.Stream(tpl, bs.Condition(speed_kmh=50, rpm=2000,
                                         throttle=60, flow_ul_s=800))

    # The second adapter is opened normally and never transmits. That is the
    # whole of its job: something has to drive the acknowledge slot, and a
    # listen-only converter never will (DS39977C 27.3.4). Without it the
    # sender goes bus-off in milliseconds.
    sender.open()
    acker.open()
    for a in (sender, acker):
        a.forget()

    feed(stream, sender, (sender, acker), seconds)
    pump_until(time.monotonic() + 0.5, (sender, acker))

    heard = {i: sender.count(i) + acker.count(i) for i in TX_IDS}
    rep.check("the converter transmitted nothing at all",
              sum(heard.values()) == 0,
              ", ".join(f"{i:#05x} x{n}" for i, n in heard.items() if n))
    for label, a in (("sender", sender), ("acker", acker)):
        f = a.flags()
        rep.check(f"the {label} adapter saw no bus errors",
                  f is not None and (f & ADAPTER_BUS_ERROR) == 0,
                  "no answer" if f is None else
                  f"flags {f:#04x} -- {names(f, ADAPTER_FLAGS)}")
    rep.note("bus errors here would mean the second adapter is not "
             "acknowledging -- check it opened with O, not L")

    # The only channel left. In listen only the converter cannot tell us
    # anything at all, so this one answer has to come from somebody looking at
    # the board -- and the LEDs only mean anything WHILE traffic is flowing,
    # which is why the window below keeps the bus alive rather than asking
    # after the run has ended and the state is gone.
    if observe > 0:
        print()
        print("    " + "-" * 68)
        print("    LOOK AT THE BOARD NOW -- traffic is live for "
              f"{observe:.0f} more seconds.")
        print("    Expected: LED_CAN steady, LED_PWR blinking slowly.")
        print("      LED_CAN blinking   errors, or it never reached the mode")
        print("      LED_CAN dark       nothing is arriving at all")
        print("      LED_PWR steady     a normal build is flashed, not this one")
        print("    " + "-" * 68)
        sys.stdout.flush()
        deadline = time.monotonic() + observe
        while time.monotonic() < deadline:
            feed(stream, sender, (sender, acker), 1.0)
    record_leds(rep, led_can, led_pwr)
    return rep


def record_leds(rep: Report, led_can: str, led_pwr: str) -> None:
    """Fold an observed LED state into the verdict.

    Flags rather than a prompt, because this is driven from a session that
    cannot see the board: the observation arrives on a later invocation, or it
    does not arrive. "unknown" is reported as unconfirmed and never as a pass
    -- an unanswered question is not a green light.
    """
    if led_can == "unknown" and led_pwr == "unknown":
        rep.note("LED state not reported. 7a is INCOMPLETE without it -- "
                 "re-run with --led-can/--led-pwr once somebody has looked.")
        return
    rep.check("LED_CAN was steady", led_can == "steady",
              f"reported {led_can}")
    rep.check("LED_PWR was blinking slowly", led_pwr == "slow",
              f"reported {led_pwr}"
              + ("; steady means a normal build is flashed"
                 if led_pwr == "steady" else ""))


# --------------------------------------------------------------------------
# 7b -- traffic
# --------------------------------------------------------------------------

def adapter_gaps_ms(listener: "Adapter") -> list[int]:
    """Gaps between consecutive frames of ours, on the adapter's clock.

    The Z1 timestamp counts milliseconds and wraps at 60000, so a decrease is
    a wrap rather than time running backwards. Anything still negative after
    that correction is a reordering the adapter should not produce, and it is
    dropped rather than reported as a suspiciously small gap -- this check
    exists to catch two frames leaving together, and inventing one out of a
    parsing artefact would be worse than missing one.
    """
    stamps = sorted(t for can_id in TX_IDS for t in listener.ts.get(can_id, ()))
    gaps = []
    for a, b in zip(stamps, stamps[1:]):
        gap = b - a
        if gap < 0:
            gap += 60000
        if 0 <= gap < 60000:
            gaps.append(gap)
    return gaps


def check_frame_spacing(rep: "Report", listener: "Adapter") -> None:
    """No two of the converter's frames may arrive back to back.

    THIS CHECK EXISTS BECAUSE A BENCH RUN FOUND THE FAULT IT LOOKS FOR, and it
    cost most of a day to understand. The firmware used to send 0x600 and
    0x601 together every 100 ms and 0x602 and 0x603 behind them once a second
    -- three or four frames inside one millisecond at 500 kbps. Both USBtins
    dropped whichever of ours came third on the wire, silently, without
    setting their own overrun flag, on an otherwise empty bus. The converter
    was never at fault: the ECAN module reported every one of those frames as
    successfully transmitted, which in CAN requires somebody else's
    acknowledgement.

    So the converter now spaces its frames one per TX_SLOT_MS, and this is
    what proves it still does. A regression would look exactly like the
    original symptom: one frame's rate collapses and nothing else changes.

    IT IS MEASURED ON THE ADAPTER'S CLOCK AND IT HAS TO BE. The first version
    of this check used the host's arrival times and reported 0.0 ms on a
    converter that was in fact spacing its frames perfectly: while the host is
    replaying 357 frames a second it reads several at once and stamps them
    alike. The Z1 timestamp is applied when the frame arrived. Measured
    against a good build it gives 23-27 ms between neighbouring slots and
    75-77 ms across the three empty ones.

    THE LONGEST GAP IS WORTH READING TOO. The EEPROM write blocks for about
    48 ms, and main.c drops the slot it lands in rather than catching up --
    so a write shows up here as one stretched gap and never as two frames
    arriving together. A build that caught up instead would pass every rate
    check in this file and fail this one.
    """
    gaps = adapter_gaps_ms(listener)
    if len(gaps) < 10:
        rep.check("the converter spaces its frames out", False,
                  f"only {len(gaps) + 1} timestamped frames to measure -- the "
                  f"adapter has to be opened with Z1 for this")
        return

    smallest = min(gaps)
    rep.check("the converter spaces its frames out", smallest >= SLOT_MS - 5,
              f"closest two frames were {smallest} ms apart and one slot is "
              f"{SLOT_MS} ms; the longest gap was {max(gaps)} ms, which is the "
              f"EEPROM write and must stretch a gap rather than shorten one")


def mode_traffic(sender: Adapter, listener: Adapter, log, seconds: float,
                 speed: float, every_id: bool) -> Report:
    print("\n7b  TRAFFIC -- a real recording, replayed, and the answers read back")
    rep = Report()
    frames, offsets, timed = replay_frames(log, every_id)
    rep.note(f"{Path(log).name}: {len(frames)} frames per pass, "
             f"{'adapter timestamps' if timed else 'fixed 10 ms period'}")

    sender.open()
    if listener is not sender:
        listener.open()
    for a in {sender, listener}:
        a.forget()

    sent = 0
    started = time.monotonic()
    span = (offsets[-1] + 1) / 1000.0 / speed
    loop = 0
    while time.monotonic() - started < seconds:
        base = started + loop * span
        for frame, offset in zip(frames, offsets):
            due = base + offset / 1000.0 / speed
            while time.monotonic() < due:
                for a in {sender, listener}:
                    a.pump()
                if time.monotonic() - started >= seconds:
                    break
                time.sleep(0)
            if time.monotonic() - started >= seconds:
                break
            sender.send(frame.can_id, frame.data)
            sent += 1
        loop += 1
    elapsed = time.monotonic() - started
    pump_until(time.monotonic() + 0.5, {sender, listener})

    # What the host wrote to the adapter, which is not the same as what
    # reached the wire -- see Adapter.firmware(). The counts below are the
    # measurement; this line is only the stimulus we asked for.
    rep.note(f"wrote {sent} frames to the adapter in {elapsed:.1f} s "
             f"({sent / elapsed:.0f}/s)")
    for can_id in TX_IDS:
        n = listener.count(can_id)
        hz = n / elapsed if elapsed else 0.0
        want = EXPECTED_HZ[can_id]
        ok = n > 0 and want * 0.5 <= hz <= want * 1.8
        rep.check(f"{FRAME_NAME[can_id]}", ok,
                  f"{n} frames, {hz:.1f} Hz, expected about {want:.0f} Hz")
        if n == 0 and can_id == TX_DIAG:
            rep.note("no 0x603 at all -- is JP1 fitted?")

    check_frame_spacing(rep, listener)

    f = sender.flags()
    if f is not None and f & 0x02:
        rep.note("the adapter's transmit FIFO filled: that is the host, "
                 "not the converter. Try --speed 0.5")

    diag = latest_diag(listener)
    if diag:
        show_diag(diag, rep)
        rep.check("the converter did not restart during the run",
                  diag["uptime_s"] >= elapsed - 2,
                  f"uptime {diag['uptime_s']} s over a {elapsed:.0f} s run")
        check_clock(rep, listener, elapsed)
    else:
        rep.check("0x603 was received", False, "none seen")

    fuel = listener.last.get(TX_FUEL)
    eng = listener.last.get(TX_ENGINE)
    if fuel and eng:
        rep.note(f"FuelNow {be16(fuel, 0) / 10:.1f}  "
                 f"FuelAvg {be16(fuel, 2) / 10:.1f} l/100km  "
                 f"FuelTank {be16(fuel, 4) / 10:.1f} l  "
                 f"Range {be16(fuel, 6)} km")
        vdd = be16(eng, 6) / 100
        rep.check("VddConv is a believable supply voltage",
                  4.5 <= vdd <= 5.5, f"{vdd:.2f} V")
    return rep


# --------------------------------------------------------------------------
# 7c -- scenarios A to D
# --------------------------------------------------------------------------

class HealthWatch:
    """Which scenario latched UNHEALTHY, rather than merely that one did.

    UNHEALTHY is latched since power-up and never clears by itself, so reading
    it once at the end of a run says only that something, somewhere, saw an
    overflow or an error counter move. That is what made the LED useless as
    evidence -- it starts blinking and stays blinking, and the only witness to
    WHEN is a person watching it. Sampled between scenarios it names the one
    that did it, which is the whole difference between a lead and a shrug.

    A latch that was already set before the scenarios began cannot be improved
    on: there is no transition left to see, so say so once and stop asking.
    """

    def __init__(self, listener: "Adapter", rep: "Report"):
        self.listener = listener
        self.rep = rep
        self.set = False

    def _read(self):
        diag = latest_diag(self.listener)
        return None if diag is None else bool(diag["flags"] & 0x04)

    def start(self) -> None:
        self.set = bool(self._read())
        if self.set:
            self.rep.note("UNHEALTHY is latched before the scenarios even "
                          "start, so none of them can be blamed for it. "
                          "Reflash or power-cycle the board with the bus "
                          "already alive and run this again if you need to "
                          "know which one is at fault.")

    def check(self, label: str) -> None:
        now = self._read()
        if now is None:
            self.rep.note(f"{label}: no 0x603 to read the health from")
            return
        if self.set:
            return
        # The detail is printed whether the check passed or failed, so it has
        # to read as a fact rather than as an explanation of a failure.
        self.rep.check(f"{label} left the converter healthy", not now,
                       "UNHEALTHY is set and was clear before this scenario, "
                       "so an overflow or an error counter moved inside this "
                       "one" if now else "UNHEALTHY still clear")
        self.set = now


def settle(stream, sender, listeners, seconds, *, flood=0, rep=None):
    for a in listeners:
        a.forget()
    kept = feed(stream, sender, listeners, seconds, flood=flood)
    pump_until(time.monotonic() + 0.3, listeners)
    if kept < 0.9 and rep is not None:
        rep.note(f"WARNING: the host kept only {kept:.0%} of the intended frame rate "
                 "-- the serial link is the bottleneck, not the converter. "
                 "Results below are for a slower stream than asked for.")
    return kept


def mode_scenarios(sender: Adapter, listener: Adapter, log) -> Report:
    print("\n7c  SCENARIOS -- four behaviours, end to end over the wire")
    rep = Report()
    tpl = bs.templates(log)
    both = {sender, listener}
    sender.open()
    if listener is not sender:
        listener.open()

    # -- A: the bus goes quiet, then comes back with the counter reset -----
    print("\n  A  the bus goes quiet, then returns after an ignition cycle")
    cruise = bs.Condition(speed_kmh=50, rpm=2200, throttle=70, flow_ul_s=900)
    stream = bs.Stream(tpl, cruise)
    settle(stream, sender, both, 6, rep=rep)
    health = HealthWatch(listener, rep)
    health.start()
    rep.check("values are live while traffic flows",
              be16(listener.last.get(TX_FUEL, bytes(8)), 0) > 0)

    listener.forget()
    pump_until(time.monotonic() + 2.0, both)      # DATA_TIMEOUT_MS is 500
    fuel = listener.last.get(TX_FUEL)
    eng = listener.last.get(TX_ENGINE)
    rep.check("a quiet bus zeroes everything derived from it",
              fuel is not None and be16(fuel, 0) == 0 and be16(fuel, 6) == 0,
              "FuelNow and Range must both read 0")
    rep.check("VddConv survives a quiet bus",
              eng is not None and be16(eng, 6) > 0,
              "it is measured by the PIC on itself, not read off the bus")
    diag = latest_diag(listener)
    if diag:
        rep.check("DATA_LIVE is clear while the bus is quiet",
                  not diag["flags"] & 0x08)

    stream.restart()          # what an ignition-off really does to the counter
    settle(stream, sender, both, 4, rep=rep)
    rep.check("it recovers when traffic returns",
              be16(listener.last.get(TX_FUEL, bytes(8)), 0) > 0)
    rep.check("a counter restart invents no fuel",
              be16(listener.last.get(TX_FUEL, bytes(8)), 0) <= 999,
              "trap 2: the delta must not jump when the ECU counter resets")
    health.check("A")

    # -- B: FuelNow units and the clamp ------------------------------------
    print("\n  B  FuelNow switches unit at 4 km/h, and stops at 99.9")
    for label, cond in (
            ("2 km/h, so l/h", bs.Condition(speed_kmh=2, rpm=900,
                                            throttle=45, flow_ul_s=1000)),
            ("60 km/h, so l/100 km", bs.Condition(speed_kmh=60, rpm=2200,
                                                  throttle=70,
                                                  flow_ul_s=1000)),
            ("5 km/h at a wild flow, so clamped",
             bs.Condition(speed_kmh=5, rpm=3000, throttle=90,
                          flow_ul_s=3000))):
        stream = bs.Stream(tpl, cond)
        settle(stream, sender, both, 5, rep=rep)
        got = be16(listener.last.get(TX_FUEL, bytes(8)), 0)
        want = cond.fuel_now_d()
        rep.check(f"FuelNow at {label}", abs(got - want) <= max(2, want // 10),
                  f"read {got / 10:.1f}, expected about {want / 10:.1f}")
    rep.check("FuelNow never exceeds the gauge", got <= 999, f"read {got}")
    health.check("B")

    # -- C: the driving gate ------------------------------------------------
    print("\n  C  standing still with the throttle shut shows zero torque")
    idle = bs.Condition(speed_kmh=0.005, rpm=800, throttle=bs.THROTTLE_REST,
                        torque_b7=42, flow_ul_s=330)
    settle(bs.Stream(tpl, idle), sender, both, 5)
    eng = listener.last.get(TX_ENGINE, bytes(8))
    rep.check("Torque reads exactly zero", be16(eng, 2) == 0,
              f"read {be16(eng, 2) / 10:.1f} Nm")
    rep.check("Power reads exactly zero", be16(eng, 0) == 0,
              f"read {be16(eng, 0) / 10:.1f} kW")
    rep.note("b7 is 42 here, the value the air conditioning raises it to -- "
             "the gate must still hold")
    health.check("C")

    # -- D: the hardware acceptance filters ---------------------------------
    print("\n  D  an identifier we do not accept, flooded alongside real traffic")
    stream = bs.Stream(tpl, cruise)
    settle(stream, sender, both, 5, rep=rep)
    clean_rate = listener.count(TX_FUEL) / 5.0

    settle(stream, sender, both, 6, flood=4, rep=rep)
    flooded_rate = listener.count(TX_FUEL) / 6.0
    rep.note(f"0x600 arrived at {clean_rate:.1f} Hz clean, "
             f"{flooded_rate:.1f} Hz under flood")
    rep.check("the flood did not slow the answers down",
              flooded_rate >= clean_rate * 0.8,
              "if the six hardware filters leaked, the FIFO would fill with "
              "0x5A0 and real frames would be dropped")
    rep.check("values stayed correct under flood",
              be16(listener.last.get(TX_FUEL, bytes(8)), 0) > 0)
    diag = latest_diag(listener)
    if diag:
        # UNHEALTHY belongs to HealthWatch, which can tell a latch this
        # scenario caused from one it inherited. What is D's own to check is
        # that the flood did not push the receive error counter up.
        rep.check("the flood left the receive error counter at zero",
                  diag["rx_err"] == 0,
                  f"rx err {diag['rx_err']}, "
                  f"flags {names(diag['flags'], DIAG_FLAGS)}")
    health.check("D")
    rep.note("this is the only test of the six acceptance filters anywhere -- "
             "they exist only in silicon")

    # -- E: refuelling resets the trip --------------------------------------
    print("\n  E  a refuelling, which resets the trip average")
    rep.note("the rule is REFUEL_CONFIRM_S consecutive at-rest samples more "
             "than REFUEL_RISE_L above the settled level, and the settled "
             "level is a 16 s filter -- so this scenario is slow by nature")
    rest = bs.Condition(speed_kmh=0.005, rpm=800, throttle=bs.THROTTLE_REST,
                        tank_l=20, flow_ul_s=330)
    stream = bs.Stream(tpl, rest)
    settle(stream, sender, both, 75, rep=rep)     # ~5 tau for the rest filter
    before = listener.last.get(TX_TRIP)
    rep.check("the trip accumulated while standing",
              before is not None and int.from_bytes(before[0:4], "big") > 0,
              "fuel burns at idle even though distance does not")

    stream.cond = bs.Condition(speed_kmh=0.005, rpm=800,
                               throttle=bs.THROTTLE_REST,
                               tank_l=32, flow_ul_s=330)   # a 12 litre fill
    settle(stream, sender, both, 12, rep=rep)
    after = listener.last.get(TX_TRIP, bytes(8))
    rep.check("the trip reset when the tank rose while at rest",
              int.from_bytes(after[0:4], "big") <
              int.from_bytes((before or bytes(8))[0:4], "big"),
              "0x602 TripFuel must drop, not keep climbing")
    rep.note("otherwise this is only testable at a petrol station, and "
             "getting it wrong means the average never clears -- or clears "
             "on its own halfway through a drive")
    health.check("E")
    return rep


# --------------------------------------------------------------------------
# 7.5 -- the accumulators survive a power cycle
# --------------------------------------------------------------------------

# The one path in this firmware that nothing else can execute. test_persist.c
# simulates 100,000 write cycles against a RAM array, which proves the ring
# arithmetic and the wear levelling and says nothing at all about
# hal_eeprom_write(): the 0x55/0xAA unlock, WREN, polling WR, and the decision
# to restore GIE while that poll runs. That was datasheet reading with no
# silicon behind it until this test was first run, and it is still the only
# thing that puts silicon behind it -- so it is worth running again after
# anything touches persist.c or the write. The consequence of getting it wrong
# is invisible: the device works perfectly until the ignition goes off, and
# then loses every trip.

def mode_persist_arm(sender: Adapter, listener: Adapter, log) -> Report:
    print("\n7.5  PERSISTENCE, part 1 -- put something in the EEPROM")
    rep = Report()
    tpl = bs.templates(log)
    both = {sender, listener}
    sender.open()
    if listener is not sender:
        listener.open()

    stream = bs.Stream(tpl, bs.Condition(speed_kmh=60, rpm=2200, throttle=70,
                                         flow_ul_s=1200))
    # PERSIST_INTERVAL_MS is 20 s and persist_save() also refuses when nothing
    # changed, so 30 s of moving traffic guarantees at least one real write.
    settle(stream, sender, both, 30, rep=rep)

    trip = listener.last.get(TX_TRIP)
    rep.check("the trip accumulated", trip is not None and
              int.from_bytes(trip[0:4], "big") > 0)
    if trip is None:
        return rep

    trip_ml = int.from_bytes(trip[0:4], "big")
    trip_m = int.from_bytes(trip[4:8], "big")
    diag = latest_diag(listener)
    if diag:
        show_diag(diag, rep)

    print()
    print("    " + "-" * 68)
    print(f"    Trip is now {trip_ml} ml over {trip_m} m.")
    print("    POWER-CYCLE THE BOARD NOW -- pull the 5 V and put it back.")
    print("    Then run:")
    print(f"      python tools/bench_test.py --persist-check "
          f"--expect-trip-ml {trip_ml} --port ...")
    print("    " + "-" * 68)
    return rep


def mode_persist_check(sender: Adapter, listener: Adapter, log,
                       expect_ml: int) -> Report:
    print("\n7.5  PERSISTENCE, part 2 -- did it come back?")
    rep = Report()
    tpl = bs.templates(log)
    both = {sender, listener}
    sender.open()
    if listener is not sender:
        listener.open()

    stream = bs.Stream(tpl, bs.Condition(speed_kmh=60, rpm=2200, throttle=70,
                                         flow_ul_s=1200))
    settle(stream, sender, both, 6, rep=rep)

    diag = latest_diag(listener)
    if diag is None:
        rep.check("0x603 was received", False, "none seen")
        return rep
    # Not expect_clean: the board has just been power-cycled onto a bench bus
    # that nothing acknowledged until this run opened its adapter, so its
    # transmit error counter is still walking down from the starvation that
    # caused. That is the bench, not the converter, and it is exactly the
    # state this test has to be able to run in.
    show_diag(diag, rep, expect_clean=False)

    rep.check("the board really was power-cycled",
              bool(diag["reset_cause"] & 0x01),
              f"reset cause reads {names(diag['reset_cause'], RESET_CAUSES)}; "
              "without a power-on this test proves nothing")
    rep.check("PERSIST_OK is set, so a stored record was found",
              bool(diag["flags"] & 0x10),
              "clear means persist_load() found nothing -- either the write "
              "never happened or the ring cannot be read back")

    trip = listener.last.get(TX_TRIP, bytes(8))
    got_ml = int.from_bytes(trip[0:4], "big")
    # Up to PERSIST_INTERVAL_MS of accumulator is lost at every power-off by
    # design, and six seconds of fresh traffic is added on top, so this is a
    # band rather than an equality. src/persist.h has the arithmetic.
    floor = int(expect_ml * 0.5)
    rep.check("the trip came back rather than starting from zero",
              got_ml >= floor,
              f"read {got_ml} ml, expected at least {floor} of the "
              f"{expect_ml} ml stored -- up to 20 s of it is lost by design")
    return rep


# --------------------------------------------------------------------------
# 7e -- a broken bus, and recovery
# --------------------------------------------------------------------------

def mode_fault(sender: Adapter, acker: Adapter, log) -> Report:
    print("\n7e  FAULT INJECTION -- break the bus, then prove it recovers")
    rep = Report()
    tpl = bs.templates(log)
    both = {sender, acker}
    cruise = bs.Condition(speed_kmh=50, rpm=2200, throttle=70, flow_ul_s=900)
    stream = bs.Stream(tpl, cruise)

    sender.open()
    acker.open()
    settle(stream, sender, both, 5, rep=rep)
    baseline = latest_diag(acker)
    # No ERROR STATE, rather than no error count. TEC decrements by one per
    # successful transmission, so a converter that has just come off a bench
    # bus nobody was acknowledging is still walking a three-figure counter down
    # while this runs, and that is not a reason to refuse to start. TXBO, TXBP
    # and RXBP are the states; TXWARN, RXWARN and EWARN are only the warning
    # threshold at 96 (DS39977C Register 27-4).
    rep.check("no error state before the fault",
              baseline is not None and (baseline["comstat"] & 0x38) == 0,
              "" if baseline is None else
              f"COMSTAT {names(baseline['comstat'], COMSTAT_BITS)}, "
              f"tx err {baseline['tx_err']}")

    # -- E1: nobody acknowledges -------------------------------------------
    print("\n  E1  starve the converter of acknowledgements")
    rep.note("both adapters go listen-only, so nothing on the bus drives the "
             "ACK slot and the converter's TEC climbs by 8 per failed try")
    rep.note("no stimulus is sent during this window, and cannot be: an "
             "adapter in listen-only refuses to transmit. The only thing on "
             "the wire is the converter's own frames, which is all this needs")
    rep.note("IT DOES NOT GO BUS-OFF, and this test used to expect that it "
             "would. TEC stops at the error-passive limit of 128 and stays "
             "there: DS39977C 27.14.7 counts 'in accordance with the CAN bus "
             "specification', and the specification does not increase TEC when "
             "an already error-passive transmitter sees an acknowledge error "
             "and no dominant bit during its passive error flag. So a lone "
             "node retransmits for ever instead of falling silent -- measured "
             "here, and again in the storm every bench flash produces")
    sender.open(listen_only=True)
    acker.open(listen_only=True)
    for a in both:
        a.forget()
    listen(both, 6)
    during = {i: acker.count(i) for i in TX_IDS}
    rate = sum(during.values()) / 6.0
    rep.check("the converter kept trying rather than falling silent",
              rate > 2 * sum(EXPECTED_HZ.values()),
              f"{rate:.0f} frames a second against {sum(EXPECTED_HZ.values()):.0f} "
              f"nominal -- the excess is the same frame being retransmitted, "
              f"which is what an unacknowledged bus looks like")

    print("\n  E1  restore the acknowledgements")
    sender.open()
    acker.open()
    settle(stream, sender, both, 6, rep=rep)
    after = latest_diag(acker)
    rep.check("the converter came back on its own", after is not None,
              "DS39977C 27.11: recovery is 128 x 11 recessive bits, about "
              "2.8 ms at 500 kbps, with no MCU intervention")
    if after:
        # Not expect_clean, for the same reason as E2 below: this test has just
        # driven the transmit error counter to the error-passive limit on
        # purpose, and TEC comes down by one per frame acknowledged. At the
        # converter's 22 frames a second, six seconds of settling walks 128
        # most of the way to zero and not reliably all of it -- a run that
        # ended on 2 was failing a check on whether the counter had finished
        # counting rather than on whether the module had recovered.
        show_diag(after, rep, expect_clean=False)
        rep.check("the error counter is on its way back down",
                  after["tx_err"] < 96 and after["rx_err"] < 96,
                  f"tx {after['tx_err']}, rx {after['rx_err']}; 96 is the "
                  f"module's own warning threshold, and it was at 128")
        rep.check("UNHEALTHY stayed latched through the recovery",
                  bool(after["flags"] & 0x04),
                  "this is the whole reason that latch exists -- the counters "
                  "reset on recovery and would show nothing happened")
        rep.check("the fault did not reset the part",
                  after["reset_cause"] & 0x04 == 0,
                  "a watchdog reset here would mean bus-off wedged the loop")

    # -- E2: a node at the wrong bit rate ----------------------------------
    print("\n  E2  a node transmitting at the wrong bit rate")
    rep.note("S5 is 250 kbit/s into a 500 kbit/s bus: real error frames, "
             "which is what an intermittent fault looks like")
    acker.open(bitrate=b"S5")
    for _ in range(200):
        acker.send(0x123, bytes(8))
        time.sleep(0.005)
    acker.open()                       # back to 500 kbit/s and acknowledging
    settle(stream, sender, both, 6, rep=rep)
    recovered = latest_diag(acker)
    rep.check("the converter is transmitting again after the corruption",
              recovered is not None)
    if recovered:
        show_diag(recovered, rep, expect_clean=False)
        rep.check("the error counters came back down",
                  recovered["rx_err"] < 96 and recovered["tx_err"] < 96,
                  f"rx {recovered['rx_err']}, tx {recovered['tx_err']}; "
                  "above 96 is the module's own warning threshold")
        rep.check("the module is out of any error state",
                  recovered["comstat"] == 0,
                  names(recovered["comstat"], COMSTAT_BITS))
    return rep


# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG)
    ap.add_argument("--seconds", type=float, default=20.0,
                    help="length of the traffic and listen-only runs")
    ap.add_argument("--speed", type=float, default=1.0,
                    help="replay rate multiplier for --traffic")
    ap.add_argument("--all-ids", action="store_true")
    ap.add_argument("--port", help="the transmitting adapter")
    ap.add_argument("--port2", help="the second adapter, for 7a and 7e")
    ap.add_argument("--observe", type=float, default=30.0,
                    help="seconds 7a keeps traffic live so the LEDs can be "
                         "looked at; 0 to skip the window")
    ap.add_argument("--led-can", default="unknown",
                    choices=["steady", "slow", "fast", "dark", "unknown"],
                    help="what LED_CAN was observed doing during 7a")
    ap.add_argument("--led-pwr", default="unknown",
                    choices=["steady", "slow", "dark", "unknown"],
                    help="what LED_PWR was observed doing during 7a")
    ap.add_argument("--list", action="store_true",
                    help="list serial ports and exit")
    ap.add_argument("--listen-only", action="store_true")
    ap.add_argument("--traffic", action="store_true")
    ap.add_argument("--scenarios", action="store_true")
    ap.add_argument("--fault", action="store_true")
    ap.add_argument("--all", action="store_true",
                    help="every test, in order; needs two adapters")
    ap.add_argument("--persist-arm", action="store_true",
                    help="7.5 part 1: accumulate a trip and write it to the "
                         "EEPROM, then tell you to power-cycle")
    ap.add_argument("--persist-check", action="store_true",
                    help="7.5 part 2: after the power cycle, did it come back")
    ap.add_argument("--expect-trip-ml", type=int, default=0,
                    help="the trip --persist-arm reported, in ml")
    ap.add_argument("--all-one-device", action="store_true",
                    help="only what a single adapter can run -- traffic and "
                         "scenarios, which are the two that cover what "
                         "loopback in step 6 cannot")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    # The order is deliberate on two counts. The one-adapter tests come first,
    # so --all-one-device is a prefix of --all rather than a different subset.
    # And listen only comes last, because it is the only part wanting a
    # different hex: anywhere else it would cost a third flash, and at the end
    # it leaves the device holding exactly what step 8 asks for next.
    one_device = ["traffic", "scenarios"]
    two_device = ["fault", "listen-only"]

    wanted = [n for n, on in (("traffic", args.traffic),
                              ("scenarios", args.scenarios),
                              ("fault", args.fault),
                              ("listen-only", args.listen_only)) if on]
    if args.all_one_device:
        wanted = list(one_device)
    elif args.all or not wanted:
        wanted = one_device + two_device

    # The persistence pair is its own thing: it spans a power cycle, so it can
    # never be part of a sequence that runs straight through.
    if args.persist_arm or args.persist_check:
        port = args.port or find_port()
        sender = Adapter(port, "sender")
        acker = Adapter(args.port2, "acker") if args.port2 else None
        listener = acker or sender
        try:
            if args.persist_arm:
                rep = mode_persist_arm(sender, listener, args.log)
            else:
                rep = mode_persist_check(sender, listener, args.log,
                                         args.expect_trip_ml)
        finally:
            sender.release()
            if acker:
                acker.release()
        return summarise([rep])

    if args.list:
        require_serial()
        from serial.tools import list_ports
        for port in list_ports.comports():
            print(f"{port.device}  {port.description}")
        return 0

    if args.dry_run:
        tpl = bs.templates(args.log)
        print(f"{args.log.name}: templates for "
              + ", ".join(f"{i:#05x}" for i in sorted(tpl)))
        stream = bs.Stream(tpl, bs.Condition(speed_kmh=60, flow_ul_s=1000))
        for can_id, data in stream.tick():
            print(f"  {slcan_tx(can_id, data).decode()}")
        print(f"\nwould run: {', '.join(wanted)}")
        return 0

    needs_two = {"listen-only", "fault"} & set(wanted)
    port = args.port or find_port()
    sender = Adapter(port, "sender")
    acker = None
    if needs_two:
        if not args.port2:
            sender.release()
            sys.exit("--port2 is required for the listen-only and fault tests: "
                     "a listen-only converter never acknowledges, so something "
                     "else on the bus has to.")
        acker = Adapter(args.port2, "acker")
    listener = acker or sender

    reports = []
    try:
        # Nothing here asks whether the right hex is flashed. This is driven
        # from a session that cannot see the board, so a prompt would read EOF
        # and answer itself -- and the checks catch the wrong build anyway: a
        # silent build in the first three shows up as no frames at all, and a
        # normal build in the listen-only test as frames where there must be
        # none.
        if {"traffic", "scenarios", "fault"} & set(wanted):
            print("\n>>> the tests below need the NORMAL build flashed <<<")
        if "traffic" in wanted:
            reports.append(mode_traffic(sender, listener, args.log,
                                        args.seconds, args.speed,
                                        args.all_ids))
        if "scenarios" in wanted:
            reports.append(mode_scenarios(sender, listener, args.log))
        if "fault" in wanted:
            reports.append(mode_fault(sender, acker, args.log))
        if "listen-only" in wanted:
            print("\n>>> reflash CAN_MODE=LISTEN_ONLY before this last one <<<")
            reports.append(mode_listen_only(sender, acker, args.log,
                                            args.seconds, args.observe,
                                            args.led_can, args.led_pwr))
    finally:
        sender.release()
        if acker:
            acker.release()

    return summarise(reports)


def summarise(reports) -> int:
    failed = [f for r in reports for f in r.failed]
    print()
    if failed:
        print(f"FAIL -- {len(failed)} check(s):")
        for f in failed:
            print(f"  {f}")
        return 1

    print("Bench test finished. Traffic sent, the converter answered, its CAN")
    print("error counters are zero and it recovered from every fault injected.")
    print()
    # Printed output stays ASCII. The docstrings and docs/ use a warning sign
    # freely because those are UTF-8 files; a console is whatever the machine
    # set it to, and on this one it is cp1250, where printing that character
    # raises UnicodeEncodeError and takes the whole run down AT THE END, after
    # every test has already passed.
    print("WARNING: the EEPROM now holds synthetic trip and tank data. The reflash at")
    print("  the start of step 8 clears it -- do NOT pass -Z0-3FF there. The")
    print("  next 0x603 proves it: PERSIST_OK comes back clear.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
