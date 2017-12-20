#!/usr/bin/env python3

"""
--- Day 2: Corruption Checksum ---
"""

input_file = 'input_day2.txt'


def get_input():
    with open(input_file, 'r') as f:
        return f.readlines()


def parse_input(lines):
    """ parse the string into a matrix """
    matrix = []
    for line in lines:
        line_nums = [int(x) for x in line.split('\t')]
        matrix.append(line_nums)
    return matrix


def compute_checksum(sheet):
    """ main algorithm to do stuff """
    result = 0
    for line in sheet:
        result += max(line) - min(line)
    return result


def compute_divisible_checksum(sheet):
    result = 0
    for line in sheet:
        # PM me a non-ugly way to return both [divisible, by_what]
        bignum = next((i for i in line if any(i != j and i % j == 0 for j in line)), None)
        assert bignum
        line.remove(bignum)
        for x in line:
            if bignum % x == 0:
                result += bignum // x
                continue

    return result


def main():
    sheet = parse_input(get_input())

    result = compute_checksum(sheet)
    print("Checksum 1: {}".format(result))

    result2 = compute_divisible_checksum(sheet)
    print("Checksum 2: {}".format(result2))

    return


if __name__ == '__main__':
    main()


