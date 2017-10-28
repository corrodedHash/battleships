"""Contains MarginBot class"""

import random

from util import Coord

from .huntingbot import HuntingBotOffensive


class MarginBotOffensive(HuntingBotOffensive):
    """Shoots to the cell with the statistically highest
    chance of a ship being there"""

    def shoot(self) -> Coord:
        """Get next coordiate to shoot"""
        if self.open_hit is not None:
            return HuntingBotOffensive.shoot(self)

        shot_list = self.finder.sort_margin()
        shot_list = [shot[0]
                     for shot in shot_list if shot[1] == shot_list[0][1]]
        coord = random.sample(shot_list, 1)[0]
        return coord
