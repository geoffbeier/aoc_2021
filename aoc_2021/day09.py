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

aoc_day = 9
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
    height_map: List[List[int]]
    map_w: int
    map_h: int


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    height_map = []
    for line in raw:
        line = line.strip()
        height_map.append([int(x) for x in list(line)])
    map_w = len(height_map[0])
    map_h = len(height_map)
    context = AOCContext(raw, height_map, map_w, map_h)
    return context


def neighbors(context: AOCContext, x: int, y: int):
    if y > 0:
        yield (x, y - 1), context.height_map[y - 1][x]
    if y < context.map_h - 1:
        yield (x, y + 1), context.height_map[y + 1][x]
    if x > 0:
        yield (x - 1, y), context.height_map[y][x - 1]
    if x < context.map_w - 1:
        yield (x + 1, y), context.height_map[y][x + 1]


def basin(
    context: AOCContext, x: int, y: int, visited: Set[Tuple[Tuple[int, int], int]]
):
    basin_points = [((x, y), context.height_map[y][x])]
    for neighbor in neighbors(context, x, y):
        if neighbor[1] < 9:
            basin_points.append(neighbor)
            if neighbor not in visited:
                visited.add(neighbor)
                basin_points.extend(
                    basin(context, neighbor[0][0], neighbor[0][1], visited)
                )
    return set(basin_points)


def low_points(context: AOCContext):
    points = []
    for y in range(context.map_h):
        for x in range(context.map_w):
            test_point = context.height_map[y][x]
            if all(test_point < p[1] for p in neighbors(context, x, y)):
                logger.debug(
                    f"test_point({x},{y})={test_point} < all neighbors: {list(neighbors(context, x, y))}"
                )
                points.append(((x, y), test_point))
    return points


def part1(context: AOCContext):
    lowest_points = low_points(context)
    risk_level = sum(p[1] + 1 for p in lowest_points)
    logger.debug(f"low_points: {lowest_points}")
    return str(risk_level)


def part2(context: AOCContext):
    basins = []
    lowest_points = low_points(context)
    for p in lowest_points:
        basins.append(list(basin(context, p[0][0], p[0][1], set())))
    logger.debug(f"found {len(basins)}")
    basin_sizes = sorted([len(b) for b in basins])
    return str(prod(basin_sizes[-3:]))


tests = [
    (
        """2199943210
3987894921
9856789892
8767896789
9899965678
""",
        15,
        part1,
    ),
    (
        """2199943210
3987894921
9856789892
8767896789
9899965678
""",
        1134,
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
