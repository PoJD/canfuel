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

⚠ **Keep the battery connected through step 2a.** If a repair needs it
off, say so before step 2b.

## Step 2a — the smoke tests, engine off and cold

**The intake**
1. Smoke tester: Lincos `MG78016`, 5–35 ml of **the smoke oil supplied
   with it**. Do not mix it with any other oil. Nothing flammable in it,
   no workshop air.
2. Ignition off. **Take the MAF out**: unplug it, take it off the airbox
   and off the hose. Keep it bagged, away from the car, until both smoke
   tests are done.
3. Clamp a glove or bag into the open end of the hose to the throttle.
   Leave the airbox's outlet open.
4. Take the vacuum hose off the fuel pressure regulator. Feed the smoke
   in there.
5. Hold the throttle open with a string on the cable or a hand on the
   quadrant.
6. Smoke for a few minutes. With a torch, look at:
   - the throttle's flange and its hose clamp
   - the upper-to-lower plenum joint
   - the four injector seats
   - the hoses at the back: brake servo, the old secondary-air vacuum line
   - the brake servo's valve
   - the breather, its hose and the hose's plastic connector
   - the oil filler, the dipstick (top and foot in the block), the cover
     joint
   - the airbox's open outlet
7. Photograph every place smoke comes out, and note whether it is a wisp
   or a steady stream.

**The exhaust**, with the same tester
1. Smoke into the tailpipe. Close the gap round the hose with a rag or
   tape. Give it time.
2. Look at:
   - the manifold itself
   - its gasket to the head
   - the front lambda probe's boss
   - the manifold's outlet flange
   - the joint behind the converter, and anything behind it
   - the airbox's open outlet
3. Photograph every place smoke comes out.
4. Only now: the MAF back in, the hose back on.

**Afterwards:** repair whatever leaked on the intake. Smoke at the
manifold, its gasket or the probe boss → go straight to step 3.2's
manifold decision. Then step 2b.

## Step 2b and 2c — one drive

**At home, the night before:** the battery stays connected. No 098.

**On the laptop, before the ignition**
1. `git pull`.
2. Claude starts the capture:
   `python tools/usbtin_capture.py --seconds 3600 --out <session>_z1.txt`
3. Second `cmd` window, yours: `python tools\oilwatch.py <session>_z1.txt`
4. VCDS: start a log, **groups 014 + 055 + 033**.
5. Start the engine. Check that VCDS is still logging.

**2b — the idle stops, loads off at every stop**
1. **A1:** stand 2–3 minutes. Look at whatever 2a repaired. Drive off.
2. **A2:** drive normally, no hard driving. Stop at **56–62 °C oil**
   (three beeps = 90 s to go). Stand until the long beep, about 2 minutes.
3. **A3:** drive normally. Stop at **68–72 °C oil**. Stand 3 minutes.
   Aim for the lower edge of each band.

**2c — knock, straight on from A3, engine running, capture running**
1. VCDS: stop the log. Start a new one, **groups 020 + 026 + 003**.
   Quickly.
2. Still standing, **neutral, handbrake on**. Hold each speed 10–15 s:
   **1600, 2000, 2400, 2800, 3200, 3500**, then **3200, 2800, 2400, 2000,
   1600**.
3. Drive on:
   - a dozen or more **tip-ins after a coast, and after gearchanges**, at
     1000–2000 rpm;
   - where the road allows, **two or three full-throttle pulls through
     3000–4000 rpm**.

**At the end**
1. Engine off.
2. Claude stops the capture and closes the USBtin's channel.
3. Ignition on, **photograph 032**.
4. Upload both VCDS logs (Downloads) and the photo.

**Session B, the same day, only if Claude says so** (Part 2): cool down
to below 45 °C oil, then 2b again (A1–A3, with 014 + 055 + 033), no 2c.

## Step 3 — only if the idle is still not fixed

One at a time, Claude says after each whether the next is needed.

1. **Vacuum gauge, warm idle.** Tee it into the fuel pressure regulator's
   vacuum hose. Short hose to the gauge, tight T-piece. Note what the
   needle does.
2. **The exhaust manifold, warm idle, outdoors.**
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
3. **The next repair** — Claude picks it from `open.md` then.

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

**Where it stands:** the valve cover, throttle and breather job and the
cover joint are done and recorded (`vehicle-history.md`, `idle-log.md`);
the three sessions after them are in `open.md` S3. The misfires remain,
and they follow 055's learned idle air value (`open.md` H10) — the
likeliest reason the ECU learns air away being air the plate did not let
in.

**Why the battery stays connected.** The learned value has settled at
about −1.1 g/s, and that is what makes step 2b readable in one session.
With the battery off, 2b's stops count only once the learned value is
past −0.93 again — **or once it plainly is not going there**: on 4/10,
from zero, it took about 35 minutes of driving and stops to pass −0.93. A
learned value that stays well short of that after as long is a result in
itself (H10: air the plate did not let in is gone).

## Step 2a — why, and what the smoke means

*Owner's decision, 4/10/2026:* **next, whatever H10 turns out to
be** — the misfires are there either way, and the smoke says
where air gets in, which H10 cannot. It also looks for the hiss the owner
hears and cannot place (`open.md` S11). Engine off and cold, so it costs
no idle.

**The dipstick tube is refitted** (9/10/2026, `open.md` H3, *The
dipstick tube*), so smoke at the dipstick now means something.

**The intake** (*general practice, not VW's*):
- **the tester** has its own pump because the owner has no aquarium pump
  (*owner*, 4/10/2026). The pressure only has to make the smoke flow;
- **the supplied oil**: the tester came with its own bottle, labelled in
  Chinese as smoke oil for smoke leak testers (*owner*, photos,
  8/10/2026). Its notes say: for smoke testers only, not to be mixed
  with other substances, and old liquid poured out before new is added.
  So nothing else is bought. Had it been needed, the choice was baby oil
  reading `Paraffinum Liquidum`, never a plant oil, which gums on the
  heater (*general*). The Weleda calendula oil at hand is sesame oil, and
  bicycle brake mineral oil carries additives and dye. Both were ruled
  out;
- **not through the MAF**: oil smoke over its sensing element is the one
  thing here that can spoil a part (*general caution*). **It comes out
  altogether** (*owner's decision, 8/10/2026*), not just off the hose,
  because smoke can reach it from the airbox side too. **Two routes
  into the airbox.** The thin line from the intake manifold runs through
  N112, the electric valve, to the combination valve's control side, the
  valve the pump blows through. **N112 vents into the airbox** (*owner*,
  8/10/2026). Both valves are probably original (*owner*), and neither
  was ever tested for passing smoke. A8 tested only that the combination
  valve seals against exhaust and that the line passed no air when cold
  (`refuted.md` A8).
  - **Through N112's vent** (*reasoned*). Unpowered, N112 should block
    the manifold and vent the control line into the airbox. If it passes
    manifold to vent, smoke comes straight out in the airbox, and **this
    needs N112 alone**. At idle it would also be a small unmetered leak:
    manifold vacuum drawing filtered air from the airbox past the MAF.
  - **Through the pump** needs N112 *and* the combination valve's control
    side to pass, into the pump's path and back through the pump. That
    takes both valves at once (*owner*, 8/10/2026), so it is the
    unlikely one.

  **Smoke at the airbox's open outlet** therefore points at N112 first.
  *Corrected 8/10/2026, twice: first N112's vent was taken as said by the
  owner before he had said it, then it was withdrawn; the owner has since
  confirmed it.* The MAF out also
  leaves the MAF-to-hose clamp untested. It holds by the owner's check, is a
  rubber-lined pipe clamp rather than VW's, and was sprayed at a warm
  idle on 26/9 with no change (`open.md` H3, *Spray test*; `idle-log.md`,
  *The MAF*). The throttle end, refitted since, is inside the smoke;
- **the regulator's hose** (*owner's choice*: at the front, the easiest
  to reach) puts the smoke into the manifold behind the plate; the
  brake-servo hose would do the same. **No fuel in it** (*owner*,
  4/10/2026): it was off several times during 1–4/10 and never smelled of
  petrol, so the regulator's diaphragm is not leaking into the manifold
  (*general*: that is how such a leak shows);
- **the throttle held open** so the smoke fills both sides of the plate;
- **the back** is what no spray ever reached;
- **smoke at the oil filler, the dipstick or the cover joint is a leak
  too**, of the crankcase: the breather joins the crankcase to the intake
  behind the MAF, so wherever smoke leaves the crankcase, air gets in at
  idle unmetered. It is a smaller path than a joint on the intake — what
  it admits has to pass the breather's valve, and the crankcase sits only
  slightly below atmosphere — but not nothing: the idle got audibly worse
  with the filler cap off (`open.md` H9). Judge by amount: a faint wisp
  round a seated dipstick against a steady stream. *Corrected 4/10/2026:
  this read "smoke at the oil filler or the dipstick is expected, not an
  intake leak".*

**The exhaust** (*owner's decision, 6/10/2026*; *general practice, not
VW's*): a cold look at H2's zone (`open.md` H2) before the warm tailpipe
test of step 3. The exhaust is a large volume at almost no pressure,
hence the time.
- the manifold, its gasket, the probe boss and the outlet flange are
  **H2's zone, ahead of the front probe**;
- smoke from the joint behind the converter or anything behind it is
  **behind both probes**: noted, but it is not H2;
- with the engine stopped some exhaust valves stand open, so smoke that
  comes through a cylinder into the intake is that, not a leak;
- ⚠ **a clean result does not clear H2.** A crack in cast iron may only
  open hot (`open.md` H2), so nothing here replaces step 3's warm test.
  Smoke *does* settle it.

## Step 2b — why, and how it is read

**One session can decide**, which on 4/10 it could not (*reasoned*, from
`open.md` H10): that day's first session ran on adaptations fresh from a
disconnect, and 014 stayed at zero until the learned value passed about
−0.93, so its zero said nothing. With the adaptations kept, the learned
value starts where the last session left it (−1.0 to −1.2), where 014
counted at every stop, the cold one included.

**The setup.** The CAN capture is Claude's because the laptop is; the oil
watch beeps ninety seconds before a stop is due and once, long, when the
idle in the band is long enough. Aim for the band's lower edge because
the oil keeps rising at a standing idle. VCDS has lost the ECU during
cranking before, hence the check. Everything else comes from the
capture's raw frames afterwards (`tools/idledips.py`): the MFD is out
while the USBtin is in, so the capture holds no 0x600–0x604.

**What it says** (Claude reads the logs; nothing is judged at the car):
- **014 at zero at A2 and A3 with the learned value still past −0.93** →
  a real change. **Session B the same day** as confirmation (*owner's
  decision, 4/10/2026*). Zero in both → the idle is fixed; record it.
- **014 at zero, and the learned value has risen above −0.93 during the
  session** — the likeliest look of a fix if 2a sealed the leak
  (*reasoned*, H10): the ECU stops learning air away because the air is
  gone, and stops counting with it. **A real change too**, and readable,
  because the value started at −1.0 to −1.2 with nothing reset, so the
  rise itself says the air changed. Then session B, and **055 and 014 on
  the next few drives**: the value staying up and 014 at zero → the idle
  is fixed; record it.
- **The learned value above −0.93 and 014 still counting** → not fixed,
  and **against H10**: counting without the learned value is what H10
  says does not happen. The one way 2b still tests H10 (`open.md` H10,
  *The test*).
- **Counts at A2 or A3** → not fixed; no session B; step 3.
- **Either way, the air** (*reasoned*, H10; `open.md` H10, *How much of
  it a leak can be*). If 2a sealed a leak, the plate has to let in what
  the leak used to. **The first sign is 055 field 2, the live regulator,
  going positive already at A1**, where it otherwise sits near zero. Over
  the session the learned value, field 3, drifts from −1.0 to −1.2 toward
  zero and takes over from field 2, slowly: on 4/10 it took about 35
  minutes to go from zero to −0.93. The sum of the two moves at once, by
  the leak's share, tenths of a g/s at most. And 003 against the warm
  stops of 4/10 — air 3.1–3.3 g/s at 760 rpm, plate 2.6°, 055's sum
  −1.1 g/s — where a sealed leak shows as more air through the MAF and a
  slightly wider plate. On the fuel side, 033 dips a few per cent negative
  and 032's idle cell follows only over distance. **All of these are
  small.** 014 decides; these say only whether the air changed at all,
  read at a matched oil temperature with the loads off.

## Step 2c — why, and how it is read

*Owner's decision, 6/10/2026:* **straight on from A3, whatever 014 shows
there**, one drive and one capture file. An exception to the rule above,
made knowingly: S4/S5 are not the idle fault (`refuted.md` A10). It is
cheap, though, it costs no idle, and no knock log has been taken since
all four injectors went home on 1/10; until then only cylinder 4's was
seated (`open.md` H5). 2b is over by the time this starts, so the load
cannot touch its reading.

**Why not blips at idle.** S4's retard came only **while driving**,
under load: tip-ins after a coast or a gearchange, and full-throttle
pulls. S5's excess appeared **standing in neutral, but at a held 2300 rpm
and up**; at idle all four cylinders sit on the floor. Blips at a
standstill load nothing, so they show neither.

**The setup.** 020 + 026 + 003 are the groups of
`vcds-knock-020-026-003.csv`. The VCDS switch is idle time, hence
quickly. The capture carries the oil temperature and engine speed to
align with. 3500 rpm catches the move to cylinder 1's window above
~3350 rpm. The oil after A3 sits about 70 °C, close to the `-clamp` log's
65 → 71 °C. The befores: `vcds-neutral-026-003.csv` and `-clamp.csv` for
the holds, `vcds-knock-020-026-003.csv` and `vcds-knock-022-023.csv` for
the drive.

**What it says** (`open.md` H5; Claude reads the log):
- **Cylinder 4's excess over 1 in 026 gone, and 020's events spread over
  several cylinders, moved to another or gone** → the likeliest reading is
  injector 4's click, coupled into the block while it alone was seated.
  "All four alike" is only one form of this result: a click falls where
  injection timing puts it, not necessarily in its own cylinder's window,
  and a steady click is learned away as noise. ⚠ The job of 1–2/10 also
  refitted the throttle, the breather and the cover, so a loose part among
  those (H5's second candidate) changed at the same time, and this cannot
  fully separate the two.
- **Still on cylinder 4 alone, in both parts** → the injectors are cleared
  from S4/S5; next come G66's 20 Nm and its connector, then a look for a
  loose bracket at ~3000 rpm in neutral (H5's tests).

## Step 3 — why, and how it is read

**Idle solved → stop and record.** Otherwise each item decides whether
the next is needed.

1. **The vacuum gauge** (`open.md`, *Tools worth owning*). A long hose
   smooths away the flick a valve makes. Read against itself (*general*):
   **a steady needle** → no valve and no large leak; **a regular flick
   down** at one point in the cycle → a valve (H1); **a low or slowly
   wandering needle** → a leak or a mixture fault (H3, H7).
2. **The exhaust ahead of the front probe (H2)**, if `open.md`'s ranking
   then puts it next. With the outlet closed, a leak that draws air in at
   idle blows out, and hisses or puffs. Warm, because a crack in cast iron
   may only open hot; never longer than a few seconds and never indoors
   (*general*). A new manifold if it leaks (*owner's decision*, 3/10/2026);
   the suffix differs by model and year; the studs into the head are 26
   years old. **Nothing leaks ahead of the probe** → H2 is refuted for its
   zone and goes to `refuted.md`.
3. **The next repair** is chosen then, not now, from `open.md`'s ranked
   candidates.

## Standing items — why

- **The cover's nuts**: the gasket settles (`open.md` S10).
- **The thermometer reading (A4)**: `docs/firmware/open.md` question 10.
  The ignition goes back on so the capture keeps 0x420. The coolant hose
  checks the instrument against 0x288's coolant.
- **The deliberate misfire**: `docs/firmware/open.md` question 11 — 014
  and `IdleHealth` read against a misfire of known rate.
