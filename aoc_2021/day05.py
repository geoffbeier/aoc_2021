import sys
from dataclasses import dataclass
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

from collections import defaultdict, OrderedDict

aoc_day = 5


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x},{self.y})"


def points(start: Point, end: Point, include_diagonal: bool = False):
    hits = set()
    if start.x != end.x and start.y != end.y:
        if not include_diagonal:
            return hits
    hits.add(str(start))
    hits.add(str(end))
    dx = 0
    dy = 0
    if start.x < end.x:
        dx = 1
    elif start.x > end.x:
        dx = -1
    if start.y < end.y:
        dy = 1
    elif start.y > end.y:
        dy = -1
    curr = start
    while curr != end:
        curr = Point(curr.x + dx, curr.y + dy)
        hits.add(str(curr))
    return hits


def preprocess():
    context = {"raw": aocd.get_data(day=aoc_day, year=aoc_year).splitlines()}
    segments: List[Tuple[Point, Point]] = []
    for line in context["raw"]:
        ss, es = line.strip().split(" -> ")
        x1, y1 = ss.split(",")
        start = Point(int(x1), int(y1))
        x2, y2 = es.split(",")
        end = Point(int(x2), int(y2))
        segments.append((start, end))

    context["segments"] = segments
    return context


def print_board(hits):
    for y in range(10):
        line = ""
        for x in range(10):
            line += "." if hits[Point(x, y)] == 0 else str(hits[Point(x, y)])
        print(line)


def part1(context: Dict[str, Any]):
    hits: Dict[str, int] = defaultdict(int)
    for s in context["segments"]:
        for p in points(s[0], s[1]):
            hits[p] += 1
    danger = sum(hits[h] >= 2 for h in hits.keys())
    return str(danger)


def part2(context: Dict[str, Any]):
    hits: Dict[str, int] = defaultdict(int)
    for s in context["segments"]:
        for p in points(s[0], s[1], include_diagonal=True):
            hits[p] += 1
    danger = sum(hits[h] >= 2 for h in hits.keys())
    return str(danger)


tests = [
    (
        """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""",
        5,
        part1,
    ),
    (
        """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""",
        12,
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
    logger.debug(f"Starting tests.")
    test()
