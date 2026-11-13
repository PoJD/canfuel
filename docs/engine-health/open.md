# Engine health — what is still wrong, and how to find out why

**The working document for one open investigation into the engine itself.**
It holds only what is **unresolved**: the symptoms still present, the
hypotheses still standing, and the test that would confirm or kill each one.
It has an end date. When every symptom below is either fixed or shown to be
normal for this engine, the file is deleted.

| file | what is in it |
|---|---|
| **this one** | symptoms → hypotheses → tests. Short on purpose |
| `refuted.md` | every hypothesis **settled against** and every symptom closed, with what settled it. Read it before proposing something |
| `vcds.md` | the VCDS blocks read on this car, their specifications, and how to record them |
| `vehicle-history.md` | the service record: parts, dates, distances. **Stays when this investigation closes** |
| `idle-log.md` | **the diary of the idle investigation**: what was done and measured at each stage. **Stays** |
| `plan.md` | **the planned fixes, in order**. Emptied as the work is done |

**The full text this file was condensed from on 20/10/2026** — every
alignment, every table session by session, every argument and its
corrections — is in git: `git show d327332:docs/engine-health/open.md`.
The dated log before it: `git show 7c69883:docs/engine-health.md`.
Nothing in the tree depends on either.

**Rules for this file.** A hypothesis that is refuted, or a symptom that
closes, moves to `refuted.md` in the same commit and leaves this file. A
new measurement goes into the evidence of the symptom and of every
hypothesis it touches, not into a dated section. Owner reports are marked
*owner*; general engine knowledge *general*; an inference *reasoned*.
**Every new observation of the owner's is checked against the symptom
list, and the owner decides** whether it is a symptom. When the symptom
list changes, every fit table gains or loses the column in the same commit
and the ranked list is re-read.

⚠ **Nothing here changes a constant in `src/`.** `IdleHealth` and the start
bytes on 0x604 are one of the instruments (`docs/firmware/frames.md`).

---

## Where it stands — 13 November 2026

**Closed**, in `refuted.md` §D: S6 the exhaust joint behind the
converter, S8 the top end, S9 the rich trim, S10 the oil leak at the back
of the head, S13 the
throttle's routine, S15 the sputter, S18 cylinder 3 out with a tick
(24/10), **S7 the cold start (31/10: the fuel — four clean starts on
OMV after six bad of eight on the Verva)**, **S24 the coolant reading
(12/11, D12: oil round G62's pins, cleaned; the owner's decision, to
reopen if it comes back)**, **S23 the new rear probe's signal at zero,
P0137 (12/11, D13: the new probe's own fault — the old one refitted read
healthy on two drives with no P0137; the owner's decision)**; H9 (crankcase ventilation,
A15), H10 (when 014 counts, C19) and **H15 (the NGK plug ends, C24,
4/11)**.

**The timing belt's marks were read 13/11 morning, cold** (`plan.md`
8i, done; the row A1): **the camshaft sprocket's OT mark set against
its mark** (*owner*), a tooth of the sprocket painted white, most likely
at the belt change of 10/2017 (album 9:42); **the one narrow notch on
the crankshaft pulley's rim then stood 30–60° of crank from the groove
on the block, behind it** (*owner*, by eye and by the borescope with a
finger on the notch, album 10:12–10:39; first given as about 45°) —
1.5–3 teeth of the cam if both marks are the right ones (*reasoned*).
No other notch on the pulley; the two wide cut-outs at 4 and 9 o'clock
read as balancing cuts (*reasoned*). **The direction is the owner's,
read off the part** (*owner*, 13/11: the crank turns clockwise, and the
notch stands counter-clockwise of the groove, short of it): **the crank
lags the cam, so the cam is advanced and every valve opens and closes
early** (*reasoned*). *Until his word this said the direction might be
mirrored from below.* **Still open is the size**: 2–3 teeth sit badly
with the flat full-load pulls (A1), and the piston of cylinder 1, which
would have settled it, was not looked at (*the owner*: not taking a
plug out). **The air the engine takes at full throttle says the cam is
not 30–60° out** (13/11, *the owner's question*: b7 is only the ECU's
belief, so can the data show it at all): the ECU does not believe the
air, it measures it (the mass air flow, 003), and the car's acceleration
is nobody's belief. Over every 003 log, full throttle held 1.5 s or
more: **496 mg a stroke at 2,400 rpm, 520 at 3,600–4,400, 485 at 5,200,
452 at 5,600 — 85–90 g/s at the top**, the air of an 85 kW engine, and
the acceleration needs 145–152 Nm from 2,000 to 5,000 rpm in 3rd and
4th and 130–137 above (the row A1). A cam 30–60° early shuts the inlet
near bottom dead centre and opens the exhaust mid-stroke; the filling
above 4,000 rpm would collapse (*general*), and it is whole. **So the
notch or the groove is not the mark** (*reasoned*); a few degrees, up to
perhaps a tooth, the air cannot exclude with no healthy AQY to set it
against. **Kept first in list A all the same** (*the owner*, 13/11). **The owner's decision: the belt and the water
pump renewed at a garage** (`plan.md` 8q) — nine years on the belt,
nothing lost if it was right; the mechanic reads the old belt's marks
before it comes off.

**The original map has been in the ECU since 3/11** (`plan.md` 5a), the
adaptations reset with it; the drive home was captured (`42`) and read
the same day, and **the tuner's two files compared**: **the remap
changed five tables, only at high speed and the highest load** — less
fuel, more advance — and nothing at idle (H14). The drive agrees: the
idle advance, the overrun cut, the full-load advance, air and b7 read as
on the remap; **014 read zero**, which the files say is not the map's
(S3). **The second drive (`43`, 5b, 3/11 evening, to football)
was read in a cloud session the same day**: **cylinder 3** the weak
one, 13 % of a stroke under the mean with 62 % of the weak strokes
(`cylscan.py`, read 12/11; S1, *Every stroke named*), 014 counts
again, and the first full-throttle pulls ran short of air (H14).

**The hydrogen clean of 9/11 is done** (`plan.md` item 8; captured
`44`–`46`, read the same day in a cloud session; S1, *The clean of
9/11*). **Stop 3 before it** began as `42` and `43` did — `IdleHealth`
about 90 for five minutes, **cylinder 3 at −18 to −27 % of a stroke
with up to 12 weak strokes a minute, 014 at 1.03 % of combustions, the
most of any warm stop on record** — and settled after its cut to about
50, 3 at about −9 % with 0–1, 014 near zero. **Stop 7 after it** read
about 60 from its first minute to its last: **no rough start, 014 at
0.12–0.14 %, 3's weak strokes 4.2 per 1000 against stop 3's 12.9**,
**but not below stop 3's settled level, and 3's deficit kept, −8 %**
(`cylscan.py`, read 12/11; S1, *The clean of 9/11*). **With the provider's gas
flowing at idle the idle had no dips at all** (8,700 strokes, `IdleHealth` 14–29); S22's
tick, heard during the clean, was closed that evening as the clean's own
sound (`refuted.md` D11) and reopened 11/11 night. One stop each side.

**The probes read before the swap, 9/11 night** (`plan.md` 8c, standing,
shortened at the owner's decision; H11, *The reading before the swap*):
**at every idle the rear probe sinks towards lean over the minutes**,
below 0.2 V by the third, and is back near 0.6 V after 1,500 rpm; the
A/C did not lift it in the log, though the display calmed with it
(130–140 loads off, 90–100 with the A/C); both heaters inside their
specification, 032/055 unchanged, no code. **Read 10/11** (H11, *What
the rear probe can and cannot say*): **a lean mean behind the front
probe at idle, its size not read, from one of four causes** — the
front probe reading rich, hydrogen from unequal cylinders, **air drawn
in between the probes (H2, widened to that zone 10/11)**, or a lean
bias the rear loop does not trim at idle. **Both probes replaced
10/11** (*the owner's decision*; no analyser): **the old front probe's
tip coated in a cracked grey-beige layer, the rear's clean** (H11, *The
old probes seen*); the swap rules out the old probes, not the other
three, and the reading after decides by H11's five marks. S22's tick heard again at
that idle loads off, not with the A/C — added to D11 at the owner's
decision, not reopened.

**The reading after the swap, 10/11** (`plan.md` 8c, done; H11, *The
reading after the swap*), standing as on 9/11 night and then a drive of
about 29 minutes with 014 033 036: **the new rear probe held flat at
0.59–0.60 V through 18 minutes of idle** — loads off, the A/C, loads off
— where the old one had sunk within the first phase, **then switched
in one sample to the front's swing** (0.07–0.78 V) until the 1,500 rpm;
flat again at the last idle and for the first 1½ minutes of the warm
stop. **The idle did not change**: loads off 112–140 (9/11: 130–140),
the A/C 66–75 (90–100), the warm stop at the end 48–90, `Misfires` 3–7,
014 0.24 % of combustions there. 032 −7.8 / +7.0 → **−6.3 / +5.5 %**
over the drive; heaters, 055 and the fault memory fine. **Read**: the
old probes carried most of the lean mean, **but the idle was as rough
without it** — H11's mark 2 met, marks 3 and 4 failed at the first stop.
**The battery was disconnected after parking at work** (*the owner*), so
032 relearns from zero on the new probes: on the old ones it was back
at −6.3 % after one drive both times it was reset (H11, *The relearn
after the battery disconnect*).

**The relearn drive, 10/11 evening** (`plan.md` 8d, done; captured
`47`–`48`, read in a cloud session the same evening; H11, *The relearn
drive*): **032 from zero to −6.3 / +6.3 % within 37 minutes**, −3.9 /
+7.0 at the end — **the split back on new probes in one drive, so not
the old probes'** (mark 1 failed; S19). **The idle as before**: queue
stops 49–92, the warm stop at the end 52–84 a minute, 014 0.15–0.24 %;
**cylinder 3 has 73 % of the weak strokes again** (38 % the day after
the clean), its deficit −9 to −17 % (−8 to −14 % on `46`) — **the
clean's effect on 3's misfires lasted a day, and its deficit never
went** (`cylscan.py`, read 12/11; S1, *Every stroke named*). **New, S23** (*the owner's decision*): **the new
rear probe's signal fell under load from 16:57 and read 0.000 V at full
load from 17:29, P0137 sporadic** — the lead, the connector or the part,
not the gas; normal again at the basic settings after it (034, 046, 037
all OK). **The last four minutes of the warm stop, 17:38–17:42, read
36–45, the calmest warm idle captured outside the provider's gas** — at
a plain idle, before both the clear of P0137 and the basic settings (the
bus marks them from 17:41:44), so neither made it (H11, *The relearn
drive*). *Unexplained until 12/11*: **3's deficit fell there in one
step, −22 to −9 %, its weak strokes from 11 a minute to 1–3** (S1,
*Every stroke named*).

**The second research, 11/11** (*the owner's request*; *What the
forums say*, 11/11; S1, *The rough start of a warm stop*, *How the weak
strokes follow each other*; S23): **two things on top of each other** —
**cylinder 3 weak in the first 5–8 minutes of a warm stop after a hot
drive**, and **a settled floor of about 40–55 loads off**, which
neither the clean nor the gas touched (*read again 12/11, the third
research, below: the rough start is a swell of 3's deficit, and the
floor carries 3's deficit of about −9 %, not 4's*); **the probes are out of
the idle**. The weak strokes come in spells of seconds on one cylinder,
and the stroke after a weak one in the same cylinder is less often weak
— a mixture or dilution limit rather than a spark limit. **S23's
sinking fits the contact spray of 10/11 morning** (Bosch forbids it on a
probe's connector), its zero the broken terminal. **Re-ranked with the
owner**: H1 to second; H21 above H11; S1s added to the fit tables.

**The first drive on the canister, 11/11 night** (8k, `idle-log.md` 11/11 night,
done; VCDS 032 055 014 over 65 minutes, then 001 with 033 and 036 at
the last warm stop; MFD in, no capture): **P0137 stored before it**,
cleared by the owner, so 032 relearnt from zero — **−3.9 / +2.3 % at
the end, −3.1 / +2.3 after the long last stop**, against −6.3 / +6.3
and −3.9 / +7.0 on 10/11's relearn with the bypass: **the part-load
cell a third of what it was, the first sign of the canister** (S21,
H16); the idle cell bent towards zero by S23. **The warm stops on the
display** (the everyday state): after a hard motorway run, oil 102 °C,
about 80 → **100–119** → 70–89, `Misfires` 13–15 → 1–3; every load
with the A/C **35–50**, `Misfires` 4 → 0; near home, oil 97 °C, **90–110
→ 45–50, waves of 40–80, then 25–40 for minutes at 100 °C, the calmest
warm stop on record** (*owner*), 014 at zero through the four minutes
logged. **But S23 came back and stayed**, the rear probe at 0.000 V at
idle, and **a new code, P0118 (G62, sporadic)**, with the coolant on
the MFD higher than any capture and dropping fast (**S24**, new) — the
record stop is read with G62 in doubt. **S22's tick heard again at the
first warm stop, reopened** (*the owner's decision*).

**The drive on the old rear probe and the cleaned G62, 12/11 night**
(VCDS 032 036 001 over 52 minutes, then 014 001 036 at the stop;
`idle-log.md`): **no P0137 and no P0118** — the old rear probe 0.575 V
at a warm idle and at zero only on the overrun, so **the new probe was
S23's fault** (going back to the seller); G62 39–100.5 °C with no step,
**the oil in its socket was S24** (closed 12/11, `refuted.md` D12). **032 from zero to −5.5 / +2.3 %**:
**the part-load cell +2.3 on both drives on the canister**, the idle
cell back near its old −6 to −7 — 11/11's −3.1 was S23's. **The warm
stops**: 80–90 at 92–95 °C; after the motorway 70–90; near home 120
→ **35–50 within three minutes and for about thirteen more, mostly
about 40**, with G62 sound, **014 at 0.04 % of combustions** at a
load of 25–26.5 %, where it counts (S3) — **the longest calm warm stop
on record outside the provider's gas, and 014 a third of the 0.12–0.24 %
of 9–10/11's warm stops**; only `42` (3/11) read lower, at 30 % load on
fresh adaptations, a silence S3 does not read as calm; 11/11's stop
near home read no count in 4.2 minutes at 25–28.5 %, G62 then misreading
(S1, the warm stops' table; *re-read 12/11 at the owner's question*:
the session at the car called it the settling seen before, which holds
for the level alone). **New: P0300 and P0303
stored on the drive, no cut, the lamp not seen** (S3); the limiter
touched once. Cleared by the owner.

**The third research, 12/11** (*the owner's request*: the idle and what
014 counts, read again from the raw captures; `tools/cylscan.py`, kept;
S1, *Every stroke named*; S3, *What 014 counts, by cylinder*; *Naming
the cylinder*, *The count that does not slip*). **Three things in how
the bus was read were wrong, and they hid one cylinder.** The stroke
count slipped (cylinders named at a cut were two slots off minutes
later); **the crank wheel itself alternates by 0.217 % of engine speed**
— 1.7 rpm at idle, measured on the overrun with no fuel, cylinders 2 and
3 reading high — and **that alternation was "cylinder 4's steady
deficit"**; and a stroke's loss shows a quarter in the slot before its
own. With all three taken out: **cylinder 3 gives 10–20 % of a stroke
less than the mean in every warm idle on record (from 24/9), and cold,
with the A/C and on the provider's gas; cylinder 4 is level warm since
October; 2 and 1 are above.** **What 014 counts is cylinder 3**: of 1,135 rises
of 014 at a standing idle put to a cylinder, **65 % on 3 and 30 % on 4
up to 18/10, 80 % on 3 since the VW leads** (85 % without `46`), 1 and 2
together 5–6 % throughout. **Cold, 4 is weak with 3** (the weak strokes
3 > 4 > 1 > 2, the borescope's order of the deposit but for 1 and 2).
**And 3's state moves over minutes**: at an unloaded warm idle its
deficit grows from about −14 to −26 % with its misfires, **then falls in
one step to a floor of about −9 %** (*over 30–45 s, read 12/11
evening, below; the A/C masks it rather than ends it*) — after an injector cut, with the
A/C, or by itself (10/11's "four calm minutes" are that step, 17:38);
the idle's grade follows it (r −0.6 over 205 warm windows). **The small
steps of a few rpm are on all four** (3 a fifth more than 1 and 4, 2 the
least); the misfires are not. **Agreed with the owner the same day**:
list B before list A; H3, H4, H7 and 6m read for 3, not 4; no injector
cut at the captured stop. **The injector itself is unlikely** (*the
owner's argument*, the same day): 3 was the weak one on the old
injectors in August too, so an exchange of injectors 3 and 2, agreed
earlier, was withdrawn and H7's one injector put last in B
(*The idle's candidates, ranked*).

**The captured warm drive on the canister, 12/11** (`plan.md` item 6,
the first of its captures; `49`, read in a cloud session the same day;
S1, *The first captured stop on the canister*): 30 minutes with five
full-throttle pulls, then **a warm stop of 18 minutes with no cut**.
**It began with 3's swell** — `IdleHealth` 76–89, 3 to −23 %, 014 at
0.69 % with 37 of 40 rises on 3 — **then 3 stepped to its floor by
itself** (11:19:30) and the stop held **30–44 for fourteen minutes**,
014 one count. **Settled, as calm as `44` after its cut and `48`
before the canister, and no calmer**, the common part the same: **the
canister lowered neither part at this stop**; only the floor's length
was new. **The seat shudders felt at 35–40** (*owner*, ruled a shift
of S1) are that floor's small dips, **on all four cylinders**, not 3's
misfires. **032 went −14.8 / +2.3 → −7.0 / +8.6 %**: the part-load
cell back at the bypass's level (S19, S21, H16). **020: cylinder 4 to
12.7° at full load and 14.2° on a tip-in, now at 3,500–4,600 rpm as on
the remap, and 2 beside it near the limiter** — recorded in S4 as an
observation (*the owner*, 12/11). The fault memory empty throughout; the engine
lamp only at its check before the start. **H16 stays first in list A
until the new N80** (*the owner*, 12/11; Claude had proposed it down;
*third since 12/11 evening, below*):
his reading — a valve still leaking canister vapour, a gentle morning
drive leaving the canister loaded (−14.8), the brisk one drying it
(+8.6) — fits all four 032 readings on the canister (H16, *The owner's
reading, 12/11*).

**The two parts read again, 12/11 evening** (*the owner's questions*;
S1, *The swell's shape, and what the common part follows*). **3's wave
is a sawtooth**: its deficit grows 1.5–3 % a minute for 3–8 minutes to
−21 to −28 %, then falls to −1 to −8 % **over 30–45 s, not in a step**,
with nothing on the bus at the fall; every stroke of 3's is weaker in
it, not only the misfires; a load masks it without ending it; the
mixture and the injection time do not move. **So not 3's air or fuel,
not its spark, not a flake blown out**; *reasoned*, in the order they
fit: **a seat on 3 that fouls at idle and burns itself clean** (H1 with
H13), oil gathering at 3's inlet valve (H18, one valve), coolant (H20),
the ECU's purge phases (H16). **The common part is a constant**:
2.7–3.1 rpm rms at every warm idle since 24/9, within 5 %, through
every repair; it moves only with a load (a fifth less), the provider's
gas (two fifths less) and temperature (a fifth more cold), and not
with 3's wave — what H0 or a fixed fault on all four gives (the belt's
marks, 8i, read 13/11 and not settled — the full-throttle air against 30–60°, the row A1; the belt renewed, 8q), not a source that changes by the day (H16's leak, H7's
rail, H18, H11, H21). **Agreed with the owner the same evening, all
four**: the phone's recording through a swell beside a capture
(`plan.md` 6p; the tailpipe half done 12/11 evening at `50`'s
stop); N80's hose shut for two captured drives, after the new
valve's own two (8o); the warm leak-down made on an engine switched
off in a swell (item 9); and **list A re-ordered: the belt and H0 at
its head, H16 third** (*The idle's candidates, ranked*). The reading
is `tools/swellscan.py`, kept at his request.

**Off idle, 12/11 night** (*the owner's questions*; `tools/drivescan.py`,
kept; *Naming the cylinder*, *Off idle*). **The stroke count now holds
through a whole drive**, to the limiter: above about 2,800 rpm, where a
stroke is shorter than a frame, the crank wheel's alternation says
which stroke a frame shows — cylinder 2 on the same slot at all 124
named idles of sixteen captures. **Cylinder 3 is the idle's and the
light pedal's**: a fifth to a quarter of a stroke under 2 standing and
crawling, under 9 % as soon as the engine pulls, **1–3 % at full
load** — load helps, measured. **Cylinder 4 gives 2–4 % less than 1 at
every load from 1,600 rpm up** (S4). **At full throttle no stroke
misfires or half-fires** (100,000 strokes; the excess of weak over
strong is nothing, to about 0.3 % of the power) and 014 agrees — 59
rises above 1,200 rpm in 24 driving logs, one above 2,820; **what 3
and 4 cost there is about 1–2 %**. **The car's own acceleration needs
0.95 of the torque b7 claims** (76 pulls, half of them 0.89–1.04; the
registration's 1,303 kg, the resistances assumed), so the engine gives
its rated torque to within a tenth. **014's split by cylinder is set against chance since** (S3):
83 % on 3 against 50 % in control windows, not against 25 %. **Agreed
with the owner the same night: H4 above H20 in list B**, H1 read as a
seat that dilutes at vacuum rather than one that loses compression, and
**6m (injector 3's circuit) before item 9's garage session**; **his
reading added to H3** — a leak at runner 3 *and* a mixture the ECU
trims lean at idle for another reason, which takes 032's negative idle
cell out of the case against H3.

**Open:**

- **The idle — S1 (unsettled) and S3 (014 counts at idle).** Every part in
  the fuel and ignition path has been replaced and both remain. Warm, in
  the everyday state, **about 70 on 27/10, level with its best days of
  12–15/10, back up to 80–105 from 28/10 to 2/11** on the display, on the
  Verva and on OMV alike; **on the original map, 3/11 (`42`, fresh
  adaptations): 93 for the first three minutes of a stop straight after
  the motorway, then 54 ± 3, and 63–77 at the stops on the way home**;
  cold 98 ± 3 at 50–61 °C of oil, against 110–140 on the display the day
  before. **014 read zero all session**, at an idle load of about 30 %
  (S3). **On `43`, one drive later, loads off: 86 for the first 3
  minutes of the warm stop, 48 ± 3 for its last five** — the best level
  shown loads off, one stop; **014 counting again** at 26.5 % load, then
  zero for the last 2 minutes (S3). **On the display the same night**,
  the drive home: **70–95** at 101 °C of oil, everyday state (*owner*).
  **4/11, display**: **90–110** in queues until the engine was revved,
  the larger dips felt, **70–90** after; **45–50** with the A/C, the
  blower full and the rear window (*owner*). **5/11, display, the A/C
  on**: **60–76**, and the first warm `Misfires`, **2–10** (S3); **the
  drive home, 100 °C of oil, the A/C on**: **51–54**, `Misfires` 3–4 at
  the end, 1–22 over the hour (S3). **6/11, display**, the first reading
  after 5/11's contact cleaner and straightened gasket edge, at the end
  of a 40-minute drive with queues, oil 98 °C, **the A/C on, the blower
  on 2**: **65**, `Misfires` **18**, MisfAvg **23.0**, the
  misfire figures higher on only about 5 minutes of idle, hardly any of
  it warm; **the engine behaved the same** (*owner*; S3). **The drive
  home the same day**, oil 90 °C, **the A/C off, the blower on 1**:
  **73**, `Misfires` **6**, MisfAvg **8.6**, the idle "relatively OK" —
  and the engine lamp, P0440 (S21) (*owner*, the album). **8/11**, home
  after the OMV fill, oil 97 °C, the everyday state, about a minute:
  **70–75**, `Misfires` **9–12**, MisfAvg **12.5** since the start at the
  pump; most of the drive gentle on the last of the fuel, a little
  higher revs after the fill (*owner*). **9/11, the clean's day**
  (`44`–`46`, the everyday state, A/C off, oil 101–103 °C): **stop 3
  before it 90 then 50**, **stop 7 after it 57–63** (S1, *The clean of
  9/11*); felt **"a little calmer" after it**, which he says he no
  longer trusts himself (*owner*), and more unsettled at the provider
  straight after the clean (*owner*, 11:26). **10/11, after both
  probes** (H11, *The reading after the swap*): standing, loads off
  **112–140**, the A/C **66–75**; the warm stop after a drive of 29
  minutes, the everyday state, A/C off, oil 101–102 °C: **48–90**,
  `Misfires` 3–7 — no change. **10/11 evening** (`47`, the relearn
  drive, 032 relearning from zero): queue stops **49–92**, the warm
  stop at the end **52–84** a minute for 8 minutes, **then 36–45 for
  four**, before the clear and the tests (unexplained; H11, *The
  relearn drive*). **11/11 night, on the canister** (8k, above): the
  stop after the motorway 100–119 settling to 70–89; **near home 25–40
  for minutes**, oil and coolant 100 °C, the calmest on record — with
  G62 in doubt (S24, closed); **12/11 night, G62 sound, the old rear probe**:
  after the motorway 70–90, near home 120 → **35–50 within three
  minutes and about thirteen more, mostly about 40, 014 at 0.04 %** —
  **the longest calm warm stop on record outside the provider's gas**,
  the second calm night in a row, **both on the canister** (re-read
  12/11 at the owner's question; the session at the car had called it
  the settling of 10/11 evening, which held 36–45 for four minutes after
  eight at 52–84); **P0303 stored on the
  drive** (S3). **12/11, captured** (`49`, above): 76–89 for four
  minutes on 3's swell, then **30–44 for fourteen**, no cut, 014 one
  count — settled as `44` after its cut and `48`, no calmer.
  **By cylinder** (`tools/cylscan.py`, 12/11; S1, *Every stroke
  named*): **3 is the weak one at every warm idle since 24/9, 10–20 %
  of a stroke under the mean, with 35–77 % of the weak strokes** —
  on every set of plugs and leads, both MAFs and both maps, before and
  after the clean (`44` 58 %, `46` 38 %, `47` 73 %, `49` 54 %); 4 was weak with
  it on 24/9 and is level warm since October. **014's rises are 3's**,
  80 % since the VW leads (S3, *What 014 counts, by cylinder*); P0303
  after `43`'s cut and on 12/11 without one. *The dip shares this
  paragraph gave until 12/11 — "two thirds on 3 and 4", "all four
  alike on `40` and `41`", "`46` the first with no leader" — came from
  a count that slipped and left the crank wheel's alternation in;
  removed (Naming the cylinder).*
- **Around the idle:** S2 (an occasional puff), S14 (bangs on an
  unblipped downshift), S11 (a hiss at the back, perhaps the throttle's
  own air).
- **The cylinder 4 knock window: S4, S5** — its own cluster, not in
  `plan.md` (*owner's decision*, 9/10). **On the original map cylinder 4
  retarded alone on 3/11**, as often as on the remap and about half as
  far; **on 12/11 as far as on the remap (to 12.7° at full load), and
  above 5,300 rpm with 2 beside it** in 57 % of the samples — **2, the
  strongest cylinder at idle**; the heading changed with it (S4, *Since
  12/11*; no fit-table symbol moved).
- **S19, P0172 and the split trim** — the code once (24/10), not back on
  any reading since; **032's idle cell at −6.3 to −8.6 % and its
  part-load cell at +5.5 to +8.6 %** from 25/10 on the remap. **On the
  original map, one drive after the reset: −6.3 / +3.1 %, two:
  −6.3 / +3.9 %, settled on 6/11: −7.0 / +6.3 %** — neither cell is the
  map's (S19). **On the new probes, 10/11: −7.8 / +7.0 → −6.3 / +5.5 %
  in one drive, then reset by the battery disconnect; relearnt from
  zero on 10/11 evening to −6.3 / +6.3 within 37 minutes, −3.9 / +7.0
  at the end** — the split is not the old probes' (S19); reset again by
  the clear of P0137 (`plan.md` 8f). **On the canister, 11/11 night:
  −3.9 / +2.3 % in one drive, −3.1 / +2.3 after a long stop** — the
  part-load cell a third of the bypass's (S19, S21); **12/11 night,
  the old rear probe: −5.5 / +2.3** — the part-load cell held, the idle
  cell back near −6; **12/11, the captured drive: −14.8 / +2.3 before
  (one MFD drive after the clear), −7.0 / +8.6 after** — the part-load
  cell back at the bypass's level in one brisk drive (H16).
- **S21, P0440 and the engine lamp, steady** (6/11, added at the
  owner's request): the evaporative system, the code of 1/2018 back; no
  fill and no hose touched before it; cleared by the owner (H16). Not
  the idle. **The tank lets out a strong overpressure at the filler
  cap in summer** (*owner*, 11/11), and **that evening the canister
  was found bypassed** — the tank's line joined straight to N80's, by
  an earlier owner (8j), and plumbed back the same evening; **the first
  drive on it, 032's part-load cell +2.3 % where it read +6.3 to +7.0**
  (S21, *The first drive on the canister*).
- **S12, a sudden jerk at a crawl and on moving off** (reopened 10/11
  night at the owner's request; not the pedal): not on the bus at a
  crawl; 014 counted single misfires in moving-offs on 10/11.
- **S22, a tick once per engine cycle** (9/11, closed the same evening,
  **reopened 11/11 night** at the owner's decision): heard again warm
  with no clean, the same pattern quieter; **the recording read 12/11:
  the once-per-cycle rhythm at the size of every warm idle recording
  since 15/10, not 18/10's** — nothing new in it, which a lifter that
  bleeds down hot would have shown. H1's lifter, an injector, a port,
  or one cylinder's burn; the stethoscope, hot (`plan.md` 9).
- **S20, the speed wandering at a constant pedal** (since 1–2/10, on the
  road) — **a little better since the cable was slackened and the pedal
  greased (27/10), still there** (*owner*, 28/10). Not the idle.
- **Not pursued:** S16 (a tick on the gearbox side), S17 (a resonance at
  ~2200 rpm; **not the exhaust's heat shields** — still there after their
  new clips, 31/10 — perhaps nearer the engine).

**Ranked in two lists since 12/11** (*the owner's decision*; *The
idle's candidates, ranked*): the idle split into **the common part**,
about two thirds of `IdleHealth`, and **one cylinder's part**, the
steady pattern over the cylinders and the rough start after a hot
drive, about a third. **A, common** (*re-ordered 12/11 evening, agreed
with the owner*: the common part is a constant, S1, *The swell's shape,
and what the common part follows*): **the timing belt a tooth out**
(its marks read 13/11, 8i: the crank's notch 30–60° from its groove by
eye, which the air the engine takes at full throttle speaks against,
the row A1; the belt renewed at a garage, 8q, *the owner's
decision*), **H0**,
**H16** (the purge path, the valve and the canister; first until that
evening; the new N80 still to fit, 8a — the common part by capture
before and after it), H8, **H7's rail pressure**, **H21**, **H11**, H2
(the zone between the probes), H18. **B, one
cylinder**, cylinder 3's, **first since 12/11** (the third research,
*agreed with the owner*): **H13 and H1** (3's deposit, its exhaust seat
or a flake, its lifter), **H3** (runner 3's lower gasket), **H4**
(the injector loom at 3; *above H20 since 12/11 night, agreed with the
owner*: 3's deficit is an amount at a small charge, not a share, which
an injector opening late gives), **H20** (coolant into 3), **H7's one
injector** last (3 was weak on the old injectors too). H12 done. **Which part 11/11's and 12/11's calm stops lowered:
neither, by the captured stop of 12/11** (`49`) — 3's swell as before,
the settled floor no lower than before the canister; **H16 down list
A proposed 12/11 and declined by the owner** until the new N80, **then
agreed that evening on the common part's own reading, third** (H16,
*The owner's reading, 12/11*).
*Before the split, 11/11–12/11*: H13 and H1, H16, H3, H4, H7, the belt,
H21, H11, H2, H0, H8, H20, H18, H12 (every
fit table re-read 4/11). **H15 refuted 4/11** (`refuted.md` C24).
**H14 and H19 left it on 3/11**: the tuner's files
show the remap touched only the corner of highest load, and neither the
idle nor the MAF's curve (`refuted.md` C22, C23). **After `43`
(cylinder 3 named) deposits and a valve on 3 lead, H7 fourth.** **Read
4/11 on the load and revving patterns alone**: H13 with H1's exhaust seat
on 3 the one reading that fits both; H3 the load only; the order stands.
**Re-read 5/11 on the dips' anatomy** (S1, *How many strokes make a
dip*): one dip in five is two firings in a row, warm on `43` those lean
to 3 as well; the order stands. **The fresh look at the data, 5/11** (S1,
S3): 014 counts misfires per 200 revolutions and partly silences itself
under load; a steady pattern over the cylinders, 3 and 4 weak and 2
strong (*3 alone, read 12/11*), is about a third of `IdleHealth` (S1, *A steady pattern over the cylinders*); re-ranked
on it with the owner: **H3 second, H1 third, H4 fifth**. **Re-read
10/11 midday, after the reading after the swap: the order kept until
the owner decides after the relearn drive (8d); proposed, H11 from third to seventh** (its idle form
has lost its link — the lean mean went with the old probes, the
roughness stayed; *The idle's candidates, ranked*). **Re-read 10/11
evening, after the relearn drive, agreed with the owner**: H11 from
third to seventh, its marks 1, 3, 4 and 5 failed; **H21 added eighth**,
the probes' wiring; H13's "the clean took 3's excess" weakened, 3
leading again a day later (*The idle's candidates, ranked*). **Re-read
11/11 night, after 8k, S22 reopened and S24 added: the order kept** —
S22's ✔ goes to H1, already first with H13; H16's part-load reading is
one drive; S24 sits outside the tables. **Re-read 12/11 night: the
order kept** — P0303 without a cut names 3 again, where H13 and H1
already sit; H16's part-load cell held on a second drive. **12/11, H16
from sixth to third** (*the owner's decision*): the two calm nights on
the canister; H3, H4, H7 one down.
**Re-read 12/11, the third research, agreed with the owner** — the
misfires and the steady deficit are cylinder 3's, so **list B before
list A: H13 and H1 on 3, H3's runner 3, H20, H4, H7's injector 3**;
"4's deficit" gone from H3, H4 and H7; list A as it was, H16 first until
the captured stop on the canister is read by cylinder (*The idle's
candidates, ranked*). **Read 12/11** (`49`, above): **H16 from first of
list A to fifth proposed; the owner kept it first until the new
N80**. **Re-read 12/11 evening, agreed with the owner** (the swell's
shape and the common part): **list A: the belt, H0, H16, then as
before**; list B as it was, the swell read first as a seat on 3 that
fouls and burns clean (H1 with H13). **Read 12/11 night, the queue
drive (`50`, 6q): the order kept** — nothing the ECU measures or
commands moved with 3's swell or with the common part (S1, *The queue
drive, and what the ECU sees through a swell*), which leaves both
lists where the bus alone had put them; no change proposed.
**Re-read 12/11 night, off idle, agreed with the owner**: **H4 above
H20** — list B is H13 and H1, H3, H4, H20, H7's injector (*The idle's
candidates, ranked*).

**Read 12/11 night, 6p's
recordings at the tailpipe: the order kept** — 3's exhaust pulse grows
with its deficit and drops with the fall, on every stroke; it puts the
swell in 3's combustion and does not choose between a seat and a
dilution (S1, *The phone at the tailpipe through a swell and a fall*).

**Next** (`plan.md`; *the owner*, 10/11–13/11): **until the new N80
(in hand since 13/11, to be fitted about the weekend of 14–15/11) no further
captured drive** (*the owner*, 13/11): the old valve's baseline for H16,
*The owner's reading, 12/11*, is what `49`, `50` and the drives before
them hold (H16 third in A since 12/11 evening; the baseline stands); **6p's second half, the phone above cylinder 3**, at the next
captured stop that swells (the tailpipe half done at `50`'s stop);
**6i's oil level
next about 156,400 km** (read 11/11 evening: another 0.5–1 mm lower,
H18); **8q, the timing
belt and water pump renewed at a garage** (*the owner's decision*, 13/11,
after 8i), the old belt's marks read by the mechanic before it comes
off, with a captured drive between it and the new N80 (the garage chosen, a
date asked for 13/11, none yet); **the new rear probe sent back to the
seller under warranty 13/11, its replacement fitted when it comes, the
old rear probe on the car meanwhile** (S23 closed 12/11 as its fault,
`refuted.md` D13); **then 8a, the new N80**: 032/055 and the fault
memory before, 070 after, then one gentle and one brisk drive captured
with 032 after each (H16, S19, S21); **then 8o, two captured drives
with N80's hose shut**; **8h, the loads against the
sensors' voltages**, at a laptop session; **8f, 032 at every VCDS
session**; **6m's injector circuits**, read for 3, **at the owner's
next evening with the upper intake off, ahead of the garage session**
(*agreed 12/11 night*), and item 9's tests
(the coolant's CO₂ test, the stethoscope, then one garage session with
the upper intake off: a warm leak-down with 3 twice, the engine
switched off in a swell, a warm
compression, VW's tappet check, 6m, the gasket) by what those show;
**8e's harness at the end**, 8g and 8b dropped (*the owner*, 11/11).

---

## The symptoms

### S1. Unsettled idle — engine speed fluctuates

**What is seen.** Every few seconds the idle dips by 20–45 rpm and recovers in
about a quarter of a second. It feels restless from the driver's seat too:
**the larger dips, about 15 rpm and over by the owner's guess, are felt as a
slight jerk in the seat** and heard, and between jerks `IdleHealth` holds
lower (*owner*, 23/10/2026: about 50 between, higher with each).
**On the new regulator hose, 25/10, no jerk was felt** with `IdleHealth`
about 90 loads off and 120–130 straight after a start and after the loads
went off (*owner*) — so a high grade did not come from felt jerks that
time.
**12/11, at the captured warm stop** (*owner*; **a shift of S1, not the
engine mounts**, his ruling the same day): **frequent small shudders in
the seat at `IdleHealth` 35–40**, one minute holding 38 dips of 10 rpm
and more, 8 of 15 and 1 of 20 — felt below the "about 15 rpm" of 23/10.
**On the bus** (`49`, the stop's settled fourteen minutes): 28–50 dips
of 10 rpm and more a minute, 3–14 of 15, 0–4 of 20, **spread over all
four cylinders** — of 10 rpm and more 1 34 %, 3 25 %, 4 20 %, 2 20 %;
of 15 and more 1 35 %, 3 29 %, 2 22 %, 4 14 % — with 014 silent: **the
common part's steps, not 3's misfires** (*The first captured stop on
the canister*). One idle, oil about 80 °C; whether the grade's make-up changed
(more small steps, fewer deep dips) needs a capture.
**By ear, 25/10 evening** (*owner*, warm, the everyday state): **in the
calmer stretches the engine speed drops a little and holds there**. Not
shown by VCDS, whose 40 rpm steps put the stretches with 014 counting and
without at the same 760–800 (`idle-log.md`); a capture's quarter-rpm
0x280 would show it. It sits beside *What comes before a dip*: a dip
follows the idle overshooting a little.
**By feel, 25/10** (*owner*): the idle felt calmer all day, on the new
regulator hose and the second 44K tank; he says so himself before the
data. 6j's 014 agrees in kind: its episodes stayed at 12 (below).

**How it is measured.** `IdleHealth` on 0x604 grades one firing against the
next (100 = the engine before the repair, lower is smoother). Offline,
`tools/idledips.py --roughness` gives the same grade from a capture.
**Every idle figure in these files is on the `IdleHealth` scale**
(*owner's decision*, 12/10): the mean step in rpm × 50. A capture's figure
is a mean over a window, the display's a running filter of the same
quantity. **A reading without the oil temperature beside it compares with
nothing**. **Fresh adaptations** (after a battery disconnect) were held
to read calmer on every ruler; **014 does not** — it counted on 27/10's
reset as on settled drives, and only 4/10 A was quiet (`refuted.md` C19,
2/11) — and `IdleHealth` on fresh ones (3/10 61–68, 4/10 A 72–74, 27/10
about 50) sits inside the settled range, so it is not shown either way.

**What one dip is worth.** Engine speed on 0x280 is recomputed once per 180°
of crank, one power stroke (`docs/firmware/can-decoding.md` trap 5), so a dip
is one cylinder's stroke. A stroke that gives nothing costs an estimated
33–57 rpm; the deepest dips are 37–46, the typical one 20–22 — a partial
burn. **The dip is the failed combustion itself**, and the recovery is the
idle governor. **About three dips in four are one weak stroke, one in five
two in a row** (*How many strokes make a dip*, below).

**Every session since the repairs, like with like** (standing idle, 30 s
windows, 93–111 °C of oil, heavy-load windows left out; mean ± standard
error):

| date | capture | adaptations | what changed | `IdleHealth` |
|---|---|---|---|---|
| 24/9 | `19`/`20` | fresh | new injectors, old MAF | 113 ± 5 |
| 24/9 | `24` | fresh | **new MAF** | 91 ± 6 |
| 3/10 | `26` | fresh | the valve cover job | 61–68 (few windows) |
| 4/10 A | `28` | fresh | the right cover gasket | 72–74 |
| 4/10 B | `29` | settled | | 89 |
| 9/10 | `30` | settled | dipstick, MAF clamp | 83–89 |
| 10/10 | `31` | settled | **new NGK leads and plugs** | 77 ± 4 |
| 12/10 | `32` | settled | lead 4 re-seated, airbox sealed | **63 ± 1** |
| 15/10 | `37`, `38` | settled | the cleaner in | **59–61** |
| 18/10 eve | `39` | settled | after the episodes of 18/10 (`refuted.md` D10) | 78 ± 4 |
| 19/10 | display | settled | | about 100 loads off |
| 21/10 | `40` | settled | **VW plugs and leads, new plenum gasket** | 67 ± 2 |
| 23/10 | display | settled | the first 44K tank, ~70 km in, after a hard motorway run | 45–50 between jerks, 70–90 with them, **never above 100** warm; *fan on 1, one seat heater on 1, lights* (*owner*) |
| 23/10 eve | display | settled | home through Prague traffic, much idling, unsettled throughout; the last stretch held at higher revs in a low gear | **37** straight after, the lowest yet in this state, then slowly back to 50 within about a minute and above it after another; *fan on 1, one seat heater on 1, lights* (*owner*) |
| 24/10 eve | display | settled | the second 44K tank, Orlen Verva 100, after ~340 km in the day with about an hour above 4000 rpm; 3–5 min of warm idle | **70–80**, everyday state (*owner*) |
| 25/10 | display | settled, 032 relearning | **the regulator's vacuum hose renewed**; oil about 80 °C, not 93+ | **about 90** loads off, **35–40** loads on (lowest 35); **no jerk felt** (*owner*) |
| 25/10 eve | display | settled | the new hose, a drive later; oil 96 °C | **70–80**, everyday state; **50–60** at a light before, same state (*owner*) |
| 26/10 | display | settled | warmed in a jam, gently, under 3000 rpm; then one brisker stretch, revs held up in 2nd downhill on engine braking | **80–100** all through the warm-up, **still at 92 °C** of oil; **60–70** after the brisker stretch; everyday state (*owner*) |
| 27/10 | display, video | settled | `plan.md` 6k: a gentle drive to about 88 °C of oil, the A/C against the loads (`idle-log.md`) | **~70** everyday state; **35–50** the A/C alone; **54–62** every load but the A/C; **25–35** both |
| 27/10 eve | display, video | settled (055 reset that afternoon, relearnt to −1.17) | the pedal greased; oil changed 26/10; the second 44K tank about four-fifths used; oil 100 °C | **54** loads off (mean; **35–65** in waves of about 1½ min); **34** every load on with the A/C (26–42, still falling) — **the first stop with loads off within 25 of loads on** (condition 2 below), one stop |
| 28/10 | display | settled | the last of the Verva tank, 13 l in the morning to 5 l; oil 95–100 °C | **70–100 most of the time, down to 47 at moments**, everyday state; **felt worse** (*owner*), and the figures agree: above 27/10's ~70 in the same state, lower being calmer |
| 29/10 | display | settled | home from the pump, 5 km driven gently, oil 87 °C; the Verva still in the lines | **90–130, very unsettled**, everyday state (*owner*) |
| 30/10 | display | settled | the first warm drive on OMV; oil 99 °C | **80–100**, everyday state (*owner*) |
| 2/11 | display | settled | OMV, about 85 km in, the can's 5–6 l added 31/10; the day before the map; oil about 100 °C | **85–105**, everyday state; **felt worse again** (*owner*); cold **110–140** |
| 3/11 | `42` | fresh (reset with the map) | **the original map**; the drive home from the tuner, motorway to 186 km/h, then a stop of about 9 min with throttle blips, oil 103–105 °C; b7 25–29 at idle | **71 ± 3** over every warm window (41–100): **93 ± 2** for the first 3 min after the motorway, **54 ± 3** from the fifth minute (41–67), 63 ± 3 and 77 ± 4 at the two stops near home; cold **98 ± 3** at 50–61 °C of oil |
| 3/11 eve | `43` | one drive after the reset (032 −6.3 / +3.9) | the original map, the second drive: mostly motorway to 90 °C of oil, full-throttle pulls, then a warm stop of 11 min **loads off** (b7 21) with a 57 s cut on injector 4, oil 99–100 °C | **86 ± 4** the first 3 min; 74 the 2 min after the cut; **48 ± 3** from then to engine off (5 min, windows 30–67) — `42`'s shape, settling about the sixth minute; cold 129 over only 26 s settled, oil about 47 °C |
| 3/11 night | display | relearning (032 cleared after `43`'s cut) | the original map, the drive home from football, MFD in | **70–95**, oil 101 °C, everyday state (*owner*) — the first display reading on the original map, a little under the remap's 80–105 of 28/10–2/11 |
| 4/11 | display | relearning | the original map; mostly slow driving and queues, then the engine revved; oil about 100 °C | **90–110** until the engine was revved, **the larger dips felt in the seat**; **70–90** after it; everyday state. **45–50** with the A/C and the blower on full and the rear window heated (no main beam, no seat heaters), still falling; the supply down to about 12.4 V at times with everything on (*owner*) |
| 5/11 | display, photos and a video | relearning | the original map; stops on two short morning drives, the engine perhaps never fully warm and never revved above 3500 rpm, which always leaves it a little worse (*owner*); **the A/C on at every stop** (*owner*); oil not read | **60–76** with the A/C; `Misfires` **2** at 7:33, **5–10** at 9:05; MisfAvg 7.4 and 9.8–11.6 (the start's mean, its cold part in it) — the first warm readings of `Misfires`; cold the night before 18–23 (*owner*, the album) |
| 5/11 eve | display, a video | relearning | the drive home, an hour, mostly queues, revved a little at times; the everyday state plus **the A/C and the blower on 2** throughout; oil 100 °C at the end (*owner*) | **51–54** settling from 60–67 in the last 45 s, still the A/C on; `Misfires` **3–4** there, **1–22** over the drive (*owner*); MisfAvg 8.7 → 8.2 |
| 6/11 | display, a photo | relearning | the first reading after 5/11's contact cleaner (injector 4, T3) and runner 3's gasket edge straightened; about 40 min with a few queues; the everyday state plus **the A/C and the blower on 2**; oil 98 °C (*owner*) | **65** with the A/C; `Misfires` **18**, MisfAvg **23.0** at the end, higher because **only about 5 min of idle in the drive, hardly any warm**; **the engine behaved the same** (*owner*, the album 9:29) |
| 6/11 eve | display, a photo | relearning | the drive home; oil 90 °C; **the A/C off, the blower on 1** (*owner*); **the engine lamp came on** on the way, P0440 (S21) | **73**; `Misfires` **6**, MisfAvg **8.6**; the idle "relatively OK" (*owner*, the album 16:40) |
| 8/11 | display | relearning | home after the OMV fill (about 10 % Efecta 95 in the tank), mostly gentle on the last of the fuel, a little higher revs after the fill; oil 97 °C; the everyday state, about a minute (*owner*) | **70–75**; `Misfires` **9–12**, MisfAvg **12.5** since the start at the pump (*owner*) |
| 9/11 | `44` | relearning (032 −7.8 / +6.3) | stop 3 **before the hydrogen clean**, after about 50 min of driving with a motorway stretch; the everyday state, the A/C off; 30 s cut on 4; oil 103 °C | **90** the 5 min up to the cut (76–107), **50** the 5 min after it (37–64); 014 1.03 % then 0.02 % of combustions (S1, *The clean of 9/11*) |
| 9/11 | `44`, `45` | relearning | **the provider's gas flowing at idle**: 10:19–10:22 with the A/C and the blower on 4, and the clean's last 2 min with the blower on 4 and the heater full; oil 97–106 °C | **20** and **14–29**, **no dip at all** in 8,700 strokes (S1, *The clean of 9/11*) |
| 9/11 | `46` | relearning | **straight after the clean**, the hose off with the engine running, oil 104 °C; then stop 7 after a motorway run, the everyday state, the A/C off, a 30 s cut on 4, oil 101 °C | **60** straight after; **57** the 3½ min up to stop 7's cut, **63** the 6 min after it; 014 0.12–0.14 %; at work after the short drive on, 93 → 54–79 over 4 min |
| 10/11 | display, VCDS | kept (032 −7.8 / +7.0) | **the first idle on both new probes** (H11, *The reading after the swap*): a cold start standing, then loads off, the A/C, loads off, 1,500 rpm, idle; coolant 78–99 °C, oil 54 °C at the start of loads off | **120–140, then 112–120** loads off; **70, then 66–75** with the A/C; 98–120 loads off; 70–99 after 1,500 rpm; `Misfires` 13–14, 3–4, 8–12, 7 → 5 (*owner*) — as on 9/11 night with the old probes (130–140, 90–100) |
| 10/11 | display, VCDS 014 | 032 −6.3 / +5.5 after it | the drive on to work, about 29 min; a warm stop at the end, the everyday state, the A/C off, oil 101–102 °C | **60–70, 55, 70, 50–55, 48, then 80–90**; `Misfires` 7, 5, 3 (*owner*); 014 0.24 % of combustions |
| 10/11 eve | `47`, VCDS 014 032 036 | **relearning from zero** (the battery off; −6.3 / +6.3 by 16:58, −3.9 / +7.0 at the end) | `plan.md` 8d, the drive home from work; queue stops 16:51–17:17 in the everyday state, oil 99–103 °C; one with the A/C | **63, 91, 82, 92, 63, 49, 55, 71** loads off; **52** with the A/C; 014 0.24 % over the stops; cold at 44–46 °C of oil with 032 at zero 91–104 (H11, *The relearn drive*) |
| 10/11 eve | `47`, `48` | −3.9 / +7.0 (reset by the clear of P0137, 17:40:05–17:41:44, after the calm began) | the warm stop after a brisk stretch, the everyday state **plus the hazard lights from arrival** (*owner*), the A/C off, **no cut**, oil 102–104 °C; **the rear probe reading zero** (S23) | **59, 57, 52, 54, 65, 66, 84, 70** a minute for 8 min (014 0.15 %); **then 45, 43, 38, 39, 36 — the calmest warm idle captured outside the provider's gas** (the display touched 37 once, 23/10 evening), 3's deficit stepped from −22 to −9 % (`cylscan.py`, 12/11), to the revs for 034 at 17:42:50; 40–66 in the basic settings after (H11, *The relearn drive*) |
| 11/11 night | display, VCDS 014 at the stops | **relearning from zero** (−3.9 / +2.3, then −3.1 / +2.3) | 8k, **the first drive on the canister**; the rear probe at zero (S23), G62 misreading (S24, closed); after a hard motorway run, oil 102 °C, then near home, oil 97 °C | after the motorway **100–119 → 70–89**, `Misfires` 13–15 → 1–3; near home **90–110 → 45–50, waves of 40–80, then 25–40 for minutes**; **014: no count in 4.2 min logged** (22:39–22:43) (*owner*; 8k) |
| 12/11 night | display, VCDS 014 at the last stop | **relearning from zero** (−5.5 / +2.3 at the end) | 8n, the second drive on the canister; **the old rear probe sound, G62 cleaned**; 52 min with a motorway stretch and the limiter touched; the stop near home 01:46–02:02, coolant 94.5–99 °C | **120 (01:46) → 80–90 → 60–70 → 30–60 by 01:48**, then **35–50 for about 13 minutes, mostly about 40** (lowest 34 at 02:02, highest 58), `Misfires` 9–10 → 2–6 → **3**; **014: five counts of one misfire in 7.7 min logged (01:52–02:00), 0.04 % of combustions** (*owner*, times as sent; 8n) |
| 12/11 | `49`, VCDS 014 020 033, then 014 032 036 | 032 −14.8 / +2.3 before (one MFD drive after the clear of the night), **−7.0 / +8.6 after** | `plan.md` item 6, **the first captured warm drive on the canister**: 30 min with five full-throttle pulls, then a warm stop of 18 min, the everyday state but **the seat heater off until about 11:31**, the A/C off, **no cut**, oil 102 °C | **77, 89, 84, 76** a minute for the first four minutes (014 0.69 %), then from 11:20 **47, 52, 40, 35, 40, 44, 36, 34, 39, 33, 30, 37, 39, 37, 37** (014 one count in 13 min) — 3's swell and its step with no cut (*The first captured stop on the canister*) |
| 12/11 eve | `50`, VCDS one group at a time (003, 001, 014; 004 beside) | 032 −7.0 / +8.6 before, **−4.7 / +6.3 after** | `plan.md` 6q, **the queue drive**: 19 km in 67 min from coolant 39 °C, gentle (3 s above 4,000 rpm in its first 39 min, then 30 s in 17:01–17:07, to 6,440 rpm), 23 warm standing idles of 10–58 s, then a stop of 14.8 min slightly uphill, the everyday state, the A/C off, **no cut**, oil 100–101 °C | **72** over the queue's standing idles; the last stop a minute at a time **69, 64, 86, 82, 48, 60, 66, 74, 83, 63, 36, 47, 71, 71, 82** — three swells of 3's and two falls with no cut (*The queue drive, and what the ECU sees through a swell*); 014 19 rises in the stop's last 84 s, 16 on 3 |
**The dips themselves on the original map** (3/11, `42` against `24`–`40`;
standing idles settled 30 s and more, oil 93 °C and over, dips against the
one-second median): **about 17–20 a minute of 15 rpm and over**, as `32`,
`37`, `40` (16) and above `38`'s loads-off 9; **of 30 and over 0–0.4 a
minute**, as `32`–`40` (0.2–0.7); **none of 40 and over in 11 minutes**,
where `40` had one in 20 and `37` one in 7 — too few to tell apart; the
deepest 37.8 against 41–59 on `37`–`40`; the median dip 17.2 rpm as
everywhere. **One thing reads differently**: the spread of engine speed
inside a stop, **8.5 rpm** standard deviation against 9.8–13.9 on `24`–`40`
(only `38`'s single stops as low) — less slow wander, not fewer
stumbles; one drive. The idle speed (794–796 rpm) and 0x280's load byte
(21) as before. Cold (oil 40–70 °C, loads on): 22 dips a minute, 0.7 of
30 and over, against `32`'s 38–40 and 1.6–2.1.

**The clean of 9/11** (`plan.md` item 8, done; `44`–`46` and their
014/001/003 logs; read 9/11 in a cloud session; `idledips --roughness
--windows 30` and *ad-hoc scripts, not kept*, for the steady pattern
and 014 per stop; **the cylinders re-read 12/11 with `tools/cylscan.py`**,
which replaced the dip shares and names of 9/11 — *Naming the cylinder*).
Both stops in the everyday state with the A/C off, oil 101–103 °C,
each after a motorway run, each with a 30 s cut on 4:

| | stop 3, before (`44`) | stop 7, after (`46`) |
|---|---|---|
| `IdleHealth`, up to the cut | **90** (76–107, 5 min) | **57** (48–65, 3½ min) |
| `IdleHealth`, after the cut | **50** (37–64, 5 min) | **63** (57–76, 6 min) |
| the same with the steady pattern taken out | 45, then 33 | 40, then 41 |
| cylinder 3, % of a stroke against the mean | **−21** (−18 to −27 a minute), then **−9** | **−8, then −9** (−7 to −11 a minute) |
| cylinders 1 / 4 / 2 | +4 / +4 / +13, then +4 / −1 / +6 | +1 / −3 / +9, then +3 / −4 / +10 |
| weak strokes per 1000, 1 / 3 / 4 / 2 | 2 / **25** / 2 / 0, then 2 / 0.5 / 4 / 0.5 | 1 / 5 / 5 / 0, then 3 / 4 / 8 / 1 |
| dips per 1000 strokes | 4.8, then 2.7 | 2.6, 2.6 |
| 014, % of combustions | **1.03** (to 132 in one window), then 0.02 | 0.12, then 0.14 (to 36) |

- **Stop 3 began as `42` and `43` began**: rough for about five
  minutes, then calm. **The rough part is cylinder 3's swell**: its
  deficit −18 to −27 % a minute with up to 12 weak strokes a minute,
  51 of the 60 weak strokes before the cut, and 014 counting up to
  eleven misfires in a window of 200 revolutions — **the highest stop
  on record** (S3); after the cut 3 at −8 to −10 % with 0–1 a minute.
  **`43` the same**: 3 at −14 to −18 % up to its cut, −7 to −10 % after,
  back to −14 % by the tenth minute (S1, *Every stroke named*).
- **Stop 7 had no rough start**: about 60 from the first window, **3
  at −7 to −9 % in every minute — its floor, with no swell** — and 3's
  weak strokes 5 and 4 per 1000 against stop 3's 25; **4 had more than
  3** (25 against 16 over the stop), and 014's rises at stop 7 fell on
  4 (16 of 25), the one capture where they did (S3); 014 low.
- **But stop 7 was not calmer than stop 3's settled half**: 57–63
  against 50, the rest after the pattern 40 against 33, the dips 2.6
  against 2.7 a thousand, **and 3's deficit the same, −8 to −9 % against
  −9 %**: the clean took the swell, not the floor. *These bullets and
  the table said "3 within 0–3.6 % of the others", "the dips on all four
  alike, 3's share from 48 % to 23 %" and "4's steady deficit (5–8 %)"
  until 12/11*: a slipping count with the crank wheel's alternation in
  (*Naming the cylinder*).
- **Around it, the same capture**: **straight after the clean**, the
  hose off with the engine running, oil 104 °C: about 60, and **3 at
  −12 to −13 % for all five minutes**; 014 counted (*owner*: more
  unsettled there, 11:26). **At work**, after a short drive on from
  stop 7: 93 → 54–79 over four minutes, **3 at −11 % in the first
  minute (4 −9 % with it, for that minute alone) and −15 to −18 % by
  the third and fourth** — a swell on 3 again. *This said the rough
  first minute was 4's, 10–12 %, "not 3", until 12/11.*
- **The day after** (10/11 evening, `47`; H11, *The four calm minutes
  read closely*): **the dips back at 5.6 per 1000 strokes at the queue
  stops and 7.8 at the warm stop**, against 1.7–3.8 at every warm stop
  of 9/11 after the clean, **3 with 73 % of the weak strokes and its
  swell back** (−26 % in the warm stop's seventh minute). The provider
  said the clean's effect shows over a few hundred km (*owner*, 10/11);
  one day read the other way.
- **With the provider's gas flowing at idle the idle had no dips at
  all.** Twice: 10:19–10:22, the hose fitted with the engine running,
  the A/C and the blower on 4 — **`IdleHealth` about 20, 0 dips in
  4,877 strokes against 0.9 a thousand in the same state before it**
  (4.4 expected, p 0.01); and the clean's last two minutes at idle, the
  blower on 4 and the heater full — **14–29, 0 dips in 3,815**. The
  lowest grades on record. With it the throttle closed (3.0° → 1.3–2.2°),
  the MAF fell (3.1 → 2.4–2.8 g/s) and the lambda correction stayed near zero or
  went negative (−0.6 to −4.3 % in 20 s means): **what came in burns, and the ECU took
  air and fuel away for it** (*reasoned*; whether the machine ran before
  its noted start, 10:23:40, is not recorded, and nothing else explains
  a closing throttle with fuel taken away). **When the calm came — the gas,
  not the air** (9/11 evening, *the owner's question*: had it come the
  moment the hose went on, unmetered plain air would be what calms it,
  pointing at fuel to spare that 032's idle cell already shows; had it
  come with the machine, it is the gas). The 001/003 log in 20 s steps
  against the capture: **10:16:48–10:18:48**, idle with the A/C, the hose
  not yet in: MAF 3.31–3.39 g/s, throttle 2.9–3.0°, lambda −2.5 to +0.5 %,
  `IdleHealth` 43–62. **10:19:08, the intake opened for the hose**:
  **lambda jumps to +4.7 % for one window** — air the MAF did not see,
  the ECU adding fuel for it — and `IdleHealth` reads 42, about where it
  was. **From 10:19:28 lambda is back at −0.6 to +1.6 % and stays there**,
  while the MAF keeps falling (3.04 → 2.78 g/s) and the throttle closing
  (2.7 → 2.2°) **over three minutes**, and `IdleHealth` falls step by
  step, **31, 25, 22, 23, 18, 23, 18, 14, 14**, no dip at all. **The end
  is a step**: at the clean's last idle (11:19:28–11:21:08) MAF 2.44–2.60,
  throttle 1.3–1.8°, `IdleHealth` 19–31; **at 11:21:28 the MAF rises to
  2.75, the throttle opens to 2.4° and within 20 s `IdleHealth` is 61**,
  then 55–76 with dips again once the hose is off. *Reasoned*: **plain
  unmetered air** would hold lambda positive for as long as it came in —
  the MAF under-reading by about 15 % asks about 15 % more fuel — and
  would not let the throttle close; it showed for 20 s, with no calm.
  **What came after is balanced in itself** (lambda near zero while the
  MAF fell by a sixth): **oxyhydrogen**, hydrogen and oxygen in the
  ratio that burns them, carrying energy so the governor took air away
  — **its rise over three minutes is the machine coming up** (cells
  warming; the noted start, 10:23:40, is then the provider's full
  setting or the owner's note, not the first gas), **and its end a
  step**. So **the calm is the gas burning with the charge, not air the
  MAF missed**: a better-burning charge, not fuel to spare. ⚠ The A/C
  was on in the first stretch, the blower on 4 and the heater full in
  the second; the 20 s of plain air are one window.
  **The gas idle taken apart** (9/11 evening, *the owner's question*:
  does it weaken this file's reading of the engine, and does it point
  elsewhere; 30 s windows, the steady pattern fitted as in *A steady
  pattern over the cylinders*, named by taking the strongest slot for 2;
  *ad-hoc script, not kept*):

  | stretch | grade | with the pattern out | the pattern, rms % of a stroke | its slots, sorted | steps ≤ −8 rpm per 1000 |
  |---|---|---|---|---|---|
  | the wait, A/C on 4, no gas | 40–50 | 25–28 | 4.7–5.8 | −8 … +6 | 15–22 |
  | **the gas rising, A/C on 4** | **22** | **9** | **4.5** | −7 … +4.5 | **1.4** |
  | **the gas, the clean's end, blower 4** | **29** | **11** | **5.5** | −9 … +4.6 | **8** |
  | straight after, the hose off | 60 | 38 | 5.9 | −9 … +6 | 34 |
  | stop 3 before its cut / after it | 89 / 49 | 45 / 33 | 8.6 / 5.2 | −14 … +9 / −8 … +6 | 67 / 28 |
  | stop 7 before its cut / after it | 60 / 64 | 41 / 41 | 5.5 / 5.9 | −9 … +6 / −9 … +7 | 36 / 39 |

  **The gas took the random part and left the steady one.** The
  weak strokes and the dips went (steps of −8 rpm and more from 15–39 a
  thousand to 1–8), and the grade with the pattern out fell to 9–11, a
  third of the best stop; **the steady difference between the
  cylinders stayed exactly as it was** — 2 about 8 % strong, 4 about
  5 % weak, the same size and shape with the gas as without, at the
  provider and at stops 3 and 7 — **in one unbroken run from before
  the gas into it (10:16–10:22), the same weak slot stays while the
  grade falls from 49–54 to 18–23**. The advance hardly moved (3.1°
  before, 2.6–4.9° with it). **By cylinder** (`cylscan.py`, 12/11):
  **3 at −8 to −11 % a minute through `44`'s long run at the provider,
  with the gas and without, and −13 % on `45`'s last idle with it** —
  one weak stroke in 4,400; 2 and 1 above. *The slots were named 9/11
  by a count that left the crank wheel's alternation in, and read "2
  about 8 % strong, 4 about 5 % weak" until 12/11; the slot that stayed
  is 3's.* **Read** (*reasoned*):
  - **This file's reading holds and sharpens.** The dips are strokes at
    the edge of stable burning (*What one dip is worth*); a quicker,
    more easily lit charge (*general*: hydrogen's ignition energy about
    a tenth of petrol's, its flame several times faster, and it
    tolerates dilution far better; a few per cent of it is known to
    cut an engine's cycle-to-cycle variation sharply) takes them away
    **even on a smaller air charge** (load 25 % against 30). So *"anything
    that takes a little charge away tips them over"* (*Load smooths
    it*) is better put as **how easily the charge lights and burns**,
    of which its size is one part. At a closed throttle the cylinder
    keeps much of its own exhaust (*general*: residual gas is largest at
    idle and falls as the manifold pressure rises), which slows and
    scatters the burn — **a load lowers that dilution, which is why a
    load calms it, and the gas tolerates it**, which is why the gas
    calmed it more than any load. Not new physics: the same edge, with
    the reason it is an edge named.
  - **Two separate things, then**: **the dips** — a burn that fails
    now and then, cured by a better charge (the clean's effect on 3 was
    on this part: 3's rough start and 014's storm); and **the steady
    pattern** — 3 giving less every cycle, its floor of about −9 %,
    which neither the clean nor the gas touched, so **a difference in
    what 3 gets or keeps, not in how well it burns**: its share of air
    or fuel, or of compression. That fits what acts on 3 alone and on
    quantity — **H3** (runner 3's lower gasket: less charge or a leaner
    one), **H4** (less fuel into 3 through its loom), **H1's seats on
    3**, H13's deposit on them — and not what acts on ignition (the
    spark, plug gaps): those would have been rescued by the gas like the
    dips were. *This read "4 giving less and 2 more", runner 4, fuel into
    4 and 4's inlet seat until 12/11.*
  - **What it points at more now**: for the dips, **anything that
    raises the residual gas or slows the burn at idle on all four** —
    a valve that does not quite close on the exhaust side (H1, H13's
    seat), deposit (H13), and **the cam's timing against the crank**:
    a belt a tooth out moves every valve event, the overlap with them,
    against the piston (one camshaft: the overlap's length stays) and with it the
    exhaust kept at idle, with compression even and the full-load
    power nearly intact (*general*) — the one candidate this reading
    lifts that sits low in the ranking (ninth; its marks are cheap to
    check). And **H0**, an AQY that idles near its dilution limit by
    design, is not weakened: every engine is calmer on hydrogen.
  - ⚠ The gas idles are two stretches of 3 and 2½ minutes, with the
    A/C on in one and the blower on 4 in the other; the pattern named
    by its strongest slot, as at work.
 Straight after, the hose
  off: 60 and 2.6 dips a thousand again. **Read** (*reasoned*): a
  faster-burning, more easily lit charge (*general*: hydrogen's wide
  limits and quick flame) **cures the weak strokes outright, even on a
  smaller air charge** — **the failure is in the burn, lighting or
  spreading**, not a mechanical event; it fits every cause that leaves a
  charge hard to light or slow to burn (H13's deposit, H3's lean runner,
  H4's spark, H7's fuel), and not a part that taps or a stroke that
  loses its charge outright. It does not name which.
- **014 was `deaktiv.` through the whole clean** (load about 19 % at
  1,750–2,150 rpm): it saw nothing there.
- **The fault memory** read at every phase (`vcds/vcds-step8-faults.txt`):
  empty at the start; after stop 3's cut **P1240 (injector 4, open,
  sporadic), P0300, P0304** — the cut's own — and nothing more after
  the clean or stop 7's cut; cleared by the owner at work after 032/055
  (032 −7.8 / +6.3 % at every read, 055 −1.13 before the clean and
  −1.05 after).

**What it leaves** (*reasoned*; *plan.md*'s reading, Part 2 *Step 3*):
**3's swell** — its deficit beyond its floor, its weak strokes, the
rough first minutes and 014's storm — **was not there at stop 7**,
which is the H13 branch for 3 (the deposit that `43` and the borescope
put on 3). **3's floor, about −9 %, and the settled level were kept**:
the clean took the part that came and went with the minutes, not the
floor. ⚠ **One stop each side, and the swell is the thing that varies
most between stops**: stop 3's own second half read like stop 7, 3 was
at −12 % straight after the clean and swelling at work the same
afternoon. **Answered by `47`, a day later**: the swell back on 3
(*The day after*, above) — **the clean did not take it for more than
the day**. *Until 12/11 this read "4's deficit kept, a cause of its
own for 4" (H3 runner 4, H4 4's circuit, H1's inlet seat on 4) and
asked for a second captured stop with a cut on 4.*


**The trend over every capture** (28/10, at the owner's question; every
standing idle settled 30 s and more, graded as `tools/afterpull.py`'s
`idle_runs()` grades, the display's filter replayed beside it;
loads off is b7 ≤ 25 at 93 °C of oil and over):

| | warm, loads off: stop means | middle band, ~77–88 °C |
|---|---|---|
| 11/8 (`09`, `11`) | 48, one 22 s hold | 106 |
| 24/9 (`24`, new MAF) | 88, 92 | 84 |
| 3–10/10 (`26`–`31`) | 67–103, most 75–95 | 90–111 |
| 12–15/10 (`32`, `37`, `38`) | **48–75**, most 55–66 | 93 |
| 18/10 (`39`) | 68–96 | — |
| 21/10 (`40`) | 61–67 | 75 |
| 24/10 (`41`) | — | 87–104, warmed at idle |
| 27/10 (display) | 54 | — |
| 3/11 (`42`, the original map, fresh adaptations) | 93 → 54 over one stop, 63 and 77 near home | — |

**Against the tank's level** (*the owner's question*, 28/10: the Verva
tank run down to about 5 l): the level off 0x320 in each capture
(`tools/replay.py`), beside the warm stops above — 50 l on 24/9 (88, 92);
29→23 l on 3–10/10 (most 75–95); **22 l on 12/10 (63)**; 36→35 l on 15/10
(48–75); 51 l on 18/10 (68–96); 43→40 l on 21/10 (61–67). **No relation**:
the calmest and the roughest both sit at about 22–29 l and at 35–51 l, and
every change of level came with a repair. The display gives no more (28/10:
70–100 at 13→5 l, oil 95–100 °C).

**Before October there is no trend to read**: two days of captures, and
the one hot figure of August is a 22 s hold. **Warm, the idle stepped
down once**, from about 75–95 to about 50–70, **between 10 and 12/10**
(the leads, lead 4 re-seated), rose for 17–19/10 and came back; 27/10
is level with its best, not past it, and **from 28/10 it is back at
about 80–105** on the display (to 2/11), the end of the Verva and the
OMV alike — so not the fuel. **On the original map (3/11, `42`)**
54 ± 3 settled into a stop and 63–77 near home, on fresh adaptations:
back inside the 50–70 band, one drive. **Cold it has come down**, and
that is the clearer change (below, *Temperature*).

**The outside air is not in this trend** (*the owner's question*, 28/10:
August was hot, late October about 10 °C — is the idle the same and only
the weather cooler?). Not on the bus (`docs/firmware/can-decoding.md`,
*What is NOT on the bus*); the intake air is in VCDS 004/006, logged once
(4/10). Against the weather as the whole (*reasoned*): the calmest hot
figure is August's, the hottest month; the warm idle moved **in a step**
between 10 and 12/10 and went up again 17–19/10, not gradually as the
autumn cooled; and the cold drop of 21/10 came on a start at 24 °C of oil,
warmer than the others. **Measured against the weather, 28/10**: the
air temperature of each capture day, 07–19 local, from the SYNOP reports of
Praha-Ruzyně (WMO 11518, via OGIMET), against every warm loads-off stop
(oil ≥ 93 °C, b7 ≤ 25, settled 30 s and more; `tools/afterpull.py`'s
`idle_runs()`):

| day | air, mean (min–max) | stops | `IdleHealth`, each stop |
|---|---|---|---|
| 24/9 (`24`) | 12.6 (10.4–15.1) | 2 | 88, 92 |
| 3/10 (`26`) | 16.0 (11.1–21.2) | 1 | 67 |
| 4/10 (`28`, `29`) | 15.0 (6.0–19.3) | 5 | 72, 80, 77, 95, 93 |
| 9/10 (`30`) | 9.7 (6.0–12.2) | 5 | 93, 75, 77, 82, 75 |
| 10/10 (`31`) | 11.6 (10.3–12.6) | 3 | 78, 89, 103 |
| 12/10 (`32`) | 9.7 (5.4–12.9) | 4 | 72, 48, 59, 66 |
| 15/10 (`36`–`38`) | 11.0 (4.8–15.3) | 6 | 66, 55, 69, 75, 58, 58 |
| 18/10 (`39`) | 10.1 (7.9–11.9) | 3 | 68, 81, 96 |
| 21/10 (`40`) | 10.8 (4.9–13.9) | 3 | 61, 67, 66 |
| 27/10 (display), evening | about 7 | 1 | 54 |

**No relation**: the day means against the day's mean grade correlate at
r = 0.13 (nine days), and days of the same air differ by 20 — 9/10 and
12/10 both 9.7 °C, 80 against 61; the warmest October day, 3/10, is among
the calm ones. Within September–October the weather does not explain the
trend. ⚠ Day temperatures, not the moment of the stop, and the intake air
under the bonnet at a warm idle is set more by the engine than by the
weather. **Not recorded with each reading** (*the owner's decision*,
28/10): with no relation found it is not worth his time; the weather
archive can be asked again if a question ever needs it.

**The MAF is the one change that showed at once** (24/9: the dips halved).
The calmest settled idles, 12/10 and 15/10, came in the days after the new
leads and lead 4's re-seat; the idle has worsened since (*Why the idle got
worse*, below).

**What is not known: the healthy target.** Every recording is of this engine
with the fault present, and **none will be**: a CAN capture of another car
needs its cluster harness tapped behind the vent, which no owner will allow
(*owner*, 21/10).

**When S1 closes** (*the owner's decision*, 12/11; he closes it):
**`IdleHealth` steadily under 30 at a warm idle, never above it, in the
everyday state and with every load off alike**, oil 95–100 °C, after
the adaptations have settled (032 and 055 not freshly reset), over
**three drives on different days**. **Warm only** (*the owner*, 12/11):
a rough cold idle is no part of the mark — it may be this engine's
own (H0). It asks for what the idle needs:
cylinder 3 level with the others (S1, *Every stroke named*) **and** the
common part gone (*The idle's candidates, ranked*, lists B and A) —
only both together get the grade that low; **the provider's gas did it
once**, with the A/C or the blower on (14–29, 9/11); nothing else has. *Reasoned*: about 8 of the
grade is the crank wheel's own alternation (*A steady pattern over the
cylinders*), which every engine with this wheel carries, so under 30 is
strict but within reach of a healthy idle. `tools/cylscan.py` is read
beside it to say which part moved, but is no mark of its own. Short of
it, the owner may close S1 as *acceptable, cause known*. *Until 12/11
the marks were three — the dips no longer keeping to a pair
(`cutscan.py --shares`, removed), loads-off `IdleHealth` within about 25
of loads-on, at least the best level shown, about 50–60 loads off
(decided 20/10); on 12/11 for a few hours they were cylinder 3 level
by `cylscan.py` alone, and the same day the owner replaced them with
this.* **Probably on the overrun as well** (*the owner's decision*,
28/10): the downshift without a blip, where the load reads about 10 %
(VCDS 014, field 2) and the bangs of S14 come, is the thinnest charge
and so the strictest test (*owner*). strictest test (*owner*). **Read by ear, not by 014** (*owner*): on the overrun 014's
misfire recognition reads `deaktiv.` — in every 014 log in
`test/fixtures/vcds/`, every row above 1300 rpm with the load under 20 %
reads it, none `aktivováno` (counted 28/10) — so the counter cannot move
there.

**Load smooths it.** Every consumer at idle — A/C, lights, blower, heated
glass — makes the ECU open up the air, and the idle calms (26/9: 35–50 loads
on against 70–80 off, *owner*). The supply voltage is 1.25 V *lower* then,
so it is the charge, not the volts. **Since the cleaner, the partial loads
hardly matter** (*owner*, 19/10): lights and blower alone make little
difference, everything on together still calms it. **The first measured
pair**, 19/10, oil 101 °C: loads off mostly about 100, every load on mostly
about 50 — twice what one pair can show by chance. **Again 4/11**
(display, oil about 100 °C, *owner*): 90–110 in the everyday state
against **45–50** with the A/C, the blower on full and the rear window
heated, while the supply fell to about 12.4 V at times — the calmest
idle on the lowest supply. **Read beside the higher idle of 12/10**
(`refuted.md` D9; *reasoned*): a load raises the charge of every stroke
at the same engine speed, and helps; 830 rpm raised the speed on about
the same charge a stroke, and did not. **So what fails answers to the
charge a stroke and the cylinder's pressure, not to the air flow or the
speed** — and a weak spark would go the other way twice over: a higher
cylinder pressure asks more voltage to break down the gap, and the
supply is lower (*general*). Read as (*reasoned*):
**one or more cylinders run at the edge of stable combustion at the idle's
charge**, and anything that takes a little charge away tips them over.
**A second reading, from 26/10** (*the owner's hypothesis*, not tested):
**with the A/C and every load on, the ECU sets its learnt idle air aside.**
In the relearning log of 26/10
(`test/fixtures/vcds/vcds-step6a-055-relearn-014-055-001.csv`,
`idle-log.md`) 055's learnt value read **exactly 0.00 whenever its load
bits read `0101`** — the A/C and all-loads stretches — and came back the
moment they returned to `0000`. That learnt value was once read as what
switches 014's counting (`refuted.md` C19, refuted 2/11), negative on this
engine since September.
So "every load on" may calm the idle not by the load at all but by
taking the learnt value out of play; and **since the cleaner the partial
loads hardly matter while everything on together does** — and
everything on is the one state with the A/C in it. **What would test
it**: at a warm stop, a minute of the everyday state with the A/C alone
against a minute of every load but the A/C, `IdleHealth` and 055 field 3
read in each; and a log of 055 with 014 across such a switch. ⚠ Which of
the bits is the A/C was not separated, and whether the ECU uses another
learnt value with the A/C on, or none, is not known. **Ross-Tech's list
of groups 050–059** describes a variant of 055 *"with separation for rear
window defroster/A/C readiness"* (searched 26/10): **a separate learnt
value for that state** would read 0.00 too if the disconnect of 26/10
reset it and it had not relearnt yet. So the 0.00 may be a second learnt
value at zero rather than none. **Read it at the next A/C stop**: field 3
staying at 0.00 over minutes of A/C idle says none or not shown; moving
away from 0 says a learnt value of its own.
**Read at the A/C stop of 27/10** (the done `plan.md` 6k, `idle-log.md`; oil about
90 °C, warm; `vcds/vcds-step6k-2-014-055-001.csv`): **`0101` is the A/C** —
every load but the A/C left the bits at `0000`. **Field 3 held 0.00 for
eight minutes of A/C idle and a drive**, never moving, while field 2, the
live correction, went to about −1.0 g/s, the learnt value's size: **with
the A/C on the ECU sets the learnt value aside and corrects live**, and
no second learnt value showed. `IdleHealth` off the owner's video, the
everyday state about **70**; **the A/C alone 35–50** from its second
minute, 014 silent; **every load but the A/C about 57**, the learnt
value *not* set aside but walking from −1.04 to −0.77 while it ran, and
37 at its end; **both together 25–35**. ⚠ Against the learnt value alone:
in the A/C's sixth minute, field 3 still at 0.00, the grade climbed back
to 56–75. **Read as** (*reasoned*, one stop): both act — the A/C's calm
is the larger and the quicker, and the loads calm the idle without the
learnt value set aside, as it moves towards zero. Neither of `plan.md`'s
clean outcomes; neighbouring 2-minute windows differ by 4–18.

**Temperature.** Roughest cold, calmer as the oil warms, calmest hot, in every
session since 24/9. Every engine idles roughest cold (*general*), so this
says nothing about the fault on its own. The roughest reading yet, ~186, came
cold on the dampest, foggiest morning (26/9, *owner*).

**The cold idle has come down since 21/10** (*the owner's observation*,
28/10: over 100 now only after a start, about 130 at the coldest, nothing
near 200; checked against every capture with a cold start, the same day).
The display's highest in the first idle after a start, and the stop's
mean:

| start | oil at the start | first idle: mean / display's highest | the idle after it, 23–39 °C |
|---|---|---|---|
| 11/9 (`18`) | 21 °C | 108 / 157 | — |
| 24/9 (`19`) | 17 °C | 111 / 179 | 134 / 160 |
| 26/9 (display) | cold | ~186 (*owner*) | |
| 3/10 (`25`), fresh adaptations | 21 °C | 127 / **196** | 161 / **196** |
| 4/10 (`27`), fresh adaptations | 19 °C | 112 / 185 | 160 / 181 |
| 9/10 (`30`) | 17 °C | 107 / 148 | 114 / 140 |
| 10/10 (`31`) | 18 °C | 105 / 165 | 147 / 184 |
| 12/10 (`32`) | 15 °C | 121 / 178 | |
| 14/10 (`33`) | 20 °C | 103 / 150 | |
| **21/10 (`40`)** | 24 °C | **77 / 90** | **118 / 145** |
| 24/10 (6e, display) | cold, under 70 °C | 120–140 (*owner*) | |
| since (display) | | about 130 at the coldest (*owner*) | |
| 2/11 (display) | 22 °C | 110–140 (*owner*) | |

`35` (15/10) is left out: it started with every load on. **The first
capture that reads low cold is 21/10's**, the first drive on the VW plugs
and leads and the new plenum gasket, **two days before the first 44K
tank** — so the cold drop is not the cleaner's, whatever else it may be.
⚠ One capture: 21/10 started at 24 °C of oil, warmer than the 15–21 °C
of the others, and the display since is the owner's glances. A cold
capture from about 15–20 °C would settle it.

**But warm oil alone does not bring the calm idle; driving does** (26/10,
*the owner's observation, checked against the captures*). On 26/10 a
gentle warm-up in a jam, under 3000 rpm, held `IdleHealth` at 80–100 up
to 92 °C of oil; it fell to 60–70 only after one brisker stretch (table
above). **The same again 4/11** (display, *owner*): mostly slow driving
and queues at about 100 °C of oil held **90–110**, with the larger dips
felt in the seat, until the engine was revved; **70–90** after it. The
captures agree in kind (`tools/afterpull.py`'s `idle_runs()`,
graded per minute, 26/10): **warmed at idle, the grade stops at about
90–110** — `41` ~120 → ~90 over 52–82 °C, `32` 139 → ~95 over 46–78 °C,
`25`+`26` ~110 at 82–91 °C after a warm-up that never held 3000 rpm —
and **every calm warm idle came after a drive**. **What the drive needs is
not high revs**: `26` read 67 at 96 °C after a drive home under
3000 rpm, `35` 38–55 at 91–94 °C after one that touched 3292; and high
revs do not reliably calm it (`19` 57 → 104–143 after 6000 rpm, before
the cleaner — *After high revs*, below). ⚠ **Not separated**: no capture
warms past 92 °C at idle alone, so a few degrees more oil and the drive
itself always came together. The owner's reading (*hypothesis*): the
chambers carry something — deposit, oil, moisture — that a working drive
clears and an idle does not (H13, H18; H17 refuted, `refuted.md` C21). Settled by a warm-up to 95 °C at idle alone,
or by a gentle warm drive straight into an idle.

**What comes before a dip** (`tools/dipcontext.py`, 852 warm dips,
10/10). **The ECU has trimmed the charge just before a dip** — injection time
0.33 and indicated torque 0.35 counts lower 0.4–0.1 s before, about 1 %, and
engine speed a few rpm higher: the idle overshoots a little, the governor
takes a little air or advance away, and a weak cylinder fails in the next
cycles. A dip follows a trim down 1.6–3.5 times as often as a trim up. ⚠ An
average, under one count; no single dip shows it. The figure `dip-profile.svg`
beside this file shows one dip stroke by stroke.

![One idle dip](dip-profile.svg)

**The dips ride a swing of the idle loop at about 0.8 Hz** (5/11, the
same fresh look). Engine speed at idle oscillates with a period of
1.2–1.4 s, and the same line stands in b7 and in the injection time.
Intervals of 1.0–1.25 s between dips come 2.1 times as often as by
chance, so about one dip in ten is an echo of the one before; averaged
over 1,093 dips the ECU trims injection and b7 down **twice, 1.6 s and
0.4 s before**, and speed has a trough 1.2 s before and after. Over
seconds the dips are otherwise random; **over minutes they come and go**:
nine dip-free stretches longer than 64 s against 0.3 expected, with no
regular period. Within warm loads-off stops neither the grade nor the dip
rate follows oil (80–105 °C), b7, idle speed, time since the start or the
stop's length. *Reasoned*: a ringing loop decides when a marginal
cylinder fails — combustion at its edge, not an electrical fault, which
would not care about the loop's phase.

**What VCDS saw just before a dip** (11/10, `dipcontext.py --vcds`): on two
sessions the lambda correction was about 0.8 % lower just before a dip than in
quiet idle — the loop on its lean swing. **Not reproduced on 12/10** (`32`,
001 alone, the session built for it): a direction one session failed to
repeat.

**How many strokes make a dip** (`tools/dipshape.py`, 5/11, *at the
owner's question*; every warm `_z1` idle, oil ≥ 80 °C, cuts left out,
1,870 dips). A dead stroke is **one step**, not two: on the cuts the dead
slot reads one step of −23 to −29 rpm and the next windows +12 to +18 and
+7 to +11. So counting the strokes that lose more than 8 rpm inside a dip
— **each against its own cylinder's median step**, since the idle carries
a steady pattern over the cylinders (*A steady pattern over the
cylinders*, below) that otherwise names most weak strokes for the low
slot — separates **one weak firing (75 %) from two in a row (22 %) and
three or more (3 %)**; two in a row are always **two different
cylinders**, the next in the firing order. *The figures of the first
reading that day were taken on raw steps (64 / 32 / 4 %, and "15 of 17"
clusters on 3 below) and are superseded.*
- **Deeper dips are more often clusters**: 20–25 rpm 85 % single, 25–30
  69 %, 30–40 53 %; at 40 rpm and more 29 %, but those are mostly slow
  sags (the largest step a fifth of the drop: a load, the regulator), not
  runs of failed firings. ⚠ Requiring 20 rpm favours clusters by
  construction (two steps of −12 make a dip, one does not).
- **Weak firings come together, about 3½ times as often as by chance**:
  3.2 % of all steps lose more than 8 rpm against their cylinder's median,
  10.9 % of those straight after one that did.
- **Not changed by any repair**: by period the single share is 73–78 %
  and the follow-on 2.3–5.7 × chance throughout, while the dips per 1000
  strokes fell from 9.8 (`19`/`20`/`24`) to 4.9–5.8 (`40`–`43`). **The
  repairs took dips of both kinds away alike**, and the depth
  distribution kept its shape (Kolmogorov–Smirnov before against after
  12/10: D 0.04, p 0.54).
- **Cold, more clusters**: below 40 °C of oil 60 % single (833 dips)
  against 75 % warm, at the same depths.
- **Which cylinder**: the weak strokes are 3's, warm and cold (S1,
  *Every stroke named*: 58–73 % on `40`–`47` warm, 56 % on `41` cold).
  *This bullet named them with `dipshape.py --name` until 12/11 — on
  `43` 24 of 58 single dips on 3, 9 of 12 pairs with 3 in them, and
  "cold, `41`, spread over all four" — on a count that slipped; that
  option was removed with it (Naming the cylinder).*

**A steady pattern over the cylinders, apart from the dips** (5/11, the
owner's request for a fresh look at the data; scripts not kept, the
reading is described here). ⚠ **Re-read 12/11** (*Every stroke named*,
below): the pattern is real, but **1.7 rpm of it is the crank wheel's
own alternation**, and with that out the weak cylinder is **3 alone**,
4 level and 2 and 1 above. **Split again 12/11** (`cylscan.py`'s
stroke count and wheel, the grade rebuilt per stroke over 497 warm
30 s windows of 20 captures, the A/C off at the start of the run;
*ad-hoc script, not kept*): of a grade of about 68, **about 8 is the
crank wheel's alternation** — no combustion in it, a floor no repair
can lower, which the display carries on every engine with this wheel
(*reasoned*) — **about 22 is the cylinders' steady differences**,
mostly 3's, and **about 38 is what is left** with each window's four
slot means out. So "about a third" holds for the pattern as measured,
**but an eighth of the grade is the wheel's, not the engine's.** The
step from one firing to the next carries
a **period-4 component of 3–6 rpm** (0.2–0.9 with the steps shuffled): a
steady difference in what each cylinder gives, present with no dip at
all. **It is about a third of `IdleHealth`**: over 318 warm loads-off
windows of 30 s from 19 captures the grade averages 78, and 51 with each
window's four slot means taken out. It is independent of the dips (rank
correlation 0.21 with dips per 1000 strokes, 0.02 with what is left) and
**moves over minutes**: in `31` it rose from 1.0 to 5.8 rpm and took the
grade from 71 to 110 with the dips unchanged; in `43`'s stop the settling
from 86–114 to 31–55 was mostly this pattern fading. The A/C's load
(`40`) calms the rest and leaves the pattern as large as loads off. The
display's swings inside one stop (27/10, *waves of about 1½ min*) are
more likely the radiator fan (below, *The radiator fan's cycle*). *This
said "can be this alone" until 6/11.* *It named the slots by the cuts
too, until 12/11: "warm, 3 and 4 give the least and 2 the most" (`31`
1 −2.1, 3 +3.1, 4 +4.1, 2 −6.0 % of a stroke short; `43` alike), with
the crank wheel's alternation in and on a count that slipped; by
`cylscan.py` `31` reads 1 +8, 3 −15, 4 −3, 2 +11 and `43` 1 +5, 3 −13,
4 +2, 2 +6 % (S1, *Every stroke named*; Naming the cylinder). The
"pattern's phase holds for minutes, then drifts or jumps" it noted was
that count slipping, as 9/11 found (the shifted pattern correlating
0.9–1.0 with the cut's); `refuted.md` A5's slot means of 3.5–5.9 rpm
"with no consistent outlier" were the same pattern read on runs whose
phase was lost.*


**The radiator fan's cycle** (6/11, *at the owner's question about the
waves*; every warm settled stop of 4 minutes and more without an
injector cut, nine stops in seven captures, 77 minutes; `IdleHealth`
rebuilt every 2 s over 10 s; *an ad-hoc script, not kept*). **At every
warm stop the coolant (0x288) climbs to 100.5 °C and falls to 92–97 °C
again, a cycle of 74–90 s on most stops** (to 170 on a few) — the fan
switching on and off (*reasoned*; the switch points are not on the
bus). **The engine's torque (0x280 b7) rises 12–18 s before the coolant
turns down**, and **`IdleHealth` falls with it**: averaged over the
nine stops, the correlation with the coolant's fall 12–18 s later is
**+0.40 for b7 and −0.36 for `IdleHealth`**, against about ±0.06 for
the same series shifted at random (some 6 standard deviations). The
fan's load comes first and the coolant answers later, as a fan's would.
Split crudely by the coolant's slope, `IdleHealth` is about 6 % lower
while it falls. **Read** (*reasoned*): the waves are mainly the fan, one
more load that smooths the idle (*Load smooths it*), not a cause inside
the engine; a reading at a warm stop catches the fan on or off by
chance, which is part of the display's spread.

**Every stroke named: one weak cylinder, and it is 3** (12/11, the
third research, *the owner's request*; `tools/cylscan.py`, kept, with
its tests; how the count, the wheel and the spread were found is in
*Naming the cylinder*, *The count that does not slip*). Every standing
idle of every `_z1` capture, each stroke on its cylinder for the whole
run, the crank wheel's alternation taken out, each stroke's loss
gathered from the two slots it shows in. **Per cent of one stroke's
work against the four's mean** (a cylinder out is −100), and the weak
strokes — a step 12 rpm or more under the cylinder's own median — per
1000 of its strokes:

| captures, warm (oil ≥ 85 °C) | 1 | 3 | 4 | 2 | weak per 1000: 1 / 3 / 4 / 2 | 3's share of the weak |
|---|---|---|---|---|---|---|
| `19` (24/9, the old MAF) | +8 | **−13** | −11 | +16 | 5 / 26 / 38 / 6 | 35 % |
| `24`–`31` (24/9–10/10) | +6 to +13 | **−11 to −18** | −7 to +1 | +1 to +13 | 1–7 / 13–32 / 5–16 / 0–5 | 48–75 % |
| `32`–`39` (12–18/10) | +4 to +11 | **−10 to −20** | −4 to +3 | +7 to +9 | 0–3 / 6–37 / 2–7 / 0–2 | 55–77 % |
| `40` (21/10, VW leads) | +6 | **−14** | +1 | +7 | 5 / 15 / 3 / 1 | 64 % |
| `42`, `43` (3/11, the original map) | +2, +5 | **−14, −13** | +1, +2 | +10, +6 | 5 / 15 / 4 / 1 | 58 %, 62 % |
| `44` (9/11, before the clean) | +4 | **−11** | −1 | +8 | 1 / 4 / 2 / 0 | 58 % |
| `45` (the gas, the clean's last idle) | +6 | **−13** | +1 | +6 | 0 / 1 / 0 / 0 | one weak stroke in 4,400 |
| `46` (9/11, after the clean) | +3 | **−10** | −3 | +10 | 3 / 6 / 6 / 1 | 38 % |
| `47`, `48` (10/11 evening) | +5, +4 | **−15, −14** | +4, +4 | +6, +6 | 3 / 16 / 2 / 1 and 2 / 6 / 2 / 0 | 73 %, 61 % |
| `49` (12/11, the canister) | +2 | **−9** | +4 | +3 | 3 / 7 / 2 / 1 | 54 % |
| `50` (12/11 evening, the queue drive's last stop) | +5 | **−16** | +4 | +7 | 2 / 22 / 5 / 1 | 74 % |

- **Cylinder 3 is the weak one in every warm idle on record, 10–20 %
  under the mean** — from 24/9 on (`19`, the first warm idle long
  enough to read), on three sets of plugs and of leads, two MAFs and
  both maps. **And before the injectors were changed (23/9), as far as
  the short idles of August can say** (*the owner's question*, 12/11:
  did 3 lead on the old set too): `09` (11/8, 60 s warm) **3 −19 %**,
  `12` (25 s, the A/C on) **−11 %**, `17` (11 s) **−23 %**, `11` (25 s)
  −21 % with the strongest slot too close to name; only the cold start
  of 11/9 (`18`) had 4 the weakest, −14 %, and 3 −5 %. ⚠ Seconds, not
  minutes, and the names rest on the strongest slot being 2's, which no
  cut checked on the old injectors. **Cylinder 4 was weak on 24/9
  (−11 %) and is level warm since early October**; 2 and 1 give more
  than the mean throughout. *This file said "3 and 4 weak, 2
  strong" and "4's steady deficit, 5–8 %" until 12/11*: the crank
  wheel's alternation reads cylinders 1 and 4 low by 1.7 rpm at idle
  and 3 and 2 high, which took 3's deficit for 4's.
- **3's deficit is there in every state**: cold (−11 to −17 % under
  60 °C of oil), warm, **with the A/C on (−10 %, its weak strokes
  nearly gone: 1.6 per 1000 against 12)** and **on the provider's gas
  (−9 to −13 %, one weak stroke in 4,400)**. So the gas and a load take the
  misfires and leave the deficit: *reasoned*, 3 gets or keeps less
  charge than the others all the time — its air, its fuel, or what it
  holds through compression — and that same shortage puts it nearest
  the edge at the smallest charge, where its strokes fail.
- **Cold, 4 is weak with 3**: under 60 °C of oil 4 gives 6–14 % less
  (`18`–`41`) and the weak strokes fall **3 > 4 > 1 > 2** (45 / 34 /
  15 / 6 % of 1,700 on `24`–`39`; 54 / 23 / 16 / 7 % of 310 on
  `40`–`47`) — **the borescope's order of the deposit, 3 > 4 > 2 > 1,
  but for the last two** (H13). Warm, 4's weak strokes fell from 38
  per 1000 (`19`) to 2–7 from 12/10 on: what the leads and the MAF
  cured was mostly 4's.
- **3's deficit moves over minutes, and falls in a step**
  (`--minutes`; per cent, and 3's weak strokes in each minute):
  `44` stop 3, after the motorway: **−18, −19, −19, −23, −27** with
  11, 12, 3, 12, 12 weak strokes, the 30 s cut on 4, then **−10, −9,
  −8, −9, −9** with 0–1; `43`: −14, −18, −18 up to its cut, −7 to −10
  after, climbing back to −14 by the tenth minute; `47`, **no cut**:
  −15, −15, −14, −14, −17, −20, **−26, −22**, then **−9, −10** from
  17:38 — *the four calm minutes that were "unexplained"*; `40`: −14
  with 22 weak strokes in the first minute, **the A/C on: −9 to −11
  with none**, the A/C off: −11 climbing to −22 over seven minutes;
  `49` (12/11, the canister), **no cut**: −14, −19, −23, −13 with 12,
  17, 9, 6, then **−5 to −8 for fourteen minutes** with 0–3, the step
  inside 40 s at 11:19:30 and no second swell; `50` (12/11 evening,
  the queue drive's last stop), **no cut**: −13, −14, −20, −20, **−8**,
  −11, −15, −18, −22, −17, **−8**, −14, −18, −18, −23 with 8, 9, 10, 8,
  4, 4, 8, 19, 17, 6, 3, 4, 11, 9, 11 — **three swells in fifteen
  minutes**, the bottoms 5½ minutes apart.
  So **"a warm stop starts rough and settles" is 3's state**, it is
  not tied to the stop's first minutes (`40`, `47`), and **what ends it
  is a jolt — a cylinder cut, a load, or nothing seen** — not time.
  *Read again 12/11 evening (*The swell's shape*, below): the fall
  with nothing seen takes 30–45 s, and a load masks the swell without
  ending it — a sawtooth, not a jolt.*
  Over 205 warm loads-off windows of 30 s since 21/10 the grade
  correlates −0.6 with 3's deficit; 3's weak strokes go from 0.6 a
  window at −8 % to 4.8 at −22 %, the other three's stay at 1.2–1.7.
- **The small steps are on all four.** With each cylinder's own
  median taken out, the scatter of a stroke is 3.5 rpm rms on 1 and 4,
  4.2 on 3 and 2.9 on 2 (`40`–`47`, warm, 146,000 strokes): the
  everyday unevenness under the misfires is common, 3 a fifth above,
  2 a sixth below — the strongest cylinder is the steadiest. That
  part is what "the common part" of the two lists measures; **the
  misfires that 014 counts are not in it** (S3).
- **What it does not say**: why 3 is short. Not its plug or its lead,
  each changed twice with 3 unchanged; not the coil, whose other
  tower fires 2, the strongest; **and hardly its injector**: 3 was the
  weak one on the old set in August and on the new one since, and the
  same place failing in two sets is unlikely (*the owner's argument*,
  12/11). **Left for 3 alone: its valves, seats, guides and lifters
  (H1), the deposit on them (H13), its runner's joint (H3), its
  injector's wiring, which stayed (H4), coolant (H20)**. A slow growth
  ended by a jolt fits something that settles and is shaken off — a
  valve not quite seating on its deposit until it turns or a flake
  moves, a lifter — better than a leak, a wire or a short injector,
  which have no reason to mend at a cut on another cylinder
  (*reasoned*, weakly: the mean mixture did not differ between the
  swell and the calm at `44`'s stop 3, 001's regulation −0.2 % in
  both, so it is not the trim creeping).
  ⚠ The deficit's scale rests on the cuts (a dead stroke is 34 rpm of
  step); the names on the strongest slot being 2's, which held at all
  eight cuts and puts 014's misfires where the ECU's own P0303 does.

**The idle speed target** (0x288 b5, decoded 10/11 at the owner's
request, `docs/firmware/can-decoding.md`, *The bus byte by byte*; *the
owner's question*: does the target follow anything, did it come down
with the hydrogen, and is a lower idle a calmer one — his feeling).
Over every capture with a time base, 30 s windows of settled idle,
coolant 85 °C and over (434 windows; *ad-hoc script, not kept*):
- **The target is fixed warm: 780 rpm in 410 of 434 windows**; the
  other 24 are `32`'s idle-adaptation steps (800, 820, 830 rpm). Cold
  it starts at 900 and steps down to 780 as the coolant warms (`18`,
  `41`, `47`). **It did not move on the gas of 9/11**, nor at any warm
  stop since August — so it carries nothing about the idle's quality.
- **The engine sits 15–18 rpm above it** at every warm idle (794–798
  rpm, every capture), the governor's own offset.
- **The actual speed does not tell a calm idle from a rough one**:
  loads off, A/C off, the 343 windows at 785–805 rpm show no relation
  between speed and `IdleHealth` (r 0.07; medians 70–71 in every 5-rpm
  band); the few above 805 rpm were rougher, 84–93, too few to say.
  **The gas idle**: 788–797 rpm in the clean's last two minutes (one of
  the lowest), but 796–805 with the gas and the A/C at the provider —
  at 14–27 either way.
- **Raising the target leaves the grade where it was**: `32`'s steps
  put the engine at 798, 819, 835 and 848 rpm and `IdleHealth` read 66,
  66, 66 and 67 (`refuted.md` D9, measured the same way).
- **Read** (*reasoned*): **a lower idle is not by itself a calmer one**
  on this engine; what the owner feels as calmer at a lower speed is
  more likely a different shake at a different frequency than a
  different combustion. Not a symptom, not a test.

**After high revs** (*owner*, 23/10 evening, the first 44K tank,
display, the everyday state): straight after a stretch held at high revs,
`IdleHealth` **37**, the lowest yet in that state, then **slowly back to 50
within about a minute and above it after another**; stretches of plain idle
without revving go back to 70–80. **New to him**, though he watches the
display and drives hard most days now: after hard driving before, the
lowest came only after about half a minute. **The captures agree that it is
new** (`tools/afterpull.py`, 23/10): engine speed held above 4000 rpm at
any load — sustained revs, a light foot in second as often as full
throttle (*the owner's correction*) — in the five minutes before a warm
stop, the grade in bins from the moment the idle settles. Without a
cleaner the idle after high revs **starts rough and calms over 1–3
minutes** — `30` 98 → 56 (33 s above 4000), `40` 100 → 54 (30 s), `39`
87 → 69, `28` 92 → 70; the one capture with a cleaner in the tank and high
revs before a stop, `37` (Liqui Moly, 15/10), **starts calm and rises** —
57, 44, then 60, and 64, 54, 77, 76 at the next stop. One capture, two
short stops, against a bin-to-bin scatter of ±20 in a single idle; **no
capture after high revs on a 44K tank** (the tanks ended 29/10), and none holds more than 18 s above 4000 at a
stretch, far less than the owner drives now.
Read as (*reasoned*), if it is the cleaner: what the cleaner has loosened
and not yet removed (H13) costs combustion at idle on the cylinders that
carry it, and the heat and gas flow of high revs clear or dry it for a
while — flakes under 3's exhaust seat blown out (*the owner's reading*), or
softened deposit that soaks up fuel at a cool idle and is dried hot.

**The rough start of a warm stop is cylinder 3's** (11/11, the research
of 11/11, *agreed with the owner*; every warm `_z1` stop of 3 minutes or
more at oil ≥ 85 °C, `afterpull.idle_runs()` graded, scripts not kept).
**After a drive with high revs a long warm stop starts rough and settles
within 5–8 minutes**: `42` 90–96 → 54, `43` 81–91 → 41–50, `44` stop 3
79–98 → 45–53; graded 0–3 minutes against the rest, **`40` 72 → 58 (63 s
above 4000 rpm in the 15 minutes before), `43` 86 → 55 (215 s), `44`
83 → 62 (75 s), `49` 85 → 40 (339 s, 12/11, no cut)**. **After a gentle drive it does not**: `24` 85/83, `28`
65/76, `30` 89/97, `31` 75/79, `32` 55/62 and 57/68, `40`'s second stop
63/69, `47` 56/62, `48` 51/68 (0–26 s above 4000) — level or slowly
worse, as queuing is. The exceptions: **`46` stop 7**, after the most
high revs of the week (234 s) and 40 minutes after the clean, **58/66,
no rough start**, and `37` (gentle, 64 → 41). **The rough minutes are
3's swell** (`cylscan.py --minutes`, 12/11; *Every stroke named*):
`44` stop 3 3 at −18 to −27 % with up to 12 weak strokes a minute,
then −8 to −10 % with 0–1; `43` −14 to −18 %, then −7 to −10 %; `42`'s
first stop −18 % with 27 weak strokes per 1000, the next four about
−10 % with 0–11, and −16 % with 22 at the last; and the dip rate falls
with it. So **"3 is worst" and
"a warm stop starts rough" are one observation**, and the cylinders
are compared between captures on the settled part, or minute by
minute. *This read "the dips of the first 8 minutes keep to one slot"
(top two 68 %, p 8 × 10⁻⁵) and "3's 7–14 % deficit is the rough
minutes', 0–2.5 % settled" until 12/11: a count that slipped, the
alternation left in (Naming the cylinder).* **The cuts did not make the
settling**: `42` and `47` settled without one.

Nothing on the bus shares its time: coolant (94.5–100.5 °C, cycling about
once a minute), the fan, oil, the idle target (780), the plate and b6 the
same in rough and calm minutes; b7 and the fuel rise with the roughness
about 20 s after it, the governor answering; 055 converging over the same
minutes on `42` and `43`, but its two fields' sum hardly moving (H8). The
radiator fan and the rear probe never tracked it. *Reasoned*: a seal on
3 that leaks hot, or a flake the drive loosens and the idle seats or
burns away (H13 with H1's exhaust seat), fits a fault that is worst
right after a hot drive and fades as the head cools to idle; a heat
soak of the fuel rail would fit the time but not one cylinder (H7); a
coolant weep into 3 would fit the pressure after a hot drive (H20).
⚠ Older captures show swells every 4–6 minutes rather than one rough
start (`31`, `32`, `28`); whether they are the same thing in stops of
another length is not known.
**Read 12/11** (*Every stroke named*): they are — 3's deficit swelling
and falling back in a step; the "rough start" is a swell that happens
to be under way on arrival, and `40` and `47` show one starting minutes
into a stop.

**The first captured stop on the canister** (12/11, `49`; `plan.md`
item 6; `cylscan.py --minutes` and `--vcds`, the rest *ad-hoc scripts,
not kept*). A warm drive of 30 minutes with five full-throttle pulls
(40.7 s above 4,000 rpm in the five minutes before the stop), then 18
minutes standing, 11:16:04–11:34:28, oil 102 °C, the everyday state but
the seat heater off until about 11:31 (*owner*), the A/C off, **no
cut**. The question it was captured for (H16, *Re-read 12/11*): which
part of the idle the canister lowered.
- **The swell came as before.** 11:16–11:19:30: 3 from −11 to −23 % of
  a stroke in 20 s windows, 12, 17, 9 and 6 weak strokes a minute,
  `IdleHealth` 76–89, **014 at 0.69 % of combustions** (0.46–1.05 % a
  minute) with **37 of its 40 rises on 3** — `44` stop 3's storm
  (−18 to −27 %, 1.03 %) at a smaller size.
- **Then a step with nothing seen**: 3 from −21 to −6 % between
  11:19:25 and 11:19:45 — no cut, the A/C off throughout, the throttle
  byte the same; 033's regulation −0.4 to −1.1 % in every 30 s before
  and after (sd 1.0–1.1), so the mean mixture did not move with it, as
  at `44` (001's −0.2 % in both).
- **The floor held fourteen minutes** with no second swell — where
  `43` climbed back to −14 % by its tenth minute and `40` to −22 over
  seven: 3 at −5 to −8 % a minute, 0–3 weak strokes, `IdleHealth`
  30–44, **014 one count in 19,400 combustions** (on 4, 11:33:56), at
  29–33 % load — the load where it counts less (S3), but it counted
  0.69 % at the same 29–31 % in the swell. The small dips there are on
  all four (S1, *What is seen*: the seat shudders), each cylinder's
  scatter 3.1–3.4 rpm rms with 3 no longer above. The seat heater's
  last three minutes read 37–39, 3 at −8 %: nothing to tell on three
  minutes.
- **Against the settled floors before the canister** (warm, loads off,
  the A/C off, the last four minutes of each stop; the grade rebuilt
  per stroke, and with each 30 s window's four slot means out — the
  common part):

  | stop | `IdleHealth` | per stroke | slot means out | 3 | 2 | steps ≤ −10 rpm a minute, 3's share |
  |---|---|---|---|---|---|---|
  | `43` (3/11, after its cut) | 48 | 47 | 36 | −10 | +3 | 12.5, 70 % |
  | `44` stop 3 (9/11, after its cut) | 47 | 46 | 28 | −9 | +6 | 8.2, 30 % |
  | `46` stop 7 (9/11, after the clean) | 64 | 62 | 36 | −9 | +9 | 13.2, 32 % |
  | `47` (10/11 evening, before the calm) | 64 | 66 | 42 | −18 | +4 | 16.5, 73 % |
  | `48` (10/11 evening, the calm's end) | 39 | 37 | 31 | −9 | −1 | 8.3, 44 % |
  | **`49` (12/11, the canister)** | **37** | **36** | **30** | **−8** | **−1** | **8.2, 18 %** |

- **Read** (*reasoned*): **settled, this stop is as calm as `44`
  after its cut and `48` — the calmest floors before the canister — and
  no calmer**: the same grade, the same common part, the same small
  steps a minute; 3's floor a point or two smaller and 2's surplus gone,
  as at `48`. **So by H16's own test the canister did not take away
  what tips 3** — it swelled after the hot drive as before — **and the
  calm is in the floor all four share, which was there before the
  canister too.** What this stop has that the earlier ones did not is
  the floor's length, fourteen minutes without a second swell; one stop.
  The two calm stops of 11/11 and 12/11 night on the display read as
  this floor (*owner*: 25–40 and 35–50 for minutes), reached without a
  cut.
- **The grade taken apart** (12/11 evening, *the owner's question*:
  what part is 3, what the common part, what the wheel; per stroke,
  30 s windows; *ad-hoc script, not kept*). The wheel's alternation
  taken out alone, then each cylinder's mean step; what is left split
  by slot, **slot 2 the clean reference** — 3's weak stroke spills into
  1's slot before it and 4's recovery after, 2's is the farthest from
  both:

  | `49` | grade | the wheel | the steady pattern (3's deficit, 2's surplus) | 3's weak strokes and their spill | common (as slot 2) |
  |---|---|---|---|---|---|
  | the swell, 11:16–11:19:30 | 78 | 5 | 27 | about 25 | about 21 |
  | the floor, 11:20–11:34 | 37 | 4 | 4 | about 3 | about 26 |

  **So the stop calms because 3 does** — its deficit and its weak
  strokes together are about 52 of 78 in the swell and about 7 of 37 on
  the floor — **while the common part stays where it is, about 20–26 in
  both**; the same at the floors before the canister (slot 2: `44` after
  its cut 19, `48` 30, `43` 24). ⚠ Not exactly additive (each step's
  dead band); the wheel's share moves from window to window (−1 to 12
  here; about 8 over 497 windows, *A steady pattern over the
  cylinders*). *Reasoned*: **the floor of about 37 is about 30 of wheel
  and common part with 3 nearly level** — so S1's mark of under 30
  (*When S1 closes*) needs the common part lower as well, not only 3
  mended.

**The swell's shape, and what the common part follows** (12/11 evening,
*the owner's questions*: what could make 3's waves — why the idle is
first rougher and then falls — and whether the common part moves with
anything; every standing idle of `24`–`49` in 30 s windows, 437 warm
ones loads off, each with 3's deficit, each cylinder's scatter about its
own median — **cylinder 2's taken as the common part**, the slot farthest
from 3's spill — and what the bus carries beside them: oil, coolant, b7,
b6, the injection time, the fuel counter, the lights, the brake, the
tank, the time into the stop, the seconds above 4,000 rpm before it;
the steps again in 8 s windows; **`tools/swellscan.py`, kept at the
owner's request** with its tests — `--series`, `--falls`, `--corr`; the
first reading was by scripts not kept, and the tool gives the same
figures).

*Cylinder 3's wave:*
- **It is a sawtooth.** 3's deficit grows by **1.5–3 % of a stroke a
  minute for 3–8 minutes**, to −21 to −28 %, and then falls to −1 to
  −8 % — three times at `32`'s last two stops, the last stop's two
  falls 6½ minutes apart (−11 → −23, −7 → −21, −6 → −19 at the
  capture's end), `47` −15 → −28,
  `49` −13 → −23, `31` −12 → −22 up to its cuts; **`50`, three times
  in one stop of fifteen minutes**: −12 → −24, −6 → −23, −5 → −24 at
  its end, growing by 3.3–4.3 % a minute, the two bottoms 5½ minutes
  apart (*The queue drive, and what the ECU sees through a swell*).
- **The fall is not a jolt: it takes 30–45 s**, some 200–300 of 3's
  strokes, at all five falls with no cut (`32` three, `47`, `49`; 8 s
  windows: `49` −22, −20, −15, −11, −13, −9, −6, −4; `47` −25, −22, −19
  held for 20 s, −13, −9, −7), twice in two stages; between a fifth
  and four fifths of the drop, 16–36 s (`swellscan.py --falls`). *This file said
  "in one step" and "what ends it is a jolt"*; the 20–40 s it gave for
  `49` was right, the word was not. **At `50` both falls were slower:
  108 s and about 80 s** between the same fifths (−24 to −5 and −24 to
  −5 in 8 s windows), each gradual, the last quarter of the second
  inside 8 s — so half a minute to nearly two.
- **Nothing on the bus shares the fall's time**: the coolant was rising
  at three and at its low or its peak at the others, so not the fan; b7
  rose by 5 a minute before two of them (`32`'s first, `47`) and not
  before the other three; engine speed, the injection time, the lights
  and the brake did not move. Within a stop 3's deficit correlates with
  none of them (|r| ≤ 0.06 for the coolant, b7, the injection time, the
  fuel counter, the lights, the brake; −0.18 with the oil); **only the
  seconds above 4,000 rpm in the fifteen minutes before, r −0.32** — the
  deficit is deeper after high revs, as *The rough start of a warm stop*
  found by stops.
- **Every stroke of 3's is weaker in the swell, not only the weak ones**:
  `49`, the raw step of 3's slot, the median −3.0 rpm in the swell and
  +0.5 on the floor, its ninth decile +2.5 against +4.5 — the whole
  distribution moves. Twelve weak strokes a minute of about 400 could
  not make 18 % by themselves.
- **A load masks it and does not end it**: `40`, −14 % before the A/C,
  −9 % at once with it, −13 and −14 % in the first minute after it and
  growing on to −22; the lights' load (b7 +5) took −15 to −10 while
  it lasted. A cut, by contrast, is usually followed by the floor
  (`44`, `43`, `31`'s second; not `31`'s first).
- **Straight after the fall 3 is nearly level**, −1 to −5 % (`32`, `43`,
  `49`), and settles to −7 to −9 % within two minutes: the "floor" may
  be the wave's first stage as much as a fixed part.
- **What follows the fall differs**: it grows again at once on `32`
  (12/10), `40` (21/10), `43` (3/11) and **`50` (12/11 evening, twice,
  within 40 s of each bottom)**; it did not in `49`'s fourteen
  minutes (12/11 morning — the same day, the same canister and valve),
  in `44`'s 4½ after its cut, nor at any time at `46`'s
  stops the day of the clean.
- On `32`, as 3 came back, **4 fell to −11 and −12 %** (twice; the
  others' share of the mean's shift would be about −5); on `47` and
  `49` the three shared it evenly. 12/10 was before 4 went level warm.
- **The mean mixture does not move with it**: the injection time and
  the fuel counter are the same in the swell and on the floor (r 0.01
  within a stop), beside 001's and 033's regulation (*Every stroke
  named*, *The first captured stop on the canister*).

**Read** (*reasoned*; nothing here is measured inside the engine).
**What the shape rules out as the wave's cause** (not as the floor's):
**a quantity of air or fuel into 3** — a leak at its runner (H3), its
injector or its loom (H7, H4), purge gas going its way (H16): a
cylinder 18 % short through its mixture would be a fifth lean or rich
and move the loop's regulation by about 5 %, which read the same within
1 % at both stops where it was logged; **the spark** (H4), which a
load makes harder, not easier; and **a flake blown out or a valve
turning**, which would mend in a stroke, not in 250. **What it asks
for**: something in 3 that builds steadily at a closed throttle, costs
every stroke — a slower burn or charge lost, with the air and the fuel
as before — counts for less the moment the manifold pressure rises, and
clears itself in half a minute once it has grown to a certain size.
In the order they fit:
1. **A seat on 3 that fouls and burns itself clean** (H1 with H13; the
   exhaust seat or the inlet's, whose crust the port photos show broken
   on 3). At idle a film of soot and oil builds on a seat that already
   closes on a deposit; the leak grows, 3 keeps less charge and more
   burnt gas, every stroke weakens and the weakest fail; when the gap
   is large enough the flame through it burns the film off in a few
   hundred strokes and the seat closes on what is left. It fits the
   steady growth, the fall's half minute, 3 nearly level straight after
   it, the load (the same gap matters less at a larger charge), the
   mixture not moving, the gas curing the misfires and not the deficit,
   the clean taking the swell for a day, and S22's tick once per cycle.
   Weak points: nobody has seen it, and the cold compression is even.
2. **Liquid that gathers at 3's inlet valve and is drawn in at once** —
   oil down 3's inlet guide or from the breather, pulled hardest at the
   idle's vacuum (H18, for one valve). A trap that fills and empties is
   the commonest sawtooth there is; against, no blue smoke ever, the
   plugs dry, and a load should not lift it at once.
3. **Coolant into 3** (H20): steam dilutes without moving the mixture
   and the system's pressure is highest after a hot drive; but nothing
   in it fills and empties, and it grows again in a stop's fifteenth
   minute as in its first.
4. **The ECU's purge phases** (H16): the one thing known to run a slow
   ramp and a quick shut-off by the minute, and not on the bus. It
   would need the purge gas to go mostly into runner 3 and to be
   neither rich nor lean; the injection time gives no sign of it.
   Kept because its test is the cheapest.
A lifter is inside the first: one that sags shortens the overlap and
calms an idle, so it would have to be one that holds a valve off its
seat, with the same picture as a fouled seat (*general*).

**What would tell them apart** (*proposed 12/11 evening and agreed
with the owner the same evening*; `plan.md` 6p, 8o, item 9):
(a) **the phone's recording through a swell and its fall**, at the
tailpipe and above 3, beside a capture — a seat that leaks more makes
S22's once-per-cycle part grow with 3's deficit and drop with the fall;
the other three leave it as it is; (b) **N80's hose clamped for whole
warm stops**, captured — a swell with the hose shut ends the fourth;
(c) item 9 as planned: the CO₂ test for the third, the warm leak-down
with 3 twice for the first — ⚠ made with the engine stopped, so on
whatever state 3 was left in; a stop switched off in a swell (the
display above 75) is the one worth testing.
*(a)'s tailpipe half was done that evening at `50`'s stop: 3's pulse
grows and drops with the swell, which does not tell a seat from a
dilution (*The phone at the tailpipe through a swell and a
fall*); the cam cover is left.*

*The common part* (cylinder 2's scatter about its own median, rpm rms
of step):
- **It is the same at every warm idle since 24/9**: the stops' means by
  capture, loads off, **2.7–3.1** (ten captures of eight windows and
  more, sd 0.13, under 5 %) — on both MAFs, three sets of plugs and of
  leads, both maps, before and after the clean, the probes and the
  canister (`49` 3.0, `48` 3.1, `44` 2.8, `32` 2.8). A window's own
  spread is 11 %, of which 7 % is what 100 strokes give by chance.
- **It does not follow 3's wave**: 2.9 at −24 % as at −8 % (r 0.05).
- **Three things move it**: **a load** — the A/C 2.3, a fifth less;
  **the provider's gas** — 1.8, nearly two fifths less, the lowest
  measured; **temperature** — 3.5 under 60 °C of oil, a fifth more,
  falling to its warm level by about 85 °C.
- **Small**: the first 30 s of a stop a tenth higher (3.1); the
  coolant's peak, where the fan runs, a twentieth lower (2.74 at 99–100.5 °C
  against 2.90 at 95–97; r −0.41 within a stop, *The radiator fan's
  cycle*); between stops, more fuel at idle goes with more scatter
  (r +0.28 with the fuel counter, +0.24 with the injection time; within
  a stop none).
- **Nothing else**: the oil once warm, the time into the stop past its
  first half minute, the tank's level (14–51 l), the lights, the
  brake, the high revs before, the date.
- ⚠ Its size as combustion is not known: the gas's 1.8 is an upper
  bound on what the measurement adds by itself, so at least 2.3 of the
  2.9 is the engine's — some 7–10 % of a stroke's work from one stroke
  to the next.

**Read** (*reasoned*): **the common part is a constant of this engine
as it stands**, answering only to what every engine's stroke-to-stroke
scatter answers to — how full the charge is, how easily it burns, how
warm it is — and to no repair and no day. That is what **H0** predicts,
and what **a fixed fault on all four** would give as well (the belt a
tooth out, the cam's timing: more burnt gas kept at idle on every
cylinder, all the time). **It is not what a source that changes from
day to day gives**: a purge path leaking canister vapour by how loaded
the canister is (H16, *The owner's reading, 12/11*) would move the
common part between a gentle day and a brisk one, between the bypass
and the canister, and it stayed within 5 %; so with the probes and
their wiring (H11, H21: both probes changed, the same 3.0), the rail's
pressure after a hot drive (H7: the high revs before, nothing) and oil
past the seals after idling (H18: the time into the stop, nothing).
**No healthy AQY has been measured**, so whether 2.9 is this engine
type's or this engine's is what the list cannot yet say; **8i, the
belt's marks, was the one test in the plan that bore on it**; read
13/11, the crank's notch stood 30–60° from its groove by eye, not
settled, and the air at full throttle says not so far (the row A1), and **the belt's renewal (8q) is now the test**:
the common part by capture before and after it, as the new N80 will
show once more whether it moves at all.

**The queue drive, and what the ECU sees through a swell** (12/11
evening, `50`; `plan.md` 6q, done; *the owner's offer*: VCDS one group
at a time, three rows a second; `cylscan.py`, `swellscan.py --series
--falls`, the rest *ad-hoc scripts, not kept*). 19 km in 67 minutes
from a start at 39 °C of coolant, 16:21:37–17:28:14, the A/C off, the
everyday state; a queue that crawls more than it stands — **23 warm
standing idles of 10–58 s** between 16:35 and 17:07, 590 s together —
then **a stop of 14.8 minutes, 17:10:52–17:25:41**, slightly uphill,
oil 100–101 °C, no cut; the fault memory empty before, at the stop and
after; the engine lamp lit only before the start and after the engine
was off.
- **In the queue 3 sat in the middle**: −9.5 to −15 % at the ten idles
  of 25 s and more (mean −13), 3's weak strokes 15 per 1000 against 4,
  6 and 1 on 1, 4 and 2 (58 % of 102), `IdleHealth` 72 over them, the
  common part 2.85 — **with next to no high revs before** (0.7–2.4 s
  above 4,000 rpm in the quarter hour before each, up to 17:01). So a
  gentle crawl gives neither the floor (−5 to −8) nor the deep swell:
  the high revs before deepen it (r −0.32) and are not what makes it.
  A stop of under a minute cannot show the sawtooth; whether each
  short stop restarts the growth is not read.
- **The last stop: three swells, two falls, no settled floor.** After
  30 s above 4,000 rpm in the ten minutes before it, 3 went −12 → −24 %
  by 17:13:50, fell to −6 by 17:15:30 (108 s), grew at once to −23 by
  17:19:30, fell to −5 by 17:21:05 (about 80 s), and was at −24 again
  when the stop ended; `IdleHealth` 82–86 at the peaks, 36–48 at the
  bottoms. Where `49`'s floor that morning held fourteen minutes, here
  it held none — **the same canister, the same N80, the same day**, so
  what keeps a floor is not the purge hardware (H16).
- **003 alone through the first swell and fall** (17:12:46–17:17:23,
  3.34 rows a second, set by the clock: ⚠ below). **Mass air 3.06–3.12
  g/s at −17 to −25 %, 3.02–3.09 on the floor**, and it follows the
  throttle angle and b7 (r 0.90–0.99: the radiator fan's load, 3.14–3.20
  while it ran); with the throttle taken out, 3's deficit is worth
  0.002 g/s a per cent — **0.03 g/s, under 1 %, across the whole
  swell**; the injection time 35.3–35.8 against 34.7–35.3, about
  1.5 %. A whole cylinder cut raises the injection time by 14–16 %
  (`43`, `44`: 34.6 → 41.9, 37.7 → 44.1), so fifteen points of 3's
  deficit ask for about 2 % more charge if the governor makes the work
  up: **what is seen, 1–1.5 %, is that or a little less**. *Reasoned*:
  6q's test — air creeping up with the swell for a seat, level for a
  dilution — **does not separate them**: either way 3 gives less work
  and the governor adds the same air; and the air and the fuel into
  the engine do not move by more than the lost work asks, so nothing
  is being added or taken at the throttle's side. **The advance**
  averaged 1.4–4.4° BTDC in 20 s windows, scattered 1.3–2.4° within
  them, the same in the swell and on the floor (r +0.1 with 3's
  deficit).
- **The advance against the common part** (H8; 48 windows of 10 s,
  the stop's 27 and 21 from phase B's standing idles, 16:34:50–16:55:42):
  **the scatter of the advance in a window does not go with the common
  part in it, r +0.08**; it goes with the scatter of engine speed
  (r +0.75) — the governor answering. Only the row-to-row jitter of the
  advance leans to the common part (r +0.45), which a governor trimming
  the spark after each speed step gives as well as one causing them;
  at 3.3 rows a second against 26 strokes the order of the two cannot
  be read. **Not for H8, and not against it beyond what the constant
  common part already says.**
- **001 alone through the second swell, its fall and the regrowth**
  (17:19:06–17:23:09): **the regulation swings with a period of 1.5 s,
  4.6–5.5 % peak to peak, sd 1.2 %, the same at −23 %, through the
  fall, at −5 % and growing again** (means −0.4, −0.5, −0.3, +0.2);
  r +0.2 between its mean and 3's deficit over 52 windows with phase
  C's (16:56:42–17:10:46), +0.3 between its scatter and the common
  part. The third reading of the same thing (`44` 001, `49` 033), now
  with the swing itself resolved: **no mixture moving under all four
  shows in it** (H16, H11, H21). Its 1.5 s is near the 0.8 Hz swing
  the dips ride (*The dips ride a swing of the idle loop*).
- **014 at the stop's end** (17:24:09–17:25:33, with 004 and 055, 1.1
  rows a second), in the third swell at −17 to −24 %: **19 rises in
  84 s, 16 on 3, all 13 of the deep ones on 3** (S3). 014 alone
  (phase D) ran three seconds before the stop came; not read.
- **004**: the intake air was 39 °C at the start, 24–27 °C on the road
  by the tenth minute and **46.5 → 48 °C at the stop's fourteenth
  minute** — logged only in phase A and there, so not minute by
  minute. *Reasoned*: under a closed bonnet it can only have risen
  through the stop, and 3 swelled and fell three times in it, so the
  wave does not follow the intake air's temperature. The ECM's supply
  12.5–12.95 V at the stop, 13.2–13.7 on the road (H4: within 004's
  12.0–14.5).
- **A puff from the exhaust heard at about 17:20** (*owner*, at the
  tailpipe with 6p's phone): that minute is the second swell's peak,
  3 at −21 to −23 % with eight weak strokes in 20 s (S2). **6p's
  recordings are read in the next section**; the door on
  the bus for them: open 17:15:48–17:16:23, shut three times
  17:22:49–17:22:59, and 17:24:22–17:24:30.
- ⚠ **A log taken wholly at a standing idle does not set itself
  against the capture by engine speed**: 003's 760–800 rpm fitted five
  and a half minutes late as well as anywhere (`cylscan.align()`), and
  phase C's missed the 40 rpm bound. The session's driving logs give
  the capture's start as 16:19:07.5 to 0.05 s, twice; the standing
  logs were set by their header's clock from that and trimmed within
  5 s on engine speed (`vcds.md`). 014's log at the stop's end set
  itself to the same second.
- **Read** (*reasoned*): **as 6q's own reading had it for "nothing
  found"** — 3's swell stays inside cylinder 3 (the air, the spark and
  the mixture the ECU gives are the same through it), and the common
  part stays with H0 and the belt. New from this stop: the wave can
  run three times in a quarter of an hour with no floor between, a
  fall can take nearly two minutes, and a gentle hour does not empty
  it. The seat that fouls and burns clean (H1 with H13) still fits —
  a slower fall is a slower burn-off; a trap that fills and empties
  (H18 for one valve) fits a period of 5½ minutes at least as well.

**The phone at the tailpipe through a swell and a fall** (`plan.md`
6p's first half, done; recorded 12/11 evening at `50`'s last stop, read
that night in a cloud session; three recordings of the owner's phone,
243 s from 17:16:13, 148 s from 17:20:20 and 81 s from 17:22:57 — **not
kept in the repository**; *ad-hoc scripts, not kept*). The first and
the third set by the door's shut on the bus (17:16:23, and the last of
three at 17:22:59), the second by its file's time; then each trimmed on
the strokes themselves, below. They cover 3 growing from −11 to −23 %,
the second fall to −5 %, and the growth to −20 % after it.
- **Every firing is found on the recording.** The firing line (26.5 Hz,
  795–800 rpm, the capture's speed to the rpm) gives each firing's
  start; the sound's energy at 35–400 Hz in each firing, against the
  40 round it, is one pulse's strength. Set against the capture's step
  for the same stroke it correlates **−0.35, −0.68 and −0.34** on the
  three recordings, at one lag each and nothing a stroke either side
  (the two door-set recordings agree on the lag to 7 ms).
- **A weak stroke is a louder pulse**, by how weak: 3's strokes 12 rpm
  and more down **+15 to +22 %**, 6–12 down +15 to +20 %, 0–6 down +3
  to +9 %, above their median −8 to +3 %; the few weak strokes of 1, 4
  and 2 the same, +13 to +38 %. *Reasoned*: a charge that burns late is
  still burning when the exhaust valve opens and goes out with more
  pressure; a stroke's weakness on the bus and its pulse at the
  tailpipe are one event. **S1's dips and S2's sound are on one
  recording at last** (S2).
- **3's pulse grows with its deficit and drops with the fall — on its
  steady strokes too.** In 20 s windows, the pulse of 3's firing
  against the four's mean: **−1 % at −11 %, +5 % at −15 to −17 %, +11 %
  at −23 %** (the first recording); **+1 % at −15 %, −7 % at −5.5 %,
  back to +2 % at −15 %** (the second, through the fall and after);
  −1, +7 and +9 % at −17 to −20 % (the third's three windows). **r −0.95 and −0.99 with 3's
  deficit** within a recording (11 and 7 windows), −0.92 and −0.94 with
  every stroke 6 rpm and more down left out — about 0.9 % of pulse for
  each per cent of deficit. The other three give it back between
  them; the sound's level does not change (r −0.2, +0.1).
  Folded on the cycle (the second recording, the clean one), **the gain
  sits in about 105° of crank at the front of 3's pulse**, 1.2–1.7
  times the floor's, the same with every cycle that holds a weak stroke
  left out.
- **By 6p's rule as it was written** — growing with the swell and
  dropping at its fall is for the seat (H1 with H13), the same through
  both for what only dilutes — **this is for the seat. *Reasoned*, the
  rule does not hold**: every stroke that burns later sounds stronger
  at the tailpipe (the weak strokes above), and a charge diluted by
  oil, coolant or burnt gas burns later as surely as one that lost
  compression past a seat. A seat that leaked into the exhaust would
  rather be heard between the pulses, during 3's compression, and the
  gain is on the pulse. **What it does settle**: the swell is in 3's
  combustion on every stroke — graded, there on the steady strokes,
  gone with the fall — where the bus alone could not tell work lost in
  the cylinder from, say, friction; and it is not the microphone's
  place (two placings, one slope). ⚠ One microphone, a telephone's,
  through speech compression; which 105° of 3's event (blowdown or
  before) is not known — the lag was fitted, not measured.
- **The loudest pulse of the first recording, +77 % at 17:19:48.9**
  (3:37 into it), **came two firings after the deepest stroke of 3's
  in those four minutes, −27 rpm** — nearly a dead stroke; the three
  strokes of 20 rpm and more down average +7 % in their own pulse,
  +22 % in the next and +53 % in the one after. *Reasoned*: a whole
  misfire's charge going off in the exhaust — **the owner's puff of
  "about 17:20"** (S2: the symptom he knows, *owner*, 12/11 night;
  the pulse at 3:37 itself not confirmed by ear).

**How the weak strokes follow each other** (11/11, *the research*;
`dipshape.py`'s warm runs, each step against its cylinder's median,
`24`–`47` without `36`, `45`, `48`, 401,718 strokes, 2.65 % losing more
than 8 rpm). The chance of a weak stroke k strokes after a weak one,
against the base rate: **k = 1: 3.95 ×** (the pairs, above); **k = 2–6:
0.75–0.99 ×**, a lull of about one cycle; **k = 4, the same cylinder one
cycle later: 0.87 ×**; **k = 8, 12, 16, 20, 24, the same cylinder two to
six cycles later: 2.5, 2.1, 2.0, 2.0, 1.9 ×**, the strokes between them
1.0–1.5 ×. The same in 17 of the 20 captures with a warm idle read one by one
(k = 4 under k = 8; not in `25`, `35`, `38`, few weak strokes or the
gauge's).
*Read* (*reasoned*, against the published work on cyclic variability:
Daw, Finney, Wagner, ORNL): **a weak stroke
comes in a spell of seconds on one cylinder** — that cylinder is
weaker for a while, which a slowly changing seal, mixture or deposit on
it gives and a random failure of the spark does not — **and inside the
spell the stroke right after a weak one in the same cylinder is less
often weak**, about 2½ times less than the spell would give: what a
partial burn leaves behind (unburnt fuel and less burnt gas in the
residual) feeding the next cycle, the coupling published near the lean
and dilution limits. So **the weak cylinder sits at a mixture or
dilution limit, not at a spark limit** — weakly, since a missed spark
also leaves fuel behind. The lull at k = 2–6 on the other cylinders may
be the ECU's answer to the dip (*What comes before a dip*) or the
measure itself.

**Why the idle got worse** (19/10, *reasoned*; display readings, loads off or
lights only, warm): 50–61 on 12/10, ~54 on 15/10, 70–90 on 17/10, 80–90 on
18/10 afternoon, ~100 on 19/10; with every load on it has hardly moved (~40–50).
**The rise began about 16–17/10, with the cleaner and the hard driving**, not
with the episodes of 18/10 (`refuted.md` D10); it is worse only at a small charge; and `39`, the first
capture after them, has more of its weak strokes on cylinder 3 than any
capture before or since — 77 %, 3 at −17 to −23 % (`cylscan.py`, 12/11;
*this said "the dips more concentrated on the pair, top two 77 %" until
then*). **Not an adaptation**: 032 −3.1/+5.5 %, 055 −1.27 g/s,
both inside their history (19/10). The candidates: deposit loosened by the
cleaner and not yet burnt off (H13), and **a relief after the leads' re-seat
of 10–12/10 wearing off** (`refuted.md` C24, *The idle against every time the leads were
handled*). **It passed**: 67 on 21/10 (`40`), 54 on 27/10 (display), loads
off, warm.

### S2. An occasional puff from the exhaust

*Owner*, at idle, long-standing — before the exhaust work, the injectors and
the MAF. Much weaker than S14's bangs, and in the owner's reading the same
thing smaller: **a misfire's unburnt charge going off in the exhaust**. On
12/10 he heard the puffs **come with the dips** (by ear, not aligned with a
recording). It outlived the resealed joint behind the converter (S6, closed).
**Heard again 26/10** (*owner*), at the warming idle between the two EPR
flushes, on the fresh oil with what EPR was left in it, and recorded by
phone (48 s). Read from the sound (the exhaust note at twice the firing
rate, 65.7 Hz; idle about 990 rpm): **no single stroke stands out** —
of about 1600, none above 1.45× the median pulse — but **four moments,
at about 0:03, 0:12, 0:24 and 0:37, where the exhaust note weakens by
about 20 % and the speed dips about 15–20 rpm for half a second**
(averaged over 0.25 s, so the true dip is deeper), the size of an S1 dip.
**Whether those four are the puffs he hears is not yet confirmed**; if
they are, S2 and S1 are aligned on a recording for the first time.
**Heard again 9/11 night** (*owner*), standing at a warm idle with every
load off (coolant 92–96 °C, the reading before `plan.md` 8c's swap),
`IdleHealth` about 130 on the display; no capture, so not aligned.
**Heard 12/11 evening at about 17:20** (*owner*, at the tailpipe at
`50`'s last stop, 6p's phone beside it): **the first puff inside a
capture** — in the minute of cylinder 3's second swell at its deepest,
−21 to −23 % with eight weak strokes in 20 s (S1, *The queue drive,
and what the ECU sees through a swell*). "About" a minute is too wide
to name the stroke; the phone's recording, set by the door, can.
**Read that night** (S1, *The phone at the tailpipe through a swell
and a fall*): **every weak stroke on the bus is a louder pulse at the
tailpipe**, +15 to +22 % for a stroke 12 rpm down, so S1's dips and the
exhaust's sound are aligned stroke for stroke, as 26/10's recording
could not show; and **the loudest pulse of the four minutes, +77 % at
17:19:48.9 (3:37 into the first recording), came two firings after
cylinder 3's deepest stroke, −27 rpm** — the owner's reading of S2, a
misfire's charge going off in the exhaust, seen once. **The puff he
heard that evening was this symptom, the one he knows** (*owner*,
12/11 night); whether the pulse at 3:37 is the very one he heard he
has not said.

### S3. Misfires counted by the ECU at idle

**VCDS group 014**, 12–120 against VW's 0–5, on every drive since it was
first logged. No fault code is stored (the ECU stores P0300 only above 2 %
over 1000 revolutions, `vcds.md`); **it once did**: P0304 and P0172 in an
old scan of 5/2019 (`vehicle-history.md`).

**When S3 closes** (*the owner's decision*, 12/11): **no count at all —
014 at 0 at a warm idle in the everyday state, on three drives on
different days, after the adaptations have settled**, oil 95–100 °C,
the whole idle long; not one rise, on any cylinder. Strict, by his
choice: the counter steps in twelves, so zero is the only reading
inside VW's specification. *Until 12/11 this read "0 at a warm idle
with loads off for 3–5 minutes, on three sessions" (decided 20/10),
and for a few hours that day "and what it still counts no longer 3's".
It also asked for one session straight after a hard drive* (20/10),
dropped 23/10 at the owner's decision: what that rested
on, 014 counting only after the hard drive of 4/10, was an adaptation
completing rather than load (`refuted.md` C19).

- **Only at idle, and that is the car.** Detection sees a misfire more easily
  under load and switches off below about 20 % load (measured over every 014
  log). Driving with detection `aktivováno`, new counts start once per ~250
  samples, against several a minute standing. **But not never: on 27/10
  (6k's drive) two episodes on the road climbed 12 → 36 and 12 → 48**, at
  1900–2100 rpm and 25–26 % load, and four more counted 12 (once 24) at
  1160–1920 rpm and 25–30 % load, all just above the cut-off. **After the
  pedal was greased (27/10 evening, `vcds-pedal-drive-2-014-003-055.csv`)
  they went on with no tip-in at all**: five episodes of 12–36 at a steady
  2000–2200 rpm and 25 % load, throttle about 10°, while the jerk the owner
  had tied to them was gone (`refuted.md` D6) — so they are not the
  pedal's. With detection `deaktiv.` the field
  reads 13, 15, 16, 18 at each lift: **counted misfires after all**, one
  each, at a weight that grows with load and engine speed, caught in the
  sample where detection switches off (5/11, *What the number is*; this
  said "not steps of 12, so not misfires" until then). The C4 full-load lamp lit on
  this map, so detection under load was not off — **unless the remap dulled
  it** (H14 route 6).
- **The events are the S1 dips** (`tools/s3align.py`, eleven sessions,
  16/10): half of 014's rises sit on a dip in the 1.5 s before, against 22 %
  by chance; a third of the dips get a rise. Over minutes the two part:
  **whether it counts is decided by the load** (`refuted.md` C19; the
  learned idle air as the switch refuted 2/11), not by how rough the idle
  is. **The A/C switches it**
  (*owner*, 16/10): A/C on, 014 at zero for minutes with `IdleHealth` ~70; A/C
  off, it counts and the grade barely moves. *Partly the detector's own
  threshold, rising with load* (*What it counts*, below).
- **What the number is** (5/11, from all 50 014 logs, 31 aligned to the
  bus; `vcds.md`): **the misfires counted in the current window of 200
  crank revolutions, times a weight**, reset to zero at the window's end —
  about 15 s at idle. Between resets the revolutions integrated from the
  bus are k × 200 in 388 of 388 pairs (about 12 % for one pair by chance);
  with one cylinder dead the field peaks at 1,164–1,188 = 97–99 × 12,
  one missed combustion every two revolutions. The weight is **12 per
  misfire at idle below about 34 % load, 13 above**, more above
  2000 rpm. So **12 is one misfire in the last ~15 s**, the owner's usual
  12–48 one to four in 400 combustions (0.25–1 %), and P0300's 2 % per
  1000 revolutions a reading of about 96 window after window; the worst
  natural 1000 revolutions on record are 1.95 % (4/10). VW names the
  200-revolution window for this ECU (SSP 175, catalyst protection). Off
  (`deaktiv.`) the count and the window's revolutions both freeze; the
  first window starts about 5 s after the crank. **Off below a load that
  rises with speed** (about 20 % at idle, 22–25 % at 1400–3000 rpm,
  27–30 % above) and **while speed falls faster than about 100 rpm/s**; no
  temperature condition (it counts below 40 °C of coolant).
- **What it costs the converter** (6/11 night, *at the owner's
  question*; *reasoned*, the materials' figures *general*). A warm idle
  burns **1.06 l/h** (median over the warm idle of `40`, `42`, `43` on
  `tools/replay.py`; 0.97–1.16), about **8 mg of petrol per combustion**
  at 790 rpm. A misfired charge reaches the converter with its own air,
  so at most it burns there: a share *f* of combustions lost heats the
  exhaust by about **f × 2,500 K** (petrol's 43 MJ/kg over the 15.7 kg
  of a stoichiometric charge, over the gas's 1.1 kJ/kg K) — the same at idle
  and under load, because fuel and exhaust both scale. **This car's idle**:
  0.25–1 % as 014 reads it (above), **6–25 K**; every dip of 15 rpm and
  more taken as a whole misfire, about 1.3 %, **33 K**; the worst natural
  1000 revolutions on record, 1.95 %, **49 K** — against a converter
  that runs at a few hundred °C at idle and ages from about 900–1,000 °C
  (*general*). Cold, before light-off, the charge passes unburnt: an
  emission, not heat. **What does melt one** is a share in the tens of
  per cent held for minutes — one cylinder dead is 25 %, about 600 K —
  above all under load, where the converter already runs hot; the old
  converter's "chamber burned right through" (`vehicle-history.md`) is
  that kind of heat, which this idle cannot make. The injector cuts put
  no fuel in (the injector is off), so they cost the converter nothing.
  **Read**: the idle's misfires are not a converter risk; a cylinder
  dropping out under load (a stored P030x, the lamp flashing) is, and
  the standing items already stop for it (`plan.md`).
- **What it counts** (5/11, the same logs against the bus): **one stroke's
  loss against the one before**, not the dip's depth — a fitted threshold
  of about 19 rpm at 28 % load, **rising 0.33 rpm per % of load**, about
  0.2 s after the stroke; held out one capture at a time it ranks the
  counted strokes with an AUC of 0.85 (0.91 with load and the neighbouring
  strokes). **Isolated weak strokes are counted, clusters and sags mostly
  not** (91 % at a loss of 20 rpm, 10 % when the next stroke keeps
  losing). Two things follow (*reasoned*): **the A/C's silence is partly
  the detector's** — its load raises the threshold — though the grade
  falls with it too (S1); and **`42`'s zero after the map and the reset
  was the detector's state, not the engine** — the bus predicts 55–80
  counting windows there and 014 showed none, which fits the threshold
  Bosch's patents raise until the crank wheel's tooth errors are learnt
  (`refuted.md` C19). **Open**: on `41`'s cold cut (oil 63 °C, 35 % load)
  only about 10 % of the dead strokes were counted, against 87–100 % on
  the warm cuts, though the bus shows the same −25 rpm dead stroke; a warm
  cut with the A/C on would tell load from temperature.
- **Every warm stop with 014 beside the bus, as a share of
  combustions** (9/11, after the clean; the window's counts summed over
  every warm standing stretch of 150 s and more, oil ≥ 90 °C, detection
  on, cuts left out; *ad-hoc script, not kept*): `24` 0.63 %, `28`
  0.60, `31` 0.26, `32` 0.28, `37` 0.20, `39` 0.47, `40` 0.11, 0.46
  and 0.16, `43` 0.12 (after its cut); **`44` (stop 3, before the
  clean) 1.03 up to the cut — the highest on record — then 0.02**, the
  provider's wait with the A/C 0.00; **`46` (stop 7, after it) 0.12
  and 0.14**. Load 22–31 % throughout. **Stop 7 sits with the lowest
  of the settled stops**; stop 3's settled half lower still. **During
  the clean 014 was off** (load about 19 % at 1,750–2,150 rpm), and at
  idle with the gas flowing too (21–23 %). One stop each side: 014's
  storm at the start of stop 3 and its absence at stop 7 are S1's rough
  start on 3 and its absence (S1, *The clean of 9/11*). **10/11, VCDS
  alone, the warm stop after the drive on both new probes** (H11, *The
  reading after the swap*): **0.24 %** — twelve misfires in about 3
  minutes at 32–35 % load, the windows' counts summed the same way —
  between the settled stops, no lower for the probes. **10/11 evening,
  the relearn drive** (`47`, the battery off for hours before it; H11,
  *The relearn drive*): **counting from 16:33, twelve minutes after the
  start** — so not quiet after a disconnect this time; the queue stops
  16:51–17:17 (shorter than 150 s, so summed per stop) **0–0.58 %, 0.24 %
  over them**, the stop at the end **0.15 %** at 25–26 % load, with the
  rear probe reading zero (S23). **12/11, `49`, the first captured stop
  on the canister** (S1, *The first captured stop on the canister*):
  **0.69 %** over its first four minutes (0.46–1.05 % a minute), 3's
  swell, then **0.01 %** — one count in thirteen minutes — on 3's
  floor, at 29–33 % load throughout; on the road five counts of one at
  2,240–3,240 rpm; no code stored.
- **What 014 counts, by cylinder** (12/11, the third research;
  `tools/cylscan.py --vcds`, kept). The ECU has no per-cylinder counter
  (`vcds.md`), but the bus names the stroke: each rise of 014 between
  two samples at a standing idle, recognition on, is put to the cylinder
  of the weakest stroke in the interval before it (the rise shows about
  0.2 s after its stroke; the log set against the capture on engine
  speed to 0.05 s; cuts left out). **1,135 rises** in 27 logs beside 16
  captures:

  | | rises | 1 | 3 | 4 | 2 |
  |---|---|---|---|---|---|
  | `24`–`39` (24/9–18/10) | 840 | 26 | **544 (65 %)** | 252 (30 %) | 18 |
  | of them `31`, `32` (10–12/10, the NGK leads) | 329 | 13 | 162 | 146 | 7 |
  | `40`–`47` (21/10–10/11, the VW leads) | 295 | 13 | **237 (80 %)** | 40 (14 %) | 5 |
  | of them `41` (cold, oil 52–63 °C) | 49 | 3 | 36 | 8 | 2 |
  | `43` (3/11) | 31 | 1 | 29 | 0 | 1 |
  | `44` (9/11, stop 3's storm and the stops before) | 78 | 5 | 63 | 9 | 1 |
  | `46` (9/11, after the clean) | 25 | 2 | 7 | **16** | 0 |
  | `47` (10/11 evening) | 37 | 1 | 35 | 0 | 1 |
  | `49` (12/11, the canister; after the count above) | 41 | 0 | **37** | 3 | 1 |
  | `50` (12/11 evening, the last 84 s of the queue drive's stop; after the count above) | 19 | 1 | **16** | 1 | 1 |

  Where the weakest stroke is at least 12 rpm under its median — the
  name is surest there — 3 has 63 % and 4 34 % of 580 up to 18/10, **3
  has 82 % and 4 15 % of 197 since**; 1 and 2 together 3 %. **So 014's
  count at idle is cylinder 3's misfires, with 4's beside them until
  the leads of 10–21/10** — on the NGK leads 4 had as many as 3 — and
  **1 and 2 are next to never counted**. The ECU's own name agrees:
  P0303 on 18/10, after `43`'s cut and on 12/11. `46` is the one
  capture where 4 leads, at stop 7 after the clean and round its cut on
  4. **How deep a stroke is counted** (the same rises; warm, 16,000
  sample intervals): at 20–28 % load a stroke 20 rpm and more under its
  median is counted about two times in three, 17–20 rpm one in two,
  14–17 one in three, 11–14 one in seven; at 31–36 % load one in three
  at best — the threshold that rises with load (*What it counts*).
  *Reasoned*: a count of 12 is a real, nearly whole misfire of one
  cylinder (a dead stroke reads 24–33 rpm in its own slot at a cut's
  first stroke), not the idle's general unevenness; **S3 closes when
  cylinder 3 stops misfiring**.
  **Against chance, 12/11 night** (asked for by the session before,
  `git show c2e9e19:handoff/README.md`): the
  weakest stroke of any few strokes is cylinder 3's more often than one
  time in four, because 3 has most of the weak strokes — so the split
  is to be set against the same pick with no rise, not against 25 %.
  The same pick in the windows 5 s before and 5 s after each rise
  (`cylscan.misfires_014()` with the log shifted; the 24 driving logs
  that line up, their standing idles): **since the VW leads 83 % of
  286 rises on 3 against 50 % of 558 control windows, 1 and 2 together
  5 % against 28 %**; up to 18/10 62 % on 3 against 45 %, 4 34 %
  against 31 %, 1 and 2 4 % against 23 %. Where the stroke is 12 rpm
  and more down: 84 % against 73 % since, 60 % against 53 % before.
  **So the names stand — a rise is next to never 1's or 2's — but 3's
  lead over chance is 83 to 50, not 80 to 25**, and 4's share before
  the VW leads is hardly above what its own weak strokes give by
  chance. **Off idle** (*Naming the cylinder*, *Off idle*): 014 counts
  while crawling as it does standing, and next to never under load.
- **Three properties to keep in mind** (`refuted.md` A11, A12): steps of 12;
  off below ~20 % load; its sensitivity per dip moved five- to fiftyfold with
  the MAF. **So 014 is a yes/no witness, not a ruler.** Compare across time
  with engine speed or `IdleHealth`.
- **An estimate of it on the display since 4/11** (*the owner's request*;
  `docs/firmware/can-decoding.md` question 11, *Misfires*): `Misfires` on 0x604, the dips
  of 20 rpm in the last minute of standing idle. Over every capture with a
  014 log, warm, **no minute in which 014 counted read zero on it**, and
  with the A/C on (`40`) it read zero 79 % of the time as 014 does; per
  single event it misses most of 014's counts, and it does not count
  driving. Zero there reads "014 most likely silent"; VCDS decides.
  **The first readings after a warm-up, 5/11** (display, the A/C on at
  every stop; two short drives, perhaps never fully warm, not revved
  above 3500 rpm, *owner*; S1's table): **2 and 5–10**; **the drive home
  the same evening** (an hour of queues, the A/C and the blower on 2,
  oil 100 °C): **1–22** over the drive, **3–4** at the end with
  `IdleHealth` 51–54, falling as the engine warmed
  (*owner*); cold 18–23. **6/11**, after 5/11's contact cleaner and
  straightened gasket edge (40 minutes with queues, the A/C and the
  blower on 2, oil 98 °C): **18** at the end with `IdleHealth` 65,
  MisfAvg **23.0**, about twice to three times 5/11's 7.4–11.6 — but
  **only about 5 minutes of idle in the whole drive, hardly any of it
  warm** (*owner*), so the start's mean is mostly the cold part and the
  last minute of idle is few warm seconds; **the engine behaved the
  same** (*owner*, the album). **The drive home the same day** (the A/C
  off, the blower on 1, oil 90 °C): **6** with `IdleHealth` 73, MisfAvg
  **8.6**, back to 5/11's level (*owner*, the album). **8/11** (the
  everyday state, oil 97 °C, about a minute): **9–12**, MisfAvg 12.5
  (*owner*). ⚠ **Not the capture's near-zero with the A/C**
  (`40`: zero 79 % of the time, 0.2 a minute) — that was read on minutes
  with the compressor's load in b7 (b7 ≥ 36), and the display cannot tell
  whether the compressor was running; in November it may cycle or stay
  off. A capture with the A/C on would say which.
- **Session A, 3/10**, and **Session A after step 1b, 4/10**: the first warm
  stops ever with 014 at zero — on fresh adaptations — then counting again
  after five minutes of hard driving. **Session B, 4/10**: counting again,
  055's learned value at −1.0 to −1.2. **Steps 2b and 2c, 9/10**: the first
  session on kept adaptations, counting at every stop. Read together then
  as the learned idle air (C19); **refuted 2/11**: 27/10 counted on fresh
  idle air, and 4/10 A's quiet is the exception.
- **The drive after the new leads, 10/10** (`31`): 014 at about 9/10's
  rates — better hot, worse cold, no direction. The leads did not fix S3.
- **The new regulator hose, 25/10** (`plan.md` 6i, 6j): on 6i 014 counted
  loads off at 80 °C of oil and read 0 loads on; **a drive later, at
  96 °C of oil in the everyday state, it counted at 12 ten times in
  4.7 minutes, 24 and 36 near the end**, and 0 through a 34 s stop at a
  light (`idle-log.md`). The hose did not fix S3.
- **How far an episode climbs** (25/10): the counter's floor is 12, so
  how often it counts says less than whether an episode stops at 12 or
  climbs to 24, 36 and more. Warm idles, coolant ≥ 88 °C: **6j 2 of 16
  episodes climbed (12 %)**, 6i 2 of 9; 12/10 25 of 47, 15/10 10 of 31
  and 12 of 41, 18/10 24 of 37, 21/10 8 of 20. 6j against the four
  before the hose, pooled: one-sided p ≈ 0.06, episodes of one stop not
  independent, and 6j in the everyday state. **How often it counts did
  not change** — about two episodes a minute, as 15/10 and 21/10. The
  hose and the second 44K tank (24/10) cannot be told apart here.
- **014 against `IdleHealth`, re-read in stretches** (25/10,
  `tools/s3align.py --windows`; `docs/firmware/can-decoding.md` question 11, *Re-read in
  stretches*): **no `IdleHealth` below which 014 is silent at an
  ordinary load** on settled adaptations — a plateau to about 80, more
  above. On fresh adaptations (to 4/10) it did fall silent below about
  70, and loads on (014's load above 28 %) silence it at any grade.
- **The original map, 3/11** (`42`, fresh adaptations; the three VCDS
  logs `vcds-step5a-*`): **014 never left 0** — 2,563 `aktivováno`
  samples at idle and on the road, 1,071 of them at idle, and none
  of 1,388 above 1500 rpm against 15 in about 4,300 on the remap. **Two
  things stop it reading as S3 closed.** The idle load sat at **30 %**
  (p10–p90 27.7–32.4, the everyday state), against 26.5–29.3 % on the
  settled remap sessions, which is near the 28 % above which loads
  silence it; but 6k (28.5 %) and 6l (28.9–29.3 %) counted at about
  2–3 per 100 samples. And 4/10 A on fresh adaptations was quiet too,
  the one exception C19 found. A map that set the detection differently
  (H14 route 6) would read the same, **and the tuner's files say it did
  not**: the detection was not touched (H14; `refuted.md` C23).
  Read again on 5b at a similar load; S3's closing mark is loads off.
- **The second drive on the original map, 3/11 evening** (`43`,
  `vcds-step5b-*`, 032 relearnt part of the way): **014 counts again**
  (*owner*, and the logs agree). At the town stops before the warm one,
  5 rises in 174 idle samples at 30.8 % load (p10–p90 28.5–43.3) — the
  settled remap's 2–3 per 100 at `42`'s load, so **`42`'s zero was the
  fresh adaptations, as 4/10 A**, not the load (*reasoned*, one
  session). At the warm stop, loads off, 26.5 % load (25.7–28.1), oil
  99 °C: **10 episodes in 200 s before the cut, 9 of them climbing past
  12** (to 24–48), the highest share read (*How far an episode climbs*);
  4 in the 80 s after it; then **zero for the last 2 minutes** to engine
  off, at 25.7 %, while `IdleHealth` read 48 (S1). Two minutes, one day:
  not S3's mark. **In the cut** the field climbed by 72 every sample, 12
  for each of cylinder 4's missing combustions (`vcds.md`).
- **The clearing of 24/10 reset 032 to 0.0 / 0.0 and left 055 at −1.31
  g/s** (`idle-log.md`), read once: on this ECU the clearing did not
  restart the learned idle air that C19 then tied 014 to, so 6i and 6j
  count on settled idle air. Whether it restarts the crank-wheel adaptation is
  not known (`vcds.md`).
- **P0300 and P0303 stored on a drive with no cut, 12/11 night**
  (`vcds/vcds-step8n-drive-faults-after.txt`, both 35-00, neither
  sporadic; the memory empty at the start, 00:58): **the first P0303
  without an injector cut since 18/10** (`refuted.md` D10). The engine
  lamp not seen lit or flashing (*owner*). The drive: 52 minutes, a
  brisk motorway stretch, **the limiter touched once** (6,280 rpm,
  about 01:37 by 001) and "a few times" by the owner's account; the day
  before, driven the same way on the new rear probe and the oily G62,
  stored neither. 014 was not in the drive's log, so **when it was set is
  not known**. At the warm stop after it (`vcds-step8n-stop-014-001-036.csv`,
  7.7 minutes, 25–26.5 % load) **014 rose by 12 six times**, about once
  a minute or two. *Reasoned*: whether this ECU counts the limiter's
  cut as misfire is not known; a code on 3 fits H1 and H13 as 3's
  deficit and 014's rises do. Cleared by the owner after the stop, 032/055 read
  first.

### S4. Knock retard on cylinder 4 — near the limiter on 2 beside it — and 4 a little short under load

*The heading said "and only cylinder 4" until 12/11* (*the owner*: the
captured drive's 020 changes the symptom, not only its data; *Since
12/11, below*); **widened 12/11 night** (*the owner's decision*: an
extension of S4, not a new symptom) by what 4 gives under load, read
off the bus (*What cylinder 4 gives under load*, below). Groups 022/023 and 020: cylinders 1–3 read zero in almost every sample;
cylinder 4 retards in steps up to 13.5 °CA, mostly on a tip-in after a coast
or gearchange and on hard pulls, **never at idle**. Within VW's 0–15 °CA while
driving. 9/10: still cylinder 4 alone with all injectors seated (`refuted.md`
B7); 10/10, the first drive on new leads: almost none (3 samples); 12/10:
back, smaller, on a harder drive. **On the VW leads** (21/10, `40`):
in 40 % of 020's full-load samples above 3000 rpm, mean 2.5 °CA over
them all, to 11.2, and cylinder 1 in 12 % (to 9.0). **On the original map** (3/11,
`vcds-step5a-pulls-014-003-020.csv`, five pulls to the limiter at
92–106 °C of oil): **cylinder 4 alone in 41 %**, mean 1.1 °CA, **to 6.0**,
at 5000–5500 rpm, retarding and walking back in 0.75° steps; cylinders 2
and 3 once, together with 4, to 3.0 at 6000 rpm; 1 never. **The second
drive** (3/11 evening, `vcds-step5b-pull-014-003-020.csv`, two pulls in
4th to 5,760 rpm at 91–97 °C of oil, short of air, H14): **cylinder 4
alone in 37 %** of 60 full-load samples above 3000 rpm, mean 0.8 °CA,
to 4.5 at 4,700–5,640 rpm; 1–3 never. So as often on
both maps and about half as far on the original: **not the map's** —
less depth fits a milder full-load advance, but 003 reads the same
advance at full load on both (H14). **The captured warm drive, 12/11**
(`vcds-step6w-drive-014-020-033-2.csv`, the original map, five pulls
to 6,000–6,320 rpm and full load at 3,500–4,600 rpm, oil about
100 °C): **cylinder 4 in 47 %** of 335 samples above 3000 rpm at 80 %
load and over, mean 2.2 °CA, **to 12.7 there and to 14.2 on a tip-in
at 3,920 rpm and 16 % load** (11:10:01) — inside VW's 15 — **most of
it at 3,500–4,600 rpm** (54 of 156 full-load samples there, 9–13°),
where the drives of 3/11 had 1 of 40; at the limiter 1.5–6°. **And
cylinder 2 in 14 %** (to 6.0, every one at 5,300–6,300 rpm and with
4), 1 in 4 % (to 5.2), 3 in 2 % (to 3.0), all at the limiter. The
owner read 15–17 on the screen (*owner*); the log's highest is 14.2,
so the screen's figure fell between the logged samples or on another
field (not known). **Not the band alone**: 3/11's two drives had 40
full-load samples at 3,500–4,600 rpm and 4 retarded in one, this drive
54 of 156 — **on the original map 4 now retards there as on the remap**
(`40`: to 11.2); 2 beside 4 near the limiter is new in these logs.
**The symptom changed with it** (*the owner*, 12/11; the heading and
*Since 12/11*, below). *Reasoned*: an arc at lead 4's plug end is
broadband noise in 4's own window (`refuted.md` C24), as is real knock from the crust on
4's crown (`idle-log.md`, 19–20/10).

**Since 12/11: by speed, and cylinder 2 beside 4** (every 020 log
with 014's speed and load beside it; full load = 014 at 80 % and over;
the share of samples in which each cylinder retards, and its most):

| log | 3,000–4,700 rpm | 4,700–5,300 rpm | above 5,300 rpm |
|---|---|---|---|
| 12/10 (`vcds-step3-1-drive-*`, NGK leads) | 4 41 %, to 11.2; 1 8 % | 4 in all 4 | 4 in all 4 |
| 21/10 (`40`, the remap) | **4 31 %, to 11.2; 1 17 %, to 11.2** | 4 40 %; 1 10 % | 4 11 %; 1 22 % (9 samples) |
| 3/11 (`vcds-step5a-*`, the original map) | none in 15 | 4 47 %, to 6.0 | 4 45 %; **2 9 %, 3 7 %, to 3.0** |
| 3/11 evening (`vcds-step5b-*`) | 4 1 of 57 | 4 46 %, to 4.5 | 4 93 %, to 3.0 |
| **12/11** (`vcds-step6w-*-2`) | **4 29 %, to 12.7**; 1 1 % | 4 53 %, to 12.7 | **4 84 %, to 7.5; 2 57 %, to 6.0**; 1 and 3 9 % |

- **2 retards only above 5,300 rpm and never without 4** (0 of 43
  samples on its own); 1 and 3 there in one sample in eleven. On 3/11's
  pulls to the same speeds 2 was in 9 %. So at the limiter all four
  retard a little on 12/11, 4 and 2 the most — **and 2 is the strongest
  cylinder at a warm idle** (S1, *Every stroke named*: +3 to +10 % of a
  stroke, the steadiest), which is what makes it odd (*the owner*).
- **Not odd for knock itself** (*reasoned*, the physics *general*):
  knock comes where the cylinder's pressure and the end gas's heat are
  highest; a cylinder that fills and burns best — 2 at idle — makes the
  highest peak pressure at full load too, so the strongest cylinder is
  the first after 4 to knock. A cylinder that gives least (3) is the
  least likely, and 3 retards least. **Odd for a fault in 4's window**:
  a noise booked to 4 alone (H5) does not put retard on 2, unless the
  noise at 6,000 rpm is long enough to reach the next window (2 fires
  180° after 4, 5 ms at 6,000 rpm) or one sender hears both — which
  sender serves which cylinder is not recorded here.
- **4 deeper in the middle band than on 3/11** (29 % to 12.7 against
  none in 15 and 1 in 57), as on the remap, where the advance at
  3,500 rpm is the same on both maps (H14, *The drive on the original map, 3/11*: 19.5° on both).
  **What differs from 3/11**, none measured against it: the hydrogen
  clean (9/11), the battery disconnect and the clears since (H6), and
  **about a tenth of Orlen Efecta 95 in the tank since 8/11**
  (`vehicle-history.md`); the November air is colder, which goes the
  other way (*general*).

- **Not the rev limiter** (12/11, *the owner's question*: with the
  throttle wide open, the ECU could hold the speed down only by
  retarding). Three things say no: **2's retard starts at 5,300–5,500
  rpm while the engine is still climbing freely** — on the pulls of
  11:00:43 and 11:08:41 the speed rose 5,750 → 6,300 and 5,900 → 6,350
  at a steady 80–89 µl of fuel per revolution until the driver lifted
  (`49`, 0x280 and 0x480 in half-second steps), so nothing was being
  held; **020 is knock control's retard, cylinder by cylinder** (`vcds.md`),
  in the 0.75° steps it walks back in, with 4 at 3.0 while 2 is at 6.0
  in the same sample — a limit on speed would act on all four alike and
  belong to the base advance (003), not to this group; and **the limiter
  sits at about 6,300 rpm** (12/11 night, 6,280), which these pulls
  reached for half a second at most. How this ECU limits speed is not in
  its documentation here; Motronic of the time usually cuts injection
  (*general*), and with a cable throttle that is what it has besides the
  spark.

**What cylinder 4 gives under load, from the bus** (12/11 night;
`tools/drivescan.py`; *Naming the cylinder*, *Off idle*): **4 gives
2–4 % of a stroke less than 1** — the two cylinders the crank wheel
reads alike — from 1,600 rpm up, at every load from part to full, on
sixteen drives, `19`–`50`: +1.2 to +2.5 % at 2,100–3,300 rpm
and full load, +2.6 to +3.2 at 3,300–4,200, +3.8 to +4.4 at
4,200–5,200 (±0.2 to ±0.8). **It is there at part load too** (+2.6 to
+3.5 % at 1,600–2,600 rpm, b7 about 62), where 020 reads no retard, so
the retard is not all of it; where 4 does retard, a few degrees cost
about this much (*general*). At idle 1 less 4 is +5 % since the VW
leads and was +10 % before. **Part of S4** (*the owner*, 12/11 night).

**Why 4, and why the other way round from 3** (*the owner's question*,
12/11 night; *reasoned*, nothing here measured beyond what is cited).
**It is not the other way round**: 4 is a few per cent under 1 in
every state — 5 % at idle, 2–4 % under load, a share; 3 has something
on top of that only where the charge is small, an amount. Two
different things, not one cause with two signs. **For 4, three
readings**:
- **Real knock from the crust on 4's crown** (H13): retard costs
  torque, so 4 is short where it retards. Against it as the whole:
  4 is as short at part load, where 020 reads no retard; 3 has more
  deposit than 4 and retards least; and the clean of 9/11 was followed
  by more retard, not less.
- **4 fills or burns a few per cent less at every load** — the crust
  round the inlet seat's edge on 4 (the port photos of 20/10), runner
  4's torn gasket edge, or less lift at one of its valves. A share, as
  measured. On its own it would make 4 the *least* likely to knock, so
  it does not explain the retard.
- **Something mechanical at 4 that does both** — a valve, lifter or
  cam lobe on 4 that lifts short and is heard: less filling at every
  load (the share), **a noise in 4's window with no load at all** (S5:
  026 reads 4 20–70 % over 1 in neutral, which knock cannot be) that
  the ECU books as knock (H5), and a tick once per cycle (S22, on a
  cylinder no recording has named). **The one reading that takes S4's
  retard, S5 and the 2–4 % together**, and it is H5 with a part named.
  Against: 2 beside 4 near the limiter (above) is not explained by it.
**What would tell**: the stethoscope on the cam cover above each
cylinder, hot, and VW's tappet check (`plan.md` 9, there for 3) —
**listened to and checked on 4 as well**; 026 in neutral again after
any work on 4's valve gear.

**What it changes in the hypotheses** (12/11, at the owner's request;
*reasoned*; **no fit-table symbol changes**, each said why):
- **H5** (something in 4's window that is not combustion): ✔ stays —
  4 alone below 5,300 rpm, as always; **weakened at the top**, where 2
  beside 4 points to combustion or a noise heard in more than one
  window.
- **H13** (deposits): ~ stays. The crust on 4's crown (the borescope)
  is a reason for 4 to knock; **2's crown has a thin layer only**, so
  not for 2; and a clean that took deposit away (9/11) was followed by
  more retard on 4, not less — weakly against H13's form for S4.
- **H14** (the remap): ~ stays. **The middle band is not the remap's**
  — 4 retards there on the original map as on the remap, at the same
  advance; above 5,300 rpm, where the remap did differ, `40` has too
  few samples to compare.
- **H6** (knock control relearning after a disconnect): fits that S4
  changes between logs; 3/11 was the day of the flash and 12/11 two
  days after the disconnect, both on young adaptations — not telling.
- **H4 / H21's shared earth** (S4, S5 through a common sender earth):
  noise there would reach all four windows, which the small retard on
  1 and 3 at the limiter allows; ~ as it was.
- **H1, H3** (3's valve, runner 3): nothing — 3 retards least.
- **The idle's ranking is untouched**: S4 is outside it (*owner's
  decision*, 9/10) and its column moved no symbol.

### S5. Cylinder 4 reads high in group 026 (knock sensor voltage)

With no load at all, standing in neutral, cylinder 4 reads 20–70 % above
cylinder 1 from about 1400–2700 rpm up; above ~3350 rpm the excess moves to
cylinder 1. So **not knock** — knock needs cylinder pressure. At idle all four
sit on the floor. 1 and 4 reading twice 2 and 3 is explained without a fault
(`refuted.md` B2). ⚠ 026 includes the ECU's amplifier factor, and 1 and 4 are
probably on different sensors.

### S11. A hiss at the back of the engine at a warm idle

*Owner*, from 26/9. It outlived the new breather and cover gasket. Closed
12/10 and **reopened 14/10** (*owner*): heard again, roughly **on the right
side, near the throttle or the hose from the MAF to it**, only with his head
by the hoses. Moving the hose and covering places by hand changed nothing.
**His own reading: it may be normal** — idle air past the nearly shut plate
under manifold vacuum (*general*). Kept open with that note; no test planned.
If it is a leak: behind the throttle it is H3, ahead of the probe H2.

### S12. A sudden jerk at a crawl and on moving off

*Reopened 10/11 night at the owner's request*, in a new form; its
history, closed twice as play (4/10) and as a sticking pedal (27/10), is
`refuted.md` D6. **Now** (*owner*): **now and then, creeping gently, the
car gives one hard jerk, as if someone had let go of the throttle
abruptly; and the same when moving off. Not every time. Not the
pedal**, which has moved smoothly since it was greased (27/10).

**Looked for on `47`** (10/11 evening, about 40 moving-offs and long
crawls in the queues; *ad-hoc scripts, not kept*): **nothing that can be
named a jerk**, and none of the times is known. (1) Engine speed at a
steady pedal: every fall of 60 rpm and more in 0.3 s at under 25 km/h
lies at a gearchange or a lift (the pedal at rest, b7 falling), a
clutch the bus cannot see. (2) The car's own speed: 0x1A0 below about
10 km/h moves in steps held for tenths of a second, so its derivative
makes false decelerations of 1–2 m/s² at every step; at the candidate
moments engine speed showed no stumble. **The bus cannot show this
symptom at a crawl** (*reasoned*). (3) **014 counted at moving off**:
seven single misfires on the road (12–18, `aktivováno`) at 43–57 % load
— 16:34:33, 16:46:01, 16:47:35, **17:15:52** (0–8 km/h, 757–1,114 rpm in
the 15 s before), **17:19:30** (0–6 km/h), 17:23:02, 17:26:00 — and
**each window held a moving-off from standstill**; a misfire under load
in first gear is a torque step the driver feels (*reasoned*). Whether
he felt one then is *not known*.

**To catch it**: say "teď" (now) in the chat the moment it happens on a
captured drive, or note the clock; a capture with a word at the time
names the stroke, the load and the cylinder.

### S14. Bangs from the exhaust on a downshift without a blip

*Owner*, 4/10: on a downshift **without a throttle blip** a series of small
bangs, 1–2 s after the clutch comes up; with a blip almost never; warm. Gone
9–14/10, **back on 15/10, quieter** (*owner*), with the joint behind the
converter tight — so that joint fed or carried it at most. **28/10**:
on every downshift without a blip, **no more often than before, only more
muffled since the joint was sealed** (*owner*). Read as
(*reasoned*): the engine dragged up on a shut throttle is fuelled at its
thinnest charge; a charge that fails to fire goes out as fuel and air and
burns when the fuel cut pumps plain air in after it — **a misfire where 014
is blind**. The ECU cuts the injectors 0.8–1.6 s after the lift
(`coastscan.py`). **The owner's to watch, not in `plan.md`** (*owner's
decision*, 4/10): worked on only if it outlives S1/S3.

**Does it keep to cylinder 3, as the idle's dips do?** (6/11, *at the
owner's request*; every coast with a fuel cut in the `_z1` captures,
655, `tools/coastscan.py`'s windows; *an ad-hoc script, not kept*.)
**It could not be named then**: a cylinder was named only by phase
carried from an injector cut at idle, and on the road the phase was not
kept that far. *Since 12/11 `cylscan.py --wheel` carries one stroke
count from an overrun into the standing idle after it (13 overruns),
which could name the fuelled strokes of such a coast; not read — S14 is
the owner's to watch.* **What the bus does show**: with the pedal up,
the strokes still fuelled before the cut (from 0.7 s after the lift)
have the same mean stroke-to-stroke step as the cut ones at the same
speed — the car, not combustion, holds the crank's speed in gear — but
**more large steps**: the 95th percentile 13–16 rpm against 9–14 at
1200–2600 rpm. So the thin charge on the overrun burns unevenly enough
to be seen, the mechanism S14 is read by (*reasoned*; the ECU's own
torque reduction before the cut would look the same, not ruled out).
**Not on one cylinder**: in the 20 fuelled stretches with the phase
intact and three or more large steps, the top slot holds 45 % of them
against 49 % by chance (p 0.9). No sign that S14 shares the idle's
cylinder; nor can it be excluded, with so few strokes per coast.

### S16. A tick in neutral, cold, with the clutch pedal up

*Owner*, 12/10: a regular tick at a cold idle in neutral, **gone with the
pedal down** — the gearbox side. **Not pursued** (*owner's decision*): the
idle graded the same pedal up and down (H12). Out of the fit tables.
**A link not looked at before** (6/11, *general*, *reasoned*): rattle
from a gearbox in neutral with the clutch engaged is excited by the
crank's unevenness at idle, so the tick could be S1 heard through the
gearbox rather than a fault of its own. Untested; the owner's ear would
say it: does the tick follow the felt dips, and does it fade with the
A/C on, when the idle is calmer (S1)?

### S17. A new exhaust sound, from a new place

*Owner*, 15/10: only at about 2200 rpm, **like a resonance**, perhaps the
remade joint behind the converter, perhaps nearer the engine. A sound tied to
one engine speed is a part vibrating, not a leak (*general*), so it bears on
no hypothesis about the idle. Out of the fit tables until placed.

**31/10: taken for the sheet-metal heat shields around the exhaust**
(*owner*: "that is it"), **and still heard after their new clips** the
same day (*owner*), so not them, or not only them; *this said "placed"
until then*. They rattled at certain engine speeds; held
once before with nuts over the old clips, a stopgap that did not hold,
so the resonance stayed (*owner*; when not given). **The shields were
loose before the new clips; the joint behind the converter checked and
"held as if nailed"** (*owner*, 31/10), so not the joint. **New clips
fitted 31/10** (`vehicle-history.md`). **Where it is now** (*owner*):
perhaps nearer the engine, where a lot else resonates, so hard to say.
**Looked over from below again, the engine included** (*owner*, 31/10):
nothing moves anywhere; a few sheets bent a little, just in case, without
much faith. He may try to locate it with a second person at the
throttle. Unplaced again, and not pursued. A candidate there (*reasoned*): the
manifold's own heat shield, which cannot be seen (`plan.md` 7) — a part
vibrating, not a leak, so still no bearing on the idle.
**The same band in 014 on the road** (6/11, *at the owner's request
for new links*; every VCDS log with group 014, detection on, above
1100 rpm and at 32 % load or less, increases within 20 s taken as one
episode; *an ad-hoc script, not kept*): **2000–2400 rpm, 35 episodes in
24 minutes (1.45 a minute), against 13 in 21 minutes (0.63) at
1600–1800 and 2400–2600** — about 2.3 times, p about 0.005 for so many
by chance, the band chosen from S17 beforehand; spread over 16 logs,
not one drive. **What does not follow it**: the bus's stroke-to-stroke
roughness at steady throttle on the road (second difference of the
180° speed, 1300–3200 rpm, every `_z1` capture) rises smoothly with
speed, with no peak at 2200; and S5's excess on cylinder 4 begins
about 2000 rpm but keeps growing to 3200 (`vcds-neutral-026-003.csv`
and its clamp log), no peak either. **Read** (*reasoned*): a candidate,
not a link — a crank-synchronous vibration there could feed both the
knock sensor's window and the misfire detector, or the detector's own
thresholds may simply be lowest there. **A test without new kit**: hold
2200 rpm on the road in two gears, VCDS on 014, and say in the chat
when the resonance is heard; counts that follow the engine speed and
the sound, not the gear, would make it one thing.

### S19. P0172 stored, too rich — with one start that died at once

**16556 / P0172, bank 1 too rich, 35-00, not marked sporadic** (P1240 beside it was), found in the fault memory before
the cold capture on the night of 24/10 (`idle-log.md`), **the first since
5/2019** (`vehicle-history.md`), and set some time after the last empty
reading. The same window holds **the one bad start of that afternoon**:
after about 4 hours parked nose uphill the engine caught and died at once,
the next start normal (`idle-log.md`, 24/10). **The two are suspected to be
one event** (*owner's decision*, 24/10): a flooded start reads the same to
the driver as a starved one, and an injector or regulator that lets fuel
into a cylinder while the car stands would give both (*reasoned*). The
trims behind it were lost to the clearing before 032 was read
(`CLAUDE.md`). Also in the
window: the first tank of Orlen Verva 100 and two 170 km drives held at
5000 rpm. **It cannot be dated more closely** (28/10): this ECU's fault
memory carries a code and its status only, no mileage, time or freeze
frame (`photos/vcds-faults-2026-10-26-after-flush2.jpg`), so the window is
everything between the empty reading of 23/10 and the night of 24/10 —
and it **opens before the fill**, with the drive out on the old tank (OMV
and the first 44K) run down to 0.4–0.7 l. Before the window nothing points
at it: 032 −3.1 to −6.3 % (19–23/10), the live regulation at a warm idle
centred on 0 with no excursion past −5.5 % (21/10, VCDS 001). **What sets it is not
known**: VW's manual gives 032 a range of −10 to +10 % (`vcds.md`), which
is the specification, not the code's condition, and the label file holds
none. **It is not the idle cell reaching −10 as VCDS shows it**: on 25/10
night, with the regulator's hose off, the idle cell went to **−12.5 %**
for about 40 s (`vcds/vcds-step6e-cold-2-001-032-033.csv`) and the fault
memory was empty afterwards. The part-load cell is positive, the other way,
and has been on every reading since the new MAF (24/9): +1.6 to +5.5 %
up to 23/10, +6.3 to +8.6 % since 25/10. *This said "since 25/10", which
held only for the higher values (the owner, 28/10).*

**Not settled that the start set it** (*reasoned*): a start that dies at
once runs on a cold probe, open loop, and cannot itself trip a trim fault;
what would link the two is **one cause** that puts in too much fuel, seen
once at the start and once later in closed loop. **Read by what followed:**
032's idle trim well negative at the next reading, or P0172 back with no bad
start, says a standing cause rather than a one-off — **and the idle trim
has been −7.8 to −8.6 % on every settled reading since (25–27/10)**,
while P0172 has not come back: a standing cause, below the code's
threshold; P0172 back after
fills only would point at the purge path (*general*: a canister flooded by a
brim-full fill), which 070 found sound on 27/9 (`refuted.md` A6) but not
since — and 070 shows that the valve opens, not that it seals (H16).
The 001 of 24/10 night, with the stored adaptation still in force, read
**+15 to +22 %** while warming and about **−3 to +1 %** warm — adding fuel
cold, near zero warm, which a hard rich fault would not show; weak, since
it is the trim on top of an adaptation not read. **The misfires make it
stronger, not weaker** (*reasoned*, as `refuted.md` A7): an unburnt charge
carries oxygen to the probe and reads lean, so with 014 counting the
mixture is if anything richer than the trims say. And **it all but rules
out a meaningful intake leak** (A7): that would have pushed the other
way.

**The new probes, 10/11** (H11, *The reading after the swap*, *The
relearn after the battery disconnect*): **−7.8 / +7.0 → −6.3 / +5.5 %
over one drive** on kept adaptations — the split narrowed by about
three points — **then both cells reset by the owner's battery
disconnect after parking**. Where the idle cell goes from zero on the
new probes was the test of whether the old front probe made it
(`plan.md` 8d): on the old probes it was back at −6.3 % after one drive
from every reset — and on the new ones too (below, *On the new probes,
from zero*).

**S7 closed 31/10 as the fuel** (`refuted.md` D2), and S19's start of
24/10 was one of its starts, hours after the Verva fill. **What it
leaves here** (*reasoned*): if the start and the code were one event,
the fuel is the first candidate for the code too — a fuel that
evaporates more readily, through N80's small leak (H16), gives a rich
idle cell and floods a start alike, and a fuel with less energy per
litre raises the part-load cell alone; how Verva 100 and OMV MaxxMotion
100 differ in either is not known. Against: S19's window opens before
the fill, on the drive out on the old tank. **Read by 032 on the OMV
tank**: the idle cell back towards the −0.8 to −3.1 % of before the
Verva says the fuel; still at −6 to −9 % says a standing cause (H7's
injector, H19's MAF). The map of 3/11 reset 032, so it was read before
it. **31/10, on OMV** (album; warm, coolant 95 °C, oil 75 °C, after a
drive): **032 −7.8 / +7.0 %, 055 −1.17 g/s at 790 rpm, load bits
`0000`** — the idle cell where it sat on the Verva (−7.8 to −8.6 since
25/10), the part-load cell inside its +5.5 to +8.6, the idle air level
with 27/10's relearnt −1.17; "the adaptations hardly moved" (*owner*).
The lines have held OMV since 30/10 afternoon, more than a day of
driving. **Read** (*reasoned*): 032 relearnt from 0.0 to about −6 to
−8 % within a day after the clearing of 24/10 (S3, *The clearing of
24/10*), so a day on a fuel that caused the split would have moved it
by now; it did not. **Against the fuel as S19's cause**, and so against
the start and the code being one event — S7 was the fuel, the split was
not. What is left for the split: H7's injector and H19's MAF against the
map, which 3/11 read (below). **About 81 km on OMV** (the cluster's trip
81.2 km, `TripDist` 82.3 km, *owner*); **the fault memory empty**, so
P0172 not back.
**On the original map, 3/11** (reset to 0.0 / 0.0 with it,
`vcds-step5a-end-adaptations-032-055.csv`, after the 58 min drive home,
warm): **032 −6.3 / +3.1 %**, 055 −1.04 g/s; the fault memory empty
before and after. **The idle cell relearnt to −6.3 within one drive**,
as it did within a day after 24/10's clearing: **not the map's**, which
leaves H7's injector; H19's MAF against the map went with the files
(`refuted.md` C22). The part-load cell
at +3.1 is below the remap's +5.5 to +8.6 % and inside the +1.6 to
+5.5 % before 25/10; one drive is not settled, so it was read again on
5b (below). **The remap took about 5 % of fuel away from 1400 rpm and heavy
part load up (H14, T1)**, which the loop would learn back into this
cell: **the part-load cell settling at about +1 to +3 % on the original
map would confirm it**, and the rest of the split as the new MAF's.
**After the second drive** (3/11 evening,
`vcds-step5b-adaptations-032-055.csv`, before the owner cleared the
cut's codes): **−6.3 / +3.9 %** — the idle cell held, the part-load
cell up 0.8, not yet settled; the clearing restarts both. **Read 3/11
night, at the owner's question** (*reasoned*): **not a conclusion yet**.
The cell was still climbing when the clearing reset it, and +3.9 sits
inside what the remap itself read up to 23/10 (+1.6 to +5.5), so it
cannot yet tell the map from what moved it to +6.3–8.6 from 25/10 (the
regulator's hose, the tanks). It is already above the +1 to +3 that
would have confirmed T1 as the cause, which leans against T1 doing it
alone. **The settled reading, 6/11** (`photos/vcds-adaptations-2026-11-06.jpg`,
warm, read before the owner cleared S21's P0440): **032 −7.0 / +6.3 %**,
055 **−1.24 g/s** at 790 rpm, load bits `0000`. The idle cell where it
has sat since 25/10; **the part-load cell back at +6.3, inside the
remap's +5.5 to +8.6** after three days on the original map. **Read**
(*reasoned*): **the part-load cell is not the map's either** — T1's fuel
did not make it, and the whole split outlived the map; what moved it to
+6.3–8.6 from 25/10 is left with the idle cell's cause (H7's injector,
H16). P0172 not back; P0440 instead (S21). The clearing restarts both
cells. *This said "a settled reading is the next 032 … no session for
it" until 6/11.*
**On the new probes, from zero** (10/11 evening, the relearn drive after
the battery disconnect; `vcds/vcds-step8d-drive-014-032-036-2.csv`;
H11, *The relearn drive*): **the part-load cell moved first** — +3.9 %
five minutes into the drive, +6.3 % by 16:46, **+7.0 %** from 17:24 —
and **the idle cell followed it to −6.3 % within 37 minutes**, held
there for about ten, then **−3.9 to −4.7 %** to the end: **−3.9 / +7.0
%** at the stop, 055 **−0.91 g/s**. **The split came back on new probes
in one drive**, as on the old ones after both resets, so **neither cell
is the old probes'** (H11's mark 1). P0172 not back; P0137 instead,
the new rear probe's (S23), cleared by the owner — which resets 032
again (S3, *The clearing of 24/10*), so the next VCDS reading starts
from a fresh relearn.
**On the canister, from zero** (11/11 night, the first drive with the
canister back, 8k, `idle-log.md` 11/11 night; S21, *The first drive on the canister*):
**−3.9 / +2.3 %** at the end, **−3.1 / +2.3** after the long warm
stop, 055 −1.04 g/s — **the part-load cell a third of the bypass's**,
the idle cell bent towards zero by S23. P0172 not back. **12/11 night**
(the old rear probe): −5.5 / +2.3. **12/11, the captured drive**
(`49`; reset by the clear after 12/11 night, then a 40-minute MFD drive
that morning): **−14.8 / +2.3 % before** — the idle cell past VW's
−10 with no code, a shift of S21 and H16 and not a new symptom (*the
owner*, 12/11) — and **−7.0 / +8.6 after** the brisk drive, 055 −0.84
→ −0.98 g/s: **the part-load cell back at the bypass's level and
above** (H16, *Read 12/11, the captured stop*). P0172 not back.

### S20. Engine speed wanders at a constant pedal

*Added 26/10 at the owner's request.* **During the first EPR flush**
(26/10, `idle-log.md`), standing in neutral, the pedal held by a stick of wood:
the speed swung a little at first, held about 1250, then rose slowly to
about 1300 by itself, and **"it just fluctuates"** (*owner*). **His
9 s video** of it, read from its sound (the firing rate in the clicks
above 3 kHz, 1 s windows): **1266–1294 rpm for 4 s, then a step down to
1215–1241** for the rest, ±10–15 rpm within each. **Over the flush**
(*owner*, off the display): mostly swinging **1250–1300**, now and then
settling at about **1230**; **the stick does not move at all**. **A 3-minute
recording** at about minute 22–25 of the flush, read the same way (1 s
windows): median **1260**, mostly 1240–1290, swinging 10–20 rpm over
seconds; **once a lower, calmer stretch of about 28 s at 1195–1222**,
entered by a drop of about 45 rpm within 2 s and left by a rise, and
one shorter dip to about 1205. **Two states, then: lower and calm,
higher and swinging** — the video's 1266–1294 → 1215–1241 the same
pattern. What switches between them is not known; an on/off load such as
the radiator fan, or the purge valve's cycles (H16), would give a step at
a held plate (*reasoned*); the sound shows no fan switching clearly.
**The flush's part is weak since** (*owner*, 26/10, in the second
flush): setting the stick so that it did not move turned out hard, and
the swing may have been the stick after all; set again, it sits at
1250–1300. **And the ECU was in it** (*reasoned*): **P0507** set in the
first flush and **055's learnt value went to −2.10 g/s**, so the ECU took
the held engine for an idle running high and worked its idle control
against it; with the plate near its stop, a controller pushing against a
held pedal could itself give a speed that swings and steps. **So S20
rests on the road observation**, not on the flush.
**Also on the road**
(*owner*): hard to hold the engine speed steady, **noticed since the job
of 1–2/10**, which fitted **the new throttle** (Pierburg `7.03703.13.0`)
and **took up the throttle cable's slack** (`idle-log.md`, *1–2/10 — the valve
cover, throttle and breather job*); the same job renewed the cover gasket, the
plenum gasket and the breather.

**Not S1.** S1 is dips at idle with the idle governor in charge; this is
above idle with the pedal held. **The pedal works the throttle by a
cable** (*owner*, 26/10, off the car; *this said the pedal was a sensor
and the ECU moved the throttle — wrong*), so with the pedal held the plate
is held, and what wanders is the engine's torque at that plate, or the
plate itself through the cable and the idle stop. ⚠ **Soft**: it was
seen with EPR, a solvent, in the oil. The stick is not it (*owner*: it
does not move).

**The captures show no change with the new throttle at part throttle**
(26/10). Every stretch of at least 2 s with 0x280 b5 not moving by one
count, above 15 km/h, in one gear, oil above 80 °C; the rpm's scatter
about its straight-line trend in each: **1500–2500 rpm, part throttle,
5.3 rpm on the old throttle (`19`, `24`, 84 stretches) against 4.1 on
the new (`26`–`40`, 137)**; 2500–3500 4.3 against 4.2. Only full
throttle above 3500 rpm reads higher on the new, 9.0 against 5.9 — pulls,
far more and harder after 2/10, not a held speed. ⚠ What this cannot
see: a wander slower than a few seconds, which on the road the gradient
hides, and a standing hold above idle, which no capture since 2/10
holds. *An ad-hoc script, not kept.* A capture tells them apart:
0x280 b5 is the throttle, so stretches where it holds still show whether
the speed wanders anyway.
The slow rise to 1300 reads as the oil thinned by EPR and still warming,
less friction at the same throttle (*reasoned*); the swings and the step
do not.

**Since 27/10 the cable is slackened and the pedal greased** (S12 closed
on the pedal, `refuted.md` D6): a pedal that stuck in small jumps near the
start of its travel holds a plate unsteadily too, so S20 may have been
the pedal. **It outlived them, a little better** (*owner*, 28/10): the
pedal was part of it at most.

**The first capture since the pedal, 3/11** (`42`, the original map; *the
owner's question*). **With the plate held** (0x280 b5 within ±2 counts
for 6 s and more, part throttle, above 40 km/h): the speed's scatter
about its trend **0.14 km/h**, engine speed 0.19 %, against 0.16 / 0.31
on the old throttle (`19`) and 0.12–0.17 / 0.23–0.26 on the new
(`31`, `37`, `40`) — **a held plate holds the car, on every throttle**.
**How still the plate is held** at a cruise (5 s windows, 50–130 km/h):
the plate's spread **2.8 counts** on `42`, against **3.2–3.5 on the old
throttle** (`19`, `24`) and **5.5–8.1 on most drives with the new one
before the pedal was greased** (`30`, `31`, `32`, `37`, `40`; `39` 3.5,
`26` 1.2 with few windows). **Read** (*reasoned*): S20 lives in the
pedal, the cable and the plate, not in the engine — the engine holds a
held plate steady — and since 27/10 the plate is held as still as on
the old throttle, which fits "a little better". ⚠ `42` is mostly
motorway, where a foot holds still more easily than in town; one drive.
The map does not reach this range (H14).

### S21. P0440 stored and the engine lamp lit — the evaporative system

*Added 6/11 at the owner's request.* **On the drive home of 6/11 the
engine lamp came on, steady**, the first time in years; oil at 90 °C,
the idle "relatively OK" (*owner*). **The fault memory read that
evening** (`photos/vcds-faults-2026-11-06.jpg`): one code, **16824 /
P0440, evaporative emission system, 35-10, malfunction, sporadic**. 032
and 055 were read before the owner cleared it by hand
(`photos/vcds-adaptations-2026-11-06.jpg`; S19). **The same code as
1/2018** (`vehicle-history.md`, *Fault memory*), never repaired and not
stored on any reading since, until now.

**What was ruled out at once** (*owner*, 6/11): **no fill on 5/11 or
6/11**, so not a filler cap left loose after a fill; **the hoses around
N80 not touched** in 5/11's work at the injector connectors and the
gasket's edge (`idle-log.md`).

**What sets it is not known.** These files hold no description of how
this ECU checks the system; block 070 opens N80 and reads the lambda
(`refuted.md` A6), but whether the ECU runs a check of its own while
driving, and what fails it, is not in `vcds.md`. The fault memory keeps
no freeze frame (S19), so when in the drive it was stored is known only
by the lamp. **A steady lamp** is the ECU flagging an emissions fault,
not the flashing misfire lamp of the standing items (*general*);
**sporadic** says the fault was not present when it was read (*general*,
VCDS's status). The ordinary causes of P0440 are N80 sticking or not
sealing, a cracked or loose hose, the canister, and the filler cap
(*general*).

**Read with H16** (*reasoned*): N80 passed "really little" air at rest
on 25/10, and P0440 of 2018 was already that hypothesis's history; the
code back is the first sign of the evaporative system that is a fault
code and not an inference from the trims. **Not the idle**: the same
drive, at a warm stop, read `IdleHealth` **73**, `Misfires` **6**,
MisfAvg **8.6** (S1; the A/C off, the blower on 1), in the range of the
days before. **Read by what follows**: the code back after the clearing
says a standing fault, not back says a one-off; the fault memory is read
on 9/11 anyway (`plan.md` 8). **Read 9/11 at every phase: no P0440**,
only the cut's codes (`vcds/vcds-step8-faults.txt`).

**Read 11/11, with P0172 and every recent code** (*the owner's
question*: one cause, or only the car driven more? the research of
11/11; scripts not kept). **Of eleven codes since August three came by
themselves** — P0303 (18/10), P0172 (23–24/10), P0440 (6/11); P0411 and
P0137 follow found faults (the torn secondary-air hose, the rear
probe's harness), the rest were provoked (cuts, a hose pulled, the
stick on the pedal). **The car is driven far more**: about 75 km a day
since 23/10 against 2–14 km a day in every year since 2018; the one
period like it, 9/2017–2/2018 (about 68 km a day), holds the first
P0440. *Reasoned*: the purge check runs at every warm idle, so a system
near its threshold shows a sporadic code more often the more the car is
driven — **it explains P0440 coming back well, P0172 less** (5/2019 came
in a year of little use). **How the check works** (VW's manual for the
2.0 in the Golf IV; Bosch patents US5243853, US5604305): with no leak
detection pump it is a flow check — at a warm idle without load N80 is
opened and the lambda correction and the idle air watched; too little
answer is the fault, and a load on the idle weakens the answer. **One
part fits both codes**: VW's fault table for this engine names N80
under 16556 and 16824 alike, and a valve that leaks a little while
closed would feed vapour the idle trim takes up (rich) and leave
little to answer when opened (P0440) (*reasoned*). **Against or not
shown**: the canister cut off on 25/10 left the idle cell as it was
(*the tank's line, in truth: the canister was found bypassed 11/11*)
(cold only); out of the car N80 hardly passed air — by mouth, about 0.1–
0.19 bar at most against 0.6–0.7 bar of vacuum across it at idle, so
weak; P0440 not back on 9/11; and neither explains the positive
part-load cell. **Separate causes fit as well**: P0172 from the
regulator's cracked vacuum hose found in its window, P0440 from N80, its
line or the canister's vent. **The car's own data**: no step in 032 at
any fill (none larger than one VCDS step); live 001 at a warm idle
−1.6 to +0.6 % in every session; the warm idle's fuel flow on 0x480 no
different with the tank full or low beyond about 3 %; both codes of 2026
in the bottom third of a tank (two cases). **The one odd record is 24/10
night** (`41`, P0172 still stored, its adaptation in force): +20.5 %
while warming, against −2.6 to +6.2 % in nine other cold sessions — the
stored cell was taking away fuel the engine no longer needed, so
P0172's rich source was passing and gone at a cold idle, when nothing
is purged. The test left is `plan.md` 8a's: 032 before and after the
new one (the old valve under the gauge declined 11/11, *the owner*).
⚠ 0x288 b2 bit 5 (*not looked into* in `docs/firmware/can-decoding.md`)
is set in the captures with the lamp lit and clear in `41` with P0172
stored — perhaps the ECU's lamp request; not decoded, nothing rests on
it.
**The canister itself** (*the owner's question*, 11/11; *reasoned*,
*general*): never replaced, so its charcoal is the original. A canister
that holds less with age gives less to purge, so the ECU's check sees
a smaller answer when it opens N80 — **P0440 without a faulty valve**,
likelier in the cold when the tank gives little vapour (both P0440s,
1/2018 and 6/11, came in winter) — **but it would not give P0172**,
which a canister flooded with liquid would (rich purge, and granules
into N80). Its signs: a fuel smell near it when the tank is warm,
granules rattling or in its hoses (none on 6/11, `idle-log.md`), a
crack, a vent blocked by dirt or a stone. Looked at and blown through before N80 is changed
(`plan.md` 8j, 11/11); replaced only if P0440 comes back with the new valve.
**The tank under pressure at the filler cap** (*owner*, 11/11, from
past summers): in summer, a hot one above all, **every time the fuel
filler cap is opened the tank lets out an overpressure, clearly more
than a faint psst** — pressure, not a vacuum; whether his other cars
do it he is not sure. *General*: a sealed tank that breathes only
through the canister builds some pressure in heat, and a short puff is
common; whether this car has a valve that holds a pressure on purpose
is not in these files. *Reasoned*: a strong one says the tank's path
to the canister passes vapour too slowly — the valve at the tank or
the filler neck, or the line kinked or blocked — so the canister gets
less to purge and the ECU's check a smaller answer (fits P0440);
against, both P0440s came in winter, when there is little vapour
anyway, and it would not give P0172. A vacuum would have named the
canister's vent; it is not that. Not N80 (H16), which sits after the
canister. Heard with the old cap; the new one (about early 10/2026) has
not met a summer. Tested in `plan.md` 8j: the tank's line off at the
canister before the cap is opened, and how it takes air.
*Explained the same evening by the finding below.*

**11/11 evening: the canister is not in the circuit** (*owner*, at the
car, the right rear wheel arch, the liner off; the album, 17:02–17:27).
**The line from the tank is joined straight to the line to N80**: the
thick cream hose from the valve at the top of the filler neck (white
body, black rubber top, *owner*) goes into a black rubber elbow, held by
a worm clamp, and on into the thin cream line printed `1C0 201 …` that
runs forward to the engine; **the canister's port on top stands open,
nothing on it**, a small hole beside it (the album, 17:18:22). The owner
sees only two ports on it. **When and by whom not known** — not done in
his time by his own account, so an earlier owner's, perhaps when the
tank was replaced (`vehicle-history.md`; *reasoned*), perhaps for a
leaking canister, as the fuel filter was once only taped (*owner*).
Dried white runs down the canister's side; what they are, not known.
Its number, read off it out of the car: **`1HM 201 801 B`** on its end,
the housing `171 201 813` (the album, 18:06–18:23); no longer sold
under that number by the owner's search. **Out of the car** (*owner*,
the borescope): nothing rattles; inside the ports a plastic grid and
spring plate, whole and dry to the eye. **Sound**: the line across its
top is **a seam from manufacture**, not a crack — two halves joined,
as the owner reads it off the part (a parting line or a weld) — cleaned and
photographed close (the album, 18:55), it runs straight on along both
ports and through the moulding's gate mark; and **with both top ports
closed nothing passes when blown in at the vent** (*owner*). Both ports
whole, the small one a barbed nipple. *For about an hour this said "its
top is cracked across, the small port broken short", from an end-on
photograph; the owner doubted it and the close-ups settled it.*
**What it means** (*reasoned*, from how
the system works, *general*): the tank's vapour reaches N80 **with no
charcoal and no opening to the air** between. So **the tank is sealed
whenever N80 is closed** — the summer overpressure at the cap above —
and **each time N80 opens, the intake draws raw tank vapour**, rich
when the fuel is warm and hardly anything when it is cold, instead of
air drawn through the charcoal. That fits **P0440 in winter** (both
of them: the check opens N80 and little answers), and it **takes back
"it would not give P0172"** above: in warm weather each purge is
straight vapour the trim has to take away. The negative idle cell
(S19) is a candidate for it only warm — 25/10's test, which closed the
line at N80, was cold (H16, *corrected*). **The test is the repair**:
the canister plumbed back (`plan.md` 8j), then 032 and item 6's warm
stops against the readings before.
**The same evening, the parts around it** (*owner*): the line to the
engine free (passes with N80 off it; with N80 on, nothing — the valve
seals closed, as on 6/11). **The valve at the top of the filler neck,
VW `1C0 201 756`** (the album, 17:45:43): **by mouth nothing passes
either way unless it is moved**. What it is, is not in these files; a
valve there is commonly a gravity or roll-over valve, open upright and
closing when tilted or flooded (*general*) — held in the hand it may
simply have been tilted. **If it is closed upright**, it seals the tank
on its own and starves the purge whatever the canister: the summer
overpressure and P0440 both, a second time over (*reasoned*). Its test:
blown through held exactly as fitted (`plan.md` 8j). **Done 11/11
evening** (*owner*; the number read clear, the album 18:31:11): **held as it
sits on the car it passes; upside down nothing passes either way unless
it is shaken** (*owner*). A gravity or roll-over valve, working: closed
when inverted or flooded, so that liquid fuel cannot reach the canister
(its neighbours in VW's numbering, `… 201 751`/`752`, are sold as
gravity valves, *general*). **Not the cause**: the summer overpressure is
the bypass alone. *This said "stuck" for a quarter of an hour: the first
test had held it upside down.* **The canister blown through** (*owner*,
11/11): in at either top port, out at the other; with that one closed,
out at the vent at the bottom, a little harder — **it passes everywhere**.
Why it was bypassed is not known: the canister shows no fault; the
owner's guesses — at the same time as the leaking fuel filter was
taped, or a cracked rubber piece at one port joined straight across
rather than replaced (11/11) — cannot be checked.

**The first drive on the canister, 11/11 night** (8k, `idle-log.md` 11/11 night; 032
logged over 65 minutes, `vcds/vcds-step8k-*`): 032 read **−7.0 /
+7.0 %** before it (21:17, the bypass's last value), was reset by the
clear of P0137, and **relearnt from zero to −3.9 / +2.3 % by the end
of the drive, −3.1 / +2.3 after the long warm stop** (22:49;
`vcds-step8k-end-adaptations-032-055.csv`) — against **−6.3 / +6.3
within 37 minutes and −3.9 / +7.0 at the end** on 10/11's relearn,
with the bypass. **Read** (*reasoned*): **the part-load cell is the
reading** — it learnt +3.9 early, touched +6.3 once, and sat at +2.3
for the last half hour, where it held +6.3 to +7.0 with the bypass;
part load is where the purge flows, and S23's second loop (S23, *Does
the rear probe touch the mixture*) would push it up, not down. **The
idle cell is not clean**: P0137 stored on this drive and the rear
probe at zero at the stop after it (036 was not logged on the road),
which pulls the idle cell towards zero as on 10/11. **The second
drive, 12/11 night, on the old rear probe** (healthy, no P0137;
`vcds/vcds-step8n-*`), relearnt from zero again to **−5.5 / +2.3 %**:
**the part-load cell +2.3 on both drives — the canister's**; the idle
cell back near the bypass's −6 to −7, **so the idle side was S23's and
the canister did not move it**.
**The third and fourth drives, 12/11** (032 reset by the clear after
the second): a 40-minute MFD drive that morning, then the captured
brisk drive (`49`, `vcds/vcds-step6w-*`): **−14.8 / +2.3 % after the
first, −7.0 / +8.6 after the second**, 055 −0.84 → −0.98 g/s, no code.
**The part-load cell is not the canister's after all**: +2.3 on three
drives, +8.6 after the fourth, with its five full-throttle pulls
(*reasoned*: the cell learns where the
drive spends its part load, and a purge gas that changes with how hot
and how full the canister is moves it with the drive; H16, *Read 12/11,
the captured stop*). The owner's reading: the canister emptied by the
brisk drive (*owner*, 12/11; *reasoned*, not measured).

### S22. A tick once per engine cycle — reopened 11/11 night

*Added 9/11 at the owner's request, closed that evening as the hydrogen
clean's own sound (`refuted.md` D11, which keeps the entry as it stood:
the recordings, the burst pattern, the read), **reopened 11/11 night at
the owner's decision**.* **Heard again warm with no clean**: on 10/11 at
an idle loads off, and **on 11/11 night at the warm stop after a hard
motorway run** (oil 102 °C, the everyday state, bonnet down, from the
driver's seat), **"the same pattern, or nearly, only quieter" than
during the clean** (*owner*); recorded at the engine bay (the album,
11/11 21:55), read 12/11 (below). *This said "not yet read" until then.*

**Read** (*reasoned*): with no oxyhydrogen in the charge, D11's
explanation — the clean's faster burn making a usual difference louder
— does not reach it; what stays is D11's own list: **one valve's lifter
(H1), one injector (H7), one cylinder's port leaking at its joint
(H2), or one cylinder's combustion different from the others** (S1, *A
steady pattern over the cylinders*). Louder during the clean fits a
part whose tick the faster burn masked less, or one cylinder's burn —
the recordings did not tell them apart then either. **A lifter that
ticks warm after a hard drive** is what H1 predicts and what the hot
recording of 26/10 did not find.

**The recording of 11/11 read** (12/11, a cloud session; album
21:55:11, 40 s, the phone held close over the plenum's cast runners,
neutral, warm, just after the motorway run; *an ad-hoc script, not
kept*): the envelope of the sound at 2–12 kHz, the engine speed from
its own firing line — **about 800 rpm throughout** — and the envelope
spectrum's amplitude at the camshaft's frequency over its median in
3–100 Hz. **In 3 s windows the once-per-cycle rhythm stands 5.5–9.6
times the median, about 7 in the middle**; the firing line itself
13–18. That is **D11's own range for 3 s windows (3–10) and the size of
9/11's idle after the clean (7.8) and 15/10's warm idle (7.1)**, not
18/10's 16.4 with cylinder 3 out. Folded on the cycle, **one of the
four firings is 1.2–1.4 times the mean of the four in every window**,
and **it is loud** (above 1.5 times the other three) **in about a
quarter of the 251 cycles**, mostly single cycles, a few runs of 3–9
(0.5–1.4 s) — D11's bursts, at idle. *D11 does not record its window
for the per-video figures, so those compare in order of size, not to
the decimal.* **Read** (*reasoned*): **the tick he heard is the same
once-per-cycle part every engine-bay recording has carried since
12/10, at its usual size** — it did not grow after the hard drive,
which **a lifter bleeding down hot would have shown as a jump towards
18/10's**. It does not say which cylinder: one
microphone cannot. It leaves H1's lifter where it was — not found by
the sound, not excluded — and the stethoscope as the test.

**Tests**: **the stethoscope on the cam cover above each
cylinder, hot** (`plan.md` 9); VW's tappet check in item 9's garage
session.

### Other — not symptoms, but they touch this file

**Oil temperature.** 0x420's `OilTemp` is `raw − 60` °C (`docs/firmware/can-decoding.md`
question 10, closed 23/10). A bias moves both sides of every comparison alike.

**The remap.** The ECU was remapped in 6/2018, "mild", the tuner finding
nothing at the top. Written down as H14 (16/10). Not written back on 22/10 (*owner*,
20/10); **written back on 3/11**, the tuner's original and remap compared the same day,
privately, never in this repository. **3/11, at the tuner**: the ECU out —
VW `06A 906 018 EJ`, *BENZIN V04*, Bosch `0 261 206 327`, made 15.06.99 in
Mexico (*owner's photo*); **the tuner: the map should not affect the idle**
(*owner*); on the MAF's scaling, the idle advance and the idle speed
nothing; **the files came the same day and were compared** — only full
load changed (H14). **The drive home on it** is read under H14 too.

**Water under the tailpipe during the clean** (*owner*, 9/11, photo
10:56): a wet patch of clear water, darker only with soot or rust from
the pipe, after about half an hour of the hydrogen clean at 2,000 rpm
with no load. Expected (*general*): combustion makes water, the
oxyhydrogen almost nothing else, and an exhaust run without load never
gets hot enough at the back to carry it off as vapour, so it condenses
in the silencer and drips. **Not a symptom** (*the owner's decision*);
it would bear on H20 only if water kept dripping after a long warm
drive.

**The brake pedal is soft and long** (*owner*, 9/10): hydraulics, not the
servo and not the engine — a matter for a garage.

**Oil on the underside, the sump's rear the wettest** (*owner*, 26/10,
looking from below during the oil change; `photos/sump-oil-2026-10-26-*.jpg`):
an oily film over the sump towards the back, along its flange and on the
bracket behind it; the gearbox casing drier. **It was there before the
change** (*owner*), though nobody had looked from below. **Settled 31/10
from right under the engine** (*owner*): **the engine leaks nowhere** —
the oil there is what is left of the earlier leak at the cover joint
(S10, closed) — and **the gearbox leaks**, the oil coming from it. *This
said "whether it is what ran down from the cover joint or a leak of its
own is not known" until then.* **It bears on `plan.md` 6i**: with no
engine leak, a falling dipstick level is oil burnt, not lost.

---

## How the symptoms relate — what is measured

| pair | link | evidence |
|---|---|---|
| S1 ↔ S3 | **the same events, but 014 is switched** | half of 014's rises sit on a dip; whether it counts follows load and the learned idle air, not the grade (S3) |
| S1 ↔ oil temperature | **strong** | roughest cold, calmest hot, every session |
| S1 ↔ load | **strong** | every load on calms it (S1) |
| S1 ↔ the drive before a warm stop | **medium, 11/11** | four captures of five after high revs (`46` the exception; `49` 12/11), nine after gentle drives: after high revs the stop starts rough on 3 and settles in 5–8 minutes, after a gentle drive it is level or slowly worse (S1, *The rough start of a warm stop*) |
| S2 ↔ S3 | **likely** | the owner heard the puffs come with the dips (12/10); never aligned |
| S14 ↔ S2 | **likely one mechanism** (*owner*) | a misfire's charge burning in the exhaust, loud when the fuel cut adds air |
| S14 ↔ S3 | **possible** | 014 is blind on the overrun, so it cannot be aligned |
| S4 ↔ S5 | **very likely one thing** | same window, same speeds; S5 needs no combustion |
| S4/S5 ↔ S1/S3 | **none measured** | no retard and no 026 signal at idle; 014's misfires sat on 3 and 4 until the VW leads and on 3 since (S3, *What 014 counts, by cylinder*; *this said "all four alike since" until 12/11*), and lead 4's end was the loosest (`refuted.md` C24) |
| S19 ↔ the bad start of 24/10 | **suspected one event** (*owner*) | same window, both what a cylinder flooded while standing gives (S19) |
| S21 ↔ S19 | **possible, through H16** (*reasoned*) | both would sit on the purge path; no event links them |
| S12 ↔ S3 | **possible** (*reasoned*) | 014 counted seven single misfires on `47`, each in a window holding a moving-off (S12) |
| S3 on the road ↔ S17, S5 | **possible, one engine-speed band** (6/11) | 014's road episodes at 21–32 % load: 2000–2400 rpm about twice 1600–1800 and 2400–2600 (S17); the bus shows no stroke-to-stroke roughness peak there |
| S16 ↔ S1 | **untested** (*general*) | a gearbox's rattle in neutral is driven by the crank's unevenness at idle (S16) |
| S11 ↔ S1 | **untested** | if the hiss is a leak, H3 or H2; the owner reads it as the throttle's own air |

**Two clusters**: **the idle** (S1, S2, S3, S14) and **the cylinder 4
window** (S4, S5). S11 sits beside the idle, unplaced; S19 and S21 beside
it, the trims and the evaporative system. *S23, the new rear probe's
signal, stood apart until it closed 12/11 (`refuted.md` D13).*

---

## The open hypotheses

Each lists what it explains, what speaks against it, and the test that
settles it. ✔ fits, ~ fits weakly, ✘ does not fit, — says nothing.

**The columns are the open symptoms that bear on the engine**: S1, S2, S3,
S4, S5, S11, **S12** (reopened 10/11 night, the jerk at a crawl), S14,
S19, S20 (added 26/10), S21 (added 6/11); **S22** (added 9/11, closed
the same evening, `refuted.md` D11, **reopened 11/11 night** at the
owner's decision, its column back: ✔ for H1's lifter, ~ where a part
or one cylinder's burn could tick once per cycle — H0, H2's port, H7's
injector, H13); **S23** (added 10/11 evening, the rear probe's signal;
a column since H21 was added the same evening, — everywhere but there);
**S1s** (added 11/11, *agreed with the owner*): not a symptom but S1's
rough start of a warm stop after a hot drive, cylinder 3's and settled
in 5–8 minutes (S1, *The rough start of a warm stop*) — ✔ where a fault
worst hot on 3 fits it (H1's exhaust seat, H13's flake), ✘ where the
hypothesis expects the drive to calm it at once (H18).
Left out: S16 (the gearbox side, shown not to touch
the idle) and S17 (a resonance, not placed); S24 (G62's reading, a
sensor's own fault no hypothesis here explained) was never a column and
closed 12/11 (D12); S7 closed on 31/10 (D2)
and its column went with it; the closed ones are in
`refuted.md` §D.

### H0. The idle is normal for this engine — and there is no fault to find

**Re-read 12/11, the third research** (S1, *Every stroke named*; S3,
*What 014 counts, by cylinder*): **against.** The misfires are one
cylinder's — 80 % of 014's rises on 3 since 21/10, 1 and 2 next to
never — and 3 gives 10–20 % less than the mean at every warm idle; an
engine idling at its limit by design would spread them over four.
What is left for H0 is the small unevenness on all four (about 3.5 rpm
rms a stroke), which no repair has moved.
**12/11 evening, for, in that part** (S1, *The swell's shape, and what
the common part follows*): the common part is the same at every warm
idle since 24/9 — 2.7–3.1 rpm rms by capture, within 5 % — and moves
only with a load (a fifth less), the provider's gas (two fifths less)
and temperature (a fifth more cold): a constant answering to the
charge alone, as an engine's own scatter does. A fixed fault on all
four would read the same; no healthy AQY says which.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ✘ | — | ~ | — | ~ | ✘ | ✘ | ~ | — | ~ |

- **Against:** 014 reads 12–120 against VW's 0–5; the old converter burned
  through; the misfires and the steady deficit are 3's (S1, *Every
  stroke named*; S3), and P0303 has been stored three times (18/10, after
  `43`'s cut, 12/11 without one); the 2019 P0304 and the noisy knock
  window are 4's; the inside of 3 and 4 is worse. *This said "the dips
  sit on 3 and 4" until 12/11.*
- **For, 12/11: about an eighth of `IdleHealth` is the crank wheel's own
  alternation** (S1, *A steady pattern over the cylinders*) — no
  combustion, there on any engine with this wheel, nothing to find.
- **For:** no code is stored (2 % threshold: *under 2 %*, not *healthy*).

**Test:** ~~a USBtin capture of a healthy AQY~~ — **not obtainable**
(*owner*, 21/10): the bus is reached only at the cluster harness behind the
vent, and no owner will have a splice made there. What remains needs only the
diagnostic port: **VCDS on 014 at a warm idle of a healthy AQY**, 3–5 min,
loads off — whether a sound engine of this family also counts above VW's
0–5. It compares only on the same ECU (Motronic M5.9.2), and says nothing
of the grade or of the one cylinder.

### H1. A lifter or valve on one cylinder (valvetrain)

**Re-read 12/11, the third research** (S1, *Every stroke named*):
**for, and the cylinder is 3 by every measure** — its steady deficit
(−9 % at its floor), its misfires (80 % of 014's rises), and a state
that **swells over minutes of unloaded idle to −26 % and falls back in
one step** at a jolt (a cut on 4, the A/C coming on, or nothing seen):
what a valve that does not quite seat until it turns or sheds a flake,
or a lifter, gives, and what a leak, a wire or a short injector has no
reason to. Against a valve that leaks all the time: the cold
compression (A4), and on the overrun 3's slot reads level with the
others' (nothing left with the wheel out, `--wheel`) — a closed
throttle hardly loads a seat, so weak. **The warm leak-down with 3 twice (item 9) is the test of the
cylinder now named.**
**12/11 evening** (S1, *The swell's shape*): the swell is a sawtooth —
1.5–3 % a minute up, 30–45 s down, with nothing on the bus at the
fall — and every stroke of 3's is weaker in it; a load masks it and
does not end it; the mixture does not move. **For a seat on 3 that
fouls at idle and burns itself clean**, the reading that fits most of
it; **against a flake blown out or a valve turning**, which this entry
named and which would mend in a stroke, not in 250. A lifter only if
it holds a valve off its seat. *Agreed with the owner the same
evening*: the phone's recording through a swell and its fall beside a
capture (`plan.md` 6p); the warm leak-down made on an engine switched
off in a swell (item 9).

A hydraulic lifter that bleeds down, or a valve that seats late or not quite,
on one or two cylinders. *General.* **Widened 4/11/2026** (*agreed with the
owner*, after the research of 4/11):
**the exhaust seat on 3 the likeliest form** — a small leak there draws
exhaust back into the cylinder through the intake stroke at idle vacuum,
which load (a higher manifold pressure) eases and a higher idle speed does
not (`refuted.md` D9), and cold cranking compression misses (A4); it is
also where H13's flake would sit (SAE 2000-01-2858, 2003-01-3187: deposit
flakes trapped under exhaust seats leak and run a cylinder rough, water
the strongest trigger of flaking). **A stem sticking in its guide** (varnish
or carbon on the stem, which neither the EPR flushes nor H13's clean
reach) fits S18's cold hang-up and a mild steady excess after it; **a
lifter stuck pumped up** holds its valve a hair open with no tick. A
lifter that bleeds down would tick, and the hot recording of 26/10 found
none at idle; **9/11, a tick once per cycle during the hydrogen clean**
(S22) was closed the same evening as the clean's own sound
(`refuted.md` D11). **8/11, the coldest start on record** (about 14 hours outdoors at
−2.5 °C; `idle-log.md`): **the valvetrain clattered for the first second
or two, then stopped** (*owner*; not a new symptom, *the owner's
decision*) — what hydraulic lifters that leaked down overnight do
until the oil pressure refills them (*general*), so it says nothing for
a lifter stuck at a warm idle; one that kept ticking warm would. *General* for these (GM bulletin 19-NA-219, another engine family:
valve leakage misfires most at idle, compression normal, a leak-down
finds it). **The inlet seats of 3 and 4** (*the owner's reading* of the
port photos, 7/11, re-read with him): looking down the ports of 19–20/10
(album 00:00–00:33; `photos/borescope-2026-10-20-cyl*-inlet-port-*.jpg`),
**1 and 2 have a thin, even brown band where the throat meets the seat
ring; 4 a band of white beaded crust along it** (00:03:06–00:03:49),
**3 a thick, broken crust all round it, with a lump standing out of
the edge** (00:12:31, the owner's marked frame of 7/11, and
00:12:44–00:15:44). The camera sees the ring's upper edge with the
valve a little open; the contact face under the head cannot be seen, so
whether the crust reaches it is not known (*reasoned*). **What an inlet
seat that does not quite seal would do** (*general*, *reasoned*): at
idle, with the manifold at its deepest vacuum, compression and burning
gas leak back into the port, so the cylinder loses charge and takes in
hot residual with the next one — worst at the smallest charge, eased by
load (a higher manifold pressure), not helped by a higher idle speed,
and missed by a cold cranking compression test, as the exhaust seat's
form above. **It answers this hypothesis's main against** (*A steady
pattern over the cylinders*): two crusted inlet seats weaken 3 and 4
together, where one exhaust seat on 3 would weaken 3 alone; and more
crust on 3 fits the dips leaning to 3. **Against**: the crust is seen,
its seal is not; and 3 and 4's ports and chambers are worse alike
(H13), so it may be where the deposit sits rather than what fails. **The
leak-down names it**: a hiss at the throttle with the plenum off. **The
chamber photos beside them** (7/11, *at the owner's request*; album
00:43–02:44): a valve stands open in only a few frames — cylinder 2's
(02:24:33–02:25:20), whose conical seat face reads smooth and even with
white beads of deposit on the head's rim beside it; 4's (00:48:24), out
of focus, crust at the edge; 1's (02:41:31) unclear; **3 none**, every
frame of 3 a closed valve or the crown. Which valve of each is open is
not known from the frame. **So the chamber side neither confirms nor
clears the inlet seats of 3 and 4**; what stands is the ports' contrast,
1 and 2 even against 3 and 4 broken, read from above. **The open valves at full
resolution** (7/11, *the owner's reading*: the inlet head reads light,
the exhaust dark; he sees 4's seat face uneven, 2's and 1's smoother):
the sharp frames, 2's (02:25:20) and 1's (02:41:31), show a smooth
face; **4's only open frame (00:48:24) is out of focus**, and its round
beads are what blur makes of any edge — 2's own blurred frames
(02:24:33, 02:25:09) show the same beads along its rim. So the
difference cannot yet be told from blur (*reasoned*); a sharp frame of
4's face would decide it.
**Test: a warm leak-down on all four**, listening at the
tailpipe (exhaust seat), the throttle (inlet) and the oil filler (rings);
**a stethoscope on the cam cover above 3, hot**, against 1, 2, 4. The AQY's lifters are hydraulic bucket
tappets (*hydrostely*), fed from the head's gallery through a small hole
each; inside, a plunger and a check ball hold an oil column that takes up
the lash. They fail two ways (*general*): **one that does not fill** (a
narrowed feed, air, wear) leaves lash, ticks, and opens its valve late and
short, worst hot at idle; **one whose plunger or ball sticks** with varnish
or debris holds its valve a hair open, which costs compression and misses
at a small charge and is covered by load — the case this hypothesis is
about. The valve is closed by its spring; the lifter only removes the gap.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ✔ | ✔ | ~ | ~ | — | ~ | ~ | — | — | — | ✔ |

- **9/11, after the clean** (S1, *The clean of 9/11*; S22): 3's swell
  gone at stop 7 and its floor kept (−8 to −9 %), the swell back a day
  later (`47`) — the clean cannot reseat a worn seat (*general*), so a
  seat that leaks as a part fits the floor and one that a deposit holds
  open the swell; S22's tick closed as the clean's own sound
  (`refuted.md` D11), reopened 11/11; and with the gas flowing **no dip
  at all**, which a stroke that loses its charge through a seat would
  not obviously give (*reasoned*, against in part). *This bullet read
  "3's excess gone", and "4's deficit kept, which an inlet seat on 4
  fits", until 12/11.*
- **3 is the weak one at every warm idle on record** (S1, *Every stroke
  named*; `43`, 3/11 evening, −13 % with 62 % of the weak strokes) — one
  cylinder, the one with the deposit and 18/10's tick (S18; `refuted.md`
  D10): **for**. A compression or leak-down reading on 3 against the
  others would show a seat that does not close (*general*).
- **4/11, the two patterns on their own** (S1, *Load smooths it* and
  *driving does*; *reasoned*, agreed with the owner): with H13's flake on
  3's exhaust seat, **the one reading that fits both** — a load raises
  the manifold pressure and so cuts the exhaust drawn back past the seat;
  a working drive burns, dries or blows the flake off it for a while, and
  queuing lets it soak and soften again. **For.**
- **The owner's reading of the photos, 4/11** (`borescope-2026-10-20-cyl3-exhaust-valve*.jpg`):
  **coarse deposit right up to the edge of 3's exhaust seat**, in the
  dark band beside the valve's margin. Not conclusive by his own account:
  the contact line itself is hidden while the valve is closed, so the
  photos show deposit beside the seat, not under it. **For**, with H13.
  **How the seat is reached** (*general*, searched 4/11): only with the
  head off — the valve cannot come out with the head on, the cover gives
  only the cam and the lifters, the exhaust port only the back of the
  valve, and a soak through the plug hole (a Kia/Hyundai procedure, TSB
  23-EM-007H, the nearest maker's one found; none from VW for this engine)
  lies on the crown, not the roof. So the warm leak-down comes first
  (`plan.md` 9): the head off for the seat only if it hisses at the
  tailpipe on 3.
- **For:** a valve that seals worse at low cylinder pressure misfires at a
  small charge and is covered by load; the tick once per cycle of 18/10 (`refuted.md` D10); one forum
  AQY case of a sticking bucket tappet (pkw-forum.de, 2003) and one of valves
  not sealing (forum.vwgolf.pl t=522030).
  **The oil before 6/2026** (*owner*, 23/10; `vehicle-history.md`): about
  three years in the engine, nearly one of them standing outdoors,
  condensed water under the filler cap at the change — the conditions in
  which oil forms varnish and acids (*general*), and varnish is what
  sticks a plunger or a check ball. **The old oil came out really black,
  and no flush was run** (*owner*, 24/10). Weak: it says the means was
  there, not that a lifter took it up — black is what a detergent oil
  holding soot looks like after three years (*general*), and the top end
  seen with the cover off on 1/10 carried only a thin golden-brown film,
  no sludge on the cam or the caps (`refuted.md`, the head gasket entry).
- **For, 11/11: the rough start of a warm stop after a hot drive is
  3's** and settles in 5–8 minutes (S1, *The rough start of a warm
  stop*) — what a seat that leaks hot, or holds a flake the drive
  loosened, gives; and the weak strokes come in spells of seconds on one
  cylinder (S1, *How the weak strokes follow each other*). *Reasoned*,
  three captures after high revs, `46` the exception.
- **Neither, 11/11: the cold clatter of 8/11** (the first second or two
  at −2.5 °C): VW's own procedure for the 2-valve 2.0 calls irregular
  valve noise on starting normal (*What the forums say*, 11/11).
- **For, 12/11: the steady pattern is 3's alone** (S1, *Every stroke
  named*): with the crank wheel's alternation out, 3 gives 10–20 % less
  and 4 is level — what one seat on 3 gives. What moves over minutes is
  3's swell; its floor holds still, as a fixed leak would (*reasoned*).
  *This was "against, 5/11: the steady pattern names 3 and 4 alike" until
  12/11*, on a count that slipped with the wheel left in.
- **Off idle, 12/11 night** (*Naming the cylinder*, *Off idle*): 3's
  deficit against 2 is a fifth of a stroke at idle and 1–3 % at full
  load. **For**: a seat's leak is set by time, and fades with speed.
  **Against**: at idle speed it falls from −24 to −9 % when the engine
  pulls (b7 27 → 57) — more charge at the same time per stroke, which
  a leak would follow (*reasoned*). **What is left of the seat is its
  dilution form** (*agreed with the owner*, 12/11 night): an exhaust
  seat that lets burnt gas back into 3 at the idle's vacuum, or a flake
  that holds it off; a seat that loses compression is not what the
  load shows, nor what 12 bar on all four showed.
- **Against:** compression **13 bar in 2018 and 12 bar even on all four in
  2026** (`vehicle-history.md`) — no cylinder losing; the vacuum gauge
  steady cold and warm, no flick (H3); no ticking before 18/10, and **none on any
  drive since, through 24/10** (`refuted.md` D10) — a lifter that hung
  should not fade, and this did; the idle is never worst hot, where a thin-oil lifter
  should be; **the phone recording of 24/10, part-warm** (oil 52–58 °C):
  one click per firing, all four alike, over every injector and over the
  cover at each cylinder — no once-per-cycle sound over any lifter
  (`idle-log.md`, 24/10), and **the same hot, 26/10** (oil 100 °C): no
  once-per-cycle sound above the noise floor at any of the eight places
  (`idle-log.md`, 26/10); the valves looked whole on 19–20/10 (which says nothing of
  sealing); 18/10 is explained by 3's flaked deposit without it.

**Tests:** a phone recording over each injector and each lifter, **done part-warm 24/10 and hot 26/10, nothing** (the screwdriver by ear dropped 24/10); **the two EPR flushes**, done 26/10 (`idle-log.md`), which clean the
feed passages and the plungers' varnish — alongside BG 44K, so an
improvement would not tell H1 from H13; no tick since; a warm leak-down
(declined 20/10, *owner's decision*; back in `plan.md` 9 since 4/11, 3
twice since 11/11); VW's tappet check with the cover off (`plan.md` 9). 18/10 coming back, cold, would reopen it (`refuted.md` D10).

### H2. A leak ahead of the converter — ahead of the front probe (manifold, its joint to the head, the probe boss), or between the probes

At idle the exhaust pulses dip below atmospheric and a crack draws air in.
*General.* **Two zones, which act differently** (the second added 10/11,
*the owner* agreeing; *reasoned*):
- **ahead of the front probe**: the **original manifold, its gasket to
  the head and the probe's boss** — the probe sits on the manifold
  (`vehicle-history.md`). The front probe sees the air, the ECU enriches,
  and the converter gets a mean of about λ = 1;
- **between the front probe and the converter**: the manifold-to-front-pipe
  joint (remade by the garage on 10/9), the new flex pipe, the universal
  front pipe, and **its spare lambda boss, closed by an old probe with its
  leads cut off** (`vehicle-history.md`). The front probe sees the true
  mixture, so the fuelling, 032 and the cylinders are untouched; the
  converter gets the air besides, and **the rear probe reads lean, most
  at idle's small flow**, and sinks over minutes as any lean excess does
  once the converter's store is full (H11, *The sinking is the
  converter's shape*) — the 036 reading of 9/11 night in full (H11,
  *What the rear probe can and cannot say*). Nothing else in the table:
  air there reaches neither a cylinder nor the front probe, so the fit
  below is the first zone's.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ✔ | ~ | ✘ | ✘ | ✔ | — | ✔ | ✘ | ~ | — | ~ |

- **For:** the puff (S2), the hiss (S11), air for S14's bangs; a 26-year-old
  manifold that has lived through years of misfires; **for the second zone,
  the rear probe sinking towards lean at every idle** (9/11 night, H11),
  and a boss closed by a probe that was never meant as a plug.
- **The plugged boss, 10/11 night** (*owner*, the album 22:45–22:47):
  the cut-off old probe in it **would not turn further — tight**; the
  boss's weld on the pipe rusty and lumpy, a darker patch at one edge
  that a photograph cannot tell from soot (*reasoned*) — for the warm
  tailpipe test to look at (`plan.md` 7).
- **Against:** air outside the cylinder does not stop one firing, and cannot
  pick a cylinder; no ticking, no exhaust smell (*owner*); just before a dip
  the probe read a little *rich*, not lean; the cold tailpipe test found
  nothing (12/10, the whole exhaust ahead of the tailpipe, both zones) and
  the cold exhaust smoke test nothing (9/10, the exhaust
  would hardly take pressure); **the manifold seen from close below on
  31/10: old and rusty, no black soot marks and no holes** (*owner*) —
  what a leak leaves (`plan.md` 7); **its joint to the head, seen from
  below, nothing visibly wrong** (*owner*); the part under its heat
  shield and the joint from above not seen. The second zone cannot give
  032's idle cell or the dips.

**Test:** the tailpipe test **warm** (`plan.md` item 7), which covers both
zones. A leak in the first zone means a new
manifold; in the second, that joint or the boss resealed.

**After the probes, 10/11** (H11, *The reading after the swap*;
*reasoned*): the new rear probe held flat for 18 minutes of idle and
then switched to the front's swing, rich peaks included. Air drawn in
between the probes would feed a steady excess from the start and show
the lean side only, so **the reading after fits the second zone less
well than 9/11's did**; it does not rule it out. The new probes were
tightened by hand without a torque wrench (`vehicle-history.md`), and a
probe seated loose is a leak in this zone of its own making, hence
their check first (`plan.md` 8e) and the warm tailpipe test after it.

### H3. A small unmetered air leak at one intake runner

**Re-read 12/11, the third research** (S1, *Every stroke named*): **the
runner is 3's, not 4's.** "4's steady deficit", which runner 4's torn
gasket edge was held to explain, was the crank wheel's alternation;
warm, 4 is level. What is left is what this entry already names: **the
lower manifold's gasket at runner 3, never renewed.** For: 3 short in
every state and nearest the edge at the smallest charge; cold, 4 weak
beside it — two neighbouring runners and a joint that closes on one
as it warms (*reasoned*). Against: 032's idle cell is negative where
a leak asks for fuel, the smoke test showed nothing (9/10), and a
leak has no reason to swell over minutes and mend in a step.
**12/11 evening** (S1, *The swell's shape*): **against, for the
swell**: a cylinder 18 % short through its air would be a fifth lean
and move the loop's regulation by about 5 %, and it read the same in
the swell and on the floor; the injection time did not move either.
What is left for a leak is 3's floor.

Air past the MAF leans one cylinder at idle, where air flow is smallest.
*General.* **The only candidate that predicts *load helps* directly.**
*Widened 4/11/2026 to a line entering the plenum near runner 3, and
withdrawn the same day* (*owner*, off the car): **every line joins the
intake in its common part, none nearer one runner than another**, so
whatever enters by a line reaches all four alike; what is left of H3 is
the lower manifold's gasket at runner 3, never renewed.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ✔ | ~ | ~ | ✔ | ~ | ✘ | ~ | ~ | ✔ | ✘ | — | — | — |

- **9/11** (S1, *The clean of 9/11*): **3's floor kept after the clean**
  (−8 to −9 % at stop 7): for, on 3; **the gas cured the weak strokes
  outright**, as a richer, quicker-burning charge would in a lean runner
  (*reasoned*): for in kind. *This bullet read "4's steady deficit kept"
  until 12/11.*
- **One cylinder throughout, and it is 3** (S1, *Every stroke named*):
  never "all four alike" on `40`–`41` (3 −14 %, 64 % of the weak strokes
  on `40`), so **the demotion of 24/10 had no ground**: **for**, at
  runner 3.
- **4/11, the two patterns on their own** (S1; *reasoned*, agreed with
  the owner): **load, the best of all** — the leak's flow is about fixed
  at idle vacuum, so its share falls as the charge grows; **the calm after
  revving, not at all** — a leak does not know what the engine did a
  minute before. **Against**, on that half.
- **For:** the regime; S14 at the thinnest charge; a leak at one runner acts
  on one cylinder, and 3 and 4 are neighbours on the lower manifold.
- **For, 12/11: the steady pattern is 3's alone** (S1, *Every stroke
  named*): 3 gives 10–20 % less warm, 4 level — one runner; cold 4 weak
  beside it. *This read "names 3 and 4 alike", a leak between their
  runners, until 12/11.*
- **5/11 evening, the lower manifold's gasket seen from below** (*owner*;
  `photos/lower-manifold-gasket-2026-11-05-*.jpg`): **at runner 4 torn,
  and looked at closely the tear may reach into the sealing face; at
  runner 3 not torn but bent, straightened by the owner the same night;
  whole at 1 and 2** (*owner*; the
  first look read both as torn outside the face, cosmetic, perhaps from
  his own hands reaching for the plugs). The gasket old, perhaps
  original. *Reasoned*: from
  below a tear at the outer edge cannot be told from one that runs in
  across the face, and only a smoke test or the manifold off says which;
  for H3 in place, not in proof. **The smoke test of 9/10 showed no smoke
  there** (*owner*, 5/11: nothing smoked below; *Against* below) — against
  a tear that passes air, with the limit that a smoke test pushes a few
  kPa outward on a cold engine, while a warm idle pulls about two thirds
  of an atmosphere inward (*reasoned*).
- **For, 12/11 night: *load helps*, measured** (*Naming the cylinder*,
  *Off idle*; `tools/drivescan.py`): 3 less 2 is −21 to −26 % of a
  stroke standing, crawling and to 1,600 rpm with the pedal light, −9 %
  pulling at idle speed, −2 to −5 % at part load, −1 to −3 % at full,
  at every speed to 5,200 rpm — a deficit that follows the manifold's
  vacuum, as a leak at the runner does. H18 and H20 predict the same.
- **The owner's reading, 12/11 night: two causes at once** (*owner*;
  the rest *reasoned*). A leak at runner 3 **and** something that
  makes all four rich at idle (N80 passing vapour, H16; or whatever
  S19's is): the ECU trims the idle 6–8 % lean for the four together,
  and 3, already lean by its leak, is leaner by that again — at the
  edge where it misfires. **It answers the strongest point against
  H3**: 032's negative idle cell no longer speaks against a leak at
  3, because the trim is the other cause's; one cylinder's leak asks
  for about a quarter of its own size the other way and would be
  buried in −6 to −8. **And it fits the load**: both the leak and a
  fixed flow of vapour are large against the idle's air and nothing
  against full load's. **His second half, the swell as N80 letting
  vapour through in waves, is not what VCDS showed**: the regulation
  (001, three rows a second, `50`) read −0.4, −0.5, −0.3 and +0.2 %
  at −23 %, through the fall, at −5 % and growing again, swinging the
  same throughout, and the injection time moved 1.5 % (S1, *The queue
  drive, and what the ECU sees through a swell*) — a wave of vapour
  under all four would have pushed the regulation lean by its own
  size, since the learnt value (032) is too slow to take it. *The one
  way round that*: vapour reaching mostly runner 3, which the single
  front probe sees a quarter of. **What tells**: 8a's new N80 and
  8o's hose shut — if the rich idle trim goes with the valve, 3 loses
  the second cause and should calm even with its leak; 001 and 032
  beside 014 at every one of those stops, as planned (8f).
- **Against, 5/11** (*reasoned*): a cylinder running lean would pull
  032's idle cell positive; it reads −6 to −8 % (H4, the same argument;
  medium, the trim carries other inputs). *It said "two cylinders" until
  12/11*; one cylinder's leak pulls it a quarter as far, so this is
  weaker than it was — **and weaker again with a second cause for the
  trim** (*The owner's reading, 12/11 night*, above).
- **Against:** a large leak is refuted (`refuted.md` A7): idle air 3.1–3.5 g/s
  against VW's leak mark of 2.0, 055 inside ±1.5, 032's idle cell negative.
  **The intake smoked tight cold** (9/10) after the dipstick guide and the
  MAF clamp were put right; **the vacuum gauge** on the tee by the runners
  steady at 18–19 inHg cold and warm, higher at 2500, no flick (14–15/10) — a
  gauge on the common plenum cannot see a leak at one runner. The lower
  gasket looked alike at all four (*owner*, 20/10). The crankcase gas enters
  the common intake, so it cannot pick out 3 (*owner*).
- **Parts renewed in its name:** the upper plenum gasket (each time it came
  off), the breather and its hoses (12/10), the throttle and its gasket (2/10),
  the injectors re-seated (1/10).

**Test: none without dismantling.** Brake cleaner at each runner's head
joint and injector seat was the plan, and it **cannot be done in place**
(*owner*, 24/10): no room past the coil at 4, the runners of 2 and 3 out of
reach. What is left is the plenum and the lower manifold off, **the lower
gasket renewed** and the injector O-rings looked at — a repair that tests
by its result.

### H4. Weak spark from what feeds the parts (earth, wiring, coil feed)

**Re-read 12/11, the third research** (S1, *Every stroke named*): what
is left of it is read **for 3**: the injector loom where it reaches 3
(6m, flexed while measured). 3 alone carries the deficit and the
misfires since the VW leads; 4's share went with the leads. A wire has
no reason to cost a steady 9 % in every state, so weak.
**12/11 evening** (S1, *The swell's shape*): against, for the swell —
the mixture and the injection time do not move with it, and a load
masks it at once, where a load makes a weak spark worse.

**Much weakened, kept last of the electrical side.** Measured clean: the
coil's ground and supply for a gross fault, the engine's earth under load,
the charging; the battery is new (8/2026). **The idle is better with the loads
on, when the coil's supply sits 1.25 V lower** — a spark limited by supply
would go the other way. The weak cylinder is 3, through three sets of
leads and plugs, and its coil output also fires 2, the strongest, so
neither the coil nor its feed can pick it (*this said "the dips sat on
3 and 4 … on different coil outputs" until 12/11*). **What is left**:
the injector loom where it reaches 3 (and 4), taped and oily — its wires at 4 whole outwardly (*owner*,
19/10; tape renewed). The plug-end side moved to H15, refuted 4/11 (`refuted.md` C24).

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | ~ | ~ | — | ✔ | ~ | ✘ | — | — | — |

- **9/11** (S1, *The clean of 9/11*): 3's floor kept after the clean,
  its swell gone for a day: for 3's own circuit (6m) in the floor; with
  the gas flowing no dip at all — hydrogen lights on less energy
  (*general*): for in kind. *This read "4's steady deficit kept, 3's
  gone: for 4's own circuit" until 12/11.*
- **One cylinder, 3** (S1, *Every stroke named*): weakly for at 3.
- **4/11** (S1, *Load smooths it*): 45–50 with the A/C and the rear
  window on at about 12.4 V against 90–110 without — a higher cylinder
  pressure needs more voltage at the gap and the supply is lower, so
  anything on the spark side, plug 3's gap included, predicts the
  opposite (*general*). **Against.**
- **12/11 night, off idle** (*Naming the cylinder*, *Off idle*): **at
  full load 3 is within 1–3 % of 2, and no stroke of 100,000 there
  misfires** — where the spark is hardest to make. **Against** the
  spark side on 3; the injector-branch form (short only at the
  smallest quantities) is not touched by it.
- **5/11, the steady pattern over the cylinders**, re-read 12/11 (S1,
  *Every stroke named*): **3 alone gives 10–20 % less** warm, 4 level;
  a raised resistance in 3's branch would give a steady deficit, but no
  reason for it to swell and mend in a step (*reasoned*). Against the
  spark side as above. *It read "3 and 4 give 3–4 % less alike — the
  pair the loom feeds; for the loom" until 12/11.*
- **Why load would help** (5/11, *reasoned*, *general* for the physics): a
  raised resistance slows the current's rise in the injector's coil, so it
  opens later by a fixed delay; at idle the pulse is shortest and that
  delay costs the largest share of the fuel, under load a smaller one.
  **H4 predicts "worse only at idle, load helps"** on its own. And the
  trims before a dip (S1, *The dips ride a swing of the idle loop*) fit a
  cylinder that is lean already and fails when the mixture is trimmed —
  as much for H3.
- **Against, 5/11** (*reasoned*): **032's idle cell is negative** (−6 to
  −8 %): a cylinder lean by its deficit would make the mixture lean, the
  probe would see it and the trim would add fuel, not take it away — the
  same against H3. Medium: the trim carries other inputs (the purge, the
  MAF). **The calm after revving** needs heat to reach the joint, a weak
  link. **3 is the borescope's worst** (3 > 4 > 2 > 1), so H13 explains
  it without a wire. *"3 and 4 do not behave alike … where a shared
  loom would expect them close" is moot since 12/11: 4 is level warm.*
- **5/11 evening, the first look** (*owner*, plenum on): only 1's and 4's
  connectors reachable. **From one pin of 4's connector to a pin of the
  loom's own 3-pin connector** (at the end of the loom, by cylinder 1):
  **about 2 Ω, at times 1.9, at times 3.4** — against the manual's 1.5 Ω
  for a whole wire; the meter's probes touched together read 0 (*owner*),
  so the figure is the path's or the probe's seating, which wandered —
  **injector 1's contact 1 to the same pin** tells which: alike, the shared
  part (T3 or D95); 4 alone higher, 4's own branch. **Flexing the loom at
  injector 4 while reading did not move the figure** (*owner*, engine off
  and cooling): no intermittent joint there that a hand can find — against
  a loose contact in 4's branch, at least cold and still. **Then, the
  probes re-zeroed: injector 1's and injector 4's contact 1 to the same
  T3 pin both 0.001–0.002 Ω** (*owner*); the 1.8–3.4 Ω before was the
  probes, not the wire. **The supply to 1 and 4 is sound and alike**; 2
  and 3 and the control wires not measured (the intake on). **That 3-pin connector's latch
  is worn**: it holds, but comes off by pulling without pressing the
  tongue (*owner*). **The beeper joins one of its pins to contact 1 of
  injector 4** (*owner*) — the supply side, so the 3-pin connector carries
  the injectors' supply at least.
- **The wiring, from VW's diagram for this engine** (Golf/Bora 2.0 AQY,
  sheet 55/6; the text of the diagram read only in a garbled preview,
  eserviceinfo.com and portal-diagnostov.com, 5/11): **one supply for all
  four** — fuse S232 (No. 32, 10 A), 1.5 mm² red/violet, connection A101
  (relay terminal 87), connector T10a/5 (10-pin, cable channel left in the
  engine bay), 1.0 mm² red/violet to the splice **D95** in the harness and
  on to **contact 1 of each injector**, all red/violet. **Contact 2 to the
  ECU**, 1.0 mm²: cylinder 1 pin 73 violet, 2 pin 80 violet/green, 3 pin 58
  violet/red, 4 pin 65 violet/blue — the manual's pins (above). The sheet
  also lists **T3, a 3-pin connector near the intake manifold**, beside the
  engine speed sender G28 and the sender earth 220; which of its pins
  carries what the garbled text does not show, and the owner's beeper puts
  the supply on one. **So the supply is not split by pairs** (*reasoned*):
  a poor joint in it, the worn T3 included, would starve all four alike,
  not 3 — **against H4 through the supply**; what is left for 3 is its
  own branch after D95 and its control wire (pin 58).
- **What the loom can and cannot do unseen** (5/11, *reasoned*, at the
  owner's question). An **open** circuit — the plug off on 3/11 — is
  stored at once: P1240, injector 4, open circuit, sporadic. **No
  P1237–P1240 has ever been stored without a cut**, so a contact that
  drops out completely, even briefly, is unlikely. **A raised
  resistance is not stored**: as long as enough current flows for the
  output stage not to see an open, the ECU finds the circuit good while
  the injector opens late and short and the cylinder runs lean. That is
  what is left of H4, and only a measurement shows it.
**Tests:** **the circuits measured** (`plan.md` 6m among themselves, 6n to the ECU; VW's repair manual, Golf Mk4, *Motronic injection and ignition system (2.0 ltr. engine)*, *Checking injectors* (workshop-manuals.com, read 5/11/2026)):
the injector itself 14–18 Ω at about 20 °C; each wire, connector to
connector, at most 1.5 Ω; contact 1 of the 2-pin connector is the
supply from the fuel pump relay J17, shared by all four, contact 2 the
ECU's output, at the 80-pin connector **pin 73 for cylinder 1, 80 for 2,
58 for 3, 65 for 4** (test box V.A.G 1598/22, whose sockets carry the
connector's numbers; the manual's, not yet checked on this car). Three of
four alike and one tenths of an ohm higher is the reading.
The injector loom flexed at 3 and 4 at a warm idle — **done by
the owner on 24/10, part-warm, during the first phone recording, above all
the repaired wire at injector 4, judged by ear only: no change heard**
(reported 28/10). Weaker than the planned
read (dips per minute in a capture), which was dropped with it. What
is left: VCDS 004 (the ECM's supply) beside 014.
VW's TSB 01-08-27 (the coil's ground wire, US sister engines) is the joint to
look at first if the spark side ever comes back.

### H5. Something in cylinder 4's knock window that is not combustion (S4, S5)

The ECU books anything at cylinder 4's crank angle to cylinder 4: G66, its
torque or connector; a loose ancillary part buzzing in a speed band; **an arc
at lead 4's plug end** (`refuted.md` C24). Injector 4's click is settled against (B7).

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | ✔ | ✔ | — | — | — | — | — | — | — |

**Tests** — not scheduled (*owner's decision*, 9/10): G66's torque and
connector; a look for a loose bracket at ~3000 rpm in neutral; after the VW
leads, the neutral 026 holds and a 020 drive against
`vcds/vcds-step2c-020-026-003.csv`.

### H6. Knock control relearning after the battery disconnects

Explains how S4 changed between logs, not S5. **Test:** 020 + 026 after a few
hundred km without a disconnect.

### H7. Fuel delivery at idle: rail pressure, one injector

**Re-read 12/11, the third research** (S1, *Every stroke named*):
the one-injector form would be injector 3's — 3 gives 10–20 % less at
every warm idle, in every state, which a short injector does. **But 3
was the weak one before the injectors were changed too** (`09`, `12`,
`17` of August, −11 to −23 %, seconds each), **so the injector itself
is unlikely: the same place would have to be bad in the old set and in
the new** (*the owner's argument*, 12/11). An exchange of injectors 3
and 2 was agreed earlier that day as its test and **withdrawn
on this** (`plan.md` 6o, removed). What stays with the cylinder through
a change of injectors is its wiring and the ECU's driver (H4, 6m, 6n).
**12/11 evening** (S1, *The swell's shape, and what the common part
follows*): **against both forms.** One injector: the swell moves
neither the loop's regulation nor the injection time, so it is not
3's fuel. The rail's pressure: the common part is the same after high
revs as after none and the same on every day, within 5 %.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | — | — | — | ~ | ~ | ✔ | ~ | — | ~ |

- **3 the one cylinder throughout, P0303 three times** (S1, *Every
  stroke named*; S3) — one injector in reach by the cylinder; 25/10
  night's "the dips then sat on all four alike" (`40`, `41`) was a count
  that slipped: 3 led there too. **Against, by the owner** (3/11): the
  injectors are new (9/2026); **no swap** (*his decision*, agreed 12/11
  and withdrawn the same day, above), so this stays untested. *The
  owner's history of 3/11 — "on the new VW leads the dips were on all
  four alike and 3 came back only later; a bad injector would never
  have been even" — rested on those shares; by `cylscan.py` 3 was never
  even, and the argument that stands is 12/11's: 3 weak on the old set
  too.*
- **Against:** four new injectors and a new filter changed nothing in S1; the
  trims near zero; full-load pulls reach ~85 kW, where a weak pump shows first;
  the regulator (6/2026, 3 bar) dry at its hose, **no fuel and no smell at
  the hose's end when it came off on 25/10** (*owner*) — against a leaking
  diaphragm, not against one that does not answer its reference; injector tips clean on the
  borescope (19–20/10).
- **A plug washed clean by fuel** (a forum extract on the AEG/AQY, 20/10:
  *"#3 was much cleaner … replaced #3 injector as it was washing that plug"*):
  plug 3 is the cleanest here too. Weak, for the reasons above; a reason not
  to read plug soot as combustion quality.
- **12/11 night, off idle** (*Naming the cylinder*, *Off idle*): 3's
  deficit is not a share of its fuel — a fifth of a stroke at idle,
  1–3 % at full load. **Against** an injector on 3 that flows short in
  proportion; **not against** one short only at the idle's smallest
  quantities (or its wiring, H4).
- **For, since 24/10: S19.** A dripping injector or a regulator that does
  not hold gives a rich code and a start that floods after standing; the
  only hypothesis that predicts both. Every lean-side one (H2, H3, H4,
  H15: unburnt air reaches the probe) predicts P0171 or nothing, not
  P0172. **Since 24/10 not the only one**: a purge valve that does not
  seal predicts both as well (H16), and its test is cheaper.

- **The regulator's vacuum reference** (*the owner's question*, 25/10).
  The regulator holds the rail a fixed 3 bar above the intake through a
  hose to a narrow tube on the intake; the old hose was well perished when
  he replaced it in 6/2026, so crumbs of it could sit in that tube. **A
  blocked or open reference leaves the rail at the no-vacuum pressure at
  idle**, VW's 3.0 bar instead of 2.5 (`vcds.md`): about half a bar more
  across the injectors, roughly 8 % more fuel at idle and less and less as
  the throttle opens and the vacuum falls (*reasoned*: flow goes with the
  square root of the pressure across the injector). **That is the shape of
  this car's 032**, low at idle and normal at part load, and VW's "fuel
  pressure too high". Only a full blockage or a leak does it; a partly
  blocked tube only slows the response. **Tested 25/10 night** (6e,
  `idle-log.md`), cold, the hose off at the intake end twice: **the
  regulation went to −8.6 and −10.2 % within seconds** and came back
  when it went on, **no fuel at the hose** — the regulator answers its
  reference and its diaphragm holds (`refuted.md` C20). **Not tested**:
  its base pressure, the pump's non-return valve and the injectors, which
  only a gauge reads.
- **Found 25/10** (*owner*; `photos/fpr-vacuum-hose-2026-10-25-end.jpg`,
  `-side.jpg`): that hose's **intake end is breaking up** — on the photo
  the wall has come apart into layers with voids between them and a crack
  runs from the bore outwards *(this said "split" until the photo)*, after
  the many times it came off with the intake work, **no clip on it since
  6/2026**, and **at least once left on when the intake came off, so it
  was stretched and pinched** — the likely start of the crack, **from
  about September** (*owner*, 25/10; *this said "left off at least once"
  until he corrected it*). It blows through freely. The timing fits 032:
  low at idle at every reading since 24/9, the first after the MAF. **A split at the joint
  pushes rich, not lean** (*reasoned*): the narrow tube on the intake
  limits what the split can let into the engine, while the hose behind it
  fills from outside, so the regulator sees less vacuum than the intake
  has and holds the rail higher. How much depends on the split against the
  tube, unmeasured. **The first part found on the car that fits the shape
  of 032 and VW's "fuel pressure too high"**; its weight is not known.
  **Its own figure, 25/10**: 032 relearnt from zero since 24/10's
  clearing, about 10 km of driving on it, **−8.6 / +3.9 %** — **the most
  negative idle value on record** (before: −6.3), the part load positive
  as always (`photos/vcds-032-055-2026-10-25-before-new-fpr-hose.jpg`;
  055 −1.25 g/s; fault memory empty). **Read after a few seconds of idle
  with the old hose pulled off**, so it may carry them (*the owner*,
  25/10; *reasoned*: a fraction of a point at 6i's relearning rate, and
  the open hose pushes both ways — `idle-log.md`). **Replaced the same evening** with
  clips at both ends; 032 after some drives says the rest.
  **The first idle on the new hose, the same afternoon**: the live
  regulation **+6.5 % loads off for the first minute and a half**, and
  032's idle cell already **−4.7** from −8.6 — **the hose was carrying
  fuel**, so the rich idle trim is at least partly answered. **Partly**:
  two minutes in, the regulation fell to −10 % and settled near zero, the
  engine wanting about −5 % in all (idle cell plus regulation, an
  approximation) against about −2 % before — **about 3 points of fuel
  arriving on their own at a warm idle**, which fits the purge starting
  (H16; *reasoned*) — left unmeasured by the owner's decision (25/10), and
  6e's cold start showed no such step (`idle-log.md`). `IdleHealth` loads off **about 90
  at 80 °C of oil**, where it has sat before: the roughness is not shown to
  have gone with it (`idle-log.md`).
  **A drive later, the same evening (6j): 032 −7.8 / +6.3 %** — the idle
  cell back to about where it stood on the cracked hose, the part load
  higher than ever. So the rich idle trim is **not** answered by the hose;
  what it answered on 6i's first minute and a half did not last a drive
  (`idle-log.md`).
  **Its size, then** (25/10, *reasoned*): from −8.6 on the cracked hose
  to −7.8 a drive later on the new one is under a point, against the
  roughly 8 % a fully open or blocked reference would give — and the −8.6
  was read with the old hose already off for a few seconds. **The hose
  was at most a small share of the extra fuel**; the rest comes from
  elsewhere (H16, H17, or the regulator or an injector itself). **Since
  6e** (25/10 night) not H16 and not the regulator's reference: with the
  canister cut off the regulation sat near zero on top of −7.8 (H16), and
  the regulator answered its hose. Left: **an injector** (H17 refuted
  29/10, `refuted.md` C21) — a
  regulator holding a high base pressure would scale the fuel alike at
  every load, not take it away at idle alone (*reasoned*).

**Tests:** a rail pressure gauge (**not bought**, *owner's decision*, 10/10;
VW's figures, if one is: 2.5 bar at idle, 3.0 with the regulator's hose
off, **2.0 bar or more ten minutes after switching off**, the last being
S19's question — `vcds.md`);
swap injector 3 with another if the cylinder stays named.

### H8. Idle air control and the throttle body

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | — | ~ | — | — | — | ~ | — | — | ✔ | — | — |

**For: S20, by its timing** (*owner*, 26/10): the speed has been hard
to hold at a steady pedal since the job of 1–2/10, which fitted this
throttle and took up its cable's slack. Not measured; a capture with the
throttle held still would show whether the plate or the engine moves.

**Against, the target** (10/11, 0x288 b5; S1, *The idle speed
target*): the ECU's idle speed target is 780 rpm at every warm idle on
record and the engine holds 15–18 rpm above it every time; raising the
target to 830 left `IdleHealth` at 66. The governor's set point is
steady and met.

**Against:** a dip is one firing that fails and recovers in a quarter of a
second (three in four; one in five is two firings in a row, and warm
those lean to cylinder 3 too — S1, *How many strokes make a dip*, 5/11);
the dips do ride a 0.8 Hz swing of the idle loop (S1, 5/11), but as the
moment a marginal cylinder fails, not as a hunting loop of its own; the plate angle in every VCDS log is steady and
the misfires do not ride on it (27/9); the potentiometer track has no dead
spot or dropout on the bus; the throttle is **new since 2/10** (Pierburg
`7.03703.13.0`) and the idle fault outlived it; it acts on all four. Kept
because it is in the idle air path, not because anything points here.

**The owner's hypothesis, 26/10: the idle regulation itself.** 055's
learnt value has been negative on this engine since September, so the
ECU idles it on less air than its base model; **less air is a smaller
charge, and a smaller charge is nearer the edge S1 reads the idle at**
(*Load smooths it*) — more air, from a load or from the learnt value set
aside (S1, *A second reading*), calms it (*reasoned*). **For**: on 26/10
`IdleHealth` off the display fell as the value relearnt from −2.78 to
−0.90 (`idle-log.md`); 014's counting was read then as following the
value (`refuted.md` C19, refuted 2/11); S20 dates from this throttle (*owner*). **Against**: in the same
log **014 counted about as often at −1.0 as at −2.8** (no trend,
`idle-log.md`); the display readings were single figures across changing
temperature, loads and time, with no `IdleHealth` in the VCDS log to set
against the value; and a dip is one failed firing (S1), which a
regulator can bring nearer but not cause.
**The A/C stop of 27/10** (6k; S1, *A second reading*): **for** — the A/C
sets the learnt value aside and the idle calmed at once, 014 silent for
eight minutes, and with every other load on the grade improved as the
learnt value walked from −1.04 to −0.77; **against** — in the A/C's sixth
minute, the learnt value still aside, the grade climbed back to 56–75.
One stop; it supports the regulation narrowing the margin, not as the
whole.

**The sum of 055's two fields does not move** (27/10, re-read over
every VCDS log with 055 and 014). Field 2 (the live regulator) plus
field 3 (the learnt value) sits at **−0.9 to −1.35 g/s at every warm
idle on record**, whether field 3 was 0.00 (2/10, 4/10 after 098),
−1.2 (settled) or −2.78 (26/10, when field 2 stood at +1.46). After a
reset the live field carries the whole correction at once and hands it
to the learnt one over **two to three minutes of warm idle**; the
learnt value always ends at about −1.1 to −1.3. On 27/10 the A/C did
the same bookkeeping: **everyday −1.07, A/C −0.98, A/C with the loads
−1.10** — the learnt value set aside, the correction the same.
So **zeroing 055 does not give the warm idle more air** beyond its
first minutes (*measured*, VCDS 003 on 4/10: 3.1–3.3 g/s and a plate at
2.6–2.8° in the quiet phase after the reset, as on settled sessions),
and 6k's calm with the A/C is the A/C's load, not the value set aside.
The one state that moved the sum was every load but the A/C: −0.69,
the ECU giving more air than its model. Against the regulation half of
H8 as "less air"; the −1.1 reads as what this engine needs at a warm
idle (`refuted.md` C19).

**Do 055 and 032 belong together?** (*the owner's question*, 26/10): the
ECU takes away both air (055) and fuel (032's idle cell). *Reasoned*, not
measured: **not through one cause**. Air the MAF did not see would push
055 negative but 032 *positive* (lean); extra fuel — vapour from the
breather or N80, fuel in the oil — pushes 032 negative, but the lambda
loop brings the mixture back to λ = 1, which leaves the idle's torque and
so 055 where they were. And both are answers, not causes: undone, the
idle would run rich and fast, not better. **The exception was 26/10**,
when 055's −2.78 was learnt wrong against the stick, and undoing it did
help.

**Tests**: **6g, done 29/10** — 032's idle cell back at −8.6 with 055 at
−1.11, so the two are independent and the rich idle has its own source
(H7, H16; H17 refuted, `refuted.md` C21). **5a, done 3/11** (`42`,
`vcds-step5a-warm-014-055-003.csv`): the learnt value walked from −0.28
to −1.24 over the warm stop, **only after a throttle blip** — each one
started it about 22 s later and moved it about 0.27 g/s over about
20 s (*owner*, seen in the log) — while field 2 gave the difference
back, the sum at −1.2 to −1.4 throughout. **`IdleHealth` fell as it walked**: 93
at −0.3 to −0.6, about 84 at −0.6 to −0.85, 41–67 from −0.85 to −1.25;
014 zero throughout. **Against the regulation narrowing the margin**
on its face, since the idle calmed as the learnt value went down; but
the stop came straight after the motorway, and the first minutes after
high revs read rough on their own (`tools/afterpull.py`), so time and
the value cannot be told apart on one stop (*reasoned*). Not a test
any more: 5b's stops are on a settled value.
**12/11 evening, 003 alone at three rows a second** (`50`; S1, *The
queue drive, and what the ECU sees through a swell*): the scatter of
the advance in a 10 s window does not go with the common part in it
(r +0.08, 48 windows) but with the scatter of engine speed (+0.75);
only its row-to-row jitter leans that way (+0.45), as a governor
answering would give too. Nothing for the regulation narrowing the
margin; the order of spark and speed step is finer than VCDS reads.

### H11. Both lambda probes shifted alike

*Added 10/10 at the owner's request, as a weak hypothesis written down so
that it is not argued again.* The probes are from 10/2017, the one part of
the mixture control not changed.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | — | ~ | ~ | — | — | — | — | ~ | ~ | ~ | — | — |

**Against:** 032 + 033 near zero on a new MAF and new injectors bound a hidden
shift to a few per cent, and with the wrong sign (the ECU takes fuel out); a
shift small enough to hide is too small to misfire. **Test:** a four-gas
analyser at the emissions station, warm idle and 2500 rpm — **declined
by the owner** (10/11); `plan.md` 8c replaces both probes instead.

**Could they give S19's idle cell?** (*the owner's question*, 31/10;
*reasoned*.) **The sign, yes**: a front probe that reads richer than the
mixture is makes the ECU take fuel out, which is a negative idle cell.
**The split, no**: a probe's offset sits under every load alike, so it
would pull the part-load cell negative too, where it reads +5.5 to
+8.6 %; at most it is a common part under both, with something else
still opening the gap. **The step, no**: the idle cell went from −0.8 to
−6.3 % before 24/10 to −6.3 to −8.6 % after, on the same 2017 probes,
and a probe ages over thousands of kilometres, not in a day. An aged
narrowband probe can drift differently at idle's cooler exhaust than
under load (*general*), which would make a split; which way this one
would drift is not known. So a contributor at most, not S19's cause;
the map of 3/11 reset 032, and **the idle cell was back at −6.3 after one
drive** (S19), on the same probes.

**Re-read 9/11 evening: a fault at idle only** (*the owner's suspicion*;
*reasoned*). The *against* above was written on 10/10, when 032 sat near
zero; it has stood at −6.3 to −8.6 % at idle since 24/10, and the gas
idle of 9/11 shows how close to the edge the burn sits (dips are
preceded by about 1 % less injection; S1, *The gas idle taken apart*),
so a few per cent matter. **The form not yet argued: the front probe
reads richer than the mixture only at idle** — the coolest, slowest
exhaust, where a probe of 2017 is at its laziest — and right under load.
The ECU then leans the idle (the negative idle cell) while part load is
untouched (the split), and **the real idle mixture is lean**: worse
after queuing, better after a brisk drive, calmed by a load that heats
the exhaust, cured by hydrogen's wide lean limit — every pattern of S1 —
and P0172 once, the ECU's "too rich", fits a probe that reads rich. **The
rear probe need not catch it**: SSP 175 (p. 28) has M5.9.2 correct a
shift of the front probe's curve through a second loop on the rear
probe, *"within a defined framework"*, but says nothing of a correction
by load, and behind the converter at idle's small flow the rear probe
answers slowly (*general*). **The idle cell over time** (9/11 night,
*the owner's question*; every reading in `idle-log.md`): **−5.5 % on
20/8 and −4.7 % on 10/9**, on the old injectors and the old MAF;
−0.8 % on 4/10, relearning after the battery disconnects; −4.7, −3.1,
−6.3, −3.1 % from 15/10 to 23/10; **−8.6 % on 25/10** and −6.3 to −8.6
on every reading since (−6.3 one drive after the reset of 3/11). **So
it is no step but a cell that has been negative since August, a few
points more since 24/10** — the *step* above was overdrawn, and
negative before any repair, as a probe bias would be. **Not telling
either way**: 033's front probe voltage at warm idle swings 0.03–0.72 V (p10–p90,
`vcds-step6i-warm-idle-2`, `vcds-step2b`), which VCDS's ~1 s sampling
cannot judge. **Test, free, read only** (`plan.md` 8c, *agreed with the
owner*, 9/11; **read 9/11 night, below**): **036 field 1,
the rear probe's voltage**, with 033 and 041 (`vcds.md`), at a warm idle
loads off, then with the A/C, then at 2,500 rpm — steady low (about
0.1–0.3 V) at idle and normal at 2,500 says the idle runs lean behind
the front probe; about 0.6–0.75 V throughout says not (*general*).
*Until 10/11 this said "and the front probe misleads": a lean idle does
not name its cause* (*What the rear probe can and cannot say*, below).
**A four-gas analyser** (λ, CO, HC, O₂ at the same three points)
would read the size the rear probe cannot; **the owner declines it**
(10/11) and replaces both probes instead (`plan.md` 8c).

**The reading before the swap, 9/11 night** (`plan.md` 8c;
`vcds/vcds-step8c-before-001-033-036.csv`, `-adaptations-041-032-055`,
`-faults.txt`; standing outside, a cold start, VCDS from coolant 73 °C;
**shortened at the owner's decision** — a housing estate near midnight
— to idle loads off about 3 min, the A/C about 3 min, loads off about
3½ min, **1,500 rpm** (not 2,500) 1 min, idle loads off 1 min). The
rear probe, 036 field 1, means over each phase:

| phase | coolant °C | rear probe V | above 0.45 V |
|---|---|---|---|
| warming idle, the A/C on and off (*owner*) | 74–77 | 0.51 | 70 % |
| loads off | 78–86 | 0.40 → 0.30 | 13 % |
| the A/C on | 88–92 | 0.30 | 34 % |
| loads off | 92–96 | **0.15–0.24** | 14 % |
| 1,500 rpm | 92–95 | 0.26–0.38 | 46 % |
| idle, loads off | 94–95 | 0.58 → 0.42 | 79 % |

**At every idle the rear probe sinks towards lean over the minutes**
(0.6 → 0.3 after warming, below 0.2 by the third phase, 0.58 → 0.42
within a minute after 1,500 rpm), swinging 0.07–0.76 V throughout, so
the probe and the converter answer. **The A/C did not lift it** in the
log (0.30 against 0.30), though the owner read about 0.6 with the A/C
and 0.2 without during the warming idle, and the display calmed with it
(`IdleHealth` 130–140 loads off, 90–100 with the A/C; *owner*). The
front probe swung normally, 0.32–0.47 V in 20 s means, 033's regulation
within ±1.5 %. **041**: heaters 27–31 Ω front and 22–24 Ω rear, both on
— inside 6.4–47.5 Ω (`vcds.md`), so **not a weak heater**. 032 −7.8 /
+7.0 %, 055 −1.17 g/s, unchanged; the fault memory empty before and
after. **Read** (*reasoned*, corrected 10/11): **the mean mixture
reaching the converter runs lean at every idle** — that much the
sinking says, the rear probe's heater being good — **but not by how
much, nor why** (*What the rear probe can and cannot say*, below).
**For H11, not proof.** *Until 10/11 this said that a converter's
store filling at idle's small flow on a correct mixture looks alike;
it does not: the store gains oxygen only while the mean is lean.*

**The reading after the swap, 10/11** (`plan.md` 8c, done;
`vcds/vcds-step8c-after-001-033-036.csv` and `-after-2-` — VCDS dropped
at the start — `-after-adaptations-041-032-055`,
`-drive-014-033-036`, `-drive-end-adaptations-032-055`, and the fault
memory files beside them; a cold start at 11:36 local after about 3½
hours standing, coolant 18 °C, the garage door open; the phases of 9/11
night step for step, then the drive on with 014 033 036). The rear
probe, 036 field 1; *jumps* the share of successive ~1 s samples more
than 0.2 V apart; `IdleHealth` and `Misfires` off the display (*owner*):

| phase (10/11, local) | coolant °C | rear V | above 0.45 V | jumps | 9/11 night, rear V | `IdleHealth`, `Misfires` 10/11 | 9/11 |
|---|---|---|---|---|---|---|---|
| warming idle, 11:36–11:46 | 21–78 | 0.59 (0.44 the first minute, the heater warming) | 89 % | 0 % | 0.51 (from 74 °C) | — | — |
| loads off, 11:46–11:49½ | 78–94 | **0.60, flat** | 100 % | 0 % | 0.40 → 0.30 | **120–140, then 112–120**; 13–14 | 130–140 |
| the A/C, 11:49½–11:52¾ | 94 | **0.59, flat** | 100 % | 0 % | 0.30 | **70, then 66–75**; 3–4; 80–90 / 9 at its end | 90–100 |
| loads off, to 11:54:45 | 94–96 | **0.59, flat** | 100 % | 0 % | 0.15–0.24 | 98–120; 8–12 (the whole phase) | — |
| loads off, from 11:54:45 | 96–94 | **0.28, the front's swing** | 29 % | 53 % | | | |
| 1,500 rpm, 1 min | 93–94 | 0.35 | 37 % | 39 % | 0.26–0.38 | — | — |
| idle, loads off | 94–99 | 0.56, flat | 93 % | 9 % | 0.58 → 0.42 | 70–99; 7 → 5 | — |

**The drive on** (12:01–12:30, about 29 minutes, the first time the
rear probe was read under load): in the steadier minutes **0.51–0.59 V
with the tenth percentile at 0.28–0.57**, down to 0.00 on every
overrun (the fuel cut); 033's regulation within ±2 %. **014: seventeen
single counts of 12–16** at 1,500–2,900 rpm and 13–27 % load, each in
the sample where detection switches off or on at a lift — S3's known
shape (*What the number is*). **The warm stop at the end** (12:27:15–12:30:19,
the everyday state, the A/C off, oil 101–102 °C): the rear probe flat
at 0.57 V from arriving to about 12:28:10, then **spells of the front's
swing between flat spells**, lean side only (never above 0.57) —
over the stop a mean of 0.48 V, the last minute 0.45, jumps 15 %, never
under 0.2 V for more than 3 s; `IdleHealth` **60–70, 55, 70, 50–55, 48,
then 80–90**, `Misfires` 7, 5, 3 (*owner*); **014 twelve misfires in
about 3 minutes, 0.24 % of combustions** (S3; *the laptop session's
note said zero for the whole drive, which the log does not bear out*).
**032 −6.3 / +5.5 %** after the drive, from −7.8 / +7.0 that morning
— each cell two VCDS steps towards zero on kept adaptations; 055
−1.18 g/s; **041 26.8 / 21.7 Ω**, both heaters on; the fault memory
empty before, after and at the end.

**Read** (*reasoned*):
1. **The rear probe changed.** On 9/11 it sank in the first loads-off
   phase and did not come back above 0.45 V at idle; on 10/11 it held
   **flat at 0.59–0.60 V — the healthy shape** (*How a healthy rear
   probe looks*, below) — through the warming idle, loads off, the A/C
   and two minutes more, about 18 minutes of idle, and again at the
   last idle and for the first 1½ minutes of the warm stop. **So the
   old probes carried most of the lean mean** behind the front probe.
   Which of the two is not known: both were changed at once (*the
   owner's decision*).
2. **It did not hold.** At 11:54:45, 18 minutes into the idle, the rear
   trace became the front's within one sample — 0.07–0.78 V in step with
   it — with nothing changing in 001 or 033 (coolant 96 °C, the
   regulation ±2 %, the radiator fan not heard, *owner*); the 1,500 rpm
   ended it. A store filling on a lean mean passes the lean side only
   (*The sinking is the converter's shape*); **peaks to 0.78 V, above
   the flat level, say rich gas passing too**, which a full store alone
   does not give. What did it is *not known*: 036 field 2 went from
   `zap.` to `OK` 2½ minutes later (`vcds.md`), and whether the ECU
   tests the rear probe or the converter at a warm idle by moving the
   mixture is not known. At the warm stop the spells came after 1½
   minutes and kept to the lean side.
3. **The idle did not change.** Loads off **112–140** against 130–140
   on 9/11, **with the rear probe flat at 0.60 V the whole phase**;
   **the A/C calmed it as much as before** (to 66–75, about 50 lower)
   with the rear probe flat in both phases; the warm stop 48–90, against
   57–63 at stop 7 of 9/11 and 48 ± 3 on `43`. **So the idle was as
   rough with no lean mean behind the front probe as with one** — the
   A/C's against (*Against, the A/C*, below) now holds on both sides:
   **the lean idle of 9/11 was not the roughness's cause.**
4. **032** moved two steps towards zero in one drive. Mark 1 was not
   read then; the battery disconnect that followed made it a clean
   relearn, read that evening: it failed (*The relearn drive*, below).

**What else could have shaped it** (10/11 midday, *the owner's
question*; *reasoned*, each with what the next drive says):
- **032 still at the old probe's −7.8 %** — the owner's hypothesis
  (below, after the relearn); against it, the live correction centred
  on zero; the relearn reads it.
- **The display read by eye and one warm stop.** `IdleHealth` off the
  display is a running figure, and one stop is within the spread
  between stops (S1's table: 48–93 settled on the same day); the dips'
  share and the steady pattern were not read at all. The capture of 8d
  read them: no change, and 3 leading again (*The relearn drive*,
  below).
- **The standing phases on part-warm oil**: 54 °C at the start of loads
  off, coolant 78–99 °C, against 9/11 night's start at 73 °C of coolant
  (oil not read then); the idle is roughest cold (S1, *Temperature*), so
  those phases compare with 9/11 night only, never with a warm stop.
- **New probes run in**: whether a new probe reads differently over its
  first hours is *not known* for these parts; the rear one's flat 0.60 V
  in the first 18 minutes argues it worked from the start.
- **The rear probe's switch at 11:54:45** — nothing in 001 or 033 at the
  sample: the live correction moved from about −0.3 to −0.6 %, within
  its noise; the front's switching unchanged. Left: **the converter
  cooling over a long idle** (its storage falls with temperature, and
  the switch passed rich and lean alike, ended by the 1,500 rpm and
  returned only after 1½ minutes at the hot stop — which fits the cold
  standing better than the hot stop); **purge** (N80 opens on a warm
  engine, its vapour reads rich), not visible in 001 at VCDS's ~1 s; the
  ECU's own check of the rear probe (036 field 2's `zap.` → `OK`); a
  probe seated loose (8e). None told apart.
- **The day before**: the hydrogen clean of 9/11 changed cylinder 3, so
  a stop on 10/11 compares with stop 7 (57–63), not with stops before
  the clean.

**The five marks at the first stop** (12:27): **1** not read then (−6.3 %; failed on the relearn drive, below);
**2** met in the first loads-off phase and, at its limits, at the stop
(0.09 V lower at the end, a mean of 0.48, jumps 15 %), failed in the
last 1½ minutes of the second loads-off phase; **3 failed** (48–90, not
at or below 40); **4 failed** (the A/C still about 50 lower); **5** not
read, no capture. By the *Read* under the marks, **2 without 3–4: the
old probes were faulty, or a part of what made the lean mean, but not
the idle's cause** — one stop of the three the marks ask for, and mark
1 still to come.

**The relearn after the battery disconnect, 10/11** (*the owner*:
disconnected after parking at work, to see whether 032 goes back to the
large negative values and whether that moves the idle; `plan.md` 8d).
032 starts again from 0.0 / 0.0 on the new probes, and 055 too if the
battery was off for hours (`idle-log.md`, 27/10: a minute does not reset
it, hours do). **On the old probes the idle cell was back at −6.3 %
after one drive both times it was reset** — 27/10 (hours off) and 3/11
(the map) — and settled at −7.0 to −7.8 % (S19). So the drive from work
with 032 logged reads mark 1 directly: **back to about −6 % within a
drive or two → the idle cell is not the old front probe's**, and what
is left for S19's split is the hydrogen of unequal cylinders (cause 2)
or a fuel cause (H7, H16); **staying within ±3 % over the next drives →
the old probes made it** (mark 1). Either way the owner's note stands
beside it: **the idle was rough at −4.7 % in the summer too** (*owner*,
10/11; the cell's history in *Re-read 9/11 evening*, above), so mark 1
alone says nothing of the idle; marks 3 and 4 do. A quiet 014 after a
disconnect is no evidence (`refuted.md` C19's rule), and 055 relearns
at the first warm stops, so the stop at the end is read with 055
settled.

**The owner's hypothesis for the relearn** (10/11): the idle is a burn
at the edge, and **the negative idle cell the old probe taught may
itself keep the mixture lean**, so the idle may settle only once 032 is
near zero — which one drive on kept adaptations did not reach. **Against
it** (*reasoned*): in closed loop the learnt value only sets where the
live regulation starts; the mixture follows the probe. On 10/11 at idle,
with the cell at −7.8 %, **001's live correction centred on −0.1 %**
(−4.7 to +3.9, 11:47–11:56) and the new rear probe sat flat at 0.60 V,
so the mixture the new front probe asked for was reached, and the idle
was rough at it. The learnt value acts directly only where the loop is
open: the first 40–100 s after a cold start and the return from an
overrun cut. **The drive tests it either way**: the idle cell starts at
zero, so the first warm stops are the idle with 032 near zero; **rough
there as well, and the cell sinking again**, says the cell is not the
idle's cause (*the owner's criterion*, 10/11).

**The relearn drive, 10/11 evening** (`plan.md` 8d, done; `47`, `48`,
`vcds/vcds-step8d-*`; read in a cloud session the same evening;
`idledips.roughness()` per stop and per minute, *ad-hoc scripts, not
kept*, for the rest; the cylinders re-read 12/11 with `cylscan.py`). 098 by the owner, the fault
memory empty, **032 and 055 all zero before the start** (the battery
off for hours); started 16:21:36; a mild drive in the everyday state,
queues 16:29–16:41 and 16:51–17:17, **the A/C on 17:06–17:09 and
17:22–17:27**, a brisk stretch to about 5,000 rpm 17:23–17:29, the warm
stop from 17:30, the A/C off, **the hazard lights on from arrival**
(*owner*, said after the reading), **no cut** (the engine cover on).
**The hazard lights show in the stop's engine speed**: a line at
1.27–1.28 Hz, the flasher's rate, absent at the queue stops, about
1.5 rpm over the stop's first seven minutes and 5 rpm in its calm end
(a sine fitted to the detrended speed; *ad-hoc script, not kept*); a
swing that size moves engine speed by about 0.3–1.6 rpm between two
0x280 updates, under `IdleHealth`'s 3 rpm dead band, so it adds little
to the grade (*reasoned*), and it was on from the first minute, so it
did not bring the calm.

| 10/11 (local) | oil °C | 032 idle / part, % | `IdleHealth` | rear probe (036) |
|---|---|---|---|---|
| cold start, 16:21:36–16:23:25 | 44–46 | 0.0 / 0.0 | **91, then 104** | 0.44 (heater warming) |
| the queue, 16:29–16:41 | 77–98 | −0.8 → −3.9 / +4.7 | no settled idle (creeping) | 0.5–0.6 at the stops, 0.00–0.76 driving |
| queue stops, 16:51–16:56 | 99–102 | −4.7 / +6.3 | 63, 91 | 0.48–0.54, flat |
| queue stops, 16:57–17:05 | 102 | **−5.5 → −6.3** / +6.3 | 82, 92, 63, 49, 55 | **sinking, 0.39 → 0.24** |
| the A/C, 17:07:42–17:08:31 | 102 | −6.3 / +6.3 | 52 | 0.55 |
| queue stop, 17:16:17–17:17:11 | 102–103 | −4.7 / +6.3 | 71 | 0.25 |
| the warm stop, 17:30–17:38, per minute | 104 → 102 | −3.9 / +7.0 | **59, 57, 52, 54, 65, 66, 84, 70** (64 over it) | **0.00–0.14** (S23) |
| the same stop, 17:38–17:42:50 | 102 | not read after 17:34 | **45, 43, 38, 39, 36** | not read |

- **Mark 1 failed: the idle cell is not the old front probe's.** From
  zero it went to −3.1 % in 12 minutes, **−6.3 % at 16:58, 37 minutes
  in**, held there to 17:09, then −3.9 to −4.7 % to the end; the
  part-load cell moved first and furthest, **+7.0 %** from 17:24.
  **−3.9 / +7.0 %** at the stop (17:34), 055 **−0.91 g/s**. As on the
  old probes after both resets on record — so the split of S19 does
  not come from the old probes; what is left for it is cause 2 (the
  hydrogen of unequal cylinders), H7 and H16 (*The relearn after the
  battery disconnect*, above).
- **The owner's hypothesis was not reached warm.** The cell was at
  −4.7 % before the first settled warm idle (16:51); at zero only the
  cold start ran, **91–104 at 44–46 °C of oil**, as `42`'s 98 ± 3 at
  50–61 °C. **Rough there, and the cell sinking again** — his
  criterion's "rough and sinking" holds, but on a cold idle, which is
  rough anyway (S1, *Temperature*). But see the calm at the end, below.
- **Mark 3 failed**: the warm stops 49–92, the stop at the end 52–84
  per minute, against 57–63 at stop 7 of 9/11 and 48–90 on the display
  that morning — no change. **Mark 4, one stop**: the A/C read 52
  against 49 and 55 at the loads-off stops either side, **the first
  time it did not calm the idle** — but those stops were already at
  the level the A/C usually brings it to (S1's table: 45–65), so it
  says load brings the idle to about 50, not that the margin is back
  (*reasoned*). A stop after the queues (49–92) and after the brisk
  stretch (52–66 for its first six minutes) do not differ by more than
  the stops among themselves.
- **Mark 5 failed: cylinder 3 is the weak one again** (`cylscan.py`,
  12/11; S1, *Every stroke named*): **73 % of the weak strokes** against
  38 % on `46`, its deficit −9 to −17 % a stop and swelling to −26 % in
  the warm stop's seventh minute. **The clean's effect on 3's misfires
  lasted a day.** *Read 10/11 with the dip shares — "41 % of the warm
  dips named by the strongest slot, its steady deficit back level with
  4's" — withdrawn 12/11.*
- **Mark 2 cannot be read from 16:57.** The rear probe held 0.48–0.54 V
  flat at the first queue stops, then sank at every idle — **but its
  ceiling fell with it, under load as well** (S23): from 16:57 it never
  read above 0.44 V, even at 75–97 % load, where before 16:50 it reached
  0.67–0.76 V at every high load, and from 17:29 it read 0.000 V at 93 %
  load. A probe in rich full-load gas cannot read zero (*general*), so
  the signal itself failed (S23); **its readings from 16:57 say nothing
  of the mixture**, and the warm stop ran with the ECU seeing a lean
  rear probe (how this ECU's rear loop answers that at idle is *not
  known*).
- **The calm at the end of the stop** (`47`'s last two minutes and
  `48`'s first three): in 20 s windows `IdleHealth` **73, 55, 55, 41,
  47, 42, 42, 35** from 17:37:18, then **31–43** to 17:42:50, when the
  revs for 034 began — **the calmest warm idle captured outside the
  provider's gas** — the display once touched 37 in the everyday state,
  for a moment (23/10 evening, S1's table); here it held for four
  minutes (S1), `Misfires` 0–3 a minute; **cylinder 3's deficit fell
  in one step from −22 to −9 %, its weak strokes from 11 a minute to
  1–3** (`cylscan.py --minutes`, 12/11; *this said "3 gave no named
  dip, 0 of 13" until then*), the dips 4.1 per 1000 strokes against
  8.1 in the stop's first eight minutes, the steady pattern about half.
  Nothing in the frames changed with it: idle
  speed 790–800 rpm, 0x280's load 24–27, coolant 97–100 °C, as before.
  **The VCDS reads around it**: 030/033/036 17:37:21–17:37:42, 041
  17:38:39–17:39:00. **When P0137 was cleared, from the bus**: the
  owner remembered it as in 17:38–17:42, before the tests, not surely
  (*owner*, 10/11 evening). **VCDS sends 0x200 each time it opens a
  session with the ECU** (`docs/firmware/can-decoding.md`), and the
  unfiltered capture (release `raw-captures`) carries one at every
  connection: 17:34:03.9, 17:36:59.0 and 17:38:23.0, 16–22 s before
  the tool's three files; **17:40:04.7, a session no file of the tool's
  belongs to — the owner's, by hand, for the clear and then the basic
  settings**; 17:49:57.9 before the fault memory read at 17:50:25. No
  session opened between 17:38:23 and 17:40:04. **The basic settings
  show on the bus too**: 0x480 b1 carries 0x20 from **17:41:44 to
  17:47:58** in `48` and at no other time of 47–48 but the crank
  (*reasoned*: it begins at a plain idle a minute before the revs for
  034, whose photo is 17:44:31, and ends between 037's photo, 17:47:45,
  and 036's as a measuring block, 17:48:46; `20` carries it too, after
  VCDS was reconnected; whether it is the basic-settings state itself
  or a lamp it lights is *not known*). So **the clear fell in
  17:40:05–17:41:44, and the calm began at 17:37:40, two and a half
  minutes earlier, at a plain idle with 032 still at −3.9 / +7.0** —
  **not the reset of 032 and not the tests** (*reasoned*; *the owner*
  asked whether the catalyst test had changed something). The calm ran on into the first minute of the
  basic settings, at idle, and ended with the revs; **after the tests
  the idle was 40–66 again**, so they left nothing calmer behind. **The
  four minutes are 3's swell ending in a step** (12/11, `cylscan.py
  --minutes`; S1, *Every stroke named*), as at `40`, `43` and `44`;
  what set the step off, nothing on the bus shows.
  *Until the 0x200 frames were read this said the clear's time was not
  recorded and might have brought the calm.* **The tests of 24/9**
  (034, 036, 037, 046 all OK, `refuted.md` C5; *the owner*: they
  needed no revs then, the exhaust hot by itself) are probably `20`'s
  first 137 s: the same 0x20 on 0x480 b1, at a plain idle, VCDS
  reconnected (*reasoned*); `IdleHealth` 76–118 in them and 104–132
  after, on the old MAF's last morning — one session, nothing to
  compare with today's.
- **014** counted from 16:33, twelve minutes after the start — not
  quiet after the disconnect (`refuted.md` C19's rule did not apply);
  **0–0.58 % of combustions at the queue stops, 0.24 % over them, 0.15 %
  at the stop at the end**; on the road single counts of 12–26 at
  lifts, as always (S3).

**The four calm minutes read closely** (10/11 night, *the owner's
request*: chance, or the clean working late — the provider said its
effect shows over a few hundred km, *owner*; `47`–`48` and their
unfiltered captures, *ad-hoc scripts, not kept*; 014 was not logged
then, its log ended 17:33:15). The stop in phases, all at 795–798 rpm,
the hazard lights on throughout, the A/C off (0x288 b2 16, below):

| 10/11 | `IdleHealth` | dips / 1000 strokes | `Misfires` | named 1 / 3 / 4 / 2 | steady pattern, rpm (1 / 3 / 4 / 2) | b7 | fuel µl/s |
|---|---|---|---|---|---|---|---|
| 17:30:15–17:33:00 | 56 | 7.0 | 17 | 9 / 8 / 9 / 3 | +0.1 / −1.5 / −0.5 / +1.9 | 22.8 | 300 |
| 17:33:00–17:35:20 | 59 | 8.8 | 17 | 7 / 11 / 4 / 5 | +0.3 / −1.6 / −0.6 / +1.9 | 22.4 | 299 |
| 17:35:20–17:37:40, rough | 78 | 8.2 | 23 | 2 / **16** / 6 / 6 | +0.9 / **−2.6** / −1.0 / +2.7 | 25.4 | 316 |
| **17:37:40–17:39:50** | **46** | 7.1 | 13 | 6 / 10 / 3 / 4 | 0.0 / −0.8 / −0.5 / +1.3 | 25.6 | 315 |
| **17:39:51–17:42:50** | **38** | **4.1** | 7 | 3 / **0** / 3 / 7 | +0.1 / −0.3 / −0.9 / +1.1 | 23.8 | 310 |
| 17:46:20–17:47:57, basic settings | 51 | 8.4 | 6 | 3 / 11 / 2 / 6 | +0.1 / −1.1 / −1.4 / +2.2 | 27.1 | 344 |

- **Two steps, not one**: the grade fell at 17:37:40 (10 s windows 80
  → 29, then 35–66) with 3 still leading the dips and the dips as
  frequent; **only from about 17:39:50 did 3's dips stop and the dips
  halve**, the steady pattern at about half — to the revs at 17:42:50.
  **It came straight after the roughest part of the stop**, in which
  3's deficit was the largest of the stop (−2.6 rpm) — the shape of
  `42`–`44`'s rough start and settling, late (*reasoned*).
- **Nothing on the bus moved with it.** Engine speed 795–797 rpm;
  coolant cycling 96.8–100.5 °C about once a minute through the whole
  stop, the radiator fan's rhythm, unchanged; the fuel flow and b7 as
  in the stop's first minutes, so no sign of a cleaner burn taking
  fuel away (on the gas of 9/11 it did); **a load step at 17:36:18**
  (b7 23 → 27–29, 0x288 b6 37 → 41, the fuel +5 %) **lasting to about
  17:39:48** — under the rough part and the first calm step alike, so
  not the cause; what it was is *not known* (the A/C was off, the fan
  shows smaller; the owner does not remember what he did then). Every other identifier of the
  unfiltered capture checked byte by byte: no change at 17:37–17:40
  but VCDS's own session frames (0x200 and 0x5D0 b0, 17:38:23).
  **0x488 b3** stepped 0x8D → 0x8C 32 times, 17:29:19–17:35:17 — the
  ECU's altitude correction by opendbc's name, not the rear probe
  (`docs/firmware/can-decoding.md`, *The bus byte by byte*; *this said
  "around the rear probe's fault, meaning not known" until the survey*).
- **VCDS around it**: 033 at 17:37:21–17:37:42, just before: the front
  probe switching 0.06–0.73 V, its correction −2.3 to +1.6 % — the loop
  normal; 036 0.03–0.14 V (S23) through all of it; 041 17:38:39–17:39:00,
  heaters 25.5 / 22.9 Ω, inside the calm.
- **The clean's late effect** (the provider's claim): **by dips the day
  after is worse, not better** — the queue stops 5.6 and this stop 7.8
  per 1000 strokes against **1.7–3.8 at every warm stop of 9/11 after
  the clean** and 0.7–4.4 on `40`–`46` (S1, *The clean of 9/11*); even
  the calm's 4.1 is above stop 7's 1.7. A cleaning that keeps working
  would show as later stops calmer than earlier ones, with 3's share
  falling; one day says the reverse. *Not ruled out* over hundreds of
  km — item 6's stops over the coming weeks read it (8b's capture dropped 11/11).
- **Read** (*reasoned*; *the owner*, 10/11 night: left as an anomaly,
  a few calm minutes, not pursued): **chance, or this stop's own late
  settling** —
  the best four minutes on record in the everyday state, but neither
  the clear (17:40:05 at the earliest) nor the tests, nor any load or
  temperature the bus shows, came with them, and the clean's effect is
  read the other way by the same evening's dips.

**Read** (*reasoned*): **the idle cell came back on the new probes as
on the old, so mark 1 is gone; marks 3–5 failed again; mark 2 is
spoilt by the rear probe's own fault (S23).** H11's idle form has no
mark left standing: the calm of 17:38–17:42 came before the clear that
reset 032, so it is not the owner's hypothesis at work. **The rear probe fault (S23) is new and the new probe's
own** — a lead, a connector or the part — not evidence that the old
one was right.

**What the rear probe can and cannot say** (10/11, *the owner's
question*; *general* and *reasoned*). **The oxygen a converter stores
grows with (λ − 1) × the exhaust's mass flow** (the integral the
storage-capacity measurements use, e.g. US 8 225 649): on a mean of
exactly λ = 1 the store swings about one state and does not drift, so
a rear probe sinking over minutes means a lean mean behind the front
probe. **Its size is not read**: a narrowband probe only switches, and
a fresh converter's store (of the order of a gram of oxygen at most;
this one's is *not known*) fills at idle's ~3 g/s of air in 5–10
minutes on a mean only 0.1–0.2 % lean, as on one 5 % lean, faster.
**Four causes give it, and the rear probe cannot tell them apart:**
1. **the front probe reading rich at idle** — this hypothesis, the only
   one of the four that also gives 032's negative idle cell;
2. **hydrogen from unequal cylinders** fooling the front probe
   (*How a probe can read rich at idle only*, below) — which fools a
   new probe as well;
3. **air drawn into the exhaust between the front probe and the
   converter** (H2, its second zone): the front probe sees the true
   mixture, the converter gets air besides — the rear probe's reading
   in full, but neither 032 nor the dips;
4. **a small lean bias of the front loop by design** that the rear
   probe's second loop does not trim at idle — whether M5.9.2 runs it at
   idle is *not known* (SSP 175 p. 28: *"within a defined framework"*);
   037 field 3 would show it, a basic setting Claude does not run.

Misfires give the opposite (*below*), and **1,500 rpm standing is not
load**: the rear probe read 0.26–0.38 V there too, so "normal under
load" has not been measured — **nor does that low reading say the
mixture at 1,500 was lean**: a full store stays full on a mean of
λ = 1, and only a rich spell empties it (*The sinking is the
converter's shape*, below; corrected 10/11). **What replacing both probes decides**
(`plan.md` 8c; *the owner's decision*, 10/11): the rear probe **not
sinking** — steady in the upper half (above the 0.45 V switching point)
through every idle loads off — and 032's idle cell falling towards
zero, say the old probes were it (1); the same sinking says the old probes
were not, and leaves 2, 3 and 4 standing — **the swap rules out parts,
not mechanisms**. A new rear probe that sinks alike rules out the old
rear probe's own fault as well. **Read 10/11** (*The reading after the swap*,
above): neither outcome cleanly — the new rear probe did not sink for 18
minutes, then switched to the front's swing; 032's idle cell moved two
steps towards zero in a drive and was then reset by the battery
disconnect, so its answer is the relearn — **which brought it back to
−6.3 % in 37 minutes** (*The relearn drive*, above).

**The old probes seen, 10/11** (both replaced that morning, `plan.md`
8c; `photos/lambda-front-old-tip-2026-11-10.jpg`,
`photos/lambda-rear-old-tip-2026-11-10.jpg`; *owner* for which is
which). **The front probe's inner protective tube is coated in a
continuous grey-beige layer, cracked like dried mud**; not white or
gritty. **The rear probe's tip is dark and clean.** Neither sooted
(rich) nor glazed (lead). *General*: such a layer is usually ash from
additives in the fuel or from oil burnt; a layer over the tube's holes
slows how fast the gas reaches the electrode — the poisoning mechanism
below (*How a probe can read rich at idle only*), worst where the probe
is slowest, at idle. **For H11, not proof**: where the layer came from
(the BG 44K tanks, oil, eight years) and whether it slowed the probe
the photo cannot say; the five marks decide (the reading after, 10/11,
above: the rear probe flat at idle for 18 minutes on the new pair). The
difference between the two fits the converter between them, the front
probe meeting raw exhaust. **The converter's outlet face**, through the
rear boss with the borescope: light grey, regular cells, nothing melted
or sooted (`photos/converter-outlet-borescope-2026-11-10.jpg`).

**Why the criterion is a trend, not 0.6 V** (10/11, *the owner's
question*). **No healthy rear-probe voltage is published for this
engine**: the label file gives 036 field 1 only its range, 0.00–1.00 V,
and 037 a verdict; VW's procedures for later engines say *"fluctuates"*
between limits not public; Bosch's service rule is only the sides, warm
*rich above 0.6 V, lean below 0.4 V*; a Bosch patent on two-sensor
control starts the rear set point at **750 mV** (US 11 428 143). **Why
the upper half** (*general*): a two-step zirconia probe reads which side
of λ = 1 the gas is on, not how far — about 0.05–0.2 V with oxygen
left, 0.7–0.9 V with none, a steep step at λ = 1 — and a converter
converts all three gases best just rich of λ = 1, so the rear set point
is chosen above the step; **where this ECU puts it is not known**. So
0.6–0.75 V is experience, not a specification, and **a rear probe that
sinks to 0.15–0.24 V and stays there is on the lean side whatever the
set point** (if it reads true). Its wide swing (0.07–0.76 V) fits a
converter full of oxygen, no longer smoothing the front loop's
oscillation (*reasoned*). **The new probes' first reading becomes this
car's own reference**; 036 was never logged before 9/11.

**The sinking is the converter's shape, not the cause's** (10/11,
*the owner's question*: would a leak not read lean all the time?;
*general* and *reasoned*). While its store has room the converter takes
up any oxygen to spare and the gas behind it stays near λ = 1, so the
rear probe reads high; once the store is full the oxygen passes and the
probe falls. **Every one of the four causes feeds a steady excess of
oxygen, so every one gives the same shape** — high, then down over the
minutes — and differs only in how fast, which VCDS's ~1 s sampling and
a converter of unknown capacity cannot read. A leak would read lean all
the time only on a store already full; this one was emptied by the cold
start's enrichment (the warming idle at 0.51 V, 70 % above 0.45) and,
*reasoned*, by the fuel that leaves the inlet walls when the throttle
shuts after 1,500 rpm (the rise to 0.58 V back at idle).

**If the swap changes nothing** (*reasoned*): the old probes are out
(1), and three causes are left, of which **only one has to do with the
idle**:

| cause | 032's idle cell | tied to the rough idle | how it is told |
|---|---|---|---|
| 2, hydrogen from unequal cylinders | stays negative | **yes**, through the cylinders' difference | only by removing the difference (H3 runner 4's gasket, H4 injector 4's circuit): the cell and the sinking shrink with it |
| 3, air between the probes (H2) | untouched | **no**, the rear probe only | the warm tailpipe test (`plan.md` 7) |
| 4, a lean bias the rear loop leaves at idle | untouched | **no**, likely every AQY's normal state | 037 field 3 (a basic setting the owner runs, not Claude): whether the rear loop acts at idle at all |

So **032's idle cell is the key**: unchanged with the same sinking
leaves, of what touches the idle, only hydrogen — back to the
cylinders' difference (H3, H4), not the probes; the other two would
explain the rear probe and nothing of the idle, and the sinking would
stop being a clue.

**What would confirm the probes as the idle's cause** (10/11, *the
owner's request*; the thresholds are *decisions*, set against the
readings before the swap). A new probe can be right and the idle still
rough — a real fault, not the idle's — so **the mechanism and the idle
are each read, and the idle's change must be the one the mechanism
predicts**. All five, over at least **three warm stops on different
days** in the everyday state, oil 95–100 °C, the A/C off, within the
first weeks:
1. **The mixture was corrected at idle**: 032's idle cell from −7.8 %
   to within **±3 %** after a few drives, the part-load cell where it
   was — the split closes (S19). This is the front probe's own mark;
   the new rear probe cannot fake it.
2. **The idle no longer runs lean**: in each idle loads off of 3
   minutes or more, read from 036 at VCDS's ~1 s — **(a) no sinking**:
   the last minute's mean no more than about 0.1 V below the first's;
   **(b) the phase's mean at about 0.45 V or above**, short dips below
   allowed, **never lying under 0.2 V** for more than a few seconds;
   **(c) flat**: a jump of more than 0.2 V between successive samples in
   at most about 15 % of them (*How a healthy rear probe looks, and the
   9/11 log minute by minute*). *Until 10/11 this said "steady above
   0.45 V through each idle", which a healthy probe need not meet: it
   may dip with the front loop and transients, and where this ECU sets
   its target is not known.*
3. **The idle is better**: `IdleHealth` at every stop **at or below 40
   from its first minute to its last** — below the best settled level
   so far (48 ± 3 on `43`, 50–63 on 9/11) and without the rough first
   minutes (86–93 on `42`, `43`); `Misfires` at the end of each stop
   near zero, 014 within VW's 0–5 when VCDS is on (S3).
4. **The patterns that a lean idle explained are gone**: a stop after a
   queue no worse than one after a brisk run (within about 10), and the
   A/C no longer calming it by more than about 10 — the load helped by
   widening a lean margin, so with the margin back it has little left
   to do. **If load still calms it as much, the lean idle was not the
   reason**, whatever 1–3 say.
5. **The dips no longer lean to one cylinder** in a capture with a cut
   (then `cutscan.py --shares`, 8b's kind; `cylscan.py` since 12/11, and
   no cut needed), and the steady pattern over the
   cylinders smaller — a correct mixture leaves a weak cylinder less
   often over the edge; *if the steady pattern is kept with the dips
   gone, the probes were the dips' cause and the cylinders' difference
   is left as this engine's spread*.

**Read**: 1–5 → the probes were S1's cause, S1 and S3 closed as such;
1–2 without 3–4 → the probes were faulty but not the idle's cause; 3–4
without 1 → something else changed (the fuel, the weather), not
confirmed; 1–4 with the steady pattern kept → the dips' cause found,
the spread left (5's note).

**How a healthy rear probe looks, and the 9/11 log minute by minute**
(10/11, *the owner's request*). **No manufacturer's figure was found**
(VW: none public for M5.9.2; Bosch's lambda brochure only the probe's
range, about 20–900 mV, and the ECU's 450 mV reference). **What the
other sources agree on is the shape, not a number** (*general*; shop
references and forums, not sources in the datasheet sense): behind a
working converter the rear probe is **nearly flat, with slow, lazy
movements**, at 0.65–0.85 V in shop references, 0.35–0.65 V or "about
half a volt" in forum reports, one Golf IV 1.6 reading 0.756 V in 036;
**a rear trace that switches like the front one is the warning** — a
converter that no longer buffers. **Per minute of the 9/11 night log**
(`vcds-step8c-before-001-033-036.csv`; *jumps* the share of successive
~1 s samples more than 0.2 V apart):

| minutes | phase | rear mean V | p10–p90 V | above 0.45 V | jumps |
|---|---|---|---|---|---|
| 0–1 | warming idle, store emptied by the cold start | 0.54–0.56 | 0.26–0.63 | 76–85 % | 9–15 % |
| 2–4 | loads off | 0.35 → 0.27 | 0.10–0.63 | 24 → 2–10 % | 3–14 % |
| 5–7 | the A/C | 0.30–0.32 | 0.10–0.65 | 32–39 % | **58–60 %** |
| 8–11 | loads off | 0.18–0.23 | 0.09–0.63 | 10–21 % | 21–45 % |
| 12 | 1,500 rpm | 0.33 | 0.09–0.67 | 39 % | 42 % |
| 13–14 | idle, loads off | 0.53 → 0.45 | 0.10–0.67 | 81 → 69 % | 32–48 % |

**Read** (*reasoned*): **the first two minutes are this car's nearest
thing to the healthy shape** — about 0.55 V, flat, few jumps — while
the store still had room; **once it sank, the rear probe began to
follow the front loop** (jumps from about 15 % to 35–60 %), which is
the full store passing the front's swing through, not a failing
converter (new on 10/9, block 046 OK on 24/9). Hence criterion 2's
three parts and their figures (*decisions*): the trend, the floor and
the flatness, each against what this log showed.

**The idle without the lambda loop** (10/11, *the owner's idea*: if the
probes made the dips, the idle should be calm whenever the ECU does not
use them). **Where the loop is off at idle, from every VCDS log with
group 001** (field 3 held at 0.0): **only the first 40–100 s after a
cold start** (`vcds-item5-drive-…-1`, `-step3-1-drive-`, `-step3-2-gauge-cold-`,
`-step6b-drive-2-`, `-step6k-2-`, `-step8-home-2-`; the loop closes at
28–42 °C of coolant), **and during every injector cut** (6d, 8b's
kind, the clean's stops) — the cut itself the larger change, so those
say nothing. **The cold-start window is calmer**: on the standing cold
starts `31`, `32`, `33` `IdleHealth` reads about 45–65 with the loop
off and jumps to about 80–110 within the next half minute, at 33–35 °C,
every time. **But the loop is not the only thing that changes then**:
on `vcds-step3-2-gauge-cold` the ECU holds a catalyst-heating idle — 920
rpm, the MAF at 5–6.5 g/s, the advance retarded to −2…−11° — and ends
it at 93 s (800 rpm, 4.2 g/s, the advance back to 0…+8°); **the loop
closes 4 s later**. A fuller charge, a faster idle and a later burn are
what calm this idle anyway (S1, the load helping), so **the calm window
fits H11 and the charge alike, and `IdleHealth`'s ~10 s smoothing cannot
split 4 s**. Full throttle (open loop, never rough) carries the load
the same way. **Not telling either way**; the comparison that does —
the reading after the swap, 10/11 — found the idle as rough with the
rear probe flat as with it sinking (*The reading after the swap*,
above). **Re-read 11/11 with the idle target decoded** (0x288 b5,
`docs/firmware/can-decoding.md`; *the owner's question* after the cold
start of 11/11; six standing cold starts, `18`, `25`, `27`, `31`, `32`,
`33`, in 10 s windows, `IdleHealth` as the mean step with no smoothing;
*ad-hoc script, not kept*): **the catalyst-heating idle ends on a timer,
100 s after the start every time** — the target 900 → 830 → 810 rpm,
the engine 930 → 820 within 10 s, the injection time down a step, b7
unchanged. **The roughness does not follow it at once**: the window
110–120 s, the speed already down, reads 42–83 (four of six under 70,
as calm as before the step); **it builds over the next 20–40 s**, to
95–171 by 130–150 s, every time. And the first 40 s after the start,
at 930–1000 rpm and the richest, were rough (100–170) — so speed and
charge alone do not make it calm. *Reasoned*: a fuller, slower charge
calms at once when it comes and roughens at once when it goes; this
roughening lags the drop by tens of seconds, as the closed loop takes
over (about 105–110 s) and its swing grows — **for the lean-edge family**
(a lean cylinder or a mis-read mixture the loop's swing pushes over:
H3, H4, H13, H11/H21) **and against a pure dilution at the lower speed**
(H1's exhaust seat, the belt's overlap), which would show at once. One
kind of event, six times; a slower change (the exhaust cooling after
the retarded burn) is not ruled out. *Not recommended now*: unplugging the front
probe at a warm idle would open the loop at the same charge, but the
ECU then runs on 032's learnt value, which a misreading probe set, and
it stores a code.

**Against, the A/C** (10/11, *agreed with the owner*; *reasoned*): **the
A/C calmed the idle but did not lift the rear probe** — `IdleHealth`
130–140 loads off against 90–100 with it (*owner*, the display), the
rear probe 0.30 V in both phases (the log; the owner's 0.6 with the A/C
read during the warming idle, before the logged phases). If the lean
idle made the roughness, a load that calms it should have made the idle
less lean too; it did not, so **the A/C's calm comes from elsewhere** —
the fuller charge (S1) — and the link "a lean idle, so a rough one" is
not shown. One reading at VCDS's ~1 s and coolant still climbing
(88–92 °C with the A/C, 78–86 before it). **Repeated after the swap,
10/11, at a steady 94 °C**: the A/C calmed the display from 112–140 to
66–75 with the new rear probe flat at 0.59–0.60 V before, during and
after it — **no lean idle to widen, and the load still calmed it as
much**, which is mark 4's failure (*The reading after the swap*,
above). *The rear probe was from 2017 as well, and might have sat a
little lean of its own; this said so until 10/11, when the new one read
0.59–0.60 V at the same phases.*

**How a probe can read rich at idle only** (9/11 night, *the owner's
question*; *general* mechanisms, which of them, if any, *not known*):
- **A slow probe, slower one way.** A narrowband probe's reading is only
  as good as its speed, and at idle its gas is coolest and its flow
  smallest. If an aged probe turns from rich to lean more slowly than
  back, it shows "rich" longer each cycle, the ECU keeps leaning longer,
  and the mean mixture runs lean — worst where the probe is slowest, at
  idle. **SSP 175 (p. 28): a change in reaction time "can be acquired,
  stored and displayed but cannot be compensated for"** — only a shift of
  the curve is, by the rear probe's loop. ⚠ The German Audi edition
  read on 11/11 says of the same change *"eine Anpassung erfolgt über die
  Nach-Kat-Sonde"* (an adaptation is made through the rear probe); the
  English edition was not reached to settle which is meant.
- **Hydrogen in the exhaust and unequal cylinders.** The probe's electrode
  sees hydrogen, which diffuses through its protective layer faster than
  oxygen, so exhaust that carries hydrogen reads richer than it is. A
  mix of richer and leaner cylinders makes exactly such exhaust, and the
  ECU then leans the whole engine — the reason engines since 2011 carry
  an imbalance monitor (*general*). This car has a steady imbalance (S1:
  4 weak, 2 strong); **if part of it is mixture — air at runner 4 (H3) —
  it is largest at idle**, where a fixed leak is the largest share of the
  air, and so would be the probe's error: a link between H3 and H11.
- **Poisoning.** Silicone, oil ash or fuel additives coat the electrode
  and slow it — **the old front probe came out with its tip coated**
  (10/11, *The old probes seen*). The idle cell's few extra points came in the window of
  the two BG 44K tanks (23–24/10) and the hours of hard driving on them
  (`vehicle-history.md`); the cell itself was negative since August, so
  poisoning would at most have added to an older offset.
- **A weak heater** leaves the probe coolest at idle; 041 reads its
  resistance — **27–31 Ω on 9/11 night, inside the specification, so
  not this** (*The reading before the swap*, above).
Misfires push the other way (their unburnt oxygen reads lean, the ECU
enriches, and the rear probe would rise), as does an exhaust leak ahead
of the probe (H2's first zone); a leak between the probes reads lean
behind the converter only (H2's second zone).

### H12. Driveline play read as misfires

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | — | ✘ | ~ | ~ | ~ | — | ✔ | ✘ | — | — | — | — |

**Against:** the MAF swap halved the dips; play repeats every 360°, the pairs
1+4 and 2+3, while the dips sit on 3 and 4, 180° apart; the puffs come with
the dips, and play makes no unburnt charge. **The clutch minutes** (12/10):
pedal up no rougher than down — not the gearbox side (S16). The crank
pulley's damper fine by eye.

*Until 27/10 evening S12 counted for this hypothesis; it turned out to be
a sticking pedal (`refuted.md` D6).*

### H13. Deposits after years of gentle driving — inlet valves, chambers, ring lands

**Re-read 12/11, the third research** (S1, *Every stroke named*):
**for.** Cold, the weak strokes fall 3 > 4 > 1 > 2 and 4 is weak beside
3 — the borescope's order of the deposit (3 > 4 > 2 > 1) but for the
last two — and warm it is 3 alone, the cylinder with the most. A
deposit that soaks fuel cold fits both cylinders cold; a seat or a
stem that carries it fits 3 warm, its swell and its step (H1).
Against: the clean left 3's floor where it was (−9 % before its cut at
stop 3's end and −7 to −9 % at stop 7) and 3 led again a day later.
**12/11 evening** (S1, *The swell's shape*): the swell read as a seat
on 3 fouling at idle and burning itself clean (H1) is this entry's
deposit at work — it fits the clean taking the swell for a day and
`46`'s stops showing no growth at all; against "a flake moved", the
fall takes 30–45 s.

*Added 15/10 at the owner's request.* The engine seldom saw more than
3000 rpm for at least nine years (*owner*). Gentle use builds deposits where
hard use burns them off (*general*).

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ✔ | ✔ | ~ | ✔ | ~ | — | — | ~ | ~ | ~ | — | — | ~ |

- **11/11, the second research**: the clean's relief lasted a day
  (`47`), and **no source gives seat deposit forming again in a day** —
  the one time base found is about 200 hours for inlet-valve deposit
  (SAE 922263) — so a flake moved, or lodged and burnt away, fits better
  than regrowth (SAE 2000-01-2858: flakes trapped by chance, water the
  strongest trigger); and **the rough start after a hot drive is 3's**
  (S1, *The rough start of a warm stop*), read with H1's exhaust seat.
  *Reasoned*.
- **9/11, the clean** (S1, *The clean of 9/11*): **after it 3's swell
  was gone at stop 7** — its weak strokes 25 → 5 per 1000, the rough
  first minutes and 014's storm absent — **for, on 3**; **3's floor
  (−8 to −9 %) and the settled level kept**, and the swell back a day
  later: against H13 as the whole story. *This bullet read "its share of
  the dips 48 % → 23 %, its steady deficit 7–14 % → 0–3.6 %, 4's
  deficit kept" until 12/11.* **With its gas flowing
  the idle had no dips at all**: the weak strokes are a burn that fails,
  which deposit makes (*general*) but not it alone. ⚠ One stop each
  side; straight after the clean 3 was still short for minutes.
- **3 the weak one at every warm idle** (S1, *Every stroke named*; `43`
  −13 %), the one ranked first inside (3 > 4 > 2 > 1): for, though
  deposits act on all four in kind. **A hydrogen decarbonisation was
  done before**, 10/8/2021 (`vehicle-history.md`), its effect not
  remembered; the deposits of 10/2026 built up since. **The owner's
  reading of 3/11** — every cylinder dips, 3 the most, so a cause on
  all four with 3 worst; all four alike just after the VW leads and
  plugs, 3 worse again two weeks later, a cylinder that burns badly and
  wears its new plug down — **keeps its first half and loses its
  second**: the small unevenness is on all four (the common part) and
  3 is worst, but 3 was not even on `40`–`41` (−14 %, 64 % of the
  weak strokes on `40`), so nothing grew worse on 3 after the leads
  (*re-read 12/11*). The plug 3 beside the others would still show
  whether it wears (the 10/10 plugs read 3 the
  cleanest after nine days, `vehicle-history.md`), and **its gap with a
  wire gauge** at the same time (`refuted.md` A2, reopened for plug 3
  alone, 3/11). It costs the plenum off; **not for now** (*the owner*,
  3/11).
- **The look inside, 19–20/10** (H13 test 3, `idle-log.md`): **no inlet valve
  back is coked** — thin lacquer on all four, so no walnut clean; **the
  chambers carry it** — thin layers on every crown, a crust on 4's bowl edge,
  and **on 3 a layer breaking up, crown and exhaust valve alike**. Ports and
  chambers rank **3 > 4 > 2 > 1** — 3 the weak one warm, 3 and 4 cold.
- **Consequence more than cause** (*the owner's reasoning*, 20/10): every
  cause put forward for deposits acts on all four alike, and 3 and 4 are
  worse — so their extra deposit reads as **years of poorer combustion on 3
  and 4**, from something that touches those two only (`refuted.md` C24). Once there, the
  deposit adds to it: a flake under a seat (18/10, `refuted.md` D10), heat and compression for
  knock on 4 (S4).
- **The inlet side, 7/11** (*the owner's reading*, H1): the crust at the
  seat ring's edge in the ports of 3 and 4, a lump standing out of it on
  3, 1 and 2 thin and even. **What the clean of 9/11 can reach**
  (*reasoned*): hydrogen burns in the chamber; the port above a closed
  inlet valve sees only the incoming charge, so deposit on the inlet
  side, the seat ring's upper edge included, is the least likely to go. The gas does pass the ports — it goes in behind the MAF
  (*owner*) — but cold, hydrogen and oxygen do nothing to carbon; what
  can clean is the flame and its steam, in the chamber (*general*; the
  vendors' chemistry above).
  So if 3 stays weak after 9/11, the inlet seats are left standing
  (H1), and the leak-down is the test. **9/11: 3's floor kept at stop
  7, its swell gone for a day** (S1, *The clean of 9/11*) — the inlet
  seat left standing is 3's. *This read "3 not weak at stop 7, 4 still
  is — the inlet seat left standing is 4's" until 12/11.*
- **4/11, the two patterns on their own** (S1; *reasoned*, agreed with
  the owner): with H1's exhaust seat on 3, **the one reading that fits
  both** the calm under load and the calm that lasts after revving
  (H1). **What 9/11 should then show**: loads off nearer loads on, and
  queuing nearer the drive after revving. *Not read 9/11: no stop after
  the clean had the A/C or a queue; the display's stops will.*
- **4/11, the owner reads coarse deposit up to the edge of 3's exhaust
  seat** on the photos of 20/10 (H1): for, the contact line itself not
  seen.
- **With a cleaner in, the idle after high revs starts calm and worsens
  over minutes; without one, the reverse** (S1, *After high revs*): one capture and one display evening, so far.
- **18/10 has not come back** in six days of hard driving, a strong 44K
  tank among them (`refuted.md` D10) — what a flake that burnt off does.
  Weak: one episode, and its absence.
- **The steady pattern over the cylinders, re-read 12/11** (S1, *Every
  stroke named*): warm 3 alone gives less, 4 level, 2 and 1 above; cold
  4 weak beside 3, the weak strokes 3 > 4 > 1 > 2 — the borescope's
  order but for the last two; and 3's swell moves over minutes, as
  deposit that soaks and gives back fuel would (*reasoned*): for. *It
  read "warm 3 and 4 give the least", and "cold both spread over all
  four", until 12/11.*
- **Against:** a detergent premium fuel since 2017; compression even;
  **the strong first 44K tank changed nothing** (23–24/10, *owner*): about
  450 km on it, hours above 4000 rpm, and `IdleHealth` at the warm stops
  70–80 as before (S1, the table). The owner now expects the cleaner to do
  nothing for the idle (24/10).

**Tests:** the cleaner and hard driving (a tank from 15/10, done; two tanks of
BG 44K, **the second run out 29/10, the idle no calmer at its end** —
everyday about 70 on 27/10 and 70–100 on 28/10 (S1's table); the
EPR flushes and fresh oil, done 26/10).

### H14. The remap of 6/2018 — at full load only (S4, S19's part-load cell)

*Added 16/10 at the owner's request as the idle's ignition or its margin;*
**the idle half refuted 3/11** by the tuner's files and the drive on the
original map (`refuted.md` C23, *agreed with the owner*). What is left is
what the remap did change: the corner of highest load.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ✘ | — | ✘ | ✘ | ~ | ✘ | — | ✘ | ✘ | ~ | ✘ | — | — |

**What the remap changed** (the two whole flashes from the tuner, 3/11;
compared byte for byte, the files not kept here; the tables with every
cell in the owner's private artifact *Beetle AQY remap diff*). Both
images carry the same identification, `06A906018EJ … 0261206327
1037352075 … M5.92`. **462 bytes differ**: 257 are erased flash (0xFF)
written 0x00 after the calibration, most likely the tuning tool's
checksum area, and **205 sit in five 16-point tables**, every one of them
only in its **last three or four columns and from the fifth row down**:

| table (address, size) | by its shape (*reasoned*, no map definition) | the remap |
|---|---|---|
| T1 (`0x09C03`, 16×16) | a fuel factor, values about 128 = 1.0 | **−6 to −7 counts, about −5 %** |
| T2 (`0x09E09`, 16×16) | a fuel factor on other inputs | **−4 counts, about −3 %** |
| T3 (`0x0B750`, 16×16) | ignition advance, rising with speed, falling with load | **+1 to +4 counts** |
| T4 (`0x0B8C6`, 16×12) | a smaller ignition table | **+1 to +3 counts** |
| T5 (`0x0B9AA`, 16×16) | a second ignition table, a little higher than T3 | **+1 to +5 counts** |

Taking the rows as engine speed and the columns as load, which is how the
advance tables fall: **less fuel and more advance at high speed and the
highest load, nothing anywhere else.** At Bosch's usual 0.75° a count,
+0.75 to +3.75° (*general*; this ECU's scale not read). **Not touched**:
the idle region of all five, and every other byte — so not the idle
speed, the idle advance, the misfire detection (route 6), the limiter,
the overrun cut or the MAF's curve (`refuted.md` C22). A classic mild
remap of a naturally aspirated engine. The axes are stored as
increments; no map definition for this software is public (searched
3/11; the image names its source `DAMOS39M / 39M02G3-S`).

**The axes, fitted** (3/11, *reasoned* from measurement): T3 laid over
the advance VCDS 003 read on the original map (`vcds-step5a-*`, 1,642
samples without knock retard, 16 full-throttle points at 2500–6250 rpm).
**Rows: 40 rpm a count** (the full-throttle line fits to 0.85–1.1° RMS;
part load alone gives 42). **Advance: 0.75° a count, offset about −25°**
(a free fit gives 0.8–0.9; 0.75 with −24 to −26.5 fits nearly as well,
and part load alone gives −25). **Load: full throttle sits at about 120
counts of the column axis** (115–130); at the usual 0.75 % a count
that is about 90 % relative fill, which is assumed, not fitted. Read
that way:

| table | the change begins at | full throttle at ≈120 | reached |
|---|---|---|---|
| T1 fuel −5 % | 1400 rpm, column 90 | between columns 110 and 130 | **yes, wholly** — and heavy part load (≈108) too |
| T2 fuel −3 % | other axis types, units not known | — | not known |
| T3 advance | 1880 rpm; column 130 (+1), 140 (+2), 160 up (+4) | just below 130 | **practically not**, half a count at most |
| T5 advance | the same columns | just below 130 | **practically not** |
| T4 advance | 1880 rpm; column 110 (+1), 120 (+2) | on 120 | **yes, +2 counts ≈ +1.5°**, if the ECU uses it |

So **the advance at full throttle reads the same on both maps because
the added advance lies above the load the engine reaches**; and **T1's
leaner fuel reaches full throttle and heavy part load**, where the
lambda loop runs and the multiplicative cell of 032 would learn it back
— the remap's +5.5 to +8.6 % (S19). T4's lower values fit a knock-safe
table that advance falls back to; raising it would let more advance stay
under knock, which fits cylinder 4's deeper retard on the remap
(*reasoned*, not settled).

**What the remap was worth** (*the owner's question*, 3/11; *reasoned*).
At full throttle the lambda loop is off, so T1's −5 % did reach the
mixture there — but **the learnt multiplicative trim (032's part-load
cell) is applied in open loop too** (*general*, Bosch Motronic), and on
the remap it had learnt +5.5 to +8.6 %, so at full throttle it gave back
most or all of what T1 took, as far as that cell was T1's and not the
MAF's. The added advance lies above the load the engine reaches (T3,
T5); only T4's +1.5° is reached, if that table is used. **Measured**:
the same full-load air, advance and b7 plateau on both maps. So **the
gain was small to nothing on any channel read here**; what is not read
is the full-load lambda itself (no wideband probe) and T2's inputs, and
there was no dynamometer.

**Where it still reaches** (*reasoned*):
- **S4**: more advance and less fuel at full load is what makes knock;
  on the remap cylinder 4 retarded to 11.2°, on the original to 6.0° on
  3/11 — **and to 12.7° on 12/11**, mostly at 3,500–4,600 rpm where the
  two maps' advance is the same (S4, *Since 12/11*). *This said "the
  remap deepened 4's retard" until 12/11*: the depth is not the map's;
  it did not make 4 the one that retards either.
- **S19's part-load cell**: +5.5 to +8.6 % on the remap, +3.1 after one
  drive on the original, +3.9 after two, **+6.3 on 6/11, settled**
  (S19). If T1/T2's leaner corner reached loads the lambda loop runs at,
  the cell would have fallen to about +1 to +3 on the original map; it
  did not, so **the map does not explain it**.
- **Against both**: VCDS 003 reads the same full-load advance on both
  maps (below), so either the engine does not reach those columns, or
  knock control takes the advance back.

**The pulls of the second drive, 3/11 evening** (`43`,
`vcds-step5b-pull-014-003-020.csv`; the pull in 4th asked for the
converter, `docs/firmware/can-decoding.md` question 8): two in 4th from
2,250–2,380 rpm to 5,760 at 91–97 °C of oil, then full-throttle runs in
2nd–5th at 101–105 °C. **The pulls in 4th were short of air**: 33.6 g/s
at 2,400, 66 at 4,500, 74 at 5,000 and **flat at 75–76 g/s from 5,000
up**, against `42`'s 76 / 82–83 / 85–87 and this drive's own later
runs, 79–81 at 4,500 and 86–89 at 5,200 (`vcds-step5b-warm-014-055-003.csv`);
the advance 1–5° higher, as a lower load asks. **b7 155 at 2,400 and
167–171 from 4,000 to 5,200**, against 169 and 183–187 on `42`'s first
pulls and 185 and 192–198 on `19`; the later runs read 192–196 at
4,500–5,000, as `42`'s and `19`'s did. So 2,400 rpm was held long enough
but not on full air: **the torque scale is neither confirmed nor moved**.
`42` showed the same in kind, smaller (its first runs 181–192 against
196–206 later, on 5–11 % more air, `idle-log.md`). **What admits less
air on the first pulls of a drive is not read**: no group logged has
the intake air temperature, and a MAF reading low would lower b7 the
same way, since the ECU computes b7 from its load (*reasoned*). **Not
pursued, not a symptom** (*the owner*, 3/11): perhaps the engine needs
to be warm for longer before it takes its full air; he felt the pulls
of this drive weaker too.

**The ECU** (`vcds.md`): Bosch M5.9.2, hardware `0261206327`, software
`1037352075` V04, 256 KB flash. No map definition is public.

**The drive on the original map, 3/11** — the measurements behind
`refuted.md` C23 (`42` and `vcds-step5a-*`, fresh adaptations), on
what the cleaner and the adaptations cannot move:

| | remap | original map, 3/11 |
|---|---|---|
| warm idle advance (`idleadvance.py`) | median 3.0–3.8°, p10 0–0.8, p90 6.0–6.8 | **3.0°**, 0.8, 6.8 |
| full-load advance, 3500 / 4500 / 5000 / 5500 rpm (003) | 19.5 / 21.8 / 22.5 / 23.6° (`40`) | **19.5 / 21.0–21.8 / 21.8–22.5 / 24.0–25.1°** |
| full-load air, the same speeds | 58 / 77 / 81 / 88 g/s | **55–56 / 76 / 82–83 / 85–87 g/s** |
| b7 at full throttle in 3rd, 4000 / 4500 / 5200 rpm | 187 / 192 / 187 (`40`) | **185 / 189 / 187** |
| the overrun cut (`coastscan.py`) | 0.8–1.6 s after the lift, back at 1,300–2,400 rpm | **0.76–1.39 s, back at 1,463–1,848** on the coasts that ran down to idle |
| 014 at idle / under load | counting / 15 in about 4,300 | **0 / 0 in 1,388** |
| 020, cylinder 4 at full load | 40 %, to 11.2° (`40`) | **41 %, to 6.0°** (S4) |
| `IdleHealth`, warm | 80–105 on the display (28/10–2/11), 61–67 on `40` | **54 ± 3** settled into a stop, 63–77 near home |

**Read** (*reasoned*): **the advance, the air, b7 and the cut are the
remap's to within a VCDS step**, at idle and at full load. **014's zero
and `IdleHealth` inside the stop are not the map's**: the files show the
idle region and the detection untouched, so they are the fresh
adaptations or the engine on the day; 5b read them again: **014 counted
on `43`** at `42`'s load, so its zero was the fresh adaptations (S3). The idle cell
of 032 came back at once (S19), so the split is not the map's either.

### H15. ~~The aftermarket leads (and plugs) — NGK plug ends that grip loosely~~ — refuted 4/11, `refuted.md` C24

### H16. The purge valve N80 does not seal — fuel vapour into the intake

**Re-read 12/11, the third research** (S1, *Every stroke named*; S3):
**the misfires 014 counts are cylinder 3's, and every line joins the
intake in its common part** (H3, *owner*, 4/11), so the purge path
cannot make them by itself; what it can do is move the mixture of all
four and tip the one cylinder that is already 9 % short. **So the two
calm nights on the canister are read by cylinder**: if the captured
stop shows 3's deficit at its floor with no swell, the canister took
away what tips 3; if 3 swells as before and the stop is calm all the
same, the calm is in the small steps on all four.

**12/11 evening, the common part by capture** (S1, *The swell's shape,
and what the common part follows*): **2.7–3.1 rpm rms at every warm
idle since 24/9, within 5 %** — the bypass and the canister alike
(`48` 3.1, `49` 3.0), gentle days and brisk. **Against the purge path
as the common part's cause** in the form of *The owner's reading,
12/11* below: a leak that follows the canister's load would move it
from day to day. **For 3's swell the purge phases are kept as a weak
fourth reading** — the one slow ramp with a quick shut-off the ECU is
known to run, not on the bus; the injection time shows no sign of it —
with a cheap test, *agreed with the owner the same evening*: N80's
hose shut for two captured drives, after the new valve's own two
(`plan.md` 8o). **Third in list A since that evening**, below the belt
and H0 (*agreed with the owner*; *The idle's candidates, ranked*); the
new valve stays its test — the common part by capture before and after
it.

**Read 12/11, the captured stop** (`49`; S1, *The first captured stop
on the canister*): **3 swelled as before** after the hot drive (to
−23 %, 014 0.69 %, 37 of 40 rises on 3), stepped to its floor by
itself and held it fourteen minutes; **settled, the stop was as calm
as `44` after its cut and `48`, before the canister, and no calmer** —
the grade 37, the common part 30 against 28 and 31. **So neither part
was lowered at this stop**; the canister's one sign left at the idle is
the floor's length, one stop. **And 032's part-load cell went back up**:
+2.3 % after the morning's MFD drive, **+8.6 % after this one** — the
bypass's level (+6.3 to +7.0) and above, where two drives on the
canister had read +2.3; the idle cell −14.8 → −7.0 (S19). *Reasoned*:
the part-load "for" below rested on +2.3 holding; a cell that moves
from +2.3 to +8.6 in one brisk drive says the purge gas's make-up still
moves it, or that +2.3 was not the canister's. *Claude proposed H16
down list A on both counts the same day*; **the owner kept it first
until the new N80 is fitted** (12/11, below: the canister is back, the
valve is not changed yet; *third since 12/11 evening, above*).

**The owner's reading, 12/11** (*owner*; the mechanism *reasoned*, not
measured). **With the bypass** N80 drew straight from the tank: under
load a large purge emptied the vapour space and drew nearly clean air
through the cap's vent — the part-load cell's +6.3 to +7.0 — while at
idle the small flow still carried vapour — the idle cell's −6 to −8.
**With the canister back and N80 still not sealing**, the purge gas is
the charcoal's, steadier: the part-load cell fell to +2.3 on three
drives, the idle cell hardly moved, **because a valve that leaks shut
lets a little canister vapour in all the time**, most felt at idle.
**This morning's gentle 40-minute drive** purged little, the canister
stayed loaded and leaked on at idle — **the idle cell to −14.8 %**, the
most on record; **the brisk drive after it** purged the canister nearly
dry — the part-load cell to **+8.6** on air through dry charcoal, the
idle cell back to **−7.0** with less to leak.
- **For**: it explains all four readings on the canister with one
  valve, and the bypass's split as well. **The part-load cell moves
  with the drive within a drive**, not only between drives: on 11/11
  night's log it climbed from +2.3 to +6.3 in eleven seconds at
  51 minutes and was back at +2.3 two minutes later (`vcds-step8k-
  drive-032-055-014.csv`); a purge gas whose make-up changes does that,
  a fixed fault does not. **And at 11/11 night's long warm stop the
  idle cell came back from −5.5 to −3.9 %** (the log's end) — less
  vapour to leak as the stop draws the canister down, which this reading
  predicts (S23 bent that drive's idle cell, so weakly). A leak sized at
  0.6–0.7 bar of idle vacuum was never tested (*Tested 25/10 night*:
  by mouth, 0.1–0.2 bar; 6/11 out of the car, cold).
- **Against or not fitting yet**: **12/11 night's drive was brisk too**
  — a motorway stretch, the limiter touched — and ended at +2.3, not
  +8.6; full-throttle pulls run open loop with the purge shut
  (*general*), so what dried the canister this morning would have to be
  the part load around them. Out of the car on 6/11 the valve passed
  "really very little", unpowered. A drive's fuel and temperature are
  in it too: November's cold tank gives little vapour, so what loads
  the canister overnight is not known. **And it is about the trim, not
  the roughness**: today's stop was no calmer settled at −7.0 than the
  floors before at −6 to −8 (S1, *The first captured stop on the
  canister*); whether a less negative idle cell brings a calmer idle
  is not shown — one stop.
- **12/11 evening, the queue drive** (`50`): a gentle hour, a crawl
  and a quarter of an hour's idle at the end, took 032 from −7.0 /
  +8.6 to **−4.7 / +6.3 %**, 055 −0.93 → −0.97 g/s. **Against "a gentle
  drive leaves the canister loaded and the idle cell falls"** — the
  morning's gentle 40 minutes gave −14.8, this gentler hour moved it
  towards zero; **for "a long stop draws it down"**, as 11/11 night's
  did. And at the stop 3 swelled three times with no floor, where the
  morning's floor held fourteen minutes on the same valve and canister:
  the floor's length is not the purge hardware's (S1, *The queue drive,
  and what the ECU sees through a swell*).
- **What decides it — the new N80** (`plan.md` 8a, in hand 13/11, the swap about the weekend): **032
  read after a gentle drive and after a brisk one on the new valve**.
  This reading predicts the idle cell nearer zero and no longer
  following the drive (−14.8 after a gentle one could not come back);
  the part-load cell may still move with the purge, which is the
  system working. **No change → the leak was not the valve**, and
  the idle cell's rich source is elsewhere (H7, S19).

*Added 24/10 at the owner's request.* For **the rich idle trim, S19 and,
since 6/11, S21**, not for the idle itself. 032's idle cell has read at or below zero in
every reading since the MAF was replaced on 24/9 (−3.1, −0.8, −2.3, 0.0,
−4.7, −3.1, −6.3, −3.1 %, `idle-log.md`; the 0.0 / 0.0 of 24/10 is the
clearing's reset), while the part-load cell reads +2 to +6 %.
**Somewhere a fixed amount of fuel joins the charge that the ECU did not
meter**, and a fixed amount shows most where the air is least, at idle
(*reasoned*). Nothing in these files has said where it comes from. **11/11** (S21, *Read 11/11*): VW's fault
table names N80 under both P0172 and P0440, the one part it does; the
tests behind the "against" below were cold or by mouth, never warm under
the idle's vacuum; the new valve is ordered (`plan.md` 8a; in hand 13/11).
**11/11 night, the first drive on the canister** (S21, *The first
drive on the canister*): the part-load cell relearnt to +2.3 % where
it held +6.3 to +7.0 with the bypass — **for H16's purge path**, one
drive; the idle cell bent by S23, so the idle side is unread.
**12/11 night, the second** (8n): +2.3 again; the idle cell −5.5, near
its old −6, so the canister did not move it. **The two nights' stops
near home are the two calmest warm stops on record outside the
provider's gas** — 25–40 for minutes on 11/11 (G62 then misreading),
35–50 for about thirteen minutes with 014 at 0.04 % on 12/11 (S1, the
warm stops' table). *Reasoned*: the canister is the one change both
nights share — 11/11 had the faulty rear probe and the oily G62, 12/11
neither — and a purge path that no longer sends raw tank vapour fits a
calmer warm idle; **against**, two stops, a different place from most
warm stops, and 10/11 evening's four calm minutes came before the
canister. **Moved up from sixth to third on it, 12/11** (*the owner's
decision*), and **first of the common part's list** (*third since
12/11 evening*) when the idle was
split in two the same day (*The idle's candidates, ranked*).

**How it would make the idle rougher** (*reasoned*, 12/11, at the
owner's question; the mechanism is not measured). **Not a steady flow**:
N80 is closed without power and hardly passed air out of the car (6/11),
so vapour came in only while the ECU purged — warm, in closed loop, at
idle too at a small rate. **What the bypass changed is the purge gas's
make-up.** The charcoal is a buffer: it takes the tank's vapour in, gives
it back steadily, and its own vent lets fresh air through it. Drawn
straight from the tank's vapour space, the gas follows the tank —
nearly pure fuel vapour while the tank is warm and pressed, air through
the cap's vent once the purge has drawn the pressure off — and that
changes over seconds with no buffer to smooth it. **The lambda loop
corrects the mean, slowly**: at idle one swing of the front probe takes
a second or more, plus the gas's way to the probe, so a mixture that
moves faster than that, or irregularly, goes through; 032 learns only
the long mean. A mixture moving under all four cylinders alike is **the
common part** (list A). **For**: the part-load cell, +7 → +2.3 % with the
canister back — a lean source gone where the purge flow is largest,
which air drawn through the tank fits (*+8.6 % again after the captured
drive of 12/11, above*); P0440; the summer overpressure at
the cap (S21); the two calm stops (*the captured one of 12/11 no calmer
settled than the floors before the canister, above*). **Against or not known**: **the idle
cell did not move** (−6 before, −5.5 after), so at idle the mean
mixture was the same and only its swings could have changed — not
measured, the front probe is not on the bus; **the dips do not keep time
with the valve's 4–5 Hz** (*The valve's pulses against the dips*), so
not pulse by pulse; **the idle is roughest cold**, when the valve is
not driven at all, so the cold roughness has another cause; two stops.
**What would show it**: a captured warm stop (the common part against
the slot means, `plan.md` item 6) and 033 at the same stop, whose
regulation value swings with the mixture the loop is chasing. *Read
12/11 (above): the common part no lower than before; 033 steady,
sd 1.0–1.1 %, through the swell and its step.*

**How the system works** (*general*, not from this ECU's documentation):
the tank vents into a charcoal canister; N80 sits between the canister and
the intake (*on this car, until the repair of 8j, the canister was
bypassed and N80 drew straight from the tank: S21, 11/11*) and is **closed without power**. The ECU pulses it open only in
closed-loop lambda control, warm, so that the probe sees what the vapour
does and the injection is corrected. A pause after the start, then pulses,
is the valve working as designed (the owner saw exactly that, 25–27/9).
A healthy engine purges at idle too, at a small rate. **A valve that does
not seal** passes vapour all the time, cold and in open loop, on the
overrun and **while the car stands**, when vapour from the canister can
settle in the intake and flood the first start.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | — | — | — | — | — | ~ | ~ | ✔ | ~ | ✔ | — |

- **For: S19.** A rich code and a start that dies at once after four hours
  standing, in a window that holds a fill, is the textbook picture of a
  leaking purge valve (*general*). **H7 is no longer the only hypothesis
  that predicts both.**
- **For: the idle trim** negative at idle, positive at part load — the
  shape of a fixed fuel flow rather than a scale error. **Re-read 12/11
  after two drives on the canister** (*the owner's question*): the
  part-load cell fell (+7 → +2.3 %), so with the bypass **the purge gas
  at part load was lean, not rich** — the ECU added fuel to make up for
  it — which air drawn in through the tank's vent fits, once a large
  purge flow had emptied the vapour space; with the canister back, the
  same flow carries the vapour the charcoal stored (*reasoned*). **The
  idle cell did not move** (−6 → −5.5), so **the bypass was not the
  idle's rich source**; a valve that passes vapour shut would still be
  (the new N80, `plan.md` 8a, reads it: 032's idle cell before and
  after).
- **For: the history.** P0440, EVAP, stored in 1/2018 and never repaired
  (`vehicle-history.md`). **And back on 6/11** (S21): the same code,
  the engine lamp lit, sporadic, with no fill and no hose touched
  before it (*owner*) — the first fault code on this path since 2018,
  and the one symptom that names the evaporative system directly. What
  in the system it names is not known: a valve that does not seal is
  one ordinary cause of P0440 among the hoses, the canister and the cap
  (*general*). **And VW lists it**: among the causes of a low
  idle learnt value in 032, *"the activated charcoal filter solenoid
  valve permanently open"* (`vcds.md`, block 032). *(This bullet first
  read the "filler cap off at idle" of 25–27/9 as the fuel tank's; in
  these files the filler cap is the oil filler, so that test bears on
  the crankcase, H17 — the oil filler, confirmed by the owner 25/10.)*
- **Against: what block 070 found** (`refuted.md` A6): TEV OK, lambda
  deviation 0.0 %. A test that commands the valve open and reads the
  response says the valve **opens**; it cannot say that the valve **seals**
  without power (*reasoned*; exactly what that block looks for is not in the
  label summary, `vcds.md`). 0.0 % says only that the canister had nothing to
  give at that moment. So 070 refutes a dead valve, not a leaking one.
- **Against: S1 and S3.** A dip is one firing that fails and recovers in
  about a quarter of a second (S1; **5/11**: one in five is two firings in
  a row, weak firings follow each other 3½ times as often as by chance —
  the one thing a moment of vapour would predict — but warm the weak
  strokes are 3's, which vapour through the plenum cannot pick: S1,
  *Every stroke named*); vapour comes through the common plenum
  to all four alike as a slow, even flow that the lambda loop follows, so
  it cannot make one firing in hundreds fail and the next succeed. **The
  weak strokes and the deficit are 3's at every warm idle on record** (S1,
  *Every stroke named*; *"the dips sat on 3 and 4 for weeks" until
  12/11*), which a common-plenum source cannot pick. And the size: a trim of a few per cent
  rich is far from any rich misfire limit — slightly rich burns more
  readily, not less (*general*). Load smoothing the idle (S1) fits it, but
  fits almost everything that adds charge. S14 is ~ only because a leaking
  valve feeds vapour into the intake during the overrun fuel cut, where the
  vacuum is highest (*reasoned*).

**The owner's variant** (24/10): **each pulse a slug of fuel**, from a
canister flooded with liquid that the charcoal no longer holds, and now and
then a slug that burns badly. That answers the first *Against* above in
part: pulses are not an even flow, and a slug reaches whichever intake
strokes are open at that moment, so it *could* fail one firing and not the
next (*reasoned*). What speaks against it: **on 27/9, with the idle
already rough, 070 opened the valve and lambda moved 0.0 %** (`refuted.md`
A6) — a flooded canister would have sent the probe rich at once; and the
weeks on 3 and 4 would need the purge port to sit nearer their runners,
which nobody has looked at. A canister flooded since 27/9 is not
excluded: a tank filled past the first click, or the car parked nose
uphill on a full tank, can push liquid into it (*general*). **The first
does not happen here**: the owner always stops at the first click
(25/10), the fill of 24/10 included; the slope stays. *This said the hose would be closed off at N80 at a warm idle with
`IdleHealth` read off the display; dropped by the owner, 25/10* (`plan.md`
6e): liquid fuel at the hose when the pulses come is what the variant
leaves to look for.

**Tested 25/10 night** (`plan.md` 6e, `idle-log.md`): engine off, a blow
through N80 towards the intake **passed, "but really little"**
(*owner*); on the cold start **no suction** at its tank-side port, then
the pulses, **no liquid fuel**. **What it leaves:**

- **Not the rich idle trim.** With the port closed by the finger the
  canister had no way in (*the tank, in truth: the canister was found
  bypassed 11/11, S21*), and the regulation still sat at −0.7 % on top
  of 032's −7.8: the engine wanted the same fuel taken away with N80 out
  of the circuit (*reasoned*; the learnt value applied cold is
  *general*). The trim's first *For* above is answered against —
  **cold**; a warm idle with the canister cut off was not run.
- **The owner's slug variant: no liquid**, on a day after a fill.
- **Still possible: S19.** A valve that passes air without power
  passes vapour while the car stands, which no running test sees; the
  leak is small. *The valve was not to be replaced (the owner's
  decision, 25/10: a part that helps neither the idle nor the trim is
  not worth fitting for the starts alone) until P0440 came back on
  6/11, below.* **S7 closed 31/10 as the fuel**
  (`refuted.md` D2): if the Verva's vapour came this way, it went with
  the Verva, and the valve's small leak is left without a symptom of
  its own (*reasoned*). **6/11, P0440 back** (S21): the system has a
  symptom of its own again, a fault code; the valve's leak of 25/10 is
  one candidate for it, not shown to be the cause. The trim's split
  outlived the map (S19, settled 6/11), which this hypothesis was
  already answered against cold, not warm. **6/11 night, out of the
  car** (`idle-log.md`): unpowered it passed air not clearly at all, at
  most "really very little", perhaps only the hose's grooved end (*owner*)
  — less than the "really little" of 25/10 — no granules, no fuel; cleaned
  with its contacts and refitted. **Replaced only if P0440 comes back or
  item 8 changes nothing** (*the owner's decision*, 6/11 night, `plan.md`
  8a; *this said "replaced after item 8's readings", his decision of the
  same evening, and before that "not replaced"*) **9/11: the clean changed
  cylinder 3 and no P0440 was stored, so now only if P0440 comes back.**
**11/11: ordered all the same** (*the owner*, "to be sure", after the
research on P0172 and P0440; S21, *Read 11/11*), fitted when it arrives with
032 read before and after (`plan.md` 8a).

**The valve's pulses against the dips** (6/11 night, *at the owner's
question*). The owner heard the valve click **about 4–5 times a second**
(*owner*); its exact drive frequency is in no source found (the nearest,
a Bosch purge valve on another make: 16 Hz purging, 8 Hz in its
diagnosis; *general*). If each pulse could tip a weak firing over, the
dips would keep time with the pulses. **Read over every settled idle in
the `_z1` captures** (5½ hours, 29 captures; warm = oil 80 °C and over
at the window's start, cold = under 50 °C at its end, when the ECU does
not drive the valve; *an ad-hoc script, not kept*):
- **Engine speed's spectrum**, 0x280 held at 100 Hz, 10 s blocks: the
  only lines are the engine's own — the camshaft frequency (6.6–6.7 Hz,
  one cylinder differing) and twice it; **nothing at 3.5–5.5 Hz, warm
  or cold** (the warm average there at its continuum, ×1.0). A
  narrow line at a fixed frequency is no more frequent warm than cold
  (4–5¼ Hz: 4.2 % of warm blocks, 4.5 % of cold), and spread over the
  whole band as chance spreads it. **Its reach**: a 4.5 Hz swing of
  0.5 rpm added to every warm block shows as ×1.5, of 1 rpm in 30 % of
  them as ×1.6 — so any steady swing there is below about half an rpm,
  against dips of 20–45.
- **The dips' timing** (≥ 20 rpm, Rayleigh test per window, averaged,
  1.5–13 Hz in 0.005 Hz steps): warm, 43 windows, 2025 dips — **the one
  clear peak is the camshaft frequency, 6.63 Hz (2.9 against 1 by
  chance)**, the weak strokes keeping to one cylinder (S1, *Every stroke
  named*), which shows the test can see a rhythm; **3.5–5.5 Hz at most
  1.4, what the largest of that many chance values reaches**; cold
  (20 windows, 830 dips) the same, 4.8 Hz at 1.7 by chance. A rhythm
  above 13 Hz, as the 16 Hz of the other make, folds into this band
  (one sample per firing) and is not there either.
**Read** (*reasoned*): the valve's pulses do not set when the dips come.
What this cannot see: a purge that was off through most of the warm
windows (the ECU's purge phases are not on the bus), and a rhythm whose
frequency wanders. A canister giving more now and then would show as
more dips in some minutes, not as a rhythm; on 6/11 night the valve's
canister side showed no granules, dirt or fuel (*owner*).

**Re-read 6/11, at the owner's question: a common cause of the idle?**
The owner's reading: not the difference between the cylinders, but the
common stress that pushes the weakest of them, 3 and 4, over the edge.
**It does not contradict the cylinder pattern** (*reasoned*): a common
source sets how many dips there are, the weak cylinders where they fall.
- **For**: VW lists N80 permanently open among the causes of a low 032
  idle value (`vcds.md`), and 032's idle cell is −6 to −8 % on both maps;
  a German workshop reads a negative correction without the valve
  driven as a leaking or open valve, and names an unsteady idle among
  its symptoms (*general*, `kfz-dietrich.com`). **Purge comes in phases**:
  the pattern over the cylinders moving over minutes, weak firings in
  pairs 3½ times as often as by chance (*How many strokes make a dip*) —
  what phases of vapour would give (*reasoned*; *since 12/11 the moving
  part is 3's swell, one cylinder, which vapour does not pick*). And now a fault code on
  the system. *This also named `IdleHealth`'s waves of about 1½ min
  (27/10) until 6/11 night, when they followed the radiator fan (S1,
  *The radiator fan's cycle*).*
- **Against**: **the idle is roughest cold**, when the ECU does not
  drive the valve and a cold fuel gives little vapour; **25/10, cold,
  the canister closed off, the engine still wanted the same fuel taken
  away** (above). **A warm idle with the canister closed off was never
  run** — the gap; not run before the swap either (*the owner*, 6/11: not
  needed), so the swap itself is the test, read against item 8's
  readings.

**What P0440 can mean on this car** (*reasoned*, from *general*
sources; this ECU's own check is not documented here). A European car
(the VIN) with **no tank pressure sensor and no leak detection pump**:
the ECU can judge the system only by opening N80 and watching lambda and
the idle air (block 070's fields: the valve's opening, lambda, the idle
air valve, OK / not OK; Ross-Tech's list), as Bosch's patents describe
both. So a malfunction is **no reaction when the valve is opened**: a
valve that does not open or is fouled, a blocked hose, charcoal granules
from the canister, or a valve that leaks so much that opening it adds
little; and **Bosch notes the lambda check is unreliable when the fuel
hardly evaporates**, as in November. **The filler cap cannot set it
here**, with nothing to measure the tank's pressure — and it is new from
about early 10/2026, bought for its torn tether (*owner*, 6/11).
**6/11, the album** (18:42): the number on the part around the valve is
`051 133 459 A`, EPDM — a seller lists it as the rubber holder of such a
valve, with a Bosch valve among its cross-references (*general*); so not
the valve's own number, as the owner read it too. **6/11 night, the valve out**
(`idle-log.md`): **Bosch `0 280 142 353`, VW `1C0 906 517 A`**, date code
`040`; **no granules, no dirt, no smell of fuel** at its canister-side
port, the hoses old but sound (*owner*). So **not a canister shedding
charcoal** and no liquid in the line; what is left for P0440 is the
valve itself (not opening fully, or leaking so much that opening adds
little), its wiring, or the line to the intake (*reasoned*).

### H18. Oil past the valve-stem seals, drawn in at idle

**12/11 evening** (S1, *The swell's shape, and what the common part
follows*): **for one valve, 3's inlet, as the swell's second reading** —
oil gathering at idle's vacuum and drawn in at once is a trap that
fills and empties, the sawtooth's shape; against, no blue smoke, the
plugs dry, and a load lifts the swell at once. **Against it as the
common part's cause**: the common part does not grow with the time
into a stop (r −0.09), which this entry's "worse after idling" asks
for.

*Added 26/10 at the owner's request*, from his reading of 26/10 (S1,
*Temperature*): the warm idle stays at 90–110 through a gentle warm-up
and calms only after a drive in which the engine works, and stays calm
for the next 15–20 minutes of idling. **The mechanism** (*general*;
owners' forums, not a manufacturer): a worn or hardened stem seal lets
oil run down the valve guide, and the intake's vacuum, highest at idle,
draws it into the cylinder, where it costs combustion; under load the
vacuum falls, the flow stops, and what collected burns away.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ✘ | — | ~ | — | — | — | — | — | — | — | — | — |

- **For: the shape of 26/10**, worse after idling and gentle driving,
  calmer after work, the calm lasting — what oil collecting at a small
  charge and burnt off under load would give (*reasoned*).
- **For: the small unevenness on all four** (S1, *Every stroke named*,
  *The small steps are on all four*): the seals age together, and that
  part of the idle is common. **Against: the misfires and the steady
  deficit are 3's**, at every warm idle on record. *Until 12/11 this read
  "for: since the VW leads the dips sat on all four alike; against since
  3/11: one cylinder again" — those leads never spread them (Naming the
  cylinder).*
- **For, weakly: what the screen showed** on 19–20/10 (`idle-log.md`):
  a thin lacquer on the back of every inlet valve and wet patches on
  every crown. Oil from the guide would leave both, but so would the
  breather's oil mist, fuel or condensed water; a cheap screen with the
  engine stopped cannot tell them apart.
- **For, 12/11 night** (the one-valve form on 3): load helps, measured
  — 3's deficit a fifth of a stroke at idle and with the pedal light,
  1–3 % at full load (*Naming the cylinder*, *Off idle*); H3 and H20
  predict the same.
- **Against: no blue smoke seen**, ever (*owner*, 26/10), and the plugs of
  20/10 dry black, not oily. The oil on every plug's thread is from the
  cover side and says nothing about the chamber.
- **Against: 26/10 itself.** The calm came after engine braking downhill,
  when the vacuum is at its highest and a leaking seal passes the most;
  the drive's load after it would have to burn off more than the coast
  drew in.
- **Against, 4/11** (S1, *driving does*): the calm after revving — the
  overrun on the way draws the most oil past a seal.
- **Against: the dipstick** (`plan.md` 6i): no loss can be read between
  top-ups. **How much oil it burns is not known.** **5/11, the first
  reading** (*owner*; `photos/dipstick-2026-11-05.jpg`): **0.5–1 mm under
  the top mark at 155,546 km**, 522 km after it stood at the mark —
  within what the angle of the car and the draining time can make, so not
  a consumption by itself. **11/11 evening, the second** (*owner*, given
  12/11; the album 20:51:55, the car standing in the garage): **about
  another 0.5–1 mm lower**, the film ending a few millimetres short of
  the mark, at between 155,853 and 155,969 km — **some 850–950 km since
  the mark, two readings falling the same way: a small consumption**
  (*owner*: "it eats a little oil, nothing terrible"). How much in
  litres is not read off a dipstick without its span, which is not
  recorded here; no top-up yet. **The owner's reading**
  (5/11): oil past the rings, held by deposit (H13), which the wet-looking
  patches of the borescope photos might be — against it so far, the plugs
  dry, no blue smoke, compression even.
- **S3 ~** for the same reason as S1: misfires at idle, on all four.

**Tests:** **the oil consumption on the fresh oil** after the change of 26/10,
read on the dipstick from a photographed level (`plan.md` 6i) — oil
burnt lowers the level, fuel in the oil would raise it (`refuted.md`
C21); **the plugs** at the next
change, for oily deposit on the firing end. A compression or leak-down
test does not reach the seals.

---

### H19. ~~The MAF's curve against the remap~~ — refuted 3/11, `refuted.md` C22

### H20. Coolant into cylinder 3 — a weep at the head gasket or the head

**Re-read 12/11, the third research** (S1, *Every stroke named*): 3 is
the cylinder by every measure, which this entry needs; a weep would be
worst after a hot drive, as the swells often are, but they also start
minutes into a stop and end in a step (`40`, `47`), which pressure
falling slowly does not give. Its test stands (the CO₂ test, item 9).
**12/11 evening** (S1, *The swell's shape*): steam fits the mixture
not moving and every stroke weaker; nothing in a weep fills and empties
by the minute, and `32` grew three times over in one long idle.

*Added 4/11/2026 at the owner's request*, as a weak candidate after `43`
named cylinder 3. **The claim** (*general*): a millilitre a day past the
gasket or a hairline in the head next to 3 enters where the cylinder's
pressure is lowest, at idle vacuum, and steams the charge — a misfire
at idle on that cylinder, eased by load, and a plug kept clean.

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | ~ | ~ | ~ | — | — | — | — | ~ | — | — | — | — |

- **For:** one cylinder at idle; load helps (a higher manifold pressure
  draws less in, *reasoned*); **plug 3 the cleanest** of the 10/10 set
  after nine days (`vehicle-history.md`, the photos), on the cylinder
  that misfires most; S2's puffs could be steam as well as unburnt
  charge.
- **For, 12/11 night**: load helps, measured — 3's deficit −21 to
  −26 % of a stroke at idle and with the pedal light, −1 to −3 % at
  full load (*Naming the cylinder*, *Off idle*); H3 and H18 predict
  the same.
- **Against:** **the level does not visibly fall** (*owner*, 4/11) —
  weak against a weep this small, which is why it is kept; **no
  emulsion** under the cover, on the cam or the dipstick (1/10,
  `refuted.md` C13); compression even (A4, cold); the borescope shows
  **no steam-cleaned crown** on 3 — its crown carries the most deposit,
  not the least (*What the forums say*, the photos read again, 4/11); the warm-up to
  99–100.5 °C holds; no white smoke reported; **the calm after revving**
  (S1, 4/11; *reasoned*): the coolant's pressure is highest after a hard
  drive, so a weep should be worst then, not best.
- **Test:** **a combustion-gas (CO₂, "block") test of the coolant**,
  warm — a few hundred Kč at a garage or a kit; `refuted.md` C13 never
  had one. A leak-down (H1's test) watched at the expansion tank for
  bubbles on 3 says the same.

---

### H21. The probes' wiring and connectors — the harness side, not changed with the probes

*Added 10/11 evening at the owner's request* (his idea: a joint in the
probes' wiring that moved that day, and the catalyst test that put it
right for a while). Both probes were replaced on 10/11 with their own
leads and plugs; **the sockets on the harness side, the wires to the
ECU and their earths are the car's** (`vehicle-history.md`).

| S1 | S1s | S2 | S3 | S4 | S5 | S11 | S12 | S14 | S19 | S20 | S21 | S22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ~ | — | — | — | — | — | — | ~ | — | ~ | — | — | — |

**S23 closed 12/11** (`refuted.md` D13; *the owner's decision*): the
new rear probe's own fault, the old one healthy on the same harness on
two drives — **so H21 lost its one ✔ with the column**; what is left of
it is S19's idle cell (the front probe's damaged signal-earth wire,
below) and S12's ~. Its place in list A (fifth) is the owner's to
re-read; Claude proposes no move before the new N80, which reads the
idle cell too.

- **For, S23** (*reasoned*; *S23 closed 12/11 as the new probe's own fault, so this no longer stands for the harness*): a leak to earth in a damp or oxidised
  socket pulls the signal down in proportion, so the ceiling falls under
  load as well as the idle, which is what the rear probe did from 16:57
  on 10/11, before reading zero at full load; it came back after the
  revs of the basic settings, not after cooling, which suits a contact
  moved by vibration better than a lead melting on the exhaust. **One
  circuit, two probes, three days**: the old rear probe sank at every
  idle on 9/11 night, the new one switched to the front's swing after
  18 minutes on 10/11 morning and failed under load that evening.
- **For, found 10/11 evening** (S23, *Found at the harness*): the
  front probe's signal-earth wire (grey at the probe, brown on the
  harness side) worn and cracked inside the box the leads run through,
  and the rear probe's heater lead cracked and corroding beside its
  signal — both on the harness side the swap did not change.
- **For, S19's idle cell** (*reasoned*, the wiring of this car not in
  these files): the cell came back to −6.3 % on new probes (H11, *The
  relearn drive*), so whatever makes the front probe read rich at idle
  survived the swap. A resistance in the front probe's signal earth,
  if heater current shares any of its path, would lift the reading by
  the heater current times that resistance — and the heater runs most
  at idle, where the exhaust is coolest (*general*), so the shift would
  be largest there. Whether the signal and heater earths share a path
  on M5.9.2 is *not known*.
- **For, the idle (S1), and S12** (*the owner*, 10/11 night): a
  resistance that comes and goes in the **front** probe's circuit makes
  the ECU see false rich or lean, and it moves the mixture of all four
  cylinders after it; the idle is where the engine runs nearest its
  edge (the gas idle of 9/11, S1), so a mixture thrown about would show
  there first — and a step of it at a crawl or a moving-off would be a
  jerk (S12). *Reasoned*, and fair: nothing below rules out glitches
  shorter than VCDS's sample.
- **Against, for the idle (S1)**: (1) **the front probe's own trace**:
  033 at a warm idle, about one sample a second, 9/11 night (664
  samples, the old probe) and 10/11 morning (741, the new): **switching
  regularly between 0.06–0.08 and 0.74–0.77 V, never more than 6 s on
  one side, the correction within −4.7 to +3.9 %** — no dropout, no
  stuck value, no excursion of the correction (*ad-hoc script, not
  kept*); a glitch under a second would not show. (2) On 10/11 morning
  the new rear probe read flat at 0.59–0.60 V, the healthy shape, for 18
  minutes, and the idle was as rough and the A/C calmed it as much (H11,
  *The reading after the swap*) — the mixture behind the converter was
  right while the idle was rough. (3) A mixture moves all four
  cylinders alike; the idle's misfires and its steady deficit are 3's
  (S1, *Every stroke named*), which a mixture does
  not make. **So a part of the idle at most** — its four-alike share,
  not the cylinders' difference (*reasoned*).
- **Against, S23 as the circuit**: the new probe failing early is not
  ruled out; a lead and socket found sound leave the part. **The
  owner's own view** (10/11 night): the connectors are very likely
  sound and the leads well tucked in; he follows the harness on to the
  ECU and its earths instead (`plan.md` 8e).

**A shared earth, linking it to H4** (10/11 night, *the owner's
question*: could one earth fault tie the probes to the idle; *reasoned*
unless marked). An earth that both the probes' signal returns and other
circuits share would carry their currents and shift every reading
referred to it, **alike for both probes** — H11's literal form, which
the swap could not test — and, if the crankshaft sender G28 and the
knock sensors share it (VW's diagram for this engine lists a **sender
earth, 220**, beside G28 and T3; which senders it carries the garbled
text does not show, H4), noise there would reach 014's misfire count
(S3) and the knock window (S4, S5) as well. **What is known**: the
engine's earth under load measured clean (H4); the rear probe has been
read under load twice, the old one never (10/11 morning fine, 10/11
evening S23), and the front only at VCDS's ~1 s, so noise faster than
that has never been seen. **One test in the data, against at idle**:
the radiator fan, the largest load at a stop, runs while the coolant
falls; over the queue stops of 16:55–17:27 on `47` the rear probe read
a median **0.29 V with the coolant falling (386 samples) and 0.29 V
with it rising (475)** — the fan's current moved nothing (*ad-hoc
script, not kept*). **A second, on the bus** (10/11 night, *the
owner's question*: correlate every voltage that could share an earth):
the coolant is read twice — the ECU's sender on 0x288 b1 and the
cluster's own on 0x420 b4, a separate circuit
(`docs/firmware/can-decoding.md`, question 10) — so a load that lifts
the ECU's sensor earth would step their difference. On `47` it held
**8.6–9.2 °C with the A/C off and on, twice**, and 9.3 against 9.7 °C
with the radiator fan off and running at the warm stop: within half a
bit (0.75 °C). An NTC sender reads a few mV as a degree or more at its
hot end (*general*), so an earth that moved with these loads by more
than a few mV would have shown — **against, for the ECU's sensor
earth**; whether the probes' signal earths share it is *not known*.
**Measurable cheaply**: the voltage between the
ECU's earth and the engine block, and between each probe's signal-earth
pin on the harness side and the ECU's earth, at a warm idle with every
load on — a few tens of mV is an earth fault (*general*). **And VCDS**
(*the owner's request*, 10/11 night; `plan.md` 8h): the largest loads
switched from the seat at a warm idle, each against 004's supply, the
probes, the temperatures, the throttle's sensor voltage, the air mass,
the knock sensors and the heaters' resistance — what moves with a load
besides the supply shares its earth.

**Tests:** the sockets of both probes looked into from the harness side
at the next cold engine, with the rear lead's run (`plan.md` 8e); the
probes' loom and both connectors flexed with 033 and 036 logged, with
the ignition only (a leak to earth pulls the bias off its steady
0.43–0.44 V; never with the engine running, *the owner's decision*,
10/11 night — a series resistance, which would show only on a hot
probe, is left to the multimeter);
a jump in either is the find (8g, *dropped 11/11*, the owner); each wire from the socket
to the ECU's pin, resistance and insulation to earth, with the ECU's
plug off when 6n is done (the pins from the current flow diagram, read
first).

## Naming the cylinder

The bus carries no cylinder identification and 014 has no per-cylinder
counter. Two things name cylinders: the **injector cuts** (one connector off
at a warm idle), which mark their slot through a long run, and
the fault codes they leave; **and since 12/11 a third, with no cut: the
strongest slot is cylinder 2's** (*The count that does not slip*,
below; `tools/cylscan.py`). **The cuts, eight in all**: **10/10**
(`31`) 1, 4, 4, 1; **24/10** (`41`, cold) one on 4; **3/11 evening**
(`43`) one of 57 s on 4; **9/11** (`44`, `46`) one of 30 s on 4 at each
stop. No cut is asked for any more to name the cylinders (*the owner*,
12/11; `CLAUDE.md`). **Off idle** the names are carried through a
whole drive by one stroke count (*Off idle*, below; `tools/drivescan.py`).

**The leads' order on the coil** (*owner-read off the car, 1/10/2026*):
**1, 4, 2, 3, clockwise from the top tower** — 1 and 4 side by side, 2 and 3
side by side, the two pairs the coil fires together in the firing order
1-3-4-2. Which tower the coil itself calls which cylinder is not read.
*Dropped by the condensation of 20/10 and put back 21/10, when the leads
were changed.*

### The count that does not slip, the wheel, and the spread

*12/11, the third research; `tools/cylscan.py`, kept, and
`tools/test_cylscan.py`.* Three corrections to how a stroke is put to a
cylinder; **the dip shares read before them are withdrawn** (*What the
dip shares said, and what stands*, below; S1, *Every stroke named*; S3,
*What 014 counts, by cylinder*).

- **The count.** `cutscan.bridged_runs()` (removed 12/11) counted
  strokes by how long a value was held and lost one at two equal
  neighbours or a missing frame — the slips of 9/11. Engine speed integrated over time is crank
  angle, one stroke per 180°; `cylscan.track()` rounds that to a stroke
  index and lets every change of 0x280's value correct the phase a
  twentieth of its error. The rounding error stays under half a stroke
  (99.9 % of changes within ±0.42 on `09`, `31`, `43`); **on `31` one run of 883 s holds the four
  cuts (1, 4, 4, 1) on their own two slots**, and no run slips.
- **The crank wheel alternates, and it is not combustion.** Successive
  strokes read alternately high and low: cylinders **2 and 3 high, 1
  and 4 low** — the two pairs that share a half of the wheel.
  **Measured where nothing burns**, on the overrun with the fuel
  counter standing (`--wheel`, 850 windows of 40 strokes): **0.216–0.226 %
  of engine speed in each of thirteen captures** from 24/9 to 10/11
  (0.216–0.222 in the ten with twenty windows or more), and the same in every band
  from 1450 to 2500 rpm (3.2 rpm at 1500, 5.4 at 2400) — proportional
  to speed, as an angle error of about 0.2° of crank is and a
  combustion difference is not. The neutral holds of August (`10`,
  `15`: 0.22–0.23 %) and the clean's 55 minutes at 1,850 rpm (4.1 rpm,
  steady to ±0.05 from window to window) read the same. **Named** (`--wheel`, its last lines): thirteen
  overruns run into a standing idle in one stroke count, and by that
  idle's names the overrun's steps read **−0.219, +0.217, −0.218 and
  +0.219 % of engine speed for 1, 3, 4, 2** (±0.004, some 530 strokes
  each) — 2 and 3 high, and **nothing left on any cylinder with the
  alternation out** (0.02 rpm at most at idle). *This said "ad-hoc
  script, not kept" until the owner asked for it in the tool, 12/11.* At idle it is **1.7 rpm** — as large as the pattern over the
  cylinders it sits under. It lowered 4 and 1 and raised 3 and 2:
  **"4 weak, 3 hardly" was 3 weak, 4 level.** VW says the ECU learns
  the same error on the overrun for its own misfire detection (SSP 175,
  `vcds.md`); the speed it sends on the bus is not corrected.
- **The spread.** A stroke's loss shows in two values: about a quarter
  in the one before its own slot. The first dead stroke of each cut
  reads −7 to −18 rpm and then −24 to −33 (`31`, `41`, `43`, `44`,
  `46`); 6,000 isolated weak strokes read 0.22–0.33 of their own step
  already in the value before. In a steady cut the three live cylinders' gain
  hides it, which is why the cuts never showed it.
  `cylscan.deviation()` undoes it with the wheel.
- **The names.** With no cut in a run, the strongest slot is taken for
  2 (*the owner's idea*, 9/11): it is 2's at all eight cuts, and it
  puts 014's rises on the cylinder the ECU's own P0303 names.
- **What it changes**: `41`, cold, is not "all four alike" — 3 has
  56 % of its weak strokes and 36 of 014's 49 rises; `40` to `47` put
  58–73 % of the weak strokes on 3 where the dips' shares read 41–48 %;
  the old pattern in per cent of a stroke carried the wheel (4 too low,
  3 too high by about 5 % of a stroke each, 2 too high and 1 too low
  likewise). The rest is in the table below.


### Off idle — the count through a whole drive, and what the cylinders give under load

*12/11 night, at the owner's questions after the third research;
`tools/drivescan.py`, kept, and `tools/test_drivescan.py`. Sixteen
drives, `19`–`50`; warm (oil 80 °C and over).*

- **The ceiling of about 2,800 rpm was the method's, not the bus's.**
  `cylscan.track()` corrects its phase by *when* 0x280's value changes;
  0x280 comes every 10.65 ms, so from about 2,820 rpm a stroke is
  shorter than a frame and the moment of a change says nothing. One
  count from one standing idle to the next held in **38 of 38** drives
  that stayed under about 2,850 rpm and slipped in **16 of 28** above
  3,000 (by one or two strokes; moving off, gear changes, queues and
  the overrun were never the problem — speed was). **What a frame
  *reads* still names its stroke**: the crank wheel's alternation (2
  and 3 high, 1 and 4 low) grows with engine speed — 6 rpm between
  neighbours at 3,000, some 25 at 5,000 — so every frame says whether
  its stroke is an even or an odd one. `drivescan.track_drive()` lets
  the integral of engine speed carry the count, corrects it by the
  timing below 2,600 rpm and by that parity above, and learns the
  parity's sign where both work. **Cylinder 2 is on the same slot at
  every named standing idle of every engine run: 124 idles in sixteen
  captures, to 6,440 rpm, none slipped** (`--count`); in `35`, which
  has too little above 1,900 rpm to learn the sign, the count is
  restarted past 2,850 rpm instead of trusted. And the sign learned
  under load agreed with the idle's name in 16 of 16: **the pair that
  reads high at 2,000–2,500 rpm is the pair of the idle's strongest
  cylinder**, the wheel's.
- **What can be read off idle: two differences.** On the overrun, with
  nothing burning, the alternation left after `cylscan.WHEEL_ALT` is
  nothing up to about 2,400 rpm and then grows — 0.04 % of engine
  speed at 2,600, 0.13 % at 3,800, 0.27 % at 5,000 (13 rpm) — so the
  wheel is not one number at speed, and the pair 2 and 3 against the
  pair 1 and 4 is not read above 2,400. **3 less 2 and 1 less 4 carry
  none of it** (the wheel moves each pair alike): on the overrun they
  read −0.04 to −0.5 and +0.03 to +0.25 rpm in every band to 5,200
  (5,700 windows of 40 strokes), which is the floor of what follows.
- **The scale.** A whole stroke is 34 rpm of step at idle
  (`cylscan.STROKE_RPM`); the same work lifts a faster crank less and
  a loaded cylinder does more of it, so off idle it is taken as
  `34 × (b7 / 25) × (800 / rpm)` — 60 rpm at 2,950 rpm and b7 160, 42
  at 4,700 and 180. **A decision, good to about a quarter**: b7 is the
  ECU's model (at idle it reads 26–29 with the friction byte at 21),
  and the crank inertia that standing revs give (0.2–0.3 kg m² by b7
  less b6) is the idle figure's only to that. Every per cent of a
  stroke below carries it; the rpm of step do not.
- **A. The idle's pattern off idle: 3's deficit fades with load, 4's
  does not.** Per cent of a stroke, `19`–`37` | `39`–`50`:

  | | b7 | **3 less 2** | **1 less 4** |
  |---|---|---|---|
  | standing idle | 26 | −25.8 \| −20.6 | +10.2 \| +5.0 |
  | moving, to 1,150 rpm, the pedal light | 27 | −20.5 \| −23.9 | +8.5 \| +6.7 |
  | the same, pulling (moving off, a crawl uphill) | 57 | −8.6 \| −8.9 | +6.1 \| +2.9 |
  | 1,150–1,600, light | 20 | −22.1 \| −25.4 | +12.5 \| +6.8 |
  | 1,150–1,600, part load | 62 | −3.3 \| −4.8 | +1.9 \| +0.9 |
  | 1,600–2,600, part load | 62 | −1.8 to −4.0 \| −2.2 to −3.6 | +2.6 to +3.5 \| +2.6 to +2.7 |
  | 1,600–2,600, b7 90–140 | 105 | −1.5 to −2.0 \| −0.9 to −2.3 | +2.2 to +2.5 \| +1.5 to +2.2 |
  | 2,100–3,300, b7 140 and over | 160 | −1.8 to −1.9 \| −1.1 to −1.3 | +1.8 to +2.1 \| +1.2 to +2.5 |
  | 3,300–4,200, the same | 175 | −2.1 \| −1.6 | +3.2 \| +2.6 |
  | 4,200–5,200, the same | 185 | −0.3 \| −3.0 | +4.4 \| +3.8 |

  (errors ±0.2 to ±0.7 under load, ±1 at the top in `19`–`37`; the
  light-pedal bands above 1,600 rpm read −6 to −15 and +5 to +13, on a
  scale of 10–15 rpm with a noise of a quarter to a half of a stroke —
  not to be leaned on.) **Cylinder 3 is the idle's and the light
  pedal's**: a fifth to a quarter of a stroke under 2 standing,
  crawling and to 1,600 rpm with the pedal light; **under 9 % as soon
  as the engine pulls at idle speed, 2–5 % at part load, 1–3 % at
  full**, at every speed to 5,200 and in both periods. In rpm of step
  it goes from −7 to −8 at idle to −0.4 to −1.5 under load; as work
  (step × speed) from the idle's to a quarter to a half of it through
  the middle. **So it is not a share of the charge that 3 loses** — a
  cylinder short of compression or of fuel in proportion would stay a
  fifth short — **and load at the same speed lifts it** (idle speed,
  b7 27 → 57: −24 → −9 %), which a leak past a seat, set by time and
  pressure, would not do. *Load helps*, measured. **Cylinder 4 is the
  other way round**: 2–4 % under 1 from 1,600 rpm up at every load
  from part to full, in both periods, growing a little to the top
  (+0.8 to +2.1 rpm of step at full load against the overrun's +0.03
  to +0.25) — **a share, not an amount** (S4).
- **B. What weak strokes cost at full throttle: nothing that shows,
  and the standing difference about 1–2 %.** `--weak`: every stroke's
  step against its neighbours, 100,000 strokes at b7 140 and over.
  Noise is as often over as under; a misfire is only ever under. The
  noise there is 3–5 % of a stroke (2 rpm against a stroke's 45–70),
  so half a stroke lost would stand out twenty-fold: **strokes a half
  under 0.1–6 per 1,000, a half over 0.7–6 per 1,000** in every band
  (most of both are gear changes and the pedal coming on inside a
  window); **the excess under is −0.1 to −0.8 % of the work — none**.
  At part load the same (±0.2 % in every band of 10,000 strokes and
  more; the one small band that stands out — `19`–`37`, 2,820–4,200
  rpm at b7 90–140, 72 strokes of 4,456 a half under against 10 over —
  is bursts inside single seconds on all four cylinders, the driveline
  at a gear change or the pedal lifting, not a cylinder). At a standing idle the same measure
  reads +0.4 to +0.5 %: 17–27 strokes per 1,000 a quarter under
  against 8–14 over. **So at full throttle no stroke misfires or
  half-fires, on any cylinder**, to within about 0.3 % of the power.
  What is there is the standing difference: if 3 gave what 2 gives and
  4 what 1 gives, the engine would give (1 to 3 + 2 to 4) / 4 =
  **about 1–2 % more**, on the scale above. *What all four might lack
  alike cannot be seen this way* — D.
- **C. Against 014** (`--vcds`, 24 driving logs beside their captures;
  the pick's control 5 s before and after each rise, S3, *Against
  chance*): **moving at up to 1,200 rpm** — crawling, moving off —
  **014 counts what it counts standing**: since the VW leads 24 of 36
  rises on 3 (67 %, the control 36 %), 4 22 %, 1 and 2 6 % each; up to
  18/10 3 and 4 alike (17 and 16 of 38), as at the idles then.
  **Above 1,200 rpm it hardly counts**: 59 rises in all the logs, 20
  of them with the engine pulling (b7 45 and over), **one above
  2,820 rpm**. The 20 are real — the stroke before them 40–57 % of a
  stroke down, the control's 16–18 % — and they are nobody's: 8 on 1,
  7 on 3, 2 on 4, 3 on 2. So the ECU's count and the bus agree off
  idle too: next to no misfire under load. (*The session before's "smears
  onto 1 above 1,200 rpm" was 82 rises on a cruder measure; with the
  scale and the count above it is 4 of 9 since the leads — too few to
  name.*)
- **D. Whether b7's maxima are a healthy engine's** (`--pulls`). b7
  cannot say: it is the ECU's model from air and spark, and its scale
  here was *set* so that the full-throttle plateau reads the rated
  torque (`docs/firmware/frames.md`, *The scale*). **The car's own
  acceleration can**: 76 full-throttle pulls in 3rd and 4th, each
  second's acceleration turned into crank torque against b7 less the
  drag line × 1.06. **The car's mass is the registration
  certificate's, 1,303 kg in running order** (*the owner's photograph*,
  12/11 night; by the EU's definition with a 75 kg driver and the tank
  nine tenths full; *1,400 kg was assumed until then, and read 1.00*);
  the rest is assumed, none read off this car — CdA 0.84 m², rolling
  0.012, driveline 0.92. **The median pull needs 0.95 of what b7
  claims, half of them 0.89–1.04** (the spread is the road's slope; by
  capture 0.82–1.15); band by band 147–156 Nm at 2,000–5,000 rpm,
  130–137 at 5,000–6,000. Every 50 kg the car carries over the
  certificate (a heavier driver, the laptop, the boot) is 3.5 % more,
  and the assumed resistances are worth some 5 % either way. **So the
  engine gives its rated torque to within a tenth, and nearer a
  twentieth under than over; a fifth missing would show.** With B:
  nothing found that a healthy AQY would do better at full throttle
  beyond the 1–2 % of 3 and 4 — a few per cent common to all four is
  neither shown nor excluded. *What would tighten it*: the car on a
  weighbridge as driven, and a pull each way on the same stretch.
- **What it bears on** (*reasoned*; **no fit-table symbol changes**;
  **the ranking: H4 above H20, agreed with the owner the same night**,
  *The idle's candidates, ranked*): **H3** (a leak at
  runner 3) and **H18** (oil at idle vacuum) predict exactly this
  fading with manifold pressure; **H7**'s one-injector form fits if
  the injector is short only at its smallest quantities, not if it is
  short by a share; **H1** (a seat on 3) fits the fading with speed
  but not the lift by load at idle speed — unless the seat acts by
  dilution, an exhaust seat that lets burnt gas back at the idle's
  vacuum, rather than by lost compression, which 12 bar on all four
  already spoke against; **H4**'s weak spark on 3 is
  against — the spark is hardest to make at full charge, where 3 is
  within 1–3 % of 2 — **and its injector branch gains the most**: an
  injector that opens late loses the same fuel at every injection, a
  large share of the idle's and next to none of full load's, which is
  the shape measured, where "a steady 9 % in every state" had been
  held against it; **H13** stays as it was (a flake on a seat acts
  like H1's leak; a crust that dilutes the idle's small charge fades
  with load). Cylinder 4's 2–4 % is S4's to carry.
  **List A is not read by any of this** (*the owner's question*, 12/11
  night): the timing belt, H0 and the rest of the common part act on
  all four alike, which a comparison between cylinders cannot see.
  D alone touches the belt, weakly against (no tilt of the full-load
  torque from low speed to high; the row A1).

### What the dip shares said, and what stands

From 9/10 to 11/11 the cylinders were named by **the share of the dips
on each firing slot** — `cutscan.py --shares`, `--name` and `--pairs`,
`dipshape.py --name`, and on 9–10/11 an ad-hoc naming by the strongest
slot on the same count. **Removed 12/11 at the owner's decision**: the
count slipped and the crank wheel's alternation was left in (*The
count that does not slip*, above). Their tables, capture by capture,
are in git (`git show 296a5d7:docs/engine-health/open.md`, the
subsections *One cylinder or two* and *The dips keep to one slot*);
nothing here rests on them. What they concluded, against `cylscan.py`
(S1, *Every stroke named*; warm unless said):

| read with the dip shares | by `cylscan.py`, 12/11 |
|---|---|
| two thirds of the dips on two neighbours, **4 first, then 3** (`31` named by its cuts; `09`–`38` pooled) | **3 alone**: `31` 3 −15 %, 54 % of the weak strokes; 4 −3 % |
| **all four alike after the VW leads** (`40` 58 %, p 0.77; `41` cold, named, 31 % on 3) | 3 −14 % with 64 % on `40`; 56 % on `41` cold |
| one slot again on the original map (`42` 45 %); `43` named, **43 % on 3** | 3 −10 to −18 % with 58 % on `42`, −13 % with 62 % on `43` |
| `44` 48 % on 3 before the clean, **`46` all four alike after it** (p 0.01) | 58 % → 38 %, 4's weak strokes as many as 3's at stop 7; **3's deficit −11 % → −10 %**, its floor kept |
| `47` 3 leads again, 41 % | 73 %, the swell back |
| a steady pattern, **3 and 4 weak, 2 strong** | **3 weak, 4 level warm since October**, 2 and 1 strong; 1.7 rpm of the old pattern is the wheel |
| before 24/9: 4 and 3 weak, cold 4 most (`18`) | `09` 3 −19 %, `12` −11 %, `17` −23 %; `18` cold 4 −14 %, 3 −5 % |

**So the one conclusion that changed is the pair**: there was never a
second weak cylinder warm since early October, and never "all four
alike" — every reading that used one (H3 runner 4, H4 the loom at 3
and 4, H15's ends on 3 and 4, the 24/10 demotions for "the dips no
longer keep to 3 and 4") is re-read in its own entry.

**What stands unchanged: P0303 at `43`'s cut** (3/11 evening; the
dips in the cut named at the cut's own phase, where the dead slot
holds the count and nothing slips). 3 dipped on its own in the cut, 5
of the 7 dips there and none on 2 — 5 in about 375 of its strokes,
twice its rate outside, but 1.3 %, under the 2 % VW sets for a code
(`vcds.md`). **Where it came from** (3/11, at the owner's question):
the last read before it was empty, at the start of the warm VCDS run
(17:19, VCDS clock), after the pulls; between it and the cut came 16
minutes of driving with full-throttle runs to 6,258 rpm (the capture,
17:20–17:24) with **014 at 0 through them and to 17:28**, then 12–24 at
the town stops and the crawling between them, and the warm stop's idle
counts — counts like these never stored a code in any session before.
So it came with the cut, not with hard driving. **Not the ECU charging
4's misses to its neighbour by habit**: the same cut on 4 twice on
10/10 (warm) and once on 24/10 (cold) stored no P0303 (`idle-log.md`).
*Reasoned*: with 4 dead the total ran far over 2 %, and in that window
the ECU named the cylinders it had counted, 3 among them — real
misfires on 3, named because 4's pushed the window over; on its own 3
would not have set it. The lamp at the cut is 4's. **This ECU stores
no freeze frame** (*owner*, 3/11), so the fault memory holds only the
codes and their status. *On 12/11 P0303 was stored without any cut*
(S3).

**After every captured session** each cylinder's deficit, weak strokes
and 014's rises are reported to the owner from `tools/cylscan.py`
(`CLAUDE.md`).

---

## What the forums say about this idle

Searched 27/9, 9/10 and 20/10, in German, Polish, Czech and English (forums
and search extracts; leads, not sources). **The finding is the pattern:
almost nobody reports a fix.** Every AQY thread with this picture that could
be read to its end stops unresolved after the same parts list this car has
been through. What was reported as fixed: a new battery, a new Bosch coil, a
new lambda probe, **original VW leads instead of aftermarket ones**, rings
and a head going-over, a sticking bucket tappet, the timing belt a tooth out.
Most of these are already done here; the belt's marks were read 13/11
(not settled; the full-throttle air against 30–60°, the row A1) and the belt is to be renewed (`plan.md` 8q).

**A remap that made the idle worse** (searched 28/10 at the owner's
request, Czech and English): **no AQY, 2.0 8v or Motronic M5.9.2 case
found**, and no thread where going back to the stock map was the fix on
such an engine. What there is, all general and none a source: Czech
tuners' own pages say a poorly made map can give an uneven idle
(raziteam.cz, radyprovsechny.cz); a flash clears the adaptations, so the
idle can read worse for a few drives until they relearn
(nefariousmotorsports, "Rough idle after remap"); and **HP Tuners'
material on MAF scaling says a scaling error shows most at idle, where
the flow is lowest** — the mechanism H19 rests on — with owners of tuned
cars reporting idle trouble after a MAF of a different make, gone with
the original. **The owner's recollection** (28/10, uncertain, nearly ten
years back): the tuner may have warned that the idle could get worse.

**P0172 and a negative idle trim on this engine** (searched 25/10, the
same languages): **no AQY thread with a reported fix.** The general
lists agree with VW's (`vcds.md`, block 032): a leaking injector, fuel
pressure too high, a purge valve stuck open, the MAF, the probe, **and
fuel in the oil** — Mazda SA-026/18 and GM PIP5647A, both for
direct-injection engines and both with the oil level rising (`refuted.md` C21). New Beetle forum leads, unread to their end (the
pages refuse automated reading): the short vacuum hose to the fuel
pressure regulator, N80. Overfilling the tank past the first click is
named as a way to flood the canister (*general*; H16).

**The idle air regulation, 055 and P1582** (searched 26/10, English and
German, for H8): **no source gives typical values of 055's learnt value
on this engine, and none relates it to 014** — the one specification is
still VW's own, −1.50 to +1.50 g/s and negative on a run-in engine
(`vcds.md`), which every reading here except the stick's has kept inside.
A German overview gives 055 in per cent for other ECUs, so the g/s scale
is this ECU's label file and not general. **P1582 on an AQY**, in one
motor-talk thread read only in search extracts: a cracked vacuum hose to
the brake servo, unmetered air, with the additive lambda learnt value
high (the opposite sign of this car's 032), cured with the hose and the
adaptations reset. The general P1582 lists name air leaks, the injectors,
the fuel pressure regulator, the throttle and oil dilution. Throttle
cleaning and a relearn are the usual advice; one AQY extract says the
stutter got *worse* after a relearn. **One more AQY thread with this
picture** (golf4.de, 2012, read in full): a warm idle that stutters now
and then, dipping from 800 to 760 rpm only in the stutter, driving fine,
the probe, plugs, leads, coil, coolant sender and MAF replaced and the
throttle cleaned and adapted — **unresolved**, like the rest.

**Pictures of the inside of this engine family** (searched 21/10, the same
languages): **none found** that would compare — no borescope or head-off
photo set of an AQY, AEG, APK or AZJ with its mileage. The one general
reading that bears on it is ExxonMobil's borescope guide for gas engines
(*A Basic Guide to Borescopic Inspection*, §3): some crown deposit is
normal and *"should be evenly distributed. Uneven deposit distribution is a
sign for non-homogeneous thermal dissipation"* — the amount on this
engine is not judged against anything, its **unevenness, 3 > 4 > 2 > 1**,
is the finding (H13).

**Searched again 4/11** (DE, PL, CZ, EN; VW's manual as transcribed,
Ross-Tech; the notes are not kept here): **still no AQY/AEG thread with a
confirmed fix for an idle-only misfire on one cylinder**; the confirmed
idle-only cylinder-3 fixes on other engines were all at the valve (lash,
a burnt valve, a broken spring; *forum leads*). **VW, read**: compression
new 10–13 bar, wear limit 7.5, **largest difference 3 bar** — so 12 even
excludes only a gross loss (`refuted.md` A4); 014 is the total only,
specified 0–5 at 740–820 rpm and 15–35 % load, with no per-cylinder
group; **misfires from an ignition output are stored in pairs** (1+4,
2+3), which no code on this car has done, so neither the coil nor its
output stage; **P1300 / 17708 is a misfire put down to an empty tank**,
so captures run above reserve; P1237–P1240 are injectors N30–N33. **Not
found**: an AQY TSB on the idle, a crank-wheel adaptation procedure.
**A generic OBD-II read** (VCDS's OBD-II mode, read only) after a stored
P030x may show mode 02's freeze frame or mode 06's misfire results
though the VW view shows none; whether M5.9.2 supports either is not
known. **The photos read again** (the same 37): 3 the only crown whose
layer has broken into sharp-edged islands (flaking), a raised rim on its
exhaust valve face; no burnt margin, no steam-clean crown, no oil-wet
deposit anywhere; 4's crown-line mark undecided (a deposit edge or a
crack) — one frame of it again whenever the borescope goes in.

**Hydrogen decarbonisation, searched 4/11 evening** (*the owner's
request*; EN, DE, PL, CZ; H13, `plan.md` 8). **What the machines make**:
water split by electrolysis into hydrogen and oxygen, 2 : 1, fed to the
intake — from about 280 l/h (a German workshop's figures, about 0.8 % of
hydrogen in the intake air) to 30 l/min, about 1 kg an hour. **The
vendors' chemistry does not hold** (*general*, *reasoned*): hydrogen
taking up the carbon as methane (C + 2H₂ → CH₄) needs a catalyst, a
hydrogen pressure of tens of bar and minutes of contact, where the
cylinder offers a hundredth of a bar for milliseconds, and at flame
temperature the equilibrium runs the other way; the water-gas reaction
(C + H₂O → CO + H₂) needs the carbon at about 600 °C and more, which the
workshop itself gives as its limit, against a chamber wall of a few
hundred. **What can act**: hydrogen's flame burns closer to the walls
than petrol's, and its water may flake deposit (SAE 2000-01-2858); the
carbon that does leave goes as CO₂ and CO, as from any burning, and
the ash of the oil's additives, which the deposits carry, does not burn
at all — it can leave only as flakes. **Independent evidence**: one
study (Sci. Rep. 2026, s41598-026-54105-y): a 2001 Škoda Fabia 1.4,
about 1 kg of HHO in an hour, idle alternating with 3,000 rpm — **no
change** in power, fuel per kWh (287.2 → 287.0 g/kWh), cranking current or
the idle's HC; deposits not measured. It cites one diesel tractor whose
exhaust valve's carbon cover went from 65 to 15 % (not read). No ADAC or
magazine test found; Polish owners split, some mechanics against it on
engines over 20 years old (a seal may start to leak); the rest is the
sellers'. **Read for this car** (*reasoned*): the hours above 4000 rpm
on the 44K tanks heated the chambers more than an hour at 2,000 rpm
without load and moved nothing, so what the clean adds is hydrogen's
flame at the wall and the water — expected small, cheap to try, and
still the one repair that reaches 3's crown without the head off.
**Done 9/11** (an 800 l/h machine at about 60 %, about 8 l a minute of
the mixture): 3's excess gone at the stop after it, 4's and the settled
level kept (S1, *The clean of 9/11*) — not "no change", one stop each
side. **At idle the gas itself made the idle the calmest on record**,
which the study's idle HC could not show.

**Searched again 11/11** (*the owner's request*, the second deep
research; DE, PL, EN, Czech not reached; manufacturers' and SAE pages
read as abstracts, forums as leads; the notes are not kept here).
**Still no AQY/AEG/AZJ/APK/AVH/AZG case of an idle-only misfire on one
cylinder with a confirmed fix**; the one family case with a confirmed
cause is an AEG timing belt a tooth out, and it stored a code. What is
new:
- **Deposit flakes on the exhaust seat** (Shell, SAE 2000-01-2858,
  2002-01-2833, 2003-01-3187): trapped by chance, a leak that switches
  on sharply once enough deposit is lost (about 55 µm), **water the
  strongest trigger of flaking**, harder driving less of it. No source
  gives how fast seat deposit forms again; the one time base found is
  about 200 hours for inlet-valve deposit on a port-injected engine
  (SAE 922263) — so **a day's relief fits a flake moved, not deposit
  regrown** (H13, H1).
- **The tappets** (VW's procedure for the 2-valve 2.0, read from its
  SEAT and Škoda pages): **"irregular valve noise on starting is
  normal"** — the clatter of 8/11 at −2.5 °C is VW's normal. The check:
  the fan in once, 2,500 rpm for 2 minutes, the cover off with the cam
  up, more than 0.2 mm of play renewed, else the tappet pressed with a
  plastic wedge and a 0.2 mm feeler tried. It finds a soft tappet, not
  one stuck pumped up, which only a leak-down or a warm compression
  shows (H1).
- **The timing belt**: VW's fault table has **16725 / P0341, G40
  implausible signal**, and Ross-Tech names a misaligned timing among
  its causes; an AEG forum case with a tooth off set P0340/P0341. So an
  empty fault memory is weak evidence against, not proof: whether this
  M5.9.2 runs the check is not confirmed. **Read again 13/11**
  (*the owner's questions*: could 30° be misjudged, which way a belt
  slips, would an engine like this keep its power more than a tooth
  out): **Motor magazine on the 2.0 ABA, the same family** (8/2003 and
  9/2003, VW specialists interviewed): an engine with the belt one or
  two teeth off "may still run smoothly", but "will lack power, and both
  emissions and fuel economy will be terrible", and it is "very likely
  to trigger a P0341" — one shop puts nine in ten P0341 on these engines
  down to a stretched or misfitted belt. Forum reports on the ABA and
  AEG agree in kind: a tooth advanced, "lots of low end, no top end"; a
  tooth retarded, a bog at low speed; a tooth given as about 8° of cam.
  **No measured case of two teeth or more was found**, on a dynamometer
  or otherwise. **The marks**: the same article names the camshaft
  sprocket's OT against the arrow on the rear cover and **the flywheel's
  mark in the gearbox window** as the marks to set; the crank pulley's
  notch is on the ABA set against a chisel mark on the intermediate
  shaft's sprocket, and forum posts on the AEG set it against a raised
  line on the lower belt cover — whether the AQY carries a mark on the
  block as well was not confirmed either way (*the owner*: the web
  shows the notch on the pulley and one on the block, as he found).
  **Which way a belt slips** (*reasoned*; the search gave anecdotes both
  ways): the crank drives, so a belt that jumps or stretches leaves the
  cam behind — retarded, the pulley's notch past its mark with the cam
  at OT; **8i read the notch short of it, the cam advanced, which a slip
  does not give — only a belt fitted so in 10/2017**, or a misread.
  So what is left is a misjudged angle (*the owner's own doubt*: the
  borescope and a finger in a cramped place) or a belt a tooth out
  since 2017; the flywheel's mark with the cam at OT would read it to a
  few degrees with no plug out. A tooth acts on all four alike
  and cannot by itself part 3 from 4. **SAE 972936** (idle, the overlap
  moved 10° later): less residual but a longer burn and *more* cyclic
  variation — the effective compression ratio, not the residual alone.
- **A leak at one runner** (trade sources): the lower gasket the usual
  cause of a one-cylinder idle misfire; its signature a trim positive at
  idle and falling with speed. This car's negative idle cell rules out a
  leak large enough to move the whole trim, not a small one at 4; at
  idle vacuum the leak is choked, a fixed flow against a charge that
  grows with load (*reasoned*), and a smoke test pushes the other way.
- **The idle's physics** (Heywood; SAE 972936; Ji and Wang, *Int. J.
  Hydrogen Energy*): residual gas, burn duration and the early flame
  kernel set the idle's cyclic variation; a higher manifold pressure
  lowers the residual (the calm under load); **hydrogen at idle halved
  COV of IMEP at 6.5 %** and moved the lean limit far — studies at 1 %
  and less were not found. A faster flame rescues borderline strokes
  but cannot supply a missing quantity of air, fuel or compression,
  which is why the gas took the dips and left the steady pattern (S1,
  *The gas idle taken apart*). Bosch's crank-speed misfire detection
  (SAE 930399) is built for full misfires; partial burns at idle are
  its hardest case, so 014 is a lower bound (S3).
- **The probes** (Bosch, Denso, SSP 175 German edition): contact spray
  forbidden on their connectors (S23); the signal earth a wire of its own
  to the ECU, so a cracked earth shifts the reading only through a
  leakage current; **the rear probe's failure leaves the front loop
  running** and could push only rich; the rear loop not documented at a
  warm idle. **VW's list for a low learnt value** puts *"low at idle,
  part load normal: possible oil dilution"* first, then a leaking
  injector, high fuel pressure, N80 stuck open and the probe — oil
  dilution was settled against on 26/10 (`refuted.md` C21). The grey-
  beige crust of the old front probe matches no chart entry cleanly:
  coolant (green-white, grainy), oil (dark), fuel additives (red or
  white) — the cleaners explain it as well as coolant does.

---

## The idle's candidates, ranked

**A judgement, not a measurement**, for S1, S2, S3 and S14. **Mirrored in
Czech on the owner's private page *Pořadí hypotéz volnoběhu***, republished
with every change here (`CLAUDE.md`, the currency pass). Re-read after
every test and whenever the symptom list changes; the history of each re-read
is in git.

**Two lists since 12/11** (*the owner's decision*, the lists proposed by
Claude): the idle is two things on top of each other, and they are
measured apart. **The steady pattern over the cylinders** — 3 weak,
4 level, 2 and 1 above (*read 12/11; "3 and 4 weak" until then*) — **is
about a third of `IdleHealth`**: over 318 warm
loads-off windows the grade averages 78, and 51 with each window's four
slot means taken out (S1, *A steady pattern over the cylinders*); **of
that third, about an eighth of the whole grade is the crank wheel's own
alternation**, not combustion, and the rest 3's (*split again 12/11*,
the same section); the rough start of a warm stop after a hot drive is
3's swell (`43`, `44`). **The rest, about 51 of 78, has no pattern over the
cylinders**: the common part. A hypothesis goes in the list whose part
it can make; H7 has a form in each. **Which part the calm stops of
11/11 and 12/11 night lowered** — the owner's reading was the common
part, the canister (*owner*, 12/11) — **was read on the captured stop
of 12/11 (`49`; S1, *The first captured stop on the canister*):
neither.** 3 swelled after the hot drive as before and stepped to its
floor by itself; settled, the grade (37) and the common part (30) were
those of `44` after its cut and `48`, before the canister; only the
floor's length, fourteen minutes, was new. And 032's part-load cell
went back to +8.6 % (H16, S21). *Claude proposed H16 from first of A
to fifth the same day*; **the owner kept it first** (12/11; *third
since that evening, the re-read below*): the
canister is back but N80 itself is not changed, and a valve leaking
canister vapour explains the four 032 readings on the canister (H16,
*The owner's reading, 12/11*) — the new N80 decides.
*Reasoned*: purge vapour enters the intake at one point and need not
reach the four runners alike, so H16 is not ruled out of list B either.

**B. One cylinder — what makes 3 worse than the rest** (**first of
the two lists since 12/11**, *agreed with the owner*: the misfires 014
counts, 3's steady deficit and its swells; *this said "3 (or 4)" and
stood second until then* — "4's deficit" in the rows' older lines,
now in git, was the crank wheel's alternation, the re-read under the
tables):

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| B1 | **H13** deposits | **12/11 night, the phone at the tailpipe, kept with H1**: 3's exhaust pulse +11 % at −23 % and −7 % at −5 %, on its steady strokes too — the swell is 3's combustion on every stroke; a seat and a dilution both give it (S1, *The phone at the tailpipe through a swell and a fall*); **12/11 night, the queue drive, kept with H1**: three swells in one stop, the falls 80–108 s, the air, the spark and the regulation the same through them — still inside 3 (S1, *The queue drive, and what the ECU sees through a swell*); **12/11, the third research** (*agreed with the owner*): first, with H1, and for 3 by every measure — its steady deficit at every warm idle, 80 % of 014's rises, the swell and its step; the borescope's most deposit on 3 (3 > 4 > 2 > 1), and cold 4 weak beside it in that order; **12/11, the idle split in two** (*the owner's decision*): 3's exhaust seat or a flake, read with H1; **11/11, after the second research** (*agreed with the owner*): the rough start of a warm stop after a hot drive is 3's swell (S1, *The rough start of a warm stop*), and a day's relief fits a flake moved, not deposit regrown (SAE 2000-01-2858); **9/11, the clean**: it took 3's swell for a day and left its floor (S1, *The clean of 9/11*); **24/10**: its own test, the strong 44K tank and ~450 hard km, moved nothing, and the deposit reads as a consequence as much as a cause (H13). *Older re-reads in git (`git show 296a5d7:docs/engine-health/open.md`); those of 3/11–9/11 rested on the dip shares withdrawn 12/11.* | both 44K tanks done; **the hydrogen clean done 9/11**: the swell gone for a day, 3's floor and the settled level kept (S1, *The clean of 9/11*); with H1, a warm leak-down with 3 twice (`plan.md` 9) |
| B2 | **H1** valve or lifter | **12/11 night, off idle** (*agreed with the owner*; *Naming the cylinder*, *Off idle*): kept, **read as a seat that dilutes at the idle's vacuum, not one that loses compression** — 3 is within 1–3 % of 2 at full load and load lifts its deficit at idle speed; **12/11, the third research** (*agreed with the owner*): with H13 on 3 — a seat on 3 that leaks (the floor) or holds a flake (the swell), or a lifter; the steady pattern is 3's alone, as one seat gives; **12/11, the idle split in two** (*the owner's decision*); **11/11 night, kept**: S22 reopened, a tick once per cycle heard warm after a hard drive; **read 12/11: the usual once-per-cycle part at its usual size, no lifter's jump** (S22); **11/11 up from fourth** (*agreed with the owner*): 3's exhaust seat, leaking hot or holding a flake, fits the rough start after a hot drive that settles in 5–8 minutes; the weak strokes come in spells of seconds on one cylinder, at a mixture or dilution limit (S1, *How the weak strokes follow each other*); VW calls the cold clatter of 8/11 normal; **7/11**: the port photos of 20/10 show crust broken round the inlet seat's edge on 3 and 4, a lump on 3, 1 and 2 even (*the owner's reading*); **26/10**: the hot phone recording found no lifter, 18/10's tick not back. *Older re-reads in git (`git show 296a5d7:docs/engine-health/open.md`); those of 3/11–9/11 that weighed 3 against 4 rested on the dip shares withdrawn 12/11.* | the EPR flushes done 26/10, the hot recording found no lifter; left: **a warm leak-down on all four** and a stethoscope above 3, hot (`plan.md` 9) |
| B3 | **H3** a leak at one runner, 3's | **12/11 night, off idle** (*agreed with the owner*; *Naming the cylinder*, *Off idle*): kept third, **strengthened**: *load helps* measured, −21 to −26 % of a stroke at idle and with the pedal light, −1 to −3 % at full load; **the owner's reading** — a second cause that makes all four rich takes 032's negative idle cell out of the case against it (H3); **12/11, later the same day** (*the owner's argument*): one up, H7 below it; **12/11, the third research** (*agreed with the owner*): **runner 3's lower gasket**, never renewed — the one cause that predicts *load helps* directly; 3 short in every state, cold 4 weak beside it, the neighbouring runner; runner 3's gasket edge bent and straightened by the owner on 5/11, runner 4's torn; against: 032's idle cell negative, the smoke test of 9/10 clean, and a leak has no reason to swell and mend in a step; **4/11**: the calm under load best of all, the calm after revving not at all (S1). *Until 12/11 it was read for runner 4 ("4's deficit") and demoted 24/10 for "the dips no longer keep to 3 and 4" — both on the dip shares withdrawn 12/11.* *Older re-reads in git (`git show 296a5d7:docs/engine-health/open.md`).* | no test in place (the brake cleaner cannot reach, 24/10); the lower manifold off and its gasket renewed |
| B4 | **H4** the injector loom at 3 | **12/11 night, off idle** (*agreed with the owner*; *Naming the cylinder*, *Off idle*): **up one, above H20**: 3's deficit is an amount at a small charge and not a share — what an injector that opens late through a raised resistance gives, and the opposite of the "steady 9 % in every state" held against it; the spark side against, 3 level at full load; 6m ahead of the garage session; **12/11, later the same day** (*the owner's argument*): one up; the wiring is what stays with the cylinder through a change of injectors; **12/11, the third research** (*agreed with the owner*): the loom at 3 (its own branch after D95, its control wire to pin 58); a wire has no reason to cost a steady 9 % in every state or to swell and mend in a step; the load argument is against the spark side, not the injectors; **24/10**: flexed part-warm by the owner, by ear, no change. *Read for 4's circuit and for "the pair the steady pattern names" until 12/11, on the dip shares withdrawn then.* *Older re-reads in git (`git show 296a5d7:docs/engine-health/open.md`).* | VCDS 004 beside 014; the circuits measured (`plan.md` 6m, 6n) |
| B5 | **H20** coolant into cylinder 3 | **12/11 night, off idle** (*agreed with the owner*; *Naming the cylinder*, *Off idle*): one down, H4 above it; it predicts the fading with load as H3 does, with the level and the crown against it as before; **12/11, later the same day** (*the owner's argument*): one up; **12/11, the third research** (*agreed with the owner*): one up, H4 below it; **12/11, the idle split in two** (*the owner's decision*): coolant into 3; **10/11 evening one down** (H21 added above it); **9/11 late evening one down** (H11 above it); **added 4/11** (*the owner*, weak): one cylinder at idle, where its pressure is lowest; plug 3 the cleanest of the 10/10 set; against: the level holds (*owner*), no emulsion, no steam-cleaned crown in the photos | a combustion-gas (CO₂) test of the coolant (`plan.md` 9) |
| B6 | **H7** fuel delivery — one injector, 3's | **12/11, later the same day** (*the owner's argument*): **from third to last**: 3 was the weak one on the old injectors in August too, so the injector itself is unlikely, and the exchange of injectors 3 and 2, agreed earlier that day (`plan.md` 6o), is withdrawn; **12/11, the idle split in two** (*the owner's decision*): its one-injector form, the rail's in A4; plug 3 the cleanest; S19's side is A4's and H16's. *Older re-reads in git (`git show 296a5d7:docs/engine-health/open.md`).* | **no injector swap** (*the owner*, 3/11; agreed and withdrawn 12/11); a rail gauge (A4) |

**A. The common part — what makes every cylinder alike rougher**
(the small unevenness on all four, most of `IdleHealth`'s floor and
nothing 014 counts; second since 12/11):

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| A1 | **the timing belt a tooth out** | **13/11, the marks' 30–60° set against the air and the acceleration** (*the owner's question*: whether the ECU would know, b7 being its own belief): b7 is computed from the measured air, so it follows what the cam does to the filling and misses only what the cam does to the work got from it — and the acceleration reads that; **settled full throttle (the throttle at 80° or more for 1.5 s, every 003 log but the short-of-air pulls of 3/11): 504 mg of air a stroke at 2,000 rpm, 496 at 2,400, 484 at 3,200, 520 at 3,600–4,400, 502 at 4,800, 485 at 5,200, 452 at 5,600, 418 at 6,000 — 5,200 within 2 % of 2,400, 85–90 g/s at the top**; the acceleration in 3rd and 4th needs 145–152 Nm in every band from 2,000 to 5,000 rpm and 130–137 from 5,000 to 6,000 (83 pulls, 0.94 of b7; rated 170 and 156 at 5,200); the warm idle takes 3.1–3.5 g/s at 2–4° of advance, as specified; **against 1.5–3 teeth outright** — that much advance would take the top of the filling away (*general*) — **and no lift of the low end against the top that one tooth of advance would give, though with no healthy AQY measured a tooth or less is not excluded**; so the notch read on 13/11 or the groove it was set against is not the timing mark, **or the angle was misjudged** (*the owner*, the same day: the marks are the web's, the borescope and a hand in a cramped place may well have made 30° of less; and a slip would have gone the other way — *What the forums say*, the timing belt: Motor magazine has the ABA running smoothly one or two teeth off but short of power and very likely with P0341, and a slipped belt retards the cam) (*reasoned*); where the true mark is was not looked up — a flywheel mark through the gearbox window or the pulley's notch against the lower belt cover are usual on these engines (*general*, from memory, not checked against VW's manual), neither of them a groove on the block; by gear, the acceleration against b7: 3rd 0.96, 0.97, 0.92, 0.94 and 4th 0.90, 0.97, 1.04, 1.00 in the bands from 2,000, 3,000, 4,000 and 5,000 rpm — no tilt (`drivescan.py --pulls`, all fifty captures); the air by log, at 5,000–5,500 rpm: 84–90 g/s in sixteen logs from 9/2026 to 9/11 (medians by 500 rpm band), lower in two — the short-of-air pulls of 3/11 (76) and `vcds-step8-home-2-014-001-003.csv` (78–83, nine samples, not read further) — so nothing moved over the autumn either; **kept first by the owner after this reading** (13/11, asked whether it should go below H0: no, until the belt is renewed); **13/11, its marks read (8i), kept first** (*the owner*; the paragraph under *Where it stands*): the cam's OT mark set, **the crank pulley's only notch 30–60° of crank behind the groove on the block**, by eye and borescope — **for it if both marks are the true ones**, 1.5–3 teeth, **the cam advanced** (the direction the owner's, read off the part: the crank clockwise, the notch short of the groove; *until his word, "may be mirrored from below"*); against, 2–3 teeth of advance would lift the low end and cost the top, and the full-load pulls below are flat, so the size is unsettled; the piston at plug 1, which settles it, declined (*the owner*); **the belt renewed at a garage** (8q, *the owner's decision*), the mechanic to read the old marks before it comes off; **12/11 night, off idle, kept** (*the owner's question*; *Naming the cylinder*, *Off idle*): what this session read is one cylinder against another, and a belt moves all four alike, so 3's and 4's figures say nothing for or against it; **two things do bear on it, both weakly against**: at full throttle the car's acceleration needs 0.91–1.04 of what b7 claims in every band from 2,000 to 6,000 rpm, **with no tilt from low speed to high**, where a cam a tooth out moves the filling from one end to the other (*general*), and the whole is within a tenth of the rated torque; a tenth is also about what a tooth could cost, so the marks (8i) still decide; **12/11 evening up from second to first** (*agreed with the owner*): the common part is a constant — the same within 5 % at every warm idle since 24/9, answering only to a load, the gas and temperature — which a fixed fault on all four gives and a source that varies by the day does not (S1, *The swell's shape, and what the common part follows*); **12/11, the idle split in two** (*the owner's decision*): all four cylinders' timing alike; **11/11 kept, but its marks looked at first, being free** (*agreed with the owner*); VW's fault table has 16725 / P0341 for a G40 signal out of place, so an empty memory is weak evidence against (*What the forums say*, 11/11); **10/11 evening one up** (H11 down, *agreed with the owner*); **9/11 late evening one down** (H11 above it); **9/11 evening up from ninth** (*agreed with the owner*): the gas idle names the dips a burn at the dilution edge, and the cam's timing sets the exhaust kept at idle through where the valves' overlap falls against the piston (one camshaft, so its length cannot change), with compression even and the full-load power nearly intact (S1, *The gas idle taken apart*); belt from 10/2017; a forum fix | its marks, read 13/11 (8i): the crank's notch 30–60° off by eye, not settled; **the old belt's marks read by the mechanic before it comes off, and the common part by capture before and after the new belt** (`plan.md` 8q); even compression and the full plateau argue against; **the ECU would not necessarily say** (*the owner's question*, 9/11): the AQY has a Hall sender G40 on the camshaft, which SSP 175 (p. 49) describes only as identifying cylinder 1, with the advance retarded as an emergency function if it fails — no check of the cam's angle against the crank is described, unlike engines with variable cam timing; so a tooth off may store nothing, and no G40 code has been read on any session since 9/2026 |
| A2 | **H0** normal for this engine | **12/11 evening up from ninth to second** (*agreed with the owner*): a common part that no repair, day or drive has moved, and that answers only to the charge, is what an engine's own scatter looks like; a fixed fault reads the same and no healthy AQY says which (S1, *The swell's shape, and what the common part follows*); **12/11, the idle split in two** (*the owner's decision*): the floor left when every fault is gone; **10/11 evening one down** (H21 added above it); **9/11 late evening one down** (H11 above it); **9/11 evening one down**; no healthy AQY recorded; 014 far above VW's 0–5 against it | 014 on a healthy AQY, VCDS only; a capture is not obtainable |
| A3 | **H16** the purge path (the valve, the canister bypassed) | **12/11 night, the queue drive, kept**: 001 at three rows a second swung the same through 3's swell, its fall and the floor; 032 moved towards zero on a gentle hour, against the owner's reading's gentle half; `49`'s long floor did not come again on the same hardware (H16); **12/11 evening down from first to third** (*agreed with the owner*): the common part read 2.7–3.1 rpm rms by capture on the bypass and on the canister alike, gentle days and brisk, where a leak following the canister's load would move it (S1, *The swell's shape, and what the common part follows*); the purge phases kept as a weak reading of 3's swell, tested by 8o; **12/11, the idle split in two** (*the owner's decision*): the common part's first: the two calm nights on the canister; **12/11 up from sixth to third** (*the owner's decision*: "H16 higher"; third proposed by Claude): the two calmest warm stops on record outside the gas came on the two nights since the canister went back, the only change they share — the one hypothesis with a change that moved the settled floor, so above H3, H4 and H7, which explain the one cylinder's part but have had no change that moved anything; below H13 and H1 because it cannot pick a cylinder; **the new N80 not yet fitted** (`plan.md` 8a), the valve half of it untested warm; **11/11 night, kept**: the first drive on the canister relearnt 032's part-load cell to +2.3 % where the bypass held +6.3 to +7.0 — for it, **held on 12/11's second drive (−5.5 / +2.3)**; the idle cell back near −6, not moved by the canister (S21, *The first drive on the canister*); **both nights' stops near home the calmest on record outside the gas, 12/11's for about 13 minutes with 014 at 0.04 % — the canister the one change they share** (two stops; H16, *12/11 night*); **11/11 evening up from twelfth** (*agreed with the owner*): the canister found bypassed, the tank's line straight to N80 (S21) — raw tank vapour at every purge, rich when warm: P0440 in winter and a warm rich source fit it; it still cannot pick one cylinder; **10/11 evening one down** (H21 added above it); **9/11 late evening one down** (H11 above it); **6/11 night down from seventh** (*agreed with the owner*): out of the car the valve hardly passed air unpowered, and its pulses do not line up with the dips (H16, *The valve's pulses against the dips*); before that **6/11 evening up from eleventh**: P0440 and the engine lamp (S21), the system's own fault code; VW lists N80 open among the causes of 032's low idle value; purge comes in phases, as the weak firings in pairs do (the idle's 1½-min waves turned out the radiator fan, S1); a common stress on the weakest cylinders, not their difference (H16, *a common cause of the idle?*). Against: roughest cold, when the valve is not driven; 25/10 cold, the canister closed off, the trim unchanged; no liquid (6e) | **the canister plumbed back, done 11/11, its first drive read** (S21); 032 after drives without a reset (`plan.md` 8f); then the valve ordered 11/11 (*the owner*), in hand 13/11, fitted about the weekend, 032 before and after (`plan.md` 8a); 6/11 night, out of the car, it hardly passed air unpowered |
| A4 | **H8** throttle and idle control | **12/11 night, the queue drive, kept**: 003 at three rows a second — the advance's scatter does not go with the common part (H8); **12/11, the idle split in two** (*the owner's decision*): the air and the idle regulation, all four alike; **10/11 evening one down** (H21 added above it); **9/11 late evening one down** (H11 above it); **9/11 evening one down**; **down 27/10 from third** (*agreed with the owner*): 055's two fields sum to the same correction at every warm idle, so a reset or the A/C gives no more air and the regulation half has no mechanism (H8); what is left is S20, a little better since the cable and the pedal (27/10) and still there; before that **up 26/10 from seventh**: S20 dates from this throttle (*owner*); 014's counting read as following 055's learnt value (`refuted.md` C19, **refuted 2/11**), and 26/10 showed a wrong learnt value spoiling the idle and the starts; the owner's hypothesis that the regulation itself narrows the margin (H8); all four alike | 055 against `IdleHealth` from zeroed adaptations (`plan.md` 5a); 6k (27/10) showed the A/C's calm with the learnt value aside, but not as the whole |
| A5 | **H7** fuel delivery — the rail's pressure | **12/11 evening** (*agreed with the owner*): against — the common part is the same after high revs as after none; one down, H0 above it; **12/11, the idle split in two** (*the owner's decision*): its rail-pressure form, all four alike; **12/11 one down** (H16 above it, *the owner's decision*); **11/11 kept** (*agreed with the owner*): a hot rail after a hot drive fits the rough start's time, not its one cylinder; **10/11 evening one up** (H11 down, *agreed with the owner*); **9/11 late evening one down** (H11 above it); **9/11 down from fourth** (*agreed with the owner*): H3 and H4 above it; **down 3/11 evening from first to fourth** (*the owner*: the injectors are new, 9/2026); never gauged; **demoted 25/10 night from second**: the regulator answers its reference (`refuted.md` C20) and a high base pressure does not fit 032's positive part load, so what is left of it is mostly for the starts — **closed 31/10 as the fuel** (`refuted.md` D2), which leaves S19; **S19 fits it** (24/10), shared since with H16; one code so far | a rail gauge — **the owner buys one if the map does not help** (29/10) |
| A6 | **H21** the probes' wiring and connectors | **12/11, the idle split in two** (*the owner's decision*): the probes' readings steer all four alike; **11/11 one up** (H11 below it, *agreed with the owner*): S23 explained by the broken terminal and, for its sinking, the contact spray (S23); **added 10/11 evening** (*agreed with the owner*): the harness side was not changed with the probes, so what the swap could not rule out lives here — **S23 in full** (the new rear probe's signal pulled down under load and to zero, then back), and **S19's idle cell** if a signal earth carries heater current, which is highest at idle (*reasoned*); **for the idle itself weak**: on 10/11 morning the new rear probe read healthy for 18 minutes and the idle was as rough (H21) | the connectors seen from the harness side cold (`plan.md` 8e, postponed to the end 11/11); 036 watched at VCDS sessions (8f; 8g dropped 11/11, *the owner*); each wire to the ECU's pin with the plug off (with 6n) |
| A7 | **H11** both probes shifted | **12/11, the idle split in two** (*the owner's decision*): as H21; **11/11 one down** (*agreed with the owner*): the rear probe's state never tracked `IdleHealth`, and its failure leaves the front loop running (SSP 175); **10/11 evening down from third to seventh** (*agreed with the owner*): on the relearn drive its marks 1, 3, 4 and 5 failed and mark 2 was spoilt by the rear probe's own fault; the calm of 17:38 came before the clear (H11, *The relearn drive*); what is left of it, the probes' circuit, is H21; **9/11 late evening up from thirteenth** (*agreed with the owner*): in its idle-only form — the front probe reading rich at idle's cool exhaust only, so the real idle mixture lean — it fits every pattern of S1 (queuing worse, a brisk drive better, a load calming, hydrogen curing), the negative idle cell with part load untouched, and P0172 once (H11, *Re-read 9/11 evening*); 2017 probes | **036 read 9/11 night**: the rear probe sinks towards lean at every idle, heaters good — for, not proof (H11, *The reading before the swap*); **both probes replaced** (*the owner's decision*, 10/11; no analyser, which he declines) and the same reading after it (`plan.md` 8c) — it rules out the old probes, not the mechanisms (H11, *What the rear probe can and cannot say*); **read after, 10/11**: the new rear probe flat for 18 minutes of idle, then the front's swing; **the idle unchanged** — mark 2 met, marks 3 and 4 failed at the first stop (H11, *The reading after the swap*); **mark 1 failed on the relearn drive, 10/11 evening** (032's idle cell back to −6.3 % within 37 minutes), marks 3–5 failed again, mark 2 spoilt by the rear probe's own fault (H11, *The relearn drive*; S23) |
| A8 | **H2** a leak ahead of the converter | **12/11, the idle split in two** (*the owner's decision*): in its widened form, air between the probes, all four alike; **10/11 evening one down** (H21 added above it); **10/11 widened, not moved** (*the owner* agreeing): the zone between the front probe and the converter added — the joint, the flex, the plugged boss — which gives the rear probe's lean idle in full but not 032 or the dips (H2); **9/11 late evening one down** (H11 above it); **9/11 evening one down** (the belt above it); **down 31/10 from fourth** (*agreed with the owner*): the manifold seen from close below, rusty but no soot marks and no holes, its joint to the head nothing visibly wrong from below (H2); the part under its heat shield unseen; S2, S11, S14's air; cannot pick a cylinder | the warm tailpipe test (`plan.md` 7), both zones |
| A9 | **H18** oil past the stem seals | **12/11 evening** (*agreed with the owner*): against as the common part's cause — it does not grow with the time into a stop; for one valve it is the swell's second reading (list B's matter, S1, *The swell's shape*); **12/11, the idle split in two** (*the owner's decision*): all four alike by its own entry; **10/11 evening one down** (H21 added above it); **9/11 late evening one down** (H11 above it); added 26/10: worse after idling, calm after a working drive; all four alike; **no blue smoke ever**, plugs dry | the oil level on the fresh oil (`plan.md` 6i) |

**Done:**

| rank | hypothesis | why here | what settles it |
|---|---|---|---|
| — | **H12** driveline play | — | done: the clutch minutes cleared it |

**Re-read 12/11 night, off idle — agreed with the owner the same
night** (*Naming the cylinder*, *Off idle*; `tools/drivescan.py`).
Cylinder 3's deficit is the idle's and the light pedal's: a fifth to a
quarter of a stroke there, 9 % as soon as the engine pulls at idle
speed, 1–3 % at full load. **It follows the size of the charge, not
the time a stroke takes**, and it is an amount, not a share. So in
list B: **H13 and H1 stay first**, the only two that give the swell,
with H1's seat read as one that dilutes at vacuum (a seat that loses
compression would cost its share at full load too); **H3 stays third,
stronger** — and with the owner's reading of two causes at once, 032's
negative idle cell no longer counts against it (H3); **H4 goes above
H20**, its injector branch being the one cause that gives a fixed
amount by itself; **H7's injector stays last**, a share being what it
would give. None of them explains the swell better than before.
**6m, injector 3's circuit, is brought ahead of item 9's garage
session** (`plan.md`). List A is not touched: nothing here reads the
common part.

**Re-read 12/11 evening, the swell's shape and the common part —
agreed with the owner the same evening** (*the owner's questions*; S1,
*The swell's shape, and what the common part follows*). **What the reading says for list B**: the swell is not
3's air, fuel or spark, so **H3, H4 and H7's injector explain at most
3's floor**; H13 with H1 fits most of it as a seat that fouls and
burns clean; H18 enters B for one valve; H20 fits the mixture and not
the sawtooth. **For list A**: the common part has been the same within
5 % at every warm idle since 24/9 and answers only to the charge — a
load, the gas, temperature — so it is **H0's or a fixed fault's on all
four** (the belt), and the entries that vary by the day or the
drive have nothing in it to explain: **H16**, **H7's rail**,
**H21** and **H11**, **H18**. **So the belt and H0 go to the head of
A and H16 below them, third** (*agreed with the owner*; he had kept
H16 first until the new N80 earlier that day); the new valve is the
test either way: the common part by capture before and after it. The
three tests of S1's section agreed with it (`plan.md` 6p, 8o, item 9).

**Re-read 12/11, the third research — agreed with the owner the same
day** (S1, *Every stroke named*; S3, *What 014 counts, by cylinder*;
`tools/cylscan.py`). The two lists stand, but what each one holds is
not what the split assumed:
- **List B is the misfire and the swell, and its cylinder is 3 only.**
  80 % of what 014 counts since 21/10, the 10–20 % deficit at every
  warm idle, and the minutes when the grade doubles are all 3's.
  "3 (or 4)" in its heading, and "4's deficit" in the rows of H3, H4
  and H7, were the crank wheel's alternation: **H3 is runner 3's lower
  gasket, H4 the loom at 3, H7 injector 3.**
- **List A is the small unevenness on all four** — about 3.5 rpm rms a
  stroke, 3 a fifth above — and nothing 014 counts. It is most of
  `IdleHealth`'s floor and none of S3.
- **The order**: B before A, since S3 and the grade's swings are
  B's; inside B: **H13 and H1 on 3** first as before, H3's runner 3,
  H20, H4, **H7's injector 3 last** (*placed third earlier that day with an
  exchange of injectors 3 and 2 as its test; put last and the exchange
  withdrawn the same day, the owner's argument: 3 was weak on the old
  injectors too* — H7). Inside A as it was (*re-ordered that evening,
  above*), **H16 first until the captured stop
  on the canister is read by cylinder** (H16, above). **Read 12/11
  (`49`): neither part lower; H16 kept first by the owner (*third since
  that evening*) until the new
  N80** (above).
- **What would be read first**, in this order of cost: the captured
  warm stop already planned (which list the canister moved; *read 12/11,
  neither*); item 9's stethoscope above 3 and its warm leak-down with 3
  twice.

**Re-read 12/11, H16 from sixth to third** (*the owner's decision*,
the place proposed by Claude; H16, *12/11 night*): the stops near home
on 11/11 and 12/11, the two calmest warm stops on record outside the
provider's gas, both on the canister and sharing nothing else; H3, H4
and H7 one down each. Its limits stand: two stops, one place, and no
cylinder named.

**The re-reads before 12/11** (14/10–11/11) are in git (`git show
296a5d7:docs/engine-health/open.md`, this section). **Those that moved
H1, H3, H4, H7 and H15 between cylinders 3 and 4, or between one
cylinder and all four, rested on the dip shares withdrawn 12/11**
(*Naming the cylinder*, *What the dip shares said, and what stands*):
24/10's demotions for "the dips no longer keep to 3 and 4", 25/10
night's "one injector does not fit dips on all four alike", 4/11's
"one cylinder named again", 5/11's "3 and 4 give less alike" and 9/11's
"what acts on 4 alone". **What stands from them**, on grounds of its
own:
- **H14 and H19 out of the idle, 3/11**: the tuner's files show the
  remap touched only the corner of highest load, neither the idle nor
  the MAF's curve (`refuted.md` C22, C23).
- **H15 refuted 4/11** (`refuted.md` C24): re-read 12/11, 3 was as weak
  on the NGK leads as on the VW ones.
- **H7's rail half down, 25/10 night**: the regulator answers its
  reference (`refuted.md` C20), and a high base pressure does not fit
  032's positive part load; **31/10** S7 closed as the fuel (D2).
- **H8 down, 27/10**: 055's two fields sum to the same correction at
  every warm idle, so neither a reset nor the A/C idles the engine on
  more air; S20 and the idle air path keep it.
- **H2 down, 31/10**: the visible manifold shows none of the soot a
  leak leaves; **widened 10/11** to the zone between the probes.
- **H1**: the hot phone recording of 26/10 found no lifter; the port
  photos of 20/10 show crust round the inlet seat's edge on 3 and 4, a
  lump on 3 (*the owner's reading*, 7/11); **up 11/11** for 3's exhaust
  seat and the rough start after a hot drive.
- **H16**: down 6/11 night (out of the car the valve hardly passed air
  unpowered; no rhythm of its pulses in the dips), up 11/11 evening
  (the canister found bypassed), up 12/11 (the two calm nights).
- **The timing belt up, 9/11 late evening**: the gas idle names the
  dips a burn at the dilution edge, which the cam's timing against the
  crank sets.
- **H11 up 9/11 late evening, down 10/11 evening** (its marks failed on
  the relearn drive); **H21 added 10/11 evening**; **H20 added 4/11**;
  **H18 added 26/10**; **the column S1s added 11/11**.

**More than one at once** (*the owner's point*, 12/10): each repair may help
only in part; a partial improvement is read as a share, not a miss.

### How the vacuum gauge is read

*General*, the classic readings; read the needle against itself. Read on
14–15/10 (H3): **steady at idle, a little higher at 2500** — no valve fault or
large leak the gauge can see.

| the needle | reading |
|---|---|
| steady at idle, rises a little at 2500 | no valve fault, no large leak |
| an occasional sharp flick at idle, gone at 2500 | the misfires themselves; names nothing |
| a regular flick every cycle | one valve that never seals |
| low and steady at idle, normal at 2500 | air in behind the throttle (H3) |
| low at idle and at 2500 alike | a late cam, or an exhaust restriction |
| a fast flutter, worse at 2500 | weak valve springs or worn guides |
| slow wandering at idle | mixture or idle control hunting (H8, H7) |

---

## The plan

**The order of work is `plan.md`**: the idle first, a repair at a
time, readings only where they decide the next step, as little idling as
possible. The tests above are reference, not a schedule.

**A higher idle was tried, 12/10, and does not help**: raised to 830 rpm
specified (VW's procedure, login 01283), 014 kept counting and `IdleHealth`
rose slightly; put back the same day (`refuted.md` D9).
