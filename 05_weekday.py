#!/usr/bin/env python3

import datetime
from sys import stdin

__author__      = "Christoph Rist"

# Solve this problem most fast, easy and error-proof
# by making use of built-in standard library functionality.
# ... don't reinvent the wheel ...
 

WEEKDAY_NAMES = {
        0: "Montag",
        1: "Dienstag",
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag"
}

def main():
    lines = stdin.readlines();
    nb_cases = int(lines[0])
    for i in range(1, nb_cases + 1):
        n = lines[i].split(" ")
        yyyy = int(n[0])
        mm = int(n[1])
        dd = int(n[2])
        while yyyy < 1:
            yyyy += 400

        d = datetime.datetime(yyyy, mm, dd)
        print(WEEKDAY_NAMES[d.weekday()])


if __name__ == "__main__":
    main()

