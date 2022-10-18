#!/usr/bin/env python
"""A relatively simple implementation of Kuznyechik cypher"""

import argparse
from kuznyechik import ctr
from kuznyechik.base import gen_key
import sys


def hex_int(x):
    return int(x, 16)


parser = argparse.ArgumentParser(description="Kuznyechik cypher encryption")
parser.add_argument(
    '--in',
    dest='infile',
    type=argparse.FileType('r'),
    default=sys.stdin,
    help='the input file',
)
parser.add_argument(
    '--out',
    dest='outfile',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='the output file',
)
parser.add_argument(
    '--key',
    type=hex_int,
    default=None,
    help='the key for the encription algorithm',
)
parser.add_argument(
    '--iv',
    type=hex_int,
    default=None,
    help='the IV key for the decription algorithm',
)
parser.add_argument(
    '--decrypt',
    action='store_true',
    help='decrypt the message instead of encoding it',
)


def main():
    args = parser.parse_args()
    if args.decrypt:
        if args.key is None:
            print('You must provide the key')
            sys.exit(1)
        if args.iv is None:
            print('You must provide the IV key')
            sys.exit(1)

    msg = args.infile.buffer.read()
    if args.decrypt:
        out = ctr.decrypt(args.key, args.iv, msg)
    else:
        if args.key is None:
            KEY = gen_key()
            print(f"KEY = {hex(KEY)[2:]}")
        else:
            KEY = args.key
        IV, out = ctr.encrypt(KEY, msg)
        print(f"IV = {hex(IV)[2:]}")
    args.outfile.buffer.write(out)


if __name__ == "__main__":
    main()
