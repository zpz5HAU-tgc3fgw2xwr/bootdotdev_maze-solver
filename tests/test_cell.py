import unittest
from maze_solver.cell import Cell

class TestCell(unittest.TestCase):
    def test_initialization(self):
        cell = Cell(0, 0, 20, 20)
        self.assertTrue(cell.has_left_wall)
        self.assertTrue(cell.has_top_wall)
        self.assertFalse(cell.visited)

    def test_draw_move(self):
        # Mocked window for testing draw behavior
        pass  # Add as needed, based on test requirements