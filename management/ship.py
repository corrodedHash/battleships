"""Contains Ship class"""

import itertools
from util import Coord, Orientation, DIRORI_MAP, DIRTUPLE_MAP
from util.direction import clockwise, counter_clockwise
from typing import List, Generator, Iterator


class Ship:
    """Class to manage cellular ships"""

    def __init__(self) -> None:
        self.cells: List[Coord] = []

    def orientation(self) -> Orientation:
        """Return orientation given from the coordinates in cells"""
        if len(self.cells) < 2:
            return Orientation.unknown
        for direction, dirtuple in DIRTUPLE_MAP.items():
            if self.cells[0] + dirtuple in self.cells:
                return DIRORI_MAP[direction]
        raise RuntimeError

    def possible_additions(self) -> Generator[Coord, None, None]:
        """Return generator of cells the ship can expand
        without violatig the orientation"""
        if not self.cells:
            return None
        if len(self.cells) == 1:
            for _, dirtuple in DIRTUPLE_MAP.items():
                yield self.cells[0] + dirtuple
        else:
            possible_directions = [
                direction for direction,
                orientation in DIRORI_MAP.items() if orientation == self.orientation()]
            possible_direction_tuples = [DIRTUPLE_MAP[d]
                                         for d in possible_directions]
            for cell in self.cells:
                for dirtuple in possible_direction_tuples:
                    if cell + dirtuple not in self.cells:
                        yield cell + dirtuple

    def get_parallel_sur(self) -> Generator[Coord, None, None]:
        """Get list of all cells that are next to the ship
        in the orientation of the ship"""
        if len(self.cells) >= 2:
            possible_directions = [
                d for d, o in DIRORI_MAP.items() if o == self.orientation()]
            possible_directions = [clockwise(d) for d in possible_directions]
            possible_direction_tuples = [DIRTUPLE_MAP[d]
                                         for d in possible_directions]
            assert len(possible_direction_tuples) == 2
            for cell in self.cells:
                for dirtuple in possible_direction_tuples:
                    yield cell + dirtuple

        else:
            raise RuntimeError

    def get_front_end_sur(self) -> Generator[Coord, None, None]:
        """Get list of cells that are at the front and end of the ship"""
        if len(self.cells) >= 2:
            return self.possible_additions()
        else:
            raise RuntimeError

    def get_sur(self) -> Generator[Coord, None, None]:
        """Get all cells that surround this ship"""
        if len(self.cells) == 1:
            for x in self.possible_additions():
                yield x

        for x in self.get_front_end_sur():
            yield x
        for x in self.get_parallel_sur():
            yield x

    def append(self, coord: Coord) -> None:
        if not self.cells:
            self.cells.append(coord)
        elif len(self.cells) == 1:
            if coord not in self.get_sur():
                raise RuntimeError
            self.cells.append(coord)
        else:
            if coord not in self.get_front_end_sur():
                raise RuntimeError
            self.cells.append(coord)

    def __len__(self) -> int:
        return len(self.cells)

    def __iter__(self) -> Iterator[Coord]:
        return self.cells.__iter__()

    def __getitem__(self, key: int) -> Coord:
        if isinstance(key, int):
            return self.cells[key]
        else:
            raise TypeError

    def __setitem__(self, key: int, value: Coord) -> None:
        if isinstance(key, int):
            self.cells[key] = value
        else:
            raise TypeError
