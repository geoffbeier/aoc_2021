import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 10
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
    position: Tuple[int, int]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    guide_exp = r".*.row (\d+?), column (\d+?).$"
    row, col = (int(x) for x in re.match(guide_exp, raw[0]).groups())
    context = AOCContext(raw, (row, col))
    return context


def next_code(code: int):
    return (code * 252533) % 33554393


def code_for_position(row: int, col: int, start: int = 20151125):
    n_code = sum(range(row + col - 1)) + col
    current_code = start
    for _ in range(1, n_code):
        current_code = next_code(current_code)
    return current_code


def part1(context: AOCContext):
    return str(code_for_position(context.position[0], context.position[1]))


def part2(context: AOCContext):
    ...
    return str(None)


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
