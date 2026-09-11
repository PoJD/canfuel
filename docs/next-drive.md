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

**The converter's own arithmetic is not checked on this trip.** `FuelNow`
against `FuelCntRaw`, `Torque` against `TorqRaw` — that wants the display
fitted, takes five minutes, needs nothing dismantled, and can happen any time
afterwards.

---

## What to run

**On the laptop, two things at once. They do not interfere** — the USBtin is on
the CAN pair and VCDS is on the OBD socket, over K-line
(`docs/vcds-session.md`).

**1. The capture**, listen-only, for the whole session:

```
python tools/usbtin_capture.py --seconds 3600 --out postfix_z1.txt
```

**2. VCDS logging, groups 003 and 010, running throughout.** Between them:
engine speed, **mass air flow**, **engine load**, throttle angle and ignition
advance. Those first two are the point — **neither is on the CAN bus**, so the
capture cannot get them and only VCDS can.

⚠ **Two groups, not three.** Three drops the sampling rate to about one per
second. Two gives about 1.7, which is plenty here for the reason below.

**The two recordings do not need to be synchronised.** Engine speed appears in
both, so every VCDS sample can be matched to the right stretch of capture by
its rpm alone — the method `docs/vcds-session.md` established and the reason it
keeps that rig described. Nothing has to line up in time.

---

## The drive

**Start the capture at a cold or cool start** and leave it running. Drive
normally for **forty-five minutes to an hour**, and deliberately include:

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

1. **Group 014 — misfires.** `Rozpoznani` must read **`aktiv.`**; if it says
   `deaktiv.` the engine is not running and the number beside it is
   meaningless. **The counter is a current count and not a total**, whatever
   the label says, so read it while idling rather than expecting a sum.
2. **Group 032 — the lambda adaptations.** They were **−4.7 % at idle against
   +1.6 % at part load** before the work. Moving toward zero at idle is the
   single cleanest sign that the injectors were the fault.
3. **The fault memory.** Do not clear it, before or after.

---

## What comes back here

| | |
|---|---|
| the capture | filtered to `0x280`, `0x420` and `0x1A0` before sending — about a fifth of the size and nothing this analysis needs is outside those three |
| the VCDS log | as it comes |
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
- **It does not check the converter.** That wants the display fitted and is a
  five-minute job with nothing dismantled, any time afterwards.
