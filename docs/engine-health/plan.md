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
**1 and 2 are one warm session**: Claude runs the capture, drive until
the oil is at 68–72 °C, stop outdoors, loads off, handbrake on, neutral.

1. **The brake servo hose.**
   - VCDS: start a log, **groups 003 + 055 + 014**. Start a stopwatch
     at the same moment.
   - Do not touch the brake pedal until the end.
   - **0:00–1:00** hose free. **1:00–2:00** pinched. **2:00–3:00** free.
     **3:00–4:00** pinched. **4:00–5:00** free. Then stop the log.
   - Pinch it **close to the manifold**, with hose-clamp pliers or with
     pliers over a folded rag, so the hose is not cut.
   - Write into the chat if the engine speed or the sound changed while
     pinched.
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

1. **The brake servo hose** (*decided 9/10/2026*, H3). It is the one
   part of the intake the smoke could not test: smoke pushed into the
   manifold closes the servo's check valve, so the servo's diaphragm and
   seals behind it were never pressurised (*general*: the valve passes
   only from servo to manifold). A servo that leaks feeds unmetered air
   into the manifold at exactly the idle vacuum. Pinched shut, that air
   stops: **003's air rises and 055's live regulator moves positive by the
   same amount**, while the ECU replaces through the throttle what the
   leak used to give. **014 alone cannot say it** — it is a yes/no witness
   and needs minutes, so it is logged only as a bonus. **Fixed one-minute
   windows** from the log's own clock, so no alignment is needed; two
   pinched windows so that one drift is not read as a result. **Read:** a
   shift of **0.2 g/s or more, the same way in both pinched windows and
   back in the free ones** → the servo, its check valve or that hose
   leaks: replace what leaks. Less → the servo is cleared, and H3 is left
   with joints that open only hot. Pinched near the manifold so the
   whole hose is on the servo's side. The pedal stays still because a
   brake application lets air into the servo and would move 055 on its
   own (*general*).
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
