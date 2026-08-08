# Hostové testy jádra. Běží gcc, ne XC8 — o to tu jde.
#
# Jádro (decode.c, compute.c, txframes.c) nesmí obsahovat <xc.h>, takže
# se dá přeložit a otestovat na počítači proti reálným logům z auta.
#
#   make            přeloží a spustí
#   make check-pure ověří, že se do jádra nevloudil hardware
#   make clean
#
# Dokud v src/ nejsou zdrojáky, cíle projdou naprázdno. To je záměr —
# CI má být zelená od prvního dne.

CC      ?= gcc
CFLAGS  ?= -std=c11 -Wall -Wextra -Werror -O1 -g
CFLAGS  += -I../src -I.
LDFLAGS ?=

BUILD := build
SRCDIR := ../src

# Jen čisté moduly. hal_*.c se na hostu nepřekládá.
CORE_SRC := $(wildcard $(SRCDIR)/decode.c $(SRCDIR)/compute.c $(SRCDIR)/txframes.c $(SRCDIR)/persist.c)
TEST_SRC := $(wildcard test_*.c)
TESTS    := $(patsubst %.c,$(BUILD)/%,$(TEST_SRC))

.PHONY: all test check-pure clean

all: test

ifeq ($(strip $(TEST_SRC)),)

test:
	@echo "test/: zatím žádné test_*.c — fáze 1 ještě nezačala, přeskakuji"

else

test: $(TESTS)
	@echo
	@for t in $(TESTS); do \
	    echo "--- $$t"; \
	    ./$$t || exit 1; \
	done
	@echo
	@echo "všechny hostové testy prošly"

$(BUILD)/%: %.c $(CORE_SRC) | $(BUILD)
	$(CC) $(CFLAGS) -o $@ $< $(CORE_SRC) $(LDFLAGS)

$(BUILD):
	mkdir -p $(BUILD)

endif

# Nepřekročitelné pravidlo z CLAUDE.md, ohlídané strojově.
check-pure:
	@echo "kontrola: jádro nesmí sáhnout na hardware"
	@bad=$$(grep -l -E '#include[[:space:]]*<(xc|pic18)' \
	        $(SRCDIR)/decode.c $(SRCDIR)/compute.c $(SRCDIR)/txframes.c 2>/dev/null); \
	if [ -n "$$bad" ]; then \
	    echo "CHYBA: hardwarový include v čistém modulu:"; \
	    echo "$$bad"; \
	    exit 1; \
	fi; \
	echo "  ok"

clean:
	rm -rf $(BUILD)
