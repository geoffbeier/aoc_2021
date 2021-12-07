import itertools
import json
import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 12


@dataclass
class AOCContext:
    raw: List[str]
    decoded: Any


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    pyobj = json.loads("\n".join(raw))
    context = AOCContext(raw, pyobj)
    return context


def tally_dict(items: Dict[Any, Any], ignored_values: List[str] = None):
    tally = 0
    if ignored_values:
        for v in ignored_values:
            if v in items.values():
                return tally
    for k, v in items.items():
        if isinstance(k, int):
            tally += k
        if isinstance(v, int):
            tally += v
        elif isinstance(v, list):
            tally += tally_list(v, ignored_values)
        elif isinstance(v, dict):
            tally += tally_dict(v, ignored_values)
        else:
            logger.debug(f"Unable to tally {type(v)}")
    return tally


def tally_list(items: List[Any], ignored_values: List[str] = None):
    tally = 0
    for i in items:
        if isinstance(i, int):
            tally += i
        elif isinstance(i, list):
            tally += tally_list(i, ignored_values)
        elif isinstance(i, dict):
            tally += tally_dict(i, ignored_values)
        else:
            logger.debug(f"Unable to tally {type(i)}")
    return tally


def part1(context: AOCContext):
    tally = 0
    pyobj = context.decoded
    if isinstance(pyobj, dict):
        tally = tally_dict(pyobj)
    elif isinstance(pyobj, list):
        tally = tally_list(pyobj)
    else:
        logger.error(f"Unexpected type: {type(pyobj)}")
    return str(tally)


def part2(context: AOCContext):
    tally = 0
    pyobj = context.decoded
    ignored_values = ["red"]
    if isinstance(pyobj, dict):
        tally = tally_dict(pyobj, ignored_values)
    elif isinstance(pyobj, list):
        tally = tally_list(pyobj, ignored_values)
    else:
        logger.error(f"Unexpected type: {type(pyobj)}")
    return str(tally)


tests = [
    (
        """[1,2,3]
""",
        6,
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
