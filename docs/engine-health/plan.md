# Engine health — the planned fixes, in order

**Part 1 is what to do, in order, with no explanation.** It is what goes
to the car. **Part 2 is why, and how the results are read.** Keep it that
way (*owner's decision, 8/10/2026*). An instruction goes in Part 1 and its
reason in Part 2, never mixed. Why each step exists at all lives in
`open.md`; what was done lives in `vehicle-history.md` and `idle-log.md`.
**A step that is done is removed from both parts in the commit that
records it**, and the file is deleted when it is empty.

---

# Part 1 — what to do

## Step 3 — the idle is not fixed

One at a time; Claude says after each whether the next is needed.
Claude runs the capture on every drive.

5. **Until the map goes back: `IdleHealth` off the display**, with the MFD in: on
   drives where the oil reaches **95–100 °C** on the display, at one
   stop **in the two states of the standing items**, loads off and
   loads on. Write into the chat: date, oil temperature, and for each
   state **where `IdleHealth` mostly sat and the lowest it touched**.
   **Also until the map goes back, on every drive (S18) — protecting the engine and
   the converter comes first:**
   - **Warm the engine up gently**: no high revs until the oil reads
     **80 °C** on the display.
   - **Warm and on four cylinders**: spirited driving is fine, full
     throttle included.
   - **A tick or a felt misfire**: ease off and drive on gently, no
     high revs while it lasts.
   - **The engine lamp on**: ease off.
   - **The engine lamp flashing, or running on three cylinders**: stop
     where it is safe, **switch the engine off, wait a few minutes**,
     start again. Drive on only if it runs on four.
   - VCDS on **014, 001, 003** whenever the laptop is in the car.
   - **After the drive: read the fault memory of 01, save it ("Uložit
     chyby"), then clear it.**
   - **If there was an episode** (a tick or a misfire), write into the
     chat: **when** (date, roughly what time, minutes after the start),
     **what came before** (hard driving, a cold start, a long stand),
     **oil temperature** and **`IdleHealth`** off the display.
5a. **Postponed: the original map written back** at the tuner — not
   on 22/10; first the tuner emails both files, the original and his
   remap; upload them into the chat (they never go into the
   repository); a new date after they are read. Then, at the tuner, the ECU
   comes out of the car. **The drive home first, as below; then one or
   two ordinary warm drives**: Claude runs the capture; VCDS on
   **014, 003**; 055 once at the end, warm idle; on one of them **one
   held full-throttle pull in 4th**, with VCDS on **014, 003, 020** for
   that drive.
   - **At the tuner, before he writes**, ask for these files, each the
     **whole flash**, not only the maps: **the original** he read
     before the remap, **his remapped version**, and if he will,
     **a read of the ECU as it is now**. Write down the software
     version off his tool. Not the EEPROM.
     Upload the files into the chat; they never go into the repository.
   - **The drive home from the tuner, captured, not with the MFD.** Capture started **before the first
     start** at the tuner, running to engine off at home; VCDS on
     **014, 055, 003** the whole way. No `oilwatch.py`. **A few minutes
     of idle straight after the start, cold**; once warm, drive briskly;
     **when 055's field 3 nears −0.95, stop for another few minutes of
     idle** — read it at a stop, not while driving; **one more at home**.
     Write each stop into the chat.
   - **On one of these drives, two or three stops with a cut**, oil at
     95–100 °C: neutral, handbrake on, loads off. **Injector 1's
     connector off for 30 s** (injector 4 if 1 cannot be reached), by
     the connector body with the clip pressed, gloves; back on. **Then
     at least 3 minutes of idle, nothing touched** — no throttle, no
     steering, no loads. Write each off and on into the chat. A
     flashing lamp is expected; clear the fault memory with VCDS after
     the drive.
   - **At one of those stops, after the 3 minutes, the loom**, still
     in neutral, no throttle, timed on a phone from the moment injector
     1 went back on: **minute 3–4 flex the loom and connector at
     injector 3**, gently, by hand; **4–5 hands off**; **5–6 the same at
     injector 4**; **6–7 hands off**; then drive on. Keep clear of the
     belt, the fan and the HT leads. Write into the chat anything the
     engine did and at which injector.
6. **On the next tank: two or three ordinary drives, warm**, on
   different days. Claude runs the capture; VCDS on **014, 003, 020**;
   055 once at the end, warm idle. Write the stops.
   - **On one of them, a hard motorway run**: a few minutes brisk at
     the limit, two or three full pulls, then **a warm stop of a few
     minutes** with loads off. Before it: the timing belt's interval
     checked against its date (10/2017).
6a. **A second can of the cleaner, only after 6's drives, and only if
   the owner decides to then.** Until then every tank is plain
   OMV MaxxMotion 100. If it goes in: the maker's dose, into a fresh
   tank of the usual fuel, and **item 5's S18 rules on every drive of
   that tank**. **After that tank: oil and filter changed.**
6b. **When the parts arrive (21/10), the refit**: VW plugs
   `101 000 033 AA` at 25–30 Nm; VW leads `06A 905 409 L`,
   every end pushed fully home at the plug and at the coil; the plenum
   on a new Elring `271.230` (VW `06A 129 717` is out of production). A photo of each box with its part
   number. Then start it and write into the chat how it started and how
   the idle runs.
   - **Before fitting, the old NGK set** (*plug ends of 1, 3, 4; lead 2
     is torn*): with a caliper, the inner diameter of the metal clip in
     each plug end; each lead's length and its end-to-end resistance
     with a multimeter. A photo of the caliper on each reading.
   - **A photo of a VW plug's top beside an NGK's**, the terminal both
     leads grip.
   - **While fitting the VW set**: for each cylinder, how firmly the end
     seats and whether it clicks — metal or rubber. The same for the
     coil ends. Write it into the chat by cylinder.
   - **On the first warm drive after it**: `IdleHealth` in the two
     states of the standing items.
7. **Only if Claude asks after 6:**
   - **The exhaust test again, warm**, after a drive to 95–100 °C of oil.
     **Leaks there → a new manifold**: new gasket to the head, new nuts,
     new outlet gasket, the probe refitted with anti-seize. Part
     `06A 253 031` + suffix: read the number cast into the manifold, or
     ask by VIN. New from VW about €350–490, used 700–1,500 Kč.
     Penetrating oil on the studs the days before; a snapped stud goes
     to a garage.
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
  - At a stop longer than a minute or two, where it is safe: engine off.
  - After a hard or long drive: switch off on arrival, no idling.
  - **Engine lamp flashing**: ease off at once, stop where safe, engine
    off, write it into the chat.
- **`IdleHealth` at a warm stop, always in two states** (oil 95–100 °C,
  neutral, no throttle, nothing else touched), on every drive that reads
  it, captured or off the display:
  1. **2 minutes with every load off**, the lights too where the switch
     allows it (in the dark); whatever cannot be switched off stays on,
     and say which.
  2. **Then 2 minutes with every load on**: main beam, both seat
     heaters, the heated glass, A/C and the blower on full.

  With the laptop, Claude reads both off the capture; with the MFD in,
  write each state's reading into the chat.
- **After a few hundred km:** re-tighten the cover's outer nuts you can
  reach with the plenum on, and look along the joint.
- **When there is a thermometer, at the end of a hot captured session:**
  engine off; ignition straight back on; within a minute measure the oil
  filter, the sump from beneath and the upper coolant hose; write the
  three readings into the chat in that order.

---

# Part 2 — why, and how it is read

## The rule — the owner's decision, 27/9/2026

**The idle comes first.** After the oil leak, the one thing this work is
for is the unsettled idle (S1) and the misfires VCDS counts at idle (S3,
group 014). **Amended 18/10/2026** (*owner's decision*): **S18,
cylinder 3 dropping out with a tick, is now the worst symptom and comes
first**, with the idle beside it, since the owner reads both as likely
one cause. The rules below hold for both. So:

- **Fix, then look.** Each step is a repair; the only readings taken are
  the ones that decide the next step.
- **No test for its own sake**, and nothing unrelated to the idle is
  pursued until the idle is solved — unless it could be related.
- **Run the engine as little as possible, and above all not at idle.**
  The misfires are an idle phenomenon and the old converter already paid
  for them once. Warm the engine by driving, not by idling.

The rest of `open.md` — the other symptoms, every hypothesis's test list —
stays as reference. **It is not a to-do list.**

**Where it stands:** recorded in `idle-log.md` — steps 2a–2c (9/10),
and on 10/10 the servo, new plugs and leads with a new intake gasket,
the drive after and one day of injector cuts. The intake is tight cold,
the servo is cleared, and the misfires remain at every warm stop on
settled adaptations with nothing a sealed leak would move having moved
(`open.md` S3; `refuted.md` C19). On the one drive since the new leads
the dips no longer keep to one cylinder's stroke. **On 12/10 item 1
of this step was done** (`idle-log.md`): the exhaust tight to the ear
cold, the clutch no part of the dips, and the idle raised as far as the
ECU allows without quieting 014, then put back.
**The cylinder 4 knock window stays out of this plan** (*owner's
decision, 9/10/2026*): with no link found between it and the misfires,
G66 and the rest of H5's tests stay in `open.md` as tests, not steps.

## Step 3 — why, and how it is read

**Idle solved → stop and record.** Otherwise each item decides whether
the next is needed.

**Item 5 — the can, and the tank after it.** The drives of 15/10, the
can and the warm gauge are done (`idle-log.md`, 15/10). **They are a
before, not an after**: a cleaner needs a tank's worth of driving to
act (*general*, and the maker's dose is one can per 30–50 l), so those
drives carry at most its first trace; the reading is item 6's. They
also stand as the captured drives item 5a wants before the map goes
back. **The display's `IdleHealth` runs only until the map goes back** (*owner's
decision*, 18/10/2026): from the reflash on, every drive is item 5a's
or 6's, captured, and `IdleHealth` is computed from the capture
instead. *It read "through both tanks after the can", which ran into
5a.*

**Item 5, the S18 drives** (*owner's request*, 18/10/2026; `open.md`
S18). The question S18 leaves is **whether cylinder 3 and the tick keep
coming back**. A flake of deposit loosened by the cleaner (H13) should
come back less and less and then stop. A lifter or valve (H1) should
not fade, and should be at its worst cold. So the reading is the run of
drives, not any one of them:
- **No tick and no code on several drives in a row, and no 014 burst
  above 72 while driving**: fading, which reads for the flake.
- **The tick back cold, again and again**: compression and a leak-down
  on 3, warm and cold, then a borescope at the seats (`open.md` S18).

**Why gently cold**: S18 first came on a cold engine, and a cold engine
is where a hanging lifter would show. **Why spirited driving warm**
(*owner's decision*, 19/10/2026): until then this read "up to about
4000 rpm, not full throttle to the limiter", set by the owner on 18/10
when more episodes were expected — full load on a valve that might not
be seating was the one case that risked more than a misfire (*reasoned,
not shown*). None came: four drives since the afternoon of 18/10, two
of them with full-throttle pulls (`39`, and 19/10 afternoon), no tick
and no lamp (S18). A cylinder that fires with no tick has nothing
holding a valve open, and hard driving keeps the chamber hot enough to
burn deposit off (*general*), which is what the cleaner is for. What
stays is the reaction to a warning: **a lamp that lights** means ease
off, and **a flashing lamp** is the misfire rate the
ECU treats as damaging to the converter (`vcds.md`, SSP 175), so the
engine stops rather than carrying on to home on three cylinders
(*owner's decision*, 18/10/2026). On 18/10 a restart after a few
minutes off brought all four back (S18).

**No tests at the car, and only four things written down** (*owner's
decision*, 18/10/2026). Pointing at one cylinder would not change what
comes next: H13 acts on all four, the dips sit on 3 and 4 with 1 and 2
better but not clean, and loosening the deposits is the cure for all of
them. The car is driven normally, to work as well, with no time to stop
and listen. So item 5 protects the engine and the converter, and keeps
only what costs nothing: when, what came before, the oil temperature
and `IdleHealth`. That is enough to see whether episodes follow hard
driving and the cleaner (deposits) or cold starts after a stand (a
lifter), and whether they fade. The screwdriver, the injector's
connector, the look in the dark and the videos were dropped; they are
in git history (*Read as* in `open.md` S18 keeps what each would have
told). **The fault memory is saved before it
is cleared** so that each drive starts from an empty memory and the
saved file keeps the code, its status and its count. **014 above 72
while driving** is the new mark: sixteen earlier logs never reached
it, and 18/10 read 270 and 351 (S18).

**Which VCDS groups, and why** (*decided 11/10/2026*, the owner's
question why 014/020/026 were in the gauge session): **026** belongs to
the knock window (S5) and reads its floor at idle, so it is dropped from
every idle-only step; **020** stays only where there is driving under
load, for cylinder 4's retard after the new leads (S4); **014** stays
where the clutch minutes or a stop are read for misfires. **001** joins
wherever there is idle — engine speed to align on and the lambda
correction in one group (`open.md` S1, *What VCDS saw just before a
dip*).

**003 is also the MAF's own figure** (*decided 12/10/2026*, the owner's
request after the airbox was sealed; `open.md` S9, *the cracked
airbox*): 12/10 held the idle on the least charge on record with 032's
idle cell at 0.0, which a MAF that used to over-read would explain, and
003 was not logged that day. So **every step with an idle logs 003**:
the gauge session read it cold, the same as the earlier cold starts minute by
minute (`idle-log.md`, 14/10), and 15/10 read it warm (row C there:
unchanged); item 6 logs it already.

**Item 5a — the original map** (*owner's decision*, 12/10/2026, to take
the remap out of the idle question; `open.md`, *The remap*). **The tuner
kept it, and was to write it back on 22/10/2026** (*owner*, 13/10).
**Postponed 20/10** (*owner*): the tuner agreed to email both files, the
original and the remap, so that they can be compared first — in a
private place, never in this repository, since they are the tuner's
and VW's. What a comparison can show (*decided*): where the two differ
and by how much; what each differing table *is* needs a map definition
for this ECU, so without one it is a guess from a table's shape and is
written as one. It also leaves the VW leads of item 6b as the only
change on the car, so they are read on their own. After the
gauge, so the gauge's reading stays on the car as it has been. **The can
goes in before it, straight after the gauge, and the two are knowingly
not told apart** (*owner's decision*, 13/10/2026: the aim is a healthy
idle, not knowing which change gave it). The captures of 15/10 between them
(item 5) keep a rough before for the map. **The adaptations start from
zero**: the ECU comes out of the car, which resets them as a battery
disconnect does (`refuted.md` C19, *owner*: already seen on this car),
so the tuner is not asked. Fresh adaptations look better on both
rulers (C19), so the reading is taken on the last of the drives and
against `30`–`32`. **The pull
in 4th** is for the converter, not the idle: the torque scale was fitted
by making this car's plateau reproduce the stock ratings
(`docs/firmware/can-decoding.md` question 8), so on a stock map the pull
says whether it still holds.

**The drive home, captured** (*owner's decision*, 18/10/2026). The
reflash resets the adaptations, which is the battery-off test of
`refuted.md` C19 that was refused on 6/10 as not worth a test of its
own — here it comes free. C19 says 014 stays at zero while 055's
learned idle air (field 3) sits above about −0.93 g/s and counts from
about −0.95, by time correlation only; so 055 is logged the whole way
rather than once at the end, with 014 beside it. **014 starting as
field 3 crosses −0.95** supports C19; starting elsewhere reopens it.
`IdleHealth`, computed from the capture over the same drive, says
whether the idle itself changes at that moment or only the counter.
003 keeps the idle advance for H14. The cold stop is the one fresh
adaptations have never counted on (C19), so it is the before; the car
will have stood for hours at the tuner (the flash transfer is slow on
this ECU, *owner*), so the start is a true cold one. **The brisk
driving** is what 4/10 A did before field 3 crossed; the stop at −0.95
puts an idle right on the crossing, and the one at home is the after
(*owner's decision*, 18/10/2026). **Whether field 3 learns while
driving or only at idle is not known here**, which is why it is read
at each stop as well. No `oilwatch.py`: no step on this drive waits
for an oil band.

**The tuner's files** (*owner's decision*, 18/10/2026). The ECU is read
on the bench through its pins, not over OBD, which gives the whole
flash: the program as well as the calibration. **The original against
the remap** says byte for byte what the tuner changed, so the map's
part in the idle can be read off the files rather than only off the
drives after 22/10: whether idle speed, idle advance, the overrun fuel
cut or **misfire detection** were touched. The last matters most — a
detection dulled by the remap would make 014 understate the engine on
every drive since, which is H14's other half (`open.md`, *The remap*).
**The whole flash, not only the maps**, because a maps-only file can be
diffed but not disassembled, and the program is where the CAN torque
reference behind 0x280 b7 lives (`docs/firmware/can-decoding.md`
question 8, measured, not read). **The read of the ECU as it is now**
shows that the remapped file he kept is the one that was in the car,
and the software version that the original belongs to this ECU, whose
part number VCDS reads as **06A 906 018 EJ**, Motronic (18/10/2026). **Not the EEPROM**: it holds the immobiliser and nothing this
needs. **Never in the repository, nor on its public release**: it is
Bosch/VW software, the same reason the VCDS label file is not kept
here; what goes into the repository is the summary of what changed.

**How the map is told from the can** (*added 16/10/2026*, when the remap
became `open.md` H14 at the owner's request). The drives after 22/10
carry the map, the cleaner and fresh adaptations at once, so they are
read on what the cleaner cannot move: **003's idle advance** against the
remap's 3.3° quiet (`open.md` S1, *What VCDS saw just before a dip*);
**the fuel cut on the overrun**, by `coastscan.py` on the captures,
against 0.8–1.6 s and 1,300–2,400 rpm; **014 against `IdleHealth`** —
one moving without the other is the detection's calibration, not the
engine; **014 under load**, new counts per `aktivováno` sample above
1500 rpm against 15 in about 4,300 on the remap (`open.md` H14 route 6,
whether the remap dulled the detection while driving); and **020 on the
pull**, cylinder 4's retard (S4), which is why
that one drive logs it. A calmer idle with the advance or the fuel cut
moved points at the map; with both where they were, at the cleaner or
the adaptations (H14 test 1). Nothing for the owner to do beyond 020.

**Items 5 and 6 — the engine left alone, and the additive** (*owner's
decision*, 10/10/2026). **The can goes in whatever the gauge shows**
(*owner's decision*, 12/10/2026): a leak and tired valves can both be
there at once (`open.md`, *The idle's candidates, ranked*), so a leak
found does not make the cleaner pointless. **After the gauge, not
before it** (*decided 12/10/2026*): the gauge's needle is the cleanest
reading of the valves there will be, and deposits the can moves would
move it — so the gauge first gives the before. After the gauge, unless it shows an intake leak
plainly, no more work on the engine for now: no new tools, nothing taken
apart, no garage. The one thing tried is an inlet-valve cleaner in the
fuel, because inlet-valve deposits (`open.md` H1, *Inlet-valve deposits*)
are the one candidate a can in the tank can reach. **Why this product**:
Liqui Moly states that it works through **polyetheramine (PEA)** and
that it suits every four-stroke petrol engine; PEA is the additive
chemistry aimed at inlet-valve and chamber deposits (*general*). The
"direct injection" in its name is not a restriction — on this engine
the injector sprays onto the back of the inlet valve, so fuel with the
cleaner in it washes exactly where port-injection deposits sit
(*reasoned*). **Dose and interval are the maker's**: 120 ml for 30–50 l,
and no sooner than every 5,000 km ("at the earliest", the maker's
wording on the retail listing), so it is **one treatment**, not a
course. **A course of two or three tanks if the first helps**
(*owner's decision*, 17/10/2026): deposits of a decade or more do not
come off in one tank (*general*), so a first sign is a reason to go on
rather than to stop. **It knowingly departs from the maker's interval**,
which gives no reason and no overdose data. *Reasoned, from the
chemistry*: the dose per litre stays the maker's, which is what does the
cleaning — twice the cleaner in one tank is not twice the cleaning; PEA
is ashless and metal-free, so the converter and the probes are not at
risk; **the oil is**: fuel and its additive reach the crankcase past the
rings, and an SAE study of PEA cleaners at high treat rates (SAE
2020-01-2100) found one PEA chemistry (PO-PEA) forming varnish and
sludge in the oil and another (BO-PEA) not — which one Liqui Moly uses
is not known. Varnish is also what sticks a hydraulic lifter, so it
would work against the cure. **Hence the oil change after the course**;
the oil is from 6/2026 anyway. Loosened carbon can lodge under a valve
for a while (*general*), so a rough patch during the course is read
against the next tank, not as a verdict. **The first tank read no
better** (17/10/2026, `idle-log.md`): loads off, `IdleHealth` 70–90 at
99 °C of oil, inside the 50–90 the display has wandered over since 12/10
and at its rough end. So **no second can** — the owner had already
filled without one — and **no oil change is owed to the cleaner**
(*decided 17/10/2026*): it was the price of a course, and one can at the
maker's dose is the maker's own use of it.

**Item 6a reopens the second can, for S18 and for the idle**
(*owner's decision*, 18/10/2026: the owner reads both as likely one
cause, deposits). If S18 is deposits (H13), the cleaner
is what loosens them, and a second tank may finish the job. Hard
driving on plain fuel may do some of the same, and the plain tanks
show how much. **Not before the map, and not on item 6's tank**: the
map goes back on 22/10, and item 6 reads what it did. A can in that
tank would change two things at once and leave the reading with no
answer. **Episodes on the cleaner's tank are expected, not a verdict**:
under H13, each tank sheds another layer, so a tick or a 014 burst
there is the same process. Under H1 the tick would not depend on which
tank is in. **The oil and filter are changed after the second can's
tank** (*owner's decision*, 18/10/2026): not all of what the cleaner
loosens leaves through the exhaust, and the varnish risk above is on
the oil side. The filter holds particles, not what is dissolved or
finer than its mesh (*general*), so only the change takes it out. Not a verdict on the can
either: that stays item 6's reading, below. **The usual fuel, OMV MaxxMotion 100**, so that the can is the
only thing that changes. **How it is
read**: the drives of item 6 against `30`, `31` and 14/10's gauge session (`33`, `34`) —
014 by stop and `IdleHealth` by oil band (`open.md` S1, S3), adaptations
settled (the battery stays on, `refuted.md` C19 — except the reset on
22/10, item 5a, so the drives just after it read low on 014 for a
reason that is not the can). Better → deposits had
a part; the same → H13 loses its inlet-valve half, and Claude picks from the
ranked list. A tank is weeks of this car's driving, so the reading is
late by design. **`IdleHealth` off the display is the running reading in
between** (*the owner's point*, 10/10/2026) — the one instrument that
needs neither the laptop nor a capture. Read like with like or not at
all: it moves with the oil (S1, *Temperature matters*), and **loads
lower it on their own** — lights, blower and A/C took it from 70–80 to
35–50 (S1, 26/9) — so winter's habit of running them would pass for the
additive working. *Superseded 19/10/2026 by the two states of the standing items, all
loads off against all on; what follows is the reasoning that held
until then.* **Loads off, then, for that one minute** (*decided
10/10/2026*, the owner's point that the baseline already exists): the
captured hot stops on settled adaptations are loads-off — `30` and `31`
`IdleHealth` 77–89 at 93–111 °C (S1's table),
and 14/10's gauge session adds one more — so no readings are needed before
the can. **The lights are the exception** (*owner*, 15/10/2026): the
car runs them all the time, so they are on in every captured baseline
(`test/fixtures/README.md` lists headlights throughout) and stay on for
the reading; "loads off" means everything else. A minute without loads is the price, against the standing rule
for the converter, accepted for one stop a drive. It needs about half a
minute of settled idle before it reads at all (255 until then,
`docs/firmware/frames.md`) and wanders from window to window, so a
direction needs several readings, not one. **Where it sat and the lowest
it touched, both** (*owner*, 15/10/2026: the minima are what he
watches): a minimum is a signal, but on a grade that wanders it keeps
falling the longer one watches, so on its own it would make long stops
look better than short ones; beside the level it sat at, it does not. Not a test of anything else, and it decides nothing on
its own about a lifter.

**Item 6b, the refit** (*owner's decision*, 20/10/2026): the look of
19–20/10 is done (`idle-log.md`). Lead 2 tore on removal, so the leads
are replaced, and with them the plugs: **VW originals**, the swap H15
was waiting for, decided on 9/10 and not done then. ⚠ **The leads are
only at VW's central store**, so both arrive on 21/10 (*owner*, 20/10;
the plugs were in stock, but he wants the two together): the set goes
in the day before the map of 22/10, or that morning, and a change in
the idle then could not be given to one of them alone. **The map was
then postponed** (item 5a), so the leads and plugs are read on their
own after all. **What is recorded at the refit, and why** (*decided*,
20/10/2026): H15 rests on how the NGK ends sat on these plugs — by
grip 2 > 1 > 3 ≈ 4, a rubbery click with a faint metallic one (`open.md`
H15) — so the old ends are measured (the clip's inner diameter; length
and resistance per lead, an outlier against the others being the sign,
whether the set's resistance is in the core, rising with length, or
fixed in the ends) and the VW ends are described the same way, cylinder
by cylinder, against them. The first warm drive's two-state
`IdleHealth` is the first reading of the change (`open.md` S1, *When S1
closes*).

**Item 6 — the drives** (*decided 10/10/2026*, before the additive was; they now come after it). The first drive after the new
   plugs and leads put the dips at a quarter of pairs on one slot — 10
   of 39, 26 %, against 34 of 103, 33 %, on 9/10 — while 014 counted as
   before (`open.md` S3, *The drive after the new leads*). One drive
   cannot tell those apart; two or three more, pooled, can, and they
   cost nothing. **How it is read** (*since 17/10/2026*): `cutscan.py
   --shares` on the idles, alone and pooled since the last repair — the
   share the top two carry and p against all four alike (`open.md`, *One
   cylinder or two*: two neighbours with two thirds, 3 and 4 on `31`); a
   capture with cuts in it also `--name`. *This read "`--pairs` ... near a
   quarter / back toward a third", on the short runs whose pair shares
   turned out high.* 014 by
   stop and `IdleHealth` by oil band against `open.md` S1 and S3. **The
   groups**: **014** is the reading; **003** the idle air, which says
   whether anything sealed or opened; **055 once**, at the end on a
   warm idle (*owner's choice*, 10/10/2026): still near −1.1 to −1.3
   says the adaptations are settled and the comparison holds
   (`refuted.md` C19). **020** stays on as a third group, data and not a
   step: on 10/10 cylinder 4's retard nearly vanished with the new
   leads (`open.md` S4), and more drives say whether it holds. **026 on
   the next drive** (*owner's decision*, 10/10/2026), to see whether
   cylinder 4's high knock-sensor reading (S5) went with lead 4 too;
   VCDS takes three groups, so 003 sits that drive out (*decided*): its
   idle air was 3.08 g/s on 10/10, the baseline is set, and the idle is
   still read off 014 and the capture.
**Item 6's hard run** (*owner's request*, 14/10/2026: to bring back the
drive after which the misfires once came). On 4/10, on fresh
adaptations, 014 counted only at the stop after a hard drive, 7–9 a
minute, and at no gentler stop (`open.md` S3, *Session A after step
1b*); since 9/10, on settled ones, it counts at every warm stop
anyway, so the run says less than it would have then. What is read is
**the stop after it**, not the run: under load 014 has almost never
counted on this car. **After 22/10**, so that the run's heat is not
mixed into the can's reading and so that it is on the original map;
no harm to the engine or to the cleaner (*general*: the cleaner is
made for ordinary driving, motorways included). **The belt** is the
one part that sustained high revs load harder, and at 9 years its
age, not its 27,800 km, is what to check against VW's interval, which
this repository does not hold (`vehicle-history.md`). The legal limit
caps it: minutes at 5000 rpm in top gear are well past 130 km/h, so
brisk at the limit plus full pulls is the run.

**Item 7 — the exhaust ahead of the front probe (H2), warm** (*reasoned*,
   9/10/2026): `open.md`'s first candidate when this was written (**fourth since 12/10**, when the dips came back on one slot and the cold test found nothing) (since 9/10 second, behind H3, now that the dips keep to one cylinder — but still the one with symptoms of its own), and next now that 2b moved nothing on
   the intake side, and free (S15, which first made it urgent, closed
   12/10 with the joint behind the converter, and S11's hiss the same
   day; what is left for it is S2's puff). With the outlet closed, a leak that draws air in at idle blows
   out, and hisses or puffs. Warm, because a crack in cast iron may only
   open hot; never longer than a few seconds and never indoors
   (*general*) — **but cold first** (*decided 9/10/2026*): the owner
   hears S15 cold too, so a leak that sputters cold can be found cold,
   and the drive is needed only if cold finds nothing. **Cold found
nothing, 12/10/2026** (*owner*, `idle-log.md`): no hiss or puff at any
closure, above or below, only the exhaust being throttled — so warm is
what is left, if Claude asks for it after item 6. The owner works
   alone, so the phone listens at the manifold while he closes the
   tailpipe, and his "teď" marks each closure on the audio. Claude
   cannot hear the recordings (and this laptop cannot decode a phone's
   audio), so the owner listens back and reports; each closure
   also loads the engine and shows on the capture as a dip in engine
   speed, which places it in time but says nothing about where a leak
   is. **The joints cannot be told apart by ear** — they cannot be
   reached (*owner*, 9/10/2026) — so the sound only says engine bay or
   underbody, and **the photographs do the locating**: an exhaust leak
   leaves a black soot trail where it blows out (*general*), and a
   photograph outranks every other source here. **The manifold and its
   joint to the head sit under the heat shield** and cannot be seen or
   photographed (*owner*, 9/10/2026), so the photos cover only the flange
   and the pipe below it. **Photographed 12/10/2026, cold, before the
   test** (*owner*; `idle-log.md`): the joint to the front pipe and
   cylinders 3 and 4's pipes from below; no clear soot trail in Claude's reading of them. **How it is read** (*decided 9/10/2026*): soot
   below → that joint; louder from the engine bay with nothing below →
   the manifold or its joint to the head, which is the owner's standing
   decision of a new manifold (3/10/2026), the shield coming off then
   anyway; nothing either way → warm, then a garage with a lift. The front pipe as far as the converter is listened to as
   well — a new manifold answers only a leak in the manifold. A new manifold if it leaks (*owner's decision*,
   3/10/2026); the suffix differs by model and year; the studs into the
   head are 26 years old. **Nothing leaks ahead of the probe** → H2 is
   refuted for its zone and goes to `refuted.md`.
**The stop cuts in item 5a** (*owner's decision*, 17/10/2026; `open.md`,
*One cylinder or two*). **They replace item 7's injectors 1 and 4**,
whose reasoning stays below for the criteria. Since 17/10 the cylinder
phase holds for minutes at idle, so one cut names every dip in the idle
run it sits in, up to the moment the car moves (`cutscan.py --name`);
it does not reach across driving, so each stop needs its own cut. One
cut of 30 s is enough to fix the slot (`31`'s cuts held it through 430
s); the 3 minutes after it are what is named, about 20–40 dips a stop,
so two or three stops give more named dips than all of `31`. After the
map, because the question is whether the dips are still on **3 and 4**
on the stock map and the cleaner: the same pair → the map was not what
weakened them, and the hypotheses that act on that pair (`open.md`, the
ranked list) stand; a different pair, or all four alike → the map or
the cleaner moved it. Injector 1 rather than 4 so that the suspect
cylinder runs throughout. Read with `--name` on each stop and `--shares`
pooled.

**The loom at one stop** (*owner's decision*, 17/10/2026; `open.md` H4
row, H7 test 3). What is left of the electrical side is the injector
loom where it runs to 3 and 4 — one section for the two, taped and
oily in the photograph of 26/9. A contact that breaks for a moment
drops or shortens one injection, which the ECU does not see (it knows
what it commanded, not what the injector did). **It goes after the
stop's 3 untouched minutes and before the car moves**, so the run the
cut named is still unbroken and every dip during the flexing is named
too; the minutes are timed from injector 1 going back on because that
moment is in the capture, which a message in the chat is not. **Read**:
dips on 3 a minute with the hand at 3, against the minutes either side,
and the same for 4. A clear rise on the cylinder under the hand → that
loom; nothing → the loom is cleared as far as a hand can clear it.

**Item 7 — injectors 1 and 4 again** (*superseded 17/10/2026 by the
stop cuts above*; *the owner's proposal, 9/10/2026*; `open.md`,
   *Naming the cylinder*). It is also `docs/firmware/open.md` question
   11's deliberate misfire, brought forward at the owner's decision the
   same day. With a connector off, that cylinder gets no fuel, so the
   converter sees air and not fuel (*general*); the light comes on because
   a quarter of the firings missing is far above the 2 % VW stores a code
   at (`vcds.md`, *What VW says*), and the rate that damages a converter
   flashes it (SSP 175) — VW does not publish this ECU's figure.
   - **Why it can name a cylinder at all.** The idles already show the
     dips not shared alike (`open.md`, *The dips keep to one slot*),
     but the bus cannot say which cylinder a slot is. *Since 17/10/2026
     the cut also names the idle around it*: the phase now holds for
     minutes (`open.md`, *One cylinder or two*), so `cutscan.py --name`
     names every dip in the run the cut sits in — on `31`, 4 and 3. While a cylinder is
     out its slot is known, and the firing order 1-3-4-2 names the other
     three: **cutting 1 names 3, 4 and 2; cutting 4 names 2, 1 and 3.** So
     the two outer cylinders name all four, and 2 and 3 are named by both
     cuts — the two must agree about them, which is the check.
     (*Decided 9/10/2026*, the owner's question: 2 and 3 are hard to
     reach, and they are not needed.) The one assumption, stated rather
     than proved: a dip shows in its cylinder's slot with the same lag as
     the dead stroke's deficit.
   - **Why up to three days.** The idles put roughly 45 % of the dips on
     one cylinder (or 40 % each on two neighbours in the firing order),
     about 1.8 times its share — a real effect but not a large one, so it
     takes many dips. Simulated with `tools/cutscan.py` at 6–10 dips a
     minute (*decided 9/10/2026*): the named cylinder comes out right in
     0–47 % of trials on one day's four cut-minutes, 25–83 % on twelve,
     and 58–92 % on all four cylinders for sixteen; a cylinder carrying
     three quarters or more is found on one day. Three days of 1, 4, 4, 1
     are twelve cut-minutes without any one idle growing past about
     7 minutes, which keeps to the rule. The days are pooled.
   - **`tools/cutscan.py` reads the whole test**, all days together: it
     finds the cuts in the capture, counts, applies the rules below and
     prints the verdict; it stops rather than guess if it finds a
     different number of cuts than the order names.
   - **The criteria, fixed before the test** (*decided 9/10/2026*, so the
     result cannot be read to fit; *revised the same day*, before any
     run, when the dips were found to keep to one slot — the earlier
     version compared the cuts with each other first, which simulation
     showed would find a 45 % cylinder only 14–28 % of the time):
     1. **By name — the main reading.** Dips counted on the three firing
        cylinders, named from the dead slot, the first 5 s of each cut
        out; each a stroke 20 rpm below its own cylinder's neighbours.
        **One cylinder** if its rate is the highest at p < 0.05 against
        every cylinder alike (an exact multinomial on the counts, given
        their total and each cylinder's strokes), **and** it is the
        highest in both halves of the pooled cuts.
     2. **Air — a steadily weak cylinder.** 003's air over the last 40 s
        of each cut, its ignition angle beside it (the idle control uses
        both). **Weak** if one cut needs **≥ 0.15 g/s less** than the
        other, in both halves — about 10 % less work from that cylinder
        (*reasoned*: cutting a healthy one needs ~1.1 g/s more, a 10 %
        weaker one ~0.14 g/s less than that). Only 1 and 4 can be weighed
        this way.
     3. **No cylinder stands out** if the named rates give p > 0.2 after
        three days. That rules out one carrying three quarters or more,
        **not a smaller share**, and it is recorded that way.
     4. **Anything between is undecided** after three days — not a reading
        stretched to fit. The cuts compared with each other are printed
        as a secondary reading and decide nothing.
   - **What each outcome points at:** a cylinder named → that cylinder:
     its plug and lead, its injector, its runner (H3), its valves (H1);
     air weak too → a steady fault there (a valve, a runner leak) rather
     than an intermittent one; nothing → the whole engine (H0, H2, H4,
     H7, H8).
   - **The names hold only while a cylinder is out.** The bus loses the
     cylinder phase every few seconds — whenever two strokes quantise to
     the same 0.25 rpm (`idledips.cylinder_runs`; on `30` the phase held
     a median 3 s, at most 16 s). So they cannot be carried into the
     four-cylinder minutes or into earlier captures. *Corrected 9/10/2026*:
     this said the names would hold "in this capture and every earlier
     one".
   - **Done warm, by hand, on 10/10/2026** (*owner*): gloves were enough,
     so the dry run and the cold fallback planned for it are dropped.
     The connectors are taken by the body because the harness is 26
     years old (`open.md` H7 test 3). The plug lead of a cylinder is
     **never** pulled instead: that sends fuel to the converter.
   - **A cut may be 30 s** (*owner*, 10/10/2026, with 014 reading high):
     the counts are per stroke, so a shorter cut costs strokes and not
     the method.
   - Question 11's own reading — 014 and `IdleHealth` against a misfire
     of known rate — comes from the same minutes.
   **Day 1, 10/10/2026** (`open.md`, *Naming the cylinder*): no
   cylinder stands out (p = 0.28), neither 1 nor 4 weak by air, on
   twenty dips. **Not repeated unless item 6's drives bring the dips back to one
   slot** (*decided 10/10/2026*): the test exists to name the cylinder
   the dips keep to, and on the same drive they kept to none. **On
   12/10 they were back on one slot**, 46 of 121 pairs, 38 %, p = 0.0011
   (`open.md`, *Naming the cylinder*) — so the cuts are back in play;
   item 6's drives confirm it first, since they are captured anyway.
**Item 7 — the high-voltage side** (`open.md` H4 test 1e, *decided 9/10/2026*):
   the roughest reading on record came on a foggy morning (S1), and the
   moisture a tracking boot or coil needs is what the mist supplies.
   The plugs and leads are new (10/10) and the coil is from 6/2026,
   which is why it is late in the order; it is free.
**Item 8 — the next repair** is chosen then, not now, from `open.md`'s ranked
   candidates.

## Standing items — why

- **Every drive, for the converter** (*the owner's question*, 10/10/2026;
  all from this car's data): **122 of 129 counted misfire events began
  at a standing idle** and almost none under load (`open.md` S3), so the
  converter's exposure is standing idle, cold warm-ups included — 014
  counts on the cold idle too since 9/10. **Loads on smooth it**: lights,
  blower and A/C took `IdleHealth` from 70–80 to 35–50 (S1, 26/9), and a
  dip is likelier the moment the charge falls (S1, *What comes before a
  dip*), so anything that adds charge at idle — an electrical load or a
  little throttle — helps. **After a hard drive** session A counted at
  every stop where gentle warm-ups had not (S3, 4/10). **A flashing
  lamp** is the ECU's own converter-damage rate (SSP 175, `vcds.md`);
  this car's idle counts sit below even the 2 % that stores a code, so a
  flash means something new.

- **`IdleHealth` in two states** (*owner's decision*, 19/10/2026;
  `open.md` S1, *Since the cleaner*): since the cleaner's tank the
  partial loads seem to make little difference, now and then the
  opposite, and only everything on together still calms it (*owner*).
  So "loads off but the lights" is replaced: one state is loads off
  and the other is all of them on, which leaves nothing between them
  to argue about. The lights were kept on because the car runs them
  all the time (15/10), but they can be switched off in the dark
  (*owner*), so they go off where they can. **Why two minutes each**:
  on a steady warm idle, neighbouring 2-minute windows of `IdleHealth`
  differ by 4–18 (standard deviation, `24`, `26`, `28`, `30`, `32`,
  `37`), and minute windows wander more. So one pair shows only a
  large difference, about 25 or more. **Pairs pool over drives**, which
  is what an hour's idle in one place would otherwise be. In a capture
  the switch is visible in b7, which jumps with the load, so the states
  need no timing in the chat. Four minutes standing is accepted against
  the converter rule above (*owner*).
- **The cover's nuts**: the gasket settles (`open.md` S10).
- **The thermometer reading (A4)**: `docs/firmware/open.md` question 10.
  The ignition goes back on so the capture keeps 0x420. The coolant hose
  checks the instrument against 0x288's coolant.
