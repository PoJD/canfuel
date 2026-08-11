# The VCDS session — open questions 3 and 8

One session in the car settles both, because both want the same thing: the
ECU's own idea of a quantity, read through diagnostics, next to the raw bytes
of 0x280 and 0x288 read off the bus.

- **Question 3** — 0x288 b5 and b6 are load-dependent and undecoded. Candidates
  are mass air flow, ignition advance and injection time.
- **Question 8** — 0x280 b7 is a percentage of a reference torque inside the
  ECU, not Nm. The firmware uses 0.75 Nm/bit, a decision inside a bracket the
  factory ratings imply rather than a measurement.

**Expectation, set honestly before anyone drives anywhere.** Question 3 should
close: all three candidates are ordinary ME7 measuring values. Question 8 may
not, because it depends on whether this ECU exposes engine torque in Nm at all
— see "if there is no torque value" below. Going in expecting one and a half
answers is better than going in expecting two.

---

## The one idea that makes this easy

**Do not try to align the two recordings in time. Match them on engine speed.**

Engine speed is in the CAN data (0x280 b2–b3) *and* on the VCDS screen. So if
the engine is held at a few distinct steady speeds, every VCDS reading can be
matched to the right stretch of CAN capture by its rpm alone. Nothing has to be
synchronised, no clocks have to agree, and it does not matter if VCDS samples
three times a second while the bus runs at seven hundred.

Two consequences, and both are good news:

- **VCDS does not have to log to a file.** A photo of the screen at each hold
  point is enough, and it carries the rpm in the same frame as the values. If
  the version in the car does have a log button, use it — it is tidier — but
  nothing depends on it.
- **The holds have to be steady, and that is the only demanding part.** Ten to
  fifteen seconds at a stable speed. A drifting throttle is what breaks this
  method, not a slow logger.

## The two tools do not interfere

They are on different connections. VCDS goes to the OBD-II socket; the USBtin
is on the CAN pair tapped at the instrument cluster. On this generation engine
diagnostics runs over K-line rather than CAN, so VCDS traffic does not appear
on the powertrain bus at all.

And if that is wrong and this car does diagnose over CAN, it still does not
matter: the extra frames would simply show up in the capture, and the USBtin is
in listen-only mode where it cannot answer anything. There is no case where
running both causes a problem.

## Division of labour

- **The USBtin runs from the laptop: one short capture per hold point**, about
  25 s, started when the driver says the speed is steady.

  ```
  python tools/usbtin_capture.py --port COM5 --seconds 25 --out p1_idle_noac.txt
  ```

- **VCDS is driven by hand** on the same or a second laptop, screen
  photographed **during** each capture window so the two genuinely overlap.

**One capture per point rather than one long one, and the reason is not
tidiness.** A short capture can be checked immediately — engine speed, how
steady it was, whether the adapter dropped frames — and a bad hold can be
repeated *while the car is still sitting at that speed*. Finding it at a desk
twenty minutes later costs another trip to the car. Each file also carries its
own condition in its name, so nothing has to be segmented by rpm afterwards;
the rpm in the data then merely confirms what the filename already says, which
is the right way round.

Nothing happens between hold points, so continuity buys nothing here.

---

## Step by step

### 1. Before starting the engine

Connect the USBtin to the CAN pair and VCDS to the OBD-II socket. Engine warm
before any readings are taken — a warming ECU is on a different fuelling map
and every value below moves with it. Coolant needle in the middle.

### 2. Find the channels in VCDS

Select **address 01, Engine**, then measuring values. In current VCDS this is
**Advanced Measuring Values**, which lists channels by name and is far easier
than remembering group numbers — type a word into the filter and tick what
comes up.

Look for, by name:

| Wanted for | Look for | Unit |
|---|---|---|
| the match key | **Engine speed** | rpm |
| question 8 | **Engine torque** — if it exists | Nm |
| question 8 fallback | **Engine load** | % |
| question 3 | **Mass air flow** | g/s |
| question 3 | **Ignition timing / ignition angle** | ° |
| question 3 | **Injection time / injector on-time** | ms |

If only the older group-number interface is available, the shortlist is
**group 001, 002, 003** and **020 or 021**. Between them these carry engine
speed, load, injection time, mass air flow and ignition advance on ME7. Read
the labels rather than trusting the numbers — group contents vary by ECU
version, which is exactly why the named list is preferable.

**Tick engine speed plus as many of the others as the screen will show at
once.** If they do not all fit, do the run twice with different selections;
the rpm matching makes two runs as good as one.

### 3. The hold points

Stationary, **in neutral**, handbrake on, so the load is repeatable.

| # | Target | Hold | Note |
|---|---|---|---|
| 1 | idle, ~800 | 15 s | **air conditioning OFF** |
| 2 | idle, ~800 | 15 s | **air conditioning ON** |
| 3 | 1500 | 15 s | |
| 4 | 2000 | 15 s | |
| 5 | 2500 | 15 s | |
| 6 | 3000 | 15 s | |

**Points 1 and 2 are worth more than they look.** They are two different engine
loads at the same engine speed, which is the only way to tell a byte that
tracks *load* from one that tracks *speed*. Every other point moves both at
once. If time runs short, keep these two and drop 2500.

Photograph the VCDS screen once the numbers have settled at each point, and say
out loud or note down which point is which. The rpm on the photo is what ties
it to the capture, so it must be legible.

### 4. Afterwards

Stop the capture and keep the file. The analysis is a regression of each
candidate against each byte at six operating points, which is desk work.

For question 8 the plot is the whole answer: **VCDS torque in Nm against
0x280 b7**. A straight line through the origin, and its slope is the scale.
Four points across the range are plenty because there is nothing to fit but a
gradient.

## If there is no torque value

Entirely possible. Torque in Nm is a normal measuring value on diesel ECUs and
is not guaranteed on ME7 petrol, which tends to report **load in per cent**
instead.

If that is what turns up, question 8 does not close and the session is still
worth having:

- **Load % against b7 still identifies what b7 is.** If they are proportional,
  b7 is the same internal quantity the ECU calls load, which is a real finding
  even without units — and it would confirm the reading that b7 is *indicated*
  torque rather than crank torque, which is the correction made on 2026-08-11.
- **Question 3 is unaffected** and closes on the same data.
- The remaining route to the scale is then a full-throttle pull, which is
  deliberately not planned, or a factory document nobody has.

Say what was found either way. "The ECU does not report torque in Nm" is an
answer worth writing down, because the next person will otherwise plan this
same session again.
