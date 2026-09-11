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
median, over the three warm idle fixtures:

| fixture | oil | coolant | dips ≥ 20 rpm | dips ≥ 15 rpm |
|---|---|---|---|---|
| `09_idle_60s_z1` | **61.0 °C** | 99.2 °C | **13 in 60 s** | 35 |
| `11_idle_noac_z1` | 72.8 °C | 99.6 °C | **0 in 25 s** | 4 |
| `12_idle_ac_z1` | 73.5 °C | 99.5 °C | **0 in 25 s** | 1 |

⚠ **An earlier pass at this reported the fixtures as smooth and was wrong.** It
looked for the single deepest dip, which is a different question: the deepest
excursion in `09` is only 37.5 rpm, while what the owner describes is a small
event *repeating*. Asking for the maximum answers "is there one big stumble"
and says nothing about thirteen small ones.

**The lever is how heat-soaked the engine is, and the coolant hides it.**
Coolant sits at 99 °C in all three, so the ECU's own warm-up state is identical
and cannot be what differs. The only thing that separates them is the real
temperature of the engine, for which the oil is the available proxy: the
stumbles are there at 61 °C and gone at 73 °C.

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
the thirteen dips: engine speed falls 20–37 rpm while the ECU's modelled torque
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

**Most of it needs no capture at all any more.** `S-AQY.TRI` now carries
`TorqRaw`, the raw 0x280 b7 beside the torque computed from it, so b7 can be
read off the display and set against the load percentage VCDS logs at the same
engine speed. **`docs/next-drive.md` is that procedure, in order.** Only the
fuel counter still wants a bus capture, and only to remove the air-fuel
assumption.

`install.md` step 11 covers everything else a trip behind the display should
pick up while it is open, and `can-decoding.md` question 7 wants a hot-oil
sweep from the same trip. **Batch them.**
