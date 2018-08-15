"""Contains RandomBot class"""
import random

from util import Direction, DIRTUPLE_MAP
from management.field import Field
from management.ship import Ship
from util import Coord
import itertools 

from . import basebot as basebot
from typing import List, Optional


class RandomBotDefensive(basebot.BaseBotDefensive):
    """Places ships randomly in field"""

    def __init__(self, own_field: Field) -> None:
        basebot.BaseBotDefensive.__init__(self, own_field)
        self.ships: List[List[Coord]] = []

        self._place_ships()

    def get_shot(self, coord: Coord) -> Optional[Field.States]:
        if self.own_field[coord] != Field.States.intact:
            return basebot.BaseBotDefensive.get_shot(self, coord)

        for ship in self.ships:
            if coord not in ship:
                continue
            ship.remove(coord)
            if not ship:
                self.own_field[coord] = Field.States.sunk
                self.ships = [s for s in self.ships if s]
                if not self.ships:
                    return None
            else:
                self.own_field[coord] = Field.States.hit
            return self.own_field[coord]
        raise RuntimeError

    def _place_ships(self) -> None:
        def _place_ship(shipsize: int) -> None:
            shuffled_cells = list(self.own_field.__iter__())
            random.shuffle(shuffled_cells)
            shuffled_direction = list(Direction.__iter__())
            random.shuffle(shuffled_direction)
            for cell, direction in itertool.combinations(shuffled_cells, shuffled_direction):
                try_ship = Ship()
                dir_tuple = DIRTUPLE_MAP[direction]
                cur_cell = cell
                for _ in range(shipsize):
                    if cur_cell not in self.own_field:
                        break
                    if self.own_field[cur_cell] == Field.States.intact:
                        break
                    try_ship.append(cur_cell)
                    cur_cell = cur_cell + dir_tuple
                else:
                    possur = (s for s in try_ship.get_sur()
                              if s in self.own_field.size)
                    for sur in possur:
                        if self.own_field[sur] == Field.States.intact:
                            break
                    else:
                        for shipcell in try_ship:
                            self.own_field[shipcell] = Field.States.intact
                        self.ships.append(try_ship.cells)
                        return
            raise RuntimeError

        scl = self.own_field.shipcount
        for shipsize, ship_count in zip(range(len(scl), 0, -1), scl[::-1]):
            for _ in range(ship_count):
                _place_ship(shipsize)
