# Engine health — the planned fixes, in order

**Part 1 is what to do, in order, with no explanation.** It is what goes
to the car. **Part 2 is why, and how the results are read.** Keep it that
way (*owner's decision, 8/10/2026*). An instruction goes in Part 1 and its
reason in Part 2, never mixed. Why each step exists at all lives in
`open.md`; what was done lives in `vehicle-history.md` and `idle-log.md`.
**A step that is done is removed from both parts in the commit that
records it**, and the file is deleted when it is empty.

---

# Part 1 — what to do

## Step 3 — the idle is not fixed

One at a time, Claude says after each whether the next is needed.

1. **G66, the knock sensor for cylinders 3 and 4.**
   - Find it on the block, below the intake.
   - Unplug it. Look at the contacts on both halves for green or white
     corrosion. Photograph them.
   - Undo the bolt, clean the sensor's face and the block where it sits,
     refit it **dry at 20 Nm** with a torque wrench. Photograph it.
   - Plug it back in until it clicks.
   - Then a drive. Claude runs the capture; VCDS logs **020 + 026 +
     003**. At 65–72 °C of oil, standing, neutral, handbrake on, hold
     each speed 10–15 s: **1600, 2000, 2400, 2800, 3200, 3500**, then
     back down to 1600. Then drive on: a dozen **tip-ins after a coast
     and after gearchanges** at 1000–2000 rpm, and **two or three
     full-throttle pulls** through 3000–4000 rpm.
2. **Vacuum gauge, warm idle**, once one is bought. Tee it into the fuel
   pressure regulator's vacuum hose. Short hose to the gauge, tight
   T-piece. Note what the needle does.
3. **The exhaust manifold, warm idle, outdoors.**
   - Close the tailpipe for **2–3 s at a time**, never longer.
   - Meanwhile listen at the manifold, its gasket to the head, the probe
     boss and the outlet flange. A hand near, never on. Phone recording at
     the head.
   - **Leaks there → a new manifold**: new gasket to the head, new nuts,
     new outlet gasket, the probe refitted with anti-seize. Part
     `06A 253 031` + suffix: read the number cast into the manifold, or
     ask by VIN. New from VW about €350–490, used 700–1,500 Kč.
     Penetrating oil on the studs the days before; a snapped stud goes to
     a garage.
4. **The next repair** — Claude picks it from `open.md` then.

## Standing items

- **After a few hundred km:** re-tighten the cover's outer nuts you can
  reach with the plenum on, and look along the joint.
- **When there is a thermometer, at the end of a hot captured session:**
  engine off; ignition straight back on; within a minute measure the oil
  filter, the sump from beneath and the upper coolant hose; write the
  three readings into the chat in that order.
- **Once the idle is solved:** one injector unplugged for a minute at a
  warm idle, with 014 logged.

---

# Part 2 — why, and how it is read

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

**Where it stands:** steps 2a–2c are done and recorded (`idle-log.md`,
9/10/2026). The intake is tight cold, the misfires remain at every warm
stop on settled adaptations, and nothing a sealed leak would move —
003's air, the plate, 055's learned value — moved (`open.md` S3, H10).

## Step 3 — why, and how it is read

**Idle solved → stop and record.** Otherwise each item decides whether
the next is needed.

1. **G66 first** (*owner's decision, 9/10/2026*: cheap, and the vacuum
   gauge is not bought yet). **An exception to the rule above, made
   knowingly**: G66 is the cylinder 4 knock window (S4, S5), not the idle
   (`refuted.md` A10). It is next in H5's list now that 2c cleared the
   injectors (`refuted.md` B7). The 20 Nm is VW's figure (*general*, H5);
   too loose a sensor couples less of the block and reads a different
   noise floor, and a corroded contact reads one cylinder pair wrong. Dry,
   because anything between sensor and block changes what it hears
   (*general*). **The befores** are 2c's: `vcds-step2c-020-026-003.csv`
   for the holds and the drive, with `vcds-neutral-026-003.csv` and
   `-clamp.csv` behind it. **What it says** (`open.md` H5): cylinder 4's
   020 events gone or spread, and its 026 excess over cylinder 1 gone in
   the holds → G66 was it. Unchanged → the loose bracket at ~3000 rpm in
   neutral is next, when the idle allows.
2. **The vacuum gauge** (`open.md`, *Tools worth owning*). A long hose
   smooths away the flick a valve makes. Read against itself (*general*):
   **a steady needle** → no valve and no large leak; **a regular flick
   down** at one point in the cycle → a valve (H1); **a low or slowly
   wandering needle** → a leak or a mixture fault (H3, H7).
3. **The exhaust ahead of the front probe (H2)**, the top of
   `open.md`'s ranking after H10 now that 2b moved nothing on the intake
   side. With the outlet closed, a leak that draws air in at idle blows
   out, and hisses or puffs. Warm, because a crack in cast iron may only
   open hot; never longer than a few seconds and never indoors
   (*general*). A new manifold if it leaks (*owner's decision*,
   3/10/2026); the suffix differs by model and year; the studs into the
   head are 26 years old. **Nothing leaks ahead of the probe** → H2 is
   refuted for its zone and goes to `refuted.md`.
4. **The next repair** is chosen then, not now, from `open.md`'s ranked
   candidates.

## Standing items — why

- **The cover's nuts**: the gasket settles (`open.md` S10).
- **The thermometer reading (A4)**: `docs/firmware/open.md` question 10.
  The ignition goes back on so the capture keeps 0x420. The coolant hose
  checks the instrument against 0x288's coolant.
- **The deliberate misfire**: `docs/firmware/open.md` question 11 — 014
  and `IdleHealth` read against a misfire of known rate.
