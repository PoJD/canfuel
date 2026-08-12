# Host tests for the core. Runs gcc, not XC8 — that is the whole point.
#
# The core (decode.c, compute.c, txframes.c) must not contain <xc.h>, so it
# can be compiled and tested on a PC against real logs from the car.
#
#   make             build and run everything
#   make test        the same
#   make sanitize    the same tests under ASan and UBSan (Linux/CI only)
#   make replay-host build only the tool tools/replay.py --host-build drives
#   make check-pure  verify that no hardware crept into the core
#   make check-hal   syntax-check the HAL and main.c against a stub xc.h
#   make clean
#
# While src/ has no sources, the targets pass doing nothing. That is
# deliberate — CI should be green from day one.

# make has a built-in default of "cc", so ?= would never fire. Only replace
# it when it really is that default -- CC=clang on the command line still wins.
ifeq ($(origin CC),default)
CC := gcc
endif

CFLAGS  ?= -std=c11 -Wall -Wextra -Werror -O1 -g
CFLAGS  += -I../src -I.
LDFLAGS ?=

# MSYS make hands its recipes an empty TMP, and the MSYS2 gcc then tries to
# write its temporary files into C:\WINDOWS and is refused. That used to be a
# documented papercut -- every invocation here had to be spelled
# `make TMP="$TEMP" test' -- which is both easy to forget and, being a shell
# variable, impossible for anything to allow-list.
#
# mplab/Makefile has solved this for itself since 2026-08-09 and the same two
# lines work here: `cygpath -m /tmp' is the Windows temporary directory in
# forward-slash form. cygpath exists only on MSYS and Cygwin, so this is
# self-guarding and leaves Linux, macOS and CI alone.
CYGPATH := $(shell command -v cygpath 2>/dev/null)
ifneq ($(CYGPATH),)
export TMP := $(shell cygpath -m /tmp)
endif

BUILD := build
SRCDIR := ../src

# Pure modules only. hal_*.c is never compiled on the host.
CORE_SRC := $(wildcard $(SRCDIR)/decode.c $(SRCDIR)/compute.c $(SRCDIR)/txframes.c $(SRCDIR)/persist.c)
TEST_SRC := $(wildcard test_*.c)
TESTS    := $(patsubst %.c,$(BUILD)/%,$(TEST_SRC))

# Not a test: it replays a log through the real core and prints what the
# converter would transmit, so tools/replay.py can diff Python against C.
HOST_TOOL := $(BUILD)/replay_host

.PHONY: all test sanitize replay-host check-pure check-hal clean

all: test

ifeq ($(strip $(TEST_SRC)),)

test:
	@echo "test/: no test_*.c yet — phase 1 has not started, skipping"

sanitize:
	@echo "test/: no test_*.c yet, nothing to sanitize"

replay-host:
	@echo "test/: no core yet, nothing to build"

else

test: $(TESTS) $(HOST_TOOL)
	@echo
	@for t in $(TESTS); do \
	    echo "--- $$t"; \
	    ./$$t || exit 1; \
	done
	@echo
	@echo "all host tests passed"

replay-host: $(HOST_TOOL)

# Headers are dependencies too. tt.h, logread.h and replay_core.h are
# header-only on purpose, so a change to one of them changes the behaviour of
# every binary here while leaving no .o file to go stale -- and make would
# happily report "Nothing to be done". That is not hypothetical: on
# 2026-08-11 a fix to logread.h's timestamp parsing was silently not built,
# and the stale replay_host went on disagreeing with Python for three rounds
# of debugging.
HEADERS := $(wildcard *.h) $(wildcard $(SRCDIR)/*.h)

$(BUILD)/%: %.c $(CORE_SRC) $(HEADERS) | $(BUILD)
	$(CC) $(CFLAGS) -o $@ $< $(CORE_SRC) $(LDFLAGS)

$(BUILD):
	mkdir -p $(BUILD)

# The same tests again, under the address and undefined-behaviour sanitizers.
#
# WHAT THIS IS FOR, AND WHAT IT IS NOT. It is insurance against the next
# change, not a hunt for a bug we have today: the arrays that could plausibly
# have been indexed out of range -- a 128-bucket histogram indexed by a byte
# straight off the bus, and a 30-slot ring -- were both deleted on 2026-08-12,
# and what is left is indexed by counters bounded two lines above their use.
# Signed overflow is the other half and the core is unsigned almost throughout.
#
# So it is expected to be silent. The value is that the fuzzing in
# test_props.c -- 50,000 malformed frames and 10,000 fabricated states -- runs
# through a checker rather than only through assertions somebody remembered to
# write. -fno-sanitize-recover makes the first finding fatal instead of a line
# of output nobody reads.
#
# Not part of `make test`: it roughly triples the run time, mostly in
# test_divconst's 1.2 million checks. CI runs it as its own step.
#
# IT DOES NOT RUN ON THIS DESK, and that is the toolchain rather than a fault
# here: the MSYS2 gcc on Windows ships neither libasan nor libubsan, so both
# `-fsanitize=address` and `-fsanitize=undefined` fail at the link with
# `collect2.exe: ld returned 1 exit status` and nothing more helpful. Tried
# 2026-08-12, both separately. So this target is Linux and CI only. If you
# want it locally, WSL or a container is the way; overriding SAN_CFLAGS will
# not conjure a library that is not installed.
SAN_CFLAGS ?= -fsanitize=undefined,address -fno-sanitize-recover=all \
              -fno-omit-frame-pointer
SAN_TESTS  := $(patsubst %.c,$(BUILD)/san/%,$(TEST_SRC))

sanitize: $(SAN_TESTS)
	@echo
	@for t in $(SAN_TESTS); do \
	    echo "--- $$t"; \
	    ./$$t || exit 1; \
	done
	@echo
	@echo "all sanitized tests passed"

$(BUILD)/san/%: %.c $(CORE_SRC) $(HEADERS) | $(BUILD)/san
	$(CC) $(CFLAGS) $(SAN_CFLAGS) -o $@ $< $(CORE_SRC) $(LDFLAGS)

$(BUILD)/san:
	mkdir -p $(BUILD)/san

endif

# The non-negotiable rule from CLAUDE.md, enforced mechanically. persist.c is
# in the list too: it reaches the EEPROM through function pointers precisely
# so that it stays host-testable, and that has to keep being true.
PURE_SRC := $(SRCDIR)/decode.c $(SRCDIR)/compute.c $(SRCDIR)/txframes.c $(SRCDIR)/persist.c

check-pure:
	@echo "check: the core must not touch hardware"
	@bad=$$(grep -l -E '#include[[:space:]]*<(xc|pic18)' \
	        $(PURE_SRC) 2>/dev/null); \
	if [ -n "$$bad" ]; then \
	    echo "ERROR: hardware include in a pure module:"; \
	    echo "$$bad"; \
	    exit 1; \
	fi; \
	echo "  ok"

# The other half of the same idea. check-pure keeps hardware out of the core;
# this keeps the hardware half from rotting, because XC8 is not installed here
# and is not installed in CI either.
#
# It is a syntax check and nothing more -- test/xc8stub/xc.h declares exactly
# the registers hal_*.c happens to name, so it agrees with the code by
# construction and says nothing whatever about the silicon. What it does catch
# is main.c calling the core with the wrong arguments, which is the one thing
# in these three files that a datasheet cannot tell you about.
HAL_SRC := $(SRCDIR)/hal_can.c $(SRCDIR)/hal_sys.c $(SRCDIR)/main.c

# -Wno-unknown-pragmas: pic_config.h is a wall of #pragma config, which is the
# whole point of it and which gcc has never heard of.
HAL_CFLAGS := -std=c11 -Wall -Wextra -Werror -Wno-unknown-pragmas \
              -I../src -Ixc8stub

check-hal:
	@echo "check: the HAL and main.c still compile (gcc, stub xc.h)"
	@for f in $(HAL_SRC); do \
	    echo "  $$f"; \
	    $(CC) $(HAL_CFLAGS) -fsyntax-only $$f || exit 1; \
	done
	@echo "  ok"

clean:
	rm -rf $(BUILD)
