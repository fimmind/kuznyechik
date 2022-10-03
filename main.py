#!/usr/bin/env python
"""A relatively simple implementation of Kuznyechik cypher"""

from kuznyechik import decrypt_CTR
from kuznyechik import encrypt_CTR
import lorem


def main():
    KEY = 0x8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef

    msg = lorem.paragraph()
    print(f"\nMessage:\n{msg}")

    IV, raw_enc_msg = encrypt_CTR(KEY, msg.encode(encoding='utf'))
    print(f"\nRaw encrypted message:\n{raw_enc_msg}\n")

    raw_dec_msg = decrypt_CTR(KEY, IV, raw_enc_msg)
    print(f"\nRaw decrypted message:\n{raw_dec_msg}\n")

    dec_msg = raw_dec_msg.decode('utf')
    print(f"\nDecoded message:\n{dec_msg}\n"
          f"\nEquals to the original?\n{msg == dec_msg}")


if __name__ == "__main__":
    main()
