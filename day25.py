#!/usr/bin/env python3

"""
--- Day 25: The Halting Problem ---
"""


INPUT_FILE = 'input_day25.txt'
TEST_INPUT = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""


def get_input():
    """
    Read the Turing's instructions.
    """
    # return TEST_INPUT.strip().split('\n\n')
    with open(INPUT_FILE) as f:
        return f.read().strip().split('\n\n')


def parse_input(parts):
    """
    Return the rules for the Turing machine, with some extra metadata.
    metadata = ( start_state, checksum_after )
    A rule is a map such as:
    ('A', 0) => (0, '>', 'B')
    this means that if in a state A and position = 0, we write 0, move right and set state = B.
    - dir = '<' | '>'
    """

    """
        Begin in state A.
        Perform a diagnostic checksum after 6 steps.
    """
    turing = {}
    metadata_part = parts[0].split('\n')
    start_state = metadata_part[0][-2]
    checksum_after = 12302209

    metadata = (start_state, checksum_after)

    for part in parts[1:]:
        lines = part.split('\n')
        state = lines[0][-2]
        state_num = int(lines[1][-2])
        # print("PART N: ", state, state_num)
        #   - Write the value X.
        write_val = int(lines[2][-2])
        move = '>' if lines[3][-6:-1] == 'right' else '<'
        next_state = lines[4][-2]
        turing[(state, state_num)] = (write_val, move, next_state)

        state_num = int(lines[5][-2])
        # print("PART N: ", state, state_num)
        write_val = int(lines[6][-2])
        move = '>' if lines[7][-6:-1] == 'right' else '<'
        next_state = lines[8][-2]
        turing[(state, state_num)] = (write_val, move, next_state)

    # print(turing)

    return turing, metadata


def run(ruleset, start='A', steps=6):
    """ Run the Turing machine. """
    # represent infinite tape with a sparse array:
    tape = set()
    # arbitrary position on an infinite tape:
    position = 0
    state = start

    for _ in range(steps):
        tape_val = 1 if position in tape else 0
        val, move, next_state = ruleset[state, tape_val]
        # (1) write 0/1 onto the tape:
        if val == 0 and position in tape:
            tape.remove(position)
        elif val == 1:
            tape.add(position)
        # (2) move <,> on the tape:
        position += 1 if move == '>' else -1
        # (3) change to the new state
        state = next_state

    # return the checksum
    return len(tape)


def main():
    """ Run the Turing Machine! """

    ruleset, meta = parse_input(get_input())
    start, steps = meta
    x = run(ruleset, start, steps)
    print("Checksum is {}.".format(x))

    return


if __name__ == '__main__':
    main()
