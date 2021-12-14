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

aoc_day = 2
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


Position = namedtuple("Position", "col row")


class KeypadNavigator:
    def __init__(self, keys=None):
        self.keys = keys or [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
        ]
        self.current = Position(1, 1)

    def up(self):
        new_pos = Position(col=max(self.current.col - 1, 0), row=self.current.row)
        if self.keys[new_pos.row][new_pos.col]:
            self.current = new_pos

    def down(self):
        new_pos = Position(
            col=min(self.current.col + 1, len(self.keys) - 1), row=self.current.row
        )
        if self.keys[new_pos.row][new_pos.col]:
            self.current = new_pos

    def left(self):
        new_pos = Position(col=self.current.col, row=max(self.current.row - 1, 0))
        if self.keys[new_pos.row][new_pos.col]:
            self.current = new_pos

    def right(self):
        new_pos = Position(
            col=self.current.col, row=min(self.current.row + 1, len(self.keys[0]) - 1)
        )
        if self.keys[new_pos.row][new_pos.col]:
            self.current = new_pos

    def current_key(self):
        return self.keys[self.current.col][self.current.row]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    context = AOCContext(raw)
    return context


def part1(context: AOCContext):
    combination = ""
    keys = KeypadNavigator()
    for line in context.raw:
        for c in line:
            if c == "R":
                keys.right()
            elif c == "L":
                keys.left()
            elif c == "D":
                keys.down()
            elif c == "U":
                keys.up()
        combination += str(keys.current_key())
    return combination


def part2(context: AOCContext):
    combination = ""
    layout = [
        [None, None, "1", None, None],
        [None, "2", "3", "4", None],
        ["5", "6", "7", "8", "9"],
        [None, "A", "B", "C", None],
        [None, None, "D", None, None],
    ]
    keys = KeypadNavigator(keys=layout)
    for line in context.raw:
        for c in line:
            if c == "R":
                keys.right()
            elif c == "L":
                keys.left()
            elif c == "D":
                keys.down()
            elif c == "U":
                keys.up()
        combination += str(keys.current_key())
    return combination


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
    logger.debug(f"Testing keypad navigator")
    nav = KeypadNavigator()
    nav.up()
    nav.left()
    nav.left()
    assert nav.current_key() == 1
    nav.right()
    nav.right()
    nav.down()
    nav.down()
    nav.down()
    assert nav.current_key() == 9
    nav.left()
    nav.up()
    nav.right()
    nav.down()
    nav.left()
    assert nav.current_key() == 8
    nav.up()
    nav.up()
    nav.up()
    nav.up()
    nav.down()
    assert nav.current_key() == 5
    nav.up()
    assert nav.current_key() == 2
    nav.down()
    assert nav.current_key() == 5
    nav.down()
    assert nav.current_key() == 8
    nav.up()
    assert nav.current_key() == 5
    nav.left()
    assert nav.current_key() == 4
    nav.right()
    assert nav.current_key() == 5
    logger.debug(f"Pass")
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
