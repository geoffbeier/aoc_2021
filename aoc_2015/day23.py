import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 23
try:
    if __name__ != "__main__":
        assert str(aoc_day) in __name__
except AssertionError:
    logger.error(
        f"aoc_day={aoc_day} but this module name is {__name__}. aocd.get_data() is not going to behave properly."
    )
    m = re.match(r".*.day(\d+?)$", __name__)
    if m:
        aoc_day = int(m.groups()[0])
        logger.warning(
            f"Attempting to self-correct based on {__name__}. Now aoc_day={aoc_day}"
        )
    else:
        logger.error(f"Unable to guess a day from {__name__}. Exiting")
        sys.exit(1)


@dataclass
class AOCContext:
    raw: List[str]
    program: List[Tuple[str, List[Any]]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    program = []
    for line in raw:
        cmd, args = line.split(" ", maxsplit=1)
        arglist = []
        args = args.split(", ")
        if cmd == "hlf":
            arglist = [args[0]]  # r
        elif cmd == "tpl":
            arglist = [args[0]]  # r
        elif cmd == "inc":
            arglist = [args[0]]  # r
        elif cmd == "jmp":
            arglist = [int(args[0])]  # offset
        elif cmd == "jie":
            arglist = [args[0], int(args[1])]  # reg, offset
        elif cmd == "jio":
            arglist = [args[0], int(args[1])]  # reg, offset
        program.append((cmd, arglist))
    context = AOCContext(raw, program)
    return context


class Computer:
    pc: int
    max_pc: int
    registers: Dict[str, int]
    program: List[Tuple[str, List[Any]]]

    def __init__(self):
        self.pc = 0
        self.max_pc = 0
        self.registers = defaultdict(int)

    def load(self, context: AOCContext):
        self.program = deepcopy(context.program)
        self.pc = 0
        self.registers = defaultdict(int)
        self.max_pc = len(self.program) - 1

    def run(self):
        while self.pc <= self.max_pc:
            logger.debug(
                f"pc: {self.pc} - a={self.registers['a']}, b={self.registers['b']}"
            )
            ins, args = self.program[self.pc]
            logger.debug(f"ins: {ins} {args}")
            if ins == "hlf":
                r = args[0]
                self.registers[r] = self.registers[r] // 2
                self.pc += 1
            elif ins == "tpl":
                r = args[0]
                self.registers[r] *= 3
                self.pc += 1
            elif ins == "inc":
                r = args[0]
                self.registers[r] += 1
                self.pc += 1
            elif ins == "jmp":
                offset = args[0]
                self.pc += offset
            elif ins == "jie":
                r = args[0]
                offset = args[1]
                if self.registers[r] % 2 == 0:
                    self.pc += offset
                else:
                    self.pc += 1
            elif ins == "jio":
                r = args[0]
                offset = args[1]
                if self.registers[r] == 1:
                    self.pc += offset
                else:
                    self.pc += 1
            else:
                raise ValueError(f"Unrecognized instruction: {ins}")


def part1(context: AOCContext):
    computer = Computer()
    computer.load(context)
    computer.run()
    return str(computer.registers["b"])


def part2(context: AOCContext):
    computer = Computer()
    computer.load(context)
    computer.registers["a"] = 1
    computer.run()
    return str(computer.registers["b"])


tests = [
    (
        """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
""",
        605,
        part1,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    for i, t in enumerate(tests[start:finish]):

        def gd(*args, **kwargs):
            return t[0]

        aocd.get_data = gd
        result = t[2](preprocess())
        if f"{result}" != f"{t[1]}":
            logger.error(f"Test {start + i + 1} failed: got {result}, expected {t[1]}")
            break
        else:
            logger.success(f"Test {start + i + 1}: {t[1]}")


if __name__ == "__main__":
    test()
