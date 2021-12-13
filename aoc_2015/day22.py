import itertools
import re
import sys
import operator
from collections import defaultdict, namedtuple
from copy import copy
from dataclasses import dataclass
from enum import Enum
from itertools import product
from math import prod
from queue import PriorityQueue
from typing import List, Dict, Any, Tuple
import aocd
from aoc_2015 import aoc_year
from loguru import logger

aoc_day = 22
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
    starting_player: Dict
    starting_boss: Dict
    available_spells: Dict


def get_player():
    return """Hit Points: 50
Mana: 500
""".splitlines()


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    boss = {}
    for line in raw:
        k, v = line.split(": ")
        boss[k.lower().replace(" ", "_")] = int(v)
    player = {}
    for line in get_player():
        k, v = line.split(": ")
        player[k.lower().replace(" ", "_")] = int(v)
    player["armor"] = 0
    available_spells = {
        "Magic Missile": {
            "cost": 53,
            "damage": 4,
            "healing": 0,
            "defense": 0,
            "timer": 1,
            "mana": 0,
        },
        "Drain": {
            "cost": 73,
            "damage": 2,
            "healing": 2,
            "defense": 0,
            "timer": 1,
            "mana": 0,
        },
        "Shield": {
            "cost": 113,
            "damage": 0,
            "healing": 0,
            "defense": 7,
            "timer": 6,
            "mana": 0,
        },
        "Poison": {
            "cost": 173,
            "damage": 3,
            "healing": 0,
            "defense": 0,
            "timer": 6,
            "mana": 0,
        },
        "Recharge": {
            "cost": 229,
            "damage": 0,
            "healing": 0,
            "defense": 0,
            "timer": 5,
            "mana": 101,
        },
    }
    for k, v in available_spells.items():
        available_spells[k]["name"] = k

    context = AOCContext(
        raw,
        starting_boss=boss,
        starting_player=player,
        available_spells=available_spells,
    )
    return context


class GameState(Enum):
    ONGOING = 0
    PLAYER_WON = 1
    BOSS_WON = 2
    ILLEGAL = 3


def apply_effects(effects, player, boss):
    rv = []
    for effect in effects:
        if effect["timer"] == 0:
            player["armor"] -= effect["defense"]
            continue

        boss["hit_points"] -= effect["damage"]
        player["hit_points"] += effect["healing"]
        player["mana"] += effect["mana"]
        eo = copy(effect)
        eo["timer"] -= 1
        rv.append(eo)
    return rv


def play_round(state, spell, current_best, hard_mode: bool = False):
    boss = copy(state["boss"])
    player = copy(state["player"])
    state_out = {"player": player, "boss": boss, "mana_spent": state["mana_spent"]}
    if hard_mode:
        player["hit_points"] -= 1
        if player["hit_points"] < 1:
            state_out["current_effects"] = []
            state_out["current_state"] = GameState.BOSS_WON
            return state_out

    player_effects = apply_effects(state["current_effects"], player, boss)
    if boss["hit_points"] < 1:
        state_out["current_effects"] = player_effects
        state_out["current_state"] = GameState.PLAYER_WON
        return state_out
    for e in player_effects:
        if e["name"] == spell["name"] and e["timer"] > 0:
            state_out["current_effects"] = player_effects
            state_out["current_state"] = GameState.ILLEGAL
            return state_out
    player["mana"] -= spell["cost"]
    if player["mana"] < 0:
        state_out["current_effects"] = player_effects
        state_out["current_state"] = GameState.ILLEGAL
        return state_out
    player["armor"] += spell["defense"]
    state_out["mana_spent"] += spell["cost"]
    if current_best is not None and state_out["mana_spent"] > current_best:
        state_out["current_effects"] = player_effects
        state_out["current_state"] = GameState.ILLEGAL
        return state_out

    player_effects.append(spell)

    boss_effects = apply_effects(player_effects, player, boss)
    state_out["current_effects"] = boss_effects
    if boss["hit_points"] < 1:
        state_out["current_state"] = GameState.PLAYER_WON
        return state_out

    player["hit_points"] -= max(1, boss["damage"] - player["armor"])
    if player["hit_points"] < 1:
        state_out["current_state"] = GameState.BOSS_WON
        return state_out

    state_out["current_state"] = GameState.ONGOING
    return state_out


def part1(context: AOCContext):
    initial_game = {
        "player": copy(context.starting_player),
        "boss": copy(context.starting_boss),
        "current_effects": [],
        "mana_spent": 0,
        "current_state": GameState.ONGOING,
    }
    game_states = PriorityQueue()
    game_states.put((0, initial_game))
    current_best = sys.maxsize
    minimum_mana_spend = 53
    while not game_states.empty():
        (_, state) = game_states.get()
        for spell in list(context.available_spells.values()):
            result = play_round(state, spell, current_best)
            if result["current_state"] == GameState.ONGOING:
                # print(f"{result}")
                if result["mana_spent"] + minimum_mana_spend < current_best:
                    game_states.put((-result["mana_spent"], result))
            elif result["current_state"] == GameState.PLAYER_WON:
                if result["mana_spent"] < current_best:
                    current_best = result["mana_spent"]
        # if round == 2:
        #     break
    return str(current_best)


def part2(context: AOCContext):
    initial_game = {
        "player": copy(context.starting_player),
        "boss": copy(context.starting_boss),
        "current_effects": [],
        "mana_spent": 0,
        "current_state": GameState.ONGOING,
    }
    game_states = PriorityQueue()
    game_states.put((0, initial_game))
    current_best = sys.maxsize
    minimum_mana_spend = 53
    while not game_states.empty():
        (_, state) = game_states.get()
        for spell in list(context.available_spells.values()):
            result = play_round(state, spell, current_best, hard_mode=True)
            if result["current_state"] == GameState.ONGOING:
                # print(f"{result}")
                if result["mana_spent"] + minimum_mana_spend < current_best:
                    game_states.put((-result["mana_spent"], result))
            elif result["current_state"] == GameState.PLAYER_WON:
                if result["mana_spent"] < current_best:
                    current_best = result["mana_spent"]
        # if round == 2:
        #     break
    return str(current_best)


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
