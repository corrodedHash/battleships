"""Contains ShotFinder class"""
from util import Space, Coord
from . import field


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

    def __len__(self):
        return len(self.cells)


class ShotFinder:
    """Utilities to compute the next shot to make"""

    def __init__(self, search_field):
        self.field = search_field

    def sort_margin(self):
        """Returns a list of coords
        Sorted by the probabilities that a ship is in that coord"""
        result = list()
        for cell in self.field:
            if self.field[cell] != field.Field.States.empty:
                continue
            margin = self.field.get_margins(cell)
            total_pp = 0
            for ship_size in range(1, len(self.field.shipcount) + 1):
                top = min(margin[Space.Direction.top], ship_size - 1)
                bottom = min(
                    margin[Space.Direction.bottom], ship_size - 1)
                left = min(margin[Space.Direction.left], ship_size - 1)
                right = min(margin[Space.Direction.right], ship_size - 1)
                possible_positions = max(0, left + right + 2 - ship_size)
                possible_positions += max(0, top + bottom + 2 - ship_size)
                total_pp += possible_positions * \
                    self.field.shipcount[ship_size - 1]
            result.append((cell, total_pp))
        return sorted(result, key=lambda x: x[1], reverse=True)

    def hunt_ship(self, cell: Coord):
        """Return possible next coords for the ship on the given coord"""
        def find_end(dir_tuple):
            """Move in the given direction until hitting a un-hit cell"""
            new_point = cell
            while new_point + dir_tuple in self.field.size:
                if self.field[new_point + dir_tuple] != field.Field.States.hit:
                    return new_point
                new_point = new_point + dir_tuple
            return new_point

        if self.field[cell] != field.Field.States.hit:
            raise RuntimeError

        ship_orientation = Space.Orientation.unknown
        for direction in Space.Direction:
            dir_tuple = Space.tupleDirMap[direction]
            new_cell = cell + dir_tuple
            if new_cell in self.field.size:
                if self.field[new_cell] == field.Field.States.hit:
                    ship_orientation = ship_orientation + \
                        Space.dirOriMap[direction]

        result_list = []
        if ship_orientation == Space.Orientation.both:
            raise RuntimeError
        elif ship_orientation == Space.Orientation.unknown:
            margin = self.field.get_margins(cell)
            result_list.append(
                (cell + (0, -1), margin[Space.Direction.top]))
            result_list.append(
                (cell + (0, 1), margin[Space.Direction.bottom]))
            result_list.append(
                (cell + (-1, 0), margin[Space.Direction.left]))
            result_list.append(
                (cell + (1, 0), margin[Space.Direction.right]))
            result_list = [x for x in result_list if x[1] > 0]
        else:  # either horizontal or vertical
            directions = [key for key, value in Space.dirOriMap.items(
            ) if value == ship_orientation]
            for direction in directions:
                dir_tuple = Space.tupleDirMap[direction]
                ship_end = find_end(dir_tuple)
                ship_margin = self.field.get_margins(ship_end)[direction]
                if ship_margin > 0:
                    result_list.append((ship_end + dir_tuple, ship_margin))

        result_list = sorted(result_list, key=lambda x: x[1], reverse=True)
        return result_list
