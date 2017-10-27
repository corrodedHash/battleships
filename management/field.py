"""Contains Field class"""
import copy
import enum
from enum import Enum

from util import Size, Coord, Space, to_alpha


class Field:
    """Battleship field"""
    class States(Enum):
        """Possible states a battleship field cell can be in"""
        empty = enum.auto()
        miss = enum.auto()
        hit = enum.auto()
        sunk = enum.auto()
        suspect = enum.auto()
        intact = enum.auto()

    def __init__(self, size: Size, shipcount=None):
        assert size.width > 0
        assert size.height > 0
        if shipcount is None:
            shipcount = [0, 4, 3, 2, 1]
        self.size = size
        self.shipcount = shipcount
        self.cells = Field.generate_field(self.size)

    @staticmethod
    def generate_field(size: Size):
        """Generates a 2D list to access all cells of the field"""
        result = [[Field.States.empty for _ in range(
            size.height)] for _ in range(size.width)]
        return result

    def get_margins(self, cell: Coord):
        """Return the amount of directly connecting unknown cells
        around the given coord"""
        result = Space()
        for direction in Space.Direction:
            dir_tuple = Space.tupleDirMap[direction]
            count = 0
            new_point = copy.deepcopy(cell) + dir_tuple
            while True:
                if new_point not in self.size:
                    break
                if self[new_point] != Field.States.empty:
                    break
                new_point = new_point + dir_tuple
                count += 1
            result[direction] = count

        return result

    def __getitem__(self, key):
        if isinstance(key, Coord):
            return self.cells[key.x][key.y]
        else:
            print(type(key))
            raise TypeError

    def __setitem__(self, key, value):
        if isinstance(key, Coord):
            self.cells[key.x][key.y] = value
        else:
            raise TypeError

    def __iter__(self):
        """Returns a generator to access all cells of the field"""
        w_range = range(self.size.width)
        h_range = range(self.size.height)
        return (Coord(x, y) for x in w_range for y in h_range)

    def print_table(self, char_fun=None):
        """Print the field"""
        def standard_print(board, x, y):
            """Replace enum with char"""
            enum_translation = {self.States.empty: " ", self.States.hit: "X",
                                self.States.miss: "~", self.States.sunk: "#",
                                self.States.suspect: "v", self.States.intact: "O"}
            return enum_translation[board[Coord(x, y)]]
        if char_fun is None:
            char_fun = standard_print
        result = "  "
        cell_range = range(len(self.cells))
        result += "".join(["| {:<2}".format(x + 1) for x in cell_range])
        result += "\n--"
        result += "+---" * len(self.cells)
        result += "\n"
        for cell_y in range(len(self.cells[0])):
            result += "{0} ".format(to_alpha(cell_y))
            for cell_x in range(len(self.cells)):
                result += "|{:^3}".format(char_fun(self, cell_x, cell_y))
            result += "\n--"
            result += "+---" * len(self.cells)
            result += "\n"
        return result
