# Refuted hypotheses

Things that were believed in this project — some of them written down as fact,
some of them acted on — and then turned out to be wrong. Each entry says what
was believed, what refuted it, and what it cost.

**Why keep this.** A refuted idea is not worthless: it is a plausible idea, and
plausible ideas come back. Without a record, the second person to have one has
to spend the same afternoon disproving it, or worse, does not and acts on it.
Several of the entries below are things that *look* right and would be
reintroduced by anyone reasoning from first principles.

**Scope.** This covers all three repositories — `canfuel` (firmware), `kicad`
(the board) and `mfd15` (the display configuration). It lives here because
`canfuel` is the busiest of the three; the other two point at it.

**What does not belong here.** Open questions — things not yet settled either
way — live in `can-decoding.md`. This file is only for things that were settled
*against*. If an entry below is ever un-refuted by new evidence, say so in it
rather than deleting it.

---

## A. Reading the datasheet

The most reusable section, because these are not mistakes about this project —
they are mistakes about how to read a Microchip datasheet.

### A1. "The ECAN module is chapter 22"

**Believed:** section numbers of the form §22.x throughout the firmware notes.
**Refuted by:** DS39977C itself — ECAN is **chapter 27**. §22 is a chapter
number from an older PIC18 CAN datasheet and does not carry over.
**Cost:** every citation in an early revision of `CLAUDE.md` pointed at the
wrong chapter. Nothing was built wrong, but no citation could be re-checked,
which is the entire point of a citation.

### A2. "Setting CANMX moves CANTX/CANRX to the alternate pins"

**Believed:** on the authority of DS39977C §27.1, whose opening paragraph says
the pins "can be placed on alternate I/O pins by *setting* the CANMX
Configuration bit".
**Refuted by:** Register 28-5, which defines bit 0 as `1` = RB2/RB3 and `0` =
RC6/RC7, and the pin-table footnote, which agrees with the register. Two
independent parts of the document against one sentence of prose. `CanSwitch.X`
in the sibling `can` repository is a third witness: its comment on `PORTC`
reads "ECAN TX and RX pins are located on RC6 and RC7".
**Cost:** nothing, because it was caught. It would have cost a board — this is
the single most expensive bit in the project, and with the escape header gone
(D1) fixing it means soldering to the underside of the PDIP socket.
**Lesson, now a rule in `CLAUDE.md`:** register tables outrank prose.

### A3. "Table 3-1 gives the oscillator mode for a given frequency"

**Believed:** reasonably, since that is what the table is for.
**Refuted by:** the table's own frequency column, which is misaligned against
its mode column by one row from HS1 downwards. Register 28-2 gives the real
mapping: `0011` = HS1 (4–16 MHz), `0010` = HS2 (16–25 MHz).
**Cost:** none. Use Register 28-2.

### A4. "The A/D is ten bits, so VDD = 1.024 × 1023 / code"

**Believed:** and written into both `CLAUDE.md` and `docs/frames.md`. It is the
correct formula — for a different PIC.
**Refuted by:** DS39977C Table 31-25 parameter A01, `NR Resolution ... 12 bit`,
and §23.5, "The A/D conversion requires 14 TAD per 12-bit conversion".
**Cost:** would have reported **four times the real supply voltage**. 20 V on
the display is exactly the kind of wrong that gets blamed on the wiring, and
somebody would have gone looking for it with a multimeter.

### A5. "Parameter D122 gives the limits on the EEPROM write time"

**Believed:** on the authority of §8.4, which says the write time "will vary
with voltage and temperature, as well as from chip-to-chip. Please refer to
Parameter D122 ... for **exact limits**".
**Refuted by:** D122, which reads `-- 4 --` ms. A typical with no minimum and
no maximum. The datasheet refers the reader to a bound it does not contain.
**Cost:** none yet, and it is why `docs/timing.md` treats the 48 ms record
write as what to expect rather than what to design against.

### A6. "`piclib/dao.c` omits the GIE bracket the datasheet's Required Sequence asks for"

**Believed:** and written into `CLAUDE.md` as a defect in a sibling repository.
**Refuted by:** the caller. `dao_saveDataItem()` opens with `di()` and closes
with `ei()` — exactly that bracket, around a superset of the sequence. The
claim came from reading the inner `dao_writeByte()` in isolation.
**Cost:** an unfair accusation, caught before it could justify writing
something different here for no reason.
**Lesson:** check the caller before writing down that somebody else's code got
it wrong.

---

## B. Decoding the car

### B0. "The car has a fuel consumption signal on a wire"

**The first hypothesis in the project, and its refutation is why the project
exists.** Numbered B0 rather than appended at the end so that it sits where it
belongs chronologically, and so the entries other repositories already cite
keep their numbers.

**Believed:** that the ECU feeds the instrument cluster a consumption signal
over a dedicated wire — an injector-duty or pulse output — the way older VWs
with the MFA trip computer do. If so, the whole job would have been tapping
that wire and scaling it: no CAN decoding, no acceptance filters, no
converter firmware worth the name.

**Refuted in two steps, and the second one is what mattered.**

1. **From the web** — wiring documentation for the platform. On PQ34 with the
   AQY there is no consumption wire. The powertrain is fully CAN and
   the figure the cluster displays is computed, not carried.
2. **Then confirmed on the bus.** A CAN sniff showed the ECU emitting
   consumption after all, just not the way the hypothesis expected: frame
   **0x480, bytes 2–3, little endian, masked with 0x7FFF, is a free-running
   fuel counter in microlitres**, and it is there in every recording.

That second step turned a dead end into a design. Everything downstream — the
accumulators, FuelAvg as a ratio of microlitres to metres, the whole reason the
core is integer-only and never needs a conversion factor — follows from that
one signal existing and being exact.

**Cost:** none. It cost the afternoon that found the answer, and it settled the
architecture: the device had to be a CAN node, which is what made the board, the
transceiver, the filters and the ECAN driver necessary at all.

**Worth knowing if it comes back:** the fact that older VWs really do have that
wire is exactly what makes this hypothesis plausible. It is not a silly idea —
it is a correct idea about a different car.

### B1. "The speed validity gate is `b1 == 0x40`"

**Believed:** and written into the implementation plan as step 3 of phase 1.
**Refuted by:** the logs. `b1` is a bit field, not a value; the correct rule is
`(b1 & 0x40) && !(b1 & 0x03)`.
**Cost:** the equality throws away **two thirds of the speed samples**, which
corrupts both FuelAvg and Range. Caught in phase 0, before any code depended on
it. It is trap 1 in `can-decoding.md`.

### B2. "0x5A0 byte 0 is the tank level"

**Believed:** in an early revision of the sensor table.
**Refuted by:** the data — it sits at 127–128 at rest and moves either side
while driving, which is an accelerometer around a zero offset, not a tank.
**Cost:** none; corrected before the TRI file was written. The tank is 0x320
b2, masked with 0x7F.

### B3. "0x420 b3 might be intake air temperature"

**Believed:** genuinely open, with `07_accel` recorded
specifically to settle it and coming out inconclusive.
**Refuted by:** reading all seven fixtures in the order the coolant says they
were recorded. It is a warm-up curve lagging the coolant, 21 → 65 °C while the
coolant goes 68 → 99 °C; it is *highest* in `03_drive`, the one log with air
actually moving through the engine, where an intake temperature would fall; and
it reads 255 with the ignition on and the engine off, which a thermistor the
ECU can read at any time would not.
**Cost:** none — the firmware had always treated it as oil. It is now a finding
rather than an assumption.

### B4. "0x5D8 b0 is the instrument cluster's trip counter"

**Believed:** the candidate for a cluster-driven trip reset, with
`06_trip_reset.txt` recorded to confirm it. The log then sat unanalysed for
months.
**Refuted by:** analysing it. **All eight bytes of 0x5D8 are constant for the
entire 135 s recording** — `21 05 00 00 00 00 00 00`. So is 0x5D0. Sweeping
every byte of all fourteen broadcast identifiers for anything that grows and
then falls finds only the fuel counter and the oil warming up.
**Caveat kept deliberately:** the recording covers 124.6 m, so a trip odometer
in units of 0.1 km would tick once and a scan could not tell that from noise.
This kills the candidate, not the possibility.
**Cost:** none, because C2 had already removed the need for it.

### B5. "The specification's starting counter for `07_accel` disagrees with the file"

**Believed:** an open question for months — the specification quotes 13247, the
file starts at 12870, and only the end agreed.
**Refuted by:** looking. The counter reaches 13247 at 0x480 frame #23 of 290,
1.14 s into the recording, and the fuel burnt before that is **377 µl, which is
exactly the discrepancy**. The specification was computed from 1.14 s in.
**Cost:** none. A discrepancy that never existed, left open for want of ten
minutes.

### B6. "0x280 b7 is scaled so that full scale is the AQY's 172 Nm"

**Believed:** and used, giving 0.67 Nm/bit.
**Refuted by:** the fixture sitting next to it. In `05_rev3000`, at 2940 rpm in
neutral, the crank is putting out nothing and b7 still reads 37 — so b7 is
*indicated* torque, and its full scale is the maximum **indicated** torque, the
rated crank figure plus drag. Scaling to the crank maximum and then subtracting
drag counts the friction twice.
**Cost:** the display could never have shown the 85 kW the car is sold with. It
topped out at 76.5 kW at 5200 rpm and 147 Nm, at any throttle opening, and
**nothing tested that** — which is the part worth remembering. Two tests in
`test_compute.c` now pin the ceiling.

### B7. "Bit 15 of the fuel counter is constantly 1"

**Believed:** stated as measured fact in `mfd15/docs/sensors.md`.
**Refuted by:** the logs. It is **zero from ignition on until the first wrap,
then permanently one**.
**Cost:** none, because the 0x7FFF mask drops it either way — but only by luck.
Anyone using it as a validity flag, which "constantly 1" invites, would have
been wrong for the first few minutes of every drive. It is trap 3 in
`can-decoding.md`.

### B9. "b7 reaches 133 at throttle 38 while driving, so the throttle cannot gate on its own"

**Believed:** written into `config.h`, `docs/frames.md`, `CLAUDE.md` and
`test/fixtures/README.md`, and it is the whole reason the torque gate was an
AND — zero only when the car was standing still *and* the pedal was released.

**Refuted by:** looking at the frame the maximum came from. It is one frame of
`17_drive_property_z1`, at 4522 rpm, during a gearchange, and 0x1A0 was not
reporting a valid speed in it. Bucketed by engine speed, mean b7 at throttle 38
is 14–17 everywhere above 1000 rpm, which is *below* the drag line and displays
zero anyway; only the idle bucket sits above it, at 27.6. **A maximum over a
log is not a state the car sits in** — that is the general lesson and it is
cheap to repeat.

**Cost:** two wrong states on the display, both reported off the car rather
than caught here. Revving in neutral at a standstill showed a number, and so
did the last few seconds of every roll to a stop, where the idle governor lifts
b7 back above the drag line while the pedal never moves. `docs/frames.md` has
the worked stop and the fix, which is one character: the AND is an OR.

**Un-refuting it would take** a state where the pedal is at rest, the car is
moving, and the engine is genuinely driving the wheels — sustained, not a
transient. Cruise control would be one; this car has none.

### B10. "0x420 b3 might be oil pressure, not oil temperature"

**Believed:** never, which is the interesting part — **it was never
considered.** Question 4 asked *"is 0x420 b3 oil or IAT?"*, answered it, and
closed. A binary question gets a binary answer and the third option is not
wrong, it is absent. Raised by the maintainer on finding that this engine is
said to carry an oil *pressure* switch and no oil temperature sender at all,
which makes a pressure channel the obvious reading.

**Refuted by:** `18_coldstart_z1` and the four free-revving holds, three ways,
all measured and none needing a decode to be right first — direction of travel
survives any monotonic scale.

1. **It does not move when the engine starts.** Oil pressure goes from zero to
   several bar within one revolution. Across the start the raw byte is 81
   before cranking, 81 at 451 rpm, 81 at 1439 rpm, and **still 81 eighty
   seconds later**. It first moves at about 160 s.
2. **It is not zero with the engine stopped.** It holds a steady 81 for the
   41 s of ignition-on before the engine fires, and `08_ign_only_z1` holds a
   steady 133 for its whole twenty seconds. A stopped engine has no oil
   pressure.
3. **It ratchets instead of tracking.** Across holds at 1492, 1792, 2342 and
   2892 rpm it goes 161 → 162 → 163 → 165 → 167, one count per 25 s hold,
   monotonically, **and never comes back down between holds** — where the
   revs did come down. Pressure roughly doubles over that rpm range and is
   reversible; this moved 3.7 % and is not.

**It is also not a number computed from the coolant**, which is the other
thing a car with no sender might broadcast. In hold `15_rev2372_z1` the
coolant **fell five counts while this channel rose two**. A value derived from
the coolant cannot move against it.

**What survives:** something with real thermal mass, heated by the engine,
responding to load rather than to engine speed, and slow enough to take
minutes. That is oil temperature, whatever supplies it.

**And it is a sensor rather than a computed number**, which was open when this
entry was written and is now measured: every step the byte ever takes is ±1
count, 85 up and 58 down, including twelve downward steps during a warm-up it
was unambiguously climbing through. That is one-LSB dither around a moving
value — an analogue sensor and its converter — and not arithmetic, which does
not rattle in both directions while its inputs move one way. `can-decoding.md`
question 4 has it.

⚠ **What is NOT settled, and is a question about the car rather than about the
bus:** whether that sensor is the sump's own G266 or something else. **This
project does not take car facts off the web** — they are settled by
measurement here. It matters less than it did, because "there is no sensor,
so the number is modelled" is now excluded either way.

**Cost:** none. The conclusion question 4 reached is unchanged and the
firmware needed no edit. What it cost before it was asked is a closed question
that had only ever been tested against one alternative — **a question guards
the answers it was written from**, which is the same lesson as C8.

---

### B11. "0x420 b1 and b2 are zero, so the car has no ambient temperature sensor"

**Believed:** written as a flat statement of fact in `can-decoding.md`'s list
of things that were searched for and not found, and repeated from there into
`frames.md` and `src/config.h` — three places, one of them a code comment.

**Refuted by:** a photograph. The car displays the outside temperature next to
the clock in the rear-view mirror console, reading **20.5 °C** on a September
afternoon. The maintainer adds that it tracks the real outside temperature
reliably and has never shown anything like an oil temperature, so it is
ambient and not some other channel misread.

**The bytes were read correctly and the conclusion did not follow.** `0x420`
b1 and b2 really are zero. What that establishes is that **the ambient
temperature is not on those bytes** — nothing whatever about what is fitted to
the car. It reaches that display by some other route: a different frame, or a
wire that never touches this bus at all.

⚠ **ABSENCE ON A BUS IS ABSENCE ON A BUS.** That is the reusable half and it
is worth more than the entry. This repository decodes a vehicle by watching
seven identifiers on one of its networks, and **every "the car does not have
X" conclusion drawn that way is really "X is not on the frames we watch"**.
The two are not the same sentence and this one was written as though they
were.

**Cost:** nothing functional — no firmware consumes an ambient temperature and
none was ever going to. What it cost is a wrong fact repeated in three files
for months, and the risk that somebody would have reasoned from it.

**What it gains:** a fourth independent reading of the cold soak, free and in
real degrees, from a sensor and a path that share nothing with VCDS or with
either CAN channel. The post-repair drive took it: 10.0 °C, beside 12.0 °C of
coolant from VCDS after a 19-hour soak.

⚠ **Do not go hunting for the ambient channel on the bus.** Nothing in this
firmware or on the MFD15 consumes one, so a decoded field would be dead
weight — the same rule that keeps 0x5A0 out of the acceptance filters.

---

### B8. "The fuel counter wraps at 32767"

**Believed:** in the same place.
**Refuted by:** the arithmetic. It wraps at **32768**, so the modulus is 32768
and the delta is `(new − old) mod 32768`.
**Cost:** an off-by-one in every delta across a wrap, roughly once every 33 ml
of fuel. The original measurement text is kept in `sensors.md` with the
correction beside it.

---

## C. The firmware

### C1. "`piclib` will be added as a submodule"

**Believed:** and written into `CLAUDE.md` as a plan.
**Refuted by:** reading it while writing `hal_can.c`. `can.c` is Mode 0 only —
one transmit buffer, two receive buffers, six filters — and this needs an
eight-deep FIFO, so Mode 2, which it has no notion of. (At the time it also
needed a seventh filter; 0x5A0 was dropped and six now fit, but
two receive buffers still do not hold 3.58 frames per 10 ms.) Its API
is a `CanHeader` of message type and node ID belonging to a house lighting
protocol, not "send this identifier". `can_initRcPortsForCan()` is hard-wired
to the wrong pin pair for this board. `can.h` *defines* two variables in the
header rather than declaring them.
**Cost:** none — the reversal happened before anything depended on it. This
repository has no submodules, and `piclib` remains the best available reference
for these registers on this silicon, which is a different thing from being a
dependency.

### C2. "The trip average is reset from the instrument cluster's trip reset"

**Believed:** enough to design two implementations behind an `#ifdef` —
`RESET_SRC_CLUSTER` watching a cluster counter, and `RESET_SRC_MFD` watching
frame 0x702, the latter needing a paid Can Switching licence.
**Refuted by:** a better idea rather than by evidence — resetting on refuelling
instead, which needs no sniff, no licence and no undecoded byte, and behaves
like the "since refuelling" average in modern cars. See `refuel-reset.md`.
**Cost:** none, and it saved a licence purchase. B4 later showed the cluster
route would have needed more work than expected anyway.

### C3. "Range can read the tank level straight off the bus"

**Believed:** and shipped that way in the phase 1 core, while the *displayed*
tank level was damped over 60 s from the start.
**Refuted by:** `07_accel`, where the raw value swings across 10 L during a
pull-away. That is a range appearing and disappearing across **111 km several
times a second**, while the level gauge next to it sat still.
**Cost:** caught before any hardware ran. `compute_range_km()` now takes no
`decode_state_t` at all, so it cannot regress.

### C4. "Leaving RB2 low at start-up is cosmetic"

**Believed:** implicitly — `ports_init()` wrote `LATB = 0x00` along with every
other unused pin.
**Refuted by:** DS20005167C. RB2/CANTX drives the MCP2562's `TXD`, which is
**active low**, so a driven-low TXD is a request to hold the bus dominant —
from power-up until `hal_can_init()` runs several milliseconds later, with a
whole EEPROM ring scan in between. The transceiver's own permanent-dominant
protection (§1.5) only intervenes after tPDT, 1.25 ms typical, which at
500 kbps is over six hundred bit times.
**Cost:** would have jammed the car's powertrain bus at every power-up.
`LATB` is `0x04` now.

### C5. "piclib's bit timing split is fine at 500 kbps"

**Believed:** inherited without checking — Sync 1 + Prop 4 + Phase1 8 +
Phase2 3, sampling at 81.25 %.
**Refuted by:** doing the round-trip arithmetic. `Prop_Seg ≥ 2 × (t_transceiver
+ t_cable)` with DS20005167C's 125 ns and 110 ns gives **3.0 m of node
separation** at Prop_Seg = 500 ns. That is not a comfortable budget for a bus
running from the engine bay to the dashboard, and it says nothing of the
unterminated 1.4 m stub this board hangs on.
**Cost:** caught before the first bus contact. The split is now
1 + 7 + 5 + 3 with SJW 2, which buys 40.5 m, and the sample point did not move.

### C6. "`static inline` in a header is free"

**Believed:** `decode_rpm()` was one.
**Refuted by:** XC8, which emits it into every translation unit that includes
the header and then warns three times that it is never called.
**Cost:** three warnings and a puzzled ten minutes. It is an ordinary function
in `decode.c` now, and the hex is byte-for-byte the same size — the compiler
was inlining it anyway.

### C7. "Loopback exercises everything except the wire"

**Believed:** written into `hal_can.h` and into `docs/install.md`, which
claimed the loopback step tests "the bit timing, all six acceptance filters,
the eight-deep FIFO, the access-bank window, `txframes` and `decode`" — and
gave **steady `LED_CAN`** as the pass, with dark meaning "the transmit path or
the FIFO is not working".

**Refuted by:** reading the code before running the step for the first time.
Loopback delivers only the frames we send ourselves, which are 0x600–0x603.
Those match **none** of the six acceptance filters — the filters hold the
car's identifiers — so they are rejected before reaching the FIFO. Nothing is
decoded, no 0x480 arrives, `compute_data_live()` stays false, and `LED_CAN` is
therefore **dark**. Steady is not merely unlikely in that mode; it is
unreachable.

**Cost:** none yet, and it was close. The step had never been run. The
documented pass condition was impossible and the documented failure condition
was the pass, so the first run would have reported a working board as a broken
transmit path — and the obvious next move, suspecting `hal_can_send()` or the
FIFO, would have been an afternoon in the wrong place.

**What loopback does prove** is that the module accepted its configuration and
reached the requested mode, which is worth having and is what the 5 Hz blink
denies. The receive path, the FIFO and the filters need frames from outside;
`install.md` step 7 is where they are tested, and this is a large part of why
that step exists.

### C8. "A standing car with the throttle shut is the only state that must show zero torque"

**Believed:** as a fixed requirement, in capitals, in five files — and the
requirement was right as far as it went. What was wrong is *only*.

**Refuted by:** the car, on the first drive with the converter live. Two states
the AND left showing a number:

- **revving in neutral at a standstill.** The crank drives nothing there, which
  is exactly what makes the four free-revving holds a calibration rather than
  data.
- **the last few seconds of every roll to a stop.** High in the deceleration
  the ECU cuts fuel, b7 falls below the drag line and the answer is zero; once
  engine speed drops back onto the idle governor, b7 climbs 7 → 27 with the
  pedal untouched and up to 9.5 Nm reached the display, then snapped to zero at
  the standstill.

Both are the same fault — **the drag line is systematically low at idle**, 14
against a measured 25 in b7 at 800 rpm — and the fix is to assert idle for
every state the engine idles in rather than only the parked one.

**Cost:** nothing permanent, and it was visible from the driver's seat within a
minute. Worth noting is what did *not* catch it: `test_compute.c` had six tests
guarding the gate, `test_txframes.c` two more end to end off real idle logs,
and all eight were about a *parked* car, because that was the belief. **A test
suite guards the rule it was written from.**

**What it does cost, deliberately:** pulling away reads zero until the car
moves, a median of 0.7 s after the pedal leaves rest, so real torque against a
slipping clutch is not shown for that time. The alternative — gating on the
throttle alone — leaves a revving parked car showing a number, which is the
more visible wrong.

### C10. "A level persistently higher than the baseline means somebody refuelled"

**Believed:** as the whole of the refuelling rule, and written into
`refuel-reset.md` as *"is the level suddenly and persistently higher than it
was"*. Five consecutive at-rest seconds more than 3 L up, at-rest meaning
under 1 km/h.

**Refuted by:** the car, at a Beetle meet. Parked on grass, and a **250 km
trip was cleared on the way out** — noticed an hour later only because the
average moved faster than the mileage could explain.

**The rule tested a STATE where it had to test an EVENT.** "Higher than some
older figure" is true of a refuelling and equally true of a car standing at an
angle, or one whose float is still swinging from the ground it just crossed.
Three measurements, all from fixtures that were already in the repository:

- **the at-rest gate admitted a moving car.** A standing car sends
  0.005 km/h and the next value that appears anywhere is 0.2 km/h, so the band
  up to 1 km/h is a car creeping. `17_drive_property_z1` spends **2,755 of its
  47,093 speed samples** in it — 5.9 % of the log.
- **the amplitude was always there.** In that same log the raw level spans
  **5 L with the car fully stopped**, against a threshold of 3.
- **nothing required the float to have settled.** The displayed level is
  damped over TANK_DAMP_SAMPLES because the raw reading is unusable; the
  refuelling rule read it raw.

**What was actually holding the rule up** was the consecutive-sample counter
and nothing else. Replayed over every fixture it never fires, and the
longest run above the threshold is **1 of the 5** required. That is not a
margin, it is a coincidence of how long tarmac stops last.

**Cost:** one destroyed 250 km trip and its average. Nothing persistent, and
nothing that a bench could have caught — see below.

**Fixed by** arming the rule only after `REFUEL_ARM_S` at rest, during which
the reference takes up whatever level is found at this stop, so an arrival
cannot fire it; tightening the gate to the measured 0.1 km/h; and 3 L to 4 L.

⚠ **ONE CASE REMAINS AND IT IS NOT A TUNING PROBLEM.** A car parked on a slope
and then key-cycled is *indistinguishable* from one that had fuel added while
it stood there: both are "the level is higher than the last stored reference,
at rest, at power-up", and there is no third fact available. The firmware
resolves it in favour of detecting the fill, because refuelling with the
ignition off is how refuelling normally happens. Do not re-derive this as a
bug.

**What did not catch it, and it is a new blind spot rather than the old
one:** every fixture containing a moving car has **0–10 L in the tank**, and
the only one with a real level never moves. The float has never been recorded
in motion anywhere but the bottom of its travel, on a sender known to be
nonlinear. **A measurement taken in one corner of the state space is a
measurement about that corner**, which is the same lesson as B10 and C8
arriving by a third road.

*Later:* `19` and `24` added the opposite corner — a brimmed tank on the move,
at the float's top stop — and the rule did not fire. The middle of the travel,
where this entry's trip was lost, is still unrecorded.

---

### C9. "The rolling Range basis is a property of the trip, so a reset clears it"

**Believed:** written down in as many words in `compute_reset_trip()`, and
inherited from the segment ring that came before the filter — clearing the
ring was the only thing that *could* be done with thirty slots of a journey
that no longer existed. The filter kept the habit without re-deriving it. The
ignition cycle was the same belief by omission: `basis_q4` was never added to
`persist_record_t`, while `total_mm` was.

**Refuted by:** the car, on a long drive. Range read about 400 km on the road,
halved on pulling away from a filling station, and climbed back over the next
fifty kilometres of ordinary driving.

The mechanism needs all three of these and no more:

1. **a zero basis meant "no history", and the filter took the next completed
   kilometre as its whole value** — no damping, one kilometre defining the
   number;
2. **both things that zeroed it happen at a filling station** — a refuelling,
   and an ignition cycle restoring a long `total_mm` beside an empty filter;
3. **the first kilometre off a forecourt is the worst kilometre there is.**
   `17_drive_property_z1` is 880 m of that driving at **23.2 l/100 km**
   against 11-ish on the road, because fuel burned standing still accumulates
   into the segment while the segment's distance does not move.

With ~46 l aboard and a road basis of 11.5, the arithmetic gives 400 km → 198
km → 323 km after twenty further kilometres → 396 km after forty. That is the
report, with the tank level as the only free parameter.

**The refutation is of the premise, not of the number.** The trip counter is a
property of the trip. The rolling basis is a property of *how the car is being
driven*, and neither filling the tank nor turning the key changes that. The
same car with the same driver on the same road burns the same fuel a minute
after a fill-up as a minute before.

**Cost:** four drives' worth of a gauge that was wrong by a factor of two for
an hour after every fill-up, and nothing else — no hardware, no wire. The
basis now opens at the conservative default, is seeded from the persisted trip
average at start-up, and survives a reset; the undamped seeding branch and the
`RANGE_MIN_MM` display gate are both gone, which makes `compute_range_km()`
smaller than it was.

⚠ **The tempting fix is the wrong one and is refuted with it: "make the window
shorter, say five kilometres".** The time constant is sixteen kilometres and
was never the problem — the restart was. Shortening it would have *tripled*
the weight of the very kilometre that caused this. The complaint was
sensitivity and the cause was a filter being restarted from a single sample;
those look identical from the driver's seat.

**What did not catch it:** every module was individually correct.
`test_persist.c` round-trips the record faithfully, `test_compute.c` had four
tests on the basis, and none of them crossed the seam where the record meets
`compute_restore()`. The same lesson as the `persist_save()` entry in
`CLAUDE.md` — **an assumed input cannot see a fault upstream of it** — and the
replacement test now runs compute → persist → compute rather than checking
`compute_restore()` against a record it built itself.

---

## D. The board

### D1. "An escape header bringing out the unused pins is cheap insurance"

**Believed:** enough to fit J4, a 2×8 header carrying all fourteen unused I/O
pins plus power, on the grounds that it rescues a design error.
**Refuted by:** routing the board with and without it. Same router, same
placement, same order:

| | with J4 | without J4 |
|---|---|---|
| connections to route | 39 | 25 |
| **left unroutable** | **8** | **0** |
| DRC | incomplete | **0 violations** |

**Five of the eight failures were not escape signals** — both status LEDs and
the whole ICSP header. A header that existed to rescue a design error was
stopping the chip from being programmed.
**Cost:** paid in full and recovered. Patching now goes
onto the PDIP socket pins from underneath, which are through-hole and
reachable, so the escape route survives without the header. The freed column
was inside the 6 mm keep-out circle of DS39977C §2.3, so the MCLR cluster moved
into it and its worst far corner went from 10.68 mm to 8.67 mm.
**Do not put it back.**

### D2. "The board needs an enclosure"

**Believed:** and a candidate was priced.
**Refuted by:** looking at where it goes. Everything around the board in the
vent is plastic, so there is nothing to short against; the vent is closed off
by a flap, so no airflow, no meaningful dust and no water; and the board is
invisible either way. A box bought nothing but mechanical retention, which
standoffs buy better. The space could not be measured properly anyway, because
the MFD15 is in the way.
**Do not reopen it.**

### D3. "The board needs a 12 V branch"

**Believed:** in the early requirements.
**Refuted by:** the MFD15 supplying 5 V directly on plug C, measured at 5.01 V
at C6/C12.
**Cost:** none, and it removed a regulator, reverse-polarity protection and a
TVS from the design. What replaced it is a 200 mA fuse in the loom, because a
short on the converter is now a short across the display's 5 V rail.

### D4. "Prototype on a breadboard first"

**Believed:** phase 3 of the original plan.
**Refuted by:** the connector. Micro-Fit has a 3.0 mm pitch and does not fit a
breadboard.
**Cost:** none. Everything is socketed and the board is the prototype, which is
why `CAN_MODE=LOOPBACK` exists — it exercises bit timing, filters, the FIFO and
the transmit path on a desk with no bus and no transceiver at all.

---

## E. The toolchain

E1 to E4 landed in one afternoon, and **none of them was the
firmware's fault**. All four are now encoded in `mplab/Makefile` so they cannot
recur. E5 is CI's; E6 is the programmer's, and is the only one in this file
whose refutation is a piece of school physics.

### E1. "XC8 ships the device data"

**Believed:** reasonably, since every earlier XC8 did.
**Refuted by:** XC8 v4.00, which ships **none** — no `pic/dat`, no
`pic/include/proc`, no `docs/chips`. Everything about the part comes from a
Device Family Pack passed with `-mdfp`, and without one the build stops at
`error: (2103)`.
**Also retired:** the instruction to read `<xc8>/docs/chips/18f25k80.html`. It
does not exist; the per-device HTML now lives in the pack.

### E2. "`-mdfp` points at the pack"

**Refuted by:** `error: (2104)`, which reads like the pack is missing. It points
at the **`xc8` subdirectory inside** the pack.

### E3. "Any recent Device Family Pack will do"

**Refuted by:** the same error 2104. MPLAB X v6.00 bundles `PIC18F-K_DFP`
1.5.114 and XC8 v4.00 will not read it. v4.00's readme names **1.13.292**.

### E4. "The path to the pack is just a path"

**Refuted by:** a home directory containing an accented character. Under
`C:\Users\Luboš\.mchp_packs` the device data resolved but the pack's include
directories were **silently dropped**, and the build died two steps later on
`'pic18.h' file not found`. The pack lives at `C:\mchp_packs` for that reason
alone.
**Cost:** the longest of the four to diagnose, because the error appears two
steps away from its cause and blames the wrong file.

### E5. "`--netservername ''` is harmless if you are not using a network licence"

**Believed:** carried over in CI from the XC8 v2.50 pin.
**Refuted by:** three failed CI runs. v4.00's installer has no such option and,
being InstallBuilder, treats an unknown one as **fatal** rather than ignoring
it. It was passing an empty value, so it had never configured anything anyway.

### E6. "The PICkit 3 cannot power a target — it only manages 4.6 V of the 5.0 V it asks for"

**Believed** briefly, and written into `CLAUDE.md` and `docs/install.md` as a *measurement* that had finally replaced a piece of borrowed
errata. `ipecmd -I -W` against a bare ICSP header reports *"trying to supply
5,000000 volts ... but the target VDD is measured to be 4,625000 volts"*, and
that was read as the supply sagging: 0.375 V lost with no load at all, so
nothing left for a real board.

**Refuted by four things, the first of which should have stopped it being
written:**

- **There is no load.** The header was open — nothing connected to any pin. No
  current flows, and a supply cannot sag into an open circuit. Whatever 4.625 V
  is, it cannot be droop, and the argument was self-refuting on the evidence it
  was standing on.
- **Watching the rail.** It does not step to 4.6 V. It rises to roughly
  **5.5 V and settles back to 4.6 V after about a second** — the profile of
  something regulating to a set point, not of something failing to reach one.
- **The readme.** §17.36: `-W` powers the target *"at default VDD voltage"* and
  takes an argument — `-W2.5` *"powers the target to 2.5 volts"*. §17.38 adds
  `-A`, `-N` and `-X` for VDDAPP, VDD Nominal and VDD Max. So the tool has a
  commanded voltage and a measured one, and the message is a **mismatch between
  a set point and a readback** with its own tolerance. It is not a complaint
  about capability.
- **It has been done.** The same flag was used successfully on an earlier
  project on this MCU.

**Cost:** one commit (`8203082`) whose central claim was exactly this, and a
paragraph in two documents that presented an interpretation as a measurement.
The observation itself — 4.625 V — was real and is retained; only the reading
of it was wrong.

**What survives.** `-W` is still not used, and none of the reasoning above ever
argued that it should be. The grounds are unchanged from before the false
measurement was added: the board takes 5 V from the display or a bench supply,
so the flag **buys nothing**, and *Readme for PICkit 3.htm* §8.3.2 records a
silicon issue on the PIC18F45K20/46K20 family that appears only with *"power
from programmer"* — not our part, cited honestly as somebody else's errata,
and reason enough to decline a risk that has no upside. **`-W never` is a
decision, not a limitation of the tool.**

**Not affected:** the separate finding that `-W` leaves the rail live after the
command exits, and that a plain run clears it. That was tested by alternation
with the meter watched throughout, and it is the reason the header must read
zero before a self-powered board is connected. See `docs/install.md` step 4.

**Lesson.** The project's rule is that a decision must not be dressed up as a
specification. This is the same failure one step further on: an *interpretation*
dressed up as a measurement. The number was measured; "therefore it cannot drive
a load" was not, and the two sat in one sentence.


### E7. "A node nobody acknowledges climbs to 256, goes bus-off and falls silent"

**Believed** because it is what the counting rule looks like from one end:
DS39977C §27.14.7 says the devices "go to bus-off if the transmit error counter
equals or exceeds the bus-off limit of 256", an acknowledge error makes the
transmitter send an error flag, and an error flag costs 8. Thirty-two failed
tries is a fraction of a second, so a converter alone on a bench bus should be
silent almost immediately. `docs/install.md` step 7.3 said so, and
`tools/bench_test.py` **checked for that silence** and treated frames as the
failure.

**Refuted by the bench, twice, and one of them by accident.** Between every
flash and the start of a test, nothing on the bench bus acknowledges anything.
The converter transmits into that silence for as long as it lasts — and it
never stops. A capture of one such window has **3629 frames of 0x600 in two
seconds**, going on for tens of seconds; the deliberate version in 7.3 measures
**1812 frames a second against 22 nominal**. When acknowledgements came back,
0x603 reported `TXERRCNT` at **116** and `COMSTAT` showing `TXWARN|EWARN`, not
`TXBO`. It had never been anywhere near 256.

**Why.** The same sentence in §27.14.7 that gives the limits also says the
counters are incremented "in accordance with the CAN bus specification", and
the specification's fault-confinement rules carry an exception the datasheet
does not spell out: a transmitter that is **already error-passive**, detects an
acknowledge error, and sees no dominant bit while sending its passive error
flag, **does not increase TEC**. So TEC climbs 8 at a time to 128, the node
becomes error-passive, and there it stays — retransmitting for ever. Bus-off
needs somebody else on the bus generating errors, which is exactly what a lone
node does not have.

**What this cost.** Nothing on the car, and half a day on the bench: the
retransmission storm is also why `UNHEALTHY` and the refusal counter are set on
almost every bench run before a single test has started, which read as a fault
in the converter for most of a morning. `tools/bench_test.py` now explains that
state where it prints it.

**What survives.** The recovery claim, which was never about this path.
DS39977C §27.11's 128 × 11 recessive bits is how a module that really did go
bus-off comes back, with no MCU intervention. This firmware has still never
been observed in bus-off, so **that path remains untested on this silicon** —
say so rather than assuming 7.3 covered it.

**Lesson.** A limit in a register description is not the whole counting rule.
The datasheet said where it delegates, and the delegated document was not read.
