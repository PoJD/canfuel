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

## Step 1 — the valve cover job and the throttle body: done 1–2/10/2026

Recorded in `vehicle-history.md`, *The valve cover and throttle job,
1–2/10/2026*, with the check start that followed it; what the job found is
in `open.md` (S10, H8, H9) and `refuted.md` (C14–C16).

**Still owed before session A:**
- **Top up the coolant**, cold — the level dropped a little after the job
  and none was at hand on 2/10.
- **The MAF's orientation, settled by the harness** (`vehicle-history.md`,
  the MAF row): the connector points forward, and whether that is turned
  round is not known. The car's own harness decides it — where its clip
  holder is, and which way the connector reaches it with no strain. Turn
  the housing (two screws) only if the harness says so, and clip it
  either way. Cosmetic by the owner's assessment, so not counted as a
  change to what session A tests.
- At A1, **listen at the timing-belt end**: a noise there on 2/10 went when
  the upper belt cover was refitted (*owner*), and it should stay gone.

---

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
  is still logging after the engine catches (`vcds.md`). On the laptop it
  lands in Downloads, where Claude picks it up afterwards.
- **`IdleHealth` and the start are computed from the ECU's raw frames**,
  not read off anything: with the USBtin connected the MFD is out, and the
  converter, powered through it, is off the bus — **the capture holds no
  0x600–0x604** (*owner*, `CLAUDE.md`, *Recording a session at the car*).
  `tools/idledips.py` computes both from 0x280 and 0x288 afterwards.

### Session A — the cold start and the warm-up drive, one log

**Capture and VCDS 014 + 003 + 055** from before the start to engine off.
003 is air mass and plate angle, 055 the idle regulator and its learned
value; all three carry engine speed, so the log aligns to the capture
(`vcds.md`). **A cold start**: the engine has stood overnight, or all day,
and has not been run since. Note the coolant temperature at the start. The
start's quality **is now measured too** (*owner's decision, 3/10/2026*,
reversing "it is ignored"). That rule was written for the very first start
after the job, with the rail just opened and a new throttle on its first
run, which says nothing about the car. That start happened on 2/10, and the
check starts that day were part-warm, so **A is the first real cold start
on the repaired car**. And the job touched two things a start sees: **the
injectors were taken out and refitted**, and a seat that now leaks drains
the rail over a stand and lengthens the crank, which was the old injectors'
fault (`refuted.md` C3); and **the new throttle** sets the air for the
first seconds, which is the fall after first firing.

**Computed from the capture's raw ECU frames** — 0x280's engine speed and
0x288's coolant — by `idledips.health_summary()`: the same `StartCrank`,
`StartDip` and `StartClt` the firmware puts in 0x604 (`docs/firmware/frames.md`,
*The start*), which is not itself in a capture. The capture starts before
the ignition, so the engine is seen stopped and the crank is timed from its
first turn. Note how long the car stood. Start it the way the earlier ones
were. **Compared with** `refuted.md` C3, the two captured starts in the
same arithmetic (`docs/firmware/frames.md`):

| | stand | coolant | crank to first firing | `StartDip` |
|---|---|---|---|---|
| 24/9 (`19`) | ~19 h | 12 °C | 0.83 s | 118 rpm |
| 25/9 | ~12 h | — | 0.77 s | — (clean) |
| 26/9 | ~10 h | 14 °C | 0.93 s | 74 rpm |
| 11/9 (`18`), old injectors | ~10 h | 16 °C | 1.22 s | 141 rpm, nearly died |

- **Crank about 0.8–0.95 s, dip within 74–118 rpm** → the start is as it
  was on the new injectors; the refit and the throttle did not hurt it.
- **Crank towards 1.2 s or longer** after a night's stand → a seat that
  drains the rail, the same mechanism as C3: the refit is suspect, a leak
  check at the injectors before anything else.
- **Dip clearly below 74** → the start got better, most likely the
  throttle. **Dip near or above 141, or a near-stall** → it got worse.
- ⚠ **One start is noise** (`docs/firmware/frames.md`): only the
  near-stall and a crank past 1.2 s count on their own. Everything else
  is a first point, and each cold morning from now on adds one.

The start decides nothing about the misfires; that stays A2 and A3.

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
- **A3+ — then about an hour's driving, and one last stop hot**
  (*owner's decision, 2/10/2026*): **three minutes standing, loads off**,
  the same three groups. It decides nothing on its own — the verdict
  stays A2 and A3 — but it shows whether the idle settles as the fresh
  adaptations learn. At this stop also: **any smoke or hiss at the back**
  (S11, not seen on the cold check starts).
  **Then, after the three minutes, the MAF wiggle** (*owner's decision,
  3/10/2026*): one short blip of the throttle to mark the moment in the
  capture, then **30–60 s of moving the MAF's connector and harness**
  by hand, still standing, loads off. Afterwards the dips and the grade
  in the wiggle window are set against the three quiet minutes before it,
  and 003's air mass beside them. Dips that cluster in the wiggle, or air
  that drops out, mean the contact; nothing different means the harness
  found unclipped (`vehicle-history.md`, the MAF row) was cosmetic, as
  assessed.
- **A4 — the oil thermometer, the first minute after engine off**, at
  the end of A3+ when the oil is at its hottest (*owner's decision,
  2/10/2026*: **taken, no longer optional** — the Extol is bought;
  `docs/firmware/open.md` question 10). **No cold reading beforehand**
  (*decision*): the instrument is checked hot, in the same minute, on the
  coolant hose below, and a cold engine adds nothing — every surface sits
  at ambient, and the capture's first seconds at ignition-on record the
  cold soak anyway. **The thermometer rides in the cabin** so it is
  acclimatised (its manual: 30 minutes), set to **E 0.95**, with dark matt
  tape on the filter if it is bare metal. No engine running, so it costs
  the idle nothing. **Ignition back on at once** so
  that 0x420 keeps coming and the capture keeps running; **the owner
  writes or dictates the three readings in order into the chat** —
  Claude cannot hear him (*this said "reads aloud"; corrected 2/10/2026*).
  Claude matches them to the minute after engine off, which the capture
  shows as the speed falling to zero; the oil moves far too slowly in
  that minute to matter against a 23 °C gap. **The oil filter first**, then **the sump pan from
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

`IdleHealth` is computed from the capture's 0x280 afterwards
(`idledips.py`), against the band
**57–100** (`open.md` S1), but decides nothing yet: no healthy target for
it exists.

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
  points at which repair* below.
- **Counts** — they were not gone; A's zero was luck: step 2.
- **055's learned value** against the −0.73 g/s of 11/9, and **032's idle
  cell** (`open.md` S9): either moving *negative* also says a leak was
  sealed. Read here for what they are after a day; **a photograph of both
  screens after a few hundred km** is worth having later, but decides
  nothing.

**At B's second stop, after its three minutes — only if both sessions are
zero so far:** **one minute of group 002** as its own short log (VW's idle
limits: air 2.0–5.0 g/s, injection 2.0–5.5 ms, load 15–35 %, `vcds.md`),
then **two minutes with the A/C on**, the capture still running — the
regulator's answer to a load step, the two-hold method of `vcds.md`.

*There used to be a session C for this* — a separate warm recording of the
healthy idle. **Dropped, owner's decision 2/10/2026:** if A and B are both
zero, their warm stops already are the healthy-idle recording that H0 never
had (`open.md` S1, *What is not known: the healthy target*), with the
capture beside them. The two things C added beyond that, 002 and the A/C
step, cost three minutes here instead of a session.

### Afterwards, either way

A look along the new joints after the first warm run, and again after a
few hundred km — **re-tightening the cover's outer nuts**, the ones
reachable with the plenum on (`open.md` S10, *Decision, 1/10/2026*).

### If the idle is fixed: what points at which repair

*Owner's aim, 28/9/2026: indications, not proof — the repair came first.*
With everything done in one job, **the idle itself cannot tell the parts
apart** (the cost accepted when it was planned as one job). What can:

| sign | points at |
|---|---|
| **What the job found** (`vehicle-history.md`): the old breather **sitting loose on a ring that had flowed out of shape**, a **hardened cover gasket under six loose nuts**, **cylinder 2's injector O-ring damaged**, the throttle's vacuum elbow **hard with age**, the old throttle's **idle-stop face worn smaller**. Found whole: both plenum gaskets, the throttle gasket, no protrusion | the part it was found on. **The strongest sign there will be** — the breather's ring and seat first |
| **A1 showed the leak signature** (more air, 055 nearer zero) | a sealed unmetered leak — plenum gasket, breather, hoses, injector seats, the throttle's flange (H3/H9/H8); which one only the photographs say |
| **no leak signature** | the throttle itself (H8) — its routine did not change with the new part (S13 closed), so that sign is gone; the worn idle-stop face is what is left |
| **zero in both sessions, from the first warm reading** | a mechanical change — a leak, a seat, the throttle — rather than anything that has to learn |
| **better, but only to August's level** (`IdleHealth` 48 on 11/8) | the injector seats — only in play since 23/9, while the rough idle is older (S2, S3); anything clearly better than August is something older |

**The one way to split the throttle from the rest — optional, the owner's
call:** the old throttle is kept. Refitted for a day (15 minutes, the
coolant hose, adaptation 098), a returning fault would name it beyond
doubt, and the new one goes back on.

## Step 2 — the exhaust, by the owner

*Owner's decision, 3/10/2026, replacing "at the garage":* if the idle is
not fixed by step 1, **the owner tests and repairs the exhaust himself**
(H2, S6, S11). The garage is the fallback, not the plan.

1. **Make the known joint tight first** — the one behind the converter
   that has never been tight (`open.md` S6), clamped since without
   sealant. It is behind both probes and cannot touch the idle, but the
   test below pressurises the whole exhaust, and a joint that blows there
   is the loudest thing on the car and masks a smaller leak further
   forward.
2. **The tailpipe test**, warm idle, outdoors: the tailpipe closed for
   **2–3 s at a time** — a folded rag in a gloved hand, or a rubber
   bung — while the manifold, its joint to the head, the probe boss and
   the outlet flange are listened to and felt for (a hand near, never on:
   the manifold is far too hot to touch). With the outlet closed the whole
   exhaust is under pressure, so a leak that draws air in at idle (H2)
   now blows out, and hisses or puffs. A helper, or a phone recording at
   the head, since one person cannot do both ends. *All general:* never
   longer than a few seconds, never indoors; a leak that ticks loudest in
   the first minute after a cold start is a crack that closes as it
   warms, so listen then too; dry black soot at a joint is exhaust.
   **Warm and not cold** because a crack in cast iron may only open hot.
   A smoke machine into the tailpipe, cold (`open.md`, *Tools worth
   owning*), shows the place better but cannot see a crack that only
   opens hot; it is the second look, not the first.
3. **If it leaks ahead of the front probe — the manifold, its gasket to
   the head or the probe boss — a new manifold** (*owner's decision*:
   new rather than the old one re-gasketed, once it is off anyway),
   with a new gasket to the head, new nuts, a new gasket at the outlet
   flange, and the probe refitted with anti-seize on its thread.
   - **Which part.** VW numbers the AQY manifold `06A 253 031` plus a
     suffix, and the suffixes differ by model and year: VW Classic Parts
     lists `…AQ` for the AEH/AKL 1.6, while a parts aggregator lists the
     same `…AQ` for a Golf IV AQY. **Neither is taken as fact.** The
     number cast into this car's manifold, read and photographed, or a
     dealer's or mlparts' lookup by VIN, decides it.
   - **What it costs, looked up 3/10/2026** (prices move): new from VW,
     about **€350–490** for the `06A 253 031` family (VW Classic Parts
     €388 for `…AQ`, €485 for `…BP`); **used, 700–1,500 Kč** at Czech
     breakers. No new aftermarket cast manifold for the AQY was found in
     a quick search of Czech shops; worth asking mlparts by VIN before
     paying VW's price. Performance headers were not looked at — not
     wanted.
   - ⚠ *General:* the studs into the head are 26 years old and the one
     real risk of the job. Penetrating oil the days before, heat, and
     patience; a stud that snaps in the head is the point at which it
     goes to a garage after all.
4. **If nothing leaks ahead of the probe**, H2 is refuted for the zone it
   is about and goes to `refuted.md`; the manifold stays.

Afterwards: session A's hot idle again — 014 logging, three minutes at
68–72 °C with the oil watch, `IdleHealth` against the band. *Skipped if
the idle is already fixed by then.*

## Step 3 — only if the idle is still not fixed

The same rule: **idle solved → stop and record.** Otherwise, in this order
(*owner's decision, 29/9/2026; items 1 and 2 swapped 3/10/2026*), each
deciding whether the next is needed:

1. **A vacuum gauge at a warm idle** (`open.md`, *Tools worth owning*),
   teed into **the fuel pressure regulator's vacuum hose** at the front of
   the engine (*owner's choice, 3/10/2026*: the easiest to reach) or the
   brake-servo line — any hose to the manifold **behind the throttle
   plate** reads the same vacuum (*general*). Keep the gauge's hose short,
   or it smooths away the flick a valve makes, and the T-piece tight, or
   it is a leak of its own. A few minutes at idle, warmed by driving. **First because it is cheap and needs nothing built**
   (*owner's decision, 3/10/2026*, swapping it with the smoke test).
   Read against itself, not against a number (*general*):
   - **a steady needle** → no valve and no large leak; go to item 3. ⚠ A
     small leak can still hide under a steady needle, so the smoke test
     stays possible later if nothing else explains the idle;
   - **a regular flick down** at one point in the cycle → a valve (H1);
     the smoke test is not needed, go to item 3 with H1 first;
   - **a low or slowly wandering needle** → a leak or a mixture fault
     (H3, H7): the smoke test follows, to say *where*.
2. **An intake smoke test, done at home — only if item 1 points at a
   leak** (`open.md`, *The idle's candidates, ranked*, row 1 and *Tools
   worth owning*). The engine off
   and cold, so it costs no idle. The leak is still candidate 1 after
   step 1, which replaced parts but tested no joint, and smoke is what
   names *where*.
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
   **None** → the leak is as good as ruled out, and item 3 follows.
   *How to make the smoke is not settled yet* (*owner, 3/10/2026*: the
   machines are too dear); the home-made one above is the candidate.
3. **Then the next repair from `open.md`'s ranked candidates**, chosen
   then, not now.
