"""Contains the GroundsTest class"""
import unittest

from util import Size
from management.field import Field
import bot.marginbot
from bot import DefenderBot
import bot.randombot
import bot.grounds


class GroundsTest(unittest.TestCase):
    """Tests the bots in action"""

    def test_random(self) -> None:
        """Check if random and margin are having a game"""
        attacker = bot.marginbot.MarginBot(Field(Size(10, 10)))
        defender_field = Field(Size(10, 10))
        defender_ships = bot.randombot.place_ships_random(defender_field)
        defender = DefenderBot(defender_field, defender_ships)

        tick_count = 0
        while True:
            tick_count += 1
            self.assertLessEqual(tick_count, 100)
            next_shot = attacker.shoot()
            self.assertTrue(next_shot in attacker.enemy_field.size)
            self.assertTrue(next_shot in defender.own_field.size)
            state = defender.get_shot(next_shot)
            if state is None:
                break
            self.assertEqual(defender.own_field[next_shot], state)
            attacker.mark_hit(next_shot, state)
