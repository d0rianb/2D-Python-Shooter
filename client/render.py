#!/usr/bin/env python
# -*- coding: utf-8 -*-

class RenderedObject:
    def __init__(self, type, x, y, **kwargs):
        self.type = type # rect/text/oval/line
        self.x = x
        self.y = y
        self.options = kwargs
        self.x2 = kwargs.get('x2', None)
        self.y2 = kwargs.get('y2', None)
        self.width = kwargs.get('width', None)
        self.height = kwargs.get('height', None)
        self.text = kwargs.get('text', None)
        self.color = kwargs.get('color', None)
<<<<<<< HEAD:client/render.py
        self.fill = kwargs.get('fill', None)
=======
>>>>>>> multi-0.0.1:client/render.py
        self.font = kwargs.get('font', None)
        self.anchor = kwargs.get('anchor', None)
        self.zIndex = kwargs.get('zIndex', 1)
