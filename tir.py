import math

class Tir:
    def __init__(self, x, y, dir, damage, speed, from_):
        self.x = x
        self.y = y
        self.dir = dir
        self.damage = damage
        self.speed = speed
        self.from_ = from_

    def update(self):
        self.x += math.cos(self.dir)*self.speed
        self.y += math.sin(self.dir)*self.speed

    def render(self, canvas):
        canvas.create_line(self.x, self.y, self.x + math.cos(self.dir)*12, self.y + math.sin(self.dir)*12)
