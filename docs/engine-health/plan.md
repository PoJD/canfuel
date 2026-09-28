# Engine health — the planned fixes, in order

**The order of work, and nothing else.** Why each step is there lives in
`open.md` (symptoms, hypotheses, the ranked candidates); what was done
lives in `vehicle-history.md` once it is done. **A step that has been done
is removed from this file in the same commit that records it**, and the
file is deleted when it is empty — `git log` keeps the rest.

## The rule — the owner's decision, 27/9/2026

**The idle comes first.** After the oil leak, the one thing this work is
for is the unsettled idle (S1) and the misfires VCDS counts at idle (S3,
group 014). So:

- **Fix, then look.** Each step is a repair; the only readings taken are
  the ones that decide the next step.
- **No test for its own sake**, and nothing unrelated to the idle is
  pursued until the idle is solved — unless it could be related.
- **Run the engine as little as possible, and above all not at idle.**
  The misfires are an idle phenomenon and the old converter already paid
  for them once. Warm the engine by driving, not by idling.

The rest of `open.md` — the other symptoms, every hypothesis's test list —
stays as reference. **It is not a to-do list.**

---

## Step 1 — the valve cover job, all in one

*Owner's decision:* everything below in one job, with no measurement between
the parts, because the engine is not to be taken apart twice. The cost,
accepted: an improvement cannot afterwards be put down to one part.

**Parts** (ordered 27/9, `open.md` S10): valve cover gasket Elring
`325.070`, breather Febi `32452`, filler seal Febi `100690`, upper plenum
gasket Elring `271.230`, sealant Elring `030.793` (Dirko HT).
**Added 28/9, ordered** (*owner's decision*): a second `100690` for under
the breather (item 5, if it matches the old one — `open.md`). The oil
filler cap is kept: nothing in it to wear, and it has never been wet with
oil.

The throttle body is **not** part of this job — it is step 2 (*owner's
decision, 28/9/2026*).

**Photograph before touching anything, and anything found.**

**The work, in order:**

1. **Plenum and cover off.**
2. **Under the cover — look, photograph:** no light-brown "mayonnaise" on
   the cam, the caps or the cover's underside. None: nothing to do. Any:
   `refuted.md` C13 reopens — say so before carrying on.
3. **The breather**: *turns clockwise to come off* (manual, item 3). Lay
   the old item 5 beside the second `100690`: if they match, the new one
   goes under the breather; if not, the one in the `32452` box if there is
   one, else the old one if undamaged. The first `100690` goes under the
   old cap (item 2).
4. **Clean off all the oil** — head, cover joint, plug area, injector area,
   the manifold below. Keep cleaner out of the open intake ports.
5. **Plugs out, cylinders 3 and 4 first** (the oily boots, S10): photograph each plug's insulator
   and each lead boot **with its cylinder number**, then clean. Oil on the
   ceramic or in a boot is noted (H4).
6. **Injectors out and refitted properly** (H3, *The injector seats*):
   - look at each manifold-end O-ring for a nick or a flat from being
     forced in on 23/9; a damaged one is replaced, not reused;
   - push **each injector home in its bore on its own** — it clicks, as the
     old one did in every bore — and only then fit the rail over all four;
   - all four must end fully home, like cylinder 4's now.
7. **While the plenum is off — look only, photograph:**
   - the injector wiring under its sleeving and the four connectors;
   - the hoses at the back: brake-servo line, the old secondary-air vacuum
     line, the breather hose and its `N79` tee — cracked, hard, oily;
   - **the old breather, out of the car** (H9) — what matters is any
     opening **to the outside**, since that is what would let unmetered
     air in: the membrane, if it can be seen (torn, hardened, deformed);
     the body and its spigots (cracks); a vent hole by the membrane, if it
     has one (oil at it means something inside leaks). Photograph it;
   - the ECM's harness earth on the plenum (ground 608 on the Golf/Jetta
     list): eyelet tight and clean;
   - the bare stud beside the injector on the right: does something belong
     on it?
   Anything bad is fixed now; nothing is measured.
8. **New cover gasket:** a dab of Dirko at the four points where the
   arches meet the straight runs, **and at the joint of bearing cap 1 to
   the head**, which the manual insists on. **Cover nuts by hand, evenly,
   gasket lightly compressed** — no torque figure (owner's decision, S10).
9. **New plenum gasket, plenum on, breather in, everything reconnected.**

*Optional, only if it is quick while everything is open:* the four HT leads
on ohms against each other; the four injector windings on ohms against
each other. Skip them freely.

## Test 1 — after step 1: one cold start in the garden, no drive

*Owner's decision, 28/9/2026:* the valve cover job is tested with **one
cold start at idle, standing, and the engine off again** — no drive, no
warm-up. The full test waits for step 2.

⚠ **What this test cannot show: the idle fault itself.** The misfires come
at the *warm* idle; none were counted at the cold idles on record
(`open.md` H8, *Checked against the logs already held*). What a cold start
*can* show is **whether a leak was sealed**, because the leak signs have a
cold-start baseline — and a sealed leak is the mechanism behind most of
step 1.

**Before the job, with the old throttle still on:** ignition on, engine
not started — **time the throttle's routine with a stopwatch** (`open.md`
S13), then read and note the engine's fault memory (VCDS, 01, fault
codes) — in particular **17973 / P1565, J338 lower stop not reached**.
No engine running needed, and *no stored faults* is a precondition of the
adaptation anyway.

**After the job, before starting:**

1. Ignition on for a few seconds, off, on again, two or three times, so
   the pump fills the rail; look and **smell** at every injector and the
   rail for fuel.
2. **The throttle adaptation** — VW's manual asks for it after any battery
   disconnect. **Basic setting, group 098** (VW's manual page 24-119,
   `open.md` H8). Ignition on, engine not running, no stored faults,
   battery ≥ 11.5 V, all consumers off, pedal untouched; basic settings,
   098, *ADP runs* — the positioner driven to min, max and a few points
   between, **at most 10 s** — then *ADP OK*. Ignition off to store it.
3. **Ignition on again, stopwatch:** does the old part still run its
   routine after an adaptation that has certainly completed, and how long?
   (`open.md` S13)

**The start — the engine cold, after a night**, so it compares with the
cold starts on record. The rail was opened, so a long crank and a rough
first seconds are expected — **the start's quality is ignored**.

- **Leaks** — fuel at the injectors and the rail, oil along the cover
  joint.
- **A CAN capture and one VCDS log, 014 + 003 + 055, from before the start
  to engine off** (*decided 28/9/2026*). 014 is the misfire count — **a
  count, not an event**: it accumulates between readings, so three groups
  cost it no misfire, only sharpness in time. 003 is air mass and plate
  angle, 055 the idle regulator and its learned value. All three carry
  engine speed, so the log aligns to the capture (`vcds.md`).
- **About five minutes, then engine off.** That covers the cold plateau
  and its step down at ~95–100 s and reaches the one 055 reading on
  record.

**Read against the cold-start baselines** (`open.md` H8, *The cold-start
idle*; `vcds.md`, 055):

| | before (old throttle) | a sealed leak would show |
|---|---|---|
| plateau | 910–1020 rpm for 93–102 s, then ~810–850 | the same — this is the ECU's schedule |
| 003 on the plateau (`19`) | air 6.8 → 5.2 g/s, plate 7.8 → 5.2° | **more air through the MAF for the same speed, the plate further open** |
| 003 after the step | air ~4.3 g/s, plate 3.5–3.9° | the same, more air and more plate |
| 055, field 2 + field 3 | **−1.2 g/s** just after the start, **−0.8** five minutes in (11/9) | **clearly nearer zero** |

**055 is read as the sum of its two air fields** (the live regulator plus
the learned value): the whole correction the idle is making. With the
learned value at zero after the battery, the regulator carries all of it,
and the two trade places as it learns — so the sum compares from the first
start. VW's manual: regulator −2.00…2.00 g/s, learned value −1.50…1.50,
and **a run-in engine sits negative, a new one positive**, so −0.73 was
normal for this engine and **only a change means anything**. *That the two
fields add is reasoned from the labels and the unit, not from VW.*

**Then:** whatever it shows, on to step 2. A clear leak signature here is
put down to step 1 — no later step can take it.

## Step 2 — the throttle body

*Owner's decision, 28/9/2026:* done **after** test 1, whatever it showed
— as the fix if the idle is still unsettled, as prevention if it is not.
Kept apart from step 1 so that what test 1 shows belongs to step 1; it
comes off with the engine assembled, and splitting it off also shortens
step 1 if that does not fit in one session.

**Part:** Pierburg `7.03703.13.0`, **ordered 28/9** — cross-referenced to
`06A 133 064 H`, the variant **without cruise control**, which is what the
car's own label says (`open.md` H8). Plus a new gasket for its flange if
one is not in the box.

1. **Photograph the old one's plate and bore** at the idle edge before it
   comes off; swap it with a new flange gasket. **Keep the old one,
   labelled.**
2. **Check the cable** — the lever on its idling stop at rest, full
   throttle reached at the quadrant with the pedal down (`open.md` H8,
   *What VW's repair manual says*).

## Test 2 — after step 2: the full test

1. **Adaptation 098** as in test 1, *ADP OK*, ignition off. **Ignition on
   again, stopwatch:** does the new part run the routine, and how long
   against the old part's times? (`open.md` S13)
2. **If the engine is cold:** the same five minutes as test 1 — plateau,
   003, 055 — against test 1. **Air mass and 055 as in test 1, only the
   plate different** → the new throttle and its freshly learned stops,
   nothing more.
3. **Warm it by driving**, and take **the reading that decides**: at
   **70–72 °C of oil, loads off**, a minute or two of `IdleHealth` against
   the band **57–100** (`open.md` S1), with 014 + 003 + 055 logging.
   Engine off.
4. ⚠ **Repeat it after a few days of normal driving.** Fresh adaptations
   have read worse before: 146 and 117 straight after the 23/9
   disconnect, 84 after 24/9's, 57–100 once settled (`open.md` H8, *The
   throttle adaptation and the battery disconnects*). A first reading
   inside or above the band does not yet say "unchanged".
5. **032 after a few hundred km** (`open.md` S9): an idle cell moving
   *negative* would also say a leak was sealed.

**Then:**

- **Idle fixed** — **014 at zero** through the warm-idle reading, on the
  first reading *and* on the repeat (VW's specification is 0…5; zero is
  the owner's bar), whatever `IdleHealth` reads, since no healthy target
  for it exists yet: record it and read *What points at which repair*
  below. The loose ends in `open.md` then close at leisure.
- **Idle unchanged after the repeat — the expected outcome:** go to
  step 3. S13 is at least answered.

Either way: a look along the new joints after the first warm run, and
again after a few hundred km (the hand-tightened nuts).

### If the idle is fixed: what points at which repair

*Owner's aim, 28/9/2026: indications, not proof — the repair came first.*
The warm-idle fix itself is seen only in test 2, after both steps, so the
two cannot be split on it directly. They can be split on **mechanism**:

| sign | points at |
|---|---|
| **What the job found** — a torn breather membrane, a cracked hose, a nicked injector O-ring, a flattened plenum gasket, photographed in step 1 | the part it was found on. **The strongest sign there will be** |
| **Test 1 already showed the leak signature** (more air, plate further open, 055 nearer zero) | step 1: a sealed unmetered leak — plenum gasket, breather, hoses, injector seats (H3/H9) |
| test 1 showed **nothing**, test 2's cold start shows only a different plate, and **S13 changed** with the new part | the throttle (H8) |
| **fixed from the first warm reading** | a mechanical change — a leak, a seat, the throttle |
| **fixed only after days of driving** | adaptations settling, or the throttle's adaptation completing |
| **better, but only to August's level** (`IdleHealth` 48 on 11/8) | the injector seats — only in play since 23/9, while the rough idle is older (S2, S3); anything clearly better than August is something older |

**One cheap way to go further — optional, the owner's call:** the old
throttle is kept. Refitted for a day (15 minutes, adaptation 098), a
returning fault would name it beyond doubt, and the new one goes back on.

## Step 3 — the exhaust, at the garage

A repair visit, not a test visit (H2, S6, S11):

- **the whole exhaust leak-tested and made tight** — manifold, its joint to
  the head, the flange and its gasket, the flex pipe, every joint back;
- **both lambda probes**: seated and tight in their bosses, no leak at
  either.

*One line to ask, since it is the same machine and the same visit:* if they
smoke-test the exhaust, whether they will put the smoke through the intake
too (H3). Not required.

Afterwards: `IdleHealth` at 70–72 °C against the band, as in test 2, with
014 logging. *Skipped if the idle is already fixed by then.*

## Step 4 — decided by step 3's result

The same rule: **idle solved → stop and record; idle unchanged → the next
repair from `open.md`'s ranked candidates**, chosen then, not now.
