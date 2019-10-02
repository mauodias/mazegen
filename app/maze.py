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
    def __init__(self, rows, cols, cell_size, drawer, debug=False):
        self.debug = debug
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
            if self.debug:
                self.print_grid(current)
            neighbors = self.get_neighbors(current)
            if neighbors:
                nextcell = neighbors[random.randint(0, len(neighbors)-1)]
                if len(neighbors) > 1:
                    stack.append(current)
                if current.x == nextcell.x:
                    if current.y > nextcell.y:
                        current.walls['top'] = False
                        nextcell.walls['bottom'] = False
                    else:
                        current.walls['bottom'] = False
                        nextcell.walls['top'] = False
                if current.y == nextcell.y:
                    if current.x > nextcell.x:
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
        return self.drawer.get_contents()

    def print_grid(self, current):
        ul = u'\u250f'
        ur = u'\u2513'
        dl = u'\u2517'
        dr = u'\u251b'
        v = u'\u2503'
        h = u'\u2501'
        hl = u'\u252b'
        hr = u'\u2523'
        vu = u'\u253b'
        vd = u'\u2533'
        curr = u'\u25cf'
        vstd = u'\u25aa'
        local_grid = [' '] * (self.height * 3 + 2)
        for row in range(len(local_grid)):
            local_grid[row] = [' '] * (self.width * 3 + 2)
        for row in range(self.height):
            for col in range(self.width):
                cell = self.grid[col][row]
                x = row * 3 + 2
                y = col * 3 + 2
                local_grid[y][x] = vstd if cell.visited else ' '
                if cell.walls['top']:
                    local_grid[y-1][x-1] = ul
                    local_grid[y-1][x] = h
                    local_grid[y-1][x+1] = ur
                if cell.walls['bottom']:
                    local_grid[y+1][x-1] = dl
                    local_grid[y+1][x] = h
                    local_grid[y+1][x+1] = dr
                if cell.walls['left']:
                    local_grid[y][x-1] = v
                if cell.walls['right']:
                    local_grid[y][x+1] = v

        local_grid[0][0] = ul
        local_grid[0][self.width*3+1] = ur
        local_grid[self.height*3+1][0] = dl
        local_grid[self.height*3+1][self.width*3+1] = dr
        partial_result = ''
        for row in local_grid:
            partial_result = partial_result + ''.join(x for x in row) + '\n'
        result = ''.join(x for x in partial_result)
        print(result)
        time.sleep(1)
