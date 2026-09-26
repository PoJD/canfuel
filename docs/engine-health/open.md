# Engine health — what is still wrong, and how to find out why

**The working document for one open investigation into the engine itself.**
It holds only what is **unresolved**: the symptoms still present, the
hypotheses still standing, and the test that would confirm or kill each one.
It has an end date. When every symptom below is either fixed or shown to be
normal for this engine, the file is deleted.

| file | what is in it |
|---|---|
| **this one** | symptoms → hypotheses → tests → plan. Short on purpose |
| `refuted.md` | every hypothesis **settled against**, with what settled it, plus the questions that were **answered**. Read it before proposing something: most obvious ideas are already there |
| `vcds.md` | the VCDS blocks read on this car, their specifications, and how to record VCDS beside a CAN capture |
| `vehicle-history.md` | the car's permanent record: distance, consumption, every part replaced. **Stays when this investigation closes**; `open.md` and `refuted.md` go |

The long version this replaced, a dated log of 10–25 September 2026 with every
alignment and argument in full, is in git:
`git show 7c69883:docs/engine-health.md`. Nothing in the tree depends on it.

**Rules for this file.** A hypothesis that is refuted moves to
`refuted.md` in the same commit, with its evidence, and leaves
this file. A new measurement goes into the evidence line of the symptom and of
every hypothesis it touches, not into a dated section. Owner reports are
marked *owner-reported*; general engine knowledge is marked *general*, since
none of it comes from a document this project holds.

⚠ **Nothing here changes a constant in `src/`.** The firmware only reports;
`IdleHealth` and the start bytes on 0x604 are one of the instruments used
below (`docs/firmware/frames.md`).

---

## Where it stands — 25 September 2026

**Replaced so far:** coil (6/2026), exhaust from the flex pipe back including
the converter (9/2026), plugs and leads (17/9), all four injectors, fuel
filter (23/9), MAF (24/9). The regulator is from 7/2026. Compression is
12 bar on all four.

**Fixed by that:** the rich lambda trim (it was the MAF; one confirming
read owed, S9), the cold-overrun burble, the long cranking, the historical
full-load lamp. The car pulls better
and drives better than at any point on record.

**Not fixed:** the idle. It still stumbles, the ECU still counts misfires at a
standstill idle, the exhaust still puffs now and then. **Every part in the fuel
and ignition path has now been changed and it is still there**, so what is
left is either outside those parts or is normal for this engine.
Separately, knock control hears something in cylinder 4's window above about
2300 rpm that is not knock.

---

## The symptoms

Numbered so that the hypotheses can refer to them.

### S1. Unsettled idle — engine speed fluctuates

**What is seen.** Every few seconds the idle dips by 20–45 rpm and recovers in
about a quarter of a second. It feels restless from the driver's seat too.
*Owner-reported:* the hesitation that the old MAF caused has gone; the
twitching has not.

**How it is measured.** `IdleHealth` on 0x604 grades one firing against the
next (100 = the engine before the repair, lower is smoother). Offline,
`tools/idledips.py` counts dips of ≥ 20 rpm and computes the same grade from a
capture.

**Current values**, *owner-reported off the display*. Hot idle, 69–72 °C of
oil: `IdleHealth` **57–100, sometimes over 100**; 93 on the last reading,
"fluctuating a lot". At 56–68 °C: about 120. Readings with no temperature
noted: 80–160, which compare with nothing. Dips ≥ 20 rpm at a standstill idle: **5–11 a minute**
(`24_mafswap_drive_z1`), down from 15–21 on the old MAF the same morning.

**What is not known: the healthy target.** Every recording is of this engine
with the fault present. August's hot idle graded 48 (and 29 with the A/C on),
but those are 22-second holds, shorter than the device waits before it grades
at all, and August's idle stumbled too. **So nobody knows what a well AQY
grades.** That is hypothesis H0 below, and it is the first thing to fix.

**What one dip is worth.** Engine speed on 0x280 is recomputed once per 180°
of crank, one power stroke (`docs/firmware/can-decoding.md` trap 6), so a dip is one
cylinder's stroke. At the warm idle of `09_idle_60s_z1` — 796 rpm, 326 µl/s,
about 18.5 Nm indicated — one power stroke is worth about 58 J. A cylinder
that produces nothing takes that out of the rotating assembly: **33–57 rpm for
an assumed 0.20–0.12 kg·m² of crank, flywheel and clutch** (the inertia is an
estimate, not measured). The deepest dips measured are 37.5–46 rpm, inside
that bracket; the typical one is 20–22 rpm, about half — a partial burn, or a
full misfire the sampling rounded off. The fall takes one or two firings and
the recovery about 250 ms, which is the idle governor, not a fuelling loop:
**the dip is the failed combustion itself, not the ECU correcting anything.**

**Load at idle smooths it, 26/9/2026 — repeated.** *Owner-observed off the
display*, warm after ~100 km, standing: with headlights, blower and A/C on,
`IdleHealth` **48–50**, the calmest in weeks; everything off, it climbed to
**70–80**; on again, back towards 50. Two to three times, the last switch-on
with a smaller effect. **The same direction as August**, when the A/C-on hold
(`12`) graded 29 against 48 without it (`11`).

What it means, and what it does not: every one of those consumers is
**torque** the engine has to make at idle — the A/C compressor directly, the
lights and blower through the alternator — so the ECM opens up the air and
the engine idles at higher load. **The idle is rougher the lighter the load**,
which is where the misfires were always counted. ⚠ **It is not evidence for a
bad electrical joint** — more current through a poor joint makes its drop
larger, which would make things worse, not better; the system voltage is
also a little *lower* with the loads on. It argues for causes that matter
less as the air through the engine rises: **a small unmetered leak (H3)**,
diluted by more metered air; exhaust gas left in the cylinder at high vacuum;
a valve that seals worse at low cylinder pressure (H1). **To separate
electrical from mechanical load:** log VCDS group 002 (load, injection time,
air mass) with `IdleHealth` for lights only, A/C only, and both — if the grade
follows the load figure whichever consumer raises it, it is the load.

**The same, split by consumer, 26/9/2026 — owner-observed, VCDS not
running:** A/C with the blower on full, lights and rear heater off →
`IdleHealth` down to **35**; lights and rear window heater, no A/C → towards
**40**; everything off → climbing back to 70–80 each time. **Both lower it,
and this cannot tell which mechanism**: the A/C compressor is mostly
mechanical load, lights and rear heater mostly electrical current, but
20-odd amps through the alternator is also a few newton-metres the engine
has to make at idle. Group 002's load figure beside each state is what
would separate them.

**The roughest reading yet, 26/9/2026 — cold, and in fog.** A few minutes
after an overnight cold start (`StartClt` 14 °C) on a cold, foggy, very damp
morning, `IdleRough` read **3.72 rpm** (index ~186) before the car drove off.
*Owner-reported off the display, not photographed.* ⚠ Not comparable with the
warm figures: the grade had not converged (under 30 s of idle; the filter
rises from zero, so an unconverged reading is if anything low), and the only
recorded cold idle, `18_coldstart_z1`, graded 2.74 in its first minute at
25 °C of coolant. What it adds is the weather: the start itself was clean and
the idle the worst seen, **on the dampest morning yet** — which is what an
ignition fault that tracks moisture would do (H4, test 1e).

**Temperature matters and it is not monotonic.** Rough cold, worst at about
50–61 °C of oil, least rough hot. A reading without the oil temperature beside
it cannot be compared with anything.

### S2. An occasional puff from the exhaust

*Owner-reported*, at idle, before the injectors and after them, before the MAF
and after it. Not recorded, not timed, never aligned with anything. It did
**not** coincide with misfire detection going `deaktiv.`.

### S3. Misfires counted by the ECU at idle

**VCDS group 014**, on every drive since the counter was first logged.

- **122 of 129 new events began at a standstill idle**; the few seen in 1st
  and 2nd are mostly the three-second hold of an event that began standing.
  None during a pull.
- **Values 12–120 against the label file's stated 0 to 5.** By VW's own
  measuring-block specification, this is out of range.
- **The events are the S1 dips.** Aligned on engine speed, counter increments
  sit next to dips far more often than chance: p = 0.023 on the cold start,
  0.005 and < 5×10⁻⁵ on the two drives of 24/9. ⚠ Both are readings of crank
  speed (*general*: that is how OBD misfire detection works), so they are not
  two independent witnesses. And the converse does not hold: only 7 of 34,
  37 of 319 and 38 of 70 dips carry an increment.
- **No fault code is stored.** The rate stays below whatever the ECU needs to
  set one.

**Three properties of the counter that must be kept in mind**, all measured
on the 24/9 logs (`refuted.md` A11, A12): it moves in steps of 12; detection switches off below about 20 % load, which on
the new MAF is right at the hot-idle load; and it counted **five to fifty times
more per dip** after the MAF swap than before. **So 014 is a yes/no witness,
not a ruler.** Compare across time with engine speed or `IdleHealth`, never
with 014.

### S4. Knock retard on cylinder 4, and only cylinder 4

**Groups 022/023 (24/9) and 020 (25/9).** Cylinders 1–3 read zero in almost
every sample; cylinder 4 is retarded in steps of up to **6.7 °CA**, recovering
within seconds.

- 24/9: 16 events at 960–2000 rpm, 13 of them on a tip-in after a coast or a
  gearchange.
- 25/9, about 100 km later: the small tip-in events had shrunk to 0.7–1.5 °CA;
  the large ones (up to 5.2 °CA) came only at full throttle, 3000–4000 rpm.
- **Never at idle**, in either log.
- **Within VW's specification** of 0–15 °CA per cylinder while driving —
  VW's repair manual for the Golf Mk4, *Motronic injection and ignition system
  (2.0 ltr. engine)*, display groups 10–29, as transcribed on
  workshop-manuals.com (a third-party transcription, not a PDF held here).

### S5. Cylinder 4 reads high in group 026 (knock sensor voltage)

- **With no load at all** — standing in neutral, a tenth of full-throttle air —
  cylinder 4 reads **40–70 % above cylinder 1 from about 2300–2700 rpm up**.
  So it is not knock: *general*, knock needs cylinder pressure.
- **Above about 3350 rpm the extra moves to cylinder 1's window** and comes
  back to 4 as soon as the speed drops. One log; not seen in the other because
  it did not go that high.
- **At idle all four sit on the floor** (0.31 V). 026 sees nothing there.
- Cylinders **1 and 4 read about twice 2 and 3 in every state, fired or not.**
  That pair is the crank-symmetric one and is explained without a fault (see
  `refuted.md`); only cylinder 4's excess over cylinder 1 is
  open.
- ⚠ 026 is the voltage *with the ECU's amplifier factor included* (Ross-Tech's
  block list), and cylinders 1 and 4 are probably on different sensors (G61
  for 1–2, G66 for 3–4, from a sister engine's manual, not the AQY page). So
  comparing 4 against 1 is weaker than the tables make it look.

### S6. The exhaust is not tight

**Mostly acoustic**, and it has never been tight: holes in the old system, then
a joint behind the converter that the garage filled with sealant, which shook
out within two weeks and rattled under the driver's seat, loudest at about
3000 rpm and on the overrun. The clamp is now tightened as a temporary fix,
without sealant; the joint **hums slightly** and no longer rattles. The garage
still has to redo it.

**That joint is downstream of both lambda probes**, so it cannot affect the
mixture, the trims or any misfire. What matters for the other symptoms is
whether there is a leak **ahead of the front probe** — the original, 26-year-old
manifold, the new gasket at its flange, the probe boss. Nobody has tested
that; the garage is going to.

### S7. The cold start — closed 26/9/2026

**Fixed by the new injectors.** An overnight cold start at 14 °C of coolant,
in cold fog, cranked in 0.93 s and fell only 74 rpm after first firing,
against 1.24 s and a near-stall (451 → 311 rpm) on the old injectors. The
table and the reasoning are in `refuted.md` C3.

### S8. Top end — "loses breath above 5000 rpm"

*Owner-reported* after the morning drive of 24/9, on the old MAF: the car
pulls better in 1st to 3rd but runs out of breath above about 5000 rpm in
4th. Full-throttle pulls after the MAF swap "feel unchanged".

**What the recordings say — both MAFs, pulls to 5,840–6,030 rpm:**

| full throttle | `19`, old MAF | `24`, new MAF |
|---|---|---|
| air, 5000–5500 rpm (VCDS) | 86.4 g/s | 85.3 g/s |
| air, 5500–6000 rpm | 88.1 g/s | 88.5 g/s |
| relative load above 5000 rpm | — | ~80 % |
| b7 median, 4000–5000 / 5000–5500 / 5500–6000 rpm | 196 / 191 / 181 | 192 / 187 / 181 |
| power this firmware computes from those medians | ~86 kW at 5250, ~86 at 5750 | ~84 kW at 5250, ~86 at 5750 |

So **the air flattens above 5000 rpm on both MAFs, and power stays at
84–86 kW from 5000 to nearly 6000 rpm** — the AQY's rating is 85 kW at
5200 rpm. Torque falls past its peak while power holds flat, which is the
normal shape of a naturally aspirated engine past peak torque (*general*).
⚠ The power figures are this firmware's arithmetic on the ECU's modelled
torque, not a dynamometer, and the scale was itself set by requiring the
plateau to reproduce the ratings — so "it reaches 85 kW" is partly the
calibration agreeing with itself. What is measured is that **nothing changed
between the two MAFs and nothing collapses at the top.**

**Probably not a fault.** How it closes:

1. A held 4th-gear pull to 6000 rpm on the new MAF with the display's `Power`
   and a capture running: a plateau near 85 kW around 5000–5500 rpm that
   eases rather than drops off closes it as the engine's normal curve.
2. The healthy-AQY recording of H0, if it includes a pull, is the only
   comparison against another engine.
3. If the owner's feel was only ever about the old MAF's morning, say so and
   close it.

### S9. The rich lambda trim — fixed by the MAF, one confirming read owed

Group 032 went from −4.7 / +1.6 % (August) to **−16.4 / −13.3 %** after the
injector change on the old MAF, and to **−3.1 / +4.7 %** by the end of the
first afternoon on the new one, with air per commanded fuel back at August's
value. The explanation is in `refuted.md` C2: the old MAF over-read.

**How it closes:** one photographed 032 screen after a few hundred km with no
battery disconnect in between. Closed if both cells have settled within a few
per cent of zero — the proper bar is the specified range for 032 in the
label file, which was not noted when the blocks were looked up; note it
beside the reading. **An idle cell moving positive** would instead feed H3
(an unmetered leak); a part-load cell moving strongly either way reopens the
air metering.

### Other — not symptoms, but they touch this file

**Oil temperature.** Whether 0x420's `OilTemp` is right is a firmware
question, `docs/firmware/open.md` question 10, and is settled by a
thermometer in hot oil. It matters here because S1 depends on oil temperature
and every `IdleHealth` comparison is made at a matched one. If the channel
turns out to read 25 °C low, every oil temperature in this file shifts with
it — the comparisons between readings still hold, the absolute figures do not.

**The remap.** The ECU was chipped in 2018; the tuner's own remark was that
there was nothing to be had at the top of the range. What a remap on a
naturally aspirated engine normally changes is ignition advance and
full-load enrichment (*general*), for all four cylinders alike.

- **It cannot explain S4 or S5**, which are one cylinder's window, and the S5
  excess is there with no load at all. It can at most explain why cylinder 4
  sits close enough to the knock limit to be retarded on a tip-in.
- **It is very unlikely to explain S1–S3.** *The owner's assessment*: the idle
  probably not, the rest almost certainly not. The one route in would be an
  altered idle ignition map, and idle is held by the ECU's own closed-loop
  control.
- **How it closes: return the ECU to standard**, which the owner is
  considering. That needs the original map (whether the tuner kept it is not
  recorded). If it happens:
  1. `IdleHealth` at a matched oil temperature and a 020 + 026 neutral log,
     before and after — that turns the remap's role in S1 and S4/S5 from an
     assessment into a measurement;
  2. **one held full-throttle pull in 4th with a capture**, because the
     firmware's torque scale was derived by making this car's plateau
     reproduce the *stock* ratings (`docs/firmware/can-decoding.md`
     question 8). On a stock ECU that premise becomes true by construction;
     if b7's plateau moves, the scale is recalibrated from the new pull.

---

## How the symptoms relate — what is measured

| pair | link | evidence |
|---|---|---|
| S1 ↔ S3 | **the same events** | aligned three times, p ≤ 0.023. Both are crank speed, so partly one signal read twice |
| S1/S3 ↔ S9 | **strong** | the MAF swap halved the dips at every oil temperature (−51 to −65 %). An over-reading MAF was causing some of the stumbles; the rest is the residual fault |
| S1/S3 ↔ oil temperature | **strong, non-monotonic** | worst at ~50–61 °C of oil, less cold, least hot. On every drive |
| S4 ↔ S5 | **very likely one thing** | same cylinder window, same engine speeds, and S5 needs no combustion. Knock control retards cylinder 4 because it hears S5's noise |
| S4/S5 ↔ S1/S3 | **none measured** | no retard and no 026 signal at idle, in any log. Only a common cause could link them |
| S2 ↔ S3 | **unknown** | never aligned in time. A misfire puffs and a leak puffs |
| S2 ↔ S6 | **possible** | if there is a leak ahead of the probes. The known leak is behind them |
| S5 ↔ S6 | **no** | the clamp was tightened and cylinder 4's excess stayed exactly as it was |
| S7 ↔ S1 | **none** | S7 improved with the injectors; S1 did not |
| S8 ↔ anything | **none** | top-end air and b7 identical on both MAFs; the idle changed a lot |

**So there are two separate clusters**, and they are worked separately below:
**the idle** (S1, S2, S3) and **the cylinder 4 window** (S4, S5). S6 matters
only if it leaks ahead of the front probe; S7 is closed, and S8 and S9 each
want one confirming reading and are probably closed.

---

## The open hypotheses

Each one lists what it explains, what speaks against it, and the test that
settles it. ✔ fits, ~ fits weakly, ✘ does not fit, — says nothing.

### H0. The idle is normal for this engine — and there is no fault to find

**The one hypothesis nobody has been able to test.** An AQY with 26 years on
it might simply idle like this, and every number above might be its normal
state.

| S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|
| ~ | ~ | ✘ | — | ~ |

- **Against:** 014 reads **12–120 against VW's own 0–5**. The old converter
  burned through, which needs raw fuel in it. The owner feels it.
- **For:** no fault code; the counter's sensitivity moves with the MAF and with
  battery disconnects; today's best hot idle (57) is in the neighbourhood of
  August's, before any work (48). And for S5: there is no healthy AQY's 026 to compare with, so the
  1-and-4 excess could be how this engine sounds.

**Tests:**

1. **Record a healthy AQY** — another Golf/Bora/Octavia 2.0 with the AQY (or
   the same family), warm idle, 3–5 minutes: a USBtin capture and VCDS 014.
   `idledips.py --roughness` gives the grade and the dip rate; 014 gives the
   counter. **This is the single most valuable measurement left**: it gives
   S1 a target, tells whether 014 counts on a good engine too, and — with a
   026 neutral run — whether cylinder 4's excess is the engine type.
2. The same on any other Motronic 5.9.2 engine is a weaker substitute.

### H1. A lifter or valve on one cylinder at a hot idle (valvetrain)

A hydraulic lifter that bleeds down or pumps up leaves a valve slightly open
or late, intermittently, and gets worse as the oil thins. *General.*

| S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|
| ✔ | ✔ | ✔ | ✔ | ✔ |

- **For:** with H4, one of the **two candidates that can explain both
  clusters at once**: an
  intermittent leak past a valve at idle misfires, and puffs; a ticking lifter
  at camshaft speed lands in one knock window. Temperature-dependent through
  oil viscosity. Compression is a **cranking** test and does not see a valve
  that closes at 250 rpm but hangs at a hot idle.
- **Against:** S1 is worst at 50–61 °C and eases when hot, while a thin-oil
  lifter should be worst hot. The S5 excess switches on above ~2300 rpm and
  moves to cylinder 1 above ~3350, which fits a resonance better than a single
  part. No ticking has been reported.
- **From the Polish AQY thread** (see H4): one poster traced idle vibration
  to valves not sealing and fixed it with head work. A forum report.

**Tests:**

1. **Stethoscope** (or a long screwdriver to the ear), warm, neutral, at idle
   and at 2800–3200 rpm: the head over cylinder 4 against the head over
   cylinder 1; around 3400 rpm, cylinder 1. A tick at idle, or a difference at
   3000 rpm and not at 2000, is the part.
2. **Cold start by ear**: a lifter that bleeds down overnight clatters for the
   first seconds.
3. **Leak-down test, warm**, all four cylinders. Unlike compression, it is done
   at TDC on a hot engine and shows a valve that does not quite seat. A
   garage job.
4. **Oil pressure at a hot idle** against VW's figure, if a gauge can be put
   on the sender port. Low pressure starves the lifters at exactly that
   state.

### H2. A leak ahead of the front lambda probe (exhaust manifold, flange, probe boss)

At idle the exhaust pulses dip below atmospheric and a crack draws air in;
under load it only blows out. *General.* The front probe reads lean, the rear
loop absorbs it, so 032 barely moves (SSP 233 p. 16, the two-loop control).

| S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|
| ~ | ✔ | ~ | ✘ | ✘ |

- **For:** the puff, idle only, an old manifold that has lived through years
  of misfires, a new flange gasket, the rear probe on the rich side at hot
  idle (0.665–0.725 V), the exhaust never having been tight.
- **Against:** air outside the cylinder does not stop a cylinder firing, and
  a few per cent rich does not normally misfire. A crack leaks most cold, but
  S1 peaks mid-temperature. The MAF swap halved S1, which an exhaust leak
  would not care about. It cannot produce S5: that is there without exhaust
  pressure.

**Tests:**

1. **Smoke or pressure test** of the manifold, flange and probe boss, at the
   exhaust specialist. Looking is not a test. *Already decided by the owner.*
2. **Written before the repair, so the repair is a test:** if a leak ahead of
   the probes is found and sealed, the puff goes; the rear probe (036/037) at
   hot idle moves a little leaner; `IdleHealth` at 70–72 °C stays in its
   57–120 band; the mid-temperature 014 rate does not fall beyond scatter;
   cylinder 4's 026 excess does not change. **If the idle improves clearly,
   this hypothesis was underrated and the argument against it is wrong.**
3. If nothing is found, the puff is the misfire itself (H1, H3, H4, H5).

### H3. A small unmetered air leak at one intake runner

Air past the MAF leans one cylinder at idle, where air flow is smallest.
*General.*

| S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|
| ✔ | ~ | ✔ | ~ | ✘ |

- **For:** the regime is exactly right. A lean cylinder can also knock on a
  tip-in (S4). Several of the forum cases were a breather hose.
- **Against:** the idle trim is −3.1 %, slightly rich, and a leak big enough
  to misfire one cylinder would still pull the trim positive through one
  sensor averaging four. **A large leak is refuted** (`refuted.md`);
  only a small one at one runner survives. It cannot produce S5.

**Tests:**

1. **Spray test at a warm idle**: brake cleaner or propane along the manifold
   gasket, the runner joints, the injector seats, the breather hoses and the
   vacuum lines, with `IdleHealth` or engine speed on the display. A leak
   shows as a change in idle at the spot. Cheap, no dismantling. *General.*
2. A smoke test of the intake at the same garage visit as H2.
3. 032 after a few hundred km: an idle cell moving positive would support it.

### H4. Weak spark at light load that is not in the parts (earth, wiring, battery, coil connector)

All the ignition parts are new, so what is left is what feeds them. A poor
engine earth weakens the spark and adds noise to the knock-sensor signal
(*general*).

**What has already been measured on this car, and what it does not show.**
*Owner-measured, in the headlight work (`vehicle-history.md`, *Electrical work, 2026*), differentially
under load:* 0.9 V lost at the dipped-beam bulb, 1.6–1.9 V with main beam
too — **all of it on the positive side**. The lamp's earth dropped only
0.1–0.2 V, and **the battery terminals 0.000 V (+) and 0.002 V (−)** under the
same ~15 A. Most of the loss sat in the old light switch (0.3–0.7 V across
it); the rest is in its feed and the run to the lamp.

So ⚠ **the terminals and the body earth are clean**, and an earlier line here
that read the lights as a hint of a bad earth was wrong. Two things still
carry over:

- **the engine's own earth (ground 2, block to battery) was never loaded by
  that test** — headlight current does not flow through it — so it is still
  untested;
- **26-year-old switch contacts had crept to tenths of a volt.** The ignition
  coil and the ECM are fed through the same generation of relays, switches
  and connectors, so a drop on the **positive** feed to the coil or the ECM is
  as good a way to weaken the spark as a bad earth, and is measured the same
  way (tests 5a and 5b below).

The battery itself is new (end of August 2026, the old one found dead during
the headlight work), so the thread's one confirmed
electrical fix — a new battery — has in effect already been tried here.

| S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|
| ✔ | ✔ | ✔ | ~ | ✔ |

- **For:** with H1 the only candidate that could explain **both clusters**: a
  weak spark misfires at idle and high vacuum, and a noisy ground puts a
  signal into the knock channel that depends on engine speed. Cylinders 1 and
  4 share one coil output (twin-spark coils, SSP 233 p. 5), and their old
  plugs were the worse pair.
- **Against:** the plug pair is better explained by the old coil. Nothing
  here measures the ignition.

**What the long Polish AQY thread actually says** (forum.vwgolf.pl, t=522030,
twelve pages, 2013–2017; a forum, so leads, not sources). ⚠ An earlier
revision of this file said the original poster fixed it with a welded
exhaust manifold. **He did not**: welding made it "practically stop" for a few
days, then everything came back; he went on to a coil, leads, lambda probe,
timing belt and plugs, planned to pull the head, and **never reported a fix**.
The "four cracks, welding solved it" quote is from another thread, relayed by
someone else. What posters did report as fixed:

- **a new battery** (raq88, a battery 6–7 years old at purchase): "after 4
  years the misfires stopped"; the moderator concluded *"the cause of the
  vibrations is the car's electrics"*. One poster, a few weeks' follow-up;
- **a new Bosch coil** (two posters, one also with a lambda probe);
- **original thick VW leads** instead of new aftermarket (Beru) ones, which
  made it misfire (one poster);
- a cleaned-up earth was only **suggested** ("unscrew all the earths, wire-brush
  them, copper paste"), with no result reported. Nobody in the thread
  confirmed an earth fix; one noted it idled smoother after new alternator
  brushes and regulator, and worse in wet weather.

**VW had a service bulletin for exactly this, on the sister engines.** VW
of America TSB **01-08-27**: intermittent misfires and ignition "open
circuit" fault codes on the 2.0 8V (US codes AVH, AZG, BDC, BEV, BBW, BGD,
2002–2004, Golf/Jetta/Bora and the Beetle), traced to **the ground wire of
the ignition coil's harness**, which runs from the coil connector to a bolt
on the cylinder head. The repair replaces that wire and takes the coil's
ground on a new wire to the ground points **under the battery tray**
(repair wires `000 979 225 1` and `000 979 230 1`, butt splice
`111 971 939 B`, seal `357 972 741 B`). ⚠ **Not read from the bulletin
itself** — it is quoted, consistently, on newbeetle.org, vwvortex and in a
photographed repair on a 2002 Jetta; the part numbers come from those
reports. **The AQY is the European sibling of those engines and is not on
the bulletin's list**, and this car's coil is new but its harness is 26
years old. It makes the coil's own ground — ground 15 below — the first
earth to measure, not the last.

**Where the earths are.** A Golf/Jetta IV ground list (web.mit.edu/dennis,
from the US repair literature; **this car's own current-flow diagram in the
owner's manual is the authority** — the New Beetle shares the platform but
not necessarily every ground point). The ones on the engine's side:

| ground | where | carries |
|---|---|---|
| **1** | engine compartment, left, below the battery tray | battery negative to body |
| **2** | on the transmission, near the engine block | **battery negative to transmission/engine — the engine's main earth** |
| **15** | on the cylinder head | **ignition coils** |
| **608** | plenum, left centre, forward of the ECM | engine-compartment wiring harness (the ECM's harness ground on that list) |
| **609** | plenum, right, forward of the pollen filter | secondary air pump |

The knock sensors do not use a chassis earth: they are screened pairs back to
the ECM and bolted to the block (*general*). What matters for them is that the
ECM's own ground and the engine block sit at the same potential — which is
exactly what a poor ground 2 or 608 breaks.

**Two things at the battery, owner-reported, 9/2026:** the main red positive
cable is **chafed through right at the battery**, bare strands visible under
the heat-shrink, condition unknown; and the **battery cover is broken**, so
moisture can reach the terminals and the cable. A cable whose strands have
corroded or broken carries everything — starter, alternator, ECM, coil — and
only shows a drop under load (*general*). It heads the list below.

**The ECM's own view of its supply is in VCDS: block 004, field 2**
(`napájecí napětí`, specified 12.0–14.5 V in this ECU's label file). Logged together with the battery posts on a multimeter at the same
moment, the difference is the drop on the ECM's positive feed and ground —
with no connector to back-probe — and logged beside 014 it shows whether a
voltage dip lines up with a misfire.

**Which bad joint could cause the misfires directly, and which only
indirectly.** The primary symptoms are the misfires and the idle, so the
joints are ranked by how directly they reach the spark (*general*):

| joint | effect on the spark | rank |
|---|---|---|
| **coil ground** (connector pin → wire → eyelet on the head → engine → battery −) | direct: the coil pack's switching stage returns its current here; a poor ground weakens every spark it fires — the joint TSB 01-08-27 is about | **first** |
| **coil supply** (fuse → wire → coil + pin) | direct: less voltage, less energy per spark | **first** |
| HT leads seated on the coil towers and the plugs | direct, on the pair or cylinder concerned | first, by eye and hand |
| ECM ground and supply | indirect but real: the ECM times the coil's dwell and the injectors from the voltage it sees | second |
| main positive cable, engine earth strap, battery clamps | indirect: they only matter through the system voltage and the paths above | third |

So **start at the coil.** If both its joints and its leads are clean, the
electrical branch of H4 is largely answered, and the rest is the slower work.

**How the measurement works.** A voltage drop only shows while current flows
through the joint. The coil draws its current at every spark, so **the coil's
own joints are loaded at a plain warm idle** — no lights or fans needed, and a
few minutes of idle is enough for all of them. The main cable and the engine
earth are loaded by the alternator's charging current, which is why the later
tests switch the headlights, rear window heater and blower on. Meter on DC
volts; a long lead with crocodile clips so one probe can sit on the battery;
that probe on the **battery post itself**, not the clamp. The meter averages
the pulsed coil current, so the coil readings are small: **under ~0.1 V is
clean, several tenths is a bad joint** (*general*).

#### Step 1 — the coil (warm idle, secondary-air pump removed for access)

- **1a. Coil ground: battery − post → the coil's ground eyelet on the head**
  (ground 15).
- **1b. Coil ground: battery − post → the ground pin of the coil connector**,
  back-probed with the connector plugged in (a thin pin slid in beside the
  wire seal, not through the insulation). The **difference 1b − 1a is the
  wire TSB 01-08-27 replaces.**
- **1c. Coil supply: battery + post → the supply pin of the coil connector**,
  back-probed the same way. The pin assignment is in the manual's
  current-flow diagram; it is the one that reads battery voltage with the
  ignition on.
- **1d. Engine off: the HT leads.** Each one pushed fully home on its coil
  tower and its plug, the boots dry and uncracked. With the meter on ohms,
  the four leads against each other: one reading far from the others (for
  its length) is the bad one.

- **1e. Damp and dark: the high-voltage side.** Moisture makes a cracked
  coil housing or a worn boot leak its spark to earth instead of across the
  plug (*general*; one AQY owner in the Polish thread found his idle worse in
  wet weather, and the rough reading of 26/9 came on a foggy morning). On a
  damp evening, engine idling, bonnet open, lights off: look along the leads
  and the coil for sparks or a blue glow. Then a fine water mist from a spray
  bottle over one lead at a time: a stumble that follows the mist names the
  lead or the coil tower. Keep hands and the bottle clear of the HT side.

Clearing the secondary-air fault the removal sets is expected afterwards.

**Results, 26/9/2026, first pass** (warm, coil connector unplugged, pins
numbered from the left; *owner-measured*). Battery 12.23 V.

| pin | ignition on, V to battery − | ignition off, Ω to battery − | reading |
|---|---|---|---|
| 1 | 0.158 V | 0.7 kΩ | ECM trigger line |
| 2 | **12.02 V** | 552 kΩ | **supply** |
| 3 | 0.157 V | 0.7 kΩ | ECM trigger line |
| 4 | 0.009 V | **3.8 Ω** | **ground** |

- **Supply: 0.21 V lost with the coil unplugged** — i.e. with only the other
  ignition-switched consumers drawing through the shared feed (ignition
  switch, fuse, connectors). With the coil's own current added it can only
  be more; the running test (1c) is what sizes it.
- **Ground: 3.8 Ω is far too high for a ground path** if it is real — at the
  coil's current it would lose volts, not tenths. Not yet trusted: the meter
  lead resistance (R0) was not measured and a probe on the front of a female
  terminal makes poor contact. Split it: pin 4 → eyelet, eyelet → battery −.
- Flexing the chafed battery cable changed nothing (expected; it clears
  nothing).

**Second pass, same day, battery out and part of the intake off for access:**
**3.8 / 3.2 Ω was the measurement, not the car.** From the battery's own
negative cable clamp to pin 4: **≤ 0.4 Ω**; from the positive clamp to pin 2
with the key on: the same, ≤ 0.4 Ω (with the key off, kilo-ohms — the
ignition switch is in that path, which is exactly why the key matters); from
the negative clamp to the intake and various metal housings: < 0.4 Ω
everywhere. The earlier reading went through the extension lead's crocodile
clip on the battery post. ⚠ **An ohmmeter cannot see what is being looked for
here:** its floor is a few tenths of an ohm, while 0.21 V at a few amps is
~0.05 Ω. So this rules out a **gross** fault in the coil's ground and supply
— nothing like the TSB's broken wire — and says nothing finer. The running
voltage drops (1a–1c) are what can.

⚠ **The battery was disconnected for this**, so the ECM's adaptations
(032, knock references, idle) start again from zero — another boundary for
every before/after comparison (`vehicle-history.md`, *Before and after*).

**Running, 26/9, warm idle** (*owner-measured*; "loads on" = headlights, rear
window heater and blower on full). Back-probing the coil connector was
abandoned — its sleeve and seal are in the way, and the seal had already been
disturbed once — and **no ground eyelet for the coil was found on the head**:
the ground wire runs into the loom, probably to a splice shared with other
consumers and on to a point under the car. The Golf/Jetta list's "ground 15 on
the cylinder head" therefore does not hold for this car as seen. What was
measured instead:

| test | loads off | loads on | reading |
|---|---|---|---|
| battery − post → bare metal of the coil bracket (engine earth, 1a′) | 70–80 mV | 170–210 mV | **healthy**: ~0.1–0.13 V more for an estimated 30–40 A is a few milliohms for clamp, strap and engine together |
| battery + → battery − (2d) | 13.97 V | **12.72 V** | the alternator does not hold the loads at idle |

- **The engine's earth is clean.** Of the coil's ground path, only the thin
  wire from pin 4 to wherever it lands is not covered by a running
  measurement, and the ohmmeter showed it unbroken.
- **The voltage argues against H4 on its own.** With the loads on, the whole
  system — the coil's supply included — sits about 1.25 V *lower*, and that is
  exactly the state in which `IdleHealth` is *better* (35–50 against 70–80,
  S1). A spark weakened by supply voltage would do the opposite. Load on the
  engine, not volts at the coil, is what moves the idle.
- **12.72 V at idle with the loads on is its own question**, separate from the
  misfires: a healthy alternator at idle speed may simply not cover this much
  load, or the belt, the regulator or the chafed B+ cable may be losing it.
  Raised by hand at the throttle to roughly 2000–3000 rpm (not read) with the
  loads on, the battery came back to **13.4 V**: the alternator does charge,
  just short of the ~13.5 V a working system usually holds (*general*). Still
  open between a loaded alternator and a loss on the way — the B+ cable
  (battery + → alternator B+ nut, loads on, revs up) is what splits them.
- The headlights were lit with the switch off while the engine ran. Most
  likely the daytime running lights (fuse 27), which only run with the
  engine; not yet confirmed by switching the engine off with the key on.

#### Step 2 — only if step 1 is clean: the main supply path (warm idle, loads on)

Headlights, rear window heater and blower on full.

- **2a. Battery + post → the alternator's B+ nut** (the rubber-capped stud
  where the thick red cable ends; *general* for this engine family — follow
  the cable to be sure). Flex the chafed section while watching: a jump is
  broken strands. The starter cable carries nothing at idle and cannot be
  tested this way.
- **2b. Battery − post → the alternator's case** (or any bare bolt on the
  block): ground 2 and the clamp together. If high, split it: − post →
  − clamp, then strap lug → gearbox.
- **2c. Battery − post → body** next to ground 1, and **engine block → body.**
- **2d. Battery voltage** across the posts: roughly 13.5–14.5 V is a working
  charging system (*general*).

*General guidance for step 2:* under 0.2 V per path is healthy, over 0.3 V
is worth chasing, and every single joint should drop hundredths.

#### Step 3 — only if steps 1 and 2 are clean: the ECM (warm idle)

- **3a. Battery + post → the ECM's supply pins** (via the main relay) and
  **engine block → the ECM's ground pins**, back-probed; pins from the
  current-flow diagram for the AQY. Even a tenth is suspect here.
- **3b. Without a meter:** VCDS block 004 field 2 (the ECM's supply,
  12.0–14.5 V) logged beside 014 and `DisplayVolt` on the display, with the
  loads switched on and off. If the ECM's reading falls clearly more than
  `DisplayVolt` when the loads come on, the drop is on the engine side;
  whether a voltage dip lines up with a misfire shows at VCDS's ~0.3 s
  resolution. *On record, 25/9: `DisplayVolt` 13.9–14.2 V at a warm idle,
  peaks 14.2–14.5 V — the charging itself looks normal.*
- **3c. Without a meter, the chafed cable:** watch `DisplayVolt` while
  flexing it at idle with the loads on. A reading that moves only with the
  cable finds it; one that does not move clears nothing, because a steadily
  corroded section does not change with movement and the battery holds the
  system voltage on its side. Step 2a is what sees that.

Whatever reads high: clean to bright metal, refit at the manual's torque, and
**then** compare `IdleHealth` at the same oil temperature and repeat the
neutral 026 holds. **The leads fitted on 17/9 are NGK**, i.e. aftermarket
and not VW's thick originals. In the thread, NGK leads did not help its
original poster and one poster's new aftermarket (Beru) leads made his engine
misfire until he went back to the originals — a lead, cheap to test by
borrowing a genuine VW set.

### H5. Something in the cylinder 4 knock window that is not the engine's combustion (S4 + S5 only)

The ECU books anything it hears at cylinder 4's crank angle to cylinder 4.
Three candidates, all *general*:

- **G66, its 20 Nm torque or its connector.** VW's own table for one cylinder
  deviating: *connector corroded → check the knock sensors*. The torque is
  VW's figure; the connector needs gold-plated contacts.
- **A loose ancillary part** — VW's third row. Much has been off and back on
  in September: the rail, the MAF, the exhaust, the heater. A bracket that
  buzzes only in a speed band would explain the switch-on and the move to
  cylinder 1 above 3350 rpm. **The exhaust clamp was one candidate and it was
  not it.**
- **An injector click** that slides into the window as injection timing moves
  with speed. No knock log exists from before the new injectors.

| S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|
| — | — | — | ✔ | ✔ |

**Tests:** check G66's torque and connector; look over everything refitted in
September for a loose bracket, clip or heat shield with the engine held at
~3000 rpm in neutral; the stethoscope from H1 on the injector bodies of 4 and
1. **After each, repeat the neutral 026 + 003 holds** at the same oil
temperature: `vcds/vcds-neutral-026-003.csv` and `-clamp.csv` are the before.

**Is it worth chasing?** The retard is within VW's specification and costs a
moment of torque on cylinder 4. It matters for this investigation only if H1
or H4 turns out to be behind it.

### H6. Knock control relearning after the battery disconnects

The battery was off twice in one week. *General:* that resets the learned
knock references, and they come back over driving.

Explains the change **between** the two S4 logs (large tip-in events on 24/9,
small ones 100 km later). Does not explain S5, which is a raw voltage. **Test:**
log 020 + 026 again after a few hundred km without a disconnect; the tip-in
retard should stay small.

### H7. Fuel delivery at idle: rail pressure, one new injector

The regulator (7/2026) and the pump are the parts of the fuel path not
changed in September, and neither has ever been gauged. (The bad cold start
that once pointed here is closed, S7: it was the old injectors.)
The owner's own remaining candidate is one of the new injectors.

| S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|
| ~ | ~ | ~ | — | — |

- **Against, for the idle:** four new injectors and a new filter changed
  nothing in S1; the trims are near zero; a leaking seat adds fuel at idle and
  the trim would show it.

**Tests:**

1. **A fuel pressure gauge on the rail**: pressure at idle with the vacuum
   hose on and off. Settles the regulator in minutes. *General; VW's figures are
   not held here.*
2. If a cylinder is ever named (see *Naming the cylinder* below): swap its
   injector with another and see whether the fault follows.

### H8. Idle air control and the throttle body

**New here, not argued in the log.** Idle speed on this engine is held by the
electronic throttle and by ignition advance (the advance moving 0–9 °CA at
idle in group 003 is that control working). A dirty throttle body or a lost
throttle adaptation makes the governor hunt. *General.* The MAF swap halving
S1 shows that the idle is sensitive to how air is metered and controlled.

| S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|
| ~ | — | ~ | — | — |

- **Against:** a hunting governor is a slow oscillation, while S1 is a
  sudden dip lasting one or two firings and recovering in a quarter of a
  second — a combustion event, not a control loop.

**Test:** look into the throttle body; clean it if dirty and run the throttle
adaptation (VCDS basic setting). Compare `IdleHealth` at the same oil
temperature. Cheap, but it is last on the list because the shape of the dip
argues against it.

---

## Naming the cylinder — the missing measurement

**The idle fault has never been placed in a cylinder.** 014 on this ECU has no
per-cylinder counter, the bus carries no cylinder identification, and the
per-cylinder analysis of engine speed found ordinary cylinder-to-cylinder
variation rather than one bad cylinder (`refuted.md` A5). Knock
control names cylinder 4, but for a noise off idle, not for the stumble.

Naming it would split the hypotheses at once: one cylinder points at H1 or H3
at that runner; all four alike points at H0, H4, H7 or H8. Three ways to try,
all *general*:

1. **Exhaust runner temperatures at a hot idle**, with an infrared
   thermometer on the four manifold pipes close to the head, several minutes
   into a steady idle. A cylinder that misfires runs a cooler runner.
   Harmless, needs no tools beyond the thermometer.
2. **Cylinder balance by unplugging one injector at a time**, at a warm idle,
   for a few seconds each, watching engine speed. The cylinder whose removal
   drops the speed least is the weakest. ⚠ It sends unburnt air, not fuel,
   through the converter, but it does set a fault code to clear afterwards;
   keep each cut short.
3. **Plug reading after a few hundred km on the new plugs**, with the
   cylinder of each plug recorded this time. The old ones named 1 and 4, but
   that pair is also the old coil's output.

---

## The plan, cheapest and most decisive first

Each step names the hypotheses it tests. Every step that can have a capture
running beside it should have one, and every `IdleHealth` reading should have
the oil temperature beside it.

1. **The confirming readings, whenever the car is out anyway**: 032 after a
   few hundred km (S9; a positive idle cell would feed H3) and one held 4th-gear pull to 6000 rpm
   with `Power` on the display and a capture running (S8).
2. **Stethoscope and cold-start listening** — H1, H5. Free.
3. **The voltage-drop tests of H4, coil first**, then clean only what
   fails — H4, H5. A multimeter, then a wire brush.
4. **Spray test of the intake at a warm idle** — H3. A can of brake cleaner.
5. **Exhaust runner temperatures with an IR thermometer** — names a cylinder,
   splits everything. Cheap.
6. **G66 torque and connector, and a look for loose parts** — H5.
7. **Smoke/pressure test of the manifold and intake at the garage**, with
   the predictions under H2 held against the result — H2, H3. Already planned.
8. **Leak-down test warm, and a rail pressure gauge** — H1, H7. Garage work,
   do both on one visit.
9. **A healthy AQY recorded** — H0. Depends on finding one, so start asking
   now; it can happen at any point in this list and it changes how every other
   result is read.
10. **Throttle body cleaned and adapted** — H8, last.

**After each step:** `IdleHealth` at 70–72 °C and at 50–61 °C of oil against
the current band, and the neutral 026 + 003 holds if the step touched
S4/S5. If a step changes nothing, say so in the hypothesis and leave it; if it
kills a hypothesis, move it to `refuted.md`.

**Meanwhile:** the owner avoids long idles — the misfires are an idle
phenomenon and the exhaust has already paid for them once. `IdleHealth` on
0x604 is the trend to watch.
