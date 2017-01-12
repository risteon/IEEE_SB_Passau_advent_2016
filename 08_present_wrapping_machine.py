#!/usr/bin/env python3
from itertools import groupby

__author__ = "Christoph Rist"
__license__ = "MIT"


DIST_TOP = 200
DIST_LEFT = 250
DIST_RIGHT = 250


class Present:
    def __init__(self):
        self.length = None
        self.width_begin = None
        self.width_end = None
        self.height_begin = None
        self.height_end = None

    def volume(self):
        w1, w2 = self.width_begin, self.width_end
        h1, h2 = self.height_begin, self.height_end
        return self.length * (h1*w1/3 + h1*w2/2 - h1*w2/3 + h2*w1/2 - h2*w1/3 + h2*w2/3)


def parse_object(top, sideward):
    ob = Present()
    ob.length = len(top)
    ob.width_begin = sideward[0]
    ob.width_end = sideward[-1]
    ob.height_begin = DIST_TOP - top[0]
    ob.height_end = DIST_TOP - top[-1]

    if False and ob.length > 2:
        d_h = top[1] - top[0]
        d_w = sideward[1] - sideward[0]

        for i in range(1, len(top) - 1):
            if top[i+1] - top[i] != d_h:
                raise ValueError("test")
            if sideward[i+1] - sideward[i] != d_w:
                raise ValueError("test")
    return ob


def split(iterable, splitters):
    return [list(g) for k, g in groupby(iterable, lambda x: x in splitters) if not k]


def main():
    # read input
    frequency, speed, nb_samples = map(int, input().split(" "))
    # not sure if this can happen...
    if nb_samples == 0:
        print("0")
        return
    # the three sensor lines
    a = input().split(" ")
    b = input().split(" ")
    c = input().split(" ")
    # Lines ending in spaces and multiple spaces in between are not specified and consume way to much time to debug!
    # remove all empty strings
    a = filter(None, a)
    b = filter(None, b)
    c = filter(None, c)

    # integer lists
    top = list(map(int, a))
    left = list(map(int, b))
    right = list(map(int, c))

    # sanity check input
    # ... number of samples
    # THIS CONDITION DOES NOT HOLD IN TESTCASE 5.
    #if len(top) != nb_samples or len(left) != nb_samples or len(right) != nb_samples:
    #    raise RuntimeError("Invalid number of input samples")

    # ... no object detected: all three values -1, or no value -1
    for x in zip(top, left, right):
        if -1 in x and (x[0] != -1 or x[1] != -1 or x[2] != -1):
            raise RuntimeError("Invalid input")

    # max sensor values
    if max(top) > DIST_TOP or max(left) > DIST_LEFT + DIST_RIGHT or max(right) > DIST_LEFT + DIST_RIGHT:
        raise RuntimeError("Invalid value for sensor")

    # calculate object width
    sideward = list(map(lambda l, r: DIST_LEFT + DIST_RIGHT - l - r, left, right))

    # split at -1
    top_split = split(top, (-1,))
    sideward_split = split(sideward, (DIST_LEFT + DIST_RIGHT + 2,))

    # create objects
    objects = [parse_object(t, s) for t, s in zip(top_split, sideward_split)]

    # "rounding" in this task seems to be defined as cutting away decimal places... *sigh* ...
    volumes = [int(o.volume()) for o in objects]
    print(len(objects), end="")
    if volumes:
        print(" ", end="")
        print(*volumes, sep=" ")
    else:
        print("")


if __name__ == "__main__":
    main()
