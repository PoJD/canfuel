# Handoff, 12/11/2026: the stroke count through a drive, and 014's rises while driving

**Temporary.** Written at the owner's request so that a new session can pick
this up; that session folds what stands into `docs/engine-health/open.md`
(and `cylscan.py`, if kept), does the currency pass, and deletes this folder.
Nothing here has gone into `docs/` yet, and nothing in `docs/` rests on it.
The scripts are ad hoc, copied unchanged out of the session's scratchpad:
they hard-code `/home/user/canfuel` and write their pickles beside
themselves, so copy them into a scratchpad before running them.

## The owner's requests in that session (translated from Czech)

1. "Explain the last day's work by the Fable model. How did it find so many
   inconsistencies? How does the phase-shift calculation work that made
   naming the cylinders in the cycle from the bus exact even on a long
   idle? How was 014's link to the firings found when VCDS samples so
   slowly?"
2. "Describe the integral to me in more detail. It's been 20 years since I
   last worked one out."
3. "And that holds only for the idle, I'd guess, where the engine speed does
   not change so fast? I.e. under acceleration or engine braking it would
   fall apart?"
4. (Asked whether to test one count from one stop through the drive to the
   next.) "Yes."
5. "Try whether we can then also find which cylinders 014's misfires while
   driving were on, where that can be found from a nearby idle or a nearby
   stretch of lower engine speed."
6. "Write only these conclusions into a new temporary document and commit.
   Include my original prompt. I'll start a new session for it."

## 1. The stroke count holds through a drive below about 2,800 rpm

`drivecount.py`: for every two consecutive named standing idles in `31`,
`39`, `40`, `42`, `44`, `46`, `47`, `49`, `50` (`43` gave no pair), one
`cylscan.track()` count from the start of the first to the end of the
second; the strongest slot (cylinder 2) read at each end on that one count.
No frame gap over 0.06 s in any of them.

| highest engine speed of the drive between | drives | same slot at both ends | slipped |
|---|---|---|---|
| up to about 2,850 rpm | 38 | **38** | 0 |
| about 3,000 rpm and above | 28 | 12 | 16 (by 1 or 2 strokes) |

The edge is sharp: drives topping out at 2,856 and 3,012 rpm held, 3,088 did
not. 12 of 28 is barely above the quarter that chance (and two opposite
slips cancelling) gives. Moving off, gear changes, queues and the overrun
are no problem; speed is.

**Why** (reasoned, and borne out): 0x280 arrives at about 94 Hz, so at
about 2,820 rpm (94 × 30) there is one frame per stroke; above it strokes go
unseen between frames and the phase correction loses its reference.
`where.py`, the share of value changes whose rounding error exceeds 0.40 of
a stroke (uniform noise would give 20 %), over `39`–`50`:

| rpm | 500–1000 | 1000–2500 | 2500–3000 | 3000–3500 | 3500–6500 |
|---|---|---|---|---|---|
| \|error\| > 0.40 | 0.2 % | 2–3 % | 7 % | 13 % | 4–9 % |

**Consequence**: nothing read so far changes — `cylscan.py` names every
standing idle on its own and never carries the count across a drive.

## 2. Naming a stretch with no stop in it

`drive014.py` / `drive014b.py` cut every capture into stretches at
500–2,700 rpm with no frame gap over 0.1 s, one count each.

- Where a stretch holds two or more named idles, they agree in **35 of 35**.
- **The strongest slot of the driving part alone** (raw steps by slot, the
  idles ±2 s left out, at least 500 strokes a slot) gave the idle's
  cylinder 2 in **56 of 56** stretches — although its margin over the next
  slot was as little as 1 rpm in some. So a stretch can be named with no
  stop in it. Unexplained why it works this well while driving; worth
  understanding before it is relied on.

## 3. 014's rises while driving

The 014 logs were paired with their captures by engine speed (numpy brute
force, then 0.05 s steps; mean error about 20 rpm): 32 driving logs
matched; logs wholly at a standing idle cannot be paired this way (as
`vcds.md` already says) and were skipped. A rise between two samples with
recognition on and at most 2.5 s apart was put to the weakest stroke in
[previous sample − 0.30 s, the rise's sample − 0.12 s] (cylscan's lags). The
weakness measure is cruder than `cylscan.py`'s: each step against the
median of the same slot's steps in ±6 cycles, **no spread (`OWN_SHARE`) or
wheel correction**. Control: the same pick in the windows 5 s before and
after each rise.

**The control is not 25 % a cylinder: about 46 % falls on cylinder 3**,
because 3 is the most uneven cylinder and wins "weakest in a window" with no
misfire at all. Only the excess over the control says anything.

146 driving rises were named (64 by an idle in the stretch, 82 by the
driving part's strongest slot); 3 in unnamed stretches, 22 lost to high rpm
or gaps.

| | 1 | 3 | 4 | 2 |
|---|---|---|---|---|
| **≤ 1,200 rpm, from 21/10 (the VW leads)**, 33 rises | 3 % | **73 %** | 18 % | 6 % |
| control | 16 % | 46 % | 22 % | 15 % |
| **≤ 1,200 rpm, up to 18/10**, 52 rises | 2 % | **50 %** | **46 %** | 2 % |
| control | 12 % | 45 % | 26 % | 16 % |
| 1,200–2,700 rpm, from 21/10, 31 rises | 32 % | 39 % | 16 % | 13 % |
| control | 8 % | 34 % | 16 % | 41 % |
| 1,200–2,700 rpm, up to 18/10, 30 rises | 17 % | 13 % | 37 % | 33 % |
| control | 14 % | 38 % | 16 % | 32 % |

The weakest stroke at a rise is deeper than in the control: median −14.9
against −9.6 rpm.

**Conclusions**

- **Below 1,200 rpm (moving off, crawling in a queue) 014's driving
  misfires are the idle's**: cylinder 3 since the VW leads, 3 and 4 about
  equally before them — the same as the standing idle on the NGK leads
  (`open.md` S3). 1 and 2 are next to never named, against 12–16 % by
  chance.
- **Above 1,200 rpm the rises differ from the control, but the name smears
  onto neighbouring slots** — since 21/10 onto 1, which fires just before 3.
  Most likely the spread of a stroke's loss into the adjacent slot, which
  is measured and corrected only at idle and will differ with speed and
  with a gear in (the car's mass damps the step). **This does not say
  cylinder 1 misfires while driving.** Naming above 1,200 rpm would need
  `OWN_SHARE` measured per speed band.
- **Worth checking in `cylscan.py --vcds`**: the standing-idle split in
  `open.md` S3 (*What 014 counts, by cylinder*, 80 % on 3 since the VW
  leads) is set against 25 % by chance, not against a control window. 3
  most likely still leads, but by less than that figure suggests. This
  session's own standing-idle check (60 % on 3, 22 % on 1 from 21/10, crude
  measure) does not match `cylscan.py`'s figures and is no substitute.

## Files

- `drivecount.py` — section 1, the table.
- `where.py` — section 1, rounding error by speed band.
- `drive014.py` — log-to-capture pairing (writes `caps.pkl`, `pairs.pkl`).
- `drive014b.py` — sections 2 and 3 (reads them, writes `res.pkl`).
