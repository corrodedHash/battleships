"""Contains HuntingBot class"""
import random
import itertools

from bot.basebot import BaseBotOffensive
from management.field import Field
from management.ship import Ship
from util import Coord
from management import shotfinder
from typing import Optional


class HuntingBotOffensive(BaseBotOffensive):
    """Base class that hunts ships if they are found"""

    def __init__(self, enemy_field: Field) -> None:
        BaseBotOffensive.__init__(self, enemy_field)
        self.open_hit: Optional[Ship] = None

    def shoot(self) -> Coord:
        """Get next cell to shoot at"""
        if self.open_hit is None:
            raise NotImplementedError

        shot_list = shotfinder.hunt_ship(self.enemy_field, self.open_hit[0])
        refined_shot_list = [shot[0]
                             for shot in shot_list if shot[1] == shot_list[0][1]]
        coord_tuple = random.sample(refined_shot_list, 1)[0]
        return Coord(coord_tuple.x, coord_tuple.y)

    def mark_hit(self, coord: Coord, state: Field.States) -> None:
        self.enemy_field[coord] = state
        if state == Field.States.hit:
            if self.open_hit is None:
                self.open_hit = Ship()
                self.open_hit.append(coord)
            else:
                assert coord in self.open_hit.possible_additions()
                self.open_hit.append(coord)
                for sur in self.open_hit.get_parallel_sur():
                    if sur in self.enemy_field.size:
                        if self.enemy_field[sur] == Field.States.empty:
                            self.enemy_field[sur] = Field.States.suspect
        elif state == Field.States.sunk:
            assert self.open_hit is not None
            assert coord in self.open_hit.possible_additions()
            self.open_hit.append(coord)
            par_sur = self.open_hit.get_parallel_sur()
            fe_sur = self.open_hit.get_front_end_sur()
            surroundings = itertools.chain(par_sur, fe_sur)
            for sur in surroundings:
                if sur in self.enemy_field.size:
                    if self.enemy_field[sur] == Field.States.empty:
                        self.enemy_field[sur] = Field.States.suspect
            self.enemy_field.shipcount[len(self.open_hit) - 1] -= 1
            assert self.enemy_field.shipcount[len(self.open_hit) - 1] >= 0
            self.open_hit = None
