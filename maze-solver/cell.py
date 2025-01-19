from point import Line, Point

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
		"""Draw the walls of the cell based on their state."""
		if self._win:
			light_gray = "#C9C9C9"
			
			# Draw left wall
			self._win.draw_line(
				Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
				"black" if self.has_left_wall else light_gray
			)

			# Draw right wall
			self._win.draw_line(
				Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
				"black" if self.has_right_wall else light_gray
			)

			# Draw top wall
			self._win.draw_line(
				Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
				"black" if self.has_top_wall else light_gray
			)

			# Draw bottom wall
			self._win.draw_line(
				Line(Point(self._x1, self._y2), Point(self._x2, self._y2)),
				"black" if self.has_bottom_wall else light_gray
			)

	def draw_move(self, to_cell, undo=False):
		"""Draw the path between two cells during maze solving."""
		color = "gray" if undo else "red"
		from_center = ((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
		to_center = ((to_cell._x1 + to_cell._x2) // 2, (to_cell._y1 + to_cell._y2) // 2)
		if self._win:
			self._win.draw_line(Line(Point(*from_center), Point(*to_center)), color)