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

5. **The can is in (15/10). Drive the tank as usual**, captures or not.
   - **`IdleHealth` off the display, through both tanks after the can:**
     on drives where the oil reaches **95–100 °C** on the display, at one stop of **at
     least a minute with every load off but the lights**, which stay
     on. Write into the chat: date, oil temperature, **where
     `IdleHealth` mostly sat and the lowest it touched**.
5a. **22/10: the original map written back** at the tuner; the ECU
   comes out of the car. Then **two or three ordinary warm drives**:
   Claude runs the capture; VCDS on **014, 003**; 055 once at the end,
   warm idle; on one of them **one held full-throttle pull in 4th**,
   with VCDS on **014, 003, 020** for that drive.
6. **On the next tank: two or three ordinary drives, warm**, on
   different days. Claude runs the capture; VCDS on **014, 003, 020**;
   055 once at the end, warm idle. Write the stops.
   - **On one of them, a hard motorway run**: a few minutes brisk at
     the limit, two or three full pulls, then **a warm stop of a few
     minutes** with loads off. Before it: the timing belt's interval
     checked against its date (10/2017).
7. **Only if Claude asks after 6:**
   - **The exhaust test again, warm**, after a drive to 95–100 °C of oil.
     **Leaks there → a new manifold**: new gasket to the head, new nuts,
     new outlet gasket, the probe refitted with anti-seize. Part
     `06A 253 031` + suffix: read the number cast into the manifold, or
     ask by VIN. New from VW about €350–490, used 700–1,500 Kč.
     Penetrating oil on the studs the days before; a snapped stud goes
     to a garage.
   - **Injectors 1 and 4 again, warm idle** — as on 10/10: oil at
     95–100 °C, neutral, handbrake on, loads off; Claude runs the
     capture, VCDS on **014, 055, 003**; 1 min as it is; **1, 4, 4, 1**,
     each connector off **1 min** (30 s at the least) and back on for
     **30 s**, by the connector body with the clip pressed, gloves; 1 min
     as it is, engine off. Write every off and on into the chat; a
     flashing lamp is expected. Clear the fault memory with VCDS.
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
group 014). So:

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
back.

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
kept it, and writes it back on 22/10/2026** (*owner*, 13/10). After the
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

**How the map is told from the can** (*added 16/10/2026*, when the remap
became `open.md` H14 at the owner's request). The drives after 22/10
carry the map, the cleaner and fresh adaptations at once, so they are
read on what the cleaner cannot move: **003's idle advance** against the
remap's 3.3° quiet (`open.md` S1, *What VCDS saw just before a dip*);
**the fuel cut on the overrun**, by `coastscan.py` on the captures,
against 0.8–1.6 s and 1,300–2,400 rpm; **014 against `IdleHealth`** —
one moving without the other is the detection's calibration, not the
engine; and **020 on the pull**, cylinder 4's retard (S4), which is why
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
and no sooner than every 5,000 km, so it is **one treatment**, not a
course. **The usual fuel, OMV MaxxMotion 100**, so that the can is the
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
additive working. **Loads off, then, for that one minute** (*decided
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
**Item 7 — injectors 1 and 4 again** (*the owner's proposal, 9/10/2026*; `open.md`,
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

- **The cover's nuts**: the gasket settles (`open.md` S10).
- **The thermometer reading (A4)**: `docs/firmware/open.md` question 10.
  The ignition goes back on so the capture keeps 0x420. The coolant hose
  checks the instrument against 0x288's coolant.
