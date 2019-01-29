#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

class Client(threading.Thread):
    def __init__(self, ip, port, client_socket, server):
        threading.Thread.__init__(self)
        self.id = 0
        self.ip = ip
        self.port = port
        self.client_socket = client_socket
        self.server = server
        self.server.clients.append(self)
        print('New Connection : {}:{}'.format(self.ip, self.port))
