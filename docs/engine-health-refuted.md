# Engine health — refuted hypotheses and answered questions

The companion of `engine-health.md`. **Every idea about this engine that was
put forward and then settled against**, with what settled it, and the
questions that were simply answered. It exists because each entry here was a
plausible idea once, and plausible ideas come back: read this before
proposing a cause.

The same two rules as `refuted.md`, which covers the firmware, the board and
the toolchain: **only settled things go in**, and **nothing is deleted**. If
new evidence un-refutes an entry, say so inside the entry and move the
hypothesis back to `engine-health.md`.

The detail behind every entry is in `engine-health-log.md`, cited as
*log, § …*. The entries are short on purpose.

**Strength of each refutation**, because they are not all equal:

- **measured** — a measurement on this car contradicts it
- **replaced** — the part was replaced and the symptom stayed
- **argued** — a measurement makes it very unlikely, but does not exclude it
  outright. Say what would revive it

---

## A. Causes of the idle stumble and the misfires

### A1. "The old injectors were dribbling, and that is the idle fault" — replaced

**Believed:** for most of the investigation; the leading explanation after the
burned-through converter, the −4.7 % idle trim and the cold overrun burble.
**Refuted by:** four new Bosch injectors (23/9) and the stumble and the
misfire counter both stayed (log, § *The post-repair drive*).
**What survives:** the old injectors probably did cause the cold-overrun burble
and part of the bad cold start (C1, C3). They were never bench-tested; they are
kept, labelled by cylinder. By inspection cylinder 1's nozzle was the dirtiest
and cylinder 4's the cleanest.

### A2. "Fouled plugs or tired leads" — replaced

Plugs and leads new on 17/9, misfires unchanged. The old plugs were worn out
after ~1,500 km, with 1 and 4 the worse pair; see A9 for what that pair means.

### A3. "The ignition coil" — replaced

New in 6/2026, and the idle misfires outlived it. (The historical full-load
misfire it was changed for is gone — C4.)

### A4. "A per-cylinder mechanical fault: burnt valve, broken rings, head gasket between cylinders" — measured

**Refuted by:** compression 12 bar, even on all four (garage, 17/9). The
evenness is the result; the absolute figure is weak. **Does not cover** a valve
that seats at cranking speed but not on a hot idle — that is H1 in
`engine-health.md`, and a warm leak-down test is its test.

### A5. "One bad cylinder dominates the idle roughness" — measured

**Refuted by:** the per-cylinder periodogram of engine speed (`idledips.py
--cylinders`). The period-4 line is just as strong in the smooth recordings as
in the rough ones (13.4× against 13.1×), and the four phase slots differ by
3.5–5.9 rpm with no consistent outlier (log, § *Is it one cylinder?*).
**Limit:** four cylinders equally bad leave nothing periodic, so "all four
together" is neither confirmed nor refuted.

### A6. "The evaporative purge" — measured

Block 070: TEV OK, lambda deviation 0.0 %. Also purge runs warm, while the
stumble was worst mid-temperature and present cold.

### A7. "A large intake (unmetered) air leak" — argued

**Refuted by:** the idle trim reads −3.1 %, slightly rich, on the new MAF. A
leak big enough to misfire a cylinder, and the misfires themselves (oxygen
through an unburnt cylinder), would both push it positive (log, § *The trim
argument is stronger*). **A small leak at one runner is not excluded** and is
H3 in `engine-health.md`.

### A8. "The secondary-air combination valve or N112 open at idle — air or exhaust between intake and exhaust (an uncontrolled EGR)" — measured

**Refuted by:** two owner tests on 25/9. Test 1: pump hose pulled off the valve
at a warm running idle, nothing pulsed out — the valve seals. Test 2: the thin
hose between N112 and the valve pulled off, cold — neither end passed air, and
the ECU set a secondary-air fault, which is the system behaving as designed
(log, § *What is on the car* and after). The P0411 of 11 August was a hose that
came off during the heater work, refitted since.

### A9. "Plugs 1 and 4 worse means injectors 1 and 4 were leaking" — argued

**Weakened past use.** The AQY has two twin-spark coils (SSP 233 p. 5), so 1
and 4 share one coil output and its leads; the old coil was probably original
and those plugs spent 3½ of their 4 years on it. Cylinder 4's old injector had
the cleanest nozzle. **The pair names a coil output, not two injectors.**

### A10. "Knock control is causing the idle stumble" — measured

No retard on any cylinder at idle in either knock log (0 of 443 idle samples
on 24/9), and group 026 sits at its floor at idle. The ECU changes nothing at
idle on account of the knock sensors, and misfire detection uses crank speed.

### A11. "The MAF swap made the idle worse" — measured

It came from the 014 counter, which read more at the hot idle after the swap.
**Refuted by:** engine speed. Dips at a standstill idle fell 51–65 % at every
oil temperature band; the counter was counting five to fifty times more per
dip. The ruler changed, not the engine (log, § *Did the 20 % threshold mask
the morning?*).

### A12. "Misfire detection's 20 % load threshold masked the morning's misfires" — measured

Real in kind, small in size: re-running the morning as if on the new MAF
loses at most a tenth of detection time. It does not explain the change of
counts per dip.

### A13. "The exhaust leak behind the converter affects the mixture or causes misfires" — argued

The rattling joint is downstream of both lambda probes, so nothing drawn in
there reaches either probe; this ECU meters fuel from the MAF's air mass, so
back pressure does not move the fuelling; and a leak outside the cylinder does
not stop it firing. Tightening the clamp did not move `IdleHealth`.

### A14. "A contaminated fuel supply is still feeding the injectors" — measured

Lines from the tank flushed with the filter off, and through the new filter:
clear petrol at every stage (23/9). The filter that came off was sound. The
older chain (dirty tank → holed filter → spoiled injectors) is **unresolvable
now**: the tank's replacement date is unknown and the old injectors went
untested. Parked, not refuted.

---

## B. The cylinder 4 knock window

### B1. "Cylinder 4 really knocks" — measured

**Refuted by:** the neutral test (25/9). Standing in neutral with a tenth of
full-throttle air, cylinder 4's 026 voltage still reads 40–70 % above cylinder
1 above ~2700 rpm. Knock needs cylinder pressure (*general*). Also argued
against by 100-octane fuel, five points above the RON 95 SSP 233 specifies.
**Not excluded:** a little real knock at full throttle on top of the noise;
the retard is within VW's 0–15 °CA either way.

### B2. "Cylinders 1 and 4 reading twice 2 and 3 means something wrong in both" — measured

The pair is the crank-symmetric one: pistons 1 and 4 move together, so a noise
once per crank revolution lands in both windows. The ratio is the same fired
and unfired, at every speed. How this engine's sensors hear its crank, not a
fault. Only 4's excess over 1 is open (`engine-health.md` S5).

### B3. "An exhaust leak ticking at cylinder 4's runner is what knock control hears" — measured

A leak needs exhaust pressure, and the excess is there with the throttle shut.
A crank-locked puff stays in one window at every speed, while the excess moves
to cylinder 1 above ~3350 rpm. And tightening the rattling clamp left it
unchanged.

### B4. "The rattling clamp under the driver's seat is the cylinder 4 noise" — measured

Same engine speed, so worth testing. Clamp tightened, neutral 026 holds
repeated: cylinder 4 still 25–60 % above cylinder 1 at the same speeds (log,
§ *After the clamp*).

### B5. "The camshaft sensor G40" — argued

SSP 233: on a G40 fault the advance is retarded for all cylinders as a
precaution. One cylinder retarding is not that.

### B6. "A dead or open knock sensor" — argued

It would set a fault code and retard all cylinders to be safe. No code, and
three cylinders read zero retard.

---

## C. Other things that were suspected and are settled

### C1. "The ECU does not cut fuel on a cold overrun, so the cold burble was commanded fuel" — measured

**Refuted by:** `coastscan.py` on `19_postfix_drive_z1`: the first coasts of the
morning, on oil at 13–22 °C, cut the injectors 1.20–1.34 s after the lift
exactly as warm. So the burble was fuel arriving with none commanded — the old
injectors — and it has not been heard since. Gap: coolant below ~60 °C, the
first two minutes of driving, has no coast recorded.

### C2. "The rich trim is from new injectors of a different flow class, from fuel in the oil, from a leaking seat, or from rail pressure" — measured / argued

**Answered: it was the MAF.** Swapping it took the trim from −16.4 / −13.3 %
to −3.1 / +4.7 % and air per commanded fuel back to August's value.
Separately: old and new injectors are the same part (`06A 906 031 C`, Bosch
`0 280 155 791`); fuel in the oil would need most of a litre of dilution and
the dipstick smelt of nothing; a seat leak is additive and the error was
multiplicative. **Rail pressure was never measured** — it is simply no longer
needed to explain the trim. It survives for the cold start as H7.

### C3. "The cold start is the fuel pump's check valve" — open, not refuted

Listed here only to say where it is: the cold start improved a lot on the new
injectors, which points at their seats, but the check valve is eliminated
only once the next overnight cold starts read clean (`engine-health.md` S7).

### C4. "The historical full-load misfire and warning lamp" — answered

The lamp used to come on after minutes above ~4500 rpm on the motorway. On
25/9, ~100 km with five minutes held at 4500 and bursts to 5000 on all the new
parts: no lamp, no hesitation. *Owner-reported.* Cleared on the new parts.

### C5. "The oxygen sensors failed again" / "the new converter is failing" — measured

034, 036, 037 and 046 all OK on 24/9; readiness all complete. The rear
probe is an independent witness against a front probe lying rich. The jingle
on the overrun was the clamp (B4); the knock test on the cold converter can is
still worth a tap next time the car is up, but nothing points at it.

### C6. "A thermostat stuck open, or a coolant sensor reading low, drives a warm-up enrichment" — measured

The coolant on 0x288 — the ECU's own figure — warms up to 99–100.5 °C like a
healthy engine. The oil channel feeds only the cluster and is not an ECU input.

### C7. "The throttle or pedal is being limited" — measured

The throttle reaches its mechanical stop, 85.1–85.5°, under load and with the
engine stopped.

### C8. "The MAF is badly under-reading" — measured

Volumetric efficiency at full throttle comes out at a normal 84–93 %. (It
turned out to be over-reading at idle, which is C2.)

### C9. "The cracked hose to the injector air shrouds" — argued

The shroud air is taken downstream of the MAF and is metered (SSP 233); the
hose runs near intake-pipe pressure; the cracks are in the surface rubber only.

### C10. "Group 014 is a lifetime total" — measured

It is a current count that holds about three seconds and returns to zero,
specified 0 to 5. The label `(celkovy)` is wrong.

### C11. "The engine is down on power" / "the torque display under-reads" — answered

The torque scale was measured off the full-throttle plateau and the firmware
now ships it (`can-decoding.md` question 8). The low peak on the display was
the old scale, not the engine.

### C12. "A warm idle that feels calmer is evidence" — method

A warm idle counted zero dips before any repair, so an impression formed there
has nothing to be calmer than. Compare only at matched oil temperature, with a
number.
