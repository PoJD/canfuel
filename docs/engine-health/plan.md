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
   - After the drive: read the fault memory of 01, save it ("Uložit
     chyby"), then clear it.
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
   - **After the tank: one or two warm drives captured**, on different
     days. Claude runs the capture; VCDS on **014, 003, 020**; 055 once
     at the end, warm idle. Write the stops.
   - **On one of them, a hard motorway run**: a few minutes brisk at the
     limit, two or three full pulls, then **a warm stop of a few
     minutes**, loads off.
6a. **Two tanks of BG 44K** (BG `208` *44K Platinum*, 325 ml a can), from
   the BG kit 6577. **Into the next tank, after this one**, never into
   this one, and **into the tank after that again**. One can into each
   fresh tank of the usual OMV MaxxMotion 100, **filled up**, and no
   refuelling until that tank is run down (at least 40 l a tank). Drive it
   as item 6: warm, brisk once warm. **Item 5's S18 rules on every drive
   of both tanks.** The map at 3/11 goes ahead whatever tank is in.
   **Straight after the second tank: the oil flushed, then oil and filter
   changed**:
   - Warm the engine to operating temperature, park it.
   - One can of **BG `109` EPR** (325 ml, from the kit) into the warm oil.
   - **Run it standing for the time on the can**, at the speed the can
     says; no driving. A tick: stop the engine and drain.
   - Drain at once, hot. **New filter Bosch `0 451 103 314`**, set beside
     the old one first: the same thread, seal and height, or it does not
     go on. **New oil Total *Quartz 9000 Energy* 5W-40**; the can must say
     **VW 502.00**. Write into the chat the odometer and the litres it
     took.
   - **The kit's BG `115` MOA stays on the shelf**: nothing into the new
     oil.
6c. **Any time, when convenient: two checks at one warm stop**, oil
   95–100 °C, neutral, handbrake on, loads off, bonnet open. With the
   USBtin capturing if the laptop is there (no MFD then); otherwise by ear
   and the rev counter.
   - **The screwdriver**: a long screwdriver's tip on the valve cover, ear
     on the handle, **above each cylinder in turn, 1, 2, 3, 4**, about
     30 s each, then 3 and 4 again. Keep clear of the belt, the fan and the
     HT leads. Write into the chat whether any cylinder sounds different:
     a tick, a knock, an uneven beat.
   - **Brake cleaner**, **non-chlorinated only** (the can says so), a fire
     extinguisher within reach. Short bursts of one second, **never on the
     exhaust manifold, the leads or the coil**. 20–30 s between places,
     until the idle is back. In this order:
     1. the joint of the lower manifold to the head at **cylinder 1**;
     2. the same joint at **cylinder 3**, then at **cylinder 4**;
     3. where **injector 3**, then **injector 4**, enters the manifold;
     4. the joint of the upper plenum to the lower manifold; the vacuum
        hoses.
     Watch the first one or two seconds after each burst. Write each place
     into the chat with the time, and whether the engine changed: revs up,
     smoother, or a stumble.
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
- **The fault memory after every session at the car**: read, saved,
  then cleared by the owner by hand.
- **After a few hundred km:** re-tighten the cover's outer nuts you can
  reach with the plenum on, and look along the joint.
- **When there is a thermometer, at the end of a hot captured session:**
  engine off; ignition straight back on; within a minute measure the oil
  filter, the sump from beneath and the upper coolant hose; write the
  three readings into the chat in that order.

---

# Part 2 — why, and how it is read

## The rule — the owner's decision, 27/9/2026, amended 18/10/2026

**The idle comes first**: the unsettled idle (S1) and the misfires 014
counts at idle (S3). **S18, cylinder 3 dropping out with a tick, now comes
first beside it**, since the owner reads both as likely one cause. So:

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

**The S18 drives** (*owner's request*, 18/10/2026; `open.md` S18). The
question is **whether cylinder 3 and the tick keep coming back**. A flake
of deposit loosened by the cleaner (H13) should come back less and less,
then stop; a lifter or valve (H1) should not fade, and should be worst
cold. So the reading is the run of drives:
- **No tick and no code on several drives in a row, and no 014 burst
  above 72 while driving** → fading, which reads for the flake.
- **The tick back cold, again and again** → a valve or lifter (H1). No
  leak-down (*owner's decision*, 20/10/2026; `open.md` S18).

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

**Item 6's hard run** (*owner's request*, 14/10/2026). On 4/10, on fresh
adaptations, 014 counted only at the stop after a hard drive (`open.md`
S3, *Session A after step 1b*); on settled ones it counts at every warm
stop, so the run says less than it would have then. What is read is
**the stop after it**: under load 014 has almost never counted on this
car. On the original map if it is back by then, and apart from a
cleaner's tank. The legal limit caps the run: brisk at the limit plus
full pulls.

**Item 6a — two tanks of BG 44K** (*owner's decision*, 18/10/2026: S18
and the idle likely one cause, deposits; *21/10–22/10*: BG 44K for two
tanks in a row instead of the Liqui Moly Pro-Line `5153` bought on 21/10,
which is kept for later; **the overlap with the map at 3/11 accepted** —
*"I mainly want it solved"*). **Two tanks** because BG's own instructions
for a deep clean are two full tanks in a row, against one can per
10,000–15,000 km for upkeep; a third adds less. BG names injectors,
valves and the combustion chamber, and publishes no chemistry: that it is
PEA is said of it, not stated by its maker.

**What the overlap costs.** The drives after 3/11 read the map and the
cleaner together, and only those before it read the cleaner alone. If the
idle improves, which of H13 and H14 did it is left open; the owner chose a
fix over the answer.

**The flush and the oil** (*owner's decision*, 21/10, kept with BG's
product). Two cleaner tanks and hard driving put additive and loosened
deposit into the oil: additive reaches the crankcase past the rings, one
PEA chemistry formed varnish at high treat rates (SAE 2020-01-2100), and
varnish sticks lifters — **hence the change straight after the second
tank, not later**. BG's run time for EPR differs between its own sheets
(45 min at 1,200 rpm on the product page, 5–10 min in its oil-change
procedure), so **the can decides**. BG warns against EPR on a heavily
sludged engine; clean amber oil on every plug thread on 20/10
(`idle-log.md`) says this one is not. **The oil and filter** (*bought 22/10*, mlparts.cz, with the BG cans):
Total *Quartz 9000 Energy* 5W-40, whose maker's data sheet lists ACEA
A3/B4 and **VW 502.00**/505.00 — 502.00 is the approval for this engine on
fixed-interval changes; the list varies by market, hence the check on the
can. Filter Bosch `0 451 103 314`, sold for this engine and crossed to VW
`06A 115 561 B` by sellers' listings rather than a maker's catalogue, hence
the side-by-side check. **MOA is not used** (*owner*,
22/10): it stays in the new oil for the whole interval, its composition is
not published, it is about 8 % of the fill and so changes an oil chosen
for its VW approval, and its claims (ring and valve carbon) are H13's —
a change that would sit in the engine for months.

**Episodes on the cleaner's tanks are expected, not a verdict**: under H13
each tank sheds a layer; under H1 the tick would not depend on the tank.
For the converter it is a misfire that matters, not the cleaner — hence
item 5's rules. **Read**: item 6's drives and the captures after each
tank against `30`, `31`, `33`, `34` and `40`, on settled adaptations (the
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

**Item 6c — the screwdriver and the brake cleaner** (*owner's
decision*, 21/10/2026: no propane for now, no stethoscope bought; *when
he gets to it*). Both test a cause rather than name a cylinder, which
`open.md` already does for 3 and 4.

- **The screwdriver is H1's cheapest test** (`open.md` H1): a lifter that
  bleeds down or a valve that seats late ticks at camshaft rate over its
  own cylinder. A sound only over 3 or 4 points at the valvetrain there; all
  four alike weakens H1. A screwdriver hears less than a stethoscope, so
  silence is weaker evidence than a tick.
- **The brake cleaner is H3's** (`open.md` H3): sprayed where air is drawn
  in, it is drawn in too and enriches the charge for a moment, and the idle
  answers within a second or two before the lambda loop takes it back. Any
  prompt change counts. **Cylinder 1 first** shows what *nothing* looks like.
  A reaction at 3 or 4's head joint or injector seat, and not at 1, is a
  leak at that runner: the lower gasket or the injector's O-ring is the
  repair. **No reaction anywhere weakens H3 a good deal**, since this reaches
  the one place the vacuum gauge on the common plenum could not (`open.md`
  H3). The smoke test of 9/10 looked for air going out, cold; this one looks
  for air going in, warm and running. **Non-chlorinated**, because a
  chlorinated cleaner burnt in the cylinder makes phosgene (*general*).
- **Captured if possible**: `IdleHealth` is a filtered grade and too slow for
  a one-second event, but the capture resolves each stroke, so each burst
  can be read off engine speed against the time written into the chat.

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
- **The fault memory** (*owner*, 18/10/2026): every session starts from
  an empty memory, and the saved file keeps what the session stored.
- **The cover's nuts**: the gasket settles (`refuted.md` D5).
- **The thermometer reading**: `docs/firmware/open.md` question 10. The
  ignition goes back on so the capture keeps 0x420; the coolant hose
  checks the instrument against 0x288's coolant.
