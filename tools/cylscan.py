#!/usr/bin/env python3
"""Which cylinder -- every stroke of a standing idle put to its cylinder.

docs/engine-health/open.md, *Naming the cylinder*. Written 12/11/2026 for
the owner's request for a third fresh look at the idle and at what group
014 counts. Kept as a tool for the reason idledips.py gives for itself: the
readings it replaces were *ad-hoc scripts, not kept*, and three things they
could not do decide how the idle is read.

1. **The stroke count does not slip.** cutscan.bridged_runs() counts strokes
   by how long a value was held, and loses one where two neighbours read the
   same or a frame is missing, so a cylinder named at an injector cut is
   named two slots off a few minutes later. Here the count is a phase-locked
   loop: engine speed integrated over time is crank angle, one stroke per
   180 degrees, and every change of 0x280's value corrects the phase a
   little (`track`). On `31` one run of 883 s holds all four cuts (1, 4, 4,
   1) on their own slots; no run in the corpus slips.

2. **The crank wheel alternates, and that is not combustion.** Successive
   strokes read alternately high and low by `WHEEL_ALT` of engine speed --
   cylinders 2 and 3 high, 1 and 4 low -- because the two halves of the
   wheel a segment is timed over are not quite equal (about 0.2 deg of
   crank). Measured where nothing burns, on the overrun fuel cut (`--wheel`):
   0.210-0.225 % of engine speed in every band from 1450 to 2500 rpm, 850
   windows of 13 captures from 24/9 to 10/11; and by cylinder, over the
   13 overruns that run into an idle in one count, -0.219, +0.217,
   -0.218 and +0.219 % for 1, 3, 4, 2: nothing is left once it is out. At idle it is 1.7 rpm, as large as the pattern it
   sits under, and it is what made cylinder 4 look weak.

3. **A stroke's loss shows in two slots.** About a quarter of it is in the
   value before its own (`OWN_SHARE`): the first dead stroke of every cut
   reads -7 to -18 rpm and then -24 to -33. `deviation()` undoes both.

What comes out
--------------

default     every standing idle run (warm ones, or ``--all``): each
            cylinder's steady deviation in per cent of one stroke's work,
            and its weak strokes per 1000; ``--minutes`` the same minute by
            minute, which is where cylinder 3's swells show.
``--vcds``  group 014's increments at a standing idle, each put to the
            cylinder of the weakest stroke in the sample interval before it:
            the ECU's own misfire count by cylinder, which the ECU does not
            give (no groups 015/016, docs/engine-health/vcds.md).
``--wheel`` the alternation on the overrun fuel cut, the measurement behind
            `WHEEL_ALT`; and, for every overrun that runs into a standing
            idle, the same steps by cylinder -- which cylinders read high,
            and that nothing else is left where nothing burns.

How a cylinder gets its name: with no cut in the run, **the strongest slot
is cylinder 2** -- true at every injector cut in the corpus (`31`, `41`,
`43`, `44`, `46`) -- and the firing order 1-3-4-2 names the rest. A run
whose strongest slot does not stand `NAME_MARGIN_RPM` clear is reported
unnamed.

    python cylscan.py FILE [FILE ...]
    python cylscan.py --minutes FILE
    python cylscan.py --vcds LOG.csv FILE
    python cylscan.py --wheel FILE [FILE ...]
"""
from __future__ import annotations

import argparse
import bisect
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canlog  # noqa: E402
import cutscan  # noqa: E402

#: The crank wheel's alternation: step amplitude over engine speed. Measured
#: on the overrun fuel cut, `--wheel`; cylinders 2 and 3 read high.
WHEEL_ALT = 0.00217
#: The share of a stroke's deviation that shows in its own slot; the rest is
#: in the slot before. Read off the first dead stroke of the eight cuts and
#: off 6,000 isolated weak strokes (0.75-0.78).
OWN_SHARE = 0.77
#: One whole stroke's work in rpm of step: a cylinder out reads -23.5 to -28
#: below the idle before it in its own slot, which `OWN_SHARE` and the three
#: live cylinders' share make 32-36.
STROKE_RPM = 34.0
#: A stroke this far below its own cylinder's median step is weak.
WEAK_RPM = 12.0
#: The firing order; the slot after cylinder 4's is cylinder 2's.
FIRING_ORDER = (1, 3, 4, 2)
#: `track`: how much of each phase error is taken into the offset, and how
#: far ahead the reported speed is read (it is a segment's mean, reported
#: after the segment).
PLL_GAIN = 0.05
PLL_LEAD_STROKES = 0.75
#: The idle gate: engine speed, the pedal within one count of its rest, the
#: car standing (STANDSTILL_MMH in src/config.h).
IDLE_RPM = (550.0, 1150.0)
GATE_SPEED_MMH = 100
#: A run shorter than this is not read; a frame gap longer than this ends it.
MIN_RUN_S = 30.0
MAX_GAP_S = 0.1
#: The strongest slot has to stand this far above the next for a name.
NAME_MARGIN_RPM = 1.5
#: A cylinder is out where a slot's mean step over `CUT_SLOT_STROKES` of its
#: own strokes is below `CUT_STEP_RPM`; that many cycles each side are left
#: out with it.
CUT_STEP_RPM = -12.0
CUT_SLOT_STROKES = 40
#: Weak strokes are judged against the slot's median over blocks this long.
BLOCK_S = 30.0
WARM_OIL_C = 85.0
#: `--vcds`: the stroke 014 counted lies between the sample before the rise,
#: less `LAG_BEFORE_S`, and the sample of the rise, less `LAG_AFTER_S`.
LAG_BEFORE_S = 0.30
LAG_AFTER_S = 0.12
VCDS_MAX_GAP_S = 2.5
ALIGN_FINE_S = 0.05
#: `--wheel`: an overrun is the fuel counter standing this long, the engine
#: between these speeds; read in windows of this many strokes.
OVERRUN_MIN_S = 2.0
OVERRUN_RPM = (1300.0, 2500.0)
WHEEL_WINDOW = 40
#: `--wheel`, the names: an overrun is linked to the standing idle that
#: begins within `LINK_S` of its end, if that idle gives `LINK_IDLE_SAMPLES`
#: frames under `LINK_IDLE_RPM` and its strongest slot stands
#: `LINK_MARGIN_RPM` clear.
LINK_S = 45.0
LINK_IDLE_RPM = 950.0
LINK_IDLE_SAMPLES = 1400
LINK_MARGIN_RPM = 2.0


# --- reading ----------------------------------------------------------------

def read(path):
    """{e: [(t, rpm, throttle, speed mm/h)], fuel: [(t, counter)],
    oil: [(t, degC)], ac: [(t, on)]} -- one pass over a `_z1` capture."""
    frames = canlog.parse_file(path)
    if not frames or frames[0].ts_ms is None:
        raise SystemExit(f"{path}: no adapter timestamps; only the _z1 logs "
                         "can be read for this")
    t0 = frames[0].ts_ms
    e, fuel, oil, ac = [], [], [], []
    speed = 0
    for f in frames:
        t = (f.ts_ms - t0) / 1000.0
        d = f.data
        if f.can_id == 0x280 and len(d) >= 8:
            e.append((t, (d[2] | d[3] << 8) / 4.0, d[5], speed))
        elif f.can_id == 0x1A0 and len(d) >= 4:
            if (d[1] & 0x40) != 0 and (d[1] & 0x03) == 0:
                speed = (d[2] | d[3] << 8) * 5
        elif f.can_id == 0x480 and len(d) >= 4:
            fuel.append((t, (d[2] | d[3] << 8) & 0x7FFF))
        elif f.can_id == 0x420 and len(d) >= 4 and d[3] != 0xFF:
            oil.append((t, canlog.oil_c(d[3])))
        elif f.can_id == 0x288 and len(d) >= 3:
            ac.append((t, bool(d[2] & 0x08)))
    return {"e": e, "fuel": fuel, "oil": oil, "ac": ac}


def _at(pairs, t, default=None):
    i = bisect.bisect_right(pairs, (t, float("inf"))) - 1
    return pairs[i][1] if i >= 0 else default


# --- the stroke count -------------------------------------------------------

def track(e, i0=0, i1=None, gain=PLL_GAIN, lead=PLL_LEAD_STROKES):
    """[(t, rpm, stroke index)] for every change of 0x280's value in
    e[i0:i1]. The index is the integrated crank angle in strokes, rounded,
    with the offset following the rounding error."""
    ts = [x[0] for x in e[i0:i1]]
    rs = [x[1] for x in e[i0:i1]]
    n = len(ts)
    out = []
    phi = 0.0
    off = None
    j = 0
    for i in range(1, n):
        # the speed reported `lead` strokes later is this moment's speed
        ahead = ts[i] + lead * 30.0 / max(rs[i], 300.0)
        while j + 1 < n and ts[j + 1] <= ahead:
            j += 1
        dt = min(max(ts[i] - ts[i - 1], 0.0), 0.2)
        phi += rs[max(j, i)] / 30.0 * dt
        if rs[i] != rs[i - 1]:
            if off is None:
                off = phi
            x = phi - off
            k = round(x)
            off += gain * (x - k)
            out.append((ts[i], rs[i], k))
    return out


class Run:
    """One stretch of strokes on a dense index: T, R (rpm), S (step from the
    stroke before; None for the first), and what is derived from them."""

    def __init__(self, events):
        k0 = events[0][2]
        n = events[-1][2] - k0 + 1
        self.T = [None] * n
        self.R = [None] * n
        for t, r, k in events:
            self.T[k - k0] = t
            self.R[k - k0] = r
        for i in range(1, n):          # a held value hid this stroke
            if self.R[i] is None:
                self.R[i] = self.R[i - 1]
                self.T[i] = self.T[i - 1] + 30.0 / self.R[i - 1]
        self.S = [None] + [self.R[i] - self.R[i - 1] for i in range(1, n)]
        self.cut = _cut_mask(self.S)
        self.slot2, self.margin = _strongest(self.S, self.cut)
        self.E = _residual(self.T, self.S, self.cut)

    def __len__(self):
        return len(self.R)

    @property
    def named(self):
        return self.margin >= NAME_MARGIN_RPM

    def cyl(self, i):
        """The cylinder whose stroke index i is: slot2 is 2, then 1, 3, 4."""
        return (2, 1, 3, 4)[(i - self.slot2) % 4]

    def span(self, t0, t1):
        return (bisect.bisect_left(self.T, t0), bisect.bisect_left(self.T, t1))


def _cut_mask(S):
    n = len(S)
    mask = [False] * n
    w = CUT_SLOT_STROKES
    for q in range(4):
        idx = list(range(q, n, 4))
        vals = [S[i] or 0.0 for i in idx]
        acc = [0.0]
        for v in vals:
            acc.append(acc[-1] + v)
        for m in range(len(vals) - w + 1):
            if (acc[m + w] - acc[m]) / w < CUT_STEP_RPM:
                a = max(0, idx[m] - 4 * w)
                b = min(n, idx[m + w - 1] + 4 * w)
                for i in range(a, b):
                    mask[i] = True
    return mask


def _strongest(S, cut):
    sums, cnt = [0.0] * 4, [0] * 4
    for i, s in enumerate(S):
        if s is not None and not cut[i]:
            sums[i % 4] += s
            cnt[i % 4] += 1
    if min(cnt) == 0:
        return 0, 0.0
    means = [a / c for a, c in zip(sums, cnt)]
    order = sorted(range(4), key=lambda q: means[q])
    return order[-1], means[order[-1]] - means[order[-2]]


def _residual(T, S, cut):
    """Each step against its own slot's median over the `BLOCK_S` block it
    is in: what a stroke lost, with the steady pattern taken out."""
    n = len(S)
    E = [None] * n
    a = 1
    while a < n:
        b = bisect.bisect_left(T, T[a] + BLOCK_S, a, n)
        if n - b < 200:
            b = n
        for q in range(4):
            idx = [i for i in range(a + (q - a) % 4, b, 4) if not cut[i]]
            if len(idx) < 8:
                continue
            med = statistics.median(S[i] for i in idx)
            for i in idx:
                E[i] = S[i] - med
        a = b
    return E


def idle_runs(data, min_s=MIN_RUN_S):
    """Every standing idle of `min_s` and more as a `Run`."""
    e = data["e"]
    at_idle = sorted(x[2] for x in e if 700.0 < x[1] < 900.0)
    rest = at_idle[len(at_idle) // 2] if at_idle else 38
    out = []
    i, n = 0, len(e)
    while i < n:
        t, r, thr, spd = e[i]
        if not (IDLE_RPM[0] <= r <= IDLE_RPM[1] and thr <= rest + 1
                and spd <= GATE_SPEED_MMH):
            i += 1
            continue
        j = i + 1
        while j < n:
            t2, r2, thr2, spd2 = e[j]
            if not (IDLE_RPM[0] <= r2 <= IDLE_RPM[1] and thr2 <= rest + 1
                    and spd2 <= GATE_SPEED_MMH) or t2 - e[j - 1][0] > MAX_GAP_S:
                break
            j += 1
        if e[j - 1][0] - t >= min_s:
            ev = track(e, i, j)
            if len(ev) > 100:
                out.append(Run(ev))
        i = j + 1
    return out


# --- what each cylinder gives -----------------------------------------------

def invert(p):
    """Undo `OWN_SHARE`: p[k] = a d[k] + (1 - a) d[k + 1], cyclic."""
    a, b = OWN_SHARE, 1.0 - OWN_SHARE
    c = [a ** 3, -a * a * b, a * b * b, -b ** 3]
    den = a ** 4 - b ** 4
    return [sum(c[j] * p[(k + j) % 4] for j in range(4)) / den for k in range(4)]


def deviation(run, i0=1, i1=None):
    """{cylinder: per cent of one stroke's work above the four's mean} over
    strokes i0..i1, cuts left out; None with too few strokes."""
    i1 = len(run) if i1 is None else i1
    sums = {c: 0.0 for c in FIRING_ORDER}
    cnt = {c: 0 for c in FIRING_ORDER}
    rpm, m = 0.0, 0
    for i in range(max(i0, 1), i1):
        if run.cut[i]:
            continue
        c = run.cyl(i)
        sums[c] += run.S[i]
        cnt[c] += 1
        rpm += run.R[i]
        m += 1
    if min(cnt.values()) < 25:
        return None
    p = [sums[c] / cnt[c] for c in FIRING_ORDER]
    mean = sum(p) / 4.0
    alt = WHEEL_ALT * rpm / m
    wheel = {1: -alt, 3: alt, 4: -alt, 2: alt}
    d = invert([x - mean - wheel[c] for x, c in zip(p, FIRING_ORDER)])
    return {c: 100.0 * x / STROKE_RPM for c, x in zip(FIRING_ORDER, d)}


def weak(run, i0=1, i1=None, depth=WEAK_RPM):
    """({cylinder: weak strokes}, {cylinder: strokes read}) over i0..i1."""
    i1 = len(run) if i1 is None else i1
    w = {c: 0 for c in FIRING_ORDER}
    n = {c: 0 for c in FIRING_ORDER}
    for i in range(max(i0, 1), i1):
        if run.E[i] is None:
            continue
        c = run.cyl(i)
        n[c] += 1
        if run.E[i] <= -depth:
            w[c] += 1
    return w, n


def cut_cylinder(run):
    """The cylinder that was out in this run's cuts, by the run's naming;
    None with no cut."""
    sums, cnt = {}, {}
    for i, s in enumerate(run.S):
        if s is not None and run.cut[i]:
            c = run.cyl(i)
            sums[c] = sums.get(c, 0.0) + s
            cnt[c] = cnt.get(c, 0) + 1
    if not cnt:
        return None
    means = {c: sums[c] / cnt[c] for c in cnt}
    c = min(means, key=means.get)
    return c if means[c] < CUT_STEP_RPM else None


# --- 014 by cylinder --------------------------------------------------------

def align(vcds_rpm, e):
    """Seconds to add to VCDS time for capture time: cutscan.align()'s
    half-second answer, then the best of `ALIGN_FINE_S` steps around it --
    the interval a rise is looked for in is only a few strokes wide."""
    cap = [(x[0], x[1]) for x in e]
    coarse = cutscan.align(vcds_rpm, cap)
    ts = [t for t, _ in cap]

    def err(off):
        tot, n = 0.0, 0
        for t, r in vcds_rpm:
            i = bisect.bisect_right(ts, t + off) - 1
            if 0 <= i < len(cap) - 1:
                tot += abs(cap[i][1] - r)
                n += 1
        return tot / n if n else float("inf")

    steps = int(round(1.0 / ALIGN_FINE_S))
    return min((coarse + m * ALIGN_FINE_S for m in range(-steps, steps + 1)),
               key=err)


def misfires_014(vcds_path, data, runs):
    """[(capture time, cylinder, the stroke's residual rpm, rise)] for every
    rise of 014's count between two samples at a standing idle with
    recognition on, in a named run and outside the cuts."""
    g = cutscan.read_vcds(vcds_path).get("014")
    if not g:
        raise SystemExit(f"{vcds_path}: no group 014")
    pts = []
    for t, f in g:
        try:
            pts.append((t, float(f[0]), int(float(f[2])), f[3].startswith("aktiv")))
        except (ValueError, IndexError):
            continue
    off = align([(t, r) for t, r, _, _ in pts], data["e"])
    out = []
    for (t0, r0, m0, a0), (t1, r1, m1, a1) in zip(pts, pts[1:]):
        if not (a0 and a1 and m1 > m0 and t1 - t0 <= VCDS_MAX_GAP_S
                and 600 <= r0 <= 1000 and 600 <= r1 <= 1000):
            continue
        a, b = t0 + off - LAG_BEFORE_S, t1 + off - LAG_AFTER_S
        for run in runs:
            if not (run.named and run.T[0] <= a and b <= run.T[-1]):
                continue
            i0, i1 = run.span(a, b)
            j0, j1 = run.span(a - 3.0, b + 3.0)
            if any(run.cut[j0:j1]):
                break
            idx = [i for i in range(i0, i1) if run.E[i] is not None]
            if len(idx) >= 5:
                i = min(idx, key=lambda k: run.E[k])
                out.append((t1 + off, run.cyl(i), run.E[i], m1 - m0))
            break
    return out


# --- the wheel --------------------------------------------------------------

def _overruns(data):
    """(i0, i1, end time) of every stretch of 0x280 samples with the fuel
    counter standing `OVERRUN_MIN_S` and the engine inside `OVERRUN_RPM`."""
    e, fuel = data["e"], data["fuel"]
    et = [x[0] for x in e]
    i, n = 0, len(fuel) - 1
    while i < n:
        if fuel[i + 1][1] != fuel[i][1]:
            i += 1
            continue
        j = i
        while j < n and fuel[j + 1][1] == fuel[j][1]:
            j += 1
        a, b = fuel[i][0] + 0.3, fuel[j][0]
        i = j
        if b - a < OVERRUN_MIN_S:
            continue
        i0, i1 = bisect.bisect_left(et, a), bisect.bisect_right(et, b)
        rs = [x[1] for x in e[i0:i1]]
        if len(rs) < 50 or min(rs) < OVERRUN_RPM[0] or max(rs) > OVERRUN_RPM[1]:
            continue
        yield i0, i1, b


def _steps(ev):
    """[(stroke index, step, rpm)] for events one stroke apart."""
    return [(ev[m][2], ev[m][1] - ev[m - 1][1], ev[m][1])
            for m in range(1, len(ev)) if ev[m][2] - ev[m - 1][2] == 1]


def _detrended(seq):
    """Windows of `WHEEL_WINDOW` steps, a straight line taken out of each:
    [[(stroke index, residual step, rpm)]]."""
    w = WHEEL_WINDOW
    out = []
    for q in range(0, len(seq) - w + 1, w):
        ss = [s[1] for s in seq[q:q + w]]
        xm, ym = (w - 1) / 2.0, sum(ss) / w
        slope = (sum((x - xm) * (y - ym) for x, y in enumerate(ss))
                 / sum((x - xm) ** 2 for x in range(w)))
        out.append([(s[0], y - ym - slope * (x - xm), s[2])
                    for x, (s, y) in enumerate(zip(seq[q:q + w], ss))])
    return out


def wheel_windows(data):
    """[(rpm, |alternation| in rpm)] per `WHEEL_WINDOW` strokes of overrun
    fuel cut: the mean step of the even strokes less the odd ones', halved,
    a straight line taken out first."""
    out = []
    for i0, i1, _ in _overruns(data):
        for win in _detrended(_steps(track(data["e"], i0, i1))):
            ev_ = [r for k, r, _ in win if k % 2 == 0]
            od_ = [r for k, r, _ in win if k % 2 == 1]
            if len(ev_) < 8 or len(od_) < 8:
                continue
            alt = (sum(ev_) / len(ev_) - sum(od_) / len(od_)) / 2.0
            out.append((sum(x[2] for x in win) / len(win), abs(alt)))
    return out


def wheel_named(data):
    """({cylinder: [step / rpm, ...]}, overruns linked): the overrun's steps
    by cylinder, for every overrun that runs into a standing idle within
    `LINK_S` in one stroke count -- the idle's strongest slot names the
    cylinders, the overrun's strokes before it keep the names. With
    nothing burning, what each cylinder's slot reads is the wheel's and
    nothing else: +WHEEL_ALT for 2 and 3, -WHEEL_ALT for 1 and 4."""
    e = data["e"]
    et = [x[0] for x in e]
    got = {c: [] for c in FIRING_ORDER}
    linked = 0
    for i0, i1, b in _overruns(data):
        j1 = bisect.bisect_right(et, b + LINK_S)
        after = e[i1:j1]
        if (not after or max(x[1] for x in after) > OVERRUN_RPM[1]
                or min(x[1] for x in after) < 500.0):
            continue
        idle = [m for m, x in enumerate(after)
                if x[1] < LINK_IDLE_RPM and x[3] <= GATE_SPEED_MMH]
        if len(idle) < LINK_IDLE_SAMPLES:
            continue
        t_idle = after[idle[0]][0] + 2.0
        seq = _steps(track(e, i0, i1 + idle[-1] + 1))
        tk = {ev[2]: ev[0] for ev in track(e, i0, i1 + idle[-1] + 1)}
        sums, cnt = [0.0] * 4, [0] * 4
        for k, s, r in seq:
            if tk[k] >= t_idle and r < LINK_IDLE_RPM:
                sums[k % 4] += s
                cnt[k % 4] += 1
        if min(cnt) < 60:
            continue
        means = [a / c for a, c in zip(sums, cnt)]
        order = sorted(range(4), key=lambda q: means[q])
        if means[order[-1]] - means[order[-2]] < LINK_MARGIN_RPM:
            continue
        slot2 = order[-1]
        linked += 1
        for win in _detrended([x for x in seq if tk[x[0]] <= b]):
            for k, res, r in win:
                got[(2, 1, 3, 4)[(k - slot2) % 4]].append(res / r)
    return got, linked


# --- reports ----------------------------------------------------------------

def _fmt_dev(d):
    return "   ".join("%d %+5.1f" % (c, d[c]) for c in FIRING_ORDER)


def _fmt_weak(w, n):
    return "  ".join("%d %4.1f" % (c, 1000.0 * w[c] / n[c] if n[c] else 0.0)
                     for c in FIRING_ORDER)


def report(path, data, runs, show_all=False, minutes=False, out=sys.stdout):
    name = os.path.basename(path)
    print(f"{name}: each cylinder's steady deviation, % of a stroke "
          f"(wheel {100 * WHEEL_ALT:.3f} % out), and weak strokes "
          f"(-{WEAK_RPM:.0f} rpm) per 1000", file=out)
    tw = {c: 0 for c in FIRING_ORDER}
    tn = {c: 0 for c in FIRING_ORDER}
    for run in runs:
        t0, t1 = run.T[1], run.T[-1]
        oil = _at(data["oil"], t0)
        if t1 - t0 < 60.0 or (not show_all and (oil is None or oil < WARM_OIL_C)):
            continue
        if not run.named:
            print(f"  {t0:7.0f} s  {t1 - t0:5.0f} s  not named: the strongest "
                  f"slot only {run.margin:.1f} rpm clear", file=out)
            continue
        d = deviation(run)
        if d is None:
            continue
        w, n = weak(run)
        cut = cut_cylinder(run)
        print(f"  {t0:7.0f} s  {t1 - t0:5.0f} s  oil {oil if oil is not None else float('nan'):5.1f}"
              f"  | {_fmt_dev(d)}  | {_fmt_weak(w, n)}"
              + (f"  | cut on {cut}" if cut else ""), file=out)
        for c in FIRING_ORDER:
            tw[c] += w[c]
            tn[c] += n[c]
        if minutes:
            t = t0
            while t < t1 - 30.0:
                i0, i1 = run.span(t, t + 60.0)
                dm = deviation(run, i0, i1)
                wm, nm = weak(run, i0, i1)
                ac = _at(data["ac"], t + 30.0)
                if dm is not None:
                    print(f"      +{(t - t0) / 60.0:4.1f} min  | {_fmt_dev(dm)}  | "
                          + "  ".join("%d %2d" % (c, wm[c]) for c in FIRING_ORDER)
                          + ("  A/C" if ac else ""), file=out)
                elif any(run.cut[i0:i1]):
                    print(f"      +{(t - t0) / 60.0:4.1f} min  | a cylinder out",
                          file=out)
                t += 60.0
    total = sum(tw.values())
    if total:
        print("  weak strokes: " + ", ".join(
            "%d: %d (%.0f %%)" % (c, tw[c], 100.0 * tw[c] / total)
            for c in FIRING_ORDER), file=out)
    return tw, tn


def report_014(vcds_path, data, runs, out=sys.stdout):
    got = misfires_014(vcds_path, data, runs)
    print(f"{os.path.basename(vcds_path)}: {len(got)} rises of 014 at a "
          f"standing idle, by the cylinder of the weakest stroke before each",
          file=out)
    for label, sel in (("all", got),
                       ("the stroke at least %.0f rpm down" % WEAK_RPM,
                        [x for x in got if x[2] <= -WEAK_RPM])):
        cnt = {c: sum(1 for x in sel if x[1] == c) for c in FIRING_ORDER}
        print(f"  {label}: " + ", ".join(
            "%d: %d" % (c, cnt[c]) for c in FIRING_ORDER)
            + (f"  -- {100.0 * cnt[3] / len(sel):.0f} % on 3" if sel else ""),
            file=out)
    return got


def report_wheel(paths, out=sys.stdout):
    rows = []
    named = {c: [] for c in FIRING_ORDER}
    linked = 0
    for p in paths:
        data = read(p)
        w = wheel_windows(data)
        got, n = wheel_named(data)
        linked += n
        for c in FIRING_ORDER:
            named[c] += got[c]
        rows += w
        if w:
            print(f"{os.path.basename(p)}: {len(w)} windows, "
                  f"{100 * statistics.median(a / r for r, a in w):.3f} % of "
                  f"engine speed", file=out)
        else:
            print(f"{os.path.basename(p)}: no overrun long enough", file=out)
    for lo in range(int(OVERRUN_RPM[0]), int(OVERRUN_RPM[1]), 150):
        band = [(r, a) for r, a in rows if lo <= r < lo + 150]
        if len(band) >= 4:
            print(f"  {lo}-{lo + 150} rpm: {len(band):4d} windows, "
                  f"{statistics.median(a for _, a in band):.2f} rpm, "
                  f"{100 * statistics.median(a / r for r, a in band):.3f} %",
                  file=out)
    if rows:
        print(f"  all: {len(rows)} windows, "
              f"{100 * statistics.median(a / r for r, a in rows):.3f} % "
              f"(WHEEL_ALT is {100 * WHEEL_ALT:.3f} %)", file=out)
    if linked:
        print(f"  by cylinder, {linked} overruns followed into the idle after "
              f"them (step / engine speed, %; what is left with the wheel "
              f"out, rpm at 800):", file=out)
        sign = {1: -1, 3: 1, 4: -1, 2: 1}
        for c in FIRING_ORDER:
            v = named[c]
            m = sum(v) / len(v)
            se = statistics.pstdev(v) / len(v) ** 0.5
            print(f"    {c}: {100 * m:+.3f} +- {100 * se:.3f} %, "
                  f"{len(v)} strokes; left {800 * (m - sign[c] * WHEEL_ALT):+.2f} rpm",
                  file=out)
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("captures", nargs="+")
    ap.add_argument("--all", action="store_true",
                    help="cold runs too (default: oil %.0f degC and over)" % WARM_OIL_C)
    ap.add_argument("--minutes", action="store_true",
                    help="each run minute by minute")
    ap.add_argument("--vcds", metavar="LOG",
                    help="a VCDS log with group 014 taken beside the (one) capture")
    ap.add_argument("--wheel", action="store_true",
                    help="the crank wheel's alternation on the overrun")
    args = ap.parse_args(argv)
    if args.wheel:
        report_wheel(args.captures)
        return 0
    if args.vcds and len(args.captures) != 1:
        ap.error("--vcds reads one capture")
    for p in args.captures:
        data = read(p)
        runs = idle_runs(data)
        if args.vcds:
            report_014(args.vcds, data, runs)
        else:
            report(p, data, runs, show_all=args.all, minutes=args.minutes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
