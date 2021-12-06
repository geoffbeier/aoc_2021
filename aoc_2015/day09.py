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

aoc_day = 9


def preprocess():
    context = {
        "raw": aocd.get_data(day=aoc_day, year=aoc_year).splitlines(),
        "routes": {},
        "cities": set(),
    }
    for s in context["raw"]:
        route, distance = s.split(" = ")
        distance = int(distance)
        origin, destination = route.split(" to ")
        context["cities"].add(origin)
        context["cities"].add(destination)
        context["routes"][(origin, destination)] = distance
        context["routes"][(destination, origin)] = distance
    logger.info(f"Cities to visit: {context['cities']}")
    return context


def get_routes(stops, legs):
    routes = defaultdict(list)
    for route in itertools.permutations(stops):
        length = 0
        route_origin = None
        route_stops = []
        for origin, destination in zip(route[:-1], route[1:]):
            if not route_origin:
                route_origin = origin
            route_stops.append(destination)
            length += legs[(origin, destination)]
        route_cities = [route_origin]
        for s in route_stops:
            route_cities.append(s)
        routes[length].append(route_cities)
    return routes


def part1(context: Dict[str, Any]):
    possible_routes = get_routes(context["cities"], context["routes"])
    shortest = min(possible_routes.keys())
    shortest_details = possible_routes[shortest]
    if len(shortest_details) > 2:
        logger.info(f"Multiple routes found with distance {shortest}:")
        for d in shortest_details:
            logger.info(f"{' -> '.join(d)}: {shortest}")
    else:
        logger.info(f"{' -> '.join(shortest_details[0])}: {shortest}")
    return str(shortest)


def part2(context: Dict[str, Any]):
    possible_routes = get_routes(context["cities"], context["routes"])
    longest = max(possible_routes.keys())
    longest_details = possible_routes[longest]
    if len(longest_details) > 2:
        logger.info(f"Multiple routes found with distance {longest}:")
        for d in longest_details:
            logger.info(f"{' -> '.join(d)}: {longest}")
    else:
        logger.info(f"{' -> '.join(longest_details[0])}: {longest}")
    return str(longest)


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
