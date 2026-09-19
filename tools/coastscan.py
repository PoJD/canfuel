#!/usr/bin/env python3
"""Does this engine stop injecting when the car is driving it?

This is the analysis behind step 13a of docs/next-drive.md and behind *The
oldest symptom is on the overrun* in docs/engine-health.md. It exists as a
tool for the same reason tools/b7scan.py does: the figures it prints decide
how a symptom is read, and a figure typed into prose cannot be re-checked
against a new capture.

What it answers
---------------

The owner reports that on a COLD engine, braking on the engine down a hill,
fuel could be heard going into the exhaust and burning there, and that on a
warm engine it does not happen. Whether that means anything at all turns on
one fact nobody here holds from a document: whether this ECU cuts the
injectors on the overrun. If it does, fuel reaching the exhaust there is fuel
arriving while the driver asks for none. If it does not, the burble is
commanded fuel and says nothing.

The bus answers it directly. Find the windows where the car is driving the
engine, and read the fuel counter across them.

What counts as a coast, and why the gear test is the whole difficulty
--------------------------------------------------------------------

A released pedal is not enough. A gearchange and a clutch-in coast both look
like "moving, pedal at rest, engine turning", and in both of them the engine
is NOT being driven by the car -- so fuel at idle rates is exactly what should
be there and proves nothing.

What separates them is that a car in gear holds a fixed ratio between engine
speed and road speed. So a window is in gear only while that ratio stays put,
which is checked here rather than assumed. Applied to the fixtures it rejects
every window they contain, which is the honest answer: **the corpus holds no
sustained in-gear overrun at all.** Eighteen recordings of idling, revving in
neutral and first-gear pottering do not include one, and the next drive is
what supplies it.

Usage
-----

    python coastscan.py                    # the fixtures
    python coastscan.py CAPTURE [CAPTURE ...]
    python coastscan.py --windows CAPTURE  # every window, in gear or not
"""

from __future__ import annotations

import argparse
import glob
import os

import canlog

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, os.pardir, "test", "fixtures")

#: From src/config.h. THROTTLE_REST is a released pedal and is not an equality
#: -- docs/can-decoding.md says why 38 is the rest value and 39-43 are empty.
THROTTLE_REST = 38
#: Fast enough that the ratio below means something. 20 km/h in 0.001 km/h.
COAST_MIN_MMH = 20000
#: Above the idle governor, so the engine is being turned rather than held.
COAST_MIN_RPM = 1500
#: A window shorter than this says nothing about a fuel cut either way.
COAST_MIN_S = 1.0
#: Warm idle, measured: 326 ul/s at 796 rpm in 09_idle_60s_z1, which is
#: 24.6 ul per revolution. Injection quantity scales with engine speed, so
#: ul/s across a coast that is also a deceleration cannot be compared with it
#: and ul/rev can.
IDLE_UL_PER_REV = 24.6
#: Below this the ECU is not fuelling the engine in any meaningful sense. A
#: DECISION, not a measurement: it is a twentieth of idle's charge, far below
#: anything a running engine is given and far above the zero an exact cut
#: would produce, so nothing lands near it by accident.
CUT_UL_PER_REV = 1.2
#: How far the engine-speed-to-road-speed ratio may drift and still be one
#: gear. A DECISION, not a measurement: a gearchange moves it by tens of per
#: cent (the fixtures' five windows move 6-28 %), while in gear it should move
#: only by what tyre slip and the two channels' sample skew contribute. Ten per
#: cent sits between those and nothing in the corpus lies near it.
GEAR_RATIO_TOL = 0.10


def samples(path):
    """(t, rpm, throttle, speed_mmh, d_ul) per 0x480 frame, with the bus state.

    d_ul is the fuel the ECU commanded since the previous 0x480, per
    docs/can-decoding.md trap 2: the delta is (new - old) mod 32768 and a
    counter of zero is a restart rather than a reading.
    """
    frames = canlog.parse_file(
        path, fix_doubled=os.path.basename(path).startswith("02"))
    t0 = None
    rpm = throttle = speed_mmh = 0
    prev = None
    out = []
    for f in frames:
        if f.ts_ms is not None and t0 is None:
            t0 = f.ts_ms
        if f.can_id == 0x1A0 and len(f.data) >= 4:
            # trap 1: the validity gate is not an equality.
            if (f.data[1] & 0x40) != 0 and (f.data[1] & 0x03) == 0:
                speed_mmh = (f.data[2] | (f.data[3] << 8)) * 5
        elif f.can_id == 0x280 and len(f.data) >= 8:
            rpm = (f.data[2] | (f.data[3] << 8)) / 4.0
            throttle = f.data[5]
        elif f.can_id == 0x480 and len(f.data) >= 4:
            raw = (f.data[2] | (f.data[3] << 8)) & 0x7FFF
            if raw == 0 or rpm == 0:      # trap 2: the ignition went off
                prev = None
            d = 0 if prev is None else (raw - prev) & 0x7FFF
            prev = raw
            if f.ts_ms is not None:
                out.append(((f.ts_ms - t0) / 1000.0, rpm, throttle,
                            speed_mmh, d))
    return out


def coasting(row):
    """Moving, pedal released, engine turning well above the governor."""
    return (row[3] >= COAST_MIN_MMH and row[2] <= THROTTLE_REST
            and row[1] >= COAST_MIN_RPM)


def windows(rows, min_s=COAST_MIN_S):
    """Contiguous runs of coasting samples, long enough to say anything."""
    out, cur = [], []
    for r in rows:
        if coasting(r):
            cur.append(r)
            continue
        if len(cur) >= 3 and cur[-1][0] - cur[0][0] >= min_s:
            out.append(cur)
        cur = []
    if len(cur) >= 3 and cur[-1][0] - cur[0][0] >= min_s:
        out.append(cur)
    return out


def ratio_drift(win):
    """How much the engine-speed-to-road-speed ratio moved across a window.

    As a fraction of the largest of the two. Near zero is one gear with the
    clutch up; anything else is a change of gear or a clutch that is down.
    """
    a = win[0][1] / (win[0][3] / 1000.0)
    b = win[-1][1] / (win[-1][3] / 1000.0)
    return abs(b - a) / max(a, b)


def in_gear(win):
    return ratio_drift(win) <= GEAR_RATIO_TOL


def rate_ul_s(win):
    dur = win[-1][0] - win[0][0]
    return sum(r[4] for r in win) / dur if dur > 0 else 0.0


def ul_per_rev(win):
    """The charge per revolution, which is what compares against idle.

    A coast is also a deceleration, so ul/s falls with the engine speed
    whatever the ECU is doing. Dividing it out is what makes the number mean
    "is it fuelling" rather than "how fast is it turning".
    """
    revs_per_s = sum(r[1] for r in win) / len(win) / 60.0
    return rate_ul_s(win) / revs_per_s if revs_per_s > 0 else 0.0


def describe(win):
    return ("%5.2f s  rpm %5.0f->%5.0f  %4.1f->%4.1f km/h  ratio drift %4.1f %%"
            "  fuel %6.0f ul/s = %5.1f ul/rev (idle %.1f)  %s"
            % (win[-1][0] - win[0][0], win[0][1], win[-1][1],
               win[0][3] / 1000.0, win[-1][3] / 1000.0, ratio_drift(win) * 100,
               rate_ul_s(win), ul_per_rev(win), IDLE_UL_PER_REV,
               "IN GEAR" if in_gear(win) else "not in gear"))


def report(path, show_windows=False):
    name = os.path.basename(path)
    rows = samples(path)
    if not rows:
        print("%-28s   no timestamps, skipped" % name)
        return
    wins = windows(rows)
    geared = [w for w in wins if in_gear(w)]
    print("%-28s   %2d coast window%s, %d in gear"
          % (name, len(wins), "" if len(wins) == 1 else "s", len(geared)))
    for w in (wins if show_windows else geared):
        print("        " + describe(w))
    if geared:
        most = max(ul_per_rev(w) for w in geared)
        print("        verdict: the ECU %s injecting on the overrun -- "
              "%.1f ul/rev at most, against %.1f at warm idle"
              % ("KEEPS" if most > CUT_UL_PER_REV else "STOPS",
                 most, IDLE_UL_PER_REV))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="logs to read (default: the fixtures)")
    ap.add_argument("--windows", action="store_true",
                    help="print every coast window, in gear or not")
    args = ap.parse_args(argv)

    for p in args.files or sorted(glob.glob(os.path.join(FIXTURES, "*.txt"))):
        report(p, show_windows=args.windows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
