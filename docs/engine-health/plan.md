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
**2 is a warm session**: Claude runs the capture, drive until the oil
is at 68–72 °C, stop outdoors, loads off, handbrake on, neutral.

1. **The brake servo, check c — a cold start will do, no drive.**
   - Claude starts the capture; then start the engine.
   - About **two minutes** after the start, once the idle has settled:
     **hold the pedal down firmly for 30 s**, release, wait 30 s, hold
     again 30 s. Nobody else touches anything.
   - Write when you pressed, and anything heard. Engine off.
2. **The exhaust manifold, the same session, straight after.**
   - Close the tailpipe for **2–3 s at a time**, never longer.
   - Meanwhile listen at the manifold, its gasket to the head, the probe
     boss, the outlet flange and the front pipe back to the converter.
     A hand near, never on. Phone recording at each.
   - Listen there also with the tailpipe open, for the sputter (S15),
     and say where it is loudest.
   - **Leaks there → a new manifold**: new gasket to the head, new nuts,
     new outlet gasket, the probe refitted with anti-seize. Part
     `06A 253 031` + suffix: read the number cast into the manifold, or
     ask by VIN. New from VW about €350–490, used 700–1,500 Kč.
     Penetrating oil on the studs the days before; a snapped stud goes to
     a garage.
3. **Vacuum gauge, warm idle**, once one is bought. Tee it into the fuel
   pressure regulator's vacuum hose. Short hose to the gauge, tight
   T-piece. Note what the needle does.
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
**The cylinder 4 knock window stays out of this plan** (*owner's
decision, 9/10/2026*): with no link found between it and the misfires,
G66 and the rest of H5's tests stay in `open.md` as tests, not steps.

## Step 3 — why, and how it is read

**Idle solved → stop and record.** Otherwise each item decides whether
the next is needed.

1. **The brake servo** (*decided 9/10/2026*, H3). It is the one part of
   the intake the smoke could not test (*a and b done 9/10/2026, both
   good — `open.md` H3*): smoke pushed into the manifold
   closes the servo's check valve, so the servo's diaphragm and seals
   behind it were never pressurised (*general*: the valve passes only
   from servo to manifold). A servo that leaks feeds unmetered air into
   the manifold at exactly the idle vacuum. **Pinching its line was the
   first plan and cannot be done**: the line is rigid plastic (*owner*,
   9/10/2026). The three checks are the standard ones (*general*, not
   read for this car): **a** — the pedal sinks when the engine starts,
   or the servo gives no assist; **b** — one or two light presses after
   switch-off, or the check valve or the diaphragm does not hold;
   **c** — no hiss and no dip in engine speed with the pedal held, or
   the diaphragm leaks into the manifold. The dip is read off the
   capture, aligned on the dip itself. **Cold is enough for c**
   (*decided 9/10/2026*): the manifold vacuum the diaphragm sees is an
   idle's either way, and the servo's rubber does not need engine heat
   to leak; two minutes in, the fast-idle step is over, so a dip is not
   confused with it. Two holds, so that one stray dip is not the
   result. It saves a drive, and it keeps the idle short. **All three good** → the servo is
   cleared for H3, which is left with joints that open only hot. **Any
   bad** → the check valve and its line first (cheap), the servo only if
   they are not it. ⚠ **The pedal is soft and long** (*owner*, 9/10) —
   that is hydraulic, not the servo (a servo that fails makes the pedal
   *hard*), so it is not read into any of this (`open.md`, *Other*).
2. **The exhaust ahead of the front probe (H2)** (*reasoned*,
   9/10/2026): `open.md`'s next after H10 now that 2b moved nothing on
   the intake side, the one with a symptom of its own since S15 was
   heard, and free, while the gauge is not yet bought. With the outlet closed, a leak that draws air in at idle blows
   out, and hisses or puffs. Warm, because a crack in cast iron may only
   open hot; never longer than a few seconds and never indoors
   (*general*). The front pipe as far as the converter is listened to as
   well, and the sputter with the tailpipe open, because S15 may sit just
   behind the manifold rather than in it (`open.md` S15) — a new manifold
   answers only a leak in the manifold. A new manifold if it leaks (*owner's decision*,
   3/10/2026); the suffix differs by model and year; the studs into the
   head are 26 years old. **Nothing leaks ahead of the probe** → H2 is
   refuted for its zone and goes to `refuted.md`.
3. **The vacuum gauge** (`open.md`, *Tools worth owning*). A long hose
   smooths away the flick a valve makes. Read against itself (*general*):
   **a steady needle** → no valve and no large leak; **a regular flick
   down** at one point in the cycle → a valve (H1); **a low or slowly
   wandering needle** → a leak or a mixture fault (H3, H7).
4. **The next repair** is chosen then, not now, from `open.md`'s ranked
   candidates.

## Standing items — why

- **The cover's nuts**: the gasket settles (`open.md` S10).
- **The thermometer reading (A4)**: `docs/firmware/open.md` question 10.
  The ignition goes back on so the capture keeps 0x420. The coolant hose
  checks the instrument against 0x288's coolant.
- **The deliberate misfire**: `docs/firmware/open.md` question 11 — 014
  and `IdleHealth` read against a misfire of known rate.
