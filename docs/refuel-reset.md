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

The original design wanted to hook into the
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

---

## Corner cases — audited 2026-08-11

Every path that touches the tank was walked. One was a real defect; the rest
are listed so that the next person does not have to re-derive them.

### Fixed: the range read the raw float position

`compute_range_km()` used `decode_state_t.tank_l` — the instantaneous sender
reading, slosh and all — while the level gauge next to it had been damped from
the start. On `07_accel` the raw value swings across 10 L during a pull-away,
which is **111 km of range appearing and disappearing several times a second**.
It now reads the damped level and no longer takes a `decode_state_t` at all.
See `frames.md`.

### The damped level *is* trustworthy while driving

This was the open worry, and the numbers settle it. Running the filter over the
fixtures, one sample a second:

| Log | Raw spread | Damped, 60 s | Damped, 120 s |
|---|---|---|---|
| `07_accel` (driving) | 10 L | 0.44 L | 0.18 L |
| `06_trip_reset` (near empty) | 8 L | 3.45 L | 2.67 L |

The float's slosh is roughly symmetric about the true level, so a first-order
filter converges on it rather than being dragged around by it. The time
constant was raised from 60 s to 120 s on the strength of the table — see
`TANK_DAMP_SAMPLES` in `config.h` for why that costs nothing.

`06_trip_reset` is the honest caveat: it was recorded on the reserve lamp with
the sender at the bottom of its travel, where it is at its worst, and no
filter rescues that. Near empty, treat both the level and the range as
indicative.

### The refuelling trigger stays at-rest-only, deliberately

The damped value is good enough to *display* while driving. It is not good
enough to *reset the trip average* on, and the asymmetry is the point: a missed
refuelling costs one late reset, a false one silently destroys an average the
driver has been watching for 600 km. The median at rest is the most trustworthy
number the tank produces, and the trigger stays on it.

### Known limitations, accepted

- **Refuelling with the engine running, then driving off within ~5 s.** The
  median needs `TANK_MEDIAN_MIN` samples at rest, and the ring is not fed while
  moving, so the rise is only noticed at the next stop — possibly a long drive
  later, and the reset then discards that drive. Refuelling with the ignition
  off, which is the normal case, is unaffected: the ring lives in RAM, so it
  starts empty and reaches the five-sample minimum a few seconds after start-up.
- **A sender fault that reads 0 L and then recovers** is indistinguishable from
  filling up from empty, and will reset the average. There is nothing in the
  frame to tell the two apart.
- **0x320 going silent on its own** freezes the level and the range at their
  last values. The zeroing in `txframes_gather()` keys off the fuel counter's
  liveness, not off each frame separately, and per-frame timeouts were judged
  not worth the state they need.
- **The damped level is not persisted.** After an ignition cycle it is seeded
  from the first live reading rather than restored from EEPROM, which is
  correct — no ramp from zero — but means it briefly carries the slosh of that
  one sample. Only `tank_stable_l` survives, because only the trigger needs
  history.
- **The filter stalls within 0.12 L of its target**, since the step is an
  integer division by `TANK_DAMP_SAMPLES`. That is one digit of the display's
  0.1 L resolution and nothing else.

### Checked and sound

- The refuelling comparison cannot underflow: `median > tank_stable_l` guards
  the `uint8_t` subtraction that follows it.
- A *fall* in the level never triggers anything, so consumption, a leak and a
  sender fault all behave the same way — the level simply follows down.
- The first stable median after an empty EEPROM initialises without resetting,
  so a power cycle does not clear the average.
- Sampling is driven by `compute_tick()` at `TANK_SAMPLE_MS` and is independent
  of frame arrival, so a gap in 0x320 costs samples but never time.
