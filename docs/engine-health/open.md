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

## Where it stands — 24 October 2026

**Closed**, in `refuted.md` §D: S6 the exhaust joint behind the converter,
S7 the cold start, S8 the top end, S9 the rich trim, S10 the oil leak at
the back of the head, S12 the tip-in hesitation, S13 the throttle's
routine, S15 the sputter, S18 cylinder 3 out with a tick (24/10); H9 (crankcase ventilation, A15) and H10 (when
014 counts, C19).

**Open:**

- **The idle — S1 (unsettled) and S3 (014 counts at idle).** Every part in
  the fuel and ignition path has been replaced and both remain. **About two
  thirds of the dips sat on two neighbouring cylinders, 3 and 4**, on every
  capture until the VW leads; **on all four alike since** (`40`, `41`; *The
  dips keep to one slot*). The look inside
  on 19–20/10 found **3 and 4 worse inside too** — ports, crowns, exhaust
  valves — and their NGK plug ends the loosest (`idle-log.md`).
- **Around the idle:** S2 (an occasional puff), S14 (bangs on an unblipped
  downshift), S11 (a hiss at the back, perhaps the throttle's own air).
- **The cylinder 4 knock window: S4, S5** — its own cluster, not in
  `plan.md` (*owner's decision*, 9/10).
- **New, 24/10: S19** — P0172 stored, suspected with the start that died at
  once; fits H7 and H16 (the purge valve, added 24/10); the code alone
  also H17 (fuel in the oil, 25/10).
- **Not pursued:** S16 (a tick on the gearbox side), S17 (a resonance at
  ~2200 rpm).

**Ranked (24/10, after the cold capture with one cut):** **H14, H7, H13, H1,
H2**, then H0, H8, H3, H15, H4, the timing belt, H16, H17, H11, H12 (*The idle's
candidates, ranked*). **The dips are on all four alike on both captures since
the VW leads** (`40`, `41`; *The dips keep to one slot*), while the warm idle
graded no better than the best days on the NGK set: the leads took away 3 and
4's excess, not the roughness. So what acts on all four leads, and what acts
on one or two (H3, H15, H4) goes down. H7 rises on S19 alone. H16 enters
low: it is there for the rich trim and S19, not for the idle.

**Next** (`plan.md`): the VW leads `06A 905 409 L` and plugs
`101 000 033 AA` on 21/10, **the only change on the car**; the first drive
captured from the laptop. The original map (H14) is postponed until the
tuner's two files have been compared.

---

## The symptoms

### S1. Unsettled idle — engine speed fluctuates

**What is seen.** Every few seconds the idle dips by 20–45 rpm and recovers in
about a quarter of a second. It feels restless from the driver's seat too:
**the larger dips, about 15 rpm and over by the owner's guess, are felt as a
slight jerk in the seat** and heard, and between jerks `IdleHealth` holds
lower (*owner*, 23/10/2026: about 50 between, higher with each).

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
| 18/10 eve | `39` | settled | after the episodes of 18/10 (`refuted.md` D10) | 78 ± 4 |
| 19/10 | display | settled | | about 100 loads off |
| 21/10 | `40` | settled | **VW plugs and leads, new plenum gasket** | 67 ± 2 |
| 23/10 | display | settled | the first 44K tank, ~70 km in, after a hard motorway run | 45–50 between jerks, 70–90 with them, **never above 100** warm; *fan on 1, one seat heater on 1, lights* (*owner*) |
| 23/10 eve | display | settled | home through Prague traffic, much idling, unsettled throughout; the last stretch held at higher revs in a low gear | **37** straight after, the lowest yet in this state, then slowly back to 50 within about a minute and above it after another; *fan on 1, one seat heater on 1, lights* (*owner*) |
| 24/10 eve | display | settled | the second 44K tank, Orlen Verva 100, after ~340 km in the day with about an hour above 4000 rpm; 3–5 min of warm idle | **70–80**, everyday state (*owner*) |

**The MAF is the one change that showed at once** (24/9: the dips halved).
The calmest settled idles, 12/10 and 15/10, came in the days after the new
leads and lead 4's re-seat; the idle has worsened since (*Why the idle got
worse*, below).

**What is not known: the healthy target.** Every recording is of this engine
with the fault present, and **none will be**: a CAN capture of another car
needs its cluster harness tapped behind the vent, which no owner will allow
(*owner*, 21/10).

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

**After high revs** (*owner*, 23/10 evening, the first 44K tank,
display, the everyday state): straight after a stretch held at high revs,
`IdleHealth` **37**, the lowest yet in that state, then **slowly back to 50
within about a minute and above it after another**; stretches of plain idle
without revving go back to 70–80. **New to him**, though he watches the
display and drives hard most days now: after hard driving before, the
lowest came only after about half a minute. **The captures agree that it is
new** (`tools/afterpull.py`, 23/10): engine speed held above 4000 rpm at
any load — sustained revs, a light foot in second as often as full
throttle (*the owner's correction*) — in the five minutes before a warm
stop, the grade in bins from the moment the idle settles. Without a
cleaner the idle after high revs **starts rough and calms over 1–3
minutes** — `30` 98 → 56 (33 s above 4000), `40` 100 → 54 (30 s), `39`
87 → 69, `28` 92 → 70; the one capture with a cleaner in the tank and high
revs before a stop, `37` (Liqui Moly, 15/10), **starts calm and rises** —
57, 44, then 60, and 64, 54, 77, 76 at the next stop. One capture, two
short stops, against a bin-to-bin scatter of ±20 in a single idle; **no
capture on a 44K tank yet**, and none holds more than 18 s above 4000 at a
stretch, far less than the owner drives now.
Read as (*reasoned*), if it is the cleaner: what the cleaner has loosened
and not yet removed (H13) costs combustion at idle on the cylinders that
carry it, and the heat and gas flow of high revs clear or dry it for a
while — flakes under 3's exhaust seat blown out (*the owner's reading*), or
softened deposit that soaks up fuel at a cool idle and is dried hot.

**Why the idle got worse** (19/10, *reasoned*; display readings, loads off or
lights only, warm): 50–61 on 12/10, ~54 on 15/10, 70–90 on 17/10, 80–90 on
18/10 afternoon, ~100 on 19/10; with every load on it has hardly moved (~40–50).
**The rise began about 16–17/10, with the cleaner and the hard driving**, not
with the episodes of 18/10 (`refuted.md` D10); it is worse only at a small charge; and `39`, the first
capture after them, has its dips more concentrated on the pair than any pool
before (top two 77 %). **Not an adaptation**: 032 −3.1/+5.5 %, 055 −1.27 g/s,
both inside their history (19/10). The candidates: deposit loosened by the
cleaner and not yet burnt off (H13), and **a relief after the leads' re-seat
of 10–12/10 wearing off** (H15, *The idle against every time the leads were
handled*).

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
days**. The counter steps in twelves, so zero is the only reading inside
the specification. *This also asked for one session straight after a hard
drive* (20/10), dropped 23/10 at the owner's decision: what that rested
on, 014 counting only after the hard drive of 4/10, was an adaptation
completing rather than load (`refuted.md` C19).

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
(`CLAUDE.md`); the next reading of 032 is the first evidence. Also in the
window: the first tank of Orlen Verva 100 and two 170 km drives held at
5000 rpm.

**Not settled that the start set it** (*reasoned*): a start that dies at
once runs on a cold probe, open loop, and cannot itself trip a trim fault;
what would link the two is **one cause** that puts in too much fuel, seen
once at the start and once later in closed loop. **Read by what follows:**
032's idle trim well negative at the next reading, or P0172 back with no bad
start, says a standing cause rather than a one-off; P0172 back after
fills only would point at the purge path (*general*: a canister flooded by a
brim-full fill), which 070 found sound on 27/9 (`refuted.md` A6) but not
since — and 070 shows that the valve opens, not that it seals (H16).
Tonight's 001, with the stored adaptation still in force, read
**+15 to +22 %** while warming and about **−3 to +1 %** warm — adding fuel
cold, near zero warm, which a hard rich fault would not show; weak, since
it is the trim on top of an adaptation not read.

### Other — not symptoms, but they touch this file

**Oil temperature.** 0x420's `OilTemp` is `raw − 60` °C (`docs/firmware/can-decoding.md`
question 10, closed 23/10). A bias moves both sides of every comparison alike.

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
| S19 ↔ the bad start of 24/10 | **suspected one event** (*owner*) | same window, both what a cylinder flooded while standing gives (S19) |
| S11 ↔ S1 | **untested** | if the hiss is a leak, H3 or H2; the owner reads it as the throttle's own air |

**Two clusters**: **the idle** (S1, S2, S3, S14) and **the cylinder 4
window** (S4, S5). S11 sits beside the idle, unplaced.

---

## The open hypotheses

Each lists what it explains, what speaks against it, and the test that
settles it. ✔ fits, ~ fits weakly, ✘ does not fit, — says nothing.

**The columns are the open symptoms that bear on the engine**: S1, S2, S3,
S4, S5, S11, S14, S19. Left out: S16 (the gearbox side, shown not to touch
the idle) and S17 (a resonance, not placed); the closed ones are in
`refuted.md` §D.

### H0. The idle is normal for this engine — and there is no fault to find

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ✘ | — | ~ | — | ✘ | ✘ |

- **Against:** 014 reads 12–120 against VW's 0–5; the old converter burned
  through; the dips sit on 3 and 4, the cylinder of the 2019 P0304 and of the
  noisy knock window; the one cylinder the ECU has named, 18/10, is 3 (`refuted.md` D10); the inside of 3 and 4 is worse.
- **For:** no code is stored (2 % threshold: *under 2 %*, not *healthy*).

**Test:** ~~a USBtin capture of a healthy AQY~~ — **not obtainable**
(*owner*, 21/10): the bus is reached only at the cluster harness behind the
vent, and no owner will have a splice made there. What remains needs only the
diagnostic port: **VCDS on 014 at a warm idle of a healthy AQY**, 3–5 min,
loads off — whether a sound engine of this family also counts above VW's
0–5. It compares only on the same ECU (Motronic M5.9.2), and says nothing
of the grade or of the pair.

### H1. A lifter or valve on one cylinder (valvetrain)

A hydraulic lifter that bleeds down, or a valve that seats late or not quite,
on one or two cylinders. *General.* The AQY's lifters are hydraulic bucket
tappets (*hydrostely*), fed from the head's gallery through a small hole
each; inside, a plunger and a check ball hold an oil column that takes up
the lash. They fail two ways (*general*): **one that does not fill** (a
narrowed feed, air, wear) leaves lash, ticks, and opens its valve late and
short, worst hot at idle; **one whose plunger or ball sticks** with varnish
or debris holds its valve a hair open, which costs compression and misses
at a small charge and is covered by load — the case this hypothesis is
about. The valve is closed by its spring; the lifter only removes the gap.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ✔ | ✔ | — | ~ | — |

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
- **Against:** compression **13 bar in 2018 and 12 bar even on all four in
  2026** (`vehicle-history.md`) — no cylinder losing; the vacuum gauge
  steady cold and warm, no flick (H3); no ticking before 18/10, and **none on any
  drive since, through 24/10** (`refuted.md` D10) — a lifter that hung
  should not fade, and this did; the idle is never worst hot, where a thin-oil lifter
  should be; **the phone recording of 24/10, part-warm** (oil 52–58 °C):
  one click per firing, all four alike, over every injector and over the
  cover at each cylinder — no once-per-cycle sound over any lifter
  (`idle-log.md`, 24/10); the valves looked whole on 19–20/10 (which says nothing of
  sealing); 18/10 is explained by 3's flaked deposit without it.

**Tests:** a phone recording over each injector and each lifter, warm (`plan.md` 6c; the screwdriver by ear dropped 24/10); **the two EPR flushes** (`plan.md` 6a), which clean the
feed passages and the plungers' varnish — they run alongside BG 44K, so
an improvement does not tell H1 from H13; a warm leak-down (**not to be
done**, *owner's decision*, 20/10); the lifters pressed down with the cover
off. 18/10 coming back, cold, would reopen it (`refuted.md` D10).

### H2. A leak ahead of the front lambda probe (manifold, its joint to the head, the probe boss)

At idle the exhaust pulses dip below atmospheric and a crack draws air in.
*General.* The zone is only the **original manifold, its gasket to the head
and the probe's boss**: the probe sits on the manifold (`vehicle-history.md`).

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | ✔ | ~ | ✘ | ✘ | ✔ | ✔ | ✘ |

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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
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

**Test: none without dismantling.** Brake cleaner at each runner's head
joint and injector seat was the plan, and it **cannot be done in place**
(*owner*, 24/10): no room past the coil at 4, the runners of 2 and 3 out of
reach. What is left is the plenum and the lower manifold off, **the lower
gasket renewed** and the injector O-rings looked at — a repair that tests
by its result.

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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | ~ | — | ~ | ✘ |

**Tests:** the injector loom flexed at 3 and 4 at a warm idle, watching the
grade (`plan.md` 5a's loom minutes); VCDS 004 (the ECM's supply) beside 014.
VW's TSB 01-08-27 (the coil's ground wire, US sister engines) is the joint to
look at first if the spark side ever comes back.

### H5. Something in cylinder 4's knock window that is not combustion (S4, S5)

The ECU books anything at cylinder 4's crank angle to cylinder 4: G66, its
torque or connector; a loose ancillary part buzzing in a speed band; **an arc
at lead 4's plug end** (H15). Injector 4's click is settled against (B7).

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | — | ~ | ✔ |

- **Against:** four new injectors and a new filter changed nothing in S1; the
  trims near zero; full-load pulls reach ~85 kW, where a weak pump shows first;
  the regulator (7/2026, 3 bar) dry at its hose; injector tips clean on the
  borescope (19–20/10).
- **A plug washed clean by fuel** (a forum extract on the AEG/AQY, 20/10:
  *"#3 was much cleaner … replaced #3 injector as it was washing that plug"*):
  plug 3 is the cleanest here too. Weak, for the reasons above; a reason not
  to read plug soot as combustion quality.
- **For, since 24/10: S19.** A dripping injector or a regulator that does
  not hold gives a rich code and a start that floods after standing; the
  only hypothesis that predicts both. Every lean-side one (H2, H3, H4,
  H15: unburnt air reaches the probe) predicts P0171 or nothing, not
  P0172. **Since 24/10 not the only one**: a purge valve that does not
  seal predicts both as well (H16), and its test is cheaper.

**Tests:** a rail pressure gauge (**not bought**, *owner's decision*, 10/10;
VW's figures, if one is: 2.5 bar at idle, 3.0 with the regulator's hose
off, **2.0 bar or more ten minutes after switching off**, the last being
S19's question — `vcds.md`);
swap injector 3 with another if the cylinder stays named.

### H8. Idle air control and the throttle body

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | — | ~ | — | — | — | — | — |

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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | — | — | — | ~ | ~ |

**Against:** 032 + 033 near zero on a new MAF and new injectors bound a hidden
shift to a few per cent, and with the wrong sign (the ECU takes fuel out); a
shift small enough to hide is too small to misfire. **Test:** a four-gas
analyser at the emissions station, warm idle and 2500 rpm. *Not in
`plan.md`.*

### H12. Driveline play read as misfires

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | ✘ | ~ | ~ | ~ | — | ✘ | — |

**Against:** the MAF swap halved the dips; play repeats every 360°, the pairs
1+4 and 2+3, while the dips sit on 3 and 4, 180° apart; the puffs come with
the dips, and play makes no unburnt charge. **The clutch minutes** (12/10):
pedal up no rougher than down — not the gearbox side (S16). The crank
pulley's damper fine by eye.

### H13. Deposits after years of gentle driving — inlet valves, chambers, ring lands

*Added 15/10 at the owner's request.* The engine seldom saw more than
3000 rpm for at least nine years (*owner*). Gentle use builds deposits where
hard use burns them off (*general*).

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ✔ | ~ | ✔ | ~ | — | — | ~ | ~ |

- **The look inside, 19–20/10** (H13 test 3, `idle-log.md`): **no inlet valve
  back is coked** — thin lacquer on all four, so no walnut clean; **the
  chambers carry it** — thin layers on every crown, a crust on 4's bowl edge,
  and **on 3 a layer breaking up, crown and exhaust valve alike**. Ports and
  chambers rank **3 > 4 > 2 > 1**, the pair the dips sit on.
- **Consequence more than cause** (*the owner's reasoning*, 20/10): every
  cause put forward for deposits acts on all four alike, and 3 and 4 are
  worse — so their extra deposit reads as **years of poorer combustion on 3
  and 4**, from something that touches those two only (H15). Once there, the
  deposit adds to it: a flake under a seat (18/10, `refuted.md` D10), heat and compression for
  knock on 4 (S4).
- **With a cleaner in, the idle after high revs starts calm and worsens
  over minutes; without one, the reverse** (S1, *After high revs*): one capture and one display evening, so far.
- **18/10 has not come back** in six days of hard driving, a strong 44K
  tank among them (`refuted.md` D10) — what a flake that burnt off does.
  Weak: one episode, and its absence.
- **Against:** a detergent premium fuel since 2017; compression even;
  **the strong first 44K tank changed nothing** (23–24/10, *owner*): about
  450 km on it, hours above 4000 rpm, and `IdleHealth` at the warm stops
  70–80 as before (S1, the table). The owner now expects the cleaner to do
  nothing for the idle (24/10).

**Tests:** the cleaner and hard driving (a tank from 15/10, done; two tanks of
BG 44K, the second from 24/10, then a flush and fresh oil, `plan.md` 6a).

### H14. The remap of 6/2018 — the idle's ignition, or its margin

*Added 16/10 at the owner's request.* A map acts on all four alike, so at most
it narrows the margin until the weakest two show. Fuel at a warm idle is pulled
back by the lambda loop and would show in 032, which reads small.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | ✘ | — | ~ | ~ |

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

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ~ | ~ | — | ✔ | ✘ |

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
- **A once-per-cycle sound on the NGK set, none on the VW one** (*reasoned*,
  24/10, from two phone recordings): the gauge clip of 14/10 carries a
  strong component once every 720° (7.7 % of the level, steady across its
  two halves) besides an eight-per-cycle one; the recording of 24/10, on the
  VW leads, has neither — only one click per firing, all four alike. An
  arcing plug end clicks once per cycle (S18's reading). **Not a
  comparison**: other place, 924 against 810 rpm, a clip of 10 s.

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

**Read 21/10 (`40`, one drive): not the main cause** (*owner*, 21/10).
Loads off 67 ± 2 hot, **level with 12–15/10 and not better**; 014 next to
15/10; loads on and cold the calmest recorded. The least it predicted is
met, the *calmer* is not. **One thing is not yet read the same way**: the
dips spread out, top two 58 % at p 0.77 — the first capture since 11/8
where the pair does not show; but 157 dips, one drive, and `24` read
p 0.4 once before. **The upper plenum gasket was renewed the same day**, so
the leads were not the only change. **Kept, demoted**, for a share: if the
captures after item 6 keep the dips spread, the leads took the pair away
and left the level — a part, not the whole (*More than one at once*); if the
pair comes back, H15 goes to `refuted.md`.

### H16. The purge valve N80 does not seal — fuel vapour into the intake

*Added 24/10 at the owner's request.* For **the rich idle trim and S19**,
not for the idle itself. 032's idle cell has read at or below zero in
every reading since the MAF was replaced on 24/9 (−3.1, −0.8, −2.3, 0.0,
−4.7, −3.1, −6.3, −3.1 %, `idle-log.md`; the 0.0 / 0.0 of 24/10 is the
clearing's reset), while the part-load cell reads +2 to +6 %.
**Somewhere a fixed amount of fuel joins the charge that the ECU did not
meter**, and a fixed amount shows most where the air is least, at idle
(*reasoned*). Nothing in these files has said where it comes from.

**How the system works** (*general*, not from this ECU's documentation):
the tank vents into a charcoal canister; N80 sits between the canister and
the intake and is **closed without power**. The ECU pulses it open only in
closed-loop lambda control, warm, so that the probe sees what the vapour
does and the injection is corrected. A pause after the start, then pulses,
is the valve working as designed (the owner saw exactly that, 25–27/9).
A healthy engine purges at idle too, at a small rate. **A valve that does
not seal** passes vapour all the time, cold and in open loop, on the
overrun and **while the car stands**, when vapour from the canister can
settle in the intake and flood the first start.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | — | — | — | — | — | ~ | ✔ |

- **For: S19.** A rich code and a start that dies at once after four hours
  standing, in a window that holds a fill, is the textbook picture of a
  leaking purge valve (*general*). **H7 is no longer the only hypothesis
  that predicts both.**
- **For: the idle trim** negative at idle, positive at part load — the
  shape of a fixed fuel flow rather than a scale error.
- **For: the history.** P0440, EVAP, stored in 1/2018 and never repaired
  (`vehicle-history.md`). **And VW lists it**: among the causes of a low
  idle learnt value in 032, *"the activated charcoal filter solenoid
  valve permanently open"* (`vcds.md`, block 032). *(This bullet first
  read the "filler cap off at idle" of 25–27/9 as the fuel tank's; in
  these files the filler cap is the oil filler, so that test bears on
  the crankcase, H17 — the oil filler, confirmed by the owner 25/10.)*
- **Against: what block 070 found** (`refuted.md` A6): TEV OK, lambda
  deviation 0.0 %. A test that commands the valve open and reads the
  response says the valve **opens**; it cannot say that the valve **seals**
  without power (*reasoned*; exactly what that block looks for is not in the
  label summary, `vcds.md`). 0.0 % says only that the canister had nothing to
  give at that moment. So 070 refutes a dead valve, not a leaking one.
- **Against: S1 and S3.** A dip is one firing that fails and recovers in
  about a quarter of a second (S1); vapour comes through the common plenum
  to all four alike as a slow, even flow that the lambda loop follows, so
  it cannot make one firing in hundreds fail and the next succeed. **The
  dips sat on 3 and 4 for weeks** (*The dips keep to one slot*), which a
  common-plenum source cannot pick. And the size: a trim of a few per cent
  rich is far from any rich misfire limit — slightly rich burns more
  readily, not less (*general*). Load smoothing the idle (S1) fits it, but
  fits almost everything that adds charge. S14 is ~ only because a leaking
  valve feeds vapour into the intake during the overrun fuel cut, where the
  vacuum is highest (*reasoned*).

**The owner's variant** (24/10): **each pulse a slug of fuel**, from a
canister flooded with liquid that the charcoal no longer holds, and now and
then a slug that burns badly. That answers the first *Against* above in
part: pulses are not an even flow, and a slug reaches whichever intake
strokes are open at that moment, so it *could* fail one firing and not the
next (*reasoned*). What speaks against it: **on 27/9, with the idle
already rough, 070 opened the valve and lambda moved 0.0 %** (`refuted.md`
A6) — a flooded canister would have sent the probe rich at once; and the
weeks on 3 and 4 would need the purge port to sit nearer their runners,
which nobody has looked at. A canister flooded since 27/9 is not
excluded: a tank filled past the first click, or the car parked nose
uphill on a full tank, can push liquid into it (*general*). **The first
does not happen here**: the owner always stops at the first click
(25/10), the fill of 24/10 included; the slope stays. **So the hose is pinched at a warm idle with `IdleHealth` read off the
display** (`plan.md` 6e): lower while pinched, back when released, would
put the idle itself on H16.

**Tests** (`plan.md` 6e, 6f): the valve without power at a warm idle, a finger
on its canister-side port — **any suction is a leak**; then the hose to the
intake pinched for a minute at a time with 001 logged, best right after a
full fill — **lambda control rising while it is pinched** is fuel that came
through the purge. **Read:** suction → a new N80, and 032 read again after
some drives; neither shows anything → H16 to `refuted.md` on the seal test,
and the fuel is looked for elsewhere (H7).

### H17. Fuel in the oil, boiled off through the crankcase ventilation

*Added 25/10, from the owner's question* (does the extra fuel at idle
belong with the idle and with S19?) *and VW's own list.* **VW's
evaluation of block 032 for this engine puts it first**: *low learnt
values at idling with part load normal — possible oil dilution*, which
goes away after a motorway drive or an oil change (`vcds.md`, block 032).
That is exactly this car's 032 (H16 has the readings).

**The mechanism** (*general*): fuel washes past the rings while the
engine runs rich and cold, collects in the oil, and **boils off once the
oil is hot**, into the crankcase ventilation and the intake, as fuel the
MAF never saw. The ECU takes it away at idle, where it is the largest
share. **Mazda's Service Alert SA-026/18** (5/2018, NHTSA's file) gives
the pattern: many short trips, the oil level rising, **then a longer trip
fully warm and P0172**, from the fuel boiling off at once; GM's PIP5647A
(4/2020) the same picture with trims near −20 % and the cure an oil
change. ⚠ **Both are about direct injection**, and Mazda says outright
that on a port-injected engine, which the AQY is, fuel is unlikely to
reach the cylinder walls. **Both also have the oil level rising**, which
here it has not (below). They show the mechanism; for this engine the
only source is VW's own list.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 |
|---|---|---|---|---|---|---|---|
| ~ | — | — | — | — | — | — | ✔ |

- **For: S19, the code.** Since 24/9 this engine has stood through cold
  idles for minutes at a time, session after session, for the captures
  — open loop, rich, the regime that puts fuel in the oil (*general*).
  P0172 then set in the window holding **two 170 km drives with 5000 rpm
  held** and oil to 110 °C. The oil is from 6/2026, after a change three
  years apart (`vehicle-history.md`).
- **For: the idle trim**, low at idle and normal-to-positive at part
  load: VW's own wording for it.
- **Against: the dipstick** (*owner*, 24/10): the level where it was at
  the last top-up, about 1 mm over the upper mark. Fuel collecting in the
  oil raises the level (*general*), and it has not risen that far can be
  read; a millimetre is the stick's resolution, so a small dilution is not
  excluded, and the smell was not reported.
- **Against: the bad start of 24/10.** Fuel in the oil does not flood a
  start after standing (*reasoned*); if P0172 and that start are one event
  (*owner's decision*, S19), H16 and H7 explain both and H17 only the code.
  Two causes in one window are not excluded.
- **S1 ~, through a mechanism and not the size.** The ECU's correction is
  the same for all four cylinders; vapour from the breather need not
  reach all four alike, so the cylinders that get less of it end up lean
  by about the trim, a few per cent (*reasoned*). A cylinder at the edge
  of stable combustion (S1, *Load smooths it*) could be tipped by that.
  **Against it**: the idle is roughest cold, when there is little to boil
  off, and it was rough for years, through oil changes. **The change of
  6/2026**, three-year-old black oil out, **brought nothing the owner
  noticed in the idle** (*owner*, 25/10) — weak, since that was on the
  old parts with no `IdleHealth` and no 032 read either side. The same
  holds for H16's vapour.
- **How fuel would reach the oil on a port-injected engine**
  (*general*): cold, part of the injected fuel stays liquid on the port
  walls and the cold cylinder walls, and some of it is scraped past the
  rings; **a misfire** sends a whole unburnt charge into the cylinder,
  some of it down past the rings with the blow-by; a **dripping
  injector** after switching off wets one cylinder directly (H7); worn
  rings or stuck ring lands (H13) let more of all of it by. This car has
  the first two in quantity: long cold idles for the captures, and 014
  counting at them.

**Tests:** the dipstick, read 24/10 (above); **032 before the
oil change and again on the new oil** after a couple of hundred km, with
no clearing between unless 032 is read first. A trim that moves to zero
on fresh oil is VW's own confirmation; one that stays points back at H16
and H7.

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
| `40` (21/10), the first after the VW plugs and leads | 157 | **58 %** | **0.77** |
| `41` (24/10), cold, one cut on 4 | 124 | **55 %** | **0.77** |
| **pooled `40`–`41`** | **281** | **56 %** | **0.56** |

**Named by cylinder** (`--name`, `41`, the run spanning the cut, 137
dips): **1: 24 %, 3: 31 %, 4: 20 %, 2: 25 %** — all four alike, cold. Two
captures since the VW plugs and leads now say the same, against every one
before them: what acts on one or two cylinders (H3 at one runner, H4, H15's
ends on 3 and 4) loses its ground, what acts on all four (H14, H8, H1 in
general, H0) gains (`idle-log.md`, 24/10 night).

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
Most of these are already done here; the belt is not.

**P0172 and a negative idle trim on this engine** (searched 25/10, the
same languages): **no AQY thread with a reported fix.** The general
lists agree with VW's (`vcds.md`, block 032): a leaking injector, fuel
pressure too high, a purge valve stuck open, the MAF, the probe, **and
fuel in the oil** — Mazda SA-026/18 and GM PIP5647A, both for
direct-injection engines and both with the oil level rising (H17). New Beetle forum leads, unread to their end (the
pages refuse automated reading): the short vacuum hose to the fuel
pressure regulator, N80. Overfilling the tank past the first click is
named as a way to flood the canister (*general*; H16).

**Pictures of the inside of this engine family** (searched 21/10, the same
languages): **none found** that would compare — no borescope or head-off
photo set of an AQY, AEG, APK or AZJ with its mileage. The one general
reading that bears on it is ExxonMobil's borescope guide for gas engines
(*A Basic Guide to Borescopic Inspection*, §3): some crown deposit is
normal and *"should be evenly distributed. Uneven deposit distribution is a
sign for non-homogeneous thermal dissipation"* — the amount on this
engine is not judged against anything, its **unevenness, 3 > 4 > 2 > 1**,
is the finding (H13).

---

## The idle's candidates, ranked

**A judgement, not a measurement**, for S1, S2, S3 and S14. Re-read after
every test and whenever the symptom list changes; the history of each re-read
is in git.

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| 1 | **H14** the remap | the one control change never undone; narrows the margin on all four until the weakest show; **first since 24/10: the dips on all four alike on `40` and `41`**, the picture it predicts | the files, then the original map (3/11) |
| 2 | **H7** fuel delivery | never gauged; plug 3 the cleanest; **S19 fits it** (24/10), shared since with H16; one code so far | a rail gauge, an injector swap |
| 3 | **H13** deposits | 3 > 4 > 2 > 1 inside; 3's deposit coming away and 18/10 not back (`refuted.md` D10); the rise to ~100 and back to 67 follows the cleaner and the hard driving, not the parts; **demoted 24/10 from first: its own test, the strong 44K tank and ~450 hard km, moved nothing**, and the deposit reads as a consequence (H13) | the second 44K tank (`plan.md` 6a), driving |
| 4 | **H1** valve or lifter | 18/10's tick, a seat that nearly closes — on 3 one with deposit on it (H13); weakened 24/10, the tick did not come back | the phone recording over each lifter (`plan.md` 6c); the EPR flushes (6a) |
| 5 | **H2** a leak ahead of the probe | S2, S11, S14's air; cannot pick a cylinder | the warm tailpipe test |
| 6 | **H0** normal for this engine | no healthy AQY recorded; 014 far above VW's 0–5 against it | 014 on a healthy AQY, VCDS only; a capture is not obtainable |
| 7 | **H8** throttle and idle control | new since 2/10; all four | — |
| 8 | **H3** a leak at one runner | the only one that predicts *load helps* directly; the lower gasket never renewed; **demoted 24/10: it acts on one runner, and the dips no longer keep to 3 and 4** (`40`, `41`) | no test in place (the brake cleaner cannot reach, 24/10); the lower manifold off and its gasket renewed |
| 9 | **H15** the leads' plug ends | demoted 21/10: VW leads level with the best on NGK; the dips spread on `40` | whether the shares stay spread after item 6 |
| 10 | **H4** the injector loom at 3 and 4 | shared by the two, old and taped; demoted 24/10 with H3, for the same reason | flexed at a warm idle |
| 11 | **the timing belt a tooth out** | belt from 10/2017; a forum fix | its marks; even compression and the full plateau argue against |
| 12 | **H16** the purge valve leaking | here for the rich idle trim and S19, not the idle: an even flow to all four cannot fail one firing in hundreds; a slug per pulse could, and 6e asks (H16) | the pinch off the display, then the seal test (`plan.md` 6e, 6f) |
| 13 | **H17** fuel in the oil | VW's first cause for this car's 032; the oil level has not risen; here for the trim and S19's code, not the idle: roughest cold, when there is nothing to boil off | 032 on the new oil (`plan.md` 6g) |
| 14 | **H11** both probes shifted | 2017 probes | a four-gas analyser |
| 15 | **H12** driveline play | — | done: the clutch minutes cleared it |

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
time, readings only where they decide the next step, as little idling as
possible. The tests above are reference, not a schedule.

**A higher idle was tried, 12/10, and does not help**: raised to 830 rpm
specified (VW's procedure, login 01283), 014 kept counting and `IdleHealth`
rose slightly; put back the same day (`refuted.md` D9).
