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

## The car, the symptoms, and the instruments

**The car.** VW New Beetle, 2.0 l **AQY** (85 kW), ECU `06A 906 018`,
model year 2000, bought in 9/2017 at 126,200 km and driven little since.
**Remapped in 6/2018**, described by the owner as mild; not undone. The engine warning lamp had been masked by a previous
owner and was restored in 2017.

**S1 — the unsettled idle.** At a standstill the engine speed dips by 20–45
rpm every few seconds and recovers in about a quarter of a second. Felt from
the seat. **It depends on temperature, and not simply:** rough cold, worst
at about 50–61 °C of oil, calmest hot. A reading without the oil
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
  the 60 s warm idle of 11/8 at 61 °C of oil (`09`) and the cold start's
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

- **6/2018** — remap. **12/2017** — fuel filter changed; the old one came
  off corroded and leaking, with dark, cloudy fuel in it (photographed).
  The fuel tank was replaced at some point in the ownership; when is not
  recoverable.
- **The idle had stumbled for years**, alongside a poor cold start and, on
  a cold engine coasting downhill, fuel heard burning in the exhaust.
- **6/2026** — new ignition coil, after a misfire under full load (gone
  since). Throttle body inspected: already clean.
- **7/2026** — new fuel pressure regulator; MAF connector cleaned.
- **Summer 2026** — heater replaced with the dashboard out; **the battery
  was off for more than a week**, so every adaptation restarted. A small
  secondary-air hose was torn off in the work (fault P0411, 11/8), and
  refitted.
- **11/8** — the first captures (`09`, `11`, `12`). The hot idle graded
  **43–48** (29 with the A/C on); at 61 °C of oil 15 dips a minute. Before
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
August's: **the old MAF had been over-reading** (`refuted.md` C2).

- **Confident:** the rich trim was the MAF.
- **The idle got smoother on engine speed** — dips at a standstill fell
  51–65 % in every oil band.
- **But 014 counted *more*** at the hot idle. **The counter, not the
  engine**: on the new MAF it counted five to fifty times more per dip
  (`refuted.md` A11). Reasoned: this ECU's misfire threshold depends on
  load, which it computes from the MAF.

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
- **014 still counted** at the warm stops — 16–17 a minute at 40–66 °C of
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

**What the two sessions showed together** (`open.md` H10): 014 followed
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
| the job of 1–2/10 | **probably, for smoothness at the hot idle**: about 9 dips a minute (24/9), 5 (3/10, a one-minute stop) and 4.4 (4/10). The middle band did not move. Which part — the seated injectors, the breather, the throttle — **cannot be told**; they went in together |
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
| middle band, ~55–62 °C of oil | **2.12 rpm (`09`, 11/8)** | 1.67 (51–61 °C) | 2.22 (58–65 °C) | **1.95** (A2), **2.14** (B1) |
| cold idle, the first five minutes | **2.16 (`18`, 11/9)** | — | — | **2.42** (A1) |
| hot, ~70 °C | 0.96 (`11`, 11/8, a 22 s hold) | 1.85 | — | **1.44** (A3) |

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
  August's.

---

## Where it stands, and what comes next

**Open:** S1 and S3. The misfires remain on settled adaptations. The lead
idea is **air reaching the engine past the throttle** — an unmetered leak at
the back of the intake, never sprayed, where the owner also hears a hiss he
cannot place — with the learned idle air value as the ECU's way of showing
it. **Next** (`plan.md`): an **intake smoke
test**; then session A **without** resetting the adaptations, so that a
zero means something.

*Entries are added here as each step is done.*

**9/10/2026 — the exhaust joint behind the converter, resealed** (*owner,
photographed*: `photos/exhaust-joint-2026-10-09-old-parts.jpg`,
`photos/exhaust-joint-2026-10-09-new.jpg`). The joint the garage had
filled with sealant on 10/9, and that had rattled since, was taken apart
and remade with a two-bolt sleeve connector and exhaust sealant. A little
play remains — the pipe behind is about 1 mm narrower — which the sealant
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
mattered** — nothing is claimed until it has.

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
at the stop at 45–50 °C of oil and after the hot end of the run; the
smoke seen was the 3/10 oil burning off (*owner*). The hiss at the back
remained (S11). Fault memory empty afterwards; 032 −0.8 / +2.3 %
(`photos/vcds-032-2026-10-04-after-sessionA.jpg`). **The belt noise
was gone, too.** *Owner, 4/10/2026:* with the wrong gasket of 2–3/10 the
cover most likely sat lower than it should, and the timing belt probably
rubbed on the plastic of its cover — the likely source of the ticking at
the belt end on 2/10 (above); with `915.653` on, the noise was gone and
the engine bay quieter. **The belt was checked by the owner and is
fine.**

**Session B the same afternoon**, after a cool-down to 32 °C of oil: a
part-warm start, the misfires back at B1 and on the idle after the start,
ended by the owner at B1 (`open.md` S3, *Session B*; H10).

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
