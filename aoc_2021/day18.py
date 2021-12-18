import ast
import itertools
import math
import operator
import re
import sys
from dataclasses import dataclass
from functools import reduce
from typing import List, Union, Optional

import aocd
from loguru import logger

from . import aoc_year

aoc_day = 18
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

SnailfishNumberType = Union[List["SnailfishNumber"], int]


# There is probably a nicer way to express "direction" here... I originally set out to store
# snailfish numbers as tuples of pair, depth. So going left meant indexing backwards into the list
# and going right meant indexing forwards. I kept the -1 and 1 from that even after I dropped
# that idea.
def exp_add(sn: SnailfishNumberType, b: Optional[int], direction: int):
    if not b:
        return sn
    if isinstance(sn, int):
        return sn + b
    if direction == -1:
        return [exp_add(sn[0], b, direction), sn[1]]
    else:
        return [sn[0], exp_add(sn[1], b, direction)]


def explode(sn: SnailfishNumberType, depth: int = 4):
    did_explode = False
    if isinstance(sn, list):
        if depth == 0:
            did_explode = True
            return did_explode, 0, (sn[0], sn[1])
        did_explode, result, (left, right) = explode(sn[0], depth - 1)
        if did_explode:
            return did_explode, [result, exp_add(sn[1], right, -1)], (left, None)
        did_explode, result, (left, right) = explode(sn[1], depth - 1)
        if did_explode:
            return did_explode, [exp_add(sn[0], left, 1), result], (None, right)
    return did_explode, sn, (None, None)


def split(sn: SnailfishNumberType):
    did_split = False
    if isinstance(sn, list):
        did_split, result = split(sn[0])
        if did_split:
            return did_split, [result, sn[1]]
        did_split, result = split(sn[1])
        return did_split, [sn[0], result]
    if sn >= 10:
        did_split = True
        return did_split, [math.floor(sn / 2), math.ceil(sn / 2)]
    return did_split, sn


class SnailfishNumber:
    n: SnailfishNumberType

    def __init__(self, n: Union[List["SnailfishNumber"], int] = None):
        self.n = n

    def __add__(self, rhs: "SnailfishNumber"):
        result = [self.n, rhs.n]
        complete = False
        while not complete:
            did_explode, result, _ = explode(result)
            if did_explode:
                continue
            did_split, result = split(result)
            if not did_split:
                complete = True
        return SnailfishNumber(result)

    def __str__(self):
        return f"{self.n}"

    def magnitude(self):
        if isinstance(self.n, list):
            return (3 * SnailfishNumber(self.n[0]).magnitude()) + (
                2 * SnailfishNumber(self.n[1]).magnitude()
            )
        return self.n


def make_snailfish_number(representation: str):
    return SnailfishNumber(ast.literal_eval(representation))


@dataclass
class AOCContext:
    raw: List[str]
    snailfish_numbers: List[SnailfishNumber]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    snailfish_numbers = []
    for line in raw:
        snailfish_numbers.append(make_snailfish_number(line))
    context = AOCContext(raw, snailfish_numbers)
    return context


def part1(context: AOCContext):
    snailfish_sum = reduce(operator.add, context.snailfish_numbers)
    return str(snailfish_sum.magnitude())


def part2(context: AOCContext):
    largest_magnitude = max(
        map(
            SnailfishNumber.magnitude,
            [
                operator.add(p[0], p[1])
                for p in itertools.permutations(context.snailfish_numbers, 2)
            ],
        )
    )
    return str(largest_magnitude)


def test_add(context: AOCContext):
    snailfish_sum = reduce(operator.add, context.snailfish_numbers)
    return str(snailfish_sum)


tests = [
    (
        """[1,1]
[2,2]
[3,3]
[4,4]
""",
        [[[[1, 1], [2, 2]], [3, 3]], [4, 4]],
        test_add,
    ),
    (
        """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
""",
        [[[[3, 0], [5, 3]], [4, 4]], [5, 5]],
        test_add,
    ),
    (
        """[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]
""",
        [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]],
        test_add,
    ),
    (
        """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""",
        [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]],
        test_add,
    ),
    (
        """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""",
        [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]],
        test_add,
    ),
    (
        """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""",
        4140,
        part1,
    ),
    (
        """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""",
        3993,
        part2,
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
