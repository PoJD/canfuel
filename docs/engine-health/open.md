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
| `plan.md` | **the planned fixes, in order**, and the rule that governs them: the idle first, no test for its own sake, as little idling as possible. Emptied step by step as the work is done |

The long version this replaced, a dated log of 10–25 September 2026 with every
alignment and argument in full, is in git:
`git show 7c69883:docs/engine-health.md`. Nothing in the tree depends on it.

**Rules for this file.** A hypothesis that is refuted moves to
`refuted.md` in the same commit, with its evidence, and leaves
this file. A new measurement goes into the evidence line of the symptom and of
every hypothesis it touches, not into a dated section. Owner reports are
marked *owner-reported*; general engine knowledge is marked *general*, since
none of it comes from a document this project holds.

**Every new observation of the owner's is checked against the symptom list,
and the owner decides.** When something new is reported — a sound, a smell,
a leak, a reading — say whether it could be a new symptom (or change an
existing one) and why, and ask. Do not add it as a symptom unasked, and do not
let it pass without asking.

⚠ **Nothing here changes a constant in `src/`.** The firmware only reports;
`IdleHealth` and the start bytes on 0x604 are one of the instruments used
below (`docs/firmware/frames.md`).

---

## Where it stands — 27 September 2026

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

**New on 26/9:** oil leaking at the back of the head (S10), and smoke with
possibly a hiss from the same place at a warm idle (S11). **S10's source is
found — the valve cover gasket**, heavily at the back and at the front as far
as the plug boots of cylinders 3 and 4 (S10). The owner replaces it with the
filler-neck breather in one job with the upper plenum gasket and a proper
refit of the injectors, **three of which have not been fully home since
23/9** (H3). Then the throttle body on its own (28/9, H8), then, if the
idle is unchanged, the garage for the exhaust. **The order is `plan.md`.**

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

**August's hot idle, examined, 27/9/2026** (*the owner's question: was
something done after August that made it worse?*).

- **It is one session, not two recordings.** `11` (A/C off, 48) and `12`
  (A/C on, 29) were taken minutes apart on 11/8 at 73 °C of oil; the A/C
  one being smoother is the load effect above. So the hot, loads-off
  August idle is **one 19 s hold grading 43–48**.
- **Against September at the same state.** `24` at 69–70 °C, loads off —
  the same torque at idle on 0x280 b7 (23 against August's 25) — cut into
  the same 22 s windows grades **53–106**, median about 75. August sits
  just below September's best window: unusual, not impossible by chance.
- **At mid temperature August was not better.** `09`, the same day at
  61 °C, grades 79–104 per window; `24` at 57–61 °C grades 48–89.
- **Not the old battery.** The idea that a dying battery loaded the
  alternator in August — a load, and load smooths this idle — is refuted
  by the bus: indicated torque at idle was 25 then and 23 now.

**On the same MAF, it did get worse** (*the owner's reading, 27/9: perhaps
August's one fault was the MAF, and something done since added another*).
The 2018 MAF was fitted until 24/9, so August and the morning of 24/9
(`19`, `20`, before the swap) share it. Hot, in 22 s windows: August
**43–48**; 24/9 **53–118**, median about 90 — and that with **more** torque
at idle (b7 41–51 against 25), which should have smoothed it. So between
11/8 and 24/9, with the MAF unchanged, the hot idle roughly doubled its
grade; the new MAF then took about a third of it back (53–106, and 57–100
off the display since). **That places the added cause in the table below,
minus the MAF** — and several of its rows were the owner's own work. One
limit: `19` and `20` came the morning after the 23/9 disconnect, with
every adaptation fresh from zero.

**What changed between 11/8 and the first September hot idle** — every item
on record, so nothing is overlooked:

| change | could it make only the hot idle worse? |
|---|---|
| **the secondary-air control line refitted, after 11/8** — in August it was off (P0411), so the combination valve could not open at all | **no — tested**: the line pulled off at idle, as in August, and `IdleHealth` did not move (below; `refuted.md` A8) |
| new battery, end of August | no — see above |
| converter, flex pipe, silencer and a new flange gasket, 10/9 | through a leak ahead of the probe (H2) |
| plugs and **NGK leads**, 17/9 | a lead that tracks (H4); the Polish thread's aftermarket leads |
| injectors and fuel filter, 23/9 — **fitted by the owner; three of four not fully home in the manifold** (`vehicle-history.md`), never leak-tested | **yes — the strongest candidate left**: H3, *The injector seats* |
| MAF, 24/9 | no — the idle got better with it (A11) |
| four battery disconnects — every fuel, idle and knock adaptation from zero | yes: relearning takes distance (H6) |
| the fuel: the tank was filled in September | a different batch; nothing specific |
| the weather: warm August, cool September | intake air temperature; nothing specific |

**The secondary-air line is already tested** (*owner-reported, 27/9/2026*):
the thin line from N112 to the combination valve was pulled off at a
running idle in the September work, recreating August's state, and
`IdleHealth` **did not change**. Date and oil temperature were not noted.
So that row is closed; `refuted.md` A8 carries it.

**The old leads are not kept** (*owner, 27/9*), so the August ignition
cannot be put back; a set of genuine VW leads is the only way to test the
NGK ones (H4).

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
and after it. **Long-standing: already there before the 10/9 exhaust work**,
like the rough idle (*owner-reported, 28/9/2026*). Not recorded, not timed,
never aligned with anything. It did
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
- **When the counts start after a cold start** (checked 28/9/2026, VCDS
  014 aligned on engine speed to the captures). **11/9** (`18`, old
  injectors): the first count **2 min** after the start at coolant 35 °C,
  oil 13 °C, then steadily from ~4 min (coolant 56–64 °C). **24/9** (`19`,
  the injectors fitted 23/9, old MAF): **3 min of cold idle with detection
  active and no count at all** (coolant 12 → ~48 °C); the first count at
  +584 s, coolant 90 °C, oil 43 °C, then many. The logs after the MAF
  swap (`24`) begin warm and cannot say. So on the car as it now is, **a
  cold idle without counts is not evidence of a fix.**

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

### S10. Oil leaking at the back of the head

*Owner-reported, 26/9/2026*, and pointed out earlier by a garage (when, not
recorded). Oil at the **back** of the head — the firewall side, where the
throttle body sits and the intake plenum is only bracketed to the engine,
with the exhaust manifold below it.

**Not the first leak.** The service record of **12/7/2018** lists a
dipstick, a dipstick cap and a seal written as *"těsnění ventilu"* — against
an oil leak (`vehicle-history.md`). **What the owner remembers of it**
(*owner-reported, 27/9/2026*; the paper is no longer kept): the job was the
dipstick — the narrow neck the dipstick goes into was cracked and leaked
oil — and the seal was probably the rubber the dipstick seats in. Not
certain. So **whether the valve cover gasket is the original one is not
known**; nothing on record says it was ever changed. ⚠ Oil at the dipstick
is also the classic sign of crankcase pressure (*general*), but **a cracked
neck leaks without any help**, so the 2018 leak is no evidence for H9's
blocked-ventilation branch. An earlier revision counted it as a weak point
for it.

**Source found, 26/9/2026 — the valve cover gasket.** *Owner-observed and
photographed*, engine off, in the evening:

- **at the back**, along the cover's edge and down onto the bracket and studs
  below it: wet oily grime, not dried residue — **it leaks heavily there**;
- **at the front, the plug side**: a wet line along the cover-to-head joint by
  the leads, and **a wet ring of oil around the plug boot at the head** on
  cylinders 3 and 4 only — the two at the right-hand end as the owner stands
  at the engine. *Corrected 28/9/2026:* this said 1 and 2 until then, because
  the owner had counted from the right; cylinder 1 is at the timing-belt end
  (`vcds.md`, *Cylinder numbering*);
- **the filler-neck breather** (`06A 103 465`): its lower body is visibly
  oilier than the cover around it, so its seat or O-ring probably weeps too;
- the breather hose to the intake looks sound from outside and was sprayed
  in the H3 test with no change;
- oily grime around the injector seats and the manifold flange below the
  plugs, read as oil running down from the cover. ⚠ The seats were **not**
  sprayed (*owner's correction, 27/9*; an earlier revision said they were).

⚠ **Correction:** an earlier revision said the plugs are on the front "so
this oil does not reach the plug boots". The photographs show that it does.

**What that changes.** The leak itself is now explained and needs no
hypothesis; what stays open is **why** (H9: a gasket this old leaks on its
own, a blocked ventilation makes it leak sooner) and **what the oil at the
plug boots does** — oil on a boot or on the plug's ceramic is a path for the
spark to track to earth, most of all when damp (*general*). ⚠ **It cannot
be the cause of S1/S3** (*the owner's point, 27/9/2026*): plugs and leads were
new on 17/9 with clean boots, and the idle and the misfires were no better
straight afterwards (`refuted.md` A2) — the fault was there before any oil
could have reached them. The ring seen on 26/9 is on those new leads, so oil
gets there within about nine days; **at most it adds to the stumble on 1 and
2** from now on, which is one more reason to clean up and not a lead on the
idle. Settled by what the boots and the plugs' insulators look like when
they come out.

**Why it is in this file and not only in the service list:** oil on the
exhaust manifold is a fire risk and the likeliest source of S11's smoke; and
*why* oil comes out can be the same thing that disturbs the idle — crankcase
pressure and ventilation (H9).

**How it closes:** the gasket and the breather are replaced (the owner's
job), the head and the plug area are cleaned, and the boots and plugs of 1
and 2 are photographed before cleaning. **Before taking anything apart**, at
70–72 °C of oil: a few minutes of `IdleHealth` as the before-value, and H9
test 3 (the filler cap) and a look at the dipstick — after a new gasket,
whether the crankcase was pushing oil out can no longer be told. Then S11 is
looked at again with the oil gone.

**Parts ordered 27/9/2026** (mlparts.cz, arriving the week after; matched to
the car by the shop's catalogue): valve cover gasket Elring `325.070`
(= `06A 103 483 C`); crankcase breather Febi `32452` (= `06A 103 465`);
oil filler cap seal Febi `100690` (= `06A 103 483 D`); upper intake manifold
gasket Elring `271.230` (= `06A 129 717`, the plenum has to come off for the
cover); sealant Elring `030.793`, Dirko HT beige (= VW `D 176 404 A2`), a dab
at the four points where the gasket's arches meet its straight runs. They go
into `vehicle-history.md` once fitted. **Added 28/9/2026, ordered:** the
throttle body Pierburg `7.03703.13.0` (= `06A 133 064 H`, H8) and a second
`100690` for under the breather.

**The exploded view, 27/9/2026** — the Bentley workshop manual for the
Golf/Jetta, *Cylinder head and valvetrain (2.0 l engine)*, page 15c-5,
figure N15-0205, *External cylinder head assembly*; found on the web by the
owner. Summarised here rather than kept: it is a commercial publication, the
same reason the VCDS label file is not in this repository. **The part being
replaced is item 18.** From top to bottom:

| item | part | the manual's note |
|---|---|---|
| 1 | cap | — |
| 2 | gasket | under the cap |
| 3 | vent housing — the breather, `06A 103 465` | **turn clockwise to remove** |
| 4 | nut | 10 Nm |
| 5 | gasket, under the vent housing | replace if damaged |
| 6 | bracket | — |
| 17 | oil deflector, under the cover | — |
| **18** | **valve cover gasket** | replace if damaged; **before installing, coat the joint between bearing cap 1 and the head with sealant** |
| 19 | valve cover | — |
| 20 | reinforcing strip, on top of the cover | — |

What it settles and what it moves:

- **The breather does sit on its own seal** (item 5), and the cap on
  another (item 2) — the question this paragraph used to leave open. The
  oily lower body of the breather seen on 26/9 is item 5's seat. **The
  ordered Febi `100690` is item 2**, the cap's: febi's own catalogue calls
  it *"Gasket for oil filler cap"* (partsfinder.bilsteingroup.com, febi
  `100690`, read 28/9/2026). A still from someone's replacement video,
  found by the owner, shows **the breather's underside, turned over** — the
  cross-ribbed bayonet that locks it into the cover, with a yellowish flat
  ring round it: item 5. (An earlier revision of this paragraph read the
  same still as the breather's top with the cap off; the owner corrected
  it — there is no cap opening there, only the bayonet.) **The cap locks
  onto the breather's top by the same kind of bayonet**, so item 5 may well
  be the same ring as item 2 — *a second-hand claim (another AI model,
  relayed by the owner), not checked against a VW catalogue*. **Owner's
  decision, 28/9/2026:** buy a second `100690` (ordered; the filler cap
  itself is kept — nothing in it to wear, never wet with oil), and settle
  it at the bench — if the second ring matches the old item 5, it
  goes under the breather. **Whether the new breather Febi `32452` comes
  with item 5 anyway is not known**: febi's catalogue gives no scope of
  delivery and its photograph shows the part black on black; the shop was
  asked (28/9, a public holiday).
- **"Turn clockwise to remove"** is the opposite of what a hand does by
  default, on a 26-year-old plastic housing. Worth knowing before the
  first attempt.
- **Where the sealant goes differs.** The plan above says a dab at the four
  arch points; the manual names **the joint of bearing cap 1 to the head**,
  the cam's front cap at the belt end, where the gasket crosses a split
  line. They need not conflict — that joint is one of the arch points — but
  the manual's is the one place it insists on. Its drawing is too small to
  say whether it wants the same at the back cap.
- The page gives **no torque for the valve cover's own nuts**. The 10 Nm on
  it belongs to item 4, the bracket's nut.

  **Decision, 27/9/2026 (the owner's): the cover nuts are tightened by hand,
  by feel** — evenly, until the gasket is lightly compressed and not
  squeezed out of shape, and without stressing the cover. Chosen over a
  torque wrench because no source this project holds gives a figure for
  these nuts: 10 Nm turns up in a web comment, which is not a source, and a
  video of the job did it by hand in exactly this way. The risk it accepts
  is an uneven or loose joint; the check is a look along the joint after
  the first warm run, and again after a few hundred km.

**The job itself — the work list, the first start and what follows — is in
`plan.md`**, step 1. *Owner's decision, 27/9/2026:* the cover gasket, the
breather and its seals, the upper plenum gasket, the injector refit
(H3, *The injector seats*) and the cleaning all in one job, with no
measurement between them. What it costs: an improvement afterwards cannot
be put down to one part. What stays separable all the same: S11's smoke
(the oil), the `--cylinders` pattern (the injector seats move f = 0.25,
not f = 0.50) and S4/S5 on cylinder 4 (H5).

**The before-values for the repair are the ones already in S1** — the warm
band at 69–72 °C of oil, loads off; the after-reading is taken the same way.
No separate cold baseline was taken.

### S11. Smoke, and possibly a hiss, at the back of the head at a warm idle

*Owner, by eye and ear, 26/9/2026*, warm idle, bonnet open, over the exhaust
manifold. A **faint smoke**; a **faint hiss** that the owner is not sure of;
whether it smelled of exhaust could not be told.

- **The smoke is something blowing out; the hiss need not be.** An intake
  leak makes no smoke, but it does hiss — a vacuum leak is heard as air
  being drawn in (*general*). ⚠ An earlier revision read S11 as "not the
  intake side" on the strength of the smoke alone, which conflated the two
  observations.
- **Three readings, not exclusive:** oil from S10 burning on the hot manifold
  gives smoke and no hiss; exhaust escaping at the manifold's joint to the
  head, the manifold itself or its flange gives a hiss, and can carry smoke —
  a leak **ahead of the front lambda probe**, H2; and **a vacuum leak at the
  back of the intake** gives a hiss with no smoke of its own — H3 or H9, in
  exactly the area the spray test left out. Smoke from the first and a hiss
  from the third together would look like what was seen.
- The rear of the intake and the old secondary-air vacuum line sit over the
  same hot manifold and were not sprayed in the H3 test, on purpose.
- **The gasket itself is an unlikely source of the hiss.** A leak hisses
  only across a pressure difference, and H9 test 3 found the crankcase at
  atmospheric — no suction at the cap, nothing at the dipstick. So after the
  new gasket the smoke is expected to go and **a hiss that stays is the
  exhaust or the intake**, H2 or H3; one that goes with the job was probably
  never there.

**How it closes:** the garage's smoke or pressure test from the head to the
front probe (H2) and the source of S10. *Checks the owner can make, left to
the garage by choice:* a rag held over the tailpipe for 2–3 s makes an
exhaust leak hiss louder (a phone recording at the head, since it is a
one-person job); an exhaust leak ticks loudest in the first minute after a
cold start; dry black soot at a joint is exhaust, wet oily grime is oil
(*all general*).

### S12. A hesitation on tip-in, and after a gearchange

*Owner-reported, 27/9/2026; added as a symptom at the owner's decision.*
When the pedal is pressed the car **almost always hesitates** — the engine
takes a moment and then pulls; *"spíš zaváhání"*, a hesitation rather than
a knock through the driveline — and the same after a gearchange. Long
present and lived with: the owner feeds the throttle in very gently over
the clutch. Not a new fault, a newly reported one.

⚠ S1 records the owner's earlier note that *"the hesitation that the old
MAF caused has gone"*. Whether that was this or a different one (at
cruise, say) is not recorded; this one is there on the new MAF.

**What it could share with the idle.** A tip-in starts from the same
state as the idle — the idle switch opening, the least air, the leanest
transient — so a cause at the bottom of the load range can show in both:

- **a lean tip-in**: air arriving before its fuel, worst with a leak past
  the MAF (H3) or low rail pressure (H7) (*general*);
- **the knock retard on tip-in** (S4): events of several °CA on cylinder 4
  at 960–2000 rpm, 13 of 16 on a tip-in after a coast — a retard is a
  moment of lost torque, which is what a hesitation is;
- **the spark under a sudden load** (H4), the moment cylinder pressure
  rises fastest;
- **the throttle** (H8) — checked off the bus on 27/9: its potentiometer
  shows no dead spot and no dropout, so not its track.

**Not the driveline**, on the owner's description: engine and gearbox
mounts give a knock or a lurch, not a pause in the engine's pull.

**How it is measured.** Nothing records it yet. A capture of deliberate
tip-ins — from a coast and after gearchanges, warm — with VCDS 020 (knock
retard) beside it, shows whether the pause lines up with a retard on
cylinder 4, with indicated torque (0x280 b7) lagging the pedal (b5), or
with a stumble in engine speed. `17`, `19` and `24` already hold tip-ins
and can be looked at first.

**First look at the tip-ins already held, 27/9/2026.** In `17`, `19` and
`24`, every point where 0x280 b5 leaves its rest value with the engine
running was taken, and kept only where the clutch was demonstrably engaged
— engine speed over road speed (0x1A0) within 6 % from 0.8 s before to
0.9 s after, above 15 km/h. That leaves **84 tip-ins**, nearly all from
`19` and `24` (warm), none from a standstill. The car's own acceleration,
from 0x1A0 over 0.3 s, was set against the ECM's indicated torque (b7).

- **The firm ones pull cleanly.** Where b7 rose by 100 or more within
  0.2 s (7 cases, 48–56 km/h), acceleration went from about −1.5 to
  +3…+5 km/h/s within 0.25–0.4 s and stayed there — **no dip, no pause** at
  this resolution.
- **The gentle ones are slow, but in proportion.** Most tip-ins here are
  small (b5 to 44–52), b7 takes 0.3–1 s to rise by 20, and the deceleration
  merely fades over 0.5–0.8 s. That can feel like a hesitation, and nothing
  in the data separates *slow because the pedal was gentle* from *slow
  because the engine was*.
- **Not reachable from these logs:** a pull-away, and the moment after a
  gearchange while the clutch is still slipping — where the owner feels
  it most — because engine speed then says nothing about the engine; and
  anything shorter than about 0.15 s.

**Reading:** no stumble is visible in 84 engaged tip-ins; the recorded
driving does not contain the event in a form these logs can show. **What
would:** a capture made for it — warm, 2nd or 3rd gear at a steady
1500–2000 rpm, clutch fully up, the owner's normal gentle tip-in five to
ten times, with a passenger pressing VCDS's log marker at each one that
*feels* like a hesitation, and 020 (knock retard) logged beside it. The
marked and unmarked tip-ins are then compared with each other, which needs
no healthy car.

### S13. The throttle runs its routine at every ignition-on

*Owner-reported, 28/9/2026; added as a symptom at the owner's decision.*
With the ignition left on and the engine not started, the throttle is
heard working for **20–30 s**, like seeking its stops — **at every
ignition-on**, not once after a disconnect; confirmed to come from the
throttle. Usually the engine is started straight away and the routine is
cut short. **The engine's fault memory is empty, and 17973 has never been
seen.** Whether it also did this after the June manual adaptation is not
remembered.

**Why it is a symptom:** VW's manual for this engine gives the adaptation
at most 10 s and repeats it at ignition-on only after an interrupted one,
storing 17973 / P1565 (H8, *What VW's manual says against that*). A
routine at every ignition-on is therefore either an adaptation that never
completes — the idle then running on unfinished values, which touches S1
— or this unit's own check, which the manual does not describe.

**What owners of this engine family report, searched 28/9/2026** —
forum-grade, not VW, and the fullest threads sit behind paywalls, so only
their search excerpts were read:

- **VW Vortex, Mk4 2.0 AEG** (the US sister of the AQY, same throttle
  family): a buzzing of **about 15 s at every ignition-on, then one
  click**, *"the sound of the throttle body trying to do a
  self-alignment"*, with the rider *"if you don't hear that noise when
  you turn the ignition on, your throttle body isn't aligning ... IT'S
  SUPPOSED TO MAKE THAT NOISE"* (*Throttle Body Noise - Help Please !*;
  *Throttle body - 5 sec noise when ignition turns on*). The AEG advice
  there: key on, do not start, *"you'll hear the throttle body
  aligning"*.
- **Czech and German forums** (Octavia 2.0, Golf 4) call a quiet whine
  from the throttle at ignition-on normal — the positioner's motor.
- **VW's own procedure after a disconnect** starts *"switch ignition on
  for at least 10 seconds"* before anything else — something happens in
  that time, though the manual does not say what.

**Reading: this is most likely the unit's normal routine**, and the
every-time part is what owners describe too. Two things stay open: the
**length** — owners say ~15 s (one thread 5 s), the owner here 20–30 s,
none of it timed — and **the click at the end**, which nobody here has
listened for. So S13 now rests on a duration, not on its existence.
**The click is there** (*owner-reported, 28/9/2026*), at the end of every
run; the length was never timed, so ~15 s is possible. The owner keeps it
open all the same: the forum's "normal" could be a normal of throttles
that are already worn, and only a new part settles that.

**How it closes** (`plan.md` tests 1 and 2), timed each time: the old
part before the job; the old part after test 1's adaptation, which has
certainly completed; the new part after its own adaptation in test 2.
**New part silent, or clearly shorter → the old unit differed**, and S13
becomes a lead on it (H8). **The same routine → it is how these parts
behave**, and S13 closes as normal.

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
| S10 ↔ S11 | **likely, not shown** | same place; the valve cover gasket leaks heavily at the back, above the manifold, and oil on a hot manifold smokes. The hiss, if real, is not oil |
| S11 ↔ S2 | **possible** | an exhaust leak ahead of the probe both hisses and puffs. Never observed together |
| S11 ↔ S6 | **possible** | if the hiss is exhaust, "never tight" reaches upstream of the probes too |
| S10/S11 ↔ S1/S3 | **untested, not weak** | nothing measured so far *could* have shown a link, so "unknown" is no evidence against one. Oil outside the engine does not touch combustion; what can is the cause or a neighbour: a vacuum leak at the unsprayed rear hissing (H3/H9), the ventilation's oil fouling the throttle (H9 → H8), an exhaust leak ahead of the probe (H2), oil reaching a lead boot (H4, 1e) — seen on 26/9 at the boots of 3 and 4, but **not a cause**: the idle was as rough on 17/9 with new, clean leads (S10). The one existing datum that points this way: the idle is better under load, which is what a small unmetered leak does |
| S12 ↔ S4 | **possible, untested** | the knock retard is a tip-in event and a retard is lost torque. Never aligned in time |
| S12 ↔ S1/S3 | **possible, untested** | both start from the bottom of the load range; a lean or weak-spark cause would show in both |
| S13 ↔ S1 | **possible, untested** | an adaptation that never completes leaves the idle control on unfinished values (H8). Answered by the new part's adaptation |

**So there are two separate clusters**, and they are worked separately below:
**the idle** (S1, S2, S3) and **the cylinder 4 window** (S4, S5). S6 matters
only if it leaks ahead of the front probe; S7 is closed, and S8 and S9 each
want one confirming reading and are probably closed. **A third cluster, the
back of the head (S10, S11)**, appeared on 26/9 and goes to the garage as its
own job; whether it joins the idle cluster is exactly what H2 and H9 ask.

---

## The open hypotheses

Each one lists what it explains, what speaks against it, and the test that
settles it. ✔ fits, ~ fits weakly, ✘ does not fit, — says nothing.

**The columns are the open symptoms that bear on the engine.** Left out,
each for a stated reason: **S6** (the exhaust's joint behind both probes —
acoustic; the part of it that matters is H2's), **S7** (closed), **S8**
(probably not a fault), **S9** (fixed by the MAF, one confirming read
owed). S12 and S13 were added on 28/9/2026: **S12**, the tip-in
hesitation, fits a lean tip-in (H3/H9, H7), a moment of knock retard (H5)
and weak spark under sudden load (H4); **S13**, the throttle's routine, is
H8's alone.

### H0. The idle is normal for this engine — and there is no fault to find

**The one hypothesis nobody has been able to test.** An AQY with 26 years on
it might simply idle like this, and every number above might be its normal
state.

| S1 | S2 | S3 | S4 | S5 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ✘ | — | ~ | — | — | — | — |

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

**Searched for on the web, 27/9/2026 — nothing usable exists.** Nobody was
found to have published a recording of a healthy AQY's idle in any form that
compares with this car's:

- **VCDS**: no posted 014 (or 015/016) readings from a healthy AQY or a
  sister engine at a warm idle. The forums quote VW's `0...5` and "zero or
  near zero on a good engine" as general advice; the only AQY figures posted
  are from engines with a fault. The specification stays the only target.
- **Video**: Golf 4 2.0 drive videos exist, but an idle heard through a
  phone is not a number, and none is labelled as a known-good engine.
- **CAN**: comma.ai's public `commaCarSegments` dataset (MIT licence, raw
  bus captures from openpilot users) has **no PQ34 car**; its one PQ
  platform is the Passat NMS, whose powertrain bus carries 0x280 in the same
  format (`opendbc` `vw_pq.dbc`, `Motor_1`, 0.25 rpm). All 33 of its
  segments were read, with `tools/idledips.py` run on the six standstill
  idles found (11–28 s each, ~800 rpm, coolant 88–103 °C). **It does not
  compare**, for a reason worth keeping: that ECU **recomputes engine speed
  every 10 ms frame and smooths it** — `--degrees` reads 49° at idle, not
  180°, steps are at most 3 rpm per frame against up to 16 here, and the
  grade reads exactly 0 on every hold because no step clears its deadband.
  A per-power-stroke signal is a property of this car's Motronic, not of
  0x280, so **`IdleHealth` means something only on an ECU that holds engine
  speed per stroke**, and a donor car for test 1 should be checked with
  `--degrees` before its grade is believed. (For the record, its dip counter
  read 0–1 per hold at 20 rpm; on a smoothed signal that says nothing.)

### H1. A lifter or valve on one cylinder at a hot idle (valvetrain)

A hydraulic lifter that bleeds down or pumps up leaves a valve slightly open
or late, intermittently, and gets worse as the oil thins. *General.*

| S1 | S2 | S3 | S4 | S5 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ✔ | ✔ | — | — | — | — |

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
- **From a German AQY thread** (pkw-forum.de, *Ölverbrauch und
  Zündaussetzer beim 2,0 ltr-Motor AQY*, 2003–2015): a Golf with misfires
  whose head came off to find **a bucket tappet sticking intermittently**
  (*"dass ein Tassenstößel zeitweise klemmte"*); the head was replaced and
  VW paid 40 %. The same thread has AQYs burning up to a litre of oil per
  1,000 km and misfiring on cylinder 2. A forum report, 2003, and the only
  one found where the cause was named in the valvetrain.
  **That thread's oil-burning pattern is not this car's**: oil changed in
  6/2026, never topped up since, and still at the upper mark on 27/9
  despite the leak (`vehicle-history.md`) — over about 700 km, so a
  consumption of a couple of decilitres per 1,000 km could hide in it; a
  litre could not. A sticking tappet needs no oil consumption, so this takes
  nothing from H1 itself.

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

### H2. A leak ahead of the front lambda probe (exhaust manifold, its joint to the head, probe boss)

At idle the exhaust pulses dip below atmospheric and a crack draws air in;
under load it only blows out. *General.* The front probe reads lean, the rear
loop absorbs it, so 032 barely moves (SSP 233 p. 16, the two-loop control).

| S1 | S2 | S3 | S4 | S5 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|
| ~ | ✔ | ~ | ✘ | ✘ | — | ✔ | — | — |

- **For:** the puff, idle only, an old manifold that has lived through years
  of misfires, the rear probe on the rich side at hot idle
  (0.665–0.725 V), the exhaust never having been tight.
- **Where "ahead of the probe" is, 28/9/2026** (*owner-observed*): the
  front probe sits **on the manifold itself**, and the pipe fitted on 10/9
  starts at the manifold's outlet (`vehicle-history.md`). So the zone this
  hypothesis is about is only the **original manifold, its gasket to the
  head and the probe's boss** — all 26 years old. The outlet flange and its
  new gasket are downstream of the front probe and outside it. (An earlier
  revision counted the new flange gasket *for* this hypothesis.) It fits
  the owner's account that the puff and the rough idle are both older
  than the 10/9 exhaust work, as are August's 014 counts.
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

**S11 is the first physical sign for this hypothesis** (26/9): smoke and
possibly a hiss over the exhaust manifold at a warm idle. The smoke alone is
more likely S10's oil; **the hiss, if the garage confirms it, is this leak.**
Nothing else about the argument above changes until the test is done.

### H3. A small unmetered air leak at one intake runner

Air past the MAF leans one cylinder at idle, where air flow is smallest.
*General.*

| S1 | S2 | S3 | S4 | S5 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|
| ✔ | ~ | ✔ | ~ | ✘ | — | ~ | ✔ | — |

- **For:** the regime is exactly right. A lean cylinder can also knock on a
  tip-in (S4). Several of the forum cases were a breather hose. The idle is
  better the more air goes through the engine (S1, *load at idle*), which
  dilutes a fixed leak.
- **S11 fits half:** an intake leak makes no smoke, but it hisses, and the
  back of the intake is the part the spray test did not reach. What sits
  there is for the garage's smoke test to list; the brake-servo vacuum line
  and the old secondary-air vacuum line are the usual candidates on an engine
  of this age (*general*, not checked against this car).
- **Against:** the idle trim is −3.1 %, slightly rich, and a leak big enough
  to misfire one cylinder would still pull the trim positive through one
  sensor averaging four. **A large leak is refuted** (`refuted.md`);
  only a small one at one runner survives. It cannot produce S5.
- **VW's own leak signs, checked 28/9/2026** (`vcds.md`, VW's manual):
  idle air mass is 3.1–3.5 g/s against 2.0–5.0, where VW's sign of
  unmetered air is *below 2.0*; 055's learnt value read −0.73 g/s on 11/9
  against −1.50…1.50, and VW says a run-in engine sits negative. Neither
  is near a limit, so both agree with "no large leak" and **neither can
  see a small one**. The 055 reading also predates 23/9, so it says
  nothing about the injector seats.

**Tests:**

1. **Spray test at a warm idle**: brake cleaner or propane along the manifold
   gasket, the runner joints, the injector seats, the breather hoses and the
   vacuum lines, with `IdleHealth` or engine speed on the display. A leak
   shows as a change in idle at the spot. Cheap, no dismantling. *General.*
2. A smoke test of the intake at the same garage visit as H2.
3. 032 after a few hundred km: an idle cell moving positive would support it.

**The injector seats — three not fully home, 27/9/2026.** *Owner-reported
and photographed:* since the 23/9 refit, three injectors stand **under
about 1 mm** proud of their bosses; only cylinder 4's is
fully home, and an old injector alone clicked fully into every bore
(`vehicle-history.md`). The manifold-end O-ring is all that seals them.

**Against the data** (*general* for how a seat leak behaves):

- **It fits the timing.** On the same MAF, the hot idle graded 43–48 on
  11/8 and 53–118 on the morning after the refit (S1) — the injectors are
  in that window, and they were the day before.
- **It fits the load effect.** Air leaking at a seat enters the port
  directly, past the MAF, and is largest against the highest vacuum — at
  idle. More load means more metered air, so a fixed leak weighs less.
- **It fits A5.** Three cylinders leaking alike leave no one cylinder
  dominating the per-cylinder analysis.
- **It fits S12.** A lean port misfires or stumbles on a tip-in first.
- **It does not explain everything:** the idle stumbled and 014 counted
  before 23/9 too (August at mid temperature, the cold start of 11/9).
  At most it is the **added** cause S1 asks for.
- **What speaks against:** a proud injector need not leak — the O-ring
  may still sit in the bore; and the idle trim after the MAF swap read
  **−3.1 %**, rich, where three leaking seats would push it positive. That
  read was taken on the first afternoon of an adaptation learning from
  zero, and the battery was off again on 26/9, so it is weak.

**What settles it:** the 032 idle cell after a few hundred km without a
disconnect (S9) — positive supports a seat leak; the smoke test with the
engine off, which reaches the seats safely; and the refit itself, each
injector home on its own before the rail goes on, with the O-rings looked
at for a nick from being forced, then `IdleHealth` at 70–72 °C against
57–100. It goes together with the valve cover job, by the owner's
decision (`plan.md`, step 1): the cure is wanted more than the
attribution.

**Spray test, 26/9/2026** (contact cleaner — isopropanol and C6–C7 alkanes;
warm idle, loads off, engine speed watched): **no change** — but it covered
**the hoses only**: the MAF-to-throttle hose and the other hoses in reach
at the front. ⚠ *Owner's correction, 27/9/2026:* the injector seats, the
area round the plugs, the throttle body's joints and the manifold's runner
joints were **not** sprayed, for fear of spraying near the ignition on a
running engine — an earlier revision listed them as sprayed and clean. **The
injector seats, refitted by the owner on 23/9, are untested**; the smoke
test after the valve cover job covers them, with the engine off.
The rear of the manifold, and the small vacuum line that used to serve the
secondary-air valve, were **not** sprayed: they sit above the exhaust
manifold, which is no place for a flammable spray. The open secondary-air
intake port is ahead of the MAF and counts as metered air, not a leak.

### H4. Weak spark at light load that is not in the parts (earth, wiring, battery, coil connector)

**Verdict after 26/9/2026: much weakened, not refuted — kept here, last in
line.** Measured and clean: the coil's ground and supply for a gross fault
(ohms), the engine's earth under load (running voltage drop), the charging.
And the strongest point is not a measurement of a joint at all: **the idle is
better with the loads on, when the whole system — the coil's supply included —
sits 1.25 V lower.** A spark limited by supply would go the other way. Not
measured, and why it stays open rather than going to `refuted.md`: the running
drop on the thin wire from coil pin 4 to its splice (no back-probing, and its
earth point was not found), and the ECM's own supply and grounds (608), which
matter for the knock-sensor signal (S5) more than for the spark. Results in
full under *Step 1* below.

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

| S1 | S2 | S3 | S4 | S5 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ~ | ✔ | — | — | ~ | — |

- **For:** with H1 the only candidate that could explain **both clusters**: a
  weak spark misfires at idle and high vacuum, and a noisy ground puts a
  signal into the knock channel that depends on engine speed. Cylinders 1 and
  4 share one coil output (twin-spark coils, SSP 233 p. 5).
- **Against:** nothing here measures the ignition. (The old plugs were once
  cited here as "1 and 4 the worse pair"; they were never labelled, so which
  plug was worst is not known — `refuted.md` A9.)

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

⚠ **"Plenum" in this list is the plenum chamber** — the body's water tray
under the windscreen base, where the ECM and the pollen filter sit — **not
the intake plenum** (the upper intake manifold). The pollen filter in 609's
row is what gives it away. An earlier revision of `plan.md` looked for 608
on the intake plenum while it was off.

**This engine's own current-flow diagram, 28/9/2026** (VW's Golf 2003
diagrams for the 2.0 l / 85 kW Motronic, AQY, as transcribed on
portal-diagnostov.com; the drawings themselves are behind a login, only
the legends were read): **608 is "Earth point, in centre of plenum
chamber"**, and the ECM J220 is "in centre plenum chamber" — so 608 sits
by the ECM in the middle of the water tray, not left of centre as the US
list has it. The ignition page's legend (N152, the coil pack) **names no
earth point**, so where this car's coil is earthed — ground 15 on the head
in the US list — is still not confirmed for the AQY. *Practical, general
VW convention:* earth wires are **brown**; following the brown wire out of
the coil's connector finds its earth, and following the battery's negative
cable finds ground 2.

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

  **While there, look for S10's oil on the coil and the lead boots.** Oil
  softens rubber and holds dirt and water, which is how a boot starts to
  track (*general*) — the one way the leak itself, rather than its cause,
  could reach the spark.

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
- **The B+ path, measured** (battery + post → alternator B+ stud, loads on;
  the B+ nut had just taken a slight further turn): **160 mV at idle, 360 mV
  at raised revs**, battery 13.4 V as before. So the alternator's own terminal
  sits at about 13.75 V and **roughly a third of a volt is lost on the way to
  the battery at full charge current** — over the ~0.3 V worth chasing
  (*general*), in the path that holds the chafed cable. It is a charging
  question and not a misfire one: the coil is fed through the ignition switch,
  not through this cable, and the idle is better, not worse, when the loads
  drag the whole system down. Where in the path it sits — the eyelet at the
  alternator, the cable, or its landing at the battery — is split by
  measuring each piece the same way.
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

| S1 | S2 | S3 | S4 | S5 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|
| — | — | — | ✔ | ✔ | — | — | ~ | — |

**Tests:** check G66's torque and connector; look over everything refitted in
September for a loose bracket, clip or heat shield with the engine held at
~3000 rpm in neutral; the stethoscope from H1 on the injector bodies of 4 and
1. **After each, repeat the neutral 026 + 003 holds** at the same oil
temperature: `vcds/vcds-neutral-026-003.csv` and `-clamp.csv` are the before.

**The seated injector is cylinder 4's, 27/9/2026.** Since the 23/9 refit
only cylinder 4's injector is fully home; 1–3 stand up to about 1 mm proud
on their O-rings (`vehicle-history.md`). **And every knock log — S4's 022/023
and 020, S5's 026 — was taken after that refit**, on 24–25/9; there is no
knock log from before it. So *the only knocking cylinder is the only seated
injector* is a coincidence nothing yet separates from a cause, and the
third candidate above gives the cause a mechanism (*general*): an injector
bottomed in its boss is coupled rigidly to the manifold and the head, one
floating on its O-rings much less, so **only injector 4's click would
reach the knock sensor strongly** — and an injector's click moves through
the crank-angle windows as injection timing moves with engine speed, which
is what S5's excess does when it slides to cylinder 1 above ~3350 rpm. A
lean cylinder cannot be the route here: cylinder 4 is the one that is
*not* proud.

**Why a click would show on tip-ins and not in steady driving**
(*general*: how knock control works on engines of this kind, not read for
this ECU). The knock sensor hears everything — valves, injectors, the
timing gear — so the ECM does not judge loudness. For each cylinder it
learns the normal noise level in that cylinder's window and calls knock
only when the signal **jumps** above it. A steady click is learned and
ignored; a click that **appears suddenly** is not, until the level catches
up. That is S4's pattern: 13 of 16 events on a tip-in **after a coast or a
gearchange**. On the overrun the ECM cuts injection, the injectors fall
silent and the learned level drops; on the tip-in they start again at
once, and a click well coupled into the block — injector 4's — lands above
the level just learned. It also reads the full-throttle events of 25/9
without strain: injection quantity, and so the click, grows fastest there.

**What to expect with all four seated.** Steady driving: nothing — every
click is learned as noise. Tip-ins after a coast: either the events spread
or move — an injector's click need not fall in its own cylinder's window,
it falls where injection timing puts it — or nothing changes and stays on
4, which clears the injectors. Nothing here harms the engine either way:
the retard is inside VW's 0–15 °CA.

**What settles it, at no extra cost:** the neutral 026 + 003 holds
(`vcds-neutral-026-003.csv` is the before) and a 020 drive with the same
tip-ins after coasts as on 24–25/9, repeated
**after the injectors are refitted all four home**. If S4/S5 were injector
4's click, the excess moves or spreads once 1–3 are seated too; if it stays
on 4 alone, the injectors are cleared from it. Before the refit, the
stethoscope on the body of injector 4 against 1 at ~3000 rpm in neutral
is the direct look.

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

| S1 | S2 | S3 | S4 | S5 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | — | — | ~ | — |

- **Against, for the idle:** four new injectors and a new filter changed
  nothing in S1; the trims are near zero; a leaking seat adds fuel at idle and
  the trim would show it.

**Tests:**

1. **A fuel pressure gauge on the rail**: pressure at idle with the vacuum
   hose on and off. Settles the regulator in minutes. *General; VW's figures are
   not held here.*
2. If a cylinder is ever named (see *Naming the cylinder* below): swap its
   injector with another and see whether the fault follows.
3. **The injector harness, engine off, during the valve cover job** — when
   the plenum is off and the rail's wiring is in reach for once. The
   injectors are new, but **the harness to them is 26 years old**, and an
   intermittent break or a chafe at idle vibration is exactly the fault
   that no part swap reaches and that the ECU need not log. *General*
   methods; no pinout or resistance figure for this car is held here, so
   every test compares the four cylinders with each other.
   - **By eye, under the sleeving**: insulation that is cracked, brittle,
     oil-soaked or rubbed through, especially where the loom bends or
     touches the head or the manifold; the four connectors' seals and
     locking clips; green or white corrosion on the pins. Photograph what
     is found before touching it.
   - **Injector winding, connector unplugged, meter on ohms** across each
     injector's two pins: the four should read alike. One far from the
     others is that injector; the absolute value is Bosch `0 280 155 791`'s
     and is not written here without its data.
   - **Each wire for a break**, key off: from each connector's two harness
     pins to where they go — one is a supply common to all four, the other
     runs alone to the ECM, pins per the current-flow diagram. **While
     measuring, flex the loom along its length**: an ohmmeter cannot see a
     slightly high joint (see H4's second pass), but a reading that jumps
     to open as the loom moves is the fault.
   - **Each wire for a chafe to earth**: harness side, injector unplugged,
     each pin to bare engine metal. With the ECM connected the reading goes
     through it, so it is compared between cylinders, not against a
     number: one pin reading near zero where the other three read high is
     a wire touching earth.
   - **Running, afterwards (optional):** at a warm idle, flex each
     connector and the loom by hand while watching `IdleHealth` or the
     engine note. A stumble that follows the hand names the place. Keep
     clear of the belt and the HT leads.

   **First look, 26/9/2026 evening** (*owner's photograph*, in the dark, one
   injector on the right-hand end — cylinder 3 or 4, not certain which):
   the two wires into the connector are wrapped in old tape, grey with oil
   and dirt and lifting in places. An orange patch where the tape stops
   short of the connector is **the wires' own insulation, not bare copper**
   (*owner-checked*). Nothing there looks damaged; the other three
   connectors and the loom under the sleeving are still to be looked at.
   Beside the injector a bare threaded stud carries no nut — whether one
   belongs there is not known.

### H8. Idle air control and the throttle body

**New here, not argued in the log.** Idle speed on this engine is held by the
electronic throttle and by ignition advance (the advance moving 0–9 °CA at
idle in group 003 is that control working). A dirty throttle body or a lost
throttle adaptation makes the governor hunt. *General.* The MAF swap halving
S1 shows that the idle is sensitive to how air is metered and controlled.

| S1 | S2 | S3 | S4 | S5 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|
| ~ | — | ~ | — | — | — | — | — | ✔ |

- **Against:** a hunting governor is a slow oscillation, while S1 is a
  sudden dip lasting one or two firings and recovering in a quarter of a
  second — a combustion event, not a control loop.

**Already done once:** in 6/2026 the throttle body was inspected, found
clean, given a new gasket and adapted (`vehicle-history.md`), and the idle
fault outlived it.

**A hard protrusion on the throttle's flange face, from the owner's
photograph of 23/6/2026** (the June cleaning; found in the photos on
28/9/2026): at the **lower left of the throttle body's mating face**, a
small raised point that stayed after the face was cleaned — *"suspiciously
hard"*, like baked-on remains of the original gasket or a flaw in the
casting (*owner-observed*). **If it held the new June gasket off the face,
air could pass round the gasket into the plenum — behind the plate, so
unmetered**: a small leak of exactly H3's kind, present since June and
possibly before. Weighed honestly: one point on a soft gasket may seal
anyway, and the photograph cannot show whether it did. The phone
screenshot is not kept here; **proper photographs come when the throttle
is off in `plan.md` step 2**, of both faces.

⚠ **What it does to step 2's reading:** the swap now changes two things —
the throttle *and* this joint (a new part's clean face, a new gasket). So
an idle fixed only by step 2 names **the throttle or its flange**, not the
throttle alone. The air-against-angle curve can separate them: a sealed
flange leak moves the idle **along** the curve (more air through the MAF,
the plate further open), a different throttle moves the curve itself.

**Test:** look into the throttle body again; clean it if dirty and run the
throttle adaptation (VCDS basic setting). Compare `IdleHealth` at the same oil
temperature. Cheap, but it is last on the list because the shape of the dip
argues against it.

**How a clean throttle could still do it** (*general*, asked 27/9/2026). At
idle the plate is **almost closed** — all the idle air passes through a gap
of a degree or two at its edge — so it is the smallest opening, not the
bore, that matters. Three ways, none of them dirt:

- **The position sensor worn at the idle position.** The plate spends most
  of its life at that one angle, so a potentiometer's track wears there
  first; a worn spot gives a noisy or jumping angle exactly at idle, and
  the ECM corrects for movement that is not happening. The electronics and
  the real angle then disagree, as the owner put it — only at idle.
- **The idle actuator's motor or gears worn**: play or sticking makes the
  plate move late or in small jumps, and the governor hunts.
- **Wear of the plate edge or the bore** where it seals at idle: an air
  gap the adaptation does not expect; the adaptation absorbs a fixed one,
  but not one that moves.

The same argument against applies to all three: they disturb **control**,
which is a wander over seconds, while S1 is a single firing that fails.
**What would show it:** VCDS 003's throttle angle logged at a warm idle
beside the engine speed — an angle that twitches or jumps without cause,
or moves in step with the dips, is this hypothesis; a steady one clears
it. **The throttle is cable-operated** (*owner-observed, 27/9/2026*: a cable
runs from the pedal to it), so idle is held by an actuator moving the plate
inside the idle range, and the angle VCDS reports is the ECM's own sensor.

**Checked against the logs already held, 27/9/2026** —
`vcds/vcds-postfix-drive-003-014.csv` (003 with 014, the drive of
`19`), and the 003 columns of `vcds-01-002-003`, `vcds-ride-002-003`,
`vcds-neutral-026-003`, `-clamp` and `vcds-knock-020-026-003`; idle taken
as 650–950 rpm with air mass under 4.5 g/s. Each group is read about every
0.6 s.

- **The angle is steady at a warm idle.** Between consecutive readings it
  is unchanged about three times in four, and otherwise moves by **one
  display step (0.4–0.5°)**; larger steps are rare and sit at transitions
  into or out of idle. No twitching, no jumps — in every log, August's
  included.
- **The misfires do not ride on it.** Over the drive's idles the counter
  rose 36 times, and in almost every case the angle was the same before and
  after.
- **A pattern that is not this hypothesis:** no misfire was counted at the
  cold idles, where the ECM held the plate at 3.0–3.9°, and they came at the
  warm idles at 0.9–2.6° (detection active throughout). That is S1's own
  shape — more air, and the temperature dependence — with the two
  confounded; it says nothing about the throttle being at fault.

**The potentiometer's track, off the bus, 27/9/2026.** With a cable
throttle the ECM has no pedal sensor, so the driver's demand it puts on
0x280 b5 can only come from the throttle body's own potentiometer
(*reasoned from the layout, not read off a diagram*). Over `17`, `19` and
`24` — about 540,000 frames at 10 ms — a worn track would show as dropouts
or jumps. It shows neither:

- **no single-frame spike anywhere** (a value leaving both neighbours by
  three counts or more and coming straight back);
- off rest, consecutive frames move by 0 or 1 count (0.4 %) almost always;
  the larger steps are the pedal moving fast;
- **every value from 41 to 212 occurs** — no dead spot along the track.
  The only thin zone is 39–42, straight after the rest value 38, and that
  is the switch from idle to driving, not wear (*Driving gate* in
  `CLAUDE.md`: nothing between 38 and 44 in any log).

The ECM may filter the value before sending it, so a glitch shorter than a
frame or two could be smoothed away; a track worn enough to disturb the
driving would not be.

**What VW's repair manual says about this throttle, 27/9/2026** — Golf Mk4,
*Motronic injection and ignition system (2.0 ltr. engine)*, as transcribed
on workshop-manuals.com (*Checking throttle valve control part*,
*Idling check*, *Technical data*; the 4-cyl. 2.0 mechanics, *Adjusting
throttle cable*). A transcription of VW's manual, not VW's own document;
the same source as the knock-retard specification in `vcds.md`. The part
itself — `06A 133 064 H`, VDO `408.237/111/017` — is listed by parts
sellers for the AEG, AQY and APK **without cruise control**, which is the
variant the manual's pin numbers below refer to.

- **The throttle valve control part J338** holds four things: the drive
  G186 (the idle actuator's motor), its angle sender **G187**, the
  throttle potentiometer **G69**, and the idle switch **F60**.
- **Display group 060, warm idle** (coolant ≥ 85 °C): zone 1 *throttle
  valve angle at the idling stop* **0…6°**; zone 2 *throttle valve
  positioner* **60…90 %**; zone 3 *Idling*. ⚠ The manual's own
  measured-value tables (`vcds.md`) put the **60–90 % in group 098** and
  give 060 the positioner as a voltage, so read the percentage in 098.
  ⚠ On this ECU 060 is also a
  basic-setting block (`vcds.md`): read it under *measured values*, not
  under *basic settings*, which would start whatever routine the label
  file gives it. (An earlier revision said it runs the throttle
  adaptation; that had no source — see below.)
- **Display group 054, ignition on**: G69 at rest **0…6°**, at full
  throttle **at least 75°**; the same check reads F60's state as
  *idling* or *part throttle* (which zone was not transcribed reliably).
- **Electrical**, connector off (without cruise control): G186's winding,
  pins 1 + 2, **3…200 Ω**; supply pins 4 + 7 **≥ 4.5 V** and 3 + 7
  **≥ 9 V** with the ignition on; each wire to the ECM **≤ 1.5 Ω** and
  open to its neighbours.
- **Idle**: 740…820 rpm for the AQY, target 780 (group 056), not
  adjustable; ECU Motronic M5.9.2.
- **The cable**: adjusted only so that **full throttle is reached at the
  quadrant** with the pedal down; the manual gives **no free-play figure**.
  At rest the lever must sit on its idling stop, which the idling check
  then confirms.

**Against this car's data.** Group 003's third field on this ECU is
*"klapka Pohon snímač úhlu 1"* — the throttle drive's angle sender, G187,
the same quantity as 060 zone 1. At warm idle it read **0.9–3.9°** on the
drive of 24/9 (mostly 1.7–2.2°) and **2.6–4.8°** in August's holds with and
without the A/C: **inside 0…6° throughout**. Not yet read: 060 zone 2 (the
positioner's %), and 054 (G69's range and F60). **060 zone 2 is the most
useful of them** (*reasoned, not from the manual*): it is how far the
actuator has to hold the plate for the target idle, so an unmetered leak
(H3) should push it towards the low end and a restriction towards the high
end — one reading at a warm idle, loads off, before and after the valve
cover job.

**Which way it moves is checked on the car, not assumed.** The manual
gives only the band; what a low or a high reading means is the reasoning
above. So calibrate it in one sitting, warm idle, 060 in measured values:
read it loads off; then **A/C on** (the engine needs more air — the
reading should move one way); then, loads off again, **the oil filler cap
off** (unmetered air past the MAF through the breather's route, as in H9
test 3 — it should move the other way). Two known disturbances give the
direction and roughly the size of a real one. **Outside 60–90 %** is a
fault by the manual's own terms: the actuator is at the end of its travel
and the idle is being held by something else.


**The throttle adaptation and the battery disconnects, 27/9/2026.** The web
says the throttle adaptation (a VCDS basic setting) should be run after
every battery disconnect, **and so does VW's manual** for this engine
(pages 24-119 and the notes on groups 060 and 098, `vcds.md`) — the voltage
supply interrupted, the throttle removed or renewed. (An earlier revision
said the manual asked for it only on a new J338; that was read off one
page and was wrong.) The same page adds that an interrupted adaptation
stores fault **17973** and *"when next switching on ignition the basic
setting is automatically performed again"*. **It was run once, in 6/2026**, when the throttle was
cleaned (`vehicle-history.md`) — *owner-reported*, date within the summer
not recorded — and never since. The battery has been off many times after
it: **for more than a week in the summer, for the heater and dashboard
work, before the August recordings** (*owner-reported*), then the new
battery at the end of August, and 23/9, 24/9, 26/9.

The hot-idle grades (`idledips.py --roughness`, oil ~70–77 °C, loads off)
were 48 on 11/8, 146 and 117 on 24/9 after the 23/9 disconnect, 84 after
the 24/9 one, and 57–100 off the display since. **August looked like the
one state with the June adaptation intact, and it was not** — the battery
had been out for over a week before it. So the best hot idle on record
came *without* a fresh adaptation, and **the grades give no reason to
suspect a missing adaptation**. (They could not have carried a conclusion
anyway: the converter, plugs, leads, injectors, MAF and every other
adaptation changed between August and September.)

**Which basic-setting group adapts it, 28/9/2026** (asked by the owner).
**Settled by VW's manual for this engine: 098** (page 24-119, *Adapting
engine control unit to throttle valve control part*; `vcds.md`), which
also names 060 as adapting it. The reasoning below came first and is kept
because it agreed.
Ross-Tech's wiki, *Throttle Body Alignment (TBA)*, splits by hardware:
**cable-throttle engines without an idle stabilisation valve use group
098** (some SIMOS/Marelli ECUs 001), **drive-by-wire engines 060**. This
car is the first kind — a cable to the plate, idle held by J338's own
actuator rather than a separate valve — so **098 is the expected group**,
and plan.md's earlier "060" was an inference, not a source. Ross-Tech's
procedure: key on, engine off, no faults, battery ≥ 11.5 V, throttle at
idle, coolant 5–95 °C; basic settings, the group, *ADP RUN*, the throttle
heard cycling for the first seconds, about 30 s. Its notes add that on a
cable throttle a mis-adjusted or sticky cable makes it fail. ⚠ **The
ECU's label file carries both 060 and 098 as basic-setting blocks**
(`vcds.md`), so the page decides nothing by itself: open both in
*measured values* first and read what the label file names them; the one
whose fields are the adaptation's is the one to run.

**What the throttle does at every ignition-on** (*owner-observed,
27/9/2026*): it is heard working for **about 20 s** after the key is
turned, and sounds like it is **seeking its stops**. *Owner-observed,
28/9/2026:* **at every ignition-on, not once after a disconnect**, for
**20–30 s** when the ignition is left on, confirmed to come from the
throttle; whether it also did so after the June manual adaptation is not
remembered. Usually the engine is started straight away and the routine
never finishes.

**What VW's manual says against that** (page 24-119, *Adapting engine
control unit to throttle valve control part*, and the fault table; the
links are in `vcds.md`): the adaptation drives the positioner to min, max
and a few points between and **takes at most 10 s**. If it is
interrupted, fault **17973 / P1565 — "Throttle valve control part -J338
lower stop not reached"** is stored and *"when next switching on ignition
the basic setting is automatically performed again"*. Causes it lists:
the plate not reaching its mechanical stop (oil deposits, a mis-adjusted
cable), battery voltage too low, J338 or its wiring defective. Nothing in
the manual describes a routine at *every* ignition-on on an adapted unit.
(An earlier revision read the sound as normal self-relearning that made a
manual adaptation unnecessary; that was an inference and the manual does
not support it.)

**So two readings, and the fault memory tells them apart:**

- **a loop** — an adaptation that never completes, because the key goes
  straight to *start* or because it fails, is retried at the next
  ignition-on, for ever. With **17973 stored** this is it, and it would
  mean the idle has been run on an unfinished adaptation;
- **this unit's normal check** at every ignition-on, not described in the
  manual — possible, and then no fault is stored.

**How it closes, without running the engine:** read the engine's fault
memory (VCDS, 01, fault codes) **before the job** with the old throttle
still on, and write down what is there — 17973 in particular. Then, with
the new part, the manual adaptation (098, *ADP OK*), ignition off, and at
the next ignition-on listen: the routine should now not run, or run only
briefly. **If it still runs 20–30 s every time with *ADP OK* and no
fault, it is the unit's own behaviour.** Either way this is the one sign
the actuator gives of its own health, and worth noting if it changes.

**Reading: against H8 at the resolution there is.** A sensor glitch shorter
than the 0.6 s between readings would not be seen; a worn track that made
the ECM chase phantom movement would, and does not show. Left in the file
because cleaning and adapting is cheap, not because anything points here.

**Replaced preventively, on its own after the valve cover job — the
owner's decision, 28/9/2026** (`plan.md` step 2). Nothing in the data asks
for it; the part is original, 26 years old, cheap, and sits in the idle air
path. First planned inside the valve cover job, then **split off by the
owner the same day** so that its effect shows alone: the valve cover job
and its readings first with the old throttle, then the swap and the same
readings. It comes off with the engine assembled, so the split costs
nothing. A new aftermarket part is itself an unknown on the idle's side of
the engine, which is why the old one is kept. What it buys: an idle fixed
by the valve cover job clears the throttle; one fixed only by the swap
names it; one fixed by neither sends the whole of H8 (the three wear routes
above included) to `refuted.md`.

**The cold-start idle, the baseline for the swap, 28/9/2026** (asked by
the owner, who expected **1200+ rpm for 15–20 s** from the web and sees
about 1000 at most). Off the three cold starts on record, all on the
original throttle — `18` (coolant 16.5 °C), `19` (12.0 °C), `24`
(27.0 °C) — engine speed off 0x280 from the first frame above 400 rpm:

| | `18` | `19` | `24` |
|---|---|---|---|
| flare, first 2 s (peak) | 1446 | 1522 | 1340 |
| 2–5 s, median | 931 | 1018 | 912 |
| 5–60 s, median | 925–936 | 938–978 | 933–944 |
| step down to ~810–850 at | 101.7 s, 32 °C | 101.5 s, 28.5 °C | 93.0 s, 40.5 °C |

- **1200+ lasts about two seconds**, the start's own flare. After it the
  engine holds a **flat plateau of 910–1020 rpm for 93–102 s**, then steps
  down within about two seconds to the warm-up idle. Only the coldest start,
  `19`, runs a little higher in its first ten seconds.
- **The three starts are alike.** The plateau's height barely moves with
  a 15 °C spread in start temperature, and the step comes at almost the
  same *time* while the coolant stands anywhere from 28 to 40 °C. So it
  is a **timed phase, not a temperature threshold**. That it is the
  catalyst-heating phase, with the secondary-air pump running, is an
  inference: the pump is heard after a cold start (H9 test 3), and the
  timing and the retard below fit it. It is not read in a VW document.
- **The ECU gets the speed it asks for.** VCDS 003 across `19`'s start
  (`vcds-postfix-drive-003-014.csv`): 920–960 rpm on the plateau with
  **ignition retarded to −0.8…−12 °**, the plate at **7.8° falling to
  5.2°** as the engine warms. Then, at the step, advance goes positive, air
  drops from 5.2 to 4.3 g/s and the plate goes to 3.5–3.9°. The speed is
  flat while the plate moves smoothly, so the plateau is a **target being
  met**: an actuator short of travel would show the speed sagging instead.
  The plate is above the warm-idle band of 0…6°, but that band is
  specified warm (060, coolant ≥ 85 °C).
- **The web's 1200 is forum talk** about Mk4s in general, "for 30–60 s"
  and "the secondary air ... no more than 30 s" (VW Vortex, uk-mkivs).
  **No VW figure for the AQY's cold idle was found**: the manual's
  transcription gives only the warm 740…820 rpm. So nothing says ~950 is
  wrong for this ECU.

**The plate angle across every VCDS log with 003, 28/9/2026** — steady
warm idle only (740–900 rpm for five readings running), split by air
mass because the A/C adds about 1 g/s:

| log | date | MAF | air ≈ 3.1–3.5 g/s | air ≥ 3.6 g/s |
|---|---|---|---|---|
| `vcds-01-002-003` | 11/8 | 2018 | **2.6–3.0°** (3.40 g/s) | 4.3–6.1° (4.31) |
| `vcds-ride-002-003` | 11/8 | 2018 | **2.6–3.0°** (3.26) | 3.0–4.3° (3.68) |
| `vcds-postfix-drive-003-014` | 24/9 | 2018 | **1.7–2.2°** (3.47) | 1.7–3.5° (4.37) |
| `vcds-neutral-026-003` (+ `-clamp`) | 25/9 | new | **1.7–2.6°** (3.22–3.26) | — |
| `vcds-knock-020-026-003` | 25/9 | new | **1.3–2.2°** (3.12) | 2.6–3.0° (3.79) |

(10th–90th percentile; the display steps by 0.4–0.5°.) The cold plateau
of `19` reads 7.8 → 5.2°, and full throttle reaches **85.1–85.5°** in every
log that has it (`refuted.md` C7). Outside idle the angle follows the
pedal.

- **For the same metered air, the plate stands about 0.8° lower in
  September than in August.** The MAF is the same 2018 unit on 11/8 and
  24/9, so this is not the sensor swap. Between the two dates the
  converter, the injectors, the plugs and leads all changed, and the
  battery was disconnected several times. Every disconnect means the ECU
  learns the throttle's stops again, and the angle is read against them.
  **Which of these it is cannot be told**, and it is recorded rather than
  argued: the step is two display counts, and nothing else in it points
  at the throttle. It is not listed as a symptom.
- **The new part's warm-idle baseline is therefore 1.3–2.6° at about
  3.1–3.5 g/s**, loads off, from the September logs.

**The lowest idle air and plate angle ever logged, 28/9/2026** — every
VCDS log with 002 or 003, steady idle 700–900 rpm (asked by the owner,
against VW's limits: idle air 2.0–5.0 g/s with *below 2.0* named as a large
unmetered leak; plate 0–6°, `vcds.md`):

| log | date | MAF | lowest idle air | plate there | lowest plate |
|---|---|---|---|---|---|
| `vcds-01-002-003` | 11/8 | 2018 | 3.19–3.26 g/s | 2.6° | 2.6° |
| `vcds-ride-002-003` | 11/8 | 2018 | 3.12 g/s | 2.6° | 2.6° |
| `vcds-postfix-drive-003-014` | 24/9 | 2018 | 2.92 g/s | 0.9° | 0.9° |
| `vcds-mafswap-002-032` | 24/9 | new | **2.57 g/s** (load 19.1 %) | *003 not logged* | — |
| `vcds-mafswap-002-014` | 24/9 | new | 2.71 g/s (load 19.5 %) | — | — |
| `vcds-neutral-026-003` (+ `-clamp`) | 25/9 | new | 3.06 g/s | 2.2° | 1.7° |
| `vcds-knock-020-026-003` | 25/9 | new | **2.64 g/s** | **0.9°** | 0.9° |

- **Never near VW's leak mark**: the lowest air ever is 2.57 g/s against
  2.0. The lowest plate, 0.9°, is at the bottom of 0–6° but inside it.
- **Both fell between August and September.** For the air, part of it is
  the sensor — the 2018 MAF over-read (`refuted.md` C2). For the plate it
  is not: 0.9° is already there on 24/9 **on the 2018 MAF**.
- **A lower plate for the same idle means less air is needed through the
  plate.** Either the engine burns better (new plugs, leads, injectors) or
  air arrives past it (a leak behind the throttle). These two quantities
  cannot tell which; **the air and the plate rising together after the
  job** can (`plan.md`, test 1).
- **On the new MAF the idle load is 19–20 %**, right at the ~20 % below
  which the ECU switches misfire detection off (S3) — why a zero in 014 at
  a warm idle counts only with detection `aktivováno`.

**Air against plate angle is the throttle's own calibration curve**
(*reasoned, general physics, 28/9/2026*). At idle the manifold is deep
enough in vacuum that the flow past the plate is close to choked: how much
air passes depends on the opening, the pressure ahead of the plate and the
intake air's temperature, hardly on the manifold. So for one throttle body
at a similar intake temperature, **a given angle means a given air mass**.
Two different movements follow:

- **along the curve** — air and angle rise or fall together. A leak
  *behind* the plate sealed or opened does this; it does not move the
  curve;
- **the curve itself moving** — the same angle with a different air mass
  (or the same air at a different angle). Causes: (1) the angle is read
  differently from the plate's real opening — the sender's zero or the
  learned lower stop moved; (2) the plate or bore changed — deposits, wear,
  or a different part; (3) the MAF reads differently; (4) air entering
  **between the MAF and the plate**, which passes the plate unmeasured and
  makes the MAF read *less* at the same angle; (5) the intake temperature
  (group 004, not in 003).

**The curve has already moved once, on the same parts:** August against
24/9, the same throttle and the same 2018 MAF, ~3.3–3.4 g/s at 2.6–3.0°
then and at 1.7–2.2° after (the table above). Most likely (1): the battery
was disconnected several times in between and the ECU relearns the stops
each time — the owner's reading, that the old unit's electronics may show
something other than the plate's real opening, has this much support. Only
two display steps, and the intake temperature of those days is unknown.

**How the plan reads it:** test 1 keeps the throttle and the MAF, so the
curve should stay put — a move there is the relearned stop (098 is run) or
air between the MAF and the plate. Test 2 changes the throttle, so a moved
curve says the two parts differ, but not whether in the sender or in the
metal; only a look at the plate's physical opening could split that.
**Group 004 once per test** gives the intake temperature for the
comparison (`plan.md`).

**What the swap is compared on:** the first cold start after it should
show the same plateau height, the same ~95–100 s and a similar plate angle.
A different height or length would be the ECU choosing differently, which
a new J338 should not cause. A sagging speed with the plate high would be
the new part.

### H9. Crankcase ventilation, or the valve cover gasket (S10, and possibly the idle)

The crankcase is ventilated into the intake, and blow-by leaves through the
breather hoses. *General* for any engine: **if the breather path is blocked**,
crankcase pressure rises and pushes oil out of the weakest seal — typically
the valve cover gasket — onto whatever is below. **If a breather hose or the
gasket leaks instead**, the crankcase draws in air past the MAF at idle, where
the manifold vacuum is highest: an unmetered leak, H3 by a different door.
Either way one fault can make S10 and reach the idle.

| S1 | S2 | S3 | S4 | S5 | S10 | S11 | S12 | S13 |
|---|---|---|---|---|---|---|---|---|
| ~ | — | ~ | — | — | ✔ | ✔ | ~ | — |

- **For:** the commonest explanation of S10 and, through the oil, of S11's
  smoke. Several forum cases of an unsettled idle were a breather hose (H3).
  The back of the engine is exactly what the spray test could not reach.
- **Against:** a gasket that only weeps oil lets in little air — it seals
  against splash, and the crankcase is near atmospheric — and the idle trim
  (−3.1 %) argues against a large unmetered leak (`refuted.md` A7). A
  26-year-old gasket weeps without any help from a blocked breather, so S10
  alone proves nothing about the ventilation.

**What the web says about this engine's ventilation — searched 26/9/2026.**
Parts catalogues and forums, not VW documents; nothing here was read off a
drawing of this car.

- **The layout.** The breather sits in the **oil filler neck on the valve
  cover**, VW `06A 103 465` (later revision `-D`), sold for AQY, APK, AZH,
  AZJ and AEG and described as a pressure-control breather with an oil
  separator. From it one hose runs to the **intake hose ahead of the throttle
  valve** — after the MAF — with the heater `N79` teed into it against icing.
  *Confirmed on this car by the owner's photograph of 26/9/2026.*
  One aggregator claims a second hose to the intake manifold; no other source
  shows one, so it is not relied on.
- **What follows from that layout.** With the breather joined ahead of the
  throttle, the crankcase sits near atmospheric at idle, so a weeping gasket
  lets in little air — the argument *against* below stands. But anything
  that leaks **between the breather and the intake hose**, or in the hose
  itself, is air past the MAF, and a torn separator or valve in the filler
  neck opens the crankcase to it.
- **Why that route is weak at idle** (*general*, reasoned from the layout,
  27/9/2026). Ahead of the throttle the intake sits only a little below
  atmospheric — what the filter and the MAF cost — and at idle, with the
  least air flowing, that difference is at its smallest. A tear in the
  breather's diaphragm or a crack in its hose is driven by that small
  difference, not by manifold vacuum, so it passes little air exactly where
  the idle is worst. It is not nothing: the idle was audibly slightly worse
  with the filler cap off (test 3), so this engine does notice air entering
  there. The diaphragm valve's job, as the catalogue describes the part, is
  to **regulate** the crankcase's depression rather than to act as a
  one-way valve; its internal layout was not read off a drawing.
- **Why a healthy breather adds no unmetered air, and a torn one does**
  (*general*; the owner's question, 28/9/2026). What a healthy system
  carries is **blow-by**: charge that the MAF already measured on its way
  into the cylinders and that leaked past the rings — mostly burnt gas,
  little oxygen, a small and steady flow the ECM's calibration already
  lives with. A closed crankcase has no other inlet. A torn diaphragm (a
  regulator diaphragm usually has outside air on its far side), a split
  hose or a leaking seal **opens that closed path to the outside**, and
  outside air never passed the MAF. The filler cap off (test 3) is exactly
  that fault made on purpose — and the idle got slightly worse.
- **Febi's own leaflet, 28/9/2026** — *Control of Crankcase Emissions*,
  Ferdinand Bilstein GmbH + Co. KG, found by the owner at the breather he
  bought (Febi `32452`). General, not about `06A 103 465`, and written to
  sell parts. It gives **a ruptured rubber membrane and blocked or split
  hoses as the typical defects**, with *"high oil consumption, burning oil,
  loss of power, misfiring, and high carbon deposits"*; early signs
  *"whistling noises from the intake, blueish smoke in the exhaust, high oil
  consumption, and thick white or yellow residue under the oil cap"*. Its VW
  example — 1.8/2.0 FSI/TFSI, a valve on the cover **connected directly to
  the intake manifold** — adds *"engine idle speed to fluctuate and stall,
  whistling noises from the engine at idle speed"* when the membrane splits.

  **Against this car:** idle fluctuation and misfires, yes. Everything else
  on the list, no — oil not topped up over ~700 km and still at the upper
  mark (`vehicle-history.md`), the cap's underside clean (`refuted.md`
  C13), no whistle reported, the smoke at the back explained as the cover
  leak's oil (S11). And the leaflet's mechanism is manifold vacuum on a
  torn membrane: had that been the case here, the crankcase would sit under
  that vacuum and **the filler cap would suck** — test 3 found none. So the
  leaflet raises nothing test 3 did not already weigh. **The one thing it
  made worth checking** was where this car's breather hose really joins
  the intake. **Answered by the owner's photograph of 26/9/2026**: the
  thick hose from the breather under the filler cap runs up into the
  intake duct **directly ahead of the throttle body** (`06A 133 064 H`,
  its label in the same frame) — after the MAF, not on the manifold. The
  catalogues' layout above holds, and the leaflet's manifold-vacuum case
  does not apply to this car.
- **Blocked ventilation is the commonest cause of oil leaks on the sister
  AZJ**, and **a fouled throttle body the commonest cause of an unsettled
  idle** — mymotorlist.com's page for the AZJ (the AQY page lists ignition,
  the idle controller and the crank sensor instead). The two meet: the
  breather's oil mist is delivered straight onto the throttle, so a
  ventilation that carries too much oil is H8 as well as H9. ⚠ **On this
  car that route is weak**: the throttle body was inspected in 6/2026 and
  found clean (`vehicle-history.md`), so any fouling since is three months'
  worth.
- **Forum cases on this engine**: an AQY Golf with `17990 / P1582` (idle
  adaptation at its limit) and a cracked ventilation hose (golf4.de); German
  threads on oily sludge in the filler-neck-to-intake hose, cleared with the
  idle improving. Leads, not results.
- **No VW bulletin was found** for the AQY or its US siblings about the
  ventilation, a rear oil leak or the valve cover. The one bulletin that
  touches this investigation is still TSB 01-08-27 (H4).

**The valve cover gasket and a rough idle — searched 27/9/2026.** Forums and
repair blogs; still nothing from VW.

- **The generic claim has two routes**, repeated across repair blogs: oil
  reaching the spark plugs or their boots and tracking the spark to earth,
  and a leaking gasket drawing in unmetered air. The first is written for
  engines whose plugs sit **in wells under the cover**, where a failed
  gasket fills the well. On the AQY the plugs are outside the cover on the
  front of the head, so oil reaches a boot only by running down the outside
  — which is what was photographed on 1 and 2 (S10). The second needs
  vacuum in the crankcase, and this layout holds it near atmospheric (above,
  and test 3's result), so **the air route is weak here**.
- **The one AQY thread on this exact job** (golf4.de, *Ventildeckeldichtung
  wechseln AQY 2.0*): the complaint was **oil at the top of the engine, with
  smoke and a smell of burnt oil** — S10 and S11's smoke as seen here. One
  poster still leaked after the new gasket and found the **camshaft seal**
  instead; the thread reports **no change to the idle** either way, and it
  was not asked. Its advice: the plenum comes off, check the gasket's VW
  number rather than trust a catalogue's cross-reference, and do the plugs
  while they are that easy to reach.
- **A Golf 4 that stuttered at idle** (motor-talk.de, a 1.4 16V — a
  different engine, plugs in wells) with the cover gasket weeping and a
  breather hose wet with oil: the hose and breather were replaced, the oil
  leak and a noise went, **the stutter stayed**. A second AQY thread on
  VWVortex with random misfires and a rough idle could not be opened
  (paywalled to crawlers); its title matches, its outcome is not known.
- **Reading.** No source found attributes a rough idle on an AQY to its
  valve cover gasket and reports it cured by the gasket. The one route that
  fits this car — **oil on the boots of 3 and 4** — cannot be the cause
  either: the idle was just as rough on 17/9 with new, clean plugs and leads
  (S10). **So the job is expected to cure S10 and S11's smoke and not
  expected to change S1.** If `IdleHealth` does improve clearly at a matched
  oil temperature afterwards, that is a surprise worth chasing — through the
  breather replaced with it (H9) rather than through the gasket.

**Tests:**

1. ~~**The garage names S10's source**~~ — found by the owner on 26/9: the
   valve cover gasket (S10).
2. **The breather hoses by eye and hand**, engine off: cracked, collapsed,
   hardened so that they split when bent, or wet with oil on the outside
   (*general*).
3. **The oil filler cap at a warm idle** (*general*): loosen it slightly. A
   strong, pulsing push of fumes means heavy blow-by or a blocked breather; a
   slight steady suck means the ventilation works. Note what the engine speed
   does — **an idle that settles with the cap loose** is the telltale the
   Czech sources give for a faulty ventilation. A garage can measure
   crankcase pressure properly.

   **How to read it on this layout** (the breather joins ahead of the
   throttle, so a working system holds the crankcase only a little below
   atmospheric — *general*, from the layout above):
   - **cap hard to lift, or strong suction** — manifold vacuum is reaching
     the crankcase, which this layout should not allow. **A clear fault**:
     a second path to the manifold with a failed valve or membrane in it.
   - **a pulsing push of fumes** — blow-by is not getting out: a blocked
     breather or hose, or heavy blow-by. Also a clear finding.
   - **cap comes off easily, neither of the above** — normal, and ⚠ **it
     does not clear the membrane**: on this layout a torn one would not
     make a strong vacuum either.
   - **idle better with the cap off** — suggestive, not proof. Opening the
     cap also lets unmetered air into the intake hose, and an engine with a
     slightly rich trim can idle better leaner for that reason alone.
     Decisive only if it repeats, cap on and off, at a matched oil
     temperature.

   **Result, 26/9/2026 evening** (*owner-observed*; cold engine a few
   minutes after a cold start, secondary-air pump heard running, so oil well
   below the warm band; `IdleHealth` watched but not written down):
   - **no suction at the cap** — as expected on this layout; it clears a
     second path to the manifold and says nothing about the membrane;
   - **a mild pulsing of air from the opening**, felt and heard as coming
     from the cylinders; no strong push, no fumes reported. Some pulsing is
     normal with the cap off (*general*); a strong push of fumes would mean
     blow-by is not getting out;
   - **the dipstick at atmospheric**: no push, no suction, no pulsing — **a
     point against crankcase pressure**, and so against the blocked-
     ventilation branch of H9 as the reason the gasket leaks;
   - **`IdleHealth` somewhat worse with the cap off, not consistently**, and
     the idle **audibly slightly worse** too —
     no sign that the ventilation disturbs the idle. If anything the extra
     unmetered air made it rougher, which is the direction H3 predicts, but
     inconsistent readings on a cold engine carry little weight.

   **Reading:** the valve cover gasket (S10) most likely leaks from age, not
   from pressure behind it. What would still change that: a strong,
   fume-laden push at the cap on a **warm** engine, or a separator found
   blocked in test 4.
4. **The filler-neck breather and its hose off, engine cold**: oil sludge in
   the hose or at its end on the intake hose, a split in the hose where
   `N79` tees in, the separator in `06A 103 465` intact. The part costs a few
   tens of euros, so replacing it on suspicion is a fair test.
5. **After the repair**, `IdleHealth` at a matched oil temperature against the
   current band: the same rule as H2 — a clear improvement means this was
   underrated.

## What the forums say about this idle — searched 27/9/2026

A fresh sweep for the idle and the misfires alone (S1–S3), in German,
Polish, Czech and English, looking for **threads that end in a fix**.
Forums, so leads and not sources; several of the big ones (motor-talk.de,
skodacommunity.de, vagboard.de, VWVortex) refuse automated reading, so what
is below is only what could be read to the end.

**The pattern is the finding: almost nobody reports a fix.** Every thread on
an AQY or a sister engine with this picture that could be read to its end
stops unresolved, after the same parts list this car has already been
through.

- **golf4.de, *Golf 4 AQY 2.0 Liter Benziner Motor ruckelt im Leerlauf*** —
  the closest match found: an AQY stuttering **at idle only, not under load**,
  intermittently, speed sagging to 760, **fault memory empty**; lambda
  probe, plugs, leads, coil, coolant sensor, MAF replaced and the intake
  cleaned and adapted. The advice was 014–016 while it happens; the owner
  never came back.
- **golf4.de, *Golf 4 2.0 AZJ 2001 Zündaussetzer im Leerlauf*** (the sister
  engine) — misfires **only standing at idle**, one cylinder, every 10–30 s;
  plugs and leads replaced; injector swap and the ECU suggested; a second
  owner with the same picture, and **no fix**.
- **forum.vwgolf.pl, *wypadanie zapłonu 2.0 aqy*** (t=434728, one page,
  2011–2020) — two AQYs. The second (2016) is the one of interest:
  misfires on several cylinders that **did not occur with the A/C on** —
  the direction of S1's *load at idle* — and came worse in rain; plugs,
  leads and coil changed, the leads helped a little; **no fix**, and a third
  owner asked the same in 2020. The poster read the A/C effect as a part
  overheating and being cooled by the condenser fan. That reading does not
  fit here, where the lights and the blower did the same as the A/C at a
  standstill; **the load reading still stands** (S1).
- **VWVortex, a 2000 Golf with the AEG** (the US sibling, P0300/0301/0303/
  0304) — per the search index, **leads arcing to the intake manifold**,
  found by misting them with water in the dark. Not read in full. Test 1e
  under H4 is this test; with new NGK leads it is a cheap check, not a
  suspicion.
- **golf4.de, *2.0 läuft unrund!!!*** (AQY/AGN) — rough cold, worse in the
  wet, popping on acceleration; plugs, leads, coil no help; "fixed" by
  unplugging and replugging the MAF — a MAF adaptation reset. This car's
  MAF is new (S9), so there is nothing to take from it.
- The general lists repeat what is already here: breather hoses (H9),
  intake leaks at the lower manifold and the brake-servo line (H3), the
  coolant sensor (`refuted.md` C6), lambda (C5), injectors (A1).

**One lead not yet in this file: the timing belt a tooth out.** A cam
sprocket a tooth off makes an engine idle roughly and shake slightly
(*general*, repeated in the AQY timing-belt threads). This car's belt and
water pump are from **10/2017** (`vehicle-history.md`). Against it:
compression is even (A4) and the engine reaches its rated torque plateau
(C11), where a retarded cam costs most. For it: nothing specific.
**Not checked in the valve cover job — the owner's decision, 28/9/2026:**
weak, and it is not free after all. VW's manual for this engine checks
the cam pulley's mark against *OT* on the belt guard and the flywheel's in
the gearbox window, together (*Removing, installing and tensioning toothed
belt*, `vcds.md`'s source), which means the upper guard off and the
engine turned by hand. Left here should the ranked list ever reach it.

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
   cylinder of each plug recorded this time. The old ones were not labelled:
   one was worst, and which cylinder it came from is not known.

---


**What `--cylinders` shows across the dates, 27/9/2026** (the question: can
the three proud injectors, 1–3, against a seated 4, be seen?).

| log | when | f = 0.25 (one cylinder) | f = 0.50 (alternate firings) |
|---|---|---|---|
| `09`, `11` | 11/8, warm | 13x | **0.8–1.1x** |
| `18` | 11/9, cold start | 21x | **20x** |
| `19` | 24/9, whole drive | 23x | **19x** |
| `20`, `24` | 24/9, warm | 20–22x | **11–12x** |

- **No one cylinder stands out since 23/9.** The phase slots of `20` and
  `24` split two high and two low, not one against three, which is what a
  seated 4 against three leaking seats would look like. A small leak could
  hide under it; a large one would not.
- **Something new appeared between 11/8 and 11/9 — before the injectors,
  the plugs and the leads:** a **period-2** pattern, absent in August,
  present in every September log. In a firing order of 1-3-4-2
  (*general*), period 2 is **cylinders 1 and 4 against 2 and 3** — the
  coil's two outputs (H4). What changed in that month: the new battery and
  the headlight wiring (end of August), the converter and flange (10/9),
  the secondary-air line (closed, A8). One more reading, *a hypothesis*:
  engine ECUs learn the crank wheel's tooth errors for misfire detection
  and may lose that with the battery (*general, not read for this ECU*);
  a lost adaptation shows exactly as a once-per-revolution pattern in
  engine speed, which is period 2 — an artefact of measurement, not the
  engine. It would fade with distance; an ignition or exhaust cause would
  not.
- **How much of the grade it is:** adding a period-2 of ±0.9 rpm — the
  size seen in `24` — to August's `11` raises its grade from 48 to 62. So
  it can account for a part of the August-to-September difference (S1),
  not all of it.

**What settles it:** `--cylinders` on every capture from now on — the
f = 0.50 line fading over a few hundred km without a disconnect is the
adaptation; staying is ignition or exhaust. The refit of the injectors
should, if the seats leaked, change f = 0.25 and not f = 0.50.

## The idle's candidates, ranked — 28 September 2026

**A judgement, not a measurement**, for S1–S3 only (the cylinder 4 window
is its own cluster). It weighs three facts above all: **the idle is better
the more load and air go through the engine** (S1), **no one cylinder
dominates** (`refuted.md` A5), and **the mixture matters** (the MAF swap
halved the dips, S9). Re-rank after every test, **and whenever the symptom
list changes**. *Re-read 28/9/2026 after S12 and S13 were added: the order
stands; what moved is recorded in the rows.*

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| 1 | **H3/H9 — a small unmetered leak**: **three injectors not fully home since 23/9** (H3, *The injector seats*), and at the back the plenum and its upper gasket, the brake-servo line, the old secondary-air vacuum line, the breather hose; **and the throttle's flange**, where a hard protrusion on the old face may have kept the June gasket off (H8, 28/9) | the only candidate that predicts *load helps*; the back was never sprayed; S11's hiss; a leak at the plenum feeds all four, as A5 wants; **also fits S12**, a lean tip-in. Against: trim −3.1 %; VW's own leak signs — idle air 3.1–3.5 g/s against 2.0–5.0, 055's learnt value −0.73 against ±1.50 — rule out a large leak, not a small one (28/9) | the valve cover job itself, which replaces the upper plenum gasket and the breather — an improvement afterwards answers it; if none, a **smoke test of the intake** (below) |
| 2 | **H0 — normal for this engine** | any engine idles least steadily at its lightest load; nothing has ever been compared. Against: 014 reads 12–120 against VW's 0–5 | a healthy AQY recorded (H0 test 1) |
| 3 | **H1 — a lifter or valve** | the one cause a forum has named on an AQY (a sticking bucket tappet); compression cannot see it. Against: worst at mid temperature, not hot; A5 | a **vacuum gauge** at idle (below), the stethoscope, a warm leak-down |
| 4 | **H7 — rail pressure** | the regulator and pump never gauged; mixture sensitivity. Against: trims near zero | a **fuel pressure gauge** |
| 5 | **H8 — throttle body and idle control** | original part, all four cylinders. Against: the dip is one firing, not a hunting loop; found clean in 6/2026; **the idle angle in every VCDS log is steady and the misfires do not move with it** (27/9) | **replaced on its own after the valve cover job** (owner's decision, 28/9; `plan.md` step 2), so its effect shows alone. **S13** (its routine at every ignition-on) now sits here too, most likely the unit's normal behaviour by owners' reports — timed on both parts in the plan |
| 6 | **H4 — the electrical feed to the spark** | harness 26 years old. Against: better with loads on, when the supply sags 1.25 V | a look while the plenum is off (`plan.md`, step 1); H7 test 3 for the injector side |
| 7 | **H2 — an exhaust leak ahead of the probe** | explains the puff and possibly S11's hiss; the zone is now only the **original manifold, its gasket to the head and the probe boss** — the new flange is behind the probe (28/9), and the puff is older than the 10/9 exhaust work (S2). Against: air outside the cylinder does not stop it firing | a smoke test **of the exhaust** (`plan.md` step 3) |
| 8 | **the timing belt a tooth out** | belt from 10/2017. Against: even compression, the torque plateau is reached | the marks (VW's manual), **not done in the valve cover job** — owner's decision, 28/9 |

**Tools worth owning for this, cheapest first** (*general*; prices not
recorded here, since they move):

- **A vacuum gauge on the manifold at a warm idle** — the cheapest
  instrument that splits the top three. A steady needle is a healthy idle;
  a regular flick down at one point in the cycle is a valve; a low, slowly
  wandering needle is a leak or a mixture fault. Teed into a manifold
  vacuum line (the brake-servo or the regulator's hose); readings are
  compared with themselves and before/after, not against a number.
- **An IR thermometer** for the four exhaust runners (*Naming the
  cylinder*).
- **A mechanic's stethoscope** (H1 test 1).
- **A smoke leak detector for the intake** — the one the owner asked about.
  The engine off and cold, the intake sealed at the air filter end, smoke
  fed in at **the low pressure the machine is made for** (never workshop
  air); smoke appearing anywhere downstream of the MAF is the leak, and a
  plenum, a hose or a gasket at the back shows it where no spray could go.
  The same machine into the tailpipe, cold, finds H2's leak ahead of the
  probe. **After the valve cover job is enough** (*the owner's point,
  27/9/2026*): the job replaces the upper plenum gasket and the breather
  and takes the rear hoses off and on, so it can cure an intake leak — and
  if the idle improves, that is the answer wanted, whichever part did it.
  A test **before** would only say *which* part it was; it is optional.
  If the idle does not improve, the smoke test afterwards covers the whole
  intake as refitted. (The valve cover gasket itself is not an intake
  joint: the crankcase sits at atmospheric, H9 test 3.)
  **Smoke rather than a pressure- or vacuum-decay test of the intake**
  (*general*): a sealed intake is never sealed — the throttle plate, the
  open inlet valves and the breather all pass air — so a gauge that falls
  says little, and says nothing about *where*. Smoke shows the place. The
  vacuum gauge above is a different instrument, for the running engine.
- **A fuel pressure gauge** with the adapter for this rail (H7 test 1).
- **A leak-down tester** with a compressor, warm engine (H1 test 3): where
  the air leaves names the fault — the throttle an inlet valve, the tailpipe
  an exhaust valve, the filler neck the rings, the expansion tank the head
  gasket.

## The plan

**The order of work is `plan.md`**, under the owner's rule of 27/9/2026:
the idle first, a repair at a time, readings only where they decide the
next step, and as little idling as possible. The tests listed under each
symptom and hypothesis in this file stay as reference for when a step
needs one; **they are not scheduled**. An earlier ten-step test plan stood
here; it is in git.

**Meanwhile:** avoid long idles — the misfires are an idle phenomenon and
the exhaust has already paid for them once. `IdleHealth` on 0x604 is the
trend to watch, always with the oil temperature beside it.
