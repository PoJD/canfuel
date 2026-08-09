# The device build, without the IDE.
#
# This is the authoritative recipe: it is what CI runs and it is what the
# canfuel.X project is configured to reproduce. MPLAB X is a convenient editor
# and the only way to drive a PICkit, but a build that only exists inside an
# IDE is a build nobody else can check.
#
#   make            build build/canfuel.hex
#   make clean
#
# It looks for xc8-cc on the PATH. If it is not there, point at it instead of
# editing anything -- and mind that the Windows default has a space in it, so
# the quotes are not optional on the command line either:
#
#   make XC8=/opt/microchip/xc8/v4.00/bin/xc8-cc
#   make XC8="/c/Program Files/Microchip/xc8/v4.00/bin/xc8-cc"
#
# XC8 is not installed on the development machine this was written on, so the
# first person to run this should expect to fix something. Everything the
# compiler needs to know about the part is in src/pic_config.h, not here.

XC8    ?= xc8-cc
DEVICE ?= 18F25K80

SRCDIR := ../src
BUILD  := build
TARGET := $(BUILD)/canfuel

# main.c first, then the two hardware modules, then the pure core. The order
# is cosmetic -- it is the order the code is meant to be read in.
SRC := \
	$(SRCDIR)/main.c \
	$(SRCDIR)/hal_can.c \
	$(SRCDIR)/hal_sys.c \
	$(SRCDIR)/decode.c \
	$(SRCDIR)/compute.c \
	$(SRCDIR)/txframes.c \
	$(SRCDIR)/persist.c

# -O2: the loop is nowhere near tight, but the core does 32-bit arithmetic on
# an 8-bit machine and there is no reason to make it worse. Overridable
# because XC8's free licence restricts the higher levels -- `make OPT=-O0'
# builds with nothing switched on, which is what CI does.
OPT ?= -O2

# -mstack=compiled: the PIC18 hardware stack is 31 levels of return addresses
# and nothing else, so locals live in a compiled stack. Nothing here recurses.
XC8FLAGS ?= -mcpu=$(DEVICE) -std=c99 $(OPT) -mstack=compiled -I$(SRCDIR)

.PHONY: all clean

all: $(TARGET).hex

# "$(XC8)" is quoted because the default install path on Windows is
# C:\Program Files\Microchip\xc8\..., and an unquoted space there would make
# the recipe try to run a program called "C:/Program".
$(TARGET).hex: $(SRC) | $(BUILD)
	"$(XC8)" $(XC8FLAGS) -o $@ $(SRC)

$(BUILD):
	mkdir -p $(BUILD)

clean:
	rm -rf $(BUILD)
