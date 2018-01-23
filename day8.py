#!/usr/bin/env python3

"""
--- Day 8: I Heard You Like Registers ---
"""


from collections import namedtuple
import re


input_file = 'input_day8.txt'

test_input = '''b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10'''

regex = re.compile(r'(^[a-z]+) (inc|dec) (-?\d+) if ([a-z]+) (>=|<=|>|<|==|!=) (-?\d+)$')

Instruction = namedtuple('Instruction', 'reg increment value condition')
Condition = namedtuple('Condition', 'reg op num')


def is_input_valid():
    """ all lines must pass the regex test """
    for line in get_input():
        if not re.match(regex, line):
            return False
    return True


def get_input():
    """ return the input instructions """

    # return test_input.splitlines()

    with open(input_file) as f:
        return f.readlines()


def parse_input(lines):
    """
    input:  b inc 5 if a > 1
    match:  1  2  3    4 5 6
    """
    instrs = []
    for line in lines:
        match = re.match(regex, line)
        assert match
        assert len(match.groups()) == 6
        cond = Condition(*match.groups()[3:])
        cond = cond._replace(num=int(cond.num))
        instr = Instruction(*match.groups()[:3], condition=cond)
        instr = instr._replace(value=int(instr.value))
        instrs.append(instr)

    return instrs


def eval_condition(cond, regs):
    assert cond.reg in regs
    if cond.op == '==':
        return regs[cond.reg] == cond.num
    elif cond.op == '!=':
        return regs[cond.reg] != cond.num
    elif cond.op == '>=':
        return regs[cond.reg] >= cond.num
    elif cond.op == '<=':
        return regs[cond.reg] <= cond.num
    elif cond.op == '>':
        return regs[cond.reg] > cond.num
    elif cond.op == '<':
        return regs[cond.reg] < cond.num
    # unreachable:
    print("unknown operator '{}'" % cond.op)
    exit(3)


def execute(instrs):
    """
    Instruction: reg increment value condition
    Condition:   reg op num
    """
    regs = {}
    max_reg = 0
    for i in instrs:
        if i.reg not in regs:
            regs[i.reg] = 0
        if i.condition.reg not in regs:
            regs[i.condition.reg] = 0
        if eval_condition(i.condition, regs):
            inc = i.value if i.increment == 'inc' else -i.value
            regs[i.reg] += inc
            if regs[i.reg] > max_reg:
                max_reg = regs[i.reg]
    print("Biggest number in any register is {}".format(max(regs.values())))
    print("Biggest number ever in register was {}".format(max_reg))


def main():
    if not is_input_valid():
        print("invalid input!")
        exit(1)

    instrs = parse_input(get_input())
    execute(instrs)

    return 0


if __name__ == '__main__':
    main()


