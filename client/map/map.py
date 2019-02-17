#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PIL import Image, ImageTk
from map.rect import Rect
from render import RenderedObject


class Map:
    def __init__(self, env, file, name='Map1'):
        self.env = env
        self.env.map = self
        self.name = name
        self.rects = []
        self.rects_texture = {}
        self.file = file
        dir = os.path.dirname(os.path.realpath(__file__))

        self.wall_texture_path = os.path.join(dir, '../ressources/texture/wall_texture_2.jpg')
        self.wall_texture = Image.open(self.wall_texture_path, mode='r')
        self.texture_width, self.texture_height = self.wall_texture.size

        lines = []
        keyword = ['rect', 'object']
        map_file = open(os.path.join(dir, file), 'r')
        for line in map_file.readlines():
            if len(line.split()) > 0 and line.split()[0] in keyword:
                lines.append(line.strip('\n').split())
        map_file.close()

        for line in lines:
            if line[0] == 'rect':
                self.rects.append(Rect(len(self.rects) + 1, line[1], line[2], line[3], line[4], self))

        for rect in self.rects:
            scale_factor = min(self.texture_width/rect.width, self.texture_height/rect.height)
            box = (0, 0, rect.width*scale_factor, rect.height*scale_factor)
            image = self.wall_texture.crop(box).resize((int(rect.width), int(rect.height)))
            texture = ImageTk.PhotoImage(image=image)
            self.rects_texture[rect.id] = texture

    def render(self):
        for rect in self.rects:
            # self.env.rendering_stack.append(RenderedObject('image', rect.x, rect.y, image=self.rects_texture[rect.id]))
            self.env.rendering_stack.append(RenderedObject('rect', rect.x, rect.y, width=rect.width, height=rect.height, color=rect.color))
