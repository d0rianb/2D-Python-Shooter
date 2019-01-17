from map.rect import Rect

class Object:
    def __init__(self, id, type, x, y):
        self.id = id
        self.type = type
        self.x = int(x)
        self.y = int(y)
        self.rect = {}

    def addRect(self, id, x, y, width, height):
        # x and y are the relatives position od rectangle in object and width and height are the width and height of rectangle
        self.rect[id] = Rect(id, x, y, width, height)
        print(self.rect[id].getDimensions())

    def render(self, env):
        for key in self.rect:
            self.rect[key].render(self.x, self.y, env)
