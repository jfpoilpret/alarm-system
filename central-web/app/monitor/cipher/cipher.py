# -*- coding: utf-8 -*-
import random
import sys

if sys.version_info > (3,):
    long = int
random.seed(None)

class XTEA:
    DEFAULT_ROUNDS = 32
    KEY_SCHEDULE = long(0x9E3779B9)

    @staticmethod
    def generate_key():
        key = []
        for i in range(4):
            key.append(random.getrandbits(32))
        return key

    def __init__(self, rounds = DEFAULT_ROUNDS):
        self.rounds = rounds
        self.xor1 = []
        self.xor2 = []

    def set_key(self, key):
        delta = XTEA.KEY_SCHEDULE
        MASK = long(0xFFFFFFFF)
        self.xor1 = []
        self.xor2 = []
        sumval = 0
        for i in range(self.rounds):
            self.xor1.append(sumval + key[sumval&3])
            sumval = (sumval + delta) & MASK
            self.xor2.append(sumval + key[(sumval>>11)&3])

    def encipher(self, v):
        v0 = v[0]
        v1 = v[1]
        MASK = long(0xFFFFFFFF)
        for i in range(self.rounds):
            t = (((v1<<4) ^ (v1>>5)) + v1) ^ self.xor1[i]
            v0 = (v0 + t) & MASK
            t = (((v0<<4) ^ (v0>>5)) + v0) ^ self.xor2[i]
            v1 = (v1 + t) & MASK
        return [v0, v1]

    def decipher(self, v):
        v0 = v[0]
        v1 = v[1]
        MASK = long(0xFFFFFFFF)
        for i in range(self.rounds):
            t = (((v0<<4) ^ (v0>>5)) + v0) ^ self.xor2[self.rounds - 1 - i]
            v1 = (v1 - t) & MASK
            t = (((v1<<4) ^ (v1>>5)) + v1) ^ self.xor1[self.rounds - 1 - i]
            v0 = (v0 - t) & MASK
        return [v0, v1]

