# The idle log — chasing a rough idle and misfires on a VW 2.0 AQY

**A diary of one investigation, kept for the owner looking back and for
anyone with the same engine and the same complaint.** The forums hold many
threads about an AQY that idles unevenly and counts misfires, and most of
them end unresolved (`open.md`, *What the forums say about this idle*). This
one records what was believed at each point, what was done, what was
measured, and — just as much — **what nobody can say for sure a repair
achieved**.

It covers the two symptoms that matter here, **S1** (the idle is unsettled)
and **S3** (the ECU counts misfires at idle). Other faults appear only where
they crossed this path. Where things stand **now** is `open.md`; what comes
next is `plan.md`; what was settled against is `refuted.md`; the car's
service record is `vehicle-history.md`. This file is the story between
them, and it is kept current until the idle is fixed — then it stays, as
reference.

**How to read it.** Each stage gives the picture *at that time* (which
was sometimes wrong, and says so), what was done, and what it showed.
Procedures are not repeated; `git log` has them. ⚠ **A repair followed by a
better idle is not proof that the repair fixed it** — several were done
together, adaptations were reset along the way, and the instruments changed
twice. Each stage says how sure it is.

---

## What is being chased, in one picture

![One idle dip](dip-profile.svg)

*Added 11/10/2026, at the owner's request, as the preamble to everything
below.* At a warm standing idle, every few seconds, **the engine speed
falls by twenty-odd rpm in two strokes and climbs back in about a fifth
of a second.** The picture is the average of four hundred of them, read
off the CAN bus; the details are in `open.md` S1, *One dip, read stroke
by stroke*.

What it shows, in plain words:

1. **Half a second before**, the idle has crept a few rpm too high, and
   the ECU does what it should: it takes a little air and fuel away —
   about one per cent.
2. **Then one combustion fails or nearly fails.** The crank loses speed
   over two strokes.
3. **The ECU notices at once** and adds fuel, air and advance; the idle
   is back within about five strokes and overshoots slightly.

**The ECU is not the fault**: it regulates correctly and in time. **The
engine is**: a charge one per cent smaller than usual — well inside the
range the idle control always works in — is enough to make it misfire.
A healthy engine has the margin for that and this one does not. **Where
the margin went is the question this whole diary is about**, and it is
still open. It is also why the engine is fine under load (a bigger
charge, more margin), and why the ECU's own misfire counter (014) sees
only some of these dips — it is switched off at the lightest load and
counts in steps of twelve.

---

## The car, the symptoms, and the instruments

**The car.** VW New Beetle, 2.0 l **AQY** (85 kW), ECU `06A 906 018`,
model year 2000, bought in 9/2017 at 126,200 km and driven little since.
**Remapped in 6/2018**, described by the owner as mild; not undone so
far — the tuner kept the original, to be written back on 22/10/2026 (*owner*, 13/10). The engine warning lamp had been masked by a previous
owner and was restored in 2017.

**S1 — the unsettled idle.** At a standstill the engine speed dips by 20–45
rpm every few seconds and recovers in about a quarter of a second. Felt from
the seat. **It depends on temperature:** roughest cold, calmer as the oil
warms, calmest hot. *(This read "not simply: … worst at about 71–85 °C of
oil" until 9/10/2026; the middle-band peak was 014's, sharpest on fresh
adaptations, and engine speed never showed it — `open.md` S1.)* A reading without the oil
temperature beside it compares with nothing.

**S3 — misfires counted at idle.** VCDS group **014** field 3. Three
properties of this counter were learned the hard way and matter to anyone
reading their own:
- it is a **current count**, not a lifetime total, despite its label — it
  holds a value about 3 s and returns to zero;
- it **moves in steps of 12** (12, 24, 36 …), not by single misfires;
- the label file gives **0–5** as the specification, and this car reads
  12–120;
- detection reads `deaktiv.` below about 20 % load — which on this car is
  right at the hot idle;
- and **what it counts changes with the air measurement and the
  adaptations** (the MAF swap of 24/9 and the learned idle air of 4/10,
  below). **It is a yes/no witness, not a ruler.**

**The instruments.**
- **VCDS** on a laptop: 014 (misfires), 003 (air mass, throttle angle),
  055 (idle regulator and its learned value), 032 (lambda adaptations),
  033 (live lambda control), 004 (intake air), 020/022/023/026 (knock).
- **A CAN capture** of the powertrain bus (USBtin, listen only, the
  adapter's own timestamps) — engine speed once per 180° of crank, one
  value per firing, which makes each dip one cylinder's stroke.
- **`IdleHealth`**, a grade this project computes from those firings —
  the mean change of engine speed from one firing to the next, small
  changes ignored — shown on the dashboard display and recomputed from
  captures. **Its 100 is two recordings, not an average over driving:**
  the 60 s warm idle of 11/8 at 85 °C of oil (`09`) and the cold start's
  five-minute warm-up of 11/9 (`18`), both on the old parts, both
  2.12 rpm, rounded to 2.00 for the arithmetic. Lower is smoother. So it
  measures against **the middle band and the cold idle before the
  repairs**, not against the hot idle, which was already better then;
  and **dips ≥ 20 rpm a minute** from the same data
  (`tools/idledips.py`). **Neither reproduces 014**, and why is
  `docs/firmware/open.md` question 11: they measure smoothness, 014 is the
  ECU's own per-cylinder judgement.

---

## Before September 2026 — the history

- **1/2018** — fault memory (*owner's old scan*,
  `photos/vcds-faults-2018-01.png`): **16824 / P0440, EVAP system,
  intermittent** — never repaired; not seen since.
- **5/2019** — fault memory (*owner's old scan*,
  `photos/vcds-faults-2019-05.png`): **16556 / P0172, too rich**,
  **16684 / P0300** and **16688 / P0304, cylinder 4 misfire**, all
  intermittent. Codes this ECU stores only above a 2 % misfire rate
  (`vcds.md`), so cylinder 4 was misfiring well past today's counts
  then; and rich, a year after the remap and the 2018 MAF. *(This read
  "the MAF that over-read until 9/2026" until 11/10/2026: that MAF was
  found over-reading only on 24/9/2026, and read near zero in August —
  `refuted.md` C2. What made 2019 rich is not known.)* Not seen again
  in any scan since.
- **6/2018** — remap. **12/2017** — fuel filter changed; the old one came
  off corroded and leaking, with dark, cloudy fuel in it (photographed).
  The fuel tank was replaced at some point in the ownership; when is not
  recoverable.
- **The idle had stumbled for years**, alongside a poor cold start and, on
  a cold engine coasting downhill, fuel heard burning in the exhaust.
- **6/2026** — new ignition coil, after a misfire under full load (gone
  since).
- **About 6/2026, before the repairs began** (*owner*, recalled
  16/10/2026): **every start ran on three cylinders** at first; it turned
  out to be the old fuel (about three years in the tank, `refuted.md`
  A14) and went with fresh fuel. **Which cylinder is not known** — no
  scan from then was kept. *Reasoned*, two readings, not exclusive: the
  cylinder with the least margin fails first when something takes margin
  from all four, which fits the dips sharing out unevenly today
  (`open.md`, *One cylinder or two*); or those starts left deposits from
  the stale fuel on that cylinder's inlet valve and chamber, which is
  H13 and what the cleaner in the tank is for. A history, not a symptom:
  fresh fuel ended it. Throttle body inspected: already clean.
- **7/2026** — new fuel pressure regulator; MAF connector cleaned.
- **Summer 2026** — heater replaced with the dashboard out; **the battery
  was off for more than a week**, so every adaptation restarted. A small
  secondary-air hose was torn off in the work (fault P0411, 11/8), and
  refitted.
- **11/8** — the first captures (`09`, `11`, `12`). The hot idle graded
  **43–48** (29 with the A/C on); at 85 °C of oil 15 dips a minute. Before
  the September work 032 read **−4.7 % / +1.6 %**.

**The picture then:** a leaking injector. A fixed dribble matters most where
there is least air — idle — and fits a slightly rich idle trim.

## 10/9 — the blocked converter

The car came back from a garage with the exhaust replaced **from the flex
pipe back**: the converter of 10/2017 was **completely blocked, cracked
outside, one chamber burned through**. A few per cent of rich trim does not
do that; raw fuel burning in it does — misfires. **The one hard fact of the
whole investigation**, and why it was taken seriously.

## 11/9 — a cold start recorded, on the old parts

`18_coldstart_z1`, with 014 + 055 beside it. The start: **1.24 s of
cranking, first firing at 451 rpm, a fall to 311 rpm, nearly died.**
- **The dips and the 014 increments were the same events** (all seven
  increments beside a dip, p = 0.023). So the felt stumble and the counted
  misfire are one thing.
- **No single cylinder dominates** the roughness (a per-cylinder spectrum of
  the 180° values; `refuted.md` A5). What it cannot show is all four being
  equally bad.
- 014 counted at a cold idle: values to 36, steps of 12.

## 17/9 — plugs, leads, compression

At a garage, because the injectors had not yet arrived: **new plugs and NGK
leads**. The old plugs were worn out after about 1,500 km, one visibly
worse — **from which cylinder is not known**, they were not labelled.
**Compression 12 bar, even on all four** — which rules out a burnt valve,
broken rings or a head gasket between cylinders (`refuted.md` A4), though
not a valve that seals cold and not hot. The owner felt the idle a little
calmer; nothing measured it (`refuted.md` C12: a warm idle had counted
zero dips before anything changed, so an impression there has nothing to
be calmer than).

## 23/9 — new injectors and fuel filter

By the owner: four new Bosch injectors (the same part as the old), new
filter, the lines flushed — **clear petrol throughout**. The battery off
for the work. **The old injectors were never leak-tested**, so whether one
was dribbling is not known. ⚠ *Found later (27/9):* **three of the four
new ones sat about 1 mm proud** of their bores — a possible air leak at the
seats, from this day until 1/10.

Afterwards: no fault codes; the idle "not fundamentally different".

## 24/9 — the post-repair drive, and the MAF

Morning drive (`19`) on all the new parts: **the car pulled better; the
misfires stayed.** And 032 went to **−16.4 % / −13.3 %** — a large, nearly
equal correction at idle and part load. The shape said *multiplicative*:
the air measured too high, or too much fuel per millisecond, everywhere.
Air per commanded fuel had risen 14–45 % since August.

**Afternoon: the MAF replaced** (a genuine VW unit for an insert of 2018).
**032 settled at −3.1 / +4.7 %** and the air-to-fuel ratio returned to
August's: **the old MAF was over-reading that morning** (`refuted.md` C2;
*"had been over-reading" until 11/10/2026* — since when is not known).

- **Confident:** the rich trim was the MAF.
- **The idle got smoother on engine speed** — dips at a standstill fell
  51–65 % in every oil band.
- **But 014 counted *more*** at the hot idle. **The counter, not the
  engine**: on the new MAF it counted five to fifty times more per dip
  (`refuted.md` A11). Reasoned: this ECU's misfire threshold depends on
  load, which it computes from the MAF.

*Read again 11/10/2026* (`refuted.md` C2, *What the bus says*): the
old MAF read **about a third high on the hot idle after the pulls** —
the same fuel per stroke, the same throttle, more air on the gauge — so
it drifted with heat. August's captures read
normal, but none of them has a hot idle after hard driving.

**Lesson for anyone else:** after changing the MAF, do not compare 014
across the change.

## 25–27/9 — testing everything cheap

The idle was still rough and every part in the fuel and ignition path was
new. A round of tests that cost nothing:

| test | result |
|---|---|
| knock retard per cylinder (022/023), and 026 | none at idle; **knock is not the idle fault** (`refuted.md` A10). Cylinder 4 retards at higher speeds — a separate matter (`open.md` S4/S5) |
| secondary-air valve and N112: hoses pulled at idle | the valve seals; pulling the N112 line at idle did not change `IdleHealth` (A8) |
| evaporative purge (070) | OK (A6) |
| supply and earths: coil connector, earth points, voltages under load | no gross fault; electrical weakened as a cause (`open.md` H4) |
| **spray test at a warm idle** — the front hoses, the MAF-to-throttle hose | **no change**; but the back of the intake, the injector seats and the throttle joints were **not** sprayed |
| loads on at idle (A/C, lights, blower) | **`IdleHealth` down from 70–80 to 35–50** — the idle is rougher the lighter the load |
| filler cap off at idle | the idle audibly slightly worse |
| oil at the back of the head, smoke and possibly a hiss over the manifold | new symptoms then: the valve cover gasket (S10), the hiss (S11) |

**The picture at the end of 27/9** (`open.md`, ranked candidates): first, **a
small unmetered air leak** — the proud injector seats, the back of the
intake, the breather — because it is the only cause that predicts *load
helps*; then "normal for this engine" (nobody has a healthy AQY recorded);
a valve; rail pressure; the throttle body; the electrics; an exhaust leak
ahead of the front probe.

**The owner's question that week:** did anything after August make the hot
idle worse? On the same old MAF, the hot idle roughly doubled its grade
between 11/8 and 24/9; the new MAF took back about a third. The list of
everything changed in between is in `open.md` S1. **The proud injector
seats were the strongest suspect.** It was never proven.

## 1–2/10 — the valve cover, throttle and breather job

One job by the owner's decision, so the engine was opened once — **at the
cost that an improvement could not be put down to one part.**

- **Injectors refitted** one by one, all four clicked home (one O-ring
  damaged and replaced).
- **New valve cover gasket** (⚠ it turned out to be the wrong part — 3/10),
  new upper plenum gasket.
- **New breather** — the old one sat loose on a ring that had flowed out of
  shape.
- **New throttle body** — the old one's idle-stop face was worn 1–2 mm
  smaller; 098 adaptation OK.
- Found: six of eight cover nuts loose by hand over a gasket gone hard;
  the throttle's vacuum elbow hard with age.
- Battery off again: every adaptation from zero.

## 3/10 — session A: still counting, and the cover leaks

A cold start after 27 h (0.77 s crank, a clean start), a warm-up drive,
stops at warm and hot oil.
- **014 still counted** at the warm stops — 16–17 a minute at 57–92 °C of
  oil, about as on 24/9.
- On engine speed, **mixed**: about as rough as 24/9 or rougher in the
  middle band, smoother at the one hot stop — which was only about a minute
  long.
- **The new cover gasket leaked a stream of oil** at cylinder 4's end by
  the first warm stop, down to the coil. That night, with the cover off:
  **the gasket was for another engine** — an open arch where this head has
  a solid half-moon, leaving a hole of about 1 cm into the crankcase.

**Not known:** how much of 3/10's counting was that hole. It was open the
whole session.

## 4/10 — the right gasket, then two sessions

**Morning:** the right gasket (Elring `915.653`) on, the battery off again,
098 run. **Session A on fresh adaptations:**
- the joint **stayed dry**;
- **014 read zero at both warm stops — the first time ever**, at oil
  temperatures where it had always counted;
- the hot idle was **the smoothest since August** by both grades
  (`IdleHealth` 60–72, 4.4 dips a minute), and the owner felt it calmer.
  ⚠ Not the smoothest on record: August's one hot hold graded **48** — but
  it lasted 22 s, too short to compare like with like;
- **then, after five minutes of hard driving, 014 counted at every idle.**

**Afternoon, session B** after a cool-down: **014 counting again** — at the
middle stop as on 3/10, and even on the idle straight after the start,
which no session had done before. The live lambda control (033) did not
correct toward rich, which an exhaust leak at the front probe would force.

**What the two sessions showed together** (then `open.md` H10, closed 9/10/2026 as `refuted.md` C19): 014 followed
**055's learned idle air value**, not the heat. From zero after the
disconnect it walked negative as the engine ran; **while it was above about
−0.93 g/s, 014 read zero; from −0.95 on, it counted — warm or cold.** The
hard drive was simply where it crossed. A learned value walking negative is
the ECU learning to let *less* air past the throttle at idle — what it does
when air arrives that the throttle did not let in.

**How sure:** one day, two sessions — a correlation in time. 3/10 does not
fit (it counted at −0.28, with the hole open).

**What changed, and what nobody can say:**

| change | sure it helped? |
|---|---|
| the MAF, 24/9 | **yes** — the rich trim, and the idle smoother on engine speed |
| the job of 1–2/10 | **not shown.** *This read "probably, for smoothness at the hot idle": about 9 dips a minute (24/9), 5 (3/10, a one-minute stop) and 4.4 (4/10).* Both calm hot stops were on fresh adaptations; on settled ones (4/10 B, 9/10) the hot idle is back where the MAF left it (*corrected 9/10/2026*, `open.md` S1). The middle band did not move |
| the right gasket, 4/10 | **for the oil, yes.** For 014: the zero of session A came on fresh adaptations, and session B counted again, so **not shown** |
| the plugs, leads, injectors, coil | they did not fix the idle; the old injectors probably caused the bad cold start, which is gone. *This also said "and the cold burble"; that came back on the new injectors, warm, 4/10 (`open.md` S14)* |

The owner's honest note at the end of the day: the morning's "calmest idle
yet" was measured against the noisy 3/10 (a belt that had probably rubbed on
its cover with the cover sitting low) — and the grades agreed with that
reading rather than with a wish.

---

### `IdleHealth` against its own 100, 4/10/2026

*The owner's question: the 100 is "before the repairs" — measured the same
way now, has it moved?* The whole-stop mean step, in the conditions the
100 was taken in and beside them:

| state | before the repairs | 24/9, new MAF | 3/10 | **4/10** |
|---|---|---|---|---|
| middle band, ~77–87 °C of oil | **2.12 rpm (`09`, 11/8)** | 1.67 (72–85 °C) | 2.22 (81–91 °C) | **1.95** (A2), **2.14** (B1) |
| cold idle, the first five minutes | **2.16 (`18`, 11/9)** | — | — | **2.42** (A1) |
| hot, ~97 °C | 0.96 (`11`, 11/8, a 22 s hold) | 1.85 | — | **1.44** (A3) |

As an index (÷ 2.00 × 100): the middle band 106 → 98–107, the cold idle
108 → 121, the hot idle 92 on 24/9 → 72 on 4/10.

**What it says, plainly:**
- **Against its own 100, the idle has not measurably improved.** The
  middle band reads within a few per cent of the August recording; the
  cold idle reads a little worse than the cold start of 11/9, which was on
  the old injectors.
- **The hot idle improved against 24/9** — the morning after the
  injectors and the MAF — **but not past August's**, which was one short
  hold.
- So the calmer idle the owner feels on 4/10 is real *at the hot idle* and
  *against the week before*; it is not a return to a better engine than
  August's. *Corrected 9/10/2026:* and it did not last — it came on fresh
  adaptations, and on settled ones the hot idle reads as it did after the
  MAF (`open.md` S1).

---

## Where it stands, and what comes next

**Open:** S1 and S3. The misfires remain on settled adaptations, with
new plugs and leads (10/10, below), and the intake is tight cold. The
dips that kept to one cylinder's stroke did not keep to one on the first
drive after the new leads, and fewer came. **Next** (`plan.md` step 3):
the exhaust test found nothing cold, the gearbox side is cleared and the
idle raise did nothing (12/10, below); nothing more
until the vacuum gauge arrives (*owner's decision*, 10/10), and the
gauge on a cold start of its own; unless it shows an intake leak
plainly, the engine is left alone and a tank is run with a PEA
inlet-valve cleaner, read on the drives after. **14/10: the gauge cold
read steady and normal**, **15/10 warm the same** (below), and the can
went in on 15/10; the tank is now driven, `IdleHealth` read off the
display, until the original map goes back on 22/10.

*Entries are added here as each step is done.*

**9/10/2026 — the exhaust joint behind the converter, resealed** (*owner,
photographed*: `photos/exhaust-joint-2026-10-09-old-parts.jpg`,
`photos/exhaust-joint-2026-10-09-new.jpg`). The joint the garage had
filled with sealant on 10/9, and that had rattled since, was taken apart
and remade with a two-bolt sleeve connector and exhaust sealant. A little
play remains — one pipe is about 1 mm narrower (*Corrected 12/10/2026* (*owner-measured*): the narrower pipe is **the one from the converter, 54.2 mm**; the one from behind is **55.0 mm**; this said the pipe behind was the narrower.) — which the sealant
is expected to take up; a reducing connector if not. **Done for comfort,
not for the idle**: the joint is behind both lambda probes, so it cannot
have touched the mixture, the trims or a misfire, and **nothing is
claimed for S1 or S3**. What it can say is about S2 and S14: a puff or a
bang that goes on unchanged after it was not fed by this joint. S6 closed
at the owner's decision (`open.md`).

**9/10/2026 — the dipstick guide renewed** (*owner, photographed*:
`photos/dipstick-2026-10-09-*.jpg`). The old orange guide was loose at
its foot and turned out not to be this engine's part, its mounting tab
in another place — perhaps why the bracket was gone. The metal tube
was fully home in the block. The new one clicks onto it and holds; the bracket is a strip of sheet metal
bolted to the head, the guide cable-tied to it. **Done so that the
smoke test can read the dipstick, not as a cure**: the crankcase path it
closed is a small one, behind the breather's valve (`open.md` H3), and
**nothing is claimed for S1 or S3** until a session measures it.

**9/10/2026 — the intake smoked, cold** (*owner, photographed*:
`photos/smoke-intake-2026-10-09-*.jpg`). The test the investigation had
wanted since 27/9: smoke into the manifold, the MAF out. **The back of
the intake — the plenum, the injector seats, the hoses no spray had
reached — showed nothing.** The one leak was at the dipstick, where the
new guide seats on the metal tube: a crankcase path, the smallest kind.
The plug in the hose leaked most, which was the test and not the car.
The airbox's outlet, the throttle, the filler and the cover joint were
clean. **The dipstick was a real stream; the guide was reseated and the
bracket bent to press it down, and smoked again it gave only a faint
wisp** — the same day.
⚠ Cold and stopped, so a joint that opens only hot is not cleared; and
it **does not show** that the leak found had anything to do with the
misfires. The drive of 2b will say.

**Then the intake again, the old MAF in the hose** so that it held
pressure on its own joint: the dipstick now clean, and **smoke at the
MAF-to-hose joint under the owner's rubber-lined clamp** — or at the
glove and rag closing the MAF's end beside it; the photo cannot tell
(`photos/smoke-intake-2026-10-09-maf-clamp.jpg`). A leak there would be
air behind the MAF. **With a narrower all-metal clamp it smoked clean**,
so the joint is tight now; whether it leaked before cannot be told —
the owner thinks the old clamp pressed in the wrong place.

**9/10/2026 — the exhaust smoked, cold.** No smoke anywhere, but it
would hardly take pressure, so it says little. A leak ahead of the
probe (H2) is neither found nor ruled out.

**Where that leaves the idle:** the intake tight cold everywhere, two
possible leaks behind the MAF closed on one afternoon. **The next drive,
with the adaptations kept, is the first that can show whether either
mattered** — nothing is claimed until it has. The car went back together the same
day with the new MAF, the regulator's hose and nothing left in the duct
(*owner*).

**9/10/2026 — the drive on kept adaptations (steps 2b and 2c)**
(`30_step2b_z1`; `open.md` S3, *Steps 2b and 2c*). The first session in
which nothing had been reset, so a zero would have meant something.
**There was none**: 014 counted on the cold idle after the start, at
both warm stops (6.8 a minute at 79–85 °C, 11–12 at 94 °C) and on the
way home. 055's learned value sat at −1.1 to −1.3 throughout and never
rose; 003's air and plate at a warm idle were 4/10's to the decimal;
032 read −2.3 / +5.5 % afterwards. **So the dipstick guide and the MAF
clamp did not fix the idle**, and nothing says they let in the air the
ECU is learning away. On engine speed the idle is where 4/10 left it.
The owner felt it calmer at A2; the grades do not show that.

The same drive answered the knock window: with all four injectors home,
the retard and 026's excess **stayed on cylinder 4** (S4, S5), so the
injectors are cleared from it (`refuted.md` B7). With no link found
between the window and the misfires, it stays out of the plan (*owner's
decision*, 9/10/2026); G66 is a test in `open.md` H5, not a step.

**Heard on the same drive** (*owner*): no puff (S2) and no bangs on
the unblipped downshifts (S14) — possibly the joint behind the
converter feeding them, possibly a tighter exhaust muffling them; both
kept open. And, newly audible now that joint is quiet, **a constant
sputter close behind the engine at every load**, added as S15 — H2's
zone, so the tailpipe test moves to the front of step 3.

**9/10/2026, evening — the brake servo, checks a and b** (*owner*).
The one part of the intake the smoke could not reach, since its check
valve shuts against smoke from the manifold. The pedal sank at the
start, and after switch-off gave one or two light presses before going
hard: the servo assists and holds vacuum. A leaking diaphragm is not
shown by these alone; check c, the pedal held at a warm idle with a
capture, is the one that would see it.

**What the drive is not known to have achieved:** anything. It changed
nothing on the car; it measured the 9/10 work, and that measured as no
change at idle.

**9/10/2026 — H10 closed at the owner's decision** (`refuted.md` C19).
With 014 counting straight after a cold start on kept adaptations, as it
never has on fresh ones, the owner took the learned idle air value as
settled: it says **when** 014 counts, not **why** — a correlation
accepted, never tested by a battery disconnect. It changes nothing on
the car and leaves the fault where it was; what it leaves behind is a
rule: a quiet 014 after a disconnect is not a repair until the learned
value has walked back past about −0.93 g/s. The leak ahead of the probe
(H2) is now the first candidate.

**9/10/2026 — every session since the repairs, compared like with like**
(`open.md` S1, the table under *Owner, 4/10/2026*). By oil band and with
the adaptations matched, **the MAF of 24/9 is the only repair that shows
on engine speed.** The calmer hot idle of 3/10 and 4/10, credited until
today to the job of 1–2/10, came both times on fresh adaptations, and on
settled ones it is gone — the same thing 014 does. So neither the cover,
the throttle, the breather, the gasket, the dipstick nor the clamp is
known to have changed the idle; the gasket did fix the oil. One hint
left: 9/10's cold idle read calmer than 3/10 and 4/10, too few windows
to carry.

**9/10/2026 — the dips keep to one cylinder.** Looked for once more at
the owner's question, as events this time rather than as averages: in
every idle capture since August, two dips close together fall on the
same cylinder's stroke far more often than chance — 36 % of pairs against
25 %. Roughly half the stumbles come from one cylinder (or from two
neighbours in the firing order). Which one, the bus cannot say; cutting
injectors 1 and 4 in turn can, and that is now `plan.md` step 3.3. It
moves the suspicion from what acts on the whole engine — the exhaust
ahead of the probe among them — to what acts on one cylinder: its
runner, its valves, its plug and lead (`open.md`, *The dips keep to one
slot*).

**10/10/2026 — new plugs and leads, and a new intake gasket** (*owner*,
photographed and numbered by cylinder; `vehicle-history.md`). NGK
`RC-VW254` leads and NGK `BKUR6ET-10` plugs — the plugs the same type as
the old ones, so what really changed is **the leads** and **the upper
intake gasket**, which had to come off to reach them. The battery stayed
connected, so the adaptations stayed settled. The old parts named two
single-cylinder faults after the fact: **lead 4's plug end** scored
inside, its terminal out of sight, over **plug 4's pitted terminal**;
and **plug 1, almost loose** — cylinder 4's 360° partner (`open.md` H4,
1d). Every old plug end came off far more easily than the new ones go
on.

**10/10/2026 — the drive after, the servo held, injectors 1 and 4 cut**
(`31_step4_drive_z1`, `vcds/vcds-step4-*.csv`, `vcds-step5-*.csv`;
`open.md` S3, *The drive after the new leads*). One session: a cold
start, the servo held twice on the cold idle, stops at 81–84 °C and
96–97 °C of oil, the cut test on the hot stop, home.
- **The servo: no dip.** The pedal is on the bus (0x1A0), so the holds
  are timed exactly: 813 rpm held, 813 released, 806 on the second hold,
  the drift of the warm-up; 003's air did not rise. All three checks
  good — the servo is cleared (`open.md` H3).
- **014 still counts**: 3.6 a minute on the cold idle (9/10: 1.4–1.8),
  9.4 at 81–84 °C (6.8), 6.0 at the hot stop (10.7–12.5), 3–6 on the hot
  stops home (3.7–5.8). Better at one stop, worse at another — **not
  fixed**.
- **The dips no longer keep to one slot**: 10 of 39 pairs, 26 % against
  chance's 25 % (9/10: 34 of 103, 33 %) — and there are far fewer of
  them. One drive is a direction, not a verdict.
- **Nothing a sealed runner would show moved**: 003 at the hot idle
  3.08 g/s (9/10: 3.12); 055's learned value −1.14 to −1.29, so the
  adaptations are the settled ones the comparison needs. The engine-speed
  `IdleHealth` by oil band: calmer hot (77 against 89), the same in
  the middle, rougher cold (120 against 95).
- **The cuts named no cylinder** (one day, cuts of 47–73 s): dips by
  name 1: 0, 2: 7, 3: 11, 4: 2, p = 0.28; the air with 1 out and with 4
  out the same (3.52–3.58 against 3.46–3.58 g/s), so neither 1 nor 4 is
  a steadily weak cylinder. With so few dips the test could only have
  found a cylinder carrying most of them.
- **020: cylinder 4's retard nearly gone** — 3 of 1,841 samples, at most
  1.5°, against 44 of 800 and up to 13.5° on 9/10 — and fewer at every
  load band, not only at full load. The owner, watching it, saw none
  where on earlier days he saw it regularly. A gentler drive than 9/10's
  pulls, so a direction (`open.md` S4).

**What it is not known to have achieved:** the misfire count did not
fall, so **the new leads did not fix S3**. What may have gone with lead
4 or plug 1 is the one-cylinder share of the dips; two or three more
drives say whether that holds, and the intake gasket changed the same
day, so even then it cannot be split between them.

The fault memory after the cuts held the test's five codes and nothing
else — P1237/P1240 for the pulled connectors, P0301/P0304 and P0300 —
so the ECU named the two cut cylinders and no other (`open.md`, *Naming
the cylinder*; `photos/vcds-faults-2026-10-10-after-cuts.jpg`). Cleared.

**10/10/2026, evening — no work on the car; the idles read again, and
decisions** (*owner*). The vacuum gauge was ordered (MAR-POL `M57673`),
the engine is to stay unstarted until it comes, and its test is merged
with the exhaust test into one cold session (`plan.md` step 3). The
fuel pressure gauge is **not** bought: low rail pressure would show at
full load first, where the engine is well, and a steady error would
show in 032 (H7, down to 5). Both lambda probes reading wrong together
is written down as H11, last. Every warm idle since 24/9 read again
with a new tool (`tools/dipcontext.py`; `open.md` S1, *What comes before
a dip*): **a dip is more likely just after the idle governor has
trimmed the charge** — less air or advance, the mixture unchanged — so
one or more cylinders run at the edge of firing at the idle's charge,
which is "load helps" (26/9) seen within a second. It names no part. A
reading of it as short runs on one cylinder, pointing at a hanging
valve, did not survive a closer look at the same day. **What it is not
known to have achieved:** nothing was changed; it weakened the causes
that do not care about the charge (H4, H7's harness) and left the
order of the rest as it was.

**10/10/2026 — the joint behind the converter heard again** (*owner*):
the remake of 9/10 did not hold — the pipe from the converter is 54.2 mm
(the one behind 55.0; *corrected 12/10/2026*, this said the pipe behind) in a
55 mm connector and moved in it even tightened. S6 reopened; a shim
under the connector is the owner's fix, and the exhaust test waits on
it. Nothing for the idle either way: the joint is behind both probes.

**12/10/2026 — the joint behind the converter shimmed; the exhaust
photographed from below; a new air filter** (*owner, photographed*;
`vehicle-history.md`). No engine run.
- **The joint** (`photos/exhaust-joint-2026-10-12-*.jpg`): apart, a
  strip cut from the old connector (probably galvanised) wrapped round
  the narrower pipe, the one from the
  converter (54.2 mm; the one behind is 55.0, *owner-measured*), sealant under and over
  it, the sleeve connector back on. **It holds and nothing moves**, and
  the rubber hangers are fine (*owner*).
  Whether it is quiet is read on the drive (`plan.md` item 1).
- **From below, cold** (`photos/exhaust-flange-2026-10-12-below-*.jpg`,
  `photos/manifold-2026-10-12-*.jpg`): the joint from the manifold to
  the front pipe, with its spring bolts, and cylinders 3 and 4's pipes.
  The owner sees nothing wrong at the joint; the pipes are original and
  rusty outside, and a hole cannot be told from there. In Claude's
  reading no clear black soot trail shows anywhere photographed. One
  close-up of a dark rough surface with a crack-like line is **probably
  the driveshaft** (*owner*; `photos/driveshaft-2026-10-12-below.jpg`),
  not the exhaust. Cylinders 1 and 2
  and the joint to the head stay unseen.
- **The blanked boss is an old probe with its leads cut off**
  (`photos/exhaust-blanked-boss-2026-10-12.jpg`), behind the front
  probe, so not in H2's zone. The rear probe's cable re-routed clear of
  the floor.
- **The crank pulley, engine off** (`photos/crank-pulley-2026-10-12.jpg`,
  partly legible `…105 243 F` cast in): **fine by eye** (*owner*); in
  Claude's reading no crack or bulge shows in the rubber ring and the
  outer ring sits in line, as far as a photo can say. Also photographed,
  the three-bolt pulley beside the A/C compressor, `038 145 255 A` cast
  in (`photos/pulley-038145255A-2026-10-12-*.jpg`), and the ribbed belt
  over it: nothing seen.
- **A new Bosch air filter**, and **a crack in the airbox**, ahead of
  the MAF, sealed with putty (`photos/airbox-crack-2026-10-12-sealed.jpg`;
  the old element, `photos/air-filter-old-2026-10-12-*.jpg`).

**What it is not known to have achieved:** nothing for the idle. The
joint is behind both probes, and the airbox crack is ahead of the MAF,
so the air through it was metered — neither can have moved the mixture
or 014. The photos clear nothing ahead of the probe on their own: the
exhaust test is what reads it.

**12/10/2026 — the exhaust test cold, the clutch, and the idle raised
and put back** (`32_step3_item1_z1`, `vcds/vcds-step3-1-*.csv`;
`plan.md` step 3 item 1). One session on kept adaptations: a cold start
at 10.5 °C of coolant, the exhaust test on the cold idle, the clutch
cold, a 9 min drive to 95–97 °C of oil, the clutch warm, 3 min of warm
idle on 001, then the idle adaptation, engine off.
- **The exhaust test, cold: nothing** (*owner*, from his two phone
  recordings): five closures by the manifold and five under the car by
  the front pipe; no hiss or puff at any of them, only the exhaust being
  throttled. Claude cannot hear the recordings; this is the owner's
  reading. H2 is not refuted by it — a crack in cast iron may open only
  hot — so the warm test stays in `plan.md` item 7.
- **The joint behind the converter: not heard on the whole drive**
  (*owner*). S6 closed (`open.md`); the bolts are tightened once more
  cold. **The sputter close behind the engine (S15) has gone with it** —
  the owner's reading is that it was that joint; S15 closed at his
  decision, to reopen if it is heard again.
- **The hiss at the back of the engine (S11) closed too** (*owner's
  decision*): not heard since 10/10, and no smoke at the engine; the
  owner puts it down to the valve cover or the breather. To reopen if
  heard again.
- **The clutch makes no difference to the idle**, cold or warm. The
  `IdleHealth` (30 s halves from the blip's
  drop) cold, oil ~44 °C: down 145, up 135, down 145, up 126; warm,
  oil 97 °C: down 83 (still settling from the blip), up 57, down
  45, up 50, down 58, up 51. Pedal up is not rougher — if
  anything the reverse — so the gearbox input shaft and the clutch disc
  are not where the dips come from (`open.md` H12). The flywheel and
  the pulley turn either way and stay unseparated by it.
- **A tick in neutral, cold, pedal up only** (*owner*, heard; on his
  phone video, which Claude cannot hear): regular, gone with the pedal
  down. Added as S16, not to be pursued (*owner's decision*).
- **The idle adaptation**: channel 01 read **128 = 780 rpm** (fault
  memory empty, coolant 90 °C, login 01283;
  `photos/vcds-idle-adapt-2026-10-12-*.jpg`). Two minutes at each of
  128, 130, 132, 133 and 133 again — 134 was meant and 133 entered, and
  136 was then saved and **the ECU kept 133 = 830 rpm, its limit**. 014
  kept counting at every stage with detection active; from 133 it read
  `deaktiv.` for a third and then two thirds of the time, as a higher
  idle lowers the load (S3). By stage:

  | channel 01 | specified | `IdleHealth` | dips /min (bus) | 014 steps up /min |
  |---|---|---|---|---|
  | 128 | 780 | 61 | 4.9 | ~9 |
  | 130 | 800 | 66 | 2.3 | ~5 |
  | 132 | 820 | 68 | 5.1 | ~4 |
  | 133 | 830 | 68 | 2.6 | ~5 |
  | 133 | 830 | 70 | 3.1 | (detection mostly off) |

  The last column counts how often the VCDS field stepped up within the
  stage, not the counter's total, so it compares stages with each other
  and not with S3's earlier rates. **No stage quieted 014, and the bus
  shows no trend** — the dips go up and down and `IdleHealth` rises
  slightly with engine speed. **Put back to 128 the same day** (*owner's
  decision*), warm on a restart, 056 reading 780
  (`vcds/vcds-step3-1-back128-014-056.csv`).
- **The warm idle was calmer than on any day before** at the same oil:
  `IdleHealth` 50 at the first warm stop and 61 at 128 after the clutch,
  against 77–89 for `30` and `31` at 93–111 °C (`open.md` S1); the
  owner saw smaller 014 figures than usual too, but **counted, 014
  hardly moved**: 5.3 rises a minute hot, 40 % of samples non-zero,
  against 6.1 and 42 % on 10/10 and 8.8 and 58 % on 9/10 (`open.md` S1,
  *12/10*). 055's learned value
  −1.18 to −1.21 (settled), and 032 read **0.0 / +2.3 %** afterwards
  (`photos/vcds-032-2026-10-12-after-step3-1.jpg`; 4/10 −0.8 / +2.3,
  9/10 −2.3 / +5.5). The changes since `31`: the joint behind the
  converter — behind both probes, so not it (`refuted.md` A13) — and
  the new air filter with the airbox crack sealed. One day; the drives
  of item 6 say whether it holds.

- **The dips keep to one slot again**: 46 of 121 pairs, 38 %, p =
  0.0011 (`cutscan.py --pairs`), against 10/10's 26 % on 39 — so the
  new leads did not take the one-cylinder share (`open.md`, *Naming the
  cylinder*).
- **The 3 min of 001 did not repeat the lean swing before a dip**:
  lambda correction −0.38 % before a dip, −0.48 % quiet, no difference
  (`open.md` S1, *What VCDS saw just before a dip*).

- **Evening, cold: the joint's bolts tightened once more** (`plan.md`
  item 1, done): one moved a little, the one over the shim not at all —
  the sealant inside settling, as expected after its first heat cycle
  (*owner*).
- **Lead 4 reseated, cold** (`plan.md` step 3, the item added the same
  day): lead 4's plug end had felt the least firm of the four when the
  new leads went on (`open.md` H4, test 1e). Pulled, turned a little and
  pushed home, it no longer tends to work its way off; all four boots
  sit alike and lead 4 looks sound (*owner*). Nothing named; H4 keeps
  its place on the one-cylinder argument alone (`open.md`, *The idle's
  candidates, ranked*).
- **Two original hoses off the intake hose, taken off and
  looked at** (*owner, photographed*; `refuted.md` A15 and C9): the
  breather hose `06A 103 493 N` with its cuff split along the moulding
  seam at the end, torn at the edge, crazed at the bend and oily inside;
  the injectors' shroud supply hose crazed, clean inside, and perhaps a
  very small leak when blown into with the far end stopped. Both sit on
  the intake ahead of the throttle, where a crack draws little at idle,
  and on all four cylinders alike — so not read as the dips' cause.
- **The thin hose from the tee leaks** (`open.md`, *What the web
  says about this engine's ventilation*): the thin hose to the tee by
  the runners, white print `06A 133 374`, lets air out when blown into
  with the far end stopped, cracked across its bend and crazed at its
  end. It sits on the line at manifold vacuum, so it is the one of the
  three that can matter at idle — on all four cylinders alike. To be
  replaced with plain 6 mm silicone hose, the number not being had; the
  shroud supply with 8 mm hose; and the missing clamps (*owner's
  decision*). **The breather hose is replaced too**, a new one ordered
  the same evening: it holds when blown through, but cleaning would not
  take out years of deposit inside and it is worn (*owner's decision*;
  *this entry first said it was kept and cleaned, a new one being too
  slow to come*). Its inside carried a black sticky layer of about
  0.5 cm, oil with dust or other dirt (*owner*; `refuted.md` A15). **In
  the owner's reading the damage on all three is surface, and the
  rubber is porous with age**: the thin hose to the tee lets air seep
  away slowly rather than through a hole, the shroud supply perhaps a
  little, and a new hose cannot be blown through at all. **The intake hose MAF to throttle `1C0 129 684` is
  the one original hose left**: blown through, its loose-feeling
  plastic stub included, it leaks nowhere (*owner*). The engine goes
  back together in two goes — the intake hose, perhaps one new thin
  hose and new clamps on the tee-to-throttle hose on 13/10, the rest
  when the parts come, about 14/10 with the vacuum gauge (*owner*). **The next warm idle is the first with these hoses new**:
  calmer, or 032/033 moving, would say this line was drawing air.

**What it is not known to have achieved:** the idle raised to the ECU's
limit did not quiet 014, so the raise is not a workaround and was
undone. Whether the calmer warm idle is the new filter and the sealed
airbox, the weather or one day's chance is not known.

**14/10/2026 — every hose on, and the vacuum gauge cold**
(`33_step3_gauge_cold_z1`, `34_step3_gauge_2500_z1`,
`vcds/vcds-step3-2-gauge-*.csv`; `plan.md` step 3 items 1 and 2).
- **The reassembly finished** (*owner, photographed*): the new breather
  hose (Gates `EMH118`) with a new spring clamp at its upper end, the
  thin hose to the tee and the 8 mm hose from the tee to the throttle
  with new clips at both ends, the thin hose on the intake hose's spigot
  clamped. **The 8 mm hose was sound before clamping** (*owner*,
  reported afterwards): tight at both ends, on a tee whose upward leg
  is 8 mm and side leg 6 mm.
- **The gauge** (MAR-POL `M57673`) teed in **at the top of the tee by
  the runners**, on the 8 mm line from the throttle's vacuum spigot
  (*owner*, reported afterwards: the regulator's hose is about 4 mm,
  too narrow for the tester's 6 mm tee and hose). *This entry said
  "teed into the fuel pressure regulator's hose", from the plan.* The
  line runs at manifold vacuum, but its tee's side leg goes to the
  breather's connector ahead of the throttle, so the point may sit a
  little below the manifold's own vacuum (*reasoned*): the readings
  below are, if anything, low. **Its needle rests a quarter-turn off zero** with
  the engine off (*owner, photographed*), so readings are taken against
  that rest position. Two starts: `33` cold (coolant 16 → 64 °C, about
  5 min of idle at 820–960 rpm, no hold) and `34` part-warm (53 → 82 °C:
  two snaps, ~14 s at 2100–2200 rpm, 3½ min of idle). Read off the
  owner's 32 s video of `34`, frame by frame: **steady at idle**, about
  18–19 inHg against the rest position (measured below; *this read
  16–17, read off the angle*); **on a
  snap it dropped towards zero, overshot above idle and settled back**;
  **a little higher and steady at the hold**. That is the
  "steady and normal" row (`open.md`, *How the vacuum gauge is read*): no large leak behind the throttle and no
  valve that does not seal, as far as a gauge can say (`open.md` H3,
  *The vacuum gauge*). The video holds only a few seconds of idle at a
  stretch, so **flicks were neither counted nor ruled out**; on the
  cold start's film the owner saw the needle not move at all.
- **`IdleHealth` ~103 on `33`** (cold) and **~114 on `34`**, rough as the
  owner felt it.
- **The hiss at the back heard again** on the cold start (*owner*); his
  reading is that it is the same hiss, and **S11 is reopened** at his
  decision (`open.md` S11). The tee and the gauge's fitting were in the
  line, and the start without them was not made, so the hiss is not
  placed.

- **Read afterwards** (*Claude, 14/10*; `open.md` H3, *The vacuum
  gauge*): the slow fall after a snap, which the owner asked about, is
  the landing every capture since 3/10 shows, 2–2½ s from 1400 rpm to
  idle; 003's air over the cold idle, over 6 g/s in the first minute,
  is what 3/10 and 10/10 read at the same minutes. The cold idle on
  `idledips --roughness` sits between 9/10's and 12/10's, calm for the
  first minute or two and rougher from about 40 °C of coolant, as both
  of those did. **Nothing in it sets the renewed hoses or the airbox
  apart from before**, cold.
- **The warm gauge reading dropped** (*owner's decision*, 14/10): the
  idle is roughest cold and the gauge saw nothing there. **Put back the
  same evening** (*owner*), for completeness, at the end of 15/10's
  drive with the can already in.
- **The level, measured off the owner's video and photos** (*Claude,
  14/10*; the owner's rest photo, his 32 s video in three parts, engine
  speed from the video's sound). The dial's green "NORMAL MOTOR" band is
  about 17–22 inHg, its red "LATE IGN TIMING" about 14–17. **Engine off,
  the needle's tip rests low on the left, at about 12 on the dial**; the
  vacuum turns it the dial's own way, and the printed scale runs about
  5.7° per inHg, so the true vacuum is the angle turned from rest over
  that. The needle's wide tail end makes it easy to read: it points at
  the dial's vacuum "0" when the true vacuum is **about 19 inHg** (tip
  and tail measured on the rest photo and an idle frame, 18.8 and
  19.9), and every inHg the tail moves along the vacuum scale adds one.
  | moment (engine speed from the sound) | true vacuum, inHg |
  |---|---|
  | settled idle, ~815 rpm | **about 18–19** |
  | the throttle opening, ~1600–1700 rpm rising | about 13, for a moment |
  | steady at 2000–2150 rpm | about 20–21½ |
  | sharp release from ~2600 rpm, 2000 → 1200 rpm | **about 24–25**, falling to idle's 19 in about 3 s |
  | gentle release from ~1850 rpm | about 20–21, back to 19 |
  ±1½ inHg on every row: two different camera angles, and the
  assumption that the mechanism turns by its printed scale, which a
  needle that rests a quarter-turn out cannot confirm. **The idle sits
  in the green band, not the red one**, before any allowance for
  altitude, which would only raise it against a sea-level band.
  *Corrected the same evening*: Claude first took the photo at idle for
  the rest position, then had the rest at the far end of the dial; the
  owner put both right, and the figures here replace both.
- **The dips the film caught** (*Claude, 14/10*; each part of the video
  put on `34`'s clock by engine speed from its sound, to within a
  frame or two). About 9 s of the 32 are settled idle, and `34` has
  **three dips** in them: 42 rpm at 188.8 s, 21 at 190.7, 29 at 211.5
  — the usual rate for that oil. Stepped through at 30 frames a second
  against the dial's ticks: **no flick of the needle at either
  readable one** (the 21 rpm dip falls in a blurred stretch); a jump
  of 1.4° at the third is a doubled frame of camera shake, the print
  doubled with it. What this frame rate and hand-held film could have
  shown is about 1° of needle, roughly ⅕ inHg. Not surprising
  (*reasoned*): a cylinder that fails to fire still draws its charge,
  so the manifold barely notices; a valve that does not seal is what
  flicks a gauge, and the bus sees these dips far better than any
  gauge can.
- **The cold start's film** (*Claude, 14/10*; the owner's second video
  in four parts, 46 s, put on `33`'s clock by engine speed from its
  sound, correlation 0.70–0.93: it runs from **33 s to 80 s after the
  start**, at 920–940 rpm). **About 17½ inHg**, against about 18½ on
  the same measure at the part-warm idle of `34` — a hair lower, not
  higher, which a cold idle with the throttle further open gives
  (*general*); the difference is inside the error. That stretch is the
  calm one every cold start shows: **one dip of 20 rpm or more** in
  the 46 s, 941 → 909 over 0.15 s at 112.1 s, and twenty of 12–19.
  Through it the needle's tip moved **0.6–0.8°, for five frames**,
  towards *more* vacuum — about 0.15 inHg, at the limit of what the
  film resolves, against ±0.3° of frame-to-frame noise and two single
  frames of 0.7° elsewhere. If it is real, it fits the throttle easing
  shut a little as the dip began (`open.md` S1, *What comes before a
  dip*: the dips come just after the ECU trims the charge), not a
  cylinder failing to draw. **Not a finding**: one event, at the noise
  floor.
- **The idle advance beside it** (003): a median of 2–5° BTDC at idle
  on every captured idle since 3/10, inside VW's 0–12° (`vcds.md`), and
  18–25° at 2000–2150 rpm. The ECU moves it −10 to +18° from sample to
  sample, which is its fast idle control. A low idle advance is what
  the dial's "LATE IGN TIMING" band means, and the reading did not
  fall into it.

**What it is not known to have achieved:** the gauge on the common
plenum cannot see a small leak at one runner, and the idle it read was
part-cold; the warm reading was not made.

**15/10/2026 — the can, and the warm idle, still on the remap**
(`plan.md` item 5; `35`–`38`). One can of Liqui Moly *DFI
Cleaner* into the tank at the station, then about 18 l of OMV
MaxxMotion 100, between `35` and `36`. Read so far, at the end of the
drive home (`37`, headlights only, A/C and blower off, oil 100–101 °C):

- **032 −4.7 / +4.7 %** (12/10: 0.0 / +2.3; 4/10: −0.8 / +2.3). The
  idle cell moved 4.7 points lean of 12/10's, the part-load cell 2.4
  points rich, the first reading on the new fuel and the cleaner: a
  direction, not a finding.
- **055's learned value −1.18 g/s**, inside the settled −1.14 to −1.29.
- **003's air at the warm idle**, read as decided on 12/10 against 9/10
  (A well lower → the MAF used to over-read; B a little lower → the
  engine needs less air; C unchanged → suspect the comparison first;
  D higher): **3.15 g/s, spread 0.10**, over the last 3 min (the first
  minute after the stop 3.25 with a tail to 4.4, the engine settling);
  9/10's hot idle 3.14, spread 0.07. **Row C, unchanged and as
  scattered** — the comparison is ordinary (760–800 rpm, loads off, 96–
  100 °C of coolant), so the MAF reads as it did and 12/10's lower
  charge did not hold. The gauge's idle after the hold, `38`: 3.09,
  spread 0.09.
- **`IdleHealth` 54** over the 4 min at home (oil 100–101 °C), **59** over
  `38`'s idle at 93–97 °C; 12/10's 50–61 at 95–99 °C, `30`/`31`'s
  77–89. As calm as 12/10.
- **014 counted on 70 of 285 samples, 25 %, at the home idle**, max 36
  — against 40 % on 12/10's hot band.
- **The dips keep to one slot** on the day pooled, 33 % (`open.md`,
  *The dips keep to one slot*).
- **The gauge warm** (`38`; oil 93–97 °C, coolant 94–100 °C; `open.md`
  H3, *The vacuum gauge warm*). The owner's video, 3 min 34 s, starts
  about 1½ min after the start and ends before engine off, so **there
  is no engine-off frame and 14/10's rest position is used** (same
  gauge, same tee). Put on `38`'s clock by engine speed from its sound
  (offset 194.4 s, the two agreeing within 1 % at idle, the hold and
  the snap). Read the 14/10 way, by the needle's tail on the vacuum
  scale:
  | moment | true vacuum, inHg |
  |---|---|
  | settled idle, ~800 rpm | **about 19** |
  | hold at ~2490 rpm, 15 s | **about 22**, steady |
  | throttle opening to ~3000 rpm | about 18, for a moment |
  | each release, 2300 → idle | **about 22½–23**, back to 19 in a few seconds |
  ±1½ inHg as on 14/10; the hold and the releases from the needle's
  angle against the idle's in the same film (5.7° per inHg).
  **Flicks** (the plan's question): the needle's angle measured on every
  frame against the dial's own hub, brass pivot and screw, so the hand
  holding the gauge drops out. **None** of 0.6° or more (about 0.1 inHg)
  in the 78 s where the film is still enough to read, against a frame
  noise of 0.1°. Of `38`'s eight dips of 20 rpm or more in the filmed
  idle, **seven are readable and none moved the needle** beyond 0.3°
  (troughs 768–787 rpm); three of them in a stretch where the hand
  turned the dial slowly, read off the needle's angle in the picture,
  which turned with it and did not jump; the eighth fell while the
  camera pointed at the engine. **None at 2500 either**: steady through the hold. As on 14/10,
  a cylinder that fails to fire still draws its charge, so the
  manifold barely notices; the bus sees these dips far better.

- **`IdleHealth` off the display, later the same day** (*owner*;
  item 5's running reading, no capture): a shorter drive, the tank at
  28 l, so about 10–12 l of the treated fill burnt. At a level crossing,
  **oil 100 °C**, headlights and the blower on its first step: **40–50
  for about three minutes, once 35** for a moment, before the filming
  began (an 11 s film of the display there reads **40–48**, `IdleRough`
  0.81–0.97 rpm, the same quantity ×50); after five more
  minutes of driving, standing at home, **70**. *Read*: **the lights
  are on all the time** (*owner*), and in every captured baseline, so
  the one load beyond the baseline was **the blower's first step**.
  40–48 with that alone is below the day's captured range with only the
  lights, 54–75 at 93–101 °C (`37`, `38`), and level with this morning's
  stops under heavier loads — blower and seat heating, at times the A/C
  — 38–55 at 92–93 °C (`35`). So it is lower than the small load
  explains on its face; but the blower's share has never been read on
  its own, it is one stop, and 70 at home five minutes later is back
  inside the range. **A lead, not a change** — and half a tank is early
  for the cleaner by its maker's dose (`plan.md` item 5). *This read at
  first "where small loads put this idle before the can", counting the
  lights as a load the baselines did not have.*

- **`IdleHealth` after the hardest drive yet, the same evening**
  (*owner*, off the display, no capture): a motorway run at full throttle
  with ~10 min held at 5000 rpm (`open.md` S8), then a warm idle at **oil
  98 °C** (the new scale), lights only, blower and seats off: **about 70
  at first, 30–40 for a while, about 50–55 as the owner's median**. In
  the band of the day's captured idles with the lights only (54–75) and
  of 12/10's (50–61), at its low edge; one stop, after a drive like no
  other in the record, so a reading and not a change.
  **Then, the same stop, A/C on and the blower on 2: 31–39, median
  about 35, and much steadier** (*owner*) — the load effect of S1
  (26/9: A/C with the blower, towards 35), the same as before the can.
  **Falling as the stop went on, to 23–25** (*owner*), still with the
  A/C and blower — the lowest `IdleHealth` on record in any state; the
  A/C idle of August graded 29 (`12`), 26/9's went towards 35. Under
  load, so not comparable with the lights-only baseline, but a floor
  nobody had seen.
  **A/C and blower off again, oil still 98 °C: back up towards a median
  of about 55** (*owner*). So the low was the load's, as on 26/9, and
  the lights-only idle stood where it had at the start of the stop.
- **`IdleHealth` at home after the drive back, the same evening**
  (*owner*, off the display): a brisker drive, then at **oil 100 °C**
  **about 80 with the lights only, and not below 50 with every load on**.
  Rougher than the stop before, which had also followed a brisk drive and
  read 55 and 23 in the same two states — so the drive before a stop
  does not decide it (4/10's pattern was the adaptations, `refuted.md`
  C19), and the idle on one evening spans 55–80 lights-only.
- **The display's `OilTemp` moved to `raw − 60` the same evening**
  (`mfd15` `S-AQY.TRI`, uploaded by the owner): every oil temperature
  read off the display from then on is on it, as every figure in these
  documents is (`docs/firmware/open.md` question 10).

**What it is not known to have achieved:** the gauge on the common
plenum still cannot see a small leak at one runner; and the can had
been in the tank an hour, so these readings are a before for item 6,
not an after.

**16/10/2026 — a brisker drive, and 014 against the A/C** (*owner*, off
the display and VCDS 014, no capture; `plan.md` item 5's running
reading). After a brisker drive than usual, a warm idle: **`IdleHealth`
about 50–70** at **oil 99 °C** (*owner*), rougher than the evening
before's ~80 at home at 100 °C; the loads were not given. Then with VCDS on 014: **A/C
on, 014 at zero for several minutes with `IdleHealth` about 70; A/C off,
014 counting and `IdleHealth` barely moved** (`open.md` S3, *The A/C
switches it*). Read the same day against every capture with a 014 log
(`tools/s3align.py`): when 014 counts it counts the dips, but how often
it counts does not follow `IdleHealth` (`open.md` S3, *The events are
the S1 dips*). So 014 is no ruler of this idle, as S3 already said, and
now on eleven sessions.

**One cylinder or two, read the same day** (*the owner's correction*:
these files said *one cylinder* where the evidence always allowed two).
Runs of three or more dips keep their order, which pairs lose, and fitted
over every idle since August (`cutscan.py --shares`): **about half the
dips on one cylinder, most of the rest on its neighbour in the firing
order, almost none on its 360° partner**; since the new leads the two are
level, 43 and 41 % (`open.md`, *One cylinder or two*). Which pair, the bus
cannot say; not the two on one coil output.

**What it is not known to have achieved:** nothing changed on the car;
one stop is a reading and not a change.

---

## Appendix — the job of 1–4/10 in detail

*Moved here from `vehicle-history.md` on 4/10/2026, when that file became
the service record alone. The working detail of the job, kept because
`open.md` cites it.*

### The valve cover and throttle job

*By the owner, at home; every item photographed and reported as it was
done. The full working checklist is in git (`plan.md` before 3/10/2026).*
One job by decision, so that the engine was opened once — and at the cost
that an improvement cannot be put down to one part.

**What was done.** Upper plenum off and aside; valve cover off; breather
out. Oil cleaned off the head, the cover joint, the plug area and the
manifold. **Injectors out and refitted one by one**, each clicked home on
its own, then the rail on at 10 Nm — cylinder 2's damaged manifold-end
O-ring replaced with the intake-side ring of an old injector (all four
then flush, photographed). Plugs left in (new since 17/9, not reachable
from the back); leads ohmed (~6 kΩ each) and refitted 1, 4, 2, 3
clockwise from the top tower. Injector windings 15.9 Ω each. The
injectors' air-shroud line refitted with new sleeves. The breather hose
and the MAF-to-throttle hose cleaned of oil. **New cover gasket** with
Dirko at the four arch points; **the cover nuts with a ratchet, by feel,
about 4 Nm at most**, gone round again after the middle ones slackened
as the gasket settled. **New plenum gasket**, plenum at 10 Nm. **New
throttle** on a new gasket at 10 Nm, both coolant hoses back, the vacuum
elbow replaced by a longer hose (it would not reach the new spigot,
which was not turned: it sits at manifold vacuum). **New breather** on
its own ring, in the cover by its bayonet alone; the new `100690` in the
old cap. The throttle cable's slack taken up (*owner's decision*).

**What it found** (the detail is in `open.md`): the old breather **sat
loose in the cover on a ring that had flowed out of shape** — larger than
the new, marked, almost liquid in places (H9); **six of the eight cover
nuts loose by hand** over a gasket gone **hard, almost like plastic**
(S10); the vacuum elbow **hard with age**; the old throttle **silent
where the new one's idle switch clicks**, with an **idle-stop face worn
1–2 mm smaller** (H8). Found sound: both plenum gaskets, the June
throttle gasket (and no protrusion on the flange), the plenum's face, the
hoses at the back, every injector connector, no emulsion under the cover.
The patch on the old breather turned out original (`refuted.md` C15).

**Before the first start, 2/10/2026.** No fuel at the rail after priming.
**098 *ADP OK*** (10.4°, 59.2 %, *volnoběh*). The ignition-on routine
**still 20 s** with the new part, which closed S13 (`refuted.md` C16).
**054: 5.6° and *volnoběh* at rest, 91.1° to the floor**, the switch
changing to *část. zatíž.* — inside VW's figures before and after the
cable was taken up. Battery reconnected, so every adaptation started
from zero (055's learned value read 0.00); **no reset through VCDS**,
decided, since there was nothing left to reset.

**The check start, 2/10/2026** — standing only, no drive, no bus
capture, on a part-warm engine (it had run a minute just before);
`test/fixtures/vcds/vcds-postrepair-checkstart-003-014-055.csv`. Fault
memory empty afterwards. **No leaks** seen. After the step down from the
warm-up speed the standing idle matched `19`'s at the same stage — rpm
794 ± 14.0 against 798 ± 14.5, timing 3.2 ± 2.3° against 4.0 ± 2.6° —
with a little less air (3.96 against 4.28 g/s), which the warmer start
accounts for; no leak signature, but the comparison was never a clean
one. **014 counted 13 twice at ~71–88 s**, cold, and nothing after; one
dip to 680 rpm at ~262 s. `IdleHealth` off the MFD peaked near 200 at
first and read **57 at its lowest** later that evening, cold, with the
A/C, blower, lights and rear window on — fresh adaptations, so neither
compares. **A ticking at the timing-belt end** that softened when the
upper belt cover was pressed went once the cover was taken off and
refitted (*owner*). **The belt end is completely dry**, nothing
seeping anywhere behind the guard — so neither the camshaft seal nor the
bearing cap 1 joint just resealed leaks there, on a cold engine
(*owner*, 3/10/2026; a toothed belt runs dry by design). **No smoke or hiss at the back** (S11), on a cold or
part-warm engine only.

**The first warm run, 3/10/2026 — the cover leaks again, at cylinder 4's
end.** Session A (`open.md` S3, *Session A*): coolant topped up cold
beforehand, the MAF left as it was. Dry at the cold start. **At the
in-band stop, about 20 minutes after the start, oil running out "in a
stream" at the half-moon arch at the gearbox end of the head, cylinder 4's
end** — from outside, nowhere along the front, the back or the timing-belt
end (*owner,
photographed*: `photos/cover-leak-2026-10-03-cyl4-end.jpg` and, below it,
`photos/cover-leak-2026-10-03-below.jpg`). It ran down **as far as the
ignition coil**, and the drive home was short and gentle.
In the photograph the gasket's edge shows as a light strip along the
joint, pushed out into a loop at that corner, with oil pooled on the head
below it (*Claude's reading of a photograph*). What the owner noticed
afterwards: **on that side the wiring-loom bracket sits under the strips
that hold the cover down**, while the video of the job has the front and
rear strips on the cover and the side bracket on top of them — which can
load the cover unevenly (*owner*). **About 0.5 l of oil topped up** at
home, the dipstick having read at its bottom mark (*owner*).

**The wrong gasket, the same night.** The owner took the plenum and the
cover off again rather than wait, and **the fault was the part, not the
fitting**: the new Elring `325.070` has, at the half-moon, **an open arch
that leaves a hole about 1 cm across** into the crankcase once
assembled, where the gasket that came off on 1/10 has **a solid, ribbed
half-moon**. The new one also has **no metal sleeves** at the bolt holes,
which the old one has, and a taller, softer section (*owner, photographed
side by side*). No part number found on the old gasket. **`325.070` is
listed for AZJ, BER, AZG and AEG and not for AQY**; Elring `915.653` is
listed for AQY and looks like the old one (autokelly, 4/10/2026). Why the
wrong one was ordered: `open.md` S10, *The cause*. The right part goes
on next (`plan.md`, step 1b).
With the cover off, **a little oil at the back of the joint too**, which
the look from outside had not shown. **About a litre** had run down to the
right, over the wiring harnesses and down to the driveshaft, none onto the
exhaust manifold or the back of the head; wiped off where reachable
(*owner*, 4/10/2026).

**The right gasket in hand, 4/10/2026.** Elring `915.653` bought, with
solid, ribbed half-moons and metal sleeves like the gasket that came off
(*owner, photographed*: `photos/cover-gasket-915653-halfmoon.jpg`,
`photos/cover-gasket-915653-whole.jpg`); **`915.653` read off the
package's label**, EAN `4041248115435`
(`photos/cover-gasket-915653-label.jpg`; *this used to say the number was
not legible in the photographs*). The worst of the oil cleaned off the cables; **the leads dry and oil on one part of the coil** after the 3/10 leak
had run down as far as it (*this said the coil's body was dry; corrected
by the owner the same day*). **The lead boots and the plugs clean, no oil
in them** (*owner*).
The oil left on the gearbox is left there, as cosmetic (*owner*;
`photos/cover-leak-2026-10-04-cleaned.jpg`).
**The cover back on, 4/10/2026**, with `915.653`: the nuts tightened
evenly by feel, each felt seating on its brass sleeve (*owner*;
`photos/cover-on-2026-10-04-*.jpg`). **The plenum back on the same day
with its new gasket, the job complete** (*owner*;
`photos/plenum-on-2026-10-04.jpg`). Oil: about 1 l topped up in all since
the leak; cold, the dipstick about 0.5 mm below the upper mark (*owner*).

**The first warm run after step 1b, 4/10/2026.** Battery disconnected
for the job, so 098 was run before the start (*owner*: OK). Session A
again (`open.md` S3, *Session A after step 1b*). **The joint stayed dry**
at the stop at 64–71 °C of oil and after the hot end of the run; the
smoke seen was the 3/10 oil burning off (*owner*). The hiss at the back
remained (S11). Fault memory empty afterwards; 032 −0.8 / +2.3 %
(`photos/vcds-032-2026-10-04-after-sessionA.jpg`). **The belt noise
was gone, too.** *Owner, 4/10/2026:* with the wrong gasket of 2–3/10 the
cover most likely sat lower than it should, and the timing belt probably
rubbed on the plastic of its cover — the likely source of the ticking at
the belt end on 2/10 (above); with `915.653` on, the noise was gone and
the engine bay quieter. **The belt was checked by the owner and is
fine.**

**Session B the same afternoon**, after a cool-down to 47 °C of oil: a
part-warm start, the misfires back at B1 and on the idle after the start,
ended by the owner at B1 (`open.md` S3, *Session B*; `refuted.md` C19).

**The starts measured from the capture** (`StartCrank`, `StartDip`,
`StartClt` by `tools/idledips.py`, `docs/firmware/frames.md`, *The
start*). ⚠ One start is noise: only a near-stall or a crank past 1.2 s
counts on its own.

| | stand | coolant | crank to first firing | `StartDip` |
|---|---|---|---|---|
| 11/9 (`18`), old injectors | ~10 h | 16 °C | 1.22 s | 141 rpm, nearly died |
| 24/9 (`19`) | ~19 h | 12 °C | 0.83 s | 118 rpm |
| 25/9 | ~12 h | — | 0.77 s | — (clean) |
| 26/9 | ~10 h | 14 °C | 0.93 s | 74 rpm |
| 3/10, session A | 27 h | 17 °C | 0.77 s | 15 rpm |
| 4/10, session A, adaptations at zero after a disconnect and 098 | ~15 h | 15 °C | 1.38 s | 0 rpm |
| 4/10, session B, part-warm | ~2 h | 44 °C | 0.70 s | 0 rpm |

### The injectors were not fully seated, 23/9 to 1/10/2026 — owner-reported and photographed

The four were fitted **already clipped into the fuel rail**, and the rail
was then pushed down onto the manifold. **Three would not go fully home**:
a gap of **under about 1 mm** is left between the injector body and its
boss, visible in the owner's photographs; **the one at the right-hand end,
as the owner stands at it — cylinder 4 (*owner*, re-confirmed 28/9/2026) — is fully home**; 1, 2 and 3
are the proud ones. When the owner tried one of
the old injectors on its own, it **clicked fully home in every bore**,
audibly. The O-ring on the manifold end is what seals each one against
the intake. To be refitted during the valve cover job: each injector into
its bore on its own first, then the rail over them (`open.md` H3). **Done on
1/10/2026: all four flush** (*The valve cover and throttle job*, above).

### The MAF

**24/9/2026**, genuine VW `06A 906 461 A`; the 2018 unit is kept. **Noticed 3/10/2026** (*owner*): the connector points to the front of the car, as on the 2018 unit before it; a video of another VW with a similar engine showed it pointing to the firewall. **Whether this one is turned is not settled** — photos of other cars show it as it is here — *this said "turned 180°, found" until later the same day*. The flow direction is right either way (the housing's two ends differ, airbox side and hose side), the connector is plugged in and its wires are not under tension; **only the harness is not clipped into its holder at the back**. *The owner's assessment: cosmetic either way.* **Then, the same day: "almost certainly" turned round** (*owner*, by the harness). **Left as it is, owner's decision before session A, 3/10/2026**: the harness reaches its holder this way too, so there was nothing to gain from turning it. **The wiggle test, 4/10/2026** (`open.md` S3, *Session A after step 1b*): 30–60 s of moving the connector and harness at a hot idle changed nothing — 003's air never dropped out (3.06–3.54 g/s against 2.92–4.03 in the three minutes before), and the misfires counted there were already counting before the hand went near it (*owner*, who watched 014 before going to the engine). **The contact is sound; the unclipped harness is cosmetic, as assessed**. **The hose from the MAF to the throttle is not held by the original clips** (*owner*, 4/10/2026, fitted by him at some earlier date): at the MAF a pipe clamp — a rubber-lined band drawn up by two bolts each side — and at the throttle a plain metal band clamp with one screw
