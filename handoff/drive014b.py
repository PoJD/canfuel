"""Phase 2: the rises put to cylinders (reads caps.pkl, pairs.pkl)."""
import sys, os, pickle, bisect, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive014 import *

D = pickle.load(open(f"{SCR}/caps.pkl", "rb"))
pairs = pickle.load(open(f"{SCR}/pairs.pkl", "rb"))
NAMES = (2, 1, 3, 4)
res = {"idle": [], "drive": [], "ctrl": [], "drive_unnamed": 0, "drive_hi": 0, "drive_nostretch": 0}
cons = []      # stretches with 2+ idles: agree?
blind = []     # driving part's strongest detrended slot vs the idle's name
prepared = {}
for l, c, off, err in pairs:
    data = D[c]; e = data["e"]; et = [x[0] for x in e]
    if c not in prepared:
        idles = cylscan.idle_runs(data)
        sts = []
        for i0, i1 in stretches(e):
            ev, s2, nid, agree = named_stretch(data, i0, i1, idles)
            if len(ev) < 300: continue
            k0, T, R, E = residuals(ev)
            sums, cnt = [0.0]*4, [0]*4
            for q in range(1, len(R)):
                sums[(k0 + q) % 4] += R[q] - R[q-1]; cnt[(k0 + q) % 4] += 1
            mm = [a/b if b else -1e9 for a, b in zip(sums, cnt)]
            o = sorted(range(4), key=lambda q: mm[q])
            blind_slot = o[-1] if min(cnt) > 500 else None
            blind_margin = mm[o[-1]] - mm[o[-2]]
            sts.append(dict(t0=e[i0][0], t1=e[i1-1][0], s2=s2, nid=nid, agree=agree,
                            k0=k0, T=T, R=R, E=E, blind=blind_slot, bm=blind_margin, idles=[r for r in idles if r.T[0] >= e[i0][0] and r.T[-1] <= e[i1-1][0]]))
            if nid >= 2: cons.append((os.path.basename(c), nid, agree))
            if s2 is not None:
                # blind naming from the driving part alone
                sums, cnt = [0.0]*4, [0]*4
                for i in range(1, len(R)):
                    t = T[i]
                    if any(r.T[0] - 2 <= t <= r.T[-1] + 2 for r in sts[-1]["idles"]): continue
                    if R[i] > 1100 or True:
                        s = R[i] - R[i-1]
                        sums[(k0 + i) % 4] += s; cnt[(k0 + i) % 4] += 1
                if min(cnt) > 500:
                    m = [a/b for a, b in zip(sums, cnt)]
                    blind.append((m.index(max(m)) == s2, sorted(m)[-1] - sorted(m)[-2]))
        prepared[c] = sts
    sts = prepared[c]
    pts = vcds014(l)
    for (t0, r0, ld0, m0, a0), (t1, r1, ld1, m1, a1) in zip(pts, pts[1:]):
        if not (a0 and a1 and m1 > m0 and t1 - t0 <= 2.5):
            continue
        a, b = t0 + off - 0.30, t1 + off - 0.12
        i = bisect.bisect_right(et, b) - 1
        if i < 0: continue
        standing = e[i][3] <= cylscan.GATE_SPEED_MMH and max(r0, r1) <= 1000
        st = next((s for s in sts if s["t0"] <= a - 3 and b + 3 <= s["t1"]), None)
        if st is None:
            if not standing:
                if max(r0, r1) > RPM_MAX - 200: res["drive_hi"] += 1
                else: res["drive_nostretch"] += 1
            continue
        how = "idle-named"
        if st["s2"] is None or not st["agree"]:
            if standing or st["blind"] is None:
                if not standing: res["drive_unnamed"] += 1
                continue
            st = dict(st, s2=st["blind"]); how = "blind"
        def pick(a, b):
            ia, ib = bisect.bisect_left(st["T"], a), bisect.bisect_left(st["T"], b)
            idx = [j for j in range(ia, ib) if st["E"][j] is not None]
            if len(idx) < 5: return None
            j = min(idx, key=lambda q: st["E"][q])
            return NAMES[(st["k0"] + j - st["s2"]) % 4], st["E"][j], st["R"][j]
        p = pick(a, b)
        if p is None: continue
        rec = (os.path.basename(c), t1 + off, p[0], p[1], p[2], (m1 - m0), ld1, how)
        res["idle" if standing else "drive"].append(rec)
        if not standing:
            for sh in (-5.0, 5.0):
                q = pick(a + sh, b + sh)
                if q: res["ctrl"].append((os.path.basename(c), 0, q[0], q[1], q[2], 0, 0, how))
pickle.dump(res, open(f"{SCR}/res.pkl", "wb"))

def table(name, recs, depth=None):
    rr = [r for r in recs if depth is None or r[3] <= -depth]
    cnt = {k: sum(1 for r in rr if r[2] == k) for k in (1, 3, 4, 2)}
    n = len(rr) or 1
    print(f"{name:34s} n={len(rr):4d}  " + "  ".join(f"{k}: {cnt[k]:4d} ({100*cnt[k]/n:3.0f}%)" for k in (1, 3, 4, 2)))

print("stretches with 2+ idles, names agree:", sum(1 for x in cons if x[2]), "of", len(cons))
print("blind naming from driving part == idle name:", sum(1 for x in blind if x[0]), "of", len(blind))
print("driving rises: in a named stretch", len(res["drive"]), "| stretch unnamed", res["drive_unnamed"],
      "| near/above", RPM_MAX - 200, "rpm", res["drive_hi"], "| other (gap, short)", res["drive_nostretch"])
table("standing idle (check vs earlier)", res["idle"])
table("driving, all", res["drive"])
table("driving, idle-named", [r for r in res["drive"] if r[7] == "idle-named"])
table("driving, blind-named", [r for r in res["drive"] if r[7] == "blind"])
table("  control, blind-named", [r for r in res["ctrl"] if r[7] == "blind"])
print("blind margins (rpm) of the named stretches' check:", sorted(round(x[1]) for x in blind)[:5])
table("driving, weakest <= -8 rpm", res["drive"], 8)
table("driving, weakest <= -12 rpm", res["drive"], 12)
table("control (+-5 s), all", res["ctrl"])
table("control, weakest <= -8 rpm", res["ctrl"], 8)
table("control, weakest <= -12 rpm", res["ctrl"], 12)
d = [r[3] for r in res["drive"]]; cc = [r[3] for r in res["ctrl"]]
if d and cc:
    print("median depth of weakest stroke: rises %.1f rpm, control %.1f rpm" % (statistics.median(d), statistics.median(cc)))
for lo, hi in ((500, 1200), (1200, 1800), (1800, 2700)):
    table(f"driving {lo}-{hi} rpm", [r for r in res["drive"] if lo <= r[4] < hi])
    table(f"  control {lo}-{hi} rpm", [r for r in res["ctrl"] if lo <= r[4] < hi])
by = {}
for r in res["drive"]:
    by.setdefault(r[0], []).append(r)
for k in sorted(by):
    table("  " + k, by[k])
