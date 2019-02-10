#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from render import RenderedObject

class Tir:
    def __init__(self, id, x, y, dir, from_player):
        self.id = id
        self.x = x
        self.y = y
        self.dir = dir
        self.damage = 20
        self.theorical_speed = 18
        self.speed = self.theorical_speed * 60 / from_player.env.framerate
        self.size = 12
        self.head = {'x': x, 'y': y}
        self.from_player = from_player
        self.env = from_player.env

    def checkWallCollide(self, map):
        x = self.head['x']
        y = self.head['y']
        for rect in map.rects:
            if x >= rect.x and x <= rect.x2 and y >= rect.y and y <= rect.y2:  # Check for Head
                if self in self.env.shoots:
                    self.env.shoots.remove(self)
            elif self.x >= rect.x and self.x <= rect.x2 and self.y >= rect.y and self.y <= rect.y2:  # Check for bottom
                if self in self.env.shoots:
                    self.env.shoots.remove(self)

    def update(self):
        self.speed = self.theorical_speed * 60 / self.env.framerate
        self.x += math.cos(self.dir) * self.speed
        self.y += math.sin(self.dir) * self.speed
        self.head = {
            'x': self.x + math.cos(self.dir) * self.size,
            'y': self.y + math.sin(self.dir) * self.size
        }
        self.checkWallCollide(self.env.map)

    def render(self):
        self.env.rendering_stack.append(RenderedObject('line', self.x, self.y, x2=self.head['x'], y2=self.head['y']))
