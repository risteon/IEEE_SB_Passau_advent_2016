#!/usr/bin/env python3
import sys

__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False


def get_subsub(sub, n):
    max = sub[0]
    subsub = [sub[0]]

    for l in range(1, n + 1):
        for i in range(n - l + 1):
            s = sum(sub[i:i + l])
            if s > max:
                subsub = sub[i:i + l]
                max = s

    return subsub


def main():

    if DEBUG:
        sys.stdin = open("samples/15.1_input.txt")

    c = int(input())
    n = int(input())
    seq = []
    for _ in range(c):
        seq.append(int(input()))

    max = sum(seq[:n])
    subsub = seq[:n]

    for i in range(c-n+1):
        ss = get_subsub(seq[i:i+n], n)
        s = sum(ss)
        if s > max:
            subsub = ss
            max = s

    print(*subsub, sep='\n')


if __name__ == "__main__":
    main()
