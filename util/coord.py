import re
from .alphanum import toAlpha, fromAlpha


class Coord:
    def __init__(self, x=0, y=0, alphanum=None):
        if alphanum is not None:
            alphapart = re.search(r'\A[A-Z]+', alphanum.upper())
            if not alphapart:
                raise RuntimeError
            self.y = fromAlpha(alphapart.group(0).upper())

            numpart = re.search(r'\d+\Z', alphanum)
            if not numpart:
                raise RuntimeError
            self.x = int(numpart.group(0)) - 1
            assert self.x >= 0
        else:
            self.x = x
            self.y = y

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
        if type(other) is tuple:
            return Coord(self.x - other[0], self.y - other[1])
        else:
            raise RuntimeError

    def __add__(self, other):
        if type(other) is tuple:
            return Coord(self.x + other[0], self.y + other[1])
        else:
            raise RuntimeError

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()

    def getHumanStr(self):
        return toAlpha(self.y) + str(self.x + 1)

    def __deepcopy__(self, other):
        return Coord(self.x, self.y)
