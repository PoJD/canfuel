# canfuel — converter firmware

A fuel consumption converter for VW PQ34 cars with the AQY engine (2.0 l /
85 kW), developed and verified on a 2.0 AQY. It reads the powertrain CAN bus
(500 kbps), computes consumption, range, torque and power, and sends them back
onto the bus in frames 0x600–0x604. A CANchecked MFD15 Gen2 display renders
them from its own TRI file (repo `mfd15`). MCU: PIC18F25K80, 16 MHz, XC8. The
board lives in the `kicad` repo.

This file holds **the rules and where things are**. The reasoning behind each
hardware decision lives next to the code it produced (`src/hal_can.c`,
`src/hal_sys.c`, `src/pic_config.h`, `src/config.h`) and in `docs/firmware/`;
when this file and those disagree on a detail, read the code and fix this file.

*Condensed 28/10/2026 at the maintainer's request; the full previous version
is `git show bfbdd8d:CLAUDE.md`.*

---

## Language and address

**Everything in this repository is written in English** — code, identifiers,
comments, CLI help, documentation, commit messages, file names. Conversation
with the maintainer may be in Czech; nothing written to disk ever is.

**The maintainer is a man and is addressed informally**: in Czech *tykání*
and masculine forms throughout (*udělal jsi*, *naměřil jsi*).

---

## Sourcing hardware facts — manufacturer datasheets only

**Every register name, configuration bit, timing, endurance figure and
electrical limit comes from the manufacturer's datasheet for the exact part,
and from nothing else** — not forums, not application notes from memory, not
code from a previous project, not anybody's recollection, the model's
included.

- **Quote the source** next to every hardware constant: `DS39977C §2.7`,
  `DS39977C Table 31-1 D122`.
- The datasheets are in `docs/firmware/datasheets/`: `pic18f25k80-datasheet.pdf`
  (DS39977C) and `mcp2562-datasheet.pdf` (DS20005167C).
  `pdftotext -layout <pdf> -` makes them greppable.
- **Register tables outrank prose** (the CANMX case below). **Absolute
  Maximum Ratings outrank DC characteristics**, and both outrank what a part
  is seen to tolerate. **Typical is not guaranteed**: a *typ* with no min/max
  cannot be designed against — say so and what it costs.
- **Where the datasheet is deliberately not followed**, say so and why, next
  to the citation.
- **Where the datasheet does not settle it, decide and write the decision
  down as a decision** — what was chosen, over what, why. Never a plausible
  number dressed as a fact, and **do not queue questions for the
  maintainer**. If it genuinely needs information nobody has yet, say so in
  one line and carry on.
- ⚠ **The VCDS label file is deliberately not kept here** (Ross-Tech's,
  commercial). This project keeps its own summary of the blocks it uses, in
  `docs/engine-health/vcds.md`.

Facts about the *car* (signal table, frame periods, the bus already
terminated) are settled by measurement and marked as measured in
`docs/firmware/can-decoding.md`; the rule above is about parts.

**Working code from the sibling repos is evidence, not a source.**
`github.com/PoJD/can` (`CanSwitch.X`, `CanRelay.X`) and `github.com/PoJD/piclib`
run the same PIC18F25K80 at the same 16 MHz and are the right place to start a
register question — but they were bench-tested at **50 kbps**, ten times
slower, so their bit timing proves nothing at ours, and they carry deviations
that must not propagate: `CanSwitch.X/config.h` sets `CANMX = PORTC` (wrong
here), `can_initRcPortsForCan()` uses the same wrong pins, `piclib/can.c` never
writes `CIOCON.CLKSEL`. ⚠ **Check the caller before concluding a sibling got
something wrong** (`piclib/dao.c`'s GIE bracket is in `dao_saveDataItem()`).
Read them, check against the PDF, cite the PDF. Neither is a submodule;
**`piclib` was evaluated and not used** (Mode 0 only, a house-protocol API,
wrong pins, globals defined in a header).

---

## What this is, and where everything lives

**A complete firmware that builds clean**: `make -C mplab` →
`mplab/build/canfuel.hex` under XC8 v4.00, no warnings. Byte counts are not
quoted here; `README.md` carries a generated block.

```
src/
  config.h        every constant and switch           PURE
  decode.c/.h     frame parsing                       PURE
  compute.c/.h    maths                               PURE
  txframes.c/.h   frame assembly                      PURE
  persist.c/.h    EEPROM circular buffer              PURE
  divconst.h      division by a constant              PURE  (optimisation.md)
  fastmul.h       wide multiplication                 PURE  (optimisation.md)
  hal_can.c/.h    ECAN + MCP2562
  hal_sys.c/.h    Timer2 ms clock, band-gap A/D, LEDs, DBG_EN, EEPROM
  pic_config.h    the #pragma config bits, each cited
  main.c          the cooperative scheduler and nothing else
test/             tt.h, logread.h, replay_core.h, sched.h (header-only on
                  purpose), test_*.c (globbed), replay_host.c, xc8stub/xc.h
mplab/            Makefile (the authoritative device build, what CI runs),
                  canfuel.X (IDE), README.md (toolchain traps, JP2)
tools/            Python, standard library unless noted below
test/fixtures/    recordings from the car; README.md documents every one
docs/firmware/    everything the converter needs
docs/engine-health/  the car's own engine
```

**The two `config` headers must not be confused**: `src/config.h` is the pure
core's and never sees `<xc.h>`; `src/pic_config.h` is the `#pragma config`
block, included only by `main.c`, `hal_can.c`, `hal_sys.c`. Constants belong in
`config.h`, not in code.

**`docs/` has two folders and a document belongs to exactly one.**
Firmware documents may point at engine-health for context, never for a fact
they need; engine-health points at firmware freely.

- **`docs/firmware/`** — `install.md` (**the procedure**; it deliberately
  carries no progress — where the build is, is asked, not read),
  `can-decoding.md`, `frames.md` (all five frames and the torque/driving-gate
  reasoning), `refuel-reset.md`, `timing.md`, `optimisation.md`,
  `flashing.md`, `fuel-check.md`, `refuted.md`, `open.md`, `datasheets/`.
- **`docs/engine-health/`** — see *Engine health* below.

A one-shot procedure that has been followed is deleted; `git log` keeps it.

---

## Non-negotiable rule: a pure C core

`decode.c`, `compute.c`, `txframes.c` and `persist.c` **never include
`<xc.h>`**; `make -C test check-pure` enforces it. They take bytes and a
millisecond time and return numbers; `persist.c` reaches the EEPROM through
`persist_backend_t`. The whole core compiles with gcc and is tested against
real logs with no hardware. Hardware belongs only in `hal_can.c` and
`hal_sys.c`.

**No floating point anywhere in the core.** Every quantity is a scaled
integer named by its scale: `_UL` µl, `_MM` mm, `_MMH` 0.001 km/h, `_CNM`
0.01 Nm, `_D` tenths, `_C` hundredths. One µl per metre is exactly
0.1 l/100 km; v [0.001 km/h] × t [ms] ÷ 3600 = s [mm].

### The core's API — what `main.c` calls

```c
decode_state_t st; compute_t cp; persist_t ps; tx_values_t tx;

/* start-up */
decode_init(&st); compute_init(&cp);
persist_record_t rec;
if (persist_load(&ps, &hal_eeprom_backend, &rec))
    compute_restore(&cp, rec.total_ul, rec.total_mm,
                    rec.tank_stable_l, rec.tank_stable_valid);
/* a virgin EEPROM returns false: correct, not an error */

/* every received frame */
decode_frame(&st, id, data, dlc);
if (id == CAN_ID_FUEL)        compute_on_fuel(&cp, &st, now_ms);
else if (id == CAN_ID_ENGINE) compute_on_engine(&cp, &st, now_ms);

/* every pass: distance, tank, refuelling */
compute_tick(&cp, &st, now_ms);

/* every 100 ms */
txframes_gather(&tx, &cp, &st, hal_sys_vdd_c(), now_ms);
txframes_fuel(&tx, buf);   hal_can_send(CAN_ID_TX_FUEL,   buf, TXFRAME_DLC);
txframes_engine(&tx, buf); hal_can_send(CAN_ID_TX_ENGINE, buf, TXFRAME_DLC);

/* every second */
txframes_gather_trip(&tx, &cp, now_ms);
txframes_trip(&tx, buf);   hal_can_send(CAN_ID_TX_TRIP, buf, TXFRAME_DLC);
if (hal_sys_debug_enabled()) {          /* 0x603 only with JP1 */
    txframes_gather_diag(&tx, hal_can_rx_errors(), hal_can_tx_errors(),
                         hal_can_status(), flags, hal_sys_reset_cause(),
                         tx_fail, uptime_s);
    txframes_diag(&tx, buf); hal_can_send(CAN_ID_TX_DIAG, buf, TXFRAME_DLC);
}
txframes_gather_health(&tx, &cp, now_ms);   /* 0x604 always */
txframes_health(&tx, buf); hal_can_send(CAN_ID_TX_HEALTH, buf, TXFRAME_DLC);
persist_save(&ps, &rec, now_ms);            /* decides itself whether to write */
```

`persist_save()` carries the `PERSIST_INTERVAL_MS` rule (20 s, so at most
three times a minute), the only-on-change rule and the refusal to store an
empty record: call it every second and let it say no. `main.c` must **not**
clear the trip on refuelling, zero values on a quiet bus, or clamp to the
display's range — the core does all three. `now_ms` is free-running and may
wrap; never reset or clamp it. Read `hal_sys_millis()` once per pass and hand
that value to every call.

---

## The board — frozen

Sourced from `kicad/canfuel/docs/implementation-plan.md` §4.2, which wins on
any disagreement.

| Signal | Pin | Notes |
| --- | --- | --- |
| `CAN_TX` / `CAN_RX` | **RB2** (23) / **RB3** (24) | to MCP2562 pins 1 / 4 |
| `LED_PWR` / `LED_CAN` | **RC0** (11) / **RC1** (12) | 1 kΩ to an LED to ground, active high |
| `DBG_EN` | **RA0** (2) | JP1 to +5 V, 10 kΩ pull-down |
| `PGC` / `PGD` | RB6 / RB7 | ICSP header J3 (5 pins, no LVP) |
| MCLR | 1 | R6 470 Ω, C8 100 nF behind JP2 |
| OSC1 / OSC2 | 9 / 10 | 16 MHz crystal, HS, **no PLL** |

Firmware obligations that follow:

1. **The fourteen unused pins are driven low at start-up** (RA1–3, RA5,
   RC2–7, RB0, RB1, RB4, RB5; DS39977C §2.7) — there are no resistors.
2. **`CANMX` = 1 (RB2/RB3).** Moving the module now means soldering under
   the socket.
3. **`DBG_EN` gates the LEDs and the 0x603 frame**; RA0 is AN0 and must be
   made digital before it is read. It is not the CAN mode switch.
4. The MCP2562's STBY is hard-wired to ground, VIO to VDD — nothing to drive.
5. **The 120 Ω terminator is not fitted** (R5 DNF): the car's bus is
   terminated (60.1 Ω measured). A bench needs an external one.
6. **JP2 off before programming, back on after.**
7. Pin 6 is VCAP; the 28-pin K80 has no RA4 and no ENVREG.

Port A sources only 2 mA; anything that drives current comes from B or C.

## The decisions behind the HAL — an index

Each is argued, with citations, in a comment beside the code it produced.
Anything without a citation is a **decision** and says so; do not promote it
to a specification without opening the PDF.

- **`CANMX` is 1, and DS39977C §27.1's prose says the opposite** — Register
  28-5 and the pin-table footnote win. **The ECAN chapter is §27, not §22.**
  Take `#pragma config` spellings from the XC8 device header.
- **RB2 idles high** (`LATB = 0x04`): TXD is active low, so a low RB2 asks
  the transceiver to jam the bus until `hal_can_init()`; in Loopback LATB2 is
  all that keeps a fitted transceiver quiet.
- **500 kbps: BRP = 0, SYNC 1 + PROP 7 + PS1 5 + PS2 3, SJW 2**,
  `BRGCON1/2/3 = 0x40/0xA6/0x82` — Prop_Seg widened for the 1.4 m
  unterminated stub. Ran on the bench and in the car with both error counters
  at zero.
- **Mode 2, an eight-deep FIFO, six hardware filters**, receive by polling
  every pass. **Every function touching an `RXB0*` name sets `EWIN` first**
  (`ECANCON = 0x90`). Only identifiers something consumes are accepted;
  0x5A0 deliberately is not.
- **Three modes at build time**: `make -C mplab CAN_MODE=LISTEN_ONLY` /
  `LOOPBACK`; `hal_can_send()` refuses in Listen Only; `LED_PWR` blinks slowly
  in either silent mode. Not the jumper.
- **Configuration bits** differ from `CanSwitch.X` in `CANMX = PORTB`,
  `WDTEN = ON` with `WDTPS = 512` (2.048 s), `BORV = 0` (3.0 V: the A/D is
  specified only above), `BOREN = ON`, `RETEN = OFF`. **`SOSCSEL = DIG` must
  not be lost** (RC0/RC1 are the LEDs). `FOSC = HS1` — use Register 28-2,
  Table 3-1 is misaligned. `T3CKMX`/`T0CKMX` deliberately absent.
- **VddConv = 1.024 × 4096 / code** — twelve bits, **never the ten-bit
  1023**; the 1.024 V reference has no tolerance, so it is calibrated per unit
  (`VDD_CAL_*`); read a mean, never one frame.
- **Timer2 makes the millisecond** with no remainder; the clock is read
  atomically, restoring rather than forcing `GIE`.
- **EEPROM**: the ring uses 0..767; D120's 100 K is the limit, **D124 is not
  a ceiling** (`config.h`, `persist.h`). **One deliberate deviation**:
  `hal_eeprom_write()` restores `GIE` the instant `WR` is set instead of
  holding it across the 4 ms poll (`hal_sys.c` argues why), and never clears
  the watchdog inside the poll.

**What is verified and what is not.** It compiles and links clean for the
real part; the configuration words are **read back out of the hex**
(`CONFIG3H = 0x89`, CANMX set); 500 kbps has run on the bench and on the
car's bus. **Compiling proves nothing about order, timing or value on
silicon.** The timing budget is counted out of the listing, not measured
(`timing.md`). **One frame leaves every 25 ms and never two together** — a
correctness rule (USBtin dropped the third of a burst); it is why the EEPROM
write sits in a slot that transmits nothing. **Distance is integrated on
`DIST_TICK_MS` with the remainder carried**, a correctness rule no fixture
can show (`optimisation.md` §6). **Neither multiplication nor division uses
XC8's helpers** (`fastmul.h`, `divconst.h`); **never add a divisor by hand** —
`tools/divconst.py` derives and proves it; a divisor should be one the
physics forces. **`docs/firmware/optimisation.md` is required reading before
changing any loop or arithmetic in `src/`.** `tools/cycles.py --check` gates
every backward branch.

---

## The coupling to `mfd15` and `kicad`

**The layout of all five frames, 0x600–0x604**, defined in
`docs/firmware/frames.md` and read by `mfd15/tri/S-AQY.TRI`, **changes there in
the same breath as here** — a mismatch shows plausible wrong numbers, not an
error. `test/test_txframes.c` pins every offset against the TRI file. Every
field on the wire is coupled, 0x602 and 0x603 included. **0x603** (CAN
health) is sent only with JP1, so it reads zero in a closed dashboard by
design. **0x604** (idle grade and the start) is **not** behind JP1, and its
"not known" is 255, never 0. The coupling to `kicad` is the pin table above,
one-way and frozen.

Useful check on the display: FuelCntRaw (the raw ECU counter) rising while
FuelNow is nonsense means the fault is in this firmware's arithmetic.

---

## Before touching the maths

**Read `docs/firmware/can-decoding.md`** — its traps: the speed validity gate
is `(b1 & 0x40) && !(b1 & 0x03)`, not an equality; the fuel counter resets at
ignition-off and its delta is `(new − old) mod 32768`; bit 15 is not constant;
FuelAvg is zero below 100 m; **a frame that never arrived is not a reading of
zero** (`tank_valid`); **0x280's engine speed changes once per 180° of crank**,
so anything counted over frames rather than changes is weighted by engine
speed — and it is not cylinder identification.

**The torque calibration** (`frames.md`, `can-decoding.md` questions 7–8,
`config.h`): `TORQUE_CNM_PER_BIT` (1.06) and the drag line are **one
calibration — never move one alone**; the drag line is fitted on warm oil and
**idle is asserted, not fitted**; b7 is *indicated* torque and **b7 = 255 is
not full scale**. **The driving gate is a fixed requirement, not a
calibration**: torque and power are shown only while the car moves **and**
the pedal is off its rest (`compute_torque_d()`); the tests that hold it are
fixed in the code, never in the test. `TORQUE_TRIM_PCT` stays 0. The tank
calibration is closed as a decision; do not reopen it.

**`docs/firmware/refuted.md`** — read before reintroducing a good idea; only
settled-against things go in, nothing is ever deleted. The firmware's
questions sort four ways: `refuted.md` (settled "no"), `can-decoding.md`
*Resolved questions* (answered), *Never resolved but not required* (do not
work on these), `docs/firmware/open.md` (genuinely open: 11, `IdleHealth`
against 014).

---

## Testing — and what a test proves

```
make -C test test           # the whole C suite          make -C test check-pure
make -C test check-hal      # HAL compiles vs a stub     make -C test sanitize (CI)
python tools/replay.py --host-build test/fixtures/*.txt  # Python vs C
python -m unittest discover -s tools -p "test_*.py"
python tools/checkdocs.py --check                         # prose vs config.h
python tools/cycles.py --check                            # needs a build
```

- **Fixtures are real logs; never edit them.** Only the `_z1` logs have
  trustworthy time; `06`/`07` carry host time wrong by about ×2;
  `02_idle_60s` holds its recording twice and is corrected at read time.
  `test/fixtures/README.md` documents every one and the measured values.
- `tools/test_replay.py` and `test/test_compute.c` are twins: **a change to
  the maths belongs in both.** But **twins do not catch a fault they share**,
  and fixtures tick the core off 0x480 while `main.c` ticks it every pass —
  hence `test_scheduler.c` (drives the core as `main.c` does, the EEPROM
  write as a blocking gap) and `test_props.c` (invariants, fuzzing **reachable
  states only**).
- **A verification is only as wide as the call chain it ran.** Do not
  hand-build a struct another module produces when the question is what the
  device does; drive `decode_frame()` → `compute_*()` → the consumer
  (`test_a_silent_bus_reaches_the_eeprom_not_at_all` is the shape). Report
  the scope that actually ran.
- `test/xc8stub/xc.h` agrees with the code by construction and proves nothing
  about the hardware.
- Adding a `test_*.c` needs no Makefile change.

### Numbers in prose — `checkdocs.py` enforces both rules

What rots here is figures inside correct arguments.
1. **A number a command prints is generated or not written down.**
   `README.md`'s build-size block is filled by `checkdocs.py --write` from
   XC8's own summary; **never edit it by hand**.
2. **A number derived from a constant is derived in one place**; everywhere
   else says what it means and cites it.

Repeat reasoning freely; cross-reference by name (symbol, heading, register),
never by line number. Datasheet numbers may be repeated.

---

## Building, flashing, committing

**`make -C mplab` is the build** (XC8 v4.00 + `PIC18F-K_DFP 1.13.292`, pack
path pure ASCII, `TMP` derived under MSYS); `mplab/README.md` has every trap.
`ipecmd` must be on `PATH`. The pack IPECMD uses is not the compiler's, on
purpose.

**Flashing is `tools/flash.py` / IPECMD**, never the IDE
(`docs/firmware/flashing.md`): **`-OL` on every programming command**;
**`-W4.5` only for a bare board on the desk**, never with another supply; the
EEPROM is erased by default and **`--preserve-eeprom` is the opt-in that also
proves it**, while `canfuel.X` preserves — know which is in your hand;
**never branch on IPECMD's exit code**. Build and flash are one step so a hex
cannot be flashed in the wrong mode.

**Work directly on `main`** — no branches, no pull requests; if a harness
hands you a branch, merge it into `main` and push `main`. CI is the review.

**One commit per problem, committed as each is finished**; but when edits
have mixed, **do not split them by hand** — a tree where code, tests and docs
agree beats a tidy log.

**Before committing anything that touches the core**: the test commands
above. **If anything that ends up in the hex changes** (`src/`,
`mplab/Makefile`), **install XC8 first and run the `firmware` job's gates
locally** — nothing else catches a stale size block. Take both versions from
`.github/workflows/ci.yml`'s `env:`:

```sh
XC8=4.00; DFP=1.13.292          # <- from .github/workflows/ci.yml
curl -fSL -o /tmp/xc8.run "https://ww1.microchip.com/downloads/aemDocuments/documents/DEV/ProductDocuments/SoftwareTools/xc8-v$XC8-full-install-linux-x64-installer.run"
chmod +x /tmp/xc8.run && /tmp/xc8.run --mode unattended --unattendedmodeui none
curl -fSL -o /tmp/dfp.atpack "https://packs.download.microchip.com/Microchip.PIC18F-K_DFP.$DFP.atpack"
mkdir -p "$HOME/packs/PIC18F-K_DFP/$DFP" && unzip -q /tmp/dfp.atpack -d "$HOME/packs/PIC18F-K_DFP/$DFP"
export PATH="/opt/microchip/xc8/v$XC8/bin:$PATH"
make -C mplab DFP="$HOME/packs/PIC18F-K_DFP/$DFP/xc8"
python tools/cycles.py --check && python tools/checkdocs.py --check
```

Then `checkdocs.py --write` and commit the README change with the code. A
session that changes only documents, tools or tests does not install it. If
CI is already red, copy XC8's summary from the job log into
`mplab/build/memory.txt` and run `--write`.

---

## Engine health — `docs/engine-health/`

| file | what | lifetime |
|---|---|---|
| `open.md` | symptoms → hypotheses → tests, only what is unresolved; opens with *Where it stands* | ends |
| `refuted.md` | every hypothesis settled against, every symptom closed; nothing deleted | ends |
| `plan.md` | the planned fixes in order: **Part 1** bare instructions for the car, **Part 2** why and how it is read — never mixed; a new instruction and its reason land in the same commit (*the maintainer, 8/10*) | ends |
| `idle-log.md` | the diary of the idle investigation | permanent |
| `vehicle-history.md` | the service book: parts, dates, distances, nothing more | permanent |
| `vcds.md` | the VCDS blocks used, their specifications, how to record them | permanent |

### Keeping it current — every time, unasked (*the maintainer, 28/10/2026*)

**Every change under `docs/engine-health/` — and every report from the
maintainer about the car — ends with a currency pass over the whole folder,
in the same commit.** He must never have to ask for it. The pass:

1. **`open.md` *Where it stands***: its date, the closed and open lists, the
   ranking line and **Next** match the rest of the folder.
2. **`plan.md`**: a step that is done — by anyone, the maintainer on his own
   included — leaves **both parts**; Part 1 says what is really next; no
   "postponed", "booked", "current item" that is no longer true.
3. **`idle-log.md`**: every completed step or repair has its entry.
4. **`vehicle-history.md`**: everything fitted, changed, topped up or added
   (fuel cleaners, oil, adjustments) has its row; the odometer table has any
   new reading.
5. **Every symptom and hypothesis the change touches**: no "the next
   reading will…", "not yet", "tonight", "until X" that has since happened —
   replace it with what happened; superseded figures corrected where they
   stand; a settled item moved to `refuted.md`.
6. Then `grep -n -i "not yet\|next \|tonight\|postpon\|waits\|until"` over
   the folder and read each hit.

**The pass applies to its own edits**: what it changes is checked the same
way before the commit. A commit that leaves the folder inconsistent with
itself is not finished.

### The rules for its content

- **`idle-log.md` entries**: a `##` heading with the date and a short title,
  then three lines in this order — **Repairs** (changed, fitted, adjusted,
  added), **Tests** (only tested, read, recorded), **Changes after** (split
  *measured*, *felt*, *not known*) — an empty line left out; then a short
  detail, no procedure. Analysis and questions that only re-read earlier data
  are not entries; their findings go to the symptom in `open.md` (*28/10*).
- **`open.md`**: a new measurement goes into the evidence of the symptom and
  of every hypothesis it touches, not into a dated section. Mark *owner*,
  *general* (engine knowledge), *reasoned* (inference). **When the symptom
  list changes, every hypothesis's fit table gains or loses that column in
  the same commit and the ranking is re-read**; a symptom left out of the
  tables says why, once. A ranking change is agreed with the maintainer.
- **Every new observation the maintainer reports** — a sound, a smell, a
  leak, a reading — **is flagged: could it be a new symptom, or change one,
  and why; then ask. He decides**; never add a symptom unasked, never let one
  pass without asking.
- **A photograph of the part on the car, or anything he reads directly off
  it, outranks everything in the repository.** The document is corrected in
  the same commit and says what it used to say.
- **Idle smoothness is always on the `IdleHealth` scale** — `idledips
  --roughness`'s mean step × 50 — never the raw rpm grade (*12/10*);
  **lower is calmer**. **A warm-stop reading is in the everyday state**
  (blower 1, one seat heater 1, lights; *23/10*), the only one since
  *28/10*: the two states (every load off, every load on; *19/10*) were
  dropped, and idling is kept short — never ask for a stop made only to
  read it. A figure without a state is in it.
- **The repository is public: nothing that identifies the car or owner** —
  not the full VIN, not a plate, not an address; photos cropped first
  (*12/10*). The full VIN is in his private claude.ai artifact *New Beetle
  VIN*; **the photo album** (Google Photos, every repair since 6/2026) is in
  the private artifact *New Beetle Photo Album* with how to page it from a
  cloud session — find both with the Artifact tool's `action: "list"`, never
  copy either into a file here.
- The dated log before `open.md` lives only in git
  (`git show 7c69883:docs/engine-health.md`); nothing cites it.

### Sessions at the car — who runs what

**Find out where you are running first.** The maintainer's Windows laptop has
VCDS and the USBtin; a cloud container has neither, and then he is usually on
his phone. Check the platform and for a VCDS install; if unclear, ask once.

- **On the laptop**, propose every time: **you run `usbtin_capture.py`**,
  started before the ignition, to engine off; **he runs `oilwatch.py`** in a
  second terminal on the same file; **you run `tools/vcds_log.py`**
  (`--groups 014 001 003 --out "C:/Users/Luboš/Downloads/<name> 14-1-3
  YY-MM-DD.CSV"`, in the background). One run does the session: fault memory
  before, the log (reconnecting into `-2`, `-3` … when the ECU drops), fault
  memory after, then closes VCDS. **At the end, engine still idling, he says
  so; you create `<out>.stop`, the tool reads the fault memory (~30 s), you
  give him the codes — only then does he switch off.** He clicks nothing.
- **In the cloud**: hand him the commands and read what he uploads.
- **The fault memory is read after every session with VCDS connected**,
  without asking (never after a plain drive), saved beside the logs, the codes
  given to him with their status; **he clears it, by hand**. **Before he
  clears anything, read the adaptations** (`--groups 032 055 --seconds 20`,
  saved as `test/fixtures/vcds/vcds-<step>-adaptations-032-055.csv`):
  clearing resets 032.
- **After every captured session, without asking**: the capture to its next
  free `test/fixtures/NN_<name>_z1.txt`; **the whole capture uploaded
  unfiltered to the GitHub release `raw-captures`** — gzip a copy outside the
  repo as `YYYY-MM-DD_<name>_unfiltered_z1.txt.gz`, `gh release upload`,
  download it back and compare the decompressed `sha256sum`, **filter nothing
  until it matches**, delete the `.gz`; then filter the fixture to
  `grep -E '^t(1A0|280|288|320|420|480)'`, add it to `FILTERED` in
  `tools/test_canlog.py`, a row in `test/fixtures/README.md` and its count in
  `tools/test_coastscan.py`. VCDS logs go to
  `test/fixtures/vcds/vcds-<step>-<groups>.csv`. A capture stopped early leaves
  the adapter open: send `C\r`. **Never commit an unfiltered capture** (size:
  git keeps it for good); fetch one on demand into a temp dir (the scratchpad
  in the cloud) from
  `https://github.com/PoJD/canfuel/releases/download/raw-captures/<file>.gz`
  and delete it after.
- **Then, every time, the dips' share over the cylinders**:
  `tools/cutscan.py --shares` on the capture and pooled with every capture
  since the last repair — the top two slots' share and p against all four
  alike — reported to him and added to `open.md`, *The dips keep to one
  slot*; with injector cuts, `--name` too. `--pairs` is history only.
- **When Claude drives VCDS, it may only read**: measuring blocks, logging,
  reading the fault memory and saving it. **Nothing that writes to a control
  unit, ever** — no clearing, coding, adaptation, basic settings, output tests
  or resets. Scripts click only an allow-list and stop on anything unknown. If
  a step seems to need a write, stop and ask.
- **You cannot hear him.** A reading at the car reaches you as text (phone
  dictation works); align it to the capture by an event it records, never by
  when the message arrived.
- **The MFD and the CAN capture are one or the other, and the converter goes
  with the MFD**: a capture never contains 0x600–0x604. Everything from a
  captured session is computed from the ECU's raw frames — `IdleHealth` and
  the start by `tools/idledips.py`'s `health_summary()`, the oracle 0x604 is
  diffed against. Never ask him to read the display during a capture.

### Tools for the car

`pyserial` (for `usbtin_capture.py`) and `pywinauto` (for `vcds_log.py`,
Windows) are the only third-party dependencies; there is no
`requirements.txt` because CI needs neither.

```
python tools/usbtin_capture.py --seconds 60 --out idle_z1.txt
python tools/oilwatch.py idle_z1.txt
python tools/canlog.py FILE          # per-ID summary; --dump --id 0x480
python tools/replay.py --every 100 FILE
python tools/idledips.py --roughness FILE
python tools/afterpull.py FILE       # the warm idle after high revs
python tools/cutscan.py --shares FILE...
python tools/vcds_log.py --faults FILE
python tools/flash.py --mode loopback | --preserve-eeprom | --identify | --dry-run
```
