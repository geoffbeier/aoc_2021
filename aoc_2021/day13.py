import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple, Set
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 13
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


Point = namedtuple("Point", "x y")


@dataclass
class AOCContext:
    raw: List[str]
    visible_dots: Set[Point]
    folds: List[Tuple[str, int]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    visible_dots = set()
    fl = 0
    folds = []
    for i, line in enumerate(raw):
        if not line:
            fl = i + 1
            break
        x, y = line.split(",")
        visible_dots.add(Point(int(x), int(y)))
    for line in raw[fl:]:
        axis, location = line.split("=")
        axis = axis.split()
        axis = axis[-1]
        folds.append((axis, int(location)))

    context = AOCContext(raw, visible_dots, folds)
    return context


def fold(visible_dots: Set[Point], direction: str, location: int):
    updated_visible_dots = visible_dots.copy()
    past_the_fold = set(
        filter(lambda p: getattr(p, direction) > location, updated_visible_dots)
    )
    updated_visible_dots.difference_update(past_the_fold)
    for dot in past_the_fold:
        if direction == "x":
            new_dot = Point(dot.x - (2 * (dot.x - location)), dot.y)
        elif direction == "y":
            new_dot = Point(dot.x, dot.y - 2 * (dot.y - location))
        else:
            raise ValueError(f"Unexpected direction: {direction}")
        updated_visible_dots.add(new_dot)
    return updated_visible_dots


def part1(context: AOCContext):
    direction, loc = context.folds[0]
    visible_dots = fold(context.visible_dots, direction, loc)
    return str(len(visible_dots))


def print_visible(points: Set[Point], fill: str = "."):
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    for y in range(max_y + 1):
        line = []
        for x in range(max_x + 1):
            if Point(x, y) in points:
                line.append("#")
            else:
                line.append(fill)
        print("".join(line))


def part2(context: AOCContext):
    visible_dots = context.visible_dots
    for direction, loc in context.folds:
        logger.info(f"Folding along {direction}={loc}")
        visible_dots = fold(visible_dots, direction, loc)
    print_visible(visible_dots, fill=" ")
    return str(None)


tests = [
    (
        """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""",
        17,
        part1,
    ),
    (
        """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""",
        None,
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
