# The next drive — what to do, in order

**One drive, two questions, no USBtin and no dismantling.** This is the
procedure for the run after the injectors are fitted. It exists because the
last drive answered less than it could have, purely for want of one channel
that takes five minutes to add.

The two questions, and they are independent of each other:

1. **Is the engine well now?** Feel, first-gear misfires, the idle adaptation,
   cold starts.
2. **Does b7 ever approach 255?** Which decides whether the display can ever
   show the factory maxima at all — `src/config.h` above
   `TORQUE_CNM_PER_BIT`, and `docs/engine-health.md` for why it is in doubt.

⚠ **The oil temperature is not on this list, and that is deliberate.** The
hot-oil refit is worth **+0.7 % at the peak** (`can-decoding.md` question 7),
so it does nothing for the maxima. Take the reading if the drive happens to be
long enough — if the oil genuinely never passes ~75 °C, question 7 closes for
free — but do not plan the drive around it.

⚠ **The USBtin is not needed either.** It would settle the drag line and
nothing here, and it needs the dashboard open. Leave it.

---

## Before the car moves

**1. Upload the display configuration.** `S-AQY.TRI` in the `mfd15` repo has
one new row appended, `TorqRaw` — **0x280 byte 7, raw, 0 to 255**. It is the
same trick as `FuelCntRaw` and `TankL`: the untouched byte beside the number
this firmware computes from it, so the two can be compared in one glance.

Follow `mfd15/README.md`, *Uploading the file*. The display's Wi-Fi hotspot is
off by default and is turned on by holding both buttons. **Do not reorder the
rows** — the file is addressed by position and the new row is appended, not
inserted.

⚠ **Upload the file again after any page change**, even one that looks
harmless. The MFD15 can lose its sensor definitions when a page's contents are
edited, and **RPM disappearing is the tell** (`install.md` step 2).

**2. Put `TorqRaw` on a page where it can be read at a glance**, next to
`Torque` and `RPM`.

**3. Set VCDS up but do not start logging yet.** Group **003** — engine speed,
mass air flow g/s, throttle angle, ignition advance — and group **010** —
engine speed, load %, throttle angle, advance. Both, and nothing else: a third
group drops the sampling rate to about one sample a second, which is too slow
for a pull that lasts five to eight seconds.

**Group 014 is deliberately not logged.** Its counter is cumulative-looking but
is in fact a current count, so it is read on the screen afterwards rather than
sampled. See below.

**4. Do not clear the fault memory**, before or after.

---

## The drive

**5. Warm it up properly first.** Everything below wants a warm engine, and the
holds are worthless cold.

**6. ⚠ Reset the display's min/max once the engine is running, and before the
first pull. This step is not optional and the whole `TorqRaw` reading depends
on it.**

**b7 reads 191 while the starter is turning.** `06_trip_reset` carries 70
frames of it — b7 = 191 at 187 rpm with the throttle at its rest position — so
a max that was armed before the engine fired records a cranking artefact and
nothing else. The firmware itself is immune, because `compute_torque_d()` gates
on `TORQUE_MIN_RPM`; **the raw display channel has no such gate**, and the TRI
format has no validity gate to give it one. `mfd15/docs/sensors.md` §10 has the
same problem on `OilTemp` and the same answer.

**7. The pull that matters is in a HIGH gear from about 2400 rpm.** Fourth or
fifth, or up a hill — anywhere the engine *sits* near peak torque instead of
flashing through it. Start the VCDS log, floor it, hold it to about 5500 rpm,
lift.

**This is the step the last drive got wrong**, and it is worth being blunt
about: peak torque is at 2400 rpm and the previous log had essentially no
full-throttle data below 3000, because every pull was a first- or second-gear
sweep that crossed 2400 in a moment. **Two or three pulls in a high gear are
worth more than ten in a low one.**

**8. Do a low-gear pull to high revs as well**, as before, for the power end.
The last one reached 5720 rpm and that part of the data was fine.

**9. Watch for misfires in the states that produced them** — a slow pull-away
in first, and downshifting to first while braking almost to a stop.

---

## Straight after, with the engine still idling

**10. Read `TorqRaw`'s maximum off the display** and write it down with the
gear and roughly where in the rev range it happened.

**11. Read group 014 on the screen.** `Rozpoznani` must say **`aktiv.`** — if
it says `deaktiv.` the engine is not running and the number below it is
meaningless. Note the misfire count.

**12. Read group 032**, the lambda adaptations, and note both values. They were
−4.7 % at idle and +1.6 % at part load before the injectors.

**13. Note the oil temperature maximum** off the display, if the drive was long
enough to be worth anything.

---

## What comes back here

Four things, and the second one is the point of the whole exercise:

| | |
|---|---|
| the VCDS log file | as before |
| **`TorqRaw` max**, with the gear and rev range | **the new one** |
| group 014 with `aktiv.` showing, and group 032 | |
| how the car felt | not a soft measure here — see the prediction below |

**`TorqRaw` max against the load percentage from the same rpm is what settles
the ceiling**, and both numbers now come off instruments already in the car:

| if | then |
|---|---|
| `TorqRaw` / 255 ≈ the ECU's load % | b7 carries the reference charge is normalised to, 255 is unreachable with real air, and **the factory maxima can never be displayed** — the scale needs redefining |
| `TorqRaw` / 255 clearly above load % | the current derivation stands, and a healthy engine near 2400 rpm should push toward it |

**The prediction, written before the drive so it can be wrong.** If the
injectors were the fault: the car pulls better, first-gear misfires go to zero
and the idle adaptation moves toward zero — while **load stays near 78 % and
`Torque` on the display stays near 117 Nm**, because none of the model's inputs
moved. `docs/engine-health.md` argues why, and what it means if the displayed
maxima jump instead.

---

## What this drive does not do

- **It does not refit the drag line.** That wants steady holds in neutral on
  95–110 °C oil and a bus capture, which means the dashboard open.
  `can-decoding.md` question 7.
- **It does not measure torque.** Nothing here is a dynamometer. It measures
  the ECU's own byte and how close that byte gets to its ceiling.
- **It does not need the converter reflashed.** Nothing in `src/` changed.
