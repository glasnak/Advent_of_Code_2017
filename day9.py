#!/usr/bin/env python3

"""
--- Day 9: Stream Processing ---
"""

input_file = 'input_day9.txt'


def get_garbage():
    with open(input_file, 'r') as f:
        return f.read()


def remove_exclamations(text):
    """
    '!' indicates that the next character is garbage.
    Remove all the exclamation marks and the following characters with them.
    """
    new_text = ''
    should_skip = False
    for ch in text:
        if should_skip:
            should_skip = False
            continue
        should_skip = ch == '!'
        if should_skip:
            continue
        new_text += ch
    return new_text


def remove_comments(text):
    """
    '<' indicates start of garbage. Doesn't end until
    the '>' character. Remove all comments like these.
    Assumes already removed exclamation marks aka garbage.
    """
    new_text = ''
    should_skip = False
    removed = 0
    for ch in text:
        if should_skip:
            should_skip = ch != '>'
            removed += 1 if should_skip else 0
            continue
        should_skip = ch == '<'
        if should_skip:
            continue
        new_text += ch
    return new_text, removed


def count_groups(text):
    score = 0
    depth = 0
    for token in text:
        if token == '{':
            depth += 1
        elif token == '}':
            score += depth
            depth -= 1
        elif token == ',':
            pass
        else:
            assert False

    return score


def main():
    """ Incrementally clean up text until it's simpler and countable """
    text = get_garbage()
    text = remove_exclamations(text)
    text, removed = remove_comments(text)
    result = count_groups(text)
    print("Groups total Score: {}".format(result))
    print("Removed the total of {} characters.".format(removed))

    return result


if __name__ == '__main__':
    main()


