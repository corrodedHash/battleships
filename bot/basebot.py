"""Contains BaseBot class, as well as its only attacking
and protecting variances"""

import logging
from typing import Optional, List

from management.field import Field
from management.ship import Ship
from util import Coord


class BaseBot:
    """Common interface for every attacking battleship AI"""

    def __init__(self, enemy_field: Field) -> None:
        self.enemy_field = enemy_field

    def shoot(self) -> Coord:
        """Get next shot from this AI"""
        raise NotImplementedError

    def mark_hit(self, coord: Coord, state: Field.States) -> None:
        """Mark a cell"""
        self.enemy_field[coord] = state


class DefenderBot:
    """AI receiving shots"""

    def __init__(self, own_field: Field, ships: List[Ship]) -> None:
        self.own_field = own_field
        self.ships = ships

    def get_shot(self, coord: Coord) -> Optional[Field.States]:
        """Shoot this AI"""
        if self.own_field[coord] == Field.States.empty:
            self.own_field[coord] = Field.States.miss
            return self.own_field[coord]
        if self.own_field[coord] == Field.States.hit:
            logging.warning("Hitting cell that was already shot at")
            return self.own_field[coord]
        if self.own_field[coord] == Field.States.sunk:
            logging.warning("Hitting cell that was already shot at")
            return self.own_field[coord]

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
