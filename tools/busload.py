#!/usr/bin/env python3
"""How much of the 500 kbps bus the car uses, and how much the converter adds.

    python tools/busload.py test/fixtures/09_idle_60s_z1.txt
    python tools/busload.py test/fixtures/17_drive_property_z1.txt
    python tools/busload.py --bursts test/fixtures/17_drive_property_z1.txt

Every frame of a `_z1` capture is counted on the wire exactly as the bus
carries it: an 11-bit data frame is 44 + 8 * DLC bits from SOF to the end of
EOF, plus 3 bits of intermission, plus the stuff bits -- and those are not
estimated, they are counted, by building each frame's bit stream (CRC-15
included) and inserting a stuff bit after every five equal ones. Load is that
total over the capture's span, against 500,000 bit/s.

The converter's own frames are not in any capture (the MFD and the USBtin are
one or the other), so they are added from the schedule: two fast frames each
at `TX_SLOTS_PER_SEC / 4` a second, 0x602 and 0x604 once a second, and 0x603
once a second only with JP1 (`src/config.h`, *timing*). Their stuffing is the
mean of the capture's own 8-byte frames; the worst case is printed beside it.

Only a capture with every identifier says anything: the later fixtures are
filtered to the six the converter reads, and this refuses those. And the
count is a floor -- a frame the adapter missed is load the car still carried.

--bursts looks inside the average, at the adapter's 1 ms resolution: the
longest silence between two frames, the most bits stamped in one millisecond,
the peak load over windows of a few milliseconds, and what one converter
frame does when it lands in the car's densest millisecond. The adapter's
MCP2515 has two receive buffers and has been seen to lose the third frame of
a fast burst (`src/config.h`, *timing*), so the densest milliseconds are the
ones most likely undercounted.
"""

from __future__ import annotations

import argparse
from collections import Counter
import re
import sys
from pathlib import Path

from canlog import parse_file

ROOT = Path(__file__).resolve().parent.parent
BITRATE = 500_000
TX_DLC = 8
# A filtered fixture carries only these; a full capture carries more.
CONVERTER_READS = {0x1A0, 0x280, 0x288, 0x320, 0x420, 0x480}


def config_int(name: str) -> int:
    text = (ROOT / "src" / "config.h").read_text(encoding="utf-8")
    m = re.search(rf"#define\s+{name}\s+(\d+)", text)
    if not m:
        raise SystemExit(f"{name} not found in src/config.h")
    return int(m.group(1))


def crc15(bits: list[int]) -> int:
    crc = 0
    for b in bits:
        nxt = b ^ ((crc >> 14) & 1)
        crc = (crc << 1) & 0x7FFF
        if nxt:
            crc ^= 0x4599
    return crc


def stuff_bits(can_id: int, data: bytes) -> int:
    """Stuff bits in an 11-bit data frame, SOF to the end of the CRC."""
    bits = [0] + [(can_id >> i) & 1 for i in range(10, -1, -1)]
    bits += [0, 0, 0]                                   # RTR, IDE, r0
    bits += [(len(data) >> i) & 1 for i in range(3, -1, -1)]
    for byte in data:
        bits += [(byte >> i) & 1 for i in range(7, -1, -1)]
    crc = crc15(bits)
    bits += [(crc >> i) & 1 for i in range(14, -1, -1)]
    stuffed, run, last = 0, 1, bits[0]
    for b in bits[1:]:
        if b == last:
            run += 1
        else:
            run, last = 1, b
        if run == 5:
            stuffed += 1
            last, run = 1 - b, 1                         # the stuff bit starts a run
    return stuffed


def frame_bits(can_id: int, data: bytes) -> int:
    """Bits on the wire, intermission included."""
    return 44 + 8 * len(data) + 3 + stuff_bits(can_id, data)


def worst_stuff(dlc: int) -> int:
    return (34 + 8 * dlc - 1) // 4


def converter_rates() -> dict[str, float]:
    fast = config_int("TX_SLOTS_PER_SEC") / 4
    return {"always": 2 * fast + 2, "jp1": 1}


def measure(path: str) -> dict:
    frames = parse_file(path)
    if not frames or frames[0].ts_ms is None:
        raise ValueError(f"{path}: needs adapter timestamps (a _z1 capture)")
    ids = {f.can_id for f in frames}
    if ids <= CONVERTER_READS:
        raise ValueError(f"{path}: filtered to the converter's identifiers")
    span_s = (frames[-1].ts_ms - frames[0].ts_ms) / 1000
    total = 0
    per_id: dict[int, int] = {}
    stuff8: list[int] = []
    for f in frames:
        bits = frame_bits(f.can_id, f.data)
        total += bits
        per_id[f.can_id] = per_id.get(f.can_id, 0) + bits
        if len(f.data) == TX_DLC:
            stuff8.append(stuff_bits(f.can_id, f.data))
    mean_stuff = sum(stuff8) / len(stuff8)
    base = 44 + 8 * TX_DLC + 3
    rates = converter_rates()
    return {
        "span_s": span_s,
        "frames_per_s": len(frames) / span_s,
        "car_bps": total / span_s,
        "per_id_bps": {k: v / span_s for k, v in per_id.items()},
        "conv_bps": rates["always"] * (base + mean_stuff),
        "conv_worst_bps": rates["always"] * (base + worst_stuff(TX_DLC)),
        "jp1_bps": rates["jp1"] * (base + mean_stuff),
        "conv_frames_per_s": rates["always"],
    }


WINDOWS_MS = (1, 2, 5, 10, 25, 100)


def bursts(path: str) -> dict:
    frames = parse_file(path)
    if not frames or frames[0].ts_ms is None:
        raise ValueError(f"{path}: needs adapter timestamps (a _z1 capture)")
    if {f.can_id for f in frames} <= CONVERTER_READS:
        raise ValueError(f"{path}: filtered to the converter's identifiers")
    t0, t1 = frames[0].ts_ms, frames[-1].ts_ms
    per_ms = [0] * (t1 - t0 + 1)
    for f in frames:
        per_ms[f.ts_ms - t0] += frame_bits(f.can_id, f.data)
    peak = {}
    for w in WINDOWS_MS:
        run = best = sum(per_ms[:w])
        for i in range(w, len(per_ms)):
            run += per_ms[i] - per_ms[i - w]
            best = max(best, run)
        peak[w] = 100 * best / (w * BITRATE / 1000)
    gaps = [b.ts_ms - a.ts_ms for a, b in zip(frames, frames[1:])]
    worst_tx = 44 + 8 * TX_DLC + 3 + worst_stuff(TX_DLC)
    return {
        "longest_gap_ms": max(gaps),
        "empty_ms_pct": 100 * per_ms.count(0) / len(per_ms),
        "most_frames_in_1ms": max(Counter(f.ts_ms for f in frames).values()),
        "peak_pct": peak,
        "ms_over_80_pct": sum(b > 0.8 * BITRATE / 1000 for b in per_ms),
        "ms_total": len(per_ms),
        "tx_worst_us": worst_tx * 1e6 / BITRATE,
        "densest_plus_tx_pct": 100 * (max(per_ms) + worst_tx) / (BITRATE / 1000),
    }


def pct(bps: float) -> float:
    return 100 * bps / BITRATE


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--bursts", action="store_true",
                    help="silences and bursts at 1 ms resolution")
    args = ap.parse_args(argv)
    for path in args.files:
        if args.bursts:
            try:
                b = bursts(path)
            except ValueError as e:
                print(e, file=sys.stderr)
                return 1
            print(f"{path}:")
            print(f"  longest silence    {b['longest_gap_ms']} ms between two frames;"
                  f" {b['empty_ms_pct']:.0f} % of milliseconds empty")
            print(f"  densest            {b['most_frames_in_1ms']} frames in one ms;"
                  f" {b['ms_over_80_pct']} of {b['ms_total']} ms over 80 %")
            print("  peak load          " + ", ".join(
                f"{w} ms {v:.0f} %" for w, v in b["peak_pct"].items()))
            print(f"  one converter frame {b['tx_worst_us']:.0f} us at worst; in the"
                  f" densest ms it makes {b['densest_plus_tx_pct']:.0f} %")
            continue
        try:
            m = measure(path)
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1
        top = sorted(m["per_id_bps"].items(), key=lambda kv: -kv[1])[:5]
        print(f"{path}: {m['span_s']:.0f} s, {m['frames_per_s']:.0f} frames/s")
        print(f"  the car      {m['car_bps']:7.0f} bit/s  {pct(m['car_bps']):5.2f} %")
        print(f"  + converter  {m['conv_bps']:7.0f} bit/s  {pct(m['conv_bps']):5.2f} %"
              f"  ({m['conv_frames_per_s']:.0f} frames/s; worst-case stuffing "
              f"{pct(m['conv_worst_bps']):.2f} %)")
        print(f"  + 0x603, JP1 {m['jp1_bps']:7.0f} bit/s  {pct(m['jp1_bps']):5.2f} %")
        print(f"  together     {pct(m['car_bps'] + m['conv_bps']):5.2f} %")
        print("  heaviest     " + ", ".join(f"0x{k:03X} {pct(v):.1f} %" for k, v in top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
