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
# It looks for xc8-cc on the PATH and falls back to the Windows default install
# path. Either can be overridden -- and mind that the Windows path has a space
# in it, so the quotes are not optional on the command line either:
#
#   make XC8=/opt/microchip/xc8/v4.00/bin/xc8-cc
#   make XC8="/c/Program Files/Microchip/xc8/v4.00/bin/xc8-cc"
#
# Everything the compiler needs to know about the part is in src/pic_config.h
# and in the DFP below, not here.

XC8_FOUND := $(shell command -v xc8-cc 2>/dev/null)
XC8    ?= $(if $(XC8_FOUND),$(XC8_FOUND),C:/Program Files/Microchip/xc8/v4.00/bin/xc8-cc)
DEVICE ?= 18F25K80

# The Device Family Pack, and it is not optional.
#
# XC8 v4.00 ships no device data at all: no pic/dat, no pic/include/proc, no
# docs/chips. Every register name, every #pragma config keyword and every
# linker script for this part lives in a DFP, and without -mdfp the compiler
# stops at "error: (2103) no device-support files specified".
#
# Three things about that path, all learned the hard way on 2026-08-09:
#
#  1. It points at the *xc8 subdirectory inside* the pack, not at the pack
#     root. The user's guide is explicit ("path is the relevant path to the
#     xc8 directory within the DFP"); pointing at the root gets you error 2104
#     instead, which reads like the pack is missing rather than misaddressed.
#  2. The version matters. MPLAB X v6.00 bundles PIC18F-K_DFP 1.5.114 and
#     XC8 v4.00 will not read it -- same error 2104. v4.00's own readme names
#     1.13.292 as the version it ships with, and that is the one pinned here.
#     Download it from packs.download.microchip.com; the .atpack is a zip.
#  3. **The path must be pure ASCII.** With the pack unpacked under a home
#     directory containing an accented character, device support resolves but
#     the DFP include directories are silently not added, and the build dies
#     on `xc.h: 'pic18.h' file not found'. That is why the desk default below
#     is C:/mchp_packs and not the conventional %USERPROFILE%/.mchp_packs --
#     this machine's user name is "Lubos" with a caron.
#
# CI overrides DFP with its own unpacked copy of the same version.

DFP_VERSION ?= 1.13.292
DFP         ?= C:/mchp_packs/Microchip/PIC18F-K_DFP/$(DFP_VERSION)/xc8

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
# Which ECAN mode the firmware starts in. Empty means the default in
# src/config.h, which is normal operation -- the converter. The other two are
# diagnostic builds that put nothing on the wire and are documented in
# src/hal_can.h:
#
#   make -C mplab CAN_MODE=LISTEN_ONLY     receives and decodes, never ACKs
#   make -C mplab CAN_MODE=LOOPBACK        talks to itself, no bus needed
#
# It is a build flag rather than an edit so that a diagnostic hex leaves no
# trace in the tree to be committed by accident. LED_PWR blinks slowly in
# either silent mode, so a stray one is visible rather than merely silent.
CAN_MODE ?=
CAN_MODE_FLAG := $(if $(CAN_MODE),-DCAN_START_MODE=HAL_CAN_MODE_$(CAN_MODE))

# -Wa,-a makes pic-as write the assembly listing next to the hex. It is what
# tools/cycles.py counts instructions out of, and it is the only way to know
# what the code actually costs on the part -- see docs/timing.md. It changes
# nothing about the hex and costs a second, so it is always on rather than
# being a separate target somebody would forget to run.
XC8FLAGS ?= -mcpu=$(DEVICE) -mdfp=$(DFP) -std=c99 $(OPT) -mstack=compiled -I$(SRCDIR) $(CAN_MODE_FLAG) -Wa,-a

# xc8-cc is a native Windows program even under MSYS, and it needs a temporary
# directory it can parse. MSYS make has neither TMP nor TEMP in its
# environment, so clang gets nothing and dies with "unable to create temporary
# file" and an LLVM stack dump. The obvious `make TMP="$TEMP"' from the shell
# is no better: that value has backslashes, which xc8-cc mangles into
# `directory "Temp" does not exist'.
#
# `cygpath -m /tmp' answers both at once -- it is the Windows temporary
# directory, in forward-slash form, and MSYS reports it in 8.3 short form,
# which incidentally keeps it ASCII. cygpath only exists on MSYS and Cygwin,
# so this is self-guarding and leaves Linux and macOS alone.
CYGPATH := $(shell command -v cygpath 2>/dev/null)
ifneq ($(CYGPATH),)
export TMP := $(shell cygpath -m /tmp)
endif

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
