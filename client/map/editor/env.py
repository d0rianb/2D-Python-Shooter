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

    def bind(self):
        self.fen.bind('<MouseWheel>', self.change_scale)
        self.fen.bind('<Button-1>', lambda *e: self.click('left', 'start'))
        self.fen.bind('<Button-2>', lambda *e: self.click('right', 'start'))
        self.fen.bind('<ButtonRelease-1>', lambda *e: self.click('left', 'end'))
        self.fen.bind('<ButtonRelease-2>', lambda *e: self.click('right', 'end'))
        keyboard.on_press_key('delete', self.delete_all)
        keyboard.on_press_key('enter', self.axial_symmetry)
        keyboard.on_press_key('t', self.semi_axial_symmetry)
        keyboard.on_press_key('m', self.map.save)
        keyboard.on_press_key('l', lambda *e: self.map.save(e, compiled=True))
        keyboard.on_press_key('&', lambda *e: self.change_scale(value=1))
        keyboard.on_press_key('é', lambda *e: self.change_scale(value=self.viewArea['width']/self.canvas.width))

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
            if obj.rel_x == rel_x and obj.rel_y == rel_y:
                return obj
        return False

    def optimize(self):
        duplicate = []
        for rect in self.objects:
            for other in self.objects:
                if rect == other and rect is not other:
                    duplicate.append(rect)
        print(duplicate)
        for dup in duplicate:
            self.objects.remove(dup)

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
                    rect.rel_x, rect.rel_y = obj.rel_x, obj.rel_y
                    try:
                        while line_array[index+1]:
                            rect.rel_width += 1
                            del line_array[index+1]
                        line_rects.append(rect)
                    except IndexError:
                        print(self.objects)
        i = 0
        while i < len(line_rects):
            cell = line_rects[i]
            has_merged = False
            for other in line_rects:
                if cell.rel_x == other.rel_x and cell.rel_width == other.rel_width and cell.rel_y + cell.rel_height == other.rel_y and cell != other:
                    rect = Rect(0, cell.rel_x, cell.rel_y, cell.rel_width, cell.rel_height + other.rel_height, self.map)
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

    def semi_axial_symmetry(self, *event):
        self.objects = [rect for rect in self.objects if rect.rel_x + rect.rel_width <= self.map.grid['x'] // 4 and rect.rel_y + rect.rel_height <= self.map.grid['y'] // 4]
        for rect in self.objects:
            if rect.rel_x + rect.rel_width <= self.map.grid['x'] // 4 and rect.rel_y + rect.rel_height <= self.map.grid['y'] // 4:
                rect.color = 'green'
            new_x = self.map.grid['x'] / 2 - rect.rel_x - 1
            new_y = self.map.grid['y'] / 2 - rect.rel_y - 1
            new_rect_x = Rect(-1, new_x, rect.rel_y, rect.rel_width, rect.rel_height, self.map)
            new_rect_y = Rect(-1, rect.rel_x, new_y, rect.rel_width, rect.rel_height, self.map)
            new_rect_both = Rect(-1, new_x, new_y, rect.rel_width, rect.rel_height, self.map)
            new_rects = [new_rect_x, new_rect_y, new_rect_both]
            for new in new_rects:
                already_exist = False
                for rect in self.objects:
                    if rect == new and rect is not new:
                        already_exist = True
                if not already_exist:
                    self.objects.append(new)

    def axial_symmetry(self, *event, axis='both'):
        for rect in self.objects:
            if rect.rel_x + rect.rel_width <= self.map.grid['x'] // 2 and rect.rel_y + rect.rel_height <= self.map.grid['y'] // 2:
                new_x = self.map.grid['x'] - rect.rel_x - 1
                new_y = self.map.grid['y'] - rect.rel_y - 1
                new_rects = []
                if axis == 'x' or axis == 'both':
                    new_rect_x = Rect(-1, new_x, rect.rel_y, rect.rel_width, rect.rel_height, self.map)
                    new_rects.append(new_rect_x)
                if axis == 'y' or axis == 'both':
                    new_rect_y = Rect(-1, rect.rel_x, new_y, rect.rel_width, rect.rel_height, self.map)
                    new_rects.append(new_rect_y)
                if axis == 'both':
                    new_rect_both = Rect(-1, new_x, new_y, rect.rel_width, rect.rel_height, self.map)
                    new_rects.append(new_rect_both)

                for new in new_rects:
                    already_exist = False
                    for rect in self.objects:
                        if rect == new and rect is not new:
                            already_exist = True
                    if not already_exist:
                        self.objects.append(new)

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
