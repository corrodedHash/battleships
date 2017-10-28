"""Contains MarginBot class"""

import random
import itertools

from management.shotfinder import ShotFinder, Ship
from management.field import Field
from util import Coord

from .basebot import BaseBotOffensive


class MarginBotOffensive(BaseBotOffensive):
    """Shoots to the cell with the statistically highest chance of a ship being there"""

    def __init__(self, enemy_field):
        BaseBotOffensive.__init__(self, enemy_field)
        self.finder = ShotFinder(self.enemy_field)
        self.open_hit = None 

    def shoot(self) -> Coord:
        """Get next coordiate to shoot"""
        if self.open_hit is not None:
            shot_list = self.finder.hunt_ship(self.open_hit.cells[0])
            shot_list = [shot[0] for shot in shot_list if shot[1] == shot_list[0][1]]
            coord_tuple = random.sample(shot_list, 1)[0]
        else:
            shot_list = self.finder.sort_margin()
            shot_list = [shot[0] for shot in shot_list if shot[1] == shot_list[0][1]]
            coord_tuple = random.sample(shot_list, 1)[0]
        return Coord(coord_tuple[0], coord_tuple[1])

    def mark_hit(self, coord, state):
        self.enemy_field[coord] = state
        if state == Field.States.hit:
            if self.open_hit is None:
                self.open_hit = Ship()
                self.open_hit.cells.append(coord)
            else:
                assert coord in self.open_hit.possible_additions()
                self.open_hit.cells.append(coord)
                for sur in self.open_hit.get_parallel_sur():
                    if sur in self.enemy_field.size:
                        if self.enemy_field[sur] == Field.States.empty:
                            self.enemy_field[sur] = Field.States.suspect
        if state == Field.States.sunk:
            assert coord in self.open_hit.possible_additions()
            self.open_hit.cells.append(coord)
            par_sur = self.open_hit.get_parallel_sur()
            fe_sur = self.open_hit.get_front_end_sur()
            surroundings = itertools.chain(par_sur, fe_sur)
            for sur in surroundings:
                if sur in self.enemy_field.size:
                    if self.enemy_field[sur] == Field.States.empty:
                        self.enemy_field[sur] = Field.States.suspect
            self.open_hit = None
