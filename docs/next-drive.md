# The next drive — one session, in order

**This is the procedure for the first drive after the injectors, spark plugs,
ignition leads and silencers are fitted.** One session, one configuration, one
capture. Allow **an hour and a half**.

**The document is in two halves and they are meant to be used differently.**

- **[Part 1](#part-1--the-session-step-by-step) is the procedure.** Follow it
  in the car without deciding anything. It says what to do and in what order,
  and nothing else.
- **[Part 2](#part-2--why-each-step-is-there-and-how-to-read-what-comes-back)
  is why**, and how to read what comes back. Read it before, or afterwards
  with the results in hand. **Nothing in it is needed while driving.**

**Nothing happens before the parts are on.** The car stands until then, because
a new catalytic converter behind a cylinder still dumping raw fuel is the same
converter that was cut open. There will be no clean before/after for most of
this and that is accepted; the fixtures already hold the "before" for the
measurements that matter.

---

# Part 1 — the session, step by step

## Before the day

**1. Do not clear the fault memory. Do not disconnect the battery. Do not reset
adaptations.** Not before, not after, not at the garage. If the garage offers,
decline.

**2. Do not do this the day the car comes back.** Drive it home and leave it.
The drive home is wanted; see Part 2.

**3. Plan the start for about ten hours after the engine last ran.** Overnight
is right. **Do not deliberately make it longer.**

**4. Take the display and the converter out**, and put the USBtin on that pair.
They cannot share it — the converter is powered from the display, so removing
one removes both.

## In the car, before the key

**5. Connect VCDS to the OBD socket and the USBtin to the display's pair.**
Both at once is fine.

**6. Read group 006 and write two numbers on paper:** intake air temperature
and the altitude correction factor.

**7. Start the capture:**

```
python tools/usbtin_capture.py --seconds 3600 --out postfix_z1.txt
```

**8. Start VCDS logging, groups 003 and 014. Two groups, never three.**

**9. From here until step 17, do not touch the VCDS screen.** Changing the
group selection is what the log records; switching to another block ends the
recording.

## The start

**10. Start the engine the way you normally start it.** Do not cycle the key to
prime the pump — unless that is your normal habit, in which case do it.

**11. As soon as it catches, check the VCDS log is still counting samples.** If
it has stopped, restart it immediately. Keep glancing at it.

## The drive — 45 to 60 minutes

**12. Three stationary idles of three to five minutes each**, spread through
the warm-up: **one early, one in the middle, one when thoroughly hot.** Engine
running, in neutral, nothing touched, air conditioning off.

**13. Two or three full-throttle pulls in a HIGH gear from about 2400 rpm** —
fourth or fifth, or up a hill. Somewhere the engine *sits* near peak torque
rather than flashing through it.

**14. One low-gear pull to high revs.**

**15. Nothing needs marking and no times need noting.** Drive; the analysis
finds the idles and the pulls by itself.

**16. Finish at a standstill with the engine idling and hot.** Do not switch
off.

## Straight after — engine idling, hot

**17. Stop the capture, then stop the VCDS log.** Both. Only now may the group
selection be touched.

**18. Read these and photograph each screen:**

| group | what to read |
|---|---|
| **014** | the misfire count — watch it for a minute rather than glancing |
| **032** | both lambda adaptations |
| **055** and **056** | idle regulator, its adaptation, target idle speed |
| **100** | readiness bits and OBD status |
| **006** | intake air temperature and altitude factor, the second time |

**19. Now the basic settings. This is how one is run** — it is not *Akční
členy*, which is the other function:

- in **`Měřené hodnoty`**, press **`Přepnout na základní nastavení`**
  (bottom left), **or** use `ZÁKLADNÍ NASTAVENÍ` from the controller window
- enter the group number, press **START**
- **each block shows its own entry conditions as its first fields.** Hold the
  engine where those fields ask, watch them come into range, then read the
  result field
- stationary, **in neutral, handbrake on**; the throttle is a foot, so both
  hands stay free

**20. Run group 046.** Hold the engine speed its own field asks for. Read and
photograph the result.

**21. The same for group 034.**

**22. The same for group 037.**

**23. The same for group 070.** Expect this one to operate a valve.

**24. Read group 036** — an ordinary read, not a basic setting.

## The last capture — one recording covers the last two steps

**25. Engine still idling, VCDS still connected. Start a capture:**

```
python tools/usbtin_capture.py --seconds 420 --out final_z1.txt
```

**26. While it runs, disconnect VCDS from the ECU and reconnect it.** Engine
running, bonnet shut, nothing else touched.

**27. Switch the engine off but LEAVE THE IGNITION ON**, and **leave the
capture running.** The bus stays alive with the ignition on, which is the whole
point of this step.

**28. Put a thermometer down the dipstick tube.** Note the reading and the
clock time to the second. Take your time — the capture is recording the car's
own oil channel while you do it, and the two are compared afterwards.

**29. Stop the capture. Ignition off. Do not clear the fault memory.**

## Some hundreds of kilometres later

**30. Read group 032 again** and photograph it. One screen, no session, no
instruments. This one matters and is easy to forget.

## What comes back

| | |
|---|---|
| the capture | filtered to `0x280`, `0x1A0`, `0x420` and `0x480` before sending |
| `final_z1.txt` | whole, it is small — it carries the 0x200 test and the oil reading |
| the VCDS log | as it comes, groups 003 and 014 |
| the photographs | every screen from steps 18 and 20–24 |
| two paper numbers, twice | group 006, before and after |
| the dipstick reading | with the clock time |
| how it drives | in plain words |
| later | the second group 032 photograph |

---

# Part 2 — why each step is there, and how to read what comes back

## Steps 1–3 — why nothing is cleared, and why not on day one

**The lambda adaptations are the measurement, so clearing them destroys it.**
`032` reads **−4.7 % at idle against +1.6 % at part load**, and *moving toward
zero at idle* is the single cleanest sign that the injectors were the fault.
Clear the adaptations and the after-value starts at zero because it was forced
there, not because anything was repaired. The same argument covers the battery:
disconnecting it takes the idle adaptation (`055`, **−0.73 g/s**), the throttle
body adaptation and the readiness bits with it.

**The fault memory is evidence** and a cleared one also resets readiness, so
`100` would read "not complete" and say nothing about the new converter.

⚠ **How long the ECU needs to re-adapt to new injectors is not known here.** It
was asserted in conversation once as "weeks" and never written down or sourced,
so it is treated as unknown. **The procedure is built not to depend on it**:
nothing is cleared, the session is not delayed waiting for adaptation, and
`032` is simply read a second time later (step 30). The *movement* between the
two readings is the evidence, and that works whatever the time constant is.

**Why the day off, and why the drive home is wanted rather than tolerated
(step 2).** Two separate reasons, and the second is the stronger one.

**The first start after the injectors are fitted is not comparable to
anything.** The fuel rail was opened to change them, so it has air in it and
that start will crank long for a reason that is not the engine's health. **The
garage does that start**, and by the time the measured one happens it is the
third or fourth — which is what makes it a measurement rather than an artefact.

**The second is the stored adaptation.** From a cold start the ECU runs open
loop until the oxygen sensor lights off, and in open loop it uses the *stored*
adaptation rather than a live one. New injectors with a stale −4.7 % in memory
therefore carry that error straight into the warm-up.

⚠ **Closed-loop control does not protect the measured cold start**, and this is
the point worth being clear about: it corrects the mixture within seconds once
the sensor is live, which covers the warm idles and the pulls and covers
nothing at all about the first minute from cold. **The drive home, plus
whatever running the garage does, is the only thing that moves that stored
number before the measurement.** Seven kilometres is roughly ten minutes of
closed-loop running.

**But the confound is bounded, and smaller than an earlier version of this file
implied.** The adaptation is multiplicative, and cold start is *deliberately*
rich by far more than 4.7 %:

| | µl/s | against warm idle |
|---|---|---|
| measured, first 30 s from cold | **927** | **2.84×** |
| the same with a stale −4.7 % still applied | 883 | 2.71× |
| warm idle, `09_idle_60s_z1` | 326 | 1× |

**A mixture that was meant to be 2.84× and comes out 2.71× is still a cold-start
mixture.** So the drive home is worth having and is not worth engineering:
taking a longer route buys an unknown amount of an unknown quantity, while the
design already does not depend on convergence — that is what the second `032`
reading in step 30 is for.

**Why ten hours and not longer (step 3).** The before-recording,
`18_coldstart_z1.txt`, was taken about ten hours after the previous start.
**Matching it is worth more than making the test harsher.** A harsher after-run
that passes is nice; a harsher one that fails cannot be told apart from a
longer stand, and the clean before/after is the whole value.

## Steps 4–9 — the configuration, and the one screen rule

**The display and converter come out** because a capture carries b7, engine
speed, oil temperature, road speed, throttle and the fuel counter at about
ninety-four frames a second each, every one with the others beside it in time.
A display channel would be the same byte reduced to a held maximum.

⚠ **`OilTemp` is not the converter's.** Its TRI row reads `0x420` byte 3, the
car's own frame, so every capture already carries it.

**Groups 003 and 014, and not 010.** `014` already carries the load, so
`003 + 014` is a superset of `003 + 010` with the misfire counter added and
nothing given up — logging misfires costs no sampling rate at all. A third
group would drop the rate from about 1.7 samples a second to 1.1, and **the
rate is the one thing that cannot be recovered afterwards.**

**Mass air flow and engine load are the point of the second instrument** —
neither is on the CAN bus, so only VCDS can give them.

**Group 006 is read twice and never during the drive**, because reading it
means changing the group selection and that ends the log. The cold reading is
essentially ambient, the hot standing one is ambient plus engine bay — today's
cold start gave 22.5 °C standing with the oil starting at 12.75 °C — so the
pair **brackets** what the engine breathed during a pull. The
volumetric-efficiency table in `engine-health.md` wants a bound and gets a
narrower one.

**The two recordings do not need to be synchronised.** Engine speed appears in
both, so every VCDS sample matches to the right stretch of capture by its rpm
alone.

## Steps 10–11 — the start

**There is a before-picture and it is the one thing that cannot be repeated.**
`18_coldstart_z1.txt` holds one cold start on the old injectors:

| | |
|---|---|
| cranking | **1.24 s** at about 235 rpm |
| first firing | 451 rpm |
| then | **falls back to 311 rpm and nearly stalls** |
| running | 43.00 s, then a flare to 1446 rpm |

**A prime masks exactly that symptom**, which is why step 10 says not to — with
the qualification that the before-recording was taken with whatever the usual
start is, so "usual" wins over "clean".

**Step 11 exists because VCDS lost the ECU during cranking last time** and did
not recover by itself, which cost the whole start and the first 86 seconds of
running — the one thing the session was asked for.

## Steps 12–14 — why the idles are spread out

⚠ **A hot idle alone would waste the trip.** A hot idle counted **zero before
the repair** — `11_idle_noac_z1` and `12_idle_ac_z1`, old injectors, 73 °C — so
zero afterwards says nothing whatever.

| state | oil | before, `dips_cheap()` | predicted after |
|---|---|---|---|
| cold idle | 13–17 °C | **12.1/min** | ~0 |
| warm-ish idle | 61.5 °C | **11.6/min** | ~0 |
| hot idle | 72.8–73.5 °C | 0.0/min | 0, and it says nothing |

**One minute at a matched temperature settles "gone or not gone"** — at 11.6 a
minute, seeing none in sixty seconds has a probability of 7×10⁻⁵ if nothing
changed. **Three minutes also settles "how much better"**, at p = 0.002 for a
halving. The whole analysis is `python tools/idledips.py CAPTURE`; no firmware
change and no display channel is involved.

**High gear for the pulls** because the last drive got this wrong: every pull
was a low-gear sweep that crossed 2400 rpm in a moment, so there was
essentially no full-throttle data below 3000 rpm.

**If the oil stops climbing and you want `can-decoding.md` question 7 closed
outright**, add the free-revving holds from that question at the end while it
is hot. They will display nothing, and there is no display fitted anyway — the
holds are read off the raw log and b7.

## Step 18 — what each screen is for

**`014` — misfires.** `Rozpoznani` must read **`aktivováno`**; `deaktiv.` means
the engine is not running and the number beside it is meaningless. **It is a
current count, not a total.** Before the work it took the values **0, 12, 13,
24 and 36 and nothing else**, held each about three seconds and returned to
zero — against a label file that specifies 0 to 5.

⚠ **A log of zeroes is evidence and not proof.** At 1.7 samples a second a
brief event falls between samples. An hour is about six thousand samples, which
is a strong statistical argument and still not the same as none having
happened. **This screen is the one where it is watched continuously**, which is
why a minute of watching is asked for rather than a glance.

**`032` — the lambda adaptations**, and see steps 19–24 below for the fork that
decides what they mean.

**`055`/`056` — the idle regulator.** Specified −2.00 to +2.00 g/s, its
adaptation −1.50 to +0.150 g/s, target idle 780 rpm. The before-reading, over
five minutes of cold idle: the regulator worked between **−0.63 and +0.01 g/s**,
mean −0.31, and the adaptation sat at **−0.73 g/s and never moved**. An
adaptation is stored, so one run cannot shift it; only the next reading shows
whether it has.

**`100` — readiness and OBD status.** Reading `00000000` says every monitor has
completed. **Completed is not passed**, which is why step 20 exists.

## Steps 19–24 — the four blocks that give verdicts

**These are the only measurements here that need no baseline**, which is what
makes them valuable on a car whose "before" can no longer be produced.

| block | checks | the answer |
|---|---|---|
| **046** | catalytic converter conversion | `CatConvB1 OK` / `not OK` |
| **034** | pre-cat oxygen sensor ageing | `B1-S1 OK` / `not OK` |
| **037** | post-cat sensor, basic setting | `Sys. OK` / `not OK` |
| **036** | post-cat sensor availability | `B1-S2 OK` / `not OK` |

**Both oxygen sensors on this car have already been replaced once**, so **any**
`not OK` is a second failure of that sensor — which argues for something that
keeps killing them rather than for a worn part. Both have also sat in the
exhaust of a converter that was burning through.

**That is what makes `032` mean something**, and the fork is clean:

| 034 / 036 / 037 | what −4.7 % at idle then means |
|---|---|
| all `OK` | the ECU is correcting a **real** fuel excess — the injectors |
| any `not OK` | a second sensor has failed; the adaptation may be its artefact, and `032` is re-read after it is replaced |

**The converter temperature these blocks display is a gate, not a reading.**
There is no need to know what a healthy catalyst temperature is: the number is
an entry condition and the ECU supplies the judgement. That is also why step 19
says to watch the block's own fields rather than quoting rpm ranges here — the
block knows them.

**`070` operates the evaporative valve.** If the purge is shut while the engine
stumbles, the alternative explanation for the idle is out.

⚠ **`022` and `023` — knock retard per cylinder — are deliberately not in this
session.** They are the only per-cylinder signal this ECU offers, but they are
a live value under load: at idle after a drive nothing is knocking and they
read what a quiet engine reads. Catching them needs a third logged group, a
broken log, or a passenger. **Their own session, with somebody else holding the
laptop.**

## Steps 27–28 — the thermometer, and why the ignition stays on

**`can-decoding.md` question 10 is whether the oil temperature is *right*, not
merely oil.** The channel never exceeds 77 °C and sits twenty-odd degrees
*below* the coolant in every state ever recorded, including an hour of driving
that peaked at 72–74 °C. A warmed engine under load normally runs its oil at
90–110 °C and above the coolant.

⚠ **No screen can settle this.** `01-Motor` has no oil temperature block at
all — every temperature it defines is coolant, intake air or catalytic
converter. The thermometer is the only test there is, and it matters because
the drag line question 7 is still open about is fitted against that number.

**The ignition stays on because that is what keeps the bus alive**, and the
oil channel with it: `08_ign_only_z1` holds a steady 51.75 °C for twenty
seconds with the engine stopped, and `18_coldstart_z1` reads 12.75 °C for the
whole 41 s before the engine fires. So `0x420` b3 is being recorded while the
thermometer is being read, and the two are compared on the clock afterwards.

⚠ **An earlier version of this file had the engine switched off before the
0x200 test and the thermometer reading taken then** — which killed the ignition
and with it both the bus and the VCDS connection, so the capture the
thermometer was supposed to be compared against had already stopped, and VCDS
had to be reconnected to do a test about reconnecting VCDS. One capture over
both steps, engine off but ignition on, costs nothing and works.

**The reading does not have to be taken at peak oil temperature**, which is
just as well, because by this point the engine has idled through all the
static reads. The question is whether the channel and a thermometer agree at
*one moment*, not what the highest number of the day was.

⚠ **Hot oil and an open bonnet.** The dipstick tube is not the exhaust, but
take the time the step allows rather than hurrying.

## Steps 25–26 — the 0x200 test

`18_coldstart_z1.txt` is the only log carrying identifier **0x200**, twice, and
both times it fell in the window where VCDS had dropped the ECU and was being
reconnected by hand — while `11`–`17` hold half an hour of bus with VCDS merely
*attached* and never show it. **If 0x200 appears, it is the tester and not the
car**, and the same goes for the only two frames in the whole corpus where
`0x5D0` byte 0 is not zero, each of which follows a 0x200 within 90 ms.

**With the engine running and VCDS already connected**, which is the state the
session ends in anyway — so this costs the seven minutes the capture runs and
no setting up at all. Nothing depends on the answer; the alternative is leaving
a fifteenth identifier on the bus unexplained.

## The capture filter

**Sizes measured on `18_coldstart_z1.txt` rather than estimated.** The whole
bus is **65 MB an hour**; the four identifiers kept are **36 % of the bytes,
about 24 MB an hour.** `usbtin_capture.py` writes line by line, so an
interrupted capture keeps everything up to the interruption.

⚠ **`0x480` is in that list and an earlier version of this file left it out**,
which would have thrown away the one thing the capture is still needed for.
Everything else can now be read off the display or the VCDS log; the **fuel
counter cannot**, and it is what removes the air-fuel assumption from the
efficiency argument in `engine-health.md` — measured air from group 003 over
the same pulls, divided by measured fuel. **Filter it out and the pulls have to
be driven again.**

**`0x288` is deliberately out**, and it is the only close call: the coolant
would take the filtered capture from 36 % to 48 %, nine more megabytes for a
channel that sat at 99 °C in all three warm idle fixtures while the thing being
measured moved. If the warm-up state itself ever becomes the question, take the
unfiltered capture.

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
nothing this project holds says so. **Misfire detection is per-cylinder and
does run on this car**, so the ECU is not without a combustion signal; whether
it reaches the torque model is simply unknown.

Which makes it the most informative line here rather than the least: **if b7
rises while load and airflow stay put, the premise is wrong and we learn
something no other measurement on this drive can give.**

**On the idle specifically**, a repair that removes the stumbles only in the
hot state has not removed the cause.

---

## After the reflash — the one check that costs nothing

**The loop this drive starts ends with a reflash**: the capture gives the
numbers, `TORQUE_CNM_PER_BIT` and the drag line move together if the tree below
says they should, the hex is rebuilt and programmed, and then the display is
looked at.

**Put `Torque`, `Power` and `RPM` on the same page and photograph one steady
moment.** All three are already on the display in the normal fitted
configuration, two from `0x601` and one straight off the car's `0x280`.

⚠ **There is no `TorqRaw` channel and none is wanted.** `S-AQY.TRI` carries 31
sensors and that is not one of them; it never was, in any commit of `mfd15`.
The raw byte is already in the capture at ninety-four samples a second, and
`mfd15/README.md` records that the display sometimes loses its sensor
definitions when a page's contents are changed. Editing a working configuration
for a convenience is a poor trade. If it is ever genuinely wanted it can be
appended then.

**It is worth the one photograph because it closes a gap nothing else can.**
The host tests check the core under gcc; the device runs XC8 over the
hand-written wide arithmetic in `fastmul.h` and `divconst.h`. *Compiling proves
nothing about the silicon*, and a green host test is evidence about the code
and a **hypothesis about the device**. A single frame showing b7, engine speed
and the torque computed from them is the only thing that has ever tested the
arithmetic **as the part actually executes it**.

⚠ **Set the scale before reaching for `TORQUE_TRIM_PCT`, not at the same
time.** Adding a few per cent on top of a scale that is itself being changed
leaves two unknown corrections on one number and no way to tell which is doing
what.

---

## What happens after the reading — the decision tree

**Step 1 is the engine, because otherwise you are calibrating against a sick
one.** Does it pull better with the new injectors? If not, today's numbers were
already its best and you go to step 2 with them; if it does, re-measure first.

**Step 2 is b7's maximum at full throttle**, taken out of the capture, with the
ECU's load from the same engine speed beside it.

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
   and `..._torque` assert what b7 = 255 produces. They would assert what the
   OBSERVED maximum produces — which is the first version of that test with a
   measurement behind it.
5. **`TORQUE_TRIM_PCT` is not the tool for this** and must not be used as one.
   A scale that is wrong is wrong for everybody who builds this firmware; the
   trim is one owner's gain on a correct scale. Fixing the first with the
   second leaves the next person a number that no longer means what its
   comment says.

---

## What this session answers

| question | what settles it |
|---|---|
| **is the engine well now** | first-gear misfires, the stumbling idle against oil temperature, the idle adaptation, how it pulls |
| **is the new converter converting** | block 046, and it needs no baseline |
| **are either of the replaced oxygen sensors gone again** | blocks 034, 036, 037 |
| **can the display ever show the factory maxima** | b7 at full throttle against the ECU's load at the same engine speed |
| **does the oil ever get hot enough to matter** | the oil temperature a long drive actually reaches, and the thermometer beside it |

**The last one is close to answered already.** The drive of 2026-09-10 peaked
at **72–74 °C of oil after about an hour**, and the warm holds the drag line is
fitted to are 72.8–76.6 °C — the same range. `can-decoding.md` question 7 rests
on "72–77 °C is warm, not the 95–110 °C of real driving", and that sentence
appears to be false for this engine. **Unless question 10 is the reason it
appears false**, which the thermometer settles.
