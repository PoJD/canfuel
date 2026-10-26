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
Claude runs the capture on every drive. **Current: item 6.**

5. **Until the map goes back, on drives with the MFD in:** where the oil
   reaches **95–100 °C**, one stop in the two states of the standing
   items. Write into the chat: date, oil temperature, and for each state
   **where `IdleHealth` mostly sat and the lowest it touched**.
   **Also until the map goes back, on every drive (S18):**
   - Warm up gently: no high revs until the oil reads **80 °C**.
   - Warm and on four cylinders: spirited driving is fine, full throttle
     included.
   - A tick or a felt misfire: ease off, drive on gently, no high revs
     while it lasts.
   - Engine lamp on: ease off.
   - Engine lamp flashing, or running on three cylinders: stop where
     safe, **engine off, wait a few minutes**, start again. Drive on only
     if it runs on four.
   - VCDS on **014, 001, 003** whenever the laptop is in the car.
   - After a drive with VCDS connected: read the fault memory of 01,
     save it ("Uložit chyby"), then clear it.
   - After an episode (a tick or a misfire), write into the chat:
     **when** (date, time, minutes after the start), **what came before**
     (hard driving, a cold start, a long stand), **oil temperature**,
     **`IdleHealth`**.
5a. **Postponed: the original map written back** at the tuner, **booked
   for 3/11**.
   First the tuner emails both files, the original and his remap;
   upload them into the chat (never into the repository); a new date
   after they are read. When it goes ahead:
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
     drive briskly; **when 055 field 3 nears −0.95, stop for a few
     minutes of idle** (read it at a stop, not while driving); **one more
     stop at home**. Write each stop into the chat.
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
   - **At one of those stops, after the 3 minutes, the loom**, still in
     neutral, no throttle, timed on a phone from injector 1 going back
     on: **minute 3–4 flex the loom and connector at injector 3** gently
     by hand; **4–5 hands off**; **5–6 the same at injector 4**; **6–7
     hands off**; then drive on. Keep clear of the belt, the fan and the
     HT leads. Write into the chat anything the engine did and at which
     injector.
6. **This tank: drive normally with the MFD in**, plain fuel, item 5's
   rules; brisk driving once warm is welcome. At a warm stop now and
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
     off at once**, then item 5's rules.
   - **Item 5's S18 rules on every drive of both tanks.** The map at 3/11
     goes ahead whatever tank is in.
   **The flush and the oil change are done** (26/10, `idle-log.md`); the
   tank is driven out on the new oil.
6g. **032 on the new oil** (the *before* read 26/10: −8.6 / +7.8 %).
   - After about 200 km on the new oil: 032 and 055, before anything is
     cleared.
6h. **Every cold start, until S7 is placed.** Before turning the key,
   nothing else. Write into the chat: date, how long parked, the outside
   temperature, **caught and died, or ran**, and `StartCrank` and
   `StartDip` off the display.
   - **On alternate cold mornings, prime it**: ignition on 3 s, off, on
     3 s again, then start. Write **primed** beside that start.
6i. **The oil level on the new oil.** After the first drive on it, the
   car on level ground and **at least 5 minutes standing**: the dipstick
   out, wiped, in, out, and **photographed**; the odometer into the
   chat. **The same about every 500 km**, always after at least 5 minutes
   standing on level ground. Any top-up: the litres and the odometer
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
- **After a few hundred km:** re-tighten the cover's outer nuts you can
  reach with the plenum on, and look along the joint.

---

# Part 2 — why, and how it is read

## The rule — the owner's decision, 27/9/2026, amended 18/10/2026

**The idle comes first**: the unsettled idle (S1) and the misfires 014
counts at idle (S3). **S18, cylinder 3 dropping out with a tick, came
first beside it** from 18/10 until it closed on 24/10, after a week
without it (`refuted.md` D10); item 5's drive rules stay until the map
goes back, so that a return is caught. So:

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

**Item 5 — `IdleHealth` off the display, and the S18 rules.** The display
reading runs only until the map goes back (*owner's decision*,
18/10/2026); from then every drive is captured and `IdleHealth` comes from
the capture. **Where it sat and the lowest it touched, both** (*owner*,
15/10/2026): on a grade that wanders, a minimum keeps falling the longer
one watches, so alone it would favour long stops; beside the level it
does not. It needs about half a minute of settled idle before it reads
at all (255 until then, `docs/firmware/frames.md`), so a direction needs
several readings.

**The S18 drives** (*owner's request*, 18/10/2026; `refuted.md` D10). The
question is **whether cylinder 3 and the tick keep coming back**. A flake
of deposit loosened by the cleaner (H13) should come back less and less,
then stop; a lifter or valve (H1) should not fade, and should be worst
cold. So the reading is the run of drives:
- **No tick and no code on several drives in a row, and no 014 burst
  above 72 while driving** → fading, which reads for the flake.
- **The tick back cold, again and again** → a valve or lifter (H1). No
  leak-down (*owner's decision*, 20/10/2026; `refuted.md` D10).

**014 above 72 while driving** is the mark: sixteen earlier logs never
reached it, and 18/10 read 270 and 351. **Gently cold** because S18 came
cold, where a hanging lifter would show. **Spirited driving warm**
(*owner's decision*, 19/10/2026): full-throttle drives since 18/10 brought
no tick, and heat burns deposit off (*general*). **A flashing lamp** is the misfire
rate the ECU treats as damaging to the converter (`vcds.md`, SSP 175), so
the engine stops rather than carrying on on three cylinders; on 18/10 a
restart after a few minutes brought all four back. **No tests at the car,
four things written down** (*owner's decision*, 18/10/2026): they are
enough to see whether episodes follow hard driving (deposits) or cold
starts after a stand (a lifter). **The fault memory is saved before it is
cleared** so that each drive starts empty and the file keeps the code,
its status and its count.

**Item 5a — the original map** (*owner's decision*, 12/10/2026, to take
the remap out of the idle question; `open.md` H14, *The remap*).
**Postponed 20/10** (*owner*): the tuner emails both files to be compared
first, privately, never in this repository. What each differing table
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
  untouched minutes give about 20–40 named dips a stop. The question is
  whether the dips are still on **3 and 4** on the stock map: the same
  pair → the map was not what weakened them; a different pair or all
  four alike → the map or the cleaner moved it. Injector 1 rather than 4
  so the suspect cylinder runs throughout. Read with `--name` per stop and
  `--shares` pooled. (`cutscan.py`'s verdict rules,
  fixed 9/10 before the first cuts, are in its source.) Never the plug lead instead of the
  connector: that sends fuel to the converter.
- **The loom** (*owner's decision*, 17/10/2026; `open.md` H4): what is
  left of the electrical side is the injector loom where it runs to 3
  and 4, one taped, oily section for the two. A contact that breaks for a
  moment drops an injection the ECU does not see. After the 3 untouched
  minutes and before the car moves, so the named run is unbroken; timed
  from injector 1 going back on because that moment is in the capture.
  **Read**: dips on 3 per minute with the hand at 3, against the minutes
  either side, and the same for 4. A clear rise on the cylinder under the
  hand → that loom; nothing → cleared as far as a hand can clear it.

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

**The strong first tank** (*owner's decision*, 23/10, variant C of the
research that day). Its source is the BG reseller Red Rider (BG Centrum
Liberec), not BG: for an engine over 150,000 km, or one that drives
badly — this one is both — it offers two or three full tanks in a row, three
cans at once, or one can into about 15 l and a second into a full tank.
**That is a reseller's practice, claimed over a hundred engines, not a
specification.** Chosen here at about 25–30 l, between two and three times
the strength BG's label allows for (one can to 75 l) and milder than their
15 l, for two risks of this car
rather than of engines in general: a cleaner that works faster sheds more
deposit at once, and S18 already looks like **one flake under valve 3's
exhaust seat after a single can** of another cleaner — a flake held there
under load can burn a seat; and every misfire heats **the converter fitted
in 9/2026, whose predecessor came off blocked and burnt through**. The
strong tank has one property three cans at once lack, which is what
makes it acceptable: **it can be undone at any pump** — filling up dilutes
it at once. The can goes in before the fuel so that the fuel mixes it
(Red Rider). **Aimed at litres in the tank, not at the reserve lamp**
(*owner*, 23/10): the strength is the can over the litres in the tank,
whatever was there before, and the MFD shows them. The lamp is bit 0x80 of
0x320 b2 and the fixtures place it at **8–11 indicated litres**: on through
8 in `17`, off at 11 in `27`; no capture crosses it, so where in between
is not known. **The indication reads low**, by a gain of 0.83 near empty
and 0.905 over most of the travel (`docs/firmware/refuel-reset.md`), so
25 indicated is somewhat more in the tank (the owner aims at 25 rather
than 27 for that reason, 23/10), and the strength a little milder; the
window of 25–30 l is wider than that error. Nothing independent compares the variants; three cans at once
(their option 2) was rejected for the most shedding at once, three times
the cost and no evidence of more benefit.

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

*Done 26/10 (`idle-log.md`); kept below for how its results are read.*
**The flush and the oil** (*owner's decision*, 21/10, kept with BG's
product; **twice, variant O3**, 23/10). Two cleaner tanks and hard driving
put additive and loosened deposit into the oil: additive reaches the
crankcase past the rings, one PEA chemistry formed varnish at high treat
rates (SAE 2020-01-2100), and varnish sticks lifters — **hence the change
straight after the second tank, not later**, and the strong first tank
makes that more true, not less. **Moved ahead to before the map, with the
second tank still in** (*owner's decision*, 24/10): the caution was this
project's, not BG's or any source's; the owner no longer trusts an oil that
has carried a strong tank, hours above 4000 rpm and loosened carbon; and
**done now it stands apart from the map of 3/11** (H14, first since 24/10),
leaving drives between to read it alone, where at the end of the tank the
two would have fallen together. The cost, accepted: the rest of the second
tank's additive and loosened deposit goes into the new oil — small, the
treat rate reaching the crankcase being a fraction of the dose, and the
first tank showed no harm; a plain change after the tank stays possible,
not planned. The overlap with 44K reads nothing away: the second tank is
expected to move nothing (below). **The warm phone recording went first, on
the old oil** (26/10, `idle-log.md`), because it is the lifters' test and
after the flush there is nothing left to compare it with. **EPR cleans the oil side** — rings and
hydraulic lifters — **not valve faces or chambers**, which are the fuel
cleaner's. **Both of its sides can reach the idle**: the lifters are H1's,
and a ring stuck with coke costs compression, which tells most at idle,
where the charge is small. Against rings as the cause: compression **12 bar
even on all four** (`refuted.md` A4), while the inside differs by cylinder
(3 > 4 > 2 > 1); the evenness is the strong part, the absolute figure is
weak (gauge, cranking strokes and throttle not recorded). *This said "it is
not expected to mend the idle by itself"* (23/10), which the evidence does
not support; corrected the same day at the owner's question. **The drain
plug at about 30 Nm** is the owner's figure (23/10), not a VW document. **No compression test before and after**
(*owner's decision*, 23/10): it would read EPR's effect on the rings, at the
cost of the leads off twice, which disturbs H15's reading of the new VW
leads; whether the idle moves is read as for the tanks.

**The oil sample — dropped, 26/10** (*the owner's decision*): not taken.
H17 is read from 032 alone (6g), with the two blind cases below left
open, and 6i's level reads oil burnt against fuel gained only together.
What it was for, kept for the record:
**The oil sample** (`open.md` H17; *the owner's agreement*, 25/10). The
dipstick cannot tell fuel coming in from nothing happening when oil is
burnt at the same time (*the owner's point*), and 032 on the new oil says
whether, not how much; a laboratory's fuel dilution reads it directly,
whatever the oil use. **Before the first EPR, not at the drain**: EPR is
a solvent, and in the oil it reads as fuel to the light-end measurements
a dilution figure comes from (*reasoned*; how a given laboratory measures
it, gas chromatography or flash point, is theirs to say). The 44K does
not matter: what reaches the oil from the fuel carries it either way, at
a fraction of the dose. **Hot, after a drive**, because that is the oil as
it is mixed and as the engine sees it; the hot oil has also boiled off
some fuel, so the figure is a lower bound (*general*). **Taken always,
sent only if 032 does not settle it** (*the owner's decision*, 25/10):
032 on the new oil answers for free, but not in two cases — **unchanged**
while fuel still reaches the oil and refills the new oil within the few
hundred km before the reading, and **back to zero** where EPR freeing the
rings cut the blow-by rather than the old oil carrying fuel (H13). A
sealed bottle keeps for weeks (*general*). **Read**: a
dilution of a few per cent or more → H17 stands, whatever 032 does next;
none → H17 to `refuted.md`, and the rich idle trim is the injectors' or
the MAF's (H7).

**What would have to be wrong for the flush to mend the idle** (*reasoned*,
24/10, at the owner's question). EPR reaches the idle by three routes only:

- **A lifter on 3 or 4 whose plunger or check ball is varnished** and holds
  its valve a hair open (H1): compression lost at a small charge, covered by
  load — the idle's own pattern. Against: compression even, a valve held
  open shows when cranking; the vacuum gauge steady with no flick per cycle;
  the idle not worst hot; 18/10's tick never back. A lifter that does not
  fill would tick all the time, and none does.
- **A compression ring coked in its groove on 3 or 4** (H13's ring lands):
  worst where cylinder pressure is lowest, at idle. Against: that is exactly
  what a compression test finds, and it read even — the strongest point
  against; the absolute 12 bar is the weak one.
- **Oil-control rings stuck**, oil burnt on 3 and 4, the deposit and the
  poorer combustion with it. Against: plug 3 the cleanest, no oil use known;
  and that would mend over thousands of kilometres, not at a flush.

Not a route: **the AQY has no cam phaser**; fresh, thinner oil lowers the
friction of all four alike, which `IdleHealth`, a spread between power
strokes, does not see. **So the flush mends the idle only if a ring or a
lifter on 3 or 4 is wrong in a way compression and the gauge both missed** —
possible, against the two best measurements held. Its firm reason is
maintenance: the additive and the loosened deposit of two strong cleaner
tanks out of the oil before they varnish a lifter. **The test that told
first** was the phone recording over each lifter, hot (26/10,
`idle-log.md`): **all four alike**, so for the idle the flush is an oil
change with an additive; 3 or 4 sounding unlike 1 and 2 would have given
it a chance.

**And the fuel cleaner in the tank** (*the owner's point*, 24/10): the strong
first 44K tank, hours above 4000 rpm and about 450 km left `IdleHealth` at
70–80, as before, and he expects the second tank to do no more. What it can
reach on this engine (*reasoned*): the injector nozzles, new in 9/2026; the
inlet valve backs, only thin lacquer on the borescope; **the chambers and
exhaust valves, where 3 and 4 do carry more** — slowly, over tanks. For it
to mend the idle, that chamber deposit would have to be **the cause** of 3
and 4's poorer combustion rather than its consequence, which the evenness
of every other cause speaks against (`open.md` H13). So the second tank is
driven out because the can is in, and read as the last word on H13; the
idle is not expected to move on it.

**The run time.** BG's data sheet for `109`: for a **3.7–5.6 l** crankcase,
one can, **10 minutes at 1,200 rpm** after full operating temperature
(20 for direct injection and small diesels). *This said "45 min at 1,200
rpm on the product page"*: 45 minutes is the same sheet's figure for a
9.4–15.1 l crankcase and the 946 ml bottle, not for this engine. BG calls
10 minutes a minimum ("in as little as 10 minutes"); Red Rider runs
**30 minutes at about 1,300 rpm**. **30 minutes is chosen** (*decision*):
standing, without load, the bearings are lightly loaded and the time is
cheap, while the one way EPR is known to do harm, driving on it, is
excluded either way. The clock starts at **90 °C of oil** rather than at
warm coolant, because "full operating temperature" is the oil's.

**Twice in one day.** Red Rider advises EPR at three changes in a row and
says the first may be done **twice at once**, which BG neither says nor
forbids. A drain leaves roughly a tenth of the fill behind, so the EPR left
in the new oil is under one percent of it. The oil between runs standing for
under an hour, so it needs the viscosity and nothing else; it is **the same oil
as the final fill**, Total *Quartz 9000 Energy* 5W-40 (*owner*, 23/10), so
what a drain leaves behind is that oil and EPR and nothing else. *Quartz
9000* 5W-40 was chosen first; it carries the same ACEA A3/B4 and VW
502.00/505.00 in TotalEnergies' catalogue, so nothing is lost either way,
and *Energy 0W-30* was set aside as a different grade. **A filter
each stage**: the old one is not left to run the second flush in bypass
with the first flush's debris; the Bosch, crossed by sellers' listings
only, serves the oil between, and **the VW original serves the interval**
(*owner*, 23/10), with a new VW drain plug. **The 0.3 l out first**: on
27/9 the oil stood at the upper mark, and a can on top of that is above it
(Red Rider's first step). **The optional rinse — dropped, 26/10** (*the
owner's decision*); the final fill keeps the EPR of one drip, under one
percent by the estimate below. It would have taken the EPR left in the final fill from under
one percent to about a tenth of that, by the same tenth-a-drain
estimate. Neither level is known to harm anything; BG's own single flush
leaves the first. It needs no oil bought: about 10 l in hand, some 3.5 l
a fill. It runs at a normal level, never with less oil and EPR in it:
halving the fill under EPR doubles its strength against BG's one can to
3.7–5.6 l. Without the rinse about 1.5 l more stays for topping up; with
it, about 0.5 l. **The lifter after the fill**: a hydraulic lifter
can tap briefly while it fills from new oil, which is not S18's tick at
camshaft rate that stays.

BG warns against EPR on a heavily sludged engine; clean amber oil on every
plug thread on 20/10 (`idle-log.md`) says this one is not. **The oil**
(*bought 22/10*, mlparts.cz): Total *Quartz 9000 Energy*
5W-40, whose maker's data sheet lists ACEA A3/B4 and **VW 502.00**/505.00 —
502.00 is the approval for this engine on fixed-interval changes; the list
varies by market, hence the check on the can. **No additive in the new oil**
(*owner*, 22/10): BG's `115` MOA, considered with the cleaners and not
bought (only the two cleaners were, two cans of each), would stay in the
oil for the whole interval, its composition is not published, it is about
8 % of the fill and so changes an oil chosen for its VW approval, and its
claims (ring and valve carbon) are H13's — a change that would sit in the
engine for months. **Later changes**: EPR
at every change until the symptoms are settled, at most once a year
(*owner*, 23/10). **The VW filter** is `06A 115 561 B` off its box
(`photos/oil-filter-vw-2026-10-23-box.jpg`), the number the Bosch was
crossed to, bought at the dealer 23/10 for about 500 Kč against a little
over 100 at mlparts.cz (*owner*), where the next one comes from.

**Episodes on the cleaner's tanks are expected, not a verdict**: under H13
each tank sheds a layer; under H1 the tick would not depend on the tank.
For the converter it is a misfire that matters, not the cleaner — hence
item 5's rules. **Read**: the display through each tank, and the captures
once `IdleHealth` moves, against `30`, `31`, `33`, `34` and `40`, on settled adaptations (the
reset at 5a makes the drives just after it read low on 014 for another
reason), and the shares pooled since the last repair. A tank is weeks of
this car's driving, so the reading is late by design.

**Item 6b — the refit** (*owner's decision*, 20/10/2026). The look of
19–20/10 is done (`idle-log.md`); lead 2 tore on removal, so the leads are
replaced and the plugs with them: **VW originals**, the change H15 waits
for. Both arrive on 21/10 together. With the map postponed, **they are the
only change on the car** and are read on their own. **What is recorded at
the refit**: H15 rests on how the NGK ends sat — by grip 2 > 1 > 3 ≈ 4,
a rubbery click with a faint metallic one (`open.md` H15) — so the old
ends are compared with the VW ones by eye and by force, cylinder by
cylinder; resistance was dropped as unlikely to be the difference
(*owner*). Fitted and first driven 21/10, captured (`idle-log.md`).
**Read** over several drives against 19/10 and 12–15/10, by how long a
relief lasts (`open.md` H15): lasting weeks → the leads; a few days, then
back → the seating, H3 next; the same → H15 refuted.

**Item 6g — fuel in the oil** (`open.md` H17; 25/10/2026, from VW's
evaluation of block 032, `vcds.md`). VW names oil dilution first for a
low idle learnt value with part load normal, which is this car's 032,
and says it goes away with an oil change — which 6a does anyway, so the
test costs one reading either side. (The dipstick part is done: 24/10,
the level unchanged since the last top-up, `idle-log.md`.) **Read**: 032's idle
cell close to zero on the new oil → H17 confirmed and the cold idles of
the captures were feeding it — fewer and shorter standing cold idles
from then on; unchanged → H16 and H7 carry the trim. **`IdleHealth`
beside it, cold and warm apart** (the owner's loop, `open.md` H17): fuel
boils off only from hot oil, so H17 predicts the warm idle calmer and the
cold one unchanged; a calmer warm idle with 032 unmoved is EPR on the
rings (H13), not H17. EPR in the flush
(6a) does not spoil the comparison: it is drained with the old oil.

**Item 6h — the cold start** (`open.md` S7, reopened 25/10). The priming
asks one question: **did the rail lose its pressure while standing?** With
the ignition on the pump runs for a moment (*general*), so two goes refill
a rail that bled down overnight; a start that then catches and stays was
starved, and the leak is the pump's non-return valve, an injector or the
regulator (H7; VW's holding test in `vcds.md` names which with a gauge).
Primed starts that die as well say flooding (H7's injector, H16) or the
fuel, and the next fill of another brand reads the fuel. Alternate
mornings, so that plain and primed meet the same weather. `StartCrank`
and `StartDip` because the display carries them and a start the owner
calls normal may still show a long crank.

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
