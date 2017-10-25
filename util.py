import re 
class Size:
    def __init__(self, width=0, height=0):
       self.width = width
       self.height = height

    def __contains__(self, other):
        if type(other) is Coord:
            return other.x >= 0 and other.y >= 0 and self.__gt__(other)
        else:
            raise TypeError

    def __gt__(self, other):
        if type(other) is Coord:
            assert other.x >= 0
            assert other.y >= 0
            return other.x < self.width and other.y < self.height

    def __leq__(self, other):
        return not self.__leq__(other)


class Coord:
    def __init__(self, x=0, y=0, alphanum=None):
        if alphanum is not None:
            alphapart = re.search(r'\A[^\d]+', alphanum)
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

    def __getitem__(self, key, value):
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
            raise Error

    def __add__(self, other):
        if type(other) is tuple:
            return Coord(self.x + other[0], self.y + other[1])
        else:
            raise Error

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return self.__str__()

    def getHumanStr(self):
        return toAlpha(self.y) + str(self.x + 1) 

    def __deepcopy__(self, other):
        return Coord(self.x, self.y)


class Space:
    def __init__(self):
        self.top = 0
        self.bottom = 0
        self.left = 0
        self.right = 0

    def getXLine(self):
        return self.left + self.right + 1
    def getYLine(self):
        return self.top + self.bottom + 1

    def __repr__(self):
        return "(" + str(self.top) + ", " + str(self.bottom) + ", " + str(self.left) + ", " + str(self.right) + ")"

def toAlpha(number):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    power = 0
    max_num = number // len(alphabet)
    while max_num > 0:
        max_num = max_num // len(alphabet)
        power += 1

    result = ""
    while power >= 0:
        result += alphabet[number // (len(alphabet) ** power)]
        power -= 1
    return result

def fromAlpha(number):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert len(number) > 0
    power = len(number) - 1
    result = 0
    for char in number:
        result += alphabet.index(char) * (len(alphabet) ** power)
    return result
