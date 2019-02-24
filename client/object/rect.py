#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rect:
    def __init__(self, id, x, y, width, height, map, multiplier=1):
        self.id = int(id)
        self.multiplier = multiplier
        self.relative_x = float(x) * float(self.multiplier)
        self.relative_y = float(y) * float(self.multiplier)
        self.relative_width = float(width) * float(self.multiplier)
        self.relative_height = float(height) * float(self.multiplier)
        self.relative_x2 = self.relative_x + self.relative_width
        self.relative_y2 = self.relative_y + self.relative_height
        self.map = map
        real_ratio = abs(self.map.env.viewArea['width'] / self.map.env.viewArea['height'] - 16 / 9)
        self.gridX = self.map.env.width / self.map.grid['x']
        self.gridY = self.map.env.height / (self.map.grid['y'] + real_ratio)

        self.color = '#757575'

        self.computed_values()

    def __repr__(self):
        return 'Rect x:{relative_x} y:{relative_y} width:{relative_width} height:{relative_height}'.format(**self.__dict__)

    def computed_values(self):
        self.x = self.relative_x * self.gridX
        self.y = self.relative_y * self.gridY
        self.width = self.relative_width * self.gridX
        self.height = self.relative_height * self.gridY
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height

    def contains(self, x, y):
        return x >= self.x and x <= self.x2 and y >= self.y and y <= self.y2

    def contains_rect(self, other):
        return other.x >= self.x and other.x2 <= self.x2 and other.y >= self.y and other.y2 <= self.y2

    def grid_contains(self, x, y):
        return x >= self.relative_x and x <= self.relative_x + self.relative_width and y >= self.relative_y and y <= self.relative_y + self.relative_height

    def merge(self, rect):
        x = min(self.relative_x, rect.relative_x)
        y = min(self.relative_y, rect.relative_y)
        x2 = max(self.relative_x2, rect.relative_x2)
        y2 = max(self.relative_y2, rect.relative_y2)
        return Rect(self.id, x, y, x2-x, y2-y, self.map)
