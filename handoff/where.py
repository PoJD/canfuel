"""Ad-hoc: where in a drive does the rounding error reach half a stroke?"""
import sys, bisect
sys.path.insert(0, "/home/user/canfuel/tools")
import cylscan
from collections import Counter

def track_err(e, i0, i1, gain=0.05, lead=0.75):
    ts = [x[0] for x in e[i0:i1]]; rs = [x[1] for x in e[i0:i1]]
    n = len(ts); out = []; phi = 0.0; off = None; j = 0
    for i in range(1, n):
        ahead = ts[i] + lead * 30.0 / max(rs[i], 300.0)
        while j + 1 < n and ts[j + 1] <= ahead: j += 1
        dt = min(max(ts[i] - ts[i - 1], 0.0), 0.2)
        phi += rs[max(j, i)] / 30.0 * dt
        if rs[i] != rs[i - 1]:
            if off is None: off = phi
            x = phi - off; k = round(x); out.append((ts[i], rs[i], x - k)); off += gain * (x - k)
    return out

bands = Counter(); risky = Counter()
for path in sys.argv[1:]:
    data = cylscan.read(path); e = data["e"]
    ev = track_err(e, 0, len(e))
    for t, r, err in ev:
        b = int(r // 500) * 500
        bands[b] += 1
        if abs(err) > 0.40: risky[b] += 1
for b in sorted(bands):
    print(f"{b:5d}-{b+499:5d} rpm  changes {bands[b]:8d}  |err|>0.40: {100*risky[b]/bands[b]:6.2f} %")
