import enum

Direction = enum.Enum('Direction', 'top bottom left right')


def counter_clockwise(direction: Direction) -> Direction:
    """Rotate the current direction by 90 degrees ccw"""
    order = [Direction.top, Direction.right, Direction.bottom, Direction.left]
    return order[(order.index(direction) - 1) % len(order)]


def clockwise(direction: Direction) -> Direction:
    """Rotate the current direction by 90 degrees cw"""
    order = [Direction.top, Direction.right, Direction.bottom, Direction.left]
    return order[(order.index(direction) + 1) % len(order)]
