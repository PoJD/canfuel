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

**One procedure hangs off this file:** `docs/next-drive.md`, the session
after the injectors, plugs and leads are changed. Its results land here.

**The before-recording has no procedure in the tree and is not missing one.**
It was a one-shot, it was followed, and a spent procedure kept around becomes
a diary. What it produced is `test/fixtures/18_coldstart_z1.txt` and the two
VCDS logs beside it, read in *The cold start* below; everything it taught
about running the after-session is in `next-drive.md`. `git log` has the steps
themselves if the wording of one is ever wanted.

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
position and it is the right one — `next-drive.md`, *The four blocks that give
verdicts*, is what produces them, and they are absolute rather than
comparative, so they need no baseline this car can no longer provide.

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

**The car is now parked until the injectors arrive**, which restores the one
condition `next-drive.md` needs and had lost: an overnight stand with nothing
disturbing it. It also means the tank stays as it was filled — see
`refuel-reset.md`, *The 2026-09-19 fill*, and `next-drive.md` step 4a.

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
`b7 = (Nm + 6.74 + 0.004820 × rpm) / 0.74`, from `TORQUE_CNM_PER_BIT` and the
drag line in `config.h`, with `TORQUE_TRIM_PCT` at zero. **The rpm band is the
whole of the uncertainty**; everything else is arithmetic. This is not a
substitute for the capture and `next-drive.md` steps 13–14 are unchanged by
it.

**What it is worth anyway.** `tools/b7scan.py` puts the largest b7 this engine
has ever been *seen* to make at **185**, out of three wide-open bursts that
were every one of them still climbing when the throttle shut. A steady 117 Nm
above 4,000 rpm implies b7 near **196** — higher than anything recorded, and
for the first time **not still rising when it was read**. `next-drive.md`
predicts b7max near 196–217 for a healthy engine at a September intake
temperature, so this lands on the bottom edge of the predicted band.

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
group selection, and that ends the VCDS log the rest of the session depends on;
`next-drive.md` carries the rule. So 006 is read cold before the key and hot at
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
extend it. **A single continuous warm-up recording would settle it**, which is
what `docs/next-drive.md` already asks for and what `18_coldstart_z1` is half
of — it holds 13 °C to 17 °C of oil and stops, because five minutes of idling
moves the oil almost not at all.

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
burning there** — a burbling from the back of the car. **On a warm engine it
does not happen.**

**That is the same thermal lever as the idle stumbles, stated far more
cleanly.** The idle argument has to work through counting dips and comparing
three recordings that differ in more than temperature. This one is an event
the driver can hear, present in one thermal state and absent in the other,
with no instrument involved at all.

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

**One coast on the next drive settles it and costs nothing**, because the
drive happens anyway: `next-drive.md` step 13a is the coast — cold, high gear,
clutch up, long enough to get past the 1.2 s delay — and `coastscan.py` is the
analysis.

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

---

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

### Engine speed on 0x280 is recomputed once per firing event

**Measured, over the fixtures, by `python tools/idledips.py --segments`.** The
frame goes out every 10 ms but its speed field holds a value for several
frames, and how long it holds tracks the firing interval rather than the frame
period — 39 ms held against 37.5 ms of firing at 800 rpm, 30 against 28.6 at
1050, 20 against 20.0 at 1500, 13 against 13.6 at 2200, and then it saturates
at the 10 ms frame period above about 3000 rpm where the engine fires faster
than the bus reports.

**So each sample is close to "how fast did the crank turn through one
cylinder's power stroke"**, which is what makes the depth of a dip a per-cylinder
quantity worth putting into an energy budget at all rather than a smoothed
average of four.

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

### The idle counter, frozen before the repair so the after-reading means something

**The question this answers: after the injectors, does the stumble go?** It is
worth setting up carefully because it is cheap to get wrong in a way that
looks like a result.

⚠ **A warm reading after the repair proves nothing, because a warm reading
already read zero before it.** `11_idle_noac_z1` and `12_idle_ac_z1` were
taken at 72.8 and 73.5 °C **on the old injectors** and both count zero. So the
after-measurement has to be taken in the states where the before-measurement
was not zero — **from cold, and at around 61 °C of oil.** `docs/next-drive.md`
already asks for idles spread through the warm-up; this is why.

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
p = 0.002. `next-drive.md` asks for three to five minutes, which is enough for
both questions.

**And it needs no firmware.** The next session records a bus capture anyway,
and the detector runs over the capture afterwards. **Nothing in `src/` is
involved, no frame layout changes and `S-AQY.TRI` is untouched** — putting the
count on the bus and onto the display is a separate want with a separate cost,
and it waits until the count has been shown to mean something.

⚠ **This is not a misfire counter and must not be called one.** Seven of the
44 dips had a misfire increment beside them; the other 37 may be unreported
misfires or may be something else, and no data here separates those. It counts
dips of engine speed at idle. Naming it after what it is thought to indicate
would be the same error as the label file's `(celkovy)`.

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
`TORQUE_CNM_PER_BIT` is derived by requiring b7 = 255 to reproduce the two
*factory* ratings — of a stock engine. This engine is not stock. If the remap
gained anything, the true ratings are higher, full scale should map to more
Nm, and the current scale under-reads by about as much as the remap gained.
That is a named bias of a few per cent rather than an explanation of the gap
above, and **it is one more reason the scale is arithmetic closing on itself.**

**Returning the ECU to standard is not planned**, so this stays an unknown to
be reasoned around rather than removed.

---

## The service of 17 September 2026 — compression, and the plugs that came out

**The repair was split in two, and not by choice.** Spark plugs and ignition
leads went on at this visit; the injectors were still in transit from the UK
and follow separately. `next-drive.md` was written assuming one visit and now
has a two-step experiment to read instead — what that costs, and the one thing
it buys, are below.

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
3, and one of the four visibly worse than the rest.** Photographed in the
garage; the photograph is not kept here, on the same principle as every other
screen in this file — what a photograph is worth is written down, and the
picture itself goes stale in a drawer.

What is visible in it: dry, dark, sooty deposits on all four — carbon rather
than the wet sheen of oil — with the ground straps and centre electrodes
rounded off rather than square.

⚠ **A photograph cannot grade fouling and must not be used to.** Lighting,
angle and which way a plug happens to be turned move the apparent severity more
than a real difference between two cylinders would. **The owner handled them
and the ranking is his, not the picture's.**

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

### The worst plug names a cylinder, and that datum is perishable

**This is the most actionable thing in this section.** *The old converter was
shown to the owner* says one burned-through chamber "fits one cylinder better
than four" and then, correctly, refuses to name which: exhaust flows mix in the
manifold, so the converter cannot identify anything.

**A plug does not mix.** It sits in one cylinder and records only that cylinder.
So the worst of the four is the first candidate identification of the suspect
cylinder this investigation has ever had — **provided anybody can still say
which cylinder it came out of.**

- **Ask the garage while they still remember**, and write the answer down here.
  Plugs come out in a rush and end up loose in a cap; the position is lost
  within days and cannot be reconstructed afterwards.
- **Keep the four plugs, bagged and labelled by cylinder.** They are physical
  evidence of exactly the kind this file has been short of. If the new injectors
  cure everything, the worst plug should have come from the cylinder that was
  being fed the extra fuel, and that is a prediction this set of parts can still
  be held against.

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

⚠ **Whether the AQY is wasted-spark is not established by any document in
`docs/` and is not asserted here.** The coil was replaced in 6/2026 and the
misfires outlived it, which is what moved ignition from cause to casualty in
this file — but the *leads* dated from 12/2022 and have only now been changed,
so the pairing question is live in a way it was not a month ago. **It is cheap
to settle**: the topology is visible on the car, or in the parts catalogue for
the ignition components. Settle it before reading anything into the pair.

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

**Cost: the next drive no longer has one variable.** `next-drive.md`'s
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

## What the next drive settles, and what it does not

**The plugs and ignition leads went on 17 September 2026 and the injectors
follow separately** — see *The service of 17 September 2026*, above, for why
that split matters and what it costs this comparison. The plugs and leads had
last been changed in 2022, so they had spent four years downstream of whatever
has been happening; the coil is a month old and the misfires outlived it, which
is what took the ignition side off the list of causes and left it on the list of
casualties.

⚠ **The table below was written for one visit and now covers two.** Everything
in the left column is still what the *injectors* would settle **if the plugs had
changed nothing** — and the plugs are no longer a null change, because they came
out eroded and carboned at under 1,500 km. Read every row below as "the repair",
not "the injectors", unless the middle capture in the section above was taken.

| the next drive settles | it does not settle |
|---|---|
| whether the engine was unhealthy — feel, first-gear misfires, the stumbling idle at both thermal states, the idle adaptation, cold starts | whether `TORQUE_CNM_PER_BIT` is right |

**Three symptoms have run together for years** — the exhaust destroying itself,
the stumbling idle, and poor cold starts, the last of these for a period nobody
has pinned down. A single cause for all three is worth more than three
explanations, and a leaking injector is the only candidate on the table that
produces all of them.

⚠ **The owner's reading extends that back past the purchase, and it is a
hypothesis rather than a finding.** If the injectors are the single cause, the
fault is older than this ownership — which would also explain why the car
arrived with its warning lamp taped over and a dead oxygen sensor behind it
rather than with either of them fixed. **Nothing here establishes it**, and by
construction nothing can: the pre-2017 record does not exist
(`vehicle-history.md`, *The masked warning lamp*). It is written down because it
is testable in one direction only — **if the new injectors cure all three
symptoms, the hypothesis survives; if they cure none, it is dead** — and because
an unstated assumption that the history began in 2017 is the more expensive
mistake.

**The prediction worth writing down before it happens**, so it can be wrong:
if the injectors were the fault, the car pulls better, the first-gear misfires
go to zero and the idle adaptation moves toward zero — while **load stays near
78 % and the display keeps showing about 117 Nm and 58 kW**. The model's
inputs will not have moved, so its output should not either.

⚠ **Confidence in that last row is low, and lower than this file first
claimed.** It needs the torque model to be blind to fuelling, which is the
unsourced step above. Charge should not move; **ignition advance could**, if the
knock control had been retarding a cylinder the new injectors settle; and if
the per-cylinder misfire signal feeds the model at all, the row is simply
wrong. **A displayed figure that rises is therefore a result and not a
surprise.**

**If the displayed maxima move substantially, the fault was not the injectors** —
something changed in the air path or in the ignition, and that is a different
trail.

---

## What would settle the scale

**One capture, and it needs the dashboard open anyway.**

A bus capture carrying **0x280 b7 and the 0x480 fuel counter**, taken
simultaneously with a VCDS log of group 003, over the same full-throttle pulls.
Measured air divided by measured fuel gives the real air-fuel ratio, which
removes the largest assumption in the efficiency table above; b7 against that
gives the scale.

⚠ **The fuel counter measures what the ECU commanded, not what left the
injector**, and full-load enrichment is mapped rather than closed-loop — so a
leaking injector would deliver more than the counter reports and the ratio
would look better than it is. **A high reading would prove something; a normal
one proves much less.** Do this after the injectors are replaced, not before.

⚠ **This does not revive the parked VCDS session.** Question 8 in
`can-decoding.md` stays parked and that session stays cancelled: this ECU has
no torque measuring block, so there is nothing to read there. What is new is a
different measurement — torque inferred from air and fuel — which needs no such
block.

**And one capture answers three questions at once**, which is why
`next-drive.md` settled on a single configuration rather than splitting the
work: a continuous recording through the warm-up gives the stumble rate against
oil temperature as a curve instead of two points, holds b7 at ninety-four
samples a second beside the ECU's own load, and finds out whether this engine's
oil ever passes about 75 °C — which would close `can-decoding.md` question 7
rather than leave it open.

**The raw byte comes off the capture, not off the display.** `S-AQY.TRI`
carries `Torque` and `Power`, which are computed from 0x280 b7, but no channel
showing b7 itself — a claim to the contrary stood here and was wrong, and
`next-drive.md` says why adding one is not worth the risk to a working display
configuration. **`docs/next-drive.md` is the procedure, in order.** The
fuel counter still wants a bus capture, and only to remove the air-fuel
assumption.

`install.md` step 11 covers everything else a trip behind the display should
pick up while it is open, and `can-decoding.md` question 7 wants a hot-oil
sweep from the same trip. **Batch them.**
