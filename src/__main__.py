import argparse
import random
from mazesolver.window import Window
from mazesolver.entities.maze import Maze

def main():
	# Parse command-line arguments
	parser = argparse.ArgumentParser(description="Maze Solver")
	parser.add_argument("--x", type=int, default=10, help="Number of columns in the maze (default: 10)")
	parser.add_argument("--y", type=int, default=10, help="Number of rows in the maze (default: 10)")
	parser.add_argument("--seed", type=int, default=None, help="Random seed for maze generation (default: random)")

	args = parser.parse_args()

	# Set up initial maze parameters
	x = args.x
	y = args.y
	seed = args.seed if args.seed is not None else random.randint(0, 100000)

	# Callback to generate a new maze from the UI
	def generate_maze_callback(new_x, new_y, speed, new_seed):
		nonlocal x, y, seed, current_maze
		x = new_x
		y = new_y
		seed = int(new_seed) if new_seed else random.randint(0, 100000)

		# Calculate cell size and window dimensions
		cell_size, window_width, window_height = calculate_dimensions(x, y)
		win.set_window_size(window_width, window_height)  # Dynamically update window size
		win.clear_canvas()

		current_maze = Maze(50, 50, y, x, win=win, seed=seed)
		current_maze.set_animation_speed(speed)
		current_maze.solve()


	# Calculate initial cell size and window dimensions
	def calculate_dimensions(num_cols, num_rows):
		max_window_width, max_window_height = 1440, 900
		default_window_width, default_window_height = 960, 600
		margin = 100  # Space for UI controls

		# Calculate optimal cell size
		cell_size_x = (max_window_width - margin) // num_cols
		cell_size_y = (max_window_height - margin) // num_rows
		cell_size = min(cell_size_x, cell_size_y)

		# Calculate window size
		window_width = min(max_window_width, cell_size * num_cols + margin)
		window_height = min(max_window_height, cell_size * num_rows + margin)

		return cell_size, window_width, window_height

	# Create the window and set up the callback
	cell_size, initial_window_width, initial_window_height = calculate_dimensions(x, y)
	win = Window(initial_window_width, initial_window_height, initial_seed=seed)
	win.set_generate_callback(generate_maze_callback)

	# Create the initial maze
	current_maze = Maze(50, 50, y, x, win=win, seed=seed)
	current_maze.solve()

	# Start the UI loop
	win.wait_for_close()

if __name__ == "__main__":
	main()