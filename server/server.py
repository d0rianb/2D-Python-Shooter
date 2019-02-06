#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import threading
import json
import datetime
import keyboard
import logging
import time
import multiprocessing

from client import Client


class Server(threading.Thread):
    def __init__(self,ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = None
        self.clients = []
        self.max_tickrate = 144
        self.tick = 0
        self.tickrate = 0
        self.is_running = True
        self.pool = multiprocessing.Pool(processes=1)

        ## Logging system
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d | [%(levelname)s] : %(message)s', datefmt='%X')
        # formatter = logging.Formatter('%(message)s', datefmt='%X')
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        keyboard.on_press_key('k', self.end)

    def time(self):
        # return datetime.datetime.utcnow().timestamp() * 1000
        return time.time()

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(0)

        logging.info('Server is running on port {}'.format(self.port))

        delta_tick = 0
        while self.is_running:
            self.tick += 1
            self.tickrate = int(1 / (self.time() - delta_tick))
            delta_tick = self.time()
            try:
                data, addr = self.socket.recvfrom(1024)
                message = json.loads(data)
                if message['title'] == 'connect_infos':
                    self.new_connection(message, addr)

                elif message['title'] == 'update_position':
                    self.update_position(message)
            except BlockingIOError:
                pass

            ## Send players position
            for client in self.clients:
                players_array = [client.player.toJSON() for client in self.clients]
                self.pool.apply_async(self.send_message, ['players_array', players_array, client.ip, client.port])
                #self.send_message('players_array', players_array, client.ip, client.port)

    def new_connection(self, message, addr):
        reconnect = False
        for client in self.clients:
            if client.ip == addr[0]:
                reconnect = True
                old_client = client
        if reconnect:
            self.clients.remove(old_client)
            logging.info('{} is reconnecting'.format(addr[0]))

        client_id = len(self.clients) + 1
        Client(client_id, message, addr, self)
        self.send_message('response_id', {'id': client_id}, addr[0], addr[1])

    def update_position(self, message):
        for client in self.clients:
            if client.id == message['from']:
                client.update_player(message)

    def send_message(self, title, content, ip, port):
        message = {
            'title': title,
            'content': content,
            'infos': { 'timestamp': self.time() }
        }
        encoded = json.dumps(message).encode('utf-8')
        self.socket.sendto(encoded, (ip, port))


    def end(self, *event):
        self.is_running = False
        if self.socket:
            self.socket.close()
