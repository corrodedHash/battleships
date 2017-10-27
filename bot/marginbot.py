"""Contains MarginBot class"""

from .basebot import BaseOffensiveBot
from management.shotfinder import ShotFinder

class MarginBotOffensive(BaseBotOffensive):
    def __init__(self, enemy_field):
        BaseBot.__init__(self, enemy_field)
        self.finder = ShotFinder(self.enemy_field)

    def shoot(self) -> Coord:
        shot_list = self.finder.sort_margin()
        shot_list = [shot for shot in shot_list if shot[1] == shot_list[-1][1]]
        return random.sample(shot_list, 1)[0]



