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

aoc_day = 24
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
    weights: List[int]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    weights = [int(line) for line in raw]
    context = AOCContext(raw, weights)
    return context


def get_groupings_of_size(packages, target_weight, num_pkgs):
    candidate_groupings = set()
    min_first_weight = int(target_weight / num_pkgs + num_pkgs / 2)
    for combo in itertools.combinations(sorted(packages, reverse=True), num_pkgs):
        if sum(combo) == target_weight:
            candidate_groupings.add((combo, tuple(set(packages).difference(combo))))
        if min_first_weight > combo[0]:
            break
    return candidate_groupings


def get_group_candidates(packages, target_weight):
    subgroups = set()
    max_count_per_group = len(packages) // 2 + len(packages) % 2
    for n in range(1, max_count_per_group):
        subgroups.update(get_groupings_of_size(packages, target_weight, n))
        if subgroups:
            break
    return subgroups


class PackageSorter:
    packages: List[int]
    group_count: int
    target_group_weight: int

    def __init__(self, context: AOCContext, group_count: int):
        self.packages = sorted(context.weights, reverse=True)
        self.group_count = group_count
        # it is easier if we assume only one package of each weight
        assert len(self.packages) == len(set(self.packages))
        # this won't work at all if package weight can't be evenly divided across the groups.
        total_weight = sum(self.packages)
        assert total_weight % self.group_count == 0
        self.target_group_weight = total_weight // self.group_count

    def get_best_quantum_entanglement(self):
        min_QE = None
        for first_group, remaining in get_group_candidates(
            self.packages, self.target_group_weight
        ):
            if get_group_candidates(remaining, self.target_group_weight):
                QE = 1
                for package in first_group:
                    QE *= package
                if min_QE is None or min_QE > QE:
                    min_QE = QE
        return min_QE


def part1(context: AOCContext):
    sorter = PackageSorter(context, 3)
    return str(sorter.get_best_quantum_entanglement())


def part2(context: AOCContext):
    sorter = PackageSorter(context, 4)
    return str(sorter.get_best_quantum_entanglement())


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
