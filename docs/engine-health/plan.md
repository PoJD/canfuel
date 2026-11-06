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
Captures only where an item asks for one. **Current: item 6 and 6i
from 4/11, the MFD in; item 8, the decarbonisation, Monday 9/11 at
9:45, captured from home to work; 8a, the purge valve, after its
readings; 6m or item 9 after it.**

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
   **only if item 8 changes nothing**, with the upper intake off, **never
   the same day as item 8**. (5/11: contact cleaner went into 4's
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
8. **The next repair: a professional decarbonisation, with hydrogen**
   (*the owner's decision*, 3/11; a provider such as *Bez karbonu*,
   his choice; 70 min for up to 2.5 l, 3,290 Kč by its site). **Monday
   9/11/2026, 9:45.** They do not clear the fault memory, and the gas goes
   in behind the MAF (*owner*, 6/11). **One captured session from home to
   work** (*the owner's plan*, 6/11), Claude in a session on the laptop,
   on the car's 12 V charger; fuel above reserve:
   1. **At home, before the ignition**: the MFD out, the USBtin in. Claude
      starts `usbtin_capture.py`, then `vcds_log.py --groups 014 001 003`
      (fault memory read first).
   2. **About 30 minutes out, the motorway included**, until the oil is at
      95 °C or more.
   3. **A stop on a car park before the provider, not at it**: the A/C
      off, the same loads as at step 7; 3 minutes' idle, **injector 4's
      connector off for 30 s** (say when, by the chat), then 3 minutes
      more.
   4. **At the provider**: say in the chat when the engine stops and when
      it starts for the clean; the capture runs on, VCDS is restarted by
      Claude once it runs. **Ask the machine's output in litres a minute,
      and whether it makes oxyhydrogen (HHO) or hydrogen alone**. **The
      coolant and oil temperatures are watched by us** through the hour,
      on the capture (Claude, 0x288 and 0x420; `oilwatch.py` on the
      laptop) (*the owner*, 6/11). The cluster has no temperature gauge,
      only a blue lamp while the coolant is cold (below about 60 °C, read
      against the MFD) and a red one for too hot or too little coolant
      (*owner*).
   5. **After the clean**: a few minutes' idle there, no cut.
   6. **On to work with a brisk motorway run first**, as the provider
      advises after a clean, about as long and hard as the morning's;
      **listen for a tick** like 18/10's (a flake under a seat), and say
      in the chat if one comes.
   7. **A stop before work**, as step 3: the A/C off, the same loads, 3
      minutes, injector 4 off for 30 s, 3 minutes more.
   8. **At the end, engine idling**: Claude reads the fault memory, then
      **032/055 before anything is cleared**; the owner clears it by hand.
   **The baseline before it**: the display's readings of 6–8/11, after the
   contact cleaner and the straightened gasket edge of 5/11 (6/11: 65
   with the A/C, `Misfires` 18, MisfAvg 23.0; 6/11 evening: 73 with the
   A/C off, `Misfires` 6, MisfAvg 8.6; `open.md` S1). **After it**:
   item 6's drives again, `IdleHealth` as always, at several warm stops,
   **with a word on what came before each stop** (queuing, or a brisk
   stretch), and the A/C's figure too whenever it happens to be on; **an
   odd cold misfire or a drop-out on one cylinder in the days after** goes
   into the chat at once.
8a. **The purge valve N80 replaced** (*the owner's decision*, 6/11),
   **only after item 8's readings**, never in the same days as item 8.
   - **The part**: the valve's own number, **on the valve body** once it
     is out of its rubber holder (`051 133 459 A` is the holder, 6/11),
     most likely a Bosch `0 280 142 …`; VW or Bosch, not aftermarket.
     **Found by the car (*owner*, 6/11): Bosch `0 280 142 353`**, = VW
     `1C0 906 517 A`; compare it with the old valve before fitting
     (ports, hose sizes, the holder), and buy it where it can go back.
   - **While it is out**: photograph the rubber hose from the canister's
     side as far as it can be seen, bent, for cracks and hardness, and
     the thick hose from N80 to the back of the intake; look into the
     old valve's canister-side port and the hose behind it for **black
     granules**, and photograph them. **The plastic line under the upper
     intake to the T at the throttle stays** (looked over with the
     intake off several times, the smoke test clean; *owner*, 6/11).
   - **Granules, or a smell of fuel at the canister-side port → the
     canister is looked at**: follow the tank's vent line (the third of
     the three under the car) to it, most likely behind a rear wheel
     arch liner; photograph it; liquid fuel or granules → a new canister
     and its hoses. Otherwise the canister is not touched.
   - Rubber hoses cracked or hard → new, the same day.
   - **Afterwards, warm**: the owner runs **basic setting 070** himself
     and photographs the result (the TEV line and the lambda); then
     item 6's warm stops as always, `IdleHealth`, `Misfires`, MisfAvg,
     into the chat.
9. **After item 8, by what it shows** (Claude says which):
   - **A CO₂ ("block") test of the coolant**, warm, at a garage or with
     a kit.
   - **A stethoscope (or a long screwdriver) on the cam cover above
     cylinder 3, hot**, against 1, 2 and 4: a tick or a hiss on one.
   - **A warm leak-down on all four** at a garage, oil at 80 °C or
     more: the upper intake off and all four plugs out (the same plugs
     back afterwards; plug 3's gap measured while out); each cylinder at
     TDC on its compression stroke, firing order 1-3-4-2; the crank held
     while the air is on. For each: **the percentage, and where it
     hisses** — tailpipe, throttle, oil filler, bubbles in the coolant
     tank, the next plug hole.
   - With VCDS connected anyway after a stored P030x: **a generic
     OBD-II read** (modes 02 and 06), read only, saved.
   - **No head off** (*the owner*, 4/11, leaning, not final): if the
     leak-down names 3's exhaust seat, the car is driven as it is and S1
     most likely closed as *acceptable, cause known*.

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
- **`IdleHealth` and `Misfires` only in the everyday state** — **blower on 1, one seat
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
without it (`refuted.md` D10); the owner kept its drive rules as a
habit until the map went back (3/11), so that a return was caught (they
left Part 1 on 26/10 at his request: not a step, what he does anyway);
whether he keeps them since is his. So:

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

**Item 7 — the high-voltage side** (`open.md` H4; `refuted.md` C24): the roughest
reading on record came on a foggy morning (`open.md` S1, *Temperature*),
and the mist supplies the moisture a tracking boot or coil needs. Late
because the coil is from 6/2026 and the leads are new again; it is free.

**Item 8's day, why it is read this way** (*agreed with the owner*,
6/11). **One session, before and after the same day**, because the
weekend's display gives the level but not the cylinders: only a cut
names them, and the last one (`43`, 3/11) came before 5/11's changes.
**Like with like**: the idle is calmer for minutes after a brisk drive
(`open.md` S1, *After high revs*), and an hour at 2,000 rpm is one, so
the "before" stop comes after the motorway and the "after" stop after
the drive to work, not straight after the clean. **The A/C off at both**:
its load raises 014's threshold (`open.md` S3, *What it counts*) and
calms the random part of the grade. **Cuts on a car park, not at the
provider**: a cut stores P1240 and perhaps P030x (3/11), which should
not mix with their work. **During the clean** the gas enters behind the
MAF, so the MAF does not see it, and the hose they slip under the intake
boot lets in unmetered air around it: lambda and 032 will move and
relearn; 014 is likely deactivated at 2,000 rpm with no load. **Read**:
`IdleHealth` split into the steady pattern over the cylinders and the
rest (`open.md` S1, *A steady pattern over the cylinders*), named by
each cut; `cutscan.py --shares --name`, `dipshape.py --name --order 4`
and 014 at both stops. 3 and 4's deficit gone after → H13; kept → H3 or
H4 (item 6m); 3 alone → H1 (item 9).

**Item 8 — the next repair** is chosen then, from `open.md`, *The idle's
candidates, ranked*. **Since 3/11 evening deposits (H13) and a valve on
3 (H1) led** (*agreed with the owner*): `43`'s injector cut names
cylinder 3, the one the borescope found worst; **since 5/11 H13, then a
leak at runners 3–4 (H3), then H1** (the steady pattern names 3 and 4
alike, `open.md` S1). The two 44K tanks moved
nothing, so a chemical clean through the fuel is spent; a professional
decarbonisation is **the next repair** (*the owner's decision*, 3/11), for
H13 and, if the deposit on 3's seat is what keeps it from sealing, H1.
**Read**: `IdleHealth` in the everyday state before and after, the same
ruler as item 6; a capture only once the display shows a change (item
6). What it reaches is asked first because a clean through the intake
works on the chambers and crowns, where the borescope found the
deposit, not on a seat that is worn (*general*). **The output** because
the machines differ about sixfold (280 l/h to 30 l/min), and the one
independent study ran the large one and found no change (`open.md`,
*What the forums say*, hydrogen decarbonisation, 4/11). **The car had one
before**, with hydrogen, on 10/8/2021 (`vehicle-history.md`): its
effect was not recorded, and the 3,400 km and more since (152,000 at
1/2022 against 155,357 on 3/11, the odometer table there), most of
them gentle until 9/2026 and a year laid up, were enough to build what
the borescope saw in 10/2026 — so a clean is a reset, not a cure, if
gentle use comes back (*reasoned*). **2,000 rpm held, not idle**: an
hour at a standing idle would be the converter's exposure the standing
items avoid (122 of 129 counted misfire events began at a standing
idle, `open.md` S3); held revs are not. **Nothing measured there**, so
the before and after is `IdleHealth` on the display — **before** is
what is already read: 80–105 on the display on the remap (28/10–2/11),
and on the original map `42`'s 54–77, `43`'s 48–86 loads off and
**70–95 on the display** the night of 3/11 (everyday state, oil 101 °C),
**90–110 after queuing and 70–90 after revving on 4/11, 45–50 with the
A/C**, plus whatever item 6's drives give until the appointment. **What
the stops are read for** (`open.md` S1, re-read 4/11 on the load and
revving patterns): if the deposit on 3's exhaust seat is what the two
share (H13 with H1), the clean narrows **both gaps** — loads off towards
the A/C's figure, queuing towards after revving; the gap after queuing
gone and the load's kept points at H3 instead; both kept, item 9. Hence
the word on what came before each stop. And H1's own test
(a warm compression or leak-down reading on 3 against the others,
`refuted.md` A4) stays for afterwards, if the clean does not help. **No injector swap**
and **no plug change for now** (*his decisions*, 3/11). **The days after**
(*reasoned*, from SAE 2000-01-2858: water flakes deposits most): the
clean burns hydrogen to water vapour, so a flake may come loose and lodge
under a seat, an 18/10-like drop-out; if one comes, a warm leak-down on 3
the same day or the next is the one moment it can be told from a seat
or a guide. **The capture with the cut** (`cutscan.py --shares --name`,
and `dipshape.py --name --order 4`: whether 3's dips of two firings in a
row go with its single ones, `open.md` S1, *How many strokes make a dip*;
and `IdleHealth` split into the steady pattern over the cylinders and the
rest, named by the cut, `open.md` S1, *A steady pattern over the
cylinders*: whether the clean took 3 and 4's deficit, the dips, or both)
is the reading that separates: calmer with 3's share near 25 % → the
deposit on 3 was the excess (H13); calmer with 3 still leading → 3 has
its own cause (H1, item 9); no change → item 9. The display's own spread
(48–105 loads off) is as large as the effect looked for, so `IdleHealth`
alone does not decide it; the capture is the exception item 6's "no
captures until the display shows a change" makes for a repair (*agreed
with the owner*, 4/11). Above reserve, because the ECU puts a misfire
on an empty tank down as P1300 (`open.md`, *What the forums say*).

**Item 8a — the purge valve** (*the owner's decision*, 6/11, after
P0440 and the engine lamp, `open.md` S21 and H16; *this was "not
replaced", the owner's decision of 25/10, until then*). **After item 8's
readings** (*the owner*, 6/11): one change at a time, so that the idle
after each can be put down to it. **What else**: the hoses because a
cracked one gives the same code, and the granules because a canister
that sheds charcoal jams the new valve open (*general*). **The part**: Bosch `0 280 142 353`
is listed by sellers as VW `1C0 906 517 A` (superseding `955 605 517 00`),
and one lists that for the New Beetle 2.0 from chassis 1C-Y-400 001, a
split inside model year 2000; this car is a 2000 with a serial above it
(the VIN), so it should fit (*general*, sellers' lists, not VW's
catalogue); **Auto Kelly lists it for this car, engine AQY** (*owner*,
6/11). Whether the valve on the car is already of that kind is
seen only when it is out, hence the comparison. **The plastic
line under the upper intake is left** (*the owner*, 6/11): seen whole
with the intake off several times, the smoke test showed nothing there,
and changing it means the intake off. **Where the canister is** is not
settled: on US New Beetles of 1998–2000, with a leak detection pump, a
rear wheel arch, the right by Chilton's manual, the left by others
(*general*); a European car need not match, so the tank's vent line is
followed to it, and only if the valve's port shows granules or fuel.
**The filler cap
is not on the list**: it is new from about early 10/2026 (*owner*,
6/11, `vehicle-history.md`), and this car has no tank pressure sensor and no leak
detection pump (a European car, the VIN), so the ECU can only open N80
and watch lambda and idle air (block 070's fields), and a cap cannot fail
that (*reasoned*). **070 afterwards** is the ECU's own check of a valve
that opens; it is a basic setting, so the owner runs it, never Claude
(`CLAUDE.md`). **No warm A–B–A with the hose plugged before it** (*the
owner*, 6/11: not needed); so the idle after the swap is read against
item 8's readings, on the display, with the A/C state named.

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
worse beyond its spread are read as a seat getting worse; and the
converter carries the idle's misfires (`open.md` S3), which is why the
standing items keep idling short.

## Standing items — why

- **`Misfires` beside `IdleHealth`** (*the owner's request*, 4/11):
  an estimate of VCDS 014 off the bus — the dips of 20 rpm in the last
  minute of standing idle, zero whenever 014 had not counted in that
  minute over every capture with a 014 log, and near zero with the A/C on
  as 014 is (`docs/firmware/open.md` 11, *Misfires*). It lets a stop say
  whether 014 is counting without VCDS; VCDS stays the instrument.
  `--preserve-eeprom` keeps the stored trip and tank (`flashing.md`).

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
