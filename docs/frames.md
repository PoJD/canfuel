# Rámce, které převodník vysílá

Tři vlastní rámce na volných ID. Ve všech logách je ověřeno, že 0x600–0x602
nikdo jiný nepoužívá (`test_target_ids_are_free`).

**Vše unsigned big endian.** Little endian používá auto, big endian používáme
my — je to schválně, ať se to nedá splést, a MFD15 to umí obojí (sloupec
Format v TRI, 0 = big endian).

---

## 0x600 @ 100 ms — spotřeba

| Bajty | Hodnota | Krok | Rozsah |
|---|---|---|---|
| 0–1 | FuelNow | 0,1 | dvojí jednotka, viz níže |
| 2–3 | FuelAvg | 0,1 l/100 km | 0–999 |
| 4–5 | FuelTank | 0,1 l | tlumeno 60 s |
| 6–7 | Range | 1 km | |

## 0x601 @ 100 ms — motor a diagnostika

| Bajty | Hodnota | Krok |
|---|---|---|
| 0–1 | Power | 0,1 kW |
| 2–3 | Torque | 0,1 Nm |
| 4–5 | Průtok | 0,01 l/h |
| 6–7 | VddConv | 0,01 V |

Průtok je v 0x601 samostatně i v případě, že FuelNow zrovna posílá l/100 km.
Díky tomu jde na displej přidat dedikovaný senzor, aniž by se cokoliv měnilo.

VddConv je napájecí napětí, které si PIC změří sám přes vestavěnou referenci
FVR 1,024 V: `VDD = 1,024 × 1023 / ADC`. Nula externích součástek.

## 0x602 @ 1 s — dráha a palivo od resetu

Pomalý rámec, slouží k diagnostice a k ověření, že se akumulátory chovají.

---

## FuelNow — dvojí jednotka

```
v <  4,0 km/h  →  posílá se okamžitý průtok v l/h
v >= 4,0 km/h  →  posílá se spotřeba v l/100 km
```

**Jediný práh, žádná hystereze.** Skok při přepnutí je záměrný vizuální
signál, že se přepnulo. Pásmo 0,5 km/h se dá přidat později, kdyby číslo
poblikávalo při popojíždění přesně kolem prahu.

**Ořezat na 999** (99,9 na displeji). Ručička v TRI má max 99.90 a vyšší
hodnota by se chovala neurčitě.

**Proč 4 a ne 3 km/h:** při 3 km/h stačí průtok nad 3 l/h a hodnota přeleze
99,9, takže by při každém normálním rozjezdu byla useknutá. Při 4 km/h je
ta hranice až u 4 l/h.

Konstanty `FUELNOW_LH_BELOW_KMH` a `FUELNOW_CLAMP` patří do `config.h`.

Když je rychlost neplatná (brána v 0x1A0 b1, viz `can-decoding.md`), posílá
se l/h — bez důvěryhodné rychlosti nemá l/100 km smysl.

---

## FuelAvg

Vždy l/100 km. Počítá se jako **podíl akumulovaných mikrolitrů a metrů**,
ne integrací okamžité hodnoty — stání na semaforu tak průměr nezničí.

Pod 100 m ujeté dráhy vracet nulu. Bez té pojistky vychází dělení skoro
nulovou dráhou; na `06_trip_reset.txt` to dávalo 21 395 l/100 km.

Akumulátory se ukládají do EEPROM 1× za 60 s, kruhový buffer, 64 slotů.

---

## Range

```
zbylé litry ÷ (klouzavá spotřeba za posledních 30 km) × 100
```

Klouzavý průměr po segmentech 1 km, tedy 30 slotů. Chová se pak jako
v moderních autech — po sešlápnutí plynu na dálnici postupně klesá,
neskočí okamžitě.

Dokud není najeto aspoň 5 km od startu, použije se konzervativní default
9 l/100 km, aby odhad nebyl při studeném startu nesmysl.

---

## Torque a Power

Od indikovaného momentu (0x280 b7) se odečte **ztrátový moment** — tření,
čerpadla, alternátor. Není konstantní, roste s otáčkami, modeluje se
lineárně podle otáček.

Kalibrace ve dvou bodech, oba už jsou v logách:

- volnoběh (`02_idle_60s`, 797 ot/min)
- 2940 ot/min v neutrálu (`05_rev3000`) — moment na kolech je nulový,
  takže indikovaný moment = ztrátový

```
výkon [kW] = moment [Nm] × otáčky [1/min] ÷ 9550
```

MFD15 to spočítat neumí — math kanály jsou podle manuálu jen pro MFD28/32.

---

## Corner cases

| Situace | Chování |
|---|---|
| průtok 0 | FuelNow 0,0 |
| výpadek zdroje dat > 500 ms | všechny hodnoty nuly |
| dráha < 100 m | FuelAvg 0,0 |
| dráha < 5 km | Range počítá s 9 l/100 km |
| rychlost neplatná | FuelNow v l/h |
| hodnota nad rozsah | ořez na 999 |
