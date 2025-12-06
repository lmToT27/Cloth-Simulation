import math

class point_t:
    def __init__(self, x, y, pinned = False):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.pinned = pinned
        self.mass = 1.0

class line_t:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.length = math.hypot(point1.x - point2.x, point1.y - point2.y)
