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

aoc_day = 7
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


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    context = AOCContext(raw)
    return context


def contains_abba(address: str):
    for i, c in enumerate(address):
        if c == "[" or c == "]":
            continue
        if i >= len(address) - 3:
            return False
        if (
            address[i + 1] == address[i + 2]
            and address[i] == address[i + 3]
            and address[i] != address[i + 1]
        ):
            return True
    return False


def part1(context: AOCContext):
    found = 0
    for line in context.raw:
        if contains_abba(line):
            tls = True
            for x in re.findall(r"\[.+?]", line):
                if contains_abba(x):
                    tls = False
            if tls:
                found += 1
    return str(found)


def part2(context: AOCContext):
    found_ssl = 0
    for line in context.raw:
        hypernet_segments = re.sub(r"\[.*?]", " ", line).split()
        abas = []
        babs = []
        for seg in hypernet_segments:
            for triple in zip(seg, seg[1:], seg[2:]):
                if triple[0] != triple[1] and triple[0] == triple[2]:
                    abas.append("".join(triple))
                    babs.append(triple[1] + triple[0] + triple[1])
        if abas:
            ssl = False
            for bab in babs:
                for x in re.findall(r"\[.+?]", line):
                    if bab in x:
                        ssl = True
            if ssl:
                found_ssl += 1
    return str(found_ssl)


tests = [
    (
        """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
""",
        2,
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
