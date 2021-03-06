"""Contains BattleShellTest class"""
import unittest

from .context import battleships

from battleships import battleshell
from battleships.management import field
from battleships.util import Coord


class BattleShellTest(unittest.TestCase):
    """Tests the battleshell module"""

    def test_standard(self) -> None:
        """Just tries a few commands"""
        myshell = battleshell.BattleShell()
        myshell.do_init("10 10")
        myshell.do_hit("B4")
        assert myshell.field is not None
        self.assertEqual(myshell.field[Coord(3, 1)], field.Field.States.hit)
        myshell.do_miss("C1")
        self.assertEqual(myshell.field[Coord(0, 2)], field.Field.States.miss)
        myshell.do_reset("B4")
        self.assertEqual(myshell.field[Coord(3, 1)], field.Field.States.empty)
        myshell.do_reset("J9")
        self.assertEqual(myshell.field[Coord(8, 9)], field.Field.States.empty)
