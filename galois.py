#!/usr/bin/env python
"""A basic implementation of the Galois field used by Kuznyechik"""


class G:
    """An element of the Galois field"""

    _base = 0b111000011  # x^8 + x^7 + x^6 + x + 1

    def __init__(self, val):
        assert val in range(0, 256), f"{ val } is out of range"
        self._val = val

    def __add__(self, other):
        return G(self._val ^ other._val)

    def __mul__(self, other):
        x = self._val
        res = 0
        for d in other.digits():
            res ^= d * x
            x <<= 1
            if (x >> 8):
                x ^= G._base
        return G(res)

    def digits(self):
        x = self._val
        while x:
            yield x & 1
            x >>= 1

    def __repr__(self):
        return str(self._val)

    def __int__(self):
        return self._val
