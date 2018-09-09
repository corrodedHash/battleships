"""Contains orientation and utils"""
import enum

Orientation = enum.Enum('Orientation', 'unknown vertical horizontal both')

def change_orientation(orientation: Orientation) -> Orientation:
    """Inverts vertical and horizontal orientation, and unknown and both"""
    if orientation == Orientation.vertical:
        return Orientation.horizontal
    if orientation == Orientation.horizontal:
        return Orientation.vertical
    if orientation == Orientation.both:
        return Orientation.unknown
    if orientation == Orientation.unknown:
        return Orientation.both
    raise RuntimeError

def accumulate_orientation(
        orione: Orientation,
        oritwo: Orientation) -> Orientation:
    """Returns the sum of two orientations"""
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
