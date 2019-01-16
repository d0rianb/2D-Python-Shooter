import random
import math
from tir import Tir

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.dir = 0 # degré °
        self.color = random.choice(['red', 'green', 'cyan', 'magenta'])
        self.speed = 5
        self.health = 100
        self.ammo = 10

    def move(self, x, y):
        self.x += x*self.speed
        self.y += y*self.speed


    def dash(self, *args):
        print('dash')
        for i in range(15):
            self.move(math.cos(self.dir), math.sin(self.dir))

    def shoot(self):
        tir = Tir(self.x, self.y, self.dir, 10, 15, self)
        return tir

    def update(self, mouse):
        deltaX = mouse['x'] - self.x if (self.x != mouse['x']) else 1
        deltaY = mouse['y'] - self.y
        self.dir = math.atan2(deltaY, deltaX)

    def render(self, canvas):
        canvas.create_oval(self.x - self.size/2, self.y - self.size/2, self.x+self.size/2, self.y+self.size/2, fill=self.color, outline=self.color)
        canvas.create_line(self.x + math.cos(self.dir)*12, self.y + math.sin(self.dir)*12, self.x + math.cos(self.dir)*20, self.y + math.sin(self.dir)*20)
