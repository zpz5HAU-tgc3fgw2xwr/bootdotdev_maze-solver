import random
import time
from mazesolver.entities.cell import Cell

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
		"""Initialize the grid of cells and break walls."""
		for col in range(self._num_cols):
			column = []
			for row in range(self._num_rows):
				x1 = self._x1 + col * self._cell_size_x
				y1 = self._y1 + row * self._cell_size_y
				x2 = x1 + self._cell_size_x
				y2 = y1 + self._cell_size_y
				column.append(Cell(x1, y1, x2, y2, self._win))
			self._cells.append(column)

		self._break_entrance_and_exit()
		self._break_walls_r(0, 0)
		self._reset_cells_visited()
		self._redraw_maze()

	def _redraw_maze(self):
		"""Redraw all cells after walls are broken."""
		for col in self._cells:
			for cell in col:
				cell.draw()

	def _break_walls_r(self, col, row):
		"""Recursively break walls to create a solvable maze."""
		self._cells[col][row].visited = True
		while True:
			directions = []
			if col > 0 and not self._cells[col - 1][row].visited:
				directions.append((-1, 0))
			if col < self._num_cols - 1 and not self._cells[col + 1][row].visited:
				directions.append((1, 0))
			if row > 0 and not self._cells[col][row - 1].visited:
				directions.append((0, -1))
			if row < self._num_rows - 1 and not self._cells[col][row + 1].visited:
				directions.append((0, 1))

			if not directions:
				return

			dcol, drow = random.choice(directions)
			ncol, nrow = col + dcol, row + drow

			if dcol == -1:
				self._cells[col][row].has_left_wall = False
				self._cells[ncol][nrow].has_right_wall = False
			elif dcol == 1:
				self._cells[col][row].has_right_wall = False
				self._cells[ncol][nrow].has_left_wall = False
			elif drow == -1:
				self._cells[col][row].has_top_wall = False
				self._cells[ncol][nrow].has_bottom_wall = False
			elif drow == 1:
				self._cells[col][row].has_bottom_wall = False
				self._cells[ncol][nrow].has_top_wall = False

			self._break_walls_r(ncol, nrow)

	def _break_entrance_and_exit(self):
		"""Break entrance and exit walls."""
		self._cells[0][0].has_top_wall = False
		self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False

	def _reset_cells_visited(self):
		"""Reset all cells' visited status."""
		for col in self._cells:
			for cell in col:
				cell.visited = False

	def solve(self):
		"""Solve the maze starting from the top-left corner."""
		return self._solve_r(0, 0)

	def _solve_r(self, col, row):
		"""Recursive helper to solve the maze."""
		self._cells[col][row].visited = True
		if col == self._num_cols - 1 and row == self._num_rows - 1:
			return True

		directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		for dcol, drow in directions:
			ncol, nrow = col + dcol, row + drow
			if 0 <= ncol < self._num_cols and 0 <= nrow < self._num_rows and not self._cells[ncol][nrow].visited:
				if (dcol == -1 and not self._cells[col][row].has_left_wall) or \
				   (dcol == 1 and not self._cells[col][row].has_right_wall) or \
				   (drow == -1 and not self._cells[col][row].has_top_wall) or \
				   (drow == 1 and not self._cells[col][row].has_bottom_wall):
					self._cells[col][row].draw_move(self._cells[ncol][nrow])
					if self._solve_r(ncol, nrow):
						return True
					self._cells[col][row].draw_move(self._cells[ncol][nrow], undo=True)

		return False
	
	def set_animation_speed(self, speed):
		"""Set the animation speed for solving the maze."""
		self._animation_speed = speed

	def _animate(self):
		if self._win:
			self._win.redraw()
		time.sleep(self._animation_speed)