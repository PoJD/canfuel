# IPECMD in detail, and notes for `tools/flash.py`

**`docs/install.md` is the procedure and needs none of this.** Steps 4 and 5
there are what somebody with a programmer in one hand actually follows. This
file is everything underneath: what each flag does, what the tool returns, how
it behaves on this machine, and what a `tools/flash.py` would have to know.

Two audiences, then — whoever debugs a programming session that went wrong, and
whoever writes the tool. **If the tool is ever written, the specification half
of this file goes with it; the observations do not.** They are the only record
of behaviour that no Microchip document states.

`tools/flash.py` is deliberately not written yet. The commands here have been
run only in the forms marked as observed; `-C`, `-M`, `-Y`, `-OL` and `-Z` have
never been run against a real target. Write the tool after a board has been
programmed by hand, not before.

---

## What the tool should do

- Wrap the four commands of `install.md` step 5 in one invocation.
- **Read `CONFIG3H` at byte address 300005h out of the hex and check `CANMX`
  before flashing anything.** Bit 0 set means CANTX/CANRX on RB2/RB3, which is
  what the board is wired to. This is the single most expensive bit in the
  project and it is checkable statically.
- **Tie the build mode and the flash into one step**, so a `LOOPBACK` hex
  cannot be flashed while the operator believes it is a normal one. The three
  modes differ only in a `#define`, and the resulting hex is otherwise
  indistinguishable.
- **Read the persist ring back off the part**, for bring-up in the vehicle.

---

## The utility is IPECMD

Three command-line programmers ship in the same MPLAB X install. Two are
disqualified by their own documentation:

- **`pk3cmd.exe`** — *Readme for PK3CMD.htm* §1: *"provided for legacy users
  (MPLAB IDE v8.xx) for backward script compatibility. It will not be enhanced
  with new features. Please use the IPECMD going forward."* It does have one
  thing IPECMD lacks: a documented exit-code table, §9 — 0 success, 7 operation
  failed, 36 bad argument.
- **`mdb.bat`** — *Readme for MDB.htm* §9, **MDB-44**: *"MDB holds device in
  reset after programming with PK3."* Wrong behaviour for a converter that has
  to start running.
- **`ipecmd.exe`** — the survivor, and the one Microchip point at.

`ipecmd.exe` and `pk3cmd.exe` are in `mplab_platform/mplab_ipe` under the
MPLAB X install directory, `mdb.bat` in `mplab_platform/bin`. **The tool should
invoke `ipecmd` by bare name and let `PATH` resolve it**, as `docs/install.md`
does, rather than hard-coding an install path with a version number in it.

---

## Flags, and why each one is what it is

- **`-OL` on every programming command.** *Readme for IPECMD.htm* §13 gives the
  default for *Release From Reset* as `Hold in reset`. Omitting it produces a
  correctly programmed board that does nothing, which reads as a firmware
  fault.
- **`-M` programmes and implicitly verifies.** §17.6: *"The Verify with (/M)
  operation implicitly performs a Verify when it completes the programming
  portion."* A separate `-Y` afterwards is free, not required.
- **`-W` never.** It powers the target from the programmer. The board has its
  own 5 V supply, so the flag buys nothing, and *Readme for PICkit 3.htm*
  §8.3.2 records a silicon issue on the PIC18F45K20/46K20 family that appears
  only with *"power from programmer"* — a different part, but a risk with no
  upside. See the hazard below.
- **The EEPROM is erased by default.** `-OH` (*Erase All Before Program*) is on
  unless disabled, so a plain `-M` discards the persist ring. That is the right
  default during bring-up: `persist_load()` returning false on a virgin EEPROM
  is a correct start, not an error. `-Z0-3FF` preserves it, and §17.8 warns
  that `-E` overrides `-Z`.
- **`mplab/canfuel.X` sets `programoptions.preserveeeprom = true`**, so the IDE
  and the command line deliberately differ on that point.

---

## Exit codes cannot carry the decision — parse the output

§10.2 promises only that an exit code is returned and never enumerates them.
The one table the readme carries, §15, is headed *MPLAB PM3 Specific* and does
not fit: it calls 9 `INVALID_PROGRAMMER` and 10 `NO_PROGRAMMER`.

Observed, with `-P18F25K80 -TPPK3`:

| Situation | Prints | Exit |
|---|---|---|
| no programmer | `Programmer not found` | 9 |
| programmer, target not powered | `Target device was not found (could not detect target voltage VDD)`, then `Operation Succeeded` | **0** |
| programmer, target powered, ICSP silent | `Target Device ID (0x0) is an Invalid Device ID`, `Operation Failed` | 1 |
| `-I -W` into an open header | `Connection Failed.`, then `Operation Succeeded` | 0 |
| `-T` (list tools) | the tool list | 50 |

**The one case the code gets wrong is the worst one:** a target nobody powered
returns 0 and prints `Operation Succeeded`. Bad ICSP wiring fails honestly with
1. Since `-W` is not used, an unpowered board is among the likeliest bench
mistakes there is.

**So the tool must decide on the printed output.** Never branch on the exit
code alone, and do not encode §15's table.

**Row three was produced deliberately, and it is the useful one.** A bench 5 V
supply across header pins 2 and 3, with MCLR, PGC and PGD left unconnected and
no `-W`, gives:

```
Target voltage detected
Target Device ID (0x0) is an Invalid Device ID. Please check your connections to the Target Device.
Operation Failed
```

`Target voltage detected` says VDD sensing works and sees an external supply.
`Device ID (0x0)` says the programmer ran the ICSP sequence and read back zeros
because nothing answered. **That is exactly what a dead ICSP link on a powered
board looks like**, which is the failure `install.md` step 5's first command
exists to catch — and it is now known rather than guessed at.

---

## Hazard: `-W` leaves the rail live after the command exits

Measured on the programmer's own header with a voltmeter: the ~4.6 V that `-W`
applies is **still present after the command has exited**. A plain run — the
same command without `-W` — clears it, established by alternating the two with
the meter watched throughout.

This matters because the board powers itself. A header left live by an earlier
`-W` puts two supplies onto one rail with no command running and nothing on
screen to suggest it. **If the tool ever offers `-W`, it must follow it with a
plain run**, and the operator must measure zero before connecting a
self-powered board.

---

## Environment facts that shape the implementation

- **The programmer is a USB HID device, not a virtual COM port**
  (*Readme for PICkit 3.htm* §8.2). There is no serial protocol to write
  against, the way `usbtin_capture.py` does for the CAN adapter. IPECMD is the
  only interface. There is no driver to install and no COM port to look for;
  the operating system's own view of it, under Microchip's vendor ID `04D8`, is

  ```
  Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match 'VID_04D8' }
  ```

- **Something else can hold the interface, and then IPECMD reports the
  programmer as absent.** §8.2 of the same readme: *"Some applications,
  plug-ins or widgets may take control of, or interfere with"* it, and
  *Readme for IPECMD.htm* §20.1 is explicit that a tool loaded in the MPLAB IPE
  will fail to communicate with anything else. **MPLAB X or IPE being open is
  the first thing to rule out** on a `Programmer not found` with the hardware
  visibly enumerated.
- **IPECMD talks to its own USB layer over a localhost TCP socket**, §14.5.1.
  `C:\Windows\System32\mchpdefport` holds the host and port, two lines — on
  this machine `localhost` and **30000**, read out of the file. Loopback only;
  nothing leaves the machine. A blocked port presents as a tool-communication
  failure with no mention of a firewall — §19.3 says so outright for the
  sibling IPECMDBoost utility and its ports 2012 and 2013. Worth detecting and
  reporting explicitly, and worth reading the file rather than assuming 30000:
  the readme describes it as configuration, not as a constant.
- **IPECMD appends an `MPLABXLog.xml` to whatever directory it runs from.**
  Run it from a scratch directory, or expect one in the working tree. The ones
  observed are empty.
- **The pack IPECMD uses is not the pack the compiler uses.** IPECMD resolves
  the pack bundled with MPLAB X; `mplab/Makefile` pins a different version
  because XC8 refuses the bundled one. Do not force them to agree — one
  describes the part to a compiler, the other to a programmer.
- **The first operation on a programmer flashes the programmer's own
  firmware**, §12: *"Upgrading the operating system of the programming tool
  happens automatically when the first operation using the tool is performed."*
  Unavoidable, and identical from the IDE. Expect the first run to be slow and
  chatty; a subsequent identical run should download nothing.
- **Read the tool's firmware version from the tool, not from the readme.** The
  two did not agree on the combination tested.

---

## If the programmer is replaced

IPECMD drives MPLAB Snap, PICkit 4 and ICD 4 as well; only the `-TP` short name
changes (§14.1). The tool packs bundled with MPLAB X v6.00 each list this part
in their `device_support.xml`:

| Tool | Pack | `PIC18F25K80` |
|---|---|---|
| MPLAB Snap | `Snap_TP 1.9.685` | listed |
| MPLAB PICkit 4 | `PICkit4_TP 1.10.1305` | listed |
| MPLAB ICD 4 | `ICD4_TP 1.9.1287` | listed |

⚠ **Being listed in a pack is not the same as fitting this board.** It says the
software knows the part; it says nothing about MCLR and VPP handling, target
power, or the 5-pin ICSP header on J3. Read the replacement's own user's guide
on those points, particularly how it drives MCLR, since `pic_config.h` sets
`MCLRE = ON` and JP2 exists precisely because that pin is fussy during
programming.

**An unknown header can be established by measurement**, with no document and
on any programmer:

- **Ground rings out at 0 Ω to the USB connector shell**, with nothing powered.
  Free, no risk, and it identifies that pin outright.
- **The supply pin carries the programmer's own voltage under `-W`** into an
  open header — mind the hazard above.
- **An external supply across those two produces `Target voltage detected`**,
  which is the tool confirming the pair.

The tool should therefore take the `-TP` name as a parameter rather than
hard-coding one.
