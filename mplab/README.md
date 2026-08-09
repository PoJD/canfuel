# Building the firmware

Two ways in, and they compile the same seven files.

## Without the IDE — `make`

```
make -C mplab                    # -> mplab/build/canfuel.hex
make -C mplab XC8=/path/to/xc8-cc
```

This is the authoritative recipe and it is what CI runs. It needs nothing but
`xc8-cc` on the path. Everything the compiler has to know about the part is in
`src/pic_config.h`, so the makefile only carries the device name, the standard
and the optimisation level.

**XC8 is not installed on the machine this was written on.** The flags are the
documented ones, but the first person to run it should expect to fix
something, and should say what in a commit message.

### Which XC8

**MPLAB X IDE and XC8 are two separate downloads.** Installing the IDE does not
install a compiler; it offers the links at the end and that is all.

- **MPLAB X IDE — take the newest.** It is an editor and a PICkit front end,
  it has no opinion about this code, and it will drive any XC8.
- **XC8 — v2.50**, which is the last of the v2 line. `.github/workflows/ci.yml`
  is pinned to the same version, so a build that works on the desk is a build
  that works in CI.

XC8 v3.00 and v3.10 exist and may be perfectly fine. They are a major version
bump, and the first XC8 build this firmware has ever had should not also be the
first test of a new major version — when something breaks there would be two
candidates instead of one. Once v2.50 produces a clean hex, trying v3 is a
five-minute experiment with a known-good baseline to diff against, and moving
the pin is one line.

A licence is not needed. Unlicensed, XC8 runs in Free mode, which compiles
everything and only restricts the optimiser — hence the `OPT` variable above,
and `make OPT=-O0` in CI.

## With MPLAB X — `mplab/canfuel.X`

Open the project. It targets the PIC18F25K80 with XC8 and a PICkit 3, and
pulls all seven sources out of `../../src`.

`nbproject/Makefile-*.mk` are **not committed**. MPLAB X generates them from
`configurations.xml` on the first build; they carry absolute paths to whichever
XC8 is installed, so committing them would mean a diff per machine. If the IDE
complains that the project must be updated, let it — that is what it is doing.

One setting is deliberate rather than default:
`programoptions.preserveeeprom = true`. The trip accumulators live in the data
EEPROM, and reprogramming the device should not throw away the tank level and
the litres since the last refuelling.

## Programming the board

Two things from the board's own list of obligations, both easy to forget:

- **JP2 comes off before programming and goes back afterwards.** It puts the
  100 nF capacitor on MCLR, which is what DS39977C Figure 2-2 asks for in
  normal operation and what interferes with ICSP.
- **The 120 Ω termination is not fitted** (R5, silkscreened `120R DNF`). The
  car's bus is terminated at both ends already. Bench testing off the car needs
  an external terminator, or the transceiver has nothing to drive against.
