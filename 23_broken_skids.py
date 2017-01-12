#!/usr/bin/env python3
import sys

__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False


class Grid:
    def __init__(self):
        self.width = 0
        self.lines = []

    def add_line(self, line):
        # add line without whitespaces at end
        self.lines.append(line.rstrip())
        if len(self.lines[-1]) > self.width:
            self.width = len(self.lines[-1])

    def check(self):
        if self.width == 0:
            return True
        # check how big the gap is
        first_col = self._get_col(0)
        gap = Grid._get_gap(first_col)
        if gap is False:
            return False

        # check if gap is of equal size in every column
        for c in range(1, self.width):
            g = Grid._get_gap(self._get_col(c))
            if g is False:
                return False
            if g != gap:
                return False

        return True

    @staticmethod
    def _get_gap(col_vec):
        empty = [i for i, x in enumerate(col_vec) if x is False]
        if len(empty) > 0:
            # check if gap is contiguous
            begin = empty[0]
            for e in range(1, len(empty)):
                if empty[e] != begin + e:
                    return False

        return len(empty)

    def _get_col(self, c):
        col = []
        for l in self.lines:
            if len(l) > c:
                col.append(True if l[c] is '#' else False)
            else:
                col.append(False)
        return col


def main():
    if DEBUG:
        sys.stdin = open("samples/23.2_input.txt")

    n = int(input())
    for i in range(n):
        grid = Grid()
        nb_l = int(input())
        for l in range(nb_l):
            grid.add_line(input())

        if grid.check():
            print("Ja")
        else:
            print("Nein")


if __name__ == "__main__":
    main()
