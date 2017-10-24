import field
import shotfinder
import util

class ShotManager:
    def __init__(self, myfield):
        self.field = myfield
        self.finder = shotfinder.ShotFinder(myfield)

    class CoolPrinter:
        def __init__(self, shot_list):
            self.shot_list = shot_list 

        def print(self, board, x, y):
            if board.cells[x][y] == 0:
                for coord, value in self.shot_list:
                    if coord.x == x and coord.y == y:
                        return value
                else:
                    return ""
            else:
                return board.cells[x][y]

    @staticmethod
    def _truncate_shots(shots):
        best_value = shots[-1][1]
        best_list = [shots[-1][0]]
        for shot in shots[-2::-1]:
            if shot[1] == best_value:
                best_list.append(shot[0])
            else:
                break
        return sorted(best_list, key=lambda x: (x.y, x.x))

    def printTable(self):
        shot_list = self.finder.find_shot()
        print(self.field.printTable(ShotManager.CoolPrinter(shot_list).print))
        for shot in ShotManager._truncate_shots(shot_list):
            print(shot.getHumanStr())

def main():
    mymanager = ShotManager(field.Field(util.Size(10, 10)))
    mymanager.printTable()
    mymanager.field.cells[2][0] = "X" 
    mymanager.field.cells[0][1] = "X" 
    mymanager.field.cells[1][1] = "X" 
    mymanager.printTable()
