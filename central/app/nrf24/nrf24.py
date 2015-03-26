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

def _BV(x):
    return 1 << x

class Payload:
    def __init__(self, payload):
        # NB payload is:
        # - status (NRF24L01)
        # - source device (Cosa) 
        # - port (Cosa)
        # - actual content
        self.status = payload[0]
        self.device = payload[1]
        self.port = payload[2]
        self.content = payload[3:]

class Register:
    CONFIG = 0x00
    EN_AA = 0x01
    EN_RXADDR = 0x02
    SETUP_AW = 0x03
    SETUP_RETR = 0x04
    RF_CH = 0x05
    RF_SETUP = 0x06
    STATUS = 0x07
    OBSERVE_TX = 0x08
    RPD = 0x09
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

class Command:
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

class PALevel:
    RF_PWR_18DBM = 0
    RF_PWR_12DBM = 2
    RF_PWR_6DBM = 4
    RF_PWR_0DBM = 6

class RF_SETUP:
    CONT_WAVE = 7
    RF_DR_LOW = 5
    PLL_LOCK_SIGNAL = 4
    RF_DR_HIGH = 3
    RF_PWR = 1

class BitRate:
    RF_DR_1MBPS = 0
    RF_DR_2MBPS = _BV(RF_SETUP.RF_DR_HIGH)
    RF_DR_250KBPS = _BV(RF_SETUP.RF_DR_LOW)

class CONFIG:
    EN_CRC = 3
    CRCO = 2
    MASK_RX_DR = 6
    MASK_TX_DS = 5
    MASK_MAX_RT = 4
    PWR_UP = 1
    PRIM_RX = 0

class EN_AA:
    ENAA_P5 = 5
    ENAA_P4 = 4
    ENAA_P3 = 3
    ENAA_P2 = 2
    ENAA_P1 = 1
    ENAA_P0 = 0
    ENAA_PA = 0x3F

class EN_RXADDR:
    ERX_P5 = 5
    ERX_P4 = 4
    ERX_P3 = 3
    ERX_P2 = 2
    ERX_P1 = 1
    ERX_P0 = 0
    ERX_PA = 0x3F

class SETUP_AW:
    AW = 0
    AW_3BYTES = 1
    AW_4BYTES = 2
    AW_5BYTES = 3

class SETUP_RETR:
    ARD = 4
    ARC = 0
    # retransmit delay 500us
    DEFAULT_ARD = 2
    # retry count 15
    DEFAULT_ARC = 15

class STATUS:
    RX_DR = 6
    TX_DS = 5
    MAX_RT = 4
    RX_P_NO = 1
    RX_P_NO_MASK = 0x0E
    RX_P_NO_NONE = 0x07
    TX_FIFO_FULL = 0

class OBSERVE_TX:
    PLOS_CNT = 4
    ARC_CNT = 0

class FIFO_STATUS:
    TX_REUSE = 6
    TX_FULL = 5
    TX_EMPTY = 4
    RX_FULL = 1
    RX_EMPTY = 0

class DYNPD:
    DPL_P5 = 5
    DPL_P4 = 4
    DPL_P3 = 3
    DPL_P2 = 2
    DPL_P1 = 1
    DPL_P0 = 0
    DPL_PA = 0x3F

class FEATURE:
    EN_DPL = 2
    EN_ACK_PAY = 1
    EN_DYN_ACK = 0

# Signal Mnemonics
LOW = 0
HIGH = 1

class NRF24:
    BROADCAST = 0

    MAX_CHANNEL = 127
    MAX_PAYLOAD_SIZE = 32

    def __init__(self, network, device):
        self.set_channel(64)
        self.power = PALevel.RF_PWR_0DBM
        self.set_address(network, device)
        self.spidev = None
        GPIO.setmode(GPIO.BCM)

    def set_address(self, network, device):
        self.network = network & 0xFFFF
        self.device = device & 0xFF
    
    def get_device_address(self):
        return self.device
    
    def get_network_address(self):
        return self.network

    def set_channel(self, channel):
        self.channel = channel
            
    def get_channel(self):
        return self.channel
            
    def begin(self, major, minor, ce_pin, autoAck = True):
        # Initialize SPI bus
        self.spidev = spidev.SpiDev()
        self.spidev.open(major, minor)
        self.ce_pin = ce_pin
        GPIO.setup(self.ce_pin, GPIO.OUT)
        time.sleep(5 / 1000000.0)

        # Setup hardware features, channel, bitrate, retransmission, dynmic payload
        self.write_register(Register.FEATURE,
            _BV(FEATURE.EN_DPL) | _BV(FEATURE.EN_ACK_PAY) | _BV(FEATURE.EN_DYN_ACK))
        self.write_register(Register.RF_CH, self.channel)
        self.write_register(Register.RF_SETUP,
            BitRate.RF_DR_2MBPS | self.power)
        self.write_register(Register.SETUP_RETR,
            (SETUP_RETR.DEFAULT_ARD << SETUP_RETR.ARD) | (SETUP_RETR.DEFAULT_ARC << SETUP_RETR.ARC))
        self.write_register(Register.DYNPD, DYNPD.DPL_PA)

        # Setup hardware receive pipes address: network (16b), device (8b)
#       P0: auto-acknowledge (see set_transmit_mode)
#       P1: node address<network:device> with auto-acknowledge
#       P2: broadcast<network:0>
        self.write_register(Register.SETUP_AW, SETUP_AW.AW_3BYTES)
        address = [(self.network >> 8) & 0xFF, self.network & 0xFF, self.device]
        self.write_register(Register.RX_ADDR_P1, address)
        self.write_register(Register.RX_ADDR_P2, NRF24.BROADCAST)
        self.write_register(Register.EN_RXADDR,
            _BV(EN_RXADDR.ERX_P2) | _BV(EN_RXADDR.ERX_P1))
        if autoAck:
            self.write_register(Register.EN_AA,
                _BV(EN_AA.ENAA_P1) | _BV(EN_AA.ENAA_P0))
        else:
            self.write_register(Register.EN_AA, 0)

        self.powerUp()

    def set_device_output_power(self, dBm):
        if dBm < -12:
            self.power = PALevel.RF_PWR_18DBM
        elif dBm < -6:
            self.power = PALevel.RF_PWR_12DBM 
        elif dBm < 0:
            self.power = PALevel.RF_PWR_6DBM
        else:
            self.power = PALevel.RF_PWR_0DBM
        if self.spidev:
            self.write_register(Register.RF_SETUP,
                BitRate.RF_DR_2MBPS | self.power)
        
    def end(self):
        if self.spidev:
            self.spidev.close()
            self.spidev = None

    # Receive structured payload: device, port, content
    def recv(self, timeout_secs = 0.0):
        # set receive mode
        self.ce(LOW)
        self.write_register(Register.CONFIG,
            _BV(CONFIG.EN_CRC) | _BV(CONFIG.CRCO) | _BV(CONFIG.PWR_UP) | _BV(CONFIG.PRIM_RX))
        self.ce(HIGH)
        # wait for the radio to come up (130us actually only needed)
        time.sleep(130 / 1000000.0)
        # wait for payload reception
        now = time.time()
        while not self.available():
            if timeout_secs != 0.0 and time.time() - now > timeout_secs:
                return None
            time.sleep(0.001)
        self.write_register(Register.STATUS, _BV(STATUS.RX_DR))
        # read payload size
        count = self.get_payload_size()
        if count > NRF24.MAX_PAYLOAD_SIZE:
            self.flush_rx()
            return None
        # read payload
        txbuffer = [Command.NOP] * (count + 1)
        txbuffer[0] = Command.R_RX_PAYLOAD
        payload = self.spidev.xfer2(txbuffer)
        self.flush_rx()
        return Payload(payload)

    def send(self, dest, port, content):
        # set transmit mode
        address = [(self.network >> 8) & 0xFF, self.network & 0xFF, dest]
        self.write_register(Register.TX_ADDR, address)
        self.ce(LOW)
        self.write_register(Register.CONFIG,
            _BV(CONFIG.EN_CRC) | _BV(CONFIG.CRCO) | _BV(CONFIG.PWR_UP))
        self.ce(HIGH)
        # wait for the radio to come up (130us actually only needed)
        time.sleep(130 / 1000000.0)
        # Write command, device, port, content
        if dest == NRF24.BROADCAST:
            command = Command.W_TX_PAYLOAD_NO_ACK
        else:
            command = Command.W_TX_PAYLOAD
        txbuffer = [command, self.device, port]
        txbuffer += content
        self.spidev.xfer2(txbuffer)
        # Check auto acknowledge
        if dest != NRF24.BROADCAST:
            self.write_register(Register.RX_ADDR_P0, address)
            self.write_register(Register.EN_RXADDR,
                _BV(EN_RXADDR.ERX_P2) | _BV(EN_RXADDR.ERX_P1) | _BV(EN_RXADDR.ERX_P0))
        # Wait for transmission
        #TODO timeout???
        while True:
            status = self.get_status()
            if status & (_BV(STATUS.TX_DS) | _BV(STATUS.MAX_RT)):
                break
            time.sleep(0.001)
        data_sent = self.get_status() & _BV(STATUS.TX_DS)

        # Check for auto ack pipe disable
        if dest == NRF24.BROADCAST:
            self.write_register(Register.EN_RXADDR,
                _BV(EN_RXADDR.ERX_P2) | _BV(EN_RXADDR.ERX_P1))

        #TODO
        # Reset status bits

        if data_sent:
            return len(content)
        self.flush_tx()
        return -2

    def powerDown(self):
        time.sleep(32 / 1000.0)
        self.ce(LOW)
        self.write_register(Register.CONFIG,
            _BV(CONFIG.EN_CRC) | _BV(CONFIG.CRCO))

    def powerUp(self):
        self.ce(LOW)
        self.write_register(Register.CONFIG,
            _BV(CONFIG.EN_CRC) | _BV(CONFIG.CRCO) | _BV(CONFIG.PWR_UP))
        time.sleep(3 / 1000.0)

        self.write_register(Register.STATUS,
            _BV(STATUS.RX_DR) | _BV(STATUS.TX_DS) | _BV(STATUS.MAX_RT))
        self.flush_tx()
        self.flush_rx()

    def testRPD(self):
        return self.read_register(Register.RPD) & 1
    
    # Implementation methods
    #========================
    def available(self):
        if self.get_fifo_status() & _BV(FIFO_STATUS.RX_EMPTY):
            return False
        if self.get_payload_size() <= NRF24.MAX_PAYLOAD_SIZE:
            return True
        self.flush_rx()
        return False

    def ce(self, level):
        if level == HIGH:
            GPIO.output(self.ce_pin, GPIO.HIGH)
        else:
            GPIO.output(self.ce_pin, GPIO.LOW)
        return

    def get_fifo_status(self):
        return self.read_register(Register.FIFO_STATUS)

    def get_payload_size(self):
        return self.spidev.xfer2([Command.R_RX_PL_WID, 0])[1]

    def read_register(self, reg, blen=1):
        buf = [Command.R_REGISTER | (Command.REGISTER_MASK & reg)]
        buf += [Command.NOP] * max(1, blen)

        resp = self.spidev.xfer2(buf)
        if blen == 1:
            return resp[1]

        return resp[1:]

    def write_register(self, reg, value, length=-1):
        buf = [Command.W_REGISTER | (Command.REGISTER_MASK & reg)]

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
        return self.spidev.xfer2([Command.FLUSH_RX])[0]

    def flush_tx(self):
        return self.spidev.xfer2([Command.FLUSH_TX])[0]

    def get_status(self):
        return self.spidev.xfer2([Command.NOP])[0]

