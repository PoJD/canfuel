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

**The engine runs once before the vacuum gauge is here — for item 1 —
and otherwise not until it is.** Then one at a time; Claude says after
each whether the next is needed. Claude runs the capture on every drive.

1. **The joint behind the converter, made tight, then the exhaust test,
   cold.**
   - Measure both pipes' outside diameters; write them into the chat.
   - Connector off. A strip of thin sheet, **about 0.4–0.5 mm,
     stainless, not galvanised**, as wide as the connector's grip on
     the narrower pipe, wrapped round it as far as it goes, a small gap
     at the ends.
   - A thin coat of exhaust sealant on the pipe under the strip and on
     the strip under the connector. Pipe ends as close together as they
     go.
   - Connector on, bolts tightened in turn, evenly. Nothing may move.
   - Look at the exhaust's rubber hangers: nothing pulling the joint
     sideways or letting it sag.
   - **Cold start.** Claude runs the capture; VCDS on **014, 020, 026**.
   - **The exhaust test**, straight after the start:
     - Phone recording, laid in the engine bay by the manifold; later
       under the car by the front pipe.
     - At the tailpipe, **say aloud "teď"** and close it for **2–3 s**,
       never longer. Five times, a few seconds apart.
     - Move the phone under the car by the front pipe and do the five
       again.
     - Then, tailpipe open, say whether the sputter (S15) is louder
       **from above in the engine bay or from under the car**, and
       whether the joint behind the converter is heard.
   - **A short drive** to warm the exhaust, then home, engine off.
   - **Play both recordings back yourself** and write whether a hiss or
     a puff comes up at each "teď", and on which recording.
   - **Cold again (the next morning will do):** the connector's bolts
     tightened once more; **photograph from below** whatever the phone
     reaches — the flange under the manifold, the front pipe back to the
     converter, the probe if it shows. **Black soot streaks** at a joint
     mark a leak. The manifold itself is under its heat shield: leave
     it. Write whether the joint was heard on the drive.
2. **When the gauge is here: the gauge, cold.** No driving with the
   gauge on.
   - **Before, engine cold and off:** tee the gauge into the fuel
     pressure regulator's vacuum hose. Short hose to the gauge, tight
     T-piece. Lay the gauge clear of the belt and the exhaust.
   - **Start it.** Claude runs the capture; VCDS on **014, 020, 026**.
     Film the gauge **30 s** straight after the start, then **1 min**
     more.
   - **Then 2500 rpm, held by hand, 15 s**, filming; let it fall back
     and film **15 s** of idle. Engine off.
   - **Gauge off**, the regulator's hose back on its own, pushed fully
     home.
   - **Write, from the films:** the number the needle sits at, in the
     dial's own units, at idle and at 2500; **how many times it flicked
     down in the 1 min of idle**; whether the flicks come singly or a few
     in a row; whether they are still there at 2500.
3. **Only if the needle showed nothing cold: the gauge warm.**
   - A drive to 68–72 °C of oil, as on 10/10. Claude runs the capture;
     VCDS on **014, 020, 026**. A few stops at a warm idle, a minute or
     two each. Write the stops.
   - Back: engine off, tee the gauge in as before.
   - Start, film the gauge **1 min** at idle, then **2500 rpm 15 s** and
     **15 s** of idle again. **055 read once.** Engine off, gauge off,
     hose back on.
   - **Write** the same four things as in 2.
4. **No clear intake leak in 2 or 3 → the engine is left alone.** Low
   and steady at idle only → Claude says the next step instead.
5. **One can of Liqui Moly *DFI Cleaner* (= *Pro-Line Direct Injection
   Cleaner*, 120 ml)** into the tank, then fill **30–50 l** of the usual
   OMV MaxxMotion 100. Drive the tank as usual. Battery stays connected.
   - **`IdleHealth` off the display, through both tanks after the can:**
     on drives where the oil reaches **68–72 °C**, at one stop of **at
     least a minute with every load off**. Write into the chat: date,
     `IdleHealth`, oil temperature.
6. **On the next tank: two or three ordinary drives, warm**, on
   different days. Claude runs the capture; VCDS on **014, 003, 020**;
   055 once at the end, warm idle. Write the stops.
7. **Only if Claude asks after 6:**
   - **The exhaust test again, warm**, after a drive to 68–72 °C of oil.
     **Leaks there → a new manifold**: new gasket to the head, new nuts,
     new outlet gasket, the probe refitted with anti-seize. Part
     `06A 253 031` + suffix: read the number cast into the manifold, or
     ask by VIN. New from VW about €350–490, used 700–1,500 Kč.
     Penetrating oil on the studs the days before; a snapped stud goes
     to a garage.
   - **Injectors 1 and 4 again, warm idle** — as on 10/10: oil at
     68–72 °C, neutral, handbrake on, loads off; Claude runs the
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
the dips no longer keep to one cylinder's stroke.
**The cylinder 4 knock window stays out of this plan** (*owner's
decision, 9/10/2026*): with no link found between it and the misfires,
G66 and the rest of H5's tests stay in `open.md` as tests, not steps.

## Step 3 — why, and how it is read

**Idle solved → stop and record.** Otherwise each item decides whether
the next is needed.

**The engine runs for item 1 and otherwise waits for the vacuum gauge**
(*owner's decision*, 10/10/2026; the gauge is MAR-POL `M57673`, ordered
10/10, `open.md` *Tools worth owning*). **Item 2 is the gauge alone**,
on a cold start of its own (*owner's decision*, 10/10/2026, replacing
the plan of one session for the gauge and the exhaust test together:
the exhaust test moved to item 1, with the joint). **The gauge is read cold first, and warm
only if cold shows nothing; it is never on during a drive** (*owner's
decision*, 10/10/2026, replacing the same day's plan of one session with
the gauge left on through the drive). Cold is not the cleaner reading —
a cold idle runs raised and enriched, which moves the needle for reasons
of its own, and the warm idle is where 014 counts at the stops
(*general*) — but S1 is roughest cold, and a valve that flicks the
needle (H1) or a leak that drags it low (H3) is there cold too. So a
clear result cold is enough; a quiet needle cold leaves the warm idle,
which item 3 reads on a drive that is captured anyway and so counts as
one of item 6's. Filmed rather than watched, because a flick at idle
comes several times a second and a video can be stepped through.

**Item 1 — the joint first, then the exhaust test** (*owner's
decision*, 10/10/2026: the joint and the test together, the gauge on its
own when it comes; `open.md` S6, reopened; the method *general*). The joint rattles again, and a
leak behind the converter lets the closed tailpipe's pressure out there,
so the manifold ahead of the probe is barely tested, and its noise
drowns the sputter (S15) the phone is listening for — so the joint
comes first and the test straight after, on the same cold start. The
short drive is the shim's first heat cycle, after which the bolts are
tightened again. **The shim**: about 54.2 mm in a 55 mm connector is
about 0.4 mm a side, so a strip of that thickness takes up the play; a
thicker one keeps the connector from closing evenly. Stainless because
plain steel rusts out and galvanised sheet gives off zinc fumes when the
exhaust is hot. Sealant thin, so the connector grips metal and not a
layer of paste. Retightened after one heat cycle because the sealant
and the sheet settle. **How it is read**: not heard after the drive →
S6 closes again; heard → the hangers, then a welded joint at an exhaust
shop.

**Items 4 to 6 — the engine left alone, and the additive** (*owner's
decision*, 10/10/2026). After the gauge, unless it shows an intake leak
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
read**: the drives of item 6 against `30`, `31` and item 2's session —
014 by stop and the grade by oil band (`open.md` S1, S3), adaptations
settled (the battery stays on, `refuted.md` C19). Better → deposits had
a part; the same → H1's deposit branch loses, and Claude picks from the
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
grade 1.53–1.77 rpm at 67–80 °C (S1's table; `IDLE_ROUGH_100` is 2.00),
and item 2's session adds one more — so no readings are needed before
the can. A minute without loads is the price, against the standing rule
for the converter, accepted for one stop a drive. It needs about half a
minute of settled idle before it reads at all (255 until then,
`docs/firmware/frames.md`) and wanders from window to window, so a
direction needs several readings, not one. Not a test of anything else, and it decides nothing on
its own about a lifter.

**Item 6 — the drives** (*decided 10/10/2026*, before the additive was; they now come after it). The first drive after the new
   plugs and leads put the dips at a quarter of pairs on one slot — 10
   of 39, 26 %, against 34 of 103, 33 %, on 9/10 — while 014 counted as
   before (`open.md` S3, *The drive after the new leads*). One drive
   cannot tell those apart; two or three more, pooled, can, and they
   cost nothing. **How it is read**: `cutscan.py --pairs` on the idles,
   outside any cut, pooled with 10/10's — still near a quarter → the
   one-cylinder share is gone, and what 014 counts acts on the whole
   engine; back toward a third → item 7's cuts name the cylinder. 014 by
   stop and the grade by oil band against `open.md` S1 and S3. **The
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
**Items 1 and 7 — the exhaust ahead of the front probe (H2)** (*reasoned*,
   9/10/2026): `open.md`'s first candidate when this was written (since 9/10 second, behind H3, now that the dips keep to one cylinder — but still the one with symptoms of its own), and next now that 2b moved nothing on
   the intake side, the one with a symptom of its own since S15 was
   heard, and free. With the outlet closed, a leak that draws air in at idle blows
   out, and hisses or puffs. Warm, because a crack in cast iron may only
   open hot; never longer than a few seconds and never indoors
   (*general*) — **but cold first** (*decided 9/10/2026*): the owner
   hears S15 cold too, so a leak that sputters cold can be found cold,
   and the drive is needed only if cold finds nothing. The owner works
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
   and the pipe below it. **How it is read** (*decided 9/10/2026*): soot
   below → that joint; louder from the engine bay with nothing below →
   the manifold or its joint to the head, which is the owner's standing
   decision of a new manifold (3/10/2026), the shield coming off then
   anyway; nothing either way → warm, then a garage with a lift. The front pipe as far as the converter is listened to as
   well, and the sputter with the tailpipe open, because S15 may sit just
   behind the manifold rather than in it (`open.md` S15) — a new manifold
   answers only a leak in the manifold. A new manifold if it leaks (*owner's decision*,
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
     dips keeping to one slot (`open.md`, *The dips keep to one slot*),
     but the bus cannot say which cylinder a slot is. While a cylinder is
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
   the dips keep to, and on the same drive they kept to none.
**Item 7 — the high-voltage side** (`open.md` H4 test 1e, *decided 9/10/2026*):
   the roughest reading on record came on a foggy morning (S1), and the
   moisture a tracking boot or coil needs is what the mist supplies.
   The plugs and leads are new (10/10) and the coil is from 6/2026,
   which is why it is late in the order; it is free.
**Items 2 and 3 — how the gauge is read** (`open.md`, *Tools worth
owning*, and H1 test 5). Everything here is *general* — the classic
readings of a manifold vacuum gauge — and none of it is VW's figure
for this engine. **Read the needle against itself**, never against a
number from a book: the absolute level also depends on altitude and the
weather.

- **What a flick is.** At idle each cylinder draws on the manifold once
  per cycle, about 6–7 times a second per cylinder at 780 rpm, so a
  healthy needle sits still or trembles evenly. A cylinder that does
  not draw its share — a valve not closing, or a firing that failed —
  shows as **a quick dip of the needle and back**, a fraction of a
  second. That is why it is filmed: a phone at 30 frames a second can
  be stepped through, an eye cannot.
- **A flick is any misfire, not only a valve.** Whatever makes a
  cylinder miss — a valve, a spark, a lean runner — flicks the needle
  the same way. **So the count is first compared with the dips**: the
  capture runs under the same minute, and if the needle flicks about as
  often as the engine speed dips (S1: 5–15 a minute warm), the gauge is
  seeing the misfires themselves. The 2500 rpm hold is also the marker
  that lines the film up with the capture.
- **Flicks at idle that are gone at 2500 do not separate the causes**
  (*corrected 10/10/2026, the owner's point*: this table first read a
  flick that stays at 2500 as H1's sign). Nothing on this car has ever
  misfired under load: with detection `aktivováno` while driving, 014
  started counting about once per 250 samples, against several a minute
  at idle (`open.md` S3, *Off idle, by detection state*). A 2500 rpm
  hold in neutral is light load, where 014 is mostly `deaktiv.` and the
  bus is too noisy to see a misfire, so **the gauge is the only thing
  that reads it there** — and flicks gone at 2500 is still the expected
  reading **for every hypothesis, H1 included**: a hydraulic lifter has
  least oil pressure behind it at idle (*general*).

| what the needle does | reading | for |
|---|---|---|
| **steady at idle**, the level normal for itself, rises a little at 2500 and steady there | no valve fault, no large leak; the dips are too small for the gauge to see | H0, or a fault the gauge cannot reach |
| **an occasional sharp flick down** at idle, irregular, gone at 2500 | the misfires themselves — a hanging valve, a spark, a lean runner all look alike here | S3 confirmed; **names nothing** |
| the same flicks **still there at 2500** | something that misfires off idle too, which nothing on this car has done before | new; a valve (H1) first |
| **a regular flick on every cycle**, same size each time | one valve that never seals (burnt, bent) — unlikely with even compression | H1, a worse form; leak-down next |
| **low and steady at idle**, normal-ish at 2500 | air in behind the throttle | H3 |
| **low and steady at idle and at 2500 alike** | a late cam — the belt a tooth out — or an exhaust restriction | the belt (ranked 8) |
| **a fast, even flutter** that gets worse at 2500 | weak valve springs, or worn guides if it steadies with speed | H1, the springs and guides |
| **slow wandering** up and down over seconds, at idle | mixture or idle control hunting | H8, H7 |

**What follows from it:**

- **What the gauge can and cannot say about H1.** It points at the
  valvetrain only through the rarer readings — a regular flick, a fast
  flutter, flicks that stay at 2500. **An intermittent flick at idle
  alone cannot tell a hanging valve from any other misfire.** H1 is
  then answered by the tests aimed at it: the stethoscope over each
  lifter at a warm idle (H1 test 1), a warm leak-down (test 3), and with
  the valve cover off, each lifter pressed down with its cam lobe
  pointing up — a lifter that gives before the valve moves has bled
  down (*general*; VW's manuals describe a check of this kind for these
  engines, recalled and **not** checked against the manual here).
- **Flicks only at idle**: the gauge has confirmed the misfires and not
  named them; nothing moves in the ranked list, and the next repair is
  chosen from it as it stands.
- **Low and steady**: at idle only → H3 moves up, and the intake is
  smoked warm; at 2500 too → the belt's marks are checked.
- **Steady and normal**: the valvetrain and a large leak are cleared as
  far as a gauge can clear them; H1 and H3 both lose, and H0 gains.
- **Cold and warm differ** (item 3 done): a flick cold that is gone warm
  fits the cold enrichment and deposits (H1, *inlet-valve deposits*);
  one that is there warm only fits a lifter on thin oil.

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
