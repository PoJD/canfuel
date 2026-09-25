#!/usr/bin/env python3
"""Watch a capture as it is being written and say when to stop and idle.

The problem it solved was the post-repair drive's: the
middle idle had to land near 61.5 C of oil, because that is the only mid-range
temperature with a before-reading to compare against -- and by that point in
the session the display and the converter are out and VCDS is locked to groups
003 and 014, so **the driver has no oil temperature at all**. The fallback is
to take several idles and hope one lands in the band.

This is the better route when somebody is sitting with the laptop: the capture
file already carries 0x420 byte 3 at ninety-odd frames a second, so the oil
temperature is on the laptop the whole time. This reads the file **while
usbtin_capture.py is still writing it**, measures how fast the oil is
climbing, and says how long there is before the band arrives -- in time for the
driver to find somewhere to stop rather than being told to stop now.

It never opens the serial port and never writes to the capture. It only reads.

⚠ **The capture is block-buffered, so this lags it by about half a second.**
Measured rather than assumed, and it is worth having the number because it is
the one thing that could make a "stop now" late. Python's text file becomes
visible to another reader in **8216-byte blocks** -- 8 KB plus the line that
overshot -- and this bus writes **17.0-18.1 kB/s** across every _z1 fixture,
idle and driving alike, because the frames are periodic and the rate barely
moves. That is **0.44-0.47 s**, against a decision horizon of ninety seconds.

**usbtin_capture.py is deliberately not changed for it.** A flush per line at
seven hundred frames a second is a real cost to the instrument, and buys half
a second of something nobody is waiting on. What *was* changed is Ctrl-C: it
now ends a capture cleanly rather than by traceback, because ending the
recording by hand is how the drive actually finishes. A hard kill still loses
whatever is in that 8 KB buffer.

Usage
-----

    python oilwatch.py postfix_z1.txt            # a refreshing status line
    python oilwatch.py postfix_z1.txt --once     # one line and exit
    python oilwatch.py postfix_z1.txt --lead 120 # more warning
    python oilwatch.py postfix_z1.txt --until band --timeout 570

Who watches it
--------------

**Nobody in the car can watch a terminal**, which is the thing to design
around: the driver is driving and the laptop is on the passenger seat. So
there are three ways to use this and they are not equivalent.

* `--watch` (the default) prints a line whenever the verdict changes and rings
  the terminal bell when it becomes actionable. This is the only mode that
  needs nobody in the loop, and it is the fallback whatever else is running.
* `--once` prints one line. This is what another program polls.
* `--until` **blocks until there is something to say**, then prints it and
  exits -- 0 if the state arrived, 2 if it timed out with nothing to report.
  This is the mode for an assistant driving the session from the same laptop:
  a tool call that returns exactly when the driver needs telling, rather than
  a poll that has to be remembered. `--timeout` exists because the caller's
  own command timeout does; time out, report nothing, and call again.
"""

from __future__ import annotations

import argparse
import os
import time

import canlog

# --- the band, and why it is these numbers ---------------------------------
#
# ⚠ ALL THREE ARE DECISIONS, not specifications. The before-repair fixtures
# have exactly two readings with a non-zero dip rate -- 13-17 C and 61.5 C --
# and a zero one at 72.8-73.5 C, and the relationship between the three is not
# monotonic. So there is no measured width to take; what follows is chosen:
#
# TARGET is the one mid-range before-reading, so a matched after-reading is a
# comparison rather than a new measurement. The band is centred on it, stops
# well short of the 72.8 C that already counted zero ON THE OLD INJECTORS --
# an idle above that proves nothing whichever way it comes out -- and is wide
# enough that a driver can reach somewhere to stop. Widen it and the match
# weakens; narrow it and the stop becomes unreachable.
#
# ⚠ THESE ARE OIL, 0x420 BYTE 3, AND NOT THE COOLANT. The target is really
# raw byte 146; 61.5 C is what this project's decode calls it, and that decode
# is the open question 10 in docs/firmware/open.md. It does not matter here,
# because the before-reading went through the same decode -- matching the
# label matches the byte either way. It would matter if anyone retuned these
# numbers against a corrected scale without moving the before-reading with
# them.
TARGET_C = 61.5
BAND_LO_C = 55.0
BAND_HI_C = 68.0

#: How long the idle itself wants to be. The post-repair drive's rule: one
#: minute settles "gone or not gone", three settle "how much better". Only the
#: FIRST idle is cut short there, and for a reason that does not apply here --
#: it is spending coolant the cold coasts need, and by the middle idle that
#: budget is long gone.
IDLE_S = 3 * 60.0

#: Seconds of warning asked for before the band arrives. A driver has to notice
#: the screen and then find somewhere legal to stop.
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
    """

    def __init__(self, path):
        self.path = path
        self.offset = 0
        self.tail = ""
        self.raw_prev = None
        self.wrap = 0
        self.oil = []          # (t_s, C), at most one a second
        self.now = {}          # last seen of each channel
        self.t_s = 0.0
        self._idle_since = None

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
            self.__init__(self.path)
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
        self._track_idle()

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

    def _track_idle(self):
        if self.stationary():
            if self._idle_since is None:
                self._idle_since = self.t_s
        else:
            self._idle_since = None


def verdict(tail, lead_s=LEAD_S):
    """(headline, detail) -- what to tell the driver right now."""
    oil = tail.now.get("oil")
    if oil is None:
        return "WAITING", "no 0x420 yet -- is the ignition on and the capture running?"
    if tail.stationary():
        left = IDLE_S - tail.idle_seconds()
        if BAND_LO_C <= oil <= BAND_HI_C:
            if left > 0:
                return "IDLING, IN BAND", f"hold it another {left/60:.1f} min"
            return "IDLING, DONE", "this one is in the band and long enough"
        if left > 0:
            return "IDLING", f"oil {oil:.1f} C is outside the band; {left/60:.1f} min to go"
        return "IDLING, DONE", f"long enough, but at {oil:.1f} C"
    if oil > BAND_HI_C:
        return "PAST THE BAND", ("too hot for the middle idle -- this is now the hot "
                                 "one, step 16")
    if oil >= BAND_LO_C:
        return "STOP NOW", f"oil {oil:.1f} C is in the band"
    eta = tail.seconds_to(BAND_LO_C)
    if eta is None:
        return "KEEP DRIVING", "oil not climbing measurably yet"
    if eta <= lead_s:
        return "STOP WITHIN A MINUTE", f"band in about {eta/60:.1f} min -- find a place"
    return "KEEP DRIVING", f"band in about {eta/60:.0f} min"


#: What --until can wait for, as the verdict headlines that satisfy each.
UNTIL = {
    "band": ("STOP WITHIN A MINUTE", "STOP NOW"),
    "idle-done": ("IDLING, DONE",),
    "hot": ("PAST THE BAND",),
}

BELL_ON = frozenset(("STOP WITHIN A MINUTE", "STOP NOW", "IDLING, DONE"))


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
        "standing" if tail.stationary() else "moving  ",
        head, detail))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("capture", help="the file usbtin_capture.py is writing")
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
                    help="do not ring the terminal bell in --watch")
    args = ap.parse_args(argv)

    tail = Tail(args.capture)
    tail.poll()
    if args.once:
        print(line(tail, args.lead))
        return 0

    if args.until:
        return wait_for(tail, args.until, args.timeout, args.every, args.lead)

    print("target %.1f C, band %.1f-%.1f C, %.0f s of warning. Ctrl-C to stop."
          % (TARGET_C, BAND_LO_C, BAND_HI_C, args.lead))
    last = None
    try:
        while True:
            tail.poll()
            now = line(tail, args.lead)
            if now != last:
                head, _ = verdict(tail, args.lead)
                # The driver is driving; a quiet line on a laptop on the
                # passenger seat is not an interface. The bell is.
                bell = "\a" if head in BELL_ON and not args.no_bell else ""
                print(bell + now, flush=True)
                last = now
            time.sleep(args.every)
    except KeyboardInterrupt:
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
