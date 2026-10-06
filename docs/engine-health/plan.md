# Engine health — the planned fixes, in order

**The order of work, and nothing else.** Why each step is there lives in
`open.md` (symptoms, hypotheses, the ranked candidates); what was done
lives in `vehicle-history.md` (the parts) and `idle-log.md` (the story)
once it is done. **A step that has been done
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

**Where it stands:** the valve cover, throttle and breather job and the
cover joint are done and recorded (`vehicle-history.md`, `idle-log.md`); the three
sessions after them are in `open.md` S3. The misfires remain, and they
follow 055's learned idle air value (`open.md` H10) — the likeliest
reason the ECU learns air away being air the plate did not let in.

⚠ **Keep the battery connected through steps 2 and 2a** if the work
allows. The learned value has settled at about −1.1 g/s, and that is what
makes step 2b readable in one session. If a repair needs the battery off,
say so: step 2b's stops then count only once the learned value is past
−0.93 again — **or once it plainly is not going there**: on 4/10, from
zero, it took about 35 minutes of driving and stops to pass −0.93. A
learned value that stays well short of that after as long is a result in
itself (H10: air the plate did not let in is gone).

---

## Step 2 — the exhaust joint behind the converter, by the owner

*Owner's decision, 4/10/2026*, after the owner is back (about 11/10),
with the new flange and exhaust sealant in hand: the joint behind the
converter that has never been tight (`open.md` S6). **For comfort, not
for the idle** — it is behind both probes and spits on every drive. The
manifold is not part of this step (step 3).

## Step 2a — the intake smoke test, and the repair of what it finds

*Owner's decision, 4/10/2026:* **straight after step 2, whatever H10
turns out to be** — the misfires are there either way, and the smoke says
where air gets in, which H10 cannot. It also looks for the hiss the owner
hears and cannot place (`open.md` S11). The engine off and cold, so it
costs no idle.

**First, the dipstick tube** (*owner's decision, 4/10/2026*): loose, its
bracket missing, fresh oil at its foot (`open.md` H3, *The dipstick
tube*). Refitted before the smoke, so that smoke at the dipstick means
something. **The part numbers, to be confirmed by VIN at the parts shop
before ordering** (ETKA shows the bracket and its bolt on the same
drawing; none of these was read off a VW catalogue page for this car):
- dipstick: **`06B 115 611 R`** — sold for the Beetle, Golf and Jetta
  2.0 SOHC 1998–2005 by several sellers;
- upper guide, the orange one: **`06A 103 663 C`** — listed by VW's US
  parts site for the 2002 Beetle 2.0; **not `…663 B`**, which is the
  1.8T's;
- lower metal tube, block to guide: **not replaced** (*owner's decision,
  4/10/2026*: by most accounts hard to get out). Pushed home in the block
  if it has backed out;
- the bracket: **no number found.** On videos of this engine it is a flat
  steel strap bolted under the intake manifold, with a small pin at its
  foot that the orange guide's tab clips over. Ask by VIN; or take one,
  with its bolt, off a scrapped engine of the same family — **check the
  engine code on the donor** (AQY, AZJ, APK, AZH, AEG — Golf IV, Bora,
  Beetle, Octavia I 2.0, *general*, not checked against a catalogue) and
  compare it with a photo of the manifold before taking it.
  `06A 133 228 S`, sold as an "inlet manifold support" for the AZJ, came
  up in a search; whether it is this strap is **not known**.

The guide clipped onto the tube and onto the bracket's pin.

*General practice, not VW's:*

- **the smoke**: a 12 V smoke tester **with its own air pump** — the
  owner has no aquarium pump. **Lincos `MG78016` ordered** (*owner*,
  4/10/2026): pump built in, 5–35 ml of mineral (baby) oil — the oil to
  have in hand. Never anything flammable
  in it, never workshop air: the pressure only has to make the smoke
  flow;
- **seal the intake behind the MAF** — the hose between the MAF and the
  throttle off **at the MAF's end**, a glove or bag clamped into it.
  **Not through the MAF**: oil smoke over its sensing element is the one
  thing here that can spoil a part (*general caution*). That leaves the
  MAF-to-hose clamp untested; it holds by the owner's check, is a
  rubber-lined pipe clamp rather than VW's, and was sprayed at a warm
  idle on 26/9 with no change (`open.md` H3, *Spray test*;
  `idle-log.md`, *The MAF*). The throttle end, refitted since,
  is inside the smoke;
- **feed the smoke through the fuel pressure regulator's vacuum hose**
  (*owner's choice*: at the front, the easiest to reach), taken off at
  the regulator, so the smoke enters the manifold behind the plate; the
  brake-servo hose would do the same. **No fuel in it** (*owner*,
  4/10/2026): it was off several times during the intake work of 1–4/10
  and never smelled of petrol, so the regulator's diaphragm is not
  leaking into the manifold (*general*: that is how such a leak shows);
- **hold the throttle open** (a string on the cable or a hand on the
  quadrant) so the smoke fills both sides of the plate;
- a few minutes of smoke, a torch, and look at the throttle's flange and
  its hose clamp, the upper-to-lower plenum joint, the injector seats,
  the hoses at the back (brake servo, the old secondary-air vacuum line),
  the breather and its hose's plastic connector, the brake servo's valve
  — **the back is what no spray ever reached**;
- **smoke at the oil filler, the dipstick or the cover joint is a leak
  too**, of the crankcase: the breather joins the crankcase to the
  intake behind the MAF, so wherever smoke leaves the crankcase, air
  gets in at idle and reaches the manifold unmetered. It is a smaller
  path than a joint on the intake itself — everything it admits has to
  pass the breather's valve, and the crankcase sits only slightly below
  atmosphere — but not a nothing: the idle got audibly worse with the
  filler cap off (`open.md` H9). Judge by amount: a faint wisp round a
  seated dipstick against a steady stream. *Corrected 4/10/2026: this
  read "smoke at the oil filler or the dipstick is expected, not an
  intake leak".* With the dipstick tube refitted (above), look at its foot in the block
  as well as its top;

**Smoke found** → that joint is repaired, then step 2b. **None** → step 2b
all the same.

## Step 2b — the test afterwards: session A, adaptations kept

**One session can decide**, which on 4/10 it could not (*reasoned*, from
`open.md` H10): that day's first session ran on adaptations fresh from a
disconnect, and 014 stayed at zero until the learned value passed about
−0.93, so its zero said nothing. With the adaptations kept, the learned
value starts where the last session left it (−1.0 to −1.2), where 014
counted at every stop, the cold one included.

**The session:**
- **a cold start** after a night's stand; no battery disconnect, no 098;
- **A1** — standing 2–3 minutes, then drive off; a look for leaks at
  whatever 2a repaired;
- **A2** — drive, and stop at **56–62 °C of oil**: two minutes standing,
  loads off, until the long beep;
- **A3** — drive on, and stop at **68–72 °C**: three minutes standing,
  loads off;
- driving between the stops normally — no hard drive;
- engine off; **032 photographed** with the ignition on.

**Who runs what — the laptop, two windows:**
- **`git pull` on the laptop first.**
- **The CAN capture is Claude's**: `usbtin_capture.py`, listen only, one
  file for the session, started before the ignition and left running to
  engine off — `python tools/usbtin_capture.py --seconds 3600 --out
  <session>_z1.txt`. **Stopped early, Claude closes the USBtin's channel**
  so its light goes out.
- **The oil watch is the owner's**, in a second `cmd` window on the same
  file: `python tools\oilwatch.py <session>_z1.txt`. Three beeps ninety
  seconds before a stop is due, one long when the idle in the band is
  long enough. **Aim for the band's lower edge**: the oil keeps rising at
  a standing idle.
- **VCDS on its own log, groups 014 + 055 + 033** from before the start to
  engine off; check it is still logging once the engine catches. It lands
  in Downloads, where Claude picks it up.
- **Everything else comes from the capture's raw frames afterwards**
  (`tools/idledips.py`): the MFD is out while the USBtin is in, so the
  capture holds no 0x600–0x604.

**What it says** (Claude reads the logs; nothing is judged at the car):
- **014 at zero at A2 and A3 with the learned value still past −0.93** →
  a real change. **Session B the same day** after a cool-down to below
  45 °C of oil — the same two stops — as confirmation (*owner's decision,
  4/10/2026*). Zero in both → the idle is fixed; record it.
- **Counts at A2 or A3** → not fixed; session B is not run; step 3.
- **Either way, the learned value**: if a leak was sealed it should drift
  back toward zero over the session (*reasoned*, H10). And 003 against
  the warm stops of 4/10 — air 3.1–3.3 g/s at 760 rpm, plate 2.6°, 055's
  sum −1.1 g/s — where a sealed leak shows as more air through the MAF.

## Step 2d — the cylinder 4 knock window again, all four injectors seated

*Owner's decision, 6/10/2026:* **after step 2b, whatever 014 shows
there.** An exception to the rule above, made knowingly: S4/S5 are not
the idle fault (`refuted.md` A10). It is cheap, though, it costs no idle,
and no knock log has been taken since all four injectors went home on
1/10. Until then only cylinder 4's injector was seated (`open.md` H5).

**Not an idle with throttle blips.** S4's retard came only **while
driving**, under load: tip-ins after a coast or a gearchange, and
full-throttle pulls. S5's excess appeared **standing in neutral, but at a
held 2300 rpm and up**, and at idle all four cylinders sit on the floor.
Blips at a standstill load nothing, so they show neither. Two parts,
one VCDS log, **groups 020 + 026 + 003**, the same three as
`vcds-knock-020-026-003.csv`:

1. **Standing, neutral, handbrake on, warm by driving**, oil about 56–70 °C
   (the before ran 56 → 68 °C). Hold each speed for 10–15 s:
   **1600, 2000, 2400, 2800, 3200, 3500 rpm**, then back down the same
   steps, then the engine off. 3500 is there to catch the move to
   cylinder 1's window above ~3350 rpm. The before is
   `vcds-neutral-026-003.csv` and `-clamp.csv`.
2. **A drive, warm**, repeating 24–25/9: **tip-ins after a coast and
   after gearchanges at 1000–2000 rpm**, a dozen or more, and where the
   road allows **two or three full-throttle pulls through 3000–4000 rpm**.
   The before is `vcds-knock-020-026-003.csv` and `vcds-knock-022-023.csv`.

**No CAN capture needed**, since VCDS carries everything here. **The MFD in**,
so the oil temperature is read off the display at the start and end of
part 1 and written into the chat.

**What it says** (`open.md` H5; Claude reads the log):
- **Cylinder 4's excess over 1 in 026 gone, and 020's events spread over
  several cylinders, moved to another or gone.** The likeliest reading is
  injector 4's click, coupled into the block while it alone was seated.
  "All four alike" is only one possible form of this result. A click
  falls where injection timing puts it, not necessarily in its own
  cylinder's window, and a steady click is learned away as noise.
  ⚠ The job of 1–2/10 also refitted the throttle, the breather and the
  cover, so a loose part among those (H5's second candidate) changed at
  the same time, and this reading cannot fully separate the two.
- **Still on cylinder 4 alone, in both parts.** The injectors are cleared
  from S4/S5, and next come G66's 20 Nm and its connector, then a look
  for a loose bracket at ~3000 rpm in neutral (H5's tests).

## Step 2c — the adaptation test (`open.md` H10): optional

*Owner's decision, 4/10/2026:* optional — it says how the ECU comes to
count, not where the air comes from. **The battery off overnight, 098,
then step 2b's session**, driving on afterwards until the learned value
has passed −1.0 and stopping three minutes. Zero while the learned value
is near zero and counts once it passes about −0.93 → H10 confirmed;
counts while it is still near zero → H10 refuted, and the manifold
(step 3) moves up.

## Step 3 — only if the idle is still not fixed

The same rule: **idle solved → stop and record.** Otherwise, each
deciding whether the next is needed:

1. **A vacuum gauge at a warm idle** (`open.md`, *Tools worth owning*),
   teed into the fuel pressure regulator's vacuum hose. Keep the gauge's
   hose short, or it smooths away the flick a valve makes, and the
   T-piece tight. Read against itself (*general*): **a steady needle** →
   no valve and no large leak; **a regular flick down** at one point in
   the cycle → a valve (H1); **a low or slowly wandering needle** → a leak
   or a mixture fault (H3, H7).
2. **The exhaust ahead of the front probe (H2)**, if `open.md`'s ranking
   then puts it next:
   - **the tailpipe test**, warm idle, outdoors: the tailpipe closed for
     **2–3 s at a time** while the manifold, its joint to the head, the
     probe boss and the outlet flange are listened to and felt for (a
     hand near, never on). With the outlet closed a leak that draws air
     in at idle blows out, and hisses or puffs. A phone recording at the
     head, since one person cannot do both ends. *General:* never longer
     than a few seconds, never indoors; warm, because a crack in cast
     iron may only open hot;
   - **if it leaks ahead of the probe — a new manifold** (*owner's
     decision*, 3/10/2026), with a new gasket to the head, new nuts, a
     new outlet gasket and the probe refitted with anti-seize. **Which
     part:** `06A 253 031` plus a suffix that differs by model and year;
     the number cast into this car's manifold, or a lookup by VIN,
     decides it. **Cost**, looked up 3/10/2026: new from VW about
     €350–490, used 700–1,500 Kč. ⚠ The studs into the head are 26 years
     old — penetrating oil the days before, heat and patience; a snapped
     stud is where it goes to a garage;
   - **if nothing leaks ahead of the probe**, H2 is refuted for its zone
     and goes to `refuted.md`.
3. **Then the next repair from `open.md`'s ranked candidates**, chosen
   then, not now.

## Standing items

- **The cover's outer nuts re-tightened after a few hundred km** — the
  ones reachable with the plenum on, with a look along the joint
  (`open.md` S10).
- **The oil thermometer reading (A4) when there is a thermometer** —
  `docs/firmware/open.md` question 10: in the first minute after engine
  off at the end of a hot session, the oil filter, the sump from beneath
  and the upper coolant hose, the ignition back on at once so the capture
  keeps 0x420; the owner writes the three readings in order into the
  chat. The last one checks the instrument against 0x288's coolant.
- **Once the idle is solved:** `docs/firmware/open.md` question 11's
  deliberate misfire — one injector unplugged for a minute at a warm
  idle — to read 014 and `IdleHealth` against a misfire of known rate.
