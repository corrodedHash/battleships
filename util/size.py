"""Contains Size class"""
from .coord import Coord


class Size:
    """Contains size of a 2D rectangular object"""

    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height

    def __contains__(self, other: Coord):
        if isinstance(other, Coord):
            return other.x >= 0 and other.y >= 0 and self.__gt__(other)
        else:
            raise TypeError

    def __gt__(self, other: Coord):
        if isinstance(other, Coord):
            assert other.x >= 0
            assert other.y >= 0
            return other.x < self.width and other.y < self.height
        else:
            raise TypeError

    def __leq__(self, other):
        return not self.__gt__(other)
