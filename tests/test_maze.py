import unittest
from mazesolver.entities.maze import Maze

class TestMaze(unittest.TestCase):
	def test_create_cells(self):
		"""Test that the maze initializes with the correct number of cells."""
		maze = Maze(0, 0, 10, 10, 20, 20)
		self.assertEqual(len(maze._cells), 10)  # 10 columns
		self.assertEqual(len(maze._cells[0]), 10)  # 10 rows

	def test_break_walls(self):
		"""Test that walls are correctly broken during maze generation."""
		maze = Maze(0, 0, 5, 5, 20, 20, seed=0)
		visited_cells = sum(cell.visited for column in maze._cells for cell in column)
		self.assertEqual(visited_cells, 0)

	def test_entrance_exit(self):
		"""Test that the maze has correct entrance and exit points."""
		maze = Maze(0, 0, 5, 5, 20, 20)
		self.assertFalse(maze._cells[0][0].has_top_wall)  # Entrance
		self.assertFalse(maze._cells[-1][-1].has_bottom_wall)  # Exit

	def test_solve(self):
		"""Test that the maze is solvable."""
		maze = Maze(0, 0, 5, 5, 20, 20, seed=0)
		self.assertTrue(maze.solve())

if __name__ == "__main__":
	unittest.main()