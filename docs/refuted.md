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

1. **From the web** — wiring documentation for this car. On the New Beetle with
   the AQY (PQ34) there is no consumption wire. The powertrain is fully CAN and
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
  project on this MCU, on this desk.

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
