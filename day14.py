#!/usr/bin/env python3

"""
--- Day 14: Disk Defragmentation ---
"""

from day10 import Hash


TEST_INPUT = 'flqrgnkx'
INPUT = 'stpzcrnm'

#         north,   south,  west,    east
SIDES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

test_matrix = [[1, 0, 1, 1, 1, 0, 1],
               [1, 1, 0, 1, 1, 0, 0],
               [1, 0, 1, 0, 0, 0, 1],
               [0, 1, 1, 1, 1, 0, 1]]


def get_input():
    """ Return the input code """
    # return TEST_INPUT
    return INPUT


def build_matrix(input_code):
    """ return the 2d matrix of ones and zeros from the hex numbers """
    h = Hash()
    hash_matrix = []
    for x in range(128):
        input_string = str(input_code) + '-' + str(x)
        hash = []
        for ch in h.dense_hash(input_string):
            binary = format(int(ch, 16), '#010b')[2:]
            hash += [int(x) for x in binary[4:]]
        hash_matrix += [hash]
    return hash_matrix


def count_ones(matrix):
    """ Sum of 2d array. Takes advantage of True == 1 """
    return sum(sum(x) for x in matrix)


def print_matrix(matrix):
    """ prints # for each 1, dot for each 0 """
    print('-'*(len(matrix)+4))
    for line in matrix:
        print('| ', end='')
        for ch in line:
            char = '#' if ch == 1 else '.'
            print(char, end='')
        print(' |')
    print('-'*(len(matrix)+4))


def within_range(matrix, cell):
    """ assumes non-zero length matrix """
    x, y = cell
    return 0 <= x < len(matrix) and 0 <= y < len(matrix[0])


def fill_region(matrix, cell, fill=-1):
    """ Fill the entire region in @matrix around the @cell with the provided
    @fill value. """
    x, y = cell
    if matrix[x][y] <= 0:  # already filled or not in region:
        return matrix

    stack = {(x, y)}
    while stack:
        x, y = stack.pop()
        matrix[x][y] = fill
        for dx, dy in SIDES:
            if within_range(matrix, (x+dx, y+dy)) and matrix[x+dx][y+dy] > 0:
                    stack.add(tuple([x+dx, y+dy]))

    return matrix


def count_regions(matrix):
    """ Count the regions connected through sides. """
    counter = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            ch = matrix[i][j]
            if ch <= 0:
                continue
            matrix = fill_region(matrix, (i, j))
            counter += 1
    return counter


def main():
    """ Calculate the puzzle """
    # Part 1, count the ones:
    hash_matrix = build_matrix(get_input())
    print_matrix(hash_matrix)
    print("Number of ones in the matrix = {}".format(count_ones(hash_matrix)))

    # Part 2, group the ones into regions.
    # Regions are those ones connected through one of four sides.
    num_regions = count_regions(hash_matrix)
    print("The whole array has {} regions.".format(num_regions))


if __name__ == '__main__':
    main()
