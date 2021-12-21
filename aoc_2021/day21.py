import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple, Counter
from dataclasses import dataclass
from functools import cache
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple, Iterable
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 21
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


class DiracDice:
    rolls: int
    positions: Dict[int, int]
    scores: Dict[int, int]
    die: Iterable

    def __init__(self, lines: List[str]):
        self.rolls = 0
        self.positions = {}
        self.scores = {}
        for line in lines:
            # logger.debug(f"Processing '{line}'")
            player, position = map(
                int,
                re.match(r"^Player (\d+?) starting position: (\d+?)$", line).groups(),
            )
            # using a zero-indexed board makes moving around a circle easier to track. but the positions in the input
            # are definitely one-indexed.
            self.positions[player] = position - 1
            self.scores[player] = 0
            # logger.debug(f"positions={self.positions}, scores={self.scores}")
        self.die = itertools.cycle(range(1, 101))

    # return True if game is over
    def play(self, player: int) -> bool:
        rolls = [next(self.die) for _ in range(3)]
        self.rolls += 3
        moves = sum(rolls)
        new_position = (self.positions[player] + moves) % 10
        self.positions[player] = new_position
        self.scores[player] += new_position + 1
        # logger.debug(f"player {player} rolls {rolls} and moves to space {new_position + 1} for a total score of {self.scores[player]}.")
        if self.scores[player] >= 1000:
            return True
        return False


# The mutable state above can't be cached effectively and there will be so much dict copying
# that I don't see a feasible way to use it for part 2. A named tuple is easy to cache during
# the search for winning states.
DiracState = namedtuple("DiracState", "pos1 pos2 score1 score2")


def play_roll(state: DiracState, total: int, player: int) -> DiracState:
    if player == 1:
        new_pos = (state.pos1 + total) % 10
        return DiracState(
            pos1=new_pos,
            pos2=state.pos2,
            score1=state.score1 + new_pos + 1,
            score2=state.score2,
        )
    elif player == 2:
        new_pos = (state.pos2 + total) % 10
        return DiracState(
            pos2=new_pos,
            pos1=state.pos1,
            score2=state.score2 + new_pos + 1,
            score1=state.score1,
        )


@dataclass
class AOCContext:
    raw: List[str]
    game: DiracDice
    initial: DiracState


def preprocess() -> AOCContext:
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    game = DiracDice(raw)
    context = AOCContext(
        raw, game, DiracState(game.positions[1], game.positions[2], 0, 0)
    )
    return context


# rewritten to use the tuple for state so that part2 can cache. the only reason for rewriting part1 was to make sure
# the new play function and state were working as expected.
def part1(context: AOCContext) -> str:
    state = context.initial
    rolls = 0
    practice_die = itertools.cycle(range(1, 101))
    for p in itertools.cycle(range(1, 3)):
        roll = [next(practice_die) for _ in range(3)]
        rolls += 3
        state = play_roll(state, sum(roll), p)
        # logger.debug(f"Player {p} rolls {roll} to advance to {state.pos1 + 1 if p == 1 else state.pos2 + 1} with a total score of {state.score1 if p == 1 else state.score2}")
        if state.score1 >= 1000 or state.score2 >= 1000:
            break
    losing_score = min(state.score1, state.score2)
    return str(losing_score * rolls)


# original part 1, using the game class
def part1_orig(context: AOCContext) -> str:
    losing_score = 0
    for p in itertools.cycle(context.game.positions):
        victory = context.game.play(p)
        if victory:
            break
    scores = {v: k for k, v in context.game.scores.items()}
    losing_score = min(scores.keys())
    losing_player = scores[losing_score]
    logger.info(
        f"part1: player {losing_player} lost with a score of {losing_score} after {context.game.rolls} rolls"
    )
    return str(losing_score * context.game.rolls)


d3_combinations = Counter(sum(p) for p in list(product(range(1, 4), repeat=3)))


# @cache is the difference between this not finishing in a reasonable amount of time and finishing in ~200ms.
@cache
def wins_for_state(state: DiracState, player_turn: int, max_score: int) -> (int, int):
    p1_wins = p2_wins = 0
    for roll_total, combos in d3_combinations.items():
        result = play_roll(state, roll_total, player_turn)
        if player_turn == 1 and result.score1 >= max_score:
            p1_wins += combos
        elif player_turn == 2 and result.score2 >= max_score:
            p2_wins += combos
        else:
            p1_raw, p2_raw = wins_for_state(
                result, 1 if player_turn != 1 else 2, max_score
            )
            p1_wins += p1_raw * combos
            p2_wins += p2_raw * combos
    return p1_wins, p2_wins


def part2(context: AOCContext):
    p1_wins, p2_wins = wins_for_state(context.initial, 1, 21)
    return str(max(p1_wins, p2_wins))


tests = [
    (
        """Player 1 starting position: 4
Player 2 starting position: 8
""",
        739785,
        part1_orig,
    ),
    (
        """Player 1 starting position: 4
Player 2 starting position: 8
""",
        739785,
        part1,
    ),
    (
        """Player 1 starting position: 4
Player 2 starting position: 8
""",
        444356092776315,
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
