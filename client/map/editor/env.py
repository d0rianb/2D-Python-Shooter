#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import sys
import os
import platform
import re
import time
import keyboard
import cv2

from threading import Timer
from render import RenderedObject
from object.rect import Rect
from object.circle import Circle

class Env:
    def __init__(self, fen, canvas, width, height):
        self.fen = fen
        self.canvas = canvas
        self.canvas.env = self
        self.width = width
        self.height = height
        self.camera = None
        self.interface = None
        self.map = None
        self.objects = []
        self.rendering_stack = []
        self.max_framerate = 144
        self.framerate = self.max_framerate
        self.last_frame_timestamp = 0
        self.tick = 0
        self.scale = 1
        self.left_click_pressed = False
        self.right_click_pressed = False
        self.viewArea = {
            'x': 0,
            'y': 0,
            'width': self.fen.winfo_screenwidth(),
            'height': self.fen.winfo_screenheight()
        }
        self.fen.bind('<MouseWheel>', self.change_scale)
        self.fen.bind('<Button-1>', lambda *e: self.click('left', 'start'))
        self.fen.bind('<Button-2>', lambda *e: self.click('right', 'start'))
        self.fen.bind('<ButtonRelease-1>', lambda *e: self.click('left', 'end'))
        self.fen.bind('<ButtonRelease-2>', lambda *e: self.click('right', 'end'))
        keyboard.on_press_key('delete', self.delete_all)
        keyboard.on_press_key('m', self.merge_rect)

    def change_scale(self, *event, value=1):
        if event:
            event = event[0]
            if (self.scale >= 0.1 and event.delta > 0) or (self.scale <= 5 and event.delta < 0):
                self.scale -= event.delta/100
        else:
            self.scale = value

    def objects_contains(self, object):
            for obj in self.objects:
                if obj.x == object.x and obj.x2 == object.x2 and obj.y == object.y and obj.y2 == object.y2:
                    return True
            return False

    def click(self, side, state):
        bool = True if state == 'start' else False
        if side == 'left':
            self.left_click_pressed = bool
        elif side == 'right':
            self.right_click_pressed = bool


    def add_rect(self, display_x, display_y):
        x, y = (self.viewArea['x'] + display_x)/self.scale, (self.viewArea['y'] + display_y)/self.scale
        for col in range(self.map.grid['x']):
            for line in range(self.map.grid['y']):
                rect = Rect(1, col, line, 1, 1, self.map)
                if rect.contains(x, y) and not self.objects_contains(rect):
                        self.objects.append(rect)
                        return

    def remove_rect(self, display_x, display_y):
        x, y = (self.viewArea['x'] + display_x)/self.scale, (self.viewArea['y'] + display_y)/self.scale
        for obj in self.objects:
            if obj.contains(x, y):
                self.objects.remove(obj)
                return

    def find_rect(self, rel_x, rel_y):
        for obj in self.objects:
            if obj.relative_x == rel_x and obj.relative_y == rel_y:
                return obj
        return False

    def merge_rect(self, *event):
        line_rects = []
        for line in range(self.map.grid['y']):
            line_array = []
            for col in range(self.map.grid['x']):
                rect = self.find_rect(col, line)
                if rect:
                    line_array.append(rect)
                else:
                    line_array.append(None)
            for (index, obj) in enumerate(line_array):
                rect = Rect(-1, 0, 0, 1, 1, self.map)
                if obj:
                    rect.id = 99
                    rect.relative_x, rect.relative_y = obj.relative_x, obj.relative_y
                    while line_array[index+1]:
                        rect.relative_width += 1
                        del line_array[index+1]
                    line_rects.append(rect)
        i = 0
        while i < len(line_rects):
            cell = line_rects[i]
            has_merged = False
            for other in line_rects:
                if cell.relative_x == other.relative_x and cell.relative_width == other.relative_width and cell.relative_y + cell.relative_height == other.relative_y and cell != other:
                    rect = Rect(0, cell.relative_x, cell.relative_y, cell.relative_width, cell.relative_height + other.relative_height, self.map)
                    line_rects.append(rect)
                    del line_rects[line_rects.index(cell)]
                    del line_rects[line_rects.index(other)]
                    has_merged = True
            if has_merged:
                i = 0
            else:
                i += 1

        self.objects = []
        for rect in line_rects:
            rect.computed_values()
        self.objects = line_rects.copy()


    def delete_all(self, *event):
        self.objects = []

    def background(self):
        self.rendering_stack.append(RenderedObject('rect', 0, 0, width=self.width, height=self.height, color='#F1E7DC', zIndex=1))

    def update(self):
        pointer_x = self.fen.winfo_pointerx() - self.fen.winfo_rootx()
        pointer_y = self.fen.winfo_pointery() - self.fen.winfo_rooty()
        if self.left_click_pressed:
            self.add_rect(pointer_x, pointer_y)
        elif self.right_click_pressed:
            self.remove_rect(pointer_x, pointer_y)

        self.tick += 1
        for object in self.objects:
            if isinstance(object, Rect):
                rect = object
                self.rendering_stack.append(RenderedObject('rect', rect.x, rect.y, width=rect.width, height=rect.height, color=rect.color, borderwidth=1, zIndex=3))
            elif isinstance(object, Circle):
                circle = object
                self.rendering_stack.append(RenderedObject('oval', circle.x1, circle.y1, x2=circle.x2, y2=circle.y2, color=circle.color, zIndex=3))
        self.interface.update()
        self.camera.update()
        self.render()

        if self.tick % 10 == 0:
            self.GAME_IS_FOCUS = True if self.fen.focus_get() != None else False
            self.viewArea['width'], self.viewArea['height'], *offset = map(lambda val: int(val), re.split(r'[+x]', self.fen.geometry()))
            end_time = time.time()
            framerate = int(10 / (end_time - self.last_frame_timestamp))
            self.framerate = framerate if framerate != 0 and framerate <= self.max_framerate else self.max_framerate
            self.last_frame_timestamp = end_time

        self.fen.after(1000 // self.max_framerate, self.update)

    def render(self):
        self.background()
        self.camera.render()
        self.interface.render()
        self.map.display_grid()
        for object in self.objects:
            if isinstance(object, Rect):
                rect = object
                self.rendering_stack.append(RenderedObject('rect', rect.x, rect.y, width=rect.width, height=rect.height, color=rect.color))
            elif isinstance(object, Circle):
                circle = object
                self.rendering_stack.append(RenderedObject('oval', circle.x1, circle.y1, x2=circle.x2, y2=circle.y2, color=circle.color))

        self.rendering_stack.append(RenderedObject('text', self.viewArea['x'], self.viewArea['y'] - 15, text='View Box',anchor=tk.SW, color='#92959b'))
        self.rendering_stack.append(RenderedObject('line', self.viewArea['x'], self.viewArea['y'], width=self.viewArea['width'], height=0, zIndex=2))
        self.rendering_stack.append(RenderedObject('line', self.viewArea['x'], self.viewArea['y'], width=0, height=self.viewArea['height'], zIndex=2))
        self.rendering_stack.append(RenderedObject('line', self.viewArea['x'] + self.viewArea['width'], self.viewArea['y'], width=0, height=self.viewArea['height'], zIndex=2))
        self.rendering_stack.append(RenderedObject('line', self.viewArea['x'], self.viewArea['y'] + self.viewArea['height'], width=self.viewArea['width'], height=0, zIndex=2))

        ## Canvas rendering
        self.rendering_stack = sorted(self.rendering_stack, key=lambda obj: obj.zIndex)
        self.canvas.render(self.rendering_stack)
        self.rendering_stack = []
