# Frames transmitted by the converter

Three frames of our own on free IDs. Every log confirms that nobody else uses
0x600–0x602 (`test_target_ids_are_free`).

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
l/100 km. That way a dedicated sensor can be added on the display without
changing anything.

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

- **1.024 V is quoted with no tolerance.** The figure appears in DS39977C only
  in the channel list of Register 23-1; there is no min, typ or max for it
  anywhere in Section 31.0. So VddConv is a trend and a sanity check, not a
  calibrated voltmeter. An absolute reading needs a per-unit calibration
  constant.
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

**S-AQY.TRI does not read this frame.** It is the only one of the three with
no consumer on the display, so its layout is ours to change; the coupling
described in `CLAUDE.md` applies to 0x600 and 0x601. It exists to be watched
on a USBtin while the accumulators are being trusted for the first time.

---

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

The accumulators are written to EEPROM once every 60 s, into a circular buffer
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

**It was a flat average over thirty 1 km slots until 2026-08-12**, which is
120 bytes of RAM summed ten times a second for a number that can only change
once a kilometre. The filter has a mean age of 16 km against the window's 15,
so the estimate is very nearly as steady; `docs/optimisation.md` §10 has the
arithmetic and the one detail that is not obvious, which is that the filter
carries four fractional bits so it cannot stall a long way from the truth.

Until 5 km have been driven since startup, a conservative default of 9 l/100 km
is used so the estimate is not nonsense on a cold start.

**"Litres remaining" is the damped level, not the raw one.** Until 2026-08-11
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
2026-08-11 and this ECU has no torque measuring block at all; a full-throttle
pull would settle it and is deliberately not planned. It is parked under *Never
resolved but not required* in `can-decoding.md` — do not plan that session
again. `test_compute.c` pins the ceiling so the factory figures cannot silently
go out of reach.

**Drag torque** — friction, pumps, alternator — is subtracted from the
indicated torque. It is not constant; it rises with engine speed and is
modelled linearly against rpm.

**Refitted on 2026-08-11 on warm oil.** Four calibration points, the
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
since 2026-08-12, so that dividing it out is a free byte shift on the PIC
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

**The idle point is excluded on purpose, and the idle gate below covers it.**
`11_idle_noac_z1` is 798 rpm at b7 = 24.96 on the same warm oil, which is
*above* the line the other four make — b7 actually falls 24.96 → 18.81 between
idle and 1536 rpm before it starts rising. Idle is a different state: the
throttle sits at its rest position 38 against 48–61 for the holds, so the
pumping loss against a nearly closed throttle is large, and the ECU is
regulating speed rather than letting the engine free-rev. No straight line in
rpm passes through both, so idle is **asserted rather than fitted**. Raising
the intercept to hide the residual instead puts the line back above all four
measured points and brings the understatement straight back.

### The idle gate — a standing car shows zero

**A car standing still with the throttle shut displays zero torque and zero
power. This is a fixed requirement, not a calibration**, and it is not to be
relaxed or made conditional by any future refit of the drag line. It holds on
cold oil and hot, at whatever idle speed the ECU picks.

```c
if (speed_mmh <= IDLE_GATE_SPEED_MMH && throttle <= THROTTLE_REST) return 0;
```

Both thresholds are measured, and neither is an equality:

- **Speed.** A stationary car does not send zero — 0x1A0 raw speed is **1**
  (0.005 km/h) in every log while standing, 7953 frames of it in
  `06_trip_reset` alone. The next value that ever appears is above 40
  (0.2 km/h); nothing in between exists anywhere. The gate is 0.1 km/h.
- **Throttle.** 0x280 b5 is exactly **38** at rest and never lower in any log,
  against 48–61 across the four holds. It is the pedal, not the load: while
  driving, b7 reaches 133 with the throttle still at 38, which is why the
  throttle **alone** cannot be a gate and must be paired with standing still.

Pulling away is throttle above rest while the car still reads 1, so the gate
releases *before* the car moves and the clutch biting is not swallowed.
Coasting downhill off the throttle is not a standstill either, so the gate does
not apply there and the drag line answers, as it should.

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

Six tests in `test_compute.c` and two in `test_txframes.c` assert it, the
latter end to end off the real idle logs including the one with the air
conditioning running. If one goes red, the fix is the code.

The line still says nothing about drag under load, and 72–77 °C is warm rather
than the 95–110 °C of real driving, so it very likely still overstates drag a
little — the conservative direction. `can-decoding.md` question 7 stays open
for that and is the only open question left. Torque is clamped at zero rather
than going negative on the overrun, and is zero below 500 rpm, where the
starter is turning the engine and b7 reads a constant 191–192.

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
