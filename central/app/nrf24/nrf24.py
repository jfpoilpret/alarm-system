#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Python port of Maniacbug NRF24L01 library
# Author: Joao Paulo Barraca <jpbarraca@gmail.com>
#
# BeagleBoneBlack and Raspberry Pi use different GPIO access methods.
# Select the most appropriate for you by uncommenting one of the
# two imports.

try:
    # For Raspberry Pi
    import RPi.GPIO as GPIO
except ImportError:
    raise ImportError('RPi.GPIO module not found.')

import spidev
import time
import sys

def _BV(x):
    return 1 << x

class Payload:
    def __init__(self, payload):
        self.device = payload[0]
        self.port = payload[1]
        self.content = payload[2:]

class NRF24:
    BROADCAST = 0

    MAX_CHANNEL = 127
    MAX_PAYLOAD_SIZE = 32

    # PA Levels
    PA_MIN = 0
    PA_LOW = 1
    PA_HIGH = 2
    PA_MAX = 3
    PA_ERROR = 4
    RF_PWR_18DBM = 0
    RF_PWR_12DBM = 2
    RF_PWR_6DBM = 4
    RF_PWR_0DBM = 6

    # Bit rates
    BR_1MBPS = 0
    BR_2MBPS = 1
    BR_250KBPS = 2

    # CRC
    CRC_DISABLED = 0
    CRC_8 = 1
    CRC_16 = 2
    CRC_ENABLED = 3

    # Registers
    CONFIG = 0x00
    EN_AA = 0x01
    EN_RXADDR = 0x02
    SETUP_AW = 0x03
    SETUP_RETR = 0x04
    RF_CH = 0x05
    RF_SETUP = 0x06
    STATUS = 0x07
    OBSERVE_TX = 0x08
    CD = 0x09
    RX_ADDR_P0 = 0x0A
    RX_ADDR_P1 = 0x0B
    RX_ADDR_P2 = 0x0C
    RX_ADDR_P3 = 0x0D
    RX_ADDR_P4 = 0x0E
    RX_ADDR_P5 = 0x0F
    TX_ADDR = 0x10
    RX_PW_P0 = 0x11
    RX_PW_P1 = 0x12
    RX_PW_P2 = 0x13
    RX_PW_P3 = 0x14
    RX_PW_P4 = 0x15
    RX_PW_P5 = 0x16
    FIFO_STATUS = 0x17
    DYNPD = 0x1C
    FEATURE = 0x1D

    # Bit Mnemonics */
    MASK_RX_DR = 6
    MASK_TX_DS = 5
    MASK_MAX_RT = 4
    EN_CRC = 3
    CRCO = 2
    PWR_UP = 1
    PRIM_RX = 0
    ENAA_P5 = 5
    ENAA_P4 = 4
    ENAA_P3 = 3
    ENAA_P2 = 2
    ENAA_P1 = 1
    ENAA_P0 = 0
    ERX_P5 = 5
    ERX_P4 = 4
    ERX_P3 = 3
    ERX_P2 = 2
    ERX_P1 = 1
    ERX_P0 = 0
    AW = 0
    ARD = 4
    ARC = 0
    PLL_LOCK = 4
    RF_DR = 3
    RF_PWR = 6
    RX_DR = 6
    TX_DS = 5
    MAX_RT = 4
    RX_P_NO = 1
    TX_FULL = 0
    PLOS_CNT = 4
    ARC_CNT = 0
    TX_REUSE = 6
    FIFO_FULL = 5
    TX_EMPTY = 4
    RX_FULL = 1
    RX_EMPTY = 0
    DPL_P5 = 5
    DPL_P4 = 4
    DPL_P3 = 3
    DPL_P2 = 2
    DPL_P1 = 1
    DPL_P0 = 0
    DPL_PA = 0x3F
    EN_DPL = 2
    EN_ACK_PAY = 1
    EN_DYN_ACK = 0

    # Instruction Mnemonics
    R_REGISTER = 0x00
    W_REGISTER = 0x20
    REGISTER_MASK = 0x1F
    ACTIVATE = 0x50
    R_RX_PL_WID = 0x60
    R_RX_PAYLOAD = 0x61
    W_TX_PAYLOAD = 0xA0
    W_ACK_PAYLOAD = 0xA8
    W_TX_PAYLOAD_NO_ACK = 0xB0
    FLUSH_TX = 0xE1
    FLUSH_RX = 0xE2
    REUSE_TX_PL = 0xE3
    NOP = 0xFF

    # Non-P omissions
    LNA_HCURR = 0x00

    # P model memory Map
    RPD = 0x09

    # P model bit Mnemonics
    RF_DR_LOW = 5
    RF_DR_HIGH = 3
    RF_PWR_LOW = 1
    RF_PWR_HIGH = 2

    RF_DR_1MBPS = 0
    RF_DR_2MBPS = _BV(RF_DR_HIGH)
    RF_DR_250KBPS = _BV(RF_DR_LOW)

    # Signal Mnemonics
    LOW = 0
    HIGH = 1

    # defaults
    # retransmit delay 500us
    DEFAULT_ARD = 2
    # retry count 15
    DEFAULT_ARC = 15

    datarate_e_str_P = ["1MBPS", "2MBPS", "250KBPS"]
    model_e_str_P = ["nRF24L01", "nRF24l01+"]
    crclength_e_str_P = ["Disabled", "8 bits", "16 bits"]
    pa_dbm_e_str_P = ["PA_MIN", "PA_LOW", "PA_MED", "PA_HIGH"]

    def __init__(self, network, device):
        self.ce_pin = "P9_15"
        self.channel = 64
        self.network = network & 0xFFFF
        self.device = device & 0xFF
        self.spidev = None

    def ce(self, level):
        if level == NRF24.HIGH:
            GPIO.output(self.ce_pin, GPIO.HIGH)
        else:
            GPIO.output(self.ce_pin, GPIO.LOW)
        return

    def read_register(self, reg, blen=1):
        buf = [NRF24.R_REGISTER | (NRF24.REGISTER_MASK & reg)]
        buf += [NRF24.NOP] * max(1, blen)

        resp = self.spidev.xfer2(buf)
        if blen == 1:
            return resp[1]

        return resp[1:]

    def write_register(self, reg, value, length=-1):
        buf = [NRF24.W_REGISTER | (NRF24.REGISTER_MASK & reg)]

        if isinstance(value, (int, long)):
            if length < 0:
                length = 1
            else:
                length = min(4, length)

            i = length
            while i > 0:
                buf += [int(value & 0xff)]
                value >>= 8
                i -= 1

        elif isinstance(value, list):
            if length < 0:
                length = len(value)

            for i in xrange(min(len(value), length)):
                buf.append(int(value[len(value) - i - 1] & 0xff))
        else:
            raise Exception("Value must be int or list")

        return self.spidev.xfer2(buf)[0]

    def flush_rx(self):
        return self.spidev.xfer2([NRF24.FLUSH_RX])[0]

    def flush_tx(self):
        return self.spidev.xfer2([NRF24.FLUSH_TX])[0]

    def get_status(self):
        return self.spidev.xfer2([NRF24.NOP])[0]

    #TODO move prints at the end
    def print_single_status_line(self, name, value):
        print("{0:<16}= {1}".format(name, value))

    def print_status(self, status):
        status_str = "0x{0:02x} RX_DR={1:x} TX_DS={2:x} MAX_RT={3:x} RX_P_NO={4:x} TX_FULL={5:x}".format(
            status,
            1 if status & _BV(NRF24.RX_DR) else 0,
            1 if status & _BV(NRF24.TX_DS) else 0,
            1 if status & _BV(NRF24.MAX_RT) else 0,
            ((status >> NRF24.RX_P_NO) & int("111", 2)),
            1 if status & _BV(NRF24.TX_FULL) else 0)

        self.print_single_status_line("STATUS", status_str)

    def print_observe_tx(self, value):
        tx_str = "OBSERVE_TX=0x{0:02x}: POLS_CNT={2:x} ARC_CNT={2:x}\r\n".format(
            value,
            (value >> NRF24.PLOS_CNT) & int("1111", 2),
            (value >> NRF24.ARC_CNT) & int("1111", 2))

        print(tx_str)

    def print_byte_register(self, name, reg, qty=1):
        registers = ["0x{:0>2x}".format(self.read_register(reg+r)) for r in range(0, qty)]
        self.print_single_status_line(name, " ".join(registers))

    def print_address_register(self, name, reg, qty=1):
        address_registers = ["0x{4:>2x}{3:>2x}{2:>2x}{1:>2x}{0:>2x}".format(
            *self.read_register(reg+r, 5))
            for r in range(0, qty)]

        self.print_single_status_line(name, " ".join(address_registers))

    #TODO those methods should be called before begin(), and not use SPI yet
    def setChannel(self, channel):
        self.channel = min(max(0, channel), NRF24.MAX_CHANNEL)
        self.write_register(NRF24.RF_CH, self.channel)

    def getChannel(self):
        return self.read_register(NRF24.RF_CH)

    def printDetails(self):
        self.print_status(self.get_status())
        self.print_address_register("RX_ADDR_P0-1", NRF24.RX_ADDR_P0, 2)
        self.print_byte_register("RX_ADDR_P2-5", NRF24.RX_ADDR_P2, 4)
        self.print_address_register("TX_ADDR", NRF24.TX_ADDR)

        self.print_byte_register("RX_PW_P0-6", NRF24.RX_PW_P0, 6)
        self.print_byte_register("EN_AA", NRF24.EN_AA)
        self.print_byte_register("EN_RXADDR", NRF24.EN_RXADDR)
        self.print_byte_register("RF_CH", NRF24.RF_CH)
        self.print_byte_register("RF_SETUP", NRF24.RF_SETUP)
        self.print_byte_register("CONFIG", NRF24.CONFIG)
        self.print_byte_register("DYNPD/FEATURE", NRF24.DYNPD, 2)

        self.print_single_status_line("Data Rate", NRF24.datarate_e_str_P[self.getDataRate()])
        self.print_single_status_line("Model", NRF24.model_e_str_P[self.isPVariant()])
        self.print_single_status_line("CRC Length", NRF24.crclength_e_str_P[self.getCRCLength()])
        self.print_single_status_line("PA Power", NRF24.pa_dbm_e_str_P[self.getPALevel()])

    #TODO move public API at the beginning (after __init__())
    def begin(self, major, minor, ce_pin):
        # Initialize SPI bus
        self.spidev = spidev.SpiDev()
        self.spidev.open(major, minor)
        self.ce_pin = ce_pin
        GPIO.setup(self.ce_pin, GPIO.OUT)
        time.sleep(5 / 1000000.0)

        # Setup hardware featues, channel, bitrate, retransmission, dynmic payload
        self.write_register(NRF24.FEATURE,
            _BV(NRF24.EN_DPL) | _BV(NRF24.EN_ACK_PAY) | _BV(NRF24.EN_DYN_ACK))
        self.write_register(NRF24.RF_CH, self.channel)
        self.write_register(NRF24.RF_SETUP, NRF24.RF_DR_2MBPS | NRF24.RF_PWR_0DBM)
        self.write_register(NRF24.SETUP_RETR,
            (NRF24.DEFAULT_ARD) << NRF24.ARD | (NRF24.DEFAULT_ARC << NRF24.ARC))
        self.write_register(NRF24.DYNPD, NRF24.DPL_PA)

        # Setup hardware receive pipes address: network (16b), device (8b)
        self.write_register(NRF24.SETUP_AW, 3 - 2)
        address = [(self.network >> 8) & 0xFF, self.network & 0xFF, self.device]
        self.write_register(NRF24.RX_ADDR_P1, address)
        self.write_register(NRF24.RX_ADDR_P2, NRF24.BROADCAST)
        self.write_register(NRF24.EN_RXADDR, _BV(NRF24.ERX_P2) | _BV(NRF24.ERX_P1))
        self.write_register(NRF24.EN_AA, _BV(NRF24.ENAA_P1) | _BV(NRF24.ENAA_P0))

        self.powerUp()

    def end(self):
        if self.spidev:
            self.spidev.close()
            self.spidev = None

    # Receive structured payload: device, port, content
    def recv(self, timeout_secs = 0.0):
        # set receive mode
        self.write_register(NRF24.CONFIG,
            _BV(NRF24.EN_CRC) | _BV(NRF24.CRC0) | _BV(NRF24.PWR_UP) | _BV(NRF24.PRIM_RX))
        self.ce(NRF24.HIGH)
        # wait for the radio to come up (130us actually only needed)
        time.sleep(130 / 1000000.0)
        now = time.time()
        while not self.available():
            if timeout_secs == 0.0 or time.time() - now > timeout_secs:
                return None
            time.sleep(0.001)
        # read payload size
        count = self.read_register(NRF24.R_RX_PL_WID)
        # read payload
        txbuffer = [NRF24.NOP] * count
        txbuffer[0] = NRF24.R_RX_PAYLOAD
        payload = self.spidev.xfer2(txbuffer)
        return Payload(payload)

    def send(self, dest, port, content):
        # set transmit mode
        address = [(self.network >> 8) & 0xFF, self.network & 0xFF, dest]
        self.write_register(NRF24.TX_ADDR, address)
        self.write_register(NRF24.CONFIG,
            _BV(NRF24.EN_CRC) | _BV(NRF24.CRC0) | _BV(NRF24.PWR_UP))
        self.ce(NRF24.HIGH)
        # wait for the radio to come up (130us actually only needed)
        time.sleep(130 / 1000000.0)
        # Write command, device, port, content
        if dest == NRF24.BROADCAST:
            command = NRF24.W_TX_PAYLOAD_NO_ACK
        else:
            command = NRF24.W_TX_PAYLOAD
        txbuffer = [command, self.device, port]
        txbuffer += content
        self.spidev.xfer2(txbuffer)
        # Check auto acknowledge
        if dest != NRF24.BROADCAST:
            self.write_register(NRF24.RX_ADDR_P0, address)
            self.write_register(NRF24.EN_RXADDR,
                _BV(NRF24.ERX_P2) | _BV(NRF24.ERX_P1) | _BV(NRF24.ERX_P0))
        # Wait for transmission
        status = self.get_status()
        #TODO timeout???
        while not (self.get_status() & (_BV(NRF24.TX_DS) | _BV(NRF24.MAX_RT))):
            time.sleep(0.001)
        data_sent = self.get_status() & _BV(NRF24.TX_DS)

        # Check for auto ack pipe disable
        if dest == NRF24.BROADCAST:
            self.write_register(NRF24.EN_RXADDR,
                _BV(NRF24.ERX_P2) | _BV(NRF24.ERX_P1))

        #TODO
        # Reset status bits

        if data_sent:
           return length(content)
        self.flush_tx()
        return -2

    def powerDown(self):
        self.write_register(NRF24.CONFIG, self.read_register(NRF24.CONFIG) & ~_BV(NRF24.PWR_UP))

    def powerUp(self):
        self.write_register(NRF24.CONFIG, self.read_register(NRF24.CONFIG) | _BV(NRF24.PWR_UP))
        time.sleep(150 / 1000000.0)

    def available(self, pipe_num=None):
        if not pipe_num:
            pipe_num = []

        status = self.get_status()
        result = False

        # Sometimes the radio specifies that there is data in one pipe but
        # doesn't set the RX flag...
        if status & _BV(NRF24.RX_DR) or (status & 0b00001110 != 0b00001110):
            result = True
            # If the caller wants the pipe number, include that
            if len(pipe_num) >= 1:
                pipe_num[0] = (status >> NRF24.RX_P_NO) & 0b00000111

                # Clear the status bit

                # ??? Should this REALLY be cleared now?  Or wait until we
                # actually READ the payload?
        self.write_register(NRF24.STATUS, _BV(NRF24.RX_DR))

        # Handle ack payload receipt
        if status & _BV(NRF24.TX_DS):
            self.write_register(NRF24.STATUS, _BV(NRF24.TX_DS))

        return result

    def testCarrier(self):
        return self.read_register(NRF24.CD) & 1

    def testRPD(self):
        return self.read_register(NRF24.RPD) & 1


    def getPALevel(self):
        power = self.read_register(NRF24.RF_SETUP) & (_BV(NRF24.RF_PWR_LOW) | _BV(NRF24.RF_PWR_HIGH))

        if power == (_BV(NRF24.RF_PWR_LOW) | _BV(NRF24.RF_PWR_HIGH)):
            return NRF24.PA_MAX
        elif power == _BV(NRF24.RF_PWR_HIGH):
            return NRF24.PA_HIGH
        elif power == _BV(NRF24.RF_PWR_LOW):
            return NRF24.PA_LOW
        else:
            return NRF24.PA_MIN



