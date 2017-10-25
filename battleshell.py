import cmd
import os

import battleprinter
import field
import util

class BattleShell(cmd.Cmd):
    intro = 'Welcome to the [b]4ttl3shell.   Type help or ? to list commands.\n'
    prompt = 'prostagma? '
    file = None

    def __init__(self):
        super().__init__()
        self.field = None
        self.printer = None

    def parse_coord(self, coord):
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
        coord = self.parse_coord(arg)
        if coord is None:
            return
        print(self.printer.finder.hunt_ship(coord))

    def do_init(self, arg):
        width, height = map(int, arg.split())
        self.field = field.Field(util.Size(width, height))
        self.printer = battleprinter.BattlePrinter(self.field)

    def shoot(self, arg, char: field.Field.States):
        for given_coord in arg.split():
            coord = self.parse_coord(given_coord)
            if coord is None:
                continue
            if self.field[coord] == field.Field.States.empty:
                self.field[coord] = char 
            else:
                print("Cell not empty")
                continue

    def do_suspect(self, arg):
        self.shoot(arg, field.Field.States.suspect)

    def do_hit(self, arg):
        self.shoot(arg, field.Field.States.hit)

    def do_miss(self, arg):
        self.shoot(arg, field.Field.States.miss)

    def do_reset(self, arg):
        coord = self.parse_coord(arg)
        if coord is None:
            return
        self.field[coord] = field.Field.States.empty 

    def do_add(self, arg):
        try:
            count = int(arg)
            self.printer.finder.shipcount[count] += 1
        except ValueError:
            print("Not a number")
        except IndexError:
            print("Not a ship")
        print(self.printer.finder.shipcount)

    def do_sink(self, arg):
        try:
            count = int(arg)
            self.printer.finder.shipcount[count] -= 1
        except ValueError:
            print("Not a number")
        except IndexError:
            print("Not a ship")
        print(self.printer.finder.shipcount)
    
    def postcmd(self, stop, line):
        if self.printer is not None:
            self.printer.printTable()
        return False


if __name__ == '__main__':
    BattleShell().cmdloop()
