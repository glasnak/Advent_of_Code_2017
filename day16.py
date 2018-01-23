#!/usr/bin/env python3

"""
--- Day 16: Permutation Promenade ---
"""


import string

input_file = 'input_day16.txt'

LENGTH = 16


def get_input():
    """ get input """
    with open(input_file) as f:
        return f.read().split(',')


def make_step(step, order):
    """ one step at a time... """
    if step[0] == 's':
        length = int(step[1:])
        order = order[-length:] + order[:LENGTH - length]
    elif step[0] == 'x':
        a, b = [int(x) for x in step[1:].split('/')]
        order[a], order[b] = order[b], order[a]
    elif step[0] == 'p':
        a, b = step[1:].split('/')
        i, j = order.index(a), order.index(b)
        order[i], order[j] = order[j], order[i]
    else:
        print("Unknown step!")
        exit(1)
    return order


def compute(times=1):
    """ main algorithm """
    order = list(string.ascii_lowercase[:LENGTH])  # a..p
    steps = get_input()
    orders = [''.join(order)]
    repeating_range = None
    # find the repeating range:
    for _i in range(times):
        for step in steps:
            order = make_step(step, order)
        orders += [''.join(order)]
        if len(set(orders)) != len(orders):
            repeating_range = len(set(orders))
            break
    # done without repeating range:
    if not repeating_range:
        return order
    # ignore loops, modulo repeats:
    for _i in range(times % repeating_range):
        for step in steps:
            order = make_step(step, order)

    return order


def main():
    """ main """
    order = compute()
    print(''.join(order))

    order = compute(times=1000000000)
    print(''.join(order))

    return


if __name__ == '__main__':
    main()


