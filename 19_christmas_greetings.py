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
        return sequence

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
        sys.stdin = open("samples/19.1_input.txt")

    n = int(input())
    for i in range(n):
        graph = Graph()

        p, x = map(int, input().split(" "))
        connections = input().split(";")
        for c in connections:
            nodes = c.split(" ")
            if len(nodes) is not 2:
                raise RuntimeError("Invalid input")

            graph.set_undirected_edge(nodes[0], nodes[1], 1)

        diameter = graph.diameter()
        if diameter is None:
            print("Nicht verbunden")
        else:
            print(diameter)


if __name__ == "__main__":
    main()
