import time
import random
from tkinter import Tk, BOTH, Canvas

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
    
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.start_point.x, self.start_point.y,
            self.end_point.x, self.end_point.y,
            fill=fill_color, width=2
        )

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.visited = False
    
    def draw(self):
        if self._win is None:
            return
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "white")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "white")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "white")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "white")

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        color = "gray" if undo else "red"
        from_center_x = (self._x1 + self._x2) // 2
        from_center_y = (self._y1 + self._y2) // 2
        to_center_x = (to_cell._x1 + to_cell._x2) // 2
        to_center_y = (to_cell._y1 + to_cell._y2) // 2
        self._win.draw_line(Line(Point(from_center_x, from_center_y), Point(to_center_x, to_center_y)), color)

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.geometry(f"{width}x{height}")
        
        self.__canvas = Canvas(self.__root)
        self.__canvas.pack(fill=BOTH, expand=True)
        
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
    
    def close(self):
        self.__running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        if seed is not None:
            random.seed(seed)
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                cell_x1 = self._x1 + i * self._cell_size_x
                cell_y1 = self._y1 + j * self._cell_size_y
                cell_x2 = cell_x1 + self._cell_size_x
                cell_y2 = cell_y1 + self._cell_size_y
                cell = Cell(cell_x1, cell_y1, cell_x2, cell_y2, self._win)
                column.append(cell)
            self._cells.append(column)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            directions = []
            if i > 0 and not self._cells[i - 1][j].visited:
                directions.append((-1, 0))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                directions.append((1, 0))
            if j > 0 and not self._cells[i][j - 1].visited:
                directions.append((0, -1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                directions.append((0, 1))
            
            if not directions:
                self._draw_cell(i, j)
                return
            
            di, dj = random.choice(directions)
            ni, nj = i + di, j + dj
            
            if di == -1:
                self._cells[i][j].has_left_wall = False
                self._cells[ni][nj].has_right_wall = False
            elif di == 1:
                self._cells[i][j].has_right_wall = False
                self._cells[ni][nj].has_left_wall = False
            elif dj == -1:
                self._cells[i][j].has_top_wall = False
                self._cells[ni][nj].has_bottom_wall = False
            elif dj == 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[ni][nj].has_top_wall = False
            
            self._break_walls_r(ni, nj)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw()
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        # Break entrance (top wall of top-left cell)
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        
        # Break exit (bottom wall of bottom-right cell)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self._num_cols and 0 <= nj < self._num_rows and not self._cells[ni][nj].visited:
                if (di == -1 and not self._cells[i][j].has_left_wall) or \
                   (di == 1 and not self._cells[i][j].has_right_wall) or \
                   (dj == -1 and not self._cells[i][j].has_top_wall) or \
                   (dj == 1 and not self._cells[i][j].has_bottom_wall):
                    self._cells[i][j].draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)

        return False

# Example usage in main function
def main():
    win = Window(800, 600)
    
    maze = Maze(50, 50, 10, 10, 50, 50, win, seed=0)
    maze.solve()
    
    win.wait_for_close()

if __name__ == "__main__":
    main()