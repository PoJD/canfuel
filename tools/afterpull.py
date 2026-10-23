#!/usr/bin/env python3
"""The warm idle in the minutes after full-load pulls -- does it start calm or rough?

Written on 23/10/2026 for the owner's observation on the first BG 44K tank
(docs/engine-health/open.md S1, *After full-load pulls*): straight after
driving the engine hard, `IdleHealth` at a stop reads far lower than usual and
climbs back over the next minutes. The question was whether the captures show
that shape before the cleaner, and kept as a tool for the reason idledips.py
gives for itself: an ad-hoc script that is not kept produces numbers nobody
can check.

What it does, per capture:

* finds the **pulls**: stretches where engine speed is above `PULL_RPM` and
  indicated torque (0x280 b7) above `PULL_B7` -- full load, the plateau of
  docs/firmware/can-decoding.md question 8 being 185-206;
* finds every **warm standing idle** with the gate, settle rule and dead band
  of `idledips.roughness()`, so that the grade is the one the display shows;
* for each idle that began within `LOOK_S` of a pull, prints the pulls in that
  window and the grade in bins of time since the idle settled.

The grade is `IdleHealth`'s scale, the mean dead-banded step x 50, as
everywhere in docs/engine-health. A bin with fewer than `MIN_STEPS` steps is
left empty rather than read: a 15 s bin of a warm idle holds several hundred.
Injector cuts (`cutscan.find_cuts`) are left out, as in dipcontext.py; a
dead cylinder would read as the roughest idle on record.

``--all`` prints every warm idle, pulls before it or not, which is the
like-with-like control.

The constants are the ones the reading in open.md was made with. Change them
and the numbers there no longer reproduce.
"""

from __future__ import annotations

import argparse
import os
import sys

import canlog
import cutscan
import idledips

#: A pull: engine speed above this...
PULL_RPM = 4500.0
#: ...with indicated torque (0x280 b7) above this. Full load reads 185-206.
PULL_B7 = 150
#: Samples further apart than this do not add time (a gap in the capture).
MAX_DT_S = 0.5
#: Two stretches closer than this are one pull.
PULL_MERGE_S = 1.0
#: How far before an idle a pull is looked for.
LOOK_S = 300.0
#: Warm: oil at least this at the end of the idle (0x420, raw - 60).
OIL_MIN_C = 85.0
#: An idle shorter than this, once settled, is not printed.
MIN_IDLE_S = 30.0
#: Bins of time since the idle settled, seconds.
BINS = ((0, 15), (15, 30), (30, 60), (60, 120), (120, 180), (180, None))
#: A bin is read only with at least this many steps.
MIN_STEPS = 100
#: Padding around an injector cut, as dipcontext.CUT_PAD_S.
CUT_PAD_S = 5.0


def samples(path):
    """(t, rpm_q4, throttle, speed_mmh, b7, oil_c) per 0x280 frame."""
    frames = canlog.parse_file(path)
    if not frames or frames[0].ts_ms is None:
        raise SystemExit(f"{path}: no adapter timestamps; only _z1 logs.")
    t0 = frames[0].ts_ms
    speed_mmh, oil, out = 0, None, []
    for f in frames:
        t = (f.ts_ms - t0) / 1000.0
        if f.can_id == 0x1A0 and len(f.data) >= 4:
            # docs/firmware/can-decoding.md trap 1: the gate is not an equality.
            if (f.data[1] & 0x40) and not (f.data[1] & 0x03):
                speed_mmh = (f.data[2] | (f.data[3] << 8)) * 5
        elif f.can_id == 0x420 and len(f.data) >= 4 and f.data[3] != 0xFF:
            oil = canlog.oil_c(f.data[3])
        elif f.can_id == 0x280 and len(f.data) >= 8:
            out.append((t, f.data[2] | (f.data[3] << 8), f.data[5], speed_mmh,
                        f.data[7], oil))
    return out


def pulls(smp, rpm=PULL_RPM, b7=PULL_B7):
    """[start, end, seconds above, integral of (rpm - PULL_RPM) dt] per pull."""
    out, cur = [], None
    for k in range(len(smp) - 1):
        t, rq4, _, _, torque, _ = smp[k]
        dt = smp[k + 1][0] - t
        r = rq4 / 4.0
        if r > rpm and torque > b7 and dt < MAX_DT_S:
            if cur is None or t - cur[1] > PULL_MERGE_S:
                cur = [t, t, 0.0, 0.0]
                out.append(cur)
            cur[1] = t
            cur[2] += dt
            cur[3] += (r - rpm) * dt
    return out


def idle_runs(smp, cuts=()):
    """Every standing idle, graded the way idledips.roughness() grades.

    Each run is a dict: ``t_idle`` when the gate opened, ``t0``/``t1`` the
    first and last settled sample, ``oil`` at the end, ``b7`` the median
    indicated torque while settled (the load state), and ``steps`` as
    (seconds since t0, dead-banded step in 0.25 rpm).
    """
    dead = idledips.ROUGH_DEADBAND_RPM * 4
    trip = idledips.TRIP_RPM * 4
    out, cur = [], None
    base = since = prev = None
    b7s = []

    def close():
        if cur is not None and "t0" in cur:
            b7s.sort()
            cur["b7"] = b7s[len(b7s) // 2]
            out.append(cur)

    for t, r, thr, spd, torque, oil in smp:
        if (spd > idledips.GATE_SPEED_MMH or thr > idledips.GATE_THROTTLE
                or r == 0):
            close()
            cur, base, since, prev, b7s = None, None, None, None, []
            continue
        if since is None:
            since = t
            base = r << idledips.EWMA_SHIFT
            cur = {"t_idle": t, "steps": []}
        baseline = base >> idledips.EWMA_SHIFT
        settled = (t - since) >= idledips.SETTLE_S
        if not settled and baseline - r >= trip:
            since = t
        if settled:
            cur.setdefault("t0", t)
            cur["t1"], cur["oil"] = t, oil
            b7s.append(torque)
            in_cut = any(a <= t < b for a, b in cuts)
            if prev is not None and r != prev and not in_cut:
                cur["steps"].append((t - cur["t0"], max(0, abs(r - prev) - dead)))
        if prev is None or r != prev:
            prev = r
        base += r - baseline
    close()
    return out


def grade(steps, a, b=None):
    """IdleHealth over [a, b) seconds since settling, or None if too few steps."""
    v = [s for t, s in steps if t >= a and (b is None or t < b)]
    if len(v) < MIN_STEPS:
        return None
    return sum(v) / len(v) / 4.0 * 50.0


def cut_spans(smp):
    gated = [(t, r, thr, spd) for t, r, thr, spd, _, _ in smp]
    return [(a - CUT_PAD_S, b + CUT_PAD_S)
            for a, b in cutscan.find_cuts(cutscan.stroke_runs(gated))]


def report(path, look=LOOK_S, show_all=False, out=sys.stdout):
    smp = samples(path)
    pp = pulls(smp)
    name = os.path.basename(path)[:22]
    rows = 0
    for run in idle_runs(smp, cut_spans(smp)):
        if run["t1"] - run["t0"] < MIN_IDLE_S:
            continue
        if run["oil"] is None or run["oil"] < OIL_MIN_C:
            continue
        before = [q for q in pp if run["t_idle"] - look <= q[1] < run["t_idle"]]
        if not before and not show_all:
            continue
        g = [grade(run["steps"], a, b) for a, b in BINS]
        last = ("%5.0fs" % (run["t_idle"] - before[-1][1])) if before else "     -"
        out.write("%-22s %6.0f %4.0f %4.0f | %5d %6.1f %7.1f %s | %s | %3d\n" % (
            name, run["t0"], run["t1"] - run["t0"], run["oil"], len(before),
            sum(q[2] for q in before), sum(q[3] for q in before) / 1000.0, last,
            " ".join("%5s" % ("-" if x is None else "%.0f" % x) for x in g),
            run["b7"]))
        rows += 1
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+", help="_z1 captures to read")
    ap.add_argument("--look", type=float, default=LOOK_S,
                    help="seconds before an idle to look for pulls (%(default)s)")
    ap.add_argument("--all", action="store_true",
                    help="every warm idle, pulls before it or not")
    args = ap.parse_args(argv)
    print("%-22s %6s %4s %4s | %5s %6s %7s %6s | %s | %3s" % (
        "log", "idle@", "dur", "oil", "pulls", "s>4500", "krpm*s", "last",
        " ".join("%5s" % ("%d-%s" % (a, b if b else "")) for a, b in BINS), "b7"))
    for path in args.files:
        report(path, args.look, args.all)
    return 0


if __name__ == "__main__":
    sys.exit(main())
