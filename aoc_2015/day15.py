import itertools
import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple, Iterable
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 15


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def make_ingredient(description: str):
    name, attributes = description.split(": ")
    parsed_attributes = {}
    for a in attributes.split(", "):
        k, v = a.strip().split(" ")
        parsed_attributes[k] = int(v)
    return Ingredient(name=name, **parsed_attributes)


@dataclass
class AOCContext:
    raw: List[str]
    ingredients: Dict[str, Ingredient]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    ingredients = {}
    for line in raw:
        ingredient = make_ingredient(line.strip())
        ingredients[ingredient.name] = ingredient
    context = AOCContext(raw, ingredients)
    return context


def score_combination(amounts: Tuple[int], ingredients: Iterable[Ingredient]):
    capacity = 0
    durability = 0
    flavor = 0
    texture = 0
    for amount, ingredient in zip(amounts, ingredients):
        capacity += amount * ingredient.capacity
        durability += amount * ingredient.durability
        flavor += amount * ingredient.flavor
        texture += amount * ingredient.texture
    capacity = max(0, capacity)
    durability = max(0, durability)
    flavor = max(0, flavor)
    texture = max(0, texture)
    return capacity * durability * flavor * texture


def part1(context: AOCContext):
    available_ingredients = context.ingredients
    possible_combinations = filter(
        lambda x: sum(x) == 100,
        itertools.permutations(range(0, 101), len(available_ingredients)),
    )
    best_score = -1
    best_combination = None
    for combination in possible_combinations:
        curr_score = score_combination(combination, available_ingredients.values())
        if curr_score > best_score:
            best_score = curr_score
            best_combination = combination
    recipe = []
    for amount, ingredient in zip(best_combination, available_ingredients.keys()):
        recipe.append(f"{amount} tsp {ingredient}")
    logger.info(f"Recipe {recipe} scores {best_score}")
    return str(best_score)


def calorie_combinations(
    amounts: Iterable[Tuple[int]],
    ingredients: Iterable[Ingredient],
    calorie_target: int,
):
    for combo in amounts:
        calorie_count = sum(
            amount * ingredient.calories
            for amount, ingredient in zip(combo, ingredients)
        )
        if calorie_count == calorie_target:
            yield combo


def part2(context: AOCContext):
    available_ingredients = context.ingredients
    possible_combinations = filter(
        lambda x: sum(x) == 100,
        itertools.permutations(range(0, 101), len(available_ingredients)),
    )
    best_score = -1
    best_combination = None
    for combination in calorie_combinations(
        possible_combinations, available_ingredients.values(), 500
    ):
        curr_score = score_combination(combination, available_ingredients.values())
        if curr_score > best_score:
            best_score = curr_score
            best_combination = combination
    recipe = []
    for amount, ingredient in zip(best_combination, available_ingredients.keys()):
        recipe.append(f"{amount} tsp {ingredient}")
    logger.info(f"Recipe {recipe} scores {best_score} for 500 Calories")
    return str(best_score)


tests = [
    (
        """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
""",
        62842880,
        part1,
    ),
    (
        """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
""",
        57600000,
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
