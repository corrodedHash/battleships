"""Contains MarginBot class"""

import random

from management.shotfinder import ShotFinder
from util import Coord

from .basebot import BaseBotOffensive


class MarginBotOffensive(BaseBotOffensive):
    """Shoots to the cell with the statistically highest chance of a ship being there"""

    def __init__(self, enemy_field):
        BaseBotOffensive.__init__(self, enemy_field)
        self.finder = ShotFinder(self.enemy_field)

    def shoot(self) -> Coord:
        """Get next coordiate to shoot"""
        shot_list = self.finder.sort_margin()
        shot_list = [shot for shot in shot_list if shot[1] == shot_list[-1][1]]
        return random.sample(shot_list, 1)[0]
