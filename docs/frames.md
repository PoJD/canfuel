# Frames transmitted by the converter

Four frames of our own on free IDs. Every log confirms that nobody else uses
0x600–0x603 (`test_target_ids_are_free`).

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

---

## The four frames are spaced out, and it is not tidiness

**One frame leaves every 25 ms and never two together.** 0x600 at 0 ms, 0x601
at 25, 0x602 at 50 and 0x603 at 75, with the EEPROM write in the slot at
550 ms because that one sends nothing. Rates on the wire are unchanged — both
fast frames are still 10 Hz and both slow ones 1 Hz — so nothing here concerns
`S-AQY.TRI`.

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

Until 5 km have been driven since startup, a conservative default of 9 l/100 km
is used so the estimate is not nonsense on a cold start.

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

**The byte scale, 0.74 Nm/bit, is a decision.** 0x280 b7 is not Nm — it is a
percentage of a reference torque held in the ECU's calibration. It used to be
read at 0.67 Nm/bit, from "the AQY's maximum is 172 Nm, so 172/256". That
premise is wrong on the fixtures' own evidence: at 2940 rpm in neutral
(`05_rev3000`) the crank puts out nothing and b7 still reads 37, so b7 is
**indicated** torque and its full scale is the maximum *indicated* torque —
the rated crank figure plus the drag at that speed. Scaling to the crank
maximum and then subtracting drag counts the friction twice.

Requiring b7 = 255 to reproduce each factory rating in turn brackets the scale
— and **the bracket moves with the drag line**, because what full scale has to
cover is the rated crank figure *plus* the drag at that speed. On the old
cold-oil line the two ratings disagreed, 0.745 (85 kW at 5200 rpm) against
0.773 Nm/bit (170 Nm at 2400 rpm). On the warm line below they nearly agree:

| | bracket | at the chosen scale |
|---|---|---|
| cold-oil drag line, 0.75 Nm/bit | 0.745 – 0.773 (3.7 % wide) | 85.6 kW, **165 Nm** — 3 % under the rating |
| warm drag line, **0.74 Nm/bit** | **0.736 – 0.738** (0.3 % wide) | **85.4 kW, 170.4 Nm** — both within 0.5 % |

That the two independent ratings now agree about the scale is a check that
passed, not a measurement: the constraint is dominated by the drag line's
*slope*, so a wrong intercept can still look consistent. **Nothing available
settles it, and it is no longer an open question.** The VCDS session was run on
This ECU has no torque measuring block at all; a full-throttle
pull would settle it and is deliberately not planned. It is parked under *Never
resolved but not required* in `can-decoding.md` — do not plan that session
again. `test_compute.c` pins the ceiling so the factory figures cannot silently
go out of reach.

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
with residuals of −0.9 to +1.8 counts, and at 0.74 Nm/bit that is

```
drag [Nm] = 6.74 + 0.00482 × rpm
```

The constants live in `config.h` as `DRAG_TORQUE_BASE_CNM` and
`DRAG_TORQUE_SLOPE_Q16` — the slope scaled by 2**16 rather than by 10,000
so that dividing it out is a free byte shift on the PIC
rather than a reciprocal multiply. The line is unchanged to five parts per
million. **The calibration is in bytes, not Nm** — change the
scale above and this line has to be refitted with it, which is exactly what
happened here: the scale moved 0.75 → 0.74 in the same breath.

**What it replaces.** A two-point line, `drag = 19.52 + 0.0028 × rpm`, fitted
on `02_idle_60s` (oil 60.8 °C) and `05_rev3000` (oil **39.0 °C**). Cold oil
overstates drag, and since this line is *subtracted*, the display understated
torque and power — it read zero through 51 % of `17_drive_property_z1` where
the new line reads a number through 78 % of it. Peak torque over that same
drive barely moves, 105.8 → 107.0 Nm, because at high load the drag is a small
term. The whole of the difference is at part throttle.

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

  | speed | rpm | b7 | old gate |
  |---|---|---|---|
  | 19.6 km/h | 1358 | 7 | 0.0 Nm |
  | 13.5 km/h | 898 | 17 | 1.5 Nm |
  | 8.0 km/h | 792 | 25 | 8.0 Nm |
  | 3.8 km/h | 783 | 27 | 9.5 Nm |
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
unmoved at 107.0 Nm — but that log is six minutes of first-gear pottering with
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
| data source lost for > 500 ms | every bus-derived value zero, VddConv unchanged |
| engine stopped (rpm 0 or counter 0) | flow zero, not frozen at its last reading |
| distance < 100 m | FuelAvg 0.0 |
| distance < 5 km | Range uses 9 l/100 km |
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
