#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from client import Client

class Game:
    def __init__(self, server, map):
        self.server = server
        self.map = map
        self.width = self.map.width
        self.height = self.map.height
        self.last_tickrate = 0
        self.tickrate = 0
        self.players = []
        self.alive = []
        self.shoots = []

    def add_shoot(self, x, y, dir, weapon):  ## a suppr
        Tir(x, y, dir, weapon, self)

    def manage_shoots(self):
        for shoot in self.shoots:
            if shoot.x < 0 or shoot.x > self.width or shoot.y < 0 or shoot.y > self.height:
                self.shoots.remove(shoot)
            else:
                shoot.update()

    def update(self):
        self.tickrate = 1 / (time.time() - self.last_tickrate)
        self.last_tickrate = time.time()
        self.manage_shoots()
