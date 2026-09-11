#!/usr/bin/env python3
"""Count transient dips of engine speed against its own one-second median.

This is the measurement behind the idle tables in docs/engine-health.md. It
exists as a tool rather than as a number typed into prose because the first
pass at it was an ad-hoc script that was not kept, and a later reconstruction
of it disagreed with the published counts by two events -- small, but nobody
could tell which of the two was right, which is the whole failure mode the
"numbers in prose" rules in CLAUDE.md are about.

What it measures, and why it is this and not the maximum
--------------------------------------------------------

The symptom is a small event *repeating*, not one large excursion, so the
question is how often engine speed leaves its own recent baseline and by how
much. For every 0x280 frame the median of all samples within +/- 0.5 s is
taken as the baseline, and a sample sitting THRESHOLD rpm or more below it
opens a dip; the dip closes on the first sample that is not. One dip is one
event however many consecutive samples it spans, which is what makes the
counts comparable between logs of different length.

A rolling median rather than a mean or a fixed idle speed: the baseline has to
survive both the warm-up ramp, where idle falls from about 930 to 800 rpm over
five minutes, and the dips themselves. A median of roughly ninety samples does
both, and needs no sort to be defensible -- unlike the firmware, this runs on
a laptop.

Two detectors, and why there are two
------------------------------------

`dips()` is the measurement. `dips_cheap()` asks the same question in a shape
a PIC18F25K80 could answer live -- a first-order baseline, a latch, an idle
gate -- and is the one whose numbers the prediction in docs/engine-health.md
is written against. Its constants are frozen; the comment above them says why,
and it is the only part of this file that must not be re-tuned.

**Nothing in src/ uses either of them, and that is deliberate.** The question
they answer is answered offline over a capture, which the next session records
anyway, so no firmware changes and no display channel is needed to find out
whether the idle got better. Putting the count on the bus is a separate want
with a separate cost, and it waits until the count has been shown to mean
something.

Usage
-----

    python idledips.py                       # the table in engine-health.md
    python idledips.py FILE [FILE ...]       # one line per log
    python idledips.py --from 50 --to 360 FILE
    python idledips.py --thresholds 15,20,25 FILE
"""

from __future__ import annotations

import argparse
import bisect
import os
import statistics
import sys

import canlog

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, os.pardir, "test", "fixtures")

#: The logs the published table is built from, with the window each is read
#: over. None means the whole log. 18 starts after the cold-start flare has
#: settled -- the ramp from 300 to 1450 rpm is not idle and no baseline can
#: describe it.
#:
#: 17 is a drive and is in the table on purpose, as the control. The median
#: detector has no idle gate and reports 72 events a minute over it, which is
#: gearchanges and nothing else; the cheap detector finds 7.7 s of settled idle
#: in six minutes and counts none. Neither number is about combustion -- the
#: row is here so that the difference between "measures idle" and "measures
#: engine speed" stays visible in the output rather than only in this comment.
TABLE = (
    ("09_idle_60s_z1.txt", None, None),
    ("11_idle_noac_z1.txt", None, None),
    ("12_idle_ac_z1.txt", None, None),
    ("17_drive_property_z1.txt", None, None),
    ("18_coldstart_z1.txt", 50.0, 360.0),
)

WINDOW_S = 0.5  # half-width of the median window


def series(path: str):
    """Engine speed, oil and coolant against time in seconds.

    Also returns the samples the cheap detector needs, which is the same 0x280
    stream with the two gate inputs attached: road speed carried forward from
    0x1A0 through its validity rule, and the throttle byte.
    """
    frames = canlog.parse_file(path)
    if not frames or frames[0].ts_ms is None:
        raise SystemExit(
            f"{path}: no adapter timestamps. Only the _z1 logs can be read "
            f"for this -- see test/fixtures/README.md."
        )
    t0 = frames[0].ts_ms
    rpm, oil, clt, gated = [], [], [], []
    speed_mmh = 0
    for f in frames:
        t = (f.ts_ms - t0) / 1000.0
        if f.can_id == 0x1A0 and len(f.data) >= 4:
            # docs/can-decoding.md trap 1: the gate is not an equality.
            if (f.data[1] & 0x40) != 0 and (f.data[1] & 0x03) == 0:
                speed_mmh = (f.data[2] | (f.data[3] << 8)) * 5
        elif f.can_id == 0x280 and len(f.data) >= 8:
            rpm_q4 = f.data[2] | (f.data[3] << 8)
            rpm.append((t, rpm_q4 / 4.0))
            gated.append((t, rpm_q4, f.data[5], speed_mmh))
        elif f.can_id == 0x420 and len(f.data) >= 4:
            oil.append((t, f.data[3] * 0.75 - 48.0))
        elif f.can_id == 0x288 and len(f.data) >= 2:
            clt.append((t, f.data[1] * 0.75 - 48.0))
    return rpm, oil, clt, gated


def dips(rpm, threshold, t_from=None, t_to=None):
    """Dip events: (time of the deepest sample, depth in rpm)."""
    seg = [
        (t, r)
        for t, r in rpm
        if (t_from is None or t >= t_from) and (t_to is None or t < t_to)
    ]
    times = [t for t, _ in seg]
    values = [r for _, r in seg]
    events = []
    inside, deepest, at = False, 0.0, 0.0
    for t, r in seg:
        lo = bisect.bisect_left(times, t - WINDOW_S)
        hi = bisect.bisect_right(times, t + WINDOW_S)
        depth = statistics.median(values[lo:hi]) - r
        if depth >= threshold:
            if not inside:
                inside, deepest, at = True, depth, t
            elif depth > deepest:
                deepest, at = depth, t
        elif inside:
            events.append((at, deepest))
            inside = False
    if inside:
        events.append((at, deepest))
    span = (seg[-1][0] - seg[0][0]) if len(seg) > 1 else 0.0
    return events, span


# --- the cheap detector -----------------------------------------------------
#
# The median detector above is the measurement. This one is the same question
# asked in a shape a PIC18F25K80 could answer in real time, and it exists so
# that the numbers quoted for the next drive are the numbers a firmware would
# produce rather than ones only a laptop can.
#
# ⚠ THESE CONSTANTS ARE FROZEN, and the reason is not superstition. They were
# fitted against one rough engine (09 at 61 C, 18 from cold) and two smooth
# readings of the same engine (11 and 12 at 73 C). New injectors, plugs and
# leads are fitted the week after 18 was recorded, and if they cure the idle
# there will never again be a rough engine to fit anything against -- at which
# point ANY threshold reads zero and a detector tuned to read zero measures
# nothing at all. So they are fixed before the repair, and the reading
# afterwards is taken with them unchanged. docs/engine-health.md carries the
# prediction this pins down.
#
# Every operation is one a PIC18 does cheaply: the shift is 8, which on this
# part is byte selection and therefore free, where a shift of 5 is a rotate
# loop (CLAUDE.md, and docs/optimisation.md). There is no division, no
# multiplication and no loop -- which also means no backward branch for
# tools/cycles.py to have to account for, if it ever does move into src/.

EWMA_SHIFT = 8       # baseline time constant 256/94 Hz = 2.7 s
TRIP_RPM = 20        # a dip opens this far below the baseline
REARM_RPM = 10       # ...and does not re-arm until it comes back this close
SETTLE_S = 3.0       # ignore this long after idle begins; see below
GATE_SPEED_MMH = 100  # STANDSTILL_MMH in src/config.h
GATE_THROTTLE = 38    # THROTTLE_REST in src/config.h


def dips_cheap(gated, t_from=None, t_to=None, shift=EWMA_SHIFT,
               trip_rpm=TRIP_RPM, rearm_rpm=REARM_RPM, settle_s=SETTLE_S):
    """Dip events and settled idle seconds, the way firmware would count them.

    The baseline is a first-order filter rather than a median -- the same
    substitution docs/optimisation.md section 8 made for the tank, and for the
    same reason: "is this sample well below where the signal has been" needs no
    sort. A filter can be dragged down by the dip itself, which a median
    cannot, so the excursion is latched and does not re-arm until engine speed
    has come back within REARM_RPM.

    SETTLE_S is not tidiness either. Coming to a stop, engine speed falls from
    driving speed to idle over a second or two and the lagging baseline reads
    the whole descent as one long dip: without the delay, 17_drive_property_z1
    reports thirteen events in its 25 s of standstill, and with it, none.

    ⚠ **The delay alone is not enough, and the fixtures hide that.** A fixed
    three seconds is shorter than the baseline needs to fall from where the
    gate opens to idle: seeded at the 1054 rpm that is the highest of the 24
    gate openings measured in 17_drive_property_z1, it is still 130 rpm high
    when the delay expires and books one spurious event. **17 does not show
    it only because its stops are too short to reach the delay at all** -- and
    docs/next-drive.md asks for idles of three to five minutes, where every one
    of them would contribute a false count against a prediction of zero. So the
    timer is *restarted* by any excursion past the trip threshold that happens
    before counting has begun: counting starts after SETTLE_S of quiet, not
    SETTLE_S of elapsed time. It costs one comparison that is already computed.
    """
    trip = int(trip_rpm * 4)        # samples are in 0.25 rpm units, as on the bus
    rearm = int(rearm_rpm * 4)
    base = None
    armed = True
    idle_since = None
    prev_t = None
    idle_s = 0.0
    events = []
    for t, rpm_q4, throttle, speed_mmh in gated:
        if (t_from is not None and t < t_from) or (t_to is not None and t >= t_to):
            continue
        if speed_mmh > GATE_SPEED_MMH or throttle > GATE_THROTTLE or rpm_q4 == 0:
            base, armed, idle_since, prev_t = None, True, None, None
            continue
        if idle_since is None:
            idle_since = t
        if base is None:
            base = rpm_q4 << shift
        baseline = base >> shift
        below = baseline - rpm_q4
        settled = (t - idle_since) >= settle_s
        if not settled and below >= trip:
            idle_since = t              # not quiet yet -- start the delay again
        if settled:
            if prev_t is not None:
                idle_s += t - prev_t
            if armed and below >= trip:
                events.append((t, below / 4.0))
                armed = False
            elif not armed and below <= rearm:
                armed = True
        prev_t = t
        base += rpm_q4 - baseline
    return events, idle_s


def _last(seq, t):
    vals = [v for tt, v in seq if tt <= t]
    return vals[-1] if vals else float("nan")


def report(path, thresholds, t_from, t_to, label=None):
    rpm, oil, clt, gated = series(path)
    counts, span = [], 0.0
    for thr in thresholds:
        ev, span = dips(rpm, thr, t_from, t_to)
        counts.append(ev)
    cheap, idle_s = dips_cheap(gated, t_from, t_to)
    seg = [
        r
        for t, r in rpm
        if (t_from is None or t >= t_from) and (t_to is None or t < t_to)
    ]
    end = t_to if t_to is not None else rpm[-1][0]
    cells = "  ".join(
        "%4d (%5.1f/min)" % (len(ev), len(ev) * 60 / span if span else 0)
        for ev in counts
    )
    cells += "  | %4d (%5.1f/min) in %5.1fs" % (
        len(cheap), len(cheap) * 60 / idle_s if idle_s > 1 else 0.0, idle_s)
    print(
        "%-26s %6.1fs  %5.0f rpm  %s  oil %5.2f  clt %6.2f"
        % (
            label or os.path.basename(path),
            span,
            sum(seg) / len(seg) if seg else 0,
            cells,
            _last(oil, end),
            _last(clt, end),
        )
    )
    return counts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="logs to read (default: the table)")
    ap.add_argument("--thresholds", default="20,15", help="rpm, comma separated")
    ap.add_argument("--from", dest="t_from", type=float, default=None)
    ap.add_argument("--to", dest="t_to", type=float, default=None)
    args = ap.parse_args(argv)

    thresholds = [int(x) for x in args.thresholds.split(",")]
    header = "  ".join("%15s" % ("dips >=%d rpm" % t) for t in thresholds)
    print("%-26s %7s  %9s  %s  | %s"
          % ("log", "span", "mean", header, "cheap detector, over settled idle"))

    if args.files:
        for path in args.files:
            report(path, thresholds, args.t_from, args.t_to)
    else:
        for name, lo, hi in TABLE:
            report(os.path.join(FIXTURES, name), thresholds, lo, hi)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
