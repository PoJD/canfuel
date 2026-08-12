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
directly* for straight-line code, understating only by taken branches.

LOOPS ARE MEASURED, NOT REMEMBERED. A branch whose target label appears earlier
in the same function is a backward branch, so the words between the two are the
body -- read out of the listing rather than written down here. Only the trip
count is declared, in LOOPS below, and it names the config.h constant that
bounds it wherever one exists. This matters: the bodies used to be written down
by hand, and when tank_median stopped being an insertion sort the table went on
describing the sort, so the tool reported a new algorithm as costing exactly
what the old one had.

AND EVERY LOOP MUST BE DECLARED. Each backward branch in the build has to
appear in LOOPS (costed), HARDWARE_WAITS (spinning on a peripheral) or
NOT_LOOPS (ordinary control flow), and a LOOPS entry whose loop has vanished is
an error too. The tool stops rather than guessing, which is what makes a change
of algorithm impossible to slip past unnoticed.

WHAT IT IS NOT. It is not a sound WCET analyser and it has never been checked
against a stopwatch. It cannot see how often a branch is really taken, and it
costs a nested loop as outer x inner, which overstates a triangular one. Its
job is to catch something expensive being added by accident, not to certify a
deadline.

docs/optimisation.md is required reading before changing any loop in the core.
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

# Loops. ONLY the trip count lives here; the body is measured from the listing.
#
# This used to carry the body size by hand as well, and that was a trap rather
# than a shortcut: when tank_median stopped being an insertion sort the entry
# still said (50, 299), so the tool reported the new algorithm as costing
# exactly what the old one had. It measured a model of code that no longer
# existed and nothing complained. Now find_loops() measures the real body out
# of the real listing, so a change in the *code* needs no edit here at all.
#
# What still cannot be measured is how many times a loop runs -- that is
# semantics, not instructions. So each entry names the config.h constant that
# bounds it, and the value is read from config.h at run time. Change
# FLOW_BUCKETS and this follows on its own.
#
# ("CONSTANT", None)  -> iterations = that constant from src/config.h
# (None, n)           -> iterations = n, for bounds that are not ours to name
# Each entry is the list of loops in that function, OUTERMOST FIRST. Nesting is
# worked out from the addresses, and an inner loop's cost is multiplied by every
# loop that encloses it -- persist_crc16 is 10 bytes each of 8 bits, and costing
# it as a single loop would understate it eightfold.
LOOPS = {
    "___lldiv":          [(None, 32,                  "one per bit of a 32-bit divisor")],
    # ___lmul was here until 2026-08-12 and is gone from the build entirely:
    # every multiply in the core now goes through fastmul.h. If it comes back,
    # something reintroduced a plain 32-bit product.
    # _tank_median was here until 2026-08-12, first as an insertion sort and
    # then as a 128-bucket histogram sweep. The refuelling rule does not need a
    # median at all -- see docs/optimisation.md -- so the function is gone and
    # with it the last data structure the core walked once a second.
    # _compute_range_km was here until 2026-08-12, summing a 30-slot ring of
    # microlitre totals ten times a second for a number that can only change
    # once a kilometre. The basis is a filter now and the sweep is gone.
    "_flow_push":        [("FLOW_BUCKETS", None,     "the four buckets, summed when one closes")],
    "_persist_load":     [("PERSIST_SLOTS", None,     "start-up only")],
    "_hal_can_receive":  [(None, 8,                   "bytes in a frame")],
    "_tx_load":          [(None, 8,                   "dlc, and ours is always 8")],
    "_slot_read":        [("PERSIST_RECORD_BYTES", None, "")],
    "_slot_write":       [("PERSIST_RECORD_BYTES", None, "")],
    "_persist_crc16":    [(None, 10,                  "CRC_OFFSET bytes"),
                          (None, 8,                   "bits per byte")],
    # The shift inside div_const(). XC8 emits single-bit rotates with a counter
    # even for a constant shift, so any shift that is not a multiple of eight is
    # a loop. divconst.py picks a free shift wherever it can; these two divide
    # by 100, where 2**8 > 100 makes that impossible, so they keep a 5-iteration
    # rotate. If either stops appearing here, divconst.h changed shift.
    "_compute_tank_d":    [(None, 5,                  "DIVC_100 shift")],
    "_compute_flow_lh_c": [(None, 5,                  "DIVC_100 shift")],
    # The same thing again, and for the same reason: RANGE_BASIS_Q4 and
    # RANGE_BASIS_SHIFT are both 4, and a shift that is not a multiple of eight
    # is a rotate loop with a counter even when the count is a literal. Four
    # iterations of two bytes each, so a few dozen cycles -- costed rather than
    # waved away, because a shift that quietly became a divide would look
    # exactly like this and cost thirty times as much.
    "_compute_range_km":     [("RANGE_BASIS_Q4", None,    "rotate, basis back to tenths")],
    "_range_basis_update":   [("RANGE_BASIS_SHIFT", None, "rotate, the filter step")],
}

# Loops that spin waiting for a peripheral, not for the CPU. Their duration is
# set by hardware -- an A/D conversion, an EEPROM write -- so counting their
# instructions would say nothing useful, and the budgets account for the wait
# itself where it matters (fast_slot adds the A/D time as a constant, and the
# EEPROM write is excluded from slow_slot by name and analysed in timing.md).
HARDWARE_WAITS = {
    "_hal_sys_vdd_c":    "waits for ADCON0bits.GO",
    "_adc_init":         "50 us for the band gap, start-up only",
    "_hal_eeprom_write": "waits for EECON1bits.WR, ~4 ms typ and unbounded",
    "_can_set_mode":     "waits for OPMODE to be acknowledged, start-up only",
}

# Functions with a backward branch that is NOT a loop. XC8 emits them for
# ordinary control flow -- decode_frame's switch is the obvious case -- and
# listing them here is what lets the tool insist that every *other* backward
# branch is accounted for above.
NOT_LOOPS = {
    "_decode_frame",
    "_main",
    "_txframes_gather",
    "_compute_tick",
    "_tank_sample",
    "_persist_save",
    "_persist_save_now",
    "_hal_can_init",
    "_hal_sys_init",
    "_ports_init",
    "_leds_update",
    "_compute_on_fuel",
    # Has DIVC_10 (shift 3) and DIVC_10000 (shift 13) inline, so its widest
    # backward branch is a rotate loop rather than control flow. Costed as a
    # loop below would need two entries and the spans are not reliably ordered
    # against its switch; the two rotates together are under 80 cycles against
    # 530 for the two mulhi calls, so this is listed here and the shortfall is
    # named rather than hidden.
    "_compute_torque_d",
    "_can_set_filter",
    "_memset",
    "__initialization",
}

# name -> (what it is, ceiling in microseconds).
#
# These are deliberately tighter than the headroom the hardware allows, because
# a ceiling that can never be hit is not a gate. They sit roughly 1.5x above
# what the code costs today, which is enough room for an honest change and not
# enough to hide a millisecond arriving by accident. The real hardware limits
# are in docs/timing.md; these are a regression alarm, not a deadline.
BUDGETS = {
    "rx_frame": ("one received frame, decoded and accumulated", 1000.0),
    "compute_tick": ("compute_tick, worst case (with the tank sample)", 1000.0),
    "fast_slot": ("the 100 ms slot, everything in it", 3600.0),
    "slow_slot": ("the 1 s slot, excluding the EEPROM write", 1500.0),
}


def read_constants(path):
    """The #define values in src/config.h, so a loop bound has one home."""
    out = {}
    define = re.compile(r"^#define\s+(\w+)\s+(\d+)")
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            match = define.match(line)
            if match:
                out[match.group(1)] = int(match.group(2))
    return out


def parse(path):
    """-> (words per function, calls per function, loop body words per function).

    The third one is what stops this tool measuring the past. Every label and
    every instruction carries its address, so a branch whose target address is
    below the branch itself is a backward branch -- a loop. The words between
    the target label and the branch are the body, measured rather than
    remembered."""
    words = collections.Counter()
    calls = collections.defaultdict(collections.Counter)
    loops = collections.defaultdict(list)
    current = None
    labels = {}                 # label -> (address, words seen in function so far)
    running = 0                 # words emitted in the current function

    with open(path, encoding="latin-1") as handle:
        for line in handle:
            match = LABEL_RE.match(line)
            if match and " equ " not in line:
                name = match.group(2)
                if name.startswith("_"):
                    current = name
                    words.setdefault(current, 0)
                    labels = {}
                    running = 0
                elif current:
                    labels[name] = running
                continue

            match = INSN_RE.match(line)
            if match and current:
                size = 2 if match.group(3) else 1
                words[current] += size
                running += size
                op, rest = match.group(4), match.group(5).strip()

                if op in ("call", "rcall"):
                    target = re.match(r"(_\w*)", rest)
                    if target:
                        calls[current][target.group(1)] += 1
                elif op in BRANCHES:
                    target = re.match(r"(\w+)", rest)
                    if target and target.group(1) in labels:
                        # Backward: the label was emitted earlier in this
                        # function. The body spans from it up to and including
                        # this branch; keep both ends so nesting can be seen.
                        start = labels[target.group(1)]
                        loops[current].append((start, running))

    return words, calls, loops


def loop_iterations(name, spec, constants):
    const, literal, _ = spec
    if const is not None:
        if const not in constants:
            raise SystemExit(
                "cycles.py: %s is bounded by %s, which is not a #define in "
                "src/config.h any more. Fix the LOOPS table." % (name, const))
        return constants[const]
    return literal


def self_cycles(name, words, loops, constants):
    """The function's own instructions, plus what its loops repeat.

    Measured bodies, declared trip counts. Loops are matched to the LOOPS entry
    by nesting depth -- outermost first -- and an inner loop is multiplied by
    every loop that contains it."""
    cycles = words.get(name, 0)
    found = loops.get(name)
    if name not in LOOPS or not found:
        return cycles

    # Widest span first, and take as many as the table declares. XC8 emits
    # backward branches for ordinary control flow inside a loop as well -- an
    # `if` at the end of a body is one -- so more spans than loops is normal
    # and the big ones are the real loops. FEWER is not normal: it means a loop
    # this table still costs has gone, which is exactly the case that used to
    # slip through, so that stops the tool.
    specs = LOOPS[name]
    ordered = sorted(found, key=lambda span: span[0] - span[1])[:len(specs)]
    if len(ordered) < len(specs):
        raise SystemExit(
            "cycles.py: %s has %d loops in the listing but %d in the LOOPS "
            "table. The code changed shape -- read docs/optimisation.md, then "
            "fix the table." % (name, len(ordered), len(specs)))

    for i, (start, end) in enumerate(ordered):
        body = end - start
        repeats = loop_iterations(name, specs[i], constants) - 1
        # Multiply by every loop that encloses this one.
        for j, (outer_start, outer_end) in enumerate(ordered):
            if j != i and outer_start <= start and end <= outer_end:
                repeats *= loop_iterations(name, specs[j], constants)
        cycles += body * repeats
    return cycles


def audit(words, loops):
    """Every measured loop must be accounted for, in one table or the other.

    This is the part that makes a change of algorithm impossible to slip past:
    a new loop in a costed function, or a costed loop that has disappeared,
    both stop the tool rather than quietly changing a number."""
    problems = []
    for name in LOOPS:
        if name not in words:
            problems.append("%s is in LOOPS but not in the listing -- renamed "
                            "or gone?" % name)
        elif not loops.get(name):
            problems.append("%s is in LOOPS but has no backward branch any "
                            "more. If the loop went away, take it out of "
                            "LOOPS; if it changed shape, check the bound."
                            % name)
    for name in loops:
        if name not in LOOPS and name not in NOT_LOOPS and name not in HARDWARE_WAITS:
            problems.append("%s has a backward branch and is in neither LOOPS "
                            "nor NOT_LOOPS. Decide which: a real loop needs a "
                            "trip count, anything else needs listing as not a "
                            "loop." % name)
    return problems


def total_cycles(name, words, calls, loops, constants, seen=()):
    """Cycles for a function including everything it calls. Recursion is not
    possible here -- -mstack=compiled would not survive it -- but the guard
    keeps a cycle in the call graph from hanging the tool."""
    if name in seen or name not in words:
        return 0
    cycles = self_cycles(name, words, loops, constants)
    for callee, count in calls[name].items():
        # +4 for the call and the return themselves, both two-cycle.
        cycles += count * (total_cycles(callee, words, calls, loops, constants,
                                        seen + (name,)) + 4)
    return cycles


def budgets(words, calls, loops, constants):
    def cost(name):
        return total_cycles(name, words, calls, loops, constants)

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

    # txframes_gather_trip is the two divisions by 1000 that used to sit in the
    # fast slot, where nine out of ten of them were computed for nobody. They
    # are part of this budget now, not that one.
    slow_slot = (cost("_txframes_gather_trip") + cost("_txframes_trip")
                 + cost("_hal_can_send") + cost("_persist_save"))

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

    words, calls, loops = parse(args.lst)
    if not words:
        sys.stderr.write("%s parsed to nothing -- is it a pic-as listing?\n" % args.lst)
        return 2

    constants = read_constants(os.path.join(HERE, os.pardir, "src", "config.h"))

    problems = audit(words, loops)
    if problems:
        sys.stderr.write("the loop tables no longer match the code:\n")
        for problem in problems:
            sys.stderr.write("  - %s\n" % problem)
        sys.stderr.write("\nRead docs/optimisation.md before touching either "
                         "table.\n")
        return 2

    def cost(name):
        return total_cycles(name, words, calls, loops, constants)

    ranked = sorted(words, key=cost, reverse=True)
    print("%-26s %9s %11s" % ("function", "cycles", "time"))
    for name in ranked[:args.top]:
        cycles = cost(name)
        print("%-26s %9d %8.1f us" % (name.lstrip("_"), cycles, cycles * TCY_US))

    print()
    failed = []
    for key, cycles in budgets(words, calls, loops, constants).items():
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
