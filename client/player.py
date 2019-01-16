import random
import math
import keyboard
from tir import Tir

class Player:
    def __init__(self, x, y, env):
        self.x = x
        self.y = y
        self.env = env
        self.size = 20
        self.dir = 0 # degré °
        self.mouse = {'x': 0, 'y': 0}
        self.color = random.choice(['red', 'green', 'cyan', 'magenta'])
        self.speed = 5
        self.health = 100
        self.ammo = 10
        self.env.players.append(self)

        self.env.fen.bind('<Motion>', self.mouse_move)
        self.env.fen.bind('<Button-1>', self.shoot)
        keyboard.on_press_key(56, self.dash) # dash on shift

    def mouse_move(self, event):
        self.mouse['x'], self.mouse['y'] = event.x, event.y

    def detect_keypress(self):
        x = 0
        y = 0
        if keyboard.is_pressed('z'):
            y = -1
        if keyboard.is_pressed('s'):
            y = 1
        if keyboard.is_pressed('d'):
            x = 1
        if keyboard.is_pressed('q'):
            x = -1
        self.move(x, y)

    def move(self, x, y):
        self.x += x*self.speed
        self.y += y*self.speed

    def dash(self, *args):
        print('dash')
        for i in range(15):
            self.move(math.cos(self.dir), math.sin(self.dir))

    def shoot(self, event):
        self.env.shoots.append(Tir(len(self.env.shoots), self.x, self.y, self.dir, self))

    def update(self):
        deltaX = self.mouse['x'] - self.x if (self.x != self.mouse['x']) else 1
        deltaY = self.mouse['y'] - self.y
        self.dir = math.atan2(deltaY, deltaX)
        self.detect_keypress()

    def render(self, canvas):
        canvas.create_oval(self.x - self.size/2, self.y - self.size/2, self.x+self.size/2, self.y+self.size/2, fill=self.color, outline=self.color)
        canvas.create_line(self.x + math.cos(self.dir)*12, self.y + math.sin(self.dir)*12, self.x + math.cos(self.dir)*20, self.y + math.sin(self.dir)*20)
