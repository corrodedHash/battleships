"""Contains RandomBot class"""
import random

from util import Direction, DIRTUPLE_MAP
from management.field import Field
from management.ship import Ship
from util import Coord
import itertools

from . import basebot as basebot
from typing import List, Optional, Tuple


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

    def _create_ship(self,
                     position: Coord,
                     dir_tuple: Tuple[int,
                                      int],
                     shipsize: int) -> Optional[Ship]:
        try_ship = Ship()
        for _ in range(shipsize):
            if position not in self.own_field:
                return None
            if self.own_field[position] == Field.States.intact:
                return None
            try_ship.append(position)
            position = position + dir_tuple

        if not any(sur in self.own_field.size
                   and self.own_field[sur] == Field.States.intact
                   for sur in try_ship.get_sur()):
            return try_ship
        return None

    def _place_ships(self) -> None:
        def _place_ship(shipsize: int) -> None:
            shuffled_cells = list(self.own_field.__iter__())
            random.shuffle(shuffled_cells)
            shuffled_direction = list(Direction.__iter__())
            random.shuffle(shuffled_direction)
            for cell, direction in itertools.product(
                    shuffled_cells, shuffled_direction):
                try_ship = self._create_ship(
                    cell, DIRTUPLE_MAP[direction], shipsize)

                if not try_ship:
                    continue

                for shipcell in try_ship:
                    self.own_field[shipcell] = Field.States.intact
                self.ships.append(try_ship.cells)
                return

            raise RuntimeError

        scl = self.own_field.shipcount
        for shipsize, ship_count in zip(range(len(scl), 0, -1), scl[::-1]):
            for _ in range(ship_count):
                _place_ship(shipsize)
