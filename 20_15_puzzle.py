#!/usr/bin/env python3
import sys
from copy import deepcopy
import heapq
__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def not_empty(self):
        return bool(self._queue)


class Grid:
    def __init__(self):
        self.tiles = [j for j in range(16)]
        self.empty = 15

    @classmethod
    def from_input(cls):
        instance = cls()
        for i in range(4):
            line = input().split(" ")
            try:
                x_index = line.index("X")
                line[x_index] = 16
                instance.empty = i*4 + x_index
            except ValueError:
                pass
            instance.tiles[i*4:(i+1)*4] = list(map(lambda x: int(x) - 1, line))
        return instance

    def solved(self):
        for i in range(len(self.tiles)):
            if self.tiles[i] != i:
                return False
        return True

    def valid_moves(self):
        valid = []
        if self.empty > 3:
            valid.append(0)
        if self.empty < 12:
            valid.append(2)
        if self.empty % 4 != 0:
            valid.append(3)
        if self.empty % 4 != 3:
            valid.append(1)
        return valid

    def _switch(self, index):
        self.tiles[self.empty], self.tiles[index] = self.tiles[index], self.tiles[self.empty]
        self.empty = index

    def apply_move(self, move):
        if move == 1:
            self._switch(self.empty + 1)
        elif move == 3:
            self._switch(self.empty - 1)
        elif move == 0:
            self._switch(self.empty - 4)
        elif move == 2:
            self._switch(self.empty + 4)

    def nb_inversions(self):
        return sum(self._inversion_of_n(i) for i in range(1, 15))

    def check_solvable(self):
        n = self.nb_inversions() + (self.empty//4) + 1
        return bool(n % 2 == 0)

    def _inversion_of_n(self, n):
        inv = 0
        i = self.tiles.index(n)
        for j in range(i + 1, 16):
            if self.tiles[j] < n:
                inv += 1
        return inv


class Solverstate:
    def __init__(self, grid):
        self.grid = grid
        self.steps = []

    @classmethod
    def from_previous(cls, solverstate, move):
        instance = deepcopy(solverstate)
        instance.grid.apply_move(move)
        instance.steps.append(move)
        return instance

    def get_value(self):
        return len(self.steps) + self.grid.nb_inversions()


def solve(grid):
    queue = PriorityQueue()
    initial = Solverstate(grid)
    queue.push(initial, initial.get_value())

    while queue.not_empty:
        state = queue.pop()

        if state.grid.solved():
            return state.steps

        moves = state.grid.valid_moves()

        for move in moves:
            next_state = Solverstate.from_previous(state, move)
            queue.push(next_state, next_state.get_value())


def main():

    if DEBUG:
        sys.stdin = open("samples/20.1_input.txt")

    n = int(input())
    for i in range(n):
        grid = Grid.from_input()
        steps = solve(grid)
        print(len(steps))


if __name__ == "__main__":
    main()
