#!/usr/bin/env python3

"""
--- Day 18: Duet ---
"""


INPUT_FILE = 'input_day18.txt'

TEST_INPUT = '''
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
'''


class Interpreter:
    """
    More-or-less interpreter of the micro-language we have for the puzzle.
    """

    _pc = 0
    _regs = {}
    _muls = 0

    def add(self, var, num):
        """ add a a|1 """
        self._regs[var] = self._regs.get(var, 0)
        self._regs[var] += num

    def sub(self, var, num):
        """ sub a a|1 """
        self._regs[var] = self._regs.get(var, 0)
        self._regs[var] -= num

    def jgz(self, var, num):
        """ jgz a|1 a|1 """
        if var > 0:
            self._pc += num - 1

    def jnz(self, var, num):
        """ jnz a|1 a|1 """
        if var != 0:
            self._pc += num - 1

    def mod(self, var, num):
        """ mod a a|1 """
        self._regs[var] = self._regs.get(var, 0)
        # print(self._regs, var, num, self._pc)
        self._regs[var] %= num

    def mul(self, var, num):
        """ mul a a|1 """
        # print([var, num])
        self._regs[var] = self._regs.get(var, 0)
        self._regs[var] *= num
        self._muls += 1

    def rcv(self, var):
        """ rcv a """
        if var != 0:
            print("Recovered with {}.".format(self._regs['SOUND']))
            exit()

    def set(self, var, num):
        """ set a a|1 """
        self._regs[var] = self._regs.get(var, 0)
        self._regs[var] = num

    def snd(self, var):
        """ snd a """
        self._regs['SOUND'] = var

    def _get_value(self, x):
        """ return the value of register or the immediate, whatever x is. """
        return int(self._regs.get(x, 0) if x.islower() else x)

    def _execute(self, instruction):
        """
        Execute a single instruction.
        Return a difference in PC that this instruction causes
        (usually 1, not always)
        """
        operation, operands = instruction
        # syntax descriptions include 1 for '\d+', a for '[a-z]'
        d_pc = 1
        if operation in ['add', 'sub', 'set', 'mod', 'mul']:
            # syntax: OPC a a|1
            op0 = operands[0]
            op1 = self._get_value(operands[1])
            getattr(self, operation)(op0, op1)
        elif operation in ['snd', 'rcv']:
            # syntax: OPC a
            op1 = self._get_value(operands[0])
            getattr(self, operation)(op1)
        elif operation in ['jgz', 'jnz']:
            # syntax: jgz a|1 a|1
            op0 = self._get_value(operands[0])
            op1 = self._get_value(operands[1])
            d_pc = getattr(self, operation)(op0, op1)
        else:
            print("Unreachable!")
            exit(1)

        return d_pc

    def restart(self):
        """ start from the beginning. """
        self._pc = 0
        for r in self._regs.keys():
            self._regs[r] = 0

    def run(self, program):
        """ Run the whole program. """
        len_program = len(program)
        while 0 <= self._pc < len_program:
            self._execute(program[self._pc])
            self._pc += 1

        return self._regs

    def run23(self, program):
        """ Run the whole day23 program. """
        len_program = len(program)
        while 0 <= self._pc < len_program:
            self._execute(program[self._pc])
            self._pc += 1

        return self._muls

    def run23_2(self, program):
        """ Run the part 2 of day23: See day23.py. """
        self._regs['a'] = 1
        len_program = len(program)
        while 0 <= self._pc < len_program:
            self._execute(program[self._pc])
            self._pc += 1

        return self._regs.get('h', -42)


def get_input():
    """ return the input instructions """
    # return TEST_INPUT.strip().splitlines()

    with open(INPUT_FILE) as f:
        return f.readlines()


def parse_input(lines):
    """ parse input such as 'mod a 5' into executable instructions. """
    instrs = []
    for line in lines:
        instr = line.strip().split(' ')
        instrs.append((instr[0], instr[1:]))

    return instrs


def main():
    """ run the puzzle of day 18, find the sound. """

    instrs = parse_input(get_input())
    interpreter = Interpreter()
    interpreter.run(instrs)

    return 0


if __name__ == '__main__':
    main()
