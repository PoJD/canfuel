# Firmware — open questions

**The questions about what this firmware reads and transmits that are still
open**, each with what is known, what it costs while it stays open, and the
measurement that closes it. The numbers are the ones `can-decoding.md` has
always used, because code and documents cite them; the answered ones are in
`can-decoding.md` under *Resolved questions*, and the ones not worth answering
under *Never resolved but not required*.

**One is open, 12** (18/11/2026; updated 19/11, the morning's drop-out and the evening without one). **11** (`IdleHealth` against VCDS 014)
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
restarts. **MisfAvg is read from the car only when StartCrank shows a
value** (*the owner's rule*, 18/11). It holds in the code: a converter
that restarts with the engine turning finds it already running
(`start_watch()`, `HEALTH_START_UNKNOWN` → `RUNNING`), so the start is
not seen and StartCrank stays 255 until the next start from a
standstill, and the start's totals are cleared only at such a start. A
quiet bus does not fake one: `start_watch()` runs only when a 0x280
arrives. A CAN-only drop-out leaves the totals as they were, and the
idle it hid is in neither half of the mean.

**The harness fuse, 18/11 evening** (*owner*, the display and converter
out of the car). Across the loom's connector CAN and ground read 0.2 Ω;
the 5 V line starts the same and creeps up to **2.7 Ω**. The line
carries the harness fuse (`kicad`, `canfuel/docs/implementation-plan.md`
§9.2: SIBA 179120.0.2, 200 mA time-lag glass, in an inline K23411
holder). Two spares read **1.9–2.0 Ω** once the meter settles. Nothing
visible on the old one under a loupe. **The fuse was replaced**; the
test is the next few days in the car.

What the datasheet says (SIBA G79120-30 Rev. 0, quoted in §9.2): 500 mV
drop at the rated 200 mA, 2.5 Ω hot; I²t 0.7 A²s; at 1.5 In = 0.30 A at
least 1 h before it opens, at 2.1 In = 0.42 A between 600 ms and 2 min.
What follows (*reasoned*):
- **A fuse that was opening would have stayed open.** The converter came
  back every time, so what broke the supply was a contact that opened
  and closed again — inside the fuse's end caps or the holder's cap and
  springs. The old fuse's extra 0.7 Ω is not it: at the converter's
  ~30 mA average (§9.2) that is about 20 mV, and the transceiver's
  dominant-bit peaks come from C6 downstream.
- **A momentary open is enough to restart the part.** At ~30 mA the
  ~10 µF behind the fuse loses a volt in about a third of a millisecond,
  so an open of about a millisecond takes VDD under the 3.0 V brown-out
  (`BORV = 0`, `pic_config.h`).
- **An overcurrent has nowhere to come from.** The board's inrush is
  about 10⁻³ A²s against 0.7 A²s (§9.2), and a fault on the 5 V side
  big enough to age the element would have to hold far above 0.30 A.
  Whether a glass fuse's resistance rises with use is not in the
  datasheet; the spares' 1.9–2.0 Ω against 2.7 Ω through the old one
  and its holder does not separate the fuse from the holder.
- **A shorter open can take the CAN link alone.** The MCP2562 lets go
  of the bus when its VDD falls under its POR comparator's low level,
  3.4–4.0 V (DS20005167C §1.6, VPORL), and comes back above 3.8–4.3 V
  (VPORH) — above the PIC's 3.0 V brown-out. An open that takes VDD
  under about 4 V but not under 3 V drops the converter off the bus,
  frames cut mid-way among them (the MFD's red, *reasoned*), and the
  part runs on with its values kept. **So one intermittent contact in
  the 5 V line accounts for all three things seen**; the CAN pair's
  own contacts or the board remain the other explanation for the
  CAN-only ones.

A larger fuse is not called for unless a 200 mA one actually blows (it
then stays open). The display's limit of 0.5 A is what the rating
protects.

**The holder, 18/11 evening** (*owner*): now and then, rarely, the
converter seemed not to run at all while the bus did — the ECU's own
values on the display, zeros from the converter — and **pressing on the
MFD's body always brought it back**, which is pressing on the fuse
holder behind it. The holder was wrapped over in fabric tape
(`kicad`, `canfuel/docs/harness.md` D2) on a section of loom bent hard;
the tape may have pulled on the holder's cap and slackened the spring
inside. **The new fuse now sits in the holder with no tape over its body**; the
loom was re-taped the same evening up to and over the holder's ends, so
nothing bare shows, and everything looked stable after (*owner*). Over
the last few days a light touch on the display had been enough to drop
the converter (*owner*): the spring in the holder must be well seated,
and the tape's pressure over it upset it (*owner*'s reading).
The old fuse is kept; three spares in hand. This makes the holder's
contact the leading explanation of the drop-outs (*reasoned*), the
board's joints the other.

**The LED found, 18/11 evening** (*owner*): a cold joint on a resistor
by JP1 — moving it starts an LED blinking; left alone it is quiet and
the converter is not in debug. By `kicad`'s parts list
(`implementation-plan.md`) R2 is RA0's 10 kΩ pull-down: with its joint
open RA0 floats, reads high now and then, and the LEDs and 0x603 follow
(*reasoned*). **If it is R1** (MCLR's 10 kΩ pull-up) instead, a floating
MCLR resets the part, and that would be a cause of the restarts too.

**The owner's view**: the board itself, cold joints, or the fuse's
contact; a second board is to be built in any case, as a spare.

**The second board, 19/11** (*owner*): assembled, left to dry, not yet
flashed. Its joints are, by the owner's reading, sounder throughout than
the first board's, and its LED pads are undamaged — on the first board
they are not. Photos are in the owner's album, not in the repository.

**The tests, one change at a time**: the harness was repaired on 18/11
(new fuse, holder re-taped, above), and **the first board goes back into
the car on its own first**, so the harness repair is tested alone. If the
drop-outs stop, the holder was the cause. Then the second board replaces
it once flashed (`docs/firmware/flashing.md`); if drop-outs that
survived the harness repair stop on it, the first board's assembly was
the cause. Not worked on with Claude (*owner*: the engine and the idle
first); recorded so it is not lost.

**The first morning on the repaired harness, 19/11** (*owner*; the first
board in the car, the harness's fuse and holder as repaired on 18/11):
**before the start the MFD showed the bus fault again; moving the MFD
brought it back**, and it then held the whole drive to work, through
switching the display's screens too. So the harness repair alone did not
stop it. A contact the MFD's movement works is still the explanation —
the holder, the MFD's own plug or the board's joints through the loom's
pull (*reasoned*); **the owner's reading: perhaps not only the harness
but the board too.** **Next, the owner's**: the second board flashed and
fitted over the coming days (`docs/firmware/flashing.md`); the first
board's joints repaired some time later. **A printed enclosure that takes
the loom's pull off J1/J2** (`kicad`, `canfuel/enclosure/`; `refuted.md`
D2) **was printed on 20/11 and fits the vent** (*owner*); the second board
is flashed and goes into it the same evening.

**The evening of 19/11** (*owner*): the drive home, about 50 minutes,
**no drop-out**, and StartCrank shown at the end, so the converter ran
from the start to the stop and MisfAvg (4.1) covers the drive. One day
without a drop-out after the MFD was moved in the morning; not yet a
test of anything, the harness and the board both unchanged since.

The engine's own faults are not here; they are `docs/engine-health/open.md`.
