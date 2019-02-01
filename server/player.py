#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Player:
    def __init__(self, id, x, y, dir, size, health):
        self.id = id
        self.x = x
        self.y = y
        self.dir = dir
        self.size = size
        self.health = health
        self.alive = self.health > 0

    def toJSON(self):
        object = {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'dir': self.dir,
            'health': self.health
        }
        return json.dumps(object)
