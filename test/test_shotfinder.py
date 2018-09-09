"""Contains the ShotFinderTest class"""
import unittest

from .context import battleships

from battleships.management.field import Field
import battleships.management.shotfinder
from battleships.util import Size, Coord


class ShotFinderTest(unittest.TestCase):
    """Tests the shotfinder module"""

    def test_hunt_ship(self) -> None:
        """Check if hunt_ship crashes"""
        myfield = Field(Size(10, 10))

        myfield[Coord(5, 5)] = Field.States.hit
        possible_shipparts = battleships.management.shotfinder.hunt_ship(myfield, Coord(5, 5))
        self.assertTrue((Coord(5, 4), 5) in possible_shipparts)
