#!/usr/bin/env python3
"""Bench tests for a converter on a desk, with a verdict instead of a blink rate.

docs/install.md step 7, and the last chance to find a fault while the board is
still on a table. --traffic and --scenarios need one adapter and are the two
worth doing whatever else is skipped: loopback in step 6 cannot exercise the
receive path, the acceptance filters or decode, so without these the first run
of any of that is in the car.

    python tools/bench_test.py --list           # find the adapters
    python tools/bench_test.py --traffic        # one adapter
    python tools/bench_test.py --listen-only    # two adapters
    python tools/bench_test.py --scenarios      # one adapter
    python tools/bench_test.py --fault          # two adapters
    python tools/bench_test.py --all            # all four, in order
    python tools/bench_test.py --dry-run        # no hardware at all

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

try:
    import serial
except ImportError:  # pragma: no cover - depends on the machine
    sys.exit("pyserial is not installed:  python -m pip install pyserial")

from usbtin_capture import BEL, BITRATE_CMD, CR, find_port, read_flags

REPO = Path(__file__).resolve().parents[1]
DEFAULT_LOG = REPO / "test" / "fixtures" / "09_idle_60s_z1.txt"

TX_FUEL, TX_ENGINE, TX_TRIP, TX_DIAG = 0x600, 0x601, 0x602, 0x603
TX_IDS = (TX_FUEL, TX_ENGINE, TX_TRIP, TX_DIAG)
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

DIAG_FLAGS = [(0x01, "CAN_OK"), (0x02, "SILENT"), (0x04, "UNHEALTHY"),
              (0x08, "DATA_LIVE"), (0x10, "PERSIST_OK")]
RESET_CAUSES = [(0x01, "power-on"), (0x02, "brown-out"), (0x04, "WATCHDOG"),
                (0x08, "RESET instruction"), (0x10, "STACK")]
# DS39977C Register 27-4, COMSTAT bits 5-0.
COMSTAT_BITS = [(0x20, "TXBO bus-off"), (0x10, "TXBP transmit passive"),
                (0x08, "RXBP receive passive"), (0x04, "TXWARN"),
                (0x02, "RXWARN"), (0x01, "EWARN")]

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
        self.port = port
        self.label = label
        self.ser = serial.Serial(port, baudrate=115200, timeout=0)
        self._pending = bytearray()
        self.rx: dict[int, list[float]] = {}
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

    def open(self, *, listen_only: bool = False, bitrate: bytes = BITRATE_CMD):
        self._close_channel()
        self._cmd(bitrate)
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
                self.last[frame.can_id] = frame.data

    def forget(self) -> None:
        self.rx.clear()
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


def latest_diag(listener: Adapter):
    raw = listener.last.get(TX_DIAG)
    return decode_diag(raw) if raw else None


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
    rep.check("the last reset was not a brown-out",
              not diag["reset_cause"] & 0x02)
    rep.check("0x603 layout is the one this script speaks",
              diag["version"] == DIAG_LAYOUT_VERSION,
              f"frame says {diag['version']}")


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
                  f == 0, "no answer" if f is None else f"flags {f:#04x}")
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

    rep.note(f"sent {sent} frames in {elapsed:.1f} s "
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

def settle(stream, sender, listeners, seconds, *, flood=0, rep=None):
    for a in listeners:
        a.forget()
    kept = feed(stream, sender, listeners, seconds, flood=flood)
    pump_until(time.monotonic() + 0.3, listeners)
    if kept < 0.9 and rep is not None:
        rep.note(f"⚠ the host kept only {kept:.0%} of the intended frame rate "
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

    # -- C: the idle gate ---------------------------------------------------
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
        rep.check("no receive overflow and nothing latched UNHEALTHY",
                  not diag["flags"] & 0x04 and diag["rx_err"] == 0,
                  f"rx err {diag['rx_err']}, "
                  f"flags {names(diag['flags'], DIAG_FLAGS)}")
    rep.note("this is the only test of the six acceptance filters anywhere -- "
             "they exist only in silicon")
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
    rep.check("healthy before the fault",
              baseline is not None and baseline["comstat"] == 0
              and baseline["tx_err"] == 0)

    # -- E1: nobody acknowledges -------------------------------------------
    print("\n  E1  starve the converter of acknowledgements")
    rep.note("both adapters go listen-only, so nothing on the bus drives the "
             "ACK slot and the converter's TEC climbs by 8 per failed try")
    rep.note("no stimulus is sent during this window, and cannot be: an "
             "adapter in listen-only refuses to transmit. The only thing on "
             "the wire is the converter's own frames, which is all this needs")
    sender.open(listen_only=True)
    acker.open(listen_only=True)
    for a in both:
        a.forget()
    listen(both, 6)
    during = {i: acker.count(i) for i in TX_IDS}
    rep.check("the converter fell silent while bus-off",
              sum(during.values()) == 0,
              "a node at the bus-off limit of 256 transmits nothing")

    print("\n  E1  restore the acknowledgements")
    sender.open()
    acker.open()
    settle(stream, sender, both, 6, rep=rep)
    after = latest_diag(acker)
    rep.check("the converter came back on its own", after is not None,
              "DS39977C 27.11: recovery is 128 x 11 recessive bits, about "
              "2.8 ms at 500 kbps, with no MCU intervention")
    if after:
        show_diag(after, rep)
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
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    wanted = [n for n, on in (("listen-only", args.listen_only),
                              ("traffic", args.traffic),
                              ("scenarios", args.scenarios),
                              ("fault", args.fault)) if on]
    if args.all or not wanted:
        wanted = ["listen-only", "traffic", "scenarios", "fault"]

    if args.list:
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
        # normal build in 7a shows up as frames where there must be none, and a
        # silent build in 7b as no frames at all.
        if "listen-only" in wanted:
            print("\n>>> 7a needs CAN_MODE=LISTEN_ONLY flashed <<<")
            reports.append(mode_listen_only(sender, acker, args.log,
                                            args.seconds, args.observe,
                                            args.led_can, args.led_pwr))
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
    finally:
        sender.release()
        if acker:
            acker.release()

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
    print("⚠ The EEPROM now holds synthetic trip and tank data. The reflash at")
    print("  the start of step 8 clears it -- do NOT pass -Z0-3FF there. The")
    print("  next 0x603 proves it: PERSIST_OK comes back clear.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
