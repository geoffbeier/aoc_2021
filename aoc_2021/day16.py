import re
import sys
from dataclasses import dataclass
from math import prod
from typing import List

import aocd
from loguru import logger

from . import aoc_year

aoc_day = 16
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


class Packet:
    version: int
    type_id: int
    bitstream: str
    cur: int
    sub_packets: List["Packet"]

    def __init__(self, bitstream: str):
        self.version = 0
        self.type_id = 0
        self.bitstream = bitstream
        self.cur = 0
        self.sub_packets = []
        self.parse()

    def read_bits(self, num_bits: int):
        rv = int(self.bitstream[self.cur : self.cur + num_bits], 2)
        self.cur += num_bits
        return rv

    def parse(self):
        self.version = self.read_bits(3)
        self.type_id = self.read_bits(3)
        return self.cur

    def value(self):
        raise NotImplementedError


class LiteralValuePacket(Packet):
    def __init__(self, bitstream: str = None):
        self._value = 0
        super().__init__(bitstream)

    def parse(self):
        super().parse()
        if self.type_id != 4:
            raise ValueError(
                f"LiteralValuePacket: expected type_id 4, got type_id {self.type_id}"
            )
        value_bits = ""
        while self.bitstream[self.cur] == "1":
            value_bits += self.bitstream[self.cur + 1 : self.cur + 5]
            self.cur += 5
        value_bits += self.bitstream[self.cur + 1 : self.cur + 5]
        self.cur += 5
        self._value = int(value_bits, 2)
        return self.cur

    def value(self):
        return self._value


class OperatorPacket(Packet):
    def __init__(self, bitstream: str = None):
        super().__init__(bitstream)

    def parse(self):
        super().parse()
        if self.type_id == 4:
            raise ValueError(f"OperatorPacket: expected any type_id other than 4")
        length_type = self.read_bits(1)
        if length_type == 0:
            length = self.read_bits(15)
            end = self.cur + length
            while self.cur <= end - 11:
                self.sub_packets.append(make_packet(self.bitstream[self.cur :]))
                self.cur += self.sub_packets[-1].cur
        else:
            count = self.read_bits(11)
            for _ in range(count):
                self.sub_packets.append(make_packet(self.bitstream[self.cur :]))
                self.cur += self.sub_packets[-1].cur
            assert len(self.sub_packets) == count

    def value(self):
        if self.type_id == 0:
            return sum(p.value() for p in self.sub_packets)
        elif self.type_id == 1:
            return prod(p.value() for p in self.sub_packets)
        elif self.type_id == 2:
            return min(p.value() for p in self.sub_packets)
        elif self.type_id == 3:
            return max(p.value() for p in self.sub_packets)
        elif self.type_id == 5:
            assert len(self.sub_packets) == 2
            return 1 if self.sub_packets[0].value() > self.sub_packets[1].value() else 0
        elif self.type_id == 6:
            assert len(self.sub_packets) == 2
            return 1 if self.sub_packets[0].value() < self.sub_packets[1].value() else 0
        elif self.type_id == 7:
            assert len(self.sub_packets) == 2
            return (
                1 if self.sub_packets[0].value() == self.sub_packets[1].value() else 0
            )


def make_packet(bitstream: str):
    pkt = Packet(bitstream)
    if pkt.type_id == 4:
        return LiteralValuePacket(bitstream)
    return OperatorPacket(bitstream)


@dataclass
class AOCContext:
    raw: List[str]
    bitstream: str


def preprocess():
    raw = aocd.get_data(day=aoc_day, year=aoc_year).splitlines()
    bits = ""
    for nibble in raw[0]:
        bits += f"{int(nibble, 16):04b}"
    context = AOCContext(raw, bits)
    return context


def flatten(pkt: Packet):
    packet_list = [pkt]
    if pkt.sub_packets:
        for p in pkt.sub_packets:
            packet_list.extend(flatten(p))
    return packet_list


def part1(context: AOCContext):
    pkt = make_packet(context.bitstream)
    tot = sum(p.version for p in flatten(pkt))
    return str(tot)


def part2(context: AOCContext):
    pkt = make_packet(context.bitstream)
    return str(pkt.value())


tests = [
    (
        """8A004A801A8002F478
""",
        16,
        part1,
    ),
    (
        """620080001611562C8802118E34
""",
        12,
        part1,
    ),
]


def test(start: int = 0, finish: int = len(tests)):
    aocd.get_data = lambda *_, **__: "38006F45291200\n"
    ctx = preprocess()
    pkt = make_packet(ctx.bitstream)
    logger.debug(f"subpackets: {len(pkt.sub_packets)}")
    assert len(pkt.sub_packets) == 2
    aocd.get_data = lambda *_, **__: "EE00D40C823060\n"
    ctx = preprocess()
    pkt = make_packet(ctx.bitstream)
    logger.debug(f"subpackets: {len(pkt.sub_packets)}")
    assert len(pkt.sub_packets) == 3

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
