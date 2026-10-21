# The vehicle — what it is, what it has done, and what has been changed on it

**The car's service book and nothing more**: what was replaced or
serviced, when, at what distance, with what part. How the idle was
investigated — what each job found and each test showed — is
`idle-log.md`; what is still open is `open.md`, what is settled
`refuted.md`. **A permanent document**: it outlives `open.md`.

The full previous version, with the reasoning since moved out:
`git show d327332:docs/engine-health/vehicle-history.md`.

⚠ **Provenance.** Distances and service dates are the **owner's
records**, not measurements by this project; anything derived here is
marked *(derived)*. The fuel bought at the pump is
`docs/firmware/fuel-check.md`.

---

## The vehicle

| | |
|---|---|
| Model | VW New Beetle |
| VIN | `WVWZZZ9CZYM……` — **the serial deliberately left out** of this public repository (*owner's decision*, 12/10/2026). `9C` New Beetle, `Y` model year 2000, `M` Puebla (ISO 3779 structure, a reading rather than a document) |
| Engine | **2.0 l AQY**, 85 kW — ECU `06A 906 018`, labels `06A-906-018-AQY.LBL` |
| Platform | PQ34 |
| Bought | **25 September 2017** at 126,200 km |

**The engine warning lamp was masked inside the cluster by the previous
owner.** Uncovered within days of the purchase; it has worked normally
since. It had been hiding a faulty pre-cat oxygen sensor (10/2017,
below). Nothing is known of what it reported before 9/2017; every
symptom in `docs/` is dated after it, with a working lamp.

---

## Distance and use

| | |
|---|---|
| At purchase, 25 Sep 2017 | 126,200 km |
| At 13 Sep 2026 | 154,000 km |
| **Covered in ownership** | **27,800 km over 9.0 years**, about 3,100 km a year *(derived)* |

Odometer at the start of each year, from the owner's expense sheet
(round readings, *owner*, 20/10/2026):

| When | Odometer | Covered *(derived)* |
|---|---|---|
| 9/2017 | 126,200 km | — |
| 2/2018 | 135,000 km | 8,800 km in the first five months |
| 2/2019 | 139,000 km | 4,000 km in 2018 |
| 1/2020 | 142,000 km | 3,000 km in 2019 |
| 1/2022 | 152,000 km | 10,000 km over 2020–2021 |
| 1/2023 | 152,900 km | 900 km in 2022 |
| 1/2024 | 153,500 km | — |

| Year | Distance |
|---|---|
| 2023 | 900 km |
| 2024 | 600 km |
| 2025 | **0 km** — laid up, and **deregistered** |
| 2026 | re-registered September |

The 900 + 600 + 0 of 2023–2025 agrees with the **~1,500 km since the
plugs and leads of 12/2022** *(derived)*.

⚠ **Since the 13/9/2026 reading**: about 450 km to the Šumava and back,
ending 19/9/2026 (*owner-reported, not an odometer reading*), then the
investigation's drives (24/9, 25/9 about 100 km of motorway, 3/10, 4/10,
9/10, 10/10 and later). **No odometer reading taken since**; the next one
goes in the first table.

---

## Service entries from the owner's expense sheet, 2018–2026

*Owner's records; descriptions as he wrote them, makes not stated unless
given.*

| Date | Entry | Where |
|---|---|---|
| 20/6/2018 | service: A/C, **plugs, leads**, radiator, exhaust repair | a garage |
| 30/6/2018 | chiptuning (below) | the tuner |
| 6/7/2018 | **new MAF** | — |
| 12/7/2018 | dipstick, cap and a seal, against an oil leak (work table) | service record |
| 31/8/2018 | A/C, STK, **the intake looked at: no fault found; compression about 13 bar** (below) | Dakuma |
| 10/10/2018 | oil and oil filter (long-life) | — |
| 9/1/2020 | service: oil, **plugs**, boots, track-rod ends, **battery, thermostat** | Spei |
| 10/8/2021 | annual service: arms, brakes, oil, **decarbonisation** (what kind is not recorded), filters | Spei |
| 16/8/2022 | oil, STK, brake cleaning | Dakuma |
| 22/12/2022 | **plugs and leads, NGK** (invoice) | Dakuma |
| 15/6/2026 | oil and filter, the old fuel drained | the owner |
| 25/6/2026 | new ignition coil | — |
| 17/9/2026, 10/10/2026 | plugs and leads, NGK | Dakuma, then the owner |

**Plugs changed five times in the ownership, leads four**: 6/2018,
1/2020 (plugs only), 12/2022, 9/2026, 10/2026. The owner believes every
set was NGK; it is proven for 12/2022 and both sets of 2026, and 6/2018 and
1/2020 are to be checked against theirs.

---

## Work done to the engine, fuel and intake tract

Rows of September and October 2026 in the order the work was done.
Owner-supplied from service records or from his own work.

| Part | Fitted | Age in distance |
|---|---|---|
| Both oxygen sensors (pre- and post-cat) | **10/2017 — never changed since** | ~27,600 km |
| Timing belt and water pump | **10/2017** | ~27,800 km |
| Fuel filter | **12/2017**; another bought 10/2022, believed the wrong type and never fitted (no record either way) | 4 or 9 years, **not established** |
| Chiptuning, described by the owner as mild | 6/2018 — **confirmed by the original order email** (*owner*, 12/10/2026). The tuner kept the original map; writing it back was set for 22/10/2026 and is **postponed** (`plan.md` 5a). *This said "the car is not going back to standard" until 12/10* | — |
| MAF sensor | 7/2018 *(connector cleaned 7/2026)* | not recoverable |
| Dipstick, cap and a seal recorded as "valve seal", against an oil leak. *Owner's recollection (27/9/2026), not certain:* the dipstick's neck was cracked; the seal probably the rubber it seats in, not the valve cover gasket. Record not kept | **12/7/2018** | — |
| **Fuel tank** | **replaced inside the ownership, date not recoverable** (*owner certain*). *An earlier revision said the tank had never been touched* | unknown |
| Fuel pump, Bosch | 10/2022 | ~1,500 km |
| Spark plugs and leads, **NGK both** (Dakuma invoice, 22/12/2022, no part numbers; not kept here, it carries the owner's name and plate) | 12/2022 *(replaced 9/2026)* | ~1,500 km — came out destroyed (below) |
| Ignition coil | 6/2026 | ~0 |
| Engine oil (filter presumably, not stated) | **6/2026**. Not topped up since; at the upper mark on 27/9/2026 | about 700 km to 27/9 (*owner's estimate*); odometer at the change not recorded |
| Throttle body `06A 133 064 H` (VDO `408 237/111/017`) | **original until 2/10/2026** (kept). 6/2026: inspected, already clean, new gasket, adaptation run. *Part number read off the label, photographed 26/9/2026; an earlier revision gave `028 129 748`, unsourced* | the car's |
| Fuel pressure regulator `037 133 035 C`, **3 bar** printed on it (*read off the part*, 10/10/2026) | 7/2026 | ~0 |
| Heater replacement, dashboard dismantled | **summer 2026, before 11/8**; **battery out for more than a week**, every ECM adaptation restarted | — |
| Small hose, secondary-air combination valve to the intake ahead of the MAF | torn off in the heater work; fault **16795 / P0411** photographed **11/8/2026 16:39**; refitted that day or a few days after | — |
| Catalytic converter, **flex pipe**, silencer, exhaust gaskets: flex pipe to the tail | **10/9/2026** *(previously 10/2017)*; the old converter found blocked (below). The new front pipe is universal; its lambda boss, **ahead of the converter, behind the front probe**, is closed by **an old lambda probe with its leads cut off short** (`photos/exhaust-blanked-boss-2026-10-12.jpg`; *this said only "blanked-off" until the photo*). The front probe sits **on the manifold**. The manifold-to-front-pipe joint **remade by the garage in this work**, and once before (date not recorded). Rear probe cable re-routed and tied up by the owner 12/10/2026 (`photos/rear-probe-2026-10-12.jpg`, `photos/exhaust-joint-2026-10-12-on-4.jpg`); the converter `photos/converter-2026-10-12.jpg` | ~0 |
| Rear shock absorbers, A/C recharge, minor items | 17/9/2026 | ~0 |
| Upper intake manifold gasket, **Elring `271.230`** (= VW `06A 129 717`, matched to the VIN by the shop) | **17/9/2026 at the garage**, then **23/9 by the owner**; packaging dated 17/9/2026, Carvo s.r.o. (*read off the photo*). *This row used to give one fitting.* New ones again 2/10, 4/10 and 10/10 (rows below) | ~0 |
| **Spark plugs and ignition leads**: NGK `BKUR6ET-10` plugs (*read off one on removal*, `photos/plug-old-2026-10-10-type.jpg`); NGK leads, grey, printed *"NGK SPARK PLUG CABLE"*, *"5ME2"* (`photos/cover-leak-2026-10-04-cleaned.jpg`) | **17/9/2026**, Dakuma; **off 10/10/2026**, kept numbered | ~0 |
| **Compression, 17/9/2026: 12 bar on all four** (*garage-recorded*; *earlier revisions said 13, misremembered*) | — | — |
| Injectors `06A 906 031 C` / Bosch `0 280 155 791`, new from the UK | delivered 22/9, **fitted 23/9/2026** by the owner; three not fully home until refitted 1/10/2026 (`idle-log.md`) | ~0 |
| **Fuel filter, new**, Bosch `0 450 905 318` | **23/9/2026**, with the injectors | ~0 |
| **MAF sensor, new**, genuine VW `06A 906 461 A` (the 2018 unit kept). Hose to the throttle on the owner's clamps: at the MAF a rubber-lined pipe clamp, **since 9/10/2026 a worm-drive band clamp `W2 50-70mm`** (`photos/maf-clamp-2026-10-09-*.jpg`); a one-screw band clamp at the throttle | **24/9/2026** (`idle-log.md`, *The MAF*) | ~0 |
| Injectors' air-shroud line: **new 8 mm sleeves** on the rigid pipe | **1/10/2026**, by the owner | ~0 |
| **Throttle body, new**, Pierburg `7.03703.13.0` (cross-referenced to `06A 133 064 H`, without cruise control), new flange gasket | **2/10/2026**, by the owner; 098 *ADP OK* | ~0 |
| Throttle vacuum elbow `06A 133 374` — **replaced by a longer plain hose**, **8 mm bore**, on a tee whose other thin leg takes 6 mm (*owner*, 12/10/2026); the old elbow kept | **2/10/2026**, by the owner | ~0 |
| **Valve cover gasket** Elring `325.070` — ⚠ **the wrong part, for another engine; off again 3/10/2026** —, **crankcase breather** Febi `32452` (its ring fitted), **filler cap ring** Febi `100690` (= `06A 103 483 D`), sealant Elring `030.793` | **2/10/2026**, by the owner | ~0 |
| **Valve cover gasket, the right one**, Elring `915.653` (listed for AQY), on Dirko Elring `030.793`, with a new Elring `271.230` plenum gasket | **4/10/2026**, by the owner | ~0 |
| **Dipstick guide (orange upper tube), new**, clipped onto the original metal tube, held by a home-made sheet-metal bracket bolted to the head (thread-locked) and cable ties (`photos/dipstick-2026-10-09-final.jpg`). The old guide was not this engine's part — bent the other way, tab about 2 cm lower (`photos/dipstick-2026-10-09-old-vs-new-*.jpg`) — and the original bracket was missing | **9/10/2026**, by the owner (`photos/dipstick-2026-10-09-*.jpg`) | ~0 |
| **Exhaust joint behind the converter**, remade: two-bolt sleeve connector (55 mm) and exhaust sealant, replacing the garage's joint of 10/9. Pipes **54.2 mm** from the converter, **55.0 mm** behind (*owner-measured*, 12/10/2026; *this said the reverse until then*). **Remade again 12/10/2026**: a strip of the old connector, probably galvanised, as a shim round the narrower pipe, sealant under and over, the connector refitted | **9/10/2026** (`photos/exhaust-joint-2026-10-09-*.jpg`); **12/10/2026** (`photos/exhaust-joint-2026-10-12-*.jpg`), by the owner | ~0 |
| **Spark plugs and ignition leads, new**: NGK `BKUR6ET-10` at 25–30 Nm (*NGK box*); NGK `RC-VW254` leads, black, printed *"5MB"* (`photos/leads-new-2026-10-10-*.jpg`). New Elring `271.230` under the plenum. Battery left connected | **10/10/2026**, by the owner | ~0 |
| **Air filter element, new**, Bosch **`S 3714`** = `1 457 433 714` (`photos/air-filter-new-2026-10-12-label.jpg`), replacing one of **1/2023** (*owner's records*; old element `photos/air-filter-old-2026-10-12-*.jpg`). The car stands outdoors all year. **Airbox `1C0 129 607 A`** (element `1J0 129 620`, Mann `C37153`, *read off the lid*, `photos/airbox-2026-10-12-label.jpg`) **found cracked** on the filtered side ahead of the MAF; sealed with putty inside and out, a stopgap (`photos/airbox-crack-2026-10-12-sealed.jpg`, `-sealed-outside.jpg`, `photos/airbox-2026-10-12-detail.jpg`, `photos/airbox-2026-10-12-outlet-maf.jpg`) | **12/10/2026**, by the owner | ~0 |
| Valve cover nuts **re-tightened**: loosened about 90° to a full turn, all eight tightened with the plenum on | **12/10/2026**, by the owner | ~0 |
| **Exhaust manifold** (stainless, double-flow, SSP 233 p. 7) | **original, never replaced** (*owner*: rusty outside; a hole cannot be told from below). `photos/manifold-2026-10-12-*.jpg`, `photos/exhaust-flange-2026-10-12-below-*.jpg` | the car's |
| **Idle speed adaptation**, 01 channel 01 (login 01283; `vcds.md`) | **128 = 780 rpm, as found 12/10/2026** (`photos/vcds-idle-adapt-2026-10-12-*.jpg`); raised to **133 = 830 rpm** (the most accepted) and **put back to 128** the same day (*owner*; `refuted.md` D9) | — |
| **Borescope look**: plenum off; inlet ports through the runners, chambers through the plug holes; plugs out and back hand-tight. **Lead 2's plug end tore** on removal. Injector 4's peeling harness tape renewed, the wires whole. **Clean amber oil on every plug thread** (`photos/plug-2026-10-20-cyl*.jpg`). Nothing cleaned. **Ordered from VW, arriving 21/10**: leads `06A 905 409 L`, plugs `101 000 033 AA`; plenum gasket Elring `271.230` (VW `06A 129 717` out of production). A row of their own once fitted | **19–20/10/2026**, by the owner | ~0 |
| **Spark plugs and ignition leads, VW**: plugs `101 000 033 AA`, whose box reads **"NGK BKUR6ET-10"** — the same plug as the set of 10/10, made in Japan, printed VW/Audi and NGK in black and stamped with the VW number (`photos/plug-vw-2026-10-21-*.jpg`; the 10/10 plug beside one, printed *NGK R* in blue, `photos/plug-ngk-old-vs-vw-2026-10-21.jpg`). Leads `06A 905 409 L` (`photos/leads-vw-2026-10-21-*.jpg`), **much stiffer to the touch** than the NGK `RC-VW254`, and **each plug end has a small rubber ring inside** where it seats on the plug, which the NGK ends do not have (*owner*; the inside of each, `photos/lead-end-vw-2026-10-21-inside.jpg`, `photos/lead-end-ngk-old-2026-10-21-inside.jpg`). Plugs fitted first, then the leads, 1, 4, 2, 3 clockwise from the coil's top tower, routed clear of the plenum (`photos/refit-2026-10-21-ports-covered.jpg`); every end clicked and sits with no play (*owner*) | **21/10/2026**, by the owner, bought from VW the same day | ~0 |
| **Fuel: OMV MaxxMotion 100**, always (*owner*, 10/10/2026). Before 9/2017 not known. **Until summer 2026 the tank held fuel about three years old** | since 9/2017 | ~27,800 km |
| **Battery disconnected** (every ECM adaptation restarts) | after the summer heater work, then **23/9, 26/9, 1–2/10 and the morning of 4/10/2026**; 098 run 2/10 and 4/10. **Connected since 4/10** | — |

### Notes to the table

**The converter of 10/2017 came off blocked, 9/2026**: cracked outside,
blocked inside, one chamber burned right through (as shown to the
owner), after nine years and under 28,000 km.

**The plugs and leads of 12/2022 came out destroyed at ~1,500 km**:
eroded electrodes and dry carbon on all four, one visibly worse (*the
owner's ranking, by hand*). Which cylinder each came from is not known —
the garage did not label them. *This said "worse on cylinders 1 and 4"
until 28/9/2026, a pair nothing recorded.* Replaced 17/9, ahead of the
injectors of 23/9.

**Compression**: about **13 bar, 31/8/2018** (Dakuma invoice, found
20/10/2026: "the engine's air path without apparent fault", "engine
compression about 13 bar", no per-cylinder figures; invoice not kept, it
carries name, address and plate), and **12 bar on all four, 17/9/2026**
— different gauges and garages. What it rules out is `refuted.md` A4.

**The valve cover and throttle job, 1–4/10/2026**: the rows dated 1/10,
2/10 and 4/10. What it found is `idle-log.md`, *Appendix — the job of
1–4/10 in detail*.

---

## Fault memory, as found in old scans

*Owner's VCDS scans, found 10/10/2026; the dates are the owner's.*

| When | Stored | Since |
|---|---|---|
| **1/2018** | 16824 / P0440, EVAP emission control system, intermittent | **never repaired**; not stored since |
| **5/2019** | 16556 / P0172, fuel trim too rich; 16684 / P0300, random/multiple misfire; **16688 / P0304, cylinder 4 misfire** — all intermittent | not stored since |

Scans: `photos/vcds-faults-2018-01.png`, `photos/vcds-faults-2019-05.png`.

---

## Electrical work, 2026

*Owner-supplied; days not recorded.*

| Part | Fitted | Why |
|---|---|---|
| **Battery, new** | **end of August 2026** | the old one found dead in the headlight work |
| Headlights, complete: ALKAR `2741128` left / `2742128` right (H1 dipped, H1 main, W5W, levelling motor) | **end of August 2026** | reflectors degraded, water getting in |
| Light switch, Herth+Buss Elparts, replacing the original `1C0 941 531 A` | **September 2026** | 0.3–0.7 V lost across the old switch |
| Chafed main positive cable at the battery, wrapped in PVC tape (a stop-gap) | **26/9/2026**, by the owner | bare strands under the heat-shrink |

**Voltage drops measured before the switch** (differential, under
load): 0.9 V at the dipped-beam bulb (1.6–1.9 V with main beam), all on
the positive side; lamp earth 0.1–0.2 V; battery terminals 0.000 V (+)
and 0.002 V (−) on the new battery; about half the loss before the fuse
box (~0.09 Ω). **After**: 0.2 V across the switch (0.6 V with main beam),
about 0.45 V remaining at the bulb. Left as it is, by decision. Read
against the engine's earth in `open.md` H4.

**The alternator** (label, 26/9/2026): Bosch `0 124 325 003`, VW
`028 903 028 D`, **14 V 90 A**, date code 17/99, made in Spain — most
likely the original. With headlights, rear window heater and blower on:
12.72 V at idle, 13.4 V at about 2000–3000 rpm. The B+ nut took a slight
further turn; eyelet in place, some surface corrosion at its edge.

---

## The fuel system

**The fuel filter**: 12/2017, or a 10/2022 one if that was fitted after
all (believed not) — so 4 or 9 years old until **replaced 23/9/2026** as
protection for the new injectors, not on suspicion. If the 10/2022 part
turns up unopened, that settles it. The 2017 one was **leaking** at the
clamp (*owner*), heavily corroded, and drained a dark, cloudy "black
mixture" (photos below; the filter is the corroded can in the middle of
the frame, the markings on hoses around it belong to other parts). Its
age when removed is not known.

**At some time in the ownership the car ran out of fuel under load** —
stopped pulling, then picked up. A fuel-system fault, the part not
established; not seen for years (*owner, not dated*).

**The fuel tank** was replaced in the ownership, date unknown (work
table). Whether the 2017 filter ran on both tanks is therefore not known
either.

**Filter interval: five years on the calendar, regardless of distance —
a decision**, over six (the top of a 100,000 km / 5–6 year range the
owner found online, not a VW schedule) and over any distance trigger: the
car covers a few hundred km a year and parks outside.

---

## Photographs

`docs/engine-health/photos/`. **The written judgement is the record**; a
picture is kept so a later reader can see what was judged.

| | |
|---|---|
| [`fuel-filter-2017-in-situ.jpg`](photos/fuel-filter-2017-in-situ.jpg) | the filter on the car, 12/2017, before removal |
| [`fuel-filter-2017-removed.jpg`](photos/fuel-filter-2017-removed.jpg) | the can, off |
| [`fuel-filter-2017-drained.jpg`](photos/fuel-filter-2017-drained.jpg) | what drained out of it |
| [`plugs-2026-09-17-removed.jpg`](photos/plugs-2026-09-17-removed.jpg) | the four plugs out at 17/9/2026, after ~1,500 km |
| [`cover-leak-2026-10-03-cyl4-end.jpg`](photos/cover-leak-2026-10-03-cyl4-end.jpg) | the wrong cover gasket leaking at cylinder 4's end, 3/10/2026, first warm run |
| [`cover-leak-2026-10-03-below.jpg`](photos/cover-leak-2026-10-03-below.jpg) | the same leak, the oil below it |
| [`cover-leak-2026-10-03-bracket.jpg`](photos/cover-leak-2026-10-03-bracket.jpg) | the loom bracket under the cover's hold-down strip at that end |
| [`cover-gasket-old-halfmoon.jpg`](photos/cover-gasket-old-halfmoon.jpg) | the gasket off on 1/10: a solid half-moon |
| [`cover-gasket-old-halfmoon-edge.jpg`](photos/cover-gasket-old-halfmoon-edge.jpg) | the same half-moon from its edge, ribbed all round |
| [`cover-gasket-325070-open-arch.jpg`](photos/cover-gasket-325070-open-arch.jpg) | Elring `325.070`, the wrong part: an open arch at the same place |
| [`cover-gasket-325070-open-arch-2.jpg`](photos/cover-gasket-325070-open-arch-2.jpg) | the same arch from another side |
| [`cover-gasket-325070-profile.jpg`](photos/cover-gasket-325070-profile.jpg) | `325.070`'s taller ribbed section |
| [`cover-gasket-915653-halfmoon.jpg`](photos/cover-gasket-915653-halfmoon.jpg) | Elring `915.653`, the right part: a solid half-moon and a sleeved bolt hole |
| [`cover-gasket-915653-whole.jpg`](photos/cover-gasket-915653-whole.jpg) | the same gasket whole, beside the new plenum gasket |
| [`cover-gasket-915653-label.jpg`](photos/cover-gasket-915653-label.jpg) | its package label: `915.653`, Elring Germany |
| [`cover-leak-2026-10-04-cleaned.jpg`](photos/cover-leak-2026-10-04-cleaned.jpg) | coil, leads and harness after the oil was cleaned off, 4/10/2026 |
| [`cover-on-2026-10-04-belt-end.jpg`](photos/cover-on-2026-10-04-belt-end.jpg) | `915.653` fitted, the cover on: the timing-belt end |
| [`cover-on-2026-10-04-halfmoon.jpg`](photos/cover-on-2026-10-04-halfmoon.jpg) | the same, a half-moon in place at the end of the head |
| [`cover-on-2026-10-04-strip.jpg`](photos/cover-on-2026-10-04-strip.jpg) | a hold-down strip and its nut on the refitted cover |
| [`cover-on-2026-10-04-bracket.jpg`](photos/cover-on-2026-10-04-bracket.jpg) | the side bracket and harness at the refitted cover |
| [`plenum-on-2026-10-04.jpg`](photos/plenum-on-2026-10-04.jpg) | the engine reassembled, plenum on, 4/10/2026 |
| [`plug-well-cyl4-2026-10-09.jpg`](photos/plug-well-cyl4-2026-10-09.jpg) | cylinder 4's plug well: dark patches on the terminal, a smudge on the hex (seen 1/10, would not come off with petrol) |
| [`plug-well-2026-10-09-b.jpg`](photos/plug-well-2026-10-09-b.jpg), [`-c`](photos/plug-well-2026-10-09-c.jpg), [`-d`](photos/plug-well-2026-10-09-d.jpg) | the other three plug wells, cylinder not recorded; `-d` too dark to judge |
| `leads-2026-10-01-coil-end-1`…`-4.jpg` | the 9/2026 leads' **coil** ends: red sleeve, rolled terminal, wire spring; which lead not recorded |
| `leads-2026-10-01-plug-end-1`…`-6.jpg` | their **plug** ends: slotted metal sleeve round a rubber insert; `-1`'s insert darker and crusted; which lead not recorded |
| `leads-old-2026-10-10-plug-end-cyl1`…`cyl4.jpg` | the same leads' plug ends, **numbered by cylinder** on removal 10/10: 4's insert scored and ragged, terminal not visible; 1–3 smoother, terminals in view |
| `plug-old-2026-10-10-cyl1-top.jpg`, `-cyl1-tip.jpg` | old plug 1, **came out almost without effort**: terminal darkened, firing end sooted |
| `plug-old-2026-10-10-cyl2-top.jpg`, `-cyl2-tip.jpg` | old plug 2: terminal darkened, smooth; firing end lighter, grey electrodes |
| `plug-old-2026-10-10-cyl3-top.jpg`, `-cyl3-tip.jpg` | old plug 3: terminal smooth; firing end sooted, crusted ground electrodes |
| `plug-old-2026-10-10-cyl4-top.jpg`, `-cyl4-tip.jpg` | old plug 4: terminal dark and pitted; firing end in dry black soot |
| `plug-old-2026-10-10-type.jpg`, `plug-new-2026-10-10.jpg` | an old plug's print, NGK `BKUR6E…10`, `…ET … JAPAN`; a new one of the same type beside it |
| `leads-new-2026-10-10-set.jpg`, `-coil-end.jpg` | the NGK `RC-VW254` set: black (the old grey), *"5MB"* (the old *"5ME2"*); angled coil ends, metal-shielded plug ends |
| `plug-2026-10-20-cyl1.jpg` … `-cyl4.jpg` | the 10/10 plugs after nine days: insulators white; **1 and 4 sooted black, 2 lighter, 3 the cleanest** (*owner*, 20/10; *this said "plug 2 alone light" until he corrected it*); clean amber oil on every thread |
| `borescope-2026-10-20-cyl3-exhaust-valve.jpg`, `-2.jpg` | cylinder 3's exhaust valve: light patches with a raised dark rim, where deposit has come away |
| `borescope-2026-10-20-cyl4-piston-edge.jpg` | cylinder 4's piston crown: a granular crust heaviest along the bowl edge |
| `borescope-2026-10-20-cyl2-chamber.jpg` | cylinder 2's chamber: an even thin layer, nothing flaking |
| `lead2-plug-end-torn-2026-10-20.jpg` | lead 2's plug end, torn on removal |
| `injector4-loom-2026-10-19.jpg` | injector 4's wires leaving the harness, old tape peeling, insulation whole |

---

## Keeping this current

- **Add a row, do not rewrite one.** The record is cumulative; it has to
  answer "what changed between those two dates".
- **Distances are derived in one place** — the odometer tables above —
  and say so. Do not type a second copy elsewhere.
- **Mark what is measured**: pump figures measured, service dates
  recorded, anything computed from them derived.
