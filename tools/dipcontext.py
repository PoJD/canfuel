#!/usr/bin/env python3
"""What the engine was doing just before an idle dip -- the context of S1.

`idledips.py` counts the dips of engine speed at idle and `cutscan.py` asks
which cylinder they sit on. This asks a third question, which neither can:
**is a dip more likely in some state the ECU has put the engine in?** It
was written on 10/10/2026 for the owner's request to go through every idle
again (docs/engine-health/open.md S1, *What comes before a dip*), and kept
as a tool for the reason idledips.py gives for itself: an ad-hoc script that
is not kept produces numbers nobody can check.

Three readings, all over a warm standing idle:

``--trigger``
    The event-triggered average. For every dip, each channel is read at
    fixed offsets around it, relative to its own value one second before;
    the same is done at random idle moments as the control. Channels:
    engine speed averaged over one engine cycle (so that the period-4
    structure of 0x280 averages out), injection time (0x288 b6,
    docs/firmware/can-decoding.md question 3) and indicated torque
    (0x280 b7). What it can show is a change *before* the dip that the
    control does not have.

``--strata``
    The same question without averaging over events, which a dip detector
    could bias: at every moment of idle, did a dip start within the next
    `HORIZON_S`, split by how indicated torque (or injection time) moved
    over the half second before, and by how engine speed moved, so that a
    torque change is never confused with the speed change the idle
    governor answers.

``--runs``
    How the next dip follows one: after a whole number of engine cycles
    (720 deg -- the same cylinder again) or after a whole number plus a
    half (360 deg -- its partner in the firing order). Equal windows, so
    chance puts as many in one as in the other.

**The injector cuts are left out** (`cutscan.find_cuts`, padded by
`CUT_PAD_S`): a dead cylinder dips every cycle and would make every reading
here about the cut. The first version of this analysis did not, and read
the cuts of `31` as runs of misfires on one cylinder.

The constants are the ones the reading in open.md was made with. Change
them and the numbers there no longer reproduce.
"""

from __future__ import annotations

import argparse
import bisect
import os
import random
import statistics
import sys

import canlog
import cutscan
import idledips

#: Warm standing idle: oil at least this, 0x420 (S1's middle and hot bands).
OIL_MIN_C = 55.0
#: Engine speed accepted as idle.
IDLE_RPM = (650.0, 950.0)
#: Seconds kept clear either side of a found injector cut.
CUT_PAD_S = 5.0
#: A dip is idledips.dips() at this depth -- S1's threshold.
DIP_RPM = 20
#: One engine cycle at idle is ~0.15 s; the speed channel is averaged over
#: one cycle centred on the moment read.
CYCLE_S = 0.152
#: Offsets read around each dip, seconds.
OFFSETS = tuple(round(i * 0.04, 2) for i in range(-20, 11))
#: Control moments per dip.
CONTROL_PER_DIP = 5
CONTROL_SEED = 1
#: --strata: the look-ahead, the step between moments, and the bands.
HORIZON_S = 0.3
STEP_S = 0.05
TORQUE_BAND = 0.5   # counts of b7 or b6 between the two windows
RPM_BAND = 3.0      # rpm, cycle-averaged, over 0.4 s
#: --runs: how close to a whole (or half) number of cycles counts.
RUN_TOL = 0.12
RUN_MAX_CYCLES = 6.5


class Series:
    """A step function of time, read by bisection."""

    def __init__(self, pairs):
        self.t = [t for t, _ in pairs]
        self.v = [v for _, v in pairs]

    def at(self, t):
        i = bisect.bisect_right(self.t, t) - 1
        return self.v[i] if i >= 0 else None

    def mean(self, a, b):
        lo = bisect.bisect_left(self.t, a)
        hi = bisect.bisect_right(self.t, b)
        return sum(self.v[lo:hi]) / (hi - lo) if hi > lo else None


class Capture:
    """The channels of one capture, and which moments are warm idle."""

    def __init__(self, path):
        frames = canlog.parse_file(path)
        if not frames or frames[0].ts_ms is None:
            raise SystemExit(f"{path}: no adapter timestamps (_z1 logs only)")
        t0 = frames[0].ts_ms
        rpm, b5, b7, inj, oil, spd = [], [], [], [], [], []
        speed = 0
        for f in frames:
            t = (f.ts_ms - t0) / 1000.0
            d = f.data
            if f.can_id == 0x1A0 and len(d) >= 4:
                if (d[1] & 0x40) and not (d[1] & 0x03):
                    speed = (d[2] | (d[3] << 8)) * 5
                spd.append((t, speed))
            elif f.can_id == 0x280 and len(d) >= 8:
                rpm.append((t, (d[2] | (d[3] << 8)) / 4.0))
                b5.append((t, d[5]))
                b7.append((t, d[7]))
            elif f.can_id == 0x288 and len(d) >= 7:
                inj.append((t, d[6]))
            elif f.can_id == 0x420 and len(d) >= 4:
                oil.append((t, d[3] * 0.75 - 48.0))
        self.path = path
        self.rpm_pairs = rpm
        self.rpm = Series(rpm)
        self.b5, self.b7, self.inj = Series(b5), Series(b7), Series(inj)
        self.oil, self.spd = Series(oil), Series(spd)
        _, _, _, gated = idledips.series(path)
        self.cuts = [(a - CUT_PAD_S, b + CUT_PAD_S)
                     for a, b in cutscan.find_cuts(cutscan.stroke_runs(gated))]

    def idle(self, t):
        if any(a <= t <= b for a, b in self.cuts):
            return False
        r, o = self.rpm.at(t), self.oil.at(t)
        th, sp = self.b5.at(t), self.spd.at(t)
        return (r is not None and IDLE_RPM[0] <= r <= IDLE_RPM[1]
                and o is not None and o >= OIL_MIN_C
                and th is not None and th <= idledips.GATE_THROTTLE
                and (sp or 0) <= idledips.GATE_SPEED_MMH)

    def idle_around(self, t, before=1.0, after=1.0):
        return all(self.idle(t + o) for o in (-before, -before / 2, 0.0,
                                              after / 2, after))

    def speed_cycle(self, t):
        return self.rpm.mean(t - CYCLE_S / 2, t + CYCLE_S / 2)

    def dips(self):
        """Dip times whose second either side is warm idle."""
        ev, _ = idledips.dips(self.rpm_pairs, DIP_RPM)
        return [t for t, _ in ev if self.idle_around(t)]

    def controls(self, n):
        pool = [t for t, _ in self.rpm_pairs[::5] if self.idle_around(t)]
        if not pool:
            return []
        rnd = random.Random(CONTROL_SEED)
        return [rnd.choice(pool) for _ in range(n)]


CHANNELS = ("speed", "inj", "b7")


def _read(cap, ch, t):
    if ch == "speed":
        return cap.speed_cycle(t)
    return (cap.inj if ch == "inj" else cap.b7).at(t)


def trigger(caps):
    """{channel: [(offset, mean, se, control mean)]}, and the dip count."""
    acc = {c: [[] for _ in OFFSETS] for c in CHANNELS}
    ctl = {c: [[] for _ in OFFSETS] for c in CHANNELS}
    n = 0
    for cap in caps:
        ev = cap.dips()
        n += len(ev)
        for times, store in ((ev, acc), (cap.controls(CONTROL_PER_DIP * len(ev)), ctl)):
            for t in times:
                for c in CHANNELS:
                    base = _read(cap, c, t - 1.0)
                    vals = [_read(cap, c, t + o) for o in OFFSETS]
                    if base is None or None in vals:
                        continue
                    for i, v in enumerate(vals):
                        store[c][i].append(v - base)
    out = {}
    for c in CHANNELS:
        rows = []
        for i, o in enumerate(OFFSETS):
            a, b = acc[c][i], ctl[c][i]
            if len(a) < 2 or not b:
                continue
            se = statistics.pstdev(a) / len(a) ** 0.5
            rows.append((o, statistics.mean(a), se, statistics.mean(b)))
        out[c] = rows
    return out, n


def strata(caps, channel="b7"):
    """{(torque move, speed move): [dips started, moments]}."""
    tab = {}
    for cap in caps:
        ev = sorted(cap.dips())
        src = cap.b7 if channel == "b7" else cap.inj
        t, end = cap.rpm.t[0] + 1.0, cap.rpm.t[-1] - 1.0
        while t < end:
            if cap.idle_around(t, before=0.6, after=0.4):
                now = src.mean(t - 0.12, t)
                then = src.mean(t - 0.52, t - 0.40)
                s_now = cap.speed_cycle(t)
                s_then = cap.speed_cycle(t - 0.4)
                if None not in (now, then, s_now, s_then):
                    d, ds = now - then, s_now - s_then
                    k1 = "fell" if d <= -TORQUE_BAND else ("rose" if d >= TORQUE_BAND else "flat")
                    k2 = "fell" if ds <= -RPM_BAND else ("rose" if ds >= RPM_BAND else "flat")
                    j = bisect.bisect_right(ev, t)
                    hit = j < len(ev) and ev[j] <= t + HORIZON_S
                    cell = tab.setdefault((k1, k2), [0, 0])
                    cell[0] += hit
                    cell[1] += 1
            t += STEP_S
    return tab


def runs(cap):
    """(dips, next at k*720 deg, next at k*720+360 deg)."""
    ev = cap.dips()
    whole = half = 0
    for i, a in enumerate(ev):
        r = cap.rpm.at(a)
        if not r:
            continue
        cyc = 120.0 / r
        nxt = [b for b in ev[i + 1:i + 8] if b - a < RUN_MAX_CYCLES * cyc]
        if not nxt:
            continue
        x = (nxt[0] - a) / cyc
        k = round(x)
        if k >= 1 and abs(x - k) < RUN_TOL:
            whole += 1
        elif abs(x - k - 0.5) < RUN_TOL or abs(x - k + 0.5) < RUN_TOL:
            half += 1
    return len(ev), whole, half


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--trigger", action="store_true")
    g.add_argument("--strata", action="store_true")
    g.add_argument("--runs", action="store_true")
    ap.add_argument("--channel", choices=("b7", "inj"), default="b7",
                    help="--strata: indicated torque or injection time")
    args = ap.parse_args(argv)
    caps = [Capture(p) for p in args.files]
    if args.trigger:
        out, n = trigger(caps)
        print(f"{n} dips, warm standing idle, cuts left out")
        for c in CHANNELS:
            print(f"{c}: offset  mean  ±se  control")
            for o, m, se, mc in out[c]:
                print(f"  {o:+.2f}  {m:+7.3f} ±{se:.3f}  {mc:+7.3f}")
    elif args.strata:
        tab = strata(caps, args.channel)
        print(f"{args.channel} over 0.5 s  speed over 0.4 s  moments  dips  rate")
        for k in sorted(tab):
            hit, n = tab[k]
            print(f"  {k[0]:5}  {k[1]:5}  {n:7d} {hit:5d} {100.0 * hit / n:5.2f} %")
    else:
        tw = th = tn = 0
        for cap in caps:
            n, w, h = runs(cap)
            tn, tw, th = tn + n, tw + w, th + h
            print(f"  {os.path.basename(cap.path)[:28]:28} {n:5d} dips  "
                  f"next at k*720: {w:4d}  at k*720+360: {h:4d}")
        print(f"  {'all':28} {tn:5d} dips  next at k*720: {tw:4d}  at k*720+360: {th:4d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
