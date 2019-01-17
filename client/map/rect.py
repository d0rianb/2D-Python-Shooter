class Rect:
    def __init__(self, id, x, y, width, height):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.color = '#757575'

    def getDimensions(self):
        return self.x, self.y, int(self.width), int(self.height)

    def render(self, x, y, env):
        env.canvas.create_rectangle((self.x + x)*env.width/100, (self.y + y)*env.height/100, (self.x + x + self.width)*env.width/100, (self.y + y + self.height)*env.height/100,
            fill = self.color,
            width=0)
