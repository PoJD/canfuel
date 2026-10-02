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
- **`IdleHealth` comes from the capture, not the MFD**: the two are one or
  the other, never both (*owner*, `CLAUDE.md`, *Recording a session at the
  car*). Nobody reads it off the display during a captured session.

### Session A — the cold start and the warm-up drive, one log

**Capture and VCDS 014 + 003 + 055** from before the start to engine off.
003 is air mass and plate angle, 055 the idle regulator and its learned
value; all three carry engine speed, so the log aligns to the capture
(`vcds.md`). **A cold start**: the engine has stood overnight, or all day,
and has not been run since. Note the coolant temperature at the start. The
start's quality is not what is tested — **it is ignored.**

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

`IdleHealth` is read out of the capture afterwards, against the band
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
