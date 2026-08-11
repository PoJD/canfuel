# Fixtures — logs from the USBtin

Real recordings from the Beetle's powertrain CAN bus. **Do not edit.** The
tests in `tools/` reference exact numbers from them, so any change shows up
immediately.

## ⚠ Read this before using any timestamp

**Only the three `_z1` logs have trustworthy time.** They were recorded on
2026-08-11 with `tools/usbtin_capture.py`, which drives the adapter directly
with `Z1` on, so each millisecond timestamp is stamped **in the USBtin when the
frame arrives**. Nothing else in this directory has a defensible time base:

- The **viewer** logs carry USBtinViewer's timestamps, which are taken on the
  host when a Java GUI got round to the line. The tool says so of itself. They
  are **wrong by roughly a factor of two** — measured, see below.
- The **slcan** logs carry no time at all. Time used to be synthesised for them
  from an assumed 49.5 ms period of frame 0x480. **That is now known to be
  unsound**: 0x480 has no fixed period.

**What is still good in every log, old and new:** the fuel totals. The ECU's
counter is absolute and in microlitres, so a missing frame is not missing fuel
and a wrong clock is not a wrong total. Every counter figure the tests assert
stands. It is duration, average flow and distance that need a clock.

## Overview

| File | Format | Frames | Time | What it is | CLT |
|---|---|---|---|---|---|
| `01_ign_only.txt` | slcan | 3,402 | none | ignition on, engine off, counter all zero | 100.5 °C |
| `02_idle_60s.txt` | slcan | 89,882 | none | warm idle at 797 rpm — **doubled, see below** | 94.5–99 °C |
| `03_drive.txt` | slcan | 18,018 | none | driving in first gear up to 19.4 km/h | 99 °C |
| `05_rev3000.txt` | slcan | 1,522 | none | 2940 rpm in neutral | 90 °C |
| `06_trip_reset.txt` | viewer | 99,101 | ❌ host | standing, trip reset, a 125 m crawl | 53–64 °C |
| `07_accel.txt` | viewer | 11,188 | ❌ host | brisk acceleration to 24.8 km/h | 76 °C |
| `08_ign_only_z1.txt` | slcan+Z1 | 14,656 | ✅ adapter | ignition on, engine off, 20 s | — |
| `09_idle_60s_z1.txt` | slcan+Z1 | 40,976 | ✅ adapter | warm idle at 796 rpm, 60 s, **A/C off** | 96.75–100.5 °C |
| `10_rev2600_z1.txt` | slcan+Z1 | 14,548 | ✅ adapter | 2586 rpm held in neutral, 20 s, **A/C on** | — |
| `idle.txt` | slcan | 1,136 | none | short idle, colder engine | 68.25 °C |

## The three `_z1` logs

Recorded in one session on 2026-08-11, engine warm, car stationary, MFD15
unplugged from the bus, adapter in listen-only mode. Conditions are recorded
here because they are not recoverable from the files and they change what the
numbers mean.

### `08_ign_only_z1.txt` — 20 s, ignition on, engine not running

The fuel counter is frozen and 0x480 is emitted irregularly, with every gap on
a **10 ms grid** — as are the modal gaps of the engine ECU's other frames
(0x0C2, 0x280, 0x288, 0x488, all exactly 10 ms). That is what retired 49.5 ms
as a candidate period: it is not a whole number of scheduler ticks.

This log also pinned the adapter's timestamp wrap. The counter reaches 60000
and the next frame reads 0, which is `canlog.TIMESTAMP_WRAP_MS = 60001`.

### `09_idle_60s_z1.txt` — 60 s, warm idle ← the reference recording

**796 rpm median, coolant 96.75 → 100.50 °C, air conditioning off.**

```
19,561 ul over 60.027 s  =  325.9 ul/s  =  1.17 l/h
```

The counter actually advanced 19,573 µl. The tools report 19,561 and **2
restarts** on a recording where the engine never stopped, because the counter
wrapped straight onto zero — `32756 → 0 → 0 → 24` — and `counter == 0` is the
ignition-restart test. One 12 µl step is discarded. It is understood, it is
deliberate, and the reasoning is under trap 2 in `docs/can-decoding.md`.

Measured, not derived: the counter is absolute and the clock is the adapter's.
This is the number that settled open question 9 — against USBtinViewer's
implied 157 µl/s (0.57 l/h), and roughly agreeing with the 310 µl/s that the
assumed period gave. The 796 rpm corroborates the air conditioning being off
on its own, since the compressor raises the idle to 850–900, and it lands on
the same 797 rpm the older warm-idle figure was taken at.

### `10_rev2600_z1.txt` — 20 s, engine held at 2586 rpm

**Air conditioning on.** This is the one difference from `09`, and it was
reported by the driver rather than being visible in the file.

Recorded to test whether 0x480 is broadcast once per injection, which the idle
log had made look likely — 26.4 frames/s against 26.6 injections/s is a ratio
of 0.994. **It is not.** Engine speed rose 3.25×, and the frame rate *fell*:

| | `09` idle | `10` revs |
|---|---|---|
| rpm | 797 | 2586 |
| 0x480 frames/s | 26.4 | 18.0 |
| mean gap | 37.9 ms | 55.5 ms |
| injections/s | 26.6 | 86.2 |
| ratio frames/injections | 0.994 | **0.209** |
| fuel | 326 µl/s | 888 µl/s |

Dropped frames cannot explain it: total throughput was *higher* in `10`
(727/s against 683/s), so the adapter was losing less, not more. Nor can the
air conditioning, which raises load and fuel flow and would push the rate up.

**Using this log to compare fuel flow against `09` or against `05_rev3000` is
wrong** — different load, different engine speed, and one has the compressor
running. It answers a question about broadcast rate, and that is all.

---

## Two and a half formats

**slcan** — the raw stream from the USBtin, no timestamps:

```
t1a0800400100fefe001d
^ ^  ^^
| |  +- payload, two hex chars per byte
| +---- DLC, one hex char
+------ 11-bit ID, three hex chars
```

**slcan + Z1** — the same, with four hex digits of adapter timestamp appended:

```
t1A0800400100FEFE0012B8C8
                     ^^^^ milliseconds, stamped in the adapter
```

The counter runs 0..60000 and then restarts, so it must be unwrapped before
any subtraction — `canlog.unwrap_timestamps()`.

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

After the correction the numbers are 18,652 µl over an assumed 60.1 s =
**310.1 µl/s**. The 18,652 µl is measured and stands. The 60.1 s does not: it
comes from multiplying the 0x480 frame count by an assumed 49.5 ms, and this
file has no timestamps to check it against.

> **This paragraph used to end "which is exactly the figure in the
> specification — that is also the strongest indirect evidence that the period
> of frame 0x480 really is 49.5 ms." Both halves of that are now withdrawn.**
> `09_idle_60s_z1.txt` measures the same operating point with a real clock and
> gets 326.1 µl/s, 5 % higher; on that clock this recording lasted 57.2 s
> rather than 60.1. And the period it was evidence for does not exist — see
> `10_rev2600_z1.txt` above and open question 1.

No other fixture is doubled (`test_no_other_fixture_is_doubled`).

---

## Naming

`02_idle_60s.txt` was originally called `02_idle_60sec_170ms.txt` and
`05_rev3000.txt` was `rev3000.txt`. Renamed to match the specification
(BOOTSTRAP section 5); the contents are untouched.

`idle.txt` was not numbered in the specification and keeps its original name.
By coolant temperature (68.25 °C) it is chronologically the **first** of the
session, ahead of `05_rev3000`, so numbering it 04 would imply the wrong order.

The `_z1` suffix is deliberate and worth keeping on any future recording: it
says the timestamps in that file can be trusted, which is the single most
important thing to know about a log here.

---

## Repeated payloads — normal, and previously misdiagnosed

In every log, **39–55 % of frames repeat the payload of the previous frame with
the same identifier**. This is not an artefact of the recording. It is what a
periodically broadcast frame does when its contents have not changed since the
last one, and the clearest example is in `09_idle_60s_z1.txt`: 31 % of 0x480
frames carry an unchanged fuel counter, because at idle the counter steps about
12 µl at a time and the frame goes out more often than that.

**Measured across both recording chains on 2026-08-11**, which is what settles
it — the `_z1` logs share no software with the viewer exports beyond the
adapter itself:

| | old fixtures | `_z1` logs |
|---|---|---|
| same-ID repeats | 38.6 – 55.3 % | 42.8 – 54.7 % |

The same range. Whatever produces them is not USBtinViewer.

> **What this section used to say, and why it was wrong.** It claimed the
> repeats were "an artefact of the recording, not of the bus", and that they
> "double any measured frame period, which is why periods cannot be derived
> from these logs". The first claim is refuted by the table above. The second
> was never sound reasoning — a repeated payload is a real frame and does not
> stretch an interval. Note that its *conclusion* survives anyway, for a
> better reason: periods cannot be derived from these logs because 0x480 has
> no period, and because five of them have no clock.
>
> There is also a plain reading of the old wording under which it is simply
> false: **immediate** duplicates, i.e. two identical consecutive *lines*, are
> **0.0 % in all ten files**. The 39–55 % figure only appears when "preceding
> frame" is read as "preceding frame of the same identifier".
