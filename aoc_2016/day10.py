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


class Bin:
    id: int
    chips: List[int]

    def __init__(self, id):
        self.id = id
        self.chips = []

    def add(self, chip: int):
        self.chips.append(chip)

    def __str__(self):
        return f"Bin {self.id}"


class Bot:
    id: int
    chips: List[int]
    high: Any
    low: Any
    log: Dict[Tuple[int, int], int]

    def __init__(
        self,
        id,
        high_destination: Any,
        low_destination: Any,
        log: Dict[Tuple[int, int], int],
    ):
        self.id = id
        self.high = high_destination
        self.low = low_destination
        self.log = log
        self.chips = []

    def add(self, chip: int):
        self.chips.append(chip)
        if len(self.chips) == 2:
            hc = max(self.chips)
            lc = min(self.chips)
            logger.debug(f"bot {self.id} gives chip {hc} to {self.high}")
            self.high.add(hc)
            logger.debug(f"bot {self.id} gives chip {lc} to {self.low}")
            self.low.add(lc)
            self.log[(hc, lc)] = self.id

    def __str__(self):
        return f"Bot {self.id}"


@dataclass
class AOCContext:
    raw: List[str]
    inputs: List[Tuple[int, ...]] = None
    bots: Dict[int, Bot] = None
    outputs: Dict[int, Bin] = None
    bot_log: Dict[Tuple[int, int], int] = None

    def __post_init__(self):
        self.reset()

    def reset(self):
        inputs = []
        bots = {}
        outputs = {}
        bot_log = {}
        for line in self.raw:
            if line.startswith("value"):
                inputs.append(
                    tuple(
                        int(x)
                        for x in re.match(
                            r"value (\d+?) goes to bot (\d+?)$", line
                        ).groups()
                    )
                )
                continue
            if line.startswith("bot"):
                matchexp = r"bot (\d+?) gives low to (bot|output) (\d+?) and high to (bot|output) (\d+?)$"
                bot_id, low_type, low_id, high_type, high_id = re.match(
                    matchexp, line
                ).groups()
                low_dest = None
                high_dest = None
                bot_id = int(bot_id)
                low_id = int(low_id)
                high_id = int(high_id)
                if low_type == "output":
                    ob = outputs.get(low_id, Bin(low_id))
                    outputs[ob.id] = ob
                    low_dest = ob
                elif low_type == "bot":
                    b = bots.get(low_id, Bot(low_id, None, None, bot_log))
                    bots[b.id] = b
                    low_dest = b
                if high_type == "output":
                    ob = outputs.get(high_id, Bin(high_id))
                    outputs[ob.id] = ob
                    high_dest = ob
                elif high_type == "bot":
                    b = bots.get(high_id, Bot(high_id, None, None, bot_log))
                    bots[b.id] = b
                    high_dest = b
                b = bots.get(bot_id, Bot(bot_id, None, None, bot_log))
                b.high = high_dest
                b.low = low_dest
                bots[bot_id] = b
            self.inputs = inputs
            self.bots = bots
            self.outputs = outputs
            self.bot_log = bot_log


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    context = AOCContext(raw)
    return context


def part1(context: AOCContext):
    for (value, bot) in context.inputs:
        logger.debug(f"bot {bot} takes chip {value} from input")
        context.bots[bot].add(value)
    return str(context.bot_log[(61, 17)])


def part2(context: AOCContext):
    chips_out = sum(len(o.chips) for o in context.outputs.values())
    if not chips_out:
        part1(context)
    return str(
        context.outputs[0].chips[0]
        * context.outputs[1].chips[0]
        * context.outputs[2].chips[0]
    )


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
