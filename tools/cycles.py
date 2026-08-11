#!/usr/bin/env python3
"""Worst-case cycle counts for the firmware, from the XC8 assembly listing.

    python tools/cycles.py                      # the budget table
    python tools/cycles.py --check              # non-zero exit if a budget blows
    python tools/cycles.py --lst path/to.lst    # a listing from somewhere else

The reasoning behind every number, and what the budgets mean, is in
docs/timing.md. This script is the executable half of that document: the
document explains, the script re-derives, and CI runs the script.

HOW IT WORKS. `mplab/Makefile` passes -Wa,-a, so pic-as writes
mplab/build/canfuel.lst with every generated instruction, its address and its
encoding. On the PIC18 at FOSC/4 a single-word instruction is one 250 ns cycle
and a two-word instruction is two, so *counting program words gives cycles
directly* for straight-line code, understating only by taken branches. Loops
are costed by finding the backward branches, measuring the body, and
multiplying by a trip count taken from the C source -- that table is TRIPS
below and it is the part a human has to keep honest.

WHAT IT IS NOT. It is not a sound WCET analyser and it has never been checked
against a stopwatch. It cannot see how often a branch is really taken and it
trusts TRIPS. Its job is to catch something expensive being added by accident,
not to certify a deadline -- which is why the ceilings in BUDGETS are wide.
"""

import argparse
import collections
import os
import re
import sys

TCY_US = 0.25                       # 16 MHz / 4 = 4 MIPS, DS39977C pin table

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LST = os.path.join(HERE, os.pardir, "mplab", "build", "canfuel.lst")

LABEL_RE = re.compile(r"^\s*\d+\s+([0-9A-F]{6})\s+(\??[A-Za-z_]\w*):")
INSN_RE = re.compile(
    r"^\s*\d+\s+([0-9A-F]{6})\s+([0-9A-F]{4})(?:\s+([0-9A-F]{4}))?\s+\t?\s*([a-z]+)\b(.*)$"
)
BRANCHES = {"bra", "bz", "bnz", "bc", "bnc", "bn", "bnn", "bov", "bnov", "goto"}

# Loop trip counts, worst case, each one read out of the C source. The pair is
# (body size in words, extra iterations beyond the first) -- so a loop that runs
# n times contributes body * (n - 1) on top of the function's own size.
#
# Only loops that are really loops in the source belong here. A backward branch
# is not proof of one: XC8 emits them for ordinary control flow too, and
# decode_frame's switch is the obvious example.
TRIPS = {
    "___lldiv": (31, 31),            # one iteration per bit of a 32-bit divisor
    "_tank_median": (50, 299),       # insertion sort, n(n-1)/2 at n = 25 slots
    "_compute_range_km": (33, 29),   # RANGE_SEGMENTS
    "_flow_push": (33, 31),          # FLOW_WINDOW_SLOTS
    "_persist_load": (47, 63),       # PERSIST_SLOTS, start-up only
    "_hal_can_receive": (19, 7),     # bytes in a frame
    "_decode_rec": (4, 11),          # PERSIST_RECORD_BYTES
    "_encode": (4, 11),
    "_slot_write": (4, 11),
}

# name -> (what it is, ceiling in microseconds). Wide on purpose: these catch a
# millisecond-scale mistake, not a regression of a few per cent.
BUDGETS = {
    "rx_frame": ("one received frame, decoded and accumulated", 5000.0),
    "compute_tick": ("compute_tick, worst case (tank median)", 20000.0),
    "fast_slot": ("the 100 ms slot, everything in it", 25000.0),
    "slow_slot": ("the 1 s slot, excluding the EEPROM write", 5000.0),
}


def parse(path):
    """-> (words per function, calls per function, listing order)."""
    words = collections.Counter()
    calls = collections.defaultdict(collections.Counter)
    current = None

    with open(path, encoding="latin-1") as handle:
        for line in handle:
            match = LABEL_RE.match(line)
            if match and " equ " not in line:
                if match.group(2).startswith("_"):
                    current = match.group(2)
                    words.setdefault(current, 0)
                continue

            match = INSN_RE.match(line)
            if match and current:
                words[current] += 2 if match.group(3) else 1
                if match.group(4) in ("call", "rcall"):
                    target = re.match(r"(_\w*)", match.group(5).strip())
                    if target:
                        calls[current][target.group(1)] += 1

    return words, calls


def self_cycles(name, words):
    cycles = words.get(name, 0)
    if name in TRIPS:
        body, extra = TRIPS[name]
        cycles += body * extra
    return cycles


def total_cycles(name, words, calls, seen=()):
    """Cycles for a function including everything it calls. Recursion is not
    possible here -- -mstack=compiled would not survive it -- but the guard
    keeps a cycle in the call graph from hanging the tool."""
    if name in seen or name not in words:
        return 0
    cycles = self_cycles(name, words)
    for callee, count in calls[name].items():
        # +4 for the call and the return themselves, both two-cycle.
        cycles += count * (total_cycles(callee, words, calls, seen + (name,)) + 4)
    return cycles


def budgets(words, calls):
    def cost(name):
        return total_cycles(name, words, calls)

    rx_frame = cost("_hal_can_receive") + cost("_decode_frame") + cost("_compute_on_fuel")

    fast_slot = (
        cost("_hal_sys_vdd_c")
        + 88                                    # 22 us of A/D conversion, DS39977C 23.5
        + cost("_txframes_gather")
        + cost("_txframes_fuel")
        + cost("_txframes_engine")
        + 2 * cost("_hal_can_send")
        + cost("_leds_update")
    )

    slow_slot = cost("_txframes_trip") + cost("_hal_can_send") + cost("_persist_save")

    return {
        "rx_frame": rx_frame,
        "compute_tick": cost("_compute_tick"),
        "fast_slot": fast_slot,
        "slow_slot": slow_slot,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lst", default=DEFAULT_LST,
                        help="assembly listing (default: mplab/build/canfuel.lst)")
    parser.add_argument("--check", action="store_true",
                        help="exit non-zero if any budget is over its ceiling")
    parser.add_argument("--top", type=int, default=18,
                        help="how many functions to list (default 18)")
    args = parser.parse_args()

    if not os.path.exists(args.lst):
        sys.stderr.write(
            "no listing at %s\n"
            "build it first:  make -C mplab\n" % args.lst)
        return 2

    words, calls = parse(args.lst)
    if not words:
        sys.stderr.write("%s parsed to nothing -- is it a pic-as listing?\n" % args.lst)
        return 2

    ranked = sorted(words, key=lambda f: -total_cycles(f, words, calls))
    print("%-26s %9s %11s" % ("function", "cycles", "time"))
    for name in ranked[:args.top]:
        cycles = total_cycles(name, words, calls)
        print("%-26s %9d %8.1f us" % (name.lstrip("_"), cycles, cycles * TCY_US))

    print()
    failed = []
    for key, cycles in budgets(words, calls).items():
        what, ceiling = BUDGETS[key]
        micros = cycles * TCY_US
        over = micros > ceiling
        if over:
            failed.append((what, micros, ceiling))
        print("%-46s %8.2f ms   (ceiling %5.1f ms) %s"
              % (what, micros / 1000.0, ceiling / 1000.0, "OVER" if over else "ok"))

    if args.check and failed:
        print()
        for what, micros, ceiling in failed:
            print("FAIL: %s takes %.2f ms, ceiling is %.2f ms"
                  % (what, micros / 1000.0, ceiling / 1000.0))
        print("If the cost is intended, raise the ceiling in tools/cycles.py and "
              "say why in docs/timing.md.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
