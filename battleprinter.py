import field
import shotfinder
import random
import logging


class BattlePrinter:
    def __init__(self,
                 myfield: field.Field,
                 myfinder: shotfinder.ShotFinder = None):
        self.field = myfield
        if myfinder is None:
            self.finder = shotfinder.ShotFinder(myfield)
            logging.warning("Should initialize the battleprinter "
                            "with custom shotfinder")
        else:
            self.finder = myfinder

    class CoolPrinter:
        def __init__(self, shot_list):
            self.shot_list = shot_list

        def print(self, board, x, y):
            if board.cells[x][y] == field.Field.States.empty:
                for coord, value in self.shot_list:
                    if coord.x == x and coord.y == y:
                        return value
                else:
                    return ""
            elif board.cells[x][y] == field.Field.States.hit:
                return "X"
            elif board.cells[x][y] == field.Field.States.miss:
                return "_"
            elif board.cells[x][y] == field.Field.States.suspect:
                return "~"
            else:
                return "?"

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
        shot_list = self.finder.sort_margin()
        cool_print = BattlePrinter.CoolPrinter(shot_list).print
        print(self.field.printTable(cool_print))
        shot_list = BattlePrinter._truncate_shots(shot_list)
        print(", ".join([coord.getHumanStr() for coord in shot_list]))
        print("Random: " + random.sample(shot_list, 1)[0].getHumanStr())
