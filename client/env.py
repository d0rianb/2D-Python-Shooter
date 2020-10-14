#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import sys
import os
import platform
import threading
import multiprocessing
import concurrent
import re
import time
import pprint
import random

from object.rect import Rect, Box
from object.object import Object
from render import RenderedObject
from collectible import Heal, LandMine
from stats import Stats

HEAL_NUMBER = 15
MINE_NUMBER = 20

SOUND_ALLOWS = True


class Env:
    def __init__(self, fen, map, canvas, max_framerate=60):
        self.fen = fen
        self.canvas = canvas
        self.map = map
        self.map.env = self
        self.width = self.map.width
        self.height = self.map.height
        self.scale = 1
        self.ratio = self.width / self.height
        self.max_framerate = max_framerate
        self.stats = Stats(self)
        self.own_player = None
        self.collectible = []
        self.players = []
        self.players_alive = []
        self.shoots = []
        self.rays = []
        self.sounds = []
        self.tick = 0
        self.interface = None
        self.debug = False
        self.rendering_stack = []
        self.platform = platform.system()
        self.GAME_IS_RUNNING = True
        self.GAME_IS_FOCUS = True
        self.optimize = True
        self.command_entry_focus = False
        self.canvas.env = self
        self.viewArea = {
            'x': 0,
            'y': 0,
            'width': self.fen.winfo_screenwidth(),
            'height': self.fen.winfo_screenheight()
        }
        for obj in self.map.objects:
            if isinstance(obj, Rect):
                obj.computed_values()
        for i in range(HEAL_NUMBER):
            self.collectible.append(Heal(i, random.randint(0, self.width), random.randint(0, self.height), self))
        for i in range(MINE_NUMBER):
            self.collectible.append(LandMine(i, random.randint(0, self.width), random.randint(0, self.height), self))

        self.fen.protocol("WM_DELETE_WINDOW", self.exit)
        self.fen.bind("<MouseWheel>", self.change_scale)

    def change_scale(self, *event, value=1):
        if event:
            event = event[0]
            if (self.scale >= 0.1 and event.delta > 0) or (self.scale <= 5 and event.delta < 0):
                self.scale -= event.delta / 100
        else:
            self.scale = value

    def toggle_optimization(self, value=None):
        if value:
            self.optimize = value
        else:
            self.optimize = not self.optimize

    def manage_shoots(self):
        for shoot in self.shoots:
            if shoot.x < 0 or shoot.x > self.width or shoot.y < 0 or shoot.y > self.height:
                self.shoots.remove(shoot)
            else:
                shoot.update()

    def manage_sounds(self):
        if not SOUND_ALLOWS:
            return
        for sound in self.sounds:
            if self.in_viewBox(sound.player) and self.own_player:
                dist = self.own_player.dist(sound.player)
                volume = abs(1 - (dist / (self.viewArea['width'] / 1.5)))
                sound.set_volume(volume)
                sound.play()
        self.sounds = []

    def find_by(self, attr, value):
        for player in self.players:
            if player.__dict__[attr] == value:
                return player

    def isMac(self):
        return self.platform == 'Darwin'

    def isWindows(self):
        return self.platform == 'Windows'

    def exit(self):
        self.GAME_IS_RUNNING = False
        for player in self.players:
            if player.own and player.client:
                player.client.disconnect()
        self.fen.destroy()

    def panic(self, *event):
        if self.GAME_IS_FOCUS:
            print('Exit with panic')
            if self.isMac():
                os.system("open -a IDLE ./ressources/TP-Info.py")
            self.exit()

    def background(self):
        self.rendering_stack.append(
            RenderedObject('rect', 0, 0, width=self.width, height=self.height, color='#F1E7DC', zIndex=1,
                           persistent=True))

    def in_viewBox(self, obj):
        viewBox = Box(self.viewArea['x'], self.viewArea['y'], self.viewArea['x'] + self.viewArea['width'],
                      self.viewArea['y'] + self.viewArea['height'])
        if isinstance(obj, RenderedObject):
            if obj.persistent: return True
            if obj.type == 'rect':
                return Object.intersect(viewBox, obj)
            elif obj.type == 'oval':
                return Object.intersect(viewBox, obj)
            elif obj.type == 'line':
                return obj.x >= viewBox.x and obj.y >= viewBox.y and obj.x2 <= viewBox.x2 and obj.y2 <= viewBox.y2
            elif obj.type == 'text':
                return True
            else:
                return True
        elif isinstance(obj, Object):
            return Object.intersect(viewBox, obj)
        elif obj.x and obj.y:
            return viewBox.x <= obj.x <= viewBox.x2 and viewBox.y <= obj.y <= viewBox.y2

    def add_render_object(self, render_object):
        if not self.optimize or self.in_viewBox(render_object):
            self.rendering_stack.append(render_object)

    @profile
    def update(self):
        if not self.GAME_IS_RUNNING: return
        self.tick += 1
        run_stats = self.tick % 10 == 0
        if run_stats: self.stats.frame_start()
        if len(self.players) > 0:
            for player in self.players_alive:
                player.update()
        self.players_alive = [player for player in self.players if player.alive]

        for ray in self.rays:
            ray.update()
        self.manage_shoots()
        self.manage_sounds()
        self.interface.update()
        self.render()

        if run_stats:
            self.GAME_IS_FOCUS = True if self.fen.focus_get() is not None else False
            self.viewArea['width'], self.viewArea['height'], *offset = map(lambda val: int(val),
                                                                           re.split(r'[+x]', self.fen.geometry()))
            self.stats.calculate_fps(sample=10)
            self.stats.frame_end()
        self.fen.after(1000 // self.max_framerate, self.update)

    @profile
    def render(self):
        ## Pre-Render
        self.background()
        self.map.render()
        self.interface.render()
        for player in self.players:
            if player.alive:
                player.render()
        for collectible in self.collectible:
            collectible.render()
        for shoot in self.shoots:
            shoot.render()
        for ray in self.rays:
            ray.render()

        if self.scale != 1:
            self.rendering_stack.append(
                RenderedObject('line', self.viewArea['x'], self.viewArea['y'], width=self.viewArea['width'], height=0,
                               zIndex=2))
            self.rendering_stack.append(
                RenderedObject('line', self.viewArea['x'], self.viewArea['y'], width=0, height=self.viewArea['height'],
                               zIndex=2))
            self.rendering_stack.append(
                RenderedObject('line', self.viewArea['x'] + self.viewArea['width'], self.viewArea['y'], width=0,
                               height=self.viewArea['height'], zIndex=2))
            self.rendering_stack.append(
                RenderedObject('line', self.viewArea['x'], self.viewArea['y'] + self.viewArea['height'],
                               width=self.viewArea['width'], height=0, zIndex=2))

        ## Canvas rendering
        rendering_stack = self.rendering_stack
        self.rendering_stack = sorted(rendering_stack, key=lambda obj: obj.zIndex)
        self.canvas.render(self.rendering_stack)

        ## Reset
        self.rendering_stack = []
