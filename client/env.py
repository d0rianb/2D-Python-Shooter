#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import sys
import os
import platform
import re
import time
from render import RenderedObject

class Env:
    def __init__(self, fen, width, height, canvas):
        self.fen = fen
        self.canvas = canvas
        self.width = width
        self.height = height
        self.ratio = width / height
        self.max_framerate = 144
        self.framerate = self.max_framerate
        self.last_frame_timestamp = 0
        self.players = []
        self.players_alive = []
        self.shoots = []
        self.tick = 0
        self.map = None
        self.interface = None
        self.debug = False
        self.rendering_stack = []
        self.platform = platform.system()
        self.GAME_IS_RUNNING = True
        self.GAME_IS_FOCUS = True
        self.viewArea = {
            'x': 0,
            'y': 0,
            'width': self.width,
            'height': self.height
        }
        self.fen.protocol("WM_DELETE_WINDOW", self.exit)

    def manageShoots(self):
        for shoot in self.shoots:
            if shoot.x < 0 or shoot.x > self.width or shoot.y < 0 or shoot.y > self.height:
                self.shoots.remove(shoot)
            else:
                shoot.update()

    def isMac(self):
        return self.platform == 'Darwin'

    def isWindows(self):
        return self.platform == 'Windows'

    def exit(self):
        self.GAME_IS_RUNNING = False
        for player in self.players:
            if player.client:
                player.client.disconnect()
        self.fen.destroy()
        sys.exit(0)

    def panic(self, *event):
        if self.GAME_IS_FOCUS:
            print('Exit with panic')
            if self.isMac():
                os.system("open -a IDLE ./ressources/TP-Info.py")
            self.exit()

    def update(self):
        self.GAME_IS_FOCUS = True if self.fen.focus_get() != None else False
        self.tick += 1
        for player in self.players_alive:
            player.update()

        self.players_alive = [player for player in self.players if player.alive]
        self.manageShoots()
        self.interface.update()
        self.render()

        if self.tick % 10 == 0:
            # Update viewArea
            self.viewArea['width'], self.viewArea['height'], *offset = map(lambda val: int(val), re.split(r'[+x]', self.fen.geometry()))
            # Manage Framerate
            end_time = time.time()
            framerate = int(10 / (end_time - self.last_frame_timestamp))
            self.framerate = framerate if framerate != 0 and framerate <= self.max_framerate else self.max_framerate
            self.last_frame_timestamp = end_time

        # Loop
        if self.GAME_IS_RUNNING:
            self.fen.after(1000 // self.max_framerate, self.update)


    def render(self):
        self.map.render()
        self.interface.render()
        for player in self.players:
            if player.alive:
                player.render()
        for shoot in self.shoots:
            shoot.render()

        self.rendering_stack = sorted(self.rendering_stack, key=lambda obj: obj.zIndex)

        self.canvas.delete('all')
        for object in self.rendering_stack:
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


        self.rendering_stack = []
        self.canvas.pack()
