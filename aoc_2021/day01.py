from typing import List
import aocd
from . import aoc_year

aoc_day = 1


def preprocess():
    measurements = [
        int(item) for item in aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    ]
    return measurements


def part1(measurements: List[int]):
    return len(
        [
            measurement
            for n, measurement in enumerate(measurements[1:])
            if measurement > measurements[n]
        ]
    )


def part2(measurements: List[int]):
    return part1(
        [
            measurements[i] + measurements[i + 1] + measurements[i + 2]
            for i in range(0, len(measurements) - 2)
        ]
    )
