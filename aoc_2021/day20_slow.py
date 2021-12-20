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

aoc_day = 20
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


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def neighbors(self):
        # order here is important, so we can't use:
        #  return [Point(x, y) for x, y in product(range(self.x - 1, self.x + 2), range(self.y - 1, self.y + 2))]
        for y in range(self.y - 1, self.y + 2):
            for x in range(self.x - 1, self.x + 2):
                yield Point(x, y)


class EnhancementAlgorithm:
    algorithm: str

    def __init__(self, algorithm: str):
        self.algorithm = algorithm

    def get_pixel_value(self, int):
        return 1 if self.algorithm[int] == "#" else 0


class TrenchImage:
    pixels: Dict[Point, str]
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    unknown_pixels: str

    def __init__(self, lines: str):
        lines = lines.split("\n")
        self.pixels = {}
        self.min_x = 0
        self.max_x = len(lines[0])
        self.min_y = 0
        self.max_y = len(lines)
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    self.pixels[Point(x, y)] = "1"
        self.unknown_pixels = "0"
        self.expand_bounds()

    def expand_bounds(self, expansion_size: int = 1):
        new_min_x = self.min_x - expansion_size
        new_max_x = self.max_x + expansion_size
        new_min_y = self.min_y - expansion_size
        new_max_y = self.max_y + expansion_size
        if self.unknown_pixels != "0":
            for p in [
                Point(x, y)
                for x, y in itertools.chain(
                    product(range(new_min_x, self.min_x), range(new_min_y, self.min_y)),
                    product(
                        range(self.max_x + 1, new_max_x + 1),
                        range(self.max_y + 1, new_max_y + 1),
                    ),
                )
            ]:
                self.pixels[p] = self.unknown_pixels
        self.min_x, self.max_x = new_min_x, new_max_x
        self.min_y, self.max_y = new_min_y, new_max_y

    def enhance(self, algorithm: EnhancementAlgorithm):
        result = {}

        def index(pixel: Point):
            index_string = ""
            in_window = (
                lambda p: self.min_x <= p.x <= self.max_x
                and self.min_y <= p.y <= self.max_y
            )
            for n in pixel.neighbors():
                if in_window(n):
                    index_string += self.pixels.get(n, "0")
                else:
                    index_string += self.unknown_pixels
            return int(index_string, 2)

        for p in [
            Point(x, y)
            for x, y in product(
                range(self.min_x - 1, self.max_x + 2),
                range(self.min_y - 1, self.max_y + 2),
            )
        ]:
            lit = algorithm.get_pixel_value(index(p))
            if lit:
                result[p] = "1"
        self.pixels = result
        self.unknown_pixels = (
            "1" if algorithm.get_pixel_value(int(self.unknown_pixels * 9, 2)) else "0"
        )
        self.expand_bounds()

    def get_image(self, dark: str = ".", light: str = "#"):
        lines = []
        for row in range(self.min_y - 5, self.max_y + 6):
            line = ""
            for col in range(self.min_x - 5, self.max_x + 6):
                line += light if self.pixels.get(Point(col, row)) else dark
            lines.append(line)
        return "\n".join(lines)


@dataclass
class AOCContext:
    alg: EnhancementAlgorithm
    image: TrenchImage


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year)
    algorithm, image = raw.split("\n\n")
    algorithm = EnhancementAlgorithm(algorithm)
    image = TrenchImage(image)

    context = AOCContext(algorithm, image)
    return context


def part1(context: AOCContext):
    enhancements = 2
    logger.debug(f"Before enhancements: {len(context.image.pixels)} pixels lit")
    logger.debug(f"\n{context.image.get_image()}")
    for i in range(enhancements):
        context.image.enhance(context.alg)
        logger.debug(f"After round {i + 1}: {len(context.image.pixels)} pixels lit")
        logger.debug(f"\n{context.image.get_image()}")
    return str(len(context.image.pixels))


def part2(context: AOCContext):
    enhancements = 50
    for i in range(enhancements):
        context.image.enhance(context.alg)
        logger.info(f"step {i} complete")
    return str(len(context.image.pixels))


tests = [
    (
        """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""",
        35,
        part1,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    for i, t in enumerate(tests[start:finish]):
        aocd.get_data = lambda *_, **__: t[0]
        result = t[2](preprocess())
        if f"{result}" != f"{t[1]}":
            logger.error(f"Test {start + i + 1} failed: got {result}, expected {t[1]}")
            break
        else:
            logger.success(f"Test {start + i + 1}: {t[1]}")


if __name__ == "__main__":
    test()
