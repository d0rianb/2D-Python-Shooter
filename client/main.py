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

from test import profile
from app import LocalGame, OnlineGame, SplashScreen, Settings

MODE = 'debug' # 'normal / profile / debug'

def start_local_game(name, difficulty, role):
    app = LocalGame(name, difficulty, role)
    app.generate_target()
    app.start()

def start_online_game(name, ip, port, role):
    app = OnlineGame(name, role)
    app.connect(ip, port)
    app.start()

def toggle_settings(splash_screen):
    splash_screen.fen.attributes('-topmost', False)
    settings = Settings()

def parse_args(argv):
    global MODE
    for arg in argv:
        if '=' in arg:
            key, val = arg.split('=')
            if key == 'mode':
                MODE = val
        elif '-' in arg:
            pass

if __name__ == '__main__':
    if len(sys.argv) > 1: parse_args(sys.argv)
    splash_screen = SplashScreen(start_online_game, start_local_game, toggle_settings)
    splash_screen.create_window()
    splash_screen.start()
    sys.exit(0)
