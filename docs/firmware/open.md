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
bus errors too (*reasoned*). **Warm too**: the cold was chance (*the
owner's correction*, 20/11 night; *this read "only after a cold night"
until then*) — with the car warm it drops out, **sometimes only on
switching the MFD's screen**, which means touching the display. The
car's control units store nothing.

**Ruled out**: the supply — since the harness fuse was replaced (18/11)
the converter has not restarted once, StartCrank showing a value at
every start, a quick one before the MFD has booted included; and the
board — the second board, in the printed enclosure since 20/11
(`kicad`, `canfuel/enclosure/`), behaves as the first.

**Left**: **a CAN wire, a crimp on one or a connector's contact in the
harness** (*owner*). **Narrowed on the evening of 20/11
to the MFD's side** — the short cable from the converter to the MFD or
the MFD's connector, which has play (below).

**What it costs**: a CAN-only drop-out leaves the converter's totals as
they were; the display misses its frames while it lasts.

**Next, if it keeps coming** (*owner*): when it shows, ring out every CAN wire of the harness end to end, flexing the
loom along its length with the meter on it (`kicad`,
`canfuel/docs/harness.md`). **JP1 is on since 20/11** (left on, kept so):
LED_CAN shows a drop-out at the converter, and 0x603's latched
`DIAG_FLAG_UNHEALTHY` and error counters record one nobody watched
(`frames.md`). The first board is the spare.

The history up to 20/11 — the restarts, the fuse and its holder, the
first board's cold joint, the second board — is in git: `git show
bef2fd6:docs/firmware/open.md`.

**The evening of 20/11** (*owner*): **a crimp on the car side** of the
loom, on the CAN wires, long distrusted, **was redone** (photos in the
owner's album) — **and the drop-outs go on**. **A light touch on the
MFD still brings the bus back.** Left dropped out for a while on a
drive, **TripDist jumped by about 0.4 km when it came back**, the
distance driven in the gap. *Reasoned*: the trip is integrated from
the car's speed frames (`compute_tick()`), so **through the gap the
converter was powered and receiving the car** on the CAN pair, and
what was lost was the MFD's side. **The owner's reading: the fault is
not on the converter's side, where the connector was just redone, but
in the short cable from the converter to the MFD or in the MFD's own
connector, where the USBtin is always plugged in.** That fits the touch
on the MFD. LED_CAN blinking at the same moments does not argue
against it (*reasoned*): a contact that bounces on a stub disturbs
frames for every node on the bus, while the converter goes on
receiving between the errors, as the trip shows.

**Whether the USBtin's DuPont jumpers opened the sockets.** Molex
SD-43045-001 (the Micro-Fit 3.0 header, `kicad`,
`canfuel/docs/micro-fit-43045-datasheet.pdf`) gives the mating pin as
**0.64 mm square** (.025 SQ TYP); the 43030 socket is made for that.
The jumpers' pins have no datasheet here; the usual 2.54 mm jumper pin
is nominally the same 0.64 mm square, so by size alone it should not
open a 43030 socket — but **a jumper is not latched and is levered
sideways at every touch**, and a cheap pin may be oversize or burred.
**Decision** (not a datasheet fact): measure a jumper pin with
calipers; a socket that lets a 0.64 mm pin fall out under its own
weight is opened. A socket that is suspect is re-crimped with a new
43030 terminal (spares in hand) rather than bent back, and **the USBtin
gets its own adapter with a real Micro-Fit plug**, so nothing but
Micro-Fit pins enters the loom's sockets again (the owner's idea, a
spare cable used only with the MFD, does the same from the other end).
Whether the sockets in the MFD's plug C are of a family a 0.64 mm pin
fits is not known here.

**The short cable rung out, 20/11 night** (*owner*): both CAN lines
with the multimeter, the cable flexed — **nothing**. *Reasoned*, what
that does not rule out: an open of milliseconds, which a meter's
display does not catch (its beeper is quicker, and the bus needs only
a bit's worth); a socket's grip on a mated pin, which probing the
cable end does not load. **Decision**: the sockets are tested with a pin in
— a 0.64 mm pin (a Micro-Fit pin or the header) in each, the meter on
the beeper through it and the cable, pin and cable wiggled — and the
ringing repeated at once when the fault shows, as *Next* says.

**The MFD's own connector, 20/11 night** (*owner*): **it has play and
moves on the display.** Moved by hand with the loom held fixed, it did
not make a drop-out. *Reasoned*: a connector that wobbles on the
display's body can be the plug loose in its header, or the header loose
on the display's board — **its solder joints or its anchoring inside the
MFD**, which a press on the display's buttons flexes and a hand on the
plug alone may not; one failed attempt does not clear it. **Decision**:
the play taken up (the plug pushed fully home and wedged or taped to the
display's body so it cannot rock) and the display used as before; if
the drop-outs on switching screens stop, the fault is at that
connector, and whether in the plug or inside the MFD is then the
question, the display opened only if it comes to that.

**The owner's decision, 20/11 night**: not the wedge test — **the MFD
opened and repaired properly**. His suspicion: a joint of the
connector inside the display has loosened from the plug being pulled
out and pushed back so often (for the USBtin among others). The joints
checked inside and resoldered, and **the connector bedded in adhesive
round it, so the loom's pull is taken by the adhesive, not the
solder**. *General*: an acetic-cure silicone gives off acid that
corrodes copper and solder; a neutral-cure one or an epoxy does not;
the mating face and the latch kept clear. **The test after**: the
screens switched and the display touched as before — a drop-out then
puts the fault back in the loom (the short cable, its sockets, ringing
out with a pin in, above).

The engine's own faults are not here; they are `docs/engine-health/open.md`.
