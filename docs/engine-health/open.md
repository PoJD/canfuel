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

## Where it stands — 20 October 2026

**Closed**, in `refuted.md` §D: S6 the exhaust joint behind the converter,
S7 the cold start, S8 the top end, S9 the rich trim, S10 the oil leak at
the back of the head, S12 the tip-in hesitation, S13 the throttle's
routine, S15 the sputter; H9 (crankcase ventilation, A15) and H10 (when
014 counts, C19).

**Open:**

- **The idle — S1 (unsettled) and S3 (014 counts at idle).** Every part in
  the fuel and ignition path has been replaced and both remain. **About two
  thirds of the dips sit on two neighbouring cylinders, 3 and 4** where the
  injector cuts of 10/10 name them (*One cylinder or two*). The look inside
  on 19–20/10 found **3 and 4 worse inside too** — ports, crowns, exhaust
  valves — and their NGK plug ends the loosest (`idle-log.md`).
- **S18** — cylinder 3 out, cold, with a tick at camshaft rate, 18/10 (P0303).
  Not back on five drives since; deposit seen to have come away on 3 only.
- **Around the idle:** S2 (an occasional puff), S14 (bangs on an unblipped
  downshift), S11 (a hiss at the back, perhaps the throttle's own air).
- **The cylinder 4 knock window: S4, S5** — its own cluster, not in
  `plan.md` (*owner's decision*, 9/10).
- **Not pursued:** S16 (a tick on the gearbox side), S17 (a resonance at
  ~2200 rpm).

**Ranked (20/10 evening):** **H15, H13, H1, H3, H4, H14, H2**, then H0, H7,
H8, the timing belt, H11, H12 (*The idle's candidates, ranked*).

**Next** (`plan.md`): the VW leads `06A 905 409 L` and plugs
`101 000 033 AA` on 21/10, **the only change on the car**; the first drive
captured from the laptop. The original map (H14) is postponed until the
tuner's two files have been compared.

---

## The symptoms

### S1. Unsettled idle — engine speed fluctuates

**What is seen.** Every few seconds the idle dips by 20–45 rpm and recovers in
about a quarter of a second. It feels restless from the driver's seat too.

**How it is measured.** `IdleHealth` on 0x604 grades one firing against the
next (100 = the engine before the repair, lower is smoother). Offline,
`tools/idledips.py --roughness` gives the same grade from a capture.
**Every idle figure in these files is on the `IdleHealth` scale**
(*owner's decision*, 12/10): the mean step in rpm × 50. A capture's figure
is a mean over a window, the display's a running filter of the same
quantity. **A reading without the oil temperature beside it compares with
nothing**, and a session on **fresh adaptations** (after a battery
disconnect) reads calmer on every ruler and is no test of a repair
(`refuted.md` C19).

**What one dip is worth.** Engine speed on 0x280 is recomputed once per 180°
of crank, one power stroke (`docs/firmware/can-decoding.md` trap 5), so a dip
is one cylinder's stroke. A stroke that gives nothing costs an estimated
33–57 rpm; the deepest dips are 37–46, the typical one 20–22 — a partial
burn. **The dip is the failed combustion itself**, and the recovery is the
idle governor.

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
| 18/10 eve | `39` | settled | after S18's episodes | 78 ± 4 |
| 19/10 | display | settled | | about 100 loads off |

**The MAF is the one change that showed at once** (24/9: the dips halved).
The calmest settled idles, 12/10 and 15/10, came in the days after the new
leads and lead 4's re-seat; the idle has worsened since (*Why the idle got
worse*, S18).

**What is not known: the healthy target.** Every recording is of this engine
with the fault present; nobody has recorded a healthy AQY (H0 test 1).

**When S1 closes** (*decided*, 20/10; the owner closes it), read over several
drives at 95–100 °C of oil: **(1) the dips no longer keep to a pair** —
`cutscan.py --shares`, pooled since the last repair, consistent with all four
alike; it needs no target, so it is the strongest mark; **(2) load is no
longer needed** — loads-off `IdleHealth` within about 25 of loads-on (19/10:
about 100 against 50); **(3) at least the best level shown**, loads off about
50–60 (12/10, 15/10). Short of all three, the owner may close it as
*acceptable, cause known*.

**Load smooths it.** Every consumer at idle — A/C, lights, blower, heated
glass — makes the ECU open up the air, and the idle calms (26/9: 35–50 loads
on against 70–80 off, *owner*). The supply voltage is 1.25 V *lower* then,
so it is the charge, not the volts. **Since the cleaner, the partial loads
hardly matter** (*owner*, 19/10): lights and blower alone make little
difference, everything on together still calms it. **The first measured
pair**, 19/10, oil 101 °C: loads off mostly about 100, every load on mostly
about 50 — twice what one pair can show by chance. Read as (*reasoned*):
**one or more cylinders run at the edge of stable combustion at the idle's
charge**, and anything that takes a little charge away tips them over.

**Temperature.** Roughest cold, calmer as the oil warms, calmest hot, in every
session since 24/9. Every engine idles roughest cold (*general*), so this
says nothing about the fault on its own. The roughest reading yet, ~186, came
cold on the dampest, foggiest morning (26/9, *owner*).

**What comes before a dip** (`tools/dipcontext.py`, 852 warm dips,
10/10). **The ECU has trimmed the charge just before a dip** — injection time
0.33 and indicated torque 0.35 counts lower 0.4–0.1 s before, about 1 %, and
engine speed a few rpm higher: the idle overshoots a little, the governor
takes a little air or advance away, and a weak cylinder fails in the next
cycles. A dip follows a trim down 1.6–3.5 times as often as a trim up. ⚠ An
average, under one count; no single dip shows it. The figure `dip-profile.svg`
beside this file shows one dip stroke by stroke.

![One idle dip](dip-profile.svg)

**What VCDS saw just before a dip** (11/10, `dipcontext.py --vcds`): on two
sessions the lambda correction was about 0.8 % lower just before a dip than in
quiet idle — the loop on its lean swing. **Not reproduced on 12/10** (`32`,
001 alone, the session built for it): a direction one session failed to
repeat.

### S2. An occasional puff from the exhaust

*Owner*, at idle, long-standing — before the exhaust work, the injectors and
the MAF. Much weaker than S14's bangs, and in the owner's reading the same
thing smaller: **a misfire's unburnt charge going off in the exhaust**. On
12/10 he heard the puffs **come with the dips** (by ear, not aligned with a
recording). It outlived the resealed joint behind the converter (S6, closed).

### S3. Misfires counted by the ECU at idle

**VCDS group 014**, 12–120 against VW's 0–5, on every drive since it was
first logged. No fault code is stored (the ECU stores P0300 only above 2 %
over 1000 revolutions, `vcds.md`); **it once did**: P0304 and P0172 in an
old scan of 5/2019 (`vehicle-history.md`).

**When S3 closes** (*decided*, 20/10): 014 reads **0** at a warm idle with
loads off, oil 95–100 °C, for 3–5 minutes, **on three sessions on different
days, one straight after a hard drive**. The counter steps in twelves, so
zero is the only reading inside the specification.

- **Only at idle, and that is the car.** Detection sees a misfire more easily
  under load and switches off below about 20 % load (measured over every 014
  log). Driving with detection `aktivováno`, new counts start once per ~250
  samples, against several a minute standing. The C4 full-load lamp lit on
  this map, so detection under load was not off — **unless the remap dulled
  it** (H14 route 6).
- **The events are the S1 dips** (`tools/s3align.py`, eleven sessions,
  16/10): half of 014's rises sit on a dip in the 1.5 s before, against 22 %
  by chance; a third of the dips get a rise. Over minutes the two part:
  **whether it counts is decided by the load and the learned idle air**
  (`refuted.md` C19), not by how rough the idle is. **The A/C switches it**
  (*owner*, 16/10): A/C on, 014 at zero for minutes with `IdleHealth` ~70; A/C
  off, it counts and the grade barely moves.
- **Three properties to keep in mind** (`refuted.md` A11, A12): steps of 12;
  off below ~20 % load; its sensitivity per dip moved five- to fiftyfold with
  the MAF. **So 014 is a yes/no witness, not a ruler.** Compare across time
  with engine speed or `IdleHealth`.
- **Session A, 3/10**, and **Session A after step 1b, 4/10**: the first warm
  stops ever with 014 at zero — on fresh adaptations — then counting again
  after five minutes of hard driving. **Session B, 4/10**: counting again,
  055's learned value at −1.0 to −1.2. **Steps 2b and 2c, 9/10**: the first
  session on kept adaptations, counting at every stop. Read together: the
  learned idle air (C19).
- **The drive after the new leads, 10/10** (`31`): 014 at about 9/10's
  rates — better hot, worse cold, no direction. The leads did not fix S3.

### S4. Knock retard on cylinder 4, and only cylinder 4

Groups 022/023 and 020: cylinders 1–3 read zero in almost every sample;
cylinder 4 retards in steps up to 13.5 °CA, mostly on a tip-in after a coast
or gearchange and on hard pulls, **never at idle**. Within VW's 0–15 °CA while
driving. 9/10: still cylinder 4 alone with all injectors seated (`refuted.md`
B7); 10/10, the first drive on new leads: almost none (3 samples); 12/10:
back, smaller, on a harder drive. *Reasoned*: an arc at lead 4's plug end is
broadband noise in 4's own window (H15), as is real knock from the crust on
4's crown (`idle-log.md`, 19–20/10).

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

### S14. Bangs from the exhaust on a downshift without a blip

*Owner*, 4/10: on a downshift **without a throttle blip** a series of small
bangs, 1–2 s after the clutch comes up; with a blip almost never; warm. Gone
9–14/10, **back on 15/10, quieter** (*owner*), with the joint behind the
converter tight — so that joint fed or carried it at most. Read as
(*reasoned*): the engine dragged up on a shut throttle is fuelled at its
thinnest charge; a charge that fails to fire goes out as fuel and air and
burns when the fuel cut pumps plain air in after it — **a misfire where 014
is blind**. The ECU cuts the injectors 0.8–1.6 s after the lift
(`coastscan.py`). **The owner's to watch, not in `plan.md`** (*owner's
decision*, 4/10): worked on only if it outlives S1/S3.

### S16. A tick in neutral, cold, with the clutch pedal up

*Owner*, 12/10: a regular tick at a cold idle in neutral, **gone with the
pedal down** — the gearbox side. **Not pursued** (*owner's decision*): the
idle graded the same pedal up and down (H12). Out of the fit tables.

### S17. A new exhaust sound, from a new place

*Owner*, 15/10: only at about 2200 rpm, **like a resonance**, perhaps the
remade joint behind the converter, perhaps nearer the engine. A sound tied to
one engine speed is a part vibrating, not a leak (*general*), so it bears on
no hypothesis about the idle. Out of the fit tables until placed.

### S18. Cylinder 3 dropped out, cold, with a tick at camshaft rate — 18/10/2026

**What happened** (*owner*, 18/10). On a short gentle drive, cold, the engine
**ran on three cylinders for a while** and a **tick** started that followed
engine speed. **P0300 and P0303** stored — the first time the ECU named a
cylinder. The tick, off the owner's phone video: **once per 720°, camshaft
rate, one event per cycle**, with all four firing beneath it
(`photos/tick-2026-10-18-cold-spectrogram.png`); by ear from under the cover
rather than the injectors. Cylinder 3 dropped out again **with the lamp
flashing**; after a restart all four ran and the tick was gone. **The
afternoon, warm**: the tick back for a few minutes, gone by itself; **two
bursts in 014 under part load** (270 at 1720 rpm, 351 at 2960 rpm), where
sixteen earlier logs never read above 72 while driving; `IdleHealth` while it
ticked 120–130 against 80–90 without. Context: the cleaner's tank had just run
out, after the hardest driving this car has had in the owner's hands.

**Since** (`39`, and four drives off the display, 18–19/10): **no tick, no
three-cylinder running, the lamp off**, full-throttle pulls included; fault
memory empty before and after `39` and over 19/10; 032 and 055 inside their
history (19/10, `idle-log.md`). **The look inside, 19–20/10**: **cylinder 3's
exhaust valve carries light patches where a layer of deposit has come away**,
its crown a layer breaking into islands — the only cylinder where that is
seen. It fits a flake under 3's exhaust seat and does not show it.

**Read as** (*reasoned*), all fitting a tick once per cycle and a cylinder
that misses: **a flake of deposit under valve 3's seat** after the cleaner
(H13) — gas jetting past a seat that nearly closes ticks, a larger gap drops
the cylinder; **a valve or lifter on 3 that hung** (H1); **an arc at lead 3's
plug end** (H15), which clicks exactly once per cycle; injector 3, weak for
the tick. **No leak-down** (*owner's decision*, 20/10): whether S18 recurs is
what tells a flake from a valve. **A flashing lamp means ease off and stop**
(`plan.md` item 5).

**Why the idle got worse** (19/10, *reasoned*; display readings, loads off or
lights only, warm): 50–61 on 12/10, ~54 on 15/10, 70–90 on 17/10, 80–90 on
18/10 afternoon, ~100 on 19/10; with every load on it has hardly moved (~40–50).
**The rise began about 16–17/10, with the cleaner and the hard driving**, not
with the episodes; it is worse only at a small charge; and `39`, the first
capture after them, has its dips more concentrated on the pair than any pool
before (top two 77 %). **Not an adaptation**: 032 −3.1/+5.5 %, 055 −1.27 g/s,
both inside their history (19/10). The candidates: deposit loosened by the
cleaner and not yet burnt off (H13), and **a relief after the leads' re-seat
of 10–12/10 wearing off** (H15, *The idle against every time the leads were
handled*).

### Other — not symptoms, but they touch this file

**Oil temperature.** 0x420's `OilTemp` is `raw − 60` °C (`docs/firmware/open.md`
question 10). A bias moves both sides of every comparison alike.

**The remap.** The ECU was remapped in 6/2018, "mild", the tuner finding
nothing at the top. Written down as H14 (16/10). **Postponed 20/10** (*owner*):
not written back on 22/10; the tuner emails the original and his remap to be
compared first, privately, never in this repository (`plan.md` 5a).

**The brake pedal is soft and long** (*owner*, 9/10): hydraulics, not the
servo and not the engine — a matter for a garage.

---

## How the symptoms relate — what is measured

| pair | link | evidence |
|---|---|---|
| S1 ↔ S3 | **the same events, but 014 is switched** | half of 014's rises sit on a dip; whether it counts follows load and the learned idle air, not the grade (S3) |
| S1 ↔ oil temperature | **strong** | roughest cold, calmest hot, every session |
| S1 ↔ load | **strong** | every load on calms it (S1) |
| S2 ↔ S3 | **likely** | the owner heard the puffs come with the dips (12/10); never aligned |
| S14 ↔ S2 | **likely one mechanism** (*owner*) | a misfire's charge burning in the exhaust, loud when the fuel cut adds air |
| S14 ↔ S3 | **possible** | 014 is blind on the overrun, so it cannot be aligned |
| S4 ↔ S5 | **very likely one thing** | same window, same speeds; S5 needs no combustion |
| S4/S5 ↔ S1/S3 | **none measured** | no retard and no 026 signal at idle; but the dips sit on 3 and 4, and lead 4's end was the loosest (H15) |
| S18 ↔ S1 | **the same pair** | cylinder 3 named; the idle worse since (S18) |
| S11 ↔ S1 | **untested** | if the hiss is a leak, H3 or H2; the owner reads it as the throttle's own air |

**Two clusters**: **the idle** (S1, S2, S3, S14, S18) and **the cylinder 4
window** (S4, S5). S11 sits beside the idle, unplaced.

---

## The open hypotheses

Each lists what it explains, what speaks against it, and the test that
settles it. ✔ fits, ~ fits weakly, ✘ does not fit, — says nothing.

**The columns are the open symptoms that bear on the engine**: S1, S2, S3,
S4, S5, S11, S14, S18. Left out: S16 (the gearbox side, shown not to touch
the idle) and S17 (a resonance, not placed); the closed ones are in
`refuted.md` §D.

### H0. The idle is normal for this engine — and there is no fault to find

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ✘ | — | ~ | — | ✘ | ✘ |

- **Against:** 014 reads 12–120 against VW's 0–5; the old converter burned
  through; the dips sit on 3 and 4, the cylinder of the 2019 P0304 and of the
  noisy knock window; S18 named cylinder 3; the inside of 3 and 4 is worse.
- **For:** no code is stored (2 % threshold: *under 2 %*, not *healthy*).

**Test:** **record a healthy AQY** — another 2.0 8V (AQY, AEG, APK, AZJ;
Motronic M5.9.2), warm idle, 3–5 min, a USBtin capture and 014. The single
most valuable measurement left; nothing usable has been published (searched
27/9 and 9/10). ⚠ It only compares on an ECU that holds engine speed per
stroke (`idledips.py --degrees` reads 180°); the one public PQ capture,
comma.ai's Passat, smooths it and grades 0.

### H1. A lifter or valve on one cylinder (valvetrain)

A hydraulic lifter that bleeds down, or a valve that seats late or not quite,
on one or two cylinders. *General.*

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ✔ | ✔ | — | ~ | ✔ |

- **For:** a valve that seals worse at low cylinder pressure misfires at a
  small charge and is covered by load; S18's tick once per cycle; one forum
  AQY case of a sticking bucket tappet (pkw-forum.de, 2003) and one of valves
  not sealing (forum.vwgolf.pl t=522030).
- **Against:** compression **13 bar in 2018 and 12 bar even on all four in
  2026** (`vehicle-history.md`) — no cylinder losing; the vacuum gauge
  steady cold and warm, no flick (H3); no ticking before S18, and none on the
  five drives since; the idle is never worst hot, where a thin-oil lifter
  should be; the valves looked whole on 19–20/10 (which says nothing of
  sealing); S18 is now explained by 3's flaked deposit without it.

**Tests:** a stethoscope over each lifter, warm; a warm leak-down (**not to be
done**, *owner's decision*, 20/10); the lifters pressed down with the cover
off. **Whether S18 recurs** is the reading left.

### H2. A leak ahead of the front lambda probe (manifold, its joint to the head, the probe boss)

At idle the exhaust pulses dip below atmospheric and a crack draws air in.
*General.* The zone is only the **original manifold, its gasket to the head
and the probe's boss**: the probe sits on the manifold (`vehicle-history.md`).

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ✔ | ~ | ✘ | ✘ | ✔ | ✔ | ~ |

- **For:** the puff (S2), the hiss (S11), air for S14's bangs; a 26-year-old
  manifold that has lived through years of misfires.
- **Against:** air outside the cylinder does not stop one firing, and cannot
  pick a cylinder; no ticking, no exhaust smell (*owner*); just before a dip
  the probe read a little *rich*, not lean; the cold tailpipe test found
  nothing (12/10) and the cold exhaust smoke test nothing (9/10, the exhaust
  would hardly take pressure).

**Test:** the tailpipe test **warm** (`plan.md` item 7). A found leak means a
new manifold.

### H3. A small unmetered air leak at one intake runner

Air past the MAF leans one cylinder at idle, where air flow is smallest.
*General.* **The only candidate that predicts *load helps* directly.**

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ✔ | ~ | ✔ | ~ | ✘ | ~ | ✔ | ✘ |

- **For:** the regime; S14 at the thinnest charge; a leak at one runner acts
  on one cylinder, and 3 and 4 are neighbours on the lower manifold.
- **Against:** a large leak is refuted (`refuted.md` A7): idle air 3.1–3.5 g/s
  against VW's leak mark of 2.0, 055 inside ±1.5, 032's idle cell negative.
  **The intake smoked tight cold** (9/10) after the dipstick guide and the
  MAF clamp were put right; **the vacuum gauge** on the tee by the runners
  steady at 18–19 inHg cold and warm, higher at 2500, no flick (14–15/10) — a
  gauge on the common plenum cannot see a leak at one runner. The lower
  gasket looked alike at all four (*owner*, 20/10). The crankcase gas enters
  the common intake, so it cannot pick out 3 and 4 (*owner*).
- **Parts renewed in its name:** the upper plenum gasket (each time it came
  off), the breather and its hoses (12/10), the throttle and its gasket (2/10),
  the injectors re-seated (1/10).

**Test:** the lower manifold gasket at the head — renewed, or smoked warm —
**next if the VW leads change nothing** (H15).

### H4. Weak spark from what feeds the parts (earth, wiring, coil feed)

**Much weakened, kept last of the electrical side.** Measured clean: the
coil's ground and supply for a gross fault, the engine's earth under load,
the charging; the battery is new (8/2026). **The idle is better with the loads
on, when the coil's supply sits 1.25 V lower** — a spark limited by supply
would go the other way. The dips sit on 3 and 4, on separate leads and on
**different coil outputs** (1+4, 2+3), so neither the coil nor its feed can
pick them. **What is left**: the injector loom where it reaches 3 and 4,
shared by the two, taped and oily — its wires at 4 whole outwardly (*owner*,
19/10; tape renewed). The plug-end side moved to H15.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | ~ | — | ~ | ~ |

**Tests:** the injector loom flexed at 3 and 4 at a warm idle, watching the
grade (`plan.md` 5a's loom minutes); VCDS 004 (the ECM's supply) beside 014.
VW's TSB 01-08-27 (the coil's ground wire, US sister engines) is the joint to
look at first if the spark side ever comes back.

### H5. Something in cylinder 4's knock window that is not combustion (S4, S5)

The ECU books anything at cylinder 4's crank angle to cylinder 4: G66, its
torque or connector; a loose ancillary part buzzing in a speed band; **an arc
at lead 4's plug end** (H15). Injector 4's click is settled against (B7).

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| — | — | — | ✔ | ✔ | — | — | — |

**Tests** — not scheduled (*owner's decision*, 9/10): G66's torque and
connector; a look for a loose bracket at ~3000 rpm in neutral; after the VW
leads, the neutral 026 holds and a 020 drive against
`vcds/vcds-step2c-020-026-003.csv`.

### H6. Knock control relearning after the battery disconnects

Explains how S4 changed between logs, not S5. **Test:** 020 + 026 after a few
hundred km without a disconnect.

### H7. Fuel delivery at idle: rail pressure, one injector

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | — | ~ | ~ |

- **Against:** four new injectors and a new filter changed nothing in S1; the
  trims near zero; full-load pulls reach ~85 kW, where a weak pump shows first;
  the regulator (7/2026, 3 bar) dry at its hose; injector tips clean on the
  borescope (19–20/10).
- **A plug washed clean by fuel** (a forum extract on the AEG/AQY, 20/10:
  *"#3 was much cleaner … replaced #3 injector as it was washing that plug"*):
  plug 3 is the cleanest here too. Weak, for the reasons above; a reason not
  to read plug soot as combustion quality.

**Tests:** a rail pressure gauge (**not bought**, *owner's decision*, 10/10);
swap injector 3 with another if the cylinder stays named.

### H8. Idle air control and the throttle body

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | — | ~ | — | — | — | — | ✘ |

**Against:** a dip is one firing that fails and recovers in a quarter of a
second, not a hunting loop; the plate angle in every VCDS log is steady and
the misfires do not ride on it (27/9); the potentiometer track has no dead
spot or dropout on the bus; the throttle is **new since 2/10** (Pierburg
`7.03703.13.0`) and the idle fault outlived it; it acts on all four. Kept
because it is in the idle air path, not because anything points here.

### H11. Both lambda probes shifted alike

*Added 10/10 at the owner's request, as a weak hypothesis written down so
that it is not argued again.* The probes are from 10/2017, the one part of
the mixture control not changed.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | — | ~ | ✘ |

**Against:** 032 + 033 near zero on a new MAF and new injectors bound a hidden
shift to a few per cent, and with the wrong sign (the ECU takes fuel out); a
shift small enough to hide is too small to misfire. **Test:** a four-gas
analyser at the emissions station, warm idle and 2500 rpm. *Not in
`plan.md`.*

### H12. Driveline play read as misfires

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ✘ | ~ | ~ | ~ | — | ✘ | ✘ |

**Against:** the MAF swap halved the dips; play repeats every 360°, the pairs
1+4 and 2+3, while the dips sit on 3 and 4, 180° apart; the puffs come with
the dips, and play makes no unburnt charge. **The clutch minutes** (12/10):
pedal up no rougher than down — not the gearbox side (S16). The crank
pulley's damper fine by eye.

### H13. Deposits after years of gentle driving — inlet valves, chambers, ring lands

*Added 15/10 at the owner's request.* The engine seldom saw more than
3000 rpm for at least nine years (*owner*). Gentle use builds deposits where
hard use burns them off (*general*).

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ✔ | ~ | ✔ | ~ | — | — | ~ | ✔ |

- **The look inside, 19–20/10** (H13 test 3, `idle-log.md`): **no inlet valve
  back is coked** — thin lacquer on all four, so no walnut clean; **the
  chambers carry it** — thin layers on every crown, a crust on 4's bowl edge,
  and **on 3 a layer breaking up, crown and exhaust valve alike**. Ports and
  chambers rank **3 > 4 > 2 > 1**, the pair the dips sit on.
- **Consequence more than cause** (*the owner's reasoning*, 20/10): every
  cause put forward for deposits acts on all four alike, and 3 and 4 are
  worse — so their extra deposit reads as **years of poorer combustion on 3
  and 4**, from something that touches those two only (H15). Once there, the
  deposit adds to it: a flake under a seat (S18), heat and compression for
  knock on 4 (S4).
- **Against:** a detergent premium fuel since 2017; compression even.

**Tests:** the cleaner and hard driving (a tank from 15/10, done; a second can
is `plan.md` 6a, the owner's call after the next drives); whether S18 recurs.

### H14. The remap of 6/2018 — the idle's ignition, or its margin

*Added 16/10 at the owner's request.* A map acts on all four alike, so at most
it narrows the margin until the weakest two show. Fuel at a warm idle is pulled
back by the lambda loop and would show in 032, which reads small.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | ✘ | — | ~ | ✘ |

**Where a remap could reach the idle**: the idle's base advance (the governor's
fast actuator); its cold corrections; **the misfire detection's own
thresholds** — **route 6**: dulled under load, so that misfires everywhere are
counted only at idle; the overrun fuel cut (S14); knock control under load
(S4). **The idle advance** (`tools/idleadvance.py`, 17/10): medians 1.5–3.8°
BTDC since 24/9, inside VW's 0–12°, **not aggressive**; on 11/8, on the same
map, after TDC most of the time — so that shift is not the map's.

**The ECU** (`vcds.md`): Bosch M5.9.2, hardware `0261206327`, software
`1037352075` V04, 256 KB flash. No map definition is public.

**Tests:** (1) **the tuner's two files compared** (postponed 20/10): the diff
— how many bytes, in how many blocks; tables found by shape, written as a
guess where it is one; **the idle cells of the ignition map against the
measured idle advance**; whether the detection's thresholds were touched.
(2) **The original map** afterwards (`plan.md` 5a), read on the idle advance,
the overrun cut, 014 against `IdleHealth`, 014 under load (15 counts in about
4,300 `aktivováno` samples on the remap), and 020 on a pull; one held pull in
4th to re-check the torque scale (`docs/firmware/can-decoding.md` question 8).

### H15. The aftermarket leads (and plugs) — NGK plug ends that grip loosely, on 3 and 4 above all

*Added 17/10 at the owner's request; retitled 20/10* (it read *a set that fits
all four slightly wrong*). **The claim**: not one bad lead but **the NGK
design's fit on these plugs** — every set on the car since at least 12/2022
has been NGK (the invoice; `vehicle-history.md`), and the owner believes all
of them since 2018 were. A genuine VW set has never been on the car in his
time.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S18 |
|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ~ | ~ | — | ✔ | ~ |

**What it rests on:**

- **The plug ends of 3 and 4 came off far more easily** (*owner*, 19–20/10):
  by grip **2 > 1 > 3 ≈ 4**, 2 the tightest this time and on 10/10, 3 and 4
  almost without force. Oil was on all four threads, so oil does not explain
  it. The NGK ends click like rubber, with only a faint metallic click
  (*owner*). Lead 4 felt the least firm on 10/10, 12/10 and 15/10; re-seated
  on 12/10 it held better, "though not as a lead should", and was loose again
  by 19/10 (*owner*).
- **The old plug 4's terminal burnt black and pitted** (1/10), and the old
  lead 4's insert scored, its terminal set back (10/10) — what arcing at a
  loose end leaves.
- **The deposits on 3 and 4 need a cause of their own** (H13): the coil cannot
  pick them (outputs 1+4, 2+3), nor the crankcase gas (common intake); the
  plug ends are the only evidence of one.
- **Forum and search** (leads, not sources): one AQY owner cured by going back
  to "thick VW originals" (forum.vwgolf.pl t=522030); `06A 905 409 L`, the set
  ordered, a later revision of the factory `F`, thicker, with extra silicone
  by the intake (a vwvortex AEG write-up, not confirmed in a catalogue); a
  Beetle 2.0's Bosch plug end that arced and burnt out (newbeetle.org).

**Why it can still be wrong** (*general* and this car's):

- **The idle-versus-load argument holds only against a voltage fault.** At
  idle the manifold sits at about 0.35–0.4 bar absolute (the gauge's 18–19
  inHg), so the gap needs few kV but the thin, cool, diluted charge is hard to
  light: what it needs is spark **energy and duration**. Under load the gap
  needs tens of kV and the dense charge lights from almost any spark. So **a
  voltage fault** (cracked insulation, a damp boot) shows under load and in
  the damp; **an energy fault** (a loose contact, high resistance) at idle
  and cold. A loose end is the second kind.
- **The pattern outlived three NGK sets** — which H15 survives only as the
  design's fit, not a bad lead. Why the design would fail on 3 and 4 and not
  on 1 and 2 is not known.
- **The plug soot does not follow the pair**: 1 and 4 sooted, 2 lighter, 3 the
  cleanest (*owner's reading*, 20/10).

**The idle against every time the leads were handled** (the like-with-like
table in S1): the calmest settled idles, **12/10 and 15/10, came in the days
after the new set and lead 4's re-seat**, and it worsened from there — the
shape of a fresh grip working loose, and also of the cleaner and the
episodes, on the same days. A hint, not a test.

**The relief after each plug change, and how long it lasts.** *The owner's
reading*: new plugs help while good, and the poor combustion spoils them (the
12/2022 set came out eroded at ~1,500 km). *The second* (*reasoned*): every
plug change re-seats the leads, and a fresh end grips, then works loose.
**They are told apart by how long a relief lasts.**

**Test:** **the VW set `06A 905 409 L` with VW plugs `101 000 033 AA`**,
21/10, **the only change on the car** (`plan.md` 6b): at the refit, for each
cylinder the force each end takes and whether it clicks metal or rubber; the
first drive captured from the laptop, with the two states at its warm idle;
then more drives. Read against 19/10 (loads off ~100, on ~50) and 12–15/10
(~60):

- **calmer, the dips off 3 and 4 (towards a quarter each), 014 counting less,
  lasting weeks** → it was here; the ends are checked by hand after a few
  drives;
- **calmer for a few days, then back**, as after 10/10 → the relief was the
  seating, not the design: H3 next;
- **the same** → H15 refuted, and H4's spark side with it.

**Fitted 21/10/2026** (*owner*). **The VW plug is the same NGK
`BKUR6ET-10` as the set of 10/10** — its box says so — so the plugs are
only new, not different, and **the leads are the one real change**. The VW
leads are much stiffer than the NGK
set, and **each VW plug end carries a small rubber ring inside**, where it
seats on the plug; the NGK ends have none. A difference in exactly the
part H15 is about, seen before any drive; what it does to the grip is the
refit's measurement, not this.
**The refit** (*owner*, 21/10): every VW end on with about the same
force, an audible click, and **no play at all**, where the NGK ends had a
slight play on 3 and 4, perhaps 1 — the cylinders whose dips and deposits
stand out. The leads routed clear of the plenum, 3's above all.

**The least it predicts** (*owner*): the idle back at least where it was
before the episodes, loads off about 70–90 at 95–100 °C.

---

## Naming the cylinder

The bus carries no cylinder identification and 014 has no per-cylinder
counter. Two things name cylinders: the **injector cuts** (one connector off
at a warm idle; `plan.md` 5a), which mark their slot through a long run, and
the fault codes they leave. **10/10** (`31`): cuts of 1, 4, 4, 1.

**The leads' order on the coil** (*owner-read off the car, 1/10/2026*):
**1, 4, 2, 3, clockwise from the top tower** — 1 and 4 side by side, 2 and 3
side by side, the two pairs the coil fires together in the firing order
1-3-4-2. Which tower the coil itself calls which cylinder is not read.
*Dropped by the condensation of 20/10 and put back 21/10, when the leads
were changed.*

### One cylinder or two

`cutscan.py --shares` fits the shares of the four firing slots to every run of
three or more dips, each run's phase unknown; **bridged runs** keep the phase
across held values (`cutscan.HOLD_SPLIT` = 1.75 stroke-times, read off the
cuts), so a run lasts minutes. **One run of 430 s spans all four cuts of
10/10** and names every slot: outside the cuts the dips fall **42 % on
cylinder 4, 31 % on 3**, 14 % on 2, 12 % on 1. Pooled over `09`–`38` (2,435
dips): **two neighbours in the firing order carry two thirds** (0.37 and 0.30;
the other two 0.16 each); all four alike is far worse a fit, one cylinder
worse still, the two on one coil output the worst. Only `31` is named; the
others show the same two-neighbour shape unnamed.

### The dips keep to one slot

**By capture** (`cutscan.py --shares`, bridged runs; top two = the two
largest shares):

| capture | dips | top two | p (all alike) |
|---|---|---|---|
| `09` (11/8) | 18 | 72 % | 0.008 |
| `19` (24/9) | 257 | 67 % | 4×10⁻⁵ |
| `24` (24/9) | 154 | 62 % | 0.4 |
| `26`–`30` (3–9/10) | 89–262 | 66–77 % | 10⁻¹–10⁻⁶ |
| `31` (10/10) | 201 | 69 % | 4×10⁻⁵ |
| `32` (12/10) | 388 | **59 %** | 0.004 |
| `35`–`38` (15/10) | 13–228 | 62–84 % | 0.08–1 |
| `39` (18/10) | 70 | **77 %** | 0.0009 |
| **pooled `09`–`38`** | **2,435** | **67 %** | **10⁻³³** |

The pair was already there on 11/8, on the 2022 leads and the old injectors.
`--pairs` is kept for history only: pairs within a run are not independent.
**After every captured session** the shares are reported to the owner, alone
and pooled since the last repair (`CLAUDE.md`).

---

## What the forums say about this idle

Searched 27/9, 9/10 and 20/10, in German, Polish, Czech and English (forums
and search extracts; leads, not sources). **The finding is the pattern:
almost nobody reports a fix.** Every AQY thread with this picture that could
be read to its end stops unresolved after the same parts list this car has
been through. What was reported as fixed: a new battery, a new Bosch coil, a
new lambda probe, **original VW leads instead of aftermarket ones**, rings
and a head going-over, a sticking bucket tappet, the timing belt a tooth out.
Most of these are already done here; the VW leads and the belt are not.

---

## The idle's candidates, ranked

**A judgement, not a measurement**, for S1, S2, S3, S14 and S18. Re-read after
every test and whenever the symptom list changes; the history of each re-read
is in git.

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| 1 | **H15** NGK plug ends | the only thing found that touches 3 and 4 alone; an energy fault shows at idle | the VW set, 21/10, the only change |
| 2 | **H13** deposits | 3 > 4 > 2 > 1 inside; 3's deposit coming away (S18) — a consequence and now a cause | the cleaner, driving; S18 recurring or not |
| 3 | **H1** valve or lifter | S18's tick, a seat that nearly closes | S18 recurring; no leak-down (*owner*) |
| 4 | **H3** a leak at one runner | predicts *load helps*; 3 and 4 neighbours | the lower gasket, if H15 changes nothing |
| 5 | **H4** the injector loom at 3 and 4 | shared by the two, old and taped | flexed at a warm idle |
| 6 | **H14** the remap | the one control change never undone | the files, then the original map |
| 7 | **H2** a leak ahead of the probe | S2, S11, S14's air; cannot pick a cylinder | the warm tailpipe test |
| 8 | **H0** normal for this engine | no healthy AQY recorded | a healthy AQY's capture |
| 9 | **H7** fuel delivery | never gauged | a rail gauge, an injector swap |
| 10 | **H8** throttle and idle control | new since 2/10; all four | — |
| 11 | **the timing belt a tooth out** | belt from 10/2017 | its marks; even compression and the full plateau argue against |
| 12 | **H11** both probes shifted | 2017 probes | a four-gas analyser |
| 13 | **H12** driveline play | — | done: the clutch minutes cleared it |

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

**The order of work is `plan.md`**: the idle and S18 first, a repair at a
time, readings only where they decide the next step, as little idling as
possible. The tests above are reference, not a schedule.

**A higher idle was tried, 12/10, and does not help**: raised to 830 rpm
specified (VW's procedure, login 01283), 014 kept counting and `IdleHealth`
rose slightly; put back the same day (`refuted.md` D9).
