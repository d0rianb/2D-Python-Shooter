#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk

class Canvas:
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        self.env = None
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height, bg='#EEE', highlightthickness=0)

    def scale(self, object):
        scale = self.env.scale #* self.env.width / self.env.viewArea['width']
        object.x *= scale
        object.y *= scale
        object.x2 *= scale
        object.y2 *= scale
        object.width *= scale
        object.height *= scale
        return object

    # @profile
    def render(self, stack):
        self.canvas.delete('all')
        for object in stack:
            object = self.scale(object)
            view_x, view_y, view_x2, view_y2 = object.viewBox_coord(self.env.viewArea)
            if object.type == 'rect':
                self.canvas.create_rectangle(view_x, view_y, view_x + object.width, view_y + object.height, fill=object.color, width=0)
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
        self.anchor = kwargs.get('anchor', tk.CENTER)
        self.zIndex = kwargs.get('zIndex', 1)

    def viewBox_coord(self, viewBox):
        return self.x - viewBox['x'], self.y - viewBox['y'], self.x2 - viewBox['x'], self.y2 - viewBox['y']
