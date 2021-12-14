import itertools
import re
import string
import sys
import operator
from collections import defaultdict, namedtuple, Counter
from dataclasses import dataclass
from itertools import product
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from . import aoc_year
from loguru import logger

aoc_day = 4
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
class Room:
    encrypted_name: str
    sector_id: int
    checksum: str


@dataclass
class AOCContext:
    raw: List[str]
    rooms: List[Room]


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    rooms = []
    for line in raw:
        matchexp = r"(.*)-(\d+?)\[(.....)\]"
        encrypted_name, sector_id, checksum = re.match(matchexp, line).groups()
        rooms.append(Room(encrypted_name, int(sector_id), checksum))
    context = AOCContext(raw, rooms)
    return context


def get_real_rooms(context: AOCContext):
    real_rooms = []
    for room in context.rooms:
        letters = room.encrypted_name.strip()
        letters = letters.replace("-", "")
        char_counter = Counter(letters)
        frequent = "".join(
            [str(x) for x in list([c[0] for c in char_counter.most_common()])]
        )
        calculated_checksum = ""
        for i, c in enumerate(frequent):
            if c in calculated_checksum:
                continue
            if (
                i == len(frequent) - 1
                or char_counter[c] > char_counter[frequent[i + 1]]
            ):
                calculated_checksum += c
                continue
            ii = i + 1
            while ii < len(frequent) and char_counter[frequent[ii]] == char_counter[c]:
                ii += 1
            calculated_checksum += "".join(sorted(frequent[i:ii]))

        if calculated_checksum[:5] == room.checksum:
            real_rooms.append(room)
        else:
            logger.debug(
                f"{room.encrypted_name} is not real: {calculated_checksum}/{room.checksum}"
            )
    return real_rooms


def decrypt_room_name(room: Room):
    rotation = room.sector_id % 26
    letters = string.ascii_lowercase
    key = {
        x: y for (x, y) in zip(letters, letters[rotation:] + letters[: rotation + 1])
    }
    key.update({x.upper(): key[x].upper() for x in key.keys()})
    key["-"] = " "
    decode = lambda x: "".join((key.get(c, c) for c in x))
    decrypted = decode(room.encrypted_name)
    return decrypted


def part1(context: AOCContext):
    real_rooms = get_real_rooms(context)
    logger.debug(
        f"Real rooms: {len(real_rooms)}: {[room.sector_id for room in real_rooms]}"
    )
    return str(sum(r.sector_id for r in real_rooms))


def part2(context: AOCContext):
    real_rooms = get_real_rooms(context)
    for room in real_rooms:
        decrypted_name = decrypt_room_name(room)
        if "north" in decrypted_name and "pole" in decrypted_name:
            logger.debug(f"decrypted: {decrypt_room_name(room)}")
            return room.sector_id
    return str(None)


tests = [
    (
        """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
""",
        1514,
        part1,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    print(
        decrypt_room_name(
            Room(encrypted_name="qzmt-zixmtkozy-ivhz", sector_id=343, checksum="")
        )
    )
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
