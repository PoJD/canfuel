# The idle log — chasing a rough idle and misfires on a VW 2.0 AQY

**A diary of one investigation, kept for the owner looking back and for
anyone with the same engine and the same complaint.** The forums hold many
threads about an AQY that idles unevenly and counts misfires, and most of
them end unresolved (`open.md`, *What the forums say about this idle*). This
one records what was done to the car, what was tested, what changed after —
and, just as much, **what nobody can say for sure a repair achieved**.

It covers the two symptoms that matter here, **S1** (the idle is unsettled)
and **S3** (the ECU counts misfires at idle). Other faults appear only where
they crossed this path. Where things stand **now** is `open.md`; what comes
next is `plan.md`; what was settled against is `refuted.md`; the car's
service record is `vehicle-history.md`. This file is the story between
them, kept current until the idle is fixed — then it stays, as reference.

**How to read it.** One entry per day, or per job where a day held two.
Every entry opens with the same three lines, and a line that would be
empty is left out:

- **Repairs** — what was changed, fitted, adjusted or added on the car;
- **Tests** — what was only tested, read or recorded;
- **Changes after** — what moved afterwards, split into *measured*, *felt*
  (the owner's impression, nothing behind it) and *not known*.

The detail follows, short. Analysis and questions that only re-read
earlier data are not entries: their findings belong to the symptom in
`open.md`. ⚠ **A repair followed by a better idle is not proof that the
repair fixed it** — several were done together, adaptations were reset
along the way, and the instruments changed twice.

*All dates are 2026. Condensed 20/10/2026 (the full version is
`git show d327332:docs/engine-health/idle-log.md`) and restructured
28/10/2026 into the three lines above (the version before is
`git show c3d8760:docs/engine-health/idle-log.md`).*

---

## What is being chased, in one picture

![One idle dip](dip-profile.svg)

*Added 11/10/2026, at the owner's request.* At a warm standing idle, every
few seconds, **the engine speed falls by twenty-odd rpm in two strokes and
climbs back in about a fifth of a second.** The picture is the average of
four hundred of them, read off the CAN bus (`open.md` S1).

1. **Half a second before**, the idle has crept a few rpm high and the ECU
   takes about one per cent of air and fuel away.
2. **Then one combustion fails or nearly fails**; the crank loses speed over
   two strokes.
3. **The ECU adds fuel, air and advance at once**; the idle is back within
   about five strokes.

**The ECU regulates correctly; the engine has lost the margin** to absorb a
charge one per cent smaller than usual. Where it went is the open question.

---

## The car, the symptoms, and the instruments

**The car.** VW New Beetle, 2.0 l **AQY** (85 kW), ECU `06A 906 018`,
model year 2000, bought in 9/2017 at 126,200 km and driven little since.
**Remapped in 6/2018**, described by the owner as mild; the tuner kept the
original (*owner*, 13/10). The engine warning lamp had been masked by a
previous owner and was restored in 2017.

**S1 — the unsettled idle.** At a standstill the engine speed dips by 20–45
rpm every few seconds and recovers in about a quarter of a second. Felt from
the seat. Roughest cold, calmer as the oil warms, calmest hot *(until
9/10/2026 this said "worst at about 71–85 °C of oil"; that peak was 014's,
not engine speed's)*. A reading without the oil temperature beside it
compares with nothing.

**S3 — misfires counted at idle.** VCDS group **014** field 3:
- a **current count** held about 3 s, not a lifetime total, despite its label;
- it **moves in steps of 12**;
- the label file specifies **0–5**; this car reads 12–120;
- it reads `deaktiv.` below about 20 % load — right at the hot idle;
- **what it counts changes with the air measurement and the adaptations**.
  **A yes/no witness, not a ruler.**

**The instruments.**
- **VCDS**: 014, 003, 055 (learned idle air), 032 (lambda adaptations), knock groups.
- **A CAN capture** (USBtin, listen only, the adapter's timestamps) —
  engine speed once per 180° of crank, one value per firing.
- **`IdleHealth`**, the mean firing-to-firing change of engine speed × 50,
  on the display and recomputed from captures; lower is smoother. **Its 100
  is two recordings on the old parts**: the 60 s warm idle of 11/8 at 85 °C
  of oil (`09`) and the five-minute cold warm-up of 11/9 (`18`), both 106 on
  this scale. And **dips ≥ 20 rpm a minute** (`tools/idledips.py`).
  **Neither reproduces 014** (`docs/firmware/open.md` question 11).

---

## Before September 2026 — the history

- **1/2018** — fault memory (`photos/vcds-faults-2018-01.png`): **16824 /
  P0440, EVAP**, intermittent; not seen since.
- **5/2019** — fault memory (`photos/vcds-faults-2019-05.png`): **P0172 too
  rich, P0300, P0304 cylinder 4**, all intermittent and stored only above a
  2 % misfire rate (`vcds.md`). Not seen again until 24/10/2026. What made
  2019 rich is not known *(this blamed the MAF until 11/10/2026; that MAF
  read near zero in August — `refuted.md` C2)*.
- **12/2017** — fuel filter changed; the old one corroded and leaking, dark
  cloudy fuel in it. **6/2018** — remap. The fuel tank was replaced at some
  unknown point.
- **For years** the idle stumbled and the cold start was poor.
- **6/2026** — new ignition coil, after a misfire under full load (gone since).
- **About 6/2026** (*owner*, recalled 16/10): **every start ran on three
  cylinders** at first, on fuel about three years old (`refuted.md` A14);
  gone with fresh fuel. Which cylinder is not known. Throttle body
  inspected: clean.
- **6/2026** — new fuel pressure regulator (*owner*, 25/10/2026; *this
  said 7/2026 until then*).
- **7/2026** — MAF connector cleaned.
- **Summer 2026** — heater replaced; **battery off more than a week**, every
  adaptation restarted. A secondary-air hose torn off in the work (P0411,
  11/8) and refitted.
- **11/8** — the first captures (`09`, `11`, `12`). Hot idle **43–48** (29
  with the A/C on); at 85 °C of oil 15 dips a minute. *This line also
  carried 032 −4.7 / +1.6 %; the owner's photo dates that reading 10/9,
  not 11/8.*
- **20/8, 7:49** — 032 **−5.5 / 0.0 %**; 001 at the same idle 760 rpm,
  coolant 94.5 °C, regulation +0.8 % (`photos/vcds-001-032-2026-08-20.jpg`,
  found by the owner in the album 25/10). Two months on the oil of 15/6,
  before any of the captures' cold idles.
- **6–9/2026, how the car was used** (*owner*, 25/10): still unregistered,
  so **many short cold runs**: started in the garden and left idling while
  he and his son sat in it, now and then moved a little on the property.
  Next to no road driving between the oil change and September.

**The picture then:** a leaking injector.

---

## 10/9 — the converter replaced

- **Repairs:** the exhaust from the flex pipe back, by a garage.
- **Changes after:**
  - *measured:* 032 **−4.7 / +1.6 %** at 17:49 (`photos/vcds-032-2026-09-10.jpg`)
    — on cells that mostly still held what was learnt on the old exhaust.

The converter of 10/2017 was **completely blocked, cracked outside, one
chamber burned through** — raw fuel burning in it, i.e. misfires. **The
one hard fact of the investigation.**

## 11/9 — a cold start recorded, on the old parts

- **Tests:** a cold start captured (`18_coldstart_z1`), VCDS 014 + 055.

**1.24 s of cranking, first firing at 451 rpm, a fall to 311 rpm, nearly
died.** The dips and the 014 increments were the same events (all seven
beside a dip, p = 0.023); no single cylinder dominated (`refuted.md` A5);
014 up to 36 at the cold idle.

## 17/9 — plugs and leads, compression

- **Repairs:** new plugs and NGK leads, at a garage.
- **Tests:** compression.
- **Changes after:**
  - *felt:* the idle a little calmer (*owner*);
  - *measured:* nothing measured it (`refuted.md` C12).

**Compression 12 bar, even on all four** (`refuted.md` A4). The old plugs
were worn out after about 1,500 km, one visibly worse — which cylinder is
not known.

## 23/9 — new injectors and fuel filter

- **Repairs:** four new Bosch injectors (the same part), a new fuel filter,
  the lines flushed; battery off.
- **Changes after:**
  - *measured:* no codes;
  - *felt:* the idle "not fundamentally different";
  - *not known:* the old injectors were never leak-tested.

Clear petrol throughout. ⚠ **Three of the four sat about 1 mm proud** of
their bores until 1/10: fitted already clipped into the rail, then the rail
pushed down; cylinder 4 was home. An old injector tried alone clicked fully
home in every bore. The manifold-end O-ring is the seal against the intake
(`open.md` H3).

## 24/9 — the MAF replaced

- **Repairs:** the MAF, genuine VW `06A 906 461 A` (afternoon; the 2018
  unit kept).
- **Tests:** a drive on all the new parts in the morning (`19`); 032 before
  and after.
- **Changes after:**
  - *measured:* 032 **−16.4 / −13.3 % → −3.1 / +4.7 %**, the air-to-fuel
    ratio back to August's; standstill dips **down 51–65 %** in every oil
    band; **014 counted more** at the hot idle, five to fifty times more per
    dip (`refuted.md` A11) — the counter, not the engine;
  - *felt:* the morning drive pulled better; the misfires stayed;
  - *not known:* since when the old MAF over-read.

In the morning the air per commanded fuel was up 14–45 % on August: **the
old MAF was over-reading**, about a third high on the hot idle after the
pulls (`refuted.md` C2). **Confident: the rich trim was the MAF.** For
anyone else: do not compare 014 across a MAF change.

The new MAF's connector points forward, as on the 2018 unit; flow direction
right; the harness not clipped in, **left as it is** (*owner's decision*,
3/10).

## 25–27/9 — testing everything cheap

- **Tests:** the table below.

| test | result |
|---|---|
| knock retard (022/023), 026 | none at idle (`refuted.md` A10); cylinder 4 retards at higher speeds (`open.md` S4/S5) |
| secondary-air valve, N112 hoses pulled at idle | valve seals; no change in `IdleHealth` (A8) |
| evaporative purge (070) | OK (A6) |
| coil connector, earths, voltages under load | no gross fault (`open.md` H4) |
| **spray test, warm idle**: front hoses, MAF-to-throttle hose | **no change**; back of the intake, injector seats, throttle joints **not** sprayed |
| loads on at idle (A/C, lights, blower) | **`IdleHealth` 70–80 → 35–50** |
| filler cap off at idle | audibly slightly worse |
| oil at the back of the head, smoke, a possible hiss | new symptoms: the cover gasket (S10, `refuted.md` D5), the hiss (S11) |
| injectors looked at, 27/9 | three of four proud (23/9) |

**The picture at 27/9:** a small unmetered air leak (the proud injector
seats, the back of the intake, the breather). Never proven.

## 1–2/10 — the valve cover, throttle and breather job

- **Repairs:** injectors refitted one by one, all four home (rail at
  10 Nm, cylinder 2's O-ring replaced); new valve cover gasket (⚠ the
  wrong part, 3/10); new upper plenum gasket; new crankcase breather (Febi
  `32452`), a new ring `100690` in the old filler cap; new throttle body
  (Pierburg `7.03703.13.0`); the vacuum elbow replaced by a longer hose;
  the throttle cable's slack taken up; battery off, every adaptation from
  zero.
- **Tests:** leads about 6 kΩ each, injector windings 15.9 Ω each; 098
  *ADP OK* (10.4°, 59.2 %); 054 5.6° at rest, 91.1° on the floor; the
  ignition-on routine still 20 s; a check start standing, part-warm
  (`vcds/vcds-postrepair-checkstart-003-014-055.csv`).
- **Changes after:**
  - *measured:* at the check start the idle as `19`'s (794 against 798
    rpm, air 3.96 against 4.28 g/s); 014 counted 13 twice, then nothing;
    `IdleHealth` 57 at its lowest that evening, every load on, fresh
    adaptations; no leaks, no hiss;
  - *not known:* one job by the owner's decision, **so no improvement can
    be put down to one part**.

**Found:** the old breather **loose on a ring flowed out of shape**
(`refuted.md` A15), the patch on its body original (C15); **six of eight
cover nuts loose by hand** over a gasket gone hard, almost like plastic
(D5); the vacuum elbow hard; the old throttle's idle switch silent, its
idle-stop face **worn 1–2 mm** (`open.md` H8). Sound: both plenum gaskets,
the June throttle gasket, the plenum face, the rear hoses, every injector
connector; no emulsion. The 20 s routine closed S13 (`refuted.md` D7, C16).
A ticking at the timing-belt end went once the belt cover was refitted.

## 3/10 — the cover leaks

- **Tests:** session A — a cold start after 27 h, a warm-up drive, warm and
  hot stops.
- **Changes after** (of 1–2/10):
  - *measured:* **014 still counted**, 16–17 a minute at 57–92 °C of oil;
    engine speed mixed — as rough or rougher in the middle band, smoother
    at the one hot stop (about a minute); the start clean, 0.77 s;
  - *not known:* how much of the counting was the hole below.

**The new cover gasket leaked a stream of oil** at cylinder 4's end, about
20 minutes in, down to the coil (`photos/cover-leak-2026-10-03-*.jpg`);
about 0.5 l topped up. Cover off that night: Elring `325.070` is **a gasket
for another engine** (AZJ, BER, AZG, AEG), with **an open arch leaving a
hole about 1 cm across into the crankcase** where the old one had a solid
ribbed half-moon (`refuted.md` C17, D5). About a litre had run down to the
driveshaft.

## 4/10 — the right gasket, then two sessions

- **Repairs:** the right cover gasket, Elring `915.653` (solid half-moons,
  metal sleeves); the plenum back on; battery off and 098.
- **Tests:** session A on fresh adaptations; the MAF wiggle test; session B
  in the afternoon after a cool-down to 47 °C of oil.
- **Changes after:**
  - *measured:* **the joint stayed dry**; **014 zero at both warm stops of
    session A — the first time ever**; hot `IdleHealth` 60–72, 4.4 dips a
    minute; 032 −0.8 / +2.3 %; **after five minutes of hard driving 014
    counted at every idle**, and in session B again from the start;
  - *felt:* calmer in session A; the belt noise gone (most likely the belt
    rubbing a cover that sat low on the wrong gasket);
  - *not known:* whether the gasket did anything for 014.

The MAF wiggle test found nothing (003 3.06–3.54 g/s against 2.92–4.03
before, 014 already counting): the contact is sound. About 1 l of oil
topped up in all. **Together** (`refuted.md` C19): 014 followed **055's
learned idle air value** — quiet above about −0.93 g/s, counting from −0.95
on, warm or cold.

| change | sure it helped? |
|---|---|
| the MAF, 24/9 | **yes** — the rich trim, and smoother engine speed |
| the job of 1–2/10 | **not shown** — both calm hot stops were on fresh adaptations, and on settled ones the hot idle is back where the MAF left it |
| the right gasket, 4/10 | **for the oil, yes**; for 014 **not shown** |
| plugs, leads, injectors, coil | did not fix the idle; the old injectors probably caused the bad cold start, which is gone. The cold burble came back warm on 4/10 (`open.md` S14) |

**`IdleHealth` against its own 100:**

| state | before the repairs | 24/9, new MAF | 3/10 | 4/10 |
|---|---|---|---|---|
| middle band, ~77–87 °C of oil | **106 (`09`, 11/8)** | 84 | 111 | **98** (A), **107** (B) |
| cold idle, first five minutes | **108 (`18`, 11/9)** | — | — | **121** (A) |
| hot, ~97 °C | 48 (`11`, a 22 s hold) | 92 | — | **72** (A) |

Against its own 100 the idle had not measurably improved.

**The starts measured from the capture** (`tools/idledips.py`;
`docs/firmware/frames.md`, *The start*). ⚠ Only a near-stall or a crank
past 1.2 s counts on its own.

| | stand | coolant | crank to first firing | `StartDip` |
|---|---|---|---|---|
| 11/9 (`18`), old injectors | ~10 h | 16 °C | 1.22 s | 141 rpm, nearly died |
| 24/9 (`19`) | ~19 h | 12 °C | 0.83 s | 118 rpm |
| 25/9 | ~12 h | — | 0.77 s | — (clean) |
| 26/9 | ~10 h | 14 °C | 0.93 s | 74 rpm |
| 3/10, session A | 27 h | 17 °C | 0.77 s | 15 rpm |
| 4/10, session A, after a disconnect and 098 | ~15 h | 15 °C | 1.38 s | 0 rpm |
| 4/10, session B, part-warm | ~2 h | 44 °C | 0.70 s | 0 rpm |

## 9/10 — small leaks sealed, and the first drive on kept adaptations

- **Repairs:** the exhaust joint behind the converter remade with a
  two-bolt sleeve connector and sealant; the dipstick guide renewed; the
  MAF-to-hose clamp changed to an all-metal one.
- **Tests:** the intake smoked, cold; the exhaust smoked, cold; a drive on
  kept adaptations (`30_step2b_z1`, steps 2b and 2c); the brake servo,
  checks a and b.
- **Changes after:**
  - *measured:* **014 counted** on the cold idle, at both warm stops (6.8 a
    minute at 79–85 °C, 11–12 at 94 °C) and home; 055 −1.1 to −1.3; 032
    −2.3 / +5.5 %; the grades no calmer;
  - *felt:* calmer at the first warm stop (*owner*);
  - *not known:* whether the MAF joint leaked before.

The exhaust joint and the dipstick guide were done for comfort and for the
smoke test; nothing is claimed for S1 or S3 (the joint is behind both
probes). **The smoke test**: the back of the intake — plenum, injector
seats, hoses — showed nothing; one stream at the dipstick guide, a faint
wisp once reseated; **smoke at the MAF-to-hose joint** under the owner's
rubber-lined clamp, clean with an all-metal clamp. Cold and stopped, so a
joint that opens only hot is not cleared. The exhaust took hardly any
pressure: H2 neither found nor ruled out. The servo assists and holds
vacuum. Cylinder 4's knock retard stayed with all four injectors home,
clearing the injectors from it (`refuted.md` B7). **A constant sputter
close behind the engine** heard: S15 (`refuted.md` D8).

## 10/10 — new plugs, leads and intake gasket; injectors 1 and 4 cut

- **Repairs:** NGK `RC-VW254` leads and `BKUR6ET-10` plugs (the same plug
  type), a new upper intake gasket.
- **Tests:** a drive (`31_step4_drive_z1`), the brake servo held twice on
  the cold idle, injectors 1 and 4 cut hot (47–73 s each).
- **Changes after:**
  - *measured:* **014 still counts** — 3.6 a minute cold, 9.4 at 81–84 °C,
    6.0 hot; `IdleHealth` hot 77 (against 89), the same mid, cold 120
    (against 95); the dips no longer kept to one slot (26 % of pairs, and
    far fewer); cylinder 4's retard nearly gone, on a gentler drive;
  - *not known:* whether the leads did anything — the intake gasket changed
    the same day.

**The old parts:** lead 4's plug end scored inside over plug 4's pitted
terminal; plug 1 almost loose; every old plug end came off far more easily
than the new ones go on (`open.md` H15). **The servo held: no dip** — cleared
(`open.md` H3). **The cuts named no cylinder** (dips by name 1: 0, 2: 7,
3: 11, 4: 2, p = 0.28); afterwards only the cut cylinders' codes stored
(P1237/P1240, P0301/P0304, P0300), cleared. The exhaust joint of 9/10 heard
moving again: S6 reopened.

## 12/10 — the joint shimmed, a new air filter, the idle raised and put back

- **Repairs:** the exhaust joint shimmed (a strip round the 54.2 mm pipe,
  sealant, nothing moves); **a new Bosch air filter** and a crack in the
  airbox ahead of the MAF sealed with putty; in the evening the joint's
  bolts tightened again and **lead 4 reseated**.
- **Tests:** the exhaust photographed from below, cold; the exhaust test
  cold (ten closures); the clutch up and down at idle; the idle speed
  raised in steps and put back (`32_step3_item1_z1`); three original hoses
  looked at.
- **Changes after:**
  - *measured:* **the warm idle calmer than any day before** at the same
    oil — `IdleHealth` 50 and 61 against 77–89 on 9/10 and 10/10; 014 5.3
    rises a minute hot, 40 % of samples (9/10: 8.8, 58 %); 055 −1.18 to
    −1.21; 032 0.0 / +2.3 %; the dips kept to one slot again (38 %, p =
    0.0011); the joint not heard (S6 closed, the sputter S15 with it);
  - *not known:* whether the calmer idle is the filter and the airbox, the
    weather or chance.

From below nothing seen at the front joint or 3 and 4's pipes; the blanked
boss behind the front probe is an old probe, leads cut. The exhaust test
cold found nothing: H2 not refuted, a crack may open only hot. **The clutch
makes no difference** (`open.md` H12). The hiss (S11) closed at the owner's
decision. A tick in neutral, cold, pedal up: S16, not pursued.

**The idle speed** (`refuted.md` D9): two minutes at each stage, then back
to 128 (`vcds/vcds-step3-1-back128-014-056.csv`). **No stage quieted 014.**

| channel 01 | specified rpm | `IdleHealth` | dips /min | 014 steps up /min |
|---|---|---|---|---|
| 128 | 780 | 61 | 4.9 | ~9 |
| 130 | 800 | 66 | 2.3 | ~5 |
| 132 | 820 | 68 | 5.1 | ~4 |
| 133 (the ECU's limit) | 830 | 68–70 | 2.6–3.1 | ~5 |

**The three original hoses** (photographed; `refuted.md` A15, C9): the
breather hose `06A 103 493 N` split at its cuff, oily, a black layer about
0.5 cm thick inside; the shroud supply crazed; **the thin hose to the tee by
the runners, `06A 133 374`, cracked at its bend and leaking** — the one at
manifold vacuum. All three to be replaced (*owner's decision*). The intake
hose `1C0 129 684` leaks nowhere.

## 14/10 — the hoses renewed, and the vacuum gauge, cold

- **Repairs:** **a new breather hose** (Gates `EMH118`), **the thin hose to
  the tee** and **the 8 mm hose to the throttle**, new clips.
- **Tests:** a vacuum gauge (MAR-POL `M57673`) on the top of the tee by the
  runners, cold (`33_step3_gauge_cold_z1`) and part-warm
  (`34_step3_gauge_2500_z1`).
- **Changes after:**
  - *measured:* `IdleHealth` about 103 (`33`) and 114 (`34`), cold and
    part-warm; 003's cold air and the cold idle as on earlier days —
    nothing sets the renewed hoses apart, cold;
  - *not known:* the effect warm.

| moment | true vacuum, inHg (±1½) |
|---|---|
| settled idle, ~815 rpm | **about 18–19** — in the green band |
| throttle opening, ~1600–1700 rpm | about 13, a moment |
| steady 2000–2150 rpm | about 20–21½ |
| sharp release from ~2600 rpm | **about 24–25**, back to 19 in ~3 s |

**Steady and normal** (`open.md`, *How the vacuum gauge is read*): no large
leak behind the throttle, no valve that does not seal, as far as a gauge on
the plenum can say; it cannot see a small leak at one runner. **No flick**
at the dips that could be read. The hiss heard again, cold: S11 reopened.

## 15/10 — a can of cleaner, and the gauge warm

- **Repairs:** one can of Liqui Moly *DFI Cleaner* with about 18 l of OMV
  MaxxMotion 100.
- **Tests:** the drive (`35`–`38`), the vacuum gauge warm (`38`), the
  hardest drive yet (~10 min at 5000 rpm).
- **Changes after:**
  - *measured:* 032 −4.7 / +4.7 %; 055 −1.18 g/s; 003 at the warm idle
    3.15 g/s, unchanged; `IdleHealth` 54 at home and 59 over `38`, as calm
    as 12/10; 014 on 25 % of samples at the home idle; after the hard drive
    the display read **23–25 with the A/C and blower on**, the lowest
    yet, and about 80 lights only at home after;
  - *not known:* the can had been in an hour — a before, not an after.

**The gauge warm**: about 19 inHg at idle, 22 steady at 2490 rpm, 22½–23 on
each release; no flick of 0.1 inHg in 78 readable seconds, none at seven
readable dips. **The display's `OilTemp` moved to `raw − 60`** the same
evening; every oil figure since is on it (`docs/firmware/can-decoding.md`
question 10).

## 16/10 — 014 against the A/C

- **Tests:** a brisker drive, then the warm idle with the A/C on and off
  (display, VCDS 014).

`IdleHealth` about 50–70 at oil 99 °C. **A/C on: 014 zero for several
minutes, `IdleHealth` about 70; A/C off: 014 counting, `IdleHealth` barely
moved** (`open.md` S3, *The A/C switches it*).

## 17/10 — the cleaner's tank run down

- **Repairs:** refilled with OMV MaxxMotion 100, no cleaner.
- **Tests:** a brisk motorway drive and a warm stop (display).
- **Changes after** (of 15/10's can):
  - *measured:* `IdleHealth` mostly 70–90 loads off, about 40 at its lowest
    with every load on — **no better** than before the can; `FuelAvg` 10.3
    l/100 km;
  - *felt:* pulled normally.

No second can (`plan.md`, Part 2).

## 18/10 — cylinder 3 out, and a tick

- **Tests:** the fault memory read before the afternoon drive.

**Morning, cold**: on a short gentle drive the engine **ran on three
cylinders for a while**, with a tick at camshaft rate (the owner's video);
the clutch did not change it. **P0303 and P0300 stored** — the ECU's first
named cylinder. Cylinder 3 dropped out again, lamp flashing; after a
restart all four ran and the tick stayed gone. The day after the cleaner's
tank ran out (`refuted.md` D10, S18).

**Afternoon, warm**: P0300 and P0303 twice each, sporadic; cleared. **The
tick came back a few minutes in and stopped by itself**; `IdleHealth` while
it ticked about 120–130, 80–90 without. 014 two bursts under part load,
270 and 351 — nothing above 72 had been logged driving. **Not known**: a
flake of deposit, or a valve or lifter on 3; the owner holds deposits (H13)
the most likely.

## 19–20/10 — the adaptations read, and the look inside

- **Repairs:** injector 4's peeling tape renewed; lead 2 torn on removal.
- **Tests:** VCDS engine off (19/10); a borescope through the ports and the
  plug holes, the plenum off (`plan.md` 6b; `open.md` H13 test 3).

19/10: fault memory **empty** after three drives; **032 −3.1 / +5.5 %, 055
−1.27 g/s**, inside their earlier ranges — an adaptation learnt in the
misfires is not why the idle got worse. Warm idle that day about 100 loads
off, about 50 every load on.

A reading of a cheap screen, not a measurement:

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| inlet port deposit | least | little | **most** | some |
| back of the inlet valve | thin lacquer | thin lacquer | thin lacquer | thin lacquer |
| injector tip | clean | clean | clean | clean |
| plug, firing end | **black, sooted** | lighter, grey | **the cleanest** | **black, sooted** |
| oil on the plug's thread | yes | yes | yes | yes |
| lead's plug end came off | hard | hard, **tore** | **easily** | **easily** |
| exhaust valve | a band at the edge | clean | **deposit come away** | a thin rim |
| piston crown | thin layer | thin layer | **layer breaking up** | **crust at the edge** |
| wet patches on the crown | yes | yes | yes | yes |
| bore | cross-hatch, no scores | the same | the same | the same |

**No valve back coked** — nothing for a walnut clean; valves whole, bores
unscored. **3 and 4 differ from 1 and 2**; only 3 shows deposit come away.
The camera cannot show whether a valve seals.

## The week of 19/10 — the valve cover nuts re-tightened

- **Repairs:** the cover nuts re-tightened, a few hundred km on the new
  gasket (*owner*, reported 26/10). Nothing claimed for the idle.

## 21/10 — VW plugs and leads, a new plenum gasket, and the drive after

- **Repairs:** plugs `101 000 033 AA` (NGK `BKUR6ET-10` in the box, the plug
  of 10/10) and **VW leads `06A 905 409 L`**, routed clear of the plenum's
  brackets (`photos/leads-vw-2026-10-21-*.jpg`); the plenum back on a new
  Elring `271.230`.
- **Tests:** an hour's drive (`40_refit_drive_z1`): a cold start, the
  two-state warm stop, full-throttle pulls, a warm stop at the end; VCDS
  014, 001, 003, 020, 032, 055.
- **Changes after:**
  - *measured:* the warm stop loads off `IdleHealth` 67–79, every load on
    **34–45**, about where it was before 18/10, not better; against every
    settled idle since 24/9 **level with 12–15/10**, and every load on the
    calmest recorded (37, 0.7 dips a minute); cold 94, against 109–137;
    014 at warm idle 2.7 and 4.6 rises a minute (26 % and 43 % of
    samples), a hard zero every load on; **the dips spread over all four**
    (top two 58 %, p 0.77) — the first capture since `24` not keeping to a
    pair; 032 −6.3 / +5.5 %, 055 −1.42 to −1.37 g/s; nothing the MAF can
    see changed;
  - *felt:* calmer, with longer quiet stretches, though not always; full
    throttle a touch livelier — nothing measured shows it, nor contradicts
    it;
  - *not known:* one drive.

Every VW plug end went on with the same force, clicked, and sits with no
play; the NGK ends had a slight play at 3 and 4, perhaps 1. Fault memory
empty throughout. Cylinder 4 still retards at full throttle (S4). A
hesitation of about a second after a 1–2 change was **the traction
control** (0x1A0 reading inferred from this one event); not a symptom
(*owner's decision*).

## 23/10 — the first tank of 44K

- **Repairs:** one can of BG 44K into 23.5 l of OMV MaxxMotion 100, at
  154,501 km (`plan.md` 6a).
- **Tests:** a hard motorway run and Prague traffic (display); VCDS
  afterwards, engine off.
- **Changes after:**
  - *measured:* `IdleHealth` in the everyday state 45–50 between jerks,
    70–90 with them; **37 straight after a stretch above 4000 rpm**, the
    lowest yet in that state, back to 50 within a minute; fault memory
    empty; 032 −3.1 / +4.7 %, 055 −1.32 g/s, back where they were before
    21/10;
  - *felt:* new to the owner — after hard driving before, the lowest came
    only after about half a minute;
  - *not known:* whether it is the cleaner, and whether it lasts.

## 24/10 — the second tank of 44K, a bad start, P0172

- **Repairs:** the first tank run down to 0.4–0.7 l; **the second can of
  44K** and 50.88 l of **Orlen Verva 100** at 154,755 km — the first fill of
  another brand since 2017.
- **Tests:** about 340 km in the day, an hour above 4000 rpm; a phone
  recording over injectors and cover, part-warm (`plan.md` 6c), and **the
  injector loom flexed by hand** while it was made, above all the repaired
  wire at injector 4, judged by ear only (*owner*, reported 28/10): no
  change heard; a cold
  capture with injector 4 cut for 30 s (`41`, `plan.md` 6d, VCDS
  014/001/003).
- **Changes after:**
  - *measured:* **no tick, no miss, no lamp** all day; `IdleHealth` 70–80
    part-warm and warm, everyday state — no change; `Power` about 87 kW
    above 5000 rpm; the first tank 9.9 l/100 km off the pump
    (`docs/firmware/fuel-check.md`); in the cold capture `IdleHealth`
    123–131 for the first five minutes, 87–104 from oil 73 °C;
  - *felt:* pulls well, perhaps better (the owner calls it possibly
    placebo);
  - *not known:* whether the strong tank did anything to the idle; what set
    P0172.

**S18 closed** (*owner's decision*; `refuted.md` D10): no tick, no
three-cylinder running and no lamp since the evening of 18/10.

**A bad start in the afternoon**: after about 4 hours parked nose uphill,
the engine **caught and died at once, as if it had no fuel**; the next start
normal. The first in about a month (`open.md` S7).

**The phone recording** (oil 52–58 °C, 810 rpm): one click per firing, all
four alike, at every one of the eight places — **no cylinder's sound stands
out**; injector against injector cannot be told this way.

**The cold capture**: the fault memory before the start held **16556 /
P0172, too rich**, the first since 5/2019; after the cut **17648 / P1240,
injector 4 open circuit**, and no P0304 — 014 counted through the cut
regardless, and counts cold (12 to 72 in the first five minutes). Both
cleared by the owner, so the trims behind P0172 were lost: 032 read 0.0 /
0.0 % after, 055 −1.31 g/s. **The dips: all four alike** (top two 55 %,
p = 0.77; by name 1: 24 %, 3: 31 %, 4: 20 %, 2: 25 %).

## 25/10 — the regulator's vacuum hose found cracked and renewed

- **Repairs:** the regulator's vacuum hose — first the cracked end cut back
  about 1 cm and the hose turned round; in the evening **a new hose**
  (STARLINE 4 × 8 mm) **with a spring clip at each end**
  (`photos/fpr-vacuum-hose-2026-10-25-*.jpg`; `plan.md` 6e).
- **Tests:** the old hose pulled off at a running idle; VCDS 032/055 before
  the new hose; the first warm idle on it, VCDS 014/001/033 (`plan.md` 6i);
  a drive and a warm stop in the everyday state, VCDS 014/001/032 (`plan.md`
  6j).
- **Changes after:**
  - *measured:* 032 −8.6 / +3.9 % before (the most negative idle value
    on record, perhaps carrying the seconds the hose was off) → **−4.7 /
    +3.9 %** after the first idle → **back to −7.8 / +6.3 %** after the
    drive; **014 still counts warm** on the new hose, more towards the end
    of a long stop; `IdleHealth` loads off about 90, every load on 35–40,
    where it sat warm before; fault memory empty;
  - *felt:* no jerk in the seat at any point; in the calmer stretches the
    engine speed drops a little and holds there (*owner, by ear*);
  - *not known:* a smoother idle; the hose answers part of the rich idle,
    not all of it.

**Found:** the hose's intake end **breaking up**, the wall parted into
layers, a crack from the bore outwards; no clip on it since 6/2026 and
pinched at least once in an intake job — the crack from about September
(*owner*). A split there pushes rich (`open.md` H7), the first part found
that fits 032's shape. **Pulled off at idle for a few seconds**: vacuum on
the intake side, no fuel at the regulator end, `IdleHealth` 70 → about 120.

**The first idle on the new hose**, oil about 80 °C: the lambda regulation
sat at **+6.5 %** for a minute and a half — the ECU giving back fuel the
adaptation had learnt to take away — then fell to −10 % and settled at
about −1 %: **something brought about 3 points of fuel two minutes into a
warm idle**, the canister purge the obvious candidate (*not shown*). The
probe switches 36–50 times a minute, against VW's 20. 014 read 12 on and
off loads off and 0 every load on.

**The drive and warm stop**: 014 12 ten times, 24 twice and 36 once on a
4.7-minute stop at 94–99 °C of coolant, `IdleHealth` 70–80; it also
counted while driving; no step in the regulation like the first idle's.

**The morning's cold start**, after 12 hours on the level, **caught and
died**, the second ran — so 24/10's slope was not needed. S7 reopened
(`open.md`); priming on alternate mornings (`plan.md` 6h).

## 25/10, night — N80 and the regulator, cold

- **Tests:** N80 blown through engine off and felt at a running start; the
  regulator's hose off at the intake end twice for about 40 s (`plan.md`
  6e; VCDS 032, 055, 001, 033).

**N80 passes "really little"** blown through at rest — by 6e's rule a valve
that does not seal — but with the engine running a finger on its port felt
no suction until the pulses came, and no liquid fuel. **With the canister
cut off the regulation sat at −0.7 % with 032's −7.8 still in force**: the
fuel behind the negative idle trim does not come through N80, at least
that night. **The regulator's hose off**: the regulation went to −8.6 and
−10.2 % within seconds, +3 to +8.6 % back on — the step the regulator owes
its reference, twice. **So neither N80 nor the regulator's reference is
the source**; H17 and an injector are left (`open.md` H7, H17). N80 not
replaced (*owner's decision*). `IdleHealth` 120–140 cold. Fault memory
empty; 032 −8.6 / +7.8 % after.

## 26/10 — the cold start, plain, and the readings before the oil change

- **Tests:** the cold start not primed (`plan.md` 6h); 032 and 055 engine
  off (`plan.md` 6g's *before*); a phone recording hot, oil 100 °C (`plan.md`
  6c).

**The start**: about 10 hours in the garage, coolant 24 °C; the starter
held about 4 s; **it did not die**. **`StartCrank` 1.22 s, `StartDip`
218 rpm** — the deepest `StartDip` on record: it fired at 1.22 s and fell
back to cranking speed, the catch and die of 24 and 25/10 carried by the
starter (`open.md` S7).

**032 −8.6 / +7.8 %, 055 −1.14 g/s**, fault memory empty
(`photos/vcds-032-055-2026-10-26-before-6a.jpg`).

**The phone recording hot**: one click per firing, all four alike at all
eight places, no cylinder standing out — **hot, no lifter ticks** at
camshaft rate, which the part-warm recording could not say.

## 26/10 — two EPR flushes and the oil change; P0507, P1582

- **Repairs:** at 154,999 km **two cans of EPR**, each 30 minutes at
  1220–1300 rpm with the pedal held by a stick; drained hot after each, a
  Bosch `0 451 103 314` filter between; **VW filter `06A 115 561 B`, a new
  VW drain plug and Total *Quartz 9000 Energy* 5W-40**, about 4 l; at night
  **the battery off for about a minute**.
- **Tests:** the fault memory and 032/055 after each flush; 098 (opened as
  a measuring block, so it did not run); 055 logged as it relearnt
  (`vcds/vcds-step6a-055-relearn-014-055-001.csv`).
- **Changes after:**
  - *measured:* **P0507** (idle above target) after each flush and
    **P1582** (idle adaptation at its limit) after the second — the stick
    holding the speed up for half an hour; **055 −2.10, then −2.78 g/s**,
    outside VW's ±1.50; on the first drive without the stick **P1582 back
    and the engine nearly stalled after a warm start**, twice; the minute's
    disconnect reset 032 to 0.0 / 0.0 but **not 055**; then **055 learnt
    itself back** over warm idling, −2.78 → **−0.90**, and the next three
    starts were clean, lamp off;
  - *felt:* the engine livelier overall, revving more willingly (*owner*,
    28/10, who allows it may be placebo);
  - *not known:* anything for the idle — read on the new oil with 6g's 032
    at about 200 km.

No tick during either flush. The first drain dark, even, no foam, no
emulsion; the second black. The underside oily, the sump's rear the
wettest, before the change too (`open.md`, *Other*). **055 learns only at a
warm standing idle** and holds through driving; **with the A/C on it reads
exactly 0.00** (bits `0101`). 014 counted at every learnt value from −2.8
to −0.97 (19–49 % of the warm idle), with no trend. `IdleHealth` off the
display 55–60 at 62 °C of oil, about 100 warm with the value at about −2.

## 27/10, morning — a primed cold start, and the A/C at a warm stop

- **Repairs:** about 0.4 l of oil topped up at 155,024 km, after the level
  fell overnight as the oil ran back from the head; at the top mark after
  the drive (`plan.md` 6i's first reading).
- **Tests:** the cold start primed four times (`plan.md` 6h); a gentle
  drive and a warm stop in steps of load, A/C on and off (`plan.md` 6k;
  display video, VCDS 014/055/001).

**The start**: 11 hours at 18 °C, primed four times. **Not clean**: it
cranked long, ran and **hesitated for a while**; `StartCrank` 1.18 s,
`StartDip` 0 — the display misses a stumble carried by the held starter.
Before the new injectors priming always made it catch at once (*owner*), so
this is not the rail draining while standing.

**The warm stop**, oil about 88 °C:

| state | `IdleHealth` (video) | 014 | 055 field 3 |
|---|---|---|---|
| everyday | **~70** (59–73) | 12–72 | −1.11 → −1.04 |
| + A/C, first minute | 59 → 45 | 0 | **0.00** (`0101`) |
| + A/C, minutes 2–5 | **35–50** | 0 | 0.00 |
| + A/C, minute 6 | **56 → 75** | 0 | 0.00 |
| + A/C + every load but main beam | **35 → 25** | 0 | 0.00 |
| every load but the A/C and main beam | **54–62**, 37 at the end | 12 ×3, then 0 | −1.04 → −0.77 |

**`0101` is the A/C**: with it on field 3 holds 0.00 and field 2 carries
the correction. The loads calm the idle without the A/C too, and the A/C's
sixth minute was not calm. **On the drive 014 counted on the road**, at
1160–2100 rpm and 25–30 % load, at the jerk the owner feels when the
throttle goes back on: **S12 reopened**. 032 −6.3 / +8.6 %; fault memory
empty.

## 27/10 — the throttle cable slackened, and 055 reset

- **Repairs:** **the throttle cable slackened** — taken up to the stop on
  1–2/10, the top of the pedal's travel no longer felt right; **the battery
  off, both poles, for several hours**; 098 run under basic settings.
- **Tests:** 054 after the cable; 032 and 055 before and after 098; the
  drive home (40 minutes) and the idles after it, VCDS 014/055/003
  (`plan.md` 6l).
- **Changes after:**
  - *measured:* 054 about 5° at rest, 90° on the floor — the plate still
    rests and still opens fully; **after hours off 032 and 055 both at
    0.00**: a disconnect of hours resets 055, a minute does not; 098 *ADP
    OK*, plate 5.6°; **055 relearnt to −1.11 to −1.13 within three
    entries into idle** (about 3 minutes in all) — back where it was;
    032 −6.3 / +6.3 % after the drive; `IdleHealth` about 50 in the
    everyday state, as on 26/10;
  - *not known:* not a repair, and not meant as one.

**055 learns only in the 15–30 s after each entry into idle** — a stop, the
A/C going off, a blip — and holds between; a steady drive teaches it
nothing. Fault memory empty throughout. The 098 *ADP OK* of 26/10 and of
this morning had been read as a measuring block, so no adaptation ran then.

## 27/10, evening — the accelerator pedal greased, and the drive after

- **Repairs:** **the accelerator pedal greased.**
- **Tests:** the plate angle logged against the pedal before and after,
  ignition on, engine off (VCDS 098/060/003 as measuring blocks); a
  15-minute drive and a warm stop in two states (VCDS 014/003/055, two
  display videos).
- **Changes after:**
  - *measured:* off rest the plate now moves **in steps of 0.4–0.5°, the
    sensor's own resolution**, four times out of four, where before it
    jumped 1–4° (5.6 → 8.7 → 10.0°); at the warm stop, oil 100 °C, every
    load off **`IdleHealth` mean 54**, swinging 35–65 in waves of about a
    minute and a half, every load on with the A/C **mean 34**, 26–32 in its
    third minute; 014 counted 12–36 five times on the road at a steady
    2000–2200 rpm and 25 % load, none at a tip-in; 032 −8.6 / +8.6 % —
    back where it was on 26/10; 055 −0.97;
  - *felt:* **the throttle could be fed in smoothly, for the first time
    with this car** — **S12 closed** (`refuted.md` D6);
    the speed wandering at a held pedal (S20) a little better, still
    there (28/10);
  - *not known:* nothing at idle — the pedal is not touched there.

The pedal stuck in the band where the ECU switches from idle to part load.
At the warm stop loads off **014 counted in the calming halves** of the
waves and not in the climbs, about 7 rpm lower and 1° more advance while it
counted — two waves on one stop, so not a finding, but the opposite of 014
counting a rough idle (`open.md` S1, *By ear*). The display's supply 14.1 V
loads off, 12.5 V loads on. *The two `IdleHealth` means are read off the
videos (28/10); the owner's glances had given about 45 and 39.* Fault
memory empty before and after.

## 28/10, morning — the cold start, plain

- **Tests:** the cold start not primed, after about 10 hours (`plan.md`
  6h).

**It ran**: perhaps a slight hesitation in the first second, but **no
fall of the engine speed** as on the mornings before (*owner*).
**`StartCrank` 0.7 s, `StartDip` 0** — as quick as the clean starts of
24/9–4/10 (0.70–0.93 s). The temperature was not given. Three starts now
(26/10 plain, bad; 27/10 primed, hesitant; 28/10 plain, clean) do not
follow the priming, which is against a rail that drained while standing
(`open.md` S7). **The throttle cable does not fit** (*owner*): it was
taken up from the new throttle's fitting on 1–2/10, and the starts were
clean for three weeks after that, until 24/10. *This said the cable,
slackened 27/10, could not be told apart from the battery disconnect.*
The owner's reading: the fuel, or deposits loosening as the cleaner's
tank runs out — not known.

## 28/10, afternoon — after 6 hours outdoors, caught and died

- **Tests:** the start not primed, after about 6 hours parked outdoors on
  the level, about 10 °C outside (*owner*; `plan.md` 6h).

**It caught and died at once**; the starter was not held (*owner*), so
nothing carried it as on 26/10. The second start was clean. **The first:
`StartCrank` 1.41 s, longer than any start above, `StartDip` 254 — saturated,
the engine stopping inside the 2 s — `StartClt` 18 °C. The second: 0.74 s,
0, 18 °C.** Shortly after, coolant and oil 20 °C, the display's supply
14.7 V, `VddConv` 5.00 V. On the level, unlike 24/10's nose uphill.
Like 24/10, an afternoon after a few hours outdoors; the morning's start,
after about 10 hours in the garage, was clean (`open.md` S7).

## 29/10 — the second 44K tank run out; OMV; a start that did not fire

- **Repairs:** 50.16 l of OMV MaxxMotion 100plus at 155,193 km, no cleaner; the Verva and
  44K tank run down to 2.2 l indicated (`vehicle-history.md`).
- **Tests:** the cold start, plain; the four figures before the nozzle
  (`docs/firmware/fuel-check.md`, *The fill of 2026-10-29*); the
  afternoon's start; 032 and 055 at about 200 km on the new oil.
- **Changes after:**
  - *measured:* the afternoon's start `StartCrank` 0.80 s, `StartDip`
    103, `StartClt` 22 °C; **032 −8.6 / +5.5 %, 055 −1.11 g/s**;
    `IdleHealth` 90–130 home from the pump;
  - *felt:* the afternoon's start bad, less than the morning's; the idle
    home very unsettled;
  - *not known:* anything about OMV yet — the lines still held the Verva.

**The start**: **3–4 s of cranking with not one firing**, the key off;
the second caught a little and died; the third ran (*owner*) — the first
start in the investigation that did not fire at all (`open.md` S7).
In the garage at 17 °C, coolant and oil about 25 °C; the morning's start,
before the fill. How long parked and the display's figures not given.

**The tank**: 438 km by the odometer, **11.45 l/100 km off the pump**;
the converter's fuel within 0.6 % of the pump's, its distance 1.2 % over
the odometer (`fuel-check.md`). **The idle at its end no calmer**: about
70 everyday on 27/10, 70–100 on 28/10 (`open.md` S1).

## 30/10 — the first starts on OMV

- **Tests:** the cold start, plain, after about 16 hours in the garage
  (`plan.md` 6h); `IdleHealth` at a warm stop; the afternoon's start,
  plain, after about 4 hours in the garage, about 30 km on OMV; the
  evening's, plain, after about 4 hours more.
- **Changes after:**
  - *measured:* the morning's `StartCrank` 0.77 s, `StartDip` 0,
    `StartClt` 20 °C (oil 24 °C, 17 °C in the garage); `IdleHealth`
    80–100 everyday at 99 °C of oil; the afternoon's `StartCrank` 0.70 s,
    `StartDip` 0, coolant 38 °C and oil 41 °C before it; the evening's
    not read;
  - *felt:* the morning's start nearly clean, a slight hesitation; the
    afternoon's and the evening's clean, as before 24/10 (*owner*; *the morning's said
    "clean" until the afternoon*);
  - *not known:* whether it is the OMV — the morning's lines held only
    about 8 km of it, and the later two came after only a few hours,
    the afternoon's warm.
