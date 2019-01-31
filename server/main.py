#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import threading
import select
import json
from server import Server
from client import Client

SERVER_PORT = 12801
SERVER_IS_RUNNING = True

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', SERVER_PORT))
socket.listen(5)

server = Server(socket)
print('Server is running in port {}'.format(SERVER_PORT))

while SERVER_IS_RUNNING:
        wait_connections, wlist, xlist = select.select([socket], [], [], 0.05)

        for connection in wait_connections:
            (client_socket, (ip, port)) = socket.accept()
            Client(ip, port, client_socket, server)

        try:
            server.clients_to_read, wlist, xlist = select.select([client.socket for client in server.clients], [], [], 0.05)
            server.receive()
        except select.error:
            pass
        server.send_client_list()


print("Close")
client.close()
stock.close()
