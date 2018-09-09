"""Contains MarginBot class"""

import random
from util import Coord

from management import shotfinder
from .huntingbot import HuntingBot


class MarginBot(HuntingBot):
    """Shoots to the cell with the statistically highest
    chance of a ship being there"""

    def shoot(self) -> Coord:
        """Get next coordiate to shoot"""
        if self.open_hit is not None:
            return HuntingBot.shoot(self)

        shot_list = shotfinder.list_ship_probabilities(self.enemy_field)
        refined_shot_list = [shot[0]
                             for shot in shot_list if shot[1] == shot_list[0][1]]
        coord = random.sample(refined_shot_list, 1)[0]
        return coord
