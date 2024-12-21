import pygame, random, math


class Cell:
    def __init__(self, x, y, size, col, row) -> None:
        self.x = x
        self.y = y
        self.col = col
        self.row = row
        self.size = size
        self.color = (0, 0, 0)
        self.border_color = (255, 255, 255)

        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False

        self.f = 0
        self.g = 0
        self.h = 0
        self.parent_row = None
        self.parent_col = None

    def show_body(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def show_border(self, win):
        x = self.x
        y = self.y
        s = self.size
        if self.north:
            pygame.draw.line(win, self.border_color, (x, y), (x + s, y))
        if self.south:
            pygame.draw.line(win, self.border_color, (x, y + s), (x + s, y + s))
        if self.west:
            pygame.draw.line(win, self.border_color, (x, y), (x, y + s))
        if self.east:
            pygame.draw.line(win, self.border_color, (x + s, y), (x + s, y + s))


class Grid:
    def __init__(self, x, y, width, height, cell_size) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.grid = []
        self.__make_grid()

        # the maze generation
        self.__first_loop_maze = True
        self.stack = []

        # A star solver
        self.__first_loop_pathfinding = True
        self.open = []
        self.closed = []
        self.trace_current = 0
        self.found = False

    def __make_grid(self):
        x_num = self.width // self.cell_size
        y_num = self.height // self.cell_size
        for j in range(y_num):
            row = []
            for i in range(x_num):
                x = i * self.cell_size + self.x
                y = j * self.cell_size + self.y
                cell = Cell(x, y, self.cell_size, i, j)
                row.append(cell)
            self.grid.append(row)

    def show_grid(self, win):
        for i in self.grid:
            for cell in i:
                cell.show_body(win)

        for i in self.grid:
            for cell in i:
                cell.show_border(win)

    def __is_valid(self, col, row):
        rows = len(self.grid)
        cols = len(self.grid[0])
        return (col < cols) and (col >= 0) and (row < rows) and (row >= 0)

    def generate_maze_step(self, col=0, row=0, targetCol=-1, targetRow=-1):
        if (targetCol == -1) or (targetRow == -1):
            return self.__generate_maze_step(
                col, row, (len(self.grid[0]) - 1), (len(self.grid) - 1)
            )
        else:
            return self.__generate_maze_step(col, row, targetCol, targetRow)

    def generate_maze_full(self, col=0, row=0, targetCol=-1, targetRow=-1):
        if (targetCol == -1) or (targetRow == -1):
            return self.__generate_maze_full(
                col, row, (len(self.grid[0]) - 1), (len(self.grid) - 1)
            )
        else:
            return self.__generate_maze_full(col, row, targetCol, targetRow)

    def __generate_maze_step(self, col, row, targetCol, targetRow):
        if self.__first_loop_maze:
            self.__first_loop_maze = False
            self.starting_cell = self.grid[row][col]
            self.target_cell = self.grid[targetRow][targetCol]
            self.starting_cell.visited = True
            self.stack.append(self.starting_cell)

        # main algorithim body
        if len(self.stack) > 0:
            # current cell
            current_cell = self.stack.pop()
            if current_cell.color == (0, 0, 0):
                current_cell.color = (255, 0, 255)
            elif current_cell.color == (255, 0, 255):
                current_cell.color = (150, 0, 150)

            # neighbors
            neighbor_cells = self.__get_neighbors(current_cell)
            if len(neighbor_cells) != 0:
                self.stack.append(current_cell)
                i = random.randint(0, len(neighbor_cells) - 1)
                next_cell = neighbor_cells[i]
                self.__remove_wall_between(current_cell, next_cell)
                next_cell.visited = True
                self.stack.append(next_cell)
            else:
                current_cell.color = (150, 0, 150)
            return False
        else:
            print("finished generating maze")
            self.__reset_grid_color()
            return True

    def __generate_maze_full(self, col, row, targetCol, targetRow):
        if self.__first_loop_maze:
            self.__first_loop_maze = False
            self.starting_cell = self.grid[row][col]
            self.target_cell = self.grid[targetRow][targetCol]
            self.starting_cell.visited = True
            self.stack.append(self.starting_cell)

        # main algorithim body
        while len(self.stack) > 0:
            # current cell
            current_cell = self.stack.pop()
            if current_cell.color == (0, 0, 0):
                current_cell.color = (255, 0, 255)
            elif current_cell.color == (255, 0, 255):
                current_cell.color = (150, 0, 150)

            # neighbors
            neighbor_cells = self.__get_neighbors(current_cell)
            if len(neighbor_cells) != 0:
                self.stack.append(current_cell)
                i = random.randint(0, len(neighbor_cells) - 1)
                next_cell = neighbor_cells[i]
                self.__remove_wall_between(current_cell, next_cell)
                next_cell.visited = True
                self.stack.append(next_cell)
            else:
                current_cell.color = (150, 0, 150)
        print("finished generating maze")
        self.__reset_grid_color()
        return True

    def __remove_wall_between(self, cell, other):
        row = cell.row - other.row
        col = cell.col - other.col

        if (row == 0) and (col == -1):
            cell.east = False
            other.west = False
            return
        elif (row == 0) and (col == 1):
            cell.west = False
            other.east = False
            return
        elif (col == 0) and (row == -1):
            cell.south = False
            other.north = False
            return
        elif (col == 0) and (row == 1):
            other.south = False
            cell.north = False
            return

    def __get_neighbors(self, cell):
        neighbors = []
        r = cell.row
        c = cell.col

        if self.__is_valid(c + 1, r):
            if not self.grid[r][c + 1].visited:
                neighbors.append(self.grid[r][c + 1])
        if self.__is_valid(c, r + 1):
            if not self.grid[r + 1][c].visited:
                neighbors.append(self.grid[r + 1][c])
        if self.__is_valid(c - 1, r):
            if not self.grid[r][c - 1].visited:
                neighbors.append(self.grid[r][c - 1])
        if self.__is_valid(c, r - 1):
            if not self.grid[r - 1][c].visited:
                neighbors.append(self.grid[r - 1][c])

        return neighbors

    def __reset_grid_color(self):
        for i in self.grid:
            for cell in i:
                cell.color = (0, 0, 0)

    def a_star_step(self, col=0, row=0, targetCol=-1, targetRow=-1):
        if (targetCol == -1) or (targetRow == -1):
            return self.__a_star_step(
                col, row, (len(self.grid[0]) - 1), (len(self.grid) - 1)
            )
        else:
            return self.__a_star_step(col, row, targetCol, targetRow)

    def a_star_full(self, col=0, row=0, targetCol=-1, targetRow=-1):
        if (targetCol == -1) or (targetRow == -1):
            return self.__a_star_full(
                col, row, (len(self.grid[0]) - 1), (len(self.grid) - 1)
            )
        else:
            return self.__a_star_full(col, row, targetCol, targetRow)

    def __a_star_step(self, col, row, targetCol, targetRow):
        if self.__first_loop_pathfinding:
            self.__first_loop_pathfinding = False
            self.target_cell = self.grid[targetRow][targetCol]
            self.starting_cell = self.grid[row][col]
            self.starting_cell.parent_row = 0
            self.starting_cell.parent_col = 0
            self.starting_cell.color = (255, 0, 255)
            self.open.append(self.starting_cell)

        if (len(self.open) > 0) and (not self.found):
            current = self.__get_smallest_f()
            self.open.remove(current)

            self.__handle_successors(current)

            current.color = (150, 0, 150)
            self.closed.append(current)
            return False

        if self.found:
            self.__trace_path()
            return True

    def __a_star_full(self, col, row, targetCol, targetRow):
        if self.__first_loop_pathfinding:
            self.__first_loop_pathfinding = False
            self.target_cell = self.grid[targetRow][targetCol]
            self.starting_cell = self.grid[row][col]
            self.starting_cell.parent_row = 0
            self.starting_cell.parent_col = 0
            self.starting_cell.color = (255, 0, 255)
            self.open.append(self.starting_cell)

        while (len(self.open) > 0) and (not self.found):
            current = self.__get_smallest_f()
            self.open.remove(current)

            self.__handle_successors(current)

            current.color = (150, 0, 150)
            self.closed.append(current)

        if self.found:
            self.__trace_path_full()
            return True

    def __handle_successors(self, current):
        r = current.row
        c = current.col
        successors = []

        if self.__is_valid(c + 1, r):
            s = self.grid[r][c + 1]
            if (not current.east) and (not s.west):
                successors.append(s)
        if self.__is_valid(c - 1, r):
            s = self.grid[r][c - 1]
            if (not current.west) and (not s.east):
                successors.append(s)
        if self.__is_valid(c, r + 1):
            s = self.grid[r + 1][c]
            if (not current.south) and (not s.north):
                successors.append(s)
        if self.__is_valid(c, r - 1):
            s = self.grid[r - 1][c]
            if (not current.north) and (not s.south):
                successors.append(s)

        for s in successors:
            g = current.g + 1
            h = self.__calculate_h(s)
            f = g + h
            if s == self.target_cell:
                s.parent_row = r
                s.parent_col = c
                s.g = g
                s.h = h
                s.f = f
                s.color = (150, 0, 150)
                print("target found")
                self.found = True
            else:
                if (s in self.open) and (s.f < f):
                    continue

                if (s in self.closed) and (s.f < f):
                    continue

                s.parent_row = r
                s.parent_col = c
                s.g = g
                s.h = h
                s.f = f
                s.color = (255, 0, 255)
                if s not in self.open:
                    self.open.append(s)

    def __calculate_h(self, s):
        tRow = self.target_cell.row
        tCol = self.target_cell.col
        a = abs(tRow - s.row)
        b = abs(tCol - s.col)
        return math.sqrt(a**2 + b**2)

    def __trace_path(self):
        if self.trace_current == 0:
            self.starting_cell.color = (0, 150, 0)
            self.trace_current = self.target_cell

        if self.trace_current != self.starting_cell:
            self.trace_current.color = (0, 150, 0)
            pRow = self.trace_current.parent_row
            pCol = self.trace_current.parent_col
            self.trace_current = self.grid[pRow][pCol]

    def __trace_path_full(self):
        if self.trace_current == 0:
            self.starting_cell.color = (0, 150, 0)
            self.trace_current = self.target_cell

        while self.trace_current != self.starting_cell:
            self.trace_current.color = (0, 150, 0)
            pRow = self.trace_current.parent_row
            pCol = self.trace_current.parent_col
            self.trace_current = self.grid[pRow][pCol]

    def __get_smallest_f(self):
        f = -1
        smallest = 0
        for cell in self.open:
            if (f == -1) or (cell.f < f):
                f = cell.f
                smallest = cell

        return smallest
