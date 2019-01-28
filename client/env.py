#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import re
import time
from renderedObject import RenderedObject

class Env:
    def __init__(self, fen, width, height, canvas):
        self.fen = fen
        self.canvas = canvas
        self.width = width
        self.height = height
        self.ratio = width / height
        self.max_framerate = 60
        self.framerate = self.max_framerate
        self.last_frame_timestamp = 0
        self.players = []
        self.shoots = []
        self.map = {}
        self.debug = False
        self.rendering_queue = []
        self.viewArea = {
            'x': 0,
            'y': 0,
            'width': self.width,
            'height': self.height
        }

    def manageShoots(self):
        for shoot in self.shoots:
            if shoot.x < 0 or shoot.x > self.width or shoot.y < 0 or shoot.y > self.height:
                self.shoots.remove(shoot)
            else:
                shoot.update()

    def update(self):
        self.canvas.delete('all')
        for player in self.players:
            player.update()
        self.manageShoots()
        self.render()
        self.viewArea['width'], self.viewArea['height'], *offset = map(lambda val: int(val), re.split(r'[+x]', self.fen.geometry())) # Update width&height
        end_time = time.time()
        framerate = int(1 / (end_time - self.last_frame_timestamp))
        self.framerate = framerate if framerate != 0 and framerate <= self.max_framerate else self.max_framerate
        self.last_frame_timestamp = end_time
        self.fen.after(1000 // self.max_framerate, self.update)

    def render(self):
        self.map.render()
        for player in self.players:
            if player.alive:
                player.render()
        for shoot in self.shoots:
            shoot.render(self.canvas)
        self.canvas.pack()
