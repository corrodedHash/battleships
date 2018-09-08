"""Contains utilities"""
import unittest
import random

from util import from_alpha, to_alpha, Direction, counter_clockwise, clockwise, Orientation, change_orientation, accumulate_orientation


class UtilTest(unittest.TestCase):
    """Tests the util module"""

    def test_alphanum(self) -> None:
        """Convert rics from and to real numbers"""
        self.assertEqual(to_alpha(0), "A")
        self.assertEqual(from_alpha("A"), 0)
        self.assertEqual(to_alpha(7), "H")
        self.assertEqual(from_alpha("H"), 7)
        self.assertEqual(to_alpha(15), "P")
        self.assertEqual(from_alpha("P"), 15)

    def test_alphanum_random(self) -> None:
        for i in range(100):
            current_num = random.randint(0, 1000)
            num = to_alpha(current_num)
            returned_num = from_alpha(num)
            self.assertEqual(returned_num, current_num)

    def test_direction(self) -> None:
        self.assertEqual(Direction.top, counter_clockwise(Direction.right)) 
        self.assertEqual(Direction.left, clockwise(Direction.bottom))
