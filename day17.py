#!/usr/bin/env python3

"""
--- Day 17: Spinlock

Creates a list with 50M elements. Run with pypy if possible.
"""


from blist import blist


def solve(spins, result_is_after, step=354):
    """ Solve the spinlock puzzle. """
    nums = blist([0])
    pos = 0
    for i in range(1, spins):
        pos = (pos + step) % i + 1
        nums.insert(pos, i)

    return nums[nums.index(result_is_after)+1]


def main():
    """ Calculate the puzzle """
    # Part 1
    result = solve(spins=2018, result_is_after=2017)
    print("2018'th value is {}.".format(result))

    # Part 2
    result = solve(spins=50000001, result_is_after=0)
    print("Value after 50M spins is {}.".format(result))

    return


if __name__ == '__main__':
    main()
