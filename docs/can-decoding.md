# Decoding the powertrain CAN bus — VW New Beetle, AQY engine

500 kbps bus, PQ34 platform. Every value below was verified by measurement on
the car; the logs live in `test/fixtures/`.

Two levels of confidence are distinguished:

- **Confirmed** — holds across every log and is pinned down by a test in `tools/`.
- **Open** — written down but not yet proven. See the end of this file.

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

**Free for the converter:** 0x600–0x602 appear in none of the logs
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
| Fuel in tank | 0x320 | 2, mask 0x7F | litres | bit 0x80 = reserve lamp |
| Torque (indicated) | 0x280 | 7 | 0.75 Nm/bit | a decision, see `frames.md` |
| Throttle position | 0x280 | 5 | 38 = rest position | |
| Engine load | 0x280 | 6 | | 0 with the engine off |
| Wheel speeds | 0x4A0 | 4× 16-bit LE | (raw >> 1) × 0.01 km/h | bit 0 = direction |
| Acceleration | 0x5A0 | 0 | (val − 127) / 100 G | |
| Doors | 0x320 | 0 | bit mask | |

DLC is constant per ID: 0x050 carries 4 bytes, 0x5D0 carries 6, everything
else 8. A parser that assumes a fixed length of 8 would break on 0x050 and 0x5D0.

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

It makes no difference to the arithmetic — the 0x7FFF mask drops it. It is
usable as a "this ignition cycle is still young" flag.

## Trap 4: FuelAvg divides by an almost-zero distance

The average fuel consumption is a ratio of accumulators. Right after starting,
distance is nearly zero and the ratio runs away — on `06_trip_reset.txt` it
produced **21,395 l/100 km** before the car had moved. Below 100 m of distance
it must return zero.

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
- **Ambient temperature** — 0x420 b1 and b2 are both zero; the car has no sensor.
- **Trip odometer and trip reset** — see open questions.

---

## Open questions

Reviewed in full on 2026-08-11. Three were closed by going back to the
fixtures, which nobody had done since they were written down; one candidate was
eliminated; one new question came out of the review and it is the most
important thing on this page. What remains open carries the procedure that
would close it, because a question without one is a wish.

Two of them — 3 and 8 — want the same VCDS session and should be done together.

---

### 1. ~~What is the real period of 0x480?~~ — **closed 2026-08-11: there isn't one**

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

### 2. ~~The starting counter value in `07_accel`~~ — **closed 2026-08-11**

The specification quotes 13247 → 22622 while the file starts at 12870, a
difference of 377 µl. **Confirmed exactly**: the counter reaches 13247 at
0x480 frame #23 of 290, 1.14 s into the recording, and the fuel burnt between
the first frame and that one is 377 µl to the microlitre. The specification
was computed from 1.14 s in. No discrepancy exists.

### 3. 0x288 b5 and b6 — **b6 closed 2026-08-11, b5 narrowed**

The session happened. `docs/vcds-session.md` is the procedure,
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

**Why this stays open.** Only two distinct advance levels exist below the
ceiling — idle and 1536 rpm — so the fit rests on two clusters, not on a
spread. And 152 is an odd place to clip: not 255, not a power of two.

**What would close it:** the same two loggers running **during a drive**.
Under load the advance varies at constant engine speed, which is exactly the
axis a stationary sweep in neutral cannot produce — every point above idle here
was free-revving at the same throttle opening. A ten-minute drive gives more
distinct advance values than an hour of holding revs in a driveway.

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

### 4. ~~Is 0x420 b3 oil or IAT?~~ — **closed 2026-08-11: it is oil**

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
- **It reads 255 with the ignition on and the engine off** (`01_ign_only`, and
  the first seconds of `06_trip_reset` before the engine fires). An intake air
  sensor is a thermistor the ECU can read whenever it is awake, and it would
  give a number. A quantity that only exists once the engine is running behaves
  exactly like this.

The decoding table above already called it oil temperature and the firmware
already treats it as such, so nothing changes; it is now a finding rather than
an assumption. VCDS group 003 would confirm it in one minute if anyone cares
enough, and nobody should.

### 5. ~~AccelG — longitudinal or lateral?~~ — **closed 2026-08-11: it is lateral**

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

### 7. Drag torque calibration — **reopened 2026-08-11: it was fitted on cold oil**

Closed in phase 1 as `drag [Nm] = 19.52 + 0.00028 × rpm`, reproducing 21.75 Nm
at 797 rpm and 27.75 Nm at 2940 rpm exactly — raw b7 of 29 and 37. Both points
came from fixtures. **Neither was at operating temperature.**

| | fixture | b7 | oil (0x420 b3) | 2026-08-11 | b7 | oil |
|---|---|---|---|---|---|---|
| idle | `02_idle_60s` | 29 | **60.8 °C** | `11_idle_noac_z1` | 25 | 72.8 °C |
| ~2930 rpm | `05_rev3000` | 37 | **39.0 °C** | `16_rev2926_z1` | 27 | 77.2 °C |

**Ten counts at 2930 rpm is 7.5 Nm at the current scale**, and the gap is four
counts at idle against ten at high speed — which is the signature of viscous
friction, not of a measurement error. Viscosity falls steeply with oil
temperature and viscous drag rises with speed, so a cold-oil point overstates
drag most exactly where the fit is most sensitive to it.

`05_rev3000` was recorded with the **oil at 39 °C**. That is barely warm.

**What it costs.** The firmware subtracts this line from indicated torque, so
an overstated drag **understates the torque and the power on the display**, and
by more at high revs — the part of the range a driver actually looks at.

**Why this is not simply refitted today.** The five new points are at 72–77 °C
oil, better but still short of the 95–110 °C of real driving, and the idle
point does not belong on the same line as the others: b7 is 25.0 at 798 rpm and
18.8 at 1536, which is not monotonic. Idle is a *controlled* state — the ECU
holds the speed against accessory load and keeps a torque reserve — while the
points above are a free-revving engine against its own friction. They are two
different quantities and a straight line through both was always going to
mislead.

**What would close it properly:** the rpm sweep repeated after a drive, with
the oil genuinely hot, and the idle point either excluded or fitted separately.
That is phase 6 work and it now has a procedure and a reason.

### 8. The torque byte's scale — **still open; the VCDS session could not close it**

**The session was done on 2026-08-11 and this ECU does not report torque in
Nm.** Measuring groups 001, 002, 003 and 020 were all examined on
`06A 906 018 EJ` and the closest thing on offer is `Motor zatizeni` — engine
load, in per cent. Writing that down is the point: without it the next person
plans exactly this session again.

The trip was not wasted, because b7 was measured against that load and **is not
the same quantity**. Holds `14`, `15` and `16` sit at a constant 17.0–17.3 %
load while b7 climbs 20.7 → 26.3 → 27.2. A load percentage does not rise with
engine speed at constant load; a torque does, because the friction and pumping
torque a free-revving engine must produce grows with speed. That is independent
support for the 2026-08-11 reading that b7 is *indicated torque*, arrived at
from a different direction than the argument that produced it.

So 0.75 Nm/bit remains a decision inside the bracket the factory ratings imply.
What is left that would settle it: a full-throttle pull, which is deliberately
not planned, or a factory document nobody has.

⚠ **A second finding came out of this and it is more expensive than the
question was** — see the drag-torque note below.

---

The original procedure follows, for the record.

0x280 b7 is a percentage of a reference torque inside the ECU, not Nm. The two
factory ratings bracket the scale between 0.745 Nm/bit (85 kW at 5200 rpm) and
0.773 (170 Nm at 2400 rpm); 0.75 was chosen inside that bracket on 2026-08-11,
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

Do it in the same session as question 3 — that one wants measuring blocks too,
and the same log of 0x280 and 0x288 serves both.

### 9. ~~Two fixtures carry timestamps and disagree with the other five about time~~ — **closed 2026-08-11: the timestamps are wrong**

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
appends. Written 2026-08-11; it has been run on a desk with no adapter
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
`tools/canlog.py` parses the timestamp since 2026-08-11.

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
