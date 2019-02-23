#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rect:
    def __init__(self, id, x, y, width, height, map):
        self.id = int(id)
        self.relative_x = float(x)
        self.relative_y = float(y)
        self.relative_width = float(width)
        self.relative_height = float(height)
        self.map = map
        real_ratio = abs(self.map.env.viewArea['width'] / self.map.env.viewArea['height'] - 16 / 9)
        gridX = self.map.env.width / self.map.grid['x']
        gridY = self.map.env.height / (self.map.grid['y'] + real_ratio)

        self.x = self.relative_x * gridX
        self.y = self.relative_y * gridY
        self.width = self.relative_width * gridX
        self.height = self.relative_height * gridY
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height

        self.color = '#757575'
