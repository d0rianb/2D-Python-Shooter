#!/usr/bin/env python
# -*- coding: utf-8 -*-

class RenderedObject:
    def __init__(self, type, x, y, **kwargs):
        self.type = type # rect/text/oval
        self.x = x
        self.y = y
        self.options = kwargs
        self.width = kwargs.get('width', None)
        self.height = kwargs.get('height', None)
        self.content = kwargs.get('content', None)
        self.color = kwargs.get('color', None)
        self.fill = kwargs.get('fill', None)
