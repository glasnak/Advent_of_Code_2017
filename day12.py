#!/usr/bin/env python3

"""
--- Day 12: Digital Plumber ---
"""

from collections import namedtuple
import re

INPUT_FILE = 'input_day12.txt'

TEST_INPUT = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

Point = namedtuple('Point', 'x y')

RGX = re.compile(r'(\d+) <-> (\d+(?:, ?\d+)*)')


def get_input():
    """
    Read the input that indicates the nodes connections.
    Looks like a lot of lines such as '18 <-> 150, 1394, 1458'
    """
    # return TEST_INPUT.split('\n')
    with open(INPUT_FILE) as f:
        return f.readlines()


def parse_input(lines):
    """
    Parse input lines such as '18 <-> 150, 1394, 1458'
    into dict such as { 18 : [150, 1394, 1458] }
    """
    relations = {}
    for line in lines:
        match = re.match(RGX, line)
        assert match
        assert len(match.groups()) == 2
        key = int(match.group(1))
        values = [int(x) for x in match.group(2).split(', ')]
        relations[key] = values
    return relations


def find_relations(relations, key):
    """ Count the friends of the key node """
    stack = [key]
    relation_set = set()
    while stack:
        k = stack.pop()
        if k not in relation_set and k in relations:
            relation_set.add(k)
            stack += relations[k]

    return relation_set


def count_groups(relations):
    """ Count the number of groups that aren't connected to each other """
    groups = 0
    while relations:
        key = next(iter(relations.keys()))
        rels = find_relations(relations, key)
        for rel in rels:
            relations.pop(rel)
        groups += 1
    return groups


def main():
    """ Calculate the distance moved in the hex grid """
    relations = parse_input(get_input())
    relation_set = find_relations(relations, 0)
    print("Number of nodes connected to zero is {}".format(len(relation_set)))

    num_groups = count_groups(relations)
    print("Number of groups is {}".format(num_groups))

    return


if __name__ == '__main__':
    main()
