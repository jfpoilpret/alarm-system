# -*- coding: utf-8 -*-
import random

random.seed(None)

class XTEA:
    DEFAULT_ROUNDS = 64
    KEY_SCHEDULE = 0x9E3779B9L

    @staticmethod
    def generate_key():
        key = []
        for i in range(4):
            key[i] = random.getrandbits(32)
        return key

    def __init__(self, rounds = DEFAULT_ROUNDS):
        self.rounds = rounds
        self.key = [0L, 0L, 0L, 0L]
        pass

    def set_key(self, key):
        self.key = key

    def encipher(self, v):
        v0 = v[0]
        v1 = v[1]
        sumval = 0
        delta = XTEA.KEY_SCHEDULE
        for i in range(self.rounds):
            v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sumval + self.key[sumval & 3])
            sumval += delta
            v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sumval + self.key[(sumval >> 11) & 3])
        v[0] = v0
        v[1] = v1
        return v

    def decipher(self, v):
        v0 = v[0]
        v1 = v[1]
        delta = XTEA.KEY_SCHEDULE
        sumval = delta * self.rounds
        for i in range(self.rounds):
            v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sumval + self.key[(sumval >> 11) & 3])
            sumval -= delta
            v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sumval + self.key[sumval & 3])
        v[0] = v0
        v[1] = v1
        return v


