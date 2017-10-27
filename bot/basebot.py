"""Contains Class BaseBot"""

import logging

from management.field import Field
from util import Coord


class BaseBot:
    """Common interface for every battleship AI"""

    def __init__(self):
        self.own_field = None
        self.enemy_field = None
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
