from tkinter import Frame, Label, Entry, Button, IntVar, StringVar, ttk
import random

class Sidebar(Frame):
	def __init__(self, root, initial_seed, callback):
		super().__init__(root, padx=10, pady=10, width=200)
		self.pack(side="right", fill="y")
		
		self.callback = callback

		# Maze size controls
		Label(self, text="Maze Size (X, Y):").pack(anchor="ne", pady=(0, 5))
		self.maze_x = IntVar(value=10)
		self.maze_y = IntVar(value=10)
		self._create_size_controls()

		# Speed control
		Label(self, text="Solver Speed:").pack(anchor="ne", pady=(10, 0))
		self.solver_speed = IntVar(value=10)
		Entry(self, textvariable=self.solver_speed, width=5, justify="center").pack(anchor="ne", pady=(0, 10))

		# Seed controls
		Label(self, text="Seed:").pack(anchor="ne")
		self.seed = StringVar(value=str(initial_seed) if initial_seed is not None else "")
		self._create_seed_controls()

		# Generate buttons
		ttk.Separator(self, orient="horizontal").pack(fill="x", pady=5)
		Button(self, text="Regenerate Maze", command=self.regenerate_maze).pack(anchor="ne", pady=2)
		Button(self, text="Generate Random", command=self.generate_random_maze).pack(anchor="ne")

	def _create_size_controls(self):
		"""Create UI controls for maze size."""
		maze_size_frame = Frame(self)
		maze_size_frame.pack(anchor="ne", pady=(0, 10))

		# Maze X controls
		x_frame = Frame(maze_size_frame)
		x_frame.pack(side="top", fill="x", pady=(0, 5))
		Button(x_frame, text="-", command=lambda: self._decrement(self.maze_x), width=2).pack(side="left", padx=(0, 5))
		Entry(x_frame, textvariable=self.maze_x, width=5, justify="center").pack(side="left", padx=(0, 5))
		Button(x_frame, text="+", command=lambda: self._increment(self.maze_x), width=2).pack(side="left", padx=(0, 5))

		# Maze Y controls
		y_frame = Frame(maze_size_frame)
		y_frame.pack(side="top", fill="x", pady=(0, 5))
		Button(y_frame, text="-", command=lambda: self._decrement(self.maze_y), width=2).pack(side="left", padx=(0, 5))
		Entry(y_frame, textvariable=self.maze_y, width=5, justify="center").pack(side="left", padx=(0, 5))
		Button(y_frame, text="+", command=lambda: self._increment(self.maze_y), width=2).pack(side="left", padx=(0, 5))

	def _create_seed_controls(self):
		"""Create UI controls for seed management."""
		seed_frame = Frame(self)
		seed_frame.pack(anchor="ne", pady=(0, 10))
		Entry(seed_frame, textvariable=self.seed, width=10, justify="center").pack(side="left", padx=(0, 5))
		Button(seed_frame, text="Randomize", command=self._randomize_seed).pack(side="left")

	def _increment(self, var):
		"""Increment the value of an IntVar."""
		var.set(var.get() + 1)

	def _decrement(self, var):
		"""Decrement the value of an IntVar."""
		if var.get() > 1:  # Prevent values less than 1
			var.set(var.get() - 1)

	def _randomize_seed(self):
		"""Set a random seed value."""
		self.seed.set(str(random.randint(0, 100000)))

	def regenerate_maze(self):
		"""Regenerate the maze with the current settings."""
		self.callback(
			self.maze_x.get(),
			self.maze_y.get(),
			self.solver_speed.get(),
			self.seed.get() or None
		)

	def generate_random_maze(self):
		"""Generate a random maze by randomizing the seed and regenerating the maze."""
		self._randomize_seed()
		self.regenerate_maze()