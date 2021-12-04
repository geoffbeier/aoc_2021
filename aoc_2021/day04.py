import sys
from dataclasses import dataclass
from math import prod
from typing import List, Dict, Any
import aocd
from . import aoc_year
from loguru import logger

from collections import defaultdict, OrderedDict

aoc_day = 4


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


def mark_cards(cards: List, number: int, rows: int, cols: int):
    winning_card = None
    score = 0
    winning_row = None
    for card_num, card in enumerate(cards):
        for row_num, row in enumerate(card):
            if winning_card == card_num:
                continue
            if number in row:
                row[number] = True
                row_numbers = list(row.keys())
                if number == 24:
                    logger.debug(f"Marked 24. Checking {row}")
                if sum(row[k] for k in row_numbers) == rows:
                    logger.info(f"found winner: row match")
                    winning_card = card_num
                    winning_row = row_num
                    score = score_card(card) * number
                    continue
                idx = row_numbers.index(number)
                col_marked = 0
                for test_row in card:
                    keys = list(test_row.keys())
                    if test_row[keys[idx]]:
                        col_marked += 1
                if col_marked == cols:
                    logger.info(f"found winner: column match")
                    winning_card = card_num
                    winning_row = row_num
                    score = score_card(card) * number
                    continue
    return winning_card is not None, score, winning_card, winning_row


def part1(context: Dict[str, Any]):
    cards = context["cards"].copy()
    logger.info(f"Part 1: playing {len(cards)} cards")
    for number in context["numbers_drawn"]:
        logger.debug(f"Call: {number}")
        winner, score, _, _ = mark_cards(
            cards, number, context["rows"], context["cols"]
        )
        if winner:
            return str(score)
    return str(None)


def part2(context: Dict[str, Any]):
    cards = context["cards"].copy()
    logger.info(f"Part 2: playing {len(cards)} cards")
    last_winning_score = 0
    last_winning_card = None
    for number in context["numbers_drawn"]:
        winner, score, card_idx, row_idx = mark_cards(
            cards, number, context["rows"], context["cols"]
        )
        if winner:
            if score:
                last_winning_score = score
                last_winning_card = cards.pop(card_idx)
            else:
                logger.info(f"Got a winning card with a zero score. Skipping")
                cards.pop(card_idx)
            logger.info(
                f"Found a winner. Removing card. Winning number was {number}. Winning score was {score}. Removing card {card_idx}"
            )
            logger.info(f"Part 2: playing {len(cards)} cards")
            if not cards:
                return str(score)
    logger.info(
        f"Done calling numbers but not out of cards. Last winning card: {last_winning_card}\nLast winning score: {last_winning_score}"
    )
    return str(last_winning_score)


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
