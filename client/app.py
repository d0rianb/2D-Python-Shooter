#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform
import tkinter as tk
import tkinter.font as tkFont
import threading
import socket
import random
import keyboard
import json

from player import OwnPlayer, OnlinePlayer, Target
from env import Env
from interface import Interface, ChatInfo
from client import Client
from render import Canvas
from map.map import Map

GAME_NAME = '2PQSTD'
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ressources/config/config.json')
ROLES = [('Assault', 'A'), ('Shotgun', 'SG'), ('Sniper', 'S'), ('SMG', 'SMG'), ('Rayon', 'R')]

FULLSCREEN = False
MAP = 'full_map_3.compile.map'

class App:
    def __init__(self, player_name, role):
        self.name = player_name
        self.role = role
        self.fen = tk.Tk()
        self.config = {}
        self.init()

    def init(self):
        self.get_config()
        self.map = Map(MAP, 'map')
        self.canvas = Canvas(self.fen, self.map.width, self.map.height)
        self.env = Env(self.fen, self.map, self.canvas, max_framerate=self.config['max_framerate'])
        self.player = OwnPlayer(0, 50, 50, self.env, self.name, self.role)
        self.player.bind_keys(self.config['key_binding'])
        self.interface = Interface(self.player, self.env)
        self.chat = ChatInfo(self.env)

    def get_config(self):
        with open(config_path, 'r') as settings_file:
            self.config = json.load(settings_file)

    def start(self):
        self.fen.state("zoomed")
        if FULLSCREEN:
            self.fen.wm_attributes('-fullscreen', 'true')
        self.env.update()
        self.fen.mainloop()


class LocalGame(App):
    def __init__(self, player_name, difficulty, role):
        App.__init__(self, player_name, role)
        self.difficulty = difficulty
        self.entry = None
        self.fen.title(GAME_NAME + ' - Local')
        self.fen.bind('<Key-g>', self.restart)

    def restart(self, *event): ## Doesn't work
        if self.env.command_entry_focus: return
        self.env.exit()
        self.start()

    def generate_target(self):
        if self.difficulty == 1:
            Target(1, 400, 40, self.env, level=1)
        else:
            for i in range(self.difficulty):
                Target(i, random.randint(150, self.map.width - 150), random.randint(150, self.map.height - 150), self.env, level=self.difficulty)


class OnlineGame(App):
    def __init__(self, player_name, role):
        App.__init__(self, player_name, role)
        self.connection = None
        self.client = None
        self.fen.title(GAME_NAME + ' - Multi')

    def connect(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = Client(self.connection, self.player, ip, port)
        self.client.send_connection_info()
        self.client.start()


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
        with open(config_path, 'r') as settings_file:
            self.config = json.load(settings_file)

    def create_window(self):
        self.fen.title('Bievenue dans ' + GAME_NAME)
        self.fen.attributes('-topmost', True)
        self.width, self.height = self.fen.winfo_screenwidth(), self.fen.winfo_screenheight()
        L, H = self.width / 3, self.height / 2
        X, Y = (self.width - L) / 2, (self.height - H) / 2
        self.fen.geometry('%dx%d%+d%+d' % (L,H,X,Y))
        self.fen.resizable(width=False, height=False)

        ## Style
        title_font = tkFont.Font(family='Avenir Next', size=35, weight='bold')
        subtitle_font = tkFont.Font(family='Avenir Next', size=22, weight='normal')
        regular_font = tkFont.Font(family='Avenir Next', size=15, weight='normal')

        title = tk.Label(self.fen, text='Bievenue dans ' + GAME_NAME, font=title_font)
        subtitle = tk.Label(self.fen, text='Sélectionnez le mode de jeu : ', font=subtitle_font)

        name_var = tk.StringVar(self.fen, value=self.config['default_name'])
        difficulty_var = tk.IntVar(self.fen, value=self.config['default_difficulty'])

        name_label = tk.Label(self.fen, text='Nom : ', font=regular_font)
        name_entry = tk.Entry(self.fen, textvariable=name_var, width=20)

        role_label = tk.Label(self.fen, text='Role : ', font=regular_font)
        role_list = []
        selected_role = tk.StringVar()
        selected_role.set(self.config['default_role'])
        for (role, value) in ROLES:
            check_box = tk.Radiobutton(self.fen, text=role, value=value, variable=selected_role,
                                        indicatoron=0, width=10, pady=4, selectcolor='blue', relief=tk.SUNKEN)
            role_list.append(check_box)

        difficulty_label = tk.Label(self.fen, text='Difficultée : ', font=regular_font)
        difficulty_scale = tk.Scale(self.fen, variable=difficulty_var, orient='horizontal', from_=0, to=10, resolution=1, length=200, relief=tk.FLAT)

        PvE_button = tk.Button(self.fen, text='Local', command=lambda: handle_click('PvE'), padx=30, pady=5, relief=tk.FLAT)
        PvP_button = tk.Button(self.fen, text='Multi', command=lambda: handle_click('PvP'), padx=30, pady=5, relief=tk.FLAT)

        settings_icon = tk.PhotoImage(file='{}/ressources/open_file.gif'.format(self.path))
        settings = tk.Button(self.fen, text='Settings', relief=tk.FLAT, padx=15, pady=5, command=lambda: self.settings_callback(self))

        ## LAYOUT ##
        title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        subtitle.place(relx=0.5, rely=0.22, anchor=tk.CENTER)

        name_label.place(relx=0.1, rely=0.42, anchor=tk.W)
        name_entry.place(relx=0.8, rely=0.42, anchor=tk.E)

        role_label.place(relx=0.1, rely=0.52, anchor=tk.W)
        role_width = 0.9/len(ROLES)
        for (index, role) in enumerate(role_list):
            role.place(relx=0.05 + index*role_width, rely=0.60, anchor=tk.W)

        difficulty_label.place(relx=0.1, rely=0.74, anchor=tk.W)
        difficulty_scale.place(relx=0.8, rely=0.71, anchor=tk.E)

        PvE_button.place(relx=0.3, rely=0.9, anchor=tk.W)
        PvP_button.place(relx=0.7, rely=0.9, anchor=tk.E)

        settings.place(relx= 0.9, rely=0.9, anchor=tk.CENTER)

        def handle_click(mode):
            self.fen.destroy()
            if mode == 'PvE':
                self.offline_callback(name_var.get(), difficulty_var.get(), selected_role.get())
            elif mode == 'PvP':
                self.online_callback(name_var.get(), self.config['server_ip'], int(self.config['server_port']), selected_role.get())

    def start(self):
        self.fen.mainloop()


class Settings:
    def __init__(self, parent):
        self.parent = parent
        self.config = {}
        self.new_config = {}
        self.platform = platform.system()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.get_config()
        self.create_window()

    def get_config(self):
        with open(config_path, 'r') as file:
            self.config = json.load(file)
            self.new_config = self.config.copy()

    def create_window(self):
        self.fen = tk.Toplevel()
        width, height = self.fen.winfo_screenwidth(), self.fen.winfo_screenheight()
        L, H = width / 2.5, height / 2
        X, Y = (width - L) / 2, (height - H) / 2
        self.fen.geometry('%dx%d%+d%+d' % (L,H,X,Y))

        ## Style
        title_font = tkFont.Font(family='Avenir Next', size=30, weight='bold')
        subtitle_font = tkFont.Font(family='Avenir Next', size=20, weight='normal')
        regular_font = tkFont.Font(family='Avenir Next', size=15, weight='normal')

        max_framerate = tk.IntVar(self.fen, value=self.config['max_framerate'])
        default_difficulty = tk.IntVar(self.fen, value=self.config['default_difficulty'])
        default_role = tk.StringVar(self.fen, value=self.config['default_role'])
        default_ip = tk.StringVar(self.fen, value=self.config['server_ip'])
        default_port = tk.IntVar(self.fen, value=self.config['server_port'])
        default_name = tk.StringVar(self.fen, value=self.config['default_name'])

        title = tk.Label(self.fen, text='Paramètres', font=title_font)
        max_framerate_label = tk.Label(self.fen, text='Framerate Maximum (fps)')
        default_difficulty_label = tk.Label(self.fen, text='Difficulté par défaut (1-10)')
        default_role_label = tk.Label(self.fen, text='Role par défaut')
        default_name_label = tk.Label(self.fen, text='Nom')
        default_ip_label = tk.Label(self.fen, text='Adresse IP par défaut')
        default_port_label = tk.Label(self.fen, text='Port par défaut')

        def validate():
            self.new_config['max_framerate'] = max_framerate.get()
            self.new_config['default_difficulty'] = default_difficulty.get()
            self.new_config['default_role'] = default_role.get()
            self.new_config['server_ip'] = default_ip.get()
            self.new_config['server_port'] = default_port.get()
            self.new_config['default_name'] = default_name.get()
            with open(config_path, 'w') as config:
                config.write(json.dumps(self.new_config))
            self.parent.get_config()
            self.parent.create_window()
            self.fen.destroy()

        max_framerate_entry = tk.Entry(self.fen, textvariable=max_framerate)
        default_difficulty_entry = tk.Entry(self.fen, textvariable=default_difficulty)
        default_name_entry = tk.Entry(self.fen, textvariable=default_name)
        default_ip_entry = tk.Entry(self.fen, textvariable=default_ip)
        default_port_entry = tk.Entry(self.fen, textvariable=default_port)
        keybinding = tk.Button(self.fen, text='Key Bind', command=self.setup_keybind, padx=20, pady=5, relief=tk.FLAT)
        valider = tk.Button(self.fen, text='Valider', command=validate, padx=20, pady=5, relief=tk.FLAT)

        role_list = []
        for (role, value) in ROLES:
            check_box = tk.Radiobutton(self.fen, text=role, value=value, variable=default_role,
                                        indicatoron=0, width=7, pady=2, selectcolor='blue', relief=tk.SUNKEN)
            role_list.append(check_box)

        ## LAYOUT ##
        title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        default_name_label.place(relx=0.1, rely=0.3, anchor=tk.W)
        default_difficulty_label.place(relx=0.1, rely=0.4, anchor=tk.W)
        default_role_label.place(relx=0.1, rely=0.5, anchor=tk.W)
        default_ip_label.place(relx=0.1, rely=0.6, anchor=tk.W)
        default_port_label.place(relx=0.1, rely=0.7, anchor=tk.W)
        max_framerate_label.place(relx=0.1, rely=0.8, anchor=tk.W)

        default_name_entry.place(relx=0.9, rely=0.3, anchor=tk.E)
        default_difficulty_entry.place(relx=0.9, rely=0.4, anchor=tk.E)
        default_ip_entry.place(relx=0.9, rely=0.6, anchor=tk.E)
        default_port_entry.place(relx=0.9, rely=0.7, anchor=tk.E)
        max_framerate_entry.place(relx=0.9, rely=0.8, anchor=tk.E)
        keybinding.place(relx=0.6, rely=0.9, anchor=tk.CENTER)
        valider.place(relx=0.4, rely=0.9, anchor=tk.CENTER)

        role_width = 0.6/len(ROLES)
        for (index, role) in enumerate(role_list):
            role.place(relx=0.35 + index*role_width, rely=0.5, anchor=tk.W)

        self.fen.mainloop()

    def setup_keybind(self):
        self.key_fen = tk.Toplevel(self.fen)
        width, height = self.fen.winfo_screenwidth(), self.fen.winfo_screenheight()
        L, H = width / 2, height / 1.8
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
    		'melee': 'Coup de mêlée',
    		'reload': 'Recharger',
    		'panic': 'Panique',
    		'help': 'Aide'}
        for id, key in enumerate(self.config['key_binding'].keys()):
            self.create_key_bind(key, labels[key], id)

        tk.Button(self.key_fen, text='Valider', command=self.validate, padx=15, pady=2, relief=tk.FLAT).place(relx=0.4, rely=0.9, anchor=tk.CENTER)
        tk.Button(self.key_fen, text='Défaut', command=self.default, padx=15, pady=2, relief=tk.FLAT).place(relx=0.6, rely=0.9, anchor=tk.CENTER)

    def create_key_bind(self, key, label, id):
        offset_height = 0.65
        key_text = 'Shift' if self.new_config['key_binding'][key] == 56 else str(self.new_config['key_binding'][key]).capitalize()
        tk.Label(self.key_fen, text=label).place(relx=0.1, rely=(id + offset_height)/10, anchor=tk.W)
        tk.Button(self.key_fen, text=key_text, command=lambda: self.detect_keypress(key), width=10).place(relx=0.9, rely=(id + offset_height)/10, anchor=tk.E)

    def detect_keypress(self, key):

        new_key = keyboard.read_key()
        if self.platform == 'Darwin' and new_key == 'shift':
            new_key = 56
        self.new_config['key_binding'][key] = new_key
        self.update_key_bind()

    def default(self):
        with open(os.path.join(self.path, 'ressources/config/config_default.json'), 'r') as default:
            self.new_config['key_binding'] = json.load(default)['key_binding']
        self.update_key_bind()

    def validate(self):
        with open(config_path, 'w') as config:
            config.write(json.dumps(self.new_config))
        self.parent.get_config()
        self.fen.destroy()
