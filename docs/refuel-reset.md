# Resetting the average — on refuelling only

No button, no Can Switching licence, no RTC. It behaves like the "since
refuelling" average in modern cars.

---

## The rule

```
tankStableL  = first-order filter of (0x320 b2 & 0x7F) over the samples taken
               while standing (v < 0.1 km/h), one a second, tau = 16 s

armed        = REFUEL_ARM_S consecutive at-rest samples since the car last
               moved.  Below it the rule cannot fire at all.

refuelling   = REFUEL_CONFIRM_S consecutive at-rest samples, while armed,
               more than REFUEL_RISE_L above tankStableL
```

- Update **only while stationary**. Ignore the value entirely while driving.
- Five consecutive at-rest seconds more than **4 L** above the settled level
  means refuelling -> clear the average accumulators.
- **But not for the first REFUEL_ARM_S of any stop.** The rule asks whether
  the level ROSE while the car was parked here, not whether it is higher than
  some older figure, and a float that has just stopped moving cannot answer
  either question yet.
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

`tankStableL` is deliberately **not** the median of a ring, read out
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
litre**, and `test_no_fixture_triggers_a_refuelling` replays all eighteen
recordings and requires that none of them fires the rule.

---

## Why a 4 L threshold, and why only at rest

Both were measured on real data.

While standing, the value varies by only 2–3 L and one reading dominates
overwhelmingly — 1584 of 1622 samples were exactly 6 L. While driving the
spread is 9–10 L and evenly distributed, because the float in the tank sloshes
on every corner and every brake application.

⚠ **THAT MEASUREMENT WAS TAKEN ON A CAR THAT HAD BEEN STANDING**, and "has
been standing" is not the same claim as "its speed has just reached zero".
On `17_drive_property_z1`, a log of repeated short stops, the raw level spans
**five litres while the car is fully stopped** — 0 L ×473, 1 L ×399, 3 L ×58,
4 L ×27 — because the float has not finished swinging from the last piece of
driving. The threshold was three litres. The whole margin was the
consecutive-sample counter, and replaying the rule over every fixture shows
the longest run above the threshold reaching **1 of the 5** it needed. One
barrier, nothing behind it.

**The threshold is four litres now and not five**, which was offered on the
grounds that nothing under 5 L has ever gone into this car. It is refused
because the comparison is a `>` on an *indicated* rise and this sender
under-reads — 6 L into a nearly empty tank settled at 5 L — so at five a real
6 L fill showing as +5 would be missed. Four keeps a litre of margin either
side.

⚠ **AND THE FIXTURES CANNOT SHOW ANY OF THIS PROPERLY, WHICH IS WORTH
KNOWING BEFORE TRUSTING THE NUMBERS ABOVE.** Every fixture that contains a
moving car has **0–10 L in the tank**; the only one with a real level,
`18_coldstart_z1` at 50 L, never moves. The float therefore has never been
recorded in motion anywhere but the bottom of its travel, and the sender is
nonlinear. A capture on an ordinary drive with a half-full tank would close
this and nothing else will.

So the instantaneous value is unusable while driving, and at rest it barely
moves at all -- which is what lets a plain filter and a counter stand in for a
median.

`07_accel.txt` confirms this is real: during a short pull-away, b2 jumps
between 1, 5, 7 and 9 litres. If the reset were tied to the instantaneous
value, it would fire on every pull-away.

---

## The 2026-09-19 fill, and what it measured

**Owner-reported off the display, not a capture.** The converter and the
MFD15 were fitted and the tank was filled on the way back from a 450 km trip;
nothing was recording. So this is three numbers and an observation rather than
a log, and everything below is bounded by that.

| | |
|---|---|
| indicated before, `FuelTank` on the display | **10.9 L** |
| delivered, off the pump | **44.17 L** |
| indicated after | **50.9 L** |
| the reset | **fired** — the average zeroed |

### The rule has fired in the car at least three times, and none of them is recorded

⚠ **An earlier version of this section called this the first, and it was
not.** Owner-recalled, so the count is approximate and the dates are not
held:

| | fill | outcome |
|---|---|---|
| earlier | **6 L from a jerrycan**, at the garden | fired |
| earlier | **a full tank**, the one `18_coldstart_z1` was recorded on | fired |
| 2026-09-19 | the 44.17 L above | fired |

⚠ **All three fired on a threshold of THREE, not four.** The firmware in the
car predates `REFUEL_RISE_L` becoming 4 (commit `e8d634c`), so every one of
these is evidence about the rule **as flashed** rather than as it now stands
in the tree — and a fill watched in the car stays a test of three until the
device is reprogrammed.

**The 6 L jerrycan would have fired at four as well**, which is the one that
was in doubt: 6 L delivered showed **+5 indicated**, and 5 clears a `> 4`. It
clears it by one litre instead of two, and **that 5-against-6 is very probably
the same event `config.h` argues from** when it refuses a threshold of five.

⚠ **Which puts a number on the smallest fill the current rule is sure of, and
it is about six litres.** At the near-empty gain of 0.83 a 5 L fill indicates
4.15, the sender reports whole litres, and `4 > 4` is false. Nothing under
5 L has ever gone into this car — `config.h` says so — so this is a margin
rather than a hole, but it is the margin, and it is one litre wide.

**So the rule works in the car and has for some time.** What is still missing
is not a demonstration, it is a *recording*: every one of these happened with
nothing logging, and `18_coldstart_z1` opens at 50 L already filled rather
than filling. *Watch out when implementing* below therefore stands unchanged,
and so does the fixture suite's position — `test_no_fixture_triggers_a_refuelling`
replays eighteen logs in which nobody ever refuels.

⚠ **The jerrycan is the one worth having and the one nobody wrote down.** A
jerrycan is a small fill and `REFUEL_RISE_L` is a threshold about small
fills — a 44 L fill clears it by an order of magnitude and says nothing about
where the edge is. **If the quantity is remembered, it belongs in this
table.**

⚠ **What was observed each time is the average zeroing, and `refuels` was
never read.** 0x603 is transmitted only with JP1 fitted and the dashboard has
been shut for all three, so the count that would have confirmed them is the
one channel that was not available. `vehicle-history.md` asks for `refuels` to
be checked rather than assumed for exactly this reason, and these are the
cases that could not honour it.

**There is a second symptom at the pump and it costs nothing.** `compute.c`
snaps the damped display level straight to the raw reading when it detects a
refuelling, so on a detection the gauge **jumps**. Without one it creeps:
`TANK_DAMP_SAMPLES` is a 128 s time constant, so a 40 L step is only about
three-quarters of the way there two minutes later. **A gauge showing the new
level within seconds of the nozzle is the rule having fired**; one that walks
up over the following five minutes is the filter alone. Worth knowing next
time, because it needs no jumper, no bench and no capture.

### The sum does not add up, and the shortfall is the sender's own scale

10.9 + 44.17 = 55.07 L and the gauge settled at 50.9. **That is neither an
arithmetic fault nor this firmware** — `compute_tank_d()` applies no
calibration at all, so what the display shows is the sender's own number,
damped.

What a fill measures is the sender's **gain**: how much indicated litre it
returns per litre actually delivered.

| span | delivered | indicated rise | gain |
|---|---|---|---|
| near empty, an earlier fill | 6 L | 5 L | **0.83** |
| 11 → 51 indicated, this fill | 44.17 L | **40.0 L** | **0.905** |

**Both are under one, and the second is forty litres wide rather than five**,
so the scale is compressed over most of the travel and not only at the bottom
where the sender was already known to be poor.

⚠ **Saying that the compression "explains" the 4.17 L is circular, and it is
worth being explicit about that.** The gain was derived from the rise, so the
rise agreeing with the gain is arithmetic and not evidence. **The one
non-circular check is what a zero-offset scale of 0.905 says the tank held at
the brim: about 56 L against a 55 L nominal**, which is a filler neck and is
plausible. Plausible is the whole of what it is.

⚠ **The sender's own step is a whole litre.** The tenths on the display come
from the damping filter, not from resolution, so ±0.5 L of quantisation sits
under each end of that 40.0 and the gain is 0.905 ± 0.023.

⚠ **Neither row is an absolute calibration**, and reading them as one is the
error available here. A gain says what a *rise* is worth and says nothing
about where the scale sits, so "the tank really held 55.07 L" does not follow
from "10.9 was indicated beforehand". Whether the fill was a brim is not
recorded either — nobody watched the nozzle click.

**It points the same way as `REFUEL_RISE_L` = 4 without being what decides
it.** `config.h` refuses five because the threshold is a `>` on an *indicated*
rise and this sender under-reads; that argument rested on the 6 L fill alone,
at the one corner where the sender is known to be worst. ⚠ **This point could
not have refused five on its own**: at a gain of 0.905 a 6 L fill still shows
5.4 and would have been caught. **It is the near-empty gain of 0.83 that does
the work**, and what the wide point adds is that the compression is not a
quirk of the bottom of the travel.

### What it changes in `src/`, which is nothing, and that is a decision

**`compute_tank_d()` stays uncalibrated.** `CLAUDE.md` closed the tank as a
decision on one point taken near empty; this is a second point and it does not
reopen it. Two chords are not a curve on a sender that is nonlinear at both
ends, and a 9 % gain fitted to them would be asserting the middle of the
travel, which nothing has measured at all.

**And the direction is the safe one.** `compute_range_km()` reads the damped
level, so a scale 9 % low makes Range about 9 % pessimistic. A range that
under-promises is the error to have.

**What would change it** is the middle of the travel, which only a tank driven
down from full supplies — so the next drive and the ones after it, not another
fill.

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

⚠ **The rule has since fired in the car at least three times** — *The
2026-09-19 fill* above. Those are observations off a display and not
recordings, so this paragraph stands unchanged: what is still missing is a
capture spanning a fill, and nothing in the corpus is one.

---

## Corner cases

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
  `compute_tick()` also resets it past `TRIP_MAX_MM` (2,000 km) or
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
