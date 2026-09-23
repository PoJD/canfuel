# The next drive — one session, in order

**This is the procedure for the first drive after the injectors are fitted.**
One session, one configuration, one capture. Allow **an hour and a half**.

⚠ **The repair happened in two visits, not one, and this document was written
for one.** Spark plugs and ignition leads went on **17 September 2026**; the
injectors were still in transit and follow separately. So every "if the
injectors were the fault" below is really "if the repair was the fault" —
`docs/engine-health.md`, *What the split costs, and the one thing it buys*, has
the argument and the one capture that would separate them.

**The injectors and fuel filter went on 23 September 2026**, with the battery
disconnected. **`032` read −3.1 % / 0.0 % afterwards**, and step 1's baseline is
that reading, not −4.7 / +1.6, until the drive shows whether part load was
reset. `engine-health.md`, *The injectors and the fuel filter*, has the
details.

**The document is in two halves and they are meant to be used differently.**

- **[Part 1](#part-1--the-session-step-by-step) is the procedure.** Follow it
  in the car without deciding anything. It says what to do and in what order,
  and nothing else.
- **[Part 2](#part-2--why-each-step-is-there-and-how-to-read-what-comes-back)
  is why**, and how to read what comes back. Read it before, or afterwards
  with the results in hand. **Nothing in it is needed while driving.**

**Nothing in this procedure happens before the injectors are on.** There will be
no clean before/after for most of this and that is accepted; the fixtures
already hold the "before" for the measurements that matter.

⚠ **The car standing until then was the plan and it is not what happened.** The
injectors were late, and the car has been driven in the interval — the garage
run, and **about 450 km to the Šumava and back, ending 19 September 2026**.
**It is parked from that day until the injectors go on**, which puts the
overnight stand of step 3 back within reach and leaves the tank as it was
filled. The reasoning that wanted it parked has not changed:
a new converter behind a cylinder still dumping raw fuel is the same converter
that was cut open. What changed is the parts arriving after the calendar did.
`engine-health.md` records where the damage actually concentrates — **long
idling and low-speed pottering, not distance** — which is what made driving it
the lesser risk rather than a safe one.

---

# Part 1 — the session, step by step

## Before the day

**1. Do not clear the fault memory. Do not disconnect the battery. Do not reset
adaptations.** Not before, not after, not at the garage. If the garage offers,
decline.

⚠ **If the battery has already been off, this step is advice about the future
and not a description of the past.** A garage doing plugs has no need to
disconnect it and an injector change is a reason to; either way nobody wrote it
down. **Settle it by measurement rather than by asking**: read group `032`
before the injectors go anywhere near the car and compare against the
**−4.7 % idle / +1.6 % part load** this project recorded. Zeros mean it was
wiped; anything near those figures means the adaptation survives a disconnect on
this ECU, which no document here establishes either way. A small drift is normal
learning and not a reset. **Whatever it reads becomes the baseline**, and the
procedure works from it unchanged.

**1b. KEEP THE OLD INJECTORS, and photograph the inlet screens and the
nozzles.** Four of each, laid out so it is clear which cylinder is which.
They go in a bag, not in a bin.

⚠ **Keeping the mapping is the whole of the discipline here**, and it is the
part that failed last time: the plugs came out at the 17/9 visit and ended up
loose in a cap, so which single one was worst is gone. Only the pair survived,
because somebody said it out loud. **Lay the injectors out in order as they
come off and photograph them that way.**

⚠ **This is the only physical evidence this investigation will ever have, and
it expires the moment they are thrown away.** Everything else here measures a
symptom; the injectors are the suspect itself. Contamination shows on the
inlet screen, a poor spray pattern shows at the nozzle, and **cylinders 1 and
4 are the ones to look at hardest** — they are where the worst plugs came from
(`engine-health.md`, *The worst plugs name two cylinders*). The candidate root
cause in that file, *A candidate ROOT cause, from a photograph*, is what they
would confirm or refute.

**No conclusion depends on doing it**, and it costs a bag and five minutes.
That is the whole argument for it: the cost of keeping them is nothing and the
cost of not keeping them is a question that can never be asked again.

**2. Do not do this the day the car comes back.** Drive it home and leave it.
The drive home is wanted; see Part 2.

**3. Plan the start for about ten hours after the engine last ran.** Overnight
is right. **Do not deliberately make it longer.**

### 3a. If the injectors go on the same day — what the leak check costs

**The leak check is not negotiable and is not the problem.** The rail is empty
after the injectors are changed, so it gets primed, started, run briefly,
looked over for weeping seals and read for faults. That has to happen and it
has to happen first.

⚠ **The fuel filter is being changed in the same visit**, which opens the
system a second time and in a second place — **under the car, on the pressure
side, at a joint nobody can see from the engine bay.** One leak check covers
both only if both are looked at, so look underneath as well as at the rail.

**What it costs is decided by one channel, and `18_coldstart_z1` measures it.**
Six minutes of idling from a genuinely cold engine moved:

| | start | after 6 min |
|---|---|---|
| coolant, `0x288` | 16.5 °C | **63.75 °C** |
| oil, `0x420` b3 | 12.75 °C | **17.25 °C** |

**The oil barely notices and the coolant is transformed** — +4.5 against
+47.25, and the oil does not begin to move at all until about 200 s in. **The
coolant is also what the ECU uses to decide whether the engine is cold**, so
that one column is the whole of what a same-day session loses.

⚠ **Two measurements go, and one of them is the most valuable thing on this
drive.** The cold start (steps 10–11) is the obvious one. **The cold coast of
step 13 is the other**, and it is less obvious: if the fuel cut is inhibited
on a cold engine — the open question the coast exists to settle — the ECU
decides that off the coolant, so it would hand back the warm answer and the
question would stay open. The cold idle of step 12 is confounded rather than
lost: its oil would still be near the before-reading's 13–17 °C, but the
warm-up enrichment would not be a cold one.

**Everything else survives**, which is worth saying plainly rather than
leaving to be inferred: all four VCDS verdict blocks, `032`, `014`, the hot
idle, the pulls, the hot oil filter reading, and the whole tank and refuelling
replay. A same-day session keeps most of the value.

**So the split is by temperature, not by session.** The cold half is about
fifteen minutes of a later morning — ignition, start, idle, a short drive with
a coast in it — and needs no VCDS blocks, no basic settings and no thermometer
work. **It does not mean repeating the ninety minutes.**

⚠ **And the go/no-go is a number rather than a feeling.** Keep the leak check
as short as it can be, let the car stand, and **read group 001 against the
mirror console's ambient before committing to the cold half.** Within a few
degrees and the soak is intact; anything more and this is a warm session with
a cold one owed. *(A DECISION, not a measurement: the before-recording started
at 16.5 °C of coolant, and nothing establishes how much drift that comparison
tolerates.)*

⚠ **Step 1 is easy to lose in the rush of a same-day fitting.** Group `032`
is read **before the injectors go anywhere near the car**, and after they are
in there is no way back to it.

**4. Take the display and the converter out**, and put the USBtin on that pair.
They cannot share it — the converter is powered from the display, so removing
one removes both.

⚠ **4a. The tank is full, and that is settled rather than chosen.** It was
filled on **19 September 2026** — 44.17 L at the pump, 10.9 L indicated before
and 50.9 L after — and the car is not started again before the injectors, so
it is still full at the key. `refuel-reset.md`, *The 2026-09-19 fill*,
is that fill and what it measured. **This step is now a record of the state
the drive starts in rather than an instruction about it**, and the level
needs no noting because it is written down here.

**Which is the opposite corner of the state space from every fixture**, and
that is what it buys. Every fixture in this repository that contains a moving
car has **0–10 L in the tank**; the only one with a real level,
`18_coldstart_z1` at 50 L, never moves. The float has therefore never been
recorded in motion anywhere but the bottom of its travel, on a sender known to
be nonlinear, which is why the refuelling rule's thresholds rest on
measurements from one corner. `refuted.md` C10 is what that cost. **This drive
records the top of the travel in motion for the first time** — the slosh at
full, which is what was asked for.

⚠ **But a full tank is the LENIENT test for a false reset, not the harsh
one**, and question 4 below has to be read knowing it. The rule fires on a
**rise** above the settled level, and a brimmed float sits against its top
stop: it can swing down as the fuel moves and it cannot swing up past the
stop. So *it never fired on a full tank* is a weaker result than the same
sentence about a half-full one.

**That applies to the start of the drive and not to all of it**, which is the
one thing making it better than it sounds: an hour of this kind of driving
burns a few litres, so the float leaves its stop partway through and the later
part of the capture is an ordinary high level rather than a clipped one.
**The middle of the travel is still unsampled** — a sender nonlinear at both
ends does not interpolate between two ends that behaved — and only the drives
after this one reach it.

## In the car, before the key

**5. Connect VCDS to the OBD socket and the USBtin to the display's pair.**
Both at once is fine.

**6. Read group 006 and write two numbers on paper:** intake air temperature
and the altitude correction factor.

**6a. Read group 001 as well and write down the coolant temperature.** One
extra screen, and it is the first half of settling the coolant scale — see
*The questions* at the end.

⚠ **THE COLD SOAK IS A CALIBRATION POINT AND IT ONLY EXISTS FOR THESE FEW
MINUTES.** The car has stood overnight, so **every fluid in it is at ambient**
and five readings are all of one temperature at once:

| | where it comes from |
|---|---|
| **outside air** | **the mirror console display — read it and write it down** |
| intake air | VCDS 006, step 6 |
| coolant | VCDS 001, here |
| coolant | `0x288` b1, out of the capture |
| oil | `0x420` b3, out of the capture |
| **oil, directly** | **the infrared thermometer at step 6b** — the filter and the sump |

⚠ **Two of those five share nothing with the rest**, which is what makes them
worth more than the count suggests: the mirror console and the infrared
thermometer. Not the sensor, not the wiring, not VCDS, not this bus. The other
three can be wrong together; those two cannot join them.

**The mirror display was missed until now**, because this repository spent
months asserting the car had no ambient sensor on the strength of two zero
bytes (`refuted.md` B11).

**And the last row is the only one that reads the oil rather than inferring
it.** Every other row at this soak is coolant, intake air or ambient, and the
oil's cold value is taken on the argument that everything has stood overnight.
The filter and the sump are the oil's own container, so step 6b turns that
argument into a reading.

**Read the mirror console before opening a door**, while the car is still as
it stood. These displays heat-soak — standing in sun, or with the cabin warm,
they read high — which after an overnight stand in the morning is exactly when
they do not.

The capture starts at step 7 and the engine not until step 10, so its opening
minutes cover the same soak — nothing changes in between. **Once the engine
fires this point is gone until the next overnight stand.**

⚠ **WHAT THIS ONE READING DOES AND DOES NOT SETTLE**, because it is tempting
to think VCDS here ends the argument and it does not.

**It does not give a scale.** One point fixes an *offset*. Any slope
whatsoever fits a single point once you are free to choose the offset with
it, so the cold soak alone cannot tell 0.75 from 1.0 for either channel.
**That is the entire reason step 26a exists** — two points at different
temperatures, and only then is there a line.

**It does give three things that are worth the one screen:**

- **a falsification test, before the engine has even started.** Our coolant
  formula says raw 86 is 16.5 °C. If VCDS says 22, the formula is wrong and
  we know it in the car rather than three weeks later. **The mirror console
  gives the same test for nothing**, and from a sensor that has no connection
  to any of the others.
- **truth for both offsets at once.** Whatever number VCDS reports IS the
  temperature, so both raw bytes can be checked against it rather than
  against each other — which is the weakness of the 3.75 °C argument in
  `can-decoding.md` question 10, where two unverified channels are compared.
- ⚠ **a result that can flip the whole suspicion.** If VCDS reads near
  **13 °C**, then at the soak it is the *oil* decode that is right and the
  *coolant* decode that is three degrees out — and every argument built on
  the coolant being the reliable one has to be re-read. Write the number down
  before forming an opinion about it.

**VCDS never gives the oil, at any temperature** — `01-Motor` has no oil
block, which question 4 in `can-decoding.md` settled by looking rather than
by guessing. So the oil *slope* has exactly two routes: the filter reading at
step 28, or the two-cold-soak pair on a genuinely cold morning. **Step 6b
gives the first of those a reference at the cold end**, though not the one it
looks like — *The cold readings at step 6b* in Part 2 is what it is and is not
worth.

⚠ **If group 001 will not display with the engine stopped**, do not chase it —
note that it would not and move on. **Group 006's intake air is the fallback
and it is already being read at step 6**: on a car that has stood overnight
that is ambient too, from VCDS, in real degrees, which is all this point
needs.

**6b. Now the infrared thermometer, bonnet open, engine still cold.** Three
spots, **three readings each**, written down with the clock time:

| | where | what it is for |
|---|---|---|
| 1 | **the oil filter**, on the painted can | the step 28 target — this is the pair that matters |
| 2 | **the sump pan**, if it reaches without going under the car | where the sender actually sits |
| 3 | **a shaded body panel, or the ground beside the car** | ambient, from this instrument rather than from another |

**Same spots, same order, same distance, again hot at step 28.** That is the
whole discipline: a pair of readings of one spot is worth far more than either
reading alone, and only if the aim was the same both times.

⚠ **All three must read one number, and that is the point of taking them.**
The car has stood overnight, so filter, sump and tarmac are all at ambient.
**The spread across the three is the noise floor of the method** — if they
span four degrees cold, nothing at step 28 is worth better than ±2 °C. Three
spots is a thinner error bar than six would give and it is enough for a
question whose answer is 26 °C wide.

⚠ **The coolant is deliberately not on this list, and "there is no metal to
aim at" is not why.** Two corrections, because both are easy to get backwards.
**Bare or shiny metal is the WORST infrared target there is** — it emits
poorly and reflects the engine bay, so it reads low. Paint, rubber and plastic
are all good emitters and are what an infrared thermometer is calibrated for,
so a car with plastic pipework is not a problem for this instrument. **And
the expansion tank is a poor target for a different reason**: part of it is
air by design, it is not where the sender sits, and from outside there is no
way to tell whether the spot is aimed at coolant or at the air above it.

**If a coolant number is wanted anyway, the upper radiator hose is the
target** — rubber, a good emitter, and carrying coolant on its way out of the
engine. It lags by a few degrees through the thickness of the rubber, which
matters not at all here. **It is still optional**: VCDS reads the coolant
truthfully cold at step 6a and hot at step 26a, each against `0x288` in the
capture, and that pair *is* question 1. Two real sensors cannot be improved on
by pointing a thermometer at a hose.

⚠ **Three and not six, and the two that came off are worth a line.** An
earlier version of this step also had the rocker cover and the dipstick tube
on it, because Part 2 tells the next person not to aim at either and has
never shown what they cost — two readings would have retired that as an
assertion. **That is a nice thing to know and it is not worth two more stops
on a cold morning**, in a procedure that already runs ninety minutes. The
thermostat housing came off for a different reason: VCDS gives the coolant
truth at both ends already, at steps 6a and 26a, so an infrared reading of it
adds nothing. **Take any of the three if you are curious; skip them without a
second thought.**

⚠ **It does NOT give an offset to subtract at step 28**, which is the obvious
reading of it and the wrong one. *Steps 27–28a* in Part 2 has the argument in
three lines; the short version is that the error this instrument makes is
proportional to how far the target is from its surroundings, and at a cold
soak that distance is zero.

**7. Start the capture:**

```
python tools/usbtin_capture.py --seconds 4500 --out postfix_z1.txt
```

⚠ **Seventy-five minutes, not sixty, and the margin is the point.** The drive
is 45 to 60 minutes *plus* three idles of three to five minutes *plus* however
long it takes to find somewhere to stop for each of them, and step 16's hot
idle is at the end of all of it. An hour has no margin at all: the capture
would stop mid-drive and take the hot idle, the pulls or both with it. At the
unfiltered 65 MB an hour (*The capture filter*) the extra quarter of an hour
costs about sixteen megabytes.

**8. Start VCDS logging, groups 003 and 014. Two groups, never three.**

**9. From here until step 17, do not touch the VCDS screen.** Changing the
group selection is what the log records; switching to another block ends the
recording.

## The start

**10. Start the engine the way you normally start it.** Do not cycle the key to
prime the pump — unless that is your normal habit, in which case do it.

**11. As soon as it catches, check the VCDS log is still counting samples.** If
it has stopped, restart it immediately. Keep glancing at it.

## The drive — 45 to 60 minutes

**12. Stationary idles**, engine running, in neutral, nothing touched, air
conditioning off. **One right after the start, one at the end when thoroughly
hot, and one in the middle that has to land near 61.5 °C of oil** — that
middle one is the whole reason the trip has idles in it at all, and
*Steps 12–14a* below is why.

⚠ **61.5 °C IS THE OIL, `0x420` b3, AND NOT THE COOLANT.** The figure comes
from `09_idle_60s_z1`, where the oil sat at raw 144–146 — 60.0 to 61.5 °C —
**while the coolant beside it was raw 193–198, which is 96.75 to 100.50 °C.**
Once the engine is warm the two are nowhere near each other, and the middle
idle is indexed by the slow one.

⚠ **The trap is that the coolant PASSES THROUGH 61.5 °C, and early.** In
`18_coldstart_z1` it does so about five and a half minutes into a cold idle,
with the oil at 17 °C. **Watching the wrong channel therefore puts the
"middle" idle on top of the cold one** — two readings of the same state, and
the middle idle, which is the whole reason this drive has idles in it, never
happens at all. `tools/oilwatch.py` bands on `0x420` b3 and cannot make this
mistake; a person reading a gauge can.

**And a wrong oil scale does not break it.** What is really being matched is
**raw byte 146**; 61.5 °C is what this project's decode calls it, and that
decode is the open question 10. The before-reading went through the same
decode, so if the label moves, it moves for both — matching the temperature is
matching the byte either way.

⚠ **The first one is TWO MINUTES. The other two are three to five.** The first
idle is the only part of this drive that spends a budget something else needs:
**idling from cold raises the coolant about 8 °C a minute** (measured off
`18_coldstart_z1`), and the coolant is what step 13 needs low. Two minutes
costs 16 °C of it against the 40 °C a five-minute idle would.

**Two minutes is not a compromise on what the idle is for.** At the cold
before-reading's **8.5 dips a minute**, two minutes expects 17 of them:

| | seeing none, if nothing changed | seeing a halving or better |
|---|---|---|
| 1 min | p = 2×10⁻⁴ | p = 0.07 |
| **2 min** | **p = 4×10⁻⁸** | **p = 0.012** |
| 3 min | p = 8×10⁻¹² | p = 0.002 |
| 5 min | p = 3×10⁻¹⁹ | p = 0.0002 |

**Gone-or-not-gone is settled many times over by two minutes**, and the third
minute buys a factor of five on the harder question while costing 8 °C. If the
route to the road happens to take longer anyway, no harm done — but do not
add idling on purpose.

**Which leaves the problem that you cannot see the oil temperature from the
driver's seat**, the display and the converter being out. Two routes, and the
first is much better:

**12a. With `tools/oilwatch.py` running beside the capture:**

```
python tools/oilwatch.py postfix_z1.txt
```

It reads the capture **while `usbtin_capture.py` is still writing it**, never
touches the serial port, measures how fast the oil is actually climbing and
says how long there is before the band arrives — ninety seconds of warning by
default, which is enough to notice and then find somewhere to stop. It also
says when the idle has been long enough. **Take the three idles as written and
let it place the middle one.**

⚠ **Whoever is driving cannot watch a terminal**, so decide before the key who
or what is going to notice. Three arrangements, and the first works with
nobody paying attention:

| | how it tells you |
|---|---|
| `oilwatch.py CAPTURE` in a visible window | prints on every change and **rings the bell** when it turns actionable |
| an assistant on the same laptop | `oilwatch.py CAPTURE --until band` blocks and returns the moment there is something to say; it does the same for `idle-done` and `hot` |
| a passenger | `--once`, on request |

**Run the first one regardless.** It costs nothing and it is the only one that
does not depend on somebody remembering to look.

**12b. With nobody watching**, hedge instead: **several idles through the first
half of the drive** — roughly ten, twenty and thirty minutes in — and keep
whichever one landed in the band. They are free; *Steps 12–14a* says why.

**13. Coasts on the engine — as MANY as you like, starting as early as you
can, and one more when hot.** Rev to **at least 3,800 rpm**, lift the pedal
fully, **keep the clutch up and stay in the gear you are in**, and hold it
until the engine is back near idle.

⚠ **This comes before the pulls because the two want opposite engines.** The
pulls below need a hot one and will happen late whatever the numbering says;
**the cold coasts exist for a state that is gone in minutes**, so they are the
one thing on this drive that cannot be caught up later.

⚠ **A high gear is NOT required, and an earlier version of this step said it
was.** That was wrong and it mattered, because it made the cold coast sound
like something needing a motorway. **All four cuts in the last capture were in
first gear at 20–30 km/h.** What the coast actually needs is only that the
engine is still turning when the cut would engage: the ECU takes **1.2–1.3 s
from the pedal coming up before it shuts the injectors**, and gives them back
at **1,700–1,750 rpm**. First gear decays at about **1,320 rpm/s** (measured),
so lifting from 3,800 leaves the engine above 1,800 rpm a second and a half
later, which is the whole requirement. A higher gear decays more slowly and
gives longer — it is easier, not necessary.

**So the first one can happen on the way out of the gate**, in first or
second, before the car has been anywhere. That is the point: **it is the
coolant that is running out, not the road.**

⚠ **Take a LADDER of them rather than one cold one.** The cut is almost
certainly gated on coolant, and a warm-up is a ladder of coolant temperatures
for free — so coasts spread through the first ten or fifteen minutes say **at
which temperature the injectors start being shut**, which is a better answer
than a cold yes or no and costs nothing but lifting off a few more times.
`coastscan.py` prints the coolant beside every coast for exactly this.

**And listen for whether it goes QUIET, not for whether it burbles.** Both
states make a noise: warm, it stops a second or so after the lift; cold, the
owner reports it carrying on. So the line to write down is *went quiet after
about N seconds* or *never went quiet*, cold and hot. **N against the 1.2–1.3 s
the injectors take to shut is the whole comparison**, and counting out loud is
accurate enough for it. It is the one observation on this drive that no
analysis can recover afterwards.

**The other half comes out of the capture by itself:** `python
tools/coastscan.py CAPTURE` finds every coast and prints, for each, the
coolant it happened at and whether the injectors shut — at what engine speed,
how long after the lift, and where fuel came back.

**14. Two or three full-throttle pulls in FOURTH, from about 2,200 rpm and as
far up as the road allows.** **Hot, so late in the drive** — this is the half
of the pair step 13 defers to. Pedal on the floor, clutch up, no change of
gear part way through. **5,000 rpm is enough and 6,000 is better**; stop
wherever the limit and the traffic say, and do not go looking for somewhere
to do otherwise.

⚠ **Fourth and not fifth, and the arithmetic is the owner's own.** The Šumava
trip was run at 4,000–5,000 rpm in top at about 130 km/h, so 6,000 rpm in top
is somewhere between 155 and 195 km/h and is not on under either reading of
that. Fourth reaches the same engine speeds at a speed a motorway can hold.

⚠ **That is a sweep, and an earlier version of this file said not to sweep.**
The objection was never to the sweep, it was to the **rate** — *Steps 12–14a*
in Part 2 has the measurement and what changed.

**Do not assume the maximum sits where the factory put it.** The car has been
chipped since 6/2018 and what that did to the shape of the curve is not known
here, which is exactly why the pull covers a range instead of aiming at an
engine speed.

**14a. One low-gear pull to high revs**, as before. It costs one squirt of fuel
and it is the only thing that reaches the top of the range if fourth cannot.

**15. Nothing needs marking and no times need noting** — except the one line
step 13 asks for. Drive; the analysis finds the idles, the pulls and the
coasts by itself.

**16. Finish at a standstill with the engine idling and hot.** Do not switch
off. **This idle wants its three to five minutes before step 17**, because
step 17 is what stops recording it.

⚠ **`--seconds 4500` is a ceiling, not a plan.** When the drive is over, end
the capture with **Ctrl-C** — it closes the file cleanly, reports the frame
count and the status flags, and says it was stopped by hand. **Do not kill the
process:** the file is block-buffered and a hard kill loses about half a second
off the end (`tools/oilwatch.py` has the measurement). Waiting out the
remaining minutes costs nothing either, if the engine is happy idling.

## Straight after — engine idling, hot

**17. Stop the capture, then stop the VCDS log.** Both. Only now may the group
selection be touched.

**18. Read these and photograph each screen:**

| group | what to read |
|---|---|
| **014** | the misfire count — watch it for a minute rather than glancing |
| **032** | both lambda adaptations |
| **055** and **056** | idle regulator, its adaptation, target idle speed |
| **100** | readiness bits and OBD status |
| **006** | intake air temperature and altitude factor, the second time |
| **001** | coolant temperature, hot — **note the clock time with it** |

**19. Now the basic settings. This is how one is run** — it is not *Akční
členy*, which is the other function:

- in **`Měřené hodnoty`**, press **`Přepnout na základní nastavení`**
  (bottom left), **or** use `ZÁKLADNÍ NASTAVENÍ` from the controller window
- enter the group number, press **START**
- **each block shows its own entry conditions as its first fields.** Hold the
  engine where those fields ask, watch them come into range, then read the
  result field
- stationary, **in neutral, handbrake on**; the throttle is a foot, so both
  hands stay free

**20. Run group 046.** Hold the engine speed its own field asks for. Read and
photograph the result.

**21. The same for group 034.**

**22. The same for group 037.**

**23. The same for group 070.** Expect this one to operate a valve.

**24. Read group 036** — an ordinary read, not a basic setting.

## The last capture — one recording covers the last two steps

**25. Engine still idling, VCDS still connected. Start a capture:**

```
python tools/usbtin_capture.py --seconds 420 --out final_z1.txt
```

**26. While it runs, disconnect VCDS from the ECU and reconnect it.** Engine
running, bonnet shut, nothing else touched.

**26a. Still idling, read group 001 once more and note the clock time.** The
capture is running, so this pairs a VCDS coolant reading with the `0x288` raw
in the same file — the second of the two points that settle the coolant scale.

**27. Leave the capture running. Unplug VCDS, switch the engine off** and go
straight to the bonnet. The bus dies with the ignition, and that is fine — the
last `0x420` frames it recorded are the reference.

**28. Point an infrared thermometer at the OIL FILTER.** Note the reading and
the clock time. A minute or two after switching off is close enough.

⚠ **The filter and not the dipstick tube, and not the filler cap.** Down the
tube an infrared thermometer mostly reads the tube wall; through the filler
cap it reads the rocker cover and the valve gear, which is not the oil this
channel is about and has drained away by the time the engine stops. **The
filter is full of oil and stays full** — the anti-drainback valve sees to that
— and it is reachable without going under the car.

**Aim at the painted can, hold it close, and take three readings** rather than
one. Bare or shiny metal reads low on an infrared thermometer; a painted
filter body does not.

**28a. Then the other two spots from step 6b — same order, same distance,
three readings each, with the clock time.** The filter is what answers
question 2; the other two say how much the filter reading is worth.

**The filter-against-sump pair earns its place on its own.** It is the one
caveat Part 2 raises against reading the filter at all and has never measured:
cold the two must agree, and hot their difference is the gallery-to-pan gap.
Both surfaces are a similar distance from ambient when hot, so the
instrument's error largely divides out of the *difference* even though it does
not divide out of either reading.

**29. Stop the capture. Do not clear the fault memory.**

## Some hundreds of kilometres later

**30. Read group 032 again** and photograph it. One screen, no session, no
instruments. This one matters and is easy to forget.

## What comes back

| | |
|---|---|
| the capture | filtered to `0x1A0`, `0x280`, `0x288`, `0x320`, `0x420` and `0x480` before sending |
| `final_z1.txt` | whole, it is small — it carries the 0x200 test and the oil reading |
| the VCDS log | as it comes, groups 003 and 014 |
| the photographs | every screen from steps 18 and 20–24 |
| two paper numbers, twice | group 006, before and after |
| the infrared readings | three spots cold (step 6b) and the same three hot (steps 28–28a), three readings each, with clock times |
| the overrun | *went quiet after about N seconds* / *never went quiet*, cold and hot — step 13 |
| the coolant, twice from VCDS | group 001 cold (step 6a) and hot (step 26a), each with its clock time |
| the mirror console reading | at the cold soak, before a door is opened |
| how it drives | in plain words |
| later | the second group 032 photograph |

---

# Part 2 — why each step is there, and how to read what comes back

## Steps 1–3 — why nothing is cleared, and why not on day one

**The lambda adaptations are the measurement, so clearing them destroys it.**
`032` reads **−4.7 % at idle against +1.6 % at part load**, and *moving toward
zero at idle* is the single cleanest sign that the injectors were the fault.
Clear the adaptations and the after-value starts at zero because it was forced
there, not because anything was repaired. The same argument covers the battery:
disconnecting it takes the idle adaptation (`055`, **−0.73 g/s**), the throttle
body adaptation and the readiness bits with it.

**The fault memory is evidence** and a cleared one also resets readiness, so
`100` would read "not complete" and say nothing about the new converter.

⚠ **How long the ECU needs to re-adapt to new injectors is not known here.** It
was asserted in conversation once as "weeks" and never written down or sourced,
so it is treated as unknown. **The procedure is built not to depend on it**:
nothing is cleared, the session is not delayed waiting for adaptation, and
`032` is simply read a second time later (step 30). The *movement* between the
two readings is the evidence, and that works whatever the time constant is.

**Why the day off, and why the drive home is wanted rather than tolerated
(step 2).** Two separate reasons, and the second is the stronger one.

**The first start after the injectors are fitted is not comparable to
anything.** The fuel rail was opened to change them, so it has air in it and
that start will crank long for a reason that is not the engine's health. **The
garage does that start**, and by the time the measured one happens it is the
third or fourth — which is what makes it a measurement rather than an artefact.

**The second is the stored adaptation.** From a cold start the ECU runs open
loop until the oxygen sensor lights off, and in open loop it uses the *stored*
adaptation rather than a live one. New injectors with a stale −4.7 % in memory
therefore carry that error straight into the warm-up.

⚠ **Closed-loop control does not protect the measured cold start**, and this is
the point worth being clear about: it corrects the mixture within seconds once
the sensor is live, which covers the warm idles and the pulls and covers
nothing at all about the first minute from cold. **The drive home, plus
whatever running the garage does, is the only thing that moves that stored
number before the measurement.** Seven kilometres is roughly ten minutes of
closed-loop running.

**But the confound is bounded, and smaller than an earlier version of this file
implied.** The adaptation is multiplicative, and cold start is *deliberately*
rich by far more than 4.7 %:

| | µl/s | against warm idle |
|---|---|---|
| measured, first 30 s from cold | **927** | **2.84×** |
| the same with a stale −4.7 % still applied | 883 | 2.71× |
| warm idle, `09_idle_60s_z1` | 326 | 1× |

**A mixture that was meant to be 2.84× and comes out 2.71× is still a cold-start
mixture.** So the drive home is worth having and is not worth engineering:
taking a longer route buys an unknown amount of an unknown quantity, while the
design already does not depend on convergence — that is what the second `032`
reading in step 30 is for.

**Why ten hours and not longer (step 3).** The before-recording,
`18_coldstart_z1.txt`, was taken about ten hours after the previous start.
**Matching it is worth more than making the test harsher.** A harsher after-run
that passes is nice; a harsher one that fails cannot be told apart from a
longer stand, and the clean before/after is the whole value.

## Steps 4–9 — the configuration, and the one screen rule

**The display and converter come out** because a capture carries b7, engine
speed, oil temperature, road speed, throttle and the fuel counter at about
ninety-four frames a second each, every one with the others beside it in time.
A display channel would be the same byte reduced to a held maximum.

⚠ **`OilTemp` is not the converter's.** Its TRI row reads `0x420` byte 3, the
car's own frame, so every capture already carries it.

**Groups 003 and 014, and not 010.** `014` already carries the load, so
`003 + 014` is a superset of `003 + 010` with the misfire counter added and
nothing given up — logging misfires costs no sampling rate at all. A third
group would drop the rate from about 1.7 samples a second to 1.1, and **the
rate is the one thing that cannot be recovered afterwards.**

**Mass air flow and engine load are the point of the second instrument** —
neither is on the CAN bus, so only VCDS can give them.

**Group 006 is read twice and never during the drive**, because reading it
means changing the group selection and that ends the log. The cold reading is
essentially ambient, the hot standing one is ambient plus engine bay — today's
cold start gave 22.5 °C standing with the oil starting at 12.75 °C — so the
pair **brackets** what the engine breathed during a pull. The
volumetric-efficiency table in `engine-health.md` wants a bound and gets a
narrower one.

**The two recordings do not need to be synchronised.** Engine speed appears in
both, so every VCDS sample matches to the right stretch of capture by its rpm
alone.

## Steps 10–11 — the start

**There is a before-picture and it is the one thing that cannot be repeated.**
`18_coldstart_z1.txt` holds one cold start on the old injectors:

| | |
|---|---|
| cranking | **1.24 s** at about 235 rpm |
| first firing | 451 rpm |
| then | **falls back to 311 rpm and nearly stalls** |
| running | 43.00 s, then a flare to 1446 rpm |

**A prime masks exactly that symptom**, which is why step 10 says not to — with
the qualification that the before-recording was taken with whatever the usual
start is, so "usual" wins over "clean".

**Step 11 exists because VCDS lost the ECU during cranking last time** and did
not recover by itself, which cost the whole start and the first 86 seconds of
running — the one thing the session was asked for.

## Steps 12–14a — why the idles are spread out, and why the coasts come first

⚠ **A hot idle alone would waste the trip.** A hot idle counted **zero before
the repair** — `11_idle_noac_z1` and `12_idle_ac_z1`, old injectors, 73 °C — so
zero afterwards says nothing whatever.

| state | oil | before, `dips_cheap()` | predicted after |
|---|---|---|---|
| cold idle | 13–17 °C | **12.1/min** | ~0 |
| warm-ish idle | 61.5 °C | **11.6/min** | ~0 |
| hot idle | 72.8–73.5 °C | 0.0/min | 0, and it says nothing |

**One minute at a matched temperature settles "gone or not gone"** — at 11.6 a
minute, seeing none in sixty seconds has a probability of 7×10⁻⁵ if nothing
changed. **Three minutes also settles "how much better"**, at p = 0.002 for a
halving. The whole analysis is `python tools/idledips.py CAPTURE`; no firmware
change and no display channel is involved.

⚠ **The middle idle is at a temperature, not at a time, and nothing in the car
tells you which you have.** The two rows above with a before-reading are cold
and **61.5 °C**; an idle at 40 °C is a fine measurement with nothing to compare
it to. And by step 12 the display and the converter are out (step 4) and the
VCDS screen is locked to groups 003 and 014 (step 9), **neither of which
carries oil temperature** — so the driver has no thermometer at all. **The
coolant gauge is not one**: the coolant was already 96.8–100.5 °C in
`09_idle_60s_z1` while the oil was 60.8, so the needle settles long before the
oil arrives.

**Nobody knows when the oil passes 61 °C on this car, either.** No fixture
records a warm-up under driving — `17_drive_property_z1` opens at 75 °C with no
note of how long the car had been running — so "the middle of the drive" is a
guess at the one measurement the trip is for.

**`oilwatch.py` is the answer to all of that** (step 12a), and it is worth
being clear about what it does and does not do. It does not measure anything
new: the capture has carried `0x420` byte 3 all along, and the tool only reads
the file as it grows. What it adds is that **the number reaches the driver in
time to act on** — it fits a slope over the last few minutes and converts it
into "the band arrives in about N minutes", which neither a fixture nor a
gauge can give. ⚠ **Its band is a decision, not a specification**, and the
header of the file says so: there are two before-readings with a non-zero rate
and one zero, and no measured width to take. It is centred on 61.5 °C and stops
well short of the 72.8 °C that already counted zero on the old injectors.

⚠ **It has to run on the machine holding the USBtin**, which is the one the
capture is being written on. A Claude Code session in the cloud cannot see that
file; a local one can, and can watch it for you.

**Without it, hedge, because extra idles are free** (step 12b). Step 15 already
says nothing needs marking and the analysis finds the idles by itself, and
`idledips.py` prints the oil and coolant beside every count, so afterwards you
keep whichever stop landed near 61 °C and the others are extra points on
exactly the continuous warm-up curve `engine-health.md` says would settle
whether the thermal lever is real. **The oil is slow enough for either route to
work**: it climbs about 0.75 °C a minute while idling (the figure is under
*Steps 27–28a*, and `09_idle_60s_z1` shows the same rate at 61 °C), so a
five-minute stop drifts some four degrees. **You cannot idle past the band —
only start outside it.**

### The first idle and the cold coasts compete, and the coolant is the budget

**Nothing else on this drive is a zero-sum choice and this is**, so it is
worth stating once. The first idle and the cold coasts both want a cold
engine, and idling is the most efficient way there is to stop having one:
**about 8 °C of coolant a minute**, measured off `18_coldstart_z1`, where six
minutes took it from 16.5 °C to 63.75 while the oil moved 4.5 °C.

**The two are indexed by different channels, which is what makes the conflict
soluble.** The idle dips are argued against oil temperature, and the oil is
nearly frozen on this timescale — it does not begin to move for the first
200 s, so a two-minute idle and a five-minute one are the same measurement.
**The cut is gated on coolant**, which is spent at 8 °C a minute. So the idle
gives up the minutes it does not need, and the coasts take the temperature
they cannot get back.

⚠ **Do not resolve it the other way round by putting the coasts first.** The
before-reading is 310 s of idling from the key, and an idle that follows two
minutes of driving is a different state — the oil would still match, but the
warm-up enrichment would not, and enrichment is what the puddling hypothesis
is about.

**High gear for the pulls, and the objection is to the RATE rather than to
sweeping.** The last drive got this wrong: every pull was a low-gear sweep
that crossed 2400 rpm in a moment, so there was essentially no full-throttle
data below 3000 rpm. **The three wide-open bursts in `17_drive_property_z1`
sweep at 1,900–2,100 rpm/s** — measured, and it is why all three were still
climbing when the throttle shut. A 400-rpm band gets about a fifth of a
second, which at ninety-four samples a second is a handful of frames taken
while the filling is still catching up.

**Fourth is roughly an order of magnitude slower** *(an estimate, not a
measurement — the gearing enters roughly squared and nobody here has the
ratios from a document)*, so a 400-rpm band gets seconds rather than
fractions of one, and **a slow sweep is a series of holds**. That is what
makes step 14's 2,200-to-as-high-as-it-goes better than a hold at one engine
speed rather than a retreat from it: it covers the whole range at a rate where
b7 can settle, and it does not require guessing in advance where the maximum
is on an engine that has been remapped.

**If the oil stops climbing and you want `can-decoding.md` question 7 closed
outright**, add the free-revving holds from that question at the end while it
is hot. They will display nothing, and there is no display fitted anyway — the
holds are read off the raw log and b7.

## Step 18 — what each screen is for

**`014` — misfires.** `Rozpoznani` must read **`aktivováno`**; `deaktiv.` means
the engine is not running and the number beside it is meaningless. **It is a
current count, not a total.** Before the work it took the values **0, 12, 13,
24 and 36 and nothing else**, held each about three seconds and returned to
zero — against a label file that specifies 0 to 5.

⚠ **A log of zeroes is evidence and not proof.** At 1.7 samples a second a
brief event falls between samples. An hour is about six thousand samples, which
is a strong statistical argument and still not the same as none having
happened. **This screen is the one where it is watched continuously**, which is
why a minute of watching is asked for rather than a glance.

**`032` — the lambda adaptations**, and see steps 19–24 below for the fork that
decides what they mean.

**`055`/`056` — the idle regulator.** Specified −2.00 to +2.00 g/s, its
adaptation −1.50 to +0.150 g/s, target idle 780 rpm. The before-reading, over
five minutes of cold idle: the regulator worked between **−0.63 and +0.01 g/s**,
mean −0.31, and the adaptation sat at **−0.73 g/s and never moved**. An
adaptation is stored, so one run cannot shift it; only the next reading shows
whether it has.

**`100` — readiness and OBD status.** Reading `00000000` says every monitor has
completed. **Completed is not passed**, which is why step 20 exists.

## Steps 19–24 — the four blocks that give verdicts

**These are the only measurements here that need no baseline**, which is what
makes them valuable on a car whose "before" can no longer be produced.

| block | checks | the answer |
|---|---|---|
| **046** | catalytic converter conversion | `CatConvB1 OK` / `not OK` |
| **034** | pre-cat oxygen sensor ageing | `B1-S1 OK` / `not OK` |
| **037** | post-cat sensor, basic setting | `Sys. OK` / `not OK` |
| **036** | post-cat sensor availability | `B1-S2 OK` / `not OK` |

**Both oxygen sensors on this car have already been replaced once**, so **any**
`not OK` is a second failure of that sensor — which argues for something that
keeps killing them rather than for a worn part. Both have also sat in the
exhaust of a converter that was burning through.

**That is what makes `032` mean something**, and the fork is clean:

| 034 / 036 / 037 | what −4.7 % at idle then means |
|---|---|
| all `OK` | the ECU is correcting a **real** fuel excess — the injectors |
| any `not OK` | a second sensor has failed; the adaptation may be its artefact, and `032` is re-read after it is replaced |

**The converter temperature these blocks display is a gate, not a reading.**
There is no need to know what a healthy catalyst temperature is: the number is
an entry condition and the ECU supplies the judgement. That is also why step 19
says to watch the block's own fields rather than quoting rpm ranges here — the
block knows them.

**`070` operates the evaporative valve.** If the purge is shut while the engine
stumbles, the alternative explanation for the idle is out.

⚠ **`022` and `023` — knock retard per cylinder — are deliberately not in this
session.** They are the only per-cylinder signal this ECU offers, but they are
a live value under load: at idle after a drive nothing is knocking and they
read what a quiet engine reads. Catching them needs a third logged group, a
broken log, or a passenger. **Their own session, with somebody else holding the
laptop.**

## Steps 27–28a — the thermometer

**`can-decoding.md` question 10 is whether the oil temperature is *right*, not
merely oil.** The channel never exceeds 77 °C and sits twenty-odd degrees
*below* the coolant in every state ever recorded, including an hour of driving
that peaked at 72–74 °C. A warmed engine under load normally runs its oil at
90–110 °C and above the coolant.

⚠ **No screen can settle this.** `01-Motor` has no oil temperature block at
all — every temperature it defines is coolant, intake air or catalytic
converter. The thermometer is the only test there is, and it matters because
the drag line question 7 is still open about is fitted against that number.

**There is a gap between the last bus frame and the thermometer, and it does
not matter.** Switching the engine off takes the ignition with it, so the bus
stops; the reference is the last `0x420` b3 the capture recorded before that.
A minute or two of standing does not move sump oil measurably — over the whole
cold-start run it climbed at 0.75 °C a minute *while being heated*, and the
channel's resolution is 0.75 °C a count. **The question is whether the channel
and a thermometer agree to within a few degrees, not to within a tenth.**

⚠ **An earlier version of this file had the thermometer taken before the 0x200
test, with the engine restarted afterwards** — two switch-offs, one restart,
and VCDS reconnected in order to run a test about reconnecting VCDS. Worse, the
capture had stopped at step 17, so the reading it was to be compared against
had nothing recording. One capture across both steps fixes both.

**The reading does not have to be at peak oil temperature**, which is just as
well: by this point the engine has idled through every static read. The
question is whether the channel and a thermometer agree at one moment, not what
the highest number of the day was.

### The cold readings at step 6b — what the pair does, and the one thing it does not

**The proposal was the maintainer's and it is a good one**: read the same
spots at the cold soak, so the hot readings have a reference rather than
standing alone. Three of the four things it buys are real. The fourth is the
one everybody expects and it is not available.

**What it buys:**

- **Aim, which is not trivial and is invisible afterwards.** A hot reading
  three degrees out because the spot was half tarmac looks exactly like a hot
  reading. A cold one does not: it has to come out at ambient, and if it does
  not, the aim is wrong while there is still time to fix it.
- **The instrument against two others.** VCDS group 001 and the mirror console
  are already being read at the same soak for the same reason, so a
  thermometer that reads 3 °C high against both of them has a **constant
  offset**, and that one *is* subtractable.
- **The noise floor of the method.** Three spots that must all be at one
  temperature, and what they actually span, is the honest error bar on every
  reading at step 28. Three is a thin sample and it is still the only one
  anything here produces.
- **A sixth row for step 6a's table**, and the only one that reads the *oil*.
  Every other row at that soak is coolant, intake air or ambient; the filter
  and the sump are the oil's own container, so the cold soak stops being an
  inference about the oil and becomes a reading of it.

⚠ **What it does NOT buy is an emissivity correction to subtract from the hot
reading**, and this is worth being exact about because the assumption behind
the proposal was that the error would be the same cold and hot. It is not.
**An infrared thermometer with the wrong emissivity reads a blend of the
target and of whatever the target is reflecting** — its surroundings. At a
cold soak the target *is* its surroundings, so the blend is exact and **the
reading comes out right whatever the emissivity is**. The error is
proportional to how far the target sits from its background, which is zero
cold and sixty-odd degrees hot. So the cold reading cannot see the very error
it looks as though it measures.

**Which costs nothing here**, and that is why the step stays. Question 2 is
*77 °C against 103 °C* — a 26 °C fork, not a calibration — and the error an
emissivity of 0.85 taken for 0.95 makes on a painted can at 100 °C is a few
degrees. **Take the cold readings for the four things above and do not
subtract them from anything.**

⚠ **Hot oil and an open bonnet.** The dipstick tube is not the exhaust, but
there is no hurry here — take the minute.

## Steps 25–26 — the 0x200 test

`18_coldstart_z1.txt` is the only log carrying identifier **0x200**, twice, and
both times it fell in the window where VCDS had dropped the ECU and was being
reconnected by hand — while `11`–`17` hold half an hour of bus with VCDS merely
*attached* and never show it. **If 0x200 appears, it is the tester and not the
car**, and the same goes for the only two frames in the whole corpus where
`0x5D0` byte 0 is not zero, each of which follows a 0x200 within 90 ms.

**With the engine running and VCDS already connected**, which is the state the
session ends in anyway — so this costs the seven minutes the capture runs and
no setting up at all. Nothing depends on the answer; the alternative is leaving
a fifteenth identifier on the bus unexplained.

## Which measurement settles the torque scale — steps 14 and 14a, and nothing else

**No VCDS block answers this.** Every block in this session is about the
engine's health; **the scale question is settled by the capture**, and
specifically by the two or three **full-throttle pulls in a high gear**:

| what is needed | where it comes from |
|---|---|
| **b7's real maximum at full throttle** | `0x280` byte 7, out of the capture, at 94 samples a second |
| the ECU's **load** at the same engine speed | the VCDS log, group 014 |
| the **air** at the same engine speed | the VCDS log, group 003 |
| the **fuel** at the same engine speed | `0x480`, out of the capture |

**That is the whole of it, and it is why the pulls have to be in a high gear.**
The scale rests on the premise *b7 = 255 corresponds to the rated crank torque
plus the drag at that speed* — a premise nothing has ever tested, because
**this engine has never been observed anywhere near b7 = 255.** The pulls are
the attempt to find out what b7 actually reaches when the engine is given every
chance: full throttle, near peak torque, held rather than swept. **The last
drive got this wrong** — every pull was a low-gear sweep that crossed 2400 rpm
in a moment, so there was essentially no full-throttle data below 3000 rpm, and
b7's maximum came from the wrong part of the curve.

⚠ **There is now a number to expect, and it did not come from a capture.**
The Šumava drive of 2026-09-19 showed a steady 117 Nm at full throttle above
4,000 rpm, which inverted through this firmware's own arithmetic implies **b7
near 196** — higher than the 185 `b7scan.py` finds anywhere in the fixtures,
and the first such reading that was not still rising when it was taken.
`engine-health.md`, *What the two torque readings imply about b7*, has the
derivation and its error bars. **It is a display reading with an estimated
engine speed under it and it replaces nothing here**; what it does is say that
the pulls are expected to land near the bottom of the 196–217 band below
rather than to surprise anybody.

**The health verdicts are what licence you to believe b7max.** They are not a
parallel investigation that happens to share a session:

> **A low b7 maximum on a sick engine says nothing about the scale.** It says
> the engine did not make the torque. Only once 046, 034, 036, 037, the misfire
> count and the idle dips agree that the engine is well does a low b7 maximum
> become evidence that **the scale is wrong**.

That is exactly what step 1 of *the decision tree* below means by *"otherwise
you are calibrating against a sick one"*, and it is the reason this is one
session rather than two.

**The fourth row is the second, independent route.** Measured air divided by
measured fuel over the same pulls gives the real air-fuel ratio, which removes
the largest assumption from the efficiency argument in `engine-health.md` —
and that argument is what says the engine should be making about 150 Nm where
the display shows 117. ⚠ **It is weaker than it looks in one direction:** the
fuel counter measures what the ECU *commanded*, not what left the injector, so
a leaking injector would deliver more than the counter reports. **A high
reading would prove something; a normal one proves less.** Which is precisely
why it is taken *after* the injectors are replaced rather than before.

## The capture filter

**Sizes measured on `18_coldstart_z1.txt` rather than estimated.** The whole
bus is **65 MB an hour**; the six identifiers kept are **52 % of the bytes,
about 34 MB an hour**, so about 42 MB over the seventy-five minutes.
`usbtin_capture.py` writes line by line, so an interrupted capture keeps
everything up to the interruption.

**Keep `0x1A0`, `0x280`, `0x288`, `0x320`, `0x420` and `0x480`.**

| | share of the bus | filter total |
|---|---|---|
| `0x1A0`, `0x280`, `0x420`, `0x480` — the old four | 36.4 % | 24 MB/h |
| `0x288`, the coolant | +11.2 % | 31 MB/h |
| `0x320`, the tank | +3.9 % | **34 MB/h** |

⚠ **`0x480` is in that list and an earlier version of this file left it out**,
which would have thrown away the one thing the capture is still needed for.
Everything else can now be read off the display or the VCDS log; the **fuel
counter cannot**, and it is what removes the air-fuel assumption from the
efficiency argument in `engine-health.md` — measured air from group 003 over
the same pulls, divided by measured fuel. **Filter it out and the pulls have to
be driven again.**

⚠ **`0x288` USED TO BE DELIBERATELY OUT AND IS NOW DELIBERATELY IN**, and the
reversal is worth reading rather than skipping. The old reasoning was that the
coolant *"sat at 99 °C in all three warm idle fixtures while the thing being
measured moved"* — nine megabytes for a channel that never does anything. That
was correct about the coolant and wrong about what would be asked of it: **the
coolant has since become the reference every temperature argument leans on**,
and question 10 in `can-decoding.md` now turns on comparing it against `0x420`
b3 at one moment on a cold-soaked car. A channel that sits still is exactly
what makes a good reference. Nine megabytes for the two points that settle two
scales is not a close call any more.

⚠ **`0x320` is in for a different reason and it was never considered before.**
The tank level is what the refuelling rule watches, and after `refuted.md` C10
that rule needs a drive it has never had: every fixture with a moving car in
it has 0–10 L aboard. Four more megabytes buys the whole of question 4 below,
and without them it cannot be asked at all.

---

## The prediction, written before the drive so it can be wrong

**If the injectors were the fault:** the car pulls better, the first-gear
misfires go to zero, the idle stumbling disappears **at every oil temperature
rather than only when hot**, and the idle adaptation moves toward zero — while
**load stays near 78 % and the torque the display would compute stays near
117 Nm**.

⚠ **Read that as "if the repair was the fault".** The plugs that came out on
17 September were eroded and carbon-coated at about 1,500 km, so they are not a
null change, and fouled plugs misfire at low load and high vacuum — the same
signature. **Nothing measured on this drive can separate the two**, unless a
cold capture was taken in the window between the two visits.

**The fuel filter is the third part changed and it is very nearly not a
confound at all**, which is worth the paragraph because an earlier version of
this section made it one.

**The argument for calling it a confound:** a restricted filter limits supply
under demand, so it could hold down the pulls, b7max and the power — the half
*the decision tree* below reads. It could never make an injector dribble into
a cold port, so the idle stumbles and the cold overrun of step 13 were never
touched by it either way.

⚠ **But restriction on this car has an observable, and it has been absent for
years.** This car used to show visible fuel starvation under load — it would
stop pulling and then pick up again — and `vehicle-history.md` records that it
has not done so for years. ⚠ **Whether the filter or the fuel pump cured it is
not established and does not matter here**: what the confound needs is
restriction *now*, and **that symptom is the direct observable for it**. The
drives that would show it have been driven, including full throttle to
5,000 rpm.

**So the confound is bounded near zero rather than argued away.** What survives
is the residual: absence of visible starvation rules out *gross* restriction,
not a few per cent of rail pressure under full load that nobody could feel.
`032` reads **+1.6 % at part load**, which is a small correction and points the
same way — ⚠ **as far as part load goes, and no further**, since wide-open
throttle runs open loop and the trims do not cover it.

⚠ **It is not there as a suspect at all.** Nothing points at the filter; it is
going in to protect the new injector nozzles, and `vehicle-history.md` has the
reasoning and the five-year interval that follows from it.

**Fitting it before the drive rather than after is still the right way round.**
Holding it back would separate nothing — a starved rail and a leaking injector
are both fuel delivery and no measurement here tells them apart — and it would
leave a part of unestablished age in the measurement chain for the one session
meant to establish what this engine can make. It is worth
knowing which claim the result supports before the result is in hand: "the
engine was unhealthy and is now well" survives either way, and "it was the
injectors" does not.

**Compression was measured at that visit and came out even at 13 bar across all
four**, which removes a burnt valve, a broken ring pack and a head gasket
between cylinders from every row above. Those were the explanations that would
have survived a full set of new parts and kept the stumble; they are gone, so a
stumble that persists after the injectors points at fuelling, air or control and
not at the bottom end.

⚠ **That last clause rests on an unsourced premise and is the weakest thing in
this document.** It assumes the ECU's torque model cannot see a fuelling fault,
which needs the lambda entering that model to be the *commanded* value — and
nothing this project holds says so. **Misfire detection is per-cylinder and
does run on this car**, so the ECU is not without a combustion signal; whether
it reaches the torque model is simply unknown.

Which makes it the most informative line here rather than the least: **if b7
rises while load and airflow stay put, the premise is wrong and we learn
something no other measurement on this drive can give.**

⚠ **"b7 rises" has to mean against load, never against last time.** `python
tools/b7scan.py` says why: the largest b7 this engine has been seen to make is
**185**, and all three wide-open bursts it comes from were **still climbing
when the throttle closed** — low-gear sweeps that ended before the engine
reached a steady filling at any speed. **This drive's pulls are deliberately
better ones**, in a high gear and held, so b7max is expected to come out higher
whatever the injectors did. **A higher b7max is therefore not evidence of
anything**, and reading it as the premise failing is the easiest false positive
available on this drive.

What is comparable is **b7 against the ECU's load at the same engine speed**,
both of which this session logs anyway — b7 from the capture, load from group
014. If that ratio is where `docs/frames.md` puts it, near the relative load
itself, the model is charge-dominated and the repair did not move it. If b7
has risen *relative to load*, the premise is wrong and that is the result.

**On the idle specifically**, a repair that removes the stumbles only in the
hot state has not removed the cause.

---

## After the reflash — the one check that costs nothing

**The loop this drive starts ends with a reflash**: the capture gives the
numbers, `TORQUE_CNM_PER_BIT` and the drag line move together if the tree below
says they should, the hex is rebuilt and programmed, and then the display is
looked at.

**Put `Torque`, `Power` and `RPM` on the same page and photograph one steady
moment.** All three are already on the display in the normal fitted
configuration, two from `0x601` and one straight off the car's `0x280`.

⚠ **There is no `TorqRaw` channel and none is wanted.** `S-AQY.TRI` carries 31
sensors and that is not one of them; it never was, in any commit of `mfd15`.
The raw byte is already in the capture at ninety-four samples a second, and
`mfd15/README.md` records that the display sometimes loses its sensor
definitions when a page's contents are changed. Editing a working configuration
for a convenience is a poor trade. If it is ever genuinely wanted it can be
appended then.

**It is worth the one photograph because it closes a gap nothing else can.**
The host tests check the core under gcc; the device runs XC8 over the
hand-written wide arithmetic in `fastmul.h` and `divconst.h`. *Compiling proves
nothing about the silicon*, and a green host test is evidence about the code
and a **hypothesis about the device**. A single frame showing b7, engine speed
and the torque computed from them is the only thing that has ever tested the
arithmetic **as the part actually executes it**.

⚠ **Set the scale before reaching for `TORQUE_TRIM_PCT`, not at the same
time.** Adding a few per cent on top of a scale that is itself being changed
leaves two unknown corrections on one number and no way to tell which is doing
what.

---

## What happens after the reading — the decision tree

**Step 1 is the engine, because otherwise you are calibrating against a sick
one.** Does it pull better with the new injectors? If not, today's numbers were
already its best and you go to step 2 with them; if it does, re-measure first.

**Step 2 is b7's maximum at full throttle**, taken out of the capture, with the
ECU's load from the same engine speed beside it.

```
b7max >= 235
  -> The scale is right and the engine is well. The display reaches
     near the factory figures. NOTHING CHANGES.

b7max 200-235
  -> The scale is roughly right; the display reads 5-15 % under.
     TORQUE_TRIM_PCT closes that if the owner wants it closed.

b7max <= 200   (what this car reads now)
  |
  +- load also unchanged, near 78 %
  |    -> Same air, same modelled torque. Either the engine is still
  |       unwell, or THE SCALE IS WRONG. What separates them is how the
  |       car drives: if it pulls properly, it is the scale.
  |
  +- load jumped, near 85 %
       -> The engine breathes better and b7 did not follow, so b7 is not
          what this firmware thinks it is and the derivation is rebuilt
          from the beginning rather than rescaled.
```

### What the air already says about these branches

**The tree has no thermometer in it, and it needs one.** `frames.md`, *What
that gap is worth in Nm*, turns each b7 into the intake air it would require,
because relative load is the engine's filling times the density of the air it
breathes: **the same healthy engine reads b7 ≈ 196–217 at a September intake of
25 °C and 214–237 at 0 °C.** That is a tenth of full scale from the weather
alone, and it **straddles the 200 boundary below**. So b7max off one drive is
not a number that can be compared with a threshold until the intake temperature
is beside it — which is what makes step 6's reading of group 006 part of this
measurement rather than a formality.

**What survives the correction, and is the finding:** **b7 = 255 needs intake
air between −44 and −19 °C.** The scale's premise — that full scale is the rated
crank torque plus the drag at that speed — asks for a condition this car is
never driven in, so **the two factory figures are unreachable rather than
merely unobserved**, and *the scale is right and nothing changes* is not a live
outcome of this session. `frames.md` brackets what replaces it at **0.90–0.96
Nm/bit** against the 0.74 shipped, by two independent routes.

⚠ **`b7max >= 235` is not impossible, and a first version of this section said
it was.** It needs a hard frost — −24 to +2.5 °C of intake — which rules it out
on this drive and not in principle. **On a September drive, expect b7max near
196–217**, which is why the branch this lands in has to be read with the
thermometer and not off the number.

⚠ **"Load stays near 78 %" is the healthy prediction, not a symptom.** The
lower branch offers *either the engine is still unwell, or THE SCALE IS WRONG*
as though the load were silent between them, and it is not: at the intake
temperatures of that drive, 78 % is a normally breathing engine —
`engine-health.md` says so. **That rules out a breathing fault and only a
breathing fault** — b7 may yet see combustion, which is the open hypothesis
above, so a well-breathing engine burning badly could still hold b7 down. The
branch stands; what it no longer gets to assume is that low load is itself
evidence of a sick engine.

⚠ **And item 1 below is superseded in its numbers.** Its 1.08–1.26 Nm/bit comes
from extrapolating `17_drive_property_z1`, whose wide-open bursts were low-gear
sweeps still climbing when the throttle shut — the flaw this document names two
sections up. The relative load VCDS logged is **flat at 78.1 % from 3000 to
6000 rpm**, so the plateau b7 should be looked for near **200 rather than
149–174**. The bracket that replaces the scale is still the finding rather than
the number — but it should be built on the plateau these pulls measure, at the
intake temperature they measure it at.

### What the last branch actually changes

**The formula does not move. One premise does.** Today it reads *b7 = 255
corresponds to the rated crank torque plus the drag at that speed*. It would
become *b7 = the observed maximum at full throttle corresponds to the rated
figure*.

1. **`TORQUE_CNM_PER_BIT` rises.** Sketched against b7 extrapolated from
   `17_drive_property_z1`'s wide-open samples, the 85 kW rating asks for about
   1.08 Nm/bit and the 170 Nm rating for about 1.26.
2. **And that bracket is the finding, not the number.** It is roughly **15 %
   wide, against the 0.3 % the current derivation reports.** The 0.3 % was
   never a precision: substituting 255 into both rating equations pins them to
   the same nail, so of course they agree. Pull the nail out and the two
   factory figures start arguing, which is an honest picture of how well this
   is known. **Whatever replaces the scale should quote the bracket its own
   assumption produces, not inherit this one.**
3. **The drag line is rescaled, not refitted.** `drag_b7 = 9.11 + 0.006514 x
   rpm` is in bytes and does not move; `DRAG_TORQUE_BASE_CNM` and
   `DRAG_TORQUE_SLOPE_Q16` are that line times the scale, so they follow it.
   This is what `config.h` means by the two being one calibration.
4. **Both ceiling tests are rewritten.** `test_full_scale_reaches_the_rated_power`
   and `..._torque` assert what b7 = 255 produces. They would assert what the
   OBSERVED maximum produces — which is the first version of that test with a
   measurement behind it.
5. **`TORQUE_TRIM_PCT` is not the tool for this** and must not be used as one.
   A scale that is wrong is wrong for everybody who builds this firmware; the
   trim is one owner's gain on a correct scale. Fixing the first with the
   second leaves the next person a number that no longer means what its
   comment says.

---

## What this session answers

| question | what settles it |
|---|---|
| **is the engine well now** | first-gear misfires, the stumbling idle against oil temperature, the idle adaptation, how it pulls |
| **is the new converter converting** | block 046, and it needs no baseline |
| **are either of the replaced oxygen sensors gone again** | blocks 034, 036, 037 |
| **can the display ever show the factory maxima** | **the high-gear pulls, steps 14 and 14a** — b7 out of the capture against the ECU's load at the same engine speed. See *Which measurement settles the torque scale*; no VCDS block answers this |
| **does the oil ever get hot enough to matter** | the oil temperature a long drive actually reaches, and the thermometer beside it |
| **what a healthy idle and a healthy start look like as numbers** | the three-to-five-minute idles and the morning's cold start, through `tools/idledips.py` *with the constants frozen*. Not the same question as *is the engine well* — it is the other end of a scale whose only anchor today is the engine before the repair, and it decides whether anything gets built at all. See question 6 |
| **does the ECU cut fuel on a COLD overrun** | step 13's cold coasts through `tools/coastscan.py`. Warm it does, four times over in the last capture; cold decides whether the owner's oldest symptom means anything — `engine-health.md`, *The oldest symptom is on the overrun* |

**The last one is close to answered already.** The drive of 2026-09-10 peaked
at **72–74 °C of oil after about an hour**, and the warm holds the drag line is
fitted to are 72.8–76.6 °C — the same range. `can-decoding.md` question 7 rests
on "72–77 °C is warm, not the 95–110 °C of real driving", and that sentence
appears to be false for this engine. **Unless question 10 is the reason it
appears false**, which the oil filter reading settles.

---

# The questions, and what each one changes in `src/`

**This is the list to work from in the session after the drive.** Everything
above is how to collect; this is what to do with it. The questions are
independent except that **question 1 comes first and the next two lean on it.**

**Questions 1 to 5 change a number that already exists. Question 6 adds a
channel that does not**, in this repository and in `mfd15` together, and it is
the only one on the list that does.

⚠ **THE CONVERTER IS OFF THE BUS FOR THIS WHOLE DRIVE** — step 4 takes the
display out and the USBtin takes its place. So nothing here is answered by
watching a gauge. Questions 1–3 are answered from the capture and the
paperwork; **questions 4, 5 and 6 are answered by replaying the capture through
the core**, which exercises `decode.c` and `compute.c` exactly as the device
runs them and only leaves out the HAL. Nothing needs flashing beforehand.

## 1. The coolant scale — `× 0.75 − 48`, never verified

**Measured by:** VCDS group 001 at the cold soak (step 6a) and hot (step 26a),
each against the `0x288` b1 raw byte at the same clock time in the capture.
Two points, two unknowns, so the slope and the offset both come out —
**measured rather than bracketed for the first time.**

⚠ **BOTH readings are needed and the cold one is not the important half.** A
single point fixes an offset and says nothing about a slope, so the cold soak
on its own cannot tell 0.75 from 1.0. What makes it worth taking anyway is
that it is a free falsification test and that it gives *truth* rather than
another channel to compare against — step 6a has the three things it buys,
including the one that would flip the suspicion.

**Why it is first:** questions 2 and 3 use the coolant as their reference.
Today it is only known to be *plausible*: physics brackets its slope at
0.573–0.891 and 0.75 sits inside, which is corroboration and not measurement.
`can-decoding.md` question 10 has the arithmetic.

**Changes if it is wrong:** `temp_c100()` in `src/decode.c`, the table in
`docs/can-decoding.md`, and **every temperature conclusion in this repository
gets re-read** — including the ones that closed question 4 and the
thermostat entry in `engine-health.md`.

## 2. The oil scale — the live suspicion

**Measured by:** two points, as above.
- **cold**: the oil raw at the soak, against the coolant at the same moment,
  now on a verified scale. Step 6a's table is that point.
- **hot**: the oil filter reading at step 28, against the last `0x420` b3 in
  the capture.

**The bar is low and worth knowing before worrying about accuracy: the
question is 77 °C against 103 °C.** A 26 °C gap, not a calibration to a
degree, so infrared with all its emissivity sins settles it.

⚠ **The filter is not the sump, and the sender is in the sump.** The filter
carries gallery oil, a few degrees off what the pan holds. Inside 26 °C by a
wide margin, so it does not matter here — but it would matter if anybody ever
tried to calibrate rather than to choose between two candidates.

**Changes if the slope is wrong:** the oil line of `temp_c100()`, question 10
closes, and **question 7 is re-read rather than answered** — the drag line is
fitted against b7 at those holds and does not move, only the temperature
written beside it does. A wrong label is not a wrong line.

⚠ **The two-cold-soak experiment in `can-decoding.md` question 10 will NOT be
satisfied by this drive.** It needs two soaks about 15 °C apart and
`18_coldstart_z1` was 16.5 °C on a September morning; another September
morning is within a couple of degrees and resolves nothing. It stays available
as a free confirmation **on the first genuinely cold morning** — twenty
seconds of ignition-on, engine not started, no driving.

## 3. The torque and power scale — `TORQUE_CNM_PER_BIT`

**Measured by:** steps 14 and 14a and nothing else. *Which measurement settles
the torque scale* above is the whole argument and is unchanged by today.

**Changes:** `TORQUE_CNM_PER_BIT` in `src/config.h`, and the drag line with it
if the fit moves — **never one without the other**, per `CLAUDE.md`. The
intake air from group 006 is part of the measurement rather than a formality,
because b7 carries the charge normalisation.

## 4. The refuelling rule — does the new logic hold on a real drive

**Measured by:** replaying the capture through the core offline. `0x320` is in
the filter for this and nothing else.

**What to check, in order:**
- **it must not fire.** Not once, anywhere in the drive.
- **how close it came.** The longest run of consecutive at-rest samples above
  `REFUEL_RISE_L`, against the 5 it needs. On the old fixtures that was 1 of
  5, which is a coincidence rather than a margin; this drive says whether a
  real tank level changes the answer.
- **what the at-rest samples actually look like** with fuel aboard. Every
  fixture in the repository has 0–10 L in a moving car, and `refuted.md` C10
  is what that cost.
- **what the float does at the top stop.** The tank is brimmed (step 4a), so
  this is the first recording of the sender at the top of its travel in
  motion. Whether the slosh is clipped, whether the reserve bit behaves, and
  what the raw spread is up there are all new.

⚠ **Read the first bullet against step 4a's caveat.** A brimmed float cannot
swing upward past its stop and the rule fires only on a rise, so a full tank
is the state in which a false reset is *least* likely. **A clean result here
is a floor and not a proof**, and the middle of the travel — which only the
drives after this one reach — is where the rule is actually at risk.

**Changes if it fires or comes close:** `REFUEL_ARM_S`, `REFUEL_RISE_L` and
`TANK_STATIONARY_MMH` in `src/config.h`, and a fixture from this drive added
to `test/fixtures/` so it can never regress silently.

## 5. Range — free from the same replay, and easy to forget

**Not on the maintainer's list and it belongs there.** The rolling basis was
rebuilt this week so that it survives a reset and an ignition cycle, and the
only evidence for it is unit tests. This drive has stops, idles and restarts
in it, so replaying it says whether the basis behaves across them — whether it
stays in a sane band, and whether anything makes it collapse or run away.

**Changes if it misbehaves:** `RANGE_BASIS_SHIFT`, `RANGE_DEFAULT_L100_D` or
`RANGE_MIN_MM` in `src/config.h`, and the same fixture covers it.

## 6. Idle dips on the bus — the one change that ADDS a field rather than moving one

**Not a calibration. A new channel**, and the only item on this list that
changes `mfd15` as well as `src/`. It is here because the measurement that
justifies it is taken by this drive and by no other, and because the decision
would otherwise be taken with the rough engine already gone.

**The want, in one line:** the converter grades how steadily the engine idles
and how well it started, and puts both on the bus as numbers a driver can
watch over months. A pseudo-diagnostic — engine speed and a clock, nothing
else, from a device already on the bus and already awake.

**It is a trend instrument and it is not a fault detector**, and every
decision below follows from that. It does not need to be right in absolute
terms. It needs to move when the engine moves and to sit still when it does
not, so that a set of plugs or an injector going off can be *seen* rather than
inferred from how the car feels.

### What this drive settles, and why the decision cannot be taken without it

`docs/engine-health.md`, *The idle counter*, is a prediction written before the
repair: `dips_cheap()` counts **12.1/min cold and 11.6/min at 61 °C on the old
injectors**, and ~0 after, with the constants frozen so the after-reading is
taken on the same instrument. This drive is that after-reading, and it has a
second job the prediction table does not show.

**The missing half is a healthy engine, and everything rests on it.** Every
recording in this repository is of the engine *before* the repair — the rough
ones and the smooth ones alike. So the separation measured in
`engine-health.md` is between temperature states of one engine, and **nothing
yet shows that any of these instruments separates sick from well.** That is
what this drive supplies, and there is no second chance at it: once the engine
is well, the other end of the scale is gone for good.

**So the reading to take is not only "is it cured".** Out of the
three-to-five-minute idles the procedure already asks for:

| | what it fixes |
|---|---|
| the **grade** at each oil temperature, `--roughness --windows` | the healthy curve, to lay against `18_coldstart_z1`'s. **This is the measurement the whole design hangs on** |
| the **count**, `dips_cheap()` with its constants untouched | whether the validated-against-the-ECU instrument still says anything at all, or has gone to zero |
| the spread between idles at matched temperature | whether a trend is readable against the scatter |
| the **cold start**, on the morning of the drive | the first recording of a start that is not the bad one. n goes from 1 to 2 |
| `--cylinders`, the `sd_true` band over the healthy idles | the well-engine end of the per-cylinder spread. Three smooth runs exist today and two of them are one log; after the repair the sick end is gone for ever. Costs nothing — the capture is being made anyway |

**None of that adds a step to Part 1.** The capture starts at step 7 and the
engine not until step 10, so the cold start is already inside it — the
procedure has to be *read* differently, not performed differently, and the
whole of question 6 comes out of the recording the drive was going to make
anyway.

⚠ **If the healthy grade does NOT separate from the sick one at matched
temperature, question 6 is answered "no" and nothing gets built.** That is a
real possible outcome and it is the cheapest one: the whole channel would be
measuring idle-speed noise that has nothing to do with combustion. **Say so
plainly if it happens** rather than shipping a row that moves for reasons
nobody can name.

⚠ **Nothing re-tunes anything against the healthy engine.** Re-fitting a
threshold or a deadband there is fitting to the null: any threshold reads zero
on a well engine, and an instrument tuned to read zero measures nothing. The
constants are frozen in `tools/idledips.py`, two tests exist whose only job is
to fail if they move, and having new data does not supersede that — the new
data is the *other end* of the same instrument.

### The count is the wrong instrument, and it is the fixtures that say so

**A count past a threshold has no resolution below the threshold.** If the
repaired engine dips 5 rpm once a minute, `TRIP_RPM` = 20 reads **zero for
ever** — and so does it read zero if the engine slowly gets worse again, right
up until the day it crosses 20. A channel that reads zero for years cannot say
whether anything is improving, which is the one thing it is wanted for.

**This is measured, not argued.** `docs/engine-health.md`, *Grading the idle
instead of counting it*, sorts the whole deviation of a settled idle by the
size of the step that produced it: on the rough engine, everything at 20 rpm
and over is **2–3 %** of what is happening, while the **10–20 rpm band carries
about a third** — and `TRIP_RPM` sits just above it. On the smooth recordings
the ≥ 20 band is exactly nothing, which is why they read 0.0/min rather than
reading *small*.

**So the count is replaced on the bus, not supplemented.** It stays in
`tools/idledips.py` and it stays the thing that was correlated with the ECU's
own misfire counter at p = 0.023, which is the only evidence tying any of this
to combustion. **The bus carries the trend; a capture carries the diagnosis**,
and that division is deliberate: 0x604 answers *is it getting better or
worse*, and it will never answer *what is wrong*.

### What goes on the bus instead — a grade, and it is already anchored

**The measure is the step between one firing event and the next, dead-banded
and averaged:** `max(0, |Δrpm| − 3 rpm)`, on the gate the counter already
uses, over settled idle. `engine-health.md` has the numbers and the three
limits; what matters for the design is:

| | |
|---|---|
| the engine **before** the repair | **2.12 rpm**, from two independent recordings 45 °C apart agreeing to three figures |
| the smoothest thing ever recorded | 0.60 rpm, and **not at the floor** |
| contrast | 2.71× |
| repeatability | 13–15 % over 10 s, **3 % over 30 s** |

**Why the step and not the deviation from a baseline.** A first-order baseline
lags, so through a warm-up — idle falling from about 930 to 800 rpm — it sits
permanently above the signal and manufactures roughly 1.2 rpm of one-sided
deviation out of nothing. Against 20 rpm dips that is noise; against a healthy
floor of a few rpm it would be most of the answer. The step is immune: the
same ramp is 0.004 rpm per sample.

⚠ **The step is taken once per CHANGE of the field, not once per frame — the
opposite of `dips_cheap()`.** Not an inconsistency: that detector's EWMA is a
*time* constant and must be stepped on the clock, this one is an average *per
firing event* and must be stepped on the event. 0x280 holds its speed field
for three to four frames at idle and the hold length moves with engine speed,
so stepping this per frame makes the answer depend on idle speed through the
hold ratio. That is an artefact and not combustion.
`test_a_repeated_value_is_not_a_step` holds it.

**The 0–100 index, and why 0 is unattainable on purpose.**

```
IdleHealth = min(200, IdleRough × 25 >> 4)      /* 100 = the old engine */
```

- **100 is measured and frozen**: the engine that burned a catalytic converter
  through. **It can never be re-measured**, which is exactly why the anchor is
  taken now.
- **0 is defined as "no measurable step at all"**, which no engine reaches.
  **So the index never bottoms out** and always has room left to show an
  improvement — the failure mode of anchoring 0 to the smoothest *recording*
  is that a better engine clamps there and the channel goes dead again.
- **Above 100 is allowed** and means worse than this engine was at its worst.
  Clamped at 200.
- The pre-repair smooth readings land at **29–48** on this scale, so there is
  real room below them.

⚠ **`IDLE_ROUGH_100` is 64 counts = 2.00 rpm, and the measurement said 2.12.**
A decision, not a transcription: 100/64 is a multiply by 25 and a shift of 4
— a `uint8 × uint8` product, the one multiplication this part does in a single
cycle — where 100/68 is a division. The 6 % that costs is **inside the 13 %
the anchor itself scatters between 10 s windows**, and a scaling factor we
choose is one we may choose to be convenient (`docs/optimisation.md` §11). It
is written down in `tools/idledips.py` beside the constant.

⚠ **The index is only comparable at comparable temperature, and that is a
requirement rather than advice.** The grade is *not* monotonic through a
warm-up — `engine-health.md` has the curve, which falls and then climbs. The
practical consequence is mild, because a driver reads the number at the same
point of the same commute; the consequence for *this repository* is that a
before/after comparison must state the oil temperature or it says nothing.

### The start, and why its index ships empty

**The same 0–100 shape, and it cannot be anchored today.** The idle scale has
its bad end measured and its good end defined as zero. The start has **one
recording, and it is the bad one** — `18_coldstart_z1`, the only cold start
this car has ever had recorded, which per *The start itself* cranked for
1.24 s, fired at 451 rpm, **fell back to 311 and nearly died**, and caught on
the second attempt. There is no recording of a good start at all, and n = 1 at
one end of a scale fits nothing.

**So the firmware transmits the raw components from day one and leaves the
index byte reserved.** This is the whole point of the split: an index embeds
constants that will be revised, and a revision silently re-bases every
historical reading; **a raw number survives the revision.** Once a dozen good
starts have been recorded in the car, the constants are fitted, `StartHealth`
starts being published and the layout version in byte 7 goes up — **and the
frame layout does not change, so `mfd15` is touched once and not twice.**

The three raw components, all of them rpm and a clock:

| | definition | `18_coldstart_z1` |
|---|---|---|
| `StartCrank` | first 0x280 with rpm > 0 → first with rpm ≥ `START_FIRED_RPM` | **1.24 s** |
| `StartDip` | first-firing rpm − the lowest rpm in the 2 s after it | **140 rpm** (451 → 311) |
| `StartClt` | coolant at first firing | — |

⚠ **`START_FIRED_RPM` = 400 is a decision.** The one recording cranks at a
plateau of ~235 rpm and first fires at 451, so 400 separates them with margin
at both ends — but cranking speed moves with battery, oil and temperature, and
nothing here brackets how far. It is written as a decision, and the first few
good starts will say whether it wants moving.

⚠ **`StartClt` is not a nicety.** A hot restart is trivially easy and its
numbers mean nothing; without the temperature beside them, a summer afternoon
restart and a February morning are one column. It is also the one temperature
the display **cannot** take off the bus itself, because it is the value *at a
past instant* — which is precisely the test for whether a quantity belongs on
0x604 at all.

⚠ **Invalid is a value, and it needs saying.** `StartHealth` and the raw
fields read 255 / *invalid* when the first engine-speed sample seen after
power-up is already at or above `START_FIRED_RPM` — the key turned straight
through to crank, or the converter still finishing `persist_load()`. A start
the converter did not see the beginning of must not be published as a good
one.

**On stalling, which is the objection that matters.** A stall from dumping the
clutch is a *driver* event, not an engine fault, and **no frame this firmware
accepts carries a clutch switch**, so the converter cannot tell the two apart
in principle. What it can do is not look: the start window runs from first
crank movement to settled idle, with the standstill gate on, so a clutch dump
thirty seconds later is not in the window at all. A clutch dump *inside* the
window is possible, rare, and indistinguishable — **which is the general
property of both indices and is worth stating plainly: a single reading is
noise, and the instrument is the distribution over many mornings.** That
agrees with what the channel is wanted for.

### Where it goes: a new frame, 0x604 at 1 Hz, and there is room

**Decided, not forced.** Three reasons, in order:

- **All four existing frames are full.** 0x600, 0x601, 0x602 and 0x603 each
  carry eight bytes of eight. There is no spare byte to take.
- **0x603 is the one frame worth reorganising and it is the wrong frame.** It
  is transmitted only with JP1 fitted (`docs/frames.md`), and this channel is
  for a closed dashboard. A health number that needs the dashboard opened and
  a jumper fitted is a number nobody will ever look at. That gating is right
  for CAN diagnostics and exactly wrong for engine ones.
- **The slot schedule has room and the 25 ms rule is not threatened.**
  `TX_SLOTS_PER_SEC` is 40; slot 2 carries 0x602, slot 3 carries 0x603, slot
  22 is the EEPROM write, and the slots where `(slot & 3)` is 0 or 1 belong to
  the two 100 ms frames. **Slot 6 — 150 ms — is free**, and so are fourteen
  others. One more 1 Hz frame keeps *one frame per slot and never two*, and
  `test_never_two_frames_in_one_pass` goes on holding the rule unchanged.

⚠ **0x604 is NOT JP1-gated.** It is an ordinary frame like 0x600–0x602. Say so
where the layout is written down, because 0x603 sets the opposite precedent
three lines above it.

**The proposed layout, eight bytes of eight:**

| Byte | Name | Unit | Notes |
|---|---|---|---|
| 0 | `IdleHealth` | 0–200 | 100 = the engine before the repair. **255 = not converged** |
| 1 | `IdleRough` | **1/32 rpm** | the raw grade, 0–7.97. The index is derived from it and this is what survives a recalibration |
| 2 | `IdleSec` | s, saturating 255 | settled idle this start. Below `IDLE_CONVERGE_S` byte 0 reads 255 |
| 3 | `StartHealth` | 0–200 | **reserved — publishes 255 until the constants are fitted** |
| 4 | `StartCrank` | 0.05 s | saturating at 12.75 s |
| 5 | `StartDip` | rpm | below first-firing speed, saturating at 255 |
| 6 | `StartClt` | °C + 50 | coolant at first firing; 255 = no 0x288 seen |
| 7 | flags + layout version | | version in the top three bits, as 0x603 byte 4 does it |

**Why 1/32 rpm, and why it is not an arbitrary unit.** The EWMA accumulator
holds the grade in quarter-rpm shifted left by `ROUGH_SHIFT` = 8, so
`acc >> 5` *is* 1/32 rpm — **a pure shift, no multiply and no divide.** Range
to 7.97 rpm against a worst recorded 2.12, resolution 0.031 rpm against a
measurement that scatters by 0.10 rpm over 10 s. **Quantised well below its
own noise, which is the right place to stop.**

**Why the raw grade AND the index, when bytes are scarce.** Because the index
embeds `IDLE_ROUGH_100`, and the day that constant is revised every number
ever read off the dashboard changes meaning. The raw byte does not. It is the
same argument as `StartHealth` shipping empty, one step milder.

⚠ **`IdleSec` is the convergence gate and it is load-bearing.** The EWMA
settles over 256 firing events ≈ 9.7 s of idle, and it is **reset at every
engine start**. `--roughness --windows 60` shows what an unconverged read
looks like: the 3.2 s tail window of `18` reports a byte of 25 where the
converged value is 88. Publishing 255 until the idle has been settled long
enough is not tidiness — an unconverged grade reads *healthy*, which is the
one wrong answer that will be believed.

### What changes, and where

| file | change |
|---|---|
| `src/config.h` | `CAN_ID_TX_HEALTH 0x604`, `TX_SLOT_HEALTH 6`, the roughness constants carried over from `tools/idledips.py` **verbatim**, `START_FIRED_RPM`, `IDLE_CONVERGE_S`, each with its argument beside it |
| `src/compute.h/.c` | the grade and the start detector, and `compute_on_engine()` — a new core entry point, pure C, no `<xc.h>` |
| `src/main.c` | call `compute_on_engine()` on every `CAN_ID_ENGINE` frame, and the new slot |
| `src/txframes.h/.c` | `txframes_gather_health()` and `txframes_health()` |
| `docs/frames.md` | the 0x604 section, the slot table, and the not-JP1-gated note |
| `docs/can-decoding.md` | **the worked arithmetic**, under trap 6 — a real capture from raw frame to output byte, and its step histogram. The section already says what it has to contain; it is a requirement of this work and not a follow-up |
| `test/test_compute.c` | the grade against the fixtures, against the Python |
| `test/test_txframes.c` | the byte offsets, pinned against the TRI file as every other frame is |
| `test/test_scheduler.c` | the slot, under the one-frame-per-slot rule |
| `tools/idledips.py` | its docstring says today that nothing in `src/` uses it; that stops being true |
| `mfd15/tri/S-AQY.TRI` | the rows |
| `mfd15/docs/sensors.md` | the channel documented |
| `mfd15/README.md` | the frame list |

⚠ **`S-AQY.TRI` and `docs/frames.md` change in the same breath**, per
`CLAUDE.md`. A wrong offset there shows a plausible number rather than an
error.

⚠ **The `can-decoding.md` row is not documentation tidying and it is not
optional.** Every other signal on that page can be re-derived from a raw frame
by somebody who distrusts it. The grade cannot: it is four steps of integer
arithmetic — decode, step on change, deadband, scale — with a shift and a
chosen constant inside, and nothing published shows the chain end to end. A
number that can only be trusted rather than checked is the one kind this
repository has been burnt by repeatedly, and this one is worse than most
because it is a *statistic*: wrong arithmetic produces a plausible number
rather than an obviously broken one. **The worked example and the histogram
ship with the firmware, not after it.**

### The acceptance test, and it can be written before the drive

**`roughness()` in `tools/idledips.py` is the oracle**, exactly as
`tools/replay.py` is for the rest of the core. It already carries the
firmware's own arithmetic — an integer accumulator stepped by shifts and adds,
reported as `acc >> ROUGH_OUT_SHIFT` — so the C must reproduce its byte over
`09`, `11`, `12`, `17` and `18` **exactly**, not to within a tolerance. Both
are integer over the same samples and there is nothing to round.

Three traps, all of which would pass a careless test:

1. ⚠ **Step on change for the grade, and on arrival for the baseline.** Both
   EWMAs live in the same function and they are stepped by different things.
   `test_a_repeated_value_is_not_a_step` and `--segments` are the evidence.
2. ⚠ **The gate constants are shared with the torque rule and that is not a
   coincidence to be tidied away.** `GATE_SPEED_MMH` is `STANDSTILL_MMH` and
   `GATE_THROTTLE` is `THROTTLE_REST`. One definition in `config.h`, used by
   both. `test_the_gate_is_the_cheap_detectors_gate` proves the Python halves
   agree rather than asserting it.
3. ⚠ **The settle timer restarts on an excursion, it does not merely elapse.**
   `dips_cheap()`'s docstring has the measurement behind that — a fixed three
   seconds books a spurious event on a baseline still falling from driving
   speed, and **the fixtures do not show it** because their stops are too
   short to reach the delay. The idles this drive records are three to five
   minutes long and every one of them would show it.

**The capture from this drive becomes a fixture**, the same way question 4's
does, so the healthy grade is pinned and cannot regress silently.

### What else was considered from engine speed alone, and what happened to it

The question was asked deliberately — *is there anything else worth reporting
over the bus, purely from rpm* — and these are the answers, kept so the same
ground is not covered twice.

**Both of the ones worth building are now the design above** — the idle grade
and the start. They were arrived at here, and what is kept is the reasoning
that got them there rather than the proposal:

- **The idle had to stop being a count.** A threshold instrument on an engine
  that is about to be healthy is a row that reads zero for years, and the
  measurement in `engine-health.md` showed the threshold sitting just above
  the band that carries the information. The grade replaced it.
- **Depth as its own field did not survive.** An earlier draft carried a
  deepest-dip byte to separate a failed power stroke (33–57 rpm) from a
  partial burn (20–22). The grade already weights by depth — the physically
  meaningful quantity per *Why a misfire shows as a dip* is total missing
  work, which is linear in depth and is what a dead-banded mean sums — and
  the byte was better spent on `StartClt`. **The depth histogram is a
  question for a capture**, and `--depths` still answers it.
- **Start quality was the surprise.** It is the owner's oldest symptom, it is
  the one thing the idle instruments are blind to by construction
  (`SETTLE_S` = 3 and the idle gate), and **it is the one that needs no rough
  engine to calibrate against** — a hard start either happens or does not.
  That it cannot be *indexed* yet is a separate problem from whether it should
  be *measured*, which is why the raw fields ship and the index does not.

**Declined, and why:**

- **Anything instantaneous the display can take off the bus itself.** Engine
  speed, the idle speed the governor has settled on, throttle. The MFD15
  already reads 0x5A0 directly and needs no help with 0x280. **The converter's
  only reason to transmit a number is that the number had to be computed over
  time** — that is the rule, and it disposes of most of the obvious
  candidates.
- **Maximum engine speed since start / an over-rev latch.** Not engine health;
  it is a souvenir. And the firmware has no sourced redline for this engine,
  so the threshold would be invented.
- **Stall detection.** A stall is not rpm alone (it needs road speed to be
  distinguished from a normal switch-off), it is an event the driver
  experiences directly at the moment it happens, and it has not occurred once
  in the history in `docs/vehicle-history.md`. A channel for it would read
  zero for years.
- **Free-rev response — how fast engine speed rises off idle.** A genuinely
  good health indicator and the wrong home for it: it needs a controlled
  input, which makes it a test rather than a monitor. It belongs in a tool
  over a capture, next to `idledips.py`, not on the bus.
- **Per-cylinder structure on the bus.** Tested properly rather than waved
  away, and declined on arithmetic. `docs/engine-health.md`, *Is it one
  cylinder?*, finds a real period-4 line — 13–21× its local background — and
  then finds it **just as strongly in the smoothest recording this car has
  produced**, so the line itself separates nothing. The one statistic that
  does separate, the noise-corrected slot spread, manages **1.80× where the
  roughness grade manages 2.71× on the same recordings**. It costs a byte and
  more state than the grade and buys a weaker answer, so the byte stays with
  the grade.

  **The firmware cost, recorded so nobody re-derives it and gives up for the
  wrong reason.** The offline detrending is a 21-window moving average, which
  wants a 42-byte ring buffer — but firmware would not need it: subtracting
  the mean of each *consecutive group of four windows* removes the trend well
  enough at idle, where the governor's ramp is 0.43 rpm/s and a group spans
  150 ms, so 0.06 rpm. That is four accumulators and a mod-4 counter and no
  buffer at all. **What actually makes it awkward is the phase**: it slips at
  every missed window, 1.5 % of them, so the accumulation resets about every
  2.5 s and the statistic has to be a spread-per-run averaged over runs rather
  than one running figure.

  ⚠ **What it would uniquely catch is a future single-cylinder failure** — an
  injector silting up, a coil dying — where one slot runs away from the other
  three while the grade merely rises. **That is a diagnosis, not a trend**, and
  the division this frame is built on says diagnoses come out of a capture.
  `--cylinders` is where it lives, and it needs no firmware to do it.
- **Anything using the fuel counter, load or torque.** Out of scope by
  construction here; `b7 is modelled rather than measured` in
  `docs/frames.md` is why the torque side cannot see combustion anyway.

## What is deliberately NOT on this list

- **the oil sender unplug test.** Dropped: somebody under a car for a result
  that changes no number. `refuted.md` B10 and `can-decoding.md` question 4
  keep the reasoning.
- **`refuels` on the diagnostic frame.** Declined — it would be a change in
  two repositories for a channel nobody would be watching in a closed
  dashboard.
- **a full-throttle pull to settle the torque scale by itself.** Still not
  planned, and `can-decoding.md` parks it under *Never resolved but not
  required*.
