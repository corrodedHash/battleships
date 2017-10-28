"""Contains ShotFinder class"""
import util
from . import field


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
                top = min(margin[util.Space.Direction.top], ship_size - 1)
                bottom = min(
                    margin[util.Space.Direction.bottom], ship_size - 1)
                left = min(margin[util.Space.Direction.left], ship_size - 1)
                right = min(margin[util.Space.Direction.right], ship_size - 1)
                possible_positions = max(0, left + right + 2 - ship_size)
                possible_positions += max(0, top + bottom + 2 - ship_size)
                total_pp += possible_positions * \
                    self.field.shipcount[ship_size - 1]
            result.append((cell, total_pp))
        return sorted(result, key=lambda x: x[1], reverse=True)

    def hunt_ship(self, cell: util.Coord):
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

        ship_orientation = util.Space.Orientation.unknown
        for direction in util.Space.Direction:
            dir_tuple = util.Space.tupleDirMap[direction]
            new_cell = cell + dir_tuple
            if new_cell in self.field.size:
                if self.field[new_cell] == field.Field.States.hit:
                    ship_orientation = ship_orientation + \
                        util.Space.dirOriMap[direction]

        result_list = []
        if ship_orientation == util.Space.Orientation.both:
            raise RuntimeError
        elif ship_orientation == util.Space.Orientation.unknown:
            margin = self.field.get_margins(cell)
            result_list.append(
                (cell + (0, -1), margin[util.Space.Direction.top]))
            result_list.append(
                (cell + (0, 1), margin[util.Space.Direction.bottom]))
            result_list.append(
                (cell + (-1, 0), margin[util.Space.Direction.left]))
            result_list.append(
                (cell + (1, 0), margin[util.Space.Direction.right]))
            result_list = [x for x in result_list if x[1] > 0]
        else:  # either horizontal or vertical
            directions = [key for key, value in util.Space.dirOriMap.items(
            ) if value == ship_orientation]
            for direction in directions:
                dir_tuple = util.Space.tupleDirMap[direction]
                ship_end = find_end(dir_tuple)
                ship_margin = self.field.get_margins(ship_end)[direction]
                if ship_margin > 0:
                    result_list.append((ship_end + dir_tuple, ship_margin))

        result_list = sorted(result_list, key=lambda x: x[1], reverse=True)
        return result_list
