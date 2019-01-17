import math

class Tir:
    def __init__(self, id, x, y, dir, from_player):
        self.id = id
        self.x = x
        self.y = y
        self.dir = dir
        self.damage = 10
        self.speed = 15 * 60/from_player.env.framerate
        self.size = 12
        self.head = { 'x': x, 'y': y }
        self.from_player = from_player

    def update(self):
        self.x += math.cos(self.dir)*self.speed
        self.y += math.sin(self.dir)*self.speed
        self.head = {
            'x': self.x + math.cos(self.dir)*self.size,
            'y': self.y + math.sin(self.dir)*self.size
        }

    def render(self, canvas):
        canvas.create_line(self.x, self.y, self.head['x'], self.head['y'])
