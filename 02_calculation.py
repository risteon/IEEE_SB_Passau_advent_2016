#!/usr/bin/env python3
from enum import Enum

__author__ = "Christoph Rist"


class Operator(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    NEG = 4
    MOD = 5
    LSHIFT = 6
    RSHIFT = 7
    AND = 8
    OR = 9
    COMP = 10
    XOR = 11
    OPERATOR_COUNT = 12


OP_DICT = {
  "add" : Operator.ADD,
  "sub" : Operator.SUB,
  "mul" : Operator.MUL,
  "div" : Operator.DIV,
  "neg" : Operator.NEG,
  "mod" : Operator.MOD,
  "lshift" : Operator.LSHIFT,
  "rshift" : Operator.RSHIFT,
  "and" : Operator.AND,
  "or" : Operator.OR,
  "comp" : Operator.COMP,
  "xor" : Operator.XOR
}


def get_operation_operand_count(op):
    if op == Operator.OPERATOR_COUNT:
        raise RuntimeError("Invalid use.")
    elif op == Operator.NEG or op == Operator.COMP:
        return 1
    else:
        return 2


def calculate(operator, op_stack):
    nb_operands = get_operation_operand_count(operator)
    # sanity check
    if nb_operands > len(op_stack):
        raise RuntimeError("Invalid expression: not enough operands.")

    # op list from stack
    op = op_stack[-nb_operands:]
    # remove from stack
    for i in range(nb_operands):
        op_stack.pop()

    if operator == Operator.ADD:
        return op[0] + op[1]
    if operator == Operator.SUB:
        return op[0] - op[1]
    if operator == Operator.MUL:
        return op[0] * op[1]
    if operator == Operator.DIV:
        return op[0] // op[1]
    if operator == Operator.NEG:
        return -op[0]
    if operator == Operator.MOD:
        return op[0] % op[1]
    if operator == Operator.LSHIFT:
        return op[0] << op[1]
    if operator == Operator.RSHIFT:
        return op[0] >> op[1]
    if operator == Operator.AND:
        return op[0] & op[1]
    if operator == Operator.OR:
        return op[0] | op[1]
    if operator == Operator.COMP:
        return ~op[0]
    if operator == Operator.XOR:
        return op[0] ^ op[1]

    raise RuntimeError("Invalid operator.")


class Op:
    """Hold either an operand or an operator. Parse from input string."""
    def __init__(self, str):
        try:
            self._operand = int(str)
            self._operator = Operator.OPERATOR_COUNT
        except ValueError:
            if str not in OP_DICT:
                raise RuntimeError("Unknown operator")
            self._operator = OP_DICT[str]

    def is_operand(self):
        return bool(self._operator == Operator.OPERATOR_COUNT)

    def get(self):
        return self._operand

    def get_operator(self):
        return self._operator


def get_result(strs):
    ops = [Op(s) for s in strs]
    stack = []

    for o in ops:
        if o.is_operand():
            stack.append(o.get())
        else:
            stack.append(calculate(o.get_operator(), stack))
    return stack[0]


def main():
    line = str(input())
    strs = line.split(" ")
    print(get_result(strs))


if __name__ == "__main__":
    main()

