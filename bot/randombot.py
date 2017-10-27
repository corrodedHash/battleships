"""Contains RandomBot class"""
import random

from util import Space
from management.field import Field

from . import basebot as basebot


class RandomBotDefensive(basebot.BaseBotDefensive):
    """Places ships randomly in field"""
    def __init__(self, own_field):
        basebot.BaseBotDefensive.__init__(self, own_field)
        self._place_ships()

    def _place_ships(self):
        def _place_ship(shipsize):
            def _check_line(direction, cur_cell):
                dir_cw = Space.tupleDirMap[direction.clockwise()]
                dir_ccw = Space.tupleDirMap[direction.counter_clockwise()]
                if cur_cell not in self.own_field.size:
                    return False
                if self.own_field[cur_cell] != c_empt:
                    return False
                if cur_cell + dir_cw in self.own_field.size:
                    if self.own_field[cur_cell + dir_cw] != c_empt:
                        return False
                if cur_cell + dir_ccw in self.own_field.size:
                    if self.own_field[cur_cell + dir_ccw] != c_empt:
                        return False
                return True

            shuffled_direction = list(Space.Direction.__iter__())
            random.shuffle(shuffled_direction)
            c_empt = Field.States.empty
            for direction in shuffled_direction:
                shuffled_cells = list(self.own_field.__iter__())
                dir_tuple = Space.tupleDirMap[direction]
                dir_bw = Space.tupleDirMap[direction.clockwise().clockwise()]
                random.shuffle(shuffled_cells)
                for cell in shuffled_cells:
                    cur_cell = cell
                    for _ in range(shipsize):
                        if not _check_line(direction, cur_cell):
                            break
                        cur_cell = cur_cell + dir_tuple
                    else:
                        if cell + dir_bw in self.own_field.size:
                            if self.own_field[cell + dir_bw] != c_empt:
                                continue
                        if cur_cell in self.own_field.size:
                            if self.own_field[cur_cell] != c_empt:
                                continue
                        cur_cell = cell
                        for _ in range(shipsize):
                            self.own_field[cur_cell] = Field.States.intact
                            cur_cell = cur_cell + dir_tuple
                        return
            raise RuntimeError

        scl = self.own_field.shipcount
        for shipsize, ship_count in zip(range(len(scl), 0, -1), scl[::-1]):
            for _ in range(ship_count):
                _place_ship(shipsize)
