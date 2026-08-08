# canfuel

A fuel consumption converter for the VW New Beetle with the AQY engine
(2.0 l / 85 kW, PQ34).

It reads the powertrain CAN bus, computes instantaneous and average
consumption, range, torque and power, and sends them back onto the bus in
frames of its own. A CANchecked MFD15 Gen2 display shows them as ordinary sensors.

Physically it sits in the air vent behind the display, powered by 5 V taken
straight from the display.

## Status

Phase 0 — repository set up, bus decoding documented and verified against real
logs. The firmware itself is not written yet.

## Quick start

```
python -m unittest discover -s tools -p "test_*.py"
python tools/replay.py --every 100 test/fixtures/07_accel.txt
```

`replay.py` is the reference decoder in Python. It runs a log through the same
formulas the firmware will use and prints a consumption column to check by eye.

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
