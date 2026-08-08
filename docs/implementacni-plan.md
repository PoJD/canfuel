# Převodník spotřeby AQY → MFD15 — implementační plán

Stav k 2. 8. 2026, revize 2. Určeno k navázání na desktopu s Claude Code.
Pracovní název zařízení: **canfuel** (přejmenovat je triviální, jen v README a názvech repozitářů).

---

## 1. Struktura na GitHubu

Kopíruje tvůj dosavadní styl (`can` = firmware, `eagle` = desky), jen s KiCadem.
**Tři repozitáře**, ne monorepo — každý má jiný toolchain, jinou CI a jinou životnost.

### `kicad` — hardware (nástupce repa `eagle`)

Kontejner na všechny budoucí desky, stejně jako `eagle` dnes.

```
kicad/
├── README.md                    # index desek
├── lib/                         # sdílené symboly a pouzdra napříč projekty
│   ├── pojd.kicad_sym
│   └── pojd.pretty/
├── canfuel/
│   ├── canfuel.kicad_pro
│   ├── canfuel.kicad_sch
│   ├── canfuel.kicad_pcb
│   ├── canfuel.kicad_prl        # do .gitignore, je to lokální stav
│   ├── fab/                     # generované, commitovat kvůli dohledatelnosti
│   │   ├── gerbers/
│   │   ├── canfuel-bom.csv
│   │   └── canfuel-pos.csv
│   └── docs/
│       ├── schematic.pdf
│       └── mechanical.md        # rozměry, montáž do průduchu
└── .github/workflows/kicad.yml  # ERC + DRC + export gerberů přes kicad-cli
```

KiCad 8 má textové formáty, takže diffy jsou čitelné a `kicad-cli` umí v CI
spustit ERC i DRC bez GUI. To je hlavní důvod k přechodu z Eagle — chyba
v návrhu spadne v pull requestu, ne až na hotové desce.

### `canfuel` — firmware + dekódování

```
canfuel/
├── README.md
├── docs/
│   ├── can-decoding.md          # tabulka signálů AQY (ID, bajty, vzorce)
│   ├── frames.md                # 0x600/0x601/0x602 — přesný layout
│   └── calibration.md           # ztrátový moment, nádrž
├── src/
│   ├── main.c                   # jen scheduler a glue
│   ├── decode.c/.h              # parsování příchozích rámců — ČISTÉ, bez PIC
│   ├── compute.c/.h             # veškerá matematika — ČISTÉ, bez PIC
│   ├── txframes.c/.h            # skládání odchozích rámců — ČISTÉ, bez PIC
│   ├── reset_src.c/.h           # ⚠ zdroj trip resetu, jediné místo (viz §5)
│   ├── persist.c/.h             # EEPROM kruhový buffer
│   ├── hal_can.c/.h             # ECAN periferie PIC + MCP2562
│   ├── hal_sys.c/.h             # timery, ADC/FVR, LED, debug jumper
│   └── config.h                 # všechny konstanty a přepínače
├── test/
│   ├── test_decode.c
│   ├── test_compute.c
│   ├── test_persist.c
│   ├── fixtures/                # tvoje reálné logy z USBtinu
│   │   ├── 01_ign_only.txt
│   │   ├── 02_idle_60s.txt
│   │   ├── 03_drive.txt
│   │   └── 05_rev3000.txt
│   └── Makefile                 # gcc, běží na hostu
├── tools/
│   ├── replay.py                # prožene log host buildem a vypíše výstupy
│   └── canlog.py                # parser formátu USBtinVieweru
├── mplab/                       # MPLAB X projekt (XC8)
└── .github/workflows/ci.yml     # host testy + build XC8
```

**Klíčové architektonické rozhodnutí:** `decode.c`, `compute.c` a `txframes.c`
nesmí obsahovat jediný `#include <xc.h>`. Berou na vstup pole bajtů a čas
v milisekundách, vracejí čísla. Díky tomu je celý mozek zařízení přeložitelný
gcc a testovatelný na tvých skutečných logách bez jediného kusu hardwaru.

To je přesně to, co má zabránit deseti iteracím desky. Než vůbec něco spájíš,
poběží `tools/replay.py test/fixtures/03_drive.txt` a vypíše sloupec spotřeby,
který si očima porovnáš s realitou.

### `mfd15` — displej a TRI

```
mfd15/
├── README.md                    # jak se soubor nahrává přes oDSS
├── tri/
│   ├── S-AQY.TRI                # aktuální produkční, 16 senzorů
│   └── reference/               # oficiální Gen2 soubory jako vzory
│       ├── S-LINK.TRI
│       └── S-MAXX720.TRI
└── docs/
    ├── sensors.md               # popis všech 16 senzorů
    ├── tri-format.md            # 26 sloupců, význam každého
    └── internal-sensors.md      # FFF kanály, Gen2 škálování 0-1023 → 0-56
```

Oddělený repozitář proto, že TRI se bude měnit jinou frekvencí než firmware
a nemá žádný build. Zároveň je to jediná část, kterou by mohl chtít někdo
jiný s Beetlem a MFD15 — a ta je použitelná i bez převodníku.

---

## 2. Fáze prací

| # | Fáze | Výstup | Blokuje |
|---|---|---|---|
| 0 | Založení repozitářů, CI skeleton | tři prázdná repa, zelená CI | — |
| 1 | Jádro v C + host testy | `replay.py` vypíše spotřebu z logů | — |
| 2 | Schéma + PCB v KiCadu | gerbery, BOM, objednávka | — |
| 3 | Breadboard, listen-only v autě | ověřený dekodér na živé sběrnici | 1, nákup |
| 4 | Breadboard vysílá | MFD ukazuje reálná čísla | 3 |
| 5 | Osazení PCB, montáž | hotové zařízení v průduchu | 2, 4 |
| 6 | Kalibrace | ztrátový moment, nádrž | 5 |

Fáze 1 a 2 běží paralelně a ani jedna nepotřebuje auto.

---

## 3. Fáze 1 — jádro (nejdřív tohle)

Pořadí je zvolené tak, aby každý krok šel ověřit proti reálným datům.

1. `tools/canlog.py` — parser formátu `t480 8 <hex>` z USBtinVieweru.
2. `decode.c` — extrakce sedmi signálů podle tabulky. Testy: proti známým
   hodnotám z logů (volnoběh 797 ot/min, CLT 100,5 °C, čítač 0 v ign_only).
3. Detekce restartu motoru a inicializační rampy 0x1A0 (b1 == 0x40).
   Testy: `01_ign_only.txt` nesmí vygenerovat jediný nesmyslný skok delty.
4. `compute.c` — akumulátory µl a metrů, okamžitá a průměrná spotřeba,
   dojezd, moment po odečtu ztrát, výkon. Testy: `02_idle_60s.txt` musí dát
   310 µl/s, `05_rev3000.txt` 958 µl/s.
5. `txframes.c` — skládání 0x600/0x601/0x602, unsigned big endian.
6. `persist.c` — kruhový buffer v EEPROM, 12B záznam, 64 slotů, zápis
   1× za 60 s jen při změně. Testy: simulace 100 000 cyklů, kontrola
   rovnoměrného opotřebení a korektního obnovení po výpadku.
7. `main.c` — kooperativní scheduler na jednom timeru, žádné RTOS.
   Sloty: 10 ms čtení CAN, 100 ms TX 0x600/0x601, 1 s TX 0x602 + EEPROM.

Až tohle projde, je hotová veškerá logika, kterou by bylo bolestivé ladit
s pájkou v ruce.

### 3.1 FuelNow — dvojí jednotka podle rychlosti

Kanál FuelNow (0x600 b0-1, krok 0,1) nese **dvě různé veličiny** podle
rychlosti, jako palubní počítače moderních aut:

```
v <  4,0 km/h  →  posílá se okamžitý průtok v l/h
v >= 4,0 km/h  →  posílá se spotřeba v l/100 km
```

- **Jediný práh, žádná hystereze.** Skok při přepnutí je záměr — je to vizuální
  signál, že se přepnulo. Pásmo 0,5 km/h se dá přidat později, kdyby číslo
  poblikávalo při popojíždění přesně kolem prahu.
- **Ořezat na 999** (tj. 99,9 na displeji). Ručička v TRI má max 99.90
  a vyšší hodnota by se chovala neurčitě.
- **Proč 4 a ne 3 km/h:** při 3 km/h stačí průtok nad 3 l/h a hodnota přeleze
  99,9, takže by při každém normálním rozjezdu byla useknutá. Při 4 km/h je
  ta hranice až u 4 l/h.

Očekávané hodnoty l/100 km za prahem:

| průtok | 4 km/h | 6 km/h | 10 km/h | 15 km/h | 20 km/h |
|---|---|---|---|---|---|
| 1,5 l/h | 37,5 | 25,0 | 15,0 | 10,0 | 7,5 |
| 3 l/h | 75,0 | 50,0 | 30,0 | 20,0 | 15,0 |
| 6 l/h | 150 → 99,9 | 100 → 99,9 | 60,0 | 40,0 | 30,0 |

Obě konstanty (`FUELNOW_LH_BELOW_KMH`, `FUELNOW_CLAMP`) patří do `config.h`.

**FuelAvg zůstává vždy v l/100 km.** Počítá se jako podíl akumulovaných
mikrolitrů a metrů, ne integrací okamžité hodnoty — stání na semaforu tak
průměr nezničí. Průtok v l/h je navíc dostupný i samostatně v 0x601 b4-5
(krok 0,01 l/h), kdyby sis někdy chtěl přidat dedikovaný senzor.

Ostatní corner cases: průtok 0 → 0,0; výpadek zdroje dat > 500 ms → nuly;
dojezd z klouzavého průměru přes 30 segmentů po 1 km; nádrž tlumit 60 s.

---

## 4. Fáze 2 — deska

Rekapitulace zadání, ať je při návrhu po ruce:

- **MCU:** PIC18F25K80 (DIP, máš doma), krystal 16 MHz + 2× 22 pF
- **Transceiver:** MCP2562 (koupit — MCP2561 už nemáš volné)
- **Napájení:** 5 V přímo z MFD15 konektor C6, GND C12. Žádný měnič,
  žádná ochrana proti přepólování, žádný TVS — 12V větev z návrhu vypadla.
  Odběr musí zůstat hluboko pod limitem 0,5 A (reálně půjde o ~30 mA).
- **CAN:** C7 = CAN-H, C8 = CAN-L. **Terminaci neosazovat** — sběrnice už
  je zakončená v autě, třetí 120 Ω by ji přetížil. Pájecí jumper pro
  případ bench testu je ale rozumný.
- **Konektor:** 4pin, výběr v GME. Y-rozbočka jen na konektoru C.
- **LED:** dvě (napájení, stav CAN), aktivní jen když je nasazený debug
  jumper na RA0. V autě nesvítí nic.
- **Programování:** 5pin ICSP hlavička pro PICkit.
- **Rozměry:** deska ~55 × 45 mm, dvouvrstvá, převážně THT.
  Krabička do průduchu 6,5 × 5,5 cm, hloubka max ~3 cm (průduch má 7 cm,
  ale zbytek spotřebují konektory, které se nesmí páčit).
- **Blokování:** 100 nF u každého napájecího pinu, 10 µF na vstupu.

Do CI přidat `kicad-cli sch erc` a `kicad-cli pcb drc` — obojí musí projít
před objednáním desek.

### 4.1 Nákup součástek

Kompletní BOM vypadne až ze schématu, takže **seznam pro GME sestavit až
po fázi 2**, ne dřív. Kupovat nadvakrát je horší než kupovat později.

Co se ze šuplíku použije a co ne:

- **Ze šuplíku:** PIC18F25K80. Polovodiče v suchu nedegradují časem, jen
  statikou při manipulaci. Jsou to zároveň ty drahé a hůř sehnatelné kusy.
- **Nové:** krystal, všechny kondenzátory, odpory, konektory, patice, LED.
  Elektrolyty opravdu stárnou — bez napětí se rozkládá oxidová vrstva
  a roste ESR. Keramiky a odpory jsou věčné, ale za pár desetikorun
  nestojí za dohledávání v krabici.
- **Nový nákup:** MCP2562.

U krystalu je hlavní argument, že u neoznačeného kusu ze šuplíku neznáš
zatěžovací kapacitu, takže bys hádal i těch 22 pF k němu.

---

## 5. Otevřená otázka: zdroj trip resetu

Je to detail — ale jen tehdy, když se návrh udělá tak, aby to detail zůstalo.
Řešení je izolovat rozhodnutí do jediného modulu:

```c
// reset_src.h
bool reset_requested(const can_frame_t *f);
```

Dvě implementace, vybrané v `config.h`:

- **`RESET_SRC_CLUSTER`** — sleduje trip počítadlo z přístrojovky
  (kandidát 0x5D8 b0). Pravidlo: `delta mod 256 == 1` je normální tik
  včetně přetečení 255→0; snížená hodnota s jinou deltou = reset.
- **`RESET_SRC_MFD`** — sleduje rámec 0x702 z MFD15, bajt 2 bitová maska
  Can Switch 1–6. Vyžaduje licenci Can Switching.

Zbytek firmwaru volá jen `reset_requested()` a o zdroj se nestará. Testy
obou variant běží na hostu proti syntetickým rámcům. Změna rozhodnutí je
jednořádková v `config.h`, ne refaktoring.

**Rozhodne jeden sniff:** zapnout USBtin, ujet pár set metrů, zmáčknout trip
reset na přístrojovce, ujet další kousek. Pokud se v logu objeví bajt, který
roste s dráhou a při stisku spadne na nulu, jede varianta CLUSTER a licenci
nekupuješ. Pokud ne, koupíš licenci a jede varianta MFD.

Žádné fyzické tlačítko v žádné z variant není.

---

## 6. Fáze 3–4 — testování v autě

Postup je stavěný tak, aby každý krok mohl selhat neškodně.

1. **Bench, listen-only.** Breadboard + USBtin na stole, USBtin vysílá
   přehrané rámce z logu, převodník je jen poslouchá. Ověří se hal_can
   a filtrace ID.
2. **Bench, vysílání.** Převodník vysílá 0x600–0x602, USBtin je čte.
   Ověří se, že bajty na drátě odpovídají tomu, co počítá host build.
3. **Auto, listen-only.** Breadboard zapojený do Y-rozbočky, ale
   s odpojeným TX pinem transceiveru. Zaznamená se, co převodník dekóduje,
   a porovná s paralelním logem z USBtinu. Nula rizika pro sběrnici.
4. **Auto, vysílání.** Teprve teď se TX připojí. Nejdřív se zkontroluje,
   že 0x600–0x602 jsou opravdu volné (v logách potvrzeno), a sleduje se
   chybový čítač ECAN periferie.
5. **MFD ukazuje čísla.** Nahrát S-AQY.TRI přes oDSS, aktivovat, porovnat
   FuelNow s FuelCntRaw. Ověřit i přepnutí jednotky kolem 4 km/h.

---

## 7. Kalibrace na závěr

- **Ztrátový moment** — lineární model podle otáček, dva body už máme
  v logách (volnoběh a 2940 ot/min v neutrálu, kde je moment na kolech
  nulový, takže indikovaný moment = ztrátový).
- **Nádrž** — natankovat známé množství z kanystru a porovnat s 0x320 b2.
  Zatím ukazuje 0 l + rezervu, což na ověření nestačí.
- **Práh přepnutí jednotky** — doladit za jízdy, je to konstanta v `config.h`.
- **Spotřeba v litrech** — nepotřebuje kalibraci, jednotka 1 µl je potvrzená
  externím zdrojem i tvými daty.

---

## 8. Co je hotové a co ne

**Hotové:** dekódování sběrnice, formát vysílaných rámců, architektura HW,
umístění, napájení, S-AQY.TRI včetně Gen2 interních senzorů, chování FuelNow.

**Nezačaté:** cokoliv v repozitářích. Fáze 0 je první věc na desktopu.

**Nejisté:** zdroj trip resetu (§5), zda je 0x420 b3 opravdu olej,
význam 0x288 b5/b6, řádek `info;` v TRI.
