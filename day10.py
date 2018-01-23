#!/usr/bin/env python3

"""
--- Day 10: Knot Hash ---
"""

from math import sqrt


BINARY_INPUT = '120,93,0,90,5,80,129,74,1,165,204,255,254,2,50,113'
TEST_INPUT = '3,4,1,5'


def get_input():
    """ Return the stripped input in the binary form. """
    return BINARY_INPUT.strip()


class Hash:
    """ A static class for a Hashing function. """

    @staticmethod
    def _parsed(raw_input):
        """ parse the raw text such as [3,4,1,5] """
        # return [int(x) for x in raw_input.split(',')]
        return list(eval(raw_input))

    @staticmethod
    def sparse_hash(hash_nums, num_elements=256, times=1):
        """ main algorithm for the 'hashing' functionality """
        elements = list(range(num_elements))
        position = 0
        skip_size = 0
        for _i in range(times):
            for num in hash_nums:
                if position + num <= num_elements:  # simple reversal
                    elements = elements[:position] + elements[position:position + num][::-1] + elements[position + num:]
                else:  # reversal over the end:
                    start_idx = position
                    end_idx = (position + num) % num_elements
                    # part to reverse:
                    sublist = elements[start_idx:] + elements[:end_idx]
                    sublist.reverse()
                    # finally, combine the parts:
                    elements = sublist[-end_idx:] + elements[end_idx:start_idx] + sublist[:-end_idx]
                position = (position + num + skip_size) % num_elements
                skip_size += 1
        return elements

    @staticmethod
    def _ascii(text):
        """ returns the ascii sequence plus the default suffix. """
        return [ord(c) for c in text] + [17, 31, 73, 47, 23]

    @staticmethod
    def _chunks(lst, n):
        """ Yield successive n-sized chunks from lst """
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def dense_hash(self, raw_input):
        """ convert elements (e.g. 256 nums) into dense 16 XOR'd numbers """
        elements = self._ascii(raw_input)
        sparse = self.sparse_hash(hash_nums=elements, times=64)
        root = int(sqrt(len(sparse)))
        dense = []
        for chunk in self._chunks(sparse, root):
            dense_num = 0  # 0 is a neutral element for XOR operation
            for n in chunk:
                dense_num ^= n
            dense.append(dense_num)

        hexa_code = ''.join([format(x, '02x') for x in dense])
        return hexa_code


def main():
    """ Calculate the hash """
    # Part 1, simple hashing:
    h = Hash()
    raw_input = get_input()
    numlist = list(eval(raw_input))
    elements = h.sparse_hash(numlist)
    result = elements[0] * elements[1]
    print("Calculation of Part 1 Hash is {}.".format(result))

    # Part 2, proper hashing:
    dense = h.dense_hash(raw_input)
    print("Final hash of the input: {}".format(dense))


if __name__ == '__main__':
    main()
