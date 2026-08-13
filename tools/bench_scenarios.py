"""Synthetic streams for the bench scenarios of docs/install.md step 7.

**Frames are patched, not built.** Every frame here starts as a real one from
`test/fixtures/` and has exactly the field under test overwritten. Building
them from scratch would mean writing the inverse of `decode.c` from the same
table `decode.c` was written from -- a twin, and `CLAUDE.md` is explicit that
twins do not catch a fault they share. Taking the byte layout from a recording
off the vehicle means these scenarios test the hardware path and the clamps,
not our own idea of the format.

So the offsets below are the only thing this file asserts about the layout, and
each names the line of `src/decode.c` that reads it back.

The counter in 0x480 counts **microlitres directly** -- `compute.c` takes the
delta and calls it `delta_ul` with no conversion -- which is what lets a flow
be requested in µl/s here.
"""

from __future__ import annotations

from dataclasses import dataclass

import canlog

# src/config.h, and src/decode.c reads each one back.
ID_SPEED, ID_ENGINE, ID_COOLANT, ID_TANK, ID_OIL, ID_FUEL = (
    0x1A0, 0x280, 0x288, 0x320, 0x420, 0x480)

SPEED_GATE_REQUIRED = 0x40      # decode.c: (data[1] & 0x40) != 0
SPEED_GATE_FORBIDDEN = 0x03     # decode.c: (data[1] & 0x03) == 0
SPEED_MMH_PER_BIT = 5           # decode.c: u16le(data, 2) * 5
COUNTER_MASK = 0x7FFF           # decode.c: raw & 0x7FFF
THROTTLE_REST = 38              # config.h, and 0x280 b5 at rest


def u16le(value: int) -> bytes:
    return bytes((value & 0xFF, (value >> 8) & 0xFF))


def templates(log) -> dict:
    """One real frame per identifier, to patch from."""
    out = {}
    for frame in canlog.parse_file(log, fix_doubled=True):
        if frame.can_id not in out and frame.dlc == 8:
            out[frame.can_id] = bytearray(frame.data)
    missing = {ID_SPEED, ID_ENGINE, ID_TANK, ID_FUEL} - out.keys()
    if missing:
        raise SystemExit(
            f"{log}: no 8-byte template for " +
            ", ".join(f"{i:#05x}" for i in sorted(missing)))
    return out


@dataclass
class Condition:
    """What the car is doing, in engineering units."""
    speed_kmh: float = 0.0
    rpm: int = 800
    throttle: int = THROTTLE_REST
    torque_b7: int = 25
    tank_l: int = 40
    flow_ul_s: int = 300
    speed_valid: bool = True

    @property
    def speed_mmh(self) -> int:
        return round(self.speed_kmh * 1000)

    def fuel_now_d(self) -> int:
        """What FuelNow must read, from the same two identities the core uses.

        Below FUELNOW_LH_BELOW_MMH the display shows l/h, above it l/100 km,
        and one microlitre per metre is exactly 0.1 l/100 km -- which is why
        neither branch needs a conversion factor.
        """
        if self.speed_mmh < 4000:
            return min(999, round(self.flow_ul_s * 36 / 1000))
        return min(999, round(self.flow_ul_s * 3600 / self.speed_mmh))


def frames_for(tpl: dict, cond: Condition, counter: int) -> list:
    """The six accepted identifiers, patched to describe `cond`."""
    speed = bytearray(tpl[ID_SPEED])
    speed[1] = (speed[1] | SPEED_GATE_REQUIRED) & ~SPEED_GATE_FORBIDDEN & 0xFF
    if not cond.speed_valid:
        speed[1] &= ~SPEED_GATE_REQUIRED & 0xFF
    speed[2:4] = u16le(round(cond.speed_mmh / SPEED_MMH_PER_BIT))

    engine = bytearray(tpl[ID_ENGINE])
    engine[2:4] = u16le(cond.rpm * 4)
    engine[5] = cond.throttle & 0xFF
    engine[7] = cond.torque_b7 & 0xFF

    tank = bytearray(tpl[ID_TANK])
    tank[2] = (tank[2] & 0x80) | (cond.tank_l & 0x7F)

    fuel = bytearray(tpl[ID_FUEL])
    fuel[2:4] = u16le(counter & COUNTER_MASK)

    out = [(ID_SPEED, bytes(speed)), (ID_ENGINE, bytes(engine)),
           (ID_TANK, bytes(tank)), (ID_FUEL, bytes(fuel))]
    for extra in (ID_COOLANT, ID_OIL):
        if extra in tpl:
            out.append((extra, bytes(tpl[extra])))
    return out


class Stream:
    """A condition, ticked at 10 ms, with the fuel counter advancing.

    The counter is the only thing with memory: it is an absolute, free-running
    ECU value and the firmware takes differences of it, so a scenario that
    changes condition mid-run must not restart it -- except deliberately, which
    is what `restart()` is for and what an ignition-off really does.
    """

    TICK_MS = 10

    def __init__(self, tpl: dict, cond: Condition):
        self.tpl = tpl
        self.cond = cond
        self.counter = 1000
        self._carry = 0.0

    def restart(self) -> None:
        self.counter = 0
        self._carry = 0.0

    def tick(self) -> list:
        self._carry += self.cond.flow_ul_s * self.TICK_MS / 1000.0
        step, self._carry = divmod(self._carry, 1.0)
        self.counter = (self.counter + int(step)) & COUNTER_MASK
        return frames_for(self.tpl, self.cond, self.counter)
