"""Ad-hoc: one stroke count from one standing idle through the drive to the
next; does the strongest slot (cylinder 2) land on the same index mod 4?"""
import sys, bisect
sys.path.insert(0, "/home/user/canfuel/tools")
import cylscan

def gslot(ev, t0, t1):
    sub = [x for x in ev if t0 <= x[0] <= t1]
    if len(sub) < 200:
        return None, 0
    r = cylscan.Run(sub)
    return (sub[0][2] + r.slot2) % 4, r.margin

for path in sys.argv[1:]:
    data = cylscan.read(path)
    e = data["e"]; et = [x[0] for x in e]
    runs = [r for r in cylscan.idle_runs(data) if r.named]
    for A, B in zip(runs, runs[1:]):
        i0 = bisect.bisect_left(et, A.T[0]); i1 = bisect.bisect_right(et, B.T[-1])
        seg = e[i0:i1]
        gap = max(b[0] - a[0] for a, b in zip(seg, seg[1:]))
        mid = [x for x in seg if A.T[-1] < x[0] < B.T[0]]
        if not mid:
            continue
        rmax = max(x[1] for x in mid); vmax = max(x[3] for x in mid) / 1e6
        frac_hi = sum(1 for x in mid if x[1] > 2800) / len(mid)
        ev = cylscan.track(e, i0, i1)
        sa, ma = gslot(ev, A.T[0], A.T[-1]); sb, mb = gslot(ev, B.T[0], B.T[-1])
        if sa is None or sb is None:
            continue
        ok = "OK " if sa == sb else "SLIP %+d" % (((sb - sa + 2) % 4) - 2)
        print(f"{path.split('/')[-1][:24]:24} {A.T[-1]-A.T[0]:5.0f}s idle -> "
              f"{B.T[0]-A.T[-1]:5.0f}s drive (max {rmax:4.0f} rpm, {vmax:4.0f} km/h, "
              f">2800 {100*frac_hi:3.0f}%, gap {gap:.2f}s) -> {B.T[-1]-B.T[0]:4.0f}s idle  "
              f"margins {ma:4.1f}/{mb:4.1f}  {ok}")
