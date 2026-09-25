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

---

## The blocks

| block | what it carries | what it has been used for |
|---|---|---|
| **002** | engine speed · load · injection time · **mass air flow** | full-load air and load; b6 of 0x288 is injection time |
| **003** | engine speed · **mass air flow** · throttle angle · ignition advance | mass air flow is not on the CAN bus; the idle advance shows the idle control working |
| **006** | **intake air temperature** · altitude correction factor | the volumetric-efficiency bracket in `docs/firmware/frames.md` |
| **010** | engine speed · **relative load** · throttle · advance | the load reference (0 °C, 1013 hPa) |
| **014** | engine speed · load · **misfire count** · detection state | the idle misfires (S3) |
| **020** | ignition retard of **all four cylinders** in one group | knock control per cylinder (S4); replaces 022 + 023 and frees a slot |
| **022 / 023** | ignition retard per cylinder, 1–2 and 3–4 | the first cylinder-4 log |
| **026** | **knock sensor voltage per cylinder**, *amplifier factor included* | S5. Not the raw signal: the ECU scales each cylinder |
| **032** | lambda adaptations, idle and part load | the rich trim that was the MAF (S9) |
| **055 / 056** | idle regulator, its adaptation, target idle speed | not yet used for anything |
| **070** | evaporative valve test | TEV OK — purge ruled out |
| **100** | readiness bits, OBD status, time since start | all monitors complete |

**Specifications worth quoting, because they turn an observation into a
finding:**

- **Misfires, block 014, are specified `0...5`.** This car reads 12–120. It
  also shows the counter is a *current* count, whatever `(celkovy)` says: 0 to
  5 is not the range of a lifetime total.
- **Ignition retard per cylinder, 022/023/020: 0–15 °CA while driving** — from
  VW's repair manual (Golf Mk4, *Motronic injection and ignition system,
  2.0 ltr.*, as transcribed on workshop-manuals.com), which matches this ECU's
  groups field for field.
- **The idle regulator, block 055, is −2.00 to +2.00 g/s**, its adaptation
  −1.50 to +0.150 g/s, and the target idle in 056 is 780 rpm.
- **Intake air** is specified −45.0 to +108.5 °C.

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
  about the idle compares without it.

The CSV files are in `test/fixtures/vcds/`, described in
`test/fixtures/README.md`.
