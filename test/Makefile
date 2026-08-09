# Host tests for the core. Runs gcc, not XC8 — that is the whole point.
#
# The core (decode.c, compute.c, txframes.c) must not contain <xc.h>, so it
# can be compiled and tested on a PC against real logs from the car.
#
#   make             build and run everything
#   make test        the same
#   make replay-host build only the tool tools/replay.py --host-build drives
#   make check-pure  verify that no hardware crept into the core
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

BUILD := build
SRCDIR := ../src

# Pure modules only. hal_*.c is never compiled on the host.
CORE_SRC := $(wildcard $(SRCDIR)/decode.c $(SRCDIR)/compute.c $(SRCDIR)/txframes.c $(SRCDIR)/persist.c)
TEST_SRC := $(wildcard test_*.c)
TESTS    := $(patsubst %.c,$(BUILD)/%,$(TEST_SRC))

# Not a test: it replays a log through the real core and prints what the
# converter would transmit, so tools/replay.py can diff Python against C.
HOST_TOOL := $(BUILD)/replay_host

.PHONY: all test replay-host check-pure clean

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

$(BUILD)/%: %.c $(CORE_SRC) | $(BUILD)
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

clean:
	rm -rf $(BUILD)
