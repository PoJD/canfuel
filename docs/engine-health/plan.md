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
Captures only where an item asks for one. **Next, the new N80
(in hand since 13/11, to go in about the weekend of
14–15/11)**: **no further captured drive before the swap** (*the owner*,
13/11: the captures of 12/11 and before are enough for the old valve);
**8r, the flywheel's mark through the gearbox
window**, before the garage; **8q, the timing belt at a garage, once it
has a date** (the garage chosen, a date asked for 13/11), never on the same day as the new N80; **the new rear probe's
replacement fitted when the seller sends it** (8e; the probe sent back
13/11, the old rear probe on the car meanwhile). **Then 8a, the new N80, one laptop session** (032/055 and
the fault memory before, the swap, a captured drive with 070 at a stop
on the way, 032 after; a second drive another day); **then 8o, two more captured drives with N80's hose
shut**. **6p's second half, the phone above cylinder 3, at the next
captured stop that swells.** **6m for injector 3, at the next evening
with the upper intake off** (agreed 12/11 night), ahead of item 9; then item 9; 8h at a
laptop session; **8e's harness at the end**, 8g dropped (*the owner*,
10/11 and 11/11; `open.md` H11, *The relearn drive*; `refuted.md` D13;
S1, *The rough start of a warm stop*). *Done: 8j and its first drive
11/11, item 6's first captured drive 12/11 (`49`), 6q the queue drive
12/11 evening (`50`), 6p's tailpipe half at its stop, 8i the belt's
marks 13/11 morning.*

6. **Drive normally; the MFD out from 12/11** (*the owner*), so the
   drives can be captured — the converter goes with the MFD, so no
   `IdleHealth` on the display meanwhile; Claude gives it from the
   capture (`livewatch.py`). Brisk driving once warm is welcome.
   - **Captures** (*the first done 12/11*, `49`): **as many drives as
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
6p. **The phone above cylinder 3 through a swell** (agreed 12/11
   evening; the tailpipe half done 12/11 at `50`'s stop), at a captured
   warm stop where Claude says 3 is swelling: the car in neutral, the
   parking brake on, **the bonnet open**. **Start the phone's
   recording, then shut the driver's door once, firmly** — the door is
   on the bus and on the recording, and sets the two against each
   other. **The phone lying on the cam cover above cylinder 3**, clear
   of the belt side; left there until Claude says 3 has fallen back and
   two minutes more. **One recording, not stopped and restarted.** No
   throttle, no A/C, no switch touched meanwhile. The file into the
   chat.
6i. **The oil level on the new oil, about every 500 km** from the first
   reading (27/10, 155,024 km, at the top mark; 5/11, 155,546 km, 0.5–1 mm
   under it; 11/11 evening, about another 0.5–1 mm lower, the album
   20:51; **next about 156,400 km**): the car on level ground
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
   with the upper intake off — **at the owner's next evening with the
   upper intake off, not waiting for item 9's garage session** (agreed
   12/11 night; *"in item 9's garage session" until then*); **injector
   3's circuit is the one to watch and to flex**; with the intake off,
   **photograph runner 3's joint to the lower manifold** as well (12/11; *this said
   "for 4's deficit, which the clean left", agreed 9/11 evening, until
   then*). (5/11: contact cleaner went into 4's
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
8m. **On the first hot day**: the fuel filler cap opened — a hiss or
   not, into the chat.
8j. **The canister's joints looked at and pulled on at the next wheel
   off** (the canister plumbed back 11/11 evening, `idle-log.md`): each
   rubber piece and its clip, the tank's line where it was bent; a
   photograph into the chat.
8a. **The purge valve N80, the new one, one laptop session** (*the owner*,
   13/11; the part in hand, about the weekend of 14–15/11): Bosch
   `0 280 142 353`, VW `1C0 906 517 A`, the same as the one on the car;
   the hoses stay. Claude runs the laptop as in item 6 (he clicks
   nothing but 070). In this order:
   1. **The owner reads 032/055 for 20 s and the fault memory** with
      VCDS, the old valve still connected; saved beside the logs.
   2. **The owner swaps the valve**; **the old one kept**. While it is
      out: **a photograph of its two hoses to where they join** (the T
      at the throttle) and of the vacuum hose of the secondary-air valve
      N112 to where it joins.
   3. **Claude starts the capture and the VCDS log** (014 and 001; the
      third group Claude's choice on the day), before the ignition.
   4. **The owner drives.**
   5. **Claude says in the chat when 070 can run**: coolant over 80 °C,
      001 field 4 at `111111` (the gate for every basic setting), the
      A/C off (from the bus).
   6. **The owner parks somewhere and says so**, the engine idling,
      the A/C off, no throttle.
   7. **Claude stops the VCDS log; the capture runs on.**
   8. **The owner runs basic setting 070** to its verdict (`TEV OK` /
      `TEV ne OK`), photographs it, says the verdict and closes it;
      **then again, up to three runs, a minute or two of plain idle
      between** (*the owner*, 13/11), the phone filming VCDS's screen
      through each run, and **"start" / "konec 070" into the chat** at
      each run's start and end.
   9. **Claude starts the VCDS log again.**
   10. **The owner drives on**, gentle or brisk as it comes (Claude
       reads which from the capture); "konec" ends it as in item 6:
       032/055 for 20 s and the fault memory after.
   - **The second drive on the new valve** another day, the other kind
     of the two (gentle or brisk), captured, 032 after (8f).
   - **At any engine lamp from now on**: the odometer, the tank's needle
     and the outside temperature into the chat, and 032 read before the
     code is cleared.
8o. **Two captured drives with N80's hose shut** (agreed 12/11
   evening), **only after 8a's gentle and brisk drives are read**.
   Engine off and cold: **the rubber hose between N80 and the T at the
   throttle pinched shut with a hose clamp** (a plastic line is never
   pinched: there the hose is pulled off N80 and both open ends
   plugged); a photograph of it. Then item 6's drive, captured, to a
   warm stop of ten minutes or more, twice, on different days. After
   each: the fault memory (a purge code is expected and is said as
   such), **032 read but not counted for 8f**. After the second: the
   clamp off, the hose looked at where it was pinched, the fault memory
   cleared by the owner, and 032's next reading taken as a fresh start.
8r. **The flywheel's mark through the gearbox window** (*the owner*,
   13/11: before the garage, to be sure), at a cold engine, the key out:
   the window's plug out; the crank turned by its pulley's bolt, **only
   in the direction of rotation** (clockwise from the belt side; past
   the mark, round again twice, never back), **both marks watched in
   turn while closing in**, until **the flywheel's mark stands on the
   window's pointer** (*the owner*, 13/11: set by the flywheel, so the
   cam's error reads in teeth) — on the turn where the camshaft
   sprocket's OT mark is near its own mark, not half a turn away (that
   is TDC of 4: once more round). Then **the camshaft sprocket's mark
   against its mark**: a photograph of each square on, and if apart,
   **the sprocket's teeth between them counted** and which way. Nothing
   loosened; the plug back in. **The crank pulley's diameter measured**,
   to a centimetre or so (the gap between 8i's marks not measured: it
   cannot be reached without taking parts off, *the owner*, 13/11).
   Into the chat.
8q. **The timing belt renewed at a garage** (*the owner's decision*,
   13/11; the garage chosen by the owner, a date asked for 13/11): the belt, its tensioner and idler, and the water pump.
   **Before the old belt is loosened**, the mechanic sets the crank to
   TDC of cylinder 1 and says how many teeth the camshaft sprocket's
   mark is off its mark, which way, and photographs both marks; the
   answer into the chat. Before the garage: a captured drive to a warm
   stop with 014, 032/055 and the fault memory read. After it: the
   fault memory read, 032/055 for 20 s, and a captured drive to a warm
   stop of ten minutes. **Not on the same day as the new N80 (8a)**: a
   captured drive between the two.
8f. **032 for 20 s at every session with VCDS connected**, until both
   cells have held for three drives; **and 036 for a minute** at a warm
   idle and on the road when VCDS is on anyway (the rear probe watched
   now and then, *the owner*, 11/11). **032 read first, before any code
   is cleared**; **on a logged drive, 001 in place of 055** (G62's
   reading: S24 closed 12/11, reopened if its dither comes back; on a
   captured drive the capture reads it, 001 not needed) **and 014 always** (P0303 stored on 12/11 with no cut:
   its time is what the log gives).
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
     - **6m's injector circuits** while the intake is off, if not done
       before (12/11 night);
     - **the lower manifold's gasket**: renewed if the garage takes
       the lower manifold off as well (the tear at runner 4; **runner
       3's joint is the one the idle points at**, 12/11).
   - With VCDS connected anyway after a stored P030x: **a generic
     OBD-II read** (modes 02 and 06), read only, saved.
   - **No head off** (*the owner*, 4/11, leaning, not final): if the
     leak-down names 3's exhaust seat, the car is driven as it is and S1
     most likely closed as *acceptable, cause known*.

8e. **The probe now, the harness at the end** (*the owner*, 11/11 and
   12/11; S23 closed 12/11 as the new probe's fault, `refuted.md` D13).
   **The new rear
   probe went back to the seller under warranty, 13/11; a new one in its place
   when it comes** (*the owner*, 12/11: the old one, refitted, read healthy
   with no P0137; until then the car runs on the old rear probe). The new one
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
- **A code in the memory before a logged drive pauses it** (*the owner*,
  11/11): Claude stops the log and says the codes; the drive starts
  only after the owner has cleared them or the fault is repaired, on a
  fresh log.

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
ECU (*the owner*, 5/11): a raised resistance in the loom at 3 makes no
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
idle through the tank; the captures read where it got to. **Read**:
`tools/cylscan.py` and `--minutes` on the idles, alone and pooled since
the last repair — 3's deficit and weak strokes against the other three,
and `--vcds` with the drive's 014 log — 014's rises by cylinder; beside
`IdleHealth` and 014 themselves, which are the closing marks (`open.md`,
*When S1 closes*, *When S3 closes*). *Until 12/11 this read the
dips' shares with `cutscan.py --shares`, removed with the count it
rested on.* 014 by stop and `IdleHealth` by oil band against `open.md`
S1 and S3. **003** says
whether anything sealed or opened; **020** is data, not a step: whether
cylinder 4's retard, nearly gone with the new leads on 10/10, stays gone
(S4).
**"Konec" and the five-minute stop** (*the owner*, 12/11 night): the
session of 12/11 evening kept him at the laptop nearly ten minutes
after the drive; from now the laptop only records and uploads, the
reading is a cloud session's (`CLAUDE.md`, *Sessions at the car*), and
the capture's last minutes home are given up for it. A queue crawls
more than it stands (`50`: no standing idle over a minute in the
queue), so a stop long enough for a swell is asked for, not waited
for.

**No captures until the display shows a change** (*owner's decision*,
23/10/2026), and **the hard run dropped** with them: it was planned because on
4/10 014 counted only at the stop after a hard drive, and that was an
adaptation completing rather than load (`refuted.md` C19).
What it costs: a capture on plain fuel just before the cleaner, the
reference its tanks would have been read against. What is left: `40`,
the refit drive of 21/10 on plain fuel, as that reference; the display
through the tanks; and the captures once `IdleHealth` moves, which then
say what moved.

**It moved on 11/11 and 12/11** (the two calm stops near home on the
canister, the MFD in; `open.md` S1, the warm stops' table), so the
captures are due. **What they settle first** (*the owner*, 12/11, the
idle split in two; `open.md`, *The idle's candidates, ranked*): **which
part fell** — `idledips.py --roughness` for the whole and
`--cylinders` for the period-4 part, set against S1's 78 and 51 (*A
steady pattern over the cylinders*; the 5/11 script that took the slot
means out was not kept, so the split is computed again on the
capture; about an eighth of the grade is the crank wheel's own
alternation, which no repair moves). The common part down and 3's
pattern as before is list A's (the belt and H0 at its head since 12/11
evening, H16 third); the pattern gone too is list
B's as well.
**Read by cylinder since 12/11** (`tools/cylscan.py --minutes`, kept;
`open.md` S1, *Every stroke named*): the part with a cylinder is **3's
deficit and 3's weak strokes** minute by minute — a floor of about −9 %
of a stroke and swells to −26 % with up to twelve weak strokes a minute
on every stop before the canister — and "4's pattern" was the crank
wheel's alternation. **3 at its floor with no swell through ten minutes
is list B's part gone; 3 swelling as before under a calm grade is list
A's.** **No injector cut in these captures**: the cut was there to name
the slots, the strongest slot names them now, and a cut is one of the
things that ends a swell, so it would spoil the reading. The stop
of 10 minutes because the settling takes 3–8.
**Read on the first, 12/11** (`49`; `open.md` S1, *The first captured
stop on the canister*): **neither part fell** — 3 swelled as before
and stepped to its floor by itself; settled, the grade and the common
part were those of the calmest floors before the canister — so **a
second captured drive now would only repeat the canister's reading**,
and the next is after **8a's new N80**, the one change left on H16's
path, read the same way against `49`.
**The MFD out and every drive captured until the swap** (*the owner*,
12/11 evening, so that there are more captures and more 014; **closed
13/11 by the owner**: no further captured drive before the swap, the
baseline is what `49`, `50` and the drives before them hold): what
the drives before the swap add is not another reading of the canister
but **the old valve's baseline for the owner's reading of H16**
(`open.md` H16, *The owner's reading, 12/11*) — 032 before and after
each drive, gentle or brisk as the capture shows, should follow the drive on the old
valve (−14.8 after the gentle morning, −7.0 after the brisk drive) and
stop following it on the new one. Each captured warm stop is read by
`cylscan.py --minutes` as `49` was, so 3's swell and floor get more
stops on both valves.

**The groups on the captured drive** (12/11, three at a time): **014**
always (8f; P0303's time, the stop's count); **020**, cylinder 4's knock
retard (`open.md` S4), last read on 3/11's pulls — since then the
hydrogen clean of 9/11, which a retard from the crust on 4's crown
would follow and an arc at lead 4's end would not; it shows only on
pulls above 3,000 rpm warm, hence the pulls; **033**, the front loop's
live regulation, which swings with the mixture it chases — H16's
mechanism (`open.md` H16, *How it would make the idle rougher*) against
the stops logged with 033 on the bypass. **001 is left out** because the
capture carries the coolant (0x288) far faster; **003** this once
too.

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
c11dc75:docs/engine-health/plan.md`, item 8). **What it showed**
(re-read 12/11 with `tools/cylscan.py`): 3's swell — its deficit
beyond its floor, its weak strokes, the rough first minutes of a warm
stop and 014's storm — was not there at stop 7, which is the H13 branch
for 3; **3's floor, about −9 %, and the settled level were kept**, and
the swell was back a day later (`47`; `open.md` S1, *The clean of
9/11*). *Until 12/11 this read "its share of the dips … gone, 4's
steady deficit kept"; "4's" was the crank wheel's alternation.* **8c, the probes read before and after both were replaced, is done**
(9/11 night and 10/11; `open.md` H11, *The reading before the swap*,
*The reading after the swap*; how it was planned and why: `git show
1040e9e:docs/engine-health/plan.md`, item 8c): the new rear probe flat
for 18 minutes of idle where the old one sank, and the idle as rough as
before.

**8d, the relearn after the battery disconnect, is done** (10/11
evening; `open.md` H11, *The relearn drive*, S23; how it was planned
and why: `git show d4aeca3:docs/engine-health/plan.md`, item 8d): 032
back to −6.3 / +6.3 % within 37 minutes on the new probes, the idle as
before, 3 with most of the weak strokes again (73 %, `cylscan.py`), and the new rear probe's signal
falling to zero under load (P0137).

**8e, the probes' tightness**: they were tightened by hand to about 50
Nm estimated, without a torque wrench (`vehicle-history.md`), and the
reading after showed the rear probe switching to the front's swing
after 18 minutes of idle and in spells at the warm stop; a probe seated
loose lets air into the exhaust at idle's pulses, the second zone of
H2 of its own making (*reasoned*). Cold, because the exhaust then is at
the temperature they were fitted at. Checked before the warm tailpipe
test (item 7), which it would otherwise confuse. **The rear probe's
lead** (`refuted.md` D13 (S23)): 0.000 V at full load is not the gas, so the
signal failed on its way to the ECU, and it came back at a cooler idle
— heat on a lead or a connector the likeliest (*reasoned*); the lead was
tidied by the owner when the probe was fitted, so its run is looked at
first, the connector second; a lead and connector found sound leave the
new probe itself (a warranty matter). Cold, so it can be touched.

**S12's jerk by the clock** (reopened 10/11 night at the owner's
request): the bus cannot show a jerk at a crawl, so only its time
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
speed and both coolant readings at 10 ms (the ECU's and the cluster's,
already tested on `47`: steady to half a bit). **What it cannot see**
(*reasoned*): VCDS samples about once a second, so a load's step is
caught but noise faster than that is not; three groups at a time, so
the sets are run one after another, the sequence repeated. Four loads
because they are the largest the driver can switch from the seat, and
none needs anyone at the engine.

**8e, no spray and no seal on the probes' connectors** (`refuted.md` D13 (S23),
*The contact spray*; the research of 11/11): Bosch, Denso and Saab
forbid contact spray and grease on a lambda probe's connector, because
the probe takes its reference air along its own lead, and a solvent
drawn in lowers its curve; it went into the rear connector on the
morning of 10/11, the day the rear probe sank. Sealing the probe's own
lead airtight could starve it the same way; the fabric tape over the
harness side is not a seal.

**6p, the phone above cylinder 3** (*agreed with the owner*, 12/11
evening; `open.md` S1, *The phone at the tailpipe through a swell and
a fall*). The tailpipe half showed 3's exhaust pulse growing with its
deficit and dropping with the fall, which a seat and a dilution both
give — the rule written for it did not separate them. **On the cam
cover the question is the valve gear's**: a once-per-cycle tick at 3's
place (S22) that grows with the swell and drops at its fall is for a
valve held off its seat or a lifter (H1); the same tick through both
leaves the swell to the charge. Read as the tailpipe's was: each firing
found on the recording by the firing line, set on the capture's strokes
by the door and then by the weak strokes themselves. One recording
because a restart costs the door's mark (12/11: the second file had to
be set by its clock).

**8o, N80's hose shut** (*agreed with the owner*, 12/11 evening;
`open.md` S1, the same section; H16): the ECU's purge is the one thing
known to run a slow ramp with a quick shut-off by the minute, the
swell's shape, and its phases are not on the bus or in any measuring
block. **Read**: a swell of 3's at either stop with the hose shut —
the purge is not the swell's cause, the weakest of its four readings
gone; no swell at two stops after brisk drives, where `43`, `44`, `47`
and `49` all swelled — for it, and the stops are repeated with the
hose open. The common part is read beside it (2.7–3.1 rpm rms at every
warm idle since 24/9): a step in it with the hose shut would be the
first thing that moved it. After 8a, because a drive with the purge
shut teaches 032 nothing about either valve.

**Item 9's leak-down on an engine switched off in a swell** (*agreed
with the owner*, 12/11 evening): straight after a fall 3 is nearly
level with the others (−1 to −5 %), so a leak-down made then tests a
seat at its tightest; the engine cools while the intake comes off as
it is, and a film on a seat may not last that either — a tight 3 there
still clears nothing, a leaking one names it.

**8r, the flywheel's mark** (*the owner*, 13/11, after reading of
others who found odd marks on the pulley; `open.md` A1, *What the
forums say*, the timing belt): Motor magazine names the camshaft
sprocket's OT and **the flywheel's mark in the gearbox window** as the
marks to set on this family; the pulley's notch and the groove read in
8i are not confirmed as the AQY's timing marks. **Set by the
flywheel** (*the owner*, 13/11, in place of the cam first): with the
crank at its true TDC, the camshaft sprocket's offset counts in its own
teeth, each one belt tooth — the figure the garage would give, read
directly, where the ring gear's teeth would have needed its tooth count
(*reasoned*). The sprocket's mark on its own mark says the belt is
right and 8i's 30–60° was the wrong marks or a misjudged angle; the
cam turns once for two of the crank, so TDC of 1 is the turn with the
cam's mark near its own, half a turn of the sprocket off on the other.
**The pulley's diameter** turns the owner's 2–3 cm at least, not over 5, on its rim
(13/11 evening) into degrees: 15–40° at 14–16 cm (*reasoned*; a
centimetre on the diameter moves it by about 7 %, far less than the
gap's own 2–5 cm), one to two teeth
— where the 30–60° by eye were 1.5–3; and if the flywheel and the cam
agree while the pulley's notch does not, the pulley sits turned on its
sprocket (*the owner*). Where the window
is and what its mark looks like was not looked up in VW's manual (the
owner found it on the web). **Turned only forward** because turning
back lets the belt's slack side jump and misreads the cam; by the
crank, never by the camshaft's bolt. **The belt is renewed either
way** (*the owner*, 13/11: "for peace of mind"); 8r settles whether
8q's tooth count is expected to find anything.

**8q, the timing belt at a garage** (*the owner's decision*, 13/11,
after 8i): 8i read the cam's OT mark set and the crank pulley's one
notch 30–60° of crank from the groove on the block by eye
(`open.md`, *Where it stands*, the row A1) — 1.5–3 teeth with the cam
advanced if those are the true marks (the direction the owner's, read
off the part), which the flat full-load pulls and the air the engine takes at full
throttle argue against (485 mg a stroke at 5,200 rpm against 496 at
2,400, 85–90 g/s at the top; the row A1); the
piston at plug 1 that would have settled it was declined. The belt
is nine years old (10/2017), so renewing it loses nothing either way,
and the owner leaves the work to a garage. **What makes it a test**:
the mechanic's count of teeth before the old belt comes off says
whether 8i's reading was true; the captured warm stop before and
after says whether the common part (list A) moved — down by a clear
step if the cam was out, unchanged if it was not (H0 then gains).
**Kept apart from the new N80** so that each has a captured drive of
its own; which comes first is the dates'. Nothing in 8i was loosened;
VW's 5 mm at the crank was for the Mk4 2.0, nothing of the AQY's own
was read.

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
3.* **6m for 4** because 4 was held to be the cylinder with a
deficit of its own, and its injector circuit the cheapest of the
three causes that act on 4 alone (H4; H3's runner gasket and H1's inlet
seat cost the intake off or a leak-down). **Brought ahead of item 9, 12/11 night** (*agreed with the
owner*): off idle 3's deficit is an amount at a small charge and not a
share (`open.md`, *Naming the cylinder*, *Off idle*), which is what an
injector opening late through a raised resistance gives, so H4 went
above H20 and its test, the cheapest that can confirm or clear a cause
of that shape, no longer waits for the garage; the photograph because
H3's joint is in reach with the same cover off. **Since 12/11 it is read for
3**: the deficit and the misfires are cylinder 3's (`open.md` S1,
*Every stroke named*; S3, *What 014 counts, by cylinder*), 4 is level
warm, and the measurement is the same six pairs and four coils with
the loom flexed at 3. **The display's stops** with a
word on what came before each, because a brisk run calms the idle by
itself for a while (`open.md` S1, *After high revs*) and the display's
spread is as large as the effect; the A/C's figure for how much load
still calms it (`open.md` S1, *Load smooths it*; *"for S1's closing mark
2" until 12/11, when the marks became cylinder 3's*). **The days after** (*reasoned*, from SAE 2000-01-2858:
water flakes deposits most): the clean burns hydrogen to water vapour,
so a flake may come loose and lodge under a seat, an 18/10-like
drop-out; if one comes, a warm leak-down on that cylinder the same day
or the next is the one moment it can be told from a seat or a guide.

**8m, the filler cap on a hot day** (from 8k): the one check of the
summer overpressure (`open.md` S21), which a November day cannot give.

**8j, the canister's joints** (`open.md` S21): rubber on a line bent
back with heat can creep off its port, and a joint that lets go is a
leak of unmetered air at every purge and P0440 again; the wheel coming
off for anything else is the free moment to look.

**Item 8a as one laptop session** (*the owner*, 13/11): Claude drives
the laptop, the owner the car and VCDS's 070. **070 is a test, not an
adaptation** (the label's verdict `TEV OK` / `TEV ne OK`, nothing
stored; unlike 060 and 098, the throttle's `ADP OK`), so the car needs
none of it; it is run for the new valve's own reading — the ECU opens
it and its fields give the duty, the lambda controller's deviation and
the flow — against which a later P0440 can be read; 27/9 kept only the
verdict. **Its gate** is 001 field 4 (the label's "basic setting
requirements": coolant over 80 °C, under 2,000 rpm, throttle closed,
lambda control in order, idle, the A/C compressor off — `111111`; the
Czech label reads "pod 80 °C", a slip of translation for over), so it
cannot run cold before the start. **The VCDS log stops** because one
VCDS holds the control unit; **the capture runs on** because the stop
is a warm idle with N80 driven open on purpose — the idle's answer to
the purge, recorded (H16). **Several runs** (*the owner*, 13/11):
each opens N80 on purpose at a warm idle, and the question is whether
cylinder 3's swell follows the openings — one run could fall on a
swell by chance, three in turn with plain idle between can be set
against it; the screen filmed for 070's field 2 (the lambda
controller's deviation, which the purge moves at once where 032 moves
slowly), the chat's start and end for the capture. *Whether the
idle's own control behaves as in plain idle while a basic setting
runs is not known for this ECU* (*general*: some VW ECUs hold the
ignition or the idle controller in basic settings), so a swell during
a run is read against the minutes between runs, not against other
days. Claude never starts a basic setting
(`CLAUDE.md`), so 070 is the owner's click.

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
−6 to −9 % with a tight new valve clears it of the standing offset. **One gentle drive and one brisk** (12/11, the owner's reading of the
four readings on the canister, `open.md` H16, *The owner's reading,
12/11*): on the leaking valve the idle cell went to −14.8 % after a
gentle drive and to −7.0 after a brisk one; on a tight one it should no
longer follow the drive.
**The photographs** because whether N112 and N80 share a vacuum tap is
not recorded. **Fitted as soon as it is in hand** (*the owner*, 11/11: the
fix comes first; 8b dropped; in hand 13/11, the swap about the weekend).
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
changed** (*superseded 11/11: the canister was looked at and found
bypassed, 8j*) — a canister that shed charcoal would have jammed a new
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
  than every load on. **The closing reads it** (*the owner*, 12/11): S3 on
  it alone, S1 on it and with every load off besides (`open.md`, *When S1
  closes*, *When S3 closes*), probably with the overrun too (*owner*, 28/10).
  *Until 12/11 both closings were read loads off only.*
- **The fault memory** (*owner*, 18/10/2026): every session starts from
  an empty memory, and the saved file keeps what the session stored.
  **A code before a logged drive pauses it** (*the owner*, 11/11/2026,
  at 8k, P0137 stored before the first drive on the canister): every
  drive starts from a clean engine. The clear resets 032 (`open.md` S3,
  *The clearing of 24/10*), so 032 and 055 are read first — a running
  log of them counts — and 8f's three drives count from the clear.
  Only when VCDS is connected anyway (*owner*, 24/10/2026): a plain
  drive is not worth a laptop, and a lit or flashing lamp is the
  backstop for what it would have caught.
- **The cover's nuts**: the gasket settles (`refuted.md` D5).
