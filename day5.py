#!/usr/bin/env python3

"""
--- Day 5: A Maze of Twisty Trampolines, All Alike ---
"""

input_file = 'input_day5.txt'


def get_input():
    # test input:
    # return [0, 3, 0, 1, -3]

    with open(input_file, 'r') as f:
        return f.readlines()


def out_of_range(index, size):
    return index < 0 or index >= size


def compute(part=1):
    """ go through, instruction by instruction. """
    instrs = [int(x) for x in get_input()]
    pc = 0
    counter = 0
    while not out_of_range(pc, len(instrs)):
        # execute:
        old_pc = pc
        pc += instrs[pc]
        if part == 1:
            instrs[old_pc] += 1
        else:
            instrs[old_pc] += 1 if instrs[old_pc] < 3 else -1
        counter += 1

        # increment old value
    return counter


def main():
    result = compute(part=1)
    print("Part 1: {}".format(result))

    result2 = compute(part=2)
    print("Part 2: {}".format(result2))

    return


if __name__ == '__main__':
    main()


