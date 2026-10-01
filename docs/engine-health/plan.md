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

## Step 1 — the valve cover job and the throttle body, all in one

*Owner's decision:* everything below in one job, with no measurement between
the parts, because the engine is not to be taken apart twice. **The throttle
body is part of it** (*owner's decision, 29/9/2026*, reversing the split of
28/9): the hard protrusion on the old throttle's flange face in the June
photograph (`open.md` H8) makes that flange a sealing joint of the same kind
as the plenum gasket and the breather, and it is opened with the rest. The
cost, accepted: an improvement cannot afterwards be put down to one part —
**nor to the throttle rather than the rest**, which a separate throttle step would
have shown.

**Parts** (ordered 27/9, `open.md` S10): valve cover gasket Elring
`325.070`, breather Febi `32452`, filler seal Febi `100690`, upper plenum
gasket Elring `271.230`, sealant Elring `030.793` (Dirko HT).
**Added 28/9, ordered** (*owner's decision*): a second `100690` for under
the breather (item 5, if it matches the old one — `open.md`). The oil
filler cap is kept: nothing in it to wear, and it has never been wet with
oil. **The throttle body**, Pierburg `7.03703.13.0`, ordered 28/9 —
cross-referenced to `06A 133 064 H`, the variant **without cruise
control**, which is what the car's own label says (`open.md` H8) — plus a
new gasket for its flange if one is not in the box.

**Photograph before touching anything, and anything found.**

### What to report — the checklist

*Owner's decision, 30/9/2026:* the owner keeps no notes; he reports each
item in the session as he goes, with photographs, and Claude says what is
still missing. The numbers are the work items below. **Every photograph of
a part that exists four times names its cylinder.**

**Before anything comes off**
- [x] the coolant level, cold — **photographed 1/10/2026, not marked**:
      the owner reads it off that photograph later (*owner's decision*)
- [x] the dipstick: level, colour, any emulsion — **colour fine, no
      emulsion** (*owner-reported, 1/10/2026*); the level is wet across
      the hatched field in the photograph, not read off by the owner
- [x] the fault memory — **empty, 1/10/2026, read before the battery
      came off** (*owner-reported*)

**Items 2–3 — the cover and the breather**
- [x] the filler cap's underside: the light-brown film seen 30/9 —
      **harmless, 1/10/2026** (*owner*): a fine deposit of condensed
      water built up over a long time, no emulsion; photographed
- [ ] the cover's underside, the cam and the bearing caps: any film or
      emulsion, and **where it stops** — only near the cap and breather,
      or further down
- [x] the breather: **is there a seal under it (item 5), and under the
      cap (item 2)?** — **both there, 1/10/2026** (*owner, photographed*):
      a notched flat ring under the breather; the cap's seal is built into
      the cap (`refuted.md` C14)
- [ ] the old cover gasket: hard, cracked, flattened, where it wept
- [ ] which ring went under the breather, and why (item 3) — the old
      item 5 beside the `100690`; and whether the `100690` fits the cap at
      all, its seal being part of the cap — **when the parts arrive**, not
      in hand on 1/10/2026. *Owner considering a new cap as well — not
      decided*

**Item 5 — plugs and boots**
- [ ] each plug's insulator and electrode, cylinder by cylinder: colour,
      deposits, oil, gap if a gauge is at hand. **In the head, 1/10/2026**
      (*photographed, cylinder counted on fingers*): all four upper
      insulators clean and dry; **1 and 2 dry around the plug**, **3 and
      4 sitting in black, oily grime** from the cover leak (S10), oil
      outside only — **only a little, round the seat**, wiped off; the
      head's casting visible again. **The plugs stay in** (*owner's
      decision, 1/10/2026*): they would not come out with the access at
      the back, they are new since 17/9, and from outside all four look
      fine. Their firing ends are therefore not seen in this job
- [x] each lead boot inside: oil, tracking marks — **clean, 1/10/2026**
      (*owner, photographed*): no oil got into any boot; the leads checked
      and fine (*owner* — a silvery speckle Claude read in one photograph
      was nothing)
- [x] the four HT leads on ohms (the optional item below): **all about
      6 kΩ end to end**, small differences the owner puts down to probe
      contact

**Item 6 — injectors**
- [ ] each manifold-end O-ring: nick, flat, fine
- [ ] each injector clicked home on its own
- [ ] all four fully home under the rail

**Item 7 — while the plenum is off**
- [x] the injector wiring and its four connectors — **fine, 1/10/2026**
      (*owner*)
- [x] the four injector windings on ohms (the optional item below):
      **15.9 Ω each, all four alike** (*owner, 1/10/2026*), across the
      injector's own pins. *The harness side read 9.21–9.29 MΩ between
      its pins with the battery off — a path through the ECM, which says
      nothing about the injectors*
- [ ] the rear hoses: brake servo, old secondary-air line, breather hose
      and its plastic connector — cracked, hard, oily. **The breather hose is
      oily inside, 1/10/2026** (*owner-found*, `open.md` H9 test 4);
      **its outside fine** (*owner, 1/10/2026*); **the plastic connector
      is there, with no electrical connector — no `N79` heater on this
      car** (`open.md` H9). **Oil and deposit inside it**, the worst wiped
      out — what the breather sends, as expected (*owner, 1/10/2026*).
      **Two thinner hoses** join it too (*owner, 1/10/2026*): one to the
      injectors (their air shrouds, `refuted.md` C9), one to **another tee
      right by the head, at the intake runners**. **The connector: no crack
      seen anywhere** (*owner, 1/10/2026*) — only the smoke test (step 3)
      would settle it, and it comes out easily if one finds a leak there
      (*owner's decision: not pursued now*). **The second tee** sits on a
      rigid pipe `06A 133 374`, up towards the throttle and down under the
      runners to EVAP by the owner's reading (`open.md` H9, *The
      layout*). **Its hoses fine** (*owner, 1/10/2026*). The throttle has
      three metal spigots: this pipe on the top one — **opening behind the
      plate, so at manifold vacuum** (*owner, the part in hand*) — and
      the two coolant hoses on the two at the back underneath: one runs
      up to the expansion tank, the other down into the circuit
      (*owner*). Closed for now; the
      line goes into the smoke test with the rest if it comes to that
- [x] the intake duct where the breather hose joins it, ahead of the
      throttle: **oily inside, the whole hose off, 1/10/2026**
      (*owner-found*, `open.md` H9 test 4)
- [x] that hose — **the MAF-to-throttle connector**, which the breather
      hose and a thinner one join through a plastic connector — by hand: **sound on every side**
      (*owner, 1/10/2026*); the "split" was a frayed sliver at the end,
      torn off. Clean the oil out of it before it goes back
- [ ] the old breather out of the car: membrane, body, spigots, vent hole
      — **1/10/2026, photographed**: oily everywhere; **a foreign black
      patch on the body by the spigot**, askew and lifting at the edge,
      read by the owner as a past repair (`open.md` H9 test 4); the seam
      of its middle ring **probably fine by hand** (*owner*) — the patch is
      the suspect. **Keep the part** — the patch is evidence
- [ ] ground 2 — tight and clean if found; **not found is done**
- [x] the old upper plenum gasket — **whole, 1/10/2026** (*owner,
      photographed*): no tear, no gap, pressed in evenly; the joint looked
      fine. Both faces cleaned, a rag over the lower part's ports. The
      upper part's runners carry a **brownish oily film along their
      floors**, all four — the breather's oil, by the route H9 test 4
      traced (*reasoned*)

**Item 8 — the throttle** (the day the new one is in hand)
- [x] the old plate and bore at the idle edge — **clean, 1/10/2026**
      (*owner, photographed*): a thin dark line at the plate's edge, no
      oil film
- [x] both flange faces — **no protrusion** (`open.md` H8, *At the
      job*); the June gasket came away on its own, the green is the
      original gasket's imprint
- [x] the plenum's face after cleaning, the rule across it: **no light,
      1/10/2026** (*owner*); the scratches on its right-hand side stay
      inside the face, none from bore to outside
- [x] any pit or dent — **none, 1/10/2026** (*owner*): the dark spots on
      the plenum's face are deposit petrol did not lift; the face is flat
- [x] the June throttle gasket: **whole, 1/10/2026** (*photographed*) —
      no tear, no gap from bore to outside, at the lower left or anywhere;
      the bolt rings and a darker band along the bore pressed in evenly
- [ ] the cable: idle stop at rest, full throttle with the pedal down

**Items 9–10 — back together**
- [ ] Dirko at the four arch points, the two front ones not skimped
- [ ] every rag out of the ports — **counted**; since 1/10/2026 one in
      the cover's breather opening, one in the plenum's throttle mouth and
      one over the lower part's four ports
- [ ] **both** coolant hoses back on the new throttle, the level topped up.
      Off since 1/10/2026, their ends tied upwards (one cable-tied to a
      loom at the back, one tucked behind a cable) — **check they have
      not turned down** before refitting

**Optional**, only if quick: the four HT leads and the four injector
windings on ohms, each against the other three.

**Torques — VW's figures for this engine** (VW's manual as transcribed on
workshop-manuals.com: *Dismantling and assembling intake manifold – upper
part / – lower part*, figures N24-0950 and N24-0949, and *Removing and
installing parts of the ignition system*, *Test data, spark plugs*; the
breather's nut from the Bentley view in `open.md` S10). **A small torque
wrench** (*owner's decision*); the cover nuts stay by hand (S10).

| joint | torque | VW's note |
|---|---|---|
| intake manifold upper part → lower part, bolts (item 5) | **10 Nm** | gasket (item 13) always new |
| throttle body → upper part, bolts (item 5) | **10 Nm** | gasket (item 9) always new |
| throttle cable bracket (item 4) | 10 Nm | |
| fuel rail → lower part (item 12) | **10 Nm** | injector O-rings renewed if damaged |
| spark plugs (BKUR 6 ET-10, gap 0.9–1.1 mm) | **30 Nm** | |
| ignition coil | 10 Nm | |
| breather bracket nut (Bentley item 4) | 10 Nm | |

The upper part does not come off whole (*owner's plan, 28/9/2026*): it is
moved aside with most of its hoses at the back left on, as in the videos;
only the front hose by the fuel rail, and perhaps one at the back, is
undone. Tightening evenly and crosswise is general practice; VW gives no
order for the upper part.

**Two coolant hoses run to the throttle body** (*owner-observed: one on
28/9/2026, both found when it came off on 1/10/2026* — this paragraph
used to say *a* coolant hose), so the job opens the cooling circuit:
**start it on a cold engine**, pinch, plug or tie the hoses' ends upwards
while they are off, and **top up afterwards and check the
level again after the first warm run** (the test below) — air in the
circuit is what that finds.

**Before the job, with the old throttle still on** — ignition only, no
engine running:

- **Read the engine's fault memory** (VCDS, 01, fault codes) — a minute,
  ignition on. **It no longer decides S13**: the old part's timing did
  that (`open.md` S13). It is the record of what the car carried into the
  job, so that a code after it is known to be new. **Read 1/10/2026,
  before the battery came off for the job: empty** (*owner-reported*) —
  as after the last drive before 26/9.
  *That 098 ran on 29/9 suggests it was still empty, but VW lists "no
  stored faults" as a precondition of the procedure, not as something the
  ECU is known to enforce — and whether a disconnect clears this ECU's
  memory is not settled either* (generally it does not; not read for this
  ECU).

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
   ceramic or in a boot is noted (H4). **The leads go back on the coil as
   they came off: 1, 4, 2, 3**, clockwise from the top (*owner-read,
   1/10/2026*; `open.md` H4, *Step 1*, 1d).
6. **Injectors out and refitted properly** (H3, *The injector seats*):
   - look at each manifold-end O-ring for a nick or a flat from being
     forced in on 23/9; a damaged one is replaced, not reused;
   - push **each injector home in its bore on its own** — it clicks, as the
     old one did in every bore — and only then fit the rail over all four;
   - all four must end fully home, like cylinder 4's now.
7. **While the plenum is off — look only, photograph:**
   - the injector wiring under its sleeving and the four connectors;
   - the hoses at the back: brake-servo line, the old secondary-air vacuum
     line, the breather hose and its plastic connector — cracked, hard,
     oily;
   - **the old breather, out of the car** (H9) — what matters is any
     opening **to the outside**, since that is what would let unmetered
     air in: the membrane, if it can be seen (torn, hardened, deformed);
     the body and its spigots (cracks); a vent hole by the membrane, if it
     has one (oil at it means something inside leaks). Photograph it;
   - **the engine's two earths** (`open.md` H4, *Where the earths are*),
     each eyelet tight, clean, no corrosion — found by following the
     wires, since this engine's diagram does not name them (*VW's
     convention: earth wires are brown*):
     - **ground 2, the engine's main earth** — follow the battery's
       negative cable to where it is bolted on the gearbox/engine;
     - **the coil's earth** (ground 15 on the head in the US list) —
       *only if it can be seen*: the wires run in a sealed loom, which
       is not cut for this (*owner's decision, 28/9/2026* — the
       electrics are nearly ruled out); a look from behind the head or
       from below while the intake is aside, not pursued further;
     - **not found is done** (*owner's decision, 29/9/2026*): neither
       has been found before, and neither needs to be. The engine's earth
       was measured running on 26/9 — battery − to the coil bracket,
       healthy under load (`open.md` H4, *Step 1*) — which covers ground
       2's whole path wherever its bolt is; the coil's wire ohmed
       unbroken. A search that finds nothing is not a gap in this step;
   Anything bad is fixed now; nothing is measured.
8. **The throttle body, while the upper part is aside:**
   - **photograph the old one's plate and bore** at the idle edge before
     it comes off; **then both flange faces and the old gasket** — the
     throttle's and the plenum's — above all the **hard protrusion at the
     lower left of the throttle's face** seen in the June photograph
     (`open.md` H8), and whether the old gasket shows a gap or a dent
     there;
   - **clean the plenum's face flat; nothing may stand proud of it.**
     *How — general practice, not VW's (the manual only says the gasket
     is always new); owner's question, 29/9/2026:*
     - **solvent and a plastic scraper first, and usually only**: brake
       cleaner or technical petrol on a rag, old gasket remains lifted
       with plastic or wood, never a steel blade. Try the solvent on a
       hidden spot first if any part of the manifold is plastic;
     - **abrasive only for a hard spot the solvent does not move**, and
       then: fine wet paper (400–600) **wrapped round a flat block**, a
       few strokes along the face, never by hand alone and **never a
       rotary disc** — both round the face off, and a disc throws grit.
       **Plug the bore with a rag first**: everything that falls in on
       this side of the plate goes straight into the cylinders. Clean
       again with solvent afterwards;
     - **check it flat**: a steel rule on edge across the face in
       several directions, a light behind it — no light under the rule;
     - **a raised spot** — a deposit comes off as above; a hard lump in
       the metal is taken down **to the face and not below it**, with the
       block, checking with the rule as you go;
     - **a pit or dent**: photograph it with a rule beside it. **Off the
       line the gasket seals on, it does not matter. Across that line it
       is a leak path**, and the choice is made on the spot: a small one
       gets a thin film of the Dirko on that spot only, under the new
       gasket — *a deviation from VW's dry gasket, decided because an
       open leak path is worse*; one that a film cannot bridge means the
       upper part is not reused, and the job waits for one;
   - the new one on with a new flange gasket, **bolts 10 Nm** (the table
     above), both coolant hoses back on. **Keep the old one, labelled**;
   - **check the cable** — the lever on its idling stop at rest, full
     throttle reached at the quadrant with the pedal down (`open.md` H8,
     *What VW's repair manual says*).
9. **New cover gasket:** a dab of Dirko at the **four points where the
   half-moon arches meet the straight runs**, as in the videos. That
   already covers what the manual insists on — the **joint of camshaft
   bearing cap 1 to the head**: cap 1 is the camshaft's front bearing
   cap, at the timing-belt end, and the front half-moon sits right across
   the line where it meets the head. Nothing extra to find; just do not
   skimp on the two front points. **Cover nuts by hand, evenly, gasket
   lightly compressed** — no torque figure (owner's decision, S10).
10. **New plenum gasket, plenum on, breather in, everything reconnected.**

*Separately, any time, not part of the job* (*owner's decision,
28/9/2026*): **grounds 608 and 609** — in the plenum chamber under the
windscreen base, not at the engine; 608 in its centre by the ECM
(`open.md` H4).

*Optional, only if it is quick while everything is open:* the four HT leads
on ohms against each other; the four injector windings on ohms against
each other. Skip them freely.

## The test after the job — the misfires first

*Owner's decision, 29/9/2026:* one full test after the one job, in
sessions. **Group 014 is in every VCDS log until the misfire verdict is
in**, and only what touches the idle is recorded. 014 is **a count, not an
event**: it holds about 3 s (`refuted.md` C10) and VCDS reads three groups
in about 0.9 s, so two more groups beside it cost it no count, only
sharpness in time.

**What the verdict is compared with, and why at two temperatures**
(`open.md` S3, *How often 014 counts, by oil temperature*): on `24` — the
car as it now is, new MAF, adaptations fresh after a disconnect, which is
exactly what the job leaves — standing with detection `aktivováno` the
counter moved **20 times a minute at 56–60 °C of oil and 10 a minute at
68–72 °C**, and never stayed quiet for more than **57 s**. The middle band
is where it counted most, so it is the harder test; the hot band is the
one this plan has always read. **Only the post-MAF rate compares**: on the
old MAF the hot band counted almost nothing (0.3 a minute on `19`), so a
zero there before 24/9 proves nothing.

### Who runs what — the laptop, two windows

- **The CAN capture is Claude's**: `usbtin_capture.py`, listen only, one
  file for the whole session, started before the ignition and left
  running to engine off — `python tools/usbtin_capture.py --seconds 3600
  --out <session>_z1.txt`. It ends itself; stopped early, it loses at
  most the last half-second, after the engine is off.
- **The oil watch is the owner's**, in a second `cmd` window, reading the
  same file while it grows: `python tools\oilwatch.py <session>_z1.txt`
  (both stops in A and in B). It never touches the adapter. It **beeps
  three times** when a stop is due — ninety seconds ahead, so there is time
  to find a place — and **once, long**, when the idle in the band is long
  enough. **Aim for the band's lower edge**: after a drive the oil keeps
  rising at a standing idle (`19`: 60 → 65 °C in 4½ minutes), and a stop
  entered high heats out of it. A middle band driven through is marked
  missed and the watch moves on to the hot one; closed by accident, it is
  started again and rebuilds its state from the file.
- **VCDS on its own log file**, groups as each session says; check that it
  is still logging after the engine catches (`vcds.md`).

### Before the first start

1. Ignition on for a few seconds, off, on again, two or three times, so the
   pump fills the rail; look and **smell** at every injector and the rail
   for fuel.
2. **The throttle adaptation** — VW's manual asks for it after any battery
   disconnect and after a new J338. **Basic setting, group 098** (VW's
   manual page 24-119, `open.md` H8). Ignition on, engine not running, no
   stored faults, battery ≥ 11.5 V, all consumers off, pedal untouched;
   basic settings, 098, *ADP runs* — the positioner driven to min, max and
   a few points between, **at most 10 s** — then *ADP OK*. Ignition off to
   store it.
3. **Ignition on again, stopwatch:** does the new part run the routine,
   and how long against the old part's 20 s, the same before and after
   its own completed 098? (`open.md` S13 — this closes it.)

### Session A — the cold start and the warm-up drive, one log

**Capture and VCDS 014 + 003 + 055** from before the start to engine off.
003 is air mass and plate angle, 055 the idle regulator and its learned
value; all three carry engine speed, so the log aligns to the capture
(`vcds.md`). The coolant was opened, so the engine is cold whatever else;
note the coolant temperature at the start. The rail was opened too, so a
long crank and rough first seconds are expected — **the start's quality is
ignored.**

- **A1 — standing, 2–3 minutes, then drive off.** Leaks: fuel at the
  injectors and the rail, oil along the cover joint, **coolant at the
  throttle's hose**. The plateau and its step down at ~95–100 s. The
  **leak signature** against the cold-start baselines below. ⚠ A cold
  idle without counts is not a verdict (`open.md` S3, *When the counts
  start after a cold start*); A1 decides nothing about the misfires.
- **A2 — drive, and stop at 56–62 °C of oil** when the watch says so.
  **Two minutes standing, loads off**, until the long beep.
- **A3 — drive on, and stop at 68–72 °C.** **Three minutes standing,
  loads off**, until the long beep; then **group 004 for a minute** (a
  separate short log — the three-group one is full) for the intake air
  temperature, so that air against plate angle compares like with like
  (`open.md` H8, *Air against plate angle is the throttle's own
  calibration curve*). Engine off.
- **A4 — optional: the oil thermometer, the first minute after engine
  off** (*owner's decision, 30/9/2026*: **decided before the drive** —
  it depends on the thermometer being bought in time, and on the time
  left for the tests; `docs/firmware/open.md` question 10). No engine
  running, so it costs the idle nothing. **Ignition back on at once** so
  that 0x420 keeps coming and the capture keeps running; the owner reads
  the IR thermometer aloud and Claude stamps each reading against the
  capture's raw byte. **The oil filter first**, then **the sump pan from
  underneath**, then **the upper coolant hose** — the last one checks the
  thermometer itself against 0x288's coolant, which nobody doubts. The
  method, and why it decides, is in the firmware question.
- **Once cool: the coolant level.**

**The leak signature, A1 against the cold starts on record** (`open.md`
H8, *The cold-start idle*; `vcds.md`, 055). **The plate angle no longer
compares** — it is a different part with freshly learned stops — so a
sealed leak is read off the air and the regulator:

| | before | a sealed leak would show |
|---|---|---|
| plateau | 910–1020 rpm for 93–102 s, then ~810–850 | the same — this is the ECU's schedule |
| 003 air on the plateau (`19`) | 6.8 → 5.2 g/s | **more air through the MAF for the same speed** |
| 003 air after the step | ~4.3 g/s | the same, more air |
| 055, field 2 + field 3 | **−1.2 g/s** just after the start, **−0.8** five minutes in (11/9) | **clearly nearer zero** |

**055 is read as the sum of its two air fields** (the live regulator plus
the learned value): the whole correction the idle is making. With the
learned value at zero after the battery, the regulator carries all of it,
and the two trade places as it learns — so the sum compares from the first
start. VW's manual: regulator −2.00…2.00 g/s, learned value −1.50…1.50,
and **a run-in engine sits negative, a new one positive**, so −0.73 was
normal for this engine and **only a change means anything**. *That the two
fields add is reasoned from the labels and the unit, not from VW.*

**The misfire verdict of the day:** **014 at zero through A2 and A3, with
detection `aktivováno` throughout** — samples reading `deaktiv.` do not
count towards the time, since the ECU switches detection off below about
20 % load, right at the hot-idle load (`open.md` S3). On `24` the same five
minutes would have brought some forty and thirty counts, and each idle is
more than twice the longest quiet stretch seen there. VW's specification
is 0…5; zero is the owner's bar.

- **Any count** — the misfires are not gone: **step 2**. Session B and C
  are not run.
- **Zero** — session B, the same day.

`IdleHealth` is read beside it all, against the band **57–100** (`open.md`
S1), but decides nothing yet: no healthy target for it exists.

### Session B — the same test again, the same day, after a cool-down

*Owner's decision, 29/9/2026:* **the verdict is taken twice, both on the
day of the job** — replacing an earlier draft of the same day that put the
second reading a few hundred km later, "on settled adaptations". That
reason did not hold up against its own evidence: fresh adaptations have
read **worse** before (146 and 117 straight after the 23/9 disconnect, 84
after 24/9's, 57–100 once settled; `open.md` H8, *The throttle adaptation
and the battery disconnects*), so a zero on fresh adaptations errs towards
"unchanged", never towards "fixed", and waiting cannot make it more
certain. **And on the car as it now is, 014 has counted in every session
ever logged** (`open.md` S3, the table by oil temperature), so a whole
warm-up with none is not something that has happened by chance before.

What a second session adds is **a second, independent pass through the
band where it counted most**: a new start, a new warm-up, new air and
fuel adaptation from where the first left them.

**When:** after the engine has cooled until the oil reads **below about
45 °C** — a few hours; the oil watch shows it at ignition-on — so that the
drive climbs through 56–62 °C again with time to be warned.

**Capture and VCDS 014 + 055 + 032**, **the same two stops as A2 and A3**
(the oil watch with both stops, as in A), loads off; A1's leak checks and
the cold-start table are not repeated. **A4 again at engine off, if A4
was taken**: a second hot point for the same question.

- **014 at zero again through both stops, detection `aktivováno`** — **the
  misfires are gone**, and the verdict is closed. Record it, read *What
  points at which repair* below, and go to session C.
- **Counts** — they were not gone; A's zero was luck: step 2.
- **055's learned value** against the −0.73 g/s of 11/9, and **032's idle
  cell** (`open.md` S9): either moving *negative* also says a leak was
  sealed. Read here for what they are after a day; **a photograph of both
  screens after a few hundred km** is worth having later, but decides
  nothing.

### Session C — only if A and B are both zero: the healthy idle

**Nothing is decided by it**, so it is not a test for its own sake: it is
the recording nobody has. **This car becomes the healthy AQY that H0 has
never had** (`open.md` S1, *What is not known: the healthy target*) — the
`IdleHealth` target and VW's idle specifications on an engine that meets
them.

**Capture and VCDS 002 + 003 + 055** (014 has given its verdict; 002
carries VW's idle limits — air 2.0–5.0 g/s, injection 2.0–5.5 ms, load
15–35 %, `vcds.md`), warm at 68–72 °C: **two minutes loads off, then two
minutes with the A/C on**, same speed — the regulator's answer to a load
step, and the two-hold method of `vcds.md`.

### Afterwards, either way

A look along the new joints after the first warm run, and again after a
few hundred km (the hand-tightened nuts).

### If the idle is fixed: what points at which repair

*Owner's aim, 28/9/2026: indications, not proof — the repair came first.*
With everything done in one job, **the idle itself cannot tell the parts
apart** (the cost accepted in step 1). What can:

| sign | points at |
|---|---|
| **What the job found** — a torn breather membrane, a cracked hose, a nicked injector O-ring, a flattened plenum gasket, **a gap in the old throttle gasket at the protrusion**, photographed in step 1 | the part it was found on. **The strongest sign there will be** |
| **A1 showed the leak signature** (more air, 055 nearer zero) | a sealed unmetered leak — plenum gasket, breather, hoses, injector seats, the throttle's flange (H3/H9/H8); which one only the photographs say |
| **no leak signature, and S13 changed** with the new part | the throttle itself (H8) |
| **zero in both sessions, from the first warm reading** | a mechanical change — a leak, a seat, the throttle — rather than anything that has to learn |
| **better, but only to August's level** (`IdleHealth` 48 on 11/8) | the injector seats — only in play since 23/9, while the rough idle is older (S2, S3); anything clearly better than August is something older |

**The one way to split the throttle from the rest — optional, the owner's
call:** the old throttle is kept. Refitted for a day (15 minutes, the
coolant hose, adaptation 098), a returning fault would name it beyond
doubt, and the new one goes back on.

## Step 2 — the exhaust, at the garage

A repair visit, not a test visit (H2, S6, S11):

- **the whole exhaust leak-tested and made tight** — manifold, its joint to
  the head, the flange and its gasket, the flex pipe, every joint back;
- **both lambda probes**: seated and tight in their bosses, no leak at
  either;
- at least a **visual check of the rest of the exhaust**, with the engine
  running if they will.

*One line to ask:* whether they have a smoke machine, and if so whether
they will put the smoke through the intake too (H3). **Planned as if they
do not** (*owner's decision, 29/9/2026*) — the intake smoke test is step 3.

Afterwards: session A's hot idle again — 014 logging, three minutes at
68–72 °C with the oil watch, `IdleHealth` against the band. *Skipped if the idle is already fixed by then.*

## Step 3 — only if the idle is still not fixed

The same rule: **idle solved → stop and record.** Otherwise, in this order
(*owner's decision, 29/9/2026*), each deciding whether the next is needed:

1. **An intake smoke test, done at home** (`open.md`, *The idle's
   candidates, ranked*, row 1 and *Tools worth owning*). The engine off
   and cold, so it costs no idle. The leak is still candidate 1 after
   step 1, which replaced parts but tested no joint, and smoke is what
   names *where*. Skipped if the garage already did it in step 2.
   *General practice, not VW's:*
   - **the smoke**: a cheap 12 V smoke machine, or home-made — a sealed
     tin with a 12 V heater (a diesel glow plug or a resistance coil) and
     a wick in **mineral (baby) oil**, fed by an **aquarium air pump**.
     Never anything flammable in it, never workshop air: the pressure
     only has to make the smoke flow;
   - **seal the intake behind the MAF** — the hose between the MAF and
     the throttle off, a glove or bag clamped into it — and feed the smoke
     there or through a vacuum line (the brake-servo hose, disconnected);
   - **hold the throttle open** (a string on the cable or a hand on the
     quadrant) so the smoke reaches the plenum;
   - a few minutes of smoke, a torch, and look at the throttle's flange,
     the upper-to-lower plenum joint, the injector seats, the hoses at
     the back, the breather and its hose's plastic connector, the brake
     servo's valve;
   - ⚠ **smoke at the oil filler or the dipstick is expected**, not an
     intake leak: the breather joins the crankcase to the intake. It
     does test the new cover gasket along the way.

   **Smoke found** → that joint is fixed, then session A's hot idle again.
   **None** → the leak is as good as ruled out, and item 2 follows.
2. **A vacuum gauge at a warm idle** (`open.md`, *Tools worth owning*),
   teed into the brake-servo line: a regular flick down is a valve (H1),
   a low, slowly wandering needle a mixture fault (H7) or a leak smoke
   could not reach. A few minutes at idle, warmed by driving.
3. **Then the next repair from `open.md`'s ranked candidates**, chosen
   then, not now.
