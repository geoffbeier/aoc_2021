import itertools
import re
from collections import defaultdict, namedtuple, Counter
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 6

initial_fish_timer = 8
spawn_reset_timer = 6


@dataclass
class AOCContext:
    raw: List[str]
    ages: List[int]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    context = AOCContext(raw, [int(n) for n in raw[0].split(",")])
    return context


def process_day(fish: Dict[int, int]):
    next_fish = defaultdict(int)
    for age, count in fish.items():
        if age == 0:
            next_fish[spawn_reset_timer] += count
            next_fish[initial_fish_timer] += count
        else:
            next_fish[age - 1] += count
    return next_fish


def simulate(fish_ages: List[int], days: int):
    fish = Counter(fish_ages)
    for day in range(days):
        fish = process_day(fish)
    return fish


def part1(context: AOCContext):
    fish = simulate(context.ages.copy(), 80)
    return str(sum(fish.values()))


def part2(context: AOCContext):
    fish = simulate(context.ages.copy(), 256)
    return str(sum(fish.values()))


tests = [
    (
        """3,4,3,1,2
""",
        5934,
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
