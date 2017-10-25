import copy
import itertools
from enum import Enum

from util import Size, Coord, Space, toAlpha 

class Field:
    class States(Enum):
        empty = 0
        miss = 1
        hit = 2
        suspect = 3

    def __init__(self, size: Size):
        assert size.width > 0
        assert size.height > 0
        self.size = size
        self.cells = Field.generateField(self.size)

    @staticmethod
    def generateField(size: Size):
        result = [[Field.States.empty for _ in range(size.height)] for _ in range(size.width)]
        return result

    def getMargins(self, cell: Coord):
        tmp_result = list() 
        for direction in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            count = 0
            new_point = copy.deepcopy(cell) + direction
            while new_point in self.size and self[new_point] == Field.States.empty:
                new_point = new_point + direction
                count += 1
            tmp_result.append(count)
        result = Space()
        result.left = tmp_result[0]
        result.top = tmp_result[1]
        result.right = tmp_result[2]
        result.bottom = tmp_result[3]
         
        return result
    
    def __getitem__(self, key):
        if type(key) is Coord:
            return self.cells[key.x][key.y]
        else:
            raise TypeError

    def __setitem__(self, key, value):
        if type(key) is Coord:
            self.cells[key.x][key.y] = value
        else:
            raise TypeError


    def allCells(self):
        for x in range(self.size.width):
            for y in range(self.size.height):
                yield Coord(x, y)

    def printTable(self, char_fun=lambda board, x, y: board.cells[x][y]):
        result = "  "
        for x in range(len(self.cells)):
            result += "| {:<2}".format(x + 1) 
        result += "\n--"
        for x in range(len(self.cells)):
            result += "+---" 
        result += "\n"
        for y in range(len(self.cells[0])):
            result += "{0} ".format(toAlpha(y))
            for x in range(len(self.cells)):
                result += "|{:^3}".format(char_fun(self, x, y)) 
            result += "\n--"
            for x in range(len(self.cells)):
                result += "+---" 
            result += "\n"
        return result
