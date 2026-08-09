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
install a compiler; it offers the links at the end and that is all. Take the
newest IDE — it is an editor and a PICkit front end, it has no opinion about
this code, and it will drive any XC8.

**XC8 v4.00.** It is the current release and the only one Microchip's download
page still offers, and `.github/workflows/ci.yml` is pinned to the same
version, so a build that works on the desk is a build that works in CI.

**No licence is needed and none should be installed.** v4 dropped the Free
mode restriction on the optimiser, which is why both the desk build and CI use
the real `-O2` rather than working around a crippled compiler. If that ever
turns out to be wrong on some machine, `make OPT=-O0` is the fallback and the
hex it produces is still perfectly good to flash.

Older versions are still reachable by direct URL even though the page no
longer lists them — 2.36 through 2.50, 3.00 and 3.10 all resolve under
`https://ww1.microchip.com/downloads/aemDocuments/documents/DEV/ProductDocuments/SoftwareTools/xc8-vX.YY-full-install-linux-x64-installer.run`.
Worth knowing if v4 ever has to be bisected against, and not worth using
otherwise: pinning to a compiler nobody has installed only tests a compiler
nobody uses.

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
