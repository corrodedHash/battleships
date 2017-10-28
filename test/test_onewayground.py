"""Contains the GroundsTest class"""
import unittest

from util import Size, Coord
from management.field import Field
import bot.marginbot
import bot.randombot
import bot.grounds


class GroundsTest(unittest.TestCase):
    """Tests the bots in action"""

    def test_random(self):
        """Check if random and margin are having a game"""
        attacker = bot.marginbot.MarginBotOffensive(Field(Size(10, 10)))
        defender = bot.randombot.RandomBotDefensive(Field(Size(10, 10)))

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
