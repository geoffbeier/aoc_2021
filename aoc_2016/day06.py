import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple, Counter
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 6
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
    cols: List[str]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    # get columns from a list of strings... this is needed often enough I should camp it in a utils library.
    # almost all of the time spent on this puzzle was figuring this out for the 10th time.
    cols = list("".join(list(c[i] for c in raw)) for i in range(len(raw[0])))
    context = AOCContext(raw, cols)
    return context


def part1(context: AOCContext):
    message = ""
    for c in context.cols:
        frequencies = Counter(c)
        message += frequencies.most_common(1)[0][0]
    return str(message)


def part2(context: AOCContext):
    message = ""
    for c in context.cols:
        frequencies = Counter(c)
        message += frequencies.most_common()[-1][0]
    return str(message)


tests = [
    (
        """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
""",
        "easter",
        part1,
    ),
    (
        """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
""",
        "advent",
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
