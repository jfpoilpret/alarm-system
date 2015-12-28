#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Environment
MKDIR=mkdir
CP=cp
GREP=grep
NM=nm
CCADMIN=CCadmin
RANLIB=ranlib
CC=avr-gcc
CCC=avr-g++
CXX=avr-g++
FC=gfortran
AS=avr-as

# Macros
CND_PLATFORM=Arduino-1.6.6-Cosa-1.1.1-Windows
CND_DLIB_EXT=dll
CND_CONF=ATmega328-Release
CND_DISTDIR=dist
CND_BUILDDIR=build

# Include project Makefile
include Makefile

# Object Directory
OBJECTDIR=${CND_BUILDDIR}/${CND_CONF}/${CND_PLATFORM}

# Object Files
OBJECTFILES= \
	${OBJECTDIR}/ActivationModule.o \
	${OBJECTDIR}/ActivationNetwork.o \
	${OBJECTDIR}/Cipher.o \
	${OBJECTDIR}/NetworkUtils.o


# C Compiler Flags
CFLAGS=-mmcu=${MCU} -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -Wextra -flto -g -Os -ffunction-sections -fdata-sections

# CC Compiler Flags
CCFLAGS=-mmcu=${MCU} -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -fno-exceptions -Wextra -flto -std=gnu++11 -felide-constructors -g -Os -ffunction-sections -fdata-sections
CXXFLAGS=-mmcu=${MCU} -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -fno-exceptions -Wextra -flto -std=gnu++11 -felide-constructors -g -Os -ffunction-sections -fdata-sections

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=../arduino_cosa_111_lib/dist/ATmega328-Release/Arduino-1.6.6-Cosa-1.1.1-Windows/libarduino_cosa_111_lib.a

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/activationmodule.exe

${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/activationmodule.exe: ../arduino_cosa_111_lib/dist/ATmega328-Release/Arduino-1.6.6-Cosa-1.1.1-Windows/libarduino_cosa_111_lib.a

${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/activationmodule.exe: ${OBJECTFILES}
	${MKDIR} -p ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}
	${LINK.cc} -o ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/activationmodule ${OBJECTFILES} ${LDLIBSOPTIONS} -Os -Wl,--gc-sections -Wl,-relax -flto -mmcu=${MCU} -lm

${OBJECTDIR}/ActivationModule.o: ActivationModule.cpp 
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/ActivationModule.o ActivationModule.cpp

${OBJECTDIR}/ActivationNetwork.o: ActivationNetwork.cpp 
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/ActivationNetwork.o ActivationNetwork.cpp

${OBJECTDIR}/Cipher.o: Cipher.cpp 
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/Cipher.o Cipher.cpp

${OBJECTDIR}/NetworkUtils.o: NetworkUtils.cpp 
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/NetworkUtils.o NetworkUtils.cpp

# Subprojects
.build-subprojects:
	cd ../arduino_cosa_111_lib && ${MAKE}  -f Makefile CONF=ATmega328-Release

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${CND_BUILDDIR}/${CND_CONF}
	${RM} ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/activationmodule.exe

# Subprojects
.clean-subprojects:
	cd ../arduino_cosa_111_lib && ${MAKE}  -f Makefile CONF=ATmega328-Release clean

# Enable dependency checking
.dep.inc: .depcheck-impl

include .dep.inc
