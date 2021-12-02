from dataclasses import dataclass
from math import prod
from typing import List, Dict
import aocd
from . import aoc_year
from loguru import logger

import _md5

aoc_day = 5


def preprocess():
    return aocd.get_data(day=aoc_day, year=aoc_year).splitlines()


def nice(word: str):
    n_vowels = sum(map(word.lower().count, "aeiou"))
    if n_vowels < 3:
        return False
    doubles = sum(a == b for a, b in zip(word, word[1:]))
    if doubles < 1:
        return False
    naughty_strings = ["ab", "cd", "pq", "xy"]
    naughty_count = sum(map(lambda s: s in word, naughty_strings))
    return naughty_count < 1


def nice2(word: str):
    non_overlapping_pairs = sum(
        map(lambda s: word.count(s) > 1, [f"{a}{b}" for a, b in zip(word, word[1:])])
    )
    if non_overlapping_pairs < 1:
        return False
    skip_one_repeats = sum(a == b for a, b in zip(word, word[2:]))
    return skip_one_repeats > 0


def part1(word_list: List[str]):
    return str(sum(map(nice, word_list)))


def part2(word_list: List[str]):
    return str(sum(map(nice2, word_list)))


tests = [
    (
        """abcdef
""",
        "609043",
        part1,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    for i, t in enumerate(tests[start:finish]):

        def gd(*args, **kwargs):
            return t[0]

        aocd.get_data = gd
        result = t[2](preprocess())
        if result != f"{t[1]}":
            logger.error(f"Test {start + i + 1} failed: got {result}, expected {t[1]}")
            break
        else:
            logger.success(f"Test {start + i + 1}: {t[1]}")


if __name__ == "__main__":
    test()
