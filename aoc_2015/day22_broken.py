import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from enum import Enum
from itertools import product
from math import prod
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger
import copy

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


@dataclass
class Entity:
    hit_points: int = 0
    damage: int = 0
    armor: int = 0
    mana: int = 0


@dataclass
class Spell:
    name: str
    cost: int
    damage: int
    heals: int
    armor: int
    timer: int
    mana: int


@dataclass
class AOCContext:
    raw: List[str]
    boss: Entity
    available_spells: List[Any]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    boss = Entity()
    for line in raw:
        stat, value = line.split(": ")
        if stat == "Hit Points":
            boss.hit_points = int(value)
        elif stat == "Damage":
            boss.damage = int(value)
        elif stat == "Armor":
            boss.armor = int(value)

    available_spells = [
        Spell("Magic Missile", cost=53, damage=4, heals=0, armor=0, timer=0, mana=0),
        Spell("Drain", cost=73, damage=2, heals=2, armor=0, timer=0, mana=0),
        Spell("Shield", cost=113, damage=0, heals=0, armor=7, timer=6, mana=0),
        Spell("Poison", cost=173, damage=3, heals=0, armor=0, timer=6, mana=0),
        Spell("Recharge", cost=229, damage=0, heals=0, armor=0, timer=5, mana=101),
    ]
    context = AOCContext(raw, boss, available_spells)
    return context


class GameState(Enum):
    PLAYER_WINS = 0
    BOSS_WINS = 1
    ILLEGAL = 3
    INCOMPLETE = 4


@dataclass
class Effect:
    spell: Spell
    time: int


class Game:
    context: AOCContext
    player: Entity
    boss: Entity
    effects: List[Effect]
    mana_spent: int

    def __init__(self, context: AOCContext, player: Entity):
        self.context = context
        self.boss = copy.deepcopy(context.boss)
        self.player = copy.deepcopy(player)
        self.effects = []
        self.mana_spent = 0

    def __lt__(self, other):
        return self.mana_spent < other.mana_spent

    def apply_effects(self):
        expiring_effects = []
        for i, e in enumerate(self.effects):
            s = e.spell
            if s.mana:
                self.player.mana += s.mana
                logger.debug(f"{s.name} provides {s.mana} mana")
            if s.heals:
                self.player.hit_points += s.heals
                logger.debug(f"{s.name} heals {s.heals} points")
            if s.damage:
                logger.debug(f"{s.name} does {s.damage} damage")
                self.boss.hit_points -= s.damage
            e.time -= 1
            if e.time == 0:
                expiring_effects.append(i)
            logger.debug(f"{s.name} now has a timer of {e.time}")
        for i in sorted(expiring_effects, reverse=True):
            s = self.effects[i].spell
            if s.armor:
                self.player.armor -= s.armor
                logger.debug(
                    f"{s.name} wears off. Player armor is now {self.player.armor}"
                )
            self.effects.pop(i)

    def play_turn(self, spell: Spell, spending_limit: int):
        for e in self.effects:
            if spell.name == e.spell.name:
                return GameState.ILLEGAL
        if spell.cost > self.player.mana:
            return GameState.ILLEGAL
        ## Player part of the turn
        logger.debug(f"-- Player Turn --")
        logger.debug(f"player={self.player}")
        logger.debug(f"boss={self.boss}")
        self.apply_effects()
        if self.boss.hit_points <= 0:
            return GameState.PLAYER_WINS
        self.mana_spent += spell.cost
        if spending_limit and self.mana_spent >= spending_limit:
            return GameState.ILLEGAL
        self.player.mana -= spell.cost
        logger.debug(f"Player casts {spell.name}")
        if spell.timer:
            self.effects.append(Effect(spell, spell.timer))
            if spell.armor:
                self.player.armor += spell.armor
        else:
            if spell.heals:
                logger.debug(f"{spell.name} heals {spell.heals} points.")
                self.player.hit_points += spell.heals
            if spell.damage:
                logger.debug(f"{spell.name} does {spell.damage} damage points")
                self.boss.hit_points -= spell.damage
        if self.boss.hit_points <= 0:
            return GameState.PLAYER_WINS
        ## Boss part of the turn
        logger.debug(f"-- Boss Turn --")
        logger.debug(f"player={self.player}")
        logger.debug(f"boss={self.boss}")
        self.apply_effects()
        if self.boss.hit_points <= 0:
            return GameState.PLAYER_WINS
        damage = self.boss.damage - self.player.armor
        logger.debug(f"Boss attack does {damage} points' damage")
        self.player.hit_points -= max(1, self.boss.damage - self.player.armor)
        if self.player.hit_points <= 0:
            return GameState.BOSS_WINS
        return GameState.INCOMPLETE


def part1(context: AOCContext):
    player = Entity(hit_points=50, mana=500)
    current_best = None
    search_states = PriorityQueue()
    search_states.put((0, Game(context, player)))
    min_turn_cost = min([s.cost for s in context.available_spells])
    while not search_states.empty():
        (_, game) = search_states.get()
        if current_best and game.mana_spent + min_turn_cost >= current_best:
            continue
        for spell in context.available_spells:
            test_game = copy.deepcopy(game)
            status = test_game.play_turn(spell, current_best)
            logger.debug(
                f"player={game.player.hit_points}, boss={game.boss.hit_points}"
            )
            if status == GameState.PLAYER_WINS:
                logger.info(f"winner that costs {test_game.mana_spent}")
                if current_best is None or test_game.mana_spent < current_best:
                    current_best = test_game.mana_spent
                else:
                    logger.info(
                        f"discarding incomplete game with score {test_game.mana_spent} >= {current_best}"
                    )
                    break
            elif status == GameState.INCOMPLETE:
                if current_best is None or test_game.mana_spent < current_best:
                    search_states.put((test_game.mana_spent, test_game))
    return str(current_best)


def part2(context: AOCContext):
    player_hit_points = 100
    combinations = legal_combinations(context)
    combinations.sort(key=cost, reverse=True)
    largest_losing_cost = 0
    losing_rounds = 0
    losing_combo = 0
    for c in combinations:
        boss = Entity(context.boss.hit_points, context.boss.damage, context.boss.armor)
        player = Entity(
            player_hit_points,
            sum(item.damage for item in c),
            sum(item.armor for item in c),
        )
        won, rounds = fight_boss(player, boss)
        if not won:
            losing_rounds = rounds
            largest_losing_cost = sum(item.cost for item in c)
            losing_combo = c
            break
    logger.info(
        f"Player: {player} lost in {losing_rounds} rounds after purchasing {', '.join([i.name for i in losing_combo])} for {largest_losing_cost} gold pieces."
    )

    return str(largest_losing_cost)


tests = [
    (
        """Hit Points: 58
Damage: 9
""",
        1269,
        part1,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    # def gd(*args, **kwargs):
    #     return tests[0][0]
    # aocd.get_data = gd
    # ctx = preprocess()
    # player = Entity(hit_points=10, mana=250)
    # ctx.boss.hit_points = 14
    # ctx.boss.damage = 8
    # spells = {s.name: s for s in ctx.available_spells}
    # game = Game(ctx, player)
    # def checked_cast(sn: str):
    #     state = game.play_turn(spells[sn])
    #     logger.debug(state)
    #     logger.debug(f"\n")
    # checked_cast("Recharge")
    # checked_cast("Shield")
    # checked_cast("Drain")
    # checked_cast("Poison")
    # checked_cast("Magic Missile")
    logger.remove()
    logger.add(sys.stderr, level="INFO")
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
