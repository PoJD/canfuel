# Frames transmitted by the converter

Five frames of our own on free IDs. Every whole-bus log confirms that nobody
else uses 0x600–0x604 (`test_target_ids_are_free`).

**Everything is unsigned big endian.** The car uses little endian, we use big
endian — deliberately, so the two cannot be confused, and the MFD15 handles
both (the Format column in the TRI file, 0 = big endian).

---

## 0x600 @ 100 ms — fuel

| Bytes | Value | Step | Range |
|---|---|---|---|
| 0–1 | FuelNow | 0.1 | dual unit, see below |
| 2–3 | FuelAvg | 0.1 l/100 km | 0–999 |
| 4–5 | FuelTank | 0.1 l | damped, 128 s time constant |
| 6–7 | Range | 1 km | |

## 0x601 @ 100 ms — engine and diagnostics

| Bytes | Value | Step |
|---|---|---|
| 0–1 | Power | 0.1 kW |
| 2–3 | Torque | 0.1 Nm |
| 4–5 | Flow | 0.01 l/h |
| 6–7 | VddConv | 0.01 V |

Flow is carried separately in 0x601 even when FuelNow is currently sending
l/100 km, so the display can show the instantaneous flow whatever unit FuelNow
happens to be in. S-AQY.TRI has a `Flow` sensor on it.

VddConv is the supply voltage the PIC measures on itself through the built-in
1.024 V fixed voltage reference, with no external parts at all. The converter's
reference is VDD and the measured input is the band gap, so the reading is
inverted:

```
VDD = 1.024 × 4096 / code
```

**4096, not 1024.** The A/D on this part is twelve bits, not ten — DS39977C
Table 31-25 parameter A01, `NR Resolution ... 12 bit`. An earlier revision of
this file had `1.024 × 1023 / ADC`, which is the ten-bit formula from a
different PIC and would have reported four times the real supply.

Two things it is worth being honest about, both of them the datasheet's:

- **1.024 V is quoted with no tolerance**, so the nominal arithmetic cannot be
  an absolute reading. The figure appears in DS39977C only in the channel list
  of Register 23-1; there is no min, typ or max for it anywhere in Section
  31.0. On the board this was measured on it was out by 4.1 %, which is 0.20 V
  on a 5 V rail. **`VDD_NUMERATOR_C` in `src/config.h` is the per-unit
  calibration that closes that**, measured against a meter, with the recipe for
  redoing it beside it — every board wants its own.
- **The A/D scatters more than an LSB, so the field is filtered.** 299
  consecutive *unfiltered* samples off one board spanned 4.86 to 4.91 V — about
  ±0.025 V, five times what an LSB is worth here — which would walk the
  display's last digit around ten times a second for no reason.
  `VDD_FILTER_SHIFT` in `src/config.h` puts a first-order filter on it with a
  time constant of about 1.6 s; the same board then sat on two adjacent values,
  4.90 for 228 samples out of 240 and 4.89 for the other twelve, with the mean
  unmoved. **So what 0x601 carries is already an average**, and the accuracy is
  a couple of hundredths of a volt — plenty for the question this field exists
  to answer.

  ⚠ **The filter is why the field cannot see a fast dip**, and that is
  deliberate: cranking is the brown-out detector's job, and it reports through
  the reset cause in 0x603 rather than here.
- **Below 3 V the number stops meaning anything.** Table 31-25 specifies the
  twelve-bit resolution only for VREF ≥ 3.0 V, and VREF here is VDD itself.
  That is also why the brown-out trip point in `src/pic_config.h` is 3.0 V
  rather than the 1.8 V the sibling projects use.

## 0x602 @ 1 s — distance and fuel since reset

A slow frame, used for diagnostics and to confirm the accumulators behave.

| Bytes | Value | Step |
|---|---|---|
| 0–3 | TripFuel | 0.001 l |
| 4–7 | TripDist | 1 m |

Two 32-bit values rather than four 16-bit ones, because a tankful is around
600 km and 55 l — both overflow 16 bits long before the trip is reset.

**S-AQY.TRI reads this frame** — `TripFuel` and `TripDist`, the two 32-bit
values below — so its layout is no longer ours to change alone. The coupling
described in `CLAUDE.md` covers all four frames. It is also still worth
watching on a USBtin while the accumulators are being trusted for the first
time.

⚠ **Both values read systematically LOW against a real odometer, and by
design.** The accumulators live in RAM and reach the EEPROM every 20 s, so
every ignition-off discards 0 to 20 s of them — ten seconds on average, and in
one direction every time. Over a tankful of twenty to sixty journeys that is
roughly **two tenths of a per cent short**, cumulatively, until the next
refuelling clears the trip. FuelAvg is unaffected because it is a ratio and both halves
shrink together; these two are absolutes and nothing cancels. If you are
comparing TripDist against the cluster or a GPS during bring-up, expect the
shortfall rather than hunting an arithmetic bug. `src/persist.h` has the full
arithmetic and why it is not fixed.

## 0x603 @ 1 s — diagnostics, and only with JP1 fitted

| Byte | Value | Notes |
|---|---|---|
| 0 | RXERRCNT | the ECAN receive error counter, raw |
| 1 | TXERRCNT | the ECAN transmit error counter, raw |
| 2 | COMSTAT bits 5–0 | DS39977C Register 27-4: TXBO, TXBP, RXBP, TXWARN, RXWARN, EWARN |
| 3 | flags | `DIAG_FLAG_*`, below |
| 4 | bits 4–0 reset cause, bits 7–5 layout version | `RESET_CAUSE_*`, below |
| 5 | send refusals | `hal_can_send()` returned false this many times, saturating at 255 |
| 6–7 | uptime | seconds since power-up, saturating at 65535 (18 h) |

**Why it exists.** The ECAN error counters were readable only by code running
on the part. Nothing transmitted them, IPECMD reads flash and EEPROM but not
RAM, and a live read means a debugger and the IDE this project does not use.
That left `LED_CAN`'s blink rate as the only instrument — which asks somebody
to tell 2.5 Hz from 5 Hz correctly, once, in a car, at an angle. This frame is
the same information as numbers.

⚠ **It is transmitted only while the DBG_EN jumper (JP1) is fitted.** Nobody is
reading it in a closed dashboard, so the gather and the frame are skipped
entirely — no bus traffic and no CPU spent on nobody. **A converter that sends
0x600 and 0x601 but no 0x603 is almost always a missing jumper, not a fault.**
JP1 already meant "the LEDs may light"; it now also means "diagnostics on".

⚠ **It cannot exist in `HAL_CAN_MODE_LISTEN_ONLY`, and no frame could** — that
mode transmits nothing at all (DS39977C §27.3.4). During `install.md` step 8
the LED is still the only channel there is.

⚠ **Nothing here is latched except `UNHEALTHY`.** Both counters and every
COMSTAT bit are live state, and bus-off recovery resets the transmit counter —
so a converter that went bus-off and recovered reads clean on bytes 0–2.
`DIAG_FLAG_UNHEALTHY` is the memory, and the two are meant to be read together.

`tools/bench_test.py` decodes this frame and turns it into a verdict;
`test/test_txframes.c` pins the byte offsets from the firmware side and
`tools/test_bench_test.py` from the reader's side. **The two decoders are twins
and a layout change belongs in both.**

**There is a third decoder now: the display.** `mfd15/tri/S-AQY.TRI` carries a
row per field, with the six flag bits split out under their own names rather
than shown as one number — so "is the CAN side healthy" can be read off the
dashboard with the jumper in, and no laptop. Single bits are written there as
`shift = n`, `mask = 1 << n`; `mfd15/docs/tri-format.md` has the evidence for
that ordering, which is the opposite of the obvious one.

### Byte 3 — flags

| Bit | Name | Meaning |
|---|---|---|
| 0x01 | `CAN_OK` | `hal_can_init()` reached the mode it asked for |
| 0x02 | `SILENT` | a silent build. Only loopback can set this *and* be seen |
| 0x04 | `UNHEALTHY` | latched: an error counter was non-zero, or the FIFO overflowed, at any point since power-up |
| 0x08 | `DATA_LIVE` | frames from the car are arriving right now |
| 0x10 | `PERSIST_OK` | `persist_load()` found a stored record at start-up |
| 0x20 | `UNHEALTHY_NOW` | the same fault as 0x04, but **current**: an error counter is non-zero or the FIFO overflowed in the last 1.5 s |

`PERSIST_OK` clear is **not** an error on a freshly programmed board: `-OH`
erases the EEPROM by default, and a virgin ring is a correct start.

**`UNHEALTHY` and `UNHEALTHY_NOW` are the same reading twice, and both are
worth having.** The module's error counters walk back to zero on their own once
the bus behaves, so a fault that came and went leaves no trace in bytes 0–2 —
that is what the latch is for, and why it never clears. But a latch is useless
as a light: one transient and `LED_CAN` blinks until the next reset, saying
nothing about now. **`LED_CAN` therefore follows `UNHEALTHY_NOW`**, which goes
out again when the trouble stops, while the frame keeps the memory.

The 1.5 s hold exists because an overflow is an instant rather than a state —
`hal_can_overflow()` clears it as it reports it — and a 100 ms blink is not
something anybody can see. `DIAG_UNHEALTHY_HOLD` in `src/config.h`.

### What has actually set it, in the car: the display

⚠ **Operating the MFD15 through oDSS disturbs the bus.** Observed in the
vehicle: uploading a TRI file, and changing the display's configuration, each
produced a burst of CAN errors — `LED_CAN` blinked for a few seconds,
`UNHEALTHY` latched, and it stayed latched until the next power-up. The error
counters walked back to zero on their own straight afterwards, and no frame the
converter cares about was lost.

**So `UNHEALTHY` set with the counters at zero, after somebody has been in the
display's setup, is very probably not the converter.** Check that before
hunting a bit-timing problem. It is also exactly the case the `UNHEALTHY` /
`UNHEALTHY_NOW` pair was built for: the latch remembered an event the counters
no longer showed, and `LED_CAN` went steady again the moment the trouble
stopped. The design worked — the fault was somebody else's.

**What is NOT established is what the display does** — whether it transmits
malformed frames, resets its own CAN controller, or floods the bus while it
reads or writes its configuration. All that is known is the correlation, taken
by watching 0x603 while operating oDSS, and that distinction is worth keeping
if it is ever reported to CANchecked. `tools/usbtin_capture.py` during an
upload would say more, and nobody has run it.

**It cannot happen while driving**, which is the only time it would matter:
oDSS needs the display's Wi-Fi hotspot, and the hotspot is off by default.

### Byte 4 — reset cause

Out of RCON and STKPTR, latched by `hal_sys_init()` before anything can
disturb them (DS39977C Register 5-1, whose flags are all active low).

| Bit | Name | Meaning |
|---|---|---|
| 0x01 | power-on | POR |
| 0x02 | brown-out | BOR — **only meaningful with 0x01 clear**, see below |
| 0x04 | **watchdog** | the firmware hung. A bug, not an environment |
| 0x08 | RESET instruction | never executed by this firmware |
| 0x10 | stack | STKFUL or STKUNF, with `STVREN = ON` |

**Zero is a legitimate answer** and means none of these — an MCLR reset, which
is what a programmer leaves behind.

⚠ **Brown-out on its own says nothing, and a cold start always reports it.**
DS39977C §5.4.2: *"the BOR bit always resets to `0' on any Brown-out Reset or
Power-on Reset event. This makes it difficult to determine if a Brown-out Reset
event has occurred just by reading the state of BOR alone. A more reliable
method is to simultaneously check the state of both POR and BOR ... IF BOR is
`0' while POR is `1', it can be reliably assumed that a Brown-out Reset event
has occurred."* So **brown-out matters only when power-on is clear** — the two
bits together are the reading, never `0x02` by itself. Every plain power-up of
this board reports `power-on brown-out`, and that is the hardware working.

The other half of that method is already done: `reset_cause_init()` writes each
flag back to its inactive state after latching it, because nothing in hardware
ever does. Without that, every reset from here to the end of time would still
be reporting the power-on that started the day.

**This byte is worth more than the rest of the frame put together.** A
converter that quietly restarts every few minutes looks, from the display,
exactly like one that works: the accumulators come back out of the EEPROM and
the numbers stay plausible. The uptime beside it makes the restart visible and
this byte says whether it was the watchdog or the car's supply — different
faults with different fixes.

## 0x604 @ 1 s — engine health: the idle grade and the start

**Not JP1-gated.** An ordinary frame like 0x600–0x602, transmitted whenever the
converter is powered. 0x603 two sections up sets the opposite precedent, and
deliberately: CAN diagnostics are for somebody who has opened the dashboard,
while this is for a closed one.

| Byte | Name | Unit | Notes |
|---|---|---|---|
| 0 | IdleHealth | 0–200 | 100 = the engine before the repair. **255 = not converged** |
| 1 | IdleRough | 1/32 rpm | the raw grade, 0–7.94, saturating at 254. 255 = nothing graded yet this start |
| 2 | IdleSec | s | settled idle graded this start, saturating at 255 |
| 3 | StartHealth | 0–200 | **reserved: always 255** until the constants are fitted |
| 4 | StartCrank | 32 ms | first turn of the crank to first firing, saturating at 254 (8.1 s) |
| 5 | StartDip | rpm | first-firing speed minus the lowest in the 2 s after it, saturating at 254 |
| 6 | StartClt | °C + 50 | coolant at first firing; 255 = no 0x288 had arrived |
| 7 | flags, layout version | | bits 4–0 `HEALTH_FLAG_*`, bits 7–5 `HEALTH_LAYOUT_VERSION`, as 0x603 byte 4 does it |

| Flag | Bit | Meaning |
|---|---|---|
| `IdleNow` | 0 | settled idle right now: the grade is being stepped |
| `StartSeen` | 1 | this start was watched from a standstill, so bytes 4–6 describe it |
| `HealthLive` | 2 | frames are arriving; with it clear, every other byte reads 255 |

**A trend instrument, not a fault detector.** It needs to move when the engine
moves and sit still when it does not, so that plugs or an injector going off
can be *seen* over months. It will never say *what* is wrong: **the bus carries
the trend, a capture carries the diagnosis.** `tools/idledips.py` is where the
diagnosis lives.

**255 means "not known" in every byte, and zero never does.** A grade of zero
is a perfectly smooth engine and a crank of zero is a perfect start — the wrong
answers that would be believed. So every field that is not known yet publishes
255, the raw fields saturate at 254 to keep it unambiguous, and **on a quiet
bus the whole frame goes to 255 where the other frames go to zero**: each goes
to the value that cannot be mistaken for a reading.

⚠ **Built before a healthy idle was ever recorded, and that was a decision.**
The design said nothing would be built until a healthy grade separated from a
sick one. The post-repair drive could not supply one, because the idle was not
healthy yet. The maintainer's decision was to build the channel anyway,
*because* the idle is about to be worked on — the intake hoses are next — and
the effect is wanted on the display rather than by capture. So the index is
anchored at the old engine (100) and **has not been validated against a well
one**. The layout carries a version, so a later re-anchoring costs no layout
change and `S-AQY.TRI` is touched once, not twice.

What the display shows on day one, from the grade over the recordings so far:

| state | IdleHealth |
|---|---|
| warm idle, oil 52–60 °C, new MAF | 73–100 |
| hot idle, oil 69–71 °C, new MAF | 68–121 |
| August's hot idle, before any work | 48 |

⚠ **The index is comparable only at comparable temperature.** The grade is not
monotonic through a warm-up — it falls and then climbs — so a before/after
comparison that does not state the oil temperature says nothing. A driver
reading it at the same point of the same commute does that for free.

### The idle grade

**The step between one firing event and the next, dead-banded and averaged**:
`max(0, |Δrpm| − 3 rpm)`, filtered over 256 firing events (about 9.7 s of warm
idle), over settled idle only. The index is `min(200, IdleRough × 25 >> 4)`,
one `uint8 × uint8` product and a shift. `docs/can-decoding.md`, trap 6, carries
the chain from a raw 0x280 frame to this byte, worked on a real capture.

- **The step and not the deviation from a baseline.** A first-order baseline
  lags through a warm-up and manufactures about 1.2 rpm of one-sided deviation
  out of nothing. The step between consecutive values is immune to a ramp.
- **Once per CHANGE of the field, not once per frame.** 0x280 holds its
  speed field for three or four frames at idle, and the hold length moves with
  engine speed; stepping per frame would make the grade depend on idle speed
  through the hold ratio. The baseline that decides *whether* the idle has
  settled is the opposite — a time constant, stepped on every frame. Both
  live in `idle_grade()` and both are tested on both sides.
- **Idle is the torque rule's gate**, `STANDSTILL_MMH` and `THROTTLE_REST`,
  the same two definitions and not copies.
- **Settled means quiet, not elapsed.** Grading starts after 3 s in which no
  sample sat 20 rpm or more below the baseline; an excursion restarts the
  delay. A fixed delay grades the tail of every descent from driving speed.
- **The grade belongs to one engine start.** It is cleared when the next start
  begins, not when the car drives off, so every idle of one journey feeds one
  number — and it is withheld (255) until `IDLE_CONVERGE_S`, 30 s, of settled
  idle has been graded, because a filter that starts at zero reads *healthy*
  until it has converged.

**100 is 2.00 rpm, and the old engine measured 2.12.** `IDLE_ROUGH_100` is 64
counts because 100/64 is a multiply by 25 and a shift where 100/68 is a
division; the 6 % that costs is inside the 13 % the anchor itself scatters
between 10 s windows. **0 is "no measurable step at all"**, which no engine
reaches, so the index never bottoms out and always has room to show an
improvement.

### The start

| | `18_coldstart_z1`, before the repair | `19_postfix_drive_z1`, after |
|---|---|---|
| StartCrank | 38 = 1.22 s | 26 = 0.83 s |
| StartDip | 141 (451 → 310) | 118 (450 → 332) |
| StartClt | 66 = 16 °C | 62 = 12 °C |

- **First firing is the first 0x280 at or above 400 rpm**, a decision:
  both recorded starts crank on a plateau of 200–270 rpm and fire at 450–451.
- **A start is measured only if the engine was seen stopped first.** A
  converter that powers up with the starter already turning would start its
  clock late and report a short crank — a *good* start, the one wrong answer
  that is believed. That is stricter than the design's "first sample below
  400 rpm", on purpose.
- **StartCrank is in 32 ms units, not the design's 0.05 s.** A unit chosen here
  is one that may be chosen to be a shift (`docs/optimisation.md` §11); 32 ms
  resolves the 0.41 s between the two recorded starts thirteen times over.
- **StartClt is not a nicety.** A hot restart is trivially easy and its numbers
  mean nothing; a summer-afternoon restart and a February morning need the
  temperature beside them to be two different columns. It is also the one
  temperature the display *cannot* take off the bus itself, because it is the
  value at a past instant.
- **StartHealth ships empty.** Two starts anchor nothing, and an index embeds
  constants that will be revised; a raw number survives the revision. Once a
  dozen good starts have been recorded the constants are fitted, byte 3 starts
  being published and the layout version goes up — **the layout does not
  change**.

⚠ **A stall is indistinguishable from a bad start inside the 2 s window**, and
no frame this firmware accepts carries a clutch switch, so the converter cannot
tell a clutch dump from the engine. It does not look outside the window, so a
stall thirty seconds later is not a start at all. **A single reading is noise;
the instrument is the distribution over many mornings.**

**The oracle is `tools/idledips.py`** — `roughness()` for the grade,
`start_fields()` for the start — and `replay.py --host-build` diffs the C
against it over every timestamped fixture, **exactly**: integer arithmetic on
both sides, the same samples, the same clock, nothing to round.

---

## The frames are spaced out, and it is not tidiness

**One frame leaves every 25 ms and never two together.** 0x600 at 0 ms, 0x601
at 25, 0x602 at 50, 0x603 at 75 and 0x604 at 150 — slot 6, the first one
free of the two fast frames' pattern — with the EEPROM write in the slot at
550 ms because that one sends nothing. Both fast frames are 10 Hz and the slow
ones 1 Hz.

**It is bought with a bench measurement, not with reasoning.** The frames used
to go out in two bursts, 0x600 and 0x601 back to back and 0x602 and 0x603
behind them once a second. At 500 kbps a frame is about 230 µs, so that is
three or four frames inside one millisecond from a single node. **Both USBtin
adapters lost whichever of ours came third on the wire** — silently, without
setting their own overrun flag, and on an otherwise empty bus, so it was not
throughput. Moving a frame out of the burst restored it to exactly its nominal
rate and moving a different one in broke that one instead: two directions, same
hardware.

⚠ **The converter was never at fault, and that is the part worth keeping.** The
ECAN module reported every one of those frames as successfully transmitted, and
DS39977C Register 27-5 is explicit that `TXREQ` is *"automatically cleared when
the message is successfully sent"* — which in CAN requires an acknowledgement
from another node. The frames were on the wire and something else dropped them.
So the spacing is insurance rather than a repair, and it is bought because the
MFD15 is a small device too and nothing can be instrumented once the dashboard
is closed.

⚠ **Which frame is third on the wire is not which send is third in the code.**
DS39977C §27.6.3: buffers of equal priority are transmitted **highest buffer
number first**, and all four of ours are priority 0, so the order depends on
which of TXB0–TXB2 happened to be free when each was queued. That is why the
symptom moved between 0x601, 0x602 and 0x603 as the surrounding code changed,
and why it cannot be predicted by reading the order of the `hal_can_send()`
calls. `src/config.h` carries the full argument next to the constants.

`test_never_two_frames_in_one_pass` in `test/test_scheduler.c` holds the rule
on the host; `tools/bench_test.py` measures the smallest gap between two of our
frames on real hardware. A regression looks exactly like the original symptom —
one frame's rate collapses and nothing else changes.

## FuelNow — dual unit

```
v <  4.0 km/h  ->  instantaneous flow in l/h
v >= 4.0 km/h  ->  consumption in l/100 km
```

**A single threshold, no hysteresis.** The jump when it switches is a
deliberate visual cue that it switched. A 0.5 km/h band can be added later if
the number flickers while crawling right around the threshold.

**Clamp at 999** (99.9 on the display). The TRI gauge tops out at 99.90 and a
higher value would behave unpredictably.

**Why 4 and not 3 km/h:** at 3 km/h a flow above 3 l/h already pushes the value
past 99.9, so it would be clipped on every normal pull-away. At 4 km/h that
boundary only arrives at 4 l/h.

The constants `FUELNOW_LH_BELOW_KMH` and `FUELNOW_CLAMP` belong in `config.h`.

When speed is invalid (the gate in 0x1A0 b1, see `can-decoding.md`), l/h is
sent — without a trustworthy speed, l/100 km is meaningless.

---

## FuelAvg

Always l/100 km. Computed as a **ratio of accumulated microlitres and metres**,
not by integrating the instantaneous value — that way idling at a red light
does not ruin the average.

Below 100 m of distance it returns zero. Without that guard the division is by
an almost-zero distance; on `06_trip_reset.txt` it produced 21,395 l/100 km.

**And there is a cap at the other end.** Nothing clears the
accumulators except a detected refuelling, so a tank sender that fails — or
reads plausibly and never rises — leaves them growing until `total_mm` wraps at
4,295 km, silently, taking the average with it. Past **2,000 km or 400 l** the
trip resets itself. It is a safety net for a fault, not a feature: 2,000 km is
more than three tankfuls and an average over that distance means nothing
anyway. `TRIP_MAX_MM` in `config.h` argues the numbers and why it resets rather
than saturating.

The accumulators are written to EEPROM every 20 s, into a circular buffer
of 64 slots.

### ⚠ On a car that idles more than it moves, FuelAvg is enormous and correct

Read off the display in the vehicle, with the engine idling and 0.6 km on the
trip: **FuelAvg 51.0 l/100 km**, highlighted by the display because it is past
the 30.00 that `S-AQY.TRI` sets as that gauge's top of scale.

Nothing is wrong. l/100 km is litres divided by distance, and a car that spends
a quarter of an hour idling for every few hundred metres it covers really does
consume that much per 100 km — the guard at the other end is the 100 m floor,
which is about dividing by nearly zero, not about the answer being large. The
same drive read 33.4 l/100 km out of the EEPROM ring earlier in its life, on
150 m.

**So a huge FuelAvg on a car being shunted around a yard is arithmetic, not a
fault, and the yellow is a gauge scale rather than a warning.** Leave the
30.00: it is the right top of scale for a car that drives, and a display
configured for the yard would be wrong on the road. `install.md` step 10's
check — FuelNow against FuelCntRaw — is the one that separates a wrong number
from an unusual one.

---

## Range

```
litres remaining / (rolling consumption over the last kilometres) × 100
```

The rolling figure is a first-order filter over completed kilometres, one step
per kilometre with a time constant of sixteen. It behaves the way modern cars
do — after flooring it on the motorway the estimate falls gradually rather than
jumping.

**A flat average over thirty 1 km slots would be simpler**, which is
120 bytes of RAM summed ten times a second for a number that can only change
once a kilometre. The filter has a mean age of 16 km against the window's 15,
so the estimate is very nearly as steady; `docs/optimisation.md` §10 has the
arithmetic and the one detail that is not obvious, which is that the filter
carries four fractional bits so it cannot stall a long way from the truth.

**The basis is never zero and it has no special cases.** It opens at a
conservative 9 l/100 km on a device that has never driven, it is seeded from
the persisted trip average when the ignition comes on, it survives a
refuelling, and nothing else moves it by more than a sixteenth per kilometre.

⚠ **It used to be zeroed at both a refuelling and an ignition cycle, and a
zero basis meant the next completed kilometre became the whole estimate.**
That is the one fault this gauge has had in the car. Range read about 400 km
on the road, halved on pulling away from a filling station and crawled back
over the next fifty kilometres. The cause is a seam rather than a module:
`basis_q4` is not in `persist_record_t` and `total_mm` is, so every restart
restored a long trip beside an empty filter — and the kilometre that then
defined the number was the worst one available. `17_drive_property_z1` is
880 m of exactly that driving at **23.2 l/100 km**, because fuel burned
standing still goes into the segment while the segment's distance does not
move. `src/config.h` under `RANGE_SEGMENT_MM` has the reconstruction.

**The fix was not a shorter window**, which is the obvious thing to reach for
and would have tripled the weight of the offending kilometre.

**There is no longer a distance gate.** `RANGE_MIN_MM` used to be one, and
crossing it stepped Range from the default to whatever the first kilometres
had built — jumping, in the gauge whose whole purpose is not to. It now only
decides whether the persisted trip average is long enough to seed the filter
from at start-up.

An early display reading is kept because it is a good arithmetic check and it
predates the change: **7.6 l in the tank and Range 84 km**, which is
7.6 / 9.0 x 100 = 84.4 — the default basis exactly, on a device 0.6 km into
its life. **Range agreeing with the default to a kilometre is a check that the
arithmetic works, not evidence that the rolling figure has started.** On the
current firmware the same reading means the filter has not yet had a kilometre
to move, rather than that it is being ignored.

**"Litres remaining" is the damped level, not the raw one.**
it was the raw `0x320` b2, i.e. the float position with the slosh still in it.
Measured on `07_accel`, where the raw value swings across 10 L during a
pull-away, that is a range swinging over **111 km several times a second**,
while FuelTank — damped all along — sat still beside it. The two gauges read
the same tank and now agree about it. `compute_range_km()` takes no
`decode_state_t` at all any more, so it cannot regress to the raw value by
accident.

The settled at-rest level the refuelling rule watches would be steadier still,
but it only updates while the car is stationary, so it would leave the range
frozen for a whole motorway drive. The damped level tracks consumption, which
is the entire point of a range gauge.

---

## Torque and Power

**The byte scale, 1.06 Nm/bit, is measured** — off the plateau the engine
actually reaches, against both factory ratings. 0x280 b7 is not Nm; it is a
percentage of a reference torque held in the ECU's calibration, and nobody here
has the reference. What settles the scale is what b7 reads when the engine
makes its rated figures.

b7 is **indicated** torque: at 2940 rpm in neutral (`05_rev3000`) the crank
puts out nothing and b7 still reads 37. So a rating is what is left of b7
*after* the drag line below, and that line is held **in bytes**.

**Held full-throttle pulls in 4th, `19_postfix_drive_z1`**, median b7 in a
±150 rpm window:

| rating | rpm | b7 plateau | drag, bytes | scale |
|---|---|---|---|---|
| 170 Nm | 2400 | **185** | 24.74 | 170 / 160.26 = **1.061 Nm/bit** |
| 85 kW = 156.1 Nm | 5200 | **191** | 42.98 | 156.1 / 148.02 = **1.055 Nm/bit** |

**Two independent ratings and two independent readings agree to 0.6 %.** 1.06
is a decision inside that bracket; on a pull like that one it shows about
170 Nm at 2400 and 85.4 kW at 5200. `test_compute.c` pins both, as the first
version of those tests with a measurement behind them.

The whole plateau, for the shape: b7 rises from 175 at 2000 rpm to a peak of
198 (median) at 4500 and falls back to 175 at 6000, with the pedal on the floor
throughout. Relative load from VCDS group 014 is flat at 78–81 % across it.
**The plateau is not still climbing at the end of any burst** — that was the
flaw of every earlier pull, which ended in a low-gear sweep.

⚠ **Two caveats, stated rather than resolved.** The intake temperature was not
logged during the pulls, and b7 carries the ECU's charge normalisation, so a
hot day reads lower and a frosty one higher — physics, not an error in the
scale, and **not** something to chase with `TORQUE_TRIM_PCT`. And the engine was
not wholly well that day: every fault it had was a low-load one, no misfire
was counted during any pull, and load and air matched the earlier drive. The
scale was set from these pulls on that judgement.

#### Superseded: the scale from b7 = 255

**Kept because it is the obvious argument and it is wrong.** Until the pulls,
the scale was derived by requiring b7 = 255 to reproduce each factory rating
in turn, on the premise that full scale is the rated crank torque plus the
drag at that speed. It gave 0.67 Nm/bit first ("the maximum is 172 Nm, so
172/256", which also forgot the drag), then 0.75 on the cold-oil drag line,
then 0.74 on the warm one:

| | bracket | at the chosen scale |
|---|---|---|
| cold-oil drag line, 0.75 Nm/bit | 0.745 – 0.773 (3.7 % wide) | 85.6 kW, **165 Nm** |
| warm drag line, 0.74 Nm/bit | 0.736 – 0.738 (0.3 % wide) | 85.4 kW, 170.4 Nm |

**The two ratings "agreed" there only because both were nailed to 255.** The
premise was never observed and the pulls refute it: the engine plateaus at
185–206 and falls away above 4500 rpm with the pedal on the floor, so 255 is a
normalisation real air does not reach (see *What that gap is worth in Nm*
below). The shipped 0.74 displayed torque and power **30 % low**.

### b7 is modelled rather than measured, and how much it can see is NOT established

**The ECU has no torque sensor** — the VCDS session went looking and there is
no torque measuring block on this one at all. So b7 is computed from other
readings, and the question that matters here is *which* readings.

⚠ **That question is open, and an earlier version of this section answered it
with more confidence than anything supports.** What follows is sorted by how
well founded it is, because the difference decides how much weight the
`Torque` and `Power` channels can carry as a diagnostic.

**Founded, and it rests on where a sensor sits rather than on any model:**

- **The single pre-catalyst oxygen sensor is in the common exhaust stream**, so
  it measures the four cylinders averaged. One rich cylinder against three lean
  ones can average to a value the ECU is content with, and no amount of
  cleverness downstream recovers the split from that one signal.
- **The fuel trims are the ECU correcting that average, not reporting a
  fault.** A trim is an output of the controller, not a diagnosis.
- **An air-path problem does move b7**, because charge is measured and is
  unambiguously an input.

**Recalled and NOT sourced — treat as a hypothesis:**

- that the model is charge times an efficiency term for lambda and one for
  ignition angle, and in particular **that the lambda entering it is the
  COMMANDED value rather than a measured one**. `mfd15/docs/sensors.md` §8 says
  only that the ME7 "models it from air mass per stroke with corrections for
  ignition advance and lambda" — which is itself unsourced, sits in a sibling
  repository, and says nothing about commanded versus measured. **No Bosch
  document for this ECU is held by this project.** The commanded-lambda step is
  the load-bearing one for "combustion is invisible", and it is exactly the
  step nothing supports.

**Evidence pointing the other way, which the earlier version ignored:**

- **Misfire detection is per-cylinder and works off crankshaft speed
  fluctuation, and it demonstrably runs on this car** — the counter in
  measuring group 014 shows non-zero values in first gear
  (`docs/engine-health.md`). So the ECU is *not* without a per-cylinder
  combustion signal. Whether that signal reaches the torque model is unknown.
- **A badly burning engine does not leave the air path untouched either** —
  residual gas, thermal state and, near the limit, the idle governor all move.
  "None of the model's inputs changed" is an assumption, not a certainty.

**What survives as a working conclusion**, stated at the strength the evidence
allows: these two channels are much closer to an air meter dressed as a torque
gauge than to a dynamometer, and on an unhealthy engine they most likely
**over-read** — reporting what that air should have been worth. But *cannot see
combustion at all* is stronger than anything here establishes, and if the
displayed figures move after a fuelling repair with the air unchanged, that is
the hypothesis above failing rather than an anomaly.

**None of which makes the number wrong on a healthy engine.** It is the
quantity the ECU steers the car with.

⚠ **`docs/engine-health.md` is an open investigation into exactly this**, on
this vehicle, and holds the measurements: the display's peak against the
measured airflow of the same drive, and the two readings of the gap between
them. It is a holding document and will be folded back in or deleted.

### What b7 has actually been observed to reach

**`python tools/b7scan.py` prints this and nothing here is typed by hand.** It
mattered because the scale once rested on *b7 = 255 is the rated crank torque
plus the drag at that speed* — superseded above — and it still matters because
what the engine reaches is what the scale is now read off. The answer
separates three things a bare maximum runs together.

**Cranking is not driving.** 192 appears in `06_trip_reset` and
`18_coldstart_z1`, every sample below 900 rpm with the throttle at rest in the
seconds after the key — the ECU asking for torque to start the engine. Behind
the gate `compute_torque_d()` applies, the largest b7 this engine has been seen
to **make** is **206, at 4402 rpm in `19_postfix_drive_z1`** — 80.8 % of full
scale — and 198 in `24_mafswap_drive_z1`.

**A maximum is not a plateau, and until `19` there was no plateau.** All three
wide-open bursts in `17_drive_property_z1` had their maximum in the last
quarter: the deepest goes 159 at 2609 rpm to 185 at 4921 rpm, monotonically,
and then the throttle closes. Every pull before the repair was a low-gear
sweep that ended before the engine filled, so **b7max before the repair and
b7max after it are not a comparison.** `19` fixed that by design: held pulls in
4th, 23 wide-open bursts of which 14 had stopped rising before the throttle
closed. That is what the scale is now read off — the plateau medians in the
table above, not the maximum here.

**b7 tracks the ECU's own relative load, which is what a charge-dominated model
looks like.** The drive of 2026-09-10 showed a peak of 117 Nm on the display,
which back through the drag line is b7 ≈ 189–201 depending on where in the
range it fell — **74–79 % of full scale against the 78.1 % relative load VCDS
logged over the same pulls** (`engine-health.md`). ⚠ **Those are a display
maximum and a mean over wide-open samples, not one measurement**, so this is
arithmetic pointing somewhere rather than a result. Where it points: **the gap
from the plateau to 255 is the same size as the gap between the measured air
and the ECU's reference air** — and the held pulls in `19` then put relative
load at 78–81 % across the whole plateau. Reaching 255 needs the engine to fill to 100 % of a
reference normalised to 0 °C and 1013 hPa — and that is the reference,
measured, in *What "load" is a percentage of*. **No fuelling repair changes what
the air-mass sensor reads.**

#### What that gap is worth in Nm, if the reading is right

**Turn the normalisation round and every b7 becomes a statement about air.**
`engine-health.md` measured the reference off this car — 0 °C and 1013 hPa,
1.293 g/l — so relative load is **the engine's filling times the density of the
air it is breathing, divided by the density of that reference**:

```
rl  =  VE  x  rho(intake) / 1.293 g/l
```

⚠ **That is one identity with two unknowns in it, and they were never separated.**
The measurement is the product: **rl = 78.1 % at full throttle**, taken at an
intake temperature nobody logged. `engine-health.md` brackets it by assuming
the intake was somewhere in 20–40 °C, which is what makes its filling figure a
range — **20 °C pairs with VE 84 %, 40 °C with VE 93 %**, and those rows are
not independent readings of the engine. **The honest content of that drive is
the 78.1 %, and everything below inherits its width from the temperature nobody
wrote down.**

**So the ceiling is a function of the weather, which is the part that is easy
to miss.** Carrying the same measurement to other intake temperatures:

| intake air | relative load a full-throttle pull would show | b7 with it |
|---|---|---|
| +35 °C | 74.5 – 82.4 % | 190 – 210 |
| **+25 °C** — plausible for a September drive | **77.0 – 85.2 %** | **196 – 217** |
| +10 °C | 81.0 – 89.7 % | 207 – 229 |
| 0 °C | 84.0 – 93.0 % | 214 – 237 |
| −20 °C | 90.6 – 100.3 % | 231 – 256 |

Read the other way, what each b7 asks of the air:

| b7 | relative load | intake air it needs |
|---|---|---|
| ~199 — what the 2026-09-10 display peak inverts to | 78.0 % | **+21 to +52 °C — the drive that produced it** |
| 235 | 92.2 % | **−24 to +2.5 °C** |
| **255 — what the scale assumes** | **100 %** | **−44 to −19 °C** |

**b7 = 255 is therefore out of reach in any condition this car is driven in**,
and that is the load-bearing conclusion: the scale's premise asks for air
colder than −19 °C even at the most generous end of the bracket, and the intake
draws from the engine bay, which sits about ten degrees above ambient (the
first cold start recorded 22.5 °C of intake with the oil at 12.75). **The two
factory figures are not merely unobserved. They are unreachable.**

⚠ **b7 ≥ 235 is a different matter and an earlier version of this section got
it wrong**, by reading the filling bracket as a property of the engine rather
than as one drive's air. It needs a hard frost — −24 to +2.5 °C of intake — so
it is out of reach on a warm drive and **not** out of reach in principle. Say
"not on this drive", not "not ever".

⚠ **SUPERSEDED — the bracket below was 10–15 % low, and the reason is
arithmetic, not new data.** It divided **188 Nm**, which is the rating plus
the drag *converted to Nm at 0.74 Nm/bit*, by the plateau. But the drag scales
with the scale. Held in bytes, as `config.h` holds it, the same route lands
where the pulls put it, 1.055–1.061. Kept because the direction it pointed —
well above 0.74 — was right, and because the route is the natural one to
re-derive.

**Two independent routes then bracket the scale, and they overlap.** Full scale
has to cover the rated crank figure plus the drag at that speed — 188 Nm, and
notably the same 188 Nm at both rating points, 188.3 at 2400 rpm against 187.9
at 5200 — so the scale is 188 Nm divided by whatever b7 really plateaus at:

- **from the air**, a plateau of 196–217 at a September intake gives
  **0.87–0.96 Nm/bit**;
- **from brake thermal efficiency**, the 28–32 % that `engine-health.md` calls
  normal for this engine puts the same drive's peak at 150–171 Nm rather than
  117, which is **0.90–1.01 Nm/bit**.

The overlap is **0.90–0.96 Nm/bit**, and the shipped 0.74 sits 20–25 % below
both.

⚠ **A factory rating is quoted at a standard air condition, not at the day's
weather**, so the anchor wanted is the plateau corrected to that condition
rather than the raw maximum off any one drive. **Which standard the AQY's 85 kW
and 170 Nm are corrected to is not held by this project** — it is near 20 °C
either way, which is why the September row above is the right one to reason
from and a January one would not be.

⚠ **Neither route measures the scale.** Both are arithmetic on readings taken
for other purposes, one of them a display maximum against a log mean; and the
whole of it rests on b7 inheriting the charge normalisation, which is a
hypothesis with one coincidence behind it and a counter-observation at idle,
where b7 and relative load diverge 9.8 % against 23.2 %. **What settles it is
b7 and relative load logged together across a held full-throttle pull** —
`next-drive.md` steps 14 and 14a — because that tests the proportionality over a
range instead of at one point, **and because it reads the intake temperature
that collapses the width of every bracket above.**

**b7 is not eight bits of resolution.** Across every fixture it takes 95
distinct values between 0 and 192, and 88 of the 92 gaps between consecutive
values are **2**, with a single-count step at each multiple of 64. **One
*count* is still 0.39 % and `config.h` is right to say so** — that is the unit
the byte is transmitted in, and what `TORQUE_TRIM_PCT` steps by. What this adds
is that the ECU does not use every count: **the smallest change b7 has ever
been seen to make is two of them, about 0.8 % of full scale and near 2.1 Nm.**
That strengthens rather than weakens the "b7 did not move at the idle dips"
observation in `engine-health.md` — the resolution available to that argument
is twice as coarse as it assumed.

### At full load the lambda in the model cannot be a measured one

**The load-bearing hypothesis above is that the lambda entering the torque
model is the commanded value rather than a measured one, and nothing this
project holds says so.** At **full load specifically** it is close to forced,
by what the instrument can do rather than by what the model does:

- full-load enrichment is mapped and open-loop, at a commanded lambda well
  below 1;
- **the pre-catalyst sensor is a switching one**, which `can-decoding.md`'s own
  summary of block 034 says without meaning to: the ageing test it runs is a
  **sensor period ≤ 2.2 s**. A period is a property of a sensor that switches.
  A broadband sensor does not switch and has no period to measure.
- a switching sensor carries no information away from stoichiometric. At the
  enrichment of a full-throttle pull it is simply hard over.

**So at wide-open throttle the ECU has no instrument that could tell it the
actual lambda**, and whatever its torque model multiplies by there, it is not a
measurement. ⚠ **That argument does not extend below full load**, where the
sensor works, closed loop runs and block 032's adaptations are exactly the ECU
acting on a measured lambda. It says the *scale* question is safe from the
fuelling repair. It says nothing about b7 at idle or part load, and the general
"b7 cannot see combustion" remains what the section above calls it — a
hypothesis, and one misfire detection argues against.

⚠ **The sensor-type step is an inference from the ageing check in block 034**,
not a part number read off the car and not a Bosch document. VCDS would settle
it in one screen.

### The owner's gain — `TORQUE_TRIM_PCT`, zero by default

**Out of the box this firmware reports the factory figures for a stock AQY and
claims nothing else.** `TORQUE_TRIM_PCT` in `config.h` is a whole-per-cent gain
on the displayed torque and power, shipped at zero, for somebody who has a real
measurement of their own car — a dynamometer run, a remap with a known gain —
and wants the gauge to agree with it.

**It is a presentation knob and not a calibration**, and the distinction is
load-bearing. Everything else in this section is an argument about what the
ECU's byte *means*; the trim is an argument about what one car's owner wants
their gauge to read. Setting it does not make the scale better founded, and a
scale that is genuinely wrong is fixed by changing the scale rather than by
papering over it here — `docs/next-drive.md` has that decision tree.

**It is legitimate rather than a fudge, and the reason is worth stating.** A
factory rating is itself a *normalised* number, quoted at a standard air
condition rather than measured on the day; a dynamometer does the same, and its
software corrects the cell measurement to that standard before anyone sees a
figure. Every gauge and every printout in this field therefore reports a
corrected number. One more correction, with its reasoning written beside it, is
in keeping with the practice.

⚠ **It has to be a constant somebody sets once, because a live correction is
out of reach.** A real correction factor needs the intake air temperature, and
**that is not on this bus** — `0x420` bytes 1–2 are documented as ambient
temperature and read zero on this car, and b3 is the oil (`can-decoding.md`
question 4). ⚠ **The car does have an outside-temperature display**, in the
mirror console; it changes nothing here, because ambient is not intake air —
the intake draws from the engine bay, about ten degrees above it — and a
number a driver can read is not a number the converter can use.

It applies to **net** torque, after the drag line is subtracted, which is where
a dynamometer measures; power follows because `compute_power_d()` is handed the
trimmed torque. **The fuel figures are untouched and this must never become a
fuel trim.** One step is 0.39 %, which is exactly one count of b7 — asking for
finer would be precision the input does not carry.

**Drag torque** — friction, pumps, alternator — is subtracted from the
indicated torque. It is not constant; it rises with engine speed and is
modelled linearly against rpm.

**Fitted on warm oil.** Four calibration points, the
free-revving holds `13` to `16`, all stationary in neutral so the crank drives
nothing and b7 *is* the drag:

| Hold | rpm | b7 | oil | throttle |
|---|---|---|---|---|
| `13_rev1500_z1` | 1536 | 18.81 | 72.8 °C | 48 |
| `14_rev1850_z1` | 1850 | 20.66 | 74.2 °C | 51 |
| `15_rev2372_z1` | 2372 | 26.32 | 75.3 °C | 56 |
| `16_rev2926_z1` | 2926 | 27.23 | 76.6 °C | 61 |

Least squares through them, in bytes, gives `drag_b7 = 9.11 + 0.006514 × rpm`
with residuals of −0.9 to +1.8 counts, and at 1.06 Nm/bit that is

```
drag [Nm] = 9.66 + 0.00690 × rpm
```

The constants live in `config.h` as `DRAG_TORQUE_BASE_CNM` and
`DRAG_TORQUE_SLOPE_Q16` — the slope scaled by 2**16 rather than by 10,000
so that dividing it out is a free byte shift on the PIC
rather than a reciprocal multiply. **The calibration is in bytes, not Nm** —
both constants are the byte line times the scale, and they are recomputed from
the byte line whenever the scale moves, never rescaled from their previous
values. That has happened twice: 0.75 → 0.74 with the warm refit, and
0.74 → 1.06 with the pulls, where the byte line stayed put.

**What it replaces.** A two-point line, `drag = 19.52 + 0.0028 × rpm`, fitted
on `02_idle_60s` (oil 60.8 °C) and `05_rev3000` (oil **39.0 °C**). Cold oil
overstates drag, and since this line is *subtracted*, the display understated
torque and power — it read zero through 51 % of `17_drive_property_z1` where
the new line reads a number through 78 % of it. Peak torque over that same
drive barely moved, 105.8 → 107.0 Nm at the 0.74 scale of the time, because
at high load the drag is a small term. The whole of the difference is at part throttle.

**The idle point is excluded on purpose, and the driving gate below covers it.**
`11_idle_noac_z1` is 798 rpm at b7 = 24.96 on the same warm oil, which is
*above* the line the other four make — b7 actually falls 24.96 → 18.81 between
idle and 1536 rpm before it starts rising. Idle is a different state: the
throttle sits at its rest position 38 against 48–61 for the holds, so the
pumping loss against a nearly closed throttle is large, and the ECU is
regulating speed rather than letting the engine free-rev. No straight line in
rpm passes through both, so idle is **asserted rather than fitted**. Raising
the intercept to hide the residual instead puts the line back above all four
measured points and brings the understatement straight back.

### The driving gate — torque is shown only while the car is being driven

**Torque and power are displayed only while the car is moving *and* the driver
is asking for torque. Standing still shows zero whatever the pedal is doing,
and a released pedal shows zero whatever the speed is. This is a fixed
requirement, not a calibration**, and it is not to be relaxed or made
conditional by any future refit of the drag line. It holds on cold oil and hot,
at whatever idle speed the ECU picks.

```c
if (speed_mmh <= STANDSTILL_MMH || throttle <= THROTTLE_REST) return 0;
```

**It is an OR, and it used to be an AND.** Gating on "standing *and* released"
left two states showing a number that the car is not in:

- **Revving in neutral at a standstill.** The crank drives nothing there —
  which is exactly what makes the four free-revving holds a *calibration*
  rather than data — so the honest answer is zero. 1,528 samples of
  `17_drive_property_z1` are this state.
- **The last few seconds of every roll to a stop.** High in the deceleration
  the ECU cuts fuel, b7 falls below the drag line and the answer is zero;
  once engine speed drops back onto the idle governor, b7 climbs while the
  pedal never moves. One real stop out of `17_drive_property_z1`, throttle at
  38 throughout:

  | speed | rpm | b7 | old gate, at 1.06 Nm/bit |
  |---|---|---|---|
  | 19.6 km/h | 1358 | 7 | 0.0 Nm |
  | 13.5 km/h | 898 | 17 | 2.2 Nm |
  | 8.0 km/h | 792 | 25 | 11.4 Nm |
  | 3.8 km/h | 783 | 27 | 13.6 Nm |
  | standing | 776 | 27 | 0.0 Nm |

  **The apparent threshold is engine speed returning to idle, not road speed.**
  In first gear the two coincide near 4–8 km/h, which makes it look like a
  speed threshold and is a coincidence of gearing — worth knowing before
  hunting for one.

Both are the same fault: **the drag line is systematically low at idle**, 14
against a measured 25 in b7 at 800 rpm, because no straight line in rpm passes
through both idle and the free-revving holds. Idle is asserted rather than
fitted, and the assertion has to cover every state the engine idles in, not
only the parked one.

**What it costs**, because it is not free. Over `17_drive_property_z1` the
share of samples displaying zero goes **28.4 % → 58.0 %**, with the peak
unmoved at 153.3 Nm — but that log is six minutes of first-gear pottering with
a great deal of coasting, so it is the worst case rather than a typical drive.
And **pulling away reads zero until the car moves**: a median of 0.7 s after
the pedal leaves rest across the 14 pull-aways in that log, 1.75 s at worst, so
real torque against a slipping clutch is not shown for that time. Accepted
deliberately — a stationary car showing a number is the thing being fixed.

Both thresholds are measured, and neither is an equality:

- **Speed.** A stationary car does not send zero — 0x1A0 raw speed is **1**
  (0.005 km/h) in every log while standing, 7953 frames of it in
  `06_trip_reset` alone. The next value that ever appears is above 40
  (0.2 km/h); nothing in between exists anywhere. The gate is 0.1 km/h.
- **Throttle.** 0x280 b5 is exactly **38** at rest and never lower in any log,
  against 48–61 across the four holds; across every fixture the next value
  above 38 that ever appears is **44**, so nothing occupies 39–43. It is the
  pedal and not the load, which is what lets it gate on its own: a released
  pedal is a statement about the driver, and what b7 does afterwards is the
  engine looking after itself.

⚠ **The b7 = 133 spike is not a counter-example**, though it was read as one
here and that reading is what made the gate an AND. b7 does reach 133 at
throttle 38 in `17_drive_property_z1` — at 4522 rpm, during a gearchange, in a
frame where 0x1A0 was not reporting a valid speed at all. It is the pedal and
the load byte disagreeing for a few frames, not a state the car sits in.
Bucketed by engine speed, mean b7 at throttle 38 is 14–17 everywhere above
1000 rpm, which is *below* the drag line; only the idle bucket sits above it,
at 27.6. Gating those spikes away is a second thing this rule buys.

**The construction is not ours.** SAE J1979 carries *actual engine percent
torque* (PID 0x62) and *engine friction percent torque* (PID 0x8E) as separate
standard PIDs — precisely indicated-minus-friction — and PID 0x64, *engine
percent torque data*, gives five reference points of which **the first is
idle**, so the standard also treats the idle value as its own datum rather than
a point on a curve. Read off the [OBD-II PID
tables](https://en.wikipedia.org/wiki/OBD-II_PIDs) and [CSS
Electronics](https://www.csselectronics.com/pages/obd2-pid-table-on-board-diagnostics-j1979),
which agree with each other; J1979 itself is paywalled and has not been read.
That is **evidence, not a specification** — the rule stands on its own.
Sports-mode power displays in production cars behave the same way, reading zero
at idle and rising with load ([BMW i4
forum](https://www.i4talk.com/threads/power-torque-instrument-cluster.7190/)).

Eight tests in `test_compute.c` and two in `test_txframes.c` assert it, the
latter end to end off the real idle logs including the one with the air
conditioning running. One of the eight replays the stop above frame by frame,
and one asserts that the gate does *open* — without that, the rest would pass
on a `compute_torque_d()` that returned zero unconditionally. If one goes red,
the fix is the code.

The line still says nothing about drag under load, and 72–77 °C is warm rather
than the 95–110 °C of real driving, so it very likely still overstates drag a
little — the conservative direction. `can-decoding.md` question 7 stays open
for that and is the only open question left. Torque is clamped at zero rather
than going negative on the overrun, and is zero below 500 rpm, where the
starter is turning the engine and b7 reads a constant 191–192.

One consequence of the gate for that refit: **the holds it needs will display
zero**, because they are taken standing still in neutral. That is correct and
not a fault to chase — the refit is done off the raw log and b7, not off the
display.

```
power [kW] = torque [Nm] × rpm ÷ 9550
```

The MFD15 cannot compute this itself — per the manual, math channels exist only
on the MFD28/32.

---

## Corner cases

| Situation | Behaviour |
|---|---|
| flow is 0 | FuelNow 0.0 |
| data source lost for > 500 ms | every bus-derived value zero, VddConv unchanged; 0x604 all 255 |
| engine stopped (rpm 0 or counter 0) | flow zero, not frozen at its last reading |
| distance < 100 m | FuelAvg 0.0 |
| no kilometre completed yet | Range uses the 9 l/100 km the basis opens at |
| speed invalid | FuelNow in l/h |
| value over range | clamped to 999 |

**Why VddConv is the exception.** It is the one value here that does not come
off the bus — the PIC measures it on itself. A quiet bus is exactly the moment
somebody wants to know whether the converter is still being fed, so zeroing it
would throw away the only diagnosis available. Everything else goes to zero,
because a frozen last reading is a plausible number that is no longer true.

**Why the flow goes to zero when the engine stops.** The counter stops moving
and the restart rule takes over, so nothing new arrives to average. Left
alone, the sliding window would keep reporting whatever was burning at the
moment the ignition was switched off.
