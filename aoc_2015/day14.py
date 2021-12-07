import itertools
import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 14


class Reindeer:
    def __init__(self, name: str, rate: int, duration: int, rest_time: int):
        self.name = name
        self.rate = rate
        self.duration = duration
        self.rest_time = rest_time
        self.current_race_time = 0

    def distance_after(self, seconds: int):
        distance = 0
        remaining_seconds = seconds
        while remaining_seconds > 0:
            if remaining_seconds < self.duration:
                distance += self.rate * remaining_seconds
                remaining_seconds = 0
            else:
                distance += self.rate * self.duration
                remaining_seconds -= self.duration
                remaining_seconds -= self.rest_time
        return distance

    def tick(self):
        self.current_race_time += 1
        return self.distance_after(self.current_race_time)


@dataclass
class AOCContext:
    raw: List[str]
    reindeer: List[Reindeer]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    reindeer = []
    reindeer_match = (
        r"(.*) can fly (\d+?) km\/s for (\d+?) second.*.rest for (\d+?) seconds.$"
    )
    for line in raw:
        line.strip()
        name, rate, duration, rest_time = re.match(reindeer_match, line).groups()
        reindeer.append(Reindeer(name, int(rate), int(duration), int(rest_time)))
    context = AOCContext(raw, reindeer)
    return context


def part1(context: AOCContext):
    logger.info(
        f"{len(context.reindeer)} reindeer are competing ({', '.join([r.name for r in context.reindeer])})."
    )
    distances = {r.distance_after(2503): r.name for r in context.reindeer}
    winning_distance = max(distances.keys())
    logger.info(f"{distances[winning_distance]} went {winning_distance}km")
    return str(winning_distance)


def part2(context: AOCContext):
    scores = defaultdict(int)
    distances = defaultdict(int)
    for t in range(2504):
        positions = defaultdict(list)
        for r in context.reindeer:
            positions[r.tick()].append(r.name)
        for r in positions[max(positions.keys())]:
            scores[r] += 1
        for d in positions.keys():
            for rname in positions[d]:
                distances[rname] = d
    winner_name = max(scores, key=scores.get)
    winner_score = scores[winner_name]
    leader_board = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    for rn in leader_board.keys():
        logger.info(f"{rn}: {scores[rn]} points, {distances[rn]}km")
    return str(winner_score)


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
