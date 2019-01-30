#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import threading
import select
from server import Server
from client import Client

SERVER_PORT = 12800
SERVER_IS_RUNNING = True

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', SERVER_PORT))
socket.listen(5)

server = Server()

while SERVER_IS_RUNNING:

        wait_connections, wlist, xlist = select.select([socket],
        [], [], 0.05)

        for connection in wait_connections:
            (client_socket, (ip, port)) = socket.accept()
            Client(ip, port, client_socket, server)

        client_to_read = []
        try:
            client_to_read, wlist, xlist = select.select([client.client_socket for client in server.clients], [], [], 0.05)
        except select.error:
            pass
        else:
            for client in client_to_read:
                msg_recu = client.recv(1024)
                msg_recu = msg_recu.decode()
                if msg_recu != '':
                    print("Reçu {}".format(msg_recu))



print("Close")
client.close()
stock.close()
