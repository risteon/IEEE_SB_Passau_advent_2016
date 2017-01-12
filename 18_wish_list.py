#!/usr/bin/env python3
import sys
import base64
import operator

__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = True


def main():

    if DEBUG:
        sys.stdin = open("samples/18.1_input.txt")

    coded = sys.stdin.read()
    encoded = base64.b64decode(coded)
    print(encoded)
    print(len(encoded))

    data = None
    with open("samples/18.1_devel.txt", "r") as dev:
        data = dev.read()

    data = bytes(data, 'utf-8')
    print(data)

    stream = bytes(map(operator.xor, data[0:16], encoded[0:16]))
    print(stream)

    print(base64.b64encode(stream))

    # d3c1b4a48652b8d3b0bacc62fb891114

if __name__ == "__main__":
    main()
