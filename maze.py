import random
import time

class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {
            'left': True,
            'right': True,
            'top': True,
            'bottom': True
        }
        self.neighbors = []
        self.visited = False

    def __repr__(self):
        return f'{self.x} {self.y}'

    def visit(self):
        self.visited = True

class Maze:
    def __init__(self, rows, cols, cell_size, drawer):
        self.grid = []
        self.cell_size = cell_size
        self.width = cols
        self.height = rows
        self.drawer = drawer
        self.unvisited = rows*cols
        for y in range(rows):
            row = []
            for x in range(cols):
                row.append(Cell(x, y))
            self.grid.append(row)

    def get_neighbors(self, cell):
        neighbors = []
        x = cell.x
        y = cell.y
        left = self.grid[y][x-1] if x > 0 else None
        right = self.grid[y][x+1] if x < self.width-1 else None
        up = self.grid[y-1][x] if y > 0 else None
        down = self.grid[y+1][x] if y < self.height-1 else None
        for cell in [left, right, up, down]:
            if cell and not cell.visited:
                neighbors.append(cell)
        return neighbors if len(neighbors) > 0 else None

    def generate(self, initial_x, initial_y, final_x, final_y):
        if initial_x >= self.width or initial_y >= self.height or final_x >= self.width or final_y >= self.height:
            return None
        stack = []
        current = self.grid[initial_y][initial_x]
        current.visit()
        self.unvisited = self.unvisited - 1
        while self.unvisited:
            self.draw()
            print(current)
            input()
            neighbors = self.get_neighbors(current)
            if neighbors:
                nextcell = neighbors[random.randint(0, len(neighbors)-1)]
                if len(neighbors) > 1:
                    stack.append(current)
                if current.x == nextcell.x:
                    if current.y < nextcell.y:
                        current.walls['top'] = False
                        nextcell.walls['bottom'] = False
                    else:
                        current.walls['bottom'] = False
                        nextcell.walls['top'] = False
                if current.y == nextcell.y:
                    if current.x < nextcell.x:
                        current.walls['left'] = False
                        nextcell.walls['right'] = False
                    else:
                        current.walls['right'] = False
                        nextcell.walls['left'] = False
                current = nextcell
                current.visit()
                self.unvisited = self.unvisited - 1

            else:
                current = stack.pop()
                while stack and not self.get_neighbors(current):
                    current = stack.pop()


    def draw(self):
        for row in self.grid:
            for cell in row:
                if cell.walls['left']:
                    startx = cell.x * self.cell_size
                    starty = cell.y * self.cell_size
                    endx = startx
                    endy = starty + self.cell_size
                    self.drawer.line(startx, starty, endx, endy)
                if cell.walls['right']:
                    startx = cell.x * self.cell_size + self.cell_size
                    starty = cell.y * self.cell_size
                    endx = startx
                    endy = starty + self.cell_size
                    self.drawer.line(startx, starty, endx, endy)
                if cell.walls['top']:
                    startx = cell.x * self.cell_size
                    starty = cell.y * self.cell_size
                    endx = startx + self.cell_size
                    endy = starty
                    self.drawer.line(startx, starty, endx, endy)
                if cell.walls['bottom']:
                    startx = cell.x * self.cell_size
                    starty = cell.y * self.cell_size + self.cell_size
                    endx = startx + self.cell_size
                    endy = starty
                    self.drawer.line(startx, starty, endx, endy)
        self.drawer.save()

    def print_grid(self, current):
        rows = []
        for row in self.grid:
            l = ''
            for c in row:
                if c.visited:
                    l = f'{l}.'
                else:
                    l = f'{l} '
            rows.append(l)
        rows[current.y] = rows[current.y][0:current.x] + '+' + rows[current.y][current.x+1:]
        print('+----------+')
        for row in rows:
            print(f'|{row}|')
        print('+----------+')
