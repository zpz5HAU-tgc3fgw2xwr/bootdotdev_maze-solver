import unittest
from maze_solver.maze import Maze

class TestMaze(unittest.TestCase):
    def test_create_cells(self):
        maze = Maze(0, 0, 10, 10, 20, 20)
        self.assertEqual(len(maze._cells), 10)
        self.assertEqual(len(maze._cells[0]), 10)

    def test_break_walls(self):
        maze = Maze(0, 0, 5, 5, 20, 20, seed=0)
        visited_cells = sum(cell.visited for column in maze._cells for cell in column)
        self.assertEqual(visited_cells, 0)

    def test_entrance_exit(self):
        maze = Maze(0, 0, 5, 5, 20, 20)
        self.assertFalse(maze._cells[0][0].has_top_wall)
        self.assertFalse(maze._cells[-1][-1].has_bottom_wall)

    def test_solve(self):
        maze = Maze(0, 0, 5, 5, 20, 20, seed=0)
        self.assertTrue(maze.solve())