from enum import Enum
from random import randrange, shuffle


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
        self.fill_ray(Direction.RIGHT.value, 1)
        # print(f"(Ray) e=1 dir={Direction.RIGHT.value}")
        # self.value.print()

        # Leftest column.
        self.fill_ray(Direction.DOWN.value, n)
        # print(f"(Ray) e={n} dir={Direction.DOWN.value}")
        # self.value.print()

        e_list = list(range(2, n))
        # print(f"e_list1={e_list}")
        shuffle(e_list)
        # print(f"e_list2={e_list}")
        for e in e_list:
            direction = Board.random_direction()
            self.fill_ray(direction.value, e)
            # print(f"(Ray) e={e} dir={dir}")
            # self.value.print()

    @staticmethod
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
