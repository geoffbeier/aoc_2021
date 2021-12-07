import itertools
import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from functools import cache
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple, Iterable
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 13


@dataclass
class AOCContext:
    raw: List[str]
    mappings: Dict[str, Dict[str, int]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    mappings = defaultdict(dict)
    assignment = r"(.*) would (gain|lose) (\d+?) .*.next to (.*).$"
    for line in raw:
        if not line:
            continue
        line = line.strip()
        person1, sign, amount, person2 = re.match(assignment, line).groups()
        sign = -1 if sign == "lose" else 1
        mappings[person1][person2] = sign * int(amount)
    context = AOCContext(raw, mappings)
    return context


class Table:
    def __init__(self, arrangement: Iterable[str]):
        self.seats = list(arrangement)

    @cache
    def left_of(self, occupant: str):
        pos = self.seats.index(occupant)
        return self.seats[pos - 1]

    @cache
    def right_of(self, occupant: str):
        pos = self.seats.index(occupant)
        return self.seats[0 if pos == len(self.seats) - 1 else pos + 1]


def max_happiness(happiness_mappings: Dict[str, Dict[str, int]]):
    attendees = happiness_mappings.keys()
    arrangements = list(itertools.permutations(attendees, len(attendees)))
    logger.debug(f"checking {len(arrangements)} arrangements ({arrangements})")
    max_happiness = None
    for arrangement in arrangements:
        table = Table(arrangement)
        happiness = sum(
            happiness_mappings[occupant][table.left_of(occupant)]
            + happiness_mappings[occupant][table.right_of(occupant)]
            for occupant in arrangement
        )
        if not max_happiness:
            max_happiness = happiness
        else:
            max_happiness = max(happiness, max_happiness)
    return max_happiness


def part1(context: AOCContext):
    return str(max_happiness(context.mappings))


def part2(context: AOCContext):
    attendees = list(context.mappings.keys())
    my_happiness = {}
    for a in attendees:
        context.mappings[a]["me"] = 0
        my_happiness[a] = 0
    context.mappings["me"] = my_happiness
    return str(max_happiness(context.mappings))


tests = [
    (
        """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
""",
        330,
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
