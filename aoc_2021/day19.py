import itertools
import re
import sys
import numpy
import operator
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from math import prod
from typing import List, Dict, Any, Tuple
import aocd
from numpy.typing import ArrayLike

from . import aoc_year
from loguru import logger

aoc_day = 19
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

# Using numpy because I think brute force will work if I do, so I won't have to look up how to do this right using
# matrix math. I suspect that even if I need to, numpy will make it easier.
x, y, z = 1, 2, 3
axes = [numpy.array(combo) for combo in itertools.permutations([x, y, z])]
rotations = [
    numpy.array(direction) for direction in itertools.product([-1, 1], [-1, 1], [-1, 1])
]


class Scanner:
    id: int
    beacons: ArrayLike
    location: ArrayLike

    def __init__(self, chunk):
        lines = chunk.split("\n")
        self.id = int(re.match(r"--- scanner (\d+?) ---", lines[0]).group(1))
        if not lines[-1]:
            lines.pop()
        points = [[int(n) for n in line.split(",")] for line in lines[1:]]
        self.beacons = numpy.array(points)
        self.location = None

    def try_align(self, other: "Scanner"):
        assert other.location is None
        for axis, rotation in [(a, r) for a, r in itertools.product(axes, rotations)]:
            r_other_beacons = other.beacons[:, axis - 1] * rotation
            differences = (
                self.beacons[numpy.newaxis, :] - r_other_beacons[:, numpy.newaxis]
            )
            beacon_counts = [
                numpy.unique(differences[..., i], return_counts=True) for i in range(3)
            ]
            if all([max(counts) >= 12 for beacon, counts in beacon_counts]):
                other.beacons = r_other_beacons
                offset = numpy.array([bc[0][bc[1] >= 12][0] for bc in beacon_counts])
                other.location = offset + self.location
                return True
        return False

    def __str__(self):
        return f"Scanner {self.id}"


@dataclass
class AOCContext:
    raw_chunks: List[str]
    scanners: List[Scanner]
    part1: bool = False


def preprocess():
    chunks = [c for c in aocd.get_data(day=aoc_day, year=aoc_year).split("\n\n")]
    scanners = [Scanner(chunk) for chunk in chunks]
    context = AOCContext(chunks, scanners)
    return context


def part1(context: AOCContext):
    logger.info(f"{len(context.scanners)} scanners in input")
    # XXX *** TODO: may need to copy these depending on part 2
    context.scanners[0].location = numpy.array([0, 0, 0])
    while any(scanner.location is None for scanner in context.scanners):
        for scanner in filter(lambda ss: ss.location is None, context.scanners):
            for candidate in filter(
                lambda xx: xx.location is not None, context.scanners
            ):
                if candidate.try_align(scanner):
                    break
    found_beacons = set()
    for s in context.scanners:
        absolute_beacons = s.beacons + s.location
        for beacon in absolute_beacons:
            found_beacons.add(tuple(beacon))
    context.part1 = True
    return str(len(found_beacons))


def part2(context: AOCContext):
    if not context.part1:
        part1(context)
    return str(
        max(
            [
                sum(numpy.abs(a.location - b.location))
                for a, b in itertools.permutations(context.scanners, 2)
            ]
        )
    )


tests = [
    (
        """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""",
        79,
        part1,
    ),
    (
        """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""",
        3621,
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
