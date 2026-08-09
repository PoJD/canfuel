# canfuel

A fuel consumption converter for the VW New Beetle with the AQY engine
(2.0 l / 85 kW, PQ34).

It reads the powertrain CAN bus, computes instantaneous and average
consumption, range, torque and power, and sends them back onto the bus in
frames of its own. A CANchecked MFD15 Gen2 display shows them as ordinary sensors.

Physically it sits in the air vent behind the display, powered by 5 V taken
straight from the display.

## Status

The pure C core is written and tested: frame decoding, the fuel arithmetic,
the transmitted frames and the EEPROM buffer, all compiled with gcc and
checked against seven real logs from the car without any hardware involved.

Still to come: the hardware half — the CAN peripheral, the timers and the
scheduler — and the MPLAB project. The boards were ordered on 2026-08-09.

## Quick start

```
make -C test test                                       # the C core, 238 checks
python -m unittest discover -s tools -p "test_*.py"     # the Python tools
python tools/replay.py --every 100 test/fixtures/07_accel.txt
python tools/replay.py --host-build test/fixtures/*.txt
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

## Layout

```
src/     firmware (pure C core, HAL kept separate)
test/    host tests through gcc, plus fixtures
tools/   canlog.py, replay.py and their tests
mplab/   MPLAB X project (XC8)
```

## Related repositories

- `kicad` — the converter board
- `mfd15` — the TRI file for the display

## Licence

Not decided yet.
