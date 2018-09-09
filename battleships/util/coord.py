"""Contains Coord class"""
import re
from typing import Optional, Tuple

from .alphanum import to_alpha, from_alpha


class Coord:
    """Contains coordinates of a point on a discrete 2D plane
    and operations for those coordinates"""

    def __init__(self: 'Coord', cell_x: int = 0, cell_y: int = 0,
                 alphanum: Optional[str] = None) -> None:
        self.x = cell_x
        self.y = cell_y
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

    def __getitem__(self: 'Coord', key: int) -> int:
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        raise KeyError

    def __sub__(self: 'Coord', other: Tuple[int, int]) -> 'Coord':
        if isinstance(other, tuple):
            return Coord(self.x - other[0], self.y - other[1])
        raise RuntimeError

    def __add__(self: 'Coord', other: Tuple[int, int]) -> 'Coord':
        if isinstance(other, tuple):
            return Coord(self.x + other[0], self.y + other[1])
        raise RuntimeError

    def __eq__(self: 'Coord', other: 'Coord') -> bool:  # type: ignore
        return self.x == other.x and self.y == other.y

    def __str__(self: 'Coord') -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self: 'Coord') -> str:
        return to_alpha(self.y) + str(self.x + 1)
