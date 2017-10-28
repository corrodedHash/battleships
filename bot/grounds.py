"""Contains Grounds class"""
from util import Coord


class OneWayGround:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.tick_count = 0

    def tick(self):
        self.tick_count += 1
        next_shot = self.attacker.shoot()
        state = self.defender.get_shot(next_shot)
        if state == None:
            return True
        self.attacker.mark_hit(next_shot, state)
        return False

class Grounds:
    """Interface for two battleship AIs to fight"""

    def __init__(self):
        self.player1 = None
        self.player2 = None
