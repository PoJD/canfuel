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
           "LogFormatError"]


class LogFormatError(ValueError):
    """The line looks like a frame but cannot be taken apart."""


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
    # documentation. Callers must not assume one: take differences modulo
    # nothing and let a negative difference tell you the wrap happened, or
    # read the wrap out of the first minute of a recording, which is a minute
    # of work and settles it for good.
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
            return list(iter_frames(fh, strict=strict))
        lines = undouble(fh.read().splitlines())
    return list(iter_frames(lines, strict=strict))


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _summary(path: str, frames: list[Frame]) -> None:
    if not frames:
        print(f"{path}: no frames")
        return

    stamped = [f.ts_ms for f in frames if f.ts_ms is not None]
    fmt = "USBtinViewer (timestamped)" if stamped else "slcan (no timestamps)"

    print(f"{path}")
    print(f"  format : {fmt}")
    print(f"  frames : {len(frames)}")
    if stamped:
        print(f"  span   : {stamped[0]} .. {stamped[-1]} ms ({(stamped[-1] - stamped[0]) / 1000:.2f} s)")

    per_id: dict[int, int] = {}
    dlcs: dict[int, set[int]] = {}
    for f in frames:
        per_id[f.can_id] = per_id.get(f.can_id, 0) + 1
        dlcs.setdefault(f.can_id, set()).add(f.dlc)

    print("  ID      frames   DLC")
    for can_id in sorted(per_id):
        seen = ",".join(str(d) for d in sorted(dlcs[can_id]))
        print(f"  0x{can_id:03X}  {per_id[can_id]:8d}   {seen}")


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Parser for USBtin logs (both formats).")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--dump", action="store_true", help="print frames instead of a summary")
    ap.add_argument("--id", type=lambda s: int(s, 0), action="append",
                    help="restrict to this ID, repeatable (e.g. --id 0x480)")
    ap.add_argument("--strict", action="store_true", help="fail on the first damaged line")
    ap.add_argument("--fix-doubled", action="store_true",
                    help="drop the second copy when the file holds the recording twice")
    args = ap.parse_args(argv)

    wanted = set(args.id) if args.id else None

    for path in args.files:
        frames = parse_file(path, strict=args.strict, fix_doubled=args.fix_doubled)
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
