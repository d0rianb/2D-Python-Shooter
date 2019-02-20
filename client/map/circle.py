class Circle:
    def __init__(self, id, x, y, radius, map):
        self.id = int(id)
        self.relative_x = float(x)
        self.relative_y = float(y)
        self.relative_radius = float(radius)
        self.map = map
        real_ratio = abs(self.map.env.viewArea['width'] / self.map.env.viewArea['height'] - 16 / 9)
        gridX = self.map.env.viewArea['width'] / 32
        gridY = self.map.env.viewArea['height'] / (18 + real_ratio)

        self.radius = self.relative_radius * gridX
        self.x = self.relative_x * gridX
        self.y = self.relative_y * gridY
        self.x1 = self.x - self.radius
        self.y1 = self.y - self.radius
        self.x2 = self.x + self.radius
        self.y2 = self.y + self.radius

        self.color = '#757575'
