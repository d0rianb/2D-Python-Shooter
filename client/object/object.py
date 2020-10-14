#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Object:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.x1, self.x2 = x, y
        self.in_viewBox = 'undefined' # 'in' | 'out' | 'undefined'

    @staticmethod
    def intersect(obj1, obj2):
        dx = min(obj1.x2, obj2.x2) - max(obj1.x, obj2.x)
        dy = min(obj1.y2, obj2.y2) - max(obj1.y, obj2.y)
        return dx > 0 and dy > 0