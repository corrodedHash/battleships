"""Contains ShotFinder class"""
from util import Coord, Direction, Orientation, DIRTUPLE_MAP, DIRORI_MAP
import management.field as field
from management.field import Field
import logging

def get_ship_probability(battlefield: Field, cell: Coord):
    """Probability of a cell containing a ship"""
    if battlefield[cell] != field.Field.States.empty:
        logging.warning("Querying ship probability of known cell " + cell)
        return 0
    margin = battlefield.get_margins(cell)
    total_possible_positions = 0
    for ship_size in range(1, len(battlefield.shipcount) + 1):
        top = min(margin[Direction.top], ship_size - 1)
        bottom = min(
            margin[Direction.bottom], ship_size - 1)
        left = min(margin[Direction.left], ship_size - 1)
        right = min(margin[Direction.right], ship_size - 1)
        possible_positions = max(0, left + right + 2 - ship_size)
        possible_positions += max(0, top + bottom + 2 - ship_size)
        total_possible_positions += possible_positions * \
            battlefield.shipcount[ship_size - 1]
    return total_possible_positions

def list_ship_probabilities(battlefield: Field):
        """Returns a list of coords
        Sorted by the probabilities that a ship is in that coord"""
        result = list()
        for cell in battlefield:
            if battlefield[cell] != field.Field.States.empty:
                continue
            result.append((cell, get_ship_probability(battlefield, cell)))
        return sorted(result, key=lambda x: x[1], reverse=True)

def find_ship_end(battlefield: Field, cell: Coord, dir_tuple):
    """Move in the given direction until hitting a un-hit cell"""
    new_point = cell
    while new_point + dir_tuple in battlefield.size:
        if battlefield[new_point + dir_tuple] != field.Field.States.hit:
            return new_point
        new_point = new_point + dir_tuple
    return new_point

def get_ship_orientation(battlefield: Field, cell: Coord):
    if battlefield[cell] != field.Field.States.hit:
        logging.warning("Querying ship orientation on un-hit cell " + cell)
        raise RuntimeError

    ship_orientation = Orientation.unknown
    for direction in Direction:
        dir_tuple = DIRTUPLE_MAP[direction]
        new_cell = cell + dir_tuple
        if new_cell not in battlefield.size:
            continue

        if battlefield[new_cell] == field.Field.States.hit:
            ship_orientation = ship_orientation + DIRORI_MAP[direction]

    if ship_orientation == Orientation.both:
        logging.warning("Impossible ship configuration on " + cell)
        raise RuntimeError

    return ship_orientation


def hunt_ship(battlefield: Field, cell: Coord):
    """Return possible next coords for the ship on the given coord"""

    if battlefield[cell] != field.Field.States.hit:
        logging.warning("Hunting ship on un-hit cell " + cell)
        raise RuntimeError

    ship_orientation = get_ship_orientation(battlefield, cell) 

    result_list = []

    if ship_orientation == Orientation.both:
        raise RuntimeError
    elif ship_orientation == Orientation.unknown:
        margin = battlefield.get_margins(cell)
        result_list.append(
            (cell + (0, -1), margin[Direction.top]))
        result_list.append(
            (cell + (0, 1), margin[Direction.bottom]))
        result_list.append(
            (cell + (-1, 0), margin[Direction.left]))
        result_list.append(
            (cell + (1, 0), margin[Direction.right]))
        result_list = [x for x in result_list if x[1] > 0]
    else:  # either horizontal or vertical
        directions = [key for key, value in DIRORI_MAP.items() 
                if value == ship_orientation]
        for direction in directions:
            dir_tuple = DIRTUPLE_MAP[direction]
            ship_end = find_ship_end(battlefield, cell, dir_tuple)
            ship_margin = battlefield.get_margins(ship_end)[direction]
            if ship_margin > 0:
                result_list.append((ship_end + dir_tuple, ship_margin))

    result_list = sorted(result_list, key=lambda x: x[1], reverse=True)
    return result_list
