#!/usr/bin/env python
"""
An implementation of Kuznyechik cypher

Sources:
- GOST R 34.12-2015 (https://www.rfc-editor.org/rfc/rfc7801.html)
- GOST R 34.13-2015
"""

from galois import G
from operator import xor
import secrets

pi_vec = bytearray([
    252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77,
    233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193,
    249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79, 5,
    132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31, 235,
    52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204, 181,
    112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135, 21, 161,
    150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177, 50,
    117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87, 223,
    245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3, 224,
    15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74, 167,
    151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65, 173, 69,
    70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 7, 88, 179,
    64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137, 225, 27, 131,
    73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97, 32, 113, 103,
    164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166, 116,
    210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182
])
pi_inv_vec = bytearray([
    165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158, 57, 85, 126, 82, 145, 100,
    3, 87, 90, 28, 96, 7, 24, 33, 114, 168, 209, 41, 198, 164, 63, 224, 39,
    141, 12, 130, 234, 174, 180, 154, 99, 73, 229, 66, 228, 21, 183, 200, 6,
    112, 157, 65, 117, 25, 201, 170, 252, 77, 191, 42, 115, 132, 213, 195, 175,
    43, 134, 167, 177, 178, 91, 70, 211, 159, 253, 212, 15, 156, 47, 155, 67,
    239, 217, 121, 182, 83, 127, 193, 240, 35, 231, 37, 94, 181, 30, 162, 223,
    166, 254, 172, 34, 249, 226, 74, 188, 53, 202, 238, 120, 5, 107, 81, 225,
    89, 163, 242, 113, 86, 17, 106, 137, 148, 101, 140, 187, 119, 60, 123, 40,
    171, 210, 49, 222, 196, 95, 204, 207, 118, 44, 184, 216, 46, 54, 219, 105,
    179, 20, 149, 190, 98, 161, 59, 22, 102, 233, 92, 108, 109, 173, 55, 97,
    75, 185, 227, 186, 241, 160, 133, 131, 218, 71, 197, 176, 51, 250, 150,
    111, 110, 194, 246, 80, 255, 93, 169, 142, 23, 27, 151, 125, 236, 88, 247,
    31, 251, 124, 9, 13, 122, 103, 69, 135, 220, 232, 79, 29, 78, 4, 235, 248,
    243, 62, 61, 189, 138, 136, 221, 205, 11, 19, 152, 2, 147, 128, 144, 208,
    36, 52, 203, 237, 244, 206, 153, 16, 68, 64, 146, 58, 1, 38, 18, 26, 72,
    104, 245, 129, 139, 199, 214, 32, 10, 8, 0, 76, 215, 116
])
l_vec = [
    G(x) for x in
    [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]
]


def pi(x):
    return pi_vec[x]


def pi_inv(x):
    return pi_inv_vec[x]


def l(x):
    res = G(0)
    for i in range(16):
        res += l_vec[i] * G(x[i])
    return int(res)


def X(k, x):
    return bytearray(map(xor, k, x))


def S(x):
    return bytearray(map(pi, x))


def S_inv(x):
    return bytearray(map(pi_inv, x))


def R(x):
    return bytearray([l(x)]) + x[:15]


def L(x):
    for _ in range(16):
        x = R(x)
    return x


def R_inv(x):
    return x[1:] + bytearray([l(x[1:] + x[:1])])


def L_inv(x):
    for _ in range(16):
        x = R_inv(x)
    return x


def F(k, y, x):
    return X(L(S(X(k, y))), x), y


def expand_key(key):
    key = key.to_bytes(32, "big")
    K = [key[:16], key[16:]]
    for i in range(4):
        K.extend(K[-2:])
        for j in range(8):
            K[-2:] = F(C[8 * i + j], K[-2], K[-1])
    return K


C = [L(i.to_bytes(16, "big")) for i in range(1, 33)]


def encrypt_block(K, x):
    """Encript a single block represented as an array of 16 bytes"""
    for i in range(9):
        x = L(S(X(K[i], x)))
    x = X(K[9], x)
    return x


def decrypt_block(K, x):
    """Decript a single block represented as an array of 16 bytes"""
    x = X(K[9], x)
    for i in range(9):
        x = X(K[8 - i], S_inv(L_inv(x)))
    return x


def chunk(arr, n):
    """Chunk an array into even parts"""
    for i in range(0, len(arr), n):
        yield arr[i:i + n]


def CTR(key, IV, message):
    """(En|De)crypt a message given as a bytearray using the Counter mode"""
    K = expand_key(key)
    out = bytearray()
    counter = int.from_bytes(list(IV) + [0 for _ in range(8)], "big")
    for block in chunk(message, 16):
        mask = encrypt_block(K, counter.to_bytes(16, "big"))[:len(block)]
        out.extend(map(xor, block, mask))
        counter += 1
    return out


def encrypt_CTR(key, message):
    """Encrypt a message given as a bytearray using the Counter mode"""
    IV = secrets.token_bytes(8)
    return IV, CTR(key, IV, message)


def decrypt_CTR(key, IV, message):
    """Decrypt a message given as a bytearray using the Counter mode"""
    return CTR(key, IV, message)
