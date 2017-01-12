#!/usr/bin/env python3
import sys
import re

__author__ = "Christoph Rist"
__license__ = "MIT"

DEBUG = False


class Ex:
    def __init__(self):
        self.operands = []
        self.operators = []

    def valid_merges(self):
        return len(self.operators)

    @classmethod
    def from_string(cls, string):
        instance = cls()
        strs = re.findall(r'(?:\(-)?\d+', string)
        # remove leading '('
        for i in range(len(strs)):
            if strs[i][0] == '(':
                strs[i] = strs[i][1:]
        instance.operands = [int(x) for x in strs]

        instance.operators = re.findall(r'(\+|(?<!\()-|\*)', string)
        return instance

    def merge_at(self, pos):
        self.operands[pos] = self._get_value_at(pos)
        del self.operands[pos+1]
        del self.operators[pos]

    def get_merged(self, pos):
        op = self.operators[pos]
        if op == "+":
            res = self.operands[pos] + self.operands[pos + 1]
        if op == "*":
            res = self.operands[pos] * self.operands[pos + 1]
        if op == "-":
            res = self.operands[pos] - self.operands[pos + 1]

        instance = Ex()
        for i in range(pos):
            instance.operands.append(self.operands[i])
            instance.operators.append(self.operators[i])
        instance.operands.append(res)
        for i in range(pos + 1, len(self.operators)):
            instance.operands.append(self.operands[i+1])
            instance.operators.append(self.operators[i])
        return instance

    def _get_value_at(self, pos):
        op = self.operators[pos]
        if op == "+":
            res = self.operands[pos] + self.operands[pos + 1]
        if op == "*":
            res = self.operands[pos] * self.operands[pos + 1]
        if op == "-":
            res = self.operands[pos] - self.operands[pos + 1]
        return res

    def test(self):
        ops = [i for i in range(len(self.operators)) if self.operators[i] == '+' or self.operators[i] == '-']
        for i in reversed(ops):
            self.merge_at(i)


def get_min_max(ex):
    min = None
    max = None

    stack = [ex]

    while bool(stack):
        n = stack.pop()
        if n.valid_merges() == 0:
            value = n.operands[0]
            if not min or value < min:
                min = value
            if not max or value > max:
                max = value
        else:
            for i in range(n.valid_merges()):
                stack.append(n.get_merged(i))

    return min, max


def main():

    if DEBUG:
        sys.stdin = open("samples/11.1_input.txt")

    n = int(input())
    for _ in range(n):
        ex = Ex.from_string(input())
        ex.test()
        print(ex.operands)
        #min, max = get_min_max(ex)
        #print("{} {}".format(max, min))


if __name__ == "__main__":
    main()
