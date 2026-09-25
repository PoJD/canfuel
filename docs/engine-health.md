# Engine health — what is still wrong, and how to find out why

**The working document for one open investigation into the engine itself.**
It holds only what is **unresolved**: the symptoms still present, the
hypotheses still standing, and the test that would confirm or kill each one.
It has an end date. When every symptom below is either fixed or shown to be
normal for this engine, the file is deleted.

| file | what is in it |
|---|---|
| **this one** | symptoms → hypotheses → tests → plan. Short on purpose |
| `engine-health-refuted.md` | every hypothesis **settled against**, with what settled it, plus the questions that were **answered**. Read it before proposing something: most obvious ideas are already there |

The long version this replaced, a dated log of 10–25 September 2026 with every
alignment and argument in full, is in git:
`git show 7c69883:docs/engine-health.md`. Nothing in the tree depends on it.

**Rules for this file.** A hypothesis that is refuted moves to
`engine-health-refuted.md` in the same commit, with its evidence, and leaves
this file. A new measurement goes into the evidence line of the symptom and of
every hypothesis it touches, not into a dated section. Owner reports are
marked *owner-reported*; general engine knowledge is marked *general*, since
none of it comes from a document this project holds.

⚠ **Nothing here changes a constant in `src/`.** The firmware only reports;
`IdleHealth` and the start bytes on 0x604 are one of the instruments used
below (`frames.md`).

---

## Where it stands — 25 September 2026

**Replaced so far:** coil (6/2026), exhaust from the flex pipe back including
the converter (9/2026), plugs and leads (17/9), all four injectors, fuel
filter (23/9), MAF (24/9). The regulator is from 7/2026. Compression is
12 bar on all four.

**Fixed by that:** the rich lambda trim (it was the MAF), the cold-overrun
burble, the long cranking, the historical full-load lamp. The car pulls better
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
of crank, one power stroke (`can-decoding.md` trap 6), so a dip is one
cylinder's stroke. At the warm idle of `09_idle_60s_z1` — 796 rpm, 326 µl/s,
about 18.5 Nm indicated — one power stroke is worth about 58 J. A cylinder
that produces nothing takes that out of the rotating assembly: **33–57 rpm for
an assumed 0.20–0.12 kg·m² of crank, flywheel and clutch** (the inertia is an
estimate, not measured). The deepest dips measured are 37.5–46 rpm, inside
that bracket; the typical one is 20–22 rpm, about half — a partial burn, or a
full misfire the sampling rounded off. The fall takes one or two firings and
the recovery about 250 ms, which is the idle governor, not a fuelling loop:
**the dip is the failed combustion itself, not the ECU correcting anything.**

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
on the 24/9 logs (`engine-health-refuted.md` A11, A12): it moves in steps of 12; detection switches off below about 20 % load, which on
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
  `engine-health-refuted.md`); only cylinder 4's excess over cylinder 1 is
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

### S7. The cold start — probably fixed, not yet proven

| | stand | injectors | crank to first firing | after first firing |
|---|---|---|---|---|
| `18_coldstart_z1`, 11/9 | ~10 h | old | 1.24 s | 451 → **311** rpm, nearly died |
| `19_postfix_drive_z1`, 24/9 | ~19 h, 10 °C | new | 0.83 s | 450 → **331** rpm, caught |
| `24_mafswap_drive_z1`, 24/9, 27 °C coolant | hours | new | 0.86 s | no fall |
| 25/9 morning, display | ~12 h | new | 0.77 s | clean |
| 25/9 warm, display | minutes | new | 0.70 s | no fall, `StartClt` 86 °C |

The first three are measured through `idledips.health_summary()`, the oracle
for 0x604; the 25/9 rows are *owner-reported* off the display. Cranking
shortened by a third on the new injectors; the fall has appeared only in the
two coldest starts.
**The next overnight cold start at under ~15 °C of coolant decides it**:
`StartCrank`, `StartDip` and `StartClt` on 0x604.

The same car, in 7/2026, **held no residual pressure** in the rail when the
regulator was changed. Nobody has checked that on the new parts.

### Other things around the engine, tracked elsewhere or not at all

- **Oil temperature never above 74 °C**, even after two hours of motorway. Is
  the channel right, or does the oil really run that cool? That is
  `can-decoding.md` question 10, and it may matter here: S1 depends on oil
  temperature, and a thermostat or oil-cooler question would move every
  temperature in this file.
- **Top-end breathing.** On the old MAF the car lost breath above 5000 rpm in
  4th. After the swap, full-throttle pulls "feel unchanged" and no held pull
  above 5000 has been logged. *Owner-reported*; open but not urgent.
- **Rich trim** — fixed by the MAF, but the confirming reading is owed: group
  032 after a few hundred km. It read −3.1 % / +4.7 % at the end of the first
  afternoon.
- **The remap.** The car was chipped in 2018. It is not going back to
  standard, and it is the caveat on every ignition argument here: whatever it
  did to part-load advance applies to all four cylinders.

---

## How the symptoms relate — what is measured

| pair | link | evidence |
|---|---|---|
| S1 ↔ S3 | **the same events** | aligned three times, p ≤ 0.023. Both are crank speed, so partly one signal read twice |
| S1/S3 ↔ MAF | **strong** | the MAF swap halved the dips at every oil temperature (−51 to −65 %). An over-reading MAF was causing some of the stumbles; the rest is the residual fault |
| S1/S3 ↔ oil temperature | **strong, non-monotonic** | worst at ~50–61 °C of oil, less cold, least hot. On every drive |
| S4 ↔ S5 | **very likely one thing** | same cylinder window, same engine speeds, and S5 needs no combustion. Knock control retards cylinder 4 because it hears S5's noise |
| S4/S5 ↔ S1/S3 | **none measured** | no retard and no 026 signal at idle, in any log. Only a common cause could link them |
| S2 ↔ S3 | **unknown** | never aligned in time. A misfire puffs and a leak puffs |
| S2 ↔ S6 | **possible** | if there is a leak ahead of the probes. The known leak is behind them |
| S5 ↔ S6 | **no** | the clamp was tightened and cylinder 4's excess stayed exactly as it was |
| S7 ↔ S1 | **none** | S7 improved with the injectors; S1 did not |

**So there are two separate clusters**, and they are worked separately below:
**the idle** (S1, S2, S3) and **the cylinder 4 window** (S4, S5). S6 matters
only if it leaks ahead of the front probe; S7 is on its way out.

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

- **For:** the **only candidate that can explain both clusters at once**: an
  intermittent leak past a valve at idle misfires, and puffs; a ticking lifter
  at camshaft speed lands in one knock window. Temperature-dependent through
  oil viscosity. Compression is a **cranking** test and does not see a valve
  that closes at 250 rpm but hangs at a hot idle.
- **Against:** S1 is worst at 50–61 °C and eases when hot, while a thin-oil
  lifter should be worst hot. The S5 excess switches on above ~2300 rpm and
  moves to cylinder 1 above ~3350, which fits a resonance better than a single
  part. No ticking has been reported.

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
  sensor averaging four. **A large leak is refuted** (`engine-health-refuted.md`);
  only a small one at one runner survives. It cannot produce S5.

**Tests:**

1. **Spray test at a warm idle**: brake cleaner or propane along the manifold
   gasket, the runner joints, the injector seats, the breather hoses and the
   vacuum lines, with `IdleHealth` or engine speed on the display. A leak
   shows as a change in idle at the spot. Cheap, no dismantling. *General.*
2. A smoke test of the intake at the same garage visit as H2.
3. 032 after a few hundred km: an idle cell moving positive would support it.

### H4. Weak spark at light load that is not in the parts (earth, wiring, coil connector)

All the ignition parts are new, so what is left is what feeds them. A poor
engine earth weakens the spark and adds noise to the knock-sensor signal.
*General*, and one of the fixes in a long Polish thread on exactly this
symptom on an AQY (forum.vwgolf.pl, t=522030 — a forum, so a lead, not a
source). The original poster's own fix there was a cracked exhaust manifold;
others were genuine leads, a Bosch coil, a holed breather hose, and the earth
straps.

| S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|
| ✔ | ✔ | ✔ | ~ | ✔ |

- **For:** the other candidate that could explain **both clusters**: a weak
  spark misfires at idle and high vacuum, and a noisy ground puts a signal
  into the knock channel that depends on engine speed. Cylinders 1 and 4 share
  one coil output (twin-spark coils, SSP 233 p. 5), and their old plugs were
  the worse pair.
- **Against:** the plug pair is better explained by the old coil. Nothing
  here measures the ignition.

**Tests:**

1. **Clean the engine earth straps** — engine to body, engine to gearbox,
   battery to body. A wire brush. Then compare `IdleHealth` at the same oil
   temperature and repeat the neutral 026 holds.
2. **Voltage drop engine block to battery negative while cranking**: more
   than a few tenths of a volt is a bad earth. A multimeter. *General.*
3. **Coil connector** and the ignition harness for corrosion.
4. **Swap plugs 4 and 2** and log 020 + 026 again: a change that follows the
   plug is the plug.

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

### H7. Fuel delivery at idle: rail pressure, check valve, one new injector

The regulator (7/2026) and the pump are the parts of the fuel path not
changed in September, and neither has ever been gauged. A rail that bleeds down overnight fits S7.
The owner's own remaining candidate is one of the new injectors.

| S1 | S2 | S3 | S4 | S5 | S7 |
|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | ✔ |

- **Against, for the idle:** four new injectors and a new filter changed
  nothing in S1; the trims are near zero; a leaking seat adds fuel at idle and
  the trim would show it.

**Tests:**

1. **A fuel pressure gauge on the rail**: pressure at idle with the vacuum
   hose on and off, then the drop over an hour after switching off. Settles
   the regulator and the check valve in minutes. *General; VW's figures are
   not held here.*
2. The next cold overnight start on 0x604 (S7).
3. If a cylinder is ever named (see *Naming the cylinder* below): swap its
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
variation rather than one bad cylinder (`engine-health-refuted.md` A5). Knock
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

1. **032 read again** after a few hundred km — one photographed screen.
   Confirms the rich trim is gone (closes a loop), and a positive idle cell
   would feed H3.
2. **Stethoscope and cold-start listening** — H1, H5. Free.
3. **Earth straps cleaned, and the voltage drop measured** — H4, H5. A wire
   brush and a multimeter.
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
kills a hypothesis, move it to `engine-health-refuted.md`.

**Meanwhile:** the owner avoids long idles — the misfires are an idle
phenomenon and the exhaust has already paid for them once. `IdleHealth` on
0x604 is the trend to watch.
