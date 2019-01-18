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
        real_ratio = abs(env.width/env.height - 16/9)
        gridX = env.width/32
        gridY = env.height/(18 + real_ratio)
        env.canvas.create_rectangle((self.x + x)*gridX, (self.y + y)*gridY, (self.x + x + self.width)*gridX, (self.y + y + self.height)*gridY,
            fill = self.color,
            width=0)
