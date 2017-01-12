#!/usr/bin/env python3
import sys
import operator
from functools import reduce

__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False


def ncr(n, r):
    r = min(r, n-r)
    if r == 0:
        return 1
    numerator = reduce(operator.mul, range(n, n-r, -1))
    denominator = reduce(operator.mul, range(1, r+1))
    return numerator//denominator


def main():

    if DEBUG:
        sys.stdin = open("samples/17.1_input.txt")

    n = int(input())
    sizes = []
    for _ in range(n):
        # format is INT x INT, parse this:
        size = list(map(int, [x.strip() for x in input().split("x")]))
        # sanity check
        if len(size) != 2 or size[0] != size[1]:
            raise RuntimeError("invalid input")
        sizes.append(size[0])

    for n in sizes:
        print(ncr(2*n, n)//(n+1))


if __name__ == "__main__":
    main()
