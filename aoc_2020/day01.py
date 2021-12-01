import functools
import itertools
import operator
from typing import List

import aocd

from . import aoc_year

aoc_day = 1


def find_n(numbers: List[int], count: int, total: int):
    for s in itertools.combinations(numbers, count):
        if sum(s) == total:
            return s


def preprocess(data: List[str] = None):
    if data:
        expenses = [int(item) for item in data]
    else:
        expenses = [
            int(item) for item in aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
        ]
    expenses.sort()
    return expenses


def part1(expenses: List[int]):
    return functools.reduce(operator.mul, find_n(expenses, 2, 2020))


def part2(expenses: List[int]):
    return functools.reduce(operator.mul, find_n(expenses, 3, 2020))
