"""Contains CheckerBot class"""

from ..util import Coord

from ..management import shotfinder
from .huntingbot import HuntingBot


class CheckerBot(HuntingBot):
    """Shoots to the cell with the statistically highest chance
    of a ship being there, while only hitting every second cell"""

    def shoot(self) -> Coord:
        """Get next coordiate to shoot"""
        if self.open_hit is not None:
            return HuntingBot.shoot(self)

        shot_list = shotfinder.list_ship_probabilities(self.enemy_field)
        improved_shot_list = []
        for shot in shot_list:
            if shot[0].x % 2 == shot[0].y % 2:
                improved_shot_list.append(shot[0])

        if not improved_shot_list:
            coord_tuple = shot_list[0][0]
        else:
            coord_tuple = improved_shot_list[0]

        return Coord(coord_tuple[0], coord_tuple[1])
