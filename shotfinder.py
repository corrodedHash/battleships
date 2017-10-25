import util
import field

class ShotFinder:
    def __init__(self, search_field):
        self.field = search_field
        self.shipcount = [0, 4, 3, 2, 1]

    def sort_margin(self):
        result = list()
        for cell in self.field.allCells():
            if self.field[cell] != field.Field.States.empty:
                continue
            margin = self.field.getMargins(cell)
            total_pp = 0
            for ship_size in range(1, len(self.shipcount) + 1):
                top = min(margin.top, ship_size - 1)
                bottom = min(margin.bottom, ship_size - 1)
                left = min(margin.left, ship_size - 1)
                right = min(margin.right, ship_size - 1)
                possible_positions = max(0, left + right + 2 - ship_size)
                possible_positions += max(0, top + bottom + 2 - ship_size)
                total_pp += possible_positions * self.shipcount[ship_size - 1]
            result.append((cell, total_pp))
        return sorted(result, key=lambda x: x[1])

    def hunt_ship(self, cell: util.Coord):
        def find_end(direction):
            new_point = cell
            while new_point + direction in self.field.size:
                if self.field[new_point + direction] != field.Field.States.hit:
                    return new_point
                new_point = new_point + direction
            return new_point

        assert self.field[cell] == field.Field.States.hit 

        vertical_ship = [0]
        horizontal_ship = [0]
        vert_dir = [(0, -1), (0, 1)]
        hor_dir = [(-1, 0), (1, 0)]
        for orientation, directions in ([vertical_ship, vert_dir], [horizontal_ship, hor_dir]):
            for direction in directions: 
                new_cell = cell + direction
                if new_cell in self.field.size:
                    if self.field[new_cell] == field.Field.States.hit:
                        orientation[0] = 1
                        break

        result_list = []
        vertical_ship = vertical_ship[0]
        horizontal_ship = horizontal_ship[0]
        if vertical_ship is 1 and horizontal_ship is 1:
            raise RuntimeError
        elif vertical_ship is 1:
            ship_end_top = find_end((0, -1))
            margin_top = self.field.getMargin(ship_end_top).top
            if margin_top > 0:
                result_list.append((ship_end_top, margin_top))

            ship_end_bottom = find_end((0, 1))
            margin_bottom = self.field.getMargin(ship_end_bottom).bottom
            if margin_bottom > 0:
                result_list.append((ship_end_bottom, margin_bottom))


        elif horizontal_ship is 1:
            ship_end_left = find_end((-1, 0))
            margin_left = self.field.getMargin(ship_end_left).left
            if margin_left > 0:
                result_list.append((ship_end_left, margin_left))

            ship_end_right = find_end((1, 0))
            margin_right = self.field.getMargin(ship_end_right).right
            if margin_right > 0:
                result_list.append((ship_end_right, margin_right))

        else: # Both 0
            margin = self.field.getMargins(cell)
            result_list.append((cell + (0, -1), margin.top))
            result_list.append((cell + (0, 1), margin.bottom))
            result_list.append((cell + (-1, 0), margin.left))
            result_list.append((cell + (1, 0), margin.right))
            result_list = [x for x in result_list if x[1] > 0]

        result_list = sorted(result_list, key=lambda x: x[1])
        return result_list
