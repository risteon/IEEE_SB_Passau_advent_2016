#!/usr/bin/env python3
import sys
from copy import deepcopy
import heapq
__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False


class Landmark:
    def __init__(self, km, kind, arg=None):
        self.km = km
        self.kind = kind
        self.arg = arg

    def update_consumption(self, consumption):
        if self.kind == "Verbrauch":
            consumption = int(self.arg), consumption[1]
        elif self.kind == "Leck":
            consumption = consumption[0], consumption[1] + 0.5
        elif self.kind == "Werkstatt":
            consumption = consumption[0], 0
        return consumption


def main():

    if DEBUG:
        sys.stdin = open("samples/22.1_input.txt")

    n = int(input())
    for _ in range(n):
        k = int(input())
        landmarks = []
        for e in range(k):
            info = list(filter(None, input().split(" ")))
            info[1] = int(info[1][:-1])
            landmarks.append(Landmark(*info[1:]))

        consumption = (0, 0.0)
        current_con = 0.0
        max_con = 0
        km = 0

        for l in landmarks:
            diff = l.km - km
            current_con += (consumption[0] + consumption[1]) * diff

            if l.kind == "Tankstelle" or l.kind == "Huette":
                if current_con > max_con:
                    max_con = current_con
                    current_con = 0

            km = l.km
            consumption = l.update_consumption(consumption)

        print("{:.1f}".format(max_con))


if __name__ == "__main__":
    main()
