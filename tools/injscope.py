#!/usr/bin/env python3
"""Record an injector's control wire on the LHT00SU1 and read its pulses.

Built for `docs/engine-health/plan.md` 6r: injector 3 against injector 4, one
after the other on the analyser's single analog channel (1ACH, sigrok's A0),
through the breadboard divider of about 1:11.

**Why snippets, not one long capture.** sigrok-cli 0.7.2 / libsigrok 0.5.2
with this analyser on Windows stops after about 0.19 s whatever the sample
rate ("Device only sent N samples": 19 k at 100 kHz, 195 k at 1 MHz, 748 k at
4 MHz; logic alone 0.48 s), measured on the desk. At a warm idle each
injector fires once every two revolutions, about 150 ms, so one snippet holds
one or two pulses and forty snippets about fifty. Decision: a series of
snippets now rather than chasing a newer libsigrok in the night; the reader
does not care how a pulse reached it.

**The scale.** The chain (divider and A/D together) is calibrated as
    V_car = ratio * (A0 - offset)
`offset` is A0 with the divider's input on earth; `ratio` from a known
voltage on the input against a multimeter (`cal`). Desk, 26/11: offset
0.105 V, ratio 10.94 at 4.853 V in. The A/D is eight bits over +-10 V, a
step of 0.078 V, about 0.86 V at the car: timing is read well, levels coarsely.

    python tools/injscope.py cal                       # mean A0 of one snippet
    python tools/injscope.py cal --volts 12.61         # ratio from a known input
    python tools/injscope.py capture --out-dir D --label inj3 --count 40
    python tools/injscope.py read D/inj3_*.sr [--csv out.csv]

What `read` gives per pulse (contact 2, the ECU's side; *general* for the
shape: the wire sits at the supply while closed, is pulled to near earth for
the injection, and kicks above the supply when the output stage lets go, then
shows a small hump as the needle lands):
  width    the electrical pulse, falling edge to rising edge, ms
  on_v     the mean voltage across the output stage while it conducts
  spike    the peak after release, V
  spike_us the time the kick stays more than 3 V above the supply
  hump_ms  from release to the hump's top, the needle's closing, if seen
  hump_v   the hump's height above the settled supply
Standard library only, so it runs wherever Python does.
"""
import argparse
import datetime
import os
import statistics
import struct
import subprocess
import sys
import zipfile

SIGROK_CLI = r"C:\Program Files\sigrok\sigrok-cli\sigrok-cli.exe"
DESK_OFFSET = 0.105
DESK_RATIO = 10.94


def load_sr(path):
    """Return (samplerate_hz, [A0 volts]) from a sigrok session file."""
    with zipfile.ZipFile(path) as z:
        meta = z.read("metadata").decode()
        rate = None
        for line in meta.splitlines():
            if line.startswith("samplerate="):
                rate = parse_rate(line.split("=", 1)[1])
        names = [n for n in z.namelist() if n.startswith("analog-1-1-")]
        names.sort(key=lambda n: int(n.rsplit("-", 1)[1]))
        data = b"".join(z.read(n) for n in names)
    vals = list(struct.unpack("<%df" % (len(data) // 4), data))
    if rate is None:
        raise ValueError("%s: no samplerate in metadata" % path)
    return rate, vals


def parse_rate(text):
    text = text.strip().replace(" ", "")
    mult = {"Hz": 1, "kHz": 1e3, "MHz": 1e6, "GHz": 1e9}
    for unit in ("GHz", "MHz", "kHz", "Hz"):
        if text.endswith(unit):
            return float(text[: -len(unit)]) * mult[unit]
    for suffix, m in (("k", 1e3), ("M", 1e6), ("G", 1e9)):
        if text.endswith(suffix):
            return float(text[:-1]) * m
    return float(text)


def median3(v):
    """Kill single-sample glitches (seen on the desk, ~9 V, one in 10^5)."""
    out = list(v)
    for i in range(1, len(v) - 1):
        a, b, c = v[i - 1], v[i], v[i + 1]
        out[i] = sorted((a, b, c))[1]
    return out


def to_car(a0, ratio, offset):
    return [ratio * (x - offset) for x in a0]


def find_pulses(v, rate):
    """Pulses on a car-volt trace: list of dicts, one per complete pulse."""
    n = len(v)
    if n < 10:
        return []
    supply = statistics.median(v)
    if supply < 5:
        return []
    lo = supply * 0.5
    us = rate / 1e6
    pulses = []
    i = 1
    while i < n:
        if v[i - 1] >= lo > v[i]:
            start = i
            j = i
            while j < n and v[j] < lo:
                j += 1
            if j >= n:
                break
            end = j
            p = measure(v, rate, start, end, supply)
            if p is not None:
                pulses.append(p)
            i = end + int(200 * us)
            continue
        i += 1
    return pulses


def measure(v, rate, start, end, supply):
    ms = rate / 1e3
    pre = v[max(0, start - int(1 * ms)):start]
    if len(pre) < int(0.5 * ms):
        return None  # the pulse began too close to the snippet's start
    tail_n = int(4 * ms)
    if end + tail_n > len(v):
        return None  # the snippet ended before the needle landed
    vs = statistics.mean(pre)
    a = start + int(0.2 * ms)
    b = end - int(0.05 * ms)
    on_v = statistics.mean(v[a:b]) if b > a else statistics.mean(v[start:end])
    win = v[end:end + int(0.5 * ms)]
    k = max(range(len(win)), key=win.__getitem__)
    spike = win[k]
    hi = vs + 3.0
    j = end
    while j < len(v) and (v[j] > hi or j < end + k):
        j += 1
    spike_us = (j - end) / rate * 1e6
    settled = statistics.mean(v[end + int(3 * ms):end + tail_n])
    # the hump: smooth over 50 us, look from the spike's end to 2.5 ms
    w = max(1, int(0.05 * ms))
    seg = v[j:end + int(2.5 * ms)]
    hump_ms = hump_v = None
    if len(seg) > 2 * w:
        sm = [sum(seg[x:x + w]) / w for x in range(len(seg) - w)]
        # skip the spike's decay: start after the trace first dips to settled
        s0 = next((x for x, y in enumerate(sm) if y <= settled + 0.3), None)
        if s0 is not None and s0 < len(sm) - 1:
            m = max(range(s0, len(sm)), key=sm.__getitem__)
            if sm[m] - settled >= 0.4 and m < len(sm) - 1:
                hump_ms = (j - end + m + w / 2) / rate * 1e3
                hump_v = sm[m] - settled
    return {
        "width_ms": (end - start) / rate * 1e3,
        "supply_v": vs,
        "on_v": on_v,
        "spike_v": spike,
        "spike_us": spike_us,
        "hump_ms": hump_ms,
        "hump_v": hump_v,
    }


def summary(rows, key):
    xs = [r[key] for r in rows if r[key] is not None]
    if not xs:
        return "%-9s   -" % key
    xs.sort()
    q = lambda f: xs[min(len(xs) - 1, int(f * (len(xs) - 1) + 0.5))]
    return "%-9s median %8.3f  IQR %8.3f..%-8.3f n=%d" % (
        key, statistics.median(xs), q(0.25), q(0.75), len(xs))


def cmd_read(args):
    rows = []
    for path in args.files:
        rate, a0 = load_sr(path)
        v = median3(to_car(a0, args.ratio, args.offset))
        for p in find_pulses(v, rate):
            p["file"] = os.path.basename(path)
            rows.append(p)
    if not rows:
        print("no complete pulse found")
        return 1
    if args.verbose:
        for r in rows:
            print("%-28s w %6.3f ms  sup %5.2f  on %5.2f  spike %5.1f V %5.0f us"
                  "  hump %s" % (r["file"], r["width_ms"], r["supply_v"],
                                 r["on_v"], r["spike_v"], r["spike_us"],
                                 "-" if r["hump_ms"] is None else
                                 "%.3f ms %.2f V" % (r["hump_ms"], r["hump_v"])))
    print("%d pulses from %d files" % (len(rows), len(args.files)))
    for key in ("width_ms", "supply_v", "on_v", "spike_v", "spike_us",
                "hump_ms", "hump_v"):
        print(summary(rows, key))
    if args.csv:
        keys = ["file", "width_ms", "supply_v", "on_v", "spike_v", "spike_us",
                "hump_ms", "hump_v"]
        with open(args.csv, "w") as f:
            f.write(",".join(keys) + "\n")
            for r in rows:
                f.write(",".join("" if r[k] is None else str(r[k])
                                 for k in keys) + "\n")
    return 0


def snippet(out, rate):
    r = subprocess.run([args_cli(), "--driver", "fx2lafw", "--channels", "A0",
                        "--config", "samplerate=%s" % rate,
                        "--samples", "10000000", "-o", out],
                       capture_output=True, text=True)
    return r.stderr.strip()


_CLI = [SIGROK_CLI]


def args_cli():
    return _CLI[0]


def cmd_capture(args):
    os.makedirs(args.out_dir, exist_ok=True)
    log = os.path.join(args.out_dir, "%s.log" % args.label)
    with open(log, "a") as lf:
        for k in range(1, args.count + 1):
            out = os.path.join(args.out_dir, "%s_%03d.sr" % (args.label, k))
            t = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
            msg = snippet(out, args.rate)
            lf.write("%s %s %s\n" % (t, os.path.basename(out), msg))
            print("%s %s %s" % (t, os.path.basename(out), msg), flush=True)
    return 0


def cmd_cal(args):
    out = os.path.join(args.out_dir, "cal.sr")
    os.makedirs(args.out_dir, exist_ok=True)
    snippet(out, "1M")
    _, a0 = load_sr(out)
    a0 = median3(a0)
    m = statistics.mean(a0)
    print("A0 mean %.4f V over %d samples" % (m, len(a0)))
    if args.volts is not None:
        if args.volts == 0:
            print("offset = %.4f V" % m)
        else:
            print("ratio = %.3f  (at offset %.4f)" % (
                args.volts / (m - args.offset), args.offset))
    else:
        print("V_car = %.2f V at ratio %.3f, offset %.4f" % (
            args.ratio * (m - args.offset), args.ratio, args.offset))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cli", default=SIGROK_CLI, help="sigrok-cli executable")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("read", "cal"):
        p = sub.add_parser(name)
        p.add_argument("--ratio", type=float, default=DESK_RATIO)
        p.add_argument("--offset", type=float, default=DESK_OFFSET)
    r = sub.choices["read"]
    r.add_argument("files", nargs="+")
    r.add_argument("--csv")
    r.add_argument("-v", "--verbose", action="store_true")
    c = sub.choices["cal"]
    c.add_argument("--volts", type=float, help="the multimeter's reading at the input")
    c.add_argument("--out-dir", default=".")
    p = sub.add_parser("capture")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--count", type=int, default=40)
    p.add_argument("--rate", default="2M")
    args = ap.parse_args(argv)
    _CLI[0] = args.cli
    return {"read": cmd_read, "capture": cmd_capture, "cal": cmd_cal}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
