from .coord import Coord


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
