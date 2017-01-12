#!/usr/bin/env python3
import sys
from collections import namedtuple

__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False

Vec3 = namedtuple("vec3", ['x', 'y', 'z'])


class Vector3D(Vec3):
    def __new__(cls, x=0.0, y=0.0, z=0.0):
        self = super(Vector3D, cls).__new__(cls, x=x, y=y, z=z)
        return self

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y and other.z == self.z

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        return Vector3D(self.x * other, self.y * other, self.z * other)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


REINDEERS = {
    'Dasher': (Vector3D(0.0, -1.0, 0.0), 0.05),
    'Dancer': (Vector3D(2.0, 0.0, 0.0), 0.01),
    'Prancer': (Vector3D(0.0, 0.0, 0.7), 0.01*11),
    'Vixen': (Vector3D(-1.0, -0.1, 0.0), 0.042),
    'Comet': (Vector3D(0.0, 0.3, -0.1), 0.18),
    'Cupid': (Vector3D(0.0, 0.0, 0.0), 0.5),
    'Dunder': (Vector3D(0.1, -0.1, -0.1), 0.07),
    'Blixem': (Vector3D(-0.4, 0.0, 0.4), 0.03)
}


class Reindeer:
    def __init__(self, name, fitness):
        if name not in REINDEERS:
            raise RuntimeError("Unknown reindeer")
        self.dir = REINDEERS[name][0]
        self.consumption = REINDEERS[name][1]
        self.fitness = fitness
        self.f = fitness

    def reset(self):
        self.f = self.fitness

    def update_fitness(self):
        self.f -= self.consumption
        if self.f < 0.0:
            self.f = 0.0

    def get_direction(self):
        return self.dir * (2.0 - self.f)


def evaluate(reindeers, start, nb_steps):
    for r in reindeers:
        r.reset()
    pos = start
    crash = abs(pos[0]) > 10 or abs(pos[1]) > 10 or abs(pos[2]) > 10
    for _ in range(nb_steps):
        for r in reindeers:
            pos += r.get_direction()
        for r in reindeers:
            r.update_fitness()

        crash = abs(pos[0]) > 10 or abs(pos[1]) > 10 or abs(pos[2]) > 10
        if crash:
            break

    return not crash, pos


def main():

    if DEBUG:
        sys.stdin = open("samples/14.1_input.txt")

    nb_reindeers, nb_testcases = map(int, input().split(" "))
    # read reindeers
    reindeers = []
    for _ in range(nb_reindeers):
        name, fitness = input().split(" ")
        reindeers.append(Reindeer(name, float(fitness)))

    for _ in range(nb_testcases):
        inp = list(map(int, filter(None, input().split(" "))))
        works, pos = evaluate(reindeers, Vector3D(*inp[0:3]), inp[3])
        if works:
            print("Works")
            print("{:.2f} {:.2f} {:.2f}".format(pos[0], pos[1], pos[2]))
        else:
            print("Crash")
            print("{:.5f} {:.5f} {:.5f}".format(pos[0], pos[1], pos[2]))


if __name__ == "__main__":
    main()
