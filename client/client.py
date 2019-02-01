#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import time

class Client:
    def __init__(self, connection,  player, ip, port):
        self.connection = connection
        self.player = player
        self.player.client = self
        self.id = 0
        self.ip = ip
        self.port = port
        self.ping = 0
        self.connection.setblocking(0)

    def encode(self, message):
        return json.dumps(message).encode('utf-8')

    def send_message(self, title, content={}):
        message = {
            'from': self.player.id,
            'title': title,
            'content': content,
            'timecode': time.time()
        }
        self.connection.sendto(self.encode(message), (self.ip, self.port))

    def send_position(self):
        content = {
            'id': self.player.id,
            'x': self.player.x,
            'y': self.player.y,
            'dir': self.player.dir,
            'health': self.player.health
        }
        self.send_message('update_infos', content)

    def send_connection_info(self):
        content = {
            'id': self.player.id,
            'name': self.player.name,
            'x': self.player.x,
            'y': self.player.y,
            'dir': self.player.dir,
            'size': self.player.size,
            'health': self.player.health,
            'alive': self.player.alive
        }
        self.send_message('connect_infos', content)

    def receive(self):
        try:
            data = self.connection.recv(256)
            message = json.loads(data.decode('utf-8'))

            self.ping = time.time() - message['timecode']

            if message['title'] == 'players_array':
                print(message)
                players_array = [json.loads(player) for player in message['content']]
                for player in self.player.env.players:
                    for new_player in players_array:
                        if player.id == new_player['id'] and not player.own:
                            player.x = new_player['x']
                            player.y = new_player['y']
                            player.health = new_player['health']

            if message['title'] == 'response_id':
                self.player.id = message['content']['id']
        except BlockingIOError:
            pass

    def disconnect(self):
        self.connection.close()
