# The vehicle — what it is, what it has done, and what has been changed on it

**This file is the car's service record.** What was replaced or
serviced, when, at what distance, with what part, and the distances the
car has covered. Arguments elsewhere in `docs/` lean on these facts —
that the car has been chipped, that the plugs were old, that both oxygen
sensors date from the year it was bought.

**It is the service book and nothing more**: what was replaced or
serviced, when, at what distance, with what part. **How the engine's idle
was investigated — what each job found and what each test showed — is
`idle-log.md`.**

**It is a permanent document, unlike `open.md`.** That one carries
an end date and is deleted when its investigation closes.
This one outlives them: when the investigation ends, the history it was
arguing against is still the history.

⚠ **Provenance — read this before quoting anything below as a measurement.**
The distances and the service dates are the **owner's records**, not
measurements made by this project. Where a figure is derived by this
project rather than recorded, it is marked. **The fuel bought at the pump,
and what it says about the converter's fuel channel, is
`docs/firmware/fuel-check.md`.**

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
position `open.md` takes.** A previous owner who covered the lamp
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
fill that ended the trip is not a consumption figure
(`docs/firmware/fuel-check.md`, *The fill of 2026-09-19*).

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

## Work done to the fuel and intake tract

**The order is by what it does to the measurement, not by date.** Everything
here is owner-supplied from service records.

| Part | Fitted | Age in distance |
|---|---|---|
| Both oxygen sensors (pre- and post-cat) | **10/2017 — never changed since** | the whole ownership, ~27,600 km |
| Fuel filter | **12/2017**, and possibly again 10/2022 — see below | 4 or 9 years, **not established** |
| **Fuel filter, new**, Bosch `0 450 905 318` | **23/9/2026**, with the injectors | ~0 |
| MAF sensor | 7/2018 *(connector cleaned 7/2026)* | not recoverable — see *Distance and use* |
| **MAF sensor, new** | **24/9/2026**, genuine VW `06A 906 461 A`; the 2018 unit is kept. The hose from it to the throttle is held by the owner's own clamps, not VW's: at the MAF **a narrower all-metal clamp since 9/10/2026** (a worm-drive band clamp marked `W2 50-70mm`, *photographed*: `photos/maf-clamp-2026-10-09-*.jpg`) (*until then a rubber-lined pipe clamp*, possibly not seating the hose well — `idle-log.md`, 9/10), a one-screw band clamp at the throttle. Its orientation and the wiggle test: `idle-log.md`, *The MAF* | ~0 |
| Chiptuning, described by the owner as mild | 6/2018 | — |
| Dipstick, dipstick cap and a seal recorded as "těsnění ventilu" (valve seal), **against an oil leak**. *Owner's recollection (27/9/2026), not certain:* the dipstick's narrow neck was cracked and leaking, and the seal was probably the rubber the dipstick seats in — not the valve cover gasket. The record itself is no longer kept | **12/7/2018**, service record | — |
| Timing belt and water pump | **10/2017** | the whole ownership, ~27,800 km |
| **Fuel tank** | **replaced inside the ownership, date not recoverable** | unknown — see below |
| Fuel pump, Bosch | 10/2022 | ~1,500 km |
| Spark plugs and leads | 12/2022 *(replaced 9/2026)* | **~1,500 km — see below** |
| Ignition coil | 6/2026 | ~0 |
| Engine oil (and presumably the filter, not stated) | **6/2026** *(owner-reported, 27/9/2026)*. **Not topped up since**, and on 27/9 the level still read at the **upper mark** on the dipstick despite the valve cover leak | **about 700 km** since the change *(owner's estimate, 27/9/2026: the ~450 km Šumava trip plus several runs to Ústí and back)*; odometer at the change not recorded |
| Throttle body `06A 133 064 H` (VDO `408 237/111/017`) | **original until 2/10/2026**, then replaced (row below; the old part is kept). *Part number read off the label on the part, photographed 26/9/2026; an earlier revision gave `028 129 748`, with no recorded source — possibly the June gasket's number.* 6/2026: inspected, new gasket, adaptation run. It was already clean, with no carbon — only wiped with a cloth — so it had evidently been cleaned at some earlier date nobody recorded | the car's |
| Fuel pressure regulator `037 133 035 C` | 7/2026 | ~0 |
| Catalytic converter, **flex pipe**, silencer, exhaust gaskets: everything from the flex pipe (included) to the tail | **10/9/2026** *(previously 10/2017)*. *Owner-observed, 28/9/2026:* the new front pipe is a **universal part with a blanked-off lambda boss**, and the front probe sits **on the manifold itself**. So the replaced section most likely begins at the manifold's outlet flange, with a new gasket there (*inferred, not confirmed with the garage*) | ~0 |
| Small hose from the secondary-air combination valve to the intake ahead of the MAF | torn off during the August heater work; fault **16795 / P0411** (secondary air, incorrect flow) photographed **11/8/2026 16:39**, hose refitted that day or a few days after | — |
| Heater replacement, dashboard dismantled | **summer 2026, before 11/8** *(owner-reported)*; **the battery was out and disconnected for more than a week** — every ECM adaptation, the throttle's included, started again after it | — |
| **Dipstick guide (orange upper tube), new**, clipped onto the original metal tube, held by a home-made sheet-metal bracket bolted to the head (thread-locked) with cable ties, the bracket bent to press the guide down onto the tube after the smoke test showed its seat leaking (as finally fitted: `photos/dipstick-2026-10-09-final.jpg`). The old guide was not this engine's part — bent the other way, its mounting tab about 2 cm lower (*compared side by side, photographed*: `photos/dipstick-2026-10-09-old-vs-new-*.jpg`) — and the original bracket was missing | **9/10/2026**, by the owner (*photographed*: `photos/dipstick-2026-10-09-*.jpg`) | ~0 |
| **Exhaust joint behind the converter**, remade: new two-bolt sleeve connector and exhaust sealant, replacing the garage's sealant-filled joint of 10/9 (slotted sleeve, band clamp, pressed half-shells). The pipe behind is about 1 mm narrower, so a little play remains | **9/10/2026**, by the owner (*photographed*: `photos/exhaust-joint-2026-10-09-*.jpg`) | ~0 |
| **Exhaust manifold** (stainless, double-flow, SSP 233 p. 7) | **original, never replaced** *(owner nearly certain)* | the car's |
| Injectors `06A 906 031 C` / Bosch `0 280 155 791`, new from the UK | delivered 22/9, **fitted 23/9/2026** by the owner, three of the four not fully home in the manifold until refitted on 1/10/2026 (`idle-log.md`) | ~0 |
| Upper intake manifold gasket, **Elring `271.230`** (sold as the equivalent of VW `06A 129 717`; the parts shop matched it to the VIN) | **9/2026, twice** *(owner, 1/10/2026)*: **17/9 at the garage** with the plugs, and **23/9 by the owner** with the injectors; packaging dated 17/9/2026 (Carvo s.r.o.) — *read off the photographed packaging*. *This row used to give one fitting, by the owner.* The 23/9 one came off whole on 1/10/2026 and **a third new one went on 2/10/2026** (*The valve cover and throttle job*, below) | ~0 |
| **Throttle body, new**, Pierburg `7.03703.13.0` (cross-referenced to `06A 133 064 H`, without cruise control), with a new flange gasket | **2/10/2026**, by the owner; 098 *ADP OK* | ~0 |
| **Valve cover gasket** Elring `325.070` — ⚠ **the wrong part, for another engine; off again 3/10/2026** (`idle-log.md`, *The wrong gasket*) —, **crankcase breather** Febi `32452` (its ring fitted), **filler cap ring** Febi `100690` (= `06A 103 483 D`), sealant Elring `030.793` | **2/10/2026**, by the owner | ~0 |
| **Valve cover gasket, the right one**, Elring `915.653` (listed for AQY; solid half-moons, metal sleeves), on Dirko Elring `030.793`, with a new upper plenum gasket Elring `271.230` | **4/10/2026**, by the owner | ~0 |
| Injectors' air-shroud line: **new 8 mm sleeves** on the rigid pipe | **1/10/2026**, by the owner | ~0 |
| Throttle vacuum elbow `06A 133 374` (tee to the throttle's top spigot) — **replaced by a longer plain hose**, the new throttle's spigot pointing the other way | **2/10/2026**, by the owner; the old elbow is kept | ~0 |
| **Spark plugs and ignition leads**, NGK leads | **17/9/2026**, at the Dakuma garage | ~0 |
| Rear shock absorbers, air-conditioning recharge, minor items | 17/9/2026 | ~0 |

Three entries carry more than a date.

**The catalytic converter fitted in 10/2017 was replaced in 9/2026 having been
found completely blocked**, against a service life of nine years and under
28,000 km. **Cracked outside, blocked inside, and one chamber burned right
through**, as shown to the owner — the one hard fact of the engine
investigation. A few per cent of rich trim does not melt a substrate; burning
through takes raw unburnt fuel igniting inside it, which means misfire rather
than enrichment (*general knowledge*).

**The plugs and leads of 12/2022 came out destroyed at about 1,500 km**, which
is the derived distance in the table above and a fiftieth of what a set of plugs
is normally good for. Eroded electrodes and dry carbon on all four, one visibly worse than the
rest; the ranking is the owner's, from handling them, and not the
photograph's. **Which cylinder any plug came from is not known** — the garage
did not label them. *Corrected 28/9/2026:* this said "worse on cylinders 1
and 4" until then, a pair nothing recorded. This is the **second** consumable on this car to be destroyed by
distance it never covered, after the converter directly above.

⚠ **They were replaced separately from the injectors and ahead of them**,
because the injectors were still in transit on the day: plugs and leads on
17/9, injectors on 23/9/2026. That splits a repair the rest of
`docs/` had assumed would be one event, and it cost the post-repair drive its
single variable.

**Compression, measured at the 17/9/2026 visit: 12 bar on all four cylinders**
(earlier revisions said 13, which was misremembered),
even across the engine. *Recorded from the garage, not measured by this
project.* The evenness is the load-bearing part and it eliminates every
per-cylinder mechanical explanation this project had been carrying — a burnt
valve, a broken ring pack, a head gasket leaking between cylinders. It also
agrees, from a completely different measurement, with the volumetric efficiency
`docs/firmware/frames.md` derives from mass air flow and the ECU's load channel (84–93 %).

**The chiptuning of 6/2018 is the standing unknown.** The tuner's own remark
was that there was nothing to be had at the top of the range; the car is not
going back to standard. The warnings in `docs/firmware/can-decoding.md` and
`docs/firmware/frames.md` about what a remap does to the torque and load channels all
describe this car rather than a hypothetical one. The owner describes the remap
as mild. It sits between the 8.8 of
2018 and the 9.9 of 2019 in the table above, which is suggestive and is not
evidence — see below.

### The valve cover and throttle job, 1–4/10/2026

By the owner, at home. The parts are the rows above dated 1/10, 2/10 and
4/10/2026; what the job found, the wrong gasket of 2/10 and the sessions
that followed are in `idle-log.md` (*Appendix — the job of 1–4/10 in
detail*).

---

## Electrical work, 2026

*Owner-supplied; days not recorded.*

| Part | Fitted | Why |
|---|---|---|
| **Battery, new** | **end of August 2026**, with the headlights | the old one was found dead during the headlight work |
| Headlights, complete: ALKAR `2741128` left / `2742128` right (H1 dipped, H1 main, W5W, levelling motor) | **end of August 2026** | the old reflectors had degraded and water was getting in |
| Light switch, Herth+Buss Elparts, replacing the original `1C0 941 531 A` | **September 2026** | 0.3–0.7 V was being lost across the old switch |

**The measurements that led to the switch**, differential and under load,
are the only voltage-drop figures this project holds for the car, and
`open.md` H4 reads them against the engine's earth. In short: 0.9 V lost at
the dipped-beam bulb (1.6–1.9 V with main beam), **all on the positive side**;
the lamp earth 0.1–0.2 V; the battery terminals **0.000 V (+) and
0.002 V (−)**, recently cleaned — on the new battery, fitted during that same
work. About half the loss sat before the fuse box
(a steady ~0.09 Ω), mostly in the old switch. After the new switch the
dipped beam loses 0.2 V across it (0.6 V with main beam, the same 0.04 Ω —
so the rest is on the switch's shared input side, not its contacts), and
roughly 0.45 V remains at the bulb, in the switch feed and the run from the
fuse box to the lamp. **Left as it is, by decision**; a relay harness is the
complete fix if it is ever wanted.

**The alternator**, read off its label on 26/9/2026 (*owner photo*): Bosch
`0 124 325 003`, VW `028 903 028 D`, **14 V 90 A**, date code 17/99, made in Spain — so most likely the one
the car left the factory with, 26 years old. With headlights, rear window
heater and blower on it holds 12.72 V at idle and 13.4 V at roughly
2000–3000 rpm (`open.md` H4). The B+ nut took a slight further turn when
checked; the cable eyelet under it is in place, with some surface corrosion
at its edge.

**The chafed main positive cable at the battery** — bare strands visible
under its heat-shrink — was wrapped in PVC tape on 26/9/2026 (*owner*). The
strands looked sound; the concern was moisture getting in. A tape wrap keeps
water off, not out of strands that are already wet, so it is a stop-gap.

---

## The fuel system — the filter, the tank and the interval

### The fuel filter's age is two answers and neither is provable

**The service record says 12/2017, right after the purchase.** An email then
shows **another fuel filter bought in 10/2022**, the same month as the Bosch
pump — but the owner believes it was the wrong type and was never fitted, and
there is no record either way.

**So the filter in the car is four years old or nine, and this file cannot
say which.** It is written down as an open pair rather than resolved to the
likelier one, because a service history that quietly rounds its uncertainties
is the thing this file exists not to be.

⚠ **It also stopped being worth resolving**, which is the practical part: a new
one went on with the injectors on 23/9/2026, so the question is historical. **What matters is that it was 4 to 9 years old and is not any
more.** If the 10/2022 part turns up in a box unopened, add that here — it
would settle the pair and cost nothing.

**The reason it was changed is protection, not suspicion.** Nothing
points at the filter and no leak or restriction has been observed. It is
went in because **the filter is the last barrier between nine years of tank
and a set of brand new injector nozzles**, and new injectors behind an old
filter is the one combination on this car where a cheap part can ruin an
expensive one. That it also leaves the measurement chain — the entry above in
*Which parts are old enough to bias the result* — is a consequence and was
not the motive.

### What the 2017 filter looked like coming off — photographed

**`docs/engine-health/photos/` holds the parts this car has destroyed**, and it exists
because the project has repeatedly regretted evidence that perished.
The policy: **the written
judgement is the record and a picture never grades anything** — it is kept so
a later reader can see what was being judged.

| | |
|---|---|
| [`fuel-filter-2017-in-situ.jpg`](photos/fuel-filter-2017-in-situ.jpg) | the filter on the car, 12/2017, before removal |
| [`fuel-filter-2017-removed.jpg`](photos/fuel-filter-2017-removed.jpg) | the can, off |
| [`fuel-filter-2017-drained.jpg`](photos/fuel-filter-2017-drained.jpg) | what drained out of it |
| [`plugs-2026-09-17-removed.jpg`](photos/plugs-2026-09-17-removed.jpg) | the four plugs out at 17/9/2026, after ~1,500 km |
| [`cover-leak-2026-10-03-cyl4-end.jpg`](photos/cover-leak-2026-10-03-cyl4-end.jpg) | the new cover gasket leaking at cylinder 4's end, 3/10/2026, on the first warm run — kept because cleaning the oil off destroys it |
| [`cover-leak-2026-10-03-below.jpg`](photos/cover-leak-2026-10-03-below.jpg) | the same leak, the oil below it |
| [`cover-leak-2026-10-03-bracket.jpg`](photos/cover-leak-2026-10-03-bracket.jpg) | the wiring-loom bracket under the cover's hold-down strip at that end |
| [`cover-gasket-old-halfmoon.jpg`](photos/cover-gasket-old-halfmoon.jpg) | the gasket that came off on 1/10: a solid half-moon |
| [`cover-gasket-old-halfmoon-edge.jpg`](photos/cover-gasket-old-halfmoon-edge.jpg) | the same half-moon from its edge, ribbed all round |
| [`cover-gasket-325070-open-arch.jpg`](photos/cover-gasket-325070-open-arch.jpg) | Elring `325.070`, the wrong part: an open arch at the same place |
| [`cover-gasket-325070-open-arch-2.jpg`](photos/cover-gasket-325070-open-arch-2.jpg) | the same arch from another side |
| [`cover-gasket-325070-profile.jpg`](photos/cover-gasket-325070-profile.jpg) | `325.070`'s taller ribbed section |
| [`cover-gasket-915653-halfmoon.jpg`](photos/cover-gasket-915653-halfmoon.jpg) | Elring `915.653`, the right part, 4/10/2026: a solid half-moon and a sleeved bolt hole |
| [`cover-gasket-915653-whole.jpg`](photos/cover-gasket-915653-whole.jpg) | the same gasket whole, beside the new upper plenum gasket |
| [`cover-gasket-915653-label.jpg`](photos/cover-gasket-915653-label.jpg) | its package label: `915.653`, Elring Germany |
| [`cover-leak-2026-10-04-cleaned.jpg`](photos/cover-leak-2026-10-04-cleaned.jpg) | the coil, its leads and the harness after the worst of the oil was cleaned off, 4/10/2026 |
| [`cover-on-2026-10-04-belt-end.jpg`](photos/cover-on-2026-10-04-belt-end.jpg) | `915.653` fitted, the cover on: the joint at the timing-belt end, 4/10/2026 |
| [`cover-on-2026-10-04-halfmoon.jpg`](photos/cover-on-2026-10-04-halfmoon.jpg) | the same, a solid half-moon in place at the end of the head |
| [`cover-on-2026-10-04-strip.jpg`](photos/cover-on-2026-10-04-strip.jpg) | a hold-down strip and its nut on the refitted cover |
| [`cover-on-2026-10-04-bracket.jpg`](photos/cover-on-2026-10-04-bracket.jpg) | the side bracket and harness at the refitted cover |
| [`plenum-on-2026-10-04.jpg`](photos/plenum-on-2026-10-04.jpg) | the engine reassembled, plenum on, 4/10/2026 |
| [`plug-well-cyl4-2026-10-09.png`](photos/plug-well-cyl4-2026-10-09.png) | down cylinder 4's plug well: dark, uneven patches on the plug's terminal and a smudge on its hex (*owner*: seen 1/10/2026, would not come off with petrol); sent 9/10/2026 |
| [`plug-well-2026-10-09-b.png`](photos/plug-well-2026-10-09-b.png), [`-c`](photos/plug-well-2026-10-09-c.png), [`-d`](photos/plug-well-2026-10-09-d.png) | the other three plug wells, cylinder not recorded; `-d` too dark to judge |

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

⚠ **This corrects an earlier revision of the engine investigation, which said
the tank was the one part in the chain that had never been touched.** It is not, and that
matters both ways round: an upstream source of contamination may have been
removed years ago, or last year, and the difference decides whether the
candidate root cause (`refuted.md` A14) still has a source at the time it needs one.
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

---

## Keeping this current

**Add a row, do not rewrite one.** A service record is worth having because it
is cumulative; a file that only ever describes the present state is a file that
cannot answer "what changed between those two dates", which is the question
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
