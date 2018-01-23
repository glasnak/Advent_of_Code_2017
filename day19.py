#!/usr/bin/env python3

"""
--- Day 19: A Series of Tubes ---
"""


INPUT_FILE = 'input_day19.txt'

TEST_INPUT = """
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
"""

DIRECTIONS = {
    'down': (1, 0),
    'up':  (-1, 0),
    'left': (0, -1),
    'right': (0, 1)
}


def get_input():
    """
    Read the input that indicates the firewall depths and ranges.
    Looks like a lot of lines such as '2: 14'
    """
    # return TEST_INPUT.split('\n')
    with open(INPUT_FILE) as f:
        return f.readlines()


def parse_input(lines):
    """ return non-empty lines """
    return [line for line in lines if line]


def walkthrough(matrix):
    """ walk through the path. """
    # starting point:
    word = []
    end_letter = 'A'
    position = (0, matrix[0].find('|'))
    direction = DIRECTIONS['down']

    position_val = matrix[position[0]][position[1]]
    steps = 0
    while position_val != end_letter:
        steps += 1
        # continue on lines or letters:
        # this assumes no letter is at the edge instead of '+'
        if position_val in ['|', '-'] or position_val.isupper():
            position = (position[0]+direction[0], position[1]+direction[1])
            if position_val.isupper():
                word += position_val
        elif position_val == '+':
            # change direction on +:
            if direction in [DIRECTIONS['left'], DIRECTIONS['right']]:
                x_up, y_up = DIRECTIONS['up']
                try:
                    up_neighbour = matrix[position[0]+x_up][position[1]+y_up]
                    if up_neighbour == '|' or up_neighbour.isupper():
                        direction = DIRECTIONS['up']
                    else:
                        direction = DIRECTIONS['down']
                except IndexError:
                    direction = DIRECTIONS['down']
            else:  # dir is up or down
                x_left, y_left = DIRECTIONS['left']
                try:
                    left_neighbour = matrix[position[0]+x_left][position[1]+y_left]
                    if left_neighbour == '-' or left_neighbour.isupper():
                        direction = DIRECTIONS['left']
                    else:
                        direction = DIRECTIONS['right']
                except IndexError:
                    direction = DIRECTIONS['right']
            position = (position[0] + direction[0], position[1] + direction[1])

        else:
            print("Lost the path on ", position)
            exit(1)
        position_val = matrix[position[0]][position[1]]
    return ''.join(word) + end_letter, steps + 1


def main():
    """ Walk the line """
    input_matrix = parse_input(get_input())
    word, steps = walkthrough(input_matrix)
    print("I read word {} in the matrix...".format(word))
    print("... while walking {} steps.".format(steps))

    return


if __name__ == '__main__':
    main()
