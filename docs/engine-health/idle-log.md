# The idle log — chasing a rough idle and misfires on a VW 2.0 AQY

**A diary of one investigation, kept for the owner looking back and for
anyone with the same engine and the same complaint.** The forums hold many
threads about an AQY that idles unevenly and counts misfires, and most of
them end unresolved (`open.md`, *What the forums say about this idle*). This
one records what was believed at each point, what was done, what was
measured, and — just as much — **what nobody can say for sure a repair
achieved**.

It covers the two symptoms that matter here, **S1** (the idle is unsettled)
and **S3** (the ECU counts misfires at idle). Other faults appear only where
they crossed this path. Where things stand **now** is `open.md`; what comes
next is `plan.md`; what was settled against is `refuted.md`; the car's
service record is `vehicle-history.md`. This file is the story between
them, kept current until the idle is fixed — then it stays, as reference.

**How to read it.** Each stage gives the picture *at that time* (sometimes
wrong, and says so), what was done, what it measured, and what is not
known. ⚠ **A repair followed by a better idle is not proof that the repair
fixed it** — several were done together, adaptations were reset along the
way, and the instruments changed twice.

*Condensed 20/10/2026 to what was done, measured and not known; the
reasoning and derivations behind each entry are in the full version,
`git show d327332:docs/engine-health/idle-log.md`.*

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
  2 % misfire rate (`vcds.md`). Not seen again. What made 2019 rich is not
  known *(this blamed the MAF until 11/10/2026; that MAF read near zero in
  August — `refuted.md` C2)*.
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
  carried 032 −4.7 / +1.6 %; the owner's photo dates that reading 10/9
  (below), not 11/8.*
- **20/8, 7:49** — 032 **−5.5 / 0.0 %**; 001 at the same idle 760 rpm,
  coolant 94.5 °C, regulation +0.8 % (`photos/vcds-001-032-2026-08-20.jpg`,
  found by the owner in the album 25/10). Two months on the oil of 15/6,
  before any of the captures' cold idles.
- **6–9/2026, how the car was used** (*owner*, 25/10): still unregistered,
  so **many short cold runs**: started in the garden and left idling while
  he and his son sat in it, now and then moved a little on the property.
  Next to no road driving between the oil change and September.

**The picture then:** a leaking injector.

## 10/9 — the blocked converter

The exhaust replaced **from the flex pipe back** by a garage: the converter
of 10/2017 was **completely blocked, cracked outside, one chamber burned
through** — raw fuel burning in it, i.e. misfires. **The one hard fact of
the investigation.**

032 **−4.7 / +1.6 %** at 17:49 on 10/9 (`photos/vcds-032-2026-09-10.jpg`,
found by the owner in the album 25/10): **after the exhaust work** — the
car went to the garage on 9/9 (*owner*). Little driving since, so the
cells mostly still hold what was learnt on the old exhaust (*reasoned*).
*This reading used to be dated 11/8.*

## 11/9 — a cold start recorded, on the old parts

`18_coldstart_z1`, with 014 + 055. **1.24 s of cranking, first firing at
451 rpm, a fall to 311 rpm, nearly died.**
- **The dips and the 014 increments were the same events** (all seven
  beside a dip, p = 0.023).
- **No single cylinder dominated** the roughness (`refuted.md` A5).
- 014 at a cold idle: up to 36.

## 17/9 — plugs, leads, compression

At a garage: **new plugs and NGK leads**. The old plugs were worn out after
about 1,500 km, one visibly worse — **which cylinder is not known**.
**Compression 12 bar, even on all four** (`refuted.md` A4). The owner felt
the idle a little calmer; nothing measured it (`refuted.md` C12).

## 23/9 — new injectors and fuel filter

By the owner: four new Bosch injectors (same part), new filter, lines
flushed — **clear petrol throughout**. Battery off. **The old injectors were
never leak-tested.** ⚠ *Found 27/9:* **three of the four sat about 1 mm
proud** of their bores until 1/10. Afterwards: no codes; the idle "not
fundamentally different".

## 24/9 — the post-repair drive, and the MAF

Morning (`19`), all new parts: **pulled better; misfires stayed.** 032
**−16.4 / −13.3 %**; air per commanded fuel up 14–45 % on August.

**Afternoon: the MAF replaced** (genuine VW, for an insert of 2018). **032
−3.1 / +4.7 %**, the air-to-fuel ratio back to August's: **the old MAF was
over-reading that morning** (`refuted.md` C2), about a third high on the hot
idle after the pulls; since when is not known.
- **Confident:** the rich trim was the MAF.
- **Engine speed smoother**: standstill dips down 51–65 % in every oil band.
- **014 counted *more*** at the hot idle — five to fifty times more per dip on
  the new MAF (`refuted.md` A11): **the counter, not the engine.**

**For anyone else:** do not compare 014 across a MAF change.

## 25–27/9 — testing everything cheap

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

**The picture at 27/9:** first **a small unmetered air leak** (the proud
injector seats, the back of the intake, the breather). Never proven.

## 1–2/10 — the valve cover, throttle and breather job

One job by the owner's decision — **so no improvement can be put down to one
part** (detail in the appendix).
- **Injectors refitted** one by one, all four home (one O-ring replaced).
- **New valve cover gasket** (⚠ the wrong part — 3/10), new upper plenum gasket.
- **New breather** — the old one loose on a ring flowed out of shape.
- **New throttle body** — the old idle-stop face worn 1–2 mm; 098 OK.
- Found: six of eight cover nuts loose by hand over a gasket gone hard; the
  vacuum elbow hard with age.
- Battery off again: every adaptation from zero.

## 3/10 — session A: still counting, and the cover leaks

Cold start after 27 h (0.77 s crank, clean), warm-up drive, warm and hot stops.
- **014 still counted**: 16–17 a minute at 57–92 °C of oil.
- Engine speed **mixed**: as rough or rougher in the middle band, smoother at
  the one hot stop (about a minute).
- **The new cover gasket leaked a stream of oil** at cylinder 4's end, down
  to the coil. Cover off that night: **a gasket for another engine**, an open
  arch leaving a hole of about 1 cm into the crankcase.

**Not known:** how much of 3/10's counting was that hole.

## 4/10 — the right gasket, then two sessions

**Morning:** Elring `915.653` on, battery off, 098 run. **Session A, fresh
adaptations:**
- the joint **stayed dry**;
- **014 zero at both warm stops — the first time ever**;
- hot idle `IdleHealth` 60–72, 4.4 dips a minute; felt calmer. August's one
  hot hold graded 48, but lasted 22 s;
- **after five minutes of hard driving, 014 counted at every idle.**

**Afternoon, session B** after a cool-down: **014 counting again**, even on
the idle right after the start. 033 did not correct toward rich.

**Together** (then H10, now `refuted.md` C19): 014 followed **055's learned
idle air value**: above about −0.93 g/s it read zero, from −0.95 on it
counted, warm or cold. One day, a correlation in time; 3/10 counted at
−0.28 with the hole open.

| change | sure it helped? |
|---|---|
| the MAF, 24/9 | **yes** — the rich trim, and smoother engine speed |
| the job of 1–2/10 | **not shown** — both calm hot stops were on fresh adaptations, and on settled ones the hot idle is back where the MAF left it (*this said "probably" until 9/10/2026*) |
| the right gasket, 4/10 | **for the oil, yes**; for 014 **not shown** |
| plugs, leads, injectors, coil | did not fix the idle; the old injectors probably caused the bad cold start, which is gone. The cold burble came back warm on 4/10 (`open.md` S14) |

---

### `IdleHealth` against its own 100, 4/10/2026

*The owner's question: measured the same way, has the 100 moved?*

| state | before the repairs | 24/9, new MAF | 3/10 | **4/10** |
|---|---|---|---|---|
| middle band, ~77–87 °C of oil | **106 (`09`, 11/8)** | 84 (72–85 °C) | 111 (81–91 °C) | **98** (A2), **107** (B1) |
| cold idle, first five minutes | **108 (`18`, 11/9)** | — | — | **121** (A1) |
| hot, ~97 °C | 48 (`11`, a 22 s hold) | 92 | — | **72** (A3) |

- **Against its own 100, the idle has not measurably improved**; cold reads a
  little worse than 11/9 on the old injectors.
- The hot idle improved against 24/9, not past August's one short hold — and
  *(9/10/2026)* that came on fresh adaptations and did not last.

---

## Where it stands, and what comes next

**Open:** S1 and S3, on settled adaptations, new plugs and leads, and an
intake tight cold. **Now** is `open.md`, *Where it stands*; **next** is
`plan.md`.

*Entries are added here as each step is done.*

**9/10/2026 — the exhaust joint behind the converter, resealed** (*owner*;
`photos/exhaust-joint-2026-10-09-old-parts.jpg`,
`photos/exhaust-joint-2026-10-09-new.jpg`). The garage's sealant-filled
joint, rattling since 10/9, remade with a two-bolt sleeve connector and
sealant. A little play: the pipe from the converter is 54.2 mm, the one
behind 55.0 (*owner-measured 12/10; this said the pipe behind was the
narrower*). **For comfort, not the idle**: behind both probes, so nothing is
claimed for S1 or S3 (S6, `refuted.md` D1).

**9/10/2026 — the dipstick guide renewed** (*owner*;
`photos/dipstick-2026-10-09-*.jpg`). The old guide was loose at its foot and
not this engine's part; the metal tube fully home. New guide clicked on,
held by a sheet-metal bracket and a cable tie. Done so the smoke test could
read it; **nothing claimed for S1 or S3**.

**9/10/2026 — the intake smoked, cold** (*owner*;
`photos/smoke-intake-2026-10-09-*.jpg`). Smoke into the manifold, MAF out.
**The back of the intake — plenum, injector seats, hoses — showed
nothing.** One real stream at the dipstick guide; reseated and the bracket
bent, it gave only a faint wisp. Airbox outlet, throttle, filler, cover
joint clean. ⚠ Cold and stopped: a joint that opens only hot is not cleared.

**Then with the old MAF in the hose**: the dipstick clean, **smoke at the
MAF-to-hose joint under the owner's rubber-lined clamp** — or at the rag
closing the MAF beside it; the photo cannot tell
(`photos/smoke-intake-2026-10-09-maf-clamp.jpg`). **With a narrower
all-metal clamp it smoked clean.** Whether it leaked before is not known.

**9/10/2026 — the exhaust smoked, cold.** No smoke, but it would hardly take
pressure. H2 neither found nor ruled out.

**9/10/2026 — the drive on kept adaptations (steps 2b and 2c)**
(`30_step2b_z1`; `open.md` S3, *Steps 2b and 2c*). The first session with
nothing reset. **014 counted** on the cold idle, at both warm stops (6.8 a
minute at 79–85 °C, 11–12 at 94 °C) and home. 055 −1.1 to −1.3 throughout;
003 at a warm idle as on 4/10; 032 −2.3 / +5.5 %. **The dipstick guide and
the MAF clamp did not fix the idle.** The owner felt it calmer at A2; the
grades do not show it.

With all four injectors home the retard and 026's excess **stayed on
cylinder 4** (S4, S5), clearing the injectors from it (`refuted.md` B7); the
knock window stays out of the plan (*owner's decision*).

**Heard** (*owner*): no puff (S2), no bangs (S14); **a constant sputter
close behind the engine**, added as S15 (`refuted.md` D8).

**9/10/2026, evening — the brake servo, checks a and b** (*owner*): it
assists and holds vacuum; a leaking diaphragm not shown by these alone.

**9/10/2026 — H10 closed at the owner's decision** (`refuted.md` C19): the
learned idle air value says **when** 014 counts, not **why**; never tested
by a disconnect. The rule it leaves: a quiet 014 after a disconnect is not a
repair until the learned value has walked back past about −0.93 g/s.

**9/10/2026 — every session since the repairs, compared like with like**
(`open.md` S1). By oil band with adaptations matched, **the MAF of 24/9 is
the only repair that shows on engine speed.** The calmer hot idle of 3/10
and 4/10 came on fresh adaptations and is gone on settled ones. Cover,
throttle, breather, gasket, dipstick, clamp: none known to have changed the
idle.

**9/10/2026 — the dips keep to one cylinder.** In every idle capture since
August, two dips close together fall on the same cylinder's stroke 36 % of
pairs against chance's 25 % (`open.md`, *The dips keep to one slot*). Which
one, the bus cannot say; cutting injectors 1 and 4 became `plan.md` step 3.3.

**10/10/2026 — new plugs and leads, and a new intake gasket** (*owner*,
photographed and numbered by cylinder; `vehicle-history.md`). NGK
`RC-VW254` leads and `BKUR6ET-10` plugs (the same plug type), and **the
upper intake gasket**. Battery connected; adaptations settled. The old
parts: **lead 4's plug end** scored inside over **plug 4's pitted
terminal**; **plug 1 almost loose**. Every old plug end came off far more
easily than the new ones go on (`open.md` H15).

**10/10/2026 — the drive after, the servo held, injectors 1 and 4 cut**
(`31_step4_drive_z1`, `vcds/vcds-step4-*.csv`, `vcds-step5-*.csv`;
`open.md` S3, *The drive after the new leads*). Cold start, servo held twice
on the cold idle, stops at 81–84 and 96–97 °C of oil, the cut test hot.
- **The servo: no dip** — cleared (`open.md` H3).
- **014 still counts**: 3.6 a minute cold (9/10: 1.4–1.8), 9.4 at 81–84 °C
  (6.8), 6.0 hot (10.7–12.5). **Not fixed.**
- **The dips no longer kept to one slot**: 10 of 39 pairs, 26 %, and far fewer.
- 003 hot 3.08 g/s (9/10: 3.12); 055 −1.14 to −1.29. `IdleHealth` hot 77
  (against 89), the same mid, cold 120 (against 95).
- **The cuts named no cylinder** (47–73 s each): dips by name 1: 0, 2: 7,
  3: 11, 4: 2, p = 0.28; air the same with 1 or 4 out.
- **020: cylinder 4's retard nearly gone** — 3 of 1,841 samples, ≤ 1.5°,
  against 44 of 800 and up to 13.5° on 9/10; a gentler drive (`open.md` S4).
- Fault memory after the cuts: P1237/P1240, P0301/P0304, P0300 only — the
  two cut cylinders (`photos/vcds-faults-2026-10-10-after-cuts.jpg`). Cleared.

**Not known:** the new leads did not fix S3; whether they took the
one-cylinder share needs more drives, and the intake gasket changed the
same day.

**10/10/2026, evening — no work; the idles read again, and decisions**
(*owner*). Vacuum gauge ordered; no fuel pressure gauge (H7); both probes
shifted alike written down as H11. Re-read with
`tools/dipcontext.py` (`open.md` S1, *What comes before a dip*): **a dip is
more likely just after the governor has trimmed the charge**. It names no
part. **Not known to have achieved:** nothing was changed.

**10/10/2026 — the joint behind the converter heard again** (*owner*): the
54.2 mm pipe moved in the 55 mm connector even tightened. S6 reopened; a
shim is the fix. Nothing for the idle.

**12/10/2026 — the joint shimmed; the exhaust photographed from below; a
new air filter** (*owner*; `vehicle-history.md`). No engine run.
- **The joint** (`photos/exhaust-joint-2026-10-12-*.jpg`): a strip from the
  old connector wrapped round the 54.2 mm pipe, sealant under and over, the
  connector back on. **Nothing moves**; hangers fine.
- **From below, cold** (`photos/exhaust-flange-2026-10-12-below-*.jpg`,
  `photos/manifold-2026-10-12-*.jpg`, `photos/driveshaft-2026-10-12-below.jpg`):
  nothing seen at the front joint or 3 and 4's pipes; 1 and 2 and the joint
  to the head unseen.
- **The blanked boss is an old probe, leads cut**, behind the front probe
  (`photos/exhaust-blanked-boss-2026-10-12.jpg`). The crank pulley
  (`photos/crank-pulley-2026-10-12.jpg`) and the `038 145 255 A` pulley
  (`photos/pulley-038145255A-2026-10-12-*.jpg`): nothing seen.
- **A new Bosch air filter**, and **a crack in the airbox** ahead of the MAF
  sealed with putty (`photos/airbox-crack-2026-10-12-sealed.jpg`;
  `photos/air-filter-old-2026-10-12-*.jpg`).

**Not known to have achieved:** nothing for the idle — the joint is behind
both probes, the airbox crack ahead of the MAF.

**12/10/2026 — the exhaust test cold, the clutch, and the idle raised and
put back** (`32_step3_item1_z1`, `vcds/vcds-step3-1-*.csv`). Kept
adaptations; cold start, a drive to 95–97 °C of oil.
- **Exhaust test cold: nothing** (*owner*): ten closures, no hiss or puff.
  H2 not refuted — a crack may open only hot.
- **The joint behind the converter: not heard** (*owner*). S6 closed
  (`refuted.md` D1); **the sputter went with it**, S15 closed (`refuted.md`
  D8).
- **The hiss (S11) closed** (*owner's decision*): not heard since 10/10.
- **The clutch makes no difference**: `IdleHealth` cold (~44 °C) down 145,
  up 135, down 145, up 126; warm (97 °C) down 83, up 57, down 45, up 50,
  down 58, up 51 (`open.md` H12).
- **A tick in neutral, cold, pedal up only** (*owner*, heard): added as S16,
  not pursued.
- **The idle adaptation** (`photos/vcds-idle-adapt-2026-10-12-*.jpg`;
  `refuted.md` D9): channel 01 **128 = 780 rpm**; two minutes at each stage;
  136 was saved and **the ECU kept 133 = 830 rpm, its limit**.

  | channel 01 | specified | `IdleHealth` | dips /min (bus) | 014 steps up /min |
  |---|---|---|---|---|
  | 128 | 780 | 61 | 4.9 | ~9 |
  | 130 | 800 | 66 | 2.3 | ~5 |
  | 132 | 820 | 68 | 5.1 | ~4 |
  | 133 | 830 | 68 | 2.6 | ~5 |
  | 133 | 830 | 70 | 3.1 | (detection mostly off) |

  **No stage quieted 014; no trend on the bus.** Put back to 128 the same
  day (`vcds/vcds-step3-1-back128-014-056.csv`).
- **The warm idle calmer than any day before** at the same oil:
  `IdleHealth` 50 and 61, against 77–89 for `30` and `31`. 014 hardly
  moved: 5.3 rises a minute hot, 40 % of samples non-zero (10/10: 6.1, 42 %;
  9/10: 8.8, 58 %). 055 −1.18 to −1.21; 032 **0.0 / +2.3 %**
  (`photos/vcds-032-2026-10-12-after-step3-1.jpg`).
- **The dips keep to one slot again**: 46 of 121 pairs, 38 %, p = 0.0011.
- 001 showed no lean swing before a dip (−0.38 % against −0.48 % quiet;
  `open.md` S1, *What VCDS saw just before a dip*).
- **Evening, cold:** the joint's bolts tightened once more (one moved a
  little). **Lead 4 reseated** — it had felt the least firm; it no longer
  works its way off (*owner*; `open.md` H15).
- **Three original hoses looked at** (*owner*, photographed; `refuted.md`
  A15, C9): the breather hose `06A 103 493 N` split at its cuff, oily, a
  black layer about 0.5 cm thick inside; the shroud supply crazed; **the thin
  hose to the tee by the runners, `06A 133 374`, leaks**, cracked at its
  bend — the one at manifold vacuum. All three to be replaced (*owner's
  decision*). The intake hose `1C0 129 684` leaks nowhere.

**Not known to have achieved:** the raised idle did not quiet 014 and was
undone. Whether the calmer warm idle is the filter and sealed airbox, the
weather or chance is not known.

**14/10/2026 — every hose on, and the vacuum gauge cold**
(`33_step3_gauge_cold_z1`, `34_step3_gauge_2500_z1`,
`vcds/vcds-step3-2-gauge-*.csv`).
- **Reassembly** (*owner*, photographed): new breather hose (Gates
  `EMH118`), the thin hose to the tee and the 8 mm hose to the throttle,
  new clips. The 8 mm hose was sound before clamping.
- **The gauge** (MAR-POL `M57673`) teed in **at the top of the tee by the
  runners** *(this said "into the regulator's hose"; that hose is too
  narrow)*. Its needle rests a quarter-turn off zero. `33` cold (coolant
  16 → 64 °C), `34` part-warm (53 → 82 °C, two snaps, a hold). Off the
  owner's photos and video, against the rest position:

  | moment | true vacuum, inHg (±1½) |
  |---|---|
  | settled idle, ~815 rpm | **about 18–19** — in the green band |
  | throttle opening, ~1600–1700 rpm | about 13, a moment |
  | steady 2000–2150 rpm | about 20–21½ |
  | sharp release from ~2600 rpm | **about 24–25**, back to 19 in ~3 s |
  | gentle release from ~1850 rpm | about 20–21 |

  **Steady and normal** (`open.md`, *How the vacuum gauge is read*): no large
  leak behind the throttle, no valve that does not seal, as far as a gauge
  can say.
- **Flicks**: of three dips in `34`'s filmed idle, **no flick** at the two
  readable ones (resolution about ⅕ inHg). Cold film ~17½ inHg, one dip, no
  finding.
- **`IdleHealth` ~103 on `33`, ~114 on `34`.**
- **The hiss heard again** cold (*owner*): **S11 reopened**; not placed.
- 003's cold air and the cold idle as on earlier days: **nothing sets the
  renewed hoses or the airbox apart**, cold. Idle advance 2–5° BTDC, inside
  VW's 0–12°.

**Not known to have achieved:** the gauge on the plenum cannot see a small
leak at one runner; the idle it read was part-cold.

**15/10/2026 — the can, and the warm idle, still on the remap**
(`plan.md` item 5; `35`–`38`). One can of Liqui Moly *DFI Cleaner* and
about 18 l of OMV MaxxMotion 100, between `35` and `36`. Home (`37`, lights
only, oil 100–101 °C):
- **032 −4.7 / +4.7 %** (12/10: 0.0 / +2.3). A direction, not a finding.
- **055 −1.18 g/s**, settled.
- **003 at the warm idle 3.15 g/s, spread 0.10** (9/10: 3.14, 0.07) —
  unchanged; 12/10's lower charge did not hold. `38`: 3.09.
- **`IdleHealth` 54** at home, **59** over `38` (93–97 °C); as calm as 12/10.
- **014 on 25 % of samples** at the home idle, max 36 (12/10 hot: 40 %).
- **The dips keep to one slot**, 33 % pooled over the day.
- **The gauge warm** (`38`; oil 93–97 °C; 14/10's rest position used):

  | moment | true vacuum, inHg (±1½) |
  |---|---|
  | settled idle, ~800 rpm | **about 19** |
  | hold at ~2490 rpm, 15 s | **about 22**, steady |
  | throttle opening to ~3000 rpm | about 18, a moment |
  | each release, 2300 → idle | **about 22½–23** |

  **No flick** of 0.1 inHg or more in 78 readable seconds; of `38`'s eight
  dips ≥ 20 rpm, seven readable, **none moved the needle**. None at 2500.
- **Off the display, later** (*owner*), oil 100 °C, lights and blower
  step 1: **40–50, once 35**; at home five minutes later **70**. A lead, not
  a change.
- **After the hardest drive yet** (~10 min at 5000 rpm; `refuted.md` D3), oil
  98 °C: lights only **median about 50–55**; A/C and blower **falling to
  23–25**, the lowest on record in any state. At home after, oil 100 °C:
  **about 80 lights only, not below 50 every load on**.
- **The display's `OilTemp` moved to `raw − 60`** the same evening (`mfd15`
  `S-AQY.TRI`); every oil figure since is on it (`docs/firmware/can-decoding.md`
  question 10).

**Not known to have achieved:** the can had been in an hour — a before, not
an after.

**16/10/2026 — a brisker drive, and 014 against the A/C** (*owner*, display
and VCDS 014, no capture). Warm idle after a brisk drive: **`IdleHealth`
about 50–70** at oil 99 °C. **A/C on: 014 zero for several minutes,
`IdleHealth` about 70; A/C off: 014 counting, `IdleHealth` barely moved**
(`open.md` S3, *The A/C switches it*). Across every capture with a 014 log
(`tools/s3align.py`): when 014 counts it counts the dips, but how often does
not follow `IdleHealth` (`open.md` S3, *The events are the S1 dips*).

**One cylinder or two, the same day** (*the owner's correction*: these
files said *one cylinder* where the evidence always allowed two).
`cutscan.py --shares` over every idle since August: **about half the dips
on one cylinder, most of the rest on its firing-order neighbour**; since the
new leads level, 43 and 41 % (`open.md`, *One cylinder or two*). Not the two
on one coil output.

**Not known to have achieved:** nothing changed on the car.

**17/10/2026 — the dips named: cylinders 3 and 4** (*the owner's
insistence* that a stroke's time is known from the engine speed). Counting
hidden strokes keeps the cylinder phase for minutes: one 430 s run across
all four cuts of 10/10 put cylinders 1 and 4 where the firing order says.
Outside the cuts the dips fall **42 % on 4, 31 % on 3**, 14 % on 2, 12 % on 1
(`open.md`, *One cylinder or two*). 16/10's "almost none on the partner"
came from short runs and does not hold.

**Not known:** the names rest on one drive; other captures have no cut.

**17/10/2026 — the idle advance, August against now** (`tools/idleadvance.py`;
`open.md` H14). Steady warm idle, no A/C: **11/8 medians −0.8° and −2.3°**
(after TDC, below VW's 0–12° BTDC); **every log since 24/9 reads 1.5–3.8°
BTDC**. The map did not change between. The baseline for the stock map.

**Not known:** why the ECU took advance away in August.

**17/10/2026 — the can's tank driven, and refilled without one** (*owner*,
display, no capture). Brisk motorway driving; pulled normally. Warm stop,
oil 99 °C: **`IdleHealth` mostly 70–90 loads off** but the lights, **about
40 at its lowest with every load on**. Run down to 1.1 l and **refilled
with OMV MaxxMotion 100, no cleaner**. `FuelAvg` **10.3 l/100 km** before
the fill. Against 12/10's 50–61 and `30`/`31`'s 77–89: **no better**, so no
second can (`plan.md`, Part 2).

**Not known to have achieved:** the can's effect, either way.

**18/10/2026 — cylinder 3 out, cold, and a tick** (*owner*; `refuted.md`
D10). A short gentle drive cold: the engine **ran on three cylinders for a
while**, with a tick at camshaft rate (the owner's video); the clutch did
not change it. **P0303 and P0300 stored** — the ECU's first named cylinder.
Cylinder 3 dropped out again, lamp flashing; **after a restart all four ran
and the tick stayed gone**, `IdleHealth` 60–70 with the A/C on warm. The day
after the cleaner's tank ran out. **Not known**: a flake of deposit, or a
valve or lifter on 3.

**18/10/2026, afternoon — the tick back, warm** (*owner*; `refuted.md` D10).
Fault memory before: P0300 and P0303 twice each, sporadic; cleared; the
drive stored nothing. **The tick came back a few minutes in and stopped by
itself.** `IdleHealth` while it ticked about 120–130, against 80–90 without
(a glance). **014: two bursts under part load, 270 and 351** — nothing above
72 had ever been logged driving. Warm stop, no loads: **mostly 80–90**. **The
owner holds deposits (H13) the most likely.** **Not known**: which cylinder
the bursts were, or whether they matched the tick.

**19/10/2026 — the adaptations after the episodes** (*owner*, VCDS,
engine off; `open.md` S1, *Why the idle got worse*). Fault memory
**empty** after three drives. **032 −3.1 / +5.5 %, 055 −1.27 g/s**, inside
their earlier ranges (`photos/vcds-032-055-2026-10-19-before-6b.jpg`). Warm
idle that day about 100 loads off, about 50 every load on (`open.md` S1).

**Not known to have achieved:** nothing changed; an adaptation learnt in the
misfires is ruled out as the cause of the worse idle.

**19–20/10/2026 — the look inside** (*owner*, borescope, photos off its
screen; `plan.md` item 6b; `open.md` H13 test 3, H15, S18). Plenum off,
ports from above, chambers through the plug holes. A reading of a cheap
screen, not a measurement:

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
unscored. **3 and 4 differ from 1 and 2** in ports, exhaust valves, crowns
and how easily their leads came off. **Only 3 shows deposit come away.**
The plugs: **1 and 4 sooted, 2 and 3 lighter, 3 the cleanest** (*the
owner's reading, 20/10; this said plug 2 alone was light*); the old set of
10/10 sooted 1, 3 and 4. Injector 4's peeling tape renewed; lead 2 torn on
removal.

**Not known to have achieved:** nothing cleaned or changed but lead 2 and
the tape; the camera cannot show whether a valve seals.

**21/10/2026 — the VW plugs and leads** (*owner*; `plan.md` item 6b;
`open.md` H15). Plugs `101 000 033 AA` — the box reads NGK `BKUR6ET-10`,
the plug of 10/10 — then leads `06A 905 409 L`, on the coil 1, 4, 2, 3
clockwise from the top tower, routed clear of the plenum's brackets, 3's
above all (`photos/leads-vw-2026-10-21-*.jpg`). **Every plug end went on
with about the same force, clicked audibly, and sits with no play at
all**; the NGK ends had a slight play on the plug at **3 and 4, and perhaps
1**. The VW ends carry a small rubber ring inside that the NGK ends lack.
The plenum back on a new Elring `271.230`.

**Not known to have achieved:** not yet driven; the first drive is
captured from the laptop.

**21/10/2026 — the first drive after the refit** (`40_refit_drive_z1`,
`vcds/vcds-step6b-*.csv`; `plan.md` item 6b). An hour: a cold start, a
gentle warm-up, the two-state warm stop at 99–100 °C of oil, then half an
hour on with full-throttle pulls and a warm stop at the end. VCDS 014,
001, 003, then 014, 020, 003, then 032 and 055 at the last idle. **Fault
memory empty** before and after each part.

- **The start**: 1.22 s from the first turn to the first firing, 19 °C
  of coolant, no dip after it (`19`: 0.83 s). Felt a little long
  (*owner*); **not pursued** — usual after everything was apart (*owner's
  decision*).
- **Warm stop, split by b7**:

  | state | b7 | `IdleHealth` mostly | lowest |
  |---|---|---|---|
  | loads off (the lights perhaps on by themselves) | 19–24 | 67–79 | 67 |
  | every load on | 37–47 | **34–45** | 34 |
  | loads off again, longer | 23–29 | 60–70 | 50 |

  Loads on, 30–50 was usual before the episodes too (*owner*), so this is
  about where it was before S18, not better. **Felt calmer, with longer
  quiet stretches, though not always** (*owner*).
- **014 at warm idle**: 2.7 and 4.6 rises a minute, 26 % and 43 % of
  samples non-zero (`39`: 7.5, 55 %; `37`: 3.3, 32 %). At a hard zero
  through the loads-on minutes (*owner*, and the log).
- **The dips' shares**: 157 dips, **the top two 58 %, p 0.77** against
  all four alike — the first capture since `24` in which they do not keep
  to a pair (`open.md`, *The dips keep to one slot*).
- **020**: cylinder 4 retards up to 11.2 °CA at full throttle, 4 % of
  samples; 1 a few times, 2 and 3 never. S4 stays.
- **032 −6.3 / +5.5 %, 055 −1.42 to −1.37 g/s** (19/10: −3.1 / +5.5,
  −1.27): more fuel taken away at idle and less air asked for, which a
  sealed leak would do. One reading, on adaptations still settling.
- **Full throttle felt a touch livelier** (*owner*).
- **A hesitation of about a second at 12:21**, full throttle straight
  after the 1–2 change, like fuel starvation (*owner*). **It was the
  traction control**: in that second and nowhere else in the hour,
  0x1A0 b0 goes to 1 and b4–b5 fall from FE to 7A and recover over
  1.6 s, and 0x280 b1 falls below b7 while the pedal stays down; none of
  `19`, `37` or `39` has such an event. **That reading of 0x1A0 is
  inferred from this one event, not documented.** The road was dry; a
  wheel slipping is possible (*owner*). Not a symptom (*owner's
  decision*).

- **Against every settled idle since 24/9** (every stop in each capture,
  not only the measured ones; 30 s windows, run ends trimmed). **Hot, loads
  off** (oil 93–112 °C, b7 ≤ 30): `IdleHealth` 67 ± 2, dips ≥ 20 rpm
  4.6 a minute, ≥ 30 rpm 0.3, the deepest 34, the longest stretch without a
  dip ≥ 20 rpm 52 s, 29 % of the time in stretches of 30 s or more —
  **level with 12–15/10** (`32`: 63, 4.3, 90 s, 39 %; `37`: 62, 4.8, 84 s,
  37 %; `38`: 60, 1.8, 72 s, 59 %) and **well clear of `39`** (80, 10.0,
  22 s, 0 %); not better than the best. **Hot, every load on**: 37, dips
  ≥ 20 rpm 0.7 a minute, 89 % of the time in quiet stretches, the longest
  118 s — the calmest recorded (`35`: 51, 1.0). **Cold** (oil below 60 °C):
  94, dips ≥ 30 rpm none, the deepest 29, against 109–137 and 36–49 for
  every other cold start but `35` (89). Idle speed and its spread
  unchanged (798 rpm).
- **014 against every VCDS log at idle**: the first part, coolant ≥ 85 °C,
  26 % non-zero, 2.6 rises a minute, p90 12, the longest zero 224 s;
  next to 15/10 (`item5-drive-2`: 19 %, 1.5, 256 s) and far from 18/10
  (`drive-home-2`: 55 %, 7.5, 23 s). MAF 3.19 g/s, advance 3.0–3.8 °BTDC
  and lambda 0.0 % at a hot idle, as on every drive since 15/10: **the
  plenum changed nothing the MAF can see**.
- **Full throttle**: b7 on held pulls 173–191, 1–6 counts under `19`, `37`
  and `39`; engine speed rises as fast as on `37` and `39` in 2nd and 3rd.
  **Nothing measured shows the livelier feel, nor contradicts it** — intake
  temperature and grade are not logged.

**Not known to have achieved:** one drive. Whether the shares stay spread
and the quiet stretches last is item 6's to read.

**23/10/2026 — the first 44K tank** (*owner*, display and VCDS, no
capture; `plan.md` item 6a). One can of BG 44K into 23.5 l of OMV
MaxxMotion 100 at 154,501 km; driven warm and hard.
- **After a hard motorway run**, ~70 km in, the everyday state (blower 1,
  one seat heater 1, lights): `IdleHealth` 45–50 between jerks, 70–90 with
  them, never above 100 warm (`open.md` S1, the table).
- **Home through Prague traffic in the evening**, much idling, unsettled
  throughout. Straight after a last stretch held above 4000 rpm in a low
  gear: **37**, the lowest yet in that state, then slowly back to 50 within
  about a minute and above it after another; plain idling took it back to
  70–80. **New to the owner**: after hard driving before, the lowest came
  only after about half a minute. **The captures say the same**
  (`tools/afterpull.py`): without a cleaner the idle after high revs starts
  rough and calms; with Liqui Moly in (`37`) it started calm and rose
  (`open.md` S1, *After high revs*).
- **VCDS afterwards, engine off: fault memory empty.** **032 −3.1 /
  +4.7 %, 055 −1.32 g/s** (21/10: −6.3 / +5.5, −1.42 to −1.37; 19/10:
  −3.1 / +5.5, −1.27): the idle trim back where it was before the refit,
  all inside their history. One reading.

**Not known to have achieved:** the tank is a day old; whether the calm
after high revs is the cleaner, and whether it lasts, needs a capture on a
44K tank.

**24/10/2026 — the first 44K tank run down, the second in** (*owner*,
display, no capture; `plan.md` item 6a). About 170 km out (*owner*;
this said 140 until he corrected it), much of it motorway, **5000 rpm held for long stretches**; oil never above 110 °C.
**No tick, no lamp lit or flashing, nothing wrong felt** over the whole
drive (S18). Part-warm, oil about 60 °C, after one stop: `IdleHealth`
**70–80**, the state not given, so the everyday one; the warm idle was
not read. Run down to 0.4–0.7 l and refilled at 154,755 km: **the second
can of 44K, then 50.88 l of Orlen Verva 100** — no OMV on the route, the
first fill of another brand since 2017 (`vehicle-history.md`). The tank
of 17–24/10 came out at **9.9 l/100 km off the pump**
(`docs/firmware/fuel-check.md`, *The fill of 2026-10-24*).

**S18 closed** (*owner's decision*, 24/10; `refuted.md` D10): no tick,
no three-cylinder running and no lamp on any drive since the evening of
18/10.

**A bad start in the afternoon** (*owner*): after about 4 hours parked
outdoors, nose uphill, the engine **caught and died at once, as if it had
no fuel**; the next start was normal, and none before or after it that
day was bad. The first in about a month. With a tank just filled to 51 l
indicated, a pickup running dry on the slope is hard to make work
(*reasoned*); a rail that lost its pressure while standing would do it
(*general*), and so would a fuel that starts differently, 24/10 being the
first tank of Orlen. One start; nothing shows which.

**The drive back the same evening**, about 170 km again, about 340 in the
day: **about an hour in all above 4000 rpm, much of it held at 5000**
(*owner*). No tick, no miss, no lamp. Pulls well, perhaps better
(*owner*, who calls it possibly placebo); `Power` **about 87 kW** at full
throttle above 5000 rpm, against the 85.4 the scale was set on
(`docs/firmware/frames.md`) — inside the 2 % the tests pin it to, on a cool
day, when b7 reads higher (`CLAUDE.md`, the torque scale's caveats).
**`IdleHealth` 70–80** after 3–5 minutes of warm idle near the end,
everyday state: no change.

**Not known to have achieved:** whether the strong tank did anything to
the idle; no warm reading and no capture on it. What S18 was is not
settled by its absence; it reads for a flake (`open.md` H13).

**24/10/2026, late evening — the phone recording, part-warm** (`plan.md`
item 6c; *owner*). In the garage after the drive, oil 52 → 58 °C and
coolant 57 → 75 °C over it, `IdleHealth` **about 115**. One continuous
85 s recording, injectors 1–4 then the valve cover over 1–4, knuckle
knocks between: six knocks found, the first 20 s unsplit (a knock missed;
taken as injectors 1 and 2 by the order). Idle **810 rpm** off the firing
tone (27.0 Hz). The clicks above 3 kHz, folded at the camshaft's period
(the phase carried through the whole recording off the firing tone):
**one click per firing, all four alike, at every one of the eight
places** — the four-per-cycle component 7–10 % of the level, the
once-per-cycle one at most 1.8 % with its phase wandering place to place,
which is noise. **No cylinder's sound stands out**, not over an injector
and not over the cover at 3 or 4. The phone a few cm off does not single
out the nearest injector either, so injector against injector cannot be
told this way.

**Not known to have achieved:** whether a lifter ticks hot; this was
part-warm.

**24/10/2026, night — the cold capture with one cut** (`plan.md` item 6d;
`41`, VCDS 014/001/003). In the garage, a start at oil 52 °C and coolant
60 °C, neutral, every load off, nothing touched for 4 minutes, **injector
4's connector off for 30 s**, 4 minutes more; 12.6 minutes to oil 82 °C.
**The fault memory before the start held 16556 / P0172, too rich, 35-00**,
the first since 5/2019 (`vehicle-history.md`); after the cut it added
**17648 / P1240, injector 4 open circuit**, and **no P0304 or P0300** —
014 counted through the cut regardless (36–65), and **counts cold**: 12 to
72 in the first five minutes. Both codes cleared by the owner.
`IdleHealth` **123–131** for the first five minutes, **87–104** from oil
73 °C on (`idledips --roughness`, per minute, the cut minute left out).
**The dips: all four alike.** `cutscan --shares`: 124 dips, top two
**55 %**, p = 0.77; `--name` over the run that spans the cut, 137 dips:
**1: 24 %, 3: 31 %, 4: 20 %, 2: 25 %**. Pooled with `40`: 281 dips, 56 %,
p = 0.56. **032 and 055 read afterwards, engine off: 0.0 / 0.0 %, −1.31
g/s** — the lambda adaptations were already reset by the clearing, so the
trims that went with P0172 were not read.

**Not known to have achieved:** what set P0172; the one bad start of the
afternoon and the first tank of Orlen fall in the same window.

**25/10/2026 — where the extra fuel at idle could come from** (`open.md`
H16, H17; `plan.md` 6e–6g). VW's evaluation of block 032 for this engine
(`vcds.md`) lists for a low idle value with part load normal: oil
dilution first, then a leaking injector, high fuel pressure, N80
permanently open, the MAF, the probe. Two candidates written down: **H16**,
N80 not sealing (block 070 of 27/9 showed it opens, not that it seals),
and **H17**, fuel in the oil after weeks of cold idles for the captures.
**Read off the car** (*owner*): the dipstick on 24/10 where it was at the
last top-up, about 1 mm over the upper mark — no rise to see; the tank is
never filled past the first click, the fill of 24/10 included; the
"filler cap off at idle, slightly worse" of 25–27/9 was the oil filler.

**Not known to have achieved:** nothing changed on the car; whether either
source exists waits on 6e–6g.

**Later the same day — the regulator's vacuum hose** (*owner*;
`open.md` H7). Followed up because a hose that does not carry the
intake's vacuum leaves the rail high at idle, VW's "fuel pressure too
high". **Found: its intake end breaking up** — the wall parted into
layers with voids between them, a crack from the bore outwards
(`photos/fpr-vacuum-hose-2026-10-25-end.jpg`, `-side.jpg`) — no clip on it since 6/2026, off
and on with every intake job, and at least once left on while the
intake came off, which pinched it — the crack from about September
(*owner*). Blows through
freely. A split there pushes rich (H7); the first part found that fits
032's shape. To be renewed with clips (`plan.md` 6e).

**For the days until the new one** (*owner*): the cracked end cut back by
about 1 cm, all the slack allowed
(`photos/fpr-vacuum-hose-2026-10-25-cut-piece.jpg`), and the hose turned
round so that end sits on the regulator. **The fresh cut still shows the
crack from the bore** (`…-after-cut.jpg`). A leak into that hose acts on
the regulator wherever along it it is (*reasoned*), so the turn moves it
away from the intake without making it smaller; only the shorter crack
can. 032 is read before the new hose goes on, once enough driving has
passed since the clearing of 24/10.

**Not known to have achieved:** nothing fitted yet; whether the cut
changed `IdleHealth`.

**25/10/2026 — the cold start died at once again** (*owner*): the first
start of the morning, **after about 12 hours on the level in the garage**,
caught and died, the second ran — so the slope of 24/10 was not needed. The second since the
fill of 24/10 and the rule of `refuted.md` D2 reopens **S7** (`open.md`).
Priming on alternate mornings, `StartCrank` and `StartDip` off the display
(`plan.md` 6h).

**25/10/2026, evening — the regulator's vacuum hose renewed** (*owner*;
`open.md` H7; `plan.md` 6e). About 10 km on the cracked hose since the
clearing of 24/10. At a running idle the old hose pulled off for **a few
seconds**: **vacuum on the intake's side**, **no fuel at the hose's
regulator end and no smell of it** (*owner*, 25/10), and `IdleHealth` **70 → about
120 at once** — with the hose open, so a vacuum leak and the regulator at
full pressure together, and no reading of either alone. **Then**, engine
off: **fault memory empty; 032 −8.6 / +3.9 %**, the most negative idle
value on record; **055 −1.25 g/s**
(`photos/vcds-faults-2026-10-25-before-new-fpr-hose.jpg`,
`vcds-032-055-2026-10-25-before-new-fpr-hose.jpg`). *Corrected 25/10 (the
owner): this put the reading before the hose came off.* **So the −8.6 may
carry those seconds** (*the owner*). How much is not known; against much
of it (*reasoned*): the open hose pushes both ways at once — unmetered air
lean, the rail at full pressure rich — and in 6i the idle cell moved
3.9 points in about six minutes of idle, a fraction of a point in a few
seconds at that rate. Nothing earlier bounds it from the other side:
032 relearnt from 0.0 after 24/10's clearing, so "the most negative on
record" (before: −6.3, 21/10) holds only as far as those seconds are small.
**The new hose** (STARLINE 4 × 8 mm) cut fresh at both ends and fitted
**with a spring clip at each end** (`photos/fpr-vacuum-hose-2026-10-25-fitted.jpg`).

**Not known to have achieved:** 032 on the new hose after some drives;
the cold starts (S7).

**25/10/2026, the same afternoon — the first idle on the new hose**
(`plan.md` 6i; in the garage, MFD in, no capture; Claude logged 014, 001,
033 from the start, `test/fixtures/vcds/vcds-step6i-warm-idle-*.csv`).
Restarted warm: **oil 77 °C, coolant 84 °C** before the key. The owner
did not wait for 90 °C of oil; the two states were taken at **oil about
80 °C**, coolant 90 → 96 °C, so `IdleHealth` compares only loosely.

| state | rpm | lambda regulation, 001 / 033 | `IdleHealth` (*owner*) |
|---|---|---|---|
| first 37 s after the start | ~1100 | +7.7 % | 120 |
| every load off, first ~85 s | 781 | **+6.5 %**, steady (+3.9 … +9.4) | 120 falling to **about 90**, where it held |
| every load off, the next ~65 s | 772 | **+6 → −10 % → −1 %** | |
| every load on, 2½ min | 783 | **+0.5 %**, ±2 around zero | **35–40** for long, lowest **35**, rising to 45–50 at the end |
| loads off again, 14 s logged | 769 | −0.2 % | 130 at once, then **about 90** |

*This table gave the loads-off state as one figure, +2.4 %, the mean over
both of its halves (corrected 25/10, from the log sample by sample).*

- **The regulation sat positive for the first minute and a half**, as the
  hose's effect predicted: the ECU was giving back fuel the adaptation had
  learnt to take away.
- **Then it fell through zero to −10 % within about 50 s** (−11.7 % in
  001 at its lowest, ~165 s after the start) **and came back to about −1 %**,
  coolant steady at 94.5 °C, nothing touched. **It settled about 3 points
  richer than it began**: adding the live regulation and the idle cell as
  if they were one percentage (*an approximation*: the idle cell is
  additive, the regulation a factor), the engine wanted about −2 % in the
  first minute and a half (−8.6 + 6.5) and about −5 % from then on
  (−4.7 + 0 … +0.5, loads off and on alike). **The idle cell relearning
  cannot make that by itself** (*reasoned*): moving it 3.9 points towards
  zero takes 3.9 out of the live regulation, +6.5 → about +2.6, not to
  −1. **Something brought about 3 points of fuel two minutes into a warm
  idle.** The canister purge starting is the obvious candidate, a day
  after a fill (`open.md` H16; *reasoned, not shown*); when 032 moved was
  not logged, so this log cannot tell the two apart. 6f's closed purge hose,
  with 032 logged beside the regulation, can (`plan.md`).
- **The probe switches**: 033 field 2 crossed 0.45 V at least 36–50
  times a minute in every state, rich and lean about half each — a lower
  bound, since VCDS samples each block only every 0.9 s. VW asks for 20
  (`plan.md` 6f); that half of 6f's probe check is passed. 030 was not
  logged.
- **032 had already moved, read at the idle afterwards: −4.7 / +3.9 %**
  against −8.6 / +3.9 on the cracked hose — the idle cell relearnt about
  half-way in one sitting, the part load untouched
  (`vcds-step6i-adaptations-032-055.csv`; 055 −1.21 g/s).
- **014 read 12 on and off for the whole first loads-off state** — at
  1200–1360 rpm after the start, then at 760–800 rpm warm, 24 twice
  (~114 and ~124 s) and 13 at the switch to loads on — **and 0 from
  ~191 s to the end**, every load on and the 14 s of loads off logged
  after. *This said "12 in the first ~25 s, then 0 to the end" (corrected
  25/10, from the log).* So 014 went quiet with the loads on, where
  `IdleHealth` was lowest; it stayed out of 0–5 loads off (`vcds.md`).
- **Fault memory empty** before and after. **Nothing cleared.**
- **No jerk felt in the seat** at any point, `IdleHealth` high or not
  (*owner*; `open.md` S1).

**Not known to have achieved:** a smoother idle — loads off at about 90 is
where it has sat warm before (70–90 at 99 °C of oil, 17/10), so the
roughness is not shown to have moved; the cold starts (S7); 032 after some
drives; **a lean idle** — the engine still wanted about −5 % warm once the
regulation settled, so the hose answers part of the rich idle, not all of
it.

**25/10/2026, evening — 014 at a warm idle on the new hose** (`plan.md`
6j; a drive, MFD in, no capture; Claude logged 014, 001 and 032 from
before the start, `test/fixtures/vcds/vcds-step6j-*.csv`). **Not in the
planned state**: the owner kept the everyday load (one seat heater on 2,
the blower on 1, lights) rather than every load off. On 6i 014 read 0
all through every load on, so this state does not flatter it.

| stop | length | coolant | 014 | lambda regulation | `IdleHealth` (*owner*) |
|---|---|---|---|---|---|
| a light | 78 s | 92–94 °C | **12 twice**, 5 s and 13 s | about +2 %, one swing to +28 % for 3 s | |
| a light | 34 s | 92–94 °C | **0 throughout** | about −0.5 %, ±2 | 50–60 |
| the stop, oil 96 °C | 4.7 min | 94–99 °C | **12 ten times**, 1–13 s each, **24 twice and 36 once** near the end | about −1 %, ±2, no step | **70–80** |

- **014 still counts warm on the new hose**, in a loaded state, and more
  towards the end of the long stop than at its start; the quiet stretches
  between ran 20–80 s. **So the hose did not take the counted misfires
  with it** (`open.md` S3), whatever the feel of the drive before.
- **It counted while driving too**: 12 at a steady 2200 rpm for 8 s, and
  13 over 800–1760 rpm for 15 s.
- **The regulation made no step** like 6i's fall to −10 %, at any stop:
  the purge, if it is what moved 6i, did not show here.
- **032 is back to −7.8 / +6.3 %** (−7.8 / +5.5 at the key; the part-load
  cell moved during the drive): from 6i's −4.7 / +3.9 on the same
  afternoon, **the idle cell returned to about where it stood on the
  cracked hose** (−8.6). 055 −0.06 / −0.97 g/s
  (`vcds-step6j-adaptations-032-055.csv`).
- **Fault memory empty** before and after. **Nothing cleared.**
- **The owner, by ear**: in the calmer stretches the engine speed drops a
  little and holds there, calmer (`open.md` S1). VCDS reads engine speed
  in steps of 40 rpm, and the stretches with 014 and without it both sit
  at 760–800, so this log neither shows nor contradicts it.

**Not known to have achieved:** anything for the idle. The rich idle trim
is not answered either: 032's idle cell ran back to −7.8 within a drive.

**25/10/2026, night — N80 and the regulator, on a cold start** (`plan.md`
item 6e; in the garage, MFD in, no capture; Claude logged 032, 055 and 030
before the start, then 001, 032 and 033 from the start to the end,
`test/fixtures/vcds/vcds-step6e-*.csv`). Coolant 34.5 °C at the key,
neutral, every load off. The event times below are the owner's messages,
so a few seconds late; the steps in the log lead them.

- **Before the start: fault memory empty, 032 −7.8 / +7.8 %**, 055
  −0.96 g/s. 030 was read with the engine off, `000 000`, which says
  nothing about the probe.
- **N80 blown through towards the intake, engine off, the tank-side hose
  off: it passes, "but really little"** (*owner*). By 6e's rule that is
  a valve that does not seal.
- **Started with a finger on N80's open port: no suction at all**, then
  **the pulses came**, and **no liquid fuel** at the port or the hose
  (*owner*); the hose went back on. So the leak blown in at rest is too
  small for a finger to feel against the running intake's vacuum.
- **The lambda regulation came on about 90 s after the start**, at 51 °C
  of coolant, and **with the canister cut off by the finger sat at
  −0.7 % on average** until the pulses — with 032's −7.8 still in force.
  **So the engine wanted about 8 % less fuel at idle with nothing coming
  through N80 at all**: the fuel behind the negative idle trim does not
  come from the purge path, at least tonight (*reasoned*; that the ECU
  applies the learnt idle value already at this temperature is
  *general*, not shown for this ECU). The designed purge, once the hose
  was back, showed no step either (about +0.2 % for the 80 s before the
  regulator test).
- **The regulator's hose off at the intake end, the tube closed, twice
  for about 40 s**: the regulation went **to −8.6 and −10.2 % within
  seconds**, averaging **−3.7 and −6.3 %** over each window while 032's
  idle cell learnt part of the step away (−7.8 → −12.5 the first time);
  **back on, +3 to +8.6 %** each time, settling near zero, the idle cell
  back to −8.6. **The step of about 8 % the regulator owes its
  reference, twice.** **No fuel at the hose's free end** either time
  (*owner*).
- **`IdleHealth` 120–140** off the display, cold, oil under 70 °C
  (*owner*; the planned test read none) — as 6d's cold 123–131 (24/10);
  not a new observation (*owner*).
- **After: fault memory empty; 032 −8.6 / +7.8 %**, 055 −0.06 /
  −1.16 g/s (`vcds-step6e-adaptations-032-055.csv`). **Nothing cleared.**

**Not known to have achieved:** a source for the rich idle trim — it is
neither N80 nor the regulator's reference; H17 and an injector are left
(`open.md` H7, H17). Whether N80's small leak at rest is what floods S7's
starts — the valve is **not replaced** (*the owner's decision*, 25/10:
it helps neither the idle nor the trim); 6h's priming reads S7 without
it.

**26/10/2026 — the cold start, plain, off the display** (*owner*;
`plan.md` 6h). About 10 hours in the garage, about 12 °C there (*owner's
estimate*; nothing read off the display before the start), **not
primed**. The starter held until the engine caught, **about 4 s** by
his count; **it did not die**. **`StartCrank` 1.22 s, `StartDip`
218 rpm, `StartClt` 24 °C.** The deepest `StartDip` on record (11/9's
near-stall on the old injectors: 141; the clean starts of 24/9–3/10:
15–118) and a crank to first firing level with 11/9's. Read as
(*reasoned*): `StartCrank` ends at the first 400 rpm, so it fired at
1.22 s and fell back about 218 rpm, to cranking speed, in the next 2 s —
the catch and die of 24 and 25/10, carried this time by the starter;
the 4 s are to running, not to first firing. The third bad start since
the fill of 24/10 (`open.md` S7). A coolant of 24 °C after 10 hours in
a garage of about 12 °C: either the engine had not cooled to the garage
or the garage was warmer than guessed; either way warmer than 11/9's
16 °C. The next cold start is primed.

**26/10/2026 — 032 before the oil change** (`plan.md` 6g; *owner*;
`photos/vcds-032-055-2026-10-26-before-6a.jpg`, cropped to the VCDS
window). Engine off, ignition on, before any EPR: **032 −8.6 / +7.8 %**,
**055 field 3 −1.14 g/s**; **fault memory empty** (*owner*); **nothing
cleared**. 032 the same as after 6e on 25/10 night (−8.6 / +7.8), across
the day's drives; 055 −1.16 then. This is 6g's *before*; the *after* is
032 at about 200 km on the new oil.

**26/10/2026 — the phone recording, hot** (`plan.md` 6c; *owner*). On
the old oil, straight before the first flush, **oil 100 °C**. One
continuous 82 s recording, injectors 1–4 then the valve cover over 1–4,
**a double knuckle knock between places: all seven found**, so every
place is split by its knocks, not by the order. Idle **790–800 rpm** off
the firing tone (26.3–26.7 Hz). Read as on 24/10: the clicks above
3 kHz folded at the camshaft's period, the phase carried off the firing
tone. **One click per firing, all four alike, at every one of the eight
places**: the four-per-cycle component **15–17 %** of the level
everywhere (7–10 % part-warm on 24/10); the once-per-cycle one **1.4–4.2
%**, against 1.0–3.3 % folded at a wrong period (the noise floor), its
phase not repeating from place to place and over cover 1–4 **2.4, 2.7,
3.3, 2.9 %** — no cylinder standing out. The mean level the same at all
eight places, so the phone hears the whole bay and not the part under
it, as on 24/10. ⚠ The firing tone slipped about one firing between
injector 3 and 4, so a once-per-cycle phase cannot be compared across
that join; it sat at the noise floor anyway. *The analysis was an
ad-hoc script, not kept, as on 24/10.*

**Not known to have achieved:** nothing changed on the car. **Hot, no
lifter ticks** at camshaft rate over any cylinder, which the part-warm
recording could not say; by `plan.md`'s own reading, all four alike makes
the flush an oil change with an additive for the idle.

**26/10/2026 — the first EPR flush, and P0507** (`plan.md` 6a; *owner*;
the full entry follows when the change is done). At **154,999 km**: the
first can of EPR, **30 minutes at 1250–1300 rpm**, standing, the pedal
held by a stick; no tick. Drained hot; **the old filter was a VW
original**; the Bosch `0 451 103 314` on (the same seal and thread, a
different top plate), the old drain plug back at 30 Nm, fresh oil to the
mark, no leak at the start. **The engine lamp lit in the warm-up for
the second flush**: fault memory **16891 / P0507, idle speed above the
target, 35-10, sporadic**
(`photos/vcds-faults-2026-10-26-p0507-flush.jpg`, cropped to the VCDS
window). Read as the stick (*reasoned*): the speed held about 450 rpm
above the idle target for half an hour, standing, at a plate barely off
its stop.
**Before the clearing** (`photos/vcds-032-055-2026-10-26-after-flush1.jpg`,
cropped): **032 −8.6 / +8.6 %** (+7.8 before the flush), **055 field 3
−2.10 g/s** (−1.14 before), **outside VW's −1.50 to +1.50**
(`vcds.md`). Read as the same stick (*reasoned*): the idle stabilisation
took air away for half an hour against a speed it could not bring down,
and learnt it. The clearing of 24/10 left 055 alone (−1.31 after it), so
it is expected to relearn by itself over ordinary idling; a warm
`IdleHealth` until it has is read with that in mind. Fault memory then
cleared by the owner.
**The first drain** (`photos/oil-drained-2026-10-26-flush1.jpg`,
cropped clear of the reflections): the surface dark, glossy and even,
**no foam, no milky emulsion, nothing floating**. The sky's reflection
hides the colour and the depth, so it says nothing of sediment.

**The week of 19/10/2026 — the valve cover nuts re-tightened** (*owner*,
reported 26/10; `plan.md`'s standing item after a few hundred km on the
new gasket, now done and removed). Nothing claimed for the idle.

**26/10/2026, evening — the second flush and the new oil** (`plan.md` 6a;
*owner*). The second can of EPR at 90 °C of oil, **30 minutes at
1220–1300 rpm**, the stick again; no tick. The second drain black, which
is the deposit EPR dissolves (*general*). **The VW filter `06A 115 561 B`
and the new VW drain plug, about 30 Nm; Total *Quartz 9000 Energy* 5W-40,
about 4 l**; no leak at the start. **Done at 154,999 km**: two EPR
flushes, the Bosch filter between, the sample and the rinse dropped.
**The underside oily**, the sump's rear the wettest, before the change
too (`open.md`, *Other*).

**After the second flush** (`photos/vcds-faults-2026-10-26-after-flush2.jpg`,
cropped): **16891 / P0507** again, sporadic, and **17990 / P1582, idle
adaptation at its limit, 35-00** — both the stick (*reasoned*): the idle
stabilisation went on learning against the held speed until it ran out
of range. Both cleared by the owner; the adaptations were read only
after the clearing and a short idle to look for leaks
(`photos/vcds-032-055-2026-10-26-new-oil.jpg`): **032 −1.6 / 0.0 %** (the
clearing's reset and a minute of relearning, not 6g's *after*), **055
field 3 −2.78 g/s**, further out of VW's −1.50 to +1.50 than after the
first flush. **055 is not reset by a clearing** (24/10), so it has to
relearn by itself over ordinary idling; until it has, a warm
`IdleHealth` and the idle's feel are read with it in mind, and **P1582
coming back on the road** would say it has not.

**Not known to have achieved:** anything for the idle — read on the new
oil with 6g's 032 at about 200 km, `IdleHealth` cold and warm apart, and
6i's dipstick.

**26/10/2026, night — P1582 kept coming back, the battery disconnected
and 098** (*owner*). On the first short drive on the new oil, **without
the stick, the lamp came back with 17990 / P1582**, and **the engine
nearly stalled after a warm start** — twice that evening. Read as 055's
−2.78 g/s (*reasoned*): the idle running with that much air learnt away.
**The battery off for about a minute**, then 098 under basic settings,
ignition on: **"ADP v pořádku" at once, the throttle not moving**
(5.6°, G127 71.8 %, idling; `photos/vcds-098-2026-10-26-after-disconnect.jpg`)
— read as the adaptation done by itself at the first ignition-on after
the reconnect, as this throttle does at every ignition-on (S13): **no
sound from the throttle under 098, only its usual routine at
ignition-on** (*owner*). Or 098 did not really run, with P1582 still
stored against VW's condition of an empty fault memory. *(27/10: it did
not — the owner had opened 098 as a measuring block, not under basic
settings; the same happened on 27/10.)* Then
(`photos/vcds-032-055-2026-10-26-after-disconnect.jpg`): **032 reset to
0.0 / 0.0, but 055 field 3 still −2.78 g/s**, and **P1582 still stored**
(the disconnect does not clear the fault memory). **Nearly stalled again
after the start.** So a disconnect of a minute reset 032 and not 055 —
whether a longer one, or 098 run with the fault memory empty (VW's
condition), resets 055 is not known; on 4/10 a disconnect and 098 left
it near zero (`refuted.md` C19). Left for now (*owner*, he had to go).
**Every start and idle until 055 is back is read with it in mind** —
6h's starts above all.

**26/10/2026, later — 055 learnt itself back** (*owner*, VCDS 014/055/001
logged, `LOG-01-014-055-001.CSV` on the laptop; warm idles, coolant 96 °C).
**055 field 3 walked back on its own over the idling: −2.78 → −2.08 →
about −1.8 → −1.52 → −1.24 → −0.97, settling at −0.90 / −0.91** with
field 2 swinging about ±0.1 g/s (`photos/vcds-032-055-2026-10-26-relearnt.jpg`,
cropped). **032 still 0.0 / 0.0** — not yet relearnt after the
disconnect. So no longer disconnect was needed. The settled value sits
**above the −1.1 to −1.3 of 9/10–26/10, and just above C19's −0.93**.
Off the display along the way (*owner*): `IdleHealth` 55–60 at 62 °C of
oil; about 100 warm with 014 counting (12) and the learnt value at about
−2; 60–79 straight after the A/C was switched off; **with the A/C on,
055 field 3 read 0** (*owner*: the ECU may not take the A/C idle for the
same idle); 45–50 straight after every load went off, rising slowly
over minutes — slower than the display's own filter (about 10 s,
`src/config.h` `IDLE_CONVERGE_S`), so the engine and not the display.
**The log** (`test/fixtures/vcds/vcds-step6a-055-relearn-014-055-001.csv`,
37 minutes, from the start through the drive to the end of the idling):
- **055 field 3 learns only at a warm standing idle** — with 001's
  basic-setting requirements all `111111` — and holds still through
  every stretch of driving: −2.78 for the first 12 minutes of mixed
  driving, then down in steps at each idle, field 2 at about +1.0 to
  +1.3 g/s while it learnt, falling towards 0 as it arrived.
- **Field 3 reads exactly 0.00 whenever 055's load bits read `0101`**
  (and 001's first requirement bit drops to 0) — the owner's A/C and
  all-loads stretches — and returns to the learnt value when they go
  back to `0000`. So with those loads on, the ECU does not use (or does
  not show) the learnt idle value at all. Which bit is the A/C was not
  separated.
- **014 counted at every value the learnt value passed through**:
  counter non-zero for 35 % of the warm idle at −2.2 to −2.8, 49 % at
  −1.9 to −2.2, 19 % at −1.4 to −1.9, 31 % at −1.1 to −1.4 and **37 %
  at −0.97 to −1.1**, the counter in steps of 12 up to 60. No trend with
  the learnt value; the log ended at −0.97, still below C19's −0.93, so
  **whether 014 goes quiet above it is not yet tested** — the settled
  −0.90 is the next session's to read.

**Then** (*owner*): the fault was stored again in the course of it
(P1582, read as the learnt value still out of range when it set); **cleared
by the owner once 055 had settled**, and **the next start was normal —
no dip, no fault**; **two more starts after it, both clean, the lamp
off** (*owner*). 032 was already at zero from the disconnect.

**27/10/2026 — the cold start, primed** (*owner*; `plan.md` 6h). About
11 hours in the garage, 18 °C there; oil 27 °C and coolant 24 °C off the
display before the start; **primed four times** rather than the plan's
twice. **Not a clean start**: he held the starter well past the first
firing, it cranked long, ran, and **hesitated for a while**.
**`StartCrank` 1.18 s, `StartDip` 0, `StartClt` 24 °C** (`open.md` S7)
— the display's measures end at the first firing and 2 s after it, so
they miss a stumble carried by the held starter. **His reading**: before
the new injectors priming always made it catch at once without a
hesitation, and today it did not, so this is not the rail draining while
standing. The next cold start is plain.

**27/10/2026 — the oil topped up** (*owner*; `plan.md` 6i). The level
fell overnight after the change of 26/10 as the oil ran back from the
head; **about 0.4 l added** in the morning, at the top mark straight
after; **155,024 km**. After the drive below, about 10 minutes standing:
**exactly at the top mark** (*owner*; photographed at 08:02, about
11 minutes after engine off, `photos/dipstick-2026-10-27-6i-first.jpg`).
That is 6i's first reading.

**27/10/2026 — the A/C at a warm stop** (`plan.md` 6k; *owner*, display
on video; VCDS 014/055/001 the whole drive,
`test/fixtures/vcds/vcds-step6k-014-055-001.csv` the start and
`vcds-step6k-2-014-055-001.csv` the rest). Fault memory empty before and
after. A gentle drive to about 88 °C of oil, `IdleHealth` about 90 at a
3-minute stop on the way, then 40–60 at the idles of 20–30 minutes more;
then, standing, neutral, nothing else touched:

| from | state | `IdleHealth` (video) | 014 | 055 bits | field 3 | field 2 |
|---|---|---|---|---|---|---|
| 07:23 | everyday | **~70** (59–73) | 12–48, then **0 → 72** in the 15 s before the A/C | `0000` | −1.11 → −1.04 | about 0 |
| 07:25:31 | + A/C, first minute | 59 → 45 | 0 | `0101` | **0.00** | → −0.99 |
| 07:27 | + A/C, minutes 2–5 | **35–50** | 0 | `0101` | 0.00 | about −1.0 |
| 07:31 | + A/C, minute 6 | **56 → 75** | 0 | `0101` | 0.00 | about −1.0 |
| 07:32:30 | + A/C + every load but main beam | **35 → 25** | 0 | `0101` | 0.00 | −1.28 |
| 07:38:41 | everyday, A/C off | — | 12 within a minute | `0000` | −1.04 | 0.00 |
| 07:40:18 | every load but the A/C and main beam | **54–62**, 37 at the end | 12 ×3, then 0 | `0000` | **−1.04 → −0.77** | +0.23 |
| 07:44:30 | + A/C, driving, then standing | ~51 (48–60) | 0 | `0101` | 0.00 | frozen driving, about −1.0 standing |

**`0101` is the A/C.** With it on, field 3 holds 0.00 through minutes
of idle and a drive, and field 2 takes over the learnt value's size: no
second learnt value showed. Every load but the A/C leaves the learnt
value in play, and **it relearnt by +0.27 g/s in those two minutes** —
back to −0.81 when the loads went off. Main beam left off throughout (the
owner would have dazzled the traffic). `IdleHealth` filters, so each state
reads about half a minute late. Read in `open.md` S1, *A second
reading*, and H8.

**On the drive before it, 014 counted on the road**: two climbs in
steps of 12, 12 → 36 and 12 → 48, at 1900–2100 rpm and 25–26 % load, and
four shorter counts (12, once 12 → 24) at 1160–1920 rpm and 25–30 % load,
detection `aktivováno` at each (*re-read 27/10*); the
owner saw it count at the jerk he feels when the throttle goes back on
after a gearchange. **S12 reopened** at his request (`open.md`).

**Then, A/C still on, engine running** (`vcds-step6k-adaptations-032-055.csv`):
**032 −6.3 / +8.6 %** (−8.6 / +7.8 on 26/10 before the change; 6g's
*after* is at about 200 km on the new oil, this is on the way), 055
field 3 0.00 with the A/C. Nothing cleared; nothing to clear.

**Not known to have achieved:** nothing changed on the car. 6k gave
neither of its clean outcomes: the A/C's calm is the larger, but the
loads calm without it too, and the A/C's sixth minute was not calm.

**27/10/2026, late morning — the throttle cable slackened** (*owner*).
Taken up to the stop on 1–2/10, and the very top of the pedal's travel
no longer felt right to him; he reads S20's swing, the flush's too, as
the cable holding the plate off its rest. **054 after it: about 5° at
rest, 90° on the floor** (2/10: 5.6° and 91.1°), so the plate still
rests and still opens fully. **098 at once *ADP OK*, the throttle
silent** — as on 26/10, when 055 did not reset. **Both times 098 was
opened as a measuring block, not under basic settings** (*owner*, the
same afternoon), so *ADP OK* was the stored state being read and no
adaptation ran; *this said the ECU appeared to skip the run*. **Then the battery
off, both poles, for several hours**, to reset 055: in this car 055 went
to zero each time 098 really ran after a disconnect (2/10, 4/10) and
not on 26/10, when it did not (*reasoned* from those three, not from VW).
In the afternoon: reconnect, 098, then 032 and 055 read.

---

## Appendix — the job of 1–4/10 in detail

*Moved from `vehicle-history.md` on 4/10/2026. The full checklist is in git
(`plan.md` before 3/10/2026).*

### The valve cover and throttle job

*By the owner, at home, every item photographed.*

**Done.** **Injectors refitted one by one**, rail at 10 Nm, cylinder 2's
O-ring replaced; all four flush (photographed). Leads ~6 kΩ each; injector
windings 15.9 Ω each. **New cover gasket** with Dirko at the arch points,
nuts about 4 Nm at most. **New plenum gasket** and **new throttle**, 10 Nm;
the vacuum elbow replaced by a longer hose. **New breather**, `100690` in
the old cap. Throttle cable slack taken up.

**Found:** the old breather **loose on a ring flowed out of shape**
(`refuted.md` A15); **six of eight cover nuts loose by hand** over a gasket
gone **hard, almost like plastic** (`refuted.md` D5); the vacuum elbow hard;
the old throttle's idle switch **silent**, its idle-stop face **worn 1–2 mm**
(`open.md` H8). Sound: both plenum gaskets, the June throttle gasket, the
plenum face, the rear hoses, every injector connector, no emulsion. The
patch on the old breather is original (`refuted.md` C15).

**Before the first start, 2/10/2026.** **098 *ADP OK*** (10.4°, 59.2 %).
The ignition-on routine **still 20 s**, closing S13 (`refuted.md` D7, C16).
**054: 5.6° at rest, 91.1° to the floor**, inside VW's figures. Battery
reconnected, every adaptation from zero (055 0.00); no VCDS reset.

**The check start, 2/10/2026** — standing, part-warm, no capture
(`test/fixtures/vcds/vcds-postrepair-checkstart-003-014-055.csv`). Fault
memory empty; **no leaks**; the idle as `19`'s (794 against 798 rpm, air
3.96 against 4.28 g/s). **014 counted 13 twice**, then nothing. `IdleHealth`
**57 at its lowest** that evening, every load on, fresh adaptations. **A
ticking at the timing-belt end** went once the belt cover was refitted; the
belt end dry (*owner*). **No hiss at the back**, cold or part-warm.

**The first warm run, 3/10/2026 — the cover leaks at cylinder 4's end**
(`open.md` S3, *Session A*): **oil "in a stream" at the half-moon at the
gearbox end**, about 20 min in, down to the coil (*owner*;
`photos/cover-leak-2026-10-03-cyl4-end.jpg`,
`photos/cover-leak-2026-10-03-below.jpg`). About 0.5 l topped up.

**The wrong gasket, the same night.** **The part, not the fitting**: Elring
`325.070` has **an open arch leaving a hole about 1 cm across** where the old
one had **a solid, ribbed half-moon**, and no metal sleeves (*owner,
photographed side by side*). It is listed for AZJ, BER, AZG and AEG, not
AQY; `915.653` is AQY's (`refuted.md` C17, D5). **About a litre** had run
down to the driveshaft (*owner*).

**The right gasket in hand, 4/10/2026.** Elring `915.653`, solid ribbed
half-moons and metal sleeves (`photos/cover-gasket-915653-halfmoon.jpg`,
`photos/cover-gasket-915653-whole.jpg`); number on the label, EAN
`4041248115435` (`photos/cover-gasket-915653-label.jpg`). Leads dry; **oil
on one part of the coil** (*corrected by the owner; this said dry*); boots
and plugs clean (`photos/cover-leak-2026-10-04-cleaned.jpg`). **Cover back
on**, nuts felt seating on their sleeves (`photos/cover-on-2026-10-04-*.jpg`);
**plenum back on, the job complete** (`photos/plenum-on-2026-10-04.jpg`).
About 1 l topped up in all; cold, the dipstick about 0.5 mm below the mark.

**The first warm run after step 1b, 4/10/2026.** 098 OK (*owner*). (`open.md`
S3, *Session A after step 1b*.) **The joint stayed dry**; the smoke was 3/10's
oil burning off. The hiss remained (S11). Fault memory empty; 032 −0.8 /
+2.3 % (`photos/vcds-032-2026-10-04-after-sessionA.jpg`). **The belt noise
gone** — most likely the belt rubbing its cover with the cover sitting low
on the wrong gasket (*owner*); the belt checked and fine.

**Session B the same afternoon**, after a cool-down to 47 °C of oil: the
misfires back at B1 and after the start (`open.md` S3, *Session B*;
`refuted.md` C19).

**The starts measured from the capture** (`tools/idledips.py`;
`docs/firmware/frames.md`, *The start*). ⚠ Only a near-stall or a crank past
1.2 s counts on its own.

| | stand | coolant | crank to first firing | `StartDip` |
|---|---|---|---|---|
| 11/9 (`18`), old injectors | ~10 h | 16 °C | 1.22 s | 141 rpm, nearly died |
| 24/9 (`19`) | ~19 h | 12 °C | 0.83 s | 118 rpm |
| 25/9 | ~12 h | — | 0.77 s | — (clean) |
| 26/9 | ~10 h | 14 °C | 0.93 s | 74 rpm |
| 3/10, session A | 27 h | 17 °C | 0.77 s | 15 rpm |
| 4/10, session A, after a disconnect and 098 | ~15 h | 15 °C | 1.38 s | 0 rpm |
| 4/10, session B, part-warm | ~2 h | 44 °C | 0.70 s | 0 rpm |

### The injectors were not fully seated, 23/9 to 1/10/2026 — owner-reported and photographed

Fitted **already clipped into the rail**, then the rail pushed down: **three
would not go fully home**, a gap of under about 1 mm, in the owner's
photographs. **Cylinder 4 was home** (*owner*, re-confirmed 28/9); 1, 2 and
3 proud. An old injector tried alone **clicked fully home in every bore**.
The manifold-end O-ring is the seal against the intake (`open.md` H3).
**Done on 1/10/2026: all four flush.**

### The MAF

**24/9/2026**, genuine VW `06A 906 461 A`; the 2018 unit kept. Its
connector points forward, as on the 2018 unit; flow direction right; the
harness not clipped in; **left as it is** (*owner's decision*, 3/10). **The
wiggle test, 4/10** (`open.md` S3, *Session A after step 1b*): nothing —
003 3.06–3.54 g/s against 2.92–4.03 before, 014 counting already. **The
contact is sound.** The hose to the throttle on non-original clamps
(*owner*); the MAF end changed to an all-metal clamp on 9/10 (above).
