# Firmware — open questions

**The questions about what this firmware reads and transmits that are still
open**, each with what is known, what it costs while it stays open, and the
measurement that closes it. The numbers are the ones `can-decoding.md` has
always used, because code and documents cite them; the answered ones are in
`can-decoding.md` under *Resolved questions*, and the ones not worth answering
under *Never resolved but not required*.

**10 may stay open for good, and that is allowed.** It blocks nothing:
the scale is decided and nothing in `src/` changes on it. **11 is settled
for now** — `IdleHealth` stays as it is — and waits on one test after the
engine's idle is solved. **7 closed on 15/10/2026**, when 10 decided the
scale (`can-decoding.md`, *Resolved questions*).

The engine's own faults are not here; they are `docs/engine-health/open.md`.

---

## 11. `IdleHealth` does not follow VCDS group 014 — what should it measure?

*Raised by the owner, 4/10/2026.* After step 1b the ECU's misfire counter
(group 014) read zero at both warm stops for the first time, the owner
felt the calmest idle yet, and `IdleHealth` read about what it had read
the day before. The owner wants the grade **as close to how the ECU
measures as the bus allows**.

### What was measured

Every standing stop of 60 s and more, oil above 57 °C, in the four
captures that have a 014 log beside them, 014 aligned on engine speed
(the method of `docs/engine-health/open.md` S3). Candidate grades from
0x280, each over the whole stop:

| log | oil | 014 a minute | `IdleHealth` | dips a minute (`dips_cheap`) | one slow firing ≥ 6 / 8 / 12 rpm, a minute | mean second difference, rpm |
|---|---|---|---|---|---|---|
| `19` | 72 °C | 8.0 | 123 | 16.4 | 47 / 21 / 1.3 | 6.54 |
| `19` | 88 °C | 2.0 | 64 | 10.4 | 29 / 9.7 / 1.1 | 5.90 |
| `19` | 97 °C | 0.0 | 112 | 28.4 | 68 / 19 / 3.8 | 6.76 |
| `19` | 99 °C | 0.0 | 146 | 22.1 | 78 / 39 / 3.1 | 6.42 |
| `24` | 97 °C | 9.6 | 84 | 10.9 | 36 / 11 / 0.5 | 5.56 |
| 3/10 | 87 °C | 17.5 | 114 | 12.4 | 38 / 13 / 0.7 | 6.32 |
| 3/10 | 97 °C | 5.0 | 62 | 14.9 | 8.9 / 2.0 / 0.0 | 4.28 |
| 4/10 | 64 °C | 0.0 | 117 | 14.7 | 35 / 13 / 1.1 | 5.84 |
| 4/10 | 83 °C | 0.0 | 109 | 10.1 | 38 / 11 / 0.5 | 5.89 |
| 4/10 | 99 °C | 0.0 | **60** | **5.6** | 18 / 4.7 / 0.1 | 4.81 |
| 4/10, after a hard drive | 101 °C | 9.1 | 92 | 10.1 | 16 / 2.9 / 0.3 | 5.00 |
| 4/10, the MAF wiggle | 101 °C | 14.6 | 79 | 12.8 | 16 / 3.6 / 0.0 | 5.69 |

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

1. **Keep `IdleHealth` and read it only on hot oil (≥ 92 °C)** — no
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
`vcds/vcds-step5-014-055-003.csv`; cylinders 1, 4, 4, 1 at 97 °C of oil,
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

## 10. Does the oil sender read right at the cold end?

**The scale is `°C = raw − 60`** (*decided 15/10/2026*): 0x420 is the
instrument cluster's `Kombi_2`, and commaai's opendbc `vw_pq.dbc`
(MIT-licensed, `github.com/commaai/opendbc`, fetched 15/10/2026) defines
byte 3 as `Oeltemperatur_4_1 : 24|8@1+ (1,-60)`. It is in `src/decode.c`
(`oil_c100()`), `tools/canlog.py` (`oil_c()`, which every tool uses) and
`mfd15/tri/S-AQY.TRI`.

**Why that file is believed** — it is a community file, not a VW document:

- **the rest of its `Kombi_2` fits this car.** Byte 0 bit 0,
  `Fehlerstatus_Aussentemp`, is set in every frame with the ambient bytes 1
  and 2 at zero — the cluster saying it has no ambient sensor, which
  `refuted.md` B11 found the hard way (the mirror's thermometer is its own).
  Byte 4, `Kuehlmitteltemp__4_1__Kombi_2_ (0.75, −48)`, is the cluster's
  coolant and tracks 0x288's 3–10 °C below it — the gauge's own sender
  (*general*: these engines carry one for the ECU and one for the gauge);
- the German names with their `_4_1` suffixes are VW's message-matrix
  style, so it reads as taken from VW's matrix rather than fitted to a log
  (*a judgement*);
- **an Audizine thread on the RS4's 2.7T** reads 0x420 byte 3 as oil,
  `x − 60`, from its own logging;
- **this car's soaks give the same slope on their own**: oil counts
  against coolant counts at eight cold soaks fit 0.68 oil counts per
  coolant count (r = 0.92), about 1.1 °C a count against `Kombi_2`'s 1.0;
- **warm, the oil sits at 98–104 °C**, at or a little above the coolant,
  which is where a warm engine's oil runs (*general*); the hottest recorded
  is 107 °C (`16`, `17`).

The encoding is the DBC's whole — slope and offset — rather than an offset
fitted to the soaks below (*decided 15/10/2026*, the owner's question): an
encoding has no error of its own; what can be off is the sender's reading,
and an offset fitted at one temperature would be a calibration of that one
sender carried untested to the warm end where the reading is used.

**Who reads it.** `st.oil_c100` is decoded and consumed by nothing in this
firmware. The display shows `OilTemp` straight off 0x420 through `mfd15`,
and the engine investigation compares every `IdleHealth` reading at a
matched oil temperature — on the same channel, so a bias in it moves both
sides of a comparison alike.

### What is open: the cold end reads a few degrees high

After a full soak the oil and the coolant should both sit at ambient. They
do not quite:

| soak | coolant (0x288) | oil | oil − coolant |
|---|---|---|---|
| `18_coldstart_z1`, 11/9, ~10 h | 16.5 °C | 21 °C | +4.5 |
| `19_postfix_drive_z1`, 24/9, ~19 h, ambient 10.0 °C | 12.0 °C | 17 °C | +5.0 |
| 26/9, ~10 h, cold fog; *owner-reported off the display, whole degrees* | 14 °C | 19 °C | ≈ +5 |
| `25_sessionA_cold_z1`, 3/10, 27 h, evening | 18.0 °C | 21 °C | +3.0 |
| `27_sessionA2_cold_z1`, 4/10, ~15 h | 15.75 °C | 19 °C | +3.25 |
| `30_step2b_z1`, 9/10 | 15.0 °C | 17 °C | +2.0 |
| `31_step4_drive_z1`, 10/10 | 13.5 °C | 18 °C | +4.5 |
| `32_step3_item1_z1`, 12/10 | 10.5 °C | 15 °C | +4.5 |
| `33_step3_gauge_cold_z1`, 14/10 | 15.75 °C | 20 °C | +4.25 |
| `35_item5_drive_z1`, 15/10, a cold, damp morning | 10.5 °C | 14 °C | +3.5 |

*15/10/2026, evening, off the display* (the new TRI's first reading,
*owner*, photographed): after a few hours in a garage, ignition on,
**coolant 40 °C, oil 41 °C** — +1, inside the display's whole degrees;
the old scale would have shown the oil at 28. Not a full soak, so not a
row of the table, but the first reading on the display that puts the oil
where a cooling engine's oil should be.

*Warm, the same evening* (*owner*, off the display): on the hardest
drive yet — motorway at full throttle, ~10 min at 5000 rpm — the oil
peaked at **106 °C with the coolant at 92 °C**, oil above coolant under
sustained load as a healthy engine's runs (*general*), and inside the
98–107 °C the captures record.

Each row the first 0x288 and 0x420 frame after ignition-on. **The oil reads
2–5 °C above the coolant and, on 24/9, 7 °C above the ambient** — not
where a soaked sump sits; the cluster's coolant byte errs the other way
(7.5 °C that morning). So the cluster's two senders are each a few degrees
out at the cold end. G266 measures the oil level thermally, by heating,
which could bias its temperature (*general*, not checked on this sender).

**What it costs**: a few degrees on the display when cold, and nothing
known when warm — which is the question.

### How it closes

1. **A winter morning, the engine not started.** The car outside overnight,
   **ten hours or more**, so that both sit at ambient; ignition on, and
   within the first twenty seconds `OilTemp` and the coolant off the
   display — or a 20 s capture for the raw bytes (the MFD and the capture
   are one or the other, `CLAUDE.md`). The soaks above span only 10.5–18 °C
   of coolant. **If the oil still reads 2–5 °C above the coolant at −5 to
   −10 °C**, the error is a constant offset and the warm readings are as
   good as the cold ones; **if the gap grows or shrinks**, the sender's own
   slope differs and the warm end is uncertain by about as much. *Decided
   15/10/2026*: a constant few degrees changes nothing; a drift of several
   per 20 °C would be written down beside the channel, and nothing in `src/`
   or the TRI file moves for less than that.
2. **A thermometer in hot oil, straight after a hard drive**, against
   `OilTemp` at the same moment — the direct answer at the warm end. Best a
   thin K-type thermocouple down the dipstick tube, marked at the dipstick's
   length; an IR thermometer on the sump or filter reads a surface cooling
   into the air, not the oil. **The Extol IR thermometer bought for this
   (1/10/2026) was broken the same month** (*owner*), and the one IR reading
   taken, on the filter after the 24/9 drive (the old instrument, stopping at
   60 °C, emissivity not recorded), sat 16 °C below the channel and is **not
   trusted** (*owner*, 15/10/2026). Optional.
3. **VCDS cannot do it**: this ECU has no oil temperature in any block
   (`docs/engine-health/vcds.md`). Do not spend a session looking.

---
