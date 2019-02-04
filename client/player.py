#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import math
import keyboard
from threading import Timer
from render import RenderedObject
from tir import Tir

def random_sign():
    sign = 0
    while sign == 0:
        sign = random.randint(-1, 1)
    return sign

class Player:
    def __init__(self, id, x, y, env, name="Invité", own=False):
        self.id = id
        self.x = x
        self.y = y
        self.env = env
        self.name = name
        self.own = own  # Si le player est le joueur
        self.client = None
        self.size = 10  # Radius
        self.dir = 0  # angle
        self.mouse = {'x': 0, 'y': 0}
        self.color = '#0066ff' if self.own else random.choice(['#cc6600', '#ff9900', '#ff3300'])
        self.theorical_speed = 4.2
        self.speed = self.theorical_speed * 60 / self.env.framerate   # computed value
        self.dash_length = 32
        self.dash_preview = False
        self.simul_dash = {'x': 0, 'y': 0}
        self.dash_left = 3
        self.health = 100
        self.max_ammo = 20  # Taille du chargeur
        self.ammo = self.max_ammo  # Munitions restantes
        self.is_reloading = False
        self.autofire = False
        self.hit_player = {}
        self.hit_by_player = {}
        self.alive = True
        self.env.players.append(self)

        if self.own:
            self.env.fen.bind('<Motion>', self.mouse_move)
            self.env.fen.bind('<Button-1>', self.shoot)
            self.env.fen.bind('<ButtonRelease-1>', self.stop_fire)
            keyboard.on_press_key('r', self.reload)
            # keyboard.on_press_key('p', self.env.panic)
            keyboard.on_press_key('a', self.toggle_dash_preview)
            if self.env.isMac():
                keyboard.on_press_key(56, self.dash)   # dash on shift 56
            elif self.env.isWindows():
                keyboard.on_press_key('shift', self.dash) # dash on windows

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

    def check_shoot_collide(self):
        for shoot in self.env.shoots:
            dist_head = math.sqrt((self.x - shoot.head['x'])**2 + (self.y - shoot.head['y'])**2)
            dist_tail = math.sqrt((self.x - shoot.x)**2 + (self.y - shoot.y)**2)
            if (dist_head <= self.size + 1 or dist_tail <= self.size + 1) and shoot.from_player != self:
                self.health -= shoot.damage
                if shoot.from_player.name in self.hit_by_player:
                    self.hit_by_player[shoot.from_player.name] += shoot.damage
                else:
                    self.hit_by_player[shoot.from_player.name] = shoot.damage
                if self.name in shoot.from_player.hit_player:
                    shoot.from_player.hit_player[self.name] += shoot.damage
                else:
                    shoot.from_player.hit_player[self.name] = shoot.damage
                self.env.shoots.remove(shoot)
        if self.health <= 0:
            self.dead()

    def is_colliding_wall(self):
        rects = self.env.map.rects
        collide_wall = False
        for rect in rects:
            if self.x + self.size >= rect.x and self.x - self.size <= rect.x2 and self.y + self.size >= rect.y and self.y - self.size <= rect.y2:
                collide_wall = True
        if self.env.debug:
            self.color = 'red' if collide_wall else 'green'
        return collide_wall

    def simul_is_colliding_wall(self):
        rects = self.env.map.rects
        collide_wall = False
        for rect in rects:
            if self.simul_dash['x'] + self.size >= rect.x and self.simul_dash['x'] - self.size <= rect.x2 and self.simul_dash['y'] + self.size >= rect.y and self.simul_dash['y'] - self.size <= rect.y2:
                collide_wall = True
        if self.env.debug:
            self.color = 'red' if collide_wall else 'green'
        return collide_wall

    def move(self, x, y):
        old_x, old_y = self.x, self.y

        self.x += x * self.speed
        if self.is_colliding_wall():
            self.x = old_x

        self.y += y * self.speed
        if self.is_colliding_wall():
            self.y = old_y

        # Restreint le joueur à l'environnement
        if self.x - self.size <= 0:
            self.x = self.size
        elif self.x + self.size >= self.env.width:
            self.x = self.env.width - self.size
        if self.y - self.size <= 0:
            self.y = self.size
        elif self.y + self.size >= self.env.height:
            self.y = self.env.height - self.size

    def simul_move(self, x, y):
        old_x, old_y = self.simul_dash['x'], self.simul_dash['y']

        self.simul_dash['x'] += x * self.theorical_speed
        if self.simul_is_colliding_wall():
            self.simul_dash['x'] = old_x

        self.simul_dash['y'] += y * self.theorical_speed
        if self.simul_is_colliding_wall():
            self.simul_dash['y'] = old_y

        # Restreint le joueur à l'environnement
        if self.simul_dash['x'] - self.size <= 0:
            self.simul_dash['x'] = self.size
        elif self.simul_dash['x'] + self.size >= self.env.width:
            self.simul_dash['x'] = self.env.width - self.size
        if self.simul_dash['y'] - self.size <= 0:
            self.simul_dash['y'] = self.size
        elif self.simul_dash['y'] + self.size >= self.env.height:
            self.simul_dash['y'] = self.env.height - self.size

    def dash(self, *args):
        if self.dash_left > 0:
            for i in range(self.dash_length):
                self.speed = self.theorical_speed
                self.move(math.cos(self.dir), math.sin(self.dir))
                self.render(dash=True)
            self.dash_left -= 1
            cooldown = Timer(3, self.new_dash)
            cooldown.start()

    def new_dash(self):
        if self.dash_left < 3:
            self.dash_left += 1

    def toggle_dash_preview(self, *event):
        self.dash_preview = not self.dash_preview

    def update_dash_preview(self):
        self.simul_dash['x'], self.simul_dash['y'] = self.x, self.y
        for i in range(self.dash_length):
            self.simul_move(math.cos(self.dir), math.sin(self.dir))

    def shoot(self, *event):
        if self.ammo > 0 and not self.is_reloading:
            if event:
                self.autofire = True
                self.shoot()
            if self.autofire and not event:
                tir = Tir(len(self.env.shoots), self.x, self.y, self.dir, self)
                self.env.shoots.append(tir)
                self.ammo -= 1
                Timer(.2, self.shoot).start()
        else:
            self.reload()

    def stop_fire(self, *event):
        self.autofire = False

    def reload(self, *arg):
        if self.ammo < self.max_ammo:
            self.is_reloading = True
            Timer(1, self.has_reload).start()

    def has_reload(self):
        self.ammo = self.max_ammo
        self.is_reloading = False
        if self.autofire:
            self.shoot()

    def passif(self):
        pass  # dash regain and healt regain

    def dead(self):
        self.alive = False

    def update(self):
        deltaX = self.mouse['x'] - self.x if (self.x != self.mouse['x']) else 1
        deltaY = self.mouse['y'] - self.y
        self.dir = math.atan2(deltaY, deltaX)
        self.speed = self.theorical_speed * 60 / self.env.framerate
        if self.dash_preview:
            self.update_dash_preview()
        if self.alive:
            self.check_shoot_collide()
        if self.own:
            self.detect_keypress()
        if self.client:
            self.client.send_position()
            self.client.receive()

    def render(self, dash=False):
        head_text = self.name if self.own else '{0}: {1} hp'.format(self.name, self.health)
        self.env.rendering_stack.append(RenderedObject('oval', self.x - self.size, self.y - self.size, x2=self.x + self.size, y2=self.y + self.size, color=self.color, width=0, dash=self.dash))
        if not dash:
            self.env.rendering_stack.append(RenderedObject('line', self.x + math.cos(self.dir) * 12, self.y + math.sin(self.dir) * 12, x2=self.x + math.cos(self.dir) * 20, y2=self.y + math.sin(self.dir) * 20, zIndex=2))
            self.env.rendering_stack.append(RenderedObject('text', self.x - len(self.name) / 2, self.y - 20, text=head_text, color='#787878', zIndex=3))
            if self.dash_preview:
                preview_size = self.size
                self.env.rendering_stack.append(RenderedObject('oval', self.simul_dash['x'] - preview_size, self.simul_dash['y'] - preview_size, x2=self.simul_dash['x'] + preview_size, y2=self.simul_dash['y'] + preview_size, color='#ccc'))


class Target(Player):
    def __init__(self, id, x, y, env, level=5):
        super().__init__(id, x, y, env, name="Target", own=False)
        self.id = id
        self.x = x
        self.y = y
        self.env = env
        self.level = level
        self.name = 'Target ' + str(self.id)
        self.own = False
        self.theorical_speed = level / 2.5
        self.color = '#AAA'
        self.tick = 0
        self.vx = random_sign()
        self.vy = random_sign()
        self.interval = random.randint(20, 60)
        self.shoot = self.level > 5

    def update(self):
        super().update()
        if (self.tick == self.interval):
            self.vy *= random_sign()
            self.vx *= random_sign()
            self.tick = 0
        self.tick += 1
        super().move(self.vx, self.vy)

    def render(self):
        super().render()
