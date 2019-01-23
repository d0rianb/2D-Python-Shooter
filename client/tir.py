import math

class Tir:
    def __init__(self, id, x, y, dir, from_player):
        self.id = id
        self.x = x
        self.y = y
        self.dir = dir
        self.damage = 20
        self.speed = 15 * 60/from_player.env.framerate
        self.size = 12
        self.head = { 'x': x, 'y': y }
        self.from_player = from_player
        self.env = from_player.env

    def checkWallCollide(self, map):
        x = self.head['x']
        y = self.head['y']
        for rect in map.rects:
            if x >= rect.x and x <= rect.x2 and y >= rect.y and y <= rect.y2: # Check for Head
                self.env.shoots.remove(self)
            elif self.x >= rect.x and self.x <= rect.x2 and self.y >= rect.y and self.y <= rect.y2: # Check for bottom
                self.env.shoots.remove(self)


    def update(self):
        self.x += math.cos(self.dir)*self.speed
        self.y += math.sin(self.dir)*self.speed
        self.head = {
            'x': self.x + math.cos(self.dir)*self.size,
            'y': self.y + math.sin(self.dir)*self.size
        }
        self.checkWallCollide(self.env.map)

    def render(self, canvas):
        canvas.create_line(self.x, self.y, self.head['x'], self.head['y'])
