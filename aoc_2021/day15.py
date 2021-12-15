import heapq
import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple, deque
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple, Iterable
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 15
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
    map: List[List[int]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    area_map = []
    for line in raw:
        area_map.append([int(x) for x in line])
    context = AOCContext(raw, area_map)
    return context


Point = namedtuple("Point", "x y")


def neighbors(point: Point, w: int, h: int):
    if point.y > 0:
        yield Point(point.x, point.y - 1)
    if point.y < h - 1:
        yield Point(point.x, point.y + 1)
    if point.x > 0:
        yield Point(point.x - 1, point.y)
    if point.x < w - 1:
        yield Point(point.x + 1, point.y)


def min_risk_path(graph, start, end):
    visited = set()
    q = [(0, start)]
    while len(q):
        risk, node = heapq.heappop(q)
        if node == end:
            return risk
        if node in visited:
            continue
        visited.add(node)
        for neighbor, neighbor_risk in graph[node].items():
            heapq.heappush(q, ((risk + neighbor_risk), neighbor))
    return -1


def part1(context: AOCContext):
    graph = {}
    map_w = len(context.map[0])
    map_h = len(context.map)
    for x, y in product(range(map_w), range(map_h)):
        graph[Point(x, y)] = {
            n: context.map[n.y][n.x] for n in neighbors(Point(x, y), map_w, map_h)
        }
    return str(min_risk_path(graph, Point(0, 0), Point(map_w - 1, map_h - 1)))


def part2(context: AOCContext):
    map_w = len(context.map[0])
    map_h = len(context.map)
    full_map_w = 5 * map_w
    full_map_h = 5 * map_h
    graph = {}
    logger.debug(f"Building graph for expanded map")
    for x, y in product(range(full_map_w), range(full_map_h)):

        def adjust(xx, yy, v):
            if xx < map_w and yy < map_h:
                return v
            return (v + xx // map_w + yy // map_h - 1) % 9 + 1

        graph[Point(x, y)] = {
            n: adjust(n.x, n.y, context.map[n.y % map_h][n.x % map_w])
            for n in neighbors(Point(x, y), full_map_w, full_map_h)
        }
    logger.debug(f"Done building graph for expanded map")
    return str(min_risk_path(graph, Point(0, 0), Point(full_map_w - 1, full_map_h - 1)))


tests = [
    (
        """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""",
        40,
        part1,
    ),
    (
        """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""",
        315,
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
