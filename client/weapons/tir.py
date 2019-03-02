#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from render import RenderedObject
from object.rect import Rect, Box
from object.circle import Circle

class Tir:
    def __init__(self, x, y, dir, weapon):
        self.x = x
        self.y = y
        self.dir = dir
        self.weapon = weapon
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
        self.collide_box = Box(self.x - 50, self.y - 50, self.x + 50, self.y + 50)
        self.env.shoots.append(self)

    def check_wall_collide(self, map):
        x = self.head['x']
        y = self.head['y']
        rects = [obj for obj in map.objects if isinstance(obj, Rect) and Rect.intersect(obj, self.collide_box)]
        for obj in rects:
            if isinstance(obj, Rect):
                rect = obj
                if x >= rect.x and x <= rect.x2 and y >= rect.y and y <= rect.y2:  # Check for Head
                    if self in self.env.shoots:
                        self.env.shoots.remove(self)
                elif self.x >= rect.x and self.x <= rect.x2 and self.y >= rect.y and self.y <= rect.y2:  # Check for bottom
                    if self in self.env.shoots:
                        self.env.shoots.remove(self)

    def destroy(self):
        self.env.shoots.remove(self)

    def update(self):
        player_dist = self.from_player.dist(self)
        if player_dist > self.range:
            self.destroy()
            return

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
        self.collide_box = Box(self.x - 50, self.y - 50, self.x + 50, self.y + 50)
        self.check_wall_collide(self.env.map)

    def render(self):
        self.env.rendering_stack.append(RenderedObject('line', self.x, self.y, x2=self.head['x'], y2=self.head['y']))
