#!/usr/bin/env python3

"""
--- Day 18: Duet: Part 2 ---
"""

INPUT_FILE = 'input_day18.txt'

TEST_INPUT_1 = '''
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


TEST_INPUT = '''snd 10
snd 20
snd p
rcv a
rcv b
rcv c
rcv d'''


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


class Interpreter:
    """
    An interpreter of the micro-language we have for the puzzle.
    """

    def __init__(self, process_id):
        self._regs = {'p': process_id}
        self._pc = 0
        self._send_queue = []
        self._received = []

    def add(self, var, num):
        """ add a a|1 """
        self._regs[var] = self._regs.get(var, 0)
        self._regs[var] += num

    def jgz(self, var, num):
        """ jgz a|1 a|1 """
        if var > 0:
            self._pc += num - 1

    def mod(self, var, num):
        """ mod a a|1 """
        self._regs[var] = self._regs.get(var, 0) % num

    def mul(self, var, num):
        """ mul a a|1 """
        self._regs[var] = self._regs.get(var, 0) * num

    def rcv(self, var):
        """ receive a from other process. """
        self._regs[var] = self._received.pop(0)

    def set(self, var, num):
        """ set a a|1 """
        # self._regs[var] = self._regs.get(var, 0)
        self._regs[var] = num

    def snd(self, var):
        """ send a to other process """
        self._send_queue.append(var)

    def _get_value(self, x):
        """ eval the variable or return the value itself """
        return int(self._regs.get(x, 0) if x.islower() else x)

    def execute(self, instruction):
        """
        Execute a single instruction.
        Return a difference in PC that this instruction causes
        (usually 1, not always)
        """
        operation, operands = instruction
        # syntax descriptions are: 1 for '\d+', a for '[a-z]'
        d_pc = 1
        if operation in ['add', 'set', 'mod', 'mul']:
            # syntax: OPC a a|1
            op0 = operands[0]
            op1 = self._get_value(operands[1])
            getattr(self, operation)(op0, op1)
        elif operation == 'snd':
            # syntax: snd 1
            op1 = self._get_value(operands[0])
            getattr(self, operation)(op1)
        elif operation == 'rcv':
            # syntax: rcv a
            getattr(self, operation)(operands[0])
        elif operation == 'jgz':
            # syntax: jgz a|1 a|1
            op0 = self._get_value(operands[0])
            op1 = self._get_value(operands[1])
            d_pc = getattr(self, operation)(op0, op1)
        else:
            print("Unreachable!")
            exit(1)

        return d_pc

    def run(self, program, received):
        """
        Run the program until receive.
        If starting on receive, check the received and apply.
        Otherwise quit
        """
        self._received = received
        len_program = len(program)
        assert 0 <= self._pc < len_program
        while 0 <= self._pc < len_program:
            instr = program[self._pc]
            if instr[0] == 'rcv':
                if self._received:
                    self.execute(program[self._pc])
                else:
                    break
            else:
                self.execute(program[self._pc])
            self._pc += 1
        assert 0 <= self._pc < len_program
        # the end, send the queue:
        send_queue = self._send_queue
        self._send_queue = []
        assert not self._received
        return send_queue


def run_both(instrs):
    """
    Run both interpreters at the same time.
    Stop each one on receive if its queue is empty. Otherwise, just run.
    Should run smoothly as if in parallel.
    :return: the puzzle solution (number of times program A has sent a value)
    Kill on deadlock or 0<=pc<len(program)
    """
    interpreter_a = Interpreter(process_id=0)
    interpreter_b = Interpreter(process_id=1)
    a_counter = 0
    pending = {'a': [], 'b': []}
    while True:
        pending['b'] = interpreter_a.run(instrs, received=pending['a'])
        assert not pending['a']
        if not pending['b']:
            break
        pending['a'] = interpreter_b.run(instrs, received=pending['b'])
        a_counter += len(pending['a'])
        assert not pending['b']
        if not pending['a'] and not pending['b']:
            break

    return a_counter


def main():
    """ run the puzzle of day 18, part 2 """
    instrs = parse_input(get_input())
    num_sent_by_a = run_both(instrs)

    print("Process 1 has sent {} values.".format(num_sent_by_a))

    return


if __name__ == '__main__':
    main()

