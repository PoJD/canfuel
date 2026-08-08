# Host tests for the core. Runs gcc, not XC8 — that is the whole point.
#
# The core (decode.c, compute.c, txframes.c) must not contain <xc.h>, so it
# can be compiled and tested on a PC against real logs from the car.
#
#   make            build and run
#   make check-pure verify that no hardware crept into the core
#   make clean
#
# While src/ has no sources, the targets pass doing nothing. That is
# deliberate — CI should be green from day one.

CC      ?= gcc
CFLAGS  ?= -std=c11 -Wall -Wextra -Werror -O1 -g
CFLAGS  += -I../src -I.
LDFLAGS ?=

BUILD := build
SRCDIR := ../src

# Pure modules only. hal_*.c is never compiled on the host.
CORE_SRC := $(wildcard $(SRCDIR)/decode.c $(SRCDIR)/compute.c $(SRCDIR)/txframes.c $(SRCDIR)/persist.c)
TEST_SRC := $(wildcard test_*.c)
TESTS    := $(patsubst %.c,$(BUILD)/%,$(TEST_SRC))

.PHONY: all test check-pure clean

all: test

ifeq ($(strip $(TEST_SRC)),)

test:
	@echo "test/: no test_*.c yet — phase 1 has not started, skipping"

else

test: $(TESTS)
	@echo
	@for t in $(TESTS); do \
	    echo "--- $$t"; \
	    ./$$t || exit 1; \
	done
	@echo
	@echo "all host tests passed"

$(BUILD)/%: %.c $(CORE_SRC) | $(BUILD)
	$(CC) $(CFLAGS) -o $@ $< $(CORE_SRC) $(LDFLAGS)

$(BUILD):
	mkdir -p $(BUILD)

endif

# The non-negotiable rule from CLAUDE.md, enforced mechanically.
check-pure:
	@echo "check: the core must not touch hardware"
	@bad=$$(grep -l -E '#include[[:space:]]*<(xc|pic18)' \
	        $(SRCDIR)/decode.c $(SRCDIR)/compute.c $(SRCDIR)/txframes.c 2>/dev/null); \
	if [ -n "$$bad" ]; then \
	    echo "ERROR: hardware include in a pure module:"; \
	    echo "$$bad"; \
	    exit 1; \
	fi; \
	echo "  ok"

clean:
	rm -rf $(BUILD)
