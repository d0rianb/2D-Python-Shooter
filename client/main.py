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

from app import LocalGame, OnlineGame, SplashScreen, Settings


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

if __name__ == '__main__':
    splash_screen = SplashScreen(start_online_game, start_local_game, toggle_settings)
    splash_screen.create_window()
    splash_screen.start()
    sys.exit(0)
