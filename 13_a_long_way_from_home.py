#!/usr/bin/env python3
import re   # regex to find all integers in string
from sys import maxsize

__author__ = "Christoph Rist"
__license__ = "MIT"


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
        return sequence


def main():
    # read input
    k, e, q = map(int, input().split(" "))

    graph = Graph()
    # build graph
    for i in range(e):
        # read all integers from input line
        g = input().split(" ")
        s = g[0].split("->")
        s.append(g[1])
        values = list(map(int, s))
        if len(values) is not 3:
            raise RuntimeError("Invalid input")
        graph.set_edge(values[0], values[1], values[2])

    # search shortest paths
    for i in range(q):
        # read two space-separated integers
        values = list(map(int, input().split(" ")))
        if len(values) is not 2:
            raise RuntimeError("Invalid input")

        route = graph.shortest_route(values[0], values[1])
        print(*route, sep=' -> ')


if __name__ == "__main__":
    main()
