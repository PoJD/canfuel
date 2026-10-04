# Firmware — open questions

**The questions about what this firmware reads and transmits that are still
open**, each with what is known, what it costs while it stays open, and the
measurement that closes it. The numbers are the ones `can-decoding.md` has
always used, because code and documents cite them; the answered ones are in
`can-decoding.md` under *Resolved questions*, and the ones not worth answering
under *Never resolved but not required*.

**7 and 10 may stay open for good, and that is allowed.** Neither blocks
anything: the firmware ships a defensible value for each, errs in a known
direction, and nothing in `src/` changes until a measurement says so.
**11 is a planned change**, decided by the owner and waiting on one more
set of data.

**10 sits under 7.** The drag line of question 7 is fitted against oil
temperature, so if question 10 finds the oil channel wrong, question 7 is being
asked in the wrong units — and may simply be answered.

The engine's own faults are not here; they are `docs/engine-health/open.md`.

---

## 11. `IdleHealth` does not follow VCDS group 014 — what should it measure?

*Raised by the owner, 4/10/2026.* After step 1b the ECU's misfire counter
(group 014) read zero at both warm stops for the first time, the owner
felt the calmest idle yet, and `IdleHealth` read about what it had read
the day before. The owner wants the grade **as close to how the ECU
measures as the bus allows**.

### What was measured

Every standing stop of 60 s and more, oil above 40 °C, in the four
captures that have a 014 log beside them, 014 aligned on engine speed
(the method of `docs/engine-health/open.md` S3). Candidate grades from
0x280, each over the whole stop:

| log | oil | 014 a minute | `IdleHealth` | dips a minute (`dips_cheap`) | one slow firing ≥ 6 / 8 / 12 rpm, a minute | mean second difference, rpm |
|---|---|---|---|---|---|---|
| `19` | 51 °C | 8.0 | 123 | 16.4 | 47 / 21 / 1.3 | 6.54 |
| `19` | 63 °C | 2.0 | 64 | 10.4 | 29 / 9.7 / 1.1 | 5.90 |
| `19` | 70 °C | 0.0 | 112 | 28.4 | 68 / 19 / 3.8 | 6.76 |
| `19` | 71 °C | 0.0 | 146 | 22.1 | 78 / 39 / 3.1 | 6.42 |
| `24` | 70 °C | 9.6 | 84 | 10.9 | 36 / 11 / 0.5 | 5.56 |
| 3/10 | 62 °C | 17.5 | 114 | 12.4 | 38 / 13 / 0.7 | 6.32 |
| 3/10 | 70 °C | 5.0 | 62 | 14.9 | 8.9 / 2.0 / 0.0 | 4.28 |
| 4/10 | 45 °C | 0.0 | 117 | 14.7 | 35 / 13 / 1.1 | 5.84 |
| 4/10 | 59 °C | 0.0 | 109 | 10.1 | 38 / 11 / 0.5 | 5.89 |
| 4/10 | 71 °C | 0.0 | **60** | **5.6** | 18 / 4.7 / 0.1 | 4.81 |
| 4/10, after a hard drive | 73 °C | 9.1 | 92 | 10.1 | 16 / 2.9 / 0.3 | 5.00 |
| 4/10, the MAF wiggle | 73 °C | 14.6 | 79 | 12.8 | 16 / 3.6 / 0.0 | 5.69 |

*One slow firing* is the shape a lone misfire leaves on crank speed: one
180° value below **both** its neighbours by at least the threshold — the
nearest thing on the bus to the ECU's per-cylinder segment times.
*Second difference* is |x₋₁ − 2x + x₊₁| over the same values. `24`'s
first stop has no 014 beside it and is left out.

**Rank correlation with 014** (Spearman, stops with detection active):

| grade | all 12 | new MAF only (`24`, 3/10, 4/10), 8 | hot only, 7 |
|---|---|---|---|
| `IdleHealth` | −0.12 | +0.05 | −0.22 |
| dips a minute | −0.09 | +0.27 | −0.30 |
| one slow firing ≥ 6 | −0.34 | −0.02 | −0.48 |
| one slow firing ≥ 8 | −0.24 | +0.12 | −0.48 |
| one slow firing ≥ 12 | −0.36 | −0.04 | −0.50 |
| second difference | −0.17 | +0.24 | −0.15 |

### What it says

- **No grade the bus allows follows 014** — not the current one, not a
  dip count, and not the shape-of-a-misfire detector built to imitate the
  ECU. Twelve stops is a small sample, but nothing is even close.
- **Why** (*reasoned*): the ECU times the crank per cylinder off its own
  sensor, against thresholds that move with load — which is why 014
  changed its ruler when the MAF did (`docs/engine-health/refuted.md`
  A11), and why `19` reads the roughest idle on record with 014 at zero.
  0x280 carries one recomputed speed per 180° (`can-decoding.md` trap 5);
  whatever the ECU sees in a single firing does not survive into it.
  **014 cannot be rebuilt from the bus**, and it is not on the bus.
- **What the grades do follow is the idle's smoothness — what the owner
  feels.** At the hot stop `IdleHealth` went 146 → 84 → 62 → **60** from
  `19` to 4/10 and the dip count 22 → 11 → 15 → **5.6**; 4/10's hot stop
  is the smoothest on record by both, which is what the owner felt. They
  also follow **oil temperature** more than anything else: the middle
  band reads 105–125 on most days.

### The variants, for the owner to choose from

1. **Keep `IdleHealth` and read it only on hot oil (≥ 66 °C)** — no
   firmware change: a rule for reading the display, written into
   `frames.md`. In that band it shows the trend above.
2. **Make it steadier.** The EWMA over 256 firings (9.7 s) lets two-minute
   windows of one stop read 56 to 109; `ROUGH_SHIFT` 10, about 40 s, would
   settle it. The level over a whole stop does not change, only its
   scatter.
3. **Add the dip count** (`tools/idledips.py` `dips_cheap()`, already the
   firmware's shape: shifts and adds, no division) as a second byte in
   0x604. It moved 4× at the hot stop where `IdleHealth` moved 2.4×, and
   "dips a minute" means something to a reader.
4. **Gate either grade on oil temperature in the firmware** — freeze it,
   or report 255, outside the hot band, so the display never shows a
   middle-band reading that compares with nothing.

**None of them is a misfire counter, and none can be.** For misfires,
VCDS 014 stays the instrument.

### Also due with the next change under `src/`

The `THROTTLE_REST` comment in `config.h` says b5 rests at 38; on the
throttle body fitted 2/10/2026 it rests at **35**, with nothing at 36–44
(`27`, `28`). The gate at 38 is in the empty gap for both parts and needs
no change; only the comment does.

### The decision, and the plan

*Owner's decision, 4/10/2026:* **variant 3, but as a replacement, not a
second byte** — `IdleHealth` becomes the dip count; no new metric is
added. Chosen over 1, 2 and 4 because it is the sharper reading of the
same smoothness and is legible as "dips a minute". **Not** chosen because
it follows 014: among the post-MAF stops it ranks closest (+0.27) but
weakly, and across days it does not track 014 at all (3/10's hot stop
14.9 dips with 014 at 5; `19`'s 22 with 014 at zero).

1. **Check it first against session B** (`docs/engine-health/plan.md`):
   the dip count over B's stops, with 014 beside them, added to the table
   above. Go ahead unless B shows it reading worse than `IdleHealth` on
   the same stops.
2. **Design, to be settled in the implementation:** 0x604's
   `IdleHealth` byte keeps its position and its 255 = not converged; its
   unit becomes **dips a minute over settled idle**, from `dips_cheap()`'s
   detector (trip 20 rpm, re-arm 10, the restartable 3 s settle). How the
   rate is carried — an EWMA of events against idle time, by shifts, or
   a count over a fixed idle window — is decided there, and costed in
   `docs/firmware/timing.md` like every other loop.
3. **`tools/idledips.py` is the oracle**, diffed exactly by
   `replay.py --host-build` as `IdleHealth` is today; `test_idledips.py`
   and the `_z1` fixtures carry the expected values.
4. **`mfd15` changes in the same breath** — the channel's name and unit in
   `S-AQY.TRI`, and `test_txframes.c`'s pinned offsets.
5. **XC8 installed and the `firmware` job's gates run locally** before the
   push (`CLAUDE.md`), with the `THROTTLE_REST` comment above corrected
   in the same change.

### How it closes

When the replacement is in `src/`, on the display, and B's stops agree
with the oracle; until then `IdleHealth` stays as it is.

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

   **The instrument: bought, 1/10/2026** (*owner*) — **Extol Premium
   `8831302`**, Hornbach article `10545469`, 569 Kč — the candidate named
   below. From **its own manual** (Extol's Czech user manual, read
   1/10/2026, not kept here): range **−50 to +550 °C**; accuracy **±1.5 °C
   above 25 °C**, ±3.0 °C from 0 to 25 °C; repeatability ±1 °C; emissivity
   **adjustable 0.10–1.00**, default 0.95; spot **12 : 1**; operated at
   **0–40 °C**, and **left 30 minutes to reach the ambient temperature**
   after a change of it. Set to **E 0.95** (owner's photograph). So it is
   enough: ±1.5 °C against a 23 °C gap. *The paragraph below, from 30/9,
   said no instrument had been bought.* **Taken in the engine-health
   test's session A as A4, after its last hot stop — no longer optional**
   (*owner's decision, 2/10/2026*; `docs/engine-health/plan.md`).

   *30/9/2026:* **The instrument: none yet** (*owner's decision, 30/9/2026*). A Bosch
   UniversalTemp was chosen on 29/9, not found in the shop and judged too
   dear for the job. The likely one now is an **Extol Premium 8831302**
   (EAN 8595126984171; the seller's listing, not a maker's manual: −50 to
   550 °C, ±1.5–3 °C with the band unstated, emissivity adjustable
   0.1–1.0, 12 : 1, operated at 0–40 °C) — enough against a 23 °C gap. It
   is **optional inside the engine-health test** (`docs/engine-health/plan.md`,
   A4), decided by the owner before the drive. What was worked out for
   the Bosch is kept as the checklist for whatever is bought — range past 100 °C, an emissivity setting of 0.95, the tape,
   the acclimatising, the coolant-hose check. Bosch's manual: range **−30 to +500 °C**; accuracy at 21 °C
   and emissivity 0.95 **±1.8 °C from 0 to 100 °C**, ±1.8 % above,
   worsening by 0.1 °C per kelvin the ambient is away from 21 °C;
   emissivity **fixed at three grades, ≈ 0.95 / 0.85 / 0.75**; spot
   **12 : 1**; operated at −5 to +50 °C, and **up to 30 minutes to
   acclimatise** after a change of temperature. So:

   - **it is enough, by a wide margin.** At a displayed 70 °C the two
     readings above are raw 157 — **70 against 93 °C**, a 23 °C gap
     against ±1.8 °C plus a few for the ambient; at `19`'s 75.75 °C peak
     it is 76 against 101;
   - **0.95, and only on a matt surface.** A painted filter can; bare or
     shiny metal (the manual names stainless steel) cannot, and the
     manual's answer is **dark matt tape on the spot** — stuck on before
     the drive, so that it is at the metal's temperature when read;
   - **it travels in the cabin**, not in a cold boot, so that it is not
     still acclimatising at the moment it is needed;
   - **a check of the instrument itself in the same minute**: the upper
     coolant hose (rubber, 0.95) against 0x288's coolant, which comes
     from the engine ECU and is not in question;
   - **what the surface reads is not the oil**, and errs one way: the
     filter and the pan lose heat to the air, so they read at or below
     the oil. So the two outcomes are not equally strong. **A filter well
     above the channel is decisive against the shipped scale** — the oil
     is hotter still. **A filter near the channel supports it** only as
     far as the filter tracks the oil, which the cool-down of `21`–`23`
     suggests it does (filter 1–3 °C above the channel, pan ~6–8 °C
     below). *That the surfaces read low is reasoned, general heat
     transfer, not measured here.*

   **When:** the first minute after the engine stops, **ignition back on**
   so 0x420 keeps coming — read off a capture as the raw byte, or off the
   display, whose whole degrees are fine against a 23 °C gap. Filter
   first, pan second, hose third. **Any drive will do and the harder the
   better** — the engine-health test's A4, after an hour's driving. **No
   cold reading** (*decision, 2/10/2026*): a cold engine adds
   nothing — every surface sits at ambient, which the cold soaks in item 2
   already cover without a thermometer. Any ordinary drive after it needs
   nothing but the display. *General*: the radiator fan can start with the engine
   off — hands clear of it.

   **The dipstick tube** — the best route above — needs a separate contact
   probe (the Bosch has none): a **thin, flexible wire-bead thermocouple**,
   marked at the dipstick's own length, since a stiff probe will not follow
   the tube's bend. The wet end of the dipstick shows where the oil is.
   Optional; the IR route is enough to close this.
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
   | `25_sessionA_cold_z1`, 3/10, 27 h, evening | 18.0 °C (raw 88) | 12.75 °C (raw 81) | −5.25 |

   **Consistent, and not yet decisive.** The oil sits 2–5 °C below the
   coolant at every soak, so the offset at the cold end holds up. But the four
   soaks span only ~6 °C of coolant — about 8 counts, where telling the
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
