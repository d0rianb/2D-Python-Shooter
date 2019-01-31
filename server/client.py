#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from message import Message
from player import Player

class Client():
    def __init__(self, ip, port, client_socket, server):
        self.id = 0
        self.name = ''
        self.ip = ip
        self.port = port
        self.socket = client_socket
        self.server = server
        self.player = None
        self.server.clients.append(self)
        print('New Connection : {}:{}'.format(self.ip, self.port))

    def receive(self, message):
        title = message.title
        content = message.content
        if title == 'connect_infos':
            self.id = content['id']
            self.name = content['name']
            self.player = Player(self.id, content['x'], content['y'], content['size'], content['health'], content['alive'])
        if title == 'update_infos':
            print('update_infos')
