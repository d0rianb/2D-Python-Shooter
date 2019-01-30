#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.clients = []
        self.max_tickrate = 144
        self.tickrate = 0

    def send_to(self, client):
        pass

    def send_all(self):
        pass
