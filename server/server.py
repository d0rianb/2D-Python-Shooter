#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import pickle
import json
import re

from message import Message

class Server(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.clients = []
        self.clients_to_read = []
        self.max_tickrate = 144
        self.tickrate = 0

    def decode(self, data):
        msg = data.decode('utf-8')
        if msg != '':
            print('MSG : --' + msg + '-- ')
            msg = json.loads(msg)
            return Message(msg['title'], msg['content'])

    def receive(self):
        for client_receive in self.clients_to_read:
            client = list(filter(lambda client: client.socket == client_receive, self.clients))[0]
            receive_data = client_receive.recv(10000)
            msg = self.decode(receive_data)
            if msg != None:
                client.receive(msg)

    def send_client_list(self):
        self.socket.sendall('test')

    def send_to(self, client):
        pass

    def send_all(self):
        pass
