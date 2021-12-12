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


@dataclass
class Item:
    name: str
    cost: int
    damage: int
    armor: int


@dataclass
class AOCContext:
    raw: List[str]
    boss: Entity

    weapons: List[Item]
    armor: List[Item]
    rings: List[Item]


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

    weapons = [
        Item("Dagger", 8, 4, 0),
        Item("Shortsword", 10, 5, 0),
        Item("Warhammer", 25, 6, 0),
        Item("Longsword", 40, 7, 0),
        Item("Greataxe", 74, 8, 0),
    ]

    armor = [
        Item("Leather", 13, 0, 1),
        Item("Chainmail", 31, 0, 2),
        Item("Splintmail", 53, 0, 3),
        Item("Bandedmail", 75, 0, 4),
        Item("Platemail", 102, 0, 5),
    ]

    rings = [
        Item("Damage +1", 25, 1, 0),
        Item("Damage +2", 50, 2, 0),
        Item("Damage +3", 100, 3, 0),
        Item("Defense +1", 20, 0, 1),
        Item("Defense +2", 40, 0, 2),
        Item("Defense +3", 80, 0, 3),
    ]

    context = AOCContext(raw, boss, weapons, armor, rings)
    return context


def cost(list_of_items: List[Item]):
    return sum(i.cost for i in list_of_items)


def fight_boss(player: Entity, boss: Entity):
    n_rounds = 0
    while player.hit_points > 0 and boss.hit_points > 0:
        n_rounds += 1
        boss.hit_points -= max(1, player.damage - boss.armor)
        if boss.hit_points <= 0:
            break
        player.hit_points -= max(1, boss.damage - player.armor)
    return player.hit_points > boss.hit_points, n_rounds


def legal_combinations(context: AOCContext):
    combinations = [[w] for w in context.weapons]
    combinations.extend(
        list(combo) for combo in product(context.weapons, context.armor)
    )
    one_ring_combinations = []
    for c in combinations.copy():
        for r in itertools.combinations(context.rings, 1):
            new_combo = c.copy()
            new_combo.extend(list(r))
            one_ring_combinations.append(new_combo)
    two_ring_combinations = []
    for c in combinations.copy():
        for r in itertools.combinations(context.rings, 2):
            new_combo = c.copy()
            new_combo.extend(list(r))
            two_ring_combinations.append(new_combo)
    combinations.extend(one_ring_combinations)
    combinations.extend(two_ring_combinations)
    return combinations


def part1(context: AOCContext):
    player_hit_points = 100
    combinations = legal_combinations(context)
    combinations.sort(key=lambda x: sum(i.cost for i in x))
    winning_cost = 0
    winning_rounds = 0
    winning_combo = None
    for c in combinations:
        boss = Entity(context.boss.hit_points, context.boss.damage, context.boss.armor)
        player = Entity(
            player_hit_points,
            sum(item.damage for item in c),
            sum(item.armor for item in c),
        )
        won, rounds = fight_boss(player, boss)
        if won:
            winning_rounds = rounds
            winning_cost = sum(item.cost for item in c)
            winning_combo = c
            break
    logger.info(
        f"Player: {player} wins in {winning_rounds} rounds after purchasing {', '.join([i.name for i in winning_combo])} for {winning_cost} gold pieces."
    )
    return str(winning_cost)


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
        """Hit Points: 12
Damage: 7
Armor: 2
""",
        605,
        part1,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    player = Entity(8, 5, 5)
    boss = Entity(12, 7, 2)
    win, rounds = fight_boss(player, boss)
    logger.debug(f"Win: {win}, rounds: {rounds}")
    # for i, t in enumerate(tests[start:finish]):
    #
    #     def gd(*args, **kwargs):
    #         return t[0]
    #
    #     aocd.get_data = gd
    #     result = t[2](preprocess())
    #     if f"{result}" != f"{t[1]}":
    #         logger.error(f"Test {start + i + 1} failed: got {result}, expected {t[1]}")
    #         break
    #     else:
    #         logger.success(f"Test {start + i + 1}: {t[1]}")


if __name__ == "__main__":
    test()
