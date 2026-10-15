#!/usr/bin/env python3
"""Two fuel fields of the bus against each other, at a warm standing idle.

Written on 11/10/2026 for the owner's question about the old MAF
(docs/engine-health/refuted.md C2, *What the bus says about the old MAF*):
was it wrong for years, or only on the morning of 24/9/2026? VCDS 032 was
read once in August and once that morning, which cannot answer it. The bus
was recorded on both days, and two of its fields together can.

The ratio
---------

Over a window, the fuel the ECU's own counter adds up (0x480, microlitres)
divided by the injection-time byte integrated over the intake strokes in the
same window (0x288 b6 times strokes; docs/firmware/can-decoding.md
question 3). On a warm standing idle it sits at **0.30-0.32** in every
capture on the new MAF and in every August capture on the old one, and it
does not move with the oil from 50 C up.

**What it means is not known.** It was first read (11/10/2026) as the
lambda correction -- b6 before it, the counter after it -- and that is
**refuted by the injector cuts of `31`**: with one injector unplugged the
loop adds about 16 % of fuel, and the counter per stroke and b6 both rose
by that much while the ratio stayed put. Both fields carry the correction.
What is left is an observation: the two parted on the morning of 24/9, on
the old MAF, and nowhere else -- b6 rose, the fuel per stroke on the
counter did not.

It is read only where it is comparable: a warm standing idle (coolant at
least `COOLANT_MIN_C`, engine speed `IDLE_RPM`, throttle at rest, standing).
Off idle the ratio moves with engine speed and load for reasons of its own.

Usage::

    python fuelratio.py                       # every _z1 capture with a warm idle
    python fuelratio.py FILE --windows        # the ratio window by window
"""

from __future__ import annotations

import argparse
import glob
import os
import statistics
import sys

import canlog
import idledips

FIXTURES = idledips.FIXTURES
#: Seconds per window.
WINDOW_S = 20.0
#: A window counts if the idle filled this share of it.
FILL = 0.8
#: Warm standing idle.
COOLANT_MIN_C = 85.0
IDLE_RPM = (760.0, 840.0)
#: A counter step larger than this, or a frame gap longer than this, is a
#: restart or a hole in the capture, not fuel.
MAX_STEP_UL = 600
MAX_GAP_S = 0.2


def windows(path):
    """[(window start s, ratio, oil C or None)] over the warm standing idle."""
    frames = canlog.parse_file(path)
    if not frames or frames[0].ts_ms is None:
        raise SystemExit(f"{path}: no adapter timestamps (only _z1 logs)")
    t0 = frames[0].ts_ms
    rpm, thr, b6, clt, oil, speed = 0.0, 255, None, None, None, 0
    prev = last = None
    acc = {}
    for f in frames:
        t = (f.ts_ms - t0) / 1000.0
        d = f.data
        if f.can_id == 0x280 and len(d) >= 8:
            rpm, thr = (d[2] | (d[3] << 8)) / 4.0, d[5]
        elif f.can_id == 0x288 and len(d) >= 7:
            b6, clt = d[6], d[1] * 0.75 - 48.0
        elif f.can_id == 0x420 and len(d) >= 4:
            oil = canlog.oil_c(d[3])
        elif f.can_id == 0x1A0 and len(d) >= 4:
            # docs/firmware/can-decoding.md trap 1
            if (d[1] & 0x40) and not (d[1] & 0x03):
                speed = (d[2] | (d[3] << 8)) * 5
        elif f.can_id == 0x480 and len(d) >= 4:
            c = (d[2] | (d[3] << 8)) & 0x7FFF
            ok = (IDLE_RPM[0] < rpm < IDLE_RPM[1] and b6
                  and thr <= idledips.GATE_THROTTLE
                  and speed <= idledips.GATE_SPEED_MMH
                  and clt is not None and clt >= COOLANT_MIN_C)
            if ok and prev is not None and last is not None:
                step, dt = (c - prev) % 32768, t - last
                if step < MAX_STEP_UL and dt < MAX_GAP_S:
                    a = acc.setdefault(int(t // WINDOW_S), [0.0, 0.0, 0.0, []])
                    a[0] += step
                    a[1] += b6 * rpm / 60.0 * 2.0 * dt
                    a[2] += dt
                    if oil is not None:
                        a[3].append(oil)
            prev, last = c, t
    out = []
    for k in sorted(acc):
        fuel, inj, dt, oils = acc[k]
        if dt >= FILL * WINDOW_S and inj > 0:
            out.append((k * WINDOW_S, fuel / inj,
                        statistics.median(oils) if oils else None))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--windows", action="store_true")
    args = ap.parse_args(argv)
    paths = args.files or sorted(glob.glob(os.path.join(FIXTURES, "*_z1.txt")))
    for p in paths:
        w = windows(p)
        name = os.path.basename(p)
        if not w:
            print(f"  {name:28} no warm standing idle")
            continue
        r = [x[1] for x in w]
        print(f"  {name:28} {len(w):3d} windows  ratio median {statistics.median(r):.3f}"
              f"  range {min(r):.3f}-{max(r):.3f}")
        if args.windows:
            for t, ratio, o in w:
                print(f"      {t:7.0f} s  {ratio:.3f}  oil {o}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
