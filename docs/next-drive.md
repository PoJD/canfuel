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

## Two configurations, and they answer different questions

**Three instruments want one connector and they cannot all have it.** The
converter is powered by 5 V from the display, so unplugging the display
unpowers the converter too, and a USBtin on that pair means neither is there.

**That is not the problem it looks like, because the two questions want
different configurations anyway.**

| | **A — display and converter fitted** | **B — USBtin, display and converter out** |
|---|---|---|
| runs alongside | VCDS | VCDS |
| gives | everything the converter computes, plus `TorqRaw` and `OilTemp` as max-hold and live readings | **the car's whole bus at ~94 frames a second per identifier**, so b7, engine speed, oil temperature, throttle and the fuel counter, each with the others beside it in time |
| answers | is the converter's arithmetic right — `FuelNow` against `FuelCntRaw`, `Torque` against `TorqRaw` | is the *car* right — the stumbling idle, the drag line, how hot the oil actually gets, and b7 against the ECU's load |
| cannot | sample fast enough to count a stumble | say anything about the converter, which is unpowered |

⚠ **`OilTemp` is not ours.** The TRI row reads `0x420` byte 3 — the car's own
frame — so it survives the converter being unplugged but not the display being
unplugged. In configuration B it does not need to be read at all, **because it
is in the capture**: every frame of 0x420 carries it, next to everything else.

**Which makes B the measurement configuration and A the verification one.** A
capture holds b7 at ninety-four samples a second with engine speed and oil
temperature beside each one; `TorqRaw` on the display is the same byte as a
single held maximum. Use A to check the converter, B to measure the engine.

---

## Configuration B — one continuous capture, and it answers three questions

**Do not take two sittings at two guessed temperatures. Take one capture
through the whole warm-up** and sort it by temperature afterwards.

What that buys over the two-sitting version below:

- **Two points become a curve.** The fixtures give 61 °C and 73 °C; a
  continuous record gives the stumble rate against temperature throughout, and
  that is a different quality of evidence.
- **Nothing has to be judged in the car.** No deciding when 60 °C has arrived.
- **The transition cannot be missed**, because the whole of it is recorded.
- **It is directly comparable with `09`, `11` and `12`** — same identifier,
  same rate, same analysis.

**The order, in one sitting:**

1. Start the capture at a cold start, or at the latest once the coolant gauge
   has settled — the interesting window is entirely *after* that.
2. **Idle, undisturbed, for several minutes.** This is the stumble data at the
   lower oil temperature and it is the part that is easy to cut short.
3. Drive until the oil temperature stops climbing. **Keep capturing.**
4. **Idle again for several minutes**, now fully soaked.
5. If the oil is as hot as it is going to get, add the free-revving holds in
   neutral from `can-decoding.md` question 7 while it is still running.

**It tests question 7's premise as a side effect, and may close it.** That
question rests on "72–77 °C is warm, not the 95–110 °C of real driving". **If
this engine's oil does not pass about 75 °C, that sentence is false for this
car** — the drag line is already fitted at the temperature the engine actually
runs at, and the question closes as *no refit needed* rather than staying open
indefinitely. Yesterday's drive peaked at 72–74 °C over about seven minutes of
logging, which is nowhere near long enough to have found the ceiling.

**Practicalities.** The whole bus is roughly **one megabyte per minute**, so
twenty-five minutes is about 25 MB — fine to write, awkward to hand over.
Filter to `0x280`, `0x420` and `0x1A0` before sending it anywhere; nothing this
analysis needs is outside those three. `tools/usbtin_capture.py` writes line by
line as it goes and its own header explains why filtering belongs afterwards
rather than in the adapter.

⚠ **VCDS runs at the same time** — different connection, and
`docs/vcds-session.md` establishes that the two do not interfere. So this
configuration gives the raw bus *and* mass air flow, load and the misfire
counter together, which is the richest combination available on this car.

---

## Configuration A — the idle test without opening anything

**This one is not about the drive at all**, and it is easy to skip because
nothing exciting happens during it. It is the test with a prediction already
attached: `docs/engine-health.md` measures the stumbling idle out of the
fixtures and finds it present at 61 °C of oil and absent at 73 °C, with the
coolant at 99 °C in both. If the injectors were the cause, **both states should
now be clean.**

**The gauge on the dashboard cannot see this.** It reads the coolant, which is
already at the top in both states. Use `OilTemp` on the display.

**Two sittings, each about two minutes:**

| when | oil | what to do |
|---|---|---|
| after the coolant has settled but the engine is not yet soaked | around **60 °C** | idle, count the stumbles, watch group 014 |
| after another twenty minutes of running or driving | **73 °C or more** | the same again |

**At each one, keep group 014 on the screen with `Rozpoznani` showing
`aktiv.`** The question it answers is the one nothing else can:

- **stumble and the counter increments** → it is a combustion event, so the
  air path and the evaporative system are out
- **stumble and the counter stays at zero** → it is not a misfire but a
  disturbance of the charge, which points at purge or idle air control and
  **away from the injectors**

**Log group 010 on its own for each sitting**, not two groups. One group
samples at about 3.3 per second against 1.7 for two, and a stumble lasts a few
hundred milliseconds, so the rate is the whole game here. ⚠ **Even at 3.3 per
second this undercounts** — many events will fall between samples. That is
acceptable because both sittings undercount equally, so the *comparison*
between the two thermal states survives even though the absolute count does
not.

⚠ **This configuration cannot produce a number comparable with the fixtures.**
Those come from 0x280 at about ninety-four frames a second and nothing VCDS
does approaches it, so what configuration A gives here is a yes/no on whether
the stumbles are misfires — which is worth having on its own, and is all it is.
**Configuration B above is the one that measures them**, and it batches with
the hot-oil sweep and everything else in `install.md` step 11, since all of it
needs the dashboard open once.

**What the three long-standing symptoms have in common** is worth keeping in
view while testing: the exhaust destroying itself progressively, the stumbling
idle, and poor cold starts have all been present for years. One cause that
produces all three is worth more than three separate explanations, and a
leaking injector is currently the only candidate that does.

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
`Torque` on the display stays near 117 Nm**.

⚠ **The last clause rests on an unsourced premise and is the weakest thing in
this document.** It assumes the ECU's torque model cannot see a fuelling fault,
which needs the lambda entering that model to be the *commanded* value — and
nothing this project holds says so. `frames.md` sorts what is founded from what
is recalled. **Misfire detection is per-cylinder and does run on this car**, so
the ECU is not without a combustion signal; whether it reaches the torque model
is simply unknown.

Which makes this the most informative line on the page rather than the least:
**if the displayed figures rise while load and airflow stay put, the premise is
wrong and we learn something we could not have got any other way.**

---

## What happens after the reading — the decision tree

**Step 1 is the engine, because otherwise you are calibrating against a sick
one.** Does it pull better with the new injectors? If not, today's numbers were
already its best and you go to step 2 with them; if it does, re-measure and go
to step 2 with the new ones.

**Step 2 is `TorqRaw`'s maximum at full throttle**, with the ECU's load from
the same engine speed beside it:

```
b7max >= 235
  -> The scale is right and the engine is well. The display reaches
     near the factory figures. NOTHING CHANGES.

b7max 200-235
  -> The scale is roughly right; the display reads 5-15 % under.
     TORQUE_TRIM_PCT closes that if the owner wants it closed.

b7max <= 200   (what this car reads now)
  |
  +- load also unchanged, near 78 %
  |    -> Same air, same modelled torque. Either the engine is still
  |       unwell, or THE SCALE IS WRONG. What separates them is how the
  |       car drives: if it pulls properly, it is the scale.
  |
  +- load jumped, near 85 %
       -> The engine breathes better and b7 did not follow, so b7 is not
          what this firmware thinks it is and the derivation is rebuilt
          from the beginning rather than rescaled.
```

### What the last branch actually changes

**The formula does not move. One premise does.** Today it reads *b7 = 255
corresponds to the rated crank torque plus the drag at that speed*. It would
become *b7 = the observed maximum at full throttle corresponds to the rated
figure*.

1. **`TORQUE_CNM_PER_BIT` rises.** Sketched against b7 extrapolated from
   `17_drive_property_z1`'s wide-open samples, the 85 kW rating asks for about
   1.08 Nm/bit and the 170 Nm rating for about 1.26.
2. **And that bracket is the finding, not the number.** It is roughly **15 %
   wide, against the 0.3 % the current derivation reports.** The 0.3 % was
   never a precision: substituting 255 into both rating equations pins them to
   the same nail, so of course they agree. Pull the nail out and the two
   factory figures start arguing, which is an honest picture of how well this
   is known. **Whatever replaces the scale should quote the bracket its own
   assumption produces, not inherit this one.**
3. **The drag line is rescaled, not refitted.** `drag_b7 = 9.11 + 0.006514 x
   rpm` is in bytes and does not move; `DRAG_TORQUE_BASE_CNM` and
   `DRAG_TORQUE_SLOPE_Q16` are that line times the scale, so they follow it.
   This is what `config.h` means by the two being one calibration.
4. **Both ceiling tests are rewritten.** `test_full_scale_reaches_the_rated_power`
   and `..._torque` asserts what b7 = 255 produces. They would assert what the
   OBSERVED maximum produces — which is the first version of that test with a
   measurement behind it.
5. **`TORQUE_TRIM_PCT` is not the tool for this** and must not be used as one.
   A scale that is wrong is wrong for everybody who builds this firmware; the
   trim is one owner's gain on a correct scale. Fixing the first with the
   second leaves the next person a number that no longer means what its
   comment says.

The display needs no change either way: `Torque` tops out at 200.00 in
`S-AQY.TRI` and `Power` at 100.00, so the larger figures still fit.

---

## What this drive does not do

- **It does not refit the drag line.** That wants steady holds in neutral on
  95–110 °C oil and a bus capture, which means the dashboard open.
  `can-decoding.md` question 7.
- **It does not measure torque.** Nothing here is a dynamometer. It measures
  the ECU's own byte and how close that byte gets to its ceiling.
- **It does not need the converter reflashed.** Nothing in `src/` changed.
