#!/usr/bin/env python3
"""What each cylinder gives, and how much it wobbles -- kept capture by
capture, so that a new capture is added without reading the old ones again.

`docs/engine-health/cylinders-share.csv` holds one row a capture; `add`
reads only the captures it is given and puts their rows in (replacing a row
of the same capture), `render` draws `cylinders-share.svg` from the file
alone. The figure sits in `idle-log.md` and, in Czech, on the owner's page
*Pořadí hypotéz volnoběhu* (`render --lang cs`).

Panel A, each cylinder's work per stroke against the mean of 1, 2 and 4, %
(`cylscan.deviation()` over `swellscan.py`'s 30 s windows, warm, the A/C
off, the median window): 1, 2 and 4 over every warm window; 3 apart on its
floor (`swellscan.is_floor`) and in its swell (`swellscan.is_swell`).
Against 1, 2 and 4 so that 3's swell does not drag the others.

Panel B, each stroke's step about its cylinder's own median, rpm rms, over
the same windows: weak strokes and two either side left out, the bus's own
noise (`BUS_NOISE_RPM`, the coast-down's with no fuel) taken out in
quadrature. The noise is assumed the same on every slot.

    python tools/cylshare.py add test/fixtures/55_x_z1.txt \\
        --event-en "20/11 new belt" --event-cs "20/11 nový řemen"
    python tools/cylshare.py render                  # the English figure
    python tools/cylshare.py render --lang cs --out PAGE.svg
"""

import argparse
import csv
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "docs", "engine-health", "cylinders-share.csv")
SVG = os.path.join(ROOT, "docs", "engine-health", "cylinders-share.svg")

BUS_NOISE_RPM = 1.8      # the coast-down with no fuel: 1.7-1.8 rpm rms (open.md S1)
MIN_WINDOWS = 3          # fewer warm windows than this and a value is left out
MIN_STROKES = 5          # a cylinder's strokes in a window before it counts
WEAK_NEIGHBOURS = 2      # strokes either side of a weak one left out of panel B

FIELDS = ["cap", "kind", "n_warm", "n_floor", "n_swell",
          "a1", "a3", "a3_floor", "a3_swell", "a4", "a2",
          "b1", "b3", "b4", "b2", "event_en", "event_cs"]
CYLS = ("1", "3", "4", "2")
COLOUR = {"1": "#5b7fa6", "3": "#c0503a", "4": "#d08a1a", "2": "#2e8b57"}


# --- reading a capture --------------------------------------------------------

def _rel(row, c):
    return row[f"d{c}"] - (row["d1"] + row["d2"] + row["d4"]) / 3.0


def _median(v):
    return statistics.median(v) if len(v) >= MIN_WINDOWS else None


def measure(path):
    """The row of one capture, without its events."""
    sys.path.insert(0, HERE)
    import cylscan
    import swellscan
    cap = swellscan.Capture(path)
    warm, dev = [], {c: [] for c in cylscan.FIRING_ORDER}
    for run, rows in swellscan.stops(cap):
        t = run.T[1]
        for row in rows:
            t0, t = t, t + swellscan.WINDOW_S
            if not swellscan.warm_off(row):
                continue
            warm.append(row)
            i0, i1 = run.span(t0, t0 + swellscan.WINDOW_S)
            idx = [i for i in range(max(i0, 1), i1)
                   if run.E[i] is not None and not run.cut[i]]
            out = set()
            for i in idx:
                if run.E[i] <= -cylscan.WEAK_RPM:
                    out.update(range(i - WEAK_NEIGHBOURS, i + WEAK_NEIGHBOURS + 1))
            per = {c: [] for c in cylscan.FIRING_ORDER}
            for i in idx:
                if i not in out:
                    per[run.cyl(i)].append(run.E[i])
            for c, v in per.items():
                if len(v) >= MIN_STROKES:
                    m = statistics.median(v)
                    dev[c].extend(x - m for x in v)
    floor = [r for r in warm if swellscan.is_floor(r)]
    swell = [r for r in warm if swellscan.is_swell(r)]
    rec = {"cap": cap.name, "kind": "capture", "n_warm": len(warm),
           "n_floor": len(floor), "n_swell": len(swell),
           "a3": _median([_rel(r, 3) for r in warm]),
           "a3_floor": _median([_rel(r, 3) for r in floor]),
           "a3_swell": _median([_rel(r, 3) for r in swell])}
    for c in (1, 4, 2):
        rec[f"a{c}"] = _median([_rel(r, c) for r in warm])
    for c, v in dev.items():
        if len(warm) >= MIN_WINDOWS and v:
            r = math.sqrt(sum(x * x for x in v) / len(v))
            rec[f"b{c}"] = math.sqrt(max(r * r - BUS_NOISE_RPM ** 2, 0.0))
        else:
            rec[f"b{c}"] = None
    return rec


# --- the data file ------------------------------------------------------------

def load(path=DATA):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def save(rows, path=DATA):
    rows = sorted(rows, key=lambda r: (r["kind"] != "capture", r["cap"]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: _fmt(r.get(k)) for k in FIELDS})


def _fmt(v):
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.2f}"
    return v


def upsert(rows, rec):
    """rows with rec in place of any row of the same capture and kind; the
    old row's events are kept unless rec brings its own."""
    out, old = [], None
    for r in rows:
        if r["cap"] == rec["cap"] and r["kind"] == rec["kind"]:
            old = r
        else:
            out.append(r)
    for k in ("event_en", "event_cs"):
        if not rec.get(k) and old:
            rec[k] = old.get(k, "")
    out.append(rec)
    return out


def _num(r, k):
    v = r.get(k, "")
    return float(v) if v not in ("", None) else None


# --- the figure ---------------------------------------------------------------

TEXT = {
    "en": {
        "title": "What each cylinder gives, and how much it wobbles",
        "cyl": "cylinder",
        "a": "A · each cylinder against the mean of 1, 2 and 4, % of a "
             "stroke's work (warm idle), capture by capture",
        "a_note": "1, 2 and 4 over every warm window; 3 solid on its floor, "
                  "dashed in its swell; the median window.",
        "b": "B · how much each stroke wobbles about the cylinder's own mean "
             "(rpm rms, the bus's noise out), capture by capture",
        "gas": "on the provider's gas (9/11)",
        "foot1": "Generated by tools/cylshare.py from cylinders-share.csv. "
                 "Before 3/11 cylinder 3 was seldom on its floor,",
        "foot2": "so only its swell shows there. What a healthy cylinder "
                 "gives is not known.",
    },
    "cs": {
        "title": "Co který válec dává a jak moc kolísá",
        "cyl": "válec",
        "a": "A · každý válec proti průměru 1, 2 a 4, % práce taktu "
             "(teplý volnoběh), nahrávka po nahrávce",
        "a_note": "1, 2 a 4 přes všechna teplá okna; trojka plně na dně, "
                  "čárkovaně ve vlně; medián oken.",
        "b": "B · jak moc každý takt kolísá kolem průměru svého válce "
             "(ot/min rms, bez šumu sběrnice), nahrávka po nahrávce",
        "gas": "s plynem z přístroje (9/11)",
        "foot1": "Vygenerováno tools/cylshare.py z cylinders-share.csv. "
                 "Před 3/11 byla trojka na dně zřídka,",
        "foot2": "proto je tam jen vlna. Kolik dává zdravý válec, nevíme.",
    },
}

A_TOP, A_BOT, A_MAX, A_MIN = 92.0, 268.0, 10.0, -35.0
B_TOP, B_BOT, B_MAX, B_MIN = 454.6, 585.0, 4.0, 0.0
X0, X1 = 75.0, 645.0
GAS_X = 700.0


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(rows, lang="en"):
    t = TEXT[lang]
    caps = [r for r in rows if r["kind"] == "capture"]
    gas = next((r for r in rows if r["kind"] == "gas"), None)
    n = len(caps)
    step = (X1 - X0) / max(n - 1, 1)
    X = [X0 + i * step for i in range(n)]

    def ya(v):
        v = max(A_MIN, min(A_MAX, v))
        return A_TOP + (A_MAX - v) / (A_MAX - A_MIN) * (A_BOT - A_TOP)

    def yb(v):
        v = max(B_MIN, min(B_MAX, v))
        return B_BOT - (v - B_MIN) / (B_MAX - B_MIN) * (B_BOT - B_TOP)

    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 651" '
         'width="100%" style="max-width:780px" font-family="Helvetica,Arial,'
         f'sans-serif" role="img" aria-label="{_esc(t["title"])}">',
         '<rect width="780" height="651" fill="#fcfcfb"/>',
         f'<text x="20" y="28" font-size="18" font-weight="bold" fill="#111">'
         f'{_esc(t["title"])}</text>']
    for k, c in enumerate(CYLS):
        x = 20 + 90 * k
        o.append(f'<rect x="{x}" y="40" width="14" height="4" fill="{COLOUR[c]}"/>'
                 f'<text x="{x + 18}" y="46" font-size="12" fill="#222">'
                 f'{t["cyl"]} {c}</text>')

    def poly(vals, colour, yf, dash=""):
        seg = []
        segs = []
        for x, v in zip(X, vals):
            if v is None:
                if seg:
                    segs.append(seg)
                seg = []
            else:
                seg.append((x, yf(v)))
        if seg:
            segs.append(seg)
        for s in segs:
            if len(s) > 1:
                pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in s)
                o.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" '
                         f'stroke-width="2"{dash}/>')
            else:
                o.append(f'<circle cx="{s[0][0]:.1f}" cy="{s[0][1]:.1f}" r="2.5" '
                         f'fill="{colour}"/>')

    # panel A
    o.append(f'<text x="20" y="78" font-size="12.5" font-weight="bold" '
             f'fill="#111">{_esc(t["a"])}</text>')
    for v in (10, 0, -10, -20, -30):
        y = ya(v)
        o.append(f'<line x1="60" x2="740" y1="{y:.1f}" y2="{y:.1f}" '
                 f'stroke="{"#999" if v == 0 else "#e3e3e3"}"/><text x="54" '
                 f'y="{y + 4:.1f}" font-size="10" fill="#666" text-anchor="end">'
                 f'{"+" if v > 0 else ""}{v}</text>')
    for x, r in zip(X, caps):
        if r.get(f"event_{lang}"):
            o.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{A_TOP:.0f}" '
                     f'y2="{A_BOT:.0f}" stroke="#eee"/>')
    for c in ("1", "4", "2"):
        poly([_num(r, f"a{c}") for r in caps], COLOUR[c], ya)
    poly([_num(r, "a3_floor") for r in caps], COLOUR["3"], ya)
    poly([_num(r, "a3_swell") for r in caps], COLOUR["3"], ya,
         ' stroke-dasharray="5,3"')
    if gas:
        for c in CYLS:
            v = _num(gas, f"a{c}")
            if v is not None:
                o.append(f'<circle cx="{GAS_X:.0f}" cy="{ya(v):.1f}" r="4" '
                         f'fill="{COLOUR[c]}"/>')
        o.append(f'<text x="718" y="{ya(A_MAX) + 10:.1f}" font-size="9.5" '
                 f'fill="#444" text-anchor="end">{_esc(t["gas"])}</text>')
    for x, r in zip(X, caps):
        o.append(f'<text x="{x:.1f}" y="281" font-size="9" fill="#666" '
                 f'text-anchor="middle">{_esc(r["cap"])}</text>')
        ev = r.get(f"event_{lang}")
        if ev:
            o.append(f'<text transform="translate({x - 2:.1f},290) rotate(40)" '
                     f'font-size="9" fill="#444">{_esc(ev)}</text>')
    o.append(f'<text x="20" y="372" font-size="10.5" fill="#555">'
             f'{_esc(t["a_note"])}</text>')

    # panel B
    o.append(f'<text x="20" y="418" font-size="12.5" font-weight="bold" '
             f'fill="#111">{_esc(t["b"])}</text>')
    for v in range(0, 5):
        y = yb(v)
        o.append(f'<line x1="60" x2="740" y1="{y:.1f}" y2="{y:.1f}" '
                 f'stroke="#e3e3e3"/><text x="54" y="{y + 4:.1f}" font-size="10" '
                 f'fill="#666" text-anchor="end">{v}</text>')
    for c in CYLS:
        poly([_num(r, f"b{c}") for r in caps], COLOUR[c], yb)
    if gas:
        for c in CYLS:
            v = _num(gas, f"b{c}")
            if v is not None:
                o.append(f'<circle cx="{GAS_X:.0f}" cy="{yb(v):.1f}" r="4" '
                         f'fill="{COLOUR[c]}"/>')
        o.append(f'<text x="718" y="{yb(B_MAX) + 10:.1f}" font-size="9.5" '
                 f'fill="#444" text-anchor="end">{_esc(t["gas"])}</text>')
    for x, r in zip(X, caps):
        o.append(f'<text x="{x:.1f}" y="598" font-size="9" fill="#666" '
                 f'text-anchor="middle">{_esc(r["cap"])}</text>')
    o.append(f'<text x="20" y="625" font-size="10.5" fill="#555">'
             f'{_esc(t["foot1"])}</text>')
    o.append(f'<text x="20" y="639" font-size="10.5" fill="#555">'
             f'{_esc(t["foot2"])}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


# --- the command line ---------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="read captures and put their rows in")
    a.add_argument("files", nargs="+")
    a.add_argument("--event-en", default="", help="the label under the axis")
    a.add_argument("--event-cs", default="", help="the same, in Czech")
    a.add_argument("--gas", action="store_true",
                   help="the reference on the provider's gas, drawn apart")
    a.add_argument("--data", default=DATA)
    r = sub.add_parser("render", help="draw the figure from the data file")
    r.add_argument("--lang", choices=sorted(TEXT), default="en")
    r.add_argument("--out", default=None)
    r.add_argument("--data", default=DATA)
    args = ap.parse_args(argv)
    if args.cmd == "add":
        rows = load(args.data)
        for path in args.files:
            rec = measure(path)
            if args.gas:
                rec["kind"] = "gas"
            rec["event_en"], rec["event_cs"] = args.event_en, args.event_cs
            rows = upsert(rows, rec)
            print(path, {k: _fmt(rec.get(k)) for k in FIELDS[1:15]})
        save(rows, args.data)
        return 0
    out = args.out or (SVG if args.lang == "en" else None)
    if out is None:
        ap.error("--out is needed for a language other than en")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(render(load(args.data), args.lang))
    return 0


if __name__ == "__main__":
    sys.exit(main())
