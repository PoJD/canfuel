# Firmware — open questions

**The questions about what this firmware reads and transmits that are still
open**, each with what is known, what it costs while it stays open, and the
measurement that closes it. The numbers are the ones `can-decoding.md` has
always used, because code and documents cite them; the answered ones are in
`can-decoding.md` under *Resolved questions*, and the ones not worth answering
under *Never resolved but not required*.

**One is open, 12**, the CAN link (18/11/2026; condensed 20/11 to the current problem). **11** (`IdleHealth` against VCDS 014)
**closed on 8/11/2026** at the owner's decision — the grade stays as it
is, with `Misfires` beside it — and moved to `can-decoding.md`, *Resolved
questions*, with its whole record; **7 closed on 15/10/2026** and **10 on
23/10/2026** the same way. A new question starts here with the next
number, 13.

---

## 12. Now and then the CAN link drops or errs, in the car

**What is seen** (*owner*, 20/11/2026): now and then the MFD shows its
**red CAN icon** and loses the converter's frames, and comes back with
the values kept; at the same moment **the converter's LED_CAN (D2,
yellow) blinks** — frames still arriving with an error counter above
zero (`main.c`, *the LEDs*), so the converter's own CAN module sees the
bus errors too (*reasoned*). **Only after a cold night**, and on 20/11,
cold all day, again and again. The car's control units store nothing.

**Ruled out**: the supply — since the harness fuse was replaced (18/11)
the converter has not restarted once, StartCrank showing a value at
every start, a quick one before the MFD has booted included; and the
board — the second board, in the printed enclosure since 20/11
(`kicad`, `canfuel/enclosure/`), behaves as the first.

**Left**: **a CAN wire, a crimp on one or a connector's contact in the
harness** (*owner*); one that opens as it contracts in the cold fits a
crimp or a contact rather than a wire (*reasoned*).

**What it costs**: a CAN-only drop-out leaves the converter's totals as
they were; the display misses its frames while it lasts.

**Next, if it keeps coming** (*owner*): on a cold morning, when it
shows, ring out every CAN wire of the harness end to end, flexing the
loom along its length with the meter on it (`kicad`,
`canfuel/docs/harness.md`). **JP1 is on since 20/11** (left on, kept so):
LED_CAN shows a drop-out at the converter, and 0x603's latched
`DIAG_FLAG_UNHEALTHY` and error counters record one nobody watched
(`frames.md`). The first board is the spare.

The history up to 20/11 — the restarts, the fuse and its holder, the
first board's cold joint, the second board — is in git: `git show
bef2fd6:docs/firmware/open.md`.

The engine's own faults are not here; they are `docs/engine-health/open.md`.
