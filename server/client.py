#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import threading

from message import Message
from player import Player

class Client:
    def __init__(self, message, addr):
        content = message['content']
        self.id = content['id']
        self.name = content['name']
        self.ip = addr[0]
        self.port = addr[1]
        self.player = Player(self.id, content['x'], content['y'], content['dir'], content['size'], content['health'])
        print('[INFO] New Connection : {}:{} as {}'.format(self.ip, self.port, self.name))
