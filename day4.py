#!/usr/bin/env python3

"""
--- Day 4: High-Entropy Passphrases ---
"""


input_file = 'input_day4.txt'


def get_input():
    with open(input_file, 'r') as f:
        return f.read()


def has_dups(passphrase):
    s = set()
    words = passphrase.split(' ')
    for word in words:
        s.add(''.join(word))
    return len(s) == len(words)


def has_anagram_dups(passphrase):
    s = set()
    words = passphrase.split(' ')
    for word in words:
        s.add(''.join(sorted(word)))
    return len(s) == len(words)


def compute(passphrases, check_anagrams=False):
    check_func = has_anagram_dups if check_anagrams else has_dups
    return sum(1 for x in passphrases if check_func(x))


def main():
    passphrases = get_input().splitlines()
    result = compute(passphrases, check_anagrams=False)
    print("Valid passphrases: {}\n".format(result))

    result2 = compute(passphrases, check_anagrams=True)
    print("Valid no-anagram passphrases: {}\n".format(result2))

    return


if __name__ == '__main__':
    main()


