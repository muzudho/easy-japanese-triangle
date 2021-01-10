from enum import Enum
from random import randrange


class Piece(Enum):
    """
    .
    """
    NONE = 0
    """
    . ->
    """
    RIGHT = 1
    """
    .
    |
    v
    """
    DOWN = 2
    """
    . ->
    |
    v
    """
    BOTH = 3


def starting_sq(index, n):
    """Starting square.
    Example:

    n = 4

    ...a
    ..b.
    .c..
    d...

    f(0) = 3 ... a
    f(1) = 6 ... b
    f(2) = 9 ... c
    f(3) = 12 ... d
    """
    return (index+1) * (n-1)


def random_dir():
    """
    0 <- .
         |
         v
         1
    """

    return randrange(2)


def create_board(n):
    """Create a board.

    Example:
    n=3

    0 0 0
    0 0 0
    0 0 0
    """
    return [0] * (n**2)


def print_board(board, n):
    for row in range(0, n):
        for column in range(0, n):
            print(f"{board[row*n+column]} ", end="")
        print("")  # New line.
    pass


print("start")

# Elemental number
n = 3

board = create_board(n)

for index in range(0, n):
    print(f"n={n} index={index} stargin sq={starting_sq(index,n)}")
    dir = random_dir()
    print(f"dir={dir}")
    print_board(board, n)
    pass

"""
# Square number
#
# 0 1
# 2 3
#
# Starting square number
sq = 0

# Random search
#
# . --> 0
# |
# v
# 1
#
dir = randrange(2)

if dir == 0:
    sq += 1
else:
    sq += 2

board[sq] = 1

answers = set()
answers.add(11)
for answer in answers:
    print(f"answer={answer}")

"""

print("finished")
