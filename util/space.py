"""Contains Space class"""
import enum
from enum import Enum


class Space:
    """Specifies distances of a point in 4 directions"""
    class Direction(Enum):
        """Possible directions in a checkered field"""
        top = enum.auto()
        bottom = enum.auto()
        left = enum.auto()
        right = enum.auto()

        def counter_clockwise(self):
            """Rotate the current direction by 90 degrees ccw"""
            order = [self.top, self.right, self.bottom, self.left]
            return order[(order.index(self) - 1) % len(order)]

        def clockwise(self):
            """Rotate the current direction by 90 degrees cw"""
            order = [self.top, self.right, self.bottom, self.left]
            return order[(order.index(self) + 1) % len(order)]

    class Orientation(Enum):
        """Possible 90 degree orientations"""
        unknown = enum.auto()
        vertical = enum.auto()
        horizontal = enum.auto()
        both = enum.auto()

        def __add__(self, other):
            if self == other:
                return self

            if self == self.vertical and other == self.horizontal:
                return self.both
            if self == self.horizontal and other == self.vertical:
                return self.both

            if self == self.both or other == self.both:
                return self.both
            if self == self.unknown:
                return other
            if other == self.unknown:
                return self

            raise RuntimeError

    tupleDirMap = {Direction.top: (0, -1),
                   Direction.bottom: (0, 1),
                   Direction.left: (-1, 0),
                   Direction.right: (1, 0)}

    dirOriMap = {Direction.top: Orientation.vertical,
                 Direction.bottom: Orientation.vertical,
                 Direction.left: Orientation.horizontal,
                 Direction.right: Orientation.horizontal}

    def __init__(self):
        self.values = dict()

    def __getitem__(self, key: Direction):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __repr__(self):
        return str(self.values)
