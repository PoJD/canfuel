#!/usr/bin/env python3
"""Prozene log dekoderem a vypise, co by prevodnik poslal na sbernici.

Ve fazi 0 je tohle referencni implementace v Pythonu. Je zamerne napsana
podle stejne tabulky jako budouci src/decode.c a src/compute.c, aby slo
porovnavat vysledek radek po radku -- az bude host build hotovy, prida se
sem prepinac --host-build a rozdil obou vystupu bude tvrdy test.

Do te doby slouzi ke dvema vecem: overit vzorce ocima na realnych datech
a mit cim zkontrolovat prvni verzi ceckoveho jadra.

Pouziti:
    python tools/replay.py test/fixtures/03_drive.txt
    python tools/replay.py --csv test/fixtures/07_accel.txt > out.csv
    python tools/replay.py --every 20 test/fixtures/06_trip_reset.txt
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from typing import Optional

from canlog import Frame, parse_file

# --- konstanty, ktere v C skonci v config.h -------------------------------

PERIOD_0X480_MS = 49.5      # perioda citace spotreby, kdyz log nema znacky
FUELNOW_LH_BELOW_KMH = 4.0  # pod timhle se posila l/h, nad tim l/100 km
FUELNOW_CLAMP = 999         # 99,9 na displeji
RANGE_DEFAULT_L100 = 9.0    # nez najedeme 5 km, dojezd pocitame s timhle
AVG_MIN_M = 100             # pod timhle je prumer deleni skoro nulou
COUNTER_MODULO = 32768

# Brana platnosti rychlosti v 0x1A0 bajt 1. Neni to rovnost, je to bitova
# maska -- podrobne zduvodneni v docs/can-decoding.md.
SPEED_GATE_REQUIRED = 0x40  # tenhle bit musi byt nastaveny
SPEED_GATE_FORBIDDEN = 0x03  # tyhle znamenaji inicializacni rampu po zapalovani


# --- dekodovani -----------------------------------------------------------

@dataclass
class Decoded:
    """Posledni znamy stav sbernice. Odpovida vystupu decode.c."""

    rpm: float = 0.0
    speed_kmh: float = 0.0
    speed_valid: bool = False
    clt_c: Optional[float] = None
    oil_c: Optional[float] = None
    tank_l: int = 0
    tank_reserve: bool = False
    torque_ind_nm: float = 0.0
    throttle: int = 0
    load: int = 0
    accel_g: float = 0.0
    fuel_counter: Optional[int] = None
    counter_wrapped: bool = False


def u16le(d: bytes, i: int) -> int:
    return d[i] | d[i + 1] << 8


def decode(frame: Frame, st: Decoded) -> None:
    """Zapise jeden ramec do stavu. Zadna matematika spotreby, jen extrakce."""
    d = frame.data
    cid = frame.can_id

    if cid == 0x280 and len(d) >= 8:
        st.rpm = u16le(d, 2) * 0.25
        st.throttle = d[5]
        st.load = d[6]
        st.torque_ind_nm = d[7] * 0.67

    elif cid == 0x1A0 and len(d) >= 4:
        # Bajt 1 je bitove pole, ne jedna hodnota. Bit 0x40 znamena "rychlost
        # plati", spodni dva bity jsou inicializacni rampa po zapnuti
        # zapalovani (0x43, 0x42) a musi se zahodit. Bity 0x08 a 0x10 na
        # platnost vliv nemaji -- v 07_accel je 0x48 dokonce vetsinovy stav.
        st.speed_valid = bool(d[1] & SPEED_GATE_REQUIRED) and not (d[1] & SPEED_GATE_FORBIDDEN)
        if st.speed_valid:
            st.speed_kmh = u16le(d, 2) * 0.005

    elif cid == 0x288 and len(d) >= 2:
        st.clt_c = None if d[1] == 0xFF else d[1] * 0.75 - 48.0

    elif cid == 0x420 and len(d) >= 4:
        st.oil_c = None if d[3] == 0xFF else d[3] * 0.75 - 48.0

    elif cid == 0x320 and len(d) >= 3:
        st.tank_l = d[2] & 0x7F
        st.tank_reserve = bool(d[2] & 0x80)

    elif cid == 0x5A0 and len(d) >= 1:
        st.accel_g = (d[0] - 127) / 100.0

    elif cid == 0x480 and len(d) >= 4:
        raw = u16le(d, 2)
        st.fuel_counter = raw & 0x7FFF
        st.counter_wrapped = bool(raw & 0x8000)


# --- vypocty --------------------------------------------------------------

@dataclass
class Compute:
    """Akumulatory. Odpovida compute.c."""

    prev_counter: Optional[int] = None
    total_ul: int = 0
    total_mm: int = 0
    last_ms: Optional[float] = None
    flow_ul_s: float = 0.0
    restarts: int = 0
    _flow_window: list = field(default_factory=list)

    def on_counter(self, st: Decoded, now_ms: float) -> None:
        """Nova hodnota citace. Vraci se pres self.total_ul.

        Past, kvuli ktere tenhle kod existuje: po vypnuti zapalovani se citac
        resetuje na nulu. Bez detekce restartu by delta dala skok o desitky
        tisic mikrolitru.
        """
        c = st.fuel_counter
        if c is None:
            return

        restart = c == 0 or st.rpm == 0
        if restart or self.prev_counter is None:
            if restart and self.prev_counter is not None:
                self.restarts += 1
            self.prev_counter = c
            self.last_ms = now_ms
            return

        delta_ul = (c - self.prev_counter) % COUNTER_MODULO
        self.prev_counter = c

        dt_s = None
        if self.last_ms is not None and now_ms > self.last_ms:
            dt_s = (now_ms - self.last_ms) / 1000.0
        self.last_ms = now_ms

        self.total_ul += delta_ul
        if dt_s:
            self._flow_window.append((delta_ul, dt_s))
            # klouzave okno ~1 s, jinak cislo na displeji tanci
            while sum(w[1] for w in self._flow_window) > 1.0 and len(self._flow_window) > 1:
                self._flow_window.pop(0)
            win_ul = sum(w[0] for w in self._flow_window)
            win_s = sum(w[1] for w in self._flow_window)
            self.flow_ul_s = win_ul / win_s if win_s else 0.0

    def on_distance(self, st: Decoded, dt_s: float) -> None:
        if st.speed_valid and st.speed_kmh > 0 and dt_s > 0:
            self.total_mm += int(st.speed_kmh / 3.6 * dt_s * 1000.0)

    # -- odvozene veliciny ------------------------------------------------

    @property
    def flow_lh(self) -> float:
        return self.flow_ul_s * 3.6 / 1000.0

    @property
    def avg_l100(self) -> float:
        """Podil akumulatoru, ne prumer okamzitych hodnot -- stani na semaforu
        tak prumer neznici.

        Pod AVG_MIN_M se vraci nula. Bez teto pojistky vychazi po nastartovani
        deleni skoro nulovou drahou -- na 06_trip_reset to davalo 21 395
        l/100 km, nez auto popojelo. Na displeji by to byla useknuta 99,9.
        """
        if self.total_mm < AVG_MIN_M * 1000:
            return 0.0
        return (self.total_ul / 1000.0) / (self.total_mm / 1000.0) * 100.0

    def fuel_now(self, st: Decoded) -> tuple[float, str]:
        """Dvoji jednotka. Jediny prah, zadna hystereze."""
        if not st.speed_valid or st.speed_kmh < FUELNOW_LH_BELOW_KMH:
            return min(self.flow_lh, FUELNOW_CLAMP / 10.0), "l/h"
        l100 = self.flow_lh / st.speed_kmh * 100.0
        return min(l100, FUELNOW_CLAMP / 10.0), "l/100km"

    def range_km(self, st: Decoded) -> float:
        driven_km = self.total_mm / 1_000_000.0
        basis = self.avg_l100 if driven_km >= 5.0 and self.avg_l100 > 0 else RANGE_DEFAULT_L100
        return st.tank_l / basis * 100.0


# --- prehravani -----------------------------------------------------------

def replay(path: str, *, csv: bool = False, every: int = 1, fix_doubled: bool = True):
    frames = parse_file(path, fix_doubled=fix_doubled)
    st = Decoded()
    cp = Compute()

    synthetic = all(f.ts_ms is None for f in frames)
    n480 = 0
    rows = 0

    header = ["t_s", "rpm", "km/h", "clt", "ul_s", "l/h", "FuelNow", "jedn",
              "FuelAvg", "tank_l", "range_km", "total_ul", "total_m"]
    if csv:
        print(",".join(header))
    else:
        print(f"# {path}")
        print(f"# cas {'odhadnuty z periody 0x480' if synthetic else 'z casovych znacek logu'}")
        print("  " + "".join(h.rjust(10) for h in header))

    prev_ms = None
    for f in frames:
        if f.can_id == 0x480:
            now_ms = n480 * PERIOD_0X480_MS if synthetic else float(f.ts_ms)
            n480 += 1
        else:
            now_ms = None

        decode(f, st)

        if now_ms is None:
            continue

        if prev_ms is not None:
            cp.on_distance(st, (now_ms - prev_ms) / 1000.0)
        prev_ms = now_ms

        cp.on_counter(st, now_ms)

        rows += 1
        if rows % every:
            continue

        fn, unit = cp.fuel_now(st)
        vals = [
            f"{now_ms / 1000:.2f}", f"{st.rpm:.0f}", f"{st.speed_kmh:.1f}",
            "-" if st.clt_c is None else f"{st.clt_c:.1f}",
            f"{cp.flow_ul_s:.0f}", f"{cp.flow_lh:.2f}", f"{fn:.1f}", unit,
            f"{cp.avg_l100:.1f}", f"{st.tank_l}", f"{cp.range_km(st):.0f}",
            f"{cp.total_ul}", f"{cp.total_mm / 1000:.0f}",
        ]
        print(",".join(vals) if csv else "  " + "".join(v.rjust(10) for v in vals))

    if not csv:
        span_s = (n480 - 1) * (PERIOD_0X480_MS / 1000 if synthetic else 0)
        if not synthetic:
            stamped = [f.ts_ms for f in frames if f.can_id == 0x480]
            span_s = (stamped[-1] - stamped[0]) / 1000.0
        print(f"# celkem {cp.total_ul} ul za {span_s:.2f} s "
              f"-> {cp.total_ul / span_s:.0f} ul/s = {cp.total_ul / span_s * 3.6 / 1000:.2f} l/h")
        print(f"# ujeto {cp.total_mm / 1000:.0f} m, prumer {cp.avg_l100:.2f} l/100 km, "
              f"detekovano restartu: {cp.restarts}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Prehraje log referencnim dekoderem.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--csv", action="store_true")
    ap.add_argument("--every", type=int, default=1, help="vypsat jen kazdy N-ty radek")
    ap.add_argument("--no-fix-doubled", action="store_true",
                    help="nechat zdvojeny soubor tak, jak je (viz fixtures/README.md)")
    args = ap.parse_args(argv)

    for path in args.files:
        replay(path, csv=args.csv, every=max(1, args.every),
               fix_doubled=not args.no_fix_doubled)
    return 0


if __name__ == "__main__":
    sys.exit(main())
