class Rect:
    def __init__(self, id, x, y, width, height):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.color = "black"

    def getDimensions(self):
        return (self.x, self.y, int(self.width), int(self.height))

    def render(self, x, y, canvas):
        canvas.create_rectangle(self.x + int(x), self.y + int(y), self.x + int(x) + self.width, self.y + int(y) + self.height,
            fill = self.color,
            width=0)
