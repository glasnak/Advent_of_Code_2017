#!/usr/bin/env python3

"""
--- Day 6: Memory Reallocation ---
"""

memory_banks = '4	10	4	1	8	4	9	14	5	1	14	15	0	15	3	5'.split('\t')

debug_input = [0, 2, 7, 0]

""" Execution of a weirdly-changing program counter """


def string(lst):
    """ Not ''.join, because then [12,3] == [1,2,3] collision happens."""
    return '_'.join(str(x) for x in lst)


def compute():
    """ main algorithm to do stuff """
    banks = [int(x) for x in memory_banks]
    configurations = {string(banks): 0}
    num_configs = 1
    while len(configurations) == num_configs:
        cell_index = banks.index(max(banks))
        values = banks[cell_index]
        banks[cell_index] = 0
        while values != 0:
            cell_index = (cell_index + 1) % len(banks)
            values -= 1
            banks[cell_index] += 1
        num_configs += 1
        if string(banks) not in configurations:
            configurations[string(banks)] = num_configs - 1
    cycle_length = num_configs - configurations[string(banks)] - 1
    return num_configs, cycle_length


def main():
    num_configs, cycle_length = compute()

    print("A repeating configuration after %s iterations." % str(num_configs-1))
    print("Cycle has length of %s." % cycle_length)

    return


if __name__ == '__main__':
    main()

