#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter.font as tkFont
import tkinter as tk
import keyboard
import math

from render import RenderedObject


class Interface:
    def __init__(self, player, env):
        self.player = player
        self.env = env
        self.env.interface = self
        self.margin_x = 8
        self.margin_y = 20
        self.x = self.env.viewArea['x']
        self.y = self.env.viewArea['y']
        self.width = self.env.viewArea['width']
        self.height = self.env.viewArea['height']
        self.padding = 20
        self.informations = {}
        self.color = '#92959b'
        self.font = tkFont.Font(family='Avenir Next', size=16, weight='normal')

    def parse(self, position, x, y, anchor):
        infos = self.informations[position]
        for (index, info) in enumerate(infos):
            self.env.rendering_stack.append(RenderedObject('text', x, y + index*self.padding,
                text='{0}: {1}'.format(info, infos[info]),
                anchor=anchor,
                color=self.color,
                font=self.font))

    def update(self):
        self.x = self.env.viewArea['x']
        self.y = self.env.viewArea['y']
        self.width = self.env.viewArea['width']
        self.height = self.env.viewArea['height']
        self.informations = {
            'TopLeft': {
                'FrameRate': self.env.framerate
            },
            'TopRight': {
                'Nombre d\'objets': len(self.env.objects)
            },
            'BottomRight': {}
        }

    def render(self):
        for position in self.informations:
            x, y = self.x + self.margin_x, self.y + self.margin_y
            anchor = 'w'
            if position == 'TopRight' or position == 'BottomRight':
                x = self.x + self.width - self.margin_x
                anchor = 'e'
            if position == 'BottomRight':
                y = self.y + self.height - len(self.informations['BottomRight'])*self.padding
            self.parse(position, x, y, anchor)
