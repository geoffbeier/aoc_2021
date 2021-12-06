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

aoc_day = 10


@dataclass
class AOCContext:
    raw: List[str]
    start: str


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    start = raw[0].strip()
    context = AOCContext(raw, start)
    return context


def get_run(digits: List[str]):
    run = [digits.pop(0)]
    while digits and digits[0] == run[0]:
        run.append(digits.pop(0))
    return run


def play(digits: List[str]):
    result = []
    logger.debug(f"playing {digits}")
    while len(digits):
        current_run = get_run(digits)
        logger.debug(f"got run: {current_run}")
        logger.debug(f"run: {len(current_run)} {current_run[0]}")
        result.append(str(len(current_run)))
        result.append(current_run[0])
    return str("".join(result))


def playtest(context: AOCContext):
    digits = list(context.start)
    for i in range(5):
        digits = list(play(digits))
        logger.debug(f"{''.join(digits)}")
    return "".join(digits)


# adapted from https://www.rosettacode.org/wiki/Look-and-say_sequence#Python
def look_and_say(digits: str):
    while True:
        yield digits
        digits = "".join(str(len(list(g))) + k for k, g in itertools.groupby(digits))


def part1(context: AOCContext):
    digits = context.start
    results = list(itertools.islice(look_and_say(digits), 41))[-1]
    return str(len(results))


def part2(context: AOCContext):
    digits = context.start
    results = list(itertools.islice(look_and_say(digits), 51))[-1]
    return str(len(results))


tests = [
    (
        """1
""",
        "312211",
        playtest,
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
