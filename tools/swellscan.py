#!/usr/bin/env python3
"""Cylinder 3's swell and the common part -- a standing idle window by window.

docs/engine-health/open.md, S1, *The swell's shape, and what the common part
follows*. Written 12/11/2026 for the owner's two questions -- what makes
cylinder 3's waves, and whether the common part moves with anything -- and
kept at his request, for the reason cylscan.py gives for itself: the reading
is repeated on every captured stop, and a script that is not kept cannot be
checked.

cylscan.py puts every stroke on its cylinder. This reads what it gives in
windows of `WINDOW_S`, beside everything else the bus carries:

* **3's deficit** (`d3`), per cent of a stroke's work under the four's mean,
  and its weak strokes;
* **the common part** (`common`): the scatter, rpm rms, of cylinder 2's
  steps about their own median. Cylinder 2's slot is the one farthest from
  cylinder 3's weak strokes and their spill (one slot before, the recovery
  one after), so it is what all four share and nothing of 3's;
* the oil, the coolant, 0x280 b6 and b7, the injection time (0x288 b6), the
  fuel counter's rate, the lights (0x420 b5), the brake pedal, the tank's
  level, the A/C, the time into the stop and the seconds above `HIGH_RPM`
  in the `HIGH_LOOK_S` before it.

What comes out
--------------

default     one line a capture: the warm loads-off windows, the common part
            and each cylinder's scatter, 3's deficit.
``--series``  every warm stop of `SERIES_MIN_S` and more, window by window:
            where the swells show as a sawtooth.
``--falls``   every fall of 3's deficit with no cut and no A/C, in
            `FINE_S` windows: how long it takes, and what the bus did.
``--corr``    what 3's deficit and the common part go with, over every file
            given: pooled, and within a stop (each stop's mean taken out).
``--csv OUT`` the windows, one row each.

    python swellscan.py test/fixtures/4?_*_z1.txt
    python swellscan.py --series --falls test/fixtures/49_warm_drive_z1.txt
    python swellscan.py --corr test/fixtures/[234]?_*_z1.txt
"""
from __future__ import annotations

import argparse
import bisect
import csv
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canlog  # noqa: E402
import cylscan  # noqa: E402

#: The window everything is read in; 30 s holds about 100 strokes a cylinder.
WINDOW_S = 30.0
#: Warm, as cylscan.py has it; loads off is the A/C off for the whole window.
WARM_OIL_C = cylscan.WARM_OIL_C
#: High revs before a stop: engine speed above this, in the seconds before.
HIGH_RPM = 4000.0
HIGH_LOOK_S = 900.0
#: `--series` prints stops of at least this length.
SERIES_MIN_S = 240.0
#: A fall: 3's deficit `FALL_FROM` or deeper, and `FALL_RISE` shallower
#: within `FALL_WINDOWS` windows, no cut and no A/C between.
FALL_FROM = -17.0
FALL_RISE = 8.0
FALL_WINDOWS = 3
#: `--falls` reads a fall in windows this long, this far apart, from
#: `FINE_BEFORE_S` before the first of its windows to `FINE_AFTER_S` after.
FINE_S = 8.0
FINE_STEP_S = 4.0
FINE_BEFORE_S = 30.0
FINE_AFTER_S = 120.0
#: The fall's duration is read between these shares of its drop.
FALL_SHARES = (0.2, 0.8)

#: What a window carries beside the cylinders; `--corr` reads these.
COVARIATES = ("oil", "cool", "b7", "b6", "inj", "fuel", "rpm", "dim",
              "brake", "tank", "into", "high")


# --- reading ----------------------------------------------------------------

def signals(frames):
    """{name: [(t, value)]} for what cylscan.read() leaves on the bus."""
    t0 = frames[0].ts_ms
    s = {k: [] for k in ("cool", "inj", "b7", "b6", "dim", "brake", "tank")}
    for f in frames:
        t = (f.ts_ms - t0) / 1000.0
        d = f.data
        if f.can_id == 0x288 and len(d) >= 7:
            s["cool"].append((t, d[1] * 0.75 - 48.0))
            s["inj"].append((t, d[6]))
        elif f.can_id == 0x280 and len(d) >= 8:
            s["b6"].append((t, d[6]))
            s["b7"].append((t, d[7]))
        elif f.can_id == 0x420 and len(d) >= 6:
            s["dim"].append((t, d[5]))
        elif f.can_id == 0x1A0 and len(d) >= 2:
            s["brake"].append((t, 1.0 if d[1] & 0x08 else 0.0))
        elif f.can_id == 0x320 and len(d) >= 3:
            s["tank"].append((t, d[2]))
    return s


def mean_in(pairs, t0, t1):
    """The mean of a [(t, value)] series over t0 <= t < t1; NaN with none."""
    i = bisect.bisect_left(pairs, (t0, -math.inf))
    j = bisect.bisect_left(pairs, (t1, -math.inf))
    v = [x[1] for x in pairs[i:j] if x[1] is not None]
    return sum(v) / len(v) if v else math.nan


def rms(v):
    return math.sqrt(sum(x * x for x in v) / len(v)) if v else math.nan


class Capture:
    """One `_z1` capture: cylscan's data, the other signals, the idle runs."""

    def __init__(self, path):
        frames = canlog.parse_file(path)
        if not frames or frames[0].ts_ms is None:
            raise SystemExit(f"{path}: no adapter timestamps; only the _z1 "
                             "logs can be read for this")
        self.name = os.path.basename(path)[:2]
        self.data = cylscan.read(path, frames)
        self.sig = signals(frames)
        self.sig["oil"] = self.data["oil"]
        self.sig["rpm"] = [(x[0], x[1]) for x in self.data["e"]]
        self.sig["ac"] = [(t, 1.0 if on else 0.0) for t, on in self.data["ac"]]
        self.runs = [r for r in cylscan.idle_runs(self.data) if r.named]
        e = self.data["e"]
        self._et = [x[0] for x in e]
        self._high = [0.0]
        for k in range(1, len(e)):
            dt = e[k][0] - e[k - 1][0]
            self._high.append(self._high[-1]
                              + (dt if e[k][1] > HIGH_RPM and dt < 0.5 else 0.0))

    def high_s(self, t0, t1):
        """Seconds above `HIGH_RPM` between t0 and t1."""
        i = max(bisect.bisect_left(self._et, t0) - 1, 0)
        j = max(bisect.bisect_left(self._et, t1) - 1, 0)
        return self._high[j] - self._high[i]

    def fuel_rate(self, t0, t1):
        """The fuel counter's counts a second over t0..t1."""
        fuel = self.data["fuel"]
        i = bisect.bisect_left(fuel, (t0, -1))
        j = bisect.bisect_left(fuel, (t1, -1)) - 1
        if j <= i:
            return math.nan
        return ((fuel[j][1] - fuel[i][1]) % 32768) / (fuel[j][0] - fuel[i][0])


def window(cap, run, t0, t1):
    """One window of a run as a row; None where a cut or too few strokes
    leave nothing to read."""
    i0, i1 = run.span(t0, t1)
    if i1 - i0 < 8 or any(run.cut[i0:i1]):
        return None
    dev = cylscan.deviation(run, i0, i1)
    if dev is None:
        return None
    w, _ = cylscan.weak(run, i0, i1)
    E = {c: [] for c in cylscan.FIRING_ORDER}
    for i in range(max(i0, 1), i1):
        if run.E[i] is not None:
            E[run.cyl(i)].append(run.E[i])
    row = {"cap": cap.name, "t": t0, "into": t0 - run.T[1],
           "common": rms(E[2]),
           "rpm": sum(run.R[i0:i1]) / (i1 - i0),
           "fuel": cap.fuel_rate(t0, t1),
           "high": cap.high_s(t0 - HIGH_LOOK_S, t0)}
    for c in cylscan.FIRING_ORDER:
        row[f"d{c}"] = dev[c]
        row[f"w{c}"] = w[c]
        row[f"e{c}"] = rms(E[c])
    for k in ("oil", "ac", "cool", "inj", "b7", "b6", "dim", "brake", "tank"):
        row[k] = mean_in(cap.sig[k], t0, t1)
    return row


def stops(cap, width=WINDOW_S):
    """[(run, [row or None, ...])] -- every named idle run in windows."""
    out = []
    for run in cap.runs:
        rows, t = [], run.T[1]
        while t + width <= run.T[-1]:
            rows.append(window(cap, run, t, t + width))
            t += width
        if rows:
            out.append((run, rows))
    return out


def warm_off(row):
    """A window that counts as warm with the loads off."""
    return (row is not None and row["oil"] == row["oil"]
            and row["oil"] >= WARM_OIL_C and row["ac"] < 0.05)


# --- the falls --------------------------------------------------------------

def find_falls(rows):
    """[(i, j)]: 3's deficit at rows[i] is `FALL_FROM` or deeper and at
    rows[j], within `FALL_WINDOWS`, `FALL_RISE` shallower, every window
    between read and loads off. One per swell: the search goes on from j."""
    out, i, n = [], 0, len(rows)
    while i < n:
        hit = None
        if warm_off(rows[i]) and rows[i]["d3"] <= FALL_FROM:
            for j in range(i + 1, min(i + FALL_WINDOWS, n - 1) + 1):
                if not warm_off(rows[j]):
                    break
                if rows[j]["d3"] - rows[i]["d3"] >= FALL_RISE:
                    hit = j
                    break
            # the deepest window before the rise is where the fall starts
            if hit is not None:
                k = i
                while k + 1 < hit and rows[k + 1]["d3"] <= rows[k]["d3"]:
                    k += 1
                out.append((k, hit))
                i = hit
        i += 1
    return out


def fine(cap, run, t0, t1):
    """[(t, d3)] in `FINE_S` windows every `FINE_STEP_S` over t0..t1."""
    out, t = [], max(t0, run.T[1])
    while t + FINE_S <= min(t1, run.T[-1]):
        i0, i1 = run.span(t, t + FINE_S)
        if not any(run.cut[i0:i1]):
            dev = cylscan.deviation(run, i0, i1)
            if dev is not None:
                out.append((t, dev[3]))
        t += FINE_STEP_S
    return out


def fall_seconds(series):
    """How long 3's deficit takes to fall: from the last window still within
    `FALL_SHARES[0]` of the way from its level before (the median of the
    series' first third) to its level after (of its last third), to the
    first window from which it stays beyond `FALL_SHARES[1]`. None where
    the two levels are not a fall apart."""
    n = len(series)
    if n < 9:
        return None
    lo = statistics.median(d for _, d in series[:n // 3])
    hi = statistics.median(d for _, d in series[-(n // 3):])
    if hi - lo < FALL_RISE / 2:
        return None
    a = lo + FALL_SHARES[0] * (hi - lo)
    b = lo + FALL_SHARES[1] * (hi - lo)
    below = [k for k, (_, d) in enumerate(series) if d < b]
    end = below[-1] + 1 if below else 0
    if end >= n:
        return None
    start = max((k for k in range(end) if series[k][1] <= a), default=None)
    if start is None:
        return None
    return series[end][0] - series[start][0]


# --- correlation ------------------------------------------------------------

def corr(x, y):
    """(Pearson r, pairs) over the pairs where both are numbers."""
    p = [(a, b) for a, b in zip(x, y) if a == a and b == b]
    if len(p) < 8:
        return math.nan, len(p)
    mx = sum(a for a, _ in p) / len(p)
    my = sum(b for _, b in p) / len(p)
    sxx = sum((a - mx) ** 2 for a, _ in p)
    syy = sum((b - my) ** 2 for _, b in p)
    if sxx <= 0 or syy <= 0:
        return math.nan, len(p)
    return sum((a - mx) * (b - my) for a, b in p) / math.sqrt(sxx * syy), len(p)


def within(groups, key, min_n=4):
    """`key` with each group's own mean taken out, in the groups' order;
    NaN for a group with fewer than `min_n` numbers."""
    out = []
    for rows in groups:
        v = [r[key] for r in rows if r[key] == r[key]]
        m = sum(v) / len(v) if len(v) >= min_n else math.nan
        out.extend(r[key] - m for r in rows)
    return out


# --- reports ----------------------------------------------------------------

def _mean(rows, key):
    v = [r[key] for r in rows if r[key] == r[key]]
    return sum(v) / len(v) if v else math.nan


def report_summary(caps_stops, out=sys.stdout):
    print("cap  windows  common   e1   e3   e4    d3   oil   b7", file=out)
    for cap, st in caps_stops:
        rows = [r for _, rs in st for r in rs if warm_off(r)]
        if not rows:
            print(f"{cap.name}   no warm loads-off window", file=out)
            continue
        print(f"{cap.name}   {len(rows):6d}  {_mean(rows, 'common'):6.2f} "
              f"{_mean(rows, 'e1'):4.1f} {_mean(rows, 'e3'):4.1f} "
              f"{_mean(rows, 'e4'):4.1f} {_mean(rows, 'd3'):5.1f} "
              f"{_mean(rows, 'oil'):5.0f} {_mean(rows, 'b7'):4.0f}", file=out)


def report_series(cap, st, out=sys.stdout):
    for run, rows in st:
        read = [r for r in rows if r is not None]
        if (len(rows) * WINDOW_S < SERIES_MIN_S or not read
                or max(r["oil"] for r in read if r["oil"] == r["oil"]) < WARM_OIL_C):
            continue
        print(f"\n{cap.name}  stop from {run.T[1]:.0f} s, "
              f"{len(rows) * WINDOW_S / 60:.1f} min, "
              f"{read[0]['high']:.0f} s above {HIGH_RPM:.0f} rpm before", file=out)

        def line(label, f):
            print(f"  {label:7s}" + "".join(
                "  cut" if r is None else f"{f(r):5.0f}" for r in rows), file=out)
        line("d3 %", lambda r: r["d3"])
        line("weak 3", lambda r: r["w3"])
        line("others", lambda r: r["w1"] + r["w2"] + r["w4"])
        line("comm.x10", lambda r: 10 * r["common"])
        line("A/C", lambda r: r["ac"])
        line("coolant", lambda r: r["cool"])
        line("b7", lambda r: r["b7"])


def report_falls(cap, st, out=sys.stdout):
    for run, rows in st:
        for i, j in find_falls(rows):
            t0 = rows[i]["t"] - FINE_BEFORE_S
            series = fine(cap, run, t0, rows[j]["t"] + FINE_AFTER_S)
            secs = fall_seconds(series)
            print(f"\n{cap.name}  fall from {rows[i]['d3']:.0f} to "
                  f"{rows[j]['d3']:.0f} % at {rows[i]['t']:.0f} s"
                  + (f", {secs:.0f} s from {FALL_SHARES[0]:.0%} to "
                     f"{FALL_SHARES[1]:.0%} of it" if secs is not None else ""),
                  file=out)
            print("     t    d3    b7   inj  coolant  rpm", file=out)
            for t, d in series:
                print(f"  {t - series[0][0]:4.0f} {d:5.0f} "
                      f"{mean_in(cap.sig['b7'], t, t + FINE_S):5.1f} "
                      f"{mean_in(cap.sig['inj'], t, t + FINE_S):5.1f} "
                      f"{mean_in(cap.sig['cool'], t, t + FINE_S):7.1f} "
                      f"{mean_in(cap.sig['rpm'], t, t + FINE_S):5.0f}",
                      file=out)


def report_corr(caps_stops, out=sys.stdout):
    groups = []
    for _, st in caps_stops:
        for _, rows in st:
            g = [r for r in rows if warm_off(r)]
            if g:
                groups.append(g)
    flat = [r for g in groups for r in g]
    print(f"{len(flat)} warm loads-off windows in {len(groups)} stops; "
          "r pooled / within a stop", file=out)
    for target in ("d3", "common"):
        print(f"\n{target}:", file=out)
        others = ("common",) if target == "d3" else ("d3",)
        for k in others + COVARIATES:
            r1, _ = corr([r[target] for r in flat], [r[k] for r in flat])
            r2, _ = corr(within(groups, target), within(groups, k))
            print(f"  {k:7s} {r1:+.2f}  {r2:+.2f}", file=out)


def write_csv(path, caps_stops):
    rows = [r for _, st in caps_stops for _, rs in st for r in rs if r is not None]
    if not rows:
        return
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 3) if isinstance(v, float) else v)
                        for k, v in r.items()})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--series", action="store_true",
                    help="every long warm stop, window by window")
    ap.add_argument("--falls", action="store_true",
                    help="each fall of cylinder 3's deficit, in fine windows")
    ap.add_argument("--corr", action="store_true",
                    help="what the deficit and the common part go with")
    ap.add_argument("--csv", metavar="OUT", help="write the windows")
    args = ap.parse_args(argv)
    caps_stops = []
    for path in args.files:
        cap = Capture(path)
        caps_stops.append((cap, stops(cap)))
    if not (args.series or args.falls or args.corr):
        report_summary(caps_stops)
    for cap, st in caps_stops:
        if args.series:
            report_series(cap, st)
        if args.falls:
            report_falls(cap, st)
    if args.corr:
        report_corr(caps_stops)
    if args.csv:
        write_csv(args.csv, caps_stops)
    return 0


if __name__ == "__main__":
    sys.exit(main())
