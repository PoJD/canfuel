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

**Correctness first, and it is not negotiable.** Every optimisation in sections
1 to 5 left the numbers bit-for-bit identical, and that was checked rather than
assumed:
`make -C test test`, the Python suite, and above all
`python tools/replay.py --host-build test/fixtures/*.txt`, which replays every
recording through both the C core and the Python reference and diffs the
totals. An optimisation that changes a displayed value is a bug, however fast
it is.

**From section 6 on, that rule is narrower than it looks and deliberately so.**
The first round was done under an explicit instruction — *optimise, change
nothing functionally* — and the day after it was finished the maintainer
withdrew it, on the grounds that several of the algorithms were never forced in
the first place. The tank median, the shape of the flow window and the 30 km
range window are all **our choices**, made once and never compared against a
cheaper one. So the later sections are allowed to change what the code
computes.

What does not change is the standard of evidence. A section below either
produces the same number and says so, or it produces a different number and
argues for it against the fixtures — and the two implementations still have to
agree with each other afterwards, which is what `replay.py --host-build`
enforces on every push.

**Bytes are cheap, cycles are not.** The part has 32 KB of program memory and
uses about a third. Trading size for speed is nearly always right here — §1
spends 128 bytes of RAM to remove 12,600 cycles, and §4 and §5 spend 1,400
bytes of program memory to remove the compiler's division and multiplication
helpers. RAM is the one that eventually bites, and §8 to §10 gave 347 bytes of
it back.

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
  read from `config.h` at run time. Change `FLOW_BUCKETS` and the model
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

## 5. Multiplication, the same trick again — 2026-08-12

Once the divisions were gone, **`___lmul` was the largest single item left**:
twelve calls at 849 cycles, 10,188 cycles, **2.55 ms**. It is the same per-bit
loop as `___lldiv`, for the same reason, and by then it had produced an absurd
state of affairs — `mulhi_u32` costs 300 cycles, so a *reciprocal division* had
become nearly three times cheaper than an ordinary multiply sitting next to it.

`mul_u32_u16()` in `src/fastmul.h` is the same idea as `mulhi_u32` and cheaper,
because only the low half of the product is wanted and the multiplier fits 16
bits: the product `x_i * m_j` is only needed where `i + j <= 3`, which is
**seven byte products instead of sixteen**. 137 instructions, no branches, no
calls, against 849.

**Every multiply in the core is a wide value times a small one**, which is why
this fits so well: 10, 36, 74, 1000, 3600, 4820, plus `rpm` (a uint16
quarter-count shifted down, so under 16384) and `dt_ms` (gated to 1000 by
`compute_tick`). The type is `uint16_t`, so the compiler enforces the
precondition rather than the comment.

Two of the twelve took a second look:

- **`torque_d * 10u * rpm`** left an inner `torque_d * 10u` that was still a
  32-bit product. It is two nested `mul_u32_u16` calls now.
- **`data[7] * TORQUE_CNM_PER_BIT`** in `decode.c` is an 8x8 product that the
  hardware does in one cycle, and XC8 was promoting it to 32 bits and calling
  `___lmul` anyway. Casting both operands to `uint16_t` explicitly is all it
  took.

**`___lmul` is now absent from the build entirely** — `cycles.py` said so by
refusing to run, because a `LOOPS` entry whose loop has vanished stops the
tool. That is the audit doing precisely what it was built for.

`fastmul.h` is a separate header from `divconst.h` so that `decode.c`, which
needs the multiply and not the division, does not pull in an unused static
function — `-Werror=unused-function` turns that into a build failure.

### What it bought

| | before | after |
|---|---|---|
| `txframes_gather` | 4.35 ms | **2.97 ms** |
| `compute_tick` | 1.73 ms | 1.21 ms |
| the 100 ms slot | 5.07 ms | **3.69 ms** |
| worst pass through the loop | 11.67 ms | **8.21 ms** |
| program memory | 12,218 bytes | 12,682 bytes |

**The worst pass is now inside `RX_POLL_MS`**, which it had never been — 18.72,
then 11.67, now 8.21 against a 10 ms intent. That was always survivable because
the FIFO's 22 ms is the real limit, but it is one fewer thing to explain.

Three `___lldiv` calls remain and they are not going anywhere: they divide by
`flow_sum_ms`, `speed_mmh` and `seg_count * 1000`, which are variables. A
reciprocal would have to be derived at run time, which costs more than the
division it replaces.

---

## 6. The distance integrator was throwing away several per cent — 2026-08-12

**This one is a fault, not an optimisation, and it was found by reading the
code with the "do not change behaviour" constraint lifted.** It is written up
here rather than only in the commit because the *reason* it survived this long
is the interesting part.

`main.c` calls `compute_tick()` on every pass of the scheduler, and a pass is
about 113 µs, so in the car the delta it sees is **one millisecond**. The
integration is `v [0.001 km/h] × t [ms] / 3600` in integer millimetres, and at
one millisecond the truncation is not a rounding detail:

| speed | mm per ms | stored | error |
|---|---|---|---|
| 100 km/h | 27.78 | 27 | −2.8 % |
| 50 km/h | 13.89 | 13 | **−6.4 %** |
| 7 km/h | 1.94 | 1 | −49 % |
| **under 3.6 km/h** | <1 | **0** | **no distance at all** |

It lands in `total_mm`, and from there in FuelAvg, Range and the trip.

**Why no test could see it.** `test/replay_core.h` drives `compute_tick()` from
the 0x480 frames, which are ~38 ms apart, and at 38 ms the same truncation is
0.8 % — inside the tolerance `replay.py --host-build` compares on. The Python
reference had the identical fault (`total_mm += int(...)` per interval), so the
two agreed with each other about a wrong number. **Twin implementations do not
catch a fault they share, and this is what that looks like.**

The fix is two things, and the second one is the one that was not obvious:

- **`DIST_TICK_MS = 10` and a carried remainder.** The step is ten times
  longer and what the division leaves over goes into the next step instead of
  the bin, so the integration is exact and cannot drift. Division count falls
  from ~1000/s to 100/s with it — about 14 % of the CPU, the largest single
  saving in the firmware, and entirely a side effect.
- **`DIST_MIN_MMH = 100`.** A standing car sends 0.005 km/h, not zero. Exactly
  integrated that is 1.39 mm/s, **83 mm over a minute of idling**, and two
  fixtures went red the moment the remainder was carried. The old code
  discarded it by accident, because everything under 3.6 km/h truncated to
  nothing; now it is discarded on purpose, on the same measurement the idle
  gate rests on.

Three tests pin it: the same distance whether the core is ticked every
millisecond or every second, 50 m for a minute at walking pace, and exactly
zero for a minute of standing still. `tools/replay.py` carries the remainder
too, so the oracle stays comparable rather than staying wrong in company.

## 7. Two things computed for nobody — 2026-08-12

Both behaviour-neutral, both found by reading the call graph `cycles.py` prints
rather than the code.

- **`compute_torque_d()` ran twice per gather**, once for the frame and once
  inside `compute_power_d()`, which needs the same number. `compute_power_d()`
  takes it as an argument now: **−1,042 cycles, 9 % of the 100 ms slot.** The
  gates all live in `compute_torque_d()` and each returns zero, so a zero
  torque still makes zero power — the idle gate did not move.
- **`trip_ml` and `trip_m` were gathered ten times a second** for a frame that
  goes out once a second: two divisions by 1000, 686 cycles, nine tenths of
  them wasted. `txframes_gather_trip()` is called from the slow slot instead,
  immediately before `txframes_trip()`, and obeys the same quiet-bus rule.

| | before | after |
|---|---|---|
| `txframes_gather` | 2.97 ms | **2.52 ms** |
| the 100 ms slot | 3.69 ms | **3.24 ms** |
| the 1 s slot | 0.98 ms | 1.19 ms |
| `compute_tick` worst case | 1.21 ms | 1.26 ms |
| program memory | 12,682 B | 12,824 B |

Two of those went **up**, and both are honest: the 1 s slot gained the trip
divisions the fast slot gave away, and `compute_tick`'s worst case gained the
multiply that computes the remainder. What the table cannot show is the change
that matters — the distance path now runs 100 times a second instead of a
thousand.

## 8. The tank median was never a requirement — 2026-08-12

**This is the first change here that computes something different, and it is
the clearest case of the constraint that was lifted.** The median was our
choice: a rule was needed for "somebody refuelled", a median at rest was
proposed, it worked, and nothing ever asked whether it was the cheapest shape
of that rule. It cost 2,453 cycles once a second, 153 bytes of RAM (a 25-slot
ring plus 128 buckets), and it was the reason `tank_sample` had a loop at all.

**What the rule actually asks is not "what is the middle value" but "is the
level suddenly and persistently higher than it was".** That needs no ordering
and no counting of buckets:

```c
if (raw > stable + REFUEL_RISE_L)  { if (++high >= REFUEL_CONFIRM_S) refuel(); }
else                               { high = 0; filter(stable, raw); }
```

`tank_stable_l` is now the whole part of a 16-bit first-order filter in 1/256
litre, `TANK_REST_SHIFT` = 4, so the whole thing is one shift and a compare —
**no division and no multiplication anywhere in it**, which was the other half
of what this pass was asked for.

Two details are load-bearing and both are in the code as comments:

- **The baseline is frozen while the counter runs.** Let the filter chase the
  new level and it raises `tank_stable_l` under the comparison, disqualifying
  the rise it is in the middle of confirming — a 4 l fill would then be
  detected or not depending on how fast the filter happened to move.
- **`compute_restore()` seeds the filter from the EEPROM**, not from the first
  sample after the restart. Seeding from the sample would swallow exactly the
  change the rule exists to notice, since the normal refuelling happens with
  the ignition off.

**Is it the same answer?** Not identically, and `docs/refuel-reset.md` has the
table. It is quicker on a real fill (5 s rather than ~13 s at rest), equally
deaf to a single wild reading, and the one case the median covered better — a
burst of noise longer than five seconds but shorter than thirteen — is not a
shape the sender produces at rest, where 1584 of 1622 measured samples were the
same litre. Three new tests hold the line, and one of them replays **all
seventeen fixtures and requires that not one of them fires the rule**, because
a false positive silently destroys an average the driver has watched for
600 km.

| | before | after |
|---|---|---|
| `tank_sample` | 3,942 cycles, 986 µs | **1,562 cycles, 390 µs** |
| `compute_tick` worst case | 1.26 ms | **0.67 ms** |
| worst pass through the loop | 8.02 ms | **7.43 ms** |
| RAM | 726 B | **574 B** |
| program memory | 12,824 B | 12,924 B |

`compute_tick`'s ceiling in `cycles.py` came down from 1.7 ms to 0.9 ms with
it. A ceiling that can never be hit is not a gate.

## 9. The flow window: 32 slots became 4 buckets — 2026-08-12

The instantaneous flow was a 32-slot ring of (microlitres, milliseconds), one
slot per 0x480 frame, with the oldest dropped one at a time until the window
fitted inside a second — and **the answer recomputed on every frame**, which
means a 32-bit division by a variable, 1,026 cycles, **twenty-six times a
second**, for a number that is transmitted ten times a second.

It is four quarter-second buckets now. A frame adds into the open bucket and
nothing else happens; when that bucket has held `FLOW_BUCKET_MS` the four are
averaged and the oldest is emptied to take its place. **The division runs four
times a second.**

What it costs, stated plainly: the flow steps four times a second rather than
on every frame, and the window is 0.75–1.0 s of history at the moment it is
read rather than exactly 1.0 s. Neither is visible on a gauge that shows
0.1 l/h, and the display only refreshes ten times a second anyway.

One gate moved with it. `compute_on_fuel` used to accept a sample up to
65,535 ms long; it now clears the window for anything longer than
`FLOW_WINDOW_MS`. That is both a tighter statement of what the window means — a
gap longer than the window describes a different situation, and the bus is
declared dead at half of it — and what keeps a bucket inside the `uint16`
fields it is made of.

**`tools/replay.py` grew the same buckets**, because it is the reference
implementation and not an independent opinion: with a per-frame ring on one
side and buckets on the other the two would have disagreed about `flow_ul_s`
by a quarter of a second's worth of history on every fixture. They agree on
every field again.

| | before | after |
|---|---|---|
| `flow_push` | 2,669 cycles, 667 µs | **1,676 cycles, 419 µs** (the pass that closes a bucket) |
| `compute_on_fuel` | 3,045 | **2,073** |
| one received frame | 0.96 ms | **0.71 ms** |
| FIFO drain, 8 frames | 2.33 ms | **2.09 ms** |
| worst pass through the loop | 7.43 ms | **7.18 ms** |
| RAM | 574 B | **453 B** |

The `rx_frame` ceiling came down from 1.4 ms to 1.0 with it.

## 10. Range: a 30 km window became a filter — 2026-08-12

The basis Range divides by was a flat average over the last thirty kilometres,
held as **thirty microlitre totals, 120 bytes**, and summed on every gather —
ten times a second, to produce a number that can only change **once a
kilometre**. Then divided by `seg_count * 1000`, a variable, so it could not
even use a reciprocal.

It is a first-order filter over completed kilometres now, one shift per
kilometre. Mean age 16 km against the flat window's 15, so the estimate is very
nearly as steady and reaches a new consumption level at much the same rate —
and `compute_range_km` is one division by the basis and nothing else.

The one detail that is not obvious: **the basis carries four extra bits.** In
whole tenths of l/100 km a shift of four cannot move a value at all until the
difference reaches 1.6 l/100 km, so the filter would stall a long way from the
truth and Range would sit at a wrong number indefinitely. In sixteenths it
stalls within 0.1 l/100 km, which is one digit of the average shown beside it.
An integer filter needs the headroom its own step size implies, and that is the
generalisable half of this section.

`compute_reset_trip()` clears the basis, exactly as it used to clear the ring,
so a refuelling puts Range back on the conservative default until
`RANGE_MIN_MM` of the new trip is driven.

| | before | after |
|---|---|---|
| `compute_range_km` | 3,466 cycles, 866 µs | **1,201 cycles, 300 µs** |
| `txframes_gather` | 2.52 ms | **1.96 ms** |
| the 100 ms slot | 3.24 ms | **2.68 ms** |
| worst pass through the loop | 7.18 ms | **6.73 ms** |
| RAM | 453 B | **339 B** |

`compute_tick`'s worst case went the other way, 0.67 → 0.78 ms, because the
kilometre rollover now folds the basis instead of storing a number in an array.
That is the trade and it is a good one: it happens once a kilometre.

## 11. Two divisors were ours, so they became shifts — 2026-08-12

`divconst.h` earns its keep on divisors the physics forces: 1000 for microlitres
into millilitres, 3600 for the speed integration, 95500 for the power formula.
**Two of the seven were neither** — they were scaling factors this project chose
and could choose again:

- **`TANK_DAMP_SAMPLES` 120 → 128.** The time constant was a decision inside a
  range where 60 and 120 were both defensible, so moving it 7 % costs nothing
  and turns a reciprocal multiply plus a rotate (~360 cycles) into a rotate
  (~70). The integer dead zone grows from 0.120 l to 0.128, still one digit of
  the display.
- **The drag slope scaled by 2**16 instead of by 10,000.** Nothing outside
  `config.h` reads the scaling, and a shift of 16 is *free* — three byte moves.
  31589/65536 = 0.4820023 against 0.4820, five parts per million of a slope
  whose measurement uncertainty is percent.

`DIVC_120` and `DIVC_10000` are gone from `divconst.h`, from `divconst.py` and
from `test_divconst.c`, which is 340,000 fewer checks in `make test` and two
fewer magic numbers anybody has to trust. **The rule that falls out of this is
worth keeping**: a divisor in `divconst.h` should be one the physics forces. A
constant we picked is a constant we can pick to be a power of two.

| | before | after |
|---|---|---|
| `tank_sample` | 1,516 cycles, 379 µs | **886 cycles, 222 µs** |
| `compute_torque_d` | 1,042 cycles | **720 cycles** |
| `compute_tick` worst case | 0.78 ms | **0.62 ms** |
| the 100 ms slot | 2.68 ms | **2.60 ms** |
| worst pass through the loop | 6.73 ms | **6.50 ms** |
| program memory | 12,996 B | 12,916 B |

## What is left

**`txframes_gather` is still the largest item at 1.88 ms**, and what is in it
now is neither division-by-constant nor multiplication — it is the getters
themselves, and three `___lldiv` calls that all divide by a *variable*: the A/D
code in `hal_sys_vdd_c`, the basis in `compute_range_km`, and the shared
`div_round` reached from FuelNow, FuelAvg and the flow window. A reciprocal
would have to be derived at run time, which costs more than the division it
replaces.

For scale: the whole worst pass is 6.50 ms against a 100 ms transmit slot and a
22 ms FIFO, and RAM is a small fraction of what the part has. **There is no
performance problem
left to solve here** — there was not one before either. What the second pass
bought was 347 bytes of RAM, three data structures, two loops and one real
fault in the distance.

Ideas that are *not* worth it, recorded so they are not rediscovered:

- **Caching slow-moving values with a staleness.** Still refused. Note that
  *memoisation* — recomputing only when an input changes, which is exact — is
  a different proposal and was simply never needed once the getters got cheap.
- **A second reciprocal for the runtime divisors.** Those denominators are not
  constants, so the magic would have to be computed at run time.
- **A quotient-bounded restoring division** to replace `___lldiv` where the
  answer is known to be small (FuelNow clamps at 999, so eleven iterations
  would do rather than thirty-two). It would save perhaps 700 cycles three
  times over, and it is another hand-written arithmetic helper to prove and
  maintain — against a budget that is already fourteen times inside its
  deadline. The trade that made `divconst.h` and `fastmul.h` worth it does not
  hold here.
- **A cheaper checksum in `persist`.** `persist_crc16` is 2,119 cycles, but it
  runs three times a minute and 64 times at start-up. Weakening the integrity
  check on the one thing that survives a power cycle, to save 1.6 ms a minute,
  is a bad trade in both directions.
