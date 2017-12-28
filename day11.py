#!/usr/bin/env python3

"""
--- Day 11: Hex Ed ---
"""

from collections import namedtuple

INPUT_FILE = 'input_day11.txt'

Point = namedtuple('Point', 'x y')


class HexGrid:
    """
    The representation of a Hex Grid centre and neighbours:
    --------------------------------------
            [ 0, 2]
    [-1, 1]         [ 1, 1]
            [ 0, 0]
    [-1,-1]         [ 1,-1]
            [ 0,-2]
    --------------------------------------
    No need to build the grid per se, if we only need the distance.
    This serves very well for such calculation.

    Distance from the centre can be calculated with:
        abs(x) + max(0, (abs(y) - abs(x)) // 2)
    this takes into account the sparse population of an 'array' that we
    never really built.
    """
    _position = Point(x=0, y=0)
    _moves = {
        'nw': (-1, 1),
        'n':  (0, 2),
        'ne': (1, 1),
        'se': (1, -1),
        's':  (0, -2),
        'sw': (-1, -1),
    }

    def move(self, position, direction):
        """ Return the new position after moving to @direction. """
        return Point(position.x + self._moves[direction][0],
                     position.y + self._moves[direction][1])

    def walk(self, steps):
        """
        Walk the @steps and calculate the distance from the center walked.
        Also returns max_distance for puzzle' sake.
        """
        max_distance = 0
        distance = 0
        for step in steps:
            self._position = self.move(self._position, step)
            distance = self.distance_from_center(self._position)
            if max_distance < distance:
                max_distance = distance
        return distance, max_distance

    @staticmethod
    def distance_from_center(cell):
        """ Distance in number of hexagon steps. """
        return abs(cell.x) + max(0, (abs(cell.y) - abs(cell.x)) // 2)


def get_input():
    """
    Read the input that indicates the directions moved,
    looks like e.g. 'ne,ne,n,sw,s'
    """
    with open(INPUT_FILE) as f:
        return f.read().split(',')


def main():
    """ Calculate the distance moved in the hex grid """
    grid = HexGrid()
    steps = get_input()
    distance, max_distance = grid.walk(steps)
    print("Final distance is {}".format(distance))
    print("Maximum distance was {}".format(max_distance))
    return


if __name__ == '__main__':
    main()
