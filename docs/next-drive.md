# The next drive — one session, in order

**This is the procedure for the first drive after the injectors, spark plugs,
ignition leads and silencers are fitted.** One session, one configuration, one
capture. It is written to be followed in the car without deciding anything.

**Nothing happens before then.** The car stands until the parts are on, because
a new catalytic converter behind a cylinder still dumping raw fuel is the same
converter that was cut open — and that is a four-figure risk taken to buy a
before-and-after comparison nobody needs. **There will be no clean before/after
and that is accepted**; the fixtures already hold the "before" for the one
measurement that matters, the stumbling idle.

---

## What this session answers

| question | what settles it |
|---|---|
| **is the engine well now** | first-gear misfires, the stumbling idle against oil temperature, the idle adaptation, how it pulls |
| **can the display ever show the factory maxima** | b7 at full throttle against the ECU's load at the same engine speed |
| **does the oil ever get hot enough to matter** | the oil temperature that a long drive actually reaches |

**The third one is close to answered already and this only confirms it.** The
drive of 2026-09-10 peaked at **72–74 °C of oil after about an hour of
driving** — and the warm holds the drag line is fitted to are 72.8–76.6 °C, the
same range. `can-decoding.md` question 7 rests on "72–77 °C is warm, not the
95–110 °C of real driving", and that sentence appears to be false for this
engine. If a long capture confirms the ceiling, **the question closes as *no
refit needed*** rather than staying open indefinitely.

---

## The configuration — and why there is only one

**The display and the converter come out; the USBtin goes on that pair.** They
cannot share it: the converter is powered by 5 V from the display, so removing
one removes both.

**That loses nothing this session needs.** A capture carries b7, engine speed,
oil temperature, road speed, throttle and the fuel counter at about ninety-four
frames a second each, every one of them with the others beside it in time. The
`TorqRaw` channel added to `S-AQY.TRI` is that same byte reduced to a single
held maximum — useful when the dashboard is closed, and simply outclassed here.

⚠ **`OilTemp` is not the converter's.** Its TRI row reads `0x420` byte 3, the
car's own frame, so it is one of the channels the display takes off the bus
directly. In this configuration it does not need to be watched at all, because
**every capture carries it**.

**The converter's own arithmetic is not checked on this trip, and does not
need a trip of its own either.** `FuelNow` against `FuelCntRaw` was the
bring-up check in `install.md` step 10; it passed, both move together, and
repeating it proves nothing new. What is left is covered under *After the
reflash* at the end of this document — for free, as part of something that has
to happen anyway.

---

## What to run

**On the laptop, two things at once. They do not interfere** — the USBtin is on
the CAN pair and VCDS is on the OBD socket, over K-line
(`docs/vcds-session.md`).

**1. The capture**, listen-only, for the whole session:

```
python tools/usbtin_capture.py --seconds 3600 --out postfix_z1.txt
```

**2. VCDS logging, groups 003 and 014, running throughout.**

**Not 010, and the reason is worth knowing**, because the obvious pairing is
the wrong one:

| group | fields |
|---|---|
| **003** | engine speed · **mass air flow** · throttle angle · ignition advance |
| 010 | engine speed · engine load · throttle angle · ignition advance |
| **014** | engine speed · **engine load** · **misfire count** · detection state |

**Group 014 already carries the load**, so `003 + 014` is a superset of
`003 + 010` with the misfire counter added and nothing given up. Logging the
misfires therefore costs **no** sampling rate at all, where adding 014 as a
third group would have dropped it from about 1.7 samples a second to 1.1.

⚠ **Two groups, never three.** The rate is the one thing that cannot be
recovered afterwards.

**Mass air flow and engine load are the point of the second instrument** —
neither is on the CAN bus, so the capture cannot get them and only VCDS can.

**Write down two more numbers at each idle stop, from group 006**: the intake
air temperature and the altitude correction factor. Neither moves quickly
enough to need logging, and together they turn the volumetric-efficiency
estimate in `engine-health.md` from a range into a figure. **Two numbers on
paper, three times.**

⚠ **A log of zeroes is evidence and not proof.** The misfire counter is a
*current* count rather than a total — values of 5 to 17 were watched rising and
falling — so at 1.7 samples a second a brief event falls between samples. An
hour is about six thousand samples, which is a strong statistical argument and
still not the same thing as none having happened. **The static read below is
the one where the screen is watched continuously**, and it is not replaced by
the log.

**The two recordings do not need to be synchronised.** Engine speed appears in
both, so every VCDS sample can be matched to the right stretch of capture by
its rpm alone — the method `docs/vcds-session.md` established and the reason it
keeps that rig described. Nothing has to line up in time.

---

## The drive

**Start the capture at a cold or cool start** and leave it running. Drive
normally for **forty-five minutes to an hour**, and deliberately include:

⚠ **The start itself now has a before-picture, so do not miss the after.**
`18_coldstart_z1.txt` holds one cold start on the old injectors, with VCDS
groups 014 and 055 beside it; the numbers to be beaten are in
`docs/engine-health.md`, *The cold start*. Start the bus capture and the
diagnostic log **before the key**, and **check the diagnostic log is still
running once the engine catches** — on the recording that exists, VCDS lost the
ECU during cranking and the start has no diagnostic data beside it.

- **Several stationary idles of three to five minutes each**, spread through
  the warm-up — one early, one in the middle, one when thoroughly hot. These
  are the stumble data, and they are what makes the oil-temperature curve.
- **Two or three full-throttle pulls in a HIGH gear from about 2400 rpm** —
  fourth or fifth, or up a hill, anywhere the engine *sits* near peak torque
  instead of flashing through it. **This is what the last drive got wrong**:
  every pull was a low-gear sweep that crossed 2400 in a moment, so there was
  essentially no full-throttle data below 3000 rpm.
- **One low-gear pull to high revs**, as before, for the power end.

**Nothing needs marking and no times need noting.** The capture carries road
speed, engine speed and throttle, so the idles and the pulls can be found in it
afterwards. Drive; the analysis does the sorting.

**If the oil temperature stops climbing and you want question 7 closed
outright**, add the free-revving holds in neutral from `can-decoding.md`
question 7 at the end, while it is still hot.

⚠ **They will display nothing, and there is no display fitted anyway.** The
holds are read off the raw log and b7, which is what they always were.

---

## Straight after, with the engine still idling

**Stop the capture first**, then read these on the VCDS screen and photograph
them. They are single values, not logs.

1. **Group 014 — misfires.** `Rozpoznani` must read **`aktivováno`** — that is
   the word the label file produces, not `aktiv.`; if it says `deaktiv.` the
   engine is not running and the number beside it is meaningless. **The counter
   is a current count and not a total**, whatever the label says, so read it
   while idling rather than expecting a sum. Before the work it took the values
   **0, 12, 13, 24 and 36 and nothing else**, held each for about three seconds
   and returned to zero, on an engine idling from cold — against a label file
   that specifies 0 to 5.
2. **Group 032 — the lambda adaptations.** They were **−4.7 % at idle against
   +1.6 % at part load** before the work. Moving toward zero at idle is the
   single cleanest sign that the injectors were the fault.
3. **Groups 022 and 023 — knock retard, per cylinder.** Specified 0.0 to
   15.0 °CA each. **This is the only per-cylinder signal this ECU offers** —
   there is no per-cylinder misfire counter — so a cylinder retarded further
   than its neighbours names itself. Worth a look after the pulls rather than
   at idle, where nothing knocks.
4. **Group 055 — the idle regulator**, specified −2.00 to +2.00 g/s, with its
   own adaptation beside it at −1.50 to +0.150 g/s, and group 056 for the
   target idle speed of 780 rpm. **Both now have a before-reading**, taken over
   five minutes of cold idle in `vcds/vcds-coldstart-014-055.csv`: the
   regulator worked between **−0.63 and +0.01 g/s**, mean −0.31, and the
   adaptation sat at **−0.73 g/s and never moved** — an adaptation is stored,
   so a single run cannot shift it and only the next reading can show whether
   it has. Both are inside tolerance; what matters is which way they go.
5. **Group 070 — the evaporative valve**, duty 0 to 100 % and flow 0.00 to
   0.33 g/s. ⚠ It is a *basic setting* block rather than a passive read, so
   expect it to run a test rather than report a state. If the purge is shut
   while the engine stumbles, the alternative explanation for the idle is out.
6. **Group 100 — readiness and OBD status**, which is what says whether the
   new converter has finished its monitors and emissions can be measured.
7. **The fault memory.** Do not clear it, before or after.
8. **Then start the capture again and settle 0x200, which costs two minutes.**
   With the engine still idling and a capture running, **disconnect VCDS from
   the ECU and reconnect it.** `18_coldstart_z1.txt` is the only log carrying
   identifier 0x200, twice, and both times it fell in the window where VCDS had
   dropped the ECU and was being reconnected by hand — while `11`–`17` hold
   half an hour of bus with VCDS merely *attached* and never show it. **If
   0x200 appears, it is the tester and not the car**, and the same goes for the
   only two frames in the whole corpus where `0x5D0` byte 0 is not zero, each
   of which follows a 0x200 within 90 ms. `docs/can-decoding.md` has the
   argument. Nothing depends on the answer — it is cheap and the alternative is
   leaving a fifteenth identifier on the bus unexplained.

---

## What comes back here

| | |
|---|---|
| the capture | filtered to `0x280`, `0x420` and `0x1A0` before sending — about a fifth of the size and nothing this analysis needs is outside those three |
| the VCDS log | as it comes — groups 003 and 014 |
| groups 014 and 032 | photographs are fine |
| how it drives | not a soft measure here, see the prediction below |

**Size.** The whole bus runs about **one megabyte a minute**, so an hour is
roughly 60 MB — fine to write, awkward to hand over, which is what the filter
is for. `tools/usbtin_capture.py` writes line by line as it goes, so a capture
that is interrupted keeps everything up to the interruption.

---

## The prediction, written before the drive so it can be wrong

**If the injectors were the fault:** the car pulls better, the first-gear
misfires go to zero, the idle stumbling disappears **at every oil temperature
rather than only when hot**, and the idle adaptation moves toward zero — while
**load stays near 78 % and the torque the display would compute stays near
117 Nm**.

⚠ **That last clause rests on an unsourced premise and is the weakest thing in
this document.** It assumes the ECU's torque model cannot see a fuelling fault,
which needs the lambda entering that model to be the *commanded* value — and
nothing this project holds says so. `frames.md` sorts what is founded from what
is recalled. **Misfire detection is per-cylinder and does run on this car**, so
the ECU is not without a combustion signal; whether it reaches the torque model
is simply unknown.

Which makes it the most informative line here rather than the least: **if b7
rises while load and airflow stay put, the premise is wrong and we learn
something no other measurement on this drive can give.**

**On the idle specifically**, `engine-health.md` measures the stumbles as
present at 61 °C of oil and absent at 73 °C, with the coolant at 99 °C in both.
**A repair that removes them only in the hot state has not removed the cause.**

---

## After the reflash — the one check that costs nothing

**The loop this drive starts ends with a reflash**: the capture gives the
numbers, `TORQUE_CNM_PER_BIT` and the drag line move together if the tree below
says they should, the hex is rebuilt and programmed, and then the display is
looked at to see whether it now reaches the factory figures.

**Put `TorqRaw` on the same page as `Torque` and `RPM` for that look, and
photograph one steady moment.** That is the whole of it. No session, no
instruments, nothing dismantled — both channels are already on the display in
the normal fitted configuration, one from `0x601` and one straight off the
car's `0x280`.

**It is worth the one photograph because it closes a gap nothing else can.**
The host tests check the core under gcc; the device runs XC8 over the
hand-written wide arithmetic in `fastmul.h` and `divconst.h`. *Compiling proves
nothing about the silicon*, and a green host test is evidence about the code
and a **hypothesis about the device** — which is this repository's own rule,
one level up. A single frame showing b7, engine speed and the torque computed
from them is the only thing that has ever tested the arithmetic **as the part
actually executes it**.

⚠ **Set the scale before reaching for `TORQUE_TRIM_PCT`, not at the same
time.** The remap gain belongs inside the scale's derivation with its
assumption written down; adding a few per cent on top of a scale that is itself
being changed leaves two unknown corrections on one number and no way to tell
which is doing what. Get the scale from the measurement, look at where it
lands, and only then decide whether a trim is wanted at all.

---

## What happens after the reading — the decision tree

**Step 1 is the engine, because otherwise you are calibrating against a sick
one.** Does it pull better with the new injectors? If not, today's numbers were
already its best and you go to step 2 with them; if it does, re-measure and go
to step 2 with the new ones.

**Step 2 is b7's maximum at full throttle**, taken out of the capture, with
the ECU's load from the same engine speed beside it. (With the dashboard
closed, `TorqRaw` on the display is the same byte as a held maximum and the
same tree applies.)

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

- **It does not refit the drag line, and may make that unnecessary.** The
  refit was wanted for 95–110 °C oil; this engine appears not to go there. See
  question 7 above and `can-decoding.md`.
- **It does not measure torque.** Nothing here is a dynamometer. It measures
  the ECU's own byte and how close that byte gets to its ceiling.
- **It does not need the converter reflashed.** Nothing in `src/` changed.
  `TORQUE_TRIM_PCT` stays at zero until there is a measurement to set it from.
- **It does not check the converter**, and nothing separate needs to: see
  *After the reflash*.
