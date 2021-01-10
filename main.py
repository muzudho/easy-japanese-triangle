from board import Board, Direction, Piece
from stopwatch import Stopwatch


print("start")

# Elemental number
n = 10
triout = 9000000
# e  = patterns | Triout  | Time
#  2 = 1        |      10 |
#  3 = 2        |      20 |
#  4 = 5        |      50 |
#  5 = 14       |     100 |
#  6 = 42       |    1000 |
#  7 = 132      |   20000 |
#  8 = 429 ?    |  300000 |
#  9 = 1427 ?   |  300000 | 50 sec
# 10 = 4701 ?   |  300000 | 1:01 sec
# 10 = 4680 ?   |  300000 |
# 10 = 4777 ?   |  600000 | 1:53 sec
# 10 = 4771 ?   |  600000 | 1:52 sec
# 10 = 4813 ?   |  900000 | 2:59 sec
# 10 = 4851 ?   | 3000000 | 9:43 sec
# 10 = 4848 ?   | 3000000 | 9:35 sec
# 10 = 4860 ?   | 9000000 | 28:39 sec
# 10 = ?        | 9000000 |
print(f"n={n} triout={triout}")

stopwatch = Stopwatch()

stopwatch.start()
patterns = set()

for i in range(0, triout):
    board = Board(n)
    # board.print()

    board.fill_full_rays()

    # print("check 1.")
    # board.print()
    unique = board.to_unique()
    # print(f"unique ={unique}")

    patterns.add(unique)

stopwatch.end()

"""
for pattern in patterns:
    print(f"pattern={pattern}")
    Board.from_unique(pattern, n).print()
"""

stopwatch.print()
print(f"patterns number={len(patterns)}")

print("finished")
