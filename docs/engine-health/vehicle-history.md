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
| At 11 Aug 2026 | **153,032 km** (the bus, 0x520, captures `08`–`17`) |
| At 11 Sep 2026 | **153,088 km** (the bus, capture `18`) |
| At 13 Sep 2026 | about 154,000 km — *a round figure: the bus read 153,088 two days before and 153,569 on 24/9* |
| At 24 Sep 2026 | **153,569 km** (the bus, capture `20`) |
| At 23 Oct 2026 | **154,501 km** (`photos/odometer-2026-10-23.jpg`; the cluster's trip 289.4 km since the fill of 17/10) |
| At 24 Oct 2026 | **154,755 km** (`photos/odometer-2026-10-24.jpg`; the cluster's trip 543.5 km since the fill of 17/10, zeroed at this fill) |
| At 26 Oct 2026 | **154,999 km**, the oil change (*owner*) |
| At 27 Oct 2026 | **155,024 km**, the first oil top-up (*owner*) |
| At 29 Oct 2026 | **155,193 km** (`photos/odometer-2026-10-29.jpg`), the fill; the cluster's trip read 151.4 km, zeroed by the battery disconnect of 27/10 at about 155,042 |
| At 31 Oct 2026 | **155,277 km** (album, 20:14), after the can; the cluster's trip 83.5 km since the fill of 29/10 |
| At 3 Nov 2026 | **155,357 km** (`photos/odometer-2026-11-03.jpg`), at the tuner before the map; the cluster's trip 164.1 km since the fill of 29/10 |
| At 5 Nov 2026 | **155,546 km** (album, 22:07), the oil level read (`open.md` H18); the cluster's trip 190.7 km, zeroed at about 155,355 — at the tuner on 3/11, most likely the ECU's work (*reasoned*). *This said "since the fill of 29/10" until 8/11.* |
| At 8 Nov 2026 | **155,691 km** (album, 10:38), on reserve, before the part fill below; the cluster's trip 335.8 km, zeroed at about 155,355 as above |
| At 8 Nov 2026, the fill | **155,707 km** (album, 10:56), the cluster's trip 351.1 km |
| At 9 Nov 2026 | about **156,000 km**, the hydrogen clean (the provider's certificate, rounded; the bus read 155,834 the next afternoon, so about 155,8xx) |
| At 10 Nov 2026 | **155,834 → 155,853 km**, the relearn drive home (the bus, 0x520, the unfiltered capture of `47`) |
| At 12 Nov 2026 | **155,969 → 156,011 km**, the captured warm drive (the bus, 0x520, capture `49`) |
| At 12 Nov 2026, evening | **156,011 → 156,030 km**, the queue drive (the bus, 0x520, capture `50`) |
| **Covered in ownership** | **29,800 km over 9.1 years** (to 12 Nov 2026), about 3,300 km a year *(derived)* |

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
9/10, 10/10 and later). **No odometer reading taken
until 23/10/2026**, in the first table.

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
| 10/8/2021 | annual service: arms, brakes, oil, **decarbonisation, with hydrogen** (*owner*, 3/11/2026, found in his records; *this said "what kind is not recorded" until then*), filters; how the car ran after it is not remembered | Spei |
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
| **Both oxygen sensors, new: front Bosch `0 258 006 978`, rear Bosch `0 258 010 032`** (TecDoc's for the AQY, checked against the VIN at the shop); **no part number on the old probes or the new** (*owner*); 4-pin connectors, the same purple coding as the old (`photos/lambda-connector-new-2026-11-10.jpg`, `…-old-…`). Tightened by hand, about 50 Nm estimated, no torque wrench (the slotted socket's slot too narrow for the lead); the leads below tidied, the old ones had hung out (*owner*; `photos/lambda-rear-new-fitted-2026-11-10.jpg`); the threads carry Bosch's own paste (`photos/lambda-front-new-paste-2026-11-10.jpg`). The old probe plugging the spare boss left in place. **The old front probe's tip coated in a cracked grey-beige layer**, the rear's dark and clean (`photos/lambda-front-old-tip-2026-11-10.jpg`, `photos/lambda-rear-old-tip-2026-11-10.jpg`); the old probes kept; **the new rear probe's signal fell to zero under load on the drive home the same day, P0137 sporadic, cleared by the owner** (`open.md` S23); **the new rear probe taken out again and the old rear probe refitted, 12/11/2026 just after midnight** (both measured cold first: heater 8.3 Ω new, 9.2 Ω old, every other pair open; the album 00:29), so the front is new and the rear old; **on the drive of 12/11 the old rear probe read healthy and stored no P0137, so the new rear probe goes back to the seller** (`open.md` S23) | **10/11/2026**, by the owner *(previously 10/2017, never changed until then)*; the rear back to the old **12/11/2026** | ~0 |
| Timing belt and water pump. **Its marks read 13/11/2026**: the cam's OT set, the crank pulley's notch 30–60° short of its groove by eye — the cam advanced if those are the true marks, the size not settled (`open.md` A1); the owner has decided on a renewal at a garage (`plan.md` 8q) | **10/2017** | ~29,800 km |
| Fuel filter | **12/2017**; another bought 10/2022, believed the wrong type and never fitted (no record either way) | 4 or 9 years, **not established** |
| Chiptuning, described by the owner as mild | 6/2018 — **confirmed by the original order email** (*owner*, 12/10/2026). The tuner kept the original map; writing it back was set for 22/10/2026, postponed, and **was done on 3/11/2026** at 155,357 km, by the same tuner; the adaptations reset with it (032 0.0 / 0.0 %, 055 0.00, `test/fixtures/vcds/vcds-step5a-adaptations-032-055.csv`). **What the remap had changed**, off the tuner's two flashes: five tables, less fuel and more advance at high speed and the highest load only (`open.md` H14). *This said "booked for 3/11/2026" until it was done.* *This said "the car is not going back to standard" until 12/10* | — |
| MAF sensor | 7/2018 *(connector cleaned 7/2026)* | not recoverable |
| Dipstick, cap and a seal recorded as "valve seal", against an oil leak. *Owner's recollection (27/9/2026), not certain:* the dipstick's neck was cracked; the seal probably the rubber it seats in, not the valve cover gasket. Record not kept | **12/7/2018** | — |
| **Fuel tank** | **replaced inside the ownership, date not recoverable** (*owner certain*). *An earlier revision said the tank had never been touched* | unknown |
| Fuel pump, Bosch | 10/2022 | ~1,500 km |
| Spark plugs and leads, **NGK both** (Dakuma invoice, 22/12/2022, no part numbers; not kept here, it carries the owner's name and plate) | 12/2022 *(replaced 9/2026)* | ~1,500 km — came out destroyed (below) |
| Ignition coil | 6/2026 | ~0 |
| Engine oil (filter presumably, not stated): **Total *Quartz***, the same as the new fill by his recollection; whether the *9000 Energy* or the plain *9000* not remembered (*owner*, 23/10/2026) | **6/2026**, **about three years after the change before it** (*owner*, 23/10/2026), the car having stood outdoors nearly a year of that (2025, `Distance` above); **the filler cap's underside slightly brown with condensed water** at the change, not coolant (*owner*); **the old oil really black**, changed without a flush (*owner*, 24/10/2026). At the upper mark on 27/9/2026. **Topped up at some point since the change** — the last top-up left it about 1 mm over the upper mark, **and it was still there on 24/10/2026** (*owner*, 25/10/2026; the date not given). *This said "not topped up since" until then.* | about 700 km to 27/9 (*owner's estimate*); odometer at the change not recorded |
| Throttle body `06A 133 064 H` (VDO `408 237/111/017`) | **original until 2/10/2026** (kept). 6/2026: inspected, already clean, new gasket, adaptation run. *Part number read off the label, photographed 26/9/2026; an earlier revision gave `028 129 748`, unsourced* | the car's |
| Fuel pressure regulator `037 133 035 C`, **3 bar** printed on it (*read off the part*, 10/10/2026) | **6/2026** (*owner*, 25/10/2026; *this said 7/2026 until then*) | ~0 |
| The regulator's vacuum hose, 4 mm, to a narrow tube on the intake; **the old one well perished** (*owner*, 25/10/2026). The new one rubber with an outer layer, where bought not remembered, **no clip**; off and on many times with the intake work, and **at least once left on while the intake came off, which pinched it** — the crack likely from that, **from about September** (*owner*, 25/10/2026; *this said "left off at least once" until he corrected it*); **found 25/10/2026 with its intake end breaking up** — layers parted with voids between them, a crack from the bore outwards (`photos/fpr-vacuum-hose-2026-10-25-end.jpg`) — still blowing through (*owner*). **25/10: cut back about 1 cm at that end and turned round, the cut end now on the regulator; the crack still in the fresh cut** (`photos/fpr-vacuum-hose-2026-10-25-after-cut.jpg`). **Replaced 25/10/2026** (below). |
| **The regulator's vacuum hose, new**: STARLINE fuel hose, rubber, 4 × 8 mm (AutoKelly `PH G040080`), both ends cut fresh, **a spring clip at each end** (`photos/fpr-vacuum-hose-2026-10-25-fitted.jpg`, `…-old-and-new.jpg`) | **25/10/2026**, by the owner | ~0 | **6/2026** (*owner*; the regulator itself 6/2026 too) | ~0 |
| Purge valve N80, **Bosch `0 280 142 353`, VW `1C0 906 517 A`**, date code `040` (*read off the part*, 6/11/2026, `photos/n80-2026-11-06-label.jpg`), in its rubber holder `051 133 459 A`; its rubber hoses old but sound, no granules or fuel smell in the canister side (*owner*) | **not known** — original or replaced before; P0440 stored 1/2018 and 6/11/2026 (`open.md` S21). **Taken out, cleaned with its contacts and refitted, 6/11/2026** (*owner*); replaced with the same part only if P0440 comes back (`plan.md` 8a; *until 9/11 also "or the decarbonisation changes nothing"*; it changed cylinder 3). *This said "to be replaced" until then.* | — |
| **Charcoal canister `1HM 201 801 B`**, its housing `171 201 813`, `3KD`, `PP5`, Mexico (*read off it*, 11/11/2026, the album 18:06–18:23; *this said "`… 201 813`, first group not clear" until then*): **found bypassed** — the line from the tank joined straight to the line to N80, the canister's port open (*owner*, 11/11/2026, the album); sound — dry inside, passes, holds with its top ports closed; the line across its top the mould's (the album, 18:55) | **before the owner's time**, not known | — |
| **Vent valve at the top of the filler neck, VW `1C0 201 756`** (*read off it*, 11/11/2026): **works** — passes as fitted, closed upside down (*owner*; *this said "stuck closed" briefly, the first test had it upside down*) | **the car's**, not known | — |
| Heater replacement, dashboard dismantled | **summer 2026, before 11/8**; **battery out for more than a week**, every ECM adaptation restarted | — |
| Small hose, secondary-air combination valve to the intake ahead of the MAF | torn off in the heater work; fault **16795 / P0411** photographed **11/8/2026 16:39**, the same screen reading the fault memory cleared (the album); refitted that day or a few days after. **The engine lamp was lit for it with the engine running in every capture before the clear** (`01`–`07`, 153,029–153,031 km) **and out in every one after** (`09`–`17`, 153,032 km) — read off the bus 10/11 (0x480 b1 bit 3, `docs/firmware/can-decoding.md`) | — |
| Catalytic converter, **flex pipe**, silencer, exhaust gaskets: flex pipe to the tail | **10/9/2026** *(previously 10/2017)*; the old converter found blocked (below). The new front pipe is universal; its lambda boss, **ahead of the converter, behind the front probe**, is closed by **an old lambda probe with its leads cut off short** (`photos/exhaust-blanked-boss-2026-10-12.jpg`; *this said only "blanked-off" until the photo*). The front probe sits **on the manifold**. The manifold-to-front-pipe joint **remade by the garage in this work**, and once before (date not recorded). Rear probe cable re-routed and tied up by the owner 12/10/2026 (`photos/rear-probe-2026-10-12.jpg`, `photos/exhaust-joint-2026-10-12-on-4.jpg`); the converter `photos/converter-2026-10-12.jpg` | ~0 |
| Rear shock absorbers, A/C recharge, minor items | 17/9/2026 | ~0 |
| Upper intake manifold gasket, **Elring `271.230`** (= VW `06A 129 717`, matched to the VIN by the shop) | **17/9/2026 at the garage**, then **23/9 by the owner**; packaging dated 17/9/2026, Carvo s.r.o. (*read off the photo*). *This row used to give one fitting.* New ones again 2/10, 4/10 and 10/10 (rows below) | ~0 |
| **Spark plugs and ignition leads**: NGK `BKUR6ET-10` plugs (*read off one on removal*, `photos/plug-old-2026-10-10-type.jpg`); NGK leads, grey, printed *"NGK SPARK PLUG CABLE"*, *"5ME2"* (`photos/cover-leak-2026-10-04-cleaned.jpg`) | **17/9/2026**, Dakuma; **off 10/10/2026**, kept numbered | ~0 |
| **Compression, 17/9/2026: 12 bar on all four** (*garage-recorded*; *earlier revisions said 13, misremembered*) | — | — |
| Injectors `06A 906 031 C` / Bosch `0 280 155 791`, new from the UK | delivered 22/9, **fitted 23/9/2026** by the owner; three not fully home until refitted 1/10/2026 (`idle-log.md`) | ~0 |
| **Fuel filter, new**, Bosch `0 450 905 318` | **23/9/2026**, with the injectors | ~0 |
| **MAF sensor, new**, genuine VW `06A 906 461 A` (the 2018 unit kept). Hose to the throttle on the owner's clamps: at the MAF a rubber-lined pipe clamp, **since 9/10/2026 a worm-drive band clamp `W2 50-70mm`** (`photos/maf-clamp-2026-10-09-*.jpg`); a one-screw band clamp at the throttle | **24/9/2026** (`idle-log.md`, 24/9) | ~0 |
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
| **Crankcase breather hose, new**, Gates `EMH118`, for the original `06A 103 493 N` (split at its cuff); **the thin hose to the tee by the runners** and **the 8 mm hose to the throttle** renewed; new clips | **14/10/2026**, by the owner | ~0 |
| **Fuel filler cap, new** — bought for its torn tether, the rubber cord that holds it when unscrewed (*owner*, 6/11/2026) | **about early 10/2026** (*owner*: "about a month ago", 6/11) | — |
| **Fuel cleaner**: one can of Liqui Moly *DFI Cleaner* with about 18 l of OMV MaxxMotion 100 | **15/10/2026** | — |
| Valve cover nuts **re-tightened again** | **the week of 19/10/2026**, by the owner (reported 26/10) | ~0 |
| **Exhaust manifold** (stainless, double-flow, SSP 233 p. 7) | **original, never replaced** (*owner*: rusty outside; a hole cannot be told from below). `photos/manifold-2026-10-12-*.jpg`, `photos/exhaust-flange-2026-10-12-below-*.jpg` | the car's |
| **Idle speed adaptation**, 01 channel 01 (login 01283; `vcds.md`) | **128 = 780 rpm, as found 12/10/2026** (`photos/vcds-idle-adapt-2026-10-12-*.jpg`); raised to **133 = 830 rpm** (the most accepted) and **put back to 128** the same day (*owner*; `refuted.md` D9) | — |
| **Borescope look**: plenum off; inlet ports through the runners, chambers through the plug holes; plugs out and back hand-tight. **Lead 2's plug end tore** on removal. Injector 4's peeling harness tape renewed, the wires whole. **Clean amber oil on every plug thread** (`photos/plug-2026-10-20-cyl*.jpg`). Nothing cleaned. **Ordered from VW, arriving 21/10**: leads `06A 905 409 L`, plugs `101 000 033 AA`; plenum gasket Elring `271.230` (VW `06A 129 717` out of production). A row of their own once fitted | **19–20/10/2026**, by the owner | ~0 |
| Valve cover nuts **checked with the plenum off**: most already tight, the rest tightened | **20/10/2026**, by the owner | ~0 |
| **Spark plugs and ignition leads, VW**: plugs `101 000 033 AA`, whose box reads **"NGK BKUR6ET-10"** — the same plug as the set of 10/10, made in Japan, printed VW/Audi and NGK in black and stamped with the VW number (`photos/plug-vw-2026-10-21-*.jpg`; the 10/10 plug beside one, printed *NGK R* in blue, `photos/plug-ngk-old-vs-vw-2026-10-21.jpg`). Leads `06A 905 409 L` (`photos/leads-vw-2026-10-21-*.jpg`), **much stiffer to the touch** than the NGK `RC-VW254`, and **each plug end has a small rubber ring inside** where it seats on the plug, which the NGK ends do not have (*owner*; the inside of each, `photos/lead-end-vw-2026-10-21-inside.jpg`, `photos/lead-end-ngk-old-2026-10-21-inside.jpg`). Plugs fitted first, then the leads, 1, 4, 2, 3 clockwise from the coil's top tower, routed clear of the plenum (`photos/refit-2026-10-21-ports-covered.jpg`); every end clicked and sits with no play (*owner*). **The plenum refitted on a new Elring `271.230`** | **21/10/2026**, by the owner, bought from VW the same day | ~0 |
| **Fuel: OMV MaxxMotion 100**, always (*owner*, 10/10/2026). Before 9/2017 not known. **Until summer 2026 the tank held fuel about three years old** | 9/2017 to 23/10/2026 | ~28,300 km |
| **Fuel: Orlen Verva 100**, 50.88 l, with the second can of BG 44K; no OMV on the route (*owner*). *This row said "OMV MaxxMotion 100, always" until this fill* | **24/10/2026** at 154,755 km, run down to 2.2 l indicated by 29/10 | 438 km |
| **Fuel: OMV MaxxMotion 100plus**, the fuel of every year before the Verva, 50.16 l to the first click, no cleaner (*owner*) | **29/10/2026** at 155,193 km | — |
| **Fuel topped up from a can: 5 l, perhaps 6**, OMV MaxxMotion 100plus **bought into the can on 8/9/2026** (*owner*), so about eight weeks in the cellar; poured in because it smelt there. *This said "from when the car was laid up in the garden" until he gave the date.* About 46 l in the tank before (*owner's recollection*) | **31/10/2026** at 155,277 km, 83.5 km after the fill of 29/10; **50.0 l indicated after** (album) | — |
| **Fuel: Orlen Efecta 95, 4.76 l** — on reserve, no OMV within reach, enough to reach one in Prague and fill there (*owner*; the pump read off the photo, album 10:39; *the owner called it Verva 95*) | **8/11/2026**, 155,691 km | — |
| **Fuel: OMV MaxxMotion 100, 47.61 l**, to the click | **8/11/2026**, 155,707 km | — |
| **Exhaust heat shields: new clips** on the sheet-metal shields around the exhaust, which rattled at certain engine speeds (*owner*); `open.md` S17's resonance still heard after them. Held once before with nuts over the old clips, which did not hold (date not given) | **31/10/2026**, by the owner | — |
| **Battery disconnected** (every ECM adaptation restarts — *except 055, which a minute's disconnect on 26/10 left alone*) | after the summer heater work, then **23/9, 26/9, 1–2/10, the morning of 4/10, about a minute on 26/10 and from midday 27/10/2026** (several hours), **and on 10/11/2026 from the morning to the afternoon** at work (032 and 055 read all zero after it), **and again 10/11/2026 late night**, the battery taken out to look under it after the probes' harness was taped; 098 run 2/10, 4/10, **10/11** and **10/11 late night (ADP OK)** (on 26/10 and the morning of 27/10 it was only read as a measuring block) | — |
| **Throttle cable slackened** at its detent (*owner*): it had been taken up to the stop on 1–2/10; 054 afterwards about 5° at rest to 90° on the floor | **27/10/2026**, by the owner | — |
| **Accelerator pedal greased** (*owner*): it stuck near the start of its travel, plate jumping 1–4° at a time; smooth afterwards (`idle-log.md`, 27/10 evening) | **27/10/2026**, by the owner | — |
| **Fuel cleaner, BG 44K** (`208`): the first can into 23.5 l of OMV MaxxMotion 100; the second into the Orlen fill of 24/10 (row above) | **23/10/2026** at 154,501 km; **24/10/2026** at 154,755 km | — |
| **Engine oil and filter**: two flushes with **BG EPR** (`109`), each 30 minutes at about 1250 rpm, drained hot, a Bosch `0 451 103 314` filter between; then **VW filter `06A 115 561 B`**, a **new VW drain plug** at about 30 Nm, **Total *Quartz 9000 Energy* 5W-40**, about 4 l. Next changes: EPR each time until the symptoms are settled, at most once a year (*owner*) | **26/10/2026** at 154,999 km, by the owner | 0 |
| Engine oil **topped up**, about 0.4 l, after the level fell overnight as the oil ran back from the head; at the top mark after the next drive | **27/10/2026** at 155,024 km, by the owner | — |
| **Decarbonisation, with hydrogen**, Bez Karbonu (HPower s.r.o.), Prague: oxyhydrogen from a machine of 800 l/h run at about 60 % (*owner*), into the intake behind the MAF, the engine held at 1,750–2,150 rpm by the provider for about an hour and at idle for the last two minutes, never stopped; a certificate given. The second such clean (the first 10/8/2021, above) | **9/11/2026** at about 156,000 km (the certificate's rounding) | — |

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
2/10 and 4/10. What it found is `idle-log.md`, the entries of
1–2/10, 3/10 and 4/10.

---

## Fault memory, as found in old scans

*Owner's VCDS scans, found 10/10/2026; the dates are the owner's.*

| When | Stored | Since |
|---|---|---|
| **1/2018** | 16824 / P0440, EVAP emission control system, intermittent | **never repaired**; not stored again until **6/11/2026**, the engine lamp lit (`open.md` S21; `photos/vcds-faults-2026-11-06.jpg`), cleared by the owner. *This said "not stored since" until then.* |
| **5/2019** | 16556 / P0172, fuel trim too rich; 16684 / P0300, random/multiple misfire; **16688 / P0304, cylinder 4 misfire** — all intermittent | P0172 stored again in the window of 23–24/10/2026 (`open.md` S19); the others not stored since. *This said "not stored since" for all three until 6/11/2026.* |

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
| **The lower manifold gasket's bent edge at runner 3 straightened** by hand, from below (runner 4's is torn, perhaps into the sealing face) | **5/11/2026** night, by the owner | seen bent on a look from below (`open.md` H3) |
| **The oxygen probes' harness, taped** (a stopgap): the rear probe's heater lead (blue on the harness side, the probe's outer white) cracked and corroding behind its connector, and the front probe's signal earth (brown, the probe's grey) worn and cracked, each wrapped in PVC tape; then the whole bundle wrapped so it cannot move or be pressed, and Tesa fabric tape over all of it before it went back under the plastic; **the new probes' spare lead left outside the box and held with cable ties**, as the old probes' had been; both inside the black plastic box under the car where the leads run. Spliced under heat-shrink later | **10/11/2026** night, by the owner | found under the box that evening (`open.md` S23, *Found at the harness*); the photographs in the album, 21:32–21:50, the finished work 22:11–22:20 |
| **G62's connector and the sensor's socket cleaned of old engine oil** — a film standing round the sensor's pins, a ring round the harness side's seal — with a rag and contact spray; the sensor pulled from its housing (about 10 ml of coolant lost, not topped up), its O-ring whole, greased, refitted with its clip (the album 23:55–00:13) | **11/11/2026** late night, by the owner | P0118 sporadic and the coolant reading dropping fast (`open.md` S24) |
| **Contact cleaner** sprayed into injector 4's connector and the injector loom's 3-pin connector T3 (the supply, by cylinder 1; its latch worn) | **5/11/2026** evening, by the owner | both off for a first look at the loom (`open.md` H4); probably done once already this year |

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
| `lower-manifold-2026-10-19-ports.jpg` | the lower manifold's four runners with the plenum off, 19/10 late evening |
| `borescope-2026-10-20-cyl4-inlet-port-1`…`-3.jpg`, `-cyl3-…-1`…`-3`, `-cyl2-…-1`, `-2`, `-cyl1-…-1`, `-2` | **the inlet ports from above**, stem, guide boss and the back of the inlet valve; a deposit rim round the throat in each. `cyl4-inlet-port-2` is the frame the owner asked about on 21/10 (*a hole burnt beside the seat?* — the seat face cannot be seen from the port) |
| `borescope-2026-10-20-cyl4-valve`, `-cyl2-valve`, `-cyl1-valve.jpg` | a valve head through the plug hole; **inlet or exhaust not recorded** |
| `borescope-2026-10-20-cyl4-chamber`, `-cyl4-crown.jpg` | cylinder 4's crown: a granular layer, darker round the bowl |
| `borescope-2026-10-20-cyl4-crown-line-1`…`-3.jpg` | cylinder 4's crown: **a thin dark line from the crown's edge in towards the bowl**, in three frames from different angles. Read as **the edge of a deposit where old carbon has come away** (*owner*, 21/10: similar edges on other crowns; nothing but the borescope went in, and a fibre would not survive combustion). A crack is not excluded by a cheap screen, but nothing points to one |
| `borescope-2026-10-20-cyl3-crown-1`…`-4.jpg` | cylinder 3's crown: the layer broken into islands, bare metal between them |
| `borescope-2026-10-20-cyl2-crown.jpg` | cylinder 2's crown: a thin even layer, a flake lifting at the edge |
| `borescope-2026-10-20-cyl1-crown`, `-cyl1-crown-edge.jpg` | cylinder 1's crown: a thin layer; a small dark mark at the edge in `-edge` |

The borescope frames above were taken off the owner's album and **assigned
to cylinders by their timestamps** against his order (ports 4-3-2-1 from
23:59, a few minutes apart; then chambers 4-3-2-1, each after its plug came
out, the plug photographed first). The rest of the 109 frames of that night
are in the owner's album, not here.
| `lead2-plug-end-torn-2026-10-20.jpg` | lead 2's plug end, torn on removal |
| `injector4-loom-2026-10-19.jpg` | injector 4's wires leaving the harness, old tape peeling, insulation whole |
| `lower-manifold-gasket-2026-11-05-1.jpg`, `-2.jpg` | the lower intake manifold's joint to the head from below, 5/11: the gasket's edge torn at runner 4 (perhaps into the sealing face), bent at 3, whole at 1 and 2 (*owner*) |
| `dipstick-2026-11-05.jpg` | the dipstick at 155,546 km, a little under the top mark (*owner*) |
| `timing-belt-2026-11-13-cam-ot.jpg` | the camshaft sprocket at TDC of cylinder 1, 13/11, cold: the OT mark against its mark, a tooth painted white (`open.md` A1) |
| `timing-belt-2026-11-13-crank-notch-borescope.jpg` | the crankshaft pulley's notch on the borescope's screen, the owner's finger on it, 13/11: by his eye 30–60° of crank off the groove on the block (`open.md` A1) |

---

## Keeping this current

- **Add a row, do not rewrite one.** The record is cumulative; it has to
  answer "what changed between those two dates".
- **Distances are derived in one place** — the odometer tables above —
  and say so. Do not type a second copy elsewhere.
- **Mark what is measured**: pump figures measured, service dates
  recorded, anything computed from them derived.
