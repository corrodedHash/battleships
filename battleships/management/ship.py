"""Contains Ship class"""
from typing import Iterator, Tuple, Optional

from ..util import Coord, Orientation, change_orientation, DIRORI_MAP, DIRTUPLE_MAP
from ..management.field import Field


class Ship(list[Coord]):
    """Class to manage cellular ships"""

    def orientation(self) -> Orientation:
        """Return orientation given from the coordinates in cells"""
        if len(self) < 2:
            return Orientation.unknown

        for direction, dirtuple in DIRTUPLE_MAP.items():
            if self[0] + dirtuple in self:
                return DIRORI_MAP[direction]

        raise RuntimeError

    def orientated_surrounding_cells(
            self,
            target_orientation: Orientation)-> Iterator[Coord]:
        """Returns cells next to the ship of the given orientation"""
        possible_directions = (
            direction for direction,
            orientation in DIRORI_MAP.items()
            if orientation == target_orientation)

        possible_direction_tuples = [DIRTUPLE_MAP[d]
                                     for d in possible_directions]

        possible_cells = (
            cell + dirtuple
            for cell in self
            for dirtuple in possible_direction_tuples)

        possible_new_cells = (
            cell for cell in possible_cells
            if cell not in self)

        return possible_new_cells

    def get_parallel_sur(self) -> Iterator[Coord]:
        """Get list of all cells that are next to the ship
        in the orientation of the ship"""
        if len(self) < 2:
            raise RuntimeError

        return self.orientated_surrounding_cells(
            change_orientation(
                self.orientation()))

    def get_front_end_sur(self) -> Iterator[Coord]:
        """Get list of cells that are at the front and end of the ship"""
        if len(self) < 2:
            raise RuntimeError

        return self.orientated_surrounding_cells(self.orientation())

    def possible_additions(self) -> Iterator[Coord]:
        """Return generator of cells the ship can expand
        without violatig the orientation"""
        if not self:
            return

        if len(self) == 1:
            for _, dirtuple in DIRTUPLE_MAP.items():
                yield self[0] + dirtuple
            return

        yield from self.get_front_end_sur()

    def get_sur(self) -> Iterator[Coord]:
        """Get all cells that surround this ship"""
        if len(self) == 1:
            yield from self.possible_additions()
            return

        yield from self.get_front_end_sur()
        yield from self.get_parallel_sur()

    def append(self, coord: Coord) -> None:
        """Append cell to ship"""
        if not self:
            list.append(self, coord)
        elif len(self) == 1:
            if coord not in self.get_sur():
                raise RuntimeError
            list.append(self, coord)
        else:
            if coord not in self.get_front_end_sur():
                raise RuntimeError
            list.append(self, coord)


def create_ship(battlefield: Field,
                position: Coord,
                dir_tuple: Tuple[int,
                                 int],
                shipsize: int) -> Optional[Ship]:
    """Create ship from a position, size and a direction"""
    try_ship = Ship()
    for _ in range(shipsize):
        if position not in battlefield:
            return None
        if battlefield[position] == Field.States.intact:
            return None
        try_ship.append(position)
        position = position + dir_tuple

    if not any(sur in battlefield.size
               and battlefield[sur] == Field.States.intact
               for sur in try_ship.get_sur()):
        return try_ship
    return None
