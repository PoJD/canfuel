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
| `vehicle-history.md` | the car's service record: distance, consumption, every part replaced. **Stays when this investigation closes**; `open.md` and `refuted.md` go |
| `idle-log.md` | **the diary of the idle investigation**: what was believed, done and measured at each stage, and what nobody can say a repair achieved. Kept current until the idle is fixed, then **stays** as reference |
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

## Where it stands — 10 October 2026

**A summary of what is closed and what is left, and nothing else.** How
it got here, stage by stage, is `idle-log.md`; the parts and dates are
`vehicle-history.md`; what comes next is `plan.md`. Rewritten whenever a
symptom or a hypothesis opens or closes, not added to.

**Closed** — kept below for the record, out of every fit table:

| | how it closed |
|---|---|
| S7, the cold start | fixed by the new injectors (26/9) |
| S8, the top end | owner's decision, criterion met in part (4/10) |
| S9, the rich lambda trim | fixed by the MAF (4/10, short of its own criterion) |
| S10, the oil leak at the back of the head | the cover gasket, repaired (4/10) |
| S12, the tip-in hesitation | withdrawn by the owner as mechanical play (4/10) |
| S13, the throttle's routine at ignition-on | normal for the part (2/10) |
| S14, bangs on an unblipped downshift | none since S6's joint was remade, with S3 unchanged; closed at the owner's decision (10/10) |
| H10, the learned idle air value turns the counting on | accepted as the explanation of when 014 counts, closed at the owner's decision (9/10, `refuted.md` C19). Why the ECU learns air away stays with H3 and H8 |
| H9, crankcase ventilation and the cover gasket | right about S10, settled against for the idle (4/10, `refuted.md` A15) |

Everything else settled against is in `refuted.md`.

**Open — what this file is still for:**

- **The idle: S1 (unsettled) and S3 (misfires counted at idle).** Every
  part in the fuel and ignition path has been replaced and both remain.
  **When** 014 counts is settled — it follows 055's learned idle air
  value (`refuted.md` C19, closed 9/10) — but not **what the fault is**.
  **The dips kept to one cylinder's stroke** (9/10, *Naming the
  cylinder*), and the old parts named two single-cylinder faults: lead
  4's plug end and plug 1, almost loose (H4, 1d). **New plugs and leads
  went in on 10/10, and on the drive after the dips did not keep to one
  slot — but 014 counted as before** (S3, *The drive after the new
  leads*). So the leads did not fix S3; whether they took the
  one-cylinder share of the dips, two or three more drives say. The
  servo is cleared (H3). Ranked now (*re-read 10/10*): **H2**, the
  exhaust ahead of the probe — S15 still heard — then **H3**, a leak,
  and **H1**, a valve, which the vacuum gauge on order splits; **H7**,
  rail pressure, down to 5 on the owner's argument (*The idle's
  candidates, ranked*). **H11**, both lambda probes shifted alike, is
  written down last (10/10, at the owner's request) so that it is not
  argued again from the start.
- **Around the idle:** S2 (an occasional puff from the exhaust) and S11
  (a hiss at the back of the engine at a warm idle, not yet placed) —
  **neither heard on 9/10 or 10/10**, both kept open. **S15**, a constant
  sputter from the exhaust close behind the engine at every load (added
  9/10) — H2's zone, **still heard** (*owner*, 10/10/2026). **S6**, the
  joint behind the converter, **reopened 10/10** (*owner's decision*):
  it rattles again the day after it was remade, and drowns S15 and
  vents the tailpipe test until it is tight.
- **The cylinder 4 knock window: S4 and S5**, a cluster of its own
  (H5, H6). The injectors were cleared from it on 9/10 (`refuted.md`
  B7). **Not in `plan.md`** (*owner's decision, 9/10/2026*): no link to
  the misfires has been found, so its tests, G66 first, stay in H5.

**Next:** `plan.md` step 3 — **first the joint behind the converter,
shimmed tight (S6), and the exhaust test on the cold start after it**;
then **nothing until the vacuum gauge arrives** (ordered 10/10, *owner's
decision*), and the gauge on a cold start of its own. Unless
it shows an intake leak plainly, the engine is then left alone and a
tank is run with a PEA inlet-valve cleaner, read on the drives after
(*owner's decision*, 10/10). Done:
the intake tight cold (2a–2c), the servo, new plugs and leads, and one
day of the injector cuts, which named no cylinder (S3, *The drive after
the new leads*).

---

## The symptoms

Numbered so that the hypotheses can refer to them.

### S1. Unsettled idle — engine speed fluctuates

**What is seen.** Every few seconds the idle dips by 20–45 rpm and recovers in
about a quarter of a second. It feels restless from the driver's seat too.
*Owner-reported:* the hesitation that the old MAF caused has gone; the
twitching has not.

*Owner, 4/10/2026, after step 1b:* the idle **feels clearly calmer** —
said cold and again warm. The numbers taken at matched oil temperature,
as `refuted.md` C12 asks, **agree against the car before 1/10 and barely
differ from 3/10**: at a hot stop, ~70 °C, dips ≥ 20 rpm a minute went
20 (`19`, old MAF) → 9.1 (`24`) → 5.0 (3/10) → **4.4**, and `IdleHealth`
112–146 → 84 → 62 → **60**; in the middle band the dips sit at 9–11 on
`24`, 3/10 and 4/10 alike (S3, *Session A after step 1b*). ~~So the calm
the owner feels is the job of 1–2/10 at the hot idle~~ — *withdrawn
9/10/2026*: both calm hot stops came on **fresh adaptations**, and on
settled ones the hot idle is back where the MAF left it (below). 1b's
change is in 014 rather than in engine speed.

**Every session since the repairs, like with like** (*re-read
9/10/2026*): standing idle in 30 s windows, `idledips --roughness` mean
step in rpm (lower is calmer), ± the standard error over the windows,
binned by 0x420:

| session | adaptations | < 30 °C | 50–65 °C | 67–80 °C |
|---|---|---|---|---|
| `19`/`20`, 24/9, new injectors, old MAF | fresh | 2.21 ± 0.22 | 2.17 ± 0.09 | 2.26 ± 0.09 |
| `24`, 24/9, **new MAF** | fresh | 2.07 ± 0.27 | **1.67 ± 0.07** | **1.82 ± 0.14** |
| `25`/`26`, 3/10, after the job, cover open | fresh | 2.59 ± 0.23 | 2.22 ± 0.09 | 1.36 (2 windows) |
| `27`/`28`, 4/10 A, the right gasket | **fresh** | 2.41 ± 0.29 | 1.92 ± 0.04 | **1.48 ± 0.07** |
| `29`, 4/10 B | settled | — | 2.10 ± 0.18 | 1.77 (2 windows) |
| `30`, 9/10, dipstick and MAF clamp | settled | 1.90 ± 0.13 | 1.89 ± 0.08 | **1.77 ± 0.05** |
| `31`, 10/10, **new leads and plugs**, intake gasket | settled | 2.40 ± 0.22 | 1.91 ± 0.06 (4 windows) | **1.53 ± 0.08** (cuts left out) |

**The MAF is the one change that shows** (middle and hot band, and the
dips halved). **Nothing since does, once adaptations are matched**: the
middle band has stayed at 1.7–2.2, and the calm hot idle of 3/10 and
4/10 A — taken for the job's — came on fresh adaptations and is gone on
settled ones. That is the same pattern 014 shows (`refuted.md` C19):
**fresh adaptations look better on both rulers**, so a session after a
battery disconnect is no test of a repair. The one hint the other way
is 9/10's cold idle (1.90 against 2.4–2.6), on five windows and a cold
idle that also depends on how long after the start it is measured:
the next cold start on settled adaptations says whether it holds.

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

**Temperature matters: roughest cold, calmer as the oil warms, calmest
hot.** Re-read 9/10/2026 over every capture since 24/9 (standing idle,
binned by 0x420, `idledips --roughness`): the mean step is highest cold
and falls with the oil in every session, on fresh adaptations and settled
ones alike — on `30`, 2.06 rpm at 10–20 °C, 1.89 at 50–60, 1.85 at 60–70,
1.53 at 70–80; on `29`, 2.33 / 2.12 / 1.86 / 1.83; on `27`/`28`, 2.42 /
1.94 / 1.51. The dip count scatters (8–22 a minute) with no band
consistently on top. *Corrected 9/10/2026, at the owner's question:* this
read "not monotonic … worst at about 50–61 °C of oil", which no capture
since 24/9 bears out for engine speed; the middle-band peak is 014's
(S3), and on settled adaptations that is shallow. ⚠ Every engine idles
roughest cold (*general*: enrichment, a raised idle), so cold-worst says
nothing about the fault on its own. A reading without the oil
temperature beside it cannot be compared with anything.

**What comes before a dip — 10/10/2026** (*the owner's request to go
through every idle again*; `tools/dipcontext.py`, warm standing idle at
≥ 55 °C of oil, the injector cuts of `31` left out, captures `19`, `20`,
`24` and `26`–`31`). Three readings no tool had made before:

- **The ECU has trimmed the engine just before a dip.** Averaged over
  852 dips against five times as many random idle moments: injection
  time (0x288 b6) sits **0.33 ± 0.04 counts** lower and indicated torque
  (0x280 b7) **0.35 ± 0.05** lower from about 0.4 s to 0.1 s before the
  dip — some 0.9 % and 1.5 % of their idle values — while the control
  does not move (±0.02). Engine speed, averaged over a cycle, is
  **2.8 rpm higher** 0.4 s before. Read in order (*reasoned*): the idle
  rises a little, the governor answers by taking a little air or advance
  away, and the dip comes in the next few cycles; afterwards both rise
  as it catches the fall. In 6 of the 9 captures alone; `24`, `27` and
  `29` show it weakly or not.
  ⚠ **It is an average, not something each dip shows.** The shift is
  under one count of either byte (b6 is ~0.08 ms a count against ~3 ms
  at idle, `docs/firmware/can-decoding.md` question 3), so −0.33 means
  roughly one dip in three had the byte one count lower just before it;
  no single dip can be read for it. And both bytes are **the ECU's own
  calculation** — injection time follows the air per stroke the MAF
  reports, b7 the ECU's torque model — so "trimmed" means the ECU saw
  or set a little less charge: the throttle closed a touch, or the MAF
  wavered. Air or advance cannot be told apart here: 0x280 b5 does not
  move at this scale, and the advance is only on VCDS 003, about once a
  second.
  **Not the lambda control** (*the owner's question*, 10/10/2026): it
  works on fuel alone, swings much wider (033 ran −7 to +7 % at a
  standing idle) and the 014 rises fall on its lean and rich swings
  alike (`refuted.md` C5); it does not move the ECU's torque, which
  falls here with the fuel and after a small rise in engine speed —
  the idle governor's signature, holding 780 rpm (*reasoned*). The
  governor trims both ways all the time; the finding is only that dips
  follow its trims down more often than its trims up.
- **It is not the speed rise that the dip detector selects.** Split by
  how engine speed moved, a dip starts within the next 0.3 s after
  indicated torque **fell** over the half second before in **5.0 %,
  5.9 % and 10.1 %** of moments (speed flat, rising, falling), and after
  it **rose** in **3.1 %, 1.9 % and 6.2 %**; injection time the same way
  (5.0 / 5.1 / 11.1 against 2.7 / 1.4 / 6.3 %). So with the speed trend
  held, a moment just after the ECU trimmed torque or fuel is 1.6 to 3.5
  times as likely to be followed by a dip as one just after it added
  some. ⚠ The moments are 0.05 s apart and overlap, so the counts are
  not independent; the direction holds in every row, the sizes are
  approximate.
- **A dip is followed by another on the same cylinder more often than on
  its partner**: the next dip one or more whole engine cycles later
  (720°, the same cylinder) **36 times**, against **16** a whole number
  and a half later (360°, its partner in the firing order) — equal
  windows, so chance gives as many of one as of the other (p ≈ 0.007,
  one-sided; 862 dips). ⚠ **Not runs** (*corrected the same day*, at
  the owner's question how this bears on a lifter): this read "short runs
  on one cylinder, not isolated events". By lag, the 36 are spread over
  1–6 cycles (11, 3, 1, 13, 5, 3), not gathered at one or two as a state
  that holds a few cycles would be; and a cylinder carrying more than its
  share of independent dips gives exactly this excess — at 45 % on one
  cylinder, 2.5 to 1 (*The dips keep to one slot*). So it says again
  what *The dips keep to one slot* found — some cylinder takes more than
  its share, which one unknown — and nothing about how long a fault
  lasts. **And it is the older captures that say it**: `31`, after the
  new leads, reads 2 against 2, as its pairs did (S3, *The drive after
  the new leads*).

**What it means** (*reasoned*). The three readings of load — loads on
smooth the idle (26/9, above), a more negative learned idle air makes
014 count (`refuted.md` C19), and now a momentary trim of air or advance
comes before a dip — say one thing on three timescales: **one or more
cylinders run at the edge of stable combustion at the idle's charge**,
and anything that takes a little charge away tips them over. It is a
property, not a part: what narrows that edge at light load is a valve
that seals worse at low cylinder pressure (H1), dilution by a small leak
(H3), a late cam (the belt a tooth out, ranked 8), or the engine's own
margin (H0) — **it does not choose between them**. It argues against a
fault that does not care about the charge: an intermittent wire, a
crank-sensor artefact (which would repeat at 360°, not 720°).

### S2. An occasional puff from the exhaust

*Owner-reported*, at idle, before the injectors and after them, before the MAF
and after it. **Long-standing: already there before the 10/9 exhaust work**,
like the rough idle (*owner-reported, 28/9/2026*). Not recorded, not timed,
never aligned with anything. It did
**not** coincide with misfire detection going `deaktiv.`.

*Owner, 4/10/2026:* only now and then, and **much weaker than S14's
bangs** — in his reading **the same thing, smaller**: the unburnt charge
of a misfire going off in the exhaust. It fits (*reasoned*): at idle
nothing cuts the fuel, so a misfired charge brings only its own air and
no surplus, and most of it burns quietly in the converter; on the
overrun the cut pumps plain air in after it, and it bangs. Still never
aligned with 014, so it remains a reading, not a measurement.

*9/10/2026, owner:* **no puff heard** on the drive of steps 2b/2c, the
first after the joint behind the converter was remade (S6). Possibly
gone, possibly only harder to hear through a tighter exhaust. **Kept
open** (*owner's decision*), as S14 is.

*10/10/2026, owner:* **none again.** **Kept open** (*owner's decision*):
a tighter exhaust behind the converter may only be hiding a puff that
starts ahead of it; the tailpipe test (`plan.md` step 3) is what would
show it.

### S3. Misfires counted by the ECU at idle

**VCDS group 014**, on every drive since the counter was first logged.

- **122 of 129 new events began at a standstill idle**; the few seen in 1st
  and 2nd are mostly the three-second hold of an event that began standing.
  None during a pull.
- **"Only at idle" is the car, not a blind spot of the detection** (added
  3/10/2026). The method (`vcds.md`, block 014, *What the number is*)
  sees a misfire **more** easily under load — each firing is a large
  torque pulse there, so a missing one stands far out of the noise — and
  is weakest at idle, which is why it switches off below about 20 % load
  (*general*). And on this car it has worked under load: the historical
  full-load misfire set the lamp above ~4500 rpm (`refuted.md` C4). So
  no count during a pull is a real absence. **What it does not see**
  (*general*): below about 20 % load (light cruise, the coast down), on
  the overrun with the fuel cut, at high engine speed, and **in
  transients — a gearchange, a sharp tip-in — where ECUs commonly
  suppress detection** against false alarms. That last gap is exactly
  where S12, the tip-in hesitation, would have sat: a short stumble there
  could escape 014 and the dips alike (engine speed while driving follows
  the car). S12 was withdrawn on 4/10/2026; the gap remains.
- **Off idle, by detection state** (*the owner's question*,
  10/10/2026: is 014 not simply `deaktiv.` there?). Partly: over every
  014 log from 24/9 on, above 1500 rpm detection reads `deaktiv.` in
  about 45 % of samples — the free-revving and coasting where load is
  low, which is also where a 2500 rpm hold in neutral sits. But it reads
  `aktivováno` in about 4,300 samples there, while driving at a median
  load of 40–55 %, and **new counts started in 15 of them**, under one
  per 250 samples, against several a minute at a standing idle. So the
  absence under load is real; at a free-revving 2500 nothing is known
  from 014. **Nor from the bus**: a missed firing at 2500 moves engine
  speed about a third as much as at idle, which the noise of 0x280
  there swallows (*reasoned*; `idledips` on `10`, `13`–`16` at a scaled
  threshold counts hundreds a minute, which is noise, not misfires).
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

- **How often 014 counts, by oil temperature** (*computed 29/9/2026*:
  014 aligned on engine speed to the capture beside it, standing at
  650–900 rpm with detection `aktivováno` only, binned by 0x420):

  | oil | `24` — new MAF, adaptations fresh | `19` — old MAF, adaptations fresh |
  |---|---|---|
  | 48–56 °C | — | 3.6–10 a minute |
  | 56–60 °C | **20 a minute** (102 s) | — |
  | 60–64 °C | 2.5 a minute (95 s) | 1.5 a minute (196 s) |
  | 64–68 °C | — | 2.0 a minute (152 s) |
  | 68–72 °C | **10 a minute** (318 s) | **0.3 a minute** (433 s) |

  On `24` the longest stretch of active standing idle with no count is
  **57 s**. On `19` the last ~6½ minutes of hot idle at 70–71 °C read
  **zero** — on the car before any repair, which is what A11's change of
  ruler looks like from the other side: **on the old MAF a hot-idle zero
  is not evidence**, and only `24` is a comparison for the car as it now
  is. The test after the job (`plan.md`) takes its two stops and their
  lengths from this table.

- **Session A, 3/10/2026 — after the valve cover and throttle job**
  (`25_sessionA_cold_z1` and `26_sessionA_warm_z1`, with
  `vcds/vcds-sessionA-003-014-055.csv`). A cold start after a 27 h
  stand, ~7 min of cold idle, a drive to the 55–68 °C band, ~6 min
  standing there, a drive home, ~2 min hot. Fresh adaptations (battery
  off for the job). Aligned on engine start and stop; the two clocks
  drift 12 s in 31 minutes, which is ignored. Standing idle only,
  binned by 0x420:

  | oil | 014 rises a minute | 014 non-zero | dips ≥ 20 rpm a minute (`24` / `19`) | `IdleHealth` |
  |---|---|---|---|---|
  | < 40 °C | **0** (419 s) | 0 % | **22.0** (11.8 / 13.7) | 120–178 |
  | 40–60 °C | **16.8** (111 s) | 75 % | 15.7 (9.4 / 22.4) | — |
  | 60–66 °C | **15.6** (299 s) | 75 % | 9.3 (5.2 / 14.0) | 101–117 |
  | 66–80 °C | **3.0** (102 s) | 40 % | 13.6 (8.6 / 19.4) | 60 |

  Driving, the counter read non-zero in 8–16 % of samples, 1–2 rises a
  minute; detection `deaktiv.` 19–40 % of the driving samples and 1–8 %
  standing. **The misfires are not gone**: by `plan.md`'s rule any count
  is the verdict, and these are about as many as `24` counted. **On the
  engine-speed ruler the idle is about half as rough again as `24`'s**
  and still better than `19`'s, band for band; the small samples (`24`'s
  middle band is 80 s) make that a direction, not a figure. *The dip
  column is `idledips.dips()` at 20 rpm over standing idle at 400–1100
  rpm, which reproduces this section's `24` and `19` figures to within
  1.5 a minute; `IdleHealth` is `idledips --roughness` in two-minute
  windows.*

  **Twenty-two dips a minute cold with 014 at zero** is the same thing
  `19` showed (above): cold, this ECU does not count what engine speed
  shows.

  **No leak signature at the cold start** (`plan.md`'s table): plateau
  ~920 rpm for ~95 s, 003's air 7.0 → 5.1 g/s on it (`19`: 6.8 → 5.2),
  ~4.0–4.3 g/s after the step (`19`: ~4.3); 055's regulator −0.4 → −1.65
  g/s over the first two minutes, then −0.5 to −0.8 at 3–7 min, the
  learned value 0 throughout — the same neighbourhood as 11/9's sum of
  −1.2 → −0.8. So the job sealed nothing that shows at a cold idle.
  **The cover was found leaking at cylinder 4's end by the in-band stop**
  (S10), so the warm figures were taken with a joint open; how much that
  matters is S10's question.

- **Session A after step 1b, 4/10/2026** — the cover sealed with the
  right gasket, the battery disconnected and 098 run, a cold start after
  ~15 h (`27_sessionA2_cold_z1` and `28_sessionA2_warm_z1`, with
  `vcds/vcds-sessionA2-*.csv`). Aligned on engine speed (mean error
  22 rpm), standing idle with detection `aktivováno`:

  | stop | oil | standing | 014 rises a minute | dips ≥ 20 rpm a minute | `IdleHealth` |
  |---|---|---|---|---|---|
  | A1, cold | 11–17 °C | 318 s | **0** | 17–20 | 81 → 171 |
  | the joint stop | 41–47 °C | 116 s | **0** | 11.9 | 126 |
  | **A2** | 55–62 °C | 255 s | **0** | **9.1** (3/10 at 58–65 °C: 10.8) | 103–109 |
  | **A3** | 68–71 °C | 468 s | **0** | **4.4** (3/10 at 69 °C: 5.0) | 56–62, one window 109 |
  | hot, after a hard drive | 72–73 °C | 238 s | **7–9** | 7–11 | 82–92 |
  | the MAF wiggle | 73 °C | 71 s | 13.6 | 15.3 | 79 |

  **The MAF wiggle found nothing** (`idle-log.md`, *The MAF*):
  the counts were there before it (*owner*, watching 014 before he went
  to the engine), and 003's air never dropped out under the hand. Its
  13.6 against 9.2 a minute is 71 s against 189, a difference that small
  a sample does not carry.

  *The 3/10 figures beside A2 and A3 are its stops taken whole, by the
  same rule; they replace 15.7 and 13.6, which were the 40–60 and 66–80
  °C bins of the band table above — a different cut of the same idle,
  and not like with like.* **On engine speed the idle barely moved from
  3/10** (−16 % and −12 %, the second on a 65 s stop); **014 is what
  changed**.

  **The first warm stops ever logged with 014 at zero**, at the
  temperatures where `24` counted 20 and 10 a minute and 3/10 16 and 3.
  **Then it came back, and what brought it was the drive, not the
  temperature.** For 33 minutes — the start, three stops, the drives
  between them with one brief pull to 5200 rpm — the counter never moved,
  standing or driving. Then **five minutes of hard driving** (5400–5770
  rpm, b5 ≥ 80 for 40–54 % of each minute): the first count came at
  34½ min while still driving, a traffic stop four minutes later counted
  48 in 15 s, and every idle after it counted, at the same oil and coolant
  (97–100 °C) as A3's zero. **A pattern 3/10 could not show**: it
  counted at its first warm stop after a gentle warm-up, b5 never past
  105.
  *Reasoned, not tested:* something that needs heat from load and outlasts
  the drive — the exhaust at the back (H2, with S11's hiss) first; the
  spark when hot (H4) and fuel heat-soaked at the rail (H7) fit in form
  only (the ranked list says why). Not an intake leak (H3): one does not depend on what was driven
  before, and the leak signature did not move (below). Session B's B3
  (`plan.md`) repeats it with 033 beside it.

  **The warm leak signature did not move with the joint sealed**, against
  3/10's warm stops: 003 3.12–3.26 g/s (3.19), plate 2.6° (2.6°), 055's
  sum −1.06 to −1.16 g/s (−1.21) — all inside `plan.md`'s 0.2 g/s of no
  change. 055's learned value walked 0 → −0.92 by A3 and −1.15 by the end.
  So the hole did not reach the MAF's books at idle either way.

  **The start**: 1.38 s of crank to first firing, `StartDip` 0, coolant
  15 °C, after ~15 h — past `plan.md`'s 1.2 s, on adaptations at zero;
  read against the next cold start, not alone. No fault code stored.

- **Session B, 4/10/2026** — after a cool-down to 32 °C of oil, a
  part-warm start (coolant 44 °C, `StartCrank` 0.70 s, `StartDip` 0),
  ended by the owner at B1 (`29_sessionB_z1`, with
  `vcds/vcds-sessionB-014-055-033.csv`). Standing idle, 014 aligned on
  engine speed:

  | stop | oil | 014 a minute | dips a minute | `IdleHealth` | 033, median |
  |---|---|---|---|---|---|
  | after the start | 31–36 °C | **1.5–4.3** | 9–19 | 135–156 | 0.0 / +0.8 % |
  | **B1** | 59 °C | **14.3** | 11.3 | 120 | **−0.8 %** |
  | home, two stops | 69–71 °C | ~5 | 8–20 | 90–143 | −1.6 % |

  **The misfires were back**, at B1 about as on 3/10, **and on the idle
  after the start** — the first counts on an idle that cold since the
  adaptations were last fresh. **033 did not add fuel** at B1: its median
  sat at −0.8 %, swinging both ways (above +3 % in 13 % of the session's
  samples and below −3 % in 13 %) — not the steady positive correction
  air reaching the probe would make (H2). **055's learned value was −1.02
  to −1.24 throughout**, where it had ended session A. Read together
  with session A: the learned value (`refuted.md` C19).

- **Steps 2b and 2c, 9/10/2026** — the first session on **kept
  adaptations**, after the smoke tests sealed the dipstick guide and the
  MAF-to-hose clamp (`plan.md` 2a), the exhaust joint behind the converter
  remade and the new MAF back in. A cold start, the three stops, the
  knock holds and drive, the way home (`30_step2b_z1`, with
  `vcds/vcds-step2b-*.csv` and `vcds-step2c-*.csv`). 014 aligned on engine
  speed (mean error 21–24 rpm), standing idle with detection
  `aktivováno`; dips and `IdleHealth` cut the same way from `27`–`29`
  for the comparison:

  | stop | oil | 014 rises a minute | 055 learned, g/s | dips ≥ 20 rpm a minute (4/10) | `IdleHealth` (4/10) |
  |---|---|---|---|---|---|
  | A1, cold | 10–13 °C | **1.4–1.8** | −1.12 | 12.1 (16.5) | 86 (98) |
  | **A2** | 56–61 °C | **6.8** | −1.10 to −1.17 | 8.4 (9.2) | 67 (70) |
  | **A3** | 67.5 °C | **10.7–12.5** | −1.11 to −1.17 | 13.9 (4.4) | 56 (39) |
  | hot, the way home | 72–73 °C | 3.7–5.8 | −1.17 to −1.32 | 7.4–10 (6.7–15) | 41–61 (38–59) |

  **The misfires are not gone**, at both warm stops and on the cold idle
  after the start — the second cold idle to count, after session B's,
  and again with the learned value already past −0.93. **The learned
  value never came up**: −1.07 to −1.33 all session, more negative by the
  end. **Nothing a sealed leak would show moved**: at A3, 003 read
  3.12 g/s at 760 rpm with the plate at 2.6° (4/10: 3.1–3.3 g/s, 2.6°),
  055's sum −1.14 (−1.06 to −1.16), 055's live regulator at zero rather
  than positive, 033's median −0.8 % (+1.6 % at A2). 032 after the drive:
  **−2.3 / +5.5 %** (`photos/vcds-032-2026-10-09-after-step2b.jpg`;
  4/10: −0.8 / +2.3 %) — the idle cell moved negative, not toward the
  positive a leak at the probe or behind the MAF would want. **On engine
  speed, no change**: the cold and A2 stops a little smoother than 4/10,
  A3 rougher, the hot stops the same. The owner felt the idle calmer at
  A2 (*owner-reported*, 9/10); the grades do not show it, and it is not
  recorded as a change to S1 (`refuted.md` C12).

  **The size of the readings** (*the owner's question*, 9/10): the
  non-zero values at idle had a median of 12–24 and peaks of 12–48, with
  a maximum of 72–96, against 24–36, 24–48 and 84–132 in sessions A and
  B — smaller over the session, but **not at A3**, which read 24, 48 and
  96. 014 is a yes/no witness (below), so this is a direction at most.

- **The drive after the new leads, 10/10/2026** (`31_step4_drive_z1`,
  `vcds/vcds-step4-014-003-020.csv` and `vcds-step5-014-055-003.csv`;
  `plan.md` step 3). New plugs of the same type, new leads of a
  different construction and a new upper intake gasket, the battery
  kept, so the adaptations are 9/10's. Standing idle only, 014 aligned
  on engine speed:

  | stop | oil | 014 rises a minute (9/10) | 003 air, g/s |
  |---|---|---|---|
  | cold idle, servo held | 10–13 °C | **3.6** (1.4–1.8) | 3.89–4.42 |
  | short cold stop | ~20 °C | 14.0 (—) | 3.73 |
  | middle | 58–60 °C | **9.4** (6.8) | 3.15 |
  | hot, before the cuts | 69–70 °C | **6.0** (10.7–12.5) | 3.08 (3.12) |
  | hot, after the cuts and home | 70 °C | 2.7–5.7 (3.7–5.8) | 3.11–3.24 |

  055's learned value −1.14 before the cuts, −1.28 after (9/10: −1.07 to
  −1.33). **The misfires are not gone**: better at the hot stop, worse in
  the middle and cold, no direction overall. **The dips no longer keep
  to one slot**: `cutscan.py --pairs` over the idles outside the cuts,
  10 of 39 pairs on the same slot, 26 % against chance's 25 % (9/10: 34
  of 103, 33 %); over the whole capture the tool reads 41 %, but 38 of
  its 78 pairs are inside the cuts, where a dead cylinder is the slot.
  Fewer pairs from a drive of the same kind means fewer dips. ⚠ 39 pairs
  is a direction: 33 % and 26 % are not apart at this size. The
  engine-speed grade by oil band (S1's table): calmer hot (1.53 against
  1.77), the same in the middle, rougher cold (2.40 against 1.90) — the
  same no-direction as 014.

  **No new link to cylinder 4** (*the owner's question*, 9/10).
  `idledips.py --cylinders` over the four stops finds the same period-4
  structure as 4/10, of the same size — `sd_true` 1.8–2.6 rpm against
  1.8–2.3 on `28` and `29` — and the bus cannot say which cylinder a slot
  is (*Naming the cylinder*). The knock window is still under load only,
  and at idle 026 sits on the floor, so nothing here ties the misfires to
  cylinder 4.

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
- **9/10/2026, all four injectors seated** (`vcds-step2c-020-026-003.csv`,
  step 2c): still **cylinder 4 alone** — 9.5 % of the driving samples,
  onsets at 1280–2320 rpm on the tip-ins and 3640–5560 rpm on the pulls,
  **up to 13.5 °CA** — against 2.1 % and 5.2 °CA on 25/9, on a harder drive
  (to 6,010 rpm against about 4,000). Cylinder 1 five samples above
  4000 rpm, 2 and 3 none. One event standing, at 1640 rpm in the holds.
  The injectors are cleared from it (`refuted.md` B7).
- **10/10/2026, the first drive on the new plugs and leads**
  (`vcds-step4-014-003-020.csv`, an ordinary drive with a few pulls to
  89 g/s): cylinder 4 retarded in **3 of 1,841 samples, at most 1.5°**.
  By 003's air, cylinder 4's share of samples with retard:

  | air, g/s | 25/9 | 9/10 | **10/10** |
  |---|---|---|---|
  | < 15 | 5 of 652 | 14 of 650 | **1 of 1,533** |
  | 15–30 | 3 of 71 | 8 of 69 | **0 of 208** |
  | 30–50 | 3 of 14 | 0 of 27 | **0 of 86** |
  | > 50 | 5 of 8 | 22 of 54 | **2 of 14** |

  Fewer at every band, including part load, where today has the most
  samples — not just a gentler drive. The owner, watching 020 on the
  way, saw none, where on earlier days he saw it regularly (*owner*,
  10/10/2026). *Reasoned, not shown:* lead 4's plug end was the worn one
  (H4, 1d), and a contact arcing at the plug is a broadband noise inside
  cylinder 4's own knock window — a cause for S4 and S5 that is not
  combustion, which is H5's own question. One drive; 026 was not logged,
  so S5 is not read.
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
- **9/10/2026, all four injectors seated** (step 2c's holds, mean 026 by
  rpm band): cylinder 4 **19–28 % above cylinder 1** from 1400 to
  3350 rpm, against 25–57 % in the two 25/9 holds cut the same way, and
  **below cylinder 1 above 3350** (0.83) as before. Smaller, still on 4
  (`refuted.md` B7).
- **At idle all four sit on the floor** (0.31 V). 026 sees nothing there.
- Cylinders **1 and 4 read about twice 2 and 3 in every state, fired or not.**
  That pair is the crank-symmetric one and is explained without a fault (see
  `refuted.md`); only cylinder 4's excess over cylinder 1 is
  open.
- ⚠ 026 is the voltage *with the ECU's amplifier factor included* (Ross-Tech's
  block list), and cylinders 1 and 4 are probably on different sensors (G61
  for 1–2, G66 for 3–4, from a sister engine's manual, not the AQY page). So
  comparing 4 against 1 is weaker than the tables make it look.

### S6. The exhaust is not tight — reopened 10/10/2026

**Reopened at the owner's decision, 10/10/2026**: the joint remade on
9/10 **is heard again** (*owner*). Its cause is the one noted at
closing: the pipe behind reads **about 54.2 mm** against the connector's
**55** (*owner-measured*), so even fully tightened the narrower pipe
**moved in the connector**. The closing note said a connector change
would be a repair rather than a reopened symptom; the owner reopened it
because it is again a noise in the zone being listened to. **The fix
planned** (*owner*, the method *general*): the connector off, a shim of
thin sheet — about 0.4–0.5 mm, stainless, **not galvanised** — wrapped
round the narrower pipe under it, a thin coat of exhaust sealant under
and over the shim, the bolts tightened evenly and again after the first
heat cycle, and the hangers checked for strain. **Why it matters here**:
behind both probes, so still nothing for the mixture or the misfires,
but **it drowns S15** (S15 ↔ S6) **and vents the tailpipe test** (`plan.md`
step 3), so H2 cannot be tested past it.

**Can this joint make 014 count?** (*the owner's question*, 10/10/2026,
after another assistant suggested exhaust pulses disturbed by a leak
behind the probe could read as misfires.) **No, on this car's data**:
014 counted at every warm stop on 9/10 (`30`, S3 *Steps 2b and 2c*),
the day the joint was remade and quiet; it counted in August, on the
old converter, before any of this exhaust existed; and the dips it
follows are 720° events on one firing at a time that come when the
idle governor trims the charge (S1, *What comes before a dip*) — a
leak behind the converter, past all four cylinders' merged flow, has no
way to pick a firing, and a slightly lower back pressure is if anything
easier on the idle (*reasoned*).

*What closed it on 9/10:*

**Closed at the owner's decision, 9/10/2026.** The joint behind the
converter was taken apart and remade with a new two-bolt sleeve connector
and exhaust sealant (*owner, photographed*:
`photos/exhaust-joint-2026-10-09-old-parts.jpg` — the old slotted sleeve,
band clamp and pressed half-shells — and
`photos/exhaust-joint-2026-10-09-new.jpg`, the new connector in place,
sealant at both ends). *`plan.md` step 2 expected a new flange; the photo
shows a sleeve connector, and the photo wins.* **A little play remains**:
the pipe behind the joint is about 1 mm narrower than the one ahead of it
(*owner*), which the sealant is expected to take up. The owner expects it
to blow far less; should it not, a reducing (asymmetric) connector is the
later fix, and it would be recorded as a repair, not reopened as a
symptom. Out of every fit table, as it already was. The record of what it
was follows.


**Mostly acoustic**, and it has never been tight: holes in the old system, then
a joint behind the converter that the garage filled with sealant, which shook
out within two weeks and rattled under the driver's seat, loudest at about
3000 rpm and on the overrun. The clamp is now tightened as a temporary fix,
without sealant; the joint **hums slightly** and no longer rattles. The owner
made it tight on 9/10/2026 (above; it was the garage's to redo until
3/10/2026).

**That joint is downstream of both lambda probes**, so it cannot affect the
mixture, the trims or any misfire. What matters for the other symptoms is
whether there is a leak **ahead of the front probe** — the original, 26-year-old
manifold, the new gasket at its flange, the probe boss. Nobody has tested
that; the owner will if H2 comes up again (`plan.md` step 3).

### S7. The cold start — closed 26/9/2026

**Fixed by the new injectors.** An overnight cold start at 14 °C of coolant,
in cold fog, cranked in 0.93 s and fell only 74 rpm after first firing,
against 1.24 s and a near-stall (451 → 311 rpm) on the old injectors. The
table and the reasoning are in `refuted.md` C3.

### S8. Top end — "loses breath above 5000 rpm" — closed 4/10/2026

**Closed at the owner's decision, 4/10/2026, with its first criterion
(below) met only in part.** The hard drive of 4/10 (`28`) held full
throttle to 5,770 rpm, and b7 eased rather than dropped — a median of
185 / 187 / 183 / 181 from 4,000 to 6,000 rpm in 500 rpm bins, against
`24`'s 192 / 192 / 187 / 181 — and the owner felt the car pull better at
the top than before. **What the criterion asked and this is not:** a held
pull in 4th to 6,000 rpm with the display's `Power`; these were mixed
gears, the MFD was out, and the 5,500–6,000 bin is 47 frames. Out of
every fit table, as it already was.

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

### S9. The rich lambda trim — closed 4/10/2026

**Closed at the owner's decision, 4/10/2026, short of its own criterion
below.** The criterion asked for a read after a few hundred km with no
battery disconnect; that read was never taken, because the battery came
off twice more. What there is instead: every 032 read since the MAF swap
has stayed near zero — −3.1 / +4.7 % on 24/9, −0.8 / +2.3 % on 4/10 —
against the label file's −10…+10 % for both cells, and nothing like the
−16.4 / −13.3 % of the old MAF has come back. Out of every fit table, as
it already was.

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

**After step 1b, 4/10/2026: −0.8 / +2.3 %** (idle / part load), read
with the engine off at the end of session A — about 45 minutes of
learning after a battery disconnect, so not the closing read
(`photos/vcds-032-2026-10-04-after-sessionA.jpg`). The idle cell is
**not positive**, so it gives H3 nothing. The label file's specification
for both cells is **−10…+10 %**.

**Read it only after the MAF's orientation is settled**
(`idle-log.md`, *The MAF*, 3/10/2026). If the housing sat
turned 180° about its axis, its sensing channel sampled the other side
of the duct; that
can only bias the reading by a constant few per cent, which the trims
absorb (*general*), so the trims may move a little after the turn. A
move there is the turn, not a new fault.

### S10. Oil leaking at the back of the head — closed 4/10/2026

**Found and repaired** (*owner's decision to close, 4/10/2026*): the cover
gasket, first the hardened original and then the wrong part fitted on
2/10, replaced on 4/10 by Elring `915.653`; the joint stayed dry through
both sessions of that day, hot and cold. The re-tightening of the outer
nuts after a few hundred km stays in `plan.md` (*Standing items*). Kept
here for the record; out of every fit table since.

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
- **Both seals are there — 1/10/2026** (*owner, at the job,
  photographed*): **item 5 under the breather**, a flat black ring with
  notches on its inner edge, wet with oil; and **the cap's seal sits in
  the cap's own body**. *Corrected 2/10/2026 by the owner's photograph:
  it is a separate plain flat ring seated in the cap, which comes out —
  this bullet said "not as a loose ring".* *This bullet used to read
  "Preliminary, 30/9/2026: no seal at the breather at all" — a quick look
  before anything came off, which the job has corrected* (`refuted.md`
  C14). The oily lower body seen on 26/9 is therefore not an unsealed
  seat; what is left for it is the cover gasket and the breather itself
  (H9 test 4).
- **The rings side by side, 2/10/2026** (*owner, photographed*): the
  `100690` (its bag: *Vergl. Nr. `06A 103 483 D`*, for VW-Audi) is **the
  same size as the cap's old ring**, only with three notches on its inner
  edge, and it seats in the cap more easily; and **the ring the new
  `32452` comes with fitted is the same as the `100690`**, so it stays on
  the breather. So **item 5 and item 2 are the same ring** — the
  second-hand claim above, now settled by the parts. The old item 5 is
  another matter: H9, *The old ring under the breather*.
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

**At the job, 1/10/2026 — the cover nuts were loose** (*owner-found,
photographed*): **six of the eight came off by hand**; only two needed
the ratchet. The old gasket came off **relatively well preserved** —
stuck down in places — and the owner doubts it is the original one.
**Beside the new one, 2/10/2026** (*owner, by hand*): **hard, almost like
plastic, and still holding the shape it was fitted in**, where the new
one is supple rubber and far more flexible. *This paragraph used to say
"still supple in the photographs" — Claude's reading of a photograph,
which the owner's hands correct.* A gasket that has taken a set no
longer follows the joint as the nuts back off (*general*), so the hard
gasket and the loose nuts are one story rather than two; it changes no
fit table, being a finding on a part. *Reasoned:* a joint whose nuts have
backed off leaks with any gasket, so **the loose nuts are the most
direct explanation of S10** — more than the gasket's age, which the
section above assumed. It also bears on the decision just above: the
risk it accepted, a loose joint, is exactly what was found, whoever
last fitted the cover. **The re-check after the first warm run and
after a few hundred km is therefore not optional.**

**Decision, 1/10/2026 (the owner's), replacing the hand-only rule above
for this refit:** the nuts are tightened **firmer than "lightly
compressed"**, evenly and crosswise, with feel — still by hand, no torque
figure. **Done 2/10/2026 with a ratchet, by feel, about 4 Nm at most by
the owner's estimate** (*owner*) — "by hand" here meaning without a
torque wrench, not fingers alone. **The new gasket gave as it was
tightened**: the middle nuts, done first, had slackened once the outer
ones were down, and were taken up again until all were even (*owner*).
The new gasket settling under the first pull is the same mechanism this
section blames for the old nuts backing off (*reasoned*), which is why
the middle nuts — out of reach once the plenum is on — are worth one
more round before it goes on. **No threadlocker** (Loctite 243 considered and set aside: the
nuts most likely lost their clamp to the gasket settling, which a locked
thread does not prevent, and it would hide the re-check). **The re-check
is limited to the outer nuts** that can be reached with the plenum on —
the middle ones would mean taking the plenum off again, which is not
done for this.

**The job itself — done 1–2/10/2026 — is recorded in
`idle-log.md`, *The valve cover and throttle job***; what follows it is `plan.md`. *Owner's decision, 27/9/2026:* the cover gasket, the
breather and its seals, the upper plenum gasket, the injector refit
(H3, *The injector seats*) and the cleaning all in one job, with no
measurement between them. What it costs: an improvement afterwards cannot
be put down to one part. What stays separable all the same: S11's smoke
(the oil), the `--cylinders` pattern (the injector seats move f = 0.25,
not f = 0.50) and S4/S5 on cylinder 4 (H5).

**The before-values for the repair are the ones already in S1** — the warm
band at 69–72 °C of oil, loads off; the after-reading is taken the same way.
No separate cold baseline was taken.

**Leaking again on the first warm run, 3/10/2026** (`idle-log.md`,
*The first warm run*): dry at a cold start, then **a stream of oil at
the half-moon arch at cylinder 4's end** by the in-band stop, about 20
minutes after the start, and down to the coil. **Not only there**: with
the cover off, a little oil also at **the back of the joint**, so it
probably leaked there too (*owner*, 4/10/2026; this used to say "nowhere
else along the joint", which was the look from outside on 3/10). About a
litre in all ran down **to the right, over the wiring harnesses and down
to the driveshaft** — none onto the exhaust manifold or the back of the
head (*owner*). The candidates, none settled, all *reasoned* except the last:

- **the gasket out of its groove at that arch** — set in crooked as the
  cover went down, so the corner was never under the gasket. The
  photograph shows the gasket's edge pushed out into a loop there, which
  fits, but a photograph of an oily corner is not a finding;
- **the Dirko at that arch not bridging** the step between the arch and
  the straight run — the four arch points are where a cover gasket needs
  the sealant, and where it leaks when it is short;
- **the nuts slack again**: ~4 Nm by feel on a gasket that was still
  settling when it went on (the middle nuts slackened once already). The
  re-check of the outer nuts after the first warm run was planned for
  exactly this;
- **the strips stacked the wrong way on that side** (*owner*, 3/10/2026):
  the wiring-loom bracket under the front and rear hold-down strips, where
  the video of the job puts it on top of them — so the clamp at that end
  may sit on the bracket rather than on the cover.

**Dry cold and leaking warm** says the joint opens as the head and cover
heat and the crankcase sees pressure; it does not say which of the four
(*general*).

**The cause, found the same night — none of the four: the gasket was for
another engine** (*owner*, cover off, photographed; `idle-log.md`,
*The wrong gasket*). The Elring `325.070` fitted on 2/10 has **an open
arch where this head needs a half-moon**: assembled, it leaves **a hole
about 1 cm across** from the crankcase to the outside at cylinder 4's end.
It also has **no metal sleeves** at the bolt holes and a taller, softer
section. The gasket that came off has solid, ribbed half-moons and
sleeves. So the joint could not have sealed whatever the nuts, the Dirko
or the strips did, and the four candidates above are moot. A soft section
with nothing to stop the nuts also fits the oil at the back of the joint
(*reasoned*).

**How the wrong part was chosen.** `325.070` (cross-referenced to VW
`06A 103 483 C`) was matched **to the car, not to the engine**, by
mlparts' catalogue (the parts list above, 27/9). autokelly lists it for
AZJ, BER, AZG and AEG — **not AQY** — and lists **Elring `915.653`** for
APK, AQY and AEG, with solid half-moons and sleeves, cross-referenced to
VW `051 103 483` A/D/E (*owner, 4/10/2026, screenshots*). The upper
plenum gasket `271.230` is not in question: the garage ordered it by VIN
on 17/9, and it has come off whole three times. ⚠ **A catalogue match by
vehicle is not a match by engine code**: a Golf IV 2.0 / 85 kW was built
with more than one engine, and on this car it cost a job. Every part from
now on is checked against the engine code, or against the part that came
off.

**Whether the leak bears on the idle.** The breather vents the crankcase
into the intake **behind the MAF** (the MAF-to-throttle hose, H9), so a
joint open to the outside is, at idle, a path for air the MAF does not
see (*general*: at idle the crankcase sits slightly below atmosphere
through the breather's valve). **The hole was about 1 cm across, and open
from the first start** — the oil only came through once warm, but the
air path was there cold too. Yet session A shows **no leak signature at
the cold start** (S3, *Session A*): 003's air and 055 read as on `19` and
11/9. *One reading, not tested:* the job of 1–2/10 sealed old paths (the
breather's melted ring, the injector seats) about as much as the hole
opened a new one. The cold idle did dip more (22 a minute against 12–14),
which a leak would also do. At the
warm stops 055 read about −1.1 g/s with the learned value moving
negative, which a leak would also do; **there is no warm 055 baseline to
set it against** (055 was logged only on the cold start of 11/9), so this
is a question and not a sign. It is why the misfire verdict is taken
again after the joint is sealed (`plan.md`).

**Under load it did bear, and measurably.** *Owner, 4/10/2026:* the engine
pulled worse on 3/10 — first a warm-up drive, then, once the leak was
found, gentle driving home. The capture agrees: 0x280 b7 (indicated
torque) at the same engine speed and the same b5 (throttle), driving, oil
above 55 °C, medians over bins of 500 rpm and 10 counts of b5 with at
least 30 frames in each log:

| rpm | b5 | `19` | `24` | `26`, the hole open |
|---|---|---|---|---|
| 1500 | 80–89 | 118 | 112 | **92** |
| 1500 | 90–99 | 151 | 131 | **102** |
| 2000 | 80–89 | 114 | 102 | **84** |
| 2000 | 90–99 | 135 | 133 | **96** |
| 2000 | 100–109 | 153 | 151 | **106** |
| 2500 | 90–99 | 129 | 128 | **94** |

**18–30 % less at b5 80 and above**, where `19` and `24` agree with each
other; at b5 50–69 `26` reads the same or slightly more. Air density
explains a few per cent, not a third. *Reasoned:* the hole is driven by
the drop across the filter and the MAF, which grows roughly with the
square of the flow — next to nothing at idle's 3 g/s, a real share of the
air under load. Air the MAF does not see is load the ECU does not
compute, so b7 reads low, the fuel is metered short and the engine pulls
less. **So the hole's effect is load-dependent: small at idle, which is
why 003 and 055 showed no signature there, and large when driving.** ⚠ 3/10
never went past b5 105 (`24` reached 212), so full throttle is unseen;
whether the bins were steady or accelerating was not separated; one drive,
fresh adaptations. **What tests it:** the same table on the run after
step 1b (`plan.md`) — b7 back on `24`'s line if the hole was the cause.
**Tested 4/10/2026: it was not the hole** (`refuted.md` C18). With the
joint sealed b7 reads where 3/10 did; b5 is the throttle body's own
sensor, which was replaced between `24` and `26`, and reads 35 at idle
on the new part against 38 on the old.

**After step 1b, 4/10/2026: the joint dry** at the stop at 45–50 °C and
after the hot end of session A (*owner*), with the right gasket, Elring
`915.653`. Smoke at the back was old oil from the 3/10 leak burning off
(*owner*). **The re-check of the outer nuts after a few hundred km stays**
(`plan.md`, *Standing items*); S10 closes with it.

### S11. A hiss at the back of the engine at a warm idle

*Retitled 4/10/2026, from "Smoke, and possibly a hiss, at the back of the
head at a warm idle":* the smoke was S10's oil burning off (*owner*, 4/10),
and the hiss is now certain — heard again after step 1b, from the back,
not yet placed (below). What is left of this symptom is the hiss.

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

**How it closes:** the owner's tailpipe test from the head to the front
probe (H2, `plan.md` step 3) and the source of S10. *The checks it uses:*
a rag held over the tailpipe for 2–3 s makes an
exhaust leak hiss louder (a phone recording at the head, since it is a
one-person job); an exhaust leak ticks loudest in the first minute after a
cold start; dry black soot at a joint is exhaust, wet oily grime is oil
(*all general*).

**After the job, preliminary — 2/10/2026** (*owner*): through the
check-start runs, **no smoke at the back and no hiss** seen or heard. The
engine was cold or part-warm, never at the warm idle where S11 was seen,
so this decides nothing yet. Looking back, the owner thinks it came from
the old breather — the loose seat and the flowed ring (H9). **To be
checked at a warm idle in session A.**

**After step 1b, at the hot stop — 4/10/2026** (*owner*): **the hiss is
still there**, heard at the hot idle at the end of session A with the
cover joint dry and the new breather in, **from the back** of the engine;
the owner suspects **the exhaust manifold or its gasket to the head**.
Before the job he heard more than this, **around the breather (PCV)
too**; that part is gone, and only something at the back is left. No
smoke beyond old oil from the 3/10 leak burning off. Whether it rose or
fell with the throttle blips **could not be told** — the engine drowned
it. So the breather (H9) and the cover gasket are out as its source, and
**what is left is the reading this section already gave a hiss that
stays: the exhaust ahead of the probe (H2) or the intake at the back
(H3)**. The owner's direction is H2; the tailpipe test above is what
separates the two. *Owner, the same evening:* he still hears a hiss
somewhere in the engine bay and **cannot place it**. An intake hiss is
what the smoke test of `plan.md` step 2a would show. **9/10/2026: the
intake smoked tight cold** (H3, *Smoke test of the intake*), so an intake
hiss now needs a joint that opens only warm or under vacuum.

*10/10/2026, owner:* **not heard any more in the engine bay**, listened
for on purpose. Kept open; noted, not closed.

### S12. A hesitation on tip-in, and after a gearchange — closed 4/10/2026

**Withdrawn by the owner, 4/10/2026**, after watching for it on that day's
drives: what he took for a hesitation is, in his judgement, **mechanical
play** — in the engine's mounting or the driveline — and the hesitation
itself he no longer feels; whether he felt one before, he cannot now
say. Out of every fit table since.

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

### S13. The throttle runs its routine at every ignition-on — closed 2/10/2026

**How these parts behave**: the new throttle runs the same 20 s routine
after its own completed 098 (*The new part, timed*, below); `refuted.md`
C16. Kept here for the record; out of every fit table since.

*Owner-reported, 28/9/2026; added as a symptom at the owner's decision.*
With the ignition left on and the engine not started, the throttle is
heard working for **20–30 s**, like seeking its stops — **at every
ignition-on**, not once after a disconnect; confirmed to come from the
throttle. Usually the engine is started straight away and the routine is
cut short. **The engine's fault memory is empty, and 17973 has never been
seen** — read empty again on 1/10/2026, before the battery came off for
`idle-log.md`, *The valve cover and throttle job* (*owner-reported*). Whether it also did this after the June manual adaptation is not
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

**The old part, timed — 29/9/2026** (*owner-measured, stopwatch*;
battery reconnected after 26/9, engine not run):

| | routine at ignition-on |
|---|---|
| before any adaptation | **20 s**, then one click |
| 098 itself | min and max found quickly, *ADP OK* — **within VW's 10 s** (not timed, clearly shorter than the routine) |
| ignition off, on again, after *ADP OK* | **20 s** again, then the click |

- **The routine is not the adaptation.** VW's adaptation is the short
  thing 098 does and it completed; the 20 s routine ran unchanged
  straight after it. So **the loop reading is refuted on the old part**
  (H8, *So two readings*): the idle has not been running on an unfinished
  adaptation, and S13 no longer touches S1 that way.
- **20 s is the length now**, not "20–30 s": timed twice alike. Longer
  than the owners' ~15 s, which were never timed either.

**How it closes** (the first start after the job, `idle-log.md`, *The valve cover and throttle job*): the new part
after its adaptation, before the first start, timed the same way.
**New part silent, or clearly shorter → the old unit differed**, and S13
becomes a lead on it (H8). **The same routine → it is how these parts
behave**, and S13 closes as normal.

**The new part, timed — 2/10/2026** (*owner-measured, stopwatch*;
battery reconnected, engine not run): 098 gave **ADP OK** (photographed:
10.4°, 59.2 %, *volnoběh*), and at the next ignition-on the new part ran
**the same routine, 20 s, as the old one**. By the rule above that is
*how these parts behave*. **S13 closed on this**, its column out of every fit table.

### S14. Bangs from the exhaust on a downshift without a blip — closed 10/10/2026

*Owner-reported, 4/10/2026; added as a symptom at the owner's decision.*
On a downshift **without a throttle blip**, the exhaust often lets out a
**series of small bangs**, as if unburnt fuel were burning in it. What
the owner has observed:

- **with a blip, almost never**; without one, often but not every time;
- **only on a downshift** — not on a plain lift-off in gear;
- about **one to two seconds after the clutch comes up** (*the owner's
  estimate, not timed*);
- **warm, and clearly** on 4/10 — not a cold-engine effect;
- often **right after a misfire episode**, after an idle for example —
  the owner's impression, never aligned with 014;
- **the same sound as the cold-overrun burble** that `refuted.md` A1
  and C1 put down to the old injectors. Those were replaced on 23/9, so
  that attribution does not hold; both entries now say so;
- none of the owner's other cars does it. The owner avoids doing it
  until it is fixed.

**What happens in that second** (*measured*, `coastscan.py`, `refuted.md`
C1): the ECU shuts the injectors **0.78–1.39 s after the pedal comes up**
— counted from the lift, not from the clutch, and measured on coasts in
gear, never on a downshift. **How the owner downshifts** (*owner,
4/10/2026*): pedal up and clutch down together and fast, then the
clutch let out **slowly at the end**, so as not to jerk the car — a
blip most of the time, sometimes not. So the delay starts with the
clutch, not ahead of it, and the slow end of the release is a stretch
of the engine being dragged up on a shut throttle. **Whether the ECU
fuels or cuts through that stretch is not measured**, and how long it
lasts is the owner's to vary; "one to two seconds after the clutch"
sits inside it. Which is what the owner's reading predicts
(*4/10/2026*): **fuel left unburnt in the exhaust, burning when air
reaches it.**

- **Where the fuel comes from: a cylinder that did not burn it.** The
  engine is pulled up by the wheels with the throttle shut, the highest
  manifold vacuum it ever sees and the thinnest charge, and it is still
  being fuelled. A charge that fails to fire there leaves for the
  exhaust as fuel and air. That is a misfire at the lightest load, the
  same family as S3, and **where 014 is blind**: it does not count on the
  overrun or in transients (S3). The delay before the cut is the
  factory's and every engine has it, so this is not "normal" by itself —
  a healthy engine burns that charge.
  **Why a small intake leak would show here first** (*general*): the
  vacuum is at its highest, but a small hole passes little more air for
  it — once the manifold is below about half an atmosphere the flow
  through a hole is choked and barely grows. What makes the leak matter
  is the other side: the charge per cylinder is smallest and carries the
  most residual exhaust, so the same small lean error that an idle just
  survives is enough here to stop it firing.
- **Where the air comes from: the cut itself.** Once the injectors shut,
  every cylinder pumps plain air into a hot exhaust that still holds the
  unburnt charge of the last fuelled revolutions. So the bangs can come
  **after** the cut and still be fuel injected **before** it (*general*).
  A leak ahead of the converter (H2), or S6's joint (resealed 9/10),
  would add air but is not needed. A blip opens the throttle and matches the speed, so those
  last fuelled firings burn, which is why it nearly stops it
  (*reasoned*).
- **"Left over" means seconds, not minutes.** A hot exhaust is flushed
  through in a few seconds at idle (*reasoned*, not measured), so fuel
  from a misfire episode at the last stop is gone long before the next
  downshift. What the episodes do is say the engine was misfiring then,
  and plausibly still is at the next, lighter load.
- **Fuel with none commanded — an injector that does not seal, or a
  regulator diaphragm passing fuel at high vacuum (H7) — is the weak
  reading.** The injectors are from 23/9 and the regulator from 7/2026;
  the regulator's vacuum hose was dry each time it came off (H7); and
  the original fuel hoses could only leak outwards, never into a
  cylinder (*owner, 4/10/2026*). This was C1's reading of the cold
  burble, and it no longer fits.

**The owner's decision, 4/10/2026: S14 is his to watch, and it is not
in `plan.md`.** He expects it to go with S1/S3 and will not provoke it
meanwhile. Once the idle is fixed he checks it himself; **only if S14
outlives S1/S3 is it worked on further.** The test below stays as
reference and is not scheduled.

**Test, if it is ever wanted:** one or two downshifts
without a blip, each written into the chat ("3→2, bangs" / "no bangs")
and aligned to the capture by the jump in engine speed as the clutch
comes up, not by when the message arrived. 0x480 gives how much was
injected after the clutch came up and when the cut fell — so how many
fuelled revolutions at the thinnest charge preceded each bang. Bangs
**and** a cut long before the clutch came up would point back at fuel
with none commanded. A search of `24`–`29` found no unblipped downshift
clean enough to read; the bangs themselves are not on the bus.

*9/10/2026, owner:* **no bangs at all** on the drive of steps 2b/2c,
downshifting without a blip on engine braking exactly as before — the
first drive after the joint behind the converter was remade that
morning (S6). So the bangs, or the air that made them bang, may have
been that joint's (*S14 ↔ S6* below) — **or the tighter exhaust now
simply carries less of what goes on inside it to the ear** (*owner*).
**Kept open** (*owner's decision, 9/10/2026*); one drive, and the owner
keeps watching.

**Closed 10/10/2026** (*owner's decision*): **no bangs on 9/10 or 10/10**,
downshifting unblipped as before, and the owner is fairly sure of it.
They stopped with the joint behind the converter (S6), the day before
the new plugs and leads, **while S3 kept counting** — so they were not
the idle's, which is what the decision of 4/10 above asked before S14
was worked on: they did not outlive S1/S3, they left without them. The
owner's reading: likely not related to the idle at all. Taken out of
every fit table the same day; the relations below are kept as written.

### S15. A constant sputtering from the exhaust near the engine

*Owner-reported, 9/10/2026; added as a symptom at the owner's decision.*
A **sputtering, spitting sound**, as of gas escaping from the exhaust
somewhere **close behind the engine** — heard from under the car, "almost
as if from the engine". What the owner has observed:

- **constant, not occasional** — which is what separates it from S2's
  puff;
- at idle, and **also at full throttle and under heavy load** — not a
  clean exhaust note there either;
- first heard on 9/10, **once the joint behind the converter was
  remade** (S6): before, that joint's own noise drowned it. The owner
  thinks it has been there a long time.

*Reasoned, not measured:* a leak that sputters at every load is one the
exhaust's pressure pulses push out of, which points at a joint between
the head and the converter — the manifold, its gasket to the head, the
probe boss, the manifold's outlet flange (H2's zone), or the joints just
behind it. Ahead of the front probe it would also draw air in between
pulses at idle and read lean to the probe (H2). Where along that length
it is, is the tailpipe test's question (`plan.md` step 3).

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

**The brake pedal is soft and long** (*owner-reported*, 9/10/2026): a
firm stop needs the pedal pushed a long way. **Not an engine symptom,
and not the servo** — a servo that loses vacuum makes the pedal *hard*
(*general*); soft and long is the hydraulics: air or old fluid that has
taken up water, worn pads or discs, the master cylinder (*general*). It
is here only so that `plan.md`'s servo checks are not read through it.
A safety matter for a garage, outside this investigation.

---

## How the symptoms relate — what is measured

| pair | link | evidence |
|---|---|---|
| S1 ↔ S3 | **the same events** | aligned three times, p ≤ 0.023. Both are crank speed, so partly one signal read twice |
| S1/S3 ↔ S9 | **strong** | the MAF swap halved the dips at every oil temperature (−51 to −65 %). An over-reading MAF was causing some of the stumbles; the rest is the residual fault |
| S1/S3 ↔ oil temperature | **strong; the two differ** (*re-read 9/10/2026*) | **S1** (engine speed) roughest cold and calmer as the oil warms, in every session since 24/9. **S3** (014): near zero cold — the counter's own blind spot, since engine speed is worst there; on fresh adaptations a sharp peak in the middle band and zero hot; **on settled ones flatter** — 6–16 a minute from ~40 °C up, about half as many at 70–80 °C as at 55–68 (`29`, `30`). *This read "non-monotonic, worst at ~50–61 °C, on every drive" for both* |
| S4 ↔ S5 | **very likely one thing** | same cylinder window, same engine speeds, and S5 needs no combustion. Knock control retards cylinder 4 because it hears S5's noise |
| S4/S5 ↔ S1/S3 | **none measured** | no retard and no 026 signal at idle, in any log. Only a common cause could link them |
| S2 ↔ S3 | **likely, by the owner's reading; never aligned** | the owner takes S2 for S14's smaller twin, a misfire's charge going off in the exhaust (S2, 4/10/2026). A leak ahead of the probe would puff too (H2) |
| S2 ↔ S6 | **possible**; **S6 reopened 10/10/2026** | if there is a leak ahead of the probes. The known leak was behind them. A puff that outlives the resealed joint did not come from it |
| S5 ↔ S6 | **no**; **S6 reopened 10/10/2026** | the clamp was tightened and cylinder 4's excess stayed exactly as it was |
| S7 ↔ S1 | **none** | S7 improved with the injectors; S1 did not |
| S8 ↔ anything | **none** | top-end air and b7 identical on both MAFs; the idle changed a lot. **S8 closed 4/10/2026** |
| S10 ↔ S11 | **the smoke, yes; the hiss, no** | the smoke was S10's oil burning off the manifold (owner, 4/10); the hiss stayed after S10 was repaired. **S10 closed 4/10/2026** |
| S11 ↔ S2 | **possible** | an exhaust leak ahead of the probe both hisses and puffs. Never observed together |
| S11 ↔ S6 | **possible**; **S6 reopened 10/10/2026** | if the hiss is exhaust, "never tight" reaches upstream of the probes too |
| S10/S11 ↔ S1/S3 | **S10: the hole of 3/10 bore on 014 that day; closed. S11: untested, not weak** | nothing measured so far *could* have shown a link, so "unknown" is no evidence against one. Oil outside the engine does not touch combustion; what can is the cause or a neighbour: a vacuum leak at the unsprayed rear hissing (H3/H9), the ventilation's oil fouling the throttle (H9 → H8), an exhaust leak ahead of the probe (H2), oil reaching a lead boot (H4, 1e) — seen on 26/9 at the boots of 3 and 4, but **not a cause**: the idle was as rough on 17/9 with new, clean leads (S10). The one existing datum that points this way: the idle is better under load, which is what a small unmetered leak does |
| S12 ↔ S4 | **S12 closed 4/10/2026**; was possible, untested | the knock retard is a tip-in event and a retard is lost torque. Never aligned in time |
| S12 ↔ S1/S3 | **S12 closed 4/10/2026**; was possible, untested | both start from the bottom of the load range; a lean or weak-spark cause would show in both |
| S14 ↔ S3 | **possible, owner-reported** | the bangs often follow a misfire episode; never aligned, and 014 does not count on the overrun, so it cannot be |
| S14 ↔ S2 | **likely one mechanism** (*owner, 4/10/2026*) | both are a misfire's charge burning in the exhaust: weak at idle, where it brings only its own air; loud on the overrun, where the fuel cut adds plain air behind it |
| S14 ↔ S6 | **possible**; **S6 reopened 10/10/2026**, S14 stays closed until bangs return | a leaky joint draws air in and feeds an afterburn; behind both probes, so it cannot cause the misfire. Bangs that go on unchanged after the reseal were not fed by it |
| S15 ↔ S2 | **possible** | a leak ahead of the probe can puff now and then as well as sputter all the time (H2). S2 is occasional and S15 constant, so they are kept apart |
| S15 ↔ S11 | **possible, never compared** | an exhaust leak at the head can hiss as well as sputter; whether the owner's hiss and the sputter are one sound has not been asked |
| S15 ↔ S6 | **masking only** | S6's joint was louder and hid S15 until it was remade (*owner*, 9/10/2026), **and can again from 10/10**; behind the converter, it cannot be S15's source |
| S15 ↔ S1/S3 | **untested** | only through H2: air drawn in ahead of the front probe leans its reading and the mixture follows. 033 and 032 have not shown the positive correction that would need (S3) |
| S13 ↔ S1 | **weak** | the one link was an adaptation that never completes, leaving the idle on unfinished values (H8); **refuted on the old part 29/9** — 098 completed and the 20 s routine ran unchanged after it (S13). **Closed 2/10/2026**: the new part does the same |

**So there are two separate clusters**, and they are worked separately below:
**the idle** (S1, S2, S3; S15 joins it if it is H2's leak; S14, on the overrun, closed 10/10) and **the cylinder 4 window** (S4, S5). S7, S8, S9
and S12 are closed; **S6 is open again (10/10)** but behind both probes,
and what bears on the idle is still the exhaust **ahead of** the front
probe, which is H2's. **A third cluster, the back of the head
(S10, S11)**, appeared on 26/9 — S10 is closed (4/10/2026), the hiss
remains; its oil is the valve cover job, its hiss the owner's
exhaust test; whether it joins the idle cluster is exactly what H2 and H9 ask.

---

## The open hypotheses

Each one lists what it explains, what speaks against it, and the test that
settles it. ✔ fits, ~ fits weakly, ✘ does not fit, — says nothing.

**The columns are the open symptoms that bear on the engine.** Left out,
each for a stated reason: **S6** (reopened 10/10/2026, closed 9/10: the
joint behind both probes; never a column, being acoustic and behind the
probes, so neither closing nor reopening it moves a table — the part of
it that bears on the idle is H2's), **S7** (closed), **S8**
(closed 4/10/2026), **S9** (closed 4/10/2026: fixed by the MAF),
**S10** (closed 4/10/2026: the cover joint, found and repaired),
**S12** (closed 4/10/2026: withdrawn by the owner as mechanical play),
**S13** (closed 2/10/2026: the new throttle behaves the same),
**S14** (closed 10/10/2026: gone with S6's joint while S3 stayed). S12 and S13 were added on 28/9/2026: **S12**, the tip-in
hesitation, fits a lean tip-in (H3/H9, H7), a moment of knock retard (H5)
and weak spark under sudden load (H4); **S13**, the throttle's routine, was
H8's alone.

**S14 was added on 4/10/2026** and judged the same way for every row: a
misfire at the thinnest charge (H3 ✔, H1/H4 ~, and H10 ~ until it closed 9/10), air ahead of the
converter to burn it in (H2 ✔), or fuel nobody commanded (H7 ~, the
weak reading: every part that could pass it is new). H0 ✘: the owner's other cars do not do
it, and it follows the misfire episodes. H5, H8 and the closed H9 say
nothing about it.

### H0. The idle is normal for this engine — and there is no fault to find

**The one hypothesis nobody has been able to test.** An AQY with 26 years on
it might simply idle like this, and every number above might be its normal
state.

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ~ | ~ | ✘ | — | ~ | — | ✘ |

- **Against:** 014 reads **12–120 against VW's own 0–5**. The old converter
  burned through, which needs raw fuel in it. The owner feels it.
- **For:** no fault code; the counter's sensitivity moves with the MAF and with
  battery disconnects; today's best hot idle (57) is in the neighbourhood of
  August's, before any work (48). **Why no code is ever stored**
  (*9/10/2026*, `vcds.md`, *What the number is*): VW's Motronic M5.9
  stores P0300/16684 only above a **2 % misfire rate over 1000 crank
  revolutions** — at 780 rpm about 31 misfires a minute. 014's 6–16 rises
  a minute are 0.4–1 % even if each rise were one misfire, which nobody
  has shown. So the empty fault memory says *under 2 %*, not *healthy*:
  it is consistent with H0 and with a small real fault alike. And for S5: there is no healthy AQY's 026 to compare with, so the
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

**Searched again, 9/10/2026, across the whole group** (VW, Škoda, Audi,
Seat; English, German, Czech; Ross-Tech's wiki and forums, RS246,
audizine, golf4.de, BRISKODA, Czech forums): **still no posted 014 log
from an engine described as healthy**, on any VAG petrol. What exists is
the specification — 0, in every label file and repair list found (the
AUA's, a Ross-Tech label file for the Audi 2.4) — and forum advice that
a good engine reads 0 with detection active. One search summary gave
"0 to 10" at idle for an A8 D3 V8; the page refused to open, so it is
**not used**. Forum cases with idle counts all end in a fault found
(an Octavia 1.6 MPI with counts on 1 and 4 at idle only, gone with new
leads after a corroded contact; a timing-chain fix elsewhere). So test 1
stays the only way: **any** VAG petrol with a 014 counter at a warm idle
would say whether such counters sit at zero in practice; an M5.9.2 2.0
8V (AQY, AEG, APK, AZJ) would also answer for this calibration.

### H1. A lifter or valve on one cylinder at a hot idle (valvetrain)

A hydraulic lifter that bleeds down or pumps up leaves a valve slightly open
or late, intermittently, and gets worse as the oil thins. *General.*

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ✔ | ✔ | — | — |

- **For:** with H4, one of the **two candidates that can explain both
  clusters at once**: an
  intermittent leak past a valve at idle misfires, and puffs; a ticking lifter
  at camshaft speed lands in one knock window. Temperature-dependent through
  oil viscosity. Compression is a **cranking** test and does not see a valve
  that closes at 250 rpm but hangs at a hot idle.
- **Against, 10/10/2026** (*owner*): **no ticking**, listened for on
  purpose, where a lifter that bleeds down is usually heard. Weak: a
  valve that hangs slightly need not tick.
- **Against:** the idle is never worst hot, while a thin-oil lifter should
  be — engine speed is calmest hot, and 014 at 70–80 °C counts about half
  what it does at 55–68 (*re-read 9/10/2026*; this read "S1 is worst at
  50–61 °C and eases when hot"). The S5 excess switches on above ~2300 rpm and
  moves to cylinder 1 above ~3350, which fits a resonance better than a single
  part. No ticking has been reported.
- **From the Polish AQY thread** (see H4; forum.vwgolf.pl t=522030, page
  6, re-read 10/10/2026): **Kavior** (14/11/2013) put an AQY's idle
  vibration down to valves not sealing, and after **new piston rings and
  "a light going-over of the head"** it "practically disappeared" — new
  plugs and leads had not helped him; **nowed** (23 and 25/11/2013) had
  vibration, **bangs into the exhaust** and misfires, found **some carbon
  on the valves** and replaced **three valve guides**, and called it the
  head. Rings and head together, so the valves are not separated from
  the rings; a forum report. **No lifter in it** — the lifter case is the
  German thread below.
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

- **For, 10/10/2026, weakly** (S1, *What comes before a dip*): the dips
  come when the ECU has just taken a little charge away, which is when a
  valve that seals worse at low cylinder pressure would show — and when
  a leak at one runner would (H3), so it does not separate the two. *This
  also read "and in short runs on one cylinder", corrected the same day:
  the excess is a weak cylinder's share, not runs.* The same search found an Opel Zafira A with misfires at idle
  only, a few minutes after the start, **sticking inlet valves**, cured
  by an inlet-valve cleaner and hard driving (*autoservicepraxis.de*,
  FabuCar case, 6/2023 — another engine, a trade magazine's reader case,
  so a lead).
- **Inlet-valve deposits** are the other way a valve hangs or seals
  late, and the same search's general sources put them at a cold,
  low-throttle idle on port-injected engines (*general*): they soak up fuel
  while cold, which fits S1 being roughest cold. Nothing on this engine
  has looked at the backs of the valves. **Against, 10/10/2026**: the
  owner has run OMV MaxxMotion 100 since 2017 (`vehicle-history.md`), a
  premium fuel sold with a detergent package, which works against
  inlet-valve deposits building up (*general*); what the car ran on
  before 2017 is not known.

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
5. **The vacuum gauge** (`plan.md` step 3) reads H1 only through its
   rarer patterns — a regular flick, a flutter, flicks that stay at 2500;
   an intermittent flick at idle is any misfire (`plan.md` Part 2).
6. **The lifters pressed down, valve cover off**, cam lobe up: one
   that gives before the valve moves has bled down (*general*; a VW
   check of this kind is recalled, not read here).
7. **A borescope through the plug hole** — no running, nothing taken
   apart but the plugs (*the owner's question*, 10/10/2026; *general*).
   Engine cold, all four plugs out, each cylinder in turn, the crank
   turned by hand so the piston is down and the valves can be seen
   closed and open. **What it can show:** the combustion side of both
   valves — carbon on the faces, a burnt or chipped edge, a seat that
   shows light; the piston crown (dry soot, or wet with oil); scoring on
   the bore. Compared cylinder against cylinder, since nothing here says
   what this engine's chamber should look like. **What it cannot:** the
   back of the inlet valve, where port-injection deposits sit, and a
   lifter. The back of the inlet valve is reached the other way, the
   scope down an injector's bore in the manifold with that injector out
   — whether the angle shows the valve is not known until tried; or with
   the manifold off. A side-view (mirror) or articulating tip is what
   makes the valves visible at all; a straight-ahead scope sees the
   piston. A chemical inlet-valve cleaner is the cheap trial if it finds
   deposits, *not scheduled* — another run at idle, the owner's call.

### H2. A leak ahead of the front lambda probe (exhaust manifold, its joint to the head, probe boss)

At idle the exhaust pulses dip below atmospheric and a crack draws air in;
under load it only blows out. *General.* The front probe reads lean, the rear
loop absorbs it, so 032 barely moves (SSP 233 p. 16, the two-loop control).

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ~ | ✔ | ~ | ✘ | ✘ | ✔ | ✔ |

- **Against, mildly, 10/10/2026** (S1, *What comes before a dip*):
  this hypothesis acts on the mixture through the lambda control, and
  what comes before a dip is the idle governor's trim of the charge,
  not a lean swing of the mixture (as `refuted.md` C5 found for 014).
  Its sounds (S2, S11, S15) are untouched by this.

- **For:** the puff, idle only, an old manifold that has lived through years
  of misfires, the rear probe on the rich side at hot idle
  (0.665–0.725 V), the exhaust never having been tight.
- **Against, 9/10/2026** (*owner-reported*): **no ticking** is heard,
  cold or warm. A crack or a blown gasket at the head classically ticks,
  loudest in the first minute after a cold start (*general*). Weak — a
  small leak need not — and it fits a leak further back (the outlet
  flange, the front pipe), where S15's sputter "from under the car" also
  points, better than one at the head. **10/10/2026, again** (*owner*):
  no ticking, and **no smell of exhaust** in the engine bay, which a
  leak at the head would usually give. Weak, for the same reason.
- **For, 9/10/2026:** S15 — a constant sputter close behind the engine at
  every load, heard once the louder joint behind the converter was
  remade. The first symptom that is a leak heard rather than inferred;
  where along the front pipe it is stays open until the tailpipe test.
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
  a few per cent rich does not normally misfire. The MAF swap halved S1, which an exhaust leak
  would not care about. It cannot produce S5: that is there without exhaust
  pressure.
- **Withdrawn 9/10/2026:** "a crack leaks most cold, but S1 peaks
  mid-temperature". S1 does not peak there in any capture since 24/9 —
  it is roughest cold (S1, *Temperature matters*). That does not turn
  into evidence *for* this hypothesis: every engine idles roughest cold.

**Tests:**

1. **A pressure test** of the manifold, its joint to the head and the probe
   boss: the tailpipe closed for a few seconds at a warm idle, the known
   joint behind the converter made tight first. Looking is not a test.
   *The owner's own, decided 3/10/2026* (`plan.md` step 3), replacing the
   exhaust specialist; a found leak ahead of the probe means a new
   manifold.
   **Before it, a cold smoke test of the exhaust** with the intake smoke
   tester, fed into the tailpipe (`plan.md` step 2a, *owner's decision,
   6/10/2026*). Smoke ahead of the probe settles H2. Clean does not clear
   it, since a crack in cast iron may only open hot.
   **Done 9/10/2026** (*owner*): **no smoke anywhere** — the manifold
   or anywhere below — **but the exhaust would hardly take pressure**,
   so the owner rates it as saying little. With the converter, the
   silencer and the open valves to fill, that is what a low-pressure
   tester meets (*reasoned*). **H2 is neither cleared nor touched**;
   the warm tailpipe test (`plan.md` step 3) stays its test.
2. **Written before the repair, so the repair is a test:** if a leak ahead of
   the probes is found and sealed, the puff goes; the rear probe (036/037) at
   hot idle moves a little leaner; `IdleHealth` at 70–72 °C stays in its
   57–120 band; the mid-temperature 014 rate does not fall beyond scatter;
   cylinder 4's 026 excess does not change. **If the idle improves clearly,
   this hypothesis was underrated and the argument against it is wrong.**
3. If nothing is found, the puff is the misfire itself (H1, H3, H4, H5).

**S11 is the first physical sign for this hypothesis** (26/9): smoke and
possibly a hiss over the exhaust manifold at a warm idle. The smoke alone is
more likely S10's oil; **the hiss, if the tailpipe test confirms it, is this leak.**
Nothing else about the argument above changes until the test is done.

### H3. A small unmetered air leak at one intake runner

Air past the MAF leans one cylinder at idle, where air flow is smallest.
*General.*

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ✔ | ~ | ✔ | ~ | ✘ | ~ | — |

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
2. A smoke test of the intake, at home — **done 9/10/2026**, tight cold
   after the dipstick and the MAF clamp were put right (*Smoke test of
   the intake*, below).
3. 032 after a few hundred km: an idle cell moving positive would support it.

**The injector seats — three not fully home, 27/9/2026.** *Owner-reported
and photographed:* since the 23/9 refit, three injectors stand **under
about 1 mm** proud of their bosses; only cylinder 4's is
fully home, and an old injector alone clicked fully into every bore
(`idle-log.md`, *The injectors were not fully seated*). The manifold-end O-ring is all that seals them.

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
decision (`idle-log.md`, *The valve cover and throttle job*): the cure is wanted more than the
attribution.

**Found at the refit, 1/10/2026 — cylinder 2's manifold-end O-ring was
damaged** (*owner-found, photographed*). Cylinder 2's injector went in
harder than cylinder 1's, and is most likely the one forced in on 23/9;
its intake-side ring came off damaged. Cylinder 1's was fine. **This is
the first leak path found on a part since the investigation began** —
the seal that alone closes the seat against manifold vacuum (above) —
on one cylinder, present since 23/9. *What it does not settle*
(*reasoned*): whether the damage went through the sealing line, and so
how much air it passed, cannot be read from a photograph of a ring off
the part; and it is one cylinder, where A5 saw no one cylinder stand out
— though 2 sits in the 2-and-3 pair of the period-2 pattern under
*Naming the cylinder*. The fit table is unchanged; a stumble that fades
after this job is consistent with it, and so is one that does not.

**What went back in its place** (*owner, 1/10/2026*): the spare ring in
the new injectors' kit fits only the rail end, so cylinder 2 now carries
**the intake-side ring taken off one of the old injectors** — in service
until 23/9, looked fine and was refitted. *A decision, recorded as one:*
an aged ring is a weaker seal than a new one of the right size; it was
chosen over leaving the car open for a part. **The owner judged the ring
well preserved and soft** and does not plan a new one (*owner's decision,
1/10/2026*). If the idle does not settle, a new intake-side ring for
cylinder 2 stays the cheap first thing to fit.

**The dipstick tube — loose, its bracket missing, 4/10/2026**
(*owner-observed*, by hand and against videos of the same engine; a
finding on a part, not a symptom, at the owner's decision). The orange
upper guide's mounting tab holds nothing — the metal bracket that should
fix it is not there — the tube moves under the hand, the dipstick sits
a little loose in it, and **a small amount of fresh oil** shows round
its foot below; it may have backed out of the block again. The 2018
service record already lists a dipstick job against an oil leak (S10,
*Not the first leak*). **Why it belongs here:** the tube is an opening
into the crankcase, and the breather joins the crankcase to the intake
behind the MAF, so a tube that does not seal is a small unmetered leak
— the same kind as 3/10's hole in the cover, smaller than one on the
intake itself because what it admits has to pass the breather's valve.
**Against:** the dipstick read atmospheric with the engine running (H9
test 3), so the crankcase depression it would act on is slight; how
much it admits is not known. The fit table is unchanged.

**Refitted 9/10/2026** (*owner, photographed*:
`photos/dipstick-2026-10-09-bracket.jpg`, `-seated.jpg`, `-guide.jpg`).
**The lower metal tube was fully home in the block** (*owner*), so it
had not backed out. A new orange guide, **clicked onto the metal tube** and holding it
better than the old one, which was not visibly cracked but was very
loose at its foot. The original bracket could not be had, so a strip of
sheet metal is bolted to the head (thread-locked) and the guide is
cable-tied to it; the original can replace it if one turns up. **The old
guide was not this engine's part** (*owner*): its mounting tab sat
elsewhere, which may be why the bracket had been taken off. Side by side
with the new one (*owner, photographed*:
`photos/dipstick-2026-10-09-old-vs-new-*.jpg`): the old guide is bent
the other way — to the left, were the bracket where it belongs — and its
tab sits about 2 cm lower than the new, correct one's. *Inferred,
not known:* the 2018 dipstick job (*Not the first leak*, above) is the
likeliest time it went on. **What this settles:** the dipstick is now a
sealed, fixed path, so smoke at it in `plan.md` step 2a is a finding
rather than the loose fit. Nothing is claimed for the idle; the fit
table stays as it was. *It was not sealed after all: see the smoke test
below — smoke came out at the guide's seat on the metal tube.*
*What the web says, searched 4/10/2026* (forum threads and parts
guides, read only as search summaries — the threads themselves would not
open): the plastic tube on the Mk4/Beetle 2.0 is a **known failure**,
brittle with heat and age, and a cracked or loose one is a known intake
leak through the crankcase. The cases reported come **with a lean code
(P0171) or lean trims**, a rough idle, sometimes a whistle. This car
has **neither** — 032's idle cell −0.8 %, no fault stored — so a leak
here is possible but, if it is there, smaller than the forum cases.
Ross-Tech's own P0171 page lists intake leaks and the MAF, and does
not name the dipstick. Generic "most common vacuum leak" lists rank the
dipstick high; they are written for every engine at once.

**Smoke test of the intake, 9/10/2026** (*owner, photographed*:
`photos/smoke-intake-2026-10-09-1.jpg` … `-7.jpg`; Lincos tester, cold,
engine off, `plan.md` step 2a). Smoke into the regulator's vacuum hose,
the MAF out, the hose to the throttle plugged.
- **The one real leak: the dipstick, where the new orange guide seats
  on the metal tube** (*owner*) — **a stronger stream, not a wisp**. A
  crankcase path, so smoke reached it through the breather — the small
  kind, behind the breather's valve (above, *The dipstick tube*). **Put
  right the same day** (*owner*): the guide pulled off, the seat cleaned,
  clicked back on, and the sheet-metal bracket bent so that it presses
  the guide down onto the tube — perhaps what the original bracket did.
  Smoked again: **almost nothing, only a very faint wisp**
  (`photos/smoke-intake-2026-10-09-8.jpg`). **No sealant on the seat**
  (*owner's decision, 9/10/2026*): the factory fits nothing there, the
  guide is meant to click on dry, and a wisp behind the breather's valve
  is not worth a joint that is harder to take apart.
- **Tight** (*owner*): the injector seats, the intake itself and the
  hoses at the back.
- **The plug in the hose to the throttle leaked most** — round the
  glove, less once a rag was pushed in behind it. That is the test's own
  seal, not the car; the hose itself the owner judges sound.
- **Also clean** (*owner*, asked): the throttle body, the oil filler,
  the cover joint, the valves, and nothing anywhere at the back.
- **No smoke from the airbox's open outlet** (*owner*), so N112 did not
  pass manifold to vent, unpowered and cold — the route `plan.md` had
  put first for smoke there.

**The second test, the same day, with the old MAF in the hose**
(`plan.md` step 2a; *owner, photographed*:
`photos/smoke-intake-2026-10-09-maf-clamp.jpg`). The 2018 MAF pushed
into the hose as the real one sits, its airbox end closed with a glove
and a rag, so the hose held pressure on the car's own joint.
- **Smoke at the MAF-to-hose joint, under the owner's rubber-lined pipe
  clamp** (*owner*: "it seems to"). **That joint is behind the MAF**: air
  in there is unmetered — the one leak in this whole intake that H3 would
  most want, the kind the ECU learns away (`refuted.md` C19). ⚠ **Not yet certain**: the glove and rag closing
  the MAF's end sit a few centimetres away and leaked the first time, so
  the smoke in the photo can be theirs. The owner fits a narrower
  all-metal clamp and smokes it again; that tells the two apart.
- **The dipstick: nothing**, or practically nothing.
- Nothing anywhere else.

**The third test, the same day, with a new clamp** (*owner*): the
rubber-lined pipe clamp at the MAF end replaced with a narrower
all-metal one, and smoked again — **no smoke anywhere**. Whether the old
joint really leaked stays open: the smoke may have been the plug's, or,
the owner's reading, the old clamp pressed in the wrong place and held
the hose badly. **Either way the joint behind the MAF is now tight cold**,
and the intake as a whole with it.

⚠ **The brake servo was not tested by any of it** (*reasoned*,
9/10/2026): smoke pushed into the manifold closes the servo's check
valve (*general*: it passes only from servo to manifold), so the servo's
diaphragm and seals behind it never saw the smoke. A leaking servo feeds
unmetered air at exactly the idle vacuum. Its line is rigid plastic and
cannot be pinched (*owner*); its tests are the three standard servo
checks (`plan.md` step 3). **9/10/2026, a and b good** (*owner*): the
pedal sank when the engine started, so the servo assists; after
switch-off the first press was light, the second perhaps a little,
then hard, so the check valve and diaphragm hold vacuum for a press or
two. **c** was tried the same evening without a capture: no hiss heard
from the driver's seat with the bonnet open, and no change in the idle
by ear with the pedal held — read again off a capture (`plan.md`).
**10/10/2026, c good off a capture** (`31_step4_drive_z1`, on the cold
idle two minutes after the start): the brake switch is on the bus —
0x1A0 byte 1 bit 3, which toggles exactly at each hold — so the two
holds of 45 s and 44 s are timed to the frame. Engine speed 813 rpm on
the first hold, 813 released, 806 on the second, the warm-up's drift;
no step at any edge; 003's air 4.07 / 3.95 / 3.89 g/s, falling with the
warm-up, not rising with the pedal; 014 counted the same with the pedal
and without (the owner saw it counting with neither foot down). **All
three checks good: the servo is cleared** — tested cold, as decided, so
it is the diaphragm at idle vacuum that is cleared, not a joint that
opens only hot.

⚠ **Cold and stopped, so a joint that opens only hot is not cleared.**
What the result does do: the back of the intake that no spray ever
reached showed nothing, and the one place it did show is the crankcase's
smallest path. Read into the ranked list below.

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

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ~ | ✔ | — | — |

- **Against, 10/10/2026** (S1, *What comes before a dip*): the dips
  come 1.6–3.5 times as often just after the idle governor has trimmed
  the charge as just after it added some. An intermittent contact —
  in the harness, an earth, the coil's feed — does not care about the
  charge, so it cannot make that dependence; it could still be a part
  of the dips, not the reason they follow the trims. The same direction
  as *load helps* (S1), which already counted against this hypothesis.

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
- **1d, done 1/10/2026** (*owner*, at the job, `idle-log.md`, *The valve cover and throttle job*): the four
  leads all measure **about 6 kΩ end to end**, the small differences put
  down to probe contact; every boot clean inside, no oil in any — so the
  oil on 3 and 4's boots seen on 26/9 (S10) stayed on the outside.
  **Plug 4's terminal, seen at the same job** (*owner*, 1/10/2026;
  photographed, `photos/plug-well-cyl4-2026-10-09.jpg`, reported
  9/10/2026): a **black, burnt-looking patch on top of the plug** that
  petrol would not shift. In the photo the terminal post of 4 is darkly
  mottled where the other plug wells' terminals are light and even, and
  the hex carries a dark smudge. On the metal, not on the ceramic. *General*:
  a burnt terminal is what a boot contact that does not grip well leaves
  behind — the spark jumps a small gap at the terminal, pits and blackens
  it, and loses energy for the gap in the cylinder: **an intermittent
  misfire on that one cylinder**, often worse in the wet. The plugs and
  leads were new on 17/9, so it formed within two weeks. The 6 kΩ of 1d
  is the lead end to end, which says nothing about the grip at the plug.
  *Reasoned, not shown:* it fits the dips keeping to one cylinder
  (*Naming the cylinder*) and, since 1 and 4 most likely share a coil
  output (above: period 2 is the coil's two outputs), a fault at plug 4
  would cost cylinder 4 and spare 1 — the shape the pairs fit. The boots
  were pushed home again on 1/10, and the dips kept to one slot after it
  (`25`–`30`), so if this is the cause, reseating did not cure it.
  **The first named candidate for the cylinder** — `plan.md` step 3.5
  names the cylinder before anything is changed.
  **The boots never clicked clearly** (*owner*, 9/10/2026): refitting
  the leads, he has not heard a clear click on the plugs, and has not
  trusted the leads from the start. *General*: a boot latches over the
  plug's terminal — on plugs for VW often a nut screwed on an M4 thread
  — and one that does not latch rests on it and arcs, which is what
  burns a terminal black. **The plugs carry solid terminal posts, no
  screwed-on nut** (*owner*, 9/10/2026, as the plug-well photos show),
  so a loose nut is ruled out and what is left is the grip of the boots
  themselves. Checked at `plan.md` step 2's dry run.
  **The ends of the leads, photographed 1/10/2026** (*owner*,
  `photos/leads-2026-10-01-*.jpg`, sent 9/10/2026), not labelled by
  cylinder. **The plug end** (*owner*, 9/10/2026; told by the outer
  shell) is a **slotted metal sleeve with tabs for a puller**, round a
  rubber insert with the terminal deep inside; **the coil end** is
  rubber, a red sleeve round a rolled terminal held by a wire spring, and
  there the click is clear. *Read off the photos*: one plug end's insert
  (`-plug-end-1`) is darker and crusted where the other five shots are
  clean — the end that sits on a plug, so if it is lead 4's it is the
  other half of plug 4's burnt terminal. The coil ends' springs sit
  differently from end to end, but those ends click. **The owner pulls
  the plug ends by hand, having no puller.** *General*: without one the
  pull tends to go through the cable, and the crimp or resistor inside
  the end is what gives — a loose contact that arcs. Neither photo set
  can be put to a cylinder; the dry run labels them.
  *Corrected 9/10/2026*: this read the rubber end as the plug's, before
  the owner said which is which.
  **The new set, tried dry** (*owner*, 10/10/2026): NGK `RC-VW254` plug
  ends click onto the plugs only with far more force than he had ever
  used on the old ones — so the old ones may never have been fully home.
  It does not tell a worn or ill-fitting end from one never pushed far
  enough; either leaves a contact that arcs.
  **The old leads off, 10/10/2026** (*owner*, photographed and numbered,
  `photos/leads-old-2026-10-10-plug-end-cyl*.jpg`): the coil ends all
  fine; at the plugs **4 the worst**, and every old end came off far more
  easily than the new ones went on. *Read off the photos*: **cylinder 4's
  rubber insert is scored and ragged inside, and its terminal cannot be
  seen**, where in 1, 2 and 3 the insert is smoother and the brass
  terminal plainly in view. *Reasoned:* a terminal sitting further back in
  its boot — pulled up the cable, or never seated — reaches the plug's
  post short, which is a contact that arcs and the burnt terminal of plug
  4 (1/10); it could also be no more than the light. **Lead 4 is the
  named part**, after the fact, by its own end.
  **The old plugs, out on 10/10/2026** (*owner*, photographed by
  cylinder, `photos/plug-old-2026-10-10-cyl*.jpg`; all NGK `BKUR6ET-10`,
  the same type as the new ones):
  - **terminal tops:** only **4** pitted and mottled; 1, 2 and 3 darkened
    but smooth — the other half of lead 4's end;
  - **firing ends:** dry black soot on **1, 3 and 4**, lightest on **2**.
    Soot on three of four is the engine's (*general*: rich running, much
    idling, short trips), not one cylinder's;
  - **plug 1 came out almost without effort, as if never tightened**
    (*owner*). *General*: a loose plug can let combustion gas past its
    seat and runs hot. The compression of 17/9 (12 bar, even) was taken
    **with the plugs out, before these were fitted**, so it does not
    cover this. *Reasoned:* cylinder 1 is cylinder 4's 360° partner — the
    pair the slot pairs pointed at (*The dips keep to one slot*: one
    cylinder high, its partner low) — so between them, lead 4 and plug 1
    are the two single-cylinder faults found, and both are now renewed.
    Which of the two carried the dips, the change cannot say.
  **The drive after the change, 10/10/2026** (S3, *The drive after the
  new leads*): 014 still counts, at about 9/10's rates; the dips no
  longer keep to one slot, on one drive. **So the high-voltage side was
  not the misfires**; it may have been the one-cylinder share of the
  dips, which more drives confirm or not.
- **1d. Engine off: the HT leads.** Each one pushed fully home on its coil
  tower and its plug, the boots dry and uncracked. With the meter on ohms,
  the four leads against each other: one reading far from the others (for
  its length) is the bad one.

  **The leads' order on the coil** (*owner-read off the car, 1/10/2026*):
  **1, 4, 2, 3**, clockwise from the top tower. So 1 and 4 sit side by
  side, as do 2 and 3 — the two pairs the coil fires together in a firing
  order of 1-3-4-2 (*general*), which is the period-2 split under *Naming
  the cylinder*. A lead crossed between the pairs would fire a cylinder
  on its exhaust stroke and could not pass as a rough idle; one swapped
  within a pair still fires on time. Which tower the coil itself calls
  which cylinder is not read here.

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
every before/after comparison (`docs/firmware/fuel-check.md`, *Before and after*).

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
- ~~**An injector click** that slides into the window as injection timing
  moves with speed.~~ **Settled against 9/10/2026** (`refuted.md` B7): with
  all four seated, both S4 and S5 stayed on cylinder 4.

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| — | — | — | ✔ | ✔ | — | — |

**Tests** — not scheduled (*owner's decision, 9/10/2026*: the idle
first, and no link between this window and the misfires has been found):
check G66's torque and connector first; look over everything refitted in
September for a loose bracket, clip or heat shield with the engine held at
~3000 rpm in neutral. **After each, repeat the neutral 026 + 003 holds and
the 020 drive** at the same oil temperature:
`vcds/vcds-step2c-020-026-003.csv` is the before, with
`vcds-neutral-026-003.csv` and `-clamp.csv` behind it.

**Why the events come on tip-ins and not in steady driving**
(*general*: how knock control works on engines of this kind, not read for
this ECU). The knock sensor hears everything — valves, injectors, the
timing gear — so the ECM does not judge loudness. For each cylinder it
learns the normal noise level in that cylinder's window and calls knock
only when the signal **jumps** above it. A steady noise is learned and
ignored; one that **appears suddenly** is not, until the level catches
up. That is S4's pattern: 13 of 16 events on 24/9 on a tip-in **after a
coast or a gearchange**, and again on 9/10. Whatever cylinder 4's window
hears, it is something that rises sharply with load. *Until 9/10/2026
this paragraph argued it for injector 4's click, coupled into the block
while it alone was seated; that is settled against (`refuted.md` B7), and
the argument for it is there and in git.*

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

*4/10/2026 (owner):* the regulator's vacuum hose came off several times
during the intake work of 1–4/10 and never smelled of petrol — no sign
of a diaphragm leaking fuel into the manifold (*general*: that is how
one shows).

The regulator (7/2026) and the pump are the parts of the fuel path not
changed in September, and neither has ever been gauged. (The bad cold start
that once pointed here is closed, S7: it was the old injectors.)
The owner's own remaining candidate is one of the new injectors.

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | — | — |

- **Against, 10/10/2026** (S1, *What comes before a dip*): the dips
  follow the governor's trims of the charge. Rail pressure does not
  move with them, and an intermittent break in the injector harness
  (test 3) does not care about the charge; either could be a part of
  the dips, not the reason they follow the trims.

- **Against, for the idle:** four new injectors and a new filter changed
  nothing in S1; the trims are near zero; a leaking seat adds fuel at idle and
  the trim would show it.
- **Against, 10/10/2026 — the owner's argument, checked:** fuel demand is
  highest at full load, so a weak pump, a restriction or a low regulator
  shows there first — and the held full-throttle pulls reach the torque
  plateau and ~85 kW (`19_postfix_drive_z1`), the motorway at 4500–5000 rpm
  is clean (`refuted.md` C4). A pressure steadily off shows in 032 as the
  injectors' flow changes with it, and 032 is near zero on new injectors
  and a new MAF. The regulator (7/2026, 3 bar) never smelled of petrol at
  its hose, the filter is new, the pump a few years old (*owner*), and
  the cold starts are good since the new injectors, so the rail holds
  pressure standing. What is left — a brief drop the trims average away —
  would show while driving too, and idle is where the least fuel flows.
  **The fuel pressure gauge is not bought** (*owner's decision*,
  10/10/2026); test 1 stays for if 032 ever wanders.

**Tests:**

1. **A fuel pressure gauge on the rail**: pressure at idle with the vacuum
   hose on and off. Settles the regulator in minutes. **3 bar** is printed on
   the regulator (`vehicle-history.md`, *owner-read*, 10/10/2026) — the
   figure to read against; VW's own is not held here. **Needs a gauge
   reading well past 3 bar**: the vacuum gauge on order (*Tools worth
   owning*) stops at 1 kg/cm² and cannot do it.
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
   Beside the injector a bare threaded stud is **one of several on the
   head, and nothing is missing from it** (*owner, 30/9/2026*; this read
   "carries no nut — whether one belongs there is not known").

### H8. Idle air control and the throttle body

**New here, not argued in the log.** Idle speed on this engine is held by the
electronic throttle and by ignition advance (the advance moving 0–9 °CA at
idle in group 003 is that control working). A dirty throttle body or a lost
throttle adaptation makes the governor hunt. *General.* The MAF swap halving
S1 shows that the idle is sensitive to how air is metered and controlled.

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ~ | — | ~ | — | — | — | — |

- **Unchanged, 10/10/2026** (S1, *What comes before a dip*): the
  governor's trims come before the dips, so this part is the trigger,
  but the trims are ordinary — about 1 % of the injection time and
  1.5 % of the torque — and come both ways all the time. A governor
  that hunts would show larger and more frequent ones; these do not
  point at the throttle.

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
is off in the valve cover job**, of both faces.

**At the job, 1/10/2026 — no protrusion, and the joint looks sealed**
(*owner, photographed*): the old throttle's flange face carries the old
gasket's green residue all over and **no raised point at the lower
left**; the owner thinks he most likely levelled it himself while
cleaning in June. **The June gasket came away on its own**, not stuck
to either face; the green on both faces is the residue and imprint of
**the original gasket**, which was torn when it came off in June
(*owner*). *An earlier revision of this paragraph took the green on the
plenum for the June gasket, stuck on and whole all round — the owner
corrected it the same day.* **The June gasket itself is whole**
(photographed): no tear and no gap from the bore to the outside, at the
lower left or anywhere, its bolt rings and the band along the bore
pressed in evenly. The plate and both sides of the bore look clean
— a thin dark line at the plate's edge, no oil film to be seen despite
the oily intake hose ahead of it (H9 test 4) — and the owner judges the
part fine. **So the flange is not a leak this job found**, and the
`plan.md` table's row *"a gap in the old throttle gasket at the
protrusion"* did not happen. The June photograph's point stays recorded
above as what it showed then.

**Behind the throttle, the same day** (*owner, photographed by torch*):
the plenum's mouth is **dry cast aluminium**, light grey, with a darker
smudge at its lowest point — no standing oil, no wet film. The oil seen
in the intake hose (H9 test 4) has not visibly reached the plenum. The
plenum's flange face carries the original gasket's green imprint and
**fine scratch marks towards its right-hand side**. Cleaned with petrol,
**the rule across it shows no light**, and **the scratches stay inside
the face** — none runs from the bore to the outside (*owner*). The dark
spots near its right-hand edge are deposit petrol did not lift, **not
pits** (*owner*). The face is closed as fine.

**The two parts side by side, 2/10/2026** (*owner, by eye and ear on the
bench*) — findings on the old part, not symptoms, so the fit table is
unchanged:

- **The new part clicks as the plate leaves rest**, like a door switch;
  **the old one makes no sound at all.** J338 carries the idle switch F60
  (*What VW's repair manual says*, below), so the click is most likely
  F60 (*reasoned*). The owner reads it as the switch that hands the idle
  over to the electronic idle control and back. Whether the old part's
  F60 still switches is not known; an ohmmeter across the old
  connector's pins, plate at rest against plate lifted, would say.
- **The contact face at the idle stop inside the old part is visibly
  smaller than the new one's, by perhaps 1–2 mm** — possibly worn down.
  *Why it could matter (reasoned, not from VW):* the idle stop is where
  the plate rests and where the switch is told it is at idle, so a worn
  face moves both; the throttle adaptation (098) learns the stops, which
  may hide some of it.

Both point at the throttle (`plan.md` before 4/10/2026, the table *What
points at which repair*; in git), and both are read on the car only once it runs on the new part.

⚠ **What it does to the reading:** the swap changes two things — the
throttle *and* this joint (a new part's clean face, a new gasket). It is
also **why the throttle went back into the valve cover job** (*owner's
decision, 29/9/2026*): the flange is a sealing joint like the others the
job renews, so a fixed idle now names the job, and only the photographs of
this face can speak for the flange. The air-against-angle curve can separate them: a sealed
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
positioner's %), and 054 (G69's range and F60). **054 on the new part,
2/10/2026** (*photographed, engine off*): 5.6° and *volnoběh* at rest,
91.1° and *část. zatíž.* to the floor — inside both figures, F60
switching. The old part was never read in 054; the owner recalls it never
above 85°. **060 zone 2 is the most
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

**Answered for the old part, 29/9/2026** (S13, *The old part, timed*): 098
completed with *ADP OK* inside VW's 10 s, and the next ignition-on ran the
same 20 s routine. **Not a loop.** Whether it is this unit's own check or
every such part's is what the new part says.

**Reading: against H8 at the resolution there is.** A sensor glitch shorter
than the 0.6 s between readings would not be seen; a worn track that made
the ECM chase phantom movement would, and does not show. Left in the file
because cleaning and adapting is cheap, not because anything points here.

**Replaced inside the valve cover job — the owner's decision,
29/9/2026** (`idle-log.md`, *The valve cover and throttle job*). Nothing in the data asks for it; the part
is original, 26 years old, cheap, and sits in the idle air path. First
planned inside the job, split off on 28/9 so that its effect would show
alone, and **put back into the job on 29/9** after the flange photograph
above: the owner accepts that the idle then cannot tell the throttle from
the rest. A new aftermarket part is itself an unknown on the idle's side of
the engine, which is why the old one is kept — refitted for a day, it is
the one way left to name it (`plan.md` before 4/10/2026, *What points at
which repair*; in git). An
idle fixed by neither the job nor anything after it sends the whole of H8
(the three wear routes above included) to `refuted.md`.

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
  cannot tell which; **more air through the MAF after the job** can
  (`plan.md`, session A) — the plate no longer, since the job changes the
  throttle too.
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

**How the plan reads it:** the job changes the throttle, so a moved
curve says the two parts differ, but not whether in the sender or in the
metal; only a look at the plate's physical opening could split that. A
sealed leak is therefore read off the **air and 055**, not off the plate
(`plan.md`, session A). **Group 004 once per test** gives the intake
temperature, so that the new part's own curve is recorded like for like
(`plan.md`). *(Until 29/9 a separate test 1 kept the old throttle so that
the curve could be read across the job; the owner put the throttle into
the job instead.)*

**What the swap is compared on:** the first cold start after it should
show the same plateau height, the same ~95–100 s and a similar plate angle.
A different height or length would be the ECU choosing differently, which
a new J338 should not cause. A sagging speed with the plate high would be
the new part.

### H9. Crankcase ventilation, or the valve cover gasket (S10, and possibly the idle) — closed 4/10/2026

**Closed** (*owner's decision, 4/10/2026*): right about S10 — the cover
gasket was the leak, and it is repaired — and settled against for the
idle, since the misfires outlived the new breather (2/10) and the sealed
cover (4/10). `refuted.md` A15. What is left, the original breather hose
and its connector, belongs to H3 and is inside the smoke test. Kept here
for the record; out of the ranked list.

The crankcase is ventilated into the intake, and blow-by leaves through the
breather hoses. *General* for any engine: **if the breather path is blocked**,
crankcase pressure rises and pushes oil out of the weakest seal — typically
the valve cover gasket — onto whatever is below. **If a breather hose or the
gasket leaks instead**, the crankcase draws in air past the MAF at idle, where
the manifold vacuum is highest: an unmetered leak, H3 by a different door.
Either way one fault can make S10 and reach the idle.

**The concrete door, 1/10/2026.** *This paragraph used to say the
breather might sit on no seal at all (30/9, a quick look); at the job
both seals were found in place (S10, `refuted.md` C14).* The door the job
did find was **the breather's own body** (test 4, below): a patch on it
that the owner read as a past repair. *2/10/2026: the new `32452` carries
the same patch, so it is original (`refuted.md` C15); this paragraph used
to name it as the door.* What is left of this door is the old ring under
the breather (below) and the membrane, which nobody has judged. Either way
the mechanism is this
second branch: at idle the breather holds the crankcase slightly below
atmospheric, so an opening to the outside draws air, which leaves through
the ventilation into the intake **behind the MAF** — unmetered. It is
**test 3's filler-cap-off made smaller**, and that made the idle audibly
slightly worse; the depression is small (test 3 felt no suction, and *The
valve cover gasket and a rough idle* below calls the air route weak), so a
small leak rather than a large one (*reasoned, general*) — which is what
rank 1 in *The idle's candidates* asks for. The fit table below is
unchanged until it is confirmed.

**The old ring under the breather, 2/10/2026** (*owner, photographed
beside a new `100690`*): **visibly larger than the ring the new `32452`
comes with, with pressed-in marks, very soft, and smeared out as if the
rubber had begun to flow — almost liquid in places.** In the photograph
it stands out past the new ring's outside edge all round and carries a
raised step on its face, where the new one is flat sheet (*Claude's
reading*). **On the car it always looked odd** (*owner*): it stuck out
well beyond the breather's base, and not evenly. **And the old breather
sat very loosely in the cover, where the new one with its new ring went
in much more stiffly** (*owner, at the refit, 2/10/2026*) — a seat with
little or no pressure on its ring, which fits a ring that had flowed
out of shape (*reasoned*). Wrong for
the part, or flattened out of shape over the years — not known. *Rubber
that has sat in oil softening and swelling is general, not read for this
part*, and would account for both the size and the softness. A ring that
no longer seals is a door of exactly this kind (*reasoned*) — and with
the patch shown original, the only concrete one the job found here; a finding on a part, not a symptom, so the fit
table stays as it is.

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ~ | — | ~ | — | — | ✘ | — |

*4/10/2026:* **right about S10** — the cover gasket was the leak, and it is
repaired (S10, closed). S11 is now the hiss alone, and it **outlived the
new breather and the new gasket**, so it is no longer this hypothesis's
(✘); S11's smoke was S10's oil, as the first bullet below said. What is
left of H9 for the idle is H3's: an unmetered leak, now at the breather's
hose and connector only, which the smoke of 9/10/2026 found tight cold
(H3).

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
  valve** — after the MAF. *Confirmed on this car by the owner's
  photograph of 26/9/2026.* **No heater on this car** (*owner, the part in
  hand, 1/10/2026*): the hose joins the intake hose through **a plastic
  connector with no electrical connector**, and a thinner hose joins the
  same connector. *This bullet used to say "with the heater `N79` teed
  into it against icing", from the catalogues; the part on the car has no
  wiring, so no heater is fitted here.* **Two thinner hoses** join the same
  connector (*owner, 1/10/2026*): one to the injectors' air shrouds
  (`refuted.md` C9), one to **a second tee right by the head, at the
  intake runners**. That tee (*owner, photographed 1/10/2026*) sits on a
  line that runs **up towards the throttle** and **down under the
  runners, by the owner's reading to the EVAP side**. **The piece up to
  the throttle is a short moulded rubber elbow marked `06A 133 374`**
  (VW/Audi logos, *Germany*; *owner, photographed and confirmed
  2/10/2026*) — **hard with age**, where a new hose of the same kind is
  much more flexible (*owner*). It was replaced at the job by a longer
  plain hose, the new throttle's spigot pointing the other way (`plan.md`
  item 8). *This sentence used to say the tee sat on a rigid pipe marked
  `06A 133 374`; the number is the elbow's, and what the rest of the line
  is made of was not read.* *What the pipe is, and which port on the throttle it
  serves, is not read from any VW document.* **Why it matters**
  (*reasoned*): if its top end takes vacuum from **behind the plate** —
  the throttle's bore carries a nipple on its plenum side — then this
  line runs at full manifold vacuum, and a leak anywhere along it, the
  tee or the thin hose to the breather's connector, is a far stronger
  unmetered leak than anything ahead of the plate. **The pipe is on the throttle's top
  spigot** (*owner*), and the photograph of the old throttle's plenum
  side shows a brass port at the top of the bore **behind the plate** —
  **confirmed by the owner with the part in hand**: the port opens into
  the bore on the engine side of the plate, so **this line runs at
  manifold vacuum**. Its hoses were checked by hand and are fine (*owner,
  1/10/2026*); a smoke test is what would settle it.
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
  mark (`vehicle-history.md`), no whistle reported, the smoke at the back explained as the cover
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
  car that route was thought weak** (*the breather hose was found oily
  inside on 1/10/2026, test 4 below, which weakens this*): the throttle body was inspected in 6/2026 and
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
   the hose or at its end on the intake hose, a split in the hose or at
   its plastic connector, the separator in `06A 103 465` intact. The part costs a few
   tens of euros, so replacing it on suspicion is a fair test.

   **Partial result, 1/10/2026** (*owner-found and photographed*, during
   the valve cover job, `idle-log.md`, *The valve cover and throttle job*): **the hose from the breather to the intake ahead of
   the throttle is oily inside** — a finger put into it came out covered.
   The photograph shows the bore dark and wet, with a light-grey crusty
   deposit on one side of the inner lip. The owner had looked at the
   breather side in 6/2026 and is not sure that look was thorough, so
   **how long the oil has been there is not known**.

   **What it does and does not say** (*general, reasoned*): oil in this
   hose is oil mist that the breather's separator let through, so it
   speaks to **the separator and to the amount of blow-by** — the
   blocked-or-overloaded branch of H9 — and it means the mist reaches
   the throttle's bore (the route under *What the web says*, which is
   no longer only three months' worth). **It does not by itself name
   the membrane**: on this layout a torn membrane admits outside air
   (*Why a healthy breather adds no unmetered air*), which a hose wet
   with oil neither shows nor rules out — and some oil film in a
   breather hose is common on a healthy engine too, so the amount is
   the question, which a photograph cannot grade. The membrane is
   judged on the old part out of the car (`idle-log.md`, *The valve cover and throttle job*); the new
   breather replaces it either way. The fit table is unchanged.

   **The big intake hose too, 1/10/2026** (*owner-found and
   photographed*): the oil has gone on past the breather hose's junction
   — **the large connector from the MAF to the throttle**, which the
   breather hose and a thinner one join through a plastic connector, **is
   oily inside**, taken off
   the car whole; a wet film along the bottom of the bore. **The hose
   itself is sound** (*owner, by hand*): what the photograph showed at
   its clamped end as a possible split was a small frayed sliver of the
   material turned inwards, which tore off like a loose thread — the
   end only frays. *An earlier revision of this paragraph read it as
   possibly a split through the wall, an opening behind the MAF; the
   owner's hands corrected it the same day.* Fine on every side.

   **The old breather itself, out of the car, 1/10/2026** (*owner-found,
   photographed*):
   - **a foreign patch on the body** — on one side, where the body
     meets the hose spigot, **something black looks melted or stuck on,
     like a tape** (*owner's reading*). He reads it as not original: it
     sits **slightly askew** rather than square to the part, and its edge
     is **lifting a little** — but a fingernail cannot lift it. At its
     corner the photograph shows a whitish, branching mark; *an earlier
     revision of this paragraph read that mark as a crack in the body,
     before the owner described the patch*. A patch there would most
     plausibly cover an earlier breach (*reasoned, not seen under it*);
   - **the seam of the ring round the body's middle** — the joint of the
     two halves, where a membrane would sit (*general*) — looks lifted in
     places in the photographs, not checked by hand;
   - **oily in every direction**, inside and out; a finger does not reach
     the membrane.

   **What it says** (*reasoned*): the body is on the crankcase side of
   the ventilation, slightly below atmospheric at idle. **A breach under a
   lifting patch, or an open seam, is an opening to the outside behind
   the MAF** — the concrete door above. Not proven: nobody has seen under
   the patch, and it does hold. *2/10/2026: the patch is original — the
   new part carries the same one (`refuted.md` C15) — so it is no sign of
   an earlier breach.* **The owner also reads the oil as the
   membrane passing it**; the oil reaches the hose by the valve's normal
   path — blow-by and its mist go *through* the breather — so oil past it
   speaks to the separator, not to the membrane (*reasoned*, above). The
   membrane stays unjudged; the new breather (`32452`) replaces it either
   way. **The fit table is unchanged.** *This used to end "but this is
   the strongest sign for H9's air branch found so far"; with the patch
   original, that sign is now the old ring under the breather.*
5. **After the repair**, `IdleHealth` at a matched oil temperature against the
   current band: the same rule as H2 — a clear improvement means this was
   underrated.

### H11. Both lambda probes shifted alike, so the mixture is off and nothing sees it

*Added 10/10/2026 at the owner's request, as a weak hypothesis written
down so that it is not argued again from the start.* Both probes are the
one part of the mixture control that has not been changed: **10/2017,
~27,600 km** (`vehicle-history.md`; both, *the owner's decision to keep
the record as it stands*, 10/10/2026).

**What it needs.** The two-loop control (SSP 233 p. 16, as in H2) holds
the front probe at its switching point and lets the rear probe move that
point slowly. One probe lying is caught by the other; **only both lying
in the same direction is not.** For a mixture that is really rich to pass
unseen, both have to read *leaner* than the truth: the front makes the
ECU add fuel, the rear then sees its target and does not take it back.
(Both reading richer would hide a lean mixture the same way.) An aged
narrowband probe can shift where it switches, and one that answers
lean-to-rich more slowly than rich-to-lean moves the mean mixture in the
same way (*general*).

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | — | — |

- **Against, mildly, 10/10/2026** (S1, *What comes before a dip*):
  what comes before a dip is less charge at the same mixture, not a
  leaner mixture; a shift of the probes moves the mixture.

S1 and S3 only as a background on all four cylinders — **a few per cent
off λ = 1 does not misfire on its own** (*general*, as under H2); S2 for
surplus fuel burning in the exhaust. S4 and S5 are one cylinder's; S11
and S15 are sounds a probe does not make.

- **For:** nine years, and a misfiring idle with a burned-through
  converter behind them (`vehicle-history.md`). **None of the probe tests
  sees a shift**: 034 times the front probe's period, 046 compares
  amplitudes, 036/037 check the rear for presence and response (`vcds.md`)
  — all OK on 24/9 (`refuted.md` C5), and all blind to where the
  switching point sits. The front probe's even, full swing at idle
  (`refuted.md` C5) rules out a lazy probe, not a shifted one. Dry soot on
  plugs 1, 3 and 4 (H4, 1d) fits a rich mixture — and fits idling, short
  trips and misfires as well. In the long Polish AQY thread (t=522030,
  2016–2017) two posters reported the vibration gone with a **new lambda
  probe**, one naming an original Bosch — but nothing says theirs were
  merely shifted rather than dead (*forum*). **10/10: the dips no longer keep to one slot**
  on one drive (S3), which gives back a little to causes acting on all four.
- **The rear probe's 0.665–0.725 V at a hot idle does not decide it**
  either way: that is where a narrowband probe behind a working converter
  usually sits (*general*), and a shifted rear probe reads the same.
- **Against — the trims, read as an independent sum.** The ECU meters fuel
  from the MAF and the injectors' flow, and the probes only correct it. A
  steady error in the probes therefore shows in 032 + 033 as a correction
  of its own size, **less whatever error the MAF and the injectors carry**.
  Read: 032 −0.8 / +2.3 % (4/10), 033's median −0.8 % at idle (B1) — on a
  **new MAF and new injectors** (9/2026). A hidden error of five per cent
  would need the two new parts to be wrong by five per cent the other way,
  just enough to cancel it. Their tolerances are not held here, so this
  bounds the shift to a few per cent rather than excluding it.
- **Against — the sign.** Hiding a rich mixture means the ECU adding fuel:
  a positive correction. The idle cell has read negative every time on the
  new MAF (−3.1 %, −0.8 %), the ECU taking fuel out.
- **Against, as the misfires' cause:** a shift small enough to hide in the
  trims is too small to misfire, and one large enough to misfire could not
  hide in them.

**Tests:**

1. **A four-gas analyser** — the emissions station's, the one instrument
   on the list that measures the mixture without the car's probes: CO, HC,
   O₂ and the λ computed from them, at a warm idle and at ~2500 rpm. λ
   close to 1 with low CO closes this; λ clearly below 1 with the trims
   near zero opens it. *Not in `plan.md`.*
2. **A wideband sensor as a reference**, if the blanked-off boss on the
   new front pipe (`vehicle-history.md`) turns out to sit ahead of the
   converter — where it sits is not recorded. Its λ against the ECU's
   switching, at idle and under load.
3. If either finds a shift: new probes, front first, and 032 read again on
   settled adaptations.

### H12. Driveline play read as misfires — gearbox input shaft, clutch, flywheel, crank pulley

*Added 10/10/2026 at the owner's request, from a lead another assistant
raised; ranked last.* The idea: the dips and 014 are not misfires but
mechanical play in what the crank drives, felt at an unloaded idle where
almost nothing resists the crank, and taken up under load. 014 reads
crank-segment times through G28 (`vcds.md`), so a jolt there would be
counted as readily as a missed firing.

| S1 | S2 | S3 | S4 | S5 | S11 | S15 |
|---|---|---|---|---|---|---|
| ~ | ✘ | ~ | ~ | ~ | — | — |

S1 and S3 as a counterfeit of both; S4 and S5 because a mechanical
knock in cylinder 4's window could read as knock (S5 already fits a
resonance better than a single part, H1); S2 not — a puff is unburnt
charge, which play does not make.

- **For:** load calms the idle (S1, 26/9), and play is taken up under
  load (the owner's relay of the argument); the dips come just after the
  governor has lowered the torque (S1, *What comes before a dip*), which
  is when play would show.
- **Against:** the MAF swap halved the dips (`refuted.md` A11) and the
  learned idle air decides when 014 counts (`refuted.md` C19) — neither
  touches a flywheel; the dips kept to one firing slot, 720°, on the
  captures to 9/10 (*The dips keep to one slot*), where anything turning
  with the crank repeats every 360° and the alternator at a ratio that is
  not whole — weaker since 10/10, when that pattern went; the old
  converter burned through, which takes unburnt fuel; the injector cuts
  stored codes for exactly the cut cylinders and no other, so the
  detection works (*Naming the cylinder*). **Compression does not bear on
  it** either way: a cranking test sees neither play nor a flywheel.
  Whether this car has a dual-mass flywheel at all is **not recorded**.

**Tests:**

1. **The clutch minutes** (`plan.md` step 3, item 1, cold and warm): pedal down takes
   the gearbox input shaft and the clutch disc out of the engine's load.
   Dips and `IdleHealth` the same either way → not that side; clearly
   calmer with the pedal down → it is a lead. The flywheel and the pulley
   turn either way and are not separated by it.
2. **The crank pulley's damper, by eye, engine off**: the rubber ring
   between its inner and outer metal rings cracked, bulging or the outer
   ring walking out of line (*general*). Free.
3. What the flywheel is, read off the parts catalogue by VIN, if test 1
   or 2 points here.

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

**Searched again 10/10/2026** (*the owner's request*), German, Czech and
English, for an AQY or a sister 2.0 8V with an idle-only misfire that
ends in a fix. **Nothing new on this engine.** What came back:
Ross-Tech's list for 16684/P0300 (intake leaks, fuel supply, injectors,
plugs and leads, coils, a stuck EGR valve, G40, G28, carbon, the
valvetrain) — everything on it but the valvetrain, carbon and G28 has
been through this car, and this engine has no EGR valve;
mymotorlist.com naming the idle controller and the crank sensor as the
AQY's usual electrical faults; the Opel case under H1. **G28** — the
crank sensor, which both 014 and the bus's engine speed are read from —
would give artefacts at 360°, not the 720° runs above, and a failing one
usually sets a code (*general*); not a hypothesis on that alone.
**The pkw-forum.de bucket-tappet thread (H1) is still the only AQY
report found with a named cause in the valvetrain.**

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

   ⚠ **What it can see here, worked out 29/9/2026** (*the owner offered to
   measure the cylinders after a drive with the new IR thermometer*):
   **a dead or badly weak cylinder, not this fault.** At 800 rpm each
   cylinder fires about 400 times a minute; the dips come at 5–11 a minute
   for the **whole** engine (S1), and a typical one is half a stroke. Even
   all of them in one cylinder is **1–3 % of its combustions** — a runner
   that much cooler sits inside the ordinary spread between four healthy
   runners (*general*), so a reading that shows nothing says nothing.
   **Around each plug or injector on the head is worse still**, and is not
   worth taking: the head is one aluminium casting on one coolant circuit,
   which smears any difference between cylinders, the intake side is
   cooled by the fuel, and bare cast aluminium has an emissivity far
   below the thermometer's lowest grade of 0.75 (*general*), so it reads
   low and reflects its surroundings. *Decided:* the runners only if they
   can be reached without dismantling anything, as a cheap check for a
   gross fault; the head not at all.
2. **Cylinder balance by unplugging one injector at a time**, at a warm idle,
   for a few seconds each, watching engine speed. The cylinder whose removal
   drops the speed least is the weakest. ⚠ It sends unburnt air, not fuel,
   through the converter, but it does set a fault code to clear afterwards;
   keep each cut short.
   **Scheduled, 9/10/2026** (*owner's decision*): `plan.md` step 3.5 —
   cylinders 1 and 4 only, which name all four while they are out, on up
   to three days, read by name off the capture (*The dips keep to one
   slot*, below). **Day 1, 10/10/2026** (`31`, after the new leads):
   1, 4, 4, 1, cuts of 47–73 s. Dips by name 1: 0, 2: 7, 3: 11, 4: 2 —
   **no cylinder stands out** (p = 0.28); the air with 1 out and with 4
   out alike (3.52 / 3.58 against 3.46 / 3.58 g/s), so neither is a
   steadily weak cylinder. Twenty dips in all, so only a cylinder
   carrying most of them could have been found. **No second day for
   now** (*decided 10/10/2026*): the dips stopped keeping to one slot on
   the same drive (below), which was the reason to name one.
   **The fault memory after the cuts** (*owner's photograph*,
   `photos/vcds-faults-2026-10-10-after-cuts.jpg`; cleared since): five
   codes, all the test's own — 17645/P1237 and 17648/P1240, injectors 1
   (N30) and 4 (N34) *open circuit, sporadic*, the connectors pulled;
   16685/P0301 and 16688/P0304, misfire on 1 and 4; 16684/P0300,
   multiple. *Reasoned:* **the ECU named the two cut cylinders and no
   other** — so its per-cylinder detection names cylinders correctly on
   this car, and **no P0302 or P0303** means neither 2 nor 3 crossed the
   2 % store threshold (`vcds.md`, *What VW says*) that day. P0300 is
   the cuts' too, or cannot be told from them. Nothing else was stored.
3. **Plug reading after a few hundred km on the new plugs**, with the
   cylinder of each plug recorded this time. The old ones were not labelled:
   one was worst, and which cylinder it came from is not known.

### The dips keep to one slot — 9/10/2026

*Asked by the owner: has a single weaker cylinder ever been looked for?*
It had — as slot **means** (`refuted.md` A5), which show no outlier. A
cylinder that stumbles on 1–3 % of its strokes moves its mean by about half
an rpm, under the ordinary 2 rpm spread between slots, so means cannot see
it. **The dips are events, and the events keep to one slot.**

**The method** (`tools/cutscan.py --pairs`). Within a run the cylinder
phase is intact, so two dips in one run either fall on the same slot or
not; by chance a quarter of pairs would. Each stroke is judged against its
own slot's neighbours, so a slot that merely sits low cannot make dips of
its own, and pairs closer than 16 strokes are left out as one stumble and
its recovery.

**The result**, every idle capture from `09` to `30`: **256 of 720 pairs
on the same slot — 36 % against 25 %, p ≈ 2×10⁻¹⁰.** By log it runs 31–46 %
except the short ones and `26` (3/10, the cover open, 9 % of 23 pairs);
44 % before the MAF, 33 % on 9/10. Tested against itself: dips planted on
all four alike give 20–34 %, all on one cylinder 96 %.

**What it is, and what it is not:**
- **Not a recovery echo**: the same-slot pairs are spread over lags of 16
  to 50 strokes and more, and the result holds beyond 40.
- **Not a slot offset**: each slot is judged against itself; with a
  neighbour baseline instead, the figure rises to 50 %, which is the
  offset's share.
- **Not the crank wheel**: a tooth error repeats once a revolution and
  would favour slots two apart; those are the *rarest* (lag ≡ 2 mod 4 in
  11–16 % of pairs).
- **How it is shared** (*a model fit, not unique*): lag 0 / 1 / 2 / 3 mod 4
  at roughly 35 / 24 / 14 / 25 % fits **one cylinder carrying about 45 %
  of the dips with its 360° partner carrying almost none** — and fits two
  cylinders neighbouring in the firing order at about 40 % each just as
  well. Either way it is not the whole engine alike.
- **Which cylinder, the bus cannot say**: the phase is lost every few
  seconds. `plan.md` step 3.5 names it, by cutting 1 and 4.

*Reasoned:* it fits what acts on one cylinder — its runner (H3), its valves
(H1), its plug, lead or coil tower (H4's high-voltage side), its injector —
and argues against the dips coming from what acts on all four alike (H2's
air at the shared probe, H7, H8, H0, H4's supply).

**10/10/2026, after the new plugs and leads** (`31`): 10 of 39 pairs on
the same slot, 26 %, outside the injector cuts — chance — and fewer
pairs than any drive of its length. One drive cannot tell 26 % from
33 %; if the next two or three stay near a quarter, the one-cylinder
share went with lead 4 or plug 1 (H4, 1d) or the intake gasket changed
the same day, and the misfires 014 still counts (S3) are the engine's
as a whole. ⚠ `cutscan.py --pairs` reads the whole capture: on a
capture with cuts in it the cut minutes must be left out by hand, or
the dead slot makes the pairs (41 % on `31` with them in).

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
stands; what moved is recorded in the rows. Re-read 29/9/2026 when the
throttle went into the job: no symptom changed, the order stands, rows 1
and 5 say how each is now settled. Re-read 2/10/2026 when S13 closed: it
was H8's alone, so only row 5 changes; the order stands. **Re-read 4/10/2026 after session A on the sealed
engine** (S3, *Session A after step 1b*): no symptom added or closed, but
the order changes — 014 at zero at both warm stops and back only after a
hard drive is a fault that needs heat from load. **H2 moves to the top**
(with S11's hiss), H4 and H7 up behind it as the fallbacks if B3's 033
does not point at the probe — both fit the pattern in form only (the rows
say why) — and H3/H9 down: the leak signature did not move. H8's part is new and the
pattern does not follow it. What separates the top three is `plan.md`
session B's B3.* *Re-read 4/10/2026 evening, after session B: no symptom
added or closed. **H10 goes in at the top** — the counts followed 055's
learned value through both sessions, and B counted on a cold idle — and
**H3/H9 come back up behind it**, as the likeliest reason the ECU learns
idle air away; **H2 drops**: at B1 033 did not correct toward rich, and
counts at a cold manifold do not need it. H8 rises with H3 for the same
reason. The order is settled by `plan.md` steps 2a–2c.* *Re-read 4/10/2026,
late, when S8 and S10 closed and S11 lost its smoke: S10 was in no row's
reasoning except as H9's oil, which the repair answered; the order stands.
Re-read again when S9 and S12 closed: S12 was a supporting point for H3
("also fits S12") and nothing more, S9 was in no row; the order stands.
H9 closed the same evening (`refuted.md` A15); row 2 is H3 alone, with
the breather hose folded into it.* *Re-read 4/10/2026 when S14 was
added: it fits H3 and H2 alike and leaves the order as it stands; it
would lift H7 only if its test finds bangs with the cut long past.*
*Re-read 9/10/2026 when S6 closed and after the intake smoke test: S6
was in no row. The smoke found the back of the intake tight cold and
one leak, at the dipstick guide's seat — a crankcase path, the smallest
of H3's. **Then, the same day, the rest came in clean** — the airbox
outlet included — and the seat was put right to a faint wisp. So H3 has
lost its cold evidence: everything left of it is a joint that opens only
hot, which is H2's argument too, and H2 has not been looked at at all.
**H2 moves to 2, H3 to 3.** 2b still reads 055 on the reseated
dipstick, and the exhaust smoke test is H2's first look.* *Then the
second test showed smoke at the MAF-to-hose clamp, not yet told apart
from the test's own plug. **The order is held until the new clamp is
smoked**: a leak there confirmed puts H3 back to 2 — unmetered air
right behind the MAF, the kind H10 says the ECU learns away; clean puts
it where it is.* *Then the new clamp smoked clean, and whether the old
one leaked cannot now be told. **The order stands — H2 at 2, H3 at 3**:
the intake is tight cold everywhere, and the exhaust smoke test said
nothing either way. **2b now decides between them**: 055 rising and 014
quiet on the sealed intake points at what was sealed today (H3, the
dipstick or the MAF joint); no change points at H2's warm test.*
*Re-read 9/10/2026 after 2b: no symptom added or closed. **No change** —
014 counting at every stop, the learned value never above −1.07, 003's
air and plate as on 4/10, 032's idle cell more negative. So neither the
dipstick nor the MAF joint was the air H10 is learning away. **The order
stands, H2 at 2 and H3 at 3**, with H3 weaker by one more test: tight
cold, and now no warm sign of the two places it found. H2's warm test is
`plan.md` step 3, behind the vacuum gauge, which splits H1, H3 and H7
once bought.* *Re-read 9/10/2026 when S15 was added: it fits H2 and no
other row (H0 against). **H2 stays at 2 behind H10 but gains a symptom
of its own** — a leak heard rather than inferred — **and its test moves
to the front of `plan.md` step 3**: it costs nothing and needs no
purchase, while the vacuum gauge is not yet bought.* *Re-read 9/10/2026
when H10 closed at the owner's decision (`refuted.md` C19): no symptom
added or closed. **H10 leaves the list** — it was never a fault, only
the explanation of when 014 counts, and it ranked first for that. **H2
moves to 1, H3 to 2**, the rest up one. The question H10 left — why the
ECU learns air away — is H3's and H8's, and their rows already carry
it.* *Re-read 9/10/2026 when the temperature profile was corrected
(S1, *Temperature matters*): no symptom added or closed. S1 is roughest
cold, not mid-temperature, so H2 loses one argument against it and gains
none for it; H1 keeps its against in a new form (never worst hot). **The
order stands.*** *Re-read 9/10/2026 after the search on 014 (`vcds.md`, *What the
number is*; `refuted.md` C19): no symptom added or closed. The 4/10
zeros at the warm stops, counted against H0 and H1, came on fresh
adaptations and are withdrawn from both rows; the empty fault memory is
explained by the 2 % threshold and fits H0 and a real fault alike. **H0
stands stronger than it did, the order stands**: H0's test 1, a healthy
AQY's 014, is still the one reading that decides it.* *Re-read 9/10/2026 when the dips were found to keep to one slot (*Naming
the cylinder*): no symptom added or closed. **What acts on one cylinder
gains; what acts on all four alike loses as the dips' cause.** H3 to 1 (a
leak at one runner), H2 to 2 — it keeps S2, S11 and S15, which are its
own, but air at the shared probe cannot pick a cylinder —, H1 from 7 to
3, H4 stays 4 for its high-voltage side, H7 5, H8 from 3 to 6, H0 7, the
belt 8. `plan.md` step 3.5 names the cylinder; until it has, the order is
a judgement.* *Re-read 9/10/2026 after plug 4's terminal, the plug-end
boots and the photographed lead ends (H4, 1d): no symptom added or
closed. **H4 to 1** — its high-voltage side now has a part to point at
on one cylinder, where H3 and H1 have none; the rest down one. The
repair is the owner's (`plan.md` step 3.3), and the drive after it reads
it.* *Re-read 10/10/2026 after the new plugs and leads, the servo, one day of
cuts, and S14 closed: S14 was a supporting point for H3 and H2 (and ~ for
H1, H4, H7) and decided no row's place. What moves the order is the drive:
**014 counted as before on new leads, so H4's high-voltage side is not the
misfires — H4 from 1 to 6**; what is left of it is the coil (6/2026) and
its feed. The dips at a quarter on one slot (one drive) take back, for
now, half of what *The dips keep to one slot* gave to one-cylinder causes:
**H7 rises to 3**, acting on all four alike, and **H0 to 5** — every part
in the fuel and ignition path is new and 014 still counts, with nothing
else wrong that the owner can find; 014's 12–96 against VW's 0–5 keeps it
off the top. **H2 to 1**: S15 is still heard and its test is free and
next, though S2 and S11 went quiet and nothing ticks or smells. **H3 to
2**: the intake is tight cold, the gasket new, the servo cleared, so only
a joint that opens hot is left, which the spray test is for. H1 4 (no
ticking, against), H8 7, the belt 8.* *Then the spray test was struck out (*owner's decision*, 10/10/2026)
on the owner's argument: a joint that opens only hot runs against S1 —
roughest cold, calmest hot — and a leak present cold is the smoke's,
which found the intake tight on 9/10. **H3 drops behind H7, to 3**: what
is left of it is the gasket renewed on 10/10.* *No smoke for it either
(*owner's decision*, 10/10/2026): the gasket is the same part fitted the
same way for the third time, and nothing moved that a new leak would
move — 003's air at a warm idle 3.08 g/s against 3.12, 055's learned
value where it was, 014 at 9/10's rates. That reading is the test, and
it is clean; H3 keeps its place at 3 with no test of its own left
short of the vacuum gauge.* *Re-read 10/10/2026 when **H11** was
added (both probes shifted alike, at the owner's request): no symptom
added or closed. **It goes in last, at 9** — the trims on a new MAF and new
injectors bound it to a few per cent, the wrong sign for a hidden rich
mixture, and too little to misfire; the order above it stands.*
*Re-read 10/10/2026 on the owner's argument against H7 (H7, *Against,
10/10*): no symptom added or closed. Low rail pressure would show at full
load first, where the engine is well, and a steady error would show in
032, which is near zero; **H7 from 2 to 5**, behind H1 and H0, and its
gauge is not bought. **H3 to 2, H1 to 3, H0 to 4.***
*Re-read 10/10/2026 after the idles were gone through again (S1, *What
comes before a dip*): no symptom added or closed. The dips come when the
ECU has just trimmed the charge, which H1 and H3 fit alike. **The order
stands.** (It moved H1 to 2 for an hour, on "short runs on one
cylinder", which the lags did not bear out.) The vacuum gauge, next,
reads both.*
*Re-read 10/10/2026 for what the same finding takes from the others
(*the owner's question*): a fault that does not care about the charge
cannot make the dips follow the governor's trims, so **H4** and the
harness half of **H7** are weaker as the cause, though not out as a
part; **H2** and **H11**, which act on the mixture ratio, a little
weaker; **H8** unchanged. No symptom added or closed, and **the order
stands** — H7 and H4 already sit at 5 and 6.*
*Re-read 10/10/2026 when S6 reopened: no column moves (it was never
one). **The order stands**; H2's test waits on the joint being tight,
since a leak behind the converter vents the tailpipe test and its noise
drowns S15 (`plan.md` step 3).*
*Re-read 10/10/2026 when **H12** was added (driveline play, at the
owner's request): no symptom added or closed. **It goes in last, at
10**: its two points for are shared with H1 and H3, and four of the
measurements against it are things play cannot do. The clutch minutes
are free and on a capture already planned.*

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| 1 | **H2 — an exhaust leak ahead of the probe** | explains the puff and possibly S11's hiss; the zone is now only the **original manifold, its gasket to the head and the probe boss** — the new flange is behind the probe (28/9), and the puff is older than the 10/9 exhaust work (S2). Against: air outside the cylinder does not stop it firing **4/10: the hiss stayed after 1b, from the back (S11), and 014 came back only after a hard drive — heat from load, which opens a crack or a gasket; the owner's lead.** Still against: it has to act through the lambda control, which B3's 033 shows **4/10 evening, against:** at B1 033's median was −0.8 %, not the positive correction air at the probe would force, and B counted on a cold idle **9/10, against it as the dips' cause: they keep to one slot, and air at the shared probe acts on all four alike** — its sounds (S2, S11, S15) are its own either way | the owner's tailpipe test, and a new manifold if it leaks there (`plan.md` step 3, *owner's decision, 3/10*) |
| 2 | **H3 — a small unmetered leak** (with what is left of H9, closed 4/10: the breather's original hose and connector): ~~three injectors not fully home since 23/9~~ (all four seated 1/10, `idle-log.md`; H3, *The injector seats*), and at the back the plenum and its upper gasket, the brake-servo line, the old secondary-air vacuum line **and N112, which vents into the airbox ahead of the MAF** (8/10, `plan.md` step 2a), the breather hose; **the dipstick tube, loose with its bracket missing** (4/10, a crankcase path; **refitted 9/10; the only place smoke came out on 9/10, at the guide's seat, put right to a faint wisp the same day**); **and the throttle's flange**, where a hard protrusion on the old face may have kept the June gasket off (H8, 28/9) | the only candidate that predicts *load helps*; the back was never sprayed; S11's hiss; a leak at the plenum feeds all four, as A5 wants; **also fits S12**, a lean tip-in. Against: trim −3.1 %; VW's own leak signs — idle air 3.1–3.5 g/s against 2.0–5.0, 055's learnt value −0.73 against ±1.50 — rule out a large leak, not a small one (28/9) **4/10, against:** the warm leak signature did not move with the hole sealed, and a leak does not wait for a hard drive (S3, *Session A after step 1b*) **4/10 evening, for:** an unmetered leak is what makes an ECU learn idle air away — the likeliest reason the ECU learns air away (H10, closed 9/10, `refuted.md` C19) **9/10, against: the intake smoked clean cold, the airbox outlet (N112) included** **9/10, for: the dips keep to one slot** (*The dips keep to one slot*) — a leak at one runner acts on one cylinder | the valve cover job itself, which replaces the upper plenum gasket, the breather **and the throttle with its flange gasket** (29/9) — an improvement afterwards answers it; now **the smoke test of the intake**, next (`plan.md` step 2a, *owner's decision, 4/10*) |
| 3 | **H1 — a lifter or valve** | the one cause a forum has named on an AQY (a sticking bucket tappet); compression cannot see it. Against: never worst hot (S1, S3, re-read 9/10); A5 ~~**4/10, against:** zero at both warm stops~~ *(withdrawn 9/10: fresh adaptations, `refuted.md` C19)* **9/10, for: the dips keep to one slot** **10/10, for, weakly: the dips come just after the ECU trims the charge — as H3's do (S1, *What comes before a dip*)** | a **vacuum gauge** at idle (below), the stethoscope, a warm leak-down |
| 4 | **H0 — normal for this engine** | any engine idles least steadily at its lightest load; nothing has ever been compared. Against: 014 reads 12–120 against VW's 0–5 **4/10, against:** ~~zero at both warm stops is not what a normal-for-the-engine idle does on a counter that read 10–20 a minute there~~ *withdrawn 9/10: those zeros came on fresh adaptations (`refuted.md` C19)* **9/10, against: the dips keep to one slot rather than spreading over four alike** — weakly: nobody knows how a healthy AQY shares them | a healthy AQY recorded (H0 test 1) |
| 5 | **H7 — rail pressure** | the regulator and pump never gauged; mixture sensitivity. Against: trims near zero **4/10: the pattern fits only in form** — fuel heat-soaked at the rail after a hard drive; against, the return-flow rail keeps fuel moving, heat soak is a hot-*restart* effect, and the coolant read the same at A3's zero **9/10, against: rail pressure acts on all four alike, and the dips keep to one slot** **10/10, against (the owner's argument): low pressure shows at full load first, where the engine is well, and a steady error shows in 032, near zero** | a fuel pressure gauge — **not bought** (*owner*, 10/10) |
| 6 | **H4 — the electrical feed to the spark** | harness 26 years old. Against: better with loads on, when the supply sags 1.25 V **4/10: the pattern fits only in form** — a coil that breaks down hot is the textbook case, but **the coil is from 6/2026**, and the 3/10 oil sat **only on the outside of its plastic and on the outsides of the leads of 3 and 4, wiped dry** (*owner*, 4/10/2026) **9/10: the dips keep to one slot — for the high-voltage side of one lead or tower (test 1e), against the supply side** **9/10, for — the first named part: plug 4's terminal burnt black by 1/10, the plug-end boots never click, one plug end crusted, the owner pulls them by hand (1d)** | **new plugs and leads, VW originals** (*owner's decision, 9/10*, `plan.md` step 3.3), and the drive after: the dips back to a quarter of pairs on one slot → it was here **10/10, done: a quarter (26 %) on the first drive, but 014 counting as before — so not the misfires; the one-cylinder share of the dips, if two or three more drives hold** |
| 7 | **H8 — throttle body and idle control** | original part, all four cylinders. Against: the dip is one firing, not a hunting loop; found clean in 6/2026; **the idle angle in every VCDS log is steady and the misfires do not move with it** (27/9) **4/10 evening:** a new throttle passing more at rest than the ECU's model would also make it learn air away (`refuted.md` C19) **9/10, against: the throttle feeds all four alike, and the dips keep to one slot** | **replaced inside the valve cover job** (owner's decision, 29/9, reversing 28/9's separate step; `idle-log.md`, *The valve cover and throttle job*), so its effect no longer shows alone — only the kept old part, refitted for a day, can name it. **S13** (its routine at every ignition-on) now sits here too, most likely the unit's normal behaviour by owners' reports; **the old part timed at 20 s before and after a completed 098** (29/9), so not an unfinished adaptation — **and the new part the same, 2/10: S13 closed, nothing left of it for H8** |
| 8 | **the timing belt a tooth out** | belt from 10/2017. Against: even compression, the torque plateau is reached | the marks (VW's manual), **not done in the valve cover job** — owner's decision, 28/9 |
| 9 | **H11 — both lambda probes shifted alike** | the only part of the mixture control not changed, 10/2017; no probe test sees a shift; soot on three plugs. Against: 032 + 033 near zero on a new MAF and new injectors bounds it to a few per cent, and with the wrong sign — negative, the ECU taking fuel out; a few per cent does not misfire | a **four-gas analyser** at the emissions station (H11 test 1) |
| 10 | **H12 — driveline play read as misfires** | load calms the idle, and the dips follow torque trims down, both of which play would also do. Against: the MAF swap and the learned idle air move it, which play would not; the 720° slot pattern (to 9/10); a burned-through converter; the cut test's exact codes | the **clutch minutes** (`plan.md` item 1), the crank pulley's damper by eye |

**Tools worth owning for this, cheapest first** (*general*; prices not
recorded here, since they move):

- **A vacuum gauge on the manifold at a warm idle** (*ordered by the
  owner 10/10/2026, due the following week*: MAR-POL `M57673`, a fuel-pump
  and vacuum tester with hoses and adapters, 0–1 kg/cm² on the pressure
  side by a retailer's listing — its vacuum scale to be checked on the
  dial when it arrives; **not a rail-pressure gauge**, H7 test 1) — the cheapest
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
  intake as refitted. **The crankcase is part of what it tests**, though
  only indirectly: the breather vents it into the duct ahead of the
  throttle, behind the MAF, at a slight depression — too slight for test
  3 to feel as suction, but the idle got audibly worse with the filler
  cap off (H9). So a leak at the cover joint or at the breather's seat is
  a small unmetered leak of its own, and the smoke reaches both through
  the breather hose; **smoke at the filler cap or the dipstick is a leak
  of the same kind** — the crankcase not sealed there — and is judged by
  amount (*corrected 4/10/2026*: this read "is that path, not a leak").
  (*Corrected 30/9/2026*: this read "the valve cover
  gasket itself is not an intake joint: the crankcase sits at
  atmospheric".)
  **Smoke rather than a pressure- or vacuum-decay test of the intake**
  (*general*): a sealed intake is never sealed — the throttle plate, the
  open inlet valves and the breather all pass air — so a gauge that falls
  says little, and says nothing about *where*. Smoke shows the place. The
  vacuum gauge above is a different instrument, for the running engine.
- ~~**A fuel pressure gauge**~~ — **not bought** (*owner's decision*,
  10/10/2026, H7): kept for H7 test 1 if 032 ever wanders; it would need
  the adapter for this rail and a scale well past the regulator's 3 bar.
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
