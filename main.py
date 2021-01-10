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


class Direction(Enum):
    """
    . ->
    """
    RIGHT = 0
    """
    .
    |
    v
    """
    DOWN = 1


def starting_x(e, n):
    """Example:

    n = 4

    ...a
    ..b.
    .c..
    d...

    f(e) = sq
    f(1) =  3 ... a
    f(2) =  2 ... b
    f(3) =  1 ... c
    f(4) =  0 ... d
    """
    # `e` is 1 origin.
    return n-(e-1)


def sq_of_e(e, n):
    """Starting square.
    Example:

    n = 4

    ...a
    ..b.
    .c..
    d...

    f(e) = sq
    f(1) =  3 ... a
    f(2) =  6 ... b
    f(3) =  9 ... c
    f(4) = 12 ... d
    """

    # `e` is 1 origin.
    # `sq` is 0 origin.
    return e * (n-1)


def get_step_and_end_sq(dir, e, n):
    """Ending square.
    Example:

    n = 4

    ..c.
    ....
    b.a.
    ....

    b = int(a / n)
    c = a mod n

    """
    sq = sq_of_e(e, n)
    if dir == Direction.RIGHT.value:
        return -1, int(sq/n)
    else:
        return -n, sq % n


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


def board_to_unique(board):
    unique = ""
    for sq in range(0, len(board)):
        if board[sq] != 0:
            unique += str(board[sq])
    return unique


def fill_square(board, dir, sq, n):
    if board[sq] == Piece.RIGHT.value:
        board[sq] = Piece.BOTH.value
    elif board[sq] == Piece.DOWN.value:
        board[sq] = Piece.BOTH.value
    elif board[sq] == Piece.BOTH.value:
        board[sq] = Piece.BOTH.value
    else:
        if dir == Piece.RIGHT.value:
            board[sq] = Piece.RIGHT.value
        else:
            board[sq] = Piece.DOWN.value
        pass


def fill_line(board, dir, e, n):
    sq = sq_of_e(e, n)
    # print(f"e={e} sq_of_e={sq} dir={dir}")
    step, end_sq = get_step_and_end_sq(dir, e, n)
    # print(f"step={step} end_sq={end_sq}")
    while sq != end_sq:
        fill_square(board, dir, sq, n)
        sq += step

    # Root.
    fill_square(board, dir, 0, n)


def calculate_unique(n):
    board = create_board(n)
    # print_board(board, n)

    # Top row.
    # print("e=1")
    fill_line(board, Direction.RIGHT.value, 1, n)
    # print_board(board, n)

    # Leftest column.
    # print(f"e={n}")
    fill_line(board, Direction.DOWN.value, n, n)
    # print_board(board, n)

    for e in range(2, n):
        # print(f"e={e}")
        dir = random_dir()
        fill_line(board, dir, e, n)
        # print_board(board, n)

    unique = board_to_unique(board)
    # print(f"unique={unique}")
    return unique


print("start")

# Elemental number
n = 3
print(f"n={n}")

patterns = set()

for i in range(0, 1000):
    unique = calculate_unique(n)
    patterns.add(unique)

for pattern in patterns:
    print(f"pattern={pattern}")

print(f"patterns number={len(patterns)}")

print("finished")
