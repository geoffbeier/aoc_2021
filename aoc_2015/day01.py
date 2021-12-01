from typing import List, Any, Dict, Tuple, Pattern
import aocd
from loguru import logger
from . import aoc_year

aoc_day = 1


def preprocess():
    return aocd.get_data(day=aoc_day, year=aoc_year).splitlines()


def part1(data: List[str]):
    starting_floor = 0
    floor = starting_floor + data[0].count("(") - data[0].count(")")
    return f"{floor}"


def part2(data: List[str]):
    floor = starting_floor = 0
    ending_char = len(data[0])
    for pos, c in enumerate(data[0], 1):
        if c == "(":
            floor += 1
        elif c == ")":
            floor -= 1
        if floor < 0:
            ending_char = pos
            break
    return f"{ending_char}"


tests = [
    (
        """(())
""",
        0,
        part1,
    ),
    (
        """()()
""",
        0,
        part1,
    ),
    (
        """))(((((
""",
        3,
        part1,
    ),
    (
        """)())())
""",
        -3,
        part1,
    ),
    (
        """()())
""",
        5,
        part2,
    ),
    (
        """)
""",
        1,
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
    test(4)
