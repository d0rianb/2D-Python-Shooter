#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkFont

class EditorSettings:
    def __init__(self, editor):
        self.editor = editor
        self.env = self.editor.env
        self.map = self.editor.map
        self.fen = tk.Toplevel(self.editor.fen)
        self.fen.title('Editor Settings')
        self.create_window()

    def create_window(self):
        self.width, self.height = self.fen.winfo_screenwidth(), self.fen.winfo_screenheight()
        L, H = self.width / 3, self.height / 2
        X, Y = (self.width - L) / 2, (self.height - H) / 2
        self.fen.geometry('%dx%d%+d%+d' % (L,H,X,Y))

        ## Style
        title_font = tkFont.Font(family='Avenir Next', size=35, weight='bold')
        subtitle_font = tkFont.Font(family='Avenir Next', size=22, weight='normal')
        regular_font = tkFont.Font(family='Avenir Next', size=15, weight='normal')

        title = tk.Label(self.fen, text='Editeur de Map', font=title_font)

        grid_width_var = tk.IntVar(self.fen, value=128)
        grid_height_var = tk.IntVar(self.fen, value=72)
        multiplier_var = tk.IntVar(self.fen, value=1)

        name_label = tk.Label(self.fen, text='Nom : ', font=regular_font)
        #name_entry = tk.Entry(self.fen, textvariable=name_var, width=20)

        name = '_'
        grid_width = 'X'
        grid_height = 'X'
        multiplier = 'X'
        symetry_axis = '_'
        symetry_destructive = '_'
