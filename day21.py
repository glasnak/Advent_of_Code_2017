#!/usr/bin/env python3

"""
--- Day 21: Fractal Art ---
"""

from collections import namedtuple
import itertools
import pprint
import numpy as np

Rule = namedtuple('Rule', 'before after')

INPUT_FILE = 'input_day21.txt'
TEST_INPUT = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"""

"""
    .#.
    ..#
    ###
"""
START_PATTERN = [[False, True, False],
                 [False, False, True],
                 [True, True, True]]


def get_input():
    """ Read the input rules. """
    # return TEST_INPUT.split('\n')
    with open(INPUT_FILE) as f:
        return f.readlines()


def parse_input(lines):
    """
    Return lines parsed into the structure that we can work with,
    input represents rules for transforming squares into bigger squares...
    examples:
    ##/#. => ###/#.#/.##
    ##./##./... => .#.#/#.##/####/.###
    """
    # rules structure:
    # a tuple of (before, after)
    #     where before is the smaller square ([[1,1],[1,0])
    #     and after is the bigger square: ([1,1,1],[1,0,1],[0,1,1])
    rules = {2: [], 3: []}
    binary_map = {'.': False, '#': True}
    ruleset = set()
    for line in lines:
        if not line.strip():
            continue
        before, after = line.strip().split(' => ')
        smaller = []
        bigger = []
        for row in before.strip().split('/'):
            smaller.append([binary_map[n] for n in row])
        for row in after.strip().split('/'):
            bigger.append([binary_map[n] for n in row])
        for _ in range(2):
            for rotation in range(4):
                # add all four rotations in:
                rot = np.rot90(smaller, rotation)
                strrot = ','.join(str(item) for row in rot for item in row)
                if strrot not in ruleset:
                    rules[len(rot[0])].append(Rule(np.array(rot), np.array(bigger)))
                    ruleset.add(strrot)

            smaller = np.flipud(smaller)

    return rules


def dump(stuff):
    """ pretty print stuff """
    pp = pprint.PrettyPrinter(indent=4)
    for x, y in stuff:
        pp.pprint(x)
        pp.pprint(y)
        print('-' * 50)


def show_image(image):
    """ pretty print the image """
    print('-' * (len(image) + 4))
    for line in image:
        print('| ', end='')
        for ch in line:
            char = '#' if ch is True else '.'
            print(char, end='')
        print(' |')
    print('-' * (len(image) + 4))


def enlarge(image, rules):
    """
    Large scale algorithm that runs enhancement algorithm on each of the squares
    the picture has.
    """
    imgsize = len(image)
    new_image = []
    divisibility = 2 if imgsize % 2 == 0 else 3
    for row in range(0, imgsize, divisibility):
        square_row = []
        for col in range(0, imgsize, divisibility):
            subimage = image[row:row + divisibility, col:col + divisibility]
            new_subimage = enhance(subimage, rules)
            square_row.append(new_subimage)
        new_image.append(square_row)

    img = []
    for m_row in new_image:
        for L in zip(*m_row):
            img.append(list(itertools.chain(*L)))

    return np.array(img)


def enhance(image, rules):
    """ A single enhancement step for a subimage of size specified in the rules.
    Finds a rule to follow and returns the new image. """

    # go through rules for this specific image size:
    for rule in rules[len(image)]:
        if np.array_equal(rule.before, image):
            return rule.after

    print("No rule fits this image:")
    show_image(image)
    print("Quitting...")
    exit(1)


def main():
    """ Parse the image and match the rules """

    rules = parse_input(get_input())
    for part in [5, 18]:
        image = np.array(START_PATTERN).astype(bool)
        for i in range(part):
            image = enlarge(image, rules)
        count = sum(sum(ch for ch in row) for row in image)

        print("Number of # in the final matrix after {} iterations is {}.".format(part, count))
    return


if __name__ == '__main__':
    main()
