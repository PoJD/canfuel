# Firmware spec: what the post-repair drive changes

**The work order for one session**, ending in a flash. It is built from
`docs/postfix-drive-results.md`, which holds the measurements, and from
Part 2 of `docs/next-drive.md`, which holds the designs. This file is a
holding document like both of them. When the work below is done and flashed,
all three are deleted and whatever is still true lives in the permanent
documents.

**Order matters**: 1 and 2 are independent, 3 is the large one, 4 and 5 close
the session. Each numbered item is one commit, per `CLAUDE.md`, unless two
of them touch the same files. **Items 1–3 change the hex, so XC8 is installed
before the first push** (see *Changing code means installing XC8 first* in
`CLAUDE.md`).

---

## 1. The torque scale: `TORQUE_CNM_PER_BIT` 74 → 106

**Evidence:** `postfix-drive-results.md` §3. Held full-throttle pulls in
4th put b7 at a median of **185 at 2400 rpm** and **191 at 5200 rpm**. With
the drag line held in bytes (`drag_b7 = 9.11 + 0.006514 × rpm`), the two
factory ratings give 1.061 and 1.055 Nm/bit, **0.6 % apart**. 106 is a
decision inside that bracket.

**Changes:**

| where | what |
|---|---|
| `src/config.h` | `TORQUE_CNM_PER_BIT` 74 → **106**. `DRAG_TORQUE_BASE_CNM` and `DRAG_TORQUE_SLOPE_Q16` are the byte line times the scale, so they follow: **966** cNm and **45252**. Recompute both from the byte line; do not copy them from here. The drag line in bytes does not move. The comment block above them is rewritten: the premise changes from *b7 = 255 is the rated crank torque plus drag* to *the observed full-throttle plateau reproduces both ratings* |
| `test/test_compute.c` | `test_full_scale_reaches_the_rated_power` and `..._torque` are rewritten to assert that **b7 = 185 at 2400 rpm gives about 170 Nm, and b7 = 191 at 5200 rpm gives about 85 kW**. That is the first version of these tests with a measurement behind them. The eight driving-gate tests must stay green **untouched** |
| `test/test_txframes.c` | whatever pins a torque or power byte against a fixture moves with the scale. The two driving-gate tests there stay untouched |
| `tools/replay.py` | its `0.74` → `1.06`, and the drag line with it. **A change to the maths belongs in both twins** |
| `docs/frames.md` | the 0.90–0.96 bracket is superseded. That route divided 188 Nm (rating plus drag *in Nm at 0.74*) by the plateau. With the drag held in bytes it lands where the ratings do. Keep the old argument, marked superseded, with the reason |
| `docs/can-decoding.md` | the torque scale entry under *Never resolved but not required* moves to *Resolved questions*, with the pulls as the evidence |
| `CLAUDE.md` | *The torque calibration* section: 0.74, "85.4 kW and 170.4 Nm against ratings", "0.736–0.738" and the "b7 = 255" premise are all rewritten. The drag line stays |

⚠ **`TORQUE_TRIM_PCT` stays 0.** Setting the scale is not a job for the trim.

⚠ **Overflow.** At 106 cNm/bit, 255 counts is 27,030 cNm. Check that every
`uint16`/`int16` intermediate in `compute_torque_d()` and
`compute_power_d()` still holds it. `test_props.c` fuzzes b7 through the
getters and will show a wrap, but read the arithmetic anyway.
`docs/optimisation.md` §6/§11 has the conventions.

## 2. Promote the pending fixtures

`test/fixtures/pending/README.md` lists the files and the seven tests they
break.

- move `19`, `20`, `21`–`23` and `24` up one level under the same names, and the
  three VCDS CSVs into `test/fixtures/vcds/`
- **update the seven tests to the widened corpus, and do not delete them.**
  Each one describes the data, and each has to become true of the new data
  for the reason the data gives:
  - `test_0x200_is_a_one_off_too`: 0x200 now appears in `20`, **while VCDS
    reconnected**. That is the finding (`postfix-drive-results.md`, *The
    0x200 test*). Assert it: 0x200 appears only in logs where VCDS was being
    reconnected
  - `test_regular_id_set`, `test_dlc_is_stable_per_id`: the switch-off burst
    in `20` produces corrupted identifiers (0x000, 0x058, 0x078, a 29-bit
    one) within a millisecond of the bus dying. Exclude them explicitly and
    say why. Do not widen the regular set to admit them
  - `test_no_lambda_on_0x488`: read what `20` actually carries before
    deciding
  - the three `test_coastscan` tests: the corpus now has 72 cuts, fuel
    returning at 1,380–3,500 rpm and engaging 0.77–4.27 s after the lift.
    The claims become ranges measured over the corpus
- `test/fixtures/README.md`: a row per file in the overview table, and a
  section for the drive and the MAF-swap session
- `tools/checkdocs.py` counts fixtures, so prose quoting the count will
  change with it. Let the check say where

⚠ **Runtime.** `19` is 33 MB and the Python suite parses the whole corpus.
Measure the `tools` CI job before and after. If it becomes painful, a
module-level parse cache in the tests is the fix, not dropping the file.

## 3. The health frame, 0x604: idle grade and start, NOT JP1-gated

**The design is Part 2 question 6 of `docs/next-drive.md`, in full**:
*What goes on the bus instead*, *The start, and why its index ships empty*,
*Where it goes*, *What changes, and where*, *The acceptance test*. Read it
first. It is not repeated here, because it is already exact. What follows
is what the drive changed about it.

**Built now, on the maintainer's decision, although the engine is not
healthy.** The question-6 rule said nothing gets built unless a healthy
grade separates from a sick one, and no healthy idle has been recorded yet
(`postfix-drive-results.md` §6). The decision here is that the channel is
wanted *because* the idle is about to be worked on: the intake hoses are next,
and the owner wants to see the effect on the display rather than by capture.
**That is a trend instrument doing its job.** It is not a claim that the grade
has been validated against a healthy engine. The frame layout carries a
version, so a later re-anchoring costs no layout change.

**What the display will show on day one**, from the grade over today's
recordings:

| state | index (100 = the engine before the repair) |
|---|---|
| warm idle, 52–60 °C oil, new MAF | 73–100 |
| hot idle, 69–71 °C, new MAF | 68–121 |
| August's hot idle, before any work | 48 |

**Constants, verbatim from `tools/idledips.py`, and never re-fitted:**
`ROUGH_DEADBAND_RPM` 3, `ROUGH_SHIFT` 8, `ROUGH_OUT_SHIFT` 5,
`IDLE_ROUGH_100` 64, `IDLE_INDEX_MAX` 200. The gate uses the existing
`STANDSTILL_MMH` and `THROTTLE_REST`, with one definition shared by both
rules.

**Two constants the design left open, decided here:**

- **`IDLE_CONVERGE_S` = 30 s.** The grade's EWMA spans 256 firing events,
  about 9.7 s at a warm idle, so it is 95 % converged after three of those,
  about 29 s. 30 s of settled idle before byte 0 stops reading 255. The
  alternative was one time constant (10 s), which would publish a grade still
  a third short of its value, and an unconverged grade reads *healthy*
- **`START_FIRED_RPM` = 400**, as the design has it. Both recorded starts
  fire at 450–451 rpm after a cranking plateau of 200–270, so 400 has margin
  at both ends

**The start fields have a second recording now** (`postfix-drive-results.md`,
*The start: n = 2*): crank 0.83 s against 1.24 s, fall-back 118 against 140
rpm. `StartHealth` still ships reserved (255). Two starts anchor nothing.

**The acceptance test is unchanged**: the C must reproduce `roughness()`'s
byte **exactly** over `09`, `11`, `12`, `17`, `18`, and now `19` and `24`,
once item 2 has promoted them. The three traps in *The acceptance test* are
the ones to test for.

**Across the two repositories, in one breath:** `docs/frames.md` 0x604
section, the slot table and the not-JP1-gated note; `mfd15/tri/S-AQY.TRI`
rows; `mfd15/docs/sensors.md`; `mfd15/README.md`; `test/test_txframes.c`
offsets pinned against the TRI lines. **Check that slot 6 is still free in
`config.h` before taking it.** The design says so, and the slot table is the
thing that moves.

## 4. What does not change, and must not be changed by accident

- **coolant decode** `× 0.75 − 48`: confirmed against VCDS at 12.0, 99.0 and
  100.5 °C (`postfix-drive-results.md` §1). Record it in `can-decoding.md`.
  No code change
- **oil decode** `× 0.75 − 48`: still open. The 1.1 decision was withdrawn
  on three cool-down points (§2). **Do not change `decode.c` or `OilTemp` in
  the TRI.** Question 10 gets the three points as evidence
- **the refuelling rule and Range** held over the drive (§4, §5)
- **no fuel correction factor.** The rich trim was the MAF, and the fuel
  counter was right (*The MAF swap*)

## 5. Close out the documents, then flash

- **delete `docs/next-drive.md`** once item 3 has taken its design across.
  Step 30 (read 032 again after a few hundred km) moves into
  `engine-health.md`, since it now reads the new MAF's adaptation settling
- **`engine-health.md`**: the MAF swap and the idle-only misfire finding go
  into it as the current state. `postfix-drive-results.md` is then deleted,
  along with this file
- `README.md` size block, regenerated by `checkdocs.py --write` from the XC8
  build, committed **with** the code

**Before pushing:** `make -C test check-pure test check-hal`,
`python tools/replay.py --host-build test/fixtures/*.txt`, the Python suite,
`make -C mplab`, `python tools/cycles.py --check`,
`python tools/checkdocs.py --check`, **each checked by exit code**. Piping one
into `tail` is how a failing check reached CI earlier today.

**Flash:** `python tools/flash.py --preserve-eeprom`, which keeps the trip and
checks that it did (`docs/flash-tool-notes.md`). Normal mode.

**The check after the flash, and it costs one photograph**, from *After the
reflash* in `next-drive.md`: `Torque`, `Power` and `RPM` on one page during
a steady moment. It is the only test of `fastmul.h`/`divconst.h` as the part
executes them. **Then idle for at least 30 s and read the new 0x604 rows**:
byte 0 must leave 255, and the index should land in the table under item 3.
