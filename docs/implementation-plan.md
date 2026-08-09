# AQY fuel converter → MFD15 — implementation plan

State as of 2 August 2026, revision 2. Written to be picked up on the desktop
with Claude Code.

Working name of the device: **canfuel** (renaming it is trivial — it only
appears in the README and in repository names).

---

## 1. Structure on GitHub

Follows the existing style (`can` = firmware, `eagle` = boards), only with
KiCad. **Three repositories**, not a monorepo — each has a different
toolchain, different CI and a different lifetime.

### `kicad` — hardware (successor to the `eagle` repo)

A container for all future boards, the same way `eagle` is today.

```
kicad/
├── README.md                    # index of boards
├── lib/                         # symbols and footprints shared across projects
│   ├── pojd.kicad_sym
│   └── pojd.pretty/
├── canfuel/
│   ├── canfuel.kicad_pro
│   ├── canfuel.kicad_sch
│   ├── canfuel.kicad_pcb
│   ├── canfuel.kicad_prl        # gitignored, it is local state
│   ├── fab/                     # generated, committed for traceability
│   │   ├── gerbers/
│   │   ├── canfuel-bom.csv
│   │   └── canfuel-pos.csv
│   └── docs/
│       ├── schematic.pdf
│       └── mechanical.md        # dimensions, mounting in the air vent
└── .github/workflows/kicad.yml  # ERC + DRC + gerber export via kicad-cli
```

KiCad 8 uses text formats, so diffs are readable and `kicad-cli` can run ERC
and DRC in CI without a GUI. That is the main reason for moving off Eagle — a
design error fails in the pull request, not on a finished board.

### `canfuel` — firmware and decoding

```
canfuel/
├── README.md
├── docs/
│   ├── can-decoding.md          # AQY signal table (IDs, bytes, formulas)
│   ├── frames.md                # 0x600/0x601/0x602 — exact layout
│   └── calibration.md           # drag torque, tank
├── src/
│   ├── main.c                   # scheduler and glue only
│   ├── decode.c/.h              # parsing incoming frames    PURE, no PIC
│   ├── compute.c/.h             # all the maths              PURE, no PIC
│   ├── txframes.c/.h            # assembling outgoing frames PURE, no PIC
│   ├── reset_src.c/.h           # trip reset source, single place (see §5)
│   ├── persist.c/.h             # EEPROM circular buffer
│   ├── hal_can.c/.h             # PIC ECAN peripheral + MCP2562
│   ├── hal_sys.c/.h             # timers, ADC/FVR, LEDs, debug jumper
│   └── config.h                 # every constant and switch
├── test/
│   ├── test_decode.c
│   ├── test_compute.c
│   ├── test_persist.c
│   ├── fixtures/                # real logs from the USBtin
│   │   ├── 01_ign_only.txt
│   │   ├── 02_idle_60s.txt
│   │   ├── 03_drive.txt
│   │   └── 05_rev3000.txt
│   └── Makefile                 # gcc, runs on the host
├── tools/
│   ├── replay.py                # runs a log through the host build, prints output
│   └── canlog.py                # parser for the USBtinViewer format
├── mplab/                       # MPLAB X project (XC8)
└── .github/workflows/ci.yml     # host tests + XC8 build
```

**Key architectural decision:** `decode.c`, `compute.c` and `txframes.c` must
not contain a single `#include <xc.h>`. They take arrays of bytes and a time in
milliseconds, and return numbers. That makes the entire brain of the device
compilable with gcc and testable against real logs without a single piece of
hardware.

That is precisely what should prevent ten board revisions. Before anything is
soldered, `tools/replay.py test/fixtures/03_drive.txt` runs and prints a column
of fuel consumption that can be checked against reality by eye.

### `mfd15` — display and TRI

```
mfd15/
├── README.md                    # how the file is uploaded via oDSS
├── tri/
│   ├── S-AQY.TRI                # current production file, 16 sensors
│   └── reference/               # official Gen2 files as examples
│       ├── S-LINK.TRI
│       └── S-MAXX720.TRI
└── docs/
    ├── sensors.md               # description of all 16 sensors
    ├── tri-format.md            # 26 columns, meaning of each
    └── internal-sensors.md      # FFF channels, Gen2 scaling 0-1023 -> 0-56
```

A separate repository because the TRI file changes at a different rate than the
firmware and has no build. It is also the only part somebody else with a Beetle
and an MFD15 might want — and it is usable even without the converter.

---

## 2. Phases

| # | Phase | Output | Blocks on |
|---|---|---|---|
| 0 | Create repositories, CI skeleton | three empty repos, green CI | — |
| 1 | C core + host tests | `replay.py` prints consumption from logs | — |
| 2 | Schematic + PCB in KiCad | gerbers, BOM, order | — |
| 3 | Breadboard, listen-only in the car | decoder verified on a live bus | 1, purchase |
| 4 | Breadboard transmits | MFD shows real numbers | 3 |
| 5 | Assemble PCB, install | finished device in the air vent | 2, 4 |
| 6 | Calibration | drag torque, tank | 5 |

Phases 1 and 2 run in parallel and neither needs the car.

---

## 3. Phase 1 — the core (this first)

The order is chosen so that every step can be verified against real data.

1. `tools/canlog.py` — parser for the `t480 8 <hex>` format from USBtinViewer.
2. `decode.c` — extract the seven signals per the table. Tests: against known
   values from the logs (idle 797 rpm, CLT 100.5 °C, counter 0 in ign_only).
3. Detect engine restarts and the 0x1A0 init ramp (b1 == 0x40). Tests:
   `01_ign_only.txt` must not produce a single nonsensical delta jump.
4. `compute.c` — µl and metre accumulators, instantaneous and average
   consumption, range, torque after subtracting losses, power. Tests:
   `02_idle_60s.txt` must give 310 µl/s, `05_rev3000.txt` 958 µl/s.
5. `txframes.c` — assemble 0x600/0x601/0x602, unsigned big endian.
6. `persist.c` — circular buffer in EEPROM, 12-byte record, 64 slots, written
   once every 60 s and only on change. Tests: simulate 100,000 cycles, check
   for even wear and correct recovery after a power loss.
7. `main.c` — cooperative scheduler on a single timer, no RTOS. Slots: 10 ms
   read CAN, 100 ms TX 0x600/0x601, 1 s TX 0x602 + EEPROM.

Once this passes, all the logic that would be painful to debug with a soldering
iron in hand is done.

> **Correction from phase 0.** Item 3 above is wrong as written. The gate is a
> bit mask, not an equality: `(b1 & 0x40) && !(b1 & 0x03)`. Item 4 is also off —
> `05_rev3000.txt` measures 1005 µl/s, not 958, and `02_idle_60s.txt` only
> gives 310 µl/s once the doubled file is de-duplicated. See
> `can-decoding.md` for both.

### 3.1 FuelNow — dual unit by speed

The FuelNow channel (0x600 b0-1, step 0.1) carries **two different quantities**
depending on speed, like the trip computers in modern cars:

```
v <  4.0 km/h  ->  instantaneous flow in l/h
v >= 4.0 km/h  ->  consumption in l/100 km
```

- **A single threshold, no hysteresis.** The jump when it switches is
  intentional — it is a visual cue that it switched. A 0.5 km/h band can be
  added later if the number flickers while crawling right around the threshold.
- **Clamp at 999** (i.e. 99.9 on the display). The TRI gauge tops out at 99.90
  and a higher value would behave unpredictably.
- **Why 4 and not 3 km/h:** at 3 km/h a flow above 3 l/h already pushes the
  value past 99.9, so it would be clipped on every normal pull-away. At 4 km/h
  that boundary only arrives at 4 l/h.

Expected l/100 km values above the threshold:

| flow | 4 km/h | 6 km/h | 10 km/h | 15 km/h | 20 km/h |
|---|---|---|---|---|---|
| 1.5 l/h | 37.5 | 25.0 | 15.0 | 10.0 | 7.5 |
| 3 l/h | 75.0 | 50.0 | 30.0 | 20.0 | 15.0 |
| 6 l/h | 150 → 99.9 | 100 → 99.9 | 60.0 | 40.0 | 30.0 |

Both constants (`FUELNOW_LH_BELOW_KMH`, `FUELNOW_CLAMP`) belong in `config.h`.

**FuelAvg always stays in l/100 km.** It is computed as a ratio of accumulated
microlitres and metres, not by integrating the instantaneous value — that way
idling at a red light does not ruin the average. Flow in l/h is additionally
available on its own in 0x601 b4-5 (step 0.01 l/h) should a dedicated sensor
ever be wanted.

Other corner cases: flow 0 → 0.0; data source lost for > 500 ms → zeros; range
from a rolling average over 30 segments of 1 km; tank damped over 60 s.

---

## 4. Phase 2 — the board

A recap of the requirements, to have them at hand during design:

- **MCU:** PIC18F25K80 (DIP, already in stock), 16 MHz crystal + 2× 22 pF
- **Transceiver:** MCP2562 (to buy — no MCP2561 left)
- **Power:** 5 V straight from the MFD15, connector C6, ground C12. No
  converter, no reverse-polarity protection, no TVS — the 12 V branch was
  dropped from the design. Current draw must stay far below the 0.5 A limit
  (realistically ~30 mA).
- **CAN:** C7 = CAN-H, C8 = CAN-L. **Do not fit the termination** — the bus is
  already terminated in the car and a third 120 Ω would overload it. A solder
  jumper for bench testing is sensible though.
- **Connector:** 4-pin, to be picked at GME. Y-splitter only on connector C.
- **LEDs:** two (power, CAN status), active only when the debug jumper on RA0
  is fitted. Nothing lights up in the car.
- **Programming:** 5-pin ICSP header for a PICkit.
- **Dimensions:** board ~55 × 45 mm, two layers, mostly through-hole.
  Enclosure for the air vent 6.5 × 5.5 cm, depth max ~3 cm (the vent is 7 cm,
  but the connectors eat the rest and must not be forced).
- **Decoupling:** 100 nF at every supply pin, 10 µF at the input.

Add `kicad-cli sch erc` and `kicad-cli pcb drc` to CI — both must pass before
the boards are ordered.

> **Correction from phase 0.** The crystal load capacitance is 32 pF, so
> **33 pF** should be fitted, not 22 pF. See `kicad/CLAUDE.md`.

### 4.1 Buying parts

The complete BOM only falls out of the schematic, so the **GME list should be
put together after phase 2**, not before. Buying twice is worse than buying later.

What comes out of the drawer and what does not:

- **From the drawer:** PIC18F25K80. Semiconductors do not degrade with age when
  kept dry, only from static during handling. They are also the expensive,
  harder-to-source parts.
- **New:** crystal, all capacitors, resistors, connectors, sockets, LEDs.
  Electrolytics really do age — without voltage the oxide layer breaks down and
  ESR rises. Ceramics and resistors last forever, but for a few crowns they are
  not worth digging out of a box.
- **New purchase:** MCP2562.

For the crystal the main argument is that an unmarked part from the drawer has
an unknown load capacitance, so even the 22 pF would be guesswork.

---

## 5. Open question: source of the trip reset

It is a detail — but only as long as the design keeps it one. The answer is to
isolate the decision in a single module:

```c
// reset_src.h
bool reset_requested(const can_frame_t *f);
```

Two implementations, selected in `config.h`:

- **`RESET_SRC_CLUSTER`** — watches the trip counter from the instrument
  cluster (candidate 0x5D8 b0). Rule: `delta mod 256 == 1` is a normal tick
  including the 255→0 rollover; a decreased value with any other delta is a reset.
- **`RESET_SRC_MFD`** — watches frame 0x702 from the MFD15, byte 2 being a bit
  mask of Can Switch 1–6. Requires the Can Switching licence.

The rest of the firmware only calls `reset_requested()` and does not care about
the source. Tests for both variants run on the host against synthetic frames.
Changing the decision is one line in `config.h`, not a refactor.

**One sniff decides it:** switch on the USBtin, drive a few hundred metres,
press the trip reset on the cluster, drive a bit more. If a byte shows up in
the log that grows with distance and drops to zero on the press, the CLUSTER
variant wins and no licence is needed. If not, buy the licence and use the MFD
variant.

Neither variant involves a physical button.

> **Superseded in phase 0.** The average is now reset on refuelling instead,
> which needs neither a sniff nor a licence. See `refuel-reset.md`. The
> CLUSTER variant can still be added later as a second trigger.

---

## 6. Phases 3–4 — testing in the car

The procedure is built so that every step can fail harmlessly.

1. **Bench, listen-only.** Breadboard and USBtin on the desk, the USBtin
   replaying frames from a log, the converter only listening. Verifies hal_can
   and ID filtering.
2. **Bench, transmitting.** The converter sends 0x600–0x602 and the USBtin
   reads them. Verifies that the bytes on the wire match what the host build
   computes.
3. **Car, listen-only.** Breadboard wired into the Y-splitter but with the
   transceiver TX pin disconnected. Record what the converter decodes and
   compare against a parallel log from the USBtin. Zero risk to the bus.
4. **Car, transmitting.** Only now is TX connected. First check that
   0x600–0x602 really are free (confirmed in the logs), then watch the ECAN
   error counters.
5. **MFD shows numbers.** Upload S-AQY.TRI via oDSS, activate, compare FuelNow
   against FuelCntRaw. Also verify the unit switch around 4 km/h.

> **Superseded in phase 0.** The breadboard phase is skipped — Micro-Fit has a
> 3.0 mm pitch and does not fit a breadboard. Everything is socketed and the
> core is tested on the host.

---

## 7. Calibration at the end

- **Drag torque** — a linear model against engine speed; both points are
  already in the logs (idle, and 2940 rpm in neutral where torque at the wheels
  is zero, so indicated torque equals drag torque).
- **Tank** — refuel a known amount from a jerrycan and compare against 0x320
  b2. It currently reads 0 l plus the reserve lamp, which is not enough to
  verify against.
- **Unit switch threshold** — fine-tune while driving; it is a constant in
  `config.h`.
- **Fuel in litres** — needs no calibration, the 1 µl unit is confirmed by an
  external source as well as by our own data.

---

## 8. What is done and what is not

**Done:** bus decoding, format of the transmitted frames, hardware
architecture, placement, power supply, S-AQY.TRI including the Gen2 internal
sensors, FuelNow behaviour.

**Not started:** anything inside the repositories. Phase 0 is the first thing
on the desktop.

**Uncertain:** source of the trip reset (§5), whether 0x420 b3 really is oil,
the meaning of 0x288 b5/b6, the `info;` line in the TRI file.

> **Superseded.** Phase 0 is complete, phase 2 shipped as an order to Gatema
> on 2026-08-09, and steps 1 to 6 of §3 are done: `config.h`, `decode.c`,
> `compute.c`, `txframes.c` and `persist.c` all exist, are compiled by gcc and
> are checked against every fixture. Step 7, `main.c`, waits on the two HAL
> modules, which are the only things left in phase 1.
>
> Two open questions from §7 closed along the way. Drag torque is calibrated —
> `drag [Nm] = 17.44 + 0.0002501 × rpm`, reproducing both logged points
> exactly. The 0x602 layout was chosen freely because `S-AQY.TRI` turns out not
> to read that frame at all; only 0x600 and 0x601 are coupled to the display.
>
> The current state of play lives in `CLAUDE.md`, not here. This file is the
> original plan and is kept as one.
