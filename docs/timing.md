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
| `tank_median` sweep | 128 | one per bucket, `TANK_HIST_BINS` |
| `compute_range_km` | 30 | `RANGE_SEGMENTS` |
| `flow_push` | 32 | `FLOW_WINDOW_SLOTS` |
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
| `txframes_gather` (all seven getters) | 17,418 | **4.35 ms** |
| `compute_tick` (with the tank median) | 6,900 | 1.73 ms |
| `persist_load` (start-up only) | 6,207 | 1.55 ms |
| `tank_sample` | 5,323 | 1.33 ms |
| `compute_range_km` | 4,158 | 1.04 ms |
| `compute_power_d` | 3,914 | 979 µs |
| `compute_on_fuel` | 3,737 | 934 µs |
| `flow_push` | 3,361 | 840 µs |
| `compute_fuel_now_d` | 3,348 | 837 µs |
| `tank_median` alone | 2,453 | 613 µs |
| `mulhi_u32`, one reciprocal multiply | ~530 | 133 µs |
| `persist_crc16` (10 bytes x 8 bits) | 2,119 | 530 µs |
| `hal_sys_vdd_c` (plus 22 µs of A/D) | 1,112 | 300 µs |
| `___lldiv`, one 32-bit division | 1,026 | 257 µs |
| `decode_frame` | 507 | 127 µs |
| `hal_can_send` | 286 | 72 µs |
| `hal_can_receive` | 234 | 59 µs |
| `hal_sys_millis` | 25 | 6 µs |
| `hal_sys_isr` (the millisecond tick) | 14 | 3.5 µs |

**`txframes_gather` is nine divisions in a trench coat.** Nothing in it is
slow; there are simply ten `___lldiv` call sites in the core and this is where
most of them get exercised. It is now the largest single item by a wide margin,
and division is where any further work belongs.

### `tank_median` used to be the largest, and it is worth saying why it is not

It was an insertion sort over the 25-slot ring: 15,068 cycles, **3.77 ms**,
worst case a reversed ring at 300 comparisons and moves. It is a histogram
sweep now — 2,453 cycles, 613 µs, **6.1× less** — and `compute_tick` fell from
4.82 ms to 1.66 ms with it.

Three things made that possible, and the first is the only interesting one:

- **We never wanted the sorted array, only the middle element**, and the key is
  a tank level masked to seven bits. A small fixed key space means counting
  beats comparing. `tank_sample()` maintains 128 buckets as samples enter and
  leave the ring, so the median is one sweep.
- **`cum` and `target` are `uint8_t`.** The ring holds at most 25 samples, so
  neither can overflow a byte, and a 16-bit compare cost six extra instructions
  per bucket.
- **A walking pointer instead of `tank_bins[v]`.** Indexing made XC8 rebuild
  the address from the struct base every iteration — twelve instructions of
  `lfsr` and `addwf` against one `infsnz`. The loop body went from 33 words to
  19.

**The bound is now a property of the code rather than of the data**, which
matters more than the number. The old worst case needed an unlucky ring and
was twelve times the typical case; this one is 128 buckets whatever the car
does. It costs 128 bytes of RAM.

⚠ **`tools/cycles.py` carries the loop model by hand**, and it said `(50, 299)`
for an algorithm that no longer existed — it reported no improvement at all
until the entry was corrected to `(19, 127)`. If a loop changes shape, that
table changes with it, or this whole document quietly measures the past.

---

## The three budgets

### Every pass of the loop

| | Cycles | Time |
|---|---|---|
| `hal_sys_watchdog_clear` + `hal_sys_millis` | 26 | 7 µs |
| FIFO drain, 8 frames, one of them 0x480 | 8,856 | 2.21 ms |
| `compute_tick`, moving, no tank sample | 1,534 | 384 µs |
| `compute_tick`, standing, tank median worst case | 6,900 | 1.73 ms |

A **typical** pass is none of that: the FIFO is empty, `dt_ms` is zero and
`compute_tick` returns almost immediately — about 450 cycles, **113 µs**, so
the loop runs roughly 8,800 times a second.

That number matters twice. The FIFO is drained 8,800 times a second against
frames arriving at about 400 a second, which is the twenty-fold margin
`CLAUDE.md` claims for polling over interrupts, now counted rather than
asserted. And because a pass is well under a millisecond, most passes see
`dt_ms == 0` and skip the distance division entirely — the loop is
self-limiting.

### Every 100 ms

| | Cycles | Time |
|---|---|---|
| `hal_sys_vdd_c` incl. the A/D conversion | ~1,200 | 300 µs |
| `txframes_gather` | 17,418 | 4.35 ms |
| two frames assembled and queued | 818 | 205 µs |
| error counters, overflow flag, LEDs | ~200 | 50 µs |
| **total** | | **5.07 ms** |

**5.1 % of the 100 ms it has.** The remaining 94.7 % is spent draining an empty
FIFO.

### Every 1 s

| | Cycles | Time |
|---|---|---|
| `txframes_trip` + `hal_can_send` | 384 | 96 µs |
| `persist_save` deciding not to write | 625 | 156 µs |
| `persist_save` **writing**, once a minute | — | **~48 ms** |

---

## The answer: where the margin is

Stacking every worst case that can genuinely land in the same pass:

```
FIFO drain (8 frames)            2.21 ms
compute_tick, tank median        1.73 ms
the 100 ms slot                  5.07 ms
the 1 s slot, not writing        0.98 ms
                                --------
worst pass without an EEPROM write      10.0 ms
plus the once-a-minute EEPROM write     ~58.0 ms
```

Every figure here comes from `tools/cycles.py` against a real build. The same
pass measured 18.2 ms before the tank median stopped sorting and 13.7 ms before
constant division stopped using `___lldiv`, both on 2026-08-11. What changed
and why is `docs/optimisation.md`.

Against the two deadlines:

- **The 100 ms transmit cadence.** A 12.6 ms pass leaves an **8× margin**. The
  once-a-minute pass leaves 1.65×, so 0x600 and 0x601 arrive up to 60 ms late
  once a minute and the display sees a gap of about 160 ms instead of 100 ms.
  Nothing reads a period, so this is invisible.
- **`RX_POLL_MS`, the 10 ms the FIFO must not fall behind by.** The worst
  non-EEPROM pass is 12.6 ms, which is over that number — but the number is
  conservative, and what actually matters is the FIFO's depth. Eight buffers
  against 3.58 frames per 10 ms is **22 ms of blindness before anything is
  lost**, so a 12.6 ms pass loses nothing. The EEPROM write does overflow the
  FIFO, which is analysed in `main.c` and is harmless: the fuel delta is
  modulo-32768 so a gap costs nothing, and distance is integrated against the
  clock rather than against frame arrivals. The EEPROM write does overflow
  the FIFO, which is analysed in `main.c` and is harmless: the fuel delta is
  modulo-32768 so a gap costs nothing, and distance is integrated against the
  clock rather than against frame arrivals.

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

For the once-a-minute write that means roughly 21 ms buffered and 27 ms
dropped, or about ten lost frames: three or four of 0x1A0, a couple each of
0x280 and 0x288, and — at roughly 26 a second at idle — one or two 0x480
among them.

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

The **ordinary** worst pass, 12.8 ms, is inside the 21 ms the FIFO holds, so
outside the EEPROM write nothing is dropped at all.

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
| one received frame, decoded and accumulated | 1.30 ms | 2.0 ms |
| `compute_tick`, worst case | 1.73 ms | 2.5 ms |
| the 100 ms slot | 5.07 ms | 7.0 ms |
| the 1 s slot, excluding the EEPROM write | 0.98 ms | 1.5 ms |

**The ceilings sit about 1.4x above what the code costs today**, which is a
deliberate tightening: they used to be four or five times the cost, and a
ceiling that can never be hit is not a gate. The hardware has far more headroom
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
