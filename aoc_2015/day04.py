from dataclasses import dataclass
from math import prod
from typing import List, Dict
import aocd
from . import aoc_year
from loguru import logger

import _md5

aoc_day = 4


def preprocess():
    return aocd.get_data(day=aoc_day, year=aoc_year).splitlines()[0]


def find_suffix(secret: str, prefix: str = "00000"):
    i = 0
    found = False
    while not found:
        i += 1
        digest = _md5.md5(f"{secret}{i}".encode()).hexdigest()
        if digest.startswith(prefix):
            return i


def part1(secret: str):
    return str(find_suffix(secret, "00000"))


def part2(secret: str):
    return str(find_suffix(secret, "000000"))


tests = [
    (
        """abcdef
""",
        "609043",
        part1,
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
