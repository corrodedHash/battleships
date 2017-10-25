import unittest

from field import Field
from shotfinder import ShotFinder
from util import Size, Coord

class ShotFinderTest(unittest.TestCase):
    def test_margin(self):
        myfield = Field(Size(10, 10))
        myfinder = ShotFinder(myfield)

        myfield[Coord(5, 5)] = Field.States.hit
        myfinder.hunt_ship(Coord(5, 5))

