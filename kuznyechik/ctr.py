#!/usr/bin/env python
"""
An implementation of Kuznyechik's Counter mode

Sources:
- GOST R 34.13-2015
"""

from operator import xor
import secrets
from kuznyechik.base import expand_key, encrypt_block


def _chunk(arr, n):
    """Chunk an array into even parts"""
    for i in range(0, len(arr), n):
        yield arr[i:i + n]


def _CTR(key, IV, message):
    """(En|De)crypt a message given as a bytearray using the Counter mode"""
    K = expand_key(key)
    out = bytearray()
    counter = IV << (8 * 8)
    for block in _chunk(message, 16):
        mask = encrypt_block(K, counter.to_bytes(16, "big"))[:len(block)]
        out.extend(map(xor, block, mask))
        counter += 1
    return out


def gen_key():
    return int.from_bytes(secrets.token_bytes(32), "big")


def encrypt(key, message):
    """Encrypt a message given as a bytearray using the Counter mode"""
    IV = int.from_bytes(secrets.token_bytes(8), "big")
    return IV, _CTR(key, IV, message)


def decrypt(key, IV, message):
    """Decrypt a message given as a bytearray using the Counter mode"""
    return _CTR(key, IV, message)
