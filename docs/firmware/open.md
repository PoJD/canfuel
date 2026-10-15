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
**11 is settled for now** — `IdleHealth` stays as it is — and waits on
one test after the engine's idle is solved.

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
  is the smoothest since August by both, which is what the owner felt
  (August's one hot hold, 22 s, graded 48; `docs/engine-health/idle-log.md`,
  *`IdleHealth` against its own 100*). They
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

### The decision: `IdleHealth` stays as it is

*Owner's decision, 4/10/2026, evening:* **nothing in the firmware
changes.** Matching 014 is not a goal worth having: the owner has often
felt an unsettled idle with 014 at zero, the ECU evidently counts little
or nothing before its adaptations settle (`docs/engine-health/refuted.md`
C19), and much else goes into it. 014 is most likely built to catch a
**real, regular misfire** and would show one plainly; what it shows at a
merely rough idle is an undocumented by-product. `IdleHealth` grades the
idle's smoothness, which is what it was built for and what the owner
feels.

The evidence behind it, all from 4/10/2026:

- **Session B** (`29`): five stops, 014 at 1.5 / 4.3 / 14.3 / 5.2 / 4.7 a
  minute; the dip count read 9.2 / 18.5 / 11.3 / 7.8 / 20.3 and
  `IdleHealth` 135 / 156 / 120 / 143 / 90. Neither follows 014.
- **The adapted stops only** (the eight where 055's learned value had
  passed about −0.93, `docs/engine-health/refuted.md` C19): rank correlation with 014 — `IdleHealth`
  −0.62, the dip count −0.05, one slow firing ≥ 6 / 8 / 12 rpm −0.50 /
  −0.29 / +0.51 (the last on two non-zero stops out of eight), second
  difference −0.38, **oil temperature +0.68**.
- **014 weighted by its size** — the sum of the counter's increments a
  minute, and its mean — over all 24 stops with a 014 log: every grade's
  correlation agrees with the count of rises to within 0.08, since the
  counter steps in twelves. With the cold stops in, every grade correlates
  *negatively* (−0.28 to −0.63): a cold idle is the roughest on engine
  speed and the one 014 does not count.
- **014 cannot be split by cylinder on this ECU**: the label file has
  group 014 and no 015 or 016.

**Considered and set aside the same day: the dip count in place of
`IdleHealth`.** Variant 3 as a replacement in byte 0, keeping the name,
with `IdleRough` (byte 1, the same grade in raw units) made reserved. It
was the sharper reading of smoothness at the hot stop, but no closer to
014 than the grade it would have replaced, and that closeness was the
reason it was wanted.

### Next: a deliberate misfire

*Owner's proposal, 4/10/2026. **Brought forward on 9/10/2026** (owner's
decision): it is now `docs/engine-health/plan.md` step 3.5, cylinders 1 and 4
in turn on up to three days, where it also names the cylinder the dips
keep to;
this was "not before `plan.md` is empty".* A known, regular misfire, so that both instruments can be read
against something real:

- **Warm idle, oil in the hot band, loads off**; the capture running and
  VCDS on 014 (with 055 and 033 beside it).
- **A minute as it is, then one injector's connector off for a minute,
  then back on for a minute.** With the connector off that cylinder gets
  no fuel, so nothing unburnt reaches the converter (*general*). One
  cylinder of four out is a quarter of the firings — about 200 a minute at
  800 rpm.
- **The fault memory cleared afterwards** (*owner*).

**What it gives:** how 014 counts a misfire whose rate is known; what one
looks like on 0x280 — the size of the dip, whether the *one slow firing*
shape of the table above appears every second revolution; and what
`IdleHealth` reads with a cylinder dead. If the grade then wants a
different scale or anchor, that is decided from this test, not before.

**Run once, 10/10/2026** (`test/fixtures/31_step4_drive_z1.txt`, with
`vcds/vcds-step5-014-055-003.csv`; cylinders 1, 4, 4, 1 at 70 °C of oil,
each cut 47–73 s rather than a minute, the owner's call while 014 read
high). What it gave:

- **014 with one cylinder of four dead**: the field changed about 60
  times a minute, median 474–528, peaks 1,152–1,188 — against 12–96 on an
  ordinary idle. About 200 misfires a minute did not make 200 changes a
  minute, so neither its rate of change nor its size is a misfire rate.
- **On 0x280**: the dead cylinder's slot sits **20–23 rpm** below the
  other three, every stroke, for the whole cut (`cutscan.py --scan`).
  So a single missing combustion at idle is about a 20 rpm step — the
  size the ordinary idle dips already are.
- **The grade** (`idledips.py --roughness --windows 30`) over windows
  holding a cut: a mean step of 3.6–10.7 rpm, the 0–200 index at its
  clamp, against 1.0–2.3 rpm on the same stop with all four firing.

Not yet read into a decision: whether the grade wants a scale or an
anchor from these is a change to `src/` and its tests, and is its own
piece of work.

### How it closes

When the deliberate-misfire test has been run and read: `IdleHealth`
either gets a scale or an anchor from it, or is confirmed as it is.
Until then nothing in `src/` changes for this question.

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

**The owner does not trust that IR reading** (*owner*, 15/10/2026), and
it is given little weight from here on (*decision*): it was the old
instrument that stops at 60 °C, its emissivity and spot on the filter
were not recorded, and a filter or a pan read from outside is a surface
cooling into the air, not the oil. With it discounted, **what is left
for the shipped slope is only the analogy with the coolant's scale**;
against it, the 25 °C gap to the coolant and the soaks' lean towards
~1.1 (*How it closes*, item 2). **Still open**: the soaks are confounded
and span 6 °C, and nothing changes in `decode.c` or the TRI file until
the winter morning.

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

### A published layout: `Kombi_2`, oil `raw − 60` (*found 15/10/2026*)

**The question was never searched on the web until 15/10/2026** (the
owner's question). It has an answer there, and it is not ours:

- **commaai's opendbc, `opendbc/dbc/vw_pq.dbc`** (the PQ platform's
  CAN database, MIT-licensed, fetched 15/10/2026 from
  `github.com/commaai/opendbc`), message `BO_ 1056 Kombi_2` — 0x420 —
  signal `Oeltemperatur_4_1 : 24|8@1+ (1,-60)`: **byte 3, `°C = raw ×
  1 − 60`**, commented "kombi oil temperature". The German names and
  their `_4_1` suffixes are VW's own message-matrix style, so it reads
  as taken from VW's matrix rather than fitted to a log — *a judgement
  about a community file, not a VW document*.
- **An Audizine thread on the RS4's 2.7T** reads 0x420 byte 3 as oil,
  `x − 60` °C, from its own logging — another platform, the same answer.

**The rest of the same definition fits this car, which is what makes it
count:** byte 0 bit 0 is `Fehlerstatus_Aussentemp` and is **set** in
every frame (b0 = 1), with the ambient bytes 1 and 2 at zero — the
cluster reporting that it has no ambient sensor, which is what
`refuted.md` B11 found the hard way (the mirror's thermometer is its
own). Byte 4 is `Kuehlmitteltemp__4_1__Kombi_2_ (0.75, −48)`, **the
cluster's coolant**, and in `18` and `38` it tracks 0x288's coolant 4–13
counts below it — a second coolant reading (the gauge's own sender,
*general*: these engines carry one for the ECU and one for the gauge).

**What it settles and what it does not.** The **slope, 1.0**, agrees
with the soaks' lean (~1.1, 1.03–1.23) and with oil near the coolant
when warm; the shipped 0.75 now rests on nothing but the borrowed
analogy. The **offset is less sure**: at the cold soaks `raw − 60` puts
the oil 3.5–5 °C *above* 0x288's coolant, and on 24/9 at 17 °C against
an ambient of 10.0 — not where a soaked sump sits — while `raw − 64`
lands within a degree of the ECU's coolant at every soak. A sender or
cluster a few degrees off at the cold end would do it; nothing here
says which. **On the display, the two differ by 4 °C**: today's 72 °C
(raw 160) is **100 °C by the DBC, 96 °C by `raw − 64`**.

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
   (*owner's decision, 2/10/2026*; `docs/engine-health/plan.md`, *Standing
   items*).

   *30/9/2026:* **The instrument: none yet** (*owner's decision, 30/9/2026*). A Bosch
   UniversalTemp was chosen on 29/9, not found in the shop and judged too
   dear for the job. The likely one now is an **Extol Premium 8831302**
   (EAN 8595126984171; the seller's listing, not a maker's manual: −50 to
   550 °C, ±1.5–3 °C with the band unstated, emissivity adjustable
   0.1–1.0, 12 : 1, operated at 0–40 °C) — enough against a 23 °C gap. It
   is **optional inside the engine-health test** (`docs/engine-health/plan.md`,
   *Standing items*, A4), decided by the owner before the drive. What was worked out for
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
   | `27_sessionA2_cold_z1`, 4/10, ~15 h | 15.75 °C (raw 85) | 11.25 °C (raw 79) | −4.5 |
   | `30_step2b_z1`, 9/10 | 15.0 °C (raw 84) | 9.75 °C (raw 77) | −5.25 |
   | `31_step4_drive_z1`, 10/10 | 13.5 °C (raw 82) | 10.5 °C (raw 78) | −3.0 |
   | `32_step3_item1_z1`, 12/10 | 10.5 °C (raw 78) | 8.25 °C (raw 75) | −2.25 |
   | `33_step3_gauge_cold_z1`, 14/10 | 15.75 °C (raw 85) | 12.0 °C (raw 80) | −3.75 |
   | `35_item5_drive_z1`, 15/10, a cold, damp morning | 10.5 °C (raw 78) | 7.5 °C (raw 74) | −3.0 |

   *Rows from `27` on added 15/10/2026*, each the first 0x288 and 0x420
   frame after ignition-on; soak lengths not recorded except where the
   fixture's README row gives one. **15/10's "very cold" start was not
   colder than 12/10's** — the same coolant byte — so the span did not
   widen.

   **The eight soaks fitted, and why it is not a result.** Oil counts
   against coolant counts give **0.68 oil counts per coolant count** (r =
   0.92), which on a coolant slope of 0.75 puts the oil's at **about 1.1
   °C per count**, 1.03–1.23 leaving any one soak out — nearer `raw − 64`
   than the shipped scale. Two reasons it settles nothing: the span is
   still **8 coolant counts, 6 °C**, where the method wants ~25; and **the
   soaks are not equal**. A sump cools faster than the water in the head,
   so a shorter soak or a warmer night leaves the coolant further above
   the oil — which is exactly what a slope above 0.75 looks like
   (*reasoned*, not measured; the soak lengths and ambients that would
   separate the two were not recorded). And it runs against the hot end,
   where the filter read within 1–3 °C of the shipped scale (`21`–`23`);
   at 1.1 the filter would sit ~14 °C below the oil, though the owner
   does not trust that reading (above). **A lean, not a reading**; the winter morning or item 1's thermometer still closes it.

   **How cold the winter morning has to be** (*worked out 15/10/2026*;
   the IR thermometer was broken the same week, *owner*, so this is now
   the way it closes). The soaks so far sit at a coolant of 10–17 °C,
   about 13 on average, with the oil 2–5 °C below it on the shipped
   scale. Both slopes have to agree there, so the table anchors each at
   that cluster (13 °C true, oil displayed ~10) and asks what the shipped
   scale would display after a full soak at an ambient T:

   | ambient | coolant shows | oil shows, if 0.75 is right | if 1.0 | if 1.1 |
   |---|---|---|---|---|
   | 25 °C, a summer dawn | 25 | about 22 | about 19 | about 18 |
   | 0 °C | 0 | about −3 | about 0 | about +1 |
   | −5 °C | −5 | about −8 | about −3½ | about −2 |
   | −10 °C | −10 | about −13 | about −7 | about −6 |

   Oil minus coolant is **about −3 °C at every ambient on the right
   scale**; on a steeper one it moves by roughly a third of a degree for
   every degree away from 13 °C — up in the cold, down in the heat. The
   soaks' own scatter in that difference is about 3 °C (−2.25 to −5.25
   above), so the move has to be twice that: **−5 °C hints, −10 °C
   settles it**, and a summer dawn at 25 °C moves it only 3–4 °C, as
   much as a 0 °C morning. *Reasoned from the fit above, not measured*,
   good to a degree or two. *This table first anchored the steeper
   slopes at raw 77 = 10 °C against the shipped scale's −3 °C offset,
   which overstated the 0 °C row by about three degrees.*

   **Summer counts only before the sun.** Sun on a parked car heats the
   bonnet and the top of the engine, where the coolant sensor is, well
   before the sump by the road; that puts the coolant above the oil,
   which is the same direction a steeper oil slope shows in the heat
   (*reasoned*). A dawn reading after a warm night is fair; an
   afternoon one is not. **No summer soak exists in the fixtures** —
   August's captures (`08`–`17`) all start on a warm engine, and `18`
   on 11/9 is the first cold start — so a summer dawn would widen the
   span, and with a winter morning give the 25 °C the method wants.

   **The procedure**: the car outside **overnight, ten hours or more**,
   so that both are at ambient and the soak-length confound above
   shrinks to nothing; the ignition on, **the engine not started**, and
   within the first twenty seconds `OilTemp` and the coolant read off
   the display — or, better, a 20 s capture for the raw bytes (the MFD
   and the capture are one or the other, `CLAUDE.md`).

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
