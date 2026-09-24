# The post-repair drive: what came back

**This is the analysis of the session `docs/next-drive.md` describes**, taken
with new plugs, leads, injectors and fuel filter fitted. It is the input to the
firmware spec that follows it, and like `engine-health.md` it is a holding
document: once the spec has consumed it, what is still true gets folded into
the permanent documents and this file is deleted.

Everything below was produced by the tools named beside it, over the files in
`test/fixtures/pending/`. Figures from VCDS screens were read off photographs
of those screens.

---

## The session, as run

| | |
|---|---|
| cold soak | about 19 h since the engine last ran (the plan asked for about 10). Mirror console **10.0 °C** before a door was opened |
| instruments | USBtin on the display's pair (display and converter out), VCDS on OBD, logging 003 and 014 |
| start | one crank, fired, idled two minutes |
| drive | 56 min engine running, **32.16 km**, **3.375 l** commanded (10.5 l/100 km). The driver's own words: *the hardest this car has ever been driven* |
| idles | cold (2 min), an extra one at oil 50–53 °C that was left early, middle in band at oil 60.8–65 °C, a stop at about 08:28, hot at oil 69.8–71.2 °C |
| pulls | held full throttle in **4th** (26.4 km/h per 1000 rpm) from about 2000 rpm to 5400–5760, several times; 5th and 2nd/3rd as well; peak 6001 rpm |
| after | step 18 screens, basic settings 046/034/037/070, 036, the final capture, switch-off |

**The thermometer failed at the hot end, and why is now known.** It is a
Berrcom JXB-178, a medical forehead thermometer. Its manual gives a surface
mode range of **0–60 °C** ([manuals.plus](https://manuals.plus/berrcom/non-contact-infrared-thermometer-jxb-178-manual)).
The oil filter and the expansion tank both read `HI`, so all it says about them
is that they were above 60 °C. The oil channel said 72.75 °C at that moment,
so the reading agrees with either scale and settles nothing. The cool-down
readings in section 2 went below the ceiling. **The next
thermometer has to be an industrial one, or a K-type thermocouple down the
dipstick tube**, which is what `can-decoding.md` question 10 already names as
the right tool.

| reading | cold, about 07:50–07:53 | hot, a few minutes after switch-off |
|---|---|---|
| oil filter | 10.7 °C | `HI` (> 60 °C) |
| top of the intake manifold, standing in for the unreachable sump | 10.8 °C | 50.1 °C |
| shaded ground | 10.3 °C | 13.4 °C |
| expansion tank | — | `HI` (> 60 °C) |

One reading per spot rather than three.

---

## 1. The coolant scale: `× 0.75 − 48` is CONFIRMED

| | VCDS group 001 | 0x288 b1 raw | `× 0.75 − 48` |
|---|---|---|---|
| cold soak | **12.0 °C** | 80 | **12.00 °C** |
| hot, step 18 | 100.5 °C | 198 (fan cycle 193–198) | 96.75–100.5 °C |
| hot, step 26a | 99.0 °C | 196 (same cycle) | 96.75–100.5 °C |

**Exact at the cold end and inside the cycle at the hot end, over 88 °C of
span.** All three VCDS values also land exactly on the 0.75 °C grid of the raw
byte (12.0 = 80, 99.0 = 196, 100.5 = 198). That indicates VCDS reads the same
quantity at the same resolution, so our decode is the ECU's own scale. **Q1 is
closed and nothing changes in `src/`.** Every temperature argument that leaned
on the coolant now has a measured reference under it.

## 2. The oil scale: still open, and now leaning towards the shipped slope

**Today's cold point:** oil raw **77** against a filter at 10.7 °C, ambient
10.0, coolant 12.0. Under the shipped formula that is 9.75 °C, so **the offset
is right at the cold end to within about a degree**, whichever slope is true.

**The two-soak test, poor but no longer empty.** `18_coldstart_z1` soaked at
coolant raw 86 and oil raw 81. Today's soak was coolant 80 and oil 77. The
coolant moved 6 counts (4.5 °C) and the oil moved **4**. A slope of 0.75 would
have moved the oil 6 counts; 1.1 would move it about 4. With ±1 count of
quantisation on each of the four readings the ratio spans 1.0 to 2.3. Between
two soaks only 4.5 °C apart that says almost nothing. A real test needs about
25 °C between them, which means a winter morning.

**The hot end: the thermometer's ceiling was 60 °C**, so the readings straight
after switch-off say only "above 60".

### A decision that was taken and then withdrawn

After the drive, the maintainer's first decision was to treat the highest oil
readings ever seen (raw 165–167) as 105–110 °C, which with today's cold point
gives `raw × 1.1 − 74`. **It was withdrawn within the hour**, on the
measurements below, and is kept here so it is not re-proposed without them.

### Three points during the cool-down

**The engine cooled with the bonnet open in the rain.** The ignition was
switched on (engine not running) for each reading, a capture was taken while
the thermometer was read, and the ignition was switched off again. Recordings:
`pending/21`–`23_oilcool_*`.

| clock | filter | other spot | oil raw | `× 0.75 − 48` | `× 1.1 − 74` | coolant |
|---|---|---|---|---|---|---|
| 09:51 | 48.8 | — | 125 | **45.75** | 63.5 | 72.75–73.5 |
| 09:54 | 47.3 | metal directly above the filter: 55.3 | 123–124 | **44.6** | 61.8 | 71.25–72.75 |
| 09:58 | 44.0 | bottom of the sump pan: about 38 | 121–122 | **43.1** | 59.6 | 68.25–69.0 |

- **The filter follows the shipped scale at all three points, within
  1–3 °C**, and falls alongside it. The filter is full of oil from the same
  circuit; `next-drive.md`'s *Where to aim* explains why it stays full.
- **The new slope needs the oil to be 15–20 °C hotter than both the filter
  and the pan it sits in.** Thin steel reading 22 °C below the oil inside it
  is implausible, even allowing for rain and the ground cooling the underside.
- **The one warm reading (55.3 °C) was taken on metal directly above the
  filter**, next to the block. The block's coolant was at about 72 °C, so
  that spot is heated by the block, not by the oil.
- ⚠ **These are still surface readings, not the oil.** Rain, evaporation and
  emissivity all push an IR reading down, so each is a lower bound. That cuts
  against the shipped scale, and it still leaves the new slope needing a 15 °C
  error on every oil-wetted surface.

**Status: `× 0.75 − 48` stays. Nothing changes in `src/` or `S-AQY.TRI`.**
Question 10 stays open, with these three points as the strongest evidence it
has had, and they point towards the formula already shipped. **Question 7 stays
open with it**, because the drag holds are then at 72.8–76.6 °C of oil, as
written.

**What settles it, and why more cool-down points will not:** as the engine
cools, the two scales converge on the cold point they share, so every later
reading discriminates less than the one before. The two scales are furthest
apart when the oil is hot. So what settles it is **the oil itself, hot**: a
K-type thermocouple down the dipstick tube, or an IR thermometer rated past
100 °C on the filter and the pan straight after a hard drive. Either is cheap.

## 3. The torque scale: the pulls happened, and the two ratings agree

**b7 at full throttle, held pulls, from `19_postfix_drive_z1`:**

| rpm (±150) | 4th, median | 4th, max | 5th, median |
|---|---|---|---|
| 2000 | 175 | 181 | — |
| **2400** | **185** | 191 | — |
| 3000 | 181 | 187 | 181 |
| 3500 | 187 | 194 | 187 |
| 4000 | 192 | 200 | 194 |
| 4500 | **198** | **206** | 198 |
| 5000 | 192 | 198 | 192 |
| **5200** | **191** | 194 | — |
| 5500 | 185 | 191 | — |
| 6000 | 175 | 175 | — |

`b7scan.py` reports **206 at 4402 rpm**. The shape is a plateau, and b7 is not
still climbing at the end of any burst: it peaks at 4000–4500 and falls away
above. **Relative load from group 014 is flat at 78–81 % from 2000 to
5500 rpm**, the 78.1 % of the earlier drive. The air is unchanged, and so is
the load. MAF rises to 86.9 g/s at 5000 and only 88.2 at 5500. That flattening
airflow is the engine running out of breath above 5000, which is what the
driver felt in 4th. It is a property of the engine's breathing and not of the
repair; the 85 kW rating is at 5200.

**The scale, taken from the two factory ratings with the drag line in bytes**
(`drag_b7 = 9.11 + 0.006514 × rpm`):

```
170 Nm @ 2400:   s = 170   / (185 − 24.74) = 1.061 Nm/bit
 85 kW @ 5200:   s = 156.1 / (191 − 42.98) = 1.055 Nm/bit
```

**The two ratings agree to 0.6 %.** Under the old premise (b7 = 255 is full
scale) they only agreed because both were nailed to 255. Here they are
independent measurements.

⚠ **This supersedes the 0.90–0.96 bracket in `docs/frames.md`, and the reason
is arithmetic, not new data.** That route divided **188 Nm** by the plateau,
and 188 is the rating plus the drag *in Nm at 0.74 Nm/bit*. The drag scales
with the scale. Held in bytes, as `config.h` holds it, the bracket moves up to
where the ratings put it.

**What it would change:** `TORQUE_CNM_PER_BIT` 74 → **106** (a decision
inside 1.055–1.061), with `DRAG_TORQUE_BASE_CNM` and `DRAG_TORQUE_SLOPE_Q16`
following it (9.11 × 106 = 966 cNm, 0.006514 × 106 × 65536 = 45252). The
drag line in bytes does not move. Both ceiling tests are rewritten to assert
that **the observed plateau reproduces the ratings**, not that 255 does. At
106 the display would show about 170 Nm at 2400 and 85.4 kW at 5200 on a pull
like today's.

⚠ **Two caveats, both stated rather than resolved:**

- **the intake temperature during the pulls was not logged.** Group 006 read
  28.5 °C at the hot idle after the drive, ambient was about 10 °C, and the
  rating's standard condition is not held by this project. b7 carries the
  charge normalisation, so a hot day will read lower and a frosty one higher.
  That is the physics, and it is not an error in the scale
- **step 1 of the decision tree, "is the engine well", is not cleanly
  satisfied.** See the engine-health section below. Everything wrong is a
  *low-load* fault: no misfire was counted during any pull, load and air match
  the earlier drive, and 046/034/036/037 are all OK. The judgement here is that
  the scale can be set from these pulls. The alternative is waiting for an idle
  fault that may be unrelated.

## 4. The refuelling rule: did not fire, and never came close

Replayed through `decode.c` and `compute.c` (harness outside the repo, core
unchanged):

| | |
|---|---|
| resets | **0** |
| longest run of at-rest samples above the rise | **0** of the 5 needed |
| raw level | **51 l for almost the whole drive**, with slosh dips to 43–49 while moving |
| settled level | 50–51 l, damped 48.6–50.9 |

**The float sat at its top stop**, as `next-drive.md` predicted for a brimmed
tank. Rises are clipped there, so this is the state in which a false reset is
least likely. **A floor, not a proof. Nothing changes.**

## 5. Range: sane across idles, stops and pulls

The basis ran **9.1–10.9 l/100 km**. Range sat at **449–566 km** and moved
smoothly with it. It never collapsed and never ran away. The trip average
finished at 10.5 l/100 km. **Nothing changes.**

## 6. The idle grade: the healthy end was not measured, because the idle is not healthy

**`idledips.py --roughness --windows 60`, constants untouched**, against the
frozen before-readings:

| state | oil | before | after |
|---|---|---|---|
| cold idle | 10–17 °C | 2.12 rpm, index 132 | 1.80–2.70 rpm, index 85–148 |
| mid idle | 61–65 °C | 2.12 rpm, index 112 | 1.36–2.31 rpm, index 62–123 |
| **hot idle** | **71–73 °C** | **0.96 rpm, index 48** | **2.04–2.65 rpm, index 92–150** |

`dips_cheap()` per idle: cold 17.0/min, the extra idle 18.0/min, middle
10.6/min, **hot 26.6/min**. Before the repair these were 12.1, 11.6 and 0.0.

**The grade did not improve anywhere, and at hot idle it is worse than before.**
At hot idle, 90 % of the grade comes from steps of 5–20 rpm. **Question 6 is
therefore neither yes nor no.** The prediction said a healthy engine would
supply the other end of the scale, and there is no healthy idle in this
recording to supply it. **Nothing gets built for 0x604 yet.**

⚠ **The grade and the ECU's own misfire counter disagree about the hot idle.**
Group 014 counted **zero** through the whole hot idle and through the minute
watched at step 18. The mid idles counted plenty (below). Before the repair
the two moved together, at p = 0.023. Either the hot-idle roughness is not
misfire, or the counter's steps of twelve miss single events. This recording
cannot separate the two, and it matters to 0x604 whichever it is.

## The start: n = 2

| | `18_coldstart_z1` (16.5 °C) | today (12 °C) |
|---|---|---|
| crank to first firing (≥ 400 rpm) | 1.24 s | **0.83 s** |
| first firing | 451 rpm | 450 rpm |
| fall-back after it | to 311 (−140) | to 331 (−118) |
| then | caught, 1,440 peak | caught, 1,522 peak |
| first 30 s of fuel | 937 µl/s | 1,063 µl/s (colder) |

**The same shape twice**: fire, fall back, catch. Twice suggests this is how
this engine starts rather than a symptom, though two is still a small number.
The crank was shorter today, from a colder soak.

**The shorter crank fits a rail that held its pressure overnight.**
`engine-health.md` records that when the regulator was changed the system held
no residual pressure, and a rail that bleeds down has to be refilled by the
pump before the engine can fire. Today it fired 0.41 s sooner after 19 hours
standing rather than 10. That is consistent with the new injectors sealing. It
is not a pressure measurement: n = 2, and cranking time also moves with the
battery and the temperature.

## The overrun: cuts from the first coast that could

`coastscan.py`: **157 coast windows, 72 with the injectors shut**. The coldest
coast that cut was at **63.8 °C of coolant**; the only colder one, 61.5 °C,
did not. The oil was still near 20 °C, because the coolant warms far faster.
The three deliberate early coasts from about 3,800 rpm (coolant 66.8–72 °C)
all cut, for 9–10 s each, 1.25–1.34 s after the lift. Fuel returned anywhere between
1,380 and 3,500 rpm depending on gear and speed. There is no single resume
speed, so the 1,700 of first gear and the 1,200 seen from the driver's seat
can both be right.

**The driver heard no burble at all, cold or hot**: *quiet immediately*. The
oldest symptom is gone and the ECU's behaviour explains why it can be gone. No
coast happened below 61 °C of coolant, so the ECU's behaviour on a genuinely
cold overrun is still not recorded.

## The 0x200 test: it is the tester

**0x200 appeared twice, 50 ms apart, at 09:06:38**, while VCDS was being
disconnected and reconnected at step 26, and at no other time in 241 s of
whole-bus capture. **Settled: 0x200 is VCDS establishing its session, not the
car.** Switch-off produced one burst of corrupted identifiers (0x000, 0x058,
0x078, a 29-bit one) within a millisecond, as the bus died. Those are not
frames.

---

## Engine health: better to drive, not cured, and one new finding

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

**By the fork in `next-drive.md`, with 034/036/037 all OK, this is a real
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
032 reading (step 30, a few hundred km on) is worth more now than it was when
it was planned.

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

## The two screens nobody explained

- **Group 100 `Čas od Motor Start` read 1843.2 s at step 18.** The engine had
  been running about 57 minutes without a stop, and the capture has no restart
  in it. What the field counts is not known. Nothing depends on it.
- **Group 006's altitude factor read −10.2 % with the engine off** and 3.1 %
  hot at idle. The engine-off value has no meaning (load read 99.5 % at the
  same moment). 3.1 % against the 0.0 % of the earlier session is small, and
  nothing here explains it.

---

## The MAF swap, the same afternoon: the rich trim was the MAF

**What was changed.** The car's MAF housing is an original Bosch
`0 280 218 002` (VW `06A 906 461 A`). The sensing insert in it was a
separately fitted `F 00C 2G2 032`, recorded as bought in 2018 with no invoice.
The whole meter was replaced with a genuine VW `06A 906 461 A`, housing and
insert together as supplied, and the old unit is kept. **Fitting it needed the
battery disconnected, so 032 started again from 0.0 / 0.0.** Recordings:
`pending/24_mafswap_drive_z1.txt` (filtered, about 30 min: a warm restart,
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

**The misfire counter did NOT go away, and at hot idle it is now worse.**

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

**So the rich trim and the misfires/puffs are two faults, and only the first
is solved.** Plugs, leads, injectors, fuel filter, regulator and now the MAF
are all new, and compression is even. What is left for the second is not
decided here. The cheap next reads are blocks 022/023 (knock retard per
cylinder) at a warm idle, and the dip-against-counter correlation that
`engine-health.md` ran on the cold start, repeated on `24`.

## For the spec: what changes, and what does not

| item | status | change |
|---|---|---|
| Q1 coolant scale | **confirmed** | none |
| Q2 oil scale | **open**; three cool-down points favour the shipped slope; the 1.1 decision was withdrawn | none; settled later by a thermocouple or a >100 °C thermometer on hot oil |
| Q3 torque scale | **measured**, one caveat | `TORQUE_CNM_PER_BIT` 74 → 106, drag constants follow, ceiling tests rewritten, `frames.md`'s bracket corrected |
| Q4 refuelling rule | holds, floor only | none |
| Q5 range | holds | none |
| Q6 idle/start channel 0x604 | **not answerable yet**: no healthy idle recorded | none; revisit after the fuelling is fixed |
| fuel counter vs pump | **settled by the MAF swap**: the counter was right | none |
| fixtures | recorded, pending | promote `pending/` into the corpus and update the seven tests it breaks, as a change of their own |
| `next-drive.md` | followed | delete once the spec has taken what it needs; step 30 (032 again) moves into whatever replaces it |

**Owed by the owner, none of it urgent:** 032 again after a few hundred km on
the new MAF, to see the adaptation settle; blocks 022/023 at a warm idle, for
the misfire question. The oil change and the oxygen sensors were set aside by
the owner once the MAF explained the trim.
