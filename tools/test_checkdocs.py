#!/usr/bin/env python3
"""Tests for checkdocs.py -- that the gate still fails when it should.

Running them:
    python -m unittest discover -s tools -p 'test_*.py' -v
    python tools/test_checkdocs.py

A checker with no test of its own has one failure mode worse than all the
others: a regex stops matching, every run goes green, and nobody notices for
months -- which is exactly the kind of silent drift the tool exists to stop.
So these tests do not check that the repository is clean today. They break the
inputs on purpose and require the tool to complain.

The two cases below are the two real bugs from 2026-08-12, reproduced:
PERSIST_INTERVAL_MS moving without the prose following it, and a measurable
count written into a document.
"""

from __future__ import annotations

import unittest

import checkdocs


def scan(text, name="sample.md"):
    """Run every rule over one string, the way main() runs it over a file."""
    flat, line_map = checkdocs.flatten(text)
    hits = []

    for fact in checkdocs.DERIVED:
        for m in fact["pattern"].finditer(flat):
            window = flat[max(0, m.start() - checkdocs.CONTEXT_CHARS):
                          m.end() + checkdocs.CONTEXT_CHARS].lower()
            if not any(word in window for word in fact["needs"]):
                continue
            stated = checkdocs.word_to_int(m.group(1).replace(" times", ""))
            if stated is not None and stated != fact["expected"]():
                hits.append((fact["name"], m.group(0)))

    for rule in checkdocs.FORBIDDEN:
        for m in rule["pattern"].finditer(flat):
            hits.append((rule["name"], m.group(0)))

    return hits


def names(hits):
    return {name for name, _ in hits}


class DerivedFacts(unittest.TestCase):
    """The frequency in the prose has to track PERSIST_INTERVAL_MS."""

    def test_correct_frequency_passes(self):
        want = 60_000 // checkdocs.CFG["PERSIST_INTERVAL_MS"]
        phrase = {1: "once", 2: "twice"}.get(want, f"{checkdocs.WORD_FOR[want]} times")
        text = f"The EEPROM write blocks for 48 ms, {phrase} a minute."
        self.assertEqual(names(scan(text)), set())

    def test_stale_frequency_is_caught(self):
        text = "The EEPROM write blocks for about 48 ms, once a minute."
        self.assertIn("eeprom-writes-per-minute", names(scan(text)))

    def test_caught_across_a_line_wrap(self):
        """The bug that made the first version of the tool nearly useless.

        Everything here is wrapped at about 78 columns, so the keyword and the
        figure routinely land on different lines. Scanning line by line missed
        ten of the fourteen places that state this frequency.
        """
        text = ("The one place frames are really lost is the EEPROM\n"
                "write, which happens once a minute and blocks for 48 ms.")
        self.assertIn("eeprom-writes-per-minute", names(scan(text)))

    def test_unrelated_sentence_is_left_alone(self):
        """`needs` keeps the pattern off text that is not about persistence."""
        text = "The driver checks the mirrors about once a minute."
        self.assertEqual(names(scan(text)), set())

    def test_identifier_count_tracks_config(self):
        stale = checkdocs.accepted_can_ids() + 1
        text = f"the {checkdocs.WORD_FOR[stale]} identifiers we accept arrive fast"
        self.assertIn("accepted-identifiers", names(scan(text)))

    def test_identifier_count_matches_config(self):
        now = checkdocs.accepted_can_ids()
        text = f"the {checkdocs.WORD_FOR[now]} identifiers we accept arrive fast"
        self.assertEqual(names(scan(text)), set())


class ForbiddenNumbers(unittest.TestCase):
    """Counts a command prints must not be written down."""

    def test_check_counts(self):
        self.assertIn("test-counts", names(scan("the suite runs 350+ checks")))
        self.assertIn("test-counts", names(scan("80+ tests, all green")))

    def test_binary_counts(self):
        self.assertIn("binary-counts",
                      names(scan("250 checks across seven test binaries")))

    def test_build_size(self):
        self.assertIn("build-size",
                      names(scan("it uses 11,594 bytes of 32,768 of program space")))
        self.assertIn("build-size",
                      names(scan("and 564 bytes of 3,649 of RAM")))

    def test_prose_without_numbers_passes(self):
        text = ("`make -C test test` runs the whole suite and prints what it "
                "checked; it fits with room to spare.")
        self.assertEqual(names(scan(text)), set())


class SourceOfTruth(unittest.TestCase):
    """The tool must actually be reading config.h, not a copy of it."""

    def test_constants_are_parsed(self):
        self.assertIn("PERSIST_INTERVAL_MS", checkdocs.CFG)
        self.assertGreater(checkdocs.CFG["PERSIST_INTERVAL_MS"], 0)

    def test_can_ids_exclude_the_transmitted_ones(self):
        n = checkdocs.accepted_can_ids()
        self.assertEqual(n, sum(1 for k in checkdocs.CFG
                                if k.startswith("CAN_ID_")
                                and not k.startswith("CAN_ID_TX_")))
        self.assertNotIn("CAN_ID_TX_FUEL", [
            k for k in checkdocs.CFG
            if k.startswith("CAN_ID_") and not k.startswith("CAN_ID_TX_")])

    def test_word_and_digit_forms_both_parse(self):
        self.assertEqual(checkdocs.word_to_int("three"), 3)
        self.assertEqual(checkdocs.word_to_int("17"), 17)
        self.assertEqual(checkdocs.word_to_int("1,024"), 1024)
        self.assertIsNone(checkdocs.word_to_int("several"))


class Flattening(unittest.TestCase):
    """Offsets in the flattened text must map back to the right line."""

    def test_line_numbers_survive_flattening(self):
        flat, line_map = checkdocs.flatten("alpha\nbravo\ncharlie\n")
        self.assertEqual(flat, "alpha bravo charlie")
        self.assertEqual(checkdocs.line_of(line_map, flat.index("alpha")), 1)
        self.assertEqual(checkdocs.line_of(line_map, flat.index("bravo")), 2)
        self.assertEqual(checkdocs.line_of(line_map, flat.index("charlie")), 3)

    def test_runs_of_whitespace_collapse(self):
        flat, _ = checkdocs.flatten(" a  \n\n\t b \n")
        self.assertEqual(flat, "a b")


SUMMARY = """
18F25K80 Memory Summary:
    Program space        used  32BAh ( 12986) of  8000h bytes   ( 39.6%)
    Data space           used   153h (   339) of   E41h bytes   (  9.3%)
    Configuration bits   used     7h (     7) of     7h words   (100.0%)
    EEPROM space         used     0h (     0) of   400h bytes   (  0.0%)
    ID Location space    used     0h (     0) of     8h bytes   (  0.0%)
"""


class GeneratedBlock(unittest.TestCase):
    """The size figures in README.md are written by the tool, never typed.

    Parsing XC8's summary is the one place this tool depends on somebody
    else's output format. If v4.00 ever changes it these tests go red, which
    is the point -- the alternative is a block that silently stops updating.
    """

    def parse(self, text):
        return {m.group(1): (int(m.group(2)), int(m.group(3), 16), float(m.group(4)))
                for m in checkdocs.MEMORY_LINE.finditer(text)}

    def test_summary_parses(self):
        stats = self.parse(SUMMARY)
        self.assertEqual(stats["Program space"], (12986, 0x8000, 39.6))
        self.assertEqual(stats["Data space"], (339, 0xE41, 9.3))
        self.assertEqual(stats["EEPROM space"], (0, 0x400, 0.0))

    def test_configuration_and_id_rows_are_ignored(self):
        """Config bits are always 100 % and ID space is always empty."""
        self.assertNotIn("Configuration bits", self.parse(SUMMARY))
        self.assertNotIn("ID Location space", self.parse(SUMMARY))

    def test_totals_come_out_as_the_datasheet_has_them(self):
        stats = self.parse(SUMMARY)
        self.assertEqual(stats["Program space"][1], 32768)
        self.assertEqual(stats["EEPROM space"][1], 1024)

    def test_rendered_block_is_delimited_and_carries_the_numbers(self):
        block = checkdocs.render_block(self.parse(SUMMARY))
        self.assertTrue(block.startswith(checkdocs.BLOCK_BEGIN))
        self.assertTrue(block.endswith(checkdocs.BLOCK_END))
        self.assertIn("12,986 B", block)
        self.assertIn("39.6 %", block)

    def test_replacing_the_block_leaves_the_rest_alone(self):
        doc = (f"before\n{checkdocs.BLOCK_BEGIN}\nstale\n"
               f"{checkdocs.BLOCK_END}\nafter\n")
        out = checkdocs.replace_block(doc, checkdocs.render_block(self.parse(SUMMARY)))
        self.assertTrue(out.startswith("before\n"))
        self.assertTrue(out.endswith("after\n"))
        self.assertNotIn("stale", out)

    def test_a_document_without_markers_is_an_error(self):
        with self.assertRaises(SystemExit):
            checkdocs.replace_block("no markers here", "x")

    def test_the_block_is_exempt_from_the_forbidden_patterns(self):
        """Measurable numbers inside the markers are fine; outside they are not."""
        offending = "it uses 11,594 bytes of 32,768 of program space"
        self.assertIn("build-size", names(scan(offending)),
                      "sanity: that sentence really does trip a rule")

        inside = (f"intro\n{checkdocs.BLOCK_BEGIN}\n{offending}\n"
                  f"{checkdocs.BLOCK_END}\noutro\n")
        self.assertEqual(names(scan(checkdocs.strip_block(inside))), set())

        outside = f"intro\n{offending}\n{checkdocs.BLOCK_BEGIN}\n\n{checkdocs.BLOCK_END}\n"
        self.assertIn("build-size", names(scan(checkdocs.strip_block(outside))))

    def test_stripping_preserves_line_numbers(self):
        doc = (f"one\n{checkdocs.BLOCK_BEGIN}\na\nb\n{checkdocs.BLOCK_END}\nlast\n")
        stripped = checkdocs.strip_block(doc)
        self.assertEqual(len(stripped.splitlines()), len(doc.splitlines()))
        self.assertEqual(stripped.splitlines()[-1], "last")

    def test_readme_block_matches_the_build_when_there_is_one(self):
        stats = checkdocs.build_stats()
        if stats is None:
            self.skipTest("no mplab/build/memory.txt; needs XC8")
        readme = (checkdocs.ROOT / checkdocs.BLOCK_FILE).read_text(encoding="utf-8")
        self.assertEqual(checkdocs.current_block(readme),
                         checkdocs.render_block(stats))


class RepositoryIsClean(unittest.TestCase):
    """Belt and braces: the repository itself passes right now."""

    def test_no_problems_in_the_tree(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = checkdocs.main(["--check"])
        self.assertEqual(rc, 0, buf.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
