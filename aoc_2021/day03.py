from dataclasses import dataclass
from math import prod
from typing import List, Dict
import aocd
from . import aoc_year
from loguru import logger

from collections import defaultdict

aoc_day = 3


def preprocess():
    return aocd.get_data(day=aoc_day, year=aoc_year).splitlines()


def min_key(frequency_dict: dict):
    keys = list(frequency_dict.keys())
    min_k = keys[0]
    for k in keys:
        if frequency_dict[k] < frequency_dict[min_k]:
            min_k = k
    return min_k


def max_key(frequency_dict: dict):
    keys = list(frequency_dict.keys())
    max_k = keys[0]
    for k in keys:
        if frequency_dict[k] > frequency_dict[max_k]:
            max_k = k
    return max_k


def bit_frequencies(report: List[str]):
    frequency_table = []
    for i in range(len(report[0])):
        frequency_table.append(defaultdict(int))
    for row in report:
        for i, col in enumerate(row):
            frequency_table[i][col] += 1
    return frequency_table


def part1(report: List[str]):
    frequency_table = bit_frequencies(report)
    gamma = int("".join(max_key(d) for d in frequency_table), 2)
    epsilon = int("".join(min_key(d) for d in frequency_table), 2)
    return str(gamma * epsilon)


def part2(report: List[str]):
    remaining = report.copy()
    for col in range(len(report[0])):
        frequency_table = bit_frequencies(remaining)
        most_common = (
            "1" if frequency_table[col]["1"] >= frequency_table[col]["0"] else "0"
        )
        remaining = [r for r in remaining if r[col] == most_common]
        if len(remaining) == 1:
            break
    o2 = int(remaining[0], 2)
    remaining = report.copy()
    for col in range(len(report[0])):
        frequency_table = bit_frequencies(remaining)
        least_common = (
            "0" if frequency_table[col]["0"] <= frequency_table[col]["1"] else "1"
        )
        remaining = [r for r in remaining if r[col] == least_common]
        if len(remaining) == 1:
            break
    co2 = int(remaining[0], 2)
    return str(o2 * co2)


tests = [
    (
        """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""",
        198,
        part1,
    ),
    (
        """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""",
        230,
        part2,
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
