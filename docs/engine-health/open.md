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
| `plan.md` | **the planned fixes, in order**, and the rule that governs them: S18 and the idle first, no test for its own sake, as little idling as possible. Emptied step by step as the work is done |

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

## Where it stands — 18 October 2026

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
| S6, the exhaust joint behind the converter | shimmed 12/10 and not heard on the drive that day (*owner*) |
| S15, the sputter close behind the engine | not heard since S6's joint was remade, 12/10; the owner's reading is that it was that joint (*owner's decision*) |
| H10, the learned idle air value turns the counting on | accepted as the explanation of when 014 counts, closed at the owner's decision (9/10, `refuted.md` C19). Why the ECU learns air away stays with H3 and H8 |
| H9, crankcase ventilation and the cover gasket | right about S10, settled against for the idle (4/10, `refuted.md` A15) |

Everything else settled against is in `refuted.md`.

**Open — what this file is still for:**

- **S18 is now the worst symptom** (*owner's decision*, 18/10/2026),
  ahead of the idle; the owner reads the two as likely one cause
  (deposits, H13). **S18, cylinder 3 out cold with a tick at camshaft
  rate** (18/10):
  P0303 and P0300 stored, the first time the ECU has named a cylinder;
  gone after a restart and through a longer drive. Ranked re-read: H13
  up to 2 behind H1, H3 to 3. **It came back warm the same afternoon**:
  the tick for a few minutes, and two short bursts in 014 under part
  load, the largest the counter has ever read while driving, with no
  code. A loose flake fits better than the valvetrain. **20/10, the
  look inside**: only 3 shows deposit come away, on its exhaust valve
  and crown (`idle-log.md`). **No leak-down** (*owner's decision*,
  20/10); whether S18 recurs is what tells a flake from a valve.
- **The idle: S1 (unsettled) and S3 (misfires counted at idle).** Every
  part in the fuel and ignition path has been replaced and both remain.
  **When** 014 counts is settled — it follows 055's learned idle air
  value (`refuted.md` C19, closed 9/10) — but not **what the fault is**.
  **The dips are not shared alike** (9/10, *Naming the
  cylinder*): **about two thirds on two cylinders that fire one after the
  other, and on `31`, where the cuts name them, those are 3 and 4**
  (16–17/10, *One cylinder or two*; the documents said *one cylinder*
  until then), and the old parts named two single-cylinder faults: lead
  4's plug end and plug 1, almost loose (H4, 1d). **New plugs and leads
  went in on 10/10, and on the drive after the dips did not keep to one
  slot — but 014 counted as before** (S3, *The drive after the new
  leads*). So the leads did not fix S3; whether they took the
  one-cylinder share of the dips, two or three more drives say —
  **and on 12/10 the dips were back on one slot** (38 %, p = 0.001), so
  they did not take it either. The
  servo is cleared (H3). **Re-ranked 20/10 after the look inside:
  H15, H13, H1, H3, H4, H14, H2** (*The idle's candidates, ranked*).
  Ranked before it (*re-read 17/10*, when the dips
  were named on 3 and 4): **H1**, the valvetrain of 3 and 4 — two
  neighbouring sets of lifters, and 4 is S5's cylinder; **H3**, a leak
  at the runners or the lower gasket of 3 and 4; **H13**, deposits,
  whose test — the cleaner and the tank — is under way; **H4** without
  its spark side (separate leads and coil outputs, unchanged by the new
  set), leaving the injector loom at 3 and 4 — lead 4 **still looser
  than the other three by hand** (15/10, H4 test 1e) explains 4 at most,
  not 3; then **H14**, the remap
  of 6/2018 (added 16/10 at the owner's request), as a margin taken from
  all four, read when the original map goes back on 22/10; then **H15**,
  the aftermarket leads (added 17/10 at the owner's request): VW
  originals were decided on 9/10 and NGK went in; a genuine set,
  **upper plenum off to fit them** (*owner*, 18/10), is **put off
  indefinitely** (*owner's decision*, 18/10, after S18) — against it, a clean engine under load
  and two cylinders on separate leads; then **H2**, the
  exhaust ahead of the probe, down from 1: nothing cold, and it acts on
  all four alike (*The idle's candidates, ranked*). **H11**, both lambda probes shifted alike, is
  written down last (10/10, at the owner's request) so that it is not
  argued again from the start.
- **Around the idle:** S2 (an occasional puff from the exhaust) and S11
  (a hiss at the back of the engine at a warm idle, not yet placed) —
  **neither heard on 9/10 or 10/10**; **S2 heard again on 12/10**; **S11 closed 12/10 and reopened 14/10**, heard again at the back on the gauge start (*owner*);
  quieter, and by the owner's ear together with the dips. **S15**, the constant
  sputter close behind the engine, **closed 12/10**: gone since the
  joint behind the converter was remade, which the owner takes as its
  source. **The tailpipe test found no leak cold on 12/10**; the warm
  one is H2's, for S2 and S11.
  **S16**, a tick in neutral, cold, gone with the clutch pedal down
  (added 12/10) — the gearbox side, **not pursued** (*owner's
  decision*): the clutch minutes showed it has nothing to do with the
  idle (H12).
- **On the overrun: S14**, the burble on an unblipped downshift,
  **reopened 15/10** — back, now and then and much quieter, with the
  joint behind the converter still tight. **S17**, a new exhaust sound
  from a new place (added 15/10): **only at about 2200 rpm, like a
  resonance** — a part vibrating rather than a leak; the joint behind
  the converter or one nearer the engine, not yet placed.
- **The cylinder 4 knock window: S4 and S5**, a cluster of its own
  (H5, H6). The injectors were cleared from it on 9/10 (`refuted.md`
  B7). **Not in `plan.md`** (*owner's decision, 9/10/2026*): no link to
  the misfires has been found, so its tests, G66 first, stay in H5.

**12/10** (`idle-log.md`): the exhaust test cold found nothing (H2,
warm still open); the clutch minutes cleared the gearbox side (H12); the
idle raised to the ECU's limit, 830 rpm, did not quiet 014 and was put
back; and **the warm idle read calmer than on any day before** (S1,
*12/10*), cause unknown. S6 closed and S16 added; neither is a column of
the fit tables, so the ranked list stands as it was.

**The next start carries four changes at once** (*owner*, 12/10): the
airbox crack sealed inside and out, both layers cured; the three thin
and breather hoses new — the breather hose and the tee's hose on the
connector ahead of the throttle, the shroud supply behind the MAF; and the 8 mm hose
from the throttle to the tee checked, and narrower if it sits loose.
So an improvement after it cannot be put down to one of them; the
vacuum gauge reads only the hoses' share (S9, *the cracked airbox*).

**Next:** `plan.md` step 3 — **nothing until the vacuum gauge arrives** (ordered 10/10, *owner's
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
differ from 3/10**: at a hot stop, ~97 °C, dips ≥ 20 rpm a minute went
20 (`19`, old MAF) → 9.1 (`24`) → 5.0 (3/10) → **4.4**, and `IdleHealth`
112–146 → 84 → 62 → **60**; in the middle band the dips sit at 9–11 on
`24`, 3/10 and 4/10 alike (S3, *Session A after step 1b*). ~~So the calm
the owner feels is the job of 1–2/10 at the hot idle~~ — *withdrawn
9/10/2026*: both calm hot stops came on **fresh adaptations**, and on
settled ones the hot idle is back where the MAF left it (below). 1b's
change is in 014 rather than in engine speed.

**Every session since the repairs, like with like** (*re-read
9/10/2026*): standing idle in 30 s windows, `IdleHealth` (lower is calmer;
`idledips --roughness`'s mean step in rpm × 50), ± the standard error
over the windows, binned by 0x420:

| session | adaptations | < 44 °C | 71–91 °C | 93–111 °C |
|---|---|---|---|---|
| `19`/`20`, 24/9, new injectors, old MAF | fresh | 111 ± 11 | 109 ± 5 | 113 ± 5 |
| `24`, 24/9, **new MAF** | fresh | 104 ± 14 | **84 ± 4** | **91 ± 7** |
| `25`/`26`, 3/10, after the job, cover open | fresh | 130 ± 12 | 111 ± 5 | 68 (2 windows) |
| `27`/`28`, 4/10 A, the right gasket | **fresh** | 121 ± 15 | 96 ± 2 | **74 ± 4** |
| `29`, 4/10 B | settled | — | 105 ± 9 | 89 (2 windows) |
| `30`, 9/10, dipstick and MAF clamp | settled | 95 ± 7 | 95 ± 4 | **89 ± 3** |
| `31`, 10/10, **new leads and plugs**, intake gasket | settled | 120 ± 11 | 96 ± 3 (4 windows) | **77 ± 4** (cuts left out) |

**The MAF is the one change that shows** (middle and hot band, and the
dips halved). **Nothing since does, once adaptations are matched**: the
middle band has stayed at 84–111, and the calm hot idle of 3/10 and
4/10 A — taken for the job's — came on fresh adaptations and is gone on
settled ones. That is the same pattern 014 shows (`refuted.md` C19):
**fresh adaptations look better on both rulers**, so a session after a
battery disconnect is no test of a repair. The one hint the other way
is 9/10's cold idle (95 against 120–130), on five windows and a cold
idle that also depends on how long after the start it is measured:
the next cold start on settled adaptations says whether it holds.

**How it is measured.** `IdleHealth` on 0x604 grades one firing against the
next (100 = the engine before the repair, lower is smoother). Offline,
`tools/idledips.py` counts dips of ≥ 20 rpm and computes the same grade from a
capture. **Every idle figure in these files is on the `IdleHealth` scale**
(*owner's decision*, 12/10/2026: like with like): `idledips --roughness`
prints the mean step in rpm, and `IdleHealth` is that × 50
(`IDLE_ROUGH_100` = 64 counts of 1/32 rpm = 2.00 rpm). A figure from a
capture is a mean over a window; the display shows a running filter of
the same quantity, so the two agree on a steady idle and not to the unit.

**Current values**, *owner-reported off the display*. Hot idle, 96–100 °C of
oil: `IdleHealth` **57–100, sometimes over 100**; 93 on the last reading,
"fluctuating a lot". At 79–95 °C: about 120. Readings with no temperature
noted: 80–160, which compare with nothing. Dips ≥ 20 rpm at a standstill idle: **5–11 a minute**
(`24_mafswap_drive_z1`), down from 15–21 on the old MAF the same morning.

**What is not known: the healthy target.** Every recording is of this engine
with the fault present. August's hot idle graded 48 (and 29 with the A/C on),
but those are 22-second holds, shorter than the device waits before it grades
at all, and August's idle stumbled too. **So nobody knows what a well AQY
grades.** That is hypothesis H0 below, and it is the first thing to fix.

**When S1 closes** (*decided*, 20/10/2026, the owner's question; the
owner closes it): with no healthy target, by three relative marks, read
over several drives at 95–100 °C of oil: **(1) the dips no longer keep
to a pair** — `cutscan.py --shares`, pooled since the last repair,
consistent with all four alike; it needs no target, so it is the
strongest of the three; **(2) load is no longer needed** — loads-off
`IdleHealth` within about 25 of the loads-on figure, pair after pair
(19/10: about 100 against 50); **(3) at least the best level this car
has shown**, loads off about 50–60 (12/10, 15/10). A healthy AQY's
recording (H0 test 1) would replace (3) with a real target. Short of
all three, the owner may still close it as *acceptable, cause known*.

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
  (A/C on, 29) were taken minutes apart on 11/8 at 101 °C of oil; the A/C
  one being smoother is the load effect above. So the hot, loads-off
  August idle is **one 19 s hold grading 43–48**.
- **Against September at the same state.** `24` at 96–97 °C, loads off —
  the same torque at idle on 0x280 b7 (23 against August's 25) — cut into
  the same 22 s windows grades **53–106**, median about 75. August sits
  just below September's best window: unusual, not impossible by chance.
- **At mid temperature August was not better.** `09`, the same day at
  85 °C, grades 79–104 per window; `24` at 80–85 °C grades 48–89.
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
NGK ones (H15).

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

**Since the cleaner, the partial loads hardly matter** (*owner-observed
off the display*, 19/10/2026): since the PEA tank, lights alone or a
few consumers make little difference, sometimes the opposite (on 18/10
about 80 with nothing on, nearer 100 with some loads); **everything on
together** (main beam, both seats, heated glass, A/C, blower on full)
still calms it, consistently. Estimates off the display at first;
the two-state reading in `plan.md`'s standing items is what measures
it. **The first pair, 19/10/2026 afternoon** (*owner*, off the display,
oil 101 °C, after a brisk drive): **loads off 90–120, mostly about 100;
every load on 30–70, mostly about 50**, with restless stretches up to
70. Main beam stayed off, on a car park, so as not to dazzle other
drivers. A difference of about 50, against the 25 one pair can show
(`plan.md`, *`IdleHealth` in two states*): **everything on together
still calms it, now measured once**. The same evening, oil 100 °C, lights and the
blower on its first step read **100–110, at moments 120** (S18): the
partial load did not help again. Read as (*reasoned, not shown*): if the cleaner took part
of what made the idle rough only at low air flow, what is left depends
less on the load.

**The roughest reading yet, 26/9/2026 — cold, and in fog.** A few minutes
after an overnight cold start (`StartClt` 14 °C) on a cold, foggy, very damp
morning, `IdleHealth` read **~186** (`IdleRough` 3.72 rpm) before the car drove off.
*Owner-reported off the display, not photographed.* ⚠ Not comparable with the
warm figures: the grade had not converged (under 30 s of idle; the filter
rises from zero, so an unconverged reading is if anything low), and the only
recorded cold idle, `18_coldstart_z1`, graded 137 in its first minute at
25 °C of coolant. What it adds is the weather: the start itself was clean and
the idle the worst seen, **on the dampest morning yet** — which is what an
ignition fault that tracks moisture would do (H4, test 1e).

**Temperature matters: roughest cold, calmer as the oil warms, calmest
hot.** Re-read 9/10/2026 over every capture since 24/9 (standing idle,
binned by 0x420, `idledips --roughness`): the mean step is highest cold
and falls with the oil in every session, on fresh adaptations and settled
ones alike — on `30`, 103 at 17–31 °C, 95 at 71–84, 93 at 84–97,
77 at 97–111; on `29`, 117 / 106 / 93 / 92; on `27`/`28`, 121 /
97 / 76. The dip count scatters (8–22 a minute) with no band
consistently on top. *Corrected 9/10/2026, at the owner's question:* this
read "not monotonic … worst at about 71–85 °C of oil", which no capture
since 24/9 bears out for engine speed; the middle-band peak is 014's
(S3), and on settled adaptations that is shallow. ⚠ Every engine idles
roughest cold (*general*: enrichment, a raised idle), so cold-worst says
nothing about the fault on its own. A reading without the oil
temperature beside it cannot be compared with anything.

**One dip, read stroke by stroke — 11/10/2026** (*the owner's request
to see the dips "through my eyes"*). The figure is `dip-profile.svg`,
beside this file, drawn by `tools/dipcontext.py
--profile --svg` from `26`, `28`, `29` and `30` — engine speed straight
off 0x280, not averaged over a cycle, each dip aligned on its own lowest
value, injection time and indicated torque beside it, all relative to
1.2 s before. One stroke is ~37 ms at this idle.

![One idle dip](dip-profile.svg)

| from the bottom | engine speed | injection, torque | read as |
|---|---|---|---|
| −0.5 s | a few rpm **above** where it was | both begin to fall | the idle has overshot a little |
| −0.5 to −0.15 s | stays a little above | down about 0.3 count each, lowest at −0.18 s | the governor takes charge away; the lambda loop is on its lean swing (VCDS, next bullet) |
| −40 ms to 0 | **falls in two strokes** to about −22 | injection already rising | **the event**: a stroke that gives little or nothing |
| 0 to +0.2 s | climbs back over ~5 strokes | injection up at once (about +0.5 count by +0.16 s), torque from +60 ms | the governor answers the fall |
| +0.2 to +0.3 s | overshoots by about +6 | both ease off | settling |

*Reasoned, with the control loop as general knowledge:* Motronic holds
the idle on a slow path (throttle angle, so air, with the fuel computed
from the MAF and trimmed by the lambda loop) and a fast one (ignition
advance, which changes torque on the next stroke) (*general*). Read in
that light, **the ECU behaves correctly throughout**: it trims when the
idle overshoots, it answers the fall within a stroke or two, and the
size of both is ordinary. What is not ordinary is the engine: **a
charge about one per cent smaller and leaner than usual, inside the
range the control always works in, is enough for one combustion to
fail.** A healthy engine has margin for that. Something narrows it —
in one cylinder or in all — which is the question H1, H3 and the
deposits answer differently; it is also why load calms the idle and
why a higher idle is a fair mitigation. ⚠ An average: the trim before
the dip is under one count, so roughly one dip in three carries it
(next bullet); and 014 cannot be matched to single dips (S3).

**What comes before a dip — 10/10/2026** (*the owner's request to go
through every idle again*; `tools/dipcontext.py`, warm standing idle at
≥ 77 °C of oil, the injector cuts of `31` left out, captures `19`, `20`,
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
  ~~**Not the lambda control**~~ *(10/10/2026; corrected 11/10, below)*:
  this read that the lambda control works on fuel alone and swings
  wider, that 014's rises fall on its lean and rich swings alike
  (`refuted.md` C5), and that the torque falling with the fuel after a
  small rise in engine speed is the idle governor's signature. **The
  torque and the speed rise still say governor; the fuel may be the
  lambda control's as much** — see the next bullet.
- **What VCDS saw just before a dip** (*11/10/2026, the owner's
  question whether slow VCDS samples ever landed beside a dip*;
  `tools/dipcontext.py --vcds`, captures `26`, `29`–`31` with their
  logs, warm idle, cuts out). VCDS samples about once a second, so no
  single sample sees a dip — but over hundreds of dips some land within
  0.6 s before one, some after, and the rest are quiet idle:

  | VCDS field | before a dip | after a dip | quiet |
  |---|---|---|---|
  | 033 lambda correction | **−0.69 ± 0.23 %** (n 85) | −0.25 ± 0.28 % | **+0.11 ± 0.10 %** (n 361) |
  | 033 probe voltage | 0.40 ± 0.03 V | 0.33 ± 0.03 V | 0.36 ± 0.01 V |
  | 003 ignition advance | 3.6 ± 0.2° | 3.9 ± 0.2° | 3.3 ± 0.1° |
  | 003 air | 3.15 ± 0.01 g/s | 3.16 ± 0.01 g/s | 3.12 ± 0.01 g/s |
  | 055 regulator, learned | no difference | | |

  **Just before a dip the lambda control was taking fuel out** — the
  probe reading a little rich, the correction about 0.8 % lower than in
  quiet idle, about three standard errors. That is the size of the
  injection-time fall on the bus (−0.9 %), so **that fall may be the
  lambda loop's leaning swing rather than, or as well as, the
  governor's trim.** Around dips the governor is busier — a little more
  air and advance, a correction of the dips themselves (*reasoned*).
  ⚠ Two sessions carry the 033 rows (`29`, `30`), so a direction, not a
  figure; it **sharpens `refuted.md` C5**, which timed the probe against
  014's rises (late by the counter's own window) rather than against the
  dips, and found no side. **What it means**, if it holds: a cylinder
  that misfires on the lean side of the loop's swing — a mixture margin
  as much as a charge margin, which leans toward a lean runner (H3) and
  a mixture shift (H11, H7) a little more than toward a valve (H1).
  **More of it is cheap**: VCDS reads faster with fewer groups, and
  group **001** alone carries engine speed (to align on) **and** the
  lambda control (`vcds.md`).
  **12/10: not reproduced** (`32`, 3 min of 001 alone at a warm idle,
  `dipcontext.py --vcds`, which now reads 001): lambda correction
  **−0.38 ± 0.15 %** before a dip (n 62), **−0.48 ± 0.06 %** quiet
  (n 374), −0.56 ± 0.16 % after — no difference; the drive's own 001
  log the same (−0.40 / −0.55 / −0.60). So the lean swing before a dip
  is **not shown** on the one session built to show it, as many samples
  beside dips as the two earlier sessions together. Either it was
  chance there, or it belongs to the rougher idles of `29`–`30` and not
  to the calmer one of 12/10 (S1, *12/10*). It stays a direction that
  one session failed to repeat.
  **Read against H2** (*the owner's question*, 11/10): air drawn in
  ahead of the probe makes it read *lean* and the loop add fuel; just
  before a dip it read a little *rich* and the loop was taking fuel out —
  the other way, so this is **no help to H2**. After a dip the probe
  reads leaner (0.33 V), which is what a missed firing's unburnt oxygen
  passing the probe would do (*reasoned*). **Read against a probe that
  jumps** (H11's kin): 0.8 % is well inside the loop's ordinary ±7 %
  swing, so this is the loop's normal phase, not a glitch; a glitch
  would need the probe's own fast signal to see.
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
(H3), a late cam (the belt a tooth out, ranked 11), or the engine's own
margin (H0) — **it does not choose between them**. It argues against a
fault that does not care about the charge: an intermittent wire, a
crank-sensor artefact (which would repeat at 360°, not 720°).

**12/10 — the warm idle calmer than on any day before** (`32`,
`idle-log.md`). At 95–99 °C of oil `IdleHealth` was **50** at the first
warm stop and **61** over 5½ minutes at the original idle setting,
against **77–89** for `30` and `31` at 93–111 °C; dips 3.7–4.9 a
minute. The owner saw smaller 014 figures than usual; **counted, 014
moved little** (*read 12/10/2026*, the owner's question; standing idle,
detection `aktivováno`, aligned on engine speed, 10/10's cuts and
12/10's raised idle left out):

| oil | 9/10 (`30`) | 10/10 (`31`) | 12/10 (`32`) |
|---|---|---|---|
| < 57 °C | 1.8 a minute, 11 % non-zero | 6.2, 39 % | 6.9, 48 % |
| 57–84 °C | 9.6, 61 % | 9.8, 61 % | 7.6, 55 % |
| 92–111 °C | 8.8, 58 %, max 96 | 6.1, 42 %, max 48 | **5.3, 40 %, max 84** |

Rises a minute, then the share of samples non-zero. The hot band is a
little lower day by day and the readings are the usual twelves (median
12), so the calm of 12/10 shows on engine speed and hardly in 014: a
direction, inside the scatter of one session. Adaptations
settled (055 −1.18 to −1.21), and 032 read **0.0 / +2.3 %** after it,
against −0.8 / +2.3 on 4/10 and −2.3 / +5.5 on 9/10. Changed since `31`:
the joint behind the converter, which is behind both probes and so not
it (`refuted.md` A13), and **a new air filter with the airbox crack
ahead of the MAF sealed** (`vehicle-history.md`). Cold it was no better
— 125–145 at ~44 °C against `31`'s 120. **One day, cause unknown**;
the drives of `plan.md` item 6 say whether it holds, and a calmer idle
on the next drives with nothing else changed would point at the airbox.
**Raising the idle did not help**: from 780 to 830 rpm specified, the
ECU's limit, 014 kept counting and `IdleHealth` rose slightly with engine
speed; put back the same day.

*What else moved on the bus that day* (every byte of 0x280 and 0x288 and
the fuel counter, standing warm idle at 91–104 °C of oil, `24`–`32`;
*read 12/10/2026*). **One thing: the engine held the same 797 rpm on
the least charge on record** — indicated torque (0x280 b7) 20.0–20.9
against 21.6–26.6, injection time (0x288 b6) 34.0–34.9 against
35.3–39.0 counts, fuel 286–293 against 291–320 µl/s. Against `30` and
`31`, about 8 % less injection and 15 % less torque. Nothing else
moved: the throttle at rest (b5 35), the load byte at its idle floor
(b6 21), coolant and oil as on the other days; in VCDS the lambda
correction (001, −0.46 % mean) and the idle controller (055, 056) as
before. **It does not track the grade across days**: `24` needed
nearly as little and graded 91. Two readings, neither shown
(*reasoned*): fewer weak strokes, so the governor needs less charge to
hold the speed — the calm idle the cause and the low charge the
result; or **the MAF reading truer**, the airbox crack having disturbed
the flow across it (S9, *the cracked airbox*) — which 032's idle cell
agrees with, from −2.3 % on 9/10 (fuel taken away) to 0.0 %. The
intake air temperature, which a leaking airbox in the engine bay would
raise, is not on the bus. 003 was not logged that day, so the MAF's own
figure at idle is not known; the next session that logs 003 at a warm
idle reads it against 3.08–3.12 g/s (S3).

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

*12/10/2026, owner:* **heard again at idle, much quieter** than before
the joint behind the converter was shimmed, and **heard together with
the dips in engine speed** — the owner's ear, standing at the car,
not an alignment of a recording with the capture. So the puff
**outlived the resealed joint** (S2 ↔ S6) and goes with the dips, as
a misfire's unburnt charge would (S2 ↔ S3); it does not say which
cylinder. It also counts against the dips being driveline play (H12),
which puts no charge into the exhaust. The tailpipe test that day, cold,
found no leak ahead of the converter (S15).

### S3. Misfires counted by the ECU at idle

**VCDS group 014**, on every drive since the counter was first logged.

**When S3 closes** (*decided*, 20/10/2026): **014 reads 0** at a warm
idle with loads off, oil 95–100 °C, for at least 3–5 minutes, **on three
sessions on different days, one of them straight after a hard drive**,
where it has counted most. VW specifies 0–5 and this counter steps in
twelves (*The blocks*, `vcds.md`), so zero is the only reading inside
the specification.

- **122 of 129 new events began at a standstill idle**; the few seen in 1st
  and 2nd are mostly the three-second hold of an event that began standing.
  None during a pull.
- **"Only at idle" is the car, not a blind spot of the detection** (added
  3/10/2026). The method (`vcds.md`, block 014, *What the number is*)
  sees a misfire **more** easily under load — each firing is a large
  torque pulse there, so a missing one stands far out of the noise — and
  is weakest at idle, which is why it switches off below about 20 % load
  (*general*; **measured 11/10/2026** over every 014 log, the load in
  the same group: detection `aktivováno` in **none** of ~2,550 samples
  below 18 %, 5 % of them at 18–20 %, 46 % at 20–22 %, 83 % at 22–24 %
  and 90–97 % from 24 % up. Of the 832 samples off above 24 %, **404
  lie within three samples (~2 s) of a load under 18 %** — the pedal
  released, the engine braking, as the owner has noted, and detection
  staying off a moment after; the other half the group alone cannot
  explain — a gearchange or tip-in would need the throttle beside it). And on this car it has worked under load: the historical
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
- **Unless the remap dulled the detection under load** (*the owner's
  question*, 18/10/2026; H14 route 6). Everything above was read on the
  remap, and the detection's thresholds are calibration, so "only at
  idle" holds for this calibration and not yet for the engine.
  **Against it, already**: the full-load lamp of `refuted.md` C4 came
  on **after the remap** (*owner*, 18/10/2026), so the detection under
  load was not off; 032 reads small, where frequent misfires under load
  would show as a learned enrichment (the unburnt oxygen reads lean at
  the front probe); and the converter and the rear probe are well (C5).
  None of it rules out thresholds raised short of off. **Nothing
  independent sees a misfire while driving**: the dips on 0x280 are the
  calibration-free witness, and the noise there swallows them. **The
  comparison for the stock map**: new counts per `aktivováno` sample
  above 1500 rpm, **15 in about 4,300** on the remap.
- **Values 12–120 against the label file's stated 0 to 5.** By VW's own
  measuring-block specification, this is out of range.
- **The events are the S1 dips.** Aligned on engine speed, counter increments
  sit next to dips far more often than chance: p = 0.023 on the cold start,
  0.005 and < 5×10⁻⁵ on the two drives of 24/9. ⚠ Both are readings of crank
  speed (*general*: that is how OBD misfire detection works), so they are not
  two independent witnesses. And the converse does not hold: only 7 of 34,
  37 of 319 and 38 of 70 dips carry an increment.
  **Re-read over every capture with a 014 log, 16/10/2026** (*the owner's
  question*; `tools/s3align.py`, eleven sessions from `18` to `37`,
  standing idle with detection `aktivováno`, the cuts left out; four logs
  do not line up with their capture by engine speed and are skipped):
  **the timing holds in every session that counts at all.** The dip
  sits **0–1.5 s before the 014 sample that shows the rise**, and
  nowhere else (`--lag`). **50 % of the 857 rises have a dip of 20 rpm
  or more in that 1.5 s, against 22 % of the samples that did not rise**,
  p between 10⁻³ and 10⁻²⁰ session by session; the one exception, `35`,
  counted twice in a drive. **The converse still does not hold: 32 % of
  the 1,513 dips are followed by a rise**, and on `18`, `19` and `35`
  almost none (15 %, 10 %, 2 %). **And over minutes the two part**
  (`--windows`, 103 stretches of 60 s): rises a minute against
  `IdleHealth`, Spearman **0.20**; against dips a minute, 0.16; dips a
  minute against `IdleHealth`, **0.79**. At 90 °C of oil and up, the
  minutes with 014 silent read `IdleHealth` 104 in the median (n 6, 52–
  142), those with it counting 76 (n 42) — **a silent 014 was if anything
  the rougher idle.** So: **when 014 counts, it counts these dips; whether
  it counts is decided elsewhere** — the load and the learned idle air
  (`refuted.md` C19), not how rough the idle is. `35`'s near-silence came
  on the morning's stops under the blower, seat heating and at times the
  A/C (`idle-log.md`, 15/10).
- **The A/C switches it, by the owner's eye, 16/10/2026** (*owner*,
  VCDS 014 and the display, no capture): a warm idle after a brisker
  drive; **with the A/C on, 014 sat at zero for several minutes while
  `IdleHealth` read about 70; with the A/C off, 014 began counting and
  `IdleHealth` barely moved.** The same as the re-read above, seen
  live: the count follows the state the ECU is in, not the idle. Not a
  new symptom (*owner's decision*, 16/10): a property of S3's witness.
  Which of the load or the idle air does it is not told apart; a stop
  with a capture, A/C on and off, 014 and 055 in VCDS would.
- **No fault code is stored.** The rate stays below whatever the ECU needs to
  set one. **It once did**: an old scan from **5/2019** holds P0300 and
  **P0304, cylinder 4**, with P0172, too rich (*owner*, found 10/10/2026;
  `vehicle-history.md`, *Fault memory, as found in old scans*) — so in
  2019 one cylinder, number 4, misfired past the 2 % store threshold,
  inside the old converter's life. History, not a symptom of today's
  engine: every part in that cylinder's fuel and ignition path has since
  been replaced, and nothing has been stored since 2019.
- **When the counts start after a cold start** (checked 28/9/2026, VCDS
  014 aligned on engine speed to the captures). **11/9** (`18`, old
  injectors): the first count **2 min** after the start at coolant 35 °C,
  oil 21 °C, then steadily from ~4 min (coolant 56–64 °C). **24/9** (`19`,
  the injectors fitted 23/9, old MAF): **3 min of cold idle with detection
  active and no count at all** (coolant 12 → ~48 °C); the first count at
  +584 s, coolant 90 °C, oil 61 °C, then many. The logs after the MAF
  swap (`24`) begin warm and cannot say. So on the car as it now is, **a
  cold idle without counts is not evidence of a fix.**

- **How often 014 counts, by oil temperature** (*computed 29/9/2026*:
  014 aligned on engine speed to the capture beside it, standing at
  650–900 rpm with detection `aktivováno` only, binned by 0x420):

  | oil | `24` — new MAF, adaptations fresh | `19` — old MAF, adaptations fresh |
  |---|---|---|
  | 68–79 °C | — | 3.6–10 a minute |
  | 79–84 °C | **20 a minute** (102 s) | — |
  | 84–89 °C | 2.5 a minute (95 s) | 1.5 a minute (196 s) |
  | 89–95 °C | — | 2.0 a minute (152 s) |
  | 95–100 °C | **10 a minute** (318 s) | **0.3 a minute** (433 s) |

  On `24` the longest stretch of active standing idle with no count is
  **57 s**. On `19` the last ~6½ minutes of hot idle at 97–99 °C read
  **zero** — on the car before any repair, which is what A11's change of
  ruler looks like from the other side: **on the old MAF a hot-idle zero
  is not evidence**, and only `24` is a comparison for the car as it now
  is. The test after the job (`plan.md`) takes its two stops and their
  lengths from this table.

- **Session A, 3/10/2026 — after the valve cover and throttle job**
  (`25_sessionA_cold_z1` and `26_sessionA_warm_z1`, with
  `vcds/vcds-sessionA-003-014-055.csv`). A cold start after a 27 h
  stand, ~7 min of cold idle, a drive to the 77–95 °C band, ~6 min
  standing there, a drive home, ~2 min hot. Fresh adaptations (battery
  off for the job). Aligned on engine start and stop; the two clocks
  drift 12 s in 31 minutes, which is ignored. Standing idle only,
  binned by 0x420:

  | oil | 014 rises a minute | 014 non-zero | dips ≥ 20 rpm a minute (`24` / `19`) | `IdleHealth` |
  |---|---|---|---|---|
  | < 57 °C | **0** (419 s) | 0 % | **22.0** (11.8 / 13.7) | 120–178 |
  | 57–84 °C | **16.8** (111 s) | 75 % | 15.7 (9.4 / 22.4) | — |
  | 84–92 °C | **15.6** (299 s) | 75 % | 9.3 (5.2 / 14.0) | 101–117 |
  | 92–111 °C | **3.0** (102 s) | 40 % | 13.6 (8.6 / 19.4) | 60 |

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
  | A1, cold | 19–27 °C | 318 s | **0** | 17–20 | 81 → 171 |
  | the joint stop | 59–67 °C | 116 s | **0** | 11.9 | 126 |
  | **A2** | 77–87 °C | 255 s | **0** | **9.1** (3/10 at 81–91 °C: 10.8) | 103–109 |
  | **A3** | 95–99 °C | 468 s | **0** | **4.4** (3/10 at 96 °C: 5.0) | 56–62, one window 109 |
  | hot, after a hard drive | 100–101 °C | 238 s | **7–9** | 7–11 | 82–92 |
  | the MAF wiggle | 101 °C | 71 s | 13.6 | 15.3 | 79 |

  **The MAF wiggle found nothing** (`idle-log.md`, *The MAF*):
  the counts were there before it (*owner*, watching 014 before he went
  to the engine), and 003's air never dropped out under the hand. Its
  13.6 against 9.2 a minute is 71 s against 189, a difference that small
  a sample does not carry.

  *The 3/10 figures beside A2 and A3 are its stops taken whole, by the
  same rule; they replace 15.7 and 13.6, which were the 57–84 and 92–111
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

- **Session B, 4/10/2026** — after a cool-down to 47 °C of oil, a
  part-warm start (coolant 44 °C, `StartCrank` 0.70 s, `StartDip` 0),
  ended by the owner at B1 (`29_sessionB_z1`, with
  `vcds/vcds-sessionB-014-055-033.csv`). Standing idle, 014 aligned on
  engine speed:

  | stop | oil | 014 a minute | dips a minute | `IdleHealth` | 033, median |
  |---|---|---|---|---|---|
  | after the start | 45–52 °C | **1.5–4.3** | 9–19 | 135–156 | 0.0 / +0.8 % |
  | **B1** | 83 °C | **14.3** | 11.3 | 120 | **−0.8 %** |
  | home, two stops | 96–99 °C | ~5 | 8–20 | 90–143 | −1.6 % |

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
  | A1, cold | 17–21 °C | **1.4–1.8** | −1.12 | 12.1 (16.5) | 86 (98) |
  | **A2** | 79–85 °C | **6.8** | −1.10 to −1.17 | 8.4 (9.2) | 67 (70) |
  | **A3** | 94 °C | **10.7–12.5** | −1.11 to −1.17 | 13.9 (4.4) | 56 (39) |
  | hot, the way home | 100–101 °C | 3.7–5.8 | −1.17 to −1.32 | 7.4–10 (6.7–15) | 41–61 (38–59) |

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
  | cold idle, servo held | 17–21 °C | **3.6** (1.4–1.8) | 3.89–4.42 |
  | short cold stop | ~31 °C | 14.0 (—) | 3.73 |
  | middle | 81–84 °C | **9.4** (6.8) | 3.15 |
  | hot, before the cuts | 96–97 °C | **6.0** (10.7–12.5) | 3.08 (3.12) |
  | hot, after the cuts and home | 97 °C | 2.7–5.7 (3.7–5.8) | 3.11–3.24 |

  055's learned value −1.14 before the cuts, −1.28 after (9/10: −1.07 to
  −1.33). **The misfires are not gone**: better at the hot stop, worse in
  the middle and cold, no direction overall. **The dips no longer keep
  to one slot**: `cutscan.py --pairs` over the idles outside the cuts,
  10 of 39 pairs on the same slot, 26 % against chance's 25 % (9/10: 34
  of 103, 33 %); over the whole capture the tool reads 41 %, but 38 of
  its 78 pairs are inside the cuts, where a dead cylinder is the slot.
  Fewer pairs from a drive of the same kind means fewer dips. ⚠ 39 pairs
  is a direction: 33 % and 26 % are not apart at this size. The
  `IdleHealth` by oil band (S1's table): calmer hot (77 against
  89), the same in the middle, rougher cold (120 against 95) — the
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
- **12/10/2026: back, smaller than 9/10** — 16 of 2,231 samples on
  cylinder 4, up to 11.2°, and 3 on cylinder 1, up to 3.7°, on a drive
  with pulls to 5,800 rpm (`32`, `vcds/vcds-step3-1-drive-014-001-020.csv`);
  10/10 had 3 to 1.5°, 9/10 44 to 13.5°. So the new leads did not take
  it away; harder driving brings it back. Out of `plan.md`, as S4 is.
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

### S6. The exhaust is not tight — closed 12/10/2026

**Closed, 12/10/2026**: shimmed that morning, and **not heard once on the
drive the same day** (*owner*; `idle-log.md`). The bolts were tightened
once more cold that evening: one moved a little, the one over the shim
did not move at all — the sealant inside settling (*owner*). Heard again
→ the hangers, then a welded joint at an exhaust shop. What follows is the record.


**Reopened at the owner's decision, 10/10/2026**: the joint remade on
9/10 **is heard again** (*owner*). Its cause is the one noted at
closing: the pipe from the converter reads **54.2 mm** and the one from
behind **55.0 mm**, against the connector's **55** (*owner-measured*;
*corrected 12/10/2026* — this said the pipe behind was the narrower), so
even fully tightened the narrower pipe **moved in the connector**. The closing note said a connector change
would be a repair rather than a reopened symptom; the owner reopened it
because it is again a noise in the zone being listened to. **The fix
planned** (*owner*, the method *general*): the connector off, a shim of
thin sheet — about 0.4–0.5 mm, stainless, **not galvanised** — wrapped
round the narrower pipe under it, a thin coat of exhaust sealant under
and over the shim, the bolts tightened evenly and again after the first
heat cycle, and the hangers checked for strain. **Done 12/10/2026** (*owner, photographed*:
`photos/exhaust-joint-2026-10-12-*.jpg`): the strip and the sealant
under the connector, and nothing moves. **Open until the drive says
whether it is quiet** (`plan.md` item 1). **Why it matters here**:
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
one pipe is about 1 mm narrower than the other (*owner*; *Corrected 12/10/2026* (*owner-measured*): the narrower pipe is **the one from the converter, 54.2 mm**; the one from behind is **55.0 mm**; this said the pipe behind was the narrower.), which the sealant is expected to take up. The owner expects it
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

**Every captured start since, read 15/10/2026** (*the owner's question*;
the start rules of `idledips.start_fields()`, each start from rest in
`24`–`38`): **14 starts, `StartDip` 0 in 13 and 15 rpm in one** (`25`,
3/10), cold at 9.8–17 °C of coolant and warm alike. Crank to first firing
0.69–0.90 s, and **1.18–1.38 s on four cold mornings** (`27`, `30`, `31`,
`35`, coolant 9.8–15.8 °C) against 0.76–0.80 s on three others as cold
(`25`, `32`, `33`) — a spread, not a trend, and every one of them caught
cleanly. The owner's account agrees: no dip worth the name since the
injectors (*owner*). Nothing here reopens S7.

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

**15/10/2026, the hardest drive yet** (*owner*, the MFD in, no capture, no
VCDS): motorway in 6th at full throttle, then **about 10 minutes held at
~5000 rpm** — where the lamp used to flash and 014 to count (`refuted.md`
C4) — with **no lamp**; full-throttle pulls in the lower gears, and **2nd
to the limiter, which is at 6500 rpm**, not 6000 as the owner had
assumed. "Runs like butter, behaves like a healthy naturally aspirated
engine" (*owner*). **The owner's reading: there is no lack of breath at
the top.** S8 stays closed, now on his own test rather than in part. On
the remap still (`plan.md` item 5a writes the original map back on
22/10), so it says nothing yet about the stock map.

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
value. The explanation is in `refuted.md` C2: the old MAF over-read —
**on that morning**; whether it did before August is not known, and with
the loop in control the trims kept the mixture at λ = 1 (C2, *11/10*).

**A possible cause of the over-reading — the cracked airbox** (*added at
the owner's decision*, 12/10/2026; `vehicle-history.md`, the air filter
row; `photos/airbox-crack-2026-10-12-sealed.jpg`). The airbox was found
cracked on its clean side, ahead of the MAF, and sealed. Air through the
crack was metered, so it cannot have moved the mixture itself; but it
was unfiltered, and dust on a hot-film MAF's sensing element is a known
way for one to drift (*general*). **How old the crack is is not known**,
and the old MAF was not inspected for dust, so this is a candidate and
nothing more. It bears on the new MAF too: from 12/10 it breathes
filtered air only.

**A second way it could have acted, on the new MAF too: the flow across
the sensor** (*reasoned*, 12/10/2026, at the owner's question; sealed
inside and then outside the same day). A hot-film MAF samples the
stream through its own channel, not the whole duct — which is why its
orientation mattered (below). Air entering through a crack just ahead of
the outlet can skew the velocity profile there, so the sensor reads a
few per cent more or less than the engine draws, and at idle, ~3 g/s, a
small skew is a large share. **Reading high**, the ECU computes more
load: more modelled torque (0x280 b7), more injection, which the lambda
loop then takes away (a negative idle cell in 032), and its timing from
a higher-load cell. **12/10 fits all three**: the lowest b7 and
injection time at a warm idle on record, and 032's idle cell at 0.0
against −2.3 % on 9/10 (S1, *12/10*). How it could make dips: an error
that varies with the intake's pulsation is one the slow lambda loop
cannot follow, so each charge trim of the idle governor would move the
mixture for a moment — and the dips do follow those trims, with the loop
on its lean swing (S1, *What comes before a dip*). **Confounded**: the
old element's pleats were bent over at one end (`vehicle-history.md`),
which also shapes the flow to the MAF, and it was changed the same day.
The owner's other thought, warmer engine-bay air through the crack, is
mass the MAF measures, so not the mixture; a warmer charge only leans
toward knock and opens the throttle a touch — the weakest of the three
at idle.

*What would confirm or refute it, at no cost:* **003's air at a warm
idle** below the 3.08–3.12 g/s of 9/10 and 10/10 at the same idle
(logged from now on wherever there is idle, `plan.md`); b7 and the
injection time staying as low, and `IdleHealth` as calm, on the next
drives; 032's idle cell staying near zero. All of it reverting means
12/10 was chance or weather, and this goes to `refuted.md`.

**How sealed it was on 12/10** (*owner*): the inside layer went on about
30 minutes before the start, thin and still soft through the session;
the outside layer only after the engine was off. A soft sealant still
fills a crack against the airbox's slight depression (*reasoned*), so
12/10 was read with the crack mostly closed. **From the next start it is
sealed twice and cured** (both layers cured, *owner*, 12/10/2026) —
so if the airbox matters, the next warm idles
should read at least as calm as 12/10; calmer still would point at it
more strongly, rougher again would point away from it.

**If the data says the sealing helped** (*owner's decision*,
12/10/2026): the airbox comes out whole, is inspected for any other
crack, and is sealed again properly. **A new one is not bought**: none
is to be had new (*owner*, searched 12/10/2026), and a used one is not
wanted. **The vacuum gauge cannot answer this**: it reads the manifold
behind the throttle, and air through the airbox passes the throttle like
the rest; a metering error moves the fuel and the timing, not the
needle by anything readable (*reasoned*).

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
97–100 °C of oil: a few minutes of `IdleHealth` as the before-value, and H9
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
band at 96–100 °C of oil, loads off; the after-reading is taken the same way.
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
above 77 °C, medians over bins of 500 rpm and 10 counts of b5 with at
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

**After step 1b, 4/10/2026: the joint dry** at the stop at 64–71 °C and
after the hot end of session A (*owner*), with the right gasket, Elring
`915.653`. Smoke at the back was old oil from the 3/10 leak burning off
(*owner*). **The re-check of the outer nuts after a few hundred km stays**
(`plan.md`, *Standing items*); S10 closes with it.

**The re-check, 12/10/2026** (*owner*): the nuts had loosened — some
took about 90° to bring back, some a full turn — and all eight were
tightened with the plenum on. The gasket settling, as expected; no oil
seen. The standing item stays for the next few hundred km. Not an idle
fault: the calmer idle of 12/10 (S1) was read before the nuts were
tightened, and the crankcase path is settled against for the idle
(H9, `refuted.md` A15).

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

**Closed 12/10/2026 and reopened 14/10/2026, both at the owner's
decision.** Closed when it had not been heard since 10/10 and there was
no smoke at the engine; the owner then read it as the valve cover or the
breather. **Heard again at the back on 14/10** (*owner*), on the cold
start with the vacuum gauge teed in at the top of the tee by the
runners, on the throttle's vacuum line (*owner*; *this read "into the
fuel pressure regulator's hose"*), and every hose of 12/10 new; his reading is that it is the same
hiss. The tee and the gauge's own fitting were in the line that day;
**he heard it on a start without them too** (below), so it is not
theirs. The gauge on the same two
starts read steady and rising a little off idle (H3, *The vacuum gauge*),
which no large leak behind the throttle does.

**Placed, roughly, 14/10/2026** (*owner*): **on the right side of the
engine, perhaps near the throttle**, and only with his head right by
the hoses and the throttle — nothing he can hear from further off, or
while driving. **His own reading: it may be normal** — the idle's air
passing the nearly shut throttle plate under manifold vacuum, which
every throttled engine makes (*general*) — and he has never listened
to a healthy engine this close, so he cannot tell. **Kept open at his
decision**, with that note; no test is planned for it. **Heard without the gauge too, 14/10/2026** (*owner*), so it is not
the tester's fitting; and **not at the front, where the tee by the
runners sits**, but further back: **behind the throttle, at the intake
hose from the MAF to the throttle** (`1C0 129 684`, the one original
hose left on the breather's line, which could not be had new), **or
the throttle itself**. *Claude had suggested the same evening that the
tester's tee, fitted at the tee by the runners, might be the hiss; the
owner put it right.* **Moving the intake hose and covering places by
hand at random left the sound unchanged** (*owner*, 14/10/2026). A
leak at a joint usually changes when the joint is flexed or the place
covered (*general*), so this leans away from the hose and its joints
and towards the throttle's own air or something the hand did not
reach — weakly: a random search can miss the spot.

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

### S14. Bangs from the exhaust on a downshift without a blip — reopened 15/10/2026

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

**Reopened 15/10/2026** (*owner's decision*). On the drives of 15/10,
downshifting without a blip, **the burble is back**: **not every time,
and much quieter** than before 9/10, which the owner puts down to the
joint behind the converter being tight (S6, shimmed 12/10 and still
sound, *owner*). So it **outlived the resealed joint**: that joint
was at most what fed the air or carried the sound, not its source, and
the closing argument of 10/10 — gone with the joint while S3 stayed —
no longer holds. Back in every fit table, as judged on 4/10 (*The open
hypotheses*). The same day the first can of inlet-valve cleaner went
into the tank with 100-octane fuel (`plan.md` item 5), so the timing
cannot be put on either; and the fuel cut on the overrun reads as it
did on 9–12/10 (`coastscan.py` on `35`–`37`: injectors shut 0.8–1.6 s
after the lift, fuel back at 1,300–2,400 rpm). The test above is still
the one that would read it, and still not scheduled.

### S15. A constant sputtering from the exhaust near the engine — closed 12/10/2026

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

**The tailpipe test cold, 12/10/2026: no leak heard** (*owner*, from his
recordings by the manifold and under the car by the front pipe; Claude
cannot hear them): no hiss or puff at any of ten closures, only the
exhaust being throttled. Cold only, so the warm test is what is left
(`plan.md` item 7, H2).

**Closed 12/10/2026, at the owner's decision**: since the joint behind
the converter was shimmed and remade that day (S6), **the sputter is not
heard at all** (*owner*). His reading is that it was that joint all
along — still loose after 9/10, when the noise it had drowned first
appeared. *This entry, and S15 ↔ S6 below, used to say the joint behind
the converter could not be S15's source*; the owner's ear on the car
outranks that. If it is heard again, it reopens (*owner*). Out of every
fit table from today.

### S16. A tick in neutral, cold, with the clutch pedal up

*Owner-heard, 12/10/2026; added at the owner's decision, **not to be
pursued**.* A **regular ticking** at a cold idle in neutral with the
clutch pedal **up**; **gone with the pedal down** (*owner*; on his phone
video, which Claude cannot hear). With the pedal down the gearbox input
shaft stops, so it is on the gearbox side of the clutch — gear rattle in
neutral, the input shaft's bearing or the clutch disc's springs, louder
on cold gearbox oil (*general*, not checked for this car).

**It is not the idle's fault**: the same minutes graded the idle with
the pedal up and down, and pedal up was not rougher (H12, test 1). Out
of the fit tables for that reason.

### S17. A new exhaust sound, from a new place

*Owner-heard, 15/10/2026; added as a symptom at the owner's decision.*
**A sound not heard before**, different from S2's puff, S14's burble,
S15's sputter and S11's hiss, and **from another place** (*owner*);
his guess is **the joint at the exhaust manifold**, not the one behind
the converter, which he reads as sound. What it is like, when it is
heard and exactly where are **not yet known**: the owner looks under the
car. Until then it is **out of the fit tables** (*The open
hypotheses* says why); if it is at the manifold or its joint, it is in
H2's zone, ahead of the front probe, which is where a leak would also
bear on the mixture (H2) and where S15 was once placed.

*Owner, 15/10/2026, later:* **only at certain engine speeds, almost
like a resonance — at about 2200 rpm** at the moment. It **could be
the joint he remade** behind the converter (S6), though to him it
sounds **closer to the engine**. *General, not checked on this car:* a
sound tied to one engine speed is a part brought to vibrate at that
frequency — a heat shield, a hanger, a clamp or a joint not quite
tight — whereas a gas leak blows at every speed and grows with load. So
it now reads as **mechanical rather than a leak**, which bears on no
hypothesis about the idle; whether it comes with engine speed alone (in
neutral, standing) or with road speed and load is what would place it.

### S18. Cylinder 3 dropped out, cold, with a tick at camshaft rate — 18/10/2026

*Owner-reported, 18/10/2026; added at the owner's decision.* On a short,
gentle drive with the engine still cold (`IdleHealth` about 90–100 on
the display), the engine **wavered harder than its usual dips and ran on
three cylinders for a while**, and a **tick** started that followed engine
speed. A little throttle at idle brought the fourth cylinder back; the
tick stayed. Engine switched off.

- **The ECU named the cylinder for the first time**: VCDS fault memory
  `16684` **P0300** (random/multiple) and `16687` **P0303** (cylinder 3),
  both `35-00`, read at the roadside. This ECU has no per-cylinder
  counters (`vcds.md`: no 015/016) and **keeps no freeze frame**
  (*owner*), so the codes say *which* and not *when*. Cylinder 3 is one of
  the two slots the dips keep to (*One cylinder or two*).
- **The tick, off the owner's phone video** (15 s, filmed at the intake
  manifold; Claude cannot hear it, so this is the audio analysed, not
  listened to): a sharp click in the 1.5–15 kHz band repeating **every
  0.15 s at an idle of about 800 rpm — once per 720°, camshaft rate, one
  event per cycle, not four** — quickening to 0.07–0.09 s when the
  throttle was opened. The 20–300 Hz band in the same seconds shows four
  even firings (0.038 s), so the click went on with all four firing.
  **Its source is not placed by the audio**: one valve or lifter, one
  port's exhaust leak and the injector nearest the phone would all click
  once per cycle; the owner heard it as new.
  Re-analysed off the same video on the laptop, the result is the same:
  the envelope repeats every **0.149–0.154 s** while the low band fires
  every **0.037–0.039 s** at idle, four firings to a click. Revved, it
  is 0.074–0.092 s against 0.020–0.022 s, still about four to one
  (`photos/tick-2026-10-18-cold-spectrogram.png`). The step in the
  spectrogram at 3.7 s is the phone changing its audio processing, not
  the engine. The video is not in the repository: it is 23 MB and
  carries the phone's GPS position.
- **Not S16**: the clutch pedal down did not change it (*owner*), and S16
  is on the gearbox side and goes with the pedal.
- **Oil 1–2 mm above the maximum** on the dipstick (*owner*, topped up
  recently): not low, so not a starved lifter.
- **The oil looks darker than its age would suggest** (*owner*,
  18/10/2026; in since 6/2026). It is not a symptom of its own. Read
  as (*general*): the cleaner and the hard driving loosen carbon on
  the oil side too, and the oil's detergents hold it in suspension,
  finer than the filter catches. It would become one if the oil
  thickened, smelled of fuel, or **its level rose on the dipstick**,
  which would be fuel in the oil. The level is watched from 1–2 mm
  over the maximum.
- **Then**: on the drive on, the tick stopped at times, and **cylinder 3
  dropped out again with the lamp flashing**. Engine off; **after a
  restart all four ran and the tick was gone**, and stayed gone through a
  longer gentle drive. `IdleHealth` at a warm stop **60–70 with the A/C
  on**, about where it sat before (*owner*). VCDS logged 014/001/003 on
  that drive (to be read).
- **The afternoon, warm** (*owner*, and
  `vcds-s18-home-014-001-003.csv`): the fault memory read before the
  drive home held **P0300 and P0303 twice each, both `35-10`,
  sporadic**. It was cleared and the drive (about 30 minutes) stored
  nothing. **The tick started a few minutes after the start, went on
  for a few minutes and stopped by itself**; when exactly is not
  known, because it is hard to hear on the move. 014 shows **two
  bursts warm under part load**, coolant 91–94 °C: about 2.5 min in, at
  1720 rpm and 41 % load just after a gearchange, **154 → 258 → 270**,
  with lambda control going to +7 and +12.5 %; and about 8 min in, at a
  steady 2960 rpm and 41 %, **93 → 351**, with lambda at +5.5 %. Each
  lasted a few seconds. **In the sixteen earlier 014 logs, the counter
  never read above 72 above 1200 rpm**, and mostly 24–36. Neither burst
  can be put to a cylinder (no 015/016), and **lining them up with the
  tick is the owner's "a few minutes after the start", not a clock**.
  The idle on the same drive read 12–72 in twelves, as always.
  `IdleHealth` at a warm stop, oil 101 °C, no loads: **mostly 80–90, lowest about 68**.
  **Throttle did not quieten the tick** on either occasion, the morning
  or the afternoon; it only quickened, as the video shows. **It stopped
  by itself**, not with a blip, a restart or the temperature (*owner*,
  18/10). **By ear it seemed to come from under the valve cover rather
  than from the injectors at the front**, though not certainly
  (*owner*, 18/10); a valve cover resonates, and an ear places sound
  poorly in an engine bay. **Dry that day**, no rain or fog
  (*owner*).
  **`IdleHealth` while it ticked, warm in the afternoon with the oil
  above 95 °C: about 120–130, at moments 170–180**, against 80–90 at the
  stop without it; **certainly worse with the tick**, the figures a
  glance and not a count.
  **While running on three: at the top of its range** (*owner's
  estimates off the display*, 18/10). So the tick costs the combustion
  and is not only a noise. That fits a valve that does not quite seat,
  where a small leak ticks and burns worse and a larger one misses. It
  fits poorly a lifter with a gap, whose valve still closes.
- **The evening, warm, no tick** (*owner*, 18/10, off the display, no
  capture, no VCDS): a mostly calm drive with a few pulls to 4000 rpm,
  all clean; **no tick heard**, four cylinders throughout, the lamp
  off. At a stop about 18:00, some 15 minutes after the start, oil
  95 °C: **`IdleHealth` about 120 with every load off, lowest about
  98; about 100 with the lights on**. That is the level seen in the
  afternoon only **while it ticked** (120–130), against 80–90 at the
  stop without it and 70–90 on 17/10; 95 °C is the cool end of the band,
  which accounts for some of it and not 30–40. The owner felt the idle
  **more restless than before**. **Recorded under S18 at the owner's
  decision**, not as a change to S1. Read as (*reasoned, not shown*):
  either the idle as a whole got worse, or cylinder 3 still seals or
  burns worse without ticking audibly — the quiet end of a valve that
  does not quite seat. **Fault memory not yet read** for this drive; a
  stored P0303 without the lamp would favour the second.
- **The drive home, 18/10 evening, no tick** (*owner*; capture `39`,
  VCDS 014/001/003 throughout, 33 min): a cold start, pulls under
  4000 rpm and **one full-throttle pull in 2nd to nearly 6000 rpm**;
  **no tick heard and no three-cylinder running**. **Fault memory empty
  before and after** (read by `vcds_log.py` with the engine idling).
  The idle, read off 0x280 (`idledips --roughness --windows 60`, the
  `IdleHealth` scale): **64–78** at a warm stop with the blower on its
  first step and the headlights (oil 98 °C), **82–104** at home with
  every load off (oil 102 °C), which the owner felt as quite restless;
  014 counted through both, to 72 at home. **Recorded under S18 at the
  owner's decision**: a drive without an episode, now including high
  rpm under full load, which is where a valve that does not quite seat
  would be expected to tick first (*reasoned*). It does not close S18 —
  one clean drive cannot — and the idle is S1's, not a new symptom.
- **The morning, 19/10, no tick** (*owner*; no MFD, no capture, no
  VCDS): about 35 minutes, the first 10 at normal speed, so the engine
  was warm, then Prague traffic. **No tick, the lamp off**, the car
  drove normally; the idle by feel **no clear change** from the days
  before, with no figure to put on it. **Recorded under S18 at the
  owner's decision**, as a third drive without an episode. **Fault
  memory not read** after it: the next reading covers this drive too,
  so a code stored then cannot be pinned to one of the two.
- **The afternoon, 19/10, brisk, no tick** (*owner*; MFD in, no
  capture, no VCDS): about 15 minutes of motorway after the town,
  **full throttle again**, as on `39`. **No tick, the lamp off, the
  engine pulled well.** **Recorded under S18 at the owner's decision**,
  the fourth drive without an episode since the afternoon of 18/10.
  **Fault memory not read**; the owner will read it on a later drive
  and expects it empty, and that reading covers both drives of 19/10.
- **The idle since the episodes, the owner's assessment** (19/10):
  **still subjectively worse than before them**; the episodes did
  affect the idle, and so far rather for the worse. The figures with
  every load off agree: about 100 at 101 °C of oil on 19/10 (S1, *Since
  the cleaner*), about 120 and 82–104 on 18/10 evening, against 70–90
  on 17/10 and 80–90 on 18/10 afternoon without a tick. **Recorded under
  S18 at the owner's decision**, not as a change to S1. It does not say
  what the episodes did, only that the idle has not come back from them.
- **The drive home, 19/10 evening, no tick** (*owner*; MFD in, no
  capture, no VCDS): a few pulls, nothing big, in a queue of traffic.
  **No tick**; the idle **certainly less steady than before the
  episodes** (*owner*). At a warm stop, oil 100 °C, lights and the
  blower on its first step: **`IdleHealth` about 100–110, at moments
  towards 120** — no better than the afternoon's every load off
  (S1, *Since the cleaner*). **Recorded under S18 at the owner's
  decision**, the fifth drive without an episode. Fault memory not
  read; the next reading covers all three drives of 19/10.
- **Fault memory empty** (*owner*, 19/10 evening, VCDS 01, before the
  plenum came off): nothing stored over the three drives of 19/10.
- **The look inside, 19–20/10** (*owner*, borescope; `idle-log.md`):
  **cylinder 3's exhaust valve carries light patches where a layer of
  deposit has come away**, and its crown a layer breaking into islands —
  the only cylinder of the four where that is seen. It fits a flake
  under 3's exhaust seat on 18/10 (*Read as*, below) and does not show
  it: where a piece went, and whether the seat now seals, the camera
  cannot say; that stays the leak-down's.
- **Context**: the cleaner's tank (item 5, the PEA can of 15/10) was
  driven to empty on 17/10 and the tank refilled with plain fuel; this
  was the next cold start but one. **The drives of the days before were
  the hardest this car has had in the owner's hands**, on purpose, so
  that the cleaner would loosen as much deposit as it could (*owner*).

**Read as** (*reasoned, not shown*): something on cylinder 3 that did not
let it seal or fire for a while and then let go — **a flake of deposit
under valve 3's seat** after a tank of cleaner, or **a valve or hydraulic
lifter on 3** that hung and recovered. **Two more fit both the tick and
the misfire** (*reasoned, 18/10*):
- **Injector 3.** Each injector clicks once per cycle (sequential
  injection), and the phone was at the manifold beside them. A pintle
  held by a loosened piece of deposit clicks differently and sprays
  badly, so the cylinder misses. The cleaner fits it as well as it fits
  a flake. Against: the injectors are new, 23/9. **Weak for the tick**
  (*reasoned, 18/10*): a clogged injector sprays badly but clicks as
  every injector does, and a stuck one would go quieter, not louder;
  and one that starved 3 would drop it for as long as it ticked, where
  the video's tick went on with all four firing. The owner's ear put
  the sound under the cover, not at the injectors.
- **A spark arcing on 3** (lead, boot or coil tower; H4, H15). The coil
  fires 2 and 3 together every revolution. Only the compression
  spark needs a high voltage, so only that one would find a way to
  earth: **once per cycle**, and the cylinder misses because the spark
  went elsewhere. It would come and go with damp and load. Against: the
  video's tick went on with all four firing, though a partial arc can
  do that. *This said, until 18/10, that an electrical cause "does not
  click at camshaft rate unless it arcs", as if that were unlikely. An
  arc would click at exactly that rate.*
- **How a valve that does not seat can tick** (*reasoned*): gas at
  compression and combustion pressure jets through the gap past the
  seat once per cycle, as a manifold leak does, and a valve closing on
  a hard piece of carbon knocks on it. A small gap leaks and ticks
  while the cylinder still fires, which fits the video; a larger one
  drops it, which fits the misfires.
- **Deposit and lifter at once** (*reasoned*): carbon from the chamber
  cannot reach a lifter, which sits in oil behind the stem seal. But
  the oil side has its own deposits, varnish and sludge, and a little
  of the PEA reaches the oil (*general*), so a loosened particle in a
  lifter's oil feed could hang it. That is H1 caused the way H13 is,
  under the cover where the owner heard it.
- An **exhaust port leak on 3** ticks once per cycle and seals as it
  warms (*general*), but does not drop the cylinder.

**What tells them apart is when it happens** (*general, not checked on
this car*): deposits after hard driving or the cleaner, cold or warm
alike, fading over tanks; a lifter with the oil, after standing or at
a hot idle, quiet with a blip, day after day; an arc with the damp and
the load; a burnt valve getting worse, under load, with 3's compression
falling. Tests while it ticks (a screwdriver as a stethoscope, injector
3's connector off, a look in the dark) would place it, and **were
dropped by the owner** (18/10): naming the cylinder would not change the
next step (`plan.md` item 5).
**Both 014 bursts on 18/10 were warm and under load**, which fits the
flake, the injector or the arc, and the lifter poorly. **The afternoon's return leans towards the flake** (*the owner's
reading too: the tick was new and came with the cleaner*). PEA cleans
the combustion chamber as well as the intake valve. What it loosens
leaves through the exhaust valve, and a flake caught under that seat
would let the cylinder leak and miss. It would also puff out of the
port once per cycle, which could be the tick, and both would go when
the flake breaks up. **More flakes coming loose explains the return**;
a lifter explains it as well and is not ruled out. *General, not
checked on this car.* **The owner's assessment** (18/10): nothing is
certain, but the deposit hypothesis is now the most likely; the tick
was new, and it came with the cleaner and with the hardest driving. **What settles it**: if it keeps coming back,
compression and a leak-down on 3 against the others, ideally while it
ticks, then a borescope through 3's plug hole at the valve seats. **The
lamp flashing means ease off**: that is the misfire rate that damages
the converter (`vcds.md`).

**Why the idle got worse — reasoned, 19/10/2026** (*the owner's
question*; nothing here is measured beyond the readings it cites). The
warm idle with loads off, or the lights only, read off the display:
50–61 on 12/10, about 54 on 15/10 (the can in), 50–70 on 16/10, 70–90
on 17/10, 80–90 on 18/10 afternoon without a tick, about 120 and
82–104 (`39`) on 18/10 evening, about 100 on 19/10. **With every load
on it has hardly moved**: about 40 at its lowest on 17/10, mostly about
50 on 19/10 (S1, *Since the cleaner*). Three things follow:
1. **The rise began about 16–17/10, with the cleaner and the hard
   driving, not with the episodes**, which fall in the middle of it.
   Glances off the display, but about 55 to about 100 is twice what
   one pair can show.
2. **It is worse only at a small charge**: the shape of S1 itself, a
   margin that more air and fuel cover.
3. **`39`, the first capture after the episodes, has its dips more
   concentrated than any pool before it**, top two 77 % against 61–67 %
   (*The dips keep to one slot*): one capture, 70 dips, slots not named
   — but it points to one pair of cylinders getting worse rather than
   to something acting on all four.

The candidates, in order of fit (*reasoned, not shown*):
- **Deposit the cleaner loosened and has not yet burnt off (H13).** PEA
  soaks and softens carbon before driving burns or blows it out
  (*general*), so for a while the surfaces are uneven and come away in
  pieces. A piece under valve 3's seat is the episodes; what is left, a
  valve that nearly seats, is the idle — a leak costs most at a small
  charge and vanishes under load. Fits 1, 2 and 3. **If so it should
  improve over a tank or two**: a prediction, not yet an observation.
- **Injector 3 holding a loosened piece.** A poor spray matters most at
  the shortest pulse, which is the idle, and hides in a long pulse
  under load. Fits 2 and 3. Against: the injectors are new (23/9), and
  the cleaner works to clean nozzles.
- **An adaptation learnt during the misfires.** A misfire sends unburnt
  oxygen past the probe, which reads lean, and the ECU richens; if that
  went into the idle's additive mixture adaptation, or into the idle
  air in 055, it acts only at a small charge. Fits 2, and it is the one
  candidate that can be read at once. Against: it acts on all four,
  which fits 3 poorly, and the rise began before the episodes. **Read
  19/10, engine off, against** (`photos/vcds-032-055-2026-10-19-before-6b.jpg`):
  032 **−3.1 / +5.5 %**, inside its own history (−3.1 / +4.7 on 24/9,
  −2.3 / +5.5 on 9/10, 0.0 / +2.3 on 12/10, −4.7 / +4.7 on 15/10), and
  the idle cell takes fuel away where a misfire-learnt trim would add
  it; 055's learnt idle air **−1.27 g/s** against −1.18 to −1.21 on
  12/10, inside ±1.50. Nothing was learnt away by the episodes.
- **A lifter or valve (H1).** A valve that seats late hurts the idle
  most, which fits 2; but not why it began with the cleaner, nor why
  the tick has stayed away on five drives.
- **Unlikely**: the converter damaged by the flashing lamp, which would
  cost power at the top first, and that is fine; the ignition, where
  nothing changed and the timing follows the cleaner.

**What separates them, cheapest first**: 032 and 055 against their
baselines (the adaptation in or out); the borescope this week (carbon
on 3 against the others, flaking or patchy for H13; not sealing); the
injector cut on 22/10, which names the cylinders — the adaptations
start again from nothing that day, since the ECU comes out of the car
and only its permanent supply holds them (*owner*) — though the map goes
back the same day, so a change in the idle then cannot be given to one
cause alone.

### Other — not symptoms, but they touch this file

**Oil temperature.** 0x420's `OilTemp` is `raw − 60` °C, the
cluster's `Kombi_2` as opendbc defines it (`docs/firmware/open.md`
question 10). It matters here because S1 depends on oil temperature and
every `IdleHealth` comparison is made at a matched one. Whether the sender
reads right is question 10's: a few degrees high at a cold soak, unknown
warm. A bias moves both sides of every comparison alike, so the
comparisons hold whatever the absolute figures turn out to be.

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
  control. **Written down as H14 on 16/10/2026** (*owner's request*), with
  its fit table and what to read on 22/10, so that a cure by the stock map
  is on record as a candidate beforehand.
- **Postponed 20/10** (*owner*): the map is not written back on 22/10;
  the tuner emails both files, the original and the remap, to be
  compared first, privately (`plan.md` 5a).
  **What a comparison can and cannot do** (*decided*, 20/10, after a
  search): the ECU is a Bosch M5.9.2, software `1037352075` V04, a
  256 KB flash (`vcds.md`), and **no map definition for it is public**.
  So: (1) the two files are diffed — how many bytes, in how many
  blocks; (2) tables are found by shape — 8-bit maps beside rising axes
  of engine speed and load, the method tuners describe for other
  Motronics, written as a guess where it is one; (3) **the idle cells of
  the ignition map are read against what the bus measured**, the spark
  after TDC in August and 1.5–3.8° BTDC since 24/9 (`idle-log.md`,
  17/10, `tools/idleadvance.py`): a remap that touched them is H14 for
  the idle; one confined to the top of the range, as the tuner said,
  weakens it. To ask the tuner: the whole 256 KB flash, and which
  tables he changed. A vendor sells a stock file for exactly
  `1037352075`, which would show whether the tuner's *original* is
  stock — the owner's call, and never in this repository either.
- **How it closes: return the ECU to standard** (*owner's decision*,
  12/10/2026; `plan.md` item 5a). **The tuner kept the original map and
  writes it back on 22/10/2026** (*owner*, 13/10). Then:
  1. `IdleHealth` at a matched oil temperature and a 020 + 026 neutral log,
     before and after. **The cleaner goes in some days before the map**
     (*owner's decision*, 13/10/2026: the idle first, the reason second),
     so the difference is the map plus the cleaner's first days, and the
     adaptations start from zero with the ECU out — a measurement of
     *both*, not of the remap alone;
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
| S1 ↔ S3 | **the same events, but 014 is switched** | aligned three times, p ≤ 0.023; **re-read 16/10 over eleven sessions: half the rises sit on a dip in the 1.5 s before, against 22 % by chance; a third of the dips get a rise; and rises a minute do not follow `IdleHealth` (Spearman 0.20)**, nor did 014 follow the idle when the A/C went off (*owner*, 16/10). Both are crank speed, so partly one signal read twice (S3, *The events are the S1 dips*) |
| S1/S3 ↔ S9 | **strong** | the MAF swap halved the dips at every oil temperature (−51 to −65 %). An over-reading MAF was causing some of the stumbles; the rest is the residual fault |
| S1/S3 ↔ oil temperature | **strong; the two differ** (*re-read 9/10/2026*) | **S1** (engine speed) roughest cold and calmer as the oil warms, in every session since 24/9. **S3** (014): near zero cold — the counter's own blind spot, since engine speed is worst there; on fresh adaptations a sharp peak in the middle band and zero hot; **on settled ones flatter** — 6–16 a minute from ~57 °C up, about half as many at 97–111 °C as at 77–95 (`29`, `30`). *This read "non-monotonic, worst at ~71–85 °C, on every drive" for both* |
| S4 ↔ S5 | **very likely one thing** | same cylinder window, same engine speeds, and S5 needs no combustion. Knock control retards cylinder 4 because it hears S5's noise |
| S4/S5 ↔ S1/S3 | **none measured** | no retard and no 026 signal at idle, in any log. Only a common cause could link them |
| S2 ↔ S3 | **likely: heard with the dips by the owner on 12/10/2026; never aligned with a recording** | the owner takes S2 for S14's smaller twin, a misfire's charge going off in the exhaust (S2, 4/10/2026); on 12/10 he heard the puffs come with the engine-speed dips. A leak ahead of the probe would puff too (H2) |
| S2 ↔ S6 | **not S6**: **S6 closed 12/10/2026**, and S2 was heard that day | the puff outlived the resealed joint, so it did not come from it. A leak ahead of the probes remains possible (H2) |
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
| S14 ↔ S6 | **not its source**: **S14 reopened 15/10/2026** with the joint behind the converter tight (S6 closed 12/10), quieter — the joint fed or carried it at most; *this row read "possible; S14 stays closed until bangs return"* | a leaky joint draws air in and feeds an afterburn; behind both probes, so it cannot cause the misfire. Bangs that go on unchanged after the reseal were not fed by it |
| S15 ↔ S2 | **possible** | a leak ahead of the probe can puff now and then as well as sputter all the time (H2). S2 is occasional and S15 constant, so they are kept apart |
| S15 ↔ S11 | **possible, never compared** | an exhaust leak at the head can hiss as well as sputter; whether the owner's hiss and the sputter are one sound has not been asked |
| S15 ↔ S6 | **one source, by the owner's reading; S15 closed 12/10/2026** | S15 went when S6's joint was remade on 12/10 (*owner*). *This row said "masking only … behind the converter, it cannot be S15's source"* |
| S15 ↔ S1/S3 | **untested** | only through H2: air drawn in ahead of the front probe leans its reading and the mixture follows. 033 and 032 have not shown the positive correction that would need (S3) |
| S17 ↔ S6 | **possible** (*owner*, 15/10/2026) | a resonance at about 2200 rpm could be the joint behind the converter, remade 12/10, though it sounds closer to the engine |
| S17 ↔ anything else | **not yet placed** (added 15/10/2026) | a sound at one engine speed reads as a part vibrating rather than a leak (*general*), so no link to the idle is claimed; at the manifold's joint it would be in H2's zone |
| S13 ↔ S1 | **weak** | the one link was an adaptation that never completes, leaving the idle on unfinished values (H8); **refuted on the old part 29/9** — 098 completed and the 20 s routine ran unchanged after it (S13). **Closed 2/10/2026**: the new part does the same |

**So there are two separate clusters**, and they are worked separately below:
**the idle** (S1, S2, S3; S15, closed 12/10; S14, on the overrun, reopened 15/10) and **the cylinder 4 window** (S4, S5). S7, S8, S9
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
each for a stated reason: **S6** (closed 12/10/2026, after closing 9/10
and reopening 10/10: the joint behind both probes; never a column, being
acoustic and behind the probes, so neither closing nor reopening it
moves a table — the part of it that bears on the idle is H2's), **S16**
(added 12/10/2026: a tick on the gearbox side of the clutch, shown that
day to have no bearing on the idle — H12 test 1), **S7** (closed), **S8**
(closed 4/10/2026), **S9** (closed 4/10/2026: fixed by the MAF),
**S10** (closed 4/10/2026: the cover joint, found and repaired),
**S12** (closed 4/10/2026: withdrawn by the owner as mechanical play),
**S13** (closed 2/10/2026: the new throttle behaves the same),
**S17** (added 15/10/2026: a new exhaust sound, only at about 2200 rpm
like a resonance, not yet placed — read as a part vibrating rather than
a leak, so it bears on no hypothesis about the idle; it becomes a column
if it turns out to be a leak). S12 and S13 were added on 28/9/2026: **S12**, the tip-in
hesitation, fits a lean tip-in (H3/H9, H7), a moment of knock retard (H5)
and weak spark under sudden load (H4); **S13**, the throttle's routine, was
H8's alone.

**S14 was added on 4/10/2026** and judged the same way for every row: a
misfire at the thinnest charge (H3 ✔, H1/H4 ~, and H10 ~ until it closed 9/10), air ahead of the
converter to burn it in (H2 ✔), or fuel nobody commanded (H7 ~, the
weak reading: every part that could pass it is new). H0 ✘: the owner's other cars do not do
it, and it follows the misfire episodes. H5, H8 and the closed H9 say
nothing about it. **Taken out when it closed on 10/10/2026 and
back on 15/10/2026, when it reopened**, with the same judgement. H11
and H12 came after 4/10 and are judged now, as each was for S2: H11 ~
(a mixture a few per cent off fails the thinnest charge first) and H12
✘ (play puts nothing into the exhaust).

**S18 was added on 18/10/2026** (cylinder 3 out, cold, with a tick at
camshaft rate) and judged for every row: one cylinder's valve or lifter
(H1 ✔) or a flake of deposit under its seat after the cleaner's tank
(H13 ✔); an electrical drop-out on one cylinder (H4, H15 ~) or one
injector (H7 ~), neither of which clicks at camshaft rate unless it
arcs or is the injector itself; a leak at port 3 ticks once per cycle
but does not take the cylinder out (H2 ~). H0, H3, H8, H11, H12 and H14
✘: each acts on all four alike, or (H12) the clutch did not change it
and the ECU named a cylinder. H5 and the closed H9 say nothing about it.

### H0. The idle is normal for this engine — and there is no fault to find

**The one hypothesis nobody has been able to test.** An AQY with 26 years on
it might simply idle like this, and every number above might be its normal
state.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ✘ | — | ~ | — | ✘ | ✘ |

- **Against:** 014 reads **12–120 against VW's own 0–5**. The old converter
  burned through, which needs raw fuel in it. The owner feels it.
- **Against, 17/10/2026, weaker than it looks** (*the owner's question*:
  does the pair not refute it?). The dips sit two thirds on two
  neighbours, **3 and 4** where named (*One cylinder or two*). That alone
  does not refute H0: no engine fires its four cylinders alike — the
  plenum feeds its runners unevenly and the end cylinders run differently
  (*general*) — so whatever roughness a healthy AQY has would also gather
  on its weakest cylinders, and no healthy AQY has been recorded to say
  which (test 1). **What it adds against H0 is the name**: the pair holds
  cylinder 4, the one the 2019 scan stored as P0304 and the one whose
  knock window is noisy (S4, S5) — the dips sit where a stored misfire
  and a second anomaly already sat, which normal variation has no reason
  to do. Not refuted; down, and it stays below every per-cylinder
  candidate.
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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ✔ | ✔ | — | ~ | ✔ |

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
  be — engine speed is calmest hot, and 014 at 97–111 °C counts about half
  what it does at 77–95 (*re-read 9/10/2026*; this read "S1 is worst at
  71–85 °C and eases when hot"). The S5 excess switches on above ~2300 rpm and
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
  before 2017 is not known. **Moved to H13 on 15/10/2026**, with the
  chamber and the ring lands, on the owner's driving history.

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
**Which valve, and what reaches it** (*the owner's question*,
11/10/2026; *general*). A valve held off its seat **by deposits** is
more often an **inlet** — the back of the inlet valve collects them on a
port-injected engine with a breather feeding oil mist (H1, *Inlet-valve
deposits*) — though flakes of carbon on an **exhaust** seat can do the
same. A **burnt** valve is usually an exhaust one, and the even
12 bar argues against one. A **lifter** that bleeds down can sit under
**any of the eight** valves. **The PEA cleaner** reaches the backs of
the inlet valves and the chamber side of all of them, not a lifter or an
exhaust valve's stem. **The vacuum gauge does not tell inlet from
exhaust**; the warm leak-down does (test 3): air out of the throttle is
an inlet valve, out of the tailpipe an exhaust one.

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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ✔ | ~ | ✘ | ✘ | ✔ | ✔ | ~ |

- **Against, mildly, 10/10/2026** (S1, *What comes before a dip*):
  this hypothesis acts on the mixture through the lambda control, and
  what comes before a dip is the idle governor's trim of the charge,
  not a lean swing of the mixture (as `refuted.md` C5 found for 014).
  Its sounds (S2, S11; S15 closed 12/10) are untouched by this.

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
- ~~**For, 9/10/2026:** S15 — a constant sputter close behind the engine at
  every load~~ — **withdrawn 12/10/2026**: S15 went when the joint
  behind the converter was remade, behind both probes (S15, closed).
  H2 keeps S2 and S11, and no heard leak.
- **Where "ahead of the probe" is, 28/9/2026** (*owner-observed*): the
  front probe sits **on the manifold itself**, and the pipe fitted on 10/9
  starts at the manifold's outlet (`vehicle-history.md`). So the zone this
  hypothesis is about is only the **original manifold, its gasket to the
  head and the probe's boss** — all 26 years old. The outlet flange and its
  new gasket are downstream of the front probe and outside it. (An earlier
  revision counted the new flange gasket *for* this hypothesis.) *Owner, 11/10/2026:* that joint, manifold to
  front pipe, was remade by the garage in the converter work and had
  been before; web reports name it as a trouble spot on these cars. **It
  was S15's candidate, not H2's** (S15 closed 12/10, put down to the
  joint behind the converter instead): behind the probe, so a leak there
  cannot steer the mixture or the misfires, but it can sputter. The
  phone under the front pipe and the photos from below (`plan.md` item
  1) are aimed at it. It fits
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
   hot idle moves a little leaner; `IdleHealth` at 97–100 °C stays in its
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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ✔ | ~ | ✔ | ~ | ✘ | ~ | ✔ | ✘ |

- **For:** the regime is exactly right. A lean cylinder can also knock on a
  tip-in (S4). Several of the forum cases were a breather hose. The idle is
  better the more air goes through the engine (S1, *load at idle*), which
  dilutes a fixed leak.
- **The vacuum gauge, 14/10/2026, against a large leak** (`plan.md` step 3
  item 2; `33`, `34`, the owner's video of `34`): teed in at the top of
  the tee by the runners, on the throttle's vacuum line (*owner*; *this
  read "into the fuel pressure regulator's hose"*; a point that may read
  a little under the manifold's own vacuum, `idle-log.md` 14/10), the
  needle sat **steady** at idle, **about
  18–19 inHg** once its zero is taken from the engine off, inside the
  dial's green band (about 17–22) and above its "late ignition" band
  (the needle sits a quarter-turn off zero at rest; measured off the
  owner's video, ±1½, `idle-log.md`, 14/10; *this read 16–17*), went **a little higher and steady at ~2150 rpm** (20–21½), and on a snap
  dropped, overshot above idle and settled back. A leak behind the
  throttle reads low at idle and recovers off it; this did not. It does
  not rule out a small leak at one runner, which a gauge on the common
  plenum cannot see. Engine part-cold (coolant 16–82 °C across the two
  starts).
  **Two readings off the same session agree** (*checked 14/10/2026*, the
  owner's question whether the needle's slow return after a snap is a
  leak): **the landing after a snap is the car's usual one** — engine
  speed from 1400 rpm to within 30 rpm of idle in 1.8–2.4 s on `34`
  against 2.0–2.6 s at every warm standing release with the pedal
  left at rest on `28`–`32`, before the
  hoses were renewed — which is the ECU easing the throttle shut, not
  an idle that hangs (*reasoned*); the needle's overshoot above idle
  for those seconds is the closed throttle at speed, the healthy
  reading (*general*). And **003's cold air matches the earlier cold
  starts minute by minute** — 6.11, 5.14, 4.03, 3.96 g/s on 14/10
  against 6.25, 4.86, 3.96, 3.96 on 3/10 (`vcds-sessionA-*`) and 5.34,
  4.93, 4.03, 3.89 on 10/10 (`vcds-step4-*`); a leak behind the MAF
  would make it read *less* for the same idle, never more.
- **The vacuum gauge warm, 15/10/2026** (`38`, the owner's 3½ min video;
  oil 93–97 °C, coolant 94–100 °C, the same tee): **steady at idle, about
  19 inHg**, as part-cold; **about 22 at a 15 s hold of ~2500 rpm**,
  steady; **about 22½–23 on each release**, back to idle's in a few
  seconds. **No flick at idle**: none of ~0.1 inHg or more in 78 s of
  film held still (needle measured on every frame, noise 0.1°), and
  none at the seven of `38`'s eight 20-rpm dips that fell in a readable
  stretch (`idle-log.md`, 15/10). The same "steady and normal" row,
  warm: no lifter bleeding down on thin oil and no crack opening hot
  that a gauge on the plenum can see.
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
  in that window, and they were the day before. **So are the hoses**
  (*the owner's thought*, 12/10/2026): since August the intake hose and
  the thin hoses on it were off several times and handled a good deal,
  and hard, porous 1999 rubber that is moved can start to seep where it
  had not. August's 43–48 are 22 s holds, shorter than the device waits
  before it grades (S1), so the comparison is weak; the first start with
  the thin hoses and the breather hose new (`plan.md` item 2) answers it
  better than August can.
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
at for a nick from being forced, then `IdleHealth` at 97–100 °C against
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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ~ | ✔ | — | ~ | ~ |

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

  **Lead 4 at its plug, 12/10/2026** (*owner*, recalling the fitting on
  10/10): of the four new leads, **lead 4's plug end clicked but felt
  the least firm** — pushed as far as it went. Possibly because it was
  the one he had tried the click on before, so worn by the trying; he
  cannot tell. A boot not fully home leaves a gap the spark can jump or
  track across, on one cylinder only (*general*). It is the cylinder
  everything else points at — S4's retard, S5's knock-sensor reading,
  the old plug 4's burnt terminal (1d) — and the dips are back on one
  slot (*Naming the cylinder*, 12/10). **Reseated cold the same day,
  and nothing** (*owner*): all four boots sit alike on their plugs;
  lead 4, pulled and turned a little as it went back on, no longer tends
  to work its way off, and it looks sound. Nothing named — the owner's
  word for it is a red herring.

  **15/10/2026, owner, re-checked by hand:** lead 4's plug end clicks
  audibly, but **it still sits looser than the other three** — it turns
  and gives more freely in the direction of removal by hand, though it
  takes real force to pull off; it does not hold as snugly as the rest.
  So the 12/10 reseat did not make it like the others. *Reasoned:* a
  boot that grips less can leave the spark a path in the damp (above);
  whether it does is this test's question, and the one day of cuts
  (10/10) gave cylinder 4 only 2 of 20 dips — too few to clear it or name
  it (*Naming the cylinder*). A genuine VW lead for cylinder 4 alone is
  the cheap swap if it is ever wanted (*owner's question*, 15/10).

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
borrowing a genuine VW set. **Now its own hypothesis, H15** (17/10/2026).

### H5. Something in the cylinder 4 knock window that is not the engine's combustion (S4 + S5 only)

*17/10/2026*: the idle dips sit on **3 and 4** (*One cylinder or two*),
so "no link between this window and the misfires" no longer holds as
plainly — a noisy lifter or valve on 4 (H1) would be heard in 4's window
and stumble 4 at idle. Not tested; it is why H1 went to the top.

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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| — | — | — | ✔ | ✔ | — | — | — |

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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | — | ~ | ~ |

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

- **A plug washed clean by fuel** (*searched 20/10/2026*, a
  search-engine extract on the AEG/AQY, not read in full): *"#3 was much
  cleaner than all the rest … replaced #3 injector as it was washing
  that plug in fuel"*. **On this car plug 3 is the cleanest of the
  four** (`idle-log.md`, 19–20/10). Weak here: the injectors are new
  (23/9) and injector 3's tip looked clean on the borescope. It is a
  reason more not to read soot on a plug as combustion quality.

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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | — | ~ | — | — | — | — | ✘ |

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

The hot-idle grades (`idledips.py --roughness`, oil ~97–107 °C, loads off)
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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | — | ~ | — | — | ✘ | — | — |

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
  wiring, so no heater is fitted here.* **The connector sits on the
  intake hose just ahead of the throttle**, and **one thinner hose joins
  it**, a little below the breather hose: the one from **a second tee
  right by the head, at the intake runners** (*owner*, 12/10/2026). **The
  injectors' air-shroud supply does not join it**: it has a port of its
  own on the intake hose **just behind the MAF** (*owner*, 12/10/2026;
  `refuted.md` C9). *This bullet used to say that two thinner hoses
  joined the same connector, one of them the shroud supply (owner,
  1/10/2026); corrected by the owner with the hoses in hand.*
  **Could the two thin hoses have been swapped by an earlier hand?**
  (*the owner's question*, 12/10/2026.) Probably not, on three counts
  off the parts themselves: the tee's hose is a moulded VW part
  (`06A 133 374`) with a formed end over its connector, which a plain
  hose pushed on elsewhere would not be; the shroud supply was **clean
  inside** (`refuted.md` C9), where a hose carrying crankcase gas comes
  out oily, as the breather hose did; and the two bores differ, 6 and
  8 mm, so a swap would have meant forcing each onto the other's
  nipple. **The routing also makes sense as built** (*general*, not
  from a VW document for this engine): ahead of the throttle there is
  almost no suction at idle, so a breather needs a second, small path
  to manifold vacuum for its gases to move — which is what the tee's
  hose gives it, from the breather's connector to the throttle's
  vacuum spigot. The injectors' shroud air only needs clean, metered
  air ahead of the plate, which the port behind the MAF gives without
  crankcase oil in it. What would settle it: oil inside the tee's old
  hose (it then carried breather gas, as built). **Pictures of the same
  engine on the web show the same routing** (*owner*, 12/10/2026) —
  other cars, not this one, but they agree; taken as not swapped. That tee (*owner, photographed 1/10/2026*) sits on a
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
  **12/10/2026, the thin hose from the breather's connector to the tee,
  off the car: it leaks** (*owner, photographed*:
  `photos/tee-hose-2026-10-12-*.jpg`). Blown into by mouth with the far
  end stopped, **air certainly escapes**, not strongly; the bend is cut
  across by cracks, and the end over its moulded connector is crazed
  deep; **6 mm inside** (*owner-measured*), with a crack along the connector's edge. White print
  `06A 133 374` (*owner's photo*) — the number this bullet gives the
  elbow, so perhaps one number for the whole line; not settled. *1/10's
  "fine by hand" was wrong for this hose.* **Why it counts more than the
  other hoses of 12/10**: it is on the line this bullet places at
  manifold vacuum. Against it as the dips' cause: it feeds all four
  cylinders alike, and the intake smoked clean on 9/10 (H3) — either the
  crack opens with heat and movement, or the smoke did not reach it.
  **How it leaks, in the owner's reading** (12/10/2026): the cracks
  look like surface damage, and the rubber after nearly thirty years
  reads as **porous** — blown into with the far end stopped, the air
  does not go out as through a hole but **seeps away slowly
  somewhere**, perhaps at the damaged places. A new hose cannot be
  blown through at all. So a slow seep through aged rubber at manifold
  vacuum, not a hole: the kind that draws a little all the time, on all
  four cylinders alike (*reasoned*). It may make no difference at all
  (*owner*).
  Replaced with a plain 6 mm silicone hose and new clamps — the number
  is not to be had (*owner's decision*). **The intake hose MAF to
  throttle, `1C0 129 684`** (*read off the part*;
  `photos/intake-hose-2026-10-12-*.jpg`), whose plastic stub for the
  breather moves in its joint (*owner*, on video, which Claude cannot
  see), **was blown through stub included and leaks nowhere** (*owner*),
  so it stays — no new one to be had short of a VW original the owner
  will not pay for — **the one original hose left on this line**; the
  breather hose, though it holds when blown through, is replaced too
  (*owner's decision*, 12/10/2026; `refuted.md` A15). **The closed
  plastic branch on this hose just behind the MAF**, from which nothing
  leads (*owner*), is by its shape an **intake resonator** — a side
  chamber tuned to damp the intake's pressure pulsation and its noise
  (*general*, not read from any VW document for this part). Hoses sold
  for the same place without it (*owner*, 12/10/2026) are therefore not
  like for like: the MAF was calibrated with the chamber in place, and
  more pulsation at the MAF can move its reading (*general*). Clamps were
  missing at some hose ends. **The plain hose fitted 2/10 from the tee
  up to the throttle's top spigot is 8 mm** (*owner*, 12/10/2026), on
  the tee whose leg to the breather's connector takes the 6 mm hose; if
  the tee's legs are one size, an 8 mm hose sits loose on its leg —
  at manifold vacuum. **Checked at the reassembly, 14/10/2026, and
  sound** (*owner*): the tee's legs are two sizes, **8 mm upward to the
  throttle and 6 mm to the side**, and the 8 mm hose sat tight at both
  ends before the new clips went on. *This read "if the tee's legs are
  one size, an 8 mm hose sits loose on its leg"; they are not.* The
  intake had also smoked clean on 9/10 with that hose already on.
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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | — | ~ | ✘ |

- **Against, mildly, 10/10/2026** (S1, *What comes before a dip*):
  what comes before a dip is less charge at the same mixture, not a
  leaner mixture; a shift of the probes moves the mixture.

S1 and S3 only as a background on all four cylinders — **a few per cent
off λ = 1 does not misfire on its own** (*general*, as under H2); S2 for
surplus fuel burning in the exhaust. S4 and S5 are one cylinder's; S11
(and S15, closed 12/10) are sounds a probe does not make.

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
2. **A wideband sensor as a reference** in the blanked-off boss on the
   new front pipe, which sits **ahead of the converter and behind the
   front probe** (*owner*, 11/10/2026). Its λ against the ECU's
   switching, at idle and under load. **Cheaper and nearer to hand: the
   front probe's own signal** back-probed at its connector into a USB
   oscilloscope (*the owner has one*, 11/10/2026; never used: an
   **LHT00SU1** — two analog channels, ±10 V, 8 bits by its vendors'
   listings, so about 0.08 V a step, enough to see the probe switch and
   when, not a shift of its switching point; whether its software or
   sigrok records minutes at a time is **not established**, a test on
   the desk with a battery first) — a few
   hundred samples a second against VCDS's one, with the capture beside
   it; the scope's high input impedance does not load the signal, and
   the heater's 12 V shares the connector. *Not scheduled.*
3. If either finds a shift: new probes, front first, and 032 read again on
   settled adaptations.

### H12. Driveline play read as misfires — gearbox input shaft, clutch, flywheel, crank pulley

*Added 10/10/2026 at the owner's request, from a lead another assistant
raised; ranked last.* The idea: the dips and 014 are not misfires but
mechanical play in what the crank drives, felt at an unloaded idle where
almost nothing resists the crank, and taken up under load. 014 reads
crank-segment times through G28 (`vcds.md`), so a jolt there would be
counted as readily as a missed firing.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ✘ | ~ | ~ | ~ | — | ✘ | ✘ |

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
  detection works (*Naming the cylinder*); **the puffs come with the
  dips** (S2, 12/10/2026, by ear), and play puts no charge into the
  exhaust. **Compression does not bear on
  it** either way: a cranking test sees neither play nor a flywheel.
  Whether this car has a dual-mass flywheel at all is **not recorded**.

**Tests:**

1. **The clutch minutes** (cold and warm): pedal down takes
   the gearbox input shaft and the clutch disc out of the engine's load.
   Dips and `IdleHealth` the same either way → not that side; clearly
   calmer with the pedal down → it is a lead. The flywheel and the pulley
   turn either way and are not separated by it. **Done 12/10/2026: not
   that side.** `IdleHealth` in 30 s halves, cold: down 145, up 135, down
   145, up 126; warm: down 83 (settling from the blip), up 57, down
   45, up 50, down 58, up 51 (`32`, `idle-log.md`). Pedal up is
   not rougher. The gearbox side has a noise of its own (S16), and it
   does not reach the idle.
2. **The crank pulley's damper, by eye, engine off**: the rubber ring
   between its inner and outer metal rings cracked, bulging or the outer
   ring walking out of line (*general*). Free. **Done 12/10/2026: fine
   by eye** (`idle-log.md`).
3. What the flywheel is, read off the parts catalogue by VIN, if test 1
   or 2 points here.

### H13. Deposits after years of gentle driving — inlet valves, combustion chambers, ring lands

*Added 15/10/2026 at the owner's request.* For at least the nine years
he has had the car, and above all since the full-load misfires of the
old parts, the engine has seldom seen more than 3000 rpm — now and then
4000–4500, never higher — and the owner believes the previous owner drove
it as gently (*owner*). 15/10/2026 was the first hard drive in perhaps ten
or fifteen years. Gentle use builds deposits where hard use burns them
off (*general*): on the backs of the inlet valves, where they soak up
fuel cold and let a valve seal late; in the combustion chamber, where
they hold heat and add compression; on the ring lands, where they stick
a ring. **This was a branch of H1 until 15/10** (*Inlet-valve
deposits*, there); it stands alone now because it reaches beyond the
valves, and because its test is already running.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ✔ | ~ | ✔ | ~ | — | — | ~ | ✔ |

S1 and S3 fully: a margin narrowed by deposits is exactly *a charge one
per cent smaller is enough for a combustion to fail* (S1, *What comes
before a dip*), roughest cold where valve deposits soak up fuel, calmer
under load; and deposits are rarely even, so one cylinder can take more
of the dips than the rest (*The dips keep to one slot*). S2 and S14 as a
misfire's charge going out. S4 weakly: chamber deposits add compression
and hot spots, which knock control answers (*general*). S5 needs no
combustion and S11 is a sound outside the cylinder: neither.

- **For:** the driving history (*owner*, 15/10/2026), which nothing else
  on the list explains and nothing in the repairs has touched; every
  part in the fuel and ignition path is new and 014 still counts; the
  dips follow the charge, not a part (S1); a cylinder ahead of the rest
  without a part that names it.
- **Against:** OMV MaxxMotion 100 since 2017, a premium fuel with a
  detergent package (`vehicle-history.md`; *general*), which works
  against inlet-valve deposits; compression 12 bar and even on all four,
  which a ring stuck by deposits or a valve held off its seat would
  lower; the vacuum gauge steady at idle cold and warm (H3, *The vacuum
  gauge*), against a valve that does not seal.
- **For, a little** (*owner*, recalled 16/10/2026): about 6/2026 every
  start ran on three cylinders until fresh fuel replaced three-year-old
  fuel (`idle-log.md`); unburnt stale fuel in one cylinder is a source of
  exactly the deposits this needs. Which cylinder, no scan was kept.
- **Not against:** the hardest drive yet (15/10) left the warm idle where
  it was (`IdleHealth` about 55 lights-only, `idle-log.md`); one drive
  does not burn off years of deposit, and the cleaner had been in the
  tank half a day.

**Tests:**

1. **The PEA cleaner over the tank** — `plan.md` item 5, under way since
   15/10: `IdleHealth` lights-only at 95–100 °C of oil through the tank,
   then item 6's captured drives against `30`, `31` and `32`. Better → it
   was here; the same → H13 loses its inlet-valve half.
2. **Driving it hard, regularly**, now that the top end has shown itself
   sound (S8): what burns chamber and ring-land deposits off (*general*).
   Free, and in the same readings as test 1 — so the two are not told
   apart, and need not be.
3. **A borescope through a plug hole**, warm engine off: the piston crown
   and the chamber; through the inlet port with the manifold off, the
   valve backs. Looks, and names a cylinder if one is worse.
   **Brought forward to 19–20/10** (*owner's decision*,
   19/10/2026), and **the valve backs through the lower manifold's
   runners with only the upper plenum off** (*the owner's idea*), the
   plugs photographed by cylinder. Read as (*reasoned*): heavy carbon
   on the valve backs, most on 3 and 4, is H13's inlet half found, and
   a mechanical clean (walnut, at a workshop) then outranks a second
   can; little carbon there weakens the inlet half and leaves the
   chamber and the seats. It cannot show a seat that does not seal;
   that stays the leak-down's.
   **Done 19–20/10/2026** (`idle-log.md`, the table): **no inlet valve
   back is coked** — thin lacquer on all four, injector tips clean — so
   **the walnut clean has nothing to do**, and H13's inlet half is
   weak. **The chamber half is where it is**: thin layers on every
   crown, a crust on 4's bowl edge (`photos/borescope-2026-10-20-cyl4-piston-edge.jpg`),
   and **on 3 a layer breaking up, crown and exhaust valve alike**
   (`photos/borescope-2026-10-20-cyl3-exhaust-valve*.jpg`) — the only
   cylinder where deposit is seen to have come away. Ports and chambers
   rank **3 > 4 > 2 > 1**, the pair the dips sit on. Read as (*reasoned*):
   the cleaner is working on the chambers, hardest on 3, which is S18's
   cylinder; what is left there is the PEA's job and driving's, not a
   workshop's.
   - **Weighed, 19/10/2026** (*an AI answer the owner pasted in*, read
     as evidence, not a source): that the valve backs are *certainly*
     coked is not known. For it, in general: the breather's oil mist
     and the exhaust pushed back at valve overlap both bake onto the
     back of an inlet valve, and a porous deposit soaks up fuel at the
     idle. Against it, on this car: a detergent premium fuel since 2017
     (*Against* above), and port injection washes the valve, where the
     heavy cases that walnut blasting is known for are direct-injected
     (*general*). Two of its figures were this car's but from another
     cause: 032's −4.7 % was August, the old MAF (S9), and the sooty plug
     was the old plug 4, before 10/10. Cleaning the back of a valve does
     not clean its seat, and compression and the vacuum gauge were
     sound before the episodes.

### H14. The remap of 6/2018 — the idle's ignition, or its margin

*Added 16/10/2026 at the owner's request, so that if the original map
(22/10, `plan.md` item 5a) cures the idle, the record shows it was a
candidate beforehand.* Until now it sat under *The remap* (*Other — not
symptoms*) without a row. Nobody here has seen the remap's file; what
follows is what a calibration *can* reach, not what this one does.
**The owner does not remember whether the idle stumbled before the
remap** (16/10/2026) — he had the car nine months without it (9/2017 to
6/2018), so the one piece of history that would have decided this is
not there.

**Fuel directly: unlikely, because the lambda control would have
corrected it.** At a warm idle the engine runs closed loop at λ = 1
(H11), so a fuel quantity the tuner changed there is pulled back by
the control and settles in 032 as a learned offset of its own size. 032
reads small — 0.0 / +2.3 % (12/10), −4.7 / +4.7 % (15/10, still on the
remap) — and 055 and 003's air are where they were. **Three ways round
that, all weak:** both probes shifted alike (H11, whose own argument
bounds it to a few per cent); the minutes before the control closes
cold, where a changed enrichment is not corrected — but S1 stays roughest
cold after it closes; and the ECU corrects the average of all four and
slowly, so it cannot catch a single combustion — though a static map
change is not single combustions either. **The one datum pointing this
way**: P0172, *too rich*, stored in 5/2019, a year after the remap, its
cause not known (`idle-log.md`).

**Indirect routes — where a remap could reach the idle:**

1. **The idle's ignition.** The idle governor's fast actuator is the
   advance (S1, *What VCDS saw just before a dip*: 3.3° quiet, 3.6°
   before a dip, 3.9° after, on the remap); the dip recovers in about a
   quarter of a second, which is that loop. A changed base advance at
   idle changes how much the loop has in hand, and so how deep a weak
   combustion goes. **It would deepen dips, not cause them.**
2. **Its temperature corrections**: S1 is roughest cold, and a changed
   cold ignition correction would be felt there first.
3. **The misfire detection's own calibration**: 014's thresholds are
   calibration too, so S3 could move on the stock map without the
   engine moving. That is why 014 and `IdleHealth` are read apart after
   22/10.
4. **The overrun**: when the injectors shut after a lift and when fuel
   comes back are calibration — measured on the remap as 0.8–1.6 s and
   1,300–2,400 rpm (S14). A changed fuel cut fits S14's burble.
5. **Knock control**: more advance means more retard, which fits S4
   under load; **at idle it is excluded by measurement** — no retard and
   no 026 signal at idle in any log (*How the symptoms relate*).
6. **The misfire detection dulled under load, not at idle** (*the
   owner's question*, 18/10/2026). Route 3 the other way round: tuners
   commonly desensitise or switch off misfire detection (*general*), and
   if this one did it under load, the misfires would be **everywhere and
   counted only at idle**, and "only at idle" (S3) would be the
   calibration's, not the engine's. The evidence against it is in S3
   (*Unless the remap dulled the detection under load*): the C4 lamp lit
   on this map, 032 small, the converter well — enough against off, not
   against dulled. **If the stock map counted under load**, the picture
   turns over:
   - **S3** becomes "everywhere", and **S1** stays an idle symptom only
     because idle is where 0x280 can see a misfire, not where it
     happens;
   - **S4/S5 ↔ S1/S3** changes from *none measured* to suspect: the
     knock on cylinder 4 is a load event and the dips sit on 3 and 4,
     and only "no misfires under load" keeps them apart today;
   - **S2 and S14** gain: more misfires, more unburnt charge in the
     exhaust;
   - **weaker**: the candidates that act only at light load — **H3**
     (a small leak is diluted under load), **H8**, **H0**, and **H1**
     and **H13** as far as they lean on "a hot idle";
   - **stronger**: the ones that act everywhere and most under load —
     **H4 and H15**, since a spark needs more voltage the higher the
     cylinder pressure, and misfiring under load is a weak spark's
     typical sign (*general*); **H7**; one cylinder's mechanics;
   - **H14 itself** would be confirmed as why it went unseen, not as
     the cause.

   **And the other reading**: stock counting under load could also be
   a more sensitive detection catching noise (a rough road, a
   gearchange). So the files decide it before the drives do — whether
   the remap touched the detection's thresholds (`plan.md` item 5a, *The
   tuner's files*) — and the drives give the rate to set beside it.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | ✘ | — | ~ | ✘ |

S1 and S3 only as a margin taken away from all four alike, through the
idle's ignition or its detection; S2 and S14 through the overrun's fuel
cut and as a misfire's charge going out; S4 through advance under load.
S5 needs no combustion; S11 is a sound outside the cylinder.

- **The idle advance, read 17/10/2026** (*the owner's question*: is it
  aggressive against VW's figure?; `tools/idleadvance.py`, every 003 log,
  steady warm idle at 740–900 rpm with the plate shut, air at or below
  3.5 g/s): **since 24/9, medians 1.5–3.8° BTDC**, p10–p90 about 0 to
  7°, after TDC in 1–9 % of samples (26 % on `vcds-neutral-026-003`) —
  inside VW's 0–12° BTDC (`vcds.md`) at its retarded end. **Not
  aggressive at idle.** **But on 11/8, on the same map, the median was
  −0.8° and −2.3° — after TDC in 63–74 % of samples**, below VW's range
  (`vcds-01-002-003`, `vcds-ride-002-003`). The shift happened between
  11/8 and 24/9, with the map unchanged, so **it is not the map's**; what
  changed between was the new injectors (23/9), the 2018 MAF still on,
  the adaptations reset. *Reasoned, not shown*: at idle the ECU takes
  advance away when the engine makes more torque than the idle needs,
  so in August something gave it torque to spare, and the repairs took it
  away. Off idle the advance reaches 38°, which cannot be judged without
  VW's load map; 22/10 compares it like with like.
- **For:** the one change to the engine's control that nothing so far has
  undone; it is older than every replaced part, and S3 survived every
  part (S3); 5/2019's P0172 and P0304 came a year after it.
- **Against:** a map acts on all four cylinders alike, and **the dips
  are not shared alike** — two thirds of them on two neighbours in the
  firing order, 3 and 4 where named (*The dips keep to one slot*, *One
  cylinder or two*), so at most it lowers the margin until the weakest
  two show; the idle is held closed loop, by mixture and by speed; the tuner
  called it mild and found nothing at the top of the range; 003's idle
  advance sits inside VW's 0–12° (`vcds.md`), so there is no sign of
  an idle map pushed far.

**Tests:**

1. **The original map, 22/10/2026** (`plan.md` item 5a). Not alone: the
   cleaner is in the tank and the adaptations start from zero (`refuted.md`
   C19), the owner's choice (*The remap*). So it is read on what the
   cleaner does not move: **003's idle advance** against the remap's (S1,
   *What VCDS saw just before a dip*, and every 003 log since); **the
   fuel cut on the overrun** by `coastscan.py` against 0.8–1.6 s and
   1,300–2,400 rpm; **014 against `IdleHealth`**, which moving apart
   would be the detection's calibration; **014 under load**, new counts
   per `aktivováno` sample against 15 in about 4,300 (route 6); and
   **020 on the pull**, the
   retard on cylinder 4 (S4). A calmer idle with the advance moved → H14;
   with the advance where it was → the cleaner or the adaptations.

### H15. The aftermarket leads (and plugs) — a set that fits all four slightly wrong

*Added 17/10/2026 at the owner's request*, as the fallback if the idle is
the same on the original map. Until now it sat inside H4 as one sentence
(*a lead, cheap to test by borrowing a genuine VW set*), where it did not
belong: H4 is the spark **not** in the parts, and this is the parts.

**The claim.** Not one bad lead, which the new set of 10/10 would have
taken away, but **a design that sits wrong on this engine's plugs, in
every set of it**. The leads on the car since 17/9 are NGK — the garage's
set, then NGK `RC-VW254` from 10/10 — and **the 12/2022 set was NGK
too**, leads and plugs (*owner*, the invoice found 20/10/2026;
`vehicle-history.md`). *This said until then that its maker was not
recorded.* So **every set on the car since at least 12/2022 has been
NGK**, which answers the strongest argument against H15 — that the
pattern on 3 and 4 outlived three sets of leads — only if the fault is
the NGK design's fit, as claimed, and not a single bad lead. **VW originals were decided on
9/10** (ranked list, row H4) **and NGK went in instead**, so the swap the
idle was going to be read on has never happened.

**What it rests on:**

- **The Polish AQY thread** (H4): one poster's new aftermarket Beru leads
  made the engine misfire until he went back to VW's thick originals.
  One poster, a forum; the thread's original poster had NGK leads and
  they did not help him. **The thread names leads, not plugs.**
- **The plug ends.** The old NGK set came off far more easily than the
  new one went on, and lead 4's end was scored inside with its terminal
  set back (H4 test 1d); the new lead 4 still sits looser than the other
  three after a reseat (H4 test 1e, 15/10). A boot that grips a plug's
  post loosely is a contact that can arc (*general*).
- **The plug ends of 3 and 4 came off far more easily than 1 and 2**
  (*owner*, 19–20/10/2026, plugs out for `plan.md` item 6b): the NGK
  set of 10/10, nine days on. **By grip, 2 > 1 > 3 ≈ 4** (*owner*, 20/10,
corrected: this said *lead 1 came off hard*): 2 the tightest, this time
and on 10/10 alike, 1 a little less, 3 and 4 almost without force. The
owner reads it as the NGK set's design — each lead a different length,
no difference visible inside — and means to measure the ends with a
caliper. **How they seat** (*owner*, 20/10): the NGK ends of 10/10 do
click on, but it sounds like rubber, with only a faint metallic click
at the end, weaker than he would expect for a contact carrying the
spark; his own guess, to be read against the VW set. **Lead 2's plug end
  tore** when it was gripped by the rubber. The two easy ones are the
  two cylinders the dips sit on (*One cylinder or two*), and the second
  time a loose end on 4 has been felt (above). *Until 20/10 this gave
  an oiled boot as the plain reading, plugs 3 and 4 having oil on their
  threads; **all four had** (`idle-log.md`, 19–20/10), lead 2 the
  tightest of all, so oil does not explain it.* It stays a fact about
  3 and 4 without an explanation. **The swap to VW originals happens now**
  because lead 2 must be replaced (*owner*, 20/10): it is the test this
  hypothesis was waiting for, though it now lands beside the map of
  22/10, so a change in the idle cannot be given to one of them alone.
- **The deposits on 3 and 4 need a cause of their own** (*the owner's
  reasoning*, 20/10/2026, after the look inside): every cause put
  forward for the deposits so far — years of gentle driving, a blocked
  fuel filter, worn probes, the fuel, the map — acts on all four alike,
  and the look found 3 and 4 worse. So the difference is read as **the
  consequence of poorer combustion on 3 and 4 over years**, from
  something that touches those two only; the deposits may now add to
  it (a flake under a seat, S18). What touches 3 and 4 alone
  (*reasoned*): the leads and their plug ends — **the only evidence,
  felt twice**; the lower manifold gasket at their runners (H3); the
  old injectors, replaced 23/9, which could explain years of deposit
  but not the dips since; their valves, stem seals or lifters (H1).
  **Not the coil**: its outputs are 1+4 and 2+3, so 3 and 4 sit on
  different ones. **Not the crankcase gas**: the breather, the throttle's
  vacuum and the EVAP line all enter the common intake ahead of the
  runners, nothing at one cylinder (*owner*, 20/10). The lower gasket
  looked alike at all four, by eye, and the only hiss is at the
  throttle (*owner*, 20/10; S11) — which says little about a small leak.
  If the VW leads take the dips off 3 and 4, the chain holds.
- **Searched 20/10/2026** (forums and search-engine extracts; leads, not
  sources; the two big threads sit behind a bot wall and were read only
  as extracts):
  - **`06A 905 409 L` is a later revision.** A write-up of a lead change
    on the 2.0 AEG (vwvortex, *DIY: Replacing Spark Plug Wires on a 2.0
    AEG engine*) says it supersedes the factory `06A 905 409 F`, thicker
    and with extra silicone wrapping by the intake manifold, Beru making
    both. Not confirmed in a catalogue. If so, VW reworked the lead,
    which says the first design had a weakness, likely heat at the
    manifold. It is the set ordered on 20/10.
  - **A plug end that burnt out** (newbeetle.org, *Rough idle, misfire
    fixed*, a 2004 Beetle 2.0, Bosch leads): about 80,000 km on, the end
    on cylinder 1 had arced and come apart inside; a rough hot idle and
    a weak spark; new plugs and leads cured it.
  - **Idle-only misfire and the plug end**: general pages on idle-only
    misfires list a loose or worn plug end, one lead maker's page saying
    the contact matters most at idle and less as the revs rise —
    consistent with the energy reading above, and partly marketing.
- **The injector loom at 4** (*owner*, 19/10, plenum off): its PVC tape
  was peeling where it leaves the harness; the wires under it whole,
  sitting in the connector's seals. The tape renewed.

**Why it is weak, and the reasoning is general, not this car's:**

- **Only at idle, and well under load.** A spark needs the least voltage
  at idle, where the charge is thinnest in pressure; a lead that leaks
  its spark or a boot that arcs shows first under load and in the damp
  (*general*). This engine is the other way round — the motorway pulls
  are clean and the warm idle is not.
  ⚠ **That holds for a voltage fault only** (*the owner's question*,
  20/10/2026). At idle the charge is thin and diluted with residual
  gas, so it is the hardest to light, and what it needs is spark
  **energy and duration**, not voltage (*general*). A lead of high
  resistance or a **loose contact on the plug** — what 3 and 4 have
  shown, twice — costs energy, and that shows **at idle first**, where
  the margin is smallest (S1: a charge one per cent smaller is enough
  to fail). So the clean pulls argue against an arcing lead, not
  against a loose boot.
- **Two cylinders, 3 and 4** (*One cylinder or two*), on separate leads
  and different coil outputs. One poor fit explains one of them; the
  other needs the whole set to be marginal, and then the other two
  cylinders should show it too.
- **The leads changed on 10/10 and 014 did not** (S3, *The drive after
  the new leads*). That compares NGK with NGK, so it does not test this —
  but it does say a fresh boot on every plug moved nothing.
- **Load calms the idle while the supply sags 1.25 V** (H4). That is
  about the feed, not the leads, so it argues only weakly here.

**The plugs** are kept in the name and not in the test. NGK `BKUR6ET-10`
on both sets since 17/9; whether it is the type VW lists for this engine
is not checked here and is read at the VW parts counter by VIN, with the
leads. A plug of the right heat range and gap is a commodity (*general*),
and the 12/2022 set was destroyed by the engine's running, not by its
make (`vehicle-history.md`).

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ~ | ~ | — | ✔ | ~ |

*Re-read 20/10/2026* (*the owner's request*; it read ~ throughout
before): **S1 and S3**, because a plug end that costs spark energy fails
first at idle, where the charge is thinnest and the most diluted, and
load calms it by thickening the charge; **S2 and S14**, a charge that
did not light leaves through the exhaust, at idle as a puff and on the
re-entry after an overrun cut as bangs; **S4 and S5 ~**, an arc at lead
4 could put noise into the knock sensor's signal (*reasoned, not
shown*), as 4's crown crust could cause real knock; **S18 ~**, an arc at
a boot clicks once per cycle, but a restart curing it fits a flake
better. **The physics, in short** (*general*, the manifold pressure
measured): at idle the manifold sits at about 0.35–0.4 bar absolute
(the gauge's 18–19 inHg), so the charge is a third of full load's, the
gap needs a few kV to break down and the mixture, thin, cool and full of
residual gas, is hard to light: what it needs from the spark is energy
and duration. Under load the gap needs tens of kV and the dense, hot,
turbulent charge lights from almost any spark. So **a voltage fault**
(cracked insulation, a damp or oily boot) shows under load and in the
damp, **an energy fault** (a loose contact, high resistance) at idle
and cold. The old plug 4's terminal, burnt black and pitted by 1/10, is
what arcing at a loose end leaves. **Against**: the soot does not follow
the pair (plug 3 the cleanest), and the fault survived a change of
leads on 10/10 — explained only if it is the NGK design's fit on these
plugs, not one bad lead. **What the VW set should do, if this is it**:
the dips' share on 3 and 4 falls towards a quarter each, loads-off
`IdleHealth` towards the loads-on figure, 014 counts less, the bangs
thin out.

**The relief after each plug change, and how long it lasts** (*the
owner's idea*, 20/10/2026, and a second reading beside it). *His*: new
plugs help while they are good, and the poor combustion then spoils
them — the 12/2022 set came out eroded and carbon-dry at ~1,500 km
(`vehicle-history.md`), and the episodes of 18/10 may have done it again.
Against it, the plugs pulled on 19–20/10 looked sound, insulators
white, plug 3 the cleanest, and after 10/10 the pattern was back within
two days (26 % on the first drive, 38 % on 12/10), which is too soon
for a plug to wear. *The second* (*reasoned*): every plug change also
re-seats the leads; a fresh end grips, then works loose with heat and
vibration, which fits a relief of days and the two ends that held
least, 3 and 4. **Since the VW plugs and leads go in together, the two
are told apart by how long a relief lasts**: weeks, and either the VW
ends hold or the VW plugs last — the ends are checked by hand after a
few drives; a few days, as after 10/10, and it is neither, with the
intake (H3) next. **The least either reading predicts** (*the owner*):
the idle back at least where it was before the episodes, loads off
about 70–90 at 95–100 °C of oil (17/10, 18/10 afternoon), and better
if this is the cause.

**The idle against every time the leads were handled** (*the owner's
question*, 20/10/2026; `IdleHealth` from the captures, standing idle in
30 s windows at 93–111 °C of oil with the heavy-load windows left out
(b7 median above 32), mean ± standard error — the method of S1, *Every
session since the repairs*, carried on to `39`):

| date | capture | adaptations | the leads | `IdleHealth` | top two (*One cylinder or two*) |
|---|---|---|---|---|---|
| 24/9 | `24` | fresh | NGK of 17/9 | 91 ± 6 | 62 % |
| 3/10 | `26` | fresh | off and on for the cover job | 61 ± 8 (3 windows) | 69 % |
| 4/10 A | `28` | fresh | | 72 ± 3 | 75 % |
| 4/10 B | `29` | settled | | 89 ± 8 (2 windows) | 77 % |
| 9/10 | `30` | settled | pulled by hand (H4 1d) the same day | 83 ± 3 | 67 % |
| 10/10 | `31` | settled | **new NGK set** | 77 ± 4 (cuts left out) | 69 % |
| 12/10 | `32` | settled | **lead 4 re-seated** | **63 ± 1** (66 windows; the idle-speed trial in it) | **59 %** |
| 15/10 | `37`, `38` | settled | | **59 ± 4**, 61 ± 5 | 70 % |
| 18/10 eve | `39` | settled | | 78 ± 4 | 77 % |
| 19/10 | display | settled | | about 100, loads off | — |

Read as (*reasoned, not shown*): **the calmest idles on settled
adaptations this car has given, 12/10 and 15/10, came in the days after
the new set and lead 4's re-seat, and it worsened from there**; the
calm of 3–4/10 came on fresh adaptations and says nothing (S1). That is
the shape a fresh grip that works loose would give, and **the owner
felt it** (20/10): re-seated, lead 4 held better, though not as a lead
should, and by the 19/10 removal it was loose again. **It is also the
shape of the cleaner** (in from 15/10) **and of the episodes** (18/10),
which sit on the same days, and session to session the grade scatters
by about ten. No step after any handling makes the leads worse. So: a
hint for H15, not a test; the VW set, with nothing else changed, is.

S1, S2, S3 and S14 as misfires and their unburnt charge, all ~ because a
spark fault should be worse under load and is not; S4 and S5 because an
arcing end on lead 4 could put noise into cylinder 4's knock window;
S11 is a sound outside the cylinder.

**Tests:**

1. **A genuine VW set of leads, bought by VIN at the counter**, with the
   plug type checked there at the same time. **The upper plenum comes off
   to fit them** (*owner*, 18/10/2026: they cannot be pushed home
   properly without it), with a new Elring `271.230` under it as on
   10/10 — so the intake is opened too and the test is not one variable
   unless the gasket is the one thing besides the leads that changes.
   Done together with any job that takes the plenum off anyway (H3's
   runners of 3 and 4). Fitted cold, each end pushed
   home until it clicks, and then **two or three warm stops**: `IdleHealth`
   loads off at 95–100 °C, 014, and the dips by cylinder against `31`.
   Calmer, with the dips off 3 and 4 → it was here. The same → H15 is
   refuted, and H4's spark side with it.
2. *Cheaper, narrower:* lead 4 alone, the plenum off all the same. It
   can clear or name cylinder 4,
   and says nothing about cylinder 3.

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

**A stretched belt, or half a tooth?** (*the owner's question*,
14/10/2026). A belt does not jump half a tooth: it skips whole teeth or
none. What age can do is a drift of a degree or two — the belt's cords
stretch very little and its tensioner takes up what they do, and the
teeth and pulleys wear (*general*; not this belt's figure). Either way
**the cam is out by the same angle for all four cylinders**, so it
cannot explain dips that keep to one slot (*The dips keep to one
slot*), and a whole tooth is argued against by the vacuum gauge too:
about 18–19 inHg at idle, steady, a little higher at 2000 rpm
(H3, *The vacuum gauge*), where a late cam reads low at both. **Not a
reason to open it for the idle.** Its replacement is a question of
maintenance — its age against VW's interval, which this repository
does not hold (`plan.md` item 6) — and if it is renewed, the marks are
read as it comes off, which answers this lead at no extra cost.

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
**Looked for in every `_z1` capture, 11/10/2026** (*the owner's
question*; what forum owners describe from a failing G28 is a code, a
bad start, a random stall, or engine speed jumping wildly in a live
log). On 0x280, nothing of the kind:
- **no step that the crank could not make**: every change of more than
  12 % between consecutive 180° values is the engine catching on a start
  (one per start, eight in all);
- **no fall to zero while running and no gap in 0x280**, but one: 14 s in
  `26`, where the whole bus went quiet and the fuel counter came back at
  zero — the key turned off and on (`docs/firmware/can-decoding.md`
  trap 2), not a stall;
- **no spike**: a one-segment move out and straight back, 10 rpm or more,
  occurs 312 times, and **193 of them inside the injector cuts of `31`**,
  where the cylinder is known to be dead. That is the shape of a real
  missing stroke, so it is not a sensor's;
- **the idle dips are not one segment**: of 399 warm-idle dips in `26`,
  `28`, `29` and `30`, one is a lone segment; the rest fall over 2–3
  segments and recover over 3–5, and the next segment takes back a
  median of 26 % of the depth. A crank with mass slows and recovers like
  that; a late edge from a sensor is put right by the next one.
*Reasoned:* the dips are in the engine's speed, which agrees with the
owner feeling them from the seat. **What the bus cannot show** is a
glitch shorter than its 180° average — a sensor that upsets one spark
or one injection and so causes a real misfire. Only the raw signal
answers that (*Naming the cylinder*, method 4).
**The same scan on every other sensor the data carries, 11/10/2026**
(*the owner's question*):
- **The pedal, 0x280 b5**: at rest it never leaves its rest value for
  even one frame in any capture — 38 on the old throttle body, 35 on the
  new, over some 1.2 M frames at idle speed.
- **Road speed, 0x1A0** (the ABS wheel sensors, independent of G28): no
  one-frame spike above 2 km/h anywhere.
- **Coolant, 0x288 b1 (G62's reading)**: while the engine runs it only
  ever flickers by its last bit (0.75 °C), which is quantisation. **With
  the engine off and the ignition on** it twice jumps 3 bits (2.25 °C)
  and back within a few frames — 11 times in `08`, once at the end of
  `26` — which water cannot do. *Reasoned:* not the idle's cause, since
  it never happens running; whether it is the ECU reading the sender
  differently with the engine stopped or a contact at G62 is not known.
- **VCDS, at a warm standing idle** (8,767 samples of 003): the throttle
  angle steps by one display unit (1.7 ↔ 2.2) as the idle controller
  works; the air mass has three lone samples out of line, the largest
  +2 g/s — the scatter of a running engine at one sample a second, not a
  sensor. Lambda (033) switches by design and cannot be read this way.
**Not on the bus at all:** the cam sensor (G40), intake air temperature
(only in 004, once), and the knock sensors' raw signal (026 is S5's).
**The pkw-forum.de bucket-tappet thread (H1) is still the only AQY
report found with a named cause in the valvetrain.**

## Naming the cylinder — the missing measurement

**17/10/2026: placed, on one drive.** With the phase kept across held
values (*One cylinder or two*), the cuts of `31` name every slot through
a 430 s run, and the dips outside the cuts fall **42 % on cylinder 4 and
31 % on cylinder 3** (`cutscan.py --name`). What follows below is how it
stood before, kept for the reasoning.

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
4. **The crank and cam sensors on the owner's scope** (*proposed
   11/10/2026*; the LHT00SU1 of H11 test 2). The bus gives engine speed
   once per 180° (`docs/firmware/can-decoding.md` trap 5); the crank
   sensor gives it once per tooth, which is what the ECU's own misfire
   detection works from (*general*). Channel 1 back-probed on the crank
   sensor's signal, channel 2 on the cam sensor's, which marks one point
   in every 720° and so tells the cylinders apart. Per-tooth speed then
   shows **which cylinder each dip falls on**, and whether its stroke
   added nothing (a misfire) or only less (a weak one) — for every dip
   of a warm idle, not twenty dips over three days of cuts. Read off the
   signal itself, not assumed: the tooth count and the gap, the cam
   pulse's position, and which stroke is cylinder 1, by cutting one
   injector once with the scope running. **Unverified, and settles
   whether it can be done at all:** whether the scope records a minute
   or more at a few tens of kS/s on both channels (vendor software or
   sigrok, whose support for this model came as a patch, 2024), and the
   sensors' connector pins, from VW's wiring diagram for this engine.
   Nothing is bought but back-probe pins and female leads; the engine
   runs only as an idle already planned.
   **It also checks G28 itself, which nothing else can** (*the owner's
   question, 11/10*): every dip in the captures and every count in 014 is
   read off this one sensor, so a sensor or a tooth fault would counterfeit
   both. The raw signal shows a short or damaged tooth, a weak or noisy
   amplitude, and whether the dips are in the engine's speed or only in
   the pulses.

### The dips keep to one slot — 9/10/2026

⚠ **"One slot" is the name of the method, not the finding** (*the
owner's correction*, 16/10/2026: these files kept saying *one cylinder*
where the reading had always allowed two). Pairs say the dips are **not
shared alike** and nothing more; **which of one or two cylinders it is
was read on 16–17/10: two neighbours in the firing order, about two
thirds between them, and on `31` they are 3 and 4** (*One cylinder or
two*, at the end of this section).

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

⚠ **Every figure from here to *One cylinder or two* was read on runs
seconds long, and the pair shares are high**: on the bridged runs of
17/10 the same captures give 22–38 % of pairs on the same slot, 28 % in
the bulk, which is what two neighbours at about a third each and the
other two at a sixth predict (0.37² + 0.30² + 2 × 0.16² ≈ 0.28). The short
runs broke where the engine ran smoothest — a held value is two strokes
alike — so they kept the rough stretches. The p-values are not valid
either way on long runs (their pairs are not independent). **The
direction stands; the sizes and the p are history.** What replaces them
is the table in *One cylinder or two*.

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
  well. Either way it is not the whole engine alike. **Pairs can never
  tell those two apart**, however many: they measure how the dips repeat
  (the autocorrelation over four slots), and both readings repeat alike.
  *One cylinder or two*, below, reads it from runs of three.
- **Which cylinder, the bus cannot say**: the phase is lost every few
  seconds. `plan.md` step 3.5 names it, by cutting 1 and 4. *(17/10: the
  phase is kept for minutes once a held value is counted as the strokes
  it hid, and on `31` the cuts named the pair: 3 and 4 — One cylinder or
  two, below.)*

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

**12/10/2026** (`32`, no cuts, every idle in it, cold and warm and the
adaptation stages): **46 of 121 pairs on the same slot, 38 %, p =
0.0011** — back on one slot, more than 9/10's 33 %. Pooled with 10/10,
56 of 160, 35 %. So **the one-cylinder share did not go with the new
leads**: 10/10's quarter was the small sample. Which cylinder is still
the cuts' question (`plan.md` item 7), and they come back into it.

**14/10/2026** (`33` cold, `34` part-warm, the gauge starts; no cuts):
**8 of 23 pairs on the same slot, 35 %, p = 0.2** (4 of 13 and 4 of
10). The same direction as 9/10–12/10, but two short idles give too
few pairs to say anything on their own; pooled with `32`, 54 of 144,
38 %. **Read after every capture from now on** (*owner's decision*,
14/10/2026; `CLAUDE.md`, *After every captured session*): the capture
alone and pooled with the others since the last repair.

**15/10/2026** (item 5, the can in at the station between `35` and
`36`; no cuts): `35` the drive out, **29 of 98, 30 %, p = 0.17**; `36`
its continuation, 4 of 9; `37` the drive home with 4 min of warm idle,
**6 of 11, 55 %, p = 0.034**; `38` the warm gauge, 0 of 1. The day
pooled: **39 of 119, 33 %, p = 0.035**. Pooled with `32`–`34`, since the
exhaust joint: **93 of 263, 35 %, p = 0.00012**. The same direction,
and the long drive with the loads on (`35`) the weakest of it.

**One cylinder or two — 16/10/2026** (*the owner's question*;
`cutscan.py --shares`). A run with **three or more** dips in it keeps
their order as well as their spacing, and order is what pairs lose. So
the shares of the four slots are fitted to every run at once, each run's
phase unknown (EM over the four rotations), on every idle from `09` to
`38`, the injector cuts left out.

**The runs are minutes long now, not seconds** (*the owner's insistence*,
17/10/2026: the time of a stroke is known from the engine speed, so a
held value ought to say how many strokes it hid). It does, once the
threshold is read off the cuts rather than guessed: on `31`, where the
dead cylinder shows how many strokes each hold really was, **one stroke
held for 1.35–1.64 stroke-times and two for 1.83–2.20, with nothing
between** (`cutscan.HOLD_SPLIT` = 1.75; a first try at 1.5 slipped, and
had been reported to the owner as the idea failing). Bridged that way,
**one run of 430 s spans all four cuts of 10/10** (1, 4, 4, 1, with the
reconnections between): cylinder 1 on one slot both times, cylinder 4
two slots from it both times, as the firing order 1-3-4-2 requires
(`test_cutscan.BridgedRuns`). The idle gate (road speed, throttle) is now
the only thing that breaks a run.

Over bridged runs, **123 runs with two or more dips, 104 with three or
more, 2,435 dips**; in firing order from the slot that leads:

| | leader | the next to fire | its 360° partner | the one before |
|---|---|---|---|---|
| **all, `09`–`38`** | **0.37** | 0.16 | 0.16 | **0.30** |
| before the new leads, `09`–`30` | 0.40 | 0.16 | 0.15 | 0.29 |
| since, `31`–`38` | 0.34 | 0.17 | 0.18 | 0.31 |

Against the best fit, in log-likelihood (2 is about seven to one, 7 about
a thousand): **two neighbours with the other two alike (35/15/15/35) 7.0
below; all four alike 78 below; one cylinder with the rest alike 89
below; the two on one coil output 185 below.** Resampling the runs (100
times, 90 %): the leader 34–40 %, its neighbour 26–33 %, **the two
together 64–69 %**, each of the other two 14–20 %.

*This read, from the seconds-long runs of the first version: leader 0.48,
the next 0.31, **its partner 0.03**, the one before 0.19 — "almost none on
its 360° partner". The long runs do not bear that out: the partner
carries as much as the fourth. The short runs were broken at exactly the
holds a smooth stretch makes, which is a selection the long runs do not
have.*

**Named on `31`** (`cutscan.py --name`): the cuts fix which slot is which
cylinder through the whole run, so every dip outside them is named —
**83 dips over 16,332 strokes: cylinder 4 35 (42 %), cylinder 3 26
(31 %), cylinder 2 12 (14 %), cylinder 1 10 (12 %).** The same shape as
the pooled fit, with names on it: **3 and 4**, which fire one after the
other and sit side by side on the head. 61 of 83 on the pair against an
even half is p ≈ 10⁻⁵. ⚠ One drive, the first after the new leads.

**What follows:**

- **Two neighbours, not one cylinder**: about two thirds of the dips on
  a pair that fire one after the other, the rest spread over the other
  two. On `31` the pair is **3 and 4**; the other captures carry no cut,
  so their pair is not named — it is the same shape, not shown to be the
  same pair.
- **3 and 4 are side by side** (cylinder 1 at the belt end, `vcds.md`),
  sharing a wall of the intake and exhaust ports and the head gasket
  between them. **Cylinder 4 is the one S4 and S5 name**, and the one the
  2019 scan stored as P0304; the cover leaked at cylinder 4's end (S10),
  and oil was seen on the boots of leads 3 and 4 on 26/9 (H4, 1e).
- **Not one coil output**: the coil pairs 1 with 4 and 2 with 3 (S1, the
  period-2 line; H4), and the fit puts that pairing 185 below the best.
- **For the hypotheses**: one lead, plug, valve or injector explains one
  of the two at most (H1, H4's high-voltage side); what reaches both is
  what they share — the head gasket between them, their two runners where
  they meet the plenum or the gasket there (H3), their two exhaust ports
  (H2 acts at the shared probe and stays all four) — or a cause common to
  all four with these two nearer the edge (H13, *More than one at once*).
- **Naming needs a cut, and a short one will do**: one injector off for
  half a minute, then the idle left alone for minutes in the same run,
  names every dip in it (*Naming the cylinder*). `plan.md` item 7's
  injectors 1 and 4 already are such a test.
- **It does not reach across driving** (*the owner's question*, 17/10):
  above about 1500 rpm 0x280's 10 ms frames come once or twice a stroke,
  so strokes can no longer be counted, and integrating engine speed over
  time instead drifts by more than half a stroke within 10 s in 10–30 %
  of cases even at idle (`31`, `30`, `32`; 371 ppm of steady clock offset
  on `31` taken out first). Counting 0x280's frames as the clock instead
  is far worse (tens of strokes a minute): the frames are not periodic,
  7–21 ms apart. Keeping the phase across a minute at 2500 rpm needs the
  angle right to about 0.01 %; the integral holds about 0.3 % (*the
  owner's question*, 17/10). **So each stop to be named needs its own cut.**

**By capture, bridged runs** (`cutscan.py --shares`, 17/10/2026; the
shares in firing order from the slot that leads, p against all four
alike; a capture with one run cannot place its dips and reads as all
alike):

| capture | dips | shares | top two | p |
|---|---|---|---|---|
| `09` | 18 | 0.56 0.00 0.28 0.17 | 72 % | 0.008 |
| `18` | 46 | one run | — | — |
| `19` | 257 | 0.41 0.16 0.17 0.26 | 67 % | 4×10⁻⁵ |
| `20` | 66 | 0.47 0.09 0.12 0.32 | 79 % | 5×10⁻⁵ |
| `24` | 154 | 0.32 0.30 0.19 0.19 | 62 % | 0.4 |
| `25` | 139 | 0.39 0.20 0.14 0.28 | 66 % | 0.011 |
| `26` | 89 | 0.43 0.16 0.15 0.26 | 69 % | 0.011 |
| `27` | 155 | 0.39 0.28 0.11 0.23 | 66 % | 0.001 |
| `28` | 107 | 0.38 0.11 0.14 0.37 | 75 % | 0.002 |
| `29` | 109 | 0.45 0.32 0.10 0.12 | 77 % | 7×10⁻⁵ |
| `30` | 262 | 0.43 0.20 0.13 0.24 | 67 % | 5×10⁻⁶ |
| `31` | 201 | 0.41 0.14 0.17 0.28 | 69 % | 4×10⁻⁵ |
| `32` | 388 | 0.32 0.27 0.15 0.27 | 59 % | 0.004 |
| `33` | 53 | one run | — | — |
| `34` | 55 | 0.38 0.18 0.10 0.34 | 72 % | 0.04 |
| `35` | 228 | 0.35 0.27 0.12 0.26 | 62 % | 0.18 |
| `36` | 13 | 0.58 0.16 0.00 0.25 | 84 % | 0.08 |
| `37` | 66 | 0.38 0.32 0.07 0.23 | 70 % | 0.08 |
| `38` | 29 | 0.25 0.25 0.25 0.25 | — | 1 |
| `39` | 70 | 0.47 0.30 0.07 0.16 | 77 % | 0.0009 |
| **pooled `09`–`38`** | **2,435** | **0.37 0.16 0.16 0.30** | **67 %** | **10⁻³³** |

The top two are neighbours in every capture that places its dips at all
(the second-largest share sits next to the leader, never opposite it),
and the weakest captures are the loaded `35` and the short ones.

**18/10/2026** (`39`, the evening drive home; no cuts): **70 dips, top
two 77 %, p = 0.0009**, the neighbours again. Pooled since the exhaust
joint, `32`–`39`: **902 dips, 0.34 0.26 0.14 0.26, top two 61 %,
p = 6×10⁻⁷**.
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
*Re-read 12/10/2026 when **S15 closed**: the column goes from every
fit table. Only H2 had it as a ✔, and it was H2's one heard leak, so H2
is weaker; **the order stands** — H2 already sat at 4, behind H4 on
the one-cylinder argument, and still has S2 and S11.*
*Re-read 10/10/2026 when **H12** was added (driveline play, at the
owner's request): no symptom added or closed. **It goes in last, at
10**: its two points for are shared with H1 and H3, and four of the
measurements against it are things play cannot do. The clutch minutes
are free and on a capture already planned.*
*Re-read 11/10/2026 for what the MAF's effect says (*the owner's
question: if a sensor could halve the dips, can the fault be in the
engine at all?*; `refuted.md` C2). **Yes, but only a soft one.** A dip
needs two things at once: a margin too narrow, and a swing of charge or
mixture that crosses it. A sensor can only change the swing. The old
MAF made the swings bigger and the crossings twice as frequent; the
6–14 a minute that remain on the new one are crossings of a margin a
healthy engine would not have. So it **weakens a hard mechanical fault**
— a valve that does not close, a cylinder that misfires whatever the
mixture — which compression (12 bar, even) already argued against; and
**it fits every margin cause** — a lean runner (H3), deposits, a valve
that leaks or sticks only a little (H1), and H0, an engine with less
margin than it should have. It is the same reading as load calming the
idle and a higher idle being a fair mitigation. **The order stands.***

*Re-read 12/10/2026 when the dips came back on one slot (38 %, p =
0.001, *Naming the cylinder*) and the tailpipe test found nothing cold:
**what acts on one cylinder goes up, what acts on all four alike goes
down.** H3 (a runner) and H1 (a valve) to 1 and 2; **H4 to 3**, for its
high-voltage side on one cylinder — lead 4's plug end, the least firm
of the four when fitted (test 1e), on cylinder 4, where S4, S5 and the
old plug 4 all point; **H2 down to 4**: a leak ahead of the shared probe
moves the mixture of every cylinder, cold it showed nothing, and the
puffs it was credited with come with the dips, as a misfire's charge
would (S2). Not refuted — the warm test is owed. H0, H7 and H8, all
whole-engine, keep their order below it. **Later the same day lead 4
was reseated and found sound** (test 1e): H4 keeps 3 on the
one-cylinder argument alone — what is left of its high-voltage side is
the coil's output and the plug, the leads and plugs being new — and is
the first candidate to drop when anything else names a cylinder
(*decision*: the argument that moved it up still holds, the part that
named it does not). S6 closed and S16 added on
12/10; neither is a column.*

*Re-read 14/10/2026 after the vacuum gauge (`plan.md` step 3 item 2;
H3, *The vacuum gauge*) and when **S11 reopened** (heard again, *owner*):
the S11 column comes back to every fit table as it stood before 12/10.
The gauge read steady at idle and a little higher at ~2150 rpm, with a
clean snap — the "steady and normal" row of *How the vacuum gauge is read*, so **H3 and H1 are
weaker and H0 stronger**. **The order stands** (*decision*): the gauge
rules out a large leak and a valve that does not seal, both already
argued against by VW's leak signs and the even compression, and it
cannot see a small leak at one runner or an intermittent valve at all;
the idle it read was part-cold, 33's and 34's. S11 back gives H2 its
✔ again and H3 its ~, and moves neither.*

*Re-read 15/10/2026 when **S14 reopened** and **S17 was added**: the
S14 column comes back to every fit table as judged on 4/10 (H3 and H2 ✔;
H1, H4, H7 and H11 ~; H0 and H12 ✘). When it closed it had been a
supporting point for H3 and H2 and decided no row's place, and it
decides none now: **the order stands.** What it does change is its own
reading — it outlived the joint behind the converter, so that joint
was not its source. S17 is not a column until it is placed; if it is at
the manifold's joint, it is H2's to read, and H2 would be re-read then.
The warm captures of the same day (`35`–`38`) moved nothing either:
the warm idle read as on 12/10.*

*Re-read 15/10/2026 when **H13** was added (deposits after years of gentle
driving, at the owner's request, from his driving history): no symptom
added or closed. **It goes in at 1** (*decision*): it is the only
candidate with new evidence for it since 12/10, it fits every margin
property S1 has shown — roughest cold, calmer under load, one combustion
failing on a charge one per cent short, one cylinder ahead of the rest
with no part to name — and its test is already running at no cost
(`plan.md` item 5). H3 and H1 both lost ground to the vacuum gauge on
14/10, and the inlet-valve half of H1 is now H13's, so **H3 2, H1 3**,
and the rest down one. The order after the tank is H13's test's to
set.* *Re-read 16/10/2026 when **H14, the remap**, was added at the
owner's request: no symptom added or closed. **It goes in at 5**
(*decision*): below H13, H3, H1 and H4, which can each explain the
one-slot share that a map acting on all four cannot — H4 with a part on
that cylinder, lead 4's plug end still looser than the rest after the
reseat (H4 test 1e, 15/10) — and above H2, which acts on all four alike
too and has found nothing cold. The rest from H2 down one.*
*Re-read 17/10/2026 when the dips were named on `31` — **3 and 4**,
two thirds of them on those two neighbours (*One cylinder or two*): no
symptom added or closed, but the order changes (*decision*). **H1 to 1**:
the valvetrain is the one candidate that is per cylinder and can sit on
two neighbours at once (adjacent lifters and lobes), and cylinder 4 is
where the knock window is noisy with no combustion (S5) — the first link
between the idle and that window. **H3 stays 2**, now pointed at the
lower manifold gasket and the runners of 3 and 4. **H13 to 3**: deposits
can be uneven, but nothing in it prefers a neighbouring pair, and its
test is running anyway. **H4 stays 4 but loses its spark side**: plugs,
leads and coil are cleared by the shape (different leads, different coil
outputs, unchanged by the new set), leaving the injector loom at 3 and
4. **H12 goes down**: play would sit on 360° partners. What acts on all
four alike — H14, H2, H0, H7, H8, the belt, H11 — can only be the margin
the pair falls through first, and stays below. ⚠ The pair is named on one
drive; the other captures have the same shape with no name, and item
5a's stop cuts name it again (`plan.md`).*
*Re-read 17/10/2026 when **H15, the aftermarket leads**, was added at
the owner's request: no symptom added or closed. **It goes in at 6**
(*decision*): below H14, which is being tested on 22/10 anyway, and
above H2 and everything that acts on all four alike, because its test is
cheap and reversible, and lead 4 is a part on one of the two named
cylinders. ⚠ *Corrected 18/10/2026* (*owner*): this said the test
"takes nothing apart". **The leads cannot be fitted properly without the
upper plenum off**, as on 10/10 — a new Elring `271.230` under it, and a
joint on the intake opened and remade, which is H3's ground. So it is
best done when the plenum comes off anyway, and H3 at 2 is the likeliest
reason it will. It stays below H4's injector loom because the
shape (3 and 4, separate leads) and the clean pulls are against it. The
rest from H2 down one.* *Re-read 18/10/2026 when S18 was
added (cylinder 3 out, cold, with a tick at camshaft rate; P0303): it
fits H1 and H13 and is against H3, which acts at the runners and does
not click. **H13 goes to 2 and H3 to 3**: a flake of deposit under a
seat, the morning after a tank of cleaner, is the reading that also
explains why it went with a restart. H1 stays at 1 — a lifter or valve on
3 fits as well, and only a recurrence and a leak-down tell them apart.
The rest stands.*

**More than one at once** (*the owner's point*, 12/10/2026). The
ranking reads each hypothesis as the whole cause, and it need not be:
valves on some cylinders near their limit (H1) together with small
intake leaks (H3) would give both what the one-slot share shows — about
two thirds of the dips on two neighbours in the firing order, 3 and 4
where they could be named (*The dips keep to one slot*, *One cylinder or
two*, 16–17/10) — and the rest spread over the engine, and each repair would then help only in
part. *Reasoned*, not tested; it is why a partial improvement after a
repair is read as a share, not as a miss.

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| 1 | **H15 — the aftermarket leads (and plugs)** | **20/10 evening, up to 1**: the deposits on 3 and 4 need a cause that touches those two only, and the plug ends are the only evidence of one (H15, *The deposits on 3 and 4 need a cause of their own*); the clean pulls argue only against an arcing lead. **Earlier 20/10, up to 3** (*owner's decision*): the easy plug ends of 3 and 4 no longer explained by oil, and the VW set (`06A 905 409 L`, plugs `101 000 033 AA`) goes in on 21/10 as the only change, the map postponed.  VW originals were decided on 9/10 and NGK went in, so a genuine set has never been on the car since 17/9 and perhaps not since 2022; lead 4 still sits looser than the rest (H4 test 1e); one forum case of aftermarket leads misfiring until originals went back. Against: the engine is clean under load, where a spark fault shows first; the dips sit on 3 and 4, separate leads on separate coil outputs; new boots on 10/10 moved nothing. Added 17/10 at the owner's request | **a genuine VW set by VIN**, the plug type checked at the counter, then two or three warm stops (H15 test 1). **Put off indefinitely** (*owner's decision*, 18/10/2026): S18 came with the cleaner and the hard driving, the only changes of those days, on a dry day, and the tick went on with all four firing |
| 2 | **H13 — deposits after years of gentle driving** | **20/10 evening, 2**: read as the consequence on 3 and 4 rather than their cause, and now a cause in its own right (S18). **Earlier 20/10, up to 1** (the look inside, `idle-log.md`): chamber deposit ranks 3 > 4 > 2 > 1, the order of the dips; only 3 shows deposit come away, exhaust valve and crown, S18's cylinder; a crust on 4's crown, S4's; the inlet half weaker, no valve back coked.  the owner's history (15/10): the engine seldom above 3000 rpm for at least nine years and perhaps fifteen; fits every margin property of S1 — roughest cold, calmer under load, a charge one per cent smaller enough to fail one combustion, one cylinder ahead of the rest with no part naming it — and nothing in the repairs touched it. **18/10, for: S18** — cylinder 3 out cold with a tick at camshaft rate, the morning after the cleaner's tank ran out, gone after a restart; **back warm the same afternoon** (the tick for minutes, 014 bursts to 351 under part load, no code); a flake under valve 3's seat fits it best; **the owner now holds deposits the most likely** (18/10), after days of deliberately hard driving on the cleaner. Against: premium fuel with detergents since 2017; compression 12 bar and even; the vacuum gauge steady | **the PEA cleaner over the tank, under way** (`plan.md` item 5), with regular hard driving; a borescope if it is wanted sooner |
| 3 | **H1 — a lifter or valve** | **20/10, down to 3**: nothing against it, but 3's flaked deposit now explains S18 without it; the valves look whole, which says nothing about sealing.  the one cause a forum has named on an AQY (a sticking bucket tappet); compression cannot see it. Against: never worst hot (S1, S3, re-read 9/10); A5 ~~**4/10, against:** zero at both warm stops~~ *(withdrawn 9/10: fresh adaptations, `refuted.md` C19)* **9/10, for: the dips keep to one slot** **10/10, for, weakly: the dips come just after the ECU trims the charge — as H3's do (S1, *What comes before a dip*)** **17/10, for: the dips sit on 3 and 4** (*One cylinder or two*) — two neighbouring sets of lifters and lobes on one camshaft, and cylinder 4 is the one whose knock window is noisy with no combustion at all (S5): a lifter on 4 would be heard there **18/10, for and against: S18** — a tick at camshaft rate with cylinder 3 out is what a hanging lifter does, but it was new, came with the cleaner and the hardest driving, and went by itself twice, which reads more like H13's flake. **And a lifter seldom gives both at once** (*general, not checked on this car*): one short of oil leaves a gap, which clicks, but the valve still closes, so the cylinder fires; one stuck long holds the valve open, so the cylinder misses, but there is no gap to click. One that sticks and frees could alternate, so this weakens H1 for S18 rather than ruling it out. **18/10, against, the oil-starved lifter**: the tick did not quieten with throttle and stopped by itself (S18); a lifter short of oil fills as the pressure rises with revs (*general*). A lifter stuck by varnish would go on ticking, so that variant stands | a **vacuum gauge** at idle (below), the stethoscope, a warm leak-down |
| 4 | **H3 — a small unmetered leak** (with what is left of H9, closed 4/10: the breather's original hose and connector): ~~three injectors not fully home since 23/9~~ (all four seated 1/10, `idle-log.md`; H3, *The injector seats*), and at the back the plenum and its upper gasket, the brake-servo line, the old secondary-air vacuum line **and N112, which vents into the airbox ahead of the MAF** (8/10, `plan.md` step 2a), the breather hose; **the dipstick tube, loose with its bracket missing** (4/10, a crankcase path; **refitted 9/10; the only place smoke came out on 9/10, at the guide's seat, put right to a faint wisp the same day**); **and the throttle's flange**, where a hard protrusion on the old face may have kept the June gasket off (H8, 28/9) | the only candidate that predicts *load helps*; the back was never sprayed; S11's hiss; a leak at the plenum feeds all four, as A5 wants; **also fits S12**, a lean tip-in. Against: trim −3.1 %; VW's own leak signs — idle air 3.1–3.5 g/s against 2.0–5.0, 055's learnt value −0.73 against ±1.50 — rule out a large leak, not a small one (28/9) **4/10, against:** the warm leak signature did not move with the hole sealed, and a leak does not wait for a hard drive (S3, *Session A after step 1b*) **4/10 evening, for:** an unmetered leak is what makes an ECU learn idle air away — the likeliest reason the ECU learns air away (H10, closed 9/10, `refuted.md` C19) **9/10, against: the intake smoked clean cold, the airbox outlet (N112) included** **9/10, for: the dips keep to one slot** (*The dips keep to one slot*) — a leak at one runner acts on one cylinder **12/10, for: the thin hose from the breather's connector to the tee by the runners leaks when blown into — a slow seep through porous rubber, not a hole (owner) — on the line at manifold vacuum (*What the web says about this engine's ventilation*); the breather hose's cuff split along its seam and the shroud supply hose crazed, both ahead of the throttle and read as little (`refuted.md` A15, C9). All on all four alike; the thin hoses and the breather hose replaced, the intake hose kept; the 8 mm hose of 2/10 tight on the tee's own 8 mm leg and on the throttle (owner, 14/10)** | the valve cover job itself, which replaces the upper plenum gasket, the breather **and the throttle with its flange gasket** (29/9) — an improvement afterwards answers it; now **the smoke test of the intake**, next (`plan.md` step 2a, *owner's decision, 4/10*) |
| 5 | **H4 — the electrical feed to the spark** | **17/10, against the spark side: the dips sit on 3 and 4** (*One cylinder or two*), which have separate leads and plugs and sit on different coil outputs (1+4, 2+3), and the same two-neighbour shape was there before the new plugs and leads of 10/10 and after them; the supply acts on all four. **What is left is the injector loom where it reaches 3 and 4**, taped, oily and shared by the two (H7 test 3) | harness 26 years old. Against: better with loads on, when the supply sags 1.25 V **4/10: the pattern fits only in form** — a coil that breaks down hot is the textbook case, but **the coil is from 6/2026**, and the 3/10 oil sat **only on the outside of its plastic and on the outsides of the leads of 3 and 4, wiped dry** (*owner*, 4/10/2026) **9/10: the dips keep to one slot — for the high-voltage side of one lead or tower (test 1e), against the supply side** **9/10, for — the first named part: plug 4's terminal burnt black by 1/10, the plug-end boots never click, one plug end crusted, the owner pulls them by hand (1d)** | **new plugs and leads, VW originals** (*owner's decision, 9/10*, `plan.md` step 3.3), and the drive after: the dips back to a quarter of pairs on one slot → it was here **10/10, done: a quarter (26 %) on the first drive, but 014 counting as before — so not the misfires; the one-cylinder share of the dips, if two or three more drives hold** **12/10, against: back on one slot, 38 % (p = 0.001) — the leads did not take the share either** **12/10, for: lead 4's plug end felt the least firm when fitted (owner, test 1e), on the cylinder S4, S5 and the old plug 4 point at; reseated the same day: all four sit alike, lead 4 sound — nothing (test 1e)** |
| 6 | **H14 — the remap of 6/2018** | the one change to the engine's control nothing has undone, older than every replaced part; it can reach the idle through its ignition (the governor's margin), the detection's calibration and the overrun's fuel cut (S14); 5/2019's P0172 and P0304 a year after it. Against: a map acts on all four alike and the dips keep to one slot; a fuel change at idle would sit in 032, which reads small; mild by the tuner's word; the idle advance inside VW's range. Added 16/10 at the owner's request | **the original map, 22/10** (`plan.md` item 5a), read on what the cleaner does not move: 003's idle advance, the fuel cut by `coastscan.py`, 014 against `IdleHealth`, 020 on the pull (H14 test 1) |
| 7 | **H2 — an exhaust leak ahead of the probe** | explains the puff and possibly S11's hiss; the zone is now only the **original manifold, its gasket to the head and the probe boss** — the new flange is behind the probe (28/9), and the puff is older than the 10/9 exhaust work (S2). Against: air outside the cylinder does not stop it firing **4/10: the hiss stayed after 1b, from the back (S11), and 014 came back only after a hard drive — heat from load, which opens a crack or a gasket; the owner's lead.** Still against: it has to act through the lambda control, which B3's 033 shows **4/10 evening, against:** at B1 033's median was −0.8 %, not the positive correction air at the probe would force, and B counted on a cold idle **9/10, against it as the dips' cause: they keep to one slot, and air at the shared probe acts on all four alike** — its sounds (S2, S11) are its own either way **12/10: S15 closed, gone with the joint behind the converter — H2's one heard leak withdrawn** | the owner's tailpipe test, and a new manifold if it leaks there (`plan.md` step 3, *owner's decision, 3/10*) **12/10, against: the tailpipe test found nothing cold, and the dips are back on one slot (38 %) — an exhaust leak ahead of the shared probe acts on all four alike. The warm test is still owed (`plan.md` item 7)** |
| 8 | **H0 — normal for this engine** | any engine idles least steadily at its lightest load; nothing has ever been compared. Against: 014 reads 12–120 against VW's 0–5 **4/10, against:** ~~zero at both warm stops is not what a normal-for-the-engine idle does on a counter that read 10–20 a minute there~~ *withdrawn 9/10: those zeros came on fresh adaptations (`refuted.md` C19)* **9/10, against: the dips keep to one slot rather than spreading over four alike** — weakly: nobody knows how a healthy AQY shares them | a healthy AQY recorded (H0 test 1) |
| 9 | **H7 — rail pressure** | the regulator and pump never gauged; mixture sensitivity. Against: trims near zero **4/10: the pattern fits only in form** — fuel heat-soaked at the rail after a hard drive; against, the return-flow rail keeps fuel moving, heat soak is a hot-*restart* effect, and the coolant read the same at A3's zero **9/10, against: rail pressure acts on all four alike, and the dips keep to one slot** **10/10, against (the owner's argument): low pressure shows at full load first, where the engine is well, and a steady error shows in 032, near zero** | a fuel pressure gauge — **not bought** (*owner*, 10/10) |
| 10 | **H8 — throttle body and idle control** | original part, all four cylinders. Against: the dip is one firing, not a hunting loop; found clean in 6/2026; **the idle angle in every VCDS log is steady and the misfires do not move with it** (27/9) **4/10 evening:** a new throttle passing more at rest than the ECU's model would also make it learn air away (`refuted.md` C19) **9/10, against: the throttle feeds all four alike, and the dips keep to one slot** | **replaced inside the valve cover job** (owner's decision, 29/9, reversing 28/9's separate step; `idle-log.md`, *The valve cover and throttle job*), so its effect no longer shows alone — only the kept old part, refitted for a day, can name it. **S13** (its routine at every ignition-on) now sits here too, most likely the unit's normal behaviour by owners' reports; **the old part timed at 20 s before and after a completed 098** (29/9), so not an unfinished adaptation — **and the new part the same, 2/10: S13 closed, nothing left of it for H8** |
| 11 | **the timing belt a tooth out** | belt from 10/2017. Against: even compression, the torque plateau is reached | the marks (VW's manual), **not done in the valve cover job** — owner's decision, 28/9 |
| 12 | **H11 — both lambda probes shifted alike** | the only part of the mixture control not changed, 10/2017; no probe test sees a shift; soot on three plugs. Against: 032 + 033 near zero on a new MAF and new injectors bounds it to a few per cent, and with the wrong sign — negative, the ECU taking fuel out; a few per cent does not misfire | a **four-gas analyser** at the emissions station (H11 test 1) |
| 13 | **H12 — driveline play read as misfires** | **17/10, against: play repeats every 360°, which is the pairs 1+4 and 2+3; the dips sit on 3 and 4, 180° apart**; load calms the idle, and the dips follow torque trims down, both of which play would also do. Against: the MAF swap and the learned idle air move it, which play would not; the 720° slot pattern (to 9/10); a burned-through converter; the cut test's exact codes **12/10, against: the clutch minutes cleared the gearbox side, the pulley looked fine, and the puffs (S2) come with the dips** | the flywheel alone is left, from the parts catalogue by VIN, only if something points there |

**Re-read 20/10/2026, after the look inside** (`idle-log.md`): first
**H13, H1, H15, H3, H4, H14, H2** (the owner's choice for the third
place); **then, the same evening, H15, H13, H1, H3, H4, H14, H2**, once
the deposits on 3 and 4 were read as needing a cause that touches
those two only (H15). The map is postponed (`plan.md` 5a), so the VW
leads are tested on their own. **No leak-down** (*owner's decision*, 20/10): what would
have told a flake under 3's seat from a valve that leaks on its own is
not going to be done, so H13 and H1 are told apart by whether S18
recurs. **The VW leads `06A 905 409 L` and plugs `101 000 033 AA`
arrive on 21/10** (the leads only at VW's central store). **The map of
22/10 is postponed** (*owner*, 20/10; `plan.md` 5a), so they are the only
change and are read on their own. *This said, earlier on 20/10, first
that they would go in that day with drives before the map, then that
the two would not be told apart.*

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

**How the vacuum gauge is read** (H1 test 5; *moved here from
`plan.md` on 14/10/2026*, when its gauge steps were done — the cold
reading made, the warm one dropped at the owner's decision). Everything here is *general* — the classic
readings of a manifold vacuum gauge — and none of it is VW's figure
for this engine. **Read the needle against itself**, never against a
number from a book: the absolute level also depends on altitude and the
weather.

- **What a flick is.** At idle each cylinder draws on the manifold once
  per cycle, about 6–7 times a second per cylinder at 780 rpm, so a
  healthy needle sits still or trembles evenly. A cylinder that does
  not draw its share — a valve not closing, or a firing that failed —
  shows as **a quick dip of the needle and back**, a fraction of a
  second. That is why it is filmed: a phone at 30 frames a second can
  be stepped through, an eye cannot.
- **A flick is any misfire, not only a valve.** Whatever makes a
  cylinder miss — a valve, a spark, a lean runner — flicks the needle
  the same way. **So the count is first compared with the dips**: the
  capture runs under the same minute, and if the needle flicks about as
  often as the engine speed dips (S1: 5–15 a minute warm), the gauge is
  seeing the misfires themselves. The 2500 rpm hold is also the marker
  that lines the film up with the capture.
- **Flicks at idle that are gone at 2500 do not separate the causes**
  (*corrected 10/10/2026, the owner's point*: this table first read a
  flick that stays at 2500 as H1's sign). Nothing on this car has ever
  misfired under load: with detection `aktivováno` while driving, 014
  started counting about once per 250 samples, against several a minute
  at idle (`open.md` S3, *Off idle, by detection state*). A 2500 rpm
  hold in neutral is light load, where 014 is mostly `deaktiv.` and the
  bus is too noisy to see a misfire, so **the gauge is the only thing
  that reads it there** — and flicks gone at 2500 is still the expected
  reading **for every hypothesis, H1 included**: a hydraulic lifter has
  least oil pressure behind it at idle (*general*).

| what the needle does | reading | for |
|---|---|---|
| **steady at idle**, the level normal for itself, rises a little at 2500 and steady there | no valve fault, no large leak; the dips are too small for the gauge to see | H0, or a fault the gauge cannot reach |
| **an occasional sharp flick down** at idle, irregular, gone at 2500 | the misfires themselves — a hanging valve, a spark, a lean runner all look alike here | S3 confirmed; **names nothing** |
| the same flicks **still there at 2500** | something that misfires off idle too, which nothing on this car has done before | new; a valve (H1) first |
| **a regular flick on every cycle**, same size each time | one valve that never seals (burnt, bent) — unlikely with even compression | H1, a worse form; leak-down next |
| **low and steady at idle**, normal-ish at 2500 | air in behind the throttle | H3 |
| **low and steady at idle and at 2500 alike** | a late cam — the belt a tooth out — or an exhaust restriction | the belt (ranked 10) |
| **a fast, even flutter** that gets worse at 2500 | weak valve springs, or worn guides if it steadies with speed | H1, the springs and guides |
| **slow wandering** up and down over seconds, at idle | mixture or idle control hunting | H8, H7 |

**What follows from it:**

- **What the gauge can and cannot say about H1.** It points at the
  valvetrain only through the rarer readings — a regular flick, a fast
  flutter, flicks that stay at 2500. **An intermittent flick at idle
  alone cannot tell a hanging valve from any other misfire.** H1 is
  then answered by the tests aimed at it: the stethoscope over each
  lifter at a warm idle (H1 test 1), a warm leak-down (test 3), and with
  the valve cover off, each lifter pressed down with its cam lobe
  pointing up — a lifter that gives before the valve moves has bled
  down (*general*; VW's manuals describe a check of this kind for these
  engines, recalled and **not** checked against the manual here).
- **Flicks only at idle**: the gauge has confirmed the misfires and not
  named them; nothing moves in the ranked list, and the next repair is
  chosen from it as it stands.
- **Low and steady**: at idle only → H3 moves up, and the intake is
  smoked warm; at 2500 too → the belt's marks are checked.
- **Steady and normal**: the valvetrain and a large leak are cleared as
  far as a gauge can clear them; H1 and H3 both lose, and H0 gains.
- **Cold and warm differ** (*not read on this car*: the warm reading
  was dropped, 14/10/2026): a flick cold that is gone warm fits the cold
  enrichment and deposits (H1, *inlet-valve deposits*); one that is
  there warm only fits a lifter on thin oil.

## The plan

**The order of work is `plan.md`**, under the owner's rule of 27/9/2026:
the idle first, a repair at a time, readings only where they decide the
next step, and as little idling as possible. The tests listed under each
symptom and hypothesis in this file stay as reference for when a step
needs one; **they are not scheduled**. An earlier ten-step test plan stood
here; it is in git.

**A higher idle as a mitigation, not a fix** (*owner's decision*,
10/10/2026, on a lead from another assistant; **brought forward to
`plan.md` item 1**). Raising the specified idle a few tens of rpm adds a
little air at idle, which is the direction every load reading says
calms it (S1, *What comes before a dip*). **The procedure is VW's**, for
this engine family: Golf Mk4 repair manual, *Motronic (2.0 ltr.
engine)*, *Adapting idling speed* (workshop-manuals.com) — no fault
stored, coolant at least 85 °C, **login 01283**, adaptation channel 1,
10 rpm steps, kept inside the emissions-test range; the manual allows it
"slightly" for droning or vibration at idle. **Ceiling 900 rpm
specified, the owner's** — above VW's 740–820 (`vcds.md`), so it goes
back inside that range before an emissions test (`plan.md` Part 2,
item 1). **Whether this ECU has the channel is shown only by the car**:
VW's manual is for the 2.0 Motronic of the Golf Mk4, the manual whose
blocks `vcds.md` matches field for field to this ECU, but it does not
name `06A 906 018 EJ`. **11463 is not for
this**: it is the engine ECU's cruise-control activation code (Ross-Tech,
1.8T page). The owner's own `06A-906-018-AQY.LBL` lists no adaptation
channels, which a label file need not. **What it changes**: the baseline
for every reading after it, the additive's tanks included — accepted by
the owner, the original value kept to go back to. It does not show that
the learned idle air stays above −0.93 g/s, which may simply learn
around a new target (`refuted.md` C19).

**Meanwhile:** avoid long idles — the misfires are an idle phenomenon and
the exhaust has already paid for them once. `IdleHealth` on 0x604 is the
trend to watch, always with the oil temperature beside it.
