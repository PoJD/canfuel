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
consumption, range, torque and power, and sends them back on frames 0x600–0x602
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
| **A CAN interface the host can drive** | 8, and any recording | for watching the bus and recording logs. Any adapter that reaches 500 kbps will do; only the capture script is adapter-specific. *(Tested on a [USBtin](https://www.fischl.de/usbtin/); `tools/usbtin_capture.py` drives it over its serial protocol and needs `pyserial`. Every fixture in `test/fixtures/` was recorded with it.)* |
| **Multimeter** | 3, 5 | ringing out the loom, and confirming 5 V before the board is ever plugged in |
| **Crimping tools and loom parts** | 3 | listed in `kicad/canfuel/docs/harness.md`, which is where that list belongs |
| **A diagnostic tool for the vehicle** | calibration only | **optional.** Not needed to build or run anything. *(Tested with VCDS.)* |
| **The vehicle** | 6, 7, 8 | a VW PQ34 car with the AQY engine. Other PQ34 cars share much of the bus but nothing here is verified against them |

**A 120 Ω terminator** is worth knowing about: the board deliberately does not
fit R5, because the vehicle's bus is already terminated at both ends. Bench
testing off the vehicle needs an external one — but step 5, loopback, does not, which is
another reason to do it.

**Nothing above is needed for step 1.** The whole core builds and its tests run
on a PC with gcc, make and Python and no hardware whatsoever.

---

## Order of operations

The order is chosen so that each step can fail cheaply and be understood on its
own. **Do not skip step 5**: it costs ten minutes on a desk and it is the only
one that tests the CAN driver without a car attached.

| # | Step | Needs | Repository |
|---|---|---|---|
| 1 | Build and test on a PC | gcc, make, Python | `canfuel` |
| 2 | Upload the display configuration | the display and its configuration tool | `mfd15` |
| 3 | Make up the harness | crimping tools, the loom parts | `kicad` |
| 4 | Prove the programmer, with no board | a programmer, a USB port, MPLAB X | `canfuel` |
| 5 | Populate and programme a board, loopback on the desk | programmer, XC8 | `canfuel` |
| 6 | Listen only, in the vehicle | the vehicle | `canfuel` |
| 7 | Transmit, in the vehicle | the vehicle | `canfuel` |
| 8 | Check it against the raw counter | a drive | — |

Steps 1 to 4 are independent of each other and can be done in any order or in
parallel — **none of them needs a board**, which is why step 4 sits where it
does rather than inside step 5. From 5 on, the order is the point.

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
until step 7. The other nine read the car's bus directly and should be live as
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

**This is the only step in the second half that needs no board**, which is the
whole reason it is a step of its own. It retires the questions that would
otherwise all land at once the first time a populated board is plugged in:
whether the programmer is alive, whether the toolchain still recognises it,
whether the firmware update it forces goes through, and whether the command
line can drive it at all.

### The tool is IPECMD

Programming is driven from the command line, not from the IDE. **Every command
below calls `ipecmd` by bare name and expects it on `PATH`** — it is not put
there by the installer, and it lives in `mplab_platform/mplab_ipe` under the
MPLAB X install directory.

**MPLAB X has to be installed, but is never opened.** `make` builds the hex and
`ipecmd` writes it to the part. Two other command-line programmers ship in the
same MPLAB X install and both disqualify themselves; that reasoning, and the full
argument for every flag, is in [`flash-tool-notes.md`](flash-tool-notes.md).

### Run it with nothing attached first

```
ipecmd -P18F25K80 -TPPK3 -I
```

`-I` is *Display Device ID*. It reads and cannot write. Running it before the
programmer is plugged in establishes what failure looks like: it prints
`Programmer not found`. That already proves the device name is accepted, that a
Device Family Pack resolves without being told where one is, and that the tool
fails by returning rather than by opening a window.

Then plug the programmer in and run the identical command.

| What it prints | What it means |
|---|---|
| anything past `Programmer not found`, complaining about the target | **the pass.** The command line opened the tool and reached ICSP |
| `Programmer not found` again | not enumerating, or something else holds the interface — see below |
| a firmware download, then one of the above | expected, and expected **once** — see *Run it twice* |

`ipecmd -T` lists connected tools with their serial numbers and is the
shortest "is it alive" there is.

**Confirm the operating system sees it** before blaming the tool. The tested
programmer enumerates as a USB HID device under Microchip's vendor ID `04D8`:

```
Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match 'VID_04D8' }
```

**It is an HID device, not a virtual COM port** — *Readme for PICkit 3.htm*
§8.2 refers to *"the system provided HID USB driver"*. There is no serial port
to look for and no driver to install, and the same section carries the failure
mode: *"Some applications, plug-ins or widgets may take control of, or
interfere with"* it. **Check that MPLAB X or MPLAB IPE is not open**, since
*Readme for IPECMD.htm* §20.1 is explicit that a tool loaded in the IPE will
fail to communicate with anything else.

**IPECMD appends an `MPLABXLog.xml` to whatever directory it runs from.** Run
it from a scratch directory or expect one in the working tree.

### Expect a firewall prompt, and do not dismiss it

**IPECMD talks to its own USB layer over a TCP socket on localhost.**
*Readme for IPECMD.htm* §14.5.1 describes the `mchpdefport` file as carrying
*"the port or socket numbers through which the low-level library communicates
with the upper-level IPECMD"*; on Windows it is
`C:\Windows\System32\mchpdefport` and holds a host name and one port. Loopback
only — nothing leaves the machine.

**A blocked port shows up as a tool communication failure, not as a firewall
error.** Microchip say so for the sibling IPECMDBoost utility, §19.3: *"If there
are any connection issues with the tools, please ensure the firewall is not
blocking the port numbers 2012 and 2013."* Same failure mode, different ports.
If the programmer enumerates and IPECMD still insists `Programmer not found`,
check the firewall rule before suspecting the hardware.

### The firmware update happens whether you want it or not

*Readme for IPECMD.htm* §12: *"Upgrading the operating system of the
programming tool happens automatically when the first operation using the tool
is performed."* So the first command flashes the programmer itself. **This is
the one irreversible thing in the step**, and it is unavoidable — it would
happen identically from the IDE. Doing it deliberately, on a step whose only
job is to find out, is better than having it happen underneath the first real
programming attempt.

**Read the loaded version out of the tool, not out of the readme.** On the
tested combination the two did not agree.

### Run it twice, and the second run is the one that counts

**The first run measures two things at once and cannot separate them**: whether
the tool works, and whether it survives being reflashed. Its output is
confounded by the update. So run the identical command again: by then nothing
is downloaded, and what comes back is the steady state that every programming
run in steps 5 to 7 starts from.

| Run 1 | Run 2 | What it means |
|---|---|---|
| update, then past `Programmer not found` | same, no update, quick | **the pass.** The tool took the firmware and works with it |
| update, then past `Programmer not found` | `Programmer not found` | **the failure this step exists to catch.** It accepted the update and then stopped enumerating — a single run would have called this a success |
| `Programmer not found` | `Programmer not found` | never opened at all. Firewall, interface handle, or the tool is dead |
| update appears again | update appears again | the update is not sticking |

The last two rows look alike from across the room and mean opposite things.
**An update that repeats on every invocation is not a working programmer**,
even if the operations after it appear to succeed.

### ⚠ Exit codes cannot carry the decision, in either direction

*Readme for IPECMD.htm* §10.2 promises only that an exit code is returned and
never enumerates them. The one table it does carry, §15, is headed *MPLAB PM3
Specific* and does not fit what the tool actually does.

Observed with `-P18F25K80 -TPPK3`:

| Situation | Prints | Exit |
|---|---|---|
| no programmer | `Programmer not found` | 9 |
| **programmer, target not powered** | `Target device was not found (could not detect target voltage VDD)`, then `Operation Succeeded` | **0** |
| programmer, target powered, ICSP silent | `Target Device ID (0x0) is an Invalid Device ID`, `Operation Failed` | 1 |
| `-I -W` into an open header | `Connection Failed.`, then `Operation Succeeded` | 0 |
| `-T` | the tool list | 50 |

**The one case the code gets wrong is the worst one to get wrong: a target
nobody powered exits 0 and prints `Operation Succeeded`.** Bad ICSP wiring
fails honestly with 1. Since `-W` is deliberately not used here, an unpowered
board is among the likeliest bench mistakes there is, and it is exactly the one
a script checking the exit status would sail past.

**Parse the output. Never branch on the exit code alone.**

### ⚠ `-W` leaves the rail live after the command exits

`-W` powers the target from the programmer and **is not used** in this project:
the board has its own 5 V, so the flag buys nothing, and *Readme for PICkit 3.htm*
§8.3.2 records a silicon issue on the PIC18F45K20/46K20 family that appears only
with *"power from programmer"* — a different part, but a risk with no upside.

It matters anyway, because the hazard outlives the command. On the tested
programmer the ~4.6 V that `-W` applies **is still present after the command has
exited**. From step 5 on the board powers itself, so a header left live by an
earlier `-W` puts two supplies onto one rail with no command running and nothing
on screen to blame.

**If `-W` is ever used: run the plain command once afterwards — that is what
clears the rail — then measure zero across the supply pins before connecting a
self-powered board.** The meter is the gate; the next programmer need not behave
like this one.

### The header pinout, and how to confirm it without a document

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

**A different programmer needs its own pinout, and this procedure finds it
without one:**

- **Ground rings out at 0 Ω to the USB connector shell**, with nothing powered.
  Free, no risk, and it identifies that pin outright.
- **The supply pin carries the programmer's own voltage under `-W`** into an
  open header.
- **An external supply across the two produces `Target voltage detected`**,
  which is the tool confirming the pair.

### Powered header, nothing to talk to

The last thing this step can establish without a board: put a bench 5 V supply
across header pins 2 and 3, leave MCLR, PGC and PGD unconnected, and run the
ordinary command — **no `-W`**, because the supply is external.

```
Target voltage detected
Target Device ID (0x0) is an Invalid Device ID. Please check your connections to the Target Device.
Operation Failed
```

- **`Target voltage detected`** — VDD sensing works and an external supply is
  seen.
- **`Device ID (0x0)`** — the programmer ran the ICSP sequence on PGC/PGD and
  read back zeros, because nothing answered. **This is what a dead ICSP link
  looks like on a powered board**, and it is the failure step 5's command 1
  exists to catch.

### If the programmer has to be replaced

The tool packs bundled with MPLAB X v6.00 each list this part in their
`device_support.xml`:

| Tool | Pack | `PIC18F25K80` |
|---|---|---|
| MPLAB Snap | `Snap_TP 1.9.685` | listed |
| MPLAB PICkit 4 | `PICkit4_TP 1.10.1305` | listed |
| MPLAB ICD 4 | `ICD4_TP 1.9.1287` | listed |

IPECMD drives all of them — the tool short names are in *Readme for IPECMD.htm*
§14.1, so only `-TPPK3` changes.

⚠ **Being listed in a pack is not the same as fitting this board.** It says the
software knows the part; it says nothing about MCLR and VPP handling, target
power, or the 5-pin ICSP header on J3. **Read the replacement's own user's guide
on those points**, particularly how it drives MCLR, since `pic_config.h` sets
`MCLRE = ON` and JP2 exists precisely because that pin is fussy during
programming.

### What it does not prove

Nothing about the board, nothing about ICSP wiring, nothing about the hex. A
programmer that enumerates and updates its firmware can still fail to program a
target for a dozen reasons that only appear once there is a target. Step 5 is
where that gets tested.

---


## 5. Populate, programme, and loopback on the desk

This is the step that is easy to skip and should not be.

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

### The five that can go in backwards

Written out for somebody holding a soldering iron for the first time, because
"check the polarity" is not an instruction unless it says how.

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

### Programme

```
cd canfuel
make -C mplab CAN_MODE=LOOPBACK
```

That writes `mplab/build/canfuel.hex`. Building is documented in
`mplab/README.md`, including which XC8 and which Device Family Pack — the pack
is not optional and the version has to match.

⚠ **JP2 comes off before programming and goes back on afterwards.** It puts the
100 nF MCLR capacitor in circuit, which is what the datasheet asks for in
normal operation and what interferes with ICSP.

**Then flash it with the PICkit on J3**, from the repository root. The makefile
builds; it does not programme. Four commands, in this order, reading each one's
output before running the next:

```
ipecmd -P18F25K80 -TPPK3 -I                                  # 1. device ID
ipecmd -P18F25K80 -TPPK3 -C                                  # 2. blank check
ipecmd -P18F25K80 -TPPK3 -F"$PWD/mplab/build/canfuel.hex" -M -OL   # 3. program
ipecmd -P18F25K80 -TPPK3 -F"$PWD/mplab/build/canfuel.hex" -Y       # 4. verify
```

Command 1 is the one that matters most and it is read-only: **a device ID that
comes back correct means the ICSP wiring, the MCLR jumper and the part are all
good, before anything has been written.** If it fails, nothing after it can
succeed and there is no point trying. ⚠ **Read its output, not its exit code** —
step 4 provoked both failures without a board and its table says which is which.
The short version is that an unpowered board still exits 0, so a script checking
`$?` sails straight past the likeliest bench mistake there is.

Command 4 is free rather than required: `-M` verifies implicitly when it
finishes programming.

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
  there is a real trip in it. **`mplab/canfuel.X` deliberately does the
  opposite** — know which tool you are holding.

⚠ **Only the `-I` form has been run against real hardware**, and only as step 4,
with no target attached. `-C`, `-M`, `-Y`, `-OL` and `-Z` are assembled from
*Readme for IPECMD.htm* and are unproven, as is anything downstream of the ICSP
header. **Correct this block the first time it runs against a part.**

**Fit JP1** — without it both LEDs stay dark by design, and you are about to
need them.

### What loopback proves

DS39977C §27.3.5 hands the transmit buffers straight to the receive buffers, so
the module talks to itself. **No bus, no USBtin, no transceiver needed.** It
exercises the bit timing, all six acceptance filters, the eight-deep FIFO,
the access-bank window, `txframes` and `decode` — everything except the wire
itself.

Watch the LEDs:

| LED_PWR | LED_CAN | Means |
|---|---|---|
| slow blink | steady | **working** — loopback is a silent mode, so the slow blink is correct here |
| slow blink | 5 Hz blink | `hal_can_init()` never got the module into the mode it asked for. The bit timing or a configuration register is wrong. Stop here. |
| slow blink | dark | nothing is arriving — the transmit path or the FIFO is not working |
| steady | any | **wrong hex.** A steady LED_PWR means a normal build; you flashed the wrong one |

A fault caught here costs a reflash. The same fault caught in step 6 costs a
trip to the car, and in step 7 it puts error frames on the car's bus.

---

## 6. Listen only, in the car

```
make -C mplab CAN_MODE=LISTEN_ONLY
```

Flash it with the same four commands as step 5, fit JP1, wire the board in
through the Y-splitter, and switch on. **This is the first reflash where
`-Z0-3FF` is worth thinking about** — see step 5; there is nothing in the
EEPROM yet worth keeping, but from here on there will be.

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

## 7. Transmit

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

## 8. Check it against the raw counter

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
- **Refuel and watch the trip average clear.** The reset fires on five
  consecutive at-rest samples more than 3 L above the settled tank level, so
  about five seconds of standing still after the fill. `docs/refuel-reset.md`
  has the rules and the corner cases.

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

  **At a standstill with the throttle shut the display must read zero torque
  and zero power** — cold or warm. That is the idle gate (`frames.md`), a fixed
  requirement rather than a side effect of the drag fit, and it is worth
  checking on the first drive: if a stationary car shows a number, something is
  wrong with the speed or throttle decoding, not with the calibration.
- **The tank**, which needs a jerrycan: a known quantity put in, to check the
  level against.

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
| `ipecmd` says `Programmer not found` with the PICkit plugged in | in this order: **MPLAB X or IPE open** and holding the tool (*Readme for IPECMD.htm* §20.1); the **firewall rule** on localhost port 30000 (step 4); something else owning the HID handle (*Readme for PICkit 3.htm* §8.2); then the programmer itself |
| `ipecmd` says `Target device was not found (could not detect target voltage VDD)` | **the board is not powered.** `-W` is deliberately not used, so it needs its own 5 V. Nothing reached the part, so JP2 and the ICSP wiring are not the suspects. **This run still exits 0**, so it is the message that tells you, not the code |
| `ipecmd` says `Target Device ID (0x0) is an Invalid Device ID` | power is fine and ICSP is not: JP2 still fitted, MCLR/PGC/PGD wiring, or a dead part. Verified in step 4 against a powered header with those three pins left unconnected. This one does exit 1 |
| A board misbehaves or dies the first time it is plugged onto the PICkit | **had `-W` been used on that PICkit beforehand?** It leaves ~4.6 V on header pin 2 after the command exits, which then fights the board's own supply. Measure pins 2 and 3 for zero before connecting a self-powered board — step 4 |
| Programming succeeds and nothing runs | `-OL` missing. The IPECMD default is *hold in reset*, so the part is programmed and then parked |
| The trip accumulators vanished after a reflash | expected: `-OH` erases everything by default. `-Z0-3FF` is what preserves them, and `-E` overrides it |
| Both LEDs dark | JP1 not fitted — that is by design, nothing lights up in the car without it |
| LED_CAN 5 Hz | `hal_can_init()` failed. Bit timing, `CANMX`, or a configuration bit |
| LED_CAN dark, car running | wiring: CANH/CANL swapped, or the stub not connected. Ring it out |
| Display channels stay at 0 | a silent build (LED_PWR blinking), or the frame layout drifted from `S-AQY.TRI` |
| Display shows plausible but wrong numbers | the frame layout **did** drift. `docs/frames.md` and `S-AQY.TRI` must agree; `test/test_txframes.c` pins every offset |
| The fuse blew | a short on the converter board. Fit one new fuse; if the second goes, stop and find the short |
| Nothing at all after wiring | ring circuit 1 of the Micro-Fit out to the board's +5 V pad. If CANH is in circuit 1, the transceiver has had 5 V on it |

`CLAUDE.md` in this repository is the long-form reasoning behind every decision
above, and `docs/refuted.md` is what was tried and did not work.
