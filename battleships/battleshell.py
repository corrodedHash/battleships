"""Contains BattleShell class"""
import cmd
from typing import Optional

from . import util
from .management import field, shotfinder, battleprinter


class BattleShell(cmd.Cmd):
    """Shell to manually access the battlefield"""
    intro = "Welcome to the [b]4ttl3shell.   "
    "Type help or ? to list commands.\n"
    prompt = 'prostagma? '
    file = None

    def __init__(self) -> None:
        super().__init__()
        self.field: Optional[field.Field] = None

    def _parse_coord(self: 'BattleShell', coord: str) -> Optional[util.Coord]:
        """Helper function to parse an alphanumeric coord to Coord class"""
        try:
            result = util.Coord(alphanum=coord)
        except RuntimeError:
            print("given index was probably not correct")
            return None
        if self.field is None:
            print("Field not yet initialized")
            return None
        if result not in self.field.size:
            print("index out of range")
            return None
        return result

    def do_hunt(self, arg: str) -> None:
        """Hunt the ship under the cursor,
        giving possible further locations"""
        coord = self._parse_coord(arg)
        if coord is None:
            return
        try:
            if self.field is not None:
                ship_parts = shotfinder.hunt_ship(self.field, coord)
        except RuntimeError:
            print("Error")
            return

        print(ship_parts)

    def do_init(self, arg: str) -> None:
        """Initialize the field with the given 2 numbers width and height"""
        try:
            width, height = map(int, arg.split())
        except ValueError:
            print("Cannot initialize")
            return

        self.field = field.Field(util.Size(width, height))

    def _shoot(self, arg: str, char: field.Field.States) -> None:
        """Helper function to change a cell in the field"""
        if self.field is None:
            print("Field is not yet initialized")
            return
        for given_coord in arg.split():
            coord = self._parse_coord(given_coord)
            if coord is None:
                continue
            if self.field[coord] == field.Field.States.empty:
                self.field[coord] = char
            else:
                print("Cell not empty")
                continue

    def do_suspect(self, arg: str) -> None:
        """Set a cell to have logically no ships in it"""
        self._shoot(arg, field.Field.States.suspect)

    def do_hit(self, arg: str) -> None:
        """Set a cell to be a hit ship"""
        self._shoot(arg, field.Field.States.hit)

    def do_miss(self, arg: str) -> None:
        """Set a cell to have no ship in it"""
        self._shoot(arg, field.Field.States.miss)

    def do_reset(self, arg: str) -> None:
        """Reset a cell to unknown status"""
        coord = self._parse_coord(arg)
        if coord is None:
            return
        if self.field is None:
            return
        self.field[coord] = field.Field.States.empty

    def do_add(self, arg: str) -> None:
        """Add a ship in of the given length"""
        if self.field is None:
            return

        try:
            count = int(arg)
            self.field.shipcount[count] += 1
        except ValueError:
            print("Not a number")
        except IndexError:
            print("Not a ship")
        print(self.field.shipcount)

    def do_sink(self, arg: str) -> None:
        """Remove a ship of the given length"""
        if self.field is None:
            return
        try:
            count = int(arg)
            self.field.shipcount[count] -= 1
        except ValueError:
            print("Not a number")
        except IndexError:
            print("Not a ship")
        print(self.field.shipcount)

    def postcmd(self, stop: bool, line: str) -> bool:
        """Print table if the field is initialized"""
        if self.field is not None:
            print(battleprinter.print_summary(self.field))
        return False


if __name__ == '__main__':
    BattleShell().cmdloop()
