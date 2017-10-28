"""Contains Coord class"""
import re
from .alphanum import to_alpha, from_alpha


class Coord:
    """Contains coordinates of a point on a discrete 2D plane
    and operations for those coordinates"""

    def __init__(self, cell_x=0, cell_y=0, alphanum=None):
        if alphanum is not None:
            alphapart = re.search(r'\A[A-Z]+', alphanum.upper())
            if not alphapart:
                raise RuntimeError
            self.y = from_alpha(alphapart.group(0).upper())

            numpart = re.search(r'\d+\Z', alphanum)
            if not numpart:
                raise RuntimeError
            self.x = int(numpart.group(0)) - 1
            assert self.x >= 0
        else:
            self.x = cell_x
            self.y = cell_y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise KeyError

    def __setitem__(self, key, value):
        assert value >= 0
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise KeyError

    def __sub__(self, other):
        if isinstance(other, tuple):
            return Coord(self.x - other[0], self.y - other[1])
        else:
            raise RuntimeError

    def __add__(self, other):
        if isinstance(other, tuple):
            return Coord(self.x + other[0], self.y + other[1])
        else:
            raise RuntimeError

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return to_alpha(self.y) + str(self.x + 1)

    def __deepcopy__(self, other):
        return Coord(self.x, self.y)
