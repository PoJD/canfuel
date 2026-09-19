#!/usr/bin/env python3
"""Does this engine stop injecting when the car is driving it, and when?

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
whether the ECU has the injectors shut at the time: if it does, fuel reaching
a hot exhaust is fuel arriving while nobody asked for any, and the only place
left for it to come from is an injector that is not sealing. If the ECU is
fuelling normally, the burble is commanded fuel and says nothing.

The bus answers it directly, because 0x480 counts what the ECU commanded.
Find the stretches where the car is rolling with the pedal released, and look
for the counter stopping.

Why there is no gear test here, although an earlier version had one
-------------------------------------------------------------------

A released pedal is not enough by itself: a gearchange and a clutch-in coast
look the same on every other channel, and in neither of them is the car
driving the engine. That looked like it needed the engine-speed-to-road-speed
ratio checked for a constant, and it does not -- **the cut is its own
evidence.** An ECU that shuts the injectors while the clutch is down has
stalled the engine, so a counter that stops for a second while the car rolls
is an overrun by construction. The ratio is still printed, because it says
which windows ended with the clutch coming in, but nothing is gated on it.

What it found in the corpus
---------------------------

`17_drive_property_z1` -- warm, first gear, the only fixture with real
driving in it -- holds four of them, and they agree with each other closely:
the injectors shut about **1.2 to 1.3 seconds after the pedal comes up** and
fuel returns at about **1,700 to 1,750 rpm**. So the premise the overrun
argument needs is measured rather than assumed. ⚠ **It is measured WARM**,
which is the state the owner says the burble does not happen in; whether the
same ECU cuts fuel on a cold engine is exactly what step 13a is for.

Usage
-----

    python coastscan.py                    # the fixtures
    python coastscan.py CAPTURE [CAPTURE ...]
    python coastscan.py --all CAPTURE      # every coast, not only the cuts
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
#: Below walking pace the car is not driving anything. In 0.001 km/h.
COAST_MIN_MMH = 4000
#: Low enough that a whole cut fits inside one window: fuel came back at
#: 1,700 rpm in every fixture case, and a floor above that would clip the end
#: off the very thing being measured. An earlier version of this file used
#: 1,500 rpm and a 20 km/h floor and threw away all four cuts.
COAST_MIN_RPM = 1200
#: A coast shorter than this cannot contain the delay below, let alone a cut.
COAST_MIN_S = 0.5
#: Warm idle, measured: 326 ul/s at 796 rpm in 09_idle_60s_z1, which is
#: 24.6 ul per revolution. Injection quantity scales with engine speed, so
#: ul/s across a coast that is also a deceleration cannot be compared against
#: it and ul/rev can.
IDLE_UL_PER_REV = 24.6
#: At or below this the injectors are shut. A DECISION, not a measurement: it
#: is a twentieth of idle's charge, far below anything a running engine is
#: given and far above the zero an exact cut produces. The fixtures separate
#: cleanly either side of it -- fuelling reads about 11 ul/rev and a cut reads
#: 0 -- so nothing lands near it by accident.
CUT_UL_PER_REV = 1.2
#: A shorter dry run is a gap in the counter rather than a strategy.
CUT_MIN_S = 0.3


def samples(path):
    """(t, rpm, throttle, speed_mmh, d_ul, coolant_c) per 0x480 frame.

    d_ul is the fuel the ECU commanded since the previous 0x480, per
    docs/can-decoding.md trap 2: the delta is (new - old) mod 32768 and a
    counter of zero is a restart rather than a reading.

    coolant_c is carried because it is very likely what gates the cut. A
    warm-up is a ladder of coolant temperatures, so a drive with coasts spread
    through it says at WHICH temperature the injectors start being shut --
    which is a better answer than a cold yes or no, and costs nothing but
    printing a column. None until 0x288 has been seen.
    """
    frames = canlog.parse_file(
        path, fix_doubled=os.path.basename(path).startswith("02"))
    t0 = None
    rpm = throttle = speed_mmh = 0
    coolant_c = None
    prev = None
    out = []
    for f in frames:
        if f.ts_ms is not None and t0 is None:
            t0 = f.ts_ms
        if f.can_id == 0x288 and len(f.data) >= 2 and f.data[1] != 0xFF:
            coolant_c = f.data[1] * 0.75 - 48.0
        elif f.can_id == 0x1A0 and len(f.data) >= 4:
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
                            speed_mmh, d, coolant_c))
    return out


def coasting(row):
    """Rolling, pedal released, engine still turning above the governor."""
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


def charges(win):
    """Charge per revolution at each sample, from the gap to the one before.

    0x480 has no period (docs/can-decoding.md question 1), so a delta means
    nothing until it is divided by the gap it accumulated over.
    """
    out = []
    for i, r in enumerate(win):
        dt = r[0] - win[i - 1][0] if i else 0.0
        if dt <= 0 or r[1] <= 0:
            out.append(None)
        else:
            out.append((r[4] / dt) / (r[1] / 60.0))
    return out


def cut(win, min_s=CUT_MIN_S):
    """The longest stretch of the window with the injectors shut, or None."""
    best, cur = [], []
    for r, c in zip(win, charges(win)):
        if c is not None and c <= CUT_UL_PER_REV:
            cur.append(r)
        else:
            if len(cur) > len(best):
                best = cur
            cur = []
    if len(cur) > len(best):
        best = cur
    if len(best) < 3 or best[-1][0] - best[0][0] < min_s:
        return None
    return best


def ratio_drift(win):
    """How much the engine-speed-to-road-speed ratio moved across a window.

    Informational: near zero is one gear with the clutch up, and a large
    number is a gearchange or a clutch that came down. Nothing is gated on it
    -- see the module docstring.
    """
    a = win[0][1] / (win[0][3] / 1000.0)
    b = win[-1][1] / (win[-1][3] / 1000.0)
    return abs(b - a) / max(a, b)


def coolant(win):
    """The coolant at the start of the window, or None if 0x288 is filtered out."""
    return win[0][5]


def describe(win):
    c = coolant(win)
    line = ("%5.2f s  rpm %5.0f->%5.0f  %4.1f->%4.1f km/h  coolant %s"
            "  ratio %4.1f %%"
            % (win[-1][0] - win[0][0], win[0][1], win[-1][1],
               win[0][3] / 1000.0, win[-1][3] / 1000.0,
               "  n/a" if c is None else "%5.1f C" % c, ratio_drift(win) * 100))
    c = cut(win)
    if c is None:
        return line + "  ||  no cut"
    return line + ("  ||  CUT %4.2f s, shut at %5.0f rpm %4.2f s after the "
                   "lift, back at %5.0f"
                   % (c[-1][0] - c[0][0], c[0][1], c[0][0] - win[0][0],
                      c[-1][1]))


def report(path, show_all=False):
    name = os.path.basename(path)
    rows = samples(path)
    if not rows:
        print("%-28s   no timestamps, skipped" % name)
        return
    wins = windows(rows)
    withcut = [w for w in wins if cut(w) is not None]
    print("%-28s   %2d coast window%s, %d with the injectors shut"
          % (name, len(wins), "" if len(wins) == 1 else "s", len(withcut)))
    for w in (wins if show_all else withcut):
        print("        " + describe(w))
    if withcut:
        cuts = [cut(w) for w in withcut]
        delay = [c[0][0] - w[0][0] for c, w in zip(cuts, withcut)]
        back = [c[-1][1] for c in cuts]
        print("        fuel cut CONFIRMED: shuts %.2f-%.2f s after the pedal "
              "comes up, fuel back at %.0f-%.0f rpm"
              % (min(delay), max(delay), min(back), max(back)))
        hot = [coolant(w) for w in withcut if coolant(w) is not None]
        cold = [coolant(w) for w in wins
                if cut(w) is None and coolant(w) is not None]
        if hot and cold and min(hot) > min(cold):
            print("        and the coldest coast that cut was at %.1f C of "
                  "coolant, against %.1f C for the coldest that did not"
                  % (min(hot), min(cold)))
        elif hot:
            print("        coldest coast that cut: %.1f C of coolant" % min(hot))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="logs to read (default: the fixtures)")
    ap.add_argument("--all", action="store_true",
                    help="print every coast window, not only the ones with a cut")
    args = ap.parse_args(argv)

    for p in args.files or sorted(glob.glob(os.path.join(FIXTURES, "*.txt"))):
        report(p, show_all=args.all)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
