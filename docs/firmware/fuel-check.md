# Checking the fuel channel against the pump

**The only ground truth this project has for `FuelAvg` and the trip:
litres delivered at the pump against odometer kilometres.** What the
car's pump history is, what it can and cannot check, which changes to the
car a comparison must not span, and how to take the check properly.

*Moved here from `docs/engine-health/vehicle-history.md` on 4/10/2026,
when that file became the car's service book alone. The parts and dates
these sections argue from are still there.*

---

## Measured consumption, from the pump

**Litres delivered against odometer kilometres, per year.** This is the only
ground truth this project has for the fuel channel.

| Year | l/100 km |
|---|---|
| 2017 | 8.6 |
| 2018 | 8.8 |
| 2019 | 9.9 |
| 2020 | 8.6 |
| 2021 | **10.9** |
| 2022 | 7.4 |
| 2023 | 8.9 |
| 2024 | **7.0** |
| 2025 | — *(no driving)* |

**Range 7.0 to 10.9, mean 8.8, and the spread is 45 % of the mean** *(derived
from the table)*. What that scatter is worth, and what it is not worth, is the
next section.

### The fill of 2026-09-19

**44.17 litres, off the pump, at the end of the Šumava trip.** It is recorded
here because it is the first fill since the work of 9/2026 whose litres
anybody wrote down — **earlier fills happened and were not counted**
(`refuel-reset.md`) — and because a litre count is worth keeping even
when it cannot yet be divided by anything.

⚠ **It is not a consumption figure and must not be turned into one.** Neither
the odometer at this fill nor the state of the tank at the previous one was
noted, so the two things the ratio needs are both missing. The ~450 km of the trip
is owner-reported (`docs/engine-health/vehicle-history.md`, *Distance and
use*) and would give 9.8 l/100 km — **which is arithmetic, not a
measurement**, and it sits in the upper half of a table whose own spread is
45 %. Do not add it as a row.

**What the same fill did measure is the sender**, not the engine:
`refuel-reset.md`, *The 2026-09-19 fill*, has the three numbers and
what they say about the tank scale. That is a different quantity from anything
in this file.

**Next time, the odometer.** The brim-to-brim procedure at the end of this
file is five steps and step 1 is the one that half-happened: the tank was
filled, the reading was not written down. A fill with the odometer beside it,
twice, is the whole of what stands between this project and a real check on
the fuel channel — and the car is now in the state where that check is finally
worth taking.

### The fill of 2026-10-17 — the first brim with the distance kept

**51.47 litres, off the pump, filled to full** (*owner*), into a tank the
display read at **1.1 L**; the first fill without the Liqui Moly cleaner
after its tank (`docs/engine-health/plan.md` item 5). **The odometer read
about 154,200 km** shortly after, and the instrument cluster's trip was
zeroed at the pump, so **the cluster's trip carries this tank's
kilometres** to the next full fill without anybody needing the odometer
to the kilometre. That makes this step 1 of the procedure below. The
refuelling reset fired: the converter's trip started from the pump too.

**Read at the next full fill, before the nozzle goes in**: the cluster's
trip, and the display's `TripDist`, `TripFuel` and `FuelAvg`. Then the
litres off the pump.

**The converter does not see the whole tank, and that is filled in
afterwards** (*decided 17/10/2026*). With the USBtin capturing, the MFD
is out and the converter unpowered (`CLAUDE.md`, *Recording a session at
the car*), so a captured drive is missing from `TripDist` and `TripFuel`.
It is not missing from the capture: `tools/replay.py` integrates 0x1A0
and the 0x480 counter with the same arithmetic, so the captured drives'
kilometres and microlitres are added to the display's figures by
replay, not by hand. **A drive with the MFD out and no capture is lost
outright**, and the comparison then says so rather than guessing it.
In this tank so far:

- **19/10/2026 morning**, about 35 minutes, the first 10 at normal
  speed and the rest in Prague traffic (*owner*): in neither the display
  nor any fixture, so the pump's litres will run above the sum by that
  drive's fuel.
- **23/10/2026, a part fill: 3.11 l** off the pump at **154,501 km**,
  the cluster's trip at **289.4 km**, the display reading **23.5 L**
  before it (*owner*, `docs/engine-health/photos/odometer-2026-10-23.jpg`).
  It went in after **325 ml of BG 44K** (`docs/engine-health/plan.md`
  item 6a), which burns as fuel and is in no pump's litres. **The
  converter's trip reset at it all the same**: that evening the display
  read **`TripDist` 98.7 km, `FuelAvg` 11.1**, about the day's driving
  (*owner*, 23/10; `refuel-reset.md`, the table). So **the display's trip
  runs from this fill, not from 17/10**, and what it held for 17–23/10
  was not written down before the nozzle went in; the cluster's trip
  still spans the whole tank. **At the next brim, the pump's litres are
  added to these 3.11 and the can's 0.325**; the cleaner's tanks in
  between are read for the ratio, not for the engine's consumption.
  *This said "3.11 l is under `REFUEL_RISE_L`, so the converter's trip
  carries on through it" until the display showed otherwise.*

⚠ **This tank no longer spans the map going back**: that was set for
22/10 and is postponed to 3/11 (`docs/engine-health/plan.md` item 5a),
so the whole tank so far is on the remap. *This said "this tank spans
the map going back on 22/10" until 23/10.*

**Distance is a second comparison in the same numbers.** On the first
11 km, with no stop between, the display read **11.3** and the cluster
**11.1** (*owner*): 0x1A0's speed against the cluster's own calibration,
neither of them ground truth, and inside the cluster's 0.1 km
resolution. Over a tankful it becomes a percentage worth reading.

### The fill of 2026-10-24 — the 17/10 tank closed

**50.88 litres of Orlen Verva 100, off the pump**, at **154,755 km**,
the cluster's trip at **543.5 km** (the last digit half-lit; .9 is
possible and moves nothing below), after the second can of BG 44K
(`docs/engine-health/plan.md` item 6a). Read before the nozzle went in
(`docs/engine-health/photos/mfd-2026-10-24-before-fill.jpg`,
`docs/engine-health/photos/odometer-2026-10-24.jpg`): **`FuelAvg` 9.7,
`TripDist` 256, `FuelTank` 0.4, Range 4** (*owner*: 0.7 L left). Both
the cluster's trip and the converter's were zeroed at it (*owner*). The
pump receipt is not kept here: the photograph shows the owner.

**The pump's figure for the tank, 17/10 to 24/10** *(derived)*:

| | |
|---|---|
| petrol, 3.11 + 50.88 | **53.99 l** |
| and the 44K can of 23/10 | 0.325 l |
| distance, the cluster's trip | **543.5 km** (odometer 154,755 − 154,501 + 289.4 = 543.4) |
| **litres over kilometres, petrol only** | **9.94 l/100 km** |
| the same with the can counted as fuel | 9.99 l/100 km |

⚠ **Brim to brim only if both fills stopped at the same click.**
17/10 was filled to full (*owner*); 24/10 took 50.88 into 0.4–0.7
indicated against 51.47 into 1.1, so the two ends agree to about a
litre, which is the brim's own scatter (step 5 below) — about 2 % of
this figure. **Not owner-confirmed as full to the click.**

**It is the first post-repair pump figure, and it checks the firmware
only loosely.** The display's trip covers **the last 254.1 km** of the
cluster's 543.5, because the 23/10 part fill reset it (above), so no
display figure spans the same tank as the pump's. What the numbers do
say *(derived)*:

- **`TripFuel` on the last stretch: 9.7 × 2.56 ≈ 24.8 l** (±0.1 for the
  display's rounding). That leaves **29.2 l for the first 289.4 km, 10.1
  l/100 km** — the cold 19/10 drive across Prague, `39`, `40` with its
  long warm stops, and the end of the Liqui Moly tank's habits. The
  previous tank read 10.3 on the display (`docs/engine-health/idle-log.md`,
  17/10). **Plausible, and not a test**: a converter reading 5 % low
  would move the same litres into the first half and stay just as
  plausible.
- **Distance: `TripDist` 256 against the cluster's 254.1 km, +0.7 %**
  (+0.5 to +1.0 with the display's whole kilometres). A first
  percentage over a real distance; neither instrument is ground truth.
  The first 4.5 km of the next tank read **4.6 on the display** (*owner*,
  24/10): the same direction, inside both instruments' 0.1 km.

**Within the pump history, at its upper end** (7.0–10.9, above): a
tank of brisk motorway, a strong cleaner and Prague traffic, on the
remap. One tank, so the step-5 caution applies.

**The next tank is the clean one**: the cluster's trip and the
display's both start at this brim, no capture is planned
(`docs/engine-health/plan.md` item 6), and the 44K can (0.325 l) went in
before the fuel again. **Read at the next full fill, before the nozzle**:
the cluster's trip, `TripDist`, `FuelAvg`, the odometer; then the
litres, filled to the click. A captured drive or one with the MFD out in
between is written down, as above.

⚠ **Two things this tank changes and the next comparison carries.**
The fuel is **Orlen Verva 100**, not OMV MaxxMotion 100 (no OMV on the
route, *owner*): a consumption comparison across the brand is fine for
the firmware, which compares against the same tank's pump, and is noted
for the engine. And **the map goes back on 3/11** (`docs/engine-health/plan.md`
item 5a), likely inside this tank: **read the four figures on the day,
before the map goes back**, so the tank can be split at it.

---

## What this means for the measurements

**The short version: the pump history bounds canfuel's fuel channel to the
right band and no better than that, and several of the parts it was measured
through are old enough to have moved it.**

### The 7–11 spread is not a statement about accuracy

**3.9 l/100 km of spread is 45 % of the mean, which is an order of magnitude
larger than any error this firmware could plausibly make.** So the history
cannot be used to check canfuel to a few per cent. It can say "about 8 or 9,
not 5 and not 15", and that is a genuinely useful thing to be able to say
about a channel derived from a 15-bit counter — but it is the whole of what it
says.

The spread has at least five contributors, and they are listed in the order of
how much they are likely worth:

1. **The thin years are thin enough to be single fills.** 2024's 600 km at
   7.0 l/100 km is **42 litres** *(derived)* — **less than one tankful**, against the
   55 l `config.h` costs the persist interval on. 2023's 900 km is about
   one and a half. A yearly average computed over one brim is one brim's
   measurement error, and a brim is worth a litre either way. **The two lowest
   years in the table, 7.4 and 7.0, are also among the thinnest.** That is very
   likely most of the low end, and it means the bottom of the range is softer
   than the top.
2. **A car doing 600–900 km a year is doing them cold.** Short journeys run
   through the warm-up enrichment, measured directly on `18_coldstart_z1`:
   **927 µl/s in the first 30 s of running** against 326 at a warm idle, and
   162 ml for five and a quarter minutes of standing still. This pushes consumption **up**, so it is a
   candidate for the high years rather than the low ones — 2021's 10.9 is
   consistent with mostly-cold short runs and needs no fault to explain it.
3. **The converter was progressively blocking across the later years.** It was
   completely blocked when it came off in 2026 and it did not arrive there in
   a week. A restricted exhaust costs pumping work and therefore fuel, on a
   ramp with no date on it. There is no measurement that separates this from
   the item above.
4. **Both oxygen sensors date from 10/2017 and have never been replaced.** The
   ECU's fuelling is whatever the upstream sensor tells it to be, so a sensor
   that has drifted moves the pump figure and canfuel's figure **together and
   in the same direction** — which is exactly why neither can detect it.
   The fork is the thing to read here: any `not OK` from
   VCDS blocks 034, 036 or 037 is a **second** failure of an already-replaced
   sensor, and both of these have additionally spent their lives behind a
   converter that was burning through.
5. **The remap, the seasons, the tyres and the driver**, none of which are
   separable in a per-year figure and none of which are worth arguing about at
   this resolution.

### Before and after — do not mix across the September 2026 work

**There is no single "after".** The repair came in steps, several of them
with the battery off, which also resets the ECU's adaptations:

| date | change | recordings on this side of it |
|---|---|---|
| until 10/9/2026 | exhaust with the blocked converter, old plugs, old injectors, old MAF | fixtures `01`–`18` |
| 10/9 | converter, flex pipe, silencer | — |
| 17/9 | plugs and leads | — |
| 23/9 | injectors and fuel filter; battery disconnected | `19`–`23` (old MAF) |
| 24/9 | MAF; battery disconnected again, adaptations from zero | `24` onwards |
| 26/9 | battery out for the coil-harness measurements; adaptations from zero again. Back in 29/9, throttle adapted (098, *ADP OK*) on the old part | — |
| 1–2/10 | the valve cover and throttle job (`docs/engine-health/idle-log.md`); battery disconnected, adaptations from zero | `25`–`26` (session A) |
| 4/10 | the right cover gasket; battery disconnected, 098, adaptations from zero | `27`–`29` (sessions A and B) |

**Rule: no fuel calibration and no tank-to-tank comparison spans one of these
lines.** For consumption, only the state after 24/9/2026 counts, and the first
few hundred kilometres after it are the adaptations settling (group 032,
`docs/engine-health/open.md` S9). The pump history above is all from before the first line.

### The two figures measure different things, and the difference has a name

**The pump measures litres delivered. canfuel measures what the ECU believes
it injected** — 0x480 counts microlitres, one count per microlitre
(`can-decoding.md`, the signal table), and the ECU derives that from injector
open time against its own model of the injector.

So the two disagree by exactly the error in the ECU's injector model, and
**that model is now pointed at injectors fitted in 9/2026 that the ECU has
never been calibrated against.** Closed-loop control hides part of it: if the
new injectors flow differently from the model, lambda control moves the pulse
width until the mixture is right, and the counter follows the pulse width. The
residual does not vanish, it moves into the **fuel trims** — which is why
the adaptations of group 032 are the first place to look (**−4.7 % at idle
against +1.6 % at part load** before the repair; the large rich trim after it
turned out to be the MAF, `docs/engine-health/refuted.md` C2) if a tank-to-tank check comes out with a
consistent offset rather than scatter.

### Which parts are old enough to bias the result

Sorted by how directly they sit in the measurement chain:

| Part | Why it matters here |
|---|---|
| **Oxygen sensors, 10/2017** | the largest risk on the list. They set the fuelling, so they move both figures together and are invisible to any comparison of the two. **9 years and the full ownership distance**, behind a failing cat |
| **Fuel filter** | was the oldest fuel-side part on the car and **was replaced with the injectors on 23/9/2026**, so it has left this table. A restricted filter limits rail supply under demand; it was always by some distance the cheapest item here to eliminate, and it is now eliminated |
| **MAF, 7/2018** (replaced 24/9/2026) | `frames.md`'s volumetric-efficiency argument rules out a *badly* failing sensor by arithmetic — the volumetric efficiency it implies stays physical — and explicitly **does not** rule out a slightly lazy one. 8 years |
| **Plugs and leads, 12/2022** | **four calendar years but only ~1,500 km.** An earlier record called them "four years downstream of whatever has been happening", which is true of the dates; the distance is the other half of it and it is small. Old by date, nearly new by wear |
| Pump 10/2022, coil 6/2026, FPR 7/2026, cat 9/2026, injectors 9/2026 | **effectively new.** Everything that sets rail pressure and injector flow — the two inputs 0x480 depends on — is now a 2026 part |
| Throttle body, original | **not new, but inspected and found clean in 6/2026.** It meters the idle air, so it is on the idle fault's side of the engine; its condition was seen rather than assumed. An earlier revision of this table listed it as effectively new, and that was wrong |

**The asymmetry is the point, and after September 2026 it is as stark as it
can get.** Two whole sides of this engine have been renewed and a third has
not been touched in eight or nine years.

| | state after 9/2026 | exceptions |
|---|---|---|
| **fuel delivery** | pump, filter, regulator, injectors — **all new** | **the lines and pipes from the tank to the engine**, never changed; and the tank itself, replaced at an unrecorded date |
| **ignition** | coil, leads, plugs — **all 2026** | none |
| **measurement** | MAF new 24/9/2026 (a genuine VW `06A 906 461 A`, replacing the 2018 insert) | both lambda sensors 10/2017 |
| **air path** | throttle body original, inspected clean 6/2026, new gasket | the intake manifold and its hoses, never changed |

**Everything that decides how much fuel is delivered and whether it is lit is
now current, and since 24/9/2026 so is the MAF. What is left that tells the
ECU what happened is the two oxygen sensors, nine years old**, which have
spent those years behind a converter that was burning through. That was where to look next, and the fork was what read it: any `not OK` from VCDS blocks 034, 036 or 037 would have been a
**second** failure of an already-replaced sensor. **All three reported OK on
24/9/2026**, so the sensors are not what keeps the idle misfiring
(`docs/engine-health/refuted.md` C5).

⚠ **The fuel lines are the one thing on the delivery row that stays old**, and
they are named rather than passed over: they run the length of the car, they
are original as far as anything here records, and they sit between a tank of
unknown date and parts fitted in September 2026.

### How to use this as a sanity check, and how not to

**The check is tank to tank against the pump. No fixture can stand in for
it.** The longest recording in the corpus, `17_drive_property_z1`, is six
minutes and 880 m of first-gear pottering, and replaying it gives
**23.16 l/100 km** — a correct number for that log and worthless as a
comparison against a yearly average. Every fixture is idle, revving in neutral
or a crawl; none of them is a drive. The pump is the only place a comparable
figure exists.

The procedure, once the car has some distance on the new parts:

1. Brim the tank at a pump, to the same click, and note the odometer.
2. Drive normally — mixed roads, not a lap of the block.
3. Brim again at the **same pump**, same click. Litres delivered over odometer
   kilometres is the reference figure.
4. Compare against canfuel's `FuelAvg`, which the refuelling reset zeroes at
   step 1 on its own (`refuel-reset.md`) — so it measures the same tank,
   provided the reset actually fired. Check `refuels` on 0x603 rather than
   assuming.
5. **Repeat over more than one tank.** A brim is worth about a litre, which on
   a 45 l fill is over 2 % before anything else goes wrong.

Three things to keep in mind while reading the answer:

- **Expect the post-2026 car to sit at the low end, or below it.** A blocked
  converter, tired plugs and a nine-year-old filter have all been dealt with
  since the last figure in the table. **A result under 7.0 is not automatically
  a fault in the firmware** — and the last pump-measured year, 2024, is two
  years and a complete overhaul behind us, so there is no recent baseline to
  compare against at all. That gap is a consequence of the lay-up, and it will
  not be closed retrospectively.
- **Do not fit anything to the yearly numbers.** They are averages over as
  little as one fill, they are not evenly weighted, and treating them as eight
  data points invites exactly the error `refuted.md` B9 records with the
  b7 = 133 spike: a summary statistic over a log is not a state the car sits
  in.
- **This bounds the fuel channel only.** It says nothing about
  `TORQUE_CNM_PER_BIT` or the drag line — those are a different quantity
  measured a different way, and the open firmware questions in
  `open.md` are not touched by anything in this file.

---
