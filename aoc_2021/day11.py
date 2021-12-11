import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from functools import cache
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple, Set
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 11
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
    swarm: Any = None


class OctopusSwarm:
    def __init__(self, context: AOCContext):
        self.grid = []
        for line in context.raw:
            self.grid.append([int(x) for x in list(line)])
        self.grid_w = len(self.grid[0])
        self.grid_h = len(self.grid)
        self.steps = 0

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

    def increment_all(self):
        # this might argue for numpy if runtimes get long
        for y, row in enumerate(self.grid):
            row = [v + 1 for v in row]
            self.grid[y] = row

    def flash(self, x, y, flashed: Set[Tuple[int, int]]):
        self.grid[y][x] = 0
        flashed.add((x, y))
        for nx, ny in self.find_neighbors(x, y):
            if (nx, ny) not in flashed:
                self.grid[ny][nx] += 1
                if self.grid[ny][nx] >= 10:
                    self.flash(nx, ny, flashed)

    def step(self):
        self.steps += 1
        flashed = set()
        self.increment_all()
        round_flashed = -1
        while round_flashed != 0:
            round_flashed = len(flashed)
            for y, row in enumerate(self.grid):
                for x, col in enumerate(row):
                    if col >= 10:
                        self.flash(x, y, flashed)
            round_flashed = len(flashed) - round_flashed
        return len(flashed)


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    context = AOCContext(raw)
    return context


def part1(context: AOCContext):
    swarm = OctopusSwarm(context)
    total_flashes = 0
    for i in range(100):
        flashes = swarm.step()
        logger.debug(f"Round {i+1}: {flashes} flashed")
        for row in swarm.grid:
            logger.debug("".join(str(c) for c in row))
        total_flashes += flashes
    context.swarm = swarm
    return str(total_flashes)


def part2(context: AOCContext):
    swarm = context.swarm or OctopusSwarm(context)
    flashes = 0
    while flashes < 100:
        flashes = swarm.step()
    return str(swarm.steps)


tests = [
    (
        """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""",
        1656,
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
