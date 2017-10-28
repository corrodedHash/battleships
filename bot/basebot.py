"""Contains BaseBot class, as well as its only attacking and protecting variances"""

import logging

from management.field import Field
from util import Coord


class BaseBotOffensive:
    """Common interface for every attacking battleship AI"""

    def __init__(self, enemy_field: Field = None):
        self.enemy_field = enemy_field

    def shoot(self) -> Coord:
        """Get next shot from this AI"""
        raise NotImplementedError

    def mark_hit(self, coord, state):
        """Mark a cell"""
        self.enemy_field[coord] = state


class BaseBotDefensive:
    """Common interface for every receiving battleship AI"""

    def __init__(self, own_field: Field = None):
        self.own_field = own_field

    def get_shot(self, coord: Coord) -> Field.States:
        """Shoot this AI"""
        if self.own_field[coord] == Field.States.intact:
            self.own_field[coord] = Field.States.hit
        elif self.own_field[coord] == Field.States.empty:
            self.own_field[coord] = Field.States.miss
        else:
            logging.warning("Hitting cell that was already shot at")
        return self.own_field[coord]


class BaseBot(BaseBotOffensive, BaseBotDefensive):
    """Common interface for battleship AI that protec but also attac"""

    def __init__(self, own_field: Field = None, enemy_field: Field = None):
        BaseBotOffensive.__init__(self, enemy_field)
        BaseBotDefensive.__init__(self, own_field)

    def shoot(self) -> Coord:
        """Get next shot from this AI"""
        raise NotImplementedError
