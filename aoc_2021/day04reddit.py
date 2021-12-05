from itertools import chain

# solution from https://old.reddit.com/r/adventofcode/comments/r8i1lq/2021_day_4_solutions/hn7jm8x/


class Day4:
    def __init__(self, data):
        numbers, *boards = data.split("\n\n")
        (*self.numbers,) = map(int, numbers.split(","))
        self.boards = [
            [[int(n) for n in row.split()] for row in board.splitlines()]
            for board in boards
        ]
        self.winning_score = self.find_winning_score()
        self.losing_score = self.find_losing_score()

    def find_winning_score(self):
        called = []
        for number in self.numbers:
            called.append(number)
            for board in self.boards:
                if any(set(line) < set(called) for line in chain(board, zip(*board))):
                    unmarked = {n for row in board for n in row} - set(called)
                    return sum(unmarked) * number

    def find_losing_score(self):
        called = self.numbers.copy()
        while called:
            last = called.pop()
            for board in self.boards:
                if not any(
                    set(line) < set(called) for line in chain(board, zip(*board))
                ):
                    unmarked = {n for row in board for n in row} - {last, *called}
                    return sum(unmarked) * last


test_data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

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
 2  0 12  3  7"""

with open("data/github.geoffbeier.710727/2021_04_input.txt") as f:
    data = f.read()

day4_test = Day4(test_data)
assert day4_test.winning_score == 4512
assert day4_test.losing_score == 1924

day4 = Day4(data)
print("Part 1:", day4.winning_score)
print("Part 2:", day4.losing_score)
