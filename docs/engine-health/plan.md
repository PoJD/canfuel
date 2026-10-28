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
Captures only where an item asks for one. **Current: item 6 and 6a–6i;
5a on 3/11.**

5a. **The original map written back** at the tuner, **booked for 3/11**.
   The files come on the day, not before. When it goes ahead:
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
     of 3–5 minutes each**, the everyday state, nothing touched, normal
     driving between them; **one more stop at home**. Write each stop
     into the chat.
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
   welcome. At a warm stop now and
   then, the two states of the standing items, written into the chat.
   - **No captures for now.** Only **once `IdleHealth` on the MFD is
     clearly better**: one or two warm drives captured, on different
     days. Claude runs the capture; VCDS on **014, 003, 020**; 055 once
     at the end, warm idle. Write the stops.
6a. **Two tanks of BG 44K** (BG `208` *44K Platinum*, 325 ml a can).
   **The second tank is in, from 24/10** (the first ran 23–24/10).
   - **The second tank**: no refuelling until it is run down. Drive it
     as item 6. At the next fill, before the nozzle: the cluster's trip,
     `TripDist`, `FuelAvg`, the odometer; then fill to the click.
   - **On 3/11, before the map goes back**: the same four figures.
   - **Italian tune-up**: once the **oil reads 90 °C**,
     and not in the first 30 km after the pump: **the motorway at the
     limit, with full-throttle pulls** — slip roads, and 80 to 130 in
     4th — and an easy stretch after each few; a long climb whenever
     the route has one. **Oil above 120 °C: ease off** until it is
     back under 110. **A tick, a miss or the lamp, lit or flashing: ease
     off at once**.
   - The map at 3/11 goes ahead whatever tank is in.
6g. **032 on the new oil** (the *before* read 26/10: −8.6 / +7.8 %).
   - After about 200 km on the new oil: 032 and 055, before anything is
     cleared. **Before 3/11**: the map resets 032 again.
6h. **Every cold start, until S7 is placed.** Before turning the key,
   nothing else. Write into the chat: date, how long parked, the outside
   temperature, **caught and died, or ran**, and `StartCrank` and
   `StartDip` off the display. **Never primed.** A few hours parked
   outdoors in the cold counts as a cold start too.
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
- **`IdleHealth` at a warm stop, always in two states** (oil 95–100 °C,
  neutral, no throttle, nothing else touched), on every drive that reads
  it, captured or off the display:
  1. **2 minutes with every load off**, the lights too where the switch
     allows it (in the dark); whatever cannot be switched off stays on,
     and say which.
  2. **Then 2 minutes with every load on**: main beam, both seat heaters,
     the heated glass, A/C and the blower on full.

  With the laptop, Claude reads both off the capture; with the MFD in,
  write each state's reading into the chat.
- **When there is no time for the two states: the everyday state**, and
  most readings off the display will be in it — **blower on 1, one seat
  heater on 1, the lights on**, oil warm. A reading in it needs no label;
  any other state is named.
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
accepted as an exception. **6g goes first**: the map's reset would clear
the 032 it waits for.
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

**Item 6a — two tanks of BG 44K** (*owner's decision*, 18/10/2026: S18
and the idle likely one cause, deposits; *21/10–22/10*: BG 44K for two
tanks in a row instead of the Liqui Moly Pro-Line `5153` bought on 21/10,
which is kept for later; **the overlap with the map at 3/11 accepted** —
*"I mainly want it solved"*). BG's own data sheet for `208` says only that
one can treats **up to 75 l**; it publishes no chemistry, so that it is PEA
is said of it, not stated by its maker. BG names injectors, valves and the
combustion chamber, and on this port-injected engine the fuel washes the
back of the intake valves, so a fuel-borne cleaner reaches the deposits it
is meant for.

**The four figures at the second tank's ends, and on 3/11**: the
second tank is the first that the cluster's trip and the display's
both cover from a brim, so it is the first real check of `FuelAvg`
against the pump (`docs/firmware/fuel-check.md`, *The fill of
2026-10-24*); the map going back inside it would mix two calibrations
in one ratio, and the figures on the day split the tank at the line.

**The Italian tune-up** (*owner's decision*, 23/10) is Red Rider's
"indiánský způsob" for its strong tank, applied to both: heat and gas
flow through the chamber while the cleaner is in the fuel. **BG says
nothing about driving** (its sheet: add at fill-up); Red Rider calls long
distances a myth, finds mixed driving better because a standing engine
gives the cleaner time to soak, and asks for a hard throttle now and
then; no controlled study of the tune-up itself was found (23/10), only
forums and a patent's claim of deposit removal near full load. **On oil at
90 °C** (*decision*) because S18 came cold and the oil is the slower of the two to
warm; **not in the first 30 km** because the cleaner reaches the
injectors only after the fuel already in the filter and lines, 10–30 km
by Red Rider's figure. **A misfire under load costs the converter more
than one at idle** (more unburnt mixture per second into it), hence
easing off at the first sign rather than at a flashing lamp alone.
**The oil temperature** (*decision*, 23/10). No maker states a limit:
TotalEnergies' catalogue gives none for the *Quartz 9000* oils, and no VW
figure for this engine was found. What is general and agreed is that oil
oxidises about twice as fast for every 10 °C (the Arrhenius rule, AMSOIL
and others); forums put the start of real concern at a sustained 120–130 °C
and breakdown at 130–150 °C, none from a data sheet. **The owner's
recollection of 115 °C as critical was not found in any source.** So 120 °C
is chosen as the point to ease off, held only briefly: 105–110 °C on a hard
run and 111 °C for a few minutes (*owner*, 23/10) are inside it. *This said
the oil is changed straight after the second tank, so its oxidation costs
no interval*; since the flush moved ahead of the tank's end, the rest of the tank is
driven on the new oil, and brief spells under 120 °C are what a VW 502.00
oil is rated for. The reading is the instrument cluster's, on
0x420 (`docs/firmware/can-decoding.md` question 10, closed 23/10 at the
owner's decision: it reads where a warm engine's oil runs).

**Load, not revs** (*reasoned*, 23/10): what heats the chamber and the
valves is the fuel burnt per second, which is the power; on the flat at a
given speed the power is set by the drag whatever the gear, so a lower
gear adds revs and pumping losses, not heat. Power comes from speed and
from acceleration, so the motorway gives the steady part and the pulls
the peaks; the cleaner also washes the intake valves with more fuel the
higher the load. Twenty minutes of climb is not on the owner's routes,
and the pulls stand in for it.

**What the overlap costs.** The drives after 3/11 read the map and the
cleaner together, and only those before it read the cleaner alone. If the
idle improves, which of H13 and H14 did it is left open; the owner chose a
fix over the answer.

**The flush and the oil change were done 26/10** (`idle-log.md`), ahead
of the tank's end; the reasoning and the choices behind them are in
`git log`. **Later changes**: EPR at every change until the symptoms are
settled, at most once a year (*owner*, 23/10); the filter `06A 115 561 B`
(`vehicle-history.md`).

**And the second tank** (*the owner's point*, 24/10): the strong first
44K tank, hours above 4000 rpm and about 450 km left `IdleHealth` at
70–80, as before, and he expects the second to do no more. It is driven
out because the can is in, and read as the last word on H13 (`open.md`).

**Episodes on the cleaner's tanks are expected, not a verdict**: under H13
each tank sheds a layer; under H1 the tick would not depend on the tank.
For the converter it is a misfire that matters, not the cleaner — hence
easing off at one. **Read**: the display through each tank, and the captures
once `IdleHealth` moves, against `30`, `31`, `33`, `34` and `40`, on settled adaptations (the
reset at 5a makes the drives just after it read low on 014 for another
reason), and the shares pooled since the last repair. A tank is weeks of
this car's driving, so the reading is late by design.

**Item 6g — fuel in the oil** (`open.md` H17; 25/10/2026, from VW's
evaluation of block 032, `vcds.md`). VW names oil dilution first for a
low idle learnt value with part load normal, which is this car's 032,
and says it goes away with an oil change — which 6a does anyway, so the
test costs one reading either side. (The dipstick part is done: 24/10,
the level unchanged since the last top-up, `idle-log.md`.) **Read**: 032's idle
cell close to zero on the new oil → H17 confirmed and the cold idles of
the captures were feeding it — fewer and shorter standing cold idles
from then on; unchanged → H19 (the MAF against the map) or an injector carry the
trim, since 6e cleared N80 and the regulator's reference. **The first
reading on the new oil** (27/10 evening, relearnt from 0.0 after that
afternoon's disconnect): −8.6 %, already against H17. **`IdleHealth`
beside it, cold and warm apart** (the owner's loop, `open.md` H17): fuel
boils off only from hot oil, so H17 predicts the warm idle calmer and the
cold one unchanged; a calmer warm idle with 032 unmoved is EPR on the
rings (H13), not H17. EPR in the flush
(6a) does not spoil the comparison: it is drained with the old oil.

**Item 6h — the cold start** (`open.md` S7, reopened 25/10). **Plain
starts only** (*the owner's decision*, 28/10): the priming asked whether
the rail lost its pressure while standing, and three starts (26/10 plain,
bad; 27/10 primed, hesitant; 28/10 plain, clean) did not follow it, so it
has answered what it could. Plain starts now read the fuel and the
cleaner's tank running out; a few hours outdoors in the cold is the case
of 24/10. `StartCrank` and `StartDip` because the display carries them
and a start the owner calls normal may still show a long crank.

**Item 6i — the oil level on the new oil** (`open.md` H18, H17; *the
owner's agreement*, 26/10). Oil burnt past the stem seals or rings lowers
the level; fuel collecting in the oil raises it (*general*). On the old
oil neither could be read: no known starting level, and the top-ups
included the litre lost at the cover joint (3/10). A fresh fill to a
photographed level gives the start. **Read**: a level falling between
top-ups → oil burnt, H18 (or the rings) up; a level rising → fuel in the
oil, H17 up; steady → neither in quantity, or both at once (H17, *The
level may balance*), which 032 (6g) then splits. **A falling level is first
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
- **`IdleHealth` in two states** (*owner's decision*, 19/10/2026;
  `open.md` S1, *Load smooths it*): since the cleaner the partial loads
  make little difference and only everything on together calms it, so
  one state is all off and the other all on, with nothing between to
  argue about. The lights go off where the dark allows. **Two minutes
  each**: neighbouring 2-minute windows on a steady warm idle differ by
  4–18 (`24`, `26`, `28`, `30`, `32`, `37`), so one pair shows only a
  difference of about 25 or more; **pairs pool over drives**. In a
  capture the switch shows in b7, so the states need no timing in the
  chat. Four minutes standing is accepted against the converter rule
  (*owner*).
- **The everyday state** (*owner's decision*, 23/10/2026): four minutes
  and main beam at every stop do not fit his driving, so most readings
  off the display come in one fixed mild-load state. It is a third ruler,
  not either of the two: it is compared with itself, and shifts in it are
  watched without conclusions yet (*owner*). It sits between the two
  states, so it reads neither as calm as every load on nor as rough as
  every load off.
- **The fault memory** (*owner*, 18/10/2026): every session starts from
  an empty memory, and the saved file keeps what the session stored.
  Only when VCDS is connected anyway (*owner*, 24/10/2026): a plain
  drive is not worth a laptop, and a lit or flashing lamp is the
  backstop for what it would have caught.
- **The cover's nuts**: the gasket settles (`refuted.md` D5).
