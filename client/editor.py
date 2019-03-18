#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import os, platform, sys

from test import profile
from render import Canvas
from map.editor.env import Env
from map.editor.map import Map
from map.editor.camera import Camera
from map.editor.interface import Interface
from map.editor.settings import EditorSettings

class Editor:
    def __init__(self):
        self.dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'map', 'files')
        self.fen = tk.Tk()
        self.fen.title('Editeur de map')
        self.map_width = 4096
        self.map_height = 2304
        self.canvas = Canvas(self.fen, self.map_width, self.map_height)
        self.env = Env(self.fen, self.canvas, self.map_width, self.map_height)
        self.map = Map(self.env, self.dir)
        self.camera = Camera(100, 100, self.env)
        self.interface = Interface(self.camera, self.env)
        # self.start()

    def start(self):
        self.env.bind()
        self.env.update()
        self.fen.mainloop()

if __name__ == '__main__':
    editor = Editor()
    settings = EditorSettings(editor)
    editor.start()
    sys.exit(0)
