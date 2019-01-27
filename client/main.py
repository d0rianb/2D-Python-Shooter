#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkFont
import os
import sys
import math
import random
import keyboard
import socket
from player import Player, Target
from tir import Tir
from env import Env
from interface import Interface
from map.map import Map

GAME_NAME = '2PQSTD'
SERVER_HOST = 'localhost'
SERVER_PORT = 12800

def connect():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((SERVER_HOST, SERVER_PORT))
    print("Connection on {}".format(SERVER_PORT))
    connection.send(b"Test de message")

def start_game(mode):
    fen = tk.Tk()
    fen.title(GAME_NAME)
    width, height = fen.winfo_screenwidth(), 840#fen.winfo_screenheight()

    canvas = tk.Canvas(fen, width=width, height=height, bg='#F1E7DC', highlightthickness=0)
    fen.bind('<Key-g>', lambda *args: start_game('PvE'))

    env = Env(fen, width, height, canvas)
    map = Map(env, 'map1.txt', 'Test')

    dorian = Player(0, 50, 50, env, 'Dorian', own=True)
    if mode == 'PvE':
        for i in range(1, 5):
            Target(i, random.randint(150, width - 150), random.randint(150, height - 150), env)
    elif mode == 'PvP':
        connect()

    interface = Interface(dorian, env)
    env.update()
    interface.update()
    fen.mainloop()


def splash_screen():
    global GAME_IS_RUNNING
    fen = tk.Tk()
    fen.title('Bievenue dans ' + GAME_NAME)
    fen.attributes("-topmost", True)
    width, height = fen.winfo_screenwidth(), fen.winfo_screenheight()
    L, H = width / 3, height / 3
    X, Y = (width - L) / 2, (height - H)/2
    fen.geometry('%dx%d%+d%+d' % (L,H,X,Y))
    fen.resizable(width=False, height=False)

    title_font = tkFont.Font(family='Avenir Next', size=30, weight='bold')
    subtitle_font = tkFont.Font(family='Avenir Next', size=20, weight='normal')

    def handle_click(mode, fen):
        fen.destroy()
        start_game(mode)

    title = tk.Label(fen, text='Bievenue dans ' + GAME_NAME, font=title_font)
    subtitle = tk.Label(fen, text='Sélectionnez le mode de jeu : ', font=subtitle_font)
    PvE_button = tk.Button(fen, text='Local', command=lambda: handle_click('PvE', fen), padx=30, pady=20, relief=tk.FLAT)
    PvP_button = tk.Button(fen, text='Multi', command=lambda: handle_click('PvP', fen), padx=30, pady=20, relief=tk.FLAT)


    title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    subtitle.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    PvE_button.place(relx=0.3, rely=0.5, anchor=tk.W)
    PvP_button.place(relx=0.7, rely=0.5, anchor=tk.E)
    fen.mainloop()

def settings():
    pass

if __name__ == '__main__':
    #start_game('PvE')
    splash_screen()
    sys.exit(0)
