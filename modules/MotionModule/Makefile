#
#  There exist several targets which are by default empty and which can be 
#  used for execution of your targets. These targets are usually executed 
#  before and after some main targets. They are: 
#
#     .build-pre:              called before 'build' target
#     .build-post:             called after 'build' target
#     .clean-pre:              called before 'clean' target
#     .clean-post:             called after 'clean' target
#     .clobber-pre:            called before 'clobber' target
#     .clobber-post:           called after 'clobber' target
#     .all-pre:                called before 'all' target
#     .all-post:               called after 'all' target
#     .help-pre:               called before 'help' target
#     .help-post:              called after 'help' target
#
#  Targets beginning with '.' are not intended to be called on their own.
#
#  Main targets can be executed directly, and they are:
#  
#     build                    build a specific configuration
#     clean                    remove built files from a configuration
#     clobber                  remove all built files
#     all                      build all configurations
#     help                     print help mesage
#  
#  Targets .build-impl, .clean-impl, .clobber-impl, .all-impl, and
#  .help-impl are implemented in nbproject/makefile-impl.mk.
#
#  Available make variables:
#
#     CND_BASEDIR                base directory for relative paths
#     CND_DISTDIR                default top distribution directory (build artifacts)
#     CND_BUILDDIR               default top build directory (object files, ...)
#     CONF                       name of current configuration
#     CND_PLATFORM_${CONF}       platform name (current configuration)
#     CND_ARTIFACT_DIR_${CONF}   directory of build artifact (current configuration)
#     CND_ARTIFACT_NAME_${CONF}  name of build artifact (current configuration)
#     CND_ARTIFACT_PATH_${CONF}  path to build artifact (current configuration)
#     CND_PACKAGE_DIR_${CONF}    directory of package (current configuration)
#     CND_PACKAGE_NAME_${CONF}   name of package (current configuration)
#     CND_PACKAGE_PATH_${CONF}   path to package (current configuration)
#
# NOCDDL


# Environment 
MKDIR=mkdir
CP=cp
CCADMIN=CCadmin

# JFP BEGIN special variables stuff
# set variables based on each configuration
ARDUINO=166
ifeq ($(findstring UNO,${CONF}),UNO)
	VARIANT=arduino/uno
	MCU=atmega328p
	ARCH=avr5
	F_CPU=16000000L
else
ifeq ($(findstring ATmega328,${CONF}),ATmega328)
	VARIANT=arduino/atmega328p
	MCU=atmega328p
	ARCH=avr5
	F_CPU=8000000L
else
ifeq ($(findstring ATtiny84,${CONF}),ATtiny84)
	VARIANT=arduino/attinyx4
	MCU=attiny84
	ARCH=avr25
	F_CPU=8000000L
endif
endif
endif

# Set upload options
ifeq (${PROGRAMMER},)
	PROGRAMMER=UNO
endif
AVRDUDE_OPTIONS=-C ${AVRDUDE_CONF} -p ${MCU}
ifeq (${PROGRAMMER},ISP)
        AVRDUDE_OPTIONS+= -c arduinoisp 
endif
ifeq (${PROGRAMMER},SHIELD)
        AVRDUDE_OPTIONS+= -c stk500v1 -b 19200 -P com4
endif
ifeq (${PROGRAMMER},UNO)
        AVRDUDE_OPTIONS+= -c arduino -b 115200 -P com4
endif
#TODO need to add options for other programmers: leonardo, mega...
# JFP END special variables stuff

# build
build: .build-post

.build-pre:
# Add your pre 'build' code here...

.build-post: .build-impl
# Add your post 'build' code here...
	avr-objcopy -O ihex ${CND_ARTIFACT_PATH_${CONF}} ${CND_ARTIFACT_PATH_${CONF}}.hex
	avr-nm --synthetic -S -C --size-sort ${CND_ARTIFACT_PATH_${CONF}} >${CND_ARTIFACT_PATH_${CONF}}.nm.txt
	avr-objdump -m ${ARCH} -x -d -C ${CND_ARTIFACT_PATH_${CONF}} >${CND_ARTIFACT_PATH_${CONF}}.dump.txt
	avr-size -C --mcu=${MCU} ${CND_ARTIFACT_PATH_${CONF}}

# JFP BEGIN upload target
upload: .build-post
	avrdude ${AVRDUDE_OPTIONS} -Uflash:w:${CND_ARTIFACT_PATH_${CONF}}.hex:i 

setfuses: .build-post
	avrdude ${AVRDUDE_OPTIONS} -U lfuse:w:0xe2:m -U hfuse:w:0xdd:m -U efuse:w:0xff:m 
	
# JFP END upload target
	
# clean
clean: .clean-post

.clean-pre:
# Add your pre 'clean' code here...

.clean-post: .clean-impl
# Add your post 'clean' code here...


# clobber
clobber: .clobber-post

.clobber-pre:
# Add your pre 'clobber' code here...

.clobber-post: .clobber-impl
# Add your post 'clobber' code here...


# all
all: .all-post

.all-pre:
# Add your pre 'all' code here...

.all-post: .all-impl
# Add your post 'all' code here...


# build tests
build-tests: .build-tests-post

.build-tests-pre:
# Add your pre 'build-tests' code here...

.build-tests-post: .build-tests-impl
# Add your post 'build-tests' code here...


# run tests
test: .test-post

.test-pre: build-tests
# Add your pre 'test' code here...

.test-post: .test-impl
# Add your post 'test' code here...


# help
help: .help-post

.help-pre:
# Add your pre 'help' code here...

.help-post: .help-impl
# Add your post 'help' code here...



# include project implementation makefile
include nbproject/Makefile-impl.mk

# include project make variables
include nbproject/Makefile-variables.mk
