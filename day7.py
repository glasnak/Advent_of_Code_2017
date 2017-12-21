#!/usr/bin/env python3

"""
--- Day 7: Recursive Circus ---
"""

import re
from collections import Counter

input_file = 'input_day7.txt'

test_input = '''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)'''

# TODO: could easily be one regex instead and check for len(m.groups())
leaf_regex = re.compile(r'^([a-z]+) \((\d+)\)$')
node_regex = re.compile(r'^([a-z]+) \((\d+)\) -> ((?:[a-z]+(?:, )?)+)$')


class Tree:
    _nodes = {}
    _node_values = {}
    _root = None

    def __init__(self):
        pass

    def build(self, lines):
        """ parses the input lines into a tree """
        for line in lines:
            leaf_match = re.match(leaf_regex, line)
            if leaf_match:
                assert len(leaf_match.groups()) == 2
                self._node_values[leaf_match.group(1)] = int(leaf_match.group(2))
                self._nodes[leaf_match.group(1)] = []
                continue
            node_match = re.match(node_regex, line)
            if node_match:
                assert len(node_match.groups()) == 3
                self._node_values[node_match.group(1)] = int(node_match.group(2))
                self._nodes[node_match.group(1)] = node_match.group(3).split(', ')
                continue
            assert False

    def find_root(self):
        if self._root:
            return self._root
        self._root = next(iter(self._nodes.keys()))
        switched = True
        while switched:
            switched = False
            # go up in a tree until we find the root:
            for node, kids in self._nodes.items():
                if self._root in kids:
                    self._root = node
                    switched = True
                    break
        return self._root

    def sum_tree(self, node):
        """ a recursive function to sum the tree & its subtrees """
        result = self._node_values[node]
        for kid in self._nodes[node]:
            result += self.sum_tree(kid)
        return result

    def find_outlier(self):
        assert self._root
        node = self._root
        diff = 0
        while True:
            kids_sums = [self.sum_tree(kid) for kid in self._nodes[node]]
            kid_counter = Counter(kids_sums)
            outlier_num = min(kid_counter, key=kid_counter.get)
            if len(set(kids_sums)) == 1:
                answer = self._node_values[node] + diff
                print("The outlier '{}' with value {} should be {}.".format(node, self._node_values[node], answer))
                return answer

            diff = max(kid_counter, key=kid_counter.get) - outlier_num
            node_index = kids_sums.index(outlier_num)
            node = self._nodes[node][node_index]


def is_input_valid():
    for line in get_input():
        # is this leaf?
        if not re.match(leaf_regex, line) and not re.match(node_regex, line):
            return False
    return True


def get_input():
    # return test_input.splitlines()

    with open(input_file, 'r') as f:
        return f.readlines()


def main():
    if not is_input_valid():
        exit(1)

    tree = Tree()
    tree.build(get_input())
    root = tree.find_root()
    print("Root node is '{}'.\n".format(root))

    outlier = tree.find_outlier()
    print("Node should newly be {}.".format(outlier))
    return 0


if __name__ == '__main__':
    main()


