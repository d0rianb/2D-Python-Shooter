import random
import math
import keyboard
from tir import Tir

class Player:
    def __init__(self,id, x, y, env, name="Invité", own=False):
        self.id = id
        self.x = x
        self.y = y
        self.env = env
        self.name = name
        self.own = own  # Si le player est le joueur
        self.size = 20
        self.dir = 0  # angle
        self.mouse = {'x': 0, 'y': 0}
        self.color = random.choice(['green', 'cyan', 'magenta'])
        self.speed = 5 * 60/self.env.framerate
        self.health = 100
        self.ammo = 10
        self.alive = True
        self.env.players.append(self)

        if self.own:
            self.env.fen.bind('<Motion>', self.mouse_move)
            self.env.fen.bind('<Button-1>', self.shoot)
            keyboard.on_press_key(56, self.dash) # dash on shift

    def mouse_move(self, event):
        self.mouse['x'], self.mouse['y'] = event.x, event.y

    def detect_keypress(self):
        x, y = 0, 0
        if keyboard.is_pressed('z') or keyboard.is_pressed('up'):
            y = -1
        if keyboard.is_pressed('s') or keyboard.is_pressed('down'):
            y = 1
        if keyboard.is_pressed('d') or keyboard.is_pressed('right'):
            x = 1
        if keyboard.is_pressed('q') or keyboard.is_pressed('left'):
            x = -1
        self.move(x, y)

    def check_collide(self):
        for shoot in self.env.shoots:
            if abs(self.x - shoot.x - math.cos(shoot.dir)*shoot.size) < self.size and abs(self.y - shoot.y - math.sin(shoot.dir)*shoot.size) and shoot.from_player != self:
                self.health -= shoot.damage
                self.hit = not self.hit
                self.env.shoots.remove(shoot)
        if self.health <= 0:
            self.dead()

    def move(self, x, y):
        self.x += x*self.speed
        self.y += y*self.speed
        if self.x - self.size/2 <= 0:                 self.x = self.size/2
        elif self.x + self.size/2 >= self.env.width:  self.x = self.env.width - self.size/2
        if self.y - self.size/2 <= 0:                 self.y = self.size/2
        elif self.y + self.size/2 >= self.env.height: self.y = self.env.height - self.size/2

    def dash(self, *args):
        for i in range(15):
            self.move(math.cos(self.dir), math.sin(self.dir))

    def shoot(self, event):
        if self.ammo >= 0:
            self.env.shoots.append(Tir(len(self.env.shoots), self.x, self.y, self.dir, self))
        else:
            self.reload()

    def reload(self):
        # Timeout
        pass

    def dead(self):
        self.alive = False

    def update(self):
        deltaX = self.mouse['x'] - self.x if (self.x != self.mouse['x']) else 1
        deltaY = self.mouse['y'] - self.y
        self.dir = math.atan2(deltaY, deltaX)
        self.check_collide()
        if (self.own):
            self.detect_keypress()

    def render(self, canvas):
        canvas.create_oval(self.x - self.size/2, self.y - self.size/2, self.x+self.size/2, self.y+self.size/2, fill=self.color, outline=self.color)
        canvas.create_line(self.x + math.cos(self.dir)*12, self.y + math.sin(self.dir)*12, self.x + math.cos(self.dir)*20, self.y + math.sin(self.dir)*20)
        canvas.create_text(self.x - len(self.name) / 2, self.y - 20, text=self.name, fill='#787878')
