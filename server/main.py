#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import threading
import select
import json
from server import Server
from client import Client

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12801

server = Server(SERVER_IP, SERVER_PORT)
server.start()
if not server.is_running:
    server.end()
