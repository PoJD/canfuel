#!/usr/bin/env python3
"""Ignition advance at a steady warm idle, from every VCDS log with group 003.

Written on 17/10/2026 for the owner's question whether the remap's advance
looks aggressive against VW's figure (docs/engine-health/open.md H14), and
kept for the reason idledips.py gives for itself: an ad-hoc script that is
not kept produces numbers nobody can check.

A steady warm idle is `STEADY` consecutive 003 samples at 740-900 rpm with
the throttle plate at 4.5 deg or less -- the same window the plate-angle
table in open.md (H8) uses -- split by air mass, because the A/C adds about
1 g/s and so does a cold engine. 003's fourth field is the advance in deg before TDC; a negative value
is a spark after TDC. VW's figure for block 003 at idle is 0-12 deg BTDC
(docs/engine-health/vcds.md).

    python tools/idleadvance.py                 # every log with 003
    python tools/idleadvance.py LOG.csv [...]
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutscan  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
STEADY = 5
RPM = (740.0, 900.0)
PLATE_MAX = 4.5
AIR_SPLIT = (3.5, 3.6)   # g/s: the A/C or a cold engine puts the air above the second


def steady_advance(path):
    """{"air<=3.5": [deg], "air>=3.6": [deg]} over the steady warm idle of one log."""
    g = cutscan.read_vcds(path).get("003")
    out = {"air<=3.5": [], "air>=3.6": []}
    if not g:
        return out
    pts = []
    for _, x in g:
        try:
            pts.append(tuple(float(v.replace(",", ".")) for v in x[:4]))
        except (ValueError, IndexError):
            continue
    for i in range(STEADY - 1, len(pts)):
        w = pts[i - STEADY + 1:i + 1]
        if not all(RPM[0] <= p[0] <= RPM[1] and p[2] <= PLATE_MAX for p in w):
            continue
        if all(p[1] <= AIR_SPLIT[0] for p in w):
            out["air<=3.5"].append(pts[i][3])
        elif all(p[1] >= AIR_SPLIT[1] for p in w):
            out["air>=3.6"].append(pts[i][3])
    return out


def main(argv=None):
    paths = (argv if argv is not None else sys.argv[1:]) or sorted(
        glob.glob(os.path.join(HERE, "..", "test", "fixtures", "vcds", "*003*.csv")))
    for path in paths:
        for label, v in steady_advance(path).items():
            if len(v) < 20:
                continue
            v.sort()
            n = len(v)
            print("%-42s %-9s n %4d  p10 %5.1f  median %5.1f  p90 %5.1f  after TDC %3.0f%%"
                  % (os.path.basename(path), label, n, v[n // 10], v[n // 2],
                     v[9 * n // 10], 100.0 * sum(x < 0 for x in v) / n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
