# Reset průměrné spotřeby — pouze při tankování

Žádné tlačítko, žádná licence Can Switching, žádné RTC. Chová se to jako
„spotřeba od tankování" v moderních autech.

---

## Pravidlo

```
tankStableL = medián (0x320 b2 & 0x7F) přes posledních 20–30 s stání (v < 1 km/h)
```

- Aktualizovat **jen vestoje**. Za jízdy hodnotu ignorovat úplně.
- Nárůst `tankStableL` o **více než 3 L** = tankování → vynulovat akumulátory
  průměru.
- Pravidlo platí i v rámci jedné session, takže pokrývá i tankování
  s běžícím motorem.
- `tankStableL` se ukládá do EEPROM jako součást stávajícího 12B záznamu
  (zápis 1× za 60 s), aby přežil vypnutí zapalování.
- Při prvním startu s prázdnou EEPROM jen inicializovat, **neresetovat**.

---

## Proč práh 3 L a proč medián

Naměřeno na reálných datech.

Vestoje má hodnota rozptyl jen 2–3 L a drtivě dominuje jedna hodnota —
1584 z 1622 vzorků bylo přesně 6 L. Za jízdy je rozptyl 9–10 L a rovnoměrně
rozprostřený, protože plovák v nádrži šplouchá při každém zatáčení a brzdění.

Okamžitá hodnota je tedy nepoužitelná, medián z klidu je pevný jako skála.

Že je to reálné, potvrzuje i `07_accel.txt`: během krátkého rozjezdu skáče
b2 mezi 1, 5, 7 a 9 litry. Kdyby se na okamžitou hodnotu navázal reset,
spouštěl by se při každém rozjezdu.

---

## Proč ne trip reset z přístrojovky

Původní návrh (viz `implementacni-plan.md`, §5) chtěl navázat na trip reset
přístrojovky a měl dvě varianty za `#ifdef`. Log `06_trip_reset.txt` byl
pořízen právě na to rozhodnutí a **zatím není vyhodnocený**.

Vazba na tankování je proti tomu lepší v tom, že nepotřebuje ani sniff, ani
licenci, ani rozhodnutí — funguje na datech, která už spolehlivě máme. Pokud
se z `06_trip_reset.txt` ukáže, že se trip km na sběrnici vysílají, dá se
varianta CLUSTER přidat jako druhý spouštěč, ne jako náhrada.

---

## Pozor při implementaci

Nádrž v současných datech hlásí **0 litrů a svítící rezervu** (b2 = 0x80)
ve všech logách první session. Testovat pravidlo na těchto datech tedy nejde
— je potřeba log z natankování. Do té doby to musí jet na syntetických
rámcích v `test_compute.c`.
