#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import math
import keyboard

from PIL import Image, ImageTk
from threading import Timer
from render import RenderedObject
from weapons.weapon import AR, Shotgun, Sniper

default_keys = {
    'up': 'z',
    'down': 's',
    'left': 'q',
    'right': 'd',
    'dash': 56,
    'dash_preview': 'a',
    'reload': 'r',
    'panic': 'p'
}

def random_sign():
    sign = 0
    while sign == 0:
        sign = random.randint(-1, 1)
    return sign

class Player:
    def __init__(self, id, x, y, env, name="Invité", own=False, key=None):
        self.id = id
        self.x = x
        self.y = y
        self.env = env
        self.name = name
        self.own = own  # Si le player est le joueur
        self.weapon = Shotgun(self)
        self.client = None
        self.interface = None
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
        self.hit_player = {}
        self.hit_by_player = {}
        self.kills = []
        self.assists = []
        self.alive = True
        self.key = key or default_keys

        self.texture_dic = {}
        self.texture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ressources/texture/')
        texture_file = 'player.png' if self.own else 'enemy.png'
        self.texture = Image.open(os.path.join(self.texture_path, texture_file), mode='r')
        texture_width, texture_height = self.texture.size
        scale_factor = min(texture_width/(2*self.size), texture_height/(2*self.size))
        self.texture_image = self.texture.crop((0, 0, self.size*2*scale_factor, self.size*2*scale_factor)).resize((self.size*2, self.size*2))
        # self.tk_texture = ImageTk.PhotoImage(image=texture_image)

        if self.own:
            self.env.fen.bind('<Motion>', self.mouse_move)
            self.env.fen.bind('<Button-1>', self.shoot)
            self.env.fen.bind('<ButtonRelease-1>', self.weapon.stop_fire)
            keyboard.on_press_key(self.key['reload'], self.reload)
            # keyboard.on_press_key(self.key['panic'], self.env.panic)
            keyboard.on_press_key(self.key['dash_preview'], self.toggle_dash_preview)
            keyboard.on_press_key(self.key['dash'], self.dash)

        self.env.players.append(self)

    def mouse_move(self, event):
        self.mouse['x'], self.mouse['y'] = event.x, event.y

    def detect_keypress(self):
        x, y = 0, 0
        if keyboard.is_pressed(self.key['up']):
            y = -1
        if keyboard.is_pressed(self.key['down']):
            y = 1
        if keyboard.is_pressed(self.key['right']):
            x = 1
        if keyboard.is_pressed(self.key['left']):
            x = -1
        if keyboard.is_pressed(self.key['help']) and self.interface:
            self.interface.display_help()
        self.move(x, y)

    def check_shoot_collide(self):
        for shoot in self.env.shoots:
            dist_head = math.sqrt((self.x - shoot.head['x'])**2 + (self.y - shoot.head['y'])**2)
            dist_tail = math.sqrt((self.x - shoot.x)**2 + (self.y - shoot.y)**2)
            tolerance = 4
            if (dist_head <= self.size + tolerance or dist_tail <= self.size + tolerance) and shoot.from_player != self:
                self.health -= shoot.damage
                if self.health <= 0:
                        shoot.from_player.kills.append(self)
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
        if event:
            self.weapon.proceed_shoot(event)
        else:
            self.weapon.proceed_shoot()

    def reload(self, *event):
        self.weapon.reload(event)

    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def dead(self):
        print('{} est mort, il a tiré sur {} et s\'est fait tuer par {}'.format(self.name, self.hit_player, self.hit_by_player))
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
            self.assists = [player for player in self.hit_player.keys() if not self.env.find_by_name(player).alive]
        if self.own:
            self.detect_keypress()
        if self.client:
            self.client.send_position()
            self.client.receive()

    def render(self, dash=False):
        head_text = self.name if self.own else '{0}: {1} hp'.format(self.name, self.health)
        self.env.rendering_stack.append(RenderedObject('oval', self.x - self.size, self.y - self.size, x2=self.x + self.size, y2=self.y + self.size, color=self.color, width=0, dash=self.dash))
        # image = ImageTk.PhotoImage(image=self.texture_image)
        # self.texture_dic['0'] = image
        # self.env.rendering_stack.append(RenderedObject('image', self.x, self.y, image=image))
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
        self.name = 'Target {}'.format(self.id)
        self.own = False
        self.theorical_speed = level / 2.5
        self.weapon = AR(self)
        self.color = '#AAA'
        self.tick = 0
        self.vx = random_sign()
        self.vy = random_sign()
        self.move_interval = random.randint(20, 60)
        self.shoot_interval = random.randint(10-self.level, 200-self.level*2)
        self.closer_player = None
        self.can_shoot = self.level >= 2
        self.can_move = self.level > 2
        self.shoot_dispersion = math.pi/(5 + random.randint(self.level, self.level*2))

    def detect_closer_player(self):
        for player in self.env.players:
            if self.closer_player and player != self and player.alive:
                if self.dist(player) < self.dist(self.closer_player):
                    self.closer_player = player
            elif player != self and player.alive:
                self.closer_player = player

    def shoot(self):
        self.weapon.shoot()

    def update(self):
        if self.alive and len(self.env.players_alive) > 1:
            super().update()
            self.detect_closer_player()
            self.dir = math.atan2(self.closer_player.y - self.y, self.closer_player.x - self.x)
            if self.tick % self.move_interval == 0:
                self.vy *= random_sign()
                self.vx *= random_sign()
            if self.tick % self.shoot_interval == 0 and self.can_shoot:
                self.dir += random_sign()*random.random() * self.shoot_dispersion
                self.shoot()
            self.tick += 1
            if self.can_move:
                super().move(self.vx, self.vy)

    def render(self):
        super().render()
