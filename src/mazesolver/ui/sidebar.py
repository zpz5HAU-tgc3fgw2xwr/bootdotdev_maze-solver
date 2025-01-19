from tkinter import Frame, Label, Entry, Button, IntVar, StringVar
import random

class Sidebar:
	def __init__(self, parent, initial_seed, callback):
		self.parent = parent
		self.callback = callback

		# Frame for sidebar
		self.frame = Frame(parent, padx=10, pady=10, width=200)
		self.frame.pack(side="right", fill="y")

		# Maze size controls
		Label(self.frame, text="Maze Size (X, Y):").pack(anchor="nw", pady=(0, 5))
		self.maze_x = IntVar(value=10)
		self.maze_y = IntVar(value=10)
		self._create_increment_controls(
			"X:", self.maze_x, row=0, padx=(0, 5)
		)
		self._create_increment_controls(
			"Y:", self.maze_y, row=1, padx=(0, 5)
		)

		# Solver speed controls
		Label(self.frame, text="Solver Speed:").pack(anchor="nw", pady=(10, 0))
		self.solver_speed = IntVar(value=10)
		self._create_increment_controls(
			"Speed:", self.solver_speed, row=2, padx=(0, 5), min_value=0
		)

		# Seed controls
		Label(self.frame, text="Seed:").pack(anchor="nw", pady=(10, 0))
		self.seed = StringVar(value=str(initial_seed) if initial_seed else "")
		seed_frame = Frame(self.frame)
		seed_frame.pack(anchor="nw", pady=(0, 10))
		Entry(seed_frame, textvariable=self.seed, width=10).pack(side="left", padx=(0, 5))
		Button(seed_frame, text="Randomize", command=self._randomize_seed).pack(side="left")

		# Buttons for maze generation
		Button(self.frame, text="Regenerate Maze", command=self.regenerate_maze).pack(anchor="nw", pady=5)
		Button(self.frame, text="Generate Random", command=self.generate_random_maze).pack(anchor="nw")

	def _create_increment_controls(self, label, var, row, padx=(0, 5), min_value=1):
		"""Helper to create + and - increment buttons for a given variable."""
		frame = Frame(self.frame)
		frame.pack(anchor="nw", pady=(0, 10))
		Label(frame, text=label).pack(side="left", padx=padx)
		Button(frame, text="-", command=lambda: self._decrement(var, min_value)).pack(side="left")
		Entry(frame, textvariable=var, width=5, justify="center").pack(side="left", padx=(5, 5))
		Button(frame, text="+", command=lambda: self._increment(var)).pack(side="left")

	def _increment(self, var):
		"""Increment the value of an IntVar."""
		var.set(var.get() + 1)

	def _decrement(self, var, min_value):
		"""Decrement the value of an IntVar, ensuring it doesn't go below min_value."""
		if var.get() > min_value:
			var.set(var.get() - 1)

	def _randomize_seed(self):
		"""Randomize the seed value."""
		self.seed.set(str(random.randint(0, 100000)))

	def regenerate_maze(self):
		"""Regenerate the maze with current settings."""
		self.callback(
			self.maze_x.get(),
			self.maze_y.get(),
			self.solver_speed.get(),
			self.seed.get() or None
		)

	def generate_random_maze(self):
		"""Randomize the seed and regenerate the maze."""
		self._randomize_seed()
		self.regenerate_maze()