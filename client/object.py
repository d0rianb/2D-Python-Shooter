from rect import Rect

class Object:
    def __init__(self, id, type, x, y):
        self.id = id
        self.type = type
        self.x = x
        self.y = y
        self.rect = {}

    def addRect(self, id, x, y, w, h):
        #x and y are the relatives position od rectangle in object and w and h are the width and height of rectangle
        self.rect[id] = Rect(id, x, y, w, h)
        print(self.rect[id].getDimensions())

    def render(self, canvas):
        for key in self.rect:
            self.rect[key].render(self.x, self.y, canvas)
