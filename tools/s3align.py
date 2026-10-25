#!/usr/bin/env python3
"""Do 014's misfire counts sit on the idle dips -- S1 against S3, in time.

docs/engine-health/open.md S3 (*The events are the S1 dips*) first answered
this on three logs of September. Written on 16/10/2026 for the owner's
question whether it still holds on every capture since, after he watched
014 sit at zero for minutes with the A/C on while `IdleHealth` read 70, and
start counting with the A/C off while `IdleHealth` did not move. Kept as a
tool for the reason idledips.py gives for itself: an ad-hoc script that is
not kept produces numbers nobody can check.

Every capture with a VCDS log of group 014 beside it (`PAIRS`) is put on
one clock (`cutscan.align`, on engine speed; a log that does not line up is
reported and skipped). Then, over standing idle only -- 014's engine speed
at 600-1000 rpm in two consecutive samples, detection `aktivováno`, road
speed zero, the injector cuts left out:

* **a rise** is a 014 sample whose count is above the one before (the
  counter steps by 12 and falls back to zero on its own, so a rise is the
  event, not the value);
* **a dip** is `idledips.dips()` at `DIP_RPM`.

Three readings:

``--lag``      dips per sample in half-second bins of (rise sample - dip),
               for samples that rose and samples that did not. Where the
               two differ is where 014 reports a dip.
default        per capture: the share of rises with a dip in the
               `NEAR_S` before them, against the share of other samples
               (one-sided binomial p); and the share of dips followed by a
               rise within `NEAR_S`, against random idle moments.
``--windows``  `WINDOW_S` stretches of continuous active idle (or
               ``--window-s``): rises a minute, dips a minute and
               `IdleHealth` (`idledips --roughness` x 50), with Spearman's
               rank correlation between each pair; then, warm and on the
               new MAF, by `IdleHealth` band in three groups -- fresh
               adaptations (`FRESH`), settled ones, and loads on (014's
               load above `LOAD_PCT`), which have to be read apart
               (docs/firmware/open.md 11, *Re-read in stretches*).
"""
import argparse
import bisect
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutscan  # noqa: E402
import idledips  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "..", "test", "fixtures")

#: Captures and the 014 logs taken beside them. A log that spans two
#: captures is listed under both and lines up with one.
PAIRS = (
    ("18_coldstart_z1.txt", ("vcds-coldstart-014-055.csv",)),
    ("19_postfix_drive_z1.txt", ("vcds-postfix-drive-003-014.csv",)),
    ("24_mafswap_drive_z1.txt", ("vcds-mafswap-002-014.csv",)),
    ("25_sessionA_cold_z1.txt", ("vcds-sessionA-003-014-055.csv",)),
    ("26_sessionA_warm_z1.txt", ("vcds-sessionA-003-014-055.csv",)),
    ("27_sessionA2_cold_z1.txt", ("vcds-sessionA2-003-014-055.csv",)),
    ("28_sessionA2_warm_z1.txt", ("vcds-sessionA2-hot-003-014-055.csv",
                                  "vcds-sessionA2-003-014-055.csv")),
    ("29_sessionB_z1.txt", ("vcds-sessionB-014-055-033.csv",)),
    ("30_step2b_z1.txt", ("vcds-step2b-014-055-033.csv",
                          "vcds-step2b-a3-014-055-003.csv",
                          "vcds-step2c-home-014-055-003.csv")),
    ("31_step4_drive_z1.txt", ("vcds-step4-014-003-020.csv",
                               "vcds-step5-014-055-003.csv")),
    ("32_step3_item1_z1.txt", ("vcds-step3-1-idle128-014-056-055.csv",
                               "vcds-step3-1-idle130-014-056-055.csv",
                               "vcds-step3-1-idle132-014-056-055.csv",
                               "vcds-step3-1-idle133-014-056-055.csv",
                               "vcds-step3-1-idle133b-014-056-055.csv",
                               "vcds-step3-1-back128-014-056.csv",
                               "vcds-step3-1-drive-014-001-020.csv")),
    ("35_item5_drive_z1.txt", ("vcds-item5-drive-014-001-003-1.csv",)),
    ("36_item5_drive2_z1.txt", ("vcds-item5-drive-014-001-003-2.csv",)),
    ("37_item5_drive3_z1.txt", ("vcds-item5-drive3-014-001-003.csv",)),
    ("39_drive_home_z1.txt", ("vcds-drive-home-014-001-003-1.csv",
                              "vcds-drive-home-014-001-003-2.csv")),
    ("40_refit_drive_z1.txt", ("vcds-step6b-drive-014-001-003.csv",
                               "vcds-step6b-drive-014-020-003.csv",
                               "vcds-step6b-drive-2-014-001-003.csv")),
)

#: Before the MAF of 24/9: 014 measured with another ruler (refuted.md A11),
#: so --windows leaves these out of its tables.
OLD_MAF = ("18_coldstart_z1.txt", "19_postfix_drive_z1.txt")
#: On fresh adaptations -- the battery was disconnected repeatedly until the
#: morning of 4/10 and has stayed connected since (vehicle-history.md). The
#: learned idle air decides whether 014 counts at all (refuted.md C19), so
#: --windows reads these apart from the captures since.
FRESH = ("24_mafswap_drive_z1.txt", "25_sessionA_cold_z1.txt",
         "26_sessionA_warm_z1.txt", "27_sessionA2_cold_z1.txt",
         "28_sessionA2_warm_z1.txt", "29_sessionB_z1.txt")

DIP_RPM = 20.0     #: the dip threshold S1's tables use
NEAR_S = 1.5       #: the lag window --lag finds: 0-1.5 s from dip to rise
WINDOW_S = 60.0    #: --windows stretch length
CUT_PAD_S = 5.0    #: margin around an injector cut
MAX_GAP_S = 2.5    #: two 014 samples further apart are not one interval
LOAD_PCT = 28.0    #: --windows: above this mean 014 load a stretch is loads on
OIL_C = 85.0       #: --windows: the bands table reads warm stretches only


def _at(pairs, keys, t, default=None):
    i = bisect.bisect_right(keys, t) - 1
    return pairs[i][1] if i >= 0 else default


def load(dip_rpm=DIP_RPM):
    """[(capture, intervals, dips, gated)]: intervals are
    (t0, t1, rose, oil, load %, count)."""
    out = []
    for cap, logs in PAIRS:
        rpm, oil, _, gated = idledips.series(os.path.join(FIX, cap))
        cuts = cutscan.find_cuts(cutscan.stroke_runs(gated))
        dips = sorted(t for t, _ in idledips.dips(rpm, dip_rpm)[0])
        gt = [g[0] for g in gated]
        spd = [(g[0], g[3]) for g in gated]
        ot = [t for t, _ in oil]
        iv = []
        for lg in logs:
            g = cutscan.read_vcds(os.path.join(FIX, "vcds", lg)).get("014")
            if not g:
                continue
            pts = []
            for t, f in g:
                try:
                    pts.append((t, float(f[0]), int(float(f[2])), f[3],
                                float(f[1])))
                except (ValueError, IndexError):
                    continue
            try:
                off = cutscan.align([(t, r) for t, r, *_ in pts], rpm)
            except SystemExit as e:
                print("%s + %s: skipped, %s" % (cap, lg, e), file=sys.stderr)
                continue
            for (t0, r0, m0, s0, _), (t1, r1, m1, s1, l1) in zip(pts, pts[1:]):
                a, b = t0 + off, t1 + off
                if not (600 <= r0 <= 1000 and 600 <= r1 <= 1000):
                    continue
                if not s1.startswith("aktiv") or not s0.startswith("aktiv"):
                    continue
                if b - a > MAX_GAP_S or a < rpm[0][0] or b > rpm[-1][0]:
                    continue
                if _at(spd, gt, a, 0) > 100 or _at(spd, gt, b, 0) > 100:
                    continue
                if any(x - CUT_PAD_S <= t <= y + CUT_PAD_S
                       for x, y in cuts for t in (a, b)):
                    continue
                iv.append((a, b, m1 > m0, _at(oil, ot, b), l1, m1))
        iv.sort()
        out.append((cap, iv, dips, gated))
    return out


def _dip_before(dips, t):
    i = bisect.bisect_left(dips, t - NEAR_S)
    return i < len(dips) and dips[i] <= t


def binom_tail(k, n, p):
    """P(X >= k) for X ~ Bin(n, p)."""
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j)
               for j in range(k, n + 1))


def lag_table(data):
    bins = [-6 + 0.5 * i for i in range(28)]
    hist = {True: [0] * len(bins), False: [0] * len(bins)}
    n = {True: 0, False: 0}
    for _, iv, dips, _ in data:
        for a, b, rose, *_ in iv:
            n[rose] += 1
            i = bisect.bisect_left(dips, b - 8)
            while i < len(dips) and dips[i] <= b + 6:
                j = int((b - dips[i] + 6) // 0.5)
                if 0 <= j < len(bins):
                    hist[rose][j] += 1
                i += 1
    print("lag = 014 sample showing the rise - dip; dips per sample per bin")
    print("  lag    rose  did not  ratio")
    for j, lag in enumerate(bins):
        r = hist[True][j] / max(n[True], 1)
        q = hist[False][j] / max(n[False], 1)
        print("%5.1f  %6.3f  %6.3f  %5.2f" % (lag, r, q, r / q if q else float("nan")))


def timing_table(data, seed=1):
    rnd = random.Random(seed)
    print("%-4s %6s %16s %16s %8s %6s %16s %8s" % (
        "cap", "rises", "with a dip", "others with one", "p", "dips",
        "rise after", "random"))
    tot = [0, 0, 0, 0, 0, 0]
    for cap, iv, dips, _ in data:
        if not iv:
            continue
        rises = [b for a, b, r, *_ in iv if r]
        others = [b for a, b, r, *_ in iv if not r]
        k = sum(_dip_before(dips, b) for b in rises)
        q = sum(_dip_before(dips, b) for b in others)
        ends = [b for _, b, *_ in iv]

        def rise_after(t):
            i = bisect.bisect_right(ends, t)
            while i < len(ends) and ends[i] <= t + NEAR_S:
                if iv[i][2]:
                    return True
                i += 1
            return False

        def covered(t):
            i = bisect.bisect_right(ends, t)
            return i < len(iv) and iv[i][0] <= t

        cd = [d for d in dips if covered(d)]
        f = sum(rise_after(d) for d in cd)
        base = sum(rise_after(rnd.uniform(a, b))
                   for a, b, *_ in (rnd.choice(iv) for _ in range(5000))) / 5000
        pq = q / len(others) if others else 0.0
        p = binom_tail(k, len(rises), pq) if rises else float("nan")
        print("%-4s %6d %8d (%3.0f%%) %8d (%3.0f%%) %8.1e %6d %8d (%3.0f%%) %6.0f%%" % (
            cap[:2], len(rises), k, 100 * k / max(len(rises), 1), q, 100 * pq,
            p, len(cd), f, 100 * f / max(len(cd), 1), 100 * base))
        for i, x in enumerate((len(rises), k, len(others), q, len(cd), f)):
            tot[i] += x
    print("all: %d rises, %d (%.0f%%) with a dip in the %.1f s before, against "
          "%.0f%% of other samples; %d dips, %d (%.0f%%) followed by a rise" % (
              tot[0], tot[1], 100 * tot[1] / tot[0], NEAR_S,
              100 * tot[3] / tot[2], tot[4], tot[5], 100 * tot[5] / tot[4]))


def _rank(x):
    s = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and x[s[j + 1]] == x[s[i]]:
            j += 1
        for k in range(i, j + 1):
            r[s[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = _rank(a), _rank(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else float("nan")


def windows(data, window_s=WINDOW_S):
    rows = []
    for cap, iv, dips, gated in data:
        cur = []

        def flush():
            if not cur:
                return
            a, b = cur[0][0], cur[-1][1]
            if b - a < window_s - 10:
                return
            g = idledips.roughness(gated, a, b)[0]
            if g is None:
                return
            nd = bisect.bisect_left(dips, b) - bisect.bisect_left(dips, a)
            rows.append((cap[:2], 60 * sum(x[2] for x in cur) / (b - a),
                         60 * nd / (b - a), 50 * g, cur[-1][3],
                         sum(x[4] for x in cur) / len(cur),
                         sum(x[5] > 0 for x in cur) / len(cur), cap))

        for x in iv:
            if cur and (x[0] - cur[-1][1] > 1.0 or x[1] - cur[0][0] > window_s):
                flush()
                cur = []
            cur.append(x)
        flush()
    print("%d stretches of %.0f s of active standing idle" % (len(rows), window_s))
    for name, i, j in (("rises/min vs IdleHealth", 1, 3),
                       ("rises/min vs dips/min", 1, 2),
                       ("dips/min vs IdleHealth", 2, 3)):
        print("  Spearman %-24s %5.2f" % (name, spearman([r[i] for r in rows],
                                                          [r[j] for r in rows])))
    warm = [r for r in rows if r[4] is not None and r[4] >= 90]
    for label, sel in (("014 silent", [r[3] for r in warm if r[1] == 0]),
                       ("014 counting", [r[3] for r in warm if r[1] > 0])):
        if sel:
            sel.sort()
            print("  oil >= 90 C, %-12s n=%3d  IdleHealth median %3.0f, %3.0f-%3.0f" % (
                label, len(sel), sel[len(sel) // 2], sel[0], sel[-1]))
    # By IdleHealth band, the old MAF and the cold left out, loads on apart:
    # the load alone both lowers the grade and stops 014 counting, so mixed
    # in it reads as a threshold of the grade.
    use = [r for r in rows if r[7] not in OLD_MAF
           and r[4] is not None and r[4] >= OIL_C]
    for label, sel in (
            ("fresh adaptations, to 4/10",
             [r for r in use if r[7] in FRESH and r[5] <= LOAD_PCT]),
            ("settled adaptations, since 4/10",
             [r for r in use if r[7] not in FRESH and r[5] <= LOAD_PCT]),
            ("loads on, load > %.0f %%" % LOAD_PCT,
             [r for r in use if r[5] > LOAD_PCT])):
        if len(sel) < 4:
            continue
        print("oil >= %.0f C, %s: %d stretches, Spearman rises vs IdleHealth %.2f" % (
            OIL_C, label, len(sel), spearman([r[1] for r in sel], [r[3] for r in sel])))
        print("  IdleHealth    n  silent  samples counting  rises/min")
        for lo, hi in ((0, 55), (55, 70), (70, 80), (80, 100), (100, 999)):
            b = [r for r in sel if lo <= r[3] < hi]
            if b:
                print("  %3d-%-4d %6d %6.0f%% %12.0f%% %12.2f" % (
                    lo, hi, len(b), 100 * sum(r[1] == 0 for r in b) / len(b),
                    100 * sum(r[6] for r in b) / len(b),
                    sum(r[1] for r in b) / len(b)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lag", action="store_true")
    ap.add_argument("--windows", action="store_true")
    ap.add_argument("--dip-rpm", type=float, default=DIP_RPM)
    ap.add_argument("--window-s", type=float, default=WINDOW_S)
    args = ap.parse_args(argv)
    data = load(args.dip_rpm)
    if args.lag:
        lag_table(data)
    elif args.windows:
        windows(data, args.window_s)
    else:
        timing_table(data)


if __name__ == "__main__":
    main()
