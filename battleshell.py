import cmd
import os

import battlemanager
import field
import util

class BattleShell(cmd.Cmd):
    intro = 'Welcome to the [b]4ttl3shell.   Type help or ? to list commands.\n'
    prompt = 'prostagma? '
    file = None

    def __init__(self):
        super().__init__()
        self.field = None
        self.manager = None

    def do_init(self, arg):
        width, height = map(int, arg.split())
        self.field = field.Field(util.Size(width, height))
        self.manager = battlemanager.battleManager(self.field)

    def shoot(self, arg, char):
        for given_coord in arg.split():
            try:
                coord = util.Coord(alphanum=given_coord)
            except RuntimeError:
                print("given index was probably not correct")
                continue

            if coord not in self.field.size:
                print("index out of range")
                continue
            if self.field.cells[coord.x][coord.y] == 0:
                self.field.cells[coord.x][coord.y] = char 
            else:
                print("Cell not empty")
                continue

    def do_suspect(self, arg):
        self.shoot(arg, "~")

    def do_hit(self, arg):
        self.shoot(arg, "X")

    def do_miss(self, arg):
        self.shoot(arg, "_")

    def do_reset(self, arg):
        try:
            coord = util.Coord(alphanum=arg)
        except RuntimeError:
            print("given index was probably not correct")
            return
        self.field.cells[coord.x][coord.y] = 0 

    def do_add(self, arg):
        try:
            count = int(arg)
            self.manager.finder.shipcount[count] += 1
        except ValueError:
            print("Not a number")
        except IndexError:
            print("Not a ship")
        print(self.manager.finder.shipcount)

    def do_sink(self, arg):
        try:
            count = int(arg)
            self.manager.finder.shipcount[count] -= 1
        except ValueError:
            print("Not a number")
        except IndexError:
            print("Not a ship")
        print(self.manager.finder.shipcount)
    
    def postcmd(self, stop, line):
        if self.manager is not None:
            self.manager.printTable()
        return False


if __name__ == '__main__':
    BattleShell().cmdloop()
