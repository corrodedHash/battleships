from .direction import Direction
from .orientation import Orientation

DIRTUPLE_MAP = {Direction.top: (0, -1),
                Direction.bottom: (0, 1),
                Direction.left: (-1, 0),
                Direction.right: (1, 0)}

DIRORI_MAP = {Direction.top: Orientation.vertical,
              Direction.bottom: Orientation.vertical,
              Direction.left: Orientation.horizontal,
              Direction.right: Orientation.horizontal}
