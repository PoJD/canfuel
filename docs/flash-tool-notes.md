# IPECMD in detail, and notes for `tools/flash.py`

**`docs/install.md` is the procedure and needs none of this.** Steps 4 and 5
there are what somebody with a programmer in one hand actually follows. This
file is everything underneath: what each flag does, what the tool returns, how
it behaves on this machine, and what `tools/flash.py` had to know.

Two audiences, then — whoever debugs a programming session that went wrong, and
whoever writes the tool. **If the tool is ever written, the specification half
of this file goes with it; the observations do not.** They are the only record
of behaviour that no Microchip document states.

`tools/flash.py` covers `-I`, `-C`, `-M -OL`, `-M -Z0-3FF` and `-GE0-3FF`. The
output of the first three is recorded below and is what `tools/test_flash.py`
parses. **`-Z` and `-GE` are the two that used to be missing, and what closed
them is not a decision to trust the readme: `--preserve-eeprom` reads EEData
before and after and compares the two byte for byte, so the switch proves
itself on every run rather than once.** Until a real dump has been pasted into
`test_flash.py`, the dump parser is tested only against synthetic text and says
so in both files.

---

## What the tool does, and what it still does not

Done, and each one is a fault it exists to make impossible:

- **Wraps step 5 in one invocation**, and decides every step on the printed
  output rather than the exit code.
- **Reads `CONFIG3H` at byte address 300005h out of the hex and checks
  `CANMX` before flashing anything.** Bit 0 set means CANTX/CANRX on RB2/RB3,
  which is what the board is wired to. The single most expensive bit in the
  project, and checkable statically.
- **Ties the build mode and the flash into one step**, so a `LOOPBACK` hex
  cannot be flashed while the operator believes it is a normal one. The three
  modes differ only by one `-D` and the hexes are otherwise
  indistinguishable. `mplab/Makefile` writes the mode to `build/can_mode` and
  the tool reads it back, so the belief is checked rather than trusted.
- **Skips `-Y`**, for the reason below: it fails on a perfectly programmed
  board.

- **Preserves the persist ring on request, and checks that it did.**
  `--preserve-eeprom` passes `-Z0-3FF`, and because that switch had never been
  run against a part when it was added, the run does not take its word for it:
  `-GE0-3FF` before, `-GE0-3FF` after, compared byte for byte. See the section
  below for why that costs an extra command.
- **Reads EEData off the part.** `--read-eeprom FILE` writes the 1,024 bytes
  out and changes nothing, which is what looking at a persist ring during
  bring-up wants.

Not done: nothing, of the two gaps this file used to list.

Both have since run against a real part holding a real trip, and the format is
recorded below. `tools/testdata/ipecmd-ge0-400.txt` is the whole capture,
verbatim — 1,024 bytes of EEData off a converter that had been driven, with 38
persist records in it — and `tools/test_flash.py` parses that file rather than a
string somebody typed.

`tools/test_flash.py` holds IPECMD's real output for every case the tool
parses, including the three failures, and needs no programmer to run.

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
- **The EEPROM is erased by default.** *Erase All Before Program* is
  **Selected** unless the `-OH` switch turns it off (§13, and §17.48 uses it
  that way: *"The device is not erased before programming (-OH command)"*) —
  so a plain `-M` discards the persist ring. That is the right default during
  bring-up: `persist_load()` returning false on a virgin EEPROM is a correct
  start, not an error.
- **`-Z<range>` is what preserves it**, and it is `Z<range>  Preserve EEData
  on Program`, default `Do Not Preserve`, in §13's switch table; §17.7 is the
  worked example, `/Z1400-147F /M`. §17.8 warns that `-E` overrides it, and
  `-E` is not passed here. **The range is `0-3FF`**, the whole 1,024-byte array
  (DS39977C Table 1). That IPECMD addresses this part's EEData from zero is not
  read out of the readme — it is observed, in the `-Y` failure recorded below,
  which reports `Address: 0` for the low byte of `total_ul`.
- **`-G<Type><range>` reads memory to the screen**, §13: *"Types P, E, I, C, B,
  A = output read of Program, EEPROM, ID, Configuration, Boot and Auxiliary
  Memory to the screen. P and E must be followed by an address range in the
  form of x-y."* So `-GE0-3FF` is the EEData dump, and it writes nothing.
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
| `-I` alone against a running board | the device ID, `Operation Succeeded` -- **and the board stops**, held in reset | 0 |
| `-I -OL` against a running board | the same, and it goes on running | 0 |
| `-I -W` into an open header | `Connection Failed.`, then `Operation Succeeded` | 0 |
| the programmer itself wedged | `Connection Failed.`, then `Operation Succeeded`, and **no `Connecting to MPLAB PICkit 3...` banner at all** | 0 |
| `-T` (list tools) | the tool list | 50 |
| `-C` on a blank part | `Blank check complete, device is blank.` | 0 |
| `-M -OL` on a blank part | `Device Erased...`, the areas to be programmed, `Programming/Verify complete`, `Program Succeeded` | 0 |
| `-Y` against a hex with no EEPROM section, with a persist record on the part | `Address: 0 Expected Value: ff Received Value: 0`, `Verify failed` | **7** |

**The one case the code gets wrong is the worst one:** a target nobody powered
returns 0 and prints `Operation Succeeded`. Bad ICSP wiring fails honestly with
1. Since `-W` is not used, an unpowered board is among the likeliest bench
mistakes there is.

**`-OL` belongs on the read-only commands too, and this is not obvious.**
*Release From Reset* is not about programming; it is about what state the part
is left in when IPECMD lets go, and the default is to hold it. So `-I` -- which
writes nothing and reads one register -- **stops a running converter**, and
leaves it stopped until something programs it again. Measured on a live board
both ways: with `-OL` it transmitted its nominal 22 frames a second straight
through the identify; without it, zero, and zero for as long as anybody
watched. The symptom is a board that answers the programmer perfectly and does
nothing at all, which reads as dead firmware or a wedged CAN module.
`tools/flash.py` passes `-OL` on every invocation for that reason.

**`Connection Failed.` has two meanings and the banner tells them apart.** With
`-W` into an open header it is about the target. On its own, with no
`Connecting to MPLAB PICkit 3...` line above it and no firmware version, it is
about the **programmer**: IPECMD found a tool and could not talk to it. Three
things distinguish it from a dead cable, and all three were observed together:

- `ipecmd -T` still lists the unit — `1  PICkit3 S.No : DEFAULT_PK3`
- Windows still reports the device healthy (`VID_04D8&PID_900A`, status OK)
- there is no `Programmer not found`, which is what a genuinely absent tool
  prints, with exit 9

**Unplugging the PICkit and plugging it back in clears it**, and moving it to a
port on a different controller cleared it when replugging into the same one did
not. It recurred several times in one session after a handful of successful
operations, so expect it rather than treating it as a fault in the board: the
board answers again immediately afterwards with nothing changed.

⚠ **It can strike between the identify and the program**, which leaves a part
that has been erased and not written — silent, no frames, and looking exactly
like dead firmware. `flash.py` stops at the first step that did not happen and
says which, so the recovery is to replug and run it again.

**So the tool must decide on the printed output.** Never branch on the exit
code alone, and do not encode §15's table.

**The `-Y` row is the one that will be misread**, so it is worth having the
whole reason in one place. `-M` programmes program memory and configuration
memory, and verifies what it wrote. `-Y` verifies **EEData as well**, against
the same hex — which carries no EEPROM section, so the expectation is the
erased `0xFF`. Meanwhile `-OL` has released the part from reset, so anything
the running firmware puts into the persist ring before the verify reaches it
is a difference the verify reports. Hence `Expected ff, Received 0` at address
0 — the low byte of `total_ul` — on a board that is programmed perfectly.

**Whether it fails therefore depends on what the firmware has had to store**,
which is not a thing a verify should be made to depend on. `persist_save()`
refuses to write a record that says nothing, so a part erased by `-OH` and
released onto a quiet bench bus stays erased and `-Y` passes; give the same
board a live bus for a second and the first record lands, after which it
fails. Two consequences for the tool, and neither of them is "it depends":
**run `-Y` only with `-Z0-3FF`-style expectations in hand, or not at all**, and
**never program with `-OL` and then verify** if the verify is to include
EEData. Exit 7 also happens to match *Readme for PK3CMD.htm* §9's
`7 operation failed`, which is the closest thing to a documented code IPECMD
has.

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

## What a `-GE` dump looks like, and the one thing no readme says

```
DFP Version Used : PIC18F-K_DFP,1.5.114,Microchip
...
The following memory area(s) will be read:
program memory: start address = 0x0, end address = 0x7fff
configuration memory
EEData memory
User Id Memory
Read complete
Read successfully.
EEPROM Memory
000000  00  00  00  00  00  00  00  00  80  00  A1  FA  45  00  00  00   . . . . . . . . . . . . E . . .
000010  00  00  00  00  80  01  EA  5A  FB  36  00  00  00  00  00  00   . . . . . . . Z . 6 . . . . . .
...
0003F0  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF   . . . . . . . . . . . . . . . .
Operation Succeeded
```

A six-digit address, sixteen bytes separated by **two** spaces, then an ASCII
column. Two things follow for anyone parsing it:

- **The ASCII column is what a line-anchored regex dies on**, and it cannot be
  cut positionally either without assuming the row width. Every cell of it
  renders one byte as one character, so reading tokens after the address and
  stopping at the first one that is not a hex pair always stops in the right
  place. `parse_eeprom_dump()` does that and then checks the *result* — the
  bytes must cover the whole array exactly once — so a layout it does not
  understand yields nothing rather than a scrambled image.
- **It reads more than it prints.** The header says program memory,
  configuration memory, EEData and User Id; only EEData appears. That is
  IPECMD's business, but it explains why a `-GE` is not instant.

⚠ **`-G`'s end address is EXCLUSIVE, and nothing in the readme says so.**
Measured both ways on the part:

| Command | Bytes returned | Last cell |
|---|---|---|
| `-GE0-3FF` | **1,023**, 0x000–0x3FE | printed as `--` |
| `-GE0-400` | **1,024**, 0x000–0x3FF | `FF` |

So a dump asks for `0-400`. This is the kind of off-by-one that would not have
announced itself: a parser that padded the missing byte would have compared an
image it never read and called the ring preserved.

**`-Z` is left at `0-3FF`, the readme's own form, and the asymmetry is
deliberate.** Whether its end is exclusive too has *not* been established, and
the way to find out is not to try `0-400` on a board holding a real trip: if
IPECMD rejected the argument and carried on programming, the erase would take
the ring with it. The only byte in question is 0x3FF, and `persist.c` uses
0..767, so both readings cover everything that matters.

---

## Preserving EEData: why it is three commands and not one flag

`--preserve-eeprom` runs

```
ipecmd -P18F25K80 -TPPK3 -GE0-3FF -OL              # before
ipecmd -P18F25K80 -TPPK3 -Fcanfuel.hex -M -Z0-3FF  # note: no -OL
ipecmd -P18F25K80 -TPPK3 -GE0-3FF                  # still held in reset
ipecmd -P18F25K80 -TPPK3 -I -OL                    # release
```

**The programming step deliberately omits `-OL`**, which is the opposite of the
rule everywhere else in this file, and the reason is the check rather than the
programming. Released immediately, the firmware starts running and can append a
persist record between the program and the read — after which a difference
between the two dumps says nothing about whether `-Z` worked. `persist_save()`
would not usually write that fast: `PERSIST_INTERVAL_MS` does not gate the
first call after a power-up, but the record has to have *changed*, and on a
quiet bench bus a restored one has not. **"Usually" is not a verification**,
and holding the part still costs one extra command.

⚠ **Which makes the release step load-bearing.** A part left in reset answers
the programmer perfectly and does nothing at all — the exact symptom this
file's `-OL` section describes, and the one that cost an afternoon. So the
release runs even when an earlier step has failed, and if it fails too the tool
says outright that the part may still be held and what to run. `--identify` is
that command, and it is the same `-I -OL`.

**The comparison is byte for byte and the whole array**, not a checksum and not
the ring's 768 bytes. If `-Z` were ignored the array comes back all `0xFF`,
which the dump summary reports in as many words; anything else that differs is
worth seeing rather than hashing away.

**Observed, on a board holding 38 records:** `Device Erased...` appears in the
programming output exactly as it does without `-Z`, and the EEData comes back
identical anyway — 455 of 1,024 bytes written, before and after. So the erase
message is not the thing to read; the comparison is.

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
