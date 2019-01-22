import random
import math
import keyboard
from threading import Timer
from tir import Tir

class Player:
    def __init__(self, id, x, y, env, name="Invité", own=False):
        self.id = id
        self.x = x
        self.y = y
        self.env = env
        self.name = name
        self.own = own  # Si le player est le joueur
        self.size = 10
        self.dir = 0  # angle
        self.mouse = {'x': 0, 'y': 0}
        self.color = random.choice(['green', 'cyan', 'magenta'])
        self.speed = 4.5 * 60/self.env.framerate
        self.dash_length = 15
        self.dash_left = 3
        self.health = 100
        self.max_ammo = 20 # Taille du chargeur
        self.ammo = self.max_ammo # Munitions restantes
        self.is_reloading = False
        self.alive = True
        self.env.players.append(self)

        if self.own:
            self.env.fen.bind('<Motion>', self.mouse_move)
            self.env.fen.bind('<Button-1>', self.shoot)
            self.env.fen.bind('<Key-r>', self.reload)
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
            dist_head = math.sqrt((self.x - shoot.head['x'])**2 + (self.y - shoot.head['y'])**2)
            dist_tail = math.sqrt((self.x - shoot.x)**2 + (self.y - shoot.y)**2)
            if (dist_head <= self.size + 1 or dist_tail <= self.size + 1) and shoot.from_player != self:
                self.health -= shoot.damage
                self.env.shoots.remove(shoot)
        if self.health <= 0:
            self.dead()

    def is_colliding_wall(self):
        ## Détecte les murs
        rects = self.env.map.rects
        collide_wall = False
        for rect in rects:
            if self.x + self.size >= rect.x and self.x - self.size <= rect.x2 and self.y + self.size >= rect.y and self.y - self.size <= rect.y2:
                collide_wall = True
                break

        self.color = 'red' if collide_wall else 'green'
        return collide_wall

    def move(self, x, y):
        old_x, old_y = self.x, self.y

        self.x += x*self.speed
        if self.is_colliding_wall():
            self.x = old_x

        self.y += y*self.speed
        if self.is_colliding_wall():
            self.y = old_y

        ## Restreint le joueur à l'environnement
        if self.x - self.size <= 0:
            self.x = self.size
        elif self.x + self.size >= self.env.width:
            self.x = self.env.width - self.size
        if self.y - self.size <= 0:
            self.y = self.size
        elif self.y + self.size >= self.env.height:
            self.y = self.env.height - self.size



    def dash(self, *args):
        if self.dash_left > 0:
            for i in range(self.dash_length):
                self.move(math.cos(self.dir), math.sin(self.dir))
                self.render(dash=True)
            self.dash_left -= 1
            cooldown = Timer(3, self.new_dash)
            cooldown.start()

    def new_dash(self):
        if self.dash_left < 3:
            self.dash_left += 1

    def shoot(self, event):
        if self.ammo > 0 and not self.is_reloading:
            tir = Tir(len(self.env.shoots), self.x, self.y, self.dir, self)
            self.env.shoots.append(tir)
            self.ammo -= 1
        else:
            self.reload()

    def reload(self, *arg):
        self.is_reloading = True
        Timer(1, self.has_reload).start()

    def has_reload(self):
        self.ammo = self.max_ammo
        self.is_reloading = False

    def passif(self):
        pass # dash regain and healt regain

    def dead(self):
        self.alive = False

    def update(self):
        deltaX = self.mouse['x'] - self.x if (self.x != self.mouse['x']) else 1
        deltaY = self.mouse['y'] - self.y
        self.dir = math.atan2(deltaY, deltaX)
        if self.alive:
            self.check_collide()
        if self.own:
            self.detect_keypress()

    def render(self, dash=False):
        head_text = self.name if self.own else '{0}: {1} hp'.format(self.name, self.health)
        self.env.canvas.create_oval(self.x - self.size, self.y - self.size, self.x+self.size, self.y+self.size, fill=self.color, width=0)
        if not dash:
            self.env.canvas.create_line(self.x + math.cos(self.dir)*12, self.y + math.sin(self.dir)*12, self.x + math.cos(self.dir)*20, self.y + math.sin(self.dir)*20)
            self.env.canvas.create_text(self.x - len(self.name) / 2, self.y - 20, text=head_text, fill='#787878')
