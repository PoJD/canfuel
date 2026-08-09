# canfuel — converter firmware

A fuel consumption converter for the VW New Beetle, AQY engine (2.0 l / 85 kW,
PQ34). It reads the powertrain CAN bus (500 kbps), computes consumption, range,
torque and power, and sends them back onto the bus in frames 0x600–0x602. A
CANchecked MFD15 Gen2 display renders them from its own TRI file (repo `mfd15`).

MCU: PIC18F25K80, 16 MHz, XC8. The board lives in the `kicad` repo.

---

## Sourcing hardware facts — manufacturer datasheets only

The same rule as in the `kicad` repo, and for the same reason. It applies here
to firmware: **every register name, configuration bit, timing, endurance
figure and electrical limit comes from the manufacturer's datasheet for the
exact part, and from nothing else.** Not forum posts, not application notes
recalled from memory, not "this is how it is always done", not code from a
previous project, and not the recollection of whoever is at the keyboard —
**including the model's.**

When the datasheet does not settle a question, **ask the maintainer**. Do not
fill the gap with a plausible number. A guess that looks like a specification
is worse than an open question, because the next person cannot tell them apart.

In practice:

- **Quote the source.** Every hardware constant in the code or the docs names
  its document and section — `DS39977C §2.7`, `DS39977C Table 31-1 D122`. A
  number without a citation is a number nobody can re-check.
- **The datasheets are in `docs/`.** `pic18f25k80-datasheet.pdf` (Microchip
  DS39977C, PIC18F66K80 family) and `mcp2562-datasheet.pdf` (DS20005167C,
  MCP2561/2). They are duplicated from the `kicad` repo on purpose: firmware
  work should not depend on a sibling checkout being present.
- **Register tables outrank prose.** The chapters are summaries and they do
  get it wrong — see the CANMX finding below, where the ECAN chapter's opening
  paragraph contradicts the configuration register table.
- **Absolute Maximum Ratings outrank the DC characteristics tables**, and both
  outrank what a part is observed to tolerate.
- **Where the datasheet is deliberately not followed**, say so and say why,
  next to the citation. An unexplained deviation is indistinguishable from an
  oversight six months later.
- **Typical is not guaranteed.** A figure given only as *typ* with no min/max
  cannot be designed against. Say what it is and what that costs — the FVR
  below is exactly this case.

Facts about the *car* — the signal table, the frame periods, that the bus is
already terminated — are not datasheet questions. They were settled by
measurement and are marked as measured where they appear, in
`docs/can-decoding.md`. The rule above is about parts.

`pdftotext -layout docs/pic18f25k80-datasheet.pdf -` makes the PDF greppable,
which is the fastest way to find a parameter number.

### Working code from the other repos is evidence, not a source

`github.com/PoJD/can` holds `CanSwitch.X` and `CanRelay.X`, and
`github.com/PoJD/piclib` holds the CAN and EEPROM layer they share. **Both run
the same PIC18F25K80 at the same 16 MHz crystal**, in a house, in production.
That makes them the right place to start every one of the questions below — it
is a known-good register-level setup on identical silicon, which no datasheet
can give you.

What it does not do is replace the citation. Working code proves that a
configuration works *in that application*; it does not prove the value is
right for this one, and it does not stop a deviation from the datasheet
propagating. Two cases from this repo, both real:

- `CanSwitch.X/config.h` sets `CANMX = PORTC`, which is correct there and
  **wrong here** — this board is wired to RB2/RB3. Copying the file wholesale
  is the single most expensive mistake available.
- `piclib/dao.c` omits the `GIE` bracket the datasheet's required sequence
  puts around the EEPROM unlock. It is harmless in a switch that sleeps most
  of the time and is not harmless here.

So: read them first, then check what you took against the PDF, then cite the
PDF. Neither repo is a submodule of this one; clone them beside it when
needed.

---

## Current state — read this first

**The pure C core is done and verified against every fixture. What is missing
is the hardware half: `main.c`, `hal_can.c`, `hal_sys.c` and the MPLAB
project.** `mplab/` is still empty.

What exists and works:

- `src/config.h`, `decode.c`, `compute.c`, `txframes.c`, `persist.c` — the
  whole brain of the device, no `<xc.h>` anywhere, all scaled integers
- `test/` — 238 checks across four test binaries, plus `replay_host.c`
- `tools/canlog.py`, `tools/replay.py` — 77 Python tests green, and
  `replay.py --host-build` now diffs Python against the C core
- `test/fixtures/` — seven real logs from the car, documented
- `docs/` — decoding, frame layout, refuelling reset, the overall plan

The C core reproduces the Python oracle on all seven logs: the fuel totals and
restart counts agree **exactly**, distance to within 7 mm over 54 m. Whichever
of the two is wrong, they are at least wrong identically, and both were checked
against the numbers measured in the car.

All three CI jobs do real work now except `firmware`, which is still a
placeholder until there is an MPLAB project to build. `core` runs
`make check-pure`, `make test` and the `--host-build` diff.

### Next step: the hardware half

1. `hal_sys.c` — timer for the millisecond clock, ADC/FVR for VddConv, the two
   LEDs, the `DBG_EN` jumper, EEPROM read/write behind `persist_backend_t`
2. `hal_can.c` — ECAN on **RB2/RB3**, 500 kbps, receive filters for the seven
   identifiers in `config.h`, transmit for 0x600–0x602
3. `main.c` — the cooperative scheduler from `implementation-plan.md` §3.7:
   10 ms drain CAN, 100 ms send 0x600/0x601, 1 s send 0x602 and
   `persist_save()`
4. the MPLAB X project and the XC8 half of CI

Everything those four need from the core already exists and is tested. The
seven board obligations in the next section are firmware work and all of them
land in `hal_sys.c` — in particular driving the fourteen unused pins low.

The core's API and the decisions already taken for the HAL are two sections of
their own below. Read those before writing any of the four; between them they
should mean no design work is needed, only PIC work.

### Local toolchain

gcc, make, git and Python 3.11 are installed. XC8 is not — the `firmware` CI
job and any real device build still need it.

**A local quirk, not a repo problem:** in this shell `make` hands its recipes
an empty `TMP`, and the MSYS2 gcc then tries to write its temporary files into
`C:\WINDOWS` and is refused. Working around it is one word on the command line:

```
make -C test TMP="$TEMP" test
```

Plain `make` works everywhere else, including CI.

---

## The board exists now, and it fixes the pin assignment

**Three boards were ordered from Gatema PCB on 2026-08-09** and are expected
during the week of 2026-08-17. The design is finished, checked and frozen: what
is being manufactured is commit `c06e710` of the sibling `kicad` repo. Nothing
here is blocked by them — phase 1 is a pure C core with host tests and needs no
hardware — but the pinout below is no longer provisional, and `hal_can.c` and
`hal_sys.c` must be written against it.

Only two of the three can be populated at first; the third is a bare spare
waiting on two more Micro-Fit headers, deliberately not yet bought.

**Everything in this section comes from `kicad/canfuel/docs/implementation-plan.md`
§4.2. If it ever disagrees with that file, that file wins.**

| Signal | Pin | Notes |
| --- | --- | --- |
| `CAN_TX` | **RB2** (23) | to MCP2562 pin 1 |
| `CAN_RX` | **RB3** (24) | to MCP2562 pin 4 |
| `LED_PWR` | **RC0** (11) | via 1 kΩ to an LED to ground, active high |
| `LED_CAN` | **RC1** (12) | via 1 kΩ to an LED to ground, active high |
| `DBG_EN` | **RA0** (2) | JP1 to +5 V, 10 kΩ pull-down |
| `PGC` / `PGD` | RB6 / RB7 (27/28) | ICSP header J3 |
| MCLR | 1 | R6 470 Ω, C8 100 nF behind jumper JP2 |
| OSC1 / OSC2 | 9 / 10 | 16 MHz crystal, HS, **no PLL** |

Seven things follow from the board and are firmware obligations, not
suggestions:

1. **The fourteen unused pins must be driven low at start-up** — RA1, RA2, RA3,
   RA5, RC2–RC7, RB0, RB1, RB4, RB5. DS39977C §2.7 wants unused I/O either
   driven low or pulled to VSS through 1–10 kΩ, and **there are no resistors on
   the board for this**; fourteen of them would have cost more area than they
   were worth. The pins go nowhere at all — the escape header that used to
   break them out was removed because it made both LEDs and the whole ICSP
   connector unroutable. So this is the only thing standing between them and
   floating inputs.
2. **CANTX/CANRX are on RB2/RB3, so the config bit must say so.** The ECAN
   module can also sit on RC6/RC7 and both were once brought out; with the
   escape header gone, moving it now means soldering onto the PDIP socket pins
   from underneath. Get the config bit right the first time.
3. **The LEDs only light when `DBG_EN` is high**, i.e. when JP1 is fitted.
   Nothing may light up in the car. The 10 kΩ pull-down means an absent jumper
   is a defined low, not a floating input — but RA0 is AN0, so **it has to be
   switched to digital** before it is read.
4. **The MCP2562's STBY pin is hard-wired to ground.** There is no standby
   control line and no pin to drive; do not write one. Its VIO is tied to VDD.
5. **The 120 Ω termination is deliberately not fitted** (R5, silkscreened
   `120R DNF`). The car's bus is already terminated at both ends. Bench testing
   off the car needs an external terminator.
6. **JP2 must come off before programming and go back afterwards.** It puts the
   100 nF MCLR capacitor in circuit, which is what DS39977C Figure 2-2 asks for
   and also what interferes with ICSP.
7. **Pin 6 is VDDCORE/VCAP, not a port pin.** The 28-pin K80 has no RA4 and no
   ENVREG: the core regulator is always on. Nothing to configure, but do not go
   looking for an ENVREG bit.

Port A can only sink or source 2 mA against port B and C's 25 mA, which is why
the LEDs are on port C. If anything ever needs a spare pin that drives current,
it does not come from port A.

## The one coupling to another repo

This repo sits next to two siblings, `kicad` (the board) and `mfd15` (the
display config). They have separate toolchains and separate GitHub remotes
under `PoJD/`, and the directory above them is deliberately not a git repo.

The coupling to **`mfd15`** is **the layout of frames 0x600 and 0x601**,
defined in `docs/frames.md` and consumed by `mfd15/tri/S-AQY.TRI`. The coupling
to **`kicad`** is the pin assignment in the section above — one-way, and
already frozen by an order that has been placed.

That file has already been uploaded to a real display and verified, so it is
final until this firmware starts transmitting. When the layout changes here, it
must change there in the same breath. Getting it wrong does not produce an
error — the display shows plausible but wrong numbers, which is worse.
`test/test_txframes.c` pins every offset against the TRI file, with the
relevant TRI lines quoted in its header comment.

**0x602 is not coupled to anything.** S-AQY.TRI does not read it — it was
checked, sensor by sensor, while phase 1 was being written. It is ours to
change freely and exists to be watched on a USBtin. Likewise `Flow` in
0x601 b4–5 is transmitted but has no sensor on the display; that one is
deliberate, so a dedicated gauge can be added later without touching firmware.

The useful check once the converter is live: compare FuelNow against
FuelCntRaw on the display. FuelCntRaw is the raw ECU counter with no
conversion, so if it rises while FuelNow shows nonsense, the fault is in this
firmware's arithmetic rather than in its input.

---

## Language

**Everything in this repository is written in English** — code, identifiers,
comments, docstrings, CLI help text, documentation, commit messages and file
names. Conversation with the maintainer may be in Czech; nothing written to
disk ever is.

---

## Non-negotiable rule: a pure C core

`src/decode.c`, `src/compute.c` and `src/txframes.c` **must not contain a
single `#include <xc.h>`.** They take arrays of bytes and a time in
milliseconds, and return numbers.

`src/persist.c` is held to the same rule and `make check-pure` enforces it for
all four. It reaches the EEPROM through two function pointers
(`persist_backend_t`), which is what lets `test_persist.c` simulate 100,000
write cycles against a RAM array and check that the wear really is spread.

The whole core has to be compilable with gcc and testable against real logs
without a single piece of hardware. That is what should prevent ten board
revisions — before anything is soldered, a log is replayed and the consumption
figures are checked by eye.

Hardware belongs exclusively in `hal_can.c` and `hal_sys.c`.

**No floating point anywhere in the core.** Every quantity is a scaled integer
and every name says which scale: `_UL` microlitres, `_MM` millimetres, `_MMH`
0.001 km/h, `_CNM` 0.01 Nm, `_D` tenths, `_C` hundredths. The PIC18 has no FPU,
the accumulators have to be exact, and everything ends up an integer on the
wire regardless — a float would only be somewhere for rounding to hide. Two
identities do most of the work and are worth knowing:

- **one microlitre per metre is exactly 0.1 l/100 km**, so `FuelAvg` is a
  single division of the two accumulators
- **v [0.001 km/h] × t [ms] ÷ 3600 = s [mm]**, so distance never needs a
  conversion factor either

---

## The core's API — what `main.c` has to call

The whole core is four headers and no globals. Every function takes the state
it works on, so there is nothing to initialise in a particular order beyond
what is shown here. Written out in full because it is the one thing a new
session would otherwise reconstruct by reading five files.

```c
decode_state_t  st;   /* last known bus state          */
compute_t       cp;   /* accumulators and windows      */
persist_t       ps;   /* which EEPROM slot comes next  */
tx_values_t     tx;   /* one gather, three frames      */
```

**At start-up**

```c
decode_init(&st);
compute_init(&cp);

persist_record_t rec;
if (persist_load(&ps, &hal_eeprom_backend, &rec)) {
    compute_restore(&cp, rec.total_ul, rec.total_mm,
                    rec.tank_stable_l, rec.tank_stable_valid);
}
/* A virgin EEPROM returns false and zeroed accumulators. That is correct,
 * not an error -- do not treat it as one. */
```

**Every received frame**, from the 10 ms slot:

```c
decode_frame(&st, id, data, dlc);          /* returns false for ids we ignore */
if (id == CAN_ID_FUEL) {
    compute_on_fuel(&cp, &st, now_ms);     /* 0x480 is the heartbeat */
}
```

**Every scheduler tick** — integrates distance, samples the tank once a second,
and is safe to call as often as you like:

```c
compute_tick(&cp, &st, now_ms);
```

**Every 100 ms**

```c
txframes_gather(&tx, &cp, &st, hal_sys_vdd_c(), now_ms);
txframes_fuel(&tx, buf);    hal_can_send(CAN_ID_TX_FUEL,   buf, TXFRAME_DLC);
txframes_engine(&tx, buf);  hal_can_send(CAN_ID_TX_ENGINE, buf, TXFRAME_DLC);
```

**Every second**

```c
txframes_trip(&tx, buf);    hal_can_send(CAN_ID_TX_TRIP, buf, TXFRAME_DLC);

persist_record_t rec = { cp.total_ul, cp.total_mm,
                         cp.tank_stable_l, cp.tank_stable_valid };
persist_save(&ps, &rec, now_ms);   /* itself decides whether to write */
```

`persist_save()` already carries the once-a-minute rule and the only-on-change
rule. Call it every second and let it say no — do not build a second timer for
it in `main.c`.

Three things `main.c` must **not** do, because the core already does them:

- clear the trip on refuelling — `compute_tick()` does it and bumps
  `cp.refuels`
- zero the transmitted values when the bus goes quiet — `txframes_gather()`
  does it, and deliberately leaves `VddConv` alone
- clamp anything to the display's range — every getter clamps

`now_ms` is a free-running millisecond counter. It may wrap; the core uses
unsigned differences everywhere and handles the wrap correctly, so it must
**not** be reset or clamped by `hal_sys`.

---

## Decisions already taken for the HAL

Everything below that carries a citation was read out of
`docs/pic18f25k80-datasheet.pdf` (DS39977C) or `docs/mcp2562-datasheet.pdf`
(DS20005167C). Everything without one is **not yet sourced** and is marked. Do
not promote an unsourced line to a settled one without opening the PDF.

**`CANMX` is 1, and the chapter text says the opposite.** DS39977C Register
28-5 (CONFIG3H, byte address 300005h) defines bit 0:

> `1` = CANTX and CANRX pins are located on RB2 and RB3, respectively
> `0` = CANTX and CANRX pins are located on RC6 and RC7, respectively

The board is wired to RB2/RB3, so the bit is **set**, which is also the reset
default. But §22.0's opening paragraph says the pins "can be placed on
alternate I/O pins by *setting* the CANMX Configuration bit" — which is
backwards. The register table and the pin-table footnote ("Default pin
assignment for CANRX and CANTX when the CANMX Configuration bit is set") agree
with each other against the prose, so the table wins.

This is exactly why the rule above exists, and why obligation 2 in the board
section is worth taking seriously: with the escape header gone, getting this
wrong means soldering to the underside of the PDIP socket. Take the `#pragma
config` keyword from the XC8 device header rather than guessing its spelling.

**Unused pins — the datasheet gives two options and the board only allows one.**
DS39977C §2.7: *"Unused I/O pins should be configured as outputs and driven to
a logic low state. Alternatively, connect a 1 kΩ to 10 kΩ resistor to VSS on
unused pins and drive the output to logic low."* There are no such resistors on
the board, so the first option is the only one available: TRIS to output, LAT
to zero, for RA1, RA2, RA3, RA5, RC2–RC7, RB0, RB1, RB4, RB5.

**EEPROM.** 1,024 bytes on the PIC18F25K80 (DS39977C Table 1, device summary).
The circular buffer occupies 0..767 and leaves the top 256 free. From
Table 31-1, Memory Programming Requirements:

| Param | What | Value |
|---|---|---|
| D120 | Byte endurance | **100 K min**, 1000 K typ, −40 to +125 °C |
| D122 | TDEW, erase/write cycle time | 4 ms typ |
| D124 | TREF, total erase/write cycles | 1 M min, 10 M typ |
| D121 | VDD for read/write via EECON | 1.8 to 5.5 V |

D120 is the number `persist.c`'s header comment argues from and it is a
*minimum*, which is the right way round to design. The 4 ms of D122 is why the
write must not be attempted from an interrupt; once a minute it is otherwise
irrelevant. D124 is worth knowing about — it is a budget for the whole array,
not per byte, and 100,000 writes spread over 64 slots spends 100 K of the 1 M.

`persist.c` wants exactly two functions and their shape is already fixed:

```c
uint8_t hal_eeprom_read(uint16_t addr, void *ctx);
void    hal_eeprom_write(uint16_t addr, uint8_t value, void *ctx);
```

wrapped in a `persist_backend_t`. `ctx` is unused on the PIC — pass `NULL`.

**VddConv, and what it is honestly worth.** The plan is `VDD = 1.024 × 1023 /
ADC`, reading the band gap on ADC channel 31 (DS39977C: *"11111 = Channel 31
(1.024V band gap)"*) against VDD as the converter's reference. Two things the
datasheet says about that:

- the reference is specified as **1.024 V typical with no tolerance given**.
  So VddConv is a trend and a sanity check, not a calibrated voltmeter. If an
  absolute reading is ever wanted, it needs a per-unit calibration constant.
- Table 31-11 parameter 36, TIVRST: the internal reference takes **25 µs typ**
  to become stable. Enable it and wait before the first conversion.

Returned as `uint16_t hal_sys_vdd_c(void)` in 0.01 V, which is what
`txframes_gather()` takes.

**MCP2562.** DS20005167C: the `STBY` pin is the standby control (§1.7.9) and on
this board it is hard-wired to ground, so there is no line to drive and no
standby mode to write. `VIO` exists only on the MCP2562, not the MCP2561, and
here it is tied to VDD — so the digital levels are plain 5 V and no level
shifting is involved.

**LEDs.** `LED_PWR` on RC0 and `LED_CAN` on RC1, active high through 1 kΩ, and
only when `DBG_EN` (RA0) is high. Nothing lights up in the car. **RA0 is AN0,
so it has to be switched to digital before it is read** — left analogue it
reads zero and the LEDs simply never work, a bug that looks exactly like a
wiring fault. The pin assignment itself comes from the board section below,
which is sourced from `kicad`.

**Which frames to receive.** The seven `CAN_ID_*` identifiers in `config.h`.
Fourteen identifiers are broadcast periodically, so hardware filtering rather
than filtering inside `decode_frame()` is worth it at 500 kbps.

**Configuration bits — start from `CanSwitch.X/config.h`, change exactly one.**
That file is a working PIC18F25K80 configuration at a 16 MHz crystal, and
almost all of it transfers unchanged: `PLLCFG = OFF`, `XINST = OFF` (XC8
requires it), `MCLRE = ON`, `STVREN = ON`, `IESO = OFF`, `FCMEN = OFF`, all
the code and table protection off.

| Bit | CanSwitch | canfuel | Why |
|---|---|---|---|
| `CANMX` | `PORTC` | **`PORTB`** | this board is wired RB2/RB3 |
| `FOSC` | `HS1` | `HS1` | see below |
| `WDTEN` | `OFF` | undecided | a car is a better argument for a watchdog than a light switch is |

`CANMX = PORTB` / `PORTC` is also the answer to the pragma spelling. Their
comment on `PORTC` reads "ECAN TX and RX pins are located on RC6 and RC7",
which agrees with Register 28-5 and against the §22.0 prose — a third
independent confirmation of the reading above.

**`FOSC = HS1` at 16 MHz, and Table 3-1 cannot be used to check it.** DS39977C
Register 28-2 gives `0011 = HS1, HS oscillator (medium power, 4 MHz-16 MHz)`
and `0010 = HS2, HS oscillator (high power, 16 MHz-25 MHz)`, so 16 MHz is the
top of one range and the bottom of the other and either is defensible. HS1 is
what the sibling projects run at this crystal, so HS1 it is.

Table 3-1 appears to say the opposite — its frequency column is misaligned
against its mode column by one row from HS1 downwards. **Use Register 28-2.**

**The instruction cycle is Fosc/4**, so 16 MHz gives 4 MHz and Tcy = 250 ns.
DS39977C, CLKOUT in the pin table: *"OSC2 pin outputs CLKO, which has 1/4 the
frequency of OSC1 and denotes the instruction cycle rate"*, and T0CON's T0CS
bit selects *"0 = Internal instruction cycle clock (CLKO)"*. `CanSwitch.X`
confirms it empirically: Timer0 in 16-bit mode with a 1:16 prescaler off that
clock rolls over at 4 MHz/16/65536 ≈ 3.8 Hz, which is the "roughly 4 times a
second" its comment claims. (Its arithmetic calls 4 MHz the *oscillator* rate,
which is muddled — the conclusion is right, the reasoning is not. Worth
noticing, since a right value on a wrong reason stops being right the moment
anything moves.)

**500 kbps works out to BRP = 0 and needs no cleverness.** DS39977C §22 gives
`TQ (µs) = (2 × (BRP + 1))/FOSC (MHz)` and Register 22-x allows
`BRP<5:0> = 000000 → TQ = (2 × 1)/FOSC`. At 16 MHz that is TQ = 0.125 µs, and
piclib's fixed 16 TQ bit time gives 2 µs — exactly 500 kbps.

`piclib`'s own formula, `BRP = (1000 × cpuSpeed)/(32 × baudRate) − 1`, returns
0 for `can_setupBaudRate(500, 16)`, so the call is simply correct. Note it
wants the **oscillator** frequency, not the instruction rate. Its segment
split is SYNC 1 + PROP 4 + PS1 8 + PS2 3 = 16 TQ, sampling at 81.25 %.

**`piclib` needs one addition before it can be used here.**
`can_initRcPortsForCan()` sets `TRISC6`/`TRISC7` and nothing else — it is
hard-wired to the RC pin pair. This board needs RB2 as output and RB3 as
input. Either add a `can_initRbPortsForCan()` upstream or do those two lines
in `hal_can.c`; do not call the RC one. The library is consumed by adding its
sources to the project rather than by linking a binary, so a submodule works.

**`piclib`'s EEPROM layer is otherwise exactly the right shape** — `dao.c`
does `EEADRH:EEADR` addressing over the full 10-bit range, the `0x55`/`0xAA`
unlock, `WREN`, and polls `WR` until the hardware clears it. It maps onto
`hal_eeprom_read`/`hal_eeprom_write` almost line for line.

**It is missing the interrupt bracket, and here that matters.** DS39977C §8.5
marks `BCF INTCON, GIE` … `BSF INTCON, GIE` as part of the **Required
Sequence** around the unlock and the `WR` set. `dao.c` never touches `GIE`.
That is survivable in a switch that idles asleep; canfuel will have a
millisecond timer interrupt and possibly a CAN receive interrupt running, and
an interrupt landing between the `0x55` and the `0xAA` aborts the unlock and
the write fails **silently**. Add the bracket in `hal_sys.c`.

### Not yet sourced — open the datasheet before relying on these

- *Which timer makes the millisecond.* `CanSwitch.X` uses Timer0 in 16-bit
  mode with a 1:16 prescaler, but only for a coarse debug heartbeat, not a
  millisecond tick. The divider chain for 1 ms out of 4 MHz has not been
  worked out here and nothing has been checked for a clash with the ECAN
  module.
- *Interrupt or polling for receive.* At 500 kbps with fourteen periodic
  identifiers the 10 ms slot may not drain the buffers in time. Needs the
  receive-buffer and overflow behaviour in §22 before it can be decided.
  Neither sibling project settles it — a light switch sees a fraction of this
  traffic.
- *Whether the watchdog goes on.* Both siblings run with `WDTEN = OFF`. A
  converter wedged in a car is a worse outcome than a light switch wedged in a
  wall, so this deserves its own decision rather than an inherited one.

**The millisecond clock, independent of which timer provides it.** One
free-running `uint32_t`, exposed as `uint32_t hal_sys_millis(void)`. Read it
once at the top of each scheduler pass and hand that one value to every core
call in the pass — reading it repeatedly can straddle a millisecond and hand
the core a tick of zero where it expects one. It must be read atomically
against the interrupt that writes it. This is a software decision, not a
datasheet one.

---

## Read `docs/can-decoding.md` before touching the maths

It documents four traps that are easy to run aground on quietly. In short:

1. **The speed validity gate is not an equality.** `b1 == 0x40` is wrong; the
   correct rule is `(b1 & 0x40) && !(b1 & 0x03)`. The equality throws away two
   thirds of the samples and corrupts both FuelAvg and Range.
2. **The fuel counter resets to zero when the ignition goes off.** Without
   restart detection (`counter == 0 || rpm == 0` → reinitialise `prev`) the
   delta jumps nonsensically. The delta is always `(new − old) mod 32768`.
3. **Bit 15 of the counter is not constant.** It is zero from ignition on until
   the first wrap, then permanently one. The 0x7FFF mask drops it anyway.
4. **FuelAvg must return zero below 100 m of distance.** Otherwise it divides
   by nearly zero.

---

## Layout

```
src/
  main.c        scheduler and glue — the only place it all meets   TO DO
  decode.c/.h   frame parsing          PURE C                      done
  compute.c/.h  maths                  PURE C                      done
  txframes.c/.h frame assembly         PURE C                      done
  persist.c/.h  EEPROM circular buffer PURE C                      done
  hal_can.c/.h  ECAN + MCP2562                                     TO DO
  hal_sys.c/.h  timers, ADC/FVR, LEDs, jumper                      TO DO
  config.h      every constant and switch                          done
test/
  tt.h          the test framework, small enough to read at a sitting
  logread.h     the fixture parser in C, the counterpart of canlog.py
  replay_core.h one log through decode + compute, mirrors replay.py's loop
  replay_host.c the binary behind replay.py --host-build
  test_*.c      decode, compute, txframes, persist
tools/          canlog.py, replay.py — Python, runs anywhere
```

`tt.h`, `logread.h` and `replay_core.h` are header-only on purpose: the
Makefile builds one `test_*.c` against the core and nothing else, so a helper
that needed its own object file would mean touching the build rule every time.

Constants belong in `config.h`, not in the code. In particular
`FUELNOW_LH_BELOW_MMH`, `FUELNOW_CLAMP_D`, `REFUEL_RISE_L` and the frame
periods.

The `piclib` library (github.com/PoJD/piclib) will be added as a submodule — it
provides `can_setupBaudRate(baudRate, cpuSpeed)` and the EEPROM layer behind
`persist_backend_t`. It is consumed by adding its sources to the MPLAB project,
not by linking a binary. Two things it needs first are in the HAL section: an
RB2/RB3 port init, and the `GIE` bracket around the EEPROM unlock.

---

## Tools

```
python tools/canlog.py test/fixtures/03_drive.txt          # per-ID summary
python tools/canlog.py --dump --id 0x480 FILE              # print frames
python tools/replay.py --every 100 test/fixtures/07_accel.txt
python -m unittest discover -s tools -p "test_*.py"        # 77 tests

make -C test test                                          # 238 checks
make -C test check-pure                                    # no <xc.h> in the core
python tools/replay.py --host-build test/fixtures/*.txt    # Python vs C
```

`tools/replay.py` is the reference decoder in Python, written against the same
table as `decode.c` and `compute.c`. `--host-build` runs
`test/build/replay_host` over the same logs and diffs the totals; the fuel
counter and the restart count must agree exactly, distance to within a tenth of
a percent. It is a CI step, so the two cannot drift apart quietly.

`tools/test_replay.py` and `test/test_compute.c` are deliberately twins — same
fixtures, same expected numbers, one in floats and one in scaled integers.
**A change to the maths belongs in both.**

### Before committing anything that touches the core

The four commands above, in that order. All of it runs in under fifteen
seconds and it is exactly what CI does, so a green run here means a green run
there. On this machine, remember the `TMP="$TEMP"` workaround for `make`.

Adding a `test_*.c` needs no Makefile change — the glob picks it up, builds it
against all four core sources and runs it.

---

## Fixtures

Real logs from the car. **Do not edit them.** The tests reference exact numbers
from them.

⚠ `02_idle_60s.txt` contains the recording **twice** — both halves are
identical. It is corrected at read time (`parse_file(..., fix_doubled=True)`)
and the file itself stays original. Without that, the idle flow comes out doubled.

Details and a table of every log: `test/fixtures/README.md`.

---

## Verified values the core reproduces

The C core produces every one of these, and `test_compute.c` asserts them.
Distance and the fuel totals also match `tools/replay.py` — see the table
under *Current state*.

| Log | Counter total | Duration | Flow | Distance |
|---|---|---|---|---|
| `01_ign_only` | 0 µl | — | 0 | 0 |
| `02_idle_60s` | 18,652 µl | 60.1 s | 310 µl/s = 1.12 l/h | 0 |
| `03_drive` | 11,424 µl | 35.0 s | 326 µl/s | 54.3 m |
| `05_rev3000` | 1,940 µl | 1.93 s | 1005 µl/s | 0 |
| `06_trip_reset` | 51,992 µl | 135.0 s | 385 µl/s | 124.6 m |
| `07_accel` | 9,752 µl | 15.9 s | 613 µl/s | 27.3 m |
| `idle` | 487 µl | 1.44 s | 339 µl/s | 0 |

The flow column is the average over the whole log; the sliding window inside
`compute.c` reports the last second, which is why the two differ on the logs
where the load changes.

---

## What comes next

The C core is finished. What remains of phase 1 is the hardware half —
`hal_sys.c`, `hal_can.c`, `main.c` and the MPLAB project — listed in order
under *Current state*. Reasoning for the ordering is in
`docs/implementation-plan.md` §3.

The breadboard phase is skipped — Micro-Fit has a 3.0 mm pitch and does not
fit a breadboard. The boards themselves arrive during the week of 2026-08-17.
