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

Three instruments, and why there are three
------------------------------------------

`dips()` is the measurement. `dips_cheap()` asks the same question in a shape
a PIC18F25K80 could answer live -- a first-order baseline, a latch, an idle
gate -- and is the one whose numbers the prediction in docs/engine-health.md
is written against.

`roughness()` does not count at all. It GRADES the idle, because a count past
a threshold has no resolution below the threshold and a repaired engine reads
zero for ever -- `--roughness --bands` shows that the band carrying the
contrast is 10-20 rpm, just under TRIP_RPM. It is the instrument
docs/next-drive.md question 6 proposes putting on the bus.

Both sets of constants are frozen; the comments above them say why, and they
are the only parts of this file that must not be re-tuned.

**Nothing in src/ uses either of them, and that is deliberate.** The question
they answer is answered offline over a capture, which the next session records
anyway, so no firmware changes and no display channel is needed to find out
whether the idle got better. Putting the count on the bus is a separate want
with a separate cost, and it waits until the count has been shown to mean
something.

That want is written down as question 6 of docs/next-drive.md, and if it is
built, `dips_cheap()` becomes the oracle the C detector is checked against --
event for event over the logs in TABLE, exactly, the way tools/replay.py is
the oracle for the rest of the core. Two things would have to hold and both
are easy to get wrong: the firmware steps the detector once per 0x280 FRAME
including the frames that repeat a value (EWMA_SHIFT is a time constant only
under that reading), and the settle timer restarts on an excursion rather than
merely elapsing. The docstring of `dips_cheap()` has the measurement behind
the second.

Usage
-----

    python idledips.py                       # the table in engine-health.md
    python idledips.py FILE [FILE ...]       # one line per log
    python idledips.py --from 50 --to 360 FILE
    python idledips.py --thresholds 15,20,25 FILE
    python idledips.py --depths FILE          # how deep each dip was
    python idledips.py --segments             # the update rate of 0x280's rpm
    python idledips.py --roughness            # grade the idle instead
    python idledips.py --roughness --hist     # ...the raw material, as a shape
    python idledips.py --roughness --bands    # ...where the grade comes from
    python idledips.py --roughness --deadbands  # ...the contrast against it
    python idledips.py --roughness --windows 60 FILE
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


def depths(rpm, threshold, t_from=None, t_to=None):
    """The depth of every dip, deepest first. The counts say how often the
    engine stumbles; this says how hard, which is what the energy argument in
    docs/engine-health.md is written against."""
    ev, span = dips(rpm, threshold, t_from, t_to)
    return sorted((d for _, d in ev), reverse=True), span


#: Engine speed on 0x280 does not change every frame. These are the bands the
#: interval between changes is reported over, against the firing interval of a
#: four-stroke four at the middle of each -- see segments() below.
SEGMENT_BANDS = ((700, 900), (900, 1200), (1200, 1800), (1800, 2600), (2600, 4000))

CYLINDERS = 4  # firing events per two revolutions


def firing_interval_s(rpm_value):
    """Seconds between power strokes of a four-stroke four at this speed."""
    return 120.0 / (rpm_value * CYLINDERS)


def segments(rpm, bands=SEGMENT_BANDS, cap_s=0.5):
    """How often the engine-speed field actually changes, per rpm band.

    0x280 goes out every 10 ms but its speed field holds a value for several
    frames, and how long it holds tracks the firing interval rather than the
    frame period. Returns (band, n, median gap, firing interval at the band
    centre) so the two can be read side by side.

    Gaps longer than cap_s are dropped: they are the engine stopping or the
    log ending, not an update interval.
    """
    changes = [(t, r) for i, (t, r) in enumerate(rpm) if i and r != rpm[i - 1][1]]
    gaps = [(changes[i + 1][0] - changes[i][0], changes[i][1])
            for i in range(len(changes) - 1)]
    out = []
    for lo, hi in bands:
        g = sorted(d for d, r in gaps if lo <= r < hi and d < cap_s)
        if g:
            out.append((lo, hi, len(g), statistics.median(g),
                        firing_interval_s((lo + hi) / 2.0)))
    return out


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


# --- the roughness measure --------------------------------------------------
#
# The cheap detector above COUNTS events past a threshold. This one grades the
# idle instead, and it exists because the count has a floor it cannot see
# under: TRIP_RPM is 20 rpm, and `--roughness --bands` shows that on the rough
# fixtures only 2-3 % of the deviation lives at steps of 20 rpm or more while
# 26-29 % of it sits in the 10-20 rpm band the count throws away. A healthy
# engine that dips 5 rpm now and then reads exactly zero events for ever, and
# a channel that reads zero for ever cannot say whether anything is improving.
#
# What it measures, and what it does NOT measure
# ----------------------------------------------
#
# The step between one firing event and the next, dead-banded and averaged.
# ⚠ **It is not a sub-threshold dip counter and must not be sold as one.** At
# 26.5 firing events a second, one 5 rpm dip a minute contributes about 0.001
# rpm to an average of 0.78 -- invisible. What the number responds to is the
# ordinary cycle-to-cycle consistency of the whole idle, which is a different
# quantity from "how many stumbles were there" and happens to separate this
# engine's recorded states better.
#
# Why the step and not the deviation from a baseline
# --------------------------------------------------
#
# A first-order baseline lags, so during the warm-up ramp -- idle falling from
# about 930 to 800 rpm -- it sits permanently above the signal and manufactures
# a one-sided deviation of about 1.2 rpm out of nothing. Against dips of 20 rpm
# that is noise; against a healthy floor of a few rpm it is most of the answer.
# The step between consecutive values is immune: the same ramp is 0.004 rpm per
# 10 ms sample.
#
# ⚠ THE STEP IS TAKEN ONCE PER CHANGE OF THE FIELD, NOT ONCE PER FRAME, and
# this is the opposite of what dips_cheap() does. The two are not inconsistent:
# dips_cheap()'s EWMA is a TIME constant and has to be stepped on the clock,
# while this one is an average PER FIRING EVENT and has to be stepped on the
# event. 0x280 holds its speed field for three to four frames at idle (see
# `--segments`), and the hold length moves with engine speed -- so stepping
# this one per frame makes the answer depend on idle speed through the hold
# ratio, which is an artefact and not combustion.
#
# ⚠ THESE CONSTANTS ARE FROZEN FOR THE SAME REASON THE ONES ABOVE ARE, and the
# reason is stronger here, not weaker: the anchor of the scale is the engine
# before the repair, and that engine no longer exists. test_idledips.py has a
# test whose only job is to fail if somebody changes them.
#
# The deadband is 3 rpm because the contrast between the recorded rough and
# smooth states climbs with it -- 1.58x at 0, 2.20x at 2, 2.72x at 3, 4.17x at
# 5 -- while the smooth reading falls toward zero and takes the resolution with
# it (0.05 rpm at a deadband of 8). 3 keeps 2.72x with the smooth state still
# at 0.78 rpm, well clear of the floor. `--roughness --deadbands` prints it.

ROUGH_DEADBAND_RPM = 3   # steps smaller than this are the idle's own noise
ROUGH_SHIFT = 8          # EWMA over 256 firing events = 9.7 s at a warm idle
ROUGH_OUT_SHIFT = 5      # accumulator >> 5 is the reported unit, 1/32 rpm

#: The 100 point of the 0-100 index, in ROUGH_OUT_SHIFT counts.
#:
#: MEASURED: `09_idle_60s_z1` at 61 C and the whole warm-up of
#: `18_coldstart_z1` both give 2.12 rpm -- two independent recordings of the
#: engine before the repair, agreeing to three figures.
#:
#: DECIDED: the anchor is 64 counts = 2.00 rpm rather than the measured 68 =
#: 2.12, because 100/64 is a multiply by 25 and a shift of 4 where 100/68 is a
#: division, and because the 6 % that costs is inside the 13 % spread the
#: anchor itself shows between 10 s windows of a steady idle. A scaling factor
#: we choose is one we may choose to be convenient; see CLAUDE.md and
#: docs/optimisation.md section 11.
IDLE_ROUGH_100 = 64
IDLE_INDEX_MAX = 200     # above 100 means worse than the engine was; clamp here


def roughness(gated, t_from=None, t_to=None, deadband_rpm=ROUGH_DEADBAND_RPM,
              shift=ROUGH_SHIFT, settle_s=SETTLE_S):
    """Grade the idle. Returns (mean_rpm, ewma_counts, n_events, idle_s).

    ``mean_rpm`` is the exact mean of the dead-banded step over the window and
    is what the tables are quoted from. ``ewma_counts`` is the same quantity
    the way firmware would carry it -- an integer accumulator, stepped by
    shifts and adds only -- in units of 1/32 rpm, which is the byte that would
    go on the bus. The two agree to a few per cent on a steady idle, and
    test_idledips.py holds that.

    The gate and the settle rule are dips_cheap()'s, deliberately: a
    roughness measured over a different set of samples than the count would
    not be comparable with it. ``idle_s`` is returned so that a test can prove
    the two agree rather than assert that they do.
    """
    dead = deadband_rpm * 4          # samples are 0.25 rpm, as on the bus
    trip = int(TRIP_RPM * 4)
    base = None
    idle_since = None
    prev_rpm = None
    prev_t = None
    idle_s = 0.0
    acc = 0
    steps = []
    for t, rpm_q4, throttle, speed_mmh in gated:
        if (t_from is not None and t < t_from) or (t_to is not None and t >= t_to):
            continue
        if speed_mmh > GATE_SPEED_MMH or throttle > GATE_THROTTLE or rpm_q4 == 0:
            base, idle_since, prev_rpm, prev_t = None, None, None, None
            continue
        if idle_since is None:
            idle_since = t
        if base is None:
            base = rpm_q4 << EWMA_SHIFT
        baseline = base >> EWMA_SHIFT
        below = baseline - rpm_q4
        settled = (t - idle_since) >= settle_s
        if not settled and below >= trip:
            idle_since = t
        if settled:
            if prev_t is not None:
                idle_s += t - prev_t
            if prev_rpm is not None and rpm_q4 != prev_rpm:
                step = abs(rpm_q4 - prev_rpm) - dead
                if step < 0:
                    step = 0
                steps.append(step)
                acc += step - (acc >> shift)
            prev_t = t
        if prev_rpm is None or rpm_q4 != prev_rpm:
            prev_rpm = rpm_q4
        if not settled:
            prev_t = t
        base += rpm_q4 - baseline
    mean_rpm = (sum(steps) / len(steps) / 4.0) if steps else 0.0
    return mean_rpm, acc >> ROUGH_OUT_SHIFT, len(steps), idle_s


def idle_index(counts):
    """The 0-200 index from a roughness byte. 100 = the engine before the repair.

    One multiply by 25 and a shift of 4 -- a uint8 x uint8 product, which is
    the one multiplication this part does in a single cycle. No division.
    """
    idx = (counts * 25) >> 4
    return IDLE_INDEX_MAX if idx > IDLE_INDEX_MAX else idx


def step_hist(gated, t_from=None, t_to=None, edges=None):
    """How often each size of step between firing events happens.

    Returns (percentages, n). This is the distribution the grade summarises,
    and it is the answer to "what is actually being measured": not an event,
    not a threshold, but the SHAPE of this table compressed into one number.
    """
    if edges is None:
        edges = ((0, 2), (2, 4), (4, 6), (6, 10), (10, 15), (15, 25),
                 (25, 10 ** 9))
    steps = _settled_steps(gated, t_from, t_to)
    n = len(steps)
    if not n:
        return [0.0] * len(edges), 0
    return ([100.0 * sum(1 for d in steps if lo * 4 <= d < hi * 4) / n
             for lo, hi in edges], n)


def _settled_steps(gated, t_from=None, t_to=None):
    """|step| in q4 units, once per change of the field, over settled idle.

    The gate and the settle rule are dips_cheap()'s; roughness() walks the
    same samples and test_idledips.py proves the two agree.
    """
    trip = int(TRIP_RPM * 4)
    base = None
    idle_since = None
    prev_rpm = None
    out = []
    for t, rpm_q4, throttle, speed_mmh in gated:
        if (t_from is not None and t < t_from) or (t_to is not None and t >= t_to):
            continue
        if speed_mmh > GATE_SPEED_MMH or throttle > GATE_THROTTLE or rpm_q4 == 0:
            base, idle_since, prev_rpm = None, None, None
            continue
        if idle_since is None:
            idle_since = t
        if base is None:
            base = rpm_q4 << EWMA_SHIFT
        baseline = base >> EWMA_SHIFT
        below = baseline - rpm_q4
        settled = (t - idle_since) >= SETTLE_S
        if not settled and below >= trip:
            idle_since = t
        if settled and prev_rpm is not None and rpm_q4 != prev_rpm:
            out.append(abs(rpm_q4 - prev_rpm))
        if prev_rpm is None or rpm_q4 != prev_rpm:
            prev_rpm = rpm_q4
        base += rpm_q4 - baseline
    return out


def rough_bands(gated, t_from=None, t_to=None, deadband_rpm=ROUGH_DEADBAND_RPM):
    """What share of the dead-banded sum each size of step contributes.

    This is the argument for grading rather than counting, in numbers: the
    band that carries the discrimination is 10-20 rpm, and TRIP_RPM sits just
    above it.
    """
    dead = deadband_rpm * 4
    edges = ((3, 5), (5, 10), (10, 20), (20, 10 ** 9))
    prev_rpm = None
    base = None
    idle_since = None
    total = 0
    parts = [0] * len(edges)
    trip = int(TRIP_RPM * 4)
    for t, rpm_q4, throttle, speed_mmh in gated:
        if (t_from is not None and t < t_from) or (t_to is not None and t >= t_to):
            continue
        if speed_mmh > GATE_SPEED_MMH or throttle > GATE_THROTTLE or rpm_q4 == 0:
            base, idle_since, prev_rpm = None, None, None
            continue
        if idle_since is None:
            idle_since = t
        if base is None:
            base = rpm_q4 << EWMA_SHIFT
        baseline = base >> EWMA_SHIFT
        below = baseline - rpm_q4
        settled = (t - idle_since) >= SETTLE_S
        if not settled and below >= trip:
            idle_since = t
        if settled and prev_rpm is not None and rpm_q4 != prev_rpm:
            d = abs(rpm_q4 - prev_rpm)
            step = max(0, d - dead)
            total += step
            for i, (lo, hi) in enumerate(edges):
                if lo * 4 <= d < hi * 4:
                    parts[i] += step
                    break
        if prev_rpm is None or rpm_q4 != prev_rpm:
            prev_rpm = rpm_q4
        base += rpm_q4 - baseline
    if not total:
        return total, [0.0] * len(edges)
    return total / 4.0, [100.0 * p / total for p in parts]


def _last(seq, t):
    vals = [v for tt, v in seq if tt <= t]
    return vals[-1] if vals else float("nan")


def report(path, thresholds, t_from, t_to, label=None, depths_too=False):
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
    if depths_too:
        for thr, ev in zip(thresholds, counts):
            print("    >=%d rpm: %s" % (
                thr, " ".join("%.1f" % d for d in
                              sorted((d for _, d in ev), reverse=True))))
    return counts


#: The rough and the smooth recordings, as the contrast is quoted from them.
#: Both rough logs are the engine BEFORE the injectors, plugs and leads; both
#: smooth ones are the same engine, the same week, at 73 C. ⚠ So the contrast
#: below is between temperature states of one engine and NOT between a sick
#: engine and a well one -- no recording of a well one exists yet. What it
#: establishes is the scale's 100 point; whether the index separates sick from
#: well is what docs/next-drive.md question 6 asks the next drive for.
ROUGH_LOGS = ("09_idle_60s_z1.txt", "18_coldstart_z1.txt")
SMOOTH_LOGS = ("11_idle_noac_z1.txt", "12_idle_ac_z1.txt")


def _window(path, t_from, t_to):
    for name, lo, hi in TABLE:
        if os.path.basename(path) == name:
            return (lo if t_from is None else t_from,
                    hi if t_to is None else t_to)
    return t_from, t_to


def _roughness_main(paths, args):
    if args.deadbands:
        print("deadband   rough %-18s smooth %-17s contrast"
              % ("(" + ", ".join(n[:2] for n in ROUGH_LOGS) + ")",
                 "(" + ", ".join(n[:2] for n in SMOOTH_LOGS) + ")"))
        cache = {n: series(os.path.join(FIXTURES, n))[3]
                 for n in ROUGH_LOGS + SMOOTH_LOGS}
        for k in (0, 1, 2, 3, 5, 8):
            def mean_of(names):
                vals = []
                for n in names:
                    lo, hi = _window(n, None, None)
                    vals.append(roughness(cache[n], lo, hi, deadband_rpm=k)[0])
                return sum(vals) / len(vals)
            r, c = mean_of(ROUGH_LOGS), mean_of(SMOOTH_LOGS)
            print("  %2d rpm      %7.3f rpm              %7.3f rpm          %5.2fx"
                  % (k, r, c, (r / c) if c else 0.0))
        return 0

    if args.hist:
        # What the grade is a summary OF. --bands says where the SUM comes
        # from; this says how often each size of step happens at all, which
        # is the shape a reader can actually picture. The rough pair and the
        # smooth pair each agree with themselves and differ from each other
        # in the 6-15 rpm columns -- everything else is much the same.
        edges = ((0, 2), (2, 4), (4, 6), (6, 10), (10, 15), (15, 25),
                 (25, 10 ** 9))
        print("%-26s %7s  %s" % ("log", "events",
              "  ".join("%5s" % ("%d-%d" % e if e[1] < 10 ** 9 else ">%d" % e[0])
                        for e in edges)))
        for path in paths:
            lo, hi = _window(path, args.t_from, args.t_to)
            hist, n = step_hist(series(path)[3], lo, hi, edges)
            if n < 50:
                continue
            print("%-26s %7d  %s" % (os.path.basename(path), n,
                  "  ".join("%4.1f%%" % h for h in hist)))
        return 0

    if args.bands:
        print("%-26s %9s   %s" % ("log", "sum", "share of it by size of step"))
        print("%-26s %9s   %7s %7s %7s %7s"
              % ("", "", "3-5", "5-10", "10-20", ">=20"))
        for path in paths:
            lo, hi = _window(path, args.t_from, args.t_to)
            total, parts = rough_bands(series(path)[3], lo, hi)
            print("%-26s %7.0f rpm   %6.1f%% %6.1f%% %6.1f%% %6.1f%%"
                  % (os.path.basename(path), total, *parts))
        return 0

    print("%-26s %8s %7s %8s %7s %6s  %s"
          % ("log", "idle", "events", "mean", "byte", "index", "oil / clt"))
    for path in paths:
        lo, hi = _window(path, args.t_from, args.t_to)
        rpm, oil, clt, gated = series(path)
        spans = [(lo, hi)]
        if args.windows:
            t0 = gated[0][0] if gated else 0.0
            start = lo if lo is not None else t0
            end = hi if hi is not None else (gated[-1][0] if gated else 0.0)
            spans = [(w, min(w + args.windows, end))
                     for w in _frange(start, end, args.windows)]
        for a, b in spans:
            mean_rpm, counts, n, idle_s = roughness(gated, a, b)
            if n < 50:
                continue
            print("%-26s %7.1fs %7d %6.3f rpm %7d %6d  oil %5.1f  clt %5.1f"
                  % (os.path.basename(path) if len(spans) == 1
                     else "  %.0f-%.0f s" % (a, b),
                     idle_s, n, mean_rpm, counts, idle_index(counts),
                     _last(oil, b if b is not None else 1e9),
                     _last(clt, b if b is not None else 1e9)))
    return 0


def _frange(start, end, step):
    t = start
    while t < end:
        yield t
        t += step


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="logs to read (default: the table)")
    ap.add_argument("--thresholds", default="20,15", help="rpm, comma separated")
    ap.add_argument("--from", dest="t_from", type=float, default=None)
    ap.add_argument("--to", dest="t_to", type=float, default=None)
    ap.add_argument("--depths", action="store_true",
                    help="print the depth of every dip instead of counting them")
    ap.add_argument("--segments", action="store_true",
                    help="print how often 0x280's engine-speed field changes")
    ap.add_argument("--roughness", action="store_true",
                    help="grade the idle instead of counting events")
    ap.add_argument("--bands", action="store_true",
                    help="with --roughness: where the sum comes from, by step size")
    ap.add_argument("--deadbands", action="store_true",
                    help="with --roughness: the contrast against the deadband")
    ap.add_argument("--hist", action="store_true",
                    help="with --roughness: how often each size of step happens")
    ap.add_argument("--windows", type=float, default=None, metavar="S",
                    help="with --roughness: split each log into windows of S seconds")
    args = ap.parse_args(argv)

    paths = args.files or [os.path.join(FIXTURES, n) for n, _, _ in TABLE]

    if args.segments:
        print("%-26s %11s %6s %10s %10s" % (
            "log", "rpm band", "n", "update", "one firing"))
        for path in paths:
            for lo, hi, n, gap, firing in segments(series(path)[0]):
                print("%-26s %5d-%-5d %6d %8.1f ms %7.1f ms" % (
                    os.path.basename(path), lo, hi, n, gap * 1000, firing * 1000))
        return 0

    if args.roughness:
        return _roughness_main(paths, args)

    thresholds = [int(x) for x in args.thresholds.split(",")]
    header = "  ".join("%15s" % ("dips >=%d rpm" % t) for t in thresholds)
    print("%-26s %7s  %9s  %s  | %s"
          % ("log", "span", "mean", header, "cheap detector, over settled idle"))

    if args.files:
        for path in args.files:
            report(path, thresholds, args.t_from, args.t_to, depths_too=args.depths)
    else:
        for name, lo, hi in TABLE:
            report(os.path.join(FIXTURES, name), thresholds, lo, hi,
                   depths_too=args.depths)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
