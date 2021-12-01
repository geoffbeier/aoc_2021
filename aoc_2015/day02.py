from dataclasses import dataclass
from math import prod
from typing import List
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 2


@dataclass
class Box:
    l: int
    w: int
    h: int

    def paper_required(self):
        sides = [self.l * self.w, self.w * self.h, self.h * self.l]
        return sum(2 * s for s in sides) + min(sides)

    def ribbon_required(self):
        sorted_sides = sorted([self.l, self.w, self.h])
        ribbon = 2 * sorted_sides[0] + 2 * sorted_sides[1]
        bow = prod(sorted_sides)
        return ribbon + bow


def preprocess():
    dimensions = []
    for line in aocd.get_data(day=aoc_day, year=aoc_year).splitlines():
        l, w, h = line.split("x")
        dimensions.append(Box(l=int(l), w=int(w), h=int(h)))
    return dimensions


def part1(measurements: List[Box]):
    return str(sum(b.paper_required() for b in measurements))


def part2(measurements: List[Box]):
    return str(sum(b.ribbon_required() for b in measurements))


tests = [
    (
        """2x3x4
1x1x10
""",
        34 + 14,
        part2,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    for i, t in enumerate(tests[start:finish]):

        def gd(*args, **kwargs):
            return t[0]

        aocd.get_data = gd
        result = t[2](preprocess())
        if result != f"{t[1]}":
            logger.error(f"Test {start + i + 1} failed: got {result}, expected {t[1]}")
            break
        else:
            logger.success(f"Test {start + i + 1}: {t[1]}")


if __name__ == "__main__":
    test()
