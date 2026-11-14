#!/usr/bin/env python3
"""014 at a standing idle, log by log -- how much it counted, and how.

docs/engine-health/open.md, S3, *By era*, and S1, *Before and after each
repair*. Written 14/11/2026 after the same reading had twice been made by
a script that was not kept; kept for the reason cylscan.py gives for
itself. cylscan.py --vcds and s3align.py need the capture taken beside a
log; this needs the log alone, so it reads the days with no capture too.

Over every pair of consecutive samples of group 014 at a standing idle --
engine speed within `IDLE_RPM` in both, load under `LOAD_PCT`, detection
`aktivováno` in both, no more than `MAX_GAP_S` apart:

* **misfires**: the counter's rises, divided by `WEIGHT` (one misfire is
  12 at idle; docs/engine-health/vcds.md), so two in one sample count two;
* **share**: misfires per hundred combustions, two a revolution;
* **episodes**: the counter leaving zero; one **climbed** when it went
  past `WEIGHT` before it fell back -- more than one misfire inside the
  ECU's window;
* **the longest silence**: the longest unbroken idle with the counter at
  zero.

⚠ What it does not know: whether the engine was warm (group 001's coolant
is printed where the log has it), whether an injector was cut, and whether
the adaptations were fresh -- a log with a cut reads several per cent, one
on fresh adaptations reads zero (open.md S3). Read the idle-log beside it.
⚠ Not to be compared across the MAF's change of 24/9 (`refuted.md` A11).

    python misfshare.py test/fixtures/vcds/*014*.csv
"""
from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cutscan  # noqa: E402

#: A standing idle by 014's own fields, as s3align.py has it.
IDLE_RPM = (600.0, 1000.0)
#: Below this load the loads are off (docs/engine-health/open.md S3).
LOAD_PCT = 34.0
#: Two samples further apart than this are not one stretch.
MAX_GAP_S = 3.0
#: What one misfire adds to the counter at idle (vcds.md).
WEIGHT = 12.0
#: A log with less idle than this is not printed.
MIN_IDLE_S = 60.0

_MONTHS = {"z": 9, "ř": 10, "l": 11, "p": 12}


def stamp(path):
    """'dd/mm hh:mm' from the log's first line; '' where it does not read.
    The month's name is Czech in cp1250; September to December are told by
    the first letter."""
    try:
        with open(path, encoding="cp1250") as fh:
            h = fh.readline().split(",")
        month = _MONTHS[h[2].strip().lower()[0]]
        return f"{int(h[1]):02d}/{month:02d} {h[4][:5]}"
    except (OSError, IndexError, KeyError, ValueError):
        return ""


def samples(group):
    """[(t, rpm, load, count, active)] from read_vcds()'s group 014; a row
    that does not parse is left out."""
    out = []
    for t, f in group:
        try:
            out.append((t, float(f[0]), float(f[1]), float(f[2]),
                        f[3].startswith("aktiv")))
        except (ValueError, IndexError):
            continue
    return out


def share(pts):
    """The reading of one log's samples, as a dict."""
    idle_s = comb = mis = sil = longest = 0.0
    episodes = climbed = 0
    peak = None                         # the open episode's highest count
    for (t0, r0, _, m0, a0), (t1, r1, ld, m1, a1) in zip(pts, pts[1:]):
        dt = t1 - t0
        ok = (0.0 < dt <= MAX_GAP_S and a0 and a1 and ld < LOAD_PCT
              and IDLE_RPM[0] <= r0 <= IDLE_RPM[1]
              and IDLE_RPM[0] <= r1 <= IDLE_RPM[1])
        if not ok:
            sil, peak = 0.0, None
            continue
        idle_s += dt
        comb += r1 / 30.0 * dt
        if m1 > m0:
            mis += (m1 - m0) / WEIGHT
            if m0 == 0:
                episodes += 1
                peak = 0.0
            if peak is not None:
                if peak <= WEIGHT < m1:
                    climbed += 1
                peak = max(peak, m1)
        if m1 == 0:
            sil += dt
            longest = max(longest, sil)
            peak = None
        else:
            sil = 0.0
    return {"idle_s": idle_s, "misfires": mis,
            "share": 100.0 * mis / comb if comb else math.nan,
            "episodes": episodes, "climbed": climbed, "longest_s": longest}


def coolant(groups):
    """(min, max) of group 001's coolant, or None."""
    v = []
    for _, f in groups.get("001", ()):
        try:
            v.append(float(f[1]))
        except (ValueError, IndexError):
            pass
    return (min(v), max(v)) if v else None


def read(path):
    """share() of a log, with its stamp and coolant; None with no 014."""
    groups = cutscan.read_vcds(path)
    if "014" not in groups:
        return None
    got = share(samples(groups["014"]))
    got["stamp"] = stamp(path)
    got["coolant"] = coolant(groups)
    return got


def report(paths, out=sys.stdout):
    rows = []
    for p in paths:
        try:
            got = read(p)
        except SystemExit:
            got = None
        if got is not None and got["idle_s"] >= MIN_IDLE_S:
            rows.append((got["stamp"][3:5], got["stamp"], os.path.basename(p), got))
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    print("when         idle  misfires  share  episodes  climbed  longest  "
          "coolant    log", file=out)
    print("              min              %     a min        %  silence, min",
          file=out)
    for _, when, name, g in rows:
        m = g["idle_s"] / 60.0
        cl = ("%3.0f-%3.0f" % g["coolant"]) if g["coolant"] else "      -"
        up = 100.0 * g["climbed"] / g["episodes"] if g["episodes"] else math.nan
        print(f"{when:11s} {m:5.1f} {g['misfires']:9.0f} {g['share']:6.2f} "
              f"{g['episodes'] / m:9.1f} "
              + ("       ." if up != up else f"{up:8.0f}")
              + f" {g['longest_s'] / 60.0:8.1f}  {cl}    {name}", file=out)
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("logs", nargs="+")
    args = ap.parse_args(argv)
    report(args.logs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
