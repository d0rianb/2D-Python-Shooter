#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import time
import datetime
import socket
import threading
import json

from player import Player

SERVER_FREQ = 60 # Hz

class Client(threading.Thread):
    def __init__(self, connection,  player, ip, port):
        threading.Thread.__init__(self)
        self.id = 0
        self.connection = connection
        self.player = player
        self.player.client = self
        self.ip = ip
        self.port = port
        self.connected = False
        self.ping = 0
        self.connection.setblocking(0)

    def encode(self, message):
        return json.dumps(message).encode('utf-8')

    def time(self):
        # return datetime.datetime.utcnow().timestamp() * 1000
        return time.time()


    def send_message(self, title, content={}):
        message = {
            'from': self.player.id,
            'title': title,
            'content': content,
            'infos': {
                'timestamp': self.time()
            }
        }
        self.connection.sendto(self.encode(message), (self.ip, self.port))

    def send_position(self):
        content = {
            'x': self.player.x,
            'y': self.player.y,
            'dir': self.player.dir,
            'health': self.player.health
        }
        if self.connected:
            self.send_message('update_position', content)

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

    def run(self):
        self.receive()

    def receive(self):
        start_time = self.time()
        try:
            data = self.connection.recv(4096)
            message = json.loads(data.decode('utf-8'))
            self.ping = self.time() - message['infos']['timestamp']

            if message['title'] == 'players_array':
                players_array = [json.loads(player) for player in message['content']]
                for new_player in players_array:
                    player_is_new = True
                    for player in self.player.env.players:
                        if player.id == new_player['id'] and not player.own:
                            player_is_new = False
                            player.x = new_player['x']
                            player.y = new_player['y']
                            player.dir = new_player['dir']
                            player.health = new_player['health']
                    if player_is_new and new_player['id'] != self.player.id:
                        Player(new_player['id'], new_player['x'], new_player['y'], self.player.env, new_player['name'])


            if message['title'] == 'response_id':
                self.player.id = message['content']['id']
                self.connected = True
                self.player.message('global_info', 'Connected to {}:{}'.format(self.ip, self.port), duration=1.5)
                print('Connected to {}:{}'.format(self.ip, self.port))
        except BlockingIOError:
            pass

        delta_time = self.time() - start_time
        delta_time = 1/(2*SERVER_FREQ) - delta_time
        threading.Timer(delta_time, self.receive).start()

    def disconnect(self):
        self.connection.close()
