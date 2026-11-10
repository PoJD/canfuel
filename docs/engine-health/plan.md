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
Captures only where an item asks for one. **Current: 8d, the relearn after the battery disconnect of 10/11**
(the drive from work), **then 8e**; item 6 and 6i, 8b (a second
captured warm stop with a cut on 4) and 6m for cylinder 4 after them
(*the owner*, 10/11; `open.md` H11, *The reading after the swap*).

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
   with the upper intake off — **next after 8b, for 4's deficit, which
   the clean left** (*agreed with the owner*, 9/11 evening). (5/11: contact cleaner went into 4's
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
8a. **The purge valve N80, only if P0440 comes back**: Bosch `0 280 142 353`, VW `1C0 906 517 A`, the same as the
   one on the car; the hoses stay; afterwards, warm, the owner runs
   **basic setting 070** and photographs it; then item 6's warm stops.
8b. **A second captured warm stop with a cut on 4**, on another day,
   Claude in a session on the laptop, fuel above reserve: the USBtin in
   and the MFD out before the ignition; `usbtin_capture.py` from before
   the start to engine off, `vcds_log.py --groups 014 001 003` (fault
   memory read first). **A brisk run with a motorway stretch until the
   oil is at 95 °C or more**, then **a stop on a car park in the
   everyday state, the A/C off**: 3 minutes' idle, **injector 4's
   connector off for 30 s** (say when, by the chat), 3 minutes more.
   At the end, engine idling: the fault memory, then 032/055; the owner
   clears it by hand.
8d. **The relearn after the battery disconnect** (disconnected by the
   owner on 10/11 after parking at work). Claude in a session on the
   laptop, VCDS only; **no CAN capture**: the MFD in.
   1. **On reconnecting the battery, the owner runs 098 under basic
      settings** himself, as on 27/10, and photographs the result. Then,
      ignition on, engine off: the fault memory read; **032 055 for
      20 s**.
   2. **The drive home: 014 032 036 logged** from the start to engine
      off; the laptop not touched while driving. Drive as the day brings
      it. **At every warm stop on the way, `IdleHealth` and `Misfires`
      into the chat with the time** — the first ones are the idle with
      032 near zero.
   3. **At the end, a warm stop in the everyday state, the A/C off, 3
      minutes**; `IdleHealth` and `Misfires` into the chat as it goes.
      Then **032 055 for 20 s** and the fault memory, engine still
      idling; the owner clears it by hand only if there is a code.
   4. **After that, 032 for 20 s at every session with VCDS connected**,
      until both cells have held for three drives.
8e. **The new probes' tightness**, at the next cold engine after 8d:
   with the spanner they were fitted with, whether either turns further
   at the effort they were tightened with. Which, and about how far,
   into the chat; nothing undone.
9. **After the clean of 9/11, by what the next stops show** (Claude says
   which):
   - **A CO₂ ("block") test of the coolant**, warm, at a garage or with
     a kit.
   - **A stethoscope (or a long screwdriver) on the cam cover above
     cylinder 3, hot**, against 1, 2 and 4: a tick or a hiss on one, at idle.
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

**8d, the relearn after the battery disconnect** (*the owner's
decision*, 10/11: whether 032 goes back to its large negative values on
the new probes, and whether that moves the idle; `open.md` H11, *The
relearn after the battery disconnect*). **Why it is the test of H11's
mark 1**: 032 starts from 0.0 / 0.0, and on the old probes its idle
cell was back at −6.3 % after one drive from both resets on record
(27/10 and the map of 3/11), so where it gets to in one or two drives
on the new ones says whether the old front probe made it — back at
about −6 % says not, within ±3 % over three drives says it did. **The
idle is read separately** (marks 3 and 4), because the owner's idle was
rough at −4.7 % in the summer too. **032 logged through the drive**,
not only at the end, to see when each cell moves; **036** for the
rear probe at the stops and a second time under load, and whether its
switch to the front's swing after 18 minutes of idle comes back;
**014** for the misfires, though **a quiet 014 after a disconnect is no
evidence** (`refuted.md` C19's rule: the crank wheel's tooth errors may
have to be learnt again on the overrun). 001 and 033 are dropped: 014
carries engine speed and load, and 033's regulation stayed within ±2 %
on 10/11. **032/055 before the start** to see the reset itself (a
minute's disconnect leaves 055, hours reset it: `idle-log.md`, 26/10
and 27/10). **098** because VW asks for the throttle adaptation after a
disconnect (`vcds.md`); it is a basic setting, so the owner runs it,
never Claude (`CLAUDE.md`). **The warm stop at the end** is read with
055 settled — it relearns within the first few entries into a warm idle
(`idle-log.md`, 27/10) — and is the second of the three stops H11's
marks ask for. **The stops on the way** because the idle cell starts at
zero and learns at idle: they read the idle with 032 near zero, the
owner's test of whether the learnt cell itself made the idle rough
(`open.md` H11, *The owner's hypothesis for the relearn*). **The order
of the hypotheses is re-read after this drive** (*the owner*, 10/11). **No CAN capture** (*the owner*, 10/11), so the dips'
share over the cylinders waits for 8b.

**8e, the probes' tightness**: they were tightened by hand to about 50
Nm estimated, without a torque wrench (`vehicle-history.md`), and the
reading after showed the rear probe switching to the front's swing
after 18 minutes of idle and in spells at the warm stop; a probe seated
loose lets air into the exhaust at idle's pulses, the second zone of
H2 of its own making (*reasoned*). Cold, because the exhaust then is at
the temperature they were fitted at. Checked before the warm tailpipe
test (item 7), which it would otherwise confuse.

**8b, the second captured stop**, because the rough start is what
varies most between stops: stop 3's own second half read like stop 7,
and straight after the clean 3 was still short, so one stop each side
does not say the clean's effect lasts; a warm stop after a similar run
with a 30 s cut on 4, on another day, does — a rough start on 3 again
says it did not. **6m for 4** because 4 is now the cylinder with a
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

**Item 8a — the purge valve, conditional** (*the owner's decision*,
6/11 night: *this was "replaced after item 8's readings", his decision
of the same evening, until the valve was out*). Out of the car it
passed air unpowered not clearly at all, at most "really very little"
(*owner*), it had no granules or fuel behind it, and it was cleaned with
its contacts and refitted (`idle-log.md`). The part is known and fits;
**a code once in eight years is acceptable** (*the owner*), so it is
bought if P0440 comes back. *Until 9/11 also "or if item 8 leaves the
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
