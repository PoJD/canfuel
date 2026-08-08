# Fixtures — logy z USBtinu

Reálné záznamy z hnacího CANu Beetlu. **Needitovat.** Testy v `tools/` se na
ně odkazují přesnými čísly, takže jakákoliv úprava se hned projeví.

## Přehled

| Soubor | Formát | Řádků | Co to je | CLT |
|---|---|---|---|---|
| `01_ign_only.txt` | slcan | 3 402 | zapalování bez motoru, čítač celý 0 | 100,5 °C |
| `02_idle_60s.txt` | slcan | 89 882 | zahřátý volnoběh 797 ot/min, 60 s | 94,5–99 °C |
| `03_drive.txt` | slcan | 18 018 | jízda na jedničku do 19,4 km/h | 99 °C |
| `05_rev3000.txt` | slcan | 1 522 | 2940 ot/min v neutrálu | 90 °C |
| `06_trip_reset.txt` | viewer | 99 103 | stání, trip reset, popojetí 125 m | 53–64 °C |
| `07_accel.txt` | viewer | 11 192 | svižný rozjezd na 24,8 km/h | 76 °C |
| `idle.txt` | slcan | 1 136 | krátký volnoběh, studenější | 68,25 °C |

## Dva formáty

**slcan** — syrový proud z USBtinu, bez časových značek:

```
t1a0800400100fefe001d
^ ^  ^^
| |  +- data, 2 hex znaky na bajt
| +---- DLC, jeden hex znak
+------ 11bit ID, tři hex znaky
```

**viewer** — export z USBtinVieweru, pět sloupců oddělených tabulátorem:

```
2078 <TAB> jar:file:/...receive.png <TAB> 320h <TAB> 8 <TAB> 05 00 86 00 00 00 00 00
ts (ms)    ikona řádku               ID+h    DLC    bajty po mezerách
```

Řádky s ikonou `info.png` jsou hlášky vieweru („Connected to USBtin",
„Disconnected") — mají prázdné ID i DLC a parser je přeskakuje.

`tools/canlog.py` pozná formát podle tabulátoru; slcan ho nikdy neobsahuje.

---

## ⚠ `02_idle_60s.txt` obsahuje záznam dvakrát

Obě poloviny souboru jsou **řádek po řádku shodné** — 44 941 + 44 941 řádků.
Není to teorie, je to ověřené testem `test_02_is_doubled`.

**Důsledek:** bez opravy vychází volnoběžný průtok dvojnásobný (620 místo
310 µl/s) a celý výpočet spotřeby by byl mimo o 100 %.

**Jak se to řeší:** soubor zůstává v repu tak, jak přišel z USBtinu — původní
naměřená data se nepřepisují. Opravuje se až při čtení:

```python
frames = canlog.parse_file(path, fix_doubled=True)
```

```
python tools/canlog.py --fix-doubled test/fixtures/02_idle_60s.txt
```

`tools/replay.py` to má zapnuté implicitně.

Po opravě vychází 18 652 µl za 60,1 s = **310,1 µl/s = 1,12 l/h**, což je
přesně hodnota ze zadání. To je zároveň nejsilnější nepřímý důkaz, že perioda
rámce 0x480 je opravdu 49,5 ms.

Žádný jiný fixture zdvojený není (`test_no_other_fixture_is_doubled`).

---

## Pojmenování

`02_idle_60s.txt` se původně jmenoval `02_idle_60sec_170ms.txt`
a `05_rev3000.txt` byl `rev3000.txt`. Přejmenováno podle zadání
(BOOTSTRAP sekce 5), obsah je nedotčený.

`idle.txt` v zadání očíslovaný nebyl a nechává se pod původním názvem.
Podle teploty kapaliny (68,25 °C) je chronologicky **první** ze session,
tedy před `05_rev3000` — číslo 04 by pořadí naznačovalo špatně.

---

## Duplicitní rámce

39–51 % řádků v každém logu je bezprostředním duplikátem předchozího rámce
se stejným ID i stejnými daty. Je to artefakt záznamu, ne sběrnice.

Na výpočet delty čítače to vliv nemá (delta je nula), ale **měřenou periodu
rámců to zdvojnásobuje** — proto se z těchto logů periody odvodit nedají.
Podrobně v `docs/can-decoding.md`.
