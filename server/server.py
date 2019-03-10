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

from client import Client

SERVER_FREQ = 60 # Hz

class Server(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = None
        self.clients = []
        self.max_tickrate = 144
        self.tick = 0
        self.is_running = True

        ## Logging system
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d | [%(levelname)s] : %(message)s', datefmt='%X')
        # formatter = logging.Formatter('%(message)s', datefmt='%X')
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    def time(self):
        return time.time()

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(0)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)

        logging.info('Server is running on port {}'.format(self.port))
        self.start_time = self.time()
        self.update()

    def update(self):
        if not self.is_running: return
        start_time = self.time()
        self.tick += 1

        try:
            client_sock, address = self.socket.accept()
            self.new_connection(client_sock, address)
        except Exception as e:
            pass

        players_array = [client.player.toJSON() for client in self.clients if client.player]
        # logging.info(players_array)
        if len(players_array) > 0:
            for client in self.clients:
                client.send('players_array', players_array)


        # if self.tick % 60 == 0:
        #     logging.info((self.time() - self.start_time) * 60 / self.tick)
        delta_time = self.time() - start_time
        delta_time = 1/SERVER_FREQ - delta_time

        threading.Timer(delta_time, self.update).start()

    def new_connection(self, client_socket, addr):
        reconnect = False
        for client in self.clients:
            if client.ip == addr[0]:
                reconnect = True
                old_client = client
        if reconnect:
            self.clients.remove(old_client)
            logging.info('{} is reconnecting'.format(addr[0]))

        client_id = len(self.clients) + 1
        client = Client(client_id, client_socket, addr, self)
        client.start()

    def end(self, *event):
        self.is_running = False
        if self.socket:
            self.socket.close()
