import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from functools import cache, lru_cache
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple, Set
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 18
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


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    context = AOCContext(raw)
    return context


class LightDisplay:
    context: AOCContext
    grid_h: int
    grid_w: int
    lit: Set[Tuple[int, int]]
    always_on: Set[Tuple[int, int]]

    def __init__(self, context: AOCContext, always_on=None):
        self.context = context
        self.grid_h = len(context.raw)
        self.grid_w = len(context.raw[0])
        if always_on:
            self.always_on = always_on
        else:
            self.always_on = set()
        self.lit = self.get_starting_configuration()

    def get_starting_configuration(self):
        return {
            (x, y)
            for y, x in product(range(self.grid_w), range(self.grid_h))
            if self.context.raw[y][x] == "#" or (x, y) in self.always_on
        }

    def find_neighbors(self, x: int, y: int):
        if x > 0:
            yield x - 1, y
            if y > 0:
                yield x - 1, y - 1
            if y < self.grid_h - 1:
                yield x - 1, y + 1
        if x < self.grid_w - 1:
            yield x + 1, y
            if y > 0:
                yield x + 1, y - 1
            if y < self.grid_h - 1:
                yield x + 1, y + 1
        if y > 0:
            yield x, y - 1
        if y < self.grid_h - 1:
            yield x, y + 1

    @cache
    def get_neighbors(self, x: int, y: int):
        return list(self.find_neighbors(x, y))

    def update(self, cycles: int):
        logger.debug(f"Before update: {len(self.lit)} lights are on.")

        def now_lit(x, y):
            if (x, y) in self.always_on:
                return True
            lit_neighbors = sum(
                (nx, ny) in self.lit for nx, ny in self.get_neighbors(x, y)
            )
            if (x, y) not in self.lit:
                if lit_neighbors == 3:
                    return True
                else:
                    return False
            if (x, y) in self.lit:
                if 2 <= lit_neighbors <= 3:
                    return True
                else:
                    return False

        for c in range(cycles):
            self.lit = {
                (x, y)
                for x, y in product(range(self.grid_w), range(self.grid_h))
                if now_lit(x, y)
            }
            logger.debug(f"After update {c + 1}: {len(self.lit)} lights are on.")


def part1(context: AOCContext):
    display = LightDisplay(context)
    display.update(100)
    return str(len(display.lit))


def part2(context: AOCContext):
    max_x = len(context.raw[0]) - 1
    max_y = len(context.raw) - 1
    always_on = {(0, 0), (0, max_y), (max_x, max_y), (max_x, 0)}
    display = LightDisplay(context, always_on=always_on)
    display.update(100)
    return str(len(display.lit))


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
