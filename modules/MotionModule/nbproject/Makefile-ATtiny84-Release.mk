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
CND_CONF=ATtiny84-Release
CND_DISTDIR=dist
CND_BUILDDIR=build

# Include project Makefile
include Makefile

# Object Directory
OBJECTDIR=${CND_BUILDDIR}/${CND_CONF}/${CND_PLATFORM}

# Object Files
OBJECTFILES= \
	${OBJECTDIR}/_ext/742743469/Cipher.o \
	${OBJECTDIR}/_ext/742743469/CommonTasks.o \
	${OBJECTDIR}/_ext/742743469/NetworkUtils.o \
	${OBJECTDIR}/MotionDetector.o \
	${OBJECTDIR}/MotionModule.o \
	${OBJECTDIR}/MotionNetwork.o


# C Compiler Flags
CFLAGS=-mmcu=${MCU} -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -Wextra -flto -g -Os -ffunction-sections -fdata-sections

# CC Compiler Flags
CCFLAGS=-mmcu=${MCU} -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -fno-exceptions -Wextra -flto -std=gnu++11 -felide-constructors -Os -ffunction-sections -fdata-sections -mcall-prologues -DNO_CIPHER
CXXFLAGS=-mmcu=${MCU} -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -fno-exceptions -Wextra -flto -std=gnu++11 -felide-constructors -Os -ffunction-sections -fdata-sections -mcall-prologues -DNO_CIPHER

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=../arduino_cosa_111_lib/dist/ATtiny84-Release/Arduino-1.6.6-Cosa-1.1.1-Windows/libarduino_cosa_111_lib.a

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/motionmodule.exe

${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/motionmodule.exe: ../arduino_cosa_111_lib/dist/ATtiny84-Release/Arduino-1.6.6-Cosa-1.1.1-Windows/libarduino_cosa_111_lib.a

${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/motionmodule.exe: ${OBJECTFILES}
	${MKDIR} -p ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}
	${LINK.cc} -o ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/motionmodule ${OBJECTFILES} ${LDLIBSOPTIONS} -Os -Wl,--gc-sections -Wl,--relax -flto -mmcu=${MCU} -Wl,-Map,${CND_ARTIFACT_PATH_${CONF}}.map

${OBJECTDIR}/_ext/742743469/Cipher.o: ../ModuleCommons/Cipher.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/742743469
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -I../ModuleCommons -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/742743469/Cipher.o ../ModuleCommons/Cipher.cpp

${OBJECTDIR}/_ext/742743469/CommonTasks.o: ../ModuleCommons/CommonTasks.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/742743469
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -I../ModuleCommons -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/742743469/CommonTasks.o ../ModuleCommons/CommonTasks.cpp

${OBJECTDIR}/_ext/742743469/NetworkUtils.o: ../ModuleCommons/NetworkUtils.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/742743469
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -I../ModuleCommons -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/742743469/NetworkUtils.o ../ModuleCommons/NetworkUtils.cpp

${OBJECTDIR}/MotionDetector.o: MotionDetector.cpp 
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -I../ModuleCommons -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/MotionDetector.o MotionDetector.cpp

${OBJECTDIR}/MotionModule.o: MotionModule.cpp 
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -I../ModuleCommons -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/MotionModule.o MotionModule.cpp

${OBJECTDIR}/MotionNetwork.o: MotionNetwork.cpp 
	${MKDIR} -p ${OBJECTDIR}
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../Cosa/cores/cosa -I../../../Cosa/variants/${VARIANT} -I../../../Cosa/libraries/NRF24L01P -I../ModuleCommons -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/MotionNetwork.o MotionNetwork.cpp

# Subprojects
.build-subprojects:
	cd ../arduino_cosa_111_lib && ${MAKE}  -f Makefile CONF=ATtiny84-Release

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${CND_BUILDDIR}/${CND_CONF}
	${RM} ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/motionmodule.exe

# Subprojects
.clean-subprojects:
	cd ../arduino_cosa_111_lib && ${MAKE}  -f Makefile CONF=ATtiny84-Release clean

# Enable dependency checking
.dep.inc: .depcheck-impl

include .dep.inc
