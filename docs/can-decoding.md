# Dekódování hnacího CANu — VW New Beetle, motor AQY

Sběrnice 500 kbps, PQ34. Všechny hodnoty níže jsou ověřené měřením na autě,
logy jsou v `test/fixtures/`.

Rozlišujeme dva stupně jistoty:

- **Potvrzeno** — sedí napříč všemi logy a je to zamčené testem v `tools/`.
- **Otevřené** — zapsáno, ale ještě to nemá jednoznačný důkaz. Viz konec souboru.

---

## Přítomná ID

Periodicky se vysílá čtrnáct ID:

```
0x050  0x0C2  0x1A0  0x280  0x288  0x320  0x420
0x480  0x488  0x4A0  0x520  0x5A0  0x5D0  0x5D8
```

Zamčeno testem `test_regular_id_set`. Jediné, co se v krátkém logu nemusí
objevit, je 0x520 — chodí zhruba jednou za sekundu.

**0x767 není periodický rámec.** Objeví se právě jednou, v `06_trip_reset.txt`
na první časové značce, s DLC 2 a daty `3c fe`. Je to jednorázová diagnostická
odpověď zachycená při připojení USBtinu. Firmware ho ignoruje, ale rozsah
0x7xx kvůli němu nelze považovat za úplně tichý.

**Volné pro převodník:** 0x600–0x602 se na sběrnici nevyskytují v žádném logu
(`test_target_ids_are_free`).

---

## Tabulka signálů

| Signál | ID | Bajty | Vzorec | Poznámka |
|---|---|---|---|---|
| Čítač spotřeby | 0x480 | 2–3 LE, maska 0x7FFF | 1 = 1 µl | 15bit, přetéká na 32768 |
| Rychlost | 0x1A0 | 2–3 LE | × 0,005 km/h | brána v b1, viz níže |
| Otáčky | 0x280 | 2–3 LE | × 0,25 ot/min | |
| Teplota kapaliny | 0x288 | 1 | × 0,75 − 48 °C | 0xFF = chyba |
| Teplota oleje | 0x420 | 3 | × 0,75 − 48 °C | 0xFF při vypnutém motoru |
| Palivo v nádrži | 0x320 | 2, maska 0x7F | litry | bit 0x80 = rezerva |
| Moment (indikovaný) | 0x280 | 7 | ~0,67 Nm/bit | u AQY max 172 Nm |
| Škrticí klapka | 0x280 | 5 | 38 = klidová poloha | |
| Zatížení motoru | 0x280 | 6 | | 0 při vypnutém motoru |
| Rychlosti kol | 0x4A0 | 4× 16bit LE | (raw >> 1) × 0,01 km/h | bit 0 = směr |
| Zrychlení | 0x5A0 | 0 | (val − 127) / 100 G | |
| Dveře | 0x320 | 0 | bitová maska | |

DLC je pro každé ID konstantní: 0x050 má 4 bajty, 0x5D0 má 6, zbytek 8.
Parser s pevnou délkou 8 by na 0x050 a 0x5D0 spadl.

---

## Past 1: brána platnosti rychlosti není rovnost

Bajt 1 rámce 0x1A0 je **bitové pole**, ne jedna hodnota. Naměřené stavy:

| b1 | Význam | Rychlost |
|---|---|---|
| 0x40 | základní platný stav | platná |
| 0x48 | platný, s dalším příznakem | **platná** |
| 0x50 | platný, s dalším příznakem | **platná** |
| 0x43 | inicializační rampa po zapnutí zapalování | zahodit |
| 0x42 | totéž, jen 2 rámce | zahodit |

Správné pravidlo:

```c
speed_valid = (b1 & 0x40) && !(b1 & 0x03);
```

**Proč na tom záleží.** V `07_accel.txt` je 0x48 většinový stav — 1301 rámců
z 1991 — a nese plný rozsah rychlosti včetně maxima 24,78 km/h. Test na
rovnost `b1 == 0x40` zahodí dvě třetiny vzorků a ujetá dráha vyjde 14 m místo
27 m. To by přímo zkazilo FuelAvg i Range, tedy dvě ze čtyř hlavních čísel
na displeji.

Rampa 0x43 se objevuje jen v logách, které začínají zapnutím zapalování
(`01_ign_only`, `06_trip_reset`) — trvá ~0,4 s a raw hodnota během ní klesá
464 → 0. Zamčeno testem `test_init_ramp_only_after_ignition_on`.

## Past 2: čítač spotřeby se po vypnutí zapalování resetuje

Delta se počítá `(nový − starý) mod 32768`. Bez detekce restartu by delta
po novém zapnutí zapalování dala skok o desítky tisíc mikrolitrů.

```c
if (counter == 0 || rpm == 0) { prev = counter; return; }  /* reinicializovat */
```

V `06_trip_reset.txt` to sepne 324× — a je to správně, všechny detekce padnou
do souvislého úvodního úseku, kdy běží zapalování bez motoru. V `07_accel.txt`
nesepne ani jednou.

## Past 3: bit 15 čítače není konstantní

`docs/sensors.md` v repu `mfd15` tvrdí, že bit 15 je konstantně 1. **Není.**
Naměřeno napříč všemi logy:

- Od zapnutí zapalování je **nula**, dokud 15bitový čítač poprvé nepřeteče.
- Při prvním přetečení se přehodí na jedničku a už tam zůstane.

Vidět je to v `06_trip_reset.txt`, kde jde sekvence `32767 → 15` a bit 15 se
u toho přehodí z 0 na 1. V `01_ign_only.txt` je bit nulový, protože motor
stojí a čítač je celý nulový.

Pro výpočet je to jedno — maska 0x7FFF ho zahodí. Použitelné je to jako
příznak „tenhle cyklus zapalování je ještě mladý".

## Past 4: FuelAvg dělí skoro nulovou dráhou

Průměrná spotřeba je podíl akumulátorů. Hned po nastartování je dráha téměř
nulová a podíl utíká do nesmyslů — na `06_trip_reset.txt` vyšlo **21 395
l/100 km**, než auto popojelo. Pod 100 m ujeté dráhy se musí vracet nula.

---

## Ověřené hodnoty pro testy

| Log | Co to je | Čítač celkem | Doba | Průtok |
|---|---|---|---|---|
| `01_ign_only` | zapalování bez motoru | 0 µl | — | 0 |
| `02_idle_60s` | zahřátý volnoběh 797 ot/min | 18 652 µl | 60,1 s | **310 µl/s = 1,12 l/h** |
| `05_rev3000` | 2940 ot/min v neutrálu | 1 940 µl | 1,93 s | 1005 µl/s = 3,62 l/h |
| `06_trip_reset` | stání a popojetí | 51 992 µl | 135,0 s | 385 µl/s |
| `07_accel` | rozjezd na 24,8 km/h | 9 752 µl | 15,9 s | 613 µl/s |

Zahřívací křivka teploty kapaliny napříč první session:
`idle` 68,25 → `05_rev3000` 90,0 → `03_drive` 99,0 → `01_ign_only` 100,5 °C.

Ujetá dráha v `06_trip_reset` vychází 125 m, což sedí na „popojet aspoň
0,1 km" z checklistu harnessu.

---

## Periody rámců

Zadání uvádí 0x1A0 = 7,5 ms, 0x4A0 = 8,0 ms, 0x280 = 10,5 ms, 0x288 = 11,8 ms,
0x480 = 49,5 ms.

**Z logů se to potvrdit nedá** a je potřeba s tím počítat. Časové značky
z USBtinVieweru jsou kvantované po ~15,6 ms (tik systémového časovače
Windows), takže naměřené periody vycházejí jako násobky: 16, 31, 47, 94,
188 ms. Rozlišit 7,5 od 10,5 ms je pod rozlišovací schopností záznamu.

Navíc je 39–51 % řádků v každém logu **bezprostředním duplikátem** předchozího
rámce se stejným ID i daty. Na výpočet delty to vliv nemá (delta je nula),
ale měřenou periodu to zdvojnásobuje.

Nepřímý důkaz pro 49,5 ms u 0x480: při této periodě vychází volnoběžný průtok
z `02_idle_60s` na 310,1 µl/s, což je přesně hodnota ze zadání, a délka
záznamu na 60,1 s, což sedí na název souboru. To je silná shoda.

---

## Co na sběrnici NENÍ

- **Lambda** — 0x488 je ve všech logách konstantní `ff ff ff 8d ff ff ff ff`.
- **Napětí baterie** — systematicky prohledáno, nic. Řeší se interním
  senzorem displeje.
- **Venkovní teplota** — 0x420 b1 i b2 jsou nulové, čidlo v autě není.
- **Trip kilometry a trip reset** — viz otevřené otázky.

---

## Otevřené otázky

1. **Průtok v `05_rev3000` nesedí na zadání.** Zadání uvádí 958 µl/s, z dat
   vychází 1005 µl/s. Rozdíl 5 % nesedí na data, ale na předpokládanou
   periodu 0x480 — při 51,9 ms by vyšlo přesně 958. Log časové značky nemá,
   takže to rozhodne až měření periody na živé sběrnici.

2. **Počáteční hodnota čítače v `07_accel`.** Zadání uvádí 13247 → 22622,
   v souboru je první vzorek 12870. Konec sedí, začátek ne. Rozdíl 377 µl
   je několik prvních rámců — pravděpodobně se v zadání počítalo od jiného
   místa v logu.

3. **0x288 b5 a b6** — zátěžové a nedekódované. Kandidáti MAF, předstih,
   vstřikovací čas. Nejrychleji porovnáním s měřenými bloky ve VCDS.

4. **0x420 b3 = olej, nebo IAT?** `07_accel` byl pořízen právě na tohle.
   Teplota během rozjezdu drží 75,75 → 76,5 °C, tedy **neklesá**. IAT by
   při rozjezdu spadl. To mluví pro olej, ale rozjezd byl krátký (16 s),
   takže to není definitivní.

5. **AccelG: podélné, nebo příčné?** Rozhodne zaparkování napříč na svahu.

6. **Zdroj trip resetu** — kandidát 0x5D8 b0. Log `06_trip_reset` byl
   pořízen právě na tohle a ještě není vyhodnocený.

7. **Kalibrace ztrátového momentu** — dva body jsou v logách (volnoběh
   a 2940 ot/min v neutrálu), zbývá dosadit.
