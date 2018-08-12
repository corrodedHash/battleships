import enum

Orientation = enum.Enum('Orientation', 'unknown vertical horizontal both')


def accumulate_orientation(
        orione: Orientation,
        oritwo: Orientation) -> Orientation:
    if orione == oritwo:
        return orione

    if orione == orione.vertical and oritwo == orione.horizontal:
        return Orientation.both

    if orione == orione.horizontal and oritwo == orione.vertical:
        return Orientation.both

    if orione == orione.both or oritwo == orione.both:
        return Orientation.both

    if orione == orione.unknown:
        return oritwo

    if oritwo == orione.unknown:
        return orione

    raise RuntimeError
