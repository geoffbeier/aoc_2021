import itertools
import re
import string
from collections import defaultdict, namedtuple, Counter
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 11


@dataclass
class AOCContext:
    raw: List[str]
    current_password: str


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    current_password = raw[0].strip()
    context = AOCContext(raw, current_password)
    return context


def contains_straight(password):
    for i in range(len(password) - 2):
        if password[i : i + 3] in string.ascii_lowercase:
            return True
    return False


def legal_characters_only(password):
    illegal_characters = ["i", "o", "l"]
    return all(c not in password for c in illegal_characters)


def repeating_pairs(password):
    return len(Counter(a for a, b in zip(password, password[1:]) if a == b).keys()) >= 2


def is_valid(password: str):
    return (
        contains_straight(password)
        and legal_characters_only(password)
        and repeating_pairs(password)
    )


def skip_illegal_letters(password):
    r = list(reversed(password))
    illegal_letters = ["i", "o", "l"]
    found_illegals = []
    for c in illegal_letters:
        if c in r:
            found_illegals.append(r.index(c))
    if not found_illegals:
        return password
    first_illegal = min(found_illegals)
    r[first_illegal] = chr(ord(r[first_illegal]) + 1)
    for i in reversed(range(0, first_illegal)):
        r[i] = "a"
    return skip_illegal_letters("".join(reversed(r)))


def increment_password(password: str):
    codes = [ord(c) for c in password]
    codes.reverse()
    for i, c in enumerate(codes):
        if c < ord("z"):
            codes[i] += 1
            break
        else:
            codes[i] = ord("a")
    return skip_illegal_letters("".join([chr(i) for i in reversed(codes)]))


def part1(context: AOCContext):
    password = context.current_password
    while True:
        password = increment_password(password)
        logger.debug(f"trying {password}")
        if is_valid(password):
            context.current_password = password
            return password


def part2(context: AOCContext):
    part1(context)
    return part1(context)


tests = [
    (
        """abcdefgh
""",
        "abcdffaa",
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
