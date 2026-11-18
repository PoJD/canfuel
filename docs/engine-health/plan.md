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
Captures only where an item asks for one. **Next: 8q, the timing belt
at a garage, 7/12**; then item 9; **the new rear probe when the seller
sends it** (8e), **its harness at the end**; **8u, 8v, 8w by
opportunity** (*the owner*, 15/11), and **6r**, the owner's scope, best
before 8q, **6t**, the second can of BG 44K Platinum and a captured drive before 8q,
and **6s**, the cleaner drawn in (17/11). *What is done is `idle-log.md` and
`vehicle-history.md`; a step leaves this file when it is done.*

**6. Drive normally; the MFD back in from 15/11** (*the owner*, after
8h): `IdleHealth` and `Misfires` on the display again, **back in after
8z's captured drive** (17/11, `54`) until 8q's captured drive.
Brisk driving once warm is welcome. When captures resume, the MFD
comes out for them — the converter goes with the MFD.

- **Captures, when they resume**: **as many drives as
  the laptop can ride along**, each ending in a warm stop where one
  comes; Claude reads from the capture whether a drive was gentle
  or brisk (*the owner*, 12/11: nothing to report). Claude runs
  the capture; **VCDS on 014 always** (with 020 and 033 on a drive
  with pulls), 032 and 055 for 20 s before the drive and after the
  stop (8f). Once the oil is at
  90 °C or more, **two or three full-throttle pulls** in 3rd or 4th
  to about 5,500 rpm where it is safe. Write the stops. **No
  injector cut**: Claude names the cylinders from the capture
  (`tools/cylscan.py`).
- **To end a captured drive: "konec" into the chat** — at the last
  idle before home, or up to about five minutes before the garage.
  Claude closes the capture and VCDS at once and uploads while the
  drive goes on; at the garage, switch off and go. **A stop of about
  five minutes** (a petrol station) when Claude asks for one.
- **At the same warm stops, `Misfires` beside `IdleHealth`** into the
  chat; **not MisfAvg until the converter's drop-outs are settled**
  (*the owner*, 18/11; `docs/firmware/open.md` 12) (0x604; JP1 stays off, so 0x603 and the
  LEDs are dark by design).
- At several warm stops, **a word on what
  came before each stop** (queuing, or a brisk stretch), and the A/C's
  figure too whenever it happens to be on; **an odd cold misfire or a
  drop-out on one cylinder** goes into the chat at once.
- **A hard jerk at a crawl or on moving off** (`open.md` S12): the
  clock time into the chat as soon as it is safe, with the gear and
  roughly the speed; on a captured drive, **"teď"** at once.

**6i. The oil level on the new oil, about every 500 km** from the first
reading (27/10, 155,024 km, at the top mark; 11/11 evening about
1–2 mm under it; **next about 156,400 km**): the car on level ground
and **at least 5 minutes standing**, the dipstick out, wiped, in, out,
and **photographed**; the odometer into the chat. Any top-up: the litres and the odometer
into the chat.

**6n. The injector circuits to the ECU** — later, only with VCDS on the
laptop: 032/055 read first (unplugging the ECU may reset them, as a
disconnect does), then the ECU's 80-pin plug off. One extension lead
for all four: its own resistance measured end to end and taken off.
**From contact 2 of each injector connector to its pin: 73 (cylinder
1), 80 (2), 58 (3), 65 (4)**; check the numbers on the plug, and enter
its sockets only with a thin pin of the right size, never a meter tip.

**6r. The oscilloscope on injectors 3 and 4 and on the two senders**
(*the owner*, 17/11 evening: his own scope; by opportunity, best
before 8q). A warm idle, oil 90 °C or more, the everyday state; the
probes only back-probed into the connectors from behind, nothing
pierced, nothing written to the ECU:

- **Injector 3 against injector 4** (with the upper intake on only
  these two are reached; *the owner*, 17/11): one channel on contact 2
  of each — the ECU's side, 4's violet/blue wire, 3's violet/red; the
  supply wire is the one 0.2 Ω from its neighbour's — by a fine pin
  pushed under the insulation if back-probing is not possible, the
  hole sealed afterwards, the probes held clear of metal; the scope's
  earth at the battery's minus; a few
  seconds with every load off and a few with the A/C on; if a capture
  runs, a few more in a swell when Claude says so. A current clamp on
  one injector's wire as well, if one is to hand.
- **G28 and G40 together**, one channel on each sender's signal wire
  (Claude says which before), 30 s of warm idle; the same again with
  the same settings after the new belt (8q).

The files, or screenshots showing the time base and the volts per
division, into the chat.

**6t. Two cans of BG 44K Platinum, before 8q** (*the owner*, 17/11
evening): the same product as in October, **208** and "Platinum" on the
can. *The first is in (18/11, about 25 l).* **The second into a full
tank when this one is low**; each tank driven as usual, mixed — revved at times, some longer idles (*the owner*, 18/11 evening; until then briskly throughout). Nothing else changed meanwhile —
no oil change, no other cleaner. **At the end of the second tank, before
7/12, two captured drives** (or one with two stops), each to a warm stop
of at least ten minutes, the everyday state, as 6's captures: **one
after a brisk stretch, one after a gentle one or a queue**. Each can into the chat when it goes
in, with the odometer. A capture before then is welcome
(6's captures) and is not 6t's reading.

**6s. The valves' carbon cleaned from the intake, GM's way** (*the
owner*, 17/11 evening; by opportunity). Outdoors, the engine warm:

- A combustion-chamber cleaner sold for drawing in through the intake;
  its label and the hose to draw it in by into the chat first (Claude
  says which vacuum port behind the throttle).
- At about 2,000 rpm, held by hand, the cleaner drawn in slowly in a
  thin stream, the amount the label gives for a 2.0 l engine, never a
  gulp; if the engine stumbles, less.
- Engine off at once; **a hot soak of 2.5–3 hours, not longer.**
- Start (smoke is expected), drive briskly about 15 minutes, **then the
  oil changed**.
- The next warm stops on the MFD, or a captured drive; if it improved
  but did not cure, once more.

**7. Only if Claude asks after 6:**

- **The high-voltage side in the dark**, a damp evening, warm idle:
  bonnet open, lights off, look along the leads and the coil for a
  spark or a blue glow; then a fine water mist over one lead at a time
  and the coil, hands and bottle clear. Write anything seen and which
  lead the engine stumbled at.

**8a. At any engine lamp**: the odometer, the tank's needle and the outside
temperature into the chat, and 032 read before the code is cleared.

**8u. The fuel pressure** (*the owner*, 15/11; the gauge being
ordered 15/11 night): a gauge **with a shut-off tap, a scale of 0–4 or
0–6 bar and good to 0.1 bar** (class 1.6 or better), teed into **the
supply line where it meets the rail** — before ordering, a photograph
of that joint into the chat, so the adapter fits. Fitted on a cold
engine, the system let down first: a rag round the joint, loosened
slowly. Then, the tap open, the vacuum gauge on the intake beside it:

- **From the cold start to the radiator fan, at idle**: the pressure
  and the needle (steady, trembling, wandering) every few minutes.
- **Warm: three minutes without touching anything**, eyes on the
  needle — whether it moves, when, and by how much.
- **The regulator's vacuum hose off, then on again**: both pressures,
  and the intake's vacuum.
- **A blip of the throttle**: where the needle goes and how fast it
  comes back.
- **Engine off, the tap left open: the pressure at once, after one
  minute and after ten.** Under 2.0 bar at ten: start again, let it
  build, switch off and shut the tap in the same moment, and read
  again after ten.

Every figure into the chat. No smoking, the engine cold before the
gauge comes off.

**8v. The plugs at their next change** (*the owner*, 15/11): before the
new ones go in, the four old ones laid out in firing order and
**photographed close on their firing ends**, plug 3 beside the
others; oily, wet or sooty on one, into the chat.

**8w. The cylinder 4 knock window** (*the owner*, 15/11; until then out
of this plan, *the owner's decision* of 9/10):

- **G66, the knock sensor at 3 and 4**: its connector off, looked
  into, back on until it clicks; the sensor's bolt checked with a
  torque wrench at VW's figure (Claude reads it out of the manual
  first). What was found into the chat.
- **A loose part at about 3,000 rpm in neutral**, warm, the bonnet
  open: someone holds 3,000 rpm while the other listens and feels
  along the brackets, the heat shields and the ancillaries for a
  buzz.
- **026 in neutral and 020 on a drive with pulls**, with VCDS
  connected anyway (020 on 8q's captured drive or any drive with VCDS on): 026 from
  idle to about 3,500 rpm in neutral, slowly; 020 on two or three
  full-throttle pulls in 3rd or 4th.

**8q. The timing belt renewed at a garage, 7/12** (*the owner's decision*,
13/11; the date *the owner*, 16/11): the belt, its tensioner and idler, and the water pump.
**Before the old belt is loosened**, the mechanic sets the crank to
TDC of cylinder 1 — by the flywheel's mark in the gearbox window
(VW's reference) or the piston at plug 1, not by the pulley's notch —
and says how many teeth the camshaft sprocket's
mark is off its mark, which way, and photographs both marks; the
answer into the chat. Before the garage: **`54`'s warm stop** (17/11,
after the gasket) is the one the belt is set against. After it: the
fault memory read, 032/055 for 20 s, and a captured drive to a warm
stop of ten minutes.

**8f. 032 for 20 s at every session with VCDS connected**, until both
cells have held for three drives; **and 036 for a minute** at a warm
idle and on the road when VCDS is on anyway (the rear probe watched
now and then, *the owner*, 11/11). **032 read first, before any code
is cleared**; **on a logged drive, 001 in place of 055** (G62's
reading; on a captured drive the capture reads it) **and 014
always** (a P0303 stored with no cut: its time is what the log gives).

**9. By what 8q leaves** (Claude says which):

- **A CO₂ ("block") test of the coolant**, warm, at a garage or with
  a kit.
- **A stethoscope (or a long screwdriver) on the cam cover above
  cylinder 3 and above cylinder 4, hot**, against 1 and 2: a tick or
  a hiss on one, at idle.
- **One garage session with the upper intake off, straight after a
  drive** (oil at 80 °C or more), in this order:
  - **a warm leak-down on all four**: all four plugs out (the same
    plugs back afterwards; plug 3's gap measured while out); each
    cylinder at TDC on its compression stroke, firing order 1-3-4-2;
    the crank held while the air is on. For each: **the percentage,
    and where it hisses** — tailpipe, throttle, oil filler, bubbles
    in the coolant tank, the next plug hole. **Cylinder 3 twice**:
    the crank turned two full turns between the two readings.
    **The engine switched off in a swell** (agreed 12/11 evening):
    on the way in it idles until Claude, from the capture, says 3
    is swelling — or, with the MFD in, `IdleHealth` has stood above
    75 for a minute with every load off — and is switched off then,
    not after it has calmed;
  - **a warm compression test on all four** straight after, the
    throttle held open;
  - **the cam cover off: VW's tappet check** — the cam of each tappet
    pointing up, the play felt; more than 0.2 mm, the tappet renewed;
    otherwise each pressed down with a plastic or wooden wedge and a
    0.2 mm feeler tried between cam and tappet; the eight results
    into the chat;
- With VCDS connected anyway after a stored P030x: **a generic
  OBD-II read** (modes 02 and 06), read only, saved.
- **Kept, not now** (*the owner*, 17/11 evening): the warm leak-down
  above done at 8q's visit instead, before the old belt is loosened;
  and, at a garage that has them, **a running in-cylinder pressure
  trace on 3** (a transducer in plug 3's hole, injector 3 unplugged,
  cylinder 2 as the reference) before and after the belt, and **the
  secondary ignition lead by lead**.
- **No head off** (*the owner*, 4/11, leaning, not final): if the
  leak-down names 3's exhaust seat, the car is driven as it is and S1
  most likely closed as *acceptable, cause known*.

**8e. The probe when it comes, the harness at the end** (*the owner*,
11/11 and 12/11; `refuted.md` D13). **The new rear probe went back to
the seller under warranty 13/11; its replacement fitted when it
comes**, the old rear probe on the car meanwhile. The new one
is fitted as the first was: Bosch's paste on the thread only, nothing
in the connector, the lead clear of the exhaust and not pressed into
the harness box. If P0137 comes back with it, the harness — cold and
the ignition off, the connector off and **the signal wire from the
harness-side socket to the ECU's pin** read for continuity and for a
leak to earth, the lead flexed by the exhaust. Nothing measured with the engine running, nobody under
the car with it on. Then, at a cold engine, from below:

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
  same way. They are taped and the bundle wrapped (*the owner*, 10/11
  night); the splice is what is left.
- **The rear socket's broken-looking outer terminal**, on the rear
  probe's signal (the cavity meeting the probe's black wire): the
  terminal replaced —
  a VW repair terminal crimped on, or the socket half with its
  pigtail — before anything else is measured on that wire.
- **The rear connector's bent pin** straightened so it seats like
  the others; both connectors dried again, then **pushed
  until each latches with a click** — the front one included.
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
  heater on 2, the lights on** (*the owner*, 8/11) — at warm stops that come anyway (oil
  95–100 °C, neutral, no throttle), with the oil temperature; any other
  state is named. **No stop is made or lengthened only to read it.**
- **The fault memory after every session with VCDS connected**: read,
  saved, then cleared by the owner by hand. Not after a plain drive.
- **A code in the memory before a logged drive pauses it** (*the owner*,
  11/11): Claude stops the log and says the codes; the drive starts
  only after the owner has cleared them or the fault is repaired, on a
  fresh log.

---

# Part 2 — why, and how it is read

## The rule — the owner's decision, 27/9/2026, amended 18/10/2026

**The idle comes first**: the unsettled idle (S1) and the misfires 014
counts at idle (S3). So:

- **Fix, then look.** Each step is a repair; the only readings taken are
  the ones that decide the next step.
- **No test for its own sake**, and nothing unrelated to the idle is
  pursued until it is solved — unless it could be related.
- **Run the engine as the day needs it**: the idle's misfires heat it by tens of kelvin at most (`open.md` S3,
  *What it costs the converter*).

`open.md`'s tests are reference, **not a to-do list**; what goes into
this plan is the owner's choice (*15/11*: 8u, 8v and the cylinder 4
knock window, 8w, which stayed out from 9/10 until then).
Where the work stands is in `idle-log.md` and `open.md`, *Where it
stands*.

## Step 3 — why, and how it is read

**Idle solved → stop and record** (`open.md` S1, *When S1 closes*; S3,
*When S3 closes*). Otherwise each item decides whether the next is
needed.

**6n, the injector circuits to the ECU** (`open.md` H4, *What the loom
can and cannot do unseen*; the supply side and the injectors
themselves were measured sound on 17/11, 6m): a raised resistance in
3's control wire makes no code but starves its injector. The manual's figures: injector 14–18 Ω
at about 20 °C, each wire at most 1.5 Ω, contact 1 the shared supply from
J17, contact 2 the ECU's output at pins 73/80/58/65. Read as a comparison:
three alike and one higher (tenths of an ohm on a wire) names the
joint; all alike clears that wire.

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

**Item 6 — the drives.** The display follows the idle at every warm
stop; the captures read where it got to. **Read**: `tools/cylscan.py
--minutes` on the idles — **3's deficit and 3's weak strokes** minute
by minute against the other three, and `--vcds` with the drive's 014
log, 014's rises by cylinder (`open.md` S1, *Every stroke named*);
`tools/swellscan.py --floors` for floor and swell; beside `IdleHealth`
and 014 themselves, which are the closing marks (`open.md`, *When S1
closes*, *When S3 closes*). **3 at its floor with no swell through ten
minutes is list B's part gone; 3 swelling as before under a calm grade
is list A's.** **No injector cut**: the strongest slot names the
cylinders, and a cut is one of the things that ends a swell. The stop
of 10 minutes because the settling takes 3–8. **The groups**: **014**
always; **020** on a drive with pulls, cylinder 4's knock retard (S4),
which shows only on pulls above 3,000 rpm warm, hence the pulls;
**033**, the front loop's live regulation. **001 is left out** on a
captured drive because the capture carries the coolant (0x288) far
faster. **The MFD back in from 15/11** (*the owner*, after 8h): what is
left before the belt is no reading a capture gives that `49`–`54` do
not; `54` (17/11) is the stop after the gasket, and the belt's (8q)
is set against it.
**"Konec" and the five-minute stop** (*the owner*, 12/11 night): the
laptop only records and uploads, the reading is a cloud session's
(`CLAUDE.md`, *Sessions at the car*), and the capture's last minutes
home are given up for it. A queue crawls more than it stands (`50`),
so a stop long enough for a swell is asked for, not waited for.

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

*The warm exhaust test (H2) was dropped 15/11 (*the owner*): the cold
tailpipe and smoke tests found nothing, the manifold shows no soot,
032's idle cell takes fuel away where air ahead of the front probe
would make the ECU add it, the front loop holds through 3's swell, and
the rear probe's sinking went with the old probe (`open.md` H2).*

**Item 7 — the high-voltage side** (`open.md` H4; `refuted.md` C24): the roughest
reading on record came on a foggy morning (`open.md` S1, *Temperature*),
and the mist supplies the moisture a tracking boot or coil needs. Late
because the coil is from 6/2026 and the leads are new again; it is free.

**8e, the probes' tightness**: they were tightened by hand to about 50
Nm estimated, without a torque wrench (`vehicle-history.md`), and the
rear probe switched to the front's swing after 18 minutes of idle on
10/11; a probe seated
loose lets air into the exhaust at idle's pulses, the second zone of
H2 of its own making (*reasoned*). Cold, because the exhaust then is at
the temperature they were fitted at. **The rear probe's
lead** (`refuted.md` D13 (S23)): 0.000 V at full load is not the gas, so the
signal failed on its way to the ECU, and it came back at a cooler idle
— heat on a lead or a connector the likeliest (*reasoned*); the lead was
tidied by the owner when the probe was fitted, so its run is looked at
first, the connector second; a lead and connector found sound leave the
new probe itself (a warranty matter). Cold, so it can be touched.

**S12's jerk by the clock**: the bus cannot show a jerk at a crawl, so only its time
lets a capture or a VCDS log be read at that moment — the stroke, the
load, 014, and from a capture the cylinder (`open.md` S12).

**8e's cracked wire and latches** (`refuted.md` D13 (S23), *Found at the
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

**8e's sockets** (`open.md` H21): the swap changed the probes and
their own plugs, not the harness side, so a fault there survives it —
S19's idle cell perhaps. **At the end** (*the owner*, 11/11): the rear
probe has no direct hand in the mixture, no probe code was stored
before 10/11, the broken-looking terminal may be how it was made; the
probes are watched through 8f's 036 meanwhile. *The flexing with the
ignition on (8g) was dropped 11/11; what it argued is kept below for
the sockets' reading.* **With the ignition on and the
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
multimeter, each wire end to end with the ECU's plug off (6n). **Whether the
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

**8e, no spray and no seal on the probes' connectors** (`refuted.md` D13 (S23),
*The contact spray*; the research of 11/11): Bosch, Denso and Saab
forbid contact spray and grease on a lambda probe's connector, because
the probe takes its reference air along its own lead, and a solvent
drawn in lowers its curve; it went into the rear connector on the
morning of 10/11, the day the rear probe sank. Sealing the probe's own
lead airtight could starve it the same way; the fabric tape over the
harness side is not a seal.

**Item 9's leak-down on an engine switched off in a swell** (*agreed
with the owner*, 12/11 evening): straight after a fall 3 is nearly
level with the others (−1 to −5 %), so a leak-down made then tests a
seat at its tightest; the engine cools while the intake comes off as
it is, and a film on a seat may not last that either — a tight 3 there
still clears nothing, a leaking one names it.

**8q, the timing belt at a garage, 7/12** (*the owner's decision*, 13/11,
after 8i): 8i read the cam's OT mark set and the crank pulley's one
notch 30–60° of crank from the groove on the block by eye
(`open.md`, the row A2) — 2.2–4.3 teeth of 13.85° (1.0–3.0 by the
owner's fingers) with the cam advanced if those are the true marks;
the groove is not one of VW's references (the same row, 17/11) (the direction the owner's, read
off the part), which the flat full-load pulls and the air the engine takes at full
throttle argue against (485 mg a stroke at 5,200 rpm against 496 at
2,400, 85–90 g/s at the top; the row A2); the
piston at plug 1 that would have settled it was declined. The belt
is nine years old (10/2017), so renewing it loses nothing either way,
and the owner leaves the work to a garage. **What makes it a test**:
the mechanic's count of teeth before the old belt comes off says
whether 8i's reading was true — **the only reading of the true marks
left** (no gearbox window to be seen, *the owner*, 14/11; VW checks
the flywheel's mark in that window before the belt comes off and
after, so it is most likely hidden, not absent: `open.md`, *What the
forums say*, searched again 17/11); the captured
warm stop before and after says whether the common part (list A)
moved — down by a clear step if the cam was out, unchanged if it was
not (H0 then gains) — **and whether 3's floor, its swells' depth and
number and 014 moved** (*the owner's question*, 17/11): a tooth adds
or removes burnt gas on all four alike, but a cylinder already at its
edge may answer to it far more than the others (*reasoned*), so the
belt may move list B as well. Nothing in 8i was loosened;
VW's 5 mm at the crank was for the Mk4 2.0; VW's own procedure for
the AQY's family was read 17/11 (the same section).

**Why the flywheel or the piston, not the pulley** (the fourth
research, 17/11; `open.md`, *What the forums say*, searched again
17/11): VW sets the crank by the damper's mark against the bottom belt
guard and checks it by the flywheel's mark; the damper's outer ring can
slip on its rubber, so the notch alone could carry 8i's error into the
mechanic's count.

**6r, the scope** (the fourth research, 17/11; `open.md` H4 and the
row A2): a raised resistance in 3's control wire or a weak output
stage delays the opening and leaves a higher voltage across the
switch, which an output stage of the usual kind does not diagnose;
every other cause predicts 3 and 4 alike, and 6n's ohms at rest cannot
see a fault under current; **since 17/11 evening the floor's own
test** — 3's floor is a fixed amount that load does not shrink, as
fuel short by a fixed amount is (`open.md` S1, *The floor and the
common part read apart*). G28 against G40 puts the cam's phase on the
crank's wheel with no marks read, so a tooth shows as 13.85° between
before and after the belt; no trace of a healthy AQY was found, so it
is read before against after.

**6t, the 44K again** (*the owner's decision*, 17/11 evening;
`open.md` S1, *The floor and the common part read apart*): the level of
3's floor has not moved since 24/9, but the time 3 spends on it rose
from 0–20 % of the warm idle to 21–81 % across the week of 23–29/10 —
two tanks of 44K, the regulator's hose, the EPR flushes and new oil —
and not after the Liqui Moly can of 15/10, which the flake of 18/10
followed. The same product, so the result compares with October's;
nothing else changed, so it is the fuel's side alone; the capture before
8q, so the belt's comparison starts from it and the two do not merge.
**Driven mixed, not briskly throughout** (*the owner's decision*, 18/11
evening): his reasoning, that the cleaner may act better where the burn
is less complete. On this engine the injector sprays onto the back of
the intake valve at every load, so the intake side gets the cleaner
however the car is driven (*general*); the exhaust valve and its seat
see only what survives the burn, and a misfiring stroke on 3 at idle
passes its charge, the cleaner in it, out unburnt (*reasoned*; how
much that cleans is not known). What it costs: October's two tanks were
driven briskly, so the comparison with them loses one like-for-like
condition; the reading against `44`–`54` by kind of stop stands.
Read against the stops of the same kind on `44`–`54`, not against one
(*the owner's point*, 17/11: the time on the floor runs 8–81 % by
capture, 28 % pooled over `44`–`54` and 10 % over `19`–`43`; after a
brisk drive `49` 81 %, `44` 58 %, `51` 41 %, `54` 34 %; after a gentle
one or a queue `50` 8 %, `52` 14 %): the time on the floor, its level,
the swells' depth and share. **Only a change past that spread counts**
— the floor above about 80 % at more than one stop, or the swells
clearly shallower and rarer. If it moves nothing,
the oil's side (an EPR flush with the next oil change) is what is left
of that week.

**6s, the cleaner drawn in** (*the owner*, 17/11 evening; the fourth
research, `open.md`, *What the forums say*, searched again 17/11): GM's
PIP5029F and its successor 16-NA-383 are the one documented procedure
aimed at carbon on the valves short of the head off — drawn in warm at
about 2,000 rpm, a hot soak of 2.5–3 hours (longer and the deposit
hardens again), repeated if it improved; too much at low speed can
hydrolock the engine and bend a rod, hence the thin stream. The head
stays on (*the owner*: the belt job does not take it off, and the head
is not to come off), so this is what is left that reaches a seat on 3
from above. No maker gives a rate of success; the hydrogen took 3's
swell for a day and left its floor, so a step rather than a cure is
what to expect (*reasoned*). The oil change after because the cleaner
reaches the sump past the rings. What it does to the new probes and
the converter is not known; the label is read first for that.

**Item 9's options kept** (*the owner*, 17/11 evening; the fourth
research): at 8q's visit the engine is hot and the plugs may come out
anyway, which is why the leak-down could move there; a running
pressure trace reads 3's sealing unfired and the cam's timing from its
ramps (Pico's guided tests; a tooth hard to see cranking, plain at
idle); the secondary ignition reads a lean or diluted cylinder as a
high, short spark line and a leaking valve as low kV with hash. A seat
that leaks only while 3 fires hot may pass both static tests.

**8f, 032 at every session**: the battery was out once more after the
probes' harness was taped (10/11 late night), and the clear of P0137
reset 032 again, so it relearns on a repaired harness and the new
valve; what is left to read is where both cells settle (`open.md`
S19). Read, never cleared by Claude; three drives because the cells
moved by one VCDS step at a time.

**The display's stops** with a word on what came before
each, because a brisk run calms the idle by itself for a while
(`open.md` S1, *After high revs*) and the display's spread is as large
as the effect; the A/C's figure for how much load still calms it
(`open.md` S1, *Load smooths it*).

**8a, the details at a lamp**: this ECU keeps no freeze frame; with
the odometer, the tank and the weather the next code can be set
against fills and temperature, and 032 is reset by a clear.

**8u, the fuel pressure** (`open.md` H7, the row A4; S19): VW's
figures for this engine are about 2.5 bar at idle with the
regulator's hose on, about 3.0 with it off, and at least 2.0 bar ten
minutes after switching off (`vcds.md`). A high base pressure on all
four is the rail's form of H7 in list A; the pressure held after
switching off is S19's question — a rail that bleeds into a cylinder
while standing floods it, the bad start of 24/10 and P0172 (S19); a
fall below 2.0 is read by VW's order: the pump's non-return valve,
then the regulator, then the O-rings. Never gauged on this car.
**VW's procedure** (*Checking fuel pressure regulator and holding
pressure*, `vcds.md`, read again 15/11 night): V.A.G 1318 with its
adapters in the supply line, a shut-off tap in the gauge; the page
does not name the union, hence the photograph. **What a figure is
worth** (*reasoned*: the flow goes with the square root of the
pressure across the injector, 3.0 bar by design): 3 % of fuel is
0.2 bar, 6 % is 0.4, 8 % is 0.5 — so the gauge has to be good to 0.1,
and a 10 bar workshop gauge is not. **How it is read**:
- **2.4–2.6 at idle, 2.9–3.1 with the hose off, the difference equal
  to the intake's vacuum, the needle still through the three minutes,
  2.0 and over at ten**: the rail is out, in every form — H7's row A4
  goes to `refuted.md`, the idle cell is left as 8x read it (17/11:
  learnt with 070's valve shut, `open.md` S19).
- **High at idle, right with the hose off** (2.8 and over against
  3.0; the difference smaller than the vacuum): the regulator not
  getting the intake's vacuum. **Not expected** (*the owner*, 15/11
  night; `refuted.md` C20): on 6e the hose off took the regulation to
  −8.6 and −10.2 %, the whole step a regulator owes its reference, so
  it had its vacuum, and he feels the vacuum at the port with a
  finger. *This stood here as a live reading until he pointed at 6e.*
- **High both ways** (2.9 and 3.4, say): the regulator's own setting
  (the part of 6/2026) or a return that does not flow freely. It
  would pull both cells down alike, which 032 does not show; a return
  that throttles would show more at idle than on the blip.
- **The needle rising by 0.2 bar or more inside the three minutes**:
  the step of S19 (*The old logs re-read for the split's form*) is the
  rail's, not the purge's.
- **A needle that trembles or wanders at idle**: a regulator hunting
  moves the mixture under all four faster than the loop follows — it
  would reach the idle's common part (list A) **and not 032**: a
  swing about the same mean learns no negative cell (*the owner*,
  15/11 night).
- **So two readings are left that could give 032's idle cell**: the
  fall after switch-off, below, and a return that throttles (high at
  idle, less so on the blip). The owner's reading, agreed: a
  pressure high at idle alone is refuted, a pressure high everywhere
  contradicts the part-load cell. The gauge is bought to close H7's
  rail and S19's start, with little expected of it.
- **Falling after switch-off**: with the tap shut and still falling,
  the pump's non-return valve — a long crank, nothing for the mixture.
  Holding with the tap shut, so lost on the engine's side: the
  regulator or **an injector that drips** — fuel per unit of time,
  most at idle, into one cylinder, which runs rich while the loop
  leans the other three: **the one finding that would give 032's idle
  cell, S19's flooded start and an uneven idle together**. Against it
  beforehand: the injectors are new and their tips were dry on the
  borescope, and 3 was weak on the old set.
- **Not read by this test**: the part-load cell. Low pressure under
  load shows only with the engine pulling, and the gauge does not go
  on a drive.

**8v, the plugs at their change** (`open.md` H18, the row A7): oil
past the valve-stem seals leaves an oily deposit on the firing end,
and a wet or sooty plug on 3 alone would point at 3's charge (list
B); the photograph because the plugs go in the bin.

**8w, the cylinder 4 knock window** (`open.md` S4, S5, H5): the ECU
books anything at cylinder 4's crank angle to cylinder 4 — G66 loose
or its contact poor, a part buzzing in a speed band, an arc at a
plug's end — and S5's excess shows in neutral with no combustion, so
it is not knock. G66's bolt because a knock sensor reads by its
contact with the block and VW gives it a torque; 026 in neutral
because that is where S5 lives, against
`vcds/vcds-neutral-026-003.csv`; 020 on pulls because 4's retard shows
only there, against `vcds/vcds-step2c-020-026-003.csv`.

**Item 9's garage session** (*agreed with the owner*, 11/11): everything that needs the upper intake off in one
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
warm stop*).

**Item 9's other tests** (*agreed with the owner*, 4/11): the cheapest tests that name a part on 3 without an
injector swap or a plug change. **The CO₂ test** for H20, the cheapest
of all; **the stethoscope** for a lifter or valve on 3 (H1), **and on 4 since 12/11 night** (`open.md` S4, *Why 4*: 4 gives 2–4 % less than 1 at every load and has a noise in its knock window in neutral, which a valve, lifter or lobe on 4 would give together; the tappet check already covers all eight); **the warm
leak-down** decides H1's seat — VW gives no procedure for this engine,
so the garage's own, the four against each other: where it hisses names
the leak (tailpipe an exhaust valve, throttle an inlet valve, the oil
filler the rings, bubbles in the tank H20's gasket, the next plug hole
the gasket between cylinders; *general*), and 3 against the others
matters more than any absolute figure. Warm because a seat that leaks
hot can seal cold, which is what A4's cold compression missed. The
crank held because the air turns the engine; **the generic OBD-II
read** asks whether this ECU keeps what its VW view does not show
(`open.md`, *What the forums say*, 4/11).
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
  converter. **A flashing
  lamp** is the ECU's own converter-damage rate, a 200-revolution
  window weighted by speed and load (SSP 175, `vcds.md`) — the one real
  converter risk, a cylinder dropping out, above all under load. **A
  steady lamp** is an emissions fault: P0300 above 2 % over 1000
  revolutions, or P0440 as on 6/11 (`refuted.md` D14).
- **`IdleHealth` in the everyday state only** (*owner's decision*,
  28/10/2026). Two states (every load off, every load on) were read
  until then; every load on read
  calm every time and 014 counted nothing in it, so the pair stopped
  telling anything new, and four minutes standing worked against keeping
  the idling short. The everyday state (*owner's decision*, 23/10) — one
  fixed mild load, chosen because four minutes and main beam at every stop
  did not fit his driving — is now the one ruler, compared with itself. It
  sits between the two old states, calmer than every load off and rougher
  than every load on. **The closing reads it** (*the owner*, 12/11): S3 on
  it alone, S1 on it and with every load off besides (`open.md`, *When S1
  closes*, *When S3 closes*), probably with the overrun too (*owner*, 28/10).
- **The fault memory** (*owner*, 18/10/2026): every session starts from
  an empty memory, and the saved file keeps what the session stored.
  **A code before a logged drive pauses it** (*the owner*, 11/11/2026): every
  drive starts from a clean engine. The clear resets 032 (`open.md` S3,
  *The clearing of 24/10*), so 032 and 055 are read first — a running
  log of them counts — and 8f's three drives count from the clear.
  Only when VCDS is connected anyway (*owner*, 24/10/2026): a plain
  drive is not worth a laptop, and a lit or flashing lamp is the
  backstop for what it would have caught.
