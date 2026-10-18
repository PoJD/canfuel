"""vcds_log.py's read-only guard and its file naming; no VCDS needed."""

import unittest

import vcds_log as v


class Guard(unittest.TestCase):
    def setUp(self):
        self.vcds = v.Vcds.__new__(v.Vcds)   # no VCDS started

    def test_allowed_and_forbidden_do_not_overlap(self):
        self.assertFalse(v.ALLOWED & v.FORBIDDEN)

    def test_clearing_the_fault_memory_is_refused(self):
        with self.assertRaises(RuntimeError):
            self.vcds.click("blocks", None, 1293)

    def test_basic_settings_are_refused(self):
        for where, ctrl in (("blocks", 1216), ("log", 1260), ("funcs", 1104)):
            with self.assertRaises(RuntimeError):
                self.vcds.click(where, None, ctrl)

    def test_anything_unlisted_is_refused(self):
        with self.assertRaises(RuntimeError):
            self.vcds.click("funcs", None, 1095)   # fault memory: read by hand


class Parts(unittest.TestCase):
    def test_numbering(self):
        self.assertEqual(v.part_path("a/x.CSV", 1), "a/x.CSV")
        self.assertEqual(v.part_path("a/x.CSV", 3), "a/x-3.CSV")


if __name__ == "__main__":
    unittest.main()
