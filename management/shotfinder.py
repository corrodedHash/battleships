import util
from . import field


class ShotFinder:
    def __init__(self, search_field):
        self.field = search_field
        self.shipcount = [0, 4, 3, 2, 1]

    def sort_margin(self):
        result = list()
        for cell in self.field:
            if self.field[cell] != field.Field.States.empty:
                continue
            margin = self.field.getMargins(cell)
            total_pp = 0
            for ship_size in range(1, len(self.shipcount) + 1):
                top = min(margin[util.Space.Direction.top], ship_size - 1)
                bottom = min(
                    margin[util.Space.Direction.bottom], ship_size - 1)
                left = min(margin[util.Space.Direction.left], ship_size - 1)
                right = min(margin[util.Space.Direction.right], ship_size - 1)
                possible_positions = max(0, left + right + 2 - ship_size)
                possible_positions += max(0, top + bottom + 2 - ship_size)
                total_pp += possible_positions * self.shipcount[ship_size - 1]
            result.append((cell, total_pp))
        return sorted(result, key=lambda x: x[1])

    def hunt_ship(self, cell: util.Coord):
        def find_end(dirTuple):
            new_point = cell
            while new_point + dirTuple in self.field.size:
                if self.field[new_point + dirTuple] != field.Field.States.hit:
                    return new_point
                new_point = new_point + dirTuple
            return new_point

        if self.field[cell] != field.Field.States.hit:
            raise RuntimeError

        ship_orientation = util.Space.Orientation.unknown
        for direction in util.Space.Direction:
            dirTuple = util.Space.tupleDirMap[direction]
            new_cell = cell + dirTuple
            if new_cell in self.field.size:
                if self.field[new_cell] == field.Field.States.hit:
                    ship_orientation = ship_orientation + \
                        util.Space.dirOriMap[direction]

        result_list = []
        if ship_orientation == util.Space.Orientation.both:
            raise RuntimeError
        elif ship_orientation == util.Space.Orientation.unknown:
            margin = self.field.getMargins(cell)
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
                dirTuple = util.Space.tupleDirMap[direction]
                ship_end = find_end(dirTuple)
                ship_margin = self.field.getMargins(ship_end)[direction]
                if margin > 0:
                    result_list.append((ship_end + dirTuple, ship_margin))

        result_list = sorted(result_list, key=lambda x: x[1])
        return result_list
