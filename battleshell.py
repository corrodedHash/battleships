import cmd
import os

import shotmanager
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
        self.manager = shotmanager.ShotManager(self.field)

    def shoot(self, arg, char):
        try:
            coord = util.Coord(alphanum=arg)
        except RuntimeError:
            print("given index was probably not correct")
            return

        if coord not in self.field.size:
            print("index out of range")
            return
        if self.field.cells[coord.x][coord.y] == 0:
            self.field.cells[coord.x][coord.y] = char 
        else:
            print("Cell not empty")

    def do_suspect(self, arg):
        self.shoot(arg, "~")

    def do_hit(self, arg):
        self.shoot(arg, "X")

    def do_miss(self, arg):
        self.shoot(arg, "_")

    def do_reset(self, arg):
        x, y = map(int, arg.split())
        self.field.cells[x][y] = 0 
    
    def postcmd(self, stop, line):
        if self.manager is not None:
            self.manager.printTable()
        return False


if __name__ == '__main__':
    BattleShell().cmdloop()
