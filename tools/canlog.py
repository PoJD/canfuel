#!/usr/bin/env python3
"""Parser logu z USBtinu. Umi oba formaty, ktere mame ve fixtures.

Format A -- syrovy slcan proud, tak jak ho USBtin posila po seriove lince
a jak ho stary zaznam ulozil bez uprav:

    t1a0800400100fefe001d
    ^ ^  ^^
    | |  +- data, 2 hex znaky na bajt
    | +---- DLC, jeden hex znak
    +------ 11bit ID, tri hex znaky

Casove znacky v nem nejsou. Vraci se ts=None a je na volajicim, jestli si
cas dopocita z period ramcu (viz docs/can-decoding.md, sekce o periodach --
neni to spolehlive).

Format B -- export z USBtinVieweru, pet sloupcu oddelenych tabulatorem:

    2078 <TAB> jar:file:/...receive.png <TAB> 320h <TAB> 8 <TAB> 05 00 86 ...
    ts (ms)    ikona radku               ID+h    DLC    bajty po mezerach

Radky s ikonou info.png jsou hlasky vieweru ("Connected to USBtin", ...):
maji prazdny sloupec ID i DLC a text v poslednim sloupci. Preskakuji se.

Pouziti z prikazove radky:

    python canlog.py FILE [FILE ...]           # souhrn per ID
    python canlog.py --dump FILE               # vypis vsech ramcu
    python canlog.py --id 0x480 --dump FILE    # jen jedno ID
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Iterator, Optional

__all__ = ["Frame", "parse_line", "parse_file", "iter_frames", "undouble",
           "LogFormatError"]


class LogFormatError(ValueError):
    """Radek vypada jako ramec, ale nejde rozebrat."""


@dataclass(frozen=True)
class Frame:
    """Jeden CAN ramec z logu.

    ts_ms je None u formatu A, ktery casove znacky neobsahuje.
    """

    ts_ms: Optional[int]
    can_id: int
    data: bytes

    @property
    def dlc(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        ts = "        -" if self.ts_ms is None else f"{self.ts_ms:9d}"
        return f"{ts}  0x{self.can_id:03X}  [{self.dlc}]  {self.data.hex(' ')}"


# --------------------------------------------------------------------------
# parsovani
# --------------------------------------------------------------------------

def _parse_slcan(line: str) -> Optional[Frame]:
    """Format A: tIIILDD...  (a 'T' varianta pro 29bit ID)."""
    kind = line[0]
    if kind == "t":
        id_len = 3
    elif kind == "T":
        id_len = 8
    else:
        return None

    head = 1 + id_len + 1  # 't' + ID + DLC
    if len(line) < head:
        raise LogFormatError(f"slcan radek je prilis kratky: {line!r}")

    try:
        can_id = int(line[1:1 + id_len], 16)
        dlc = int(line[1 + id_len], 16)
    except ValueError as exc:
        raise LogFormatError(f"nectitelne ID/DLC: {line!r}") from exc

    if dlc > 8:
        raise LogFormatError(f"DLC {dlc} > 8: {line!r}")

    payload = line[head:head + 2 * dlc]
    if len(payload) != 2 * dlc:
        raise LogFormatError(f"DLC={dlc} slibuje {2 * dlc} hex znaku, je jich {len(payload)}: {line!r}")

    try:
        data = bytes.fromhex(payload)
    except ValueError as exc:
        raise LogFormatError(f"nectitelna data: {line!r}") from exc

    return Frame(None, can_id, data)


def _parse_viewer(line: str) -> Optional[Frame]:
    """Format B: ts <TAB> ikona <TAB> IDh <TAB> DLC <TAB> bajty."""
    cols = line.split("\t")
    if len(cols) < 5:
        return None

    ts_raw, _icon, id_raw, dlc_raw, data_raw = cols[0], cols[1], cols[2], cols[3], cols[4]

    # Informacni radky vieweru maji prazdne ID i DLC a text v poslednim sloupci.
    if not id_raw.strip() or not dlc_raw.strip():
        return None

    id_txt = id_raw.strip()
    if id_txt.lower().endswith("h"):
        id_txt = id_txt[:-1]

    try:
        can_id = int(id_txt, 16)
        dlc = int(dlc_raw.strip())
    except ValueError as exc:
        raise LogFormatError(f"nectitelne ID/DLC: {line!r}") from exc

    if dlc > 8:
        raise LogFormatError(f"DLC {dlc} > 8: {line!r}")

    try:
        data = bytes.fromhex(data_raw.replace(" ", ""))
    except ValueError as exc:
        raise LogFormatError(f"nectitelna data: {line!r}") from exc

    if len(data) != dlc:
        raise LogFormatError(f"DLC={dlc}, ale bajtu je {len(data)}: {line!r}")

    ts_ms = int(ts_raw.strip()) if ts_raw.strip() else None
    return Frame(ts_ms, can_id, data)


def parse_line(line: str) -> Optional[Frame]:
    """Rozebere jeden radek. Vraci None u radku, ktery ramec nenese.

    Rozliseni formatu je podle tabulatoru -- format A ho nikdy neobsahuje.
    """
    line = line.rstrip("\r\n")
    if not line.strip():
        return None
    if "\t" in line:
        return _parse_viewer(line)
    return _parse_slcan(line.strip())


def iter_frames(fh, *, strict: bool = False) -> Iterator[Frame]:
    """Prozene otevreny soubor a vraci ramce.

    strict=True nechá LogFormatError probublat ven i s cislem radku;
    ve vychozim rezimu se poskozeny radek preskoci (USBtin obcas urizne
    posledni radek pri zavreni portu).
    """
    for lineno, line in enumerate(fh, start=1):
        try:
            frame = parse_line(line)
        except LogFormatError as exc:
            if strict:
                raise LogFormatError(f"radek {lineno}: {exc}") from exc
            continue
        if frame is not None:
            yield frame


def undouble(lines: list[str]) -> list[str]:
    """Zahodi druhou kopii, kdyz soubor obsahuje zaznam presne dvakrat.

    Fixture 02_idle_60s.txt je takhle poskozeny -- obe poloviny jsou bajt po
    bajtu shodne. Bez teto opravy vychazi volnobezny prutok dvojnasobny.
    Detaily viz test/fixtures/README.md.
    """
    n = len(lines)
    if n >= 2 and n % 2 == 0 and lines[: n // 2] == lines[n // 2:]:
        return lines[: n // 2]
    return lines


def parse_file(path, *, strict: bool = False, fix_doubled: bool = False) -> list[Frame]:
    """Nacte cely log.

    fix_doubled=True nejdriv zkontroluje, jestli soubor neobsahuje zaznam
    dvakrat, a pripadnou druhou kopii zahodi. Pro vypocet spotreby to zapinej
    vzdycky; pro kontrolu integrity souboru naopak nikdy.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        if not fix_doubled:
            return list(iter_frames(fh, strict=strict))
        lines = undouble(fh.read().splitlines())
    return list(iter_frames(lines, strict=strict))


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _summary(path: str, frames: list[Frame]) -> None:
    if not frames:
        print(f"{path}: zadny ramec")
        return

    stamped = [f.ts_ms for f in frames if f.ts_ms is not None]
    fmt = "USBtinViewer (s casovymi znackami)" if stamped else "slcan (bez casovych znacek)"

    print(f"{path}")
    print(f"  format : {fmt}")
    print(f"  ramcu  : {len(frames)}")
    if stamped:
        print(f"  rozsah : {stamped[0]} .. {stamped[-1]} ms ({(stamped[-1] - stamped[0]) / 1000:.2f} s)")

    per_id: dict[int, int] = {}
    dlcs: dict[int, set[int]] = {}
    for f in frames:
        per_id[f.can_id] = per_id.get(f.can_id, 0) + 1
        dlcs.setdefault(f.can_id, set()).add(f.dlc)

    print("  ID     ramcu   DLC")
    for can_id in sorted(per_id):
        seen = ",".join(str(d) for d in sorted(dlcs[can_id]))
        print(f"  0x{can_id:03X}  {per_id[can_id]:7d}   {seen}")


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Parser logu z USBtinu (oba formaty).")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--dump", action="store_true", help="vypsat ramce misto souhrnu")
    ap.add_argument("--id", type=lambda s: int(s, 0), action="append",
                    help="filtrovat na dane ID, lze opakovat (napr. --id 0x480)")
    ap.add_argument("--strict", action="store_true", help="spadnout na prvnim poskozenem radku")
    ap.add_argument("--fix-doubled", action="store_true",
                    help="zahodit druhou kopii, kdyz soubor obsahuje zaznam dvakrat")
    args = ap.parse_args(argv)

    wanted = set(args.id) if args.id else None

    for path in args.files:
        frames = parse_file(path, strict=args.strict, fix_doubled=args.fix_doubled)
        if wanted is not None:
            frames = [f for f in frames if f.can_id in wanted]
        if args.dump:
            for f in frames:
                print(f)
        else:
            _summary(path, frames)
    return 0


if __name__ == "__main__":
    sys.exit(main())
