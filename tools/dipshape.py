#!/usr/bin/env python3
"""How many strokes make one idle dip? The anatomy of the dips, stroke by stroke.

`idledips.py` and the firmware count a dip once however many strokes it
spans. This asks the question they cannot: **is a dip one weak firing, or
two or three weak firings in a row?** Two in a row are always two
DIFFERENT cylinders -- consecutive 180 deg windows are consecutive cylinders
in the firing order 1-3-4-2 -- so a dip of several strokes would point at a
cause shared for a moment (mixture, air), one of one stroke at a cylinder.

What one stroke looks like
--------------------------

0x280's engine speed is recomputed once per 180 deg of crank, one power
stroke (docs/firmware/can-decoding.md trap 6). **A stroke that gives nothing
is one step, not two**: on `43`'s cut on injector 4 the dead slot reads one
step of about -24 rpm, and the next window +17 (docs/engine-health/open.md,
S1, *How many strokes make a dip*). So two losing steps in a row are two
weak strokes, not one weak stroke smeared over two windows.

The method
----------

Within a phase-intact run of strokes (`cutscan.stroke_runs`), a dip opens
where a stroke sits DIP_DEPTH_RPM or more below the median of the REF_STROKES
before it. The descent is walked back to its last rise and forward to its
trough; every step in it that loses more than LOSE_RPM is a **weak stroke**.
A dip with one is a single, with two or more a cluster. The next dip is
looked for only once speed is back within REARM_RPM of the reference, as
the firmware's rearm does.

LOSE_RPM sits just beyond the noise: on warm settled idle a step is
+-4.9 rpm (one standard deviation) and one in twenty loses more than 8.2
(pooled over every warm `_z1` fixture, 5/11/2026). *Decided*, not derived.

**A chance check that needs no simulation**: of all strokes, how many lose
more than LOSE_RPM -- and of those straight after a stroke that lost, how
many do. Weak strokes that came independently would follow one another at
the base rate. (A shuffle of the steps is no null: the shuffled sum
wanders like a random walk and makes dips of its own.)

The two caveats that bound every figure
---------------------------------------

- **Requiring 20 rpm favours clusters by construction**: two steps of -12
  make a dip that one step of -12 does not. The share of clusters is
  therefore not the share of weak strokes that come in pairs; the
  follow-on rate against the base rate is the measure of clustering.
- **The deepest dips (40 rpm and more) are mostly slow sags**, their largest
  single step a fifth of the drop -- a load coming on, the regulator, not a
  run of failed firings. Few, and read apart.

Usage
-----

    python dipshape.py CAPTURE...                  # warm (oil >= 80 C) idle
    python dipshape.py --min-oil 0 CAPTURE...      # every settled idle
    python dipshape.py --name --order 4 CAPTURE    # a capture with a cut:
                                                   # which cylinders cluster

Injector cuts (`cutscan.find_cuts`) are left out with a 5 s margin, so a
capture with a cut reads its ordinary idle only.
"""

from __future__ import annotations

import argparse
import bisect
import collections
import statistics
import sys

import cutscan
import idledips

#: Strokes before a dip whose median is its reference (about 0.6 s at idle).
REF_STROKES = 16
#: A dip opens this far below the reference -- the firmware's trip.
DIP_DEPTH_RPM = float(idledips.TRIP_RPM)
#: ...and the next is looked for once speed is back this close to it.
REARM_RPM = float(idledips.REARM_RPM)
#: A step losing more than this is a weak stroke. *Decided*: the noise's p5.
LOSE_RPM = 8.0
#: Warm, by the oil, as everywhere in the engine-health files.
WARM_OIL_C = 80.0
#: Margin around an injector cut, as cutscan keeps it.
CUT_MARGIN_S = 5.0
#: Depth bands of the report, rpm.
DEPTH_BANDS = ((20, 25), (25, 30), (30, 40), (40, 999))


# --- the dips --------------------------------------------------------------

def dips(run, ref=REF_STROKES, depth=DIP_DEPTH_RPM, lose=LOSE_RPM,
         rearm=REARM_RPM):
    """The dips of one run of (time, rpm) strokes.

    Each is a dict: t (the stroke that crossed), depth (reference minus the
    trough), weak (run indices of the strokes that lost more than `lose`),
    biggest (the largest single loss over the whole drop, 0-1).
    """
    v = [r for _, r in run]
    out = []
    i = ref
    while i < len(v):
        base = statistics.median(v[i - ref:i])
        if base - v[i] < depth:
            i += 1
            continue
        s = i
        while s > i - ref + 1 and v[s - 1] > v[s]:
            s -= 1
        e = i
        while e + 1 < len(v) and v[e + 1] < v[e]:
            e += 1
        steps = [(j, v[j] - v[j - 1]) for j in range(s + 1, e + 1)]
        weak = [j for j, x in steps if x < -lose]
        if not weak:            # one step from a level below the median
            weak = [i]
        drop = v[s] - v[e] if e > s else base - v[i]
        biggest = max((-x for _, x in steps), default=drop)
        out.append({"t": run[i][0], "depth": base - v[e], "weak": weak,
                    "biggest": biggest / drop if drop > 0 else 1.0})
        j = e
        while j < len(v) and base - v[j] > rearm:
            j += 1
        i = max(j, e) + 1
    return out


def follow_on(runs, lose=LOSE_RPM):
    """(strokes, base rate, after a weak stroke) -- the chance check."""
    n = weak = after = after_weak = 0
    for run in runs:
        v = [r for _, r in run]
        st = [v[k] - v[k - 1] for k in range(1, len(v))]
        n += len(st)
        weak += sum(1 for x in st if x < -lose)
        for a, b in zip(st, st[1:]):
            if a < -lose:
                after += 1
                after_weak += b < -lose
    return n, (weak / n if n else 0.0), (after_weak / after if after else 0.0)


# --- which idle --------------------------------------------------------------

def _oil_at(oil, t):
    if not oil:
        return None
    k = bisect.bisect_right([o[0] for o in oil], t) - 1
    return oil[max(k, 0)][1]


def idle_runs(path, min_oil=WARM_OIL_C):
    """Phase-intact runs of a capture's idle at or above `min_oil`, with
    every injector cut cut out."""
    _, oil, _, gated = idledips.series(path)
    runs = cutscan.stroke_runs(gated)
    cuts = cutscan.find_cuts(runs)
    out = []
    for run in runs:
        piece = []
        for p in run:
            if any(a - CUT_MARGIN_S <= p[0] <= b + CUT_MARGIN_S for a, b in cuts):
                if len(piece) > REF_STROKES:
                    out.append(piece)
                piece = []
            else:
                piece.append(p)
        if len(piece) > REF_STROKES:
            out.append(piece)
    if min_oil > 0:
        out = [r for r in out
               if (o := _oil_at(oil, r[0][0])) is not None and o >= min_oil]
    return out


# --- naming ------------------------------------------------------------------

def named_clusters(path, order):
    """In a capture with cuts: the cylinder of every weak stroke.

    Returns (singles {cyl: n}, cluster starts {cyl: n}, pairs {(a, b): n}).
    Uses cutscan's bridged runs and its rule for naming a run by its cuts;
    a stretch is cut wherever the bridge skipped a stroke, so a pair is
    always two strokes that were both seen.
    """
    gated = idledips.series(path)[3]
    cuts = cutscan.find_cuts(cutscan.stroke_runs(gated))
    if len(cuts) != len(order):
        raise SystemExit("found %d cuts, the order names %d"
                         % (len(cuts), len(order)))
    singles, starts, pairs = (collections.Counter() for _ in range(3))
    for run in cutscan.bridged_runs(gated):
        slot_of = []
        for (a, b), cyl in zip(cuts, order):
            w = [(i, r) for t, r, i in run if a + 5 <= t < b - 5]
            if len(w) < 100:
                continue
            med = [statistics.median([r for i, r in w if i % 4 == k])
                   for k in range(4)]
            dead = min(range(4), key=lambda k: med[k])
            slot_of.append((dead - cutscan.FIRING_ORDER.index(cyl)) % 4)
        if len(set(slot_of)) != 1:
            continue
        base = slot_of[0]

        def cyl(i):
            return cutscan.FIRING_ORDER[(i - base) % 4]

        keep = [p for p in run if not any(
            a - CUT_MARGIN_S <= p[0] <= b + CUT_MARGIN_S for a, b in cuts)]
        stretches, cur = [], []
        for p in keep:
            if cur and p[2] != cur[-1][2] + 1:
                stretches.append(cur)
                cur = []
            cur.append(p)
        stretches.append(cur)
        for s in stretches:
            idx = [i for _, _, i in s]
            for d in dips([(t, r) for t, r, _ in s]):
                w = [idx[k] for k in d["weak"]]
                if len(w) == 1:
                    singles[cyl(w[0])] += 1
                    continue
                starts[cyl(w[0])] += 1
                for a, b in zip(w, w[1:]):
                    if b == a + 1:
                        pairs[(cyl(a), cyl(b))] += 1
    return singles, starts, pairs


# --- the report ----------------------------------------------------------------

def shape(ds):
    """(n, % single, % two, % three or more, median depth)."""
    n = len(ds)
    if not n:
        return 0, 0.0, 0.0, 0.0, 0.0
    k = [len(d["weak"]) for d in ds]
    return (n, 100.0 * k.count(1) / n, 100.0 * k.count(2) / n,
            100.0 * sum(1 for x in k if x >= 3) / n,
            statistics.median(d["depth"] for d in ds))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("captures", nargs="+")
    ap.add_argument("--min-oil", type=float, default=WARM_OIL_C,
                    help="oil at the start of a run, C (0 = every idle)")
    ap.add_argument("--name", action="store_true",
                    help="a capture with cuts: the cylinders of the weak strokes")
    ap.add_argument("--order", default="4", help="the cut order, as cutscan's")
    args = ap.parse_args(argv)

    if args.name:
        order = [int(x) for x in args.order.split(",")]
        for cap in args.captures:
            singles, starts, pairs = named_clusters(cap, order)
            print(cap.split("/")[-1])
            print("  single-stroke dips by cylinder: %s (%d)" % (
                " ".join("%d:%d" % (c, singles[c]) for c in (1, 2, 3, 4)),
                sum(singles.values())))
            print("  clusters by first weak cylinder: %s (%d)" % (
                " ".join("%d:%d" % (c, starts[c]) for c in (1, 2, 3, 4)),
                sum(starts.values())))
            print("  consecutive weak pairs, in firing order: %s" % " ".join(
                "%d>%d:%d" % (a, b, pairs[(a, b)])
                for a, b in ((1, 3), (3, 4), (4, 2), (2, 1))))
        return 0

    pooled, all_runs = [], []
    print("%-30s %7s %5s %6s %5s %5s %5s %6s" % (
        "capture", "strokes", "dips", "/1000", "1", "2", "3+", "depth"))
    for cap in args.captures:
        runs = idle_runs(cap, args.min_oil)
        ds = [d for r in runs for d in dips(r)]
        strokes = sum(len(r) for r in runs)
        pooled += ds
        all_runs += runs
        if not ds:
            continue
        n, one, two, more, dep = shape(ds)
        print("%-30s %7d %5d %6.1f %4.0f%% %4.0f%% %4.0f%% %6.1f" % (
            cap.split("/")[-1][:30], strokes, n, 1000.0 * n / strokes,
            one, two, more, dep))
    if not pooled:
        print("no dips")
        return 0
    strokes = sum(len(r) for r in all_runs)
    n, one, two, more, dep = shape(pooled)
    print("%-30s %7d %5d %6.1f %4.0f%% %4.0f%% %4.0f%% %6.1f" % (
        "pooled", strokes, n, 1000.0 * n / strokes, one, two, more, dep))
    print("\nby depth (pooled):")
    for lo, hi in DEPTH_BANDS:
        ds = [d for d in pooled if lo <= d["depth"] < hi]
        if ds:
            n, one, two, more, _ = shape(ds)
            print("  %3d-%-3s rpm  %5d dips  1: %3.0f%%  2: %3.0f%%  3+: %3.0f%%"
                  "  largest step %.2f of the drop" % (
                      lo, hi if hi < 999 else "", n, one, two, more,
                      statistics.median(d["biggest"] for d in ds)))
    n, base, after = follow_on(all_runs)
    print("\nchance check: %d steps; %.1f%% lose more than %.0f rpm, "
          "%.1f%% of those straight after one that did (%.1fx)" % (
              n, 100 * base, LOSE_RPM, 100 * after,
              after / base if base else 0.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
