import unittest

from field import Field
from util import Size, Coord

class FieldTest(unittest.TestCase):
    def test_margin(self):
        myfield = Field(Size(10, 10))
        mymargin = myfield.getMargins(Coord(5, 5))
        self.assertEqual(mymargin.left, 5)
        self.assertEqual(mymargin.top, 5)
        self.assertEqual(mymargin.right, 4)
        self.assertEqual(mymargin.bottom, 4)

    def test_asymBoard(self):
        myfield = Field(Size(3, 2))

