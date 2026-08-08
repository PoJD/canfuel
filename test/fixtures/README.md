# Fixtures — logs from the USBtin

Real recordings from the Beetle's powertrain CAN bus. **Do not edit.** The
tests in `tools/` reference exact numbers from them, so any change shows up
immediately.

## Overview

| File | Format | Lines | What it is | CLT |
|---|---|---|---|---|
| `01_ign_only.txt` | slcan | 3,402 | ignition on, engine off, counter all zero | 100.5 °C |
| `02_idle_60s.txt` | slcan | 89,882 | warm idle at 797 rpm, 60 s | 94.5–99 °C |
| `03_drive.txt` | slcan | 18,018 | driving in first gear up to 19.4 km/h | 99 °C |
| `05_rev3000.txt` | slcan | 1,522 | 2940 rpm in neutral | 90 °C |
| `06_trip_reset.txt` | viewer | 99,103 | standing, trip reset, a 125 m crawl | 53–64 °C |
| `07_accel.txt` | viewer | 11,192 | brisk acceleration to 24.8 km/h | 76 °C |
| `idle.txt` | slcan | 1,136 | short idle, colder engine | 68.25 °C |

## Two formats

**slcan** — the raw stream from the USBtin, no timestamps:

```
t1a0800400100fefe001d
^ ^  ^^
| |  +- payload, two hex chars per byte
| +---- DLC, one hex char
+------ 11-bit ID, three hex chars
```

**viewer** — export from USBtinViewer, five tab-separated columns:

```
2078 <TAB> jar:file:/...receive.png <TAB> 320h <TAB> 8 <TAB> 05 00 86 00 00 00 00 00
ts (ms)    row icon                   ID+h    DLC    space-separated bytes
```

Rows with the `info.png` icon are viewer messages ("Connected to USBtin",
"Disconnected") — their ID and DLC columns are empty and the parser skips them.

`tools/canlog.py` tells the formats apart by the tab character; slcan never
contains one.

---

## ⚠ `02_idle_60s.txt` contains the recording twice

Both halves of the file are **identical line for line** — 44,941 + 44,941
lines. This is not a theory, it is pinned down by `test_02_is_doubled`.

**Consequence:** without the correction the idle flow comes out doubled
(620 instead of 310 µl/s) and the whole fuel calculation would be off by 100 %.

**How it is handled:** the file stays in the repo exactly as it came out of the
USBtin — the original measurement is never rewritten. The correction happens at
read time:

```python
frames = canlog.parse_file(path, fix_doubled=True)
```

```
python tools/canlog.py --fix-doubled test/fixtures/02_idle_60s.txt
```

`tools/replay.py` has it on by default.

After the correction the numbers are 18,652 µl over 60.1 s = **310.1 µl/s =
1.12 l/h**, which is exactly the figure in the specification. That is also the
strongest indirect evidence that the period of frame 0x480 really is 49.5 ms.

No other fixture is doubled (`test_no_other_fixture_is_doubled`).

---

## Naming

`02_idle_60s.txt` was originally called `02_idle_60sec_170ms.txt` and
`05_rev3000.txt` was `rev3000.txt`. Renamed to match the specification
(BOOTSTRAP section 5); the contents are untouched.

`idle.txt` was not numbered in the specification and keeps its original name.
By coolant temperature (68.25 °C) it is chronologically the **first** of the
session, ahead of `05_rev3000`, so numbering it 04 would imply the wrong order.

---

## Duplicate frames

In every log, 39–51 % of the lines are an immediate duplicate of the preceding
frame — same ID, same payload. It is an artefact of the recording, not of the bus.

It has no effect on counter delta arithmetic (the delta is zero), but it
**doubles any measured frame period**, which is why periods cannot be derived
from these logs. Details in `docs/can-decoding.md`.
