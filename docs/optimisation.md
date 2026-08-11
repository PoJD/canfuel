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
| `main`, one pass, all worst cases | 18.22 ms | 13.75 ms | 1.3x |
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

## 4. Division by a constant, without dividing — 2026-08-11

`txframes_gather` was the largest single item at 6.40 ms and it is nine 32-bit
divisions. `___lldiv` costs 1,026 cycles — 257 µs — every time. It is now
4.35 ms, a **32 % cut**, and `main` went 13.75 → 11.17 ms.

(That is the `main` figure `cycles.py` prints. The worst *pass* in
`docs/timing.md` is a larger number — 11.67 ms — because it stacks a full
eight-frame FIFO drain on top, which one call to `main` does not represent.
The two are consistent; they measure different things.)

**The usual trick does not work on this compiler, and finding that out first
saved building the wrong thing.** Dividing by a constant is normally replaced
by multiplying by a fixed-point reciprocal — but XC8 v4.00 calls `___lmul` for
any multiply wider than 8 bits, and `___lmul` is *also* a per-bit loop. The
obvious rewrite would have been no faster than the division.

What XC8 does compile to the hardware multiplier is **`uint8 × uint8` and
`uint16 × uint8` — one `MULWF`, no call**. So `mulhi_u32()` in `src/divconst.h`
builds the 64-bit product out of sixteen byte products: 265 instructions of
straight-line code, no branches, no calls, against ~1,050 cycles for the
division.

Two things had to be got right, and both were found by reading the listing
rather than by thinking:

- **`div_const` is a macro, not a function.** As a function taking the shift as
  a parameter, XC8 cannot know it at compile time and emits a *loop* of
  single-bit rotates, which puts back most of the saving. As a macro the shift
  is a literal at the call site.
- **A shift of 8, 16 or 24 is free; any other shift is still a loop**, even
  with a literal count. `tools/divconst.py` therefore prefers a multiple of
  eight, which needs `2**s < d` — so 1000 and 95500 get one, and 10, 100 and
  120 keep short rotates that are costed rather than ignored.

### How the magic numbers are trusted

Three independent things, because a reciprocal that is one out on a value no
fixture produces would show a wrong number on the display and break nothing
else:

1. **A proof, not a sample.** `tools/divconst.py` decides exactness with the
   Granlund–Montgomery condition (PLDI 1994, §4): with `m = ceil(2**(32+s)/d)`
   the overshoot `e = m*d - 2**(32+s)` must satisfy `(limit-1) * e < 2**(32+s)`.
   One O(1) test covers the entire declared range.
2. **Brute force disagreeing is a failure.** The same script spot-checks tens
   of thousands of real values against real division, because a transcription
   slip in the proof would otherwise be invisible.
3. **The C is tested separately from the arithmetic.** `test_divconst.c` proves
   that sixteen hand-assembled byte products actually compute that product.
   1.17 million checks run as part of `make test`; the `-DEXHAUSTIVE` build
   walks **every value in every declared range — 26,843,545,600 of them** — and
   was run when these magics were introduced. It came back clean.

   That run was also checked for having actually happened rather than exited
   early: the framework's check counter is an `int` and wraps, and the reported
   total matches the expected count modulo 2³² exactly.

**The range is part of the proof.** 95500 needs a 33-bit magic over the full
32-bit range and would not fit; it is exact for `x < 2**30`, which holds
because `torque_d * 10 * rpm < 1900 * 10 * 16384`. Understating a range there
is a silent wrong answer, so every bound in `divconst.py` is justified in
place.

### What it cost

918 bytes of program memory, which is the trade this project is happy to make
— 37.3 % of flash used against 34.5 %. `python tools/replay.py --host-build`
still agrees with the Python reference on every field of every fixture, which
is the check that matters: the arithmetic did not move.

---

## What is left

**`txframes_gather` is still the largest item at 4.35 ms**, but what remains in
it is not division any more — it is the nine getters themselves and the
`mulhi_u32` calls inside them. The next honest saving there is arranging the
arithmetic so a division disappears entirely rather than getting cheaper, which
is a change to what the code computes and needs a reason beyond speed.

Two ideas that are *not* worth it, recorded so they are not rediscovered:

- **Caching slow-moving values** — covered above; it changes behaviour.
- **A second reciprocal for the runtime divisors** (`flow_sum_ms`,
  `speed_mmh`, `seg_count`). Those denominators are not constants, so the magic
  would have to be computed at run time, which costs more than the division it
  replaces.
