import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple, deque, Counter
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 10
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
    scoring_table: Dict[str, int]


matching_characters = {
    "[": "]",
    "{": "}",
    "(": ")",
    "<": ">",
}


class SyntaxChecker:
    def __init__(self, context: AOCContext):
        self.context = context
        self.errors = []
        self.completions = []

    def add_error(self, line, col, got, expected):
        self.errors.append((line, col, got, expected))
        logger.debug(
            f"Found error: Line {line} col {col}: expected {expected} but got {got}"
        )

    def add_completion(self, line, expected):
        logger.debug(
            f"Found incomplete line: Line {line}: expected {''.join(expected)}"
        )
        self.completions.append((line, expected))

    def check_input(self):
        opening_chars = list(matching_characters.keys())
        closing_chars = list(matching_characters.values())
        for ll, line in enumerate(self.context.raw, start=1):
            closing_sequence = deque()
            for cc, c in enumerate(line, start=1):
                if c in opening_chars:
                    closing_sequence.insert(0, matching_characters[c])
                elif c in closing_chars:
                    expected = closing_sequence.popleft()
                    if expected != c:
                        self.add_error(ll, cc, c, expected)
                        break
            if not self.errors or (self.errors and self.errors[-1][0] != ll):
                self.add_completion(ll, closing_sequence)


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    scoring_table = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    context = AOCContext(raw, scoring_table)
    return context


def part1(context: AOCContext):
    checker = SyntaxChecker(context)
    checker.check_input()
    logger.info(f"Found {len(checker.errors)} errors")
    return str(sum(context.scoring_table[e[2]] for e in checker.errors))


def part2(context: AOCContext):
    checker = SyntaxChecker(context)
    checker.check_input()
    scores = []
    for c in checker.completions:
        score = 0
        characters = [None, ")", "]", "}", ">"]
        for suggestion in list(c[1]):
            score *= 5
            score += characters.index(suggestion)
        scores.append(score)
    scores.sort()
    return str(scores[len(scores) // 2])


tests = [
    (
        """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""",
        26397,
        part1,
    ),
    (
        """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""",
        288957,
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
