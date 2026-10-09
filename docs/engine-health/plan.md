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
**1 and 2 are one cold start**, outdoors, handbrake on, neutral, loads
off; Claude runs the capture throughout.

1. **The brake servo, check c — a cold start will do, no drive.**
   - Claude starts the capture; then start the engine.
   - About **two minutes** after the start, once the idle has settled:
     **hold the pedal down firmly for 30 s**, release, wait 30 s, hold
     again 30 s. Nobody else touches anything.
   - Write when you pressed, and anything heard.
2. **The exhaust manifold, straight after, still cold.**
   - Phone recording, laid in the engine bay by the manifold; later
     under the car by the front pipe.
   - At the tailpipe, **say aloud "teď"** and close it for **2–3 s**,
     never longer. Five times, a few seconds apart.
   - Move the phone under the car by the front pipe and do the five
     again.
   - **Afterwards, play both recordings back yourself** and write whether
     a hiss or a puff comes up at each "teď", and on which recording.
   - Then, tailpipe open, say whether the sputter (S15) is louder
     **from above in the engine bay or from under the car**. Engine off.
   - **Cold, engine off: photograph from below** whatever the phone
     reaches — the flange under the manifold, the front pipe back to the
     converter, the probe if it shows. **Black soot streaks** at a joint
     mark a leak. The manifold itself is under its heat shield: leave it.
   - **Nothing found cold → the same again warm**, after a drive to
     68–72 °C of oil.
   - **Leaks there → a new manifold, after step 3**: new gasket to the head, new nuts,
     new outlet gasket, the probe refitted with anti-seize. Part
     `06A 253 031` + suffix: read the number cast into the manifold, or
     ask by VIN. New from VW about €350–490, used 700–1,500 Kč.
     Penetrating oil on the studs the days before; a snapped stud goes to
     a garage.
3. **The injectors one at a time, warm idle** — only if the injector
   connectors can be reached with the plenum on. If not, skip it and say so.
   - Drive until the oil reads 68–72 °C. Stop, neutral, handbrake on,
     loads off. Claude runs the capture; VCDS on **014, 055, 003**.
   - If step 2 needs its warm run, do it first, on this same stop.
   - **1 min** as it is.
   - **Two rounds, in this order: 1, 2, 3, 4, then 4, 3, 2, 1.**
     Cylinder 1 is at the timing-belt end. Each time: connector off
     **1 min**, back on, **30 s** as it is.
   - **1 min** as it is, engine off.
   - **If 2 and 3 cannot be reached:** only 1 and 4, in the order
     **1, 4, 4, 1**, the same 1 min off and 30 s on.
   - Write the time of every off and on into the chat. The engine light
     will come on, maybe flashing: carry on.
   - Clear the fault memory with VCDS.
4. **Vacuum gauge, warm idle**, once one is bought. Tee it into the fuel
   pressure regulator's vacuum hose. Short hose to the gauge, tight
   T-piece. Note what the needle does.
5. **The next repair** — Claude picks it from `open.md` then.

## Standing items

- **After a few hundred km:** re-tighten the cover's outer nuts you can
  reach with the plenum on, and look along the joint.
- **When there is a thermometer, at the end of a hot captured session:**
  engine off; ignition straight back on; within a minute measure the oil
  filter, the sump from beneath and the upper coolant hose; write the
  three readings into the chat in that order.

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
003's air, the plate, 055's learned value — moved (`open.md` S3; `refuted.md` C19).
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
   9/10/2026): `open.md`'s first candidate since H10 closed (9/10, `refuted.md` C19), and next now that 2b moved nothing on
   the intake side, the one with a symptom of its own since S15 was
   heard, and free, while the gauge is not yet bought. With the outlet closed, a leak that draws air in at idle blows
   out, and hisses or puffs. Warm, because a crack in cast iron may only
   open hot; never longer than a few seconds and never indoors
   (*general*) — **but cold first** (*decided 9/10/2026*): the owner
   hears S15 cold too, so a leak that sputters cold can be found cold,
   and the drive is needed only if cold finds nothing. The owner works
   alone, so the phone listens at the manifold while he closes the
   tailpipe, and his "teď" marks each closure on the audio. Claude
   cannot hear the recordings (and this laptop cannot decode a phone's
   audio), so the owner listens back and reports; each closure
   also loads the engine and shows on the capture as a dip in engine
   speed, which places it in time but says nothing about where a leak
   is. **The joints cannot be told apart by ear** — they cannot be
   reached (*owner*, 9/10/2026) — so the sound only says engine bay or
   underbody, and **the photographs do the locating**: an exhaust leak
   leaves a black soot trail where it blows out (*general*), and a
   photograph outranks every other source here. **The manifold and its
   joint to the head sit under the heat shield** and cannot be seen or
   photographed (*owner*, 9/10/2026), so the photos cover only the flange
   and the pipe below it. **How it is read** (*decided 9/10/2026*): soot
   below → that joint; louder from the engine bay with nothing below →
   the manifold or its joint to the head, which is the owner's standing
   decision of a new manifold (3/10/2026), the shield coming off then
   anyway; nothing either way → warm, then a garage with a lift. The front pipe as far as the converter is listened to as
   well, and the sputter with the tailpipe open, because S15 may sit just
   behind the manifold rather than in it (`open.md` S15) — a new manifold
   answers only a leak in the manifold. A new manifold if it leaks (*owner's decision*,
   3/10/2026); the suffix differs by model and year; the studs into the
   head are 26 years old. **Nothing leaks ahead of the probe** → H2 is
   refuted for its zone and goes to `refuted.md`.
3. **The injectors one at a time** (*the owner's proposal, 9/10/2026*;
   `open.md`, *Naming the cylinder*, method 2). It is also
   `docs/firmware/open.md` question 11's deliberate misfire, brought
   forward from "once the idle is solved" at the owner's decision the same
   day and run for all four cylinders instead of one. With a connector
   off, that cylinder gets no fuel, so the converter sees air and not fuel
   (*general*); the light comes on because a quarter of the firings missing
   is far above the 2 % VW stores a code at (`vcds.md`, *What VW says*),
   and the rate that damages a converter flashes it (SSP 175) — VW does not
   publish this ECU's figure. **How it is read** (*reasoned*):
   - **055 and 003** — how much air the idle regulator adds to hold its
     speed with each cylinder out. The least is the weakest cylinder.
     Engine speed alone says little: the regulator restores it in seconds.
   - **The dips (S1) on the three that still fire**, from the capture,
     with the dead cylinder's slot taken out (`idledips.py` gets that
     when there is a capture). A cylinder that carries the stumble leaves
     the other three nearly smooth when it is out; the others do not.
     Three cylinders run at more load each, and load calms this idle, so
     the dips fall every time — only the four cuts compared with each
     other mean anything.
   - **Two rounds, the second reversed** (*decided 9/10/2026*): two
     minutes a cylinder, the reversal cancels a slow drift of temperature
     through the test, and a result must hold in both rounds. 30 s
     between cuts lets the regulator and the lambda settle.
   - **The criteria, fixed before the test** (*decided 9/10/2026*, so the
     result cannot be read to fit). Reasoned from the data, not from a
     source: at a warm idle on settled adaptations the dips ran 12 ± 3.3
     a minute (`30`, nine one-minute windows — Poisson-like; `28` was
     three times as scattered), and 003's air 3.14 g/s with a 40 s mean
     scattering ±0.04 g/s (`30`, A3). A simulated round at 6–10 dips a
     minute finds a cylinder carrying all the dips every time, one
     carrying three quarters 77–94 % of the time at two minutes (36–62 %
     at one), half rarely.
     1. **Dips — an intermittent cylinder.** Dips counted on the three
        firing cylinders, the dead slot out, the first 5 s of each cut
        out. **One cylinder** if its cut leaves the fewest, at p < 0.05
        against equal shares (the four counts as one multinomial, given
        their total), **and** it is the fewest in both rounds.
     2. **Air — a steadily weak cylinder.** 003's air over the last 40 s
        of each cut, its ignition angle beside it (the idle control uses
        both). **Weak** if its cut needs **≥ 0.15 g/s less** than the
        mean of the other three, in both rounds — about 10 % less work
        from that cylinder (*reasoned*: cutting a healthy one needs
        ~1.1 g/s more, a 10 % weaker one ~0.14 g/s less than that).
     3. **Not one cylinder** if the dips give p > 0.2 and the air differs
        by under 0.08 g/s. That rules out one cylinder carrying three
        quarters or more of the dips, or one 10 % weak — **not a smaller
        share**, and it is recorded that way.
     4. **Anything between is undecided** — at most one more round, not a
        reading stretched to fit.
   - **What each outcome points at:** dips and air on the same cylinder →
     that cylinder (H1, H3 at its runner, its plug and lead); dips alone →
     an intermittent fault there (ignition, injector, valve); air alone →
     a weak cylinder that is not the stumble; neither → the whole engine
     (H0, H2, H4, H7, H8).
   - **The dead cylinder names the slots only while it is out.** Its
     stroke is a huge dip once every four, but the bus loses the cylinder
     phase every few seconds — whenever two strokes quantise to the same
     0.25 rpm (`idledips.cylinder_runs`; on `30` the phase held a median
     3 s, at most 16 s). So the names cannot be carried into the
     four-cylinder minutes or into earlier captures, and the dips cannot
     be put to cylinders one by one: comparing the cuts is the only way.
     *Corrected 9/10/2026*: this said the names would hold "in this
     capture and every earlier one".
   - **Only 1 and 4** (if 2 and 3 cannot be reached): the same criteria,
     1 against 4 directly. It can say *1* or *4*; it **cannot** say *not
     one cylinder* — a culprit at 2 or 3 makes the two cuts alike, which
     is also what four alike cylinders do — so "alike" is recorded as
     "not 1 and not 4". Question 11's reading needs only one cut and is
     whole either way. The plug lead of 2 or 3 is **not** pulled instead:
     that sends fuel to the converter.
   - Question 11's own reading — 014 and `IdleHealth` against a misfire
     of known rate — comes from the same minutes.
   About 13 minutes of warm idle, against the rule; the owner's call, and
   the converter is not at risk with the fuel off. **Before any new
   manifold** (*decided 9/10/2026*): it is free, and the manifold is the
   bigger job — a cylinder named here would change what the manifold is
   expected to fix. Step 2's warm run shares its drive.
4. **The vacuum gauge** (`open.md`, *Tools worth owning*). A long hose
   smooths away the flick a valve makes. Read against itself (*general*):
   **a steady needle** → no valve and no large leak; **a regular flick
   down** at one point in the cycle → a valve (H1); **a low or slowly
   wandering needle** → a leak or a mixture fault (H3, H7).
5. **The next repair** is chosen then, not now, from `open.md`'s ranked
   candidates.

## Standing items — why

- **The cover's nuts**: the gasket settles (`open.md` S10).
- **The thermometer reading (A4)**: `docs/firmware/open.md` question 10.
  The ignition goes back on so the capture keeps 0x420. The coolant hose
  checks the instrument against 0x288's coolant.
