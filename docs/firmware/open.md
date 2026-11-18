# Firmware — open questions

**The questions about what this firmware reads and transmits that are still
open**, each with what is known, what it costs while it stays open, and the
measurement that closes it. The numbers are the ones `can-decoding.md` has
always used, because code and documents cite them; the answered ones are in
`can-decoding.md` under *Resolved questions*, and the ones not worth answering
under *Never resolved but not required*.

**One is open, 12** (18/11/2026). **11** (`IdleHealth` against VCDS 014)
**closed on 8/11/2026** at the owner's decision — the grade stays as it
is, with `Misfires` beside it — and moved to `can-decoding.md`, *Resolved
questions*, with its whole record; **7 closed on 15/10/2026** and **10 on
23/10/2026** the same way. A new question starts here with the next
number, 13.

---

## 12. The converter drops out in the car now and then

**What is seen** (*owner*, 18/11/2026; it has recurred over weeks):
- **Sometimes only the CAN link goes**: the MFD loses the converter's
  frames and comes back with its values kept.
- **Sometimes the converter's supply goes too**: the start's figures
  (the crank and the dips on 0x604) come back at their defaults, so the
  part has restarted.
- **The MFD flashes red at times**: bus errors, by the owner's reading
  only between the MFD and the converter. The car's control units have
  never stored anything.
- **An LED on the converter blinks now and then with JP1 off.** Both
  LEDs are written only while `hal_sys_debug_enabled()` reads RA0 high
  (`hal_sys_led_pwr()`, `hal_sys_led_can()`), so a blink without the
  jumper means RA0 was read high for that pass (*reasoned*). That points
  at the JP1/pull-down node, not the code.

**What it costs**: every figure the converter keeps since its start —
MisfAvg first, the start bytes, the trip — is short of the drive when it
restarts. **MisfAvg is not reported from the car until this is
settled** (*owner*).

**The owner's view**: the board itself, cold joints. **The test**: the
second board he plans to build — if the drop-outs stop on it, the first
board's assembly was the cause. Not worked on with Claude (*owner*: the
engine and the idle first); recorded so it is not lost.

The engine's own faults are not here; they are `docs/engine-health/open.md`.
