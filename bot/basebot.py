"""Contains Class BaseBot"""

import logging

from management.field import Field
from util import Coord


class BaseBot:
    """Common interface for every battleship AI"""

    def __init__(self, own_field: Field = None, enemy_field: Field = None):
        self.own_field = own_field
        self.enemy_field = enemy_field
        self.shipcount = None

    def get_shot(self, coord: Coord) -> Field.States:
        """Shoot this AI"""
        if self.own_field[coord] == Field.States.intact:
            self.own_field[coord] = Field.States.hit
        elif self.own_field[coord] == Field.States.empty:
            self.own_field[coord] = Field.States.miss
        else:
            logging.warning("Hitting cell that was already shot at")
        return self.own_field[coord]

    def shoot(self) -> Coord:
        """Get next shot from this AI"""
        pass

    def _place_ships(self):
        pass
