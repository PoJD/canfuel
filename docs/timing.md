# How long everything takes

A worst-case budget for the scheduler, against the rates the device has to
hold. Written 2026-08-11, before any of it had run on a board.

**This is static analysis of the code XC8 actually generated, not a
measurement.** That is a real limitation and the last section says how to close
it. What it is not is guesswork: every number below is counted out of the
assembly listing of the hex that gets flashed.

---

## Method

```
xc8-cc -mcpu=18F25K80 -mdfp=... -std=c99 -O2 -mstack=compiled -Isrc \
       -Wa,-a -Wl,-Map=canfuel.map -o canfuel.hex src/*.c
```

`-Wa,-a` makes pic-as write `canfuel.lst`, which carries every generated
instruction with its address and its encoding. Instructions were counted per
function out of that listing, and loops were costed by finding the backward
branches and multiplying the body by the trip count the C source allows.

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
| `tank_median` inner | 300 | insertion sort, n(n−1)/2 at n = 25 |
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
| `compute_tick` (with the tank median) | 19,282 | **4.82 ms** |
| `txframes_gather` (all seven getters) | 19,115 | **4.78 ms** |
| `tank_median` alone | 15,068 | 3.77 ms |
| `persist_load` (start-up only) | 3,670 | 917 µs |
| `compute_power_d` | 3,746 | 937 µs |
| `compute_range_km` | 3,350 | 838 µs |
| `compute_on_fuel` | 2,928 | 732 µs |
| `compute_torque_d` | 2,392 | 598 µs |
| `hal_sys_vdd_c` (plus 22 µs of A/D) | 1,112 | 300 µs |
| `___lldiv`, one 32-bit division | 1,026 | 257 µs |
| `decode_frame` | 507 | 127 µs |
| `hal_can_send` | 286 | 72 µs |
| `hal_can_receive` | 234 | 59 µs |
| `hal_sys_millis` | 25 | 6 µs |
| `hal_sys_isr` (the millisecond tick) | 14 | 3.5 µs |

Two of these deserve a note, because both are dominated by one thing:

- **`tank_median` is an insertion sort**, so its worst case is a reversed
  25-slot ring, 300 comparisons, 3.77 ms. Real data never comes close — 1584 of
  1622 measured samples at rest were the same litre, which is the sorted case
  and costs 25 comparisons — but the bound is the bound. It runs at most once a
  second, and only while the car is standing still.
- **`txframes_gather` is nine divisions in a trench coat.** Nothing in it is
  slow; there are simply ten `___lldiv` call sites in the core and this is
  where most of them get exercised.

---

## The three budgets

### Every pass of the loop

| | Cycles | Time |
|---|---|---|
| `hal_sys_watchdog_clear` + `hal_sys_millis` | 26 | 7 µs |
| FIFO drain, 8 frames, one of them 0x480 | 8,856 | 2.21 ms |
| `compute_tick`, moving, no tank sample | 1,534 | 384 µs |
| `compute_tick`, standing, tank median worst case | 19,282 | 4.82 ms |

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
| `txframes_gather` | 19,115 | 4.78 ms |
| two frames assembled and queued | 818 | 205 µs |
| error counters, overflow flag, LEDs | ~200 | 50 µs |
| **total** | | **5.33 ms** |

**5.3 % of the 100 ms it has.** The remaining 94.7 % is spent draining an empty
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
compute_tick, tank median        4.82 ms
the 100 ms slot                  5.33 ms
the 1 s slot, not writing        0.25 ms
                                --------
worst pass without an EEPROM write      12.6 ms
plus the once-a-minute EEPROM write     ~60.6 ms
```

Against the two deadlines:

- **The 100 ms transmit cadence.** A 12.6 ms pass leaves an **8× margin**. The
  once-a-minute pass leaves 1.65×, so 0x600 and 0x601 arrive up to 60 ms late
  once a minute and the display sees a 160 ms gap instead of 100 ms. Nothing
  reads a period, so this is invisible.
- **`RX_POLL_MS`, the 10 ms the FIFO must not fall behind by.** The worst
  non-EEPROM pass is 12.6 ms, which is over that number — but the number is
  conservative, and what actually matters is the FIFO's depth. Eight buffers
  against roughly four frames per 10 ms is **20 ms of blindness before anything
  is lost**, so a 12.6 ms pass loses nothing. The EEPROM write does overflow
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
