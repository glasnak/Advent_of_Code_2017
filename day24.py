#!/usr/bin/env python3

"""
--- Day 24: Electromagnetic Moat ---
Backtracking with Memoization 101
"""

from collections import namedtuple

Component = namedtuple('Component', 'ports free')

INPUT_FILE = 'input_day24.txt'
TEST_INPUT = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""


def get_input():
    """ Read the input. """
    # return TEST_INPUT.strip().split('\n')
    with open(INPUT_FILE) as f:
        return f.readlines()


def parse_input(lines):
    """ return the bridge components we have on input,
    as a list of tuples with ports, e.g. [(0,2), (1,4)] """
    bridges = []
    for line in lines:
        left, right = line.split('/')
        bridges.append((int(left), int(right)))

    return bridges


def fitting_components(end_port, components):
    """ return all free components that fit on the current bridge. """
    return [c for c in components if c[0] == end_port or c[1] == end_port]


def bridge_value(bridge):
    """ calculate bridge value,
        e.g. [(0,10),(10,7),(7,3)]
           ==> 0+10 + 10+7 + 7+3 = 37
    """
    val = 0
    for left, right in bridge:
        val += left + right
    return val


def bridge_length(bridge):
    """ return the longer bridge. In case of same length, pick stronger one. """
    return len(bridge)


def find_bridge(bridge, components, cmp):
    """ a recursive function to search through the possible bridges.
    bridge is e.g. [(1,2),(2,7),(7,4)]
    components are all free components we can still use.
    """
    top_bridge = []
    end_port = bridge[-1][1]
    fitting = fitting_components(end_port, components)
    if not fitting:
        return bridge
    for component in fitting:
        new_bridge = list(bridge)
        new_components = list(components)
        new_components.remove(component)
        new_bridge.append(component if end_port == component[0] else list(reversed(component)))
        cand_top = find_bridge(new_bridge, new_components, cmp=cmp)
        if cmp_bridges(cand_top, top_bridge, cmp) >= 0:
            top_bridge = cand_top

    return top_bridge


def solve(bridges, components, cmp):
    """ Solve the problem. Return the top result. """
    top_bridge = []
    while bridges:
        bridge = [bridges.pop()]
        new_components = list(components)
        new_components.remove(bridge[0])
        cand_top = find_bridge(bridge, new_components, cmp=cmp)
        if cmp_bridges(cand_top, top_bridge, cmp) >= 0:
            top_bridge = cand_top

    return top_bridge


def cmp_bridges(b1, b2, cmp_method=bridge_value):
    """ Comparison for sorting the bridges. """
    b1_val = cmp_method(b1)
    b2_val = cmp_method(b2)
    if b1_val > b2_val:
        return 1
    elif b1_val < b2_val:
        return -1
    else:
        if cmp_method != bridge_value:
            return cmp_bridges(b1, b2)
        return 0


def main():
    """ Find the strongest and longest bridges. """

    # part 1:
    components = parse_input(get_input())
    bridges = fitting_components(0, components)
    max_bridge = solve(bridges, components, cmp=bridge_value)
    print(max_bridge)
    print("Max bridge has value ==  {}.".format(bridge_value(max_bridge)))

    # part 2:
    components = parse_input(get_input())
    bridges = fitting_components(0, components)

    long_bridge = solve(bridges, components, cmp=bridge_length)
    print(long_bridge)
    print("Longest bridge length = {}.".format(len(long_bridge)))
    print("Longest bridge value = {}.".format(bridge_value(long_bridge)))

    return


if __name__ == '__main__':
    main()
