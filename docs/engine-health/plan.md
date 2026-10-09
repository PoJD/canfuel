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
   - **Still cold, engine off: a dry run for step 3.** Unplug and plug
     back injector connectors **1 and 4** once each, by the connector
     body with the clip pressed — **never by the wires**. Write whether
     it goes one-handed in a glove in a few seconds.
   - **Same time: the plug leads, one at a time, 4 first.** Pull the boot
     off, look at the metal contact inside and at the top of the plug.
     Photograph both, and the plug's ceramic where its make is printed.
     Is the top of the plug a solid post or a nut on a thread? If a nut,
     is it tight by finger? Push the boot back on: **does it click?**
     Write it for each of the four. **Change nothing.**
   - **Nothing found cold → the same again warm**, after a drive to
     68–72 °C of oil.
   - **Leaks there → a new manifold, after step 3**: new gasket to the head, new nuts,
     new outlet gasket, the probe refitted with anti-seize. Part
     `06A 253 031` + suffix: read the number cast into the manifold, or
     ask by VIN. New from VW about €350–490, used 700–1,500 Kč.
     Penetrating oil on the studs the days before; a snapped stud goes to
     a garage.
3. **Injectors 1 and 4 in turn, warm idle — on up to three separate
   days.**
   - Drive until the oil reads 68–72 °C. Stop, neutral, handbrake on,
     loads off. Claude runs the capture; VCDS on **014, 055, 003**.
   - If step 2 needs its warm run, do it first, on this same stop.
   - **1 min** as it is.
   - **In this order: 1, 4, 4, 1.** Cylinder 1 is at the timing-belt end.
     Each time: connector off **1 min**, back on, **30 s** as it is.
   - **1 min** as it is, engine off.
   - Write the time of every off and on into the chat. The engine light
     will come on, maybe flashing: carry on.
   - Clear the fault memory with VCDS.
   - **Claude says after each day whether another is needed.** At most
     three days.
   - **If it cannot be done warm:** the same on a cold start, beginning
     about 2 minutes after the start.
4. **Spray test at the intake, warm idle** — on the same warm stop as
   step 3, after it, with the capture still running.
   - A short burst of **unlit propane** (or brake cleaner) at one joint
     at a time: the throttle flange, the plenum's joints, the hoses and
     vacuum lines at the back, the servo line, the breather hose. Say
     "teď" and the place each time, and wait 10 s between.
   - **Never towards the exhaust side or its heat shield**; a fire
     extinguisher within reach.
   - Write any place where the engine speed changed.
5. **High-voltage side in the dark, a damp evening, warm idle.**
   - Bonnet open, lights off: look along the leads and the coil for a
     spark or a blue glow.
   - Then a fine water mist over one lead at a time, and the coil.
     Hands and the bottle clear of the leads.
   - Write anything seen, and which lead the engine stumbled at.
6. **Vacuum gauge, warm idle**, once one is bought. Tee it into the fuel
   pressure regulator's vacuum hose. Short hose to the gauge, tight
   T-piece. Note what the needle does.
7. **The next repair** — Claude picks it from `open.md` then.

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
   9/10/2026): `open.md`'s first candidate when this was written (since 9/10 second, behind H3, now that the dips keep to one cylinder — but still the one with symptoms of its own), and next now that 2b moved nothing on
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
3. **Injectors 1 and 4** (*the owner's proposal, 9/10/2026*; `open.md`,
   *Naming the cylinder*). It is also `docs/firmware/open.md` question
   11's deliberate misfire, brought forward at the owner's decision the
   same day. With a connector off, that cylinder gets no fuel, so the
   converter sees air and not fuel (*general*); the light comes on because
   a quarter of the firings missing is far above the 2 % VW stores a code
   at (`vcds.md`, *What VW says*), and the rate that damages a converter
   flashes it (SSP 175) — VW does not publish this ECU's figure.
   - **Why it can name a cylinder at all.** The idles already show the
     dips keeping to one slot (`open.md`, *The dips keep to one slot*),
     but the bus cannot say which cylinder a slot is. While a cylinder is
     out its slot is known, and the firing order 1-3-4-2 names the other
     three: **cutting 1 names 3, 4 and 2; cutting 4 names 2, 1 and 3.** So
     the two outer cylinders name all four, and 2 and 3 are named by both
     cuts — the two must agree about them, which is the check.
     (*Decided 9/10/2026*, the owner's question: 2 and 3 are hard to
     reach, and they are not needed.) The one assumption, stated rather
     than proved: a dip shows in its cylinder's slot with the same lag as
     the dead stroke's deficit.
   - **Why up to three days.** The idles put roughly 45 % of the dips on
     one cylinder (or 40 % each on two neighbours in the firing order),
     about 1.8 times its share — a real effect but not a large one, so it
     takes many dips. Simulated with `tools/cutscan.py` at 6–10 dips a
     minute (*decided 9/10/2026*): the named cylinder comes out right in
     0–47 % of trials on one day's four cut-minutes, 25–83 % on twelve,
     and 58–92 % on all four cylinders for sixteen; a cylinder carrying
     three quarters or more is found on one day. Three days of 1, 4, 4, 1
     are twelve cut-minutes without any one idle growing past about
     7 minutes, which keeps to the rule. The days are pooled.
   - **`tools/cutscan.py` reads the whole test**, all days together: it
     finds the cuts in the capture, counts, applies the rules below and
     prints the verdict; it stops rather than guess if it finds a
     different number of cuts than the order names.
   - **The criteria, fixed before the test** (*decided 9/10/2026*, so the
     result cannot be read to fit; *revised the same day*, before any
     run, when the dips were found to keep to one slot — the earlier
     version compared the cuts with each other first, which simulation
     showed would find a 45 % cylinder only 14–28 % of the time):
     1. **By name — the main reading.** Dips counted on the three firing
        cylinders, named from the dead slot, the first 5 s of each cut
        out; each a stroke 20 rpm below its own cylinder's neighbours.
        **One cylinder** if its rate is the highest at p < 0.05 against
        every cylinder alike (an exact multinomial on the counts, given
        their total and each cylinder's strokes), **and** it is the
        highest in both halves of the pooled cuts.
     2. **Air — a steadily weak cylinder.** 003's air over the last 40 s
        of each cut, its ignition angle beside it (the idle control uses
        both). **Weak** if one cut needs **≥ 0.15 g/s less** than the
        other, in both halves — about 10 % less work from that cylinder
        (*reasoned*: cutting a healthy one needs ~1.1 g/s more, a 10 %
        weaker one ~0.14 g/s less than that). Only 1 and 4 can be weighed
        this way.
     3. **No cylinder stands out** if the named rates give p > 0.2 after
        three days. That rules out one carrying three quarters or more,
        **not a smaller share**, and it is recorded that way.
     4. **Anything between is undecided** after three days — not a reading
        stretched to fit. The cuts compared with each other are printed
        as a secondary reading and decide nothing.
   - **What each outcome points at:** a cylinder named → that cylinder:
     its plug and lead, its injector, its runner (H3), its valves (H1);
     air weak too → a steady fault there (a valve, a runner leak) rather
     than an intermittent one; nothing → the whole engine (H0, H2, H4,
     H7, H8).
   - **The names hold only while a cylinder is out.** The bus loses the
     cylinder phase every few seconds — whenever two strokes quantise to
     the same 0.25 rpm (`idledips.cylinder_runs`; on `30` the phase held
     a median 3 s, at most 16 s). So they cannot be carried into the
     four-cylinder minutes or into earlier captures. *Corrected 9/10/2026*:
     this said the names would hold "in this capture and every earlier
     one".
   - **The dry run and the cold fallback** (*decided 9/10/2026*: the
     owner doubts the connectors can be handled hot). The injectors sit
     on the intake side, away from the manifold, which at a warm idle is
     warm rather than hot (*general*, not measured here); the dry run
     says whether a glove is enough. The connectors are taken by the
     body because the harness is 26 years old (`open.md` H7 test 3): a
     wire torn here would be a new fault no reading could tell apart.
     **Cold is the worse version**: the fast idle must be over first; 014
     hardly counts cold, so question 11's reading is lost; the regulator
     drifts as the engine warms, so the air criterion is weaker; a lifter
     that shows only on warm oil (H1) cannot show. The dips are more
     numerous cold, so criterion 1 may if anything do better. The plug
     lead of a cylinder is **never** pulled instead: that sends fuel to
     the converter.
   - Question 11's own reading — 014 and `IdleHealth` against a misfire
     of known rate — comes from the same minutes.
   **Before any new manifold** (*decided 9/10/2026*): it is free, and the
   manifold is the bigger job — a cylinder named here would change what
   the manifold is expected to fix. Step 2's warm run shares its drive.
   **The plug leads at the dry run** (*decided 9/10/2026*, `open.md` H4,
   1d): plug 4's terminal was burnt black on 1/10, which is what a boot
   contact that does not grip leaves (*general*), and the owner has never
   heard the boots click home. Their contacts have never been looked at,
   only the leads' resistance; all four, so that 4 is compared with the
   others rather than with nothing. Nothing is changed before
   step 3.3, so that the test can still name the cylinder: a new plug
   first would leave no way of telling whether it was the cause. If 4 is
   named, plug 4 and lead 4 are the first repair, and `cutscan.py
   --pairs` on an ordinary warm idle afterwards says whether the dips
   stopped keeping to one slot.
4. **The spray test** (`open.md` H3 test 1, *decided 9/10/2026*). What
   is left of H3 after the cold smoke of 9/10 is a joint that opens only
   hot, which smoke into a cold, stopped engine cannot find; and the back
   of the intake has never been sprayed. A leak there draws the gas in
   and the engine speed moves at that spot (*general*). Free, and on the
   same warm stop as step 3, so no extra idling for the warm-up. Away
   from the exhaust because both gases burn and the manifold at idle is
   hot enough to light them (*general*).
5. **The high-voltage side** (`open.md` H4 test 1e, *decided 9/10/2026*):
   the roughest reading on record came on a foggy morning (S1), and the
   moisture a tracking boot or coil needs is what the mist supplies.
   The leads were measured and the coil is new, which is why it is late
   in the order; it is free.
6. **The vacuum gauge** (`open.md`, *Tools worth owning*). A long hose
   smooths away the flick a valve makes. Read against itself (*general*):
   **a steady needle** → no valve and no large leak; **a regular flick
   down** at one point in the cycle → a valve (H1); **a low or slowly
   wandering needle** → a leak or a mixture fault (H3, H7).
7. **The next repair** is chosen then, not now, from `open.md`'s ranked
   candidates.

## Standing items — why

- **The cover's nuts**: the gasket settles (`open.md` S10).
- **The thermometer reading (A4)**: `docs/firmware/open.md` question 10.
  The ignition goes back on so the capture keeps 0x420. The coolant hose
  checks the instrument against 0x288's coolant.
