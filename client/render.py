#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk

class Canvas:
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        self.env = None
        self.scale = 1
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height, bg='#EEE', highlightthickness=0)

    def _scale(self, object):
        if not self.env: return
        scale_x = self.scale * self.env.viewArea['width'] / self.env.width
        scale_y = self.scale * self.env.viewArea['height'] / self.env.height
        object.x *= scale_x
        object.y *= scale_y
        object.x2 *= scale_y
        object.y2 *= scale_y
        object.width *= scale_x
        object.height *= scale_y
        return object

    # @profile
    def render(self, stack):
        self.canvas.delete('all')
        for object in stack:
            object = self._scale(object)
            if object.type == 'rect':
                self.canvas.create_rectangle(object.x, object.y, object.x + object.width, object.y + object.height, fill=object.color, width=0)
            elif object.type == 'image':
                self.canvas.create_image(object.x, object.y, image=object.image, anchor=tk.NW)
            elif object.type == 'oval':
                self.canvas.create_oval(object.x, object.y, object.x2, object.y2, fill=object.color, width=0)
            elif object.type == 'line':
                self.canvas.create_line(object.x, object.y, object.x2, object.y2, smooth=1, capstyle='round')
            elif object.type == 'text':
                self.canvas.create_text(object.x, object.y, text=object.text, font=object.font, fill=object.color, anchor=object.anchor)
        self.canvas.pack()


class RenderedObject:
    def __init__(self, type, x, y, **kwargs):
        self.type = type  # rect/text/oval/line
        self.x = x
        self.y = y
        self.options = kwargs
        self.x2 = kwargs.get('x2', 0)
        self.y2 = kwargs.get('y2', 0)
        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)
        self.text = kwargs.get('text', 'No text')
        self.image = kwargs.get('image', None)
        self.color = kwargs.get('color', None)
        self.font = kwargs.get('font', None)
        self.id = kwargs.get('id', -1)
        self.anchor = kwargs.get('anchor', tk.CENTER)
        self.zIndex = kwargs.get('zIndex', 1)
