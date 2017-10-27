import unittest

from management.field import Field
from util import Size, Coord, Space


class FieldTest(unittest.TestCase):
    def test_margin(self):
        myfield = Field(Size(10, 10))
        mymargin = myfield.getMargins(Coord(5, 5))
        self.assertEqual(mymargin[Space.Direction.left], 5)
        self.assertEqual(mymargin[Space.Direction.top], 5)
        self.assertEqual(mymargin[Space.Direction.right], 4)
        self.assertEqual(mymargin[Space.Direction.bottom], 4)

    def test_asymBoard(self):
        myfield = Field(Size(3, 2)) # NOQA
