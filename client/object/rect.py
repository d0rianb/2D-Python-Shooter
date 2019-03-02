#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

Box = namedtuple('Box', 'x y x2 y2')

class Rect:
    def __init__(self, _id, x, y, width, height, map, multiplier=1):
        self.id = int(_id)
        self.multiplier = multiplier
        self.rel_x = float(x) * float(self.multiplier)
        self.rel_y = float(y) * float(self.multiplier)
        self.python_id = id(self)
        self.rel_width = float(width) * float(self.multiplier)
        self.rel_height = float(height) * float(self.multiplier)
        self.rel_x2 = self.rel_x + self.rel_width
        self.rel_y2 = self.rel_y + self.rel_height
        self.map = map
        real_ratio = abs(self.map.env.viewArea['width'] / self.map.env.viewArea['height'] - 16 / 9)
        self.gridX = self.map.env.width / self.map.grid['x']
        self.gridY = self.map.env.height / (self.map.grid['y'] + real_ratio)

        self.color = '#757575'

        self.computed_values()

    def __repr__(self):
        return 'Rect x:{rel_x} y:{rel_y} width:{rel_width} height:{rel_height} at {python_id}'.format(**self.__dict__)

    def __eq__(self, other):
        return self.rel_x == other.rel_x and self.rel_y == other.rel_y and self.rel_width == other.rel_width and self.rel_height == other.rel_height

    def computed_values(self):
        self.x = self.rel_x * self.gridX
        self.y = self.rel_y * self.gridY
        self.width = self.rel_width * self.gridX
        self.height = self.rel_height * self.gridY
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height

    def contains(self, x, y):
        return x >= self.x and x <= self.x2 and y >= self.y and y <= self.y2

    def contains_rect(self, other):
        return other.x >= self.x and other.x2 <= self.x2 and other.y >= self.y and other.y2 <= self.y2

    def grid_contains(self, x, y):
        return x >= self.rel_x and x <= self.rel_x + self.rel_width and y >= self.rel_y and y <= self.rel_y + self.rel_height

    def merge(self, rect):
        x = min(self.rel_x, rect.rel_x)
        y = min(self.rel_y, rect.rel_y)
        x2 = max(self.rel_x2, rect.rel_x2)
        y2 = max(self.rel_y2, rect.rel_y2)
        return Rect(self.id, x, y, x2-x, y2-y, self.map)

    @staticmethod
    def intersect(rect1, rect2):
        dx = min(rect1.x2, rect2.x2) - max(rect1.x, rect2.x)
        dy = min(rect1.y2, rect2.y2) - max(rect1.y, rect2.y)
        return dx >= 0 and dy >= 0
