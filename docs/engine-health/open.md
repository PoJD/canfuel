# Engine health — what is still wrong, and how to find out why

**The working document for one open investigation into the engine itself.**
It holds only what is **unresolved**: the symptoms still present, the
hypotheses still standing, and the test that would confirm or kill each one.
It has an end date. When every symptom below is either fixed or shown to be
normal for this engine, the file is deleted.

| file | what is in it |
|---|---|
| **this one** | symptoms → hypotheses → tests. Short on purpose |
| `refuted.md` | every hypothesis **settled against** and every symptom closed, with what settled it. Read it before proposing something |
| `vcds.md` | the VCDS blocks read on this car, their specifications, and how to record them |
| `vehicle-history.md` | the service record: parts, dates, distances. **Stays when this investigation closes** |
| `idle-log.md` | **the diary of the idle investigation**: what was done and measured at each stage. **Stays** |
| `plan.md` | **the planned fixes, in order**. Emptied as the work is done |

**The full text this file was condensed from on 20/10/2026** — every
alignment, every table session by session, every argument and its
corrections — is in git: `git show d327332:docs/engine-health/open.md`.
The dated log before it: `git show 7c69883:docs/engine-health.md`.
Nothing in the tree depends on either.

**Rules for this file.** A hypothesis that is refuted, or a symptom that
closes, moves to `refuted.md` in the same commit and leaves this file. A
new measurement goes into the evidence of the symptom and of every
hypothesis it touches, not into a dated section. Owner reports are marked
*owner*; general engine knowledge *general*; an inference *reasoned*.
**Every new observation of the owner's is checked against the symptom
list, and the owner decides** whether it is a symptom. When the symptom
list changes, every fit table gains or loses the column in the same commit
and the ranked list is re-read.

⚠ **Nothing here changes a constant in `src/`.** `IdleHealth` and the start
bytes on 0x604 are one of the instruments (`docs/firmware/frames.md`).

---

## Where it stands — 20 November 2026

*What was done and measured, day by day, is `idle-log.md`; each result
is in the evidence of its symptom and hypotheses below. This section
holds only the current state (condensed 15/11/2026 at the owner's
request; the dated version is in git, `git show 1780e07:docs/engine-health/open.md`).
Condensed again 17/11 at the owner's request — S1, S3, S19, H11 and H16;
the full text in `git show 5e1ddf2:docs/engine-health/open.md` and, for
the second pass over S1, S3 and S19, `git show 5741dfa:docs/engine-health/open.md`.*

**Closed**, in `refuted.md` §D: S6 the exhaust joint behind the
converter, S7 the cold start (the fuel), S8 the top end, S9 the rich
trim, S10 the oil leak at the back of the head, S13 the throttle's
routine, S15 the sputter, S18 cylinder 3 out with a tick, S23 the new
rear probe's signal at zero (the probe's own fault), S24 the coolant
reading (oil round G62's pins), S21 P0440 and the summer overpressure
(the canister found bypassed, plumbed back 11/11, the new N80 14/11,
the ECU's own check passed 15/11). **Hypotheses settled**: H3 (`refuted.md` C28: the lower
manifold's gasket renewed 17/11 and 3's floor and swell as before),
H16 (C30: the canister plumbed back and N80 renewed, and neither the
idle nor S19's split moved; *the owner*, 17/11), H9, H10, H14, H15, H17, H19, and the forms C25 (the purge times the
swell), C26 (a shared earth under the probes and senders), C27 (the
air mass meter's plug or the earth point by the ECU makes 032's idle
cell) and C29 (H7's injector 3: injectors 2 and 3 swapped 17/11 and
the deficit stayed on 3); H12 done.

**What is known about the idle** (S1, *Every stroke named*, *The
swell's shape, and what the common part follows*; S3; *Naming the
cylinder*):
- **It is two things on top of each other.** **Cylinder 3's part**: a
  floor of about −6 to −9 % of a stroke under the mean at every warm
  idle since 24/9, which swells over 3–8 minutes to −20 to −28 % and
  falls back in half a minute to two minutes; most of the weak strokes
  and **80–90 % of 014's standing rises are 3's**. **The common part**:
  the small unevenness on all four, 2.6–3.1 rpm rms at every warm idle
  since 24/9, moved only by a load, the provider's gas and temperature,
  and by no repair.
- **Load helps 3**: a fifth to a quarter of a stroke short at idle,
  1–3 % at full load; no misfire at full throttle, and the car's
  acceleration needs the rated torque to within a tenth (*Off idle*).
- **Not the swell's cause**, measured: 3's air or fuel as a quantity,
  its spark, the supply voltage, the old probes, the purge's phases
  (`refuted.md` C25), a shared earth (C26); **nor its floor**: injector
  3 (C29) and runner 3's lower gasket (C28), 17/11.
- **Changed and moving neither part**: every part in the fuel and
  ignition path, the MAF (24/9) and the plugs and leads (10/10) apart,
  which moved it once each; the cleaners, the oil, the hydrogen clean,
  the canister plumbed back and the new N80, **the lower manifold's
  gasket and injectors 2 and 3 swapped** (17/11, `54`; S1, *Before and
  after each repair*, *The first stop on the new gasket*). The original
  map since 3/11.
- **The timing belt's marks** (8i, 13/11, the row A2): the cam's mark
  set, the crank pulley's notch 30–60° of crank from the groove on the
  block by eye, 2–5 cm along the rim by the owner's fingers; the air
  the engine takes at full throttle argues against more than about a
  tooth. The true marks are read only by the mechanic before the old
  belt comes off (8q).

**Open symptoms**:
- **The idle**: **S1** the unsettled idle, **S3** the misfires 014
  counts at idle — what `plan.md` works on.
- **Around the idle**: S2 an occasional puff from the exhaust (a
  misfire's charge, seen once on the tailpipe recording), S11 a hiss at
  the back at a warm idle (not the lower joint, 17/11; perhaps the
  throttle's own air), S14 bangs
  on an unblipped downshift (the owner's to watch).
- **The cylinder 4 knock window**: S4 knock retard on 4 (2 beside it
  near the limiter), S5 4 high in 026 in neutral — its tests in
  `plan.md` 8w since 15/11 (*the owner*; out of the plan from 9/10).
- **The mixture**: S19 P0172 once and 032's
  split (idle cell −6 to −9 %, part-load +2 to +9 %).
- **The drive**: S12 a hard jerk at a crawl and on moving off; S20 the
  speed wandering at a constant pedal (better since the pedal, 27/10).
- **S22** a tick once per engine cycle, warm.
- **Not pursued**: S16 a tick in neutral, cold, clutch up; S17 a
  resonance at about 2,200 rpm.

**Ranked** (*The idle's candidates, ranked*; re-ranked 17/11 evening,
*agreed with the owner*): **B, cylinder 3** — H1 a seat on 3 (its
dilution form) and H13 deposits, H4 the injector loom at 3, H20
coolant into 3 (H3 and H7's injector out 17/11, *agreed with the
owner*).
**A, the common part** — H0 normal for this engine, the timing belt a
tooth out, H8 the throttle and idle control, H11 both probes, H7 the
rail's pressure, H2 a leak ahead of the converter, H18 the stem seals,
H21 the front probe's signal-earth wire. **18/11**: every cylinder has a
floor of its own (3 −9.7, 4 −4.4, 1 +1.6, 2 +2.8 % against 1, 2 and 4),
only 3 swells; kept as A and B, not split (*agreed with the owner*).

**The lower manifold's gasket renewed by the owner, 17/11** (Elring
`165.210`; `idle-log.md`), **injectors 2 and 3 swapped**, and **6m
measured: the injectors and their supply side sound, 3 no different**
(H4). **The first drive on it, captured the same morning** (`54`; S1,
*The first stop on the new gasket*): **3 −12 and −10 %, 2 +6 and +5 %**
at the two warm stops — the deficit stayed on 3, so not the injector
(`refuted.md` C29); **3's floor −8.6 % and its swell to −22 % as before**,
so not the gasket (C28); the common part 2.96 rpm rms, as before; 014's
rises 88 % on 3; 032 back to −6.3 / +7.8 % on one drive; cylinder 4's
knock as before; the exhaust puffs (S2) and the hiss (S11) heard as
before (*owner*). **The ranking re-read 17/11** (*agreed with the
owner*): H3 and H7's injector form out of list B.

**The fourth research, 17/11** (*the owner's request*; *What the forums
say*, searched again 17/11; S1, *The advance, the cold fast idle, a
warm engine-off and a coast-down*): **VW's own belt procedure for the
AQY has no mark on the block** — the damper against the bottom belt
guard and the flywheel in the gearbox window — and a tooth is 13.85°
of crank, so 8i's two readings meet only at two teeth, which the air
and the empty fault memory argue against (the belt's row, A2); **3 gains more than the
others from the governor's spark** (a burn phased later), **is level
through the cold fast idle** and drops within a minute of its end,
and **is not reset by a warm engine-off**. **Re-ranked the same
evening** (*agreed with the owner*): H1 above H13 in B, H0 above the
belt and H11 above H7 in A.

**Next** (`plan.md`): **8q**, the timing belt and water pump at a
garage on **7/12**, the old marks read first, `54`'s stop the one it is
set against; then **item 9** by what those show (the coolant's CO₂
test, the stethoscope, the garage session with the intake off);
**8e**, the new rear probe when the seller sends it, the harness at
the end; standing: **8f** at every VCDS session, **6i** the oil level
about 156,400 km, the MFD's `IdleHealth` and `Misfires` at warm stops;
by opportunity (*the owner*, 15/11): **8u** the fuel pressure, **8v** the plugs at their change,
**8w** the cylinder 4 knock window, and (17/11) **6r** the owner's scope
on injectors 3 and 4 and on G28/G40, best before 8q; **6t** two cans of
BG 44K Platinum and a captured drive at their end, before 8q (the
first can in 18/11 at 156,365 km, into about 25 l); and **6s** GM's
cleaner drawn in for the valves' carbon (the head stays on, *the
owner*).

---

## The symptoms

### S1. Unsettled idle — engine speed fluctuates

**What is seen.** Every few seconds the idle dips by 20–45 rpm and recovers in
about a quarter of a second. It feels restless from the driver's seat too:
**the larger dips, about 15 rpm and over by the owner's guess, are felt as a
slight jerk in the seat** and heard, and between jerks `IdleHealth` holds
lower (*owner*, 23/10/2026: about 50 between, higher with each).
**On the new regulator hose, 25/10, no jerk was felt** with `IdleHealth`
about 90 loads off and 120–130 straight after a start and after the loads
went off (*owner*) — so a high grade did not come from felt jerks that
time.
**12/11, at the captured warm stop** (*owner*; **a shift of S1, not the
engine mounts**, his ruling the same day): **frequent small shudders in
the seat at `IdleHealth` 35–40**, one minute holding 38 dips of 10 rpm
and more, 8 of 15 and 1 of 20 — felt below the "about 15 rpm" of 23/10.
**On the bus** (`49`, the stop's settled fourteen minutes): 28–50 dips
of 10 rpm and more a minute, 3–14 of 15, 0–4 of 20, **spread over all
four cylinders** — of 10 rpm and more 1 34 %, 3 25 %, 4 20 %, 2 20 %;
of 15 and more 1 35 %, 3 29 %, 2 22 %, 4 14 % — with 014 silent: **the
common part's steps, not 3's misfires** (*The first captured stop on
the canister*). One idle, oil about 80 °C; whether the grade's make-up changed
(more small steps, fewer deep dips) needs a capture.
**By ear, 25/10 evening** (*owner*, warm, the everyday state): **in the
calmer stretches the engine speed drops a little and holds there**. Not
shown by VCDS, whose 40 rpm steps put the stretches with 014 counting and
without at the same 760–800 (`idle-log.md`); a capture's quarter-rpm
0x280 would show it. It sits beside *What comes before a dip*: a dip
follows the idle overshooting a little.
**By feel, 25/10** (*owner*): the idle felt calmer all day, on the new
regulator hose and the second 44K tank; he says so himself before the
data. 6j's 014 agrees in kind: its episodes stayed at 12 (below).

**How it is measured.** `IdleHealth` on 0x604 grades one firing against the
next (100 = the engine before the repair, lower is smoother). Offline,
`tools/idledips.py --roughness` gives the same grade from a capture.
**Every idle figure in these files is on the `IdleHealth` scale**
(*owner's decision*, 12/10): the mean step in rpm × 50. A capture's figure
is a mean over a window, the display's a running filter of the same
quantity. **A reading without the oil temperature beside it compares with
nothing**. **Fresh adaptations** (after a battery disconnect) were held
to read calmer on every ruler; **014 does not** — it counted on 27/10's
reset as on settled drives, and only 4/10 A was quiet (`refuted.md` C19,
2/11) — and `IdleHealth` on fresh ones (3/10 61–68, 4/10 A 72–74, 27/10
about 50) sits inside the settled range, so it is not shown either way.

**What `IdleHealth` is made of** (17/11, *the owner's request* to have
it in one place; the split of 12/11, *A steady pattern over the
cylinders*, below; drawn in `idlehealth-parts.svg` and in
`idle-log.md`). Of a typical warm grade of about 68 (497 warm 30 s
windows of 20 captures): **about 8 the crank wheel's alternation** — no
combustion, on every engine with this wheel, nothing lowers it; **about
22 the cylinders' steady differences, 3's** — list B, with 3's weak
strokes, the misfires 014 counts, a few points more inside the rest
(*reasoned*: about five a minute on the floor, more in a swell); **about
38 the rest, the common part** — list A, 2.6–3.2 rpm rms a stroke on
all four, which 014 does not count. Of the 38, about 4 is the bus's own
measurement noise (*The floor and the common part read apart*,
below), as fixed as the wheel's 8. **What each could give**
(*reasoned*): 3 level, about 38–46; the common part gone as well, the
wheel's 8 and a healthy engine's own scatter, which no recording here
gives. The parts do not add exactly: the grade counts steps above a
dead-band, so less of A makes 3's deficit count less too — **the
provider's gas gave 14–29 with 3 still 9–13 % short** (*The clean of
9/11*). Measured for scale: the calmest floor stops 36–45, the mean
since 12/10 61–67, a swell's windows 69–86, the old MAF 113.

**What one dip is worth.** Engine speed on 0x280 is recomputed once per 180°
of crank, one power stroke (`docs/firmware/can-decoding.md` trap 5), so a dip
is one cylinder's stroke. A stroke that gives nothing costs an estimated
33–57 rpm; the deepest dips are 37–46, the typical one 20–22 — a partial
burn. **The dip is the failed combustion itself**, and the recovery is the
idle governor. **About three dips in four are one weak stroke, one in five
two in a row** (*How many strokes make a dip*, below).

**Every session since the repairs, like with like** (standing idle, 30 s
windows, 93–111 °C of oil, heavy-load windows left out; mean ± standard
error):

| date | capture | adaptations | what changed | `IdleHealth` |
|---|---|---|---|---|
| 24/9 | `19`/`20` | fresh | new injectors, old MAF | 113 ± 5 |
| 24/9 | `24` | fresh | **new MAF** | 91 ± 6 |
| 3/10 | `26` | fresh | the valve cover job | 61–68 (few windows) |
| 4/10 A | `28` | fresh | the right cover gasket | 72–74 |
| 4/10 B | `29` | settled | | 89 |
| 9/10 | `30` | settled | dipstick, MAF clamp | 83–89 |
| 10/10 | `31` | settled | **new NGK leads and plugs** | 77 ± 4 |
| 12/10 | `32` | settled | lead 4 re-seated, airbox sealed | **63 ± 1** |
| 15/10 | `37`, `38` | settled | the cleaner in | **59–61** |
| 18/10 eve | `39` | settled | after the episodes of 18/10 (`refuted.md` D10) | 78 ± 4 |
| 19/10 | display | settled | | about 100 loads off |
| 21/10 | `40` | settled | **VW plugs and leads, new plenum gasket** | 67 ± 2 |
| 23/10 | display | settled | the first 44K tank, ~70 km in, after a hard motorway run | 45–50 between jerks, 70–90 with them, **never above 100** warm; *fan on 1, one seat heater on 1, lights* (*owner*) |
| 23/10 eve | display | settled | home through Prague traffic, much idling, unsettled throughout; the last stretch held at higher revs in a low gear | **37** straight after, the lowest yet in this state, then slowly back to 50 within about a minute and above it after another; *fan on 1, one seat heater on 1, lights* (*owner*) |
| 24/10 eve | display | settled | the second 44K tank, Orlen Verva 100, after ~340 km in the day with about an hour above 4000 rpm; 3–5 min of warm idle | **70–80**, everyday state (*owner*) |
| 25/10 | display | settled, 032 relearning | **the regulator's vacuum hose renewed**; oil about 80 °C, not 93+ | **about 90** loads off, **35–40** loads on (lowest 35); **no jerk felt** (*owner*) |
| 25/10 eve | display | settled | the new hose, a drive later; oil 96 °C | **70–80**, everyday state; **50–60** at a light before, same state (*owner*) |
| 26/10 | display | settled | warmed in a jam, gently, under 3000 rpm; then one brisker stretch, revs held up in 2nd downhill on engine braking | **80–100** all through the warm-up, **still at 92 °C** of oil; **60–70** after the brisker stretch; everyday state (*owner*) |
| 27/10 | display, video | settled | `plan.md` 6k: a gentle drive to about 88 °C of oil, the A/C against the loads (`idle-log.md`) | **~70** everyday state; **35–50** the A/C alone; **54–62** every load but the A/C; **25–35** both |
| 27/10 eve | display, video | settled (055 reset that afternoon, relearnt to −1.17) | the pedal greased; oil changed 26/10; the second 44K tank about four-fifths used; oil 100 °C | **54** loads off (mean; **35–65** in waves of about 1½ min); **34** every load on with the A/C (26–42, still falling) — **the first stop with loads off within 25 of loads on** (condition 2 below), one stop |
| 28/10 | display | settled | the last of the Verva tank, 13 l in the morning to 5 l; oil 95–100 °C | **70–100 most of the time, down to 47 at moments**, everyday state; **felt worse** (*owner*), and the figures agree: above 27/10's ~70 in the same state, lower being calmer |
| 29/10 | display | settled | home from the pump, 5 km driven gently, oil 87 °C; the Verva still in the lines | **90–130, very unsettled**, everyday state (*owner*) |
| 30/10 | display | settled | the first warm drive on OMV; oil 99 °C | **80–100**, everyday state (*owner*) |
| 2/11 | display | settled | OMV, about 85 km in, the can's 5–6 l added 31/10; the day before the map; oil about 100 °C | **85–105**, everyday state; **felt worse again** (*owner*); cold **110–140** |
| 3/11 | `42` | fresh (reset with the map) | **the original map**; the drive home from the tuner, motorway to 186 km/h, then a stop of about 9 min with throttle blips, oil 103–105 °C; b7 25–29 at idle | **71 ± 3** over every warm window (41–100): **93 ± 2** for the first 3 min after the motorway, **54 ± 3** from the fifth minute (41–67), 63 ± 3 and 77 ± 4 at the two stops near home; cold **98 ± 3** at 50–61 °C of oil |
| 3/11 eve | `43` | one drive after the reset (032 −6.3 / +3.9) | the original map, the second drive: mostly motorway to 90 °C of oil, full-throttle pulls, then a warm stop of 11 min **loads off** (b7 21) with a 57 s cut on injector 4, oil 99–100 °C | **86 ± 4** the first 3 min; 74 the 2 min after the cut; **48 ± 3** from then to engine off (5 min, windows 30–67) — `42`'s shape, settling about the sixth minute; cold 129 over only 26 s settled, oil about 47 °C |
| 3/11 night | display | relearning (032 cleared after `43`'s cut) | the original map, the drive home from football, MFD in | **70–95**, oil 101 °C, everyday state (*owner*) — the first display reading on the original map, a little under the remap's 80–105 of 28/10–2/11 |
| 4/11 | display | relearning | the original map; mostly slow driving and queues, then the engine revved; oil about 100 °C | **90–110** until the engine was revved, **the larger dips felt in the seat**; **70–90** after it; everyday state. **45–50** with the A/C and the blower on full and the rear window heated (no main beam, no seat heaters), still falling; the supply down to about 12.4 V at times with everything on (*owner*) |
| 5/11 | display, photos and a video | relearning | the original map; stops on two short morning drives, the engine perhaps never fully warm and never revved above 3500 rpm, which always leaves it a little worse (*owner*); **the A/C on at every stop** (*owner*); oil not read | **60–76** with the A/C; `Misfires` **2** at 7:33, **5–10** at 9:05; MisfAvg 7.4 and 9.8–11.6 (the start's mean, its cold part in it) — the first warm readings of `Misfires`; cold the night before 18–23 (*owner*, the album) |
| 5/11 eve | display, a video | relearning | the drive home, an hour, mostly queues, revved a little at times; the everyday state plus **the A/C and the blower on 2** throughout; oil 100 °C at the end (*owner*) | **51–54** settling from 60–67 in the last 45 s, still the A/C on; `Misfires` **3–4** there, **1–22** over the drive (*owner*); MisfAvg 8.7 → 8.2 |
| 6/11 | display, a photo | relearning | the first reading after 5/11's contact cleaner (injector 4, T3) and runner 3's gasket edge straightened; about 40 min with a few queues; the everyday state plus **the A/C and the blower on 2**; oil 98 °C (*owner*) | **65** with the A/C; `Misfires` **18**, MisfAvg **23.0** at the end, higher because **only about 5 min of idle in the drive, hardly any warm**; **the engine behaved the same** (*owner*, the album 9:29) |
| 6/11 eve | display, a photo | relearning | the drive home; oil 90 °C; **the A/C off, the blower on 1** (*owner*); **the engine lamp came on** on the way, P0440 (S21, `refuted.md` D14) | **73**; `Misfires` **6**, MisfAvg **8.6**; the idle "relatively OK" (*owner*, the album 16:40) |
| 8/11 | display | relearning | home after the OMV fill (about 10 % Efecta 95 in the tank), mostly gentle on the last of the fuel, a little higher revs after the fill; oil 97 °C; the everyday state, about a minute (*owner*) | **70–75**; `Misfires` **9–12**, MisfAvg **12.5** since the start at the pump (*owner*) |
| 9/11 | `44` | relearning (032 −7.8 / +6.3) | stop 3 **before the hydrogen clean**, after about 50 min of driving with a motorway stretch; the everyday state, the A/C off; 30 s cut on 4; oil 103 °C | **90** the 5 min up to the cut (76–107), **50** the 5 min after it (37–64); 014 1.03 % then 0.02 % of combustions (S1, *The clean of 9/11*) |
| 9/11 | `44`, `45` | relearning | **the provider's gas flowing at idle**: 10:19–10:22 with the A/C and the blower on 4, and the clean's last 2 min with the blower on 4 and the heater full; oil 97–106 °C | **20** and **14–29**, **no dip at all** in 8,700 strokes (S1, *The clean of 9/11*) |
| 9/11 | `46` | relearning | **straight after the clean**, the hose off with the engine running, oil 104 °C; then stop 7 after a motorway run, the everyday state, the A/C off, a 30 s cut on 4, oil 101 °C | **60** straight after; **57** the 3½ min up to stop 7's cut, **63** the 6 min after it; 014 0.12–0.14 %; at work after the short drive on, 93 → 54–79 over 4 min |
| 10/11 | display, VCDS | kept (032 −7.8 / +7.0) | **the first idle on both new probes** (H11, *The reading after the swap*): a cold start standing, then loads off, the A/C, loads off, 1,500 rpm, idle; coolant 78–99 °C, oil 54 °C at the start of loads off | **120–140, then 112–120** loads off; **70, then 66–75** with the A/C; 98–120 loads off; 70–99 after 1,500 rpm; `Misfires` 13–14, 3–4, 8–12, 7 → 5 (*owner*) — as on 9/11 night with the old probes (130–140, 90–100) |
| 10/11 | display, VCDS 014 | 032 −6.3 / +5.5 after it | the drive on to work, about 29 min; a warm stop at the end, the everyday state, the A/C off, oil 101–102 °C | **60–70, 55, 70, 50–55, 48, then 80–90**; `Misfires` 7, 5, 3 (*owner*); 014 0.24 % of combustions |
| 10/11 eve | `47`, VCDS 014 032 036 | **relearning from zero** (the battery off; −6.3 / +6.3 by 16:58, −3.9 / +7.0 at the end) | `plan.md` 8d, the drive home from work; queue stops 16:51–17:17 in the everyday state, oil 99–103 °C; one with the A/C | **63, 91, 82, 92, 63, 49, 55, 71** loads off; **52** with the A/C; 014 0.24 % over the stops; cold at 44–46 °C of oil with 032 at zero 91–104 (H11, *The relearn drive*) |
| 10/11 eve | `47`, `48` | −3.9 / +7.0 (reset by the clear of P0137, 17:40:05–17:41:44, after the calm began) | the warm stop after a brisk stretch, the everyday state **plus the hazard lights from arrival** (*owner*), the A/C off, **no cut**, oil 102–104 °C; **the rear probe reading zero** (S23) | **59, 57, 52, 54, 65, 66, 84, 70** a minute for 8 min (014 0.15 %); **then 45, 43, 38, 39, 36 — the calmest warm idle captured outside the provider's gas** (the display touched 37 once, 23/10 evening), 3's deficit stepped from −22 to −9 % (`cylscan.py`, 12/11), to the revs for 034 at 17:42:50; 40–66 in the basic settings after (H11, *The relearn drive*) |
| 11/11 night | display, VCDS 014 at the stops | **relearning from zero** (−3.9 / +2.3, then −3.1 / +2.3) | 8k, **the first drive on the canister**; the rear probe at zero (S23), G62 misreading (S24, closed); after a hard motorway run, oil 102 °C, then near home, oil 97 °C | after the motorway **100–119 → 70–89**, `Misfires` 13–15 → 1–3; near home **90–110 → 45–50, waves of 40–80, then 25–40 for minutes**; **014: no count in 4.2 min logged** (22:39–22:43) (*owner*; 8k) |
| 12/11 night | display, VCDS 014 at the last stop | **relearning from zero** (−5.5 / +2.3 at the end) | 8n, the second drive on the canister; **the old rear probe sound, G62 cleaned**; 52 min with a motorway stretch and the limiter touched; the stop near home 01:46–02:02, coolant 94.5–99 °C | **120 (01:46) → 80–90 → 60–70 → 30–60 by 01:48**, then **35–50 for about 13 minutes, mostly about 40** (lowest 34 at 02:02, highest 58), `Misfires` 9–10 → 2–6 → **3**; **014: five counts of one misfire in 7.7 min logged (01:52–02:00), 0.04 % of combustions** (*owner*, times as sent; 8n) |
| 12/11 | `49`, VCDS 014 020 033, then 014 032 036 | 032 −14.8 / +2.3 before (one MFD drive after the clear of the night), **−7.0 / +8.6 after** | `plan.md` item 6, **the first captured warm drive on the canister**: 30 min with five full-throttle pulls, then a warm stop of 18 min, the everyday state but **the seat heater off until about 11:31**, the A/C off, **no cut**, oil 102 °C | **77, 89, 84, 76** a minute for the first four minutes (014 0.69 %), then from 11:20 **47, 52, 40, 35, 40, 44, 36, 34, 39, 33, 30, 37, 39, 37, 37** (014 one count in 13 min) — 3's swell and its step with no cut (*The first captured stop on the canister*) |
| 12/11 eve | `50`, VCDS one group at a time (003, 001, 014; 004 beside) | 032 −7.0 / +8.6 before, **−4.7 / +6.3 after** | `plan.md` 6q, **the queue drive**: 19 km in 67 min from coolant 39 °C, gentle (3 s above 4,000 rpm in its first 39 min, then 30 s in 17:01–17:07, to 6,440 rpm), 23 warm standing idles of 10–58 s, then a stop of 14.8 min slightly uphill, the everyday state, the A/C off, **no cut**, oil 100–101 °C | **72** over the queue's standing idles; the last stop a minute at a time **69, 64, 86, 82, 48, 60, 66, 74, 83, 63, 36, 47, 71, 71, 82** — three swells of 3's and two falls with no cut (*The queue drive, and what the ECU sees through a swell*); 014 19 rises in the stop's last 84 s, 16 on 3 |
| 18/11 | display | settled | the day of 6t's first 44K Platinum can, into about 25 l at 156,365 km; whether the stops came before or after it not said | **50–70, 70–90 in the waves**, everyday state; the idle unchanged (*owner*) |
| 18/11 eve | display | settled | **the first drive on 6t's first can**: home through a queue, much slow crawling and a few standstills; oil 103 °C | **60–70** at the drive's first stops, **then 30–50 from there on, mostly 34–45**, 40–50 in places, **lowest 32**; `Misfires` **3**; everyday state (*owner*) — the morning's 50–70 halved, at the calm of 10/11 eve and 12/11 night. **Then a stop at home: 3's swell after about three minutes, `IdleHealth` 60–70, `Misfires` 4, then back to about 35 ± 2, fairly steady, `Misfires` 2, down to 31–32 and up again to 35–40, `Misfires` 1, then 30–40, steady at 35–37 with small shudders still felt in the seat, and then **25–29 about ten minutes into the stop**, as low as 11/11 night's 25–40 near home, **then another swell of 3's, 50–60, about half a minute, and back under 40**, **and further swells to 60 at most, each falling straight back**; **nothing above 73 over the whole drive**, and 73 only at the start, the engine not yet fully warm. **Then the engine off for about five minutes and restarted warm: 60–70 after the start, then 50–60, `Misfires` 0** (MisfAvg 2.5 since that start, *owner*, not used — `docs/firmware/open.md` 12). **Then about ten minutes of brisker driving and a stop: 40–50, within a minute up to 70–90, in about three minutes back to 50–60 and slowly falling, at moments down towards 40 but not as low as before the restart, then holding about 50–60, a little above and below** (*owner*: "more like before") — the shape after a brisk stretch, as `49`'s 77–89 in its first minutes (*owner*) — the shape of every warm stop since 24/9, the swell and its fall. MisfAvg (5.9, then 5) **not used: the converter or its wiring dropped out now and then, so it did not cover the drive** (*owner*; `docs/firmware/open.md` 12). **One drive, not 6t's reading** |
| 19/11 | display | settled | the drive to work on 6t's first can, **very gentle, never over 3,000 rpm**, no long standing idle; the everyday state (no other said) | **about 100** shortly after the start, cold; **50–60** at the traffic lights on the way; **about 100** at arrival, oil 100 °C (*owner*) — the gentle drive's higher arrival, as 5/11's "never revved above 3,500 rpm, always a little worse" (*owner*), and the stop's start after a drive (S1, *After high revs*); not a long stop, so no swell or settled figure. `Misfires` not read. **One drive, not 6t's reading** |
| 19/11 eve | display | settled | the drive home from work on 6t's first can, **about 50 min**: queues, and **long stretches in 2nd at high revs but light load, the pedal gentle** — not a brisk drive (*owner*); **then about 10 min of standing idle at the end**; the everyday state (no other said); oil 101 °C; **no drop-out of the converter** | **mostly 40–50**, **waves to 62 at most**, **lowest 35**; `Misfires` **1–6**; **MisfAvg 4.1** since the start, StartCrank shown, so the converter ran the whole drive (*owner*; `plan.md` 6); **three more minutes of the stop: 35–46, `Misfires` 0, MisfAvg 3.9** (*owner*) — **the lowest MisfAvg read from the car** (5/11–8/11 7.4–23.0, the cold part in each as in this one); **the waves to 62 only at the stop's start, then 55 at most over about ten minutes standing, `Misfires` 0–2, MisfAvg down to 3.3** (*owner*). **About 15 minutes into the stop a wave, 45–54 only, the radiator fan cutting in and out at times then** (*owner*: perhaps the fan's doing); MisfAvg 3.3 at engine off after about 15 min standing. **Then after about 10 min off a warm restart, standing, no revs: 40–60 throughout, `Misfires` 1–2** (MisfAvg 2.9 since that start, warm, so not comparable; *owner*). The fan a circumstance, not a symptom (*agreed with the owner*, 19/11). **Then a drive on, high revs at light load again, and a stop: 90–110 for about three minutes, then down to 50 for a moment, then further waves of 60–70** (*owner*) — the same kind of drive before both stops, and one started at 62, the other at 90–110. **One drive, not 6t's reading** |
| 20/11 | display | settled | the third day on 6t's first can: the morning drive and the evening's, the evening's a queue with the engine revved now and then; the everyday state (no other said); oil 104 °C | **80–100 all day, never under 70**, the morning's included, warm; in the evening's queue **80–100 before the revs**, **after them mostly 60–89, at moments down to 50 and at moments up to 100** (*owner*: worse today, the opposite of the two evenings before) — the band of 28/10–2/11 (80–105) and of 4/11 (90–110 until revved, 70–90 after), above 18/11 eve's 30–50 and 19/11 eve's 40–50 on the same can; **lower after the revs, not higher**, as 4/11 without a cleaner; **then about 5 min into a stop 40–45, `Misfires` 0, MisfAvg 6.0**, later **at moments 30–35**, back to about 55, then **oscillating about 50** (*owner*: after the longer standing it still does not climb as high). **Nothing else different that day** (*owner*). **The morning's cold start: 160 after the secondary air stopped** (*owner*: not seen for a long time, even cold) — the top of every captured cold start's 110–160 after the secondary air, as 16/11 night's "over 150" (`idle-log.md`). **One day, not 6t's reading** |

**The dips themselves on the original map** (3/11, `42` against `24`–`40`;
standing idles settled 30 s and more, oil 93 °C and over, dips against the
one-second median): **about 17–20 a minute of 15 rpm and over**, as `32`,
`37`, `40` (16) and above `38`'s loads-off 9; **of 30 and over 0–0.4 a
minute**, as `32`–`40` (0.2–0.7); **none of 40 and over in 11 minutes**,
where `40` had one in 20 and `37` one in 7 — too few to tell apart; the
deepest 37.8 against 41–59 on `37`–`40`; the median dip 17.2 rpm as
everywhere. **One thing reads differently**: the spread of engine speed
inside a stop, **8.5 rpm** standard deviation against 9.8–13.9 on `24`–`40`
(only `38`'s single stops as low) — less slow wander, not fewer
stumbles; one drive. The idle speed (794–796 rpm) and 0x280's load byte
(21) as before. Cold (oil 40–70 °C, loads on): 22 dips a minute, 0.7 of
30 and over, against `32`'s 38–40 and 1.6–2.1.

**The clean of 9/11** (`plan.md` item 8, done; `44`–`46`; the
cylinders by `cylscan.py`, 12/11; condensed 17/11, the full text in
`git show 5e1ddf2:docs/engine-health/open.md`, this heading). Both stops after a motorway run, oil 101–103 °C,
each with a 30 s cut on 4.
- **Before** (stop 3): the grade 90 → 57, 3 swelling to −21 % with
  014's storm (1.03 %), then −8 to −9 % after the cut — `42`'s and
  `43`'s pattern. **After** (stop 7): **no rough start**, 3 at its floor
  −7 to −9 % every minute, but no calmer than stop 3's settled half.
  **The day after** (`47`): the swell back on 3, 73 % of the weak
  strokes. **The clean took 3's swell for a day and left its floor.**
- **With the provider's gas flowing**: `IdleHealth` about 20, no dips
  (0 in 4,877 strokes), the grade 14–29 — the calm came in over three
  minutes with the gas and ended in a step when it stopped; the MAF
  and lambda say it was the gas burning, not unmetered air. **The gas
  took the random part and left the steady one**: 3 at −8 to −13 %
  with the gas and without.
- **Read**: a charge easier to light cures the weak strokes outright,
  so **they are a burn that fails** (lighting or spreading); **3's floor
  is what 3 gets or keeps** — air, fuel or compression — which no
  burn aid touches. It does not name the part.
- 014 `deaktiv.` through the clean (19 % load). Faults after stop 3's
  cut: P1240, P0300, P0304, the cut's own; 032 −7.8 / +6.3 % at every
  read.

**The trend over every capture** (28/10, the display's filter replayed;
condensed 17/11, the table and the weather's figures in `git show 5741dfa:docs/engine-health/open.md`, this
heading). Before October there is no trend to read. **Warm, the idle
stepped down once**, from about 75–95 to 50–70, between 10 and 12/10
(the leads), and has wandered inside 50–105 since; **cold it has come
down**, the clearer change (*Temperature*). **No relation** with the
tank's level, the fuel brand or the outside air, measured 28/10.
**The MAF is the one change that showed at once** (24/9, the dips
halved). **What is not known: the healthy target** — every recording is
of this engine, and none of a healthy AQY will be. The grade by repair
since is the table in *Before and after each repair*, below.

**When S1 closes** (*the owner's decision*, 12/11; he closes it):
**`IdleHealth` steadily under 30 at a warm idle, never above it, in the
everyday state and with every load off alike**, oil 95–100 °C, after
the adaptations have settled (032 and 055 not freshly reset), over
**three drives on different days**. **Warm only** (*the owner*, 12/11):
a rough cold idle is no part of the mark — it may be this engine's
own (H0). It asks for what the idle needs:
cylinder 3 level with the others (S1, *Every stroke named*) **and** the
common part gone (*The idle's candidates, ranked*, lists B and A) —
only both together get the grade that low; **the provider's gas did it
once**, with the A/C or the blower on (14–29, 9/11); nothing else has. *Reasoned*: about 8 of the
grade is the crank wheel's own alternation (*A steady pattern over the
cylinders*), which every engine with this wheel carries, so under 30 is
strict but within reach of a healthy idle. `tools/cylscan.py` is read
beside it to say which part moved, but is no mark of its own. Short of
it, the owner may close S1 as *acceptable, cause known*. **A note,
not a mark** (*the owner*, 18/11): if the belt (8q) moves neither part,
S1 may be closed with the swells of 3's gone altogether, even with the
grade above 30; the mark above stays as it is until he says otherwise. *Until 12/11
the marks were three — the dips no longer keeping to a pair
(`cutscan.py --shares`, removed), loads-off `IdleHealth` within about 25
of loads-on, at least the best level shown, about 50–60 loads off
(decided 20/10); on 12/11 for a few hours they were cylinder 3 level
by `cylscan.py` alone, and the same day the owner replaced them with
this.* **Probably on the overrun as well** (*the owner's decision*,
28/10): the downshift without a blip, where the load reads about 10 %
(VCDS 014, field 2) and the bangs of S14 come, is the thinnest charge
and so the strictest test (*owner*). strictest test (*owner*). **Read by ear, not by 014** (*owner*): on the overrun 014's
misfire recognition reads `deaktiv.` — in every 014 log in
`test/fixtures/vcds/`, every row above 1300 rpm with the load under 20 %
reads it, none `aktivováno` (counted 28/10) — so the counter cannot move
there.

**Load smooths it** (condensed 17/11; every reading in `git show 5741dfa:docs/engine-health/open.md`, this
heading). Every consumer at idle makes the ECU open up the air, and the
idle calms — 19/10 loads off about 100, every load on about 50; 4/11
90–110 against 45–50 with the A/C, the blower on full and the rear
window, on the lowest supply. A higher idle (830 rpm, `refuted.md` D9)
did not help. **So what fails answers to the charge a stroke, not to
the air flow, the speed or the volts**: *reasoned*, one cylinder runs
at the edge of stable combustion at the idle's charge. **The A/C stop
of 27/10**: with the A/C on (055's load bits `0101`) the ECU sets the
learnt idle air aside (field 3 at 0.00 for eight minutes) and corrects
live; the A/C alone 35–50, every load but the A/C about 57, both
together 25–35 against 70 — both act, the A/C the more.

**Temperature.** Roughest cold, calmer as the oil warms, calmest hot, in every
session since 24/9. Every engine idles roughest cold (*general*), so this
says nothing about the fault on its own. The roughest reading yet, ~186, came
cold on the dampest, foggiest morning (26/9, *owner*).

**The cold idle has come down since 21/10** (*the owner's
observation*; condensed 17/11, the figures in `git show 5741dfa:docs/engine-health/open.md`, this heading): the
first capture that reads low cold is `40`, two days before the first
44K tank. **But warm oil alone does not bring the calm idle; driving
does** (26/10, 4/11): warmed at idle the grade stops at about 90–110;
every calm warm idle came after a drive, and not necessarily a brisk
one. ⚠ Not separated: no capture warms past 92 °C at idle alone. The
owner's reading (*hypothesis*): the chambers carry something a working
drive clears and an idle does not (H13, H18).

**What comes before a dip, and what a dip is** (`dipcontext.py`,
`dipshape.py`; 10/10–6/11; condensed 17/11, every figure in `git show 5741dfa:docs/engine-health/open.md`,
under *What comes before a dip* to *The radiator fan's cycle*):
- **The ECU has trimmed the charge just before a dip** (about 1 % less
  injection), and **the dips ride a swing of the idle loop at about
  0.8 Hz** — the lambda controller's period at idle is 1.2 s; 3 answers
  the swing no more than the others (*Each cylinder against the idle's
  0.8 Hz swing*, below).
- **How many strokes make a dip**: one weak firing in 75 %, two in a row
  in 22 % (a pair mostly on two different cylinders), three or more in
  3 %; weak firings come together about 3½ times as often as by chance;
  deeper dips more often clusters, cold more clusters. No repair changed
  the mix.
- **A steady pattern over the cylinders, apart from the dips** (5/11,
  split again 12/11): of a typical grade of about 68, **about 8 is the
  crank wheel's own alternation** (1.7 rpm, reading 1 and 4 low), **about
  22 the cylinders' steady differences — 3 alone** — and about 38 the
  common part. 3's part is about a third of `IdleHealth` and moves over
  minutes.
- **The radiator fan's cycle** (6/11): the coolant cycles 92–100.5 °C
  every 74–90 s at a warm stop; b7 rises 12–18 s before the coolant
  turns down and the grade falls with it (r +0.40 and −0.36) — the fan's
  load, a small effect.

**Every stroke named: one weak cylinder, and it is 3** (12/11, the
third research, *the owner's request*; `tools/cylscan.py`, kept, with
its tests; how the count, the wheel and the spread were found is in
*Naming the cylinder*, *The count that does not slip*). Every standing
idle of every `_z1` capture, each stroke on its cylinder for the whole
run, the crank wheel's alternation taken out, each stroke's loss
gathered from the two slots it shows in. **Per cent of one stroke's
work against the four's mean** (a cylinder out is −100), and the weak
strokes — a step 12 rpm or more under the cylinder's own median — per
1000 of its strokes:

| captures, warm (oil ≥ 85 °C) | 1 | 3 | 4 | 2 | weak per 1000: 1 / 3 / 4 / 2 | 3's share of the weak |
|---|---|---|---|---|---|---|
| `19` (24/9, the old MAF) | +8 | **−13** | −11 | +16 | 5 / 26 / 38 / 6 | 35 % |
| `24`–`31` (24/9–10/10) | +6 to +13 | **−11 to −18** | −7 to +1 | +1 to +13 | 1–7 / 13–32 / 5–16 / 0–5 | 48–75 % |
| `32`–`39` (12–18/10) | +4 to +11 | **−10 to −20** | −4 to +3 | +7 to +9 | 0–3 / 6–37 / 2–7 / 0–2 | 55–77 % |
| `40` (21/10, VW leads) | +6 | **−14** | +1 | +7 | 5 / 15 / 3 / 1 | 64 % |
| `42`, `43` (3/11, the original map) | +2, +5 | **−14, −13** | +1, +2 | +10, +6 | 5 / 15 / 4 / 1 | 58 %, 62 % |
| `44` (9/11, before the clean) | +4 | **−11** | −1 | +8 | 1 / 4 / 2 / 0 | 58 % |
| `45` (the gas, the clean's last idle) | +6 | **−13** | +1 | +6 | 0 / 1 / 0 / 0 | one weak stroke in 4,400 |
| `46` (9/11, after the clean) | +3 | **−10** | −3 | +10 | 3 / 6 / 6 / 1 | 38 % |
| `47`, `48` (10/11 evening) | +5, +4 | **−15, −14** | +4, +4 | +6, +6 | 3 / 16 / 2 / 1 and 2 / 6 / 2 / 0 | 73 %, 61 % |
| `49` (12/11, the canister) | +2 | **−9** | +4 | +3 | 3 / 7 / 2 / 1 | 54 % |
| `50` (12/11 evening, the queue drive's last stop) | +5 | **−16** | +4 | +7 | 2 / 22 / 5 / 1 | 74 % |
| `53` (15/11, 8h: 39 minutes, ten of plain idle, then the loads) | +7 | **−11** | −2 | +5 | 3 / 11 / 4 / 2 | 59 % |
| `54` (17/11, the new lower gasket, **injectors 2 and 3 swapped**; the two warm stops) | +4, +3 | **−12, −10** | +2, +2 | +6, +5 | 5 / 18 / 4 / 1 and 8 / 15 / 2 / 1 | 63 % |

- **Cylinder 3 is the weak one in every warm idle on record, 10–20 %
  under the mean** — from 24/9 on (`19`, the first warm idle long
  enough to read), on three sets of plugs and of leads, two MAFs and
  both maps. **And before the injectors were changed (23/9), as far as
  the short idles of August can say** (*the owner's question*, 12/11:
  did 3 lead on the old set too): `09` (11/8, 60 s warm) **3 −19 %**,
  `12` (25 s, the A/C on) **−11 %**, `17` (11 s) **−23 %**, `11` (25 s)
  −21 % with the strongest slot too close to name; only the cold start
  of 11/9 (`18`) had 4 the weakest, −14 %, and 3 −5 % — *the pattern of
  the cold fast idle in every cold start since, found 17/11 (The
  advance, the cold fast idle, a warm engine-off and a coast-down,
  below)*. ⚠ Seconds, not
  minutes, and the names rest on the strongest slot being 2's, which no
  cut checked on the old injectors. **The crank wheel checks half of it
  in `17`** (*the owner's question*, 15/11: could the pattern have lain
  otherwise before the injectors; *Naming the cylinder*, *The names
  before the injectors*): the weak slot there is one of the two the
  wheel reads high, so **it was 2 or 3, not 1 or 4**; and read as 3 the
  whole pattern is the one of the weeks after the change (1 +18, 3 −22,
  4 +3, 2 +1), read as 2 it is that pattern turned half a cycle on the
  day the injectors went in. **Cylinder 4 was weak on 24/9
  (−11 %) and is level warm since early October**; 2 and 1 give more
  than the mean throughout. *This file said "3 and 4 weak, 2
  strong" and "4's steady deficit, 5–8 %" until 12/11*: the crank
  wheel's alternation reads cylinders 1 and 4 low by 1.7 rpm at idle
  and 3 and 2 high, which took 3's deficit for 4's.
- **3's deficit is there in every state**: cold (−11 to −17 % under
  60 °C of oil), warm, **with the A/C on (−10 %, its weak strokes
  nearly gone: 1.6 per 1000 against 12)** and **on the provider's gas
  (−9 to −13 %, one weak stroke in 4,400)**. So the gas and a load take the
  misfires and leave the deficit: *reasoned*, 3 gets or keeps less
  charge than the others all the time — its air, its fuel, or what it
  holds through compression — and that same shortage puts it nearest
  the edge at the smallest charge, where its strokes fail.
- **Cold, 4 is weak with 3**: under 60 °C of oil 4 gives 6–14 % less
  (`18`–`41`) and the weak strokes fall **3 > 4 > 1 > 2** (45 / 34 /
  15 / 6 % of 1,700 on `24`–`39`; 54 / 23 / 16 / 7 % of 310 on
  `40`–`47`) — **the borescope's order of the deposit, 3 > 4 > 2 > 1,
  but for the last two** (H13). Warm, 4's weak strokes fell from 38
  per 1000 (`19`) to 2–7 from 12/10 on: what the leads and the MAF
  cured was mostly 4's.
- **3's deficit moves over minutes, and falls in a step**
  (`--minutes`; per cent, and 3's weak strokes in each minute):
  `44` stop 3, after the motorway: **−18, −19, −19, −23, −27** with
  11, 12, 3, 12, 12 weak strokes, the 30 s cut on 4, then **−10, −9,
  −8, −9, −9** with 0–1; `43`: −14, −18, −18 up to its cut, −7 to −10
  after, climbing back to −14 by the tenth minute; `47`, **no cut**:
  −15, −15, −14, −14, −17, −20, **−26, −22**, then **−9, −10** from
  17:38 — *the four calm minutes that were "unexplained"*; `40`: −14
  with 22 weak strokes in the first minute, **the A/C on: −9 to −11
  with none**, the A/C off: −11 climbing to −22 over seven minutes;
  `49` (12/11, the canister), **no cut**: −14, −19, −23, −13 with 12,
  17, 9, 6, then **−5 to −8 for fourteen minutes** with 0–3, the step
  inside 40 s at 11:19:30 and no second swell; `50` (12/11 evening,
  the queue drive's last stop), **no cut**: −13, −14, −20, −20, **−8**,
  −11, −15, −18, −22, −17, **−8**, −14, −18, −18, −23 with 8, 9, 10, 8,
  4, 4, 8, 19, 17, 6, 3, 4, 11, 9, 11 — **three swells in fifteen
  minutes**, the bottoms 5½ minutes apart; `53` (15/11, 8h), **no
  cut**: **ten minutes of plain idle with no swell** — −12 to −10 with
  1–13 weak strokes a minute, easing to −6 to −8 by the eleventh to
  thirteenth — then, with the loads switched, **three swells to −20,
  −20 and −22** (minutes 17, 25 and 31 of the stop) with 7–12, the
  bottoms about seven minutes apart, and −4 to −7 with 0–3 for the
  last six minutes (S1, *8h's plain idle*).
  So **"a warm stop starts rough and settles" is 3's state**, it is
  not tied to the stop's first minutes (`40`, `47`), and **what ends it
  is a jolt — a cylinder cut, a load, or nothing seen** — not time.
  *Read again 12/11 evening (*The swell's shape*, below): the fall
  with nothing seen takes 30–45 s, and a load masks the swell without
  ending it — a sawtooth, not a jolt.*
  Over 205 warm loads-off windows of 30 s since 21/10 the grade
  correlates −0.6 with 3's deficit; 3's weak strokes go from 0.6 a
  window at −8 % to 4.8 at −22 %, the other three's stay at 1.2–1.7.
- **The small steps are on all four.** With each cylinder's own
  median taken out, the scatter of a stroke is 3.5 rpm rms on 1 and 4,
  4.2 on 3 and 2.9 on 2 (`40`–`47`, warm, 146,000 strokes): the
  everyday unevenness under the misfires is common, 3 a fifth above,
  2 a sixth below — the strongest cylinder is the steadiest. That
  part is what "the common part" of the two lists measures; **the
  misfires that 014 counts are not in it** (S3).
- **What it does not say**: why 3 is short. Not its plug or its lead,
  each changed twice with 3 unchanged; not the coil, whose other
  tower fires 2, the strongest; **and hardly its injector**: 3 was the
  weak one on the old set in August and on the new one since, and the
  same place failing in two sets is unlikely (*the owner's argument*,
  12/11). **Left for 3 alone: its valves, seats, guides and lifters
  (H1), the deposit on them (H13), its runner's joint (H3), its
  injector's wiring, which stayed (H4), coolant (H20)**. A slow growth
  ended by a jolt fits something that settles and is shaken off — a
  valve not quite seating on its deposit until it turns or a flake
  moves, a lifter — better than a leak, a wire or a short injector,
  which have no reason to mend at a cut on another cylinder
  (*reasoned*, weakly: the mean mixture did not differ between the
  swell and the calm at `44`'s stop 3, 001's regulation −0.2 % in
  both, so it is not the trim creeping).
  ⚠ The deficit's scale rests on the cuts (a dead stroke is 34 rpm of
  step); the names on the strongest slot being 2's, which held at all
  eight cuts and puts 014's misfires where the ECU's own P0303 does.

**The idle speed target** (0x288 b5; condensed 17/11, the figures in
`git show 5741dfa:docs/engine-health/open.md`, this heading): **fixed warm at 780 rpm** (410 of 434 windows),
unmoved on the gas; the engine sits 15–18 rpm above it; **the actual
speed does not tell a calm idle from a rough one** (r 0.07), and raising
the target left the grade where it was (D9). *Reasoned*: a lower idle
is not by itself a calmer one. Not a symptom, not a test.

**After high revs, and the rough start of a warm stop** (*owner*,
23/10; 11/11–12/11; condensed 17/11, every stop's figures in `git show 5741dfa:docs/engine-health/open.md`, under
*After high revs* and *The rough start of a warm stop is cylinder 3's*).
After a drive with high revs **a long warm stop starts rough and settles
within 5–8 minutes** (`40` 72 → 58, `43` 86 → 55, `44` 83 → 62, `49`
85 → 40); after a gentle drive it does not, as a rule. **The rough
minutes are 3's swell** (*Every stroke named*), so **"3 is worst" and "a
warm stop starts rough" are one observation**; the cuts did not make the
settling (`42`, `47` settled without one), and the swell also starts
minutes into a stop. Nothing else on the bus shares its time.
*Reasoned*: a seal or a flake on 3 that is worst right after a hot drive
fits; the swell's depth goes weakly with the seconds above 4,000 rpm
before (r −0.32).
**18/11 evening, on the first 44K can** (display, *owner*): the stops
of a queue home at 25–40 with short swells to 60; after ten minutes of
brisker driving the stop **started at 40–50, rose within a minute to
70–90** and was back at 50–60 in about three — the start the one
capture with a cleaner in (`37`) showed, calm and rising, not rough and
settling (H13, *With a cleaner in*).
**19/11 evening, the same can** (display, *owner*): a drive of about 50
minutes with queues and **long stretches in 2nd at high revs but light
load, the pedal gentle** (*owner*: not like a brisk drive), then about
fifteen minutes standing: **waves to 62 only at its start, then
55 at most, mostly 40–50, lowest 35, 35–46 later, one wave of 45–54
about the fifteenth minute with the radiator fan cycling** — no 70–90. **Then a drive on, the same kind —
high revs at light load — and a stop at 90–110 for about three
minutes**, down to 50 for a moment, then waves of 60–70 (*owner*). Two
stops after the same kind of drive, one starting at 62, one at 90–110:
**the owner's reading, no correlation; how a stop starts is not
predictable from the drive before it, the 62 likely chance.** Load and
revs before a stop are **not split by a test** (*the owner's decision*,
19/11 evening; a step proposed as `plan.md` 6u the same evening and
withdrawn); it may be looked for in the captures' data some time.
**20/11, the third day on the can** (display, *owner*): **80–100 all
day, never under 70**, warm; in the evening's queue 80–100 before the
revs, **mostly 60–89 after them**, at moments 50, at moments 100 — the
idle lower after high revs, not higher: the shape without a cleaner
(4/11), on the can; about five minutes into the stop **40–45**,
`Misfires` 0, MisfAvg 6.0, at moments 30–35, then about 50–55 — a
stop settling, as `42`–`49`'s; nothing else different that day (*owner*).

**The first captured stop on the canister** (12/11, `49`; condensed
17/11, the full text in `git show 5e1ddf2:docs/engine-health/open.md`, this heading). 18 minutes standing after
a warm drive with five pulls, no cut. **The swell came as before**
(3 to −23 %, 014 0.69 % of combustions, 37 of 40 rises on 3), **then a
step with nothing seen** to −6 %, and **the floor held fourteen
minutes** (014 one count in 19,400 combustions). Settled, as calm as
the calmest floors before the canister and no calmer: **by H16's test
the canister did not take away what tips 3**. Taken apart, the stop
calms because 3 does; the common part stays (20–26 of the grade).

**The swell's shape, and what the common part follows** (12/11
evening; `tools/swellscan.py`, cylinder 2 taken as the reference;
condensed 17/11, the full argument in `git show 5741dfa:docs/engine-health/open.md`, this heading).
- **It is a sawtooth**: 3 deepens by 1.5–3 % of a stroke a minute for
  3–8 minutes, then **falls in 30–45 s** (80–108 s at `50`), not a jolt;
  up to three times a stop. **Every stroke of 3's is weaker in the
  swell**, not only the weak ones. **A load masks it and does not end
  it.** Straight after a fall 3 is nearly level (−1 to −5 %) and settles
  to its floor in about two minutes. **Nothing on the bus shares the
  fall's time**, and **the mean mixture does not move with it**.
- **What the shape rules out as the swell's cause** (*reasoned*): a
  quantity of air or fuel into 3 (the mixture would move), the spark,
  a flake blown out or a valve turning in one go (the fall is gradual).
  **What it asks for**: a seat on 3 that fouls and burns itself clean;
  a liquid that gathers at 3's inlet valve and is drawn in at once
  (oil, H18; coolant, H20). The ECU's purge phases, once on the list,
  do not time it (`refuted.md` C25). **Left to tell them apart: item 9.**
- **The common part**: 2.6–3.2 rpm rms at every warm idle since 24/9; it
  does not follow 3's swell; **three things move it — a load, the
  provider's gas and temperature** — and nothing else, no repair and no
  day (`54`, 17/11: 2.96). **Read**: a constant of this engine as it
  stands — what H0 predicts and what a fixed fault on all four gives
  (the belt a tooth out); not a source that changes by the day (the
  probes, the purge, the rail after a hot drive, the stems all tried).
  **The belt's renewal (8q) is its test.**
- **What the shape allows, read together 17/11** (*the owner's
  request*; *reasoned*): a relaxation — slow build, a fall that leaves
  3 better than its floor for two minutes — of **something physical**
  (it survives a warm engine-off), **driven by the idle's vacuum** (a
  load masks it), **that slows 3's burn** (the advance, the louder
  pulse) **and adds neither air nor fuel the MAF misses** (the mean
  unmoved). That is **a seat holding burnt gas** — the exhaust seat's
  soft deposit fouling and burnt off, or the inlet seat's crust — with
  a stem that sticks and frees as the next; oil or coolant pooling at
  3, a lifter bleeding down (it would tick) and a deposit soaking fuel
  (the mean would move) fit worse. **Electrical causes fit the swell
  badly**: fuel short on 3 would move the mean, the supply is flat
  through it, the spark is ruled out at full load, and nothing
  electrical would be cleaned by the hydrogen or run better than the
  floor after a fall. 6r in a swell settles the injector's side; the
  floor is a separate question (H4).

**The queue drive, and what the ECU sees through a swell** (12/11
evening, `50`; condensed 17/11, the full text in `git show 5e1ddf2:docs/engine-health/open.md`, this heading).
23 standing idles of 10–58 s in the queue, 3 in the middle of its
range; then **a stop of 14.8 minutes with three swells and two falls,
no settled floor**. Through them the ECU saw nothing move: **the air
mass 3.02–3.12 g/s** (under 1 % across a swell), **the advance's scatter
not with the common part** (r +0.08), **001's regulation swinging the
same 4.6–5.5 % peak to peak at −23 %, through the fall and at −5 %** —
no mixture moving under all four. 014 at the end: 19 rises in 84 s,
16 on 3, all 13 deep ones on 3. A puff heard at about 17:20 (S2). ⚠ A
log taken wholly standing is set by its header's clock (`vcds.md`).

**The phone at the tailpipe through a swell and a fall** (`50`,
`plan.md` 6p; the recordings not kept here; condensed 17/11, the full
text in `git show 5e1ddf2:docs/engine-health/open.md`, this heading). Every firing found on the recording.
**A weak stroke is a louder pulse**, +15 to +22 % for one 12 rpm down,
so S1's dips and S2's sound are one event. **3's pulse grows with its
deficit and drops with the fall, its steady strokes too** (r −0.95 and
−0.99), the gain in about 105° of crank at the front of its pulse.
**The loudest pulse, +77 % at 17:19:48.9, came two firings after 3's
deepest stroke** (−27 rpm): the owner's puff of about 17:20. The rule
6p was written with would have read it for the seat; *reasoned*, the
rule does not hold, and nothing names the part.

**The first drive on the new N80** (14/11, `51`; condensed 17/11, the
full text in `git show 5e1ddf2:docs/engine-health/open.md`, this heading). Two warm stops, 38 and 16 minutes.
**Cylinder 3 swelled four times, as deep as on the old valve**, 56 %
of the weak strokes; **the common part did not move** (2.97 rpm rms).
**The purge opened on purpose** (070, once, 7.8 % vapour) **did not
deepen 3** (−11 to −13 % through it). Every swell that day began with
a basic setting engaged, which the next drive answered (below).
**Read**: the swell is not a valve that leaks shut, nor a purge of
that size tipping 3 at once; what was left of the purge was its
timing. The seat shakes the owner felt at about 18:08 fell in the
second stop's floor: the small dips on all four, not 3's misfires.

**The second drive on the new N80: the purge's phases read against
the swell** (15/11, `52`; condensed 17/11, the full text in `git show 5e1ddf2:docs/engine-health/open.md`, this
heading). A warm stop of 18½ minutes, 070 logged as a measuring block
(field 1, the valve's opening). The ECU purged twice, each a slow ramp
and a quick shut; **3 swelled three times, to −20, −24 and −24 %, and
the valve's state did not set 3's** — a swell with the valve shut, a
floor with it open, one onset by chance at an opening. The floor
−8.2 %, the common part 2.63; the supply voltage and the intake air do
not time the swell either. **The purge shows on the bus in b7**, which
the next section uses. **Read**: the ECU's purge does not time 3's
swell (`refuted.md` C25); 8o dropped; nothing measured is left of the
purge for the idle. The cold idle felt "cleaner" at about 10:57
(*owner*): **not a symptom** (*the owner's decision*, 15/11), nor the
radiator fan at 99 °C.

**The purge's phases on the older captures** (`plan.md` 8s, done;
condensed 17/11, the full text in `git show 5e1ddf2:docs/engine-health/open.md`, this heading). b7 tells a shut
reliably and an opening only roughly; the fan and a drive's settling
can look alike. 15 of 40 stops show a shut, 17 in all. **3's deficit
by the purge's state**: open −12.5 % (33 % of windows in swell), shut
−15.3 % (56 %); across a shut −1.1 in the mean; **no fall follows a
shut, no swell starts at an opening**. Read: on every older stop where
b7 shows the phases, they do not time 3's swell (C25).

**The phone on the cam cover through a swell and a fall** (`52`,
6p, above cylinder 3; not in the repository; condensed 17/11, the full
text in `git show 5e1ddf2:docs/engine-health/open.md`, this heading). Every firing on it at one lag. **Low down
it repeats the tailpipe**: 3's pulse follows its deficit. **Higher up,
where a valve gear's tick would be, nothing follows the swell** — no
once-per-cycle tick at 3's place or anywhere; 105 s of the second
swell's climb are masked above 1 kHz by a broadband noise. Read: no
such tick on the cam cover above 3, in the swell or out of it (H1's
lifter form, against).

**8h's plain idle and its loads** (15/11, `53`; condensed 17/11, the
full text in `git show 5e1ddf2:docs/engine-health/open.md`, this heading). A warm stop of 39 minutes: **ten
minutes of plain idle brought no swell** (3 −12 to −10 %, easing to
−6 to −8); **the swells came with the loads**, to −20, −20 and −22 %
about seven minutes apart. **036 through the first swell**, the only
one on record: the rear probe did not move with it. **055 through the
swells of 18 older warm stops**: the idle regulator does not follow
the swell (−0.06 g/s in it against −0.05 on the floor, r 0.02). Read:
neither the rear probe nor the idle regulator moves through a swell;
8t dropped the same evening.

**The first stop on the new gasket** (17/11, `54`; `plan.md` 8z and
8x, done; a laptop session at the car, read in a cloud session the
same day; `cylscan.py --minutes` and `--vcds`, `swellscan.py --floors`,
the pulls and the knock by scripts not kept; every log set on the
capture by engine speed, the capture starting 06:24:28.5). The lower
manifold's gasket renewed overnight, **injectors 2 and 3 swapped**
(each on its own old lower ring), the throttle adapted (098); the
first start and drive captured, the MFD out, the everyday state: a cold
idle, a drive with warm cuts from 4,000–5,600 rpm, **the warm stop
06:54–07:05** (oil 105 °C, the parking brake on), the engine off 30 s,
pulls to the limiter in 2nd and 3rd (*owner*), **a second stop
07:17:35–07:24:50**, home.
- **The deficit stayed on 3**: 3 −12.4 % at the warm stop and −10.3 %
  at the second, **2 +6.4 and +5.4 %, the strongest as before**, 1 +4
  and +3, 4 +2 and +2 — `53`'s pattern (+7 / −11 / −2 / +5) and every
  warm idle's since 24/9. The injector that was 3's now fires 2 and
  gives most. **Not the injector** (H7, `refuted.md` C29): it would
  have taken the deficit to 2.
- **3's floor and swell as before**: by minute at the warm stop −16,
  −14, −12, −11, −10, −11, −17, **−21**, −11, **−5**, −9 with 16, 6, 5,
  4, 10, 9, 10, 10, 5, 0, 2 weak strokes; the second stop −9, −13,
  −17, then −7 to −10 with 1–4. **The floor −8.6 %** in the 30 s
  windows (`49`–`53`: −6.3 to −8.2), **the swell's bottom −21.9 %**
  (−22.5 to −26.2), the floor's share 34 % of the windows (14–81 %).
  **Not the gasket** (H3, `refuted.md` C28): its test in `plan.md`
  8z was floor gone or halved, and it is neither.
- **The common part 2.96 rpm rms** (2.63–3.16 on `49`–`53`), so no
  leak shared by the four was closed by the gasket either.
- **The grade 63** over the warm stops (`52` 61, `53` 58), the owner's
  "the same as before" (*owner*, 17/11). 014's rises at the second stop
  **88 % on 3** where the stroke was 12 rpm down (S3).
- **Read** (*reasoned*): what was renewed or moved on 17/11 — the
  joint, the injector, the manifold's oil — was not 3's. What is left
  with the cylinder is its head: the seat, the deposits on it, the
  stems (H1, H13, H18's one-valve form), coolant (H20), and the
  injector's wiring past the connector (H4, 6n).

**The advance, the cold fast idle, a warm engine-off and a coast-down**
(17/11, the fourth research, *the owner's request*; scripts not kept;
`cylscan.py`'s and `drivescan.py`'s stroke counts over the `_z1`
captures, warm meaning oil 85 °C and over, the A/C, basic settings and
cuts left out).
- **3 gains more than the others from the idle governor's spark.** At
  a standing warm idle 003's advance is the governor's output — it
  follows engine speed within 0.1 s (−0.20° per rpm, r −0.76; 8,561
  samples in 18 captures) — so a regression on 003 is no test (the
  other cylinders read as large). Read by event instead: after an
  isolated weak stroke on 1, 2 or 4 the governor advances the strokes
  that follow, and every cylinder at the same lag sees the same speed.
  **3 gains 1.2–1.4 times what the others gain** (+0.05 rpm of step per
  rpm of the dip, 95 % CI +0.03 to +0.07; 1,027 events in 109 runs of
  27 captures, `19`–`54`; a placebo gives a tenth of it) — **clear in a
  swell** (+0.07, +0.04 to +0.11), **borderline on the floor** (+0.03,
  −0.01 to +0.07); about +0.8 % of a stroke per degree over the others'
  1.8 %, a scale good to about two. *Reasoned*: a cylinder short of a
  normally burning charge would gain less (about −0.02); a burn phased
  later — slow, diluted or lean — gains more. Two cautions: most causes
  of a short charge slow the idle's burn too (a leaking seat raises the
  residual), and the healthy cylinders differ the same way among
  themselves, ordered against their work (2, the strongest, gains
  least).
- **The cold fast idle keeps 3 level, and its end drops 3 within a
  minute.** In the first 60–150 s after a cold start (930–1,000 rpm,
  003 at −4.8 to −0.7°, about 10 % more air a stroke) **3 is within
  about 5 % of the mean (−5.4 % over 15 cold starts) and 4 is the weak
  one** (−8 to −31 % in the first minute); when the fast idle ends 3
  drops to about −15 % with 23 weak strokes per 1000 — **at the same
  coolant (30–40 °C) and b7 (37–39): −5.6 % with none against −15.4 %
  with 22.6** — in 8 of the 9 cold starts with both phases (`18`, on
  the old injectors, −2 → −7 %). From there to 110 °C of oil 3 sits at
  −13 to −16 % with no trend; at matched b7 (36–40) the cold idle is
  about 5 points deeper than the warm (−15.3 against −10.2 %) with 3–5
  times the weak strokes. **4's cold weakness fades with the oil on its
  own course**: −8 % at 30–40 °C, −4.5 at 70–90, −1.6 at 90–100, +1
  above 100. *Reasoned*: the fast idle moves speed, spark, air and the
  after-start enrichment together (the enrichment not measured: the
  loop is open cold); a later spark should hurt a slow burner, so what
  helps 3 is the speed, the denser charge or the enrichment — a mixture
  or dilution limit rather than a fixed loss of compression, and more
  than the vacuum's change alone would give (10 % more air, a stroke
  13 % shorter). What makes 4 weak cold does not set 3's deficit.
- **The radiator fan's cycle does not pick 3** (27 stops of 300 s and
  more in 17 captures): +0.18 % of a stroke per °C of coolant (+0.05 to
  +0.32), the fan running against not −0.13 % (−0.40 to +0.12), the
  others moving as much.
- **A warm engine-off does not reset 3** (four restarts: `54`'s 30 s,
  `51`'s 22 s key-off and its 4.9-minute fill, `37` → `38`'s 4.7
  minutes): the first 30 s after within about ±5 points of the last 30 s
  before (`54` −9.7 → −7.8 %, `51` −10.5 → −12.8 and −13.6 → −8.9,
  `37` → `38` −15.2 → −13.4), and twice 3 began to deepen 1.5–2.5
  minutes after the restart — after `51`'s fill to −26 % within five.
  It bounds an effect the size of a fall, not one of 2–3 points; no warm
  restart after 5–30 minutes is on record. *Reasoned*: what builds the
  swell survives minutes without combustion — a layer, a seat held off,
  a pool — which item 9's leak-down on an engine switched off in a
  swell relies on.
- **Nothing of 3's own after a coast-down** (12 warm stops in 9
  captures, standing 8–30 s after the fuel returns): 3's deficit in the
  first 15 s as a minute later (−0.0 %, −1.7 to +1.7); the first 15 s
  rougher on all four alike (3's weak strokes 35 against 16.5 per 1000,
  the others' 13 against 2.6). The overrun's deepest vacuum leaves
  nothing on 3 that shows.

**The floor and the common part read apart** (17/11 evening, *the
owner's request*: what each is — mixture, burn at its edge, or
something else; scripts not kept).
- **The floor is a fixed amount at idle speed, not a share, and the
  manifold's vacuum does not set it.** In rpm of step, at 700–1,150
  rpm, warm, the A/C off: 3 less 2 is −6.8 to −8.3 from b7 18 to 60
  (−4.4 above 60), and 3's own median −3.3 to −4.6 from b7 18 to 100
  (93,521 windows of 40 strokes, 33 captures) — where b7 roughly
  doubles and the vacuum behind a seat would fall by a third or more.
  *Off idle's "load at the same speed lifts it, −24 → −9 %" was per
  cent of a stroke that grows with load; in rpm it hardly moves.* The
  loss falls with speed (a quarter to a half by 2,000 rpm), not with
  load. **The swell is the other kind**: a load removes it (the A/C,
  3 at −10 % with no swell). *Reasoned*: two mechanisms — **the swell
  driven by the vacuum** (a seat, H1), **the floor a fixed amount per
  stroke** that a leak of charge (it would grow with load) or of burnt
  gas (it would shrink) does not give, and that **fuel short by a fixed
  amount** (H4's wire or the ECU's output; injector 3 itself is out)
  does — the loop trims a constant shortfall into the idle cell, so the
  unmoved mean says nothing against it; the provider's gas leaving the
  floor fits missing fuel too. 6r reads it directly.
- **The floor's level has not moved since 24/9** (`swellscan.py
  --floors`, every capture with a warm floor window): −8.1 % on `19`
  (the old MAF), −7.1 to −8.5 on `26`–`43`, −8.1 to −9.0 on `44`–`48`,
  −6.3 to −8.6 on `49`–`54` — through the leads, the cleaners, 18/10's
  flake (`39`, 18/10 evening, had no floor at all: 90 % swell, the
  deepest −25.7 %), the map, the hydrogen and the gasket. **What moved
  is the time spent on it**: 0–20 % of the warm windows before 3/11
  (none on `28`–`30`, `36`–`40`), 21–81 % since. *Reasoned*, at the
  owner's question (17/11): deposit is not excluded for the floor — a
  burn slowed by a crust costs a share that shrinks as load speeds the
  burn, which can read as a fixed amount too, and the floor gains a
  little from the spark; against it, nothing that cleaned (the
  cleaners, the hydrogen) moved the level by a point, and the gas that
  took every misfire left it. The fixed amount tells a leak (it would
  shrink or grow with load) from the rest; it does not tell fuel short
  from a burn slowed by deposit.
- **The floor burns a little slower too**: the governor's spark event by
  event with dips of 9 rpm and more (35,125 lag rows, 109 runs), 3 gains
  more than the others on the floor, +0.028 rpm per rpm of dip (95 %
  +0.005 to +0.042), in a swell +0.044 (+0.020 to +0.066) — a lean
  cylinder and a diluted one alike; cylinder 4 gains as much as 3 at
  some lags, so weakly.
- **About two fifths of the common part's variance is the bus's own
  measurement.** On the overrun, nothing burning, a step's residual
  about its slot is 1.7–1.8 rpm rms at 1,600–2,400 rpm (1,500 windows;
  2.1 at the edges); at a warm idle the common part is 2.96 (26
  captures), **on the provider's gas 1.88 — at the bus's floor**. So the
  engine's own share is about 2.3–2.4 rpm rms, near 7 % of a stroke's
  work, and **the gas took nearly all of it**: cycle-to-cycle variation
  of the early flame on all four, which a flame easier to light cures.
  **The spark does not move it** inside the idle's 0–6°: −0.01 rpm rms
  per degree, nothing with engine speed held (8,559 samples of 003). The
  bus's noise alone makes about 4 of the grade (*reasoned*, by
  simulation), beside the wheel's 8. *Reasoned*: what makes an early
  flame vary on all four is burnt gas kept (the cam's timing, the
  belt), a lean or uneven mixture, or this engine's design (H0); the
  data do not choose.
- **The common part by cylinder** (each cylinder's step about its own
  median, weak strokes and two either side out, warm, 26 captures;
  the engine's own share after the bus's 1.8 rpm is taken out in
  quadrature): **3 > 4 ≈ 1 > 2 at every capture** — 3 about 3.4–3.7 rpm
  since mid-October (4.0–4.2 in September), 4 2.6–3.0 (4.1 on `19`,
  the old MAF), 1 2.5–3.1, 2 1.8–2.6, steadiest; on the provider's gas
  3 2.0, 4 1.5, 1 1.2, 2 0.6. So it is not alike on all four: it
  follows the cylinders' order of the cold weak strokes (3 > 4 > 1 > 2)
  and nearly the deposit's (3 > 4 > 2 > 1), and since 10/10 moved only
  where 4 came down. ⚠ The bus's noise is assumed the same on every
  slot. Drawn with what each cylinder gives in
  `cylinders-share.svg` (`idle-log.md`).
- **The mixture's swing cannot be read per stroke**: the injection
  time on 0x288 b6 moves in steps of 2 counts, about 5 %, against the
  loop's ±2.5 %, and VCDS is too slow and too loosely aligned.

**Every cylinder at 3's floor and in its swell** (18/11, *the owner's
question*; `swellscan.py --series --csv` over `44`, `46`, `47`, `49`–`54`,
warm, the A/C off, the median window; each cylinder's work per stroke
against the mean of four, the crank wheel's alternation left in):

| 3's state | windows | 3 | 4 | 1 | 2 | stroke-to-stroke, rpm rms 3 / 4 / 1 / 2 |
|---|---|---|---|---|---|---|
| floor (3 above −10 %) | 166 | −7.5 | −2.2 | +3.8 | +5.0 | 3.46 / 3.44 / 3.25 / 2.88 |
| between | 146 | −12.2 | −0.1 | +5.0 | +7.5 | 4.24 / 3.56 / 3.48 / 2.90 |
| swell (3 at −15 % and under) | 118 | −18.7 | +3.8 | +6.2 | +9.1 | 4.84 / 3.50 / 3.55 / 2.96 |

Against the mean of 1, 2 and 4 alone: **on the floor 3 −9.7, 4 −4.4,
1 +1.6, 2 +2.8; in the swell 3 −25.1, 4 −2.6, 1 −0.2, 2 +2.7.** So **only
3 swells**: 1, 2 and 4 keep their order and their spread of about 7 %
through it, and their stroke-to-stroke scatter does not move, while 3's
rises by two fifths. **4 holds a small floor of its own on 3's floor**,
−4.4 against the other two, but it is not steady from capture to
capture (−3.8 to +4.4 against the mean of four at 3's floor), and part
of 1's and 4's place is the wheel's (they read low, *Naming the
cylinder*). 3's floor is a little over twice 4's.

**2 and 4 change places on 3's long floors** (18/11, *the owner's
question*: 2 second weakest at `48`; the same windows). At the end of
`47`, the moment 3 stepped from −26 to −12 % (the calm of 10/11
evening), 2 slid from about 0 to −3 to −4 % and 4 rose to +1 to +2
against the mean of 1, 2 and 4, and stayed so into `48` until the
revs for 034, after which 2 was back at +2 and 3 back in a swell. `49`
did the same after its fall at about 11:20: over the fourteen minutes
on the floor 2 went from +3 to −3 or −4, 4 from −2 to +3 or +4. So 2
is the weaker of the pair only on 3's long, calm floors, and settles
there over minutes; nothing else on the bus marks it. Read
(*reasoned*, not settled): it rides on 3's floor, not on any repair or
event; whether it is a real shift of 2's and 4's burn or how the slots
are weighed when 3 is level is not known.

**Before and after the canister and the new valve** (14/11 evening;
condensed 17/11, the full text in `git show 5e1ddf2:docs/engine-health/open.md`, this heading). Nothing in the
common part, the swell or the dips moved. **3's floor read about two
points shallower** (−6.3 to −6.8 % on `49`–`51` against −8.1 to −9.0
before) **and held longer** (14.5 and 9.5 minutes unbroken) — **but
`52` the next day had it back at −8.2 %, a minute at the longest**, and
four things changed in those 36 hours, two hard drives among them.
Read: the canister may sit 3 a little nearer the others between
swells; not shown to last (`54`: −8.6 %).

**Before and after each repair, 24/9 to 14/11** (14/11 night, *the
owner's question*: did the three fuel cleaners and the oil flush move
anything, and the MAF and the plugs and leads; and does the idle move
at all where 014 and `IdleHealth` do not show it. The warm standing
idle of `19`–`51`, oil 90 °C and more, the A/C off, cuts left out, in
the 30 s windows of the section above — `swellscan.py --floors`, each
row below its pooled line over the captures named; 014 from every log
at a standing idle with detection on, not sorted by warmth —
`misfshare.py`). The grade here is the stroke steps' own (the
dead-banded step × 50 over a window), near `IdleHealth` but not the
display's byte.

| | windows | the grade | dips a minute | 3's weak strokes per 1000 | the others' | the common part | 3 / 4 / 1 / 2, % of a stroke | floor, share of windows |
|---|---|---|---|---|---|---|---|---|
| `19`, 24/9 morning, the old MAF | 10 | 113 | 26 | 25 | 14 | 3.28 | −13 / −9 / +7 / +15 | 10 % |
| `24`–`30`, 24/9–9/10 | 64 | 83 | 6.9 | 23 | 4.2 | 3.08 | −17 / −1 / +8 / +10 | 2 % |
| `31`, `32`, 10–12/10, the NGK plugs and leads, the intake gasket | 85 | 65 | 1.0 | 12 | 3.2 | 2.84 | −14 / −2 / +8 / +8 | 15 % |
| `36`–`38`, 15/10, the DFI can in | 24 | 61 | 6.0 | 13 | 1.6 | 2.66 | −13 / −3 / +8 / +8 | 0 |
| `39`, 18/10, the day of the episodes | 10 | 79 | 14 | 37 | 3.8 | 2.91 | −19 / +2 / +10 / +7 | 0 |
| `40`, 21/10, the VW plugs and leads | 33 | 65 | 3.8 | 18 | 3.2 | 2.82 | −15 / +2 / +6 / +7 | 0 |
| `42`, `43`, 3/11, after both 44K tanks, the flushes and the oil, on the original map | 42 | 67 | 5.4 | 14 | 3.7 | 3.03 | −13 / +2 / +3 / +8 | 29 % |
| `44`, 9/11, before the hydrogen | 33 | 62 | 0.7 | 10 | 2.1 | 2.72 | −13 / 0 / +4 / +9 | 58 % |
| `46`, 9/11, after it | 43 | 63 | 5.6 | 7 | 3.1 | 2.86 | −11 / −2 / +4 / +10 | 47 % |
| `47`, `48`, 10/11 | 49 | 62 | 8.2 | 13 | 2.0 | 3.09 | −14 / +4 / +4 / +6 | 24 % |
| `49`–`51`, the canister | 166 | 61 | 4.3 | 13 | 3.0 | 2.97 | −12 / +1 / +5 / +6 | 42 % |
| `54`, 17/11, the lower gasket renewed, injectors 2 and 3 swapped (`52`, `53` before it: grade 61, 58; common part 2.63, 3.16) | 44 | 63 | 3.1 | 19 | 3.5 | 2.96 | −12 / +2 / +4 / +7 | 34 % |

- **The idle moved twice, and both times at a repair.** **The MAF**
  (24/9, `19` against `24` the same day): the grade 113 → 91, dips of
  20 rpm 26 → 12 a minute, and **cylinder 4 came up from −9 to −4 %**
  with the other three's weak strokes halved (14 → 7 per 1000, most of
  them 4's, `cylscan.py`) — on the old MAF 4 was weak beside 3; 3
  itself did not move (25 → 30) and the common part did not (3.3 →
  3.2). **The plugs, leads and intake gasket of
  10/10** (`30` against `31` the next day, then `32`): 3's weak strokes
  23 → 13 → 11 per 1000, the grade 87 → 76 → 62, the dips 5.3 → 2.0 →
  0.7 a minute; the common part 2.9 on all three. The three parts
  cannot be told apart, nor 12/10's shim and air filter from them.
- **Since 12/10 the mean has not moved**: the grade 61–67 on every
  group of captures but `39`, through the DFI can, the VW plugs and
  leads (`37`, `38` against `40`: 61 → 65, 3's weak strokes 13 → 18),
  both 44K tanks, the two flushes and the new oil, the original map,
  the hydrogen, the probes, the canister and the new valve.
- **What has moved since is how the idle is made up**: a floor in 0 %
  of the warm windows on `36`–`40`, 24–58 % from 3/11, 42 % on the
  canister — and **the swells between are as rough as September's**.
  At an equal deficit of 3's (−16 to −23 %) its weak strokes were
  22–28 per 1000 on `24`–`30`, **13–14 on `31` and `32`**, and are
  **21–30 again on `42`–`44` and `49`–`51`**, and 22 and 24 on `52`
  and `53` (15/11; `swellscan.py --csv`, warm, the A/C off, ×4 for
  3's own strokes) — level since 3/11, neither better nor worse; a swell window's grade
  85, 69, 86, 80. **The gain of 10/10 inside a swell has gone**; it
  holds only where 3 is shallow (−13 to −10 %: 27, 12, and 11–12
  since). When it went the captures do not date closer than between
  `40` (mixed) and `42`. *A finding of this reading, not explained.*
- **The DFI can** (15/10): with it in, the grade 61 against 65 before,
  3's weak strokes 13 against 12, the common part 2.66 against 2.84 —
  the one figure that stood out, a day after every hose was renewed,
  and 2.82 again on `40`; 014's share of combustions 0.27–0.62 % on
  12/10, 0.12–0.22 on 15/10, 0.53 on 18/10. **Nothing that lasted.**
- **The two 44K tanks, the regulator's hose, the flushes and the oil**
  (23–27/10) have no capture between them: `40` before, `42` after,
  with the original map and fresh adaptations on top. Across the lot
  the grade is 65 → 67, 3's weak strokes 18 → 14 (within their
  scatter), the common part 2.82 → 3.03, **cylinder 1 down from +6.0
  to +3.5 %** (±0.4 each; the others taking it up) and the floor
  there. **014 is the only reading inside the bundle**: 0.20–0.33 %
  of combustions on 21/10, 0.14–0.21 on 25/10 (the second can in, the
  hose renewed that day), 0.29 on 26/10 with 055 off, **0.07–0.15 on
  27/10** on the new oil, and 0.06–0.18 on 9–10/11 — **halved inside
  that week and held a fortnight**, and not to be shared out between
  the cleaner, the hose and the oil. The display read 45–90 through
  all of it (the table above).
- **The hydrogen** (`44` against `46`, one day, one tank, one map):
  3's floor −8.6 → −8.1 %, the floor's grade 46 → 63 and its dips
  0 → 4.5 a minute, the common part 2.72 → 2.86; the swells that
  afternoon shallower and calmer (to −19 % against −29; 11 weak strokes
  per 1000 against 25, seven windows) and as before the next day
  (`47`, `48`: 20). **A day's relief in the swell, nothing kept** — as
  H13 has it.

**Read** (*reasoned*). **No cleaner shows on the bus**: not the DFI
can, with a clean pair; not the hydrogen, with the cleanest pair there
is; the 44K tanks cannot be read apart from four other changes, and
what sits across them is 014's share halving and cylinder 1 coming
down — neither is 3's deficit, which in a swell is what it was in
September. **For another can in the tank the record gave no ground**
(*reasoned*; the injectors are new since 23/9, and the strongest clean
of the chambers left 3 where it was) — *until 17/11 evening, when the
time on the floor was read by capture: it rose across the 44K week, so
6t repeats it*. **And the idle does move where
014 and the display do not show it** — in how much of a stop is floor,
which the mean hides because the swells have grown rougher again.

**Each cylinder against the idle's 0.8 Hz swing, and how the weak
strokes follow each other** (11/11–14/11; condensed 17/11, the figures
in `git show 5741dfa:docs/engine-health/open.md`, these headings). The lambda controller swings with a period of
1.2 s at idle; **3 answers no more than the others**, and the misfires
keep to the swing's small-charge half, on 3 most — it does not tell
lean from diluted. **A weak stroke comes in a spell of seconds on one
cylinder** (the same cylinder two to six cycles later 1.9–2.5 × as often
weak), and inside the spell the stroke right after a weak one in the
same cylinder is less often weak (0.87 ×): *reasoned*, the weak cylinder
sits at a mixture or dilution limit, not a spark limit.

**Why the idle got worse in October** (19/10, *reasoned*): the rise
began about 16–17/10, with the cleaner and the hard driving, not an
adaptation; it passed (S1's table, *Every session since the repairs*).

### S2. An occasional puff from the exhaust

*Owner*, at idle, long-standing — before the exhaust work, the injectors and
the MAF. Much weaker than S14's bangs, and in the owner's reading the same
thing smaller: **a misfire's unburnt charge going off in the exhaust**. On
12/10 he heard the puffs **come with the dips** (by ear, not aligned with a
recording). It outlived the resealed joint behind the converter (S6, closed).
**Heard again 26/10** (*owner*), at the warming idle between the two EPR
flushes, on the fresh oil with what EPR was left in it, and recorded by
phone (48 s). Read from the sound (the exhaust note at twice the firing
rate, 65.7 Hz; idle about 990 rpm): **no single stroke stands out** —
of about 1600, none above 1.45× the median pulse — but **four moments,
at about 0:03, 0:12, 0:24 and 0:37, where the exhaust note weakens by
about 20 % and the speed dips about 15–20 rpm for half a second**
(averaged over 0.25 s, so the true dip is deeper), the size of an S1 dip.
**Whether those four were the puffs he hears was never confirmed**;
12/11's recording aligned S2 and S1 instead (below).
**Heard again 9/11 night** (*owner*), standing at a warm idle with every
load off (coolant 92–96 °C, the reading before `plan.md` 8c's swap),
`IdleHealth` about 130 on the display; no capture, so not aligned.
**Heard 12/11 evening at about 17:20** (*owner*, at the tailpipe at
`50`'s last stop, 6p's phone beside it): **the first puff inside a
capture** — in the minute of cylinder 3's second swell at its deepest,
−21 to −23 % with eight weak strokes in 20 s (S1, *The queue drive,
and what the ECU sees through a swell*). "About" a minute is too wide
to name the stroke; the phone's recording, set by the door, can.
**Read that night** (S1, *The phone at the tailpipe through a swell
and a fall*): **every weak stroke on the bus is a louder pulse at the
tailpipe**, +15 to +22 % for a stroke 12 rpm down, so S1's dips and the
exhaust's sound are aligned stroke for stroke, as 26/10's recording
could not show; and **the loudest pulse of the four minutes, +77 % at
17:19:48.9 (3:37 into the first recording), came two firings after
cylinder 3's deepest stroke, −27 rpm** — the owner's reading of S2, a
misfire's charge going off in the exhaust, seen once. **The puff he
heard that evening was this symptom, the one he knows** (*owner*,
12/11 night); whether the pulse at 3:37 is the very one he heard he
has not said.
**17/11, on the new lower gasket and the swapped injectors** (*owner*,
about 06:57, `54`'s warm stop): **the puffs heard as before** —
unchanged by 8z, as 3's swell was (S1, *The first stop on the new
gasket*).

### S3. Misfires counted by the ECU at idle

**VCDS group 014**, 12–120 against VW's 0–5, on every drive since it was
first logged. No fault code is stored (the ECU stores P0300 only above 2 %
over 1000 revolutions, `vcds.md`); **it once did**: P0304 and P0172 in an
old scan of 5/2019 (`vehicle-history.md`).

**When S3 closes** (*the owner's decision*, 12/11): **no count at all —
014 at 0 at a warm idle in the everyday state, on three drives on
different days, after the adaptations have settled**, oil 95–100 °C,
the whole idle long; not one rise, on any cylinder. Strict, by his
choice: the counter steps in twelves, so zero is the only reading
inside VW's specification. *Until 12/11 this read "0 at a warm idle
with loads off for 3–5 minutes, on three sessions" (decided 20/10),
and for a few hours that day "and what it still counts no longer 3's".
It also asked for one session straight after a hard drive* (20/10),
dropped 23/10 at the owner's decision: what that rested
on, 014 counting only after the hard drive of 4/10, was an adaptation
completing rather than load (`refuted.md` C19).

- **Only at idle, and that is the car.** Detection sees a misfire more easily
  under load and switches off below about 20 % load (measured over every 014
  log). Driving with detection `aktivováno`, new counts start once per ~250
  samples, against several a minute standing. **But not never: on 27/10
  (6k's drive) two episodes on the road climbed 12 → 36 and 12 → 48**, at
  1900–2100 rpm and 25–26 % load, and four more counted 12 (once 24) at
  1160–1920 rpm and 25–30 % load, all just above the cut-off. **After the
  pedal was greased (27/10 evening, `vcds-pedal-drive-2-014-003-055.csv`)
  they went on with no tip-in at all**: five episodes of 12–36 at a steady
  2000–2200 rpm and 25 % load, throttle about 10°, while the jerk the owner
  had tied to them was gone (`refuted.md` D6) — so they are not the
  pedal's. With detection `deaktiv.` the field
  reads 13, 15, 16, 18 at each lift: **counted misfires after all**, one
  each, at a weight that grows with load and engine speed, caught in the
  sample where detection switches off (5/11, *What the number is*; this
  said "not steps of 12, so not misfires" until then). The C4 full-load lamp lit on
  this map, so detection under load was not off — **unless the remap dulled
  it** (H14 route 6).
- **The events are the S1 dips** (`tools/s3align.py`, eleven sessions,
  16/10): half of 014's rises sit on a dip in the 1.5 s before, against 22 %
  by chance; a third of the dips get a rise. Over minutes the two part:
  **whether it counts is decided by the load** (`refuted.md` C19; the
  learned idle air as the switch refuted 2/11), not by how rough the idle
  is. **The A/C switches it**
  (*owner*, 16/10): A/C on, 014 at zero for minutes with `IdleHealth` ~70; A/C
  off, it counts and the grade barely moves. *Partly the detector's own
  threshold, rising with load* (*What it counts*, below).
- **What the number is** (5/11, from all 50 014 logs, 31 aligned to the
  bus; `vcds.md`): **the misfires counted in the current window of 200
  crank revolutions, times a weight**, reset to zero at the window's end —
  about 15 s at idle. Between resets the revolutions integrated from the
  bus are k × 200 in 388 of 388 pairs (about 12 % for one pair by chance);
  with one cylinder dead the field peaks at 1,164–1,188 = 97–99 × 12,
  one missed combustion every two revolutions. The weight is **12 per
  misfire at idle below about 34 % load, 13 above**, more above
  2000 rpm. So **12 is one misfire in the last ~15 s**, the owner's usual
  12–48 one to four in 400 combustions (0.25–1 %), and P0300's 2 % per
  1000 revolutions a reading of about 96 window after window; the worst
  natural 1000 revolutions on record are 1.95 % (4/10). VW names the
  200-revolution window for this ECU (SSP 175, catalyst protection). Off
  (`deaktiv.`) the count and the window's revolutions both freeze; the
  first window starts about 5 s after the crank. **Off below a load that
  rises with speed** (about 20 % at idle, 22–25 % at 1400–3000 rpm,
  27–30 % above) and **while speed falls faster than about 100 rpm/s**; no
  temperature condition (it counts below 40 °C of coolant).
- **What it costs the converter** (6/11 night, *the owner's question*;
  *reasoned*, condensed 17/11, the arithmetic in `git show 5741dfa:docs/engine-health/open.md`, this heading):
  at idle 1.06 l/h is about 8 mg of petrol a combustion; burnt in the
  converter, a misfire rate f heats it by about f × 2,500 K — **this
  car's idle 6–25 K, 33 K at the worst minute, 49 K at a cut on one
  cylinder**, against the hundreds of kelvin that melt a substrate.
  Not limited for the converter (*the owner*, 6/11).
- **What it counts** (5/11, the same logs against the bus): **one stroke's
  loss against the one before**, not the dip's depth — a fitted threshold
  of about 19 rpm at 28 % load, **rising 0.33 rpm per % of load**, about
  0.2 s after the stroke; held out one capture at a time it ranks the
  counted strokes with an AUC of 0.85 (0.91 with load and the neighbouring
  strokes). **Isolated weak strokes are counted, clusters and sags mostly
  not** (91 % at a loss of 20 rpm, 10 % when the next stroke keeps
  losing). Two things follow (*reasoned*): **the A/C's silence is partly
  the detector's** — its load raises the threshold — though the grade
  falls with it too (S1); and **`42`'s zero after the map and the reset
  was the detector's state, not the engine** — the bus predicts 55–80
  counting windows there and 014 showed none, which fits the threshold
  Bosch's patents raise until the crank wheel's tooth errors are learnt
  (`refuted.md` C19). **Open**: on `41`'s cold cut (oil 63 °C, 35 % load)
  only about 10 % of the dead strokes were counted, against 87–100 % on
  the warm cuts, though the bus shows the same −25 rpm dead stroke; a warm
  cut with the A/C on would tell load from temperature.
- **Every warm stop with 014 beside the bus, as a share of
  combustions** (9/11, after the clean; the window's counts summed over
  every warm standing stretch of 150 s and more, oil ≥ 90 °C, detection
  on, cuts left out; *ad-hoc script, not kept*): `24` 0.63 %, `28`
  0.60, `31` 0.26, `32` 0.28, `37` 0.20, `39` 0.47, `40` 0.11, 0.46
  and 0.16, `43` 0.12 (after its cut); **`44` (stop 3, before the
  clean) 1.03 up to the cut — the highest on record — then 0.02**, the
  provider's wait with the A/C 0.00; **`46` (stop 7, after it) 0.12
  and 0.14**. Load 22–31 % throughout. **Stop 7 sits with the lowest
  of the settled stops**; stop 3's settled half lower still. **During
  the clean 014 was off** (load about 19 % at 1,750–2,150 rpm), and at
  idle with the gas flowing too (21–23 %). One stop each side: 014's
  storm at the start of stop 3 and its absence at stop 7 are S1's rough
  start on 3 and its absence (S1, *The clean of 9/11*). **10/11, VCDS
  alone, the warm stop after the drive on both new probes** (H11, *The
  reading after the swap*): **0.24 %** — twelve misfires in about 3
  minutes at 32–35 % load, the windows' counts summed the same way —
  between the settled stops, no lower for the probes. **10/11 evening,
  the relearn drive** (`47`, the battery off for hours before it; H11,
  *The relearn drive*): **counting from 16:33, twelve minutes after the
  start** — so not quiet after a disconnect this time; the queue stops
  16:51–17:17 (shorter than 150 s, so summed per stop) **0–0.58 %, 0.24 %
  over them**, the stop at the end **0.15 %** at 25–26 % load, with the
  rear probe reading zero (S23). **12/11, `49`, the first captured stop
  on the canister** (S1, *The first captured stop on the canister*):
  **0.69 %** over its first four minutes (0.46–1.05 % a minute), 3's
  swell, then **0.01 %** — one count in thirteen minutes — on 3's
  floor, at 29–33 % load throughout; on the road five counts of one at
  2,240–3,240 rpm; no code stored.
- **What 014 counts, by cylinder** (12/11, the third research;
  `tools/cylscan.py --vcds`, kept). The ECU has no per-cylinder counter
  (`vcds.md`), but the bus names the stroke: each rise of 014 between
  two samples at a standing idle, recognition on, is put to the cylinder
  of the weakest stroke in the interval before it (the rise shows about
  0.2 s after its stroke; the log set against the capture on engine
  speed to 0.05 s; cuts left out). **1,135 rises** in 27 logs beside 16
  captures:

  | | rises | 1 | 3 | 4 | 2 |
  |---|---|---|---|---|---|
  | `24`–`39` (24/9–18/10) | 840 | 26 | **544 (65 %)** | 252 (30 %) | 18 |
  | of them `31`, `32` (10–12/10, the NGK leads) | 329 | 13 | 162 | 146 | 7 |
  | `40`–`47` (21/10–10/11, the VW leads) | 295 | 13 | **237 (80 %)** | 40 (14 %) | 5 |
  | of them `41` (cold, oil 52–63 °C) | 49 | 3 | 36 | 8 | 2 |
  | `43` (3/11) | 31 | 1 | 29 | 0 | 1 |
  | `44` (9/11, stop 3's storm and the stops before) | 78 | 5 | 63 | 9 | 1 |
  | `46` (9/11, after the clean) | 25 | 2 | 7 | **16** | 0 |
  | `47` (10/11 evening) | 37 | 1 | 35 | 0 | 1 |
  | `49` (12/11, the canister; after the count above) | 41 | 0 | **37** | 3 | 1 |
  | `50` (12/11 evening, the last 84 s of the queue drive's stop; after the count above) | 19 | 1 | **16** | 1 | 1 |
  | `51` (14/11, the new N80: the pump's idle and the two stops' logged parts; after the count above) | 10 | 0 | **7** | 3 | 0 |
| `53` (15/11, 8h's ten minutes of plain idle; after the count above; the three strokes 12 rpm and more down all 3's) | 18 | 1 | **11** | 4 | 2 |
| `54` (17/11, the new lower gasket, injectors 2 and 3 swapped: the second stop, 07:17–07:24; after the count above; 14 of 16 strokes 12 rpm and more down 3's) | 23 | 2 | **16** | 4 | 1 |

  Where the weakest stroke is at least 12 rpm under its median — the
  name is surest there — 3 has 63 % and 4 34 % of 580 up to 18/10, **3
  has 82 % and 4 15 % of 197 since**; 1 and 2 together 3 %. **So 014's
  count at idle is cylinder 3's misfires, with 4's beside them until
  the leads of 10–21/10** — on the NGK leads 4 had as many as 3 — and
  **1 and 2 are next to never counted**. The ECU's own name agrees:
  P0303 on 18/10, after `43`'s cut and on 12/11. `46` is the one
  capture where 4 leads, at stop 7 after the clean and round its cut on
  4. **How deep a stroke is counted** (the same rises; warm, 16,000
  sample intervals): at 20–28 % load a stroke 20 rpm and more under its
  median is counted about two times in three, 17–20 rpm one in two,
  14–17 one in three, 11–14 one in seven; at 31–36 % load one in three
  at best — the threshold that rises with load (*What it counts*).
  *Reasoned*: a count of 12 is a real, nearly whole misfire of one
  cylinder (a dead stroke reads 24–33 rpm in its own slot at a cut's
  first stroke), not the idle's general unevenness; **S3 closes when
  cylinder 3 stops misfiring**.
  **Against chance, 12/11 night** (asked for by the session before,
  `git show c2e9e19:handoff/README.md`): the
  weakest stroke of any few strokes is cylinder 3's more often than one
  time in four, because 3 has most of the weak strokes — so the split
  is to be set against the same pick with no rise, not against 25 %.
  The same pick in the windows 5 s before and 5 s after each rise
  (`cylscan.misfires_014()` with the log shifted; the 24 driving logs
  that line up, their standing idles): **since the VW leads 83 % of
  286 rises on 3 against 50 % of 558 control windows, 1 and 2 together
  5 % against 28 %**; up to 18/10 62 % on 3 against 45 %, 4 34 %
  against 31 %, 1 and 2 4 % against 23 %. Where the stroke is 12 rpm
  and more down: 84 % against 73 % since, 60 % against 53 % before.
  **So the names stand — a rise is next to never 1's or 2's — but 3's
  lead over chance is 83 to 50, not 80 to 25**, and 4's share before
  the VW leads is hardly above what its own weak strokes give by
  chance. **Off idle** (*Naming the cylinder*, *Off idle*): 014 counts
  while crawling as it does standing, and next to never under load.
- **Three properties to keep in mind** (`refuted.md` A11, A12): steps of 12;
  off below ~20 % load; its sensitivity per dip moved five- to fiftyfold with
  the MAF. **So 014 is a yes/no witness, not a ruler.** Compare across time
  with engine speed or `IdleHealth`.
- **An estimate of it on the display since 4/11** (`Misfires` on 0x604,
  *the owner's request*; condensed 17/11, the readings in `git show 5741dfa:docs/engine-health/open.md`, this
  heading): no minute in which 014 counted read zero on it; warm stops
  2–22, drives with little warm idle near zero. ⚠ Not the capture's
  near-zero with the A/C (`40`), read with the compressor's load in b7.
- **By session, 3/10–3/11** (condensed 17/11; every session's counts,
  how far its episodes climbed and the re-read in stretches are in `git show 5741dfa:docs/engine-health/open.md`,
  this list): 014 quiet only on fresh adaptations (3/10 and 4/10 A, and
  `42` on the original map, 3/11), counting again after a hard drive
  (`43`: 10 episodes in 200 s at the warm stop, 9 climbing past 12);
  **no repair of those weeks stopped it** — not the leads (10/10), not the
  regulator hose (25/10, 6i, 6j), not the map. About two episodes a
  minute at a warm idle throughout; **no `IdleHealth` below which 014 is
  silent** at an ordinary load on settled adaptations; loads on (014's
  load above 28 %) silence it at any grade (`refuted.md` C19).
- **The clearing of 24/10 reset 032 to 0.0 / 0.0 and left 055 at −1.31
  g/s** (`idle-log.md`), read once: on this ECU the clearing did not
  restart the learned idle air that C19 then tied 014 to, so 6i and 6j
  count on settled idle air. Whether it restarts the crank-wheel adaptation is
  not known (`vcds.md`).
- **P0300 and P0303 stored on a drive with no cut, 12/11 night**
  (`vcds/vcds-step8n-drive-faults-after.txt`, both 35-00, neither
  sporadic; the memory empty at the start, 00:58): **the first P0303
  without an injector cut since 18/10** (`refuted.md` D10). The engine
  lamp not seen lit or flashing (*owner*). The drive: 52 minutes, a
  brisk motorway stretch, **the limiter touched once** (6,280 rpm,
  about 01:37 by 001) and "a few times" by the owner's account; the day
  before, driven the same way on the new rear probe and the oily G62,
  stored neither. 014 was not in the drive's log, so **when it was set is
  not known**. At the warm stop after it (`vcds-step8n-stop-014-001-036.csv`,
  7.7 minutes, 25–26.5 % load) **014 rose by 12 six times**, about once
  a minute or two. *Reasoned*: whether this ECU counts the limiter's
  cut as misfire is not known; a code on 3 fits H1 and H13 as 3's
  deficit and 014's rises do. Cleared by the owner after the stop, 032/055 read
  first.
- **At the limiter, 17/11** (`54`; *owner*: held at the limiter in 2nd
  and 3rd, by his account the first time so — 12/11 night touched it
  once): 014 rose nowhere under load; its four rises in the pulls' log
  were at idle but one, at 2,080 rpm and 19.5 % load. With 3 level at
  full load (*Off idle*), **the owner's reading: the P0303s of 12/11
  and 16/11 were not set high in the revs** — *reasoned*, it fits;
  neither drive logged 014 while driving, so their time is still not
  known.
- **Fresh adaptations, 17/11** (`54`, after the battery and 098):
  **014 read zero from the start until 07:13:11**, through the warm
  stop with recognition `aktivováno` while 3 had 5–16 weak strokes a
  minute, and counted from then, in the pulls after an engine restart
  — at the second stop 0.23 % (24 in 6.6 minutes). 26 warm cuts before
  the warm stop, 8 of them from 4,150–5,560 rpm, did not start it. **The zero is
  `refuted.md` C19's, not a repair**; which adaptation turns the count
  on stays open.
- **P0300 and P0303 again, 16/11, on a drive with no cut** (the
  album, 13:56: **16684 P0300 35-00 and 16687 P0303 35-00**, neither
  sporadic — the same pair as 12/11; **the engine lamp neither lit
  nor flashing**, *owner*, so set while driving by his reading). Which
  drive is not recorded: the battery was off until the night of 16/11,
  so after it — the gentle drive of 8y (014 read 0 at its end, 03:19)
  or the day's driving. **The second in four days without a cut** (12/11
  above), where the eight weeks before had one, on 18/10. *Reasoned*:
  no lamp fits a code stored on its first trip — a steady lamp needs
  the fault confirmed, a flashing one the converter-damage rate
  (`plan.md`, *Standing items — why*). It names 3 as everything since
  12/11 does and tells nothing between list B's causes. After it the
  owner brought the lower gasket forward (`plan.md` 8z, done 17/11,
  and it moved nothing; `refuted.md` C28).

- **014 on 3's floor and in its swell** (18/11, *the owner's question*;
  each warm 30 s window of `swellscan.py` by 3's state, the 014 logs
  beside the captures on one clock as `cylscan.py --vcds` puts them,
  standing idle with recognition on; script not kept, logs that did not
  line up left out). **Since 10/11 (`47`–`54`): on the floor 16 rises
  in 34 min, about 0.5 a minute, 0.03 % of combustions; in the swell
  148 in 19 min, about 8 a minute, 0.5 %** — sixteen times the floor's
  rate. Over all 26 captures from `24`: floor 0.06 % (53 rises, 56 min,
  most of them `32` and `46`, the morning after the hydrogen, where 4
  led), between 0.19 %, swell 0.56 % (575 rises, 65 min). **So 014
  counts on the floor too, rarely**; `42` counted nothing at all,
  fresh from the map's reset. What 014 counts is 3's swell above all.

- **On the new N80** (14–15/11, `51`, `52`; condensed 17/11, the phases
  in `git show 5741dfa:docs/engine-health/open.md`, this list): at the pump's idle 0.29 % of combustions, at the
  second stop one count in 7.7 minutes; the next day's warm stop **89
  misfires in 18.4 minutes, 0.31 %**, 0.78 % inside a swell and 0.13–0.16 %
  on the floor; **81 of 89 standing rises on 3 (91 %)**. The valve did not
  stop it.
- **By era** (14/11 evening, *the owner's question*: "the 014 records
  are from these days"; every 014 log at a warm idle below 34 % load,
  detection on, logs with a cut, the silent sessions on fresh
  adaptations (4/10's first, 3/11) and the clean's gas left out; a
  script not kept):

  | | idle logged | share of combustions | episodes a minute | climbing past 12 | the longest silence |
  |---|---|---|---|---|---|
  | 11/9–18/10 | 156 min | 0.38 % | 2.4 | 59 % | 4.1 min |
  | 21/10–10/11 (the VW leads, the bypass) | 150 min | 0.17 % | 1.6 | 42 % | 7.4 min (27/10) |
  | 11–12/11 (the canister, the old valve) | 56 min | 0.35 % | 1.6 | **74 %** | **12.2 min** (12/11) |
  | 14/11 (the new valve; three of four swells not logged) | 14 min | 0.08 % | 1.1 | 13 % | 7.1 min |

  **Both records are the canister's days**: the longest silences —
  12.2 minutes on `49`'s floor, 7.1 on `51`'s, 4.2 on 11/11 night —
  and the stormiest plain idle since early October: 11/11 night's
  drive, 224 misfires in 24 minutes of idle, 50 of 65 episodes
  climbing, and the last 84 s of `50`'s stop at 1.02 %. **014's idle
  has split in two with 3's swell and floor** (S1, *Before and after
  the canister and the new valve*): how often an episode starts is
  what it was (1.6 a minute), but it either climbs or does not come at
  all. On the road nothing moved: 4–9 rises in ten minutes in every
  era. *14/11's row is biased low*: the swells went unlogged.
- **The values that are not twelves** (14/11, *the owner*: 16 and the
  like seen on the drive; the first rise from zero in every log, 1,279
  of them): **the weight of one misfire grows with engine speed** — 12
  (24 for two) in all but 17 of 985 below 1,500 rpm (13 above about 34 %
  load); 12–15 at 1,500–2,000; 12–16 at 2,000–2,400; **13–19 at 2,400–2,800**; 15–19
  above. So 16 is one misfire at about 2,200–2,700 rpm, and 13, 15, 17
  and 18 the same thing at other speeds; three quarters of the odd
  values on the road are caught in the sample where detection switches off at a lift.
  14/11 showed more of them than most days because 014 was open on the
  road and closed, for 070, at most of the idle (`vcds.md`).

### S4. Knock retard on cylinder 4 — near the limiter on 2 beside it — and 4 a little short under load

*The heading said "and only cylinder 4" until 12/11* (*the owner*: the
captured drive's 020 changes the symptom, not only its data; *Since
12/11, below*); **widened 12/11 night** (*the owner's decision*: an
extension of S4, not a new symptom) by what 4 gives under load, read
off the bus (*What cylinder 4 gives under load*, below). Groups 022/023 and 020: cylinders 1–3 read zero in almost every sample;
cylinder 4 retards in steps up to 13.5 °CA, mostly on a tip-in after a coast
or gearchange and on hard pulls, **never at idle**. Within VW's 0–15 °CA while
driving. 9/10: still cylinder 4 alone with all injectors seated (`refuted.md`
B7); 10/10, the first drive on new leads: almost none (3 samples); 12/10:
back, smaller, on a harder drive. **On the VW leads** (21/10, `40`):
in 40 % of 020's full-load samples above 3000 rpm, mean 2.5 °CA over
them all, to 11.2, and cylinder 1 in 12 % (to 9.0). **On the original map** (3/11,
`vcds-step5a-pulls-014-003-020.csv`, five pulls to the limiter at
92–106 °C of oil): **cylinder 4 alone in 41 %**, mean 1.1 °CA, **to 6.0**,
at 5000–5500 rpm, retarding and walking back in 0.75° steps; cylinders 2
and 3 once, together with 4, to 3.0 at 6000 rpm; 1 never. **The second
drive** (3/11 evening, `vcds-step5b-pull-014-003-020.csv`, two pulls in
4th to 5,760 rpm at 91–97 °C of oil, short of air, H14): **cylinder 4
alone in 37 %** of 60 full-load samples above 3000 rpm, mean 0.8 °CA,
to 4.5 at 4,700–5,640 rpm; 1–3 never. So as often on
both maps and about half as far on the original: **not the map's** —
less depth fits a milder full-load advance, but 003 reads the same
advance at full load on both (H14). **The captured warm drive, 12/11**
(`vcds-step6w-drive-014-020-033-2.csv`, the original map, five pulls
to 6,000–6,320 rpm and full load at 3,500–4,600 rpm, oil about
100 °C): **cylinder 4 in 47 %** of 335 samples above 3000 rpm at 80 %
load and over, mean 2.2 °CA, **to 12.7 there and to 14.2 on a tip-in
at 3,920 rpm and 16 % load** (11:10:01) — inside VW's 15 — **most of
it at 3,500–4,600 rpm** (54 of 156 full-load samples there, 9–13°),
where the drives of 3/11 had 1 of 40; at the limiter 1.5–6°. **And
cylinder 2 in 14 %** (to 6.0, every one at 5,300–6,300 rpm and with
4), 1 in 4 % (to 5.2), 3 in 2 % (to 3.0), all at the limiter. The
owner read 15–17 on the screen (*owner*); the log's highest is 14.2,
so the screen's figure fell between the logged samples or on another
field (not known). **Not the band alone**: 3/11's two drives had 40
full-load samples at 3,500–4,600 rpm and 4 retarded in one, this drive
54 of 156 — **on the original map 4 now retards there as on the remap**
(`40`: to 11.2); 2 beside 4 near the limiter is new in these logs.
**The symptom changed with it** (*the owner*, 12/11; the heading and
*Since 12/11*, below). *Reasoned*: an arc at lead 4's plug end is
broadband noise in 4's own window (`refuted.md` C24), as is real knock from the crust on
4's crown (`idle-log.md`, 19–20/10).

**Since 12/11: by speed, and cylinder 2 beside 4** (every 020 log
with 014's speed and load beside it; full load = 014 at 80 % and over;
the share of samples in which each cylinder retards, and its most):

| log | 3,000–4,700 rpm | 4,700–5,300 rpm | above 5,300 rpm |
|---|---|---|---|
| 12/10 (`vcds-step3-1-drive-*`, NGK leads) | 4 41 %, to 11.2; 1 8 % | 4 in all 4 | 4 in all 4 |
| 21/10 (`40`, the remap) | **4 31 %, to 11.2; 1 17 %, to 11.2** | 4 40 %; 1 10 % | 4 11 %; 1 22 % (9 samples) |
| 3/11 (`vcds-step5a-*`, the original map) | none in 15 | 4 47 %, to 6.0 | 4 45 %; **2 9 %, 3 7 %, to 3.0** |
| 3/11 evening (`vcds-step5b-*`) | 4 1 of 57 | 4 46 %, to 4.5 | 4 93 %, to 3.0 |
| **12/11** (`vcds-step6w-*-2`) | **4 29 %, to 12.7**; 1 1 % | 4 53 %, to 12.7 | **4 84 %, to 7.5; 2 57 %, to 6.0**; 1 and 3 9 % |
| 17/11 (`vcds-step8z-pulls-*-2`, the new lower gasket, injectors 2 and 3 swapped; the limiter in 2nd and 3rd) | 4 19 %, to 6.0; 1 2 % | 4 30 %, to 9.0; 1 13 %, 3 9 % | **4 96 %, to 9.7; 2 44 %, to 9.7**; 1 28 %, 3 16 % |

- **17/11** (`54`): as 12/11 — 4 the most, 2 beside it only above
  5,300 rpm; over every full-load sample above 3,000 rpm 4 in 36 %,
  mean 1.5 °CA (12/11: 41 %, 2.1). The 15.0 °CA logged on 2 was at
  6,160 rpm and 7.8 % load, the lift after a pull, not under load.
  The swapped injectors moved nothing here either: 2 (now injector 3's)
  and 4 retard as before.
- **2 retards only above 5,300 rpm and never without 4** (0 of 43
  samples on its own); 1 and 3 there in one sample in eleven. On 3/11's
  pulls to the same speeds 2 was in 9 %. So at the limiter all four
  retard a little on 12/11, 4 and 2 the most — **and 2 is the strongest
  cylinder at a warm idle** (S1, *Every stroke named*: +3 to +10 % of a
  stroke, the steadiest), which is what makes it odd (*the owner*).
- **Not odd for knock itself** (*reasoned*, the physics *general*):
  knock comes where the cylinder's pressure and the end gas's heat are
  highest; a cylinder that fills and burns best — 2 at idle — makes the
  highest peak pressure at full load too, so the strongest cylinder is
  the first after 4 to knock. A cylinder that gives least (3) is the
  least likely, and 3 retards least. **Odd for a fault in 4's window**:
  a noise booked to 4 alone (H5) does not put retard on 2, unless the
  noise at 6,000 rpm is long enough to reach the next window (2 fires
  180° after 4, 5 ms at 6,000 rpm) or one sender hears both — which
  sender serves which cylinder is not recorded here.
- **4 deeper in the middle band than on 3/11** (29 % to 12.7 against
  none in 15 and 1 in 57), as on the remap, where the advance at
  3,500 rpm is the same on both maps (H14, *The drive on the original map, 3/11*: 19.5° on both).
  **What differs from 3/11**, none measured against it: the hydrogen
  clean (9/11), the battery disconnect and the clears since (H6), and
  **about a tenth of Orlen Efecta 95 in the tank since 8/11**
  (`vehicle-history.md`); the November air is colder, which goes the
  other way (*general*).

- **Not the rev limiter** (12/11, *the owner's question*: with the
  throttle wide open, the ECU could hold the speed down only by
  retarding). Three things say no: **2's retard starts at 5,300–5,500
  rpm while the engine is still climbing freely** — on the pulls of
  11:00:43 and 11:08:41 the speed rose 5,750 → 6,300 and 5,900 → 6,350
  at a steady 80–89 µl of fuel per revolution until the driver lifted
  (`49`, 0x280 and 0x480 in half-second steps), so nothing was being
  held; **020 is knock control's retard, cylinder by cylinder** (`vcds.md`),
  in the 0.75° steps it walks back in, with 4 at 3.0 while 2 is at 6.0
  in the same sample — a limit on speed would act on all four alike and
  belong to the base advance (003), not to this group; and **the limiter
  sits at about 6,300 rpm** (12/11 night, 6,280), which these pulls
  reached for half a second at most. How this ECU limits speed is not in
  its documentation here; Motronic of the time usually cuts injection
  (*general*), and with a cable throttle that is what it has besides the
  spark.

**What cylinder 4 gives under load, from the bus** (12/11 night;
`tools/drivescan.py`; *Naming the cylinder*, *Off idle*): **4 gives
2–4 % of a stroke less than 1** — the two cylinders the crank wheel
reads alike — from 1,600 rpm up, at every load from part to full, on
sixteen drives, `19`–`50`: +1.2 to +2.5 % at 2,100–3,300 rpm
and full load, +2.6 to +3.2 at 3,300–4,200, +3.8 to +4.4 at
4,200–5,200 (±0.2 to ±0.8). **It is there at part load too** (+2.6 to
+3.5 % at 1,600–2,600 rpm, b7 about 62), where 020 reads no retard, so
the retard is not all of it; where 4 does retard, a few degrees cost
about this much (*general*). At idle 1 less 4 is +5 % since the VW
leads and was +10 % before. **Part of S4** (*the owner*, 12/11 night).

**Why 4, and why the other way round from 3** (*the owner's question*,
12/11 night; *reasoned*, nothing here measured beyond what is cited).
**It is not the other way round**: 4 is a few per cent under 1 in
every state — 5 % at idle, 2–4 % under load, a share; 3 has something
on top of that only where the charge is small, an amount. Two
different things, not one cause with two signs. **For 4, three
readings**:
- **Real knock from the crust on 4's crown** (H13): retard costs
  torque, so 4 is short where it retards. Against it as the whole:
  4 is as short at part load, where 020 reads no retard; 3 has more
  deposit than 4 and retards least; and the clean of 9/11 was followed
  by more retard, not less.
- **4 fills or burns a few per cent less at every load** — the crust
  round the inlet seat's edge on 4 (the port photos of 20/10), runner
  4's torn gasket edge, or less lift at one of its valves. A share, as
  measured. On its own it would make 4 the *least* likely to knock, so
  it does not explain the retard.
- **Something mechanical at 4 that does both** — a valve, lifter or
  cam lobe on 4 that lifts short and is heard: less filling at every
  load (the share), **a noise in 4's window with no load at all** (S5:
  026 reads 4 20–70 % over 1 in neutral, which knock cannot be) that
  the ECU books as knock (H5), and a tick once per cycle (S22, on a
  cylinder no recording has named). **The one reading that takes S4's
  retard, S5 and the 2–4 % together**, and it is H5 with a part named.
  Against: 2 beside 4 near the limiter (above) is not explained by it.
**What would tell**: the stethoscope on the cam cover above each
cylinder, hot, and VW's tappet check (`plan.md` 9, there for 3) —
**listened to and checked on 4 as well**; 026 in neutral again after
any work on 4's valve gear.

**What it changes in the hypotheses** (12/11, at the owner's request;
*reasoned*; **no fit-table symbol changes**, each said why):
- **H5** (something in 4's window that is not combustion): ✔ stays —
  4 alone below 5,300 rpm, as always; **weakened at the top**, where 2
  beside 4 points to combustion or a noise heard in more than one
  window.
- **H13** (deposits): ~ stays. The crust on 4's crown (the borescope)
  is a reason for 4 to knock; **2's crown has a thin layer only**, so
  not for 2; and a clean that took deposit away (9/11) was followed by
  more retard on 4, not less — weakly against H13's form for S4.
- **H14** (the remap): ~ stays. **The middle band is not the remap's**
  — 4 retards there on the original map as on the remap, at the same
  advance; above 5,300 rpm, where the remap did differ, `40` has too
  few samples to compare.
- **H6** (knock control relearning after a disconnect): fits that S4
  changes between logs; 3/11 was the day of the flash and 12/11 two
  days after the disconnect, both on young adaptations — not telling.
- **H4 / H21's shared earth** (S4, S5 through a common sender earth):
  noise there would reach all four windows, which the small retard on
  1 and 3 at the limiter allows; ~ as it was. *15/11, 8h*: the knock
  sensors' 026 voltages did not move with the electrical loads (±0.03 V)
  and no sender referred to the ECU's earth moved on its own (H21,
  *8h, the loads at a warm stop*) — against the common earth at VCDS's
  second (`refuted.md` C26); H4's ~ kept on its other paths, the coil's
  feed and the loom.
- **H1, H3** (3's valve, runner 3): nothing — 3 retards least.
- **The idle's ranking is untouched**: S4 is outside it (*owner's
  decision*, 9/10) and its column moved no symbol.

### S5. Cylinder 4 reads high in group 026 (knock sensor voltage)

With no load at all, standing in neutral, cylinder 4 reads 20–70 % above
cylinder 1 from about 1400–2700 rpm up; above ~3350 rpm the excess moves to
cylinder 1. So **not knock** — knock needs cylinder pressure. At idle all four
sit on the floor. 1 and 4 reading twice 2 and 3 is explained without a fault
(`refuted.md` B2). ⚠ 026 includes the ECU's amplifier factor, and 1 and 4 are
probably on different sensors.

### S11. A hiss at the back of the engine at a warm idle

*Owner*, from 26/9. It outlived the new breather and cover gasket. Closed
12/10 and **reopened 14/10** (*owner*): heard again, roughly **on the right
side, near the throttle or the hose from the MAF to it**, only with his head
by the hoses. Moving the hose and covering places by hand changed nothing.
**His own reading: it may be normal** — idle air past the nearly shut plate
under manifold vacuum (*general*). Kept open with that note; no test planned.
If it is a leak: behind the throttle it is H3, ahead of the probe H2.

**16/11, heard again lower down** (*owner*, by his own words perhaps
placebo, nothing conclusive): above the cam cover hardly, **a head's
height lower clearly** — so it could come from the lower intake
manifold; and to his ear **certainly a fault, not the engine's own
sound**, which withdraws his "may be normal" of 14/10. *Reasoned*: the
lower manifold's joint to the head lies below the cover's level, the
throttle and the MAF hose above it, so a lower source points at H3's
joint rather than the throttle's own air; the ear cannot place a hiss
to a runner. **Its test is the first warm idle on the new gasket**
(fitted 17/11): a hiss gone after it is H3's (`plan.md` 8z).
**17/11: still there on the new gasket** (*owner*, about 07:01,
`54`'s warm stop) — **not the lower joint** (H3, `refuted.md` C28,
whose fit table went with it); what is left is the throttle's own air
or a leak ahead of the probe (H2).

### S12. A sudden jerk at a crawl and on moving off

*Reopened 10/11 night at the owner's request*, in a new form; its
history, closed twice as play (4/10) and as a sticking pedal (27/10), is
`refuted.md` D6. **Now** (*owner*): **now and then, creeping gently, the
car gives one hard jerk, as if someone had let go of the throttle
abruptly; and the same when moving off. Not every time. Not the
pedal**, which has moved smoothly since it was greased (27/10).

**Looked for on `47`** (10/11 evening, about 40 moving-offs and long
crawls in the queues; *ad-hoc scripts, not kept*): **nothing that can be
named a jerk**, and none of the times is known. (1) Engine speed at a
steady pedal: every fall of 60 rpm and more in 0.3 s at under 25 km/h
lies at a gearchange or a lift (the pedal at rest, b7 falling), a
clutch the bus cannot see. (2) The car's own speed: 0x1A0 below about
10 km/h moves in steps held for tenths of a second, so its derivative
makes false decelerations of 1–2 m/s² at every step; at the candidate
moments engine speed showed no stumble. **The bus cannot show this
symptom at a crawl** (*reasoned*). (3) **014 counted at moving off**:
seven single misfires on the road (12–18, `aktivováno`) at 43–57 % load
— 16:34:33, 16:46:01, 16:47:35, **17:15:52** (0–8 km/h, 757–1,114 rpm in
the 15 s before), **17:19:30** (0–6 km/h), 17:23:02, 17:26:00 — and
**each window held a moving-off from standstill**; a misfire under load
in first gear is a torque step the driver feels (*reasoned*). Whether
he felt one then is *not known*.

**To catch it**: say "teď" (now) in the chat the moment it happens on a
captured drive, or note the clock; a capture with a word at the time
names the stroke, the load and the cylinder.

**16/11, the owner's reading and two new forms** (*owner*): he holds the
jerk to be cylinder 3's — 3 has a charge above which it hardly misfires,
and **every moving-off, above all from the overrun into an ordinary
pull at a light pedal, crosses it**; and **the traction control has
cut in where it has no business**, once **between 3rd and 4th on a
dry road** at full throttle, power the car does not have to spin a
wheel; is it the same thing, a stupid traction control at a light
moving-off as well, or 3's burning fooling it? *Looked for*
(`47`, `49`–`53`, and every `_z1` capture for 0x1A0; three unfiltered
captures from the release for the wheel speeds, 0x4A0; *ad-hoc
scripts, not kept*):
- **The overrun into a pull** (`drivescan.py`'s windows, warm, 1,150–
  2,600 rpm, b7 30–140; 292 windows in the 3 s after an overrun of a
  second or more, against 3,366 in steady driving): **3 less 2 −2.9 ±
  1.7 % of a stroke after the overrun, −5.8 ± 0.3 % in steady
  driving** — 3 no weaker there. Strokes half a stroke under their
  neighbours **four times as many after the overrun (about 11 per
  1000 against 3), and on all four alike** (1: 10.6, 3: 11.3, 4: 10.2,
  2: 11.3): the shunt of a load reversal through the driveline, not a
  cylinder. And 3's deficit fades with the charge gradually (*Naming
  the cylinder*, *Off idle*: −24 % at a light pedal, −9 % pulling at
  idle speed, −2 to −5 % at part load), with no step to cross.
- **At a crawl and moving off, up to 1,200 rpm**, 014 counts what it
  counts standing — two thirds of its rises on 3 (*Off idle*, C), and
  on `47` seven single misfires each in a window holding a
  moving-off (above). **There the owner's reading stands**: one
  stroke in four missing in first gear is a torque step he would feel,
  and it is 3's. Not shown is that a felt jerk was one.
- **The traction control, 0x1A0** (opendbc's `Bremse_1`: b0 bit 0 the
  ASR's request, b4–b5 its torque limit, bit 2 ABS braking, bit 3 EDS,
  bit 4 ESP): **the torque request twice since September** (`40`, 21/10
  and `46`, 9/11), **both at a full-throttle change from 1st to 2nd**
  at 45–50 km/h and 3,200–3,900 rpm, the torque held to 39–54 % for
  1.0–1.6 s; on 9/11 the front wheels ran 5–6 km/h ahead of the rear
  (13 %) as the clutch bit — **real wheelspin, rightly caught**; the
  rest on private land in 1st (`17`, August). **Never at a light
  pedal, never at 3→4** in any capture; ESP's bit never set. **EDS
  once at a crawl** (`31`, 10/10: 0.4 s at 3 km/h, the pedal at 21 %,
  lifted at once after) — EDS brakes a spinning front wheel, which is
  felt; its cause there is not on the filtered bus. **ABS braking
  flagged for 10 ms, about 30 times, with no brake pressed**, each at
  a one-sample dip of 2–4 km/h on a rear wheel (six of six checked,
  four of them the left rear) — a bump or the sensor; with no brake
  applied it acts on nothing.
- **Can 3's burning fool it**: *reasoned*, no — the traction control
  reads the four wheels' speeds against each other, and a misfire
  takes torque away, which spins no wheel. A rear wheel's speed
  dipping for a sample, as above, makes the fronts look ahead of it
  for that moment: **if anything gives a traction cut at 3→4 on a dry
  road, it is that** (*reasoned*, not seen).
- **To catch either**: "teď" on a captured drive — the unfiltered
  upload keeps 0x4A0, so a cut is read wheel by wheel.
- **The traction cut at 3→4 is a note to S12, not a symptom of its
  own** (*the owner's decision*, 16/11).

### S14. Bangs from the exhaust on a downshift without a blip

*Owner*, 4/10: on a downshift **without a throttle blip** a series of small
bangs, 1–2 s after the clutch comes up; with a blip almost never; warm. Gone
9–14/10, **back on 15/10, quieter** (*owner*), with the joint behind the
converter tight — so that joint fed or carried it at most. **28/10**:
on every downshift without a blip, **no more often than before, only more
muffled since the joint was sealed** (*owner*). Read as
(*reasoned*): the engine dragged up on a shut throttle is fuelled at its
thinnest charge; a charge that fails to fire goes out as fuel and air and
burns when the fuel cut pumps plain air in after it — **a misfire where 014
is blind**. The ECU cuts the injectors 0.8–1.6 s after the lift
(`coastscan.py`). **The owner's to watch, not in `plan.md`** (*owner's
decision*, 4/10): worked on only if it outlives S1/S3.

**Does it keep to cylinder 3, as the idle's dips do?** (6/11, *at the
owner's request*; every coast with a fuel cut in the `_z1` captures,
655, `tools/coastscan.py`'s windows; *an ad-hoc script, not kept*.)
**It could not be named then**: a cylinder was named only by phase
carried from an injector cut at idle, and on the road the phase was not
kept that far. *Since 12/11 `cylscan.py --wheel` carries one stroke
count from an overrun into the standing idle after it (13 overruns),
which could name the fuelled strokes of such a coast; not read — S14 is
the owner's to watch.* **What the bus does show**: with the pedal up,
the strokes still fuelled before the cut (from 0.7 s after the lift)
have the same mean stroke-to-stroke step as the cut ones at the same
speed — the car, not combustion, holds the crank's speed in gear — but
**more large steps**: the 95th percentile 13–16 rpm against 9–14 at
1200–2600 rpm. So the thin charge on the overrun burns unevenly enough
to be seen, the mechanism S14 is read by (*reasoned*; the ECU's own
torque reduction before the cut would look the same, not ruled out).
**Not on one cylinder**: in the 20 fuelled stretches with the phase
intact and three or more large steps, the top slot holds 45 % of them
against 49 % by chance (p 0.9). No sign that S14 shares the idle's
cylinder; nor can it be excluded, with so few strokes per coast.

### S16. A tick in neutral, cold, with the clutch pedal up

*Owner*, 12/10: a regular tick at a cold idle in neutral, **gone with the
pedal down** — the gearbox side. **Not pursued** (*owner's decision*): the
idle graded the same pedal up and down (H12). Out of the fit tables.
**A link not looked at before** (6/11, *general*, *reasoned*): rattle
from a gearbox in neutral with the clutch engaged is excited by the
crank's unevenness at idle, so the tick could be S1 heard through the
gearbox rather than a fault of its own. Untested; the owner's ear would
say it: does the tick follow the felt dips, and does it fade with the
A/C on, when the idle is calmer (S1)?

### S17. A new exhaust sound, from a new place

*Owner*, 15/10: only at about 2200 rpm, **like a resonance**, perhaps the
remade joint behind the converter, perhaps nearer the engine. A sound tied to
one engine speed is a part vibrating, not a leak (*general*), so it bears on
no hypothesis about the idle. Out of the fit tables until placed.

**31/10: taken for the sheet-metal heat shields around the exhaust**
(*owner*: "that is it"), **and still heard after their new clips** the
same day (*owner*), so not them, or not only them; *this said "placed"
until then*. They rattled at certain engine speeds; held
once before with nuts over the old clips, a stopgap that did not hold,
so the resonance stayed (*owner*; when not given). **The shields were
loose before the new clips; the joint behind the converter checked and
"held as if nailed"** (*owner*, 31/10), so not the joint. **New clips
fitted 31/10** (`vehicle-history.md`). **Where it is now** (*owner*):
perhaps nearer the engine, where a lot else resonates, so hard to say.
**Looked over from below again, the engine included** (*owner*, 31/10):
nothing moves anywhere; a few sheets bent a little, just in case, without
much faith. He may try to locate it with a second person at the
throttle. Unplaced again, and not pursued. A candidate there (*reasoned*): the
manifold's own heat shield, which cannot be seen — a part
vibrating, not a leak, so still no bearing on the idle.
**The same band in 014 on the road** (6/11, *at the owner's request
for new links*; every VCDS log with group 014, detection on, above
1100 rpm and at 32 % load or less, increases within 20 s taken as one
episode; *an ad-hoc script, not kept*): **2000–2400 rpm, 35 episodes in
24 minutes (1.45 a minute), against 13 in 21 minutes (0.63) at
1600–1800 and 2400–2600** — about 2.3 times, p about 0.005 for so many
by chance, the band chosen from S17 beforehand; spread over 16 logs,
not one drive. **What does not follow it**: the bus's stroke-to-stroke
roughness at steady throttle on the road (second difference of the
180° speed, 1300–3200 rpm, every `_z1` capture) rises smoothly with
speed, with no peak at 2200; and S5's excess on cylinder 4 begins
about 2000 rpm but keeps growing to 3200 (`vcds-neutral-026-003.csv`
and its clamp log), no peak either. **Read** (*reasoned*): a candidate,
not a link — a crank-synchronous vibration there could feed both the
knock sensor's window and the misfire detector, or the detector's own
thresholds may simply be lowest there. **A test without new kit**: hold
2200 rpm on the road in two gears, VCDS on 014, and say in the chat
when the resonance is heard; counts that follow the engine speed and
the sound, not the gear, would make it one thing.

### S19. P0172 stored, too rich — with one start that died at once

**16556 / P0172, bank 1 too rich, 35-00, not marked sporadic** (P1240 beside it was), found in the fault memory before
the cold capture on the night of 24/10 (`idle-log.md`), **the first since
5/2019** (`vehicle-history.md`), and set some time after the last empty
reading. The same window holds **the one bad start of that afternoon**:
after about 4 hours parked nose uphill the engine caught and died at once,
the next start normal (`idle-log.md`, 24/10). **The two are suspected to be
one event** (*owner's decision*, 24/10): a flooded start reads the same to
the driver as a starved one, and an injector or regulator that lets fuel
into a cylinder while the car stands would give both (*reasoned*). The
trims behind it were lost to the clearing before 032 was read
(`CLAUDE.md`). Also in the
window: the first tank of Orlen Verva 100 and two 170 km drives held at
5000 rpm. **It cannot be dated more closely** (28/10): this ECU's fault
memory carries a code and its status only, no mileage, time or freeze
frame (`photos/vcds-faults-2026-10-26-after-flush2.jpg`), so the window is
everything between the empty reading of 23/10 and the night of 24/10 —
and it **opens before the fill**, with the drive out on the old tank (OMV
and the first 44K) run down to 0.4–0.7 l. Before the window nothing points
at it: 032 −3.1 to −6.3 % (19–23/10), the live regulation at a warm idle
centred on 0 with no excursion past −5.5 % (21/10, VCDS 001). **What sets it is not
known**: VW's manual gives 032 a range of −10 to +10 % (`vcds.md`), which
is the specification, not the code's condition, and the label file holds
none. **It is not the idle cell reaching −10 as VCDS shows it**: on 25/10
night, with the regulator's hose off, the idle cell went to **−12.5 %**
for about 40 s (`vcds/vcds-step6e-cold-2-001-032-033.csv`) and the fault
memory was empty afterwards. The part-load cell is positive, the other way,
and has been on every reading since the new MAF (24/9): +1.6 to +5.5 %
up to 23/10, +6.3 to +8.6 % since 25/10. *This said "since 25/10", which
held only for the higher values (the owner, 28/10).*

**Not settled that the start set it** (*reasoned*): a start that dies at
once runs on a cold probe, open loop, and cannot itself trip a trim fault;
what would link the two is **one cause** that puts in too much fuel, seen
once at the start and once later in closed loop. **Read by what followed:**
032's idle trim well negative at the next reading, or P0172 back with no bad
start, says a standing cause rather than a one-off — **and the idle trim
has been −7.8 to −8.6 % on every settled reading since (25–27/10)**,
while P0172 has not come back: a standing cause, below the code's
threshold; P0172 back after
fills only would point at the purge path (*general*: a canister flooded by a
brim-full fill), which 070 found sound on 27/9 (`refuted.md` A6) but not
since — and 070 shows that the valve opens, not that it seals (H16).
The 001 of 24/10 night, with the stored adaptation still in force, read
**+15 to +22 %** while warming and about **−3 to +1 %** warm — adding fuel
cold, near zero warm, which a hard rich fault would not show; weak, since
it is the trim on top of an adaptation not read. **The misfires make it
stronger, not weaker** (*reasoned*, as `refuted.md` A7): an unburnt charge
carries oxygen to the probe and reads lean, so with 014 counting the
mixture is if anything richer than the trims say. And **it all but rules
out a meaningful intake leak** (A7): that would have pushed the other
way.

**032 after every reset and repair, and on the new lower gasket, from
zero** (idle cell / part-load cell, %;
condensed 17/11, each reading's circumstances and argument in `git show 5741dfa:docs/engine-health/open.md`,
under *The new probes, 10/11* to *The cell over the three months*):

| when | what changed | 032 |
|---|---|---|
| 20/8, 10/9 | before the repairs, old injectors and MAF | −5.5, −4.7 idle |
| 31/10 | the OMV tank (S7 closed as the fuel, `refuted.md` D2) | −7.8 / +7.0 |
| 3/11 | **the original map**, reset to zero | −6.3 / +3.1 in one drive, **−7.0 / +6.3 settled (6/11)** — neither cell the map's |
| 10/11 | **both probes new**, reset by the battery | −6.3 / +7.0 within 37 min, −3.9 / +7.0 at the end — neither cell the old probes' |
| 11–12/11 | **the canister plumbed back**, from zero | −3.9 / +2.3, then −7.0 / +8.6 after a brisk drive |
| 14–15/11 | **the new N80** (−9.4 / +7.8 on the old valve before it) | −8.6 / +7.8, then −9.4 / +5.5 after a gentle drive |
| 16/11 | **the MAF's plug and the ECU's earth cleaned** (C27) | −5.5 / +5.5 after one drive |
| 17/11 | **the lower gasket, injectors 2 and 3 swapped** (`54`) | −7.0 in the warm stop, −6.3 / +7.8 at the end, learnt with 070's valve shut |

**No repair moved the idle cell towards zero** (*the owner's
observation* that it grows more negative is not shown: each reading
stands a different distance from a reset). The part-load cell learns
first, the idle cell follows within a drive.

**The old logs re-read for the split's form, and what the split is**
(15/11 night and after; condensed
17/11, the research — Bosch's sorting of mixture errors, the purge and
adaptation patent, the trade's reading of opposite signs, the MAF's
plug, the supply — in `git show 5741dfa:docs/engine-health/open.md`, this heading):
- **With the cells learnt the regulation is flat everywhere** (16 logs
  by speed and air per stroke: 85 of 99 cells within ±1.0 %), and **the idle cell is worth its figure**:
  −8 % is about 8 % of the idle's fuel.
- **The idle's extra fuel stepped in at a standing idle**: on 8n −2.4 %
  for the first 80 s, then −5.9 % within a minute and a half — the
  timescale of the ECU's purge; **learnt with the valve shut** (b7 on
  the old logs, 070 on `54`), so **the −6 % is the engine's own, not the
  canister's vapour** (H16 refuted, `refuted.md` C30).
- **Ruled out by repair or test**: the injectors (both sets), either
  MAF, either pair of probes, either map, the fuel, the regulator's
  vacuum reference (C20), the purge (C30), the MAF's plug and the
  ECU's earth (C27), the supply as the ECU sees it (half a point for
  half a volt at most).
- **Left — VW's own list for an idle value low with part load normal**:
  **a leaking injector and fuel pressure too high**, both read by 8u's
  gauge; and **the return's form** (*reasoned*): a restriction between
  the regulator and the tank backs the rail up most at idle, where most
  fuel returns — the split's shape, which 6e's hose test cannot see.
  The ECU's own reckoning of a short injection is not excluded.
  **Re-reckoned 17/11** (the fourth research, *reasoned*; *What the
  forums say*, searched again 17/11): the pump delivers an order more
  than the engine burns at idle or at part load, so a return
  restriction or a high base pressure raises the rail nearly alike in
  both and would pull both cells negative — **the return's form
  weakened**, the gauge (8u) still its test. How M5.9.2 combines the
  additive idle cell with the multiplicative part-load factor at idle
  is not documented; if both act there, the net learnt correction at
  idle is near zero. A front probe weighting a rich 3 (CARB's case)
  fits the sign, a point or two in size.

### S20. Engine speed wanders at a constant pedal

*Added 26/10 at the owner's request.* **During the first EPR flush**
(26/10, `idle-log.md`), standing in neutral, the pedal held by a stick of wood:
the speed swung a little at first, held about 1250, then rose slowly to
about 1300 by itself, and **"it just fluctuates"** (*owner*). **His
9 s video** of it, read from its sound (the firing rate in the clicks
above 3 kHz, 1 s windows): **1266–1294 rpm for 4 s, then a step down to
1215–1241** for the rest, ±10–15 rpm within each. **Over the flush**
(*owner*, off the display): mostly swinging **1250–1300**, now and then
settling at about **1230**; **the stick does not move at all**. **A 3-minute
recording** at about minute 22–25 of the flush, read the same way (1 s
windows): median **1260**, mostly 1240–1290, swinging 10–20 rpm over
seconds; **once a lower, calmer stretch of about 28 s at 1195–1222**,
entered by a drop of about 45 rpm within 2 s and left by a rise, and
one shorter dip to about 1205. **Two states, then: lower and calm,
higher and swinging** — the video's 1266–1294 → 1215–1241 the same
pattern. What switches between them is not known; an on/off load such as
the radiator fan, or the purge valve's cycles (H16), would give a step at
a held plate (*reasoned*); the sound shows no fan switching clearly.
**The flush's part is weak since** (*owner*, 26/10, in the second
flush): setting the stick so that it did not move turned out hard, and
the swing may have been the stick after all; set again, it sits at
1250–1300. **And the ECU was in it** (*reasoned*): **P0507** set in the
first flush and **055's learnt value went to −2.10 g/s**, so the ECU took
the held engine for an idle running high and worked its idle control
against it; with the plate near its stop, a controller pushing against a
held pedal could itself give a speed that swings and steps. **So S20
rests on the road observation**, not on the flush.
**Also on the road**
(*owner*): hard to hold the engine speed steady, **noticed since the job
of 1–2/10**, which fitted **the new throttle** (Pierburg `7.03703.13.0`)
and **took up the throttle cable's slack** (`idle-log.md`, *1–2/10 — the valve
cover, throttle and breather job*); the same job renewed the cover gasket, the
plenum gasket and the breather.

**Not S1.** S1 is dips at idle with the idle governor in charge; this is
above idle with the pedal held. **The pedal works the throttle by a
cable** (*owner*, 26/10, off the car; *this said the pedal was a sensor
and the ECU moved the throttle — wrong*), so with the pedal held the plate
is held, and what wanders is the engine's torque at that plate, or the
plate itself through the cable and the idle stop. ⚠ **Soft**: it was
seen with EPR, a solvent, in the oil. The stick is not it (*owner*: it
does not move).

**The captures show no change with the new throttle at part throttle**
(26/10). Every stretch of at least 2 s with 0x280 b5 not moving by one
count, above 15 km/h, in one gear, oil above 80 °C; the rpm's scatter
about its straight-line trend in each: **1500–2500 rpm, part throttle,
5.3 rpm on the old throttle (`19`, `24`, 84 stretches) against 4.1 on
the new (`26`–`40`, 137)**; 2500–3500 4.3 against 4.2. Only full
throttle above 3500 rpm reads higher on the new, 9.0 against 5.9 — pulls,
far more and harder after 2/10, not a held speed. ⚠ What this cannot
see: a wander slower than a few seconds, which on the road the gradient
hides, and a standing hold above idle, which no capture since 2/10
holds. *An ad-hoc script, not kept.* A capture tells them apart:
0x280 b5 is the throttle, so stretches where it holds still show whether
the speed wanders anyway.
The slow rise to 1300 reads as the oil thinned by EPR and still warming,
less friction at the same throttle (*reasoned*); the swings and the step
do not.

**Since 27/10 the cable is slackened and the pedal greased** (S12 closed
on the pedal, `refuted.md` D6): a pedal that stuck in small jumps near the
start of its travel holds a plate unsteadily too, so S20 may have been
the pedal. **It outlived them, a little better** (*owner*, 28/10): the
pedal was part of it at most.

**The first capture since the pedal, 3/11** (`42`, the original map; *the
owner's question*). **With the plate held** (0x280 b5 within ±2 counts
for 6 s and more, part throttle, above 40 km/h): the speed's scatter
about its trend **0.14 km/h**, engine speed 0.19 %, against 0.16 / 0.31
on the old throttle (`19`) and 0.12–0.17 / 0.23–0.26 on the new
(`31`, `37`, `40`) — **a held plate holds the car, on every throttle**.
**How still the plate is held** at a cruise (5 s windows, 50–130 km/h):
the plate's spread **2.8 counts** on `42`, against **3.2–3.5 on the old
throttle** (`19`, `24`) and **5.5–8.1 on most drives with the new one
before the pedal was greased** (`30`, `31`, `32`, `37`, `40`; `39` 3.5,
`26` 1.2 with few windows). **Read** (*reasoned*): S20 lives in the
pedal, the cable and the plate, not in the engine — the engine holds a
held plate steady — and since 27/10 the plate is held as still as on
the old throttle, which fits "a little better". ⚠ `42` is mostly
motorway, where a foot holds still more easily than in town; one drive.
The map does not reach this range (H14).

### S22. A tick once per engine cycle — reopened 11/11 night

*Added 9/11 at the owner's request, closed that evening as the hydrogen
clean's own sound (`refuted.md` D11, which keeps the entry as it stood:
the recordings, the burst pattern, the read), **reopened 11/11 night at
the owner's decision**.* **Heard again warm with no clean**: on 10/11 at
an idle loads off, and **on 11/11 night at the warm stop after a hard
motorway run** (oil 102 °C, the everyday state, bonnet down, from the
driver's seat), **"the same pattern, or nearly, only quieter" than
during the clean** (*owner*); recorded at the engine bay (the album,
11/11 21:55), read 12/11 (below). *This said "not yet read" until then.*

**Read** (*reasoned*): with no oxyhydrogen in the charge, D11's
explanation — the clean's faster burn making a usual difference louder
— does not reach it; what stays is D11's own list: **one valve's lifter
(H1), one injector (H7), one cylinder's port leaking at its joint
(H2), or one cylinder's combustion different from the others** (S1, *A
steady pattern over the cylinders*). Louder during the clean fits a
part whose tick the faster burn masked less, or one cylinder's burn —
the recordings did not tell them apart then either. **A lifter that
ticks warm after a hard drive** is what H1 predicts and what the hot
recording of 26/10 did not find.

**The recording of 11/11 read** (12/11, a cloud session; album
21:55:11, 40 s, the phone held close over the plenum's cast runners,
neutral, warm, just after the motorway run; *an ad-hoc script, not
kept*): the envelope of the sound at 2–12 kHz, the engine speed from
its own firing line — **about 800 rpm throughout** — and the envelope
spectrum's amplitude at the camshaft's frequency over its median in
3–100 Hz. **In 3 s windows the once-per-cycle rhythm stands 5.5–9.6
times the median, about 7 in the middle**; the firing line itself
13–18. That is **D11's own range for 3 s windows (3–10) and the size of
9/11's idle after the clean (7.8) and 15/10's warm idle (7.1)**, not
18/10's 16.4 with cylinder 3 out. Folded on the cycle, **one of the
four firings is 1.2–1.4 times the mean of the four in every window**,
and **it is loud** (above 1.5 times the other three) **in about a
quarter of the 251 cycles**, mostly single cycles, a few runs of 3–9
(0.5–1.4 s) — D11's bursts, at idle. *D11 does not record its window
for the per-video figures, so those compare in order of size, not to
the decimal.* **Read** (*reasoned*): **the tick he heard is the same
once-per-cycle part every engine-bay recording has carried since
12/10, at its usual size** — it did not grow after the hard drive,
which **a lifter bleeding down hot would have shown as a jump towards
18/10's**. It does not say which cylinder: one
microphone cannot. It leaves H1's lifter where it was — not found by
the sound, not excluded — and the stethoscope as the test.

**The cam cover above 3, 15/11** (6p's second half, at `52`'s stop;
S1, *The phone on the cam cover through a swell and a fall*): the
phone lying on the cover for ten minutes, every stroke set on the
capture — **at 1–11 kHz four bumps a cycle within a tenth of each
other, no once-per-cycle tick at 3's place or any other**, on the
floor, in the swell and after the fall. The tick was not reported
heard at that stop, so this is the cover's usual sound, not the tick
caught; a telephone through speech compression.

**Tests**: **the stethoscope on the cam cover above each
cylinder, hot** (`plan.md` 9); VW's tappet check in item 9's garage
session.

### Other — not symptoms, but they touch this file

**Oil temperature.** 0x420's `OilTemp` is `raw − 60` °C (`docs/firmware/can-decoding.md`
question 10, closed 23/10). A bias moves both sides of every comparison alike.

**The remap.** The ECU was remapped in 6/2018, "mild", the tuner finding
nothing at the top. Written down as H14 (16/10). Not written back on 22/10 (*owner*,
20/10); **written back on 3/11**, the tuner's original and remap compared the same day,
privately, never in this repository. **3/11, at the tuner**: the ECU out —
VW `06A 906 018 EJ`, *BENZIN V04*, Bosch `0 261 206 327`, made 15.06.99 in
Mexico (*owner's photo*); **the tuner: the map should not affect the idle**
(*owner*); on the MAF's scaling, the idle advance and the idle speed
nothing; **the files came the same day and were compared** — only full
load changed (H14). **The drive home on it** is read under H14 too.

**Water under the tailpipe during the clean** (*owner*, 9/11, photo
10:56): a wet patch of clear water, darker only with soot or rust from
the pipe, after about half an hour of the hydrogen clean at 2,000 rpm
with no load. Expected (*general*): combustion makes water, the
oxyhydrogen almost nothing else, and an exhaust run without load never
gets hot enough at the back to carry it off as vapour, so it condenses
in the silencer and drips. **Not a symptom** (*the owner's decision*);
it would bear on H20 only if water kept dripping after a long warm
drive.

**The brake pedal is soft and long** (*owner*, 9/10): hydraulics, not the
servo and not the engine — a matter for a garage.

**Oil on the underside, the sump's rear the wettest** (*owner*, 26/10,
looking from below during the oil change; `photos/sump-oil-2026-10-26-*.jpg`):
an oily film over the sump towards the back, along its flange and on the
bracket behind it; the gearbox casing drier. **It was there before the
change** (*owner*), though nobody had looked from below. **Settled 31/10
from right under the engine** (*owner*): **the engine leaks nowhere** —
the oil there is what is left of the earlier leak at the cover joint
(S10, closed) — and **the gearbox leaks**, the oil coming from it. *This
said "whether it is what ran down from the cover joint or a leak of its
own is not known" until then.* **It bears on `plan.md` 6i**: with no
engine leak, a falling dipstick level is oil burnt, not lost.

---

## How the symptoms relate — what is measured

| pair | link | evidence |
|---|---|---|
| S1 ↔ S3 | **the same events, but 014 is switched** | half of 014's rises sit on a dip; whether it counts follows load and the learned idle air, not the grade (S3) |
| S1 ↔ oil temperature | **strong** | roughest cold, calmest hot, every session |
| S1 ↔ load | **strong** | every load on calms it (S1) |
| S1 ↔ the drive before a warm stop | **medium, 11/11** | four captures of five after high revs (`46` the exception; `49` 12/11), nine after gentle drives: after high revs the stop starts rough on 3 and settles in 5–8 minutes, after a gentle drive it is level or slowly worse (S1, *The rough start of a warm stop*) |
| S2 ↔ S3 | **likely** | the owner heard the puffs come with the dips (12/10); never aligned |
| S14 ↔ S2 | **likely one mechanism** (*owner*) | a misfire's charge burning in the exhaust, loud when the fuel cut adds air |
| S14 ↔ S3 | **possible** | 014 is blind on the overrun, so it cannot be aligned |
| S4 ↔ S5 | **very likely one thing** | same window, same speeds; S5 needs no combustion |
| S4/S5 ↔ S1/S3 | **none measured** | no retard and no 026 signal at idle; 014's misfires sat on 3 and 4 until the VW leads and on 3 since (S3, *What 014 counts, by cylinder*; *this said "all four alike since" until 12/11*), and lead 4's end was the loosest (`refuted.md` C24) |
| S19 ↔ the bad start of 24/10 | **suspected one event** (*owner*) | same window, both what a cylinder flooded while standing gives (S19) |
| S12 ↔ S3 | **possible** (*reasoned*) | 014 counted seven single misfires on `47`, each in a window holding a moving-off (S12) |
| S3 on the road ↔ S17, S5 | **possible, one engine-speed band** (6/11) | 014's road episodes at 21–32 % load: 2000–2400 rpm about twice 1600–1800 and 2400–2600 (S17); the bus shows no stroke-to-stroke roughness peak there |
| S16 ↔ S1 | **untested** (*general*) | a gearbox's rattle in neutral is driven by the crank's unevenness at idle (S16) |
| S11 ↔ S1 | **untested** | if the hiss is a leak, H3 or H2; the owner reads it as the throttle's own air |

**Two clusters**: **the idle** (S1, S2, S3, S14) and **the cylinder 4
window** (S4, S5). S11 sits beside the idle, unplaced; S19 beside
it, the trims. *S23, the new rear probe's
signal, stood apart until it closed 12/11 (`refuted.md` D13).*

---

## The open hypotheses

Each lists what it explains, what speaks against it, and the test that
settles it. ✔ fits, ~ fits weakly, ✘ does not fit, — says nothing.

**The columns are the open symptoms that bear on the engine**: S1, S2, S3,
S4, S5, S11, **S12** (reopened 10/11 night, the jerk at a crawl), S14,
S19, S20 (added 26/10); S21 (added 6/11, its column dropped when it
closed 15/11, `refuted.md` D14); **S22** (added 9/11, closed
the same evening, `refuted.md` D11, **reopened 11/11 night** at the
owner's decision, its column back: ✔ for H1's lifter, ~ where a part
or one cylinder's burn could tick once per cycle — H0, H2's port, H7's
injector, H13); **S23** (added 10/11 evening, the rear probe's signal;
a column since H21 was added the same evening, — everywhere but there);
**S1s** (added 11/11, *agreed with the owner*): not a symptom but S1's
rough start of a warm stop after a hot drive, cylinder 3's and settled
in 5–8 minutes (S1, *The rough start of a warm stop*) — ✔ where a fault
worst hot on 3 fits it (H1's exhaust seat, H13's flake), ✘ where the
hypothesis expects the drive to calm it at once (H18).
Left out: S16 (the gearbox side, shown not to touch
the idle) and S17 (a resonance, not placed); S24 (G62's reading, a
sensor's own fault no hypothesis here explained) was never a column and
closed 12/11 (D12); S7 closed on 31/10 (D2)
and its column went with it; the closed ones are in
`refuted.md` §D.

### H0. The idle is normal for this engine — and there is no fault to find

**Re-read 12/11, the third research** (S1, *Every stroke named*; S3,
*What 014 counts, by cylinder*): **against.** The misfires are one
cylinder's — 80 % of 014's rises on 3 since 21/10, 1 and 2 next to
never — and 3 gives 10–20 % less than the mean at every warm idle; an
engine idling at its limit by design would spread them over four.
What is left for H0 is the small unevenness on all four (about 3.5 rpm
rms a stroke), which no repair has moved.
**12/11 evening, for, in that part** (S1, *The swell's shape, and what
the common part follows*): the common part is the same at every warm
idle since 24/9 — 2.7–3.1 rpm rms by capture, within 5 % — and moves
only with a load (a fifth less), the provider's gas (two fifths less)
and temperature (a fifth more cold): a constant answering to the
charge alone, as an engine's own scatter does. A fixed fault on all
four would read the same; no healthy AQY says which.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ✘ | — | ~ | — | ~ | ✘ | ✘ | ~ | ~ |

- **Against:** 014 reads 12–120 against VW's 0–5; the old converter burned
  through; the misfires and the steady deficit are 3's (S1, *Every
  stroke named*; S3), and P0303 has been stored four times (18/10, after
  `43`'s cut, 12/11 and 16/11 without one); the 2019 P0304 and the noisy knock
  window are 4's; the inside of 3 and 4 is worse. *This said "the dips
  sit on 3 and 4" until 12/11.*
- **For, 12/11: about an eighth of `IdleHealth` is the crank wheel's own
  alternation** (S1, *A steady pattern over the cylinders*) — no
  combustion, there on any engine with this wheel, nothing to find.
- **For:** no code is stored (2 % threshold: *under 2 %*, not *healthy*).
- **17/11, the fourth research** (*What the forums say*, searched again
  17/11): still no healthy M5.9.2 log of 014 or 032, and no statement
  that the family idles unevenly by design — nothing for or against.

**Test:** ~~a USBtin capture of a healthy AQY~~ — **not obtainable**
(*owner*, 21/10): the bus is reached only at the cluster harness behind the
vent, and no owner will have a splice made there. What remains needs only the
diagnostic port: **VCDS on 014 at a warm idle of a healthy AQY**, 3–5 min,
loads off — whether a sound engine of this family also counts above VW's
0–5. It compares only on the same ECU (Motronic M5.9.2), and says nothing
of the grade or of the one cylinder.

### H1. A lifter or valve on one cylinder (valvetrain)

**Re-read 12/11, the third research** (S1, *Every stroke named*):
**for, and the cylinder is 3 by every measure** — its steady deficit
(−9 % at its floor), its misfires (80 % of 014's rises), and a state
that **swells over minutes of unloaded idle to −26 % and falls back in
one step** at a jolt (a cut on 4, the A/C coming on, or nothing seen):
what a valve that does not quite seat until it turns or sheds a flake,
or a lifter, gives, and what a leak, a wire or a short injector has no
reason to. Against a valve that leaks all the time: the cold
compression (A4), and on the overrun 3's slot reads level with the
others' (nothing left with the wheel out, `--wheel`) — a closed
throttle hardly loads a seat, so weak. **The warm leak-down with 3 twice (item 9) is the test of the
cylinder now named.**
**12/11 evening** (S1, *The swell's shape*): the swell is a sawtooth —
1.5–3 % a minute up, 30–45 s down, with nothing on the bus at the
fall — and every stroke of 3's is weaker in it; a load masks it and
does not end it; the mixture does not move. **For a seat on 3 that
fouls at idle and burns itself clean**, the reading that fits most of
it; **against a flake blown out or a valve turning**, which this entry
named and which would mend in a stroke, not in 250. A lifter only if
it holds a valve off its seat. *Agreed with the owner the same
evening*: the phone's recording through a swell and its fall beside a
capture (`plan.md` 6p; the tailpipe 12/11, the cam cover 15/11, both
read in S1); the warm leak-down made on an engine switched off in a
swell (item 9).
**17/11, the fourth research** (S1, *The advance, the cold fast idle,
a warm engine-off and a coast-down*; *What the forums say*, searched
again 17/11): **for the dilution form** — 3 gains more than the others
from the governor's spark, as a burn phased later does (clear in a
swell, borderline on the floor); the swell survives a warm engine-off
of 25 s to 5 minutes; INA names a warm exhaust seat that "sucks in
exhaust gas", and Mercedes (LI01.30-P-072328) one leaking seat with
no code stored, the leakage test its gate. **Against the lifter
form**: a pumped-up element comes on suddenly and sinks over minutes
(INA), the swell's mirror. *Reasoned*, pulling the other way: the cold
fast idle keeps 3 level, and its end drops 3 by ten points within a
minute at the same coolant and load — more than the vacuum's change
alone gives, so part of 3's floor answers to the mixture or the
speed. *It also read "a seat that dilutes 3 should move the mean
mixture at a swell" until the same evening — wrong*: burnt gas drawn
back is neither air nor fuel the MAF misses, so 3 runs rich by its
shortfall, the others lean by a third of it, and the mean stays put;
only the probe's weighting of 3 could show it, a point or two at most.
What an unmoved mean rules out is a swell of unmetered air or of fuel
short on 3 (*reasoned*).

A hydraulic lifter that bleeds down, or a valve that seats late or not quite,
on one or two cylinders. *General.* **Widened 4/11/2026** (*agreed with the
owner*, after the research of 4/11):
**the exhaust seat on 3 the likeliest form** — a small leak there draws
exhaust back into the cylinder through the intake stroke at idle vacuum,
which load (a higher manifold pressure) eases and a higher idle speed does
not (`refuted.md` D9), and cold cranking compression misses (A4); it is
also where H13's flake would sit (SAE 2000-01-2858, 2003-01-3187: deposit
flakes trapped under exhaust seats leak and run a cylinder rough, water
the strongest trigger of flaking). **A stem sticking in its guide** (varnish
or carbon on the stem, which neither the EPR flushes nor H13's clean
reach) fits S18's cold hang-up and a mild steady excess after it; **a
lifter stuck pumped up** holds its valve a hair open with no tick. A
lifter that bleeds down would tick, and the hot recording of 26/10 found
none at idle; **9/11, a tick once per cycle during the hydrogen clean**
(S22) was closed the same evening as the clean's own sound
(`refuted.md` D11). **8/11, the coldest start on record** (about 14 hours outdoors at
−2.5 °C; `idle-log.md`): **the valvetrain clattered for the first second
or two, then stopped** (*owner*; not a new symptom, *the owner's
decision*) — what hydraulic lifters that leaked down overnight do
until the oil pressure refills them (*general*), so it says nothing for
a lifter stuck at a warm idle; one that kept ticking warm would. *General* for these (GM bulletin 19-NA-219, another engine family:
valve leakage misfires most at idle, compression normal, a leak-down
finds it). **The inlet seats of 3 and 4** (*the owner's reading* of the
port photos, 7/11, re-read with him): looking down the ports of 19–20/10
(album 00:00–00:33; `photos/borescope-2026-10-20-cyl*-inlet-port-*.jpg`),
**1 and 2 have a thin, even brown band where the throat meets the seat
ring; 4 a band of white beaded crust along it** (00:03:06–00:03:49),
**3 a thick, broken crust all round it, with a lump standing out of
the edge** (00:12:31, the owner's marked frame of 7/11, and
00:12:44–00:15:44). The camera sees the ring's upper edge with the
valve a little open; the contact face under the head cannot be seen, so
whether the crust reaches it is not known (*reasoned*). **What an inlet
seat that does not quite seal would do** (*general*, *reasoned*): at
idle, with the manifold at its deepest vacuum, compression and burning
gas leak back into the port, so the cylinder loses charge and takes in
hot residual with the next one — worst at the smallest charge, eased by
load (a higher manifold pressure), not helped by a higher idle speed,
and missed by a cold cranking compression test, as the exhaust seat's
form above. **It answers this hypothesis's main against** (*A steady
pattern over the cylinders*): two crusted inlet seats weaken 3 and 4
together, where one exhaust seat on 3 would weaken 3 alone; and more
crust on 3 fits the dips leaning to 3. **Against**: the crust is seen,
its seal is not; and 3 and 4's ports and chambers are worse alike
(H13), so it may be where the deposit sits rather than what fails. **The
leak-down names it**: a hiss at the throttle with the plenum off. **The
chamber photos beside them** (7/11, *at the owner's request*; album
00:43–02:44): a valve stands open in only a few frames — cylinder 2's
(02:24:33–02:25:20), whose conical seat face reads smooth and even with
white beads of deposit on the head's rim beside it; 4's (00:48:24), out
of focus, crust at the edge; 1's (02:41:31) unclear; **3 none**, every
frame of 3 a closed valve or the crown. Which valve of each is open is
not known from the frame. **So the chamber side neither confirms nor
clears the inlet seats of 3 and 4**; what stands is the ports' contrast,
1 and 2 even against 3 and 4 broken, read from above. **The open valves at full
resolution** (7/11, *the owner's reading*: the inlet head reads light,
the exhaust dark; he sees 4's seat face uneven, 2's and 1's smoother):
the sharp frames, 2's (02:25:20) and 1's (02:41:31), show a smooth
face; **4's only open frame (00:48:24) is out of focus**, and its round
beads are what blur makes of any edge — 2's own blurred frames
(02:24:33, 02:25:09) show the same beads along its rim. So the
difference cannot yet be told from blur (*reasoned*); a sharp frame of
4's face would decide it.
**Test: a warm leak-down on all four**, listening at the
tailpipe (exhaust seat), the throttle (inlet) and the oil filler (rings);
**a stethoscope on the cam cover above 3, hot**, against 1, 2, 4. The AQY's lifters are hydraulic bucket
tappets (*hydrostely*), fed from the head's gallery through a small hole
each; inside, a plunger and a check ball hold an oil column that takes up
the lash. They fail two ways (*general*): **one that does not fill** (a
narrowed feed, air, wear) leaves lash, ticks, and opens its valve late and
short, worst hot at idle; **one whose plunger or ball sticks** with varnish
or debris holds its valve a hair open, which costs compression and misses
at a small charge and is covered by load — the case this hypothesis is
about. The valve is closed by its spring; the lifter only removes the gap.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ✔ | ~ | ~ | — | ~ | ~ | — | — | ✔ |

- **9/11, after the clean** (S1, *The clean of 9/11*; S22): 3's swell
  gone at stop 7 and its floor kept (−8 to −9 %), the swell back a day
  later (`47`) — the clean cannot reseat a worn seat (*general*), so a
  seat that leaks as a part fits the floor and one that a deposit holds
  open the swell; S22's tick closed as the clean's own sound
  (`refuted.md` D11), reopened 11/11; and with the gas flowing **no dip
  at all**, which a stroke that loses its charge through a seat would
  not obviously give (*reasoned*, against in part). *This bullet read
  "3's excess gone", and "4's deficit kept, which an inlet seat on 4
  fits", until 12/11.*
- **3 is the weak one at every warm idle on record** (S1, *Every stroke
  named*; `43`, 3/11 evening, −13 % with 62 % of the weak strokes) — one
  cylinder, the one with the deposit and 18/10's tick (S18; `refuted.md`
  D10): **for**. A compression or leak-down reading on 3 against the
  others would show a seat that does not close (*general*).
- **4/11, the two patterns on their own** (S1, *Load smooths it* and
  *driving does*; *reasoned*, agreed with the owner): with H13's flake on
  3's exhaust seat, **the one reading that fits both** — a load raises
  the manifold pressure and so cuts the exhaust drawn back past the seat;
  a working drive burns, dries or blows the flake off it for a while, and
  queuing lets it soak and soften again. **For.**
- **The owner's reading of the photos, 4/11** (`borescope-2026-10-20-cyl3-exhaust-valve*.jpg`):
  **coarse deposit right up to the edge of 3's exhaust seat**, in the
  dark band beside the valve's margin. Not conclusive by his own account:
  the contact line itself is hidden while the valve is closed, so the
  photos show deposit beside the seat, not under it. **For**, with H13.
  **How the seat is reached** (*general*, searched 4/11): only with the
  head off — the valve cannot come out with the head on, the cover gives
  only the cam and the lifters, the exhaust port only the back of the
  valve, and a soak through the plug hole (a Kia/Hyundai procedure, TSB
  23-EM-007H, the nearest maker's one found; none from VW for this engine)
  lies on the crown, not the roof. So the warm leak-down comes first
  (`plan.md` 9): the head off for the seat only if it hisses at the
  tailpipe on 3.
- **For:** a valve that seals worse at low cylinder pressure misfires at a
  small charge and is covered by load; the tick once per cycle of 18/10 (`refuted.md` D10); one forum
  AQY case of a sticking bucket tappet (pkw-forum.de, 2003) and one of valves
  not sealing (forum.vwgolf.pl t=522030).
  **The oil before 6/2026** (*owner*, 23/10; `vehicle-history.md`): about
  three years in the engine, nearly one of them standing outdoors,
  condensed water under the filler cap at the change — the conditions in
  which oil forms varnish and acids (*general*), and varnish is what
  sticks a plunger or a check ball. **The old oil came out really black,
  and no flush was run** (*owner*, 24/10). Weak: it says the means was
  there, not that a lifter took it up — black is what a detergent oil
  holding soot looks like after three years (*general*), and the top end
  seen with the cover off on 1/10 carried only a thin golden-brown film,
  no sludge on the cam or the caps (`refuted.md`, the head gasket entry).
- **For, 11/11: the rough start of a warm stop after a hot drive is
  3's** and settles in 5–8 minutes (S1, *The rough start of a warm
  stop*) — what a seat that leaks hot, or holds a flake the drive
  loosened, gives; and the weak strokes come in spells of seconds on one
  cylinder (S1, *How the weak strokes follow each other*). *Reasoned*,
  three captures after high revs, `46` the exception.
- **Neither, 11/11: the cold clatter of 8/11** (the first second or two
  at −2.5 °C): VW's own procedure for the 2-valve 2.0 calls irregular
  valve noise on starting normal (*What the forums say*, 11/11).
- **For, 12/11: the steady pattern is 3's alone** (S1, *Every stroke
  named*): with the crank wheel's alternation out, 3 gives 10–20 % less
  and 4 is level — what one seat on 3 gives. What moves over minutes is
  3's swell; its floor holds still, as a fixed leak would (*reasoned*).
  *This was "against, 5/11: the steady pattern names 3 and 4 alike" until
  12/11*, on a count that slipped with the wheel left in.
- **Off idle, 12/11 night** (*Naming the cylinder*, *Off idle*): 3's
  deficit against 2 is a fifth of a stroke at idle and 1–3 % at full
  load. **For**: a seat's leak is set by time, and fades with speed.
  **Against**: at idle speed it falls from −24 to −9 % when the engine
  pulls (b7 27 → 57) — more charge at the same time per stroke, which
  a leak would follow (*reasoned*). **What is left of the seat is its
  dilution form** (*agreed with the owner*, 12/11 night): an exhaust
  seat that lets burnt gas back into 3 at the idle's vacuum, or a flake
  that holds it off; a seat that loses compression is not what the
  load shows, nor what 12 bar on all four showed.
- **Against:** compression **13 bar in 2018 and 12 bar even on all four in
  2026** (`vehicle-history.md`) — no cylinder losing; the vacuum gauge
  steady cold and warm, no flick (H3); no ticking before 18/10, and **none on any
  drive since, through 24/10** (`refuted.md` D10) — a lifter that hung
  should not fade, and this did; the idle is never worst hot, where a thin-oil lifter
  should be; **the phone recording of 24/10, part-warm** (oil 52–58 °C):
  one click per firing, all four alike, over every injector and over the
  cover at each cylinder — no once-per-cycle sound over any lifter
  (`idle-log.md`, 24/10), and **the same hot, 26/10** (oil 100 °C): no
  once-per-cycle sound above the noise floor at any of the eight places
  (`idle-log.md`, 26/10); the valves looked whole on 19–20/10 (which says nothing of
  sealing); 18/10 is explained by 3's flaked deposit without it.

**Tests:** a phone recording over each injector and each lifter, **done part-warm 24/10 and hot 26/10, nothing** (the screwdriver by ear dropped 24/10); **the two EPR flushes**, done 26/10 (`idle-log.md`), which clean the
feed passages and the plungers' varnish — alongside BG 44K, so an
improvement would not tell H1 from H13; no tick since; a warm leak-down
(declined 20/10, *owner's decision*; back in `plan.md` 9 since 4/11, 3
twice since 11/11); VW's tappet check with the cover off (`plan.md` 9). 18/10 coming back, cold, would reopen it (`refuted.md` D10).

### H2. A leak ahead of the converter — ahead of the front probe (manifold, its joint to the head, the probe boss), or between the probes

At idle the exhaust pulses dip below atmospheric and a crack draws air in.
*General.* **Two zones, which act differently** (the second added 10/11,
*the owner* agreeing; *reasoned*):
- **ahead of the front probe**: the **original manifold, its gasket to
  the head and the probe's boss** — the probe sits on the manifold
  (`vehicle-history.md`). The front probe sees the air, the ECU enriches,
  and the converter gets a mean of about λ = 1;
- **between the front probe and the converter**: the manifold-to-front-pipe
  joint (remade by the garage on 10/9), the new flex pipe, the universal
  front pipe, and **its spare lambda boss, closed by an old probe with its
  leads cut off** (`vehicle-history.md`). The front probe sees the true
  mixture, so the fuelling, 032 and the cylinders are untouched; the
  converter gets the air besides, and **the rear probe reads lean, most
  at idle's small flow**, and sinks over minutes as any lean excess does
  once the converter's store is full (H11, *The sinking is the
  converter's shape*) — the 036 reading of 9/11 night in full (H11,
  *What the rear probe can and cannot say*). Nothing else in the table:
  air there reaches neither a cylinder nor the front probe, so the fit
  below is the first zone's.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ✔ | ~ | ✘ | ✘ | ✔ | — | ✔ | ✘ | ~ | ~ |

- **For:** the puff (S2), the hiss (S11), air for S14's bangs; a 26-year-old
  manifold that has lived through years of misfires; **for the second zone,
  the rear probe sinking towards lean at every idle** (9/11 night, H11),
  and a boss closed by a probe that was never meant as a plug.
- **The plugged boss, 10/11 night** (*owner*, the album 22:45–22:47):
  the cut-off old probe in it **would not turn further — tight**; the
  boss's weld on the pipe rusty and lumpy, a darker patch at one edge
  that a photograph cannot tell from soot (*reasoned*).
- **Against:** air outside the cylinder does not stop one firing, and cannot
  pick a cylinder; no ticking, no exhaust smell (*owner*); just before a dip
  the probe read a little *rich*, not lean; the cold tailpipe test found
  nothing (12/10, the whole exhaust ahead of the tailpipe, both zones) and
  the cold exhaust smoke test nothing (9/10, the exhaust
  would hardly take pressure); **the manifold seen from close below on
  31/10: old and rusty, no black soot marks and no holes** (*owner*) —
  what a leak leaves; **its joint to the head, seen from
  below, nothing visibly wrong** (*owner*); the part under its heat
  shield and the joint from above not seen. The second zone cannot give
  032's idle cell or the dips.

**Against, read 15/11 (*the owner's* reading, agreed)**: **032's idle
cell at −6 to −9 %** — the ECU takes fuel away at idle, where air drawn
in ahead of the front probe would read lean and make it add fuel; **the
front loop holds through 3's swells** (`50`'s 001, `49`'s 033; S1, *8h's
plain idle and its loads*), so the swell is not made in the exhaust;
**the rear probe's sinking was the old probe's**: the new one flat for
18 minutes (10/11), the rear probe switching about 0.45 V through a
whole stop on `53`. What none of it reaches: a crack that opens only
hot, and the manifold under its heat shield.

**Test:** none planned. **The warm tailpipe test was dropped 15/11**
(*the owner*): the cold one and the smoke test found nothing, and the
readings above speak against a leak in either zone. A leak in the
first zone would mean a new manifold; in the second, that joint or the
boss resealed.

**After the probes, 10/11** (H11, *The reading after the swap*;
*reasoned*): the new rear probe held flat for 18 minutes of idle and
then switched to the front's swing, rich peaks included. Air drawn in
between the probes would feed a steady excess from the start and show
the lean side only, so **the reading after fits the second zone less
well than 9/11's did**; it does not rule it out. The new probes were
tightened by hand without a torque wrench (`vehicle-history.md`), and a
probe seated loose is a leak in this zone of its own making, hence
their check (`plan.md` 8e).

### H4. Weak spark from what feeds the parts (earth, wiring, coil feed)

**Re-read 12/11, the third research** (S1, *Every stroke named*): what
is left of it is read **for 3**: the injector loom where it reaches 3
(6m, flexed while measured). 3 alone carries the deficit and the
misfires since the VW leads; 4's share went with the leads. A wire has
no reason to cost a steady 9 % in every state, so weak.
**12/11 evening** (S1, *The swell's shape*): against, for the swell —
the mixture and the injection time do not move with it, and a load
masks it at once, where a load makes a weak spark worse.

**Much weakened, kept last of the electrical side.** Measured clean: the
coil's ground and supply for a gross fault, the engine's earth under load,
the charging; the battery is new (8/2026). **The idle is better with the loads
on, when the coil's supply sits 1.25 V lower** — a spark limited by supply
would go the other way. The weak cylinder is 3, through three sets of
leads and plugs, and its coil output also fires 2, the strongest, so
neither the coil nor its feed can pick it (*this said "the dips sat on
3 and 4 … on different coil outputs" until 12/11*). **What is left**:
the injector loom where it reaches 3 (and 4), taped and oily — its wires at 4 whole outwardly (*owner*,
19/10; tape renewed). The plug-end side moved to H15, refuted 4/11 (`refuted.md` C24).

**The supply as the ECU sees it, against the battery** (15/11 evening,
*the owner's* observation and measurement; *not a symptom* — no
decision on that asked for yet). The MFD read 14.2 V after the start
and 13.5–14.0 V with the loads, never near the 12.6–13.4 V that 004
read at `53`'s stop. **A multimeter on the battery's terminals beside
the MFD**, warm, the engine running, about 20 minutes after the drive:
**13.57 V with the MFD at 14.0; 13.50 V with main beam, the MFD at
13.7** — so **the MFD reads 0.2–0.4 V high**, and the battery itself
dropped only 0.07 V for main beam. At `53`'s stop main beam dropped
004 by 0.54–0.63 V. *Reasoned*, the two not measured at the same
moment: most of that step is lost between the battery and the ECU, in
a path main beam's current shares — which fits the loss the owner
measured in September, **about half of the headlights' drop before the
fuse box (~0.09 Ω)**, with the chafed main positive cable at the
battery (`vehicle-history.md`, *Electrical work, 2026*): about 9 A of
main beam through 0.09 Ω is 0.8 V. Whether the ECU's supply (the main
relay) is fed through that same part is *not known* (the wiring
diagram is not in these files). **The MFD, calibrated against the
battery the same evening** (`mfd15`, DisplayVolt's column 17 = 27.3; 12.4
against 12.36 V, 13.7 against 13.7), **then read 11.7 V with main beam,
the engine stopped, against 12.12 V at the battery** — 0.4 V lost
between the battery and the dashboard's feed for main beam's current
alone (*measured*), the same shape as 004's step. **It does not pick a cylinder**: the
same supply feeds all four, and the idle is calmer with the loads on.
**Measurable cheaply**: with main beam on, the drop from the battery's
plus to the ECU's supply pin and from the battery's minus to the ECU's
earth, then to the fuse box's input — tenths of a volt on either side
names the side.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | ~ | ~ | — | ✔ | ~ | ✘ | — | — |

- **9/11** (S1, *The clean of 9/11*): 3's floor kept after the clean,
  its swell gone for a day: for 3's own circuit in the floor (its supply side and coil since measured sound, 6m of 17/11; the control wire is 6n's); with
  the gas flowing no dip at all — hydrogen lights on less energy
  (*general*): for in kind. *This read "4's steady deficit kept, 3's
  gone: for 4's own circuit" until 12/11.*
- **One cylinder, 3** (S1, *Every stroke named*): weakly for at 3.
- **4/11** (S1, *Load smooths it*): 45–50 with the A/C and the rear
  window on at about 12.4 V against 90–110 without — a higher cylinder
  pressure needs more voltage at the gap and the supply is lower, so
  anything on the spark side, plug 3's gap included, predicts the
  opposite (*general*). **Against.**
- **12/11 night, off idle** (*Naming the cylinder*, *Off idle*): **at
  full load 3 is within 1–3 % of 2, and no stroke of 100,000 there
  misfires** — where the spark is hardest to make. **Against** the
  spark side on 3; the injector-branch form (short only at the
  smallest quantities) is not touched by it.
- **5/11, the steady pattern over the cylinders**, re-read 12/11 (S1,
  *Every stroke named*): **3 alone gives 10–20 % less** warm, 4 level;
  a raised resistance in 3's branch would give a steady deficit, but no
  reason for it to swell and mend in a step (*reasoned*). Against the
  spark side as above. *It read "3 and 4 give 3–4 % less alike — the
  pair the loom feeds; for the loom" until 12/11.*
- **Why load would help** (5/11, *reasoned*, *general* for the physics): a
  raised resistance slows the current's rise in the injector's coil, so it
  opens later by a fixed delay; at idle the pulse is shortest and that
  delay costs the largest share of the fuel, under load a smaller one.
  **H4 predicts "worse only at idle, load helps"** on its own. And the
  trims before a dip (S1, *The dips ride a swing of the idle loop*) fit a
  cylinder that is lean already and fails when the mixture is trimmed —
  as much for H3.
- **Against, 5/11** (*reasoned*): **032's idle cell is negative** (−6 to
  −8 %): a cylinder lean by its deficit would make the mixture lean, the
  probe would see it and the trim would add fuel, not take it away — the
  same against H3. Medium: the trim carries other inputs (the purge, the
  MAF). **The calm after revving** needs heat to reach the joint, a weak
  link. **3 is the borescope's worst** (3 > 4 > 2 > 1), so H13 explains
  it without a wire. *"3 and 4 do not behave alike … where a shared
  loom would expect them close" is moot since 12/11: 4 is level warm.*
- **5/11 evening, the first look** (*owner*, plenum on): only 1's and 4's
  connectors reachable. **From one pin of 4's connector to a pin of the
  loom's own 3-pin connector** (at the end of the loom, by cylinder 1):
  **about 2 Ω, at times 1.9, at times 3.4** — against the manual's 1.5 Ω
  for a whole wire; the meter's probes touched together read 0 (*owner*),
  so the figure is the path's or the probe's seating, which wandered —
  **injector 1's contact 1 to the same pin** tells which: alike, the shared
  part (T3 or D95); 4 alone higher, 4's own branch. **Flexing the loom at
  injector 4 while reading did not move the figure** (*owner*, engine off
  and cooling): no intermittent joint there that a hand can find — against
  a loose contact in 4's branch, at least cold and still. **Then, the
  probes re-zeroed: injector 1's and injector 4's contact 1 to the same
  T3 pin both 0.001–0.002 Ω** (*owner*); the 1.8–3.4 Ω before was the
  probes, not the wire. **The supply to 1 and 4 is sound and alike**; 2
  and 3 and the control wires not measured (the intake on). **That 3-pin connector's latch
  is worn**: it holds, but comes off by pulling without pressing the
  tongue (*owner*). **The beeper joins one of its pins to contact 1 of
  injector 4** (*owner*) — the supply side, so the 3-pin connector carries
  the injectors' supply at least.
- **The wiring, from VW's diagram for this engine** (Golf/Bora 2.0 AQY,
  sheet 55/6; the text of the diagram read only in a garbled preview,
  eserviceinfo.com and portal-diagnostov.com, 5/11): **one supply for all
  four** — fuse S232 (No. 32, 10 A), 1.5 mm² red/violet, connection A101
  (relay terminal 87), connector T10a/5 (10-pin, cable channel left in the
  engine bay), 1.0 mm² red/violet to the splice **D95** in the harness and
  on to **contact 1 of each injector**, all red/violet. **Contact 2 to the
  ECU**, 1.0 mm²: cylinder 1 pin 73 violet, 2 pin 80 violet/green, 3 pin 58
  violet/red, 4 pin 65 violet/blue — the manual's pins (above). The sheet
  also lists **T3, a 3-pin connector near the intake manifold**, beside the
  engine speed sender G28 and the sender earth 220; which of its pins
  carries what the garbled text does not show, and the owner's beeper puts
  the supply on one. **So the supply is not split by pairs** (*reasoned*):
  a poor joint in it, the worn T3 included, would starve all four alike,
  not 3 — **against H4 through the supply**; what is left for 3 is its
  own branch after D95 and its control wire (pin 58).
- **What the loom can and cannot do unseen** (5/11, *reasoned*, at the
  owner's question). An **open** circuit — the plug off on 3/11 — is
  stored at once: P1240, injector 4, open circuit, sporadic. **No
  P1237–P1240 has ever been stored without a cut**, so a contact that
  drops out completely, even briefly, is unlikely. **A raised
  resistance is not stored**: as long as enough current flows for the
  output stage not to see an open, the ECU finds the circuit good while
  the injector opens late and short and the cylinder runs lean. That is
  what is left of H4, and only a measurement shows it.
- **6m measured, 17/11** (*owner*, `plan.md` 8z's night, the rail and
  the loom off, cold, the meter's leads 0.1 Ω to be taken off):
  **each injector across its pins 16.1, 16.1, 16.0, 16.0 Ω** in the
  order 1-2-3-4 — inside VW's 14–18 Ω and alike to the meter's last
  digit; **contact 1 to contact 1, all six pairs, 0.2 Ω** — 0.1 Ω of
  wire, against VW's 1.5 Ω at most. **The shared supply side of the
  loom and the four coils are sound and 3 is no different**, cold and
  at rest. **The loom flexed with the meter on: no change.** *Also
  read by him*: from "the common connector" to contact 1 of each
  injector connector, the same on all four — **3.05 kΩ to one of its
  pins, 0.8 kΩ to the other**; to contact 2, open everywhere. **The
  connector is T3**, the loom's 3-pin one by the regulator (*owner*;
  the 5/11 entry above, where one of its pins read 0.001–0.002 Ω to
  contact 1), **and on 17/11 that third pin 0.2 Ω, as the pairs**
  (*owner*). *Reasoned*: kilohms are not a
  wire but a path through other parts on J17's supply, the same for
  all four because their contacts 1 are one node (0.1 Ω apart), and
  contact 2 runs only to the ECU, so open is what it should read.
  **It says nothing of 3.** Not measured by this: contact 2 of each
  connector to the ECU (6n).
- **17/11, the fourth research** (S1, *The advance, the cold fast idle,
  a warm engine-off and a coast-down*; *What the forums say*, searched
  again 17/11): the advance does not exclude it — a lean cylinder burns
  slowly too; weakly against (*reasoned*): the cold idle after the
  fast idle, enriched and on longer pulses, is worse at matched load
  than the warm, where a fixed opening delay would cost a smaller
  share. **For the floor, 17/11 evening** (S1, *The floor and the
  common part read apart*): at idle speed 3's loss is a fixed amount
  that load does not shrink — what fuel short by a fixed amount gives,
  and a leak does not; the swell is H1's, the floor may be this. **The direct test is the injector's voltage and current, 3
  against 2, warm and running**: a raised resistance or a weak output
  stage shows as a late opening and a higher on-voltage, and an output
  stage of the TLE6220 kind diagnoses no raised resistance — closer to
  the fault than 6n's ohms at rest.
**Tests:** **the circuits measured** (among themselves on 17/11, above; `plan.md` 6n to the ECU; VW's repair manual, Golf Mk4, *Motronic injection and ignition system (2.0 ltr. engine)*, *Checking injectors* (workshop-manuals.com, read 5/11/2026)):
the injector itself 14–18 Ω at about 20 °C; each wire, connector to
connector, at most 1.5 Ω; contact 1 of the 2-pin connector is the
supply from the fuel pump relay J17, shared by all four, contact 2 the
ECU's output, at the 80-pin connector **pin 73 for cylinder 1, 80 for 2,
58 for 3, 65 for 4** (test box V.A.G 1598/22, whose sockets carry the
connector's numbers; the manual's, not yet checked on this car). Three of
four alike and one tenths of an ohm higher is the reading.
The injector loom flexed at 3 and 4 at a warm idle — **done by
the owner on 24/10, part-warm, during the first phone recording, above all
the repaired wire at injector 4, judged by ear only: no change heard**
(reported 28/10). Weaker than the planned
read (dips per minute in a capture), which was dropped with it. What
is left: VCDS 004 (the ECM's supply) beside 014.
VW's TSB 01-08-27 (the coil's ground wire, US sister engines) is the joint to
look at first if the spark side ever comes back.

### H5. Something in cylinder 4's knock window that is not combustion (S4, S5)

The ECU books anything at cylinder 4's crank angle to cylinder 4: G66, its
torque or connector; a loose ancillary part buzzing in a speed band; **an arc
at lead 4's plug end** (`refuted.md` C24). Injector 4's click is settled against (B7).

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | ✔ | ✔ | — | — | — | — | — | — |

**Tests** — `plan.md` 8w since 15/11 (*the owner*; not scheduled from
9/10): G66's torque and connector; a look for a loose bracket at ~3000
rpm in neutral; after the VW leads, the neutral 026 holds and a 020
drive against `vcds/vcds-step2c-020-026-003.csv`.

### H6. Knock control relearning after the battery disconnects

Explains how S4 changed between logs, not S5. **Test:** 020 + 026 after a few
hundred km without a disconnect.

### H7. Fuel delivery at idle: rail pressure, one injector

**17/11: the one-injector form refuted** (`refuted.md` C29; S1, *The
first stop on the new gasket*): injectors 2 and 3 swapped, and on the
first stop after it 3 was −12 % and 2 +6 % as before. **What is left
of H7 is the rail's pressure** (list A, A4; S19), read only by a gauge
(`plan.md` 8u). The text below is kept as it stood for that form; its
injector parts are history.

**Re-read 12/11, the third research** (S1, *Every stroke named*):
the one-injector form would be injector 3's — 3 gives 10–20 % less at
every warm idle, in every state, which a short injector does. **But 3
was the weak one before the injectors were changed too** (`09`, `12`,
`17` of August, −11 to −23 %, seconds each), **so the injector itself
is unlikely: the same place would have to be bad in the old set and in
the new** (*the owner's argument*, 12/11; **15/11**: by the crank wheel
the weak cylinder of `17` was 2 or 3, and read as 2 the whole pattern
would have turned half a cycle with the injectors — *Naming the
cylinder*, *The names before the injectors*). An exchange of injectors 3
and 2 was agreed earlier that day as its test and **withdrawn
on this** (`plan.md` 6o, removed). What stays with the cylinder through
a change of injectors is its wiring and the ECU's driver (H4, 6m, 6n).
**12/11 evening** (S1, *The swell's shape, and what the common part
follows*): **against both forms.** One injector: the swell moves
neither the loop's regulation nor the injection time, so it is not
3's fuel. The rail's pressure: the common part is the same after high
revs as after none and the same on every day, within 5 %.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | — | — | — | ~ | ~ | ✔ | ~ | ~ |

- **3 the one cylinder throughout, P0303 four times** (S1, *Every
  stroke named*; S3) — one injector in reach by the cylinder; 25/10
  night's "the dips then sat on all four alike" (`40`, `41`) was a count
  that slipped: 3 led there too. **Against, by the owner** (3/11): the
  injectors are new (9/2026); **no swap** (*his decision*, agreed 12/11
  and withdrawn the same day, above), so this stayed untested — **until
  16/11: injectors 2 and 3 to be swapped in 8z** (*the owner's offer*;
  `plan.md` 8z, its reading). **Done 17/11** (*owner*): the injector from 3 is in 2,
  the one from 2 in 3, each on its own old ring; 1 and 4 where they
  were. *The
  owner's history of 3/11 — "on the new VW leads the dips were on all
  four alike and 3 came back only later; a bad injector would never
  have been even" — rested on those shares; by `cylscan.py` 3 was never
  even, and the argument that stands is 12/11's: 3 weak on the old set
  too.*
- **Against:** four new injectors and a new filter changed nothing in S1; the
  trims near zero; full-load pulls reach ~85 kW, where a weak pump shows first;
  the regulator (6/2026, 3 bar) dry at its hose, **no fuel and no smell at
  the hose's end when it came off on 25/10** (*owner*) — against a leaking
  diaphragm, not against one that does not answer its reference; injector tips clean on the
  borescope (19–20/10).
- **A plug washed clean by fuel** (a forum extract on the AEG/AQY, 20/10:
  *"#3 was much cleaner … replaced #3 injector as it was washing that plug"*):
  plug 3 is the cleanest here too. Weak, for the reasons above; a reason not
  to read plug soot as combustion quality.
- **12/11 night, off idle** (*Naming the cylinder*, *Off idle*): 3's
  deficit is not a share of its fuel — a fifth of a stroke at idle,
  1–3 % at full load. **Against** an injector on 3 that flows short in
  proportion; **not against** one short only at the idle's smallest
  quantities (or its wiring, H4).
- **For, since 24/10: S19.** A dripping injector or a regulator that does
  not hold gives a rich code and a start that floods after standing; the
  only hypothesis that predicts both. Every lean-side one (H2, H3, H4,
  H15: unburnt air reaches the probe) predicts P0171 or nothing, not
  P0172. **Since 24/10 not the only one**: a purge valve that does not
  seal predicts both as well (H16), and its test is cheaper.

- **The regulator's vacuum reference** (*the owner's question*, 25/10).
  The regulator holds the rail a fixed 3 bar above the intake through a
  hose to a narrow tube on the intake; the old hose was well perished when
  he replaced it in 6/2026, so crumbs of it could sit in that tube. **A
  blocked or open reference leaves the rail at the no-vacuum pressure at
  idle**, VW's 3.0 bar instead of 2.5 (`vcds.md`): about half a bar more
  across the injectors, roughly 8 % more fuel at idle and less and less as
  the throttle opens and the vacuum falls (*reasoned*: flow goes with the
  square root of the pressure across the injector). **That is the shape of
  this car's 032**, low at idle and normal at part load, and VW's "fuel
  pressure too high". Only a full blockage or a leak does it; a partly
  blocked tube only slows the response. **Tested 25/10 night** (6e,
  `idle-log.md`), cold, the hose off at the intake end twice: **the
  regulation went to −8.6 and −10.2 % within seconds** and came back
  when it went on, **no fuel at the hose** — the regulator answers its
  reference and its diaphragm holds (`refuted.md` C20). **Not tested**:
  its base pressure, the pump's non-return valve and the injectors, which
  only a gauge reads.
- **Found 25/10** (*owner*; `photos/fpr-vacuum-hose-2026-10-25-end.jpg`,
  `-side.jpg`): that hose's **intake end is breaking up** — on the photo
  the wall has come apart into layers with voids between them and a crack
  runs from the bore outwards *(this said "split" until the photo)*, after
  the many times it came off with the intake work, **no clip on it since
  6/2026**, and **at least once left on when the intake came off, so it
  was stretched and pinched** — the likely start of the crack, **from
  about September** (*owner*, 25/10; *this said "left off at least once"
  until he corrected it*). It blows through freely. The timing fits 032:
  low at idle at every reading since 24/9, the first after the MAF. **A split at the joint
  pushes rich, not lean** (*reasoned*): the narrow tube on the intake
  limits what the split can let into the engine, while the hose behind it
  fills from outside, so the regulator sees less vacuum than the intake
  has and holds the rail higher. How much depends on the split against the
  tube, unmeasured. **The first part found on the car that fits the shape
  of 032 and VW's "fuel pressure too high"**; its weight is not known.
  **Its own figure, 25/10**: 032 relearnt from zero since 24/10's
  clearing, about 10 km of driving on it, **−8.6 / +3.9 %** — **the most
  negative idle value on record** (before: −6.3), the part load positive
  as always (`photos/vcds-032-055-2026-10-25-before-new-fpr-hose.jpg`;
  055 −1.25 g/s; fault memory empty). **Read after a few seconds of idle
  with the old hose pulled off**, so it may carry them (*the owner*,
  25/10; *reasoned*: a fraction of a point at 6i's relearning rate, and
  the open hose pushes both ways — `idle-log.md`). **Replaced the same evening** with
  clips at both ends; 032 after some drives says the rest.
  **The first idle on the new hose, the same afternoon**: the live
  regulation **+6.5 % loads off for the first minute and a half**, and
  032's idle cell already **−4.7** from −8.6 — **the hose was carrying
  fuel**, so the rich idle trim is at least partly answered. **Partly**:
  two minutes in, the regulation fell to −10 % and settled near zero, the
  engine wanting about −5 % in all (idle cell plus regulation, an
  approximation) against about −2 % before — **about 3 points of fuel
  arriving on their own at a warm idle**, which fits the purge starting
  (H16; *reasoned*) — left unmeasured by the owner's decision (25/10), and
  6e's cold start showed no such step (`idle-log.md`). `IdleHealth` loads off **about 90
  at 80 °C of oil**, where it has sat before: the roughness is not shown to
  have gone with it (`idle-log.md`).
  **A drive later, the same evening (6j): 032 −7.8 / +6.3 %** — the idle
  cell back to about where it stood on the cracked hose, the part load
  higher than ever. So the rich idle trim is **not** answered by the hose;
  what it answered on 6i's first minute and a half did not last a drive
  (`idle-log.md`).
  **Its size, then** (25/10, *reasoned*): from −8.6 on the cracked hose
  to −7.8 a drive later on the new one is under a point, against the
  roughly 8 % a fully open or blocked reference would give — and the −8.6
  was read with the old hose already off for a few seconds. **The hose
  was at most a small share of the extra fuel**; the rest comes from
  elsewhere (H16, H17, or the regulator or an injector itself). **Since
  6e** (25/10 night) not H16 and not the regulator's reference: with the
  canister cut off the regulation sat near zero on top of −7.8 (H16), and
  the regulator answered its hose. Left: **an injector** (H17 refuted
  29/10, `refuted.md` C21) — a
  regulator holding a high base pressure would scale the fuel alike at
  every load, not take it away at idle alone (*reasoned*).

- **15/11 night, the old logs** (S19, *The old logs re-read for the
  split's form*): on 8n's relearn drive the idle's correction stood at
  −2.4 % for the first 80 s of a warm stop and at −5.9 % a minute and
  a half later. **Against a rail pressure that is simply high as the
  whole of the idle cell** — it would be there from the first second;
  not against it as the −2 to −3 % under the step, nor against a
  pressure that rises only at idle through the return (8u reads both).

**Tests:** a rail pressure gauge (`plan.md` 8u, *the owner*, 15/11;
not bought from 10/10 until then; VW's figures: 2.5 bar at idle, 3.0 with the regulator's hose
off, **2.0 bar or more ten minutes after switching off**, the last being
S19's question — `vcds.md`). The swap of injectors 2 and 3 (17/11)
cleared the injector form (`refuted.md` C29).

### H8. Idle air control and the throttle body

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | — | ~ | — | — | — | ~ | — | — | ✔ | — |

**Against, the swell** (15/11, S1, *8h's plain idle and its loads*):
the idle regulator (055 field 2) holds through cylinder 3's swells and
falls on 18 warm stops, r 0.02 within a stop.

**For: S20, by its timing** (*owner*, 26/10): the speed has been hard
to hold at a steady pedal since the job of 1–2/10, which fitted this
throttle and took up its cable's slack. Not measured; a capture with the
throttle held still would show whether the plate or the engine moves.

**Against, the target** (10/11, 0x288 b5; S1, *The idle speed
target*): the ECU's idle speed target is 780 rpm at every warm idle on
record and the engine holds 15–18 rpm above it every time; raising the
target to 830 left `IdleHealth` at 66. The governor's set point is
steady and met.

**Against:** a dip is one firing that fails and recovers in a quarter of a
second (three in four; one in five is two firings in a row, and warm
those lean to cylinder 3 too — S1, *How many strokes make a dip*, 5/11);
the dips do ride a 0.8 Hz swing of the idle loop (S1, 5/11), but as the
moment a marginal cylinder fails, not as a hunting loop of its own; the plate angle in every VCDS log is steady and
the misfires do not ride on it (27/9); the potentiometer track has no dead
spot or dropout on the bus; the throttle is **new since 2/10** (Pierburg
`7.03703.13.0`) and the idle fault outlived it; it acts on all four. Kept
because it is in the idle air path, not because anything points here.

**The owner's hypothesis, 26/10: the idle regulation itself.** 055's
learnt value has been negative on this engine since September, so the
ECU idles it on less air than its base model; **less air is a smaller
charge, and a smaller charge is nearer the edge S1 reads the idle at**
(*Load smooths it*) — more air, from a load or from the learnt value set
aside (S1, *A second reading*), calms it (*reasoned*). **For**: on 26/10
`IdleHealth` off the display fell as the value relearnt from −2.78 to
−0.90 (`idle-log.md`); 014's counting was read then as following the
value (`refuted.md` C19, refuted 2/11); S20 dates from this throttle (*owner*). **Against**: in the same
log **014 counted about as often at −1.0 as at −2.8** (no trend,
`idle-log.md`); the display readings were single figures across changing
temperature, loads and time, with no `IdleHealth` in the VCDS log to set
against the value; and a dip is one failed firing (S1), which a
regulator can bring nearer but not cause.
**The A/C stop of 27/10** (6k; S1, *A second reading*): **for** — the A/C
sets the learnt value aside and the idle calmed at once, 014 silent for
eight minutes, and with every other load on the grade improved as the
learnt value walked from −1.04 to −0.77; **against** — in the A/C's sixth
minute, the learnt value still aside, the grade climbed back to 56–75.
One stop; it supports the regulation narrowing the margin, not as the
whole.

**The sum of 055's two fields does not move** (27/10, re-read over
every VCDS log with 055 and 014). Field 2 (the live regulator) plus
field 3 (the learnt value) sits at **−0.9 to −1.35 g/s at every warm
idle on record**, whether field 3 was 0.00 (2/10, 4/10 after 098),
−1.2 (settled) or −2.78 (26/10, when field 2 stood at +1.46). After a
reset the live field carries the whole correction at once and hands it
to the learnt one over **two to three minutes of warm idle**; the
learnt value always ends at about −1.1 to −1.3. On 27/10 the A/C did
the same bookkeeping: **everyday −1.07, A/C −0.98, A/C with the loads
−1.10** — the learnt value set aside, the correction the same.
So **zeroing 055 does not give the warm idle more air** beyond its
first minutes (*measured*, VCDS 003 on 4/10: 3.1–3.3 g/s and a plate at
2.6–2.8° in the quiet phase after the reset, as on settled sessions),
and 6k's calm with the A/C is the A/C's load, not the value set aside.
The one state that moved the sum was every load but the A/C: −0.69,
the ECU giving more air than its model. Against the regulation half of
H8 as "less air"; the −1.1 reads as what this engine needs at a warm
idle (`refuted.md` C19).

**Do 055 and 032 belong together?** (*the owner's question*, 26/10): the
ECU takes away both air (055) and fuel (032's idle cell). *Reasoned*, not
measured: **not through one cause**. Air the MAF did not see would push
055 negative but 032 *positive* (lean); extra fuel — vapour from the
breather or N80, fuel in the oil — pushes 032 negative, but the lambda
loop brings the mixture back to λ = 1, which leaves the idle's torque and
so 055 where they were. And both are answers, not causes: undone, the
idle would run rich and fast, not better. **The exception was 26/10**,
when 055's −2.78 was learnt wrong against the stick, and undoing it did
help.

**Tests**: **6g, done 29/10** — 032's idle cell back at −8.6 with 055 at
−1.11, so the two are independent and the rich idle has its own source
(H7, H16; H17 refuted, `refuted.md` C21). **5a, done 3/11** (`42`,
`vcds-step5a-warm-014-055-003.csv`): the learnt value walked from −0.28
to −1.24 over the warm stop, **only after a throttle blip** — each one
started it about 22 s later and moved it about 0.27 g/s over about
20 s (*owner*, seen in the log) — while field 2 gave the difference
back, the sum at −1.2 to −1.4 throughout. **`IdleHealth` fell as it walked**: 93
at −0.3 to −0.6, about 84 at −0.6 to −0.85, 41–67 from −0.85 to −1.25;
014 zero throughout. **Against the regulation narrowing the margin**
on its face, since the idle calmed as the learnt value went down; but
the stop came straight after the motorway, and the first minutes after
high revs read rough on their own (`tools/afterpull.py`), so time and
the value cannot be told apart on one stop (*reasoned*). Not a test
any more: 5b's stops are on a settled value.
**12/11 evening, 003 alone at three rows a second** (`50`; S1, *The
queue drive, and what the ECU sees through a swell*): the scatter of
the advance in a 10 s window does not go with the common part in it
(r +0.08, 48 windows) but with the scatter of engine speed (+0.75);
only its row-to-row jitter leans that way (+0.45), as a governor
answering would give too. Nothing for the regulation narrowing the
margin; the order of spark and speed step is finer than VCDS reads.

### H11. Both lambda probes shifted alike

*Added 10/10 at the owner's request, as a weak hypothesis written down so
that it is not argued again.* *Condensed 17/11*; every reading, the five
marks, the relearn drive minute by minute and the four calm minutes of
10/11 are in `git show 5e1ddf2:docs/engine-health/open.md`, this heading.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | — | ~ | ~ | — | — | — | — | ~ | ~ | ~ | — |

**What is left: the idle-only form** (*the owner's suspicion*, 9/11;
*reasoned*): the front probe reads richer than the mixture only at
idle — the coolest, slowest exhaust — and right under load. The ECU
then leans the idle (032's negative idle cell) with part load untouched
(the split), and the true idle mixture is lean. A plain offset would
pull both cells alike, so it is not S19's split; 032's idle cell has
been negative since August (−5.5 % on 20/8), before any repair.

**How a probe can read rich at idle only** (*general*; which, if any,
not known): a probe slower from rich to lean than back (SSP 175: a
change of reaction time is not compensated); **hydrogen from unequal
cylinders**, which reads rich and would fool a new probe too; poisoning
(the old front probe's tip came out coated, 10/11); a weak heater —
**041 read 27–31 Ω on 9/11, inside the specification, so not this**.
Misfires push the other way (their oxygen reads lean).

**Both probes replaced, 10/11** (`plan.md` 8c, done; **the old probes
seen**: the front one's tip coated; `refuted.md` D13
for the new rear probe's own fault, S23):
- **The reading before the swap** (9/11 night): at every idle the rear
  probe sank towards lean over the minutes — for H11, not proof; **what
  the rear probe can and cannot say**: four causes give it (the
  front probe rich at idle; hydrogen from unequal cylinders; air between
  the probes, H2; a converter's store), and the rear probe cannot tell
  them apart.
- **The reading after the swap** (10/11): the rear probe flat at
  0.59–0.60 V, the healthy shape, for
  about 18 minutes, then the new rear probe's fault (S23). **So the old
  probes carried most of the lean mean behind the converter.**
- **But the idle did not follow**: of the five marks set beforehand,
  **mark 1 failed** (032's idle cell back at −6.3 after one drive and
  on **the relearn drive** of 10/11 evening, `47`, as on the old
  probes; 014 counting from 16:33 there), **marks 3 and 4 failed**
  (`IdleHealth` 48–90, the A/C still about 50 lower), **mark 5 failed**
  (cylinder 3 the weak one again, `cylscan.py`), and mark 2 was spoilt
  by S23. **H11's idle form has no mark left standing**; a probe's
  speed or the hydrogen form are not excluded, and neither is shown.
- **The four calm minutes of 10/11 evening** (17:38–17:42, `47`): two
  steps in the grade with nothing on the bus moving; 3 from −22 to −9 %
  — 3's own fall (S1, *Every stroke named*), before the clear that reset
  032. Left as an anomaly (*the owner*, 10/11 night).

**Against**: a four-gas analyser would read what the rear probe
cannot — **declined by the owner** (10/11). Nothing planned; 036 watched
at VCDS sessions (`plan.md` 8f). Ranked A5.

### H12. Driveline play read as misfires

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | — | ✘ | ~ | ~ | ~ | — | ✔ | ✘ | — | — | — |

**Against:** the MAF swap halved the dips; play repeats every 360°, the pairs
1+4 and 2+3, while the dips sit on 3 and 4, 180° apart; the puffs come with
the dips, and play makes no unburnt charge. **The clutch minutes** (12/10):
pedal up no rougher than down — not the gearbox side (S16). The crank
pulley's damper fine by eye.

*Until 27/10 evening S12 counted for this hypothesis; it turned out to be
a sticking pedal (`refuted.md` D6).*

### H13. Deposits after years of gentle driving — inlet valves, chambers, ring lands

**Re-read 12/11, the third research** (S1, *Every stroke named*):
**for.** Cold, the weak strokes fall 3 > 4 > 1 > 2 and 4 is weak beside
3 — the borescope's order of the deposit (3 > 4 > 2 > 1) but for the
last two — and warm it is 3 alone, the cylinder with the most. A
deposit that soaks fuel cold fits both cylinders cold; a seat or a
stem that carries it fits 3 warm, its swell and its step (H1).
Against: the clean left 3's floor where it was (−9 % before its cut at
stop 3's end and −7 to −9 % at stop 7) and 3 led again a day later.
**12/11 evening** (S1, *The swell's shape*): the swell read as a seat
on 3 fouling at idle and burning itself clean (H1) is this entry's
deposit at work — it fits the clean taking the swell for a day and
`46`'s stops showing no growth at all; against "a flake moved", the
fall takes 30–45 s.
**17/11, the fourth research** (*What the forums say*, searched again
17/11; S1, *The advance, the cold fast idle, a warm engine-off and a
coast-down*): CARB's 2006 staff report gives a car whose intake valve
deposits on one cylinder made it rich by an EGR effect, the front
probe weighting it, the loop leaning all four and the rear probe lean
throughout — the first source tying one cylinder's deposit to the sign
of 032's idle cell; its size here a point or two of the cell
(*reasoned*). Read with H1, as what holds a seat off. The cold form
splits: 4's cold weakness fades steadily with the oil, 3's deficit
does not follow temperature after the fast idle.
**14/11 night, every cleaner set against the bus** (S1, *Before and
after each repair*): **against** — the DFI can, both 44K tanks and the
hydrogen left 3's weak strokes in a swell where September had them
(21–30 per 1000 at −16 to −23 %) and the grade's mean at 61–67 since
12/10; the hydrogen gave one afternoon of shallower swells. For: 014's
share halved in the week of the 44K tanks — with the regulator's hose
and the oil in the same week. *Another can was not planned until
17/11 evening*: the time 3 spends on its floor rose from 0–20 % to
21–81 % across that same week, and not after the Liqui Moly can of
15/10 (S1, *The floor and the common part read apart*), so **two more
cans of BG 44K Platinum** (`plan.md` 6t, *the owner's decision*).

**The ring form, for the floor** (17/11 evening, *the owner's
question*; *reasoned*): carbon in 3's ring grooves keeping a ring
sluggish. A ring seals by gas pressure, so it leaks most at the idle's
low pressure and less under load — a share that falls with load, which
can read as the fixed amount the floor is (S1, *The floor and the
common part read apart*); the EPR flushes, aimed at ring-groove
deposit, fell in the week the time on the floor rose. Against: 12 bar
even cold, little oil burnt, the plugs dry; it gives no swell. **Its
test**: the leak-down hissing at the oil filler on 3 (item 9), a dry and
a wet compression on 3 against the others; its cure an EPR flush or
the ring soak of Kia/Hyundai's TSB 23-EM-007H.
*Added 15/10 at the owner's request.* The engine seldom saw more than
3000 rpm for at least nine years (*owner*). Gentle use builds deposits where
hard use burns them off (*general*).

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ~ | ✔ | ~ | — | — | ~ | ~ | ~ | — | ~ |

- **11/11, the second research**: the clean's relief lasted a day
  (`47`), and **no source gives seat deposit forming again in a day** —
  the one time base found is about 200 hours for inlet-valve deposit
  (SAE 922263) — so a flake moved, or lodged and burnt away, fits better
  than regrowth (SAE 2000-01-2858: flakes trapped by chance, water the
  strongest trigger); and **the rough start after a hot drive is 3's**
  (S1, *The rough start of a warm stop*), read with H1's exhaust seat.
  *Reasoned*.
- **9/11, the clean** (S1, *The clean of 9/11*): **after it 3's swell
  was gone at stop 7** — its weak strokes 25 → 5 per 1000, the rough
  first minutes and 014's storm absent — **for, on 3**; **3's floor
  (−8 to −9 %) and the settled level kept**, and the swell back a day
  later: against H13 as the whole story. *This bullet read "its share of
  the dips 48 % → 23 %, its steady deficit 7–14 % → 0–3.6 %, 4's
  deficit kept" until 12/11.* **With its gas flowing
  the idle had no dips at all**: the weak strokes are a burn that fails,
  which deposit makes (*general*) but not it alone. ⚠ One stop each
  side; straight after the clean 3 was still short for minutes.
- **3 the weak one at every warm idle** (S1, *Every stroke named*; `43`
  −13 %), the one ranked first inside (3 > 4 > 2 > 1): for, though
  deposits act on all four in kind. **A hydrogen decarbonisation was
  done before**, 10/8/2021 (`vehicle-history.md`), its effect not
  remembered; the deposits of 10/2026 built up since. **The owner's
  reading of 3/11** — every cylinder dips, 3 the most, so a cause on
  all four with 3 worst; all four alike just after the VW leads and
  plugs, 3 worse again two weeks later, a cylinder that burns badly and
  wears its new plug down — **keeps its first half and loses its
  second**: the small unevenness is on all four (the common part) and
  3 is worst, but 3 was not even on `40`–`41` (−14 %, 64 % of the
  weak strokes on `40`), so nothing grew worse on 3 after the leads
  (*re-read 12/11*). The plug 3 beside the others would still show
  whether it wears (the 10/10 plugs read 3 the
  cleanest after nine days, `vehicle-history.md`), and **its gap with a
  wire gauge** at the same time (`refuted.md` A2, reopened for plug 3
  alone, 3/11). It costs the plenum off; **not for now** (*the owner*,
  3/11).
- **The look inside, 19–20/10** (H13 test 3, `idle-log.md`): **no inlet valve
  back is coked** — thin lacquer on all four, so no walnut clean; **the
  chambers carry it** — thin layers on every crown, a crust on 4's bowl edge,
  and **on 3 a layer breaking up, crown and exhaust valve alike**. Ports and
  chambers rank **3 > 4 > 2 > 1** — 3 the weak one warm, 3 and 4 cold.
- **Consequence more than cause** (*the owner's reasoning*, 20/10): every
  cause put forward for deposits acts on all four alike, and 3 and 4 are
  worse — so their extra deposit reads as **years of poorer combustion on 3
  and 4**, from something that touches those two only (`refuted.md` C24). Once there, the
  deposit adds to it: a flake under a seat (18/10, `refuted.md` D10), heat and compression for
  knock on 4 (S4).
- **The inlet side, 7/11** (*the owner's reading*, H1): the crust at the
  seat ring's edge in the ports of 3 and 4, a lump standing out of it on
  3, 1 and 2 thin and even. **What the clean of 9/11 can reach**
  (*reasoned*): hydrogen burns in the chamber; the port above a closed
  inlet valve sees only the incoming charge, so deposit on the inlet
  side, the seat ring's upper edge included, is the least likely to go. The gas does pass the ports — it goes in behind the MAF
  (*owner*) — but cold, hydrogen and oxygen do nothing to carbon; what
  can clean is the flame and its steam, in the chamber (*general*; the
  vendors' chemistry above).
  So if 3 stays weak after 9/11, the inlet seats are left standing
  (H1), and the leak-down is the test. **9/11: 3's floor kept at stop
  7, its swell gone for a day** (S1, *The clean of 9/11*) — the inlet
  seat left standing is 3's. *This read "3 not weak at stop 7, 4 still
  is — the inlet seat left standing is 4's" until 12/11.*
- **4/11, the two patterns on their own** (S1; *reasoned*, agreed with
  the owner): with H1's exhaust seat on 3, **the one reading that fits
  both** the calm under load and the calm that lasts after revving
  (H1). **What 9/11 should then show**: loads off nearer loads on, and
  queuing nearer the drive after revving. *Not read 9/11: no stop after
  the clean had the A/C or a queue; the display's stops will.*
- **4/11, the owner reads coarse deposit up to the edge of 3's exhaust
  seat** on the photos of 20/10 (H1): for, the contact line itself not
  seen.
- **With a cleaner in, the idle after high revs starts calm and worsens
  over minutes; without one, the reverse** (S1, *After high revs*): one capture and two display evenings, so far (the second 18/11, on 6t's first can: 40–50, then 70–90 within a minute). 19/11 evening on the same can, after high revs at light load (not brisk), one stop to 62 at most, the next after the same kind of drive at 90–110 (*owner*: no correlation, not predictable): neither for nor against. 20/11 on the same can, a queue at 80–100 before the revs and mostly 60–89 after them (*owner*): the reverse of the pattern, against, one evening; the stop then 40–45 after about five minutes.
- **18/10 has not come back** in six days of hard driving, a strong 44K
  tank among them (`refuted.md` D10) — what a flake that burnt off does.
  Weak: one episode, and its absence.
- **The steady pattern over the cylinders, re-read 12/11** (S1, *Every
  stroke named*): warm 3 alone gives less, 4 level, 2 and 1 above; cold
  4 weak beside 3, the weak strokes 3 > 4 > 1 > 2 — the borescope's
  order but for the last two; and 3's swell moves over minutes, as
  deposit that soaks and gives back fuel would (*reasoned*): for. *It
  read "warm 3 and 4 give the least", and "cold both spread over all
  four", until 12/11.*
- **Against:** a detergent premium fuel since 2017; compression even;
  **the strong first 44K tank changed nothing** (23–24/10, *owner*): about
  450 km on it, hours above 4000 rpm, and `IdleHealth` at the warm stops
  70–80 as before (S1, the table). The owner now expects the cleaner to do
  nothing for the idle (24/10).

**Tests:** the cleaner and hard driving (a tank from 15/10, done; two tanks of
BG 44K, **the second run out 29/10, the idle no calmer at its end** —
everyday about 70 on 27/10 and 70–100 on 28/10 (S1's table); the
EPR flushes and fresh oil, done 26/10).

### H14. The remap of 6/2018 — at full load only (S4, S19's part-load cell)

*Added 16/10 at the owner's request as the idle's ignition or its margin;*
**the idle half refuted 3/11** by the tuner's files and the drive on the
original map (`refuted.md` C23, *agreed with the owner*). What is left is
what the remap did change: the corner of highest load.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ✘ | — | ✘ | ✘ | ~ | ✘ | — | ✘ | ✘ | ~ | ✘ | — |

**What the remap changed** (the two whole flashes from the tuner, 3/11;
compared byte for byte, the files not kept here; the tables with every
cell in the owner's private artifact *Beetle AQY remap diff*). Both
images carry the same identification, `06A906018EJ … 0261206327
1037352075 … M5.92`. **462 bytes differ**: 257 are erased flash (0xFF)
written 0x00 after the calibration, most likely the tuning tool's
checksum area, and **205 sit in five 16-point tables**, every one of them
only in its **last three or four columns and from the fifth row down**:

| table (address, size) | by its shape (*reasoned*, no map definition) | the remap |
|---|---|---|
| T1 (`0x09C03`, 16×16) | a fuel factor, values about 128 = 1.0 | **−6 to −7 counts, about −5 %** |
| T2 (`0x09E09`, 16×16) | a fuel factor on other inputs | **−4 counts, about −3 %** |
| T3 (`0x0B750`, 16×16) | ignition advance, rising with speed, falling with load | **+1 to +4 counts** |
| T4 (`0x0B8C6`, 16×12) | a smaller ignition table | **+1 to +3 counts** |
| T5 (`0x0B9AA`, 16×16) | a second ignition table, a little higher than T3 | **+1 to +5 counts** |

Taking the rows as engine speed and the columns as load, which is how the
advance tables fall: **less fuel and more advance at high speed and the
highest load, nothing anywhere else.** At Bosch's usual 0.75° a count,
+0.75 to +3.75° (*general*; this ECU's scale not read). **Not touched**:
the idle region of all five, and every other byte — so not the idle
speed, the idle advance, the misfire detection (route 6), the limiter,
the overrun cut or the MAF's curve (`refuted.md` C22). A classic mild
remap of a naturally aspirated engine. The axes are stored as
increments; no map definition for this software is public (searched
3/11; the image names its source `DAMOS39M / 39M02G3-S`).

**The axes, fitted** (3/11, *reasoned* from measurement): T3 laid over
the advance VCDS 003 read on the original map (`vcds-step5a-*`, 1,642
samples without knock retard, 16 full-throttle points at 2500–6250 rpm).
**Rows: 40 rpm a count** (the full-throttle line fits to 0.85–1.1° RMS;
part load alone gives 42). **Advance: 0.75° a count, offset about −25°**
(a free fit gives 0.8–0.9; 0.75 with −24 to −26.5 fits nearly as well,
and part load alone gives −25). **Load: full throttle sits at about 120
counts of the column axis** (115–130); at the usual 0.75 % a count
that is about 90 % relative fill, which is assumed, not fitted. Read
that way:

| table | the change begins at | full throttle at ≈120 | reached |
|---|---|---|---|
| T1 fuel −5 % | 1400 rpm, column 90 | between columns 110 and 130 | **yes, wholly** — and heavy part load (≈108) too |
| T2 fuel −3 % | other axis types, units not known | — | not known |
| T3 advance | 1880 rpm; column 130 (+1), 140 (+2), 160 up (+4) | just below 130 | **practically not**, half a count at most |
| T5 advance | the same columns | just below 130 | **practically not** |
| T4 advance | 1880 rpm; column 110 (+1), 120 (+2) | on 120 | **yes, +2 counts ≈ +1.5°**, if the ECU uses it |

So **the advance at full throttle reads the same on both maps because
the added advance lies above the load the engine reaches**; and **T1's
leaner fuel reaches full throttle and heavy part load**, where the
lambda loop runs and the multiplicative cell of 032 would learn it back
— the remap's +5.5 to +8.6 % (S19). T4's lower values fit a knock-safe
table that advance falls back to; raising it would let more advance stay
under knock, which fits cylinder 4's deeper retard on the remap
(*reasoned*, not settled).

**What the remap was worth** (*the owner's question*, 3/11; *reasoned*).
At full throttle the lambda loop is off, so T1's −5 % did reach the
mixture there — but **the learnt multiplicative trim (032's part-load
cell) is applied in open loop too** (*general*, Bosch Motronic), and on
the remap it had learnt +5.5 to +8.6 %, so at full throttle it gave back
most or all of what T1 took, as far as that cell was T1's and not the
MAF's. The added advance lies above the load the engine reaches (T3,
T5); only T4's +1.5° is reached, if that table is used. **Measured**:
the same full-load air, advance and b7 plateau on both maps. So **the
gain was small to nothing on any channel read here**; what is not read
is the full-load lambda itself (no wideband probe) and T2's inputs, and
there was no dynamometer.

**Where it still reaches** (*reasoned*):
- **S4**: more advance and less fuel at full load is what makes knock;
  on the remap cylinder 4 retarded to 11.2°, on the original to 6.0° on
  3/11 — **and to 12.7° on 12/11**, mostly at 3,500–4,600 rpm where the
  two maps' advance is the same (S4, *Since 12/11*). *This said "the
  remap deepened 4's retard" until 12/11*: the depth is not the map's;
  it did not make 4 the one that retards either.
- **S19's part-load cell**: +5.5 to +8.6 % on the remap, +3.1 after one
  drive on the original, +3.9 after two, **+6.3 on 6/11, settled**
  (S19). If T1/T2's leaner corner reached loads the lambda loop runs at,
  the cell would have fallen to about +1 to +3 on the original map; it
  did not, so **the map does not explain it**.
- **Against both**: VCDS 003 reads the same full-load advance on both
  maps (below), so either the engine does not reach those columns, or
  knock control takes the advance back.

**The pulls of the second drive, 3/11 evening** (`43`,
`vcds-step5b-pull-014-003-020.csv`; the pull in 4th asked for the
converter, `docs/firmware/can-decoding.md` question 8): two in 4th from
2,250–2,380 rpm to 5,760 at 91–97 °C of oil, then full-throttle runs in
2nd–5th at 101–105 °C. **The pulls in 4th were short of air**: 33.6 g/s
at 2,400, 66 at 4,500, 74 at 5,000 and **flat at 75–76 g/s from 5,000
up**, against `42`'s 76 / 82–83 / 85–87 and this drive's own later
runs, 79–81 at 4,500 and 86–89 at 5,200 (`vcds-step5b-warm-014-055-003.csv`);
the advance 1–5° higher, as a lower load asks. **b7 155 at 2,400 and
167–171 from 4,000 to 5,200**, against 169 and 183–187 on `42`'s first
pulls and 185 and 192–198 on `19`; the later runs read 192–196 at
4,500–5,000, as `42`'s and `19`'s did. So 2,400 rpm was held long enough
but not on full air: **the torque scale is neither confirmed nor moved**.
`42` showed the same in kind, smaller (its first runs 181–192 against
196–206 later, on 5–11 % more air, `idle-log.md`). **What admits less
air on the first pulls of a drive is not read**: no group logged has
the intake air temperature, and a MAF reading low would lower b7 the
same way, since the ECU computes b7 from its load (*reasoned*). **Not
pursued, not a symptom** (*the owner*, 3/11): perhaps the engine needs
to be warm for longer before it takes its full air; he felt the pulls
of this drive weaker too.

**The ECU** (`vcds.md`): Bosch M5.9.2, hardware `0261206327`, software
`1037352075` V04, 256 KB flash. No map definition is public.

**The drive on the original map, 3/11** — the measurements behind
`refuted.md` C23 (`42` and `vcds-step5a-*`, fresh adaptations), on
what the cleaner and the adaptations cannot move:

| | remap | original map, 3/11 |
|---|---|---|
| warm idle advance (`idleadvance.py`) | median 3.0–3.8°, p10 0–0.8, p90 6.0–6.8 | **3.0°**, 0.8, 6.8 |
| full-load advance, 3500 / 4500 / 5000 / 5500 rpm (003) | 19.5 / 21.8 / 22.5 / 23.6° (`40`) | **19.5 / 21.0–21.8 / 21.8–22.5 / 24.0–25.1°** |
| full-load air, the same speeds | 58 / 77 / 81 / 88 g/s | **55–56 / 76 / 82–83 / 85–87 g/s** |
| b7 at full throttle in 3rd, 4000 / 4500 / 5200 rpm | 187 / 192 / 187 (`40`) | **185 / 189 / 187** |
| the overrun cut (`coastscan.py`) | 0.8–1.6 s after the lift, back at 1,300–2,400 rpm | **0.76–1.39 s, back at 1,463–1,848** on the coasts that ran down to idle |
| 014 at idle / under load | counting / 15 in about 4,300 | **0 / 0 in 1,388** |
| 020, cylinder 4 at full load | 40 %, to 11.2° (`40`) | **41 %, to 6.0°** (S4) |
| `IdleHealth`, warm | 80–105 on the display (28/10–2/11), 61–67 on `40` | **54 ± 3** settled into a stop, 63–77 near home |

**Read** (*reasoned*): **the advance, the air, b7 and the cut are the
remap's to within a VCDS step**, at idle and at full load. **014's zero
and `IdleHealth` inside the stop are not the map's**: the files show the
idle region and the detection untouched, so they are the fresh
adaptations or the engine on the day; 5b read them again: **014 counted
on `43`** at `42`'s load, so its zero was the fresh adaptations (S3). The idle cell
of 032 came back at once (S19), so the split is not the map's either.

### H18. Oil past the valve-stem seals, drawn in at idle

**12/11 evening** (S1, *The swell's shape, and what the common part
follows*): **for one valve, 3's inlet, as the swell's second reading** —
oil gathering at idle's vacuum and drawn in at once is a trap that
fills and empties, the sawtooth's shape; against, no blue smoke, the
plugs dry, and a load lifts the swell at once. **Against it as the
common part's cause**: the common part does not grow with the time
into a stop (r −0.09), which this entry's "worse after idling" asks
for.

*Added 26/10 at the owner's request*, from his reading of 26/10 (S1,
*Temperature*): the warm idle stays at 90–110 through a gentle warm-up
and calms only after a drive in which the engine works, and stays calm
for the next 15–20 minutes of idling. **The mechanism** (*general*;
owners' forums, not a manufacturer): a worn or hardened stem seal lets
oil run down the valve guide, and the intake's vacuum, highest at idle,
draws it into the cylinder, where it costs combustion; under load the
vacuum falls, the flow stops, and what collected burns away.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ✘ | — | ~ | — | — | — | — | — | — | — | — |

- **For: the shape of 26/10**, worse after idling and gentle driving,
  calmer after work, the calm lasting — what oil collecting at a small
  charge and burnt off under load would give (*reasoned*).
- **For: the small unevenness on all four** (S1, *Every stroke named*,
  *The small steps are on all four*): the seals age together, and that
  part of the idle is common. **Against: the misfires and the steady
  deficit are 3's**, at every warm idle on record. *Until 12/11 this read
  "for: since the VW leads the dips sat on all four alike; against since
  3/11: one cylinder again" — those leads never spread them (Naming the
  cylinder).*
- **For, weakly: what the screen showed** on 19–20/10 (`idle-log.md`):
  a thin lacquer on the back of every inlet valve and wet patches on
  every crown. Oil from the guide would leave both, but so would the
  breather's oil mist, fuel or condensed water; a cheap screen with the
  engine stopped cannot tell them apart.
- **For, 12/11 night** (the one-valve form on 3): load helps, measured
  — 3's deficit a fifth of a stroke at idle and with the pedal light,
  1–3 % at full load (*Naming the cylinder*, *Off idle*); H3 and H20
  predict the same.
- **For, 17/11, the first direct sight of it** (`plan.md` 8z, the
  lower manifold off; H3, *Oil soaked into the joint*, *The lower
  manifold off*): **a dark brown liquid standing round the backs of
  inlet valves 2, 3 and 4**, there before anything was washed
  (*owner*; the album, 01:44:27–01:45:06), none seen at 1's. Oil down
  the stem onto a shut valve is what this entry claims. **It does not
  pick 3**: 2 and 4 stand in it too; and oil through the lower joint
  (H3) leaves the same. **What tells them apart** (*reasoned*): the
  joint is new from 17/11 — the swell gone on the stop after is the
  joint's oil, the swell as it was is not. **17/11 (`54`): the swell
  as it was** (S1, *The first stop on the new gasket*), so not the
  joint's oil (`refuted.md` C28); the stems, or 3's seat, are left.
- **Against: no blue smoke seen**, ever (*owner*, 26/10), and the plugs of
  20/10 dry black, not oily. The oil on every plug's thread is from the
  cover side and says nothing about the chamber.
- **Against: 26/10 itself.** The calm came after engine braking downhill,
  when the vacuum is at its highest and a leaking seal passes the most;
  the drive's load after it would have to burn off more than the coast
  drew in.
- **Against, 4/11** (S1, *driving does*): the calm after revving — the
  overrun on the way draws the most oil past a seal.
- **Against: the dipstick** (`plan.md` 6i): no loss can be read between
  top-ups. **How much oil it burns is not known.** **5/11, the first
  reading** (*owner*; `photos/dipstick-2026-11-05.jpg`): **0.5–1 mm under
  the top mark at 155,546 km**, 522 km after it stood at the mark —
  within what the angle of the car and the draining time can make, so not
  a consumption by itself. **11/11 evening, the second** (*owner*, given
  12/11; the album 20:51:55, the car standing in the garage): **about
  another 0.5–1 mm lower**, the film ending a few millimetres short of
  the mark, at between 155,853 and 155,969 km — **some 850–950 km since
  the mark, two readings falling the same way: a small consumption**
  (*owner*: "it eats a little oil, nothing terrible"). How much in
  litres is not read off a dipstick without its span, which is not
  recorded here; no top-up yet. **The owner's reading**
  (5/11): oil past the rings, held by deposit (H13), which the wet-looking
  patches of the borescope photos might be — against it so far, the plugs
  dry, no blue smoke, compression even.
- **Against, 17/11** (S1, *The advance, the cold fast idle, a warm
  engine-off and a coast-down*): 3's deficit in the first 15 s after a
  coast-down — the deepest vacuum, where a seal passes the most — is
  what it is a minute later; nothing of 3's own is drawn in on the
  overrun.
- **S3 ~** for the same reason as S1: misfires at idle, on all four.

**Tests:** **the oil consumption on the fresh oil** after the change of 26/10,
read on the dipstick from a photographed level (`plan.md` 6i) — oil
burnt lowers the level, fuel in the oil would raise it (`refuted.md`
C21); **the plugs** (`plan.md` 8v) at the next
change, for oily deposit on the firing end. A compression or leak-down
test does not reach the seals.

---

### H20. Coolant into cylinder 3 — a weep at the head gasket or the head

**Re-read 12/11, the third research** (S1, *Every stroke named*): 3 is
the cylinder by every measure, which this entry needs; a weep would be
worst after a hot drive, as the swells often are, but they also start
minutes into a stop and end in a step (`40`, `47`), which pressure
falling slowly does not give. Its test stands (the CO₂ test, item 9).
**12/11 evening** (S1, *The swell's shape*): steam fits the mixture
not moving and every stroke weaker; nothing in a weep fills and empties
by the minute, and `32` grew three times over in one long idle.

*Added 4/11/2026 at the owner's request*, as a weak candidate after `43`
named cylinder 3. **The claim** (*general*): a millilitre a day past the
gasket or a hairline in the head next to 3 enters where the cylinder's
pressure is lowest, at idle vacuum, and steams the charge — a misfire
at idle on that cylinder, eased by load, and a plug kept clean.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | — | — | — | — | ~ | — | — | — |

- **For:** one cylinder at idle; load helps (a higher manifold pressure
  draws less in, *reasoned*); **plug 3 the cleanest** of the 10/10 set
  after nine days (`vehicle-history.md`, the photos), on the cylinder
  that misfires most; S2's puffs could be steam as well as unburnt
  charge.
- **For, 12/11 night**: load helps, measured — 3's deficit −21 to
  −26 % of a stroke at idle and with the pedal light, −1 to −3 % at
  full load (*Naming the cylinder*, *Off idle*); H3 and H18 predict
  the same.
- **Against:** **the level does not visibly fall** (*owner*, 4/11) —
  weak against a weep this small, which is why it is kept; **no
  emulsion** under the cover, on the cam or the dipstick (1/10,
  `refuted.md` C13); compression even (A4, cold); the borescope shows
  **no steam-cleaned crown** on 3 — its crown carries the most deposit,
  not the least (*What the forums say*, the photos read again, 4/11); the warm-up to
  99–100.5 °C holds; no white smoke reported; **the calm after revving**
  (S1, 4/11; *reasoned*): the coolant's pressure is highest after a hard
  drive, so a weep should be worst then, not best.
- **17/11, the fourth research** (S1; *What the forums say*, searched
  again 17/11): weakly against — with the warmer coolant of the fan's
  cycle 3 is a little better, not worse (+0.18 % of a stroke per °C),
  where a weep driven by the system's pressure would go the other way
  (*reasoned*); one AQY forum lead, 3 missing under about 800 rpm after
  a coolant stop-leak (not read to its end; no stop-leak ever put in
  by the owner, *owner*, 17/11). **The CO₂ test can miss a small weep** and tests the
  other direction; the system held at the cap's pressure for hours and
  the borescope in 3 read it better (a lead).
- **Test:** **a combustion-gas (CO₂, "block") test of the coolant**,
  warm — a few hundred Kč at a garage or a kit; `refuted.md` C13 never
  had one. A leak-down (H1's test) watched at the expansion tank for
  bubbles on 3 says the same.

---

### H21. The probes' wiring and connectors — the harness side, not changed with the probes

*Added 10/11 evening at the owner's request* (his idea: a joint in the
probes' wiring that moved that day, and the catalyst test that put it
right for a while). Both probes were replaced on 10/11 with their own
leads and plugs; **the sockets on the harness side, the wires to the
ECU and their earths are the car's** (`vehicle-history.md`).

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | — | — | — | — | — | — | ~ | — | ~ | — | — |

**S23 closed 12/11** (`refuted.md` D13; *the owner's decision*): the
new rear probe's own fault, the old one healthy on the same harness on
two drives — **so H21 lost its one ✔ with the column**; what is left of
it is S19's idle cell (the front probe's damaged signal-earth wire,
below) and S12's ~. **Eighth in list A since 15/11 evening** (fifth
before; *agreed with the owner*, after 8h, below).

- **For, S23** (*reasoned*; *S23 closed 12/11 as the new probe's own fault, so this no longer stands for the harness*): a leak to earth in a damp or oxidised
  socket pulls the signal down in proportion, so the ceiling falls under
  load as well as the idle, which is what the rear probe did from 16:57
  on 10/11, before reading zero at full load; it came back after the
  revs of the basic settings, not after cooling, which suits a contact
  moved by vibration better than a lead melting on the exhaust. **One
  circuit, two probes, three days**: the old rear probe sank at every
  idle on 9/11 night, the new one switched to the front's swing after
  18 minutes on 10/11 morning and failed under load that evening.
- **For, found 10/11 evening** (S23, *Found at the harness*): the
  front probe's signal-earth wire (grey at the probe, brown on the
  harness side) worn and cracked inside the box the leads run through,
  and the rear probe's heater lead cracked and corroding beside its
  signal — both on the harness side the swap did not change.
- **For, S19's idle cell** (*reasoned*, the wiring of this car not in
  these files): the cell came back to −6.3 % on new probes (H11, *The
  relearn drive*), so whatever makes the front probe read rich at idle
  survived the swap. A resistance in the front probe's signal earth,
  if heater current shares any of its path, would lift the reading by
  the heater current times that resistance — and the heater runs most
  at idle, where the exhaust is coolest (*general*), so the shift would
  be largest there. Whether the signal and heater earths share a path
  on M5.9.2 is *not known*.
- **For, the idle (S1), and S12** (*the owner*, 10/11 night): a
  resistance that comes and goes in the **front** probe's circuit makes
  the ECU see false rich or lean, and it moves the mixture of all four
  cylinders after it; the idle is where the engine runs nearest its
  edge (the gas idle of 9/11, S1), so a mixture thrown about would show
  there first — and a step of it at a crawl or a moving-off would be a
  jerk (S12). *Reasoned*, and fair: nothing below rules out glitches
  shorter than VCDS's sample.
- **Against, for the idle (S1)**: (1) **the front probe's own trace**:
  033 at a warm idle, about one sample a second, 9/11 night (664
  samples, the old probe) and 10/11 morning (741, the new): **switching
  regularly between 0.06–0.08 and 0.74–0.77 V, never more than 6 s on
  one side, the correction within −4.7 to +3.9 %** — no dropout, no
  stuck value, no excursion of the correction (*ad-hoc script, not
  kept*); a glitch under a second would not show. (2) On 10/11 morning
  the new rear probe read flat at 0.59–0.60 V, the healthy shape, for 18
  minutes, and the idle was as rough and the A/C calmed it as much (H11,
  *The reading after the swap*) — the mixture behind the converter was
  right while the idle was rough. (3) A mixture moves all four
  cylinders alike; the idle's misfires and its steady deficit are 3's
  (S1, *Every stroke named*), which a mixture does
  not make. **So a part of the idle at most** — its four-alike share,
  not the cylinders' difference (*reasoned*).
- **Against, S23 as the circuit**: the new probe failing early is not
  ruled out; a lead and socket found sound leave the part. **The
  owner's own view** (10/11 night): the connectors are very likely
  sound and the leads well tucked in; he follows the harness on to the
  ECU and its earths instead (`plan.md` 8e).

**A shared earth, linking it to H4** (10/11 night, *the owner's
question*: could one earth fault tie the probes to the idle; *reasoned*
unless marked). An earth that both the probes' signal returns and other
circuits share would carry their currents and shift every reading
referred to it, **alike for both probes** — H11's literal form, which
the swap could not test — and, if the crankshaft sender G28 and the
knock sensors share it (VW's diagram for this engine lists a **sender
earth, 220**, beside G28 and T3; which senders it carries the garbled
text does not show, H4), noise there would reach 014's misfire count
(S3) and the knock window (S4, S5) as well. **What is known**: the
engine's earth under load measured clean (H4); the rear probe has been
read under load twice, the old one never (10/11 morning fine, 10/11
evening S23), and the front only at VCDS's ~1 s, so noise faster than
that has never been seen. **One test in the data, against at idle**:
the radiator fan, the largest load at a stop, runs while the coolant
falls; over the queue stops of 16:55–17:27 on `47` the rear probe read
a median **0.29 V with the coolant falling (386 samples) and 0.29 V
with it rising (475)** — the fan's current moved nothing (*ad-hoc
script, not kept*). **A second, on the bus** (10/11 night, *the
owner's question*: correlate every voltage that could share an earth):
the coolant is read twice — the ECU's sender on 0x288 b1 and the
cluster's own on 0x420 b4, a separate circuit
(`docs/firmware/can-decoding.md`, question 10) — so a load that lifts
the ECU's sensor earth would step their difference. On `47` it held
**8.6–9.2 °C with the A/C off and on, twice**, and 9.3 against 9.7 °C
with the radiator fan off and running at the warm stop: within half a
bit (0.75 °C). An NTC sender reads a few mV as a degree or more at its
hot end (*general*), so an earth that moved with these loads by more
than a few mV would have shown — **against, for the ECU's sensor
earth**; whether the probes' signal earths share it is *not known*.
**Measurable cheaply**: the voltage between the
ECU's earth and the engine block, and between each probe's signal-earth
pin on the harness side and the ECU's earth, at a warm idle with every
load on — a few tens of mV is an earth fault (*general*). **And VCDS**
(*the owner's request*, 10/11 night; `plan.md` 8h): the largest loads
switched from the seat at a warm idle, each against 004's supply, the
probes, the temperatures, the throttle's sensor voltage, the air mass,
the knock sensors and the heaters' resistance — what moves with a load
besides the supply shares its earth. **Read 15/11, below.**

**8h, the loads at a warm stop** (15/11, `53`; `plan.md` 8h, done; a
laptop session, read in a cloud session the same day; the windows by a
script not kept). The car standing, oil 101 °C, the everyday state; the
A/C (always with blower 1), the rear window heater, main beam and the
blower on 4, about 45 s each, one at a time, three rounds on three sets
of groups; each step's edges read off 004's supply (the owner's chat
times ran 6–21 s late), the logs set on the capture by engine speed.
Each figure is the mean over the load against the mean of the 20 s
either side; the scatter is of one sample.

| what | A/C + blower 1 | rear window | main beam | blower 4 | scatter |
|---|---|---|---|---|---|
| **supply (004)** | −0.25 V | −0.29 to −0.46 V | **−0.54 to −0.63 V** | −0.39 to −0.43 V | 0.1 V |
| front probe (033) | +0.01 V | −0.06 V | −0.03 V | +0.01 V (blower 3: −0.04) | 0.26 V |
| rear probe (036) | +0.07 V | +0.02 V | +0.03 V | +0.06 V (blower 3: +0.04) | 0.2 V |
| throttle, G187 / G188 (060) | +2.6° / −6.7 % | −0.1° / +0.1 % | +0.4° / −0.6 % | +0.2° / −0.5 % | 0.2° / 0.4 % |
| air mass (002) | +1.5 g/s | 0.0 | +0.13 g/s | +0.10 g/s | 0.1 g/s |
| knock sensors (026) | +0.08 to +0.11 V | ±0.03 V | ±0.03 V | ±0.02 V | 0.06–0.09 V |
| front heater's resistance (041) | one count down | one count down | one count down | one count down | — |
| coolant, the ECU's / the cluster's (0x288 / 0x420) | −0.2 to +1.7 °C, both alike | +0.4 to +2.1 °C, both alike | 0 to +2.2 °C, both alike | +0.9 to +2.4 °C, both alike | — |

- **Only the supply steps with every electrical load**; the A/C's
  own figures are its load: the idle control opens the throttle, the
  air and the injection time rise and the engine speed with them
  (+40 to +75 rpm).
- **The throttle's second sensor never moves on its own**: G188 goes
  against G187 by 1.5–2.6 % a degree in every step that opened the
  throttle, and by nothing where it did not.
- **The coolant rose up to 2.4 °C in most loads, and the cluster's own
  sender rose with it**: their difference held 8.6–10.4 °C before,
  during and after every step, within a bit or so (0.75 °C), and
  neither reading steps at a switching edge (no change over 1 °C in
  the 4 s either side of any). A sender earth lifted by the load
  would step the ECU's reading alone and at once; this is heat
  (*reasoned*: the fan's cycle, or a fan slowed by the lower supply —
  not read further).
- **The front heater's resistance figure follows the supply, one
  count**: 26.8 with the supply at 13.2 V and over, 25.5 at 13.0 V and
  under, changing in the same second as the supply in every step both
  ways; the rear's 22.9 flicks to 24.2 only at the highest supply. A
  heater's real resistance does not step in a second; a figure the ECU
  reckons from the heater's supply and current would (*reasoned*; how
  M5.9.2 reckons it is *not known*).
- **The probes**: the front's shift is under a quarter of its sample
  scatter in every step and of either sign; the rear's is upwards in
  all five, +0.02 to +0.07 V, against a scatter of 0.2 V a sample —
  about what a 45 s window can resolve, so *not resolved either way*.

**Read** (*reasoned*). **At VCDS's one sample a second, no sensor
referred to an earth moved with a load on its own**: the ECU's coolant
sender (against the cluster's), the intake air, the throttle's
sensor, the air mass, the knock sensors and the front probe moved
only as the load itself moved them, and the heater figure moved as a
reckoning from the supply would. **So against a shared earth under the
ECU's senders and the front probe** — the form of H21 that would tie
the probes to H4 (S4, S5) and to the idle; the rear probe's few tens
of mV are not resolved; noise faster than a second is unseen, as
before. What is left of H21 is the front probe's damaged signal-earth
wire for S19's idle cell, and S12's ~. **The shared-earth form
settled against, `refuted.md` C26; H21 kept for the front probe's
earth wire, from fifth to eighth in list A** (*agreed with the owner*,
15/11 evening; the place Claude's): what is left reaches the common
part only through a mixture, which the front probe's own trace has
never shown thrown about.

**Tests:** the sockets of both probes looked into from the harness side
at the next cold engine, with the rear lead's run (`plan.md` 8e); the
probes' loom and both connectors flexed with 033 and 036 logged, with
the ignition only (a leak to earth pulls the bias off its steady
0.43–0.44 V; never with the engine running, *the owner's decision*,
10/11 night — a series resistance, which would show only on a hot
probe, is left to the multimeter);
a jump in either is the find (8g, *dropped 11/11*, the owner); each wire from the socket
to the ECU's pin, resistance and insulation to earth, with the ECU's
plug off when 6n is done (the pins from the current flow diagram, read
first).

## Naming the cylinder

The bus carries no cylinder identification and 014 has no per-cylinder
counter. Two things name cylinders: the **injector cuts** (one connector off
at a warm idle), which mark their slot through a long run, and
the fault codes they leave; **and since 12/11 a third, with no cut: the
strongest slot is cylinder 2's** (*The count that does not slip*,
below; `tools/cylscan.py`). **The cuts, eight in all**: **10/10**
(`31`) 1, 4, 4, 1; **24/10** (`41`, cold) one on 4; **3/11 evening**
(`43`) one of 57 s on 4; **9/11** (`44`, `46`) one of 30 s on 4 at each
stop. No cut is asked for any more to name the cylinders (*the owner*,
12/11; `CLAUDE.md`). **Off idle** the names are carried through a
whole drive by one stroke count (*Off idle*, below; `tools/drivescan.py`).

**The leads' order on the coil** (*owner-read off the car, 1/10/2026*):
**1, 4, 2, 3, clockwise from the top tower** — 1 and 4 side by side, 2 and 3
side by side, the two pairs the coil fires together in the firing order
1-3-4-2. Which tower the coil itself calls which cylinder is not read.
*Dropped by the condensation of 20/10 and put back 21/10, when the leads
were changed.*

### The count that does not slip, the wheel, and the spread

*12/11, the third research; `tools/cylscan.py`, kept, and
`tools/test_cylscan.py`.* Three corrections to how a stroke is put to a
cylinder; **the dip shares read before them are withdrawn** (*What the
dip shares said, and what stands*, below; S1, *Every stroke named*; S3,
*What 014 counts, by cylinder*).

- **The count.** `cutscan.bridged_runs()` (removed 12/11) counted
  strokes by how long a value was held and lost one at two equal
  neighbours or a missing frame — the slips of 9/11. Engine speed integrated over time is crank
  angle, one stroke per 180°; `cylscan.track()` rounds that to a stroke
  index and lets every change of 0x280's value correct the phase a
  twentieth of its error. The rounding error stays under half a stroke
  (99.9 % of changes within ±0.42 on `09`, `31`, `43`); **on `31` one run of 883 s holds the four
  cuts (1, 4, 4, 1) on their own two slots**, and no run slips.
- **The crank wheel alternates, and it is not combustion.** Successive
  strokes read alternately high and low: cylinders **2 and 3 high, 1
  and 4 low** — the two pairs that share a half of the wheel.
  **Measured where nothing burns**, on the overrun with the fuel
  counter standing (`--wheel`, 850 windows of 40 strokes): **0.216–0.226 %
  of engine speed in each of thirteen captures** from 24/9 to 10/11
  (0.216–0.222 in the ten with twenty windows or more), and the same in every band
  from 1450 to 2500 rpm (3.2 rpm at 1500, 5.4 at 2400) — proportional
  to speed, as an angle error of about 0.2° of crank is and a
  combustion difference is not. The neutral holds of August (`10`,
  `15`: 0.22–0.23 %) and the clean's 55 minutes at 1,850 rpm (4.1 rpm,
  steady to ±0.05 from window to window) read the same. **Named** (`--wheel`, its last lines): thirteen
  overruns run into a standing idle in one stroke count, and by that
  idle's names the overrun's steps read **−0.219, +0.217, −0.218 and
  +0.219 % of engine speed for 1, 3, 4, 2** (±0.004, some 530 strokes
  each) — 2 and 3 high, and **nothing left on any cylinder with the
  alternation out** (0.02 rpm at most at idle). *This said "ad-hoc
  script, not kept" until the owner asked for it in the tool, 12/11.* At idle it is **1.7 rpm** — as large as the pattern over the
  cylinders it sits under. It lowered 4 and 1 and raised 3 and 2:
  **"4 weak, 3 hardly" was 3 weak, 4 level.** VW says the ECU learns
  the same error on the overrun for its own misfire detection (SSP 175,
  `vcds.md`); the speed it sends on the bus is not corrected.
- **The spread.** A stroke's loss shows in two values: about a quarter
  in the one before its own slot. The first dead stroke of each cut
  reads −7 to −18 rpm and then −24 to −33 (`31`, `41`, `43`, `44`,
  `46`); 6,000 isolated weak strokes read 0.22–0.33 of their own step
  already in the value before. In a steady cut the three live cylinders' gain
  hides it, which is why the cuts never showed it.
  `cylscan.deviation()` undoes it with the wheel.
- **The names.** With no cut in a run, the strongest slot is taken for
  2 (*the owner's idea*, 9/11): it is 2's at all eight cuts, and it
  puts 014's rises on the cylinder the ECU's own P0303 names.
- **The names before the injectors** (*the owner's question*, 15/11:
  every cut is from 10/10 on, on the new injectors — could the pattern
  have lain otherwise on the old set; ad-hoc script, not kept). The
  wheel is the one name that owes nothing to combustion, injectors or
  seals: 2 and 3 read high. **`17` (August, the old injectors) is the
  one capture before 23/9 where a drive and a standing idle share a
  stroke count** — `09`, `11` and `12` are idles alone, the holds `10`,
  `13`–`16` have no idle. `cylscan.track()` over the whole 360 s: **75
  windows of 60 strokes above 1,300 rpm, the same two slots high in all
  75** (0.20 % of engine speed), so the count does not slip. With
  those two slots taken for the wheel's high pair, the standing idle at
  the start (217 strokes, three parts of it alike) reads, slot by slot
  in firing order, **−22, +3, +1, +18 % of a stroke, the weak slot one
  of the high pair**. So **the weak cylinder of August was 2 or 3 and
  not 1 or 4**, on the wheel alone. Between the two the wheel cannot
  choose: as **3** the pattern is 1 +18, 3 −22, 4 +3, 2 +1 — the one
  of `24`–`31` on the new injectors (1 +6 to +13, 3 −11 to −18, 4 −7 to
  +1, 2 +1 to +13); as **2** it is 2 −22, 1 +3, 3 +1, 4 +18, and the
  change of injectors would have had to mend 2, break 3 by the same
  depth and exchange 1 and 4 on one day (*reasoned*: unlikely, not
  excluded). ⚠ One capture, some ten seconds of idle; the short stops
  later in it pooled with the first read the same way round (−17, 0,
  +4, +14, 730 strokes). By the deviation the strongest there is 1,
  not 2, as in several captures since; the rule takes the strongest
  slot of the raw steps, wheel in, and it took 2's.
- **What it changes**: `41`, cold, is not "all four alike" — 3 has
  56 % of its weak strokes and 36 of 014's 49 rises; `40` to `47` put
  58–73 % of the weak strokes on 3 where the dips' shares read 41–48 %;
  the old pattern in per cent of a stroke carried the wheel (4 too low,
  3 too high by about 5 % of a stroke each, 2 too high and 1 too low
  likewise). The rest is in the table below.


### Off idle — the count through a whole drive, and what the cylinders give under load

*12/11 night, at the owner's questions after the third research;
`tools/drivescan.py`, kept, and `tools/test_drivescan.py`. Sixteen
drives, `19`–`50`; warm (oil 80 °C and over).*

- **The ceiling of about 2,800 rpm was the method's, not the bus's.**
  `cylscan.track()` corrects its phase by *when* 0x280's value changes;
  0x280 comes every 10.65 ms, so from about 2,820 rpm a stroke is
  shorter than a frame and the moment of a change says nothing. One
  count from one standing idle to the next held in **38 of 38** drives
  that stayed under about 2,850 rpm and slipped in **16 of 28** above
  3,000 (by one or two strokes; moving off, gear changes, queues and
  the overrun were never the problem — speed was). **What a frame
  *reads* still names its stroke**: the crank wheel's alternation (2
  and 3 high, 1 and 4 low) grows with engine speed — 6 rpm between
  neighbours at 3,000, some 25 at 5,000 — so every frame says whether
  its stroke is an even or an odd one. `drivescan.track_drive()` lets
  the integral of engine speed carry the count, corrects it by the
  timing below 2,600 rpm and by that parity above, and learns the
  parity's sign where both work. **Cylinder 2 is on the same slot at
  every named standing idle of every engine run: 124 idles in sixteen
  captures, to 6,440 rpm, none slipped** (`--count`); in `35`, which
  has too little above 1,900 rpm to learn the sign, the count is
  restarted past 2,850 rpm instead of trusted. And the sign learned
  under load agreed with the idle's name in 16 of 16: **the pair that
  reads high at 2,000–2,500 rpm is the pair of the idle's strongest
  cylinder**, the wheel's.
- **What can be read off idle: two differences.** On the overrun, with
  nothing burning, the alternation left after `cylscan.WHEEL_ALT` is
  nothing up to about 2,400 rpm and then grows — 0.04 % of engine
  speed at 2,600, 0.13 % at 3,800, 0.27 % at 5,000 (13 rpm) — so the
  wheel is not one number at speed, and the pair 2 and 3 against the
  pair 1 and 4 is not read above 2,400. **3 less 2 and 1 less 4 carry
  none of it** (the wheel moves each pair alike): on the overrun they
  read −0.04 to −0.5 and +0.03 to +0.25 rpm in every band to 5,200
  (5,700 windows of 40 strokes), which is the floor of what follows.
- **The scale.** A whole stroke is 34 rpm of step at idle
  (`cylscan.STROKE_RPM`); the same work lifts a faster crank less and
  a loaded cylinder does more of it, so off idle it is taken as
  `34 × (b7 / 25) × (800 / rpm)` — 60 rpm at 2,950 rpm and b7 160, 42
  at 4,700 and 180. **A decision, good to about a quarter**: b7 is the
  ECU's model (at idle it reads 26–29 with the friction byte at 21),
  and the crank inertia that standing revs give (0.2–0.3 kg m² by b7
  less b6) is the idle figure's only to that. Every per cent of a
  stroke below carries it; the rpm of step do not.
- **A. The idle's pattern off idle: 3's deficit fades with load, 4's
  does not.** Per cent of a stroke, `19`–`37` | `39`–`50`:

  | | b7 | **3 less 2** | **1 less 4** |
  |---|---|---|---|
  | standing idle | 26 | −25.8 \| −20.6 | +10.2 \| +5.0 |
  | moving, to 1,150 rpm, the pedal light | 27 | −20.5 \| −23.9 | +8.5 \| +6.7 |
  | the same, pulling (moving off, a crawl uphill) | 57 | −8.6 \| −8.9 | +6.1 \| +2.9 |
  | 1,150–1,600, light | 20 | −22.1 \| −25.4 | +12.5 \| +6.8 |
  | 1,150–1,600, part load | 62 | −3.3 \| −4.8 | +1.9 \| +0.9 |
  | 1,600–2,600, part load | 62 | −1.8 to −4.0 \| −2.2 to −3.6 | +2.6 to +3.5 \| +2.6 to +2.7 |
  | 1,600–2,600, b7 90–140 | 105 | −1.5 to −2.0 \| −0.9 to −2.3 | +2.2 to +2.5 \| +1.5 to +2.2 |
  | 2,100–3,300, b7 140 and over | 160 | −1.8 to −1.9 \| −1.1 to −1.3 | +1.8 to +2.1 \| +1.2 to +2.5 |
  | 3,300–4,200, the same | 175 | −2.1 \| −1.6 | +3.2 \| +2.6 |
  | 4,200–5,200, the same | 185 | −0.3 \| −3.0 | +4.4 \| +3.8 |

  (errors ±0.2 to ±0.7 under load, ±1 at the top in `19`–`37`; the
  light-pedal bands above 1,600 rpm read −6 to −15 and +5 to +13, on a
  scale of 10–15 rpm with a noise of a quarter to a half of a stroke —
  not to be leaned on.) **Cylinder 3 is the idle's and the light
  pedal's**: a fifth to a quarter of a stroke under 2 standing,
  crawling and to 1,600 rpm with the pedal light; **under 9 % as soon
  as the engine pulls at idle speed, 2–5 % at part load, 1–3 % at
  full**, at every speed to 5,200 and in both periods. In rpm of step
  it goes from −7 to −8 at idle to −0.4 to −1.5 under load; as work
  (step × speed) from the idle's to a quarter to a half of it through
  the middle. **So it is not a share of the charge that 3 loses** — a
  cylinder short of compression or of fuel in proportion would stay a
  fifth short — **and load at the same speed lifts it** (idle speed,
  b7 27 → 57: −24 → −9 %), which a leak past a seat, set by time and
  pressure, would not do. *Load helps*, measured. **Cylinder 4 is the
  other way round**: 2–4 % under 1 from 1,600 rpm up at every load
  from part to full, in both periods, growing a little to the top
  (+0.8 to +2.1 rpm of step at full load against the overrun's +0.03
  to +0.25) — **a share, not an amount** (S4).
- **B. What weak strokes cost at full throttle: nothing that shows,
  and the standing difference about 1–2 %.** `--weak`: every stroke's
  step against its neighbours, 100,000 strokes at b7 140 and over.
  Noise is as often over as under; a misfire is only ever under. The
  noise there is 3–5 % of a stroke (2 rpm against a stroke's 45–70),
  so half a stroke lost would stand out twenty-fold: **strokes a half
  under 0.1–6 per 1,000, a half over 0.7–6 per 1,000** in every band
  (most of both are gear changes and the pedal coming on inside a
  window); **the excess under is −0.1 to −0.8 % of the work — none**.
  At part load the same (±0.2 % in every band of 10,000 strokes and
  more; the one small band that stands out — `19`–`37`, 2,820–4,200
  rpm at b7 90–140, 72 strokes of 4,456 a half under against 10 over —
  is bursts inside single seconds on all four cylinders, the driveline
  at a gear change or the pedal lifting, not a cylinder). At a standing idle the same measure
  reads +0.4 to +0.5 %: 17–27 strokes per 1,000 a quarter under
  against 8–14 over. **So at full throttle no stroke misfires or
  half-fires, on any cylinder**, to within about 0.3 % of the power.
  What is there is the standing difference: if 3 gave what 2 gives and
  4 what 1 gives, the engine would give (1 to 3 + 2 to 4) / 4 =
  **about 1–2 % more**, on the scale above. *What all four might lack
  alike cannot be seen this way* — D.
- **C. Against 014** (`--vcds`, 24 driving logs beside their captures;
  the pick's control 5 s before and after each rise, S3, *Against
  chance*): **moving at up to 1,200 rpm** — crawling, moving off —
  **014 counts what it counts standing**: since the VW leads 24 of 36
  rises on 3 (67 %, the control 36 %), 4 22 %, 1 and 2 6 % each; up to
  18/10 3 and 4 alike (17 and 16 of 38), as at the idles then.
  **Above 1,200 rpm it hardly counts**: 59 rises in all the logs, 20
  of them with the engine pulling (b7 45 and over), **one above
  2,820 rpm**. The 20 are real — the stroke before them 40–57 % of a
  stroke down, the control's 16–18 % — and they are nobody's: 8 on 1,
  7 on 3, 2 on 4, 3 on 2. So the ECU's count and the bus agree off
  idle too: next to no misfire under load. (*The session before's "smears
  onto 1 above 1,200 rpm" was 82 rises on a cruder measure; with the
  scale and the count above it is 4 of 9 since the leads — too few to
  name.*)
- **D. Whether b7's maxima are a healthy engine's** (`--pulls`). b7
  cannot say: it is the ECU's model from air and spark, and its scale
  here was *set* so that the full-throttle plateau reads the rated
  torque (`docs/firmware/frames.md`, *The scale*). **The car's own
  acceleration can**: 76 full-throttle pulls in 3rd and 4th, each
  second's acceleration turned into crank torque against b7 less the
  drag line × 1.06. **The car's mass is the registration
  certificate's, 1,303 kg in running order** (*the owner's photograph*,
  12/11 night; by the EU's definition with a 75 kg driver and the tank
  nine tenths full; *1,400 kg was assumed until then, and read 1.00*);
  the rest is assumed, none read off this car — CdA 0.84 m², rolling
  0.012, driveline 0.92. **The median pull needs 0.95 of what b7
  claims, half of them 0.89–1.04** (the spread is the road's slope; by
  capture 0.82–1.15); band by band 147–156 Nm at 2,000–5,000 rpm,
  130–137 at 5,000–6,000. Every 50 kg the car carries over the
  certificate (a heavier driver, the laptop, the boot) is 3.5 % more,
  and the assumed resistances are worth some 5 % either way. **So the
  engine gives its rated torque to within a tenth, and nearer a
  twentieth under than over; a fifth missing would show.** With B:
  nothing found that a healthy AQY would do better at full throttle
  beyond the 1–2 % of 3 and 4 — a few per cent common to all four is
  neither shown nor excluded. *What would tighten it*: the car on a
  weighbridge as driven, and a pull each way on the same stretch.
- **E. Over time, capture by capture** (*the owner's question*, 18/11:
  the car feels better at high revs than in the summer; `drivescan.py`
  default and `--weak` on every capture with pulls, `19`–`54`; group
  003 at full throttle in every VCDS log): **nothing moves from 24/9 to
  17/11.** 3 less 2 at b7 140 and over −4 to +1.5 % of a stroke in
  every capture and band but one (`37`, above 4,200 rpm, +5 ± 1.6),
  `19` (24/9) −1.4 to −2.8, `54` (17/11) −2.7 to −3.7; 1 less 4 +1 to +3, a few +5 to +10 above 3,300 rpm on
  windows of ±1–2; the excess of weak strokes at full load −0.8 to
  +0.03 % of the work in every capture — none; `--pulls` 0.82–1.15 by
  capture with no trend (`19` 1.04, `54` 0.99); **the air at full
  throttle 495–528 mg a stroke at 4,000–5,000 rpm** in the 003 logs
  from 24/9 (the new MAF) to 17/11, 85–93 g/s at the top (two short
  logs lower, 3/11 `step5b-pull` and 9/11 `step8-home-2`, 441–444). **What
  cannot be read is the summer**: the first pull on the bus is `19`
  (24/9), after the blocked converter (10/9), the plugs (17/9) and the
  injectors (23/9), and August's 002/003 logs (`vcds-01`, `vcds-ride`,
  the old MAF) hold no full throttle. So the owner's feeling and the
  record agree as far as the record goes: whatever came back at high
  revs came back before 24/9 — the converter the likeliest by size
  (*reasoned*) — and nothing since has moved it either way.
- **What it bears on** (*reasoned*; **no fit-table symbol changes**;
  **the ranking: H4 above H20, agreed with the owner the same night**,
  *The idle's candidates, ranked*): **H3** (a leak at
  runner 3) and **H18** (oil at idle vacuum) predict exactly this
  fading with manifold pressure; **H7**'s one-injector form fits if
  the injector is short only at its smallest quantities, not if it is
  short by a share; **H1** (a seat on 3) fits the fading with speed
  but not the lift by load at idle speed — unless the seat acts by
  dilution, an exhaust seat that lets burnt gas back at the idle's
  vacuum, rather than by lost compression, which 12 bar on all four
  already spoke against; **H4**'s weak spark on 3 is
  against — the spark is hardest to make at full charge, where 3 is
  within 1–3 % of 2 — **and its injector branch gains the most**: an
  injector that opens late loses the same fuel at every injection, a
  large share of the idle's and next to none of full load's, which is
  the shape measured, where "a steady 9 % in every state" had been
  held against it; **H13** stays as it was (a flake on a seat acts
  like H1's leak; a crust that dilutes the idle's small charge fades
  with load). Cylinder 4's 2–4 % is S4's to carry.
  **List A is not read by any of this** (*the owner's question*, 12/11
  night): the timing belt, H0 and the rest of the common part act on
  all four alike, which a comparison between cylinders cannot see.
  D alone touches the belt, weakly against (no tilt of the full-load
  torque from low speed to high; the row A2, A1 until 17/11).

### What the dip shares said, and what stands

From 9/10 to 11/11 the cylinders were named by **the share of the dips
on each firing slot** — `cutscan.py --shares`, `--name` and `--pairs`,
`dipshape.py --name`, and on 9–10/11 an ad-hoc naming by the strongest
slot on the same count. **Removed 12/11 at the owner's decision**: the
count slipped and the crank wheel's alternation was left in (*The
count that does not slip*, above). Their tables, capture by capture,
are in git (`git show 296a5d7:docs/engine-health/open.md`, the
subsections *One cylinder or two* and *The dips keep to one slot*);
nothing here rests on them. What they concluded, against `cylscan.py`
(S1, *Every stroke named*; warm unless said):

| read with the dip shares | by `cylscan.py`, 12/11 |
|---|---|
| two thirds of the dips on two neighbours, **4 first, then 3** (`31` named by its cuts; `09`–`38` pooled) | **3 alone**: `31` 3 −15 %, 54 % of the weak strokes; 4 −3 % |
| **all four alike after the VW leads** (`40` 58 %, p 0.77; `41` cold, named, 31 % on 3) | 3 −14 % with 64 % on `40`; 56 % on `41` cold |
| one slot again on the original map (`42` 45 %); `43` named, **43 % on 3** | 3 −10 to −18 % with 58 % on `42`, −13 % with 62 % on `43` |
| `44` 48 % on 3 before the clean, **`46` all four alike after it** (p 0.01) | 58 % → 38 %, 4's weak strokes as many as 3's at stop 7; **3's deficit −11 % → −10 %**, its floor kept |
| `47` 3 leads again, 41 % | 73 %, the swell back |
| a steady pattern, **3 and 4 weak, 2 strong** | **3 weak, 4 level warm since October**, 2 and 1 strong; 1.7 rpm of the old pattern is the wheel |
| before 24/9: 4 and 3 weak, cold 4 most (`18`) | `09` 3 −19 %, `12` −11 %, `17` −23 %; `18` cold 4 −14 %, 3 −5 % |

**So the one conclusion that changed is the pair**: there was never a
second weak cylinder warm since early October, and never "all four
alike" — every reading that used one (H3 runner 4, H4 the loom at 3
and 4, H15's ends on 3 and 4, the 24/10 demotions for "the dips no
longer keep to 3 and 4") is re-read in its own entry.

**What stands unchanged: P0303 at `43`'s cut** (3/11 evening; the
dips in the cut named at the cut's own phase, where the dead slot
holds the count and nothing slips). 3 dipped on its own in the cut, 5
of the 7 dips there and none on 2 — 5 in about 375 of its strokes,
twice its rate outside, but 1.3 %, under the 2 % VW sets for a code
(`vcds.md`). **Where it came from** (3/11, at the owner's question):
the last read before it was empty, at the start of the warm VCDS run
(17:19, VCDS clock), after the pulls; between it and the cut came 16
minutes of driving with full-throttle runs to 6,258 rpm (the capture,
17:20–17:24) with **014 at 0 through them and to 17:28**, then 12–24 at
the town stops and the crawling between them, and the warm stop's idle
counts — counts like these never stored a code in any session before.
So it came with the cut, not with hard driving. **Not the ECU charging
4's misses to its neighbour by habit**: the same cut on 4 twice on
10/10 (warm) and once on 24/10 (cold) stored no P0303 (`idle-log.md`).
*Reasoned*: with 4 dead the total ran far over 2 %, and in that window
the ECU named the cylinders it had counted, 3 among them — real
misfires on 3, named because 4's pushed the window over; on its own 3
would not have set it. The lamp at the cut is 4's. **This ECU stores
no freeze frame** (*owner*, 3/11), so the fault memory holds only the
codes and their status. *On 12/11 and on 16/11 P0303 was stored
without any cut* (S3).

**After every captured session** each cylinder's deficit, weak strokes
and 014's rises are reported to the owner from `tools/cylscan.py`
(`CLAUDE.md`).

---

## What the forums say about this idle

Searched 27/9, 9/10 and 20/10, in German, Polish, Czech and English (forums
and search extracts; leads, not sources). **The finding is the pattern:
almost nobody reports a fix.** Every AQY thread with this picture that could
be read to its end stops unresolved after the same parts list this car has
been through. What was reported as fixed: a new battery, a new Bosch coil, a
new lambda probe, **original VW leads instead of aftermarket ones**, rings
and a head going-over, a sticking bucket tappet, the timing belt a tooth out.
Most of these are already done here; the belt's marks were read 13/11
(not settled; the full-throttle air against 30–60°, the row A2) and the belt is to be renewed (`plan.md` 8q).

**A remap that made the idle worse** (searched 28/10 at the owner's
request, Czech and English): **no AQY, 2.0 8v or Motronic M5.9.2 case
found**, and no thread where going back to the stock map was the fix on
such an engine. What there is, all general and none a source: Czech
tuners' own pages say a poorly made map can give an uneven idle
(raziteam.cz, radyprovsechny.cz); a flash clears the adaptations, so the
idle can read worse for a few drives until they relearn
(nefariousmotorsports, "Rough idle after remap"); and **HP Tuners'
material on MAF scaling says a scaling error shows most at idle, where
the flow is lowest** — the mechanism H19 rests on — with owners of tuned
cars reporting idle trouble after a MAF of a different make, gone with
the original. **The owner's recollection** (28/10, uncertain, nearly ten
years back): the tuner may have warned that the idle could get worse.

**P0172 and a negative idle trim on this engine** (searched 25/10, the
same languages): **no AQY thread with a reported fix.** The general
lists agree with VW's (`vcds.md`, block 032): a leaking injector, fuel
pressure too high, a purge valve stuck open, the MAF, the probe, **and
fuel in the oil** — Mazda SA-026/18 and GM PIP5647A, both for
direct-injection engines and both with the oil level rising (`refuted.md` C21). New Beetle forum leads, unread to their end (the
pages refuse automated reading): the short vacuum hose to the fuel
pressure regulator, N80. Overfilling the tank past the first click is
named as a way to flood the canister (*general*; H16).

**The idle air regulation, 055 and P1582** (searched 26/10, English and
German, for H8): **no source gives typical values of 055's learnt value
on this engine, and none relates it to 014** — the one specification is
still VW's own, −1.50 to +1.50 g/s and negative on a run-in engine
(`vcds.md`), which every reading here except the stick's has kept inside.
A German overview gives 055 in per cent for other ECUs, so the g/s scale
is this ECU's label file and not general. **P1582 on an AQY**, in one
motor-talk thread read only in search extracts: a cracked vacuum hose to
the brake servo, unmetered air, with the additive lambda learnt value
high (the opposite sign of this car's 032), cured with the hose and the
adaptations reset. The general P1582 lists name air leaks, the injectors,
the fuel pressure regulator, the throttle and oil dilution. Throttle
cleaning and a relearn are the usual advice; one AQY extract says the
stutter got *worse* after a relearn. **One more AQY thread with this
picture** (golf4.de, 2012, read in full): a warm idle that stutters now
and then, dipping from 800 to 760 rpm only in the stutter, driving fine,
the probe, plugs, leads, coil, coolant sender and MAF replaced and the
throttle cleaned and adapted — **unresolved**, like the rest.

**Pictures of the inside of this engine family** (searched 21/10, the same
languages): **none found** that would compare — no borescope or head-off
photo set of an AQY, AEG, APK or AZJ with its mileage. The one general
reading that bears on it is ExxonMobil's borescope guide for gas engines
(*A Basic Guide to Borescopic Inspection*, §3): some crown deposit is
normal and *"should be evenly distributed. Uneven deposit distribution is a
sign for non-homogeneous thermal dissipation"* — the amount on this
engine is not judged against anything, its **unevenness, 3 > 4 > 2 > 1**,
is the finding (H13).

**Searched again 4/11** (DE, PL, CZ, EN; VW's manual as transcribed,
Ross-Tech; the notes are not kept here): **still no AQY/AEG thread with a
confirmed fix for an idle-only misfire on one cylinder**; the confirmed
idle-only cylinder-3 fixes on other engines were all at the valve (lash,
a burnt valve, a broken spring; *forum leads*). **VW, read**: compression
new 10–13 bar, wear limit 7.5, **largest difference 3 bar** — so 12 even
excludes only a gross loss (`refuted.md` A4); 014 is the total only,
specified 0–5 at 740–820 rpm and 15–35 % load, with no per-cylinder
group; **misfires from an ignition output are stored in pairs** (1+4,
2+3), which no code on this car has done, so neither the coil nor its
output stage; **P1300 / 17708 is a misfire put down to an empty tank**,
so captures run above reserve; P1237–P1240 are injectors N30–N33. **Not
found**: an AQY TSB on the idle, a crank-wheel adaptation procedure.
**A generic OBD-II read** (VCDS's OBD-II mode, read only) after a stored
P030x may show mode 02's freeze frame or mode 06's misfire results
though the VW view shows none; whether M5.9.2 supports either is not
known. **The photos read again** (the same 37): 3 the only crown whose
layer has broken into sharp-edged islands (flaking), a raised rim on its
exhaust valve face; no burnt margin, no steam-clean crown, no oil-wet
deposit anywhere; 4's crown-line mark undecided (a deposit edge or a
crack) — one frame of it again whenever the borescope goes in.

**Hydrogen decarbonisation, searched 4/11 evening** (*the owner's
request*; EN, DE, PL, CZ; H13, `plan.md` 8). **What the machines make**:
water split by electrolysis into hydrogen and oxygen, 2 : 1, fed to the
intake — from about 280 l/h (a German workshop's figures, about 0.8 % of
hydrogen in the intake air) to 30 l/min, about 1 kg an hour. **The
vendors' chemistry does not hold** (*general*, *reasoned*): hydrogen
taking up the carbon as methane (C + 2H₂ → CH₄) needs a catalyst, a
hydrogen pressure of tens of bar and minutes of contact, where the
cylinder offers a hundredth of a bar for milliseconds, and at flame
temperature the equilibrium runs the other way; the water-gas reaction
(C + H₂O → CO + H₂) needs the carbon at about 600 °C and more, which the
workshop itself gives as its limit, against a chamber wall of a few
hundred. **What can act**: hydrogen's flame burns closer to the walls
than petrol's, and its water may flake deposit (SAE 2000-01-2858); the
carbon that does leave goes as CO₂ and CO, as from any burning, and
the ash of the oil's additives, which the deposits carry, does not burn
at all — it can leave only as flakes. **Independent evidence**: one
study (Sci. Rep. 2026, s41598-026-54105-y): a 2001 Škoda Fabia 1.4,
about 1 kg of HHO in an hour, idle alternating with 3,000 rpm — **no
change** in power, fuel per kWh (287.2 → 287.0 g/kWh), cranking current or
the idle's HC; deposits not measured. It cites one diesel tractor whose
exhaust valve's carbon cover went from 65 to 15 % (not read). No ADAC or
magazine test found; Polish owners split, some mechanics against it on
engines over 20 years old (a seal may start to leak); the rest is the
sellers'. **Read for this car** (*reasoned*): the hours above 4000 rpm
on the 44K tanks heated the chambers more than an hour at 2,000 rpm
without load and moved nothing, so what the clean adds is hydrogen's
flame at the wall and the water — expected small, cheap to try, and
still the one repair that reaches 3's crown without the head off.
**Done 9/11** (an 800 l/h machine at about 60 %, about 8 l a minute of
the mixture): 3's excess gone at the stop after it, 4's and the settled
level kept (S1, *The clean of 9/11*) — not "no change", one stop each
side. **At idle the gas itself made the idle the calmest on record**,
which the study's idle HC could not show.

**Searched again 11/11** (*the owner's request*, the second deep
research; DE, PL, EN, Czech not reached; manufacturers' and SAE pages
read as abstracts, forums as leads; the notes are not kept here).
**Still no AQY/AEG/AZJ/APK/AVH/AZG case of an idle-only misfire on one
cylinder with a confirmed fix**; the one family case with a confirmed
cause is an AEG timing belt a tooth out, and it stored a code. What is
new:
- **Deposit flakes on the exhaust seat** (Shell, SAE 2000-01-2858,
  2002-01-2833, 2003-01-3187): trapped by chance, a leak that switches
  on sharply once enough deposit is lost (about 55 µm), **water the
  strongest trigger of flaking**, harder driving less of it. No source
  gives how fast seat deposit forms again; the one time base found is
  about 200 hours for inlet-valve deposit on a port-injected engine
  (SAE 922263) — so **a day's relief fits a flake moved, not deposit
  regrown** (H13, H1).
- **The tappets** (VW's procedure for the 2-valve 2.0, read from its
  SEAT and Škoda pages): **"irregular valve noise on starting is
  normal"** — the clatter of 8/11 at −2.5 °C is VW's normal. The check:
  the fan in once, 2,500 rpm for 2 minutes, the cover off with the cam
  up, more than 0.2 mm of play renewed, else the tappet pressed with a
  plastic wedge and a 0.2 mm feeler tried. It finds a soft tappet, not
  one stuck pumped up, which only a leak-down or a warm compression
  shows (H1).
- **The timing belt**: VW's fault table has **16725 / P0341, G40
  implausible signal**, and Ross-Tech names a misaligned timing among
  its causes; an AEG forum case with a tooth off set P0340/P0341. So an
  empty fault memory is weak evidence against, not proof: whether this
  M5.9.2 runs the check is not confirmed. **Read again 13/11**
  (*the owner's questions*: could 30° be misjudged, which way a belt
  slips, would an engine like this keep its power more than a tooth
  out): **Motor magazine on the 2.0 ABA, the same family** (8/2003 and
  9/2003, VW specialists interviewed): an engine with the belt one or
  two teeth off "may still run smoothly", but "will lack power, and both
  emissions and fuel economy will be terrible", and it is "very likely
  to trigger a P0341" — one shop puts nine in ten P0341 on these engines
  down to a stretched or misfitted belt. Forum reports on the ABA and
  AEG agree in kind: a tooth advanced, "lots of low end, no top end"; a
  tooth retarded, a bog at low speed; a tooth given as about 8° of cam
  (*on the AQY 6.92° of cam, 13.85° of crank: searched again 17/11,
  below*).
  **No measured case of two teeth or more was found**, on a dynamometer
  or otherwise. **The marks**: the same article names the camshaft
  sprocket's OT against the arrow on the rear cover and **the flywheel's
  mark in the gearbox window** as the marks to set; the crank pulley's
  notch is on the ABA set against a chisel mark on the intermediate
  shaft's sprocket, and forum posts on the AEG set it against a raised
  line on the lower belt cover — whether the AQY carries a mark on the
  block as well was not confirmed either way (*the owner*: the web
  shows the notch on the pulley and one on the block, as he found).
  *Answered 17/11 (below): VW's procedure for the AQY names the lower
  belt guard's mark and the flywheel's, none on the block.*
  **Which way a belt slips** (*reasoned*; the search gave anecdotes both
  ways): the crank drives, so a belt that jumps or stretches leaves the
  cam behind — retarded, the pulley's notch past its mark with the cam
  at OT; **8i read the notch short of it, the cam advanced, which a slip
  does not give — only a belt fitted so in 10/2017**, or a misread.
  So what is left is a misjudged angle (*the owner's own doubt*: the
  borescope and a finger in a cramped place) or a belt a tooth out
  since 2017; the flywheel's mark with the cam at OT would have read it
  to a few degrees with no plug out, but the owner found no window at
  the gearbox (14/11; `plan.md` 8r dropped), so the mechanic's count
  before the old belt comes off (8q) reads it. A tooth acts on all four alike
  and cannot by itself part 3 from 4. **SAE 972936** (idle, the overlap
  moved 10° later): less residual but a longer burn and *more* cyclic
  variation — the effective compression ratio, not the residual alone.
- **A leak at one runner** (trade sources): the lower gasket the usual
  cause of a one-cylinder idle misfire; its signature a trim positive at
  idle and falling with speed. This car's negative idle cell rules out a
  leak large enough to move the whole trim, not a small one at 4; at
  idle vacuum the leak is choked, a fixed flow against a charge that
  grows with load (*reasoned*), and a smoke test pushes the other way.
- **The idle's physics** (Heywood; SAE 972936; Ji and Wang, *Int. J.
  Hydrogen Energy*): residual gas, burn duration and the early flame
  kernel set the idle's cyclic variation; a higher manifold pressure
  lowers the residual (the calm under load); **hydrogen at idle halved
  COV of IMEP at 6.5 %** and moved the lean limit far — studies at 1 %
  and less were not found. A faster flame rescues borderline strokes
  but cannot supply a missing quantity of air, fuel or compression,
  which is why the gas took the dips and left the steady pattern (S1,
  *The gas idle taken apart*). Bosch's crank-speed misfire detection
  (SAE 930399) is built for full misfires; partial burns at idle are
  its hardest case, so 014 is a lower bound (S3).
- **The probes** (Bosch, Denso, SSP 175 German edition): contact spray
  forbidden on their connectors (S23); the signal earth a wire of its own
  to the ECU, so a cracked earth shifts the reading only through a
  leakage current; **the rear probe's failure leaves the front loop
  running** and could push only rich; the rear loop not documented at a
  warm idle. **VW's list for a low learnt value** puts *"low at idle,
  part load normal: possible oil dilution"* first, then a leaking
  injector, high fuel pressure, N80 stuck open and the probe — oil
  dilution was settled against on 26/10 (`refuted.md` C21). The grey-
  beige crust of the old front probe matches no chart entry cleanly:
  coolant (green-white, grainy), oil (dark), fuel additives (red or
  white) — the cleaners explain it as well as coolant does.

**Searched again 17/11** (*the owner's request*, the fourth deep
research, after H3 and injector 3 went out; DE, PL, CZ, EN; motor-talk.de,
vwvortex, golf4.de and forum.newbeetle.pl refused automated reading and
vwaudiforum.co.uk was outside the session's network, so forums are
search extracts and leads; the notes are not kept here). **Still no
healthy M5.9.2 log** of 014, 032, 055 or 001 at a warm idle, no VW or
dealer statement that this family idles unevenly by design, and no
count of P030x by cylinder that singles out 3 (H0). What is new:
- **VW's own belt procedure for this engine** (Škoda's Octavia Mk1
  workshop manual, *2.0 ltr./85 kW engine*, engine codes AEG, APK, AQY,
  AZH and AZJ, the AQY there with M5.9.2, 10.5 : 1 and no cam
  adjustment; its text and drawings A15-0024 and S13-0164 read on
  workshop-manuals.com — the New Beetle's own edition not read). Three
  references at TDC of cylinder 1: **the cam sprocket's mark against
  the cylinder-head cover's** (the camshaft chapter: the arrow on the
  belt guard), **the vibration damper's mark against the mark on the
  bottom part of the belt guard**, at the top of the damper in the
  drawing, and **the flywheel's TDC mark in the gearbox's window**,
  checked before the belt comes off and again after it is on. **No mark
  on the block anywhere.** The damper, the crank sprocket and the
  flywheel fit one way only (holes offset), the cam sprocket sits on a
  Woodruff key — so **a pulley bolted on turned is excluded by design**;
  what can move the damper's notch alone is its outer ring slipped on
  the rubber (a newbeetle.org lead) or a damper that is not the
  original. **The window on the 02J** (forum leads): on top of the bell
  housing under a rubber plug about 25 mm across (02A 301 115 A), often
  under hoses or the air box.
- **A tooth is 13.85° of crank**: the cam sprocket has 52 teeth (Topran
  118 512 / 06A 109 105 D, listed for the AQY and AZJ by parts sellers;
  about 52 counted on VW's drawing), so the crank sprocket 26 and the
  belt 06A 109 119 C 138 (Gates' listing, 1,104 mm). 8i's 30–60° by eye
  is 2.2–4.3 teeth, its 2–5 cm along a rim of 14–16 cm (the diameter
  a guess) 1.0–3.0; with the cam's mark set the error is a whole number
  of teeth, so **the two readings meet only at two** (27.7°), which the
  full-throttle air, the acceleration and the empty fault memory argue
  against (*reasoned*; the row A2).
- **The ECU compares the cam's phase with the crank's**: VW's fault
  table for the family lists **16724 / P0340 and 17748 / P1340,
  "Camshaft position/crankshaft position sensor – Incorrect
  assignment"**, beside 16725 / P0341 (Ross-Tech names a misfitted belt
  for 17748); the table covers M5.9.2 and ME7.5 together and gives no
  tolerance, and VW's list of measuring blocks has no phase. *SSP 175's
  "G40 only identifies cylinder 1" (the row A2) did not say the ECU
  never compares them.* An empty memory weighs more against two teeth
  than against one (*reasoned*).
- **What a tooth does at idle**, the direction only (Ford's work on cam
  timing, Jankovic and Magner, IFAC 2002): retarded, more residual at
  low load, a worse idle and a higher manifold pressure for the same
  air; advanced, exhaust back into the inlet and more charge trapped at
  low speed. **No measured idle figure for a whole cam moved 14° or 28°
  on a fixed-cam 2-valve engine.** The idle control would show a
  changed trapped volume as air — the throttle, the manifold's vacuum,
  055 — not in 032, since the fuel follows the MAF (*reasoned*).
- **The head's modes** (INA, *Valve Train Components*, failure
  diagnosis): "the exhaust valve sucks in exhaust gas" through a seat
  that closes improperly "when the engine is warm" — H1's dilution form,
  driven by the idle's vacuum and so an amount that fades with load; a
  hydraulic element pumped up sinks over minutes (2–10 min at ambient)
  after a sudden onset, **the mirror of 3's swell** (H1's lifter form,
  against). Valve rotation small even at speed and falling with hotter
  oil (Jelenschi, 2012), none on one bucket-tappet rig at about 600
  engine rpm (Al-Jeboori, 2018): a spot on a seat may stay where it is
  at a hot idle (*reasoned*).
- **A maker's case of one leaking seat**: Mercedes LI01.30-P-072328
  (2/2026, M260/M264): rough running, per-cylinder mixture codes
  ("cylinder 3 is irregular" among them), and "it is possible that no
  fault codes are stored"; the gate is a cylinder leakage test naming
  inlet or exhaust, then a new head. **GM PIP5029F**: diagnosis may miss
  sticking valves "depending on whether the intake/exhaust valves are
  sticking at the time of the diagnosis" — item 9's switch-off in a
  swell. GM's cleaner procedure (PIP5029F, 16-NA-383: cleaner drawn in
  warm at about 2,000 rpm, a hot soak of 2.5–3 h, repeated if improved;
  too much at low speed can hydrolock) is the one documented aim at
  valve carbon short of the head; no maker gives a recovery rate. *The
  Kia/Hyundai TSB 23-EM-007H quoted in H1 aims at the ring grooves and
  oil consumption, not the seats.*
- **One cylinder's deposit setting the whole engine's trim**: CARB's
  staff report for the 2006 OBD II amendments (pp. 17–19) — intake valve
  deposits on one cylinder gave it an EGR effect and made it rich, the
  front sensor was "oversensitive to the malfunctioning cylinder", the
  loop leaned all four, and the rear sensor read lean throughout. The
  mechanism is in patents (hydrogen from a rich cylinder reaches the
  probe's electrode faster than oxygen: US 8,600,647, WO 96/35048,
  US 5,492,612). **Its size here is small** (*reasoned*, a model not
  kept): one cylinder 15–20 % short of fresh air at the same fuel moves
  the loop by about −2 to −3.5 %, a slow but complete burn by under 1 %
  — a point or two of 032's idle cell, not −6 to −9 % (S19); and the
  loop does not move with the swell (S1).
- **S19's return, re-reckoned** (*reasoned*; the pump's delivery not
  read): a return system's pump delivers an order more than the engine
  burns at idle or at part load, so a restriction in the return or a
  high base pressure raises the rail nearly alike at both and would pull
  **both cells negative**, not −7 / +7. And how M5.9.2 combines the
  additive idle cell with the multiplicative part-load factor at idle
  is not documented; if both act there, the net learnt correction at
  idle is near zero (S19).
- **Tests that read the cylinder with the head on** (Pico's guided
  tests; Bernie Thompson's rules on diag.net; Motor magazine 7/1999,
  1/2005, 2/2007): **an in-cylinder pressure transducer** (WPS500X) in
  plug 3 with the engine running on three — the expansion pocket and
  the exhaust ramp read 3's sealing unfired, the ramps the cam's timing
  ("a 1-tooth exhaust cam error is hard to see during cranking… check
  the idle exhaust plateau ramps"; Motor read a tooth as 21.5° on
  another engine), best the same reading before and after the belt;
  **an injector's voltage and current, 3 against 2, warm and running**
  — a resistance fault delays the opening (one case 1.9 ms, "one-third
  the fuel"), a MOSFET switch drops 0.2–0.3 V, and an output stage of
  the TLE6220 kind diagnoses open load, a short and overload, not a
  raised resistance (that M5.9.2 carries it is not confirmed);
  **secondary ignition per lead** — a high, short spark line lean or
  diluted, low kV with hash a leaking valve, each power spark against
  its own waste spark; **G28 and G40 on two channels** before and after
  the belt. The CO₂ test may miss a small weep and tests the other
  direction; the cooling system held at the cap's pressure for hours and
  the borescope in 3 read a weep better (a lead). In the Czech Republic
  Bosch Car Service's FSA carries the ignition scope, the secondary
  pickups and a leak-down tester (EFAW 210 A); no workshop was found
  offering the running in-cylinder test, so it is asked for by name.
- **One AQY lead with 3's shape** (vwaudiforum.co.uk, a search extract
  only): P0303 and P0300 at idle in traffic, 3 missing under about
  800 rpm and never above, from about six months after a coolant
  stop-leak and a new radiator; unresolved (H20). None was ever
  put in by the owner (*owner*, 17/11).

---

## The idle's candidates, ranked

**A judgement, not a measurement**, for S1, S2, S3 and S14. **Mirrored in
Czech on the owner's private page *Pořadí hypotéz volnoběhu***, republished
with every change here (`CLAUDE.md`, the currency pass). Re-read after
every test and whenever the symptom list changes. **Each cell says why the
hypothesis stands where it does now and what is left to settle it**; how
it got there — every re-read and every move up or down, 14/10–15/11 — is
in git (`git show 1780e07:docs/engine-health/open.md`, this section; the
re-reads before 12/11, `git show 296a5d7:docs/engine-health/open.md`).

**Two lists since 12/11** (*the owner's decision*, the lists proposed by
Claude): the idle is two things on top of each other, measured apart
(*Where it stands*). **Cylinder 3's part** — its steady deficit, its
swells and 014's misfires — is about a third of `IdleHealth`; **the
crank wheel's own alternation** is about an eighth more, not
combustion; **the rest, a little over half, is the common part**, with
no pattern over the cylinders (S1, *What `IdleHealth` is made of*). A hypothesis goes in the list whose part it can make; H7 had
a form in each until 17/11. List B before list A (*agreed with the
owner*, 12/11): S3 and the grade's swings are B's.

**Re-read 17/11** (*agreed with the owner*; S1, *The first stop on the
new gasket*): the lower gasket renewed and injectors 2 and 3 swapped,
and 3's deficit, floor and swell as before — **H3 (B3) and H7's
injector 3 (B6) leave list B** (`refuted.md` C28, C29). What is left
of B is what stays with the cylinder's head: the seat and its deposit,
the stems, coolant, the injector's wire past the connector. **List A
loses H16** (A9, the purge path; `refuted.md` C30, *the owner*, 17/11);
its belt is read against `54`'s stop.
**Re-ranked 17/11 evening, the fourth research** (*agreed with the
owner*, the order proposed by Claude): B — **H1 above H13**, the seat's
dilution form the one reading that fits the spark, the swell's survival
of a warm engine-off and a maker's case of one seat with no code, the
deposit read as what holds it off; A — **H0 above the belt**, the marks
read against no VW reference, and **H11 above H7**, the return's form
weakened (S19).

**B. One cylinder — what makes 3 worse than the rest:**

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| B1 | **H1** a seat or lifter on 3 | The swell's best fit: **a seat on 3 that fouls at idle and burns itself clean** (with H13; S1, *The swell's shape*), diluting at the idle's vacuum rather than losing compression — 3 is within 1–3 % of 2 at full load (*Off idle*); the port photos show crust broken round 3's inlet seat (*the owner's reading*, 7/11). Against the lifter: no once-per-cycle tick at 3's place on the cam cover (15/11) and S22's tick at its usual size (12/11); a seat that leaks need not tick. **17/11**: with the joint and the injector cleared, the first of B. **17/11, the fourth research**: for the dilution form — 3 gains more from the governor's spark (a later burn), the swell survives a warm engine-off, INA's warm exhaust seat that "sucks in exhaust gas", Mercedes' one leaking seat with no code; against the lifter, whose pump-up runs the swell's course backwards (INA); against in part, the cold fast idle levels 3 within a minute | item 9: the warm leak-down with 3 twice, the engine switched off in a swell; the stethoscope above 3, hot; VW's tappet check (`plan.md` 9) |
| B2 | **H13** deposits | Fits 3 by every measure: the borescope's most deposit on 3 (3 > 4 > 2 > 1), cold 4 weak beside it in that order; the clean of 9/11 took 3's swell for a day and left its floor, which a flake moved fits better than deposit regrown (SAE 2000-01-2858). Against: no cleaner and not the hydrogen moved 3's swell or the grade's mean (S1, *Before and after each repair*); the deposit reads as a consequence as much as a cause. **Where it came from, perhaps** (16/11): the original cover gasket leaked onto the lower joint at 3 and 4 for at least ten years (*owner*), the order of the deposit (`refuted.md` C28, *Oil soaked into the joint*); **17/11**: the joint renewed and the swell as before, as a deposit laid by that oil would stay (*reasoned*). **17/11, the fourth research**: CARB's 2006 case of one cylinder's intake-valve deposit making it rich and the loop leaning all four — the sign of 032's idle cell, a point or two in size here. Read with H1 | with H1, item 9's warm leak-down with 3 twice (`plan.md` 9) |
| B3 | **H4** the injector loom at 3 | 3's deficit is an amount at a small charge, not a share — what an injector opening late through a raised resistance gives; the wiring is what stays with the cylinder through a change of injectors. Against: the supply steady through a whole stop, no step at a swell (004, 15/11); a wire has no reason to swell and mend, so the floor at most; the spark side against, 3 level at full load. **17/11, the fourth research**: weakly against, the enriched cold idle worse at matched load than the warm | **6m, 17/11**: each injector 16.0–16.1 Ω, the supply side 0.2 Ω on every pair, flexing moved nothing — the coil and the supply cleared, cold and at rest. Left: the control wire to the ECU's pin 58 (`plan.md` 6n); closer to the fault, injector 3's voltage and current against 4's, warm and running (the fourth research, 17/11) |
| B4 | **H20** coolant into 3 | Fits one cylinder at idle, where the cylinder's pressure is lowest, and the fading with load; plug 3 the cleanest of the 10/10 set (*the owner*, 4/11, weak). Against: the level holds (*owner*), no emulsion, no steam-cleaned crown in the photos; nothing in it fills and empties; **17/11**: 3 a little better, not worse, with the warmer coolant of the fan's cycle (weak) | the CO₂ test of the coolant (it can miss a small weep, 17/11); bubbles at the tank in the leak-down (`plan.md` 9); the system held at the cap's pressure and the borescope in 3 (a lead, 17/11) |

**A. The common part — what makes every cylinder alike rougher** (the
small unevenness on all four, most of `IdleHealth`'s floor and nothing
014 counts):

**Every cylinder has a floor of its own** (18/11, *the owner's
reading*; S1, *Every cylinder at 3's floor and in its swell*). On 3's
floor, against the mean of 1, 2 and 4: **3 −9.7, 4 −4.4, 1 +1.6,
2 +2.8 %** of a stroke, and the stroke-to-stroke scatter 3 > 4 ≈ 1 > 2
— nearly the borescope's order of deposit (3 > 4 > 2 > 1). Only 3
swells. So the floors may be **one cause on all four in different
measure** — deposit everywhere, most on 3 and 4 — or a different thing
on each; part of 1's and 4's place is the crank wheel's. **Kept as two
lists** (*agreed with the owner*, 18/11): 3's swell, and what puts its
floor below the others' spread, is B; the spread itself, and the
scatter on all four, is A. *Proposed the same evening and dropped: a
list C for 3's floor apart from its swell — the floor reads as A's in
3's measure as much as B's.*

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| A1 | **H0** normal for this engine | A common part that no repair, day or drive has moved, and that answers only to the charge, is what an engine's own scatter looks like; a fixed fault reads the same, and no healthy AQY says which. Against: 014 far above VW's 0–5 — but that is 3's, list B. **17/11, the fourth research**: still no healthy M5.9.2 log found; it gains only as the belt loses | 014 on a healthy AQY, VCDS only (a capture is not obtainable) |
| A2 | **the timing belt a tooth out** | The common part is a constant — the same within 5 % at every warm idle since 24/9, answering only to a load, the gas and temperature — which a fixed fault on all four gives and a source that varies by the day does not (S1, *The swell's shape*); the cam's timing sets the burnt gas kept at idle. **The marks, 8i (13/11)**: the cam's OT mark set; the crank pulley's only notch 30–60° of crank behind the groove on the block by eye and borescope, **2–3 cm along the rim, more likely more, not over 5 cm** by the owner's fingers the same evening (14–41°, if the pulley is 14–16 cm across — the diameter a guess); the cam advanced if both are the true marks (the direction the owner's, read off the part), and if they are not, the direction is open too (*the owner*, 14/11). **VW's references, read 17/11** (*What the forums say*, searched again 17/11): the damper's mark against the bottom belt guard's, the flywheel's in the gearbox window, **none on the block** — so the groove 8i read against is not one of VW's, unless it was the guard's; **a pulley bolted on turned** (*the owner*) is excluded by design, the damper and crank sprocket fitting one way only, but not the damper's outer ring slipped on its rubber. **A tooth is 13.85° of crank**: 30–60° is 2.2–4.3 teeth and 14–41° 1.0–3.0, the two meeting only at two. **Against more than about a tooth**: settled full throttle takes 496 mg of air a stroke at 2,400 rpm, 520 at 3,600–4,400, 485 at 5,200, 452 at 5,600 (85–90 g/s at the top, every 003 log; 84–90 g/s at 5,000–5,500 in sixteen logs from 9/2026 to 9/11), and the acceleration needs 0.94 of b7 with no tilt by gear or band (83 pulls; `drivescan.py --pulls`) — two teeth of advance or more would take the top of the filling away (*general*); a tooth or less is not excluded with no healthy AQY to set it against. The ECU compares the phases: VW's fault table for the family lists 16724 / P0340 and 17748 / P1340, the cam and crank senders' incorrect assignment, beside 16725 / P0341 for G40's signal out of place — none ever stored here; no tolerance is published, so one tooth may pass where two would not (*reasoned*). Belt from 10/2017. Kept first by the owner from 13/11 until **17/11 evening, when he agreed H0 above it** (the fourth research: the marks read against no VW reference) | **8q**: the mechanic's count of teeth before the old belt comes off, against VW's references (the flywheel's mark or the piston at plug 1), and the common part by capture before (`54`'s warm stop, 17/11, after the gasket: 2.96 rpm rms) and after the new belt, 7/12 (`plan.md` 8q) — and 3's floor and swells beside it, a cylinder at its edge perhaps answering to a tooth more than the rest (*the owner's question*, 17/11) |
| A3 | **H8** throttle and idle control | The air and the idle regulation act on all four alike, and S20 dates from this throttle (*owner*). Against: 055's two fields sum to the same correction at every warm idle (27/10), so a reset or the A/C gives no more air; the advance's scatter does not go with the common part (003, 12/11); 014 does not follow 055's learnt value (`refuted.md` C19); the regulator holds through 3's swells on 18 stops (15/11) | no test left for the idle; S20 keeps it |
| A4 | **H11** both probes shifted | What is left is the idle-only form — the front probe reading rich in the idle's cool exhaust, so the true mixture lean; it fits 032's negative idle cell with part load untouched. Against: both probes replaced 10/11 and the idle as rough; on the relearn drive its marks 1, 3, 4 and 5 failed (H11, *The relearn drive*); the rear probe's state never tracked `IdleHealth` | nothing planned; 036 watched at VCDS sessions (`plan.md` 8f) |
| A5 | **H7** the rail's pressure | A hot rail after a hot drive fits the time of the rough start, not its one cylinder; S19 fits it (shared with H16 until 17/11, `refuted.md` C30). Against: the regulator answers its reference (`refuted.md` C20); a high base pressure does not fit 032's positive part load; **17/11**: nor a return restriction, which would pull both cells negative (S19, *re-reckoned*); the common part is the same after high revs as after none; never gauged | a rail gauge (`plan.md` 8u): 2.5 bar at idle, 3.0 with the regulator's hose off, 2.0 or more ten minutes after switching off (`vcds.md`) |
| A6 | **H2** a leak ahead of the converter | Widened 10/11 to the zone between the probes (the joint, the flex, the plugged boss), which gives a lean rear probe at idle but not 032 or the dips; S2, S11 and S14's air. Against: the cold tailpipe and smoke tests found nothing; the visible manifold has no soot and no holes (31/10); 032's idle cell takes fuel away, where air ahead of the front probe would add it; the front loop holds through 3's swell; the rear probe's sinking was the old probe's; cannot pick a cylinder. Untested: a crack open only hot, the part under the heat shield | none planned (the warm tailpipe test dropped 15/11, *the owner*) |
| A7 | **H18** oil past the stem seals | All four alike: worse after idling, calm after a working drive; for one valve it is the swell's second reading (list B's matter, S1, *The swell's shape*). **For, 17/11**: a brown liquid stood round the backs of inlet valves 2, 3 and 4 with the manifold off, there before the wash (*owner*) — the first direct sight of oil at the valves, though the old joint left the same and it does not pick 3; **17/11 (`54`)**: the joint new and the swell as before, so the joint's oil was not it (`refuted.md` C28). Against: it does not grow with the time into a stop; **no blue smoke ever**, the plugs dry; **17/11**: 3 no worse in the first seconds after a coast-down, the deepest vacuum | the oil level on the fresh oil (`plan.md` 6i); the plugs at the next change (8v) |
| A8 | **H21** the front probe's signal-earth wire | What is left after 8h (`53`, 15/11: only the supply stepped with a load, `refuted.md` C26): the front probe's damaged signal-earth wire, which reaches the common part only through a mixture; S19's idle cell if a signal earth carries heater current (*reasoned*). Weak for the idle: the new rear probe read healthy for 18 minutes and the idle was as rough | 8e's harness at the end; each wire to the ECU's pin with the plug off (with 6n) |

**More than one at once** (*the owner's point*, 12/10): each repair may help
only in part; a partial improvement is read as a share, not a miss.

### How the vacuum gauge is read

*General*, the classic readings; read the needle against itself. Read on
14–15/10 (H3): **steady at idle, a little higher at 2500** — no valve fault or
large leak the gauge can see.

| the needle | reading |
|---|---|
| steady at idle, rises a little at 2500 | no valve fault, no large leak |
| an occasional sharp flick at idle, gone at 2500 | the misfires themselves; names nothing |
| a regular flick every cycle | one valve that never seals |
| low and steady at idle, normal at 2500 | air in behind the throttle (H3) |
| low at idle and at 2500 alike | a late cam, or an exhaust restriction |
| a fast flutter, worse at 2500 | weak valve springs or worn guides |
| slow wandering at idle | mixture or idle control hunting (H8, H7) |

---

## The plan

**The order of work is `plan.md`**: the idle first, a repair at a
time, readings only where they decide the next step. The tests above are
reference, not a schedule.

**A higher idle was tried, 12/10, and does not help**: raised to 830 rpm
specified (VW's procedure, login 01283), 014 kept counting and `IdleHealth`
rose slightly; put back the same day (`refuted.md` D9).
