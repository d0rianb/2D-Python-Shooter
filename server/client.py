#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from player import Player

class Client:
    def __init__(self, id, message, addr, server):
        content = message['content']
        self.id = id
        self.name = content['name']
        self.ip = addr[0]
        self.port = addr[1]
        self.server = server
        self.player = Player(self.id, content['x'], content['y'], content['dir'], content['size'], content['health'], self.name)
        self.ping = 0
        self.server.clients.append(self)
        logging.info('New Connection : {}:{} as {}'.format(self.ip, self.port, self.name))

    def update_player(self, message):
        self.player.x = message['content']['x']
        self.player.y = message['content']['y']
        self.player.dir = message['content']['dir']
        self.player.health = message['content']['health']
        self.ping = self.server.time() - message['infos']['timestamp']
