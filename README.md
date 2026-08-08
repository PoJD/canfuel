# canfuel

Převodník spotřeby pro VW New Beetle s motorem AQY (2,0 l / 85 kW, PQ34).

Čte hnací CAN sběrnici, počítá okamžitou a průměrnou spotřebu, dojezd, moment
a výkon, a posílá je zpět na sběrnici ve vlastních rámcích. Displej CANchecked
MFD15 Gen2 je zobrazuje jako běžné senzory.

Fyzicky sedí v průduchu za displejem, napájený 5 V přímo z displeje.

## Stav

Fáze 0 — repozitář založený, dekódování sběrnice zdokumentované a ověřené
proti reálným logům. Firmware zatím nenapsaný.

## Rychlý start

```
python -m unittest discover -s tools -p "test_*.py"
python tools/replay.py --every 100 test/fixtures/07_accel.txt
```

`replay.py` je referenční dekodér v Pythonu. Prožene log stejnými vzorci,
jaké bude mít firmware, a vypíše sloupec spotřeby ke kontrole očima.

## Dokumentace

| Soubor | Obsah |
|---|---|
| `docs/can-decoding.md` | tabulka signálů, čtyři pasti, ověřené hodnoty |
| `docs/frames.md` | layout rámců 0x600–0x602, FuelNow, Range, moment |
| `docs/refuel-reset.md` | reset průměru při tankování |
| `docs/implementacni-plan.md` | celkový plán všech fází |
| `test/fixtures/README.md` | popis logů a známé vady dat |

## Struktura

```
src/     firmware (jádro v čistém C, HAL zvlášť)
test/    host testy přes gcc + fixtures
tools/   canlog.py, replay.py a jejich testy
mplab/   MPLAB X projekt (XC8)
```

## Související repozitáře

- `kicad` — deska převodníku
- `mfd15` — TRI soubor pro displej

## Licence

Zatím neurčeno.
