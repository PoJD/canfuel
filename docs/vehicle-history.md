# The vehicle — what it is, what it has done, and what has been changed on it

**This file is the car's record, kept because the firmware's numbers are only
readable against it.** Every fuel figure this project produces is a figure
about *this* engine in *this* state of repair, and several of the arguments
elsewhere in `docs/` lean on facts that had, until now, no written home:
that the car has been chipped, that the plugs are old, that both oxygen
sensors date from the year it was bought.

**It is a permanent document, unlike `engine-health.md` and `next-drive.md`.**
Those two carry an end date and are deleted when their investigation closes.
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

---

## Work done to the fuel and intake tract

**The order is by what it does to the measurement, not by date.** Everything
here is owner-supplied from service records.

| Part | Fitted | Age in distance |
|---|---|---|
| Both oxygen sensors (pre- and post-cat) | **10/2017 — never changed since** | the whole ownership, ~27,600 km |
| Fuel filter | **12/2017 — never changed since** | the whole ownership, ~27,000 km |
| MAF sensor | 7/2018 *(connector cleaned 7/2026)* | not recoverable — see *Distance and use* |
| Chiptuning | 6/2018 | — |
| Fuel pump, Bosch | 10/2022 | ~1,500 km |
| Spark plugs and leads | 12/2022 | **~1,500 km** |
| Ignition coil | 6/2026 | ~0 |
| Throttle body `028 129 748` | 6/2026 — cleaned, new gasket, adaptation run | ~0 |
| Fuel pressure regulator `037 133 035 C` | 7/2026 | ~0 |
| Catalytic converter, silencer, exhaust gaskets | **9/2026** *(previously 10/2017)* | ~0 |
| Injectors `06A 906 031 C`, new from the UK | **9/2026** | ~0 |

Two entries carry more than a date.

**The catalytic converter fitted in 10/2017 was replaced in 9/2026 having been
found completely blocked**, against a service life of nine years and under
28,000 km. `docs/engine-health.md`, *The old converter was shown to the owner*,
is the account of it and treats it as the one hard fact in that investigation.

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
| **Fuel filter, 12/2017** | the oldest fuel-side part and never replaced in ownership. A restricted filter limits rail supply under demand; also by some distance the cheapest item here to eliminate |
| **MAF, 7/2018** | `engine-health.md` rules out a *badly* failing sensor by arithmetic — the volumetric efficiency it implies stays physical — and explicitly **does not** rule out a slightly lazy one. 8 years |
| **Plugs and leads, 12/2022** | **four calendar years but only ~1,500 km.** `engine-health.md` records them as "four years downstream of whatever has been happening", which is true of the dates; the distance is the other half of it and it is small. Old by date, nearly new by wear |
| Pump 10/2022, coil 6/2026, throttle body 6/2026, FPR 7/2026, cat 9/2026, injectors 9/2026 | **effectively new.** Everything that sets rail pressure and injector flow — the two inputs 0x480 depends on — is now a 2026 part |

**The asymmetry is the point.** The car's *delivery* side has been almost
entirely renewed and its *measurement* side — the two lambda sensors and the
MAF — has not been touched in eight or nine years.

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
