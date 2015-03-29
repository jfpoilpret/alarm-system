# -*- coding: utf-8 -*-
import random

random.seed(None)

class XTEA:
    DEFAULT_ROUNDS = 32
    KEY_SCHEDULE = 0x9E3779B9L

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
        self.key = [0L, 0L, 0L, 0L]

    def set_key(self, key):
        self.key = key
        sumval = 0
        delta = XTEA.KEY_SCHEDULE
        MASK = 0xFFFFFFFFL
        for i in range(self.rounds):
            self.xor1.append(sumval + self.key[sumval&3])
            sumval = (sumval + delta) & MASK
            self.xor2.append(sumval + self.key[(sumval>>11)&3])

    def encipher(self, v):
        v0 = v[0]
        v1 = v[1]
        MASK = 0xFFFFFFFFL
        for i in range(self.rounds):
            t = (((v1<<4) ^ (v1>>5)) + v1) ^ self.xor1[i]
            v0 = (v0 + t) & MASK
            t = (((v0<<4) ^ (v0>>5)) + v0) ^ self.xor2[i]
            v1 = (v1 + t) & MASK
        return [v0, v1]

    def decipher(self, v):
        v0 = v[0]
        v1 = v[1]
        MASK = 0xFFFFFFFFL
        for i in range(self.rounds):
            t = (((v0<<4) ^ (v0>>5)) + v0) ^ self.xor2[i]
            v1 = (v1 - t) & MASK
            t = (((v1<<4) ^ (v1>>5)) + v1) ^ self.xor1[i]
            v0 = (v0 - t) & MASK
        return [v0, v1]

