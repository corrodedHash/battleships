import enum

class Direction(enum.Enum):
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
