"""Contains utility classes and functions"""
# pylint: disable=C0414
# Aliasing to calm down mypy
from .coord import Coord as Coord
from .size import Size as Size
from .alphanum import to_alpha as to_alpha, from_alpha as from_alpha
from .direction import (
    Direction as Direction,
    clockwise as clockwise,
    counter_clockwise as counter_clockwise,
)
from .orientation import (
    Orientation as Orientation,
    change_orientation as change_orientation,
    accumulate_orientation as accumulate_orientation,
)
from .dirori import DIRTUPLE_MAP as DIRTUPLE_MAP, DIRORI_MAP as DIRORI_MAP
