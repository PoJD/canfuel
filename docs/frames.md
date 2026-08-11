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
| 4–5 | FuelTank | 0.1 l | damped over 60 s |
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
litres remaining / (rolling consumption over the last 30 km) × 100
```

The rolling average runs over 1 km segments, so 30 slots. It then behaves the
way modern cars do — after flooring it on the motorway the estimate falls
gradually rather than jumping.

Until 5 km have been driven since startup, a conservative default of 9 l/100 km
is used so the estimate is not nonsense on a cold start.

---

## Torque and Power

**The byte scale, 0.75 Nm/bit, is a decision.** 0x280 b7 is not Nm — it is a
percentage of a reference torque held in the ECU's calibration. It used to be
read at 0.67 Nm/bit, from "the AQY's maximum is 172 Nm, so 172/256". That
premise is wrong on the fixtures' own evidence: at 2940 rpm in neutral
(`05_rev3000`) the crank puts out nothing and b7 still reads 37, so b7 is
**indicated** torque and its full scale is the maximum *indicated* torque —
the rated crank figure plus the drag at that speed. Scaling to the crank
maximum and then subtracting drag counts the friction twice.

Requiring b7 = 255 to reproduce each factory rating in turn brackets the scale
between **0.745** (85 kW at 5200 rpm) and **0.773** Nm/bit (170 Nm at
2400 rpm). 0.75 sits inside the bracket, reproduces both to within 3 %, and
errs low on torque. A VCDS measuring block or a full-throttle sniff would
settle it; neither exists yet. `test_compute.c` pins the ceiling so the
factory figures cannot silently go out of reach again.

**Drag torque** — friction, pumps, alternator — is subtracted from the
indicated torque. It is not constant; it rises with engine speed and is
modelled linearly against rpm.

Two calibration points, both already in the logs:

- idle (`02_idle_60s`, 797 rpm)
- 2940 rpm in neutral (`05_rev3000`) — torque at the wheels is zero there, so
  indicated torque equals drag torque

Both points have now been substituted in. The model is

```
drag [Nm] = 19.52 + 0.00028 × rpm
```

and it reproduces both measurements exactly: 21.75 Nm at 797 rpm and 27.75 Nm
at 2940 rpm, which are the raw values 29 and 37 of 0x280 b7. The constants live
in `config.h` as `DRAG_TORQUE_BASE_CNM` and `DRAG_TORQUE_SLOPE_E4`. **The
calibration is in bytes, not Nm** — change the scale above and this line has to
be refitted with it.

It is a two-point straight line through two idling measurements, so it says
nothing about drag under load — that is what phase 6 is for. Torque is clamped
at zero rather than going negative on the overrun, and is zero below 500 rpm,
where the starter is turning the engine and b7 reads a constant 191–192.

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
