"""Contains BattlePrinter class"""
import random
import logging

from . import field
from . import shotfinder
from typing import Union, List, Tuple, Iterable
from util import Coord


def get_char(board: field.Field,
             shot_list: List[Tuple[Coord,
                                   int]],
             cell_x: int,
             cell_y: int) -> Union[str,
                                   int]:
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


def _truncate_shots(shots: List[Tuple[Coord, int]]) -> Iterable[Coord]:
    best_list = [shot[0] for shot in shots if shot[1] == shots[0][1]]
    return sorted(best_list, key=lambda x: (x.y, x.x))


def print_table(battlefield: field.Field) -> str:
    """Print the field"""
    result = ""
    shot_list = shotfinder.list_ship_probabilities(battlefield)

    def cool_char_print(board: field.Field,
                        cell_x: int,
                        cell_y: int) -> str:
        return str(get_char(board,
                            shot_list,
                            cell_x,
                            cell_y))
    result += battlefield.print_table(cool_char_print)
    refined_shot_list = list(_truncate_shots(shot_list))
    result += ", ".join([repr(coord) for coord in refined_shot_list])
    result += "\n"
    result += "Random: " + repr(random.sample(refined_shot_list, 1)[0])
    return result
