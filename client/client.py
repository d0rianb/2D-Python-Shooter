#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import pickle

class Client:
    def __init__(self, socket, player):
        self.socket = socket
        self.player = player
        self.id = 0

    def encode(self, message):
        print('send : ' + str(message))
        return json.dumps(message).encode('utf-8')

    def send_message(self, title, content=''):
        message = {
            'title': title,
            'content': content
        }
        self.socket.send(self.encode(message))

    def update_server(self):
        content = {
            'x': self.player.x,
            'y': self.player.y,
            'health': self.player.health
        }
        self.send_message('update_infos', content)


    def send_connection_info(self):
        content = {
            'id': self.player.id,
            'name': self.player.name,
            'x': self.player.x,
            'y': self.player.y,
            'size': self.player.size,
            'health': self.player.health,
            'alive': self.player.alive
        }
        self.send_message('connect_infos', content)
