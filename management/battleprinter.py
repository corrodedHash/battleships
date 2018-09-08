"""Contains BattlePrinter class"""
import random
from typing import Union, List, Tuple, Iterable, Optional, Callable

from util import Coord, to_alpha
from .field import Field
from . import shotfinder


def default_get_char(board: Field, cell: Coord) -> str:
    """Replace enum with char"""
    enum_translation = {Field.States.empty: " ", Field.States.hit: "X",
                        Field.States.miss: "~", Field.States.sunk: "#",
                        Field.States.suspect: "v",
                        Field.States.intact: "O"}
    return enum_translation[board[cell]]


def probability_get_char(board: Field,
                         shot_list: List[Tuple[Coord, int]],
                         cell: Coord) -> str:
    """Convert enum to char"""
    current_cell = board[cell]
    if current_cell == Field.States.empty:
        for coord, value in shot_list:
            if coord == cell:
                return str(value)
        return ""
    return default_get_char(board, cell)


def print_field(battlefield: Field, char_fun: Callable[[
        Field, Coord], str] = default_get_char) -> str:
    """Print the field"""

    top_bar_items = ["| {:<2}".format(x + 1) for x in 
            range(battlefield.size.width)]
    top_bar = "".join(top_bar_items)
    top_bar = "  " + top_bar

    horizontal_seperator = "\n--"
    horizontal_seperator += "+---" * battlefield.size.width
    horizontal_seperator += "\n"

    result = top_bar
    result += horizontal_seperator

    for cell_y in range(battlefield.size.height):
        result += "{0} ".format(to_alpha(cell_y))
        for cell_x in range(battlefield.size.width):
            cell_str = char_fun(battlefield, Coord(cell_x, cell_y))
            result += "|{:^3}".format(cell_str)
        result += horizontal_seperator
    return result


def _truncate_shots(shots: List[Tuple[Coord, int]]) -> Iterable[Coord]:
    best_list = [shot[0] for shot in shots if shot[1] == shots[0][1]]
    return sorted(best_list, key=lambda x: (x.y, x.x))


def print_summary(battlefield: Field) -> str:
    """Print the field"""
    result = ""
    shot_list = shotfinder.list_ship_probabilities(battlefield)
    refined_shot_list = list(_truncate_shots(shot_list))

    def cool_char_printer(board: Field, cell: Coord) -> str: 
        return probability_get_char(board, shot_list, cell)

    result += print_field(battlefield, cool_char_printer)
    result += ", ".join([repr(coord) for coord in refined_shot_list])
    result += "\n"
    result += "Random: " + repr(random.sample(refined_shot_list, 1)[0])
    return result
