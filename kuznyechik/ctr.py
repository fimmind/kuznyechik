#!/usr/bin/env python
"""
An implementation of Kuznyechik's Counter mode

Sources:
- GOST R 34.13-2015
"""

from operator import xor
import secrets
from typing import TypeVar, Iterator
from kuznyechik.base import expand_key, encrypt_block

T = TypeVar('T')


# Функция, разделяющая массив arr на куски из n элементов
def _chunk(arr: [T], n: int) -> Iterator[[T]]:
    """Chunk an array into even parts"""
    for i in range(0, len(arr), n):
        yield arr[i:i + n]


# Реализация общего алгоритма шифрования в режиме гаммирования. На основании
# значения синхропосылки IV инициализируется 16-байтный счётчик
#     CTR_1 := IV << (8 * 8)
# и для каждого следующего блока шифрования его значение увеличивается на 1:
#     CTR_(i+1) := CTR_i + 1.
# Из значений счётчика генерируется так называемая "гамма шифра" путём
# шифрования значений CTR_i, то есть i-й блок гаммы есть
#     E_(K₁, ..., K₁₀)(CTR_i).
# Наконец, каждый блок входного сообщения P_i складывается со значением гаммы
# битовой операцией XOR и на выходе получается последовательность зашифрованных
# блоков C_i, определяющихся по формуле
#     C_i := P_i ⊕ E_(K₁, ..., K₁₀)(CTR_i).
# При необходимости, последний блок гаммы урезается до длинны последнего блока
# входного сообщения.
#
# Поскольку обратной к операции прибаваления гаммы битовой опреацией XOR
# является эта же самая операция, нет необходимости отдельно реализовывать
# алгоритмы зашифрования и расшифрования, а достаточно лишь использовать общий
# алгоритм, при необходимости генерируя значение синхропосылки, что и сделано в
# методах encrypt и decrypt
# → пункт 5.2 из ГОСТа
def _CTR(key: int, IV: int, message: bytearray) -> bytearray:
    """(En|De)crypt a message given as a bytearray using the Counter mode"""
    K = expand_key(key)
    out = bytearray()
    counter = IV << (8 * 8)
    for block in _chunk(message, 16):
        mask = encrypt_block(K, counter.to_bytes(16, "big"))[:len(block)]
        out.extend(map(xor, block, mask))
        counter += 1
    return out


# Реализация алгоритма зашифрования. Сначала генерируется 8-битная
# синхропосылка IV и для неё вызывается общий алгоритм шифрования в режиме
# гаммирования
# → пункт 5.2.1 из ГОСТа
def encrypt(key: int, message: bytearray) -> (int, bytearray):
    """Encrypt a message given as a bytearray using the Counter mode"""
    IV = int.from_bytes(secrets.token_bytes(8), "big")
    return IV, _CTR(key, IV, message)


# Реализация алгоритма расшифрования через прямой вызов общего алгоритма
# шифрования в режиме гаммирования
# → пункт 5.2.2 из ГОСТа
def decrypt(key: int, IV: int, message: bytearray) -> bytearray:
    """Decrypt a message given as a bytearray using the Counter mode"""
    return _CTR(key, IV, message)
