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
Captures only where an item asks for one. **Now: 8ae**, the air mass
meter's plug renewed when its parts come (ordered 26/11, expected
about 1/12; 8ab ended 27/11 with nothing reset). **Then 8e**, **the new rear probe when it comes (bought
24/11; expected 26/11, not come by 27/11, now 28/11)**; **8q, the timing belt
at a garage, 7/12**; then item 9; **8u, 8v, 8w by
opportunity** (*the owner*, 15/11), **8af, the ECU's supply branch,
another day** (*the owner*, 27/11), and **6r**, the owner's scope on
G28 and G40 another day, best before 8q, **6t**, the second tank of BG 44K Platinum driven down and two captured drives at its end, before 8q,
and **6s**, the cleaner drawn in (17/11). *What is done is `idle-log.md` and
`vehicle-history.md`; a step leaves this file when it is done.*

**6. Drive normally; the MFD back in from 15/11** (*the owner*, after
8h): **one photograph of the display after each drive** into the
album (*the owner*, 25/11: no more hundreds), more only when something
is worth it; `IdleHealth` and `Misfires` on the display again, **back in after
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
  chat; **MisfAvg too whenever StartCrank shows a value** — then the
  converter has run since the engine started (*the owner*, 18/11)
  (0x604, sent with or without JP1; JP1 on since 20/11).
- At several warm stops, **a word on what
  came before each stop** (queuing, or a brisk stretch), and the A/C's
  figure too whenever it happens to be on; **an odd cold misfire or a
  drop-out on one cylinder** goes into the chat at once.
- **A hard jerk at a crawl or on moving off, or the hopping at a light
  pedal** (`open.md` S12): the clock time into the chat as soon as it
  is safe, with the gear and roughly the speed; on a captured drive,
  **"teď"** at once.

**6i. The oil level on the new oil, about every 500 km** from the first
reading (27/10, 155,024 km, at the top mark; 11/11 evening about
1–2 mm under it; **26/11 about 1 mm under it, as the week before**
(*the owner*; 156,868 km, the bus at the start of that day's captured
drive); **next about
500 km after that**): the car on level ground
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

**6r. The scope on the two senders, G28 and G40** (*the owner*, 17/11
evening: his own scope; another day, best before 8q). A warm idle, oil
90 °C or more, the everyday state; the probes only back-probed into
the connectors from behind, nothing pierced, nothing written to the
ECU:

- **G28 and G40 together**, one channel on each sender's signal wire
  (Claude says which before), 30 s of warm idle; the same again with
  the same settings after the new belt (8q).

**The instrument** (*the owner*, 26/11 night): his **LHT00SU1** USB
analyser — under sigrok one analog channel (**1ACH**, ±10 V) and eight
digital ones (0–5.3 V); G28 on 1ACH, G40 on a digital channel. **A
laptop session; Claude runs it** with `tools/injscope.py` (*the
owner*); the owner only connects the wires. **Ready on the laptop
since 26/11 night**: the analyser on another USB cable (its own is
faulty), Zadig's WinUSB, `sigrok-cli` and PulseView installed,
fx2lafw finding it.
- **Never straight onto the car**: **the breadboard divider, 10 kΩ in
  series and 1 kΩ to earth** — row 10 the input, the + rail the middle
  point with the wire to 1ACH, the − rail earth, with the analyser's
  GND and **a second wire to the battery's minus**. Its ratio is
  **10.94** (the desk, 26/11 night); **the zero is read again at each
  session** with the input on earth (`injscope.py cal`). **G40** on a
  digital channel only after its signal has been read with the
  multimeter: at 5 V or under, through a 1 kΩ straight in; above, a
  divider of about 1:3 (20 kΩ and 10 kΩ), never 1:11, which would
  bring it under the 1.4 V threshold.
- **The 5V pin's wire off row 10** before the car.
- **The laptop on its own battery**, not on its charger, while the
  analyser's earth is on the car.

**6t. Two cans of BG 44K Platinum, before 8q** (*the owner*, 17/11
evening): the same product as in October, **208** and "Platinum" on the
can. *Both are in: the first 18/11 into about 25 l, the second 22/11 evening into a
full tank of 51.38 l at 156,539 km.* Each tank driven as usual, mixed — revved at times, some longer idles (*the owner*, 18/11 evening; until then briskly throughout). Nothing else changed meanwhile —
no oil change, no other cleaner. **At the end of the second tank, before
7/12, two captured drives** (or one with two stops), each to a warm stop
of at least ten minutes, the everyday state, as 6's captures: **one
after a brisk stretch, one after a gentle one or a queue**. A capture before then is welcome
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
- **S17, the resonance on the exhaust — asked of the garage at 8q,
  7/12** (*the owner*, 27/11: no second person at home; the steps are
  8q's): warm, in
  neutral, the revs raised slowly from idle to about 3,500 rpm and held
  where it sounds, while the other listens and feels along the exhaust
  from the manifold back — **the flex behind the manifold first** (the
  owner's suspicion), then its heat shields, hangers and brackets, then
  the ancillaries; on a lift, the flex looked at and the exhaust moved
  by hand for the knock. What was found and the band where it is
  loudest into the chat.
- **4's spells at a warm stop** (*the owner*, 25/11), on the next
  captured drive with a warm stop: a long or brisk drive to a warm
  standing idle of ten minutes or more, **020 logged with 014 through
  the whole stop** (VCDS, beside the capture); the capture says
  afterwards when 4 led.

**8af. The ECU's supply branch — another day** (*the owner*, 27/11;
`open.md` S25, H22). The engine running, warm or past the cold fast
idle, **every consumer on** (then the same with a seat heater only);
the multimeter's black lead **on the battery's plus post**:
1. **The fuse panel's map**: the upper pad of fuses **12, 9, 25, 26,
   20, 21, 28, 10, 29 and 32** — each reading is the loss from the
   battery to that fuse; those that sag with 10 and 29 share their
   feed.
2. Then the black lead **on the battery's minus post**: **bare metal on
   the body** and **bare metal on the engine block**, with a seat
   heater only and with everything on.
3. **The earth point by the ECU** (the dashboard's top off) only if 2
   or 004 against fuses 10 and 29 asks for it: bare metal beside the
   bolt, each ring's barrel and the copper just behind each crimp,
   with the ignition on and with the engine running; the rings renewed
   only on hundreds of millivolts.
4. The figures into the chat, with what was on.
5. **The flicker, with the LHT00SU1** (*the owner*, 27/11), the same
   two loads: **no divider, fuse against fuse only** (*the owner*,
   27/11: not against the battery) — **GND on fuse 32's pad, 1ACH on
   fuse 10's**, then on 29's; `tools/injscope.py capture`. **⚠ With GND off the car's minus,
   nothing else may join the laptop to the car**: no VCDS cable in the
   diagnostic socket, no USBtin, the laptop on its own battery, nothing
   else in its USB ports. **Never 1ACH straight on a fuse against the
   battery's minus**: 12–14 V is past its ±10 V.
   **A 10 kΩ resistor in each lead**, at the clip or pin end, its legs
   sleeved; the fuse reached by a pin pushed into its test slot and
   taped, **never a wire pushed into the fuse's socket** (it spreads the
   panel's contact). **Fuse against fuse is the owner's choice** (27/11: short
   leads, the difference that matters), probes perhaps held by hand —
   **then first both probes on the two pads of one fuse** (32), the
   hand's own chatter, and only what stands clearly above it counts;
   shorter series (`--count 10`) when held.
**The owner's intention** (27/11, the date not set): the fuse holder on
the battery (`1C0 937 549 A`), the main positive cable from the
battery and the cable to the alternator renewed; 2c's readings (004
and fuses 10, 29 and 32, the two loads) taken again after it.

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
**The alternator refurbished the same visit** (*the owner*, 27/11,
agreed with the garage by phone): it comes off for the belt anyway and
goes to the refurbisher next door; a new one only if it proves really
faulty. **Before the garage and after it, the charging measured** (S25): a
multimeter on the battery's terminals, warm, at idle and at about
2,000–3,000 rpm, **twice**: as on 26/9 (the headlights, the rear window
heater and the blower on), and with **every consumer usually on at
once** (those three, the seat heater, the wipers if it rains), **the
MFD's reading beside the multimeter's** each time; the figures into
the chat, and what the refurbisher renewed (brushes, regulator,
bearings, rectifier). **And the ripple** (*the owner*, 27/11): the
same multimeter on **V~ across the battery's posts** — first with the
engine off (near 0; if it reads volts, the meter does not block DC and
the reading cannot be made with it), then at idle with every consumer
on; before the garage and after.
**The same visit, asked of the garage** (*the owner*, 27/11; 8w's
first item; the exhaust itself said to them on the spot): **the exhaust's resonance and knock (S17), and the slow
puffing on engine braking downhill (S14)** — the car on the lift, the
flex behind the manifold looked at and the exhaust moved by hand for
the metal knock; warm, in neutral, the revs raised slowly to about
3,500 rpm while a mechanic listens along the exhaust from the manifold
back (the flex, the heat shields, hangers and brackets). What they
found into the chat.
**And the squeal (S26)** (*the owner*, 28/11): the garage told of a
loud squeal now and then, often when the A/C comes on; **the ribbed
belt** looked at when it comes off for the timing belt (glazed,
cracked, worn ribs: renewed), **its tensioner and the idler** turned by
hand, **the A/C compressor's pulley and the power steering pump's**
turned by hand for roughness; the refurbisher told of it too (the
alternator's bearings and its pulley). What they found and renewed
into the chat. **Until then**: when the squeal is heard on a captured
drive, its clock time into the chat.

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
  drive** — the leak-down at the earliest about half an hour after the
  engine stops, the time the intake, the lead, the plug and the
  tester take (*the owner*, 18/11; 3's plug is reached only with the
  intake off) — in this order:
  - **a leak-down on all four, as warm as that allows**: all four plugs out (the same
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

**8ae. The air mass meter's plug renewed** (*the owner*, 26/11; the
parts ordered 26/11: the housing `1J0 973 999 A` and three repair
wires `000 979 026 E`, `vehicle-history.md`). Never on the same day
as another change.
1. **Before**, the engine cold, the ignition on: 032 and 055 for 20 s,
   the fault memory read and saved.
2. **The battery and the ECU stay connected** (*the owner*: it can be
   done so); the ignition off and the key out.
3. **The old plug photographed** from the wire side and from the front,
   **each wire's colour against its pin number** written down before
   anything is cut.
4. **One wire at a time**: cut the old wire about 10 cm from the plug,
   cut a repair wire in half, join it with a butt sleeve and
   heat-shrink, the joints staggered as on the probes' sockets, the
   terminal pushed into the new housing at the same pin number until
   it clicks; then the next wire. The red contact lock pressed home
   last; each wire pulled gently to check it holds.
5. **The colour of the new terminals** (gold or tin) into the chat,
   and a photograph of the new plug.
6. **Plugged onto the meter until it clicks**, the engine started, the
   fault memory read.
7. **032 and 055 for 20 s at the end of every drive for the next three
   or four days** (8f), the date and the kind of drive with each.

**8e. The new rear probe when it comes** (*the owner*, 11/11, 12/11,
24/11 and 25/11; `refuted.md` D13; **both probes' sockets renewed
25–26/11 night**, `idle-log.md`). **A new rear probe, Bosch `0 258 010 032`, bought
24/11 from another shop, expected 26/11, not come by 27/11, now expected 28/11** (*the owner*, 25/11 and 27/11); the butt
sleeves bought at GME 25/11; the old rear probe on the car
until then. 032
and 055 read before it goes in (8f). It
is fitted as the first was: Bosch's paste on the thread only, nothing
in the connector, the lead clear of the exhaust and not pressed into
the harness box. Then, cold, the ignition off, from below:

- **The rear probe's lead, all the way to its connector**: where it
  runs, whether it touches or lies within a finger's width of the
  exhaust or the converter, any melted, shiny or hardened
  insulation. **Photographs** of the run and of anything found.
- **If P0137 comes back after**, cold and the ignition off: the
  connector off and **the signal wire from the harness-side socket to
  the ECU's pin** read for continuity and for a leak to earth, the
  lead flexed by the exhaust. Nothing measured with the engine
  running, nobody under the car with it on.
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

**Idle solved → stop and record** (`open.md` S3, *When S3 closes*;
S1 closes with it since 26/11 night, *When S1 closes*). Otherwise each item decides whether the next is
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
and 014 itself, the closing mark (`open.md`, *When S3 closes*; S1
closes with S3 since 26/11 night). **3 at its floor with no swell through ten
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
new probe itself. Cold, so it can be touched.

**8e's new probe, and its harness with it** (*the owner*, 24/11 and 25/11): the
warranty claim for the failed new rear probe was refused 24/11 (no
company registration number for a professional fitting); the same part
was then bought elsewhere at about half the price. The old rear probe
has read healthy since it was refitted 12/11 — no P0137, never zero
outside the overrun — and its sinking at long warm stops is the one
sign against it (`refuted.md` D13). The rear probe has no direct hand
in the idle's mixture, so fitting it before 8q does not blur the belt's
before-and-after; 032 read before and after (8f) shows any shift its
trim makes. **The sockets** were renewed before it, 25–26/11 night, with the old
rear probe on (*the owner*), so that the probe and the sockets do not
change together: 8ac and 8ad read the wiring alone (26/11; nothing
moved, `refuted.md` C31), the new probe its own part after — and H11,
both probes shifted, is read again after it (*the owner*, 26/11).

**S12's jerk by the clock**: the bus cannot show a jerk at a crawl, so only its time
lets a capture or a VCDS log be read at that moment — the stroke, the
load, 014, and from a capture the cylinder (`open.md` S12).

**S12's hopping at a light pedal by the clock** (`open.md` S12 and
*Off idle*, F): off idle the scatter from stroke to stroke is the same
on all four and largest at a light pedal, so a time when it is felt
lets a capture be read at that moment against the probe's swing.

**8e's route of the harness** (*the owner*, 10/11 night: the
connectors are very likely sound and the leads well tucked in, so he
follows the harness instead): a leak or a poor earth is as likely
anywhere on the way as at a connector, and an earth eyelet the
probes' returns share is the shared earth of `refuted.md` C26.

**The probes' sockets, renewed 25–26/11** (`refuted.md` C31; the
wires to the ECU kept for 6n): the swap of 10/11 changed the probes and
their own plugs, not the harness side, so a fault there survives it —
S19's idle cell perhaps; renewed terminals take the harness side's
contacts out of it (25/11). **At the end** (*the owner*, 11/11): the rear
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

**8af, the supply branch** (`open.md` S25, H22; `idle-log.md`, 27/11
evening). **8ab ended on 27/11 with its 2c**: by its rule (004 more
than 0.2 V under fuses 10 and 29, or the gap growing 0.2 V with the
loads) the earth point needed no dashboard off, and nothing was reset;
its rings and their reasoning — the three points, why the engine runs,
the two forms by which an earth enters 032's idle cell — are in
`git show 083fdc9:docs/engine-health/plan.md`, *8ab*. **What 2c found**:
with every consumer on, fuses 10 and 29 (the ECU's) 0.3–0.4 V under
fuse 32 (the injectors', from J17), the lights the most of it; 004
about 0.5 V under fuse 32 against about 0.1 V with a seat heater only.
**The fuse holder on the battery is not it**: 20–40 mV from the
battery's post to every output, under full load (*the owner*, 27/11).
So the loss lies after the holder, in a feed the ECU's fuses share
with the lights and fuse 32 does not — the cable to the central
electrics and its contact there, the X-contact relief relay J59 that
feeds the light switch (a forum report), or the ignition switch
(*reasoned*; the wiring diagram not read). **The map** names which:
fuses that sag with 10 and 29 share their feed (fuse 12 stands for the
constant supply, 25 and 26 for the X-contact's loads, 20 and 21 for
the light switch's output, *as the card lists them*). **The earth**
enters only between the fuses and 004, 0.1–0.2 V under full load once
004's own offset (0.09–0.11 V with the ignition on) is taken off, and
grew by about 0.1 V with the loads; the lights' current returns through
the body and the battery's strap, which the ECU's earth shares, so the
body's own reading (2) comes before the dashboard. **The owner expects
the engine bay's earths to be bad** (no undertray for ten years). **Not
ohms**: a meter's ohm range on a connected car reads through every load
and its capacitors (27/11: 23 Ω and a reading creeping up from zero,
where a starter's current through 23 Ω would leave nothing to turn it);
a bad joint is milliohms, below a multimeter, so it is read as a drop
under current. **The flicker** (5; `open.md` H22, *the common part*): a
multimeter and VCDS average over a fraction of a second or more, so a
joint that flickers faster reads steady on both; the analyser reads
the difference itself, under 1 V, inside its ±10 V without a divider,
at 0.08 V a step — coarse, but a flicker of a tenth of a volt shows,
and 0.19 s snippets at kilohertz rates see the alternator's ripple
and a joint's chatter. GND on the positive side puts the laptop's
ground at +12 V, hence nothing else on the laptop: VCDS's and the
USBtin's cables join the laptop's ground to the car's minus, which
would short the battery through the laptop (*general*). The input's
absolute limit is not documented, so it is not tried. **The resistors** (*reasoned*): both leads sit
on the positive side with no fuse before them, so a bare end on the
body would put the battery's current through a Dupont wire; 10 kΩ
holds that to about 1.4 mA, and with the laptop floating almost no
current flows in either lead, so against an input of perhaps 1 MΩ
(*not documented*) they cost about a per cent of a 0.3 V difference,
a few millivolts against a step of 78. **What size and speed would
matter** (*reasoned*, *general* figures, 27/11 at the owner's
question): an injector opens later by roughly 0.1 ms per volt, so a dip
of 0.25 V while it opens costs that one pulse about 1 % of its fuel;
near stoichiometric the work hardly answers to a per cent of fuel, so
the common part's per-stroke scatter would need dips of perhaps half a
volt to a volt, different from pulse to pulse — from about 10 Hz (one
injector fires every 150 ms at idle, the four every 37 ms) to
kilohertz; slower moves the mixture, not stroke against stroke. That
acts directly only on the injectors' feed (fuse 32); the ECU's own
reading of its supply is usually filtered (*general*, not known for
M5.9.2), so a flicker there mostly averages to S19's offset. The
alternator's ripple at idle is of the order of a kilohertz and a few
tenths of a volt (*general*), averaged in part over an opening; a
failing diode raises it (S25, 8q's refurbishment). At 78 mV a step the
analyser sees 0.25 V; a regular wave is the alternator, irregular
jumps a joint. **What fuse against fuse cannot see** (the owner's
choice, 27/11): a flicker both fuses share cancels in the difference —
the alternator's ripple, and anything on the injectors' feed that the
ECU's feed carries too; what it shows is the flicker of the branch
the ECU's fuses do not share with fuse 32, the one 2c found.

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

**The alternator at the same visit** (*the owner's decision*, 27/11):
on 26/9 it gave 12.72 V at idle with the headlights, the rear window
heater and the blower on, and 13.4 V at 2,000–3,000 rpm
(`vehicle-history.md`) — low for a 14 V machine at idle under load
(*general*), and it is most likely the original of 1999. It bears on
the idle only through the supply and the load it puts on the crank
(*reasoned*): the supply's side is H4's, much weakened (the idle is
calmer with the loads on, at a lower coil supply); a regulator that
holds the voltage more steadily changes the torque it takes at idle,
which the common part could show. **What it costs**: the belt's
before-and-after (the common part, 3's floor and swells, against
`54`'s stop) now reads the belt and the alternator together; the
charging measured before and after separates the voltage, not the
torque it takes, so a step in the common part after 7/12 cannot be
given to the belt alone (*reasoned*). Accepted by the owner: the
alternator is due either way. **The measurement with every consumer
on, and the MFD beside it, is S25's** (`open.md`): the MFD showed 12.1 V
at idle with more consumers on (*the owner*, 27/11), lower than any
load was ever measured at, and its feed loses about 0.4 V under a
large load, so the battery's own figure is what closes S25 or keeps it.

**The ripple** (S25; *general*): the alternator's three phases are
rectified by diodes into a toothed voltage the battery smooths; at
idle its frequency is of the order of 1–1.5 kHz (about six pole pairs,
the alternator turning some 2.5–3 times the crank). A sound machine
leaves about a tenth of a volt; **a failed diode drops a phase**, the
ripple rises towards half a volt or a volt and the output falls —
which would fit S25 too. A workshop's rule of thumb: up to about
0.1 V AC sound, about 0.5 V and more the diodes. A multimeter's V~
blocks the DC and shows the rest as RMS, but a cheap one is specified
to a few hundred hertz and not true-RMS, so it reads the kilohertz
ripple low and roughly — **the same meter before and after** is the
reading, not its figure. What the ripple would do: about a cycle and a
half falls in an injector's opening of about a millisecond, a
different part of it for each pulse, so pulse against pulse — a tenth
of a volt is a tenth of a per cent of fuel, a volt perhaps one
(*reasoned*). A regulator or brushes that hunt act slower (hertz):
the mixture and the alternator's drag on the crank sway over several
strokes, not stroke against stroke (*reasoned*).

**The squeal at the same visit** (S26; *general*, *reasoned*): a
squeal that follows a load switched on is most often the ribbed belt
slipping as the torque it carries steps up — the compressor's clutch
engaging, or the alternator's field raised for the lights or the
blower; that it comes with the A/C but not only with it points at what
both have in common, the belt and the alternator. The belt comes off
for the timing belt anyway and the alternator goes to the refurbisher,
and the water pump (*the owner*'s other candidate, 28/11) is renewed
with the timing belt, so the visit reaches every candidate but the
compressor and the steering pump, which are only turned by hand.
**What it costs**: a squeal gone after 7/12 is not given to one part
if the belt, the pump and the alternator's bearings were all renewed;
**the owner expects it gone** and S26 stays open if it is not, the
compressor, the steering pump and the ribbed belt's tensioner then
what is left. The clock times
before the garage set it against the A/C and the lights on the bus
(`open.md` S26).

**Why the flywheel or the piston, not the pulley** (the fourth
research, 17/11; `open.md`, *What the forums say*, searched again
17/11): VW sets the crank by the damper's mark against the bottom belt
guard and checks it by the flywheel's mark; the damper's outer ring can
slip on its rubber, so the notch alone could carry 8i's error into the
mechanic's count.

**6r, the scope** (the fourth research, 17/11; `open.md` H4 and the
row A2): G28 against G40 puts the cam's phase on the crank's wheel with
no marks read, so a tooth shows as 13.85° between before and after the
belt; no trace of a healthy AQY was found, so it is read before against
after. **Injectors 3 and 4 dropped** (*the owner's decision*, 26/11
night, at the engine): contact 2 sits towards the middle and on 2 and 3
cannot be reached at all with the upper intake on, only on 1 and 4,
which he judges brings nothing; taking the intake off to lead a wire
out and seal it again is not worth the small chance of a finding.
Back-probing 3's wire at the ECU's connector was mentioned to him and
not taken up. What it would have read — a late opening or a higher
on-voltage through a raised resistance in 3's control wire, which an
output stage of the usual kind does not diagnose — is left to 6n's
ohms at rest (`open.md` H4). *This test stood first in 6r from 17/11
until then.*
**The LHT00SU1 and its divider** (*the owner*, 26/11 night; the sigrok
wiki, *Noname LHT00SU1*: supported by fx2lafw, eight digital channels
and one analog, ±10 V, the second analog input not selectable): its
inputs take ±10 V and 0–5.3 V, and an inductive sender's output grows
with speed (*general*), so the divider stays. A0 reads ±10 V in eight
bits, a step of 0.078 V, about 0.86 V at the car through the divider;
there is no range to choose. The ratio is measured, not assumed,
because the analyser's own input resistance is not documented and
loads the divider: on the desk, the analyser's 5V pin as the source,
A0 straight on 4.773 V (multimeter) read 4.800 V, the whole chain at
4.853 V in read 0.548 V against 0.105 V with the input on earth —
10.94; the zero read 0.089 V a few minutes later, so it moves and is
read at each session. Single-sample glitches near 9 V, about one in
10⁵, go to a three-sample median. `sigrok-cli` 0.7.2 (libsigrok 0.5.2)
stops after about 0.19 s at any sample rate, so `injscope.py` takes a
series of 0.19 s snippets, about 2.3 s apart with start-up (40 in
about 90 s). The laptop runs on its battery so that the analyser's
earth, which is the laptop's through USB, meets the car's at one point
only. **An exception to `CLAUDE.md`'s laptop rule** (*the owner*, 26/11
night: that rule is for the CAN and VCDS sessions in the car): the
scope's laptop session set up and built its tools there, and committed
them for the cloud session to read. The battery's calibration in the
car was not done on 26/11.

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
much that cleans is not known). What it costs little: October's two tanks were
not revved throughout either — much of the first on the motorway (*the
owner*, 18/11 evening) — so the comparison with them is about as like
for like as before; the reading against `44`–`54` by kind of stop stands.
*This said October's tanks were driven briskly until the owner's
correction the same evening.*
Read against the stops of the same kind on `44`–`54`, not against one
(*the owner's point*, 17/11: the time on the floor runs 8–81 % by
capture, 28 % pooled over `44`–`54` and 10 % over `19`–`43`; after a
brisk drive `49` 81 %, `44` 58 %, `51` 41 %, `54` 34 %; after a gentle
one or a queue `50` 8 %, `52` 14 %): the time on the floor, its level,
the swells' depth and share. **Only a change past that spread counts**
— the floor above about 80 % at more than one stop, or the swells
clearly shallower and rarer. If it moves nothing,
the oil's side (an EPR flush with the next oil change) is what is left
of that week. **Read on them too, since 26/11** (`open.md` S1, *The
long view of 1 and 4*): 1 less 4 at the warm stops, back at the level
of before the VW leads from some time between 17/11 and 22/11, within
the two cans; it fading as the treated tank runs out would point at
the cleaner. `55` (26/11, about 15 l left in the tank) already reads
the swells' depth at the shallow end (−17 to −19) and their share at
12 %, inside the spread, so it counts as neither yet.

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

**8ae, the air mass meter's plug** (*the owner*, 26/11): the meter's
renewal on 24/9 is one of the two repairs that ever moved the idle
(`open.md` S1), and its plug was found with its contact lock broken and
pieces of it inside (15–16/11, `refuted.md` C27); the contacts were
measured then only without current (0.2–0.5 Ω, the leads' own), so a
contact resistance under the meter's own current, which C27's plug form
needs, is not excluded. **A renewed plug takes it out.** What it can
move is 032's idle cell (S19) — an offset on the meter's signal reads
as more air at idle's small flow — not cylinder 3 (*reasoned*: one
meter for all four). **Kept apart from other changes**: with the battery and the
ECU connected the adaptations are not reset, so a step in 032 after it
is the plug's, against the 032 read before it. **One wire at a
time** so that no two pins swap; the meter's pins are gold-plated, so
the new terminals' plating is recorded — on the rear probe's old socket the
gold-coloured contacts were clean and the tin-coloured ones corroded
(`vehicle-history.md`, its photographs), and tin against gold is a
pairing that corrodes (*general*), which matters over years, not for
this reading. **The reading**: 032's idle cell nearer zero and staying
there over the days after it revives C27's plug form; as before
leaves the plug out.

**8w, the cylinder 4 knock window** (`open.md` S4, S5, H5): the ECU
books anything at cylinder 4's crank angle to cylinder 4 — G66 loose
or its contact poor, a part buzzing in a speed band, an arc at a
plug's end — and S5's excess shows in neutral with no combustion, so
it is not knock. G66's bolt because a knock sensor reads by its
contact with the block and VW gives it a torque. **026 in neutral and
020 on the pulls were read on 8ad** (26/11, `open.md` S4 and S5): 026
as before; at the limiter 4 half as often as on 12/11 and 17/11 and 2
as often as 4. **The loose part may be S17's resonance** (*the owner*,
27/11: always there over a wide band, on the exhaust, not the joint
behind the converter; metal knocking on metal when he moved the
exhaust by hand under the car, 25–26/11, the flex behind the manifold
suspected): placing it tells whether it is the source of S5's excess,
which on 26/11 stood out most against 1 at 2,000–2,700 rpm, and a
broken flex would also be H2's second zone (`open.md` S17). A sweep up
to 3,500 rpm because the band is wide. At a garage because the sweep
needs a second person and the flex is best seen on a lift; **at 8q's
visit** (*the owner*, 27/11) because the car is there and lifted
anyway. S14 goes with it: the owner holds S14's slow puffing on engine
braking and S17's knock to be perhaps one part, and both perhaps S5's
source (*owner*; a guess, as he says) — a part found and fixed there
is read against S5's 026 in neutral and S14's sound after.

**8w, 4's spells at a warm stop** (*the owner*, 25/11): four times
since 22/11 — 22/11 night, 23/11 afternoon, 24–25/11 night, 25/11
midday (`open.md` S1's table) — 4 has led the weakness at a warm stop
after a long or brisk drive, to −12 or −13 % with 3 on its floor.
**Kept a note, not a symptom, and not S4's** until measured (*the
owner's decision*): that the ECU retards 4 at idle too is a theory.
**The reading**: 020 showing retard on 4 during its spells puts them
under S4 (and 8w's G66 first); no retard on 4 while it is the weakest
leaves them with S1 and S3. **And whether 4 always did it** (*the
owner*): with 3's swells shorter and shallower lately, a weakness of
4's that was always there may only show more; Claude reads 4's spells
after a drive in the old captures (`cylscan.py --minutes`) against
the new ones before calling it new. **8ad, 26/11** (`55`): 4 led one
minute of the petrol station's 29 with 020 at zero, and five of the
first eight at the house, where 020 was not logged (001 003 instead) —
so the spells' 020 is still not read; hence the item stays. **Read 25/11** (`cylscan.py
--minutes` on `19`–`54`; a minute counted where 4 is the weakest of
the four and at −5 % or under): **6 of about 410 warm minutes**, and
only in `19` (the old MAF, 4 to −16 %, ahead of 3's −10 to −12) clearly
ahead of 3; in `32`, `46` and `53` level with 3 within half a point.
**The reference** (*the owner*, 25/11): the display's bytes and
`cylscan`'s deviations are against **the four's mean, 3 included**, and
nothing measures a cylinder's own torque; a shallower 3 lifts the mean
and pushes the other three down with it. Read against **the mean of 1
and 2 alone**, which 3 does not move: 4's warm minutes in the captures
reach **−29 / −24 % on 24/9** (`19`, `24`), −17 to −24 % to 21/10, and
**since the VW leads −21.5 % at most** (`53`; `46` −19.0, `47` −17.9).
25/11 midday on the display: **−21.8 %** (4 −12.0 against 1 +4.0 and
2 +15.5) — at the deepest edge of the captures since 21/10, not beyond
it; 25/11 morning −8.5. *This said until the owner's objection that 4
read deeper on the display than in any capture since 21/10, on the
four's mean.* **So the old captures do not say 4 has got weaker**: what
is new is how often 4 leads 3, and that fits 3's shallower floor and
swells (*the owner's reading*); even against 1 and 2 it stays relative
— 1 and 2 stronger reads the same as 4 weaker. 020 at the stop is the
one measurement that is not relative to the other cylinders.

**Item 9's garage session** (*agreed with the owner*, 11/11): everything that needs the upper intake off in one
visit, warm. **Cylinder 3's leak-down twice, two crank turns apart**,
because a flake under the exhaust seat (SAE 2000-01-2858: trapped by
chance) moves between readings where a worn seat does not; **a warm
compression test** straight after, because a tappet stuck pumped up
holds its valve a hair open and only shows there or in the leak-down;
**VW's tappet check** (the 2-valve 2.0's procedure: a wedge and a
0.2 mm feeler) because it finds a tappet gone soft, and VW calls a
cold-start clatter like 8/11's normal, so only the check says more.
The engine cools while the intake comes off — **at least half an hour
on this engine** before plug 3 is out and the tester in (*the owner*,
18/11; 1 and 4 are reached sooner, and are no use alone) — so **a tight
3 there does not clear a seat that leaks hot** (`open.md` S1, *The
rough start of a warm stop*), and **a leak-down hot, or one after a hard
drive against one after a gentle drive, cannot be made**: what tells a
seat that leaks hot from a deposit that soaks fuel has to come from
outside the cylinder (the stethoscope, the capture).

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
  it alone, and since 26/11 night S1 with S3 (`open.md`, *When S1
  closes*, *When S3 closes*); *until then S1 on it and with every load
  off besides, probably with the overrun too (*owner*, 28/10)*.
- **The fault memory** (*owner*, 18/10/2026): every session starts from
  an empty memory, and the saved file keeps what the session stored.
  **A code before a logged drive pauses it** (*the owner*, 11/11/2026): every
  drive starts from a clean engine. The clear resets 032 (`open.md` S3,
  *The clearing of 24/10*), so 032 and 055 are read first — a running
  log of them counts — and 8f's three drives count from the clear.
  Only when VCDS is connected anyway (*owner*, 24/10/2026): a plain
  drive is not worth a laptop, and a lit or flashing lamp is the
  backstop for what it would have caught.
