import unittest
from mazesolver.entities.cell import Cell

class TestCell(unittest.TestCase):
	def test_initialization(self):
		"""Test that the cell initializes correctly with all walls."""
		cell = Cell(0, 0, 20, 20)
		self.assertTrue(cell.has_left_wall)
		self.assertTrue(cell.has_top_wall)
		self.assertTrue(cell.has_right_wall)
		self.assertTrue(cell.has_bottom_wall)
		self.assertFalse(cell.visited)

	def test_draw_move(self):
		"""Test the draw_move function."""
		# Mocking behavior would be added here if needed
		pass

if __name__ == "__main__":
	unittest.main()