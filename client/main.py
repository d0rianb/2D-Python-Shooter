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

from app import LocalGame, OnlineGame, SplashScreen


def start_local_game(name, difficulty=5):
    app = LocalGame(name, difficulty)
    app.generate_target()
    app.start()

def start_online_game(name, ip, port):
    app = OnlineGame(name)
    app.connect(ip, port)
    app.start()



if __name__ == '__main__':
    splash_screen = SplashScreen(start_online_game, start_local_game)
    splash_screen.create_window()
    splash_screen.start()
    sys.exit(0)
