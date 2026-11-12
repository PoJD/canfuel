#!/usr/bin/env python3
"""Read a capture while it is being written and print the car's state every minute.

**The MFD and the CAN capture are one or the other** (`CLAUDE.md`, *Sessions
at the car*): on a captured drive the display is out, so the driver has no oil
or coolant temperature, no `IdleHealth` and no `Misfires`. All of them are in
the capture already. This prints one line per interval -- the wall clock, oil,
coolant, engine speed, road speed, and at a standstill the stop's own figures
-- for Claude to relay to the driver by chat. Run it from the capture's start
to its end, every captured session (*the owner*, 12/11/2026).

At a standstill the line carries, from the moment the road speed last fell to
zero:

* **IdleHealth over the last window** -- `idledips.roughness()`'s mean step
  x 50, the scale `CLAUDE.md` fixes (*lower is calmer*). This is the figure
  to quote; the display's own value is an EWMA and lags it.
* **The EWMA index since the stop** -- `idledips.idle_index()`, the byte the
  converter would put on the bus for the same stretch.
* **Misfires** -- `idledips.misfires()`, the converter's estimate line for
  line: the events in the last minute of settled idle, the stop's total, and
  MisfAvg (events per minute of settled idle).

⚠ **These are the oracle's numbers over one stop, not the converter's over a
trip.** The converter clears its grade at a start, not at a stop, so a
display in the car would show something else over the same minute. Within a
stop the two are the same arithmetic.

⚠ **A standstill is the road speed at rest (`STANDSTILL_MMH`) by 0x1A0's validity rule**
(`idledips.series()`), so a car held on the brake in traffic starts a new
stop each time it creeps. That is what is wanted: a creep is not idle.

It only reads the file, never the serial port; closing it costs the
recording nothing. The whole file is re-read every interval (a few seconds
for an hour's capture), so its state is never remembered between polls.

Usage
-----

    python livewatch.py capture_z1.txt               # a line every 60 s
    python livewatch.py capture_z1.txt --every 30
    python livewatch.py capture_z1.txt --once        # one line and exit
"""

from __future__ import annotations

import argparse
import datetime
import os
import sys
import time

import idledips

WINDOW_S = 60.0   # the IdleHealth window; one minute, as the line is read
STANDSTILL_MMH = 100   # oilwatch.py's and src/config.h's: 0x1A0 reads 5 at rest


def stop_start(gated):
    """Seconds into the capture at which the current standstill began, or None
    if the car is moving (or the engine is off) at the end of the capture."""
    if not gated:
        return None
    start = None
    for t, rpm_q4, _thr, speed_mmh in gated:
        if speed_mmh <= STANDSTILL_MMH and rpm_q4 > 0:
            if start is None:
                start = t
        else:
            start = None
    return start


def status(rpm, oil, clt, gated, window_s=WINDOW_S):
    """The state at the end of the capture, as a dict. Times in capture seconds."""
    if not gated:
        return {}
    t_end = gated[-1][0]
    tail = rpm[-200:]
    out = {
        "t_end": t_end,
        "oil_c": oil[-1][1] if oil else None,
        "clt_c": clt[-1][1] if clt else None,
        "rpm": sum(v for _, v in tail) / len(tail) if tail else None,
        "speed_kmh": gated[-1][3] / 1000.0,
        "stop_s": None,
    }
    t0 = stop_start(gated)
    if t0 is None:
        return out
    mean, _, _, idle_s = idledips.roughness(gated, t_from=max(t0, t_end - window_s))
    _, counts_all, _, _ = idledips.roughness(gated, t_from=t0)
    wsum, total, idle_ms = idledips.misfires(gated, t_from=t0)
    avg = idledips.misf_avg(total, idle_ms)
    out.update({
        "stop_s": t_end - t0,
        "idle_health": mean * 50.0,
        "idle_window_s": idle_s,
        "ewma_index": idledips.idle_index(counts_all),
        "misf_window": wsum,
        "misf_total": total,
        "misf_avg": None if avg is None else avg / 10.0,
    })
    return out


def fmt(s, clock):
    """One line for the chat."""
    if not s:
        return f"{clock}  no frames yet"
    def c(v):
        return "--" if v is None else f"{v:.0f} C"
    line = (f"{clock}  oil {c(s['oil_c'])}, coolant {c(s['clt_c'])}, "
            f"{s['rpm']:.0f} rpm, {s['speed_kmh']:.0f} km/h")
    if s["stop_s"] is None:
        return line + "  | driving"
    avg = "--" if s["misf_avg"] is None else f"{s['misf_avg']:.1f}"
    return (line + f"  | standing {s['stop_s'] / 60:.1f} min: "
            f"IdleHealth {s['idle_health']:.0f} (last {s['idle_window_s']:.0f} s idle), "
            f"EWMA {s['ewma_index']}, Misfires {s['misf_window']} "
            f"(stop {s['misf_total']}, MisfAvg {avg})")


def once(path, window_s=WINDOW_S):
    rpm, oil, clt, gated = idledips.series(path)
    s = status(rpm, oil, clt, gated, window_s)
    # The file is still being written, so its mtime is the last frame's wall
    # clock (to the half second the buffering costs; oilwatch.py measures it).
    clock = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%H:%M:%S")
    return fmt(s, clock)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file", help="the capture usbtin_capture.py is writing")
    ap.add_argument("--every", type=float, default=60.0, help="seconds between lines")
    ap.add_argument("--window", type=float, default=WINDOW_S,
                    help="IdleHealth window in seconds")
    ap.add_argument("--once", action="store_true", help="one line and exit")
    args = ap.parse_args(argv)
    while True:
        try:
            print(once(args.file, args.window), flush=True)
        except (OSError, SystemExit, IndexError) as e:   # file not there yet
            print(f"{time.strftime('%H:%M:%S')}  not readable yet: {e}", flush=True)
        if args.once:
            return 0
        time.sleep(args.every)


if __name__ == "__main__":
    sys.exit(main())
