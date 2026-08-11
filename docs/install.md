# From three clones to a working device

The whole path, in the order it has to happen, across all three repositories.
Every step says what it needs, what it proves, and how you know it worked.

**Nothing below has been done yet.** The firmware builds, the board is
manufactured and the display's configuration is verified in the car — but no
board has been populated, programmed or wired in. Steps 4 onwards are written
from the datasheets and the design, not from experience, and they say so where
it matters. Correct this document as you go; that is what it is for.

```
git clone git@github.com:PoJD/canfuel.git
git clone git@github.com:PoJD/kicad.git
git clone git@github.com:PoJD/mfd15.git
```

Side by side, in the same parent directory. The parent is deliberately not a
git repository, so run git inside one of the three.

---

## What the finished thing is

A PIC18F25K80 on a 55 × 45 mm board, in the air vent behind a CANchecked MFD15
Gen2 display, taking 5 V from the display's own plug and hanging off the car's
powertrain CAN at 500 kbps. It reads seven frames from the ECU, computes
consumption, range, torque and power, and sends them back on frames 0x600–0x602
for the display to render.

The car does not know it is there. Nothing lights up unless a jumper is fitted.

---

## Order of operations

The order is chosen so that each step can fail cheaply and be understood on its
own. **Do not skip step 4**: it costs ten minutes on a desk and it is the only
one that tests the CAN driver without a car attached.

| # | Step | Needs | Repository |
|---|---|---|---|
| 1 | Build and test on a PC | gcc, make, Python | `canfuel` |
| 2 | Upload the display configuration | the display, a PC, oDSS | `mfd15` |
| 3 | Make up the harness | crimping tools, the loom parts | `kicad` |
| 4 | Populate and programme a board, loopback on the desk | PICkit, XC8 | `canfuel` |
| 5 | Listen only, in the car | the car | `canfuel` |
| 6 | Transmit, in the car | the car | `canfuel` |
| 7 | Check it against the raw counter | a drive | — |

Steps 1 to 3 are independent of each other and can be done in any order or in
parallel. From 4 on, the order is the point.

---

## 1. Build and test on a PC

No hardware at all. This proves the arithmetic against seven real recordings
from the car before anything is soldered.

```
cd canfuel
make -C test test            # 250 checks
make -C test check-pure      # no <xc.h> anywhere in the core
make -C test check-hal       # the HAL still compiles
python -m unittest discover -s tools -p "test_*.py"        # 77 tests
python tools/replay.py --host-build test/fixtures/*.txt    # Python vs C
```

All of it runs in under fifteen seconds. `replay.py` on its own prints a
consumption column you can read by eye:

```
python tools/replay.py --every 100 test/fixtures/07_accel.txt
```

**On this machine** `make -C test` needs `TMP="$TEMP"` on the command line; the
reason is in `CLAUDE.md` under *Local toolchain* and it is a quirk of the shell,
not of the repository.

**What it proves.** The core reproduces the Python reference on all seven logs —
fuel totals and restart counts exactly, distance to within 7 mm over 54 m — and
both were checked against figures measured in the car. It proves nothing at all
about the hardware.

---

## 2. Upload the display configuration

In `mfd15`. Full instructions are in that repository's README; the short form:

1. Connect the display to a PC and start oDSS.
2. Open `tri/S-AQY.TRI`, upload it, activate it.
3. **Confirm it worked by looking at `DisplayVolt`** — it must show a realistic
   12–14 V. That is an internal sensor of the display, so it is live even with
   no car attached, which makes it the one channel that proves the upload
   rather than the wiring.

If the file will not load, or a sensor named "0" appears, delete the first
`info;1.0;...` line and upload it again.

**Expect seven channels to read zero**: FuelNow, FuelAvg, FuelTank, Range,
Torque, Power and VddConv. Those are the converter's, and they stay at zero
until step 6. The other nine read the car's bus directly and should be live as
soon as the display is in the car.

**Do not reorder the rows** of the TRI file. It is addressed by position.

---

## 3. Make up the harness

In `kicad`, and the document is
[`canfuel/docs/harness.md`](https://github.com/PoJD/kicad/blob/main/canfuel/docs/harness.md).
Follow it rather than this summary — it is a checklist with the tools, the wire
colours, the connector cavities and the fuse, and it exists because this is the
part that is awkward to redo.

What it covers, so you know whether you are ready to start it:

- a test crimp on a spare pin **before** the dashboard comes apart
- the CAN pair, twisted, from the cluster to the air vent
- the 4-pin Micro-Fit at the converter end, and **which cavity is which**
- two more sockets into the display's existing plug C, at C6 and C12, for 5 V
- a 200 mA time-lag fuse spliced into the 5 V run, positioned so it can be
  changed without dismantling the dash
- routing, and taping up only at the very end

**The one that bites:** the Micro-Fit cavity numbering is mirrored between the
wire side and the mating face, so counting from an end is exactly how CANH ends
up in circuit 1 — which puts **5 V on a CAN wire and kills the transceiver**.
Find the moulded `1` and ring circuit 1 out to the board's +5 V pad before the
first power-up.

| Micro-Fit circuit | Net | Wire | Plug C |
|---|---|---|---|
| 1 | +5V | red | C6 |
| 2 | SGND | black | C12 |
| 3 | CANH | white | C7 |
| 4 | CANL | yellow | C8 |

**Do not fit R5**, the 120 Ω termination. The car's bus is already terminated at
both ends — 60.1 Ω measured across CANH and CANL says so. A third resistor
overloads the drivers. Bench testing off the car needs an external terminator
instead.

---

## 4. Populate, programme, and loopback on the desk

This is the step that is easy to skip and should not be.

### Populate

24 parts, mostly through-hole, on a 55 × 45 mm board. The BOM is in
`kicad/canfuel/fab/canfuel-bom.csv`. Two of the three boards can be populated
today; the third is a spare waiting on two more Micro-Fit headers.

### Programme

```
cd canfuel
make -C mplab CAN_MODE=LOOPBACK
```

That writes `mplab/build/canfuel.hex`. Flash it with a PICkit through J3.
Building is documented in `mplab/README.md`, including which XC8 and which
Device Family Pack — the pack is not optional and the version has to match.

⚠ **JP2 comes off before programming and goes back on afterwards.** It puts the
100 nF MCLR capacitor in circuit, which is what the datasheet asks for in
normal operation and what interferes with ICSP.

**Fit JP1** — without it both LEDs stay dark by design, and you are about to
need them.

### What loopback proves

DS39977C §27.3.5 hands the transmit buffers straight to the receive buffers, so
the module talks to itself. **No bus, no USBtin, no transceiver needed.** It
exercises the bit timing, all seven acceptance filters, the eight-deep FIFO,
the access-bank window, `txframes` and `decode` — everything except the wire
itself.

Watch the LEDs:

| LED_PWR | LED_CAN | Means |
|---|---|---|
| slow blink | steady | **working** — loopback is a silent mode, so the slow blink is correct here |
| slow blink | 5 Hz blink | `hal_can_init()` never got the module into the mode it asked for. The bit timing or a configuration register is wrong. Stop here. |
| slow blink | dark | nothing is arriving — the transmit path or the FIFO is not working |
| steady | any | **wrong hex.** A steady LED_PWR means a normal build; you flashed the wrong one |

A fault caught here costs a reflash. The same fault caught in step 5 costs a
trip to the car, and in step 6 it puts error frames on the car's bus.

---

## 5. Listen only, in the car

```
make -C mplab CAN_MODE=LISTEN_ONLY
```

Flash it, fit JP1, wire the board in through the Y-splitter, and switch on.

**Why this mode first, and it is not caution for its own sake.** The 500 kbps
bit timing is datasheet arithmetic that no hardware has ever executed. A
Normal-mode node whose timing is wrong does not merely fail to read the bus —
**it fills the bus with error frames** and takes the car's own modules down with
it. Listen Only is silent by the module's own guarantee (§27.3.4): no
transmissions, no error flags, not even acknowledgements.

**Check first, before anything else:** `hal_can_rx_errors()` and
`hal_can_tx_errors()`. They are the ECAN error counters, and a bit-timing fault
shows there long before it shows anywhere else. `LED_CAN` blinking at 2.5 Hz is
the same news from across the room.

| LED_PWR | LED_CAN | Means |
|---|---|---|
| slow blink | steady | frames arriving, module healthy — **this is what you want** |
| slow blink | 2.5 Hz blink | arriving, but the error counters are not zero or the FIFO overflowed |
| slow blink | 5 Hz blink | the module never reached Listen Only |
| slow blink | dark | the bus has been quiet for 500 ms — the car is not talking, or the wiring is wrong |

Dark and fast-blink are the two to tell apart: **dark means the car is not
talking, fast blink means we are not listening.**

Log what the converter decodes and compare it against a parallel USBtin
recording. Nothing is on the wire from us yet, so there is nothing to break.

---

## 6. Transmit

```
make -C mplab
```

A plain build with no `CAN_MODE`, which is Normal mode. `LED_PWR` now goes
**steady** — that change is the point of it: a listen-only hex left in the
device by accident is otherwise indistinguishable from a transmitter that has
quietly stopped working.

The display's seven converter channels should come alive within a second.

Watch the error counters again for the first few minutes. This is the first
time the device acknowledges frames and arbitrates for the bus.

---

## 7. Check it against the raw counter

The useful check once it is live, and it needs no instruments:

**Compare `FuelNow` against `FuelCntRaw` on the display.** `FuelCntRaw` is the
ECU's counter with no conversion applied at all — it comes straight off 0x480.
So if it rises while `FuelNow` shows nonsense, the fault is in **this
firmware's arithmetic** rather than in its input. If neither moves, the fault is
upstream of us.

Two more worth doing on the first drive:

- **Range and FuelTank should agree with each other.** They read the same damped
  tank level; if one moves and the other does not, something is wrong in
  `compute.c`.
- **Refuel and watch the trip average clear.** The reset fires on a rise of more
  than 3 L in the at-rest median, which takes about five seconds of standing
  still after the fill. `docs/refuel-reset.md` has the rules and the corner
  cases.

---

## Then: calibration

Two things are known to be approximate and both need the car:

- **The torque scale**, 0.75 Nm/bit, is a decision inside a bracket the factory
  ratings imply rather than a measurement. A VCDS measuring block settles it in
  one session — `docs/can-decoding.md` open question 8 has the procedure, and
  question 3 wants the same session.
- **Drag torque under load.** The current model is a straight line through two
  idling measurements and says nothing about pulling.

And one that needs a jerrycan: **the tank**, which wants a known quantity put in
to check the level against.

`docs/can-decoding.md` lists every open question with what would close it. Two
of them fall out of a single sixty-second recording on a live bus.

---

## If something does not work

| Symptom | Look at |
|---|---|
| Both LEDs dark | JP1 not fitted — that is by design, nothing lights up in the car without it |
| LED_CAN 5 Hz | `hal_can_init()` failed. Bit timing, `CANMX`, or a configuration bit |
| LED_CAN dark, car running | wiring: CANH/CANL swapped, or the stub not connected. Ring it out |
| Display channels stay at 0 | a silent build (LED_PWR blinking), or the frame layout drifted from `S-AQY.TRI` |
| Display shows plausible but wrong numbers | the frame layout **did** drift. `docs/frames.md` and `S-AQY.TRI` must agree; `test/test_txframes.c` pins every offset |
| The fuse blew | a short on the converter board. Fit one new fuse; if the second goes, stop and find the short |
| Nothing at all after wiring | ring circuit 1 of the Micro-Fit out to the board's +5 V pad. If CANH is in circuit 1, the transceiver has had 5 V on it |

`CLAUDE.md` in this repository is the long-form reasoning behind every decision
above, and `docs/refuted.md` is what was tried and did not work.
