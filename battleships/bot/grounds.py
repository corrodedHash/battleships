"""Contains Grounds class"""
from .basebot import BaseBot, DefenderBot


class OneWayGround:
    """Only has one atacker and one defender"""

    def __init__(self, attacker: BaseBot,
                 defender: DefenderBot) -> None:
        self.attacker = attacker
        self.defender = defender
        self.tick_count = 0

    def tick(self) -> bool:
        """Make the attacker shoot once"""

        self.tick_count += 1
        next_shot = self.attacker.shoot()
        state = self.defender.get_shot(next_shot)
        if state is None:
            return True
        self.attacker.mark_hit(next_shot, state)
        return False


class Grounds:
    """Interface for two battleship AIs to fight"""

    def __init__(self) -> None:
        self.player1 = None
        self.player2 = None
