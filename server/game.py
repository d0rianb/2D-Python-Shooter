#!/usr/bin/env python
# -*- coding: utf-8 -*-

from client import Client

class Game:
    def __init__(self, server):
        self.server = server
        self.players = []
        self.alive = []

    def update(self):
        pass
