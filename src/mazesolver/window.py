from tkinter import Tk, BOTH, Canvas
from mazesolver.ui.sidebar import Sidebar

class Window:
	def __init__(self, width, height, initial_seed=None):
		self.__root = Tk()
		self.__root.title("Maze Solver")
		self.__root.geometry(f"{width}x{height}")
		self.current_width = width
		self.current_height = height

		# Canvas for maze drawing
		self.__canvas = Canvas(self.__root, bg="white")
		self.__canvas.pack(side="left", fill=BOTH, expand=True)

		# Sidebar for controls
		self.__sidebar = Sidebar(self.__root, initial_seed, self._generate_maze)

		# Internal variables for event handling
		self.__running = False
		self.__root.protocol("WM_DELETE_WINDOW", self.close)

	def redraw(self):
		"""Redraw the tkinter UI."""
		self.__root.update_idletasks()
		self.__root.update()

	def wait_for_close(self):
		"""Wait for the user to close the window."""
		self.__running = True
		while self.__running:
			self.redraw()

	def close(self):
		"""Close the window."""
		self.__running = False

	def draw_line(self, line, fill_color):
		"""Draw a line on the canvas."""
		self.__canvas.create_line(
			line.start_point.x, line.start_point.y,
			line.end_point.x, line.end_point.y,
			fill=fill_color, width=2
		)

	def clear_canvas(self):
		"""Clear the canvas."""
		self.__canvas.delete("all")

	def _generate_maze(self, x, y, speed, seed):
		"""Callback for generating a maze from the sidebar."""
		if self.generate_callback:
			self.generate_callback(x, y, speed, seed)

	def set_solver_speed_callback(self, callback):
		"""Set the callback for solver speed changes."""
		self.solver_speed_callback = callback

	def update_solver_speed(self, speed):
		"""Update the solver speed dynamically."""
		if self.solver_speed_callback:
			self.solver_speed_callback(speed)
	def set_generate_callback(self, callback):
		"""Set the callback for maze generation."""
		self.generate_callback = callback

	def set_window_size(self, width, height):
		"""Set the size of the window dynamically."""
		self.current_width = width
		self.current_height = height
		self.__root.geometry(f"{width}x{height}")