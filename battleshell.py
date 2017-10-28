"""Contains BattleShell class"""
import cmd

import util
import management.field as field
import management.shotfinder as shotfinder
import management.battleprinter as battleprinter


class BattleShell(cmd.Cmd):
    """Shell to manually access the battlefield"""
    intro = "Welcome to the [b]4ttl3shell.   "
    "Type help or ? to list commands.\n"
    prompt = 'prostagma? '
    file = None

    def __init__(self):
        super().__init__()
        self.field = None
        self.finder = None
        self.printer = None

    def _parse_coord(self, coord):
        """Helper function to parse an alphanumeric coord to Coord class"""
        try:
            result = util.Coord(alphanum=coord)
        except RuntimeError:
            print("given index was probably not correct")
            return None
        if result not in self.field.size:
            print("index out of range")
            return None
        return result

    def do_hunt(self, arg):
        """Hunt the ship under the cursor,
        giving possible further localtions"""
        coord = self._parse_coord(arg)
        if coord is None:
            return
        try:
            ship_parts = self.printer.finder.hunt_ship(coord)
        except RuntimeError:
            print("Error")
            return

        print(ship_parts)

    def do_init(self, arg):
        """Initialize the field with the given 2 numbers width and height"""
        width, height = map(int, arg.split())
        self.field = field.Field(util.Size(width, height))
        self.finder = shotfinder.ShotFinder(self.field)
        self.printer = battleprinter.BattlePrinter(self.field, self.finder)

    def _shoot(self, arg, char: field.Field.States):
        """Helper function to change a cell in the field"""
        for given_coord in arg.split():
            coord = self._parse_coord(given_coord)
            if coord is None:
                continue
            if self.field[coord] == field.Field.States.empty:
                self.field[coord] = char
            else:
                print("Cell not empty")
                continue

    def do_suspect(self, arg):
        """Set a cell to have logically no ships in it"""
        self._shoot(arg, field.Field.States.suspect)

    def do_hit(self, arg):
        """Set a cell to be a hit ship"""
        self._shoot(arg, field.Field.States.hit)

    def do_miss(self, arg):
        """Set a cell to have no ship in it"""
        self._shoot(arg, field.Field.States.miss)

    def do_reset(self, arg):
        """Reset a cell to unknown status"""
        coord = self._parse_coord(arg)
        if coord is None:
            return
        self.field[coord] = field.Field.States.empty

    def do_add(self, arg):
        """Add a ship in of the given length"""
        try:
            count = int(arg)
            self.field.shipcount[count] += 1
        except ValueError:
            print("Not a number")
        except IndexError:
            print("Not a ship")
        print(self.field.shipcount)

    def do_sink(self, arg):
        """Remove a ship of the given length"""
        try:
            count = int(arg)
            self.field.shipcount[count] -= 1
        except ValueError:
            print("Not a number")
        except IndexError:
            print("Not a ship")
        print(self.field.shipcount)

    def postcmd(self, stop, line):
        """Print table if the field is initialized"""
        if self.printer is not None:
            print(self.printer.print_table())
        return False


if __name__ == '__main__':
    BattleShell().cmdloop()
