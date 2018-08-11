"""Contains the FieldTest class"""
import unittest

from management.field import Field
from util import Size, Coord, Direction



class FieldTest(unittest.TestCase):
    """Tests the field module"""

    def test_margin(self) -> None:
        """Asserts that the margin is calculated correctly"""
        myfield = Field(Size(10, 10))
        mymargin = myfield.get_margins(Coord(5, 5))
        self.assertEqual(mymargin[Direction.left], 5)
        self.assertEqual(mymargin[Direction.top], 5)
        self.assertEqual(mymargin[Direction.right], 4)
        self.assertEqual(mymargin[Direction.bottom], 4)

    def test_asymmetric_board(self) -> None:
        """Checks if Field can handle non-square fields"""
        myfield = Field(Size(3, 2))
        self.assertEqual(myfield[Coord(2, 1)], Field.States.empty)
