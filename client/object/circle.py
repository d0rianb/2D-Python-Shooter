#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO : extend from class object
class Circle:
    def __init__(self, id, x, y, radius, map, multiplier=1):
        self.id = int(id)
        self.rel_x = float(x) * float(multiplier)
        self.rel_y = float(y) * float(multiplier)
        self.relative_radius = float(radius) * float(multiplier)
        self.map = map
        real_ratio = abs(self.map.env.viewArea['width'] / self.map.env.viewArea['height'] - 16 / 9)
        gridX = self.map.env.width / self.map.grid['x']
        gridY = self.map.env.height / (self.map.grid['y'] + real_ratio)

        self.radius = self.relative_radius * gridX
        self.x = self.rel_x * gridX
        self.y = self.rel_y * gridY
        self.x1 = self.x - self.radius
        self.y1 = self.y - self.radius
        self.x2 = self.x + self.radius
        self.y2 = self.y + self.radius

        self.in_viewBox = 'undefined' # 'in' | 'out' | 'undefined'


        self.color = '#757575'

        @staticmethod
        def intersect(circle1, circle2):
            dx = min(circle1.x2, circle2.x2) - max(circle1.x, circle2.x)
            dy = min(circle1.y2, circle2.y2) - max(circle1.y, circle2.y)
            return dx > 0 and dy > 0
