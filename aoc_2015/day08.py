import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 8


def unescape(raw: str):
    parsed = []
    i = 0
    while i < len(raw):
        if raw[i] != "\\":
            parsed.append(raw[i])
        else:
            if raw[i + 1] == "\\" or raw[i + 1] == '"':
                parsed.append(raw[i + 1])
                i += 1
            elif raw[i + 1] == "x":
                code = raw[i + 2 : i + 4]
                parsed.append(chr(int(code, 16)))
                i += 3
        i += 1
    return "".join(parsed)


def escape(raw: str):
    escaped = ['"']
    for c in raw:
        if c == '"':
            escaped.append("\\")
        elif c == "\\":
            escaped.append("\\")
        escaped.append(c)
    escaped.append('"')
    # logger.debug(f"{raw}({len(raw)}) => {''.join(escaped)}({len(e)})")
    return "".join(escaped)


def preprocess():
    context = {
        "raw": aocd.get_data(day=aoc_day, year=aoc_year).splitlines(),
        "parsed": [],
    }
    for s in context["raw"]:
        context["parsed"].append(unescape(s.strip()[1:-1]))
    return context


def part1(context: Dict[str, Any]):
    code_len = sum(len(s.strip()) for s in context["raw"])
    repr_len = sum(len(s) for s in context["parsed"])
    return str(code_len - repr_len)


def part2(context: Dict[str, Any]):
    escaped = []
    for s in context["raw"]:
        escaped.append(escape(s.strip()))
    code_len = sum(len(s.strip()) for s in context["raw"])
    escaped_len = sum(len(s) for s in escaped)
    return str(escaped_len - code_len)


tests = [
    (
        """""
"abc"
"aaa\\"aaa"
"\\x27"
""",
        12,
        part1,
    ),
    (
        """""
"abc"
"aaa\\"aaa"
"\\x27"
""",
        19,
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
