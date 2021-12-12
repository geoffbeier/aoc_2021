import re
import sys
from dataclasses import dataclass
from functools import cache
from typing import List, Tuple

import aocd
from loguru import logger

from . import aoc_year

aoc_day = 12
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
    segments: Tuple[Tuple[str, str]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    segments: List[Tuple[str, str]] = []
    for line in raw:
        first, second = line.split("-")
        if first != "end" and second != "start":
            segments.append((first, second))
        if first != "start" and second != "end":
            segments.append((second, first))
    context = AOCContext(raw, tuple(segments))
    return context


@cache
def get_next_caves(tail, segments):
    return [s[1] for s in filter(lambda x: x[0] == tail, segments)]


def part1(context: AOCContext):
    candidates = list(filter(lambda s: s[0] == "start", context.segments))
    paths = []
    while len(candidates):
        path = candidates.pop()
        candidate_tail = path[-1]
        if candidate_tail == "end":
            paths.append(path)
            continue
        for r in get_next_caves(candidate_tail, context.segments):
            if r in path and r.islower():
                continue
            candidates.append([*path, r])
    return str(len(paths))


# two things were making my part 2 slow:
# 1. counting visits to nodes in candidate paths too often
# 2. finding the possible next caves.
# To solve the first, I store each candidate as a (path, flag) tuple where flag is True if
# it's still ok to double visit a small cave.
# For the second, I converted the list of path segments to tuples so that it's immutable and
# hashable, then moved the call to a function and used functools.cache. This took part2 runtime
# on my AoC input from 6+ seconds to 715ms.
#
# Part 1 got the same treatment applied even though it didn't matter much there.
def part2(context: AOCContext):
    candidates = [
        (list(p), True)
        for p in filter(lambda s: s[0] == "start", list(context.segments))
    ]
    paths = []
    while len(candidates):
        path, can_double_small = candidates.pop()
        candidate_tail = path[-1]
        if candidate_tail == "end":
            paths.append(path)
            continue
        for r in get_next_caves(candidate_tail, context.segments):
            double_visiting_small = False
            if r in path and r.islower():
                if not can_double_small:
                    continue
                else:
                    double_visiting_small = True
            candidates.append(
                ([*path, r], can_double_small and not double_visiting_small)
            )
    return str(len(paths))


tests = [
    (
        """start-A
start-b
A-c
A-b
b-d
A-end
b-end
""",
        10,
        part1,
    ),
    (
        """start-A
start-b
A-c
A-b
b-d
A-end
b-end
""",
        36,
        part2,
    ),
    (
        """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""",
        103,
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
