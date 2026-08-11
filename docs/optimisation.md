# Optimisation — what was done, and the rules for doing more

**Read this before changing any loop or any arithmetic in `src/`.** Cycles are
expensive on this part in a way they are not on a desktop: 4 MIPS, no cache, no
barrel shifter, no hardware divide. A line of C that looks free can cost a
quarter of a millisecond.

`docs/timing.md` is the budget — what each piece costs and how much room there
is. This document is the other half: *why* the code is shaped the way it is,
what was tried, and what is deliberately left alone.

---

## The rule

**Correctness first, and it is not negotiable.** Every optimisation here left
the numbers bit-for-bit identical, and that was checked rather than assumed:
`make -C test test`, the Python suite, and above all
`python tools/replay.py --host-build test/fixtures/*.txt`, which replays every
recording through both the C core and the Python reference and diffs the
totals. An optimisation that changes a displayed value is a bug, however fast
it is.

**Bytes are cheap, cycles are not.** The part has 32 KB of program memory and
uses about a third. Trading size for speed is nearly always right here — the
histogram below spends 128 bytes of RAM to remove 12,600 cycles.

**Measure, do not reason.** `python tools/cycles.py` costs every function out
of the real assembly listing. Twice now the intuition was wrong and the tool
was right.

---

## What was done, 2026-08-11

### 1. The tank median stopped sorting — 19,870 → 2,453 cycles, 8.1x

`tank_median()` was an insertion sort over the 25-slot ring: worst case a
reversed ring, 300 comparisons and moves, plus a 25-byte `memcpy`. It was the
largest single item in the core and the *only* cost in the firmware that
depended on the data rather than on the code — a sorted ring cost 25
comparisons, a reversed one twelve times that.

**Both figures below are measured with the current tool**, the old code
included: the pre-optimisation core was checked out, rebuilt and re-measured so
the comparison is like for like.

**The insight is that we never wanted the sorted array, only the middle
element**, and the key is a tank level masked to seven bits: 0..127. A small,
fixed, known key space means counting beats comparing. `tank_sample()` now
maintains a 128-bucket histogram as samples enter and leave the ring, and the
median is a single sweep with a running total.

Same answer as before, and the equivalence is worth stating: the sort returned
`sorted[n/2]`, which for even `n` is the upper of the two middle elements; the
first bucket whose cumulative count exceeds `n/2` is by definition the bucket
that index `n/2` falls in.

**It costs 128 bytes of RAM and removes the data dependence entirely.** The
bound is now a property of the code.

### 2. Two changes inside that loop, worth as much as the algorithm

The first version of the histogram was barely faster than the sort it
replaced, and the algorithm was not the problem. Two things were wrong with the
loop body, and both generalise to any hot loop on this part:

- **`cum` and `target` were `uint16_t`.** The ring holds at most 25 samples, so
  neither can overflow a byte. A 16-bit compare cost **six extra instructions
  per bucket**. Types are not free on an 8-bit machine — use the narrowest that
  provably holds the value, and say why it holds in a comment.
- **`tank_bins[v]` made XC8 rebuild the address from the struct base on every
  iteration** — twelve instructions of `lfsr` and `addwf` — where a walking
  pointer it can simply increment costs one `infsnz`. **Prefer a walking
  pointer to an index in a hot loop.**

The body went from 33 words to 19.

### 3. Modulo on ring buffers → compare

`% TANK_MEDIAN_SLOTS` (25) and `% RANGE_SEGMENTS` (30) are real divisions,
because neither is a power of two. `if (++i >= N) i = 0;` is the same thing and
is a compare and a branch.

`% FLOW_WINDOW_SLOTS` (32) and `% COUNTER_MODULO` (32768) are left alone on
purpose — those are powers of two and the compiler emits a mask.

### Net effect

| | before | after | |
|---|---|---|---|
| `tank_median` | 19,870 cycles, 4.97 ms | 2,453 cycles, 613 µs | **8.1x** |
| `compute_tick` | 26,944 cycles, 6.74 ms | 9,048 cycles, 2.26 ms | **3.0x** |
| worst pass through the loop | 18.22 ms | 13.75 ms | 1.3x |
| program memory | 11,424 bytes | 11,300 bytes | smaller |
| RAM | 558 bytes | 686 bytes | +128 |

The program got *smaller*, which was not the point but is a fair sign the
change was a simplification rather than a trade.

One caveat on the old number, in the interest of not overselling this: the
tool costs a nested loop as outer x inner, and an insertion sort's inner loop
is triangular — it averages half its bound. So 19,870 is the honest worst case
under a model that cannot express "half", and the sort's true worst case is
nearer 300 inner trips than 600. The histogram wins either way, and the part
that matters is not the ratio: **it wins by the same margin whatever the data
does**, which the sort never did.

**The new `compute_tick` ceiling of 3.2 ms would have failed on the old code**,
which measured 6.74 ms. That is the gate doing its job rather than a
coincidence.

---

## The measuring tool, and why it works the way it does

`tools/cycles.py` used to carry each loop's **body size written down by hand**
alongside its trip count. That is a trap rather than a shortcut: when
`tank_median` stopped being an insertion sort, the table still described the
sort, so the tool multiplied a body that no longer existed by a trip count that
no longer applied — and reported the new algorithm as costing exactly what the
old one had. A model of the code will always drift away from the code.

It measures the listing now. Every figure in this repository, including the
"before" column above, comes from the current tool run against a real build.

### What it does

- **Loop bodies are measured** from the listing. A backward branch whose target
  is earlier in the same function is a loop; the words between are the body.
  Change the code and this follows with no edit.
- **Trip counts name a `config.h` constant** where one exists, and the value is
  read from `config.h` at run time. Change `TANK_HIST_BINS` and the model
  follows.
- **Nesting is worked out from the addresses**, so an inner loop is multiplied
  by everything that encloses it.
- **Every backward branch must be accounted for**, in one of three tables:
  `LOOPS` (costed), `HARDWARE_WAITS` (spinning on a peripheral, so counting
  instructions says nothing) or `NOT_LOOPS` (ordinary control flow). A loop
  that appears in none of them, or a `LOOPS` entry whose loop has vanished,
  **stops the tool**. That is the mechanism that makes a change of algorithm
  impossible to slip past.

Trip counts are still declared rather than derived, because how many times a
loop runs is semantics and not instructions. That is the one place a human
still has to be honest — and the audit is what forces the human to look.

---

## What is deliberately not done

- **Caching slow-moving values in `txframes_gather`.** Range, tank level and
  the average change over seconds but are recomputed ten times a second. The
  saving would be large and it **changes behaviour** — the displayed values
  would be up to a second stale. Not worth it without a reason.
- **`compute_on_fuel`.** The hottest path in the firmware and already cheap.
- **`hal_can_receive`.** Dominated by the access-bank window, which is not
  arithmetic to be improved but a hardware protocol to be followed.
- **Sleep or idle modes.** The PIC18F25K80 has them; we never use them, and
  nothing in `pic_config.h` enables anything that could slow the part down.
  `OSCCON = 0x00` is the crystal straight through, and `SLEEP` is never
  executed. Confirmed rather than assumed, because a sibling project of this
  maintainer's did run in a low-power mode.

## What is left, and it is the big one

**`txframes_gather` is 25,617 cycles, 6.40 ms — now the largest single item in
the firmware — and it is nine 32-bit divisions.** `___lldiv` costs 1,026 cycles — 257 µs — every time, and it is
called from ten places.

The divisors are **constants**: 1000, 3600, 10000. The standard replacement is
a multiply by a precomputed reciprocal and a shift, which turns 32 iterations
into a multiply and a couple of instructions, and should be worth **5× per
call**.

**The risk is real and it is precision.** The result has to be bit-for-bit
identical to `/` across the whole input range that can occur. The condition for
doing this at all is an exhaustive host test that compares the two over that
range — without it, the failure mode is a display that is subtly wrong in a way
no fixture catches.
