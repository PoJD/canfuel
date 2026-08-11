# canfuel

A fuel consumption converter for the VW New Beetle with the AQY engine
(2.0 l / 85 kW, PQ34).

It reads the powertrain CAN bus, computes instantaneous and average
consumption, range, torque and power, and sends them back onto the bus in
frames of its own. A CANchecked MFD15 Gen2 display shows them as ordinary sensors.

Physically it sits in the air vent behind the display, powered by 5 V taken
straight from the display.

## Status

**Written in full, run on nothing.**

The pure C core — frame decoding, the fuel arithmetic, the transmitted frames
and the EEPROM buffer — is compiled with gcc and checked against seven real
logs from the car, with no hardware involved. Those numbers can be trusted as
far as the logs go.

The hardware half — the ECAN driver, the millisecond timer, the A/D, the
EEPROM and the scheduler — is written against the datasheet and syntax-checked
with gcc, and that is all. **XC8 has never compiled it and no board has ever
run it.** The boards were ordered on 2026-08-09 and arrive during the week of
2026-08-17.

## Quick start

```
make -C test test                                       # the C core, 238 checks
make -C test check-pure                                 # no <xc.h> in the core
make -C test check-hal                                  # the HAL still compiles
python -m unittest discover -s tools -p "test_*.py"     # the Python tools
python tools/replay.py --every 100 test/fixtures/07_accel.txt
python tools/replay.py --host-build test/fixtures/*.txt

make -C mplab                                           # the device build, needs XC8
```

`replay.py` is the reference decoder in Python. It runs a log through the same
formulas the firmware uses and prints a consumption column to check by eye.
With `--host-build` it runs the actual C core over the same log and diffs the
two, so the reference and the code that gets flashed cannot drift apart.

## Documentation

| File | Contents |
|---|---|
| `docs/can-decoding.md` | signal table, four traps, verified values |
| `docs/frames.md` | layout of frames 0x600–0x602, FuelNow, Range, torque |
| `docs/refuel-reset.md` | resetting the average on refuelling |
| `docs/implementation-plan.md` | overall plan for all phases |
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

- `kicad` — the converter board
- `mfd15` — the TRI file for the display

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
