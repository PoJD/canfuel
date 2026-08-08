# canfuel — firmware převodníku

Převodník spotřeby pro VW New Beetle, motor AQY (2,0 l / 85 kW, PQ34).
Čte hnací CAN (500 kbps), počítá spotřebu, dojezd, moment a výkon, a posílá
je zpět na sběrnici ve vlastních rámcích 0x600–0x602. Displej CANchecked
MFD15 Gen2 je zobrazuje podle vlastního TRI souboru (repo `mfd15`).

MCU: PIC18F25K80, 16 MHz, XC8. Deska je v repu `kicad`.

---

## Nepřekročitelné pravidlo: čisté C v jádru

`src/decode.c`, `src/compute.c` a `src/txframes.c` **nesmí obsahovat jediný
`#include <xc.h>`.** Berou pole bajtů a čas v milisekundách, vracejí čísla.

Celé jádro musí jít přeložit gcc a otestovat na reálných logách bez jediného
kusu hardwaru. To je to, co má zabránit deseti iteracím desky — než se cokoliv
spájí, prožene se log a spotřeba se zkontroluje očima.

Hardware patří výhradně do `hal_can.c` a `hal_sys.c`.

---

## Než sáhneš na výpočty, přečti si `docs/can-decoding.md`

Jsou tam čtyři pasti, na kterých se dá tiše ztroskotat. Stručně:

1. **Brána platnosti rychlosti není rovnost.** `b1 == 0x40` je špatně,
   správně je `(b1 & 0x40) && !(b1 & 0x03)`. Rovnost zahodí dvě třetiny
   vzorků a zkazí FuelAvg i Range.
2. **Čítač spotřeby se po vypnutí zapalování resetuje na nulu.** Bez detekce
   restartu (`čítač == 0 || otáčky == 0` → reinicializovat `prev`) dá delta
   nesmyslný skok. Delta je vždy `(nový − starý) mod 32768`.
3. **Bit 15 čítače není konstantní.** Je nula od zapalování do prvního
   přetečení, pak trvale jedna. Maska 0x7FFF ho stejně zahodí.
4. **FuelAvg pod 100 m dráhy vracet nulu.** Jinak dělíš skoro nulou.

---

## Struktura

```
src/
  main.c        scheduler a glue — jediné místo, kde se to potkává
  decode.c/.h   parsování rámců        ČISTÉ C
  compute.c/.h  matematika             ČISTÉ C
  txframes.c/.h skládání rámců         ČISTÉ C
  persist.c/.h  EEPROM kruhový buffer
  hal_can.c/.h  ECAN + MCP2562
  hal_sys.c/.h  timery, ADC/FVR, LED, jumper
  config.h      všechny konstanty a přepínače
test/           testy jádra, běží na hostu přes gcc
tools/          canlog.py, replay.py — Python, běží všude
```

Konstanty patří do `config.h`, ne do kódu. Zejména `FUELNOW_LH_BELOW_KMH`,
`FUELNOW_CLAMP`, práh tankování a periody rámců.

Knihovna `piclib` (github.com/PoJD/piclib) se přidá jako submodul — má
`can_setupBaudRate(baudRate, cpuSpeed)`, max 500 kbps při 16 TQ.

---

## Nástroje

```
python tools/canlog.py test/fixtures/03_drive.txt          # souhrn per ID
python tools/canlog.py --dump --id 0x480 FILE              # výpis rámců
python tools/replay.py --every 100 test/fixtures/07_accel.txt
python -m unittest discover -s tools -p "test_*.py"        # 77 testů
```

`tools/replay.py` je referenční implementace dekodéru v Pythonu, psaná podle
stejné tabulky jako budoucí `decode.c` a `compute.c`. Až bude hotové ceckové
jádro, přidá se přepínač `--host-build` a rozdíl obou výstupů bude tvrdý test.
`tools/test_replay.py` je zároveň šablona pro `test/test_compute.c` — stejné
fixtures, stejná očekávaná čísla.

---

## Fixtures

Reálné logy z auta, **needitovat**. Testy se na ně odkazují přesnými čísly.

⚠ `02_idle_60s.txt` obsahuje záznam **dvakrát** — obě poloviny jsou shodné.
Opravuje se až při čtení (`parse_file(..., fix_doubled=True)`), soubor
zůstává původní. Bez toho vychází volnoběžný průtok dvojnásobný.

Podrobnosti a tabulka všech logů: `test/fixtures/README.md`.

---

## Ověřené hodnoty, na které musí jádro sednout

| Log | Čítač celkem | Doba | Průtok |
|---|---|---|---|
| `01_ign_only` | 0 µl | — | 0 |
| `02_idle_60s` | 18 652 µl | 60,1 s | 310 µl/s = 1,12 l/h |
| `05_rev3000` | 1 940 µl | 1,93 s | 1005 µl/s |
| `06_trip_reset` | 51 992 µl | 135,0 s | 385 µl/s, dráha 125 m |
| `07_accel` | 9 752 µl | 15,9 s | 613 µl/s |

---

## Prostředí

Na tomhle stroji **není nainstalovaný git, gcc, make ani XC8.** Python 3.11
je. Testy v `tools/` proto běží, testy v `test/` (gcc) zatím ne — než se
toolchain doplní, je referenční implementace v Pythonu jediná spustitelná
kontrola výpočtů.

---

## Kam dál

Fáze 1 je jádro v C s host testy. Pořadí kroků a zdůvodnění je
v `docs/implementacni-plan.md`, §3. Breadboard fáze se přeskakuje —
Micro-Fit má rozteč 3,0 mm a na breadboard nesedí.
