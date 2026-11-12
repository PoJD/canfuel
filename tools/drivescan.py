#!/usr/bin/env python3
"""Which cylinder, off idle -- every stroke of a whole drive put to its
cylinder.

docs/engine-health/open.md, *Naming the cylinder*, *Off idle*. Written
12/11/2026 for the owner's questions after cylscan.py: does the idle's
pattern between the cylinders show while driving, what do weak strokes cost
at full throttle, where do group 014's rises fall off idle, and is the
ceiling of about 2,800 rpm on the stroke count a hard one. Kept for the
reason cylscan.py gives for itself.

1. **The count holds through a whole drive.** cylscan.track() corrects its
   phase by *when* 0x280's value changes, and that says nothing once a
   stroke is shorter than a frame (`FRAME_S`: one frame a stroke at about
   2,820 rpm) -- above it the count slipped in 16 of 28 drives. But the
   crank wheel's alternation (cylscan.py: 2 and 3 read high, 1 and 4 low)
   grows with engine speed, so *what* a frame reads says whether its stroke
   is an even or an odd one. `track_drive` uses the timing below
   `TIMING_MAX_RPM` and that parity above it. The integral carries the
   count; the parity only has to keep it from drifting by one. Every named
   standing idle of a capture then finds cylinder 2 on the same slot
   (`--count`).

2. **Only two differences are free of the wheel.** On the overrun, where
   nothing burns, the alternation is `cylscan.WHEEL_ALT` up to about
   2,400 rpm and grows beyond it (to 0.5 % of engine speed at 5,000 rpm),
   so above that the pair 2 and 3 against the pair 1 and 4 cannot be read.
   The wheel raises 2 and 3 alike and lowers 1 and 4 alike: **3 less 2 and
   1 less 4** carry none of it, and the overrun rows show what is left
   (a few tenths of an rpm).

3. **A stroke's work in rpm of step moves with load and speed.** A whole
   stroke is `cylscan.STROKE_RPM` at idle; the same work lifts a faster
   crank less and a loaded cylinder does more of it, so here it is
   `STROKE_RPM * (b7 / IDLE_B7) * (IDLE_RPM / rpm)` (`stroke_rpm`). A
   decision, not a measurement: b7 is the ECU's model (what it asks for;
   at idle 26-29 with the engine's own friction byte at 21), and the crank
   inertia read off standing revs agrees with the idle's figure only to
   about a quarter. **A per cent of a stroke off idle carries that.**

What comes out
--------------

default     3 less 2 and 1 less 4 by engine speed and load (b7), warm, in
            rpm of step and per cent of a stroke: the standing idle, the
            overrun (the check: nothing burns), and driving.
``--weak``  the single strokes: how many read a quarter and a half of a
            stroke under their neighbours, against how many read as far
            over (noise is as often one as the other; a misfire is only
            ever under), and the work the excess is.
``--vcds``  group 014's rises anywhere in the drive, each put to the
            cylinder of the weakest stroke before it, beside the same pick
            in windows `CONTROL_S` before and after -- the most uneven
            cylinder wins that pick by chance, so only the excess counts.
``--count`` the check of 1: the slot the strongest cylinder has at each
            named standing idle through the capture.
``--pulls`` full-throttle pulls: the torque the car's own acceleration
            needs against the torque b7 claims. The car's mass and
            resistances are assumptions (`CAR_*`), so the ratio is good
            to about a tenth -- enough to see a fifth missing, not a
            twentieth.

    python drivescan.py FILE [FILE ...]
    python drivescan.py --weak FILE [FILE ...]
    python drivescan.py --vcds LOG.csv FILE
    python drivescan.py --count FILE [FILE ...]
    python drivescan.py --pulls FILE [FILE ...]
"""
from __future__ import annotations

import argparse
import bisect
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canlog  # noqa: E402
import cutscan  # noqa: E402
import cylscan  # noqa: E402

#: 0x280's period (docs/firmware/can-decoding.md, Trap 6): one frame a
#: stroke at 30 / FRAME_S rpm.
FRAME_S = 0.01065
#: The timing of a value's change corrects the phase below this, the
#: alternation's parity above it.
TIMING_MAX_RPM = 2600.0
#: The parity is read over this many frames, every `PARITY_HOP` frames, for
#: phase shifts of `PARITY_STEP` strokes either way; half the best shift is
#: taken. A fit under `PARITY_MIN` of the window's scatter is not used.
PARITY_FRAMES = 48
PARITY_HOP = 16
PARITY_STEP = 0.05
PARITY_GAIN = 0.5
PARITY_MIN = 0.35
#: The parity's sign is learned where the timing still holds, between
#: `LEARN_RPM`, from this many windows at least.
LEARN_RPM = (1900.0, 2500.0)
LEARN_VOTES = 3
#: A frame gap longer than this, or the engine below `STALL_RPM`, restarts
#: the count.
MAX_GAP_S = 0.15
STALL_RPM = 300.0
#: With no parity to go by the count is restarted past this: one count held
#: from stop to stop in 38 of 38 drives up to about 2,850 rpm on the timing
#: alone and slipped in 16 of 28 above 3,000.
UNAIDED_MAX_RPM = 2850.0
#: A standing idle names the cylinders if it is this long and its strongest
#: slot stands cylscan.NAME_MARGIN_RPM clear.
NAME_IDLE_S = 30.0
#: Strokes are read in windows of this many; a window needs this many of
#: them seen (above 2,820 rpm not every stroke reaches the bus) and this
#: many of each cylinder.
WINDOW = 40
WINDOW_MIN = 24
WINDOW_MIN_CYL = 4
#: `stroke_rpm`: the idle the scale is anchored at.
IDLE_B7 = 25.0
IDLE_RPM = 800.0
WARM_OIL_C = 80.0
#: The bands of the tables.
RPM_BANDS = ((600, 1150), (1150, 1600), (1600, 2100), (2100, 2600),
             (2600, 3300), (3300, 4200), (4200, 5200), (5200, 6500))
B7_BANDS = ((0, 45), (45, 90), (90, 140), (140, 256))
MIN_WINDOWS = 25
MOVING_KMH = 3.0
#: `--vcds`: cylscan's lags, and where the control windows sit.
CONTROL_S = 5.0
#: `--pulls`: the pedal on the floor is the throttle byte at this and b7 at
#: this; a pull is read in windows of `PULL_WINDOW_S` after `PULL_SKIP_S`.
PULL_THROTTLE = 205
PULL_B7 = 140
PULL_MIN_S = 2.0
PULL_SKIP_S = 0.5
PULL_WINDOW_S = 1.0
#: `--pulls`, **assumptions, none read off this car**: mass with the driver,
#: drag area, rolling resistance, driveline efficiency, the engine's and the
#: four wheels' inertia, the tyre's rolling radius (205/55 R16).
CAR_MASS_KG = 1400.0
CAR_CDA_M2 = 0.84
CAR_CRR = 0.012
CAR_ETA = 0.92
CAR_ENGINE_J = 0.22
CAR_WHEELS_J = 3.6
CAR_WHEEL_R_M = 0.316
AIR_KG_M3 = 1.2
#: The firmware's drag line in b7 counts and its scale (src/config.h,
#: DRAG_TORQUE_*, TORQUE_CNM_PER_BIT).
DRAG_B7_BASE = 9.11
DRAG_B7_PER_RPM = 0.6905 / 106.0
NM_PER_B7 = 1.06
#: km/h per 1000 rpm above which a pull is in 3rd, 4th, 5th.
GEAR_EDGES = (13.0, 19.0, 25.5, 32.0)


# --- reading ----------------------------------------------------------------

def read(path):
    """cylscan.read()'s dict with `b7`: 0x280 byte 7 for every sample of
    `e`, and `e` as cylscan has it: (t, rpm, throttle, speed in 0.001 km/h)."""
    frames = canlog.parse_file(path)
    data = cylscan.read(path, frames)
    data["b7"] = [f.data[7] for f in frames
                  if f.can_id == 0x280 and len(f.data) >= 8]
    return data


# --- the stroke count through a drive ---------------------------------------

def _phase(ts, rs):
    """Crank angle in strokes at every sample, the speed read
    cylscan.PLL_LEAD_STROKES ahead as cylscan.track() reads it."""
    n = len(ts)
    phi = [0.0] * n
    j = 0
    for i in range(1, n):
        ahead = ts[i] + cylscan.PLL_LEAD_STROKES * 30.0 / max(rs[i], 300.0)
        while j + 1 < n and ts[j + 1] <= ahead:
            j += 1
        dt = min(max(ts[i] - ts[i - 1], 0.0), 0.2)
        phi[i] = phi[i - 1] + rs[max(j, i)] / 30.0 * dt
    return phi


def _shown(r):
    """How far into a stroke its value is first seen, in strokes: half a
    frame, the timing's lock being on the middle of that."""
    return 0.5 * min(r * FRAME_S / 30.0, 0.8)


_DELTAS = [m * PARITY_STEP for m in range(-int(round(1.0 / PARITY_STEP)),
                                          int(round(1.0 / PARITY_STEP)))]


def _parity(tw, vw, xw):
    """[(shift, score)]: for each phase shift, how well 'even strokes read
    high' fits the window's values with a parabola taken out, as a share of
    their scatter; negative where the odd ones read high."""
    n = len(tw)
    tm = sum(tw) / n
    tau = [t - tm for t in tw]
    # an orthonormal basis for 1, tau, tau^2
    q0 = [1.0 / math.sqrt(n)] * n
    s1 = math.sqrt(sum(x * x for x in tau)) or 1.0
    q1 = [x / s1 for x in tau]
    t2 = [x * x for x in tau]
    a0 = sum(t2) / n
    a1 = sum(x * y for x, y in zip(t2, q1))
    q2 = [x - a0 - a1 * y for x, y in zip(t2, q1)]
    s2 = math.sqrt(sum(x * x for x in q2)) or 1.0
    q2 = [x / s2 for x in q2]
    c0 = sum(v * q for v, q in zip(vw, q0))
    c1 = sum(v * q for v, q in zip(vw, q1))
    c2 = sum(v * q for v, q in zip(vw, q2))
    vr = [v - c0 * a - c1 * b - c2 * c
          for v, a, b, c in zip(vw, q0, q1, q2)]
    nv = math.sqrt(sum(x * x for x in vr)) or 1.0
    out = []
    for d in _DELTAS:
        num = p0 = p1 = p2 = 0.0
        for x, v, a, b, c in zip(xw, vr, q0, q1, q2):
            if int(math.floor(x - d)) & 1:
                num -= v
                p0 -= a
                p1 -= b
                p2 -= c
            else:
                num += v
                p0 += a
                p1 += b
                p2 += c
        den = n - p0 * p0 - p1 * p1 - p2 * p2
        out.append((d, num / math.sqrt(den) / nv if den >= 0.25 * n else 0.0))
    return out


def track_drive(e, sign=None):
    """(k, seg) for every sample of `e`: the index of the stroke whose speed
    the frame shows, and a number that changes where the count restarts (a
    frame gap, the engine stopped); k is None before the first lock. With
    `sign` None the parity is not used and the count restarts past
    `UNAIDED_MAX_RPM`; +1 where the even strokes are cylinder 2's and
    3's, -1 where the odd ones are (`learn_sign`)."""
    ts = [x[0] for x in e]
    rs = [x[1] for x in e]
    n = len(ts)
    phi = _phase(ts, rs)
    cc = [_shown(r) for r in rs]
    k = [None] * n
    seg = [0] * n
    off = None
    s = 0
    last = -PARITY_HOP
    for i in range(1, n):
        if (ts[i] - ts[i - 1] > MAX_GAP_S or rs[i] < STALL_RPM
                or (sign is None and rs[i] > UNAIDED_MAX_RPM)):
            if off is not None:
                s += 1
            off = None
            seg[i] = s
            continue
        seg[i] = s
        if off is None:
            if rs[i] == rs[i - 1]:
                continue
            off = phi[i]
        x = phi[i] - off
        if rs[i] < TIMING_MAX_RPM:
            if rs[i] != rs[i - 1]:
                off += cylscan.PLL_GAIN * (x - round(x))
        elif (sign is not None and i - last >= PARITY_HOP
              and i >= PARITY_FRAMES):
            a = i - PARITY_FRAMES + 1
            last = i
            if (seg[a] == s and k[a] is not None
                    and min(rs[a:i + 1]) >= TIMING_MAX_RPM - 200.0):
                sc = _parity(ts[a:i + 1], rs[a:i + 1],
                             [phi[m] - off + cc[m] for m in range(a, i + 1)])
                top = max(sign * v for _, v in sc)
                if top > PARITY_MIN:
                    d = max(sc, key=lambda dv: sign * dv[1]
                            - 0.02 * abs(dv[0]) * top)[0]
                    off += PARITY_GAIN * d
        k[i] = int(math.floor(phi[i] - off + cc[i]))
    return k, seg


def learn_sign(e, k, seg):
    """+1 or -1, or None: which strokes of a timing-only count read high,
    from the windows inside `LEARN_RPM` before the count first leaves the
    timing's reach. The wheel says they are cylinder 2's and 3's."""
    ts = [x[0] for x in e]
    rs = [x[1] for x in e]
    phi = _phase(ts, rs)
    votes = 0
    n = 0
    for i in range(PARITY_FRAMES, len(e), PARITY_HOP):
        if rs[i] >= TIMING_MAX_RPM:
            break
        a = i - PARITY_FRAMES + 1
        w = rs[a:i + 1]
        if (min(w) < LEARN_RPM[0] or max(w) > LEARN_RPM[1]
                or seg[a] != seg[i] or k[a] is None):
            continue
        # the count's own phase: a frame shows stroke floor(phi - off + c)
        # and k is that floor, so phi - off + c is anything in [k, k + 1)
        x = [k[m] + 0.5 for m in range(a, i + 1)]
        sc = dict(_parity(ts[a:i + 1], w, x))[0.0]
        if abs(sc) > 0.5:
            votes += 1 if sc > 0 else -1
            n += 1
    if n >= LEARN_VOTES and abs(votes) == n:
        return 1 if votes > 0 else -1
    return None


# --- the strokes of a drive --------------------------------------------------

class Drive:
    """One capture, every stroke on its index: K, T, R (rpm), and for each
    the bus beside it -- B7, THR, V (km/h), CUT (the fuel counter standing),
    OIL -- and SLOT2, the slot (index mod 4) of cylinder 2 where the
    stretch is named, else None."""

    def __init__(self, data, parity=True):
        e = data["e"]
        k, seg = track_drive(e)
        self.idle_spans = _idle_spans(data)
        self.sign = None
        if parity:
            self.sign = learn_sign(e, k, seg)
            if self.sign is None:
                self.sign = self._sign_from_idle(e, k, seg)
            if self.sign is not None:
                k, seg = track_drive(e, self.sign)
        fuel = data["fuel"]
        ft = [x[0] for x in fuel]
        self.K, self.T, self.R = [], [], []
        self.B7, self.THR, self.V, self.CUT, self.OIL = [], [], [], [], []
        self.SEG = []
        prev = None
        for i, x in enumerate(e):
            if k[i] is None or (prev is not None and seg[i] == prev[0]
                                and k[i] <= prev[1]):
                continue
            prev = (seg[i], k[i])
            t = x[0]
            self.K.append(k[i])
            self.SEG.append(seg[i])
            self.T.append(t)
            self.R.append(x[1])
            self.THR.append(x[2])
            self.V.append(x[3] / 1e3)
            self.B7.append(data["b7"][i])
            j = bisect.bisect_left(ft, t)
            lo, hi = max(j - 6, 0), min(j + 6, len(fuel) - 1)
            self.CUT.append(bool(fuel) and fuel[hi][1] == fuel[lo][1])
            self.OIL.append(cylscan._at(data["oil"], t))
        self.idles = self._name()

    def _idle_slot(self, t0, t1, K, T, R):
        """(slot of the strongest cylinder, its margin) over one idle."""
        a, b = bisect.bisect_left(T, t0 + 2.0), bisect.bisect_left(T, t1 - 1.0)
        sums, cnt = [0.0] * 4, [0] * 4
        for i in range(a + 1, b):
            if K[i] - K[i - 1] == 1:
                sums[K[i] % 4] += R[i] - R[i - 1]
                cnt[K[i] % 4] += 1
        if min(cnt) < 100:
            return None, 0.0
        means = [x / c for x, c in zip(sums, cnt)]
        order = sorted(range(4), key=lambda q: means[q])
        return order[-1], means[order[-1]] - means[order[-2]]

    def _sign_from_idle(self, e, k, seg):
        """The parity's sign from the first named idle, where no window
        could vote: cylinder 2's slot is one of the two that read high."""
        K, T, R = [], [], []
        for i, x in enumerate(e):
            if x[1] >= TIMING_MAX_RPM:
                break
            if k[i] is not None and (not K or k[i] > K[-1]) and seg[i] == 0:
                K.append(k[i])
                T.append(x[0])
                R.append(x[1])
        for t0, t1 in self.idle_spans:
            if not T or t1 > T[-1]:
                break
            slot, margin = self._idle_slot(t0, t1, K, T, R)
            if slot is not None and margin >= cylscan.NAME_MARGIN_RPM:
                return 1 if slot % 2 == 0 else -1
        return None

    def _name(self):
        """[(t0, t1, slot, margin, segment)] for the named idles; sets
        SLOT2 for every stretch whose idles agree."""
        idles = []
        for t0, t1 in self.idle_spans:
            a = bisect.bisect_left(self.T, t0)
            b = bisect.bisect_left(self.T, t1)
            if b - a < 400 or self.SEG[a] != self.SEG[b - 1]:
                continue
            slot, margin = self._idle_slot(t0, t1, self.K, self.T, self.R)
            if slot is not None and margin >= cylscan.NAME_MARGIN_RPM:
                idles.append((t0, t1, slot, margin, self.SEG[a]))
        by_seg = {}
        for x in idles:
            by_seg.setdefault(x[4], set()).add(x[2])
        self.SLOT2 = [next(iter(by_seg[s])) if len(by_seg.get(s, ())) == 1
                      else None for s in self.SEG]
        return idles

    def cyl(self, i):
        return (2, 1, 3, 4)[(self.K[i] - self.SLOT2[i]) % 4]


def _idle_spans(data, min_s=NAME_IDLE_S):
    """(t0, t1) of every standing idle by cylscan.idle_runs()'s gate."""
    e = data["e"]
    at_idle = sorted(x[2] for x in e if 700.0 < x[1] < 900.0)
    rest = at_idle[len(at_idle) // 2] if at_idle else 38
    lo, hi = cylscan.IDLE_RPM

    def idle(x):
        return (lo <= x[1] <= hi and x[2] <= rest + 1
                and x[3] <= cylscan.GATE_SPEED_MMH)

    out = []
    i, n = 0, len(e)
    while i < n:
        if not idle(e[i]):
            i += 1
            continue
        j = i + 1
        while j < n and idle(e[j]) and e[j][0] - e[j - 1][0] <= cylscan.MAX_GAP_S:
            j += 1
        if e[j - 1][0] - e[i][0] >= min_s:
            out.append((e[i][0], e[j - 1][0]))
        i = j + 1
    return out


def stroke_rpm(rpm, b7):
    """One whole stroke's work in rpm of step at this speed and load."""
    return cylscan.STROKE_RPM * (b7 / IDLE_B7) * (IDLE_RPM / rpm)


# --- windows -----------------------------------------------------------------

def _solve(A, y):
    """Least squares by the normal equations; None where they are singular."""
    m = len(A[0])
    N = [[sum(r[a] * r[b] for r in A) for b in range(m)] for a in range(m)]
    v = [sum(r[a] * yy for r, yy in zip(A, y)) for a in range(m)]
    for c in range(m):
        p = max(range(c, m), key=lambda q: abs(N[q][c]))
        if abs(N[p][c]) < 1e-9:
            return None
        N[c], N[p] = N[p], N[c]
        v[c], v[p] = v[p], v[c]
        for q in range(c + 1, m):
            f = N[q][c] / N[c][c]
            for b in range(c, m):
                N[q][b] -= f * N[c][b]
            v[q] -= f * v[c]
    x = [0.0] * m
    for c in range(m - 1, -1, -1):
        x[c] = (v[c] - sum(N[c][b] * x[b] for b in range(c + 1, m))) / N[c][c]
    return x


class Window:
    """`WINDOW` stroke indices of a named stretch: each cylinder's level
    about a parabola through the speed, and what every stroke is off it."""

    def __init__(self, d, i, j):
        self.i, self.j = i, j
        n = j - i
        km = sum(d.K[i:j]) / n
        rows = []
        self.cyl = [d.cyl(m) for m in range(i, j)]
        for m, c in zip(range(i, j), self.cyl):
            u = (d.K[m] - km) / WINDOW
            rows.append([1.0, u, u * u,
                         (c == 1) - (c == 2), (c == 3) - (c == 2),
                         (c == 4) - (c == 2)])
        coef = _solve(rows, d.R[i:j])
        self.ok = coef is not None
        if not self.ok:
            return
        self.level = {1: coef[3], 3: coef[4], 4: coef[5],
                      2: -coef[3] - coef[4] - coef[5]}
        self.res = [r - sum(a * b for a, b in zip(row, coef))
                    for row, r in zip(rows, d.R[i:j])]
        self.rpm = sum(d.R[i:j]) / n
        self.b7 = sum(d.B7[i:j]) / n
        self.cut = sum(d.CUT[i:j]) / n
        self.v = sum(d.V[i:j]) / n
        self.thr = sum(d.THR[i:j]) / n
        oil = [x for x in d.OIL[i:j] if x is not None]
        self.oil = sum(oil) / len(oil) if oil else None

    def deviation(self):
        """{cylinder: rpm of step above the four's mean}, cylscan's wheel
        out and its spread undone. Past about 2,400 rpm the wheel is more
        than cylscan.WHEEL_ALT: only 3 less 2 and 1 less 4 are free of it."""
        order = cylscan.FIRING_ORDER
        p = [self.level[c] - self.level[order[m - 1]]
             for m, c in enumerate(order)]
        alt = cylscan.WHEEL_ALT * self.rpm
        wheel = {1: -alt, 3: alt, 4: -alt, 2: alt}
        return dict(zip(order, cylscan.invert(
            [x - wheel[c] for x, c in zip(p, order)])))

    def steps(self, d):
        """[(stroke's position in the drive, step off the fit)] for the
        strokes whose predecessor was seen too."""
        return [(self.i + m, self.res[m] - self.res[m - 1])
                for m in range(1, self.j - self.i)
                if d.K[self.i + m] - d.K[self.i + m - 1] == 1]


def windows(d):
    out = []
    i, n = 0, len(d.K)
    while i < n:
        if d.SLOT2[i] is None:
            i += 1
            continue
        j = i
        while (j < n and d.SEG[j] == d.SEG[i]
               and d.K[j] < d.K[i] + WINDOW):
            j += 1
        if j - i >= WINDOW_MIN:
            w = Window(d, i, j)
            if w.ok and min(w.cyl.count(c) for c in (1, 2, 3, 4)) >= WINDOW_MIN_CYL:
                out.append(w)
        i = max(j, i + 1)
    return out


def _warm(w):
    return w.oil is not None and w.oil >= WARM_OIL_C


def _standing(w):
    return (w.v * 1e3 <= cylscan.GATE_SPEED_MMH and w.rpm < cylscan.IDLE_RPM[1]
            and w.cut < 0.05)


def _driving(w, rpm, b7):
    return (w.cut < 0.02 and w.v > MOVING_KMH and rpm[0] <= w.rpm < rpm[1]
            and b7[0] <= w.b7 < b7[1])


def _overrun(w, rpm):
    return w.cut > 0.95 and rpm[0] <= w.rpm < rpm[1]


def _mean_se(xs):
    m = sum(xs) / len(xs)
    return m, statistics.pstdev(xs) / math.sqrt(len(xs))


# --- reports -----------------------------------------------------------------

def report_pattern(ws, out=sys.stdout):
    """3 less 2 and 1 less 4, band by band; returns {label: (n, 3-2 in per
    cent, its error, 1-4 in per cent, its error)} for the fired bands."""
    got = {}

    def line(label, sel, per_cent=True):
        sel = [w for w in sel if _warm(w)]
        if len(sel) < MIN_WINDOWS:
            return
        devs = [w.deviation() for w in sel]
        cols = []
        vals = []
        for a, b in ((3, 2), (1, 4)):
            x = [dv[a] - dv[b] for dv in devs]
            m, se = _mean_se(x)
            text = "%+5.2f+-%.2f rpm" % (m, se)
            if per_cent:
                pm, pse = _mean_se([100.0 * v / stroke_rpm(w.rpm, w.b7)
                                    for v, w in zip(x, sel)])
                text += " = %+6.2f+-%.2f %%" % (pm, pse)
                vals += [pm, pse]
            cols.append(text)
        if per_cent:
            got[label] = (len(sel), *vals)
        b7 = sum(w.b7 for w in sel) / len(sel)
        print(f"  {label:26s} {len(sel):5d} windows, b7 {b7:3.0f} | "
              f"3-2: {cols[0]} | 1-4: {cols[1]}", file=out)

    print(f"3 less 2 and 1 less 4, warm, windows of {WINDOW} strokes "
          f"(rpm of step; % of a stroke at that speed and load)", file=out)
    line("standing idle", [w for w in ws if _standing(w)])
    for rb in RPM_BANDS[1:]:
        line("overrun %d-%d" % rb, [w for w in ws if _overrun(w, rb)],
             per_cent=False)
    for rb in RPM_BANDS:
        for bb in B7_BANDS:
            line("%d-%d, b7 %d-%d" % (rb + bb),
                 [w for w in ws if _driving(w, rb, bb)])
    return got


def report_weak(d_ws, out=sys.stdout):
    """`d_ws`: [(Drive, [Window])]. Returns {label: (strokes, under a
    quarter, over a quarter, under a half, over a half, loss in per cent)}."""
    rows = []           # (kind, rpm, b7, step / a stroke, step)
    for d, ws in d_ws:
        for w in ws:
            if not _warm(w):
                continue
            kind = ("idle" if _standing(w) else "cut" if w.cut > 0.95
                    else "drive" if w.cut < 0.02 and w.v > MOVING_KMH else None)
            if kind is None:
                continue
            for m, s in w.steps(d):
                sc = stroke_rpm(d.R[m], max(d.B7[m], 1.0))
                rows.append((kind, d.R[m], d.B7[m], s / sc, s))
    got = {}

    def line(label, sel):
        n = len(sel)
        if n < 2000:
            return
        x = [r[3] for r in sel]
        steps = sorted(r[4] for r in sel)
        med = steps[n // 2]
        sd = 1.4826 * statistics.median(abs(s - med) for s in steps)
        scale = sum(r[4] / r[3] for r in sel if r[3]) / n
        th = 3.0 * sd / scale
        under = -sum(v for v in x if v < -th)
        over = sum(v for v in x if v > th)
        loss = 100.0 * (under - over) / n / cylscan.OWN_SHARE
        c = [sum(1 for v in x if v < -0.25), sum(1 for v in x if v > 0.25),
             sum(1 for v in x if v < -0.5), sum(1 for v in x if v > 0.5)]
        got[label] = (n, *c, loss)
        print(f"  {label:26s} {n:7d} strokes, noise {sd:4.1f} rpm = "
              f"{100 * sd / scale:4.1f} % | a quarter under {1000 * c[0] / n:6.2f}"
              f", over {1000 * c[1] / n:6.2f} | a half under "
              f"{1000 * c[2] / n:5.2f}, over {1000 * c[3] / n:5.2f} per 1000 | "
              f"excess under: {loss:+5.2f} % of the work", file=out)

    print("single strokes against their neighbours, warm: how many read "
          "under and over by a quarter and a half of a stroke", file=out)
    line("standing idle", [r for r in rows if r[0] == "idle"])
    for rb in ((1150, 2100), (2100, 2820), (2820, 4200), (4200, 5640)):
        for bb in B7_BANDS:
            line("%d-%d, b7 %d-%d" % (rb + bb),
                 [r for r in rows if r[0] == "drive"
                  and rb[0] <= r[1] < rb[1] and bb[0] <= r[2] < bb[1]])
    return got


def rises_014(vcds_path, data, d, ws):
    """([rise], [control]): (t, cylinder, the weakest step as a share of a
    stroke, rpm, b7, km/h) for every rise of 014 between two samples with
    recognition on, and for the windows `CONTROL_S` before and after it."""
    g = cutscan.read_vcds(vcds_path).get("014")
    if not g:
        raise SystemExit(f"{vcds_path}: no group 014")
    pts = []
    for t, f in g:
        try:
            pts.append((t, float(f[0]), int(float(f[2])),
                        f[3].startswith("aktiv")))
        except (ValueError, IndexError):
            continue
    off = cylscan.align([(t, r) for t, r, _, _ in pts], data["e"])
    steps = sorted((d.T[m], m, s) for w in ws for m, s in w.steps(d)
                   if w.cut < 0.5)
    st = [x[0] for x in steps]

    def pick(a, b):
        i0, i1 = bisect.bisect_left(st, a), bisect.bisect_left(st, b)
        if i1 - i0 < 5:
            return None
        _, m, s = min(steps[i0:i1], key=lambda x: x[2])
        return (d.T[m], d.cyl(m),
                s / stroke_rpm(d.R[m], max(d.B7[m], 1.0)), d.R[m], d.B7[m],
                d.V[m])

    rises, control = [], []
    for (t0, _, m0, a0), (t1, _, m1, a1) in zip(pts, pts[1:]):
        if not (a0 and a1 and m1 > m0
                and t1 - t0 <= cylscan.VCDS_MAX_GAP_S):
            continue
        a = t0 + off - cylscan.LAG_BEFORE_S
        b = t1 + off - cylscan.LAG_AFTER_S
        p = pick(a, b)
        if p is None:
            continue
        rises.append(p)
        for sh in (-CONTROL_S, CONTROL_S):
            q = pick(a + sh, b + sh)
            if q is not None:
                control.append(q)
    return rises, control


def report_014(rises, control, out=sys.stdout):
    bands = (("standing idle", lambda x: x[5] * 1e3 <= cylscan.GATE_SPEED_MMH
              and x[3] < cylscan.IDLE_RPM[1]),
             ("moving, to 1200 rpm", lambda x: x[5] * 1e3 > cylscan.GATE_SPEED_MMH
              and x[3] <= 1200),
             ("1200-2820, b7 under 45", lambda x: 1200 < x[3] <= 2820 and x[4] < 45),
             ("1200-2820, b7 45 and over", lambda x: 1200 < x[3] <= 2820 and x[4] >= 45),
             ("over 2820 rpm", lambda x: x[3] > 2820))
    print("014's rises by the cylinder of the weakest stroke before each, "
          f"and the same pick {CONTROL_S:.0f} s before and after", file=out)
    got = {}
    for label, f in bands:
        for name, rows in ((label, [x for x in rises if f(x)]),
                           ("  control", [x for x in control if f(x)])):
            n = len(rows)
            cnt = {c: sum(1 for x in rows if x[1] == c) for c in (1, 3, 4, 2)}
            if name == label:
                got[label] = (n, cnt)
            if not n:
                print(f"  {name:26s}    0", file=out)
                continue
            depth = statistics.median(x[2] for x in rows)
            print(f"  {name:26s} {n:4d} | " + "  ".join(
                "%d: %3d (%2.0f %%)" % (c, cnt[c], 100.0 * cnt[c] / n)
                for c in (1, 3, 4, 2))
                + f" | the stroke {100 * depth:+4.0f} % of a stroke", file=out)
    return got


def report_count(path, d, out=sys.stdout):
    slots = "".join(str(x[2]) for x in d.idles)
    segs = sorted(set(x[4] for x in d.idles))
    held = all(len({x[2] for x in d.idles if x[4] == s}) == 1 for s in segs)
    print(f"{os.path.basename(path)}: {len(d.idles)} named idles in "
          f"{len(segs)} engine run(s), cylinder 2 on slot {slots}"
          f" -- {'held' if held else 'SLIPPED'}"
          + ("" if d.sign else "; no parity (timing only)"), file=out)
    return held


def pulls(data):
    """[(pull number, rpm, km/h per 1000 rpm, Nm the acceleration needs,
    Nm b7 claims net of the drag line)] per `PULL_WINDOW_S` of full
    throttle. The car is `CAR_*`: assumed."""
    e, b7 = data["e"], data["b7"]
    out = []
    i, n, number = 0, len(e), 0

    def wot(m):
        return e[m][2] >= PULL_THROTTLE and b7[m] >= PULL_B7

    while i < n:
        if not wot(i):
            i += 1
            continue
        j = i
        while j + 1 < n and wot(j + 1):
            j += 1
        if e[j][0] - e[i][0] >= PULL_MIN_S:
            number += 1
            a = i
            t0 = e[i][0] + PULL_SKIP_S
            while t0 + PULL_WINDOW_S <= e[j][0]:
                while e[a][0] < t0:
                    a += 1
                b = a
                while e[b][0] < t0 + PULL_WINDOW_S:
                    b += 1
                t0 += PULL_WINDOW_S
                if b - a < 50:
                    continue
                ts = [e[m][0] - e[a][0] for m in range(a, b)]
                vs = [e[m][3] / 3600.0 for m in range(a, b)]
                tm, vm = sum(ts) / len(ts), sum(vs) / len(vs)
                acc = (sum((t - tm) * (v - vm) for t, v in zip(ts, vs))
                       / sum((t - tm) ** 2 for t in ts))
                rpm = sum(e[m][1] for m in range(a, b)) / (b - a)
                byte = sum(b7[a:b]) / (b - a)
                if vm < 3.0:
                    continue
                w = rpm * math.pi / 30.0
                ratio = w / vm
                force = ((CAR_MASS_KG + CAR_ENGINE_J * ratio ** 2 * CAR_ETA
                          + CAR_WHEELS_J / CAR_WHEEL_R_M ** 2) * acc
                         + CAR_MASS_KG * 9.81 * CAR_CRR
                         + 0.5 * AIR_KG_M3 * CAR_CDA_M2 * vm * vm)
                need = force * vm / (w * CAR_ETA)
                claim = (byte - DRAG_B7_BASE - DRAG_B7_PER_RPM * rpm) * NM_PER_B7
                out.append((number, rpm, vm * 3.6 / rpm * 1000.0, need, claim))
        i = j + 1
    return out


def report_pulls(rows_by_file, out=sys.stdout):
    """`rows_by_file`: [(name, pulls())]. Returns the median over the pulls
    in 3rd and 4th of each pull's median ratio."""
    print(f"full throttle: the torque the acceleration needs over the torque "
          f"b7 claims ({CAR_MASS_KG:.0f} kg, CdA {CAR_CDA_M2}, assumed)",
          file=out)
    per_pull = {}
    for name, rows in rows_by_file:
        for number, rpm, kph, need, claim in rows:
            gear = 1 + bisect.bisect_right(GEAR_EDGES, kph)
            if claim > 20.0:
                per_pull.setdefault((name, number, gear), []).append(
                    (rpm, need / claim, need, claim))
    for gear in (3, 4, 5):
        for lo in range(2000, 6500, 1000):
            sel = [x for (_, _, g), v in per_pull.items() if g == gear
                   for x in v if lo <= x[0] < lo + 1000]
            if len(sel) < 8:
                continue
            print(f"  gear {gear}, {lo}-{lo + 1000} rpm: {len(sel):3d} s | "
                  f"needs {statistics.median(x[2] for x in sel):4.0f} Nm, "
                  f"b7 claims {statistics.median(x[3] for x in sel):4.0f} Nm, "
                  f"ratio {statistics.median(x[1] for x in sel):.2f}", file=out)
    meds = [statistics.median(x[1] for x in v)
            for (_, _, g), v in per_pull.items() if g in (3, 4)]
    if not meds:
        print("  no pull in 3rd or 4th", file=out)
        return None
    meds.sort()
    q = lambda f: meds[min(int(f * len(meds)), len(meds) - 1)]  # noqa: E731
    print(f"  3rd and 4th, {len(meds)} pulls: median ratio "
          f"{statistics.median(meds):.2f}, half of them {q(0.25):.2f}-"
          f"{q(0.75):.2f}", file=out)
    for name, _ in rows_by_file:
        own = [statistics.median(x[1] for x in v)
               for (nm, _, g), v in per_pull.items() if nm == name and g in (3, 4)]
        if own:
            print(f"    {name}: {len(own)} pulls, {statistics.median(own):.2f}",
                  file=out)
    return statistics.median(meds)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("captures", nargs="+")
    ap.add_argument("--weak", action="store_true",
                    help="single strokes under and over their neighbours")
    ap.add_argument("--vcds", metavar="LOG",
                    help="a VCDS log with group 014 taken beside the (one) capture")
    ap.add_argument("--count", action="store_true",
                    help="the slot of the strongest cylinder at every idle")
    ap.add_argument("--pulls", action="store_true",
                    help="full throttle: acceleration against b7")
    args = ap.parse_args(argv)
    if args.vcds and len(args.captures) != 1:
        ap.error("--vcds reads one capture")
    if args.pulls:
        report_pulls([(os.path.basename(p), pulls(read(p)))
                      for p in args.captures])
        return 0
    ok = True
    d_ws = []
    for p in args.captures:
        data = read(p)
        d = Drive(data)
        if args.count:
            ok = report_count(p, d) and ok
            continue
        ws = windows(d)
        if args.vcds:
            report_014(*rises_014(args.vcds, data, d, ws))
            return 0
        d_ws.append((d, ws))
    if args.count:
        return 0 if ok else 1
    print(", ".join(os.path.basename(p) for p in args.captures) + ":")
    if args.weak:
        report_weak(d_ws)
    else:
        report_pattern([w for _, ws in d_ws for w in ws])
    return 0


if __name__ == "__main__":
    sys.exit(main())
