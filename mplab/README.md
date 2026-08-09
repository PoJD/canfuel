# Building the firmware

Two ways in, and they compile the same seven files.

## Without the IDE — `make`

```
make -C mplab                    # -> mplab/build/canfuel.hex
make -C mplab XC8="/c/Program Files/Microchip/xc8/v4.00/bin/xc8-cc"
make -C mplab DFP=/somewhere/PIC18F-K_DFP/1.13.292/xc8
```

This is the authoritative recipe and it is what CI runs. Everything the
compiler has to know about the part is in `src/pic_config.h` and in the Device
Family Pack, so the makefile only carries the device name, the pack, the
standard and the optimisation level.

**The plain form works on this desk with no arguments.** If `xc8-cc` is not on
the PATH the makefile falls back to the Windows default install path, and the
pack defaults to `C:\mchp_packs`. Both are overridable as above; the `XC8=`
form is quoted for a reason, since the default Windows path has a space in it.

**PATH is only this makefile's problem.** MPLAB X finds its own toolchains by
scanning the standard install locations — it does not care about PATH, and a
project that builds in the IDE says nothing about whether `make` will find the
compiler.

### The Device Family Pack, which is where the first build went wrong

**XC8 v4.00 ships no device data of its own.** There is no `pic/dat`, no
`pic/include/proc` and no `docs/chips` under the compiler install: the register
headers, the `#pragma config` keywords and the linker script for the
PIC18F25K80 all live in a Device Family Pack, passed with `-mdfp`. Without one
the build stops immediately:

```
::: error: (2103) no device-support files specified; use the -mdfp option
```

Three things about that, each of which cost a round on 2026-08-09, and each of
which reports as the same unhelpful `error: (2104) no device-support files
found`:

1. **`-mdfp` points at the `xc8` subdirectory inside the pack, not at the pack
   root.** The user's guide is explicit — "path is the relevant path to the
   xc8 directory within the DFP" — and pointing at the root fails in a way
   that reads like the pack is missing rather than misaddressed.
2. **The pack version has to match the compiler.** MPLAB X v6.00 bundles
   `PIC18F-K_DFP 1.5.114` and XC8 v4.00 refuses it. v4.00's readme names
   **1.13.292** as the version it ships with, and that is what both this desk
   and CI use. Download it from
   `https://packs.download.microchip.com/Microchip.PIC18F-K_DFP.1.13.292.atpack`
   — it is a zip whatever the extension says.
3. **The path to it must be pure ASCII.** Unpacked under a home directory
   whose name carries a caron, device support resolves but the pack's include
   directories are silently left off the search path, and the build dies much
   later on `xc.h:33: 'pic18.h' file not found`. That is why the pack lives in
   `C:\mchp_packs` here rather than in the conventional
   `%USERPROFILE%\.mchp_packs`.

CI downloads and unpacks the same version itself rather than trusting the
compiler installer to have placed it, because on this desk the installer did
not place it.

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

**The project already exists. Do not create a new one** — File → Open Project
→ `mplab/canfuel.X`. Creating one from the wizard would put a fresh `.X`
somewhere else, with its own copy of the source list, and there would then be
two answers to the question of what gets compiled.

It targets the PIC18F25K80 with XC8 and a PICkit 3, and pulls all seven sources
out of `../../src`.

**The IDE build has not been made to work on this desk, and is not the
priority.** MPLAB X v6.00 manages packs itself: it bundles `PIC18F-K_DFP
1.5.114`, which XC8 v4.00 rejects, and the Pack manager unpacks anything newer
into `%USERPROFILE%\.mchp_packs`, which is the accented path XC8 v4.00 cannot
read. Either of those can presumably be pointed elsewhere, but neither is worth
solving to build something `make -C mplab` already builds. Use the IDE as an
editor and as the PICkit front end; take the hex from `mplab/build`.

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
