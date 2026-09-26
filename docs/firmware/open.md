# Firmware — open questions

**The questions about what this firmware reads and transmits that are still
open**, each with what is known, what it costs while it stays open, and the
measurement that closes it. The numbers are the ones `can-decoding.md` has
always used, because code and documents cite them; the answered ones are in
`can-decoding.md` under *Resolved questions*, and the ones not worth answering
under *Never resolved but not required*.

**Both of these may stay open for good, and that is allowed.** Neither blocks
anything: the firmware ships a defensible value for each, errs in a known
direction, and nothing in `src/` changes until a measurement says so.

**10 sits under 7.** The drag line of question 7 is fitted against oil
temperature, so if question 10 finds the oil channel wrong, question 7 is being
asked in the wrong units — and may simply be answered.

The engine's own faults are not here; they are `docs/engine-health/open.md`.

---

## 10. Is the oil temperature right, and not merely oil?

**Question 4 settled *what* 0x420 b3 is. Nothing has settled what it is
worth.** The formula `× 0.75 − 48` was borrowed from the coolant on 0x288 by
analogy, and the two bytes come from different modules: the coolant from the
engine ECU, the oil from the instrument cluster, which the sender is wired to.

**Who reads it.** `st.oil_c100` is decoded and consumed by nothing in this
firmware, so being wrong costs the firmware nothing. The display shows
`OilTemp` straight off 0x420 through `mfd15`. And the engine investigation
leans on it: the idle fault depends on oil temperature, and every
`IdleHealth` reading is compared at a matched one.

### What makes it worth asking

The channel never gets hot and never closes on the coolant:

| state | oil | coolant |
|---|---|---|
| warm idle, `11` `12` | 72.8, 73.5 °C | 99.0 °C |
| 2926 rpm held, `16` | 77.25 °C | 99.0 °C |
| six minutes' driving, `17` | 77.25 °C | 100.5 °C |
| 56 minutes' hard driving, `19` | **75.75 °C peak** | — |
| two hours of motorway, 19/9, off the display | **≤ 74 °C** | — |

*General*: a warm engine under load runs its oil at 90–110 °C, above the
coolant rather than 25 °C below it. A thermostat stuck open is ruled out: the
coolant warms up to 99–100.5 °C like a healthy engine's.

### Two readings, and the evidence for each

**The shipped slope, `× 0.75 − 48`, is right and this oil really runs cool.**
The strongest evidence yet is the cool-down after the post-repair drive
(`21`–`23_oilcool_*`): an IR thermometer on the oil filter read 48.8, 47.3 and
44.0 °C while the shipped scale read 45.75, 44.6 and 43.1 — within 1–3 °C and
falling alongside it; the sump pan read about 38 °C. The cold end agrees too:
raw 77 after a 19-hour soak is 9.75 °C, against a filter at 10.7 and ambient
10.0. Whether this engine has an oil-to-water heat exchanger, and where the
sender sits, would explain a cool sump; nobody has looked.

**The slope is wrong, and `°C = raw − 64` is closer.** The only argument is
that the gap to the coolant grows with temperature — 3.75 °C at a cold soak,
20–26 °C warm — which is what a slope error looks like. Under `raw − 64` every
warm fixture sits within ±6 °C of the coolant. ⚠ But that fit assumes the oil
ends up near the coolant, which is exactly what is in question. **The
cool-down points above argue against it**: the steeper slope needs the oil
15–20 °C hotter than both the filter and the pan it sits in.

*Physics alone does not decide*: from a soak at ambient to a warm engine, the
coolant's slope is pinned at 0.57–0.89 (0.75 inside it), but the oil's is
0.76–1.16 only if one assumes where the oil ends up. Both 0.75 and 1.00
survive.

### How it closes

1. **A thermometer in hot oil, straight after a hard drive**, against
   `OilTemp` on the display at the same moment. **The question is 77 against
   103 °C**, a 26 °C gap, so it does not need to be precise — but it needs to
   read the oil:
   - **best: a K-type thermocouple down the dipstick tube** into the oil. Cheap,
     no emissivity to get wrong, and the sump is where the sender is;
   - acceptable: an IR thermometer **rated past 100 °C** (the one used so far
     stops at 60) on the sump pan from underneath and on the filter. Not
     through the filler cap — that is the valve gear.
2. **Two cold soaks at different ambients**, no thermometer at all. On a
   cold-soaked car both channels read the same temperature, so the ratio of
   their changes is the ratio of their slopes. 25 °C between the soaks moves
   the coolant 33 counts; it moves the oil **33 counts at slope 0.75 and 25 at
   1.00**, far outside quantisation. `18_coldstart_z1` is soak one (coolant raw
   86, oil raw 81); soak two is twenty seconds of ignition-on on a morning
   meaningfully colder, e.g. in winter.

   **The soaks so far**, on the shipped scale:

   | soak | coolant | oil | oil − coolant |
   |---|---|---|---|
   | `18_coldstart_z1`, 11/9, ~10 h | 16.5 °C (raw 86) | 12.75 °C (raw 81) | −3.75 |
   | `19_postfix_drive_z1`, 24/9, ~19 h, ambient 10.0 °C | 12.0 °C (raw 80) | 9.75 °C (raw 77) | −2.25 |
   | 26/9, ~10 h, cold fog; *owner-reported off the display, whole degrees* | 14 °C | 11 °C | ≈ −3 |

   **Consistent, and not yet decisive.** The oil sits 2–4 °C below the
   coolant at every soak, so the offset at the cold end holds up. But the three
   soaks span only ~4.5 °C of coolant — about 6 counts, where telling the
   slopes apart needs ~25 °C. The winter morning is still what closes it,
   ideally read off a capture (raw bytes) rather than the display's rounded
   degrees.
3. **VCDS cannot do it**: this ECU has no oil temperature in any block
   (`docs/engine-health/vcds.md`). Do not spend a session looking.

**When it closes:** if the shipped scale is confirmed, write it down and
close 10. If `raw − 64` (or anything else) is confirmed, the fix lands in
`decode.c` and in `mfd15/tri/S-AQY.TRI` in the same breath, and question 7
very likely closes with it (below). Until then, nothing changes.

---

## 7. The drag line on hot oil

**What the firmware ships.** A least-squares line through the four warm
free-revving holds `13`–`16`, stationary in neutral where b7 *is* the drag:

| hold | rpm | b7 | oil (shipped scale) |
|---|---|---|---|
| `13_rev1500_z1` | 1536 | 18.81 | 72.8 °C |
| `14_rev1850_z1` | 1850 | 20.66 | 74.2 °C |
| `15_rev2372_z1` | 2372 | 26.32 | 75.3 °C |
| `16_rev2926_z1` | 2926 | 27.23 | 76.6 °C |

```
drag_b7   = 9.11 + 0.006514 x rpm        residuals -0.9 to +1.8 counts
drag [Nm] = 9.66 + 0.00690  x rpm        at 1.06 Nm/bit
```

It replaced a cold-oil line (39–61 °C) that overstated drag by 4 counts at
idle and 10 at 2930 rpm, and took the share of `17_drive_property_z1` showing
a torque from 49 % to 78 %. The idle point is excluded and covered by the
driving gate instead (`frames.md`).

**Why it is open.** 72–77 °C is warm but not the 95–110 °C of real driving,
so the line probably still overstates drag a little — the conservative
direction: the display shows slightly *less* than the truth.

**What that costs, bounded.** From the cold and warm pairs, drag falls about
0.27 counts per °C at 2930 rpm; extrapolated linearly to 100 °C that is 6.2
counts, about 4.6 Nm — an **upper bound**, since viscosity falls
exponentially and not all drag is viscous. Because `TORQUE_CNM_PER_BIT` is
derived *through* the drag line, a lower line also lowers the scale (to about
1.02), and at high b7 the two cancel:

| at 4799 rpm | now | with a hot refit | |
|---|---|---|---|
| b7 = 185, the peak of `17` | 153.3 Nm | 153.4 Nm | **+0.1 %** |
| b7 = 100 | 63.2 Nm | 66.9 Nm | +6 % |
| b7 = 60 | 20.8 Nm | 26.3 Nm | +26 % |
| b7 = 40 | zero | 5.9 Nm | — |

So the error is **a roughly constant few Nm, invisible at full throttle and
dominant at part throttle.** The maxima — which is what is read on this car —
are pinned by the factory ratings whatever the oil is doing.

**It may never be worth closing, and that is the maintainer's decision.**
Under 1 % where the numbers are read; the input is the ECU's own modelled
torque on a scale read off one day's plateau; and the cost is a dismantled
dashboard. **If a part-throttle number ever starts to matter, that argument
expires.**

### How it closes

1. **Question 10 first.** If the oil scale is `raw − 64`, the four holds were
   at 98–103 °C — real operating temperature — and the line is already fitted
   where the engine runs. **Question 7 closes with no drive at all.** Do not
   plan a session around heating the oil before 10 is settled.
2. **If 10 confirms the shipped scale**, the oil on this engine peaks at about
   75–77 °C even after 56 minutes of hard driving (`19`) — which is again
   where the line is fitted. Then too there is nothing to refit, and 7 closes
   as "fitted where it runs".
3. **Only if the oil turns out to run hotter than the holds** is a refit
   owed: the rpm sweep in neutral with the oil genuinely hot, holding each
   speed until 0x420 b3 stops climbing, with several points below 1500 rpm to
   see whether the fall from idle is a curve. Connect the USBtin behind the
   display *before* the drive — the oil cools while the dashboard comes
   apart (`install.md` step 11). The holds display zero torque by design; the
   refit is done off the raw log.

**When it moves, `TORQUE_CNM_PER_BIT` moves with it** — one calibration,
never one half alone (`config.h`, `frames.md`).
