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

## Proposed, in software only

### A short history of the warm idles, in the EEPROM

*The owner's idea, 22/11/2026; its shape is agreed in outline, not built.*

So that every drive can be reported with a handful of numbers and drives can
be compared with each other, without a capture: over the **warm** standing
idles of the current start (oil warm, the 0x604 gate and settle rule),

- the **total warm idle time**, which with `Uptime` (0x603) says how much of
  the drive the figures rest on;
- the **mean `IdleHealth`**, the **misfire rate** (the `MisfAvg` arithmetic
  restricted to warm idle) and the **mean deficit of the weakest cylinder**
  from 0x605's blocks;

kept in the EEPROM and written **at most once in five minutes, and only when
a value changed**, so that a start survives the ignition going off and the
next drive can show the last one beside its own.

What it would take, and what is still to decide:

- **Its own EEPROM area.** The trip ring uses bytes 0–767 (`persist.h`);
  256 are free. A handful of starts at a few bytes each fits, with the same
  CRC discipline as the trip record. At one write in five minutes the
  endurance figure DS39977C gives (`config.h`, `persist.h`) is not
  approached.
- **Mean or median.** A mean is a sum and a count and costs nothing; a median
  needs the values kept. A mean is the natural first choice for a few bytes
  of EEPROM.
- **Where "warm" starts** — an oil temperature threshold; `tools/cylscan.py`
  uses 85 °C for its warm runs.
- **How it reaches the display**: a frame of its own (0x606) or a page of
  values cycling on one, with rows appended to `mfd15/tri/S-AQY.TRI`.

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
