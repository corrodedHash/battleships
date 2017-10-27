"""Contains Grounds class"""
from util import Coord


class Grounds:
    """Interface for two battleship AIs to fight"""

    def __init__(self):
        self.player1 = None
        self.player2 = None
