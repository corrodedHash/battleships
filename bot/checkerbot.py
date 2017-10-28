"""Contains CheckerBot class"""

import random

from management.shotfinder import ShotFinder
from management.field import Field
from util import Coord

from .huntingbot import HuntingBotOffensive


class CheckerBotOffensive(HuntingBotOffensive):
    """Shoots to the cell with the statistically highest chance of a ship being there, while only hitting every second cell"""

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
            improved_shot_list = [shot[0] for shot in shot_list if shot[0].x % 2 == shot[0].y % 2]
            if not improved_shot_list:
                coord_tuple = shot_list[0]
            else:
                coord_tuple = improved_shot_list[0]
        return Coord(coord_tuple[0], coord_tuple[1])
