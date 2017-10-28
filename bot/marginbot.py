"""Contains MarginBot class"""

import random
import itertools

from management.shotfinder import ShotFinder, Ship
from management.field import Field
from util import Coord

from .huntingbot import HuntingBotOffensive


class MarginBotOffensive(HuntingBotOffensive):
    """Shoots to the cell with the statistically highest chance of a ship being there"""
    def __init__(self, enemy_field):
        HuntingBotOffensive.__init__(self, enemy_field)
        self.finder = ShotFinder(self.enemy_field)

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

