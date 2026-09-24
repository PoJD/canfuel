# Pending fixtures: recorded, not yet in the corpus

**These are real recordings and, like every fixture, are never edited.** They
sit in this subdirectory because the tools and the tests glob
`test/fixtures/*.txt`, and adding these two files there makes seven existing
tests fail:

- `test_canlog`: `test_dlc_is_stable_per_id`, `test_0x200_is_a_one_off_too`,
  `test_no_lambda_on_0x488`, `test_regular_id_set`
- `test_coastscan`: `test_fuel_comes_back_well_above_idle`,
  `test_the_corpus_holds_four_overrun_fuel_cuts`,
  `test_the_cut_does_not_engage_the_moment_the_pedal_comes_up`

Every one of those assertions describes the corpus as it was before this drive,
so the failures are the new data disagreeing with the old corpus. They are not
faults in the recordings. Promoting the files is a piece of work in its own
right. It is listed in `docs/postfix-drive-results.md` under *Fixtures*, and it
moves them up one level under the same names.

| File | Format | What it is |
|---|---|---|
| `19_postfix_drive_z1.txt` | slcan+Z1, **filtered** to 0x1A0, 0x280, 0x288, 0x320, 0x420, 0x480 | the `next-drive.md` session: ignition on at a 10 °C cold soak, cold start, three idles, coasts, held 4th-gear full-throttle pulls, hot idle. 3605 s |
| `20_postfix_final_z1.txt` | slcan+Z1, **whole bus** | step 25–27: hot idle, VCDS disconnected and reconnected (0x200 appears), switch-off. 241 s of bus |
| `21`–`23_oilcool_p*_z1.txt` | slcan+Z1, whole bus | ignition on, engine off, during the cool-down, each taken while the oil filter was read by IR. The table is in `docs/postfix-drive-results.md` section 2 |
| `24_mafswap_drive_z1.txt` | slcan+Z1, **filtered** as `19` | the same afternoon after a new MAF: warm restart, driving, a 52–60 °C idle, more driving with some pulls, hot idle. About 30 min |
| `vcds-mafswap-002-032.csv`, `vcds-mafswap-002-014.csv` | VCDS logs, cp1250 | the first and second halves of `24`: 002 with 032 (the adaptation learning), then 002 with 014 |
| `vcds-postfix-drive-003-014.csv` | VCDS log, cp1250, as exported | groups 003 and 014 across the whole of `19`, from about 15 s before the start |

The unfiltered capture behind `19` (65 MB) is kept outside the repository.
