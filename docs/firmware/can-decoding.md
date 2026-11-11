# Decoding the powertrain CAN bus — VW PQ34, AQY engine

500 kbps bus, PQ34 platform. Every value below was verified by measurement on
the car; the logs live in `test/fixtures/`.

Two levels of confidence are distinguished:

- **Confirmed** — holds across every log and is pinned down by a test in `tools/`.
- **Open** — written down but not yet proven. `open.md` holds the open
  questions; none since 8/11/2026 (7, 10 and 11 closed into *Resolved
  questions* below). *This said "the two open questions, 7 and 10" until
  8/11/2026.*

The questions register at the end of this file holds the rest: *Resolved
questions*, answered with the evidence kept, and **Never resolved but not
required**, never answered and **not to be worked on again**. The numbering
runs 1 to 11 across the register and `open.md` and is deliberately not
contiguous within either, because code and other documents cite the numbers.

---

## IDs present on the bus

Fourteen IDs are broadcast periodically:

```
0x050  0x0C2  0x1A0  0x280  0x288  0x320  0x420
0x480  0x488  0x4A0  0x520  0x5A0  0x5D0  0x5D8
```

Pinned down by `test_regular_id_set`. The only one that may be missing from a
short log is 0x520, which arrives roughly once a second.

**0x767 is not a periodic frame.** It appears exactly once, in
`06_trip_reset.txt` on the first timestamp, with DLC 2 and payload `3c fe`.
It is a one-shot diagnostic response captured as the USBtin connected. The
firmware ignores it, but the 0x7xx range can no longer be called completely
quiet because of it.

**0x200 is not periodic either, and it is the tester — settled.** Five frames
in the whole corpus, DLC 3, payload `01 c0 80` every time: three in
`18_coldstart_z1.txt` at 53.077, 53.133 and 90.031 s, and two in
`20_postfix_final_z1.txt`, 56 ms apart. **Every one of them falls where VCDS
was being reconnected to the ECU**: in 18 by accident, after the session fell
over, and in 20 on purpose, as the test proposed below. Every other log with
VCDS attached and logging has none. So it is VCDS opening a session, not the
car. **Confirmed on the unfiltered captures of 10/11/2026** (release
`raw-captures`, `2026-11-10_step8d_*`; the filtered `47`–`48` drop it):
0x200 at every session `tools/vcds_log.py` opened, 16–22 s before the
time stamped in its file, and once at a session opened by hand — so a
capture dates each VCDS connection, which `docs/engine-health/open.md`
used to time a fault-memory clear. The firmware's six hardware filters do not accept it and nothing needs
it; `test_0x200_is_a_one_off_too` pins where it appears.

**It does not travel alone, and that is the part worth keeping.** `0x5D0`
byte 0 is `0x00` in **all 11,251 frames of it in the corpus** — except twice,
and both exceptions sit 81 and 89 ms after a 0x200 in 18:

| 0x200 | 0x5D0 b0 `00 → 02` | back to `00` | held |
|---|---|---|---|
| 53.077, 53.133 s | 53.158 s | 53.350 s | 192 ms |
| 90.031 s | 90.120 s | 90.216 s | 96 ms |

Two for two in 18, on a byte that is otherwise constant across every
recording this project has. ⚠ **But not in 20**: the two 0x200 frames there are
followed by nothing on 0x5D0 at all. Whatever b0 reports, it is something that
happened in 18's reconnection and not in 20's — plausibly the ECU having
dropped the session rather than VCDS closing it cleanly. Nothing here needs it
answered.

**It is not the ECU announcing a misfire, and that was worth testing.** The
attractive reading of a rare frame on an engine with a misfire problem is that
the engine is reporting one. It is refuted by the same overlap that tied the
stumbles to the misfire counter: **in the 231 s where the ECU registered seven
misfire increments, 0x200 appears zero times.** If it were emitted on each,
seven would be expected, and `e⁻⁷ = 0.0009`. All three frames are in the 87 s
where there is no diagnostic data at all.

**What that test also established, and it outlives the question:** every byte
of every identifier was checked against its own ±2 s median at all 44 dips of
engine speed, and **nothing on this bus responds to a misfire except engine
speed itself.** The engine load byte (0x280 b6) and the indicated torque byte
(b7) do not move at all — mean deviation 0.09 and 0.14 counts, against
standard deviations of 12.0 and 17.3 for the bytes themselves. Everything that
appeared to move is a rolling counter or a checksum, recognisable because the
scatter of its deviation equals the scatter of the byte. **Anything this
project ever builds to watch combustion from the bus has engine speed and
nothing else to work with.**

**How it was settled.** In 18 both events fall in the window where VCDS had
dropped the ECU and was being reconnected by hand — 42.4 to 129.3 s, see
`test/fixtures/README.md`. On its own that was suggestive and not a finding:
the window is 27 % of the running log, so two events landing in it is a
**7.5 %** coincidence. The test was two minutes in the next session: with the
engine idling and a capture running, disconnect VCDS from the ECU and
reconnect it. **0x200 appeared, twice, 56 ms apart, and at no other time in
241 s of whole-bus capture.** Attached is not the same as reconnecting, and
this is what separates them.

**A third unexplained event, kept apart from those two on purpose.** At
97.107 s `0x0C2` byte 0 goes `ce → f0` and **never goes back**, while bytes 2
and 3 carry `57 81` for exactly 100 ms and then return to `00 00`. A latching
byte plus a brief pulse is a different shape from the pair above and should not
be lumped in with it. 0x0C2 carries a rolling counter in byte 5 and what
behaves like a checksum in byte 7; nothing in this project decodes it, and
**none of this is being worked on** — it is written down so the next person
finds it rather than rediscovers it.

**Free for the converter:** 0x600–0x603 appear in none of the logs
(`test_target_ids_are_free`).

---

## Signal table

| Signal | ID | Bytes | Formula | Note |
|---|---|---|---|---|
| Fuel counter | 0x480 | 2–3 LE, mask 0x7FFF | 1 = 1 µl | 15-bit, wraps at 32768 |
| Speed | 0x1A0 | 2–3 LE | × 0.005 km/h | validity gate in b1, see below |
| Engine speed | 0x280 | 2–3 LE | × 0.25 rpm | |
| Coolant temperature | 0x288 | 1 | × 0.75 − 48 °C | 0xFF = fault |
| Oil temperature | 0x420 | 3 | − 60 °C | 0xFF with the engine off. `Kombi_2`, the instrument cluster's, per opendbc's `vw_pq.dbc` — question 10 |
| Fuel in tank | 0x320 | 2, mask 0x7F | indicated litres | bit 0x80 = reserve lamp; the scale reads low, `refuel-reset.md` |
| Torque (indicated) | 0x280 | 7 | 1.06 Nm/bit | measured off the full-throttle plateau, see `frames.md` |
| Throttle position | 0x280 | 5 | 38 = rest position (35 on the throttle body fitted 2/10/2026) | |
| Engine load | 0x280 | 6 | | 0 with the engine off; **not decoded by the firmware** |
| Wheel speeds | 0x4A0 | 4× 16-bit LE | (raw >> 1) × 0.01 km/h | bit 0 = direction |
| Acceleration | 0x5A0 | 0 | (val − 127) / 100 G | lateral; **not decoded by the firmware** |
| Doors | 0x320 | 0 | bit mask | |

DLC is constant per ID: 0x050 carries 4 bytes, 0x5D0 carries 6, everything
else 8. A parser that assumes a fixed length of 8 would break on 0x050 and 0x5D0.

**The coolant scale is confirmed against VCDS**, group 001, read off the same
drive as `19_postfix_drive_z1`:

| | VCDS group 001 | 0x288 b1 raw | `× 0.75 − 48` |
|---|---|---|---|
| cold soak | **12.0 °C** | 80 | **12.00 °C** |
| hot, after the drive | 100.5 °C | 198 (fan cycle 193–198) | 96.75–100.5 °C |
| hot, a few minutes later | 99.0 °C | 196 (same cycle) | 96.75–100.5 °C |

Exact at the cold end and inside the fan cycle at the hot end, over 88 °C of
span. All three VCDS values also land exactly on the 0.75 °C grid of the raw
byte (12.0 = 80, 99.0 = 196, 100.5 = 198), which says VCDS reads the same
quantity at the same resolution: **this decode is the ECU's own scale.** The
oil on 0x420 b3 is a different module's and has its own scale, `raw − 60` (question 10).

---

## Trap 1: the speed validity gate is not an equality

Byte 1 of frame 0x1A0 is a **bit field**, not a single value. Measured states:

| b1 | Meaning | Speed |
|---|---|---|
| 0x40 | base valid state | valid |
| 0x48 | valid, **the brake pedal pressed** (bit 3; *The bus byte by byte*) | **valid** |
| 0x50 | valid, a pressure-switch status set (bit 4, dbc) | **valid** |
| 0x43 | post-ignition init ramp | discard |
| 0x42 | same thing, only 2 frames | discard |

The correct rule:

```c
speed_valid = (b1 & 0x40) && !(b1 & 0x03);
```

**Why it matters.** In `07_accel.txt` the majority state is 0x48 — 1301 frames
out of 1991 — and it carries the full speed range including the 24.78 km/h
peak. Testing for equality with `0x40` throws away two thirds of the samples
and distance comes out as 14 m instead of 27 m. That would directly corrupt
FuelAvg and Range, two of the four headline numbers on the display.

The 0x43 ramp shows up in logs that start with the ignition being switched
on (`01_ign_only`, `06_trip_reset`, `25_sessionA_cold_z1`). It lasts ~0.4 s and
the raw value falls 464 → 0 during it. **It also appears when the engine stops
with the ignition left on**: `26_sessionA_warm_z1` is the one log that holds
that, and 0x43 is there for 1.5 s from the same frame as 0x480's reset to zero
(trap 2), nowhere else in its 17 minutes. So it marks an engine-run boundary,
either way. Pinned down by `test_init_ramp_only_after_ignition_on`.

**0x42 is not part of that story, and `17_drive_property_z1.txt` showed it.**
It occurs 134 times mid-drive at 26 km/h, nowhere near an ignition event, and
what it marks is the speed word **freezing** — the value stops updating and
repeats the last one until the state clears. The gate rejects it for the same
reason it rejects the ramp, so nothing downstream ever saw a wrong number; the
claim that was too narrow was the test's, about when the state can occur, not
the decoder's about what to do with it.

`test_the_gate_rejects_every_state_that_freezes_the_value` now asserts the
property rather than the list, so a state nobody has seen yet is caught instead
of quietly accepted.

**A warning to whoever reads b1 next, learned the hard way.**
Bits 0x08 and 0x10 are flags and **not** part of the speed. Reading b1's low
six bits as the value's high byte — which is an easy thing to write in a
throwaway analysis script, and was written — makes 0x48 look like a jump to
21 km/h and 0x50 like a jump to 41 km/h from a standstill, and both look
exactly like a decoder bug worth chasing. The speed is `u16le(data, 2) * 0.005`
and nothing else; `decode.c` has always done this and `S-AQY.TRI` agrees. Four
transitions were checked frame by frame at 7 ms spacing after the correct
formula was restored, and every one is continuous.

## Trap 2: the fuel counter resets when the ignition goes off

The delta is `(new − old) mod 32768`. Without restart detection, the first
delta after the ignition is switched back on jumps by tens of thousands of
microlitres.

```c
if (counter == 0 || rpm == 0) { prev = counter; return; }  /* reinitialise */
```

In `06_trip_reset.txt` this triggers 324 times — and that is correct. Every
detection falls inside the contiguous opening stretch where the ignition is on
but the engine is not running. In `07_accel.txt` it never triggers.

**The reset is the engine stopping, not only the key.** `26_sessionA_warm_z1`
ends with 35 s of ignition on after the engine stopped, and 0x480 drops from
0x90F5 to zero in the frame where engine speed reaches zero, then stays there
— 725 restarts, all in that tail. That is why the rule tests `rpm == 0` as
well as the counter, and why `compute.c` also clears the flow window there.

**A wrap can land exactly on zero, and then this misfires.** Found in
`09_idle_60s_z1.txt`, where the counter runs `32756 → 0 → 0 → 24`: a step of
12 µl happened to carry it to exactly 32768. `counter == 0` reads that as an
ignition restart and reinitialises `prev`, discarding that one step —
**19,561 µl accounted for against 19,573 actually burnt**, which is why that
log reports 2 restarts on a recording where the engine never stopped.

**The rule stays exactly as it is, and that is a decision.** At idle the counter
steps about 12 µl and wraps every 32,768 µl, so roughly one wrap in twelve lands
on zero — about once per twenty minutes of idling — and each one costs a single
step. Tightening it to `counter == 0 && rpm == 0` would trade that against the
risk of missing a real ignition restart, and a missed restart injects up to
32,768 µl of fuel that was never burnt. Twelve microlitres against thirty-two
thousand is not a close call, and the conservative direction is the one that
under-reports.

## Trap 3: bit 15 of the counter is not constant

`docs/sensors.md` in the `mfd15` repo claims bit 15 is constantly 1. **It is not.**
Measured across every log:

- It is **zero** from ignition on until the 15-bit counter first wraps.
- At that first wrap it flips to one and stays there.

It is visible in `06_trip_reset.txt`, where the sequence runs `32767 → 15` and
bit 15 flips from 0 to 1 at the same sample. In `01_ign_only.txt` the bit is
zero because the engine is not running and the counter is all zeros.

It makes no difference to the arithmetic — the 0x7FFF mask drops it, and that
dropping is asserted by a test in both implementations, because a leak here is
worth up to 32,768 µl on every total. **It is not decoded as a flag**: it would
make a usable "this ignition cycle is still young" indicator and nothing wanted
one, so the field was removed.

## Trap 4: FuelAvg divides by an almost-zero distance

The average fuel consumption is a ratio of accumulators. Right after starting,
distance is nearly zero and the ratio runs away — on `06_trip_reset.txt` it
produced **21,395 l/100 km** before the car had moved. Below 100 m of distance
it must return zero.

## Trap 5: a frame that never arrived is not a reading of zero

`decode_init()` zeroes the whole state, so every field starts at a value that
is also a legal reading. For most of them that costs nothing — the
temperatures have `DECODE_TEMP_INVALID`, speed has `speed_valid`, the fuel
counter has `fuel_counter_valid` — but **the tank had neither a sentinel nor a
flag**, and zero litres is a perfectly ordinary tank level. Several fixtures
contain it: `17_drive_property_z1` sloshes between 0 and 3 on a nearly empty
tank. So there is no value that could have meant "nothing said so".

Why it matters more for the tank than for the rest: it is the only decoded
field that feeds state which **latches and is then stored**. The first at-rest
sample initialises the baseline the refuelling rule compares against for the
whole trip, and `persist.c` writes that baseline to the EEPROM, where the next
start restores it. A fabricated zero does not stay a display glitch; it
becomes stored state, and a normal tank then reads as a refuelling.

`tank_valid` is the fix, and the general rule behind it is worth more than the
one field: **a value is data only if a frame carried it.** Anything else is
`decode_init()` wearing the same type.

**No fixture can catch this and neither can the Python reference**, which is
the part to remember. Every recording is of a car whose gauge was talking, so
absence cannot appear in one, and `tools/replay.py` replays the same
recordings. It needs a test that constructs the silence on purpose —
`test_a_silent_bus_invents_no_tank_level` in `test_compute.c` and
`test_a_silent_bus_reaches_the_eeprom_not_at_all` in `test_scheduler.c`.
In the car the gate never fires: 0x320 is periodic and arrives long before the
first sample, which is exactly why only a bench could have shown it.

---

## Trap 6: 0x280's engine speed is recomputed once per 180° of crank, not once per frame

**The signal table above is complete as a conversion and incomplete as a
statement about time.** `× 0.25 rpm` is right; what it does not say is that
consecutive frames usually carry the *same* value, and that how long a value
is held is a property of the engine rather than of the bus.

**First, it is not the logger.** `can-decoding.md`'s *Frame periods* records
that 39–51 % of the lines in the older logs are an immediate duplicate, which
would produce exactly this appearance for no reason at all. It is not that: in
`09_idle_60s_z1` 0x280 arrives 5,639 times in 60.05 s — **93.9 Hz, a period of
10.65 ms against the specification's 10.5** — so no line is doubled. 71.4 % of
those frames are nonetheless byte-for-byte identical to the one before, and
the engine-speed field changes in only 27.8 % of them. **The repetition is the
ECU's, not the recording's.**

**Second, and this is the measurement that says what is happening:** express
the gap between changes as **crank angle** rather than as time, `degrees =
gap[s] × rpm × 6`. `python tools/idledips.py --degrees`, over
`17_drive_property_z1`:

| engine speed | n | update | **crank angle** |
|---|---|---|---|
| 600–900 rpm | 2836 | 39.0 ms | **186°** |
| 900–1200 | 3976 | 30.0 ms | **182°** |
| 1200–1500 | 3125 | 21.0 ms | **172°** |
| 1500–1800 | 1815 | 20.0 ms | **189°** |
| 1800–2200 | 980 | 18.0 ms | **200°** |
| 2200–2600 | 387 | 11.0 ms | **163°** |
| 2600–3200 | 443 | 10.0 ms | **183°** |
| 3200–4500 | 496 | 10.0 ms | 232° — **saturated** |

**A constant 180° from idle to 3200 rpm, across a fivefold change of speed and
a fourfold change of interval.** Above roughly 3000 rpm 180° takes less than
the 10.4 ms frame period, so the bus cannot carry it and the angle inflates —
which is itself confirmation, because that is where a *time*-based mechanism
would have carried on unchanged.

**The scatter of 163–200° is the frame grid, not the engine.** At 800 rpm 180°
is 37.5 ms and only multiples of ~10.4 ms can be observed, so the median lands
on 39. The bands are narrow enough to show this and not narrow enough to
remove it.

### What follows, and what does NOT

**180° of crank is one power stroke.** A four-stroke completes its cycle in
720° and a four-cylinder fires four times in it, so the cylinders take turns
every 180° and each 180° window contains exactly one power stroke, start to
finish. So each value the ECU publishes is the crank's mean speed **across one
cylinder's contribution**, and the step to the next value is how much one
cylinder's contribution differed from the one before it. That is what makes
the step a per-cylinder quantity and what lets `docs/engine-health/open.md` (S1) put a
dip depth into an energy budget at all.

⚠ **"Once per 180°" and "once per firing event" are the same interval on this
engine and the data cannot separate them.** An ECU computing a fresh speed for
each combustion event and an ECU updating on a fixed crank-angle segment
boundary produce byte-identical output here. **This section claims the
geometric statement, which is measured; the combustion statement is an
interpretation of it.** Nothing downstream needs the stronger reading — the
energy budget needs only that the window *contains* one power stroke, which
geometry gives for free. ⚠ An earlier version of this section claimed the
stronger one, from nothing but the interval agreeing with the firing rate at
one speed.

⚠ **There is no cylinder identification and there cannot be.** Which cylinder
a given window belongs to needs camshaft phase, and `What is NOT on the bus`
is where that is. So **one badly misfiring cylinder and four mildly rough ones
are the same statistic.**

**But the STRUCTURE is testable without a name, and it is there.** Each
cylinder comes round every four windows, so one that differs from its
neighbours is a period-4 component in the sequence. `--cylinders` finds that
line at **13–21× its local background in every recording**, against control
frequencies at 0.1–1.5× and a shuffled null at about 1×.

⚠ **That is not a found fault, and reading it as one is the trap.** The
smoothest recording this car has produced carries it as strongly as the
roughest does, so it is **ordinary cylinder-to-cylinder variation**.
`docs/engine-health/refuted.md` A5 has the numbers, the conclusion that a
single bad cylinder is ruled out, and the limit that matters most:
**four equally bad cylinders leave no period at all**, so that hypothesis can
be neither confirmed nor refuted this way.

⚠ **An earlier version of this section said no per-cylinder signature was
present**, from an autocorrelation of the *step* series at lag 4. Wrong series
and wrong statistic: differencing between them hid a line a periodogram of the
values finds immediately. The conclusion drawn from it — that this engine has
no one bad cylinder — happens to survive, for entirely different reasons.

### The consequence for anything derived over time

- **A repeated value is not a new measurement.** At idle each value arrives
  three to four times. Anything that averages, differentiates or counts over
  0x280 *frames* rather than over *changes* is weighting each real measurement
  by however many frames happened to carry it — and since the hold length is a
  fixed crank angle, that weighting moves with engine speed. That is an
  artefact and it looks exactly like a result.
- ⚠ **`decode.c` is unaffected and deliberately so.** It stores whatever the
  last frame carried, which is correct for a displayed engine speed and for
  the torque gate. The trap bites anything *derived over time* from the field
  — which is `tools/idledips.py` and, since 0x604, `compute.c`'s idle grade.

### The idle grade on 0x604, from a raw frame to the byte

**So that the number can be checked rather than trusted.** `docs/firmware/frames.md`
says what the bytes of 0x604 mean and `docs/engine-health/open.md` (S1) what they
read on this engine now; this is the chain between a raw 0x280 frame and the byte on the
wire, on a real capture. Every figure below was printed by re-running
`roughness()` in `tools/idledips.py` over `09_idle_60s_z1.txt` and recording
each step — the capture's own numbers, not a synthetic example and not a
reconstruction from the published byte. The firmware's `idle_grade()` in
`src/compute.c` produces the same byte, and `replay.py --host-build` holds the
two to it over every timestamped fixture.

**Four steps**, all integer, in quarter-rpm (the field's own unit):

1. **Decode** — bytes 2–3, little endian, are engine speed × 4.
2. **Step on change** — a frame that repeats the previous value is the ECU
   holding its last 180° window and is skipped; only a *change* is a firing
   event. The difference is taken in quarter-rpm.
3. **Deadband** — subtract `ROUGH_DEADBAND_RPM` × 4 = 12 and floor at zero.
4. **Average** — `acc += step − (acc >> 8)`, a first-order filter over
   2⁸ = 256 firing events whose steady state is 256 × the mean step. The byte
   is `acc >> 5`: 256 × q4 ÷ 32 = 1/32 rpm.

Sixteen consecutive frames of settled idle, 40.0 s into the log, with the
accumulator as it stood when they arrived:

| t (s) | b2 b3 | rpm_q4 | rpm | | \|Δ\| (q4) | − 12, floor 0 | acc before | acc after | acc >> 5 |
|---|---|---|---|---|---|---|---|---|---|
| 40.000 | `44 0c` | 3140 | 785.00 | change | 60 | 48 | 2566 | 2604 | 81 |
| 40.009 | `44 0c` | 3140 | 785.00 | repeat | — | — | 2604 | 2604 | 81 |
| 40.019 | `44 0c` | 3140 | 785.00 | repeat | — | — | 2604 | 2604 | 81 |
| 40.026 | `44 0c` | 3140 | 785.00 | repeat | — | — | 2604 | 2604 | 81 |
| 40.040 | `4f 0c` | 3151 | 787.75 | change | 11 | 0 | 2604 | 2594 | 81 |
| 40.049 | `4f 0c` | 3151 | 787.75 | repeat | — | — | 2594 | 2594 | 81 |
| 40.061 | `4f 0c` | 3151 | 787.75 | repeat | — | — | 2594 | 2594 | 81 |
| 40.068 | `4f 0c` | 3151 | 787.75 | repeat | — | — | 2594 | 2594 | 81 |
| 40.079 | `5f 0c` | 3167 | 791.75 | change | 16 | 4 | 2594 | 2588 | 80 |
| 40.089 | `5f 0c` | 3167 | 791.75 | repeat | — | — | 2588 | 2588 | 80 |
| 40.097 | `5f 0c` | 3167 | 791.75 | repeat | — | — | 2588 | 2588 | 80 |
| 40.110 | `7a 0c` | 3194 | 798.50 | change | 27 | 15 | 2588 | 2593 | 81 |
| 40.118 | `7a 0c` | 3194 | 798.50 | repeat | — | — | 2593 | 2593 | 81 |
| 40.129 | `7a 0c` | 3194 | 798.50 | repeat | — | — | 2593 | 2593 | 81 |
| 40.139 | `7a 0c` | 3194 | 798.50 | repeat | — | — | 2593 | 2593 | 81 |
| 40.150 | `7e 0c` | 3198 | 799.50 | change | 4 | 0 | 2593 | 2583 | 80 |

With a pencil: the first row is 2566 + 48 − (2566 >> 8 = 10) = 2604, and the
second change, a step of 11 inside the deadband, is 2604 + 0 − 10 = 2594. A
change of 2.75 rpm counts for nothing; one of 15 rpm counts for 12. **Of the
sixteen frames, five are changes** — which is trap 6 in one table, and why a
per-frame average would have diluted the grade by three.

At the end of the log the accumulator is 2314, so **IdleRough = 2314 >> 5 = 72**
(the grade inside the firmware; on the wire only as IdleHealth since layout 2),
2.25 rpm, against an exact mean step of 2.117 rpm over the same 1,488 events.
The two agree to within the filter's memory of the last ten seconds, which is
what a first-order filter is.

**The index.** `IdleHealth = min(200, IdleRough × 25 >> 4)`, so 72 is
72 × 25 = 1800, >> 4 = **112**.

- **100 is measured and then rounded to a shift.** The engine before the
  repair graded 2.12 rpm on two recordings 60 °C of oil apart (`09`, and `18` from
  50 s to 360 s). `IDLE_ROUGH_100` is 64 counts = 2.00 rpm rather than 68 =
  2.12, because 100/64 = 25/16 is a multiply and a shift where 100/68 is a
  division; the 6 % that costs is inside the 13 % the anchor scatters between
  10 s windows.
- **0 is chosen**: no measurable step at all. No engine reaches it, so the
  index always has room to show an improvement.
- **So a reading of 100 means a mean step of 2.00 rpm beyond the 3 rpm
  deadband**, averaged over the last ~256 firing events of settled idle.

**The shape the grade summarises**, as `idledips.py --roughness --hist` prints
it — the share of firing events by the size of the raw step, in rpm, before
the deadband:

| log | what it is | events | 0–2 | 2–4 | 4–6 | 6–10 | 10–15 | 15–25 | >25 | IdleRough |
|---|---|---|---|---|---|---|---|---|---|---|
| `09_idle_60s_z1` | before the repair, oil 85 °C — **an anchor** | 1,488 | 25.1 % | 24.7 % | 21.2 % | 21.6 % | 5.9 % | 1.4 % | 0.1 % | 72 |
| `18_coldstart_z1`, 50–360 s | before the repair, the warm-up — **an anchor** | 8,375 | 25.3 % | 26.1 % | 19.9 % | 20.9 % | 6.2 % | 1.5 % | 0.0 % | — |
| `11_idle_noac_z1` | before the repair, oil 101 °C, A/C off | 573 | 34.7 % | 35.3 % | 18.0 % | 10.3 % | 1.6 % | 0.2 % | 0.0 % | 31 |
| `12_idle_ac_z1` | the same, A/C on | 565 | 42.5 % | 35.2 % | 14.9 % | 7.1 % | 0.4 % | 0.0 % | 0.0 % | 19 |
| `19_postfix_drive_z1` | after plugs, leads, injectors: every idle of the hour | 25,895 | 24.8 % | 24.9 % | 19.3 % | 22.4 % | 7.2 % | 1.4 % | 0.0 % | 94 |
| `24_mafswap_drive_z1` | after the MAF as well | 22,833 | 27.8 % | 27.1 % | 19.5 % | 19.7 % | 4.8 % | 1.1 % | 0.1 % | 54 |

**Read the shape, not the byte.** What moves the grade is the weight in the
6–15 rpm columns — the steps the deadband lets through in full — and the
smooth recordings differ from the rough ones there, not in the tail past
25 rpm, which is nearly empty everywhere. The post-repair drive sits on the
anchors, which is the engine investigation's finding in one row: the repair did
not make the idle smooth.

---

## VCDS measuring blocks

The blocks this project reads through VCDS, their specifications, and how to
record them beside a bus capture are in `docs/engine-health/vcds.md`. None of
it is on the bus; the firmware uses none of it. What the decoding took from
VCDS is recorded where it was used: injection time as 0x288 b6 (question 3),
the load reference in `frames.md`, and the absence of any oil temperature in
this ECU's blocks (`open.md`, the oil question).

---

## Verified values for tests

| Log | What it is | Counter total | Duration | Flow |
|---|---|---|---|---|
| `01_ign_only` | ignition on, engine off | 0 µl | — | 0 |
| `02_idle_60s` | warm idle at 797 rpm | 18,652 µl | 60.1 s | **310 µl/s = 1.12 l/h** |
| `05_rev3000` | 2940 rpm in neutral | 1,940 µl | 1.93 s | 1005 µl/s = 3.62 l/h |
| `06_trip_reset` | standing plus a short crawl | 51,992 µl | 135.0 s | 385 µl/s |
| `07_accel` | acceleration to 24.8 km/h | 9,752 µl | 15.9 s | 613 µl/s |

Coolant warm-up curve across the first session:
`idle` 68.25 → `05_rev3000` 90.0 → `03_drive` 99.0 → `01_ign_only` 100.5 °C.

Distance in `06_trip_reset` comes out as 125 m, which matches the "drive at
least 0.1 km" step in the harness checklist.

---

## Frame periods

The specification quotes 0x1A0 = 7.5 ms, 0x4A0 = 8.0 ms, 0x280 = 10.5 ms,
0x288 = 11.8 ms, 0x480 = 49.5 ms.

**The logs cannot confirm this** and that has to be accounted for. USBtinViewer
timestamps are quantised to ~15.6 ms (the Windows timer tick), so measured
periods come out as multiples: 16, 31, 47, 94, 188 ms. Telling 7.5 ms from
10.5 ms is below the resolution of the recording.

On top of that, 39–51 % of the lines in every log are an **immediate duplicate**
of the preceding frame, same ID and same payload. It has no effect on delta
arithmetic (the delta is zero) but it doubles any measured period.

Indirect evidence for 49.5 ms on 0x480: at that period the idle flow from
`02_idle_60s` works out to 310.1 µl/s, exactly the figure in the specification,
and the recording length to 60.1 s, which matches the file name. That is a
strong agreement.

⚠ **It is not the whole story.** The two logs that *do* carry timestamps imply
an idle flow about half that, and therefore a period about twice as long. Both
answers have corroboration and they cannot both be right — **open question 9**,
which is the most consequential thing on this page and is settled by one
sixty-second recording on a live bus.

---

## The bus byte by byte (10/11/2026)

Every byte of the fourteen periodic IDs, surveyed at the maintainer's
request over the whole-bus fixtures (`01`–`23`) and the unfiltered
capture of 10/11/2026 (release `raw-captures`,
`2026-11-10_step8d_relearn_*`), against **opendbc's `vw_pq.dbc`**
(commaai/opendbc, the PQ platform's message names: the source here as
`Kombi_2` already was for question 10) and the OpenStreetMap wiki's
*VW-CAN* page. **A dbc name is a lead, not a fact**: a row is
*confirmed* only where this car's own data was checked against it, and
the check is said. `tools/canlog.py --states` prints the switches below
as intervals and `odometer_km()` reads the odometer, so the owner no
longer reports them (*the owner*, 10/11; `CLAUDE.md`).

**Ours, decoded before** (signal table above): 0x1A0 b2–b3 speed,
0x280 b2–b3 engine speed, b5 throttle, b6, b7; 0x288 b1 coolant, b6
injection time; 0x320 b2 fuel; 0x420 b3 oil; 0x480 b2–b3 fuel counter;
0x4A0 wheel speeds; 0x5A0 b0 lateral acceleration.

**Confirmed on this car on 10/11** (the dbc's name, then the check):

| ID, byte | what | checked how |
|---|---|---|
| 0x288 b2 bit 3 | **A/C on** (`MO2_Sta_Klima`) | `11` all `0x10`, `12` all `0x18`; on `47` exactly the owner's A/C stretches |
| 0x288 b2 bit 4 | set whenever the engine runs (`MO2_Sta_No_Bet`?) | 0 only at the crank; meaning *not known* |
| 0x288 b3 | **road speed as the ECU has it**, about 1.3 km/h a bit | b3 × 1.31 against 0x1A0's speed over `47` (0.3 % at 46–67 km/h); the dbc puts flags here — this ECU does not |
| **0x288 b5** | **the idle speed target, × 10 rpm** (`MO2_LL_Solldz`) | 90 cold → 80 → 79 → **78 warm**, the engine 15–25 rpm above it (`18`, `41`, `47`); 78 = 780 rpm = VCDS's idle adaptation 128 (`docs/engine-health/vcds.md`); rises off idle to a ceiling of 152 — **question 3 answered** |
| 0x320 b0 bit 0 | driver's door open | the doors row above |
| 0x320 b0 bit 2 | **oil pressure present** (`Oeldruck`) — **a switch's state, not a pressure** | 0 with the ignition on, 4 from the first firing (`47`, 16:21:36); bit 3, the dbc's dynamic oil-pressure warning, never set; no byte carries a pressure value |
| 0x320 b1 bit 1 | **parking brake** (`Bremsinfo`) | on parked at work and from the warm stop to driving off (`47`) |
| 0x320 b1 bit 7 | `Tankstop`, with the reserve | `0x82` only on the low tanks |
| 0x320 b3–b4 | speed the cluster shows (15 bits, × 0.01 km/h) | follows 0x1A0 |
| 0x320 b5 bits 6–7, b6 | displayed speed, 10 bits × 0.32 km/h | follows 0x1A0; **b5 bits 4–5, the turn signals in the dbc, are never set** (the hazard lights of 10/11 not on this bus) |
| 0x420 b0 bit 0 | outside temperature in error — always | so b1, b2 (outside temperature) are 0 (`refuted.md` B11) |
| 0x420 b0 bit 1 | oil temperature in error | with the engine off, beside b3 = 0xFF |
| 0x420 b4 | coolant as the cluster shows it (× 0.75 − 48) | follows 0x288 b1 |
| 0x420 b5 | **the dash dimmer, %: the lights** (`Klemme 58d`) | 0 parked; 93–95 from 16:22:08 on `47`, the lights switched on after the start |
| 0x480 b1 bit 3 | **the engine lamp (MIL)** | on with the ignition, off seconds after the start, **on again 2–5 s into every injector cut** (`31`, `41`, `43`, `44`) and until the clear (`46`), and with the engine stopped and the ignition left on (`26`, `33`, `37`, `39`). **Lit with the engine running through every capture of early August** (`01`–`07`, 153,029–153,031 km) — **P0411, a secondary-air hose torn off in the heater work, cleared on 11/8 at 16:39** (the owner's VCDS photograph; `docs/engine-health/vehicle-history.md`) — and out in every capture after it (`09`–`17`, 153,032 km); no other lit lamp with the engine running in any capture since |
| 0x480 b1 bit 5 | **the ECU cutting the A/C compressor** (`MO5_KlimaKompr`) | at every crank and through basic settings (`48`, `20`); the A/C came on the moment it ended |
| 0x488 b3 | the dbc's **altitude correction** (`Hoeheninfo`, × 0.00787) | 0x8D nearly always, 0 with the engine off; its 32 one-frame drops to 0x8C on `47` (17:29–17:35) are a slow factor stepping between two values, which the name explains and a fault would not (*reasoned*; not checked against an altitude) — *this said "around the ECU flagging P0137" until the survey* |
| 0x520 b5–b7 | **the odometer, km** (`Kilometerstand`, 20 bits) | 153,029–153,033 in August, 153,569 on 24/9, **155,834 → 155,853 on 10/11** — the owner's figures in the same range (`docs/engine-health/vehicle-history.md`) |
| 0x520 b2 | key information (`Schluesselinfo`) | 3 always |
| 0x5D0 b0 bit 1 | **the powertrain bus in diagnosis** | one frame with each 0x200, VCDS opening a session |
| 0x1A0 b1 bit 3 | **the brake pedal** (`BR1_Lichtschalt`) | Trap 1's `0x48`; on in every slowing to a stop of `47` |

**Named by the dbc, consistent with this car, not checked further**
(none bears on the engine): 0x050 Airbag_1 (b1 the belt switches and the
airbag lamp, b2 a counter, b3 a checksum); 0x0C2 steering angle and
rate, its counter and CRC; 0x1A0 b0 ABS/ASR/EBD interventions, b1 bits
0–1 the ABS/ASR lamps (Trap 1's ramp), bit 4 a pressure-switch status
(`0x50`), b4–b5 an ASR torque request (`0xFE` = none), b7 a counter;
0x280 b0 bit 0 the pedal at rest (`Leergasinformation`; the clutch bit
3 never set); 0x5A0 b1–b2 mean wheel speed, b3–b4 a time stamp, b5–b6
path pulses, b7 = `0x80 | 43` pulses per revolution; 0x5D0 b1–b5 and
0x5D8 the car's identity and installed-module list, constant.

**What the dbc names otherwise, from this car's data**: **0x280 b6 is
`mechanisches Motor-Verlustmoment`**, the engine's own friction torque,
and **b7 `Fahrerwunschmoment`**, the torque the driver asks for, with
b1 and b4 the inner torque with and without interventions. This file
has called b6 *engine load* and b7 *indicated torque*: **b7's 1.06
Nm/bit and the drag line were measured, not named** (question 8,
`frames.md`), so nothing in `src/` changes; the names are recorded so
that the next reading of b6 starts from friction, not load.

**Constant or not populated on this car**: 0x050 b0; 0x0C2 b4 (170),
b6; 0x1A0 b6; 0x288 b4, b7; 0x320 b7; 0x420 b1, b2, b6 (255), b7; 0x480
b4 (the dbc's radiator fan, % — always 0: the AQY's fan runs off a
thermo switch), b5–b7; 0x488 b0–b2, b4–b7 (255: no automatic gearbox);
0x520 b7 high nibble; 0x5D0 b1–b5; 0x5D8.

**Not known** — the list for the next person, searched in the dbc and
the forums (OSM wiki *VW-CAN*, the dbc, forum and bulletin searches,
10/11) without an answer:

| ID, byte | what is seen |
|---|---|
| 0x288 b0 | four values in rotation (0x05, 0x5D, 0x8F, 0xDA), one per frame; a multiplex counter or a check byte — the OSM page sees the same, unnamed |
| 0x480 b0 | the same kind: four values in rotation (0x11, 0x5A, 0x94, 0xF2) |
| 0x520 b0–b1 | four value pairs in rotation, about one a second; not in the dbc's Kombi_3 |
| 0x520 b3–b4 | the dbc's `Standzeit`, × 4 s: steady within a log (660 s on 10/11 after the battery was off for hours; 60,124 and 62,660 s on 24/9) and fitting no soak the owner gave — *not trusted* |
| 0x288 b2 bit 5 | `0x30` in some old logs; *not looked into* |
| 0x420 b0 bit 7 and 0x480 b1 bits 1–2, 4, 6–7 | named in the dbc (cluster fault entry; glow, E-gas, overheat lamp, fan, A/C reduce), **never set on this car**, so nothing to check |

## What is NOT on the bus

- **Lambda** — 0x488 is `ff ff ff 8d ff ff ff ff` in every log; b3 is
  the altitude correction, not lambda (*The bus byte by byte*).
- **Battery voltage** — searched systematically, nothing. Solved with the
  display's internal sensor instead.
- **Ambient temperature** — 0x420 b1 and b2 are both zero, so it is not on
  those bytes. ⚠ **This used to read "the car has no sensor" and that was
  wrong**: the car displays the outside temperature next to the clock in the
  rear-view mirror console, photographed reading 20.5 °C. Whether it reaches
  that display on some other frame or on its own wire is unknown and **nobody
  should go looking** — nothing in this firmware or on the MFD15 consumes an
  ambient temperature. `refuted.md` B11.
- **Trip odometer and trip reset** — see open questions.

---

## Open questions

**None is open** since 11 closed on 8/11/2026 (*this said "one is open,
11" until 10/11/2026*). The numbering is unchanged across the register because code and
documents cite it, so it is not contiguous in any one section: renumbering
would silently break every `question 7` in the tree.

The register is below: **Resolved** holds 1 to 11, kept with their
evidence because a closed question that does not say how it was closed
reopens itself; **Never resolved but not required** is empty since
10/11/2026, when 3 was reopened by the maintainer and answered. The two
are kept apart on purpose: the first says what the answer is, the second
says there is no answer and none is wanted.

The engine's own faults are not in this register at all; they are
`docs/engine-health/open.md`.

---

## Resolved questions

Ten that were settled, each with its answer and the evidence that closed it
— the evidence is what stops a question being reopened by somebody arguing from
first principles, the same case `refuted.md` makes for itself. The long
write-ups that led here are in `git log`.

### 1. ~~What is the real period of 0x480?~~ — **closed: there isn't one**

The question was wrong, not unanswered. With adapter timestamps, stationary and
warm (`09_idle_60s_z1`, `10_rev2600_z1`):

| | 797 rpm | 2586 rpm |
|---|---|---|
| 0x480 frames/s | 26.4 | **18.0** |
| mean gap | 37.9 ms | **55.5 ms** |

Engine speed rose 3.25× and the frame rate **fell**; dropped frames cannot
explain it, since throughput was higher in the revs log. Every gap sits on a
**10 ms grid** — the engine ECU's scheduler tick, which 0x0C2, 0x280, 0x288
and 0x488 share — but there is no single multiple of it. A lost frame can only
merge two intervals, never produce a shorter one, so the grid is hard evidence
whatever was dropped.

**The per-injection hypothesis was tested and refuted**: at idle 26.4 frames/s
against 26.6 injections/s and 12.3 µl per frame against a modal counter step of
12–13 µl — three quantities agreeing — but at 2586 rpm the ratio collapses to
0.209. Worth remembering the next time three numbers agree. At idle 31 % of
0x480 frames carry an unchanged counter, at 2586 rpm almost none; nothing
depends on it.

**The consequence.** `tools/replay.py`'s synthesised time for the five
untimestamped fixtures (an assumed 49.5 ms per 0x480 frame) is **invalid**, not
merely imprecise, so their durations, flows and distances are not facts about
the car. Fuel totals are unaffected because the counter is absolute — which is
why the core accumulates the counter rather than integrating a flow. The
firmware runs off its own crystal and never cared. Old fixtures that ever need
a clock are re-recorded with `Z1` (question 9).

### 2. ~~The starting counter value in `07_accel`~~ — **closed**

The specification quotes 13247 → 22622 while the file starts at 12870.
**Confirmed exactly**: the counter reaches 13247 at 0x480 frame #23 of 290,
1.14 s in, and the fuel between is 377 µl to the microlitre. The specification
was computed from 1.14 s in. No discrepancy exists.

### 3. ~~0x288 b5 and b6~~ — **closed 10/11/2026: b6 is injection time, b5 the idle speed target**

**Reopened and answered 10/11/2026, at the maintainer's request** (a
survey of every byte on the bus, *The bus byte by byte*): **b5 is the
idle speed target in tens of rpm**, opendbc's `MO2_LL_Solldz` checked on
this car — 90 at a cold start (the engine at 926 rpm), 80, 79 and **78
warm** (the engine 795 rpm), and 78 is the 780 rpm of VCDS's idle
adaptation 128 (`docs/engine-health/vcds.md`). Off idle it rises with
the engine to a ceiling of 152 — the "pins at 152" below, a target and
not an advance; "78 to 126 within 900–1100 rpm" is the target moving at
a crawl and after a lift. *Until then this sat under "Never resolved but
not required", with the text below as it stood.*

**Why it is here.** Nothing in the firmware reads either byte. `decode.c`'s
`CAN_ID_COOLANT` case takes b1 and stops there, no transmitted frame carries
b5 or b6, and no test asserts anything about them. (Do not confuse them with
0x280 b5 and b6, which *are* decoded — those are throttle and load.) This was
curiosity with a use — an air mass would have let
a proper torque model replace the two-point drag line — and the air-mass
candidate is precisely the one that was eliminated. So the use is gone and the
curiosity is what remains.

b6 came out of it decoded, which is a genuine result. b5 is exhausted in the
sense that matters: all three candidates anyone had are refuted, and there is
no fourth to test. Another session would be a fishing trip, not an experiment.

The session happened, recorded as `docs/engine-health/vcds.md` describes;
`test/fixtures/11`–`16` and `test/fixtures/vcds/` are the data.

**b6 is injection time.** Across six holds:

```
b6 = 12.51 x injection_time_ms - 0.63      r = 0.9954
```

The intercept is effectively zero, so the scale is about **0.08 ms per bit**
and residuals stay inside ±2 counts. Nothing in the firmware wants it, but it
is decoded now rather than a candidate.

**b5 follows ignition advance and then stops following it.** Below roughly 16°
it fits `b5 = 4.22 x advance + 82`; from 1838 rpm upwards it sits on exactly
**152** while the advance keeps climbing 18.1 → 22.5 → 23.3°. Two things are
true at once and only one of them is explained.

**That hypothesis was tested the same afternoon and is refuted.**
`17_drive_property_z1.txt` and `vcds/vcds-ride-002-003.csv` are six minutes of
driving on private land, engine speed 537–4986, b7 from 7 to 185, throttle from
closed to 85°. Above 1900 rpm:

| | over the drive, rpm > 1900 |
|---|---|
| ignition advance, VCDS | **+3.0 to +22.5 °BTDC** — a spread of 19.5° |
| throttle angle | 3.5° to 85.1° |
| **0x288 b5, CAN** | **152 in all 2,161 samples. One distinct value.** |

The advance moved through nineteen and a half degrees and b5 did not move by a
bit. **b5 is not ignition advance.**

**This comparison needs no clock alignment**, which is why it is the one to
trust: it is two ranges over the same six minutes, not a sample-by-sample
pairing. That matters because the pairing was attempted and is unreliable —
see below.

**All three original candidates are now exhausted.** Mass air flow was
eliminated by the stationary sweep, injection time is b6, and advance is
refuted. b5 is something nobody has guessed yet.

What is known about it, and it is not much:

- it rises with engine speed to about 1900 rpm and then **pins at exactly 152**
- it is bounded below at **78**, which is its idle value in every recording
- below the ceiling it does vary at constant engine speed — 78 to 126 within
  the 900–1100 rpm band — so it is not a pure function of speed either

**Why the drive could not settle more than that.** VCDS samples about 1.7 times
a second, polls its two groups at different instants, and injection time swings
between 1.6 and 11.9 ms while driving. Cross-correlating the two engine-speed
traces aligns them at a lag of 44.0 s with r = 0.9896, but that is one number
for six minutes and it cannot track drift. Filtering down to samples where the
engine speed is locally steady leaves **27 of 902**, nearly all of them idle,
because a short piece of private land has no steady state above idle. The
stationary holds are the trustworthy dataset and the drive is the wide one; for
anything that changes fast, only the holds can be paired.

The same caution applies to **b6's scale**: the six holds give 0.08 ms/bit at
r = 0.9954, the drive pairing gives 0.147, and the holds win for the reason
above. Comparing the two ranges instead does not help either — VCDS took 902
samples where the adapter took 29,658, so the extremes it never sampled are not
evidence of anything.

**One candidate is eliminated outright and it cost nothing.** Mass air flow
rises 4.44 → 5.13 → 6.72 → 8.19 g/s across holds 3–6 while b5 sits on 152 and
b6 barely moves, and at the two idle holds the compressor raises the air mass
while b5 does not shift a bit. Neither byte is the air mass.

### 4. ~~Is 0x420 b3 oil or IAT?~~ — **closed: it is oil, from a real sensor**

Ordered by coolant, the fixtures give a warm-up curve that lags it — 32 → 91 °C
while the coolant goes 68 → 99 °C — highest in the one log with air moving
through the engine, where an intake temperature would fall:

| Log | Coolant | 0x420 b3 |
|---|---|---|
| `06_trip_reset` (cold start) | 54.0 °C | 255, then 31 °C |
| `idle` | 68.25 °C | 32 °C |
| `07_accel` | 75.75 °C | 47 °C |
| `05_rev3000` | 90.0 °C | 56 °C |
| `02_idle_60s` | 96.75 °C | 86 °C |
| `03_drive` | 99.0 °C | 91 °C |

**Measured directly as well**: at the end of `18_coldstart_z1` this channel
extrapolates to 29 °C where VCDS block 006 read the intake at **22.5 °C**.

**Not oil pressure** (`refuted.md` B10): it does not move when the engine
starts, is not zero with it stopped, and ratchets one count per hold rather
than tracking engine speed. **Not computed from the coolant**: in `15` the
coolant fell five counts while this rose two.

**A sensor, not a model**: across every fixture the byte takes 85 steps up and
58 down, every one exactly ±1 count, and dithers both ways through a steady
hold — what an analogue sensor does and arithmetic does not.

**255 is the fault / not-yet-available value** (it decodes to 195 °C, which
the display latches as an oil maximum), not a signature of a stopped engine:
`08_ign_only_z1` and the 41 s before `18` fires both read a real temperature.

**What supplies it — looked up, not measured.** Parts catalogues, workshop
pages and forums name the **oil level and temperature sender G266** in the
sump, wired to the instrument cluster, not the engine ECU — which is why
`01-Motor` has no oil temperature block. ⚠ That makes the oil byte the
cluster's and the coolant byte the ECU's: **two modules with no reason to
share a scaling**, and this firmware borrowed the coolant's `× 0.75 − 48`.
Whether the number is *right* is question 10, below.

### 5. ~~AccelG — longitudinal or lateral?~~ — **closed: it is lateral**

> The firmware no longer accepts 0x5A0; the display reads it straight off the
> bus. This stands as a fact about the car.

**Measured on the MFD15**, full lock, several laps at 15–20 km/h:

| Test | Reading |
|---|---|
| circling **left** | **+0.2 to +0.5 G**, steady, rising with speed |
| circling **right** | the same, **negative** |
| pulling away and braking | a few hundredths |

The sign inverts with the turn, the magnitude tracks cornering force, and
braking is the small number. **The scale is right too**: at a turning radius of
about 5.5 m, v²/r gives 0.20 G at 12 km/h, 0.32 at 15 and 0.51 at 19 — the
measured range — so `(raw − 127)/100 = G`. Positive is a left turn, consistent
with ISO 8855; nothing needs inverting. Standing still it reads 127–128,
0.00 G. The fixtures could never have closed it: they were recorded crawling
across an uneven lawn, where tilt swamps 0.04 G.

### 6. ~~Source of the trip reset — candidate 0x5D8 b0~~ — **candidate eliminated, question retired**

All eight bytes of 0x5D8 are constant through `06_trip_reset` (`21 05 00 00 00
00 00 00`), and so is 0x5D0; a sweep of every byte of all fourteen identifiers
for anything that grows and then falls finds only the fuel counter and the oil
warming. Caveat: 124.6 m would tick a 0.1 km counter once, so this eliminates
the candidate rather than proving the trip odometer absent. **Retired because
it no longer matters**: the average resets on refuelling (`refuel-reset.md`).
If a second trigger is ever wanted: a 3 km drive with the USBtin running and
the reset pressed halfway, then the same scan.

### 7. ~~The drag line on hot oil~~ — **closed 15/10/2026: it was fitted on hot oil**

**What the firmware ships.** A least-squares line through the four warm
free-revving holds `13`–`16`, stationary in neutral where b7 *is* the drag:

| hold | rpm | b7 | oil |
|---|---|---|---|
| `13_rev1500_z1` | 1536 | 18.81 | 101 °C |
| `14_rev1850_z1` | 1850 | 20.66 | 103 °C |
| `15_rev2372_z1` | 2372 | 26.32 | 104 °C |
| `16_rev2926_z1` | 2926 | 27.23 | 106 °C |

```
drag_b7   = 9.11 + 0.006514 x rpm        residuals -0.9 to +1.8 counts
drag [Nm] = 9.66 + 0.00690  x rpm        at 1.06 Nm/bit
```

It replaced a cold-oil line (56–85 °C) that overstated drag by 4 counts at
idle and 10 at 2930 rpm, and took the share of `17_drive_property_z1` showing
a torque from 49 % to 78 %. The idle point is excluded and covered by the
driving gate instead (`frames.md`).

**Why it was open, and why it is not.** The question was whether real
driving runs the oil hotter than the holds, so that drag there is lower and
the line overstates it. With 0x420 read as `raw − 60` (question
10), **the holds were at 101–106 °C and real driving runs at 98–107 °C**
(the hottest recorded is `16` and `17`, 107 °C; 56 minutes of hard driving,
`19`, 105 °C): the line is fitted where the engine runs. Nothing to refit.

**When it moves, `TORQUE_CNM_PER_BIT` moves with it** — one calibration,
never one half alone (`config.h`, `frames.md`). It would move only if
a thermometer in hot oil (question 10, *What would reopen it*) found the
warm end several degrees out.

### 8. ~~The torque byte's scale~~ — **closed: 1.06 Nm/bit, measured off the full-throttle plateau**

Held full-throttle pulls in 4th (`19_postfix_drive_z1`), median b7 in a
±150 rpm window, drag held in bytes:

```
170 Nm @ 2400:   b7 185,  s = 170   / (185 - 24.74) = 1.061 Nm/bit
 85 kW @ 5200:   b7 191,  s = 156.1 / (191 - 42.98) = 1.055 Nm/bit
```

Two ratings against two readings, 0.6 % apart; `TORQUE_CNM_PER_BIT` is 106.
The plateau is where the engine runs out of air (relative load flat at
78–81 %), not where a burst ended. `frames.md` has the whole argument and the
caveats (intake temperature not logged, a chipped ECU calibrated against stock
ratings).

**It refuted the old derivation** from b7 = 255, which read 30 % low
(`refuted.md` B12). **It also closed the VCDS route**: this ECU has no torque
block in Nm — groups 001, 002, 003 and 020 offer only load in per cent — and
b7 is not that load either: in holds `14`–`16` load sits at 17.0–17.3 % while
b7 climbs 20.7 → 27.2, which is what an *indicated torque* does as friction
rises with speed.

### 9. ~~Two fixtures carry timestamps and disagree with the other five about time~~ — **closed: the timestamps are wrong**

`06_trip_reset` and `07_accel` carry USBtinViewer's timestamps, which its own
documentation says are *"generated in the application on the host, the
hardware timestamping is currently not used"*
([EmbedME/USBtinViewer](https://github.com/EmbedME/USBtinViewer)) — a Java GUI
stamping about 700 lines a second, with 39–51 % duplicate lines and gaps
clustered on the 15.6 ms Windows timer tick.

**Measured with the adapter's own clock** (`09_idle_60s_z1`, 796 rpm, A/C off):

```
19,561 ul over 60.027 s  =  325.9 ul/s  =  1.17 l/h
```

| base | idle flow | verdict |
|---|---|---|
| assumed 49.5 ms period | 310 µl/s = 1.12 l/h | within 5 % |
| USBtinViewer timestamps | 157 µl/s = 0.57 l/h | **out by a factor of 2.1** |

So the durations, flows and distances of `06` and `07` are overstated by about
two; their fuel totals stand. **Only the `_z1` logs have trustworthy time.**

**How to record with a real clock** — no board, no firmware:
`tools/usbtin_capture.py` drives the adapter over its serial port with `S6`
(500 kbit/s), **`Z1` (hardware timestamps on)** and `L` (listen-only), reads
the status flags with `F` afterwards, and writes the raw slcan stream that
`canlog.py` parses ([fischl.de/usbtin](https://www.fischl.de/usbtin/)). **Record
the whole bus and filter afterwards**: no acceptance filter is set, because the
mask polarity is documented nowhere we hold and a filter that passes nothing is
indistinguishable from a dead bus.

### 10. ~~Does the oil sender read right?~~ — **closed 23/10/2026 at the owner's decision: the scale fits, the cold end's few degrees accepted**

**Closed by the owner** (23/10/2026): the scale was settled on 15/10 and
everything read on it since sits where a warm engine's oil runs — 98–107 °C
in the captures, 105–110 °C on hard runs and 111 °C at the most, off the
display. The cold end's 2–5 °C above the coolant is accepted as the
cluster's own sender, and no thermometer reading was taken: **it is closed
on agreement, not on the warm-end measurement**, which is said here so that
nobody cites it as one.


**The scale is `°C = raw − 60`** (*decided 15/10/2026*): 0x420 is the
instrument cluster's `Kombi_2`, and commaai's opendbc `vw_pq.dbc`
(MIT-licensed, `github.com/commaai/opendbc`, fetched 15/10/2026) defines
byte 3 as `Oeltemperatur_4_1 : 24|8@1+ (1,-60)`. It is in `src/decode.c`
(`oil_c100()`), `tools/canlog.py` (`oil_c()`, which every tool uses) and
`mfd15/tri/S-AQY.TRI`.

**Why that file is believed** — it is a community file, not a VW document:

- **the rest of its `Kombi_2` fits this car.** Byte 0 bit 0,
  `Fehlerstatus_Aussentemp`, is set in every frame with the ambient bytes 1
  and 2 at zero — the cluster saying it has no ambient sensor, which
  `refuted.md` B11 found the hard way (the mirror's thermometer is its own).
  Byte 4, `Kuehlmitteltemp__4_1__Kombi_2_ (0.75, −48)`, is the cluster's
  coolant and tracks 0x288's 3–10 °C below it — the cluster's own sender
  (*general*: these engines carry one for the ECU and one for the
  cluster). **This cluster has no coolant needle** (*owner*): only a blue
  lamp while cold (below about 62 °C) and a red one, lit when too hot and
  flashing when the coolant is low — so byte 4 is the one place its
  sender can be read;
- the German names with their `_4_1` suffixes are VW's message-matrix
  style, so it reads as taken from VW's matrix rather than fitted to a log
  (*a judgement*);
- **an Audizine thread on the RS4's 2.7T** reads 0x420 byte 3 as oil,
  `x − 60`, from its own logging;
- **this car's soaks give the same slope on their own**: oil counts
  against coolant counts at eight cold soaks fit 0.68 oil counts per
  coolant count (r = 0.92), about 1.1 °C a count against `Kombi_2`'s 1.0;
- **warm, the oil sits at 98–104 °C**, at or a little above the coolant,
  which is where a warm engine's oil runs (*general*); the hottest recorded
  is 107 °C (`16`, `17`).

The encoding is the DBC's whole — slope and offset — rather than an offset
fitted to the soaks below (*decided 15/10/2026*, the owner's question): an
encoding has no error of its own; what can be off is the sender's reading,
and an offset fitted at one temperature would be a calibration of that one
sender carried untested to the warm end where the reading is used.

**Who reads it.** `st.oil_c100` is decoded and consumed by nothing in this
firmware. The display shows `OilTemp` straight off 0x420 through `mfd15`,
and the engine investigation compares every `IdleHealth` reading at a
matched oil temperature — on the same channel, so a bias in it moves both
sides of a comparison alike.

**What stayed open: the cold end reads a few degrees high.**

After a full soak the oil and the coolant should both sit at ambient. They
do not quite:

| soak | coolant (0x288) | oil | oil − coolant |
|---|---|---|---|
| `18_coldstart_z1`, 11/9, ~10 h | 16.5 °C | 21 °C | +4.5 |
| `19_postfix_drive_z1`, 24/9, ~19 h, ambient 10.0 °C | 12.0 °C | 17 °C | +5.0 |
| 26/9, ~10 h, cold fog; *owner-reported off the display, whole degrees* | 14 °C | 19 °C | ≈ +5 |
| `25_sessionA_cold_z1`, 3/10, 27 h, evening | 18.0 °C | 21 °C | +3.0 |
| `27_sessionA2_cold_z1`, 4/10, ~15 h | 15.75 °C | 19 °C | +3.25 |
| `30_step2b_z1`, 9/10 | 15.0 °C | 17 °C | +2.0 |
| `31_step4_drive_z1`, 10/10 | 13.5 °C | 18 °C | +4.5 |
| `32_step3_item1_z1`, 12/10 | 10.5 °C | 15 °C | +4.5 |
| `33_step3_gauge_cold_z1`, 14/10 | 15.75 °C | 20 °C | +4.25 |
| `35_item5_drive_z1`, 15/10, a cold, damp morning | 10.5 °C | 14 °C | +3.5 |

*15/10/2026, evening, off the display* (the new TRI's first reading,
*owner*, photographed): after a few hours in a garage, ignition on,
**coolant 40 °C, oil 41 °C** — +1, inside the display's whole degrees;
the old scale would have shown the oil at 28. Not a full soak, so not a
row of the table, but the first reading on the display that puts the oil
where a cooling engine's oil should be.

*Warm, the same evening* (*owner*, off the display): on the hardest
drive yet — motorway at full throttle, ~10 min at 5000 rpm — the oil
peaked at **106 °C with the coolant at 92 °C**, oil above coolant under
sustained load as a healthy engine's runs (*general*), and inside the
98–107 °C the captures record.

Each row the first 0x288 and 0x420 frame after ignition-on. **The oil reads
2–5 °C above the coolant and, on 24/9, 7 °C above the ambient** — not
where a soaked sump sits; the cluster's coolant byte errs the other way
(7.5 °C that morning). So the cluster's two senders are each a few degrees
out at the cold end. G266 measures the oil level thermally, by heating,
which could bias its temperature (*general*, not checked on this sender).

**What it costs**: a few degrees on the display when cold, and nothing
known when warm — which is the question.

**What would reopen it** — the two measurements that were its tests, kept for whoever has a winter morning or a thermometer:

1. **A winter morning, the engine not started.** The car outside overnight,
   **ten hours or more**, so that both sit at ambient; ignition on, and
   within the first twenty seconds `OilTemp` and the coolant off the
   display — or a 20 s capture for the raw bytes (the MFD and the capture
   are one or the other, `CLAUDE.md`). The soaks above span only 10.5–18 °C
   of coolant. **If the oil still reads 2–5 °C above the coolant at −5 to
   −10 °C**, the error is a constant offset and the warm readings are as
   good as the cold ones; **if the gap grows or shrinks**, the sender's own
   slope differs and the warm end is uncertain by about as much. *Decided
   15/10/2026*: a constant few degrees changes nothing; a drift of several
   per 20 °C would be written down beside the channel, and nothing in `src/`
   or the TRI file moves for less than that.
2. **A thermometer in hot oil, straight after a hard drive**, against
   `OilTemp` at the same moment — the direct answer at the warm end. Best a
   thin K-type thermocouple down the dipstick tube, marked at the dipstick's
   length; an IR thermometer on the sump or filter reads a surface cooling
   into the air, not the oil. **The Extol IR thermometer bought for this
   (1/10/2026) was broken the same month** (*owner*), and the one IR reading
   taken, on the filter after the 24/9 drive (the old instrument, stopping at
   60 °C, emissivity not recorded), sat 16 °C below the channel and is **not
   trusted** (*owner*, 15/10/2026). Optional.
3. **VCDS cannot do it**: this ECU has no oil temperature in any block
   (`docs/engine-health/vcds.md`). Do not spend a session looking.


### 11. ~~`IdleHealth` does not follow VCDS group 014 — what should it measure?~~ — **closed 8/11/2026 at the owner's decision: `IdleHealth` stays as it is, `Misfires` beside it**

*Raised by the owner, 4/10/2026.* After step 1b the ECU's misfire counter
(group 014) read zero at both warm stops for the first time, the owner
felt the calmest idle yet, and `IdleHealth` read about what it had read
the day before. The owner wants the grade **as close to how the ECU
measures as the bus allows**.

#### What was measured

Every standing stop of 60 s and more, oil above 57 °C, in the four
captures that have a 014 log beside them, 014 aligned on engine speed
(the method of `docs/engine-health/open.md` S3). Candidate grades from
0x280, each over the whole stop:

| log | oil | 014 a minute | `IdleHealth` | dips a minute (`dips_cheap`) | one slow firing ≥ 6 / 8 / 12 rpm, a minute | mean second difference, rpm |
|---|---|---|---|---|---|---|
| `19` | 72 °C | 8.0 | 123 | 16.4 | 47 / 21 / 1.3 | 6.54 |
| `19` | 88 °C | 2.0 | 64 | 10.4 | 29 / 9.7 / 1.1 | 5.90 |
| `19` | 97 °C | 0.0 | 112 | 28.4 | 68 / 19 / 3.8 | 6.76 |
| `19` | 99 °C | 0.0 | 146 | 22.1 | 78 / 39 / 3.1 | 6.42 |
| `24` | 97 °C | 9.6 | 84 | 10.9 | 36 / 11 / 0.5 | 5.56 |
| 3/10 | 87 °C | 17.5 | 114 | 12.4 | 38 / 13 / 0.7 | 6.32 |
| 3/10 | 97 °C | 5.0 | 62 | 14.9 | 8.9 / 2.0 / 0.0 | 4.28 |
| 4/10 | 64 °C | 0.0 | 117 | 14.7 | 35 / 13 / 1.1 | 5.84 |
| 4/10 | 83 °C | 0.0 | 109 | 10.1 | 38 / 11 / 0.5 | 5.89 |
| 4/10 | 99 °C | 0.0 | **60** | **5.6** | 18 / 4.7 / 0.1 | 4.81 |
| 4/10, after a hard drive | 101 °C | 9.1 | 92 | 10.1 | 16 / 2.9 / 0.3 | 5.00 |
| 4/10, the MAF wiggle | 101 °C | 14.6 | 79 | 12.8 | 16 / 3.6 / 0.0 | 5.69 |

*One slow firing* is the shape a lone misfire leaves on crank speed: one
180° value below **both** its neighbours by at least the threshold — the
nearest thing on the bus to the ECU's per-cylinder segment times.
*Second difference* is |x₋₁ − 2x + x₊₁| over the same values. `24`'s
first stop has no 014 beside it and is left out.

**Rank correlation with 014** (Spearman, stops with detection active):

| grade | all 12 | new MAF only (`24`, 3/10, 4/10), 8 | hot only, 7 |
|---|---|---|---|
| `IdleHealth` | −0.12 | +0.05 | −0.22 |
| dips a minute | −0.09 | +0.27 | −0.30 |
| one slow firing ≥ 6 | −0.34 | −0.02 | −0.48 |
| one slow firing ≥ 8 | −0.24 | +0.12 | −0.48 |
| one slow firing ≥ 12 | −0.36 | −0.04 | −0.50 |
| second difference | −0.17 | +0.24 | −0.15 |

#### What it says

- **No grade the bus allows follows 014** — not the current one, not a
  dip count, and not the shape-of-a-misfire detector built to imitate the
  ECU. Twelve stops is a small sample, but nothing is even close.
- **Why** (*reasoned*): the ECU times the crank per cylinder off its own
  sensor, against thresholds that move with load — which is why 014
  changed its ruler when the MAF did (`docs/engine-health/refuted.md`
  A11), and why `19` reads the roughest idle on record with 014 at zero.
  0x280 carries one recomputed speed per 180° (`can-decoding.md` trap 5);
  whatever the ECU sees in a single firing does not survive into it.
  **014 cannot be rebuilt from the bus**, and it is not on the bus.
- **What the grades do follow is the idle's smoothness — what the owner
  feels.** At the hot stop `IdleHealth` went 146 → 84 → 62 → **60** from
  `19` to 4/10 and the dip count 22 → 11 → 15 → **5.6**; 4/10's hot stop
  is the smoothest since August by both, which is what the owner felt
  (August's one hot hold, 22 s, graded 48; `docs/engine-health/idle-log.md`,
  4/10, *`IdleHealth` against its own 100*). They
  also follow **oil temperature** more than anything else: the middle
  band reads 105–125 on most days.

#### The variants, for the owner to choose from

1. **Keep `IdleHealth` and read it only on hot oil (≥ 92 °C)** — no
   firmware change: a rule for reading the display, written into
   `frames.md`. In that band it shows the trend above.
2. **Make it steadier.** The EWMA over 256 firings (9.7 s) lets two-minute
   windows of one stop read 56 to 109; `ROUGH_SHIFT` 10, about 40 s, would
   settle it. The level over a whole stop does not change, only its
   scatter.
3. **Add the dip count** (`tools/idledips.py` `dips_cheap()`, already the
   firmware's shape: shifts and adds, no division) as a second byte in
   0x604. It moved 4× at the hot stop where `IdleHealth` moved 2.4×, and
   "dips a minute" means something to a reader.
4. **Gate either grade on oil temperature in the firmware** — freeze it,
   or report 255, outside the hot band, so the display never shows a
   middle-band reading that compares with nothing.

**None of them is a misfire counter, and none can be.** For misfires,
VCDS 014 stays the instrument.

#### The decision: `IdleHealth` stays as it is

*Owner's decision, 4/10/2026, evening:* **nothing in the firmware
changes.** Matching 014 is not a goal worth having: the owner has often
felt an unsettled idle with 014 at zero, the ECU evidently counts little
or nothing before its adaptations settle (`docs/engine-health/refuted.md`
C19), and much else goes into it. 014 is most likely built to catch a
**real, regular misfire** and would show one plainly; what it shows at a
merely rough idle is an undocumented by-product. `IdleHealth` grades the
idle's smoothness, which is what it was built for and what the owner
feels.

The evidence behind it, all from 4/10/2026:

- **Session B** (`29`): five stops, 014 at 1.5 / 4.3 / 14.3 / 5.2 / 4.7 a
  minute; the dip count read 9.2 / 18.5 / 11.3 / 7.8 / 20.3 and
  `IdleHealth` 135 / 156 / 120 / 143 / 90. Neither follows 014.
- **The adapted stops only** (the eight where 055's learned value had
  passed about −0.93, `docs/engine-health/refuted.md` C19): rank correlation with 014 — `IdleHealth`
  −0.62, the dip count −0.05, one slow firing ≥ 6 / 8 / 12 rpm −0.50 /
  −0.29 / +0.51 (the last on two non-zero stops out of eight), second
  difference −0.38, **oil temperature +0.68**.
- **014 weighted by its size** — the sum of the counter's increments a
  minute, and its mean — over all 24 stops with a 014 log: every grade's
  correlation agrees with the count of rises to within 0.08, since the
  counter steps in twelves. With the cold stops in, every grade correlates
  *negatively* (−0.28 to −0.63): a cold idle is the roughest on engine
  speed and the one 014 does not count.
- **014 cannot be split by cylinder on this ECU**: the label file has
  group 014 and no 015 or 016.

**Considered and set aside the same day: the dip count in place of
`IdleHealth`.** Variant 3 as a replacement in byte 0, keeping the name,
with `IdleRough` (byte 1, the same grade in raw units) made reserved. It
was the sharper reading of smoothness at the hot stop, but no closer to
014 than the grade it would have replaced, and that closeness was the
reason it was wanted.

#### Next: a deliberate misfire

*Owner's proposal, 4/10/2026. **Brought forward on 9/10/2026** (owner's
decision): it is now `docs/engine-health/plan.md` step 3.5, cylinders 1 and 4
in turn on up to three days, where it also names the cylinder the dips
keep to;
this was "not before `plan.md` is empty".* A known, regular misfire, so that both instruments can be read
against something real:

- **Warm idle, oil in the hot band, loads off**; the capture running and
  VCDS on 014 (with 055 and 033 beside it).
- **A minute as it is, then one injector's connector off for a minute,
  then back on for a minute.** With the connector off that cylinder gets
  no fuel, so nothing unburnt reaches the converter (*general*). One
  cylinder of four out is a quarter of the firings — about 200 a minute at
  800 rpm.
- **The fault memory cleared afterwards** (*owner*).

**What it gives:** how 014 counts a misfire whose rate is known; what one
looks like on 0x280 — the size of the dip, whether the *one slow firing*
shape of the table above appears every second revolution; and what
`IdleHealth` reads with a cylinder dead. If the grade then wants a
different scale or anchor, that is decided from this test, not before.

**Run once, 10/10/2026** (`test/fixtures/31_step4_drive_z1.txt`, with
`vcds/vcds-step5-014-055-003.csv`; cylinders 1, 4, 4, 1 at 97 °C of oil,
each cut 47–73 s rather than a minute, the owner's call while 014 read
high). What it gave:

- **014 with one cylinder of four dead**: the field changed about 60
  times a minute, median 474–528, peaks 1,152–1,188 — against 12–96 on an
  ordinary idle. About 200 misfires a minute did not make 200 changes a
  minute, so neither its rate of change nor its size is a misfire rate.
  *Re-read 3/11 with a second cut* (`vcds/vcds-step5b-warm-014-055-003.csv`):
  in both logs the field climbs by 72 a sample (0.9 s) and starts again
  near 1,188 — a sawtooth, so the 60 changes a minute are the sample
  rate and the climb per sample is a rate: about 12 for each missing
  combustion of the dead cylinder.
- **On 0x280**: the dead cylinder's slot sits **20–23 rpm** below the
  other three, every stroke, for the whole cut (`cutscan.py --scan`).
  So a single missing combustion at idle is about a 20 rpm step — the
  size the ordinary idle dips already are.
- **The grade** (`idledips.py --roughness --windows 30`) over windows
  holding a cut: a mean step of 3.6–10.7 rpm, the 0–200 index at its
  clamp, against 1.0–2.3 rpm on the same stop with all four firing.

*This said "not yet read into a decision" until 8/11/2026*; read then:
no scale or anchor (the closing note at the end of this question).

#### Re-read in stretches, 25/10/2026

*The owner's question:* from the seat, when no jerk is felt 014 mostly
counts nothing — is there an `IdleHealth` below which 014 is silent (his
guess 45–50)? `tools/s3align.py --windows` (`--window-s 30` as well),
now with `40` and `39` paired and 014's own load field read, over
stretches of continuous standing idle rather than whole stops, oil ≥ 85 °C,
**`18` and `19` left out** (the old MAF, `docs/engine-health/refuted.md`
A11; `19` also came a day after a battery disconnect):

- **No threshold at an ordinary load.** Since the battery stayed
  connected (4/10, captures `30`–`40`), stretches below 55 still count:
  10 % of the 30 s ones silent, 36 % of samples non-zero.
- **What looked like one is the load.** Every warm stretch silent at
  `IdleHealth` 32–43 is loads on on `40`, 014's load 32–37 % against
  23–27 % ordinarily. The load alone lowers the grade and stops 014
  counting, so mixed in it reads as a threshold.
- **On fresh adaptations it did behave so** (24/9–4/10, `24`–`29`):
  Spearman rises vs `IdleHealth` **+0.69** (30 s) / **+0.91** (60 s), and
  44 % of the 55–70 stretches silent. That is the C19 state — whether 014
  counts at all follows the learned idle air — and likely where the
  owner's sense of it comes from.
- **On settled adaptations a plateau, then a knee about 80**: +0.30 /
  +0.34; 4.5–5.9 rises a minute and 36–50 % of samples non-zero anywhere
  from below 55 to 80, then 8.7 and 11 above 80 and 100.
- **The deep dips do not lead.** In the first pass of these stretches
  (*ad hoc*, not kept) the count of dips of 30 rpm and more a minute
  correlated with 014's rises at +0.04, of 20 rpm and more at +0.32,
  `IdleHealth` at +0.46: how often 014 counts follows the idle's overall
  restlessness more than its deepest dips.

So the table above's "nothing even close" was the old MAF and the cold
stops mixed in. **The decision of 4/10 stands**: on settled adaptations
`IdleHealth` below 80 says little about 014, and 014 below 80 little
about the grade.

#### Misfires — an estimate of 014 beside the grade, 4/11/2026

*The owner's request, 4/11/2026:* a number on the display that reads
**zero whenever 014 has not counted** — stricter than 014 rather than
looser, measured all the time without a settling window, and if it could,
driving too. **`IdleHealth` stays as it is**; the estimate took IdleRough's
byte and StartHealth's (`frames.md`, layout 2). Measured the same day over
every capture with a 014 log beside it (now `24`–`43`, `41`–`43` added; the
scripts were *ad hoc* and are not kept — `s3align.py` holds the pairing):

- **Per event, deeper dips are counted more often.** Of the dips at a warm
  standing idle, a 014 rise followed within 1.5 s after 17 % of those of
  10–15 rpm (a random moment: 13–17 %), 25 % of 15–20, 40 % of 20–25,
  46 % of 25–30 and 60 % of 30–40. Before a rise there was a dip of 15 rpm
  or more 74 % of the time (other samples 39 %), of 20 or more 41 % (12.5 %).
  So **most of 014's counts come with no deep dip on the bus**, and a
  detector strict enough to miss under 10 % of them fires about 70 times a
  minute and never reads zero.
- **Over the last minute it is a different story.** `dips_cheap()` with
  its frozen 20 rpm trip, counted over a sliding minute of settled idle, at
  3,431 moments: **014 had counted in the previous minute and the window
  read zero: 0 %** (at a trip of 16 and 18 also 0 %, at 22 0.4 %, at 25
  13 %, at 30 52 %); with 014 silent the window read zero 28 % of the time
  (0 % at 16, 12 % at 18, 37 % at 22). **20 is the strictest trip that still
  reads zero sometimes.** Windows of 3 s would not do: VCDS itself lags a
  dip by up to 1.5 s.
- **With the A/C on** (b7 ≥ 36 over the whole minute, warm, standing): on
  the one capture since the new MAF that has such a minute, `40` (21/10,
  120 moments), the window read **zero 79 % of the time, 0.2 dips a
  minute**, against 0.8 % and about 8 a minute with it off over every
  capture. 014 is silent with the A/C on (S3) and so, nearly, is this. On
  the old MAF (`19`, `20`, 24/9) the A/C did not calm it: 20–26 a minute.
  **014's own window is 200 crank revolutions** (about 15 s at idle, 12
  per misfire; `docs/engine-health/vcds.md`, measured 5/11), so a minute
  holds about four of its windows. **On the display, 5/11** (two short drives, the A/C switched on, *owner*): 2–10 —
  with no b7 to say whether the compressor was running
  (`docs/engine-health/open.md` S3, for context).
- **Driving: not counted.** At 1,200 rpm and more 014 rose 16 times in all
  the logs; every detector tried read tens to hundreds of dips a minute of
  noise there, and in gear the car's inertia hides a missed stroke.

**The decision** (*the owner*, 4/11/2026): **Misfires** (byte 1) = dips of
20 rpm in the last 60 s of settled idle; **MisfAvg** (byte 3) = the start's
dips per minute of idle, in tenths. An estimate, read as "zero means 014
most likely did not count"; VCDS 014 stays the instrument for misfires.

#### How it closes

When the deliberate-misfire test has been run and read: `IdleHealth`
either gets a scale or an anchor from it, or is confirmed as it is.
Until then nothing in `src/` changes for the grade itself.

**Closed 8/11/2026** (*the owner's decision*). The deliberate misfire was
run twice (10/10 and 3/11, *Run once* above): a dead cylinder puts its
slot 20–23 rpm low and drives the grade to its clamp, which is what a
grade of the idle's restlessness should do, and nothing in it asked for
a new scale or anchor. **`IdleHealth` stays as it is**; for whether 014
counts, **`Misfires` and MisfAvg stand beside it** (*Misfires*, above);
VCDS 014 stays the instrument for misfires. Nothing in `src/` changed for
the grade. *This was "open, settled for now, waiting on the deliberate
misfire being read into a decision" until then.*

---

## Never resolved but not required

**Empty since 10/11/2026**: its one question, 3, was reopened by the
maintainer and answered (*Resolved questions*). The rule of this chapter
stands for the next one put here: a question parked here is not worked
on again unless the maintainer says so, and the entry says when he did.
