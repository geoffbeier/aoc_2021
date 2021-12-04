import sys
from dataclasses import dataclass
from math import prod
from typing import List, Dict, Any
import aocd
from . import aoc_year
from loguru import logger

from collections import defaultdict, OrderedDict

aoc_day = 4


@dataclass
class Winner:
    card: List
    score: int
    number: int
    row: int


def get_card_size(cards: List[str]):
    cols = 0
    rows = 0
    for i, line in enumerate(cards):
        line = line.strip()
        if not cols:
            cols = len(line.split())
        if not line:
            rows = i
            break
    return cols, rows


def preprocess():
    context = {"raw": aocd.get_data(day=aoc_day, year=aoc_year).splitlines()}
    lines = context["raw"]
    context["numbers_drawn"] = [int(n) for n in lines[0].split(",")]
    cols, rows = get_card_size(lines[2:])
    cards = []
    card = []
    for line in lines[2:]:
        line = line.strip()
        if not line:
            cards.append(card.copy())
            card = []
            continue
        row = OrderedDict()
        for n in line.split():
            row[int(n)] = False
        card.append(row)
    cards.append(card)
    context["cards"] = cards
    context["cols"] = cols
    context["rows"] = rows
    return context


def score_card(card: List):
    score = 0
    for row in card:
        score += sum(k for k in list(row.keys()) if not row[k])
    return score


def mark_card(card, number):
    hits = set()
    for i, row in enumerate(card):
        if number in row:
            row[number] = True
            hits.add(i)
    return hits


def play_number(cards: List, number: int, rows: int, cols: int):
    winning_card_indexes = []
    winners: List[Winner] = []
    for card_num, card in enumerate(cards):
        hits = mark_card(card, number)
        # if there's no winner, check to see if this is a winner
        if hits:
            for h in hits:
                numbers_in_row = list(card[h].keys())
                hit_idx = numbers_in_row.index(number)
                if sum(card[h][k] for k in numbers_in_row) == rows:
                    winning_card_indexes.append(card_num)
                    winners.append(Winner(card, score_card(card) * number, number, h))
                    break
                col_mark_count = 0
                for test_row in card:
                    if test_row[list(test_row.keys())[hit_idx]]:
                        col_mark_count += 1
                if col_mark_count == cols:
                    winning_card_indexes.append(card_num)
                    winners.append(Winner(card, score_card(card) * number, number, h))
    return len(winning_card_indexes) != 0, winners, winning_card_indexes


def part1(context: Dict[str, Any]):
    cards = context["cards"].copy()
    logger.info(f"Part 1: playing {len(cards)} cards")
    for number in context["numbers_drawn"]:
        logger.debug(f"Call: {number}")
        found_winner, winning_cards, _ = play_number(
            cards, number, context["rows"], context["cols"]
        )
        if found_winner:
            return str(winning_cards[0].score)
    return str(None)


def part2(context: Dict[str, Any]):
    cards = context["cards"].copy()
    logger.info(f"Part 2: playing {len(cards)} cards")
    winners: List[Winner] = []
    for number in context["numbers_drawn"]:
        found_winner, winning_cards, winning_card_indexes = play_number(
            cards, number, context["rows"], context["cols"]
        )
        if found_winner:
            if len(winning_card_indexes) > 1:
                logger.warning(
                    f"Multiple winners in one round. Undefined by rules. {winning_card_indexes}"
                )
            for winner in winning_cards:
                winners.append(winner)
            for i in sorted(winning_card_indexes, reverse=True):
                cards.pop(i)
    return str(winners[-1].score)


tests = [
    (
        """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""",
        4512,
        part1,
    ),
    (
        """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""",
        1924,
        part2,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    for i, t in enumerate(tests[start:finish]):

        def gd(*args, **kwargs):
            return t[0]

        aocd.get_data = gd
        result = t[2](preprocess())
        if result != f"{t[1]}":
            logger.error(f"Test {start + i + 1} failed: got {result}, expected {t[1]}")
            break
        else:
            logger.success(f"Test {start + i + 1}: {t[1]}")


if __name__ == "__main__":
    logger.debug(f"Starting tests.")
    test()
