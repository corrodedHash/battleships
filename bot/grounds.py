"""Contains Grounds class"""
from util import Coord


class OneWayGround:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender

    def tick(self):
        next_shot = self.attacker.shoot()
        print(next_shot)
        state = self.defender.get_shot(next_shot)
        self.attacker.mark_hit(next_shot, state)

class Grounds:
    """Interface for two battleship AIs to fight"""

    def __init__(self):
        self.player1 = None
        self.player2 = None
