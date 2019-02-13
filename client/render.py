#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk

class Canvas:
    def __init__(self, parent, width , height):
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height, bg='#F1E7DC', highlightthickness=0)

    def render(self, stack):
        self.canvas.delete('all')
        for object in stack:
            if object.type == 'rect':
                self.canvas.create_rectangle(object.x, object.y, object.x + object.width, object.y + object.height,
                    fill=object.color,
                    width=0)
            elif object.type == 'oval':
                self.canvas.create_oval(object.x, object.y, object.x2, object.y2,
                    fill=object.color,
                    width=0)
            elif object.type == 'line':
                self.canvas.create_line(object.x, object.y, object.x2, object.y2,
                    capstyle='round')
            elif object.type == 'text':
                self.canvas.create_text(object.x, object.y,
                    text=object.text,
                    font=object.font,
                    fill=object.color,
                    anchor=object.anchor)
        self.canvas.pack()


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
        self.font = kwargs.get('font', None)
        self.anchor = kwargs.get('anchor', None)
        self.zIndex = kwargs.get('zIndex', 1)
