#!/usr/bin/env python3

"""
--- Day 1: Inverse Captcha ---
"""

input_file = 'input_day1.txt'


def get_input():
    with open(input_file, 'r') as f:
        return f.read().strip()


def compute_half_circular(input_code, step):
    result = 0
    size = len(input_code)
    # step = size / 2
    for i, ch in enumerate(input_code):
        nexti = (i + step) % size
        if input_code[i] == input_code[nexti]:
            result += int(ch)
    return result


def main():
    input_code = get_input()

    # part 1
    result = compute_half_circular(input_code, 1)
    print("Captcha 1: {}".format(result))

    # part 2
    result2 = compute_half_circular(input_code, len(input_code) // 2)
    print("Captcha 2: {}".format(result2))


if __name__ == '__main__':
    main()


