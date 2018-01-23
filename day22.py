#!/usr/bin/env python3

"""
--- Day 22: Sporifica Virus ---
(A Langton ant variation)
"""

from collections import namedtuple

Rule = namedtuple('Rule', 'before after')

INPUT_FILE = 'input_day22.txt'
TEST_INPUT = """
..#
#..
..."""


class Dir: up, right, down, left = range(4)


class State: clean, weakened, infected, flagged = range(4)


directions = [Dir.up, Dir.right, Dir.down, Dir.left]


def get_input():
    """ Read the input.
    """
    # return TEST_INPUT.strip().split('\n')
    with open(INPUT_FILE) as f:
        return f.readlines()


def parse_input(lines):
    """ return the virtual matrix that sort-of looks like an input.
    Using the sparse array for this only, as I am betting we'll need like 5M
    cells for the second part.
    So the sparse array represented as a set(x,y)
    """
    matrix = set()
    for x, line in enumerate(lines):
        for y, val in enumerate(line):
            if val == '#':
                matrix.add((x, y))

    return matrix


def build_matrix_map(lines):
    """ Similar to parse input, but returns a map of (x,y) -> value instead of
    just a set of positions. This is because we now need 4 bits of info instead
    of just one. """
    matrix = {}
    for x, line in enumerate(lines):
        for y, val in enumerate(line):
            if val == '#':
                matrix[(x, y)] = State.infected
    return matrix


def infect(matrix, steps):
    """ run the @times iterations of infection algorithm on @matrix.
    each step:
    * infected => go right; else => go left.
    * flip the switch.
    * carry on with direction.
    """
    x = 12
    y = 12
    dir = Dir.up
    infected = 0
    for i in range(steps):
        if (x, y) in matrix:
            turn_right = True
            matrix.remove((x, y))
        else:
            turn_right = False
            matrix.add((x, y))
            infected += 1

        dir = (4 + dir + (1 if turn_right else -1)) % 4
        dir = directions[dir]
        if dir == Dir.up:
            x -= 1
        elif dir == Dir.right:
            y += 1
        elif dir == Dir.down:
            x += 1
        elif dir == Dir.left:
            y -= 1
        else:
            assert False

    return infected


def infect_sophisticatedly(matrix, steps):
    """ run the @times iterations of infection algorithm on @matrix.
    each step:
    * infected => go right; else => go left.
    * flip the switch.
    * carry on with direction.
    """
    x = 12
    y = 12
    dir = Dir.up
    infected = 0
    for i in range(steps):
        pos = (x, y)
        if pos in matrix.keys():
            if matrix[pos] == State.flagged:
                matrix.pop(pos)
            else:
                matrix[pos] += 1
                infected += matrix[pos] == State.infected
        else:
            matrix[pos] = 1

        dir = (2 + dir + matrix.get(pos, 0)) % 4
        dir = directions[dir]
        if dir == Dir.up:
            x -= 1
        elif dir == Dir.right:
            y += 1
        elif dir == Dir.down:
            x += 1
        elif dir == Dir.left:
            y -= 1
        else:
            assert False

    return infected


def main():
    """ Parse the image and match the rules """

    matrix = parse_input(get_input())
    infected = infect(matrix, steps=10000)
    print("Infected cells: {}.".format(infected))

    matrix = build_matrix_map(get_input())
    infected_2 = infect_sophisticatedly(matrix, steps=10000000)
    print("Infected cells 2: {}.".format(infected_2))

    return


if __name__ == '__main__':
    main()
