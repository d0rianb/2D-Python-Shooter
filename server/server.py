#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import socketserver
import threading
import json
import re
import keyboard

from message import Message
from client import Client

class Server(threading.Thread):
    def __init__(self,ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = None
        self.clients = []
        self.max_tickrate = 144
        self.tickrate = 0
        self.is_running = True
        keyboard.on_press_key('k', self.end)

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))

        print('Server is running on port {}'.format(self.port))

        while self.is_running:
            try:
                data, addr = self.socket.recvfrom(1024)
            except socket.timeout:
                print('[ERROR] : Socket Timeout')
                continue

            try:
                message = json.loads(data)
            except:
                print('[ERROR] : Loading JSON')
            try:
                if message['title'] == 'connect_infos':
                    self.clients.append(Client(message, addr))
                elif message['title'] == 'update_infos':
                    for client in self.clients:
                        if client.id == message['content']['id']:
                            client.player.x = message['content']['x']
                            client.player.y = message['content']['y']
                            client.player.health = message['content']['health']

            except KeyError:
                print("[WARNING] : Json from %s:%s is not valid" % addr)
            except ValueError:
                print("[WARNING] : Message from %s:%s is not valid json string" % addr)


    def end(self, *event):
        self.is_running = False
        for client in self.clients:
            client.conn.close()
        if self.socket:
            self.socket.close()
