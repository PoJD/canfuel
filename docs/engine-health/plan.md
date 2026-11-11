# Engine health — the planned fixes, in order

**Part 1 is what to do, in order, with no explanation.** It is what goes
to the car. **Part 2 is why, and how the results are read.** Keep it that
way (*owner's decision, 8/10/2026*). An instruction goes in Part 1 and its
reason in Part 2, never mixed. Why each step exists at all lives in
`open.md`; what was done lives in `vehicle-history.md` and `idle-log.md`.
**A step that is done is removed from both parts in the commit that
records it**, and the file is deleted when it is empty.

The full previous version, before it was condensed on 20/10/2026:
`git show d327332:docs/engine-health/plan.md`.

---

# Part 1 — what to do

## Step 3 — the idle is not fixed

One at a time; Claude says after each whether the next is needed.
Captures only where an item asks for one. **Current: 8i (the timing
belt's marks) at the next cold engine**, 8h (the loads against the
sensors' voltages) at a laptop session, and 8f at every VCDS session
(032, and 036 now and then); item 6 and 6i; 8a (the new N80, ordered
11/11) as soon as it arrives, 8j (the canister) before it; then item 9, 6m inside its garage session;
**8e postponed to the end** and 8g dropped (*the owner*, 10/11
and 11/11; `open.md` H11, *The relearn drive*, S23; S1, *The rough
start of a warm stop*).

6. **Drive normally with the MFD in**; brisk driving once warm is
   welcome. At a warm stop that comes anyway, `IdleHealth` in the
   everyday state and the oil temperature, written into the chat.
   - **No captures for now.** Only **once `IdleHealth` on the MFD is
     clearly better**: one or two warm drives captured, on different
     days. Claude runs the capture; VCDS on **014, 003, 020**; 055 once
     at the end, warm idle. Write the stops.
   - **The converter carries `Misfires` and `MisfAvg`** (0x604 layout 2,
     flashed by Claude on 4/11, the stored trip and tank kept). **The
     owner uploads `tri/S-AQY.TRI`** from `mfd15` to the display through
     oDSS himself. JP1 stays off (*the owner*, 4/11: no debug needed), so
     0x603 and the LEDs are dark by design. From then on, at the same warm
     stops, **`Misfires` and `MisfAvg` beside `IdleHealth`** into the chat.
   - **After the clean of 9/11**: at several warm stops, **a word on what
     came before each stop** (queuing, or a brisk stretch), and the A/C's
     figure too whenever it happens to be on; **an odd cold misfire or a
     drop-out on one cylinder** goes into the chat at once.
   - **A hard jerk at a crawl or on moving off** (`open.md` S12): the
     clock time into the chat as soon as it is safe, with the gear and
     roughly the speed; on a captured drive, **"teď"** at once.
6i. **The oil level on the new oil, about every 500 km** from the first
   reading (27/10, 155,024 km, at the top mark; 5/11, 155,546 km, 0.5–1 mm
   under it; **next about 156,050 km**): the car on level ground
   and **at least 5 minutes standing**, the dipstick out, wiped, in, out,
   and **photographed**; the odometer into the chat. Any top-up: the litres and the odometer
   into the chat.
6m. **The injector circuits among themselves, with a multimeter** (the
   owner's, 5/11), engine off, ignition off; the upper intake off only if
   the connectors cannot be reached without. First touch the two probes
   together and note the reading: it is taken off every value. The four
   injector connectors off; **from contact 1 of one connector to contact
   1 of each other**, all six pairs; **each injector across its own two
   pins**, all four. **If the loom has a connector of its own** on the way
   to the main harness: from contacts 1 and 2 of each injector connector to
   the pin of that connector it reaches (find it with the beeper), all
   eight. While each value is on the display, **flex the loom near 3 and
   4** and watch it. Write every value, and any that moved.
   **5/11: only 1 and 4 reachable with the intake on** (*owner*); the rest
   with the upper intake off — **in item 9's garage session, for 4's
   deficit, which the clean left** (*agreed with the owner*, 9/11
   evening; the session since 11/11). (5/11: contact cleaner went into 4's
   connector and T3 at the first look, `vehicle-history.md`.)
6n. **The injector circuits to the ECU** — later, only with VCDS on the
   laptop: 032/055 read first (unplugging the ECU may reset them, as a
   disconnect does), then the ECU's 80-pin plug off. One extension lead
   for all four: its own resistance measured end to end and taken off.
   **From contact 2 of each injector connector to its pin: 73 (cylinder
   1), 80 (2), 58 (3), 65 (4)**; check the numbers on the plug, and enter
   its sockets only with a thin pin of the right size, never a meter tip.
7. **Only if Claude asks after 6:**
   - **The exhaust test again, warm**, after a drive to 95–100 °C of oil.
     Outdoors; the tailpipe closed for a few seconds at a time, never
     longer. The phone records at the manifold; mark each closure aloud on
     the recording; listen back and report engine bay or underbody.
     Photograph the flange, the front pipe and 3 and 4's pipes from below
     for soot. **Leaks there → a new manifold**: new gasket to the head,
     new nuts, new outlet gasket, the probe refitted with anti-seize. Part
     `06A 253 031` + suffix: read the number cast into the manifold, or
     ask by VIN. New from VW about €350–490, used 700–1,500 Kč.
     Penetrating oil on the studs the days before; a snapped stud goes to
     a garage.
   - **The high-voltage side in the dark**, a damp evening, warm idle:
     bonnet open, lights off, look along the leads and the coil for a
     spark or a blue glow; then a fine water mist over one lead at a time
     and the coil, hands and bottle clear. Write anything seen and which
     lead the engine stumbled at.
8j. **The charcoal canister looked at and blown through, before 8a**
   (*the owner*, 11/11), the engine cold:
   - **The car safe first**: on level ground, the handbrake on, a chock
     at a front wheel, **on an axle stand, never on the jack alone**;
     the right rear wheel off, the wheel arch liner back as far as
     needed. No flame, no smoking, nothing that sparks near it.
   - **Photographs before anything is touched**: the canister in place,
     its label, each hose where it joins — so each goes back where it
     was. A piece of tape with a number on each hose helps.
   - **Looked at**: a crack, a stone or dirt on it, the vent's opening
     blocked, a hose cracked or soft, granules of charcoal in a hose or a
     port, a smell of fuel.
   - **The hoses off one at a time**, about three (from the tank, to
     N80, the vent); N80's hose off at N80 as well; **the filler cap
     open**. Blown through **by mouth or a low-pressure hand pump, never
     compressed air**, and **never sucked on**:
     - in at N80's port → it should come out at the vent;
     - in at the tank's port → out at the vent; the line to the tank
       blown towards the tank, the cap open (a valve on the tank's side
       may let it pass one way only — say which);
     - into the vent → in at the canister.
     Which passed easily, hard, or not at all, into the chat.
   - **Shaken gently**, if it can be: a rattle inside said in the chat.
   - Every hose back as photographed, each pushed fully on; the cap
     closed until it clicks; the liner and the wheel back, the bolts
     tightened to the wheel's torque.
8a. **The purge valve N80, the new one ordered by the owner (11/11)**:
   Bosch `0 280 142 353`, VW `1C0 906 517 A`, the same as the one on the
   car; the hoses stay. In this order, the day it is fitted:
   - **032/055 and the fault memory read with VCDS** just before the swap.
   - The swap; **the old valve kept**, not thrown away.
   - While it is out: **a photograph of its two hoses to where they
     join** (the T at the throttle) and of the vacuum hose of the
     secondary-air valve N112 to where it joins.
   - Afterwards, warm, the owner runs **basic setting 070** and
     photographs it; then item 6's warm stops, and **032 read after the
     first two drives** (8f).
   - **Fitted when it arrives**; nothing to read before it but the line above.
   - **At any engine lamp from now on**: the odometer, the tank's needle
     and the outside temperature into the chat, and 032 read before the
     code is cleared.
8i. **The timing belt's marks, at a cold engine**: the upper belt guard off; the crank turned by hand in
   the direction of rotation until cylinder 1 is at TDC, **the notch on
   the crankshaft pulley against its mark** (within about 5 mm); then
   **the camshaft sprocket's mark against its mark** on the cover or the
   head. **A photograph of each mark, square on**, into the chat; nothing
   loosened. Then the guard back on.
8f. **032 for 20 s at every session with VCDS connected**, until both
   cells have held for three drives; **and 036 for a minute** at a warm
   idle and on the road when VCDS is on anyway (the rear probe watched
   now and then, *the owner*, 11/11).
8h. **The loads against the sensors' voltages**, Claude in a session on
   the laptop, a warm engine after
   a drive, the car standing, the owner in the driver's seat:
   `usbtin_capture.py` running; the fault memory read first.
   - **Idle, the everyday state, every load off that can be**; then, 30 s
     each, on and off again with 30 s between: **the A/C, the rear window
     heater, main beam, the blower on 4**, one at a time; the rear window,
     main beam and the blower said in the chat as each goes on and off
     (the A/C and the lights Claude reads off the bus).
   - The whole sequence three times, VCDS logging a different set each
     time: **004 033 036**, then **004 060 002**, then **004 026 041**.
   - Nothing under the bonnet or the car while the engine runs. After it,
     the fault memory.
9. **After the clean of 9/11, by what the next stops show** (Claude says
   which):
   - **A CO₂ ("block") test of the coolant**, warm, at a garage or with
     a kit.
   - **A stethoscope (or a long screwdriver) on the cam cover above
     cylinder 3, hot**, against 1, 2 and 4: a tick or a hiss on one, at idle.
   - **One garage session with the upper intake off, straight after a
     drive** (oil at 80 °C or more), in this order:
     - **a warm leak-down on all four**: all four plugs out (the same
       plugs back afterwards; plug 3's gap measured while out); each
       cylinder at TDC on its compression stroke, firing order 1-3-4-2;
       the crank held while the air is on. For each: **the percentage,
       and where it hisses** — tailpipe, throttle, oil filler, bubbles
       in the coolant tank, the next plug hole. **Cylinder 3 twice**:
       the crank turned two full turns between the two readings;
     - **a warm compression test on all four** straight after, the
       throttle held open;
     - **the cam cover off: VW's tappet check** — the cam of each tappet
       pointing up, the play felt; more than 0.2 mm, the tappet renewed;
       otherwise each pressed down with a plastic or wooden wedge and a
       0.2 mm feeler tried between cam and tappet; the eight results
       into the chat;
     - **6m's injector circuits** while the intake is off;
     - **the lower manifold's gasket**: renewed if the garage takes
       the lower manifold off as well (the tear at runner 4).
   - With VCDS connected anyway after a stored P030x: **a generic
     OBD-II read** (modes 02 and 06), read only, saved.
   - **No head off** (*the owner*, 4/11, leaning, not final): if the
     leak-down names 3's exhaust seat, the car is driven as it is and S1
     most likely closed as *acceptable, cause known*.

8e. **Postponed to the end** (*the owner*, 11/11). When it is done, at a
   cold engine, from below:
   - **The rear probe's lead, all the way to its connector**: where it
     runs, whether it touches or lies within a finger's width of the
     exhaust or the converter, any melted, shiny or hardened
     insulation; the connector latched and its seal in place; then the
     connector off, both halves looked into for green, water or a pushed-back
     pin, and back on until it clicks. **Photographs** of the run and
     of anything found; into the chat.
   - **The two damaged wires** (found 10/11 evening: the rear probe's
     blue, its outer white, a heater lead; the front probe's brown, its
     grey): dried and taped for now (*the owner*); for good, each cut
     back to bright copper on both sides of the damage and joined with a
     crimp or solder sleeve under heat-shrink (VW's wiring repair or any
     sealed butt connector). The red wire beside the blue looked at the
     same way. *Taped and the bundle wrapped by the owner 10/11 night*;
     the splice is what is left of this point.
   - **The rear socket's broken-looking outer terminal**, on the rear
     probe's signal (the cavity meeting the probe's black wire): the
     terminal replaced —
     a VW repair terminal crimped on, or the socket half with its
     pigtail — before anything else is measured on that wire.
   - **The rear connector's bent pin** straightened so it seats like
     the others; both connectors dried again, then **pushed
     until each latches with a click** — the front one included, which
     did not latch on 10/11 morning.
   - **Nothing sprayed or greased into either probe's connector**, ever
     again — no contact cleaner, no dielectric grease; **the probe's own
     lead and its connector never sealed airtight** (no heat-shrink with
     glue, no silicone over them). The tape over the harness side stays.
   - **Both probes' harness on to the ECU** (the owner's own look,
     10/11): from each probe's connector along the loom as far as it
     can be followed — where it runs, what it is tied to, anything it
     rubs on, and **every earth point met on the way** (an eyelet on
     the block, the gearbox or the body): tight, clean, no green. A
     photograph of the route and of each earth point.
   - **Both probes' sockets on the harness side** (the front one too):
     each connector off, the harness half looked into for green, water,
     a pin pushed back or loose in its cavity; photographed; back on
     until it clicks.
   - **The new probes' tightness**: with the spanner they were fitted
     with, whether either turns further at the effort they were
     tightened with. Which, and about how far, into the chat; nothing
     undone.

## Standing items

- **Every drive:**
  - Idle as the day brings it; minutes are fine, hours are not.
  - **Engine lamp flashing**: ease off at once, stop where safe, engine
    off, write it into the chat.
  - **Engine lamp steady**: drive on; the fault memory read when VCDS is
    next connected, the codes into the chat.
- **`IdleHealth` and `Misfires` only in the everyday state** — **blower on 1, one seat
  heater on 2, the lights on** (*the owner*, 8/11; *this said the seat heater on 1, the
  23/10 wording, until then*) — at warm stops that come anyway (oil
  95–100 °C, neutral, no throttle), with the oil temperature; any other
  state is named. **No stop is made or lengthened only to read it.**
- **The fault memory after every session with VCDS connected**: read,
  saved, then cleared by the owner by hand. Not after a plain drive.

---

# Part 2 — why, and how it is read

## The rule — the owner's decision, 27/9/2026, amended 18/10/2026

**The idle comes first**: the unsettled idle (S1) and the misfires 014
counts at idle (S3). **S18, cylinder 3 dropping out with a tick, came
first beside it** from 18/10 until it closed on 24/10, after a week
without it (`refuted.md` D10); the owner kept its drive rules as a
habit until the map went back (3/11), so that a return was caught (they
left Part 1 on 26/10 at his request: not a step, what he does anyway);
whether he keeps them since is his. So:

- **Fix, then look.** Each step is a repair; the only readings taken are
  the ones that decide the next step.
- **No test for its own sake**, and nothing unrelated to the idle is
  pursued until it is solved — unless it could be related.
- **Run the engine as the day needs it.** *This said "as little as
  possible, above all not at idle", for the converter, until 6/11/2026*:
  the idle's misfires heat it by tens of kelvin at most (`open.md` S3,
  *What it costs the converter*).

`open.md`'s tests are reference, **not a to-do list**.
**The cylinder 4 knock window stays out of this plan** (*owner's
decision, 9/10/2026*): G66 and the rest of H5's tests stay in `open.md`.
Where the work stands is in `idle-log.md` and `open.md`, *Where it
stands*.

## Step 3 — why, and how it is read

**Idle solved → stop and record** (`open.md` S1, *When S1 closes*; S3,
*When S3 closes*). Otherwise each item decides whether the next is
needed.

**6m and 6n, the injector circuits** (`open.md` H4, *What the loom can
and cannot do unseen*), split so the first needs nothing unplugged at the
ECU (*the owner*, 5/11): a raised resistance in the loom at 3 and 4 makes no
code but starves its injector. The manual's figures: injector 14–18 Ω
at about 20 °C, each wire at most 1.5 Ω, contact 1 the shared supply from
J17, contact 2 the ECU's output at pins 73/80/58/65. Read as a comparison:
three alike and one higher (tenths of an ohm on a wire, an ohm on an
injector) names the joint; all alike clears the supply and that wire.
Contact 1 to contact 1 runs through the shared splice, so a high pair
points at one of its two branches and the pairs together at which. A
loom connector, if there is one, splits each path into the old taped run
at the injectors and the rest; a value that moves while the loom is
flexed is the intermittent joint itself.

**Which VCDS groups** (*decided 11/10/2026*). **014** wherever a stop is
read for misfires. **001** wherever there is idle: engine speed to align
on and the lambda correction (`open.md` S1, *What VCDS saw just before a
dip*). **003** on every step with an idle: the idle air and advance, and
the MAF's own figure, since 12/10's least charge on record after the
airbox was sealed is what a MAF that used to over-read would explain
(`refuted.md` D4). **020** only where there is driving under load, for
cylinder 4's retard (S4). **026** reads its floor at idle and belongs to
the knock window, so it is dropped. **055** once at a warm idle says the
adaptations are settled (about −1.1 to −1.3), so a comparison holds
(`refuted.md` C19).

**Item 6 — the drives** (*decided 10/10/2026*; *the owner, 21/10: the
tank on the display, the captures after it*). The display follows the
idle through the tank; the captures read where it got to. The dips' shares need
several drives pooled, and they cost nothing. **Read**: `cutscan.py
--shares` on the idles, alone and pooled since the last repair — the
share the top two carry and p against all four alike (`open.md`, *The
dips keep to one slot*); `--name` too if a capture has cuts. 014 by stop
and `IdleHealth` by oil band against `open.md` S1 and S3. **003** says
whether anything sealed or opened; **020** is data, not a step: whether
cylinder 4's retard, nearly gone with the new leads on 10/10, stays gone
(S4).

**No captures until the display shows a change** (*owner's decision*,
23/10/2026), and **the hard run dropped** with them: it was planned because on
4/10 014 counted only at the stop after a hard drive, and that was an
adaptation completing rather than load (`refuted.md` C19).
What it costs: a capture on plain fuel just before the cleaner, the
reference its tanks would have been read against. What is left: `40`,
the refit drive of 21/10 on plain fuel, as that reference; the display
through the tanks; and the captures once `IdleHealth` moves, which then
say what moved.

**Item 6i — the oil level on the new oil** (`open.md` H18; `refuted.md` C21; *the
owner's agreement*, 26/10). Oil burnt past the stem seals or rings lowers
the level; fuel collecting in the oil raises it (*general*). On the old
oil neither could be read: no known starting level, and the top-ups
included the litre lost at the cover joint (3/10). A fresh fill to a
photographed level gives the start. **Read**: a level falling between
top-ups → oil burnt, H18 (or the rings) up; a level rising → fuel in the
oil, `refuted.md` C21 revived; steady → neither in quantity. **The engine
does not leak** (*owner*, 31/10, from right under it: the oil on the
sump is the old cover-joint leak's, and what drips is the gearbox;
`open.md`, *Other*), so a falling level is oil burnt. Five minutes standing and
level ground because the stick reads the sump only once the oil has run
back; the photograph because a millimetre is the stick's resolution.

**Item 7 — the exhaust ahead of the converter (H2), warm.** Both of
H2's zones (widened 10/11): ahead of the front probe, and between it
and the converter, where air reaches only the rear probe — so the new
rear probe's switch to the front's swing after 18 minutes of idle on
10/11 (`open.md` H11, *The reading after the swap*) is a reason for
Claude to ask for it once 8e has found both probes tight. A leak that
draws air in at idle blows out when the outlet is closed, and hisses or
puffs; a crack in cast iron may only open hot (*general*). **Cold found
nothing on 12/10** (`idle-log.md`), so warm is what is left. Each closure shows
as a dip in engine speed, which places it in time but not in space. The sound
says only engine bay or underbody; **the photographs locate** (a leak
leaves soot), though the manifold under its heat shield cannot be seen. **Read**: soot below → that
joint; louder from the engine bay with nothing below → the manifold or
its joint to the head, the owner's standing decision of a new manifold
(3/10/2026); soot on the front pipe ahead of the converter → that
joint or its boss resealed; nothing either way →
a garage with a lift. Nothing leaks ahead of the converter → H2
refuted, into `refuted.md`.

**Item 7 — the high-voltage side** (`open.md` H4; `refuted.md` C24): the roughest
reading on record came on a foggy morning (`open.md` S1, *Temperature*),
and the mist supplies the moisture a tracking boot or coil needs. Late
because the coil is from 6/2026 and the leads are new again; it is free.

**After the clean of 9/11 — why the next steps are these** (*agreed
with the owner*, 9/11 evening; the clean itself, done, is `idle-log.md` and `open.md` S1,
*The clean of 9/11*; how its day was planned and read: `git show
c11dc75:docs/engine-health/plan.md`, item 8). **What it showed**: 3's
excess — its share of the dips, its steady deficit, the rough first
minutes of a warm stop and 014's storm — was not there at stop 7, which
is the H13 branch for 3; **4's steady deficit and the settled level were
kept**. **8c, the probes read before and after both were replaced, is done**
(9/11 night and 10/11; `open.md` H11, *The reading before the swap*,
*The reading after the swap*; how it was planned and why: `git show
1040e9e:docs/engine-health/plan.md`, item 8c): the new rear probe flat
for 18 minutes of idle where the old one sank, and the idle as rough as
before.

**8d, the relearn after the battery disconnect, is done** (10/11
evening; `open.md` H11, *The relearn drive*, S23; how it was planned
and why: `git show d4aeca3:docs/engine-health/plan.md`, item 8d): 032
back to −6.3 / +6.3 % within 37 minutes on the new probes, the idle as
before, 3 leading the dips again, and the new rear probe's signal
falling to zero under load (P0137).

**8e, the probes' tightness**: they were tightened by hand to about 50
Nm estimated, without a torque wrench (`vehicle-history.md`), and the
reading after showed the rear probe switching to the front's swing
after 18 minutes of idle and in spells at the warm stop; a probe seated
loose lets air into the exhaust at idle's pulses, the second zone of
H2 of its own making (*reasoned*). Cold, because the exhaust then is at
the temperature they were fitted at. Checked before the warm tailpipe
test (item 7), which it would otherwise confuse. **The rear probe's
lead** (`open.md` S23): 0.000 V at full load is not the gas, so the
signal failed on its way to the ECU, and it came back at a cooler idle
— heat on a lead or a connector the likeliest (*reasoned*); the lead was
tidied by the owner when the probe was fitted, so its run is looked at
first, the connector second; a lead and connector found sound leave the
new probe itself (a warranty matter). Cold, so it can be touched.

**S12's jerk by the clock** (reopened 10/11 night at the owner's
request): the bus cannot show a jerk at a crawl, so only its time
lets a capture or a VCDS log be read at that moment — the stroke, the
load, 014, and from a capture the cylinder (`open.md` S12).

**8e's cracked wire and latches** (`open.md` S23, *Found at the
harness*): a copper strand corroding in a crack is a resistance and, in
the damp, a leak to whatever touches it; tape over it keeps the damp
in, so the corroded length is cut out. Which wire it is tells what it
explains: the signal or its earth fits S23 directly, a heater lead only
through a shared path. A connector that does not latch lets its
contacts move with the engine — it is redone before any reading.

**8e's route of the harness** (*the owner*, 10/11 night: the
connectors are very likely sound and the leads well tucked in, so he
follows the harness instead): a leak or a poor earth is as likely
anywhere on the way as at a connector, and an earth eyelet the
probes' returns share is H21's shared earth itself.

**8e's sockets and 8g, the probes' circuit** — *8g dropped and 8e
postponed 11/11 (*the owner*: the rear probe has no direct hand in the
mixture, no probe code was ever stored before 10/11, the broken-looking
terminal may be how it was made; the probes are watched through 8f's
036 instead); kept for what it argued* (`open.md` H21, added
10/11 evening at the owner's request): the swap changed the probes and
their own plugs, not the harness side, so a fault there survives it —
S23 in full, S19's idle cell perhaps. **With the ignition on and the
engine off the ECU reads both probes at a steady bias** — 033 0.435 V
and 036 0.425–0.44 V on 10/11 (`vcds-step8c-after-001-033-036.csv`,
`vcds-step8d-drive-014-032-036.csv`, before the start; *the owner's
idea*, 10/11 night) — so **a leak to earth or a short, S23's kind,
pulls it off that value as a lead is moved**, with no heat and nothing
running under the car. **What it cannot show** (*reasoned*): a
resistance in series, or a break, with the probe cold and no current
through it the ECU reads its own bias either way; those would show only
with the probe hot and switching, and **the flexing is not done with
the engine running** (*the owner's decision*, 10/11 night: the exhaust
hot, and nobody under a running car) — so they are left to the
multimeter, each wire end to end with the ECU's plug off (6n). *Until
then this asked for the same flexing at a warm idle if nothing moved
with the ignition on.* **Whether the
readings are live at all** (*the owner's question*, 10/11): the rear
one is — with its probe cold it reads 0.425–0.44 V with the ignition on
or the engine running, a step of the converter either way, and slid
away from 0.44 V as the probe warmed on 10/11 morning
(`vcds-step8c-after-2-001-033-036.csv`); **the front one cannot be
told from the logs**, exactly 0.435 V in all 230 engine-off samples
over five sessions and both probes, which a substitute value would
also give. A value that moves when its connector is off is live; one
that does not, for the front, leaves the front's circuit to the
multimeter alone. The multimeter on the harness side's signal pin with the
ignition on shows whether the ECU puts a bias on the line at all (a
few hundred mV says it does; *general*: many ECUs bias the signal
through a high resistance). Unplugging may store a circuit code for
that probe: read after, cleared by the owner. A socket seen
damp or green, or a jump in 033 or 036 as one lead is moved, is the find; both clean and
steady leave the new rear probe itself for S23. The wires to the ECU
are measured only with its plug off, so with 6n.

**8h, the loads against the sensors' voltages** (*the owner's request*,
10/11 night; `open.md` H21, *A shared earth*): an earth that the probes'
signal returns, the senders and the ECU share would move every voltage
referred to it when a load switches; a sound one lets only the supply
(004) dip. So each load step is read against what should not move:
the coolant and intake-air temperatures (004, NTC senders, a few mV a
degree when hot, *general*), the front and rear probes (033, 036), the
throttle's second sensor in volts at a fixed angle (060 field 2,
G188 — 060 read as a measuring block only; its basic setting is the
owner's, never Claude's), the air mass (002), the knock sensors (026)
and the heaters' resistance (041); and the sensors against one another.
The bus beside it marks the A/C and the lights, carries the engine
speed and both coolant readings at 10 ms (the ECU's and the gauge's,
already tested on `47`: steady to half a bit). **What it cannot see**
(*reasoned*): VCDS samples about once a second, so a load's step is
caught but noise faster than that is not; three groups at a time, so
the sets are run one after another, the sequence repeated. Four loads
because they are the largest the driver can switch from the seat, and
none needs anyone at the engine.

**8e, no spray and no seal on the probes' connectors** (`open.md` S23,
*The contact spray*; the research of 11/11): Bosch, Denso and Saab
forbid contact spray and grease on a lambda probe's connector, because
the probe takes its reference air along its own lead, and a solvent
drawn in lowers its curve; it went into the rear connector on the
morning of 10/11, the day the rear probe sank. Sealing the probe's own
lead airtight could starve it the same way; the fabric tape over the
harness side is not a seal.

**8i, the timing belt's marks** (*agreed with the owner*, 11/11): the
belt sits sixth for the idle, but its check costs a quarter of an hour
and no part, so it goes before the tests that cost a garage. VW's fault
table has 16725 / P0341 for a camshaft sender signal out of place, which
an empty fault memory makes less likely but does not exclude (`open.md`,
*What the forums say*, 11/11); a mark a tooth out (roughly 18° of crank,
*reasoned* from a sprocket of about 40 teeth; the AQY's not counted)
is visible at the sprocket. **Read**: both marks on — the belt is
refuted for the idle; one off — the belt is reset before anything else.
The 5 mm tolerance at the crank is from VW's text for the Mk4 2.0;
nothing of the AQY's own was read.

**8f after the harness** (10/11 late night): the battery out once more
after the probes' harness was taped (098 run on reconnecting, OK), so
032 relearns from zero on a repaired harness — a clean before and after against the −6.3 % of the
relearn drive; and the rear probe's signal (S23) read beside it.

**8f, 032 at every session**: the idle cell came back to −6.3 % in one
drive on the new probes (`open.md` S19), so what is left to read is
where both cells settle; **the clear of P0137 at the end of 8d reset
032 again** (`open.md` S3, *The clearing of 24/10*), so the relearn
starts once more. Read, never cleared by Claude; three drives because
the cells moved by one VCDS step at a time.

**8b, dropped 11/11** (*the owner's decision*): **the goal is the
fix, not the root cause** — "even if it went, I do not care whether it
was the probes or N80"; fewer tests, a repair where one is cheap. Its
two captured stops (after a brisk and a gentle drive, the cut at minute
10) would have named the settled cylinder and given N80 a reading
before; the captures `40`–`48` and the display's stops already show the
rough start after high revs (`open.md` S1, *The rough start of a warm
stop*), and item 9's leak-down decides between H1 and H3 anyway. *Until
11/11 morning 8b was one stop after a brisk run with the cut at minute
3.* **6m for 4** because 4 is now the cylinder with a
deficit of its own, and its injector circuit is the cheapest of the
three causes that act on 4 alone (H4; H3's runner gasket and H1's inlet
seat cost the intake off or a leak-down). **The display's stops** with a
word on what came before each, because a brisk run calms the idle by
itself for a while (`open.md` S1, *After high revs*) and the display's
spread is as large as the effect; the A/C's figure for `open.md` S1's
closing mark 2. **The days after** (*reasoned*, from SAE 2000-01-2858:
water flakes deposits most): the clean burns hydrogen to water vapour,
so a flake may come loose and lodge under a seat, an 18/10-like
drop-out; if one comes, a warm leak-down on that cylinder the same day
or the next is the one moment it can be told from a seat or a guide.

**8j, the canister** (*the owner*, 11/11; `open.md` S21, *The
canister itself*): the original charcoal; a canister that holds or
passes too little gives the purge check a small answer (P0440) without
any fault in N80, and a flooded one sends granules towards the valve.
Looked at before 8a so that a canister fault is not mistaken for the
valve's. **Blown through** because a blocked vent or a blocked port
starves the purge, and P0440 is what this ECU's check stores for too
little answer; a free path everywhere leaves the valve. **The tank's
line may pass one way only** (a roll-over or gravity valve, *general*:
on many cars), so a line that will not take air towards the tank is not
a fault by itself. **No compressed air**: it can break the charcoal or
drive it into the lines. **Never sucked on**: fuel vapour. Its place,
the right rear wheel arch, from the forum leads of 11/11 and the
owner's videos, not from VW's documentation.

**Item 8a, from 11/11** (*the owner*: the part ordered "to be sure",
after the research of 11/11 on P0172 and P0440; `open.md` S21, *Read
11/11*): N80 is the one part VW's fault table for this engine names
under both codes, and the Bosch check behind P0440 opens the valve at
idle and fails when lambda and the idle air hardly answer — what a valve
that already leaks while closed would give. **The tests so far were
weak**: blown by mouth (about 0.1–0.19 bar at most) against 0.6–0.7 bar
of vacuum across it at idle, and 25/10's canister cut off cold only.
**The gauge on the canister-side port, warm, N80 unplugged** is VW's own
test (TSB 2034072, written for US cars); **declined 11/11** (*the
owner*: the gauge is out of reach for weeks), so the old valve is not
tested before the swap and 032 before and after is what reads it. **032
before and after** says what the valve carried: an idle cell still at
−6 to −9 % with a tight new valve clears it of the standing offset.
**The photographs** because whether N112 and N80 share a vacuum tap is
not recorded. **Fitted when it arrives** (*the owner*, 11/11: the
fix comes first; 8b dropped).
**The details at a lamp** because this ECU keeps no freeze frame; with
them the next code can be set against fills, tank and weather.

**Item 8a — the purge valve, conditional until 11/11** (*the owner's decision*,
6/11 night: *this was "replaced after item 8's readings", his decision
of the same evening, until the valve was out*; **kept so 11/11**, after
the second research, *the owner's decision*: no swap and no pinched hose
at 8b). Out of the car it
passed air unpowered not clearly at all, at most "really very little"
(*owner*), it had no granules or fuel behind it, and it was cleaned with
its contacts and refitted (`idle-log.md`). The part is known and fits;
**a code once in eight years is acceptable** (*the owner*), so it was
to be bought if P0440 came back — *until 11/11, when he ordered it all
the same (above)*. *Until 9/11 also "or if item 8 leaves the
idle as it was and the purge path is the next candidate"*: the clean
changed cylinder 3, and P0440 was not stored that day. **The part**: the valve taken out on
6/11 is itself Bosch `0 280 142 353`, VW `1C0 906 517 A`, date code
`040` (`photos/n80-2026-11-06-label.jpg`); Auto Kelly lists the same
for this car, engine AQY (*owner*, 6/11), so a new one is the same
part and fits as it is (in stock at Auto Kelly, not in Prague on 6/11).
**What was looked at, 6/11** (`idle-log.md`):
no granules and no smell of fuel at the canister-side port, the rubber
hoses old but sound, so **the canister is not looked at and no hose is
changed** — a canister that shed charcoal would have jammed a new
valve open (*general*), and it shows no sign of it. **The plastic line
under the upper intake is left** (*the owner*, 6/11): seen whole with
the intake off several times, the smoke test showed nothing there, and
changing it means the intake off. **The filler cap is not on the list**:
it is new from about early 10/2026 (*owner*, 6/11, `vehicle-history.md`),
and this car has no tank pressure sensor and no leak detection pump (a
European car, the VIN), so the ECU can only open N80 and watch lambda
and idle air (block 070's fields), and a cap cannot fail that
(*reasoned*). **070 afterwards** is the ECU's own check of a valve that
opens; it is a basic setting, so the owner runs it, never Claude
(`CLAUDE.md`). **No warm A–B–A with the hose plugged before it** (*the
owner*, 6/11: not needed); so the idle after a swap would be read
against the readings before it, on the display, with the A/C state
named. *Until 6/11 night this item also had the hoses and the canister
checked while the valve was out, and the part compared with the old
one; done.*

**Item 9's garage session** (*agreed with the owner*, 11/11, after the
second research): everything that needs the upper intake off in one
visit, warm. **Cylinder 3's leak-down twice, two crank turns apart**,
because a flake under the exhaust seat (SAE 2000-01-2858: trapped by
chance) moves between readings where a worn seat does not; **a warm
compression test** straight after, because a tappet stuck pumped up
holds its valve a hair open and only shows there or in the leak-down;
**VW's tappet check** (the 2-valve 2.0's procedure: a wedge and a
0.2 mm feeler) because it finds a tappet gone soft, and VW calls a
cold-start clatter like 8/11's normal, so only the check says more.
The engine cools while the intake comes off, so **a tight 3 there does
not clear a seat that leaks hot** (`open.md` S1, *The rough start of a
warm stop*). 6m and the gasket because the intake is off anyway.

**Item 9 — after the decarbonisation** (*agreed with the owner*, 4/11,
after the research): the cheapest tests that name a part on 3 without an
injector swap or a plug change. **The CO₂ test** for H20, the cheapest
of all; **the stethoscope** for a lifter or valve on 3 (H1); **the warm
leak-down** decides H1's seat — VW gives no procedure for this engine,
so the garage's own, the four against each other: where it hisses names
the leak (tailpipe an exhaust valve, throttle an inlet valve, the oil
filler the rings, bubbles in the tank H20's gasket, the next plug hole
the gasket between cylinders; *general*), and 3 against the others
matters more than any absolute figure. Warm because a seat that leaks
hot can seal cold, which is what A4's cold compression missed. The
crank held because the air turns the engine; **the generic OBD-II
read** asks whether this ECU keeps what its VW view does not show
(`open.md`, *What the forums say*, 4/11). *No pinch of the vacuum
lines*: proposed 4/11 for a line near runner 3 and dropped the same day —
every line joins the common intake (*owner*, `open.md` H3).
**The head stays on** (*the owner*, 4/11, leaning): the seat is reached
only with the head off (`open.md` H1), tens of thousands of crowns, for
an engine that burns well everywhere but at an idle without load. If
the leak-down names the seat, S1 closes as *acceptable, cause known*
(`open.md` S1, *When S1 closes*); if it does not, cleaning can go on
(a soak through the plug holes reaches the crown). **What would reopen
it** (*general*, *reasoned*): a leaking exhaust seat can burn over time,
so 014 climbing, P0303 stored without a cut, or the warm idle getting
worse beyond its spread are read as a seat getting worse.

## Standing items — why

- **`Misfires` beside `IdleHealth`** (*the owner's request*, 4/11):
  an estimate of VCDS 014 off the bus — the dips of 20 rpm in the last
  minute of standing idle, zero whenever 014 had not counted in that
  minute over every capture with a 014 log, and near zero with the A/C on
  as 014 is (`docs/firmware/can-decoding.md` question 11, *Misfires*). It lets a stop say
  whether 014 is counting without VCDS; VCDS stays the instrument.
  `--preserve-eeprom` keeps the stored trip and tank (`flashing.md`).

- **Every drive** (*the owner's decision*, 6/11/2026). **Idling is not
  limited for the converter any more**: a share *f* of misfired
  combustions heats it by about f × 2,500 K, so the idle's 0.25–1 %
  (2 % at the very worst) is tens of kelvin, against the hundreds a
  cylinder dead under load would add (`open.md` S3, *What it costs the
  converter*). Hours are still avoided — wear and fuel, not the
  converter. *Until 6/11 these items drove off within half a minute,
  never warmed the engine standing, switched it off at stops over a
  minute or two and on arrival after a hard drive, and kept loads on
  at idle, all for the converter, from 122 of 129 counted misfire
  events beginning at a standing idle (`open.md` S3).* **A flashing
  lamp** is the ECU's own converter-damage rate, a 200-revolution
  window weighted by speed and load (SSP 175, `vcds.md`) — the one real
  converter risk, a cylinder dropping out, above all under load. **A
  steady lamp** is an emissions fault: P0300 above 2 % over 1000
  revolutions, or P0440 as on 6/11 (`open.md` S21).
- **`IdleHealth` in the everyday state only** (*owner's decision*,
  28/10/2026). *Until 28/10 a warm stop was read in two states, 2 minutes
  every load off and 2 minutes every load on (owner's decision, 19/10),
  and the everyday state only when there was no time.* Every load on read
  calm every time and 014 counted nothing in it, so the pair stopped
  telling anything new, and four minutes standing worked against keeping
  the idling short. The everyday state (*owner's decision*, 23/10) — one
  fixed mild load, chosen because four minutes and main beam at every stop
  did not fit his driving — is now the one ruler, compared with itself. It
  sits between the two old states, calmer than every load off and rougher
  than every load on. **The closing of S1 and S3 is not read on it**: the
  marks stay in loads off (`open.md`, *When S1 closes*), read when the owner
  closes them, probably with the overrun too (*owner*, 28/10).
- **The fault memory** (*owner*, 18/10/2026): every session starts from
  an empty memory, and the saved file keeps what the session stored.
  Only when VCDS is connected anyway (*owner*, 24/10/2026): a plain
  drive is not worth a laptop, and a lit or flashing lamp is the
  backstop for what it would have caught.
- **The cover's nuts**: the gasket settles (`refuted.md` D5).
