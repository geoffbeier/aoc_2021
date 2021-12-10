import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from functools import reduce
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
import numpy

from . import aoc_year
from loguru import logger

aoc_day = 20
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
    presents: int


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    context = AOCContext(raw, int(raw[0]))
    return context


def part1(context: AOCContext):
    min_deliveries = context.presents // 10
    max_houses = min_deliveries
    logger.info(
        f"Finding first house to receive at least {context.presents} presents. Examining up to {max_houses} houses."
    )
    presents_delivered = numpy.zeros(max_houses + 1, dtype=int)
    first_house = 0
    for elf in range(1, max_houses + 1):
        n_visited = max_houses // elf
        visits = elf * numpy.array(range(1, n_visited - 1), dtype=int)
        presents_delivered[visits] += elf * 10
        if presents_delivered[elf] >= context.presents:
            first_house = elf
            break
    return str(first_house)


def part2(context: AOCContext):
    min_deliveries = context.presents // 10
    max_houses = min_deliveries
    logger.info(
        f"Finding first house to receive at least {context.presents} presents. Examining up to {max_houses} houses."
    )
    presents_delivered = numpy.zeros(max_houses + 1, dtype=int)
    first_house = 0
    for elf in range(1, max_houses + 1):
        n_visited = min(50, max_houses // elf)
        visits = elf * numpy.array(range(1, n_visited - 1), dtype=int)
        presents_delivered[visits] += elf * 11
        if presents_delivered[elf] >= context.presents:
            first_house = elf
            break
    return str(first_house)


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
