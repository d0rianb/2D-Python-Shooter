#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkFont
import os
import sys
import platform
import math
import random
import keyboard
import socket
import json

from player import Player, Target
from tir import Tir
from env import Env
from interface import Interface
from client import Client
from map.map import Map

GAME_NAME = '2PQSTD'
SERVER_HOST = '192.168.1.142'
SERVER_PORT = 12800


def start_local_game(name, difficulty=5):
    fen = tk.Tk()
    fen.title(GAME_NAME + ' - Local')
    width, height = fen.winfo_screenwidth(), fen.winfo_screenheight()

    canvas = tk.Canvas(fen, width=width, height=height, bg='#F1E7DC', highlightthickness=0)
    fen.bind('<Key-g>', lambda *args: restart(fen, name, difficulty))

    def restart(fen, name, difficulty):
        fen.destroy()
        start_local_game(name, difficulty)

    env = Env(fen, width, height, canvas)
    map = Map(env, 'map1.txt', 'Test')

    player = Player(0, 50, 50, env, name, own=True)

    for i in range(difficulty):
        Target(i, random.randint(150, width - 150), random.randint(150, height - 150), env, level=difficulty)

    interface = Interface(player, env)
    env.update()
    fen.mainloop()

def start_online_game(name, ip=SERVER_HOST, port=SERVER_PORT):
    print('Connection to {}:{}'.format(ip, port))
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    fen = tk.Tk()
    fen.title(GAME_NAME + ' - Multi')
    width, height = fen.winfo_screenwidth(), fen.winfo_screenheight()

    canvas = tk.Canvas(fen, width=width, height=height, bg='#F1E7DC', highlightthickness=0)
    fen.bind('<Key-g>', lambda *args: restart(fen))

    def restart(fen):
        fen.destroy()
        start_game('PvE')

    env = Env(fen, width, height, canvas)
    map = Map(env, 'map1.txt', 'Test')

    player = Player(0, 50, 50, env, name, own=True)
    client = Client(connection, player, ip, port)
    client.send_connection_info()

    interface = Interface(player, env)
    env.update()
    fen.mainloop()


def splash_screen():
    fen = tk.Tk()
    fen.title('Bievenue dans ' + GAME_NAME)
    fen.attributes("-topmost", True)
    width, height = fen.winfo_screenwidth(), fen.winfo_screenheight()
    L, H = width / 3, height / 2
    X, Y = (width - L) / 2, (height - H) / 2
    fen.geometry('%dx%d%+d%+d' % (L,H,X,Y))
    fen.resizable(width=False, height=False)

    title_font = tkFont.Font(family='Avenir Next', size=30, weight='bold')
    subtitle_font = tkFont.Font(family='Avenir Next', size=20, weight='normal')
    regular_font = tkFont.Font(family='Avenir Next', size=15, weight='normal')

    def handle_click(mode, fen):
        fen.destroy()
        if mode == 'PvE':
            start_local_game(name_var.get(), difficulty_var.get())
        elif mode == 'PvP':
            start_online_game(name_var.get(), server_ip_var.get(), int(server_port_var.get()))

    title = tk.Label(fen, text='Bievenue dans ' + GAME_NAME, font=title_font)
    subtitle = tk.Label(fen, text='Sélectionnez le mode de jeu : ', font=subtitle_font)

    name_var = tk.StringVar(fen, value='Dorian')
    server_ip_var = tk.StringVar(fen, value=SERVER_HOST)
    server_port_var = tk.StringVar(fen, value=SERVER_PORT)
    difficulty_var = tk.IntVar(fen, value=5)

    name_label = tk.Label(fen, text='Nom : ', font=regular_font)
    name_entry = tk.Entry(fen, textvariable=name_var, width=20)

    server_ip_label = tk.Label(fen, text='Adresse IP du serveur : ', font=regular_font)
    server_port_label = tk.Label(fen, text='Port du server : ', font=regular_font)
    server_ip_entry = tk.Entry(fen, textvariable=server_ip_var, width=20)
    server_port_entry = tk.Entry(fen, textvariable=server_port_var, width=20)

    difficulty_label = tk.Label(fen, text='Difficultée : ', font=regular_font)
    difficulty_scale = tk.Scale(fen, variable=difficulty_var, orient='horizontal', from_=0, to=10, resolution=1, length=200, relief=tk.FLAT)

    PvE_button = tk.Button(fen, text='Local', command=lambda: handle_click('PvE', fen), padx=30, pady=20, relief=tk.FLAT)
    PvP_button = tk.Button(fen, text='Multi', command=lambda: handle_click('PvP', fen), padx=30, pady=20, relief=tk.FLAT)

    ## LAYOUT ##
    title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    subtitle.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

    name_label.place(relx=0.1, rely=0.33, anchor=tk.W)
    name_entry.place(relx=0.8, rely=0.33, anchor=tk.E)

    server_ip_label.place(relx=0.1, rely=0.45, anchor=tk.W)
    server_port_label.place(relx=0.1, rely=0.57, anchor=tk.W)

    server_ip_entry.place(relx=0.9, rely=0.45, anchor=tk.E)
    server_port_entry.place(relx=0.9, rely=0.57, anchor=tk.E)

    difficulty_label.place(relx=0.1, rely=0.74, anchor=tk.W)
    difficulty_scale.place(relx=0.8, rely=0.71, anchor=tk.E)

    PvE_button.place(relx=0.3, rely=0.9, anchor=tk.W)
    PvP_button.place(relx=0.7, rely=0.9, anchor=tk.E)
    fen.mainloop()

def settings():
    pass

if __name__ == '__main__':
    splash_screen()
    # start_game('PvE')
    sys.exit(0)
