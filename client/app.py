#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkFont
import socket
import random

from player import Player, Target
from env import Env
from interface import Interface
from client import Client
from map.map import Map

GAME_NAME = '2PQSTD'

SERVER_HOST = '192.168.1.142'
SERVER_PORT = 12800

class App:
    def __init__(self, player_name):
        self.name = player_name
        self.fen = tk.Tk()
        self.init()

    def init(self):
        self.width, self.height = self.fen.winfo_screenwidth(), self.fen.winfo_screenheight()
        self.canvas = tk.Canvas(self.fen, width=self.width, height=self.height, bg='#F1E7DC', highlightthickness=0)
        self.env = Env(self.fen, self.width, self.height, self.canvas)
        self.map = Map(self.env, 'map1.txt', 'Test')
        self.player = Player(0, 50, 50, self.env, self.name, own=True)
        self.interface = Interface(self.player, self.env)

    def start(self):
        self.env.update()
        self.fen.mainloop()

    def restart(self):
        self.fen.destroy()
        self.run()


class LocalGame(App):
    def __init__(self, player_name, difficulty):
        App.__init__(self, player_name)
        self.difficulty = difficulty
        self.fen.title(GAME_NAME + ' - Local')
        self.fen.bind('<Key-g>', self.restart)

    def generate_target(self):
        for i in range(self.difficulty):
            Target(i, random.randint(150, self.width - 150), random.randint(150, self.height - 150), self.env, level=self.difficulty)


class OnlineGame(App):
    def __init__(self, player_name):
        App.__init__(self, player_name)
        self.connection = None
        self.client = None
        self.fen.title(GAME_NAME + ' - Multi')

    def connect(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client = Client(self.connection, self.player, ip, port)
        self.client.send_connection_info()


class SplashScreen:
    def __init__(self, online_callback, offline_callback):
        self.fen = tk.Tk()
        self.online_callback = online_callback
        self.offline_callback = offline_callback

    def create_window(self):
        self.fen.title('Bievenue dans ' + GAME_NAME)
        self.fen.attributes("-topmost", True)
        self.width, self.height = self.fen.winfo_screenwidth(), self.fen.winfo_screenheight()
        L, H = self.width / 3, self.height / 2
        X, Y = (self.width - L) / 2, (self.height - H) / 2
        self.fen.geometry('%dx%d%+d%+d' % (L,H,X,Y))
        self.fen.resizable(width=False, height=False)

        title_font = tkFont.Font(family='Avenir Next', size=30, weight='bold')
        subtitle_font = tkFont.Font(family='Avenir Next', size=20, weight='normal')
        regular_font = tkFont.Font(family='Avenir Next', size=15, weight='normal')

        title = tk.Label(self.fen, text='Bievenue dans ' + GAME_NAME, font=title_font)
        subtitle = tk.Label(self.fen, text='Sélectionnez le mode de jeu : ', font=subtitle_font)

        name_var = tk.StringVar(self.fen, value='Dorian')
        server_ip_var = tk.StringVar(self.fen, value=SERVER_HOST)
        server_port_var = tk.StringVar(self.fen, value=SERVER_PORT)
        difficulty_var = tk.IntVar(self.fen, value=5)

        name_label = tk.Label(self.fen, text='Nom : ', font=regular_font)
        name_entry = tk.Entry(self.fen, textvariable=name_var, width=20)

        server_ip_label = tk.Label(self.fen, text='Adresse IP du serveur : ', font=regular_font)
        server_port_label = tk.Label(self.fen, text='Port du server : ', font=regular_font)
        server_ip_entry = tk.Entry(self.fen, textvariable=server_ip_var, width=20)
        server_port_entry = tk.Entry(self.fen, textvariable=server_port_var, width=20)

        difficulty_label = tk.Label(self.fen, text='Difficultée : ', font=regular_font)
        difficulty_scale = tk.Scale(self.fen, variable=difficulty_var, orient='horizontal', from_=0, to=10, resolution=1, length=200, relief=tk.FLAT)

        PvE_button = tk.Button(self.fen, text='Local', command=lambda: handle_click('PvE'), padx=30, pady=20, relief=tk.FLAT)
        PvP_button = tk.Button(self.fen, text='Multi', command=lambda: handle_click('PvP'), padx=30, pady=20, relief=tk.FLAT)

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

        def handle_click(mode):
            self.fen.destroy()
            if mode == 'PvE':
                self.offline_callback(name_var.get(), difficulty_var.get())
            elif mode == 'PvP':
                self.online_callback(name_var.get(), server_ip_var.get(), int(server_port_var.get()))


    def start(self):
        self.fen.mainloop()
