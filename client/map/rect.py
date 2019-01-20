class Rect:
    def __init__(self, id, x, y, width, height, env):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.env = env
        self.color = '#757575'

    def getDimensions(self):
        return self.x, self.y, int(self.width), int(self.height)

    def render(self, x, y):
        real_ratio = abs(self.env.viewArea['width']/self.env.viewArea['height'] - 16/9)
        gridX = self.env.viewArea['width']/32
        gridY = self.env.viewArea['height']/(18 + real_ratio)
        self.rendered = {
            'x': (self.x + x)*gridX,
            'y': (self.y + y)*gridY,
            'width': (self.x + x + self.width)*gridX,
            'height': (self.y + y + self.height)*gridY
        }
        self.env.canvas.create_rectangle(self.rendered['x'],self.rendered['y'], self.rendered['width'], self.rendered['height'],
            fill = self.color,
            width=0)
