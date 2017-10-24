import field
import shotfinder
import util

def coolPrinter(board, x, y):
    if board.cells[x][y] == 0:
        return ""
    else:
        return board.cells[x][y]

myfield = field.Field(util.Size(10, 10))
myfinder = shotfinder.ShotFinder(myfield)
myfield.cells[2][0] = "X" 
myfield.cells[0][1] = "X" 
myfield.cells[1][1] = "X" 
print(myfield.printTable(coolPrinter))
print(myfinder.find_shot())
