#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import multiprocessing
import threading

class Canvas:
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        self.env = None
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height, bg='#EEE', highlightthickness=0)

    def scale(self, object):
        scale = self.env.scale
        object.x *= scale
        object.y *= scale
        object.x2 *= scale
        object.y2 *= scale
        object.width *= scale
        object.height *= scale
        return object

    def render(self, stack):
        self.canvas.delete('all')
        for object in stack:
            object = self.scale(object)
            view_x, view_y, view_x2, view_y2 = object.viewBox_coord(self.env.viewArea, self.env.scale)
            if object.type == 'rect':
                self.canvas.create_rectangle(view_x, view_y, view_x + object.width, view_y + object.height, fill=object.color, width=object.borderwidth, outline='#000')
            elif object.type == 'image':
                self.canvas.create_image(view_x, view_y, image=object.image, anchor=tk.NW)
            elif object.type == 'oval':
                self.canvas.create_oval(view_x, view_y, view_x2, view_y2, fill=object.color, width=0)
            elif object.type == 'line':
                self.canvas.create_line(view_x, view_y, view_x2, view_y2, smooth=1, capstyle='round')
            elif object.type == 'text':
                self.canvas.create_text(view_x, view_y, text=object.text, font=object.font, fill=object.color, anchor=object.anchor)
        self.canvas.pack()


class RenderedObject:
    def __init__(self, type, x, y, **kwargs):
        self.type = type  # rect/text/oval/line
        self.x = x
        self.y = y
        self.memory_id = id(self)
        self.options = kwargs
        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)
        self.x2 = kwargs.get('x2', self.x + self.width)
        self.y2 = kwargs.get('y2', self.y + self.height)
        self.text = kwargs.get('text', 'No text')
        self.image = kwargs.get('image', None)
        self.color = kwargs.get('color', None)
        self.font = kwargs.get('font', None)
        self.id = kwargs.get('id', -1)
        self.role = kwargs.get('role', None)
        self.anchor = kwargs.get('anchor', tk.CENTER)
        self.persistent = kwargs.get('persistent', False)
        self.borderwidth = kwargs.get('borderwidth', 0)
        self.zIndex = kwargs.get('zIndex', 1)

    def __repr__(self):
        return 'RenderedObject {type} at {x:n}, {y:n} at: {memory_id}'.format(**self.__dict__)

    def viewBox_coord(self, viewBox, scale):
        if scale == 1:
            viewX, viewY = viewBox['x'], viewBox['y']
        else:
            viewX, viewY = 0, 0
        return self.x - viewX, self.y - viewY, self.x2 - viewX, self.y2 - viewY
