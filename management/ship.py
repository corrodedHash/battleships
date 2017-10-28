"""Contains Ship class"""

import itertools
from util import Space


class Ship:
    """Class to manage cellular ships"""

    def __init__(self):
        self.cells = []

    def orientation(self):
        """Return orientation given from the coordinates in cells"""
        if len(self.cells) < 2:
            return Space.Orientation.unknown
        for direction, dirtuple in Space.tupleDirMap.items():
            if self.cells[0] + dirtuple in self.cells:
                return Space.dirOriMap[direction]
        raise RuntimeError

    def possible_additions(self):
        """Return generator of cells the ship can expand
        without violatig the orientation"""
        if not self.cells:
            return 0
        if len(self.cells) == 1:
            for _, dirtuple in Space.tupleDirMap.items():
                yield self.cells[0] + dirtuple
        else:
            possible_dir = Space.dirOriMap.items()
            possible_dir = [
                d for d, o in possible_dir if o == self.orientation()]
            possible_dir = [Space.tupleDirMap[d] for d in possible_dir]
            for cell in self.cells:
                for dirtuple in possible_dir:
                    if cell + dirtuple not in self.cells:
                        yield cell + dirtuple

    def get_parallel_sur(self):
        """Get list of all cells that are next to the ship
        in the orientation of the ship"""
        if len(self.cells) >= 2:
            possible_dir = Space.dirOriMap.items()
            possible_dir = [
                d for d, o in possible_dir if o == self.orientation()]
            possible_dir = [d.clockwise() for d in possible_dir]
            possible_dir = [Space.tupleDirMap[d] for d in possible_dir]
            assert len(possible_dir) == 2
            for cell in self.cells:
                for dirtuple in possible_dir:
                    yield cell + dirtuple

        else:
            raise RuntimeError

    def get_front_end_sur(self):
        """Get list of cells that are at the front and end of the ship"""
        if len(self.cells) >= 2:
            return self.possible_additions()
        else:
            raise RuntimeError

    def get_sur(self):
        """Get all cells that surround this ship"""
        return itertools.chain(self.get_front_end_sur(),
                               self.get_parallel_sur())

    def __len__(self):
        return len(self.cells)
