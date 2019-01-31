#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Player:
    def __init__(self, id, x, y, size, health, alive):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.health = health
        self.alive = True
