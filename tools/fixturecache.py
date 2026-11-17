"""A parse cache for the fixture corpus -- for the tests, and for nothing else.

Every test module that reads the corpus parses it again, and since the
post-repair drive joined it that is an hour of bus in one 33 MB file:
parsed once per module, the Python suite took twice as long as it did before.
Parsing a fixture is deterministic and the fixtures are never edited, so the
second parse of the same file is pure waste.

Importing this module replaces canlog.parse_file with a memoised one, both on
canlog itself and in any module that has already done `from canlog import
parse_file`. It has to be imported BEFORE a test module's own `from canlog
import ...` line, which is why it sits first in each test that reads the
corpus.

Three rules keep it honest:

* only files under test/fixtures are cached. A test that writes a temporary
  log and parses it gets the real parser every time;
* the key carries every argument and the file's modification time, so a
  different option or a changed file is a different entry;
* each call builds a fresh list of frames from a packed copy, so a test
  that reorders or trims its list cannot disturb another's.

It is never imported by a tool. A command-line run parses what it is given
once, and holding the whole corpus in memory would only cost it.
"""

from __future__ import annotations

import array
import os
import sys

import canlog

FIXTURES = os.path.normcase(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "test", "fixtures")))

_original = getattr(canlog.parse_file, "__wrapped__", canlog.parse_file)
_cache: dict[tuple, tuple] = {}


def parse_file(path, *, strict: bool = False, fix_doubled: bool = False):
    full = os.path.normcase(os.path.abspath(str(path)))
    if os.path.dirname(full) != FIXTURES:
        return _original(path, strict=strict, fix_doubled=fix_doubled)
    key = (full, strict, fix_doubled, os.path.getmtime(full))
    packed = _cache.get(key)
    if packed is None:
        frames = _original(path, strict=strict, fix_doubled=fix_doubled)
        _cache[key] = _pack(frames)
        return frames
    return _unpack(packed)


# The corpus is held packed, not as Frame objects: tens of millions of them
# took the suite past the CI runner's 16 GB (17/11/2026). Packed it is about
# 16 bytes and a few of data a frame, and rebuilding a file's frames costs
# about half of parsing it again, so the cache still pays.

def _pack(frames):
    ts = [f.ts_ms for f in frames]
    if any(t is None for t in ts):
        ts = tuple(ts)                  # format A carries no timestamps
    else:
        ts = array.array("q", ts)
    return (ts, array.array("l", (f.can_id for f in frames)),
            b"".join(f.data for f in frames),
            bytes(len(f.data) for f in frames))


def _unpack(packed):
    ts, ids, data, lens = packed
    frame = canlog.Frame
    out, at = [], 0
    for t, i, n in zip(ts, ids, lens):
        out.append(frame(t, i, data[at:at + n]))
        at += n
    return out


parse_file.__wrapped__ = _original
parse_file.__doc__ = _original.__doc__

canlog.parse_file = parse_file
for _module in list(sys.modules.values()):
    if getattr(_module, "parse_file", None) is _original:
        _module.parse_file = parse_file
