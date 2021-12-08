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

aoc_day = 8


@dataclass
class AOCContext:
    raw: List[str]
    readings: List[Tuple[List[str], List[str]]]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    readings = []
    for line in raw:
        line = line.strip()
        i, o = line.split(" | ")
        input_segments = ["".join(sorted(list(w))) for w in i.split()]
        output_segments = ["".join(sorted(list(w))) for w in o.split()]
        readings.append((input_segments, output_segments))
    context = AOCContext(raw, readings)
    return context


def part1(context: AOCContext):
    known_numbers = sum(
        sum(len(w) in {2, 3, 4, 7} for w in reading[1]) for reading in context.readings
    )
    return str(known_numbers)


def build_mapping(input_reading: List[str], output_reading: List[str]):
    mapping = {}
    reverse_mapping = {}

    def add_mapping(wires: str, digit: str):
        mapping[wires] = digit
        reverse_mapping[digit] = set(wires)

    # first match the segments where the count is enough to know what digit is showing
    for word in itertools.chain(input_reading, output_reading):
        if len(word) == 2:
            add_mapping(word, "1")
        if len(word) == 3:
            add_mapping(word, "7")
        if len(word) == 4:
            add_mapping(word, "4")
        if len(word) == 7:
            add_mapping(word, "8")

    # then match the ones where 5 segments are lit
    for word in itertools.chain(input_reading, output_reading):
        if len(word) != 5:
            continue
        unlit = reverse_mapping["8"] - set(word)
        # if neither segment from a one is lit, this must be showing 3
        if len(unlit & reverse_mapping["1"]) == 0:
            add_mapping(word, "3")
        # if all of the unlit segments are lit in 4, this must be showing 2
        elif unlit.issubset(reverse_mapping["4"]):
            add_mapping(word, "2")
        # otherwise it's showing a 5
        else:
            add_mapping(word, "5")

    # with the 5-segment ones mapped, the 6-segment ones can be deduced
    for word in itertools.chain(input_reading, output_reading):
        if len(word) != 6:
            continue
        unlit = reverse_mapping["8"] - set(word)
        unlit_segment = unlit.pop()
        # if the lone unlit segment is lit in 4 and not in 5, we have a 6.
        # if it's lit in 2 and not 5, we have a 9
        # if it's lit in 5, we have a 0
        if unlit_segment not in reverse_mapping["5"]:
            if unlit_segment in reverse_mapping["4"]:
                add_mapping(word, "6")
            elif unlit_segment in reverse_mapping["2"]:
                add_mapping(word, "9")
        else:
            add_mapping(word, "0")
    return mapping


def part2(context: AOCContext):
    total = 0
    for reading in context.readings:
        translation = build_mapping(reading[0], reading[1])
        digits = "".join(translation[word] for word in reading[1])
        total += int(digits)

    return str(total)


tests = [
    (
        """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""",
        26,
        part1,
    ),
    (
        """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""",
        61229,
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
