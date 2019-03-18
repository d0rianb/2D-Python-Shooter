#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import threading
import logging

from player import Player
from message import Message

SERVER_FREQ = 240 # Hz

class Client(threading.Thread):
    def __init__(self, id, socket, addr, server):
        threading.Thread.__init__(self)
        # content = message['content']
        self.id = id
        self.name = ''#content['name']
        self.ip = addr[0]
        self.port = addr[1]
        self.socket = socket
        self.server = server
        self.player = None
        self.ping = 0
        self.is_connected = True
        self.server.clients.append(self)
        self.send('response_id', {'id': self.id})
        logging.info('New Connection from : {}:{}'.format(self.ip, self.port))

    def run(self):
        self.update()

    def update(self):
        start_time = time.time()
        self.receive()
        delta_time = time.time() - start_time
        delta_time = 1/(SERVER_FREQ) - delta_time
        threading.Timer(delta_time, self.update).start()

    def receive(self):
        try:
            data, addr = self.socket.recvfrom(1024)
            message = json.loads(data)
            if message['title'] == 'update_position':
                self.update_player(message)
            elif message['title'] == 'connect_infos':
                self.set_player_infos(message)
            elif message['title'] == 'close_connection':
                self.end_connection()

        except Exception as e:
            pass

    def send(self, title, content):
        msg = Message(title, content)
        if self.is_connected:
            try:
                self.socket.send(msg.encode())
            except BrokenPipeError:
                self.end_connection()

    def update_player(self, message):
        content = message['content']
        self.player.x = content['x']
        self.player.y = content['y']
        self.player.dir = content['dir']
        self.player.health = content['health']
        self.ping = self.server.time() - message['infos']['timestamp']

    def set_player_infos(self, message):
        content = message['content']
        self.name = content['name']
        self.player = Player(self.id, content['x'], content['y'], content['dir'], content['size'], content['health'], self.name)

    def end_connection(self, *message):
        self.is_connected = False
        self.socket.close()
        self.server.clients.remove(self)
        logging.info(f'{self.name} is disconnected')
