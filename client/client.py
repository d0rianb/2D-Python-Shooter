#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

class Client:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.player = None
        self.id = 0
