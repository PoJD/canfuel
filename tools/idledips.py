#!/usr/bin/env python3
"""Count transient dips of engine speed against its own one-second median.

This is the measurement behind the idle tables in docs/engine-health.md. It
exists as a tool rather than as a number typed into prose because the first
pass at it was an ad-hoc script that was not kept, and a later reconstruction
of it disagreed with the published counts by two events -- small, but nobody
could tell which of the two was right, which is the whole failure mode the
"numbers in prose" rules in CLAUDE.md are about.

What it measures, and why it is this and not the maximum
--------------------------------------------------------

The symptom is a small event *repeating*, not one large excursion, so the
question is how often engine speed leaves its own recent baseline and by how
much. For every 0x280 frame the median of all samples within +/- 0.5 s is
taken as the baseline, and a sample sitting THRESHOLD rpm or more below it
opens a dip; the dip closes on the first sample that is not. One dip is one
event however many consecutive samples it spans, which is what makes the
counts comparable between logs of different length.

A rolling median rather than a mean or a fixed idle speed: the baseline has to
survive both the warm-up ramp, where idle falls from about 930 to 800 rpm over
five minutes, and the dips themselves. A median of roughly ninety samples does
both, and needs no sort to be defensible -- unlike the firmware, this runs on
a laptop.

Usage
-----

    python idledips.py                       # the table in engine-health.md
    python idledips.py FILE [FILE ...]       # one line per log
    python idledips.py --from 50 --to 360 FILE
    python idledips.py --thresholds 15,20,25 FILE
"""

from __future__ import annotations

import argparse
import bisect
import os
import statistics
import sys

import canlog

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, os.pardir, "test", "fixtures")

#: The logs the published table is built from, with the window each is read
#: over. None means the whole log. 18 starts after the cold-start flare has
#: settled -- the ramp from 300 to 1450 rpm is not idle and no baseline can
#: describe it.
TABLE = (
    ("09_idle_60s_z1.txt", None, None),
    ("11_idle_noac_z1.txt", None, None),
    ("12_idle_ac_z1.txt", None, None),
    ("18_coldstart_z1.txt", 50.0, 360.0),
)

WINDOW_S = 0.5  # half-width of the median window


def series(path: str) -> tuple[list, list, list]:
    """Engine speed, oil and coolant against time in seconds."""
    frames = canlog.parse_file(path)
    if not frames or frames[0].ts_ms is None:
        raise SystemExit(
            f"{path}: no adapter timestamps. Only the _z1 logs can be read "
            f"for this -- see test/fixtures/README.md."
        )
    t0 = frames[0].ts_ms
    rpm, oil, clt = [], [], []
    for f in frames:
        t = (f.ts_ms - t0) / 1000.0
        if f.can_id == 0x280 and len(f.data) >= 8:
            rpm.append((t, (f.data[2] | (f.data[3] << 8)) / 4.0))
        elif f.can_id == 0x420 and len(f.data) >= 4:
            oil.append((t, f.data[3] * 0.75 - 48.0))
        elif f.can_id == 0x288 and len(f.data) >= 2:
            clt.append((t, f.data[1] * 0.75 - 48.0))
    return rpm, oil, clt


def dips(rpm, threshold, t_from=None, t_to=None):
    """Dip events: (time of the deepest sample, depth in rpm)."""
    seg = [
        (t, r)
        for t, r in rpm
        if (t_from is None or t >= t_from) and (t_to is None or t < t_to)
    ]
    times = [t for t, _ in seg]
    values = [r for _, r in seg]
    events = []
    inside, deepest, at = False, 0.0, 0.0
    for t, r in seg:
        lo = bisect.bisect_left(times, t - WINDOW_S)
        hi = bisect.bisect_right(times, t + WINDOW_S)
        depth = statistics.median(values[lo:hi]) - r
        if depth >= threshold:
            if not inside:
                inside, deepest, at = True, depth, t
            elif depth > deepest:
                deepest, at = depth, t
        elif inside:
            events.append((at, deepest))
            inside = False
    if inside:
        events.append((at, deepest))
    span = (seg[-1][0] - seg[0][0]) if len(seg) > 1 else 0.0
    return events, span


def _last(seq, t):
    vals = [v for tt, v in seq if tt <= t]
    return vals[-1] if vals else float("nan")


def report(path, thresholds, t_from, t_to, label=None):
    rpm, oil, clt = series(path)
    counts, span = [], 0.0
    for thr in thresholds:
        ev, span = dips(rpm, thr, t_from, t_to)
        counts.append(ev)
    seg = [
        r
        for t, r in rpm
        if (t_from is None or t >= t_from) and (t_to is None or t < t_to)
    ]
    end = t_to if t_to is not None else rpm[-1][0]
    cells = "  ".join(
        "%4d (%5.1f/min)" % (len(ev), len(ev) * 60 / span if span else 0)
        for ev in counts
    )
    print(
        "%-26s %6.1fs  %5.0f rpm  %s  oil %5.2f  clt %6.2f"
        % (
            label or os.path.basename(path),
            span,
            sum(seg) / len(seg) if seg else 0,
            cells,
            _last(oil, end),
            _last(clt, end),
        )
    )
    return counts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="logs to read (default: the table)")
    ap.add_argument("--thresholds", default="20,15", help="rpm, comma separated")
    ap.add_argument("--from", dest="t_from", type=float, default=None)
    ap.add_argument("--to", dest="t_to", type=float, default=None)
    args = ap.parse_args(argv)

    thresholds = [int(x) for x in args.thresholds.split(",")]
    header = "  ".join("%15s" % ("dips >=%d rpm" % t) for t in thresholds)
    print("%-26s %7s  %9s  %s" % ("log", "span", "mean", header))

    if args.files:
        for path in args.files:
            report(path, thresholds, args.t_from, args.t_to)
    else:
        for name, lo, hi in TABLE:
            report(os.path.join(FIXTURES, name), thresholds, lo, hi)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
