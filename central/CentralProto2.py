#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

from app.message import MessageType
from MessageHandler import PingHandler, VoltageHandler, LockUnlockHandler, MessageDispatcher

CODE = '123456'

# Current alarm status
locked = 1

devices = [0x10]

#TODO define Events to split concept of network Messages and App Events...
if __name__ == '__main__':
    print "Alarm System Central Prototype..."
    #TODO pass queue to some handlers (voltageHandler, lockHandler)
    pingHandler = PingHandler()
    voltageHandler = VoltageHandler()
    lockHandler = LockUnlockHandler()
    handlers = {
        MessageType.LOCK_CODE: lockHandler,
        MessageType.UNLOCK_CODE: lockHandler,
        MessageType.PING_SERVER: pingHandler,
        MessageType.VOLTAGE_LEVEL: voltageHandler
    }
    globalHandler = MessageDispatcher(CODE, locked, devices, handlers)
    print "Global handler instantiated..."
    globalHandler.start()
    print "Global handler started..."
    while True:
        time.sleep(100.0)

