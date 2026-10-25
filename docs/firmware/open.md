# Firmware — open questions

**The questions about what this firmware reads and transmits that are still
open**, each with what is known, what it costs while it stays open, and the
measurement that closes it. The numbers are the ones `can-decoding.md` has
always used, because code and documents cite them; the answered ones are in
`can-decoding.md` under *Resolved questions*, and the ones not worth answering
under *Never resolved but not required*.

**One is open, 11, and it is settled for now** — `IdleHealth` stays as it
is — and waits on one test after the engine's idle is solved. **7 closed on
15/10/2026**, when 10 decided the scale, and **10 closed on 23/10/2026** at
the owner's decision (`can-decoding.md`, *Resolved questions*).

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

### Re-read in stretches, 25/10/2026

*The owner's question:* from the seat, when no jerk is felt 014 mostly
counts nothing — is there an `IdleHealth` below which 014 is silent (his
guess 45–50)? `tools/s3align.py --windows` (`--window-s 30` as well),
now with `40` and `39` paired and 014's own load field read, over
stretches of continuous standing idle rather than whole stops, oil ≥ 85 °C,
**`18` and `19` left out** (the old MAF, `docs/engine-health/refuted.md`
A11; `19` also came a day after a battery disconnect):

- **No threshold at an ordinary load.** Since the battery stayed
  connected (4/10, captures `30`–`40`), stretches below 55 still count:
  10 % of the 30 s ones silent, 36 % of samples non-zero.
- **What looked like one is the load.** Every warm stretch silent at
  `IdleHealth` 32–43 is loads on on `40`, 014's load 32–37 % against
  23–27 % ordinarily. The load alone lowers the grade and stops 014
  counting, so mixed in it reads as a threshold.
- **On fresh adaptations it did behave so** (24/9–4/10, `24`–`29`):
  Spearman rises vs `IdleHealth` **+0.69** (30 s) / **+0.91** (60 s), and
  44 % of the 55–70 stretches silent. That is the C19 state — whether 014
  counts at all follows the learned idle air — and likely where the
  owner's sense of it comes from.
- **On settled adaptations a plateau, then a knee about 80**: +0.30 /
  +0.34; 4.5–5.9 rises a minute and 36–50 % of samples non-zero anywhere
  from below 55 to 80, then 8.7 and 11 above 80 and 100.
- **The deep dips do not lead.** In the first pass of these stretches
  (*ad hoc*, not kept) the count of dips of 30 rpm and more a minute
  correlated with 014's rises at +0.04, of 20 rpm and more at +0.32,
  `IdleHealth` at +0.46: how often 014 counts follows the idle's overall
  restlessness more than its deepest dips.

So the table above's "nothing even close" was the old MAF and the cold
stops mixed in. **The decision of 4/10 stands**: on settled adaptations
`IdleHealth` below 80 says little about 014, and 014 below 80 little
about the grade.

### How it closes

When the deliberate-misfire test has been run and read: `IdleHealth`
either gets a scale or an anchor from it, or is confirmed as it is.
Until then nothing in `src/` changes for this question.
