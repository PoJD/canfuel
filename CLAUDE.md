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

When the datasheet does not settle a question, **decide it and write the
decision down as a decision** — what was chosen, what it was chosen over, and
what the reasoning was. Do not fill the gap with a plausible number presented
as a fact, and do not stop and ask. A guess dressed up as a specification is
worse than an open question, because the next person cannot tell them apart; a
decision that says it is a decision is neither.

**Do not queue up questions for the maintainer.** Judgement calls belong in the
work, next to the code they produce. If something is genuinely undecidable
without information nobody has yet — a measurement off the car, a part that has
not arrived — say so in the same place, in one line, and carry on with
everything that does not depend on it.

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
`github.com/PoJD/piclib` holds the CAN and EEPROM layer they share. **Both are
built on the same PIC18F25K80 at the same 16 MHz crystal**, which makes them
the right place to start every question below: a known-good register-level
setup on identical silicon, which no datasheet can give you.

**Be precise about what was actually proven.** They were never installed in
the house. They were bench-tested over a 200 m run of LAN cable and everything
worked — a serious test of the wiring and the transceivers, and better
evidence than a desk full of jumper wires. But it is a bench test, and
`CanSwitch.X/main.c` runs `#define BAUD_RATE 50`.

Which matters here, because **canfuel runs at 500 kbps — ten times faster.**
Bus length and bit timing both scale against bit rate, so their 200 m result
says nothing about ours, and their bit timing was never exercised anywhere
near our rate. What transfers is the *plumbing*: the configuration bits, the
register sequences, the shape of the driver. The 500 kbps numbers in the HAL
section below stand on the datasheet arithmetic alone and have been run on
no hardware at all yet.

Working code also does not stop a deviation from the datasheet propagating.
Three cases, all real:

- `CanSwitch.X/config.h` sets `CANMX = PORTC`, which is correct there and
  **wrong here** — this board is wired to RB2/RB3. Copying the file wholesale
  is the single most expensive mistake available.
- `piclib/can_initRcPortsForCan()` is hard-wired to the same wrong pin pair.
- `piclib/can.c` never writes `CIOCON`'s `CLKSEL`, so the CAN system clock is
  left on its reset value, which selects the PLL (DS39977C Register 27-55).
  With `PLLCFG = OFF` there is no PLL and the datasheet does not say what the
  mux then delivers. It evidently works at 50 kbps; the bit rate is not
  something to leave to inference at 500 kbps.

**One claim that used to be in this section was wrong, and it is worth knowing
why.** It said `piclib/dao.c` omits the `GIE` bracket the datasheet's Required
Sequence puts around the EEPROM unlock. It does not — `dao_saveDataItem()`
opens with `di()` and closes with `ei()`, which is exactly that bracket, around
a superset of the sequence. The claim came from reading the inner
`dao_writeByte()` in isolation. Check the caller before writing down that a
sibling repo got something wrong.

So: read them first, then check what you took against the PDF, then cite the
PDF. Neither repo is a submodule of this one; clone them beside it when
needed. **`piclib` was evaluated for this firmware and not used** — the
reasoning is in the HAL section below.

---

## Current state — read this first

**The firmware is complete and it builds: `make -C mplab` produces
`mplab/build/canfuel.hex` under XC8 v4.00 with no warnings, using about a third
of the program memory and a sixth of the RAM.** What it has never been is *run
on a board* — see the warning at the end of this section, which is still the
most important thing on this page. (Exact byte counts are deliberately not
quoted here; `make -C mplab` prints them and this file would only go stale.)

What exists and works:

- `src/config.h`, `decode.c`, `compute.c`, `txframes.c`, `persist.c` — the
  whole brain of the device, no `<xc.h>` anywhere, all scaled integers
- `src/pic_config.h` — the `#pragma config` bits, every one of them cited
- `src/hal_sys.c` — Timer2 millisecond clock, the 12-bit A/D on the band gap,
  the two LEDs, the `DBG_EN` jumper, EEPROM behind `persist_backend_t`
- `src/hal_can.c` — ECAN on RB2/RB3 at 500 kbps, Mode 2 with an eight-deep
  receive FIFO, six hardware filters, three transmit buffers, and a
  build-time choice of Normal, Listen Only or Loopback
- `src/main.c` — the cooperative scheduler, and nothing else
- `mplab/` — `canfuel.X` for the IDE and a plain `Makefile` driving `xc8-cc`,
  which is the authoritative recipe and what CI runs
- `test/` — 250+ checks across four test binaries, plus `replay_host.c`
- `tools/canlog.py`, `tools/replay.py` — 80+ Python tests green, and
  `replay.py --host-build` now diffs Python against the C core
- `test/fixtures/` — seventeen real logs from the car, documented, of which
  the `_z1` ones are the only ones with trustworthy time
- `docs/` — **`install.md` is the plan**, plus decoding, frame layout,
  refuelling reset and timing

The C core reproduces the Python oracle on every fixture: the fuel totals and
restart counts agree **exactly**, distance to within 7 mm over 54 m. Whichever
of the two is wrong, they are at least wrong identically, and both were checked
against the numbers measured in the car.

All three CI jobs do real work now. `core` runs `make check-pure`, `make test`,
`make check-hal` and the `--host-build` diff; `firmware` installs a pinned XC8
**and a pinned Device Family Pack**, builds the hex and uploads it as an
artifact.

### What has and has not been verified — read before trusting any of it

The core is checked against every fixture. The hardware half is checked
against the datasheet, against `gcc -fsyntax-only`, and — since **2026-08-09** —
against XC8 v4.00 itself. What that last one does and does not settle:

- **It compiles and links clean, with no warnings, for the real part.** Which
  retires the two failure classes this section used to warn about: every
  register and bit name in `hal_can.c` and `hal_sys.c` exists on the
  PIC18F25K80, and every `#pragma config` keyword in `pic_config.h` is spelled
  the way the device data spells it. `test/xc8stub/xc.h` could never have shown
  either, since it agrees with the code by construction.
- **The configuration words were read back out of the hex, not assumed.**
  `CONFIG3H` at 300005h comes out `0x89`, so bit 0 `CANMX` is **set** — CANTX
  and CANRX on RB2 and RB3, which is what the board is wired to and what
  DS39977C Register 28-5 says that bit means. The single most expensive bit in
  the project, confirmed against the artefact that will actually be flashed.
  `CONFIG2H = 0x26` likewise reads back as `WDTPS<3:0> = 1001` = 512.
- **It fits, with room.** 11,594 bytes of 32,768 (35.4 %) of program space and
  564 bytes of 3,649 (15.5 %) of RAM, at `-O2`.
- **It still proves nothing about the silicon.** Compiling is not running. A
  register that exists but is written in the wrong order, at the wrong time, or
  with the wrong value compiles exactly as cleanly as one that does not.
- **500 kbps has been run by nobody.** The bit timing is datasheet arithmetic
  and nothing more; `CanSwitch.X` runs at 50 kbps, so `BRP = 0` and this whole
  path is untested. Check `hal_can_rx_errors()` / `hal_can_tx_errors()` and the
  `LED_CAN` blink pattern the first time it listens to the car.
- **The A/D reading is uncalibrated by construction.** The 1.024 V reference
  has no tolerance anywhere in the datasheet.
- **The timing budget is counted, not measured.** `docs/timing.md` costs every
  function out of the assembly listing XC8 generates. Summary: a typical pass
  is 49-134 µs so the loop runs 7,400-20,000 times a second; the 100 ms slot
  uses **2.6 ms of its 100**; the worst pass that can happen without an EEPROM
  write is **6.5 ms**, against a FIFO that tolerates 22 ms of blindness. **The
  whole firmware uses 16 % of the CPU**, and the largest single item in that is
  receiving frames rather than any arithmetic. `docs/timing.md` carries both
  halves — worst case per call, and load per second — plus every non-time
  ceiling in one table. The
  arithmetic is nowhere near being the constraint. The one figure the datasheet
  declines to bound is the EEPROM write — D122's 4 ms is a *typ* with no
  maximum — and nothing downstream of it is a deadline.
- **`docs/optimisation.md` is required reading before changing any loop or any
  arithmetic in `src/`.** It carries what was optimised and why, what was tried
  and rejected, and the two things that generalise on this part: use the
  narrowest integer type that provably holds the value, and prefer a walking
  pointer to an index in a hot loop. Both were worth as much as the algorithm
  change they accompanied.
- **There is no tank median any more**, since 2026-08-12. It was an insertion
  sort, then a 128-bucket histogram sweep, and then it turned out the
  refuelling rule never wanted a median: it wants "is the level persistently
  higher than it was", which is a first-order filter and a counter of
  consecutive at-rest samples. No loop, no division, 153 bytes of RAM back.
  `docs/refuel-reset.md` is the rule and `docs/optimisation.md` §8 the
  argument that it is the same answer.
- **Distance is integrated on `DIST_TICK_MS` = 10 ms with the remainder
  carried, and that is a correctness rule, not a budget.** `main.c` calls
  `compute_tick()` every pass, so before 2026-08-12 the delta was one
  millisecond and `v × 1 ms / 3600` truncated **6.4 % of the distance away at
  50 km/h and all of it below 3.6 km/h** — straight into FuelAvg, Range and the
  trip. No fixture could show it: the tests tick on 0x480, ~38 ms apart, where
  the same fault is 0.8 %, and the Python oracle had it too, so **the twins
  agreed with each other about a wrong number**. `DIST_MIN_MMH` is the other
  half: a standing car sends 0.005 km/h, which an exact integrator turns into
  83 mm a minute. `docs/optimisation.md` §6.
- **Neither division nor multiplication uses the compiler's helpers.** XC8
  v4.00 reaches for a per-bit loop for both — `___lldiv` 1,026 cycles,
  `___lmul` 849 — while the part has a single-cycle 8x8 multiplier it will only
  use for `uint8 x uint8` and `uint16 x uint8`. So both are assembled from byte
  products by hand: `src/fastmul.h` for multiplication (seven products, 137
  instructions) and `src/divconst.h` for division by a constant, which
  multiplies by a proved reciprocal instead. **`___lmul` is now absent from the
  build entirely** and the three remaining `___lldiv` calls all divide by a
  *variable*, where a reciprocal cannot help.
  Two details that are easy to undo by accident: `div_const` is a macro so the
  shift stays a literal, and a shift of 8/16/24 is free while any other is a
  rotate loop. Never add a divisor by hand — `tools/divconst.py` derives and
  proves it, `test/test_divconst.c` proves the C, and the exhaustive build
  walked 26.8 billion values.
  **A divisor here should be one the physics forces.** 1000, 3600 and 95500
  are; 120 (the tank filter) and 10000 (the drag slope) were our own scaling
  choices and became 128 and 2**16 on 2026-08-12, so both divisions are now
  shifts and both magics are gone. A constant we picked is a constant we can
  pick to be a power of two — `docs/optimisation.md` §11.
- **`tools/cycles.py` measures loop bodies out of the listing** and requires
  every backward branch in the build to be declared in one of its three tables.
  It stops rather than guessing, so a change of algorithm cannot pass silently
  — which it once did, reporting a new algorithm as costing exactly what the
  old one had.

### The first real compile happened, and what it cost

`make -C mplab` builds `mplab/build/canfuel.hex` on this desk with no
arguments. It took four rounds to get there and **not one of them was the
firmware's fault** — three of the four predicted failure classes (a wrong
`#pragma config` keyword, a wrong register name, the `const` address-space
warning on `hal_eeprom_backend`) simply did not happen, and the fourth,
address-of on an SFR, compiled as expected. Everything that went wrong was the
toolchain, and all of it is now encoded in `mplab/Makefile` so it cannot go
wrong again. The long version is in `mplab/README.md`; the short version:

1. **XC8 v4.00 ships no device data whatsoever.** No `pic/dat`, no
   `pic/include/proc`, no `docs/chips`. Everything about the part comes from a
   Device Family Pack passed with `-mdfp`, and without one the build stops at
   `error: (2103)`. This also retires an instruction that used to be in this
   file: `<xc8>/docs/chips/18f25k80.html` does not exist, and the per-device
   HTML now lives in the pack.
2. **`-mdfp` names the `xc8` subdirectory inside the pack**, not the pack root.
   The root gives `error: (2104)`, which reads like the pack is missing.
3. **The pack version must match the compiler.** MPLAB X v6.00 bundles
   `PIC18F-K_DFP 1.5.114`; v4.00 will not read it. v4.00's readme names
   **1.13.292**, which is what is installed here and what CI downloads.
4. **The path to the pack must be pure ASCII.** Under
   `C:\Users\Luboš\.mchp_packs` the device data resolved but the pack's include
   directories were silently dropped, and the build died two steps later on
   `'pic18.h' file not found`. The pack therefore lives at **`C:\mchp_packs`**,
   which is the makefile's default.
5. **MSYS make gives xc8-cc no usable `TMP`**, and clang dies with an LLVM
   stack dump rather than a message. The makefile now derives one from
   `cygpath -m /tmp`, which is why plain `make -C mplab` works.

One real code change came out of it, and it was cosmetic: `decode_rpm()` was a
`static inline` in `decode.h`, which XC8 emits into every translation unit that
includes the header and then warns about three times (2053, "never called").
It is an ordinary function in `decode.c` now. The hex is byte-for-byte the same
size, so the compiler was inlining it anyway.

CI does the same build on every push with the same pinned XC8 **and the same
pinned pack**, and the two were checked against each other rather than assumed
to agree: the `canfuel-hex` artefact from the first green run is byte-for-byte
the desk's `mplab/build/canfuel.hex`, once the CRLF the Windows build writes is
normalised away. If they ever disagree by more than that, the difference is the
machine, not the code.

Getting that green run also took one fix on CI's side alone. The `install XC8`
step carried `--netservername ''` from the v2.50 pin; v4.00's installer has no
such option and, being InstallBuilder, treats an unknown one as fatal rather
than ignoring it — three runs failed before compiling a line. It was passing an
empty value, so it had never configured anything anyway.

### What to do next — `docs/install.md`, and only there

**The next action is step 4 of `docs/install.md`.** That document is the plan
now, and it carries its own progress column; steps 1 to 3 are done and step 4
is waiting on the boards, expected in the week of 2026-08-17.

**Do not restate the plan here, and do not add a "next session" section
anywhere else.** Two copies of a procedure diverge, and the copy nobody reads
is the one that stays wrong. When something is finished, tick it in
`install.md`. What belongs in this file is *why* the order is what it is —
which the procedure itself cannot carry:

**Loopback is the step that gets skipped and must not be.** It costs ten
minutes, needs no bus and no transceiver at all (DS39977C §27.3.5 hands the
transmit buffers straight to the receive buffers), and it exercises the bit
timing, all six filters, the FIFO, the access-bank window, `txframes` and
`decode`. A fault caught there costs a reflash; the same fault in Normal mode
puts error frames on the car's bus.

**Why Listen Only touches the car before Normal:** the 500 kbps bit timing is
arithmetic no hardware has run, and a Normal-mode node with wrong timing does
not merely fail to read the bus, it **corrupts** it. Listen Only is silent by
the module's own guarantee (§27.3.4). Check `hal_can_rx_errors()` /
`hal_can_tx_errors()` before anything else — a timing fault shows there long
before it shows anywhere else.

JP2 off before programming and back on afterwards; JP1 fitted or the LEDs stay
dark by design. `LED_PWR` blinking slowly means a silent build, which is
correct for loopback and listen-only and a mistake in a normal one.

### Local toolchain

gcc, make, git and Python 3.11 are installed, and as of **2026-08-09** so are
MPLAB X v6.00 and XC8 v4.00 — the latter at
`C:\Program Files\Microchip\xc8\v4.00\bin\xc8-cc`, **not on the PATH**, which
`mplab/Makefile` handles by falling back to that path.

`PIC18F-K_DFP 1.13.292` is unpacked at **`C:\mchp_packs`**, deliberately
outside the home directory — see point 4 above. It is 380 MB and not in any
backup; if it goes missing, re-download the `.atpack` and unzip it there.

MPLAB X finds its own toolchain regardless of PATH, so the IDE building is not
evidence that `make -C mplab` will. Nor, on this machine, the reverse: the IDE
manages its own packs and has not been made to build this project. `make` is
the build.

**The `TMP` quirk is fixed and no longer needs a workaround.** In this shell
`make` hands its recipes an empty `TMP` and the MSYS2 gcc then tries to write
its temporary files into `C:\WINDOWS` and is refused. Every invocation used to
have to be spelled `make -C test TMP="$TEMP" test`, which was easy to forget
and — being a shell variable — impossible for any tool to allow-list. Since
2026-08-12 `test/Makefile` derives it itself with the same two lines
`mplab/Makefile` has used since 2026-08-09:

```make
CYGPATH := $(shell command -v cygpath 2>/dev/null)
ifneq ($(CYGPATH),)
export TMP := $(shell cygpath -m /tmp)
endif
```

`cygpath` exists only on MSYS and Cygwin, so it is self-guarding and leaves
Linux, macOS and CI alone. **Plain `make -C test test` now works.**

---

## The board exists now, and it fixes the pin assignment

**Three boards were ordered from Gatema PCB on 2026-08-09** and are expected
during the week of 2026-08-17. The design is finished, checked and frozen: what
is being manufactured is commit `c06e710` of the sibling `kicad` repo. **They
are now the only thing the project is waiting on** — the firmware, the display
configuration and the harness are all done, so the boards arriving is what
unblocks step 4 of `docs/install.md`. The pinout below is not provisional and
`hal_can.c` and `hal_sys.c` are written against it.

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

## The decisions behind the HAL

All of these are now implemented in `src/hal_can.c`, `src/hal_sys.c` and
`src/pic_config.h`, and each of them appears again as a comment next to the
code it produced. This section is the index; the code is the detail.

Everything below that carries a citation was read out of
`docs/pic18f25k80-datasheet.pdf` (DS39977C) or `docs/mcp2562-datasheet.pdf`
(DS20005167C). Everything without one is a **decision**, not a specification,
and says so. Do not promote a decision to a specification without opening the
PDF.

**`CANMX` is 1, and the chapter text says the opposite.** DS39977C Register
28-5 (CONFIG3H, byte address 300005h) defines bit 0:

> `1` = CANTX and CANRX pins are located on RB2 and RB3, respectively
> `0` = CANTX and CANRX pins are located on RC6 and RC7, respectively

The board is wired to RB2/RB3, so the bit is **set**, which is also the reset
default. But §27.1's opening paragraph says the pins "can be placed on
alternate I/O pins by *setting* the CANMX Configuration bit" — which is
backwards. The register table and the pin-table footnote ("Default pin
assignment for CANRX and CANTX when the CANMX Configuration bit is set") agree
with each other against the prose, so the table wins.

**The ECAN chapter is §27, not §22.** Earlier revisions of this file said §22
throughout; that is the chapter number from an older PIC18 CAN datasheet and it
does not carry over. In DS39977C: §27.1 module overview and the six-step
initialisation sequence, §27.3 modes, §27.4 functional Mode 0/1/2, §27.5
buffers, §27.9 baud rate, §27.15 interrupts.

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

**VddConv, and what it is honestly worth.** Read the band gap on ADC channel 31
(DS39977C Register 23-1: *"11111 = Channel 31 (1.024V band gap)"*) against VDD
as the converter's reference, and invert:

```
VDD = 1.024 × 4096 / code
```

**4096, not 1023.** Earlier revisions of this file and of `docs/frames.md`
carried `1.024 × 1023 / ADC`, which is the ten-bit formula from a different
PIC. This A/D is twelve bits — DS39977C Table 31-25 parameter A01,
`NR Resolution ... 12 bit` — and §23.5 confirms it: *"The A/D conversion
requires 14 TAD per 12-bit conversion."* The ten-bit formula would have
reported four times the real supply, and 20 V on the display is exactly the
kind of wrong that gets blamed on the wiring.

Three things the datasheet says about it, and none of them are flattering:

- the reference is **1.024 V with no tolerance given at all** — the figure
  appears only in the channel list of Register 23-1, and Section 31.0 has no
  min, typ or max for it. So VddConv is a trend and a sanity check, not a
  calibrated voltmeter. An absolute reading needs a per-unit constant.
- Table 31-25 parameters A01 and A50 specify the twelve-bit resolution **only
  for VREF ≥ 3.0 V**, and VREF here is VDD. Below 3 V the number stops meaning
  anything, which is why `BORV` is now 3.0 V rather than the sibling projects'
  1.8 V.
- Table 31-11 parameter 36, TIVRST: the internal reference takes **25 µs typ**
  to become stable. `adc_init()` waits 50 µs once, rather than before every
  conversion.

Clock and acquisition, from Table 23-1 and Table 31-26: `ADCS<2:0> = 101`
(FOSC/16) gives TAD = 1 µs at 16 MHz, inside parameter 130's 0.8–12.5 µs and
inside the 20 MHz that Table 23-1 allows for 16 TOSC; `ACQT<2:0> = 100`
(8 TAD) is 8 µs against the 2.45 µs Equation 23-3 works out and the 1.4 µs of
parameter 135.

Returned as `uint16_t hal_sys_vdd_c(void)` in 0.01 V, which is what
`txframes_gather()` takes.

**MCP2562.** DS20005167C: the `STBY` pin is the standby control (§1.7.9) and on
this board it is hard-wired to ground, so there is no line to drive and no
standby mode to write. `VIO` exists only on the MCP2562, not the MCP2561, and
here it is tied to VDD — so the digital levels are plain 5 V and no level
shifting is involved.

**RB2 idles high, and it is not cosmetic.** RB2/CANTX drives the MCP2562's
`TXD`, which is **active low**: a driven-low TXD is a request to hold the bus
dominant. `ports_init()` used to write `LATB = 0x00`, so from power-up until
`hal_can_init()` ran — several milliseconds later, `persist_load()` scans the
whole EEPROM ring in between — the transceiver was being asked to jam the bus.
DS20005167C §1.5 is the backstop rather than the excuse: it detects a
"Permanent dominant condition on TXD" and disables the CANH and CANL drivers
"in order to prevent the corruption of data on the CAN bus", but only after
tPDT, 1.25 ms typical (Table 1-4 parameter 11), which at 500 kbps is over six
hundred bit times. `LATB` is `0x04` now, and `hal_can_init()` sets the bit
again before it touches the module.

It matters a third time in Loopback, where §27.3.5 says "The TXCAN pin will
revert to port I/O while the device is in this mode" — so there `LATB2` is the
only thing keeping a fitted transceiver off the bus.

**Three ECAN modes, chosen at build time.** `HAL_CAN_MODE_NORMAL` is the
converter; the other two exist so that the first contact between this firmware
and a real 500 kbps bus is not a node that has already started acknowledging
frames. The values of `hal_can_mode_t` *are* the `REQOP<2:0>` codes of Register
27-1, so there is one table and not two that can drift.

- **`LISTEN_ONLY`** (`011`) — §27.3.4: "a silent mode, meaning no messages will
  be transmitted while in this state, including error flags or Acknowledge
  signals". Receives and filters exactly as normal. This is the point: a
  Normal-mode node with wrong bit timing does not merely fail to read the bus,
  it corrupts it, and our bit timing is arithmetic no hardware has run.
- **`LOOPBACK`** (`010`) — §27.3.5: the transmit buffers are delivered to the
  receive buffers "without actually transmitting messages on the CAN bus", so
  the whole path can be exercised with no bus and no transceiver at all.

Selected with `make -C mplab CAN_MODE=LISTEN_ONLY` (or `LOOPBACK`), which
defines `CAN_START_MODE` over the default in `config.h`. A build flag rather
than an edit, so a diagnostic hex leaves nothing in the tree to commit by
accident; a misspelled mode is a compile error rather than a silent normal
build. **It is deliberately not the `DBG_EN` jumper** — JP1 means "the LEDs may
light", which is as useful while transmitting as while listening, so the two
have no reason to move together.

`hal_can_send()` refuses up front in Listen Only rather than setting `TXREQ` on
a frame that can never complete and leaving all three buffers busy for ever.
Loopback does queue, because delivery to our own FIFO is the whole point of it.

**LEDs.** `LED_PWR` on RC0 and `LED_CAN` on RC1, active high through 1 kΩ, and
only when `DBG_EN` (RA0) is high. Nothing lights up in the car. **RA0 is AN0,
so it has to be switched to digital before it is read** — left analogue it
reads zero and the LEDs simply never work, a bug that looks exactly like a
wiring fault. The pin assignment itself comes from the board section below,
which is sourced from `kicad`.

`LED_CAN` carries the bus state (steady = healthy, 2.5 Hz = errors or an
overflow, 5 Hz = the module never reached its mode, dark = quiet bus).
`LED_PWR` is steady in a normal build and **blinks slowly in either silent
mode** — without that, a listen-only hex left in the device by accident is
indistinguishable from a transmitter that has quietly stopped working: frames
arrive, `LED_CAN` is steady, and the display just shows nothing.

**Which frames to receive, and in which functional mode.** The six
`CAN_ID_*` identifiers in `config.h`, and **only identifiers something
consumes** — a filter is a hardware resource and a decoded field nobody reads
is dead weight. 0x5A0 was accepted until 2026-08-11 and was dropped for exactly
that reason: nothing in the firmware read the acceleration, and the display
takes 0x5A0 off the bus itself. Fourteen identifiers are broadcast
periodically and the bus carries 682–727 frames a second; the six we keep are
357 of them, so hardware filtering throws away slightly more than half the bus
reads and half the FIFO pressure before they cost anything.

**Mode 2 rather than Mode 0, and the reason is depth, not filter count.** That
used to rest on two arguments and one of them has since gone away, which is
worth saying rather than leaving the stale reasoning to be found later. With
seven identifiers, Mode 0's "Six acceptance filters, 2 for RXB0 and 4 for RXB1"
(DS39977C §27.4.1) was one short and settled it on its own. Six fit.

What still settles it is that **Mode 0 has two receive buffers and Mode 2 forms
a FIFO out of all eight** (§27.4.3). The six identifiers arrive at **3.58 per
10 ms**, measured off the `_z1` fixtures and near-identical at idle, at 2586 rpm
and over six minutes of driving. Two buffers against that is a coin toss on
every pass, and it collapses entirely during the once-a-minute EEPROM write
that blocks for ~48 ms. The sixteen filters are now a convenience; the FIFO is
the requirement.

The FIFO is read through `FP<3:0>` in `CANCON` and the access-bank window in
`ECANCON`, per §27.15.1. **That window is a loaded gun**: in Mode 1 and 2,
`ECANCON<4:0>` decides which buffer the addresses the header calls
`RXB0CON..RXB0D7` actually refer to. Every function in `hal_can.c` that touches
an `RXB0*` name sets `EWIN` first, in the same breath. Forget it once and you
read a message out of an acceptance filter, or write a transmit frame into one.
`EWIN` resets to `10000` (Receive Buffer 0), which is why `ECANCON` is set to
`0x90` and not `0x80`.

**Configuration bits — `src/pic_config.h`, started from `CanSwitch.X/config.h`.**
That file is a working PIC18F25K80 configuration at a 16 MHz crystal, and most
of it transfers unchanged: `PLLCFG = OFF`, `XINST = OFF` (XC8 requires it),
`MCLRE = ON`, `STVREN = ON`, `IESO = OFF`, `FCMEN = OFF`, `PWRTEN = ON`, all
the code and table protection off.

Four bits differ, and one that does not differ is load-bearing here in a way it
was not there:

| Bit | CanSwitch | canfuel | Why |
|---|---|---|---|
| `CANMX` | `PORTC` | **`PORTB`** | this board is wired RB2/RB3 |
| `WDTEN` | `OFF` | **`ON`** | see below |
| `WDTPS` | `1048576` | **`512`** | 4 ms × 512 = 2.048 s |
| `BORV` | `3` (1.8 V) | **`0`** (3.0 V) | the A/D is only specified above 3.0 V |
| `BOREN` | `NOSLP` | **`ON`** | we never sleep, so the distinction is empty |
| `RETEN` | `ON` | **`OFF`** | likewise — it only controls the sleep regulator |
| `SOSCSEL` | `DIG` | `DIG` | **unchanged and critical**, see below |
| `FOSC` | `HS1` | `HS1` | 16 MHz is the top of HS1 and the bottom of HS2 |

**`SOSCSEL = DIG` is the quiet one.** DS39977C Register 28-1:
`10 = Digital (SCLKI) mode; I/O port functionality of RC0 and RC1 is enabled`.
Pins 11 and 12 of the 28-pin part are `RC0/SOSCO/SCLKI` and `RC1/SOSCI` — which
are exactly the two LED pins. Without `DIG` the LEDs belong to the secondary
oscillator and simply never light, and the symptom is indistinguishable from a
dry joint. It is inherited rather than chosen, but it must not be lost.

**`WDTEN = ON`, decided rather than inherited.** Both siblings run with the
watchdog off, which is reasonable for a light switch: a wedged one gets noticed
and power-cycled. A converter behind an air vent does not, and it is feeding a
display the driver is reading. The longest the main loop can go without a
`CLRWDT()` is one EEPROM record — twelve bytes at the 4 ms typ of Table 31-1
D122, about 48 ms, once a minute. `WDTPS = 512` gives 2.048 s, forty times
that, so only a real hang can trip it.

**`BORV = 0`, likewise decided.** Table 31-25 parameters A01 and A50 specify
the A/D's twelve-bit resolution only for VREF ≥ 3.0 V, and VREF is VDD. Below
3 V the converter would keep running and keep transmitting numbers that are no
longer specified. Resetting is the better failure.

`CANMX = PORTB` / `PORTC` is also the answer to the pragma spelling. Their
comment on `PORTC` reads "ECAN TX and RX pins are located on RC6 and RC7",
which agrees with Register 28-5 and against the §27.1 prose — a third
independent confirmation of the reading above.

**`T3CKMX` and `T0CKMX` are deliberately absent.** DS39977C Register 28-5 note
1: they are "implemented only on the 64-pin devices ... Maintain as `0' on
28-pin, 40-pin and 44-pin devices", and both default to `1`. On this part they
do nothing, and the XC8 keyword for the `0` state could not be verified against
a device header from a machine without XC8 — so the documented default was kept
rather than a keyword guessed. Neither sibling sets them either.

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

**500 kbps works out to BRP = 0 and needs no cleverness.** DS39977C Equation
27-3 gives `TQ (µs) = (2 × (BRP + 1))/FOSC (MHz)` and Register 27-52 allows
`BRP<5:0> = 000000 → TQ = (2 × 1)/FOSC`. At 16 MHz that is TQ = 0.125 µs, and
piclib's fixed 16 TQ bit time gives 2 µs — exactly 500 kbps.

`piclib`'s own formula, `BRP = (1000 × cpuSpeed)/(32 × baudRate) − 1`, returns
0 for `can_setupBaudRate(500, 16)`, so the call is simply correct. Note it
wants the **oscillator** frequency, not the instruction rate.

**The segment split is not piclib's, though.** piclib uses SYNC 1 + PROP 4 +
PS1 8 + PS2 3, and so did this firmware until the round trip was worked out.
It is now **SYNC 1 + PROP 7 + PS1 5 + PS2 3 = 16 TQ, SJW 2** — the same 16 TQ,
the same 81.25 % sample point, `BRGCON1/2/3 = 0x40 / 0xA6 / 0x82`. Three TQ
moved from Phase_Seg1 into Prop_Seg, which is the segment that pays for the
signal's round trip and for reflections off an unterminated stub:

- **Round trip.** DS39977C §27.9.4, with DS20005167C §2.3 parameters 4
  (125 ns) and 6 (110 ns): `Prop_Seg ≥ 2 × (235 ns + 5 ns/m × L)` allows
  **L ≤ 3.0 m** at 500 ns and **L ≤ 40.5 m** at 875 ns. Three metres is not a
  comfortable budget for a bus running from the engine bay to the dashboard.
- **Stub.** The board hangs on an unterminated stub of **about 1.4 m of
  CANH/CANL from the instrument cluster** to the air vent — measured as
  1.3–1.4 m, and 1.4 m is the figure carried everywhere, deliberately the
  pessimistic end. **It stays an estimate on purpose**: refining it means
  taking the dashboard apart again, and at 3.5 m allowed the margin swallows
  the difference. Both 120 Ω terminators are elsewhere in the car; **60.1 Ω
  measured** across CANH/CANL says so, and is also why R5 stays unfitted.
  onsemi AND8376/D's `L_STUB_MAX ≤ T_PROP_SEG/(50 × T_PROP(BUS))` gives 2.0 m
  at the old split and 3.5 m at this one, so the margin goes from 1.4× to
  2.5×. An application note about somebody else's transceivers is evidence,
  not a specification — but it points the same way the datasheet arithmetic
  above does.

SJW = 2 rather than §27.11's "typically 1": we are one node among many whose
oscillators we neither built nor can measure, the ISO 11898-1 bound
`df ≤ SJW/(2 × 10 × NBT)` doubles from 0.31 % to 0.63 %, and the only price is
`Phase_Seg2 ≥ SJW`, which 3 ≥ 2 pays with room. The full derivation, with
every citation, is the comment block above `BRGCON1_500K` in `hal_can.c`.

All of which is arithmetic. `CanSwitch.X` passes `BAUD_RATE 50`, so BRP = 0
and the whole 500 kbps path have been exercised by nobody — the first real
test of it is a converter listening to the car. Expect to check the ECAN
error counters early rather than assuming the sums carried.

**`piclib` was read closely and then not used. That reverses what this file
used to say**, which was that it would be added as a submodule.

It was the right place to start and it settled the register sequences. But
consuming it turned out to cost more than writing the twenty lines it would
have saved:

- `can.c` is **Mode 0 only** — one transmit buffer, two receive buffers, six
  filters. We need an eight-deep FIFO, so Mode 2, which `can.c` has no notion
  of. (Its six filters would now hold our six identifiers, but its two receive
  buffers still would not hold the traffic.)
- Its API is not "send this identifier": it is a `CanHeader` of
  `messageType`/`nodeID` that `can_headerToId()` packs into the eleven bits in
  a scheme belonging to the house lighting protocol. Our identifiers are
  numbers off a VW bus.
- `can_initRcPortsForCan()` is hard-wired to the wrong pin pair for this board.
- `can.h` **defines** `MessageStatus messageStatus;` and `byte filterCount = 0;`
  in the header rather than declaring them — one translation unit only by
  luck.
- `dao.c` is shaped around 16-bit values in numbered buckets; `persist.c` wants
  arbitrary byte addresses.

So `hal_can.c` and `hal_sys.c` are written directly against DS39977C, and
**this repository has no submodules**. `piclib`'s EEPROM layer is still exactly
the right shape to have copied the *sequence* from — `EEADRH:EEADR` addressing
over the full ten-bit range, the `0x55`/`0xAA` unlock, `WREN`, polling `WR` —
and `hal_eeprom_write()` follows the same steps with the datasheet's Example
8-2 open beside it.

### The three questions this file used to leave open, and how they were decided

**Which timer makes the millisecond: Timer2.** `CanSwitch.X` uses Timer0 in
16-bit mode with a 1:16 prescaler, but only for a coarse debug heartbeat.
Timer0 would need a software reload every interrupt and would drift by the
latency of each one. Timer2 has a period register and reloads itself
(DS39977C §15.0, Register 15-1), and the chain divides exactly:

```
FOSC/4 = 4 MHz          250 ns per timer clock
prescale 1:4            1 µs per count      T2CKPS<1:0> = 01
PR2 = 249, so 250       250 µs per match
postscale 1:4           1000 µs per interrupt   T2OUTPS<3:0> = 0011
```

No remainder and nothing to drift. Timer2 clashes with nothing here — the CCP
and MSSP modules that could claim it are unused.

**Interrupt or polling for receive: polling, and it is not close.** Functional
Mode 2 turns all eight receive buffers into one FIFO (§27.4.3), and the seven
identifiers we accept arrive at roughly four frames per 10 ms. `main.c` drains
the FIFO **every loop pass**, not on a 10 ms slot, which leaves something like
a twenty-fold margin. An interrupt would buy nothing and would cost the one
thing that is genuinely awkward: the receive path and the transmit path both
steer the `ECANCON` access-bank window, and there is no lock available between
an ISR and the main loop.

The one place frames really are lost is the once-a-minute EEPROM write, which
blocks for about 48 ms. That was checked rather than waved away — the fuel
counter delta is `(new − old) mod 32768` so a gap costs nothing, distance is
integrated against the clock rather than against frame arrivals, and the clock
keeps running because `hal_eeprom_write()` re-enables interrupts the instant
the unlock sequence is over. `main.c` clears the resulting overflow flag so the
LED keeps meaning something.

**Whether the watchdog goes on: yes.** Argued in the configuration-bit table
above.

### One deliberate deviation from the datasheet, in `hal_eeprom_write()`

DS39977C Example 8-2 marks `BCF INTCON, GIE` … `BSF INTCON, GIE` as part of the
**Required Sequence**, with `GIE` staying clear across the `WR` poll as well as
across the unlock. **We restore `GIE` the instant `WR` is set**, and poll with
interrupts on.

Why: the poll is 4 ms typ per byte (Table 31-1, D122) and a record is twelve
bytes, so following the example literally would hold interrupts off for ~48 ms
once a minute. The only interrupt in this firmware is the millisecond clock,
and that clock is what every accumulator in the core is integrated against —
losing 48 ms of it per minute is a silent 0.08 % error in distance and in the
trip average.

Why it is safe: the sequence the datasheet actually requires is "write 55h to
EECON2, write 0AAh to EECON2, then set WR bit" (§8.4), and that is fully
bracketed. §8.4 also states that "after a write sequence has been initiated,
EECON1, EEADRH:EEADR and EEDATA cannot be modified", so nothing an interrupt
could do disturbs a cycle in flight.

The watchdog is deliberately **not** cleared inside that poll. If `WR` never
clears the hardware is broken and a reset is the right outcome; a `CLRWDT()`
there would turn it into a permanent hang.

**The millisecond clock itself, whatever timer feeds it.** One free-running
`uint32_t`, exposed as `uint32_t hal_sys_millis(void)`. Read it once at the top
of each scheduler pass and hand that one value to every core call in the pass —
reading it repeatedly can straddle a millisecond and hand the core a tick of
zero where it expects one. `main.c` does exactly that and should keep doing it.

It must be read atomically against the interrupt that writes it, and four bytes
on an eight-bit machine are not one instruction: `hal_sys_millis()` clears
`GIE` around the read and **restores** it rather than forcing it on, because it
is also reachable from inside the EEPROM write path. This is a software
decision, not a datasheet one.

---

## `docs/refuted.md` — read it before reintroducing a good idea

Everything this project believed and got wrong, across all three
repositories, with what refuted it. It exists because a refuted idea is a
*plausible* idea, and several of the entries are things anyone reasoning from
first principles would propose again: an escape header for the unused pins, an
enclosure, a submodule for `piclib`, reading the tank level straight off the
bus, resetting the trip from the instrument cluster.

Two rules for it. **Only settled-against things go in** — questions live in
`can-decoding.md`. And **nothing is ever deleted from it**; if new evidence
un-refutes an entry, say so inside the entry.

`can-decoding.md` sorts its questions three ways and the distinction is worth
keeping straight, because all three look similar from a distance:

| Where | What it means |
|---|---|
| `refuted.md` | believed, then **settled against**. An answer exists and it is "no" |
| `can-decoding.md` → *Resolved questions* | asked and **answered**, with the evidence kept |
| `can-decoding.md` → *Never resolved but not required* | **no answer, and none wanted.** Do not work on these |
| `can-decoding.md` → *Open questions* | genuinely open **and worth the effort**. There is one |

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
  main.c        scheduler and glue — the only place it all meets
  decode.c/.h   frame parsing          PURE C
  compute.c/.h  maths                  PURE C
  txframes.c/.h frame assembly         PURE C
  persist.c/.h  EEPROM circular buffer PURE C
  divconst.h    division by a constant  PURE C -- read docs/optimisation.md
  fastmul.h     wide multiplication     PURE C -- read docs/optimisation.md
  hal_can.c/.h  ECAN + MCP2562
  hal_sys.c/.h  timer, ADC, LEDs, jumper, EEPROM
  pic_config.h  the #pragma config bits, and only those
  config.h      every constant and switch
test/
  tt.h          the test framework, small enough to read at a sitting
  logread.h     the fixture parser in C, the counterpart of canlog.py
  replay_core.h one log through decode + compute, mirrors replay.py's loop
  sched.h       one log through the core AS main.c DRIVES IT -- a clock, the
                slots, and the EEPROM write as a blocking gap that loses frames
  replay_host.c the binary behind replay.py --host-build
  test_*.c      decode, compute, txframes, persist, divconst,
                scheduler (rate and jitter invariance), props (fuzz + invariants)
  xc8stub/xc.h  a fake device header, for `make check-hal` and nothing else
mplab/
  Makefile      the authoritative device build, drives xc8-cc — CI runs this
  canfuel.X/    the MPLAB X project, for editing and for driving a PICkit
  README.md     how to build, and what JP2 is for
tools/          canlog.py, replay.py — Python, runs anywhere
                cycles.py — cycle budgets out of the XC8 listing, a CI gate
```

**The two `config` headers must not be confused.** `src/config.h` is the pure
core's constants and must never see `<xc.h>`. `src/pic_config.h` is the
`#pragma config` block, includes `<xc.h>` itself, and is included only by
`main.c`, `hal_can.c` and `hal_sys.c`. `make check-pure` enforces the first
half of that mechanically.

`tt.h`, `logread.h` and `replay_core.h` are header-only on purpose: the
Makefile builds one `test_*.c` against the core and nothing else, so a helper
that needed its own object file would mean touching the build rule every time.

Constants belong in `config.h`, not in the code. In particular
`FUELNOW_LH_BELOW_MMH`, `FUELNOW_CLAMP_D`, `REFUEL_RISE_L` and the frame
periods.

**This repository has no submodules.** An earlier revision of this file planned
to add `github.com/PoJD/piclib` as one; that was reconsidered while `hal_can.c`
was being written and the reasoning is in the HAL section. Clone `piclib` and
`can` beside this repo when you want to read them — they are still the best
reference there is for these registers on this silicon.

---

## Tools

**`pyserial` is the project's only third-party dependency**, and only
`usbtin_capture.py` uses it (`pip install pyserial`). Everything else — the
tests, the replay, the cycle budgets — is standard library, which is why there
is no `requirements.txt` and should not be one for a single package.

```
python tools/usbtin_capture.py --seconds 60 --out idle_z1.txt   # record, Z1 on
python tools/canlog.py test/fixtures/03_drive.txt          # per-ID summary
python tools/canlog.py --dump --id 0x480 FILE              # print frames
python tools/replay.py --every 100 test/fixtures/07_accel.txt
python -m unittest discover -s tools -p "test_*.py"        # 80+ tests

make -C test test                                          # 400+ checks
make -C test check-pure                                    # no <xc.h> in the core
make -C test check-hal                                     # the HAL still compiles
make -C test sanitize                                      # ASan + UBSan, CI only
python tools/replay.py --host-build test/fixtures/*.txt    # Python vs C
python tools/cycles.py                                     # cycle budgets
python tools/cycles.py --check                             # ...and fail if over

make -C mplab                                              # -> build/canfuel.hex
make -C mplab CAN_MODE=LOOPBACK                            # talks to itself
make -C mplab CAN_MODE=LISTEN_ONLY                         # never ACKs
```

`tools/replay.py` is the reference decoder in Python, written against the same
table as `decode.c` and `compute.c`. `--host-build` runs
`test/build/replay_host` over the same logs and diffs the totals; the fuel
counter and the restart count must agree exactly, distance to within a tenth of
a percent. It is a CI step, so the two cannot drift apart quietly.

`tools/test_replay.py` and `test/test_compute.c` are deliberately twins — same
fixtures, same expected numbers, one in floats and one in scaled integers.
**A change to the maths belongs in both.**

`make -C test check-hal` is the counterpart of `check-pure`, pointing the other
way: it compiles `hal_can.c`, `hal_sys.c` and `main.c` with gcc against
`test/xc8stub/xc.h`. **That stub is not a device header and proves nothing
about the hardware** — it declares exactly the registers the code happens to
name, so it agrees with the code by construction. What it does prove is that
the C is valid and that `main.c` calls the core correctly, which is worth
having on a machine with no XC8.

### Before committing anything that touches the core

The five commands above, in that order. All of it runs in under fifteen
seconds and it is exactly what the `tools` and `core` CI jobs do, so a green
run here means a green run there — the `firmware` job needs XC8 and only runs
on GitHub. No `TMP=` prefix is needed any more; see the toolchain section.

Adding a `test_*.c` needs no Makefile change — the glob picks it up, builds it
against all four core sources and runs it.

### Two test files that exist because the others share a blind spot

`test_compute.c`, `test_txframes.c` and `tools/test_replay.py` all compare the
C core against the Python reference over the same seventeen recordings. That is
a strong check with one hole in it, and the hole cost a **6.4 % error in every
distance the device would have reported**: the two implementations were written
from the same table by the same reasoning, so a mistake in the reasoning is a
mistake in both and the diff stays clean. **Twin implementations do not catch a
fault they share.** Worse, all of them drive the core off the 0x480 frames, one
`compute_tick()` per fuel frame ~38 ms apart, while `main.c` calls it every
~100 µs — so anything that depends on *how often* the core is called was
invisible by construction.

- **`test_scheduler.c`** (with `sched.h`) drives the core the way `main.c`
  does: a millisecond clock, the 100 ms and 1 s slots, and the once-a-minute
  EEPROM write simulated as a 48 ms blocking gap that really loses frames. Its
  properties are the ones an oracle cannot express — the answers must not
  depend on the tick rate or on its jitter, `total_ul` must equal an
  independently computed sum of deltas, and the EEPROM blindness must cost
  exactly zero microlitres, which `main.c` had asserted in a comment and
  nothing had ever tested.
- **`test_props.c`** states things that must be true of the arithmetic itself
  and attacks them with inputs no fixture contains: ten thousand fuzzed states
  through every getter (a getter that divides by something reachable-zero does
  not return a wrong number here, it takes SIGFPE and the test dies), totals
  that may only move forward unless a refuelling zeroed them, a repeated frame
  that must add nothing, an invalid speed that must invent no metres.

**Fuzz reachable states only.** The generator builds a torque byte times
`TORQUE_CNM_PER_BIT` rather than an arbitrary `uint16`, a tank level masked to
seven bits, a quarter-rpm count `decode.c` could really have written. Going
beyond that manufactures failures nobody can reach and teaches the next reader
to ignore the test. The same rule fixes the DLC fuzz at 0..8: `hal_can_receive`
masks the length to four bits into an eight-byte buffer, so a longer one is not
something the hardware can hand to `decode_frame()`.

**`make -C test sanitize` runs the whole suite again under ASan and UBSan**, so
those 50,000 malformed frames and 10,000 fabricated states go through a checker
rather than only through assertions somebody remembered to write. It is
insurance against the next change and is expected to stay silent — the two
arrays that could plausibly have been indexed out of range were deleted on
2026-08-12. **It does not run on the maintainer's desk**: the MSYS2 gcc ships
neither `libasan` nor `libubsan`, so it is a CI step and `test/Makefile` says
so where somebody hitting the link error will find it.

---

## Fixtures

Real logs from the car. **Do not edit them.** The tests reference exact numbers
from them.

⚠ **Only the three `_z1` logs have trustworthy time**, recorded 2026-08-11 with
`tools/usbtin_capture.py`. `06_trip_reset` and `07_accel` carry USBtinViewer's
host timestamps and are **wrong by about a factor of two**; the other five carry
no time at all, and the 49.5 ms period that used to be used to synthesise one
**does not exist** — see questions 1 and 9, both resolved. Fuel totals are unaffected
everywhere, because the counter is absolute; it is durations, flows and
distances that need a clock.

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

⚠ **The counter column is measured. The other three are not.** Duration, flow
and distance for these seven all rest on a clock that was either the host's
(`06`, `07`) or synthesised from a 49.5 ms period that turns out not to exist
(the rest). They still pin the two implementations against each other, which is
what the tests use them for, but they are not facts about the car. The
measured warm idle, taken with adapter timestamps on 2026-08-11, is:

| Log | Counter | Duration | Flow | Conditions |
|---|---|---|---|---|
| `09_idle_60s_z1` | 19,561 µl | **60.03 s** | **326 µl/s = 1.17 l/h** | 796 rpm, A/C off |
| `10_rev2600_z1` | 17,544 µl | 19.76 s | 888 µl/s | 2586 rpm, **A/C on** |

---

## The torque calibration, and what is still soft about it

**For what to do next, see `docs/install.md`** — it is the plan and it tracks
its own progress. Nothing here restates it.

Two calibrations are approximate and both need the car: **the tank**, which
wants a known quantity from a jerrycan, and **the drag line on hot oil**, which
is the one open question in `docs/can-decoding.md`. Both are refinements to a
working device rather than blockers, and both live in `install.md` under
*Then: calibration*.

The rest of this section is why the drag line and the torque scale are what
they are, because that reasoning has nowhere else to live.

**The drag line was refitted on 2026-08-11 and the torque scale moved with
it.** It used to be a two-point line through `02_idle_60s` and `05_rev3000`,
both of which turned out to have been recorded on cold oil — 60.8 °C and
**39.0 °C**. It is now a least-squares fit through the four warm free-revving
holds `13`–`16` (72.8–76.6 °C, stationary in neutral, so net torque is zero and
b7 *is* the drag):

**The drag line was refitted on 2026-08-11 and the torque scale moved with
it.** It used to be a two-point line through `02_idle_60s` and `05_rev3000`,
both of which turned out to have been recorded on cold oil — 60.8 °C and
**39.0 °C**. It is now a least-squares fit through the four warm free-revving
holds `13`–`16` (72.8–76.6 °C, stationary in neutral, so net torque is zero and
b7 *is* the drag):

```
drag [Nm] = 6.74 + 0.00482 x rpm     was 19.52 + 0.0028 x rpm
```

Since the line is *subtracted* from indicated torque, the old one understated
torque and power: over `17_drive_property_z1` it displayed zero through 51 % of
the drive where this one displays a number through 78 %. Peak torque hardly
moves (105.8 → 107.0 Nm) — the whole difference is at part throttle.

**`TORQUE_CNM_PER_BIT` went 75 → 74 in the same breath, and had to.** Full
scale b7 = 255 must cover the rated crank torque *plus* the drag at that speed,
so the bracket the two factory ratings imply moves with the drag line: it was
0.745–0.773 Nm/bit and is now 0.736–0.738. At 0.74 the display reaches 85.4 kW
and 170.4 Nm against ratings of 85 and 170, where both used to land 3 % under.
**These two constants are one calibration — never move one alone.**

**The idle point is excluded from the fit, and the idle gate covers it.** b7
falls 24.96 → 18.81 between idle and 1536 rpm before it starts rising, because
idle is a regulated state with the throttle nearly shut, so no straight line in
rpm fits both. Idle is therefore *asserted*, not fitted. Raising the intercept
to compensate puts the line back above all four measured points and restores
the understatement — do not do it.

### The idle gate — fixed, and not to be relaxed

**A car standing still with the throttle shut shows zero torque and zero power.
This is a requirement, not a calibration.** Cold oil or hot, at whatever idle
speed the ECU picks, whatever a future drag refit does. It lives in
`compute_torque_d()` as

```c
if (speed_mmh <= IDLE_GATE_SPEED_MMH && throttle <= THROTTLE_REST) return 0;
```

and **six tests in `test_compute.c` plus two in `test_txframes.c` exist to stop
it being relaxed by accident** — the latter end to end off the real idle logs,
including `12_idle_ac_z1` where the air conditioning raises b7 from 25 to 42
and the display must still read zero. If one of them goes red, the fix is the
code, not the test.

Both thresholds are measured, and neither is an equality:

- **A standing car does not send zero.** 0x1A0 raw speed is **1** — 0.005 km/h
  — in every log while stationary (7953 frames of it in `06_trip_reset`), and
  the next value that ever appears is above 40. The gate is 0.1 km/h.
- **0x280 b5 is 38 at rest** and never lower in any log. It is the pedal, not
  the load — while driving, b7 reaches 133 with the throttle still at 38 —
  which is why the throttle **alone** cannot be a gate and is paired with
  standing still. Pulling away is throttle above rest while the car still reads
  1, so the gate releases before the car moves.

Supporting evidence, not a specification: SAE J1979 carries actual engine
percent torque (PID 0x62) and engine friction percent torque (PID 0x8E) as
separate standard PIDs — exactly indicated-minus-friction — and PID 0x64 gives
five reference points of which **the first is idle**, so the standard also
treats idle as its own datum rather than a point on a curve. `docs/frames.md`
has the citations.

The drag line is the **only open question left** in `docs/can-decoding.md` —
72–77 °C is warm, not the 95–110 °C of real driving, so it still probably
overstates drag slightly, which is the conservative direction. The questions
register was sorted on 2026-08-11 into what changes this firmware and what does
not; everything else is either resolved or parked.

**Why the scale is a decision at all, and why it is now parked.** 0x280
b7 is a percentage of a
reference torque inside the ECU, not Nm, and turning it into Nm needs a number
nobody here has. It was read at 0.67 Nm/bit — from "the AQY's maximum is
172 Nm, so 172/256" — until 2026-08-11, when that premise turned out to
contradict the fixtures it sits next to: at 2940 rpm in neutral the crank makes
nothing and b7 still reads 37, so b7 is *indicated* torque and its full scale
is the maximum *indicated* torque, not the maximum crank torque. Scaling to the
crank maximum and then subtracting drag counted the friction twice, and the
firmware could never have shown the 85 kW the car is sold with — it topped out
at 76.5 kW at 5200 rpm, at any throttle opening. **Nothing tested that**, which
is the part worth remembering.

It is now **0.74 Nm/bit**, a decision inside the bracket the two factory
ratings imply, with the ceiling pinned by two tests in `test_compute.c`. **The
measurement that was
supposed to settle it does not exist**: the VCDS session was run on 2026-08-11
and this ECU has no torque measuring block, only engine load in per cent, and a
full-throttle pull is deliberately not planned. The remaining uncertainty is
under 4 % and there is nothing to run, so the question is parked under *Never
resolved but not required* in `docs/can-decoding.md` rather than left open —
**do not plan that session again.** See `docs/frames.md` and the comment in
`config.h`.

The breadboard phase is skipped — Micro-Fit has a 3.0 mm pitch and does not
fit a breadboard. The boards themselves arrive during the week of 2026-08-17.
