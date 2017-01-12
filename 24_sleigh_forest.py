#!/usr/bin/env python3
from sys import maxsize
import sys
from itertools import combinations


__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = []

    def set_edge(self, start, end, weight):
        self.add_node(start)
        self.add_node(end)

        if (start, end) not in self.edges:
            self.nodes[start].append(end)
        self.edges[start, end] = weight

    def set_undirected_edge(self, first_node, second_node, weight):
        self.set_edge(first_node, second_node, weight)
        self.set_edge(second_node, first_node, weight)

    def shortest_route(self, start, end):
        if start not in self.nodes or end not in self.nodes:
            return None

        previous = {}
        unvisited = set(self.nodes.keys())
        distance = {n: maxsize for n in unvisited}

        distance[start] = 0

        while unvisited:
            u = min(unvisited, key=distance.get)
            if distance[u] == maxsize:
                return None
            if u == end:
                break
            unvisited.remove(u)

            for neighbor in self.nodes[u]:
                if neighbor not in unvisited:
                    continue

                d = distance[u] + self.edges[u, neighbor]
                if neighbor not in distance or d < distance[neighbor]:
                    distance[neighbor] = d
                    previous[neighbor] = u

        sequence = [end]
        u = end
        while u in previous:
            u = previous[u]
            sequence.append(u)
        sequence.reverse()
        return sequence, distance[end]

    def diameter(self):
        # find shortest path for every pair of nodes
        # currently assume an undirected graph!
        max_len = 0
        for pair in combinations(self.nodes, 2):
            seq = self.shortest_route(pair[0], pair[1])
            if seq is None:
                break
            if len(seq) - 1 > max_len:
                max_len = len(seq) - 1
        else:
            return max_len
        return None


def main():

    if DEBUG:
        sys.stdin = open("samples/24.1_input.txt")

    input_str = sys.stdin.read()
    lines = input_str.split("\n")
    lines.pop()

    grid = []

    for l in lines:
        grid.append(list(map(int, l.split("|"))))

    # check that all grid lines have the same number of elements
    width = len(grid[0])
    if not all(width == len(x) for x in grid):
        raise RuntimeError("Invalid input")

    # build a standard, undirected graph, using mean of two nodes as edge weights
    # additional start and end nodes are inserted
    # then solve problem using standard graph functionality
    graph = Graph()

    def add_edge(g, a, b):
        weight = grid[a[0]][a[1]] + grid[b[0]][b[1]]
        g.set_undirected_edge(a, b, weight)

    for row in range(len(grid) - 1):
        for col in range(len(grid[0]) - 1):
            first = row, col
            to_right = row, col + 1
            to_bottom = row + 1, col
            add_edge(graph, first, to_right)
            add_edge(graph, first, to_bottom)


    # last row:
    for col in range(len(grid[0]) - 1):
        first = len(grid) - 1, col
        second = len(grid) - 1, col + 1
        add_edge(graph, first, second)

    # last col
    for row in range(len(grid) - 1):
        first = row, len(grid[0]) - 1
        second = row + 1, len(grid[0]) - 1
        add_edge(graph, first, second)

    # start node (-1, 0)
    graph.set_undirected_edge((-1, 0), (0, 0), grid[0][0])
    # end node (0, -1)
    graph.set_undirected_edge((0, -1), (len(grid)-1, len(grid[0])-1), grid[-1][-1])

    # find path
    seq, dist = graph.shortest_route((-1, 0), (0, -1))
    # discard virtual start and end nodes
    seq = seq[1:-1]
    # build sequence of tree numbers
    trees = [grid[row][col] for row, col in seq]
    # print as specified
    print("{} : ".format(dist//2), end="")
    print(*trees, sep=" -> ")


if __name__ == "__main__":
    main()
