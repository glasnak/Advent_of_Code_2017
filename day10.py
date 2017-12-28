#!/usr/bin/env python3

"""
--- Day 10: Knot Hash ---
"""

from math import sqrt


BINARY_INPUT = '120,93,0,90,5,80,129,74,1,165,204,255,254,2,50,113'
TEST_INPUT = [3, 4, 1, 5]


def get_input(raw=False):
    """ Return the input - it varies in Part 1 and Part 2,
    so either return raw input or already parsed one """
    # return TEST_INPUT
    if raw:
        return BINARY_INPUT.strip()
    else:
        return [int(x) for x in BINARY_INPUT.strip().split(',')]


def perform_hash(num_elements, hash_nums, times=1):
    """ main algorithm for the 'hashing' functionality """
    elements = list(range(num_elements))
    position = 0
    skip_size = 0
    for _i in range(times):
        for num in hash_nums:
            if position + num <= num_elements:  # simple reversal
                elements = elements[:position] + \
                           elements[position:position + num][::-1] + \
                           elements[position + num:]
            else:  # reversal over the end:
                start_idx = position
                end_idx = (position + num) % num_elements
                # part to reverse:
                sublist = elements[start_idx:] + elements[:end_idx]
                sublist.reverse()
                # finally, combine the parts:
                elements = sublist[-end_idx:] + \
                           elements[end_idx:start_idx] + \
                           sublist[:-end_idx]
            position = (position + num + skip_size) % num_elements
            skip_size += 1
            # print(elements)
    return elements


def convert_to_ascii(text=''):
    """ returns the ascii sequence plus the default suffix. """
    return [ord(c) for c in text] + [17, 31, 73, 47, 23]


def chunks(lst, n):
    """ Yield successive n-sized chunks from lst """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def dense_hash(sparse_hash=''):
    """ e.g. 256 nums converted into dense 16 XOR'd numbers """
    root = int(sqrt(len(sparse_hash)))
    dense = []
    for chunk in chunks(sparse_hash, root):
        dense_num = 0  # 0 is a neutral element for XOR operation
        for n in chunk:
            dense_num ^= n
        dense.append(dense_num)

    return dense


def main():
    """ Calculate the puzzle """
    # Part 1, simple hashing:
    elements = perform_hash(num_elements=256, hash_nums=get_input())
    result = elements[0] * elements[1]
    print("Calculation of Part 1 Hash is {}.".format(result))

    # Part 2, proper hashing:
    ascii_nums = convert_to_ascii(get_input(raw=True))
    # start again:
    elements = perform_hash(num_elements=256, hash_nums=ascii_nums, times=64)
    dense = dense_hash(elements)
    hex_dense = [format(x, '02x') for x in dense]
    print("Final hash of the input: {}".format(''.join(hex_dense)))


if __name__ == '__main__':
    main()
