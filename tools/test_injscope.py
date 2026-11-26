"""Tests for injscope.py on a synthetic injector trace written as a .sr file.

The trace is built in car volts, then put through the desk chain the reader
inverts: divided by the ratio, offset added, quantised to the A/D's 0.078 V
step, with one single-sample glitch the median filter must remove.
"""
import math
import os
import random
import struct
import tempfile
import unittest
import zipfile

import injscope

RATE = 2_000_000
STEP = 0.078


def car_trace(pulses, n, supply=14.0, width_ms=3.0, hump_ms=1.0, hump_v=1.5):
    v = [supply] * n
    for t0 in pulses:
        s = int(t0 * RATE)
        e = s + int(width_ms * 1e-3 * RATE)
        for i in range(s, e):
            v[i] = 0.6
        for i in range(e, min(n, e + int(1.5e-3 * RATE))):
            dt = (i - e) / RATE
            kick = 45.0 * math.exp(-dt / 40e-6)
            hump = hump_v * math.exp(-((dt - hump_ms * 1e-3) / 0.15e-3) ** 2)
            v[i] = supply + kick + hump
    return v


def write_sr(path, car, ratio=10.94, offset=0.105, glitch_at=None):
    rnd = random.Random(1)
    a0 = [round((x / ratio + offset + rnd.gauss(0, 0.02)) / STEP) * STEP
          for x in car]
    if glitch_at is not None:
        a0[glitch_at] = 9.0
    data = struct.pack("<%df" % len(a0), *a0)
    meta = ("[global]\nsigrok version=0.5.2\n\n[device 1]\n"
            "samplerate=2 MHz\ntotal analog=1\nanalog1=A0\nunitsize=1\n")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("version", "1")
        z.writestr("metadata", meta)
        chunk = 5120 * 4
        for k in range(0, len(data), chunk):
            z.writestr("analog-1-1-%d" % (k // chunk + 1), data[k:k + chunk])


class InjscopeTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "inj3_001.sr")
        n = int(0.19 * RATE)
        write_sr(self.path, car_trace([0.010, 0.160], n), glitch_at=5000)

    def tearDown(self):
        for f in os.listdir(self.dir):
            os.remove(os.path.join(self.dir, f))
        os.rmdir(self.dir)

    def pulses(self):
        rate, a0 = injscope.load_sr(self.path)
        self.assertEqual(rate, RATE)
        v = injscope.median3(injscope.to_car(a0, 10.94, 0.105))
        return injscope.find_pulses(v, rate)

    def test_both_pulses_found_and_the_glitch_is_not_one(self):
        self.assertEqual(len(self.pulses()), 2)

    def test_width_supply_and_on_voltage(self):
        for p in self.pulses():
            self.assertAlmostEqual(p["width_ms"], 3.0, delta=0.01)
            self.assertAlmostEqual(p["supply_v"], 14.0, delta=0.3)
            self.assertAlmostEqual(p["on_v"], 0.6, delta=0.3)

    def test_spike(self):
        for p in self.pulses():
            self.assertAlmostEqual(p["spike_v"], 59.0, delta=1.5)
            # 45 V * exp(-t/40 us) falls under 3 V after 40*ln(15) = 108 us
            self.assertAlmostEqual(p["spike_us"], 108, delta=15)

    def test_hump(self):
        for p in self.pulses():
            self.assertIsNotNone(p["hump_ms"])
            self.assertAlmostEqual(p["hump_ms"], 1.0, delta=0.05)
            self.assertAlmostEqual(p["hump_v"], 1.5, delta=0.4)

    def test_a_pulse_cut_by_the_snippet_end_is_dropped(self):
        n = int(0.19 * RATE)
        write_sr(self.path, car_trace([0.010, 0.187], n))
        self.assertEqual(len(self.pulses()), 1)

    def test_read_command_and_csv(self):
        out = os.path.join(self.dir, "o.csv")
        self.assertEqual(injscope.main(["read", self.path, "--csv", out]), 0)
        with open(out) as f:
            self.assertEqual(len(f.read().splitlines()), 3)

    def test_rate_parsing(self):
        self.assertEqual(injscope.parse_rate("1 MHz"), 1e6)
        self.assertEqual(injscope.parse_rate("500 kHz"), 5e5)
        self.assertEqual(injscope.parse_rate("2M"), 2e6)


if __name__ == "__main__":
    unittest.main()
