#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import time
import datetime
import socket
import threading
import json

from player import OnlinePlayer

SERVER_FREQ = 60 # Hz
ENDING_CHAR = '!#'

class Client(threading.Thread):
    def __init__(self, connection, player, ip, port):
        threading.Thread.__init__(self)
        self.id = 0
        self.connection = connection
        self.player = player
        self.player.client = self
        self.ip = ip
        self.port = port
        self.connected = False
        self.ping = 0
        self.nb_msg_send = 0
        self.nb_msg_recv = 0
        self.nb_msg_lost = 0
        self.start_time = 0
        self.connection.connect((self.ip, self.port))
        self.connection.setblocking(0)

    def encode(self, message):
        return json.dumps(message).encode('utf-8')

    def time(self):
        return time.time()

    def send(self, title, content={}):
        message = {
            'from': self.player.id,
            'title': title,
            'content': content,
            'infos': {
                'timestamp': self.time()
            }
        }
        self.nb_msg_send += 1
        self.connection.send(self.encode(message))

    def send_position(self):
        content = {
            'x': self.player.x,
            'y': self.player.y,
            'dir': self.player.dir,
            'health': self.player.health
        }
        if self.connected:
            self.send('update_position', content)

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
        self.send('connect_infos', content)

    def stats(self):
        time_elapsed = time.time() - self.start_time
        print(f'''
            nb_msg_send : {self.nb_msg_send}
            nb_msg_recv : {self.nb_msg_recv}
            nb_msg_lost : {self.nb_msg_lost}
            real_msg_recv : {self.nb_msg_recv - self.nb_msg_lost}
            time_elapsed : {time_elapsed}

            msg_send/sec : {self.nb_msg_send / time_elapsed}
            msg_recv/sec : {(self.nb_msg_recv - self.nb_msg_lost) / time_elapsed}
        ''')

    def start(self):
        self.update()
        self.start_time = self.time()

    def receive(self):
        try:
            data = self.connection.recv(4096)
            data_array = data.decode('utf-8').split(ENDING_CHAR)
            for msg_data in data_array:
                self.parse_msg(msg_data)
        except BlockingIOError:
            pass

    def parse_msg(self, data):
        try:
            message = json.loads(data)
            self.nb_msg_recv += 1
            self.ping = self.time() - message['infos']['timestamp']
        except json.decoder.JSONDecodeError as e:
            self.nb_msg_lost += 1
            return

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
                    new = OnlinePlayer(new_player['id'], new_player['x'], new_player['y'], self.player.env, new_player['name'])


        if message['title'] == 'response_id':
            self.player.id = message['content']['id']
            self.connected = True
            self.player.message('global_info', 'Connected to {}:{}'.format(self.ip, self.port), duration=1.5)
            print('Connected to {}:{}'.format(self.ip, self.port))
            self.send_connection_info()

    def update(self):
        start_time = self.time()
        self.send_position()
        self.receive()
        # if self.nb_msg_recv >= 2000: # ~10s
        #     self.stats()
        #     return
        delta_time = self.time() - start_time
        delta_time = 1/(SERVER_FREQ) - delta_time
        threading.Timer(delta_time, self.update).start()

    def disconnect(self):
        self.connection.close()
