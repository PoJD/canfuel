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
Captures only where an item asks for one. **Current: item 6 and 6i;
5a on 3/11.**

5a. **The original map written back** at the tuner, **booked for 3/11**.
   The files come on the day, not before. When it goes ahead:
   - **Before the map goes back**: the cluster's trip, `TripDist`,
     `FuelAvg`, the odometer, photographed.
   - **Ask the tuner**: did he warn in 2018 that the idle could get
     worse; did the remap change the MAF's scaling, the idle advance or
     the idle speed. His answers into the chat.
   - **At the tuner, before he writes**: ask for each file as the
     **whole flash**, not only the maps — **the original** he read before
     the remap, **his remapped version**, and if he will, **a read of the
     ECU as it is now**. Write down the software version off his tool.
     Not the EEPROM. Upload them into the chat. The ECU comes out of the
     car.
   - **The drive home, captured, not with the MFD.** Capture started
     **before the first start** at the tuner, running to engine off at
     home; VCDS on **014, 055, 003** the whole way; no `oilwatch.py`.
     **A few minutes of cold idle straight after the start**; once warm,
     drive briskly; **once the oil is above 90 °C, three or four stops
     of 3–5 minutes each** — **only if the dips and 014 look different
     from now; decided together on the drive** — the everyday state,
     nothing touched, normal driving between them; **one more stop at
     home**. Write each stop into the chat.
   - **Then one or two ordinary warm drives**, captured; VCDS on
     **014, 003**; 055 once at the end, warm idle. On one of them **one
     held full-throttle pull in 4th**, with VCDS on **014, 003, 020** for
     that drive.
   - **On one of these drives, two or three stops with a cut**, oil
     95–100 °C, neutral, handbrake on, loads off: **injector 1's
     connector off for 30 s** (injector 4 if 1 cannot be reached), by the
     connector body with the clip pressed, gloves; back on. **Then at
     least 3 minutes of idle, nothing touched** — no throttle, steering
     or loads. Write each off and on into the chat. A flashing lamp is
     expected; clear the fault memory after the drive.
6. **Drive normally with the MFD in**; brisk driving once warm is
   welcome. At a warm stop that comes anyway, `IdleHealth` in the
   everyday state and the oil temperature, written into the chat.
   - **No captures for now.** Only **once `IdleHealth` on the MFD is
     clearly better**: one or two warm drives captured, on different
     days. Claude runs the capture; VCDS on **014, 003, 020**; 055 once
     at the end, warm idle. Write the stops.
6i. **The oil level on the new oil, about every 500 km** from the first
   reading (27/10, 155,024 km, at the top mark): the car on level ground
   and **at least 5 minutes standing**, the dipstick out, wiped, in, out,
   and **photographed**; the odometer into the chat. Any top-up: the litres and the odometer
   into the chat.
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
8. **The next repair** — Claude picks it from `open.md` then.

## Standing items

- **Every drive, for the converter:**
  - Drive off within half a minute of starting; never warm it up
    standing.
  - Standing at idle: **lights, blower and rear window heater on**, the
    seat heaters too. Or a touch of throttle.
  - At a stop longer than a minute or two, where safe: engine off.
  - After a hard or long drive: switch off on arrival, no idling.
  - **Engine lamp flashing**: ease off at once, stop where safe, engine
    off, write it into the chat.
- **`IdleHealth` only in the everyday state** — **blower on 1, one seat
  heater on 1, the lights on** — at warm stops that come anyway (oil
  95–100 °C, neutral, no throttle), with the oil temperature; any other
  state is named. **Idling is kept short**: no stop is made or lengthened
  to read it.
- **The fault memory after every session with VCDS connected**: read,
  saved, then cleared by the owner by hand. Not after a plain drive.

---

# Part 2 — why, and how it is read

## The rule — the owner's decision, 27/9/2026, amended 18/10/2026

**The idle comes first**: the unsettled idle (S1) and the misfires 014
counts at idle (S3). **S18, cylinder 3 dropping out with a tick, came
first beside it** from 18/10 until it closed on 24/10, after a week
without it (`refuted.md` D10); the owner keeps its drive rules as a
habit until the map goes back, so that a return is caught (they left
Part 1 on 26/10 at his request: not a step, what he does anyway). So:

- **Fix, then look.** Each step is a repair; the only readings taken are
  the ones that decide the next step.
- **No test for its own sake**, and nothing unrelated to the idle is
  pursued until it is solved — unless it could be related.
- **Run the engine as little as possible, above all not at idle.** The
  misfires are an idle phenomenon and the old converter already paid for
  them once. Warm the engine by driving.

`open.md`'s tests are reference, **not a to-do list**.
**The cylinder 4 knock window stays out of this plan** (*owner's
decision, 9/10/2026*): G66 and the rest of H5's tests stay in `open.md`.
Where the work stands is in `idle-log.md` and `open.md`, *Where it
stands*.

## Step 3 — why, and how it is read

**Idle solved → stop and record** (`open.md` S1, *When S1 closes*; S3,
*When S3 closes*). Otherwise each item decides whether the next is
needed.

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

**Item 5a — the original map** (*owner's decision*, 12/10/2026, to take
the remap out of the idle question; `open.md` H14, *The remap*).
**The four figures before it**: the OMV tank of 29/10 is on the map until
then, and read on the day they split the tank at the line, so a
consumption check never mixes two calibrations
(`docs/firmware/fuel-check.md`, *The fill of 2026-10-29*).
**The stops on the drive home** (*agreed with the owner*, 26/10, for H8):
055's learnt value moves **only at a warm standing idle** and holds
through driving (`idle-log.md`, 26/10), so after the reset it can only
walk down from zero at stops; three or four warm stops give `IdleHealth`
off the capture, second by second, against the learnt value on the way
down — the owner's hypothesis that the regulation narrows the margin
(`open.md` H8), which 26/10 had no capture for. 003 rather than 001
because the capture carries the oil, the throttle and the speed, and 003
adds what it does not: the MAF's air and the ignition angle. 10–20
minutes of idle in all, against the standing item for the converter,
accepted as an exception — **and decided on the drive** (*owner*, 29/10):
if the dips and 014 look as before, the long stops are not made.
**The questions for the tuner** (*agreed with the owner*, 28/10): the
owner half-remembers a warning about the idle (`open.md` H14), and a MAF
scaling made for the 2018 sensor is H19's mechanism; a tuner's answer
outweighs anything the web had (`open.md`, *What the forums say about
this idle*), and arrives before the diff.
**Not on 22/10 but on 3/11** (*owner*, 20/10). **The files come with the
map, not before** (*owner*, 28/10: the tuner has a busy week), so they are
compared afterwards, privately, never in this repository; the map goes
back without the diff in hand. What each differing table
*is* needs a map definition, so without one it is a guess from its shape
and is written as one.
- **The tuner's files.** The ECU is read on the bench, which gives the
  whole flash, program and calibration. **Original against remap** says
  byte for byte what was changed: idle speed, idle advance, the overrun
  cut, **misfire detection** — a detection dulled by the remap would make
  014 understate the engine on every drive (`open.md` H14 route 6).
  **The whole flash** because only the program can be disassembled, and
  it holds the torque reference behind 0x280 b7. **The read of the
  ECU as it is now** shows the remap he kept is the one in the car; the
  software version ties the original to this ECU (06A 906 018 EJ). **Not
  the EEPROM**: the immobiliser, nothing needed. **Never in the
  repository, nor on its release**: it is Bosch/VW software; only a
  summary of what changed goes in.
- **The adaptations start from zero**: the ECU comes out of the car,
  which resets them as a battery disconnect does (`refuted.md` C19).
  Fresh adaptations look better on every ruler, so the reading is the
  last of the drives, against `30`–`32`.
- **The drive home** (*owner's decision*, 18/10/2026) is C19's
  battery-off test for free. C19 says 014 stays at zero while 055 field 3
  sits above about −0.93 g/s and counts from about −0.95, by correlation
  only; so 055 is logged the whole way with 014. **014 starting as field
  3 crosses −0.95** supports C19; starting elsewhere reopens it.
  `IdleHealth` from the capture says whether the idle changes then or only
  the counter. The cold stop is the before, the stop at −0.95 sits on the
  crossing, the one at home is the after; brisk driving is what preceded
  the crossing on 4/10. Whether field 3 learns while driving is not
  known, hence a reading at each stop.
- **Map told from the cleaner and the adaptations**, on what they cannot
  move: **003's idle advance**; **the overrun fuel cut**
  by `coastscan.py`, against 0.8–1.6 s and 1,300–2,400 rpm; **014 against
  `IdleHealth`** (one moving without the other is the detection, not the
  engine); **014 under load**, new counts per `aktivováno` sample above
  1500 rpm against 15 in about 4,300 on the remap; **020 on the pull**
  (S4). A calmer idle with the advance or the cut moved points at the
  map; with both unchanged, at the cleaner or the adaptations (`open.md`
  H14 test (2)).
- **The pull in 4th** is for the converter: the torque scale was fitted
  so this car's plateau reproduces the stock ratings
  (`docs/firmware/can-decoding.md` question 8); on a stock map the pull
  says whether it holds.
- **The stop cuts** (*owner's decision*, 17/10/2026; `open.md`, *One
  cylinder or two*). The cylinder phase holds for minutes at idle, so one
  30 s cut names every dip in the idle run around it up to the moment the
  car moves (`cutscan.py --name`); each stop needs its own cut. The 3
  untouched minutes give about 20–40 named dips a stop. Since the VW leads
  the dips sit on **all four alike** (`40`, `41`); the question is
  whether that holds on the stock map — a pair coming back names the
  cylinders the remap leaves weakest. Injector 1 rather than 4
  so the suspect cylinder runs throughout. Read with `--name` per stop and
  `--shares` pooled. (`cutscan.py`'s verdict rules,
  fixed 9/10 before the first cuts, are in its source.) Never the plug lead instead of the
  connector: that sends fuel to the converter.

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
oil, `refuted.md` C21 revived; steady → neither in quantity. **A falling level is first
looked for underneath**: the sump's rear was oily on 26/10 (`open.md`,
*Other*), and a leak lowers the level exactly as burning does. Five minutes standing and
level ground because the stick reads the sump only once the oil has run
back; the photograph because a millimetre is the stick's resolution.

**Item 7 — the exhaust ahead of the front probe (H2), warm.** A leak that
draws air in at idle blows out when the outlet is closed, and hisses or
puffs; a crack in cast iron may only open hot (*general*). **Cold found
nothing on 12/10** (`idle-log.md`), so warm is what is left. Each closure shows
as a dip in engine speed, which places it in time but not in space. The sound
says only engine bay or underbody; **the photographs locate** (a leak
leaves soot), though the manifold under its heat shield cannot be seen. **Read**: soot below → that
joint; louder from the engine bay with nothing below → the manifold or
its joint to the head, the owner's standing decision of a new manifold
(3/10/2026); nothing either way → a garage with a lift. Nothing leaks
ahead of the probe → H2 refuted for its zone, into `refuted.md`.

**Item 7 — the high-voltage side** (`open.md` H4, H15): the roughest
reading on record came on a foggy morning (`open.md` S1, *Temperature*),
and the mist supplies the moisture a tracking boot or coil needs. Late
because the coil is from 6/2026 and the leads are new again; it is free.

**Item 8 — the next repair** is chosen then, from `open.md`, *The idle's
candidates, ranked*.

## Standing items — why

- **Every drive, for the converter** (all from this car's data): **122 of
  129 counted misfire events began at a standing idle** (`open.md` S3),
  so the converter's exposure is standing idle, cold warm-ups included.
  **Loads smooth it** (`open.md` S1, *Load smooths it*), and a dip is
  likelier when the charge falls (S1, *What comes before a dip*), so an
  electrical load or a little throttle at idle helps. **After a hard
  drive** 014 counted at every stop where gentle warm-ups had not
  (`open.md` S3, 4/10). **A flashing lamp** is the ECU's own
  converter-damage rate (SSP 175, `vcds.md`); this car's idle counts sit
  below even the 2 % that stores a code, so a flash means something new.
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
