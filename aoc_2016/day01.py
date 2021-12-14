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

aoc_day = 1
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
    directions: List[Tuple[str, int]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    directions = []
    for step in raw[0].split(", "):
        directions.append((step[0], int(step[1:])))
    context = AOCContext(raw, directions)
    return context


Point = namedtuple("Point", "x y")


def part1(context: AOCContext):
    start = Point(0, 0)
    current = start
    vectors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    heading = 0
    for step in context.directions:
        if step[0] == "R":
            heading += 1
        elif step[0] == "L":
            heading -= 1
        vector = vectors[heading % len(vectors)]
        current = Point(
            current.x + step[1] * vector[0], current.y + step[1] * vector[1]
        )
        logger.debug(f"{step} -> {current}")
    logger.info(f"Final destination: {current}")
    distance = abs(current.x - start.x) + abs(current.y - start.y)
    return str(distance)


def part2(context: AOCContext):
    start = Point(0, 0)
    current = start
    vectors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    heading = 0
    visited = set()
    for step in context.directions:
        if step[0] == "R":
            heading += 1
        elif step[0] == "L":
            heading -= 1
        vector = vectors[heading % len(vectors)]
        blocks = []
        for _ in range(step[1]):
            current = Point(current.x + vector[0], current.y + vector[1])
            if current in visited:
                logger.info(f"Second visit to {current}")
                break
            visited.add(current)
        else:
            continue
        break
    logger.info(f"stopping at: {current}")
    distance = abs(current.x - start.x) + abs(current.y - start.y)
    return str(distance)


tests = [
    (
        """R2, R2, R2
""",
        2,
        part1,
    ),
    (
        """R8, R4, R4, R8
""",
        4,
        part2,
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
