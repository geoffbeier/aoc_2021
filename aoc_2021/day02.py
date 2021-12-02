from dataclasses import dataclass
from math import prod
from typing import List, Dict
import aocd
from . import aoc_year
from loguru import logger

from collections import defaultdict

aoc_day = 2


def preprocess():
    return aocd.get_data(day=aoc_day, year=aoc_year).splitlines()


@dataclass
class Position:
    horizontal: int
    depth: int
    aim: int


def part1(plan: List[str]):
    pos = Position(0, 0, 0)
    for step in plan:
        direction, magnitude = step.split(" ")
        magnitude = int(magnitude)
        if direction == "forward":
            pos.horizontal += magnitude
        elif direction == "down":
            pos.depth += magnitude
        elif direction == "up":
            pos.depth -= magnitude
    return str(pos.horizontal * pos.depth)


def part2(plan: List[str]):
    pos = Position(0, 0, 0)
    for step in plan:
        direction, magnitude = step.split(" ")
        magnitude = int(magnitude)
        if direction == "forward":
            pos.horizontal += magnitude
            pos.depth += pos.aim * magnitude
        elif direction == "down":
            pos.aim += magnitude
        elif direction == "up":
            pos.aim -= magnitude
    return str(pos.horizontal * pos.depth)


tests = [
    (
        """forward 5
down 5
forward 8
up 3
down 8
forward 2
""",
        150,
        part1,
    ),
    (
        """forward 5
down 5
forward 8
up 3
down 8
forward 2
""",
        900,
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
