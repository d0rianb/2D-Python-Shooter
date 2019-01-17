

class Rect:
    def __init__(self, id, x, y, w, h):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.color = "black"

    def getDimensions(self):
        return (self.x, self.y, self.w, self.h)

    def render(self, x, y, canvas):
        #render rectange
        canvas.create_rectangle(self.x + int(x), self.y + int(y), self.x + int(x) + self.w, self.y + int(y) + self.h, fill = self.color, outline = self.color)
