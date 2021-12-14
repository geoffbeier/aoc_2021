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

aoc_day = 10
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
    template: str
    rules: Dict[str, str]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    template = raw[0]
    rules = {}
    for line in raw[2:]:
        pair, insertion = line.split(" -> ")
        rules[pair] = insertion
    context = AOCContext(raw, template, rules)
    return context


def part1(context: AOCContext):
    polymer = context.template
    for i in range(10):
        new_polymer = ""
        for ii, c in enumerate(polymer):
            new_polymer += c
            if ii + 1 < len(polymer):
                pair = f"{c}{polymer[ii+1]}"
                if pair in context.rules:
                    new_polymer += context.rules[pair]
        polymer = new_polymer
        logger.debug(
            f"After step {i+1}: len={len(polymer)} - {polymer[:min(100,len(polymer))]}"
        )
    counter = Counter(list(polymer))
    frequencies = counter.most_common()
    return str(frequencies[0][1] - frequencies[-1][1])


def pairs_to_elements(pair_counts):
    element_counts = Counter()
    for pair, count in pair_counts.items():
        element_counts[pair[0]] += count
        element_counts[pair[1]] += count
    return element_counts


def part2(context: AOCContext):
    polymer = context.template
    pair_counts = Counter(first + second for first, second in zip(polymer, polymer[1:]))
    for i in range(40):
        new_pair_counts = Counter()
        current_pairs = list(pair_counts.keys())
        for p in current_pairs:
            if p in context.rules:
                c = context.rules[p]
                # this is double-counting everything
                new_pair_counts[p[0] + c] += pair_counts[p]
                new_pair_counts[c + p[1]] += pair_counts[p]
            else:
                new_pair_counts[p] += pair_counts[p]
        logger.debug(f"after {i+1}: {new_pair_counts}")
        # logger.debug(f"{pairs_to_elements(new_pair_counts)}")
        pair_counts = new_pair_counts.copy()

    # This accounts for the first and last element being counted once where everything else got double-counted.
    element_counts = Counter([polymer[0], polymer[-1]])
    for pair, count in pair_counts.items():
        element_counts[pair[0]] += count
        element_counts[pair[1]] += count
    frequencies = element_counts.most_common()
    return str(frequencies[0][1] // 2 - frequencies[-1][1] // 2)


tests = [
    (
        """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""",
        1588,
        part1,
    ),
    (
        """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""",
        2188189693529,
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
