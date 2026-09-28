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

**Added 28/9 — the throttle body, preventively** (*owner's decision*; the
reasoning and what it costs are in `open.md` H8): Pierburg
`7.03703.13.0`, **ordered 28/9** — cross-referenced to `06A 133 064 H`, the
variant **without cruise control**, which is what the car's own label says.
Plus a new gasket for its flange if one is not in the box.

**Photograph before touching anything, and anything found.**

**The work, in order:**

1. **Plenum and cover off.**
2. **Under the cover — look, photograph:** no light-brown "mayonnaise" on
   the cam, the caps or the cover's underside. None: nothing to do. Any:
   `refuted.md` C13 reopens — say so before carrying on.
3. **The timing mark**, while the front is open: cylinder 1 at TDC, the
   cam sprocket's mark against its reference, **by the manual** — a free
   look for a belt a tooth out.
4. **The breather**: *turns clockwise to come off* (manual, item 3). Lay
   the old item 5 beside the second `100690`: if they match, the new one
   goes under the breather; if not, the one in the `32452` box if there is
   one, else the old one if undamaged. The first `100690` goes under the
   old cap (item 2).
5. **Clean off all the oil** — head, cover joint, plug area, injector area,
   the manifold below. Keep cleaner out of the open intake ports.
6. **Plugs out, cylinders 3 and 4 first** (the oily boots, S10): photograph each plug's insulator
   and each lead boot **with its cylinder number**, then clean. Oil on the
   ceramic or in a boot is noted (H4).
7. **Injectors out and refitted properly** (H3, *The injector seats*):
   - look at each manifold-end O-ring for a nick or a flat from being
     forced in on 23/9; a damaged one is replaced, not reused;
   - push **each injector home in its bore on its own** — it clicks, as the
     old one did in every bore — and only then fit the rail over all four;
   - all four must end fully home, like cylinder 4's now.
8. **While the plenum is off — look only, photograph:**
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
9. **New cover gasket:** a dab of Dirko at the four points where the
   arches meet the straight runs, **and at the joint of bearing cap 1 to
   the head**, which the manual insists on. **Cover nuts by hand, evenly,
   gasket lightly compressed** — no torque figure (owner's decision, S10).
10. **The throttle body** (added 28/9): photograph the old one's plate and
    bore at the idle edge before it comes off; swap it with a new flange
    gasket; **check the cable afterwards** — the lever on its idling stop
    at rest, full throttle reached at the quadrant with the pedal down
    (`open.md` H8, *What VW's repair manual says*). **Keep the old one,
    labelled** — it is the known part if the new one misbehaves.
11. **New plenum gasket, plenum on, breather in, everything reconnected.**

*Optional, only if it is quick while everything is open:* the four HT leads
on ohms against each other; the four injector windings on ohms against
each other. Skip them freely.

## Step 2 — the first start, and the one decision

**Before starting:** ignition on for a few seconds, off, on again, two or
three times, so the pump fills the rail; look and **smell** at every
injector and the rail for fuel.

**The throttle adaptation, before the first start** — the new J338 needs
it, and this is the one case where VW's manual asks for it. **Which
group, 098 or 060, is settled off the label file first** (`open.md` H8,
*Which basic-setting group adapts it*); 098 is the expected one. Key on,
engine off, no stored faults, battery ≥ 11.5 V, pedal untouched, coolant
5–95 °C; basic settings, the group, *ADP RUN*, about 30 s while the
throttle is heard cycling, then *ADP OK*. Listen at ignition-on for the
~20 s of the throttle seeking its stops (`open.md` H8) — the new part
should sound the same.

**First start:** the rail was opened, so a long crank and a rough first
seconds are expected — **the start's quality is ignored**. Then, briefly:

- **leaks** — fuel at the injectors and the rail, oil along the cover joint;
- **`IdleHealth`**, a **CAN capture**, and **one VCDS log from before the
  start to engine off: groups 014 + 003 + 055** (*decided 28/9/2026*).
  014 is the misfire count; 003 the air mass and the plate angle, which
  tell a sealed leak from a new throttle (below); 055 the idle regulator and its
  learned adaptation, in g/s of air (`vcds.md`; logged once, 11/9). Three
  groups cost 014 some rate and lose nothing: **014 is a count, not an
  event** — it accumulates between readings, so a slower poll misses no
  misfire, it only places each one less sharply in time. All three carry
  engine speed, so the log aligns to the capture (`vcds.md`).
- **if the engine is cold:** the cold-start plateau against the baseline
  in `open.md` H8 (~910–1020 rpm for ~95–100 s, then a step down), off the
  same capture.

Then warm it **by driving**, and take the one reading that decides: at
**70–72 °C of oil, loads off**, a minute or two of `IdleHealth` against the
current band **57–100** (`open.md` S1), with the same three groups
logging. Engine off.

**Read beside it, against `open.md` H8's baseline** (warm idle, loads off:
1.3–2.6° at 3.1–3.5 g/s):

- **air mass at idle up, and the plate up with it** → air that used to
  bypass the MAF now goes through it: a leak was sealed (H3/H9);
- **air mass unchanged, only the plate different** → the new throttle and
  its freshly learned stops, nothing more;
- **055's adaptation** read −0.73 g/s on 11/9, the idle having learned
  to take air away. It restarts from zero with the battery out, so it is
  compared **after the repeat below**, once learned again: nearer zero
  says less air was reaching the engine unasked (a sealed leak);
  about −0.7 again says nothing changed there. *The reading of the sign
  is reasoned from the label and the unit, not from a VW document.*
- **032 is not read now.** The battery is out for the job, so every
  adaptation starts from zero; 032 is read once, after a few hundred km
  (`open.md` S9), and an idle cell moving *negative* would also say a leak
  was sealed.

⚠ **Fresh adaptations have read worse before**: 146 and 117 straight after
the 23/9 disconnect, 84 after 24/9's, 57–100 once settled (`open.md` H8,
*The throttle adaptation and the battery disconnects*). **So a first
reading inside or above the band does not yet say "unchanged"** — repeat
it, the same way, after a few days of normal driving before calling it.

**Then:**

- **Idle clearly better** (well below 57 at that temperature, 014 quiet):
  record it; the loose ends in `open.md` can then be closed at leisure.
- **Idle unchanged after the repeat — the expected outcome:** no further
  tests. Go to step 3.

Either way: a look along the new joints after the first warm run, and
again after a few hundred km (the hand-tightened nuts).

## Step 3 — the exhaust, at the garage

A repair visit, not a test visit (H2, S6, S11):

- **the whole exhaust leak-tested and made tight** — manifold, its joint to
  the head, the flange and its gasket, the flex pipe, every joint back;
- **both lambda probes**: seated and tight in their bosses, no leak at
  either.

*One line to ask, since it is the same machine and the same visit:* if they
smoke-test the exhaust, whether they will put the smoke through the intake
too (H3). Not required.

Afterwards: `IdleHealth` at 70–72 °C against the band, as in step 2, with
014 logging.

## Step 4 — decided by step 3's result

The same rule: **idle solved → stop and record; idle unchanged → the next
repair from `open.md`'s ranked candidates**, chosen then, not now.
