import re
import sys
from dataclasses import dataclass

import aocd
from loguru import logger

from . import aoc_year

aoc_day = 9
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
    raw: str


def preprocess():
    raw = "".join(aocd.get_data(day=aoc_day, year=aoc_year).splitlines())
    context = AOCContext(raw)
    return context


def read_marker(data: str):
    cur = 0
    marker = ""
    assert data[cur] == "("
    cur += 1
    while data[cur] != ")":
        marker += data[cur]
        cur += 1
    cur += 1
    length, count = [int(n) for n in marker.split("x")]
    return length, count, cur


def find_decompressed_length(data: str, version: int = 1):
    chars_out = 0
    cur = 0
    while cur < len(data):
        if data[cur] == "(":
            length, count, consumed = read_marker(data[cur:])
            cur += consumed
            if version == 1:
                chars_out += length * count
            elif version == 2:
                chars_out += count * find_decompressed_length(
                    data[cur : cur + length], version
                )
            else:
                logger.error(f"Bad version.")
                return -1
            cur += length
        else:
            cur += 1
            chars_out += 1
    return chars_out


def part1(context: AOCContext):
    chars_out = find_decompressed_length(context.raw)
    return str(chars_out)


def part2(context: AOCContext):
    chars_out = find_decompressed_length(context.raw, 2)
    return str(chars_out)


tests = [
    (
        """ADVENT
""",
        6,
        part1,
    ),
    (
        """A(1x5)BC
""",
        7,
        part1,
    ),
    (
        """(3x3)XYZ
""",
        9,
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
