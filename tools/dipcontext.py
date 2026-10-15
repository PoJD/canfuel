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

``--vcds LOG``
    VCDS is far too slow to see a dip, but over hundreds of dips its
    samples land just before some of them and just after others. With
    one capture and the VCDS log taken beside it, every sample of 003,
    033 or 055 is put on the capture's clock (`cutscan.align`, on
    engine speed) and sorted: within `VCDS_NEAR_S` before a dip, within
    it after one, or quiet (no dip within `VCDS_QUIET_S`). The means of
    each field in the three classes are printed.

``--profile [--svg OUT]``
    One dip as the bus sees it, for the owner to look at: engine speed
    *not* averaged over a cycle, so the fall and the recovery keep their
    shape, each dip aligned on its own lowest 0x280 value, with injection
    time and indicated torque beside it, relative to `PROFILE_BASE_S`
    before. ``--svg`` draws the same three rows as
    docs/engine-health/dip-profile.svg (S1, *One dip, read stroke by
    stroke*).

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
#: Decided as 55 C on the old scale; the same bytes on today's (canlog.oil_c).
OIL_MIN_C = canlog.oil_from_old_scale(55.0)
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
#: --vcds: a sample "before" or "after" a dip if one lies this close.
VCDS_NEAR_S = 0.6
#: --vcds: a sample is "quiet" if no dip lies within this.
VCDS_QUIET_S = 2.0
#: --vcds: the fields read, by group: (index after the time column, name).
#: 033 carries no engine speed, so its log must hold a group that does
#: (003, 014 or 055) for the alignment.
VCDS_FIELDS = {
    "001": ((2, "lambda correction %"),),
    "003": ((1, "air g/s"), (2, "throttle deg"), (3, "advance deg BTDC")),
    "033": ((0, "lambda correction %"), (1, "probe V")),
    "055": ((1, "idle regulator g/s"), (2, "learned idle air g/s")),
}
#: --profile: offsets, the baseline, and how far either side of a found
#: dip its lowest value is looked for.
PROFILE_OFFSETS = tuple(round(i * 0.02, 2) for i in range(-40, 21))
PROFILE_BASE_S = 1.2
PROFILE_SEEK_S = 0.1
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
            elif f.can_id == 0x420 and len(d) >= 4 and d[3] != 0xFF:
                oil.append((t, canlog.oil_c(d[3])))
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


def vcds_near(cap, log_path):
    """{(group, field, class): [values]} for one capture and its VCDS log."""
    vc = cutscan.read_vcds(log_path)
    g0 = next((g for g in ("014", "003", "055", "001") if g in vc), None)
    if g0 is None:
        raise SystemExit(f"{log_path}: no group with engine speed to align on")
    vr = []
    for t, x in vc[g0]:
        try:
            vr.append((t, float(x[0])))
        except ValueError:
            pass
    off = cutscan.align(vr, cap.rpm_pairs)
    dips = sorted(cap.dips())
    out = {}
    for g, fields in VCDS_FIELDS.items():
        for t, x in vc.get(g, ()):
            tc = t + off
            if not cap.idle_around(tc, VCDS_NEAR_S, VCDS_NEAR_S):
                continue
            j = bisect.bisect_left(dips, tc - VCDS_QUIET_S)
            near = [d for d in dips[j:j + 32] if abs(d - tc) <= VCDS_QUIET_S]
            if any(0 < d - tc <= VCDS_NEAR_S for d in near):
                cls = "before a dip"
            elif any(0 <= tc - d <= VCDS_NEAR_S for d in near):
                cls = "after a dip"
            elif not near:
                cls = "quiet"
            else:
                continue
            for k, name in fields:
                try:
                    v = float(x[k].replace(",", "."))
                except (ValueError, IndexError):
                    continue
                out.setdefault((g, name, cls), []).append(v)
    return out


def profile(caps):
    """[(offset, speed, inj, b7)] means over every dip, and the dip count.

    Speed is the raw 0x280 value, aligned on each dip's own minimum.
    """
    acc = [[[], [], []] for _ in PROFILE_OFFSETS]
    n = 0
    for cap in caps:
        t, v = cap.rpm.t, cap.rpm.v
        for d in cap.dips():
            i0 = bisect.bisect_left(t, d - PROFILE_SEEK_S)
            i1 = bisect.bisect_right(t, d + PROFILE_SEEK_S)
            if i1 <= i0:
                continue
            tm = t[min(range(i0, i1), key=lambda j: v[j])]
            series = (cap.rpm, cap.inj, cap.b7)
            base = [s.at(tm - PROFILE_BASE_S) for s in series]
            vals = [[s.at(tm + o) for s in series] for o in PROFILE_OFFSETS]
            if None in base or any(None in x for x in vals):
                continue
            n += 1
            for slot, x in zip(acc, vals):
                for k in range(3):
                    slot[k].append(x[k] - base[k])
    rows = [(o,) + tuple(statistics.mean(a) for a in slot)
            for o, slot in zip(PROFILE_OFFSETS, acc) if slot[0]]
    return rows, n


def profile_svg(rows, n, names):
    """The three rows of profile() as one SVG, light background, no script."""
    panels = (("Engine speed, rpm (0x280)", 1, (-30.0, 10.0), (-20, -10, 0, 10)),
              ("Injection time, counts of ~0.08 ms (0x288 b6)", 2,
               (-0.6, 0.6), (-0.5, 0, 0.5)),
              ("Indicated torque, counts of 1.06 Nm (0x280 b7)", 3,
               (-0.6, 0.6), (-0.5, 0, 0.5)))
    w, h, left, right, top, ph, gap = 760, 690, 70, 34, 90, 150, 40
    lo_o, hi_o = rows[0][0], rows[-1][0]

    def x(o):
        return left + (o - lo_o) / (hi_o - lo_o) * (w - left - right)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}" font-family="Helvetica,Arial,sans-serif">',
           f'<rect width="{w}" height="{h}" fill="#fcfcfb"/>',
           f'<text x="{left}" y="30" font-size="17" font-weight="bold" '
           f'fill="#0b0b0b">One idle dip, as the bus sees it</text>',
           f'<text x="{left}" y="50" font-size="12" fill="#52514e">Mean of {n} '
           f'dips, warm standing idle, {", ".join(names)}. Change from '
           f'{PROFILE_BASE_S} s before; 0 ms = the lowest value.</text>']
    for p, (title, col, (lo, hi), ticks) in enumerate(panels):
        y0 = top + p * (ph + gap)

        def y(val, y0=y0, lo=lo, hi=hi):
            return y0 + ph - (max(lo, min(hi, val)) - lo) / (hi - lo) * ph

        out.append(f'<text x="{left}" y="{y0 - 8}" font-size="13" '
                   f'fill="#0b0b0b">{title}</text>')
        for a, b, fill in ((-0.50, -0.10, "#eda10022"), (0.0, 0.22, "#2a78d61a")):
            out.append(f'<rect x="{x(a):.1f}" y="{y0}" width="{x(b) - x(a):.1f}" '
                       f'height="{ph}" fill="{fill}"/>')
        for tk in ticks:
            out.append(f'<line x1="{left}" x2="{w - right}" y1="{y(tk):.1f}" '
                       f'y2="{y(tk):.1f}" stroke="'
                       f'{"#9a9994" if tk == 0 else "#e4e3df"}"/>')
            out.append(f'<text x="{left - 8}" y="{y(tk) + 4:.1f}" font-size="11" '
                       f'fill="#52514e" text-anchor="end">{tk}</text>')
        pts = " ".join(f"{x(r[0]):.1f},{y(r[col]):.1f}" for r in rows)
        out.append(f'<polyline points="{pts}" fill="none" stroke="#2a78d6" '
                   f'stroke-width="2" stroke-linejoin="round"/>')
        out.append(f'<line x1="{x(0):.1f}" x2="{x(0):.1f}" y1="{y0}" '
                   f'y2="{y0 + ph}" stroke="#52514e" stroke-dasharray="3 3"/>')
    yb = top + 3 * (ph + gap) - gap + 18
    for o in (-0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4):
        if lo_o <= o <= hi_o:
            out.append(f'<text x="{x(o):.1f}" y="{yb}" font-size="11" '
                       f'fill="#52514e" text-anchor="middle">'
                       f'{round(o * 1000):+d} ms</text>'.replace("+0 ms", "0 ms"))
    out.append(f'<text x="{x(-0.30):.1f}" y="{yb + 22}" font-size="12" '
               f'fill="#8a5a00" text-anchor="middle">the ECU trims</text>')
    out.append(f'<text x="{x(0.11):.1f}" y="{yb + 22}" font-size="12" '
               f'fill="#1c5cab" text-anchor="middle">the ECU catches it</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--trigger", action="store_true")
    g.add_argument("--strata", action="store_true")
    g.add_argument("--runs", action="store_true")
    g.add_argument("--profile", action="store_true")
    g.add_argument("--vcds", nargs="+", metavar="LOG",
                   help="VCDS logs, one per capture, in the same order")
    ap.add_argument("--channel", choices=("b7", "inj"), default="b7",
                    help="--strata: indicated torque or injection time")
    ap.add_argument("--svg", metavar="OUT", help="--profile: also draw it")
    args = ap.parse_args(argv)
    caps = [Capture(p) for p in args.files]
    if args.vcds:
        if len(args.vcds) != len(caps):
            raise SystemExit("--vcds wants one log per capture")
        pooled = {}
        for cap, log in zip(caps, args.vcds):
            for k, v in vcds_near(cap, log).items():
                pooled.setdefault(k, []).extend(v)
        for k in sorted(pooled):
            v = pooled[k]
            if len(v) < 5:
                continue
            se = statistics.pstdev(v) / len(v) ** 0.5
            print(f"  {k[0]} {k[1]:22} {k[2]:13} n={len(v):5d} "
                  f"mean {statistics.mean(v):+8.3f} ±{se:.3f}")
        return 0
    if args.profile:
        rows, n = profile(caps)
        print(f"{n} dips, warm standing idle, cuts left out")
        print("  offset   speed    inj     b7")
        for o, r, i, b in rows:
            print(f"  {o:+.2f}  {r:+6.1f}  {i:+.2f}  {b:+.2f}")
        if args.svg:
            names = [os.path.basename(c.path).split("_")[0] for c in caps]
            with open(args.svg, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(profile_svg(rows, n, names))
        return 0
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
