from dataclasses import dataclass
from math import prod
from typing import List, Dict
import aocd
from . import aoc_year
from loguru import logger

from collections import defaultdict

aoc_day = 3


def preprocess():
    return aocd.get_data(day=aoc_day, year=aoc_year).splitlines()[0]


@dataclass
class Point:
    x: int
    y: int


def get_visited_houses(directions: str, santa_count: int = 1):
    visits = defaultdict(int)
    santas = [Point(0, 0) for _ in range(santa_count)]
    for n, point in enumerate(santas):
        visits[point.x, point.y] += 1
    for n, char in enumerate(directions):
        current_santa_index = n % santa_count
        current_santa = santas[current_santa_index]
        if char == "^":
            current_santa.y += 1
        elif char == ">":
            current_santa.x += 1
        elif char == "<":
            current_santa.x -= 1
        elif char == "v":
            current_santa.y -= 1
        visits[current_santa.x, current_santa.y] += 1
    return visits


def part1(directions: str):
    visits = get_visited_houses(directions, 1)
    return str(len(visits.keys()))


def part2(directions: str):
    visits = get_visited_houses(directions, 2)
    return str(len(visits.keys()))


tests = [
    (
        """>
""",
        2,
        part1,
    ),
    (
        """^>v<
""",
        4,
        part1,
    ),
    (
        """^v
""",
        3,
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
