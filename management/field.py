"""Contains Field class"""
import copy
import enum
from enum import Enum
import logging
from typing import Optional, List, Dict, Generator, Callable, Iterator

from util import Size, Coord, Direction, DIRTUPLE_MAP


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

    def __init__(self, size: Size,
                 shipcount: Optional[List[int]] = None) -> None:
        assert size.width > 0
        assert size.height > 0
        if shipcount is None:
            shipcount = [0, 4, 3, 2, 1]
        self.size = size
        self.shipcount = shipcount
        self.cells = Field.generate_field(self.size)

    @staticmethod
    def generate_field(size: Size)-> List[List[States]]:
        """Generates a 2D list to access all cells of the field"""
        result = [[Field.States.empty for _ in range(
            size.height)] for _ in range(size.width)]
        return result

    def get_margins(self, cell: Coord) -> Dict[Direction, int]:
        """Returns dictionary keyed with directions.
        Contains the amount of unknown spaces from the cell to the next
        known cell."""
        result = dict()
        for direction in Direction:
            dir_tuple = DIRTUPLE_MAP[direction]
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

    def __getitem__(self, key: Coord) -> States:
        if isinstance(key, Coord):
            return self.cells[key.x][key.y]
        else:
            logging.error(type(key))
            raise TypeError

    def __setitem__(self, key: Coord, value: States) -> None:
        if isinstance(key, Coord):
            self.cells[key.x][key.y] = value
        else:
            raise TypeError

    def __iter__(self)-> Iterator[Coord]:
        """Returns a generator to access all cells of the field"""
        w_range = range(self.size.width)
        h_range = range(self.size.height)
        return (Coord(x, y) for x in w_range for y in h_range)

    def __contains__(self, other: Coord) -> bool:
        if isinstance(other, Coord):
            return other.x >= 0 and other.y >= 0 and self.size > other
        else:
            raise TypeError
