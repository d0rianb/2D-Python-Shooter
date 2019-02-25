#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import keyboard

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
        keyboard.on_press_key('m', self.save)


    def display_grid(self):
        for col in range(self.grid['x']):
            rect = Rect(100 + col, col, 0, 0.01, self.grid['y'], self)
            self.env.rendering_stack.append(RenderedObject('rect', rect.x, rect.y,  width=rect.width, height=rect.height, color='#BBB'))
        for line in range(self.grid['y']):
            rect = Rect(128 + line, 0, line, self.grid['x'], 0.01, self)
            self.env.rendering_stack.append(RenderedObject('rect', rect.x, rect.y,  width=rect.width, height=rect.height, color='#BBB'))

    def save(self, *event):
        self.env.merge_rect()
        rects = self.env.objects.copy()
        text = ''
        with open(self.file, 'w+') as map_file:
            text += 'define grid {x} {y}\n'.format(**self.grid)
            for obj in rects:
                if isinstance(obj, Rect):
                    text += 'rect {relative_x:n} {relative_y:n} {relative_width:n} {relative_height:n}\n'.format(**obj.__dict__)
            map_file.write(text)
