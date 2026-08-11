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

### 1. What is the real period of 0x480? **Open, and question 9 makes it worse**

The specification quotes 958 µl/s for `05_rev3000`; the data gives 1005 µl/s
on the assumed 49.5 ms period, and 51.9 ms would produce exactly 958. Five
per cent.

That was the whole question until question 9 below, which found that the two
timestamped fixtures imply a fuel flow roughly *half* what the assumed period
gives. Whatever settles one settles the other, so do question 9 first and this
becomes arithmetic.

**Procedure — and it does not need the converter board.** See question 9: the
USBtin has a hardware timestamp of its own, and `USBtinViewer` simply does not
use it. Talk to the adapter directly instead. That is the whole fix.

### 2. ~~The starting counter value in `07_accel`~~ — **closed 2026-08-11**

The specification quotes 13247 → 22622 while the file starts at 12870, a
difference of 377 µl. **Confirmed exactly**: the counter reaches 13247 at
0x480 frame #23 of 290, 1.14 s into the recording, and the fuel burnt between
the first frame and that one is 377 µl to the microlitre. The specification
was computed from 1.14 s in. No discrepancy exists.

### 3. 0x288 b5 and b6 — **open, one VCDS session**

Load-dependent and undecoded. Candidates are mass air flow, ignition advance
and injection time.

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

### 5. AccelG — longitudinal or lateral? **Open, narrowed to two**

What the fixtures did settle: standing still with the engine running
(`02_idle_60s`) the byte reads 127–128, i.e. **0.00 G**, which confirms both
the 127 offset and that the axis is **horizontal** — a vertical axis would read
+1 G at rest. That removes one of the three possibilities.

What they did not settle is which horizontal axis. Correlating the byte against
the derivative of road speed gives r = +0.05 on `07_accel` and r = +0.25 on
`03_drive`, with a slope of 0.29 where a clean longitudinal sensor would give
1.0. That is not an answer: both logs were recorded crawling across an uneven
lawn, where the tilt of the car under each wheel swamps an acceleration of
0.04 G.

**Procedure**, either of these, both a minute long:

- **Park across a slope**, engine running, wheels straight, and read the byte.
  A lateral sensor shows a steady offset proportional to the cross-slope; a
  longitudinal one shows nothing. Then park facing up the same slope: the
  answers swap. This needs no instruments and no driving.
- **Accelerate firmly in a straight line on flat tarmac**, second gear, and
  correlate against speed as above. On tarmac at 0.3 G the signal is an order
  of magnitude above the noise that ruined the garden logs.

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

### 7. ~~Drag torque calibration~~ — **closed in phase 1**

`drag [Nm] = 19.52 + 0.00028 × rpm`, reproducing 21.75 Nm at 797 rpm and
27.75 Nm at 2940 rpm exactly. It is still a straight line through two idling
measurements and says nothing about drag under load; that is phase 6. See
`frames.md` and `config.h`.

### 8. The torque byte's scale — **open, the same VCDS session as question 3**

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

### 9. Two fixtures carry timestamps and disagree with the other five about time, by about a factor of two — **open, and it is the one that matters**

Found while reviewing question 1, and it had gone unnoticed since the fixtures
were recorded.

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
| `m00000000` `MFFFFFFFF` | acceptance mask and code, set to pass 0x480 only |
| `L` | open **listen-only**. Silent on the bus by the adapter's own guarantee, exactly like the firmware's Listen Only |
| `O` | (open normally — *not* this one) |
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
