#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from object.rect import Rect
from object.circle import Circle
from render import RenderedObject


class Map:
    def __init__(self, env, file, name='temp_map'):
        self.env = env
        self.env.map = self
        self.name = name
        self.file = file
        self.grid = { 'x': 128, 'y': 72 }
        self.multiplier = 1

    def display_grid(self):
        for col in range(self.grid['x']):
            rect = Rect(100 + col, col, 0, 0.01, self.grid['y'], self)
            self.env.rendering_stack.append(RenderedObject('rect', rect.x, rect.y,  width=rect.width, height=rect.height, color='#BBB'))
        for line in range(self.grid['y']):
            rect = Rect(128 + line, 0, line, self.grid['x'], 0.01, self)
            self.env.rendering_stack.append(RenderedObject('rect', rect.x, rect.y,  width=rect.width, height=rect.height, color='#BBB'))

    def save(self, objects):
        with open(self.file, 'a') as map_file:
            pass
