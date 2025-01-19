from tkinter import Tk, BOTH, Canvas, Frame, Label, Entry, Button, IntVar, StringVar, ttk
import random

class Window:
	def __init__(self, width, height, initial_seed=None):
		self.__root = Tk()
		self.__root.title("Maze Solver")
		self.__root.geometry(f"{width}x{height}")

		# Canvas for maze drawing
		self.__canvas = Canvas(self.__root, bg="white")
		self.__canvas.pack(side="left", fill=BOTH, expand=True)

		# Sidebar for controls
		self.__controls = Frame(self.__root, padx=10, pady=10)
		self.__controls.pack(side="right", fill="y")

		# Maze size controls
		Label(self.__controls, text="Maze Size (X, Y):").pack(anchor="ne", pady=(0, 5))
		self.maze_x = IntVar(value=10)
		self.maze_y = IntVar(value=10)

		maze_size_frame = Frame(self.__controls)
		maze_size_frame.pack(anchor="ne", pady=(0, 10))

		# Maze X size controls
		x_frame = Frame(maze_size_frame)
		x_frame.pack(side="top", fill="x", pady=(0, 5))
		Entry(x_frame, textvariable=self.maze_x, width=5, justify="center").pack(side="left", padx=(0, 5))
		Button(x_frame, text="+", command=lambda: self.__increment(self.maze_x), width=2, height=1).pack(side="top", padx=(0, 5))
		Button(x_frame, text="-", command=lambda: self.__decrement(self.maze_x), width=2, height=1).pack(side="bottom")

		# Maze Y size controls
		y_frame = Frame(maze_size_frame)
		y_frame.pack(side="top", fill="x", pady=(0, 5))
		Entry(y_frame, textvariable=self.maze_y, width=5, justify="center").pack(side="left", padx=(0, 5))
		Button(y_frame, text="+", command=lambda: self.__increment(self.maze_y), width=2, height=1).pack(side="top", padx=(0, 5))
		Button(y_frame, text="-", command=lambda: self.__decrement(self.maze_y), width=2, height=1).pack(side="bottom")

		# Speed control
		Label(self.__controls, text="Solver Speed:").pack(anchor="ne", pady=(10, 0))
		self.solver_speed = IntVar(value=10)
		Entry(self.__controls, textvariable=self.solver_speed, width=5, justify="center").pack(anchor="ne", pady=(0, 10))

		# Seed controls
		Label(self.__controls, text="Seed:").pack(anchor="ne")
		self.seed = StringVar(value=str(initial_seed) if initial_seed is not None else "")
		seed_frame = Frame(self.__controls)
		seed_frame.pack(anchor="ne", pady=(0, 10))
		Entry(seed_frame, textvariable=self.seed, width=10, justify="center").pack(side="left", padx=(0, 5))
		Button(seed_frame, text="Randomize", command=self.randomize_seed).pack(side="left")

		# Generate buttons
		ttk.Separator(self.__controls, orient="horizontal").pack(fill="x", pady=5)
		Button(self.__controls, text="Regenerate Maze", command=self.regenerate_maze).pack(anchor="ne", pady=2)
		Button(self.__controls, text="Generate Random", command=self.generate_random_maze).pack(anchor="ne")

		# Internal variables for event handling
		self.__running = False
		self.__root.protocol("WM_DELETE_WINDOW", self.close)
		self.generate_callback = None

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

	def randomize_seed(self):
		"""Set a random seed value."""
		self.seed.set(str(random.randint(0, 100000)))

	def regenerate_maze(self):
		"""Regenerate the maze with the current settings."""
		if self.generate_callback:
			self.generate_callback(
				self.maze_x.get(),
				self.maze_y.get(),
				self.solver_speed.get(),
				self.seed.get() or None
			)

	def generate_random_maze(self):
		"""Generate a random maze by randomizing the seed and regenerating the maze."""
		self.randomize_seed()
		self.regenerate_maze()

	def set_generate_callback(self, callback):
		"""Set the callback for the Generate Maze button."""
		self.generate_callback = callback

	def __increment(self, var):
		"""Increment the value of an IntVar."""
		var.set(var.get() + 1)

	def __decrement(self, var):
		"""Decrement the value of an IntVar."""
		if var.get() > 1:  # Prevent values less than 1
			var.set(var.get() - 1)

	def __validate_int(self, value):
		"""Validate that a string represents a non-negative integer."""
		if value == "":
			return True  # Allow empty input
		try:
			return int(value) >= 0
		except ValueError:
			return False