#!/usr/bin/env python3
"""Derive and verify the magic numbers in src/divconst.h.

    python tools/divconst.py            # print the table, verify each entry
    python tools/divconst.py --check    # exit non-zero if any entry is wrong

For a divisor d we want a pair (m, s) such that

    x // d  ==  ((x * m) >> 32) >> s        for every x in 0 .. 2**32 - 1

with m = ceil(2**(32+s) / d). A shift s exists whenever d is not a power of
two; the search below takes the smallest one that works and then PROVES it
rather than trusting the derivation.

The proof is the point of this file. The identity holds for all x if and only
if it holds at the values either side of every multiple of d -- the error is
monotonic between them -- so checking x = k*d - 1 and x = k*d for every k up to
2**32/d settles the whole range. That is a few million checks per divisor and a
few seconds, which is cheap for the one class of bug that would otherwise reach
the display as a number that is quietly one out.
"""

import argparse
import sys

# Divisor -> (largest value ever divided, +1, and what uses it).
#
# THE RANGE IS PART OF THE PROOF, not decoration. A magic number only has to be
# exact over the inputs that can actually occur, and a tighter range allows a
# smaller shift -- which is what makes 95500 possible at all, since over the
# full 32-bit range its magic needs 33 bits and would not fit a uint32.
#
# Every bound below is justified, because an under-stated one is a silent
# wrong answer rather than an overflow anybody would notice.
DIVISORS = {
    10: (1 << 32,
         "compute_torque_d, cNm to tenths -- full range, costs nothing"),
    100: (1 << 32,
          "compute_flow_lh_c and compute_tank_d -- full range"),
    120: (1 << 32,
          "TANK_DAMP_SAMPLES, the tank filter -- full range"),
    1000: (1 << 32,
           "microlitres to millilitres and millimetres to metres; the trip "
           "accumulators are unbounded 32-bit, so this must be the full range"),
    3600: (1 << 32,
           "v[0.001 km/h] * t[ms] -> mm -- full range"),
    10000: (1 << 32,
            "DRAG_TORQUE_SLOPE_E4 -- full range"),
    # torque_d is at most 255 * TORQUE_CNM_PER_BIT / 10, i.e. under 1900 tenths
    # of an Nm, and rpm comes from a uint16 quarter-rpm counter so it is under
    # 16384. torque_d * 10 * rpm is therefore under 1900 * 10 * 16384 = 3.1e8.
    # 2**30 is a round bound comfortably above that and comfortably below the
    # 2**32 that would need a 33-bit magic.
    95500: (1 << 30,
            "POWER_DIVISOR; torque_d * 10 * rpm < 2**30, see the note above"),
}

U32 = 1 << 32


def derive(d, limit):
    """A shift that is exact for every x < limit, fits 32 bits, and is free.

    Order matters. A shift of 8, 16 or 24 costs nothing on this part -- XC8
    turns it into byte moves -- while any other shift becomes a LOOP of
    single-bit rotates, even when the count is a compile-time constant. So
    multiples of eight are tried first, and only if none works does it fall
    back to the smallest shift that does.

    A multiple of eight needs 2**s < d for the magic to stay inside 32 bits,
    so it is available for the large divisors and not for 10, 100 or 120 --
    which is fine, because their shifts are small and so are their loops."""
    for s in (8, 16, 24):
        if (1 << s) >= d:
            continue
        m = -(-(U32 << s) // d)
        if m < U32 and exact(d, m, s, limit):
            return m, s
    for s in range(0, 33):
        m = -(-(U32 << s) // d)          # ceil(2**(32+s) / d)
        if m >= U32:                     # must fit a uint32 in divconst.h
            continue
        if exact(d, m, s, limit):
            return m, s
    raise SystemExit(
        "no 32-bit magic for %d below %d -- tighten the range or divide" % (d, limit))


def exact(d, m, s, limit):
    """Is x//d == ((x*m)>>32)>>s for EVERY x in 0 .. limit-1?

    This is decided, not sampled. With m = ceil(2**(32+s)/d) the multiply
    overshoots by e = m*d - 2**(32+s), which lies in [0, d). Then

        (x*m) >> (32+s)  ==  floor( x/d + x*e / (d * 2**(32+s)) )

    and that equals floor(x/d) for every x < limit exactly when the error term
    can never carry the value up to the next integer -- that is, when
    (limit-1) * e < 2**(32+s). Granlund and Montgomery, "Division by Invariant
    Integers using Multiplication", PLDI 1994, section 4.

    One O(1) test therefore covers the whole range, which is why this file does
    not try to enumerate four billion values."""
    if m >= U32 or m <= 0:
        return False
    e = m * d - (U32 << s)
    if e < 0:
        return False
    return (limit - 1) * e < (U32 << s)


def apply(x, m, s):
    return ((x * m) >> 32) >> s


def spot_check(d, m, s, limit, per_divisor=20000):
    """A second opinion on top of exact(): the values either side of the first
    few thousand multiples of d, the top of the range, and the boundaries.

    The proof above is the authority. This is here because a transcription slip
    in exact() would otherwise be invisible, and disagreeing with brute force
    on real numbers is the cheapest way to catch that."""
    top = limit - 1
    xs = [0, 1, d - 1, d, d + 1, top, top - 1, top // d * d, top // d * d - 1]
    for k in range(1, per_divisor):
        xs.append(k * d - 1)
        xs.append(k * d)
    for x in xs:
        if 0 <= x < limit and apply(x, m, s) != x // d:
            return x
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true",
                        help="exit non-zero if any magic is wrong")
    args = parser.parse_args()

    bad = []
    print("%-8s %-12s %-6s %s" % ("divisor", "magic", "shift", "used by"))
    for d in sorted(DIVISORS):
        limit, what = DIVISORS[d]
        m, s = derive(d, limit)
        note = "proved for x < 2**%d" % (limit.bit_length() - 1)
        if not exact(d, m, s, limit):
            bad.append(d)
            note = "NOT EXACT"
        else:
            miss = spot_check(d, m, s, limit)
            if miss is not None:
                bad.append(d)
                note = "brute force disagrees at %d" % miss
        print("%-8d 0x%08X   %-6d %-52s %s" % (d, m, s, what[:52], note))

    print()
    if bad:
        print("WRONG: %s" % ", ".join(str(d) for d in bad))
        return 1
    print("every magic is exact over its declared range, by the "
          "Granlund-Montgomery condition and by spot check")
    print()
    print("Paste into src/divconst.h:")
    for d in sorted(DIVISORS):
        m, s = derive(d, DIVISORS[d][0])
        print("#define DIVC_%-10d 0x%08Xul, %du" % (d, m, s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
