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

aoc_day = 19
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
    replacements: List[Tuple[str, str]]
    starting_molecule: str


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    replacements = []
    for line in raw:
        if not line.strip():
            break
        lhs, rhs = line.split(" => ")
        replacements.append((lhs, rhs))
    starting_molecule = raw[-1]
    context = AOCContext(raw, replacements, starting_molecule)
    return context


def part1(context: AOCContext):
    new_molecules = set()
    for r in context.replacements:
        start = context.starting_molecule
        start_idx = 0
        found = start.find(r[0], start_idx)
        while found != -1:
            new_molecules.add(start[:found] + start[found:].replace(r[0], r[1], 1))
            start_idx = found + 1
            found = start.find(r[0], start_idx)
    return str(len(new_molecules))


def part2(context: AOCContext):
    # after several false starts, it looks like the way to do this is to
    # essentially reverse part one. i.e. replace the right side of the input
    # with the left side of the input, starting from the right side of the molecule,
    # until nothing but e is left. depending on the input, sorting the replacements by
    # length (descending) should be enough to get close to the fewest possible steps...
    # if it's not, buckets of lengths and shuffling within those should do.
    steps = 0
    reverse_replacements = {r[1]: r[0] for r in context.replacements}
    keys = sorted(reverse_replacements.keys(), key=lambda x: len(x), reverse=True)
    molecule = context.starting_molecule
    while molecule != "e":
        for k in keys:
            found = molecule.rfind(k)
            if found != -1:
                molecule = molecule[:found] + molecule[found:].replace(
                    k, reverse_replacements[k]
                )
                steps += 1
                break
    return str(steps)


tests = [
    (
        """H => HO
H => OH
O => HH

HOH
""",
        4,
        part1,
    ),
    (
        """e => H
e => O
H => HO
H => OH
O => HH

HOH
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
        if f"{result}" != f"{t[1]}":
            logger.error(f"Test {start + i + 1} failed: got {result}, expected {t[1]}")
            break
        else:
            logger.success(f"Test {start + i + 1}: {t[1]}")


if __name__ == "__main__":
    test()
