"""Contains the GroundsTest class"""
import unittest

from .context import battleships
from battleships.util import Size
from battleships.management.field import Field
import battleships.bot.marginbot
import battleships.bot.checkerbot
from battleships.bot import DefenderBot
import battleships.bot.randombot
import battleships.bot.grounds


class GroundsTest(unittest.TestCase):
    """Tests the bots in action"""

    def test_onewayground_random(self) -> None:
        """Check if random and margin are having a game"""
        attacker = battleships.bot.checkerbot.CheckerBot(Field(Size(10, 10)))
        defender_field = Field(Size(10, 10))
        defender_ships = battleships.bot.randombot.place_ships_random(defender_field)
        defender = DefenderBot(defender_field, defender_ships)
        ground = battleships.bot.grounds.OneWayGround(attacker, defender)

        for i in range(100):
            if ground.tick():
                return

        self.fail("Bot didn't win after 100 shots")


    def test_onewayground(self) -> None:
        """Check if random and margin are having a game"""
        attacker = battleships.bot.marginbot.MarginBot(Field(Size(10, 10)))
        defender_field = Field(Size(10, 10))
        defender_ships = battleships.bot.randombot.place_ships_random(defender_field)
        defender = DefenderBot(defender_field, defender_ships)
        ground = battleships.bot.grounds.OneWayGround(attacker, defender)

        for i in range(100):
            if ground.tick():
                return

        self.fail("Bot didn't win after 100 shots")

