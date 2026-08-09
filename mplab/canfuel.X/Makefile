# MPLAB X stub makefile. It does nothing on its own -- every target it
# defines delegates to nbproject/Makefile-impl.mk, which the IDE generates
# from nbproject/configurations.xml the first time the project is built.
#
# Those generated files are NOT committed. They carry absolute paths to
# whichever XC8 happens to be installed, and they are regenerated on every
# build anyway, so committing them would only produce a diff per machine.
# See mplab/README.md.
#
# For a build without the IDE -- which is what CI does -- use ../Makefile,
# which drives xc8-cc directly and is the authoritative recipe.
#
# NOCDDL

MKDIR=mkdir
CP=cp
CCADMIN=CCadmin
RANLIB=ranlib

build: .build-post
.build-pre:
.build-post: .build-impl

clean: .clean-post
.clean-pre:
.clean-post: .clean-impl

clobber: .clobber-post
.clobber-pre:
.clobber-post: .clobber-impl

all: .all-post
.all-pre:
.all-post: .all-impl

help: .help-post
.help-pre:
.help-post: .help-impl

include nbproject/Makefile-impl.mk
include nbproject/Makefile-variables.mk
