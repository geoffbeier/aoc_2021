import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

from _md5 import md5

aoc_day = 5
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
    door_id: str


def next_digit(door_id: str, next_index: int, prefix: str = "00000"):
    found = False
    i = next_index
    while not found:
        digest = md5(f"{door_id}{i}".encode()).hexdigest()
        i += 1
        if digest.startswith(prefix):
            return digest, i


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    door_id = raw[0].strip()
    context = AOCContext(raw, door_id)
    return context


def part1(context: AOCContext):
    password = ""
    next_i = 0
    for _ in range(8):
        digest, next_i = next_digit(context.door_id, next_i)
        c = digest[5]
        password += c
        logger.debug(f"password={password}")
    return str(password)


def part2(context: AOCContext):
    password = "--------"
    next_i = 0
    while "-" in password:
        digest, next_i = next_digit(context.door_id, next_i)
        pos = int(digest[5], 16)
        c = digest[6]
        if pos < len(password) and password[pos] == "-":
            password = password[:pos] + c + password[pos + 1 :]
            assert len(password) == 8
            logger.debug(f"password={password}")
    return str(password)


tests = [
    (
        """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
""",
        605,
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
