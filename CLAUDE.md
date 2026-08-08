# canfuel — converter firmware

A fuel consumption converter for the VW New Beetle, AQY engine (2.0 l / 85 kW,
PQ34). It reads the powertrain CAN bus (500 kbps), computes consumption, range,
torque and power, and sends them back onto the bus in frames 0x600–0x602. A
CANchecked MFD15 Gen2 display renders them from its own TRI file (repo `mfd15`).

MCU: PIC18F25K80, 16 MHz, XC8. The board lives in the `kicad` repo.

---

## Current state — read this first

**Phase 0 is done; the firmware itself does not exist yet.** `src/` is empty,
`mplab/` is empty, and `test/` holds fixtures and a Makefile but no `test_*.c`.

What does exist and works:

- `tools/canlog.py` — log parser, both formats, 77 tests green
- `tools/replay.py` — reference decoder in Python, reproduces the measured
  idle flow of 310 µl/s exactly
- `test/fixtures/` — seven real logs from the car, documented
- `docs/` — decoding, frame layout, refuelling reset, the overall plan

CI has three jobs. `tools` runs the Python tests and is doing real work today.
`core` runs `make check-pure` and `make test`, which currently pass by doing
nothing because `src/` is empty. `firmware` is a placeholder until there is an
MPLAB project to build.

### Next step: phase 1, the C core

Order and reasoning are in `docs/implementation-plan.md` §3. In short:
`decode.c` → restart detection → `compute.c` → `txframes.c` → `persist.c` →
`main.c`, each step verified against the fixtures.

`tools/replay.py` is the oracle. It is written against the same table the C
will be, so `tools/test_replay.py` doubles as the template for
`test/test_compute.c` — same fixtures, same expected numbers. Once the host
build exists, wire a `--host-build` switch into `replay.py` so the two outputs
can be diffed directly.

### Local toolchain

gcc and make are installed. XC8 is not — the `firmware` CI job and any real
device build still need it.

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

The whole core has to be compilable with gcc and testable against real logs
without a single piece of hardware. That is what should prevent ten board
revisions — before anything is soldered, a log is replayed and the consumption
figures are checked by eye.

Hardware belongs exclusively in `hal_can.c` and `hal_sys.c`.

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
  main.c        scheduler and glue — the only place it all meets
  decode.c/.h   frame parsing          PURE C
  compute.c/.h  maths                  PURE C
  txframes.c/.h frame assembly         PURE C
  persist.c/.h  EEPROM circular buffer
  hal_can.c/.h  ECAN + MCP2562
  hal_sys.c/.h  timers, ADC/FVR, LEDs, jumper
  config.h      every constant and switch
test/           core tests, run on the host through gcc
tools/          canlog.py, replay.py — Python, runs anywhere
```

Constants belong in `config.h`, not in the code. In particular
`FUELNOW_LH_BELOW_KMH`, `FUELNOW_CLAMP`, the refuelling threshold and the frame
periods.

The `piclib` library (github.com/PoJD/piclib) will be added as a submodule — it
provides `can_setupBaudRate(baudRate, cpuSpeed)`, max 500 kbps at 16 TQ.

---

## Tools

```
python tools/canlog.py test/fixtures/03_drive.txt          # per-ID summary
python tools/canlog.py --dump --id 0x480 FILE              # print frames
python tools/replay.py --every 100 test/fixtures/07_accel.txt
python -m unittest discover -s tools -p "test_*.py"        # 77 tests
```

`tools/replay.py` is the reference decoder in Python, written against the same
table as the future `decode.c` and `compute.c`. Once the C core exists, a
`--host-build` switch lands there and the diff between the two outputs becomes
a hard test. `tools/test_replay.py` doubles as the template for
`test/test_compute.c` — same fixtures, same expected numbers.

---

## Fixtures

Real logs from the car. **Do not edit them.** The tests reference exact numbers
from them.

⚠ `02_idle_60s.txt` contains the recording **twice** — both halves are
identical. It is corrected at read time (`parse_file(..., fix_doubled=True)`)
and the file itself stays original. Without that, the idle flow comes out doubled.

Details and a table of every log: `test/fixtures/README.md`.

---

## Verified values the core must reproduce

| Log | Counter total | Duration | Flow |
|---|---|---|---|
| `01_ign_only` | 0 µl | — | 0 |
| `02_idle_60s` | 18,652 µl | 60.1 s | 310 µl/s = 1.12 l/h |
| `05_rev3000` | 1,940 µl | 1.93 s | 1005 µl/s |
| `06_trip_reset` | 51,992 µl | 135.0 s | 385 µl/s, distance 125 m |
| `07_accel` | 9,752 µl | 15.9 s | 613 µl/s |

---

## What comes next

Phase 1 is the C core with host tests. The order of the steps and the reasoning
behind it are in `docs/implementation-plan.md`, §3. The breadboard phase is
skipped — Micro-Fit has a 3.0 mm pitch and does not fit a breadboard.
