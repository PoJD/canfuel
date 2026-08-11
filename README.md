# canfuel

A fuel consumption converter for the VW New Beetle with the AQY engine
(2.0 l / 85 kW, PQ34).

It reads the powertrain CAN bus, computes instantaneous and average
consumption, range, torque and power, and sends them back onto the bus in
frames of its own. A CANchecked MFD15 Gen2 display shows them as ordinary sensors.

Physically it sits in the air vent behind the display, powered by 5 V taken
straight from the display.

## Status

**It builds. It has never run.**

The pure C core — frame decoding, the fuel arithmetic, the transmitted frames
and the EEPROM buffer — is compiled with gcc and checked against seven real
logs from the car, with no hardware involved. Those numbers can be trusted as
far as the logs go.

The hardware half — the ECAN driver, the millisecond timer, the A/D, the
EEPROM and the scheduler — is written against the datasheet and, since
2026-08-09, **compiled for the real part by XC8 v4.00 with no warnings**. CI
builds the hex on every push and uploads it. That retires a whole class of
doubt: every register and configuration bit exists and is spelled the way the
device data spells it, and the configuration words were read back out of the
hex rather than assumed.

**No board has ever run it.** Compiling is not running: a register written in
the wrong order at the wrong time compiles exactly as cleanly as one that is
not, and the 500 kbps bit timing is datasheet arithmetic that no hardware has
executed. The boards were ordered on 2026-08-09 and arrive during the week of
2026-08-17. `docs/timing.md` is the same caveat for the scheduler — the timing
budget is counted out of the assembly listing, not measured.

**Everything around the board is ready.** The display's configuration is
uploaded and verified, and the harness is built, fitted in the car and measured
at 5.01 V where the board will plug in. **[`docs/install.md`](docs/install.md)
is the plan** — the whole path from three clones to a working device, with a
column showing where this particular car has got to. The next action is its
step 4.

## Quick start

```
make -C test test                                       # the C core, 250+ checks
make -C test check-pure                                 # no <xc.h> in the core
make -C test check-hal                                  # the HAL still compiles
python -m unittest discover -s tools -p "test_*.py"     # the Python tools
python tools/replay.py --every 100 test/fixtures/07_accel.txt
python tools/replay.py --host-build test/fixtures/*.txt

make -C mplab                                           # the device build, needs XC8
python tools/cycles.py                                  # cycle budgets from the build
```

`replay.py` is the reference decoder in Python. It runs a log through the same
formulas the firmware uses and prints a consumption column to check by eye.
With `--host-build` it runs the actual C core over the same log and diffs the
two, so the reference and the code that gets flashed cannot drift apart.

## Documentation

| File | Contents |
|---|---|
| **`docs/install.md`** | **from three clones to a working device — start here if you are building one** |
| `docs/can-decoding.md` | signal table, four traps, verified values, the questions register — one open, six resolved, two parked |
| `docs/frames.md` | layout of frames 0x600–0x602, FuelNow, Range, torque |
| `docs/refuel-reset.md` | resetting the average on refuelling, and the tank audit |
| `docs/timing.md` | what every part costs in cycles, and the margins |
| `docs/refuted.md` | ideas that were believed and turned out wrong — **all three repositories** |
| `test/fixtures/README.md` | description of the logs and known data defects |
| `mplab/README.md` | how to build the firmware, and what JP2 is for |

Every hardware fact in the firmware comes from the manufacturer's datasheet
for the exact part and cites its section. Both datasheets live in `docs/`:
`pic18f25k80-datasheet.pdf` (Microchip DS39977C) and `mcp2562-datasheet.pdf`
(DS20005167C). The reasoning is in `CLAUDE.md`.

## Layout

```
src/     firmware — pure C core, HAL kept strictly separate
test/    host tests through gcc, plus fixtures and a stub xc.h
tools/   canlog.py, replay.py and their tests
mplab/   the device build: a plain Makefile and an MPLAB X project
```

## Related repositories

This is one of three repositories and it is the firmware half. A working device
needs all three, and they are separate because they have separate toolchains,
separate CI and separate lifetimes. Clone them side by side.

| Repository | What it holds | Go there for |
|---|---|---|
| **`canfuel`** (this one) | the converter firmware | decoding the car's frames, the arithmetic, the frames we send, the build |
| [`kicad`](https://github.com/PoJD/kicad) | the converter board | `canfuel/docs/harness.md` — **how to make the loom and wire it into the car**, step by step. `canfuel/docs/pinout.md` is the one-page connector reference, and `canfuel/docs/implementation-plan.md` is how the board was designed |
| [`mfd15`](https://github.com/PoJD/mfd15) | the display configuration | `tri/S-AQY.TRI` and how to upload it, plus `docs/sensors.md` — what every gauge reads and where it comes from |

**The one coupling that can bite** is the layout of frames 0x600 and 0x601:
`docs/frames.md` defines it and `mfd15/tri/S-AQY.TRI` consumes it. Change it
here and it must change there in the same breath — getting it wrong produces no
error at all, just plausible wrong numbers on the display.
`test/test_txframes.c` pins every offset against the TRI file.

The `kicad` coupling is the pin assignment, and it is one-way and frozen: the
boards being manufactured are commit `c06e710` of that repository.

## Licence

[Apache License 2.0](LICENSE). Use it, change it, build one, sell one — the
only obligations are to keep the copyright and licence notices and to say what
you changed.

**`NOTICE` lists what is not ours.** The two manufacturer datasheets in `docs/`
are Microchip's and are redistributed for reference only; the licence above
does not cover them and does not claim to. Everything else in this repository
is covered.

Questions, corrections and pull requests are welcome as issues on any of the
three repositories, or by email to Lubos Housa <luboshousa@gmail.com>.
