# The vehicle — what it is, what it has done, and what has been changed on it

**This file is the car's record, kept because the firmware's numbers are only
readable against it.** Every fuel figure this project produces is a figure
about *this* engine in *this* state of repair, and several of the arguments
elsewhere in `docs/` lean on facts that had, until now, no written home:
that the car has been chipped, that the plugs are old, that both oxygen
sensors date from the year it was bought.

**It is a permanent document, unlike `engine-health.md`.** That one carries
an end date and is deleted when its investigation closes.
This one outlives them: when the investigation ends, the history it was
arguing against is still the history.

⚠ **Provenance — read this before quoting anything below as a measurement.**
The distances and the service dates are the **owner's records**, not
measurements made by this project. The consumption table is measured, but by
the pump rather than by any instrument on the car: litres delivered against
odometer kilometres. Where a figure is derived by this project rather than
recorded, it is marked.

---

## The vehicle

| | |
|---|---|
| Model | VW New Beetle |
| VIN | `WVWZZZ9CZYM601445` |
| Engine | **2.0 l AQY**, 85 kW — ECU `06A 906 018`, labels `06A-906-018-AQY.LBL` |
| Platform | PQ34 |
| Bought | **25 September 2017** at 126,200 km |

The VIN reads consistently with that: positions 7–8 `9C` are the New Beetle
type, position 10 `Y` is model year 2000 and position 11 `M` is Puebla, which
is where New Beetles were built. Positions 4–6 and 9 are VW's filler `Z`s.
That decoding is ISO 3779 structure applied to a VW VIN, so it is a reading
rather than a document — but it agrees with everything else here and nothing
in the project depends on it.

### The masked warning lamp, and the date it stopped mattering

**The car was bought with the engine warning lamp masked inside the instrument
cluster by the previous owner.** The current owner found it and uncovered it
within days of the purchase of 25 September 2017, and **the lamp has worked
normally from that point to the present.** What it had been hiding was a faulty
pre-catalyst oxygen sensor — lit the whole time and impossible to see — which is
the 10/2017 entry in the work table below and the first thing replaced on the
car.

⚠ **The mask bounds the record in one direction only, and running the two
periods together is the error to avoid.** Nothing is known about what the lamp
was reporting **before September 2017**, or for how long, and that gap cannot
be closed retrospectively. **After September 2017 there is no gap**: every
symptom described anywhere in `docs/` is dated inside the ownership and was
observed with a functioning lamp. So "for years" in a symptom description is a
lower bound only where it reaches back past the purchase.

**It is also the strongest argument for the diagnose-before-buying-parts
position `engine-health.md` takes.** A previous owner who covered the lamp
rather than read it means the car arrived carrying an unresolved fault of
unknown age, not a clean sheet.

---

## Distance and use

| | |
|---|---|
| At purchase, 25 Sep 2017 | 126,200 km |
| At 13 Sep 2026 | 154,000 km |
| **Covered in ownership** | **27,800 km over 9.0 years** — a mean of about **3,100 km a year** *(derived)* |

**The mean is the least useful number in that table**, because the distance
was not spread anything like evenly:

| Year | Distance |
|---|---|
| 2023 | 900 km |
| 2024 | 600 km |
| 2025 | **0 km** — laid up, and **deregistered** |
| 2026 | re-registered September |

⚠ **Since the 13 September odometer reading, about 450 km**: a trip to the
Šumava and back, ending 19 September 2026 — two long runs plus about an hour
of touring. **That is an owner-reported distance and not an odometer reading**,
which is why the table above is left alone — and it is also the reason the
fill that ended the trip is not a consumption figure. See *The fill of
2026-09-19* below.

So the tail end of the record is a car that was barely driven and then not
driven at all. **Per-year distance is recorded only for 2023 onwards**; the
26,300 km covered between September 2017 and December 2022 is a single lump
with no breakdown, which is why some of the service items below can be dated
but not given a distance.

Two cross-checks, both of which hold. The 900 + 600 + 0 of the three recorded
years sums to the **~1,500 km since the plugs and leads were changed in
December 2022**, which is a separate record agreeing with this one. And
26,300 km over the first five years is about 5,000 km a year, which is a car
in light but real use — the collapse is recent, not lifelong.

---

## Measured consumption, from the pump

**Litres delivered against odometer kilometres, per year.** This is the only
ground truth this project has for the fuel channel, and it is the reason this
file exists.

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
(`docs/refuel-reset.md`) — and because a litre count is worth keeping even
when it cannot yet be divided by anything.

⚠ **It is not a consumption figure and must not be turned into one.** Neither
the odometer at this fill nor the state of the tank at the previous one was
noted, so the two things the ratio needs are both missing. The ~450 km above
is owner-reported and would give 9.8 l/100 km — **which is arithmetic, not a
measurement**, and it sits in the upper half of a table whose own spread is
45 %. Do not add it as a row.

**What the same fill did measure is the sender**, not the engine:
`docs/refuel-reset.md`, *The 2026-09-19 fill*, has the three numbers and
what they say about the tank scale. That is a different quantity from anything
in this file.

**Next time, the odometer.** The brim-to-brim procedure at the end of this
file is five steps and step 1 is the one that half-happened: the tank was
filled, the reading was not written down. A fill with the odometer beside it,
twice, is the whole of what stands between this project and a real check on
the fuel channel — and the car is now in the state where that check is finally
worth taking.

---

## Work done to the fuel and intake tract

**The order is by what it does to the measurement, not by date.** Everything
here is owner-supplied from service records.

| Part | Fitted | Age in distance |
|---|---|---|
| Both oxygen sensors (pre- and post-cat) | **10/2017 — never changed since** | the whole ownership, ~27,600 km |
| Fuel filter | **12/2017**, and possibly again 10/2022 — see below | 4 or 9 years, **not established** |
| **Fuel filter, new** | **being fitted with the injectors, 9/2026** | ~0 |
| MAF sensor | 7/2018 *(connector cleaned 7/2026)* | not recoverable — see *Distance and use* |
| **MAF sensor, new** | **24/9/2026**, genuine VW `06A 906 461 A`; the 2018 unit is kept | ~0 |
| Chiptuning | 6/2018 | — |
| **Fuel tank** | **replaced inside the ownership, date not recoverable** | unknown — see below |
| Fuel pump, Bosch | 10/2022 | ~1,500 km |
| Spark plugs and leads | 12/2022 *(replaced 9/2026)* | **~1,500 km — see below** |
| Ignition coil | 6/2026 | ~0 |
| Throttle body `028 129 748` | **original, never replaced.** 6/2026: inspected, new gasket, adaptation run. It was already clean, with no carbon, so it had evidently been cleaned at some earlier date nobody recorded | the car's |
| Fuel pressure regulator `037 133 035 C` | 7/2026 | ~0 |
| Catalytic converter, silencer, exhaust gaskets: **everything from the flex pipe to the tail** | **9/2026** *(previously 10/2017)* | ~0 |
| Small hose from the secondary-air combination valve to the intake ahead of the MAF | torn off during the August heater work; fault **16795 / P0411** (secondary air, incorrect flow) photographed **11/8/2026 16:39**, hose refitted that day or a few days after | — |
| **Exhaust manifold** (stainless, double-flow, SSP 233 p. 7) | **original, never replaced** *(owner nearly certain)* | the car's |
| Injectors `06A 906 031 C`, new from the UK | **9/2026** | ~0 |
| **Spark plugs and ignition leads** | **17/9/2026** | ~0 |
| Rear shock absorbers, air-conditioning recharge, minor items | 17/9/2026 | ~0 |

Three entries carry more than a date.

**The catalytic converter fitted in 10/2017 was replaced in 9/2026 having been
found completely blocked**, against a service life of nine years and under
28,000 km. `docs/engine-health.md`, *The old converter was shown to the owner*,
is the account of it and treats it as the one hard fact in that investigation.

**The plugs and leads of 12/2022 came out destroyed at about 1,500 km**, which
is the derived distance in the table above and a fiftieth of what a set of plugs
is normally good for. Eroded electrodes and dry carbon on all four, worse on
cylinders 1 and 4, one visibly worse than the rest. `docs/engine-health.md`,
*The plugs: four years by date, under 1,500 km by wear*, reads them; the short
version is that this is the **second** consumable on this car to be destroyed by
distance it never covered, after the converter directly above.

⚠ **They were replaced separately from the injectors and ahead of them**,
because the injectors were still in transit on the day. How long the gap turned
out to be is not recorded here — add the injectors' own fitting date to the
table above when it happens, and the gap reads off the two dates. That splits a repair the rest of
`docs/` had assumed would be one event, and `engine-health.md` carries what it
costs.

**Compression, measured at the 17/9/2026 visit: 13 bar on all four cylinders**,
even across the engine. *Recorded from the garage, not measured by this
project.* The evenness is the load-bearing part and it eliminates every
per-cylinder mechanical explanation this project had been carrying — a burnt
valve, a broken ring pack, a head gasket leaking between cylinders. It also
agrees, from a completely different measurement, with the volumetric efficiency
`engine-health.md` derives from mass air flow and the ECU's load channel.

**The chiptuning of 6/2018 is the standing unknown.** `engine-health.md`, *The
remap is a standing unknown*, and the warnings in `can-decoding.md` and
`frames.md` about what a remap does to the torque and load channels all
describe this car rather than a hypothetical one. It sits between the 8.8 of
2018 and the 9.9 of 2019 in the table above, which is suggestive and is not
evidence — see below.

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
   through the warm-up enrichment, which `engine-health.md` measures directly
   in *Cold enrichment, measured*. This pushes consumption **up**, so it is a
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
   `engine-health.md`'s fork table is the thing to read here: any `not OK` from
   VCDS blocks 034, 036 or 037 is a **second** failure of an already-replaced
   sensor, and both of these have additionally spent their lives behind a
   converter that was burning through.
5. **The remap, the seasons, the tyres and the driver**, none of which are
   separable in a per-year figure and none of which are worth arguing about at
   this resolution.

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
`engine-health.md`'s **−4.7 % at idle against +1.6 % at part load** are worth
re-reading after the new injectors have some distance on them, and why they
are the first place to look if a tank-to-tank check comes out with a
consistent offset rather than scatter.

### Which parts are old enough to bias the result

Sorted by how directly they sit in the measurement chain:

| Part | Why it matters here |
|---|---|
| **Oxygen sensors, 10/2017** | the largest risk on the list. They set the fuelling, so they move both figures together and are invisible to any comparison of the two. **9 years and the full ownership distance**, behind a failing cat |
| **Fuel filter** | was the oldest fuel-side part on the car and is **being replaced with the injectors**, so it leaves this table on the day. A restricted filter limits rail supply under demand; it was always by some distance the cheapest item here to eliminate, and it is now eliminated |
| **MAF, 7/2018** | `engine-health.md` rules out a *badly* failing sensor by arithmetic — the volumetric efficiency it implies stays physical — and explicitly **does not** rule out a slightly lazy one. 8 years |
| **Plugs and leads, 12/2022** | **four calendar years but only ~1,500 km.** `engine-health.md` records them as "four years downstream of whatever has been happening", which is true of the dates; the distance is the other half of it and it is small. Old by date, nearly new by wear |
| Pump 10/2022, coil 6/2026, FPR 7/2026, cat 9/2026, injectors 9/2026 | **effectively new.** Everything that sets rail pressure and injector flow — the two inputs 0x480 depends on — is now a 2026 part |
| Throttle body, original | **not new, but inspected and found clean in 6/2026.** It meters the idle air, so it is on the idle fault's side of the engine; its condition was seen rather than assumed. An earlier revision of this table listed it as effectively new, and that was wrong |

**The asymmetry is the point, and after next week it is as stark as it can
get.** Two whole sides of this engine will have been renewed and a third has
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
spent those years behind a converter that was burning through. That was where to look next, and `engine-health.md`'s fork table was
what read it: any `not OK` from VCDS blocks 034, 036 or 037 would have been a
**second** failure of an already-replaced sensor. **All three reported OK on
24/9/2026**, and `engine-health.md` argues from them that the sensors are not
what keeps the idle misfiring.

⚠ **The fuel lines are the one thing on the delivery row that stays old**, and
they are named rather than passed over: they run the length of the car, they
are original as far as anything here records, and they sit between a tank of
unknown date and parts that will be a week old.

### The fuel filter's age is two answers and neither is provable

**The service record says 12/2017, right after the purchase.** An email then
shows **another fuel filter bought in 10/2022**, the same month as the Bosch
pump — but the owner believes it was the wrong type and was never fitted, and
there is no record either way.

**So the filter in the car is four years old or nine, and this file cannot
say which.** It is written down as an open pair rather than resolved to the
likelier one, because a service history that quietly rounds its uncertainties
is the thing this file exists not to be.

⚠ **It also stops being worth resolving**, which is the practical part: a new
one goes on with the injectors, so the question becomes historical on the day
it is asked. **What matters is that it was 4 to 9 years old and is not any
more.** If the 10/2022 part turns up in a box unopened, add that here — it
would settle the pair and cost nothing.

**The reason it is being changed is protection, not suspicion.** Nothing
points at the filter and no leak or restriction has been observed. It is
going in because **the filter is the last barrier between nine years of tank
and a set of brand new injector nozzles**, and new injectors behind an old
filter is the one combination on this car where a cheap part can ruin an
expensive one. That it also leaves the measurement chain — the entry above in
*Which parts are old enough to bias the result* — is a consequence and was
not the motive.

### What the 2017 filter looked like coming off — photographed

**`docs/photos/` holds the parts this car has destroyed**, and it exists
because the project has repeatedly regretted evidence that perished.
`engine-health.md`, under *The plugs*, has the amended policy: **the written
judgement is the record and a picture never grades anything** — it is kept so
a later reader can see what was being judged.

| | |
|---|---|
| [`fuel-filter-2017-in-situ.jpg`](photos/fuel-filter-2017-in-situ.jpg) | the filter on the car, 12/2017, before removal |
| [`fuel-filter-2017-removed.jpg`](photos/fuel-filter-2017-removed.jpg) | the can, off |
| [`fuel-filter-2017-drained.jpg`](photos/fuel-filter-2017-drained.jpg) | what drained out of it |
| [`plugs-2026-09-17-removed.jpg`](photos/plugs-2026-09-17-removed.jpg) | the four plugs out at 17/9/2026, after ~1,500 km |

**What they show, as description rather than interpretation.** The can carries
heavy surface corrosion over most of its body, and the joint at the clamp is
wet and stained. **The owner records that it was leaking**, which the staining
is consistent with. What drained out is dark and cloudy rather than clear
petrol — the owner describes it as a black mixture.

⚠ **The filter is the corroded metal can in the middle of the frame**, and
nothing else in the picture is it. Hoses and cables are routed past it and
some of them carry legible markings; **they belong to other parts and say
nothing about this one.** Read the can, the joint and what came out of it.

**The car used to starve under load, and it stopped.** At some point in the
ownership it would **visibly run out of fuel under load** — stop pulling, then
pick up again. **It was the fuel system; which part is not established and is
not worth establishing.** It has not happened for years. *Owner-observed, not
measured, and not dated.*

⚠ **What it bounds is what matters**, and it is the part the post-repair drive
leaned on: the failure mode has a direct observable, the observable has been absent
for years, and the drives that would show it have been driven. **That rules
out gross restriction now** — and not a few per cent under full load.

⚠ **Its age at that point is not known.** It came off in 12/2017, three months
after the purchase, and nothing records when it had last been changed or
whether it ever had. The service history before September 2017 is the gap this
file's *masked warning lamp* section describes.

**This is the precedent under the five-year interval below**, and it turns
that decision from an argument into an argument with a datum behind it: the
last time this car's fuel filter was left past its life, it corroded through
and stopped holding back what it was there to hold back. ⚠ **That rests on the
corrosion and the leak, which are photographed and are unambiguously the
filter** — not on the starvation, which may have been the pump.

### The fuel tank was replaced, and the date is gone

**It was replaced inside the ownership — the owner is certain of that and
cannot date it**, and no record has been found. So it is in the work table
above with the date left open rather than guessed at.

**One thing follows from the filter's own dates.** If the filter now in the
car is the 12/2017 one, then it has run on **both** tanks — it was in place
for however long the original one remained. If the 10/2022 purchase really was
fitted, the overlap is shorter or nothing. **Neither the tank's date nor the
filter's is established, so the order of the two is not either.**

⚠ **This corrects `engine-health.md`, which until now said the tank was the
one part in the chain that had never been touched.** It is not, and that
matters both ways round: an upstream source of contamination may have been
removed years ago, or last year, and the difference decides whether the
candidate root cause in that file still has a source at the time it needs one.
**A date nobody wrote down is what separates the two readings**, so neither is
argued for.

### The filter interval is five years, and it is a decision

**Chosen: five years, on the calendar, regardless of distance.** Chosen over
six, which is the top of the 100,000 km / 5–6 year range the owner found
online, and over any distance-based trigger at all.

⚠ **That range is owner-sourced from the internet and is not a VW schedule**,
so it is context rather than a specification. Nothing here rests on it, because
the reasoning below would reach five years without it.

**Why the calendar and not the odometer.** This car covers **600 to 900 km a
year** (see *Distance and use*), so a 100,000 km trigger is roughly a century
away and would never fire. And it **parks outside**, so the filter body takes
winter from underneath — salt, slush and standing wet — which is a clock that
runs on time and weather rather than on litres pumped through it.

**This is the same argument the rest of this file keeps making**, which is why
it belongs here rather than in a note somewhere. The converter managed nine
years and under 28,000 km. The plugs managed four years and ~1,500 km. **On
this car, consumables are destroyed by time and conditions and not by
distance**, and an interval quoted in kilometres is an interval that never
arrives.

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
   step 1 on its own (`docs/refuel-reset.md`) — so it measures the same tank,
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
  data points invites exactly the error `engine-health.md` warns about with the
  b7 = 133 spike: a summary statistic over a log is not a state the car sits
  in.
- **This bounds the fuel channel only.** It says nothing about
  `TORQUE_CNM_PER_BIT` or the drag line — those are a different quantity
  measured a different way, and the one open question in
  `docs/can-decoding.md` is not touched by anything in this file.

---

## Keeping this current

**Add a row, do not rewrite one.** A service record is worth having because it
is cumulative; a file that only ever describes the present state is a file that
cannot answer "what changed between those two tankfuls", which is the question
this one exists to answer.

Two rules, both borrowed from elsewhere in the project:

- **Distances are derived in one place.** The purchase and current odometer
  readings at the top are the source; every "~1,500 km since" in this file is
  computed from them and from the per-year table, and says so. Do not type a
  second copy of a distance into prose somewhere else — that is the failure
  mode `CLAUDE.md` mechanises `checkdocs.py` against.
- **Mark what is measured.** Pump figures are measured, service dates are
  recorded, and anything this project computes from them is derived. The three
  are not interchangeable.
