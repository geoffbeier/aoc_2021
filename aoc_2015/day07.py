import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

import _md5

aoc_day = 7


@dataclass
class Circuit:
    op: str
    args: Tuple
    dest: str


def preprocess():
    circuits = []
    for line in aocd.get_data(day=aoc_day, year=aoc_year).splitlines():
        lhs, rhs = line.split(" -> ")
        if " AND " in lhs:
            args = lhs.split(" AND ")
            circuits.append(Circuit("AND", (args[0], args[1]), rhs))
        elif " OR " in lhs:
            args = lhs.split(" OR ")
            circuits.append(Circuit("OR", (args[0], args[1]), rhs))
        elif " LSHIFT " in lhs:
            args = lhs.split(" LSHIFT ")
            circuits.append(Circuit("LSHIFT", (args[0], int(args[1])), rhs))
        elif " RSHIFT " in lhs:
            args = lhs.split(" RSHIFT ")
            circuits.append(Circuit("RSHIFT", (args[0], int(args[1])), rhs))
        elif lhs.startswith("NOT"):
            args = lhs.split("NOT ")
            circuits.append(Circuit("NOT", (args[1],), rhs))
        else:
            circuits.append(Circuit("SIGNAL", (lhs,), rhs))
    return circuits


def run_circuits(circuits: List[Circuit], override: Dict = None):
    wires = {c.dest: c for c in circuits}
    if override:
        for key in override.keys():
            wires[key] = override[key]
    # checking for signal and making sure all inputs signal before we're done was the tricky part here.
    # The phrase "A gate provides no signal until all of its inputs have a signal." in the puzzle
    # carried a lot of water, and the sample case did not demonstrate it at all.
    while sum(isinstance(v, Circuit) for v in wires.values()):
        for c in wires.values():
            if isinstance(c, int):
                continue
            if c.op == "SIGNAL":
                src = int(c.args[0]) if c.args[0].isdecimal() else wires[c.args[0]]
                if isinstance(src, int):
                    wires[c.dest] = src
            elif c.op == "AND":
                lhs = int(c.args[0]) if c.args[0].isdecimal() else wires[c.args[0]]
                rhs = int(c.args[1]) if c.args[1].isdecimal() else wires[c.args[1]]
                if isinstance(lhs, int) and isinstance(rhs, int):
                    wires[c.dest] = lhs & rhs
            elif c.op == "OR":
                lhs = int(c.args[0]) if c.args[0].isdecimal() else wires[c.args[0]]
                rhs = int(c.args[1]) if c.args[1].isdecimal() else wires[c.args[1]]
                if isinstance(lhs, int) and isinstance(rhs, int):
                    wires[c.dest] = wires[c.args[0]] | wires[c.args[1]]
            elif c.op == "LSHIFT":
                if isinstance(wires[c.args[0]], int):
                    wires[c.dest] = wires[c.args[0]] << c.args[1]
            elif c.op == "RSHIFT":
                if isinstance(wires[c.args[0]], int):
                    wires[c.dest] = wires[c.args[0]] >> c.args[1]
            elif c.op == "NOT":
                if isinstance(wires[c.args[0]], int):
                    wires[c.dest] = ~wires[c.args[0]] & 65535
    return wires


def part1(circuits: List[Circuit]):
    wires = run_circuits(circuits)
    return str(wires["a"])


def part2(circuits: List[Circuit]):
    # if this wasn't so fast, there would need to be a way for part 2 to otherwise know the result of part 1. this
    # interface was made in 2020 (mostly) and tweaked in 2021... if it turns out more common than i remember for old
    # puzzles to have interaction between the parts like this, it may make some sense to plan for shared state or
    # similar.
    wires = run_circuits(circuits)
    wires = run_circuits(circuits, override={"b": wires["a"]})
    return str(wires["a"])


tests = [
    (
        """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
""",
        {
            "d": 72,
            "e": 507,
            "f": 492,
            "g": 114,
            "h": 65412,
            "i": 65079,
            "x": 123,
            "y": 456,
        },
        run_circuits,
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
