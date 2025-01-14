import unittest
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_different_sizes(self):
        num_cols = 5
        num_rows = 5
        m2 = Maze(0, 0, num_rows, num_cols, 20, 20)
        self.assertEqual(len(m2._cells), num_cols)
        self.assertEqual(len(m2._cells[0]), num_rows)

        num_cols = 8
        num_rows = 3
        m3 = Maze(0, 0, num_rows, num_cols, 15, 15)
        self.assertEqual(len(m3._cells), num_cols)
        self.assertEqual(len(m3._cells[0]), num_rows)

    def test_maze_entrance_and_exit(self):
        num_cols = 10
        num_rows = 10
        m4 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m4._cells[0][0].has_top_wall)
        self.assertFalse(m4._cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_maze_break_walls(self):
        num_cols = 10
        num_rows = 10
        m5 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        visited_cells = sum(cell.visited for column in m5._cells for cell in column)
        self.assertEqual(visited_cells, num_cols * num_rows)

    def test_maze_reset_cells_visited(self):
        num_cols = 10
        num_rows = 10
        m6 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        m6._reset_cells_visited()
        visited_cells = sum(cell.visited for column in m6._cells for cell in column)
        self.assertEqual(visited_cells, 0)

    def test_maze_solve(self):
        num_cols = 10
        num_rows = 10
        m7 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        self.assertTrue(m7.solve())

if __name__ == "__main__":
    unittest.main()
