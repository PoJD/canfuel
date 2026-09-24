# The engine's own health, and why it lands in this repository

**This is a holding document for an open investigation, not a firmware
document.** It exists because one of its questions is genuinely ours — whether
the `Torque` and `Power` channels this firmware transmits are right — and the
rest of it is the evidence that question has to be argued against. When the
investigation closes, whatever survives moves into `frames.md` and
`can-decoding.md` and this file goes away.

⚠ **Nothing here changes any constant in `src/`.** Everything below is a
measurement or an argument about the vehicle. The firmware is unmodified and
the numbers it transmits are, as far as anything here shows, arithmetically
correct — see *What the display can and cannot mean*, below.

---

**Where it stands now**, after the plugs, leads, injectors, fuel filter,
regulator and MAF were all replaced (*The post-repair drive and the MAF swap*,
at the end): the car pulls better; the rich lambda trim was the MAF and is
gone; **the idle misfires and the occasional exhaust puff are not gone**, and
122 of 129 new misfire events begin at a standstill idle. That second fault is
open. The torque scale this file was opened for is settled elsewhere.

**No procedure hangs off this file any more.** Both sessions it was built
around, the cold start before the repair and the drive after it, were
one-shots and were followed; what they produced is in the fixtures and read
below, and `git log` has the procedures themselves if the wording of a step is
ever wanted.

## The occasion

The car had been off the road. It came back with a **completely blocked
catalytic converter**, found at a garage, which replaced the cat, the silencer
and the manifold — most of the exhaust — against a previous replacement about
five years and not many kilometres earlier. An ignition coil had been changed
shortly before that, after misfires under full load. New injectors and
silencers are due the following week.

**2026-09-10 was the first proper drive afterwards**, on public roads, with the
converter fitted and the display reading its ten channels. What follows is what
came off it.

### The history before any of that, and why it changes how the evidence reads

**The car was bought with an oxygen sensor already faulty, and that sensor was
one of the first things replaced.** It was found only after something else was:
**the engine warning lamp had been masked inside the instrument cluster by the
previous owner**, so it had been lit the whole time and could not be seen.

⚠ **That is history and not a current condition.** The mask was found and
removed within days of the purchase of 25 September 2017 and **the lamp has
worked normally ever since** — so everything in this file, and every symptom
description anywhere in `docs/`, was observed with a functioning lamp.
`vehicle-history.md`, *The masked warning lamp*, is the record. What nobody has
is the fault history from **before** September 2017.

Three things follow, and none of them are sentiment.

- **Both oxygen sensors have already been replaced on this car**, pre- and
  post-catalyst. So **any** `not OK` from the blocks that check them — 034 for
  the one in front, 036 and 037 for the one behind — is a **second** failure of
  that sensor, which argues for something that keeps killing them rather than
  for a worn-out part. Both have also sat in the exhaust of a converter that
  was burning through.
- **That is what makes the lambda adaptations mean something.** The **−4.7 % at
  idle against +1.6 % at part load** recorded in *Misfire counting* below were
  read during this investigation, which is to say **with both replaced sensors
  fitted**. A rich adaptation measured through a faulty sensor says nothing;
  measured through a sound one it is a real excess of fuel. So the two verdicts
  fork cleanly:

  | 034 / 036 / 037 | what −4.7 % at idle then means |
  |---|---|
  | both `OK` | the ECU is correcting a **real** fuel excess — the injectors |
  | either `not OK` | a second sensor has failed and the adaptation may be an artefact of it; re-read 032 after it is replaced |
- **The parts have been replaced in the order the symptoms surfaced**, which is
  not the same as the order of cause: sensor, then coil, then most of the
  exhaust, and only now the injectors. A single upstream cause producing
  symptoms one at a time looks exactly like this from inside it, which is the
  argument for the diagnosis-before-parts position the rest of this file takes.
- **The masked lamp means "for years" is a lower bound only where it reaches
  back past September 2017.** Inside the ownership the lamp has been working
  and the symptom dates are the owner's own; it is the period before the
  purchase that has no record, cannot be turned into a date, and should not be.
  ⚠ **The two must not be run together** — an unbounded "nobody knows how long"
  applied to the whole history is a stronger claim than the evidence supports,
  and this file made it in an earlier revision.

**Nothing further is bought before 034 and 046 report.** That is the owner's
position and it was the right one. They were read after the post-repair
drive and all four reported OK (*The post-repair drive*, below); they are
absolute rather than comparative, so they needed no baseline this car could no
longer provide.

---

## What the vehicle reported

**From the display**, read as maxima over the drive:

| | |
|---|---|
| `Torque`, peak | **117 Nm** |
| `Power`, peak | **58 kW** |
| oil temperature, peak (0x420 b3, the cluster's channel) | **72–74 °C** |

### The same three numbers after the plugs, leads and exhaust — 2026-09-19

A long drive to the Šumava and back, on new spark plugs, new leads and a new
exhaust, with the engine reporting no faults and the catalytic converter no
longer smelling once warm. **Read off the display from the driver's seat and
not logged**, so these are reported figures rather than a capture — which is
enough for the only question they answer, because the question is whether the
parts moved the number at all:

| | 2026-09-10 | 2026-09-19 | |
|---|---|---|---|
| `Torque`, peak, full throttle | 117 Nm | **115–117 Nm** | unchanged |
| `Power`, peak | 58 kW | **~50 kW** | see below |
| oil temperature, peak | 72–74 °C | **≤ 74 °C after two hours** | unchanged |

**The torque did not move, and that is the finding.** New plugs, leads and
exhaust reproduced the previous pull's peak exactly, so whatever holds b7 down
at full throttle is not the ignition side and not the back pressure. The
airflow argument below is untouched by this drive and remains the thing that
needs a capture.

**The lower peak power is not a second finding.** Peak power and peak torque
need not occur together: 117 Nm at 4735 rpm is 58 kW and 115 Nm at 4150 rpm is
50 kW, so a drive that changed up earlier reports a lower maximum with the
same engine. Only a pull held to the same engine speed compares, and nothing
here says this one was.

⚠ **Two hours and still no more than 74 °C of oil is the entry that matters
most**, and it belongs to question 10 in `can-decoding.md` rather than to this
document. That question weighs *"this car is only driven gently"* against
*"the channel is offset low"*, and the longest drive on record until now was
about an hour. A run to the Šumava and back is not gentle pottering, so the
first explanation is now carrying weight it did not have to carry before.

Two notes on the oil figure, because it invites a wrong conclusion. It is
**not** anomalous: the four warm free-revving holds this project's drag line is
fitted to sit at 72.8–76.6 °C, and the fixture table under question 4 in
`can-decoding.md` has the oil lagging the coolant badly — 65.3 °C of oil at
99.0 °C of coolant in `03_drive`. And **it cannot be a cause of a rich
mixture**: the ECU's warm-up enrichment runs off the coolant sensor, not off
this one, which feeds the instrument cluster. A cold-running *coolant* sensor
or a thermostat stuck open would be a mechanism; this channel is not.

**Both of those are now ruled out as well, so the rich mixture has to be
explained some other way.** Enrichment needs the ECU to believe the engine is
cold, and the coolant curve in `can-decoding.md` question 4 says it does not:
0x288 runs **54.0 → 68.25 → 75.75 → 90.0 → 96.75 → 99.0 → 100.5 °C** across
the fixtures in warmth order — an ordinary warm-up finishing where a healthy
engine finishes. A thermostat stuck open cannot produce that curve, and a
coolant sensor reading low cannot produce its top end. 0x288 is on the ECU's
own frame rather than a separate gauge sender, so that is what the ECU
believes and not merely what the needle shows. **Do not re-propose either as a
candidate**; the airflow and fuelling argument below is where this goes.

#### The trip itself, as the owner reports it

**About 450 km**, two long runs there and back plus roughly an hour of
touring, on new plugs, leads and exhaust and on the **old** injectors — they
were still in transit. **No faults**: the lamp stayed out and nothing was
reported.

**The smell is recorded above and 450 km did not bring it back**, which is
the part worth adding: neither the converter nor the exhaust smells unhealthy
after a long run, and it now survives two long runs rather than one warm-up.

**The motorway was deliberately gentle.** Held at about 4,000 rpm and no more
than 5,000, which the owner puts at about 130 km/h in top — the figure is not
tied to which of the two engine speeds it goes with — with brief excursions
higher when joining. So nothing on this trip is a measurement of the top end,
and the b7 figures below are not one either.

⚠ **And the owner still reports the car as not right.** A long run leaves it
feeling livelier, which is the observation this file already carries; the
residual has not gone. Nothing on the fuel side was changed before this trip,
so that is the expected result rather than a disappointing one.

**The car was then parked until the injectors arrived**, which restored the
one condition the post-repair drive needed: an overnight stand with nothing
disturbing it. It also kept the tank as it was filled — see `refuel-reset.md`,
*The 2026-09-19 fill*.

#### What the two torque readings imply about b7 — derived, not measured

Two figures came off the display, and they are worth inverting because they
are the first full-throttle readings this project holds that are **not** from
a low-gear sweep:

| what the driver did | display | rpm | **b7 this implies** |
|---|---|---|---|
| a pull from about 2,000 to 3,000 rpm, maximum over the pull | **114 Nm** | 2,000–3,000 | **176–183** |
| full throttle, held above 4,000 rpm | **117 Nm**, steady | 4,000–5,500 | **193–203** |

⚠ **Derived by inverting this firmware's own arithmetic against a display
reading, with the engine speed estimated from the driver's description.**
`b7 = (Nm + 6.74 + 0.004820 × rpm) / 0.74`, from the `TORQUE_CNM_PER_BIT` and
drag line `config.h` carried when that display was read, with
`TORQUE_TRIM_PCT` at zero. The b7 column is what stands; the scale has since
moved to 1.06. **The rpm band is the
whole of the uncertainty**; everything else is arithmetic. This is not a
substitute for a capture, and the held pulls of the post-repair drive have
since measured b7 directly — `can-decoding.md` question 8.

**What it is worth anyway.** `tools/b7scan.py` puts the largest b7 this engine
has ever been *seen* to make at **185**, out of three wide-open bursts that
were every one of them still climbing when the throttle shut. A steady 117 Nm
above 4,000 rpm implies b7 near **196** — higher than anything recorded, and
for the first time **not still rising when it was read**. The air argument in
`frames.md` predicted b7max near 196–217 at a September intake temperature, so
this landed on the bottom edge of that band; the held pulls later reached 206.

⚠ **A display reading with a wide band under it settles nothing**, and
reading it as the prediction confirmed is the mistake available here. What it
does is point where the prediction pointed, before the drive rather than
after it.

**From VCDS**, `01-Motor`, measuring blocks logged to file during the drive.
The engine is `06A 906 018`, labels `06A-906-018-AQY.LBL`. Group **003** turns
out to carry engine speed, **mass air flow in g/s**, throttle angle and
ignition advance; group **010** carries engine speed, **relative load in %**,
throttle angle and advance. That confirms the guess `can-decoding.md` records
for question 3 — mass air flow is in group 003 — against the actual ECU rather
than against a plan.

Four wide-open-throttle pulls, averaged into rpm bands. Every sample here has
the throttle above 84° in **both** groups, which rejects the transients: the
two groups are read about 0.3 s apart and disagree with each other whenever the
pedal is moving.

| rpm band | n | MAF g/s | load % | advance °BTDC |
|---|---|---|---|---|
| 3000–3499 | 3 | 51.4 | 77.9 | 18.3 |
| 3500–3999 | 9 | 64.1 | 78.9 | 14.3 |
| 4000–4499 | 13 | 71.2 | 78.3 | 19.5 |
| 4500–4999 | 10 | 80.5 | 78.4 | 21.6 |
| 5000–5499 | 8 | 84.8 | 76.4 | 23.7 |
| 5500–5999 | 2 | 86.8 | 78.6 | 25.9 |

Peak mass air flow over the whole log is **87.5 g/s at 5720 rpm**. Load at full
throttle is remarkably flat: **78.1 % mean, 75.3–81.9 %, and never higher.**
Idle is 783 rpm, 3.38 g/s, 23.2 % load, 2.9 °BTDC.

**The throttle reaches 85.1–85.5° under load**, which is the same figure it
reaches with the pedal on the floor and the engine stopped, and pressing harder
moves it only to 85.9. That is a mechanical stop, and it closes the question of
whether the pedal or the throttle is being limited. It is not.

**The advance looks healthy** — 18 → 26° rising with engine speed, with no
sustained retard. Isolated low samples (2.3°, 6.8°, 9.0°) are each a single
reading during a transition where the two groups contradict each other, so they
are not evidence of knock. Knock retard itself was not logged; it is in group
023, per cylinder.

---

## What "load" is a percentage of — measured, not assumed

**The ECU's relative load is the measured air mass normalised to 0 °C and
1013 hPa**, the classic Bosch standard condition, where air weighs 1.293 g/l.

That was not taken from anywhere. Three quantities were logged at once — grams
per second from the MAF, litres per second from engine speed and displacement,
and the ECU's own percentage — and grams divided by litres gives the density
the ECU must be normalising to. Over 51 steady samples above 70 % load the
median is **1.292 g/l**. Below about 70 % load the relationship scatters, which
is expected: at part load the ECU's load figure carries corrections that a bare
air-mass ratio does not.

**This matters because it means 78 % is not "the engine manages 78 % of what it
could".** The engine never gets 0 °C air; it draws from the engine bay. Correct
the reference to plausible intake conditions and the real filling of the
cylinders comes out as:

| intake air | real volumetric efficiency at full throttle |
|---|---|
| 20 °C, 1013 hPa | 84 % |
| 30 °C, 1000 hPa | 88 % |
| 40 °C, 980 hPa | 93 % |

Intake air temperature was not logged, so that spread is the honest bound
rather than a figure. **Every value in it is a normally breathing engine.**

⚠ **That bound can be narrowed next time, and this file first claimed it could
be replaced by a figure.** Intake air temperature is genuinely **not on the CAN
bus** — which is what matters for the firmware, and why `config.h` rules out a
live correction factor — but **VCDS has it**: groups **004** and **006** both
carry `teplota nasav. vzduchu`, and 006 adds an **altitude correction factor**.

**What cannot be had is the reading that would settle it**, which is the intake
temperature *during a full-throttle pull*. Reading any block means changing the
group selection, and that ends the VCDS log the rest of the session depends on.
So 006 is read cold before the key and hot at
the end, and the two **bracket** the pulls rather than measuring them: the
altitude factor is a constant either way, and the first cold start recorded put
the standing intake at **22.5 °C with the oil at 12.75** — about ten degrees of
engine bay over ambient, against which a moving car is somewhere in between.

**A badly failing air-mass sensor is therefore ruled out; a slightly lazy one is
not.** The calculation uses the sensor's own reading, so a sensor under-reading
by 10 % would put the true efficiency near 97 %, which is still physically
possible; one under-reading by 25 % would require over 110 %, which a naturally
aspirated engine of this kind does not do. The independent argument is the
**multiplicative part-load adaptation of +1.6 %** — a sensor reading low would
force the ECU to add fuel back, and it is not adding any.

---

## The gap that is left, and the two readings of it

At 4724 rpm the engine took **80.5 g/s** of air. What that airflow is worth
depends on how efficiently it is burned:

| if the true torque is | brake thermal efficiency comes out as |
|---|---|
| **117 Nm** — what the display showed | **21.9 %** |
| **~150 Nm** — what the airflow implies at a normal efficiency | **28.0 %** |

An engine of this type and age should reach roughly 28–32 % at full throttle.
**Both rows are reachable**: 28 % says the engine is healthy and the display
under-states it, 21.9 % says the display is right and the engine is burning
badly. The same measurement supports both, which is why this is written down as
an open question rather than answered.

⚠ **The two candidate explanations are independent of each other**, and this is
the part that is easy to get wrong. Both `117 Nm` and `~150 Nm` are *idealised*
figures — the first is the ECU's model of what the air should produce, the
second is thermodynamics' model of the same thing. Combustion quality enters
neither. **So repairing the fuelling cannot close the gap between them.** The
injectors are a question about the engine; the scale is a question about this
firmware; next week's drive speaks to the first and is silent on the second.

---

## What the display can and cannot mean

**0x280 b7 is a model output and not a measurement** — this ECU has no torque
measuring block. What that model can and cannot see is set out in `frames.md`
under *Torque and Power*, sorted by how well founded each part is, because an
earlier version of this file stated it far more confidently than the evidence
allows.

The short of it: these channels most likely **over-read on an unhealthy
engine**, reporting what the measured air should have been worth. But the step
that would make them blind to combustion outright — that the model uses the
*commanded* lambda — is **recalled rather than sourced**, and the per-cylinder
misfire detection below is evidence that the ECU has a combustion signal of
some kind. Treat "it cannot see combustion" as a hypothesis this drive can
falsify, not as a property of the device.

---

## Misfire counting — the label is wrong

**Group 014's misfire counter is a current count, not a cumulative total**,
whatever the label says. Found by accident: the screen was left open after a
log finished, read zero, and then showed non-zero values during a pull-away.

The pattern, watched rather than logged, is **first gear at low speed** — a slow
pull-away, or downshifting to first while braking almost to a stop — with
values between 5 and 17 that then fall back. A full-throttle pull with the
screen open showed **a hard zero**.

**The VCDS label file for this ECU settles what this counter is, and what it
is not.** Its entry for block 014 names the third field as the misfire count
and **specifies it as 0 to 5**. (The file is Ross-Tech's and is deliberately
not kept in this repository; `can-decoding.md` carries our own summary of the
blocks this project uses.)

Three things follow:

- **The values watched were out of specification.** 5 to 17 against a stated
  0 to 5. That is a harder claim than "there were misfires".
- ⚠ **A specification of 0 to 5 is not the range of a lifetime total**, whatever
  `(celkovy)` suggests. It is consistent with the current count the screen
  actually showed, and with the label being misleading rather than the ECU.
- **There is no absolute counter and no per-cylinder counter to find.** Group
  014 is the only misfire block in the file; looking for a cumulative one was
  a reasonable guess and the answer is that it does not exist here.

**Per-cylinder information does exist, for knock rather than misfires** —
groups **022** (cylinders 1 and 2) and **023** (3 and 4), ignition retard angle
per cylinder, specified 0.0 to 15.0 °CA. **A cylinder being retarded further
than its neighbours names itself**, which is the identification wanted here
arrived at from a different direction.

⚠ **The counter reads zero and the detection reports `deaktiv.` whenever the
engine is not running**, so a reading taken with the ignition on and the engine
stopped proves nothing. Read it with the engine idling, immediately after a
loaded drive, and do not clear the fault memory first.

Low speed, low load and high manifold vacuum is where a leaking injector shows
up: the extra fuel is a fixed quantity and matters most where there is least
air. It also fits the **lambda adaptations, −4.7 % at idle against +1.6 % at
part load** — a constant excess of fuel, corrected away in proportion at idle
and invisible under load. A single pre-catalyst oxygen sensor measures the
average of four cylinders, so one rich cylinder and three lean ones average to
something the ECU is content with while every one of them makes less torque
than a correct one.

### The rough idle is in the fixtures, and it has a thermal lever

**The symptom, as the owner describes it:** idle is not uniformly rough. It
runs reasonably and then, every few seconds, stumbles slightly. **It has been
like this for years**, alongside the exhaust system progressively destroying
itself and poor cold starts — three long-standing symptoms rather than one
recent one.

**It is in the recordings**, which means it can be measured rather than only
felt. Counting transient dips of engine speed against its own one-second
median — `python tools/idledips.py`, which prints exactly this table:

| fixture | oil | coolant | dips ≥ 20 rpm | dips ≥ 15 rpm |
|---|---|---|---|---|
| `09_idle_60s_z1` | **61.5 °C** | 100.5 °C | **15 in 60 s** | 39 |
| `11_idle_noac_z1` | 72.8 °C | 99.0 °C | **0 in 25 s** | 3 |
| `12_idle_ac_z1` | 73.5 °C | 99.0 °C | **0 in 25 s** | 1 |
| `18_coldstart_z1` | **17.3 °C** | 63.8 °C | **44 in 310 s** = 8.5/min | 165 |

⚠ **The counts moved when the measurement became a tool, and the movement is
the reason it became one.** The first pass at this was a script that was not
kept; reconstructing it later gave 15/39 against a published 13/35, with the
two zeros reproducing exactly. Nobody could say which reconstruction was
right, so `tools/idledips.py` now owns the definition — one dip is one event
however many samples it spans, the baseline is a ±0.5 s median so it rides the
warm-up ramp, and `tools/test_idledips.py` holds those properties. **The two
zeros are the load-bearing part of the table and they never moved.**

⚠ **An earlier pass at this reported the fixtures as smooth and was wrong.** It
looked for the single deepest dip, which is a different question: the deepest
excursion in `09` is only 37.5 rpm, while what the owner describes is a small
event *repeating*. Asking for the maximum answers "is there one big stumble"
and says nothing about fifteen small ones.

**The lever is how heat-soaked the engine is, and the coolant hides it.**
Coolant sits at 99 °C in all three warm logs, so the ECU's own warm-up state is
identical and cannot be what differs. The only thing that separates them is the
real temperature of the engine, for which the oil is the available proxy: the
stumbles are there at 61 °C and gone at 73 °C.

⚠ **The cold row does not extend that line, and it was expected to.** At 13–17
°C of oil the rate is 8.5 a minute — real, but *half* of the 15 a minute at
61 °C. **The relationship is not monotonic in temperature**: it peaks somewhere
in the middle and is gone at the top. Three readings and a peak in the middle
is not a curve, so what this actually does is weaken the lever rather than
extend it. **A single continuous warm-up recording would settle it**, which
`19_postfix_drive_z1` now is and `18_coldstart_z1` is half of — it holds 13 °C
to 17 °C of oil and stops, because five minutes of idling moves the oil almost
not at all.

**That fits a leaking injector and argues against the evaporative system.** A
dribble onto a port that is not yet hot puddles instead of vaporising and goes
in as a slug; once everything is heat-soaked the same dribble evaporates and
disturbs nothing. Purge, by contrast, is normally enabled only once warm, so it
would disturb *more* in the hotter state rather than less.

**The intervals are irregular**, which points the same way: 3.3, 3.9, 3.1, 3.7,
10.1, 1.5, 1.7, 3.4, 4.9, 0.9, 5.8 and 1.2 seconds — a mean of 3.6 s with a
standard deviation of 2.4. **A valve on a duty cycle produces a period.** This
is sporadic, which is how an accumulating drip behaves and how a duty-cycled
anything does not.

**A third observation, and it is weak on purpose.** b7 does not move at any of
the dips in `09`: engine speed falls 20–37 rpm while the ECU's modelled torque
stays exactly on its own baseline. That is the blindness described under *What
the display can and cannot mean* showing up in this car's own data — but the
resolution is coarse enough that a brief event might not register regardless.
**Twice as coarse as this passage used to claim**: one count of b7 is 0.39 %,
but b7 has never been seen to change by a single count, only by two, so the
smallest movement available to it is about 1.5 Nm. `python tools/b7scan.py
--ladder` prints the value set; `docs/frames.md` has it under *What b7 has
actually been observed to reach*. **Suggestive, not evidence.**

⚠ **The whole thing is a correlation across three recordings, one of which is
positive.** They differ in more than the data holds — different days, fuel and
ambient conditions — and `09` is two and a half times longer than the others,
which the per-second rates account for but which still gives it more chances.
**Treat the thermal lever as the most testable idea here, not as a finding.**

**What costs nothing to check:** if this is right, the stumbling should be worst
in the twenty minutes *after* the temperature gauge has already settled, and
should ease as the engine soaks through. The gauge reads the coolant and is
therefore useless for it; `OilTemp` on the display is not.

### The oldest symptom is on the overrun, and it is the sharpest statement of the lever

**The owner's recollection, offered after the Šumava trip and describing
something that predates all of this work:** on a **cold** engine, braking on
the engine down a hill, **fuel could be heard going into the exhaust and
burning there** — a burbling from the back of the car, **carrying on through
the engine braking**. On a warm engine there is at most **a single event just
after the pedal comes up, and then silence.**

⚠ **The discriminator is whether it STOPS, not whether it burbles**, and an
earlier version of this section had the symptom as warm-silent against
cold-noisy, which is not what was described. Both states make a noise. Only
one of them goes quiet.

**That is the same thermal lever as the idle stumbles, stated far more
cleanly.** The idle argument has to work through counting dips and comparing
three recordings that differ in more than temperature. This one is an event
the driver can hear, behaving one way in one thermal state and another way in
the other, with no instrument involved at all.

⚠ **It is a recollection and it is undated.** What the repository can now
corroborate is the *mechanism it needs* rather than the symptom itself — see
the fuel cut below. Nobody has recorded the burble.

**Why the overrun is the sharp part.** Coasting in gear with the pedal fully
released is the condition in which the ECU has the least reason to be
delivering fuel at all — the engine is being turned by the car rather than
asked for torque. Unburnt fuel reaching a hot exhaust *there* is fuel arriving
while the driver asks for none. **A dribble that puddles on a cold port and
evaporates on a hot one produces exactly the temperature dependence
described**, and it is the same mechanism this file already proposes for the
idle stumbles, observed in the state where it is loudest.

**The one fact it rests on is now measured: this ECU does cut the
injectors on the overrun.** `python tools/coastscan.py` finds four of them in
`17_drive_property_z1`, and they agree with each other closely:

| | shut at | fuel back at | after the lift | for |
|---|---|---|---|---|
| | 2668 rpm | 1750 rpm | 1.23 s | 0.93 s |
| | 2981 rpm | 1700 rpm | 1.24 s | 1.01 s |
| | 3066 rpm | 1740 rpm | 1.19 s | 1.05 s |
| | 3204 rpm | 1754 rpm | 1.30 s | 1.13 s |

**The counter does not slow down, it stops** — zero microlitres for a second
at a time while the car rolls. Two numbers come out of it and both matter
later: **the cut engages about 1.2–1.3 s after the pedal comes up**, not
immediately, and **fuel returns at about 1,700–1,750 rpm**.

**The delay is what explains the warm symptom, and it makes the warm state the
control rather than a second puzzle.** For those 1.2–1.3 s the ECU is still
fuelling normally — at the measured 769 µl/s that is about **a millilitre of
fuel commanded after the driver stopped asking for any**. A single event just
after the lift followed by silence is that millilitre finishing, on an engine
doing exactly what it is built to do. **Nothing about the warm case needs a
fault to explain it.**

**The cold case is the one with something left over.** Burbling that carries
on through the whole coast is fuel still arriving well past the point where,
warm, there is none left to arrive.

**The owner sees the same thing on the display**, independently and at road
speed rather than in first gear: `FuelNow` falls to zero on the overrun and
comes back at around 1,200 rpm. ⚠ **That zero is a real cut and not the
display rounding down.** `compute_fuel_now_d()` sends l/100 km in tenths, so a
displayed 0.0 needs the flow below speed ÷ 7200 — **under 8 µl/s at 60 km/h**,
against 326 at warm idle. Nothing short of the injectors being shut reads
zero there.

⚠ **The resume speed is the one place the two disagree**, and it is worth
checking rather than averaging: 1,700–1,750 rpm in the log against about
1,200 from the driver's seat. The log is first gear at under 30 km/h, where an
ECU has every reason to give the engine back its fuel early; a high gear at
road speed is a different case and is what the next drive records.

⚠ **What is NOT settled is whether it cuts fuel when the engine is cold, and
that is the whole of the question.** `17_drive_property_z1` opens at 75 °C of
oil, so all four of those cuts are **warm** — the state the owner says the
burble does not happen in. `18_coldstart_z1` is the only cold recording and the
car never moves in it, so there is no cold coast anywhere in this repository.

**Both answers are informative, which is what makes it worth driving for:**

| if the cold coast | then |
|---|---|
| **cuts fuel too** | fuel audible in the exhaust there is arriving with none commanded. An injector that is not sealing is what the rest of this file already points at, and purge is ruled out by the same cold-only argument as at idle — it is enabled once warm, so it would burble in the wrong state. The strongest single thing this investigation would have |
| **does not cut** | the burble is commanded fuel, the symptom says nothing about the injectors, and the cold-only pattern is the strategy rather than a leak |

**The owner's own suspicion is the second one** — that the cut may be a
warm-engine behaviour — and the fixtures cannot argue with it either way.
⚠ **It is also why the last capture "missing" it is not evidence of anything**:
it did not miss it. The cut is in that file four times over; nobody had
looked, because until now nothing asked the question.

**One coast on the next drive would settle it**, and the post-repair drive
took several: `coastscan.py` finds 72 cuts in `19`, the coldest at 63.8 °C of
coolant, and the driver heard no burble at all, cold or hot. No coast happened
below 61 °C of coolant, so the ECU's behaviour on a genuinely cold overrun is
still not recorded.

### The old converter was shown to the owner, and it is the one hard fact here

Cracked on the outside, blocked inside, and **one chamber burned right
through**.

**That is not what a slightly rich mixture does.** A fuel trim of a few per
cent does not melt a substrate; a converter is built to take exhaust gas, not
to burn as a combustion chamber itself. Burning through takes **raw unburnt
fuel igniting inside it**, which means misfire rather than enrichment.

So the misfire pathway stops being an inference from a counter on a screen and
becomes the leading explanation, on physical evidence. Everything else in this
file is reasoning; this is a piece of metal somebody looked at.

Two readings of the detail, both **hypotheses and not mechanisms**:

- **One chamber rather than the whole substrate** fits one cylinder better than
  four, which is what a single leaking injector would do. Flows mix in the
  manifold, so this is not an identification of which cylinder.
- **The external crack is probably the same thermal event**, not a separate
  fault — it is simply the part of the damage that is visible from outside,
  which is why it was what the garage first saw.

⚠ **The new converter is exposed to exactly the same fault.** Driving it while
a cylinder still dumps raw fuel cooks it the same way, which is why the car is
standing until the injectors are done.

**Whatever the rich running fouled is still fouled**, and the spark plugs are
the item that matters: they are downstream casualties that survive the repair,
and a fouled plug misfires at low load and high vacuum exactly as observed
here. New injectors do not fix one. If the ignition work did not already
include them, they belong in the same visit rather than in a later round.

**A third observation lines up with the other two**, recorded here because it
was made months earlier and its significance was not obvious at the time: when
the fuel pressure regulator was changed, the system held **no residual
pressure** and the fuel simply ran out. A system that bleeds down overnight is
losing fuel somewhere, and injectors that do not seal are one of the few paths
— the same ones that would explain the poor cold starts.

**Which points at long idling rather than hard driving as what destroyed the
catalytic converter** — that is where the misfires are, and that is where the
engine spends most of its time.

⚠ **The historical fault is not reproduced and stays open.** The warning lamp
used to appear only after minutes above ~4500 rpm in top gear on a motorway,
which a short drive cannot recreate. No lamp on this drive is therefore weak
evidence about the coil, not a clearance. **It is weak because the conditions
were not recreated and for no other reason** — the lamp itself has been
uncovered and working since 2017, so both that historical observation and this
drive's silence are readings of an instrument that reports.

**25 September 2026: the condition was recreated, near enough, and the lamp
stayed out.** About 100 km, mostly steady motorway at 4000–4500 rpm in 5th,
**once about five minutes continuously at 4500** and briefly at 5000, on the
new coil, plugs, leads, injectors and MAF. No fault, no lamp, no hesitation.
*Owner-reported, not logged.* That is the regime the old lamp needed, so the
full-load fault this section records now reads as **cleared on the new parts**,
not merely unreproduced. ⚠ One drive, and "minutes above 4500" was
five of them at 4500 rather than longer above it. For scale, the owner gives
**4000 rpm in 5th as about 135 km/h on the speedometer**; the gearing is
long.

---

### A candidate ROOT cause, from a photograph — and it is a hypothesis

**This file has a symptom and has never had a cause.** Everything above argues
that an injector is delivering fuel nobody asked for; nothing anywhere says
why an injector on a 2000 car would start doing that. **Three photographs of
the fuel filter that came off in 12/2017 supply a candidate**, and
`vehicle-history.md` has them: the can was corroded, the joint was wet, the
owner records it as leaking, and what drained out was dark and cloudy rather
than clear petrol.

**The chain, stated so it can be attacked:** the tank and lines were dirty →
the filter was overwhelmed and eventually holed → whatever it stopped holding
back went to the injectors → the injectors were damaged, and have been
dribbling ever since.

⚠ **A paragraph here briefly claimed the first link had an observation behind
it — the car's old fuel starvation — and it has been withdrawn.** That symptom
is not attributable to the filter rather than to the pump
(`vehicle-history.md`), and a pump implies nothing about contamination. **The
first link rests on the sludge in the tray and on nothing else.**

**The timeline survives the obvious objection, which is worth checking rather
than assuming.** The filter was changed in 12/2017 and the injectors are
coming out in 9/2026 — nine years later, all of them on a clean filter, so why
did anything keep dying? **Because the converter's whole life is inside that
window.** The one fitted in 10/2017 was found completely blocked in 9/2026,
and the plugs of 12/2022 were destroyed in ~1,500 km. Both are downstream of
injectors that were already spoiled before the filter was changed and have
been spoiling things since. **Contaminated fuel is not needed after 2017 for
the rest of the record to look the way it does** — one set of ruined injectors
is enough, and that is what makes the chain internally consistent rather than
merely appealing.

⚠ **Every link in it is unproven, and two of them are not even observations.**
That the injectors are faulty at all is circumstantial — the stumbles, the
cold overrun, the −4.7 % trim, the destroyed converter — and no one has
examined an injector. That contamination caused it is an inference from a
photograph of a different part taken nine years ago. **This is a candidate
root cause, not a finding**, and nothing in the plan changes because of it:
the injectors and the filter are both being replaced anyway, for reasons
decided before this was thought of.

⚠ **It points upstream, and the tank is NOT untouched — an earlier version of
this passage said it was and that was wrong.** A filter full of black sludge is
a filter that was doing its job until it could not, so **the source was above
it**. But the tank has been replaced, inside the ownership, and
`vehicle-history.md` records that **the date is not recoverable**.

**Which is what stops this being either a worry or a relief.** If the tank went
in before the injectors were spoiled, the source was gone early and the chain
above needs another one. If it went in afterwards, the source is gone *now* and
the new parts are behind a clean one. **The two readings differ only by a date
nobody wrote down**, so neither can be argued for, and the lines between tank
and filter have never been changed under either.

**Nothing here proposes dropping a tank.** It is written down because the chain
implies an upstream source and because the correction matters: this project
does not get to keep a suspicion it has already been told is out of date.

**There is exactly one test and it expires in a few days.** The old injectors
come out when the new ones go in. **Their inlet screens and nozzles are the
only physical evidence this hypothesis will ever get**, and once they are in a
bin the question is closed by default rather than by answer. *The old
injectors — kept and photographed, not tested* below is what happened to them.

## The cold start, recorded once, before the parts were changed

**One cold start and five minutes of idle, on the car as it was** — old
injectors, plugs and leads, new exhaust. It happened once and cannot be
repeated: after the injectors there is no bad cold start left to record.
The procedure it was taken by is in `git log` and not in the tree, having been
followed.

| | |
|---|---|
| `test/fixtures/18_coldstart_z1.txt` | 255,628 frames, 360.01 s, adapter timestamps |
| `test/fixtures/vcds/vcds-coldstart-014-055.csv` | groups 014 and 055, 497 samples, 297.2 s |
| `test/fixtures/vcds/vcds-coldstart-aborted-014-055.csv` | the first attempt, 7 samples — see the gap, below |

**The coldest state this car has ever been recorded in.** Oil 12.75 °C rising
only to 17.25 °C; coolant 16.50 °C rising to 63.75 °C. Every previous fixture
starts at 61 °C of oil or above.

### The start itself, at ninety-four samples a second

| CAN time | engine speed | what it is |
|---|---|---|
| 41.40 s | 15 rpm | the crankshaft first moves |
| 41.65–42.57 s | ~235 rpm | **cranking, 1.24 s of it** |
| 42.64 s | **451 rpm** | first firing |
| 42.72–42.88 s | **383 → 311 rpm** | **it falls back, and nearly dies** |
| 42.96 s | 583 rpm | catches for the second time |
| 43.00 s | 747 rpm | running |
| 43.67 s | 1446 rpm | the cold-idle flare, its peak |

**The near-stall is the symptom, in numbers.** The owner's account, given
before this trace was shown to him, is that this is the familiar moment: it
judders for a few seconds and then either dies or clears. Here it cleared. The
previous start had been **about ten hours earlier**, so the rail had had a
long time to bleed down — which is the condition under which the symptom is
worst and the condition this recording therefore caught.

⚠ **Nothing here distinguishes a leaking injector from a failing check valve
in the pump, and both bleed the rail down overnight.** The new injectors will
answer it by elimination and not by argument.

### The misfire counter, logged rather than watched

**`docs/can-decoding.md`'s expectation was that detection would read
`deaktiv.` while the engine was cold. It does not.** It reads `aktivováno`
from the first sample of the surviving log, at 920 rpm with the coolant near
30 °C. What holds is the narrower statement already in *Misfire counting*: the
counter reads zero and detection reports `deaktiv.` **whenever the engine is
not running** — the aborted log shows exactly that, through the cranking.

**The counter takes five values across 497 samples, and only five:**

| value | samples |
|---|---|
| 0 | 397 |
| 12 | 59 |
| 13 | 5 |
| 24 | 24 |
| 36 | 12 |

Two things follow, and the second is new.

- **It is out of the label file's stated 0 to 5 by a factor of seven.** The
  earlier observation was values of 5 to 17 watched on a screen; 36 is logged.
- ⚠ **It moves in steps of twelve.** 12, 24, 36 — with a single 13. A counter
  that only ever advances by twelve is not counting individual misfires as it
  reports them, and **no mechanism for that is offered here**, because none is
  sourced. It is an observation about the ECU, recorded so the next person does
  not read a step of 12 as twelve separate events.
- **It holds a value for about three seconds and returns to zero**, which
  confirms from a log what *Misfire counting* had from a watched screen: it is
  a current count, not a total.

### The stumbles and the misfires are the same events

**This is the result the recording was for.** The CAN capture and the VCDS log
were aligned on engine speed — best fit at `CAN = VCDS + 129.3 s`, root mean
square 19.1 rpm against a 10 rpm quantisation — giving **231 s of overlap**. In
that window there are **34 dips of ≥ 20 rpm and 7 increments of the misfire
counter**, and every one of the seven sits beside a dip:

| increment | at | nearest dip | lag |
|---|---|---|---|
| 0 → 13 | 163.48 s | 20.8 rpm | +0.67 s |
| 0 → 12 | 289.89 s | 30.2 rpm | −3.01 s |
| 0 → 12 | 335.45 s | 27.5 rpm | +0.23 s |
| 12 → 24 | 340.25 s | 36.0 rpm | +0.26 s |
| 0 → 12 | 350.44 s | 23.5 rpm | +1.34 s |
| 12 → 24 | 351.64 s | 20.5 rpm | −2.10 s |
| 24 → 36 | 354.04 s | 20.5 rpm | +0.30 s |

Median |lag| is **0.67 s against 2.30 s** for the same number of instants
placed at random in the same window, and a permutation test over 20,000 draws
gives **p = 0.023**. The dips are dense — one every 6.8 s — so coincidence is
cheap; the permutation test is what prices it.

**Read it as: the stumble is misfire.** That had been an inference from a
burned-through converter and a rich idle adaptation; it is now the two signals
moving together in one recording.

⚠ **Three limits, and the first is the real one.** Seven increments is a small
number and one recording is one recording. **The converse does not hold** —
only 7 of the 34 dips have an increment beside them, so either the counter's
step of twelve means single events go unreported, or most dips are something
else, and this recording cannot say which. And the ECU's counter is a windowed
quantity read at 1.7 Hz, so the lag is an upper bound on the true one and the
two negative lags are within that.

### Why a misfire shows as a dip and not as a surge

**The question is a fair one and the intuition behind it is wrong in an
instructive way:** if the fault is an injector letting extra fuel into a
cylinder, why does engine speed *fall*? More fuel should be more torque, and
the fall should then be the ECU taking the fuel back away.

**It is not the correction. The fall is the failed combustion itself**, and
three measurements say so.

**Extra fuel is not extra energy.** Torque against mixture strength peaks
slightly rich of stoichiometric and falls away on both sides of that; past
roughly half again as much fuel as there is air to burn it, a flame will not
propagate at all. A dribble from a leaking injector is not a few per cent
richer, it is a slug — and a slug that has puddled on a port wall goes in as
liquid, which does not burn, because only the vapour does. It wets the plug,
it cools the charge as it evaporates, and it displaces air that would
otherwise have carried oxygen. **Every one of those pushes the same way: less
work out of that power stroke, not more.** The burned-through converter is the
same fuel arriving in the exhaust unburnt and finding its oxygen there
instead, which is already in *The old converter* above.

⚠ **That paragraph is combustion textbook, not a document about this ECU**, and
it is why the ordering of the flammability limit is given rather than a
number. What follows is this car's own data.

**One lost power stroke is worth the dip that is measured, and the arithmetic
closes.** At the warm idle of `09_idle_60s_z1` — 796 rpm, 326 µl/s, both from
the table under *Verified values* in `CLAUDE.md` — the engine is burning about
10.5 kW of fuel and turning it into the roughly 18.5 Nm of indicated torque
that 0x280 b7 reports there, which is a net indicated efficiency of 15 % and
**about 58 J of work per power stroke.** A four-stroke four fires every 37.5 ms
at that speed, so a cylinder that produces nothing takes those 58 J out of the
kinetic energy of the rotating assembly and nothing else:

| assumed crank + flywheel + clutch inertia | predicted dip from one lost power stroke |
|---|---|
| 0.12 kg·m² | 57 rpm |
| 0.15 kg·m² | 45 rpm |
| 0.20 kg·m² | 33 rpm |

⚠ **The inertia is an estimate and nothing here measures it** — it is the
order a two-litre four of this kind carries, and it is the one input to the
table that is not off this car. So the table is a bracket, not a prediction.

Against it, `python tools/idledips.py --depths` gives a deepest dip of
**37.5 rpm** in `09` and **46.0 rpm** in `18_coldstart_z1`, and the deepest
excursion in `09` read sample to sample rather than against the rolling median
is 806.75 → 761.00 rpm, **45.75 rpm**. **The measured depths sit inside the
bracket.** One entirely failed combustion event explains the largest stumbles
in these recordings without needing the ECU to do anything at all.

**The typical dip is 20–22 rpm, which is about half of that** — consistent with
a partial burn rather than a complete failure, and consistent with only 7 of
the 34 dips in the aligned window carrying a counter increment. ⚠ **It is only
consistent with it.** The CAN speed field is at best one value per firing event
(below), so a measured depth is a lower bound on the instantaneous excursion,
and nothing here separates "a partial burn" from "a complete misfire the
sampling rounded off".

**And the ECU is what ends the dip rather than what causes it.** The fall in
`09`'s deepest event takes about 50 ms — one to two firing intervals — and the
recovery to baseline takes some 250 ms after it. **No fuelling loop is that
fast.** The pre-catalyst sensor is at the end of an exhaust port and answers
with a transport delay plus its own response time; the −4.7 % of block 032 is
a *stored adaptation*, which moves over minutes and not between two power
strokes. What the idle governor does on a timescale of 250 ms is add torque to
bring engine speed back up, which is the recovery, in the opposite direction to
the event.

### Engine speed on 0x280 is recomputed once per 180° of crank

**Measured, over the fixtures, by `python tools/idledips.py --segments`.** The
frame goes out every 10 ms but its speed field holds a value for several
frames, and how long it holds tracks the firing interval rather than the frame
period — 39 ms held against 37.5 ms of firing at 800 rpm, 30 against 28.6 at
1050, 20 against 20.0 at 1500, 13 against 13.6 at 2200, and then it saturates
at the 10 ms frame period above about 3000 rpm where the engine fires faster
than the bus reports.

**The sharper form of the same measurement is in `docs/can-decoding.md` as
trap 6**, and it is the one to cite: expressed as crank angle rather than as
time, the gap is a **constant 180° from idle to 3200 rpm**, across a fivefold
change of speed, before the frame period stops being able to carry it. A
constant angle is a statement about the engine's geometry; an interval that
merely sits near the firing rate at one speed is a coincidence waiting to be
read as a mechanism.

**So each sample is the crank's mean speed across one cylinder's power
stroke** — a four-stroke four fires every 180°, so one such window contains
exactly one power stroke — which is what makes the depth of a dip a
per-cylinder quantity worth putting into an energy budget at all rather than a
smoothed average of four.

⚠ **That is geometry, and it is all the energy budget needs.** "Once per 180°"
and "once per firing event" are the same interval on this engine and no data
here separates them, so whether the ECU computes a fresh speed *for each
combustion* or simply updates on a fixed crank-angle boundary is not
established. ⚠ **An earlier version of this section claimed the combustion
reading**, on nothing but the interval agreeing with the firing rate. The
budget below is unaffected: it needs only that the window contains one power
stroke.

⚠ **And there is no cylinder identification**, which trap 6 also covers. But
the *structure* is testable even without a name, and **it is there** — see
*Is it one cylinder?* below, which finds a strong period-4 line in every
recording including the smoothest, and concludes from that that it is ordinary
cylinder-to-cylinder variation rather than a fault. ⚠ **An earlier version of
this paragraph said the opposite**, on an autocorrelation of the *step* series
at lag 4; differencing and the wrong series between them hid a line that a
periodogram of the values finds at 13–21× its local background.

⚠ **It also qualifies the p = 0.023 above, and in the honest direction.**
Crankshaft speed irregularity is the standard way an OBD engine management
detects misfire — so the ECU's counter and `idledips.py` are most likely two
readings of the same physical signal at different resolutions, and their
agreeing is less independent than a permutation test over two arbitrary event
series assumes. **That does not make the result worthless**: it identifies the
stumbles as the events the ECU itself calls misfires, which is what it was for.
It does mean the correlation is not a second, independent witness to the
misfire diagnosis, and this file should not be read as though it were.
⚠ **That detection mechanism is general practice, not sourced for this ECU**,
and no document in `docs/` establishes it.

### Is it one cylinder? — tested properly, and the answer is no

**The question is whether the roughness is one bad cylinder or all four
together**, because it decides where to look. It is testable: each update is
one 180° window and the cylinders take turns, so a cylinder that differs from
its neighbours **repeats every four windows** — 720°, one full cycle, the same
cylinder coming round. That is a period, and a period shows in a spectrum.

| pattern | period | frequency |
|---|---|---|
| one cylinder differing | 4 | f = 0.25 cycles/window |
| two differing, **opposite** in the firing order | 2 | f = 0.50 |
| two differing, **adjacent** in the order | 4, with a period-2 component | |
| **all four differing equally** | **none** | — |

⚠ **The last row is the one that matters most and it is a limit of the method,
not a result.** Four equally bad cylinders leave nothing periodic: the governor
holds the mean speed and every window is equally depressed. **"It is all four
together" cannot be confirmed or refuted here.**

**`python tools/idledips.py --cylinders`.** Power in the bin against the
*median of its neighbours*, because the governor puts a great deal of power at
low frequency and none of it is per-cylinder:

| log | blocks | **f = 0.25** | **f = 0.50** | f = 0.20 | f = 0.30 |
|---|---|---|---|---|---|
| `09_idle_60s_z1` (rough, 61 °C) | 18 | **13.1×** | 0.8× | 0.2× | 0.5× |
| `11_idle_noac_z1` (smooth, 73 °C) | 6 | **13.4×** | 1.1× | 0.1× | 1.5× |
| `18_coldstart_z1` (rough, cold) | 76 | **20.6×** | **19.6×** | 0.3× | 0.8× |
| `12_idle_ac_z1`, `17_drive_property_z1` | 1 | — | *too little settled idle* | | |

**The line at f = 0.25 is real and it is not subtle.** The two control
frequencies sit at 0.1–1.5× where the line is 13–21×, and shuffling the same
values within each block — which destroys order and keeps everything else —
brings it to about 1×.

**And the same table is the reason it is not the fault.** `11`, the smooth
recording, carries it **as strongly as `09` does**: 13.4 against 13.1. Read
the four phase slots directly and the same thing shows as a spread of a few
rpm between the strongest and the weakest cylinder, in every recording:

| log | windows | slots, rpm about the run's mean | spread |
|---|---|---|---|
| `09` rough | 382 | +2.26, −0.03, −2.48, −0.05 | **4.74** |
| `09` rough | 179 | +1.09, +2.60, −1.70, −2.99 | **5.59** |
| `11` smooth | 190 | +1.12, −2.18, −0.98, +1.44 | **3.62** |
| `11` smooth | 98 | −0.31, +1.75, +1.22, −1.72 | **3.47** |
| `12` smooth | 85 | +1.20, −0.19, −2.19, +1.45 | **3.64** |
| `18` cold | 306 | +1.82, +1.23, −2.32, −0.49 | **4.14** |

⚠ **One slot is one cylinder, but which one is unknowable and it is not the
same one between runs.** The absolute phase is lost at every missed window
(1.5 % of them, above), so these are a *shape* and never a name. Naming a
cylinder would need camshaft phase, which `What is NOT on the bus` covers, and
the firing order, which nothing in this repository sources.

**Three conclusions, in the order they are worth.**

1. **It is not one bad cylinder.** A single failing cylinder would put one slot
   far below the other three and would make the spread much larger on the
   rough recordings than the smooth ones. Neither happens: the shape has no
   consistent single outlier and the spread is **3.5–3.6 rpm smooth against
   4.1–5.9 rough**, which overlaps. ⚠ Those are the *biased* spreads; the
   unbiased comparison is below and it separates by 1.80×, not by nothing —
   but still by less than the roughness grade does. Against the energy budget above — one
   entirely failed power stroke is 33–57 rpm — a spread of 4 rpm is **of the
   order of a tenth of one stroke's work** between the best cylinder and the
   worst. ⚠ Order of magnitude only: a sustained offset that the governor has
   already equalised against is not the same quantity as a transient dip, and
   nothing here converts one into the other properly.
2. **So the per-cylinder structure is ordinary cylinder-to-cylinder variation,
   not a fault signature.** It is present in the smoothest recording this car
   has produced. Anyone reading a strong f = 0.25 line as "found the bad
   cylinder" would be reading the engine's normal state.
3. ⚠ **The one thing that does separate the recordings is period 2, and it is
   cold, not rough.** f = 0.50 is **19.6× in `18` and 0.8× and 1.1× in the two
   warm logs** — two cylinders opposite in the firing order behaving unlike the
   other two, from cold only. **`09` is the rough engine at 61 °C and shows
   nothing there**, so what this tracks is temperature and not roughness. It is
   one recording of one cold start, it names no cylinder, and **it is not
   evidence for a two-cylinder fault** — cold enrichment and uneven warming
   would produce it in a healthy engine too. Worth one line in a future
   cold-start recording; not worth a conclusion.

#### Could it tell a healthier engine? — partly, and worse than the grade does

**The forward-looking question, because the answer decides whether this ever
becomes a channel.** Two candidate statistics, and they behave very
differently.

⚠ **First, the trap that has to be cleared or the comparison is worthless.**
The plain spread between the four slot means is **biased upward by noise**:
four means of an engine whose cylinders are identical still have a range —
about 2.06 standard errors for four draws — so a run carrying ±1.4 rpm of
noise shows nearly 3 rpm of "spread" from nothing at all. **The bias is larger
on shorter runs**, so comparing a short healthy recording against a long sick
one this way *manufactures* a difference in exactly the direction that would
be believed. The unbiased figure is `var(slot means) − mean(SE²)`, floored at
zero, and `--cylinders` prints it as `sd_true`.

| log | runs | **mean `sd_true`** | range |
|---|---|---|---|
| `09_idle_60s_z1` rough, 61 °C | 4 | **1.72 rpm** | 1.51 – 1.92 |
| `18_coldstart_z1` rough, cold | 24 | **1.99 rpm** | 0.82 – 3.77 |
| `11_idle_noac_z1` smooth, 73 °C | 2 | **1.08 rpm** | 0.88 – 1.28 |
| `12_idle_ac_z1` smooth, 73 °C | 1 | **1.10 rpm** | — |

- **The strength of the f = 0.25 line separates nothing at all** — 13.4×
  smooth against 13.1× rough. As a health statistic it is dead.
- **`sd_true` does separate: 1.95 rpm rough against 1.09 smooth, a factor of
  1.80.** Real, but **worse than the roughness grade, which separates the same
  recordings by 2.71×** (*Grading the idle*). And it rests on **three smooth
  runs**, against twenty-eight rough ones.
- ⚠ **It is confounded with temperature exactly as everything else here is.**
  Both smooth recordings are at 73 °C; `09` is 61 °C and `18` is cold. `09`
  alone against the smooth pair is 1.72 / 1.09 = **1.58×**, so part of even
  that is the warm-up and not health.

**So it is not going on 0x604, and the reason is arithmetic rather than
taste**: it costs a byte and more state than the grade, and it buys a weaker
separation of the same two states. The byte is better spent on the grade,
which is what 0x604 carries — `frames.md`.

**What it uniquely could say, and why that still belongs in a capture.** The
grade says *the idle got worse*; it cannot say *why*. A cylinder going off on
its own later — an injector silting up, a coil failing — is precisely the
case where one slot would run away from the other three while the grade merely
rose. **That is a diagnosis and not a trend**, and this repository has already
settled where each belongs: the bus carries the trend, a capture carries the
diagnosis. `--cylinders` over a recording is the right home and no firmware is
involved.

**What the next drive is therefore asked for.** The healthy end of `sd_true`
is as unrepeatable as the rough end was: once the engine is well, nobody can
go back and record it sick. Three smooth runs is thin, and two of them are one
log. **Run `--cylinders` over the healthy idles and record the `sd_true` band**
— it costs nothing, the capture is being made anyway, and it is the only
chance to widen the well-engine side of the one comparison that separates.

**What this changes for the investigation: nothing points at a cylinder.** The
plugs remain the better evidence about which injectors deserve a closer look,
and this measurement neither supports nor contradicts them. What it does rule
out is the thing that would have been easiest to find — one cylinder doing
badly enough to explain the stumble on its own.

### The idle counter, frozen before the repair so the after-reading means something

**The question this answers: after the injectors, does the stumble go?** It is
worth setting up carefully because it is cheap to get wrong in a way that
looks like a result.

⚠ **A warm reading after the repair proves nothing, because a warm reading
already read zero before it.** `11_idle_noac_z1` and `12_idle_ac_z1` were
taken at 72.8 and 73.5 °C **on the old injectors** and both count zero. So the
after-measurement has to be taken in the states where the before-measurement
was not zero — **from cold, and at around 61 °C of oil.** That is why the
post-repair drive spread its idles through the warm-up.

**`tools/idledips.py` carries a second detector for it**, `dips_cheap()`,
shaped the way firmware would have to do it: a first-order baseline, a latch,
and the standstill-and-closed-throttle gate the torque rule already uses. Its
constants are **frozen**, and `test_idledips.py` has a test whose only job is
to fail if somebody changes them.

**Why frozen matters more than the constants themselves.** If the injectors
cure the idle, there will never again be a rough engine to fit a detector
against — and at that point *any* threshold reads zero. A detector tuned after
the repair to read zero measures nothing. So the numbers below are a
prediction, written while it can still be wrong:

| state | oil | before, `dips_cheap()` | predicted after |
|---|---|---|---|
| cold idle | 13–17 °C | **12.1/min** | ~0 |
| warm-ish idle | 61.5 °C | **11.6/min** | ~0 |
| hot idle | 72.8–73.5 °C | 0.0/min | 0, and it says nothing |
| a drive | — | 0.0/min | 0, and it says nothing |

**One minute of matched idle settles it.** At 11.6 a minute, seeing none in
sixty seconds has a probability of 7×10⁻⁵ if nothing changed. Three minutes
also resolves a *partial* improvement — halving rather than curing — at
p = 0.002. Three to five minutes is enough for both questions, and the
post-repair idles were that long.

**And it needs no firmware.** The next session records a bus capture anyway,
and the detector runs over the capture afterwards. **Nothing in `src/` is
involved, no frame layout changes and `S-AQY.TRI` is untouched** — putting the
count on the bus and onto the display is a separate want with a separate cost,
and it waits until the count has been shown to mean something.

**That want was built**, as the idle grade on 0x604 (`frames.md`), on the
maintainer's decision and before a healthy idle had been recorded. ⚠ **The
after-reading therefore has a second job the table above does not show.**
*Is the idle cured* is answered by zero or near-zero. *Is the count worth a
row on the dashboard* is answered by what a healthy engine's floor actually
is — whether a well engine trickles one or two a minute or none at all for
minutes on end — and that reading exists only while somebody is looking for
it. Both come out of the same three to five minutes of idle, and only if the
constants stay frozen through it.

⚠ **This is not a misfire counter and must not be called one.** Seven of the
44 dips had a misfire increment beside them; the other 37 may be unreported
misfires or may be something else, and no data here separates those. It counts
dips of engine speed at idle. Naming it after what it is thought to indicate
would be the same error as the label file's `(celkovy)`.

### Grading the idle instead of counting it — and the count's floor, measured

**The counter above has a floor it cannot see under, and this is how far under
it the information actually is.** `TRIP_RPM` is 20 rpm. Sorting the whole
deviation of a settled idle by the size of the step it came from —
`python tools/idledips.py --roughness --bands` — puts almost none of it there:

| log | 3–5 rpm | 5–10 | 10–20 | **≥ 20** |
|---|---|---|---|---|
| `09_idle_60s_z1` (61 °C, rough) | 9.4 % | 56.3 % | **31.0 %** | **3.2 %** |
| `18_coldstart_z1` (cold, rough) | 8.8 % | 55.0 % | **33.9 %** | **2.3 %** |
| `11_idle_noac_z1` (73 °C) | 23.3 % | 60.3 % | 16.3 % | **0.0 %** |
| `12_idle_ac_z1` (73 °C, A/C) | 29.4 % | 66.5 % | 4.1 % | **0.0 %** |

**The band that separates the states is 10–20 rpm, and the threshold sits just
above it.** Everything the counter can see is 2–3 % of what is happening on
the rough engine, and on the smooth recordings it is exactly nothing — which
is why those two read 0.0/min rather than reading *small*.

**What is actually being measured, before any arithmetic.** Engine speed on
0x280 is recomputed once per firing event (above), so each new value is
roughly *how fast the crank turned through one cylinder's power stroke*. The
step to the next value is therefore **how much that cylinder differed from the
one before it** — and at a settled idle, where nothing the driver does
explains any of it, that difference is combustion. The distribution of those
steps is the whole of the raw material (`--roughness --hist`):

| log | 0–2 rpm | 2–4 | 4–6 | **6–10** | **10–15** | 15–25 | > 25 |
|---|---|---|---|---|---|---|---|
| `09` (61 °C, rough) | 25.1 % | 24.7 % | 21.2 % | **21.6 %** | **5.9 %** | 1.4 % | 0.1 % |
| `18` (cold, rough) | 25.3 % | 26.1 % | 19.9 % | **20.9 %** | **6.2 %** | 1.5 % | 0.0 % |
| `11` (73 °C) | 34.7 % | 35.3 % | 18.0 % | **10.3 %** | **1.6 %** | 0.2 % | 0.0 % |
| `12` (73 °C, A/C) | 42.5 % | 35.2 % | 14.9 % | **7.1 %** | **0.4 %** | 0.0 % | 0.0 % |

**The two rough recordings agree with each other column by column, the two
smooth ones likewise, and they differ in the 6–15 rpm columns** — twice as
many 6–10 rpm steps and four to fifteen times as many 10–15 rpm ones. The
smooth engine piles up at 0–4 rpm where the rough one does not.

⚠ **None of this is visible by eye in a short excerpt.** Thirty consecutive
frames of `09` and of `11` look like the same engine; the rough log's excerpt
happens to contain an 11.5 rpm step and the smooth log's a 12.25 rpm one. It
is a difference of *distribution* over thousands of events, which is why it
needs a statistic and why watching the number on a display for ten seconds
will never show it.

**The grade is that table compressed into one number.** The measure is the
step between one firing event and the next, dead-banded and averaged:
`mean(max(0, |Δrpm| − 3))` over settled idle, on the gate the counter already
uses. `python tools/idledips.py --roughness`:

| log | grade | oil |
|---|---|---|
| `09_idle_60s_z1` | **2.12 rpm** | 61.5 °C |
| `18_coldstart_z1` | **2.12 rpm** | 12.8 → 17.2 °C |
| `17_drive_property_z1` | 1.38 rpm | 77.2 °C |
| `11_idle_noac_z1` | 0.96 rpm | 72.8 °C |
| `12_idle_ac_z1` | 0.60 rpm | 73.5 °C |

**The two rough recordings agree to three figures across a 45 °C spread of oil
temperature**, which is what makes 2.12 worth using as the anchor of a scale.
The contrast against the smooth pair is **2.71×**, and it is bought by the
deadband — `--roughness --deadbands` gives 1.58× at 0 rpm, 2.20× at 2, 2.71×
at 3, 4.16× at 5 and 8.52× at 8, while the smooth reading falls to 0.05 rpm at
8 and takes its own resolution with it. **3 rpm is the decision**: the largest
contrast that still leaves the smooth state well clear of the floor.

**And the deadband is now obvious rather than arbitrary.** Steps of 0–4 rpm
are half to three quarters of every event on every recording, rough and smooth
alike — they are the idle's own noise and they drown the part that differs.
Subtracting 3 rpm deletes them and leaves the 6–15 rpm tail, which is where
the two pairs of recordings actually part company.

⚠ **Three limits, and the first disqualifies the obvious reading of the
table.**

- **All five recordings are of ONE engine before the repair**, so what is
  measured above is the contrast between its *temperature* states, **not
  between a sick engine and a well one**. No recording of a well one exists.
  The table establishes the scale and its 100 point; it does not establish
  that the scale separates health, and the post-repair drive could not
  supply the other half because its idle was not healthy either.
- ⚠ **It is not a sub-threshold dip counter and must not be described as
  one.** At 796 rpm a four-stroke four fires 26.5 times a second, so a healthy
  engine dipping 5 rpm once a minute contributes about **0.001 rpm** to an
  average of 0.78 — invisible. What the grade responds to is the ordinary
  cycle-to-cycle consistency of the whole idle. That is a different quantity
  from "how many stumbles were there", and the fact that it separates these
  recordings better does not make it the same measurement.
- **It is not monotonic in temperature**, so "compare at the same temperature"
  is a requirement and not advice. Through `18`'s warm-up in 60 s windows
  (`--roughness --windows 60`) it goes 2.74 rpm at 25 °C of coolant, **down to
  1.36 at 37 °C**, and then climbs steadily to 2.45 by 63 °C. Nothing here
  explains the shape and no mechanism is offered for it.

**Repeatability, which is what decides whether a trend is readable:** on a
steady idle the grade scatters about **13–15 % between 10 s windows and 3 %
between 30 s windows** (`09`, `11`). Against a contrast of 171 %, a half-minute
of matched idle is ample — which is the property the count does not have at
all once it reads zero.

### Cold enrichment, measured

The fuel counter is absolute and in microlitres, so this needs no assumption:

| | flow | |
|---|---|---|
| first 30 s running | **927 µl/s** | 3.34 l/h |
| cold idle, ~928 rpm | 750 µl/s | 2.70 l/h |
| after the idle step-down, ~815 rpm | 383 µl/s | 1.38 l/h |
| last 60 s, ~803 rpm | 355 µl/s | 1.28 l/h |
| warm idle, `09_idle_60s_z1` at 796 rpm | 326 µl/s | 1.17 l/h |

**162 ml for five and a quarter minutes of standing still.** The idle speed
steps down from ~930 to ~815 rpm between 140 and 170 s, which is the ECU and
not the driver — the throttle byte never leaves 38.

### Two screens, and what they say

Photographed with the engine running, 411.6 s after the start:

| group 006 | |
|---|---|
| intake air temperature | **22.5 °C** |
| altitude correction factor | **0.0 %** |
| engine speed / load | 760 rpm / 24.2 % |

**That turns the volumetric-efficiency bound above into a figure.** The table
under *What "load" is a percentage of* spans 84–93 % because intake air was
unknown; 22.5 °C at no altitude correction picks the top row. ⚠ **It is not the
same reading** — 22.5 °C is the intake at idle after five minutes of standing,
and what that table needs is the intake during a full-throttle pull, which is
hotter. It bounds the answer from the cool end; it does not supply it.

| group 100 | |
|---|---|
| readiness bits | **00000000** |
| OBD status | 11000000 |
| coolant | 70.5 °C |
| time since engine start | 411.6 s |

**All eight readiness positions read zero**, which in VCDS's own convention
means every monitor has completed — so the new converter has been through its
tests and an emissions measurement would be accepted. ⚠ **That convention is
taken from the tool, not measured here**, and the OBD status byte is recorded
raw because nothing in this project decodes it.

### What the gap cost

**VCDS lost the ECU 4.2 s into the first log, during cranking, and did not
recover on its own.** The second log was started by hand and begins 129 s after
the capture did — so there is **no diagnostic data at all from the start
itself, or from the first 86 s of running.**

What that lost, specifically: **when misfire detection switches on.** The
cold-start procedure asked for exactly that and it is gone — detection was
already active by the time the second log begins. All that can be said is that
it was on by 30 °C of coolant.

**Next time, check the log is still running after the engine catches.** The
crash happened at the noisiest electrical moment there is, which is not a
coincidence worth relying on not repeating.

---

## The remap is a standing unknown, and it is not hypothetical

**This car has been chipped.** `can-decoding.md` and `frames.md` both carry a
warning about what a remap does to these channels; that warning describes this
vehicle rather than a hypothetical one, and both files now say so.

What is known: it was done years ago, and the tuner's own remark was that
there was nothing to be had at the top of the range. **Whether that was a
comment on naturally aspirated engines in general or on this engine already
being flat up top is not established**, and the difference matters — the second
reading would mean the shortfall being chased here is not new.

What a remap on a naturally aspirated engine can normally touch is ignition
advance and the full-load enrichment, worth a few per cent at best. **Taking
power away is not a normal outcome**, with one route that is not impossible:
advance pushed past what the current fuel or engine condition tolerates, with
the knock control pulling it back to less than it started with. The advance
logged above does not look like that, but knock retard itself was not logged.

**The consequence for this firmware is smaller but real.**
`TORQUE_CNM_PER_BIT` is derived by requiring this car's full-throttle plateau
to reproduce the two *factory* ratings — of a stock engine. This engine is not
stock. If the remap gained anything, the true ratings are higher, the plateau
is worth more Nm than the scale says, and the display under-reads by about as
much as the remap gained. That is a named bias of a few per cent in a known
direction.

**Returning the ECU to standard is not planned**, so this stays an unknown to
be reasoned around rather than removed.

---

## The service of 17 September 2026 — compression, and the plugs that came out

**The repair was split in two, and not by choice.** Spark plugs and ignition
leads went on at this visit; the injectors were still in transit from the UK
and followed separately. The post-repair drive was planned assuming one visit
and had a two-step experiment to read instead — what that cost, and the one
thing it bought, are below.

Rear shock absorbers, an air-conditioning recharge and several small items were
done at the same visit. None of them touch anything this file measures.

### Compression: 13 bar on all four, and the evenness is the result

**Measured by the garage, recorded here.** All four cylinders read the same.

⚠ **The absolute figure is the weaker half of this.** A cranking compression
number moves with the gauge, the cranking speed, the battery, the engine's
temperature and whether the throttle was held open, and none of those were
recorded. **The spread across the four is what survives all of that**, because
every cylinder saw the same gauge and the same crank in the same ten minutes.
It needs no factory specification to be worth something, which is just as well,
because no document in `docs/` holds one.

**What an even four rules out**, and this is the first time anything has:

- a burnt or badly seating valve on one cylinder
- a broken or collapsed ring pack on one cylinder
- a head gasket leaking between two cylinders

**All three were live candidates for "one cylinder behaves differently from its
neighbours", and all three are now off the list.** That matters more than it
looks: the misfire pathway in this file has rested on a leaking injector
throughout, and a mechanical fault would have produced the same burned-through
chamber, the same first-gear stumble and the same one-cylinder story. It no
longer can.

⚠ **It does not rule out everything, and three of the gaps matter here.**
Compression is a cranking-speed test: it says nothing about the injectors, it
does not resolve valve *timing*, and an even four is entirely compatible with a
small intake leak feeding every cylinder alike. **It removes per-cylinder
mechanical causes and nothing else.**

**It also corroborates the breathing argument from a completely different
direction.** *What "load" is a percentage of* puts this engine's real
volumetric efficiency at full throttle somewhere in 84–93 % and concludes that
"every value in it is a normally breathing engine" — a figure derived from mass
air flow, engine speed and the ECU's own load percentage. Compression is none
of those things and agrees with it. **Two independent measurements now say the
engine fills and seals its cylinders normally**, which leaves the gap under
*The gap that is left* squarely between combustion quality and the torque
scale, with the air path eliminated from both ends.

### The plugs: four years by date, under 1,500 km by wear

**The old plugs came out worn, with cylinders 1 and 4 further along than 2 and
3, and one of the four visibly worse than the rest.**
[`plugs-2026-09-17-removed.jpg`](photos/plugs-2026-09-17-removed.jpg) is the
four of them in the garage, all four firing ends dry and dark with carbon
rather than carrying the wet sheen of oil.

⚠ **THE POLICY ON PHOTOGRAPHS CHANGED HERE, AND IT IS WORTH TWO LINES BECAUSE
THIS PASSAGE USED TO SAY THE OPPOSITE.** It read *"the photograph is not kept
here … what a photograph is worth is written down, and the picture itself goes
stale in a drawer"*, and photographs are now kept in `docs/photos/`. **What
was right in that rule survives and is restated below**: a picture is not the
evidence and does not grade anything. What was wrong was the conclusion — this
file spends several sections lamenting evidence that perished, and a photograph
is the cheapest thing there is that does not perish. **The written judgement
remains the record; the picture is kept beside it so a later reader can see
what was being judged.**

⚠ **A photograph cannot grade fouling and must not be used to**, and that goes
for the one now linked above. Lighting, angle and which way a plug happens to
be turned move the apparent severity more than a real difference between two
cylinders would. **The owner handled them and the ranking is his, not the
picture's** — do not re-rank them off the file.

⚠ **And the picture does not carry the cylinder mapping.** It shows four plugs
loose in a cap, which is exactly the state the next section warns about. It
preserves their condition and nothing about their position.

**The distance is the finding, and it comes out of `vehicle-history.md` rather
than out of the plugs.** Those plugs were fitted in 12/2022 and the car has
covered about 1,500 km since — the figure that file derives from the per-year
table, and the reason it flags them as "old by date, nearly new by wear".

**Eroded electrodes and a carbon coating at that distance is not wear.** Plugs
are consumables measured in tens of thousands of kilometres, and these did not
get a tenth of that. **This is the same shape as the converter**: a part
replaced in 10/2017, found destroyed in 9/2026 against under 28,000 km. Two
different consumables, both killed by distance they never covered. **The engine
has been writing the fault onto every part downstream of it**, and the plugs are
the second piece of physical evidence in this file after the cut-open converter.

⚠ **"Sooty rather than oily" is worth one sentence and no more.** Dry carbon is
what a rich mixture or a weak spark leaves and wet oil is what a ring or a valve
stem seal leaves, so the observation points the same way as everything else
here — but plug-reading is a craft with a large subjective component, the
compression result already rules out the ring-and-valve half of it far more
firmly, and nothing is gained by leaning on the colour.

### The worst plugs name two cylinders — 1 and 4, and the question is closed

**This is the most actionable thing in this section.** *The old converter was
shown to the owner* says one burned-through chamber "fits one cylinder better
than four" and then, correctly, refuses to name which: exhaust flows mix in the
manifold, so the converter cannot identify anything.

**A plug does not mix.** It sits in one cylinder and records only that
cylinder. So the worst of the four is the first candidate identification of a
suspect cylinder this investigation has ever had — and unlike most of what
this file chases, **it was captured in time.**

**The answer is cylinders 1 and 4.** The garage removed the plugs at the
17/9/2026 visit and the owner has the ranking from them; it is the same pair
the section above records, confirmed rather than reconstructed. *Owner-reported
from the garage, not measured here.*

⚠ **An earlier version of this section asked for it as an open question** —
*"ask the garage while they still remember"* — while the section above already
stated the answer. **It is closed.** Do not ask it again; that has now cost two
sessions.

⚠ **The pair survived and the individual mapping did not**, which costs
nothing. `photos/plugs-2026-09-17-removed.jpg` shows the four loose in a cap,
so which single plug was worst of all four is gone. **Every reading below works
off the pair** — end cylinders, or companion cylinders on one coil output —
and none of them needs a singleton. The datum that mattered is the one that
survives.

**The prediction the pair still has to answer:** if the new injectors cure
everything, the extra fuel should have been going to 1 or 4. That is something
this set of parts can be held against, and it needs no plug in a bag.

⚠ **1 and 4 being the worse pair may be mundane, and the innocent explanation
has to be ruled out before the interesting one is entertained.** They are the
**end cylinders**, which on many engines simply run cooler and carbon up faster
than the middle two for reasons that have nothing to do with any fault.

**And there is a second reading that is not mundane, which this project cannot
currently settle.** On a four-cylinder, 1 and 4 are companion cylinders — they
reach top dead centre together — and a wasted-spark ignition fires them from one
coil output, with 2 and 3 on the other. **If this engine's ignition is wired
that way, "1 and 4 worse" is a signature of one coil output or its pair of
leads, not of one injector.**

**It is wasted-spark: settled by VW Self-Study Programme 233**, p. 5, whose
comparison table gives the AQY *"Static high-voltage distribution with 2 twin
spark ignition coils"* (the ATU has a distributor). A twin-spark coil fires
two cylinders together, one on compression and one on exhaust, so its pair
has to be two cylinders that reach top dead centre together. On an in-line
four those are 1 with 4 and 2 with 3. **So "1 and 4 worse" is one coil
output and its two leads.** ⚠ *Earlier text, kept for the record:* whether the
AQY is wasted-spark was not established by any document in `docs/`. The coil was replaced in 6/2026 and the
misfires outlived it, which is what moved ignition from cause to casualty in
this file — but the *leads* dated from 12/2022 and have only now been changed,
so the pairing question is live in a way it was not a month ago. **It is cheap
to settle**: the topology is visible on the car, or in the parts catalogue for
the ignition components. Settle it before reading anything into the pair.

**And the owner adds the dates that make the coil reading the stronger one.**
The plugs that came out went in in 12/2022; the coil they ran on until 6/2026
was **probably the original**. So those plugs spent about three and a half
of their four years on an old coil, and only the last three months on the new
one. If the ignition is wasted-spark, a weak output on the old coil wears its
two plugs harder for exactly that long, with nothing on the fuel side involved.
*Owner's recollection about the coil's age, not a record.* It does not
identify anything either. What it changes is the weight: **1 and 4 are now
weaker evidence against the injectors than this section first made them**,
and the new injectors not curing the idle is consistent with that.

### The calmer idle is not evidence, and the reason is in this file's own table

**The owner's impression after the visit is that idle is a little calmer.**
Recorded because impressions are what prompted every measurement here, and
discarded as evidence because it cannot survive the table under *The rough idle
is in the fixtures*.

**A warm idle already counted zero dips before anything was changed.**
`11_idle_noac_z1` and `12_idle_ac_z1` were taken at 72.8 and 73.5 °C **on the
old injectors and the old plugs** and both read 0.0 a minute. So a warm engine
is precisely the state where the before-measurement was already null, and an
impression formed in it has nothing to be calmer *than*. The states that were
not zero are **from cold, and around 61 °C of oil** — which is where any real
improvement has to show up and where nothing has been recorded since the visit.

### What the split costs, and the one thing it buys

**Cost: the next drive no longer has one variable.** The drive's
prediction — misfires to zero, stumbling gone at every oil temperature, the idle
adaptation moving toward zero — was written against a single change. If all of
that comes true after the injectors, **the plugs are now an equally good
explanation for any of it**, and no measurement taken afterwards can separate
them. Four-year-old fouled plugs misfire at low load and high vacuum, which is
the same signature the injectors are accused of.

**What it buys: a middle point exists, and only until the injectors go in.**
A cold start and a few minutes of idle recorded *now* — new plugs and leads, old
injectors — turns a two-point comparison into a three-point one and makes the
split an advantage instead of a confound:

| state | recorded on | what it would say |
|---|---|---|
| `18_coldstart_z1` | old plugs, old injectors | the baseline, already held |
| **a capture now** | **new plugs, old injectors** | **splits plugs from injectors** |
| the next drive | new plugs, new injectors | the result |

**It needs no driving and no hard running** — `tools/usbtin_capture.py`, one
cold start, five minutes, engine idling on the drive. `tools/idledips.py` reads
it afterwards with `dips_cheap()`'s frozen constants, against the 12.1 and 11.6
a minute in the prediction table under *The idle counter, frozen before the
repair*.

⚠ **It is perishable in exactly the way `18_coldstart_z1` was.** Once the
injectors are in there is no "new plugs, old injectors" car left to record, and
the question of which repair did what becomes permanently unanswerable. **The
owner has declined to measure for now and that is a legitimate call** — the
middle point is a nice-to-have and the verdict does not depend on it. It is
written down so that the choice is a choice rather than an oversight.

---

## The injectors and the fuel filter — 23 September 2026

**The second half of the repair, done by the owner at home.** Everything in
this section is owner-observed unless it says otherwise; nothing here is a
capture; the capture is *The post-repair drive*, at the end of this file.

### What went in

- **Four Bosch injectors, original and unused** — three still boxed, all four
  with their plastic caps on every end. **Their O-rings were replaced
  regardless**: the originals felt stiff and dry when a cap was eased off, and
  a seal that has aged on the shelf is not recovered by being new.
- **Fuel filter, Bosch `0 450 905 318`**, the same part number as the one that
  came off.

⚠ **The O-rings could not have been the fault this file describes.** The upper
ring seals fuel at rail pressure and a leak there puts petrol *outside* the
engine, where it is seen and smelt; the lower ring seals the injector to the
manifold, and a leak there admits **air**, which leans the mixture. Fuel
delivered into a cylinder with none commanded can only come through the
needle seat. Replacing the rings is insurance for the new parts, not a
repair of the old ones.

### The fuel lines were flushed, and ran clear

**The line from the tank was flushed with the filter off**, the pump run by
key cycles into a container under the car; then **through the new filter into
a container in the engine bay** before anything was reconnected to the rail.
**Clear petrol at every stage**, with no visible sediment and no separated
water. The container had held garden dirt, so the sample was not clean enough
to be conclusive — but nothing in it pointed at the tank.

**This is the first observation of the one stretch this file had never seen**:
the lines from the tank to the filter, never changed, which *A candidate ROOT
cause* leaves as the only place an upstream source could still be. **They are
clean now.** It says nothing about what passed through them before the tank was
replaced.

**The filter that came off was sound**: plastic housing, no corrosion, no wet
joint — unlike the corroded, leaking metal can of 12/2017 in
`vehicle-history.md`. It is the same type as the new one, which fits the
10/2022 purchase having been fitted, but **does not prove it**: nothing records
what type went on in 12/2017. The owner judged the question not worth pursuing.

### The old injectors — kept and photographed, not tested

**No leak test was run, on the old set or the new one.** A drip test on the
rail was not practical — the rail has to come off its supply hoses with the
regulator to be lifted out — and switching the ignition on with half the
intake dismantled was judged not worth the risk. A hand-held air test on the
bench was considered and not done either. **So there is still no direct
evidence of which injector, if any, was leaking.**

They were laid out in engine order and photographed; the owner has the
pictures, and they are deliberately not in `docs/photos/`. **Cylinder 1 is the
rightmost viewed over the bonnet.** By the owner's inspection **cylinder 1's
nozzle is the dirtiest inside and cylinder 4's the cleanest**; the photographs
independently confirm bright metal in the orifice of cylinders 3 and 4, where
the background shows which injector was in hand. The inlet screens are too
deep to judge from the pictures.

⚠ **A dirty nozzle is not a leaking seat.** Deposits at the nozzle change the
spray and the flow; whether the needle sealed cannot be seen. So of the two
cylinders *The worst plugs name two cylinders* points at, **cylinder 1 agrees
and cylinder 4 does not**, and neither is incriminated or cleared. The old
injectors are kept, labelled by cylinder, in case a bench test is ever wanted
— start with cylinder 1.

### The battery was disconnected, and `032` has moved

**The battery was off for the work**, deliberately: the fuel pump primes when
the driver's door opens, and an open fuel system is not somewhere to risk
that. **The owner reports that the adaptations have survived a disconnect
before**, which no measurement here establishes.

**`032` read afterwards: −3.1 % at idle, 0.0 % at part load**, against the
**−4.7 % / +1.6 %** of the baseline. ⚠ **An exact 0.0 at part load after only
idling reads more like a reset than a shift** — idle adaptation learns within
minutes of idling, part load cannot learn at all without driving. Either
reading fits. **The drive decides it: a part-load value that moves off 0.0
during the drive means it was reset**, and then `−3.1 / 0.0` is a new baseline,
not a result, and must not be compared with −4.7 / +1.6.

### Afterwards, at a warm idle

- **Started first time, no fault codes stored.**
- **Group `014`: about two minutes of warm idle, no misfire counted.** A short
  sample, and the warm idle already counted zero on the old parts — see *The
  idle counter, frozen before the repair*. It is not the test.
- **The idle feels not fundamentally different** — possibly less hunting, still
  slightly unsettled, and **the exhaust still gives an occasional puff, as
  before**. An impression, not a measurement: the display does not show it, the
  capture will.

⚠ **So the repair has not visibly cured the idle, and that is not yet a
verdict.** The adaptations may be relearning from zero, the car was warm, and
the symptom this file leans on hardest is the overnight cold start, which has
not happened yet. If the cold start and the capture come back the same as
before, the pump's check valve — see the note under *The start itself* — is
where to look next — the new injectors will then have eliminated
themselves, which is what they were bought to do.

---

## The post-repair drive and the MAF swap — 24 September 2026

**Plugs, leads, injectors, fuel filter and regulator new; then, the same
afternoon, the MAF.** The morning session is `19_postfix_drive_z1` (a 10 °C
cold soak, a cold start, three idles, coasts, held full-throttle pulls in 4th,
a hot idle) with `20`–`23` and `vcds/vcds-postfix-drive-003-014.csv`; the
afternoon is `24_mafswap_drive_z1` with the two `vcds-mafswap-*` logs.
`test/fixtures/README.md` has the session. What the drive settled for the
firmware lives where it belongs: the torque scale in `can-decoding.md`
question 8, the coolant scale beside the signal table there, the oil
cool-down points in question 10, the start and the idle grade in
`frames.md`, 0x604.

**The prediction written before it, scored.** The car pulls better, as
predicted. The mid-temperature misfires did **not** go to zero, and the idle
adaptation moved a long way *away* from zero — the MAF, below. The displayed
maxima were never the test they were meant to be, because the scale they are
computed with has since been measured rather than assumed.

### Engine health: better to drive, not cured, and one new finding

**The verdict blocks, all at the hot idle:**

| block | result |
|---|---|
| 046 catalyst | **katR1 OK** (376 °C) |
| 034 pre-cat sensor ageing | **R1-S1 OK**, period 0.53 s |
| 037 post-cat sensor | **R1-S2 OK** |
| 036 post-cat availability | **R1-S2 OK** |
| 070 evaporative valve | **TEV OK**, lambda deviation 0.0 % |
| 100 readiness | `00000000`, all monitors complete |

Every block reported its result immediately with the engine idling hot. No rpm
hold was asked for.

**The lambda adaptations moved a long way, in the rich direction:**

| 032 | idle | part load |
|---|---|---|
| old injectors | −4.7 % | +1.6 % |
| after plugs and battery disconnect | −3.1 % | 0.0 % |
| **after this drive** | **−16.4 %** | **−13.3 %** |

**With 034/036/037 all OK, this is a real
excess of fuel and not a sensor artefact. 070 rules out the purge.** Part load
moving off 0.0 confirms the earlier 0.0 was a reset. The adaptation learned
−13 % from zero in one drive.

**The shape of the correction matters more than its size.** −16.4 % at idle
against −13.3 % at part load is nearly the **same percentage** at flows about
four times apart: roughly 300 µl/s at idle against 1,000–1,300 cruising. That
is a *multiplicative* error, where every commanded millisecond delivers the
same fraction too much, or the air is measured the same fraction too high. An
*additive* source, a fixed trickle of fuel from somewhere, would be a large
percentage at idle and a small one under load. That rules out two candidates
on shape before anything is measured.

1. ~~**the new injectors are a different flow class from the originals.**~~
   **Ruled out.** Old and new are the same part: VW `06A 906 031 C`, Bosch
   `0 280 155 791`, photographed on both sets.
2. ~~**fuel vapour from the oil, through the crankcase ventilation.**~~
   **Ruled out, by the owner's arithmetic as much as by the shape.** It was
   proposed because it depends on oil temperature, and the misfires do. But
   the size does not work. Holding 13–16 % off *this* drive's commanded fuel
   means about **0.5 l of uncommanded petrol in 56 minutes**: about 60 µl/s
   at idle and 150 µl/s or more cruising. That would take oil diluted by a
   good part of a litre, which a dipstick smells at once, and this one smelt
   of nothing. The oil had also been changed only a few weeks earlier. And
   a breather is an additive source, which the shape above excludes
3. ~~one new injector leaking at the seat.~~ **Unlikely on the same shape
   argument**: a leak adds a fixed quantity and would dominate at idle. It
   stays possible only as a small contributor
4. **rail pressure too high.** Multiplicative, because the vacuum-referenced
   regulator holds a fixed pressure difference across the injectors and the
   flow follows that difference at every load. The regulator
   (`037 133 035 C`) and its vacuum hose are new since 7/2026
   (`vehicle-history.md`), before the −4.7 / +1.6 baseline, so they did not
   change between the readings. That makes it less likely, not impossible:
   a new regulator can be faulty. **A gauge on the rail settles it in
   minutes**
5. **the MAF reading high.** Multiplicative too. The air matched the earlier
   drive (load 78–81 %, 88 g/s), which rules out a *change*, not a unit that
   has read high all along. A swap with a known-good unit is the test

**Air per unit of commanded fuel at a warm idle, then and now.** Group 003
logs the MAF and 0x480 logs the fuel the ECU commands, so their ratio can be
compared across drives without knowing the fuel's density or the true
stoichiometric ratio:

| | MAF | commanded fuel | ratio | against August |
|---|---|---|---|---|
| August holds, old injectors (`vcds-01-002-003`, `09`/`11`) | 3.33 g/s | 326 µl/s | 10.2 | — |
| today, middle idle | 3.54 g/s | ~305 µl/s | 11.6 | **+14 %** |
| today, final hot idle after the hard drive | 4.44 g/s | ~300 µl/s | 14.8 | **+45 %** |

**At the middle idle the ratio has moved by the size of the trim.** That is
what candidates 4 and 5 predict, and it does not separate them: a MAF reading
high and a fuel system delivering more per commanded millisecond both raise
air per commanded fuel. **The jump within one drive, from +14 % to +45 %,
points at the MAF**, because the MAF is the part that responds to heat soak
while rail pressure does not. More electrical or fan load would raise the true
air at the hot idle, but it would raise the fuel with it, and the fuel stayed
at 300 µl/s. ⚠ Not every piece of this fits: a reading 25 % higher with the
same fuel and only +1.6 % of short-term lambda correction in group 001 does
not add up, and nothing here resolves it. **It is a pointer, not a
diagnosis.** The owner is considering a new MAF, and this is the evidence most
in favour of it. After the swap the same table is one capture and one 003 log
away.

**Neither 4 nor 5 explains why the correction jumped between the readings**
(−3.1 / 0.0 before the injectors, −16.4 / −13.3 after), since neither part
changed. That jump is the open problem, and the numbers here do not solve it.
Worth knowing when reading the next 032: the part-load cell had been reset to
0.0 and learned −13 % in this single drive, the hardest the car has had.
Whether it would have learned the same on an ordinary drive is not known.

**The cracked hose feeds the injector air shrouds, and it is not a suspect.**
VW Self-Study Programme 233 (*2.0-litre engine*, AQY/ATU, section *Fuel
injection*): on the AQY *"the injectors have an additional air shroud which
improves mixture preparation. An air pipe is connected to the intake pipe. Each
injector is, in turn, connected to the air pipe. The vacuum in the intake
manifold draws air out of the intake pipe"*, the fuel is *"finely atomised"*,
and the shroud *"is mainly effective in the part-throttle mode"*. (The ATU
variant has no air shroud.) So that air is taken from the intake pipe
downstream of the MAF and is **metered**. The hose runs from the intake pipe to
the metal air pipe along the injectors, near intake-pipe pressure rather than
manifold vacuum, so even a crack through it would leak little. **The owner
reports the cracking is in the surface rubber only**, on a thick-walled hose.
Nothing to do.

A MAF that over-reads would richen the mixture as well. But the MAF is from
2018, and the load and airflow match the earlier drive exactly (78–81 %,
88 g/s), so nothing on the air side moved.

**The misfire counter did not go away.** Group 014, at 1.7 Hz across the whole
drive:

| state | oil | counter |
|---|---|---|
| cold idle, first 2 min | 10 °C | **0** |
| the extra idle | 50–53 °C | 12–36, one run to **108** |
| middle idle, in band | 60–65 °C | 12 and 24, repeatedly for four minutes |
| a stop at about 08:28 | 71 °C | 12, 24 |
| during any pull | — | **0** |
| hot idle and step 18 | 70–72 °C | **0** |

**The thermal lever is still there**: worst at mid temperatures, zero cold at
idle, zero hot. The values now reach 108, against a before-maximum of 36.
**The prediction that the repair would take the mid-temperature misfires to
zero has failed.** Taken with the rich adaptation, the mid-temperature
misfiring is now at least as likely to be *rich* misfire on a mixture the ECU
has not finished correcting. The adaptation is still converging, so the second
032 reading, a few hundred km on, is worth more now than it was when it was
planned.

**The driver's account agrees with all of it**: the car pulls better in 1st to
3rd, loses breath above 5,000 in 4th (the MAF flattening above), and the idle
is better than before the work but still twitches occasionally.

**What this does to the converter depends on which candidate it is.** The
fuel counter reports what the ECU *commanded*.

- **Rail pressure too high (4):** every commanded millisecond delivers more
  than the ECU thinks, so **the counter, and every consumption figure on the
  display, reads 13–16 % low.**
- **The MAF reading high (5):** the ECU commands for air that is not there,
  then trims the excess off. What it commands after the trim is what the
  engine burns, so **the counter is right**.

**The next fill-up tells them apart**: litres at the pump against `TripFuel`
since the last fill. Either way nothing belongs in `config.h` yet. A correction
factor is only right for a mismatch that is going to stay, and every
candidate here is a fault to fix.

**Could the sensors be lying anyway? Possible, and the rear sensor argues
against it.** The ageing test in block 034 looks only at how fast the pre-cat sensor switches (a
period of 0.53 s), not *where* it switches. A sensor whose switching point had
drifted rich would pass 034 and would drive exactly these negative trims, with
the ECU leaning out an engine that was already right. But the post-cat sensor
is an independent witness, and at the hot idle it read **0.665–0.725 V**
(037, 036). An engine leaned out by a lying front sensor would fill the
catalyst with oxygen and pull the rear sensor down towards its lean end. It
was not there. ⚠ Those voltage bands are the general behaviour of a switching
sensor and are not from a document this project holds. For the sensors to be
the cause, both would have to be wrong in the same direction.

**The owner's decision: the oil and both oxygen sensors change together, at a
garage, and the measuring happens after.** That gives up the separation the
one-change-at-a-time order above would have bought: if the trims come back
to zero, nobody will know whether it was the oil or a sensor. It is taken
deliberately, because driving on a −16 % adaptation while the steps are
separated costs more than knowing which step fixed it. **After it,
everything in the fuel and combustion path except the lines from the tank
will be new**, so a trim that is still large points outside those parts, at:

1. **rail pressure**: a faulty or mis-specified regulator, even though it is
   new. A pressure gauge on the rail settles it in minutes, at idle with the
   vacuum hose on and off
2. **the MAF over-reading**: the air side matched the earlier drive (load
   78–81 %, 88 g/s), which rules out a *change*, not a unit that has read
   high all along. A swap with a known-good one is the test
3. **one of the new injectors leaking**: the owner's own remaining candidate

Two things can be set aside already. The coolant sensor is verified against
VCDS, so a wrong warm-up enrichment is out. The purge is out by block 070. An
exhaust leak ahead of the front sensor would pull the trims positive, the
opposite direction.

### The two screens nobody explained

- **Group 100 `Čas od Motor Start` read 1843.2 s at step 18.** The engine had
  been running about 57 minutes without a stop, and the capture has no restart
  in it. What the field counts is not known. Nothing depends on it.
- **Group 006's altitude factor read −10.2 % with the engine off** and 3.1 %
  hot at idle. The engine-off value has no meaning (load read 99.5 % at the
  same moment). 3.1 % against the 0.0 % of the earlier session is small, and
  nothing here explains it.

### The MAF swap, the same afternoon: the rich trim was the MAF

**What was changed.** The car's MAF housing is an original Bosch
`0 280 218 002` (VW `06A 906 461 A`). The sensing insert in it was a
separately fitted `F 00C 2G2 032`, recorded as bought in 2018 with no invoice.
The whole meter was replaced with a genuine VW `06A 906 461 A`, housing and
insert together as supplied, and the old unit is kept. **Fitting it needed the
battery disconnected, so 032 started again from 0.0 / 0.0.** Recordings:
`24_mafswap_drive_z1.txt` (filtered, about 30 min: a warm restart,
10 min of driving, an idle at 52–60 °C of oil, more driving including some
full-throttle pulls on a country road, and a hot idle) with
`vcds-mafswap-002-032.csv` and `vcds-mafswap-002-014.csv`.

**The adaptation learned small values and stopped there.** Read from the 032
log as it happened:

| | idle | part load |
|---|---|---|
| morning, old MAF, after one drive from 0.0 | −16.4 % | −13.3 % |
| **new MAF, first 10 min of driving** | 0.0 | 0.0 → **+3.9** in steps, briefly +4.7 |
| **new MAF, end of session (photo)** | **−3.1 %** | **+4.7 %** |

**Air per commanded fuel at a warm idle is back where August had it.** At
oil 55 °C: MAF 2.98–3.33 g/s against 310 µl/s commanded, a ratio of
**9.6–10.7**, against 10.2 in August and 11.6 / 14.8 this morning. **Candidate
5, the MAF, is confirmed**, and with it:

- the jump between the readings is explained. The insert was fitted before
  August, so it read the same fraction high throughout. Why the error grew
  after the injector change is still open. A worn element drifting with heat
  soak would do it, and the +45 % at this morning's hot idle points that way
- **the fuel counter is right**, by the argument under *What this does to the
  converter*. The MAF was reading high and the trim took the excess off, so
  the fuel the ECU commanded was the fuel burned. Nothing belongs in
  `config.h`
- rail pressure (4) is no longer needed as an explanation

**The misfire counter did NOT go away, and at hot idle it now counts more.** ⚠ That is the counter and not the engine. *Did the 20 % threshold mask the morning?* below quantifies it. Engine speed says the hot idle got *better*; see *The dip-against-counter correlation* below.

| idle | oil | samples non-zero | values | recognition `deaktiv.` |
|---|---|---|---|---|
| morning, hot | 70–72 °C | **0 %** | 0 | — |
| afternoon, warm | 52–60 °C | 48 % | 12–96 | 4 % |
| **afternoon, hot** | **70 °C** | **58 %** | **12–120** | **22 %** |

⚠ **The owner noticed that recognition drops to `deaktiv.` while driving and
engine braking, and also at idle.** The log confirms it at idle. What the ECU
disables detection for is not held here, so how far to trust a counter that
switches itself off is an open question. It stays in the record rather than
being explained away.

**The idle grade improved, but not to the August hot idle.**
`idledips.py --roughness --windows 60`:

| | oil | mean step | index |
|---|---|---|---|
| morning, warm | 50–65 °C | 1.4–2.5 rpm | 62–131 |
| afternoon, warm | 52–60 °C | 1.4–1.9 rpm | 73–100 |
| morning, hot | 70–72 °C | 2.0–2.7 rpm | 92–150 |
| afternoon, hot | 69–71 °C | 1.4–2.3 rpm | 68–121 |
| August, hot, before any of the work | 73 °C | 0.96 rpm | 48 |

**The owner's account agrees: the idle is calmer and no longer hesitates, but
the exhaust still gives an occasional puff.** That puff does not coincide with
the counter going `deaktiv.`. Full-throttle pulls feel unchanged, as they
should: at full load the ECU runs open loop and the trims hardly apply.

**The misfires are an idle phenomenon, and the owner's "only in first and
second" is the counter's hold.** Aligning each 014 log on engine speed with its
capture (best offsets 207.5 s and 802.5 s, mean |Δrpm| 23 and 36) gives road
speed and gear for every VCDS sample. Counting only the samples where the
counter *rose*, i.e. new events:

| | standing | 1st | 2nd | 3rd | 4th | 5th |
|---|---|---|---|---|---|---|
| morning, new events | **32** | 2 | 0 | 2 | 1 | 0 |
| afternoon, new events | **90** | 0 | 0 | 1 | 0 | 1 |
| afternoon, counter non-zero | 63 % | 5 % | 19 % | 2 % | 0 % | — |

**122 of 129 new events began at a standstill idle.** The non-zero readings
seen in 1st and 2nd are mostly the three-second hold of an event that began
while standing, carried into the pull-away. The gear is inferred from road
speed over engine speed, so a coast with the clutch down can be misfiled,
which covers the odd one in a high gear. **That points the second fault at
the idle regime**: low load, high manifold vacuum, little air. ⚠ **An intake leak fits the
regime and not the trims, as the owner pointed out.** Unmetered air leans the
mixture most at idle, where the air flow is smallest, and the ECU would answer
with a *positive* idle trim. The idle trim with the new MAF is **−3.1 %**. A
leak big enough to misfire should show up there, so the trims argue against
one. A small leak at a single runner is diluted four ways by the one oxygen
sensor and is not excluded, but it is not what the numbers point at. Weak
ignition at light load, and how far a counter that switches itself off can be
trusted, are no less likely. The owner will look at the old hoses anyway,
directly rather than through a capture.

**The trim argument is stronger than that paragraph gives it, and a smoke test
is not worth arranging for it.** *The owner's point, and it holds.* Two things
push the idle trim positive here, and it still reads −3.1 %:

- **a leak.** One runner leaking dilutes to a quarter at the one sensor, but
  a cylinder has to run a long way lean before it misfires. A quarter of a
  long way is still several per cent of *positive* trim, and the idle cell is
  where it would land.
- **the misfires themselves.** A cylinder that does not burn sends its oxygen
  down the exhaust, and the pre-cat sensor reads it as lean. At one to two
  events a minute that is a small push, but it is in the positive direction.

**A trim slightly negative against both of those says the mixture is, if
anything, a little rich**, not lean in one cylinder. What fits a neutral trim
is a fault that leaves the mixture alone: a valve not seating on a hot idle,
the spark, or the knock control pulling timing on one cylinder. The hoses stay
worth a look while the intake is open anyway; they are no longer a lead.

**So the rich trim and the misfires/puffs are two faults, and only the first
is solved.** Plugs, leads, injectors, fuel filter, regulator and now the MAF
are all new, and compression is even. What is left for the second is not
decided here. The cheap next reads are blocks 022/023 (knock retard per
cylinder) at a warm idle, and the dip-against-counter correlation that
this file ran on the cold start, repeated on `24`.

### The dip-against-counter correlation on `19` and `24`, and the counter moved more than the engine

**Done, as owed.** The same test the cold start got, over both 24 September
sessions: each 014 log aligned on engine speed with its capture (207.6 s and
802.3 s, the offsets above to a tenth), dips of ≥ 20 rpm from
`idledips.dips()` and counter increments both restricted to a standstill idle,
and 20,000 random draws from the same standstill-idle time for the null. The
script was a one-off and is not kept; everything it used is `idledips.py` and
the two fixtures.

| | `19`, old MAF | `24`, new MAF |
|---|---|---|
| standstill idle in the overlap | 1058 s | 483 s |
| dips ≥ 20 rpm | 319, **18.1/min** | 70, **8.7/min** |
| counter increments | 32 | 89 |
| median lag, increment to nearest dip | 0.59 s, against 1.24 s random | 1.21 s, against 2.44 s random |
| permutation p | 0.005 | < 5×10⁻⁵ |
| dips with an increment within 3 s after | **37 of 319** | **38 of 70** |

**The two signals still move together, on the new parts as on the old**:
the stumble is the misfire, as the cold start found. Dips near an increment
are no deeper than the rest (22–23 rpm either way), so depth does not tell a
counted event from an uncounted one.

**Split by oil temperature, the two sessions disagree, and not in the
direction the counter alone suggests:**

| oil | `19` dips/min | `19` counter rises/min | `24` dips/min | `24` counter rises/min |
|---|---|---|---|---|
| < 30 °C (cold idle) | 14.8 | **0.0** | — | — |
| 50–60 °C | 20.9 | 8.0 | 11.0 | 19.1 |
| 60–66 °C | 14.6 | 1.9 | 5.1 | 3.6 |
| 66–80 °C (hot idle) | **20.0** | **0.3** | **8.1** | **9.4** |

(A single event raises the counter over more than one VCDS sample, 12 → 24 →
36, so "rises" over-counts events. That is the same in both columns.)

- **Engine speed says the hot idle got better with the new MAF**: 20.0 dips a
  minute down to 8.1, and the roughness grade in the table above agrees.
  The earlier line *"at hot idle it is now worse"* was the counter's reading and
  not the engine's.
- **The counter went the other way**: close to nothing to about nine a minute,
  on an engine that was stumbling less. So between the morning and the
  afternoon, **the ECU's detection itself got more sensitive**. It also counted
  nothing at all through the morning's cold idle, where the dips ran at 14.8 a
  minute.
- ⚠ **Why is not established.** The cause offered here is a hypothesis: on
  this kind of ECU, misfire thresholds are commonly mapped against load, and the
  old MAF over-read the idle air by 14–45 %, which puts the ECU in a different
  load cell. Nothing in `docs/` sources that. What *is* measured is that
  **the counter reads differently on the two MAFs at the same oil temperature,
  and by more than the engine does**, so a before/after comparison across the
  swap has to use engine speed rather than 014.
- **Nor is every dip a misfire.** `24` has 32 of its 70 dips with no increment
  after them, and nothing here can say whether the counter missed those or the
  engine did something else.

**What it means for the next steps:** the idle fault is real and still there
after the MAF, at about half the rate of the morning. Every combustion part
has now been changed, the lambda trims are near zero and the sensors pass
their own tests. So what is left is outside the fuel and ignition parts:
air getting in past the MAF, the valvetrain at a hot idle, or the ignition
wiring pairs if the coil question above comes back wasted-spark.

### The first drive with 0x604 on the display — 24 September 2026, evening

**`IdleHealth` moved between 80 and 140 over the drive**, read from the
driver's seat and not logged, **with no oil temperature noted beside it**.
On the day-one table in `frames.md` that is the new-MAF band (68–121 hot,
73–100 warm), which is the old engine's 100 and not August's 48. **The owner
feels the idle is calmer in some way beyond the engine speed**, and offers it
as possibly placebo. It need not be. The rich trim the MAF fixed made the idle
hesitate, and the owner reported that gone that afternoon, but `IdleHealth`
grades one firing against the next and cannot see a slow hesitation. So the
two can both be true.

### Knock retard per cylinder: cylinder 4, and only cylinder 4 — 24 September, evening

**Groups 022 and 023 logged over a drive of about nine minutes**
(`vcds/vcds-knock-022-023.csv`; VCDS dropped at the start again, and the first
file, `-aborted-`, is the engine standing still). No bus capture was running,
so nothing here aligns with engine-speed dips.

| cylinder | samples retarded | largest retard |
|---|---|---|
| 1 | 0 of 952 | 0.0 °CA |
| 2 | 0 of 952 | 0.0 °CA |
| 3 | 0 of 952 | 0.0 °CA |
| **4** | **41 of 952, in 16 separate events** | **6.7 °CA** |

**Every event has the same shape**: a step of 4.5–6.7 °CA, then a recovery
of about 0.75 °CA per sample back to zero within a few seconds. That is knock
control reacting to something and then giving the timing back, not a
constant offset.

**Where it happens:** 960–2000 rpm at 18–56 % load, which is pulling away and
accelerating at low engine speed. **Never at idle** (0 of 443 idle samples),
never above 2500 rpm, and none of the 54 samples above 50 % load at higher
engine speed.

**What it says, and what it does not:**

- **It names a cylinder.** This is the first name the investigation has that
  comes from the ECU and not from a plug or a mixed exhaust. Cylinder 4 is also
  in the 1 and 4 pair whose plugs were worse.
- ⚠ **Knock control names what the sensor hears, not what caused it.** Either
  cylinder 4 really knocks at low speed and part load, for example running
  leaner or hotter than the others or carrying deposits, or a mechanical noise
  lands in cylinder 4's knock window, and a lifter or something loose near that
  cylinder would do that. The log cannot separate the two.
- ⚠ **It does not explain the idle misfires by itself.** The retard happens
  off idle and the misfires at idle. One cylinder that is wrong in a way that
  shows up in both regimes would link them; nothing here proves it is the same
  cylinder.
- The remap is relevant here. Whatever it did to part-load advance applies to
  all four cylinders, so it cannot explain one cylinder alone. It can explain
  why this engine sits close enough to the knock limit for one cylinder to
  cross it.

**Swapping parts tells cylinder from part.** Swap the plug from cylinder 4 with
cylinder 2 and log 022/023 again on the same kind of drive. If the retard moves
to cylinder 2, it was the plug; if it stays on 4, it is the cylinder or
something near it. The same swap works for the injector, at more effort. A
bus capture beside the next log costs nothing and lets the events be aligned
with engine speed.

#### Why cylinder 4 — what knock control is, and what can fool it

⚠ **How knock control works is general engine-management knowledge, not
from a document this project holds.** This ECU's own documentation is not in
`docs/`. How many knock sensors the AQY has is now settled from SSP 233 (two;
see *What the web adds*), but where they sit is not.
Everything below that describes the mechanism is marked as such; what is
measured is the log.

**The mechanism, in general.** A knock sensor is a piezo accelerometer
bolted to the block, and it hears the whole engine at once. The ECU gives
each cylinder a *window* of crank angle after that cylinder's top dead centre,
using the crank sensor for angle and the camshaft sensor for which of the two
revolutions it is. Only what the sensor hears inside that window is scored,
against a reference level learned per cylinder, because each cylinder sits at
a different distance from the sensor and sounds different through the block.
When the score exceeds the reference, that cylinder's timing is pulled back
by a step and then returned a little at a time. That is exactly the shape the
log shows.

**So "cylinder 4" means "the cylinder 4 window", not "a noise from cylinder
4".** Anything that makes a sound at the same crank angle on every cycle
gets booked there, whichever part of the engine it comes from.

**What the onsets have in common, measured.** 13 of the 16 begin on a sharp
rise in load, mostly from 9–15 % (the overrun, fuel cut) to 30–53 % within
one or two samples. Several also have engine speed falling fast just before,
2200 → 1360 rpm, which is a gearchange. **So the typical event is pressing
the pedal again after coasting or changing gear.** Such a rise happens in
about 120 samples of this log between 900 and 2500 rpm, so it is followed
by retard roughly one time in ten.

**That all 16 land on one cylinder is not chance.** A noise at a random
crank angle, a clunk from the engine rocking on its mounts, say, would
fall in the four windows about equally. Sixteen out of sixteen on one
cylinder by chance is about 1 in 10⁹.

The candidates, and what each predicts:

| candidate | fits | against it | cheap test |
|---|---|---|---|
| **real knock in cylinder 4 at tip-in** | tip-in is the classic moment: fuel returns after a cut, the port wall film is not built up yet, so the mixture runs briefly lean at full part-load advance. One cylinder being a little leaner or hotter than the others is enough for it to cross first. In general, the end of the block furthest from the coolant inlet runs hottest, but which end that is on the AQY is not established here | several onsets at only 18–25 % load, where real knock is unusual | ~~fuel with a higher octane rating~~ **already the case: the owner has run 100-octane fuel for a long time**, five points above the RON 95 SSP 233 specifies, and the retard happens on it anyway. See below |
| **a noise at a fixed crank angle** | a lifter ticking, a valve seating, or an injector closing. In general, the injector of the cylinder that fires just before 4 injects while 4 is in its power stroke. Every one of those repeats in the same window every cycle | nothing in the log points at one | a mechanic's stethoscope along the head on a tip-in; octane changes nothing |
| **the knock sensor or its wiring** | the owner's own suspicion. A sensor that is loose or corroded at its face couples the block less well, and a damaged screen picks up interference | a dead or open sensor usually sets a fault code and retards **all** cylinders to be safe. No code is stored and three cylinders read zero, so the sensor is working. One mechanism would still pick out one cylinder: if 4's learned reference is the lowest, any extra noise crosses its threshold first | check the sensor's mounting torque and connector; no code means it is not dead |
| **reference levels relearning** | the battery was disconnected twice this week, which in general also resets knock control's learned values | would fade over the next few hundred km | log 022/023 again later, on the same kind of drive |
| **the new plugs** | a plug that is not fully torqued runs hot, and a hot plug can cause knock in its own cylinder | all four are new and the same type | **swap plugs 4 and 2**: if the retard follows the plug, it is the plug. At the same time check that plug 4 is at the correct torque |

**What does not fit: intake air.** A leak at cylinder 4's runner would make
it lean, and lean knocks more easily. But the owner is not taking the intake
apart again, and the trim argument above says a leak big enough to matter
would show. One cylinder leaner by a few per cent would hide in the trim; that
could make it knock on a tip-in but would hardly make it misfire at idle.

**The octane test has in effect already been run, and it weakens real
knock.** *The owner reports running 100-octane fuel for a long time*, so
the log above was taken on fuel with five points more knock resistance than the
engine is specified for. Real knock at 18–56 % load on that fuel would need
something seriously wrong in cylinder 4: heavy deposits, a hot spot, or a
cylinder far leaner than the others. That is not impossible, but **it moves the
weight towards a noise or the sensor side**: the exhaust manifold, the knock
sensors' mounting, the earth straps, a lifter. Group 026 is now the most
useful single read. ⚠ The remap is the caveat. If it was calibrated to use
the octane, its part-load advance may sit higher than stock, and then 100
octane is the baseline rather than a margin.

**Is it harmful?** 16 events of 4.5–6.7 °CA with the timing given back within
seconds is knock control doing its job. It costs a moment of torque on a
tip-in, and nothing in the log is sustained. It is a lead, not an emergency.

**Order, cheapest first** (the web section below adds to it: log 020 with
026 instead of 022/023, look at the exhaust manifold, clean the earth straps):
the plug swap with a torque check; a look at the knock sensor's mounting
and connector if it is reachable without the intake off; then, if it is
noise, a stethoscope. Every repeat log wants a bus capture beside it.

#### What the web adds — 25 September 2026

A search for other people's cases. **Forum threads are evidence, not
specifications**, and most of the English VW forums refuse automated
reading, so what follows is what could actually be read and is labelled by
where it came from.

**From a VW document, VW Self-Study Programme 233** (*2.0-litre engine*,
AQY/ATU), p. 5 and the system overview on p. 18:

- **The AQY has two knock sensors, G61 and G66** (the ATU has one). Which
  cylinders each one covers is not in the document. This corrects the
  "one sensor that hears the whole engine" of the section above: each
  sensor hears the whole engine, but the ECU can weigh two of them.
- **Motronic 5.9.2**, with a Hall sender G40 on the camshaft for phase.
  If G40 fails, *"the ignition advance angle is retarded as a safety
  precaution"*, for all cylinders. One cylinder retarding is therefore not
  a G40 fault.
- **Fuel: RON 95.** So 98 is not required, and the octane test above is a
  test, not a fix.
- **Twin-spark coils.** See *The worst plugs name two cylinders*.

**From Ross-Tech's list of VCDS measuring blocks** (groups 020–029): group
**020 carries the retard of all four cylinders in one group**, and group
**026 the knock sensor voltage per cylinder**. The 022/023 pair can
therefore be replaced by 020, which frees a group for 026 in the same log.
**026 is what separates noise from knock**: a cylinder 4 whose voltage sits
above the others all the time points at a noise or at the sensor, while one
that sits with the others and spikes on tip-in points at combustion.

**From forums, and only as leads:**

- **Knock sensor mounting torque is quoted as 20 Nm** on several VW threads,
  with the note that a piezo sensor reads differently when it is under- or
  over-torqued. That figure is from forum posts and not from a VW document.
- **A long Polish thread on AQY idle vibration** (forum.vwgolf.pl,
  t=522030, 166 posts) has the same picture as this car: a stumbling warm
  idle that feels like missed sparks, smooth when driving, no fault codes,
  and plugs, leads, coil, intake gasket, throttle clean and adaptation, MAF
  check, thermostat and coolant sensor all already changed. **The original
  poster's fix was a cracked exhaust manifold, five cracks, welded**, which
  also cured the rough cold starts and high consumption. Other posters in
  the thread fixed theirs with genuine leads instead of aftermarket ones, a
  Bosch coil, a holed crankcase breather hose, or by cleaning the engine
  earth straps. Several were never solved.

**Why the manifold is worth a look on this car too.** A cracked exhaust
manifold is the one candidate that could link both findings: an exhaust leak
ticks once per cycle at a fixed crank angle, which knock control books to
one cylinder's window, and it sits ahead of the pre-cat sensor. ⚠ The trim
here reads −3.1 %, and air drawn in ahead of the sensor would normally push it
positive. The link is a hypothesis. ⚠ **Whether the September exhaust job
replaced the exhaust manifold itself is unclear in these documents.** *The
occasion* says "the manifold", while `vehicle-history.md` lists the cat,
silencer and gaskets. If the manifold is original, it is a 26-year-old part
this repository has never looked at. Cracks show as soot tracks, and a leak
ticks audibly on a cold start before the metal expands.

**Earth straps** are the cheapest item on the forum list. The knock sensor
signal is a few hundred millivolts measured against the ECU's ground, and a
poor engine earth adds noise to it and weakens the spark. Cleaning them
costs a wire brush.

### What `deaktiv.` in group 014 is: a load threshold

**The owner asked whether detection switching itself off correlates with the
misfire numbers. It correlates with the load, and cleanly.** Across both 014
logs of 24 September, all running samples, by the ECU's own load figure from
the same group:

| load | `19`, deaktiv. | `24`, deaktiv. |
|---|---|---|
| < 20 % | **1,275 of 1,299** | **354 of 354** |
| 20–25 % | 109 of 992 | 78 of 913 |
| ≥ 25 % | 165 of 3,392 | 52 of 450 |

**Below about 20 % load, detection is off, almost without exception.** That is
all of the overrun (every one of 516 fuel-cut samples in `19` and 77 in `24`),
which is why the owner sees it while engine braking, and most of rolling with
the pedal up. Above it, the few `deaktiv.` samples fall
on transients.

**At a standstill idle it only happens in `24`, and only because the new MAF
put the idle load right on the line.** In `24`, 45 of 45 standstill idle
samples at 19.x % load read `deaktiv.`, 30 of 117 at 20.x %, and 3 of 689
at 21 % and above. Nearly all of them are one 30 s stretch at the end of the
session, on a hot idle with the load at 19.5–20.3 %. In `19` the old MAF
over-read the air, so the idle load sat mostly at 23–44 %, and none of its
standstill idle samples read `deaktiv.` below 21 %.

**The counter's values do not predict it.** Detection switched off at idle
after a zero on 5 of 7 occasions, not after a run of counts. Once it is off
the counter reads zero, so `deaktiv.` samples showing few counts is a
consequence and not a correlation.

**What this changes:** on a hot idle with the new MAF, **the ECU may simply not
be looking** part of the time. A zero from 014 there does not clear anything,
which is one more reason to judge the idle by `IdleHealth` and engine speed
rather than by 014. ⚠ The threshold is read off two logs of this car; it is
not from a document, and the exact figure may depend on engine speed or
temperature.

### Did the 20 % threshold mask the morning? Re-running `19` as if it had the new MAF

**The owner's question:** the morning looked better by the counter and worse
by engine speed. Could the new MAF have simply put the idle under the 20 %
threshold, so that the afternoon is not comparable? The question was run as
a simulation.

**How.** The old MAF's over-reading is measurable sample by sample in `19`:
air per commanded fuel at a standstill idle, MAF g/s from group 003 over the
0x480 flow, against the new MAF's **10.45 g/ml**, which `24` holds at every
oil temperature. That gives a factor *k* for each moment. The load `19`
would have shown on the new MAF is its load divided by *k*. The gate is the
one `24` measured: always off below 20 %, off 26 % of the time at 20.x %, and
on above that. The script was a one-off; its inputs are the two fixtures and
the two 014 logs.

| oil | *k* in `19` | idle load, real → simulated | `deaktiv.`, simulated | counter rises/min, real → gated | `24`, real |
|---|---|---|---|---|---|
| 40–60 °C | 1.09 | 24.2 → 22.2 % | 3 % | 8.4 → 7.6 | 19.0 |
| 60–66 °C | 1.10 | 24.2 → 22.3 % | 0 % | 1.9 → 1.9 | 3.6 |
| 66–80 °C | **1.40** | 29.6 → 21.3 % | 9 % | 0.3 → 0.3 | 9.7 (10 % `deaktiv.`) |

**The threshold explains almost nothing.** Even on the new MAF, the morning
idle would have sat just above 20 % and lost at most a tenth of its detection
time. The masking the owner suspected is real in kind but small in size,
about the same tenth in both sessions.

**What differs is how many counts the ECU gives per stumble**, the same
events counted on engine speed:

| | `18`, cold start, 11/9 | `19`, morning | `24`, afternoon |
|---|---|---|---|
| counter rises per dip ≥ 20 rpm, standstill idle | 0.21 | **0.02–0.38** | **0.71–1.74** |

`18` and `19` agree with each other. `24` counts **five to fifty times more
per dip**, so the afternoon's worse counter is detection sensitivity, and
the gate is too small to account for it. What moved the sensitivity is not
established: the load-mapped thresholds proposed earlier, or the battery
disconnect for the MAF resetting whatever the ECU learns for misfire
detection. That learning is general engine-management knowledge, not a
documented property of this ECU.

**What the old drives would read on the new MAF's counter.** If the
afternoon's counts per dip are applied to the morning's dips, band by band,
that is 38, 10 and 24 counter rises a minute against the afternoon's 19, 3.6 and
9.7. ⚠ That is a model: it assumes a morning dip is the same kind of event as
an afternoon one. The measurement underneath it needs no model and does not
depend on the ECU:

| oil | dips/min, `19` morning | dips/min, `24` afternoon | change |
|---|---|---|---|
| 40–60 °C | 22.1 | 10.9 | **−51 %** |
| 60–66 °C | 14.5 | 5.1 | **−65 %** |
| 66–80 °C | 21.4 | 8.7 | **−59 %** |

**So on the one ruler that is the same in both sessions, the new MAF about
halved the idle stumbles, and the counter's "worse" is the ruler changing.**
The earlier conclusion that the repair and the MAF made the idle worse
was read off the counter and is withdrawn. ⚠ It is one morning against
one afternoon, and the afternoon also had more heat soak and a relearn
behind it. The plausible mechanism is that an erratic, over-reading MAF
signal at idle was itself causing some of the stumbles, which the swap
removed. What is left in `24` is the residual fault.

### `IdleHealth` at a known temperature — 24 September, evening

**60–70 at 69 °C of oil, sometimes over 100.** The first reading with the
temperature beside it. Against `frames.md`'s day-one table that is the bottom
of the new-MAF hot band (68–121), still above August's hot idle at 48. One
reading from the driver's seat, not logged.

**Later the same evening: 57**, the lowest this display has shown, and
close to August's 48 before any of the work. Owner-reported, **at 72 °C of
oil**, which is the same state as August's 48 (73 °C), so the two compare
directly. The morning's hot idle on the old MAF graded 92–150 at 70–72 °C.

⚠ **How far that comparison goes, since the owner asked.** August's 48 is
`11_idle_noac_z1`, **22 s of settled idle in a single VCDS hold**. That is
shorter than the 30 s `IDLE_CONVERGE_S` the device waits before it publishes
at all, and the grade scatters 13–15 % between 10 s windows. The A/C-on hold
beside it graded 29. It was on the old MAF, but in August that MAF still read
right: air per commanded fuel was 10.2 against the new one's 10.45, and the
over-reading only appeared after the injector change. So on the MAF the
two are comparable. On length they are not: **57 against two short holds of
48 and 29 says the hot idle is back in August's neighbourhood, not better
than it.** And it is not the healthy engine this index still lacks, because
August's idle stumbled too, only less at that temperature. The owner's verdict
that the engine is subjectively in its best state yet is not contradicted by
any of this.

### The first long drive on all the new parts — 25 September 2026

**About 100 km, and the owner's verdict is that the car drives well and
definitely better than before the repairs.** Mostly steady motorway at
4000–4500 rpm, five minutes held at 4500, brief excursions to 5000, no
fault codes and no hesitation. Not logged. It closes the old full-load
lamp question as far as one drive can; see *The historical fault*, above.
The idle fault is a separate question, and this drive says nothing about it.

### What is owed, none of it urgent

- **Group 032 again, a few hundred kilometres after the MAF swap**, one
  photographed screen, no session: it reads the new MAF's adaptation after it
  has settled. The swap reset it to 0.0 / 0.0 and it had learned −3.1 % /
  +4.7 % by the end of the afternoon. Easy to forget, and it is the one reading
  that says whether the rich trim is really gone.
- **Blocks 022/023 again, after swapping cylinder 4's plug with cylinder
  2's**, with a bus capture running. The first log is above: cylinder 4
  retards and nothing else does. This read was originally planned as the cheapest
  read on the idle misfires. Log them together rather than photographing a screen, both
  at a standstill idle at 50–60 °C of oil, where `24` had the most events, and
  on a pull under load, where knock control does its real work, with a bus
  capture running so the log can be aligned on engine speed. What each outcome
  means:
  - **all four at zero at idle and close together under load**: knock control
    is not part of the idle fault. A clean result, and worth having. ⚠ Zero
    at idle alone clears less than it seems, because knock control may simply
    not act at idle. The pull is what makes it a clearance.
  - **one cylinder retarding at idle, or persistently more than the others
    under load**: that names a cylinder, the first name this investigation
    would have that does not depend on a plug or on the manifold mixing. ⚠
    It names either a cylinder that knocks or a noise the knock sensor hears
    near that cylinder. A ticking hydraulic lifter is exactly such a noise,
    so a retard confined to idle points at the valvetrain as readily as at
    combustion.
  - **retard that comes and goes with the dips**: timing pulled off at the
    moment of the stumble would itself cost work in that power stroke.
    Alignment with the capture is what shows it.
- **The old intake hoses, looked at directly** rather than through a capture.
  The idle trim argues against a leak big enough to misfire, and a small one at
  a single runner is not excluded.
- ~~The dip-against-counter correlation, repeated on `24`.~~ **Done**, in the
  section above: the signals still correlate, and the counter's sensitivity
  changed with the MAF.
- **`IdleHealth` with the oil temperature beside it.** A reading without it
  cannot be compared with anything.

The oil change and the oxygen sensors were set aside once the MAF explained
the trim.

**Until the idle fault is found, the owner avoids long idles**: the misfires
are an idle phenomenon, and the exhaust has already paid for one of them once.
`IdleHealth` on the display (0x604) is the trend to watch while the hoses and
the other reads are worked through -- at a comparable oil temperature, or the
comparison says nothing.

---

## The torque scale — settled, and not by this file's route

**This section used to say what would settle `TORQUE_CNM_PER_BIT`**: a capture
of b7 and the fuel counter beside a VCDS 003 log over held full-throttle pulls,
with the air-fuel ratio taken out of the argument. The pulls happened on
24 September, and the scale was settled more directly than that: b7 reached a
plateau, 185 at 2400 rpm and 191 at 5200 in 4th, and with the drag held in
bytes the two factory ratings agree on 1.055–1.061 Nm/bit. The firmware ships
1.06. `can-decoding.md` question 8 has the numbers; the air-and-fuel route is
not needed and nothing here is owed to it.

What this file's efficiency argument still contributes is the direction: the
earlier display peak of 117 Nm was implausibly low for the air the engine
measured, and at 1.06 the same b7 reads about 30 % higher. The two routes point
the same way.
