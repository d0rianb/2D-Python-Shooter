#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from render import RenderedObject
from object.rect import Rect, Box
from object.circle import Circle
from object.intersection import line_rect

class Tir:
    def __init__(self, x, y, dir, weapon):
        self.x = x
        self.y = y
        self.dir = dir
        self.weapon = weapon
        self.alive = True
        self.damage = self.weapon.damage
        self.damage_decrease = self.weapon.damage_decrease
        self.has_decreased_damage = False
        self.range = self.weapon.range
        self.from_player = self.weapon.player
        self.theorical_speed = self.weapon.shoot_speed
        self.speed = self.theorical_speed * 60 / self.from_player.env.framerate
        self.size = self.weapon.munition_size
        self.head = {'x': x, 'y': y}
        self.env = self.from_player.env
        self.id = len(self.env.shoots) + 1

        ## Equation : ax + by + c
        delta_y = self.head['y'] - self.y
        delta_x = self.head['x'] - self.x
        if self.head['x'] != self.x:
            self.a = delta_y / delta_x
        else:
            self.a = 0
        self.b = -1
        self.c = self.y - self.a*self.x

        self.collide_box = Box(self.head['x'] - 50, self.head['y'] - 50, self.head['x'] + 50, self.head['y'] + 50)
        self.env.shoots.append(self)

    def check_wall_collide(self, map):
        x = self.head['x']
        y = self.head['y']
        rects = [obj for obj in map.objects if isinstance(obj, Rect) and Rect.intersect(obj, self.collide_box)]
        for obj in rects:
            if isinstance(obj, Rect):
                rect = obj
                if x >= rect.x and x <= rect.x2 and y >= rect.y and y <= rect.y2:  # Check for Head
                    self.destroy()
                elif self.x >= rect.x and self.x <= rect.x2 and self.y >= rect.y and self.y <= rect.y2:  # Check for bottom
                    self.destroy()

    def update_collide_box(self):
        self.collide_box = Box(self.head['x'] - 50, self.head['y'] - 50, self.head['x'] + 50, self.head['y'] + 50)

    def destroy(self):
        if self in self.env.shoots:
            self.env.shoots.remove(self)
            self.alive = False

    def update(self):
        self.update_collide_box()
        self.check_wall_collide(self.env.map)
        player_dist = self.from_player.dist(self)
        if player_dist > self.range:
            self.destroy()
        if not self.alive: return

        decrease_factor = 1
        if player_dist > self.damage_decrease['range'] and not self.has_decreased_damage:
            self.damage *= self.damage_decrease['factor']
            self.has_decreased_damage = True

        self.speed = self.theorical_speed * 60 / self.env.framerate
        self.x += math.cos(self.dir) * self.speed
        self.y += math.sin(self.dir) * self.speed
        self.head = {
            'x': self.x + math.cos(self.dir) * self.size,
            'y': self.y + math.sin(self.dir) * self.size
        }

    def render(self):
        self.env.rendering_stack.append(RenderedObject('line', self.x, self.y, x2=self.head['x'], y2=self.head['y'], zIndex=2))

class Ray(Tir):
    def __init__(self, x, y, dir, weapon):
        super().__init__(x, y, dir, weapon)
        self.state = 'inactive'
        self.env.shoots.remove(self)
        self.env.rays.append(self)

    def toggle_state(self, *arg):
        if arg:
            self.state = arg[0]
        elif self.state == 'active':
            self.state = 'inactive'
        elif self.state == 'inactive':
            self.state = 'active'

    def head_position(self, map):
        self.head = {
            'x': self.x + math.cos(self.dir) * self.size,
            'y': self.y + math.sin(self.dir) * self.size
        }
        closest_point = (math.inf, math.inf)
        for rect in map.objects:
            point = line_rect(self.x, self.y, self.head['x'], self.head['y'], rect.x, rect.y, rect.width, rect.height)
            if point:
                dist = math.sqrt((self.x - point[0])**2 + (self.y - point[1])**2)
                closest_dist = math.sqrt((self.x - closest_point[0])**2 + (self.y - closest_point[1])**2)
                if dist <= closest_dist:
                    closest_point = point
        if closest_point != (math.inf, math.inf):
            self.head = {'x': closest_point[0], 'y': closest_point[1]}

    def is_active(self):
        return self.state == 'active'

    def update(self):
        if not self.is_active(): return
        self.weapon.ammo -= 1
        if self.weapon.ammo == 0:
            self.weapon.reload()

        self.head_position(self.env.map)
        self.speed = self.theorical_speed * 60 / self.env.framerate
        self.x = self.from_player.x + math.cos(self.from_player.dir) * 12
        self.y = self.from_player.y +  math.sin(self.from_player.dir) * 12
        self.dir = self.from_player.dir


    def render(self):
        if self.is_active():
            self.env.rendering_stack.append(RenderedObject('line', self.x, self.y, x2=self.head['x'], y2=self.head['y'], zIndex=2))
