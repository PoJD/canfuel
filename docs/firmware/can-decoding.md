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

Seven that were settled, each with its answer and the evidence that closed it
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

### 4. ~~Is 0x420 b3 oil or IAT?~~ — **closed: it is oil, from a real sensor**

Ordered by coolant, the fixtures give a warm-up curve that lags it — 21 → 65 °C
while the coolant goes 68 → 99 °C — highest in the one log with air moving
through the engine, where an intake temperature would fall:

| Log | Coolant | 0x420 b3 |
|---|---|---|
| `06_trip_reset` (cold start) | 54.0 °C | 255, then 20.3 °C |
| `idle` | 68.25 °C | 21.0 °C |
| `07_accel` | 75.75 °C | 32.3 °C |
| `05_rev3000` | 90.0 °C | 39.0 °C |
| `02_idle_60s` | 96.75 °C | 61.5 °C |
| `03_drive` | 99.0 °C | 65.3 °C |

**Measured directly as well**: at the end of `18_coldstart_z1` this channel
extrapolates to 18.4 °C where VCDS block 006 read the intake at **22.5 °C**.

**Not oil pressure** (`refuted.md` B10): it does not move when the engine
starts, is not zero with it stopped, and ratchets one count per hold rather
than tracking engine speed. **Not computed from the coolant**: in `15` the
coolant fell five counts while this rose two.

**A sensor, not a model**: across every fixture the byte takes 85 steps up and
58 down, every one exactly ±1 count, and dithers both ways through a steady
hold — what an analogue sensor does and arithmetic does not.

**255 is the fault / not-yet-available value** (it decodes to 143.25 °C, which
the display latches as an oil maximum), not a signature of a stopped engine:
`08_ign_only_z1` and the 41 s before `18` fires both read a real temperature.

**What supplies it — looked up, not measured.** Parts catalogues, workshop
pages and forums name the **oil level and temperature sender G266** in the
sump, wired to the instrument cluster, not the engine ECU — which is why
`01-Motor` has no oil temperature block. ⚠ That makes the oil byte the
cluster's and the coolant byte the ECU's: **two modules with no reason to
share a scaling**, and this firmware borrowed the coolant's `× 0.75 − 48`.
Whether the number is *right* is question 10 in `open.md`.

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

---

## Never resolved but not required

One question in this file was never answered, and it is not going to be.
**Do not come back to it.** Not "while the car is on the ramp anyway", not "it
is only ten minutes with VCDS running". It has already cost a trip to the car,
came back with less than was hoped, and blocks not a single line of firmware.
(Question 8 used to sit here too; a measurement arrived and it moved to
*Resolved*, which is how this chapter is supposed to be left.)

It is kept rather than deleted for the same reason `docs/firmware/refuted.md`
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
