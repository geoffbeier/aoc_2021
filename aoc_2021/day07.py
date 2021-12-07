import itertools
import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 7


@dataclass
class AOCContext:
    raw: List[str]
    positions: List[int]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    positions = [int(x) for x in raw[0].split(",")]
    context = AOCContext(raw, positions)
    return context


def part1(context: AOCContext):
    crab_positions = sorted(context.positions)
    logger.info(
        f"{len(crab_positions)} crab_positions from {crab_positions[0]},{crab_positions[-1]}"
    )
    fuel_use = {
        sum(abs(p - x) for x in crab_positions): p
        for p in range(crab_positions[0], crab_positions[-1])
    }
    min_fuel = min(fuel_use.keys())
    min_pos = fuel_use[min_fuel]
    logger.info(f"smallest amount of fuel used is {min_fuel} at position {min_pos}")
    return str(min_fuel)


def part2(context: AOCContext):
    crab_positions = sorted(context.positions)
    logger.info(
        f"{len(crab_positions)} crab_positions from {crab_positions[0]},{crab_positions[-1]}"
    )
    fuel_use = {
        sum(int(abs(p - x) * (abs(p - x) + 1) / 2) for x in crab_positions): p
        for p in range(crab_positions[0], crab_positions[-1])
    }
    min_fuel = min(fuel_use.keys())
    min_pos = fuel_use[min_fuel]
    logger.info(f"smallest amount of fuel used is {min_fuel} at position {min_pos}")
    return str(min_fuel)


tests = [
    (
        """16,1,2,0,4,2,7,1,2,14
""",
        37,
        part1,
    ),
    (
        """16,1,2,0,4,2,7,1,2,14
""",
        168,
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
