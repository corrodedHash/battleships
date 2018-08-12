"""Contains the ShotFinderTest class"""
import unittest

from management.field import Field
import management.shotfinder as shotfinder
from util import Size, Coord


class ShotFinderTest(unittest.TestCase):
    """Tests the shotfinder module"""

    def test_hunt_ship(self) -> None:
        """Check if hunt_ship crashes"""
        myfield = Field(Size(10, 10))

        myfield[Coord(5, 5)] = Field.States.hit
        possible_shipparts = shotfinder.hunt_ship(myfield, Coord(5, 5))
        self.assertTrue((Coord(5, 4), 5) in possible_shipparts)
