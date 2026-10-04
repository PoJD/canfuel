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
