#!/usr/bin/env python3
"""What 0x280 byte 7 has actually been observed to reach, and under what.

This is the measurement behind *What b7 has actually been observed to reach*
in docs/firmware/frames.md. It exists as a tool for the same reason tools/idledips.py
does -- the figures it prints decide how the next drive's result is read, and
a figure typed into prose cannot be re-checked against a new capture.

What it answers
---------------

The torque scale was once derived from b7 = 255, on the premise that full
scale is the rated crank torque plus the drag. This tool is how that premise
was first doubted -- the engine had never been seen near 255 -- and it is now
read off the plateau the engine actually reaches (docs/firmware/can-decoding.md
question 8). It separates three things that a bare maximum runs together:

* **Cranking is not driving.** 192 appears in 06 and 18, every sample below
  900 rpm with the throttle at rest seconds after the key -- the ECU asking for
  torque to start the engine. Excluded by the gate the torque rule in
  src/compute.c uses; behind it the largest b7 the engine has been seen to make
  is 206, in 19_postfix_drive_z1.
* **A maximum is not a plateau.** Every wide-open burst before the repair was
  still climbing when the throttle closed -- a low-gear sweep that ended before
  the engine filled -- which is why b7max before the repair and after it are
  not a comparison. The held pulls in 19 are the first bursts that stop rising,
  and the count per log says how many did.
* **The byte is not 8-bit resolution.** b7 moves in steps of two over almost
  all of its range, with a parity flip at each multiple of 64. One step is
  therefore about 0.8 % of full scale rather than 0.39 %.

Usage
-----

    python b7scan.py                     # the fixtures
    python b7scan.py FILE [FILE ...]
    python b7scan.py --ladder            # the distinct values b7 ever takes
"""

from __future__ import annotations

import argparse
import glob
import os

import canlog

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, os.pardir, "test", "fixtures")

#: The gate src/compute.c applies before it will display torque at all, and the
#: same one that keeps cranking out of the maximum below. Both come from
#: src/config.h; see docs/firmware/can-decoding.md for why neither is an equality.
GATE_SPEED_MMH = 100
GATE_THROTTLE = 38

WOT_THROTTLE = 150  # "the driver meant it" -- well past part load, short of the stop


def samples(path):
    """(t, rpm, throttle, load byte, b7) per 0x280 frame, road speed gated in.

    Time is None on the logs without adapter timestamps; nothing here needs it
    except the burst walk, which skips those logs.
    """
    frames = canlog.parse_file(
        path, fix_doubled=os.path.basename(path).startswith("02"))
    t0 = frames[0].ts_ms if frames and frames[0].ts_ms is not None else None
    out, speed_mmh = [], 0
    for f in frames:
        if f.can_id == 0x1A0 and len(f.data) >= 4:
            # docs/firmware/can-decoding.md trap 1: the gate is not an equality.
            if (f.data[1] & 0x40) != 0 and (f.data[1] & 0x03) == 0:
                speed_mmh = (f.data[2] | (f.data[3] << 8)) * 5
        elif f.can_id == 0x280 and len(f.data) >= 8:
            t = None if t0 is None else (f.ts_ms - t0) / 1000.0
            out.append((t, (f.data[2] | (f.data[3] << 8)) / 4.0,
                        f.data[5], f.data[6], f.data[7], speed_mmh))
    return out


def driving(rows):
    """The samples src/compute.c would display a torque for at all."""
    return [r for r in rows
            if r[5] > GATE_SPEED_MMH and r[2] > GATE_THROTTLE and r[1] > 0]


def peak(rows):
    """The largest b7 the engine was seen to make, and where. None if never."""
    d = driving(rows)
    return max(d, key=lambda r: r[4]) if d else None


def bursts(rows, throttle=WOT_THROTTLE, gap_s=1.0):
    """Runs of wide-open throttle, split on a gap. Needs adapter timestamps."""
    wot = [r for r in driving(rows) if r[2] >= throttle and r[0] is not None]
    out, cur = [], []
    for r in wot:
        if cur and r[0] - cur[-1][0] > gap_s:
            out.append(cur)
            cur = []
        cur.append(r)
    if cur:
        out.append(cur)
    return out


def still_rising(burst, tail=0.25):
    """Was b7 still climbing when the burst ended?

    True when the largest b7 of the burst falls in its last `tail` fraction --
    the pull ran out before the engine did, so its maximum is a property of the
    gear and the road rather than of the engine.
    """
    if len(burst) < 10:
        return None
    best = max(range(len(burst)), key=lambda i: burst[i][4])
    return best >= int(len(burst) * (1.0 - tail))


def ladder(paths):
    """Every distinct value b7 takes across the given logs, in order."""
    seen = set()
    for p in paths:
        seen.update(r[4] for r in samples(p))
    return sorted(seen)


def steps(values):
    """The gaps between consecutive distinct values, as a count per gap."""
    out = {}
    for a, b in zip(values, values[1:]):
        out[b - a] = out.get(b - a, 0) + 1
    return out


def report(path):
    rows = samples(path)
    top = peak(rows)
    raw = max((r[4] for r in rows), default=0)
    name = os.path.basename(path)
    if top is None:
        print("%-28s   %3d raw, none while driving" % (name, raw))
        return
    bs = bursts(rows)
    rising = [still_rising(b) for b in bs]
    note = ""
    if bs:
        n = sum(1 for r in rising if r)
        note = "  %d WOT burst%s, %d still rising at the end" % (
            len(bs), "" if len(bs) == 1 else "s", n)
    print("%-28s   %3d raw   %3d driving (%4.1f%% of 255) at %5.0f rpm, throttle %3d%s"
          % (name, raw, top[4], top[4] * 100.0 / 255, top[1], top[2], note))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="logs to read (default: the fixtures)")
    ap.add_argument("--ladder", action="store_true",
                    help="print the distinct values b7 ever takes")
    args = ap.parse_args(argv)

    paths = args.files or sorted(glob.glob(os.path.join(FIXTURES, "*.txt")))
    if args.ladder:
        vals = ladder(paths)
        print("%d distinct values, %d to %d" % (len(vals), vals[0], vals[-1]))
        print(" ".join(str(v) for v in vals))
        print("gaps between consecutive values:", steps(vals))
        return 0

    for p in paths:
        report(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
