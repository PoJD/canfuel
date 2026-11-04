# Engine health — refuted hypotheses and answered questions

The companion of `open.md`. **Every idea about this engine that was
put forward and then settled against**, with what settled it, and the
questions that were simply answered. It exists because each entry here was a
plausible idea once, and plausible ideas come back: read this before
proposing a cause.

The same two rules as `docs/firmware/refuted.md`, which covers the firmware, the board and
the toolchain: **only settled things go in**, and **nothing is deleted**. If
new evidence un-refutes an entry, say so inside the entry and move the
hypothesis back to `open.md`.

The entries are short on purpose. The full reasoning behind them was the
long version of `open.md`, which is in git:
`git show 7c69883:docs/engine-health.md`.

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
misfire counter both stayed (post-repair drive, 24/9).
**What survives:** the old injectors probably did cause part of the bad
cold start (C3). *Until 4/10/2026 this read "the old injectors probably
did cause the cold-overrun burble and part of the bad cold start (C1,
C3)": the burble is back on the new ones, warm (C1, `open.md` S14).* They were never bench-tested; they are
kept, but **not labelled by cylinder** (this said "labelled" until
28/9/2026). By inspection at removal, cylinder 1's nozzle was the dirtiest and
cylinder 4's the cleanest (*owner*, numbering confirmed 28/9/2026); the loose
injectors can no longer be matched to those cylinders.

### A2. "Fouled plugs or tired leads" — replaced

Plugs and leads new on 17/9, misfires unchanged. The old plugs were worn out
after ~1,500 km, one visibly worse than the rest — **from which cylinder is
not known**, since they were not labelled. (This said "1 and 4 the worse pair"
until 28/9/2026; nothing recorded that pair. See A9.)

**The gap** (*the owner's question*, 2/11/2026: never measured, taken as
set in the box). How it would act (*general*): a gap closed up leaves a
small flame kernel that the thin, diluted idle charge lights badly — an
idle misfire; one opened up needs more voltage and fails under load
first. **Why it is not the idle** (*reasoned*): three sets from three
sources — Dakuma's of 17/9, NGK's box of 10/10, VW's of 21/10 — all the
same `BKUR6ET-10`, whose `-10` is NGK's code for a 1.0 mm gap set at the
factory (*general*), and the idle the same on every one of them (S1);
one wrong box is possible, three are not. And the `T` is NGK's code for
three ground electrodes, a plug made to be fitted as it comes, not bent
(*general*). Measuring one with a wire gauge would cost the plenum off
again for a doubt this small; not done. **3/11 evening, asked again by
the owner**, after `43` named cylinder 3 (`open.md`, *The dips keep to
one slot*): the three-boxes argument covers a set, not **one plug on 3**
closed up in the fitting or knocked on the way in, which would act on
that cylinder alone; *reasoned*. Still not measured; it would be read
with plug 3 itself whenever the plenum comes off (`open.md` H13); no
plug change for now (*the owner*, 3/11).

### A3. "The ignition coil" — replaced

New in 6/2026, and the idle misfires outlived it. (The historical full-load
misfire it was changed for is gone — C4.)

### A4. "A per-cylinder mechanical fault: burnt valve, broken rings, head gasket between cylinders" — measured

**Refuted by:** compression 12 bar, even on all four (garage, 17/9). The
evenness is the result; the absolute figure is weak. **Does not cover** a valve
that seats at cranking speed but not on a hot idle — that is H1 in
`open.md`, and a warm leak-down test is its test. **Weaker than it reads**
(4/11): VW allows 10–13 bar new and **3 bar between cylinders**, the reading
was cold, cranking, in whole bar, and taken on 17/9, before the cleaner,
S18 and the deposit on 3 seen breaking up — so it excludes a gross loss and
nothing finer.

### A5. "One bad cylinder dominates the idle roughness" — measured

**Refuted by:** the per-cylinder periodogram of engine speed (`idledips.py
--cylinders`). The period-4 line is just as strong in the smooth recordings as
in the rough ones (13.4× against 13.1×), and the four phase slots differ by
3.5–5.9 rpm with no consistent outlier. The unbiased per-cylinder spread
(`sd_true`) is 1.95 rpm rough against 1.09 smooth, a weaker separation than
the idle grade gives, and confounded with temperature.
**Limit:** four cylinders equally bad leave nothing periodic, so "all four
together" is neither confirmed nor refuted.
**Partly un-refuted, 9/10/2026** (`open.md`, *Naming the cylinder*, *The
dips keep to one slot*). The slot **means** still show no outlier, and that
stands. But the **dips** — the events this hypothesis was about — keep to
one slot: 256 of 720 pairs of dips in one phase-intact run fall on the same
slot, against a quarter by chance (p ≈ 2×10⁻¹⁰). A cylinder that stumbles
on a few per cent of its strokes hardly moves its mean, which is why the
periodogram could not see it. Not "dominates" — roughly 45 % of the dips on
one cylinder, by a model fit — but not four alike either. Back in
`open.md` as the question `plan.md` step 3.5 answers. **17/10/2026**:
the pair figures above were read on runs seconds long and run high; on
minutes-long runs the dips put about two thirds on **two** neighbours in
the firing order, and on `31`, where the cuts name the slots, those are
cylinders 4 and 3 (`open.md`, *One cylinder or two*). Still not four
alike, and still no outlier in the means.

### A6. "The evaporative purge" — measured

Block 070: TEV OK, lambda deviation 0.0 %. Also purge runs warm, while the
stumble was worst mid-temperature and present cold. *(9/10/2026: the
stumble is in fact roughest cold and present warm — `open.md` S1. The
refutation stands on block 070.)* *(24/10/2026: **partly reopened.** 070 commands the
valve open and reads the response, so it shows a valve that **opens**; it
cannot show one that **seals** without power, and 0.0 % says only that the
canister gave nothing at that moment. A leaking valve is back in `open.md`
as **H16**, for the rich idle trim and S19, not for the stumble. For the
stumble the refutation stands, on other grounds now: a dip is one firing,
and vapour reaches all four as an even flow — H16.)*

### A7. "A large intake (unmetered) air leak" — argued

**Refuted by:** the idle trim reads −3.1 %, slightly rich, on the new MAF. A
leak big enough to misfire a cylinder, and the misfires themselves (oxygen
through an unburnt cylinder), would both push it positive: one runner
leaking dilutes to a quarter at the one sensor, but a cylinder has to run a
long way lean before it misfires. **A small leak at one runner is not excluded** and is
H3 in `open.md`. *(25/10/2026: **stronger since.** P0172 stored on 24/10
says the ECU ran out of room taking fuel *away*, and VW's evaluation of
032 for this engine reads unmetered air from **high** idle values, never
low (`vcds.md`, block 032). A small leak still hides if a larger rich
source outweighs it: the trim is their sum.)*

### A8. "The secondary-air combination valve or N112 open at idle — air or exhaust between intake and exhaust (an uncontrolled EGR)" — measured

**Refuted by:** two owner tests on 25/9. Test 1: pump hose pulled off the valve
at a warm running idle, nothing pulsed out — the valve seals. Test 2: the thin
hose between N112 and the valve pulled off, cold — neither end passed air, and
the ECU set a secondary-air fault, which is the system behaving as designed.
From the owner's photographs the small hose on the valve runs to a second
module with its own connector, read here as N112 (SSP 233 p. 20 diagram);
its part number was not legible. The P0411 of 11 August was a hose that
came off during the heater work, refitted since.
**Test 3, owner-reported 27/9/2026:** the line from N112 to the valve pulled
off at a running idle — the state of every August recording — and
`IdleHealth` did not change. Date and oil temperature not noted. It closes
the one route by which the refitted line could have made September's idle
worse than August's (`open.md` S1).

### A9. "Plugs 1 and 4 worse means injectors 1 and 4 were leaking" — argued

**Weakened past use.** The AQY has two twin-spark coils (SSP 233 p. 5), so 1
and 4 share one coil output and its leads; the old coil was probably original
and those plugs spent 3½ of their 4 years on it. Cylinder 4's old injector had
the cleanest nozzle. **The pair names a coil output, not two injectors.**

**Premise withdrawn, 28/9/2026:** the old plugs were never labelled by
cylinder, so "plugs 1 and 4 worse" was never an observation — only that one
plug was worst, and not which. The entry stays refuted; there is now no pair
for either reading to explain.

### A10. "Knock control is causing the idle stumble" — measured

No retard on any cylinder at idle in either knock log (0 of 443 idle samples
on 24/9), and group 026 sits at its floor at idle. The ECU changes nothing at
idle on account of the knock sensors, and misfire detection uses crank speed.

### A11. "The MAF swap made the idle worse" — measured

It came from the 014 counter, which read more at the hot idle after the swap.
**Refuted by:** engine speed. Dips at a standstill idle fell 51–65 % at every
oil temperature band; the counter was counting five to fifty times more per
dip. The ruler changed, not the engine. Dips a minute at a standstill idle,
morning (old MAF) → afternoon (new MAF): 22.1 → 10.9 at 57–84 °C of oil,
14.5 → 5.1 at 84–92 °C, 21.4 → 8.7 at 92–111 °C.

*Added 3/10/2026 — why the ruler changed, reasoned rather than measured:*
in Bosch's misfire detection the roughness threshold depends on load
(`vcds.md`, block 014, *What the number is*), and this ECU computes load
from the MAF. The new MAF reads less air than the over-reading old one
(C2), so a lower load, a different threshold, and the same dip crossing
it more often.

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
untested. Parked, not refuted. *Added 10/10/2026* (*owner*): until the
summer of 2026 the tank held fuel about three years old, from before the
lay-up — a plausible source for what spoiled the old injectors, and not
one that is still there: the lines ran clear on 23/9.

### A15. "The crankcase ventilation or the cover gasket causes the idle" (`open.md` H9) — measured

**Believed:** 26/9/2026, when oil was found at the back of the head: a
breather or a cover joint open to the outside lets the crankcase draw air
past the MAF at idle.
**Half right, and settled for the idle.** The cover gasket *was* S10's
leak — first a hardened original, then a wrong part with an open arch —
and it is repaired (`open.md` S10, closed). But the breather was replaced
on 2/10 and the cover sealed with the right gasket on 4/10, and the
misfires were still counted that day, on a joint that stayed dry hot and
cold. **What is left of it** — the original breather hose and its plastic
connector — is an ordinary unmetered-air point, H3's, and the intake
smoke test covers it (`plan.md` step 2a). **What would revive it:** smoke
at the breather's own seat or the new gasket's joint.

**The original breather hose seen off the car, 12/10/2026** (*owner,
photographed*: `photos/breather-hose-2026-10-12-*.jpg`): `06A 103 493 N`,
its larger end on the breather, its cuff on the intake hose behind the
MAF (*owner*). **The cuff's moulding seam has opened into a split at its
end**, the cuff's edge is torn in places, the outside of the bend by the
tee is crazed, and the inside carries oil and deposit — **a black,
sticky layer about 0.5 cm deep round the inside, oil with dust or other
dirt, not oil alone** (*owner*, 12/10/2026). Where the dust came from
was not established; the airbox crack let unfiltered air in ahead of
the MAF, and this hose's cuff sits in that stream (*reasoned*, not
shown). A split under a
clamp can open with heat and movement. **It does not revive this
entry**: the cuff sits on the intake ahead of the throttle, at
intake-pipe pressure, where a split draws little at idle (*reasoned*, as
C9), and whatever it draws reaches all four cylinders alike. **Blown
through with the far end stopped, it holds** (*owner*), so the split
seam does not go through. **Replaced with a new one all the same**
(*owner's decision*, 12/10/2026): cleaning would not take out years of
deposit inside, and the hose is worn. *This entry first said it was
kept and cleaned, a new one being too slow to come.*

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
fault. Only 4's excess over 1 is open (`open.md` S5).

### B3. "An exhaust leak ticking at cylinder 4's runner is what knock control hears" — measured

A leak needs exhaust pressure, and the excess is there with the throttle shut.
A crank-locked puff stays in one window at every speed, while the excess moves
to cylinder 1 above ~3350 rpm. And tightening the rattling clamp left it
unchanged.

### B4. "The rattling clamp under the driver's seat is the cylinder 4 noise" — measured

Same engine speed, so worth testing. Clamp tightened, neutral 026 holds
repeated (`vcds/vcds-neutral-026-003-clamp.csv` against
`vcds-neutral-026-003.csv`): cylinder 4 still 25–60 % above cylinder 1 at the
same speeds.

### B5. "The camshaft sensor G40" — argued

SSP 233: on a G40 fault the advance is retarded for all cylinders as a
precaution. One cylinder retarding is not that.

### B6. "A dead or open knock sensor" — argued

It would set a fault code and retard all cylinders to be safe. No code, and
three cylinders read zero retard.

### B7. "Injector 4's click, coupled into the block while only it was seated, is what knock control hears" — measured

**Believed:** 27/9–9/10/2026 (`open.md` H5): every knock log was taken
while only cylinder 4's injector was fully home, and a rigidly coupled
injector's click would reach the sensor strongest. **Refuted by** step 2c,
9/10/2026, the first knock log with all four seated
(`vcds-step2c-020-026-003.csv`, `30_step2b_z1.txt`): 020 retarded
**cylinder 4 alone** while driving — 9.5 % of samples, up to 13.5 °CA,
against 2.1 % and 5.2 °CA on 25/9, on a harder drive (to 6,010 rpm) —
with cylinder 1 at five samples above 4000 rpm and 2 and 3 at zero; and
in the neutral holds 026 still read cylinder 4 **19–28 % above cylinder 1**
from 1400 to 3350 rpm (the 25/9 holds 25–57 % by the same cut), handing
over to cylinder 1 above ~3350 rpm as before. Neither moved nor spread.
**Not excluded:** that seating 1–3 took some of S5's excess away, which the
smaller ratio would allow; it did not take it off cylinder 4.

---

## C. Other things that were suspected and are settled

### C1. "The ECU does not cut fuel on a cold overrun, so the cold burble was commanded fuel" — measured

**Refuted by:** `coastscan.py` on `19_postfix_drive_z1`: the first coasts of the
morning, on oil at 21–33 °C, cut the injectors 1.20–1.34 s after the lift
exactly as warm: in `17_drive_property_z1` the four warm cuts shut
1.19–1.30 s after the lift and gave fuel back at 1700–1754 rpm. So the burble was fuel arriving with none commanded — the old
injectors — and it has not been heard since. Gap: coolant below ~60 °C, the
first two minutes of driving, has no coast recorded.

**Un-refuted in part, 4/10/2026** (`open.md` S14): the measurement above
stands — the ECU does cut fuel cold — but **the conclusion drawn from it
does not.** The owner hears the same sound, warm, on the new injectors,
on a downshift without a blip, one to two seconds after the clutch comes
up. The cut comes 0.78–1.39 s after the *pedal*, so that can fall before
it, where the bang is a fuelled charge that did not fire rather than
fuel nobody commanded. "The old injectors, and not heard since" was
wrong on both counts.

### C2. "The rich trim is from new injectors of a different flow class, from fuel in the oil, from a leaking seat, or from rail pressure" — measured / argued

**Answered: it was the MAF.** Swapping it took the trim from −16.4 / −13.3 %
to −3.1 / +4.7 % and air per commanded fuel back to August's value.
Separately: old and new injectors are the same part (`06A 906 031 C`, Bosch
`0 280 155 791`); fuel in the oil would need most of a litre of dilution and
the dipstick smelt of nothing; a seat leak is additive and the error was
multiplicative. **Rail pressure was never measured** — it is simply no longer
needed to explain the trim. It survives for the cold start as H7.

**What is known about the old MAF, and what is not** (*the owner's
question, 11/10/2026*). The over-read rests on **one morning**: the
drive of 24/9 on the new injectors, compared with the new MAF the same
afternoon. **The same MAF had 032 at −5.5 / 0.0 % on 20/8 and −4.7 / +1.6 %
on 10/9** — fine (*this said "in August" for the second, until the
owner's photo dated it*).
So either it began to over-read between August and 24/9, or it already
did and the old injectors were delivering correspondingly less fuel per
millisecond, which hid it (*reasoned*: air per commanded fuel is the MAF's
error times the injectors' flow, and both changed that week). The data
cannot tell those apart, so **"the old MAF always over-read" is not
established**. And **an over-reading MAF is not a rich engine** while the
lambda loop is in control: a trim of −16 % is the ECU taking that fuel
back out, keeping the mixture at λ = 1 (*general*). It could have run
rich only where the loop is not in charge — warm-up before the probe is
hot, and after a battery disconnect until the trims were learned again.

**What the bus says about the old MAF — 11/10/2026** (*the owner asked
for more*; `tools/fuelratio.py`). The ECU's fuel counter (0x480) divided
by the injection byte (0x288 b6) integrated over the strokes, at a warm
standing idle. ~~A reading of how much the ECU takes away from the fuel
its MAF asks for~~ — *refuted the same day by the injector cuts of `31`:
both fields carry the lambda correction, so the ratio is not it.* What
is left is that the two fields part only on that morning, on the old MAF,
and why is not known:

| warm standing idle | MAF | injectors | ratio |
|---|---|---|---|
| August, `09`, `11`, `12` | 2018 | old | 0.30–0.32 |
| 24/9 morning, `19`, the first 35 min | 2018 | new | 0.27–0.29 |
| 24/9, the end of `19` and all of `20`, after the full-throttle pulls | 2018 | new | **0.20–0.23** |
| every capture since, `24`–`31`, hard drives included | new | new | 0.30–0.34 |

VCDS 003 agrees, at the same throttle plate (2.2°): **the old MAF read
3.5 g/s at a hot idle early in `19` and 4.75 g/s at its end**, against
about 3.2–3.3 on the new one. The fuel per intake stroke on the counter
did not move — 11.7 µl in `19`, 11.3 in `20`, 11.4 in `24`. **Same fuel,
same throttle, a third more air on the gauge.**

*Reasoned* (from the VCDS air and the counter, not from the ratio):
**on 24/9 the old MAF over-read, by about a third on the hot idle after
hard driving** — it drifted with heat — while the lambda loop kept the
fuel where it belonged; the counter carries the loop's correction (the
cuts of `31` show it), so the same fuel per stroke is the same mixture. The new one does not drift
(`28` and `30` are hot idles after hard drives). **August reads normal**,
and cannot say more: either the sensor was still fine, or the old
injectors' under-delivery cancelled it; and no August capture has a hot
idle after hard driving, which is where the fault showed. The second
reading has one thing for it: **it explains why the trims appeared the
day after the injectors** without a coincidence — new injectors that
deliver what they are told uncover a MAF the worn ones had been hiding.

**Why it was the MAF and not the injectors** (*the owner's question,
11/10*): the injectors were already in for the morning drive, and **the
same injectors** gave −16 % in the morning and −3 % in the afternoon,
with the MAF the one part changed between. And the injectors did not
calm the idle either — the morning, the first drive on them, is the
roughest warm idle on record (S1).

**What it does not explain is why the dips halved with the new MAF.**
The fall held: standing warm idle, dips a minute by oil band
(`dipcontext.Capture.dips()`), 13–19 on the old MAF (`19`, `20`) and
6–14 in every capture since (`24`–`31`). **Everything else the bus and
VCDS show of a dip is the same on both sensors** (11/10/2026): the
fuel per stroke; the dip's depth and shape, and the trim before it
(`dipcontext --profile`, `19` against `26`–`31`); the injection byte's
spread within 2 s and its wander within 10 s; VCDS's scatter of the
air; the advance at a warm idle (0.8–1.5° on both). And the dip rate
inside `19` did not follow the size of the correction. So the old MAF
changed **how often** the margin was crossed and nothing visible about
**how**. Two candidates, *reasoned*, neither shown:
- **the lambda loop's swing scaled up.** The correction multiplies the
  fuel the MAF asked for (*general*), so with the base a tenth to a
  third too large, a swing of the same few per cent is that much larger
  in real fuel — a deeper lean swing, which is where the dips sit
  (S1, *What comes before a dip*). It needs the probe on the scope
  (H11 test 2) to see.
- **the load the ECU computes from the MAF** feeds the idle governor's
  torque model and the misfire thresholds — and 014 did count
  differently after the swap (A11).
Neither excludes a third: the swap took the intake hose off and on. **A test, if wanted:** the 2018 unit is kept; refitted
for one session (hot idle, a hard drive, hot idle, VCDS 002 and 033) it
says whether that sensor drifts with heat or the morning had another
cause.

### C3. "The bad cold start is the pump's check valve, or still there" — answered: it was the old injectors

| | stand | injectors | crank to first firing | after first firing |
|---|---|---|---|---|
| `18_coldstart_z1`, 11/9 | ~10 h | old | 1.24 s | 451 → **311** rpm, nearly died |
| `19_postfix_drive_z1`, 24/9 | ~19 h, 10 °C | new | 0.83 s | 450 → **331** rpm, caught |
| 25/9 morning, display | ~12 h | new | 0.77 s | clean |
| **26/9 morning, display** | **~10 h, cold fog, `StartClt` 14 °C** | new | **0.93 s** | **`StartDip` 74 rpm**, clean |
| **3/10, `25_sessionA_cold_z1`** — after the injector refit and the new throttle | **27 h**, coolant 17 °C (`StartClt`) | new | **0.77 s** | **`StartDip` 15 rpm**, clean |

*`18`, `19` and 3/10 are measured through `idledips.health_summary()`; the
display rows are owner-reported.* **3/10 is the closest like-for-like with
`18` there is**: nearly the same coolant (raw 88 against 86) and a stand
almost three times as long, and it fell 15 rpm where `18` fell 141. The near-stall has not come back on the new
injectors in any cold start, and the 26/9 start matches `18`'s ~10 h stand
at a similar temperature. **So the rail bleed-down was the old injectors'
seats, and the pump's check valve is not needed as an explanation** — it was
never measured, so "not needed" is the strength of this, not "refuted". A
residual fall of 74 rpm on a cold engine has no healthy reference to be
judged against; `StartDip` over many mornings is the instrument
(`docs/firmware/frames.md`, 0x604).

### C4. "The historical full-load misfire and warning lamp" — answered

The lamp used to come on after minutes above ~4500 rpm on the motorway. On
25/9, ~100 km with five minutes held at 4500 and bursts to 5000 on all the new
parts: no lamp, no hesitation. *Owner-reported.* Cleared on the new parts.
**15/10/2026, harder still**: about 10 minutes held at ~5000 rpm in 6th at
full throttle on the motorway, pulls to the 6500 rpm limiter in 2nd, no
lamp (*owner*). **The lamp was on the remap**, after 6/2018 (*owner*,
18/10/2026), so the remap had not switched off misfire detection under
load (`open.md` H14 route 6).

### C5. "The oxygen sensors failed again" / "the new converter is failing" — measured

034, 036, 037 and 046 all OK on 24/9; readiness all complete. The rear
probe is an independent witness against a front probe lying rich. The jingle
on the overrun was the clamp (B4); the knock test on the cold converter can is
still worth a tap next time the car is up, but nothing points at it.

**The front probe at a standing idle, 4/10/2026** (033's voltage in
`vcds-sessionB-014-055-033.csv`, 685 samples below 900 rpm, one every
0.9 s): it **swings the full narrowband range**, 0.075–0.725 V between
the 5th and 95th percentile, **53 % of samples lean and 47 % rich** — a
probe switching evenly about its set point, not a lazy one stuck in the
middle or on one side. 41 crossings of 0.45 V a minute is at the
sampling's own limit, so it switches at least that fast. **The 83 rises
of 014 fall on both sides**: the voltage just before them was lean
(< 0.45 V) for 42 and rich for 41, and the live correction ran −7 to
+7 % — so the misfires do not wait for a lean swing. *Sharpened 11/10/2026*
(`open.md` S1, *What VCDS saw just before a dip*): timed against the
dips on the bus instead of 014's rises, the correction just before a dip
is about 0.8 % lower than in quiet idle — a slight lean-going side,
on two sessions. Still nothing against the probes themselves. *What this does not
show:* a shift of the switching point itself, which an even swing hides;
that is what the rear probe (0.665–0.725 V at a hot idle, H2) and 032
near zero on a new MAF and new injectors guard against. Both probes date
from 10/2017, about 27,600 km (`vehicle-history.md`) — nine years of a
misfiring idle behind them, few kilometres.

**The rear probe is a witness only against the front one alone.** Both
shifted the same way would pass every test above; that case is open as
`open.md` H11 (10/10/2026), bounded there by the trims rather than by the
probes.

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

**Seen again at the job, 1/10/2026** (*owner, photographed*): the shroud
rail out of the car, its four rubber sleeves printed `06A 133 264`, **deeply
crazed and cracked** on cylinders 2, 3 and 4 alike, cylinder 1's in the
best state (*owner*), worst where they bend over the nipples — further
gone than "surface only", though whether any crack goes through was not
established. The argument above still stands: the supply is taken from the
intake hose ahead of the throttle, so the rail sits near that
pressure and a crack in it admits little that is not already metered
(*reasoned*). **The owner replaces the sleeves rather than refit them**
(*owner's decision*) — cheap, and it ends the question. The genuine
sleeve was not in stock anywhere in Prague on the day; **the old sleeves
measure 15 mm outside, 8 mm inside, 47 mm long** (*owner-measured,
1/10/2026*), so a length of 8 mm bore vacuum hose cut to four 47 mm
pieces is the stand-in if the original does not come; the nipples on the
injectors and on the rail are 8 mm at their narrowest, with a barb that
holds the sleeve (*owner-measured*). **Fitted 1/10/2026**: 8 mm bore
vacuum hose cut to four 47 mm pieces, onto the injectors first and then
the rail into them, oiled; soft against the old ones' hardness, and they
hold firmly over the barbs (*owner*) — *a decision, not
VW's part*. *What would revive
this entry:* a sleeve split through on the injector side, where the nipple
opens to the port.

**Seen again 12/10/2026, the supply hose** (*owner, photographed*:
`photos/shroud-supply-hose-2026-10-12-*.jpg`): the thin hose from its
own port on the intake hose just behind the MAF to the rigid shroud
pipe (*owner*, 12/10/2026; *this read "from the breather's connector
behind the MAF"* — it does not join that connector), the one
the sleeves hang off, original (moulded date 1999). Clean inside, **its
surface crazed with fine crossing cracks**, one of them darker and more
open. Blown into with the far end stopped, **a little air may have gone
out somewhere** — the owner cannot say it was not imagined, and if it
was real it was very little. Whether any crack goes through was not
settled; the owner reads the damage as surface, the rubber porous with
age. **The argument above stands**: the hose sits at intake-pipe
pressure ahead of the throttle, on air the MAF has already metered.
Replaced (*owner's decision*) — no VW number readable on it, the white
print is smeared, so a hose of the same bore: **8 mm inside**
(*owner-measured*), the same 8 mm hose the sleeves were cut from.

### C10. "Group 014 is a lifetime total" — measured

It is a current count that holds about three seconds and returns to zero,
specified 0 to 5. The label `(celkovy)` is wrong.

### C11. "The engine is down on power" / "the torque display under-reads" — answered

The torque scale was measured off the full-throttle plateau and the firmware
now ships it (`docs/firmware/can-decoding.md` question 8). The low peak on the display was
the old scale, not the engine.

### C12. "A warm idle that feels calmer is evidence" — method

A warm idle counted zero dips before any repair, so an impression formed there
has nothing to be calmer than. Compare only at matched oil temperature, with a
number.

### C13. "A cracked head, or a head gasket leaking, behind the oil leak, the smoke and the idle" — argued

**Believed:** never strongly; asked about on 26/9 as the one cause that could
sit behind S10, S11 and the idle together (it was H10 in `open.md`).
**Refuted by**, each on its own weak, together decisive:
- **the coolant level has held for weeks** (*and still, 4/11/2026, the
  owner*: no fall seen; a weep into cylinder 3 too small to show is
  `open.md` H20 since 4/11, at his request; a combustion-gas test of the
  coolant was never made), and **no milky emulsion** has
  ever been seen. (*Removed 30/9/2026, the owner's correction:* this also
  read "the underside of the oil filler cap is clean (*owner-observed,
  27/9/2026*)" — the cap was most likely not looked at that day, so it was
  never an observation.);
  *Added 23/10/2026, the owner:* **at the oil change of 6/2026**, after
  about three years and nearly a year standing outdoors, **the cap's
  underside was slightly brown with condensed water**, which he reads as
  condensation and not coolant. So "never seen" stands for coolant
  emulsion only; condensation under the cap of an engine that stood
  outdoors is the ordinary case (*general*), and the job of 1/10 found
  none;
- compression 12 bar and even on all four (A4); the coolant warms to
  99–100.5 °C and holds it; the cold start is clean (C3), where coolant in a
  cylinder shows worst (*general*);
- the dipstick sat at atmospheric with the engine running (`open.md` H9
  test 3, cold) — combustion gas into the crankcase would push there;
- and nothing is left for it to explain: S10 is the valve cover gasket,
  found and photographed on 26/9, and S11's smoke is most likely that oil
  on the manifold.

**Strengthened at the job, 1/10/2026** (*owner, photographed*): with
the valve cover off, **no emulsion anywhere** — not under the cover, not
on the cam or the caps; the dipstick and the filler cap's underside
clean of it the same day. The cover's underside carries only a thin
golden-brown film, the ordinary varnish of hot oil (*general*).

**Not done:** a combustion-gas (CO₂) test of the coolant and a warm
leak-down. **What would revive it:** coolant going down, emulsion under the
cap or the valve cover, bubbles in the expansion tank, or a garage smoke test
that places S11's leak at the head-to-block joint.

### C14. "The breather sits on no seal, and neither does the filler cap" — measured

**Believed:** preliminarily, 30/9/2026, from a quick look before anything
came off (`open.md` S10, H9), as a concrete door for unmetered air and for
the oil on the breather's lower body.
**Refuted by** the job itself, 1/10/2026 (*owner, photographed*): a flat
ring (VW item 5) under the breather, notched on its inner edge, and the
cap's seal built into the cap's body. *Corrected 2/10/2026 by the owner's
photograph: the cap's seal is a separate plain ring seated in the cap,
not part of its body — it was there either way.* **What would revive it:** nothing —
the parts were in hand. The door H9 now points at is the breather's body.
*2/10/2026: not the patch on it, which is original — C15.*

### C15. "The patch on the old breather's body is a past repair" — measured

**Believed:** 1/10/2026, from the old breather out of the car (`open.md`
H9 test 4): a black patch where the body meets the hose spigot, askew and
lifting at the edge, read by the owner as not original and so as the
cover over an earlier breach — the concrete door for unmetered air.
**Refuted by** the new part, 2/10/2026 (*owner*): **the new `32452`
carries the same patch, looking exactly the same**, so it is how the part
is made. **What would revive it:** nothing about the patch as such; a
patch on the old part that came away from the body, or a crack found
under it, would be a fault of that patch rather than a repair.

### C16. "The throttle's routine at every ignition-on is a fault of the old part" — measured

**Believed:** 28/9/2026, as symptom S13 (`open.md`): VW's manual gives
the adaptation at most 10 s and repeats it only after an interrupted one,
so a 20–30 s routine at every ignition-on looked like an adaptation that
never completes, or a worn unit.
**Refuted by** the new throttle, Pierburg `7.03703.13.0`, 2/10/2026
(*owner-timed*): after its own 098 ended *ADP OK*, it ran **the same 20 s
routine** at the next ignition-on, as the old part did before and after
its completed 098 on 29/9. It is how these parts behave. **What would
revive it:** a throttle of this family that stays silent at ignition-on,
or a routine that lengthens.

### C17. "Elring `325.070` is the valve cover gasket for this engine" — measured

**Believed:** 27/9/2026, when the parts were ordered: the shop's catalogue
matched it to the car, a Golf IV 2.0 / 85 kW, and it went on 2/10.
**Refuted by** the part itself, 3/10/2026 (*owner, photographed*): at the
half-moon it has an open arch where this head needs a solid half-moon, so
it leaked a stream of oil at cylinder 4's end on the first warm run, and
it lacks the metal sleeves the old gasket has. Catalogues list it for
AZJ, BER, AZG and AEG, not AQY (D5). **The general
lesson:** a match by vehicle is not a match by engine code. **What would
revive it:** nothing about this head; it is a different part.

### C18. "The open cover joint cost 18–30 % of torque under load" — measured

**Believed:** 4/10/2026, from session A (`open.md` S10, *Under load it did
bear*): at b5 80 and above, 0x280 b7 on 3/10 read 18–30 % below `19` and
`24` at the same engine speed and b5, and the 1 cm hole into the crankcase
was taken to be air the MAF did not see.
**Refuted by** the run after step 1b, 4/10/2026 (`27`/`28`, the same bins,
driving, oil above 77 °C, at least 30 frames each), **with the joint
sealed and dry**: b7 reads where 3/10 read, not where `24` did — 94 against
92 at 1500 rpm and b5 80–89, 96 against 96 at 2000 and 90–99, 82 against
94 at 2500 and 90–99. **What the comparison missed:** the throttle body
was replaced between `24` and `26`, and **b5 is its own sensor** — at
idle it reads **35 on the new part and 38 on the old** in every log either
side of the swap. So equal b5 is not equal opening across the swap, and
the deficit belongs to the new part's scale, not to the hole. At full
throttle, where b5 saturates and the scale cannot matter, b7 is 175–183
against `24`'s 177–185. **The general lesson:** a byte read off a part
compares only while the part stays the same. **What would revive it:** a
part-throttle deficit between logs taken on the same throttle body.


### C19. "Why 014 is quiet on some idles and counts on others" (`open.md` H10) — answered at the owner's decision, 9/10/2026

**The question:** raised 4/10/2026 from sessions A and B. 014 read zero
at idle after some starts and counted after others, at the same oil
temperature.
**The answer, accepted:** **it follows 055's learned idle air value**
(field 3). While the value sits above about −0.93 g/s — freshly after a
battery disconnect and 098 — 014 reads zero; from about −0.95 on it
counts, warm or cold. In every session but one: 4/10 A at 0 to −0.92 and
zero counts, then counting from −0.95 after the hard drive; 4/10 B at
−1.17 and counting on a part-warm idle; 9/10 (step 2b, the first session
on kept adaptations) at −1.07 to −1.33 and **counting on the cold idle
straight after the start** and at every stop. No session on fresh
adaptations has ever counted on a cold idle; none on settled ones has
been quiet.
**How strong:** a correlation in time, not tested. **Closed by the
owner** (9/10/2026, "more or less confirmed" by the count straight after
the start), without the battery-off test that would have shown it
directly (refused 6/10/2026: it says how the ECU comes to count, not
where the air comes from). What stood against it is kept: 3/10 counted
at −0.28 with the 1 cm hole open in the cover (S10, a cause of its
own); every quantity that grows with running time grows with the
learned value; the mechanism — the live regulator answering from a
narrower base, or the plate resting where this throttle's air is least
even — is reasoned and not shown.
**What it does not answer:** the fault. **Why the ECU learns air away**
stays open, with the candidates that could cause it — H3 (air the MAF
did not see) and H8 (a new throttle passing more at rest than the ECU's
model) — and most of the −1.1 g/s is not a leak at all: that much
unmetered air would make the idle about a third lean, against a trim
near −3 % (*reasoned*, 6/10/2026; VW: a run-in engine sits negative
anyway).
**The rule it leaves:** **a quiet 014 after a battery disconnect is not
evidence of a repair** until 055's learned value has walked past about
−0.93 again. Compare 014 only on settled adaptations. *Superseded 2/11
(below): the threshold is refuted; a reset does not reliably quiet it.*
**What would revive it:** a session with the learned value above about
−0.93 and 014 counting all the same (other than with a cause of its own,
as on 3/10), or one with it well past −0.93 and 014 at zero on an
unrepaired engine.
**A second explanation fits the same data — added 9/10/2026, after the
close** (`vcds.md`, *What VW says about the same detection*). The ECU
also learns the crank wheel's tooth errors, on the overrun, for misfire
detection itself. If a disconnect clears that too (not known for this
ECU), 014 would stay quiet after a disconnect until enough fuel-cut
overrun has been driven — and every session above fits that as well:
4/10 A had 13 cuts, mostly at 2,000–3,000 rpm, and counted only after
the hard drive added cuts from 3,500–5,300 rpm; **3/10 counted at its
first warm stop after 17 cuts**, which explains H10's one exception
without the hole. The captures cannot tell the two adaptations apart.
**The rule above holds either way** — a quiet 014 after a disconnect
is no evidence — but *which* adaptation turns the counting on is open,
and "it follows 055's learned value" is the less certain half of this
entry.
**26/10/2026 — evidence for the 055 half** (`idle-log.md`, 26/10;
`test/fixtures/vcds/vcds-step6a-055-relearn-014-055-001.csv`). After a
disconnect of about a minute, **032 was at 0.0 / 0.0 but 055's learnt
value still −2.78 g/s**, and **014 counted within the first 30 s of the
warm idle** and at every value down to −0.97. So **zeroed lambda
adaptations do not quiet 014** — "fresh adaptations" in the rule above
means 055's, not 032's. It does not test the tooth-error reading: a
disconnect that left 055 alone may have left that adaptation alone too.
The threshold itself — quiet above about −0.93 — is still untested from
the other side; the log ended at −0.97.
**27/10/2026 — the 055 half loses its mechanism** (re-read of
`vcds-sessionA2-003-014-055.csv` against the settled logs). In 4/10 A's
warm idles, with field 3 walking from −0.3 to −0.92 and **no count at
all**, VCDS 003 read **3.1–3.3 g/s of air, the plate at 2.6–2.8° and
2–4° of advance** — what the settled sessions read while counting
(`step2b-a3`, `step2c-home`, `step5`), with field 2 + field 3 at −0.9
to −1.2 in both (`open.md` H8). Same air, same plate, same ignition:
the engine was not being run differently while 014 was quiet. Nor was
it smoother: `IdleHealth` 72–74 on `28` (`open.md` S1's table) against
63–89 on the settled sessions around it. **So the quiet after a reset
reads as the detector's own state, which is the tooth-error half**, and
it ended in 4/10 A's hot stop after the hard drive's overrun cuts.
Still a correlation; **what separates them**: after a real reset, warm
up and settle 055 at idle with no overrun cut above about 2500 rpm
(clutch down on every lift), then 014 at a warm idle — quiet with 055
settled says the tooth errors; then a few cuts from 4000+, and counting
again confirms it.
**2/11/2026 — the 055 half refuted, and the quiet day an exception**
(*the owner's question*: a week ago, on zeroed adaptations, 014 counted
as before). Re-read of 27/10's drive home after hours off
(`vcds-step6l-2-014-055-003.csv`, `vcds-step6l-settle-014-055-003.csv`),
which the 27/10 entry above had not used: **field 3 at 0.00 to −0.28 the
whole 44-minute drive, and 014 counting all the same** — on the road from
the sixth minute, and **21 times in 11 minutes of idle**, about 120 an
idle hour; then **7 more on the settling stops at −0.56 to −0.99**. The
settled sessions count about 90 to 1,400 an idle hour, most 100–400
(every 014 log in `test/fixtures/vcds/`). So the condition under *What
would revive it* is met: **055 above −0.93 does not quiet 014.** Of the
three sessions on fresh idle air, **3/10 counted** (the hole, S10),
**27/10 counted**, and **only 4/10 A was quiet** — the owner's reading,
accepted: an exception, whether the tooth-error adaptation or something
not known; 27/10 cannot test the tooth errors (no capture, so its
overrun cuts before the sixth minute are not known). **The rule, now**:
a reset neither quiets 014 nor makes a counting one worse — 014 on fresh
adaptations compares with settled drives (*reasoned*, from these
sessions).
**4/10 A looked at again** (*the owner's question*, 2/11; captures `27`,
`28`, VCDS `sessionA2`, `sessionA2-hot`). **The detection was on**:
VCDS read *aktivováno* on 1,069 of 1,084 idle samples of the quiet part,
as on every counting session. **The engine was not cleaner**: at the
quiet A3 stop (oil 96–98 °C) dips of 35 rpm and more — about a whole
stroke lost (`open.md` S1, *What one dip is worth*) — came 0.4 a minute,
25 and more 2.4; after the hard drive, counting, 1.7 and 4.7; but **on
12/10 (`32`) and 21/10 (`40`) 014 counted with fewer deep dips than
4/10 A had while quiet** — 0.06 and 0.00 a minute of 35 and more, 0.9 and
1.2 of 25 and more (`idledips.py --thresholds 15,25,35` over each hot
idle). So the quiet was the detector, not the engine. **Nor do the
overrun cuts separate it**: 3/10 counted at its first warm stop after 17
cuts, all shut at 2,000–2,900 rpm (`coastscan.py` on `25`), much like 4/10
A's 13 at 2,000–3,000 that left it quiet; only the hard drive's cuts from
3,500–5,300 rpm came before 4/10 A counted. What switched it on is not
known; it stays the one exception.

### C20. "The fuel pressure regulator does not answer its vacuum reference, or leaks through its diaphragm" (`open.md` H7) — measured

**Believed:** 25/10/2026, from 032's shape (low at idle, normal at part
load) and VW's "fuel pressure too high", with the regulator's vacuum hose
found cracked at its intake end.
**Refuted by** `plan.md` 6e, 25/10/2026 night, on a cold start with the
lambda regulation active (`idle-log.md`;
`test/fixtures/vcds/vcds-step6e-cold-2-001-032-033.csv`): the hose off
at the intake end, the tube closed, twice for about 40 s — **the
regulation stepped to −8.6 and −10.2 % within seconds and back to +3 to
+8.6 % when it went on**, the roughly 8 % step a regulator owes its
reference; **no fuel at the hose's free end** either time (*owner*),
nor on the warm idle earlier that day.
**What it does not refute:** the regulator's base pressure, the pump's
non-return valve and the injectors — the rest of H7, which only a rail
gauge reads.
**What would revive it:** fuel or its smell at that hose, or a repeat with
no step in the regulation.

### C21. "Fuel in the oil, boiled off through the crankcase ventilation, is the rich idle trim" (`open.md` H17) — measured

**Believed:** 25/10/2026, from VW's evaluation of block 032 for this
engine (`vcds.md`): a low idle learnt value with part load normal names
oil dilution first, and it goes away after a motorway drive or an oil
change — this car's 032, on oil about three years old.
**Refuted by** the oil change of 26/10 (two EPR flushes, fresh oil,
`idle-log.md`): **032's idle cell relearnt from zero to −8.6 % the next
evening, and read −8.6 / +5.5 % at about 200 km on the new oil**
(29/10), where it stood before the change (−8.6 / +7.8 % on 26/10);
the oil level has not risen on the dipstick either (`plan.md` 6i).
Moved here at the owner's decision, 29/10.
**What it does not refute:** a little fuel in the oil that moves no trim,
or a source that refills the oil within a day — the dipstick would show
the second.
**What would revive it:** the level rising on the new oil (`plan.md`
6i), or the idle cell moving towards zero after a later change.

### C22. "The remap's MAF scaling against the new MAF splits the trim and roughens the idle" (`open.md` H19) — measured

**Believed:** 28/10/2026, at the owner's request: 032's idle cell
negative and part-load cell positive since the genuine MAF of 24/9 read
as a MAF curve the remap was scaled for in 2018, with the 2018 sensor in
the car; ranked second for the idle from 28/10.
**Refuted by** the tuner's two whole flashes, original and remap,
compared byte for byte on 3/11: **the remap changed five tables, all at
high speed and the highest load, and no other byte** (`open.md` H14) —
no MAF curve; and by the drive on the original map (`42`): **032's idle
cell back at −6.3 % after one drive**, the full-load air the same on
both maps. Moved here at the owner's decision, 3/11.
**What it does not refute:** the MAF itself reading off its own true
curve, on any map — which is not this hypothesis but a sensor fault, and
the halved dips of 24/9 (C2) stand as measured.
**What would revive it:** nothing on the map side; the files settle it.

### C23. "The remap of 6/2018 roughens the idle or narrows its margin" (`open.md` H14, its idle half) — measured

**Believed:** 16/10/2026, at the owner's request, with his recollection
of a warning from the tuner; ranked first for the idle from 24/10, when
the dips spread over all four.
**Refuted by** the same files (C22): **the idle region of every changed
table untouched**, and the idle speed, the idle advance, the misfire
detection, the limiter and the overrun cut not touched at all — the
tuner's "the map should not affect the idle" (*owner*, 3/11) is what the
bytes say. The drive on the original map agrees on every channel the
map could move (`open.md` H14, the table). **014 at zero on that drive
is therefore not the map's** (S3): the fresh adaptations or the day.
Moved here at the owner's decision, 3/11; **H14 stays in `open.md` for
full load** (S4, S19's part-load cell), which the remap did change.
**What it does not refute:** an effect at idle through the adaptations
learnt on the remap — which the reset of 3/11 cleared anyway.
**What would revive it:** a read of the ECU showing it does not hold
the original after all.

---

### C24. "The NGK leads' plug ends grip loosely, on 3 and 4 above all, and make the idle" (`open.md` H15) — measured

**Refuted 4/11/2026, at the owner's decision.** **The VW leads went on
21/10** (`vehicle-history.md`), so no NGK plug end has been on the car
since; on them the dips spread at first (`40`, `41`, all four alike) and
then **went back onto one cylinder** (`42` 45 % on one slot; `43` named,
**cylinder 3, 43 %**). What the hypothesis names is gone and the symptom
stayed. Its own test said a returning *pair* would refute it; what came
back is one cylinder, on parts it does not describe. **Left over** and
kept elsewhere: plug 3 itself (its gap, `refuted.md` A2, reopened for
plug 3 alone, 3/11) and the high-voltage side in the dark (`plan.md`
item 7, H4). The VW plugs are the same NGK `BKUR6ET-10`; only the leads
and their ends changed.

**As it stood in `open.md` when it was refuted** (heading: *H15. The aftermarket leads (and plugs) — NGK plug ends that grip loosely, on 3 and 4 above all*):

*Added 17/10 at the owner's request; retitled 20/10* (it read *a set that fits
all four slightly wrong*). **The claim**: not one bad lead but **the NGK
design's fit on these plugs** — every set on the car since at least 12/2022
has been NGK (the invoice; `vehicle-history.md`), and the owner believes all
of them since 2018 were. A genuine VW set has never been on the car in his
time.

| S1 | S2 | S3 | S4 | S5 | S11 | S14 | S19 | S20 |
|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | ~ | — | ~ | ✘ | — |

**What it rests on:**

- **The plug ends of 3 and 4 came off far more easily** (*owner*, 19–20/10):
  by grip **2 > 1 > 3 ≈ 4**, 2 the tightest this time and on 10/10, 3 and 4
  almost without force. Oil was on all four threads, so oil does not explain
  it. The NGK ends click like rubber, with only a faint metallic click
  (*owner*). Lead 4 felt the least firm on 10/10, 12/10 and 15/10; re-seated
  on 12/10 it held better, "though not as a lead should", and was loose again
  by 19/10 (*owner*).
- **The old plug 4's terminal burnt black and pitted** (1/10), and the old
  lead 4's insert scored, its terminal set back (10/10) — what arcing at a
  loose end leaves.
- **The deposits on 3 and 4 need a cause of their own** (H13): the coil cannot
  pick them (outputs 1+4, 2+3), nor the crankcase gas (common intake); the
  plug ends are the only evidence of one.
- **Forum and search** (leads, not sources): one AQY owner cured by going back
  to "thick VW originals" (forum.vwgolf.pl t=522030); `06A 905 409 L`, the set
  ordered, a later revision of the factory `F`, thicker, with extra silicone
  by the intake (a vwvortex AEG write-up, not confirmed in a catalogue); a
  Beetle 2.0's Bosch plug end that arced and burnt out (newbeetle.org).

**Why it can still be wrong** (*general* and this car's):

- **The idle-versus-load argument holds only against a voltage fault.** At
  idle the manifold sits at about 0.35–0.4 bar absolute (the gauge's 18–19
  inHg), so the gap needs few kV but the thin, cool, diluted charge is hard to
  light: what it needs is spark **energy and duration**. Under load the gap
  needs tens of kV and the dense charge lights from almost any spark. So **a
  voltage fault** (cracked insulation, a damp boot) shows under load and in
  the damp; **an energy fault** (a loose contact, high resistance) at idle
  and cold. A loose end is the second kind.
- **The pattern outlived three NGK sets** — which H15 survives only as the
  design's fit, not a bad lead. Why the design would fail on 3 and 4 and not
  on 1 and 2 is not known.
- **The plug soot does not follow the pair**: 1 and 4 sooted, 2 lighter, 3 the
  cleanest (*owner's reading*, 20/10).
- **A once-per-cycle sound on the NGK set, none on the VW one** (*reasoned*,
  24/10, from two phone recordings): the gauge clip of 14/10 carries a
  strong component once every 720° (7.7 % of the level, steady across its
  two halves) besides an eight-per-cycle one; the recording of 24/10, on the
  VW leads, has neither — only one click per firing, all four alike. An
  arcing plug end clicks once per cycle (S18's reading). **Not a
  comparison**: other place, 924 against 810 rpm, a clip of 10 s.

**The idle against every time the leads were handled** (the like-with-like
table in S1): the calmest settled idles, **12/10 and 15/10, came in the days
after the new set and lead 4's re-seat**, and it worsened from there — the
shape of a fresh grip working loose, and also of the cleaner and the
episodes, on the same days. A hint, not a test.

**The relief after each plug change, and how long it lasts.** *The owner's
reading*: new plugs help while good, and the poor combustion spoils them (the
12/2022 set came out eroded at ~1,500 km). *The second* (*reasoned*): every
plug change re-seats the leads, and a fresh end grips, then works loose.
**They are told apart by how long a relief lasts.**

**Test:** **the VW set `06A 905 409 L` with VW plugs `101 000 033 AA`**,
21/10, **the only change on the car** (`plan.md` 6b): at the refit, for each
cylinder the force each end takes and whether it clicks metal or rubber; the
first drive captured from the laptop, with the two states at its warm idle;
then more drives. Read against 19/10 (loads off ~100, on ~50) and 12–15/10
(~60):

- **calmer, the dips off 3 and 4 (towards a quarter each), 014 counting less,
  lasting weeks** → it was here; the ends are checked by hand after a few
  drives;
- **calmer for a few days, then back**, as after 10/10 → the relief was the
  seating, not the design: H3 next;
- **the same** → H15 refuted, and H4's spark side with it.

**Fitted 21/10/2026** (*owner*). **The VW plug is the same NGK
`BKUR6ET-10` as the set of 10/10** — its box says so — so the plugs are
only new, not different, and **the leads are the one real change**. The VW
leads are much stiffer than the NGK
set, and **each VW plug end carries a small rubber ring inside**, where it
seats on the plug; the NGK ends have none. A difference in exactly the
part H15 is about, seen before any drive; what it does to the grip is the
refit's measurement, not this.
**The refit** (*owner*, 21/10): every VW end on with about the same
force, an audible click, and **no play at all**, where the NGK ends had a
slight play on 3 and 4, perhaps 1 — the cylinders whose dips and deposits
stand out. The leads routed clear of the plenum, 3's above all.

**The least it predicts** (*owner*): the idle back at least where it was
before the episodes, loads off about 70–90 at 95–100 °C.

**Read 21/10 (`40`, one drive): not the main cause** (*owner*, 21/10).
Loads off 67 ± 2 hot, **level with 12–15/10 and not better**; 014 next to
15/10; loads on and cold the calmest recorded. The least it predicted is
met, the *calmer* is not. **One thing is not yet read the same way**: the
dips spread out, top two 58 % at p 0.77 — the first capture since 11/8
where the pair does not show; but 157 dips, one drive, and `24` read
p 0.4 once before. **`41` (24/10) spread too** (55 %, p 0.77). **The upper plenum gasket was renewed the same day**, so
the leads were not the only change. **Kept, demoted**, for a share: if the
captures after item 6 keep the dips spread, the leads took the pair away
and left the level — a part, not the whole (*More than one at once*); if the
pair comes back, H15 goes to `refuted.md`. **`42` (3/11, the original
map) did not spread**: 45 % on one slot, top two 68 %, p 0.023 — one
capture, on a changed map, and one slot fitting a little better than a
pair (*The dips keep to one slot*); not the pair this asks for. **`43`
named the slot** (3/11 evening): **cylinder 3, 43 %**, 4 at 18 % — one
cylinder on the VW leads, not the pair; against H15's NGK ends (none
fitted), not against what sits at 3's plug end anyway.

## D. Symptoms closed

Moved out of `open.md` when it was condensed, 20/10/2026. Each was closed at
the owner's decision; the full entries, with every measurement, are in
`git show d327332:docs/engine-health/open.md`. **Heard or seen again → it
reopens in `open.md`.**

### D1. S6 — the exhaust is not tight — closed 12/10/2026
The joint behind the converter: the pipes read 54.2 and 55.0 mm against the
connector's 55 (*owner-measured*), so the narrower one moved in it even fully
tightened. Shimmed with thin stainless sheet and exhaust sealant on 12/10
(`photos/exhaust-joint-2026-10-12-*.jpg`) and not heard since; it lies behind
both probes, so it was never the idle (A13). Heard again → the hangers, then a
welded joint.

### D2. S7 — the cold start — closed 26/9/2026
Fixed by the new injectors (C3). Of 14 captured starts in `24`–`38`, 13 had
`StartDip` 0 and one 15 rpm, cold and warm alike; crank to first firing
0.69–1.38 s, a spread rather than a trend.
**24/10/2026, one bad start, kept closed** (*owner's decision*): after
about 4 hours parked outdoors, nose uphill, it caught and died at once, as
if without fuel; the next start and every other that day normal, the first
such in about a month. Not captured. A tank just filled to 51 l makes a
pickup starving on the slope unlikely (*reasoned*); a rail that lost its
pressure while standing fits (*general*), as does the first tank of Orlen
Verva 100 (`idle-log.md`, 24/10). **Another → S7 reopens.**
**25/10/2026: reopened** (*owner*): the cold start of the morning died at
once again, the second ran. Back in `open.md` as S7; this entry stays as
its history.
**31/10/2026: closed again, as the fuel** (*the owner's decision*,
30/10: one clean cold morning on OMV would close it). **Reopened**: of the
eight first starts after a stand on Orlen Verva 100 with the second can of
BG 44K (24/10 afternoon to 29/10 afternoon), six were bad — caught and
died (24, 25, 28/10 afternoon), carried by a held starter (26/10,
`StartDip` 218), did not fire at all in 3–4 s (29/10 morning), caught a
little (29/10 afternoon, `StartDip` 103) — one hesitant (27/10, primed)
and one about clean (28/10 morning). Primed and plain alike, so not a rail
draining while standing; after hours outdoors and out of the garage alike.
**On OMV MaxxMotion 100plus**, filled 29/10, four in a row without a fall:
30/10 morning after 16 hours (`StartCrank` 0.77 s, `StartDip` 0, coolant
20 °C; a slight hesitation, about 8 km of OMV in the lines), 30/10
afternoon (0.70 s, 0, coolant 38 °C, about 30 km on OMV) and evening
(clean, not read), and **31/10 morning after about 12 hours in the garage,
cold: about 0.7 s, `StartDip` 0, coolant 22 °C, oil 26 °C, 17 °C in the
garage, the battery 12.6 V** — in the 18–25 °C band where the Verva's
starts failed, and clean as before 24/10 (*owner*, album). At the Verva's
rate four clean in a row is a chance of well under one in a hundred
(*reasoned*). **The Verva or the 44K in it**: the OMV fill ended both, so
they are not split; the day on 44K in OMV (23–24/10) had no bad start,
which leans weakly to the Verva. What the fuel did is not known — the
reasoning offered while it was open (vapour through N80's small leak,
H16; deposits wetted by the cleaner, H13) is in the full entry. **Not
the cause**: the hose of 25/10, the oil of 26/10, the cable and pedal of
27/10, the clearing of 24/10 night (all after the first bad start); the
plugs and leads of 21/10 (clean starts until 24/10). The full entry, every
start with its figures: `git show 3a8121f:docs/engine-health/open.md`,
S7. **Another bad start on OMV → S7 reopens**, on the engine or the map
(H14, H7) — with one thing to read first: **5–6 l of the same OMV from a
can, filled 8/9 and so about eight weeks old, went in on 31/10** after
these starts (`vehicle-history.md`), about an eighth of the tank. Stored
petrol loses the light ends a cold start lives on (*general*), but eight
weeks in a closed can diluted eightfold is a weak suspect
(*reasoned*). **The first start with it in, 2/11**, after about 36 hours
in the garage at 16 °C (album, 08:22): **`StartCrank` 0.80 s, `StartDip`
78 rpm, `StartClt` 18 °C**, the battery 12.5 V — the first dip on OMV,
and inside the good month's own: 74 and 118 rpm on its clean starts after
10–19 hours at 12–14 °C of coolant (`idle-log.md`, 4/10, *The starts
measured from the capture*). The longest stand and the coldest coolant
on OMV so far. **Felt clean** (*owner*): a slight dip heard, which he
takes as normal; nothing near a stall, which is what the bad starts did.
S7 stays closed.

### D3. S8 — "loses breath above 5000 rpm" — closed 4/10/2026
On the hard drive of 4/10 (`28`) b7 eased from 185 to 181 between 4,000 and
6,000 rpm rather than dropping, and the car pulled better at the top. Its
criterion — a held pull in 4th to 6,000 rpm with the display's `Power` — was
met only in part.

### D4. S9 — the rich lambda trim — closed 4/10/2026
032 at −16.4 / −13.3 % on the old MAF, −3.1 / +4.7 % on the new one and near
zero at every read since: the old MAF over-read (C2). The airbox, found cracked
ahead of the MAF and sealed on 12/10, is a possible cause of that over-reading,
not shown.

### D5. S10 — oil at the back of the head — closed 4/10/2026
The valve cover gasket: the hardened original, then a wrong part on 2/10
(C17), replaced on 4/10 by Elring `915.653`; dry since, hot and cold. Neither
the ventilation nor the gasket was the idle (A15). The re-tightening stays in
`plan.md`'s standing items. *(26/10: re-tightened again by the
owner in the week of 19/10, hundreds of km on the gasket by then; the item
left the standing items at his request.)*

### D6. S12 — a hesitation on tip-in and after a gearchange — closed 4/10/2026
Withdrawn by the owner after watching for it: in his judgement mechanical play
in the mounting or the driveline, and the hesitation itself no longer felt.
*Reopened 27/10 at the owner's request (`open.md` S12): felt all along,
and 014 counted on the road at such moments. Whether play or combustion
is open there.*

**Closed again 27/10/2026 evening, by the owner: the accelerator pedal
was sticking, and greasing it cured the jerk.** On the drive after it
(`test/fixtures/vcds/vcds-pedal-drive-2-014-003-055.csv`) the throttle
could be fed in smoothly for the first time with this car; the play of
the engine mounts is still felt but is ordinary (*owner*). The pedal
measurement is in `idle-log.md`, 27/10 evening. **What it does not
close:** 014 counting on the road at steady 1800–2200 rpm and 25 % load
went on after the greasing, with no tip-in — that is kept in `open.md`
S3, not here.

What `open.md` said while it was open, kept as it stood:

> **Widened by the owner, 27/10 evening: both — after a gearchange and
> on a tip-in after engine braking.** *Briefly this said "not the
> gearchange, only after engine braking"; he corrected it the same
> evening.*
>
> *Closed 4/10 by the owner as play in the mounting or the driveline
> (`refuted.md` D6); reopened 27/10 at his request.* **A jerk or hesitation
> as the throttle goes back on in the next gear**, felt for a long time
> (*owner*). **On 27/10 he watched 014 on the road and saw it count at
> exactly those moments**, and reads it as misfires rather than play. The
> log (`vcds/vcds-step6k-2-014-055-001.csv`, the drive before the A/C stop):
> **two episodes counted in steps of 12 while driving, 12 → 24 → 36 at
> about 2100 rpm and 12 → 24 → 48 at about 1900 rpm, both at 25–26 %
> load**, detection `aktivováno`; and **four shorter ones, 12 (once
> 12 → 24), at 1160–1920 rpm and 25–30 % load**, also `aktivováno`, one of
> them at 06:45 with the coolant at 55 °C (*re-read 27/10*). The gear is not in the log, so that
> they were tip-ins after a change is the owner's, not the log's. ⚠ The
> other changes in that field at gearchanges came with detection
> `deaktiv.` and read 13–18, not steps of 12: not misfires (one 13, at
> 07:03:44, came with detection still `aktivováno` and cleared 2 s later).
>
> **Not settled that it is combustion** (*reasoned*): misfire detection
> reads crank speed, and **play that lets the engine rock as the drive
> takes up again shakes the crank** — exactly what H12 says and what the
> owner first concluded. A misfire on tip-in after a lift is also
> plausible: the overrun fuel cut leaves the port walls dry, and the first
> firings after it run lean (*general*). **What tells them apart**: a
> capture (0x280's engine speed per 180°) across a few such tip-ins — a
> firing that fails shows as one short step, the rocking of a mount as a
> slow oscillation at the driveline's frequency; or the same tip-ins with
> the clutch slipped gently, which takes the driveline out.
>
> **A third, mechanical, measured 27/10 evening: the pedal stuck** exactly
> where a tip-in starts. Ignition on, engine off, the plate came off its
> 5.6° rest **in jumps of 1–4°** (5.6 → 8.7 → 10.0) through the band where
> the ECU switches from idle to part load (about 9.5°); **greased, it moved
> in 0.4–0.5° steps**, the sensor's own resolution, and felt smoother
> (*owner*; `idle-log.md`, 27/10 evening). A pedal that breaks free opens
> the plate in one lurch, which the foot cannot feather — a jerk with no
> misfire in it. **It does not explain 014 counting** at those moments, so
> it would be one cause beside the other two, not instead of them. **The
> next drives tell**: whether the jerk is gone or milder, and whether 014
> still counts at the tip-ins.

### D7. S13 — the throttle's routine at every ignition-on — closed 2/10/2026
20–30 s of the throttle seeking its stops at every ignition-on. The new
throttle body does the same after its own completed 098, so it is how these
parts behave (C16).

### D8. S15 — a constant sputter from the exhaust near the engine — closed 12/10/2026
Heard from 9/10, at every load. The cold tailpipe test of 12/10 found no leak,
and since S6's joint was shimmed the same day it has not been heard at all: in
the owner's reading it was that joint all along. *The entry used to say that
joint could not be the source; the owner's ear on the car outranks that.*

### D10. S18 — cylinder 3 dropped out, cold, with a tick at camshaft rate — closed 24/10/2026
**What happened, 18/10** (*owner*): on a short gentle drive cold the engine
ran on three cylinders for a while, with a tick that followed engine speed;
**P0300 and P0303** stored, the first cylinder the ECU ever named. The tick,
off the owner's video: once per 720°, camshaft rate, all four firing beneath
it (`photos/tick-2026-10-18-cold-spectrogram.png`). Cylinder 3 dropped out
again with the lamp flashing; after a restart all four ran. That afternoon,
warm, the tick came back for a few minutes and went by itself; **014 read
two bursts under part load, 270 and 351**, where sixteen earlier logs never
read above 72 driving. The cleaner's tank had just run out.

**Since**: **no tick, no three-cylinder running, no lamp** on any drive
from the evening of 18/10 through 24/10 (*owner*) — `39`, `40`, the first
44K tank driven hard with long stretches at 5000 rpm, full-throttle pulls
on most of them; fault memory empty after `39`, over 19/10 and on 23/10.
**And the hardest test the car can be given**, 24/10 (*owner*): about
340 km in the day, about an hour of it above 4000 rpm, much held at 5000,
with none of it — the misfires under load of the 18/10 afternoon
included.
**The look inside, 19–20/10**: on 3 alone a layer of deposit come away from
the exhaust valve and the crown (`idle-log.md`).

**Closed at the owner's decision**, on the run of clean drives that
`plan.md` Part 2 (*The S18 drives*) set as the reading: it faded, which
reads for **a flake of deposit under 3's exhaust seat** (`open.md` H13)
over a lifter or valve that hung (H1), and does not prove it. Not settled:
the cause. **Heard or seen again, above all cold → it reopens in
`open.md`**; item 5's drive rules in `plan.md` stay until the map goes back.
*(26/10: they left `plan.md` at the owner's request — he keeps them as a
habit until the map goes back, not as a step.)*

### D9. "A higher idle quiets the misfires" — measured, 12/10/2026
The specified idle raised from 780 to 830 rpm, the ECU's limit (VW's
procedure, login 01283): 014 kept counting and `IdleHealth` rose slightly with
engine speed. Put back the same day.
