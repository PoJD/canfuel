# canfuel

A fuel consumption converter for VW PQ34 cars with the AQY engine
(2.0 l / 85 kW).

It reads the powertrain CAN bus, computes instantaneous and average
consumption, range, torque and power, and sends them back onto the bus in
frames of its own, which an aftermarket multi-function display shows as
ordinary sensors. *(Developed and verified on a 2.0 AQY with a CANchecked
MFD15 Gen2 display; the signal decoding is specific to that powertrain bus,
the rest is not.)*

Physically it sits behind the display, powered by 5 V taken straight from it.

## Status

**It is installed in a car and working.**

It sits behind the display in the air vent, reads the vehicle's bus and feeds
the MFD15 ten channels of its own. What that took is
[`docs/install.md`](docs/install.md), in order, from three clones to a closed
dashboard.

The pure C core — frame decoding, the fuel arithmetic, the transmitted frames
and the EEPROM buffer — is compiled with gcc and checked against seven real
logs from a vehicle, with no hardware involved. Those numbers can be trusted as
far as the logs go.

The hardware half — the ECAN driver, the millisecond timer, the A/D, the
EEPROM and the scheduler — is written against the datasheet and **compiled for
the real part by XC8 v4.00 with no warnings**. CI
builds the hex on every push and uploads it. That retires a whole class of
doubt: every register and configuration bit exists and is spelled the way the
device data spells it, and the configuration words were read back out of the
hex rather than assumed.

**What it costs the part**, straight out of the last build:

<!-- checkdocs:begin build-size -->

| Space | Used | Of | Share | What it holds |
|---|---|---|---|---|
| Program space | 13,920 B | 32,768 B | 42.5 % | the firmware itself |
| Data space | 354 B | 3,649 B | 9.7 % | RAM |

The **data EEPROM is not in that table**, because the compiler
would report it as empty: the hex initialises none of it. It is written
at run time, and `persist.c` uses **768 of 1,024 bytes** —
64 slots of 12, rewritten in turn so the wear is spread. The rest is
deliberately left free. See [`src/persist.h`](src/persist.h).

Written by `python tools/checkdocs.py --write` from XC8's memory summary
and `src/config.h`, and checked in CI. Do not edit by hand.

<!-- checkdocs:end build-size -->

The CPU side is in [`docs/timing.md`](docs/timing.md), which costs every
function out of the assembly listing: a typical scheduler pass is 49–134 µs,
the worst pass without an EEPROM write is 6.5 ms against a 10 ms slot, and the
whole firmware uses about a sixth of the CPU. `python tools/cycles.py` prints
it and CI fails if a budget is blown.

**What has actually run, and what is still only counted.** The 500 kbps bit
timing was datasheet arithmetic; it now has hours on a bench bus at 357 frames
a second and a vehicle's own bus behind it — the longer one, with a 1.4 m
unterminated stub — with both CAN error counters at zero on each. The fuel
arithmetic agrees with the display's raw ECU counter in the car. The refuelling
reset has fired on real fuel from a jerrycan.

⚠ **The timing budget is still counted rather than measured.**
[`docs/timing.md`](docs/timing.md) costs every function out of the assembly
listing XC8 generates; nothing has put a scope on it. The margins are large
enough that this is a stated limitation rather than a worry — the busiest
transmit slot uses 2.4 ms of its 25 — but it is not a measurement.

⚠ **One calibration is open**: the engine's drag torque is fitted on 72–77 °C
oil rather than the 95–110 °C of real driving, which biases torque and power
slightly low. `docs/can-decoding.md` question 7.

**[`docs/install.md`](docs/install.md) is the procedure** — the whole path from
three clones to a working device, in the order it has to happen, with each step
saying what it needs, what it proves and how you know it worked.

## Prerequisites

Only the first row is needed to work on the firmware. Nothing below it is
required to run the tests, and none of it is required to read the code.

| For | What | Notes |
|---|---|---|
| the core and its tests | **gcc**, **make**, **Python 3.11+** | no third-party packages — everything is standard library |
| building for the chip | **XC8 v4.00** and **PIC18F-K_DFP 1.13.292** | the two versions must match each other; `mplab/README.md` has the whole story and the traps |
| flashing a board | **MPLAB X** and a programmer IPECMD supports | not needed to build — `make -C mplab` produces the hex on its own. MPLAB X is installed for `ipecmd.exe`, not for the IDE, which is never opened for this. *(Tested on a PICkit 3.)* |
| recording from the bus | a **CAN interface** the host can drive | *(Tested on a USBtin; `tools/usbtin_capture.py` drives it and needs `pip install pyserial`.)* |

**What has to be on `PATH`.** `gcc`, `make`, `python` — and **`ipecmd.exe`**, which
every command in `docs/install.md` invokes by bare name. It is not put there by
the MPLAB X installer; it lives in `mplab_platform/mplab_ipe` under the install
directory. **`xc8-cc` is the exception**: `mplab/Makefile` looks for it on
`PATH` and falls back to the default Windows install path, so `make -C mplab`
works either way.

**The check that separates a toolchain problem from a code problem:**
`make -C test test` must pass **without XC8 installed at all**. The core is deliberately pure C with no
hardware headers, so if that fails, the problem is gcc or make, not the
Microchip toolchain.

**On XC8 and the Device Family Pack.** v4.00 ships no device data whatsoever, so
the pack is not optional and its version has to match the compiler — MPLAB X
v6.00 bundles a pack that v4.00 refuses. The pack's path must also be pure
ASCII. Both are documented, with the exact failure messages, in
[`mplab/README.md`](mplab/README.md); CI pins the same two versions.

**On the programmer.** Through the 5-pin ICSP header J3, driven from the
command line with `ipecmd.exe` out of the MPLAB X install — the IDE is not
opened for it. IPECMD supports MPLAB Snap, PICkit 3 and 4 and ICD 4 for this
part; only the `-TP` name changes. *(Tested on a PICkit 3, which was driven
from the command line and took its own firmware update.)* The commands are in
[`docs/install.md`](docs/install.md) steps 4 and 5, and
`python tools/flash.py` wraps them — including `--preserve-eeprom`, which keeps
the trip accumulators across a reflash and then proves it did by reading the
EEPROM back either side of the write.

One thing that transfers to any script: **IPECMD's exit code cannot be branched
on.** A `-I` that never found the target still exits 0, and `-T`, which works,
exits 50. Parse the output.

## Quick start

```
make -C test test                                       # the C core
make -C test check-pure                                 # no <xc.h> in the core
make -C test check-hal                                  # the HAL still compiles
python -m unittest discover -s tools -p "test_*.py"     # the Python tools
python tools/replay.py --every 100 test/fixtures/07_accel.txt
python tools/replay.py --host-build test/fixtures/*.txt

make -C mplab                                           # the device build, needs XC8
python tools/cycles.py                                  # cycle budgets from the build
python tools/checkdocs.py --check                       # the prose still matches config.h
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
| `docs/frames.md` | layout of frames 0x600–0x603, FuelNow, Range, torque, the diagnostic frame |
| `docs/refuel-reset.md` | resetting the average on refuelling, and the tank audit |
| `docs/timing.md` | what every part costs in cycles, and the margins |
| `docs/optimisation.md` | **read before changing any loop or any arithmetic** — what was optimised, why, and what is deliberately left alone |
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
