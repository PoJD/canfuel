"""Ad-hoc: 014's rises while driving, put to a cylinder where one stroke
count runs unbroken (rpm <= RPM_MAX, no gap) from a named standing idle."""
import sys, os, glob, bisect, pickle, statistics, random
import numpy as np
sys.path.insert(0, "/home/user/canfuel/tools")
import cylscan, cutscan

RPM_MAX = 2700.0
SCR = os.path.dirname(os.path.abspath(__file__))
FIX = "/home/user/canfuel/test/fixtures"

def vcds014(path):
    g = cutscan.read_vcds(path).get("014")
    pts = []
    for t, f in g or []:
        try:
            pts.append((t, float(f[0]), float(f[1]), int(float(f[2])), f[3].startswith("aktiv")))
        except (ValueError, IndexError):
            pass
    return pts

def np_align(pts, e):
    ct = np.array([x[0] for x in e]); cr = np.array([x[1] for x in e])
    vt = np.array([p[0] for p in pts]); vr = np.array([p[1] for p in pts])
    best = (1e9, None)
    for off in np.arange(-vt[-1], ct[-1], 0.5):
        tt = vt + off
        m = (tt >= ct[0]) & (tt <= ct[-1])
        if m.sum() < 0.6 * len(vt):
            continue
        i = np.searchsorted(ct, tt[m], side="right") - 1
        err = np.abs(cr[i] - vr[m]).mean()
        if err < best[0]:
            best = (err, off)
    if best[1] is None:
        return best
    # fine
    err0, c = best
    for off in np.arange(c - 1, c + 1.001, 0.05):
        tt = vt + off; m = (tt >= ct[0]) & (tt <= ct[-1])
        i = np.searchsorted(ct, tt[m], side="right") - 1
        err = np.abs(cr[i] - vr[m]).mean()
        if err < best[0]:
            best = (err, off)
    return best

def stretches(e):
    """(i0, i1) of stretches with rpm in 500..RPM_MAX and no gap > 0.1 s."""
    out, i, n = [], 0, len(e)
    while i < n:
        if not (500 <= e[i][1] <= RPM_MAX):
            i += 1; continue
        j = i + 1
        while j < n and 500 <= e[j][1] <= RPM_MAX and e[j][0] - e[j-1][0] <= 0.1:
            j += 1
        if e[j-1][0] - e[i][0] > 20:
            out.append((i, j))
        i = j
    return out

def named_stretch(data, i0, i1, idles):
    """global events, the global slot of cylinder 2 (or None), how many idles
    named it and whether they agreed."""
    e = data["e"]
    ev = cylscan.track(e, i0, i1)
    t0, t1 = e[i0][0], e[i1-1][0]
    slots = []
    for r in idles:
        if r.T[0] >= t0 and r.T[-1] <= t1:
            sub = [x for x in ev if r.T[0] <= x[0] <= r.T[-1]]
            if len(sub) < 200: continue
            rr = cylscan.Run(sub)
            if rr.named:
                slots.append((sub[0][2] + rr.slot2) % 4)
    if not slots:
        return ev, None, 0, True
    agree = len(set(slots)) == 1
    return ev, statistics.mode(slots), len(slots), agree

def residuals(ev):
    """{stroke index: (t, rpm, E)}: each step against the median of its own
    slot's steps in +-6 cycles."""
    k0 = ev[0][2]; n = ev[-1][2] - k0 + 1
    R = [None]*n; T = [None]*n
    for t, r, k in ev:
        R[k-k0] = r; T[k-k0] = t
    for i in range(1, n):
        if R[i] is None:
            R[i] = R[i-1]; T[i] = T[i-1] + 30.0/R[i-1]
    S = [None] + [R[i]-R[i-1] for i in range(1, n)]
    E = [None]*n
    for i in range(1, n):
        nb = [S[i+4*m] for m in range(-6, 7) if m and 1 <= i+4*m < n]
        if len(nb) >= 8:
            E[i] = S[i] - statistics.median(nb)
    return k0, T, R, E

def main():
    caps = sorted(glob.glob(f"{FIX}/[2-5][0-9]_*_z1.txt"))
    logs = sorted(glob.glob(f"{FIX}/vcds/*014*.csv"))
    cache = f"{SCR}/caps.pkl"
    D = pickle.load(open(cache, "rb")) if os.path.exists(cache) else {}
    for c in caps:
        if c not in D:
            try: D[c] = cylscan.read(c)
            except SystemExit: D[c] = None
    pickle.dump(D, open(cache, "wb"))
    pairs = []
    for l in logs:
        pts = vcds014(l)
        if len(pts) < 100: continue
        rs = [p[1] for p in pts]
        if statistics.pstdev(rs) < 150 or max(rs) < 1500:   # idle-only logs do not align by rpm
            continue
        best = None
        for c in caps:
            if D[c] is None or not D[c]["e"]: continue
            err, off = np_align(pts, D[c]["e"])
            if off is not None and (best is None or err < best[0]):
                best = (err, off, c)
        if best and best[0] < 30:
            pairs.append((l, best[2], best[1], best[0]))
            print(f"# {os.path.basename(l):42s} -> {os.path.basename(best[2]):26s} off {best[1]:8.2f}  err {best[0]:5.1f} rpm", flush=True)
        else:
            print(f"# {os.path.basename(l):42s} no match ({best and round(best[0])})", flush=True)
    pickle.dump(pairs, open(f"{SCR}/pairs.pkl", "wb"))

if __name__ == "__main__":
    main()
