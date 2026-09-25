# Decoding the powertrain CAN bus — VW PQ34, AQY engine

500 kbps bus, PQ34 platform. Every value below was verified by measurement on
the car; the logs live in `test/fixtures/`.

Two levels of confidence are distinguished:

- **Confirmed** — holds across every log and is pinned down by a test in `tools/`.
- **Open** — written down but not yet proven. The two open questions, 7 and
  10, are in `open.md`.

The questions register at the end of this file holds the rest: *Resolved
questions*, answered with the evidence kept, and **Never resolved but not
required**, never answered and **not to be worked on again**. The numbering
runs 1 to 10 across the register and `open.md` and is deliberately not
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
car. The firmware's six hardware filters do not accept it and nothing needs
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
| Oil temperature | 0x420 | 3 | × 0.75 − 48 °C | 0xFF with the engine off |
| Fuel in tank | 0x320 | 2, mask 0x7F | indicated litres | bit 0x80 = reserve lamp; the scale reads low, `refuel-reset.md` |
| Torque (indicated) | 0x280 | 7 | 1.06 Nm/bit | measured off the full-throttle plateau, see `frames.md` |
| Throttle position | 0x280 | 5 | 38 = rest position | |
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
oil on 0x420 b3 shares the formula by analogy only, and that is question 10 (`open.md`).

---

## Trap 1: the speed validity gate is not an equality

Byte 1 of frame 0x1A0 is a **bit field**, not a single value. Measured states:

| b1 | Meaning | Speed |
|---|---|---|
| 0x40 | base valid state | valid |
| 0x48 | valid, with another flag set | **valid** |
| 0x50 | valid, with another flag set | **valid** |
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

The 0x43 ramp only shows up in logs that start with the ignition being switched
on (`01_ign_only`, `06_trip_reset`). It lasts ~0.4 s and the raw value falls
464 → 0 during it. Pinned down by `test_init_ramp_only_after_ignition_on`.

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

At the end of the log the accumulator is 2314, so **IdleRough = 2314 >> 5 = 72**,
2.25 rpm, against an exact mean step of 2.117 rpm over the same 1,488 events.
The two agree to within the filter's memory of the last ten seconds, which is
what a first-order filter is.

**The index.** `IdleHealth = min(200, IdleRough × 25 >> 4)`, so 72 is
72 × 25 = 1800, >> 4 = **112**.

- **100 is measured and then rounded to a shift.** The engine before the
  repair graded 2.12 rpm on two recordings 45 °C apart (`09`, and `18` from
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
| `09_idle_60s_z1` | before the repair, oil 61 °C — **an anchor** | 1,488 | 25.1 % | 24.7 % | 21.2 % | 21.6 % | 5.9 % | 1.4 % | 0.1 % | 72 |
| `18_coldstart_z1`, 50–360 s | before the repair, the warm-up — **an anchor** | 8,375 | 25.3 % | 26.1 % | 19.9 % | 20.9 % | 6.2 % | 1.5 % | 0.0 % | — |
| `11_idle_noac_z1` | before the repair, oil 73 °C, A/C off | 573 | 34.7 % | 35.3 % | 18.0 % | 10.3 % | 1.6 % | 0.2 % | 0.0 % | 31 |
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

## What is NOT on the bus

- **Lambda** — 0x488 is constant `ff ff ff 8d ff ff ff ff` in every log.
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

**Two are open, 7 (the drag line on hot oil) and 10 (whether the oil
temperature is right), and they live in `open.md`** with what closing each
takes. The numbering is unchanged across the register because code and
documents cite it, so it is not contiguous in any one section: renumbering
would silently break every `question 7` in the tree.

The rest of the register is below: **Resolved** holds 1, 2, 4, 5, 6, 8 and 9,
kept with their evidence because a closed question that does not say how it
was closed reopens itself; **Never resolved but not required** holds 3, never
answered and not to be worked on again. The two are kept apart on purpose: the
first says what the answer is, the second says there is no answer and none is
wanted.

The engine's own faults are not in this register at all; they are
`docs/engine-health/open.md`.

---

## Resolved questions

Seven that were settled, moved out of *Open questions* so that
section holds only questions that are genuinely still open. They stay here in
full rather than being deleted: the reasoning is what stops each of them being
reopened by somebody arguing from first principles, which is the same case
`docs/firmware/refuted.md` makes for itself.

### 1. ~~What is the real period of 0x480?~~ — **closed: there isn't one**

The question was wrong, not just unanswered. **0x480 has no fixed period**, so
every attempt to pin one down was bound to produce a different number depending
on which recording it was measured from — which is exactly what happened for a
year.

Measured with adapter timestamps, stationary, engine warm
(`09_idle_60s_z1.txt` and `10_rev2600_z1.txt`):

| | 797 rpm | 2586 rpm |
|---|---|---|
| 0x480 frames/s | 26.4 | **18.0** |
| mean gap | 37.9 ms | **55.5 ms** |

Engine speed rose 3.25× and the frame rate **fell**. Whatever schedules this
frame, it is neither a fixed timer nor the injection rate — the per-injection
hypothesis was tested for exactly this reason and is refuted below. Both
recordings are irregular, on a 10 ms grid, with a long tail.

Dropped frames do not explain it: total throughput was *higher* in the revs
recording (727/s against 683/s), so the adapter was losing less, not more.

**The consequence, and it is the expensive one.** `tools/replay.py` synthesises
time for the five untimestamped fixtures by multiplying the 0x480 frame count
by an assumed 49.5 ms. That is not merely imprecise, it is **invalid**: it
applies a constant that does not exist, and its error varies with engine speed.
Every duration, average flow and distance derived from those five logs rests on
it. The fuel totals do not, because the counter is absolute — which is why the
core was built to accumulate the counter rather than integrate a flow, and that
decision has now paid for itself.

The original symptom is explained too: the specification quotes 958 µl/s for
`05_rev3000` where the data gives 1005 µl/s on the assumed period. That is a
fixed period applied to a log recorded at 2940 rpm, where the real gap is
longer than at idle. Nothing was ever wrong with the data.

**What would close it properly:** nothing needs to. The firmware runs off its
own crystal and never cared. If the five old fixtures ever need a real clock,
they need re-recording with `Z1`, not more arithmetic.

**The evidence that got there, in the order it arrived.** A 20 s
capture with `Z1` on — ignition on, engine not running — puts **every** gap
between consecutive 0x480 frames on a **10 ms grid**: 10, 20, 30, 40, 50, 60,
70 … and nothing in between. The engine ECU's other identifiers agree, all
with a modal gap of exactly 10 ms: 0x0C2, 0x280, 0x288, 0x488.

The reasoning is not sensitive to what the recording could not do. The adapter
reported `data overrun`, but **a lost frame can only merge two intervals into
one and so can only add counts at integer multiples** — it can never produce a
gap shorter than the truth. Observing gaps of 10 and 20 ms is therefore hard
evidence that the scheduler's tick is 10 ms, whatever else was dropped. And a
scheduler's tick does not change when the engine starts.

That retired 49.5 ms and 99 ms together — neither is a whole number of ticks —
and for one afternoon the answer looked like a choice between 50 and 100 ms.
It was not; the grid is real but there is no single multiple of it.

**The per-injection hypothesis, and why it was worth testing.** At warm idle
the numbers lined up almost too well: 26.4 frames/s against 26.6 injections/s
for a four-cylinder four-stroke at 797 rpm, a ratio of 0.994, and
326.1 µl/s ÷ 26.4 = 12.3 µl per frame against a modal counter step of 12–13 µl.
Three independent quantities agreeing. It would have explained why no fixed
period was ever found.

**Refuted by `10_rev2600_z1.txt`.** At 2586 rpm the injection rate is 86.2/s
and the ratio collapses to **0.209**. Had the frame been tied to injection the
ratio would have held at one. The idle agreement was a coincidence, and a
three-way one — which is worth remembering next time three numbers agree.

One observation left over, offered as an observation and not an explanation:
at idle **31 %** of 0x480 frames carry an unchanged counter (484 of 1583), at
2586 rpm almost none (3 of 355). Transmission has something to do with how
fast the counter is moving. What, is unknown, and nothing here depends on it.

**Procedure — and it does not need the converter board.** See question 9: the
USBtin has a hardware timestamp of its own, and `USBtinViewer` simply does not
use it. Talk to the adapter directly instead. That is the whole fix.

### 2. ~~The starting counter value in `07_accel`~~ — **closed**

The specification quotes 13247 → 22622 while the file starts at 12870, a
difference of 377 µl. **Confirmed exactly**: the counter reaches 13247 at
0x480 frame #23 of 290, 1.14 s into the recording, and the fuel burnt between
the first frame and that one is 377 µl to the microlitre. The specification
was computed from 1.14 s in. No discrepancy exists.

### 4. ~~Is 0x420 b3 oil or IAT?~~ — **closed: it is oil**

`07_accel` alone was inconclusive. Reading all seven fixtures in the order the
coolant says they were recorded settles it:

| Log | Coolant | 0x420 b3 |
|---|---|---|
| `06_trip_reset` (cold start) | 54.0 °C | 255, then 20.3 °C |
| `idle` | 68.25 °C | 21.0 °C |
| `07_accel` | 75.75 °C | 32.3 °C |
| `05_rev3000` | 90.0 °C | 39.0 °C |
| `02_idle_60s` | 96.75 °C | 61.5 °C |
| `03_drive` | 99.0 °C | 65.3 °C |
| `01_ign_only` (engine off) | 100.5 °C | 255 |

Three things follow, and they agree:

- **It is a warm-up curve that lags the coolant**, rising 21 → 65 °C while the
  coolant goes 68 → 99 °C. Intake air does not climb forty degrees over a
  session and stay there.
- **It is highest in `03_drive`**, the one log with air actually moving through
  the engine. An intake temperature falls when you drive; oil does not.
- ⚠ **The third argument used to be "it reads 255 with the ignition on and the
  engine off", and that is not general.** It is true of `01_ign_only` and of
  the first three frames of `06_trip_reset`, and false of the other two
  recordings taken in that state: `08_ign_only_z1` holds a steady 51.75 °C for
  its whole twenty seconds, and `18_coldstart_z1` reads 12.75 °C throughout the
  41 s before the engine fires. **255 is the fault or not-yet-available value**
  — it decodes to 143.25 °C, which `mfd15` records the display latching as an
  oil maximum — and it is not a reliable signature of the engine being stopped.
  The first two arguments do not need it.

**And it is now measured directly rather than inferred.** `18_coldstart_z1`
ends with 0x420 b3 at 17.25 °C rising 0.75 °C a minute, and a photograph of
VCDS block 006 taken 95 s later reads the intake air at **22.5 °C** against the
**18.4 °C** this channel extrapolates to. Two different numbers at one moment,
from one session, on an engine that had been running five minutes from cold.
**It is not the intake air.**

The decoding table above already called it oil temperature and the firmware
already treats it as such, so nothing changes.

⚠ **THE QUESTION AS POSED WAS BINARY, AND A THIRD ANSWER WAS NEVER TESTED.**
*"Oil or IAT?"* gets an answer about oil and IAT. **Oil *pressure* is the
obvious third reading** — this engine is said to carry an oil pressure switch
and no oil temperature sender — and it has since been tested rather than
assumed away. It is refuted three ways, all in `refuted.md` B10 and none of
them needing the decode to be right first:

- **it does not move when the engine starts.** Raw 81 before cranking, 81 at
  1439 rpm, still 81 eighty seconds later. Pressure goes zero to several bar
  in one revolution.
- **it is not zero with the engine stopped** — steady 81 for the 41 s before
  the engine fires, steady 133 through all of `08_ign_only_z1`.
- **it ratchets rather than tracking.** 161 → 167 across holds at 1492 to
  2892 rpm, one count per 25 s hold, never falling back between holds where
  the revs did. Pressure over that range roughly doubles and is reversible.

**Nor is it a figure computed from the coolant**, which is what a car with no
sender might otherwise broadcast: in `15_rev2372_z1` the coolant fell five
counts while this channel rose two, and a value derived from the coolant
cannot move against it.

So it is a real thermal quantity with mass, responding to load rather than to
engine speed, and measured by a sensor rather than computed. The signal
behaves as oil temperature and the firmware's treatment of it stands.

**IT IS A SENSOR AND NOT A COMPUTED NUMBER — measured, and it closes the one
part of this that was still open.** A value the ECU or the cluster *models*
from coolant, load and time would climb smoothly while the engine heats. This
one does not: across every fixture the byte takes **85 steps up and 58 steps
down, and every single step is exactly ±1 count** (one +4 aside, across a gap
in a log). During the `18_coldstart_z1` warm-up alone it steps *down* twelve
times while unambiguously heating, and in `15_rev2372_z1` it wobbles 6 up and
5 down through a 25 s hold at constant speed on a fully warm engine.

**That is one-LSB dither around a slowly moving true value, which is what an
analogue sensor and its converter do and what arithmetic does not.** No model
built to be sluggish enough to match a sump's thermal mass would also be built
to rattle by a count in both directions while its inputs move one way.

**It also fits the frame it arrives on.** `0x420` b1 and b2 are ambient
temperature — zero here, though the car does display an outside temperature by
some other route (`refuted.md` B11) — and ambient
air is a signal the *cluster* displays and the engine management has no use
for. So `0x420` looks like a frame of cluster-side temperature channels, which
is where a sump sender's signal would end up.

**What supplies it — looked up, and marked as looked up.** ⚠ **The sources
below are parts catalogues, workshop pages and forums, which is NOT how this
document settles facts about the car.** They are recorded because they are
consistent, because they name a mechanism, and because the mechanism has a
consequence for question 10 (`open.md`). They are an indication. The measurement that
settles it is still to unplug the connector and watch for 255.

- The part is the **oil level and oil temperature sender G266**, threaded into
  the **sump** from below, three wires, fitted across the Golf/Bora range of
  this era.
- **Its signal goes to the instrument cluster, not to the engine ECU** — a PWM
  level-and-temperature line to J285, which is what displays the oil
  temperature.

**That resolves the objection that raised all this.** "This engine has no oil
temperature sensor" is very likely right *as a statement about the engine*:
the sender belongs to the sump and the dashboard, not to the engine
management, and an engine-side parts list has no reason to carry it. It is
also exactly why `01-Motor` has no oil temperature block — **not because
nobody looked, but because the signal never reaches that ECU.** The question
of whether this particular car has it fitted is answered by the car: a number
is on the bus and it behaves thermally, so something produces it.

⚠ **AND IT UNDERMINES THE DECODE, WHICH IS THE PART THAT MATTERS.** If the oil
byte is the cluster's and the coolant byte on 0x288 is the ECU's, then they
are **two different modules choosing two different scalings**, and this
firmware took the second and applied it to the first. The formula
`× 0.75 − 48` was already flagged here as an argument from analogy; the
analogy now turns out to be between modules that had no reason to agree.
Question 10's cold-soak arithmetic and this point are independent of each
other and say the same thing.

⚠ **What this does not establish is that the number is *right*** — only what it
is a number of. That is question 10 (`open.md`). **If there is no physical sender the
answer there gets simpler, not harder**: "the sensor is faulty" leaves the
table and what remains is this firmware's decode, which the cold-soak
calibration point already says has the wrong slope.

### 5. ~~AccelG — longitudinal or lateral?~~ — **closed: it is lateral**

> **The firmware does not decode this and no longer accepts 0x5A0 at all.** The
> display reads the frame straight off the bus, so a decoded field here would
> have had no consumer; it was removed along with its acceptance
> filter. This entry stands as a fact about the car, which is what this document
> is for.

**Measured in the car**, on the MFD15 reading 0x5A0 straight off the bus with
no converter in the loop. Full lock, several laps at 15–20 km/h:

| Test | Reading |
|---|---|
| Circling **left**, full lock | **+0.2 to +0.5 G**, steady, rising with speed |
| Circling **right**, full lock | the same magnitudes, **negative** |
| Pulling away and braking | small by comparison, a few hundredths |

Three things settle it, and they are independent of each other:

- **The sign inverts with the direction of the turn.** Neither a standing bias
  nor the camber of the road does that. Only a quantity that has a direction in
  a corner does.
- **The magnitude tracks cornering force**, which a longitudinal axis knows
  nothing about.
- **Braking is the small number.** On a longitudinal sensor it would be the
  largest reading available.

**The scale came out of the same test, which was not the point of it.** A
Beetle turns in about 10.9 m, so full lock is a radius of roughly 5.5 m, and
v²/r gives 0.20 G at 12 km/h, 0.32 at 15 and 0.51 at 19 — the measured range,
in the speeds a yard allows. So `(raw − 127)/100 = G` is right in magnitude and
not merely in shape; a wrong scale would have produced plausible-looking
numbers of the wrong size.

**Positive is a left turn**, which is consistent with ISO 8855 vehicle axes
(y points left, and the centripetal acceleration of a left-hand corner points
left). Nothing needs inverting anywhere.

The few hundredths seen under braking are road camber, a little steering off
centre and imperfect sensor alignment. They are an order of magnitude down and
they do not sign-reverse, so they change nothing.

What the fixtures had already settled, and what still stands: standing still
with the engine running (`02_idle_60s`) the byte reads 127–128, i.e. **0.00 G**,
confirming the 127 offset and that the axis is horizontal.

**Why the fixtures could never have closed this.** Correlating the byte against
the derivative of road speed gives r = +0.05 on `07_accel` and r = +0.25 on
`03_drive`, with a slope of 0.29 where a clean longitudinal sensor would give
1.0 — inconclusive, and now explained: there is no longitudinal component to
find. Both logs were also recorded crawling across an uneven lawn, where the
tilt of the car under each wheel swamps an acceleration of 0.04 G.

**The procedure that closed it, kept because it generalises.** Two tests on
flat ground, neither needing the converter board: the display reads 0x5A0 b0
straight off the bus (`mfd15/tri/S-AQY.TRI` line 13), so this wants the MFD15
and nothing else. Each test moves exactly one axis, so the question is only
whether the number moved. The first one is what was run.

- **A steady circle.** Full lock, constant 15–20 km/h, several laps, no
  braking or accelerating. A **lateral** sensor settles at **0.30–0.50 G** and
  holds it for as long as the wheel is turned; a longitudinal one stays at
  0.00. Then circle the other way: on a lateral sensor the sign inverts, which
  is what separates a real response from the permanent bias `sensors.md` #12
  suspects. Do this one first — a steady reading is far easier to take off a
  display than a peak.
- **Firm braking**, straight line, 40 km/h to a stop. A **longitudinal**
  sensor dips to **−0.30 to −0.60 G**; a lateral one does not move. Harder to
  read, because the peak lasts about two seconds.

Both are around 0.3 G, i.e. **thirty times the 0.01 G resolution**, so "it did
not move" is a result and not a sensitivity problem.

**Parking across a slope also works in principle and is not worth doing.** A
stationary accelerometer reads the component of gravity along its axis, so the
deflection is sin(tilt): a 6 % driveway is 3.4° and gives **0.06 G**, six counts
against a one-count resolution. It needs a genuine hill — 20 % for 0.20 G — to
beat the two tests above, and it was the first thing suggested here for a year
on the strength of needing no driving. It needs terrain instead, which is
harder to come by.

The earlier suggestion to *accelerate* in second gear and correlate against
speed is superseded: braking is the same axis at twice the magnitude and needs
no correlation, just a glance at the display.

The channel is transmitted to the display and used for nothing else, so a wrong
label costs a wrong caption.

### 6. ~~Source of the trip reset — candidate 0x5D8 b0~~ — **candidate eliminated, question retired**

`06_trip_reset.txt` was recorded for this and had never been analysed. It has
been now, and the candidate is dead: **all eight bytes of 0x5D8 are constant
for the entire 135 s recording** — `21 05 00 00 00 00 00 00`, not one bit
moves. 0x5D0 is constant too. Sweeping every byte of all fourteen broadcast
identifiers for anything that grows and then falls turns up only the fuel
counter itself and the oil temperature climbing as the engine warms.

**One honest caveat.** The recording covers 124.6 m. A trip odometer in units
of 0.1 km would tick exactly once across it, and a single increment is not
something a scan can distinguish from noise. So this eliminates the specific
candidate and does not prove the trip odometer is absent from the bus.

**It no longer matters, which is why the question is retired rather than
open.** The average is reset on refuelling instead (`refuel-reset.md`), which
needs no sniff, no licence and no byte. If somebody ever wants the cluster's
trip reset as a *second* trigger, the procedure is a fifteen-minute drive with
the USBtin running, at least 3 km so a 0.1 km counter moves thirty times, with
the reset pressed in the middle — and then the same scan, which is now written
down and took a minute to run.

### 8. ~~The torque byte's scale~~ — **closed: 1.06 Nm/bit, measured off the full-throttle plateau**

**Moved here from *Never resolved but not required*.** It was parked there
because no measurement existed, and the parking said so; then a held
full-throttle pull in 4th produced one.

**The evidence**, `19_postfix_drive_z1`, median b7 in a ±150 rpm window, with
the drag line held in bytes (`drag_b7 = 9.11 + 0.006514 × rpm`):

```
170 Nm @ 2400:   b7 185,  s = 170   / (185 - 24.74) = 1.061 Nm/bit
 85 kW @ 5200:   b7 191,  s = 156.1 / (191 - 42.98) = 1.055 Nm/bit
```

**Two independent ratings against two independent readings, 0.6 % apart.**
`TORQUE_CNM_PER_BIT` is 106, a decision inside that bracket, and the drag
constants follow it from the byte line. The plateau rises from 175 at
2000 rpm to 198 at 4500 and falls back to 175 at 6000 with the pedal on the
floor, and relative load (group 014) is flat at 78–81 % across it — so this is
where the engine runs out of air, not where a burst happened to end.

**What it refuted.** Everything below rested on *b7 = 255 is the rated crank
torque plus the drag*. The plateau is 185–206 and 255 is never reached, so the
old derivation had nailed both ratings to a value the engine cannot produce,
and the shipped 0.74 read **30 % low**. The 0.90–0.96 bracket `frames.md` had
derived from the air was nearer, and low for an arithmetic reason: it divided
a drag figure already converted to Nm at 0.74, when the drag scales with the
scale.

⚠ **Two caveats, stated rather than resolved.** The intake temperature was not
logged, and b7 carries the charge normalisation, so a hot day reads lower and a
frosty one higher. And the engine was not wholly well — every fault was a
low-load one, no misfire was counted during any pull, and load and air matched
the earlier drive. The scale was set on that judgement. **Neither is a reason
to reach for `TORQUE_TRIM_PCT`.**

**What follows is the entry as it stood while parked**, kept because the
premise it argues from is the obvious one and is wrong.


**Why it was parked, and it was the harder of the two calls.** Unlike b5, this
one *does* touch what the firmware transmits: the scale multiplies every torque
and power figure on the display. It was parked anyway, because at the time
there was nothing left to run.

- The bracket is narrow, and got narrower. On the warm drag line the two
  factory ratings imply **0.736 to 0.738 Nm/bit** — 0.3 % — where the old
  cold-oil line made them argue between 0.745 and 0.773. The scale in the
  firmware moved 0.75 → 0.74 with the refit, which is not a new
  answer to this question but the arithmetic consequence of question 7's (`open.md`), since
  full scale must cover the rated torque plus the drag.
- The measurement does not exist. VCDS was tried and this ECU has no torque
  block. A full-throttle pull has since happened — see the note below — and it
  did not settle it either.
- Nothing degrades while it stays undecided. A decision is in the code, the
  reasoning is written down in `frames.md` and `config.h`, and two tests in
  `test_compute.c` pin the ceiling so a future edit cannot quietly put the
  factory figures out of reach again.

An open question implies work that would close it. There is none, so calling
this open was misleading.

The findings, in full:

**This ECU does not report torque in
Nm.** Measuring groups 001, 002, 003 and 020 were all examined on
`06A 906 018 EJ` and the closest thing on offer is `Motor zatizeni` — engine
load, in per cent. Writing that down is the point: without it the next person
plans exactly this session again.

The trip was not wasted, because b7 was measured against that load and **is not
the same quantity**. Holds `14`, `15` and `16` sit at a constant 17.0–17.3 %
load while b7 climbs 20.7 → 26.3 → 27.2. A load percentage does not rise with
engine speed at constant load; a torque does, because the friction and pumping
torque a free-revving engine must produce grows with speed. That is independent
support for the reading that b7 is *indicated torque*, arrived at
from a different direction than the argument that produced it.

So the scale remains a decision inside the bracket the factory ratings imply —
0.74 Nm/bit since the drag refit, 0.75 before it.

#### ⚠ New evidence, and the question stayed parked anyway

**The full-throttle pull this section said would settle it has happened**, on a
public road, logged on the ECU's own measuring blocks. It did not settle it,
and the reason is worth keeping.

- **b7 did not clip.** The display peaked at 117 Nm and 58 kW, which is b7
  around 199 of 255, at engine speeds past 5700 rpm with the pedal on the
  floor. So the remap has not pushed b7 into the ceiling, which was one of the
  two ways `frames.md` said a remap could fail.
- **But the airflow of that same pull implies more torque than the display
  showed** — enough that either the engine is burning badly or the scale
  under-reads, and the measurement supports both. `frames.md`, *What that
  gap is worth in Nm*, has the numbers and the argument.
- **The car is chipped**, which makes the derivation worse in a known
  direction: the bracket comes from *stock* ratings and this engine is not
  stock.

**None of that is a reason to re-plan the cancelled VCDS session.** There is
still no torque block on this ECU and there never will be. What is new is a
different route to the same number — torque inferred from measured air and
measured fuel — which needs no block and no dynamometer, and which
`frames.md` sets out. **Until that capture exists this stays parked**,
and it stays here rather than moving to the open register, because there is
still no work owed: the decision in the code is defensible, and the engine has
to be repaired before any measurement of it means anything.

⚠ **A second finding came out of this session and it is more expensive than the
question was** — the drag torque was fitted on cold oil. That is question 7 (`open.md`),
and it is the one question still open.

---

The original procedure follows, for the record.

0x280 b7 is a percentage of a reference torque inside the ECU, not Nm. The two
factory ratings bracket the scale between 0.745 Nm/bit (85 kW at 5200 rpm) and
0.773 (170 Nm at 2400 rpm); 0.75 was chosen inside that bracket,
and the reasoning — including why the old 0.67 was wrong — is in `frames.md`
and in `config.h`.

**Procedure.** VCDS, engine electronics, a measuring block reporting engine
torque — group 001 or 002 on ME7, depending on the version — logged alongside
0x280 with the USBtin. Warm idle, then three or four steady throttle openings
held for ten seconds each, in neutral so the load is repeatable. Plot the
block's Nm against b7: the slope is the scale and the intercept should be
zero. Four points across the range are plenty, because the only question is a
straight line through the origin.

Full throttle would settle it too and is deliberately not planned. Until then
the display is right in shape and to roughly ±5 % in magnitude, and two tests
in `test_compute.c` guard the ceiling so a wrong scale can no longer put the
factory figures out of reach unnoticed.

### 9. ~~Two fixtures carry timestamps and disagree with the other five about time~~ — **closed: the timestamps are wrong**

**Measured, at the operating point the argument was about.**
`09_idle_60s_z1.txt`: 60 s of warm idle at 796 rpm, air conditioning off,
recorded with the adapter's own timestamps.

```
19,561 ul over 60.027 s  =  325.9 ul/s  =  1.17 l/h
```

Nothing in that is derived. The counter is absolute in microlitres and the
clock is stamped in the USBtin when the frame arrives, so no period is assumed
and no host scheduler is involved.

| base | idle flow | verdict |
|---|---|---|
| assumed 49.5 ms period | 310 µl/s = 1.12 l/h | within 5 % |
| USBtinViewer timestamps | 157 µl/s = 0.57 l/h | **out by a factor of 2.1** |

So the recorded timestamps lose, exactly as the tool's own documentation said
they would, and the physical-plausibility argument below was right: a warm 2.0
8V does not idle at 0.57 l/h.

**What this changes.** `06_trip_reset.txt` and `07_accel.txt` have a wrong time
base, so their durations, average flows and distances — the 135.0 s, the 15.9 s,
the 613 µl/s, the 124.6 m, the 27.3 m — are overstated by roughly two. Their
fuel totals stand. The five untimestamped logs are no better off, but for the
different reason in question 1: the period they are reconstructed from does not
exist.

**Three fixtures with adapter timestamps now exist** — `08`, `09`, `10` — and
they are the only logs here whose time can be trusted. See
`test/fixtures/README.md`.

---

The original write-up follows, because the diagnosis is the useful part and it
was right. Found while reviewing question 1, and it had gone unnoticed since
the fixtures were recorded.

**All seven were recorded with USBtinViewer**, but saved two different ways:
five as the raw serial lines, with no time information at all, and two —
`06_trip_reset.txt` and `07_accel.txt` — as the viewer's table, which carries a
**millisecond timestamp on every line**. Why the two differ is not recorded and
is most likely a setting that got changed at some point; it does not matter,
because neither is the timestamp we want (see below).

What nobody had noticed is the consequence. `tools/replay.py` uses the
timestamps where they exist and synthesises time from the assumed 49.5 ms 0x480
period where they do not, so **two of the seven logs are measured on a
different clock from the other five** — and the two clocks do not agree.

The two clocks do not agree. Taking the 120 s of warm idle inside
`06_trip_reset` — engine running, stationary — and dividing the fuel the
counter accumulated by the elapsed time its own timestamps report:

```
18,810 ul over 119.6 s  =  157 ul/s  =  0.57 l/h     recorded timestamps
                           310 ul/s  =  1.12 l/h     assumed 49.5 ms period
```

**A warm 2.0 8V does not idle at 0.57 l/h.** 1.1 l/h is what an engine of this
size burns standing still, and 0.57 is not a number it can produce. On that
alone the assumed period wins and the recorded timestamps are wrong.

Except that each base has independent corroboration, which is why this is an
open question rather than a finding:

| | For | Against |
|---|---|---|
| **Assumed 49.5 ms** | gives `02_idle_60s` a duration of 60.1 s, which is its file name, and exactly the 310 µl/s the specification quotes; gives a credible idle | gives `05_rev3000` 1005 µl/s where the specification says 958 (question 1) |
| **Recorded timestamps** | gives `06_trip_reset` a distance of 124.6 m, matching the "drive at least 0.1 km" step of the recording checklist | gives an idle flow no engine of this size produces |

**The tool's own documentation settles which one to distrust.** USBtinViewer
says of itself: *"the timestamp is generated in the application on the host,
the hardware timestamping is currently not used"*
([EmbedME/USBtinViewer](https://github.com/EmbedME/USBtinViewer)). So the times
in those two logs are not arrival times at all — they are the times at which a
Java GUI got round to the line, and it was handling **around 700 lines a
second** while doing it.

Everything else the recordings say agrees with that. Between 39 % and 51 % of
all lines are an immediate duplicate of the line before, and per-identifier
gaps cluster on multiples of about 15.6 ms — the Windows timer tick, i.e.
batching. On top of that the recorder is *missing* frames: at warm idle the
counter steps cluster at 14–16 µl with clear harmonics at 28–31 and 44, one,
two and three periods' worth.

That is the diagnosis half of this question closed. What is still open is the
number: which period, and therefore which of the two flows, is right.

That modal step is worth one line of arithmetic, because it is the one solid
number here: **one 0x480 carries about 15 µl at warm idle.** That pins
`flow × period ≈ 15 µl` and nothing more — 310 µl/s at 49.5 ms and 157 µl/s at
99 ms both satisfy it. It is the physical plausibility of the flow, not the
data, that chooses.

**What is and is not affected.**

- **Fuel totals are untouched.** The counter is absolute and in microlitres, so
  every total in the table above, every figure the C core and the Python
  reference agree on, and every accumulator test stands whatever the clock did.
  This is exactly why the core accumulates the counter rather than integrating
  a flow.
- **Everything per-second is suspect on two logs.** Duration, average flow and
  distance for `06_trip_reset` and `07_accel` — the 15.9 s, the 613 µl/s, the
  27.3 m — rest on timestamps that may be twice too long. The figures for the
  other five rest on an assumed period instead, which is a different way of
  being unverified.
- **The firmware does not care either way.** On the car it uses its own
  crystal-derived millisecond clock. This is a question about the fixtures and
  about what the tests are asserting, not about the device.

**Procedure — no board, no firmware, one sixty-second recording.** This was
written as needing the converter in `CAN_MODE=LISTEN_ONLY`, on the reasoning
that only the device could timestamp a frame when it arrived. That was wrong:
**the USBtin does it in hardware, and only the viewer does not use it.** Drive
the adapter over its serial port directly — the commands are on
[fischl.de/usbtin](https://www.fischl.de/usbtin/):

| | |
|---|---|
| `S6` | 500 kbit/s |
| `Z1` | **timestamping on** — this is the whole point |
| `L` | open **listen-only**. Silent on the bus by the adapter's own guarantee, exactly like the firmware's Listen Only |
| `O` | (open normally — *not* this one) |
| `F` | read the status flags afterwards — they say whether frames were dropped |

**`tools/usbtin_capture.py` does exactly this** and writes the raw slcan
stream, which `canlog.py` already parses including the four hex digits `Z1`
appends. It has been run on a desk with no adapter
attached, so its argument handling works and its serial conversation has never
met a USBtin.

**The acceptance filter was deliberately dropped from this procedure.** It used
to read `m00000000` / `MFFFFFFFF`, "set to pass 0x480 only". Which polarity of
the mask means *don't care* is not stated in any document we hold, and the two
conventions in circulation are opposites — under one of them that pair passes
everything, under the other it passes nothing. A capture that silently records
zero frames is indistinguishable from a dead bus, and this is a trip to the
car. Record the whole bus and filter afterwards with `canlog.py --id 0x480`;
the throughput is affordable and `F` reports it if it is not.
| `C` | close |

Engine at warm idle, sixty seconds, capture the raw lines to a file.
`tools/canlog.py` parses the timestamp.

Filtering to 0x480 alone is not an optimisation, it is part of the fix: it
takes the line rate from about 700 a second to about 20, so the duplication and
the dropped frames that spoiled the fixtures cannot happen.

Then:

1. `frames / elapsed` is the period, from the adapter's clock.
2. `(counter_end − counter_start) / elapsed` is the idle flow in µl/s, with no
   assumption in it anywhere.
3. Compare against 49.5 ms and 310 µl/s. If they hold, `replay.py` should stop
   preferring the viewer's timestamps and the documented figures for two logs
   need correcting. If they do not, five logs need correcting instead.

**One thing to check in the first minute rather than assume:** the timestamp is
four hex digits of milliseconds and USBtin's documentation does not say what it
wraps at. Read the wrap out of the data — it costs one minute and settles it
permanently.

Until then: **trust the totals, distrust every duration.** Nothing has been
changed in the fixtures, the tests or `replay.py` on the strength of this,
because changing seven logs' worth of documented numbers on an argument about
what an engine plausibly burns is exactly the sort of thing that should wait
for the sixty seconds of measurement that settles it.

---

## Never resolved but not required

One question in this file was never answered, and it is not going to be.
**Do not come back to it.** Not "while the car is on the ramp anyway", not "it
is only ten minutes with VCDS running". It has already cost a trip to the car,
came back with less than was hoped, and blocks not a single line of firmware.
(Question 8 used to sit here too; a measurement arrived and it moved to
*Resolved*, which is how this chapter is supposed to be left.)

They are kept in full rather than deleted for the same reason `docs/firmware/refuted.md`
exists: a question that leaves no trace gets asked again by the next person, who
then repeats the session that did not answer it. The difference between that
file and this chapter is that `refuted.md` holds ideas that were settled
*against*, while these were never settled at all.

**What would reopen one.** The maintainer saying so — this chapter is a
decision about where to spend effort, not a discovery about the bus, and a
decision can be changed the same way it was made. If that happens, write it
inside the entry rather than quietly starting work, so the next reader can see
which rule is in force.

---

### 3. 0x288 b5 and b6 — **b6 decoded, b5 unexplained, parked**

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

The findings, in full:

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

---

The original write-up follows.

**Procedure.** VCDS, engine electronics (address 01), measuring blocks. Group
003 carries mass air flow and load; group 020 or 021 carries ignition advance;
injection time is in group 002 or 004 depending on the ECU version. Log 0x288
with the USBtin at the same time, at warm idle and at a couple of steady
throttle openings, and regress each byte against each block value. Two bytes,
three candidates, three or four operating points is enough to tell them apart.

Nothing in the firmware wants these bytes. This is curiosity with a use — an
air mass would let a proper torque model replace the two-point drag line — but
it blocks nothing.
