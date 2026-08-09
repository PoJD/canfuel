#!/usr/bin/env python3
"""Run a log through the decoder and print what the converter would transmit.

This is the reference implementation, written in Python. It follows the same
table as src/decode.c and src/compute.c on purpose, so the two can be compared
directly:

    python tools/replay.py --host-build test/fixtures/02_idle_60s.txt

builds nothing itself but runs test/build/replay_host over the same log and
diffs the numbers. Any drift between the reference and the code that will
actually be flashed then shows up here rather than on the display.

Usage:
    python tools/replay.py test/fixtures/03_drive.txt
    python tools/replay.py --csv test/fixtures/07_accel.txt > out.csv
    python tools/replay.py --every 20 test/fixtures/06_trip_reset.txt
    python tools/replay.py --host-build test/fixtures/*.txt
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional

from canlog import Frame, parse_file

# --- constants that will end up in config.h ------------------------------

PERIOD_0X480_MS = 49.5      # fuel counter period, used when a log has no timestamps
FUELNOW_LH_BELOW_KMH = 4.0  # below this we send l/h, above it l/100 km
FUELNOW_CLAMP = 999         # 99.9 on the display
RANGE_DEFAULT_L100 = 9.0    # used for range until we have driven 5 km
AVG_MIN_M = 100             # below this the average divides by nearly zero
COUNTER_MODULO = 32768

# Speed validity gate in 0x1A0 byte 1. It is not an equality, it is a bit
# mask -- the reasoning is spelled out in docs/can-decoding.md.
SPEED_GATE_REQUIRED = 0x40   # this bit must be set
SPEED_GATE_FORBIDDEN = 0x03  # these mark the post-ignition init ramp


# --- decoding -------------------------------------------------------------

@dataclass
class Decoded:
    """Last known bus state. Mirrors the output of decode.c."""

    rpm: float = 0.0
    speed_kmh: float = 0.0
    speed_valid: bool = False
    clt_c: Optional[float] = None
    oil_c: Optional[float] = None
    tank_l: int = 0
    tank_reserve: bool = False
    torque_ind_nm: float = 0.0
    throttle: int = 0
    load: int = 0
    accel_g: float = 0.0
    fuel_counter: Optional[int] = None
    counter_wrapped: bool = False


def u16le(d: bytes, i: int) -> int:
    return d[i] | d[i + 1] << 8


def decode(frame: Frame, st: Decoded) -> None:
    """Fold one frame into the state. Extraction only, no fuel maths."""
    d = frame.data
    cid = frame.can_id

    if cid == 0x280 and len(d) >= 8:
        st.rpm = u16le(d, 2) * 0.25
        st.throttle = d[5]
        st.load = d[6]
        st.torque_ind_nm = d[7] * 0.67

    elif cid == 0x1A0 and len(d) >= 4:
        # Byte 1 is a bit field, not a single value. Bit 0x40 means "speed is
        # valid", the low two bits mark the init ramp that runs for ~0.4 s
        # after ignition on and must be thrown away. Bits 0x08 and 0x10 do not
        # affect validity -- in 07_accel 0x48 is in fact the majority state.
        st.speed_valid = bool(d[1] & SPEED_GATE_REQUIRED) and not (d[1] & SPEED_GATE_FORBIDDEN)
        if st.speed_valid:
            st.speed_kmh = u16le(d, 2) * 0.005

    elif cid == 0x288 and len(d) >= 2:
        st.clt_c = None if d[1] == 0xFF else d[1] * 0.75 - 48.0

    elif cid == 0x420 and len(d) >= 4:
        st.oil_c = None if d[3] == 0xFF else d[3] * 0.75 - 48.0

    elif cid == 0x320 and len(d) >= 3:
        st.tank_l = d[2] & 0x7F
        st.tank_reserve = bool(d[2] & 0x80)

    elif cid == 0x5A0 and len(d) >= 1:
        st.accel_g = (d[0] - 127) / 100.0

    elif cid == 0x480 and len(d) >= 4:
        raw = u16le(d, 2)
        st.fuel_counter = raw & 0x7FFF
        st.counter_wrapped = bool(raw & 0x8000)


# --- computation ----------------------------------------------------------

@dataclass
class Compute:
    """Accumulators. Mirrors compute.c."""

    prev_counter: Optional[int] = None
    total_ul: int = 0
    total_mm: int = 0
    last_ms: Optional[float] = None
    flow_ul_s: float = 0.0
    restarts: int = 0
    _flow_window: list = field(default_factory=list)

    def on_counter(self, st: Decoded, now_ms: float) -> None:
        """A new counter reading. The result lands in self.total_ul.

        The trap this code exists for: the counter resets to zero when the
        ignition is switched off. Without restart detection the delta would
        jump by tens of thousands of microlitres out of nowhere.
        """
        c = st.fuel_counter
        if c is None:
            return

        restart = c == 0 or st.rpm == 0
        if restart or self.prev_counter is None:
            if restart and self.prev_counter is not None:
                self.restarts += 1
            self.prev_counter = c
            self.last_ms = now_ms
            return

        delta_ul = (c - self.prev_counter) % COUNTER_MODULO
        self.prev_counter = c

        dt_s = None
        if self.last_ms is not None and now_ms > self.last_ms:
            dt_s = (now_ms - self.last_ms) / 1000.0
        self.last_ms = now_ms

        self.total_ul += delta_ul
        if dt_s:
            self._flow_window.append((delta_ul, dt_s))
            # ~1 s sliding window, otherwise the number on the display dances
            while sum(w[1] for w in self._flow_window) > 1.0 and len(self._flow_window) > 1:
                self._flow_window.pop(0)
            win_ul = sum(w[0] for w in self._flow_window)
            win_s = sum(w[1] for w in self._flow_window)
            self.flow_ul_s = win_ul / win_s if win_s else 0.0

    def on_distance(self, st: Decoded, dt_s: float) -> None:
        if st.speed_valid and st.speed_kmh > 0 and dt_s > 0:
            self.total_mm += int(st.speed_kmh / 3.6 * dt_s * 1000.0)

    # -- derived quantities ------------------------------------------------

    @property
    def flow_lh(self) -> float:
        return self.flow_ul_s * 3.6 / 1000.0

    @property
    def avg_l100(self) -> float:
        """A ratio of accumulators, not an average of instantaneous values --
        that way idling at a red light does not ruin the average.

        Below AVG_MIN_M it returns zero. Without that guard we divide by an
        almost-zero distance right after starting; on 06_trip_reset that gave
        21,395 l/100 km before the car had moved. The display would show a
        clamped 99.9.
        """
        if self.total_mm < AVG_MIN_M * 1000:
            return 0.0
        return (self.total_ul / 1000.0) / (self.total_mm / 1000.0) * 100.0

    def fuel_now(self, st: Decoded) -> tuple[float, str]:
        """Dual unit. A single threshold, no hysteresis."""
        if not st.speed_valid or st.speed_kmh < FUELNOW_LH_BELOW_KMH:
            return min(self.flow_lh, FUELNOW_CLAMP / 10.0), "l/h"
        l100 = self.flow_lh / st.speed_kmh * 100.0
        return min(l100, FUELNOW_CLAMP / 10.0), "l/100km"

    def range_km(self, st: Decoded) -> float:
        driven_km = self.total_mm / 1_000_000.0
        basis = self.avg_l100 if driven_km >= 5.0 and self.avg_l100 > 0 else RANGE_DEFAULT_L100
        return st.tank_l / basis * 100.0


# --- replaying ------------------------------------------------------------

def walk(frames: list) -> Iterator[tuple]:
    """Fold a whole log, yielding (now_ms, st, cp) at every 0x480 frame.

    0x480 is the clock of the device: it is the only periodic input whose
    period we trust (49.5 ms, argued in docs/can-decoding.md). Logs in the
    viewer format carry real timestamps and those win.

    The order inside the loop -- decode, then distance, then the counter --
    is the same one test/replay_core.h uses on the C side. Swapping the last
    two would integrate the previous speed over the current interval.
    """
    st = Decoded()
    cp = Compute()
    synthetic = all(f.ts_ms is None for f in frames)
    n480 = 0
    prev_ms = None

    for f in frames:
        if f.can_id == 0x480:
            now_ms = n480 * PERIOD_0X480_MS if synthetic else float(f.ts_ms)
            n480 += 1
        else:
            now_ms = None

        decode(f, st)

        if now_ms is None:
            continue

        if prev_ms is not None:
            cp.on_distance(st, (now_ms - prev_ms) / 1000.0)
        prev_ms = now_ms

        cp.on_counter(st, now_ms)
        yield now_ms, st, cp


def summarise(path: str, *, fix_doubled: bool = True) -> dict:
    """The same numbers test/build/replay_host prints, for comparing against."""
    frames = parse_file(path, fix_doubled=fix_doubled)
    first_ms = last_ms = 0.0
    rows = 0
    st = cp = None

    for now_ms, st, cp in walk(frames):
        if rows == 0:
            first_ms = now_ms
        last_ms = now_ms
        rows += 1

    if cp is None:
        return {"fuel_frames": 0, "total_ul": 0, "total_mm": 0,
                "restarts": 0, "flow_ul_s": 0, "span_ms": 0}

    return {
        "fuel_frames": rows,
        "total_ul": cp.total_ul,
        "total_mm": cp.total_mm,
        "restarts": cp.restarts,
        "flow_ul_s": round(cp.flow_ul_s),
        "span_ms": round(last_ms - first_ms),
    }


def replay(path: str, *, csv: bool = False, every: int = 1, fix_doubled: bool = True):
    frames = parse_file(path, fix_doubled=fix_doubled)
    synthetic = all(f.ts_ms is None for f in frames)
    n480 = 0
    rows = 0
    cp = None

    header = ["t_s", "rpm", "km/h", "clt", "ul_s", "l/h", "FuelNow", "unit",
              "FuelAvg", "tank_l", "range_km", "total_ul", "total_m"]
    if csv:
        print(",".join(header))
    else:
        print(f"# {path}")
        print(f"# time {'estimated from the 0x480 period' if synthetic else 'from log timestamps'}")
        print("  " + "".join(h.rjust(10) for h in header))

    for now_ms, st, cp in walk(frames):
        n480 += 1
        rows += 1
        if rows % every:
            continue

        fn, unit = cp.fuel_now(st)
        vals = [
            f"{now_ms / 1000:.2f}", f"{st.rpm:.0f}", f"{st.speed_kmh:.1f}",
            "-" if st.clt_c is None else f"{st.clt_c:.1f}",
            f"{cp.flow_ul_s:.0f}", f"{cp.flow_lh:.2f}", f"{fn:.1f}", unit,
            f"{cp.avg_l100:.1f}", f"{st.tank_l}", f"{cp.range_km(st):.0f}",
            f"{cp.total_ul}", f"{cp.total_mm / 1000:.0f}",
        ]
        print(",".join(vals) if csv else "  " + "".join(v.rjust(10) for v in vals))

    if not csv and cp is not None:
        span_s = (n480 - 1) * (PERIOD_0X480_MS / 1000 if synthetic else 0)
        if not synthetic:
            stamped = [f.ts_ms for f in frames if f.can_id == 0x480]
            span_s = (stamped[-1] - stamped[0]) / 1000.0
        print(f"# total {cp.total_ul} ul over {span_s:.2f} s "
              f"-> {cp.total_ul / span_s:.0f} ul/s = {cp.total_ul / span_s * 3.6 / 1000:.2f} l/h")
        print(f"# distance {cp.total_mm / 1000:.0f} m, average {cp.avg_l100:.2f} l/100 km, "
              f"restarts detected: {cp.restarts}")


# --- comparing against the C core -----------------------------------------

# How far the C core may differ from this file, per field.
#
# The counter arithmetic is pure integer on both sides, so the fuel total and
# the restart count have to agree exactly -- a difference there is a bug, not
# a rounding artefact.
#
# Distance is the one place the two genuinely do different arithmetic: this
# file integrates in floating point over a 49.5 ms step, while the firmware
# works in whole milliseconds because that is what its timer gives it. Over a
# 54 m log that is worth about 7 mm.
TOLERANCE = {
    "total_ul":  (0, 0.0),      # (absolute, relative)
    "restarts":  (0, 0.0),
    "fuel_frames": (0, 0.0),
    "total_mm":  (100, 0.001),
    "flow_ul_s": (2, 0.01),
    "span_ms":   (100, 0.001),
}


def find_host_build(explicit: Optional[str] = None) -> Optional[Path]:
    """Locate the binary built by 'make -C test replay-host'."""
    if explicit:
        return Path(explicit)
    root = Path(__file__).resolve().parent.parent
    for name in ("replay_host", "replay_host.exe"):
        candidate = root / "test" / "build" / name
        if candidate.exists():
            return candidate
    return None


def run_host_build(exe: Path, path: str) -> dict:
    out = subprocess.run([str(exe), path], capture_output=True, text=True,
                         check=True).stdout
    result = {}
    for line in out.splitlines():
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        try:
            result[key] = int(value)
        except ValueError:
            result[key] = value
    return result


def compare_with_host(paths, exe: Optional[str] = None) -> int:
    """Diff this decoder against the C core over the same logs.

    Returns a process exit code: zero when every field is inside tolerance.
    """
    binary = find_host_build(exe)
    if binary is None:
        print("no host build found -- run:  make -C test replay-host", file=sys.stderr)
        return 2

    print(f"# host build: {binary}")
    bad = 0

    for path in paths:
        mine = summarise(path)
        theirs = run_host_build(binary, path)

        print(f"\n{path}")
        print(f"  {'field':<14}{'python':>12}{'C':>12}{'diff':>10}")
        for key in TOLERANCE:
            if key not in theirs:
                continue
            a, b = mine[key], theirs[key]
            abs_tol, rel_tol = TOLERANCE[key]
            limit = max(abs_tol, abs(a) * rel_tol)
            ok = abs(a - b) <= limit
            bad += 0 if ok else 1
            print(f"  {key:<14}{a:>12}{b:>12}{b - a:>10}  {'' if ok else '<-- MISMATCH'}")

    print()
    if bad:
        print(f"{bad} field(s) outside tolerance", file=sys.stderr)
        return 1
    print("python and the C core agree on every field")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Replay a log through the reference decoder.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--csv", action="store_true")
    ap.add_argument("--every", type=int, default=1, help="print only every Nth row")
    ap.add_argument("--no-fix-doubled", action="store_true",
                    help="leave a doubled file as it is (see fixtures/README.md)")
    ap.add_argument("--host-build", action="store_true",
                    help="diff this decoder against the C core in test/build/replay_host")
    ap.add_argument("--host-build-exe", metavar="PATH",
                    help="use this binary instead of looking for it")
    args = ap.parse_args(argv)

    if args.host_build or args.host_build_exe:
        return compare_with_host(args.files, args.host_build_exe)

    for path in args.files:
        replay(path, csv=args.csv, every=max(1, args.every),
               fix_doubled=not args.no_fix_doubled)
    return 0


if __name__ == "__main__":
    sys.exit(main())
