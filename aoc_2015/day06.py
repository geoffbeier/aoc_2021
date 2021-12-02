import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

import _md5

aoc_day = 6


def preprocess():
    instructions = []
    instruction_re = r"(turn on|turn off|toggle) (\d+?),(\d+?) through (\d+?),(\d+?)$"
    for line in aocd.get_data(day=aoc_day, year=aoc_year).splitlines():
        command, start_x, start_y, end_x, end_y = re.match(
            instruction_re, line
        ).groups()
        instructions.append(
            {
                "command": command,
                "start": (int(start_x), int(start_y)),
                "end": (int(end_x), int(end_y)),
            }
        )
    return instructions


def get_range(start: Tuple[int, int], end: Tuple[int, int]):
    return product(
        [x for x in range(start[0], end[0] + 1)],
        [y for y in range(start[1], end[1] + 1)],
    )


def part1(instructions: List[Dict[str, Any]]):
    lights = defaultdict(int)
    for i in instructions:
        changed_lights = get_range(i["start"], i["end"])
        for l in changed_lights:
            if i["command"] == "turn on":
                lights[l] = 1
            elif i["command"] == "turn off":
                lights[l] = 0
            elif i["command"] == "toggle":
                lights[l] = 0 if lights[l] else 1
    return str(sum(lights.values()))


def part2(instructions: List[Dict[str, Any]]):
    lights = defaultdict(int)
    for i in instructions:
        changed_lights = get_range(i["start"], i["end"])
        for l in changed_lights:
            if i["command"] == "turn on":
                lights[l] += 1
            elif i["command"] == "turn off":
                if lights[l] > 0:
                    lights[l] -= 1
            elif i["command"] == "toggle":
                lights[l] += 2
    return str(sum(lights.values()))


tests = [
    (
        """turn on 0,0 through 999,999
""",
        "1000000",
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
