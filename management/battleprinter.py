"""Contains BattlePrinter class"""
import random
import logging

from . import field
from . import shotfinder


class BattlePrinter:
    """Prints a field neatly"""

    def __init__(self,
                 myfield: field.Field,
                 myfinder: shotfinder.ShotFinder = None):
        self.field = myfield
        if myfinder is None:
            self.finder = shotfinder.ShotFinder(myfield)
            logging.warning("Should initialize the battleprinter "
                            "with custom shotfinder")
        else:
            self.finder = myfinder

    class CoolPrinter:
        """Functor that converts cell-state enums to chars"""

        def __init__(self, shot_list):
            self.shot_list = shot_list

        def get_char(self, board, cell_x, cell_y):
            """Convert enum to char"""
            current_cell = board.cells[cell_x][cell_y]
            if current_cell == field.Field.States.empty:
                for coord, value in self.shot_list:
                    if coord.x == cell_x and coord.y == cell_y:
                        return value
                return ""
            elif current_cell == field.Field.States.hit:
                return "X"
            elif current_cell == field.Field.States.miss:
                return "_"
            elif current_cell == field.Field.States.suspect:
                return "~"
            return "?"

    @staticmethod
    def _truncate_shots(shots):
        best_list = [shot[0] for shot in shots if shot[1] == shots[-1][1]]
        return sorted(best_list, key=lambda x: (x.y, x.x))

    def print_table(self):
        """Print the field"""
        result = ""
        shot_list = self.finder.sort_margin()
        cool_print = BattlePrinter.CoolPrinter(shot_list).get_char
        result += self.field.print_table(cool_print)
        shot_list = BattlePrinter._truncate_shots(shot_list)
        result += ", ".join([repr(coord) for coord in shot_list])
        result += "Random: " + repr(random.sample(shot_list, 1)[0])
        return result
