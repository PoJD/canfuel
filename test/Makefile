# Host tests for the core. Runs gcc, not XC8 — that is the whole point.
#
# The core (decode.c, compute.c, txframes.c) must not contain <xc.h>, so it
# can be compiled and tested on a PC against real logs from the car.
#
#   make             build and run everything
#   make test        the same
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

.PHONY: all test replay-host check-pure check-hal clean

all: test

ifeq ($(strip $(TEST_SRC)),)

test:
	@echo "test/: no test_*.c yet — phase 1 has not started, skipping"

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
