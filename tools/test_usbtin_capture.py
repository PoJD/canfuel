#!/usr/bin/env python3
"""Tests for the part of usbtin_capture.py that does not need an adapter.

pyserial is this project's only third-party dependency and CI installs
nothing, which is why the module is written to stay importable without it.
record() is the piece worth testing: it is where the frames become the file,
and where Ctrl-C is turned from a traceback into a supported ending.
"""

from __future__ import annotations

import io
import time
import unittest

from usbtin_capture import CR, record


class FakeSerial:
    """Hands out canned chunks, then does whatever `then` says."""

    def __init__(self, chunks, then=None):
        self.chunks = list(chunks)
        self.then = then

    def read(self, _n):
        if self.chunks:
            return self.chunks.pop(0)
        if self.then is not None:
            raise self.then
        return b""


def frames(*lines):
    return CR.join(l.encode("ascii") for l in lines) + CR


class Record(unittest.TestCase):
    def test_whole_lines_become_file_lines(self):
        ser = FakeSerial([frames("t1A08004001", "t4208010000")])
        fh = io.StringIO()
        n, stopped = record(ser, fh, time.monotonic() + 0.2)
        self.assertEqual(n, 2)
        self.assertFalse(stopped)
        self.assertEqual(fh.getvalue(), "t1A08004001\nt4208010000\n")

    def test_a_line_split_across_two_reads_is_rejoined(self):
        ser = FakeSerial([b"t1A080", b"04001" + CR])
        fh = io.StringIO()
        n, _ = record(ser, fh, time.monotonic() + 0.2)
        self.assertEqual(fh.getvalue(), "t1A08004001\n")
        self.assertEqual(n, 1)

    def test_a_partial_line_at_the_deadline_is_not_written(self):
        """Half a frame is not a frame; canlog would reject it."""
        ser = FakeSerial([b"t1A080"])
        fh = io.StringIO()
        n, _ = record(ser, fh, time.monotonic() + 0.1)
        self.assertEqual(n, 0)
        self.assertEqual(fh.getvalue(), "")

    def test_bel_and_blank_lines_are_dropped(self):
        ser = FakeSerial([frames("\x07", "", "t1A08004001")])
        fh = io.StringIO()
        n, _ = record(ser, fh, time.monotonic() + 0.2)
        self.assertEqual(n, 1)

    def test_ctrl_c_ends_the_capture_and_keeps_what_was_read(self):
        """docs/next-drive.md ends the capture by hand; that is not an abort."""
        ser = FakeSerial([frames("t1A08004001", "t4208010000")],
                         then=KeyboardInterrupt)
        fh = io.StringIO()
        n, stopped = record(ser, fh, time.monotonic() + 30.0)
        self.assertTrue(stopped)
        self.assertEqual(n, 2, "frames read before Ctrl-C must survive it")
        self.assertEqual(fh.getvalue(), "t1A08004001\nt4208010000\n")

    def test_progress_is_called_and_is_optional(self):
        seen = []
        ser = FakeSerial([frames("t1A08004001")])
        record(ser, io.StringIO(), time.monotonic() + 0.2,
               lambda lines, left: seen.append(lines))
        self.assertTrue(seen)
        record(ser, io.StringIO(), time.monotonic() + 0.05)   # no progress: fine


if __name__ == "__main__":
    unittest.main()
