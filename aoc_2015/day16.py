import itertools
import operator
import re
import sys
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple, Iterable, Callable
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
    sues: Dict[str, Dict[str, int]]
    target: Dict[str, int]
    test_funcs: Dict[str, Callable]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    sues = {}
    for line in raw:
        line = line.strip()
        aunt, attrs = line.split(": ", maxsplit=1)
        sues[aunt] = {}
        for a in attrs.split(", "):
            k, v = a.split(": ")
            sues[aunt][k] = int(v)
    ticker_tape = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""
    target = {}
    test_funcs = {}
    for line in ticker_tape.splitlines():
        line = line.strip()
        k, v = line.split(": ")
        target[k] = int(v)
        if k in ["cats", "trees"]:
            test_funcs[k] = operator.gt
        elif k in ["pomeranians", "goldfish"]:
            test_funcs[k] = operator.lt
        else:
            test_funcs[k] = operator.eq
    context = AOCContext(raw, sues, target, test_funcs)
    return context


def matches_attribute(
    key: str, value: int, candidates: Iterable, compare_func: Callable = operator.eq
):
    for c in candidates:
        if key not in c[1] or compare_func(c[1][key], value):
            yield c


def part1(context: AOCContext):
    matches = context.sues.items()
    for k, v in context.target.items():
        matches = matches_attribute(k, v, matches)
    aunts_found = list(matches)
    if len(aunts_found) != 1:
        raise ValueError(f"Expected to find 1 aunt, found {len(aunts_found)}")
    aunt_num = aunts_found[0][0].split()[1]
    return aunt_num


def part2(context: AOCContext):
    matches = context.sues.items()
    for k, v in context.target.items():
        matches = matches_attribute(k, v, matches, context.test_funcs[k])
    aunts_found = list(matches)
    if len(aunts_found) != 1:
        raise ValueError(f"Expected to find 1 aunt, found {len(aunts_found)}")
    aunt_num = aunts_found[0][0].split()[1]
    return aunt_num


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
