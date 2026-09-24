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
* the frames are frozen dataclasses, and each call returns a fresh list over
  them, so a test that reorders or trims its list cannot disturb another's.

It is never imported by a tool. A command-line run parses what it is given
once, and holding the whole corpus in memory would only cost it.
"""

from __future__ import annotations

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
    frames = _cache.get(key)
    if frames is None:
        frames = _cache[key] = tuple(
            _original(path, strict=strict, fix_doubled=fix_doubled))
    return list(frames)


parse_file.__wrapped__ = _original
parse_file.__doc__ = _original.__doc__

canlog.parse_file = parse_file
for _module in list(sys.modules.values()):
    if getattr(_module, "parse_file", None) is _original:
        _module.parse_file = parse_file
