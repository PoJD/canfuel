# Resetting the average — on refuelling only

No button, no Can Switching licence, no RTC. It behaves like the "since
refuelling" average in modern cars.

---

## The rule

```
tankStableL = median of (0x320 b2 & 0x7F) over the last 20-30 s of standing (v < 1 km/h)
```

- Update **only while stationary**. Ignore the value entirely while driving.
- A rise in `tankStableL` of **more than 3 L** means refuelling → clear the
  average accumulators.
- The rule also applies within a single session, so it covers refuelling with
  the engine running.
- `tankStableL` is stored in EEPROM as part of the existing 12-byte record
  (written once every 60 s) so it survives the ignition being switched off.
- On the very first start with an empty EEPROM, initialise only — do not reset.

## The window has to be usable before it is full

Implemented in `compute.c` as a 25-slot ring sampled once a second while
stationary, which is the 20–30 s the rule asks for. But the median is trusted
from **five** samples on, not from twenty-five (`TANK_MEDIAN_MIN`).

The reason is the sequence that actually happens at a filling station: the
engine is off while refuelling, so on the next start the ring is empty and the
driver may pull away within a few seconds. Waiting for a full window would
mean the refuelling is never noticed at all — the one case the whole rule
exists for. Five samples are enough because the value at rest barely moves:
1584 of 1622 measured samples were the same litre.

The ring is not cleared when the car starts moving, so shortly after a stop it
still holds samples from before the drive. That is intended — it is the same
tank — and it means a refuelling seen mid-window flips the median after about
thirteen seconds rather than instantly.

---

## Why a 3 L threshold and why a median

Both were measured on real data.

While standing, the value varies by only 2–3 L and one reading dominates
overwhelmingly — 1584 of 1622 samples were exactly 6 L. While driving the
spread is 9–10 L and evenly distributed, because the float in the tank sloshes
on every corner and every brake application.

So the instantaneous value is unusable, while the median taken at rest is rock
solid.

`07_accel.txt` confirms this is real: during a short pull-away, b2 jumps
between 1, 5, 7 and 9 litres. If the reset were tied to the instantaneous
value, it would fire on every pull-away.

---

## Why not the trip reset from the instrument cluster

The original design (see `implementation-plan.md`, §5) wanted to hook into the
cluster's trip reset and had two variants behind an `#ifdef`.
`06_trip_reset.txt` was recorded to settle that choice and **has not been
analysed yet**.

Tying the reset to refuelling is better in that it needs no sniff, no licence
and no decision — it runs on data we already have reliably. If
`06_trip_reset.txt` turns out to show trip kilometres on the bus, the CLUSTER
variant can be added as a second trigger rather than as a replacement.

---

## Watch out when implementing

In the current data the tank reports **0 litres with the reserve lamp on**
(b2 = 0x80) throughout the first session. The rule therefore cannot be tested
against these logs — a recording taken while refuelling is needed. Until then
it has to run on synthetic frames in `test_compute.c`.
