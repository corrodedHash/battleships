"""Contains Field class"""
import copy
from enum import Enum

from util import Size, Coord, Space, toAlpha


class Field:
    """Battleship field"""
    class States(Enum):
        """Possible states a battleship field cell can be in"""
        empty = 0
        miss = 1
        hit = 2
        suspect = 3

    def __init__(self, size: Size):
        assert size.width > 0
        assert size.height > 0
        self.size = size
        self.cells = Field.generate_field(self.size)

    @staticmethod
    def generate_field(size: Size):
        """Generates a 2D list to access all cells of the field"""
        result = [[Field.States.empty for _ in range(
            size.height)] for _ in range(size.width)]
        return result

    def getMargins(self, cell: Coord):
        result = Space()
        for direction in Space.Direction:
            dirTuple = Space.tupleDirMap[direction]
            count = 0
            new_point = copy.deepcopy(cell) + dirTuple
            while new_point in self.size and self[new_point] == Field.States.empty:
                new_point = new_point + dirTuple
                count += 1
            result[direction] = count

        return result

    def __getitem__(self, key):
        if isinstance(key, Coord):
            return self.cells[key.x][key.y]
        else:
            raise TypeError

    def __setitem__(self, key, value):
        if isinstance(key, Coord):
            self.cells[key.x][key.y] = value
        else:
            raise TypeError

    def allCells(self):
        """Returns a generator to access all cells of the field"""
        yield (Coord(x, y) for x in range(self.size.width) for y in range(self.size.height))

    def printTable(self, char_fun=lambda board, x, y: board.cells[x][y]):
        result = "  "
        result += "".join(["| {:<2}".format(x + 1) for x in range(len(self.cells))])
        result += "\n--"
        result += "+---" * len(self.cells)
        result += "\n"
        for y in range(len(self.cells[0])):
            result += "{0} ".format(toAlpha(y))
            for x in range(len(self.cells)):
                result += "|{:^3}".format(char_fun(self, x, y))
            result += "\n--"
            result += "+---" * len(self.cells)
            result += "\n"
        return result
