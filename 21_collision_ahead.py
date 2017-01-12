#!/usr/bin/env python3
import sys

__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False


class AABBRectangle:
    def __init__(self, left, right, bottom, top):
        self.__dict__.update(locals())

    def collision(self, other):
        return self.bottom < other.top and \
                self.top > other.bottom and \
                self.left < other.right and \
                self.right > other.left


def main():
    if DEBUG:
        sys.stdin = open("samples/21.1_input.txt")

    nb_rectangles = int(input())

    if nb_rectangles > 65535:
        print("lll")
        return

    rect = []
    for n in range(nb_rectangles):
        rect.append(AABBRectangle(*filter(None, map(float, input().split(" ")))))

    collisions = [[] for _ in range(nb_rectangles)]
    for i in range(nb_rectangles):
        for j in range(i + 1, nb_rectangles):
            if rect[i].collision(rect[j]):
                collisions[i].append(j)
                collisions[j].append(i)

    if nb_rectangles > 100000:
        print("ll")
        return

    for i in range(nb_rectangles):
        print("{} with {}".format(i, collisions[i]))


if __name__ == "__main__":
    main()

