#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform
import tkinter as tk
import tkinter.font as tkFont
import socket
import random
import keyboard
import json, pprint

from player import Player, Target
from env import Env
from interface import Interface, ChatInfo
from client import Client
from render import Canvas
from map.map import Map

GAME_NAME = '2PQSTD'
config_path = 'ressources/config/'

class App:
    def __init__(self, player_name):
        self.name = player_name
        self.fen = tk.Tk()
        self.config = {}
        self.init()

    def init(self):
        self.get_config()
        self.width, self.height = self.fen.winfo_screenwidth(), self.fen.winfo_screenheight()
        self.canvas = Canvas(self.fen, self.width, self.height)
        self.env = Env(self.fen, self.width, self.height, self.canvas, max_framerate=self.config['max_framerate'])
        self.map = Map(self.env, 'map1.txt', 'Test')
        self.player = Player(0, 50, 50, self.env, self.name, own=True, key=self.config['key_binding'])
        self.interface = Interface(self.player, self.env)
        self.chat = ChatInfo(self.env)

    def get_config(self):
        with open(os.path.join(config_path, 'config.json'), 'r') as settings_file:
            self.config = json.load(settings_file)
            # pprint.pprint(self.config)

    def start(self):
        self.env.update()
        self.fen.mainloop()


class LocalGame(App):
    def __init__(self, player_name, difficulty):
        App.__init__(self, player_name)
        self.difficulty = difficulty
        self.entry = None
        self.fen.title(GAME_NAME + ' - Local')
        self.fen.bind('<Key-g>', self.restart)

    def restart(self, *event): ## Doesn't work
        if self.env.command_entry_focus: return
        self.env.exit()
        self.start()

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
    def __init__(self, online_callback, offline_callback, settings_callback):
        self.fen = tk.Tk()
        self.config = {}
        self.online_callback = online_callback
        self.offline_callback = offline_callback
        self.settings_callback = settings_callback
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.get_config()

    def get_config(self):
        with open(os.path.join(config_path, 'config.json'), 'r') as settings_file:
            self.config = json.load(settings_file)

    def create_window(self):
        self.fen.title('Bievenue dans ' + GAME_NAME)
        self.fen.attributes('-topmost', True)
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

        name_var = tk.StringVar(self.fen, value=self.config['default_name'])
        server_ip_var = tk.StringVar(self.fen, value=self.config['default_ip'])
        server_port_var = tk.StringVar(self.fen, value=self.config['default_port'])
        difficulty_var = tk.IntVar(self.fen, value=self.config['default_difficulty'])

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

        settings_icon = tk.PhotoImage(file='{}/ressources/open_file.gif'.format(self.path))
        settings = tk.Button(self.fen, text='Settings',relief=tk.FLAT, command=lambda: self.settings_callback(self))

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

        settings.place(relx= 0.9, rely=0.9, anchor=tk.CENTER)

        def handle_click(mode):
            self.fen.destroy()
            if mode == 'PvE':
                self.offline_callback(name_var.get(), difficulty_var.get())
            elif mode == 'PvP':
                self.online_callback(name_var.get(), server_ip_var.get(), int(server_port_var.get()))


    def start(self):
        self.fen.mainloop()


class Settings:
    def __init__(self):
        self.config = {}
        self.new_config = {}
        self.platform = platform.system()
        self.get_config()
        self.create_window()

    def get_config(self):
        with open(os.path.join(config_path, 'config.json'), 'r') as file:
            self.config = json.load(file)
            self.new_config = self.config.copy()

    def create_window(self):
        self.fen = tk.Toplevel()
        width, height = self.fen.winfo_screenwidth(), self.fen.winfo_screenheight()
        L, H = width / 2.8, height / 2
        X, Y = (width - L) / 2, (height - H) / 2
        self.fen.geometry('%dx%d%+d%+d' % (L,H,X,Y))

        max_framerate = tk.IntVar(self.fen, value=self.config['max_framerate'])
        default_difficulty = tk.IntVar(self.fen, value=self.config['default_difficulty'])
        default_ip = tk.StringVar(self.fen, value=self.config['default_ip'])
        default_port = tk.IntVar(self.fen, value=self.config['default_port'])
        default_name = tk.StringVar(self.fen, value=self.config['default_name'])

        title_font = tkFont.Font(family='Avenir Next', size=30, weight='bold')

        title = tk.Label(self.fen, text='Paramètres', font=title_font)
        max_framerate_label = tk.Label(self.fen, text='Framerate Maximum (fps)')
        default_difficulty_label = tk.Label(self.fen, text='Difficulté par défaut (1-10)')
        default_name_label = tk.Label(self.fen, text='Nom')
        default_ip_label = tk.Label(self.fen, text='Adresse IP par défaut')
        default_port_label = tk.Label(self.fen, text='Port par défaut')

        def validate():
            self.new_config['max_framerate'] = max_framerate.get()
            self.new_config['default_difficulty'] = default_difficulty.get()
            self.new_config['default_ip'] = default_ip.get()
            self.new_config['default_port'] = default_port.get()
            self.new_config['default_name'] = default_name.get()
            with open(os.path.join(config_path, 'config.json'), 'w') as config:
                config.write(json.dumps(self.new_config))
            self.fen.destroy()

        max_framerate_entry = tk.Entry(self.fen, textvariable=max_framerate)
        default_difficulty_entry = tk.Entry(self.fen, textvariable=default_difficulty)
        default_name_entry = tk.Entry(self.fen, textvariable=default_name)
        default_ip_entry = tk.Entry(self.fen, textvariable=default_ip)
        default_port_entry = tk.Entry(self.fen, textvariable=default_port)
        keybinding = tk.Button(self.fen, text='Key Bind', command=self.setup_keybind)
        valider = tk.Button(self.fen, text='Valider', command=validate)

        ## LAYOUT ##
        title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        default_name_label.place(relx=0.1, rely=0.3, anchor=tk.W)
        default_difficulty_label.place(relx=0.1, rely=0.4, anchor=tk.W)
        default_ip_label.place(relx=0.1, rely=0.5, anchor=tk.W)
        default_port_label.place(relx=0.1, rely=0.6, anchor=tk.W)
        max_framerate_label.place(relx=0.1, rely=0.7, anchor=tk.W)

        default_name_entry.place(relx=0.9, rely=0.3, anchor=tk.E)
        default_difficulty_entry.place(relx=0.9, rely=0.4, anchor=tk.E)
        default_ip_entry.place(relx=0.9, rely=0.5, anchor=tk.E)
        default_port_entry.place(relx=0.9, rely=0.6, anchor=tk.E)
        max_framerate_entry.place(relx=0.9, rely=0.7, anchor=tk.E)
        keybinding.place(relx=0.4, rely=0.9, anchor=tk.CENTER)
        valider.place(relx=0.6, rely=0.9, anchor=tk.CENTER)

        self.fen.mainloop()

    def setup_keybind(self):
        self.key_fen = tk.Toplevel(self.fen)
        width, height = self.fen.winfo_screenwidth(), self.fen.winfo_screenheight()
        L, H = width / 2, height / 2
        X, Y = (width - L) / 2, (height - H) / 2
        self.key_fen.geometry('%dx%d%+d%+d' % (L,H,X,Y))
        self.update_key_bind()

    def update_key_bind(self):
        for widget in self.key_fen.winfo_children():
            widget.place_forget()
        labels = {
            'up': 'Avancer',
    		'down': 'Reculer',
    		'left': 'Gauche',
    		'right': 'Droite',
    		'dash': 'Dash',
    		'dash_preview': 'Aide au dash',
    		'reload': 'Recharger',
    		'panic': 'Panique',
    		'help': 'Aide'}
        for id, key in enumerate(self.config['key_binding'].keys()):
            self.create_key_bind(key, labels[key], id)

        tk.Button(self.key_fen, text='Valider', command=self.validate).place(relx=0.4, rely=0.9, anchor=tk.CENTER)
        tk.Button(self.key_fen, text='Défaut', command=self.default).place(relx=0.6, rely=0.9, anchor=tk.CENTER)

    def create_key_bind(self, key, label, id):
        offset_height = 0.65
        tk.Label(self.key_fen, text=label).place(relx=0.1, rely=(id + offset_height)/10, anchor=tk.W)
        tk.Button(self.key_fen, text=str(self.new_config['key_binding'][key]).capitalize(), command=lambda: self.detect_keypress(key), width=10).place(relx=0.9, rely=(id + offset_height)/10, anchor=tk.E)

    def detect_keypress(self, key):
        new_key = keyboard.read_key()
        if self.platform == 'Darwin' and new_key == 'shift':
            new_key = 56
        self.new_config['key_binding'][key] = new_key
        self.update_key_bind()

    def default(self):
        with open(os.path.join(config_path, 'config_default.json'), 'r') as default:
            self.new_config['key_binding'] = json.load(default)['key_binding']
        self.update_key_bind()


    def validate(self):
        with open(os.path.join(config_path, 'config.json'), 'w') as config:
            config.write(json.dumps(self.new_config))
        self.fen.destroy()
