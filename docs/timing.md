# How long everything takes

A worst-case budget for the scheduler, against the rates the device has to
hold. Written 2026-08-11, before any of it had run on a board.

**This is static analysis of the code XC8 actually generated, not a
measurement.** That is a real limitation and the last section says how to close
it. What it is not is guesswork: every number below is counted out of the
assembly listing of the hex that gets flashed.

---

## Method — and how to re-run it

```
make -C mplab            # writes build/canfuel.lst as well as the hex
python tools/cycles.py   # the table below, re-derived
python tools/cycles.py --check    # what CI runs
```

`mplab/Makefile` passes `-Wa,-a`, so pic-as writes `build/canfuel.lst` with
every generated instruction, its address and its encoding. `tools/cycles.py`
counts program words per function out of that listing and costs the loops by
finding the backward branches and multiplying the body by the trip count the C
source allows.

**The script is the executable half of this document.** This file explains and
argues; the script re-derives the numbers from whatever the compiler produced
today, so the two cannot drift. It also runs in the `firmware` CI job with
`--check`, which fails the build if a scheduler slot goes over a ceiling — see
the guard rail section at the end.

**The cycle model.** On the PIC18, at `FOSC/4` (DS39977C, CLKOUT in the pin
table), one instruction cycle is `Tcy = 250 ns` at 16 MHz — 4 MIPS. Single-word
instructions take 1 Tcy, two-word instructions (`movff`, `lfsr`, `call`,
`goto`) take 2, and a taken branch or a skip costs 1 more than an untaken one.
**Counting program words rather than instructions therefore gives the cycle
count directly for straight-line code, and understates it only by the taken
branches.** Everything below is in words and is rounded up generously where a
loop is involved.

Trip counts used, all from the source and all worst case:

| Loop | Trips | Why |
|---|---|---|
| `___lldiv` | 32 | one per bit of a 32-bit divisor |
| `compute_range_km` rotate | 4 | `RANGE_BASIS_Q4`, back to whole tenths |
| `flow_push` | 4 | `FLOW_BUCKETS`, summed when one closes |
| `persist_load` | 64 | `PERSIST_SLOTS`, start-up only |
| `hal_can_receive` | 8 | bytes in a frame |
| `compute_tick` km rollover | 1 | 1 km in one tick needs 3600 km/h |

---

## What each piece costs

Worst case, including everything it calls. `___lldiv` appears in ten places and
is the single most expensive thing in the arithmetic — 1,026 cycles, 257 µs,
every time a 32-bit division is written in the core.

| Function | Cycles | Time |
|---|---|---|
| `txframes_gather` (seven getters; the trip totals moved to the 1 s slot) | 7,833 | **1.96 ms** |
| `persist_load` (start-up only) | 6,199 | **1.55 ms** |
| `compute_range_km` | 1,201 | 300 µs |
| `persist_save` | 3,165 | 791 µs |
| `compute_on_fuel` | 2,073 | 518 µs |
| `compute_tick` (with the tank sample and a kilometre rollover) | 3,118 | 780 µs |
| `flow_push` (worst case: the pass that closes a bucket) | 1,676 | 419 µs |
| `persist_crc16` (10 bytes x 8 bits) | 2,119 | 530 µs |
| `tank_sample` | 1,516 | 379 µs |
| `hal_sys_vdd_c` (plus 22 us of A/D) | 1,112 | 278 µs |
| `___lldiv`, one 32-bit division by a *variable* | 1,026 | 256 µs |
| `hal_can_send` | 644 | 161 µs |
| `decode_frame` | 542 | 136 µs |
| `mulhi_u32`, one reciprocal multiply | 300 | 75 µs |
| `hal_can_receive` | 234 | 58 µs |
| `mul_u32_u16`, one wide multiply | 161 | 40 µs |
| `hal_sys_millis` | 25 | 6 µs |
| `hal_sys_isr` (the millisecond tick) | 14 | 4 µs |

**`txframes_gather` is seven divisions in a trench coat.** Nothing in it is
slow; the core simply divides in a lot of places and this is where most of them
get exercised. It is the largest single item by a wide margin. Three
places in the build still call `___lldiv` and every one of them divides by a
*variable*, where a reciprocal cannot help: `compute_range_km` (by the basis),
`hal_sys_vdd_c` (by the A/D code) and the shared `div_round`, reached from
FuelNow, FuelAvg and the flow window.

### The tank sample stopped being a sweep of anything

It was an insertion sort over a 25-slot ring — 15,068 cycles, **3.77 ms** — then
a sweep of a 128-bucket histogram, 2,453 cycles. Since 2026-08-12 there is no
median at all: the refuelling rule is a first-order filter and a counter of
consecutive samples, so `tank_sample` is 1,562 cycles with no loop in it and
`compute_tick`'s worst case fell 1.26 → 0.67 ms. **The 153 bytes of RAM the ring
and the buckets held came back too.**

What the three have in common is worth stating, because it is the only
generalisable thing here: each time, the win came from asking what the number
was actually *for*. The sort produced an ordering nobody wanted, only its middle
element. The histogram produced a median nobody wanted either — the rule only
ever asks whether the level is persistently higher than it was.
`docs/optimisation.md` §8 and `docs/refuel-reset.md` carry the argument that it
is the same answer.

---

## The three budgets

### Every pass of the loop

| | Cycles | Time |
|---|---|---|
| `hal_sys_watchdog_clear` + `hal_sys_millis` | 26 | 7 µs |
| FIFO drain, 8 frames, one of them 0x480 | 8,345 | 2.09 ms |
| `compute_tick`, moving, no tank sample | 1,598 | 400 µs |
| `compute_tick`, standing, with the tank sample | 3,118 | 0.78 ms |

A **typical** pass is none of that: the FIFO is empty, the distance step has
not elapsed and `compute_tick` returns almost immediately — about 450 cycles,
**113 µs**, so the loop runs roughly 8,800 times a second.

That number matters twice. The FIFO is drained 8,800 times a second against
frames arriving at about 400 a second, which is the twenty-fold margin
`CLAUDE.md` claims for polling over interrupts, now counted rather than
asserted. And **88 passes out of 89 skip the distance arithmetic entirely**,
because `compute_tick` integrates on `DIST_TICK_MS` = 10 ms rather than on
whatever delta it happens to be handed.

⚠ **That gate is not a cycle count, it is the correctness of the distance**,
and the two are easy to confuse from here. Integrating on every pass means a
one-millisecond delta, and `v × 1 ms / 3600` truncated to whole millimetres
loses 6.4 % of the distance at 50 km/h and all of it below 3.6 km/h. The
remainder is carried across steps so nothing is lost at all. `config.h`
carries the arithmetic and `docs/optimisation.md` §6 the story; the cycles
below are a side effect of a fix, not the reason for it.

The side effect is still the largest single one in the firmware. The path used
to run about 1,000 times a second at ~550 cycles — **14 % of the CPU** — and
now runs 100 times a second at ~700, which is 1.8 %. Computing the remainder
costs a multiply, so `compute_tick`'s *worst case* went **up** on its own
account (1.21 → 1.26 ms) and only came down again when the tank median went;
that is the honest way round, because the table above is per call and what
changed here is how often the call does anything.

### Every 100 ms

| | Cycles | Time |
|---|---|---|
| `hal_sys_vdd_c` incl. the A/D conversion | ~1,200 | 300 µs |
| `txframes_gather` | 7,833 | 1.96 ms |
| two frames assembled and queued | 818 | 205 µs |
| error counters, overflow flag, LEDs | ~200 | 50 µs |
| **total** | | **2.68 ms** |

**3.7 % of the 100 ms it has.** The remaining 94.7 % is spent draining an empty
FIFO.

### Every 1 s

| | Cycles | Time |
|---|---|---|
| `txframes_gather_trip` (the two divisions by 1000) | 837 | 209 µs |
| `txframes_trip` + `hal_can_send` | 384 | 96 µs |
| `persist_save` deciding not to write | 625 | 156 µs |
| `persist_save` **writing**, once a minute | — | **~48 ms** |

The first line arrived here from the 100 ms slot, where it was being computed
ten times a second for a frame that goes out once a second. That is a straight
transfer of 686 cycles from a budget with a 3.24 ms load to one with 1.19 ms,
and it leaves the slow slot at **1.26× under its ceiling** — the tightest
margin of the four, and worth watching if anything else moves in here.

---

## The answer: where the margin is

Stacking every worst case that can genuinely land in the same pass:

```
FIFO drain (8 frames)            2.09 ms
compute_tick, with the tank      0.78 ms
the 100 ms slot                  2.68 ms
the 1 s slot, not writing        1.19 ms
                                --------
worst pass without an EEPROM write      6.73 ms
plus the once-a-minute EEPROM write    ~54.7 ms
```

Every figure here comes from `tools/cycles.py` against a real build. **The same
pass measured 18.72 ms before the optimisation work**, all of it on
2026-08-11/12 and all measured with this tool, so the two compare like with
like:

| | worst pass |
|---|---|
| before any of it | 18.72 ms |
| tank median: sort -> histogram | 13.72 ms |
| constant division: `___lldiv` -> reciprocal | 11.67 ms |
| multiplication: `___lmul` -> byte products | 8.21 ms |
| the distance step, and two gathers moved | 8.02 ms |
| the tank median -> a filter and a counter | 7.43 ms |
| the flow ring -> four buckets | 7.18 ms |
| the 30 km range window -> a filter | **6.73 ms** |

What changed and why is `docs/optimisation.md`.

Against the two deadlines:

- **The 100 ms transmit cadence.** A 6.73 ms pass leaves a **14× margin**,
  where before the optimisation it left 5.3×. The once-a-minute pass leaves
  1.8×, so 0x600 and 0x601 arrive up to 56 ms late once a minute and the
  display sees a gap of about 156 ms instead of 100 ms. Nothing reads a period,
  so this is invisible.
- **`RX_POLL_MS`, the 10 ms the FIFO must not fall behind by.** The worst
  non-EEPROM pass is **6.73 ms and fits inside it**, which it never did
  before — it was 18.72 ms, then 11.67, then 8.21. That was always survivable, because
  the constant is a conservative statement of intent and the FIFO's depth is
  the real limit: eight buffers against 3.58 frames per 10 ms is **22 ms of
  blindness before anything is lost**. It is simply no longer a number that
  needs explaining away. The EEPROM write does overflow the FIFO, which is
  analysed in `main.c` and is harmless: the fuel delta is modulo-32768 so a gap
  costs nothing, and distance is integrated against the clock rather than
  against frame arrivals.

The millisecond ISR is 3.5 µs every 1 ms — **0.35 % of the CPU** — and it is
the only interrupt in the firmware.

**Nothing here needs changing.** The arithmetic is three orders of magnitude
away from the clock rate; the only thing on this page that is measured in
milliseconds rather than microseconds is the EEPROM, and that was designed for
in `main.c` before this analysis existed.

---

## What actually happens to the bus during a long pass

Worth being precise about, because "the MCU is busy for 48 ms" sounds like it
should be much worse than it is.

**The CPU is not what receives frames.** The ECAN module has its own protocol
engine: it clocks bits off the wire, matches them against the six hardware
filters, acknowledges what it accepts and writes it into the FIFO, all with no
software involved at all. While `hal_eeprom_write()` sits polling `WR`, the
module carries on doing exactly that. Nothing about a busy CPU is visible on
the bus.

So the sequence is:

1. **The first eight accepted frames are buffered.** The FIFO is eight deep
   (Mode 2, §27.4.3), and our six identifiers arrive at **357 a second**,
   measured off the `_z1` fixtures — 3.58 per 10 ms, or one every 2.8 ms.
   Eight buffers is therefore about **22 ms of storage**.
2. **After that, further frames are dropped.** Not queued anywhere: each buffer
   has an `RXFUL` bit, and DS39977C is explicit — *"As long as RXFUL is set, no
   new message will be loaded and the buffer will be considered full."* The
   module sets `RXBnOVFL` in `COMSTAT` and the message is simply lost.
3. **The bus does not notice.** A full receive buffer is not one of the five
   error conditions in §27.14 — bit, acknowledge, form, CRC and stuff — so no
   error frame is generated, and the frame is still acknowledged. The overflow
   is a local status bit and nothing more. **We lose data; the car does not.**
4. **The FIFO refills from empty** the moment the loop comes round again and
   `hal_can_receive()` drains it, which takes 59 µs a frame.

### What is actually lost, and when

Two cases, and only one of them loses anything. Both are the current code;
the columns beside them are the same arithmetic against the code as it stood
before the optimisation work of 2026-08-11, measured with this same tool so
the two are comparable.

| | before | now | the FIFO holds |
|---|---|---|---|
| worst pass, no EEPROM write | 18.72 ms | **6.73 ms** | 22 ms |
| headroom before anything is dropped | 3.3 ms | **15.3 ms** | |
| worst pass **with** the write | 66.72 ms | **54.73 ms** | |

**Outside the EEPROM write, nothing is dropped in either version** — that is
what the 22 ms buys. What changed is the margin: it was 3.3 ms and is now
15.3 ms, four and a half times as much. That matters more than the milliseconds, because
the old worst case needed an unlucky tank ring to reach and would have been
within one bad coincidence of the limit.

**During the write, both versions drop frames**, because the ~48 ms of D122
dominates everything the CPU does. At the measured idle rate of 357 frames a
second:

| Frame | per second | lost before | lost now |
|---|---|---|---|
| 0x1A0 speed | 129.8 | 5.8 | **4.4** |
| 0x280 engine | 93.9 | 4.2 | **3.2** |
| 0x288 coolant | 76.2 | 3.4 | **2.6** |
| 0x320 tank | 27.0 | 1.2 | **0.9** |
| 0x480 fuel counter | 26.4 | 1.2 | **0.9** |
| 0x420 oil | 4.1 | 0.2 | **0.1** |
| **total** | **357** | **~16** | **~12.2** |

A quarter fewer, which is the least interesting number on this page: the loss
is dominated by the EEPROM and no amount of arithmetic will change that.

None of that costs anything, which is the analysis already written out in
`main.c` and is worth repeating here because this is where the numbers are:

- **the fuel counter** delta is `(new − old) mod 32768`, so a gap costs
  *nothing at all* — the next 0x480 accounts for every microlitre burned during
  the write, including any frames that never arrived;
- **distance** is integrated from speed against the millisecond clock in
  `compute_tick()`, not against frame arrivals, and that clock keeps running
  because `hal_eeprom_write()` restores `GIE` the instant the unlock sequence
  is over;
- **everything else** — rpm, tank, temperatures — is a last-known-value that is
  48 ms stale, against a tank float that sloshes by nine litres and a coolant
  temperature that moves in minutes.

`main.c` then clears the overflow flag, because an overflow we caused
deliberately, once a minute, is not a fault worth putting on an LED.

The **ordinary** worst pass, 6.73 ms, is inside the 22 ms the FIFO holds, so
outside the EEPROM write nothing is dropped at all — and since 2026-08-12 it is
also inside `RX_POLL_MS`, which it had never been.

---

## The one number that is not bounded

The 48 ms above is **twelve bytes at the 4 ms of DS39977C Table 31-1, D122**,
and D122 reads `-- 4 --` ms. It is a typical with **no maximum at all**.
Section 8.4's prose says the write time "will vary with voltage and
temperature, as well as from chip-to-chip" and refers the reader to "Parameter
D122 ... for exact limits" — and D122 has none.

So 48 ms is what to expect and not what to design against. What makes that
tolerable is that nothing downstream of it is a deadline: the watchdog is
2.048 s, forty times the typical write; the FIFO overflow it causes is
harmless; and a late frame is invisible to the display. If a part ever wrote
slowly enough to trip the watchdog, the record would have to take sixteen times
its typical time.

---

## The guard rail

`python tools/cycles.py --check` runs in the `firmware` CI job, which is the
only one with XC8 and therefore the only one that can. It fails the build if
any of these goes over its ceiling:

| Budget | Now | Ceiling |
|---|---|---|
| one received frame, decoded and accumulated | 0.71 ms | 1.0 ms |
| `compute_tick`, worst case | 0.78 ms | 1.0 ms |
| the 100 ms slot | 2.68 ms | 3.6 ms |
| the 1 s slot, excluding the EEPROM write | 1.19 ms | 1.5 ms |

**The ceilings sit about 1.3x above what the code costs today**, and all four
came down again on 2026-08-12 as the algorithms underneath them got cheaper:
1.4 -> 1.0, 1.7 -> 1.0, 5.2 -> 3.6 and 1.5 unchanged. A ceiling that can never
be hit is not a gate, so they follow the code down. The hardware has far more headroom
than this — the numbers above in *The answer: where the margin is* are the real
limits — but these are a regression alarm, and an alarm set beyond anything
that can happen is decoration.

There is enough room for an honest change and not enough to hide a millisecond
arriving by accident. If a cost is intended, raise the ceiling in
`tools/cycles.py` and say why here. That is the whole protocol.

**What the script cannot do**, and it says so in its own header: it is not a
sound WCET analyser, and it has never been checked against a stopwatch. It
cannot see how often a branch is really taken, and it costs a nested loop as
outer x inner, which overstates a triangular one.

**What it will not do any more is measure the past.** Loop bodies come out of
the listing, trip counts name a `config.h` constant, and every backward branch
in the build has to appear in one of its three tables — `LOOPS`,
`HARDWARE_WAITS` or `NOT_LOOPS` — or the tool stops instead of guessing. A
change of algorithm therefore cannot pass silently. `docs/optimisation.md` is
where that mechanism is explained, and it is required reading before changing
any loop in the core.

---

## How to close the gap between this and reality

This is a count of instructions, not a stopwatch. Three things it cannot see:
how often branches are actually taken, what the compiler does to the stack
frame on entry, and whether any of the HAL's busy-waits take longer on real
silicon than the datasheet says.

On the board, with `DBG_EN` fitted, the cheap check is to drive `LED_CAN`
(RC1) high at the top of the loop and low at the bottom and put a scope on it:
the mark-space ratio is the duty cycle, and the widest pulse is the worst pass.
Doing the same around `persist_save()` measures the EEPROM write directly,
which is the one figure the datasheet declines to bound. Both are a two-line
change and neither belongs in the committed firmware.
