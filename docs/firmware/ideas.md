# Firmware — ideas for extending the converter

**Ideas, not plans.** What the converter could do next, written down on
22/11/2026 when the owner asked what the engine-health work suggests, so that
none of them has to be thought of again. Each says what it would show, what it
would take and where it stands. One that is built moves out of this file into
the document that describes it; one that is declined stays here, marked, with
the reason, so it is not proposed twice.

The engine's own investigation is `docs/engine-health/`; this file is about
the converter, the display and the board.

---

## Built

- **Each cylinder's share of a standing idle, live** — frame 0x605, built
  22/11/2026. `frames.md`, *0x605*.
- **A summary of every drive's warm idles, kept in the EEPROM** — the
  owner's idea, frames 0x606 (this drive) and 0x607 (the previous one),
  built 22/11/2026: warm idle time, mean `IdleHealth`, misfires a minute,
  the weakest cylinder's mean deviation. `frames.md`, *0x606 and 0x607*.

## Declined

### Not done: the engine lamp on 0x604

*Declined by the owner, 22/11/2026.* The lamp's state (0x480 b1 bit 3,
`can-decoding.md`) and a count of its lightings with the engine running could
ride in two free flag bits of 0x604. **The cluster already shows the lamp, and
it stays lit until the fault memory is cleared or several starts pass**, so
the display would add nothing.

## Proposed, with the display's own inputs — no change to the converter

The MFD15 has **six analog inputs, 0–5 V, ten bits**, and supplies the
sensors from pin C6 (`mfd15/docs/manual-mfd15-gen2.pdf`); the TRI format
already has an air/fuel-ratio sensor type. Each idea below is a sensor and
rows in the TRI file, nothing more:

- **A wideband lambda controller with an analog output.** Lambda is not on
  the bus (`can-decoding.md`, *What is NOT on the bus*), so this would be the
  first live view of the mixture — the engine-health questions about the
  mixture and the probes (`docs/engine-health/open.md`, S19 and H11). It
  needs a sensor boss in the exhaust.
- **A fuel pressure sender, 0–5 V, on the rail.** The rail pressure is
  measured once with a gauge today (`docs/engine-health/plan.md`, 8u); live,
  it would show whether it moves when the idle stumbles (H7).

Worth doing only if those questions are still open after the timing belt
(`docs/engine-health/plan.md`, 8q).

## Proposed, needing a new board

- **The crank and cam sensors (G28, G40) read directly.** The way the ECU
  itself detects misfire: every tooth of the crank wheel timed, and the cam
  sensor naming the cylinders, where 0x605 has one engine speed per 180° and
  names them by a convention. It needs an input for an inductive sensor and
  one for a Hall sensor, a capture timer, and a tap on the wiring to the ECU
  that cannot load the signal the engine runs on. A new revision of the
  frozen board; the oscilloscope work on G28 and G40 planned in
  `docs/engine-health/plan.md` (6r) would show what such an input has to
  take.
- **K-line, to read VCDS block 014 without VCDS.** Settled that it cannot be
  done over CAN (`refuted.md` B13), which says what the K-line route would
  take. The owner decided on 22/11/2026 to stay with VCDS; kept here in case
  a new board is made for the item above anyway.
