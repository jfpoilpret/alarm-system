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
RANLIB=avr-ranlib
CC=avr-gcc
CCC=avr-g++
CXX=avr-g++
FC=gfortran
AS=avr-as
AR=avr-ar

# Macros
CND_PLATFORM=Arduino-1.6.6-Windows
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
	${OBJECTDIR}/_ext/1138186933/Programmer.o \
	${OBJECTDIR}/_ext/1138186933/STK500.o \
	${OBJECTDIR}/_ext/345725447/Activity.o \
	${OBJECTDIR}/_ext/345725447/Alarm.o \
	${OBJECTDIR}/_ext/345725447/AnalogComparator.o \
	${OBJECTDIR}/_ext/345725447/AnalogPin.o \
	${OBJECTDIR}/_ext/345725447/AnalogPins.o \
	${OBJECTDIR}/_ext/345725447/Board.o \
	${OBJECTDIR}/_ext/345725447/Button.o \
	${OBJECTDIR}/_ext/345725447/Canvas.o \
	${OBJECTDIR}/_ext/1828893367/ST7735.o \
	${OBJECTDIR}/_ext/1572886093/Textbox.o \
	${OBJECTDIR}/_ext/190218594/FixedNums8x16.o \
	${OBJECTDIR}/_ext/190218594/Segment32x50.o \
	${OBJECTDIR}/_ext/190218594/System5x7.o \
	${OBJECTDIR}/_ext/971513216/UTFTFont.o \
	${OBJECTDIR}/_ext/964078797/Base64.o \
	${OBJECTDIR}/_ext/964078797/RC4.o \
	${OBJECTDIR}/_ext/927333040/DHT.o \
	${OBJECTDIR}/_ext/927333040/DS1302.o \
	${OBJECTDIR}/_ext/927333040/HCSR04.o \
	${OBJECTDIR}/_ext/927333040/IR.o \
	${OBJECTDIR}/_ext/927333040/NEXA.o \
	${OBJECTDIR}/_ext/927333040/TCS230.o \
	${OBJECTDIR}/_ext/345725447/EEPROM.o \
	${OBJECTDIR}/_ext/345725447/Event.o \
	${OBJECTDIR}/_ext/345725447/ExternalInterrupt.o \
	${OBJECTDIR}/_ext/175263189/CFFS.o \
	${OBJECTDIR}/_ext/175263189/FAT16.o \
	${OBJECTDIR}/_ext/345725447/INET.o \
	${OBJECTDIR}/_ext/924286876/DHCP.o \
	${OBJECTDIR}/_ext/924286876/DNS.o \
	${OBJECTDIR}/_ext/924286876/HTTP.o \
	${OBJECTDIR}/_ext/924286876/NTP.o \
	${OBJECTDIR}/_ext/924286876/SNMP.o \
	${OBJECTDIR}/_ext/924286876/Telnet.o \
	${OBJECTDIR}/_ext/345725447/IOStream.o \
	${OBJECTDIR}/_ext/1098285609/CDC.o \
	${OBJECTDIR}/_ext/1098285609/RS485.o \
	${OBJECTDIR}/_ext/1098285609/UART.o \
	${OBJECTDIR}/_ext/345725447/Keypad.o \
	${OBJECTDIR}/_ext/1462915086/HD44780.o \
	${OBJECTDIR}/_ext/1462915086/HD44780_IO_DFRobot.o \
	${OBJECTDIR}/_ext/1462915086/HD44780_IO_ERM1602_5.o \
	${OBJECTDIR}/_ext/1462915086/HD44780_IO_MJKDZ.o \
	${OBJECTDIR}/_ext/1462915086/HD44780_IO_Port4b.o \
	${OBJECTDIR}/_ext/1462915086/HD44780_IO_SR3W.o \
	${OBJECTDIR}/_ext/1462915086/HD44780_IO_SR3WSPI.o \
	${OBJECTDIR}/_ext/1462915086/HD44780_IO_SR4W.o \
	${OBJECTDIR}/_ext/1462915086/HD44780_IO_SainSmart.o \
	${OBJECTDIR}/_ext/1462915086/MAX72XX.o \
	${OBJECTDIR}/_ext/1462915086/PCD8544.o \
	${OBJECTDIR}/_ext/1462915086/ST7565.o \
	${OBJECTDIR}/_ext/1462915086/ST7920.o \
	${OBJECTDIR}/_ext/1462915086/VLCD.o \
	${OBJECTDIR}/_ext/345725447/Linkage.o \
	${OBJECTDIR}/_ext/345725447/Menu.o \
	${OBJECTDIR}/_ext/638459326/Actor.o \
	${OBJECTDIR}/_ext/638459326/Semaphore.o \
	${OBJECTDIR}/_ext/638459326/Thread.o \
	${OBJECTDIR}/_ext/345725447/OWI.o \
	${OBJECTDIR}/_ext/577277886/DS18B20.o \
	${OBJECTDIR}/_ext/345725447/OutputPin.o \
	${OBJECTDIR}/_ext/345725447/PWMPin.o \
	${OBJECTDIR}/_ext/345725447/Pin.o \
	${OBJECTDIR}/_ext/345725447/PinChangeInterrupt.o \
	${OBJECTDIR}/_ext/345725447/Power.o \
	${OBJECTDIR}/_ext/345725447/ProtoThread.o \
	${OBJECTDIR}/_ext/345725447/RTC.o \
	${OBJECTDIR}/_ext/345725447/Registry.o \
	${OBJECTDIR}/_ext/345725447/Rotary.o \
	${OBJECTDIR}/_ext/345725447/SPI.o \
	${OBJECTDIR}/_ext/441496781/S25FL127S.o \
	${OBJECTDIR}/_ext/441496781/SD.o \
	${OBJECTDIR}/_ext/542241094/Ciao.o \
	${OBJECTDIR}/_ext/542241094/Fai.o \
	${OBJECTDIR}/_ext/675975705/analog_pin_t.o \
	${OBJECTDIR}/_ext/675975705/digital_pin_t.o \
	${OBJECTDIR}/_ext/675975705/digital_pins_t.o \
	${OBJECTDIR}/_ext/675975705/event_t.o \
	${OBJECTDIR}/_ext/675975705/sample_request_t.o \
	${OBJECTDIR}/_ext/675975705/set_mode_t.o \
	${OBJECTDIR}/_ext/542241094/ProtocolBuffer.o \
	${OBJECTDIR}/_ext/345725447/Servo.o \
	${OBJECTDIR}/_ext/345725447/Shell.o \
	${OBJECTDIR}/_ext/345725447/Socket.o \
	${OBJECTDIR}/_ext/1797159876/W5100.o \
	${OBJECTDIR}/_ext/924617554/SOFT_SPI.o \
	${OBJECTDIR}/_ext/924617554/SOFT_UART.o \
	${OBJECTDIR}/_ext/924617554/SOFT_UAT.o \
	${OBJECTDIR}/_ext/345725447/String.o \
	${OBJECTDIR}/_ext/345725447/TWI.o \
	${OBJECTDIR}/_ext/405289639/ADXL345.o \
	${OBJECTDIR}/_ext/405289639/AT24CXX.o \
	${OBJECTDIR}/_ext/405289639/BMP085.o \
	${OBJECTDIR}/_ext/405289639/DS1307.o \
	${OBJECTDIR}/_ext/405289639/DS3231.o \
	${OBJECTDIR}/_ext/405289639/HMC5883L.o \
	${OBJECTDIR}/_ext/405289639/L3G4200D.o \
	${OBJECTDIR}/_ext/405289639/MCP7940N.o \
	${OBJECTDIR}/_ext/405289639/MPU6050.o \
	${OBJECTDIR}/_ext/405289639/PCF8574.o \
	${OBJECTDIR}/_ext/405289639/PCF8591.o \
	${OBJECTDIR}/_ext/345725447/Time.o \
	${OBJECTDIR}/_ext/345725447/Timer.o \
	${OBJECTDIR}/_ext/345725447/Tone.o \
	${OBJECTDIR}/_ext/345725447/Touch.o \
	${OBJECTDIR}/_ext/345725447/Trace.o \
	${OBJECTDIR}/_ext/1138206044/Core.o \
	${OBJECTDIR}/_ext/1138206051/USI_TWI.o \
	${OBJECTDIR}/_ext/345725447/Watchdog.o \
	${OBJECTDIR}/_ext/345725447/Watchdog_timeq.o \
	${OBJECTDIR}/_ext/382955599/CC1101.o \
	${OBJECTDIR}/_ext/382955599/NRF24L01P.o \
	${OBJECTDIR}/_ext/382955599/RFM69.o \
	${OBJECTDIR}/_ext/382955599/VWI.o \
	${OBJECTDIR}/_ext/1944289265/BitstuffingCodec.o \
	${OBJECTDIR}/_ext/1944289265/Block4B5BCodec.o \
	${OBJECTDIR}/_ext/1944289265/ManchesterCodec.o \
	${OBJECTDIR}/_ext/1944289265/VirtualWireCodec.o \
	${OBJECTDIR}/_ext/1508189122/main.o


# C Compiler Flags
CFLAGS=-mmcu=atmega328p -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -Wextra -flto -g -Os -ffunction-sections -fdata-sections

# CC Compiler Flags
CCFLAGS=-mmcu=atmega328p -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -fno-exceptions -Wextra -flto -std=gnu++11 -felide-constructors -g -Os -ffunction-sections -fdata-sections
CXXFLAGS=-mmcu=atmega328p -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -fno-exceptions -Wextra -flto -std=gnu++11 -felide-constructors -g -Os -ffunction-sections -fdata-sections

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-${CND_CONF}.mk ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libarduino_cosa_lib.a

${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libarduino_cosa_lib.a: ${OBJECTFILES}
	${MKDIR} -p ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}
	${RM} ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libarduino_cosa_lib.a
	${AR} -rv ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libarduino_cosa_lib.a ${OBJECTFILES} 
	$(RANLIB) ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libarduino_cosa_lib.a

${OBJECTDIR}/_ext/1138186933/Programmer.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AVR/Programmer.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1138186933
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1138186933/Programmer.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AVR/Programmer.cpp

${OBJECTDIR}/_ext/1138186933/STK500.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AVR/STK500.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1138186933
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1138186933/STK500.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AVR/STK500.cpp

${OBJECTDIR}/_ext/345725447/Activity.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Activity.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Activity.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Activity.cpp

${OBJECTDIR}/_ext/345725447/Alarm.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Alarm.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Alarm.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Alarm.cpp

${OBJECTDIR}/_ext/345725447/AnalogComparator.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogComparator.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/AnalogComparator.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogComparator.cpp

${OBJECTDIR}/_ext/345725447/AnalogPin.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogPin.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/AnalogPin.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogPin.cpp

${OBJECTDIR}/_ext/345725447/AnalogPins.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogPins.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/AnalogPins.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogPins.cpp

${OBJECTDIR}/_ext/345725447/Board.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Board.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Board.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Board.cpp

${OBJECTDIR}/_ext/345725447/Button.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Button.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Button.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Button.cpp

${OBJECTDIR}/_ext/345725447/Canvas.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Canvas.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas.cpp

${OBJECTDIR}/_ext/1828893367/ST7735.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Driver/ST7735.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1828893367
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1828893367/ST7735.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Driver/ST7735.cpp

${OBJECTDIR}/_ext/1572886093/Textbox.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Element/Textbox.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1572886093
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1572886093/Textbox.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Element/Textbox.cpp

${OBJECTDIR}/_ext/190218594/FixedNums8x16.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/FixedNums8x16.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/190218594
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/190218594/FixedNums8x16.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/FixedNums8x16.cpp

${OBJECTDIR}/_ext/190218594/Segment32x50.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/Segment32x50.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/190218594
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/190218594/Segment32x50.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/Segment32x50.cpp

${OBJECTDIR}/_ext/190218594/System5x7.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/System5x7.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/190218594
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/190218594/System5x7.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/System5x7.cpp

${OBJECTDIR}/_ext/971513216/UTFTFont.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/UTFTFont.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/971513216
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/971513216/UTFTFont.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/UTFTFont.cpp

${OBJECTDIR}/_ext/964078797/Base64.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Cipher/Base64.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/964078797
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/964078797/Base64.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Cipher/Base64.cpp

${OBJECTDIR}/_ext/964078797/RC4.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Cipher/RC4.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/964078797
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/964078797/RC4.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Cipher/RC4.cpp

${OBJECTDIR}/_ext/927333040/DHT.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/DHT.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/927333040
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/927333040/DHT.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/DHT.cpp

${OBJECTDIR}/_ext/927333040/DS1302.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/DS1302.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/927333040
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/927333040/DS1302.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/DS1302.cpp

${OBJECTDIR}/_ext/927333040/HCSR04.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/HCSR04.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/927333040
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/927333040/HCSR04.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/HCSR04.cpp

${OBJECTDIR}/_ext/927333040/IR.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/IR.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/927333040
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/927333040/IR.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/IR.cpp

${OBJECTDIR}/_ext/927333040/NEXA.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/NEXA.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/927333040
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/927333040/NEXA.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/NEXA.cpp

${OBJECTDIR}/_ext/927333040/TCS230.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/TCS230.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/927333040
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/927333040/TCS230.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/TCS230.cpp

${OBJECTDIR}/_ext/345725447/EEPROM.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/EEPROM.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/EEPROM.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/EEPROM.cpp

${OBJECTDIR}/_ext/345725447/Event.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Event.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Event.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Event.cpp

${OBJECTDIR}/_ext/345725447/ExternalInterrupt.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/ExternalInterrupt.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/ExternalInterrupt.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/ExternalInterrupt.cpp

${OBJECTDIR}/_ext/175263189/CFFS.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/FS/CFFS.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/175263189
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/175263189/CFFS.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/FS/CFFS.cpp

${OBJECTDIR}/_ext/175263189/FAT16.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/FS/FAT16.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/175263189
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/175263189/FAT16.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/FS/FAT16.cpp

${OBJECTDIR}/_ext/345725447/INET.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/INET.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET.cpp

${OBJECTDIR}/_ext/924286876/DHCP.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/DHCP.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/924286876
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/924286876/DHCP.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/DHCP.cpp

${OBJECTDIR}/_ext/924286876/DNS.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/DNS.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/924286876
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/924286876/DNS.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/DNS.cpp

${OBJECTDIR}/_ext/924286876/HTTP.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/HTTP.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/924286876
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/924286876/HTTP.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/HTTP.cpp

${OBJECTDIR}/_ext/924286876/NTP.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/NTP.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/924286876
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/924286876/NTP.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/NTP.cpp

${OBJECTDIR}/_ext/924286876/SNMP.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/SNMP.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/924286876
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/924286876/SNMP.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/SNMP.cpp

${OBJECTDIR}/_ext/924286876/Telnet.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/Telnet.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/924286876
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/924286876/Telnet.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/Telnet.cpp

${OBJECTDIR}/_ext/345725447/IOStream.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/IOStream.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream.cpp

${OBJECTDIR}/_ext/1098285609/CDC.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/CDC.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1098285609
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1098285609/CDC.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/CDC.cpp

${OBJECTDIR}/_ext/1098285609/RS485.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/RS485.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1098285609
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1098285609/RS485.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/RS485.cpp

${OBJECTDIR}/_ext/1098285609/UART.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/UART.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1098285609
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1098285609/UART.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/UART.cpp

${OBJECTDIR}/_ext/345725447/Keypad.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Keypad.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Keypad.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Keypad.cpp

${OBJECTDIR}/_ext/1462915086/HD44780.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/HD44780.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780.cpp

${OBJECTDIR}/_ext/1462915086/HD44780_IO_DFRobot.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_DFRobot.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/HD44780_IO_DFRobot.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_DFRobot.cpp

${OBJECTDIR}/_ext/1462915086/HD44780_IO_ERM1602_5.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_ERM1602_5.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/HD44780_IO_ERM1602_5.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_ERM1602_5.cpp

${OBJECTDIR}/_ext/1462915086/HD44780_IO_MJKDZ.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_MJKDZ.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/HD44780_IO_MJKDZ.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_MJKDZ.cpp

${OBJECTDIR}/_ext/1462915086/HD44780_IO_Port4b.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_Port4b.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/HD44780_IO_Port4b.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_Port4b.cpp

${OBJECTDIR}/_ext/1462915086/HD44780_IO_SR3W.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR3W.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/HD44780_IO_SR3W.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR3W.cpp

${OBJECTDIR}/_ext/1462915086/HD44780_IO_SR3WSPI.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR3WSPI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/HD44780_IO_SR3WSPI.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR3WSPI.cpp

${OBJECTDIR}/_ext/1462915086/HD44780_IO_SR4W.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR4W.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/HD44780_IO_SR4W.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR4W.cpp

${OBJECTDIR}/_ext/1462915086/HD44780_IO_SainSmart.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SainSmart.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/HD44780_IO_SainSmart.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SainSmart.cpp

${OBJECTDIR}/_ext/1462915086/MAX72XX.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/MAX72XX.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/MAX72XX.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/MAX72XX.cpp

${OBJECTDIR}/_ext/1462915086/PCD8544.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/PCD8544.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/PCD8544.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/PCD8544.cpp

${OBJECTDIR}/_ext/1462915086/ST7565.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/ST7565.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/ST7565.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/ST7565.cpp

${OBJECTDIR}/_ext/1462915086/ST7920.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/ST7920.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/ST7920.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/ST7920.cpp

${OBJECTDIR}/_ext/1462915086/VLCD.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/VLCD.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1462915086
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1462915086/VLCD.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/VLCD.cpp

${OBJECTDIR}/_ext/345725447/Linkage.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Linkage.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Linkage.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Linkage.cpp

${OBJECTDIR}/_ext/345725447/Menu.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Menu.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Menu.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Menu.cpp

${OBJECTDIR}/_ext/638459326/Actor.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Actor.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/638459326
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/638459326/Actor.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Actor.cpp

${OBJECTDIR}/_ext/638459326/Semaphore.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Semaphore.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/638459326
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/638459326/Semaphore.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Semaphore.cpp

${OBJECTDIR}/_ext/638459326/Thread.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Thread.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/638459326
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/638459326/Thread.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Thread.cpp

${OBJECTDIR}/_ext/345725447/OWI.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OWI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/OWI.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OWI.cpp

${OBJECTDIR}/_ext/577277886/DS18B20.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OWI/Driver/DS18B20.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/577277886
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/577277886/DS18B20.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OWI/Driver/DS18B20.cpp

${OBJECTDIR}/_ext/345725447/OutputPin.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OutputPin.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/OutputPin.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OutputPin.cpp

${OBJECTDIR}/_ext/345725447/PWMPin.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/PWMPin.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/PWMPin.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/PWMPin.cpp

${OBJECTDIR}/_ext/345725447/Pin.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Pin.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Pin.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Pin.cpp

${OBJECTDIR}/_ext/345725447/PinChangeInterrupt.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/PinChangeInterrupt.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/PinChangeInterrupt.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/PinChangeInterrupt.cpp

${OBJECTDIR}/_ext/345725447/Power.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Power.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Power.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Power.cpp

${OBJECTDIR}/_ext/345725447/ProtoThread.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/ProtoThread.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/ProtoThread.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/ProtoThread.cpp

${OBJECTDIR}/_ext/345725447/RTC.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/RTC.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/RTC.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/RTC.cpp

${OBJECTDIR}/_ext/345725447/Registry.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Registry.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Registry.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Registry.cpp

${OBJECTDIR}/_ext/345725447/Rotary.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Rotary.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Rotary.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Rotary.cpp

${OBJECTDIR}/_ext/345725447/SPI.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/SPI.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI.cpp

${OBJECTDIR}/_ext/441496781/S25FL127S.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI/Driver/S25FL127S.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/441496781
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/441496781/S25FL127S.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI/Driver/S25FL127S.cpp

${OBJECTDIR}/_ext/441496781/SD.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI/Driver/SD.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/441496781
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/441496781/SD.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI/Driver/SD.cpp

${OBJECTDIR}/_ext/542241094/Ciao.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Ciao.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/542241094
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/542241094/Ciao.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Ciao.cpp

${OBJECTDIR}/_ext/542241094/Fai.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/542241094
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/542241094/Fai.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai.cpp

${OBJECTDIR}/_ext/675975705/analog_pin_t.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/analog_pin_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/675975705
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/675975705/analog_pin_t.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/analog_pin_t.cpp

${OBJECTDIR}/_ext/675975705/digital_pin_t.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/digital_pin_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/675975705
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/675975705/digital_pin_t.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/digital_pin_t.cpp

${OBJECTDIR}/_ext/675975705/digital_pins_t.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/digital_pins_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/675975705
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/675975705/digital_pins_t.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/digital_pins_t.cpp

${OBJECTDIR}/_ext/675975705/event_t.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/event_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/675975705
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/675975705/event_t.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/event_t.cpp

${OBJECTDIR}/_ext/675975705/sample_request_t.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/sample_request_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/675975705
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/675975705/sample_request_t.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/sample_request_t.cpp

${OBJECTDIR}/_ext/675975705/set_mode_t.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/set_mode_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/675975705
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/675975705/set_mode_t.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/set_mode_t.cpp

${OBJECTDIR}/_ext/542241094/ProtocolBuffer.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/ProtocolBuffer.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/542241094
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/542241094/ProtocolBuffer.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/ProtocolBuffer.cpp

${OBJECTDIR}/_ext/345725447/Servo.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Servo.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Servo.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Servo.cpp

${OBJECTDIR}/_ext/345725447/Shell.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Shell.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Shell.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Shell.cpp

${OBJECTDIR}/_ext/345725447/Socket.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Socket.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Socket.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Socket.cpp

${OBJECTDIR}/_ext/1797159876/W5100.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Socket/Driver/W5100.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1797159876
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1797159876/W5100.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Socket/Driver/W5100.cpp

${OBJECTDIR}/_ext/924617554/SOFT_SPI.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_SPI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/924617554
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/924617554/SOFT_SPI.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_SPI.cpp

${OBJECTDIR}/_ext/924617554/SOFT_UART.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_UART.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/924617554
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/924617554/SOFT_UART.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_UART.cpp

${OBJECTDIR}/_ext/924617554/SOFT_UAT.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_UAT.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/924617554
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/924617554/SOFT_UAT.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_UAT.cpp

${OBJECTDIR}/_ext/345725447/String.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/String.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/String.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/String.cpp

${OBJECTDIR}/_ext/345725447/TWI.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/TWI.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI.cpp

${OBJECTDIR}/_ext/405289639/ADXL345.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/ADXL345.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/ADXL345.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/ADXL345.cpp

${OBJECTDIR}/_ext/405289639/AT24CXX.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/AT24CXX.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/AT24CXX.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/AT24CXX.cpp

${OBJECTDIR}/_ext/405289639/BMP085.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/BMP085.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/BMP085.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/BMP085.cpp

${OBJECTDIR}/_ext/405289639/DS1307.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/DS1307.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/DS1307.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/DS1307.cpp

${OBJECTDIR}/_ext/405289639/DS3231.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/DS3231.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/DS3231.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/DS3231.cpp

${OBJECTDIR}/_ext/405289639/HMC5883L.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/HMC5883L.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/HMC5883L.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/HMC5883L.cpp

${OBJECTDIR}/_ext/405289639/L3G4200D.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/L3G4200D.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/L3G4200D.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/L3G4200D.cpp

${OBJECTDIR}/_ext/405289639/MCP7940N.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/MCP7940N.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/MCP7940N.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/MCP7940N.cpp

${OBJECTDIR}/_ext/405289639/MPU6050.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/MPU6050.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/MPU6050.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/MPU6050.cpp

${OBJECTDIR}/_ext/405289639/PCF8574.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/PCF8574.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/PCF8574.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/PCF8574.cpp

${OBJECTDIR}/_ext/405289639/PCF8591.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/PCF8591.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/405289639
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/405289639/PCF8591.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/PCF8591.cpp

${OBJECTDIR}/_ext/345725447/Time.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Time.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Time.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Time.cpp

${OBJECTDIR}/_ext/345725447/Timer.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Timer.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Timer.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Timer.cpp

${OBJECTDIR}/_ext/345725447/Tone.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Tone.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Tone.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Tone.cpp

${OBJECTDIR}/_ext/345725447/Touch.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Touch.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Touch.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Touch.cpp

${OBJECTDIR}/_ext/345725447/Trace.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Trace.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Trace.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Trace.cpp

${OBJECTDIR}/_ext/1138206044/Core.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/USB/Core.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1138206044
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1138206044/Core.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/USB/Core.cpp

${OBJECTDIR}/_ext/1138206051/USI_TWI.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/USI/USI_TWI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1138206051
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1138206051/USI_TWI.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/USI/USI_TWI.cpp

${OBJECTDIR}/_ext/345725447/Watchdog.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Watchdog.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Watchdog.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Watchdog.cpp

${OBJECTDIR}/_ext/345725447/Watchdog_timeq.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Watchdog_timeq.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/345725447
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/345725447/Watchdog_timeq.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Watchdog_timeq.cpp

${OBJECTDIR}/_ext/382955599/CC1101.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/CC1101.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/382955599
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/382955599/CC1101.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/CC1101.cpp

${OBJECTDIR}/_ext/382955599/NRF24L01P.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/NRF24L01P.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/382955599
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/382955599/NRF24L01P.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/NRF24L01P.cpp

${OBJECTDIR}/_ext/382955599/RFM69.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/RFM69.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/382955599
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/382955599/RFM69.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/RFM69.cpp

${OBJECTDIR}/_ext/382955599/VWI.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/382955599
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/382955599/VWI.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI.cpp

${OBJECTDIR}/_ext/1944289265/BitstuffingCodec.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/BitstuffingCodec.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1944289265
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1944289265/BitstuffingCodec.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/BitstuffingCodec.cpp

${OBJECTDIR}/_ext/1944289265/Block4B5BCodec.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/Block4B5BCodec.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1944289265
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1944289265/Block4B5BCodec.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/Block4B5BCodec.cpp

${OBJECTDIR}/_ext/1944289265/ManchesterCodec.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/ManchesterCodec.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1944289265
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1944289265/ManchesterCodec.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/ManchesterCodec.cpp

${OBJECTDIR}/_ext/1944289265/VirtualWireCodec.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/VirtualWireCodec.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1944289265
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1944289265/VirtualWireCodec.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/VirtualWireCodec.cpp

${OBJECTDIR}/_ext/1508189122/main.o: ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/main.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1508189122
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1508189122/main.o ../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/main.cpp

# Subprojects
.build-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${CND_BUILDDIR}/${CND_CONF}
	${RM} ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libarduino_cosa_lib.a

# Subprojects
.clean-subprojects:

# Enable dependency checking
.dep.inc: .depcheck-impl

include .dep.inc
