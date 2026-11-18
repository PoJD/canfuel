"""cylshare.py: the data file and the figure, without reading a capture."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cylshare  # noqa: E402


def _row(cap, kind="capture", **kw):
    r = {k: "" for k in cylshare.FIELDS}
    r.update(cap=cap, kind=kind)
    r.update({k: str(v) for k, v in kw.items()})
    return r


class TestData(unittest.TestCase):
    def test_upsert_replaces_and_keeps_the_events(self):
        rows = [_row("50", a1=1.0, event_en="old", event_cs="staré")]
        rows = cylshare.upsert(rows, {"cap": "50", "kind": "capture", "a1": 2.0})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["a1"], 2.0)
        self.assertEqual(rows[0]["event_en"], "old")

    def test_upsert_keeps_a_gas_row_apart(self):
        rows = [_row("45", kind="gas")]
        rows = cylshare.upsert(rows, {"cap": "45", "kind": "capture"})
        self.assertEqual(sorted(r["kind"] for r in rows), ["capture", "gas"])

    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.csv")
            r52 = _row("52"); r52["a1"] = 1.234
            cylshare.save([r52, _row("51")], path)
            rows = cylshare.load(path)
        self.assertEqual([r["cap"] for r in rows], ["51", "52"])
        self.assertEqual(rows[1]["a1"], "1.23")
        self.assertEqual(rows[0]["b3"], "")


class TestRender(unittest.TestCase):
    def rows(self):
        return [_row("49", a1=1, a3_floor=-9, a3_swell=-24, a4=2, a2=-2,
                     b1=2.8, b3=3.0, b4=2.6, b2=2.4, event_en="12/11 canister",
                     event_cs="12/11 nádobka"),
                _row("50", a1=0, a3_swell=-25, a4=-1, a2=3,
                     b1=2.8, b3=3.6, b4=2.9, b2=2.3),
                _row("45", kind="gas", a1=1, a3=-17, a4=-3, a2=2,
                     b1=1.2, b3=2.0, b4=1.5, b2=0.6)]

    def test_both_languages_draw_every_capture_and_the_event(self):
        for lang, ev in (("en", "12/11 canister"), ("cs", "12/11 nádobka")):
            svg = cylshare.render(self.rows(), lang)
            self.assertTrue(svg.startswith("<svg") and svg.rstrip().endswith("</svg>"))
            self.assertIn(ev, svg)
            self.assertIn(">49</text>", svg)
            self.assertIn(">50</text>", svg)
            self.assertNotIn(">45</text>", svg)   # the gas is drawn apart

    def test_a_missing_floor_breaks_the_line_not_the_figure(self):
        svg = cylshare.render(self.rows(), "en")
        # 3's floor exists on one capture only: a dot, not a line
        self.assertIn('r="2.5" fill="#c0503a"', svg)
        self.assertIn('stroke-dasharray="5,3"', svg)


if __name__ == "__main__":
    unittest.main()
