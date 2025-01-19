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
		win.clear_canvas()
		current_maze = Maze(50, 50, y, x, 50, 50, win, seed=seed)
		current_maze.set_animation_speed(speed)
		current_maze.solve()

	# Create the window and set up the callback
	win = Window(800, 600, initial_seed=seed)
	win.set_generate_callback(generate_maze_callback)

	# Create the initial maze
	current_maze = Maze(50, 50, y, x, 50, 50, win, seed=seed)
	current_maze.solve()

	# Start the UI loop
	win.wait_for_close()

if __name__ == "__main__":
	main()