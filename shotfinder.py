import util
class ShotFinder:
    def __init__(self, search_field):
        self.field = search_field
        self.shipcount = [0, 4, 3, 2, 1]

    def find_shot(self):
        result = list()
        for cell in self.field.allCells():
            if self.field.cells[cell.x][cell.y] != 0:
                continue
            margin = self.field.getMargins(cell)
            total_pp = 0
            for ship_size in range(1, len(self.shipcount) + 1):
                top = min(margin.top, ship_size - 1)
                bottom = min(margin.bottom, ship_size - 1)
                left = min(margin.left, ship_size - 1)
                right = min(margin.right, ship_size - 1)
                possible_positions = max(0, left + right + 2 - ship_size)
                possible_positions += max(0, top + bottom + 2 - ship_size)
                total_pp += possible_positions * self.shipcount[ship_size - 1]
            result.append((cell, total_pp))
        return sorted(result, key=lambda x: x[1])

