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
**the engine warning lamp had been masked inside the instrument cluster**, so
it had been lit the whole time and could not be seen. Whatever the fault
history is before that point, nobody has it.

Three things follow, and none of them are sentiment.

- **A lambda sensor has already been replaced once on this car.** So if block
  034 comes back `B1-S1 not OK`, that is a **second** sensor failing, which
  argues for something that keeps killing them — running rich, or raw fuel
  reaching them — rather than for a worn-out part. ⚠ **Which sensor it was,
  pre- or post-catalyst, is not recorded here**; block 034 covers the pre-cat
  one and 036/037 the post-cat one, so the answer changes which block's verdict
  is the interesting one.
- **The parts have been replaced in the order the symptoms surfaced**, which is
  not the same as the order of cause: sensor, then coil, then most of the
  exhaust, and only now the injectors. A single upstream cause producing
  symptoms one at a time looks exactly like this from inside it, which is the
  argument for the diagnosis-before-parts position the rest of this file takes.
- **The masked lamp means the "for years" in every symptom description is a
  lower bound.** It cannot be turned into a date and should not be.

**Nothing further is bought before 034 and 046 report.** That is the owner's
position and it is the right one — `next-drive.md` step 9 is what produces
those two verdicts, and both are absolute rather than comparative, so they need
no baseline this car can no longer provide.

---

## What the vehicle reported

**From the display**, read as maxima over the drive:

| | |
|---|---|
| `Torque`, peak | **117 Nm** |
| `Power`, peak | **58 kW** |
| oil temperature, peak (0x420 b3, the cluster's channel) | **72–74 °C** |

Two notes on the oil figure, because it invites a wrong conclusion. It is
**not** anomalous: the four warm free-revving holds this project's drag line is
fitted to sit at 72.8–76.6 °C, and the fixture table under question 4 in
`can-decoding.md` has the oil lagging the coolant badly — 65.3 °C of oil at
99.0 °C of coolant in `03_drive`. And **it cannot be a cause of a rich
mixture**: the ECU's warm-up enrichment runs off the coolant sensor, not off
this one, which feeds the instrument cluster. A cold-running *coolant* sensor
or a thermostat stuck open would be a mechanism; this channel is not.

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
the display can and cannot mean* showing up in this car's own data — but one
count of b7 is 0.39 %, so the resolution is coarse enough that a brief event
might not register regardless. **Suggestive, not evidence.**

⚠ **The whole thing is a correlation across three recordings, one of which is
positive.** They differ in more than the data holds — different days, fuel and
ambient conditions — and `09` is two and a half times longer than the others,
which the per-second rates account for but which still gives it more chances.
**Treat the thermal lever as the most testable idea here, not as a finding.**

**What costs nothing to check:** if this is right, the stumbling should be worst
in the twenty minutes *after* the temperature gauge has already settled, and
should ease as the engine soaks through. The gauge reads the coolant and is
therefore useless for it; `OilTemp` on the display is not.

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
evidence about the coil, not a clearance.

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

## What the next drive settles, and what it does not

New injectors, spark plugs, ignition leads and silencers are fitted the
following week. **The plugs and leads were last changed in 2022**, so they have
spent four years downstream of whatever has been happening; the coil is a month
old and the misfires outlived it, which is what took the ignition side off the
list of causes and left it on the list of casualties.

| the next drive settles | it does not settle |
|---|---|
| whether the engine was unhealthy — feel, first-gear misfires, the stumbling idle at both thermal states, the idle adaptation, cold starts | whether `TORQUE_CNM_PER_BIT` is right |

**Three symptoms have run together for years** — the exhaust destroying itself,
the stumbling idle, and poor cold starts, the last of these for a period nobody
has pinned down. A single cause for all three is worth more than three
explanations, and a leaking injector is the only candidate on the table that
produces all of them.

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
