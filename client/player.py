#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import math
import keyboard
import time
import threading
import pygame.mixer as mixer

from threading import Timer
from render import RenderedObject
from interface import TempMessage, DamageMessage
from event import Event
from sound import Sound
from object.rect import Rect, Box
from object.circle import Circle
from weapons.weapon import AR, Shotgun, Sniper, SMG, Beam
from weapons.melee import MeleeAttack

default_keys = {
    'up': 'z',
    'down': 's',
    'left': 'q',
    'right': 'd',
    'dash': 56,
    'dash_preview': 'a',
    'reload': 'r',
    'panic': 'p',
    'melee': 'e',
    'help': 'h'
}
SOUND_PATH = 'ressources/sound/'
target_name = ['Goebbels', 'Charlotte', 'Lénine', 'Klechkovski', 'Kevin', 'Pol Pot', 'Al Kartraz', 'Ben Laden', 'Jbzz', 'Fukushima', 'Karamazov', 'Jésus', 'Bill', 'Shoshana']
display_pointer = False

def random_sign():
    sign = 0
    while sign == 0:
        sign = random.randint(-1, 1)
    return sign

class Player:
    def __init__(self, id, x, y, env, name="Invité", role='A', own=False):
        self.id = id
        self.x = x
        self.y = y
        self.env = env
        self.name = name
        self.own = own  # if the  instance is the player
        self.size = 10  # Radius
        self.dir = 0  # angle
        self.mouse = {'x': 0, 'y': 0}
        self.color = '#0c6af7'
        self.theorical_speed = 4.0
        self.speed = self.theorical_speed * 60 / self.env.framerate  # computed value
        self.dash_speed = 4.0
        self.dash_length = 38  # cycle
        self.dash_preview = False
        self.number_dash = 3
        self.dash_left = self.number_dash
        self.dash_animation = []
        self.dash_animation_duration = 3  # tick
        self.dash_animation_end_tick = 0
        self.dash_cooldown = 3  # secondes
        self.dash_sound = 'dash2.wav'
        self.health = 100
        self.movement_allowed = True
        self.hit_player = {}
        self.hit_by_player = {}
        self.total_damage = 0
        self.kills = []
        self.assists = []
        self.alive = True
        self.aimbot = False
        self.obj_in_viewbox = []
        self.collide_box = Box(self.x - 100, self.y - 100, self.x + 100, self.y + 100)
        self.melee = MeleeAttack(self)
        if role == 'A': self.weapon = AR(self)
        elif role == 'SG': self.weapon = Shotgun(self)
        elif role == 'S': self.weapon = Sniper(self)
        elif role == 'SMG': self.weapon = SMG(self)
        elif role == 'R': self.weapon = Beam(self)

        self.env.players.append(self)

    @profile
    def check_shoot_collide(self):
        for shoot in self.env.shoots:
            dist_head = math.sqrt((self.x - shoot.head['x'])**2 + (self.y - shoot.head['y'])**2)
            dist_tail = math.sqrt((self.x - shoot.x)**2 + (self.y - shoot.y)**2)
            tolerance = 6
            shooter = shoot.from_player
            victim = self
            if (dist_head <= victim.size + tolerance or dist_tail <= victim.size + tolerance) and shooter != victim:
                victim.hit_by(shooter, shoot.damage)
                # shooter.hit(victim, real_damage)
                self.env.shoots.remove(shoot)

    def check_ray_collide(self):
        for ray in self.env.rays:
            tolerance = 4.5
            shooter = ray.from_player
            victim = self
            dist = abs(ray.a * victim.x + ray.b * victim.y + ray.c) / math.sqrt(ray.a**2 + ray.b**2)
            if victim.size >= dist and shooter != victim:
                victim.hit_by(shooter, ray.damage)
                # shooter.hit(victim, real_damage)
                self.env.rays.remove(ray)
                return True

    def check_collectible_collide(self):
        for c in self.env.collectible:
            c_center = {'x': c.x + c.size/2, 'y':c.y + c.size/2}
            if math.sqrt((self.x - c_center['x'])**2 + (self.y - c_center['y'])**2) < c.size:
                c.on_collect(self)

    def hit(self, victim, damage):
        self.weapon.bullets_hit += 1
        if victim.id in self.hit_player:
            self.hit_player[victim.id] += damage
        else:
            self.hit_player[victim.id] = damage
        if victim.health <= 0 and not victim in self.kills:
            self.message('hit', f'{int(damage)}', duration=.95, victim=victim)
            self.message('alert', f'Kill {victim.name}', duration=1.15)
            self.kills.append(victim)
        elif damage > 0:
            self.message('hit', f'{int(damage)}', duration=1.05, victim=victim)

    def hit_by(self, player, damage):
        self.health -= damage
        real_damage = damage if self.health >= 0 else damage - abs(self.health)
        self.message('warning', f'Hit by {player.name}')
        if player.id in self.hit_by_player:
            self.hit_by_player[player.id] += damage
        else:
            self.hit_by_player[player.id] = damage
        if self.health <= 0:
            self.dead()
            self.health = 0
        player.hit(self, real_damage)

    def collide_wall(self):
        x, y = self.x, self.y
        collide_x, collide_y = False, False
        delta = {'x': 0, 'y': 0}

        if self.own:
            rect_array = self.obj_in_viewbox
        else:
             rect_array = [obj for obj in self.env.map.objects if Rect.intersect(obj, self.collide_box)]

        for obj in rect_array:
            delta_x, delta_y = 0, 0
            if y + self.size > obj.y and y - self.size < obj.y2 and x + self.size > obj.x and x - self.size < obj.x2:
                delta_x_left = obj.x - (x + self.size)
                delta_x_right = (x - self.size) - obj.x2
                delta_x_left = delta_x_left if delta_x_left < 0 else 0
                delta_x_right = delta_x_right if delta_x_right < 0 else 0
                delta_x = max(delta_x_left, delta_x_right)
                if delta_x == delta_x_right:
                    delta_x *= -1

                delta_y_top = obj.y - (y + self.size)
                delta_y_bottom = (y - self.size) - obj.y2
                delta_y_top = delta_y_top if delta_y_top < 0 else 0
                delta_y_bottom = delta_y_bottom if delta_y_bottom < 0 else 0
                delta_y = max(delta_y_top, delta_y_bottom)
                if delta_y == delta_y_bottom:
                    delta_y *= -1

            if delta_x != 0 and delta_y != 0:
                delta_min = min(abs(delta_x), abs(delta_y))
                delta_x = delta_x if abs(delta_x) == delta_min else 0
                delta_y = delta_y if abs(delta_y) == delta_min else 0
            ## Add the delta of each rectangle to the total delta (dict)
            if delta_x != 0 and delta['x'] == 0:
                delta['x'] = delta_x
            if delta_y != 0 and  delta['y'] == 0:
                 delta['y'] = delta_y

        return delta['x'], delta['y']

    def move(self, x, y):
        self.x += x * self.speed
        self.y += y * self.speed

        offset_x, offset_y = self.collide_wall()
        self.x += offset_x
        self.y += offset_y

        # Restreint le joueur à l'environnement
        if self.x - self.size <= 0:
            self.x = self.size
        elif self.x + self.size >= self.env.width:
            self.x = self.env.width - self.size
        if self.y - self.size <= 0:
            self.y = self.size
        elif self.y + self.size >= self.env.height:
            self.y = self.env.height - self.size

        if self.own:
            self.update_viewBox()
        else:
            self.collide_box = Box(self.x - 100, self.y - 100, self.x + 100, self.y + 100)

    def dash(self, *event):
        if not self.alive: return
        if self.dash_left > 0:
            self.dash_animation = []
            self.dash_animation_end_tick = self.env.tick + self.dash_animation_duration
            self.movement_allowed = False
            self.env.sounds.append(Sound(self.dash_sound, self))
            for i in range(self.dash_length):
                self.speed = self.dash_speed
                self.dash_animation.append({'x': self.x, 'y': self.y})
                self.move(math.cos(self.dir), math.sin(self.dir))
                # self.check_shoot_collide()
                # self.check_collectible_collide()
                self.render(dash=True)
            self.dash_left -= 1
            self.movement_allowed = True
            cooldown = Timer(self.dash_cooldown, self.new_dash)
            cooldown.daemon = True
            cooldown.start()

    def new_dash(self):
        if self.dash_left < self.number_dash:
            self.dash_left += 1

    def shoot(self, *event):
        if not self.alive: return
        if event:
            self.weapon.proceed_shoot(event)
        else:
            self.weapon.proceed_shoot()

    def reload(self, *event):
        if not self.alive: return
        self.weapon.reload(event)

    def message(self, type, text, duration=.8, victim=None):
        if not self.own: return
        if type == 'hit':
            DamageMessage(victim, text, self.interface)
        else:
            TempMessage(type, text, self.interface, duration)

    def toggle_aimbot(self):
        self.aimbot = not self.aimbot

    def dist(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def detect_closer_player(self):
        closer = None
        for player in self.env.players:
            if closer and player != self and player.alive:
                if self.dist(player) < self.dist(closer):
                    closer = player
            elif player != self and player.alive:
                closer = player
        return closer

    def submit_event(self, type, content):
        self.env.events.push(Event(type, content))

    def dead(self):
        if not self.alive: return
        self.message('alert', 'You\'re DEAD', duration=1.5)
        self.alive = False
        if self.own:
            Timer(.5, lambda: self.interface.menu.toggle('on')).start()

    def stats(self):
        precision = self.weapon.bullets_hit / self.weapon.bullets_drawn * 100 if self.weapon.bullets_drawn != 0 else 0
        return {'total_damage': self.total_damage, 'kills': len(self.kills), 'assists': len(self.assists), 'accuracy': precision}

    @profile
    def update(self):
        if not self.alive: return
        self.mouse['x'] = (self.env.viewArea['x'] + self.env.fen.winfo_pointerx() - self.env.fen.winfo_rootx()) / self.env.scale
        self.mouse['y'] = (self.env.viewArea['y'] + self.env.fen.winfo_pointery() - self.env.fen.winfo_rooty()) / self.env.scale
        deltaX = self.mouse['x'] - self.x if (self.x != self.mouse['x']) else 1
        deltaY = self.mouse['y'] - self.y
        self.speed = self.theorical_speed * 60 / self.env.framerate
        self.total_damage = sum(self.hit_player.values())
        if self.aimbot:
            closer_player = self.detect_closer_player()
            if closer_player:
                self.dir = math.atan2(closer_player.y - self.y, closer_player.x - self.x)
        elif self.own:
            self.dir = math.atan2(deltaY, deltaX)
        if self.alive:
            self.check_collectible_collide()
            self.check_shoot_collide()
            self.check_ray_collide()
            self.assists = [player for player in self.hit_player.keys() if not self.env.find_by('id', player).alive]
        if self.own:
            self.detect_keypress()

    def render(self, dash=False):
        head_position = -20 if self.y > 30 else 20
        head_text = self.name if self.own else '{0}: {1} hp'.format(self.name, math.ceil(self.health))
        self.env.rendering_stack.append(RenderedObject('oval', self.x - self.size, self.y - self.size, x2=self.x + self.size, y2=self.y + self.size, color=self.color, width=0, dash=self.dash))

        if display_pointer:
            self.env.rendering_stack.append(RenderedObject('oval', self.mouse['x'] - self.size, self.mouse['y'] - self.size/3, x2=self.mouse['x'] + self.size/3, y2=self.mouse['y'] + self.size, color='red', width=0))

        if not dash:
            self.env.rendering_stack.append(RenderedObject('line', self.x + math.cos(self.dir) * 12, self.y + math.sin(self.dir) * 12, x2=self.x + math.cos(self.dir) * 20, y2=self.y + math.sin(self.dir) * 20, zIndex=2))
            self.env.rendering_stack.append(RenderedObject('text', self.x - len(self.name) / 2, self.y + head_position, text=head_text, color='#787878', zIndex=3))
            if self.dash_preview:
                preview_size = self.size
                self.env.rendering_stack.append(RenderedObject('oval', self.simul_dash['x'] - preview_size, self.simul_dash['y'] - preview_size, x2=self.simul_dash['x'] + preview_size, y2=self.simul_dash['y'] + preview_size, color='#ccc'))

        if self.env.tick <= self.dash_animation_end_tick:
            self.env.rendering_stack = [el for el in self.env.rendering_stack if el.role != 'dash_animation']
            for coord in self.dash_animation:
                size = self.size/len(self.dash_animation) * self.dash_animation.index(coord) / 1.25
                self.env.rendering_stack.append(RenderedObject('oval', coord['x'] - size, coord['y'] - size, x2=coord['x'] + size, y2=coord['y'] + size, color=self.color, zIndex=3, role='dash_animation'))

class OwnPlayer(Player):
    def __init__(self, id, x, y, env, name, role):
        super().__init__(id, x, y, env, name, role, own=True)
        self.interface = None
        self.client = None
        self.env.own_player = self

    def bind_keys(self, key_bind):
        self.key = key_bind or default_keys
        self.env.fen.bind('<Button-1>', self.shoot)
        self.env.fen.bind('<ButtonRelease-1>', self.weapon.stop_fire)
        keyboard.on_press_key(self.key['melee'], self.melee.attack)
        keyboard.on_press_key(self.key['reload'], self.reload)
        keyboard.on_press_key(self.key['panic'], self.env.panic)
        keyboard.on_press_key(self.key['dash'], self.dash)
        # keyboard.on_press_key(self.key['dash_preview'], self.toggle_dash_preview)
        keyboard.on_press_key('&', lambda *e: self.env.change_scale(value=1))
        keyboard.on_press_key('é', lambda *e: self.env.change_scale(value=self.env.viewArea['width']/self.env.canvas.width))
        keyboard.on_press_key('à', lambda *e: self.env.toggle_optimization())
        keyboard.on_press_key('"', lambda *e: self.toggle_aimbot())

    def toggle_dash_preview(self, *event):
        self.dash_preview = not self.dash_preview

    def detect_keypress(self):
        if not self.movement_allowed: return
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

    def update_viewBox(self):
        viewBox = self.env.viewArea
        if self.x >= viewBox['width'] / 2 and self.x <= self.env.width - viewBox['width'] / 2:
            viewBox['x'] = self.x - viewBox['width'] / 2
        else:
            viewBox['x'] = 0 if self.x <= viewBox['width'] / 2 else self.env.width - viewBox['width']
        if self.y >= viewBox['height'] / 2 and self.y <= self.env.height - viewBox['height'] / 2:
            viewBox['y'] = self.y - viewBox['height'] / 2
        else:
            viewBox['y'] = 0 if self.y <= viewBox['height'] / 2 else self.env.height - viewBox['height']
        self.obj_in_viewbox = [obj for obj in self.env.map.objects if self.env.in_viewBox(obj)]

    def message(self, type, text, duration=.8, victim=None):
        if type == 'hit':
            DamageMessage(victim, text, self.interface)
        else:
            TempMessage(type, text, self.interface, duration)

class OnlinePlayer(Player):
    def __init__(self, id, x, y, env, name, role='A'):
        super().__init__(id, x, y, env, name, role)

class Target(Player):
    def __init__(self, id, x, y, env, level=5):
        super().__init__(id, x, y, env, name="Target", own=False)
        self.id = id
        self.x = x
        self.y = y
        self.env = env
        self.level = level
        self.name = random.choice(target_name)
        target_name.remove(self.name)
        self.own = False
        self.theorical_speed = level / 2.75
        self.weapon = AR(self)
        self.color = random.choice(['#AAA', '#BBB'])
        self.tick = 1
        self.vx = random_sign()
        self.vy = random_sign()
        self.move_interval = random.randint(20, 60)
        self.shoot_interval = random.randint(10, 200-self.level*2)
        self.dash_interval = random.randint(100, 300 - 10*self.level)
        self.can_shoot = self.level >= 3
        self.can_move = self.level >= 2
        self.shoot_dispersion = math.pi/(4 + random.randint(self.level, self.level*2))

    def shoot(self):
        self.weapon.shoot()

    def update(self):
        if self.alive and len(self.env.players_alive) > 1:
            super().update()
            closer_player = self.detect_closer_player()
            if closer_player:
                self.dir = math.atan2(closer_player.y - self.y, closer_player.x - self.x)
            if self.tick % self.move_interval == 0:
                self.vy *= random_sign()
                self.vx *= random_sign()
            if self.tick % self.shoot_interval == 0 and self.can_shoot:
                self.dir += random_sign()*random.random() * self.shoot_dispersion
                self.shoot()
            if self.tick % self.dash_interval == 0 and self.can_move:
                self.dir = random.random() * 2 * math.pi
                super().dash()
            self.tick += 1
            if self.can_move:
                super().move(self.vx, self.vy)
