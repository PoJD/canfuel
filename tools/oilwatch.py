#!/usr/bin/env python3
"""Watch a capture as it is being written and say when to stop and idle.

Built for the test after the valve cover job (`docs/engine-health/plan.md`,
*Test after the job*, session A): a warm-up drive with **two standing idles at
two oil temperatures**, the middle one where group 014 counted most on the car
as it now is, and the hot one the plan has always read. By then the display
and the converter are out and VCDS is busy logging, so **the driver has no oil
temperature at all** -- and a stop that lands outside its band has to be
driven again, which is exactly the idling the plan is trying to avoid.

The capture file already carries 0x420 byte 3 at ninety-odd frames a second,
so the oil temperature is on the laptop the whole time. This reads the file
**while usbtin_capture.py is still writing it**, measures how fast the oil is
climbing, says how long there is before the next band arrives -- in time for
the driver to find somewhere to stop rather than being told to stop now --
counts the idle inside the band, and rings when it is long enough.

It never opens the serial port and never writes to the capture. It only reads.
So it runs beside the capture in a second window: the capture is one process,
this is another, and closing this one costs the recording nothing.

**Its state is rebuilt from the capture, frame by frame**, not remembered
between polls: which stop is next, whether one was done or missed, how long
the car has stood in the band. So a watch window closed by accident and
started again reads the file from the top and arrives at the same place, and
`--until` in a separate process sees what `--watch` sees.

⚠ **The capture is block-buffered, so this lags it by about half a second.**
Measured rather than assumed, and it is worth having the number because it is
the one thing that could make a "stop now" late. Python's text file becomes
visible to another reader in **8216-byte blocks** -- 8 KB plus the line that
overshot -- and this bus writes **17.0-18.1 kB/s** across every _z1 fixture,
idle and driving alike, because the frames are periodic and the rate barely
moves. That is **0.44-0.47 s**, against a decision horizon of ninety seconds.

**usbtin_capture.py is deliberately not changed for it.** A flush per line at
seven hundred frames a second is a real cost to the instrument, and buys half
a second of something nobody is waiting on. Ctrl-C ends a capture cleanly; a
hard kill loses whatever is in that 8 KB buffer.

Usage
-----

    python oilwatch.py a_z1.txt                  # both stops, rings (session A)
    python oilwatch.py a_z1.txt --only hot       # the hot idle alone (session B)
    python oilwatch.py a_z1.txt --once           # one line and exit
    python oilwatch.py a_z1.txt --lead 120       # more warning
    python oilwatch.py a_z1.txt --until stop --timeout 570

Who watches it
--------------

**Nobody in the car can watch a terminal**, which is the thing to design
around: the driver is driving and the laptop is on the passenger seat. So
there are three ways to use this and they are not equivalent.

* `--watch` (the default) prints a line whenever the verdict changes and
  **rings** when it becomes actionable -- three short beeps for "stop", one
  long one for "done, drive on". This is the one the owner runs in his own
  window, and it needs nobody else in the loop. On Windows the beeps go
  through `winsound`, which reaches the speakers from a plain `cmd` window;
  elsewhere, or if that fails, the terminal bell.
* `--once` prints one line. This is what another program polls.
* `--until` **blocks until there is something to say**, then prints it and
  exits -- 0 if the state arrived, 2 if it timed out with nothing to report.
  This is the mode for an assistant driving the capture from the same laptop:
  a tool call that returns exactly when the driver needs telling, rather than
  a poll that has to be remembered. `--timeout` exists because the caller's
  own command timeout does; time out, report nothing, and call again.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from dataclasses import dataclass

import canlog

# --- the stops, and why they are these numbers -----------------------------
#
# ⚠ THE BANDS AND THE LENGTHS ARE DECISIONS, not specifications. What they are
# chosen from is measured: group 014 aligned on engine speed to the captures
# beside it, standing idle with detection `aktivováno` only, binned by oil
# temperature (`docs/engine-health/open.md` S3, *How often 014 counts, by oil
# temperature*). On 24, the car as it now is -- new MAF, adaptations fresh
# after a disconnect, which is also what the job leaves -- the counter moved
# 20 times a minute at 56-60 C and 10 times a minute at 68-72 C, and the
# longest quiet stretch of active idle was 57 s.
#
# * MID is where it counted most. The band stops at 62 C because 60-64 C
#   already read a tenth of that; it starts at 56 because below it no
#   post-MAF 014 was ever logged.
# * HOT is the band the plan has read since before this tool: 70-72 C in
#   `plan.md`, widened by two degrees downwards so that a driver can reach it.
#   On the OLD MAF this band counted almost nothing (0.3 a minute on 19) --
#   which is why only the post-MAF rate is a comparison.
# * The lengths: two and three minutes of zero, against 40 and 30 counts
#   expected on 24 over the same time, and each more than twice the longest
#   quiet stretch ever seen there. Longer buys little and costs idling with
#   misfires, which the plan exists to avoid.
#
# ⚠ THESE ARE OIL, 0x420 BYTE 3, AND NOT THE COOLANT. The decode is the open
# question 10 in docs/firmware/open.md. It does not matter here, because the
# before-readings went through the same decode -- matching the label matches
# the byte either way. It would matter if anyone retuned these numbers against
# a corrected scale without moving the before-readings with them.


@dataclass(frozen=True)
class Stop:
    name: str
    lo_c: float
    hi_c: float
    idle_s: float


STOPS = (
    Stop("mid", 56.0, 62.0, 2 * 60.0),
    Stop("hot", 68.0, 72.0, 3 * 60.0),
)

#: Seconds of warning asked for before the band arrives. A driver has to notice
#: the beep and then find somewhere legal to stop.
LEAD_S = 90.0

#: The window the climb rate is measured over. The channel quantises to 0.75 C
#: a count, so a short window sees steps rather than a slope.
SLOPE_WINDOW_S = 240.0

#: Below this the rate is noise, not a climb, and nothing is predicted from it.
SLOPE_FLOOR_C_PER_MIN = 0.05

STANDSTILL_MMH = 100   # src/config.h, and docs/firmware/can-decoding.md trap 1
THROTTLE_REST = 38     # src/config.h


def oil_c(byte):
    """0x420 byte 3. docs/firmware/can-decoding.md: x 0.75 - 48, 0xFF with the key off."""
    return None if byte == 0xFF else byte * 0.75 - 48.0


def coolant_c(byte):
    return None if byte == 0xFF else byte * 0.75 - 48.0


class Tail:
    """Reads a growing capture, keeping only what a decision needs.

    The adapter's timestamp is four hex digits, so it wraps every 65.5 s and
    has to be unwrapped as it arrives -- canlog.unwrap_timestamps does this to
    a finished list, and an hour-long capture wraps fifty-five times.

    The stops are walked here, frame by frame, for the reason the module
    docstring gives: the state has to come out the same however often, and
    from however far into the drive, somebody starts looking.
    """

    def __init__(self, path, stops=STOPS):
        self.path = path
        self.stops = tuple(stops)
        self.offset = 0
        self.tail = ""
        self.raw_prev = None
        self.wrap = 0
        self.oil = []          # (t_s, C), at most one a second
        self.now = {}          # last seen of each channel
        self.t_s = 0.0
        self._idle_since = None
        self._prev_t = None
        # the walk through the stops
        self.index = 0         # the stop being worked towards
        self.in_band_s = 0.0   # standing, in its band, since the car last moved
        self.done = False      # the current stop has had its idle
        self.log = []          # (stop name, "done" | "missed", t_s)

    def _stamp(self, raw_ms):
        if self.raw_prev is not None and raw_ms < self.raw_prev:
            self.wrap += canlog.TIMESTAMP_WRAP_MS
        self.raw_prev = raw_ms
        return (raw_ms + self.wrap) / 1000.0

    def poll(self):
        """Read whatever has been appended since last time. Returns lines read."""
        try:
            size = os.path.getsize(self.path)
        except OSError:
            return 0
        if size < self.offset:            # the file was replaced
            self.__init__(self.path, self.stops)
            size = os.path.getsize(self.path)
        if size == self.offset:
            return 0
        with open(self.path, "r", encoding="ascii", errors="replace") as fh:
            fh.seek(self.offset)
            chunk = fh.read()
            self.offset = fh.tell()
        chunk = self.tail + chunk
        lines = chunk.split("\n")
        self.tail = lines.pop()           # possibly a half-written line
        for line in lines:
            self._feed(line.strip())
        return len(lines)

    def _feed(self, line):
        if not line:
            return
        try:
            f = canlog.parse_line(line)
        except ValueError:      # canlog.LogFormatError -- a half-written line
            return
        if f is None or f.ts_ms is None:
            return
        t = self._stamp(f.ts_ms)
        self.t_s = t
        if f.can_id == 0x420 and len(f.data) >= 4:
            c = oil_c(f.data[3])
            if c is not None:
                self.now["oil"] = c
                if not self.oil or t - self.oil[-1][0] >= 1.0:
                    self.oil.append((t, c))
                    cutoff = t - SLOPE_WINDOW_S * 3
                    while self.oil and self.oil[0][0] < cutoff:
                        self.oil.pop(0)
        elif f.can_id == 0x288 and len(f.data) >= 2:
            self.now["coolant"] = coolant_c(f.data[1])
        elif f.can_id == 0x280 and len(f.data) >= 8:
            self.now["rpm"] = (f.data[2] | (f.data[3] << 8)) / 4.0
            self.now["throttle"] = f.data[5]
        elif f.can_id == 0x1A0 and len(f.data) >= 4:
            if (f.data[1] & 0x40) != 0 and (f.data[1] & 0x03) == 0:
                self.now["speed_mmh"] = (f.data[2] | (f.data[3] << 8)) * 5
        self._track(t)

    # --- the stops ----------------------------------------------------------

    def stop(self):
        """The stop being worked towards, or None when all are behind us."""
        return self.stops[self.index] if self.index < len(self.stops) else None

    def last_stop(self):
        return self.index == len(self.stops) - 1

    def in_band(self):
        s, oil = self.stop(), self.now.get("oil")
        return s is not None and oil is not None and s.lo_c <= oil <= s.hi_c

    def _advance(self, how):
        self.log.append((self.stops[self.index].name, how, self.t_s))
        self.index += 1
        self.in_band_s = 0.0
        self.done = False

    def _track(self, t):
        dt = 0.0 if self._prev_t is None else max(0.0, t - self._prev_t)
        self._prev_t = t
        standing = self.stationary()
        if standing:
            if self._idle_since is None:
                self._idle_since = t
        else:
            self._idle_since = None
        s = self.stop()
        if s is None:
            return
        if not self.moving():
            # Standing but not idling -- a touch of the pedal, the engine
            # stalled -- neither counts nor resets; nor does out-of-band
            # standing time: a hot stop entered a degree too warm cools into
            # its band at idle.
            if standing and self.in_band():
                self.in_band_s += dt
            if self.in_band_s >= s.idle_s:
                self.done = True
            return
        if self.done:
            self._advance("done")
        elif (not self.last_stop()
              and self.now.get("oil") is not None and self.now["oil"] > s.hi_c):
            # Oil does not cool on the move, so a band driven through is gone.
            self._advance("missed")
        else:
            self.in_band_s = 0.0      # an idle is one standing, not a sum

    # --- what the numbers mean ---------------------------------------------

    def slope_c_per_min(self, window_s=SLOPE_WINDOW_S):
        """Least squares over the window. None if there is not enough of it."""
        pts = [(t, c) for t, c in self.oil if t >= self.t_s - window_s]
        if len(pts) < 30 or pts[-1][0] - pts[0][0] < window_s / 3:
            return None
        n = len(pts)
        mt = sum(t for t, _ in pts) / n
        mc = sum(c for _, c in pts) / n
        den = sum((t - mt) ** 2 for t, _ in pts)
        if den <= 0:
            return None
        return sum((t - mt) * (c - mc) for t, c in pts) / den * 60.0

    def seconds_to(self, target):
        """Seconds until the oil reaches `target` at the current rate."""
        oil = self.now.get("oil")
        rate = self.slope_c_per_min()
        if oil is None or rate is None or rate <= SLOPE_FLOOR_C_PER_MIN:
            return None
        if oil >= target:
            return 0.0
        return (target - oil) / rate * 60.0

    def moving(self):
        """Road speed alone. The pedal is not motion."""
        return self.now.get("speed_mmh", 0) > STANDSTILL_MMH

    def stationary(self):
        return (self.now.get("speed_mmh", 0) <= STANDSTILL_MMH
                and self.now.get("throttle", 255) <= THROTTLE_REST
                and self.now.get("rpm", 0) > 0)

    def idle_seconds(self):
        """How long the car has been standing with the engine running.

        Road speed decides this, not the oil series, and it is tracked FRAME BY
        FRAME rather than once per poll -- otherwise an idle that began before
        the tool was started, or that spans two polls, reads as having begun at
        whatever moment the tool last looked. Only meaningful while
        stationary() is true.
        """
        return self.t_s - self._idle_since if self._idle_since is not None else 0.0


def _band(s):
    return "%s %.0f-%.0f C" % (s.name, s.lo_c, s.hi_c)


def verdict(tail, lead_s=LEAD_S):
    """(headline, detail) -- what to tell the driver right now."""
    oil = tail.now.get("oil")
    if oil is None:
        return "WAITING", "no 0x420 yet -- is the ignition on and the capture running?"
    s = tail.stop()
    if s is None:
        return "ALL STOPS DONE", "nothing left to wait for (%s)" % _summary(tail)
    missed = [n for n, how, _ in tail.log if how == "missed"]
    note = " (missed: %s)" % ", ".join(missed) if missed else ""
    if not tail.moving():
        if tail.done:
            if tail.last_stop():
                return "IDLING, DONE", ("%s idle long enough -- 004 for a minute, "
                                        "then engine off%s" % (s.name, note))
            return "IDLING, DONE", ("%s idle long enough -- drive on towards %s%s"
                                    % (s.name, _band(tail.stops[tail.index + 1]), note))
        left = s.idle_s - tail.in_band_s
        if tail.in_band():
            return "IDLING, IN BAND", "%s: hold it another %.1f min" % (s.name, left / 60)
        if oil > s.hi_c:
            return "IDLING", ("oil %.1f C above %s -- cooling; counts once in "
                              "the band" % (oil, _band(s)))
        return "IDLING", ("standing %.1f min, oil %.1f C; next stop %s"
                          % (tail.idle_seconds() / 60, oil, _band(s)))
    if oil > s.hi_c:
        # Only the last stop gets here moving: an earlier one is marked missed.
        return "STOP NOW", ("oil %.1f C, above %s -- it cools at idle, and the "
                            "time counts from when it is in the band" % (oil, _band(s)))
    if oil >= s.lo_c:
        return "STOP NOW", "oil %.1f C is in %s" % (oil, _band(s))
    eta = tail.seconds_to(s.lo_c)
    if eta is None:
        return "KEEP DRIVING", "oil %.1f C, not climbing measurably yet%s" % (oil, note)
    if eta <= lead_s:
        return "STOP WITHIN A MINUTE", ("%s in about %.1f min -- find a place"
                                        % (_band(s), eta / 60))
    return "KEEP DRIVING", "%s in about %.0f min%s" % (_band(s), eta / 60, note)


def _summary(tail):
    return ", ".join("%s %s" % (n, how) for n, how, _ in tail.log) or "none"


#: What --until can wait for, as the verdict headlines that satisfy each.
UNTIL = {
    "stop": ("STOP WITHIN A MINUTE", "STOP NOW"),
    "idle-done": ("IDLING, DONE",),
    "all-done": ("ALL STOPS DONE",),
}

#: Three short beeps: find a place and stop. One long: the idle is done.
BELL_STOP = frozenset(("STOP WITHIN A MINUTE", "STOP NOW"))
BELL_DONE = frozenset(("IDLING, DONE",))
BELL_ON = BELL_STOP | BELL_DONE


def ring(head, out=sys.stdout):
    """Make a noise somebody driving will hear. Never raises."""
    if head not in BELL_ON:
        return
    pattern = [(1000, 250)] * 3 if head in BELL_STOP else [(700, 900)]
    try:
        import winsound            # Windows only; reaches the speakers from cmd
        for freq, ms in pattern:
            winsound.Beep(freq, ms)
            time.sleep(0.1)
        return
    except (ImportError, RuntimeError):
        pass
    try:
        out.write("\a" * len(pattern))
        out.flush()
    except (OSError, ValueError):
        pass


def wait_for(tail, want, timeout_s, poll_s, lead_s, out=None):
    """Poll until one of `want`'s headlines shows, or the timeout. 0 or 2.

    Returns the exit code the CLI uses: 0 means the state arrived and the line
    printed is about it; 2 means nothing happened in the time allowed, which is
    not a failure -- the caller simply calls again.
    """
    heads = UNTIL[want]
    deadline = time.monotonic() + timeout_s
    while True:
        tail.poll()
        head, _ = verdict(tail, lead_s)
        if head in heads:
            print(line(tail, lead_s), file=out)
            return 0
        if time.monotonic() >= deadline:
            print(line(tail, lead_s), file=out)
            return 2
        time.sleep(poll_s)


def line(tail, lead_s=LEAD_S):
    oil = tail.now.get("oil")
    clt = tail.now.get("coolant")
    rate = tail.slope_c_per_min()
    head, detail = verdict(tail, lead_s)
    return ("oil %s  coolant %s  %s  %s  |  %-20s %s" % (
        "  --  " if oil is None else "%5.1f C" % oil,
        "  --  " if clt is None else "%5.1f C" % clt,
        "%+4.2f C/min" % rate if rate is not None else "   ? C/min",
        "moving  " if tail.moving() else "standing",
        head, detail))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("capture", help="the file usbtin_capture.py is writing")
    ap.add_argument("--only", choices=[s.name for s in STOPS],
                    help="watch for this one stop and no other")
    ap.add_argument("--once", action="store_true", help="print one line and exit")
    ap.add_argument("--lead", type=float, default=LEAD_S,
                    help="seconds of warning before the band (default %d)" % LEAD_S)
    ap.add_argument("--every", type=float, default=5.0, help="seconds between polls")
    ap.add_argument("--until", choices=sorted(UNTIL),
                    help="block until this state, then print one line and exit "
                         "(0 reached, 2 timed out)")
    ap.add_argument("--timeout", type=float, default=570.0,
                    help="seconds --until will wait (default 570, which fits "
                         "inside a ten-minute command timeout)")
    ap.add_argument("--no-bell", action="store_true",
                    help="do not ring in --watch")
    args = ap.parse_args(argv)

    stops = [s for s in STOPS if args.only in (None, s.name)]
    tail = Tail(args.capture, stops)
    tail.poll()
    if args.once:
        print(line(tail, args.lead))
        return 0

    if args.until:
        return wait_for(tail, args.until, args.timeout, args.every, args.lead)

    print("stops: %s; %.0f s of warning. Ctrl-C to stop watching (the capture "
          "carries on)." % ("; ".join("%s for %.0f min" % (_band(s), s.idle_s / 60)
                                      for s in stops), args.lead))
    last = last_head = None
    try:
        while True:
            tail.poll()
            now = line(tail, args.lead)
            if now != last:
                head, _ = verdict(tail, args.lead)
                print(now, flush=True)
                # The driver is driving; a quiet line on a laptop on the
                # passenger seat is not an interface. The noise is. Once per
                # new headline, not on every changed digit.
                if head != last_head and not args.no_bell:
                    ring(head)
                last, last_head = now, head
            time.sleep(args.every)
    except KeyboardInterrupt:
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
