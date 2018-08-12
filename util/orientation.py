import enum

Orientation = enum.Enum('Orientation', 'unknown vertical horizontal both')


def accumulate_orientation(
        orione: Orientation,
        oritwo: Orientation) -> Orientation:
    if orione == oritwo:
        return orione

    if orione == Orientation.vertical and oritwo == Orientation.horizontal:
        return Orientation.both

    if orione == Orientation.horizontal and oritwo == Orientation.vertical:
        return Orientation.both

    if orione == Orientation.both or oritwo == Orientation.both:
        return Orientation.both

    if orione == Orientation.unknown:
        return oritwo

    if oritwo == Orientation.unknown:
        return orione

    raise RuntimeError
