#!/usr/bin/env python3
"""Parser for USBtin logs. Handles both formats found in our fixtures.

Format A -- raw slcan stream, exactly as the USBtin emits it over the serial
line and as the older recordings stored it without post-processing:

    t1a0800400100fefe001d
    ^ ^  ^^
    | |  +- payload, two hex chars per byte
    | +---- DLC, one hex char
    +------ 11-bit ID, three hex chars

The fixtures in this repository carry no timestamps, because they were
recorded with the adapter's timestamping off: frames come back with
ts_ms=None and it is up to the caller to derive time from frame periods
(see docs/can-decoding.md, the section on periods -- it is not reliable).

Opened with Z1, the USBtin appends four hex digits of milliseconds:

    t1a0800400100fefe001d2a3f
                          ^^^^ timestamp, stamped by the adapter

which is parsed here into ts_ms. **That is the timestamp worth having** --
it is taken in the adapter when the frame arrives, where format B's is taken
by the host when it gets round to the line. Open question 9 in
docs/can-decoding.md is that difference, and one recording with Z1 closes it.

Format B -- USBtinViewer export, five tab-separated columns:

    2078 <TAB> jar:file:/...receive.png <TAB> 320h <TAB> 8 <TAB> 05 00 86 ...
    ts (ms)    row icon                   ID+h    DLC    space-separated bytes

Rows carrying info.png are viewer messages ("Connected to USBtin", ...):
their ID and DLC columns are empty and the last column holds the text.
They are skipped.

Command line usage:

    python canlog.py FILE [FILE ...]           # per-ID summary
    python canlog.py --dump FILE               # print every frame
    python canlog.py --id 0x480 --dump FILE    # restrict to one ID
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Iterator, Optional

__all__ = ["Frame", "parse_line", "parse_file", "iter_frames", "undouble",
           "unwrap_timestamps", "frame_gaps", "TIMESTAMP_WRAP_MS",
           "LogFormatError"]


class LogFormatError(ValueError):
    """The line looks like a frame but cannot be taken apart."""


# The USBtin's Z1 timestamp counts milliseconds and restarts. **Measured on
# 2026-08-11**, off a 20 s capture of the car's bus that happened to straddle
# the wrap -- which is what the comment here used to ask somebody to do:
#
#     before: 59993 59994 59995 59996 59996 60000
#     after :     0     0     1     2     4     8
#
# So the counter reaches 60000 and the next value is 0, i.e. it takes 60001
# distinct values and the wrap period is 60001 ms, not the round 60000 that
# Lawicel's 0x0000-0xEA5F range would imply. Frames arrive about 1.4 ms apart
# on this bus, so 60000 being the true maximum rather than a value that merely
# happened to be sampled is as tight as one capture can make it; the residual
# doubt is one millisecond per minute, which nothing here is sensitive to.
#
# This applies to format A only. Format B's times come from the host and do
# not wrap at all.
TIMESTAMP_WRAP_MS = 60001


def unwrap_timestamps(values: list[int]) -> list[int]:
    """Make a wrapping millisecond counter monotonic.

    Every time the value goes backwards, one wrap period is added to
    everything that follows. Returns a new list; the input is untouched.

    This has to be applied to the whole recording before any subtraction --
    computing gaps first and patching up the negative one afterwards gives the
    same answer only by accident, and not at all once a recording is longer
    than two minutes.
    """
    out: list[int] = []
    offset = 0
    previous: Optional[int] = None
    for v in values:
        if previous is not None and v < previous:
            offset += TIMESTAMP_WRAP_MS
        out.append(v + offset)
        previous = v
    return out


@dataclass(frozen=True)
class Frame:
    """A single CAN frame from a log.

    ts_ms is None for format A, which carries no timestamps.
    """

    ts_ms: Optional[int]
    can_id: int
    data: bytes

    @property
    def dlc(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        ts = "        -" if self.ts_ms is None else f"{self.ts_ms:9d}"
        return f"{ts}  0x{self.can_id:03X}  [{self.dlc}]  {self.data.hex(' ')}"


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------

def _parse_slcan(line: str) -> Optional[Frame]:
    """Format A: tIIILDD...  (plus the 'T' variant for 29-bit IDs)."""
    kind = line[0]
    if kind == "t":
        id_len = 3
    elif kind == "T":
        id_len = 8
    else:
        return None

    head = 1 + id_len + 1  # 't' + ID + DLC
    if len(line) < head:
        raise LogFormatError(f"slcan line is too short: {line!r}")

    try:
        can_id = int(line[1:1 + id_len], 16)
        dlc = int(line[1 + id_len], 16)
    except ValueError as exc:
        raise LogFormatError(f"unreadable ID/DLC: {line!r}") from exc

    if dlc > 8:
        raise LogFormatError(f"DLC {dlc} > 8: {line!r}")

    payload = line[head:head + 2 * dlc]
    if len(payload) != 2 * dlc:
        raise LogFormatError(
            f"DLC={dlc} promises {2 * dlc} hex chars, found {len(payload)}: {line!r}")

    try:
        data = bytes.fromhex(payload)
    except ValueError as exc:
        raise LogFormatError(f"unreadable payload: {line!r}") from exc

    # Anything after the payload is the USBtin's own timestamp, four hex
    # digits of milliseconds, present only when the adapter was opened with
    # Z1. THIS IS THE GOOD KIND OF TIMESTAMP: it is stamped in the adapter
    # when the frame arrives, not by the host when it gets round to the line.
    # docs/can-decoding.md open question 9 is about exactly that difference --
    # the two logs in viewer format carry host times and disagree with the
    # rest of the fixtures by roughly a factor of two.
    #
    # The counter wraps, and the wrap value is not stated in USBtin's
    # documentation. It is measured now -- see TIMESTAMP_WRAP_MS below.
    tail = line[head + 2 * dlc:].strip()
    ts_ms = None
    if tail:
        if len(tail) != 4:
            raise LogFormatError(
                f"trailing {len(tail)} chars after the payload, expected a "
                f"4-digit timestamp or nothing: {line!r}")
        try:
            ts_ms = int(tail, 16)
        except ValueError as exc:
            raise LogFormatError(f"unreadable timestamp: {line!r}") from exc

    return Frame(ts_ms, can_id, data)


def _parse_viewer(line: str) -> Optional[Frame]:
    """Format B: ts <TAB> icon <TAB> IDh <TAB> DLC <TAB> bytes."""
    cols = line.split("\t")
    if len(cols) < 5:
        return None

    ts_raw, _icon, id_raw, dlc_raw, data_raw = cols[0], cols[1], cols[2], cols[3], cols[4]

    # Viewer info rows have empty ID and DLC and carry text in the last column.
    if not id_raw.strip() or not dlc_raw.strip():
        return None

    id_txt = id_raw.strip()
    if id_txt.lower().endswith("h"):
        id_txt = id_txt[:-1]

    try:
        can_id = int(id_txt, 16)
        dlc = int(dlc_raw.strip())
    except ValueError as exc:
        raise LogFormatError(f"unreadable ID/DLC: {line!r}") from exc

    if dlc > 8:
        raise LogFormatError(f"DLC {dlc} > 8: {line!r}")

    try:
        data = bytes.fromhex(data_raw.replace(" ", ""))
    except ValueError as exc:
        raise LogFormatError(f"unreadable payload: {line!r}") from exc

    if len(data) != dlc:
        raise LogFormatError(f"DLC={dlc} but found {len(data)} bytes: {line!r}")

    ts_ms = int(ts_raw.strip()) if ts_raw.strip() else None
    return Frame(ts_ms, can_id, data)


def parse_line(line: str) -> Optional[Frame]:
    """Take one line apart. Returns None for lines that carry no frame.

    The format is told apart by the tab character -- format A never contains one.
    """
    line = line.rstrip("\r\n")
    if not line.strip():
        return None
    if "\t" in line:
        return _parse_viewer(line)
    return _parse_slcan(line.strip())


def iter_frames(fh, *, strict: bool = False) -> Iterator[Frame]:
    """Walk an open file (or any iterable of lines) and yield frames.

    strict=True lets LogFormatError propagate with the line number attached.
    By default a damaged line is skipped -- the USBtin occasionally truncates
    the last line when the port is closed.
    """
    for lineno, line in enumerate(fh, start=1):
        try:
            frame = parse_line(line)
        except LogFormatError as exc:
            if strict:
                raise LogFormatError(f"line {lineno}: {exc}") from exc
            continue
        if frame is not None:
            yield frame


def undouble(lines: list[str]) -> list[str]:
    """Drop the second copy when a file contains the recording exactly twice.

    Fixture 02_idle_60s.txt is damaged this way -- both halves are identical
    byte for byte. Without this correction the idle fuel rate comes out
    doubled. See test/fixtures/README.md for the details.
    """
    n = len(lines)
    if n >= 2 and n % 2 == 0 and lines[: n // 2] == lines[n // 2:]:
        return lines[: n // 2]
    return lines


def parse_file(path, *, strict: bool = False, fix_doubled: bool = False) -> list[Frame]:
    """Read a whole log.

    fix_doubled=True first checks whether the file holds the recording twice
    and discards the second copy. Turn it on for any fuel calculation; leave
    it off when checking file integrity.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        if not fix_doubled:
            frames = list(iter_frames(fh, strict=strict))
        else:
            lines = undouble(fh.read().splitlines())
            frames = list(iter_frames(lines, strict=strict))

    # Unwrap here, at the one place that sees a whole file, so that no consumer
    # has to know the adapter's counter restarts. Doing it in parse_line is not
    # possible -- a single line carries no context -- and leaving it to callers
    # is how tools/replay.py and test/logread.h ended up reporting a 60-second
    # recording as 26 ms and as 78 s respectively.
    #
    # Applied to every format, not just slcan+Z1, because it is a no-op on a
    # monotonic input by construction: only a value that goes *backwards*
    # triggers it. USBtinViewer's host timestamps run past 60000 without
    # restarting and are left exactly as they are -- pinned by
    # test_host_timestamps_past_60000_do_not_trigger_a_wrap.
    stamped = [f.ts_ms for f in frames if f.ts_ms is not None]
    if len(stamped) > 1 and any(b < a for a, b in zip(stamped, stamped[1:])):
        run = iter(unwrap_timestamps(stamped))
        frames = [f if f.ts_ms is None
                  else Frame(next(run), f.can_id, f.data)
                  for f in frames]
    return frames


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _summary(path: str, frames: list[Frame]) -> None:
    if not frames:
        print(f"{path}: no frames")
        return

    stamped = [f.ts_ms for f in frames if f.ts_ms is not None]
    # Do not label a timestamped slcan file "USBtinViewer" -- this whole
    # investigation is about not trusting the viewer's times, so saying a
    # capture came from it when it did not is worse than saying nothing.
    if not stamped:
        fmt = "slcan (no timestamps)"
    elif _looks_like_viewer(path):
        fmt = "USBtinViewer export (host timestamps -- see open question 9)"
    else:
        fmt = "slcan with Z1 (adapter timestamps)"

    print(f"{path}")
    print(f"  format : {fmt}")
    print(f"  frames : {len(frames)}")
    if stamped:
        run = unwrap_timestamps(stamped)
        wraps = (run[-1] - stamped[-1]) // TIMESTAMP_WRAP_MS
        note = f", {wraps} wrap(s) unwrapped" if wraps else ""
        print(f"  span   : {stamped[0]} .. {stamped[-1]} ms "
              f"({(run[-1] - run[0]) / 1000:.2f} s{note})")

    per_id: dict[int, int] = {}
    dlcs: dict[int, set[int]] = {}
    for f in frames:
        per_id[f.can_id] = per_id.get(f.can_id, 0) + 1
        dlcs.setdefault(f.can_id, set()).add(f.dlc)

    print("  ID      frames   DLC")
    for can_id in sorted(per_id):
        seen = ",".join(str(d) for d in sorted(dlcs[can_id]))
        print(f"  0x{can_id:03X}  {per_id[can_id]:8d}   {seen}")


def _looks_like_viewer(path: str) -> bool:
    """True if the file is a USBtinViewer table rather than a raw stream."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if line.strip():
                    return "\t" in line
    except OSError:
        pass
    return False


def frame_gaps(frames: list[Frame], can_id: int) -> list[int]:
    """Milliseconds between consecutive frames of one identifier.

    Timestamps are unwrapped first. **The statistic to read off this is the
    mode, not the mean**: a dropped frame -- and the adapter does drop them on
    a busy bus, which its status flags report -- turns one period into two,
    so losses add counts at integer multiples and never below the true period.
    The mean and the frame count are corrupted by exactly the losses the mode
    shrugs off.
    """
    stamped = [f.ts_ms for f in frames if f.ts_ms is not None]
    if len(stamped) < 2:
        return []
    run = unwrap_timestamps(stamped)
    picked = [t for t, f in zip(run, (f for f in frames if f.ts_ms is not None))
              if f.can_id == can_id]
    return [b - a for a, b in zip(picked, picked[1:])]


def _gaps_report(path: str, frames: list[Frame], wanted: Optional[set]) -> None:
    from collections import Counter

    stamped = [f for f in frames if f.ts_ms is not None]
    if len(stamped) < 2:
        print(f"{path}: no timestamps -- record with tools/usbtin_capture.py")
        return

    ids = sorted(wanted) if wanted else sorted({f.can_id for f in frames})
    print(f"{path}")
    print(f"  {'ID':>6} {'n':>6} {'mode':>6} {'2nd':>6} {'median':>7}")
    for can_id in ids:
        gaps = frame_gaps(frames, can_id)
        if not gaps:
            continue
        common = Counter(gaps).most_common(2)
        second = common[1][0] if len(common) > 1 else -1
        median = sorted(gaps)[len(gaps) // 2]
        print(f"  0x{can_id:03X} {len(gaps) + 1:6d} {common[0][0]:6d} "
              f"{second:6d} {median:7d}")

    if wanted and len(wanted) == 1:
        only = next(iter(wanted))
        gaps = frame_gaps(frames, only)
        if gaps:
            print(f"\n  histogram for 0x{only:03X}, ms : count")
            for gap, n in sorted(Counter(gaps).items()):
                print(f"  {gap:6d} : {n:5d}  {'#' * min(50, n)}")


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Parser for USBtin logs (both formats).")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--dump", action="store_true", help="print frames instead of a summary")
    ap.add_argument("--id", type=lambda s: int(s, 0), action="append",
                    help="restrict to this ID, repeatable (e.g. --id 0x480)")
    ap.add_argument("--gaps", action="store_true",
                    help="report the interval between frames of each ID -- the "
                         "measurement open question 9 wants. Needs a log with "
                         "timestamps; add --id for a histogram of one ID.")
    ap.add_argument("--strict", action="store_true", help="fail on the first damaged line")
    ap.add_argument("--fix-doubled", action="store_true",
                    help="drop the second copy when the file holds the recording twice")
    args = ap.parse_args(argv)

    wanted = set(args.id) if args.id else None

    for path in args.files:
        frames = parse_file(path, strict=args.strict, fix_doubled=args.fix_doubled)
        if args.gaps:
            # Deliberately before the --id filter: gaps are computed per ID
            # anyway, and dropping other IDs first would throw away nothing
            # but would make --id mean two different things.
            _gaps_report(path, frames, wanted)
            continue
        if wanted is not None:
            frames = [f for f in frames if f.can_id in wanted]
        if args.dump:
            for f in frames:
                print(f)
        else:
            _summary(path, frames)
    return 0


if __name__ == "__main__":
    sys.exit(main())
