#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import keyboard

from object.rect import Rect
from object.circle import Circle
from render import RenderedObject


class Map:
    def __init__(self, env, dir, name='temp_map'):
        self.env = env
        self.env.map = self
        self.name = name
        self.dir = dir
        self.width = self.env.width
        self.height = self.env.height
        self.grid = { 'x': 128, 'y': 72 }
        self.multiplier = 1

    def display_grid(self):
        for col in range(self.grid['x']):
            rect = Rect(100 + col, col, 0, 0.01, self.grid['y'], self)
            self.env.add_render_object(RenderedObject('rect', rect.x, rect.y,  width=rect.width, height=rect.height, color='#BBB'))
        for line in range(self.grid['y']):
            rect = Rect(128 + line, 0, line, self.grid['x'], 0.01, self)
            self.env.add_render_object(RenderedObject('rect', rect.x, rect.y,  width=rect.width, height=rect.height, color='#BBB'))
        vertical_line = Rect(-1, self.grid['x'] / 2 , 0, 0.01, self.grid['y'], self)
        horizontal_line = Rect(-1, 0, self.grid['y'] / 2, self.grid['x'], 0.01,  self)
        semi_vertical_line = Rect(-1, self.grid['x'] / 4 , 0, 0.01, self.grid['y'] / 2, self)
        semi_horizontal_line = Rect(-1, 0, self.grid['y'] / 4, self.grid['x'] / 2, 0.01,  self)
        self.env.add_render_object(RenderedObject('rect', vertical_line.x, vertical_line.y,  width=vertical_line.width, height=vertical_line.height, color='red'))
        self.env.add_render_object(RenderedObject('rect', horizontal_line.x, horizontal_line.y,  width=horizontal_line.width, height=horizontal_line.height, color='red'))
        self.env.add_render_object(RenderedObject('rect', semi_vertical_line.x, semi_vertical_line.y,  width=semi_vertical_line.width, height=semi_vertical_line.height, color='green'))
        self.env.add_render_object(RenderedObject('rect', semi_horizontal_line.x, semi_horizontal_line.y,  width=semi_horizontal_line.width, height=semi_horizontal_line.height, color='green'))

    def save(self, *event, compiled=False):
        if compiled:
            self.env.merge_rect()
            dir = os.path.join(self.dir, 'compiled')
            extension = '.compile.map'
        else:
            dir = os.path.join(self.dir, 'sources')
            extension = '.map'
        rects = self.env.objects.copy()
        text = ''
        with open(os.path.join(dir, self.name + extension), 'w+') as map_file:
            text += f'define dimension {self.width} {self.height}\n'
            text += 'define grid {x} {y}\n\n'.format(**self.grid)
            for obj in rects:
                if isinstance(obj, Rect):
                    text += 'rect {rel_x:n} {rel_y:n} {rel_width:n} {rel_height:n}\n'.format(**obj.__dict__)
            map_file.write(text)
