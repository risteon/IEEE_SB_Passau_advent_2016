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

    def set_undirected_edge(self, first_node, second_node, weight=1):
        self.set_edge(first_node, second_node, weight)
        self.set_edge(second_node, first_node, weight)

    def shortest_route(self, start, end):
        """ Return shortest path between start and end.

        This is a dijkstra implementation.
        """
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

    def nb_simple_paths(self, start, end):
        """ Calculate number of simple path between start and end

        This is a depth-first search
        """
        if start not in self.nodes or end not in self.nodes:
            return None

        visited = set()
        nb_paths = 0

        def search(node, goal):
            nonlocal nb_paths
            visited.add(node)

            if node == goal:
                nb_paths += 1
            else:
                for neighbor in self.nodes[node]:
                    if neighbor not in visited:
                        search(neighbor, goal)

            visited.remove(node)

        search(start, end)
        return nb_paths


def build_graph(size):
    graph = Graph()
    # every non-diagonal x-y-coordinate
    for x in range(1, size):
        for y in range(x):
            graph.set_undirected_edge((x, y), (x - 1, y))
            graph.set_undirected_edge((x, y), (x, y + 1))

    return graph


def main():

    if DEBUG:
        sys.stdin = open("samples/17.1_input.txt")

    n = int(input())
    sizes = []
    for _ in range(n):
        # format is INT x INT, parse this:
        size = list(map(int, [x.strip() for x in input().split("x")]))
        # sanity check
        if len(size) != 2 or size[0] != size[1]:
            raise RuntimeError("invalid input")
        sizes.append(size[0])

    if max(sizes) > 12:
        raise RuntimeError()

    for size in sizes:
        # this seems to be a matter of definition
        if size == 1:
            print(1)
            continue

        graph = build_graph(size)
        print(graph.nb_simple_paths((0, 0), (size - 1, size - 1)) * 2)


if __name__ == "__main__":
    main()
