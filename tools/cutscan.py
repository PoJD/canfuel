#!/usr/bin/env python3
"""Which cylinder carries the stumble? The injector cut test, read.

This is the reading of `docs/engine-health/plan.md` step 3.5: one injector
connector off at a time at a warm idle, in two rounds, the second reversed
(1, 2, 3, 4, 4, 3, 2, 1 -- or 1, 4, 4, 1 when only the outer two can be
reached). The criteria were fixed in plan.md BEFORE the test was run, so
that the result cannot be read to fit; this file implements them and prints
a verdict rather than a table to be interpreted.

What it does
------------

1. **Finds the cuts in the capture itself.** A dead cylinder leaves one of
   the four per-stroke slots of 0x280's engine speed far below the other
   three, every cycle. Healthy idles measured on `30`, `28`, `09` and `18`
   never put one slot more than 9.4 rpm below the mean of the other three
   in any run; a dead stroke is worth a few tens (S1, *What one dip is
   worth*). `CUT_DEFICIT_RPM` sits between. The owner's own times are a
   cross-check, not the source: the capture has no wall clock.

   It finds exactly as many cuts as the order names, or it stops and says
   so. A guess at which interval is which cylinder would be the one error
   nobody could see afterwards. `--cuts` takes the intervals by hand.

2. **Counts the dips on the three cylinders that still fire.** 0x280 is
   recomputed once per 180 deg of crank (docs/firmware/can-decoding.md trap
   5), so within a run every fourth value is the same cylinder. The run
   breaks whenever two strokes quantise to the same 0.25 rpm and the phase
   is lost (`idledips.cylinder_runs`), so the dead slot is found again in
   every run -- which is easy, since it is the one far below. A stroke is a
   dip when it sits `DIP_RPM` or more below the median of the same
   cylinder's strokes either side of it; adjacent flagged strokes are one
   event. The first `CUT_SETTLE_S` of each cut are skipped while the
   regulator catches up.

3. **Reads the air** off VCDS group 003, if a log is given: the mean over
   the last `AIR_TAIL_S` of each cut, with the ignition angle beside it.

4. **Applies plan.md's four rules** and prints the verdict.

The p-value
-----------

Under "no cylinder is special" every dip is equally likely to fall in any
cut, in proportion to how many firing strokes each cut contributed (its
exposure; runs break, so exposures differ). The statistic is the smallest
rate, count / expected; the p-value is the chance of a minimum at least
that small given the total, by exact enumeration of the multinomial. One
number, no simulation, no seed.

Usage
-----

    python cutscan.py CAPTURE                          # order 1,4,4,1
    python cutscan.py DAY1 DAY2 DAY3                   # sessions, pooled
    python cutscan.py --order 1,2,3,4,4,3,2,1 CAPTURE
    python cutscan.py --vcds LOG.csv CAPTURE           # ...with 003's air
    python cutscan.py --cuts 120-180,210-270,... CAPTURE
    python cutscan.py --scan CAPTURE                   # the per-run deficits
    python cutscan.py --pairs CAPTURE [...]            # history: same-slot pairs, no p
    python cutscan.py --shares CAPTURE [...]           # one cylinder or two
    python cutscan.py --name CAPTURE                   # cuts in it: name the dips
"""

from __future__ import annotations

import argparse
import bisect
import csv
import math
import statistics
import sys
from functools import lru_cache

import idledips

#: A run is a dead-cylinder run when its lowest slot sits this far below the
#: mean of the other three. Healthy runs reach 9.4 rpm at most (30, 28, 09,
#: 18); a dead stroke is worth tens. *Decided*, not measured on a cut -- the
#: first real capture says whether it holds, and --scan prints the deficits.
CUT_DEFICIT_RPM = 12.0
#: A cut shorter than this is not one of the owner's minutes.
CUT_MIN_S = 20.0
#: Dead runs closer than this are the same cut (a run breaks every few s).
CUT_MERGE_S = 6.0
#: Skipped at the start of each cut: the regulator is still catching up.
CUT_SETTLE_S = 5.0
#: A run needs this many strokes before its slots mean anything (6 cycles).
MIN_RUN_STROKES = 24
#: Runs whose mean engine speed is outside this are not idle and are dropped:
#: a blip in neutral or a cranking start makes slot deficits of 13-39 rpm on
#: the existing captures with every cylinder firing.
IDLE_RPM = (600.0, 1050.0)
#: idledips' threshold, so a dip here is the same size as a dip in S1.
DIP_RPM = float(idledips.TRIP_RPM)
#: Same-cylinder neighbours each side for a stroke's baseline (~0.5 s).
DIP_NEIGHBOURS = 3
#: 003's air is averaged over this tail of each cut (plan.md 3.3).
AIR_TAIL_S = 40.0

#: plan.md 3.3's criteria, fixed before the test. Do not tune them to a
#: result: change plan.md first, with the reason, and only then these.
P_ONE = 0.05
P_NONE = 0.20
AIR_WEAK_GS = 0.15
AIR_NONE_GS = 0.08


# --- the strokes ------------------------------------------------------------

def stroke_runs(gated, t_from=None, t_to=None):
    """Runs of (time, rpm), one entry per 180 deg window, phase intact.

    The same break rule as idledips.cylinder_runs(), with the time of each
    window kept, which that function drops. The gate is the idle gate only --
    no settle rule, because a cut itself would trip it.
    """
    out, cur, prev, prev_t, hold = [], [], None, None, 0

    def flush():
        if len(cur) >= MIN_RUN_STROKES:
            mean = sum(r for _, r in cur) / len(cur)
            if IDLE_RPM[0] <= mean <= IDLE_RPM[1]:
                out.append(list(cur))

    for t, q4, throttle, speed in gated:
        if (t_from is not None and t < t_from) or (t_to is not None and t >= t_to):
            continue
        if (speed > idledips.GATE_SPEED_MMH or throttle > idledips.GATE_THROTTLE
                or q4 == 0):
            flush()
            cur, prev = [], None
            continue
        if prev is None:
            prev, prev_t, hold = q4, t, 1
            continue
        if q4 == prev:
            hold += 1
            continue
        if hold >= idledips.CYL_BREAK_HOLD:
            flush()
            cur = []
        cur.append((prev_t, prev / 4.0))
        prev, prev_t, hold = q4, t, 1
    flush()
    return out


def slot_deficit(run):
    """(dead slot, rpm it sits below the mean of the other three)."""
    v = [r for _, r in run]
    med = [statistics.median(v[i::4]) for i in range(4)]
    dead = min(range(4), key=lambda i: med[i])
    others = [med[i] for i in range(4) if i != dead]
    return dead, sum(others) / 3.0 - med[dead]


# --- finding the cuts -------------------------------------------------------

def find_cuts(runs, deficit=CUT_DEFICIT_RPM):
    """Intervals (start, end) in capture seconds where a cylinder is out."""
    spans = []
    for run in runs:
        _, d = slot_deficit(run)
        if d >= deficit:
            spans.append([run[0][0], run[-1][0]])
    merged = []
    for a, b in spans:
        if merged and a - merged[-1][1] <= CUT_MERGE_S:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [(a, b) for a, b in merged if b - a >= CUT_MIN_S]


# --- dips on the firing cylinders -------------------------------------------

def firing_dips(runs, t_from, t_to):
    """(events, firing strokes examined) inside one cut."""
    events = exposure = 0
    for run in runs:
        if run[-1][0] < t_from or run[0][0] >= t_to:
            continue
        dead, _ = slot_deficit(run)
        v = [r for _, r in run]
        flagged_prev = False
        for i, (t, r) in enumerate(run):
            if i % 4 == dead:
                continue                    # the dead stroke: neither dip nor not
            if not (t_from <= t < t_to):
                flagged_prev = False
                continue
            same = [v[j] for j in range(i - 4 * DIP_NEIGHBOURS,
                                        i + 4 * DIP_NEIGHBOURS + 1, 4)
                    if j != i and 0 <= j < len(v)]
            if len(same) < DIP_NEIGHBOURS:
                flagged_prev = False
                continue
            exposure += 1
            low = statistics.median(same) - r >= DIP_RPM
            if low and not flagged_prev:
                events += 1
            flagged_prev = low
    return events, exposure


#: The firing order (*general*, the AQY's 1-3-4-2). Slot k after the dead one
#: in a run is the cylinder k places after the dead one in this order.
FIRING_ORDER = (1, 3, 4, 2)


def named_dips(runs, t_from, t_to, dead_cyl):
    """{cylinder: (events, firing strokes)} inside one cut, by NAME.

    While a cylinder is out its slot is known, and the firing order names the
    other three -- the one measurement on this bus that can put a dip to a
    cylinder. It rests on one assumption, stated rather than proved: that a
    dip shows in its cylinder's slot with the same lag as the dead stroke's
    deficit does. Cutting 1 and cutting 4 both name 2 and 3, so the two must
    agree about them; that is the check.
    """
    pos = FIRING_ORDER.index(dead_cyl)
    out = {c: [0, 0] for c in FIRING_ORDER if c != dead_cyl}
    for run in runs:
        if run[-1][0] < t_from or run[0][0] >= t_to:
            continue
        dead, _ = slot_deficit(run)
        v = [r for _, r in run]
        flagged_prev = {}
        for i, (t, r) in enumerate(run):
            k = (i - dead) % 4
            if k == 0 or not (t_from <= t < t_to):
                continue
            cyl = FIRING_ORDER[(pos + k) % 4]
            same = [v[j] for j in range(i - 4 * DIP_NEIGHBOURS,
                                        i + 4 * DIP_NEIGHBOURS + 1, 4)
                    if j != i and 0 <= j < len(v)]
            if len(same) < DIP_NEIGHBOURS:
                continue
            out[cyl][1] += 1
            low = statistics.median(same) - r >= DIP_RPM
            # one event per run of low strokes of the same cylinder
            if low and not flagged_prev.get(cyl):
                out[cyl][0] += 1
            flagged_prev[cyl] = low
    return {c: tuple(x) for c, x in out.items()}


# --- the statistics ---------------------------------------------------------

def min_rate_p(counts, exposures):
    """P(smallest count/expected <= observed), all cuts alike, given the total.

    Exact: every way of dealing the total over the cuts, weighted by the
    multinomial with probabilities proportional to exposure.
    """
    n = sum(counts)
    k = len(counts)
    if n == 0 or k < 2:
        return 1.0
    tot = float(sum(exposures))
    probs = [e / tot for e in exposures]
    observed = min(c / (n * p) for c, p in zip(counts, probs))
    logp = [math.log(p) for p in probs]
    lf = [math.lgamma(i + 1) for i in range(n + 1)]
    eps = 1e-12

    @lru_cache(maxsize=None)
    def tail(j, left, lo_seen):
        # probability mass of the remaining cells, with the running minimum
        # already at or below `observed` if lo_seen
        if j == k - 1:
            c = left
            hit = lo_seen or c / (n * probs[j]) <= observed + eps
            return math.exp(c * logp[j] - lf[c]) if hit else 0.0
        s = 0.0
        for c in range(left + 1):
            hit = lo_seen or c / (n * probs[j]) <= observed + eps
            s += math.exp(c * logp[j] - lf[c]) * tail(j + 1, left - c, hit)
        return s

    return min(1.0, math.exp(lf[n]) * tail(0, n, False))


def max_rate_p(counts, exposures):
    """P(largest count/expected >= observed), all alike, given the total.

    The mirror of min_rate_p(): the question here is whether one named
    cylinder carries MORE of the dips than its share of the strokes.
    """
    n = sum(counts)
    k = len(counts)
    if n == 0 or k < 2:
        return 1.0
    tot = float(sum(exposures))
    probs = [e / tot for e in exposures]
    observed = max(c / (n * p) for c, p in zip(counts, probs))
    logp = [math.log(p) for p in probs]
    lf = [math.lgamma(i + 1) for i in range(n + 1)]
    eps = 1e-12

    @lru_cache(maxsize=None)
    def tail(j, left, hi_seen):
        if j == k - 1:
            c = left
            hit = hi_seen or c / (n * probs[j]) >= observed - eps
            return math.exp(c * logp[j] - lf[c]) if hit else 0.0
        s = 0.0
        for c in range(left + 1):
            hit = hi_seen or c / (n * probs[j]) >= observed - eps
            s += math.exp(c * logp[j] - lf[c]) * tail(j + 1, left - c, hit)
        return s

    return min(1.0, math.exp(lf[n]) * tail(0, n, False))


def named_verdict(order, named):
    """plan.md 3.3 rule 1, by name. named[i] is named_dips() for cut i.

    Returns (lines, dict). One cylinder if the highest named rate is at
    p < P_ONE over all cuts AND it is the highest in both rounds.
    """
    half = len(order) // 2
    cyls = sorted({c for d in named for c in d})

    def pool(idx):
        ev = {c: 0 for c in cyls}
        ex = {c: 0 for c in cyls}
        for i in idx:
            for c, (e, x) in named[i].items():
                ev[c] += e
                ex[c] += x
        return ev, ex

    ev, ex = pool(range(len(order)))
    named_cyls = [c for c in cyls if ex[c] > 0]
    p = max_rate_p([ev[c] for c in named_cyls], [ex[c] for c in named_cyls])
    rate = {c: ev[c] / ex[c] for c in named_cyls}
    high = max(named_cyls, key=lambda c: rate[c])
    by_round = []
    for idx in (range(0, half), range(half, len(order))):
        e, x = pool(idx)
        ok = [c for c in named_cyls if x[c] > 0]
        by_round.append(max(ok, key=lambda c: e[c] / x[c]))
    one = p < P_ONE and all(r == high for r in by_round)
    res = {"p": p, "high": high, "by_round": by_round, "one": one,
           "rate": rate, "unnamed": [c for c in cyls if ex[c] == 0]}
    lines = ["dips by NAME, per 1000 firing strokes: " + ", ".join(
        "%d: %.1f (%d of %d)" % (c, 1000 * rate[c], ev[c], ex[c])
        for c in named_cyls),
        "p (largest rate, all alike) = %.3g; highest by round: %s"
        % (p, ", ".join(str(r) for r in by_round))]
    if one:
        lines.append(f"VERDICT by name: cylinder {high} carries more of the "
                     f"dips than its share (p < {P_ONE}, highest in both rounds)")
    elif p > P_NONE:
        lines.append("VERDICT by name: no cylinder stands out")
    else:
        lines.append("VERDICT by name: undecided")
    return lines, res


# --- VCDS -------------------------------------------------------------------

def read_vcds(path):
    """{group: [(t, [fields...]), ...]} for every group in a VCDS CSV log."""
    with open(path, encoding="cp1250", newline="") as fh:
        rows = list(csv.reader(fh))
    head = None
    for i, r in enumerate(rows[:10]):
        if any(c.strip().startswith("'0") for c in r):
            head = i
            break
    if head is None:
        raise SystemExit(f"{path}: no measuring-block header found")
    cols = [(j, c.strip()[1:]) for j, c in enumerate(rows[head])
            if c.strip().startswith("'0")]
    out = {g: [] for _, g in cols}
    for r in rows[head + 4:]:
        for j, g in cols:
            try:
                t = float(r[j - 1])
            except (ValueError, IndexError):
                continue
            out[g].append((t, [x.strip() for x in r[j:j + 4]]))
    return out


def align(vcds_rpm, cap_rpm, max_err=40.0):
    """Seconds to add to VCDS time to get capture time, by engine speed."""
    ts = [t for t, _ in cap_rpm]
    rs = [r for _, r in cap_rpm]

    def at(t):
        i = bisect.bisect_right(ts, t) - 1
        return rs[i] if 0 <= i < len(rs) else None

    sample = vcds_rpm[::3]
    best = None
    lo, hi = -vcds_rpm[-1][0], ts[-1]
    off = lo
    while off <= hi:
        err, n = 0.0, 0
        for t, r in sample:
            c = at(t + off)
            if c is not None:
                err += abs(c - r)
                n += 1
        if n >= max(10, len(sample) // 3) and (best is None or err / n < best[0]):
            best = (err / n, off)
        off += 0.5
    if best is None or best[0] > max_err:
        raise SystemExit("VCDS log does not line up with the capture by engine "
                         f"speed (best mean error {best and round(best[0])} rpm)")
    return best[1]


def air_by_cut(vcds, cap_rpm, cuts):
    """[(air g/s, ignition deg)] over the tail of each cut, from group 003."""
    g = vcds.get("003")
    if not g:
        return None
    pts = []
    for t, f in g:
        try:
            pts.append((t, float(f[0]), float(f[1]), float(f[3])))
        except (ValueError, IndexError):
            continue
    off = align([(t, r) for t, r, _, _ in pts], cap_rpm)
    out = []
    for a, b in cuts:
        tail = [(air, ign) for t, _, air, ign in pts
                if max(a, b - AIR_TAIL_S) <= t + off < b]
        out.append((statistics.mean(x for x, _ in tail),
                    statistics.mean(y for _, y in tail)) if tail else (None, None))
    return out, off


def misfires_by_cut(vcds, cap_rpm, cuts, off):
    """014 rises a minute in each cut -- question 11's reading."""
    g = vcds.get("014")
    if not g:
        return None
    pts = []
    for t, f in g:
        try:
            pts.append((t + off, int(float(f[2]))))
        except (ValueError, IndexError):
            continue
    out = []
    for a, b in cuts:
        rises, prev = 0, None
        for t, m in pts:
            if a <= t < b and prev is not None and m > prev:
                rises += 1
            prev = m
        out.append(60.0 * rises / (b - a))
    return out


# --- the verdict ------------------------------------------------------------

def verdict(order, counts, exposures, air=None):
    """plan.md 3.3's rules. Returns (lines, dict) -- the dict for the tests."""
    cyls = sorted(set(order))
    half = len(order) // 2
    rounds = (range(0, half), range(half, len(order)))

    def per_cyl(idx, vals):
        return {c: sum(vals[i] for i in idx if order[i] == c) for c in cyls}

    c_all = per_cyl(range(len(order)), counts)
    e_all = per_cyl(range(len(order)), exposures)
    p = min_rate_p([c_all[c] for c in cyls], [e_all[c] for c in cyls])
    rate = {c: c_all[c] / e_all[c] if e_all[c] else float("inf") for c in cyls}
    low = min(cyls, key=lambda c: rate[c])
    low_by_round = []
    for idx in rounds:
        cr, er = per_cyl(idx, counts), per_cyl(idx, exposures)
        low_by_round.append(min(cyls, key=lambda c: cr[c] / er[c] if er[c] else 1e9))
    dips_one = p < P_ONE and all(x == low for x in low_by_round)

    air_weak = air_none = None
    if air is not None and all(a is not None for a in air):
        diffs_by_round = []
        for idx in rounds:
            a = {c: statistics.mean(air[i] for i in idx if order[i] == c)
                 for c in cyls}
            diffs_by_round.append(
                {c: a[c] - statistics.mean(a[o] for o in cyls if o != c)
                 for c in cyls})
        weak = [c for c in cyls
                if all(d[c] <= -AIR_WEAK_GS for d in diffs_by_round)]
        air_weak = weak[0] if len(weak) == 1 else None
        mean_diff = {c: statistics.mean(d[c] for d in diffs_by_round) for c in cyls}
        air_none = all(abs(x) < AIR_NONE_GS for x in mean_diff.values())

    two = len(cyls) == 2
    res = {"p": p, "low": low, "low_by_round": low_by_round,
           "dips_one": dips_one, "air_weak": air_weak, "air_none": air_none}
    lines = ["dips per 1000 firing strokes: " + ", ".join(
        "%d: %.1f (%d of %d)" % (c, 1000 * rate[c], c_all[c], e_all[c]) for c in cyls),
        "p (smallest rate, all alike) = %.3g; lowest by round: %s"
        % (p, ", ".join(str(x) for x in low_by_round))]
    if dips_one:
        lines.append(f"VERDICT dips: cylinder {low} carries the stumble "
                     f"(p < {P_ONE}, lowest in both rounds)")
    if air_weak is not None:
        lines.append(f"VERDICT air: cylinder {air_weak} is steadily weak "
                     f"(>= {AIR_WEAK_GS} g/s less, both rounds)")
    if not dips_one and air_weak is None:
        if p > P_NONE and air_none:
            res["none"] = True
            lines.append("VERDICT: " + (
                "not cylinder 1 and not cylinder 4 -- 2 or 3 untested"
                if two else
                "not one cylinder: none carries three quarters of the dips "
                "or is 10 % weak; a smaller share is NOT excluded"))
        elif p > P_NONE and air_none is None:
            lines.append("VERDICT: undecided -- the dips are alike, but "
                         "'not one cylinder' needs the air too (no VCDS 003)")
        else:
            lines.append("VERDICT: undecided -- at most one more round "
                         "(plan.md 3.3, rule 4)")
    return lines, res


# --- the dips keep to one slot: the evidence from ordinary idles -------------

#: Two dips closer than this may be one stumble and its recovery.
PAIR_MIN_LAG = 16


def slot_dips(run):
    """Stroke indices of dip events in a four-cylinder run, each stroke judged
    against the same slot either side of it -- so a slot that merely sits a
    little low cannot make its own dips (that would be the period-4 line of
    refuted.md A5 again, which is a mean and not an event)."""
    v = [r for _, r in run]
    out, prev = [], False
    for i in range(len(v)):
        same = [v[j] for j in range(i - 4 * DIP_NEIGHBOURS,
                                    i + 4 * DIP_NEIGHBOURS + 1, 4)
                if j != i and 0 <= j < len(v)]
        if len(same) < 2 * DIP_NEIGHBOURS:
            prev = False
            continue
        low = statistics.median(same) - v[i] >= DIP_RPM
        if low and not prev:
            out.append(i)
        prev = low
    return out


def slot_pairs(gated, min_lag=PAIR_MIN_LAG):
    """[n by lag mod 4] over every pair of dips inside one phase-intact run.

    The runs are bridged ones (`bridged_runs`, minutes long) and the injector
    cuts are left out (5 s margin) -- both since 17/10/2026; before that the
    runs were seconds long and a capture with cuts had to be read by hand.

    Which cylinder a slot is cannot be known, but whether two dips fall on
    the SAME slot can: by chance a quarter of pairs would. One cylinder
    carrying share s0 of the dips (and the others s1..s3) puts sum(s_i^2)
    of the pairs on lag 0 mod 4.
    """
    by_mod = [0, 0, 0, 0]
    cuts = find_cuts(stroke_runs(gated))
    for run in bridged_runs(gated):
        tt = {i: t for t, _, i in run}
        e = [i for i in indexed_dips(run)
             if not any(a - 5 <= tt[i] <= b + 5 for a, b in cuts)]
        for a in range(len(e)):
            for b in range(a + 1, len(e)):
                lag = e[b] - e[a]
                if lag >= min_lag:
                    by_mod[lag % 4] += 1
    return by_mod


#: A held value lasting this many stroke-times or more hid a stroke. Read off
#: the injector cuts of `31` (16/10/2026), where the dead cylinder says how
#: many strokes each hold really was: one stroke held for 1.35-1.64 stroke
#: times, two for 1.83-2.20, nothing between. A stroke runs long because the
#: frames are 10 ms apart and because a dip slows the crank.
HOLD_SPLIT = 1.75


def bridged_runs(gated, t_from=None, t_to=None):
    """Runs of (time, rpm, stroke index) that keep the phase across a held
    value: a hold of r stroke-times counts as one stroke below HOLD_SPLIT
    and as int(r - HOLD_SPLIT) + 2 above it, so the index skips the hidden
    stroke instead of the run breaking. Broken only where the idle gate is.

    Checked against the cuts of `31`: one run of 430 s across all four cuts
    (1, 4, 4, 1) puts cylinder 1 on one slot both times and cylinder 4 two
    slots from it both times, as the firing order 1-3-4-2 must."""
    out, cur, prev, pt, idx = [], [], None, None, 0

    def flush():
        if len(cur) >= MIN_RUN_STROKES:
            mean = sum(r for _, r, _ in cur) / len(cur)
            if IDLE_RPM[0] <= mean <= IDLE_RPM[1]:
                out.append(list(cur))

    for t, q4, throttle, speed in gated:
        if (t_from is not None and t < t_from) or (t_to is not None and t >= t_to):
            continue
        if (speed > idledips.GATE_SPEED_MMH or throttle > idledips.GATE_THROTTLE
                or q4 == 0):
            flush()
            cur, prev, idx = [], None, 0
            continue
        if prev is None:
            prev, pt = q4, t
            continue
        if q4 == prev:
            continue
        r = (t - pt) / (60.0 / (prev / 4.0) / 2.0)
        cur.append((pt, prev / 4.0, idx))
        idx += 1 if r < HOLD_SPLIT else int(r - HOLD_SPLIT) + 2
        prev, pt = q4, t
    flush()
    return out


def indexed_dips(run):
    """Stroke indices of dips in a bridged run -- slot_dips() over an index
    that may skip: each stroke against the same slot either side of it."""
    v = {i: r for _, r, i in run}
    out, prev = [], False
    for i in sorted(v):
        same = [v[j] for j in range(i - 4 * DIP_NEIGHBOURS,
                                    i + 4 * DIP_NEIGHBOURS + 1, 4)
                if j != i and j in v]
        if len(same) < 2 * DIP_NEIGHBOURS - 2:
            prev = False
            continue
        low = statistics.median(same) - v[i] >= DIP_RPM
        if low and not prev:
            out.append(i)
        prev = low
    return out


def slot_runs(gated, min_lag=PAIR_MIN_LAG, skip_cuts=True):
    """[[slot of each dip, mod 4], ...] for every bridged run holding two or
    more dips at least `min_lag` strokes apart. Dips within 5 s of an
    injector cut (`find_cuts`) are left out when skip_cuts."""
    cuts = find_cuts(stroke_runs(gated)) if skip_cuts else []
    out = []
    for run in bridged_runs(gated):
        tt = {i: t for t, _, i in run}
        kept = []
        for i in indexed_dips(run):
            if any(a - 5 <= tt[i] <= b + 5 for a, b in cuts):
                continue
            if not kept or i - kept[-1] >= min_lag:
                kept.append(i)
        if len(kept) >= 2:
            out.append([i % 4 for i in kept])
    return out


FIRING_ORDER = (1, 3, 4, 2)


def named_idle_dips(gated, order):
    """Dips named by cylinder, in a capture with injector cuts in it.

    Within one bridged run every cut names its slot: the dead cylinder is
    the low one. The firing order then names the other three. Every dip in
    the same run outside the cuts (5 s margin) gets its cylinder. Returns
    {cylinder: dips}, the strokes examined, and how many cuts agreed with
    the firing order; a run whose cuts disagree is skipped."""
    cuts = find_cuts(stroke_runs(gated))
    if len(cuts) != len(order):
        raise SystemExit("found %d cuts, the order names %d" % (len(cuts), len(order)))
    counts = {c: 0 for c in FIRING_ORDER}
    strokes = 0
    agreed = 0
    for run in bridged_runs(gated):
        slot_of = {}
        for (a, b), cyl in zip(cuts, order):
            w = [(i, r) for t, r, i in run if a + 5 <= t < b - 5]
            if len(w) < 100:
                continue
            med = [statistics.median([r for i, r in w if i % 4 == k])
                   for k in range(4)]
            dead = min(range(4), key=lambda k: med[k])
            # slot of cylinder 1 implied by this cut
            slot_of.setdefault(cyl, []).append(dead)
        implied = set()
        for cyl, slots in slot_of.items():
            for d in slots:
                implied.add((d - FIRING_ORDER.index(cyl)) % 4)
        if len(implied) != 1:
            continue
        agreed += sum(len(v) for v in slot_of.values())
        base = implied.pop()
        tt = {i: t for t, _, i in run}
        for i in indexed_dips(run):
            if any(a - 5 <= tt[i] <= b + 5 for a, b in cuts):
                continue
            counts[FIRING_ORDER[(i - base) % 4]] += 1
        strokes += sum(1 for t, _, _ in run
                       if not any(a - 5 <= t <= b + 5 for a, b in cuts))
    return counts, strokes, agreed


def shares_loglik(shares, runs):
    """Log-likelihood of the runs under per-slot shares, the run's phase
    unknown (each of the four rotations equally likely)."""
    total = 0.0
    for r in runs:
        total += math.log(sum(math.prod(shares[(x + k) % 4] for x in r)
                              for k in range(4)) / 4)
    return total


def slot_shares(runs, iters=500):
    """The per-slot shares that best explain the runs, by EM over the
    unknown phase of each run; rotated so the largest comes first, then in
    firing order. Pairs alone fix only how the dips repeat (their
    autocorrelation) and cannot tell one cylinder carrying half from two
    neighbours in the firing order carrying 40 % each; a run with three or
    more dips carries their order, and that is what this reads. The runs
    are bridged ones (`bridged_runs`), minutes long, so most carry many."""
    p = [0.4, 0.3, 0.1, 0.2]
    for _ in range(iters):
        acc = [1e-9] * 4
        for r in runs:
            w = [math.prod(p[(x + k) % 4] for x in r) for k in range(4)]
            sw = sum(w)
            for k in range(4):
                for x in r:
                    acc[(x + k) % 4] += w[k] / sw
        n = sum(acc)
        p = [a / n for a in acc]
    k = p.index(max(p))
    return p[k:] + p[:k]


#: Named readings for --shares, as shares in firing order from the leader.
SHARE_MODELS = (
    ("all four alike", (0.25, 0.25, 0.25, 0.25)),
    ("one cylinder, the rest alike", (0.50, 1 / 6, 1 / 6, 1 / 6)),
    ("one cylinder, partner 0", (0.50, 0.25, 0.001, 0.25)),
    ("two neighbours alike", (0.42, 0.42, 0.03, 0.13)),
    ("two neighbours, two others", (0.35, 0.15, 0.15, 0.35)),
    ("the two on one coil output", (0.35, 0.15, 0.35, 0.15)),
)


def binom_upper(k, n, p):
    """P(X >= k) for X ~ Binomial(n, p), in log space so a large n works."""
    def term(j):
        return math.exp(math.lgamma(n + 1) - math.lgamma(j + 1)
                        - math.lgamma(n - j + 1) + j * math.log(p)
                        + (n - j) * math.log(1 - p))
    return min(1.0, sum(term(j) for j in range(k, n + 1)))


def chi2_3_upper(x):
    """P(chi-squared with 3 degrees of freedom >= x)."""
    if x <= 0:
        return 1.0
    return math.erfc(math.sqrt(x / 2)) + math.sqrt(2 * x / math.pi) * math.exp(-x / 2)


def shares_report(runs):
    """(best shares, p against all four alike, top two together)."""
    best = slot_shares(runs)
    lr = 2 * (shares_loglik(best, runs) - shares_loglik((0.25,) * 4, runs))
    top2 = best[0] + max(best[1], best[3])
    return best, chi2_3_upper(lr), top2


def read_session(capture, order, cuts_arg=None, vcds_path=None):
    """One capture: its cuts, dips by cut and by name, and the air."""
    rpm, _, _, gated = idledips.series(capture)
    runs = stroke_runs(gated)
    if cuts_arg:
        cuts = [tuple(float(x) for x in s.split("-")) for s in cuts_arg.split(",")]
    else:
        cuts = find_cuts(runs)
    if len(cuts) != len(order):
        print("%s: found %d cuts, the order names %d -- stopping rather than "
              "guessing which is which:" % (capture, len(cuts), len(order)))
        for a, b in cuts:
            print("  %8.1f-%8.1f s" % (a, b))
        print("check with --scan, then give them with --cuts")
        return None
    print("== %s" % capture)
    print("%-4s %-19s %6s %8s %8s" % ("cut", "capture s", "dips", "strokes",
                                       "grade"))
    counts, exposures = [], []
    for c, (a, b) in zip(order, cuts):
        ev, ex = firing_dips(runs, a + CUT_SETTLE_S, b)
        counts.append(ev)
        exposures.append(ex)
        grade = idledips.roughness(gated, a, b)[0]
        print("%-4d %8.1f-%8.1f %6d %8d %8.2f" % (c, a, b, ev, ex, grade))
    named = [named_dips(runs, a + CUT_SETTLE_S, b, c)
             for c, (a, b) in zip(order, cuts)]
    air = None
    if vcds_path:
        vc = read_vcds(vcds_path)
        got = air_by_cut(vc, rpm, cuts)
        if got:
            air_ign, off = got
            air = [x for x, _ in air_ign]
            print("VCDS aligned at %+.1f s; 003 over the last %d s of each cut:"
                  % (off, AIR_TAIL_S))
            for c, (x, y) in zip(order, air_ign):
                print("  %d: air %s g/s, ignition %s deg" % (
                    c, "-" if x is None else "%.2f" % x,
                    "-" if y is None else "%.1f" % y))
            mis = misfires_by_cut(vc, rpm, cuts, off)
            if mis:
                print("014 rises a minute per cut (question 11): " + ", ".join(
                    "%d: %.1f" % (c, m) for c, m in zip(order, mis)))
    return counts, exposures, named, air


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("captures", nargs="+",
                    help="one or more sessions, pooled in the order given")
    ap.add_argument("--order", default="1,4,4,1",
                    help="the cut order of EVERY session")
    ap.add_argument("--vcds", nargs="*", default=[],
                    help="VCDS CSVs with 003 (and 014), one per capture")
    ap.add_argument("--cuts", help="intervals by hand, one capture only")
    ap.add_argument("--pairs", action="store_true",
                    help="ordinary idles: do dips keep to one slot? (no cuts)")
    ap.add_argument("--shares", action="store_true",
                    help="ordinary idles: one cylinder or two? (cuts left out)")
    ap.add_argument("--name", action="store_true",
                    help="a capture with cuts: name the cylinder of every "
                         "dip outside them, in the same run")
    ap.add_argument("--scan", action="store_true",
                    help="print every run's slot deficit and stop")
    args = ap.parse_args(argv)

    if args.pairs:
        total = [0, 0, 0, 0]
        for cap in args.captures:
            m = slot_pairs(idledips.series(cap)[3])
            total = [x + y for x, y in zip(total, m)]
            n = sum(m)
            print("%-30s pairs %4d  same slot %3d (%s)  lag mod 4: %s" % (
                cap.split("/")[-1], n, m[0],
                "%.0f%%" % (100.0 * m[0] / n) if n else "-",
                " ".join("%d:%d" % (k, x) for k, x in enumerate(m))))
        n = sum(total)
        if n:
            print("pooled: %d of %d on the same slot (%.0f%%, chance 25%%). "
                  "No p: pairs inside one run are not independent -- "
                  "--shares is the test" % (total[0], n, 100.0 * total[0] / n))
        return 0

    if args.shares:
        runs = []
        for cap in args.captures:
            got = slot_runs(idledips.series(cap)[3])
            runs += got
            if len(args.captures) > 1 and got:
                b, p, top2 = shares_report(got)
                print("%-30s runs %3d dips %4d  shares %s  top two %.0f%%  "
                      "p(all alike) %.2g" % (cap.split("/")[-1], len(got),
                                             sum(map(len, got)),
                                             " ".join("%.2f" % x for x in b),
                                             100 * top2, p))
        if not runs:
            print("no run with two dips")
            return 0
        b, p, top2 = shares_report(runs)
        print("pooled: %d dips; top two together %.0f%%; p against all four "
              "alike %.2g" % (sum(map(len, runs)), 100 * top2, p))
        best = slot_shares(runs)
        lb = shares_loglik(best, runs)
        print("%d runs with two or more dips, %d with three or more" % (
            len(runs), sum(len(r) >= 3 for r in runs)))
        print("best shares, leader first, then in firing order: %s  (logL %.1f)"
              % (" ".join("%.2f" % x for x in best), lb))
        for name, m in SHARE_MODELS:
            print("  %-30s logL %8.1f  (%5.1f below the best)" % (
                name, shares_loglik(m, runs), lb - shares_loglik(m, runs)))
        return 0

    if args.name:
        order = [int(x) for x in args.order.split(",")]
        for cap in args.captures:
            counts, strokes, agreed = named_idle_dips(idledips.series(cap)[3], order)
            n = sum(counts.values())
            print("%s: %d cuts agreed on the phase; %d dips outside the cuts "
                  "over %d strokes" % (cap.split("/")[-1], agreed, n, strokes))
            for c in FIRING_ORDER:
                print("  cylinder %d: %3d%s" % (c, counts[c], "  (%.0f%%)" %
                                                (100.0 * counts[c] / n) if n else ""))
        return 0

    if args.scan:
        for cap in args.captures:
            for run in stroke_runs(idledips.series(cap)[3]):
                dead, d = slot_deficit(run)
                print("%8.1f-%8.1f s  %4d strokes  slot %d  %5.1f rpm%s" % (
                    run[0][0], run[-1][0], len(run), dead, d,
                    "  CUT" if d >= CUT_DEFICIT_RPM else ""))
        return 0

    order = [int(x) for x in args.order.split(",")]
    if len(order) % 2:
        raise SystemExit("--order must be two rounds of equal length")
    if args.cuts and len(args.captures) != 1:
        raise SystemExit("--cuts takes one capture at a time")
    if args.vcds and len(args.vcds) != len(args.captures):
        raise SystemExit("--vcds takes one log per capture")

    all_order, counts, exposures, named, air = [], [], [], [], []
    air_ok = True                   # the air is used only if every session has it
    for i, cap in enumerate(args.captures):
        got = read_session(cap, order, args.cuts,
                           args.vcds[i] if args.vcds else None)
        if got is None:
            return 1
        c, e, n, a = got
        all_order += order
        counts += c
        exposures += e
        named += n
        if a is None:
            air_ok = False
        else:
            air += a

    print("== pooled over %d session(s)" % len(args.captures))
    for line in named_verdict(all_order, named)[0]:
        print(line)
    print("-- the cuts compared with each other (secondary):")
    for line in verdict(all_order, counts, exposures,
                        air if air_ok else None)[0]:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
