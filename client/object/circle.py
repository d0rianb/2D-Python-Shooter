#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Circle:
    def __init__(self, id, x, y, radius, map, multiplier=1):
        self.id = int(id)
        self.relative_x = float(x) * float(multiplier)
        self.relative_y = float(y) * float(multiplier)
        self.relative_radius = float(radius) * float(multiplier)
        self.map = map
        real_ratio = abs(self.map.env.viewArea['width'] / self.map.env.viewArea['height'] - 16 / 9)
        gridX = self.map.env.width / self.map.grid['x']
        gridY = self.map.env.height / (self.map.grid['y'] + real_ratio)

        self.radius = self.relative_radius * gridX
        self.x = self.relative_x * gridX
        self.y = self.relative_y * gridY
        self.x1 = self.x - self.radius
        self.y1 = self.y - self.radius
        self.x2 = self.x + self.radius
        self.y2 = self.y + self.radius

        self.color = '#757575'
