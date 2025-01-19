class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Line:
	def __init__(self, start_point, end_point):
		self.start_point = start_point
		self.end_point = end_point

	def draw(self, canvas, fill_color):
		canvas.create_line(
			self.start_point.x, self.start_point.y,
			self.end_point.x, self.end_point.y,
			fill=fill_color, width=2
		)