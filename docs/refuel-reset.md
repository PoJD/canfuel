# Resetting the average — on refuelling only

No button, no Can Switching licence, no RTC. It behaves like the "since
refuelling" average in modern cars.

---

## The rule

```
tankStableL  = first-order filter of (0x320 b2 & 0x7F) over the samples taken
               while standing (v < 1 km/h), one a second, tau = 16 s

refuelling   = REFUEL_CONFIRM_S consecutive at-rest samples more than
               REFUEL_RISE_L above tankStableL
```

- Update **only while stationary**. Ignore the value entirely while driving.
- Five consecutive at-rest seconds more than **3 L** above the settled level
  means refuelling -> clear the average accumulators.
- The rule also applies within a single session, so it covers refuelling with
  the engine running.
- `tankStableL` is stored in EEPROM as part of the existing 12-byte record
  (written every 20 s) so it survives the ignition being switched off, and
  the filter is re-seeded from it on the next start rather than from the first
  sample -- seeding from the sample would swallow exactly the change the rule
  exists to notice.
- On the very first start with an empty EEPROM, initialise only — do not reset.

**The baseline is frozen while the counter is running.** If the filter were
allowed to chase the new level it would raise `tankStableL` under the
comparison and disqualify the rise it is in the middle of confirming, so
whether a 4 L fill was detected would depend on how fast the filter happened to
move. Held still, the rule means what it says.

### This used to be a median, and why it is not any more

Until 2026-08-12 `tankStableL` was the **median of a 25-slot ring**, read out
of a 128-bucket histogram, trusted from five samples on. It worked. It was
replaced because the median was never a requirement — it was a choice made
once, and nothing had ever compared it against a cheaper one. It cost 2,453
cycles once a second and 153 bytes of RAM, and what it was being asked is not
"what is the middle value" but **"is the level suddenly and persistently higher
than it was"**, which a counter answers directly.

What the two do differently, honestly stated:

| | median of 25 | five in a row |
|---|---|---|
| a single wild reading | rejected by construction | rejected, counter restarts |
| a reading high for 4 s | rejected | rejected |
| a reading high for 13 s | **accepted** — the ring has flipped | accepted after 5 s |
| a real fill, at rest | seen after ~13 s | seen after 5 s |
| a real fill, engine off | seen ~5 s after the next start | unchanged |
| cost | 2,453 cycles, 153 B | ~40 cycles, 3 B |

So the counter is *quicker* to believe a real fill and no more willing to
believe a spurious one — the case the median genuinely covered better, a burst
of noise longer than five seconds but shorter than thirteen, is not a shape the
sender produces at rest. **1584 of 1622 measured at-rest samples were the same
litre**, and `test_no_fixture_triggers_a_refuelling` replays all seventeen
recordings and requires that none of them fires the rule.

---

## Why a 3 L threshold, and why only at rest

Both were measured on real data.

While standing, the value varies by only 2–3 L and one reading dominates
overwhelmingly — 1584 of 1622 samples were exactly 6 L. While driving the
spread is 9–10 L and evenly distributed, because the float in the tank sloshes
on every corner and every brake application.

So the instantaneous value is unusable while driving, and at rest it barely
moves at all -- which is what lets a plain filter and a counter stand in for a
median.

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
driver has been watching for 600 km. The at-rest reading is the most
trustworthy number the tank produces, and the trigger stays on it.

### Known limitations, accepted

- **Refuelling with the engine running, then driving off within ~5 s.** The
  rule needs `REFUEL_CONFIRM_S` consecutive samples at rest and nothing is
  sampled while moving, so the rise is only noticed at the next stop — possibly
  a long drive later, and the reset then discards that drive. Refuelling with
  the ignition off, which is the normal case, is unaffected: the counter starts
  from zero on every start and five seconds of standing still is all it needs.
  The partial count is deliberately not persisted; five seconds is short enough
  that carrying it across a power cycle would buy nothing and would need a
  thirteenth byte in the record.
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
- **The displayed filter stalls within 0.12 L of its target**, since the step
  is an integer division by `TANK_DAMP_SAMPLES`. That is one digit of the
  display's 0.1 L resolution and nothing else. The settled level behind the
  refuelling rule stalls within 1/16 L for the same reason, which is a
  sixteenth of the threshold it feeds.

### Checked and sound

- The refuelling comparison cannot underflow: `st->tank_l > tank_stable_l`
  guards the `uint8_t` subtraction that follows it.
- **A refuelling is no longer the only thing that clears the trip.** Since
  2026-08-12 `compute_tick()` also resets it past `TRIP_MAX_MM` (2,000 km) or
  `TRIP_MAX_UL` (400 l), because otherwise a sender that never rises leaves the
  accumulators growing until `total_mm` wraps at 4,295 km. That path does NOT
  increment `refuels`, which keeps meaning "the tank was seen to rise".
- A *fall* in the level never triggers anything, so consumption, a leak and a
  sender fault all behave the same way — the level simply follows down.
- The first at-rest sample after an empty EEPROM initialises without resetting,
  so a power cycle does not clear the average. After a *non-empty* EEPROM the
  filter is seeded from the stored litre instead, which is what makes a
  refuelling done with the ignition off visible at all.
- Sampling is driven by `compute_tick()` at `TANK_SAMPLE_MS` and is independent
  of frame arrival, so a gap in 0x320 costs samples but never time.
