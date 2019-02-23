#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PIL import Image, ImageTk
from object.rect import Rect
from object.circle import Circle
from render import RenderedObject


class Map:
    def __init__(self, env, file, name='Map1'):
        self.env = env
        self.env.map = self
        self.name = name
        self.objects = []
        self.rects_texture = {}
        self.file = file
        self.grid = { 'x': 0, 'y': 0 }
        dir = os.path.dirname(os.path.realpath(__file__))

        self.wall_texture_path = os.path.join(dir, '../ressources/texture/wall_texture_2.jpg')
        self.wall_texture = Image.open(self.wall_texture_path, mode='r')
        self.texture_width, self.texture_height = self.wall_texture.size

        lines = []
        keyword = ['object', 'rect', 'circle', 'define']
        map_file = open(os.path.join(dir, 'files', file), 'r')
        for line in map_file.readlines():
            if len(line.split()) > 0 and line.split()[0] in keyword:
                lines.append(line.strip('\n').split())
        map_file.close()

        for line in lines:
            if line[0] == 'rect':
                self.objects.append(Rect(len(self.objects) + 1, line[1], line[2], line[3], line[4], self))
            elif line[0] == 'circle':
                self.objects.append(Circle(len(self.objects) + 1, line[1], line[2], line[3], self))
            elif line[0] == 'define' and line[1] == 'grid':
                self.grid['x'] = int(line[2])
                self.grid['y'] = int(line[3])

        for object in self.objects:
            if isinstance(object, Rect):
                rect = object
                scale_factor = min(self.texture_width/rect.width, self.texture_height/rect.height)
                box = (0, 0, rect.width*scale_factor, rect.height*scale_factor)
                image = self.wall_texture.crop(box).resize((int(rect.width), int(rect.height)))
                texture = ImageTk.PhotoImage(image=image)
                self.rects_texture[rect.id] = texture

    def render(self):
        # for col in range(self.grid['x']):
        #     rect = Rect(100 + col, col, 0, 0.05, self.grid['y'], self)
        #     self.env.rendering_stack.append(RenderedObject('rect', rect.x, rect.y,  width=rect.width, height=rect.height, color='green'))
        # for line in range(self.grid['y']):
        #     rect = Rect(128 + line, 0, line, self.grid['x'], 0.05, self)
        #     self.env.rendering_stack.append(RenderedObject('rect', rect.x, rect.y,  width=rect.width, height=rect.height, color='green'))
        for object in self.objects:
            if isinstance(object, Rect):
                rect = object
                self.env.rendering_stack.append(RenderedObject('rect', rect.x, rect.y, width=rect.width, height=rect.height, color=rect.color))
                ## Texture
                # self.env.rendering_stack.append(RenderedObject('image', rect.x, rect.y, image=self.rects_texture[rect.id]))
            elif isinstance(object, Circle):
                circle = object
                self.env.rendering_stack.append(RenderedObject('oval', circle.x1, circle.y1, x2=circle.x2, y2=circle.y2, color=circle.color))
