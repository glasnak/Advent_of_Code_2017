#!/usr/bin/env python3

"""
--- Day 23: Coprocessor Conflagration ---
"""

from day18 import Interpreter
import math


INPUT_FILE = 'input_day23.txt'


def get_input():
    """ return the input instructions """
    with open(INPUT_FILE) as f:
        return f.readlines()


def parse_input(lines):
    """ parse input. """
    instrs = []
    for line in lines:
        instr = line.strip().split(' ')
        instrs.append((instr[0], instr[1:]))

    return instrs


def is_prime(a):
    """ true if a is prime """
    return all(a % i for i in range(2, int(math.sqrt(a))))


def main():
    """ run the puzzle of day 23. """

    instrs = parse_input(get_input())
    interpreter = Interpreter()
    results = interpreter.run23(instrs)

    print("mul times =", results)

    # This would take years to finish:
    # instrs = parse_input(get_input())
    # interpreter = Interpreter()
    # results = interpreter.run23_2(instrs)

    # actually, slowly transforming the code until I understood it, all it does
    # is that it finds number of composite numbers between 108100 and 125100.
    # Easy one-liner even in python after transforming it into C solution and
    # actually understanding it:
    result = len([num for num in range(108100, 125101, 17) if not is_prime(num)])
    print("Num of composites =", result)

    return 0


if __name__ == '__main__':
    main()
