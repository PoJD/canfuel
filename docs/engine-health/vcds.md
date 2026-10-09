# VCDS on this car — the blocks we read, and how to record them

The ECU's own view of the engine comes through VCDS on the OBD socket, and
none of it is on the CAN bus the firmware reads. This file is **our own summary
of the blocks this project uses** and the one recording technique everything
in `open.md` rests on.

⚠ **The label file itself is not kept in this repository and should not be.**
It is Ross-Tech's, part of a commercial product rather than something its owner
publishes openly, so it does not belong in a repository under Apache 2.0 — not
even in `NOTICE`, which is for material whose owners do publish it. **The
tables below are our own notes of what we looked up**, not a copy of theirs.
Anyone with VCDS for this ECU has the file.

The ECU is `06A 906 018` (`06A 906 018 EJ` on the screen), Motronic 5.9.2,
labels `06A-906-018-AQY.LBL`.

**Cylinder numbering.** Cylinder 1 is at the timing-belt end; standing at the
engine, **cylinder 4 is the one at the far right** (*owner*, 28/9/2026). VCDS
numbers the same way, so every cylinder in these groups is the real one. An
observation by eye names its cylinder by this rule — the plug-boot oil of S10
was first recorded counted from the wrong end and corrected on 28/9/2026.

---

## The blocks

| block | what it carries | what it has been used for |
|---|---|---|
| **002** | engine speed · load · injection time · **mass air flow** | full-load air and load; b6 of 0x288 is injection time |
| **003** | engine speed · **mass air flow** · throttle angle · ignition advance | mass air flow is not on the CAN bus; the idle advance shows the idle control working |
| **004** | engine speed · **ECM supply voltage** (spec 12.0–14.5 V) · coolant · intake air temperature | the ECM's own view of its supply: the voltage-drop tests in `open.md` H4 |
| **006** | **intake air temperature** · altitude correction factor | the volumetric-efficiency bracket in `docs/firmware/frames.md` |
| **010** | engine speed · **relative load** · throttle · advance | the load reference (0 °C, 1013 hPa) |
| **014** | engine speed · load · **misfire count** · detection state | the idle misfires (S3) |
| **020** | ignition retard of **all four cylinders** in one group | knock control per cylinder (S4); replaces 022 + 023 and frees a slot |
| **022 / 023** | ignition retard per cylinder, 1–2 and 3–4 | the first cylinder-4 log |
| **026** | **knock sensor voltage per cylinder**, *amplifier factor included* | S5. Not the raw signal: the ECU scales each cylinder |
| **032** | lambda adaptations, idle and part load | the rich trim that was the MAF (S9) |
| **055 / 056** | idle regulator, its adaptation, target idle speed | 055 logged once, on the cold start of 11/9 (`vcds-coldstart-014-055.csv`): regulator −0.46 → −0.08 g/s as the engine warmed, adaptation **−0.73 g/s** throughout, load-state bits `0000`. The cold-start baseline for the sessions of 3–4/10 (`open.md` S3) |
| **070** | evaporative valve test | TEV OK — purge ruled out |
| **100** | readiness bits, OBD status, time since start | all monitors complete |

**Specifications worth quoting, because they turn an observation into a
finding:**

- **Misfires, block 014, are specified `0...5`.** This car reads 12–120. It
  also shows the counter is a *current* count, whatever `(celkovy)` says: 0 to
  5 is not the range of a lifetime total. **In practice the specification
  is zero**: this counter reads mostly in multiples of 12, now and then
  13–17 (every 014 log in `test/fixtures/vcds/`, counted 3/10/2026), and
  its smallest non-zero reading on record is 12 — already outside 0–5. A sister VAG ECU
  says it outright — the AUA's list of blocks and specifications gives
  014 field 3, *Zähler Verbrennungsaussetzer insgesamt*, as **0**, and 015/016
  per cylinder likewise (wiki.a2-freun.de, *J537 – Motorsteuergerät AUA –
  Messwertblöcke und Sollwerte*, read 3/10/2026; a different engine and
  ECU, so supporting evidence, not this car's figure).

- **This ECU has no per-cylinder misfire counters.** Blocks 015 and 016,
  which carry them on other VAG engines, do not exist on this car's ECU
  (*owner*, checked on the car; confirmed again 9/10/2026), and the label
  file defines only 014 in that range. So **no misfire on this car can
  be put to a cylinder by VCDS**. The only per-cylinder readings it has
  are the knock ones — 020 and 022/023 (timing retard) and 026 (knock
  sensor voltage) — and those see the engine under load, not at idle.
  Engine speed on the bus cannot name a cylinder either
  (`open.md`, *Naming the cylinder*).

  **What the number is** — Bosch's patents on misfire detection
  (DE19547058B4, DE19622448B4, DE19814732A1, DE10010459; read 3/10/2026),
  a principle and not this ECU's calibration: the ECU times each crank
  segment, one per firing; from the differences between successive
  segments it computes a roughness (*Laufunruhe*), with slow changes such
  as acceleration compensated; roughness above a threshold that depends on
  engine speed and **load** counts as a misfire; and the counts are summed
  over a window of crank revolutions (1000 in the patents) and reset. So
  014 is **the output of that calculation, not a number of misfired
  combustions** — why it reads in twelves and holds about 3 s here is the
  calibration, and no public source says. *Reasoned from it:* a threshold
  that moves with load, and load computed from the MAF, is the likely
  reason the counter's sensitivity changed with the MAF (`refuted.md` A11).

  **What VW says about the same detection on Motronic M5.9** — VW's
  self-study programme *SSP 175, On-Board-Diagnose II, Konstruktion und
  Funktion*, pp. 10 and 50–52 (read 9/10/2026; not kept here, it is VW's).
  M5.9 is this ECU's family, not its calibration:
  - **The fault code needs more than 2 %.** The rate is checked "in
    festgelegten Meßintervallen von 1000 KW-Umdrehungen"; 1.5 times the HC
    limit "entspricht einer Aussetzerrate größer 2 %". A second window of
    200 revolutions, weighted by engine speed and load, watches for a rate
    that damages the converter (the lamp blinks). Codes P0300/16684 and
    P0301–P0304/16685–16688. *Arithmetic:* at 780 rpm, 1000 revolutions
    are 77 s and 2000 firings, so 2 % is about **31 misfires a minute** —
    which is why this car's 014 has never left a code at idle.
  - **The crank wheel is adapted on the overrun**: "Um kleine
    Fehler/Toleranzen am Zahnkranz zu kompensieren, findet während des
    Fahrbetriebes in der Schubphase eine Geberradadaption statt." Detection
    measures the 60-2 wheel through G28 segment by segment, so its tooth
    errors have to be learned first. **Whether a battery disconnect clears
    it on this ECU is not known**; that it is learned only with the fuel
    cut, which here needs ~76–84 °C of coolant and 1,500+ rpm
    (`tools/coastscan.py`), is VW's statement plus this car's bus.
    Bosch's patent on the adaptation (US 6,142,011) stores the values
    from the last run and starts from zero on the very first.
  - **Rough roads switch it off** for a set time, on a signal from the
    ABS — so a count is suppressed, never invented, by the road.
- **Ignition retard per cylinder, 022/023/020: 0–15 °CA while driving** — from
  VW's repair manual (Golf Mk4, *Motronic injection and ignition system,
  2.0 ltr.*, as transcribed on workshop-manuals.com), which matches this ECU's
  groups field for field.
- **The idle regulator, block 055, is −2.00 to +2.00 g/s**, its learnt
  value **−1.50 to +1.50 g/s**, and the target idle in 056 is 780 rpm.
  (An earlier revision gave the learnt value's top as +0.150, a
  transcription slip.) VW's note on the learnt value: it is *"the amount
  that the idling speed stabilisation has moved away from the prescribed
  average. For a new engine the values lie in the positive range, because
  of the higher friction and in the negative range with an engine that
  has run-in."* Field 4's bits, left to right: A/C compressor on, gear
  engaged, A/C switched on, not relevant. *Source for this and the next
  three bullets: VW's repair manual for this engine, as transcribed on
  workshop-manuals.com — Golf Mk4, Motronic (2.0 ltr. engine),
  Evaluating measured value blocks, display groups 0…9 and 50…69, read
  28/9/2026.*
- **Idle air mass, block 002: 2.0–5.0 g/s**; below 2.0 is *"large amount
  of unmetered air between intake manifold and air mass meter"*. Idle
  injection period 2.0–5.5 ms, engine load 15–35 %.
- **Block 003 at idle: ignition 0–12 ° BTDC, throttle angle 0–6°.**
- **Blocks 060 and 098 both adapt the throttle** when run under basic
  settings, ignition on, engine not running; the adaptation procedure
  itself (page 24-119) uses **098**. Its zones: ADP state, operating
  condition *Idling*, positioner sender G127 **60.0–90.0 %**, angle 0–6°.
  060 shows the same but G127 as a voltage, 0.0–5.0 V. **VW asks for the
  adaptation after a battery disconnect** as well as after a new J338.
- **Intake air** is specified −45.0 to +108.5 °C.
- **Idle speed**, every block that carries it: 740–820 rpm, target 780
  (050/056).
- **Supply voltage, block 004 field 2: 12.0–14.5 V.**
- ⚠ **020 and 026 are not in this ECU's label file** — it defines 022/023 for
  the retard. They are on Ross-Tech's general list and this ECU answers them
  (both were logged in September 2026), so the fields are read without a
  label and without a specification.

**What is not there, looked up rather than assumed:**

- **No absolute misfire counter and no per-cylinder one.** 014 is the only
  misfire block.
- **No oil temperature.** The label file defines 29 blocks — 001–006, 010,
  014, 022, 023, 030, 032–034, 036, 037, 041, 046, 050, 054–056, 060, 066,
  070, 077, 098–100 — and every temperature in them is coolant (001, 004, 077,
  099, 100), intake air (004, 006) or catalytic converter (034, 046). So
  `OilTemp` on 0x420 cannot be cross-checked against the ECU
  (`docs/firmware/open.md`).
- **No torque in Nm.** Looked for in 2026 and not there; the scale came from
  the full-throttle plateau instead (`docs/firmware/can-decoding.md`
  question 8).

## Basic settings: the verdict blocks

**034, 036, 037, 046, 060, 070, 098 and 099 are *basic setting* blocks**: they
run a routine and report a verdict rather than a state. The catalytic
converter temperature in them is a **gate** that has to be met before the
verdict means anything, not a reading to interpret.

| block | tests | gates | answer |
|---|---|---|---|
| **034** | pre-cat oxygen sensor ageing | 2200–2800 rpm, cat ≥ 352 °C, period ≤ 2.2 s | `B1-S1 OK` / `not OK` |
| **046** | catalytic converter conversion | 2800–3200 rpm, cat ≥ 352 °C, amplitude 0.00–0.55 | `CatConvB1 OK` / `not OK` |
| **036 / 037** | post-cat sensor availability and response | 037 wants 15–35 % load | `B1-S2 OK`, `Sys. OK` |

On 24/9/2026, at a hot idle, every one of them reported OK at once, with no
rpm hold needed.

**Basic settings is not the output test**, and the two are easy to confuse.
`Akční členy` steps through actuators with START/DALŠÍ with the engine
stopped. Basic settings is the **`Přepnout na základní nastavení`** button
inside `Měřené hodnoty`, takes a group number, and runs whatever that group
defines (VAG-COM manual §5.2 and §5.3); some need the engine running.

---

## Recording VCDS and the CAN bus together

**Do not try to align the two in time. Match them on engine speed.** Engine
speed is on the bus (0x280 b2–b3) and in almost every VCDS group, so the
VCDS log can be slid against the capture until the two engine-speed traces
agree. The offset with the smallest mean |Δrpm| is the alignment; on the
24/9 drives it came out at 207.6 s and 802.3 s with a mean error of
23–36 rpm, and on the cold start at 129.3 s with 19.1 rpm RMS. No clocks
have to agree.

- **The two tools do not interfere.** VCDS is on the OBD socket and this
  engine diagnoses over K-line; the USBtin is on the CAN pair at the cluster,
  in listen-only mode.
- **Log to a file, and choose three groups that include engine speed.**
  VCDS reads the groups one after another, about 0.3 s apart, so a sample in
  one group sits that far from the next group's. That blurs a transient,
  not a steady hold.
- **Check that the log is still running after the engine catches.** VCDS has
  lost the ECU during cranking twice and does not recover on its own. The
  cold start of 11/9 lost its first 86 s of running to it.
- **For a steady measurement, hold the engine speed 10–15 s per point**, in
  neutral, handbrake on. Two holds at the same speed with a different load
  (A/C off and on) are the only way to tell a quantity that tracks load from
  one that tracks speed.
- **Note the oil temperature** off the display beside every session. Nothing
  about the idle compares without it. With the display out, the capture
  has it: `tools/oilwatch.py` reads the capture file while it is being
  written, in a second window, and beeps when an idle is due in its band
  and when it has been long enough.

The CSV files are in `test/fixtures/vcds/`, described in
`test/fixtures/README.md`.

## VW's repair manual — where the specifications come from

The VW specifications quoted in these documents are read from **VW's repair
manual for this engine as transcribed on workshop-manuals.com** — free,
public, HTML only, a third-party transcription rather than VW's own
document, and so far consistent with this ECU field for field. The
official source is VW's paid **erWin** portal. The pages used:

- [Idling check](https://workshop-manuals.com/volkswagen/golf-mk4/power_unit/motronic_injection_and_ignition_system_(2.0_ltr._engine)/mixture_preparation_system_electronic_inj.gas/checking_functions/idling_check/)
- [Evaluating measured value blocks, display groups 0…9](https://workshop-manuals.com/volkswagen/golf-mk4/power_unit/motronic_injection_and_ignition_system_(2.0_ltr._engine)/self_diagnosis_v.a.g_inspection_service/evaluating_measured_value_blocks_display_groups_0...9_-basic_functions-/)
- [Evaluating measured value blocks, display groups 50…69](https://workshop-manuals.com/volkswagen/golf-mk4/power_unit/motronic_injection_and_ignition_system_(2.0_ltr._engine)/self_diagnosis_v.a.g_inspection_service/evaluating_measured_value_blocks_display_groups_50...69_-speed_regulation-/) — 055, 056, 060, 098
- [Adapting engine control unit to throttle valve control part](https://workshop-manuals.com/volkswagen/golf-mk4/power_unit/motronic_injection_and_ignition_system_(2.0_ltr._engine)/mixture_preparation_system_electronic_inj.gas/engine_control_unit/adapting_engine_control_unit_to_throttle_valve_control_part/) — page 24-119
- [Checking throttle valve control part](https://workshop-manuals.com/volkswagen/golf-mk4/power_unit/motronic_injection_and_ignition_system_(2.0_ltr._engine)/mixture_preparation_system_electronic_inj.gas/checking_components/checking_throttle_valve_control_part)
- [Adjusting throttle cable](https://workshop-manuals.com/volkswagen/golf-mk4/engine/4-cyl._injection_engine_(2.0_ltr.)_mechanics/fuel_supply_gas_operation/accelerator_mechanism/adjusting_throttle_cable/)

Every page has `<` / `>` links to the neighbouring chapters, which is the
quickest way through the rest of the manual.
