# From three clones to a working device

The whole path, in the order it has to happen, across all three repositories.
Every step says what it needs, what it proves, and how you know it worked.

**Where a step rests on something that has not been run on hardware, it says
so.** Correct this document as you go; that is what it is for.

```
git clone git@github.com:PoJD/canfuel.git
git clone git@github.com:PoJD/kicad.git
git clone git@github.com:PoJD/mfd15.git
```

Side by side, in the same parent directory. The parent is deliberately not a
git repository, so run git inside one of the three.

---

## What the finished thing is

A PIC18F25K80 on a 55 × 45 mm board, mounted behind an aftermarket multi-function
display, taking 5 V from the display's own plug and hanging off the vehicle's
powertrain CAN at 500 kbps. It reads six frames from the ECU, computes
consumption, range, torque and power, and sends them back on frames 0x600–0x603
for the display to render.

**Scope.** The frame layout and the signal decoding are specific to the VW PQ34
powertrain bus; they are verified on a 2.0 AQY engine and nothing here is
verified against any other. The board, the firmware structure and this
procedure are not vehicle-specific — the decoding table is.

The vehicle does not know the converter is there. Nothing lights up unless a
jumper is fitted.

---

## What you need

**Software is listed in each repository's own README** — `canfuel` for the
toolchain, `kicad` for KiCad, `mfd15` for oDSS — because what you need depends
on which half you are working on, and the versions belong next to the thing
they build. This section is the **physical** side, which no single repository
owns.

| Thing | For step | Notes |
|---|---|---|
| **A CAN display that renders frames from a user-supplied config** | 2, and everything after | the whole point of the device; it also supplies the converter's 5 V. *(Tested on a CANchecked MFD15 Gen2; `mfd15/tri/S-AQY.TRI` is written for its TRI format.)* |
| **Whatever the display's configuration tool needs** | 2 | on the tested display that is a phone or laptop with Wi-Fi and a browser; nothing is installed |
| **The converter board** | 5 onwards | `kicad/canfuel/fab/` holds the gerbers, drill files and BOM a fab house needs |
| **The parts to populate it** | 5 | 23 fitted parts plus two sockets, mostly through-hole — `kicad/canfuel/fab/canfuel-bom.csv`, which lists neither the sockets nor R5. See step 5 |
| **Soldering iron** | 5 | through-hole, nothing fine-pitch |
| **A programmer IPECMD supports for the PIC18F25K80** | 4, 5 | through the 5-pin ICSP header J3, driven from the command line with **IPECMD** — see step 4. MPLAB X must be installed, because IPECMD is part of it, but the IDE is never opened. IPECMD also drives MPLAB Snap, PICkit 4 and ICD 4; only the `-TP` name changes. *(Tested on a PICkit 3 with MPLAB X v6.00.)* |
| **A CAN interface the host can drive** — a second one unlocks 7.3 and 7.4 | 7, 8, and any recording | for watching the bus and recording logs. Any adapter that reaches 500 kbps will do; only the capture script is adapter-specific. *(Tested on a [USBtin](https://www.fischl.de/usbtin/); `tools/usbtin_capture.py` drives it over its serial protocol and needs `pyserial`. Every fixture in `test/fixtures/` was recorded with it.)* |
| **Multimeter** | 3, 5, 7 | ringing out the loom, confirming 5 V before the board is ever plugged in, and measuring the bench bus termination in step 7 |
| **Crimping tools and loom parts** | 3 | listed in `kicad/canfuel/docs/harness.md`, which is where that list belongs |
| **A breadboard** | 7 only | to build a short bench bus. No resistors needed if the adapters have switchable termination — two terminators give 60 Ω, the middle of the transceiver's specified 50–65 Ω range |
| **A diagnostic tool for the vehicle** | calibration only | **optional.** Not needed to build or run anything. *(Tested with VCDS.)* |
| **The vehicle** | 8, 9, 10 | a VW PQ34 car with the AQY engine. Other PQ34 cars share much of the bus but nothing here is verified against them |

**Termination** is worth knowing about: the board deliberately does not fit R5,
because the vehicle's bus is already terminated at both ends. A bench bus
therefore needs its own — step 7 uses the adapters' own switchable terminators
rather than loose resistors — but step 6, loopback, needs none at all, which is
another reason to do it.

**Nothing above is needed for step 1.** The whole core builds and its tests run
on a PC with gcc, make and Python and no hardware whatsoever.

---

## Order of operations

The order is chosen so that each step can fail cheaply and be understood on its
own. **Do not skip step 6**: it costs ten minutes on a desk and it is the
cheapest test of the CAN driver there is.

| # | Step | Needs | Repository |
|---|---|---|---|
| 1 | Build and test on a PC | gcc, make, Python | `canfuel` |
| 2 | Upload the display configuration | the display and its configuration tool | `mfd15` |
| 3 | Make up the harness | crimping tools, the loom parts | `kicad` |
| 4 | Prove the programmer, with no board | a programmer, a USB port, MPLAB X | `canfuel` |
| 5 | Populate and programme a board | programmer, XC8, an iron | `canfuel` |
| 6 | Loopback on the desk | nothing but 5 V | `canfuel` |
| 7 | *(recommended)* A bench bus, with a verdict | breadboard, 1 CAN adapter — 2 for 7.3 and 7.4 | `canfuel` |
| 8 | Listen only, in the vehicle | the vehicle | `canfuel` |
| 9 | Transmit, in the vehicle | the vehicle | `canfuel` |
| 10 | Check it against the raw counter | a drive | — |
| 11 | Close it up | standoffs, tape | — |

Steps 1 to 4 are independent of each other and can be done in any order or in
parallel — **none of them needs a board**, which is why step 4 sits where it
does rather than inside step 5. From 5 on, the order is the point.

**Step 7 is the only one you can leave out**, and it is still the one to do.
Nothing later breaks without it — but be clear about what is being skipped,
because step 6 covers less than its name suggests.

Loopback proves the CAN module accepted its configuration and reached its mode.
It cannot prove anything about receiving, because in that mode the only frames
arriving are our own and the acceptance filters reject them (see step 6). So
**without step 7, the first time the receive path, the six hardware filters,
the eight-deep FIFO and `decode` run at all is in the car** — where a failure
costs a trip, and the only instrument is a blinking LED.

**Its four parts are not equally worth it and step 7 grades them**, so "I only
have one adapter" is not a reason to skip the lot: **7.1 and 7.2 need one**,
and they are the two that cover what step 6 cannot.

---

## 1. Build and test on a PC

No hardware at all. This proves the arithmetic against real recordings from the
car before anything is soldered.

```
cd canfuel
make -C test test            # the whole C suite
make -C test check-pure      # no <xc.h> anywhere in the core
make -C test check-hal       # the HAL still compiles
python -m unittest discover -s tools -p "test_*.py"        # the Python tools
python tools/replay.py --host-build test/fixtures/*.txt    # Python vs C
```

All of it runs in under fifteen seconds. `replay.py` on its own prints a
consumption column you can read by eye:

```
python tools/replay.py --every 100 test/fixtures/07_accel.txt
```

**What it proves.** The core reproduces the Python reference on every recorded
log — fuel totals and restart counts exactly, distance to within 7 mm over 54 m — and
both were checked against figures measured in the car. It proves nothing at all
about the hardware.

---

## 2. Upload the display configuration

**Follow `mfd15/README.md`, *Uploading the file*** — it is the step-by-step and
it is not repeated here, because a procedure kept in two places diverges. What
this section carries is what you need to know to plan around it:

**Nothing is installed.** oDSS is served by the display itself and opened in a
browser (`mfd15/docs/manual-mfd15-gen2.pdf` §4). A phone is enough; there is no
cable, no driver and no desktop application. The one trap is that the display's
Wi-Fi hotspot is **off by default** and is turned on by holding both buttons
until a QR code appears — that is what sends people looking for a USB port.

**This step does not need the car.** The display wants 12 V on plug B and
nothing else; the CAN pair matters only when you want to see live values. So it
can be done on a bench, and it can be done before the harness exists.

**Download the TRI file before you start.** Once the phone is on the display's
hotspot it has no internet.

**How you know it worked:** `DisplayVolt` shows a realistic 12–14 V. It is an
internal sensor of the display, live without a bus, which makes it the one
channel that proves the *upload* rather than the wiring. With the car's bus
connected, the CAN icon also goes green and the nine bus-fed channels come
alive.

**Expect seven channels to read zero**: FuelNow, FuelAvg, FuelTank, Range,
Torque, Power and VddConv. Those are the converter's, and they stay at zero
until step 9. The other nine read the car's bus directly and should be live as
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

## 4. Prove the programmer, with no board

**The only step in the second half that needs no board.** It answers one
question — can this machine drive this programmer from the command line — while
the answer is still simple, rather than mixed in with a freshly soldered board
the first time something goes wrong.

### The tool is IPECMD

Programming is driven from the command line, not from the IDE. **`ipecmd` is
called by bare name and has to be on `PATH`**; the installer does not put it
there, and it lives in `mplab_platform/mplab_ipe` under the MPLAB X install
directory. MPLAB X therefore has to be installed, and is never opened.

Everything else about the tool — why it rather than the two other command-line
programmers in the same install, what each flag does, the exit codes it returns
and the environment traps — is in
[`flash-tool-notes.md`](flash-tool-notes.md). None of it is needed to do this
step.

### Plug the programmer in and run one command

```
ipecmd -P18F25K80 -TPPK3 -I
```

`-I` is *Display Device ID*. It reads and cannot write, so there is nothing it
can damage, and there is deliberately no target attached yet.

| What it prints | What it means |
|---|---|
| a complaint about the **target** — no target voltage, or an invalid device ID | **the pass.** There is no target, so a complaint about one is the tool working: the command line opened it and it got as far as ICSP |
| `Programmer not found` | it never opened at all — see below |
| a firmware download first, then one of the above | see *If it downloads firmware* |

⚠ **Read what it prints, not the exit code.** IPECMD's exit codes do not mean
what they look like; `flash-tool-notes.md` has the observed values and is the
place that matters when somebody writes a script.

**If it says `Programmer not found` with the programmer plugged in**, check in
this order: **MPLAB X or MPLAB IPE open** and holding the tool, the **firewall**
on IPECMD's localhost socket, then the programmer itself. `ipecmd -T` lists
connected tools and is the shortest "is it alive" there is.
`flash-tool-notes.md` has the citations for all three.

### If it downloads firmware

*Readme for IPECMD.htm* §12: the programmer's own firmware is upgraded
automatically on the first operation. It is not a fault, and it is not
skippable — it would happen identically from the IDE.

⚠ **It is also not to be expected.** It happened here because the programmer had
been in a drawer for years; one that has been driven by a current MPLAB X will
simply not do it. If nothing is downloaded, nothing is wrong.

If it does happen, **run the identical command again**, because the first run
cannot separate "the tool works" from "the tool survived being reflashed":

- **nothing downloads the second time and it is quick** — done. That is the
  steady state every run in steps 5 to 9 starts from.
- **the download appears again, on every invocation** — the update is not
  sticking, and that is a broken programmer however successful the operations
  after it look.

### The ICSP header pinout

| Pin | Signal |
|---|---|
| 1 | ~MCLR / VPP |
| 2 | +5 V (VDD Target) |
| 3 | SGND (VSS) |
| 4 | PGD (ICSPDAT, RB7) |
| 5 | PGC (ICSPCLK, RB6) |

**The source is DS51795B Figure 1-2**, *PICkit 3 Programmer Connector Pinout*,
held at `kicad/canfuel/docs/pickit3-users-guide.pdf`. That connector is **six**
pins; pin 6 is `PGM (LVP)`, low-voltage programming, which this project does not
use, so J3 stops at five. **Align the plug on the pin 1 marker, not on the end
of the header** (§1.2.3) — a 6-pin plug on a 5-pin header overhangs by one
position, and it is only harmless because the overhang is at the far end.

**A different programmer needs its own pinout and its own user's guide.** Only
the `-TP` short name changes in the command above, but how a tool drives MCLR
and target power is not something a device listing tells you, and `MCLRE = ON`
here makes that pin fussy. `flash-tool-notes.md` lists the tools IPECMD supports
for this part, and how to establish an unknown header by measurement.

### What it does not prove

Nothing about the board, nothing about the ICSP wiring, nothing about the hex. A
programmer that opens and reports its own firmware can still fail to program a
target for a dozen reasons that only exist once there is a target. Step 5 is
where those get tested.

---

## 5. Populate and programme a board

Everything that turns a bare PCB and a bag of parts into a device that has been
written to. Testing it is step 6, deliberately separate: this step ends when
`ipecmd` says it verified, and nothing here proves the firmware runs.

### Populate

**23 fitted parts plus two sockets**, mostly through-hole, on a 55 × 45 mm
board. The BOM is in `kicad/canfuel/fab/canfuel-bom.csv`. Two of the three
boards can be populated today; the third is a spare waiting on two more
Micro-Fit headers.

⚠ **Two things that file does not tell you.**

- **The two DIP sockets** — narrow 7.62 mm DIP-28 for U1, DIP-8 for U2. They
  have no schematic symbol, so KiCad cannot emit them into a generated BOM;
  they are in the parts table of `kicad/canfuel/docs/implementation-plan.md` §2
  as rows with no reference. **Fit the sockets, and do not solder either chip
  straight into the board** — the socket is the escape hatch the design leans
  on, and it is what lets U1 come out if a pin assignment ever has to change.
- **R5 is absent on purpose.** It is the 120 Ω termination, it must not be
  fitted, and `120R DNF` is on the silkscreen. Do not count it among the parts
  to populate.

### The whole board, in the order to solder it

Every part, once, in build order. **The last column is the one to read, and it
is a trigger: `yes` means stop and check which way round it goes before the
iron touches it.** `no` means both ways are the same part and nothing you do
with it can be wrong — pick it up and solder it.

Seven parts say yes. **Two of them — J1 and J2 — are keyed**, so the connector
body physically refuses the wrong orientation; the check there takes a second
and cannot fail. **The remaining five are the real ones**: both LEDs, C6, and
the two chips. The section after the table is how to tell, one part at a time.

**The two sockets are the exception that the trigger cannot express**, which is
why they carry a note instead. Soldering a socket the wrong way round does
nothing at all — it is two rows of holes onto the same pads either way. But the
board's pin 1 marking ends up **underneath** it, and the moment orientation
really matters is later, when the chips go in. Read the next section before
soldering either socket, not after.

The order is lowest-first, for the ordinary reason: a tall part soldered early
holds the board off the bench and every part after it goes in crooked. The one
non-obvious entry is C7, which is first because it is the only surface-mount
part and it lives on the **bottom** — once through-hole legs are sticking out
down there, that pad is awkward to reach.

**Read *The joints that need more heat than they look like*, below the table,
before the iron is hot.** It is one technique note, it applies to roughly half
the joints on this board, and the joint where it matters most fails two steps
later in a way that reads as an unpowered board.

| # | Ref | Part | Where / what it does | Orientation matters |
|---|---|---|---|---|
| 1 | **C7** | 10 µF X7R 1210 **SMD** | **bottom side**, under U1 pin 6 — VDDCORE/VCAP | no |
| 2 | R1 | 10 kΩ | MCLR pull-up | no |
| 3 | R2 | 10 kΩ | RA0 pull-down, the JP1 debug jumper | no |
| 4 | R3 | 1 kΩ | in series with D1 | no |
| 5 | R4 | 1 kΩ | in series with D2 | no |
| 6 | R6 | 470 Ω | MCLR series resistor | no |
| — | ~~R5~~ | ~~120 Ω~~ | **DO NOT FIT.** Silk reads `120R DNF` | — |
| 7 | — | **DIP-28 socket**, narrow 7.62 mm | for U1. Not in the BOM | no — **but record pin 1 first, see below** |
| 8 | — | **DIP-8 socket** | for U2. Not in the BOM | no — **but record pin 1 first, see below** |
| 9 | C1, C2 | 33 pF C0G | crystal load capacitors | no |
| 10 | C3 | 100 nF | decoupling, U1 VDD (pin 20) | no |
| 11 | C4 | 100 nF | decoupling, U2 VDD (pin 3) | no |
| 12 | C5 | 100 nF | decoupling, U2 VIO (pin 5) | no |
| 13 | C8 | 100 nF | MCLR hold-up, behind JP2 | no |
| 14 | Y1 | 16 MHz HC-49/S crystal | two pins, symmetric | no |
| 15 | J3 | 1×5 header, 2.54 mm | ICSP | no |
| 16 | JP1 | 1×2 header | debug enable | no |
| 17 | JP2 | 1×2 header | isolates C8 for programming | no |
| 18 | **D1** | LED, **red** | power / heartbeat, on RC0 | **yes — long leg is +** |
| 19 | **D2** | LED, **yellow** | CAN status, on RC1 | **yes — long leg is +** |
| 20 | **C6** | 10 µF 16 V electrolytic | supply input tank | **yes — long leg is +, stripe is −** |
| 21 | J1, J2 | Micro-Fit 43045-0400, right-angle | the two 4-pin connectors, in parallel | **yes — keyed, cannot be got wrong** |
| 22 | **U1** | PIC18F25K80 | **into its socket, last** | **yes — notch** |
| 23 | **U2** | MCP2562-E/P | **into its socket, last** | **yes — notch** |

**23 fitted parts and two sockets**, which is the count in the paragraph above.

**Do not press the chips into their sockets until everything else is done and
checked.** They are the two parts a soldering mistake elsewhere can destroy,
and they are the only two that come out again without a desoldering braid.

**LED colour is free** — any colour works. Through 1 kΩ the whole span lands
between about 3.2 mA at Vf ≈ 1.8 V (red, yellow) and 1.1 mA at Vf ≈ 3.2 V
(blue, white, true green), all far under the 25 mA the port pin allows, so only
the brightness changes. **The design carries red for D1 and yellow for D2**,
both measured at Vf ≈ 1.8 V before fitting.

**If you fit something else, change it in the schematic's Value field** in
`kicad` and regenerate the BOM with the `kicad-cli` command in that repository's
plan §7 — `fab/` is generated from the schematic, so a wrong colour there
becomes a wrong colour in the file a supplier reads.

### The joints that need more heat than they look like

**Every ground pad on this board hangs on a pour that is filled on both
layers** — `kicad/canfuel/docs/solder-check.md` says so, which is also why it
uses "any ground — J3 pin 3" as the place to put the black probe. A pour
that size carries heat away from a joint about as fast as a small iron delivers
it, and the failure that produces is not a bridge and not a joint that looks
dry: **the solder melts, balls up against the iron and never wets the pin at
all**, while the pad beside it on a signal net takes solder normally. It looks
like a finished joint from above.

**Heat the pin and the pad together for three to four seconds before the solder
touches either**, then feed the solder into the joint rather than onto the
iron. That applies to every ground pad here, and there are more of them than
you would guess: **the second pad of all eight capacitors**, both LED cathodes,
R2 pad 2, pin 2 of J1 and J2, U2 pin 2, and the VSS pins of the PIC socket.

**J3 pin 3 is the one that bites**, because it is a ground pad on the one
connector that gets plugged and unplugged. A pin held only by friction in the
plastic slides when the plug is pushed on, and what that produces is an ICSP
link that comes and goes: IPECMD prints `Target device was not found (could not
detect target voltage VDD)` and **exits 0**, which step 4 reads as an unpowered
board. Two joints on the same header behaving differently is the tell.

**Strain relief on J3 is worth the two minutes** whatever the joints look like,
since every programming run pushes on it. A fillet of neutral-cure adhesive
around the base of the header does it, kept low enough that the plug still
seats fully — Pattex ONE FOR ALL Crystal is an MS polymer, so it releases
methanol rather than acetic acid and does not corrode copper or solder, and a
scalpel takes it off again if the header ever has to come out.

### The five that can go in backwards

Written out for somebody holding a soldering iron for the first time, because
"check the polarity" is not an instruction unless it says how.

**Have `kicad/canfuel/docs/assembly-orientation.svg` open while you do it.** It
draws both sides of the board out of `canfuel.kicad_pcb` — the copper, the
silkscreen, every designator and the values — and puts a `+` and a `−` on the
two pads of each part below, so the answer is a picture rather than a paragraph.
Its polarity comes from the netlist rather than from a table somebody typed, so
it cannot disagree with the board. What it cannot tell you is which leg of the
part in your hand is which, which is what the rest of this section is for.

**Everything not in this section is symmetric** — every resistor, every ceramic
capacitor, the crystal and all three headers. Fit those either way and they
work.

⚠ **Do not invent a rule from the pad numbers.** On C6 pad 1 is the **positive**
lead; on D1 and D2 pad 1 is the **cathode**, the negative one. They are
opposite. This is not a guess — `kicad/tools/check-netlist.py` pins `C6.1` to
`+5V` and `D1.1`/`D2.1` to `SGND`, and CI fails if the board ever disagrees.

| Part | Which end is positive | How the board says so |
|---|---|---|
| **D1, D2** — the LEDs | **long leg = anode = +**; the plastic rim is flattened on the *other* side, beside the short leg | the silk outline carries the same flat on the cathode side. The anode is the pad wired to its resistor (R3 for D1, R4 for D2) |
| **C6** — the electrolytic | **long leg = +**; the can has a printed stripe down the **negative** side | pad 1 is `+5V` |
| **U1, U2** — the chips | notch or dot at the pin 1 end | matching notch on the silk outline — **but see the socket note directly below, because by then the silk is covered** |

#### The sockets hide the marking they are aligned to — record it first

**The order of events is the trap, not the parts.** Soldering a socket the
wrong way round does nothing: 28 holes onto 28 pads, symmetric either way.
Orientation only matters when the chip goes into the socket — and that happens
last, by which time the socket body is sitting on top of the board's pin 1
notch.

**So do one of these before the socket is soldered, while the silk is still
visible:**

- **Photograph the bare board**, close, with the pin 1 end of both DIP outlines
  in frame. Thirty seconds, and it survives being put in a drawer for a week.
- **Or transfer the mark** — a dot of permanent marker on the board *outside*
  the silk outline, where the socket will not cover it.
- **Or align a notched socket.** Many DIP sockets have a bevel or notch at one
  end; if yours do, line it up with the silk notch and the socket carries the
  information from then on. **Do not assume yours are notched** — plenty are
  plain, and a plain socket destroys the marking without replacing it.

**And the recovery, if all of that is missed** — it needs no photograph and
works after everything is soldered, with the same multimeter in continuity
mode:

- **U1 pin 1 rings out to J3 pin 1.** Both are the `~MCLR` net, so touch one
  probe to the ICSP header's pin 1 and find the socket hole that beeps. That
  is pin 1 of U1, whatever the socket looks like.
- **U2 pin 2 rings out to SGND** and pin 3 to +5 V. Pin 1 is the corner pin on
  the same side, immediately next to the ground one.

Both come from `kicad/tools/check-netlist.py`, which CI checks against the
schematic, so they cannot quietly stop being true.

**The check that needs no memory, and the multimeter is already on the list
above.** Set it to diode mode, red probe in the `VΩ` jack and black in `COM`,
and touch the probes to the two legs: one way round **the LED lights faintly**
and the display reads its forward voltage in volts, the other way it stays dark
and reads open. **The leg on the red probe when it lights is the anode.** Five
seconds, and it settles the question on the part in your hand — which matters,
because leg length is the marking most easily destroyed.

Two things that make the difference between this working and looking broken:

- **Do it in shade.** Diode mode drives well under a milliamp, so the LED is
  dim. In daylight it looks dead either way round.
- **Red, yellow and green light; blue and white may not.** A meter's diode
  source is only a few volts, which clears the 1.8–2 V those need and can fall
  short of the ~3.2 V a blue or white one wants. If a blue LED stays dark both
  ways, it is the meter, not the LED — fall back to the long leg and the flat
  on the rim. **The board's own two are red and yellow, and both were confirmed
  this way**, reading Vf ≈ 1.8 V.

**So trim the legs after soldering, never before.** Once both are cut level the
only marking left on an LED is the flat on the rim, and on C6 only the stripe.

**C6 is the one worth slowing down for.** An aluminium electrolytic fitted
backwards heats, can vent, and does it with the car's 5 V behind it. A backwards
LED simply never lights — annoying, and harmless. If you only double-check one
part, check that one.

*(The polarity markings on the parts themselves are the ordinary industry
convention rather than something quoted from a datasheet: `hitano-exr-datasheet.pdf`
specifies ratings and dimensions and says nothing about the stripe, and no LED
datasheet is held — see the sourcing rule in `kicad/CLAUDE.md`, which exempts
both. The board side of the table is verified; the meter is what makes the part
side certain.)*

**And Y1 really is symmetric**, since it is the part people expect to be
polarised and it is not. `Crystal:Crystal_HC49-U_Vertical` has exactly two
pads — no case-ground pin — and a quartz resonator is a two-terminal device
with no anode or cathode. Fit it either way.

### The other way to get it wrong: right part, wrong slot

Orientation is one axis and the five parts above are all of it. **The second
axis is value**, and nothing on the board stops you putting the right kind of
component in the wrong place. Two pairs are worth a moment each, because both
fail quietly.

- **The resistors.** Three values in an identical body: 10 kΩ (R1, R2), 1 kΩ
  (R3, R4) and 470 Ω (R6). Colour bands are the classic misread. Swapping R6
  and an LED resistor is the one that matters — DS39977C Figure 2-2 note 2 puts
  a **≤ 470 Ω** ceiling on the MCLR series resistor, so a 1 kΩ there is outside
  what the datasheet asks for, while 470 Ω in an LED's place only makes it
  brighter and is harmless.
- **The ceramic capacitors, and this is the expensive one.** 33 pF (C1, C2) and
  100 nF (C3, C4, C5, C8) come in the same 5 mm disc. **100 nF on the crystal
  pins stops the oscillator starting at all** — the board is then completely
  dead in a way that looks exactly like a bad chip, a bad programming run or a
  firmware fault, and you would go looking in all three before suspecting a
  capacitor. The reverse swap leaves a supply pin undecoupled, which is subtler
  and worse to chase.

### Measure every part that has a value, before it goes in

**The general rule, and it is worth more than any of the specific warnings
above: if a part has a value you can measure, measure it before you solder
it.** Not because the markings are usually wrong — they are usually right — but
because reading a marking and measuring a part fail in different ways, and only
one of them is caught after the part is in the board.

It is thirteen of the twenty-three parts and one dial position on the meter.
`Select` cycles that position between resistance, capacitance, diode and
continuity:

| Mode | Parts | What you are confirming |
|---|---|---|
| **Ω** | R1, R2 (10 kΩ), R3, R4 (1 kΩ), R6 (470 Ω) | the value, against a colour code that is easy to misread |
| **capacitance** | C1, C2 (33 pF), C3, C4, C5, C8 (100 nF), C6, C7 (10 µF) | the value, and that the part is not open or shorted |
| **diode** | D1, D2 | which leg is the anode, and that the LED lights at all |

**The ten with nothing to measure** are U1, U2, both sockets, Y1, J1, J2, J3,
JP1 and JP2. A quartz crystal is not measurable with a multimeter at all — an
ohmmeter reads open and a capacitance range reads only the holder's few pF —
but there is exactly one crystal in the box, so there is nothing to confuse it
with.

Everything is out of circuit at this point, which is the condition every one of
those ranges wants, so this is the easiest it will ever be. Once a part is
soldered, measuring it means measuring whatever else shares the net.

Resistance is unambiguous. So is capacitance here: 33 pF against 100 nF is a
factor of three thousand, so no accuracy at the small end is needed to tell
them apart.

⚠ **The marking that catches people out** is the three-digit code on the discs.
`104` is 10 followed by four zeros in picofarads — **100 nF**. And **33 pF is
often printed `330`**, meaning 33 followed by no zeros, *not* 330 pF. The two
codes look like near neighbours and are three orders of magnitude apart. This
is convention rather than anything cited; the meter settles it.

### And measure again after it is soldered

The section above catches a misread colour code and nothing else. **A joint
fails in two directions and neither one is visible**, so each pad gets two
readings rather than one:

- **open** — the iron never wetted the pad, or the lead moved as it cooled.
  Continuity to the other end of the net proves it did not happen.
- **bridged** — solder reached the nearest copper, **which is hardly ever the
  next pad along**. SGND is poured on both layers, so for most pads the nearest
  copper is ground, three tenths of a millimetre away, on every side.

**Both readings, for every pad on the board, are in
`kicad/canfuel/docs/solder-check.md`.** It is generated from the board by
`kicad/tools/render-solder-check.py` — the nets out of the netlist, the
distances out of the filled copper — so there is nothing in it anybody typed
and nothing in it that can go stale. Look up the part you have just soldered
and it names where the meter must show zero and what it must stay open to,
with the gap in millimetres and a hole you can find by eye for each one.

Three things that make the difference between that table working and being
ignored:

- **Do it part by part, as you go.** That is the whole reason the solder order
  exists: while a part is the newest thing on the board, every reading is of
  that part. Once its neighbours are in, you are measuring the net.
- **Resistance, not the beeper, for anything with a capacitor across it.** The
  part charges through the meter, so the beeper chirps once and goes quiet —
  that chirp is the capacitor, not a bridge. Watch the number climb and settle
  in megohms or `OL`. A steady near-zero that never moves is a bridge.
- **The distances are copper edge to copper edge, as designed.** Solder mask
  sits between most of them, which makes a bridge less likely and not
  impossible.

**C7 is the worked example, and it is the one that needs the table most**,
because its second pad has no track at all — it *is* the ground pour, which is
why nothing appears to leave it. Measured on the first board:

| Reading | Between | Result |
|---|---|---|
| capacitance | U1 pin 6 hole and U1 pin 8 hole | **10 µF** — both joints and the track to pin 6 |
| resistance | U1 pin 6 hole and ground | **megohms** — no bridge to the pour, 0.30 mm away |
| resistance | U1 pin 6 hole and JP1 pin 2 | open — `DBG_EN` passes 0.37 mm below that pad |
| resistance | ground and J3 pin 5 | open — `PGC` passes 0.38 mm above the other pad |

Both of those tracks run **under the body of the capacitor**, across the
1.8 mm gap between its pads, which is not something the eye finds afterwards.

### Programme

⚠ **JP2 comes off before programming and goes back on afterwards.** It puts the
100 nF MCLR capacitor in circuit, which is what the datasheet asks for in
normal operation and what interferes with ICSP. No tool can check this for you.

**With the PICkit on J3, one command builds and flashes:**

```
cd canfuel
python tools/flash.py --mode loopback
```

`tools/flash.py` builds the mode you asked for, checks that the hex really is
that mode and that `CANMX` in it is set, then runs the commands below and reads
their **output** rather than their exit code. It stops at the first thing that
did not happen, and says which of the known failures it was.

Building on its own is `make -C mplab CAN_MODE=LOOPBACK`, and it is documented
in `mplab/README.md` — which XC8 and which Device Family Pack, neither
optional. The makefile builds; it does not programme.

**What the tool runs, and what to run by hand if it is ever in doubt** — from
the repository root, in this order, reading each one's output before the next:

```
ipecmd -P18F25K80 -TPPK3 -I                                  # 1. device ID
ipecmd -P18F25K80 -TPPK3 -C                                  # 2. blank check
ipecmd -P18F25K80 -TPPK3 -F"$PWD/mplab/build/canfuel.hex" -M -OL   # 3. program
ipecmd -P18F25K80 -TPPK3 -F"$PWD/mplab/build/canfuel.hex" -Y       # 4. fails, see below
```

Command 1 is the one that matters most and it is read-only: **a device ID that
comes back correct means the ICSP wiring, the MCLR jumper and the part are all
good, before anything has been written.** If it fails, nothing after it can
succeed and there is no point trying.

⚠ **Read its output, not its exit code**, and know which of the two failures you
are looking at:

| What it prints | What it means |
|---|---|
| `Target device was not found (could not detect target voltage VDD)` | **the board has no power** — or J3 pin 3 is not actually soldered to the ground pour, which behaves the same way and comes and goes as the plug moves; see step 5. Otherwise nothing reached the part, so JP2 and the ICSP wiring are not the suspects. `-W` is not used here, so the board needs its own 5 V |
| `Target Device ID (0x0) is an Invalid Device ID` | **power is fine, ICSP is not.** JP2 still fitted, wiring on MCLR/PGC/PGD, or a dead part |

The first one still exits 0, so a script checking `$?` would sail straight past
an unpowered board — the likeliest bench mistake there is. Both were provoked
without a board and the observed codes are in
[`flash-tool-notes.md`](flash-tool-notes.md).

**Command 4 can fail on a correctly programmed board, and that is not a
fault.** `-Y` verifies EEData as well as program memory and configuration,
against a hex that carries no EEPROM section, so it expects an erased `0xFF`
at address 0 — which is the low byte of `total_ul` in slot 0 of the persist
ring. Whether the part still holds `0xFF` there depends on what the firmware
has had to store since `-OL` released it from reset, and `-OL` runs before the
verify does.

On a bench with nothing on the bus it stays erased and the verify passes:
`persist_load()` finds nothing on a virgin EEPROM, and `persist_save()`
refuses to write a record that says nothing, so the ring is not touched until
an accumulator moves. Attach a live bus, or reflash a part that has already
driven with `-Z0-3FF`, and the first record lands within a second. The run
then prints

```
EEData memory
Address: 0 Expected Value: ff Received Value: 0
Verify failed
```

and **exits 7**, while `-M` above it printed `Program Succeeded`. So command 4
is free rather than required in a second sense: `-M` verifies implicitly when
it finishes programming, and that implicit verify is the one that counts — and
it is the one that does not depend on what the firmware has been doing in the
meantime.

Three things in that command line are ways to get it wrong. The full argument
for each is in [`flash-tool-notes.md`](flash-tool-notes.md):

- **`-OL` is not optional.** It is *Release From Reset* and the IPECMD default
  is the opposite, so leaving it off produces a board that is programmed
  correctly and then simply sits there — which looks exactly like a firmware
  that does not run.
- **`-W` is deliberately not used.** Power the board from the display or a bench
  supply first, then attach ICSP.
- **The EEPROM is erased, on purpose**, and that is the right default during
  bring-up: `persist_load()` returns false on a virgin EEPROM, which is a
  correct start rather than an error. `-Z0-3FF` is what preserves the ring once
  there is a real trip in it, and `python tools/flash.py --preserve-eeprom` is
  that switch with the check attached — it reads EEData before and after and
  compares them, because a preserve that silently did not happen is
  indistinguishable from one that did until the trip is gone. **`mplab/canfuel.X`
  deliberately does the opposite** — know which tool you are holding.

⚠ **What has been run against a real part, and what has not.** `-I`, `-C`,
`-M -OL` and `-Y` have all run against a powered PIC18F25K80 on J3, from Git
Bash, with the `$PWD` form of `-F` resolving correctly. Their observed output
and exit codes are in [`flash-tool-notes.md`](flash-tool-notes.md). **`-Z` has
not been run, and neither has reading memory back off the part** — a tool that
wants either has to establish it first.

**Fit JP1.** Without it both LEDs stay dark by design and the diagnostic frame
is not transmitted, and you are about to need both.

---

## 6. Loopback on the desk

**The loopback hex from step 5 is already in the device**, so this costs ten
minutes and needs nothing further: no bus, no adapter, no transceiver, no car.
Just 5 V and JP1 fitted.

DS39977C §27.3.5 hands the transmit buffers straight to the receive buffers, so
the module talks to itself. That is all it does, and the section below is
honest about how little it therefore proves — but it is the cheapest check
there is, and the one fault it does catch is fatal.

| LED_PWR | LED_CAN | Means |
|---|---|---|
| slow blink | **dark** | **the pass.** See below — dark is the expected state here, not a fault |
| slow blink | 5 Hz blink | `hal_can_init()` never got the module into the mode it asked for. A configuration register or the bit timing is wrong. **Stop here** |
| steady | any | **wrong hex.** A steady LED_PWR means a normal build; you flashed the wrong one |
| dark | dark | JP1 is not fitted, or the board is not running at all |

⚠ **Dark LED_CAN is the pass, and this is worth understanding rather than
memorising**, because it is the opposite of every other step.

`LED_CAN` follows `compute_data_live()`, which is set only by a **0x480** frame
— the fuel counter is the heartbeat. In loopback the module receives only the
frames it sent itself, which are 0x600–0x603, and those do not match any of the
six hardware acceptance filters, so they are rejected before reaching the FIFO.
No 0x480 can ever arrive. **LED_CAN steady is not merely unlikely in this step;
it is unreachable.**

**So be honest about what this step proves**, which is less than it looks:

- the scheduler runs and the part is alive — `LED_PWR` is blinking
- `hal_can_init()` reached the mode it asked for, which means the configuration
  registers were accepted and `CANMX` put the pins where the board has them —
  that is what the 5 Hz blink would deny

and **not** the receive path, the FIFO depth, the acceptance filters or
`decode`. Those need frames from outside, and **step 7 is where they are
tested** — which is a large part of why step 7 is worth doing.

A fault caught here costs a reflash. The same fault caught in step 8 costs a
trip to the car, and in step 9 it puts error frames on the car's bus.

---

## 7. *(recommended)* A bench bus, with a verdict instead of a blink rate

**Nothing later breaks without it — and it is still the step to do**, because
step 6 covers less than its name suggests. Loopback proves the module accepted
its configuration and reached its mode, and it cannot prove anything about
receiving: the only frames arriving there are our own, and the acceptance
filters reject them. **So without this step, the first time the receive path,
the six hardware filters, the eight-deep FIFO and `decode` run at all is in the
car** — where a failure costs a trip and the only instrument is a blinking LED.

**The four parts are not equally worth it:**

| | Needs | Worth |
|---|---|---|
| **7.1** traffic | 1 adapter | **do it.** The first proof the receive path works at all |
| **7.2** scenarios | 1 adapter | **do it.** The only test of the six acceptance filters anywhere |
| **7.3** fault injection | 2 adapters | the optional one. Answers "does it recover" early rather than never |
| **7.4** listen only | 2 adapters | **do it if you have two.** The only check that the listen-only hex is really silent before it meets the car's bus |
| **7.5** persistence | 1 adapter, and a hand to pull the power | **do it.** The only test of the real EEPROM write path anywhere |

**With one adapter, run `--all-one-device`**, which is 7.1 and 7.2 — the cheap
half, and exactly what step 6 cannot reach. The order is a prefix rather than a
different set, so nothing is skipped in the middle.

**7.4 is last on purpose.** It is the only part wanting a different hex;
anywhere earlier it would cost a third flash, and at the end it leaves the
device holding exactly what step 8 asks for next.

**Termination is the adapters' own jumper**, so there are no loose resistors to
find — see the measurement below.

### Build the bus

CANH to CANH, CANL to CANL, converter to adapters, on a breadboard. The board's
own R5 is deliberately not fitted, so both terminators are the adapters'.

⚠ **Measure across CANH and CANL with everything powered down and expect
50–65 Ω.** That is DS20005167C's own specified load range for `VO(D)`, the
dominant output voltage. Two terminators of 120 Ω give 60 Ω, in the middle of
it. **Measure rather than count jumpers** — three terminators on the bus give
40 Ω, which is below what the transceiver is specified to drive, and the meter
settles in five seconds what no datasheet can, because it is your hardware.

### Leave an acknowledger running, and the bench stops lying to you

```
python tools/acker.py --port COM6        # in its own window, until Ctrl-C
```

**Start this before the converter and leave it up.** A CAN transmitter needs
one other node to pull the acknowledge slot dominant, and on a bench the
converter is regularly the only node with its channel open — every gap between
a flash and the next test is one. In that gap nothing acknowledges it, so every
frame is retransmitted, the transmit error counter climbs to the error-passive
limit and stays there, and:

- **`UNHEALTHY` latches**, so `LED_CAN` blinks for the rest of the session and
  the flag in 0x603 says nothing until the next reset
- **the refusal counter saturates at 255**, because all three transmit buffers
  are permanently busy
- both read exactly like a converter with a real fault, and cost an hour each
  time

With the acknowledger up, a board flashed underneath it boots onto a live bus
and comes up clean: `flags CAN_OK DATA_LIVE`, refusals 0, LED steady. It
transmits nothing itself — acknowledging is a hardware function of the CAN
controller rather than a frame — so it cannot disturb a measurement.

⚠ **Normal mode, not listen only.** An adapter in listen-only is silent in the
acknowledge slot too. That is exactly what 7.4 needs and exactly what is
useless here.

⚠ **It holds a serial port**, so stop it before 7.3 and 7.4, which want two
adapters of their own. 7.1, 7.2 and 7.5 need one and leave the other free.

```
python tools/bench_test.py --all --port COM5 --port2 COM6
```

runs all four in the order below and prints one verdict; `--all-one-device`
runs just 7.1 and 7.2. Each also runs alone (`--traffic`, `--scenarios`,
`--fault`, `--listen-only`).

### 7.1 — traffic, and the answers read back

```
make -C mplab                            # normal build, and it stays for 7.1-7.3
python tools/bench_test.py --traffic --port COM5
```

Replays a real recording from the vehicle and checks that 0x600 and 0x601 come
back at 10 Hz, 0x602 and 0x603 at 1 Hz, that the error counters are zero and
that the converter did not restart mid-run. One adapter is enough. With
`--port2` the second one listens, which makes the frame counts an independent
measurement instead of the transmitter's own account of itself.

**It also checks the converter's clock against the host's**, from two 0x603
frames and their uptimes. Everything the device reports is integrated against
that millisecond clock — 16 MHz / 4, prescale 4, `PR2` = 249, postscale 4 — and
a mistake anywhere in that chain still runs, still transmits, and scales every
distance, flow and average by the error, with nothing on the display to suggest
it. **No host test can catch it**: they feed the core a clock of their own, and
a recording cannot check the clock it was made with.

**And VddConv is worth one meter reading here.** 0x601 carries the supply the
PIC measures on itself, and the 1.024 V band gap it measures against has *no
tolerance given anywhere in the datasheet* — so it is a trend, not a voltmeter.
Comparing it once against a multimeter at the board gives this unit's offset,
which is the only calibration it will ever get and takes ten seconds while the
bus is already running.

### 7.2 — four behaviours, end to end over the wire

```
python tools/bench_test.py --scenarios --port COM5
```

The frames are **real ones with one field overwritten** — the speed bytes of a
recorded 0x1A0, the counter of a recorded 0x480. Building them from scratch
would mean writing the inverse of `decode.c` from the table `decode.c` came
from, and `CLAUDE.md` is explicit that twins do not catch a shared fault.

| | Scenario | What it proves |
|---|---|---|
| A | traffic stops for 2 s, then returns with the counter from zero | everything derived from the bus goes to 0 and **VddConv does not**; it recovers within a second; an ECU counter restart invents no fuel (trap 2) |
| B | 2 km/h, then 60 km/h, then a wild flow at 5 km/h | FuelNow switches unit at 4 km/h and stops at **99.9**, rather than wrapping |
| C | standing still, throttle at rest, b7 raised to 42 | Torque and Power read **exactly zero** — the driving gate, with the value the air conditioning produces |
| D | an unaccepted identifier flooded **alongside** real traffic | the six hardware acceptance filters hold |
| E | standing still, then the tank rises 12 L | **the refuelling reset fires** and the trip clears — otherwise only testable at a petrol station |

**D is the one worth the trip.** The filters exist only in silicon and nothing
in the host suite can reach them. The check is not "nothing changed" — it is
that **0x600 keeps arriving at full rate with correct values, no overflow, and
`UNHEALTHY` clear**. If a filter leaked, the FIFO would fill with junk and real
frames would be dropped, which shows up as a rate that sags.

Being honest about its limit: one adapter over a serial link pushes something
like the car's own bus load, not a saturated 500 kbps bus. It is a load test
against reality, not against the worst case.

⚠ **The host is the bottleneck long before the converter is.** Six frames every
10 ms is 600 a second, and at 22 bytes of slcan text each that is 132 kbit/s
against a link nominally configured at 115200. The USBtin is a USB CDC device,
so the configured baud rate is not the real limit — but if the write buffer
does back up, the schedule slips and a scenario silently runs at less than the
condition it claims. **Every run reports the fraction of the intended rate it
achieved and says so when it falls below 90 %**, so a slow host reads as a slow
host rather than as a converter that failed to keep up.

### 7.3 — break the bus, then prove it recovers

```
python tools/bench_test.py --fault --port COM5 --port2 COM6
```

Intermittent CAN faults are the ones that are hard to chase in a car. Both
injections here are pure adapter commands — nothing is unplugged:

- **No acknowledgements.** Both adapters switch to listen-only, so nothing
  on the bus drives the ACK slot. **No stimulus is sent during this window, and
  none can be** — an adapter in listen-only refuses to transmit — so the only
  thing on the wire is the converter's own frames, which is all this needs. Its
  transmit error counter climbs by 8 per failed try to the error-passive limit
  of 128 — **and stops there. It does not go bus-off and it does not fall
  silent**: it retransmits for as long as the starvation lasts, measured at
  **1812 frames a second against 22 nominal**, and that flood is the
  observation. `docs/refuted.md` E7 carries what this used to claim and
  what refuted it. Then the adapters go back to normal, the counter walks
  back down and the module returns to error-active on its own. DS39977C
  §27.11: recovery from bus-off is 128 × 11 recessive bits with no MCU
  intervention — which is the path this test does *not* take.
- **A node at the wrong bit rate.** One adapter transmits at 250 kbit/s
  into a 500 kbit/s bus, which produces real error frames and drives the
  *receive* counter up. Then it stops and the counters must come down.

**The check that matters is `UNHEALTHY` after recovery.** Both error counters
walk back to zero as normal traffic resumes, so a converter that spent six
seconds unacknowledged reads perfectly clean afterwards — and the latched flag
is the only trace that anything happened. This test is the only proof that
latch works.

If it does **not** recover, power-cycle the board and say so: that is a real
finding, and far better found here than in the car.

### 7.4 — listen only, and the one thing a human must confirm

```
make -C mplab CAN_MODE=LISTEN_ONLY      # the one reflash in step 7
python tools/bench_test.py --listen-only --port COM5 --port2 COM6
```

**Last on purpose.** This is the only part of step 7 wanting a different hex,
so running it anywhere earlier would cost a third flash — and finishing here
leaves the device holding exactly the build step 8 asks for next.

**Why the second adapter is not optional here.** CAN requires a receiver to
drive the acknowledge slot dominant, and a listen-only converter never will —
DS39977C §27.3.4 promises exactly that, "no messages will be transmitted while
in this state, including error flags or Acknowledge signals". With one adapter
the transmitter is alone on the bus: nothing acknowledges and every frame is
retransmitted for ever, at eighty times the intended rate — see 7.3, where that
is deliberate. The second adapter is opened normally and transmits nothing at
all; acknowledging is its entire job.

Two things the script checks itself, and they are not nothing:

- **the converter transmits absolutely nothing** — zero frames on 0x600–0x603
  over the whole run. A listen-only build that transmits is a bug, and this is
  the only place it would be caught.
- **neither adapter reports a bus error**, which is also the proof that the
  second adapter really is acknowledging.

Then comes the one question no frame can answer, because in this mode the
converter cannot speak: **is LED_CAN steady, and is LED_PWR blinking slowly?**

**The LEDs only mean anything while traffic is flowing**, so the run does not
ask afterwards — it holds the bus alive for `--observe` seconds (30 by default)
and prints a banner saying to look now. Somebody looks; the answer is recorded
on a second invocation, which re-runs the machine checks too — so give it
`--seconds 5` unless you want the whole run twice:

```
python tools/bench_test.py --listen-only --observe 30 --port COM5 --port2 COM6
python tools/bench_test.py --listen-only --observe 0 --seconds 5 --port COM5 --port2 COM6 \
       --led-can steady --led-pwr slow
```

**Nothing in this tool prompts.** It is built to be driven by somebody — or
something — that cannot see the board, with a person nearby to ask, so every
question is a flag rather than a `y/n`. An unreported LED state is reported as
**unconfirmed**, never as a pass: 7.4 is incomplete without it, and saying so is
the point.

### 7.5 — the accumulators survive a power cycle

```
python tools/bench_test.py --persist-arm --port COM5
#   ... power-cycle the board when it says to ...
python tools/bench_test.py --persist-check --expect-trip-ml 1234 --port COM5
```

**This is the only test of the real EEPROM there is.** `test_persist.c`
simulates 100,000 write cycles against a RAM array, which proves the ring
arithmetic and the wear levelling and says nothing whatever about
`hal_eeprom_write()` — the `0x55`/`0xAA` unlock, `WREN`, polling `WR`, and the
deliberate decision to restore `GIE` while that poll runs. All of it was
datasheet reading that no hardware had executed until this step was run for the
first time; run it again after anything touches `persist.c` or the write, since
nothing else can.

**And the failure is invisible until it is expensive**: the device works
perfectly, the display is right, and then the ignition goes off and every trip
is gone. In the car that reads as "it forgot", months later, with nothing to
point at.

Part 1 drives 30 s of moving traffic — comfortably more than the 20 s
`PERSIST_INTERVAL_MS`, so at least one real write happens — and prints the
trip. Part 2, after the power cycle, checks three things: that the reset cause
really is **power-on** (without which the test proves nothing), that
`PERSIST_OK` is set so a record was found, and that the trip came back rather
than starting from zero.

⚠ **Up to 20 s of accumulator is lost at every power-off by design**, so part 2
allows a band rather than an equality. `src/persist.h` has that arithmetic and
why it is not a bug.

**It costs the EEPROM nothing worth counting.** Writes happen at
`PERSIST_INTERVAL_MS` and only on change, so a full `--all` run plus this pair
is about **13 writes**. The ring spreads them over 64 slots against D120's
100,000-cycle minimum, which is 6.4 M writes — 4.1 years of engine-on time, or
20 seconds of driving per write. **A whole bench session costs about four
minutes of driving.** A thousand of them would spend 0.2 % of the budget.

### Afterwards: the EEPROM holds bench data

These scenarios drive synthetic tank levels and fuel totals into the persist
ring. In the car that reads as a wrong trip and a wrong Range, and the
refuelling detector would be comparing against a level that never existed.

**The reflash at the start of step 8 clears it** — the erase is on by default,
so simply do not pass `-Z0-3FF`, and do not run `flash.py --preserve-eeprom`
there. Nothing extra to run.

**And you can prove it was cleared**: on the next run, 0x603's `PERSIST_OK`
flag comes back **clear**, because `persist_load()` returns false on a virgin
ring. That is a correct start, not an error.

---

## 8. Listen only, in the car

```
make -C mplab CAN_MODE=LISTEN_ONLY
```

Flash it with the same four commands as step 5, fit JP1, wire the board in
through the Y-splitter, and switch on.

⚠ **Do not pass `-Z0-3FF` on this reflash, and if you did step 7 that is not
optional.** The default erase is what clears the synthetic tank level and trip
totals the bench scenarios left in the EEPROM; carried into the car they would
read as a wrong Range and a wrong average, and the refuelling detector would be
comparing against a level that never existed. **From the next reflash onwards
it is the other way round** — by then the ring holds a real trip, and the
command is

```
python tools/flash.py --preserve-eeprom
```

which passes `-Z0-3FF` and then proves it worked rather than assuming: it dumps
EEData before and after and compares them byte for byte. Erasing a real trip
is not undoable, so the check is not optional either.

⚠ **Put the board where you can see both LEDs**, and leave the dashboard open
until step 11. In this step and this step alone, the LEDs are the *only*
instrument there is — see below.

**Why this mode first, and it is not caution for its own sake.** The 500 kbps
bit timing is datasheet arithmetic that no hardware has ever executed. A
Normal-mode node whose timing is wrong does not merely fail to read the bus —
**it fills the bus with error frames** and takes the car's own modules down with
it. Listen Only is silent by the module's own guarantee (§27.3.4): no
transmissions, no error flags, not even acknowledgements.

⚠ **In this step the LEDs are the only instrument, and that is a property of
the mode rather than a gap in the tooling.** The diagnostic frame 0x603 carries
the ECAN error counters as numbers everywhere else — but a listen-only node
transmits *nothing*, so there is no frame to read. Nor can they be read over
ICSP: IPECMD reaches flash and EEPROM, not RAM. A debugger would do it, and
that means the IDE this project does not use.

So: **this is what to look for, and there is nothing else to look at.**

| LED_PWR | LED_CAN | Means |
|---|---|---|
| slow blink | **steady** | frames arriving, error counters zero — **this is the pass** |
| slow blink | 2.5 Hz blink | arriving, but an error counter is non-zero or the FIFO overflowed |
| slow blink | 5 Hz blink | the module never reached Listen Only |
| slow blink | dark | the bus has been quiet for 500 ms — the car is not talking, or the wiring is wrong |
| **steady** | any | **wrong hex** — that is a normal build, and it is transmitting |

Two pairs are worth separating deliberately:

- **Dark against 5 Hz.** Dark means the car is not talking; fast blink means we
  are not listening. Opposite faults, and they look alike from across a car.
- **Steady against slow blink on LED_PWR.** Slow is correct here. A steady
  LED_PWR in this step means the listen-only hex is not the one in the device.

**A bit-timing fault shows up as 2.5 Hz within seconds of switching on**, so
watch LED_CAN before anything else. If it settles steady, the 500 kbps
arithmetic carried onto real silicon — which nothing before this step could
prove.

Log what the converter decodes and compare it against a parallel USBtin
recording. Nothing is on the wire from us yet, so there is nothing to break.

---

## 9. Transmit

```
make -C mplab
```

A plain build with no `CAN_MODE`, which is Normal mode. Keep JP1 fitted and the
dashboard open for this step too.

**How you know it is transmitting — both LEDs on, steady.**

| LED_PWR | LED_CAN | Means |
|---|---|---|
| **steady** | **steady** | **the pass.** A normal build, frames arriving, counters zero |
| steady | 2.5 Hz blink | transmitting, but an error counter is non-zero — see below |
| slow blink | any | still a silent build. You flashed the wrong hex |

`LED_PWR` going from slow blink to steady is the whole point of that indicator:
a listen-only hex left in the device by accident is otherwise indistinguishable
from a transmitter that has quietly stopped working.

**Two LEDs steady is necessary and not sufficient**, because LED_CAN means
"frames are arriving", which was true in step 8 as well. The confirmations that
we are actually on the wire:

- **the display's seven converter channels come alive within a second.** That
  is the real proof and it needs no instruments.
- **0x603 is now readable**, because a normal build transmits. With a USBtin on
  the bus, `python tools/canlog.py --dump --id 0x603 FILE` over a short capture
  gives the error counters, the reset cause and the uptime as numbers —
  `docs/frames.md` decodes the bytes. This is the first time in the car that
  the counters can be read rather than inferred.

This is the first time the device acknowledges frames and arbitrates for the
bus, so watch it for a few minutes rather than a few seconds.

---

## 10. Check it against the raw counter

The useful check once it is live, and it needs no instruments:

**Compare `FuelNow` against `FuelCntRaw` on the display.** `FuelCntRaw` is the
ECU's counter with no conversion applied at all — it comes straight off 0x480.
So if it rises while `FuelNow` shows nonsense, the fault is in **this
firmware's arithmetic** rather than in its input. If neither moves, the fault is
upstream of us.

⚠ **`UNHEALTHY` after a TRI upload is the display, not the converter.**
Operating the MFD15 through oDSS — uploading a file, changing its
configuration — produces a burst of CAN errors that latches the flag until the
next power-up, with the counters back at zero straight afterwards.
`docs/frames.md` has what was observed and what is still unexplained about it.
Power-cycle before reading that flag as a verdict on this board.

Two more worth doing on the first drive:

- **Range and FuelTank should agree with each other.** They read the same damped
  tank level; if one moves and the other does not, something is wrong in
  `compute.c`.
- **Refuel and watch the trip average clear.** The reset fires on five
  consecutive at-rest samples more than 3 L above the settled tank level, so
  about five seconds of standing still after the fill. `docs/refuel-reset.md`
  has the rules and the corner cases.

---

## 11. Close it up

The last step, and the only one that is undone by doing it.

1. **Take JP1 off.** Both LEDs go dark and 0x603 stops being transmitted. That
   is the shipping configuration: nothing lights up in the car, and the bus
   carries one frame a second less than it did.
2. **Fit JP2**, if it is not already on. It puts the 100 nF capacitor back on
   MCLR, which is what DS39977C Figure 2-2 asks for in normal operation and
   what had to come off to programme the board.
3. **Check the display still reads.** Removing JP1 must change nothing except
   the LEDs — if the converter's channels go dead, the jumper was doing
   something it should not have been.
4. **Mount the board.** Four nylon M3 standoffs into H1–H4, feet on the floor
   of the vent with automotive-grade double-sided tape. **Not PVC or fabric
   tape wrapped round the board** — a dashboard reaches 50–60 °C and the
   adhesive creeps into the sockets. The reasoning is in `kicad`.
5. **Close the dashboard and drive.**

**What you give up by closing it**, and it is worth knowing before you do:
LED_CAN was the only live health indicator, and 0x603 the only numeric one.
Both are behind that jumper now. To read the counters again — after a fault, or
just out of curiosity — the dashboard comes apart, JP1 goes back on, and a
USBtin reads 0x603. That is deliberate: nothing in the car should light up or
add traffic for a device that is working.

The calibration below can be done later, on a working car, and does not need
any of this reopened.

---

## Then: calibration

Two things are known to be approximate and both need the car:

- **Drag torque on hot oil**, and it is the one worth the trip. The line in
  `config.h` is a least-squares fit through four free-revving holds at
  72–77 °C, stationary in neutral, where net torque is zero and the raw byte
  is the drag itself. **72–77 °C is warm, not the 95–110 °C of real driving**,
  so it probably still overstates drag slightly, which is the conservative
  direction. Repeat the same sweep on hotter oil, in neutral.
  `docs/can-decoding.md` question 7 has the reasoning and the procedure.

  ⚠ **The holds themselves will display zero**, because they are taken
  standing still and the driving gate returns zero for a standing car whatever
  the pedal is doing (`frames.md`). That is correct and not a fault to chase:
  the refit is done off the raw log and b7, not off the display.

  **Torque and power must read zero whenever the car is standing still, and
  whenever the pedal is released at any speed** — cold or warm. That is the
  driving gate (`frames.md`), a fixed requirement rather than a side effect of
  the drag fit, and it is worth checking on the first drive: if a stationary
  car shows a number, or a number survives lifting off, something is wrong with
  the speed or throttle decoding, not with the calibration.
- **The tank**, which needs a jerrycan: a known quantity put in, to check the
  level against. **One point exists: 6 L into a nearly empty tank settled at
  5 L on `FuelTank`** — measured. The converter applies no calibration to that
  number at all; `compute_tank_d()` is the damped 0x320 b2 and nothing else, so
  a discrepancy at the bottom of the tank is the sender's own nonlinearity
  rather than arithmetic here. Check `TankL` beside `FuelTank` on the display
  to confirm that: `TankL` is the raw byte, so if the two agree, nothing in
  this firmware is involved. Whether a correction is worth applying needs more
  than one point, and points near empty are the least useful ones to have.

**The torque scale, 0.74 Nm/bit, is deliberately not on that list.** It is a
decision inside the narrow bracket the factory ratings imply rather than a
measurement, and the VCDS session that was supposed to settle it found that
this ECU has no torque measuring block at all. It is parked under *Never
resolved but not required* in `docs/can-decoding.md` — **do not plan that
session again.**

`docs/can-decoding.md` now has exactly one open question, and it is the drag
line above.

---

## If something does not work

| Symptom | Look at |
|---|---|
| `ipecmd` says `Programmer not found` with the PICkit plugged in | in this order: **MPLAB X or IPE open** and holding the tool; the **firewall rule** on IPECMD's localhost socket; something else owning the HID handle; then the programmer itself. `flash-tool-notes.md` has the citation and the port for each |
| `ipecmd` says `Target device was not found (could not detect target voltage VDD)` | **the board is not powered.** `-W` is deliberately not used, so it needs its own 5 V. Nothing reached the part, so JP2 and the ICSP wiring are not the suspects. **This run still exits 0**, so it is the message that tells you, not the code |
| `ipecmd` says `Target Device ID (0x0) is an Invalid Device ID` | power is fine and ICSP is not: JP2 still fitted, MCLR/PGC/PGD wiring, or a dead part. Reproduced against a powered header with those three pins left unconnected — `flash-tool-notes.md` |
| A board misbehaves or dies the first time it is plugged onto the PICkit | **had `-W` been used on that PICkit beforehand?** It leaves ~4.6 V on header pin 2 after the command exits, which then fights the board's own supply. Measure pins 2 and 3 for zero before connecting a self-powered board — `flash-tool-notes.md` |
| Programming succeeds and nothing runs | `-OL` missing. The IPECMD default is *hold in reset*, so the part is programmed and then parked |
| The trip accumulators vanished after a reflash | expected: the erase is on by default. `flash.py --preserve-eeprom` passes `-Z0-3FF` and checks it took; `-E` would override it and is never passed |
| The board is silent right after a `--preserve-eeprom` run | that flow programs without `-OL` and releases in a separate step. If the release failed, the part is **held in reset** — run `python tools/flash.py --identify` |
| Both LEDs dark | JP1 not fitted — that is by design, nothing lights up in the car without it |
| No 0x603 on the bus, but 0x600 and 0x601 are there | JP1 not fitted. The diagnostic frame is only transmitted while the debug jumper is on — `docs/frames.md` |
| No 0x603 and a listen-only build | expected and unfixable: that mode transmits nothing at all. The LED is the only instrument in step 8 |
| `bench_test.py` reports adapter errors and nothing acknowledged | a `LISTEN_ONLY` hex on the bench, so nothing drives the ACK slot. Flash the normal build, or add a second adapter — step 7 |
| `bench_test.py` says the transmit FIFO filled | the host, not the converter. `--speed 0.5` |
| 0x603 says the reset cause was WATCHDOG | the firmware hung. A bug, and the uptime beside it says how often |
| 0x603 says BROWN-OUT | the supply sagged past `BORV` = 3.0 V. Suspect the feed, the fuse or the bench supply before the code |
| LED_CAN 5 Hz | `hal_can_init()` failed. Bit timing, `CANMX`, or a configuration bit |
| LED_CAN dark, car running | wiring: CANH/CANL swapped, or the stub not connected. Ring it out |
| Display channels stay at 0 | a silent build (LED_PWR blinking), or the frame layout drifted from `S-AQY.TRI` |
| Display shows plausible but wrong numbers | the frame layout **did** drift. `docs/frames.md` and `S-AQY.TRI` must agree; `test/test_txframes.c` pins every offset |
| The fuse blew | a short on the converter board. Fit one new fuse; if the second goes, stop and find the short |
| Nothing at all after wiring | ring circuit 1 of the Micro-Fit out to the board's +5 V pad. If CANH is in circuit 1, the transceiver has had 5 V on it |

`CLAUDE.md` in this repository is the long-form reasoning behind every decision
above, and `docs/refuted.md` is what was tried and did not work.
