"""Contains BattlePrinter class"""
import random
import logging

from . import field
from . import shotfinder


def get_char(board, shot_list, cell_x, cell_y):
    """Convert enum to char"""
    current_cell = board.cells[cell_x][cell_y]
    if current_cell == field.Field.States.empty:
        for coord, value in shot_list:
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


def _truncate_shots(shots):
    best_list = [shot[0] for shot in shots if shot[1] == shots[0][1]]
    return sorted(best_list, key=lambda x: (x.y, x.x))


def print_table(battlefield: field.Field):
    """Print the field"""
    result = ""
    shot_list = shotfinder.list_ship_probabilities(battlefield)

    def cool_char_print(board, cell_x, cell_y): return get_char(
        board, shot_list, cell_x, cell_y)
    result += battlefield.print_table(cool_char_print)
    shot_list = _truncate_shots(shot_list)
    result += ", ".join([repr(coord) for coord in shot_list])
    result += "\n"
    result += "Random: " + repr(random.sample(shot_list, 1)[0])
    return result
