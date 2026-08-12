# From three clones to a working device

The whole path, in the order it has to happen, across all three repositories.
Every step says what it needs, what it proves, and how you know it worked.

**Steps 1 to 3 are written from experience. Steps 4 onwards are not** — they
come from the datasheets and the design, and they say so where it matters.
Correct this document as you go; that is what it is for, and it is the one
document that is meant to outlive the project's own notes.

> **Where this car is, 2026-08-12.** Steps 1, 2 and 3 are done: the firmware
> builds and its tests pass, `S-AQY.TRI` is uploaded and verified on the
> display, and the harness is built, fitted and measured — **5.01 V at the
> 4-pin the board will plug into**, with the display since run on that loom
> using DuPont jumpers in place of the board.
>
> **The next action is step 4, and it needs no board.** It proves the
> programmer end of the toolchain with nothing but a PICkit 3 and a USB port,
> which is the one piece of ground that can be taken while the boards are in
> the post. **Step 5 onwards is what waits on them**; they were ordered on
> 2026-08-09 and are expected in the week of 2026-08-17. Nothing else is
> outstanding: one calibration question remains open and it is a refinement,
> not a blocker — see *Then: calibration*.

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
powertrain CAN at 500 kbps. It reads six frames from the ECU, computes
consumption, range, torque and power, and sends them back on frames 0x600–0x602
for the display to render.

The car does not know it is there. Nothing lights up unless a jumper is fitted.

---

## What you need

**Software is listed in each repository's own README** — `canfuel` for the
toolchain, `kicad` for KiCad, `mfd15` for oDSS — because what you need depends
on which half you are working on, and the versions belong next to the thing
they build. This section is the **physical** side, which no single repository
owns.

| Thing | For step | Notes |
|---|---|---|
| **CANchecked MFD15 Gen2** display | 2, and everything after | the whole point of the device; it also supplies the converter's 5 V |
| **A phone or laptop with Wi-Fi** | 2 | to reach oDSS, which the display serves itself — nothing is installed for this |
| **The converter board** | 5 onwards | `kicad/canfuel/fab/` are the files a fab house needs; ours came from Gatema, 3 pieces |
| **The parts to populate it** | 5 | 24 of them, mostly through-hole — `kicad/canfuel/fab/canfuel-bom.csv` |
| **Soldering iron** | 5 | through-hole, nothing fine-pitch |
| **PICkit 3** | 4, 5 | through the 5-pin ICSP header J3, driven from the command line with **IPECMD** — see step 4. MPLAB X has to be installed for that, because IPECMD is part of it, but the IDE is never opened. Other programmers supporting the PIC18F25K80 should work; none has been tried |
| **USBtin** ([fischl.de](https://www.fischl.de/usbtin/)) | 8, and any recording | the CAN adapter every fixture in `test/fixtures/` was recorded with. `tools/usbtin_capture.py` drives it and needs `pyserial` |
| **Multimeter** | 3, 5 | ringing out the loom, and confirming 5 V before the board is ever plugged in |
| **Crimping tools and loom parts** | 3 | listed in `kicad/canfuel/docs/harness.md`, which is where that list belongs |
| **VCDS** | calibration only | **optional.** Not needed to build or run anything; it is diagnostics for the calibration work at the end |
| **The car** | 6, 7, 8 | a VW New Beetle with the AQY engine. Other PQ34 cars share much of the bus but nothing here is verified against them |

**A 120 Ω terminator** is worth knowing about: the board deliberately does not
fit R5, because the car's bus is already terminated at both ends. Bench testing
off the car needs an external one — but step 5, loopback, does not, which is
another reason to do it.

**Nothing above is needed for step 1.** The whole core builds and its tests run
on a PC with gcc, make and Python and no hardware whatsoever.

---

## Order of operations

The order is chosen so that each step can fail cheaply and be understood on its
own. **Do not skip step 5**: it costs ten minutes on a desk and it is the only
one that tests the CAN driver without a car attached.

| # | Step | Needs | Repository | This car |
|---|---|---|---|---|
| 1 | Build and test on a PC | gcc, make, Python | `canfuel` | done |
| 2 | Upload the display configuration | the display and any Wi-Fi device with a browser | `mfd15` | done |
| 3 | Make up the harness | crimping tools, the loom parts | `kicad` | done |
| 4 | Prove the programmer, with no board | a PICkit 3, a USB port, MPLAB X | `canfuel` | **next** |
| 5 | Populate and programme a board, loopback on the desk | PICkit, XC8 | `canfuel` | |
| 6 | Listen only, in the car | the car | `canfuel` | |
| 7 | Transmit, in the car | the car | `canfuel` | |
| 8 | Check it against the raw counter | a drive | — | |

Steps 1 to 4 are independent of each other and can be done in any order or in
parallel — **none of them needs a board**, which is why step 4 sits where it
does rather than inside step 5. From 5 on, the order is the point.

The last column is where this particular car has got to; it is the only
progress tracker the project keeps, and every other document that wants to say
"what next" points here instead of answering it.

---

## 1. Build and test on a PC

No hardware at all. This proves the arithmetic against real recordings from the
car before anything is soldered.

```
cd canfuel
make -C test test            # 250+ checks
make -C test check-pure      # no <xc.h> anywhere in the core
make -C test check-hal       # the HAL still compiles
python -m unittest discover -s tools -p "test_*.py"        # 80+ tests
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
whole reason it is a step of its own. It costs five minutes and it retires the
questions that would otherwise all land at once the first time a populated
board is plugged in: whether the PICkit is alive, whether it is a PICkit MPLAB
X still recognises, whether the firmware update it forces goes through, and
whether the command line can drive it at all.

### The tool is IPECMD, and it is already installed

Programming is driven from the command line, not from the IDE. The utility is
`ipecmd.exe`, part of MPLAB X:

```
C:\Program Files\Microchip\MPLABX\v6.00\mplab_platform\mplab_ipe\ipecmd.exe
```

so **MPLAB X has to be installed, but is never opened.** `make` builds the hex
and `ipecmd` writes it to the part; neither needs the IDE running, and both are
repeatable and diffable in a way that clicking is not.

Two other command-line programmers ship in the same directory and neither is
the right one. `pk3cmd.exe` describes itself as legacy — *"provided for legacy
users (MPLAB IDE v8.xx) for backward script compatibility. It will not be
enhanced with new features. Please use the IPECMD going forward"*
(*Readme for PK3CMD.htm* §1). `mdb.bat` has a documented defect that is exactly
wrong for us — *Readme for MDB.htm* §9, **MDB-44**: *"MDB holds device in reset
after programming with PK3."* The reasoning is in `CLAUDE.md`.

### With nothing plugged in

Run this first, before the PICkit is anywhere near the USB port, so that you
know what failure looks like:

```
"/c/Program Files/Microchip/MPLABX/v6.00/mplab_platform/mplab_ipe/ipecmd.exe" \
    -P18F25K80 -TPPK3 -I
```

Recorded on this desk on 2026-08-12:

```
DFP Version Used : PIC18F-K_DFP,1.5.114,Microchip
Programmer not found.
```

exit code **9**. That already proves three things worth having: `18F25K80` is a
device name IPECMD accepts, it resolves a Device Family Pack for it without
being told where one is, and it fails by returning rather than by opening a
window or hanging. `-I` is *Display Device ID* and reads nothing else — there
is no way for it to write to anything.

⚠ **Read the exit code, but do not look it up.** *Readme for IPECMD.htm* §10.2
promises only that *"the program will return an exit code upon completion which
will indicate either successful completion or describe the reason for
failure"*, and never enumerates them. The one table it does carry, §15, is
headed *List of MPLAB PM3 Specific Error Codes* — and it does not fit what we
observed: it calls 9 `INVALID_PROGRAMMER` and reserves 10 for `NO_PROGRAMMER`,
while the run above printed `Programmer not found` and returned 9. So treat
non-zero as failure, quote the message rather than the number, and build up a
mapping from runs rather than from that table.

⚠ **The pack IPECMD uses is not the pack the compiler uses.** It picks
`PIC18F-K_DFP 1.5.114`, the one MPLAB X v6.00 bundles, while `mplab/Makefile`
pins **1.13.292** because XC8 v4.00 refuses 1.5.114. That is not a conflict:
one pack describes the part to a compiler and the other describes it to a
programmer. Do not "fix" it by forcing them to match.

### With the PICkit plugged in

Same command. **What is being looked for is a different error, not a success**
— there is no target attached, so it cannot read a device ID and it must not
claim to. What it must no longer say is `Programmer not found`: anything past
that point means the CLI opened the tool.

| What it says | What it means |
|---|---|
| something other than `Programmer not found`, complaining about the target or the device ID | **this is the pass.** The CLI found the PICkit and got as far as ICSP |
| `Programmer not found` again | the PICkit is not enumerating, or something else has the HID handle — see below |
| a firmware download, then one of the above | also a pass, and expected once. See the note on firmware below |

`ipecmd.exe -T` lists connected tools with their serial numbers and is the
shortest "is it alive" there is.

**The PICkit 3 is a USB HID device, not a virtual COM port.** There is no
serial port to look for and no driver to install — *Readme for PICkit 3.htm*
§8.2 refers to *"the system provided HID USB driver"*, and the same section is
where the failure mode lives: *"Some applications, plug-ins or widgets may take
control of, or interfere with"* it. If the tool is not found, the first thing
to check is that nothing else has it — in particular **that MPLAB X or MPLAB
IPE is not open**, since *Readme for IPECMD.htm* §20.1 is explicit that a tool
already loaded in the IPE will fail to communicate with anything else.

### Windows Defender will ask, on the first run, and it is not spurious

**Expect a Windows Defender Firewall prompt the first time `ipecmd` is run**,
and do not dismiss it. It was allowed for **private networks** on this desk on
2026-08-12, which is enough.

It looks alarming for a program that only talks to a USB device, and there is a
documented reason for it: **IPECMD talks to its own USB layer over a TCP socket
on localhost.** *Readme for IPECMD.htm* §14.5.1 describes the `mchpdefport`
file as providing *"the information necessary for tool hot-plug use to both the
IPECMD and to the low-level USB library"*, and its contents are a host name and
a list of port numbers — *"the port or socket numbers through which the
low-level library communicates with the upper-level IPECMD"*. On this machine
the file is `C:\Windows\System32\mchpdefport` and it holds exactly two lines:

```
localhost
30000
```

So one instance, one port, loopback only. Nothing leaves the machine, and the
prompt is Windows noticing a listening socket rather than anything reaching out.

**A blocked port shows up as a tool communication failure, not as a firewall
error**, which is why this is written down here rather than left to be
rediscovered. Microchip say so themselves for the sibling utility — §19.3, on
IPECMDBoost: *"If there are any connection issues with the tools, please ensure
the firewall is not blocking the port numbers 2012 and 2013."* Same failure
mode, different ports. If the PICkit is plugged in, enumerates in Device
Manager, and IPECMD still insists `Programmer not found`, check the firewall
rule before suspecting the clone.

### The firmware update, which happens whether you want it or not

*Readme for IPECMD.htm* §12: *"Upgrading the operating system of the
programming tool happens automatically when the first operation using the tool
is performed."* MPLAB X v6.00 carries PICkit 3 suite **v01.56.07**
(*Readme for PICkit 3.htm*), and the images are in
`mplab_platform\mplablibs\modules\ext\PICKIT3.jar` — which is also the evidence
that v6.00 still supports the PICkit 3 at all, rather than having dropped it
the way the tool-pack directory's missing `PK3_TP` might suggest.

So the first command flashes the PICkit itself. **This is the one irreversible
thing in the step**, and it is unavoidable: it would happen identically from
the IDE. Doing it here, deliberately, on a step whose only job is to find out,
is better than having it happen underneath the first real programming attempt.

⚠ **The PICkit here is an unknown cheaper clone**, not a Microchip unit. It
worked under MPLAB X about ten years ago, which says nothing about v6.00 and is
not evidence of anything — no Microchip document covers clones and none ever
will. **That is
precisely why this step exists and why it comes before the boards arrive.** If
the clone turns out not to survive the firmware update, the answer is to buy a
programmer, and it is very much better to learn that in the week the boards are
still in the post than on the evening they arrive.

### What it does not prove

Nothing about the board, nothing about ICSP wiring, nothing about the hex. A
PICkit that enumerates and updates its firmware can still fail to program a
target for a dozen reasons that only appear once there is a target. Step 5 is
where that gets tested.

---

## 5. Populate, programme, and loopback on the desk

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

That writes `mplab/build/canfuel.hex`. Building is documented in
`mplab/README.md`, including which XC8 and which Device Family Pack — the pack
is not optional and the version has to match.

**Then flash it with the PICkit on J3, from the command line.** The makefile
builds; it does not programme. Do the whole thing in four commands, in this
order, and read each one's output before running the next:

```
IPE="/c/Program Files/Microchip/MPLABX/v6.00/mplab_platform/mplab_ipe/ipecmd.exe"

"$IPE" -P18F25K80 -TPPK3 -I                                  # 1. device ID
"$IPE" -P18F25K80 -TPPK3 -C                                  # 2. blank check
"$IPE" -P18F25K80 -TPPK3 -F"$PWD/mplab/build/canfuel.hex" -M -OL   # 3. program
"$IPE" -P18F25K80 -TPPK3 -F"$PWD/mplab/build/canfuel.hex" -Y       # 4. verify
```

Command 1 is the one that matters most and it is read-only: **a device ID that
comes back correct means the ICSP wiring, the MCLR jumper and the part are all
good, before anything has been written.** If it fails, nothing after it can
succeed and there is no point trying.

Four details in that command line, each of which is a way to get it wrong:

- **`-OL` is not optional.** It is *Release From Reset*, and the default in
  *Readme for IPECMD.htm* §13 is the opposite — `Hold in reset`. Leave it off
  and the board is programmed correctly and then simply sits there, which looks
  exactly like a firmware that does not run.
- **`-M` programmes and implicitly verifies.** §17.6: *"The Verify with (/M)
  operation implicitly performs a Verify when it completes the programming
  portion."* Command 4 is therefore a second verify and is there because it is
  free, not because it is required.
- **`-W` is deliberately not used.** It powers the target from the PICkit. The
  board takes its 5 V from the display or a bench supply, and *Readme for
  PICkit 3.htm* §8.3.2 records a silicon issue on another family that only
  appears with *"power from programmer"*. Power the board, then attach ICSP.
- **The EEPROM is erased, on purpose.** `-OH` (*Erase All Before Program*) is
  on by default, so a plain `-M` takes the trip accumulators with it. That is
  the right default here: `persist_load()` returns false on a virgin EEPROM and
  the core starts from zero, which is correct rather than an error, and during
  bring-up a known-empty ring is worth more than a preserved one. When that
  stops being true — reflashing in the car with a real trip stored —
  **`-Z0-3FF` preserves it**, and mind §17.8: `-E` overrides `-Z`.

⚠ **The `.X` project disagrees with that last one, and the disagreement is
deliberate.** `mplab/canfuel.X` sets `programoptions.preserveeeprom = true`, so
if the IDE is ever used as the programmer it will keep the EEPROM where the
command line above discards it. Neither is wrong; know which one you are
holding.

⚠ **This has not been done on this project yet, and the commands above have
never been run against a target.** They are assembled from *Readme for
IPECMD.htm* §13, §17 and §18, and only the `-I` form has actually been executed
here — against no programmer, where it printed `Programmer not found` and
returned 9. The same MCU was flashed from the IDE on an earlier project, which
is where the confidence comes from and is not the same as having done it here.
**Correct this block the first time it runs.**

⚠ **JP2 comes off before programming and goes back on afterwards.** It puts the
100 nF MCLR capacitor in circuit, which is what the datasheet asks for in
normal operation and what interferes with ICSP.

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
- **Refuel and watch the trip average clear.** The reset fires on a rise of more
  than 3 L in the at-rest median, which takes about five seconds of standing
  still after the fill. `docs/refuel-reset.md` has the rules and the corner
  cases.

---

## Then: calibration

Two things are known to be approximate and both need the car:

- **Drag torque on hot oil**, and it is the one worth the trip. The line was
  refitted on 2026-08-11 on four free-revving holds at 72–77 °C, replacing one
  fitted on cold oil, and the torque scale moved 0.75 → 0.74 Nm/bit with it.
  But 72–77 °C is warm, not the 95–110 °C of real driving, so it probably still
  overstates drag a little. Same sweep, hotter oil, in neutral.
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
| `ipecmd` says `Programmer not found` with the PICkit plugged in | in this order: **MPLAB X or IPE open** and holding the tool (*Readme for IPECMD.htm* §20.1); the **firewall rule** on localhost port 30000 (step 4); something else owning the HID handle (*Readme for PICkit 3.htm* §8.2); then the clone |
| `ipecmd` finds the tool but cannot read a device ID | JP2 still fitted, ICSP wiring, or the board is not powered — `-W` is deliberately not used, so the board needs its own 5 V |
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
