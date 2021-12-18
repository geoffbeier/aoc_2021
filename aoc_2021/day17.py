import re
import sys
from collections import namedtuple
from dataclasses import dataclass
from itertools import product
from typing import List, Tuple, Set

import aocd
from loguru import logger

from . import aoc_year

aoc_day = 17
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
    hit_points: Set[Point]
    start_point: Point
    hit_ivs: Set[Tuple[int, int]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    min_x, max_x, min_y, max_y = map(
        int,
        re.match(
            r"target area: x=(-?\d+?)..(-?\d+?), y=(-?\d+?)..(-?\d+?)$", raw[0]
        ).groups(),
    )
    hit_points = set()
    for p in product(range(min_x, max_x + 1), range(min_y, max_y + 1)):
        hit_points.add(Point(*p))
    context = AOCContext(raw, hit_points, Point(0, 0), set())
    return context


def part1(context: AOCContext):
    start = context.start_point
    min_y, max_y = min(p.y for p in context.hit_points), max(
        p.y for p in context.hit_points
    )
    min_x, max_x = min(p.x for p in context.hit_points), max(
        p.x for p in context.hit_points
    )
    peak_y = min_y

    def _add_pairs(l, r):
        return tuple(map(sum, zip(l, r)))

    logger.debug(f"Hello brute force my old friend...")
    for dx, dy in product(
        range(1, max_x * 4), range(-4 * (max_y - min_y), 4 * (max_y - min_y))
    ):
        local_peak = min_y
        curr_point = start
        curr_v = (dx, dy)
        while curr_point.x < max_x and curr_point.y > min_y:
            curr_point = Point(*_add_pairs(tuple(curr_point), curr_v))
            curr_v = _add_pairs(curr_v, (-1 if curr_v[0] > 0 else 0, -1))
            local_peak = max(curr_point.y, local_peak)
            if curr_point in context.hit_points:
                context.hit_ivs.add((dx, dy))
                peak_y = max(local_peak, peak_y)
    return str(peak_y)


def part2(context: AOCContext):
    if not context.hit_ivs:
        part1(context)
    return str(len(context.hit_ivs))


tests = [
    (
        """target area: x=20..30, y=-10..-5
""",
        45,
        part1,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    for i, t in enumerate(tests[start:finish]):
        aocd.get_data = lambda *_, **__: t[0]
        result = t[2](preprocess())
        if f"{result}" != f"{t[1]}":
            logger.error(f"Test {start + i + 1} failed: got {result}, expected {t[1]}")
            break
        else:
            logger.success(f"Test {start + i + 1}: {t[1]}")


if __name__ == "__main__":
    test()
