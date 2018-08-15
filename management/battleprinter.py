"""Contains BattlePrinter class"""
import random
from typing import Union, List, Tuple, Iterable, Optional, Callable

from util import Coord, to_alpha
from .field import Field
from . import shotfinder


def print_field(battlefield: Field, char_fun: Optional[Callable[[
        'Field', int, int], str]] = None) -> str:
    """Print the field"""
    def standard_print(board: 'Field', x: int, y: int) -> str:
        """Replace enum with char"""
        enum_translation = {Field.States.empty: " ", Field.States.hit: "X",
                            Field.States.miss: "~", Field.States.sunk: "#",
                            Field.States.suspect: "v",
                            Field.States.intact: "O"}
        return enum_translation[board[Coord(x, y)]]
    my_char_fun = standard_print
    if char_fun is not None:
        my_char_fun = char_fun
    result = "  "
    top_bar = ["| {:<2}".format(x + 1) for x in range(len(battlefield.cells))]
    result += "".join(top_bar)
    result += "\n--"
    result += "+---" * len(battlefield.cells)
    result += "\n"
    for cell_y in range(len(battlefield.cells[0])):
        result += "{0} ".format(to_alpha(cell_y))
        for cell_x in range(len(battlefield.cells)):
            result += "|{:^3}".format(my_char_fun(battlefield, cell_x, cell_y))
        result += "\n--"
        result += "+---" * len(battlefield.cells)
        result += "\n"
    return result


def get_char(board: Field,
             shot_list: List[Tuple[Coord,
                                   int]],
             cell_x: int,
             cell_y: int) -> Union[str,
                                   int]:
    """Convert enum to char"""
    current_cell = board.cells[cell_x][cell_y]
    if current_cell == Field.States.empty:
        for coord, value in shot_list:
            if coord.x == cell_x and coord.y == cell_y:
                return value
        return ""
    if current_cell == Field.States.hit:
        return "X"
    if current_cell == Field.States.miss:
        return "_"
    if current_cell == Field.States.suspect:
        return "~"
    return "?"


def _truncate_shots(shots: List[Tuple[Coord, int]]) -> Iterable[Coord]:
    best_list = [shot[0] for shot in shots if shot[1] == shots[0][1]]
    return sorted(best_list, key=lambda x: (x.y, x.x))


def print_summary(battlefield: Field) -> str:
    """Print the field"""
    result = ""
    shot_list = shotfinder.list_ship_probabilities(battlefield)

    def cool_char_print(board: Field,
                        cell_x: int,
                        cell_y: int) -> str:
        return str(get_char(board,
                            shot_list,
                            cell_x,
                            cell_y))
    result += print_field(battlefield, cool_char_print)
    refined_shot_list = list(_truncate_shots(shot_list))
    result += ", ".join([repr(coord) for coord in refined_shot_list])
    result += "\n"
    result += "Random: " + repr(random.sample(refined_shot_list, 1)[0])
    return result
