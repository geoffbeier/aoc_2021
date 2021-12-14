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

aoc_day = 3
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
    triangles: List[Tuple[int, int, int]]
    triangles2: List[Tuple[int, int, int]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    triangles = []
    a = []
    b = []
    c = []
    for line in raw:
        triangles.append(tuple(int(x) for x in line.split(maxsplit=2)))
        a.append(triangles[-1][0])
        b.append(triangles[-1][1])
        c.append(triangles[-1][2])

    triangles3 = [tuple(a[i : i + 3]) for i in range(0, len(triangles), 3)]
    triangles3.extend([tuple(b[i : i + 3]) for i in range(0, len(triangles), 3)])
    triangles3.extend([tuple(c[i : i + 3]) for i in range(0, len(triangles), 3)])

    assert triangles3[0][0] == 775 and triangles3[0][1] == 622
    context = AOCContext(raw, triangles, triangles3)

    return context


def valid(triangle):
    return (
        triangle[0] + triangle[1] > triangle[2]
        and triangle[0] + triangle[2] > triangle[1]
        and triangle[1] + triangle[2] > triangle[0]
    )


def part1(context: AOCContext):
    return str(sum(valid(t) for t in context.triangles))


def part2(context: AOCContext):
    return str(sum(valid(t) for t in context.triangles2))


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
