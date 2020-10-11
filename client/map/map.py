#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# from PIL import Image, ImageTk
from object.rect import Rect
from object.circle import Circle
from render import RenderedObject

MAP_TEXTURE = False

class Map:
    def __init__(self, file, name='Map1'):
        self.name = name
        self.objects = []
        self.rects_texture = {}
        self.file = file
        self.env = None
        self.width, self.height = 0, 0
        self.grid = { 'x': 0, 'y': 0 }
        self.multiplier = 1
        dir = os.path.dirname(os.path.realpath(__file__))

        lines = []
        keyword = ['object', 'rect', 'circle', 'define']
        map_file = open(os.path.join(dir, 'files/compiled', file), 'r')
        for line in map_file.readlines():
            if len(line.split()) > 0 and line.split()[0] in keyword:
                lines.append(line.strip('\n').split())
        map_file.close()

        for line in lines:
            if line[0] == 'define':
                if line[1] == 'grid':
                    self.grid['x'] = int(line[2])
                    self.grid['y'] = int(line[3])
                if line[1] == 'multiplier':
                    self.multiplier = int(line[2])
                if line[1] == 'dimension':
                    self.width = int(line[2])
                    self.height = int(line[3])
            elif line[0] == 'rect':
                self.objects.append(Rect(len(self.objects) + 1, line[1], line[2], line[3], line[4], self, self.multiplier, viewBox_init=False))
            elif line[0] == 'circle':
                self.objects.append(Circle(len(self.objects) + 1, line[1], line[2], line[3], self, self.multiplier, viewBox_init=False))

        if MAP_TEXTURE:
            self.wall_texture_path = os.path.join(dir, '../ressources/texture/wall_texture_2.jpg')
            self.wall_texture = Image.open(self.wall_texture_path, mode='r')
            self.texture_width, self.texture_height = self.wall_texture.size

            for object in self.objects:
                if isinstance(object, Rect):
                    rect = object
                    scale_factor = min(self.texture_width/rect.width, self.texture_height/rect.height)
                    box = (0, 0, rect.width*scale_factor, rect.height*scale_factor)
                    image = self.wall_texture.crop(box).resize((int(rect.width), int(rect.height)))
                    texture = ImageTk.PhotoImage(image=image)
                    self.rects_texture[rect.id] = texture
        if self.width == 0 or self.height == 0:
            raise MapError('IllegalDimensions')

    @profile
    def render(self):
        for object in self.objects:
            if isinstance(object, Rect) and (not self.env.optimize or self.env.in_viewBox(object)):
                rect = object
                if MAP_TEXTURE:
                    self.env.rendering_stack.append(RenderedObject('image', rect.x, rect.y, image=self.rects_texture[rect.id]))
                else:
                    self.env.rendering_stack.append(RenderedObject('rect', rect.x, rect.y, width=rect.width, height=rect.height, color=rect.color, zIndex=5))
            elif isinstance(object, Circle):
                circle = object
                self.env.rendering_stack.append(RenderedObject('oval', circle.x1, circle.y1, x2=circle.x2, y2=circle.y2, color=circle.color, zIndex=5))


class MapError(Exception):
    def __init__(self, message, *errors):
        super().__init__(message)
        self.errors = errors
