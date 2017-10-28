"""Contains Space class"""
import enum
from enum import Enum

from .direction import Direction


class Space:
    """Specifies distances of a point in 4 directions"""

    def __init__(self):
        self.values = dict()

    def __getitem__(self, key: Direction):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __repr__(self):
        return str(self.values)
