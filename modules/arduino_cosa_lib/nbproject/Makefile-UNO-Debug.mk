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
CND_CONF=UNO-Debug
CND_DISTDIR=dist
CND_BUILDDIR=build

# Include project Makefile
include Makefile

# Object Directory
OBJECTDIR=${CND_BUILDDIR}/${CND_CONF}/${CND_PLATFORM}

# Object Files
OBJECTFILES= \
	${OBJECTDIR}/_ext/681199812/Programmer.o \
	${OBJECTDIR}/_ext/681199812/STK500.o \
	${OBJECTDIR}/_ext/1033694706/Activity.o \
	${OBJECTDIR}/_ext/1033694706/Alarm.o \
	${OBJECTDIR}/_ext/1033694706/AnalogComparator.o \
	${OBJECTDIR}/_ext/1033694706/AnalogPin.o \
	${OBJECTDIR}/_ext/1033694706/AnalogPins.o \
	${OBJECTDIR}/_ext/1033694706/Board.o \
	${OBJECTDIR}/_ext/1033694706/Button.o \
	${OBJECTDIR}/_ext/1033694706/Canvas.o \
	${OBJECTDIR}/_ext/468210302/ST7735.o \
	${OBJECTDIR}/_ext/1953583258/Textbox.o \
	${OBJECTDIR}/_ext/500014043/FixedNums8x16.o \
	${OBJECTDIR}/_ext/500014043/Segment32x50.o \
	${OBJECTDIR}/_ext/500014043/System5x7.o \
	${OBJECTDIR}/_ext/165242009/UTFTFont.o \
	${OBJECTDIR}/_ext/172676428/Base64.o \
	${OBJECTDIR}/_ext/172676428/RC4.o \
	${OBJECTDIR}/_ext/209422185/DHT.o \
	${OBJECTDIR}/_ext/209422185/DS1302.o \
	${OBJECTDIR}/_ext/209422185/HCSR04.o \
	${OBJECTDIR}/_ext/209422185/IR.o \
	${OBJECTDIR}/_ext/209422185/NEXA.o \
	${OBJECTDIR}/_ext/209422185/TCS230.o \
	${OBJECTDIR}/_ext/1033694706/EEPROM.o \
	${OBJECTDIR}/_ext/1033694706/Event.o \
	${OBJECTDIR}/_ext/1033694706/ExternalInterrupt.o \
	${OBJECTDIR}/_ext/116573294/CFFS.o \
	${OBJECTDIR}/_ext/116573294/FAT16.o \
	${OBJECTDIR}/_ext/1033694706/INET.o \
	${OBJECTDIR}/_ext/357872629/DHCP.o \
	${OBJECTDIR}/_ext/357872629/DNS.o \
	${OBJECTDIR}/_ext/357872629/HTTP.o \
	${OBJECTDIR}/_ext/357872629/NTP.o \
	${OBJECTDIR}/_ext/357872629/SNMP.o \
	${OBJECTDIR}/_ext/357872629/Telnet.o \
	${OBJECTDIR}/_ext/1033694706/IOStream.o \
	${OBJECTDIR}/_ext/848081872/CDC.o \
	${OBJECTDIR}/_ext/848081872/RS485.o \
	${OBJECTDIR}/_ext/848081872/UART.o \
	${OBJECTDIR}/_ext/1033694706/Keypad.o \
	${OBJECTDIR}/_ext/1298038155/HD44780.o \
	${OBJECTDIR}/_ext/1298038155/HD44780_IO_DFRobot.o \
	${OBJECTDIR}/_ext/1298038155/HD44780_IO_ERM1602_5.o \
	${OBJECTDIR}/_ext/1298038155/HD44780_IO_MJKDZ.o \
	${OBJECTDIR}/_ext/1298038155/HD44780_IO_Port4b.o \
	${OBJECTDIR}/_ext/1298038155/HD44780_IO_SR3W.o \
	${OBJECTDIR}/_ext/1298038155/HD44780_IO_SR3WSPI.o \
	${OBJECTDIR}/_ext/1298038155/HD44780_IO_SR4W.o \
	${OBJECTDIR}/_ext/1298038155/HD44780_IO_SainSmart.o \
	${OBJECTDIR}/_ext/1298038155/MAX72XX.o \
	${OBJECTDIR}/_ext/1298038155/PCD8544.o \
	${OBJECTDIR}/_ext/1298038155/ST7565.o \
	${OBJECTDIR}/_ext/1298038155/ST7920.o \
	${OBJECTDIR}/_ext/1298038155/VLCD.o \
	${OBJECTDIR}/_ext/1033694706/Linkage.o \
	${OBJECTDIR}/_ext/1033694706/Menu.o \
	${OBJECTDIR}/_ext/498295899/Actor.o \
	${OBJECTDIR}/_ext/498295899/Semaphore.o \
	${OBJECTDIR}/_ext/498295899/Thread.o \
	${OBJECTDIR}/_ext/1033694706/OWI.o \
	${OBJECTDIR}/_ext/956736169/DS18B20.o \
	${OBJECTDIR}/_ext/1033694706/OutputPin.o \
	${OBJECTDIR}/_ext/1033694706/PWMPin.o \
	${OBJECTDIR}/_ext/1033694706/Pin.o \
	${OBJECTDIR}/_ext/1033694706/PinChangeInterrupt.o \
	${OBJECTDIR}/_ext/1033694706/Power.o \
	${OBJECTDIR}/_ext/1033694706/ProtoThread.o \
	${OBJECTDIR}/_ext/1033694706/RTC.o \
	${OBJECTDIR}/_ext/1033694706/Registry.o \
	${OBJECTDIR}/_ext/1033694706/Rotary.o \
	${OBJECTDIR}/_ext/1033694706/SPI.o \
	${OBJECTDIR}/_ext/1975510836/S25FL127S.o \
	${OBJECTDIR}/_ext/1975510836/SD.o \
	${OBJECTDIR}/_ext/2076255149/Ciao.o \
	${OBJECTDIR}/_ext/2076255149/Fai.o \
	${OBJECTDIR}/_ext/1444473650/analog_pin_t.o \
	${OBJECTDIR}/_ext/1444473650/digital_pin_t.o \
	${OBJECTDIR}/_ext/1444473650/digital_pins_t.o \
	${OBJECTDIR}/_ext/1444473650/event_t.o \
	${OBJECTDIR}/_ext/1444473650/sample_request_t.o \
	${OBJECTDIR}/_ext/1444473650/set_mode_t.o \
	${OBJECTDIR}/_ext/2076255149/ProtocolBuffer.o \
	${OBJECTDIR}/_ext/1033694706/Servo.o \
	${OBJECTDIR}/_ext/1033694706/Shell.o \
	${OBJECTDIR}/_ext/1033694706/Socket.o \
	${OBJECTDIR}/_ext/1137124355/W5100.o \
	${OBJECTDIR}/_ext/358203307/SOFT_SPI.o \
	${OBJECTDIR}/_ext/358203307/SOFT_UART.o \
	${OBJECTDIR}/_ext/358203307/SOFT_UAT.o \
	${OBJECTDIR}/_ext/1033694706/String.o \
	${OBJECTDIR}/_ext/1033694706/TWI.o \
	${OBJECTDIR}/_ext/1939303694/ADXL345.o \
	${OBJECTDIR}/_ext/1939303694/AT24CXX.o \
	${OBJECTDIR}/_ext/1939303694/BMP085.o \
	${OBJECTDIR}/_ext/1939303694/DS1307.o \
	${OBJECTDIR}/_ext/1939303694/DS3231.o \
	${OBJECTDIR}/_ext/1939303694/HMC5883L.o \
	${OBJECTDIR}/_ext/1939303694/L3G4200D.o \
	${OBJECTDIR}/_ext/1939303694/MCP7940N.o \
	${OBJECTDIR}/_ext/1939303694/MPU6050.o \
	${OBJECTDIR}/_ext/1939303694/PCF8574.o \
	${OBJECTDIR}/_ext/1939303694/PCF8591.o \
	${OBJECTDIR}/_ext/1033694706/Time.o \
	${OBJECTDIR}/_ext/1033694706/Timer.o \
	${OBJECTDIR}/_ext/1033694706/Tone.o \
	${OBJECTDIR}/_ext/1033694706/Touch.o \
	${OBJECTDIR}/_ext/1033694706/Trace.o \
	${OBJECTDIR}/_ext/681180701/Core.o \
	${OBJECTDIR}/_ext/681180694/USI_TWI.o \
	${OBJECTDIR}/_ext/1033694706/Watchdog.o \
	${OBJECTDIR}/_ext/1033694706/Watchdog_timeq.o \
	${OBJECTDIR}/_ext/1965644216/CC1101.o \
	${OBJECTDIR}/_ext/1965644216/NRF24L01P.o \
	${OBJECTDIR}/_ext/1965644216/RFM69.o \
	${OBJECTDIR}/_ext/1965644216/VWI.o \
	${OBJECTDIR}/_ext/1137922760/BitstuffingCodec.o \
	${OBJECTDIR}/_ext/1137922760/Block4B5BCodec.o \
	${OBJECTDIR}/_ext/1137922760/ManchesterCodec.o \
	${OBJECTDIR}/_ext/1137922760/VirtualWireCodec.o \
	${OBJECTDIR}/_ext/1458683045/main.o


# C Compiler Flags
CFLAGS=-mmcu=${MCU} -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -Wextra -flto -O0 -g -ffunction-sections -fdata-sections

# CC Compiler Flags
CCFLAGS=-mmcu=${MCU} -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -fno-exceptions -Wextra -flto -std=gnu++11 -felide-constructors -O0 -g -ffunction-sections -fdata-sections
CXXFLAGS=-mmcu=${MCU} -DF_CPU=${F_CPU} -DARDUINO=${ARDUINO} -fno-exceptions -Wextra -flto -std=gnu++11 -felide-constructors -O0 -g -ffunction-sections -fdata-sections

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

${OBJECTDIR}/_ext/681199812/Programmer.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AVR/Programmer.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/681199812
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/681199812/Programmer.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AVR/Programmer.cpp

${OBJECTDIR}/_ext/681199812/STK500.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AVR/STK500.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/681199812
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/681199812/STK500.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AVR/STK500.cpp

${OBJECTDIR}/_ext/1033694706/Activity.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Activity.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Activity.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Activity.cpp

${OBJECTDIR}/_ext/1033694706/Alarm.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Alarm.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Alarm.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Alarm.cpp

${OBJECTDIR}/_ext/1033694706/AnalogComparator.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogComparator.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/AnalogComparator.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogComparator.cpp

${OBJECTDIR}/_ext/1033694706/AnalogPin.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogPin.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/AnalogPin.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogPin.cpp

${OBJECTDIR}/_ext/1033694706/AnalogPins.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogPins.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/AnalogPins.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/AnalogPins.cpp

${OBJECTDIR}/_ext/1033694706/Board.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Board.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Board.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Board.cpp

${OBJECTDIR}/_ext/1033694706/Button.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Button.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Button.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Button.cpp

${OBJECTDIR}/_ext/1033694706/Canvas.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Canvas.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas.cpp

${OBJECTDIR}/_ext/468210302/ST7735.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Driver/ST7735.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/468210302
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/468210302/ST7735.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Driver/ST7735.cpp

${OBJECTDIR}/_ext/1953583258/Textbox.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Element/Textbox.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1953583258
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1953583258/Textbox.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Element/Textbox.cpp

${OBJECTDIR}/_ext/500014043/FixedNums8x16.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/FixedNums8x16.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/500014043
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/500014043/FixedNums8x16.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/FixedNums8x16.cpp

${OBJECTDIR}/_ext/500014043/Segment32x50.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/Segment32x50.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/500014043
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/500014043/Segment32x50.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/Segment32x50.cpp

${OBJECTDIR}/_ext/500014043/System5x7.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/System5x7.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/500014043
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/500014043/System5x7.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/Font/System5x7.cpp

${OBJECTDIR}/_ext/165242009/UTFTFont.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/UTFTFont.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/165242009
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/165242009/UTFTFont.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Canvas/UTFTFont.cpp

${OBJECTDIR}/_ext/172676428/Base64.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Cipher/Base64.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/172676428
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/172676428/Base64.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Cipher/Base64.cpp

${OBJECTDIR}/_ext/172676428/RC4.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Cipher/RC4.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/172676428
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/172676428/RC4.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Cipher/RC4.cpp

${OBJECTDIR}/_ext/209422185/DHT.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/DHT.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/209422185
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/209422185/DHT.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/DHT.cpp

${OBJECTDIR}/_ext/209422185/DS1302.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/DS1302.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/209422185
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/209422185/DS1302.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/DS1302.cpp

${OBJECTDIR}/_ext/209422185/HCSR04.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/HCSR04.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/209422185
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/209422185/HCSR04.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/HCSR04.cpp

${OBJECTDIR}/_ext/209422185/IR.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/IR.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/209422185
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/209422185/IR.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/IR.cpp

${OBJECTDIR}/_ext/209422185/NEXA.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/NEXA.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/209422185
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/209422185/NEXA.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/NEXA.cpp

${OBJECTDIR}/_ext/209422185/TCS230.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/TCS230.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/209422185
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/209422185/TCS230.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Driver/TCS230.cpp

${OBJECTDIR}/_ext/1033694706/EEPROM.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/EEPROM.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/EEPROM.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/EEPROM.cpp

${OBJECTDIR}/_ext/1033694706/Event.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Event.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Event.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Event.cpp

${OBJECTDIR}/_ext/1033694706/ExternalInterrupt.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/ExternalInterrupt.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/ExternalInterrupt.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/ExternalInterrupt.cpp

${OBJECTDIR}/_ext/116573294/CFFS.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/FS/CFFS.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/116573294
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/116573294/CFFS.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/FS/CFFS.cpp

${OBJECTDIR}/_ext/116573294/FAT16.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/FS/FAT16.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/116573294
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/116573294/FAT16.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/FS/FAT16.cpp

${OBJECTDIR}/_ext/1033694706/INET.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/INET.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET.cpp

${OBJECTDIR}/_ext/357872629/DHCP.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/DHCP.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/357872629
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/357872629/DHCP.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/DHCP.cpp

${OBJECTDIR}/_ext/357872629/DNS.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/DNS.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/357872629
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/357872629/DNS.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/DNS.cpp

${OBJECTDIR}/_ext/357872629/HTTP.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/HTTP.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/357872629
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/357872629/HTTP.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/HTTP.cpp

${OBJECTDIR}/_ext/357872629/NTP.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/NTP.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/357872629
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/357872629/NTP.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/NTP.cpp

${OBJECTDIR}/_ext/357872629/SNMP.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/SNMP.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/357872629
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/357872629/SNMP.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/SNMP.cpp

${OBJECTDIR}/_ext/357872629/Telnet.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/Telnet.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/357872629
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/357872629/Telnet.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/INET/Telnet.cpp

${OBJECTDIR}/_ext/1033694706/IOStream.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/IOStream.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream.cpp

${OBJECTDIR}/_ext/848081872/CDC.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/CDC.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/848081872
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/848081872/CDC.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/CDC.cpp

${OBJECTDIR}/_ext/848081872/RS485.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/RS485.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/848081872
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/848081872/RS485.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/RS485.cpp

${OBJECTDIR}/_ext/848081872/UART.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/UART.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/848081872
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/848081872/UART.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/IOStream/Driver/UART.cpp

${OBJECTDIR}/_ext/1033694706/Keypad.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Keypad.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Keypad.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Keypad.cpp

${OBJECTDIR}/_ext/1298038155/HD44780.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/HD44780.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780.cpp

${OBJECTDIR}/_ext/1298038155/HD44780_IO_DFRobot.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_DFRobot.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/HD44780_IO_DFRobot.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_DFRobot.cpp

${OBJECTDIR}/_ext/1298038155/HD44780_IO_ERM1602_5.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_ERM1602_5.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/HD44780_IO_ERM1602_5.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_ERM1602_5.cpp

${OBJECTDIR}/_ext/1298038155/HD44780_IO_MJKDZ.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_MJKDZ.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/HD44780_IO_MJKDZ.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_MJKDZ.cpp

${OBJECTDIR}/_ext/1298038155/HD44780_IO_Port4b.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_Port4b.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/HD44780_IO_Port4b.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_Port4b.cpp

${OBJECTDIR}/_ext/1298038155/HD44780_IO_SR3W.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR3W.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/HD44780_IO_SR3W.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR3W.cpp

${OBJECTDIR}/_ext/1298038155/HD44780_IO_SR3WSPI.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR3WSPI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/HD44780_IO_SR3WSPI.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR3WSPI.cpp

${OBJECTDIR}/_ext/1298038155/HD44780_IO_SR4W.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR4W.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/HD44780_IO_SR4W.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SR4W.cpp

${OBJECTDIR}/_ext/1298038155/HD44780_IO_SainSmart.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SainSmart.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/HD44780_IO_SainSmart.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/HD44780_IO_SainSmart.cpp

${OBJECTDIR}/_ext/1298038155/MAX72XX.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/MAX72XX.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/MAX72XX.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/MAX72XX.cpp

${OBJECTDIR}/_ext/1298038155/PCD8544.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/PCD8544.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/PCD8544.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/PCD8544.cpp

${OBJECTDIR}/_ext/1298038155/ST7565.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/ST7565.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/ST7565.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/ST7565.cpp

${OBJECTDIR}/_ext/1298038155/ST7920.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/ST7920.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/ST7920.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/ST7920.cpp

${OBJECTDIR}/_ext/1298038155/VLCD.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/VLCD.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1298038155
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1298038155/VLCD.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/LCD/Driver/VLCD.cpp

${OBJECTDIR}/_ext/1033694706/Linkage.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Linkage.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Linkage.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Linkage.cpp

${OBJECTDIR}/_ext/1033694706/Menu.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Menu.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Menu.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Menu.cpp

${OBJECTDIR}/_ext/498295899/Actor.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Actor.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/498295899
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/498295899/Actor.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Actor.cpp

${OBJECTDIR}/_ext/498295899/Semaphore.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Semaphore.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/498295899
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/498295899/Semaphore.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Semaphore.cpp

${OBJECTDIR}/_ext/498295899/Thread.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Thread.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/498295899
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/498295899/Thread.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Nucleo/Thread.cpp

${OBJECTDIR}/_ext/1033694706/OWI.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OWI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/OWI.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OWI.cpp

${OBJECTDIR}/_ext/956736169/DS18B20.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OWI/Driver/DS18B20.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/956736169
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/956736169/DS18B20.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OWI/Driver/DS18B20.cpp

${OBJECTDIR}/_ext/1033694706/OutputPin.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OutputPin.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/OutputPin.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/OutputPin.cpp

${OBJECTDIR}/_ext/1033694706/PWMPin.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/PWMPin.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/PWMPin.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/PWMPin.cpp

${OBJECTDIR}/_ext/1033694706/Pin.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Pin.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Pin.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Pin.cpp

${OBJECTDIR}/_ext/1033694706/PinChangeInterrupt.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/PinChangeInterrupt.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/PinChangeInterrupt.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/PinChangeInterrupt.cpp

${OBJECTDIR}/_ext/1033694706/Power.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Power.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Power.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Power.cpp

${OBJECTDIR}/_ext/1033694706/ProtoThread.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/ProtoThread.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/ProtoThread.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/ProtoThread.cpp

${OBJECTDIR}/_ext/1033694706/RTC.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/RTC.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/RTC.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/RTC.cpp

${OBJECTDIR}/_ext/1033694706/Registry.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Registry.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Registry.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Registry.cpp

${OBJECTDIR}/_ext/1033694706/Rotary.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Rotary.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Rotary.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Rotary.cpp

${OBJECTDIR}/_ext/1033694706/SPI.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/SPI.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI.cpp

${OBJECTDIR}/_ext/1975510836/S25FL127S.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI/Driver/S25FL127S.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1975510836
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1975510836/S25FL127S.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI/Driver/S25FL127S.cpp

${OBJECTDIR}/_ext/1975510836/SD.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI/Driver/SD.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1975510836
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1975510836/SD.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/SPI/Driver/SD.cpp

${OBJECTDIR}/_ext/2076255149/Ciao.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Ciao.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/2076255149
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/2076255149/Ciao.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Ciao.cpp

${OBJECTDIR}/_ext/2076255149/Fai.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/2076255149
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/2076255149/Fai.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai.cpp

${OBJECTDIR}/_ext/1444473650/analog_pin_t.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/analog_pin_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1444473650
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1444473650/analog_pin_t.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/analog_pin_t.cpp

${OBJECTDIR}/_ext/1444473650/digital_pin_t.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/digital_pin_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1444473650
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1444473650/digital_pin_t.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/digital_pin_t.cpp

${OBJECTDIR}/_ext/1444473650/digital_pins_t.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/digital_pins_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1444473650
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1444473650/digital_pins_t.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/digital_pins_t.cpp

${OBJECTDIR}/_ext/1444473650/event_t.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/event_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1444473650
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1444473650/event_t.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/event_t.cpp

${OBJECTDIR}/_ext/1444473650/sample_request_t.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/sample_request_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1444473650
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1444473650/sample_request_t.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/sample_request_t.cpp

${OBJECTDIR}/_ext/1444473650/set_mode_t.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/set_mode_t.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1444473650
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1444473650/set_mode_t.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/Fai/set_mode_t.cpp

${OBJECTDIR}/_ext/2076255149/ProtocolBuffer.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/ProtocolBuffer.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/2076255149
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/2076255149/ProtocolBuffer.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Serializer/ProtocolBuffer.cpp

${OBJECTDIR}/_ext/1033694706/Servo.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Servo.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Servo.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Servo.cpp

${OBJECTDIR}/_ext/1033694706/Shell.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Shell.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Shell.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Shell.cpp

${OBJECTDIR}/_ext/1033694706/Socket.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Socket.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Socket.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Socket.cpp

${OBJECTDIR}/_ext/1137124355/W5100.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Socket/Driver/W5100.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1137124355
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1137124355/W5100.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Socket/Driver/W5100.cpp

${OBJECTDIR}/_ext/358203307/SOFT_SPI.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_SPI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/358203307
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/358203307/SOFT_SPI.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_SPI.cpp

${OBJECTDIR}/_ext/358203307/SOFT_UART.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_UART.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/358203307
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/358203307/SOFT_UART.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_UART.cpp

${OBJECTDIR}/_ext/358203307/SOFT_UAT.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_UAT.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/358203307
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/358203307/SOFT_UAT.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Soft/SOFT_UAT.cpp

${OBJECTDIR}/_ext/1033694706/String.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/String.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/String.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/String.cpp

${OBJECTDIR}/_ext/1033694706/TWI.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/TWI.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI.cpp

${OBJECTDIR}/_ext/1939303694/ADXL345.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/ADXL345.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/ADXL345.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/ADXL345.cpp

${OBJECTDIR}/_ext/1939303694/AT24CXX.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/AT24CXX.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/AT24CXX.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/AT24CXX.cpp

${OBJECTDIR}/_ext/1939303694/BMP085.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/BMP085.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/BMP085.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/BMP085.cpp

${OBJECTDIR}/_ext/1939303694/DS1307.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/DS1307.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/DS1307.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/DS1307.cpp

${OBJECTDIR}/_ext/1939303694/DS3231.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/DS3231.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/DS3231.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/DS3231.cpp

${OBJECTDIR}/_ext/1939303694/HMC5883L.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/HMC5883L.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/HMC5883L.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/HMC5883L.cpp

${OBJECTDIR}/_ext/1939303694/L3G4200D.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/L3G4200D.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/L3G4200D.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/L3G4200D.cpp

${OBJECTDIR}/_ext/1939303694/MCP7940N.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/MCP7940N.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/MCP7940N.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/MCP7940N.cpp

${OBJECTDIR}/_ext/1939303694/MPU6050.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/MPU6050.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/MPU6050.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/MPU6050.cpp

${OBJECTDIR}/_ext/1939303694/PCF8574.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/PCF8574.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/PCF8574.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/PCF8574.cpp

${OBJECTDIR}/_ext/1939303694/PCF8591.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/PCF8591.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1939303694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1939303694/PCF8591.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/TWI/Driver/PCF8591.cpp

${OBJECTDIR}/_ext/1033694706/Time.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Time.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Time.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Time.cpp

${OBJECTDIR}/_ext/1033694706/Timer.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Timer.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Timer.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Timer.cpp

${OBJECTDIR}/_ext/1033694706/Tone.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Tone.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Tone.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Tone.cpp

${OBJECTDIR}/_ext/1033694706/Touch.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Touch.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Touch.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Touch.cpp

${OBJECTDIR}/_ext/1033694706/Trace.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Trace.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Trace.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Trace.cpp

${OBJECTDIR}/_ext/681180701/Core.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/USB/Core.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/681180701
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/681180701/Core.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/USB/Core.cpp

${OBJECTDIR}/_ext/681180694/USI_TWI.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/USI/USI_TWI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/681180694
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/681180694/USI_TWI.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/USI/USI_TWI.cpp

${OBJECTDIR}/_ext/1033694706/Watchdog.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Watchdog.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Watchdog.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Watchdog.cpp

${OBJECTDIR}/_ext/1033694706/Watchdog_timeq.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Watchdog_timeq.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1033694706
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1033694706/Watchdog_timeq.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Watchdog_timeq.cpp

${OBJECTDIR}/_ext/1965644216/CC1101.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/CC1101.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1965644216
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1965644216/CC1101.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/CC1101.cpp

${OBJECTDIR}/_ext/1965644216/NRF24L01P.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/NRF24L01P.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1965644216
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1965644216/NRF24L01P.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/NRF24L01P.cpp

${OBJECTDIR}/_ext/1965644216/RFM69.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/RFM69.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1965644216
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1965644216/RFM69.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/RFM69.cpp

${OBJECTDIR}/_ext/1965644216/VWI.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1965644216
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1965644216/VWI.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI.cpp

${OBJECTDIR}/_ext/1137922760/BitstuffingCodec.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/BitstuffingCodec.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1137922760
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1137922760/BitstuffingCodec.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/BitstuffingCodec.cpp

${OBJECTDIR}/_ext/1137922760/Block4B5BCodec.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/Block4B5BCodec.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1137922760
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1137922760/Block4B5BCodec.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/Block4B5BCodec.cpp

${OBJECTDIR}/_ext/1137922760/ManchesterCodec.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/ManchesterCodec.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1137922760
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1137922760/ManchesterCodec.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/ManchesterCodec.cpp

${OBJECTDIR}/_ext/1137922760/VirtualWireCodec.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/VirtualWireCodec.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1137922760
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1137922760/VirtualWireCodec.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/Cosa/Wireless/Driver/VWI/Codec/VirtualWireCodec.cpp

${OBJECTDIR}/_ext/1458683045/main.o: ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/main.cpp 
	${MKDIR} -p ${OBJECTDIR}/_ext/1458683045
	${RM} "$@.d"
	$(COMPILE.cc) -Wall -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa -I../../../../arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/variants/${VARIANT} -MMD -MP -MF "$@.d" -o ${OBJECTDIR}/_ext/1458683045/main.o ../../../../../electronics/arduino/tools/arduino-1.5.8/sketchbook/hardware/Cosa/avr/cores/cosa/main.cpp

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
