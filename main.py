from enum import Enum
from random import randrange, shuffle
import time


def print_time_lapsed(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print(f"Time Lapsed = {int(hours)}:{int(mins)}:{sec}")


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
    OUT_OF_TRIANGLE = 4


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


def random_direction():
    """
    0 <- .
         |
         v
         1
    """

    if randrange(2):
        return Direction.RIGHT
    else:
        return Direction.DOWN


class Board:
    _n = 0
    value = []

    def __init__(self, n):
        """Create a board.

        Example:
        n=3

        0 0 0
        0 0 4
        0 4 4
        """
        self._n = n
        self.value = [0] * (n**2)
        self.fill_out_of_triangle()

    @staticmethod
    def from_unique(unique, n):
        """
        Example:

        n = 4

        0123
        456.
        78..
        9...

        (1) 4,3,2,1 の長さの文字列と、1,2,3,4 の長さの空白が交互に現れると考える。 Example: 4,1,3,2,2,3,1,4
        (2) m の長さの文字列と、 m-n の長さの空白が、 m を 1つずつ減らしながら 交互に現れる。
        (3) m を、(n-i) と言い換えると、 0 <= i <= n と昇順にできる。
        """
        obj = Board(0)
        obj.value = []
        a = 0
        for i in range(0, n):
            m = n - i
            for _j in range(0, m):
                ch = unique[a]
                a += 1
                obj.value.append(int(ch))
            for _k in range(0, i):
                obj.value.append(Piece.OUT_OF_TRIANGLE.value)
        # print(f"board len={len(obj.value)}")
        obj.n = n
        return obj

    def fill_out_of_triangle(self):
        """
        Example:

        n = 4

        ....
        ...x
        ..xx
        .xxx

        (1) 4,3,2,1 の長さの文字列と、1,2,3,4 の長さの文字列が交互に現れると考える。 Example: 4,1,3,2,2,3,1,4
        (2) m の長さの文字列と、 m-n の長さの文字列が、 m を 1つずつ減らしながら 交互に現れる。
        (3) m を、(n-i) と言い換えると、 0 <= i <= n と昇順にできる。
        """
        n = self._n
        a = 0
        for i in range(0, n):
            m = n - i
            for _j in range(0, m):
                a += 1
            for _k in range(0, i):
                self.value[a] = Piece.OUT_OF_TRIANGLE.value
                a += 1
        # print(f"board len={len(self.value)}")

    def fill_ray(self, dir, e):
        """光線を飛ばすように、盤上の升を塗り替えます。"""
        n = self._n
        sq = Board.sq_of_e(e, n)
        # print(f"(fill_ray) e={e} sq_of_e={sq} dir={dir}")
        step, end_sq = Board.get_step_and_end_sq(dir, e, n)
        # print(f"(fill_ray) step={step} end_sq={end_sq}")

        collided = False
        while True:
            if self.value[sq] != Piece.NONE.value or sq == end_sq:
                collided = True

            self.fill_square(dir, sq)
            sq += step

            # 後判定
            if collided:
                break

        # print("(fill_ray) check.")
        # self.print()

    def print(self):
        n = self._n
        for row in range(0, n):
            for column in range(0, n):
                print(f"{self.value[row*n+column]} ", end="")
            print("")  # New line.

    def to_unique(self):
        unique = ""
        for sq in range(0, len(self.value)):
            if self.value[sq] != Piece.OUT_OF_TRIANGLE.value:
                unique += str(self.value[sq])
        return unique

    def fill_square(self, dir, sq):
        if self.value[sq] == Piece.RIGHT.value:
            if dir == Piece.RIGHT.value:
                pass
            else:
                self.value[sq] = Piece.BOTH.value
        elif self.value[sq] == Piece.DOWN.value:
            if dir == Piece.RIGHT.value:
                self.value[sq] = Piece.BOTH.value
            else:
                pass
        elif self.value[sq] == Piece.BOTH.value:
            pass
        else:
            if dir == Piece.RIGHT.value:
                self.value[sq] = Piece.RIGHT.value
            else:
                self.value[sq] = Piece.DOWN.value

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_step_and_end_sq(dir, e, n):
        """Ending square.
        Example:

        n = 4

        ..c.
        ....
        b.a.
        ....

        b = a - c
        c = a mod n

        """
        sq = Board.sq_of_e(e, n)
        if dir == Direction.RIGHT.value:
            return -1, sq - sq % n
        else:
            return -n, sq % n

    def fill_full_rays(self):
        n = self._n

        # Top row.
        self.value.fill_ray(Direction.RIGHT.value, 1)
        # print(f"(Ray) e=1 dir={Direction.RIGHT.value}")
        # self.value.print()

        # Leftest column.
        self.value.fill_ray(Direction.DOWN.value, n)
        # print(f"(Ray) e={n} dir={Direction.DOWN.value}")
        # self.value.print()

        e_list = list(range(2, n))
        # print(f"e_list1={e_list}")
        shuffle(e_list)
        # print(f"e_list2={e_list}")
        for e in e_list:
            direction = random_direction()
            self.value.fill_ray(direction.value, e)
            # print(f"(Ray) e={e} dir={dir}")
            # self.value.print()


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
# 10 =          | 9000000 |
print(f"n={n} triout={triout}")

start_time = time.time()
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

end_time = time.time()
time_lapsed = end_time - start_time
print_time_lapsed(time_lapsed)

"""
for pattern in patterns:
    print(f"pattern={pattern}")
    Board.from_unique(pattern, n).print()
"""

print(f"patterns number={len(patterns)}")

print("finished")
