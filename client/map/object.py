from map.rect import Rect

class Object:
    def __init__(self, id, type, x, y, env):
        self.id = id
        self.type = type
        self.x = int(x)
        self.y = int(y)
        self.env = env
        self.rects = {}

    def addRect(self, id, x, y, width, height):
        # x and y are the relatives position od rectangle in object and width and height are the width and height of rectangle
        self.rects[id] = Rect(id, x, y, width, height, self.env)

    def render(self, env):
        for key in self.rects:
            self.rects[key].render(self.x, self.y)
