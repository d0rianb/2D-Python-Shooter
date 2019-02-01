#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import json
import time
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
                    already_connect = False
                    for client in self.clients:
                        if client.ip == addr[0]:
                            already_connect = True
                            old_client = client
                    if already_connect:
                        self.clients.remove(old_client)
                        print('[WARNING] {} is already connected'.format(addr[0]))

                    client_id = len(self.clients)+1
                    new_client = Client(client_id, message, addr)
                    self.clients.append(new_client)
                    self.send_message('response_id', {'id': client_id}, addr[0], addr[1])

                elif message['title'] == 'update_infos':
                    for client in self.clients:
                        if client.id == message['content']['id']:
                            client.player.x = message['content']['x']
                            client.player.y = message['content']['y']
                            client.player.dir = message['content']['dir']
                            client.player.health = message['content']['health']
                            client.ping = time.time() - message['timecode']

            except KeyError:
                print("[WARNING] : Json from %s:%s is not valid" % addr)
            except ValueError:
                print("[WARNING] : Message from %s:%s is not valid json string" % addr)

            for client in self.clients:
                players_array = [client.player.toJSON() for client in self.clients]
                self.send_message('players_array', players_array, client.ip, client.port)


    def send_message(self, title, content, ip, port):
        message = {
            'title': title,
            'content': content,
            'timecode': time.time()
        }
        encoded = json.dumps(message).encode('utf-8')
        self.socket.sendto(encoded, (ip, port))


    def end(self, *event):
        self.is_running = False
        if self.socket:
            self.socket.close()
