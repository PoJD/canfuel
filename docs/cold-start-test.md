# The cold-start test — one shot, before the parts are changed

**Read this on its own.** It is written to be followed from a fresh session
with no other context, on the laptop that has the USBtin plugged in.

---

## What this is

**A single cold start and two minutes of idle, recorded, on the car as it is
now** — old injectors, old plugs, old leads, new exhaust. It happens once
because the engine is otherwise staying off: a new catalytic converter behind a
cylinder still dumping raw fuel is the same converter that was cut open, and
three minutes is the smallest exposure that still buys something.

**Two of the three things it measures become impossible next week.** Once the
injectors are in there is no bad cold start left to record, and no stumbling
idle on a cold engine either. This is the last chance at both.

| what it captures | why now and not later |
|---|---|
| **the bad cold start** | gone once the injectors are replaced |
| **idle stumbles at the lowest oil temperature ever recorded on this car** | the existing fixtures are 61, 73 and 73 °C and nothing below |
| the idle regulator, and when misfire detection switches on | neither has ever been looked at |

---

## What is connected

**The MFD15 comes out and the USBtin goes on that pair.** The converter is
powered by 5 V from the display, so it will be unpowered and silent — **frames
0x600–0x603 will not be in the capture and that is correct.** This recording is
about the car, not about us.

**VCDS runs at the same time** on the OBD socket. The two do not interfere:
different connection, and diagnostics on this engine is K-line rather than CAN
(`docs/vcds-session.md`).

⚠ **Do not fit the display for its `OilTemp` reading.** That channel is
`0x420` byte 3 — the car's own frame — so **every capture carries it already**,
against every single sample rather than as something read off a screen.

---

## The run

**1. Start the capture first.** It can run into empty air; that costs nothing.

```
python tools/usbtin_capture.py --seconds 240 --out coldstart_z1.txt
```

Listen-only is the default and is what is wanted. Four minutes leaves margin
and is about 4 MB.

**2. Start VCDS logging, groups 014 and 055, with the engine still stopped.**

| | fields |
|---|---|
| **014** | engine speed · engine load · **misfire count** · detection state |
| **055** | engine speed · **idle regulator** (−2.00…+2.00 g/s) · **its adaptation** (−1.50…+0.150 g/s) · load state |

**Two groups, never three** — three drops the rate from about 1.7 samples a
second to 1.1.

⚠ **Expect `014` to read `deaktiv.` while the engine is cold.** Misfire
detection is usually disabled below a temperature threshold. **That is not a
wasted run**: the fourth field records *when* it switches on, which nothing here
knows yet.

**3. Start the engine exactly the way it is normally started.**

⚠ **Do not cycle the key to let the pump prime first.** A prime would mask the
symptom this is here to record. If the habit is to cycle it, cycle it — what
matters is that the start is the usual one.

**4. Two minutes of idle, undisturbed.** No throttle, air conditioning off,
nothing touched.

**5. Stop the capture and the log.**

**6. With the engine still running, photograph two screens:**

- **`006`** — intake air temperature and the **altitude correction factor**.
  Two numbers that turn a bounded estimate of volumetric efficiency into a
  figure.
- **`100`** — readiness bits and OBD status, which is what says whether the new
  converter has finished its monitors and emissions can be measured.

**7. Switch off.**

---

## Write down three things the log cannot hold

The capture gives engine speed through the start at about ninety-four samples a
second. It does not give what it sounded like.

1. **How many seconds it cranked before it caught** — an estimate is fine.
2. **Whether it caught cleanly or caught and nearly died.**
3. **Whether the first seconds were rough or settled immediately.**

Next week the same start with new injectors goes beside these, and the
difference will be legible without any analysis.

---

## Do not

- **Do not clear the fault memory**, before or after.
- **Do not read group 032.** The adaptations are already recorded — **−4.7 % at
  idle against +1.6 % at part load** — and they are stored in the ECU, so they
  did not move overnight.
- **Do not bother with 022 or 023.** They are knock retard per cylinder and
  nothing knocks at idle.
- **Do not run 070.** It is a *basic setting* block and would start an actuator
  test, which is not what this start is for.

---

## What comes back

| | |
|---|---|
| `coldstart_z1.txt` | **unfiltered** — four megabytes is nothing, and it may hold something nobody thought to ask for |
| the VCDS log | groups 014 and 055 |
| two photographs | groups 006 and 100 |
| the three notes above | in plain words |

**The capture is analysed the same way as the fixtures** — transient dips of
engine speed against a one-second median, counted and bucketed by the oil
temperature carried in the same recording. `docs/engine-health.md` holds the
existing numbers it will be set beside.

---

**This document has an end date.** When the parts are on and the results are
recorded in `engine-health.md`, it has done its job and goes away.
