"""Contains RandomBot class"""
import random

from typing import List, Optional
import itertools

from ..management.field import Field
from ..management.ship import create_ship, Ship
from ..util import Coord, Direction, DIRTUPLE_MAP

def place_ships_random(battlefield: Field) -> List[Ship]:
    def _place_ship(shipsize: int) -> Ship:
        shuffled_cells = list(battlefield.__iter__())
        random.shuffle(shuffled_cells)
        shuffled_direction = list(Direction.__iter__())
        random.shuffle(shuffled_direction)
        for cell, direction in itertools.product(
                shuffled_cells, shuffled_direction):
            try_ship = create_ship(
                battlefield, cell, DIRTUPLE_MAP[direction], shipsize)

            if not try_ship:
                continue

            for shipcell in try_ship:
                battlefield[shipcell] = Field.States.intact

            return try_ship

        raise RuntimeError

    scl = battlefield.shipcount
    ships = []
    for shipsize, ship_count in zip(range(len(scl), 0, -1), scl[::-1]):
        for _ in range(ship_count):
            ships.append(_place_ship(shipsize))
    return ships
