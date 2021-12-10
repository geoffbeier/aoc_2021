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


def elves(house: int):
    # https://stackoverflow.com/a/6800214
    factors = reduce(
        list.__add__,
        ([i, house // i] for i in range(1, int(house ** 0.5) + 1) if house % i == 0),
    )
    return set(factors)


def presents_delivered(house):
    return sum(elves(house)) * 10


def part1(context: AOCContext):
    house = 1000000
    delivered = presents_delivered(house)
    while delivered < context.presents:
        ee = elves(house)
        logger.debug(f"{ee} delivered({house}): {delivered} < {context.presents}")
        house += 1
        delivered = presents_delivered(house)
    return str(house)


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
