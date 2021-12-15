import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple, Set
import aocd

from advent_of_code_ocr import convert_6
from . import aoc_year
from loguru import logger

aoc_day = 8
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

Point = namedtuple("Point", "x y")


class Screen:
    w: int
    h: int
    # bitmap: List[List[str]]
    pixels_on: Set[Point]
    fg_char = "#"
    bg_char = "."

    def __init__(self, w: int = 50, h: int = 6):
        self.w = w
        self.h = h
        self.bitmap = []
        self.pixels_on = set()

    def cmd(self, command: str, *args):
        if command == "rect":
            w = args[0]
            h = args[1]
            self.rect(w, h)
        elif command == "rotate":
            axis = args[0]
            position = args[1]
            distance = args[2]
            self.rotate(axis, position, distance)

    def rect(self, w: int, h: int):
        for y, x in product(range(h), range(w)):
            # self.bitmap[y][x] = "#"
            self.pixels_on.add(Point(x, y))

    def rotate(self, axis: str, position: int, distance: int):
        rotated_line = set()
        for p in set(filter(lambda pp: getattr(pp, axis) == position, self.pixels_on)):
            self.pixels_on.remove(p)
            if axis == "x":
                rotated_line.add(Point(p.x, (p.y + distance) % self.h))
            elif axis == "y":
                rotated_line.add(Point((p.x + distance) % self.w, p.y))
        self.pixels_on |= rotated_line

    def __str__(self):
        bitmap = []
        for _ in range(self.h):
            bitmap.append(list(f"{self.bg_char}" * self.w))
        for p in self.pixels_on:
            bitmap[p.y][p.x] = self.fg_char
        return "\n".join(["".join(row) for row in bitmap])


@dataclass
class AOCContext:
    raw: List[str]
    commands: List[Tuple[str, List[Any]]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    commands = []
    for line in raw:
        command, remaining = line.split(maxsplit=1)
        if command == "rect":
            args = [int(x) for x in re.match(r"(\d+?)x(\d+?)$", remaining).groups()]
            commands.append((command, args))
            continue
        if command == "rotate":
            words = remaining.split()
            direction, position = words[1].split("=")
            args = [direction, int(position), int(words[-1])]
            commands.append((command, args))

    context = AOCContext(raw, commands)
    return context


def part1(context: AOCContext):
    screen = Screen()
    for command in context.commands:
        screen.cmd(command[0], *command[1])
    print(screen)
    return str(len(screen.pixels_on))


def get_letter_bitmap(points: Set[Point], index: int):
    min_x = index * 5
    max_x = index * 5 + 4
    max_y = max(p.y for p in points)
    lines = []
    for y in range(max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            if Point(x, y) in points:
                line.append("#")
            else:
                line.append(".")
        lines.append("".join(line))
    return "\n".join(lines)


def recognize_letters(screen):
    n_letters = screen.w // 5  # from the puzzle
    points = screen.pixels_on
    found_letters = []
    for i in range(n_letters):
        bitmap = get_letter_bitmap(points, i)
        found_letters.append(convert_6(bitmap))
    return "".join(found_letters)


def part2(context: AOCContext):
    screen = Screen()
    for command in context.commands:
        screen.cmd(command[0], *command[1])
    print(screen)
    letters = recognize_letters(screen)
    return letters


tests = [
    (
        """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
""",
        605,
        part1,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    test = tests[0]

    def gd(*args, **kwargs):
        return test[0]

    aocd.get_data = gd
    ctx = preprocess()
    screen = Screen(w=7, h=3)
    print(screen)
    for cmd in ctx.commands:
        screen.cmd(cmd[0], *cmd[1])
        print(f"After command {cmd[0]}")
        print(screen)
    return
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
