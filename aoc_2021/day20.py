import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple, deque
from dataclasses import dataclass
from itertools import product
from math import prod
import numpy
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger
from .bitarray import BitArray

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

DEBUG = False

# My first attempt was to use a set of points that were "on". This worked fine for the demo data, but fell down with the
# real dataset. I suspect this is because the enhancer in the real input had 000000000 set to '#' instead of '.' and that
# made the bookkeeping for the infinite grid trickier. Before I try to fix that, which is fiddly and hard to debug
# with the real dataset, I'm going to try just tracking enough of a grid to look everything up and see if that ages well.
#
# from future me: just tracking the grid was easier and turned out faster on part 2. original approach is debugged
# and checked in as `day20_slow.py`

char_map = {
    "#": 1,
    ".": 0,
}

pixel_region = [(x, y) for y, x in product([-1, 0, 1], [-1, 0, 1])]


class TrenchImage:
    grid: List[BitArray]
    enhancement_algorithm: List[str]
    w: int
    h: int
    filler: int

    def __init__(self, image_lines: str, enhancment_algorithm: str):
        image_lines = image_lines.split()
        self.w = len(image_lines[0])
        self.h = len(image_lines)
        self.grid = deque([BitArray(line, one="#", zero=".") for line in image_lines])
        self.enhancement_algorithm = [char_map[c] for c in enhancment_algorithm]
        self.filler = 0
        self.expand_border()

    def expand_border(self, increment: int = 1):
        new_h = self.h + 2 * increment
        new_w = self.w + 2 * increment
        for row in self.grid:
            row.expand_left(increment, self.filler)
            row.expand_right(increment, self.filler)
        self.grid.insert(0, BitArray(f"{self.filler}" * new_w))
        self.grid.append(BitArray(f"{self.filler}" * new_w))
        self.w = new_w
        self.h = new_h

    def enhance(self):
        def index(xx, yy):
            bits = 0
            for bit, (dx, dy) in enumerate(pixel_region):
                if 0 <= xx + dx < self.w and 0 <= yy + dy < self.h:
                    bits |= self.grid[yy + dy][xx + dx] << (8 - bit)
                else:
                    bits |= self.filler << (8 - bit)
            return bits

        new_grid = deque()
        for y in range(self.h):
            line = self.grid[y].copy()
            for x in range(self.w):
                line[x] = self.enhancement_algorithm[index(x, y)]
            new_grid.append(line)
        self.grid = new_grid
        self.filler = self.enhancement_algorithm[int(f"{self.filler}" * 9, 2)]
        self.expand_border()

    def to_bitmap(self, dark: str = ".", light: str = "#"):
        bitmap = "\n".join(str(row) for row in self.grid)
        bitmap = bitmap.replace("1", light)
        bitmap = bitmap.replace("0", dark)
        return bitmap


@dataclass
class AOCContext:
    image: TrenchImage


def preprocess():
    enh, img = aocd.get_data(day=aoc_day, year=aoc_year).split("\n\n")
    image = TrenchImage(img, enh)
    context = AOCContext(image)
    return context


def part1(context: AOCContext):
    steps = 2
    if DEBUG:
        logger.debug(
            f"before\n{context.image.to_bitmap()} {sum(b.count() for b in context.image.grid)}"
        )
    for _ in range(steps):
        context.image.enhance()
        if DEBUG:
            logger.debug(
                f"after\n{context.image.to_bitmap()} {sum(b.count() for b in context.image.grid)}"
            )
    return str(sum(b.count() for b in context.image.grid))


def part2(context: AOCContext):
    steps = 50
    for i in range(steps):
        context.image.enhance()
    logger.info(f"{context.image.grid[0].w} bits per line")
    return str(sum(b.count() for b in context.image.grid))


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
    global DEBUG
    DEBUG = True
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
