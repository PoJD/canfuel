#!/usr/bin/env python3
"""Fail when the prose disagrees with the code, or quotes a number it should not.

    python tools/checkdocs.py            # report
    python tools/checkdocs.py --check    # ...and exit non-zero if anything is wrong

Every documentation fix on 2026-08-12 was a NUMBER, not an argument. The
paragraphs around them still reasoned correctly; only the figures had moved,
because one constant changed in config.h and eleven sentences elsewhere did
not. Grep does not find them: "half a millisecond a minute" contains no
mention of PERSIST_INTERVAL_MS.

So this is the same shape as tools/cycles.py --check and tools/divconst.py
--check -- a CI gate that reads the source of truth and refuses to agree with
prose that has drifted away from it. Two rules, from docs/../CLAUDE.md:

  1. A number that can be MEASURED is not written down at all. Test counts,
     binary counts, byte counts: the command prints them, and a file that
     repeats them only goes stale. FORBIDDEN below is that rule, mechanised.
  2. A number DERIVED from a constant is derived in one place. Everywhere
     else says what it means, not what it is. DERIVED below checks the places
     that genuinely need the figure to read well.

Datasheet numbers are a third kind and are deliberately not checked: the PDF
is frozen, so D122's 4 ms cannot go stale. Cite those freely.

ADDING A CHECK. Put it in DERIVED or FORBIDDEN and give it a `why`. If a line
legitimately states an old value -- docs/refuted.md and docs/optimisation.md
record what things used to be, in the past tense -- add it to ALLOW with the
reason, rather than weakening the pattern for everybody.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Files whose prose is checked. Sources are in here too: a stale comment beside
# the code is worth exactly as much as a stale sentence in a document, and on
# 2026-08-12 four of the nineteen fixes were comments.
SCAN = [
    "*.md",
    "docs/*.md",
    "mplab/*.md",
    "test/*.md",
    "test/fixtures/*.md",
    "src/*.c",
    "src/*.h",
    "test/*.c",
    "test/*.h",
]

NUMBER_WORDS = {
    "no": 0, "once": 1, "twice": 2, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20,
}
WORD_FOR = {v: k for k, v in NUMBER_WORDS.items() if k not in ("no", "one", "two")}
WORD_FOR[1] = "one"
WORD_FOR[2] = "two"


def word_to_int(text):
    """'three' -> 3, '17' -> 17, '1,024' -> 1024. None if it is not a number."""
    key = text.strip().lower().replace(",", "")
    if key in NUMBER_WORDS:
        return NUMBER_WORDS[key]
    return int(key) if key.isdigit() else None


def defines(path):
    """The #define name -> integer value, for the ones that are plain integers."""
    out = {}
    pattern = re.compile(r"^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+|\d+)[uU]?\b")
    for line in path.read_text(encoding="utf-8").splitlines():
        m = pattern.match(line)
        if m:
            out[m.group(1)] = int(m.group(2), 0)
    return out


CFG = defines(ROOT / "src" / "config.h")


def accepted_can_ids():
    """How many identifiers the firmware asks the hardware filters to accept."""
    return sum(
        1 for name in CFG
        if name.startswith("CAN_ID_") and not name.startswith("CAN_ID_TX_")
    )


def fixture_count():
    return len(list((ROOT / "test" / "fixtures").glob("*.txt")))


# --------------------------------------------------------------------------
# Facts that ARE derived from something, and the prose that states them.
#
# `pattern` must capture the stated quantity in group 1. `expected` returns the
# integer it has to equal. `needs` keeps the pattern from firing on unrelated
# sentences -- the line must also contain one of these words.
# --------------------------------------------------------------------------

DERIVED = [
    dict(
        name="eeprom-writes-per-minute",
        why="PERSIST_INTERVAL_MS went 60 s -> 20 s on 2026-08-12 and eleven "
            "places still said 'once a minute'",
        pattern=re.compile(
            r"\b(once|twice|three times|four times|\d+ times)\s+a\s+minute\b", re.I),
        needs=("eeprom", "persist", "write", "crc"),
        expected=lambda: 60_000 // CFG["PERSIST_INTERVAL_MS"],
        render=lambda n: {1: "once", 2: "twice"}.get(n, f"{WORD_FOR.get(n, n)} times")
                         + " a minute",
    ),
    dict(
        name="accepted-identifiers",
        why="0x5A0 was dropped on 2026-08-11; CLAUDE.md still said seven",
        pattern=re.compile(r"\bthe\s+(\w+)\s+identifiers\s+we\s+accept\b", re.I),
        needs=("identifier",),
        expected=accepted_can_ids,
        render=lambda n: f"the {WORD_FOR.get(n, n)} identifiers we accept",
    ),
]

# A fixture-count check was written and then deleted. "two recordings" and
# "seven fixtures" are all over the documents and almost always mean a chosen
# subset, not the corpus, so the pattern fired on five correct sentences and
# nothing else. A gate with that hit rate teaches people to skip its output,
# which is the failure mode `test_props.c` is warned about for the same reason:
# manufacture failures nobody can reach and the next reader ignores the test.
# Adding a fixture is also a deliberate act with a table in
# test/fixtures/README.md, not a silent drift. Left out on purpose.

# --------------------------------------------------------------------------
# Numbers that must not be written down at all, because a command prints them
# and the file can only go stale. CLAUDE.md already states this rule for the
# hex size -- "Exact byte counts are deliberately not quoted here" -- and then
# quoted them four lines later. Hence mechanising it.
# --------------------------------------------------------------------------

FORBIDDEN = [
    dict(
        name="test-counts",
        why="`make -C test test` prints the count; it moves with every test added",
        pattern=re.compile(
            r"\d[\d,.]*\s*(?:\+|M|million)?\s*(?:hand-written\s+)?"
            r"(?:checks|tests)\b(?!\s+run as part)", re.I),
        fix="say what the suite proves, not how many assertions it runs",
    ),
    dict(
        name="binary-counts",
        why="test/Makefile globs test_*.c; the number changes when a file is added",
        pattern=re.compile(r"\b\w+\s+test\s+binaries\b", re.I),
        fix="name the binaries that matter, or say 'the test binaries'",
    ),
    dict(
        name="build-size",
        why="`make -C mplab` prints program and RAM usage on every build",
        pattern=re.compile(
            r"\d[\d,]*\s*bytes\s+of\s+(?:32,?768|3,?649)\b", re.I),
        fix="say that it fits and point at `make -C mplab`",
    ),
]

# (path suffix, substring that must appear on the line, why it is allowed)
ALLOW = [
    ("docs/optimisation.md", "1.17 million checks run as part of",
     "a measurement of the exhaustive build, dated in its own section"),
    ("docs/optimisation.md", "340,000 fewer checks",
     "a before/after figure in the optimisation record, past tense"),
    ("test/test_divconst.c", "1.17 million checks",
     "for the exhaustive proof the count IS the claim, not decoration"),
    ("tools/checkdocs.py", "", "this file describes the patterns it forbids"),
]


# --------------------------------------------------------------------------
# The generated block.
#
# Rule 1 says a measurable number is not written down -- but the size of the
# firmware and what it costs the part are genuinely interesting, and "run make
# and read the output" is a poor answer for somebody reading the repository on
# a machine with no compiler. So one block is GENERATED instead of forbidden:
# `--write` fills it from the real artefacts, `--check` fails when it is stale.
# Nobody types these figures, so nobody can mistype them, and the CI job that
# has XC8 is the one that proves they are current.
#
# The source is XC8's own memory summary, captured to build/memory.txt by
# mplab/Makefile. Deriving the same numbers from the hex would be a second
# opinion competing with the compiler's, and the compiler's is the one that
# matters.
# --------------------------------------------------------------------------

BLOCK_FILE = "README.md"
BLOCK_BEGIN = "<!-- checkdocs:begin build-size -->"
BLOCK_END = "<!-- checkdocs:end build-size -->"

MEMORY_TXT = ROOT / "mplab" / "build" / "memory.txt"

MEMORY_LINE = re.compile(
    r"^\s*(Program space|Data space|EEPROM space)\s+used\s+"
    r"[0-9A-Fa-f]+h\s*\(\s*(\d+)\)\s*of\s+([0-9A-Fa-f]+)h\s+bytes\s*\(\s*([\d.]+)%\)",
    re.M)


def build_stats():
    """{'Program space': (used, total, percent), ...} or None if not built."""
    if not MEMORY_TXT.is_file():
        return None
    text = MEMORY_TXT.read_text(encoding="utf-8", errors="replace")
    stats = {}
    for m in MEMORY_LINE.finditer(text):
        stats[m.group(1)] = (int(m.group(2)), int(m.group(3), 16), float(m.group(4)))
    return stats or None


def render_block(stats):
    """The markdown that goes between the markers."""
    rows = [
        ("Program space", "the firmware itself"),
        ("Data space", "RAM"),
        ("EEPROM space", "the trip accumulators, written at run time"),
    ]
    out = [
        BLOCK_BEGIN,
        "",
        "| Space | Used | Of | Share | What it holds |",
        "|---|---|---|---|---|",
    ]
    for key, what in rows:
        if key not in stats:
            continue
        used, total, pct = stats[key]
        out.append(f"| {key} | {used:,} B | {total:,} B | {pct:.1f} % | {what} |")
    out += [
        "",
        "Written by `python tools/checkdocs.py --write` out of XC8's own memory",
        "summary, and checked in CI. Do not edit by hand.",
        "",
        BLOCK_END,
    ]
    return "\n".join(out)


def current_block(text):
    """What is between the markers today, or None if the block is absent."""
    start = text.find(BLOCK_BEGIN)
    end = text.find(BLOCK_END)
    if start < 0 or end < 0 or end < start:
        return None
    return text[start:end + len(BLOCK_END)]


def strip_block(text):
    """The file with the generated block blanked, line numbers preserved.

    The block states measurable numbers on purpose, so the rules must not see
    it. Blanking rather than deleting keeps every later line reporting at the
    line it is really on.
    """
    block = current_block(text)
    if block is None:
        return text
    return text.replace(block, "\n" * block.count("\n"))


def replace_block(text, new):
    old = current_block(text)
    if old is None:
        raise SystemExit(
            f"{BLOCK_FILE} has no '{BLOCK_BEGIN}' ... '{BLOCK_END}' block to fill")
    return text.replace(old, new)


def allowed(rel, line):
    return any(
        str(rel).replace("\\", "/").endswith(suffix) and (sub in line or sub == "")
        for suffix, sub, _ in ALLOW
    )


def scan_files():
    seen = set()
    for pattern in SCAN:
        for path in sorted(ROOT.glob(pattern)):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path


# Scanning line by line does not work here and the first version of this tool
# proved it: every file in the repository is wrapped at about 78 columns, so
# "the once-a-minute EEPROM write" routinely has the frequency on one line and
# the word EEPROM on the next. Two of the eleven real cases were missed that
# way. So each file is flattened into one string with a line map, patterns run
# over the flat text, and the keyword test uses a window around the match
# rather than a single line.

CONTEXT_CHARS = 160


def flatten(text):
    """One string with runs of whitespace collapsed, plus offset -> line number."""
    flat, lines, line_no = [], [], 1
    pending_space = False
    for ch in text:
        if ch == "\n":
            line_no += 1
            pending_space = True
        elif ch.isspace():
            pending_space = True
        else:
            if pending_space and flat:
                flat.append(" ")
                lines.append(line_no)
            pending_space = False
            flat.append(ch)
            lines.append(line_no)
    return "".join(flat), lines


def line_of(line_map, offset):
    return line_map[min(offset, len(line_map) - 1)] if line_map else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if anything disagrees")
    ap.add_argument("--write", action="store_true",
                    help=f"fill the generated block in {BLOCK_FILE} from the build")
    args = ap.parse_args(argv)

    block_path = ROOT / BLOCK_FILE
    stats = build_stats()

    if args.write:
        if stats is None:
            print(f"{MEMORY_TXT.relative_to(ROOT)} is missing -- run `make -C mplab`"
                  " first; it needs XC8")
            return 1
        text = block_path.read_text(encoding="utf-8")
        updated = replace_block(text, render_block(stats))
        if updated != text:
            block_path.write_text(updated, encoding="utf-8", newline="")
            print(f"{BLOCK_FILE}: build-size block updated")
        else:
            print(f"{BLOCK_FILE}: build-size block already current")
        return 0

    problems = []
    for path in scan_files():
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")

        # The generated block is full of measurable numbers on purpose, so it
        # is removed before the rules run. It is checked separately, against
        # the build, which is a stronger test than any pattern.
        flat, line_map = flatten(strip_block(text))

        for fact in DERIVED:
            for m in fact["pattern"].finditer(flat):
                window = flat[max(0, m.start() - CONTEXT_CHARS):
                              m.end() + CONTEXT_CHARS].lower()
                if not any(word in window for word in fact["needs"]):
                    continue
                n = line_of(line_map, m.start())
                if allowed(rel, m.group(0)):
                    continue
                stated = word_to_int(m.group(1).replace(" times", ""))
                want = fact["expected"]()
                if stated is not None and stated != want:
                    problems.append(
                        (rel, n, fact["name"],
                         f"says {m.group(0).strip()!r}, source of truth says "
                         f"{fact['render'](want)!r}"))

        for rule in FORBIDDEN:
            for m in rule["pattern"].finditer(flat):
                n = line_of(line_map, m.start())
                context = flat[max(0, m.start() - CONTEXT_CHARS):
                               m.end() + CONTEXT_CHARS]
                if allowed(rel, context):
                    continue
                problems.append(
                    (rel, n, rule["name"],
                     f"quotes a measurable number {m.group(0).strip()!r} -- "
                     + rule["fix"]))

    # The generated block. Without a build there is nothing to compare against,
    # and that is not a failure: the `tools` CI job has no XC8 and must still
    # pass. The `firmware` job builds first, so that is where a stale block is
    # caught -- which is also the only place it could be.
    block_text = block_path.read_text(encoding="utf-8")
    if current_block(block_text) is None:
        problems.append((pathlib.Path(BLOCK_FILE), 0, "build-size-block",
                         f"the {BLOCK_BEGIN} block is missing"))
        block_state = "absent"
    elif stats is None:
        block_state = "not checked, no build in mplab/build"
    elif current_block(block_text) != render_block(stats):
        problems.append((pathlib.Path(BLOCK_FILE), 0, "build-size-block",
                         "stale -- run `python tools/checkdocs.py --write`"))
        block_state = "STALE"
    else:
        block_state = "current"

    for rel, n, name, msg in problems:
        where = f"{rel}:{n}" if n else str(rel)
        print(f"{where}: [{name}] {msg}")

    print()
    print(f"generated build-size block: {block_state}")
    print(f"checked {len(list(scan_files()))} files, "
          f"{len(DERIVED)} derived facts, {len(FORBIDDEN)} forbidden patterns")
    print(f"source of truth: PERSIST_INTERVAL_MS={CFG['PERSIST_INTERVAL_MS']}, "
          f"{accepted_can_ids()} accepted ids, {fixture_count()} fixtures")
    print("FAIL" if problems else "ok")

    if args.check and problems:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
