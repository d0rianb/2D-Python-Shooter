#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter.font as tkFont
import tkinter as tk
import keyboard
import math

from render import RenderedObject


class Interface:
    def __init__(self, player, env):
        self.player = player
        self.env = env
        self.env.interface = self
        self.player.interface = self
        self.margin_x = 8
        self.margin_y = 20
        self.x = self.env.viewArea['x']
        self.y = self.env.viewArea['y']
        self.width = self.env.viewArea['width']
        self.height = self.env.viewArea['height']
        self.padding = 20
        self.informations = {}
        self.color = '#92959b'
        self.font = tkFont.Font(family='Avenir Next', size=16, weight='normal')

    def display_help(self, *args):
        text = (' Se déplacer : {up}, {down}, {left}, {right}\n' +
               ' Tirer : Clic Droit\n' +
               ' Dash : {dash}\n' +
               ' Recharger : {reload}\n' +
               ' Restart Game: G (only local)\n' +
               ' Toggle Dash Preview: {dash_preview}\n' +
               ' Display Help : {help}\n' +
               ' Panic : {panic} ').format(**{key: str(val).upper() if val != 56 else 'Shift' for key, val in self.player.key.items()})
        self.env.rendering_stack.append(RenderedObject('text', self.env.width/2, 100, text=text, font=self.font, color=self.color, zIndex=10))

    def parse(self, position, x, y, anchor):
        infos = self.informations[position]
        for (index, info) in enumerate(infos):
            self.env.rendering_stack.append(RenderedObject('text', x, y + index*self.padding,
                text='{0}: {1}'.format(info, infos[info]),
                anchor=anchor,
                color=self.color,
                font=self.font))

    def update(self):
        self.x = self.env.viewArea['x']
        self.y = self.env.viewArea['y']
        self.width = self.env.viewArea['width']
        self.height = self.env.viewArea['height']
        self.informations = {
            'TopLeft': {
                'FrameRate': self.env.framerate,
                'Ping': '{0:.2g} ms'.format(self.player.client.ping) if self.player.client else 0
            },
            'TopRight': {
                'People Alive': len(list(filter(lambda player: player.alive, self.env.players))),
                'Kills': len(self.player.kills),
                'Assists': len(self.player.assists)
            },
            'BottomRight': {
                'Health': math.ceil(self.player.health),
                'Ammo': self.player.weapon.ammo if not self.player.weapon.is_reloading else 'Rechargement',
                'Dash': self.player.dash_left
            }
        }

    def render(self):
        for position in self.informations:
            x, y = self.x + self.margin_x, self.y + self.margin_y
            anchor = 'w'
            if position == 'TopRight' or position == 'BottomRight':
                x = self.x + self.width - self.margin_x
                anchor = 'e'
            if position == 'BottomRight':
                y = self.y + self.height - len(self.informations['BottomRight'])*self.padding
            self.parse(position, x, y, anchor)


class ChatInfo:
    def __init__(self, env):
        self.env = env
        self.message = {}
        self.text = tk.StringVar()
        self.entry = tk.Entry(self.env.fen, width=50, bd=0, takefocus=0, highlightthickness=0, textvariable=self.text)
        self.entry_y = 0
        keyboard.on_press_key('/', self.focus_entry)
        keyboard.on_press_key('esc', self.unfocus_entry)
        keyboard.on_press_key('enter', self.parse)

    def focus_entry(self, *event):
        if self.entry_y == 0:
            entry_height = self.entry.winfo_height()
            self.entry_y = (self.env.height - entry_height) / self.env.height
        self.entry.place(relx=0, rely=self.entry_y, anchor=tk.SW)
        self.entry.focus()
        self.entry.selection_range(0, tk.END)
        self.env.command_entry_focus = True

    def unfocus_entry(self, *event):
        self.entry.place_forget()
        self.env.command_entry_focus = False

    def parse(self, *event):
        split = self.text.get().split(' ')
        command, *args = split
        if command == 'debug':
            type, value = args[0], args[1]
            self.debug(type, value)
        elif command == 'kill' or command == 'killall': ## Doesn't work
            if len(args) > 0:
                if args[0] == 'bot' or args[0] == 'bots':
                    self.env.players = [player for player in self.env.players if player.own]
                else:
                    player = self.select_player(args[0], args[1])
                    self.env.players.remove(player)
            else:
                self.env.players = []


    def debug(self, type, value):
        debug_fen = tk.Toplevel(self.env.fen)
        player = self.select_player(type, value)
        for key, val in player.__dict__.items():
            entry = tk.Label(debug_fen, text='{}: {}'.format(key, val))
            entry.pack(anchor=tk.W)

    def select_player(self, type, value):
        ''' return the first player where player.type = value '''
        for player in self.env.players:
            if str(player.__dict__[type]) == value:
                return player

    def update(self):
        pass

    def render(self):
        pass

class InterfaceMessage:
    def __init__(self, interface, type, text):
        self.interface = interface
        self.type = type
        self.text = text

        self.x = interface.env.viewArea['x'] / 2
        self.y = interface.env.viewArea['y'] / 2

        if self.type == 'info':
            self.color = "#AAA"

    def update(self):
        self.y += 1
        self.color

    def render(self):
        pass
