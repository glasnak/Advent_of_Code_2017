#!/usr/bin/env python3

import collections
import numpy
import math

Direction = {'north': (0, -1),
             'east': (1, 0),
             'south': (0, 1),
             'west': (-1, 0)
             }

directions = ['east', 'north', 'west', 'south']

Point = collections.namedtuple('Point', 'x y')

input_num = 347991


def move(location, direction):
    """ having a location and a direction, move and return new position. """
    d = Direction[direction]
    return Point(location.x + d[0], location.y + d[1])


def get_next_direction(d):
    return directions[(directions.index(d) + 3) % 4]


def get_prev_direction(d):
    return directions[(directions.index(d) + 1) % 4]


def get_distance(p1, p2):
    """ a distance between two points.  """
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def index_out_of_range(cell, size):
    return cell.x >= size or cell.x < 0 or cell.y >= size or cell.y < 0


def get_next_cell(part=1):
    """ part 1 simply returns 1, part 2 is a bit more complicated."""
    # part 1:
    if part == 1:
        return 1
    # part 2:


def build_spiral(size, next_cell_function):
    """ build a spiral of arbitrary size such as:
        5  4  3
        6  1  2 ...
        7  8  9 10
        that is, if step == zero
    """
    assert size % 2 == 1  # spiral must be a square of odd size, must have a center
    matrix = numpy.zeros((size, size)).astype(int)
    center = Point(size//2, size//2)
    cell = center
    spiral_index = 1  # initial value.
    direction = 'south'  # initial direction (rotation happens on filling initial cell too)
    stepsize = 1  # increment every two steps to create a spiral.
    while not index_out_of_range(cell, size):
        for _i in range(2):
            for _j in range(stepsize):
                if index_out_of_range(cell, size):
                    break
                matrix[cell.x][cell.y] = spiral_index
                cell = move(cell, direction)
                # call a method for calculating next cell value:
                # different num of params, please contact me if you have a nicer solution than try/except
                # the code is so ugly with *args/**kwargs I'm going down this path.
                try:
                    spiral_index = next_cell_function(spiral_index)
                except TypeError:
                    spiral_index = next_cell_function(matrix, cell)
            direction = get_next_direction(direction)
        stepsize += 1

    return matrix


def get_sum_neighbours(matrix, cell):
    """ gets only sum of the four surrounding neighbours """
    result = 0
    for direction in directions:
        new_cell = move(cell, direction)
        if not index_out_of_range(new_cell, len(matrix)):
            result += matrix.item(new_cell)
    return result


def get_sum_all_neighbours(matrix, cell):
    """
    Get the sum of all surrounding neighbours.
    This actually draws a swastika, as it moves from the centre
    to the $direction and then to the $next_direction four times,
    hence drawing 4 arms per 4 directions... This was not intended.
    """
    result = 0
    for direction in directions:
        new_cell = move(cell, direction)
        if not index_out_of_range(new_cell, len(matrix)):
            result += matrix.item(new_cell)
        new_cell = move(new_cell, get_next_direction(direction))
        if not index_out_of_range(new_cell, len(matrix)):
            result += matrix.item(new_cell)

    return result


def compute():
    """ main algorithm to do stuff """
    # how big of a spiral do we need?
    size = int(math.sqrt(input_num))
    size += 1 if size % 2 == 0 else 2
    matrix = build_spiral(size, lambda i: i + 1)
    # find the input number in the matrix
    result_cell = numpy.where(matrix == input_num)
    return get_distance(Point(size//2, size//2), Point(*result_cell))


def compute_sum_of_neighbours():
    """ every next square filling is the sum of the neighbouring cells. """
    size = 9
    matrix = build_spiral(size, get_sum_all_neighbours)
    result_cell = numpy.where(matrix > input_num)
    print(min(matrix[result_cell]))
    return get_distance(Point(size//2, size//2), Point(*result_cell))


def main():

    result = compute()
    print("Part 1: Distance from 1 to {} is {}.".format(input_num, result))

    result2 = compute_sum_of_neighbours()
    print("First value bigger than {} is {}".format(input_num, result2))

    returnga 


if __name__ == '__main__':
    main()


