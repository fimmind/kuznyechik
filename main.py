#!/usr/bin/env python
"""A relatively simple implementation of Kuznyechik cypher"""

from kuznyechik import encript_block, decript_block, expand_key


def main():
    KEY = 0x8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef
    K = expand_key(KEY)
    msg = 0x1122334455667700ffeeddccbbaa9988
    enc_msg = encript_block(K, msg)
    dec_msg = decript_block(K, enc_msg)

    for i in [msg, enc_msg, dec_msg]:
        print(hex(i))


if __name__ == "__main__":
    main()
