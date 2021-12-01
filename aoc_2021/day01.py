from typing import List
import aocd
from . import aoc_year

aoc_day = 1


def preprocess():
    measurements = [
        int(item) for item in aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    ]
    return measurements


def count_increases(measurements: List[int], interval: int = 1):
    return sum(b > a for a, b in zip(measurements, measurements[interval:]))


def part1(measurements: List[int]):
    return count_increases(measurements)


def part2(measurements: List[int]):
    return count_increases(measurements, 3)
