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
| Torque (indicated) | 0x280 | 7 | ~0.67 Nm/bit | 172 Nm max on the AQY |
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

---

## What is NOT on the bus

- **Lambda** — 0x488 is constant `ff ff ff 8d ff ff ff ff` in every log.
- **Battery voltage** — searched systematically, nothing. Solved with the
  display's internal sensor instead.
- **Ambient temperature** — 0x420 b1 and b2 are both zero; the car has no sensor.
- **Trip odometer and trip reset** — see open questions.

---

## Open questions

1. **The flow in `05_rev3000` does not match the specification.** It quotes
   958 µl/s, the data gives 1005 µl/s. The 5 % gap is not in the data but in
   the assumed 0x480 period — at 51.9 ms it would come out at exactly 958. The
   log has no timestamps, so only measuring the period on a live bus can settle it.

2. **The starting counter value in `07_accel`.** The specification quotes
   13247 → 22622; the first sample in the file is 12870. The end matches, the
   start does not. The 377 µl difference is a handful of early frames — the
   specification was probably computed from a later point in the log.

3. **0x288 b5 and b6** — load-dependent and undecoded. Candidates are MAF,
   ignition advance and injection time. Fastest route is comparing against
   measuring blocks in VCDS.

4. **Is 0x420 b3 oil or IAT?** `07_accel` was recorded to answer exactly this.
   Temperature holds at 75.75 → 76.5 °C during the acceleration, so it does
   **not** fall. IAT would drop when accelerating. That argues for oil, but the
   run was short (16 s), so it is not conclusive.

5. **AccelG: longitudinal or lateral?** Parking across a slope settles it.

6. **Source of the trip reset** — candidate 0x5D8 b0. `06_trip_reset` was
   recorded for this and has not been analysed yet.

7. **Drag torque calibration** — both points are in the logs (idle and 2940 rpm
   in neutral); they just need to be substituted in.
