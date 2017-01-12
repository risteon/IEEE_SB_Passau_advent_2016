#!/usr/bin/env python3
import sys
from collections import namedtuple
from operator import itemgetter
import math


__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = True

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


class Sphere:
    def __init__(self, pos, radius, color):
        self.pos = pos
        self.radius = radius
        self.color = color


class Canvas:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.spheres = []

        self.cam_pos = Vector3D(0.0, 0.0, 0.0)
        self.top_left = Vector3D(-1.0, 1.0, 1.0)
        self.bottom_right = Vector3D(1.0, -1.0, 1.0)

        self.pixels = []

    def add_sphere(self, sphere):
        self.spheres.append(sphere)

    def render(self):
        # input check
        if self.width == 0 or self.height == 0:
            return
        # calculate pixel positions
        diff = self.bottom_right - self.top_left
        px_right = Vector3D(diff.x/self.width, 0.0, diff.z/self.width)
        px_down = Vector3D(0.0, diff.y / self.height, 0.0)
        px_shift = Vector3D(diff.x / self.width / 2, diff.y / self.height / 2, 0.0)
        # add rendered pixels
        for y in range(self.height):
            for x in range(self.width):
                px = self.top_left + px_right * x + px_down * y + px_shift
                self.pixels.append(self._get_color_for_pixel(px))

    def print(self):
        for row in range(self.height):
            print("".join(self.pixels[row * self.width: (row + 1) * self.width]))

    def _get_color_for_pixel(self, px):
        direction = px - self.cam_pos
        intersections = []
        for sp in self.spheres:
            t, char = self._get_first_intersection_with_sphere(self.cam_pos, direction, sp)
            intersections.append((t, char))

        if not intersections:
            return "."

        _, char = min(intersections, key=itemgetter(0))
        return char

    @staticmethod
    def _get_first_intersection_with_sphere(cam_pos, direction, sphere):

        p = cam_pos - sphere.pos
        # solve quadratic equation
        a = direction.dot(direction)
        b = 2 * direction.dot(p)
        c = p.dot(p) - (sphere.radius * sphere.radius)

        # radicand
        radicand = b*b - 4*a*c
        if radicand < 0:
            # math.inf since python3.5, just use a really big floating point number
            return 1e40, "."

        t_1 = (-b + math.sqrt(radicand)) / (2*a)
        t_2 = (-b - math.sqrt(radicand)) / (2*a)

        return min(t_1, t_2), sphere.color


def main():

    if DEBUG:
        sys.stdin = open("samples/10.1_input.txt")

    nb_spheres = int(input())
    h, w = map(int, input().split(" "))

    canvas = Canvas(h, w)

    for i in range(nb_spheres):
        desc = input().split(" ")
        desc = list(filter(None, desc))
        pos = Vector3D(*map(float, desc[0:3]))
        radius = float(desc[3])
        s = Sphere(pos, radius, desc[4])
        canvas.add_sphere(s)

    canvas.render()
    canvas.print()

if __name__ == "__main__":
    main()
