#!/usr/bin/env python3

"""
--- Day 15: Dueling Generators ---
"""


A = 699
B = 124

TEST_A = 65
TEST_B = 8921

A_FACTOR = 16807
B_FACTOR = 48271

MERSENNE_8 = 2147483647


def generator(num, factor, multiplier=None):
    """ simple generator of the next number, common for A and B """
    while True:
        num = (num * factor) % MERSENNE_8
        if multiplier is None or num % multiplier == 0:
            yield num


def judge(times, multipliers=None):
    """ judge 40M times and look for common cases. """
    if multipliers is None:  # part 1
        gen_a = generator(A, A_FACTOR)
        gen_b = generator(B, B_FACTOR)
    else:  # part 2
        mul_a, mul_b = multipliers
        gen_a = generator(A, A_FACTOR, mul_a)
        gen_b = generator(B, B_FACTOR, mul_b)

    # counter = sum(1 for _ in range(times) if next(gen_a) & 0xffff == next(gen_b) & 0xffff)
    # actually, True == 1, so:
    counter = sum(next(gen_a) & 0xffff == next(gen_b) & 0xffff for _ in range(times))
    return counter


def main():
    """ Calculate the puzzle """
    # Part 1
    result = judge(times=40000000)
    print("Judge found {} pairs after 40M iterations.".format(result))

    # Part 2
    result = judge(times=5000000, multipliers=(4, 8))
    print("Judge found {} pairs after 5M iterations.".format(result))

    return


if __name__ == '__main__':
    main()
