import enum

class Orientation(enum.Enum):
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
